#!/usr/bin/env python3
"""
Run evaluation: load instances, run VLMs via mlx-vlm, compute metrics.
Supports --resume to continue after interruption; periodic atomic writes via --flush-every.
"""
import argparse
import gc
import json
import os
import sys
from pathlib import Path

_ROOT = Path(__file__).resolve().parents[1]
if str(_ROOT) not in sys.path:
    sys.path.insert(0, str(_ROOT))
_REPO = _ROOT.parent
if str(_REPO) not in sys.path:
    sys.path.insert(0, str(_REPO))

import yaml
from tqdm import tqdm

from data.io import load_instances_jsonl
from data.schema import InstanceRecord
from evaluation.inference import load_image_for_record, run_inference
from evaluation.metrics import compute_all_metrics
from evaluation.model_loader import load_model, MODEL_CONFIGS


def load_predictions_by_instance_id(path: Path) -> dict[str, dict]:
    by_id: dict[str, dict] = {}
    if not path.exists():
        return by_id
    with open(path, encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            try:
                row = json.loads(line)
            except json.JSONDecodeError:
                continue
            iid = row.get("instance_id")
            if iid:
                by_id[str(iid)] = row
    return by_id


def write_predictions_jsonl_atomic(pred_path: Path, records: list, by_id: dict[str, dict]) -> None:
    """Write predictions in dataset order (one line per record that has a prediction)."""
    tmp = pred_path.with_suffix(pred_path.suffix + ".tmp")
    with open(tmp, "w", encoding="utf-8") as f:
        for rec in records:
            iid = rec.instance_id
            p = by_id.get(iid)
            if p is not None:
                f.write(json.dumps(p, ensure_ascii=False) + "\n")
    tmp.replace(pred_path)


def predictions_in_record_order(
    records: list, by_id: dict[str, dict], model_name: str
) -> tuple[list[dict], int]:
    """Align preds to records; missing rows get empty answer. Returns (list, n_missing)."""
    out: list[dict] = []
    missing = 0
    for r in records:
        p = by_id.get(r.instance_id)
        if p is None:
            missing += 1
            out.append({"instance_id": r.instance_id, "answer": "", "model": model_name})
        else:
            out.append(p)
    return out, missing


def parse_args():
    p = argparse.ArgumentParser(description="CMC-Bench evaluation")
    p.add_argument("--config", default=str(_ROOT / "configs" / "default.yaml"))
    p.add_argument("--instances", default=None)
    p.add_argument(
        "--models",
        nargs="+",
        default=None,
        metavar="NAME",
        help=f"Subset of models to run (default: all). Keys: {', '.join(MODEL_CONFIGS)}.",
    )
    p.add_argument("--predictions-dir", default=None)
    p.add_argument("--max-instances", type=int, default=None)
    p.add_argument("--skip-inference", action="store_true")
    p.add_argument(
        "--resume",
        action="store_true",
        help="Load existing predictions for this model and only run missing instance_ids.",
    )
    p.add_argument(
        "--flush-every",
        type=int,
        default=50,
        metavar="N",
        help="After N new predictions, rewrite the jsonl atomically (0 = only at end). Default 50.",
    )
    return p.parse_args()


def main():
    args = parse_args()
    with open(args.config) as f:
        cfg = yaml.safe_load(f)
    paths = cfg.get("paths", {})
    data_dir = Path(paths.get("data_dir", "./data_cache")).resolve()
    data_dir.mkdir(parents=True, exist_ok=True)
    os.environ.setdefault("HF_HOME", str(data_dir / "hf_cache"))
    instances_path = args.instances or paths.get("instances_jsonl", "./outputs/cmc_bench_instances.jsonl")
    pred_dir = Path(args.predictions_dir or paths.get("predictions_dir", "./outputs/predictions"))
    pred_dir.mkdir(parents=True, exist_ok=True)

    records = load_instances_jsonl(instances_path)
    if not records:
        print(f"No instances at {instances_path}. Run make data first.")
        return
    if records and isinstance(records[0], dict):
        records = [InstanceRecord.model_validate(r) for r in records]
    if args.max_instances:
        records = records[: args.max_instances]
    print(f"Loaded {len(records)} instances")

    model_names = args.models or list(MODEL_CONFIGS)
    all_metrics = {}

    for model_name in model_names:
        pred_path = pred_dir / f"{model_name.replace('.', '_')}_predictions.jsonl"
        gen_extra = (MODEL_CONFIGS.get(model_name) or {}).get("generate_kwargs")
        if not args.skip_inference:
            by_id: dict[str, dict] = {}
            if args.resume and pred_path.exists():
                by_id = load_predictions_by_instance_id(pred_path)
                print(f"  Resume: loaded {len(by_id)} existing predictions from {pred_path.name}")
            n_pending = sum(1 for r in records if r.instance_id not in by_id)
            if n_pending == 0:
                print(f"  All {len(records)} instances already in {pred_path.name}; skipping load/inference")
                write_predictions_jsonl_atomic(pred_path, records, by_id)
            else:
                print(f"\nLoading model: {model_name} ({n_pending} instances to run)")
                try:
                    model, processor, config = load_model(model_name)
                except Exception as e:
                    print(f"  Failed to load: {e}")
                    continue
                new_count = 0
                bar = tqdm(
                    records,
                    desc=model_name,
                    unit="inst",
                    total=len(records),
                    dynamic_ncols=True,
                )
                for rec in bar:
                    if rec.instance_id in by_id:
                        continue
                    img_path = load_image_for_record(rec)
                    if img_path is None:
                        out = {"instance_id": rec.instance_id, "answer": "[No image]", "model": model_name}
                    else:
                        out = run_inference(
                            model,
                            processor,
                            config,
                            rec,
                            img_path,
                            generate_kwargs=gen_extra,
                        )
                        out["model"] = model_name
                    by_id[rec.instance_id] = out
                    new_count += 1
                    fe = args.flush_every
                    if fe > 0 and new_count % fe == 0:
                        write_predictions_jsonl_atomic(pred_path, records, by_id)
                        tqdm.write(f"  {model_name}: flushed {len(by_id)}/{len(records)} to disk")
                    bar.set_postfix(on_disk=len(by_id), refresh=False)
                write_predictions_jsonl_atomic(pred_path, records, by_id)
                print(f"  Wrote {pred_path} ({len(by_id)}/{len(records)} instances)")
                del model, processor, config
                gc.collect()
            predictions, n_miss = predictions_in_record_order(records, by_id, model_name)
            if n_miss:
                print(
                    f"  Warning: incomplete run ({len(records) - n_miss}/{len(records)} predicted); "
                    "metrics treat missing rows as empty answers"
                )
        else:
            if not pred_path.exists():
                print(f"  No predictions at {pred_path}; skip")
                continue
            by_id = load_predictions_by_instance_id(pred_path)
            predictions, n_miss = predictions_in_record_order(records, by_id, model_name)
            if n_miss:
                print(
                    f"  Note: {len(by_id)}/{len(records)} instances in file; "
                    "metrics use empty answers for gaps"
                )

        rec_list = [r.model_dump() if hasattr(r, "model_dump") else r for r in records]
        metrics = compute_all_metrics(rec_list, predictions, model_name=model_name)
        all_metrics[model_name] = metrics
        mfr = metrics.get("modality_following_rate", 0.0)
        hr = metrics.get("hallucination_rate", 0.0)
        delta = metrics.get("accuracy_drop", 0.0)
        print(f"  {model_name}: MFR={mfr:.3f}, HR={hr:.3f}, DeltaAcc={delta:.3f}")

    out_path = pred_dir.parent / "metrics_summary.json"
    merged = {}
    if out_path.exists():
        try:
            with open(out_path) as f:
                merged = json.load(f)
        except (json.JSONDecodeError, OSError):
            merged = {}
    merged.update(all_metrics)
    with open(out_path, "w") as f:
        json.dump(merged, f, indent=2)
    print(f"\nMetrics summary -> {out_path} ({len(merged)} model(s))")


if __name__ == "__main__":
    main()
