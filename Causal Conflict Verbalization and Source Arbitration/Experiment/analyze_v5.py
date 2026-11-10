#!/usr/bin/env python3
"""Analysis for the v5 verdict transplant. Standard library only; runs locally.

Implements Docs/PREREGISTRATION_VERDICT_TRANSPLANT.md, §§2 and 7, on transplant_v5.py output.

For each model and regime it reports:
  T1   one-sided sign-flip permutation test of mean DiD > 0 (binding vs non-binding)
  T2   ρ_bind = CDE_ℓ,bind / Ceil_ℓ, read against ±0.25 with a 90% item-bootstrap CI
  T3   ρ_nonbind, the same
  the behavioural TOST at ε = 5.0 pp, the wording floor, the explicit ceiling per
  direction, the matched para/para_flip pair, order-specific effects, saturation
  tertiles, gate counts and timings
It also writes a long-format CSV and an R script for the lme4 fits (§7.4), which are
model-based estimates, not confirmatory tests.

Orientation. s = +1 when the flipped verdict names the image (chart) side and −1 when
it names the text (report) side, per item and order. Oriented by s, a positive CDE
means the answer moved toward the source the reversed verdict names. Ceil_ℓ is
explicit-image minus explicit-text, so it is positive when explicit control works.

Multiplicity (R7: Holm within each model x regime). T2 and T3 are read from CI
criteria, so Holm needs p-values for them. This script derives bootstrap p-values:
  T2/T3 decision-relevant  p = share of bootstrap ρ* ≤ 0.25
  T2/T3 equivalence        p = max(share ρ* ≥ 0.25, share ρ* ≤ −0.25)
The pre-registered readings come from the unadjusted CIs. Holm-adjusted p-values are
reported beside them.

Usage:
    python analyze_v5.py --runs results_v5/v5dev_conflict_tp_qwen25.jsonl \
        --gates results_v5/v5dev_conflict_tp_qwen25.gates.json \
        --base results_v5/v5dev_conflict_base_qwen25.jsonl --donor results_v5/v5dev_conflict_donor_qwen25.jsonl \
        --output_dir results_v5/analysis_dev
"""
from __future__ import annotations

import argparse
import csv
import json
import math
import os
import random
import sys
from collections import defaultdict
from typing import Any, Dict, Iterable, List, Optional, Sequence, Tuple

import score_v5 as sc

EPSILON = 0.05  # behavioural TOST margin (R4)
RHO_BOUND = 0.25  # graded margin (R4)
N_BOOT = 10_000
N_PERM = 10_000
SEED = 42
MIN_ITEMS = {"math": 150, "chartqa": 100}  # R5

IMAGE_SIDE = {"image", "chart"}

# ─── Loading ─────────────────────────────────────────────────────────────────


def load_rows(paths: Iterable[str]) -> List[Dict[str, Any]]:
    rows = []
    for p in paths:
        with open(p, encoding="utf-8") as f:
            for line in f:
                try:
                    r = json.loads(line)
                except json.JSONDecodeError:
                    continue
                if r.get("outcome") in ("dl", "beh"):
                    rows.append(r)
    return rows


def side(source: Optional[str]) -> Optional[str]:
    """Map a named source to the answer side it predicts: image or text."""
    if source is None:
        return None
    return "image" if source in IMAGE_SIDE else "text"


def orientation(row: Dict[str, Any]) -> int:
    """+1 if the reversed verdict names the image side for this row's item and order."""
    own = side(row["own_source"])
    return -1 if own == "image" else 1


def follows_named(row: Dict[str, Any]) -> Optional[bool]:
    """Behavioural: does the answer match the source this row's verdict names?"""
    src, _, _ = sc.behavioural_source(row["full_text"], row["regime"], row["y_image"], row["y_text"])
    named = side(row.get("named_source"))
    if named is None:
        return None
    return src == named


def follows_image(row: Dict[str, Any]) -> Optional[int]:
    src, _, _ = sc.behavioural_source(row["full_text"], row["regime"], row["y_image"], row["y_text"])
    return {"image": 1, "text": 0}.get(src)


# ─── Statistics ──────────────────────────────────────────────────────────────


def mean(xs: Sequence[float]) -> float:
    return sum(xs) / len(xs)


