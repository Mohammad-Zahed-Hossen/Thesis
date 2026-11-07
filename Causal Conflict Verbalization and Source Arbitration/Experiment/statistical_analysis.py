#!/usr/bin/env python3
"""Paired statistics for the v3 pilot results. Standard library only.

Rewritten after the 2026-11-06 audit. What changed and why:

  * Removed Fisher and Pearson tests. They assume independent observations, but every
    item appears in both arms.
  * Removed the scipy branch. The fallback had an absolute 1e-12 tolerance that returned
    p = 3.81e-12 where the exact value is about 1e-322, so the reported p depended on
    whether scipy was installed. All p-values now use exact integer arithmetic.
  * Report p-values as log10, because they underflow a float.
  * Removed fixed verdict strings ("causally", "Very Large", "p < 0.0001"). The report
    now prints only numbers computed from the data.
  * Intervals resample problems, because each problem appears in two items.

The labels analysed here are the stored v3 labels. They are unvalidated heuristics; see
`reanalyze_v3.py` for re-scoring. None of these tests can separate the effect of the
instruction from the effect of the verbalization.

Usage:
    python statistical_analysis.py --results_file "results_v3/full_experiment_results v3.0.json" --output_dir results_v3/stats_v3_paired
"""
from __future__ import annotations

import argparse
import json
import math
import os
import random
import sys
from collections import Counter
from typing import Any, Dict, List, Sequence, Tuple

ARMS = [
    "arm1_direct",
    "arm2_placebo",
    "arm3_conflict",
    "arm4_prefill_contradict",
    "arm4_prefill_agree",
]
LABELED_ARMS = ARMS[:3]
STATES = ["follows_image_problem", "follows_text_problem", "abstains", "ambiguous"]


# ─── Exact tests ─────────────────────────────────────────────────────────────


def log10_ratio(numerator: int, denominator: int) -> float:
    """log10(numerator / denominator) for arbitrarily large positive integers."""
    if numerator <= 0:
        return -math.inf
    return math.log10(numerator) - math.log10(denominator)


def mcnemar_exact_log10p(b: int, c: int) -> float:
    """Two-sided exact McNemar test as log10(p), capped at p = 1.

    Under H0 the discordant pairs split as Binomial(b + c, 1/2).
    """
    n = b + c
    if n == 0:
        return 0.0
    tail = sum(math.comb(n, k) for k in range(min(b, c) + 1))
    return min(0.0, log10_ratio(2 * tail, 2**n))


def format_log10p(log10p: float) -> str:
    """Readable p-value that does not underflow."""
    if log10p == 0.0:
        return "1"
    if log10p > -3:
        return f"{10 ** log10p:.4f}"
    exponent = math.floor(log10p)
    return f"{10 ** (log10p - exponent):.2f}e{exponent}"


def paired_odds_ratio(b: int, c: int) -> Tuple[float, float, float]:
    """b/c with a 95% Wald interval on the log scale; 0.5 added if a cell is empty."""
    if b == 0 or c == 0:
        b, c = b + 0.5, c + 0.5
    ratio = b / c
    se = math.sqrt(1 / b + 1 / c)
    return ratio, math.exp(math.log(ratio) - 1.96 * se), math.exp(math.log(ratio) + 1.96 * se)


def cohens_h(p1: float, p2: float) -> float:
    return 2.0 * (math.asin(math.sqrt(p1)) - math.asin(math.sqrt(p2)))


def holm_adjust_log10(log10ps: Sequence[float]) -> List[float]:
    """Holm step-down adjustment, on log10 p-values, returned in input order."""
    m = len(log10ps)
    order = sorted(range(m), key=lambda i: log10ps[i])
    adjusted = [0.0] * m
    running = -math.inf
    for rank, i in enumerate(order):
        value = min(0.0, log10ps[i] + math.log10(m - rank))
        running = max(running, value)
        adjusted[i] = running
    return adjusted


# ─── Dependence-aware interval ───────────────────────────────────────────────


