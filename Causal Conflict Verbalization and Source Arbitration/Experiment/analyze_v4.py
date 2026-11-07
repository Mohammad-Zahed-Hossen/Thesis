#!/usr/bin/env python3
"""Analyze v4 runs: quality gates, planned contrasts, transplant effects. Runs locally.

The contrast lists below are a draft. Freeze them in the pre-registration before looking
at confirmatory data. Holm correction applies within each family.

Crossed problem effects: intervals here resample problems. To fit the mixed model as well,
use --export_long and fit in R, since this project's local Python has no mixed-model library:
    glmer(hit ~ arm + (1 | image_problem) + (1 | text_problem), family = binomial, data = long)

Usage:
    python analyze_v4.py --runs results_v4/dev_qwen25.jsonl --gates
    python analyze_v4.py --runs results_v4/confirm_qwen25.jsonl results_v4/transplant_qwen25.jsonl --output_dir results_v4/analysis
"""
from __future__ import annotations

import argparse
import csv
import json
import os
import sys
from collections import Counter, defaultdict
from typing import Any, Dict, Iterable, List, Optional, Sequence, Tuple

import score_v4 as sc
from statistical_analysis import format_log10p, holm_adjust_log10, mcnemar_exact_log10p, pigeonhole_ci

MAX_CAP_RATE = 0.05
MIN_ANSWER_RATE = 0.90

BEHAVIOUR_CONTRASTS = [
    ("conflict_v3", "placebo_v3"),
    ("conflict_full", "filler"),
    ("desc_image_first", "filler"),
    ("desc_text_first", "filler"),
    ("desc_image_first", "desc_text_first"),
    ("detect_only", "filler"),
    ("reliability_only", "filler"),
    ("filler", "direct"),
    ("conflict_full", "direct"),
]
TRANSPLANT_CONTRASTS = [
    # Effect of the verbalization with the instruction fixed.
    ("z0_m1", "z0_m0"),
    ("z1_m1", "z1_m0"),
    # Effect of the instruction with the verbalization fixed.
    ("z1_m0", "z0_m0"),
    ("z1_m1", "z0_m1"),
    # Direction: does naming a source move behaviour toward it?
    ("z0_rel_image", "z0_rel_text"),
    ("z1_rel_image", "z1_rel_text"),
    # Reference against a verbalization with no source content.
    ("z0_m1", "z0_filler"),
    ("z1_m1", "z1_filler"),
]
EQUIVALENCE_PAIRS = [("z0_eq_a", "z0_eq_b"), ("z1_eq_a", "z1_eq_b")]
FIDELITY_PAIRS = [("z0_m0", "desc_image_first"), ("z1_m1", "conflict_full")]
ANSWER_ONLY_TOKENS = 8
# detect_abstention's phrase list in the v3 harness. A test keeps the two identical.
V3_ABSTENTION_PHRASES = [
    "cannot be determined", "no numerical answer", "no need to provide",
    "cannot determine", "not possible to", "no direct connection",
    "cannot be answered", "not enough information", "unrelated problems",
    "contradict each other, so", "different problems, so there is no",
]


def v3_abstention_label(text: str) -> bool:
    low = text.lower()
    return any(p in low for p in V3_ABSTENTION_PHRASES)


def group_key(r: Dict[str, Any]) -> Tuple:
    """Rows are only compared within the same model and generation settings."""
    return (r["model_id"], r["split"], r["phase"], r["repetition_penalty"], r["do_sample"], r["seed"], r["paraphrase"])


def group_label(key: Tuple) -> str:
    model, split, phase, penalty, sampled, seed, para = key
    tail = f", sampled seed {seed}" if sampled else ""
    return f"{model} | {split} | {phase} | repetition_penalty={penalty} | paraphrase={para}{tail}"