def resample_indices(n: int, reps: int, seed: int) -> List[List[int]]:
    rng = random.Random(seed)
    return [[rng.randrange(n) for _ in range(n)] for _ in range(reps)]


def percentile(sorted_xs: Sequence[float], q: float) -> float:
    """Linear-interpolated percentile of an already sorted list, q in [0, 1]."""
    if not sorted_xs:
        return float("nan")
    pos = q * (len(sorted_xs) - 1)
    lo, hi = math.floor(pos), math.ceil(pos)
    return sorted_xs[lo] + (sorted_xs[hi] - sorted_xs[lo]) * (pos - lo)


def boot_ci(values: Sequence[float], idx: Sequence[Sequence[int]], level: float) -> Tuple[float, float, List[float]]:
    stats = sorted(mean([values[i] for i in s]) for s in idx)
    a = (1 - level) / 2
    return percentile(stats, a), percentile(stats, 1 - a), stats


def boot_ratio(num: Sequence[float], den: Sequence[float], idx: Sequence[Sequence[int]]) -> List[Optional[float]]:
    """mean(num*)/mean(den*) per resample; None where the resampled denominator is 0."""
    out = []
    for s in idx:
        d = mean([den[i] for i in s])
        out.append(mean([num[i] for i in s]) / d if d != 0 else None)
    return out


def sign_flip_test(values: Sequence[float], draws: int, seed: int) -> Dict[str, Any]:
    """One-sided test of mean > 0: p = (1 + b)/(draws + 1), b = draws with mean ≥ observed."""
    rng = random.Random(seed)
    obs = mean(values)
    b = 0
    for _ in range(draws):
        m = sum(v if rng.random() < 0.5 else -v for v in values) / len(values)
        if m >= obs:
            b += 1
    return {"mean": obs, "b": b, "draws": draws, "p": (1 + b) / (draws + 1)}


def holm(pvals: Dict[str, float]) -> Dict[str, float]:
    items = sorted(pvals.items(), key=lambda kv: kv[1])
    m, out, running = len(items), {}, 0.0
    for rank, (name, p) in enumerate(items):
        running = max(running, min(1.0, (m - rank) * p))
        out[name] = running
    return out


def rho_reading(ceil_ci95: Tuple[float, float], rho_ci90: Optional[Tuple[float, float]]) -> str:
    if ceil_ci95[0] <= 0 <= ceil_ci95[1]:
        return "undetermined: prompt-level control too weak"
    lo, hi = rho_ci90
    if lo > RHO_BOUND:
        return "decision-relevant"
    if -RHO_BOUND < lo and hi < RHO_BOUND:
        return "equivalent to no effect"
    return "inconclusive"


def tost_reading(ci90: Tuple[float, float], eps: float = EPSILON) -> str:
    return "equivalent" if -eps < ci90[0] and ci90[1] < eps else "not equivalent"


def combined_reading(rho: str, tost: str, floor_ok: bool) -> str:
    """§2 table, under binding."""
    if rho.startswith("undetermined"):
        return "undetermined"
    if rho == "decision-relevant":
        return "H1: the verdict decides"
    if rho == "equivalent to no effect":
        if not floor_ok:
            return "graded equivalence only; behavioural test uninterpretable (wording floor > ε)"
        return "H0: saying is not choosing" if tost == "equivalent" else "mixed"
    return "inconclusive"


# ─── Per-item quantities (§7.1) ──────────────────────────────────────────────


def index_dl(rows: Sequence[Dict[str, Any]]) -> Tuple[Dict[Tuple, Dict[str, Any]], int]:
    """(id, family, verdict, k, order) -> row, dropping boundary mismatches."""
    out, dropped = {}, 0
    for r in rows:
        if r["outcome"] != "dl":
            continue
        if r.get("boundary_mismatch"):
            dropped += 1
            continue
        out[(r["id"], r["family"], r["verdict"], r["k"], r["order"])] = r
    return out, dropped


def item_ids(rows) -> List[str]:
    return sorted({r["id"] for r in rows})


def per_item(dl: Dict[Tuple, Dict[str, Any]], ids: Sequence[str], fn) -> Dict[str, float]:
    """Mean over (k, order) of fn(id, k, order); items with no complete cell are left out."""
    out = {}
    for i in ids:
        vals = []
        for k in range(1, 5):
            for o in ("image_first", "text_first"):
                v = fn(i, k, o)
                if v is not None:
                    vals.append(v)
        if vals:
            out[i] = mean(vals)
    return out


