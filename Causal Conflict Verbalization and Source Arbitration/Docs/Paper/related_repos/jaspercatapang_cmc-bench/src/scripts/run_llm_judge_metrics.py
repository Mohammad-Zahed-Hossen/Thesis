#!/usr/bin/env python3
"""
Run LLM-as-judge on *_predictions_complete.jsonl and aggregate CMC-Bench metrics.

Expects OpenAI-compatible API credentials in the environment (e.g. AZURE_OPENAI_*)
or in a file passed via --env. See src/.env.example.
"""
from __future__ import annotations

import argparse
import asyncio
import json
import sys
import time
from pathlib import Path
from typing import Any

from tqdm import tqdm
from tqdm.asyncio import tqdm as tqdm_async

# Repo layout: run from project root with PYTHONPATH=src
_SRC = Path(__file__).resolve().parents[1]
if str(_SRC) not in sys.path:
    sys.path.insert(0, str(_SRC))

from data.schema import InstanceRecord
from evaluation.azure_judge import (
    JUDGE_PROMPT_VERSION,
    async_judge_row_with_retries,
    create_async_azure_client,
    judge_row_with_retries,
    load_env_file,
)
from evaluation.judge_report import judge_label_breakdown
from evaluation.metrics import compute_all_metrics_from_judge