def pigeonhole_ci(
    values: Sequence[float],
    cluster_a: Sequence[str],
    cluster_b: Sequence[str],
    reps: int = 2000,
    seed: int = 20261106,
) -> Tuple[float, float]:
    """95% percentile interval for a mean under two-way clustering.

    Each replicate draws multinomial weights over problems. An item's weight is the
    product of the weights of its image problem and its text problem.
    """
    keys = sorted(set(cluster_a) | set(cluster_b))
    index = {k: i for i, k in enumerate(keys)}
    ia = [index[k] for k in cluster_a]
    ib = [index[k] for k in cluster_b]
    rng = random.Random(seed)
    k = len(keys)
    estimates = []
    for _ in range(reps):
        w = [0] * k
        for j in rng.choices(range(k), k=k):
            w[j] += 1
        num = den = 0.0
        for v, a, b in zip(values, ia, ib):
            weight = w[a] * w[b]
            if weight:
                num += weight * v
                den += weight
        if den:
            estimates.append(num / den)
    estimates.sort()
    return estimates[int(0.025 * len(estimates))], estimates[int(0.975 * len(estimates))]


# ─── Report ──────────────────────────────────────────────────────────────────


def validate(data: Any) -> None:
    if not isinstance(data, list) or not data:
        raise ValueError("results file must contain a non-empty list of items")
    for item in data:
        missing = [a for a in ARMS if a not in item.get("arms", {})]
        if missing:
            raise ValueError(f"item {item.get('id')} is missing arms {missing}")


def analyze_experiment(data: List[Dict[str, Any]], reps: int = 2000) -> Dict[str, Any]:
    validate(data)
    n = len(data)
    choice = {a: [d["arms"][a]["choice"] for d in data] for a in LABELED_ARMS}
    results: Dict[str, Any] = {"n": n, "arms": {}}

    for arm in ARMS:
        rows = [d["arms"][arm] for d in data]
        results["arms"][arm] = {
            "choices": dict(Counter(r.get("choice", "n/a") for r in rows)),
            "exact_image": sum(r["ans"] == d["image_answer"] for r, d in zip(rows, data)),
            "exact_text": sum(r["ans"] == d["text_answer"] for r, d in zip(rows, data)),
            "at_token_cap": sum(bool(r.get("truncated")) for r in rows),
            "tokens_mean": sum(r["tokens"] for r in rows) / n,
        }

    v2 = [c == "follows_image_problem" for c in choice["arm2_placebo"]]
    v3 = [c == "follows_image_problem" for c in choice["arm3_conflict"]]
    a = sum(x and y for x, y in zip(v2, v3))
    b = sum(x and not y for x, y in zip(v2, v3))
    c = sum(y and not x for x, y in zip(v2, v3))
    d_ = n - a - b - c
    p2, p3 = (a + b) / n, (a + c) / n
    ci = pigeonhole_ci(
        [float(x) - float(y) for x, y in zip(v2, v3)],
        [d["image_question"] for d in data],
        [d["text_question"] for d in data],
        reps=reps,
    )
    ratio, or_low, or_high = paired_odds_ratio(b, c)
    results["primary"] = {
        "table": {"both_visual": a, "arm2_only": b, "arm3_only": c, "neither": d_},
        "arm2_visual": a + b,
        "arm3_visual": a + c,
        "difference_arm2_minus_arm3": p2 - p3,
        "difference_ci95_problem_clustered": ci,
        "mcnemar_exact_log10p": mcnemar_exact_log10p(b, c),
        "paired_odds_ratio": ratio,
        "paired_odds_ratio_ci95": (or_low, or_high),
        "cohens_h": cohens_h(p2, p3),
    }

    results["migration"] = {
        s1: {
            s2: sum(x == s1 and y == s2 for x, y in zip(choice["arm2_placebo"], choice["arm3_conflict"]))
            for s2 in STATES
        }
        for s1 in STATES
    }

    a4a = [d["arms"]["arm4_prefill_contradict"]["ans"] for d in data]
    a4b = [d["arms"]["arm4_prefill_agree"]["ans"] for d in data]
    ta = [x == d["text_answer"] for x, d in zip(a4a, data)]
    tb = [x == d["text_answer"] for x, d in zip(a4b, data)]
    ia = [x == d["image_answer"] for x, d in zip(a4a, data)]
    ib = [x == d["image_answer"] for x, d in zip(a4b, data)]
    tb_only = sum(y and not x for x, y in zip(ta, tb))
    ta_only = sum(x and not y for x, y in zip(ta, tb))
    ia_only = sum(x and not y for x, y in zip(ia, ib))
    ib_only = sum(y and not x for x, y in zip(ia, ib))
    results["arm4"] = {
        "identical_answers": sum(x == y and x is not None for x, y in zip(a4a, a4b)),
        "text_match_4b_only": tb_only,
        "text_match_4a_only": ta_only,
        "text_mcnemar_exact_log10p": mcnemar_exact_log10p(tb_only, ta_only),
        "image_match_4a_only": ia_only,
        "image_match_4b_only": ib_only,
        "image_mcnemar_exact_log10p": mcnemar_exact_log10p(ia_only, ib_only),
    }
    return results