def _get(dl, i, fam, ver, k, o):
    r = dl.get((i, fam, ver, k, o))
    return None if r is None else r["dl"]


def cde_fn(dl, fam: str, pair=("flip", "own")):
    def f(i, k, o):
        a, b = _get(dl, i, fam, pair[0], k, o), _get(dl, i, fam, pair[1], k, o)
        if a is None or b is None:
            return None
        return orientation(dl[(i, fam, pair[0], k, o)]) * (a - b)

    return f


def ceil_fn(dl, which: str = "total"):
    def f(i, k, o):
        ei, et, nb = (_get(dl, i, fam, "none", k, o) for fam in ("explicit_image", "explicit_text", "nonbinding"))
        if which == "total":
            return None if ei is None or et is None else ei - et
        if which == "image":
            return None if ei is None or nb is None else ei - nb
        return None if nb is None or et is None else nb - et

    return f


def order_only(fn, order: str):
    return lambda i, k, o: fn(i, k, o) if o == order else None


def paired(a: Dict[str, float], b: Dict[str, float]) -> Tuple[List[str], List[float], List[float]]:
    ids = sorted(set(a) & set(b))
    return ids, [a[i] for i in ids], [b[i] for i in ids]


# ─── Behavioural (§6.2, §7.3) ────────────────────────────────────────────────


def behaviour_table(rows: Sequence[Dict[str, Any]]) -> Dict[Tuple, Dict[str, Any]]:
    """(id, family, verdict, order) -> {'follow': bool, 'image': 0/1/None}, k = lowest available."""
    out: Dict[Tuple, Dict[str, Any]] = {}
    for r in sorted((r for r in rows if r["outcome"] == "beh"), key=lambda r: r["k"]):
        key = (r["id"], r["family"], r["verdict"], r["order"])
        if key not in out:
            src, _, _ = sc.behavioural_source(r["full_text"], r["regime"], r["y_image"], r["y_text"])
            out[key] = {"follow": follows_named(r), "image": follows_image(r), "src": src, "row": r}
    return out


def beh_diff(beh, ids, fam: str, a: str, b: str) -> Dict[str, float]:
    """Per item, mean over orders of [answer follows T | a] − [answer follows T | b].

    T is the source that verdict a names. Both terms use the same target, so for
    a = flip and b = own this is the behavioural CDE toward the reversed verdict's
    source (prereg §7.3). An answer matching neither source counts as not following.
    """
    out = {}
    for i in ids:
        diffs = []
        for o in ("image_first", "text_first"):
            x, y = beh.get((i, fam, a, o)), beh.get((i, fam, b, o))
            target = side(x["row"].get("named_source")) if x else None
            if x and y and target is not None:
                diffs.append(float(x["src"] == target) - float(y["src"] == target))
        if diffs:
            out[i] = mean(diffs)
    return out


def change_rate(beh, ids, fam: str, a: str, b: str) -> Optional[float]:
    n = changed = 0
    for i in ids:
        for o in ("image_first", "text_first"):
            x, y = beh.get((i, fam, a, o)), beh.get((i, fam, b, o))
            if x and y:
                n += 1
                changed += x["image"] != y["image"]
    return changed / n if n else None


# ─── Secondary analyses from the base and donor files (§7.5) ─────────────────


def load_jsonl(paths: Iterable[str]) -> List[Dict[str, Any]]:
    rows = []
    for p in paths:
        with open(p, encoding="utf-8") as f:
            for line in f:
                try:
                    rows.append(json.loads(line))
                except json.JSONDecodeError:
                    continue
    return rows


