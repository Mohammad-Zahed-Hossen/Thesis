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
  In Math the primary rule is behavioural (prereg §2.3): the behavioural Δ itself is read
  against ε = 5 pp (decision_test), with the explicit-instruction benchmark B_beh as a
  manipulation check and ρ_beh descriptive only.
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
MAX_CHURN = EPSILON  # wording-floor gate on the share of answers a paraphrase changes (prereg §7.6)
MAX_NEITHER_SHIFT = 0.10  # wording-floor guard: |P(neither | para) − P(neither | own)| (prereg §7.6, revised 2026-11-14)
ALPHA = 0.05
POWER_TARGET = 0.80
RHO_BOUND = 0.25  # graded margin (R4)
N_BOOT = 10_000
N_PERM = 10_000
SEED = 42
MIN_ITEMS = {"math": 150, "chartqa": 100}  # R5

MODEL_3B = "Qwen/Qwen2.5-VL-3B-Instruct"
MODEL_7B = "Qwen/Qwen2.5-VL-7B-Instruct"

DIAGNOSTIC_MODELS = {"Qwen/Qwen2-VL-2B-Instruct"}  # Pre-freeze D3
EXPLORATORY_REGIMES = {"chartqa"}  # Pre-freeze D4

IMAGE_SIDE = {"image", "chart"}


def confirmatory_role(model_id: str, regime: str) -> str:
    """Confirmatory designation after pre-freeze decisions D3 & D4."""
    if model_id in DIAGNOSTIC_MODELS:
        return "diagnostic_only"
    if regime in EXPLORATORY_REGIMES:
        return "exploratory"
    return "confirmatory"

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


# The Math answer parser used for the headline behavioural numbers (pre-freeze D3: "structured",
# keeping #### as first choice and allowing clean final-answer statements / \boxed{X}).
# Strict and lenient are still reported side by side in behaviour_by_parser.
HEADLINE_PARSER = "structured"


def follows_named(row: Dict[str, Any], allow_math_fallback: bool = True, parser: Optional[str] = None) -> Optional[bool]:
    """Behavioural: does the answer match the source this row's verdict names?"""
    src, _, _ = sc.behavioural_source(
        row["full_text"], row["regime"], row["y_image"], row["y_text"], allow_math_fallback=allow_math_fallback, parser=parser
    )
    named = side(row.get("named_source"))
    if named is None:
        return None
    return src == named


def follows_image(row: Dict[str, Any], allow_math_fallback: bool = True, parser: Optional[str] = None) -> Optional[int]:
    src, _, _ = sc.behavioural_source(
        row["full_text"], row["regime"], row["y_image"], row["y_text"], allow_math_fallback=allow_math_fallback, parser=parser
    )
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


def normal_cdf(z: float) -> float:
    return 0.5 * (1 + math.erf(z / math.sqrt(2)))


def tost_power(sd: float, n: int, eps: float = EPSILON) -> float:
    """Power of the TOST at margin eps when the true effect is 0 (normal approximation).

    sd is the standard deviation of the per-item differences. Power is
    2Φ(eps/SE − z_0.95) − 1, floored at 0, with SE = sd/√n.
    """
    if n < 2:
        return 0.0
    if sd <= 0:
        return 1.0
    return max(0.0, 2 * normal_cdf(eps / (sd / math.sqrt(n)) - 1.6448536269514722) - 1)


def sample_sd(xs: Sequence[float]) -> float:
    m = mean(xs)
    return math.sqrt(sum((x - m) ** 2 for x in xs) / (len(xs) - 1)) if len(xs) > 1 else 0.0


def wording_floor(
    diffs: Sequence[float],
    churn: Optional[float],
    replay_flip_rate: Optional[float] = None,
    neither_shift: Optional[float] = None,
    any_change: Optional[float] = None,
) -> Dict[str, Any]:
    """The wording-floor gate for m_para vs. m_own (prereg §7.6, revised 2026-11-14).

    The gate fails if any of these holds:
      |signed mean| > ε          mean per-item difference; opposite changes cancel in it
      churn_rate > ε             share of attributable (item, order) cells that flip image<->text
      |neither_shift| > 0.10     change in the share of non-attributable answers, para − own
    The limit is fixed. Replay noise and any-change churn are reported as diagnostics
    only: they never move the limit (the D5 replay clause was dropped on 2026-11-14).
    """
    fm = mean(diffs)
    sd = sample_sd(diffs)
    power = tost_power(sd, len(diffs))
    signed_bad = abs(fm) > EPSILON
    churn_bad = churn is not None and churn > MAX_CHURN
    neither_bad = neither_shift is not None and abs(neither_shift) > MAX_NEITHER_SHIFT
    replay_cap = (replay_flip_rate + MAX_CHURN) if replay_flip_rate is not None else None
    return {
        "n": len(diffs),
        "signed_mean": fm,
        "mean": fm,  # kept for earlier readers of this file
        "signed_mean_exceeds_epsilon": signed_bad,
        "exceeds_epsilon": signed_bad,
        "churn_rate": churn,
        "max_churn": MAX_CHURN,
        "churn_exceeds_max": churn_bad,
        "neither_shift": neither_shift,
        "max_neither_shift": MAX_NEITHER_SHIFT,
        "neither_shift_exceeds_max": neither_bad,
        "any_change_rate_diagnostic": any_change,
        "replay_flip_rate_diagnostic": replay_flip_rate,
        "replay_adjusted_max_churn": replay_cap,  # diagnostic only; not a limit
        "sd_item_difference": sd,
        "tost_power_at_this_noise": power,
        "power_below_target": power < POWER_TARGET,
        "floor_ok": not (signed_bad or churn_bad or neither_bad),
    }


def combined_reading(rho: str, tost: str, floor_ok: bool, t1_significant: bool = False) -> str:
    """§2 decision table, under binding. T1 qualifies an H1 reading; it never decides one."""
    if rho.startswith("undetermined"):
        return "undetermined"
    if rho == "decision-relevant":
        if t1_significant:
            return "H1: the verdict decides, and binding strengthens it"
        return "H1: the verdict decides; no evidence that binding strengthens it"
    if rho == "equivalent to no effect":
        if not floor_ok:
            return "graded equivalence only; behavioural test uninterpretable (wording floor > ε)"
        if tost == "equivalent":
            return "H0: saying is not choosing"
        return "inconclusive: graded equivalence, but the behavioural TOST does not show equivalence"
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


def abs_gap_fn(dl, fam: str, a: str, b: str):
    """|Δℓ(a) − Δℓ(b)| per cell, for the descriptive noise floor (§7.6)."""

    def f(i, k, o):
        x, y = _get(dl, i, fam, a, k, o), _get(dl, i, fam, b, k, o)
        return None if x is None or y is None else abs(x - y)

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


def behaviour_table(
    rows: Sequence[Dict[str, Any]], allow_math_fallback: bool = True, parser: Optional[str] = None
) -> Dict[Tuple, Dict[str, Any]]:
    """(id, family, verdict, order) -> {'follow': bool, 'image': 0/1/None}, k = lowest available.

    parser picks the Math answer parser (score_v5.MATH_PARSERS); None keeps allow_math_fallback.
    """
    out: Dict[Tuple, Dict[str, Any]] = {}
    for r in sorted((r for r in rows if r["outcome"] == "beh"), key=lambda r: r["k"]):
        key = (r["id"], r["family"], r["verdict"], r["order"])
        if key not in out:
            src, _, method = sc.behavioural_source(
                r["full_text"], r["regime"], r["y_image"], r["y_text"], allow_math_fallback=allow_math_fallback, parser=parser
            )
            out[key] = {
                "follow": follows_named(r, allow_math_fallback=allow_math_fallback, parser=parser),
                "image": follows_image(r, allow_math_fallback=allow_math_fallback, parser=parser),
                "src": src,
                "method": method,
                "row": r,
            }
    return out


def reversed_target(row: Dict[str, Any]) -> Optional[str]:
    """Side opposite own_source (the target that flip / para_flip point toward)."""
    ns = side(row.get("named_source"))
    if row.get("verdict") in ("flip", "para_flip") and ns is not None:
        return ns
    own = side(row.get("own_source"))
    if own is None:
        return None
    return "text" if own == "image" else "image"


