#!/usr/bin/env python3
"""Generate open-ended MCQ answers across the full (blur, text-noise) grid.

For each sampled example, every degradation cell (sigma, p) is presented
twice with the candidate answers (a_T, a_V) in opposite (A)/(B) orders,
greedy-decoded with up to ``--max_new_tokens`` new tokens. The parsed
A/B selection is mapped back to ``picks text`` vs ``picks vision`` so
that the open-ended choice can be compared to ``sign(s_J)`` from the
companion ``runs/<deg_run>/degradation_scores.parquet``.

Output: a sharded parquet ``mcq_generations_shard_<id>.parquet`` per
worker, with one row per (example, sigma, p, position) trial. Use
``mcq/analysis.py`` to merge and report position-debiased agreement.
"""

from __future__ import annotations

import argparse
import json
import random
import re
import sys
from pathlib import Path

import numpy as np
import pandas as pd
import torch
from datasets import load_from_disk
from tqdm import tqdm

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from config import (
    HF_CACHE_DIR,
    QWEN_MODEL,
    get_run_dir,
    get_token_noise_probs,
)
from scoring.degradation import (
    blur_image,
    get_grid_config,
    load_text_variants,
)
from scoring.vlm_scorer import _maybe_promote_patch_embed_to_fp32
from transformers import AutoModelForImageTextToText, AutoProcessor


BOXED_RE = re.compile(r"\\boxed\{\s*([AaBb])\s*\}")
PAREN_RE = re.compile(r"\(\s*([AaBb])\s*\)")
WORD_RE = re.compile(r"\b([AB])\b")


def parse_choice(text: str) -> tuple[str | None, str]:
    """Return (letter, source) where letter ∈ {'A','B'}.

    Prefers, in order: \\boxed{A|B}, parenthesised (A)/(B), word A/B.
    """
    m = list(BOXED_RE.finditer(text))
    if m:
        return m[-1].group(1).upper(), "boxed"
    m = list(PAREN_RE.finditer(text))
    if m:
        return m[-1].group(1).upper(), "paren"
    m = list(WORD_RE.finditer(text))
    if m:
        return m[-1].group(1), "word"
    return None, "none"


def build_mcq_prompt(text: str, question: str, ans_a: str, ans_b: str) -> str:
    return (
        f"{text}\n"
        f"Question: {question}\n\n"
        f"Choose the best answer from the options below.\n"
        f"(A) {ans_a}\n"
        f"(B) {ans_b}\n\n"
        f"First, explain your reasoning in a few sentences. "
        f"Then, on a new line, write your final answer as a single "
        f"letter: A or B."
    )


# Text-only demonstrations balanced across A and B (alternating order
# B/A/B/A so the model sees both letters near the test turn). The goal
# is to teach the format -- reason about the content, then emit the
# letter that matches -- without contaminating the test distribution.
# `--few_shot_n` selects how many of these to prepend.
FEW_SHOT_DEMOS = [
    {
        "user": (
            "Question: Which planet in our solar system is known as the "
            "Red Planet?\n\n"
            "Choose the best answer from the options below.\n"
            "(A) Mars\n"
            "(B) Jupiter\n\n"
            "First, explain your reasoning in a few sentences. "
            "Then, on a new line, write your final answer as a single "
            "letter: A or B."
        ),
        "assistant": (
            "Mars appears red because its surface contains iron oxide "
            "(rust), which gives it a reddish hue when viewed from Earth "
            "or by spacecraft. Jupiter, in contrast, is a gas giant with "
            "alternating bands of brown, white, and orange clouds. The "
            "planet known as the Red Planet is therefore Mars, which is "
            "option A.\n\n"
            "A"
        ),
    },
    {
        "user": (
            "Question: How many sides does a hexagon have?\n\n"
            "Choose the best answer from the options below.\n"
            "(A) Five\n"
            "(B) Six\n\n"
            "First, explain your reasoning in a few sentences. "
            "Then, on a new line, write your final answer as a single "
            "letter: A or B."
        ),
        "assistant": (
            "The prefix \"hex-\" derives from the Greek word for six, and "
            "a hexagon is by definition a six-sided polygon (common "
            "example: a honeycomb cell). A five-sided polygon is called "
            "a pentagon. A hexagon therefore has six sides, which is "
            "option B.\n\n"
            "B"
        ),
    },
    {
        "user": (
            "Question: What is the chemical formula for water?\n\n"
            "Choose the best answer from the options below.\n"
            "(A) H2O\n"
            "(B) CO2\n\n"
            "First, explain your reasoning in a few sentences. "
            "Then, on a new line, write your final answer as a single "
            "letter: A or B."
        ),
        "assistant": (
            "Water consists of two hydrogen atoms bonded to one oxygen "
            "atom, giving the formula H2O. CO2 is carbon dioxide, the "
            "gas exhaled by animals and absorbed by plants. The chemical "
            "formula for water is therefore H2O, which is option A.\n\n"
            "A"
        ),
    },
    {
        "user": (
            "Question: Which is the largest ocean on Earth by surface area?\n\n"
            "Choose the best answer from the options below.\n"
            "(A) Atlantic\n"
            "(B) Pacific\n\n"
            "First, explain your reasoning in a few sentences. "
            "Then, on a new line, write your final answer as a single "
            "letter: A or B."
        ),
        "assistant": (
            "The Pacific Ocean covers approximately 63 million square "
            "miles, making it by far the largest ocean. The Atlantic "
            "Ocean is the second largest at about 41 million square "
            "miles. The largest ocean by surface area is therefore the "
            "Pacific, which is option B.\n\n"
            "B"
        ),
    },
]


