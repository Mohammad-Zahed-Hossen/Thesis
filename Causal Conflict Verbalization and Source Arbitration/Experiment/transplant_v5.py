#!/usr/bin/env python3
"""Verdict transplant v5: minimal-edit verdicts, margin scoring, behavioural decodes.

Implements Docs/PREREGISTRATION_VERDICT_TRANSPLANT.md, §§5–6.

Inputs: a v5 base file (competency, prereg §3.3) and a v5 donor file (the model's
own verbalization under non-binding k = 1, in both orders; prereg §5.1).

For each competent item and each order, the donor verbalization v gives five verdicts:
  own        v unchanged
  flip       source nouns swapped inside the reliability sentence only
  none       the reliability sentence deleted
  para       that sentence replaced by a template naming the own source
  para_flip  the same template naming the opposite source
An item is used only if every variant in both orders passes the gates (prereg §5.3).

Cells:
  score (primary, prereg §6.1)  {nonbinding, binding} x {own, flip, none, para, para_flip}
                                + {explicit_image, explicit_text} x {none}
                                x templates k = 1..4 x both orders
  generate (secondary, §6.2)    the same grid for k in --beh_k (default: 1 only)

Prefix forcing identifies a controlled direct effect of the verdict at a fixed
instruction. It is not a natural indirect effect; don't call it mediation.

Usage on Colab:
    python transplant_v5.py --base_file results_v5/v5dev_base_qwen25.jsonl \
        --donor_file results_v5/v5dev_donor_qwen25.jsonl --phase dev --run_tag v5dev_tp_qwen25
"""
from __future__ import annotations

import argparse
import json
import os
import random
import re
import sys
from collections import Counter
from dataclasses import dataclass
from typing import Dict, List, Optional, Sequence, Tuple

import harness_v5 as h5
import score_v4 as v4
import score_v5 as sc

HERE = os.path.dirname(os.path.abspath(__file__))
JACCARD_MIN = 0.85  # prereg §5.3, gate 3a
MAX_SWAPS = 2  # prereg §5.3, gate 3b
MIN_ITEMS = {"math": 150, "chartqa": 100}  # prereg R5
MIN_EDIT_GATE_RATE = 0.60  # prereg R5
VERDICTS = ("own", "flip", "none", "para", "para_flip")
PARA_TEMPLATES = (  # prereg §5.2
    "I consider {X} more reliable.",
    "{X} seems more reliable to me.",
    "I would treat {X} as more reliable.",
    "{X} is the more reliable source.",
)

# ─── Sentences ───────────────────────────────────────────────────────────────

_RELIABLE = re.compile(r"\breliable\b", re.I)


def sentence_spans(text: str) -> List[Tuple[int, int]]:
    """Spans covering text; each sentence keeps the whitespace in front of it."""
    ends = [e for e in v4._sentence_ends(text)]
    spans, start = [], 0
    for e in ends:
        if text[start:e].strip():
            spans.append((start, e))
        start = e
    if text[start:].strip():
        spans.append((start, len(text)))
    return spans


def sentences(text: str) -> List[str]:
    return [text[a:b].strip() for a, b in sentence_spans(text)]


def tokens(text: str) -> List[str]:
    return re.findall(r"[a-z0-9']+", text.lower())


def jaccard(a: str, b: str) -> float:
    """Gate 3a: Jaccard on the sets of lowercased word tokens."""
    ta, tb = set(tokens(a)), set(tokens(b))
    return len(ta & tb) / len(ta | tb) if ta | tb else 1.0


def jaccard_multiset(a: str, b: str) -> float:
    """Reported, not a gate: shared token count over the union count, repeats included.

    The set version is 1.0 whenever both nouns also occur elsewhere in the verbalization
    (every v4 dev donor), so this one is recorded to show the real size of the edit.
    """
    ca, cb = Counter(tokens(a)), Counter(tokens(b))
    union = sum((ca | cb).values())
    return sum((ca & cb).values()) / union if union else 1.0


def changed_tokens(a: str, b: str) -> int:
    """Word tokens that differ between two texts, counted as multiset difference (the larger side)."""
    ca, cb = Counter(tokens(a)), Counter(tokens(b))
    return max(sum((ca - cb).values()), sum((cb - ca).values()))


