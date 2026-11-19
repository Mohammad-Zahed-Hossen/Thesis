"""Stratified human-coding sampler and evaluator for v5 donor verbalizations and minimal-edit flips.

Subcommands:
    sample    Sample 200 donor verbalizations (stratified across model × regime × order × family)
              plus 50 passing flipped clauses per model, and write blinded coder A/B CSVs, a
              held-out key CSV, and CODEBOOK_v5.md. Refuses to overwrite coder sheets that already
              hold labels unless --force is given. --keys_only rewrites only the KEY_*.csv files,
              after checking that the regenerated samples are the ones already coded.
    evaluate  Compute inter-coder agreement (Cohen's kappa, Gwet's AC1, PABAK, kappa_max) and
              parser accuracy / flip quality per coder, on consensus rows, and against an optional
              adjudication CSV (prereg §8).

The flip sample depends on the parser: build_flip_samples keeps only donors whose variants pass
transplant_v5's gates, which call score_v5.stated_reliable_source. After any parser change, never
re-run `sample` to refresh keys; use --keys_only, which aborts if the coded samples would change.
"""

from __future__ import annotations

import argparse
import csv
import glob
import json
import math
import os
import random
import re
import sys
from collections import Counter, defaultdict
from typing import Any, Dict, List, Optional, Sequence, Tuple

HERE = os.path.dirname(os.path.abspath(__file__))
if HERE not in sys.path:
    sys.path.insert(0, HERE)

import score_v5 as sc  # noqa: E402
import transplant_v5 as tp  # noqa: E402

VALID_VERDICT_LABELS = {"image", "text", "chart", "report", "neither", "both", "unclear"}
NO_VERDICT_LABELS = {"undetermined", "absent", "neither", "both", "unclear"}
CONFIRMATORY_MODELS = ("Qwen/Qwen2.5-VL-3B-Instruct", "Qwen/Qwen2.5-VL-7B-Instruct")
DIAGNOSTIC_MODEL = "Qwen/Qwen2-VL-2B-Instruct"
TRUTHY = {"1", "y", "yes", "true", "pass", "ok"}
FALSY = {"0", "n", "no", "false", "fail", "bad"}
# Donor files from resolution-comparison runs (R8.4, e.g. v5dev_chartqa_px501k_donor_*) repeat the
# same items at another max_pixels. The default glob skips them; pass --donor_files to use them.
_RESOLUTION_RUN = re.compile(r"_px\d+k_", re.I)
DEFAULT_ADJUDICATION = "adjudication_v5.csv"
CANON_SIDE = {"image": "source_1", "chart": "source_1", "text": "source_2", "report": "source_2"}


def canonical_verdict_label(lbl: str, regime: Optional[str] = None) -> str:
    """Map parser and human labels onto {source_1, source_2, 'no_verdict'}."""
    s = (lbl or "").strip().lower()
    if not s or s in NO_VERDICT_LABELS:
        return "no_verdict"
    if regime in sc.SOURCES and s not in sc.SOURCES[regime]:
        return "no_verdict"
    return s


def strict_three_way(lbl: str, regime: Optional[str] = None) -> str:
    """canonical_verdict_label folded to {source_1 (image/chart), source_2 (text/report), no_verdict}."""
    return CANON_SIDE.get(canonical_verdict_label(lbl, regime), "no_verdict")

CODEBOOK_MD = """# v5 Human Coding Codebook

## Part 1 — Donor Verbalization Coding (`coder_*_verdicts.csv`)
Fill `coder_stated_source` (and optional `coder_notes`) using ONLY the text shown:

- For **Math** (`regime == math`):
  - `image`: clearly states the image / photo / problem in the image is more reliable / trustworthy / accurate.
  - `text`: clearly states the text / written text / problem in the text is more reliable / trustworthy / accurate.
- For **ChartQA** (`regime == chartqa`):
  - `chart`: clearly states the chart / graph / plot / figure / image is more reliable.
  - `report`: clearly states the report / text / summary / written text is more reliable.
- For **either regime**:
  - `neither`: refuses to choose, says both are equally reliable, or discusses something else without picking one source.
  - `both`: explicitly claims both sources are reliable without preferring one, OR states contradictory reliability preferences.
  - `unclear`: truncated, garbled, or too ambiguous to assign one clear preference.

Do NOT look at the final math/chart answer when judging `coder_stated_source`; judge only the reliability verbalization.

## Part 2 — Flipped Clause Coding (`coder_*_flips.csv`)
Fill both binary columns with `1` (yes) or `0` (no):

1. `coder_grammatical_coherent`: Is `flipped_verbalization` grammatical and internally coherent (no half-swapped contradictory phrases like "the text is more reliable than the text")?
2. `coder_names_intended_source`: Does `flipped_verbalization` unambiguously state that `intended_flip_source` is the more reliable source?
"""


def load_donor_rows(paths: Sequence[str]) -> List[Dict[str, Any]]:
    rows: List[Dict[str, Any]] = []
    for p in paths:
        with open(p, encoding="utf-8") as f:
            for line in f:
                line = line.strip()
                if not line:
                    continue
                try:
                    r = json.loads(line)
                except json.JSONDecodeError:
                    continue
                if "full_text" in r and r.get("family") in ("donor", "free_binding"):
                    rows.append(r)
    return rows


