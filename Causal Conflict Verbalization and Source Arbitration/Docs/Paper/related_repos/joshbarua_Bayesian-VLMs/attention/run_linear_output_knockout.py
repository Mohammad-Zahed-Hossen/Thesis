#!/usr/bin/env python3
"""Readout-only output knockout for Qwen3.5 linear-attention layers.

Qwen3.5 interleaves full-softmax attention with GatedDeltaNet linear
attention.  A source-span knockout is well-defined only for the former: the
linear layers expose no tokenwise attention row whose image or passage logits
can be masked.  This experiment therefore asks a deliberately different
question:

    How much does the *aggregate linear-attention write at the answer readout*
    matter in each reliability context?

For every selected linear-attention layer, the module output at the answer
readout position is set to zero immediately before the residual add.  Other
positions are untouched, so the intervention does not erase the source's
earlier recurrent-state updates or its relays into passage/question states.
It removes only the direct linear-attention-family write into the readout.

The sweep uses the same cells and whole-stack default as ``run_knockout.py``:

    C = (I_clean,    T_clean)
    V = (I_degraded, T_clean)
    T = (I_clean,    T_degraded)

and reports ``delta = s_knockout - s_base`` for
``s = logit(a_T) - logit(a_V)``.  The prediction is context-sensitive rather
than modality-independent: if linear attention behaves like a multimodal
relay, its signed effect should differ between T and V.

An identity intervention (scale the same writes by exactly one) is run for
every cell/block.  ``identity_delta`` must be zero, which proves that any
knockout effect comes from removing the write rather than from the hook path.

Output: ``runs/<run_id>/linear_output_knockout[_shard_i].parquet``.
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
from attention import stimuli
from attention.patch_hooks import (BlockPorts, ScaleAttentionWrites,
                                    get_layers)
from attention.run_knockout import _blocks


def _linear_layers(model, adapter) -> list[int]:
    """Return 1-based layers whose token mixer is explicitly ``linear_attn``."""
    out = []
    for ell, layer in enumerate(get_layers(model, adapter), start=1):
        if BlockPorts(layer).attn_module_name == "linear_attn":
            out.append(ell)
    return out


@torch.no_grad()
def _forward(setup, mi, layers: list[int], scale: float | None):
    model = setup.model
    inp = move_to_device(mi.inputs, model.device)
    r = int(mi.answer_pos)
    setup.readout.bind(mi)

    hook = None
    if scale is not None and layers:
        hook = ScaleAttentionWrites(layers, [r], scale=scale,
                                    adapter=setup.adapter).attach(model)
    try:
        out = ro.forward(model, inp)
    finally:
        if hook is not None:
            hook.remove()
    score = float(setup.readout.score(out, r).s)
    rms = (sum(hook.rms.values()) / len(hook.rms)
           if hook is not None and hook.rms else float("nan"))
    return score, float(rms)


def sweep_example(setup, ex, ds_name, loc, args, blocks, linear_layers):
    sig = float(setup.meta["blur_sigmas"][args.image_level])
    img_d = stimuli.blur(ex["image"], sig)
    try:
        txt_d = setup.builder.variants.passage(ds_name, loc, args.text_level,
                                               ex["text"])
    except Exception:
        return None, "text_variant_failed"

    builder = setup.builder
    cells = {
        "C": builder.build_cell(ex, ex["image"], ex["text"]),
        "V": builder.build_cell(ex, img_d, ex["text"]),
        "T": builder.build_cell(ex, ex["image"], txt_d),
    }
    cells = {name: mi for name, mi in cells.items() if mi is not None}
    if "C" not in cells:
        return None, "clean_cell_failed"

    linear_set = set(linear_layers)
    rows = []
    for cell, mi in cells.items():
        for block, requested in blocks:
            affected = [ell for ell in requested if ell in linear_set]
            if not affected:
                continue
            # Plain and scale-one runs are both retained: the latter exercises
            # exactly the same multi-hook path as the knockout.
            s_plain, _ = _forward(setup, mi, affected, None)
            s_base, write_rms = _forward(setup, mi, affected, 1.0)
            s_ko, _ = _forward(setup, mi, affected, 0.0)
            rows.append({
                "id": int(setup._idx), "dataset": ds_name,
                "cell": cell, "block": block,
                "layer_lo": int(requested[0]),
                "layer_hi": int(requested[-1]),
                "n_layers_requested": int(len(requested)),
                "n_layers_blocked": int(len(affected)),
                "linear_layers": ",".join(map(str, affected)),
                "s_plain": float(s_plain), "s_base": float(s_base),
                "s": float(s_ko), "delta": float(s_ko - s_base),
                "identity_delta": float(s_base - s_plain),
                "write_rms_mean": float(write_rms),
                "img_level": int(args.image_level),
                "txt_level": int(args.text_level),
            })
    return rows, None


def main():
    ap = argparse.ArgumentParser(
        description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    runner.add_common_args(ap)
    ap.add_argument("--image_level", type=int, default=4,
                    help="Grid index for degraded image (4 = sigma 16).")
    ap.add_argument("--text_level", type=int, default=4,
                    help="Grid index for degraded text (4 = p 0.80).")
    ap.add_argument("--blocks", type=str, default=None,
                    help="Override blocks, e.g. 'early:1-10,late:21-32'.")
    args = ap.parse_args()

    setup = runner.prepare(args)
    linear_layers = _linear_layers(setup.model, setup.adapter)
    if not linear_layers:
        raise RuntimeError(
            "model exposes no linear_attn layers; this experiment is defined "
            "only for a hybrid/linear-attention stack")
    blocks = _blocks(setup.n_layers, args.blocks)
    linear_set = set(linear_layers)
    print(f"Linear-attention layers ({len(linear_layers)}/{setup.n_layers}): "
          f"{linear_layers}")
    print("Blocks: " + ", ".join(
        f"{name}={layers[0]}-{layers[-1]} "
        f"({len([e for e in layers if e in linear_set])} linear)"
        for name, layers in blocks))

    writer = runner.ShardedWriter(
        setup.run_dir, "linear_output_knockout", shard_id=args.shard_id,
        checkpoint_every=args.checkpoint_every, overwrite=args.overwrite)
    if writer.already_complete():
        print(f"Already complete: {writer.out_path}. Pass --overwrite to rerun.")
        return
    writer.open()

    skipped = []
    pending = writer.pending(setup.ids)
    for i, idx in enumerate(tqdm(pending, desc="linear output knockout")):
        ex, ds_name, loc = setup.example(int(idx))
        if setup.builder.skippable(ex):
            skipped.append({"id": int(idx), "reason": "answer_degenerate"})
            continue
        setup._idx = int(idx)
        try:
            rows, reason = sweep_example(setup, ex, ds_name, loc, args,
                                         blocks, linear_layers)
        except Exception as exc:                 # noqa: BLE001 - recorded
            skipped.append({"id": int(idx),
                            "reason": f"{type(exc).__name__}: {exc}"})
            continue
        if rows:
            writer.add(rows)
            writer.maybe_flush(i)
        elif reason:
            skipped.append({"id": int(idx), "reason": reason})

    writer.finalize(runner.run_meta(setup, {
        "experiment": "linear_output_knockout",
        "intervention": "scale linear-attention residual write at readout to 0",
        "image_level": args.image_level, "text_level": args.text_level,
        "blocks": {name: [layers[0], layers[-1]]
                   for name, layers in blocks},
        "linear_layers": linear_layers,
        "skipped": skipped,
    }))


if __name__ == "__main__":
    main()