def manipulation_check(donor_rows: Sequence[Dict[str, Any]]) -> Dict[str, Any]:
    """Free generation, nothing forced: does the stated verdict predict the answer's source?

    Reported for the non-binding rows (family "donor") and the binding rows
    (family "free_binding"). If binding does not raise agreement, the binding wording failed.
    """
    out: Dict[str, Any] = {}
    for fam in ("donor", "free_binding"):
        n = stated = attributable = agree = 0
        for r in donor_rows:
            if r.get("family") != fam or "full_text" not in r:
                continue
            n += 1
            verb, _ = sc.split_verbalization(r["full_text"])
            named = sc.stated_reliable_source(verb)
            if named not in sc.SOURCES[r["regime"]]:
                continue
            stated += 1
            src, _, _ = sc.behavioural_source(r["full_text"], r["regime"], r["y_image"], r["y_text"])
            if src in ("image", "text"):
                attributable += 1
                agree += src == side(named)
        out[fam] = {
            "rows": n,
            "with_stated_verdict": stated,
            "attributable_answers": attributable,
            "answer_follows_stated_verdict": agree / attributable if attributable else None,
        }
    return out


def relative_uncertainty(base_rows: Sequence[Dict[str, Any]]) -> Dict[str, float]:
    """ΔH_rel = 2(H_t − H_v)/(H_t + H_v) per item, from the gold-answer score rows of the base stage.

    H_v is the length-normalised NLL of the image answer under base_image; H_t that of
    the text answer under base_text (adapted from Zhang et al.; prereg §7.5).
    """
    h: Dict[str, Dict[str, float]] = defaultdict(dict)
    for r in base_rows:
        if r.get("outcome") != "nll" or r.get("boundary_mismatch"):
            continue
        if r["family"] == "base_image":
            h[r["id"]]["v"] = -r["lp_image"] / r["n_image"]
        elif r["family"] == "base_text":
            h[r["id"]]["t"] = -r["lp_text"] / r["n_text"]
    return {i: 2 * (d["t"] - d["v"]) / (d["t"] + d["v"]) for i, d in h.items() if len(d) == 2 and d["t"] + d["v"] > 0}


def logistic_1d(xs: Sequence[float], ys: Sequence[int], iters: int = 50) -> Optional[Tuple[float, float]]:
    """Intercept and slope of a one-predictor logistic regression (Newton's method)."""
    if len(set(ys)) < 2 or len(set(xs)) < 2:
        return None
    b0 = b1 = 0.0
    for _ in range(iters):
        g0 = g1 = h00 = h01 = h11 = 0.0
        for x, y in zip(xs, ys):
            p = 1 / (1 + math.exp(-max(-30.0, min(30.0, b0 + b1 * x))))
            w = p * (1 - p)
            g0 += y - p
            g1 += (y - p) * x
            h00 += w
            h01 += w * x
            h11 += w * x * x
        h00 += 1e-6  # a small ridge keeps separable data from diverging
        h11 += 1e-6
        det = h00 * h11 - h01 * h01
        if det <= 0:
            return None
        d0, d1 = (h11 * g0 - h01 * g1) / det, (h00 * g1 - h01 * g0) / det
        b0, b1 = b0 + d0, b1 + d1
        if abs(d0) + abs(d1) < 1e-9:
            break
    return b0, b1


def uncertainty_strata(dh: Dict[str, float], baseline: Dict[str, float], cde: Dict[str, float], radius: float = 0.5) -> Dict[str, Any]:
    """CDE inside vs. outside ±radius of the balance point.

    The balance point is the ΔH_rel at which the baseline answer (sign of Δℓ under
    non-binding with no verdict) is equally likely to favour either source.
    """
    ids = sorted(set(dh) & set(baseline) & set(cde))
    fit = logistic_1d([dh[i] for i in ids], [int(baseline[i] > 0) for i in ids]) if len(ids) >= 10 else None
    if fit is None or fit[1] == 0:
        return {"n": len(ids), "balance_point": None, "note": "balance point not estimable"}
    bp = -fit[0] / fit[1]
    inside = [cde[i] for i in ids if abs(dh[i] - bp) <= radius]
    outside = [cde[i] for i in ids if abs(dh[i] - bp) > radius]
    return {
        "n": len(ids),
        "balance_point": bp,
        "slope": fit[1],
        "inside": {"n": len(inside), "cde_mean": mean(inside) if inside else None},
        "outside": {"n": len(outside), "cde_mean": mean(outside) if outside else None},
    }


# ─── One model x regime ──────────────────────────────────────────────────────


def summarize_ci(values: Sequence[float], reps: int, seed: int, level: float) -> Dict[str, Any]:
    idx = resample_indices(len(values), reps, seed)
    lo, hi, _ = boot_ci(values, idx, level)
    return {"n": len(values), "mean": mean(values), f"ci{int(level * 100)}": [lo, hi]}