def beh_diff(beh, ids, fam: str, a: str, b: str, target_only: Optional[str] = None) -> Dict[str, float]:
    """Per item, mean over orders of [answer follows T | a] − [answer follows T | b].

    T is the source that verdict a names (or the reversed source when a == 'none').
    Both terms use the same target, so for a = flip and b = own this is the behavioural
    CDE toward the reversed verdict's source (prereg §7.3), and (none - own) + (flip - none)
    sums identically to (flip - own).
    """
    out = {}
    for i in ids:
        diffs = []
        for o in ("image_first", "text_first"):
            x, y = beh.get((i, fam, a, o)), beh.get((i, fam, b, o))
            if not (x and y):
                continue
            target = reversed_target(y["row"]) if a == "none" else (side(x["row"].get("named_source")) or reversed_target(x["row"]))
            if target is not None and (target_only is None or target == target_only):
                diffs.append(float(x["src"] == target) - float(y["src"] == target))
        if diffs:
            out[i] = mean(diffs)
    return out


def donor_replay_noise(
    beh: Dict[Tuple, Dict[str, Any]], donor_rows: Sequence[Dict[str, Any]], ids: Sequence[str], parser: str
) -> Optional[Dict[str, Any]]:
    """Measure unforced replay noise by comparing stage-2 donor decodes vs stage-3 nonbinding own decodes (D5)."""
    id_set = set(ids)
    total = attributable = flips = any_changes = 0
    for r in donor_rows:
        if r.get("family") != "donor" or r.get("id") not in id_set or "full_text" not in r:
            continue
        own = beh.get((r["id"], "nonbinding", "own", r["order"]))
        if not own:
            continue
        donor_src, _, _ = sc.behavioural_source(r["full_text"], r["regime"], r["y_image"], r["y_text"], parser=parser)
        total += 1
        if donor_src != own["src"]:
            any_changes += 1
        if donor_src in ("image", "text") and own["src"] in ("image", "text"):
            attributable += 1
            if donor_src != own["src"]:
                flips += 1
    if total == 0:
        return None
    flip_rate = flips / attributable if attributable else None
    return {
        "n_pairs": total,
        "attributable_pairs": attributable,
        "replay_flip_rate": flip_rate,
        "replay_any_change_rate": any_changes / total,
    }


def change_rate(beh, ids, fam: str, a: str, b: str) -> Optional[float]:
    """Share of attributable (image/text in both arms) (item, order) pairs that flip image<->text."""
    n = changed = 0
    for i in ids:
        for o in ("image_first", "text_first"):
            x, y = beh.get((i, fam, a, o)), beh.get((i, fam, b, o))
            if x and y and x["src"] in ("image", "text") and y["src"] in ("image", "text"):
                n += 1
                changed += x["src"] != y["src"]
    return changed / n if n else None


def neither_transition_rate(beh, ids, fam: str, a: str, b: str) -> Optional[float]:
    """Share of (item, order) pairs where either arm produced a non-attributable ('neither'/'both') answer."""
    n = non_attr = 0
    for i in ids:
        for o in ("image_first", "text_first"):
            x, y = beh.get((i, fam, a, o)), beh.get((i, fam, b, o))
            if x and y:
                n += 1
                if x["src"] not in ("image", "text") or y["src"] not in ("image", "text"):
                    non_attr += 1
    return non_attr / n if n else None


def neither_shift(beh, ids, fam: str, a: str, b: str) -> Optional[float]:
    """P(non-attributable | a) − P(non-attributable | b) over (item, order) pairs present in both arms."""
    n = 0
    total = 0.0
    for i in ids:
        for o in ("image_first", "text_first"):
            x, y = beh.get((i, fam, a, o)), beh.get((i, fam, b, o))
            if x and y:
                n += 1
                total += float(x["src"] not in ("image", "text")) - float(y["src"] not in ("image", "text"))
    return total / n if n else None


def any_change_rate(beh, ids, fam: str, a: str, b: str) -> Optional[float]:
    """Share of (item, order) pairs whose answer source differs at all, "neither" included.

    This is the letter of prereg §7.6 ("changes at all"). change_rate() counts only
    image<->text flips among pairs where both answers are attributable. Both are reported.
    """
    n = changed = 0
    for i in ids:
        for o in ("image_first", "text_first"):
            x, y = beh.get((i, fam, a, o)), beh.get((i, fam, b, o))
            if x and y:
                n += 1
                changed += x["src"] != y["src"]
    return changed / n if n else None


def attributable_pairs(beh, ids, fam: str, a: str, b: str) -> int:
    return sum(
        1
        for i in ids
        for o in ("image_first", "text_first")
        if beh.get((i, fam, a, o)) and beh.get((i, fam, b, o))
        and beh[(i, fam, a, o)]["src"] in ("image", "text") and beh[(i, fam, b, o)]["src"] in ("image", "text")
    )


def auc(pos: Sequence[float], neg: Sequence[float]) -> Optional[float]:
    """P(a random value in pos exceeds a random value in neg), ties counted as half."""
    if not pos or not neg:
        return None
    ordered = sorted([(v, 1) for v in pos] + [(v, 0) for v in neg])
    rank_sum, i = 0.0, 0
    while i < len(ordered):
        j = i
        while j < len(ordered) and ordered[j][0] == ordered[i][0]:
            j += 1
        rank_sum += ((i + j + 1) / 2) * sum(lab for _, lab in ordered[i:j])
        i = j
    return (rank_sum - len(pos) * (len(pos) + 1) / 2) / (len(pos) * len(neg))


def validity_diagnostics(rows: Sequence[Dict[str, Any]], parser: str = "strict") -> Dict[str, Any]:
    """Does Δℓ track the answer the model then gives? Each behavioural row is paired with
    the Δℓ row of the same (item, family, verdict, order) cell at the same template k.

    sign_agreement     share of attributable answers whose source matches the sign of Δℓ
    majority_baseline  what always guessing the commoner answer source would score
    auc_<order>        AUC of Δℓ for image- vs text-source answers inside one evidence order,
                       which removes the order offset that dominates the sign
    Rows whose answer is neither source are left out; n_attributable counts the rest.
    """
    dl = {(r["id"], r["family"], r["verdict"], r["k"], r["order"]): r["dl"] for r in rows if r["outcome"] == "dl" and not r.get("boundary_mismatch")}
    beh = [r for r in rows if r["outcome"] == "beh"]
    agree = n = 0
    by_order: Dict[str, Dict[str, List[float]]] = {o: {"image": [], "text": []} for o in ("image_first", "text_first")}
    for r in beh:
        src, _, _ = sc.behavioural_source(r["full_text"], r["regime"], r["y_image"], r["y_text"], parser=parser)
        d = dl.get((r["id"], r["family"], r["verdict"], r["k"], r["order"]))
        if src not in ("image", "text") or d is None:
            continue
        n += 1
        agree += (d > 0) == (src == "image")
        by_order[r["order"]][src].append(d)
    n_image = sum(len(v["image"]) for v in by_order.values())
    out: Dict[str, Any] = {
        "parser": parser,
        "n_behavioural_rows": len(beh),
        "n_attributable": n,
        "sign_agreement": agree / n if n else None,
        "majority_baseline": max(n_image, n - n_image) / n if n else None,
    }
    for o, v in by_order.items():
        out[f"auc_{o}"] = auc(v["image"], v["text"])
    return out


def behaviour_by_parser(rows: Sequence[Dict[str, Any]], ids: Sequence[str], reps: int, seed: int) -> Dict[str, Any]:
    """The secondary behavioural numbers under every Math parser, so none is hidden.

    ChartQA has one parser (strict answer-only), so it gets one entry.
    """
    regime = rows[0]["regime"]
    out: Dict[str, Any] = {}
    for parser in sc.MATH_PARSERS if regime == "math" else ("strict",):
        beh = behaviour_table(rows, parser=parser)
        entry: Dict[str, Any] = {"neither_rate": (sum(v["src"] not in ("image", "text") for v in beh.values()) / len(beh)) if beh else None}
        for fam in ("binding", "nonbinding"):
            delta = beh_diff(beh, ids, fam, "flip", "own")
            floor = beh_diff(beh, ids, fam, "para", "own")
            pair = beh_diff(beh, ids, fam, "para_flip", "para")
            e: Dict[str, Any] = {}
            if len(delta) > 1:
                ci = summarize_ci(list(delta.values()), reps, seed, 0.90)
                e["delta_flip_minus_own"] = ci["mean"]
                e["delta_ci90"] = ci["ci90"]
            e["matched_pair_para_flip_minus_para"] = mean(list(pair.values())) if pair else None
            e["floor_signed_mean"] = mean(list(floor.values())) if floor else None
            e["churn_any_change_own_vs_para"] = any_change_rate(beh, ids, fam, "own", "para")
            e["flip_rate_attributable_own_vs_para"] = change_rate(beh, ids, fam, "own", "para")
            e["attributable_pairs_own_vs_para"] = attributable_pairs(beh, ids, fam, "own", "para")
            entry[fam] = e
        out[parser] = entry
    return out


