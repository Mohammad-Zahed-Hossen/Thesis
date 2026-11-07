#!/usr/bin/env python3
"""Mediator transplant: cross the instruction with the verbalization.

v3 randomized the instruction only, so it can't say whether the verbalization itself
matters. This script holds the instruction fixed and prefills the verbalization.

  Instruction z:   neutral (default desc_image_first) or conflict (default conflict_full)
  Verbalization m: the model's own text, taken from each donor arm for the same item

Cells
  z0_m0, z1_m1     Own instruction with own verbalization. Should reproduce the donor
                   output, so these double as a fidelity check.
  z0_m1, z1_m0     Crossed. These are the causal contrasts.
  z*_rel_image, z*_rel_text   Fixed text naming a more reliable source. Tests direction.
  z*_eq_a, z*_eq_b            Two fixed texts with the same meaning. Measures how much
                              answers move when only the wording changes.
  z*_filler                   Fixed text with no source content.

Prefilling identifies the controlled effect of m at a fixed z. Natural direct and
indirect effects need further assumptions. Prefilled text isn't what the model would
write under that instruction, so effects may not transfer to free generation.

Usage on Colab, after a harness_v4.py run that includes both donor arms:
    python transplant_v4.py --donor_file results_v4/confirm_qwen25.jsonl --phase confirm --run_tag transplant_qwen25
"""
from __future__ import annotations

import argparse
import json
import os
import sys
from typing import Dict, List, Sequence, Tuple

import harness_v4 as h
import score_v4 as sc

HERE = os.path.dirname(os.path.abspath(__file__))
SEPARATOR = "\n\n"

CONFLICT_SENTENCE = "The image and the typed text do not agree, because they present different problems."
AUTHORED = {
    "rel_image": f"{CONFLICT_SENTENCE} I consider the image more reliable.{SEPARATOR}",
    "rel_text": f"{CONFLICT_SENTENCE} I consider the typed text more reliable.{SEPARATOR}",
    "eq_a": f"{CONFLICT_SENTENCE}{SEPARATOR}",
    "eq_b": f"The image and the typed text disagree, since each one presents a different problem.{SEPARATOR}",
    "filler": f"It helps to check each arithmetic step carefully. Writing units beside each number also prevents mistakes.{SEPARATOR}",
}


def donor_prefill(full_text: str) -> str:
    """The donor's verbalization, ending exactly where the model's own text continued.

    Keeps a newline break when the donor had one, and drops a single trailing space
    because the model's next token carries that space itself. Forcing a blank line on
    every donor broke the fidelity check: in the first dev run, answers reproduced in
    78 of 84 donors that really had a blank line and 58 of 316 others.

    A donor that stopped without solving has no continuation to copy. It gets a blank
    line so the model has a chance to solve, and is left out of the fidelity check.
    """
    verbalization, solve = sc.split_verbalization(full_text)
    if not verbalization.strip():
        return ""
    stripped = verbalization.rstrip()
    if not solve.strip():
        return stripped + SEPARATOR
    trailing = verbalization[len(stripped) :]
    leading = solve[: len(solve) - len(solve.lstrip())]
    gap = trailing + leading
    return stripped + (gap if "\n" in gap else "")


def load_donors(path: str, arm_neutral: str, arm_conflict: str, model_id: str) -> Tuple[Dict[str, str], Dict[str, str]]:
    """Read donor verbalizations for one model, refusing rows from any other model."""
    neutral: Dict[str, str] = {}
    conflict: Dict[str, str] = {}
    with open(path, encoding="utf-8") as f:
        for line in f:
            row = json.loads(line)
            if row["arm"] not in {arm_neutral, arm_conflict}:
                continue
            if row["model_id"] != model_id:
                raise SystemExit(f"Donor row from {row['model_id']}, but this run uses {model_id}.")
            prefill = donor_prefill(row["full_text"])
            if prefill:
                (neutral if row["arm"] == arm_neutral else conflict)[row["id"]] = prefill
    return neutral, conflict


def build_requests(
    items: Sequence[h.Item], neutral: Dict[str, str], conflict: Dict[str, str], arm_neutral: str, arm_conflict: str
) -> Tuple[List[h.Request], Dict[str, int]]:
    """Every cell for every item that has both donors, so comparisons stay complete-case."""
    requests: List[h.Request] = []
    excluded = {"no_neutral_donor": 0, "no_conflict_donor": 0}
    for item in items:
        if item.id not in neutral:
            excluded["no_neutral_donor"] += 1
        if item.id not in conflict:
            excluded["no_conflict_donor"] += 1
        if item.id not in neutral or item.id not in conflict:
            continue
        for z, arm in (("z0", arm_neutral), ("z1", arm_conflict)):
            base = h.build_request(item, arm)
            cells = {"m0": neutral[item.id], "m1": conflict[item.id], **AUTHORED}
            for m, prefill in cells.items():
                requests.append(
                    h.Request(item=item, arm=f"{z}_{m}", prompt=base.prompt, stimulus="conflict", prefill=prefill)
                )
    return requests, excluded


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    h.add_common_args(parser)
    parser.add_argument("--donor_file", required=True)
    parser.add_argument("--arm_neutral", default="desc_image_first")
    parser.add_argument("--arm_conflict", default="conflict_full")
    args = parser.parse_args()

    cfg = h.config_from_args(args, arm_set="transplant", arms=[args.arm_neutral, args.arm_conflict])
    h.resolve_revisions(cfg)
    items = h.select_items(args, cfg)
    neutral, conflict = load_donors(args.donor_file, args.arm_neutral, args.arm_conflict, cfg.model_id)
    requests, excluded = build_requests(items, neutral, conflict, args.arm_neutral, args.arm_conflict)
    if not requests:
        print("No requests: no item has both donors. Check --donor_file, --phase and --arm_*.", file=sys.stderr)
        return 2
    print(f"{len(items)} items; {len(requests)} requests; excluded: {excluded}")

    backend = h.EchoBackend() if args.dry_run else h.HFBackend(cfg)
    os.makedirs(args.output_dir, exist_ok=True)
    out_path = os.path.join(args.output_dir, f"{cfg.run_tag}.jsonl")
    manifest = os.path.join(args.output_dir, f"{cfg.run_tag}.manifest.json")
    scripts = [os.path.abspath(__file__), os.path.join(HERE, "harness_v4.py"), os.path.join(HERE, "score_v4.py")]
    h.write_manifest(manifest, cfg, backend, len(items), scripts)
    written = h.run_requests(requests, backend, cfg, out_path)
    h.write_manifest(manifest, cfg, backend, len(items), scripts)
    print(f"Wrote {written} rows to {out_path}")
    return h.report_missing(requests, out_path)


if __name__ == "__main__":
    sys.exit(main())