def load_rows(paths: Iterable[str], allow_dry_run: bool = False) -> List[Dict[str, Any]]:
    """Read and score rows. Refuses duplicates and fake-model output."""
    rows = []
    seen = set()
    for path in paths:
        manifest = path[: -len(".jsonl")] + ".manifest.json" if path.endswith(".jsonl") else None
        if not manifest or not os.path.exists(manifest):
            raise SystemExit(f"{path} has no manifest, so its origin can't be confirmed.")
        with open(manifest, encoding="utf-8") as f:
            if json.load(f)["environment"].get("backend") == "echo" and not allow_dry_run:
                raise SystemExit(f"{path} came from the fake model. It isn't data; pass --allow_dry_run to test the pipeline.")
        with open(path, encoding="utf-8") as f:
            for line in f:
                try:
                    r = json.loads(line)
                except json.JSONDecodeError:
                    print(f"Warning: skipped a cut-off line in {path}", file=sys.stderr)
                    continue
                key = (group_key(r), r["arm"], r["id"])
                if key in seen:
                    raise SystemExit(f"Duplicate row for {key}. Don't pass overlapping runs.")
                seen.add(key)
                r["score"] = sc.score_output(r["full_text"], r["image_question"], r["text_question"], r["y_image"], r["y_text"])
                rows.append(r)
    return rows


def arm_summary(rows: Sequence[Dict[str, Any]]) -> Dict[str, Any]:
    n = len(rows)
    source = Counter(r["score"]["answer_source"] for r in rows)
    methods = Counter(r["score"]["answer_method"] for r in rows)
    return {
        "n": n,
        "image": source["image"] / n,
        "text": source["text"] / n,
        "both": source["both"] / n,
        "neither": source["neither"] / n,
        "attempt_image": sum(r["score"]["attempt"] == "image" for r in rows) / n,
        "attempt_text": sum(r["score"]["attempt"] == "text" for r in rows) / n,
        "attempt_unknown": sum(r["score"]["attempt"] == "unknown" for r in rows) / n,
        "refusal": sum(r["score"]["refusal"] for r in rows) / n,
        "cap_rate": sum(r["hit_cap"] for r in rows) / n,
        "answer_or_refusal_rate": sum(r["score"]["answer"] is not None or r["score"]["refusal"] for r in rows) / n,
        "fallback_rate": methods["fallback_last_number"] / n,
        "answer_only_rate": sum(r["tokens"] <= ANSWER_ONLY_TOKENS for r in rows) / n,
        "no_solve_rate": sum(not r["score"]["has_solve_segment"] for r in rows) / n,
        "v3_abstention_rate": sum(v3_abstention_label(r["full_text"]) for r in rows) / n,
        "tokens_mean": sum(r["tokens"] for r in rows) / n,
        "verdict": dict(Counter(r["score"]["verdict"] for r in rows)),
        "stated_reliable": dict(Counter(r["score"]["stated_reliable"] for r in rows)),
    }


def check_gates(summaries: Dict[Tuple, Dict[str, Dict[str, Any]]]) -> List[str]:
    """Failures of the dev-phase gates, one string per arm and rule."""
    failures = []
    for key, arms in summaries.items():
        for arm, s in sorted(arms.items()):
            if s["cap_rate"] >= MAX_CAP_RATE:
                failures.append(f"{group_label(key)} | {arm}: token cap {100 * s['cap_rate']:.1f}% (limit <{100 * MAX_CAP_RATE:.0f}%)")
            if s["answer_or_refusal_rate"] < MIN_ANSWER_RATE:
                failures.append(f"{group_label(key)} | {arm}: answer or refusal {100 * s['answer_or_refusal_rate']:.1f}% (limit >={100 * MIN_ANSWER_RATE:.0f}%)")
    return failures


def missing_rows(rows: Sequence[Dict[str, Any]]) -> Dict[Tuple, Dict[str, List[str]]]:
    """Per group, the items each arm lacks compared with the group's other arms.

    Paired contrasts silently drop such items, so a gap has to fail the gates.
    """
    ids_by_group: Dict[Tuple, Dict[str, set]] = defaultdict(lambda: defaultdict(set))
    for r in rows:
        ids_by_group[group_key(r)][r["arm"]].add(r["id"])
    out: Dict[Tuple, Dict[str, List[str]]] = {}
    for key, arms in ids_by_group.items():
        everything = set().union(*arms.values())
        gaps = {a: sorted(everything - ids) for a, ids in arms.items() if everything - ids}
        if gaps:
            out[key] = gaps
    return out