def analyze_group(
    rows: Sequence[Dict[str, Any]],
    reps: int = N_BOOT,
    draws: int = N_PERM,
    seed: int = SEED,
    base_rows: Sequence[Dict[str, Any]] = (),
    donor_rows: Sequence[Dict[str, Any]] = (),
) -> Dict[str, Any]:
    regime = rows[0]["regime"]
    dl, dropped = index_dl(rows)
    ids = item_ids(rows)
    n_dl_rows = sum(1 for r in rows if r["outcome"] == "dl")
    res: Dict[str, Any] = {
        "model_id": rows[0]["model_id"],
        "regime": regime,
        "phase": rows[0].get("phase"),
        "n_items": len(ids),
        "boundary_mismatch_rows": dropped,
        "boundary_mismatch_share": dropped / n_dl_rows if n_dl_rows else None,
    }

    d_bind = per_item(dl, ids, cde_fn(dl, "binding"))
    d_non = per_item(dl, ids, cde_fn(dl, "nonbinding"))
    ceil = per_item(dl, ids, ceil_fn(dl))

    # Common item set for the confirmatory quantities.
    common = sorted(set(d_bind) & set(d_non) & set(ceil))
    res["n_analysed"] = len(common)
    res["meets_min_items"] = len(common) >= MIN_ITEMS[regime]
    if len(common) < 2:
        res["error"] = "fewer than two items with every confirmatory cell"
        return res
    idx = resample_indices(len(common), reps, seed)
    vb, vn, vc = ([d[i] for i in common] for d in (d_bind, d_non, ceil))
    did = [b - n for b, n in zip(vb, vn)]

    c_lo95, c_hi95, _ = boot_ci(vc, idx, 0.95)
    res["ceil"] = {"mean": mean(vc), "ci95": [c_lo95, c_hi95]}
    for which in ("image", "text"):
        per = per_item(dl, common, ceil_fn(dl, which))
        vals = [per[i] for i in common if i in per]
        if len(vals) > 1:
            res[f"ceil_{which}_direction"] = summarize_ci(vals, reps, seed, 0.95)

    pvals: Dict[str, float] = {}
    t1 = sign_flip_test(did, draws, seed)
    res["T1_did"] = {**t1, "ci95": list(boot_ci(did, idx, 0.95)[:2])}
    pvals["T1"] = t1["p"]

    for name, vals in (("T2_rho_binding", vb), ("T3_rho_nonbinding", vn)):
        cde_lo, cde_hi, _ = boot_ci(vals, idx, 0.95)
        entry: Dict[str, Any] = {"cde": mean(vals), "cde_ci95": [cde_lo, cde_hi]}
        if c_lo95 <= 0 <= c_hi95:
            entry["reading"] = rho_reading((c_lo95, c_hi95), None)
        else:
            boots = sorted(x for x in boot_ratio(vals, vc, idx) if x is not None)
            rho_ci = (percentile(boots, 0.05), percentile(boots, 0.95))
            entry.update(
                rho=mean(vals) / mean(vc),
                rho_ci90=list(rho_ci),
                reading=rho_reading((c_lo95, c_hi95), rho_ci),
                p_decision_relevant=(1 + sum(x <= RHO_BOUND for x in boots)) / (len(boots) + 1),
                p_equivalent=(1 + max(sum(x >= RHO_BOUND for x in boots), sum(x <= -RHO_BOUND for x in boots))) / (len(boots) + 1),
            )
            key = name.split("_")[0]
            pvals[f"{key}_decision_relevant"] = entry["p_decision_relevant"]
            pvals[f"{key}_equivalent"] = entry["p_equivalent"]
        res[name] = entry
    res["holm_adjusted"] = holm(pvals)

    # Behavioural (secondary): TOST and wording floor, per binding level.
    beh = behaviour_table(rows)
    floor_ok = True
    for fam in ("binding", "nonbinding"):
        delta = beh_diff(beh, ids, fam, "flip", "own")
        floor = beh_diff(beh, ids, fam, "para", "own")
        entry = {}
        if len(delta) > 1:
            ci = summarize_ci(list(delta.values()), reps, seed, 0.90)
            entry["delta_flip_minus_own"] = {**ci, "reading": tost_reading(tuple(ci["ci90"]))}
        if len(floor) > 1:
            fm = mean(list(floor.values()))
            entry["wording_floor_para_minus_own"] = {"n": len(floor), "mean": fm, "exceeds_epsilon": abs(fm) > EPSILON}
            if fam == "binding" and abs(fm) > EPSILON:
                floor_ok = False
        entry["change_rate_own_vs_para"] = change_rate(beh, ids, fam, "own", "para")
        entry["change_rate_own_vs_flip"] = change_rate(beh, ids, fam, "own", "flip")
        res[f"behaviour_{fam}"] = entry
    tost = res.get("behaviour_binding", {}).get("delta_flip_minus_own", {}).get("reading", "not available")
    res["reading_binding"] = combined_reading(res["T2_rho_binding"]["reading"], tost, floor_ok)

    # Secondary: matched pair, order, saturation, neither-rate.
    sec: Dict[str, Any] = {}
    for fam in ("binding", "nonbinding"):
        mp = per_item(dl, ids, cde_fn(dl, fam, ("para_flip", "para")))
        if len(mp) > 1:
            sec[f"matched_pair_{fam}"] = summarize_ci(list(mp.values()), reps, seed, 0.95)
        for order in ("image_first", "text_first"):
            od = per_item(dl, ids, order_only(cde_fn(dl, fam), order))
            if len(od) > 1:
                sec[f"cde_{fam}_{order}"] = summarize_ci(list(od.values()), reps, seed, 0.95)
    base = per_item(dl, common, lambda i, k, o: _get(dl, i, "nonbinding", "none", k, o))
    if len(base) >= 6:
        ranked = sorted(common, key=lambda i: abs(base.get(i, 0.0)))
        third = len(ranked) // 3
        for t, chunk in enumerate((ranked[:third], ranked[third : 2 * third], ranked[2 * third :]), 1):
            vals = [d_bind[i] for i in chunk]
            sec[f"cde_binding_baseline_abs_dl_tertile{t}"] = {"n": len(vals), "mean": mean(vals) if vals else None}
    beh_rows = [r for r in rows if r["outcome"] == "beh"]
    if beh_rows:
        sec["behaviour_neither_rate"] = sum(follows_image(r) is None for r in beh_rows) / len(beh_rows)
        if regime == "chartqa":
            sec["chartqa_answer_only_match_share"] = 1 - sec["behaviour_neither_rate"]
    secs = defaultdict(float)
    for r in rows:
        secs[r["id"]] += r.get("wall_s") or 0.0
    sec["seconds_per_item"] = mean(list(secs.values())) if secs else None
    verdict_nll: Dict[str, List[float]] = defaultdict(list)
    for r in rows:
        if r["outcome"] == "dl" and r.get("verdict_nll") is not None:
            verdict_nll[r["verdict"]].append(r["verdict_nll"])
    if verdict_nll:
        sec["verdict_nll_mean_by_verdict"] = {k: mean(v) for k, v in sorted(verdict_nll.items())}
    mine = lambda rs: [r for r in rs if r.get("model_id") == res["model_id"] and r.get("regime") == regime]
    if mine(donor_rows):
        sec["manipulation_check"] = manipulation_check(mine(donor_rows))
    dh = relative_uncertainty(mine(base_rows))
    if dh:
        sec["relative_uncertainty_binding"] = uncertainty_strata(dh, base, d_bind)
    res["secondary"] = sec
    return res