def render_markdown(r: Dict[str, Any]) -> str:
    n, p = r["n"], r["primary"]
    pct = lambda x: f"{100 * x / n:.1f}%"
    t = p["table"]
    lines = [
        "# Paired analysis of stored v3 labels",
        "",
        f"N = {n}. Labels are the stored v3 heuristics, not validated against human coding.",
        "This compares two instructions; it does not isolate the effect of the verbalization.",
        "",
        "## Arm summary",
        "",
        "| Arm | Image label | Text label | Abstain label | Ambiguous | Exact image | Exact text | At token cap | Mean tokens |",
        "|---|---:|---:|---:|---:|---:|---:|---:|---:|",
    ]
    for arm in ARMS:
        s, ch = r["arms"][arm], r["arms"][arm]["choices"]
        lines.append(
            f"| {arm} | {ch.get('follows_image_problem', 0)} | {ch.get('follows_text_problem', 0)} "
            f"| {ch.get('abstains', 0)} | {ch.get('ambiguous', 0)} "
            f"| {s['exact_image']} ({pct(s['exact_image'])}) | {s['exact_text']} ({pct(s['exact_text'])}) "
            f"| {s['at_token_cap']} ({pct(s['at_token_cap'])}) | {s['tokens_mean']:.1f} |"
        )
    lo, hi = p["difference_ci95_problem_clustered"]
    ol, oh = p["paired_odds_ratio_ci95"]
    lines += [
        "",
        "## Arm 2 vs Arm 3: image label",
        "",
        "| | Arm 3 image | Arm 3 other |",
        "|---|---:|---:|",
        f"| Arm 2 image | {t['both_visual']} | {t['arm2_only']} |",
        f"| Arm 2 other | {t['arm3_only']} | {t['neither']} |",
        "",
        f"- Arm 2: {p['arm2_visual']} ({pct(p['arm2_visual'])}); Arm 3: {p['arm3_visual']} ({pct(p['arm3_visual'])})",
        f"- Difference, Arm 2 minus Arm 3: {100 * p['difference_arm2_minus_arm3']:.1f} pp "
        f"(problem-clustered 95% interval {100 * lo:.1f} to {100 * hi:.1f})",
        f"- Exact McNemar p = {format_log10p(p['mcnemar_exact_log10p'])}",
        f"- Paired odds ratio = {p['paired_odds_ratio']:.2f} (95% interval {ol:.2f} to {oh:.2f})",
        f"- Cohen's h = {p['cohens_h']:.2f}",
        "",
        "## Label migration, Arm 2 (rows) to Arm 3 (columns)",
        "",
        "| | " + " | ".join(STATES) + " |",
        "|---|" + "---:|" * len(STATES),
    ]
    for s1 in STATES:
        lines.append(f"| {s1} | " + " | ".join(str(r["migration"][s1][s2]) for s2 in STATES) + " |")
    a4 = r["arm4"]
    lines += [
        "",
        "## Arm 4 prefills",
        "",
        "Arm 4a and 4b differ in rationale and named source together, so these contrasts can't separate the two.",
        "",
        f"- Identical answers: {a4['identical_answers']} ({pct(a4['identical_answers'])})",
        f"- Text match, 4b only vs 4a only: {a4['text_match_4b_only']} vs {a4['text_match_4a_only']} "
        f"(exact McNemar p = {format_log10p(a4['text_mcnemar_exact_log10p'])})",
        f"- Image match, 4a only vs 4b only: {a4['image_match_4a_only']} vs {a4['image_match_4b_only']} "
        f"(exact McNemar p = {format_log10p(a4['image_mcnemar_exact_log10p'])})",
        "",
    ]
    return "\n".join(lines)