def completeness_failures(rows: Sequence[Dict[str, Any]]) -> List[str]:
    return [
        f"{group_label(key)} | {arm}: {len(ids)} missing rows, e.g. {ids[:2]}"
        for key, gaps in missing_rows(rows).items()
        for arm, ids in sorted(gaps.items())
    ]


def penalty_effects(rows: Sequence[Dict[str, Any]]) -> List[Dict[str, Any]]:
    """Paired comparison of the same arm and items at the highest and lowest penalty."""
    grouped: Dict[Tuple, Dict[float, Dict[str, Dict]]] = defaultdict(lambda: defaultdict(dict))
    for r in rows:
        key = (r["model_id"], r["split"], r["phase"], r["do_sample"], r["seed"], r["paraphrase"], r["arm"])
        grouped[key][r["repetition_penalty"]][r["id"]] = r
    out = []
    measures = {
        "exact image": lambda r: r["score"]["answer_source"] == "image",
        "exact text": lambda r: r["score"]["answer_source"] == "text",
        "attempt image": lambda r: r["score"]["attempt"] == "image",
        "attempt text": lambda r: r["score"]["attempt"] == "text",
        "stops without solving": lambda r: not r["score"]["has_solve_segment"],
        "v3 abstention label": lambda r: v3_abstention_label(r["full_text"]),
    }
    for key, by_penalty in grouped.items():
        if len(by_penalty) < 2:
            continue
        low_p, high_p = min(by_penalty), max(by_penalty)
        low, high = by_penalty[low_p], by_penalty[high_p]
        ids = sorted(set(low) & set(high))
        if not ids:
            continue
        for name, f in measures.items():
            x = [f(high[i]) for i in ids]
            y = [f(low[i]) for i in ids]
            b = sum(u and not v for u, v in zip(x, y))
            c = sum(v and not u for u, v in zip(x, y))
            out.append({
                "model_id": key[0], "phase": key[2], "arm": key[6], "measure": name, "n": len(ids),
                "low_penalty": low_p, "high_penalty": high_p,
                "low_rate": sum(y) / len(ids), "high_rate": sum(x) / len(ids),
                "high_only": b, "low_only": c, "log10p": mcnemar_exact_log10p(b, c),
            })
    return out


def _problem_keys(r: Dict[str, Any]) -> Tuple[str, str]:
    return r["image_question"] or r["id"], r["text_question"] or r["id"]


def contrast(by_arm: Dict[str, Dict[str, Dict]], first: str, second: str, outcome: str, reps: int) -> Optional[Dict[str, Any]]:
    """Paired contrast on items present in both arms. None if an arm is absent."""
    if first not in by_arm or second not in by_arm:
        return None
    ids = sorted(set(by_arm[first]) & set(by_arm[second]))
    if not ids:
        return None
    kind, _, value = outcome.partition(":")
    field = "answer_source" if kind == "answer" else "attempt"
    x = [by_arm[first][i]["score"][field] == value for i in ids]
    y = [by_arm[second][i]["score"][field] == value for i in ids]
    b = sum(u and not v for u, v in zip(x, y))
    c = sum(v and not u for u, v in zip(x, y))
    keys = [_problem_keys(by_arm[first][i]) for i in ids]
    low, high = pigeonhole_ci([float(u) - float(v) for u, v in zip(x, y)], [k[0] for k in keys], [k[1] for k in keys], reps=reps)
    return {
        "first": first,
        "second": second,
        "outcome": outcome,
        "n": len(ids),
        "first_rate": sum(x) / len(ids),
        "second_rate": sum(y) / len(ids),
        "difference": (sum(x) - sum(y)) / len(ids),
        "ci95": [low, high],
        "first_only": b,
        "second_only": c,
        "log10p": mcnemar_exact_log10p(b, c),
    }


