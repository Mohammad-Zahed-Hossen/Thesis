#!/usr/bin/env python3
"""
Build CMC-Bench instances from ChartQA and MMMU.
Config-driven: 250 examples per conflict type → 1,000 examples, 4,000 instances.
"""
import argparse
import ast
import os
import random
import sys
from collections import defaultdict
from pathlib import Path

_ROOT = Path(__file__).resolve().parents[1]
if str(_ROOT) not in sys.path:
    sys.path.insert(0, str(_ROOT))
_REPO = _ROOT.parent
if str(_REPO) not in sys.path:
    sys.path.insert(0, str(_REPO))

import yaml
from tqdm import tqdm

from data.download import DEFAULT_MMMU_CONFIGS, get_chartqa_splits, get_one_mmmu_config
from data.example_generation import build_instance_records
from data.io import save_instances_jsonl
from data.schema import ConflictType, InstanceRecord


def _norm(a) -> str:
    raw = a if not isinstance(a, list) else (a[0] if a else "")
    return str(raw).strip() if raw else ""


def _answer_type(s: str) -> str:
    s = str(s).strip()
    if not s:
        return "text"
    if len(s) == 4 and s.isdigit() and 1900 <= int(s) <= 2100:
        return "year"
    if s.replace(".", "").replace("-", "").isdigit():
        return "number"
    if s.lower() in ("yes", "no"):
        return "yesno"
    return "text"


def _classify_conflict_type(gold: str, source: str) -> ConflictType | None:
    t = _answer_type(gold)
    if source == "chartqa":
        return ConflictType.TEMPORAL if t == "year" else ConflictType.FACTUAL
    if source == "mmmu":
        if t == "number":
            return ConflictType.GRANULARITY
        if t == "text" and len(gold) < 80:
            return ConflictType.ENTITY
        return ConflictType.GRANULARITY
    return None


def _wrong_pool(entries: list, gold: str) -> list[str]:
    """Other answers from entries, same answer type preferred."""
    pool = [g for (_, _, g) in entries if g != gold]
    if not pool:
        return []
    same = [a for a in pool if _answer_type(a) == _answer_type(gold)]
    return same if same else pool


def _mmmu_resolve_options(row: dict) -> tuple[str, list[str] | None]:
    """Resolve MMMU multiple-choice: answer column is A/B/C/D; option text from options column.
    Returns (gold_text, other_option_texts or None). If not multiple-choice or no options, other_option_texts is None.
    """
    answer = _norm(row.get("answer") or row.get("answers"))
    options = row.get("options")
    if not options or not answer:
        return (answer, None)
    # Parse options to list (may be list or string like "['$63,020', '$58,410']")
    if isinstance(options, list):
        opt_list = [str(o).strip() for o in options if o is not None]
    elif isinstance(options, str):
        s = options.strip()
        try:
            parsed = ast.literal_eval(s)
            opt_list = [str(o).strip() for o in parsed] if isinstance(parsed, list) else []
        except (ValueError, SyntaxError):
            opt_list = []
    else:
        opt_list = []
    if not opt_list:
        return (answer, None)
    letter = answer.strip().upper()
    if len(letter) != 1 or letter not in "ABCDEFGH":
        return (answer, None)
    idx = ord(letter) - ord("A")
    if idx < 0 or idx >= len(opt_list):
        return (answer, None)
    gold_text = opt_list[idx]
    other = [o for i, o in enumerate(opt_list) if i != idx]
    return (gold_text, other if other else None)


def _wrong_pool_plausible(entries: list, gold: str, year_window: int = 10) -> list[str]:
    """Plausible wrong answers: same type; for years, prefer nearby years (±year_window)."""
    pool = [g for (_, _, g) in entries if g != gold]
    if not pool:
        return []
    at = _answer_type(gold)
    same_type = [a for a in pool if _answer_type(a) == at]
    if at == "year" and same_type:
        try:
            g_year = int(gold)
            nearby = [a for a in same_type if a.isdigit() and abs(int(a) - g_year) <= year_window]
            return nearby if nearby else same_type
        except ValueError:
            pass
    return same_type if same_type else pool