def qualify_reading(reading: str, n: int, minimum: int, edit_gate_ok: Optional[bool]) -> Tuple[str, List[str]]:
    """A reading is reported as one only when R5 and the §8 edit gate hold."""
    caveats = []
    if n < minimum:
        caveats.append(f"n = {n} is below the R5 minimum of {minimum}")
    if edit_gate_ok is False:
        caveats.append("the edit-gate pass rate is below 60% (prereg §8)")
    if not caveats:
        return reading, caveats
    return f"NOT A READING: {'; '.join(caveats)}. The decision table alone would say: {reading}", caveats


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


def manipulation_check(donor_rows: Sequence[Dict[str, Any]], reps: int = N_BOOT, seed: int = SEED) -> Dict[str, Any]:
    """Free generation, nothing forced: does the stated verdict predict the answer's source?

    Reported for the non-binding rows (family "donor") and the binding rows
    (family "free_binding"). If binding does not raise agreement, the binding wording failed.
    """
    out: Dict[str, Any] = {}
    for fam in ("donor", "free_binding"):
        n = stated = attributable = 0
        agrees: List[float] = []
        for r in donor_rows:
            if r.get("family") != fam or "full_text" not in r:
                continue
            n += 1
            verb, _ = sc.split_verbalization(r["full_text"])
            named = sc.stated_reliable_source(verb, regime=r.get("regime"))
            if named not in sc.SOURCES[r["regime"]]:
                continue
            stated += 1
            src, _, _ = sc.behavioural_source(
                r["full_text"], r["regime"], r["y_image"], r["y_text"], allow_math_fallback=True
            )
            if src in ("image", "text"):
                attributable += 1
                agrees.append(1.0 if src == side(named) else 0.0)
        entry: Dict[str, Any] = {
            "rows": n,
            "with_stated_verdict": stated,
            "attributable_answers": attributable,
            "answer_follows_stated_verdict": mean(agrees) if agrees else None,
        }
        if len(agrees) > 1:
            entry["answer_follows_stated_verdict_ci95"] = summarize_ci(agrees, reps, seed, 0.95)["ci95"]
        out[fam] = entry
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


def uncertainty_strata(
    dh: Dict[str, float],
    baseline: Dict[str, float],
    cde: Dict[str, float],
    radius: float = 0.5,
    reps: int = N_BOOT,
    seed: int = SEED,
) -> Dict[str, Any]:
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
    in_sum = summarize_ci(inside, reps, seed, 0.95) if len(inside) > 1 else {"n": len(inside), "mean": mean(inside) if inside else None}
    out_sum = summarize_ci(outside, reps, seed, 0.95) if len(outside) > 1 else {"n": len(outside), "mean": mean(outside) if outside else None}
    return {
        "n": len(ids),
        "balance_point": bp,
        "slope": fit[1],
        "inside": {"n": len(inside), "cde_mean": in_sum["mean"], "cde_ci95": in_sum.get("ci95")},
        "outside": {"n": len(outside), "cde_mean": out_sum["mean"], "cde_ci95": out_sum.get("ci95")},
    }


# ─── One model x regime ──────────────────────────────────────────────────────


def summarize_ci(values: Sequence[float], reps: int, seed: int, level: float) -> Dict[str, Any]:
    idx = resample_indices(len(values), reps, seed)
    lo, hi, _ = boot_ci(values, idx, level)
    return {"n": len(values), "mean": mean(values), f"ci{int(level * 100)}": [lo, hi]}


def _beh_summary(
    vals_by_id: Dict[str, float],
    idx: Sequence[Sequence[int]],
    draws: int,
    seed: int,
    include_tost: bool = False,
) -> Optional[Dict[str, Any]]:
    if len(vals_by_id) < 2:
        return None
    xs = [vals_by_id[i] for i in sorted(vals_by_id)]
    use_idx = idx if len(idx[0]) == len(xs) else resample_indices(len(xs), len(idx), seed)
    lo95, hi95, _ = boot_ci(xs, use_idx, 0.95)
    lo90, hi90, _ = boot_ci(xs, use_idx, 0.90)
    sf = sign_flip_test(xs, draws, seed)
    entry: Dict[str, Any] = {"n": len(xs), "mean": mean(xs), "ci95": [lo95, hi95], "ci90": [lo90, hi90], "p": sf["p"]}
    if include_tost:
        entry["tost_reading"] = tost_reading((lo90, hi90))
    return entry


def behaviour_benchmark(
    beh: Dict[Tuple, Dict[str, Any]], ids: Sequence[str], direction: Optional[str] = None
) -> Dict[str, float]:
    """Per item, the behavioural explicit-instruction benchmark B_beh (prereg §2.3), k = 1, m∅ prefill.

    image direction: P(Y=image | explicit_image) − P(Y=image | explicit_text)
    text direction:  P(Y=text | explicit_text) − P(Y=text | explicit_image)
    B_beh (direction=None) is their average, each averaged over the two orders. It is in the
    units of the behavioural Δ: how far naming a source in the instruction raises the share
    of answers that follow it. An answer matching neither source follows neither.

    It is NOT a ceiling. The m∅ prefill lets the model write its own verdict, which can
    contradict the explicit instruction, and on dev the verdict effect exceeded B_beh. It is
    a benchmark for scale and a manipulation check (its 95% CI must exclude 0); the decision
    rule reads Δ itself (decision_test).
    """
    out = {}
    for i in ids:
        vals = []
        for o in ("image_first", "text_first"):
            ei, et = beh.get((i, "explicit_image", "none", o)), beh.get((i, "explicit_text", "none", o))
            if ei and et:
                img = float(ei["src"] == "image") - float(et["src"] == "image")
                txt = float(et["src"] == "text") - float(ei["src"] == "text")
                vals.append({"image": img, "text": txt}.get(direction, (img + txt) / 2))
        if vals:
            out[i] = mean(vals)
    return out


behaviour_ceiling = behaviour_benchmark  # earlier name; the quantity is a benchmark, not a ceiling


def delta_reading(lo90: float, hi90: float, eps: float = EPSILON) -> str:
    """§2.3 reading of the behavioural Δ itself against the fixed margin ε."""
    if lo90 > eps:
        return "decision-relevant"
    if -eps < lo90 and hi90 < eps:
        return "equivalent to no effect"
    return "inconclusive"


def decision_test(effect: Dict[str, float], benchmark: Dict[str, float], reps: int, seed: int) -> Dict[str, Any]:
    """Math decision test on the behavioural Δ (prereg §2.3, revised 2026-11-14).

    decision-relevant        90% CI of Δ lies above +ε (one-sided α = 0.05 against Δ ≤ ε)
    equivalent to no effect  90% CI inside (−ε, +ε)  (TOST at α = 0.05)
    inconclusive             otherwise; with TOST power < 0.80 it is labelled as such and is
                             never read as evidence for either hypothesis
    undetermined             the benchmark B_beh's 95% CI includes 0 (explicit control failed)
    p_entered = min(1, 2·min(p_dec, p_eq)) goes into Holm, as for T2/T3 on Δℓ.
    ρ_beh = Δ / B_beh is reported as a descriptive ratio only; it can exceed 1.
    """
    out: Dict[str, Any] = {"n": len(effect), "epsilon": EPSILON}
    if len(effect) < 2:
        out["reading"] = "undetermined: fewer than two items"
        return out
    xs = [effect[i] for i in sorted(effect)]
    idx = resample_indices(len(xs), reps, seed)
    lo95, hi95, boots = boot_ci(xs, idx, 0.95)
    lo90, hi90, _ = boot_ci(xs, idx, 0.90)
    power = tost_power(sample_sd(xs), len(xs))
    out.update(effect=mean(xs), effect_ci95=[lo95, hi95], effect_ci90=[lo90, hi90], tost_power_at_this_noise=power)
    p_dec = (1 + sum(x <= EPSILON for x in boots)) / (len(boots) + 1)
    p_eq = (1 + max(sum(x >= EPSILON for x in boots), sum(x <= -EPSILON for x in boots))) / (len(boots) + 1)
    out.update(p_decision_relevant=p_dec, p_equivalent=p_eq, p_entered=min(1.0, 2 * min(p_dec, p_eq)))
    reading = delta_reading(lo90, hi90)
    bids, ve, vb = paired(effect, benchmark)
    if len(bids) >= 2:
        bidx = resample_indices(len(bids), reps, seed)
        b_lo, b_hi, _ = boot_ci(vb, bidx, 0.95)
        out.update(benchmark=mean(vb), benchmark_ci95=[b_lo, b_hi], benchmark_n=len(bids))
        if mean(vb) != 0:
            out["rho_beh_descriptive"] = mean(ve) / mean(vb)
        if b_lo <= 0 <= b_hi:
            reading = "undetermined: explicit-instruction control too weak"
    else:
        reading = "undetermined: no explicit-instruction benchmark"
    if reading == "inconclusive" and power < POWER_TARGET:
        reading = f"inconclusive (TOST power {power:.2f} < {POWER_TARGET:.2f}; not evidence for either hypothesis)"
    out["reading"] = reading
    return out