def family(by_arm: Dict[str, Dict[str, Dict]], pairs: Sequence[Tuple[str, str]], outcomes: Sequence[str], reps: int) -> List[Dict[str, Any]]:
    results = []
    for first, second in pairs:
        for outcome in outcomes:
            r = contrast(by_arm, first, second, outcome, reps)
            if r is not None:
                results.append(r)
    if results:
        for r, a in zip(results, holm_adjust_log10([r["log10p"] for r in results])):
            r["log10p_holm"] = a
    return results


def prefix_sensitivity(by_arm: Dict[str, Dict[str, Dict]]) -> List[Dict[str, Any]]:
    """How often does the answer change when only the wording of the prefill changes?"""
    out = []
    for first, second in EQUIVALENCE_PAIRS:
        if first in by_arm and second in by_arm:
            ids = sorted(set(by_arm[first]) & set(by_arm[second]))
            if ids:
                changed = sum(not _same_answer(by_arm[first][i], by_arm[second][i]) for i in ids)
                out.append({"first": first, "second": second, "n": len(ids), "answer_changed": changed / len(ids)})
    return out


def _same_answer(a: Dict[str, Any], b: Dict[str, Any]) -> bool:
    x, y = a["score"]["answer"], b["score"]["answer"]
    return (x is None and y is None) or sc.numeric_equal(x, y)


def transplant_fidelity(by_arm: Dict[str, Dict[str, Dict]]) -> List[Dict[str, Any]]:
    """Does prefilling a model's own verbalization reproduce its own answer?

    Donors that stopped without solving are excluded, since they have nothing to reproduce.
    """
    out = []
    for cell, donor in FIDELITY_PAIRS:
        if cell in by_arm and donor in by_arm:
            shared = sorted(set(by_arm[cell]) & set(by_arm[donor]))
            ids = [i for i in shared if by_arm[donor][i]["score"]["has_solve_segment"]]
            if ids:
                same = sum(_same_answer(by_arm[cell][i], by_arm[donor][i]) for i in ids)
                out.append({"cell": cell, "donor": donor, "n": len(ids), "excluded_no_solve": len(shared) - len(ids), "same_answer": same / len(ids)})
    return out


def solvability(by_arm: Dict[str, Dict[str, Dict]]) -> Optional[Dict[str, Any]]:
    """The same problem solved from the image alone and from the text alone."""
    if "base_image" not in by_arm or "base_text" not in by_arm:
        return None
    as_image = {r["image_question"]: r for r in by_arm["base_image"].values() if r["image_question"]}
    as_text = {r["text_question"]: r for r in by_arm["base_text"].values() if r["text_question"]}
    shared = sorted(set(as_image) & set(as_text))
    if not shared:
        return None
    x = [as_image[q]["score"]["answer_source"] == "both" for q in shared]
    y = [as_text[q]["score"]["answer_source"] == "both" for q in shared]
    b = sum(u and not v for u, v in zip(x, y))
    c = sum(v and not u for u, v in zip(x, y))
    return {"n": len(shared), "image_rate": sum(x) / len(shared), "text_rate": sum(y) / len(shared), "image_only": b, "text_only": c, "log10p": mcnemar_exact_log10p(b, c)}


def analyze(rows: Sequence[Dict[str, Any]], reps: int = 2000) -> Dict[Tuple, Dict[str, Any]]:
    groups: Dict[Tuple, List[Dict[str, Any]]] = defaultdict(list)
    for r in rows:
        groups[group_key(r)].append(r)
    results = {}
    for key, members in groups.items():
        arm_rows: Dict[str, List[Dict]] = defaultdict(list)
        by_arm: Dict[str, Dict[str, Dict]] = defaultdict(dict)
        for r in members:
            arm_rows[r["arm"]].append(r)
            by_arm[r["arm"]][r["id"]] = r
        results[key] = {
            "arms": {a: arm_summary(v) for a, v in arm_rows.items()},
            "behaviour_primary": family(by_arm, BEHAVIOUR_CONTRASTS, ["answer:image", "answer:text"], reps),
            "behaviour_secondary": family(by_arm, BEHAVIOUR_CONTRASTS, ["attempt:image", "attempt:text"], reps),
            "transplant_primary": family(by_arm, TRANSPLANT_CONTRASTS, ["answer:image", "answer:text"], reps),
            "transplant_secondary": family(by_arm, TRANSPLANT_CONTRASTS, ["attempt:image", "attempt:text"], reps),
            "prefix_sensitivity": prefix_sensitivity(by_arm),
            "fidelity": transplant_fidelity(by_arm),
            "solvability": solvability(by_arm),
        }
    return results


