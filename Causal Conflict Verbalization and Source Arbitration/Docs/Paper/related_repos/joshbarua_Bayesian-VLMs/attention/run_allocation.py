#!/usr/bin/env python3
"""Readout attention-allocation surface over the (blur, text-noise) grid.

A cheap, correlational measurement that operationalizes "rerouting": at the
answer readout position, how is the softmax attention mass split across source
spans -- image / passage / question / other -- and how does that split respond
to **both** modalities' reliability?

For every grid cell ``(sigma, p)`` and every softmax-attention layer, this
records the readout's attention mass to each span, averaged over heads:

    A_S = mean_h sum_{j in S} A^{l,h}_{r,j},        S in {image, passage,
                                                          question, other}

with ``A_image + A_passage + A_question + A_other == 1`` per head (the four
spans partition the positions the readout can attend to). The joint preference
``s_J`` is recorded alongside each cell for context.

This unifies two earlier threads into one surface:

* Experiment 5 found the readout re-weights attention over the passage as the
  **image's** own reliability changes (routing responds to image blur);
* the Experiment 6 sub-pathway result found the image-attention contribution
  responds to the **text's** reliability.

If attention allocation over sources tracks *relative* reliability -- image
share falling as the image is blurred, and rising again as the competing text
is degraded -- then the reliability weighting is implemented at the point of
use, as the readout's attention allocation, and this surface locates it.

Notes.

* Attention mass is a pre-gate softmax quantity and is exact on output-gated
  architectures.
* **Hybrid stacks:** only the softmax-attention layers are measured; the
  linear-attention layers have no attention weights to report.
* Purely correlational -- no patching, one forward per cell.

Output: ``runs/<run_id>/allocation[_shard_i].parquet``.
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
from attention.attn_spans import SpanAttention

SPANS = ("image", "passage", "question", "other")


@torch.no_grad()
def sweep_example(setup, sa, ex, ds_name, loc, blur_sigmas, text_levels,
                  variants) -> tuple[list[dict], int]:
    model, adapter = setup.model, setup.adapter
    rows: list[dict] = []
    n_cells = 0
    for k, sigma in enumerate(blur_sigmas):
        img = stimuli.blur(ex["image"], float(sigma))
        for m in text_levels:
            try:
                passage = (ex["text"] if m == 0
                           else variants.passage(ds_name, loc, m, ex["text"]))
            except Exception:
                continue
            try:
                mi = setup.builder.build_cell(ex, img, passage)
            except Exception:
                continue
            if mi is None:
                continue
            try:
                spans = sp.build_spans(adapter, mi, ex["question"])
            except Exception:
                continue
            r = int(mi.answer_pos)
            setup.readout.bind(mi)
            sa.bind(spans.as_dict(), q_index=r)
            sa.arm(capture=True, want_rows=True)
            try:
                out = ro.forward(model, move_to_device(mi.inputs, model.device))
            finally:
                sa.disarm()
            s_J = setup.readout.score(out, r).s
            cap = sa.take_capture()
            n_cells += 1
            for L in sa.layers:
                rec = cap[L]
                mass = {}
                for name in SPANS:
                    a = rec.a_span.get(name)
                    # a: [H, |S|] attention row restricted to the span; sum over
                    # the span, then average over heads -> mean attention frac.
                    mass[name] = (float(a.sum(-1).mean()) if a is not None
                                  and a.numel() else 0.0)
                total = sum(mass.values())
                rows.append({
                    "id": int(setup._idx), "dataset": ds_name,
                    "blur_level": int(k), "text_level": int(m),
                    "blur_sigma": float(sigma), "layer": int(L),
                    "attention_type": sa.layer_types[L],
                    "sliding_window": sa.sliding_windows[L],
                    "A_image": mass["image"], "A_passage": mass["passage"],
                    "A_question": mass["question"], "A_other": mass["other"],
                    "A_total": float(total),         # should be ~1 (sanity)
                    "s_J": float(s_J),
                    "question_located": bool(spans.question_located),
                })
            cap.clear()
    return rows, n_cells


def main():
    ap = argparse.ArgumentParser(
        description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    runner.add_common_args(ap)
    args = ap.parse_args()

    setup = runner.prepare(args)
    blur_sigmas = list(setup.meta["blur_sigmas"])
    text_levels = list(setup.meta["text_levels"])
    grid = setup.meta["grid"]
    variants = stimuli.TextVariants(grid)
    print(f"Grid {grid}: blur={blur_sigmas} x text_levels={text_levels} "
          f"= {len(blur_sigmas) * len(text_levels)} cells/example")

    writer = runner.ShardedWriter(setup.run_dir, "allocation",
                                  shard_id=args.shard_id,
                                  checkpoint_every=args.checkpoint_every,
                                  overwrite=args.overwrite)
    if writer.already_complete():
        print(f"Already complete: {writer.out_path}. Pass --overwrite to rerun.")
        return
    writer.open()

    sa = SpanAttention(setup.model, setup.adapter,
                       list(range(1, setup.n_layers + 1))).attach()
    print(f"Measuring attention allocation on softmax layers {sa.layers}"
          f"{' (gated arch; mass is pre-gate and exact)' if sa.gated else ''}")

    skipped: list[dict] = []
    pending = writer.pending(setup.ids)
    try:
        for i, idx in enumerate(tqdm(pending, desc="allocation")):
            ex, ds_name, loc = setup.example(int(idx))
            if setup.builder.skippable(ex):
                skipped.append({"id": int(idx), "reason": "answer_degenerate"})
                continue
            setup._idx = int(idx)
            try:
                rows, n_cells = sweep_example(setup, sa, ex, ds_name, loc,
                                              blur_sigmas, text_levels, variants)
            except Exception as e:                 # noqa: BLE001 - recorded
                skipped.append({"id": int(idx),
                                "reason": f"{type(e).__name__}: {e}"})
                continue
            if rows:
                writer.add(rows)
            else:
                skipped.append({"id": int(idx), "reason": "no_cells"})
            writer.maybe_flush(i)
    finally:
        sa.remove()

    writer.finalize(runner.run_meta(setup, {
        "experiment": "allocation",
        "grid": grid, "blur_sigmas": blur_sigmas, "text_levels": text_levels,
        "gated_attention": bool(sa.gated),
        "softmax_layers": sa.layers,
        "attention_layer_types": sa.layer_types,
        "sliding_windows": sa.sliding_windows,
        "n_skipped": len(skipped), "skipped": skipped[:200],
    }))


if __name__ == "__main__":
    main()