def _load_instances(path: Path) -> tuple[list[dict], dict[str, dict]]:
    records: list[dict] = []
    by_id: dict[str, dict] = {}
    with path.open(encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            d = json.loads(line)
            rec = InstanceRecord.model_validate(d).model_dump()
            records.append(rec)
            by_id[rec["instance_id"]] = rec
    return records, by_id


def _pred_file_stem(path: Path) -> str:
    return path.name.replace("_predictions_complete.jsonl", "").replace(".jsonl", "")


def _norm_model_key(name: str) -> str:
    return name.strip().lower().replace(".", "_")


def _filter_pred_files(paths: list[Path], models: list[str] | None) -> list[Path]:
    if not models:
        return paths
    allow = {_norm_model_key(m) for m in models}
    out = [p for p in paths if _norm_model_key(_pred_file_stem(p)) in allow]
    return out


def _load_done_ids(path: Path) -> set[str]:
    if not path.is_file():
        return set()
    done: set[str] = set()
    with path.open(encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            done.add(json.loads(line)["instance_id"])
    return done


async def _judge_pending_parallel(
    *,
    pending: list[tuple[dict, dict, str, str]],
    stem: str,
    max_completion_tokens: int,
    use_json_object_mode: bool,
    concurrency: int,
    sleep_s: float,
    tqdm_disable: bool = False,
) -> list[dict]:
    sem = asyncio.Semaphore(max(1, concurrency))
    async with create_async_azure_client(120.0) as client:

        async def one(
            idx: int, row: dict, rec: dict, pred_ans: str, cond: str
        ) -> tuple[int, dict[str, Any]]:
            inst = row["instance_id"]
            async with sem:
                try:
                    j = await async_judge_row_with_retries(
                        client=client,
                        query=row.get("query", rec.get("query", "")),
                        gold_answer=row.get("gold_answer", rec["gold_answer"]),
                        text_answer=row.get("text_answer", rec["text_answer"]),
                        model_answer=pred_ans,
                        condition=str(cond),
                        max_completion_tokens=max_completion_tokens,
                        use_json_object_mode=use_json_object_mode,
                    )
                except Exception as e:
                    tqdm.write(f"judge failed {inst}: {e}", file=sys.stderr)
                    raise
                if sleep_s > 0:
                    await asyncio.sleep(sleep_s)
            b = _behavioral_from_judge(inst, stem, j, pred_ans, str(cond))
            return idx, b

        tasks = [
            one(i, row, rec, pa, c)
            for i, (row, rec, pa, c) in enumerate(pending)
        ]
        ordered = await tqdm_async.gather(
            *tasks,
            desc=f"judge:{stem}",
            disable=tqdm_disable,
        )
    ordered.sort(key=lambda x: x[0])
    return [b for _, b in ordered]


def _behavioral_from_judge(
    instance_id: str,
    model: str,
    judge: dict,
    predicted_answer: str,
    condition: str,
) -> dict:
    mi = judge["matches_image"]
    mt = judge["matches_text"]
    abst = judge["abstains"]
    matches_neither = (not mi) and (not mt)
    return {
        "instance_id": instance_id,
        "model": model,
        "condition": condition,
        "answer": predicted_answer,
        "judge_label": judge.get("judge_label", ""),
        "judge_prompt_version": judge.get("judge_prompt_version", ""),
        "matches_image": mi,
        "matches_text": mt,
        "matches_neither": matches_neither,
        "flags_disagreement": abst,
        "judge_raw": judge.get("raw_content", ""),
    }


def main() -> None:
    ap = argparse.ArgumentParser(description="LLM judge metrics for complete predictions JSONL")
    ap.add_argument(
        "--instances",
        type=Path,
        default=Path("outputs/cmc_bench_instances.jsonl"),
        help="Benchmark instances JSONL",
    )
    ap.add_argument(
        "--predictions",
        type=Path,
        nargs="+",
        help="One or more *_predictions_complete.jsonl files",
    )
    ap.add_argument(
        "--predictions-dir",
        type=Path,
        help="If set, glob *_predictions_complete.jsonl under this directory",
    )
    ap.add_argument(
        "--models",
        nargs="+",
        metavar="NAME",
        help=(
            "Only judge these models (prediction file stem). "
            "Matches *_predictions_complete.jsonl, e.g. gemma-3n-e2b or lfm2.5-vl-1.6b → lfm2_5-vl-1_6b."
        ),
    )
    ap.add_argument(
        "--flush-every",
        type=int,
        default=50,
        metavar="N",
        help=(
            "Append and flush behavioral JSONL every N new rows. "
            "Parallel: run at most N API calls per asyncio batch (still up to --concurrency at once). "
            "Use 0 for one batch for all pending (no incremental disk). "
            "Serial (--concurrency 1): 0 means flush after every row."
        ),
    )
    ap.add_argument("--out-dir", type=Path, default=Path("outputs/judge"))
    ap.add_argument("--env", type=Path, help="Load KEY=VALUE into environment (overrides existing keys)")
    ap.add_argument("--max-rows", type=int, default=0, help="Cap rows per file (0 = all)")
    ap.add_argument(
        "--concurrency",
        type=int,
        default=12,
        metavar="N",
        help="Parallel in-flight judge requests (default 12). Use 1 for fully serial.",
    )
    ap.add_argument(
        "--sleep",
        type=float,
        default=0.0,
        help="Seconds to sleep after each call when --concurrency is 1 (ignored if concurrency>1).",
    )
    ap.add_argument("--resume", action="store_true", help="Skip instance_ids already in behavioral JSONL")
    ap.add_argument("--max-completion-tokens", type=int, default=2048)
    ap.add_argument(
        "--no-json-object-mode",
        action="store_true",
        help="Do not send response_format=json_object (if the deployment returns 400)",
    )
    args = ap.parse_args()

    if args.env:
        load_env_file(args.env, override=True)
    else:
        load_env_file(_SRC / ".env", override=False)

    records, by_id = _load_instances(args.instances)
    pred_files: list[Path] = []
    if args.predictions:
        pred_files.extend(args.predictions)
    if args.predictions_dir:
        pred_files.extend(sorted(args.predictions_dir.glob("*_predictions_complete.jsonl")))
    if not pred_files:
        ap.error("Provide --predictions and/or --predictions-dir")

    pred_files = _filter_pred_files(pred_files, args.models)
    if not pred_files:
        ap.error("No prediction files left after --models filter")

    args.out_dir.mkdir(parents=True, exist_ok=True)
    summary: dict[str, dict] = {}

    for pf in pred_files:
        if not pf.is_file():
            print(f"skip missing file: {pf}", file=sys.stderr)
            continue
        stem = _pred_file_stem(pf)
        out_jsonl = args.out_dir / f"behavioral_{stem}.jsonl"
        done = _load_done_ids(out_jsonl) if args.resume else set()

        behavioral: list[dict] = []
        if args.resume and out_jsonl.is_file():
            with out_jsonl.open(encoding="utf-8") as f:
                for line in f:
                    line = line.strip()
                    if not line:
                        continue
                    behavioral.append(json.loads(line))

        pending: list[tuple[dict, dict, str, str]] = []
        with pf.open(encoding="utf-8") as pred_f:
            for line in pred_f:
                line = line.strip()
                if not line:
                    continue
                row = json.loads(line)
                inst = row["instance_id"]
                if inst in done:
                    continue
                rec = by_id.get(inst)
                if rec is None:
                    print(f"unknown instance_id {inst}, skipping", file=sys.stderr)
                    continue
                pred_ans = row.get("predicted_answer", "")
                cond = rec["condition"]
                pending.append((row, rec, pred_ans, str(cond)))
                if args.max_rows and len(pending) >= args.max_rows:
                    break

        mode = "a" if args.resume and out_jsonl.is_file() else "w"
        fe = args.flush_every
        if pending:
            if args.concurrency <= 1:
                buf: list[dict] = []
                with out_jsonl.open(mode, encoding="utf-8") as out_f:
                    pbar = tqdm(
                        pending,
                        desc=f"judge:{stem}",
                        unit="call",
                        total=len(pending),
                        dynamic_ncols=True,
                    )
                    for row, rec, pred_ans, cond in pbar:
                        inst = row["instance_id"]
                        try:
                            j = judge_row_with_retries(
                                query=row.get("query", rec.get("query", "")),
                                gold_answer=row.get("gold_answer", rec["gold_answer"]),
                                text_answer=row.get("text_answer", rec["text_answer"]),
                                model_answer=pred_ans,
                                condition=str(cond),
                                max_completion_tokens=args.max_completion_tokens,
                                use_json_object_mode=not args.no_json_object_mode,
                            )
                        except Exception as e:
                            tqdm.write(f"judge failed {inst}: {e}", file=sys.stderr)
                            raise
                        b = _behavioral_from_judge(inst, stem, j, pred_ans, str(cond))
                        behavioral.append(b)
                        if fe <= 0:
                            out_f.write(json.dumps(b, ensure_ascii=False) + "\n")
                            out_f.flush()
                        else:
                            buf.append(b)
                            if len(buf) >= fe:
                                for x in buf:
                                    out_f.write(json.dumps(x, ensure_ascii=False) + "\n")
                                out_f.flush()
                                buf.clear()
                        if args.sleep > 0:
                            time.sleep(args.sleep)
                    if buf:
                        for x in buf:
                            out_f.write(json.dumps(x, ensure_ascii=False) + "\n")
                        out_f.flush()
            else:
                with out_jsonl.open(mode, encoding="utf-8") as out_f:
                    if fe <= 0:
                        new_batch = asyncio.run(
                            _judge_pending_parallel(
                                pending=pending,
                                stem=stem,
                                max_completion_tokens=args.max_completion_tokens,
                                use_json_object_mode=not args.no_json_object_mode,
                                concurrency=args.concurrency,
                                sleep_s=0.0,
                                tqdm_disable=False,
                            )
                        )
                        for b in new_batch:
                            out_f.write(json.dumps(b, ensure_ascii=False) + "\n")
                        out_f.flush()
                        behavioral.extend(new_batch)
                    else:
                        pbar = tqdm(
                            total=len(pending),
                            desc=f"judge:{stem}",
                            unit="call",
                            dynamic_ncols=True,
                        )
                        for off in range(0, len(pending), fe):
                            chunk = pending[off : off + fe]
                            new_batch = asyncio.run(
                                _judge_pending_parallel(
                                    pending=chunk,
                                    stem=stem,
                                    max_completion_tokens=args.max_completion_tokens,
                                    use_json_object_mode=not args.no_json_object_mode,
                                    concurrency=args.concurrency,
                                    sleep_s=0.0,
                                    tqdm_disable=True,
                                )
                            )
                            for b in new_batch:
                                out_f.write(json.dumps(b, ensure_ascii=False) + "\n")
                            out_f.flush()
                            behavioral.extend(new_batch)
                            pbar.update(len(chunk))
                        pbar.close()

        if not behavioral:
            print(f"no behavioral rows for {pf.name}, skipping metrics", file=sys.stderr)
            continue
        metrics = compute_all_metrics_from_judge(records, behavioral, model_name=stem)
        judge_label_counts, judge_label_counts_by_condition = judge_label_breakdown(behavioral)
        summary[stem] = {
            **metrics,
            "judge_prompt_version": JUDGE_PROMPT_VERSION,
            "judge_label_counts": judge_label_counts,
            "judge_label_counts_by_condition": judge_label_counts_by_condition,
            "n_behavioral_rows": len(behavioral),
        }

    summary_path = args.out_dir / "metrics_judge_summary.json"
    merged_summary: dict[str, dict] = {}
    if summary_path.is_file():
        try:
            merged_summary = json.loads(summary_path.read_text(encoding="utf-8"))
            if not isinstance(merged_summary, dict):
                merged_summary = {}
        except (json.JSONDecodeError, OSError):
            merged_summary = {}
    merged_summary.update(summary)
    summary_path.write_text(
        json.dumps(merged_summary, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    print(f"wrote {summary_path} ({len(summary)} model(s) this run, {len(merged_summary)} total)")


if __name__ == "__main__":
    main()