def _contrast_table(title: str, rows: Sequence[Dict[str, Any]]) -> List[str]:
    if not rows:
        return []
    lines = [f"### {title}", "", "| First vs second | Outcome | n | First | Second | Difference | 95% interval | First only / second only | Holm p |", "|---|---|---:|---:|---:|---:|---:|---:|---:|"]
    for r in rows:
        lo, hi = r["ci95"]
        lines.append(
            f"| {r['first']} vs {r['second']} | {r['outcome']} | {r['n']} | {100 * r['first_rate']:.1f}% | {100 * r['second_rate']:.1f}% "
            f"| {100 * r['difference']:+.1f} pp | {100 * lo:+.1f} to {100 * hi:+.1f} | {r['first_only']} / {r['second_only']} | {format_log10p(r['log10p_holm'])} |"
        )
    return lines + [""]


def render(results: Dict[Tuple, Dict[str, Any]], failures: Sequence[str], penalty: Sequence[Dict[str, Any]] = ()) -> str:
    lines = ["# v4 analysis", "", "Attempt, refusal and verdict labels are heuristics until validated by `sample_for_coding.py evaluate`.", ""]
    if failures:
        lines += ["## Gate failures", ""] + [f"- {f}" for f in failures] + [""]
    if penalty:
        lines += ["## Repetition penalty, same arm and items", "", "| Arm | Measure | n | Low penalty | High penalty | High only / low only | Exact McNemar p |", "|---|---|---:|---:|---:|---:|---:|"]
        for p in penalty:
            lines.append(
                f"| {p['arm']} | {p['measure']} | {p['n']} | {100 * p['low_rate']:.1f}% ({p['low_penalty']}) | {100 * p['high_rate']:.1f}% ({p['high_penalty']}) "
                f"| {p['high_only']} / {p['low_only']} | {format_log10p(p['log10p'])} |"
            )
        lines.append("")
    for key, r in results.items():
        lines += [f"## {group_label(key)}", "", "### Arms", "", "| Arm | n | Exact image | Exact text | Same gold | Neither | Attempt image | Attempt text | Refusal | v3 abstain label | Token cap | Stops unsolved | Answer only | Fallback answer | Mean tokens |", "|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|"]
        for arm, s in sorted(r["arms"].items()):
            lines.append(
                f"| {arm} | {s['n']} | {100 * s['image']:.1f}% | {100 * s['text']:.1f}% | {100 * s['both']:.1f}% | {100 * s['neither']:.1f}% | {100 * s['attempt_image']:.1f}% "
                f"| {100 * s['attempt_text']:.1f}% | {100 * s['refusal']:.1f}% | {100 * s['v3_abstention_rate']:.1f}% | {100 * s['cap_rate']:.1f}% | {100 * s['no_solve_rate']:.1f}% "
                f"| {100 * s['answer_only_rate']:.1f}% | {100 * s['fallback_rate']:.1f}% | {s['tokens_mean']:.1f} |"
            )
        lines.append("")
        lines += ["In single-source and congruent arms both gold answers are the same, so a correct answer appears under Same gold.", ""]
        if r["solvability"]:
            v = r["solvability"]
            lines += [
                "### Solvability: same problem from image alone and text alone",
                "",
                f"Image {100 * v['image_rate']:.1f}%, text {100 * v['text_rate']:.1f}% of {v['n']} problems. Solved only from image / only from text: {v['image_only']} / {v['text_only']}; exact McNemar p = {format_log10p(v['log10p'])}.",
                "",
            ]
        congruent = {a: s for a, s in r["arms"].items() if a.startswith("congruent")}
        if congruent:
            lines += ["### Congruent arms: stated verdict (a conflict verdict here is a false alarm)", ""]
            lines += [f"- {a}: {s['verdict']}" for a, s in sorted(congruent.items())] + [""]
        if r["fidelity"]:
            lines += ["### Fidelity: own verbalization prefilled, same answer as donor", ""]
            lines += [f"- {f['cell']} vs {f['donor']}: {100 * f['same_answer']:.1f}% of {f['n']} ({f['excluded_no_solve']} donors without solving excluded)" for f in r["fidelity"]] + [""]
        if r["prefix_sensitivity"]:
            lines += ["### Wording control: answer changed between same-meaning prefills", ""]
            lines += [f"- {f['first']} vs {f['second']}: {100 * f['answer_changed']:.1f}% of {f['n']}" for f in r["prefix_sensitivity"]] + [""]
        lines += _contrast_table("Transplant, primary (exact answer)", r["transplant_primary"])
        lines += _contrast_table("Transplant, secondary (attempt label)", r["transplant_secondary"])
        lines += _contrast_table("Behaviour, primary (exact answer)", r["behaviour_primary"])
        lines += _contrast_table("Behaviour, secondary (attempt label)", r["behaviour_secondary"])
    return "\n".join(lines)