def few_shot_messages(n: int) -> list[dict]:
    """Return alternating (user, assistant) message dicts for the first
    ``n`` FEW_SHOT_DEMOS, each with text-only content."""
    out: list[dict] = []
    for demo in FEW_SHOT_DEMOS[:n]:
        out.append({
            "role": "user",
            "content": [{"type": "text", "text": demo["user"]}],
        })
        out.append({
            "role": "assistant",
            "content": [{"type": "text", "text": demo["assistant"]}],
        })
    return out


def sample_balanced_ids(
    dataset_path: Path,
    n_per_dataset: int,
    seed: int,
) -> list[int]:
    """Return a deterministic list of global ids: ``n_per_dataset`` per
    split, in sorted-split order (matches the scoring parquet's global
    id assignment).
    """
    ds_dict = load_from_disk(str(dataset_path))
    split_order = sorted(ds_dict.keys())
    rng = np.random.RandomState(seed)

    selected = []
    offset = 0
    for split_name in split_order:
        n = len(ds_dict[split_name])
        local = rng.choice(n, size=min(n_per_dataset, n), replace=False)
        for i in local:
            selected.append(offset + int(i))
        offset += n
    return sorted(selected)


def load_examples(dataset_path: Path) -> dict[int, dict]:
    """Global-id -> example dict using sorted-split iteration."""
    ds_dict = load_from_disk(str(dataset_path))
    out = {}
    offset = 0
    for split_name in sorted(ds_dict.keys()):
        for i, ex in enumerate(ds_dict[split_name]):
            out[offset + i] = ex
        offset += len(ds_dict[split_name])
    return out