def math_reading(test_reading: str, floor_ok: bool, t1_significant: bool = False) -> str:
    """§2.3 Math reading from one decision_test, the wording-floor gate and T1_beh."""
    if test_reading.startswith("undetermined"):
        return "undetermined"
    if test_reading == "decision-relevant":
        if t1_significant:
            return "H1: the verdict decides, and binding strengthens it"
        return "H1: the verdict decides; no evidence that binding strengthens it"
    if test_reading == "equivalent to no effect":
        if not floor_ok:
            return "equivalence only; H0 not claimable (wording floor failed)"
        return "H0: saying is not choosing"
    return test_reading


def ratio_test(num: Dict[str, float], den: Dict[str, float], reps: int, seed: int) -> Dict[str, Any]:
    """ρ = mean(num)/mean(den) read like R4. Kept as a utility; no longer the Math decision rule."""
    ids, vn, vd = paired(num, den)
    out: Dict[str, Any] = {"n": len(ids)}
    if len(ids) < 2:
        out["reading"] = "undetermined: fewer than two items"
        return out
    idx = resample_indices(len(ids), reps, seed)
    c_lo, c_hi, _ = boot_ci(vd, idx, 0.95)
    e_lo, e_hi, _ = boot_ci(vn, idx, 0.95)
    out.update(effect=mean(vn), effect_ci95=[e_lo, e_hi], ceiling=mean(vd), ceiling_ci95=[c_lo, c_hi])
    if c_lo <= 0 <= c_hi or mean(vd) == 0:
        out["reading"] = rho_reading((c_lo, c_hi), None)
        return out
    boots = sorted(x for x in boot_ratio(vn, vd, idx) if x is not None)
    rho_ci = (percentile(boots, 0.05), percentile(boots, 0.95))
    p_dec = (1 + sum(x <= RHO_BOUND for x in boots)) / (len(boots) + 1)
    p_eq = (1 + max(sum(x >= RHO_BOUND for x in boots), sum(x <= -RHO_BOUND for x in boots))) / (len(boots) + 1)
    out.update(
        rho=mean(vn) / mean(vd),
        rho_ci90=list(rho_ci),
        reading=rho_reading((c_lo, c_hi), rho_ci),
        p_decision_relevant=p_dec,
        p_equivalent=p_eq,
        p_entered=min(1.0, 2 * min(p_dec, p_eq)),
    )
    return out


def coprimary_reading(flip_reading: str, pair_reading: str) -> str:
    """Math reading from the two co-primary contrasts (pre-freeze D2, prereg §2.3).

    A claim is made only when both contrasts give the same kind of reading. If they
    differ, both are reported and no combined claim is made.
    """
    kind = lambda r: "H1" if r.startswith("H1") else "H0" if r.startswith("H0") else r.split(" (")[0].split(":")[0]
    if kind(flip_reading) == kind(pair_reading):
        return flip_reading if kind(flip_reading) != "H1" else f"{flip_reading} (flip−own and para_flip−para agree)"
    return f"split, no combined claim: flip−own reads '{flip_reading}'; para_flip−para reads '{pair_reading}'"


def analyze_behaviour_primary(
    beh: Dict[Tuple, Dict[str, Any]],
    common: Sequence[str],
    reps: int,
    draws: int,
    seed: int,
    regime: str,
    floor_ok: Optional[Dict[str, bool]] = None,
) -> Optional[Dict[str, Any]]:
    """Behavioural contrasts at k = 1: primary in Math (D1), co-primary matched pair (D2).

    Decision rule (prereg §2.3, revised 2026-11-14): Δ itself against ε = 5 pp
    (decision_test), the wording-floor gate, and T1_beh. B_beh is a benchmark and
    manipulation check; ρ_beh is descriptive.
    Holm family (m = 4): T1_beh, T2_beh (flip, binding), T2_beh_pair (para_flip−para,
    binding), T3_beh (flip, non-binding).
    """
    if not beh or len(common) < 2:
        return None
    floor_ok = floor_ok or {"binding": True, "nonbinding": True}
    idx = resample_indices(len(common), reps, seed)
    out: Dict[str, Any] = {
        "is_primary_for_regime": regime == "math",
        "parser": HEADLINE_PARSER,
    }
    contrasts = (
        ("flip_minus_own", "flip", "own", True),
        ("matched_pair_para_flip_minus_para", "para_flip", "para", True),
        ("none_minus_own", "none", "own", False),
        ("flip_minus_none", "flip", "none", False),
        ("para_flip_minus_none", "para_flip", "none", False),
    )
    by_fam: Dict[str, Dict[str, Dict[str, float]]] = {}
    for fam in ("binding", "nonbinding"):
        f_out: Dict[str, Any] = {}
        by_fam[fam] = {}
        for key, a, b, do_tost in contrasts:
            d = beh_diff(beh, common, fam, a, b)
            by_fam[fam][key] = d
            if len(d) >= 2:
                # Recompute CI indices if any item is missing a behavioural pair
                ci_idx = idx if len(d) == len(common) else resample_indices(len(d), reps, seed)
                f_out[key] = _beh_summary(d, ci_idx, draws, seed, include_tost=do_tost)
        out[fam] = f_out

    for did_key, contrast_key, p_key in (
        ("T1_beh_did", "flip_minus_own", "T1_beh"),
        ("T1_beh_matched_pair_did", "matched_pair_para_flip_minus_para", "T1_beh_mp"),
    ):
        b_map, nb_map = by_fam["binding"].get(contrast_key, {}), by_fam["nonbinding"].get(contrast_key, {})
        pair_ids, vb, vn = paired(b_map, nb_map)
        if len(pair_ids) >= 2:
            did_vals = [b - n for b, n in zip(vb, vn)]
            did_idx = idx if len(pair_ids) == len(common) else resample_indices(len(pair_ids), reps, seed)
            lo95, hi95, _ = boot_ci(did_vals, did_idx, 0.95)
            sf = sign_flip_test(did_vals, draws, seed)
            out[did_key] = {"n": len(did_vals), "mean": sf["mean"], "ci95": [lo95, hi95], "p": sf["p"], "significant": sf["p"] <= ALPHA}

    # Decision rule (prereg §2.3): Δ itself against ε; B_beh is a benchmark, not a ceiling.
    bench = behaviour_benchmark(beh, common)
    out["benchmark"] = summarize_ci(list(bench.values()), reps, seed, 0.95) if len(bench) > 1 else {"n": len(bench)}
    for direction in ("image", "text"):
        bd = behaviour_benchmark(beh, common, direction)
        out[f"benchmark_{direction}"] = summarize_ci(list(bd.values()), reps, seed, 0.95) if len(bd) > 1 else {"n": len(bd)}
    out["ceiling"] = out["benchmark"]  # earlier key name
    tests = {
        "T2_beh": decision_test(by_fam["binding"].get("flip_minus_own", {}), bench, reps, seed),
        "T2_beh_pair": decision_test(by_fam["binding"].get("matched_pair_para_flip_minus_para", {}), bench, reps, seed),
        "T3_beh": decision_test(by_fam["nonbinding"].get("flip_minus_own", {}), bench, reps, seed),
    }
    out["decision_tests"] = tests
    # Descriptive, per direction of the reversed verdict (Grounding on Request reports image
    # requests weaker than text requests; an average over directions would hide that).
    directional: Dict[str, Any] = {}
    for fam in ("binding", "nonbinding"):
        for direction in ("image", "text"):
            d = beh_diff(beh, common, fam, "flip", "own", target_only=direction)
            entry: Dict[str, Any] = {"n": len(d)}
            if len(d) >= 2:
                entry.update(summarize_ci(list(d.values()), reps, seed, 0.95))
            bmean = out[f"benchmark_{direction}"].get("mean")
            entry["benchmark"] = bmean
            if entry.get("mean") is not None and bmean:
                entry["rho_beh_descriptive"] = entry["mean"] / bmean
            directional[f"{fam}_toward_{direction}"] = entry
    out["directional_flip_minus_own"] = directional
    pvals = {k: v["p_entered"] for k, v in tests.items() if "p_entered" in v}
    if "T1_beh_did" in out:
        pvals["T1_beh"] = out["T1_beh_did"]["p"]
    if pvals:
        adj = holm(pvals)
        out["holm_adjusted"] = adj
        if "T1_beh" in adj:
            out["T1_beh_did"]["holm_p"] = adj["T1_beh"]
            out["T1_beh_did"]["significant_after_holm"] = adj["T1_beh"] <= ALPHA
        for k, v in tests.items():
            if k in adj:
                v["holm_p"] = adj[k]
    t1_sig = bool(out.get("T1_beh_did", {}).get("significant"))
    out["reading_binding_flip"] = math_reading(tests["T2_beh"]["reading"], floor_ok["binding"], t1_sig)
    out["reading_binding_pair"] = math_reading(tests["T2_beh_pair"]["reading"], floor_ok["binding"], t1_sig)
    out["reading_binding"] = coprimary_reading(out["reading_binding_flip"], out["reading_binding_pair"])
    out["reading_nonbinding"] = math_reading(tests["T3_beh"]["reading"], floor_ok["nonbinding"], False)
    return out


