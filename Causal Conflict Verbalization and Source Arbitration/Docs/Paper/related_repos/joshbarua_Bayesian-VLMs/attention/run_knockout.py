#!/usr/bin/env python3
"""Attention knockout: block the readout from attending to a source span.

Does the readout still need to *look* at the evidence late in the stack, or has
what it needs already been written into its own residual stream by then? This
blocks the readout's attention to one source span -- image, passage, or
question -- across a block of layers, and reads the change in the answer
preference

    s = logit(a_T) - logit(a_V)

at the first divergent token, the same readout every other experiment here uses.

Every attention logit belonging to the blocked span is set to ``-inf`` at the
readout row before the softmax, so the span gets exactly zero mass and the
freed mass is redistributed over the surviving positions in proportion to what
they already had. Values are untouched, surviving spans keep their internal
patterns, and every non-readout query position is left alone.

**Read the result as a statement about the direct route only.** Blocking the
image span at the readout does not remove the image's influence: by the time
the late layers run, image-conditioned information has already been written
into the passage and question positions' hidden states, and the readout can
still attend to those. This package's cumulative results already found that
under image degradation the readout recovers only ~0.31 of the transition from
image-source attention but ~0.97 from all sources -- most of the visual signal
arrives through textual relay positions. So a small image knockout effect is
evidence that the *direct* image route is not what carries the decision, not
evidence that the image does not matter. The ``question`` span is informative
partly for this reason: it is a relay carrier whose own tokens are fixed.

By default the intervention covers the whole stack, matching the paper table.
``--blocks`` can optionally request diagnostic subranges.

Cells. The knockout runs in several reliability conditions, because "does
attention to the evidence matter" plausibly has different answers when that
evidence is good and when it is not:

    C  = (I_clean,    T_clean)
    V  = (I_degraded, T_clean)        image degraded
    T  = (I_clean,    T_degraded)     text degraded

Each row carries the unblocked baseline ``s_base`` taken through the *same*
eager attention path, so the fused-kernel difference cancels out of the
reported effect, plus the mass the blocked span actually held before it was
blocked -- an effect can only be as large as the allocation it removed, and a
span holding ~0 mass that produces a large effect is a bug, not a finding.

The exactness control is ``span='none'``: the identical code path with an empty
block set, which must reproduce the baseline.

Output: ``runs/<run_id>/knockout[_shard_i].parquet``.

Usage::

    python attention/run_knockout.py --run_id act_Qwen2.5-VL-3B-Instruct \\
        --deg_run_id deg_Qwen2.5-VL-3B-Instruct-normalized-token-noise \\
        --n_examples 80
"""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

import torch
from tqdm import tqdm

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from attention.model_loader import move_to_device

from attention import readout as ro
from attention import runner
from attention import spans as sp
from attention import stimuli
from attention.attn_spans import KnockoutPlan, SpanAttention

SPANS = ("image", "passage", "question")


def _blocks(n_layers: int, spec: str | None) -> list[tuple[str, list[int]]]:
    """Named contiguous layer blocks, 1-based and inclusive."""
    if spec:
        out = []
        for tok in spec.split(","):
            name, rng = tok.split(":", 1) if ":" in tok else (tok, tok)
            lo, hi = (rng.split("-", 1) if "-" in rng else (rng, rng))
            out.append((name.strip(), list(range(int(lo), int(hi) + 1))))
        return out
    return [("all", list(range(1, n_layers + 1)))]


@torch.no_grad()
def _forward(setup, sa, mi, question, block_spans, layers):
    """One forward with ``block_spans`` blocked over ``layers``.

    ``block_spans`` empty runs the identical path with nothing blocked, which
    is the baseline every effect is differenced against -- taken through the
    eager attention implementation so the fused-kernel gap cancels.
    """
    model, adapter = setup.model, setup.adapter
    inp = move_to_device(mi.inputs, model.device)
    r = int(mi.answer_pos)
    spans = sp.build_spans(adapter, mi, question)
    setup.readout.bind(mi)
    sa.bind(spans.as_dict(), q_index=r)
    plan = {ell: KnockoutPlan(spans=tuple(block_spans))
            for ell in layers if ell in set(sa.layers)}
    sa.arm(capture=True, want_rows=True, knockout_plan=plan or None)
    try:
        out = ro.forward(model, inp)
    finally:
        sa.disarm()
    s = float(setup.readout.score(out, r).s)
    cap = sa.take_capture()
    # Mass per span averaged over heads then over the affected layers: what the
    # block removed (or, on the baseline, what was there to remove).
    mass = {}
    for name in SPANS:
        vals = [float(cap[e].a_span[name].sum(-1).mean())
                for e in layers if e in cap and name in cap[e].a_span
                and cap[e].a_span[name].numel()]
        mass[name] = sum(vals) / len(vals) if vals else float("nan")
    cap.clear()
    return s, mass, spans