def load_all_text_variants(
    dataset_path: Path,
    text_degradation: str,
    grid: str,
) -> dict[int, list[str]]:
    """For each global id, return a list of text variants (length
    ``n_text_levels``: index 0 = original, indices 1.. = degraded).
    """
    ds_dict = load_from_disk(str(dataset_path))
    n_token_probs = sum(1 for p in get_token_noise_probs(grid) if p > 0)
    out: dict[int, list[str]] = {}
    offset = 0
    for split_name in sorted(ds_dict.keys()):
        split_degs = load_text_variants(text_degradation, split_name, grid)
        ds = ds_dict[split_name]
        for i, ex in enumerate(ds):
            variants = [ex["text"]]
            deg = split_degs.get(str(i))
            if deg:
                vals = list(deg)[:n_token_probs]
                if len(vals) < n_token_probs:
                    vals.extend([vals[-1] if vals else ex["text"]] *
                                (n_token_probs - len(vals)))
                variants.extend(vals)
            else:
                variants.extend([ex["text"]] * n_token_probs)
            out[offset + i] = variants
        offset += len(ds)
    return out


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--run_id", type=str, required=True)
    parser.add_argument("--model_name", type=str, default=QWEN_MODEL)
    parser.add_argument(
        "--dataset_path", type=Path, required=True,
        help="Local HF DatasetDict matching the scores parquet "
             "(e.g. dataset_pixnorm).",
    )
    parser.add_argument("--n_per_dataset", type=int, default=100)
    parser.add_argument("--grid", type=str, default="6x6",
                        choices=["6x6"])
    parser.add_argument("--text_degradation", type=str, default="token_noise",
                        choices=["token_noise"])
    parser.add_argument("--max_new_tokens", type=int, default=512)
    parser.add_argument("--seed", type=int, default=42)
    parser.add_argument("--shard_id", type=int, default=0)
    parser.add_argument("--num_shards", type=int, default=1)
    parser.add_argument("--limit", type=int, default=None,
                        help="If set, only run first N (example, cell, pos) "
                             "trials assigned to this shard.")
    parser.add_argument("--checkpoint_every", type=int, default=200,
                        help="Persist shard parquet every N trials.")
    parser.add_argument("--few_shot_n", type=int, default=0,
                        help="If >0, prepend this many text-only "
                             "demonstrations from FEW_SHOT_DEMOS so the "
                             "model sees the reasoning -> letter format "
                             "before the test turn. Max 4.")
    args = parser.parse_args()

    random.seed(args.seed)
    np.random.seed(args.seed)
    torch.manual_seed(args.seed)

    run_dir = get_run_dir(args.run_id)
    run_dir.mkdir(parents=True, exist_ok=True)
    print(f"Run dir: {run_dir}")

    blur_sigmas, text_levels, text_labels = get_grid_config(
        args.grid, args.text_degradation,
    )
    n_blur = len(blur_sigmas)
    n_text = len(text_levels)
    cells = [(k, m) for k in range(n_blur) for m in range(n_text)]
    print(f"Grid: {args.grid} -- {n_blur} blur sigmas, {n_text} text levels, "
          f"{len(cells)} cells")

    # Persist run metadata on shard 0 only (avoid races)
    if args.shard_id == 0:
        meta = {
            "model_name": args.model_name,
            "grid": args.grid,
            "text_degradation": args.text_degradation,
            "blur_sigmas": list(blur_sigmas),
            "text_levels": list(text_levels),
            "text_labels": list(text_labels),
            "n_per_dataset": args.n_per_dataset,
            "seed": args.seed,
            "max_new_tokens": args.max_new_tokens,
            "few_shot_n": args.few_shot_n,
        }
        with open(run_dir / "meta.json", "w") as f:
            json.dump(meta, f, indent=2)

    selected_ids = sample_balanced_ids(args.dataset_path, args.n_per_dataset, args.seed)
    print(f"Sampled {len(selected_ids)} unique example ids "
          f"({args.n_per_dataset}/dataset target)")

    # Shard by example id (each shard handles a slice of ids, processing
    # all cells x positions for them).
    shard_ids = selected_ids[args.shard_id::args.num_shards]
    print(f"Shard {args.shard_id}/{args.num_shards}: {len(shard_ids)} ids")

    print(f"Loading dataset from {args.dataset_path}")
    examples_by_id = load_examples(args.dataset_path)
    print(f"  loaded {len(examples_by_id)} examples")

    print(f"Loading text variants ({args.text_degradation}, {args.grid})")
    text_variants_by_id = load_all_text_variants(
        args.dataset_path, args.text_degradation, args.grid,
    )

    # Trial plan: for each id, iterate (cell, position) so checkpoints
    # land at predictable example boundaries.
    trial_plan = []
    for idx in shard_ids:
        for (k, m) in cells:
            for pos in ("text_at_A", "text_at_B"):
                trial_plan.append((idx, k, m, pos))
    print(f"Trial plan: {len(trial_plan)} trials "
          f"({len(shard_ids)} ids x {len(cells)} cells x 2 positions)")
    if args.limit is not None:
        trial_plan = trial_plan[: args.limit]
        print(f"  limited to {len(trial_plan)} for pilot")

    shard_parquet = run_dir / f"mcq_generations_shard_{args.shard_id}.parquet"
    done = set()
    out_rows: list[dict] = []
    if shard_parquet.exists():
        existing = pd.read_parquet(shard_parquet)
        out_rows = existing.to_dict("records")
        for r in out_rows:
            done.add((int(r["id"]), int(r["blur_idx"]), int(r["text_idx"]),
                      r["position"]))
        print(f"Resuming from existing shard parquet: {len(done)} trials done")

    print(f"Loading model {args.model_name}")
    processor = AutoProcessor.from_pretrained(
        args.model_name, trust_remote_code=True, cache_dir=HF_CACHE_DIR,
    )
    model = AutoModelForImageTextToText.from_pretrained(
        args.model_name,
        trust_remote_code=True,
        torch_dtype=torch.bfloat16,
        device_map="auto",
        cache_dir=HF_CACHE_DIR,
    )
    model.eval()
    _maybe_promote_patch_embed_to_fp32(model)

    # Cache blurred images per (id, blur_idx) since we revisit each blur
    # sigma n_text * 2 times per example.
    blur_cache: dict[tuple[int, int], object] = {}

    def get_blurred(idx, k):
        key = (idx, k)
        if key not in blur_cache:
            blur_cache[key] = blur_image(examples_by_id[idx]["image"],
                                         blur_sigmas[k])
        return blur_cache[key]

    n_skipped = 0
    last_checkpoint = len(out_rows)
    for trial_idx, (idx, k, m, pos) in enumerate(
        tqdm(trial_plan, desc=f"shard {args.shard_id}")
    ):
        key = (idx, k, blur_sigmas[k] if False else int(text_levels[m]), pos)
        # We persisted blur_idx + text_idx in rows; resume check uses k, m.
        if (idx, k, m, pos) in done:
            n_skipped += 1
            continue
        ex = examples_by_id[idx]
        a_T = str(ex["text_answer"])
        a_V = str(ex["vision_answer"])

        if pos == "text_at_A":
            ans_a, ans_b = a_T, a_V
            letter_T = "A"
        else:
            ans_a, ans_b = a_V, a_T
            letter_T = "B"

        text_passage = text_variants_by_id[idx][m]
        prompt = build_mcq_prompt(text_passage, ex["question"], ans_a, ans_b)
        image = get_blurred(idx, k)

        msgs = []
        if args.few_shot_n > 0:
            msgs.extend(few_shot_messages(args.few_shot_n))
        msgs.append({
            "role": "user",
            "content": [
                {"type": "image", "image": image},
                {"type": "text", "text": prompt},
            ],
        })
        inputs = processor.apply_chat_template(
            msgs,
            tokenize=True,
            add_generation_prompt=True,
            return_dict=True,
            return_tensors="pt",
            # Qwen3-family and GLM-4.xV chat templates append a think trace
            # unless this is explicitly False; that puts the model into
            # reasoning mode and burns the max_new_tokens budget on the
            # trace. Ignored by Qwen2.5-VL and Gemma3 processors.
            enable_thinking=False,
        )
        inputs = {k_: v.to(model.device) for k_, v in inputs.items()}
        prompt_len = inputs["input_ids"].shape[1]

        with torch.no_grad():
            gen_ids = model.generate(
                **inputs,
                max_new_tokens=args.max_new_tokens,
                do_sample=False,
            )
        new_ids = gen_ids[0, prompt_len:]
        gen_text = processor.tokenizer.decode(new_ids, skip_special_tokens=True)

        parsed, parse_source = parse_choice(gen_text)
        out_rows.append({
            "id": idx,
            "dataset": ex["dataset"],
            "blur_idx": k,
            "blur_sigma": int(blur_sigmas[k]),
            "text_idx": m,
            "text_level": int(text_levels[m]),
            "position": pos,
            "letter_T": letter_T,
            "a_T": a_T,
            "a_V": a_V,
            "parsed_letter": parsed,
            "parse_source": parse_source,
            "gen_prefers_text": parsed == letter_T if parsed else None,
            "generated_text": gen_text,
        })

        if len(out_rows) - last_checkpoint >= args.checkpoint_every:
            pd.DataFrame(out_rows).to_parquet(shard_parquet, index=False)
            last_checkpoint = len(out_rows)

    if out_rows:
        pd.DataFrame(out_rows).to_parquet(shard_parquet, index=False)
        print(f"Saved {len(out_rows)} rows -> {shard_parquet} "
              f"({n_skipped} resumed)")
    else:
        print("WARNING: no rows generated")


if __name__ == "__main__":
    main()