def analyze_group(
    rows: Sequence[Dict[str, Any]],
    reps: int = N_BOOT,
    draws: int = N_PERM,
    seed: int = SEED,
    base_rows: Sequence[Dict[str, Any]] = (),
    donor_rows: Sequence[Dict[str, Any]] = (),
    gate_info: Optional[Dict[str, Any]] = None,
) -> Dict[str, Any]:
    regime = rows[0]["regime"]
    dl, dropped = index_dl(rows)
    ids = item_ids(rows)
    n_dl_rows = sum(1 for r in rows if r["outcome"] == "dl")
    res: Dict[str, Any] = {
        "model_id": rows[0]["model_id"],
        "regime": regime,
        "phase": rows[0].get("phase"),
        "confirmatory_role": confirmatory_role(rows[0]["model_id"], regime),
        "primary_outcome": "behaviour" if regime == "math" else "dl",
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
            p_dec = (1 + sum(x <= RHO_BOUND for x in boots)) / (len(boots) + 1)
            p_eq = (1 + max(sum(x >= RHO_BOUND for x in boots), sum(x <= -RHO_BOUND for x in boots))) / (len(boots) + 1)
            entry.update(
                rho=mean(vals) / mean(vc),
                rho_ci90=list(rho_ci),
                reading=rho_reading((c_lo95, c_hi95), rho_ci),
                p_decision_relevant=p_dec,
                p_equivalent=p_eq,
            )
            key = name.split("_")[0]
            # Each interval test has two one-sided readings. Entering the smaller p alone would
            # pick the favourable direction after the fact, so it is doubled first (capped at 1).
            pvals[key] = min(1.0, 2 * min(p_dec, p_eq))
        res[name] = entry
    res["holm_adjusted"] = holm(pvals)
    for key, name in (("T2", "T2_rho_binding"), ("T3", "T3_rho_nonbinding")):
        if key in res["holm_adjusted"]:
            res[name]["holm_p"] = res["holm_adjusted"][key]

    # Behavioural (primary in Math per D1, secondary in ChartQA): TOST, shifts, wording floor.
    mine = lambda rs: [r for r in rs if r.get("model_id") == res["model_id"] and r.get("regime") == regime]
    beh = behaviour_table(rows, parser=HEADLINE_PARSER)
    res["headline_parser"] = HEADLINE_PARSER
    replay_noise = donor_replay_noise(beh, mine(donor_rows), ids, HEADLINE_PARSER) if mine(donor_rows) else None
    res["replay_noise"] = replay_noise
    replay_flip_rate = replay_noise.get("replay_flip_rate") if replay_noise else None
    floor_ok = {"binding": True, "nonbinding": True}
    for fam in ("binding", "nonbinding"):
        delta = beh_diff(beh, ids, fam, "flip", "own")
        floor = beh_diff(beh, ids, fam, "para", "own")
        entry = {}
        if len(delta) > 1:
            ci = summarize_ci(list(delta.values()), reps, seed, 0.90)
            entry["delta_flip_minus_own"] = {**ci, "reading": tost_reading(tuple(ci["ci90"]))}
        for other in ("para", "flip"):  # §7.6: mean |ΔΔℓ| against the own verdict
            gap = per_item(dl, ids, abs_gap_fn(dl, fam, other, "own"))
            entry[f"mean_abs_dl_gap_own_vs_{other}"] = mean(list(gap.values())) if gap else None
        entry["change_rate_own_vs_para"] = change_rate(beh, ids, fam, "own", "para")
        entry["change_rate_own_vs_flip"] = change_rate(beh, ids, fam, "own", "flip")
        entry["neither_transition_rate_own_vs_para"] = neither_transition_rate(beh, ids, fam, "own", "para")
        entry["neither_transition_rate_own_vs_flip"] = neither_transition_rate(beh, ids, fam, "own", "flip")
        entry["neither_shift_para_minus_own"] = neither_shift(beh, ids, fam, "para", "own")
        entry["any_change_rate_own_vs_para"] = any_change_rate(beh, ids, fam, "own", "para")
        if len(floor) > 1:
            entry["wording_floor_para_minus_own"] = wording_floor(
                list(floor.values()),
                entry["change_rate_own_vs_para"],
                replay_flip_rate=replay_flip_rate,
                neither_shift=entry["neither_shift_para_minus_own"],
                any_change=entry["any_change_rate_own_vs_para"],
            )
            if not entry["wording_floor_para_minus_own"]["floor_ok"]:
                floor_ok[fam] = False
        res[f"behaviour_{fam}"] = entry
    # The wording-floor limit is fixed (revision 2026-11-14): replay noise is a diagnostic only.
    res["wording_floor_decision_basis"] = "fixed (signed mean, image<->text churn, neither shift)"
    beh_primary = analyze_behaviour_primary(beh, common, reps, draws, seed, regime, floor_ok=floor_ok)
    if beh_primary is not None:
        res["behaviour_primary"] = beh_primary
    tost = res.get("behaviour_binding", {}).get("delta_flip_minus_own", {}).get("reading", "not available")
    tost_nb = res.get("behaviour_nonbinding", {}).get("delta_flip_minus_own", {}).get("reading", "not available")
    res["wording_floor_ok_binding"] = floor_ok["binding"]
    res["wording_floor_ok_nonbinding"] = floor_ok["nonbinding"]
    # Readings use the unadjusted criteria, with Holm-adjusted values beside them (prereg §7.2).
    res["T1_did"]["holm_p"] = res["holm_adjusted"]["T1"]
    res["T1_did"]["significant"] = res["T1_did"]["p"] <= ALPHA
    res["T1_did"]["significant_after_holm"] = res["holm_adjusted"]["T1"] <= ALPHA
    res["reading_binding"] = combined_reading(res["T2_rho_binding"]["reading"], tost, floor_ok["binding"], res["T1_did"]["significant"])
    res["reading_nonbinding"] = combined_reading(res["T3_rho_nonbinding"]["reading"], tost_nb, floor_ok["nonbinding"], False)
    # reading_* are the bare decision-table labels. *_reported is what may be quoted: it
    # refuses to call an under-sized or gate-failing group a reading.
    edit_gate_ok = None
    if gate_info and gate_info.get("competent"):
        edit_gate_ok = gate_info.get("edit_gate_ok", gate_info["passed"] / gate_info["competent"] >= 0.60)
    res["edit_gate_ok"] = edit_gate_ok
    for key in ("reading_binding", "reading_nonbinding"):
        res[f"{key}_reported"], res["reading_caveats"] = qualify_reading(res[key], len(common), MIN_ITEMS[regime], edit_gate_ok)
    # The primary reading: behavioural in Math (D1, prereg §2.3), Δℓ in ChartQA (§2.2).
    # reading_binding/_nonbinding above stay the Δℓ table, which is secondary in Math.
    if res["primary_outcome"] == "behaviour" and beh_primary is not None:
        prim_b, prim_nb = beh_primary["reading_binding"], beh_primary["reading_nonbinding"]
    else:
        prim_b, prim_nb = res["reading_binding"], res["reading_nonbinding"]
    res["primary_reading_binding"], _ = qualify_reading(prim_b, len(common), MIN_ITEMS[regime], edit_gate_ok)
    res["primary_reading_nonbinding"], _ = qualify_reading(prim_nb, len(common), MIN_ITEMS[regime], edit_gate_ok)
    if res["confirmatory_role"] != "confirmatory":
        for key in ("primary_reading_binding", "primary_reading_nonbinding"):
            label = {"diagnostic_only": "DIAGNOSTIC MODEL", "exploratory": "EXPLORATORY REGIME"}.get(res["confirmatory_role"], res["confirmatory_role"])
            res[key] = f"{label}, not a confirmatory reading: {res[key]}"
    res["behaviour_by_parser"] = behaviour_by_parser(rows, ids, reps, seed)
    res["validity_dl_vs_behaviour"] = {
        p: validity_diagnostics(rows, p) for p in (sc.MATH_PARSERS if regime == "math" else ("strict",))
    }

    # Secondary: matched pair, decomposition, order, template/LOTO, saturation, neither-rate.
    sec: Dict[str, Any] = {}
    decomp: Dict[str, Any] = {}
    for fam in ("binding", "nonbinding"):
        mp = per_item(dl, ids, cde_fn(dl, fam, ("para_flip", "para")))
        if len(mp) > 1:
            sec[f"matched_pair_{fam}"] = summarize_ci(list(mp.values()), reps, seed, 0.95)
        for part, pair in (
            ("none_minus_own", ("none", "own")),
            ("flip_minus_none", ("flip", "none")),
            ("para_flip_minus_none", ("para_flip", "none")),
        ):
            dc = per_item(dl, common, cde_fn(dl, fam, pair))
            if len(dc) > 1:
                decomp[f"{fam}_{part}"] = summarize_ci(list(dc.values()), reps, seed, 0.95)
        for order in ("image_first", "text_first"):
            od = per_item(dl, ids, order_only(cde_fn(dl, fam), order))
            if len(od) > 1:
                sec[f"cde_{fam}_{order}"] = summarize_ci(list(od.values()), reps, seed, 0.95)
    if decomp:
        sec["cde_decomposition"] = decomp
    per_tpl: Dict[str, Any] = {}
    loto: Dict[str, Any] = {}
    for k_idx in range(1, 5):
        for fam in ("binding", "nonbinding"):
            base_fn = cde_fn(dl, fam)
            tk = per_item(dl, common, lambda i, k, o, fn=base_fn, target=k_idx: fn(i, k, o) if k == target else None)
            if len(tk) > 1:
                per_tpl[f"{fam}_k{k_idx}"] = summarize_ci(list(tk.values()), reps, seed, 0.95)
            lk = per_item(dl, common, lambda i, k, o, fn=base_fn, excl=k_idx: fn(i, k, o) if k != excl else None)
            if len(lk) > 1:
                loto[f"{fam}_excl_k{k_idx}"] = summarize_ci(list(lk.values()), reps, seed, 0.95)
    if per_tpl:
        sec["per_template"] = per_tpl
    if loto:
        sec["loto"] = loto
    base = per_item(dl, common, lambda i, k, o: _get(dl, i, "nonbinding", "none", k, o))
    if len(base) >= 6:
        ranked = sorted(common, key=lambda i: abs(base.get(i, 0.0)))
        third = len(ranked) // 3
        for t, chunk in enumerate((ranked[:third], ranked[third : 2 * third], ranked[2 * third :]), 1):
            vals = [d_bind[i] for i in chunk]
            if len(vals) > 1:
                sec[f"cde_binding_baseline_abs_dl_tertile{t}"] = summarize_ci(vals, reps, seed, 0.95)
            else:
                sec[f"cde_binding_baseline_abs_dl_tertile{t}"] = {"n": len(vals), "mean": mean(vals) if vals else None}
    beh_rows = [r for r in rows if r["outcome"] == "beh"]
    if beh_rows:
        sec["behaviour_neither_rate_headline"] = sum(follows_image(r, parser=HEADLINE_PARSER) is None for r in beh_rows) / len(beh_rows)
        sec["behaviour_neither_rate"] = sum(follows_image(r, allow_math_fallback=True) is None for r in beh_rows) / len(beh_rows)
        sec["behaviour_neither_rate_strict"] = sum(follows_image(r, allow_math_fallback=False) is None for r in beh_rows) / len(beh_rows)
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
    if mine(donor_rows):
        sec["manipulation_check"] = manipulation_check(mine(donor_rows), reps=reps, seed=seed)
    dh = relative_uncertainty(mine(base_rows))
    if dh:
        sec["relative_uncertainty_binding"] = uncertainty_strata(dh, base, d_bind, reps=reps, seed=seed)
    res["secondary"] = sec
    return res


def analyze_size_comparison(
    rows_3b: Sequence[Dict[str, Any]],
    rows_7b: Sequence[Dict[str, Any]],
    reps: int = N_BOOT,
    seed: int = SEED,
) -> Dict[str, Any]:
    """Secondary within-generation size contrast: Qwen2.5-VL-3B vs Qwen2.5-VL-7B (prereg §7.2).

    Reports difference in rho_bind on the intersection of the two models' competent & gated items,
    with a 95% item-bootstrap CI.
    """
    regime = rows_3b[0]["regime"]
    phase = rows_3b[0].get("phase")
    dl_3b, _ = index_dl(rows_3b)
    ids_3b = item_ids(rows_3b)
    d_bind_3b = per_item(dl_3b, ids_3b, cde_fn(dl_3b, "binding"))
    ceil_3b = per_item(dl_3b, ids_3b, ceil_fn(dl_3b))

    dl_7b, _ = index_dl(rows_7b)
    ids_7b = item_ids(rows_7b)
    d_bind_7b = per_item(dl_7b, ids_7b, cde_fn(dl_7b, "binding"))
    ceil_7b = per_item(dl_7b, ids_7b, ceil_fn(dl_7b))

    common = sorted(set(d_bind_3b) & set(ceil_3b) & set(d_bind_7b) & set(ceil_7b))
    res: Dict[str, Any] = {
        "regime": regime,
        "phase": phase,
        "model_3b": MODEL_3B,
        "model_7b": MODEL_7B,
        "n_intersection": len(common),
    }
    if len(common) < 2:
        res["error"] = "fewer than two items in intersection"
        return res

    vb_3b = [d_bind_3b[i] for i in common]
    vc_3b = [ceil_3b[i] for i in common]
    vb_7b = [d_bind_7b[i] for i in common]
    vc_7b = [ceil_7b[i] for i in common]

    mean_c3 = mean(vc_3b)
    mean_c7 = mean(vc_7b)
    rho_3b = mean(vb_3b) / mean_c3 if mean_c3 != 0 else None
    rho_7b = mean(vb_7b) / mean_c7 if mean_c7 != 0 else None
    delta_rho = (rho_7b - rho_3b) if (rho_3b is not None and rho_7b is not None) else None

    res["rho_3b_on_intersection"] = rho_3b
    res["rho_7b_on_intersection"] = rho_7b
    res["delta_rho_7b_minus_3b"] = delta_rho

    idx = resample_indices(len(common), reps, seed)
    boots = []
    for s in idx:
        d3 = mean([vc_3b[i] for i in s])
        d7 = mean([vc_7b[i] for i in s])
        if d3 != 0 and d7 != 0:
            r3 = mean([vb_3b[i] for i in s]) / d3
            r7 = mean([vb_7b[i] for i in s]) / d7
            boots.append(r7 - r3)

    if boots:
        boots.sort()
        res["delta_rho_ci95"] = [percentile(boots, 0.025), percentile(boots, 0.975)]
    else:
        res["delta_rho_ci95"] = None

    return res


# ─── Output ──────────────────────────────────────────────────────────────────

CSV_FIELDS = ["model_id", "regime", "item", "outcome", "family", "verdict", "k", "order", "D", "B", "O", "dl", "verdict_nll", "y_image", "named_source", "own_source"]


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
            fi = None if r["outcome"] == "dl" else follows_image(r, parser=HEADLINE_PARSER)
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
                    "verdict_nll": r.get("verdict_nll") if r["outcome"] == "dl" and r.get("verdict_nll") is not None else "",
                    "y_image": "" if fi is None else fi,
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


def provenance_check(run_paths: Sequence[str], rows: Sequence[Dict[str, Any]]) -> Dict[str, Any]:
    """Check duplicate row keys and inspect sibling .manifest.json files."""
    seen = set()
    duplicates = 0
    for r in rows:
        k = (r.get("model_id"), r.get("regime"), r.get("id"), r.get("family"), r.get("verdict"), r.get("k"), r.get("order"), r.get("outcome"))
        if k in seen:
            duplicates += 1
        seen.add(k)
    manifests: Dict[str, Any] = {}
    for p in run_paths:
        mp = p[:-len(".jsonl")] + ".manifest.json" if p.endswith(".jsonl") else p + ".manifest.json"
        if os.path.exists(mp):
            with open(mp, encoding="utf-8") as f:
                m = json.load(f)
            env = m.get("environment", {})
            manifests[os.path.basename(mp)] = {
                "resolved_model_commit": env.get("resolved_model_commit"),
                "peak_vram_gb": env.get("peak_vram_gb"),
                "written_at": m.get("written_at"),
                "n_items": m.get("n_items"),
            }
    return {"duplicate_rows": duplicates, "manifests": manifests}


def fake_backend_runs(run_paths: Sequence[str]) -> List[str]:
    """Run files whose manifest says the rows came from the fake 'echo' model."""
    fake = []
    for p in run_paths:
        mp = p[: -len(".jsonl")] + ".manifest.json" if p.endswith(".jsonl") else p + ".manifest.json"
        if os.path.exists(mp):
            with open(mp, encoding="utf-8") as f:
                if json.load(f).get("environment", {}).get("backend") == "echo":
                    fake.append(p)
    return fake


def three_way_intersections(groups: Dict[Tuple[str, str], List[Dict[str, Any]]]) -> Dict[str, Any]:
    """Compute 3-way (2B ∩ 3B ∩ 7B) item intersections per regime."""
    out: Dict[str, Any] = {}
    by_reg: Dict[str, Dict[str, set]] = defaultdict(dict)
    for (mid, reg), rs in groups.items():
        by_reg[reg][mid] = set(item_ids(rs))
    for reg, model_sets in sorted(by_reg.items()):
        if len(model_sets) >= 2:
            common = set.intersection(*model_sets.values())
            out[reg] = {"models": sorted(model_sets), "n_intersection": len(common), "per_model_counts": {m: len(s) for m, s in sorted(model_sets.items())}}
    return out


def render(
    results: Sequence[Dict[str, Any]],
    gates: Dict[str, Any],
    size_comparisons: Sequence[Dict[str, Any]] = (),
    intersections: Optional[Dict[str, Any]] = None,
    provenance: Optional[Dict[str, Any]] = None,
) -> str:
    lines = ["# v5 analysis", "", "Δℓ is image minus text. CDE is oriented toward the source the reversed verdict names.", ""]
    if any(r.get("phase") == "dev" for r in results):
        lines += ["**Dev data: for tuning and the freeze record only, not findings.**", ""]
    for r in results:
        lines += [f"## {r['model_id']} | {r['regime']} | {r['phase']}", ""]
        lines += [f"- Role: **{r.get('confirmatory_role', 'confirmatory')}**; primary outcome: **{r.get('primary_outcome', 'dl')}** (headline Math parser: `{r.get('headline_parser')}`)"]
        lines += [f"- Items: {r['n_items']}; analysed: {r.get('n_analysed')}; meets R5 minimum: {r.get('meets_min_items')}"]
        lines += [f"- Boundary mismatches: {r['boundary_mismatch_rows']} rows ({fmt(r['boundary_mismatch_share'])}; gate ≤ 0.01)"]
        if "error" in r:
            lines += [f"- **{r['error']}**", ""]
            continue
        bp_prim = r.get("behaviour_primary")
        if bp_prim:
            tag = "PRIMARY (D1)" if bp_prim.get("is_primary_for_regime") else "Secondary behavioural"
            lines += [f"- **{tag} — ΔP(follow reversed verdict) at k=1 (`{bp_prim.get('parser')}`):**"]
            t1b = bp_prim.get("T1_beh_did")
            if t1b:
                lines += [
                    f"  - T1_beh (flip−own DiD, bind−nonbind) = {fmt(t1b['mean'])} (95% CI {fmt(t1b['ci95'])}), "
                    f"p = {fmt(t1b['p'], 4)}, Holm p = {fmt(t1b.get('holm_p'), 4)}"
                ]
            t1mp = bp_prim.get("T1_beh_matched_pair_did")
            if t1mp:
                lines += [
                    f"  - Co-primary T1_beh matched-pair (para_flip−para DiD) = {fmt(t1mp['mean'])} (95% CI {fmt(t1mp['ci95'])}), p = {fmt(t1mp['p'], 4)}"
                ]
            ce = bp_prim.get("benchmark", {})
            if ce.get("mean") is not None:
                bi, bt = bp_prim.get("benchmark_image", {}), bp_prim.get("benchmark_text", {})
                lines += [
                    f"  - Explicit-instruction benchmark B_beh = {fmt(ce['mean'])} (95% CI {fmt(ce.get('ci95'))}); "
                    f"image direction {fmt(bi.get('mean'))} (95% CI {fmt(bi.get('ci95'))}), "
                    f"text direction {fmt(bt.get('mean'))} (95% CI {fmt(bt.get('ci95'))}). A benchmark, not a ceiling."
                ]
            for tname, te in bp_prim.get("decision_tests", {}).items():
                lines += [
                    f"  - **{tname}**: Δ = {fmt(te.get('effect'))} (90% CI {fmt(te.get('effect_ci90'))}) vs ε = {EPSILON}; "
                    f"reading: **{te['reading']}**; Holm p = {fmt(te.get('holm_p'), 4)}; "
                    f"TOST power {fmt(te.get('tost_power_at_this_noise'), 2)}; ρ_beh (descriptive) = {fmt(te.get('rho_beh_descriptive'))}"
                ]
            for dkey, de in bp_prim.get("directional_flip_minus_own", {}).items():
                lines += [
                    f"  - Directional (descriptive) {dkey}: Δ = {fmt(de.get('mean'))} (95% CI {fmt(de.get('ci95'))}, n = {de.get('n')}); "
                    f"benchmark {fmt(de.get('benchmark'))}; ρ_beh {fmt(de.get('rho_beh_descriptive'))}"
                ]
            for fam in ("binding", "nonbinding"):
                fe = bp_prim.get(fam, {})
                fo = fe.get("flip_minus_own")
                mp = fe.get("matched_pair_para_flip_minus_para")
                no = fe.get("none_minus_own")
                fn = fe.get("flip_minus_none")
                pn = fe.get("para_flip_minus_none")
                parts = []
                if fo:
                    parts.append(f"flip−own = {fmt(fo['mean'])} (95% CI {fmt(fo['ci95'])}, p = {fmt(fo['p'], 4)})")
                if mp:
                    parts.append(f"para_flip−para = {fmt(mp['mean'])} (95% CI {fmt(mp['ci95'])}, p = {fmt(mp['p'], 4)})")
                if no and fn and pn:
                    parts.append(f"decomp [none−own={fmt(no['mean'])}, flip−none={fmt(fn['mean'])}, para_flip−none={fmt(pn['mean'])}]")
                if parts:
                    lines += [f"  - {fam}: {'; '.join(parts)}"]
        if r.get("primary_reading_binding"):
            lines += [
                f"- **PRIMARY READING under binding: {r['primary_reading_binding']}**",
                f"- **PRIMARY READING under non-binding: {r['primary_reading_nonbinding']}**",
                f"- Wording-floor gate deciding the readings: {r.get('wording_floor_decision_basis')} (prereg §7.6)",
            ]
            if r.get("primary_outcome") == "behaviour":
                lines += ["- The Δℓ lines below are secondary/diagnostic in this regime (D1)."]
        rn = r.get("replay_noise")
        if rn:
            lines += [
                f"- Replay noise (donor vs nonbinding own): attributable flips = {fmt(rn.get('replay_flip_rate'))} "
                f"(n = {rn.get('attributable_pairs')}); any-change = {fmt(rn.get('replay_any_change_rate'))}; "
                "(diagnostic only; it does not move the wording-floor limit)"
            ]
        lines += [f"- Ceil_ℓ: {fmt(r['ceil']['mean'])}, 95% CI {fmt(r['ceil']['ci95'])}"]
        for wd in ("image", "text"):
            c = r.get(f"ceil_{wd}_direction")
            if c:
                lines += [f"  - {wd} direction vs non-binding: {fmt(c['mean'])}, 95% CI {fmt(c['ci95'])}"]
        t1 = r["T1_did"]
        lines += [
            f"- **T1** DiD = {fmt(t1['mean'])} (95% CI {fmt(t1['ci95'])}), sign-flip p = {fmt(t1['p'], 4)}, "
            f"Holm-adjusted p = {fmt(t1['holm_p'], 4)}: binding {'strengthens' if t1['significant'] else 'is not shown to strengthen'} the verdict's effect"
            f"{'' if t1['significant'] == t1['significant_after_holm'] else ' (this changes after Holm correction)'}"
        ]
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
                f"change rate own vs flip {fmt(b.get('change_rate_own_vs_flip'))}"
            ]
            if fl:
                lines += [
                    f"  - Wording floor (para vs own): signed mean {fmt(fl['signed_mean'])} (limit ±{EPSILON}), "
                    f"image<->text churn {fmt(fl['churn_rate'])} (limit {MAX_CHURN}), "
                    f"neither shift {fmt(fl.get('neither_shift'))} (limit ±{MAX_NEITHER_SHIFT}), "
                    f"gate: **{'pass' if fl['floor_ok'] else 'FAIL'}**; diagnostics: any-change churn "
                    f"{fmt(fl.get('any_change_rate_diagnostic'))}, replay flips {fmt(fl.get('replay_flip_rate_diagnostic'))}; "
                    f"TOST power at this noise {fmt(fl['tost_power_at_this_noise'], 2)}"
                ]
        lines += [
            f"- Δℓ decision table (§2.2), binding: {r.get('reading_binding_reported', r['reading_binding'])}",
            f"- Δℓ decision table (§2.2), non-binding: {r.get('reading_nonbinding_reported', r['reading_nonbinding'])}",
            "",
        ]
        bp = r.get("behaviour_by_parser")
        if bp:
            lines += [
                f"Behavioural numbers by answer parser (the lines above use `{r.get('headline_parser')}` per pre-freeze D3):",
                "",
                "| Parser | Neither | Δ bind [90% CI] | Δ non-bind | Matched pair bind | Floor signed mean bind | Any-change churn bind / non-bind | image↔text flips bind (of attributable pairs) | flips non-bind |",
                "|---|---:|---|---:|---:|---:|---|---|---|",
            ]
            for pname, e in bp.items():
                b, nb = e.get("binding", {}), e.get("nonbinding", {})
                lines += [
                    f"| {pname} | {fmt(e.get('neither_rate'))} | {fmt(b.get('delta_flip_minus_own'))} {fmt(b.get('delta_ci90'))} | {fmt(nb.get('delta_flip_minus_own'))} "
                    f"| {fmt(b.get('matched_pair_para_flip_minus_para'))} | {fmt(b.get('floor_signed_mean'))} "
                    f"| {fmt(b.get('churn_any_change_own_vs_para'))} / {fmt(nb.get('churn_any_change_own_vs_para'))} "
                    f"| {fmt(b.get('flip_rate_attributable_own_vs_para'))} (n = {b.get('attributable_pairs_own_vs_para')}) "
                    f"| {fmt(nb.get('flip_rate_attributable_own_vs_para'))} (n = {nb.get('attributable_pairs_own_vs_para')}) |"
                ]
            lines += [""]
        vd = r.get("validity_dl_vs_behaviour")
        if vd:
            lines += [
                "Does Δℓ track the answer? (behavioural rows with an attributable answer, same cell and template):",
                "",
                "| Parser | Attributable rows | Sign agreement | Majority-class baseline | AUC image-first | AUC text-first |",
                "|---|---:|---:|---:|---:|---:|",
            ]
            for pname, e in vd.items():
                lines += [
                    f"| {pname} | {e['n_attributable']}/{e['n_behavioural_rows']} | {fmt(e['sign_agreement'])} | {fmt(e['majority_baseline'])} "
                    f"| {fmt(e['auc_image_first'])} | {fmt(e['auc_text_first'])} |"
                ]
            lines += [""]
        lines += ["Secondary:", ""]
        for k, v in r["secondary"].items():
            lines += [f"- {k}: {fmt(v) if not isinstance(v, dict) else json.dumps({a: (round(b, 4) if isinstance(b, float) else b) for a, b in v.items()})}"]
        lines += [""]
    if size_comparisons:
        lines += ["## Size comparison: Qwen2.5-VL-3B vs. Qwen2.5-VL-7B (secondary, descriptive)", ""]
        for sc in size_comparisons:
            lines += [f"### Regime: {sc['regime']}", ""]
            lines += [f"- Common competent & gated items: N = {sc['n_intersection']}"]
            if "error" in sc:
                lines += [f"- **{sc['error']}**", ""]
                continue
            lines += [
                f"- ρ_bind (3B) on intersection: {fmt(sc['rho_3b_on_intersection'])}",
                f"- ρ_bind (7B) on intersection: {fmt(sc['rho_7b_on_intersection'])}",
                f"- Δρ (7B minus 3B): {fmt(sc['delta_rho_7b_minus_3b'])} (95% CI {fmt(sc['delta_rho_ci95'])})",
                "",
            ]
    if gates:
        lines += ["## Gate reports", ""]
        for name, g in gates.items():
            lines += [f"- {name}: " + json.dumps({k: v for k, v in g.items() if k != "passed_ids"})]
    if intersections:
        lines += ["", "## Multi-model item intersections", ""]
        for reg, info in intersections.items():
            lines += [f"- {reg}: intersection N = {info['n_intersection']} across {info['per_model_counts']}"]
    if provenance:
        lines += ["", "## Provenance", ""]
        lines += [f"- Duplicate rows: {provenance['duplicate_rows']}"]
        for mname, minfo in provenance["manifests"].items():
            lines += [f"- {mname}: {json.dumps(minfo)}"]
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
    parser.add_argument("--allow_dry_run", action="store_true", help="Accept rows from the fake 'echo' model (pipeline tests only)")
    args = parser.parse_args()

    fake = fake_backend_runs(list(args.runs) + list(args.base) + list(args.donor))
    if fake and not args.allow_dry_run:
        print(
            "Refusing to analyse fake-model ('echo' backend) output: " + ", ".join(os.path.basename(p) for p in fake)
            + ". These numbers mean nothing. Pass --allow_dry_run for a pipeline test.",
            file=sys.stderr,
        )
        return 2

    rows = load_rows(args.runs)
    if not rows:
        print("No transplant rows found.", file=sys.stderr)
        return 2
    groups: Dict[Tuple[str, str], List[Dict[str, Any]]] = defaultdict(list)
    for r in rows:
        groups[(r["model_id"], r["regime"])].append(r)
    base_rows, donor_rows = load_jsonl(args.base), load_jsonl(args.donor)
    gates = {}
    for p in args.gates:
        with open(p, encoding="utf-8") as f:
            gates[os.path.basename(p)] = json.load(f)
    results = [
        analyze_group(g, args.reps, args.draws, args.seed, base_rows, donor_rows, gate_info=gates.get(f"{g[0].get('run_tag')}.gates.json"))
        for _, g in sorted(groups.items())
    ]

    # Within-generation size comparison: 3B vs 7B per regime (prereg §7.2)
    size_comparisons = []
    regimes = sorted(set(r["regime"] for r in rows))
    for reg in regimes:
        g3 = groups.get((MODEL_3B, reg))
        g7 = groups.get((MODEL_7B, reg))
        if g3 and g7:
            size_comparisons.append(analyze_size_comparison(g3, g7, args.reps, args.seed))

    intersections = three_way_intersections(groups)
    provenance = provenance_check(args.runs, rows)

    os.makedirs(args.output_dir, exist_ok=True)
    with open(os.path.join(args.output_dir, "analysis_v5.json"), "w", encoding="utf-8") as f:
        json.dump(
            {
                "results": results,
                "size_comparisons": size_comparisons,
                "gates": gates,
                "intersections": intersections,
                "provenance": provenance,
            },
            f,
            indent=2,
        )
    with open(os.path.join(args.output_dir, "analysis_v5.md"), "w", encoding="utf-8") as f:
        f.write(render(results, gates, size_comparisons, intersections, provenance))
    n = export_long(rows, os.path.join(args.output_dir, "long_v5.csv"))
    with open(os.path.join(args.output_dir, "analyze_v5_lme4.R"), "w", encoding="utf-8") as f:
        f.write(R_SCRIPT)
    print(f"Wrote analysis_v5.json, analysis_v5.md, long_v5.csv ({n} rows) and analyze_v5_lme4.R to {args.output_dir}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
