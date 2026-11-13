"""Stratified human-coding sampler and evaluator for v5 donor verbalizations and minimal-edit flips.

Subcommands:
    sample    Sample 200 donor verbalizations (stratified across model × regime × order × family)
              plus 50 passing flipped clauses per model, and write blinded coder A/B CSVs, a
              held-out key CSV, and CODEBOOK_v5.md.
    evaluate  Compute inter-coder Cohen's kappa and parser accuracy / flip quality once the
              coded CSVs are filled in.
"""

from __future__ import annotations

import argparse
import csv
import glob
import json
import os
import random
import sys
from collections import Counter, defaultdict
from typing import Any, Dict, List, Optional, Sequence, Tuple

HERE = os.path.dirname(os.path.abspath(__file__))
if HERE not in sys.path:
    sys.path.insert(0, HERE)

import score_v5 as sc  # noqa: E402
import transplant_v5 as tp  # noqa: E402

VALID_VERDICT_LABELS = {"image", "text", "chart", "report", "neither", "both", "unclear"}
TRUTHY = {"1", "y", "yes", "true", "pass", "ok"}
FALSY = {"0", "n", "no", "false", "fail", "bad"}

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


def build_verdict_samples(rows: Sequence[Dict[str, Any]], n_donors: int, seed: int) -> Tuple[List[Dict[str, Any]], List[Dict[str, Any]]]:
    rng = random.Random(seed)
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
    for mid in sorted(by_model):
        all_picked.extend(
            stratified_pick(
                by_model[mid],
                key_fn=lambda rec: (rec["regime"], rec["order"]),
                total_n=n_per_model,
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
    with open(path, newline="", encoding="utf-8") as f:
        return {r["sample_id"]: r for r in csv.DictReader(f)}


def cohens_kappa(xs: Sequence[str], ys: Sequence[str]) -> Optional[float]:
    n = len(xs)
    if n == 0:
        return None
    agree = sum(a == b for a, b in zip(xs, ys)) / n
    ca, cb = Counter(xs), Counter(ys)
    pe = sum((ca[k] / n) * (cb[k] / n) for k in set(ca) | set(cb))
    return (agree - pe) / (1 - pe) if pe < 1 else 1.0


def _norm_bool(val: Optional[str]) -> Optional[int]:
    if val is None:
        return None
    s = val.strip().lower()
    if s in TRUTHY:
        return 1
    if s in FALSY:
        return 0
    return None


def evaluate_verdicts(coder_a: Dict[str, Dict[str, str]], coder_b: Optional[Dict[str, Dict[str, str]]], key: Dict[str, Dict[str, str]]) -> Dict[str, Any]:
    paired_a, paired_b = [], []
    eval_rows = []
    for sid, krow in sorted(key.items()):
        a_lbl = (coder_a.get(sid, {}).get("coder_stated_source") or "").strip().lower()
        b_lbl = (coder_b.get(sid, {}).get("coder_stated_source") or "").strip().lower() if coder_b else ""
        if a_lbl and b_lbl:
            paired_a.append(a_lbl)
            paired_b.append(b_lbl)
        human = a_lbl or b_lbl
        if human:
            pred = (krow.get("predicted_stated_source") or "").strip().lower()
            eval_rows.append((krow["model_id"], krow["regime"], pred == human, pred, human))

    by_group: Dict[str, List[bool]] = defaultdict(list)
    for mid, reg, match, _, _ in eval_rows:
        by_group[f"{mid}|{reg}"].append(match)

    out: Dict[str, Any] = {
        "n_key": len(key),
        "n_coded": len(eval_rows),
        "n_double_coded": len(paired_a),
        "inter_coder_agreement": sum(x == y for x, y in zip(paired_a, paired_b)) / len(paired_a) if paired_a else None,
        "cohens_kappa": cohens_kappa(paired_a, paired_b),
        "parser_accuracy_overall": sum(x[2] for x in eval_rows) / len(eval_rows) if eval_rows else None,
        "parser_accuracy_by_model_regime": {k: {"n": len(v), "accuracy": sum(v) / len(v)} for k, v in sorted(by_group.items())},
    }
    return out


def evaluate_flips(coder_a: Dict[str, Dict[str, str]], coder_b: Optional[Dict[str, Dict[str, str]]], key: Dict[str, Dict[str, str]]) -> Dict[str, Any]:
    gram_vals, src_vals = [], []
    gram_a, gram_b, src_a, src_b = [], [], [], []
    by_model: Dict[str, Dict[str, List[int]]] = defaultdict(lambda: {"grammatical": [], "names_intended": []})
    for sid, krow in sorted(key.items()):
        ga = _norm_bool(coder_a.get(sid, {}).get("coder_grammatical_coherent"))
        gb = _norm_bool(coder_b.get(sid, {}).get("coder_grammatical_coherent")) if coder_b else None
        sa = _norm_bool(coder_a.get(sid, {}).get("coder_names_intended_source"))
        sb = _norm_bool(coder_b.get(sid, {}).get("coder_names_intended_source")) if coder_b else None
        if ga is not None and gb is not None:
            gram_a.append(str(ga))
            gram_b.append(str(gb))
        if sa is not None and sb is not None:
            src_a.append(str(sa))
            src_b.append(str(sb))
        g = ga if ga is not None else gb
        s = sa if sa is not None else sb
        if g is not None:
            gram_vals.append(g)
            by_model[krow["model_id"]]["grammatical"].append(g)
        if s is not None:
            src_vals.append(s)
            by_model[krow["model_id"]]["names_intended"].append(s)

    return {
        "n_key": len(key),
        "n_coded_grammatical": len(gram_vals),
        "grammatical_rate": sum(gram_vals) / len(gram_vals) if gram_vals else None,
        "grammatical_kappa": cohens_kappa(gram_a, gram_b),
        "n_coded_intended_source": len(src_vals),
        "names_intended_source_rate": sum(src_vals) / len(src_vals) if src_vals else None,
        "names_intended_kappa": cohens_kappa(src_a, src_b),
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


def cmd_sample(args: argparse.Namespace) -> int:
    paths = list(args.donor_files or sorted(glob.glob(os.path.join(args.input_dir, "*_donor_*.jsonl"))))
    if not paths:
        print(f"No donor JSONL files found in {args.input_dir}", file=sys.stderr)
        return 2
    rows = load_donor_rows(paths)
    verdicts_blind, verdicts_key = build_verdict_samples(rows, args.n_donors, args.seed)
    flips_blind, flips_key = build_flip_samples(rows, args.n_flips_per_model, args.seed)

    os.makedirs(args.out_dir, exist_ok=True)
    v_fields = ["sample_id", "item_id", "model_id", "regime", "family", "order", "verbalization_text", "full_text", "coder_stated_source", "coder_notes"]
    vk_fields = ["sample_id", "item_id", "model_id", "regime", "family", "order", "predicted_stated_source", "beh_source", "verbalization_text", "full_text"]
    f_fields = ["sample_id", "item_id", "model_id", "regime", "order", "own_source", "intended_flip_source", "original_verbalization", "flipped_verbalization", "coder_grammatical_coherent", "coder_names_intended_source", "coder_notes"]
    fk_fields = ["sample_id", "item_id", "model_id", "regime", "order", "own_source", "flip_source", "jaccard_multiset_flip", "n_swaps", "original_verbalization", "flipped_verbalization"]

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

    report = {
        "verdicts": evaluate_verdicts(ca_v, cb_v, key_v),
        "flips": evaluate_flips(ca_f, cb_f, key_f),
    }
    out_path = os.path.join(args.out_dir, "evaluation_v5.json")
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

    ev = sub.add_parser("evaluate", help="Score coded sheets against each other and the parser/gates")
    ev.add_argument("--out_dir", default=os.path.join(HERE, "coding_v5"))

    args = parser.parse_args()
    if args.cmd == "sample":
        return cmd_sample(args)
    return cmd_evaluate(args)


if __name__ == "__main__":
    sys.exit(main())
