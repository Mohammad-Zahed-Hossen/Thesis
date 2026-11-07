#!/usr/bin/env python3
"""Draw outputs for human coding, then measure agreement and scorer validity.

Two modes:

  sample    Writes one blinded sheet per coder, plus a separate key. Do not open the
            key until coding is finished. Coders must work independently.

  evaluate  Reports Cohen's kappa between coders, and each score_v4 label against the
            items where the coders agreed, weighted back to the population.

The sample over-represents rare labels, so raw agreement over the sheet would misstate
accuracy. Weighted results correct for that. The weights are in the key.

Usage:
    python sample_for_coding.py sample --output_dir coding_v3
    python sample_for_coding.py evaluate --coder_a coding_v3/coder_A.csv --coder_b coding_v3/coder_B.csv --key coding_v3/KEY_do_not_open.csv
"""
from __future__ import annotations

import argparse
import csv
import json
import os
import random
import sys
from collections import Counter, defaultdict
from typing import Dict, List, Optional, Sequence, Tuple

import score_v4 as sc

HERE = os.path.dirname(os.path.abspath(__file__))
DEFAULT_RESULTS = os.path.join(HERE, "results_v3", "full_experiment_results v3.0.json")

# Sample sizes per arm. Arm 1 is small because 98.1% of its outputs hit the token cap.
ARM_SAMPLE = {"arm1_direct": 60, "arm2_placebo": 120, "arm3_conflict": 120}

CODE_COLUMNS = ["attempted_problem", "refused", "verdict", "stated_reliable"]
ALLOWED = {
    "attempted_problem": {"image", "text", "both", "neither"},
    "refused": {"yes", "no"},
    "verdict": {"conflict", "agree", "cannot_determine", "no_relation", "no_info", "none"},
    "stated_reliable": {"image", "text", "undetermined", "absent"},
}
CODEBOOK = """# Codebook

Code from the output and the two problems only. Don't look at the key or the other coder's sheet.

attempted_problem: which problem does the working operate on, ignoring any opening description?
    image | text | both | neither. Use "both" if it mixes facts from the two problems.
    Judge what it works on, not whether the arithmetic is right.
refused: does the model decline to give a solution, with no solving attempted afterwards?
    yes | no. "Cannot determine if they agree. However, I can solve..." is "no".
verdict: what does the output say about how the image and text relate? Use the part before solving.
    conflict   | says they disagree, contradict, or present different problems
    agree      | says they agree or are consistent
    cannot_determine | says it can't tell whether they agree
    no_relation | says there is no agreement or contradiction between them
    no_info    | says they give no information, without any of the above
    none       | says nothing about how they relate
stated_reliable: which source does the output call more reliable?
    image | text | undetermined (raises reliability, names neither) | absent (doesn't raise it)

Valid codes are lower case, exactly as written above.
"""


def stratify(arm: str, s: dict) -> str:
    """Stratum: refusal first, then the answer-independent attempt label."""
    if s["refusal"]:
        return "refusal"
    return f"attempt_{s['attempt']}"