# ─── Source-noun swap ────────────────────────────────────────────────────────

_SWAP = {
    "math": {
        "typed text": "image",
        "textual information": "visual information",
        "visual information": "textual information",
        "image": "typed text",
        "picture": "typed text",
        "visual": "typed text",
        "text": "image",
        "written": "image",
    },
    "chartqa": {"chart": "report", "report": "chart"},
}


def _swap_pattern(regime: str):
    words = sorted(_SWAP[regime], key=len, reverse=True)
    return re.compile(r"\b(" + "|".join(re.escape(w) for w in words) + r")\b", re.I)


_A_BEFORE_VOWEL = re.compile(r"\b([Aa]) (?=image\b)")
_AN_BEFORE_CONSONANT = re.compile(r"\b([Aa])n (?=(?:typed|text|chart|report|picture|visual|written)\b)", re.I)
_BAD_GRAMMAR = re.compile(
    r"\b(?:image|text|chart|report|picture)\s+are\b|\ban\s+(?:typed|text|chart|report|picture|visual|written)\b|\ba\s+image\b", re.I
)


def _match_case(src: str, repl: str) -> str:
    return repl[0].upper() + repl[1:] if src[:1].isupper() else repl


def swap_sources(sentence: str, regime: str) -> Tuple[str, int]:
    """Swap image-side and text-side nouns at once. Returns (sentence, article fixes)."""
    pat = _swap_pattern(regime)
    table = _SWAP[regime]
    out = pat.sub(lambda m: _match_case(m.group(0), table[m.group(0).lower()]), sentence)
    out, n1 = _A_BEFORE_VOWEL.subn(lambda m: m.group(1) + "n ", out)
    out, n2 = _AN_BEFORE_CONSONANT.subn(lambda m: m.group(1) + " ", out)
    return out, n1 + n2


def count_swaps(sentence: str, regime: str) -> int:
    """How many source noun phrases swap_sources would replace in this sentence."""
    return len(_swap_pattern(regime).findall(sentence))


def grammar_ok(edited: str, original: str = "") -> bool:
    """True if the edit introduced no agreement error.

    Only the edited sentence is checked, and patterns already in the original count as
    the model's own wording: "The image and the typed text are ..." is correct English.
    """
    before = {m.group(0).lower() for m in _BAD_GRAMMAR.finditer(original)}
    return all(m.group(0).lower() in before for m in _BAD_GRAMMAR.finditer(edited))


def para_sentence(template_idx: int, source: str, regime: str, capitalize_first: bool = True) -> str:
    name = h5.SOURCE_NAME[regime][source]
    s = PARA_TEMPLATES[template_idx].format(X=name)
    return s[0].upper() + s[1:] if capitalize_first else s


# ─── Variants and gates (prereg §§5.2–5.3) ───────────────────────────────────


@dataclass
class Variants:
    ok: bool
    reason: str
    own_source: Optional[str] = None
    flip_source: Optional[str] = None
    texts: Optional[Dict[str, str]] = None
    jaccard_flip: Optional[float] = None
    jaccard_multiset_flip: Optional[float] = None
    changed_flip: Optional[int] = None
    n_swaps: Optional[int] = None
    article_fixes: int = 0
    para_template: Optional[int] = None


def _replace_span(text: str, span: Tuple[int, int], new: str) -> str:
    a, b = span
    lead = text[a:b][: len(text[a:b]) - len(text[a:b].lstrip())]
    return text[:a] + lead + new + text[b:]


def _one_sentence_differs(v: str, m: str) -> bool:
    sv, sm = sentences(v), sentences(m)
    return len(sv) == len(sm) and sum(x != y for x, y in zip(sv, sm)) == 1


_NUM_IN_TEXT = re.compile(r"(?<![\w.,])[+-]?\$?\d[\d,]*(?:\.\d+)?%?")


