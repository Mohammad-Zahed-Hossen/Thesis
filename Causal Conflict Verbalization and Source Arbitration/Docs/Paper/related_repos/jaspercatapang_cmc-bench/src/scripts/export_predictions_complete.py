#!/usr/bin/env python3
"""
Join prediction JSONL with cmc_bench_instances.jsonl and extract plain text from
GenerationResult(text='...') when present.

Output rows: instance_id, query, gold_answer, text_answer, predicted_answer.

- For each *_predictions.jsonl (non-complete), writes *_predictions_complete.jsonl.
- If no raw prediction files exist, re-reads *_predictions_complete.jsonl and
  overwrites them (same path) so fields like text_answer stay in sync.
"""
import argparse
import json
import re
import sys
from pathlib import Path

_ROOT = Path(__file__).resolve().parents[1]
if str(_ROOT) not in sys.path:
    sys.path.insert(0, str(_ROOT))
_REPO = _ROOT.parent
if str(_REPO) not in sys.path:
    sys.path.insert(0, str(_REPO))


def extract_generation_result_text(answer: str) -> str:
    """Pull the string passed as text=... inside GenerationResult(...)."""
    s = answer.strip()
    if not s.startswith("GenerationResult("):
        return s
    m = re.search(r"\btext=(['\"])", s)
    if not m:
        return s
    quote = m.group(1)
    i = m.end()
    out: list[str] = []
    while i < len(s):
        c = s[i]
        if c == "\\" and i + 1 < len(s):
            nxt = s[i + 1]
            if nxt == "n":
                out.append("\n")
            elif nxt == "t":
                out.append("\t")
            elif nxt == "r":
                out.append("\r")
            elif nxt in "\\\"'":
                out.append(nxt)
            else:
                out.append(nxt)
            i += 2
            continue
        if c == quote:
            return "".join(out)
        out.append(c)
        i += 1
    return "".join(out)


def load_instances_by_id(path: Path) -> dict[str, dict]:
    by_id: dict[str, dict] = {}
    with open(path, encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            row = json.loads(line)
            iid = row.get("instance_id")
            if iid:
                by_id[str(iid)] = row
    return by_id


def main() -> None:
    p = argparse.ArgumentParser(description="Export enriched prediction JSONL files")
    p.add_argument(
        "--instances",
        type=Path,
        default=_REPO / "outputs" / "cmc_bench_instances.jsonl",
        help="Benchmark instances JSONL (query, gold_answer, text_answer, ...)",
    )
    p.add_argument(
        "--predictions-dir",
        type=Path,
        default=_REPO / "outputs" / "predictions",
        help="Directory with *_predictions.jsonl and/or *_predictions_complete.jsonl",
    )
    p.add_argument(
        "--dry-run",
        action="store_true",
        help="Print output paths only",
    )
    args = p.parse_args()

    inst_path = args.instances.resolve()
    pred_dir = args.predictions_dir.resolve()
    if not inst_path.is_file():
        print(f"Missing instances file: {inst_path}", file=sys.stderr)
        sys.exit(1)
    if not pred_dir.is_dir():
        print(f"Missing predictions dir: {pred_dir}", file=sys.stderr)
        sys.exit(1)

    by_id = load_instances_by_id(inst_path)
    print(f"Loaded {len(by_id)} instances from {inst_path.name}")

    raw_files = sorted(
        f
        for f in pred_dir.iterdir()
        if f.is_file()
        and f.suffix == ".jsonl"
        and f.name.endswith("_predictions.jsonl")
        and "_complete" not in f.name
    )
    complete_only = sorted(
        f
        for f in pred_dir.iterdir()
        if f.is_file()
        and f.name.endswith("_predictions_complete.jsonl")
    )
    if raw_files:
        jobs = [(p, p.with_name(f"{p.stem}_complete.jsonl")) for p in raw_files]
    elif complete_only:
        jobs = [(p, p) for p in complete_only]
    else:
        print(f"No *_predictions.jsonl or *_predictions_complete.jsonl in {pred_dir}", file=sys.stderr)
        sys.exit(1)

    for pred_path, out_path in jobs:
        if args.dry_run:
            print(f"Would write {out_path.name}")
            continue

        with open(pred_path, encoding="utf-8") as fin:
            in_lines = [ln.strip() for ln in fin if ln.strip()]

        n_ok, n_miss = 0, 0
        out_lines: list[str] = []
        for line in in_lines:
            pr = json.loads(line)
            iid = str(pr.get("instance_id", ""))
            rec = by_id.get(iid)
            raw_ans = pr.get("answer")
            if raw_ans is None:
                raw_ans = pr.get("predicted_answer", "")
            if not isinstance(raw_ans, str):
                raw_ans = str(raw_ans)
            predicted = extract_generation_result_text(raw_ans)
            if rec:
                n_ok += 1
                row = {
                    "instance_id": iid,
                    "query": rec.get("query", ""),
                    "gold_answer": rec.get("gold_answer", ""),
                    "text_answer": rec.get("text_answer", ""),
                    "predicted_answer": predicted,
                }
            else:
                n_miss += 1
                row = {
                    "instance_id": iid,
                    "query": "",
                    "gold_answer": "",
                    "text_answer": "",
                    "predicted_answer": predicted,
                }
            out_lines.append(json.dumps(row, ensure_ascii=False))

        with open(out_path, "w", encoding="utf-8") as fout:
            fout.write("\n".join(out_lines) + "\n")

        action = "Overwrote" if pred_path == out_path else "Wrote"
        print(f"{action} {out_path.name} ({n_ok} matched, {n_miss} missing instance)")

    if args.dry_run:
        print("(dry-run: no files written)")


if __name__ == "__main__":
    main()