def _save_image(row: dict, key: str, out_path: Path) -> bool:
    """Save image from dataset row to disk. Returns True if saved. Handles PIL, bytes, path, or HF Image dict."""
    img = row.get(key)
    if img is None:
        return False
    out_path.parent.mkdir(parents=True, exist_ok=True)
    try:
        import io as _io
        from PIL import Image as PILImage
        if hasattr(img, "save"):
            img.save(str(out_path))
            return True
        if isinstance(img, dict):
            if img.get("bytes") is not None:
                PILImage.open(_io.BytesIO(img["bytes"])).save(str(out_path))
                return True
            if img.get("path") is not None:
                PILImage.open(img["path"]).save(str(out_path))
                return True
        if isinstance(img, (str, Path)):
            PILImage.open(img).save(str(out_path))
            return True
        PILImage.open(_io.BytesIO(img)).save(str(out_path))
        return True
    except Exception:
        return False


def main():
    parser = argparse.ArgumentParser(description="CMC-Bench example generation")
    parser.add_argument("--config", default=str(_ROOT / "configs" / "default.yaml"))
    parser.add_argument("--data-dir", default=None)
    parser.add_argument("--output", default=None)
    parser.add_argument("--qc-sample-pct", type=float, default=20.0)
    parser.add_argument("--qc-out", default=None)
    args = parser.parse_args()

    with open(args.config) as f:
        cfg = yaml.safe_load(f)
    paths = cfg.get("paths", {})
    data_dir = Path(args.data_dir or paths.get("data_dir", "./data_cache")).resolve()
    data_dir.mkdir(parents=True, exist_ok=True)
    os.environ.setdefault("HF_HOME", str(data_dir / "hf_cache"))
    os.environ.setdefault("HF_DATASETS_CACHE", str(data_dir / "hf_cache" / "datasets"))

    output_path = args.output or paths.get("instances_jsonl", "./outputs/cmc_bench_instances.jsonl")
    out_path = Path(output_path)
    out_path.parent.mkdir(parents=True, exist_ok=True)
    image_dir = out_path.parent / "images"
    image_dir.mkdir(parents=True, exist_ok=True)

    scale = cfg.get("scale", {})
    n_factual = scale.get("factual_chartqa", 250)
    n_temporal = scale.get("temporal_chartqa", 250)
    n_entity = scale.get("entity_mmmu", 250)
    n_granularity = scale.get("granularity_mmmu", 250)

    print(f"[CMC-Bench] Config: {args.config} | scale: factual={n_factual}, temporal={n_temporal}, entity={n_entity}, granularity={n_granularity}", flush=True)
    print(f"[CMC-Bench] Data dir: {data_dir} | output: {out_path}", flush=True)

    all_records: list[InstanceRecord] = []
    example_id_counter = [0]

    def next_example_id(prefix: str) -> str:
        example_id_counter[0] += 1
        return f"{prefix}_{example_id_counter[0]}"

    # ChartQA: factual + temporal
    try:
        chartqa = get_chartqa_splits(data_dir)
        split = chartqa.get("eval") or chartqa.get("val") or chartqa.get("validation")
        if split is not None:
            entries_factual: list[tuple[int, str, str]] = []
            entries_temporal: list[tuple[int, str, str]] = []
            for idx in tqdm(range(len(split)), desc="ChartQA eval pool", unit="row"):
                row = split[idx]
                q = row.get("query") or row.get("question", "")
                gold = _norm(row.get("label") or row.get("answer"))
                if not q or not gold:
                    continue
                ct = _classify_conflict_type(gold, "chartqa")
                if ct == ConflictType.TEMPORAL:
                    entries_temporal.append((idx, q, gold))
                else:
                    entries_factual.append((idx, q, gold))

            print(f"[ChartQA] Pools: {len(entries_factual)} factual, {len(entries_temporal)} temporal.", flush=True)

            def add_chartqa(entries: list, conflict_type: ConflictType, n: int) -> int:
                pool = list({g for (_, _, g) in entries})
                shuffled = list(entries)
                random.shuffle(shuffled)
                added = 0
                for idx, q, gold in tqdm(shuffled, desc=f"ChartQA {conflict_type.value}", unit="ex", leave=False):
                    if added >= n:
                        break
                    wrong_pool = _wrong_pool_plausible(entries, gold)
                    wrong_ans = random.choice(wrong_pool) if wrong_pool else "a different value"
                    aligned_pass = f"According to the chart, the answer is {gold}."
                    contradict_pass = f"According to the source, the value is {wrong_ans}."
                    # Wrong image: same pool (same conflict type) so it's a similar chart
                    other_indices = [i for (i, _, _) in entries if i != idx]
                    wrong_idx = random.choice(other_indices) if other_indices else idx
                    img_path = image_dir / f"chartqa_{idx}.png"
                    wrong_img_path = image_dir / f"chartqa_{wrong_idx}.png"
                    if not img_path.exists() and "image" in split[idx]:
                        _save_image(split[idx], "image", img_path)
                    if not wrong_img_path.exists() and "image" in split[wrong_idx]:
                        _save_image(split[wrong_idx], "image", wrong_img_path)
                    eid = next_example_id(conflict_type.value)
                    recs = build_instance_records(
                        example_id=eid,
                        query=q,
                        image_path=str(img_path),
                        image_id=str(idx),
                        gold_answer=gold,
                        aligned_passage=aligned_pass,
                        contradicting_passage=contradict_pass,
                        text_answer_contradicting=wrong_ans,
                        wrong_image_path=str(wrong_img_path),
                        wrong_image_id=str(wrong_idx),
                        conflict_type=conflict_type,
                        source_dataset="chartqa",
                    )
                    all_records.extend(recs)
                    added += 1
                return added

            if n_temporal and entries_temporal:
                a = add_chartqa(entries_temporal, ConflictType.TEMPORAL, n_temporal)
                print(f"ChartQA temporal: {a} examples ({a * 4} instances)")
            if n_factual and entries_factual:
                a = add_chartqa(entries_factual, ConflictType.FACTUAL, n_factual)
                print(f"ChartQA factual: {a} examples ({a * 4} instances)")
    except Exception as e:
        print(f"ChartQA: {e}")

    # MMMU: entity + granularity — one config at a time to avoid freeze (validation+test per domain)
    mmmu_configs = (cfg.get("datasets") or {}).get("mmmu_configs") or DEFAULT_MMMU_CONFIGS
    n_configs = len(mmmu_configs)
    base_entity = n_entity // n_configs if n_configs else 0
    rem_entity = n_entity % n_configs if n_configs else 0
    base_granularity = n_granularity // n_configs if n_configs else 0
    rem_granularity = n_granularity % n_configs if n_configs else 0
    img_key = "image_1"  # MMMU schema: image_1..image_7, question, answer

    try:
        for cidx, config_name in tqdm(enumerate(mmmu_configs), total=n_configs, desc="MMMU configs", unit="config"):
            print(f"[MMMU] Config {cidx + 1}/{n_configs}: {config_name}...", flush=True)
            split = get_one_mmmu_config(data_dir, config_name)
            if split is None:
                continue
            print(f"[MMMU]   Loaded {len(split)} examples (val+test).", flush=True)
            entries_entity = []
            entries_granularity = []
            for idx in tqdm(range(len(split)), desc=f"MMMU {config_name} pool", unit="row", leave=False):
                row = split[idx]
                q = row.get("question", "")
                gold_text, _ = _mmmu_resolve_options(row)  # resolve A/B/C/D to option text when present
                if not q or not gold_text:
                    continue
                ct = _classify_conflict_type(gold_text, "mmmu")
                if ct == ConflictType.ENTITY:
                    entries_entity.append((idx, q, gold_text))
                else:
                    entries_granularity.append((idx, q, gold_text))
            n_entity_this = base_entity + (1 if cidx < rem_entity else 0)
            n_granularity_this = base_granularity + (1 if cidx < rem_granularity else 0)
            print(f"[MMMU]   Pools: {len(entries_entity)} entity, {len(entries_granularity)} granularity → taking {n_entity_this} entity, {n_granularity_this} granularity.", flush=True)

            def add_mmmu_one(split, entries: list, conflict_type: ConflictType, n: int) -> tuple[int, int]:
                """Returns (added_count, missing_image_count)."""
                if not n or not entries:
                    return (0, 0)
                shuffled = list(entries)
                random.shuffle(shuffled)
                added = 0
                missing = 0
                dom = config_name
                has_subfield = "subfield" in split.column_names
                for idx, q, gold in tqdm(shuffled, desc=f"{config_name} {conflict_type.value}", unit="ex", leave=False):
                    if added >= n:
                        break
                    # Wrong image: same subfield when possible (always define pool_entries)
                    sub = (split[idx].get("subfield") or "").strip() if has_subfield else ""
                    if sub:
                        same_sub_entries = [(i, qq, gg) for (i, qq, gg) in entries if (split[i].get("subfield") or "").strip() == sub]
                    else:
                        same_sub_entries = []
                    pool_entries = same_sub_entries if same_sub_entries else entries
                    # Wrong text: from same-row options (MC) or plausible pool
                    _, other_options = _mmmu_resolve_options(split[idx])
                    if other_options:
                        wrong_ans = random.choice(other_options)
                    else:
                        wrong_pool = _wrong_pool_plausible(pool_entries, gold)
                        wrong_ans = random.choice(wrong_pool) if wrong_pool else "a different value"
                    aligned_pass = f"According to the figure, the answer is {gold}."
                    contradict_pass = f"According to the source, the value is {wrong_ans}."
                    other_indices = [i for (i, _, _) in pool_entries if i != idx] if pool_entries else [i for (i, _, _) in entries if i != idx]
                    wrong_idx = random.choice(other_indices) if other_indices else idx
                    img_path = image_dir / f"mmmu_{dom}_{idx}.png"
                    wrong_img_path = image_dir / f"mmmu_{dom}_{wrong_idx}.png"
                    if not img_path.exists():
                        if img_key in split[idx]:
                            if not _save_image(split[idx], img_key, img_path):
                                missing += 1
                        else:
                            missing += 1
                    if not wrong_img_path.exists():
                        if img_key in split[wrong_idx]:
                            if not _save_image(split[wrong_idx], img_key, wrong_img_path):
                                missing += 1
                        else:
                            missing += 1
                    eid = next_example_id(conflict_type.value)
                    recs = build_instance_records(
                        example_id=eid,
                        query=q,
                        image_path=str(img_path),
                        image_id=str(idx),
                        gold_answer=gold,
                        aligned_passage=aligned_pass,
                        contradicting_passage=contradict_pass,
                        text_answer_contradicting=wrong_ans,
                        wrong_image_path=str(wrong_img_path),
                        wrong_image_id=str(wrong_idx),
                        conflict_type=conflict_type,
                        source_dataset="mmmu",
                    )
                    all_records.extend(recs)
                    added += 1
                return (added, missing)

            a_e, miss_e = add_mmmu_one(split, entries_entity, ConflictType.ENTITY, n_entity_this)
            a_g, miss_g = add_mmmu_one(split, entries_granularity, ConflictType.GRANULARITY, n_granularity_this)
            mmmu_so_far = len([r for r in all_records if r.source_dataset == "mmmu"])
            msg = f"[MMMU]   {config_name}: entity {a_e}, granularity {a_g} → MMMU total so far: {mmmu_so_far} instances."
            if miss_e or miss_g:
                msg += f" (Warning: {miss_e + miss_g} images could not be saved)"
            print(msg, flush=True)
            del split, entries_entity, entries_granularity  # free memory before next config
    except Exception as e:
        print(f"MMMU: {e}")

    print(f"[CMC-Bench] Writing {len(all_records)} instances to {out_path}...", flush=True)
    save_instances_jsonl(all_records, out_path)
    print(f"Wrote {len(all_records)} instances to {out_path}", flush=True)

    if args.qc_sample_pct > 0 and all_records:
        sample_size = max(1, int(len(all_records) * args.qc_sample_pct / 100))
        qc = random.sample(all_records, min(sample_size, len(all_records)))
        qc_path = Path(args.qc_out or str(out_path.parent / "qc_sample_instance_ids.csv"))
        qc_path.parent.mkdir(parents=True, exist_ok=True)
        with open(qc_path, "w") as f:
            f.write("instance_id,example_id,condition,conflict_type\n")
            for r in qc:
                f.write(f"{r.instance_id},{r.example_id},{r.condition.value},{r.conflict_type.value}\n")
        print(f"QC sample ({len(qc)} instances) -> {qc_path}")


if __name__ == "__main__":
    main()