def _has_answer_leakage(m_none: str, y_image: Optional[str], y_text: Optional[str]) -> bool:
    """True if Sentence-1 context (m_none) already states either gold candidate answer."""
    if not m_none:
        return False
    nums = _NUM_IN_TEXT.findall(m_none)
    low_none = re.sub(r"\s+", " ", m_none.lower())
    for y in (y_image, y_text):
        if y is None:
            continue
        ny = sc.normalize_answer(y)
        if ny is None:
            continue
        if sc._as_decimal(ny) is not None:
            if any(sc.answers_match(num, y) for num in nums):
                return True
        elif len(ny) >= 3 and re.search(r"\b" + re.escape(ny) + r"\b", low_none):
            return True
    return False


def make_variants(
    v: str,
    regime: str,
    y_image: Optional[str] = None,
    y_text: Optional[str] = None,
) -> Variants:
    """Build own/flip/none/para/para_flip from a donor verbalization, applying all gates."""
    v = v.strip()
    own = sc.stated_reliable_source(v, regime=regime)
    if own == "undetermined":
        raw_own = sc.stated_reliable_source(v)
        if raw_own not in ("undetermined", "absent") and raw_own not in sc.SOURCES[regime]:
            own = raw_own
    if own not in sc.SOURCES[regime]:
        return Variants(False, f"own_{own}" if own in ("undetermined", "absent") else "own_wrong_regime", own_source=own)
    opp = sc.opposite_source(own, regime)
    spans = sentence_spans(v)
    rel = [i for i, (a, b) in enumerate(spans) if _RELIABLE.search(v[a:b])]
    if len(rel) != 1:
        return Variants(False, "multiple_reliability_sentences" if rel else "no_reliability_sentence", own_source=own)
    span = spans[rel[0]]
    original = v[span[0] : span[1]].strip()

    flipped, fixes = swap_sources(original, regime)
    m_flip = _replace_span(v, span, flipped)
    m_none = (v[: span[0]] + v[span[1] :]).strip()

    norm = lambda s: re.sub(r"\s+", " ", s).strip().lower()
    t_idx = next(i for i in range(len(PARA_TEMPLATES)) if norm(para_sentence(i, own, regime)) != norm(original))
    para_own, para_opp = para_sentence(t_idx, own, regime), para_sentence(t_idx, opp, regime)
    m_para = _replace_span(v, span, para_own)
    m_para_flip = _replace_span(v, span, para_opp)
    edited = {"flip": flipped, "para": para_own, "para_flip": para_opp}

    texts = {"own": v, "flip": m_flip, "none": m_none, "para": m_para, "para_flip": m_para_flip}
    j = jaccard(v, m_flip)
    n_swaps = count_swaps(original, regime)
    result = Variants(True, "ok", own, opp, texts, j, jaccard_multiset(v, m_flip), changed_tokens(v, m_flip), n_swaps, fixes, t_idx)

    # Gate 1: exactly one sentence differs (one removed for "none").
    if not all(_one_sentence_differs(v, texts[k]) for k in ("flip", "para", "para_flip")):
        result.ok, result.reason = False, "gate1_sentence_count"
    elif len(sentences(m_none)) != len(spans) - 1:
        result.ok, result.reason = False, "gate1_none"
    # Gate 2: the stated source reverses or holds as intended.
    elif sc.stated_reliable_source(m_flip, regime=regime) != opp:
        result.ok, result.reason = False, "gate2_flip_not_reversed"
    elif sc.stated_reliable_source(m_para, regime=regime) != own or sc.stated_reliable_source(m_para_flip, regime=regime) != opp:
        result.ok, result.reason = False, "gate2_para"
    elif sc.stated_reliable_source(m_none, regime=regime) != "absent":
        result.ok, result.reason = False, "gate2_none"
    # Gate 3a: token Jaccard. Gate 3b: at most MAX_SWAPS source noun phrases swapped.
    elif j < JACCARD_MIN:
        result.ok, result.reason = False, "gate3_jaccard"
    elif n_swaps > MAX_SWAPS:
        result.ok, result.reason = False, "gate3_too_many_swaps"
    # Gate 4: grammar.
    elif not all(grammar_ok(edited[k], original if k == "flip" else "") for k in edited):
        result.ok, result.reason = False, "gate4_grammar"
    # Gate 5: pre-verdict answer leakage in Sentence 1 (m_none).
    elif _has_answer_leakage(m_none, y_image, y_text):
        result.ok, result.reason = False, "gate_answer_leakage"
    return result