def render_latex(r: Dict[str, Any]) -> str:
    n, p = r["n"], r["primary"]
    lo, hi = p["difference_ci95_problem_clustered"]
    rows = []
    names = {"arm1_direct": "Arm 1: Direct", "arm2_placebo": "Arm 2: Description", "arm3_conflict": "Arm 3: Conflict"}
    for arm in LABELED_ARMS:
        ch = r["arms"][arm]["choices"]
        cells = " & ".join(f"{ch.get(s, 0)} ({100 * ch.get(s, 0) / n:.1f}\\%)" for s in STATES)
        rows.append(f"{names[arm]} & {cells} \\\\")
    body = "\n".join(rows)
    return (
        "\\begin{table}[t]\n\\centering\n\\small\n"
        f"\\caption{{Stored v3 labels by instruction ($N={n}$). Labels are unvalidated heuristics.}}\n"
        "\\label{tab:v3_labels}\n\\begin{tabular}{lcccc}\n\\hline\n"
        "Condition & Image & Text & Abstain & Ambiguous \\\\\n\\hline\n"
        f"{body}\n\\hline\n"
        f"\\multicolumn{{5}}{{l}}{{Arm 2 minus Arm 3, image label: {100 * p['difference_arm2_minus_arm3']:.1f} pp "
        f"(problem-clustered 95\\% interval {100 * lo:.1f} to {100 * hi:.1f})}} \\\\\n"
        f"\\multicolumn{{5}}{{l}}{{Exact McNemar $p = {format_log10p(p['mcnemar_exact_log10p'])}$; "
        f"discordant pairs {p['table']['arm2_only']} and {p['table']['arm3_only']}}} \\\\\n"
        "\\hline\n\\end{tabular}\n\\end{table}\n"
    )


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("--results_file", required=True)
    parser.add_argument("--output_dir", required=True, help="Must be a new folder or one you mean to overwrite")
    parser.add_argument("--bootstrap_reps", type=int, default=2000)
    args = parser.parse_args()

    if not os.path.exists(args.results_file):
        print(f"Error: results file not found: {args.results_file}", file=sys.stderr)
        return 2
    with open(args.results_file, encoding="utf-8") as f:
        data = json.load(f)
    try:
        results = analyze_experiment(data, reps=args.bootstrap_reps)
    except ValueError as exc:
        print(f"Error: {exc}", file=sys.stderr)
        return 2

    os.makedirs(args.output_dir, exist_ok=True)
    markdown = render_markdown(results)
    with open(os.path.join(args.output_dir, "paired_report.md"), "w", encoding="utf-8") as f:
        f.write(markdown)
    with open(os.path.join(args.output_dir, "paired_table.tex"), "w", encoding="utf-8") as f:
        f.write(render_latex(results))
    with open(os.path.join(args.output_dir, "paired_results.json"), "w", encoding="utf-8") as f:
        json.dump(results, f, indent=2)
    print(markdown)
    return 0


if __name__ == "__main__":
    sys.exit(main())