def allocate(strata_sizes: Dict[str, int], total: int) -> Dict[str, int]:
    """Equal allocation across strata, capped by stratum size, spare spread to the rest."""
    remaining = total
    allocation = {k: 0 for k in strata_sizes}
    open_strata = [k for k, v in strata_sizes.items() if v > 0]
    while remaining > 0 and open_strata:
        share = max(1, remaining // len(open_strata))
        for k in list(open_strata):
            take = min(share, strata_sizes[k] - allocation[k], remaining)
            allocation[k] += take
            remaining -= take
            if allocation[k] >= strata_sizes[k]:
                open_strata.remove(k)
            if remaining == 0:
                break
    return allocation


def draw_sample(data: List[dict], seed: int) -> List[dict]:
    rng = random.Random(seed)
    rows = []
    for arm, size in ARM_SAMPLE.items():
        strata: Dict[str, List[int]] = defaultdict(list)
        for i, d in enumerate(data):
            s = sc.score_output(d["arms"][arm]["text"], d["image_question"], d["text_question"], d["image_answer"], d["text_answer"])
            strata[stratify(arm, s)].append(i)
        allocation = allocate({k: len(v) for k, v in strata.items()}, size)
        for name in sorted(strata):
            members = strata[name]
            for i in rng.sample(members, allocation[name]):
                rows.append({"index": i, "arm": arm, "stratum": name, "weight": len(members) / allocation[name]})
    rng.shuffle(rows)
    return rows


def write_sample(data: List[dict], rows: List[dict], output_dir: str) -> None:
    os.makedirs(output_dir, exist_ok=True)
    with open(os.path.join(output_dir, "CODEBOOK.md"), "w", encoding="utf-8") as f:
        f.write(CODEBOOK)
    header = ["coding_id", "image_problem", "text_problem", "model_output"] + CODE_COLUMNS
    for coder in ("A", "B"):
        with open(os.path.join(output_dir, f"coder_{coder}.csv"), "w", newline="", encoding="utf-8-sig") as f:
            w = csv.writer(f)
            w.writerow(header)
            for n, r in enumerate(rows):
                d = data[r["index"]]
                w.writerow([f"c{n:04d}", d["image_question"], d["text_question"], d["arms"][r["arm"]]["text"]] + [""] * len(CODE_COLUMNS))
    with open(os.path.join(output_dir, "KEY_do_not_open.csv"), "w", newline="", encoding="utf-8") as f:
        w = csv.writer(f)
        w.writerow(["coding_id", "item_id", "arm", "stratum", "weight", "score_attempt", "score_refusal", "score_verdict", "score_stated_reliable"])
        for n, r in enumerate(rows):
            d = data[r["index"]]
            s = sc.score_output(d["arms"][r["arm"]]["text"], d["image_question"], d["text_question"], d["image_answer"], d["text_answer"])
            w.writerow([f"c{n:04d}", d["id"], r["arm"], r["stratum"], f"{r['weight']:.6f}", s["attempt"], "yes" if s["refusal"] else "no", s["verdict"], s["stated_reliable"]])


def cohens_kappa(a: Sequence[str], b: Sequence[str]) -> float:
    n = len(a)
    if n == 0:
        raise ValueError("no items to compare")
    observed = sum(x == y for x, y in zip(a, b)) / n
    ca, cb = Counter(a), Counter(b)
    expected = sum(ca[k] * cb[k] for k in set(ca) | set(cb)) / (n * n)
    return 1.0 if expected == 1.0 else (observed - expected) / (1 - expected)


def read_codes(path: str) -> Dict[str, Dict[str, str]]:
    """Read a coder sheet, rejecting blanks and invalid codes rather than skipping them."""
    with open(path, newline="", encoding="utf-8-sig") as f:
        rows = list(csv.DictReader(f))
    out, problems = {}, []
    for r in rows:
        codes = {}
        for col in CODE_COLUMNS:
            v = (r.get(col) or "").strip()
            if v not in ALLOWED[col]:
                problems.append(f"{r['coding_id']}.{col}={v!r}")
            codes[col] = v
        out[r["coding_id"]] = codes
    if problems:
        shown = ", ".join(problems[:10])
        raise ValueError(f"{path}: {len(problems)} blank or invalid codes, e.g. {shown}")
    return out


SCORE_FIELD = {
    "attempted_problem": "score_attempt",
    "refused": "score_refusal",
    "verdict": "score_verdict",
    "stated_reliable": "score_stated_reliable",
}


def rescore_key(key: Dict[str, dict], data: List[dict]) -> None:
    """Replace the key's stored labels with the current scorer's labels.

    The sample and its weights stay as drawn; only the labels under test change. This
    keeps a sheet valid after a scorer fix, without asking anyone to recode.
    """
    by_id = {d["id"]: d for d in data}
    for row in key.values():
        d = by_id[row["item_id"]]
        s = sc.score_output(d["arms"][row["arm"]]["text"], d["image_question"], d["text_question"], d["image_answer"], d["text_answer"])
        row["score_attempt"] = s["attempt"]
        row["score_refusal"] = "yes" if s["refusal"] else "no"
        row["score_verdict"] = s["verdict"]
        row["score_stated_reliable"] = s["stated_reliable"]


def evaluate(coder_a: str, coder_b: str, key_path: str, results_file: Optional[str] = None) -> Tuple[str, dict]:
    a, b = read_codes(coder_a), read_codes(coder_b)
    with open(key_path, newline="", encoding="utf-8") as f:
        key = {r["coding_id"]: r for r in csv.DictReader(f)}
    if set(a) != set(b) or set(a) != set(key):
        raise ValueError("coder sheets and key do not contain the same coding_ids")
    if results_file:
        with open(results_file, encoding="utf-8") as f:
            rescore_key(key, json.load(f))
    ids = sorted(key)
    results: dict = {"n": len(ids), "fields": {}}
    lines = ["# Coding evaluation", "", f"n = {len(ids)} outputs. An AI scorer checked against two human coders.", ""]
    lines += ["| Field | Kappa | Agreed items | Weighted scorer accuracy | Unknown scorer output, among agreed |", "|---|---:|---:|---:|---:|"]
    for col in CODE_COLUMNS:
        va, vb = [a[i][col] for i in ids], [b[i][col] for i in ids]
        agreed = [i for i in ids if a[i][col] == b[i][col]]
        wsum = sum(float(key[i]["weight"]) for i in agreed)
        correct = sum(float(key[i]["weight"]) for i in agreed if key[i][SCORE_FIELD[col]] == a[i][col])
        unknown = sum(key[i][SCORE_FIELD[col]] == "unknown" for i in agreed)
        kappa = cohens_kappa(va, vb)
        accuracy = correct / wsum if wsum else float("nan")
        results["fields"][col] = {"kappa": kappa, "agreed": len(agreed), "weighted_accuracy": accuracy, "unknown_among_agreed": unknown}
        lines.append(f"| {col} | {kappa:.3f} | {len(agreed)} | {100 * accuracy:.1f}% | {unknown} |")

    by_arm: dict = defaultdict(lambda: [0.0, 0.0])
    for i in ids:
        if a[i]["attempted_problem"] == b[i]["attempted_problem"]:
            w = float(key[i]["weight"])
            by_arm[key[i]["arm"]][0] += w
            by_arm[key[i]["arm"]][1] += w * (key[i]["score_attempt"] == a[i]["attempted_problem"])
    lines += ["", "Differential error matters more than average error: the arms must not differ much here.", "", "| Arm | Weighted attempt accuracy |", "|---|---:|"]
    for arm in sorted(by_arm):
        w, c = by_arm[arm]
        results.setdefault("attempt_accuracy_by_arm", {})[arm] = c / w if w else None
        lines.append(f"| {arm} | {100 * c / w:.1f}% |")
    lines.append("")
    return "\n".join(lines), results


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    sub = parser.add_subparsers(dest="mode", required=True)
    s = sub.add_parser("sample")
    s.add_argument("--results_file", default=DEFAULT_RESULTS)
    s.add_argument("--output_dir", required=True)
    s.add_argument("--seed", type=int, default=20261106)
    e = sub.add_parser("evaluate")
    e.add_argument("--coder_a", required=True)
    e.add_argument("--coder_b", required=True)
    e.add_argument("--key", required=True)
    e.add_argument("--output_json", default=None)
    e.add_argument("--results_file", default=DEFAULT_RESULTS, help="Outputs to re-score with the current scorer")
    args = parser.parse_args()

    if args.mode == "sample":
        with open(args.results_file, encoding="utf-8") as f:
            data = json.load(f)
        rows = draw_sample(data, args.seed)
        write_sample(data, rows, args.output_dir)
        print(f"Wrote {len(rows)} outputs to {args.output_dir}: {dict(Counter(r['arm'] for r in rows))}")
        return 0

    try:
        report, results = evaluate(args.coder_a, args.coder_b, args.key, args.results_file)
    except ValueError as exc:
        print(f"Error: {exc}", file=sys.stderr)
        return 2
    print(report)
    if args.output_json:
        with open(args.output_json, "w", encoding="utf-8") as f:
            json.dump(results, f, indent=2)
    return 0


if __name__ == "__main__":
    sys.exit(main())