# ─── Output ──────────────────────────────────────────────────────────────────

CSV_FIELDS = ["model_id", "regime", "item", "outcome", "family", "verdict", "k", "order", "D", "B", "O", "dl", "y_image", "named_source", "own_source"]


def export_long(rows: Sequence[Dict[str, Any]], path: str) -> int:
    """Rows for lme4: own and flip verdicts under non-binding and binding (§7.4)."""
    n = 0
    with open(path, "w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=CSV_FIELDS)
        w.writeheader()
        for r in rows:
            if r["family"] not in ("binding", "nonbinding") or r["verdict"] not in ("own", "flip"):
                continue
            if r["outcome"] == "dl" and r.get("boundary_mismatch"):
                continue
            w.writerow(
                {
                    "model_id": r["model_id"],
                    "regime": r["regime"],
                    "item": r["id"],
                    "outcome": r["outcome"],
                    "family": r["family"],
                    "verdict": r["verdict"],
                    "k": r["k"],
                    "order": r["order"],
                    "D": 0.5 if side(r["named_source"]) == "image" else -0.5,
                    "B": r["B"],
                    "O": r["O"],
                    "dl": r.get("dl") if r["outcome"] == "dl" else "",
                    "y_image": "" if r["outcome"] == "dl" else ("" if follows_image(r) is None else follows_image(r)),
                    "named_source": r["named_source"],
                    "own_source": r["own_source"],
                }
            )
            n += 1
    return n


R_SCRIPT = r"""# lme4 fits for the v5 verdict transplant (prereg §7.4). Model-based estimates only.
# Run on Colab:  Rscript analyze_v5_lme4.R long_v5.csv lme4_out.txt
suppressPackageStartupMessages(library(lme4))
args <- commandArgs(trailingOnly = TRUE)
d <- read.csv(args[1], stringsAsFactors = FALSE)
sink(args[2])
for (g in unique(paste(d$model_id, d$regime))) {
  s <- d[paste(d$model_id, d$regime) == g, ]
  s$K <- factor(s$k); contrasts(s$K) <- contr.sum(4)
  cat("\n=====", g, "=====\n")
  fit_lmm <- function(f) tryCatch(lmer(f, data = subset(s, outcome == "dl")), error = function(e) e)
  m <- fit_lmm(dl ~ D*B + D*O + K + (1 + D | item))
  if (inherits(m, "error") || isSingular(m)) { cat("lmer: by-item slope dropped\n"); m <- fit_lmm(dl ~ D*B + D*O + K + (1 | item)) }
  if (inherits(m, "error") || isSingular(m)) cat("lmer: FAILED (singular or error)\n") else print(summary(m))
  b <- subset(s, outcome == "beh" & !is.na(y_image))
  if (nrow(b) > 0) {
    ctl <- glmerControl(optimizer = "bobyqa", optCtrl = list(maxfun = 2e5))
    fit_glmm <- function(f) tryCatch(glmer(f, data = b, family = binomial, control = ctl), error = function(e) e)
    gm <- fit_glmm(y_image ~ D*B + D*O + (1 + D | item))  # behavioural rows use k = 1 only, so no K term
    if (inherits(gm, "error") || isSingular(gm)) { cat("glmer: by-item slope dropped\n"); gm <- fit_glmm(y_image ~ D*B + D*O + (1 | item)) }
    if (inherits(gm, "error") || isSingular(gm)) cat("glmer: FAILED (singular or error)\n") else print(summary(gm))
  }
}
cat("\n"); print(sessionInfo())
sink()
"""


def fmt(x, digits=3):
    if x is None:
        return "n/a"
    if isinstance(x, (list, tuple)):
        return "[" + ", ".join(fmt(v, digits) for v in x) + "]"
    return f"{x:.{digits}f}" if isinstance(x, float) else str(x)


def render(results: Sequence[Dict[str, Any]], gates: Dict[str, Any]) -> str:
    lines = ["# v5 analysis", "", "Δℓ is image minus text. CDE is oriented toward the source the reversed verdict names.", ""]
    if any(r.get("phase") == "dev" for r in results):
        lines += ["**Dev data: for tuning and the freeze record only, not findings.**", ""]
    for r in results:
        lines += [f"## {r['model_id']} | {r['regime']} | {r['phase']}", ""]
        lines += [f"- Items: {r['n_items']}; analysed: {r.get('n_analysed')}; meets R5 minimum: {r.get('meets_min_items')}"]
        lines += [f"- Boundary mismatches: {r['boundary_mismatch_rows']} rows ({fmt(r['boundary_mismatch_share'])}; gate ≤ 0.01)"]
        if "error" in r:
            lines += [f"- **{r['error']}**", ""]
            continue
        lines += [f"- Ceil_ℓ: {fmt(r['ceil']['mean'])}, 95% CI {fmt(r['ceil']['ci95'])}"]
        for wd in ("image", "text"):
            c = r.get(f"ceil_{wd}_direction")
            if c:
                lines += [f"  - {wd} direction vs non-binding: {fmt(c['mean'])}, 95% CI {fmt(c['ci95'])}"]
        t1 = r["T1_did"]
        lines += [f"- **T1** DiD = {fmt(t1['mean'])} (95% CI {fmt(t1['ci95'])}), sign-flip p = {fmt(t1['p'], 4)}"]
        for name in ("T2_rho_binding", "T3_rho_nonbinding"):
            e = r[name]
            rho = f"ρ = {fmt(e.get('rho'))}, 90% CI {fmt(e.get('rho_ci90'))}" if "rho" in e else "ρ not computed"
            lines += [f"- **{name.split('_')[0]}** CDE = {fmt(e['cde'])} (95% CI {fmt(e['cde_ci95'])}); {rho}; reading: **{e['reading']}**"]
        lines += [f"- Holm-adjusted p: {json.dumps({k: round(v, 4) for k, v in r['holm_adjusted'].items()})}"]
        for fam in ("binding", "nonbinding"):
            b = r.get(f"behaviour_{fam}", {})
            d = b.get("delta_flip_minus_own")
            fl = b.get("wording_floor_para_minus_own")
            lines += [
                f"- Behavioural, {fam}: Δ = {fmt(d and d['mean'])}, 90% CI {fmt(d and d['ci90'])}, TOST: {d and d['reading']}; "
                f"wording floor {fmt(fl and fl['mean'])}; change rate own vs para {fmt(b.get('change_rate_own_vs_para'))}, "
                f"own vs flip {fmt(b.get('change_rate_own_vs_flip'))}"
            ]
        lines += [f"- **Combined reading under binding: {r['reading_binding']}**", "", "Secondary:", ""]
        for k, v in r["secondary"].items():
            lines += [f"- {k}: {fmt(v) if not isinstance(v, dict) else json.dumps({a: (round(b, 4) if isinstance(b, float) else b) for a, b in v.items()})}"]
        lines += [""]
    if gates:
        lines += ["## Gate reports", ""]
        for name, g in gates.items():
            lines += [f"- {name}: " + json.dumps({k: v for k, v in g.items() if k != "passed_ids"})]
    return "\n".join(lines) + "\n"


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("--runs", nargs="+", required=True)
    parser.add_argument("--gates", nargs="*", default=[])
    parser.add_argument("--base", nargs="*", default=[], help="Base-stage files: adds the relative-uncertainty strata")
    parser.add_argument("--donor", nargs="*", default=[], help="Donor-stage files: adds the manipulation check")
    parser.add_argument("--output_dir", required=True)
    parser.add_argument("--reps", type=int, default=N_BOOT)
    parser.add_argument("--draws", type=int, default=N_PERM)
    parser.add_argument("--seed", type=int, default=SEED)
    args = parser.parse_args()

    rows = load_rows(args.runs)
    if not rows:
        print("No transplant rows found.", file=sys.stderr)
        return 2
    groups: Dict[Tuple[str, str], List[Dict[str, Any]]] = defaultdict(list)
    for r in rows:
        groups[(r["model_id"], r["regime"])].append(r)
    base_rows, donor_rows = load_jsonl(args.base), load_jsonl(args.donor)
    results = [analyze_group(g, args.reps, args.draws, args.seed, base_rows, donor_rows) for _, g in sorted(groups.items())]
    gates = {}
    for p in args.gates:
        with open(p, encoding="utf-8") as f:
            gates[os.path.basename(p)] = json.load(f)

    os.makedirs(args.output_dir, exist_ok=True)
    with open(os.path.join(args.output_dir, "analysis_v5.json"), "w", encoding="utf-8") as f:
        json.dump({"results": results, "gates": gates}, f, indent=2)
    with open(os.path.join(args.output_dir, "analysis_v5.md"), "w", encoding="utf-8") as f:
        f.write(render(results, gates))
    n = export_long(rows, os.path.join(args.output_dir, "long_v5.csv"))
    with open(os.path.join(args.output_dir, "analyze_v5_lme4.R"), "w", encoding="utf-8") as f:
        f.write(R_SCRIPT)
    print(f"Wrote analysis_v5.json, analysis_v5.md, long_v5.csv ({n} rows) and analyze_v5_lme4.R to {args.output_dir}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