def stratified_pick(
    records: Sequence[Dict[str, Any]],
    key_fn,
    total_n: int,
    rng: random.Random,
) -> List[Dict[str, Any]]:
    buckets: Dict[Tuple, List[Dict[str, Any]]] = defaultdict(list)
    for rec in records:
        buckets[key_fn(rec)].append(rec)
    keys = sorted(buckets)
    for k in keys:
        rng.shuffle(buckets[k])
    chosen: List[Dict[str, Any]] = []
    cursor = {k: 0 for k in keys}
    while len(chosen) < total_n:
        progressed = False
        for k in keys:
            if len(chosen) >= total_n:
                break
            idx = cursor[k]
            if idx < len(buckets[k]):
                chosen.append(buckets[k][idx])
                cursor[k] = idx + 1
                progressed = True
        if not progressed:
            break
    rng.shuffle(chosen)
    return chosen


def _take_by_family(
    pool: Sequence[Dict[str, Any]],
    total_n: int,
    rng: random.Random,
    donor_frac: float = 2.0 / 3.0,
) -> List[Dict[str, Any]]:
    donors = [r for r in pool if r.get("family") == "donor"]
    free = [r for r in pool if r.get("family") != "donor"]
    key_fn = lambda r: (r["model_id"], r["regime"], r.get("order", ""), r["family"])
    if donors and free:
        n_d = min(len(donors), int(round(total_n * donor_frac)))
        n_f = min(len(free), total_n - n_d)
        picked = stratified_pick(donors, key_fn=key_fn, total_n=n_d, rng=rng)
        picked += stratified_pick(free, key_fn=key_fn, total_n=n_f, rng=rng)
        if len(picked) < min(total_n, len(pool)):
            seen = {(r["model_id"], r["regime"], r.get("order", ""), r["family"], r["id"]) for r in picked}
            rem = [r for r in pool if (r["model_id"], r["regime"], r.get("order", ""), r["family"], r["id"]) not in seen]
            picked += stratified_pick(rem, key_fn=key_fn, total_n=total_n - len(picked), rng=rng)
        return picked
    return stratified_pick(pool, key_fn=key_fn, total_n=total_n, rng=rng)


def build_verdict_samples(rows: Sequence[Dict[str, Any]], n_donors: int, seed: int) -> Tuple[List[Dict[str, Any]], List[Dict[str, Any]]]:
    rng = random.Random(seed)
    models = {r["model_id"] for r in rows}
    regimes = {r["regime"] for r in rows}
    if any(m in models for m in CONFIRMATORY_MODELS) and DIAGNOSTIC_MODEL in models and len(regimes) >= 2:
        conf_math = [r for r in rows if r["model_id"] in CONFIRMATORY_MODELS and r["regime"] == "math"]
        conf_chart = [r for r in rows if r["model_id"] in CONFIRMATORY_MODELS and r["regime"] == "chartqa"]
        diag = [r for r in rows if r["model_id"] == DIAGNOSTIC_MODEL]
        n_cm = int(round(0.60 * n_donors))
        n_cc = int(round(0.24 * n_donors))
        n_dg = max(0, n_donors - n_cm - n_cc)
        picked = _take_by_family(conf_math, n_cm, rng) + _take_by_family(conf_chart, n_cc, rng) + stratified_pick(
            diag, key_fn=lambda r: (r["model_id"], r["regime"], r.get("order", ""), r["family"]), total_n=n_dg, rng=rng
        )
        if len(picked) < min(n_donors, len(rows)):
            seen = {(r["model_id"], r["regime"], r.get("order", ""), r["family"], r["id"]) for r in picked}
            rem = [r for r in rows if (r["model_id"], r["regime"], r.get("order", ""), r["family"], r["id"]) not in seen]
            picked += stratified_pick(
                rem,
                key_fn=lambda r: (r["model_id"], r["regime"], r.get("order", ""), r["family"]),
                total_n=n_donors - len(picked),
                rng=rng,
            )
        rng.shuffle(picked)
    else:
        picked = stratified_pick(
            rows,
            key_fn=lambda r: (r["model_id"], r["regime"], r.get("order", ""), r["family"]),
            total_n=n_donors,
            rng=rng,
        )
    blinded: List[Dict[str, Any]] = []
    key: List[Dict[str, Any]] = []
    for idx, r in enumerate(picked, 1):
        sid = f"V{idx:04d}"
        verb, _ = sc.split_verbalization(r["full_text"])
        pred = sc.stated_reliable_source(verb, regime=r["regime"])
        beh_src, _, _ = sc.behavioural_source(r["full_text"], r["regime"], r["y_image"], r["y_text"], parser="structured")
        blinded.append(
            {
                "sample_id": sid,
                "item_id": r["id"],
                "model_id": r["model_id"],
                "regime": r["regime"],
                "family": r["family"],
                "order": r.get("order", ""),
                "verbalization_text": verb,
                "full_text": r["full_text"],
                "coder_stated_source": "",
                "coder_notes": "",
            }
        )
        key.append(
            {
                "sample_id": sid,
                "item_id": r["id"],
                "model_id": r["model_id"],
                "regime": r["regime"],
                "family": r["family"],
                "order": r.get("order", ""),
                "predicted_stated_source": pred,
                "beh_source": beh_src,
                "verbalization_text": verb,
                "full_text": r["full_text"],
            }
        )
    return blinded, key