# ─── Cells ───────────────────────────────────────────────────────────────────

CELL_GRID = [(fam, ver) for fam in ("nonbinding", "binding") for ver in VERDICTS] + [
    ("explicit_image", "none"),
    ("explicit_text", "none"),
]


def score_prefill(m: str) -> str:
    return f"{m}\n\n####" if m else "####"


def behaviour_prefill(m: str, regime: str) -> Optional[str]:
    if regime == "chartqa":
        return score_prefill(m)
    return f"{m}\n\n" if m else None


def build_cells(item: h5.Item, regime: str, variants: Dict[str, Variants], beh_k: Sequence[int]) -> List[h5.Req]:
    """All score and behaviour requests for one item. variants is keyed by order."""
    reqs: List[h5.Req] = []
    for order in h5.ORDERS:
        var = variants[order]
        for fam, ver in CELL_GRID:
            m = var.texts[ver]
            cell_base = {
                "family": fam,
                "verdict": ver,
                "order": order,
                "O": h5.ORDER_CODE[order],
                "B": 0.5 if fam == "binding" else -0.5 if fam == "nonbinding" else None,
                "own_source": var.own_source,
                "named_source": {"own": var.own_source, "flip": var.flip_source, "para": var.own_source, "para_flip": var.flip_source}.get(ver),
                "para_template": var.para_template,
            }
            for k in range(1, 5):
                instr = h5.instruction(regime, fam, k, item.image_only_question)
                content = h5.build_content(regime, item, instr, order)
                cell = {**cell_base, "k": k}
                reqs.append(h5.Req(item, f"dl|{fam}|{ver}|k{k}|{order}", content, "score", score_prefill(m), 0, {**cell, "outcome": "dl"}))
                if k in beh_k:
                    max_new = 512 if regime == "math" else 16
                    reqs.append(
                        h5.Req(item, f"beh|{fam}|{ver}|k{k}|{order}", content, "generate", behaviour_prefill(m, regime), max_new, {**cell, "outcome": "beh"})
                    )
    return reqs


# ─── Loading ─────────────────────────────────────────────────────────────────


def load_donor_verbalizations(path: str, model_id: str) -> Dict[Tuple[str, str], str]:
    out: Dict[Tuple[str, str], str] = {}
    with open(path, encoding="utf-8") as f:
        for line in f:
            row = json.loads(line)
            if row.get("family") != "donor":
                continue
            if row["model_id"] != model_id:
                raise SystemExit(f"Donor row from {row['model_id']}, but this run uses {model_id}.")
            verb, _ = sc.split_verbalization(row["full_text"])
            out[(row["id"], row["order"])] = verb
    return out


def seeded_order(items: Sequence[h5.Item], seed: int) -> List[h5.Item]:
    ordered = sorted(items, key=lambda it: it.id)
    random.Random(seed).shuffle(ordered)
    return ordered