def export_long(rows: Sequence[Dict[str, Any]], path: str) -> None:
    with open(path, "w", newline="", encoding="utf-8") as f:
        w = csv.writer(f)
        w.writerow(["model_id", "split", "repetition_penalty", "paraphrase", "seed", "id", "source", "arm", "stimulus", "image_problem", "text_problem", "exact_image", "exact_text", "attempt", "refusal", "hit_cap", "tokens"])
        for r in rows:
            image_key, text_key = _problem_keys(r)
            w.writerow([
                r["model_id"], r["split"], r["repetition_penalty"], r["paraphrase"], r["seed"], r["id"], r["source"], r["arm"], r["stimulus"],
                image_key, text_key, int(r["score"]["answer_source"] in {"image", "both"}), int(r["score"]["answer_source"] in {"text", "both"}),
                r["score"]["attempt"], int(r["score"]["refusal"]), int(r["hit_cap"]), r["tokens"],
            ])


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("--runs", nargs="+", required=True)
    parser.add_argument("--output_dir", default=None)
    parser.add_argument("--gates", action="store_true", help="Exit 1 if any arm fails a quality gate")
    parser.add_argument("--export_long", action="store_true")
    parser.add_argument("--bootstrap_reps", type=int, default=2000)
    parser.add_argument("--allow_dry_run", action="store_true")
    args = parser.parse_args()

    rows = load_rows(args.runs, allow_dry_run=args.allow_dry_run)
    if not rows:
        print("Error: no rows found.", file=sys.stderr)
        return 2
    results = analyze(rows, reps=args.bootstrap_reps)
    failures = completeness_failures(rows) + check_gates({k: v["arms"] for k, v in results.items()})
    penalty = penalty_effects(rows)
    report = render(results, failures, penalty)
    print(report)
    if args.output_dir:
        os.makedirs(args.output_dir, exist_ok=True)
        with open(os.path.join(args.output_dir, "analysis_v4.md"), "w", encoding="utf-8") as f:
            f.write(report)
        with open(os.path.join(args.output_dir, "analysis_v4.json"), "w", encoding="utf-8") as f:
            json.dump({"gate_failures": failures, "penalty_effects": penalty, "groups": {group_label(k): v for k, v in results.items()}}, f, indent=2)
        if args.export_long:
            export_long(rows, os.path.join(args.output_dir, "long.csv"))
    if args.gates:
        if failures:
            print(f"GATES FAILED: {len(failures)} rule failures.", file=sys.stderr)
            return 1
        print("GATES PASSED: every arm is complete, under the token-cap limit and over the answer-rate limit.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