def build_flip_samples(rows: Sequence[Dict[str, Any]], n_per_model: int, seed: int) -> Tuple[List[Dict[str, Any]], List[Dict[str, Any]]]:
    rng = random.Random(seed + 101)
    by_model: Dict[str, List[Dict[str, Any]]] = defaultdict(list)
    seen = set()
    for r in rows:
        if r.get("family") != "donor":
            continue
        k = (r["model_id"], r["regime"], r["id"], r.get("order", ""))
        if k in seen:
            continue
        seen.add(k)
        verb, _ = sc.split_verbalization(r["full_text"])
        var = tp.make_variants(verb, r["regime"], y_image=r.get("y_image"), y_text=r.get("y_text"))
        if not var.ok:
            continue
        by_model[r["model_id"]].append(
            {
                "item_id": r["id"],
                "model_id": r["model_id"],
                "regime": r["regime"],
                "order": r.get("order", ""),
                "own_source": var.own_source,
                "flip_source": var.flip_source,
                "original_verbalization": var.texts["own"],
                "flipped_verbalization": var.texts["flip"],
                "jaccard_multiset_flip": var.jaccard_multiset_flip,
                "n_swaps": var.n_swaps,
            }
        )

    all_picked: List[Dict[str, Any]] = []
    if all(m in by_model for m in (*CONFIRMATORY_MODELS, DIAGNOSTIC_MODEL)):
        total_target = n_per_model * len(by_model)
        conf_each = int(round(0.40 * total_target))
        diag_n = max(0, total_target - conf_each * len(CONFIRMATORY_MODELS))
        quotas = {m: conf_each for m in CONFIRMATORY_MODELS}
        quotas[DIAGNOSTIC_MODEL] = diag_n
    else:
        quotas = {mid: n_per_model for mid in by_model}
    for mid in sorted(by_model):
        all_picked.extend(
            stratified_pick(
                by_model[mid],
                key_fn=lambda rec: (rec["regime"], rec["order"]),
                total_n=quotas.get(mid, n_per_model),
                rng=rng,
            )
        )
    rng.shuffle(all_picked)
    blinded: List[Dict[str, Any]] = []
    key: List[Dict[str, Any]] = []
    for idx, rec in enumerate(all_picked, 1):
        sid = f"F{idx:04d}"
        blinded.append(
            {
                "sample_id": sid,
                "item_id": rec["item_id"],
                "model_id": rec["model_id"],
                "regime": rec["regime"],
                "order": rec["order"],
                "own_source": rec["own_source"],
                "intended_flip_source": rec["flip_source"],
                "original_verbalization": rec["original_verbalization"],
                "flipped_verbalization": rec["flipped_verbalization"],
                "coder_grammatical_coherent": "",
                "coder_names_intended_source": "",
                "coder_notes": "",
            }
        )
        key.append({"sample_id": sid, **rec})
    return blinded, key


