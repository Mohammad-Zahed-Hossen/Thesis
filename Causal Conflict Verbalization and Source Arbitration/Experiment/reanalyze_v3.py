#!/usr/bin/env python3
"""Re-score the stored v3 outputs with score_v4 and print the audit tables.

Reads only the stored outputs and never touches a model. Safe to run locally.

Usage:
    python reanalyze_v3.py --output_dir results_v3/reanalysis_v3
    python reanalyze_v3.py --check     # exit 1 if the stored data stop matching the audit
"""
from __future__ import annotations

import argparse
import json
import math
import os
import random
import re
import sys
from collections import Counter
from typing import Any, Dict, List

import score_v4 as sc
from statistical_analysis import format_log10p, mcnemar_exact_log10p, pigeonhole_ci

HERE = os.path.dirname(os.path.abspath(__file__))
DEFAULT_RESULTS = os.path.join(HERE, "results_v3", "full_experiment_results v3.0.json")
ARMS = ["arm1_direct", "arm2_placebo", "arm3_conflict", "arm4_prefill_contradict", "arm4_prefill_agree"]
SOLVE_ARMS = ARMS[:3]

# Values recomputed on 2026-11-06 from the stored file. --check fails if they drift.
EXPECTED = {
    "n": 1619,
    "n_distinct_answers": 1600,
    "legacy_image_label": {"arm1_direct": 223, "arm2_placebo": 1449, "arm3_conflict": 417},
    "legacy_abstain_label": {"arm1_direct": 0, "arm2_placebo": 4, "arm3_conflict": 221},
    "at_token_cap": {"arm1_direct": 1588, "arm2_placebo": 608, "arm3_conflict": 716},
}


def load(path: str) -> List[Dict[str, Any]]:
    with open(path, encoding="utf-8") as f:
        return json.load(f)


