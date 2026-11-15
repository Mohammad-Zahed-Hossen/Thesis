"""Aggregate LLM-judge behavioral JSONL into summary metrics (no API calls)."""
from __future__ import annotations

import json
from collections import Counter, defaultdict
from pathlib import Path
from typing import Any

from data.schema import InstanceRecord
from evaluation.judge_constants import JUDGE_PROMPT_VERSION
from evaluation.metrics import compute_all_metrics_from_judge

_CONDITION_ORDER = ("aligned", "image_correct", "text_correct", "both_wrong")


def _condition_sort_key(c: str) -> tuple[int, str]:
    try:
        return (_CONDITION_ORDER.index(c), c)
    except ValueError:
        return (len(_CONDITION_ORDER), c)


def _norm_model_key(name: str) -> str:
    return name.strip().lower().replace(".", "_")


def judge_label_breakdown(
    behavioral: list[dict],
) -> tuple[dict[str, int], dict[str, dict[str, int]]]:
    """Marginal judge_label counts and counts stratified by benchmark condition."""
    marginal: Counter = Counter()
    by_cond: dict[str, Counter] = defaultdict(Counter)
    for b in behavioral:
        lab = str(b.get("judge_label", "")).strip().upper()
        if not lab:
            continue
        marginal[lab] += 1
        cond = str(b.get("condition", "unknown"))
        by_cond[cond][lab] += 1
    marginal_out = dict(sorted(marginal.items()))
    stratified = {
        c: dict(sorted(by_cond[c].items()))
        for c in sorted(by_cond.keys(), key=_condition_sort_key)
    }
    return marginal_out, stratified


def behavioral_jsonl_stem(path: Path) -> str:
    """``behavioral_<stem>.jsonl`` → ``stem``."""
    name = path.name
    prefix, suffix = "behavioral_", ".jsonl"
    if not name.startswith(prefix) or not name.endswith(suffix):
        raise ValueError(f"expected behavioral_*.jsonl, got {path.name}")
    return name[len(prefix) : -len(suffix)]


def load_behavioral_jsonl(path: Path) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    with path.open(encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            rows.append(json.loads(line))
    return rows


def load_instances_jsonl(path: Path) -> list[dict]:
    records: list[dict] = []
    with path.open(encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            d = json.loads(line)
            records.append(InstanceRecord.model_validate(d).model_dump())
    return records


def discover_behavioral_jsonl(
    judge_dir: Path,
    models: list[str] | None = None,
) -> list[Path]:
    paths = sorted(judge_dir.glob("behavioral_*.jsonl"))
    if not models:
        return paths
    allow = {_norm_model_key(m) for m in models}
    out: list[Path] = []
    for p in paths:
        stem = behavioral_jsonl_stem(p)
        if _norm_model_key(stem) in allow:
            out.append(p)
    return out


def summary_entry_for_behavioral(
    records: list[dict],
    behavioral: list[dict],
    model_stem: str,
) -> dict[str, Any]:
    """One model block for ``metrics_judge_summary.json``."""
    metrics = compute_all_metrics_from_judge(records, behavioral, model_name=model_stem)
    marginal, stratified = judge_label_breakdown(behavioral)
    return {
        **metrics,
        "judge_prompt_version": JUDGE_PROMPT_VERSION,
        "judge_label_counts": marginal,
        "judge_label_counts_by_condition": stratified,
        "n_behavioral_rows": len(behavioral),
    }


def aggregate_summary_from_judge_dir(
    *,
    instances_path: Path,
    judge_dir: Path,
    models: list[str] | None = None,
    merge_existing: bool = True,
) -> dict[str, Any]:
    """
    Build full summary dict from ``behavioral_*.jsonl`` under ``judge_dir``.
    If ``merge_existing`` and ``judge_dir / metrics_judge_summary.json`` exists, merge keys.
    """
    records = load_instances_jsonl(instances_path)
    paths = discover_behavioral_jsonl(judge_dir, models)
    if not paths:
        raise FileNotFoundError(
            f"No behavioral_*.jsonl under {judge_dir}"
            + (f" after --models filter" if models else "")
        )
    merged: dict[str, Any] = {}
    out_path = judge_dir / "metrics_judge_summary.json"
    if merge_existing and out_path.is_file():
        try:
            raw = json.loads(out_path.read_text(encoding="utf-8"))
            if isinstance(raw, dict):
                merged = raw
        except (json.JSONDecodeError, OSError):
            merged = {}
    for p in paths:
        stem = behavioral_jsonl_stem(p)
        behavioral = load_behavioral_jsonl(p)
        merged[stem] = summary_entry_for_behavioral(records, behavioral, stem)
    return merged