def write_csv(path: str, rows: Sequence[Dict[str, Any]], fieldnames: Sequence[str]) -> None:
    with open(path, "w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=fieldnames)
        w.writeheader()
        for r in rows:
            w.writerow({k: r.get(k, "") for k in fieldnames})


def read_csv_map(path: str) -> Dict[str, Dict[str, str]]:
    with open(path, newline="", encoding="utf-8-sig") as f:
        return {r["sample_id"]: r for r in csv.DictReader(f)}


def cohens_kappa(xs: Sequence[str], ys: Sequence[str]) -> Optional[float]:
    n = len(xs)
    if n == 0:
        return None
    agree = sum(a == b for a, b in zip(xs, ys)) / n
    ca, cb = Counter(xs), Counter(ys)
    pe = sum((ca[k] / n) * (cb[k] / n) for k in set(ca) | set(cb))
    return (agree - pe) / (1 - pe) if pe < 1.0 - 1e-12 else None


# Cohen's kappa is 0 whenever one rater is constant (p_e then equals p_o), and None only when both
# are constant on the same class. With near-ceiling base rates (flip ratings) it says little, so
# agreement is also reported as Gwet's AC1, PABAK and kappa_max (the largest kappa the two raters'
# marginals allow). `categories` is the label space; it defaults to the labels observed.


def kappa_max(xs: Sequence[str], ys: Sequence[str]) -> Optional[float]:
    n = len(xs)
    if n == 0:
        return None
    ca, cb = Counter(xs), Counter(ys)
    cats = set(ca) | set(cb)
    pe = sum((ca[k] / n) * (cb[k] / n) for k in cats)
    po_max = sum(min(ca[k], cb[k]) for k in cats) / n
    return (po_max - pe) / (1 - pe) if pe < 1.0 - 1e-12 else None


def gwet_ac1(xs: Sequence[str], ys: Sequence[str], categories: Optional[Sequence[str]] = None) -> Optional[float]:
    n = len(xs)
    cats = sorted(set(categories) if categories else set(xs) | set(ys))
    if n == 0 or len(cats) < 2:
        return None
    po = sum(a == b for a, b in zip(xs, ys)) / n
    ca, cb = Counter(xs), Counter(ys)
    pe = sum(((ca[k] + cb[k]) / (2 * n)) * (1 - (ca[k] + cb[k]) / (2 * n)) for k in cats) / (len(cats) - 1)
    return (po - pe) / (1 - pe)


def pabak(xs: Sequence[str], ys: Sequence[str], categories: Optional[Sequence[str]] = None) -> Optional[float]:
    n = len(xs)
    q = len(set(categories) if categories else set(xs) | set(ys))
    if n == 0 or q < 2:
        return None
    po = sum(a == b for a, b in zip(xs, ys)) / n
    return (q * po - 1) / (q - 1)


def wilson_ci(k: int, n: int, z: float = 1.959963984540054) -> Optional[Tuple[float, float]]:
    if n == 0:
        return None
    p = k / n
    den = 1 + z * z / n
    centre = (p + z * z / (2 * n)) / den
    half = z * math.sqrt(p * (1 - p) / n + z * z / (4 * n * n)) / den
    return (max(0.0, centre - half), min(1.0, centre + half))


def agreement_block(xs: Sequence[str], ys: Sequence[str], categories: Optional[Sequence[str]] = None) -> Dict[str, Any]:
    n = len(xs)
    return {
        "n": n,
        "agreement": (sum(a == b for a, b in zip(xs, ys)) / n) if n else None,
        "cohens_kappa": cohens_kappa(xs, ys),
        "kappa_max": kappa_max(xs, ys),
        "gwet_ac1": gwet_ac1(xs, ys, categories),
        "pabak": pabak(xs, ys, categories),
        "table": {f"{a}|{b}": c for (a, b), c in sorted(Counter(zip(xs, ys)).items())},
    }


def _accuracy(matches: Sequence[bool]) -> Dict[str, Any]:
    n, k = len(matches), sum(bool(m) for m in matches)
    ci = wilson_ci(k, n)
    return {"n": n, "correct": k, "accuracy": (k / n) if n else None, "wilson95": list(ci) if ci else None}


def read_adjudication(path: Optional[str]) -> Dict[str, Dict[str, str]]:
    """sample_id -> row of the adjudication CSV, or {} when there is none."""
    if not path or not os.path.exists(path):
        return {}
    return read_csv_map(path)


def _norm_bool(val: Optional[str]) -> Optional[int]:
    if val is None:
        return None
    s = val.strip().lower()
    if s in TRUTHY:
        return 1
    if s in FALSY:
        return 0
    return None


SUBSETS = {
    "overall": lambda mid, reg: True,
    "confirmatory_math": lambda mid, reg: mid in CONFIRMATORY_MODELS and reg == "math",
    "confirmatory_all": lambda mid, reg: mid in CONFIRMATORY_MODELS,
    "diagnostic_2b": lambda mid, reg: mid == DIAGNOSTIC_MODEL,
    "chartqa": lambda mid, reg: reg == "chartqa",
}
RAW_VERDICT_LABELS = sorted(VALID_VERDICT_LABELS)
CANON_VERDICT_LABELS = ["chart", "image", "no_verdict", "report", "text"]
STRICT_VERDICT_LABELS = ["no_verdict", "source_1", "source_2"]


def evaluate_verdicts(
    coder_a: Dict[str, Dict[str, str]],
    coder_b: Optional[Dict[str, Dict[str, str]]],
    key: Dict[str, Dict[str, str]],
    adjudication: Optional[Dict[str, Dict[str, str]]] = None,
) -> Dict[str, Any]:
    """Inter-coder agreement and parser accuracy for the verdict sheets.

    Parser accuracy is given against Coder A, Coder B, consensus rows (the coders agree on the
    canonical label) and adjudicated labels. The headline (parser_accuracy_overall, the confusion
    matrix and the by-model table) uses the adjudicated labels when an adjudication is given, else
    consensus rows when both coders coded, else the one coder. It never depends on which coder's
    file is passed first.
    """
    adjudication = adjudication or {}
    rows = []
    for sid, krow in sorted(key.items()):
        regime = krow.get("regime")
        a_lbl = (coder_a.get(sid, {}).get("coder_stated_source") or "").strip().lower()
        b_lbl = (coder_b.get(sid, {}).get("coder_stated_source") or "").strip().lower() if coder_b else ""
        adj_lbl = (adjudication.get(sid, {}).get("adjudicated_stated_source") or "").strip().lower()
        if adj_lbl:
            adjudicated = adj_lbl
        elif a_lbl and (not coder_b or a_lbl == b_lbl):
            adjudicated = a_lbl
        elif b_lbl and not a_lbl:
            adjudicated = b_lbl
        else:
            adjudicated = ""
        rows.append(
            {
                "sid": sid, "model_id": krow.get("model_id"), "regime": regime, "a": a_lbl, "b": b_lbl,
                "adjudicated": adjudicated, "pred": (krow.get("predicted_stated_source") or "").strip().lower(),
            }
        )

    def canon(lbl, reg):
        return canonical_verdict_label(lbl, reg)

    def agreement(subset_rows):
        paired = [r for r in subset_rows if r["a"] and r["b"]]
        return {
            "raw": agreement_block([r["a"] for r in paired], [r["b"] for r in paired], RAW_VERDICT_LABELS),
            "canonical": agreement_block(
                [canon(r["a"], r["regime"]) for r in paired], [canon(r["b"], r["regime"]) for r in paired], CANON_VERDICT_LABELS
            ),
            "strict_three_way": agreement_block(
                [strict_three_way(r["a"], r["regime"]) for r in paired],
                [strict_three_way(r["b"], r["regime"]) for r in paired],
                STRICT_VERDICT_LABELS,
            ),
        }

    def truth(r, basis):
        if basis == "coder_a":
            return canon(r["a"], r["regime"]) if r["a"] else None
        if basis == "coder_b":
            return canon(r["b"], r["regime"]) if r["b"] else None
        if basis == "consensus":
            if not (r["a"] and r["b"]):
                return None
            ca, cb = canon(r["a"], r["regime"]), canon(r["b"], r["regime"])
            return ca if ca == cb else None
        return canon(r["adjudicated"], r["regime"]) if r["adjudicated"] else None

    bases = ["coder_a"] + (["coder_b", "consensus"] if coder_b else []) + (["adjudicated"] if adjudication else [])
    if adjudication:
        headline = "adjudicated"
    elif coder_b:
        headline = "consensus"
    else:
        headline = "coder_a"

    parser_accuracy: Dict[str, Dict[str, Any]] = {}
    for basis in bases:
        parser_accuracy[basis] = {}
        for name, fn in SUBSETS.items():
            matches = [
                canon(r["pred"], r["regime"]) == t
                for r in rows
                if fn(r["model_id"], r["regime"]) and (t := truth(r, basis)) is not None
            ]
            parser_accuracy[basis][name] = _accuracy(matches)

    confusion: Dict[str, Counter] = defaultdict(Counter)
    by_group: Dict[str, List[bool]] = defaultdict(list)
    raw_exact: List[bool] = []
    for r in rows:
        t = truth(r, headline)
        if t is None:
            continue
        c_pred = canon(r["pred"], r["regime"])
        confusion[t][c_pred] += 1
        by_group[f"{r['model_id']}|{r['regime']}"].append(c_pred == t)
        raw_truth = r["adjudicated"] if headline == "adjudicated" else (r["a"] if (headline == "coder_a" or r["a"] == r["b"]) else None)
        if raw_truth:
            raw_exact.append(r["pred"] == raw_truth)

    agree = {name: agreement([r for r in rows if fn(r["model_id"], r["regime"])]) for name, fn in SUBSETS.items()}
    overall = agree["overall"]
    head = parser_accuracy[headline]["overall"]
    unresolved = [r["sid"] for r in rows if r["a"] and r["b"] and r["a"] != r["b"] and not adjudication.get(r["sid"], {}).get("adjudicated_stated_source")]
    out: Dict[str, Any] = {
        "n_key": len(key),
        "n_coded": sum(1 for r in rows if r["a"] or r["b"]),
        "n_double_coded": overall["raw"]["n"],
        "inter_coder_agreement": overall["raw"]["agreement"],
        "cohens_kappa": overall["raw"]["cohens_kappa"],
        "inter_coder_agreement_canonical": overall["canonical"]["agreement"],
        "cohens_kappa_canonical": overall["canonical"]["cohens_kappa"],
        "cohens_kappa_strict_three_way": overall["strict_three_way"]["cohens_kappa"],
        "agreement_by_subset": agree,
        "headline_basis": headline,
        "parser_accuracy_overall": head["accuracy"],
        "parser_accuracy_overall_wilson95": head["wilson95"],
        "raw_exact_match_overall": (sum(raw_exact) / len(raw_exact)) if raw_exact else None,
        "parser_accuracy": parser_accuracy,
        "parser_accuracy_by_model_regime": {k: {"n": len(v), "accuracy": sum(v) / len(v)} for k, v in sorted(by_group.items())},
        "confusion_matrix": {ch: dict(sorted(preds.items())) for ch, preds in sorted(confusion.items())},
        "parser_errors": sorted(
            r["sid"] for r in rows if (t := truth(r, headline)) is not None and canon(r["pred"], r["regime"]) != t
        ),
        "unadjudicated_disagreements": unresolved if adjudication else [],
    }
    return out


FLIP_QUESTIONS = (
    ("grammatical", "coder_grammatical_coherent", "adjudicated_grammatical_coherent"),
    ("names_intended", "coder_names_intended_source", "adjudicated_names_intended_source"),
)


def evaluate_flips(
    coder_a: Dict[str, Dict[str, str]],
    coder_b: Optional[Dict[str, Dict[str, str]]],
    key: Dict[str, Dict[str, str]],
    adjudication: Optional[Dict[str, Dict[str, str]]] = None,
) -> Dict[str, Any]:
    """Flip quality rates and inter-coder agreement for the flip sheets.

    Rates are given per coder and as a combined value. The combined (headline) value is the
    adjudicated label when an adjudication is given, else 1 only when every coder who coded the row
    said 1 (a defect flagged by either coder counts), else the one coder. Coder order never matters.
    The rates certify mechanical edit quality (half-swaps, articles, garbling). The coding
    instructions count factual oddity as coherent, so they do not certify semantic coherence;
    adjudication rows with semantic_flag = 1 record known cross-sentence contradictions.
    """
    adjudication = adjudication or {}
    per: Dict[str, Dict[str, Any]] = {}
    rows = []
    for sid, krow in sorted(key.items()):
        entry = {"sid": sid, "model_id": krow.get("model_id"), "regime": krow.get("regime")}
        for q, col, adj_col in FLIP_QUESTIONS:
            a = _norm_bool(coder_a.get(sid, {}).get(col))
            b = _norm_bool(coder_b.get(sid, {}).get(col)) if coder_b else None
            adj = _norm_bool(adjudication.get(sid, {}).get(adj_col))
            coded = [v for v in (a, b) if v is not None]
            if adjudication:
                combined = adj if adj is not None else (coded[0] if coded and len(set(coded)) == 1 else None)
            else:
                combined = min(coded) if coded else None
            entry[q] = {"a": a, "b": b, "combined": combined}
        rows.append(entry)

    def rate(vals):
        vals = [v for v in vals if v is not None]
        ci = wilson_ci(sum(vals), len(vals))
        return {"n": len(vals), "rate": (sum(vals) / len(vals)) if vals else None, "wilson95": list(ci) if ci else None}

    for q, _, _ in FLIP_QUESTIONS:
        per[q] = {}
        for name, fn in SUBSETS.items():
            sub = [r for r in rows if fn(r["model_id"], r["regime"])]
            paired = [r for r in sub if r[q]["a"] is not None and r[q]["b"] is not None]
            per[q][name] = {
                "coder_a": rate(r[q]["a"] for r in sub),
                "coder_b": rate(r[q]["b"] for r in sub),
                "combined": rate(r[q]["combined"] for r in sub),
                "agreement": agreement_block([str(r[q]["a"]) for r in paired], [str(r[q]["b"]) for r in paired], ["0", "1"]),
            }

    by_model: Dict[str, Dict[str, List[int]]] = defaultdict(lambda: {"grammatical": [], "names_intended": []})
    for r in rows:
        for q, _, _ in FLIP_QUESTIONS:
            if r[q]["combined"] is not None:
                by_model[r["model_id"]][q].append(r[q]["combined"])

    g, s = per["grammatical"]["overall"], per["names_intended"]["overall"]
    # Prereg §8: every disagreement, and every flip either coder rated 0, needs an adjudicated value.
    unresolved = [
        r["sid"] for r in rows for q, _, adj_col in FLIP_QUESTIONS
        if ((r[q]["a"] is not None and r[q]["b"] is not None and r[q]["a"] != r[q]["b"]) or 0 in (r[q]["a"], r[q]["b"]))
        and _norm_bool(adjudication.get(r["sid"], {}).get(adj_col)) is None
    ]
    return {
        "n_key": len(key),
        "headline_basis": "adjudicated" if adjudication else ("any_coder_flags_defect" if coder_b else "coder_a"),
        "n_coded_grammatical": g["combined"]["n"],
        "grammatical_rate": g["combined"]["rate"],
        "grammatical_rate_wilson95": g["combined"]["wilson95"],
        "grammatical_agreement": g["agreement"]["agreement"],
        "grammatical_kappa": g["agreement"]["cohens_kappa"],
        "grammatical_ac1": g["agreement"]["gwet_ac1"],
        "grammatical_pabak": g["agreement"]["pabak"],
        "n_coded_intended_source": s["combined"]["n"],
        "names_intended_source_rate": s["combined"]["rate"],
        "names_intended_source_rate_wilson95": s["combined"]["wilson95"],
        "names_intended_agreement": s["agreement"]["agreement"],
        "names_intended_kappa": s["agreement"]["cohens_kappa"],
        "names_intended_ac1": s["agreement"]["gwet_ac1"],
        "names_intended_pabak": s["agreement"]["pabak"],
        "by_subset": per,
        "defects": {
            q: sorted(r["sid"] for r in rows if r[q]["combined"] == 0) for q, _, _ in FLIP_QUESTIONS
        },
        "semantic_flags": sorted(sid for sid, a in adjudication.items() if sid.startswith("F") and (a.get("semantic_flag") or "").strip() == "1"),
        "unadjudicated_disagreements": sorted(set(unresolved)) if adjudication else [],
        "by_model": {
            m: {
                "n_grammatical": len(d["grammatical"]),
                "grammatical_rate": (sum(d["grammatical"]) / len(d["grammatical"])) if d["grammatical"] else None,
                "n_intended": len(d["names_intended"]),
                "names_intended_source_rate": (sum(d["names_intended"]) / len(d["names_intended"])) if d["names_intended"] else None,
            }
            for m, d in sorted(by_model.items())
        },
    }


V_FIELDS = ["sample_id", "item_id", "model_id", "regime", "family", "order", "verbalization_text", "full_text", "coder_stated_source", "coder_notes"]
VK_FIELDS = ["sample_id", "item_id", "model_id", "regime", "family", "order", "predicted_stated_source", "beh_source", "verbalization_text", "full_text"]
F_FIELDS = ["sample_id", "item_id", "model_id", "regime", "order", "own_source", "intended_flip_source", "original_verbalization", "flipped_verbalization", "coder_grammatical_coherent", "coder_names_intended_source", "coder_notes"]
FK_FIELDS = ["sample_id", "item_id", "model_id", "regime", "order", "own_source", "flip_source", "jaccard_multiset_flip", "n_swaps", "original_verbalization", "flipped_verbalization"]
CODER_SHEETS = ("coder_A_verdicts.csv", "coder_B_verdicts.csv", "coder_A_flips.csv", "coder_B_flips.csv")
CODER_COLUMNS = ("coder_stated_source", "coder_grammatical_coherent", "coder_names_intended_source", "coder_notes")
# Columns that must match between regenerated keys and the coded sheets before --keys_only writes.
# Verdict text columns are left out: spreadsheet saves can reformat them (e.g. "20.4%" -> "20.40%").
VERDICT_IDENTITY = ("sample_id", "item_id", "model_id", "regime", "family", "order")
FLIP_IDENTITY = ("sample_id", "item_id", "model_id", "regime", "order", "own_source", "original_verbalization", "flipped_verbalization")


def default_donor_paths(input_dir: str) -> Tuple[List[str], List[str]]:
    """(used, skipped): *_donor_*.jsonl in input_dir, minus resolution-comparison runs."""
    found = sorted(glob.glob(os.path.join(input_dir, "*_donor_*.jsonl")))
    skipped = [p for p in found if _RESOLUTION_RUN.search(os.path.basename(p))]
    return [p for p in found if p not in skipped], skipped


def coded_sheets(out_dir: str) -> List[str]:
    """Coder sheets in out_dir that already hold any label or note."""
    hits = []
    for name in CODER_SHEETS:
        path = os.path.join(out_dir, name)
        if os.path.exists(path) and any(
            (r.get(c) or "").strip() for r in read_csv_map(path).values() for c in CODER_COLUMNS
        ):
            hits.append(name)
    return hits


def _norm_cell(v: Any) -> str:
    return str(v if v is not None else "").replace("\r\n", "\n")


def identity_mismatches(
    regenerated: Sequence[Dict[str, Any]], sheet: Dict[str, Dict[str, str]], columns: Sequence[str], sheet_alias: Optional[Dict[str, str]] = None
) -> List[str]:
    """sample_id:column for every identity cell where the regenerated key and a coded sheet differ."""
    sheet_alias = sheet_alias or {}
    out = []
    regen = {r["sample_id"]: r for r in regenerated}
    for sid in sorted(set(regen) | set(sheet)):
        if sid not in regen or sid not in sheet:
            out.append(f"{sid}:missing")
            continue
        for c in columns:
            if _norm_cell(regen[sid].get(c)) != _norm_cell(sheet[sid].get(sheet_alias.get(c, c))):
                out.append(f"{sid}:{c}")
    return out


def cmd_sample(args: argparse.Namespace) -> int:
    if args.donor_files:
        paths = list(args.donor_files)
    else:
        paths, skipped = default_donor_paths(args.input_dir)
        for p in skipped:
            print(f"Skipping resolution-comparison donor file {os.path.basename(p)} (pass --donor_files to include it).", file=sys.stderr)
    if not paths:
        print(f"No donor JSONL files found in {args.input_dir}", file=sys.stderr)
        return 2
    rows = load_donor_rows(paths)
    verdicts_blind, verdicts_key = build_verdict_samples(rows, args.n_donors, args.seed)
    flips_blind, flips_key = build_flip_samples(rows, args.n_flips_per_model, args.seed)

    os.makedirs(args.out_dir, exist_ok=True)
    v_fields, vk_fields, f_fields, fk_fields = V_FIELDS, VK_FIELDS, F_FIELDS, FK_FIELDS

    if args.keys_only:
        bad: List[str] = []
        for name, regen, columns, alias in (
            ("coder_A_verdicts.csv", verdicts_blind, VERDICT_IDENTITY, None),
            ("coder_B_verdicts.csv", verdicts_blind, VERDICT_IDENTITY, None),
            ("coder_A_flips.csv", flips_key, FLIP_IDENTITY, None),
            ("coder_B_flips.csv", flips_key, FLIP_IDENTITY, None),
        ):
            path = os.path.join(args.out_dir, name)
            if not os.path.exists(path):
                bad.append(f"{name}: missing")
                continue
            bad += [f"{name}: {m}" for m in identity_mismatches(regen, read_csv_map(path), columns, alias)]
            if name.endswith("_flips.csv"):
                bad += [
                    f"{name}: {m}"
                    for m in identity_mismatches(
                        [{"sample_id": r["sample_id"], "flip_source": r["flip_source"]} for r in flips_key],
                        read_csv_map(path), ("flip_source",), {"flip_source": "intended_flip_source"},
                    )
                ]
        if bad:
            print(f"--keys_only refused: the regenerated samples differ from the coded sheets in {len(bad)} cell(s):", file=sys.stderr)
            for m in bad[:25]:
                print(f"  {m}", file=sys.stderr)
            return 2
        write_csv(os.path.join(args.out_dir, "KEY_verdicts_do_not_open.csv"), verdicts_key, vk_fields)
        write_csv(os.path.join(args.out_dir, "KEY_flips_do_not_open.csv"), flips_key, fk_fields)
        print(f"Rewrote KEY files only ({len(verdicts_key)} verdict rows, {len(flips_key)} flip rows) in {args.out_dir}")
        return 0

    already = coded_sheets(args.out_dir)
    if already and not args.force:
        print(f"Refusing to overwrite coder sheets that hold labels: {', '.join(already)}. Use --keys_only, or --force to discard them.", file=sys.stderr)
        return 2

    for name in ("coder_A_verdicts.csv", "coder_B_verdicts.csv"):
        write_csv(os.path.join(args.out_dir, name), verdicts_blind, v_fields)
    write_csv(os.path.join(args.out_dir, "KEY_verdicts_do_not_open.csv"), verdicts_key, vk_fields)
    for name in ("coder_A_flips.csv", "coder_B_flips.csv"):
        write_csv(os.path.join(args.out_dir, name), flips_blind, f_fields)
    write_csv(os.path.join(args.out_dir, "KEY_flips_do_not_open.csv"), flips_key, fk_fields)
    with open(os.path.join(args.out_dir, "CODEBOOK_v5.md"), "w", encoding="utf-8") as f:
        f.write(CODEBOOK_MD)
    print(f"Wrote {len(verdicts_blind)} verdict rows and {len(flips_blind)} flip rows to {args.out_dir}")
    return 0


def cmd_evaluate(args: argparse.Namespace) -> int:
    ca_v = read_csv_map(os.path.join(args.out_dir, "coder_A_verdicts.csv"))
    cb_v_path = os.path.join(args.out_dir, "coder_B_verdicts.csv")
    cb_v = read_csv_map(cb_v_path) if os.path.exists(cb_v_path) else None
    key_v = read_csv_map(os.path.join(args.out_dir, "KEY_verdicts_do_not_open.csv"))

    ca_f = read_csv_map(os.path.join(args.out_dir, "coder_A_flips.csv"))
    cb_f_path = os.path.join(args.out_dir, "coder_B_flips.csv")
    cb_f = read_csv_map(cb_f_path) if os.path.exists(cb_f_path) else None
    key_f = read_csv_map(os.path.join(args.out_dir, "KEY_flips_do_not_open.csv"))

    adj_path = args.adjudicated if args.adjudicated is not None else os.path.join(args.out_dir, DEFAULT_ADJUDICATION)
    adjudication = read_adjudication(adj_path) if adj_path else {}
    report: Dict[str, Any] = {
        "pre_adjudication": {
            "verdicts": evaluate_verdicts(ca_v, cb_v, key_v),
            "flips": evaluate_flips(ca_f, cb_f, key_f),
        },
    }
    if adjudication:
        report["adjudicated"] = {
            "adjudication_file": os.path.basename(adj_path),
            "verdicts": evaluate_verdicts(ca_v, cb_v, key_v, adjudication),
            "flips": evaluate_flips(ca_f, cb_f, key_f, adjudication),
        }
    out_path = args.out_file or os.path.join(args.out_dir, "evaluation_v5.json")
    with open(out_path, "w", encoding="utf-8") as f:
        json.dump(report, f, indent=2)
    print(json.dumps(report, indent=2))
    return 0


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    sub = parser.add_subparsers(dest="cmd", required=True)

    sp = sub.add_parser("sample", help="Draw stratified blinded verdict and flip coding sheets")
    sp.add_argument("--input_dir", default=os.path.join(HERE, "results_v5"))
    sp.add_argument("--donor_files", nargs="*", default=None)
    sp.add_argument("--out_dir", default=os.path.join(HERE, "coding_v5"))
    sp.add_argument("--n_donors", type=int, default=200)
    sp.add_argument("--n_flips_per_model", type=int, default=50)
    sp.add_argument("--seed", type=int, default=42)
    sp.add_argument("--force", action="store_true", help="Overwrite coder sheets even if they already hold labels")
    sp.add_argument("--keys_only", action="store_true", help="Rewrite only KEY_*.csv, after checking the coded samples are unchanged")

    ev = sub.add_parser("evaluate", help="Score coded sheets against each other and the parser/gates")
    ev.add_argument("--out_dir", default=os.path.join(HERE, "coding_v5"))
    ev.add_argument("--adjudicated", default=None, help=f"Adjudication CSV (default: <out_dir>/{DEFAULT_ADJUDICATION} if present; '' to skip)")
    ev.add_argument("--out_file", default=None, help="Where to write the report (default: <out_dir>/evaluation_v5.json)")

    args = parser.parse_args()
    if args.cmd == "sample":
        return cmd_sample(args)
    return cmd_evaluate(args)


if __name__ == "__main__":
    sys.exit(main())