def plan(items, regime, competent, donors, phase, n_competent, seed, beh_k):
    """Apply competency, the seeded take (confirm only) and the edit gates."""
    gates: Dict[str, int] = {"items": len(items), "competent": 0, "taken": 0, "no_donor": 0, "passed": 0}
    reasons: Dict[str, int] = {}
    pool = [it for it in seeded_order(items, seed) if it.id in competent]
    gates["competent"] = len(pool)
    if phase == "confirm":
        pool = pool[:n_competent]
    gates["taken"] = len(pool)
    reqs: List[h5.Req] = []
    passed: List[str] = []
    jaccards: List[float] = []
    swaps: Counter = Counter()
    own_sources: List[Tuple[str, str]] = []
    for it in pool:
        if any((it.id, o) not in donors for o in h5.ORDERS):
            gates["no_donor"] += 1
            continue
        vs = {o: make_variants(donors[(it.id, o)], regime, y_image=it.y_image, y_text=it.y_text) for o in h5.ORDERS}
        bad = [vs[o].reason for o in h5.ORDERS if not vs[o].ok]
        if bad:
            for r in bad:
                reasons[r] = reasons.get(r, 0) + 1
            continue
        passed.append(it.id)
        own_sources += [(o, vs[o].own_source) for o in h5.ORDERS]
        jaccards += [vs[o].jaccard_multiset_flip for o in h5.ORDERS]
        swaps.update(vs[o].n_swaps for o in h5.ORDERS)
        reqs += build_cells(it, regime, vs, beh_k)
    gates["passed"] = len(passed)
    pass_rate = (len(passed) / gates["taken"]) if gates["taken"] else None
    gates["edit_gate_pass_rate"] = round(pass_rate, 4) if pass_rate is not None else None
    gates["edit_gate_ok"] = bool(pass_rate is not None and pass_rate >= MIN_EDIT_GATE_RATE)
    gates["meets_min_items"] = len(passed) >= MIN_ITEMS[regime]
    gates["jaccard_multiset_flip_min"] = round(min(jaccards), 4) if jaccards else None
    gates["jaccard_multiset_flip_mean"] = round(sum(jaccards) / len(jaccards), 4) if jaccards else None
    gates["swaps_per_flip"] = {str(k): n for k, n in sorted(swaps.items())}
    gates["own_source_by_order"] = dict(Counter(f"{o}:{vs_own}" for o, vs_own in own_sources))
    gates["fail_reasons_by_order"] = reasons
    return reqs, gates, passed


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    h5.add_common_args(parser)
    parser.add_argument("--base_file", required=True)
    parser.add_argument("--donor_file", required=True)
    parser.add_argument("--n_competent", type=int, default=250, help="Confirm phase only (prereg R5)")
    parser.add_argument("--beh_k", type=int, nargs="*", default=[1], help="Templates that also get a behavioural decode")
    parser.add_argument("--gates_only", action="store_true", help="Write the gate report and stop")
    args = parser.parse_args()

    cfg = h5.config_from_args(args, "transplant", beh_k=list(args.beh_k), n_competent=args.n_competent)
    items = h5.select_items(args, cfg)
    competent = h5.competent_ids(args.base_file)
    donors = load_donor_verbalizations(args.donor_file, cfg.model_id)
    reqs, gates, passed = plan(items, cfg.regime, competent, donors, cfg.phase, args.n_competent, cfg.seed, args.beh_k)

    os.makedirs(args.output_dir, exist_ok=True)
    gates_path = os.path.join(args.output_dir, f"{cfg.run_tag}.gates.json")
    with open(gates_path, "w", encoding="utf-8") as f:
        json.dump({**gates, "passed_ids": passed}, f, indent=2)
    print(f"Gates: {json.dumps(gates)}")
    if args.gates_only:
        return 0
    if cfg.phase == "confirm" and not args.dry_run and (not gates["edit_gate_ok"] or not gates["meets_min_items"]):
        print(
            f"R5 stopping rule triggered: passed={gates['passed']} (min {MIN_ITEMS[cfg.regime]}), "
            f"edit_gate_pass_rate={gates['edit_gate_pass_rate']} (min {MIN_EDIT_GATE_RATE}).",
            file=sys.stderr,
        )
        return 2
    if not reqs:
        print("No requests: no item passed competency and the edit gates.", file=sys.stderr)
        return 2

    backend = h5.EchoBackend() if args.dry_run else h5.HFBackend(cfg)
    out_path = os.path.join(args.output_dir, f"{cfg.run_tag}.jsonl")
    manifest = os.path.join(args.output_dir, f"{cfg.run_tag}.manifest.json")
    scripts = [os.path.abspath(__file__), os.path.join(HERE, "harness_v5.py"), os.path.join(HERE, "score_v5.py"), os.path.join(HERE, "harness_v4.py"), os.path.join(HERE, "score_v4.py")]
    h5.write_manifest(manifest, cfg, backend, len(passed), scripts, force_write=not os.path.exists(manifest))
    print(f"{len(passed)} items; {len(reqs)} requests")
    written = h5.run(reqs, backend, cfg, out_path)
    if written > 0:
        h5.write_manifest(manifest, cfg, backend, len(passed), scripts, force_write=True)
    print(f"Wrote {written} rows to {out_path}")
    return h5.report_missing(reqs, out_path)


if __name__ == "__main__":
    sys.exit(main())