def sweep_example(setup, sa, ex, ds_name, loc, args, blocks):
    sig = float(setup.meta["blur_sigmas"][args.image_level])
    img_d = stimuli.blur(ex["image"], sig)
    try:
        txt_d = setup.builder.variants.passage(ds_name, loc, args.text_level,
                                               ex["text"])
    except Exception:
        return None, "text_variant_failed"
    B, q = setup.builder, ex["question"]
    cells = {"C": B.build_cell(ex, ex["image"], ex["text"]),
             "V": B.build_cell(ex, img_d, ex["text"]),
             "T": B.build_cell(ex, ex["image"], txt_d)}
    cells = {k: v for k, v in cells.items() if v is not None}
    if "C" not in cells:
        return None, "clean_cell_failed"

    rows = []
    for cell, mi in cells.items():
        for bname, layers in blocks:
            # Baseline per (cell, block): the same eager path with nothing
            # blocked. It does not depend on the block, but recording it per
            # block keeps every row self-contained for the analysis.
            s_base, mass_base, spans = _forward(setup, sa, mi, q, (), layers)
            for span in ("none",) + SPANS:
                if span == "none":
                    s_ko, mass_ko = s_base, mass_base
                else:
                    if not getattr(spans, span, None):
                        continue
                    s_ko, mass_ko, _ = _forward(setup, sa, mi, q, (span,),
                                                layers)
                rows.append({
                    "id": int(setup._idx), "dataset": ds_name,
                    "cell": cell, "block": bname,
                    "layer_lo": int(layers[0]), "layer_hi": int(layers[-1]),
                    "n_layers_blocked": len([e for e in layers
                                             if e in set(sa.layers)]),
                    "span": span,
                    "s_base": float(s_base), "s": float(s_ko),
                    "delta": float(s_ko - s_base),
                    # How much allocation the block actually removed. An effect
                    # cannot exceed what this took away; a large delta from a
                    # near-zero mass is a wiring bug.
                    "mass_removed": float(mass_base.get(span, float("nan")))
                    if span != "none" else 0.0,
                    "A_image": mass_base["image"],
                    "A_passage": mass_base["passage"],
                    "A_question": mass_base["question"],
                    "img_level": int(args.image_level),
                    "txt_level": int(args.text_level),
                    "question_located": bool(spans.question_located),
                })
    return rows, None


def main():
    ap = argparse.ArgumentParser(
        description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    runner.add_common_args(ap)
    ap.add_argument("--image_level", type=int, default=4,
                    help="Grid index for the degraded image (4 = sigma 16).")
    ap.add_argument("--text_level", type=int, default=4,
                    help="Grid index for the degraded text (4 = p 0.80).")
    ap.add_argument("--blocks", type=str, default=None,
                    help="Override the layer blocks, e.g. "
                         "'early:1-12,late:25-36'. Default splits the stack "
                         "into thirds plus 'all'.")
    args = ap.parse_args()

    setup = runner.prepare(args)
    blocks = _blocks(setup.n_layers, args.blocks)

    writer = runner.ShardedWriter(setup.run_dir, "knockout",
                                  shard_id=args.shard_id,
                                  checkpoint_every=args.checkpoint_every,
                                  overwrite=args.overwrite)
    if writer.already_complete():
        print(f"Already complete: {writer.out_path}. Pass --overwrite to rerun.")
        return
    writer.open()

    sa = SpanAttention(setup.model, setup.adapter,
                       list(range(1, setup.n_layers + 1))).attach()
    print("Blocks: " + ", ".join(
        f"{n}={b[0]}-{b[-1]} ({len([e for e in b if e in set(sa.layers)])} "
        f"softmax)" for n, b in blocks))
    if len(sa.layers) < setup.n_layers:
        print(f"NOTE: only {len(sa.layers)} of {setup.n_layers} layers have "
              f"softmax attention; the rest cannot be blocked and pass "
              f"through untouched.")

    skipped: list[dict] = []
    pending = writer.pending(setup.ids)
    try:
        for i, idx in enumerate(tqdm(pending, desc="knockout")):
            ex, ds_name, loc = setup.example(int(idx))
            if setup.builder.skippable(ex):
                skipped.append({"id": int(idx), "reason": "answer_degenerate"})
                continue
            setup._idx, setup._question = int(idx), ex["question"]
            try:
                rows, reason = sweep_example(setup, sa, ex, ds_name, loc,
                                             args, blocks)
            except Exception as e:                 # noqa: BLE001 - recorded
                skipped.append({"id": int(idx),
                                "reason": f"{type(e).__name__}: {e}"})
                continue
            if rows:
                writer.add(rows)
                writer.maybe_flush(i)
            elif reason:
                skipped.append({"id": int(idx), "reason": reason})
    finally:
        sa.remove()

    writer.finalize(runner.run_meta(setup, {
        "experiment": "knockout",
        "intervention_scope": "softmax_attention_layers_only",
        "image_level": args.image_level, "text_level": args.text_level,
        "blocks": {n: [b[0], b[-1]] for n, b in blocks},
        "softmax_block_layers": {
            n: [ell for ell in b if ell in set(sa.layers)]
            for n, b in blocks
        },
        "softmax_layers": list(sa.layers),
        "attention_layer_types": sa.layer_types,
        "sliding_windows": sa.sliding_windows,
        "gated_attention": bool(sa.gated),
        "skipped": skipped,
    }))


if __name__ == "__main__":
    main()