def compute(data: List[Dict[str, Any]], reps: int) -> Dict[str, Any]:
    n = len(data)
    scored = {
        a: [
            sc.score_output(d["arms"][a]["text"], d["image_question"], d["text_question"], d["image_answer"], d["text_answer"])
            for d in data
        ]
        for a in ARMS
    }
    distinct = [i for i, d in enumerate(data) if not sc.numeric_equal(d["image_answer"], d["text_answer"])]
    out: Dict[str, Any] = {"n": n, "n_distinct_answers": len(distinct), "arms": {}}

    for a in ARMS:
        rows = [d["arms"][a] for d in data]
        tokens = sorted(r["tokens"] for r in rows)
        out["arms"][a] = {
            "legacy_labels": dict(Counter(r.get("choice", "n/a") for r in rows)),
            "at_token_cap": sum(bool(r["truncated"]) for r in rows),
            "tokens": {"mean": sum(tokens) / n, "median": tokens[n // 2], "p10": tokens[n // 10], "p90": tokens[9 * n // 10]},
            "answer_method": dict(Counter(s["answer_method"] for s in scored[a])),
            "answer_source_distinct": dict(Counter(scored[a][i]["answer_source"] for i in distinct)),
            "attempt": dict(Counter(s["attempt"] for s in scored[a])),
            "refusal": sum(s["refusal"] for s in scored[a]),
            "verdict": dict(Counter(s["verdict"] for s in scored[a])),
            "stated_reliable": dict(Counter(s["stated_reliable"] for s in scored[a])),
        }

    # Paired contrasts on numeric exact match, the outcome that needs no classifier.
    image_keys = [data[i]["image_question"] for i in distinct]
    text_keys = [data[i]["text_question"] for i in distinct]
    contrasts = {}
    for name, x, y in (
        ("arm2_vs_arm1", "arm2_placebo", "arm1_direct"),
        ("arm3_vs_arm1", "arm3_conflict", "arm1_direct"),
        ("arm3_vs_arm2", "arm3_conflict", "arm2_placebo"),
    ):
        for source in ("image", "text"):
            xs = [scored[x][i]["answer_source"] == source for i in distinct]
            ys = [scored[y][i]["answer_source"] == source for i in distinct]
            b = sum(u and not v for u, v in zip(xs, ys))
            c = sum(v and not u for u, v in zip(xs, ys))
            contrasts[f"{name}:{source}"] = {
                "first_only": b,
                "second_only": c,
                "difference": (sum(xs) - sum(ys)) / len(distinct),
                "ci95": pigeonhole_ci([float(u) - float(v) for u, v in zip(xs, ys)], image_keys, text_keys, reps=reps),
                "mcnemar_exact_log10p": mcnemar_exact_log10p(b, c),
            }
    out["contrasts"] = contrasts

    # Sensitivity: does the arm contrast survive within outputs that finished?
    finished = [i for i in distinct if not data[i]["arms"]["arm2_placebo"]["truncated"] and not data[i]["arms"]["arm3_conflict"]["truncated"]]
    out["finished_both"] = {
        "n": len(finished),
        **{
            f"{a}:{s}": sum(scored[a][i]["answer_source"] == s for i in finished) / max(len(finished), 1)
            for a in ("arm2_placebo", "arm3_conflict")
            for s in ("image", "text")
        },
    }

    # Sensitivity: token-length bins.
    bins = [(0, 80), (80, 120), (120, 160), (160, 199), (199, 10**6)]
    out["token_bins"] = {}
    for a in ("arm2_placebo", "arm3_conflict"):
        rows = {}
        for lo, hi in bins:
            idx = [i for i in distinct if lo <= data[i]["arms"][a]["tokens"] < hi]
            if idx:
                rows[f"{lo}-{hi}"] = {
                    "n": len(idx),
                    "image": sum(scored[a][i]["answer_source"] == "image" for i in idx) / len(idx),
                    "text": sum(scored[a][i]["answer_source"] == "text" for i in idx) / len(idx),
                    "attempt_image": sum(scored[a][i]["attempt"] == "image" for i in idx) / len(idx),
                }
        out["token_bins"][a] = rows

    # Dataset strata.
    out["by_source"] = {}
    for prefix in ("gsm8k", "svamp"):
        idx = [i for i in distinct if data[i]["id"].startswith(prefix)]
        out["by_source"][prefix] = {
            "n": len(idx),
            **{
                f"{a}:{s}": sum(scored[a][i]["answer_source"] == s for i in idx) / max(len(idx), 1)
                for a in ARMS
                for s in ("image", "text")
            },
        }

    # Chance baseline: match against another item's image answer.
    rng = random.Random(20261106)
    out["chance_match"] = {}
    golds = [data[i]["image_answer"] for i in distinct]
    for a in ARMS:
        total = 0.0
        for _ in range(20):
            shuffled = golds[:]
            rng.shuffle(shuffled)
            total += sum(sc.numeric_equal(scored[a][i]["answer"], g) for i, g in zip(distinct, shuffled)) / len(distinct)
        out["chance_match"][a] = total / 20

    # Stated reliability against behaviour. Post-treatment and observational.
    table = Counter((scored["arm3_conflict"][i]["stated_reliable"], scored["arm3_conflict"][i]["answer_source"]) for i in distinct)
    out["arm3_stated_reliable_by_answer"] = {f"{k[0]}|{k[1]}": v for k, v in sorted(table.items())}

    # Same problem across roles: difficulty shared between arms.
    by_image = {d["image_question"]: d for d in data}
    by_text = {d["text_question"]: d for d in data}
    role = Counter()
    for q in by_image:
        solved_as_image = sc.numeric_equal(by_image[q]["arms"]["arm2_placebo"]["ans"], by_image[q]["image_answer"])
        solved_as_text = sc.numeric_equal(by_text[q]["arms"]["arm3_conflict"]["ans"], by_text[q]["text_answer"])
        role[(solved_as_image, solved_as_text)] += 1
    n11, n10, n01, n00 = role[(True, True)], role[(True, False)], role[(False, True)], role[(False, False)]
    denom = math.sqrt((n11 + n10) * (n01 + n00) * (n11 + n01) * (n10 + n00)) or 1.0
    out["role_solved_phi"] = (n11 * n00 - n10 * n01) / denom
    return out


def check(data: List[Dict[str, Any]], out: Dict[str, Any]) -> List[str]:
    errors = []
    if out["n"] != EXPECTED["n"]:
        errors.append(f"n: {out['n']} != {EXPECTED['n']}")
    if out["n_distinct_answers"] != EXPECTED["n_distinct_answers"]:
        errors.append(f"distinct-answer items: {out['n_distinct_answers']} != {EXPECTED['n_distinct_answers']}")
    for a in SOLVE_ARMS:
        legacy = out["arms"][a]["legacy_labels"]
        if legacy.get("follows_image_problem", 0) != EXPECTED["legacy_image_label"][a]:
            errors.append(f"{a} image label: {legacy.get('follows_image_problem', 0)} != {EXPECTED['legacy_image_label'][a]}")
        if legacy.get("abstains", 0) != EXPECTED["legacy_abstain_label"][a]:
            errors.append(f"{a} abstain label: {legacy.get('abstains', 0)} != {EXPECTED['legacy_abstain_label'][a]}")
        if out["arms"][a]["at_token_cap"] != EXPECTED["at_token_cap"][a]:
            errors.append(f"{a} at cap: {out['arms'][a]['at_token_cap']} != {EXPECTED['at_token_cap'][a]}")
    return errors


def render(out: Dict[str, Any]) -> str:
    n, m = out["n"], out["n_distinct_answers"]
    pct = lambda v, t=m: f"{100 * v / t:.1f}%"
    lines = [
        "# Re-analysis of the v3 outputs with score_v4",
        "",
        f"N = {n}; {m} items have distinct answers and are used for answer-source rates.",
        "score_v4 labels are heuristics until validated against human coding.",
        "",
        "## Answer source (numeric exact match, distinct-answer items)",
        "",
        "| Arm | Image | Text | Neither | Chance match | At token cap | Fallback extraction |",
        "|---|---:|---:|---:|---:|---:|---:|",
    ]
    for a in ARMS:
        s = out["arms"][a]
        src = s["answer_source_distinct"]
        fb = s["answer_method"].get("fallback_last_number", 0)
        lines.append(
            f"| {a} | {pct(src.get('image', 0))} | {pct(src.get('text', 0))} | {pct(src.get('neither', 0))} "
            f"| {100 * out['chance_match'][a]:.1f}% | {pct(s['at_token_cap'], n)} | {pct(fb, n)} |"
        )
    lines += [
        "",
        "## Other labels (all items)",
        "",
        "| Arm | Attempt image | Attempt text | Attempt unknown | Refusal | Tokens mean / median / p10 |",
        "|---|---:|---:|---:|---:|---:|",
    ]
    for a in SOLVE_ARMS:
        s = out["arms"][a]
        t = s["tokens"]
        at = s["attempt"]
        lines.append(
            f"| {a} | {pct(at.get('image', 0), n)} | {pct(at.get('text', 0), n)} | {pct(at.get('unknown', 0), n)} "
            f"| {s['refusal']} ({pct(s['refusal'], n)}) | {t['mean']:.1f} / {t['median']} / {t['p10']} |"
        )
    v = out["arms"]["arm3_conflict"]
    lines += [
        "",
        f"Arm 3 stated verdict: {v['verdict']}",
        f"Arm 3 stated reliable source: {v['stated_reliable']}",
        f"Arm 3 stated reliable source by answer: {out['arm3_stated_reliable_by_answer']}",
        "",
        "## Paired contrasts on exact answer (distinct-answer items)",
        "",
        "| Contrast : source | First only | Second only | Difference | 95% interval (problem-clustered) | Exact McNemar p |",
        "|---|---:|---:|---:|---:|---:|",
    ]
    for name, c in out["contrasts"].items():
        lo, hi = c["ci95"]
        lines.append(
            f"| {name} | {c['first_only']} | {c['second_only']} | {100 * c['difference']:+.1f} pp "
            f"| {100 * lo:+.1f} to {100 * hi:+.1f} | {format_log10p(c['mcnemar_exact_log10p'])} |"
        )
    f = out["finished_both"]
    lines += [
        "",
        "## Sensitivity",
        "",
        f"Finished in both Arms 2 and 3 (n = {f['n']}, conditioned on a post-treatment variable): "
        f"Arm 2 image {100 * f['arm2_placebo:image']:.1f}%, text {100 * f['arm2_placebo:text']:.1f}%; "
        f"Arm 3 image {100 * f['arm3_conflict:image']:.1f}%, text {100 * f['arm3_conflict:text']:.1f}%.",
        "",
        f"Problem solved in both roles, phi = {out['role_solved_phi']:.3f}.",
        "",
        "| Arm | Token bin | n | Exact image | Exact text | Attempt image |",
        "|---|---|---:|---:|---:|---:|",
    ]
    for a, rows in out["token_bins"].items():
        for b, r in rows.items():
            lines.append(f"| {a} | {b} | {r['n']} | {100 * r['image']:.1f}% | {100 * r['text']:.1f}% | {100 * r['attempt_image']:.1f}% |")
    lines += ["", "| Dataset | n | Arm | Exact image | Exact text |", "|---|---:|---|---:|---:|"]
    for src, r in out["by_source"].items():
        for a in ARMS:
            lines.append(f"| {src} | {r['n']} | {a} | {100 * r[a + ':image']:.1f}% | {100 * r[a + ':text']:.1f}% |")
    lines.append("")
    return "\n".join(lines)


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("--results_file", default=DEFAULT_RESULTS)
    parser.add_argument("--output_dir", default=None)
    parser.add_argument("--bootstrap_reps", type=int, default=1000)
    parser.add_argument("--check", action="store_true", help="Exit 1 if stored data no longer match the audit")
    args = parser.parse_args()

    data = load(args.results_file)
    out = compute(data, reps=args.bootstrap_reps)
    report = render(out)
    print(report)
    if args.output_dir:
        os.makedirs(args.output_dir, exist_ok=True)
        with open(os.path.join(args.output_dir, "reanalysis_v3.md"), "w", encoding="utf-8") as f:
            f.write(report)
        with open(os.path.join(args.output_dir, "reanalysis_v3.json"), "w", encoding="utf-8") as f:
            json.dump(out, f, indent=2)
    if args.check:
        errors = check(data, out)
        for e in errors:
            print(f"CHECK FAILED: {e}", file=sys.stderr)
        if errors:
            return 1
        print("CHECK PASSED: stored v3 counts match the audit values.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
