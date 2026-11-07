#!/usr/bin/env python3
"""Pre-Freeze Verification Pilot for Candidate A:
Causal Conflict Verbalization and Source Arbitration in VLMs.

This script verifies ALL remaining checklist items before the thesis topic is frozen:
1. Downloads and filters the dataset (degradation_level=0 → clean conflict pairs)
2. Counts clean base pairs (verify ≈1,304)
3. Runs a 20-item 3-arm pilot (Direct / Placebo / Conflict Verbalization)
4. Tests instruction-following (2-sentence constraint compliance)
5. Measures baseline modality preference (ceiling/floor check)
6. Parses answers via regex and reports parse success rate

Run on Google Colab Pro (T4/V100):
    !pip install transformers accelerate datasets qwen-vl-utils pillow
    !python prefreeze_pilot.py
"""
from __future__ import annotations

import json
import os
import re
import time
from collections import Counter
from dataclasses import dataclass, field

import torch
from datasets import load_dataset
from PIL import Image


@dataclass
class Config:
    model_id: str = "Qwen/Qwen2.5-VL-3B-Instruct"
    dataset_id: str = "vlm-modality-research/modality-conflict-arbitration-v2"
    dtype: str = "bfloat16"
    max_pixels: int = 448 * 448
    pilot_n: int = 20
    seed: int = 42
    max_new_tokens: int = 200
    output_file: str = "prefreeze_pilot_results.json"


# ─── Prompt Templates ───────────────────────────────────────────────────────

PROMPT_DIRECT = (
    "Look at the image and read the text problem below.\n"
    "{text_question}\n\n"
    "What is the numerical answer? Reply with ONLY the number, nothing else.\n"
    "#### "
)

PROMPT_PLACEBO = (
    "Look at the image and read the text problem below.\n"
    "{text_question}\n\n"
    "In exactly two sentences, describe what you see in the image and what the "
    "text says. Then give the numerical answer.\n"
    "Description: "
)

PROMPT_CONFLICT = (
    "Look at the image and read the text problem below.\n"
    "{text_question}\n\n"
    "In exactly two sentences, state whether the image and the text agree or "
    "contradict each other, and explain why. Then give the numerical answer.\n"
    "Analysis: "
)

ARMS = {
    "direct": PROMPT_DIRECT,
    "placebo": PROMPT_PLACEBO,
    "conflict_verbalization": PROMPT_CONFLICT,
}


def tlog(*args):
    print(f"[{time.strftime('%H:%M:%S')}]", *args, flush=True)


def extract_final_number(text: str) -> str | None:
    """Extract the last number from model output using regex."""
    # Try #### pattern first (GSM8K style)
    m = re.search(r"####\s*([+-]?\d[\d,]*\.?\d*)", text)
    if m:
        return m.group(1).replace(",", "")
    # Fall back to last number in text
    numbers = re.findall(r"[+-]?\d[\d,]*\.?\d*", text)
    if numbers:
        return numbers[-1].replace(",", "")
    return None


def count_sentences(text: str) -> int:
    """Rough sentence count via period/exclamation/question splitting."""
    # Split on sentence-ending punctuation followed by space or end
    sentences = re.split(r'[.!?]+(?:\s|$)', text.strip())
    return len([s for s in sentences if s.strip()])


def main():
    cfg = Config()
    torch.manual_seed(cfg.seed)

    # ═══════════════════════════════════════════════════════════════════════
    # STEP 1: Download and inspect dataset
    # ═══════════════════════════════════════════════════════════════════════
    tlog("STEP 1: Downloading dataset...")
    ds = load_dataset(cfg.dataset_id, split="train")
    tlog(f"  Total examples: {len(ds)}")
    tlog(f"  Columns: {ds.column_names}")

    # ═══════════════════════════════════════════════════════════════════════
    # STEP 2: Filter for clean pairs (degradation_level = 0)
    # ═══════════════════════════════════════════════════════════════════════
    tlog("STEP 2: Filtering for degradation_level = 0...")
    clean = ds.filter(lambda x: x["degradation_level"] == 0)
    tlog(f"  Clean conflict pairs (degradation_level=0): {len(clean)}")
    tlog(f"  *** VERIFICATION: Claimed ~1,304. Actual: {len(clean)} ***")

    # Source distribution
    sources = Counter(clean["source"])
    tlog(f"  Sources: {dict(sources)}")

    # Conflict type distribution
    ctypes = Counter(clean["conflict_type"])
    tlog(f"  Conflict types: {dict(ctypes)}")

    # ═══════════════════════════════════════════════════════════════════════
    # STEP 3: Sample pilot items
    # ═══════════════════════════════════════════════════════════════════════
    tlog(f"STEP 3: Sampling {cfg.pilot_n} items for pilot...")
    indices = list(range(len(clean)))
    import random
    random.seed(cfg.seed)
    random.shuffle(indices)
    pilot_indices = indices[:cfg.pilot_n]
    pilot_items = clean.select(pilot_indices)

    # Show a sample item
    sample = pilot_items[0]
    tlog(f"  Sample item fields:")
    for k, v in sample.items():
        if k != "image":
            tlog(f"    {k}: {repr(v)[:120]}")
    tlog(f"    image: PIL.Image {sample['image'].size if sample['image'] else 'None'}")

    # ═══════════════════════════════════════════════════════════════════════
    # STEP 4: Load model
    # ═══════════════════════════════════════════════════════════════════════
    tlog("STEP 4: Loading model...")
    from transformers import Qwen2_5_VLForConditionalGeneration, AutoProcessor

    model = Qwen2_5_VLForConditionalGeneration.from_pretrained(
        cfg.model_id,
        torch_dtype=getattr(torch, cfg.dtype),
        device_map="auto",
        attn_implementation="eager",
    )
    processor = AutoProcessor.from_pretrained(
        cfg.model_id,
        max_pixels=cfg.max_pixels,
    )
    tlog(f"  Model loaded. VRAM: {torch.cuda.max_memory_allocated()/2**30:.2f} GB")

    # ═══════════════════════════════════════════════════════════════════════
    # STEP 5: Run 3-arm pilot
    # ═══════════════════════════════════════════════════════════════════════
    tlog("STEP 5: Running 3-arm pilot...")

    results = []

    for i in range(len(pilot_items)):
        item = pilot_items[i]
        item_results = {
            "item_index": i,
            "image_answer": item["image_answer"],
            "text_answer": item["text_answer"],
            "source": item["source"],
        }

        for arm_name, prompt_template in ARMS.items():
            prompt_text = prompt_template.format(text_question=item["text_question"])

            # Build messages in Qwen2.5-VL format
            messages = [
                {
                    "role": "user",
                    "content": [
                        {"type": "image", "image": item["image"]},
                        {"type": "text", "text": prompt_text},
                    ],
                }
            ]

            # Process inputs
            text_input = processor.apply_chat_template(
                messages, tokenize=False, add_generation_prompt=True
            )
            inputs = processor(
                text=[text_input],
                images=[item["image"]],
                return_tensors="pt",
                padding=True,
            ).to(model.device)

            t0 = time.time()
            with torch.no_grad():
                output_ids = model.generate(
                    **inputs,
                    max_new_tokens=cfg.max_new_tokens,
                    do_sample=False,
                    temperature=None,
                    top_p=None,
                )

            # Decode only the generated tokens
            gen_ids = output_ids[0, inputs["input_ids"].shape[1]:]
            gen_text = processor.tokenizer.decode(gen_ids, skip_special_tokens=True)
            wall_s = time.time() - t0

            # Extract answer
            extracted = extract_final_number(gen_text)
            n_tokens = len(gen_ids)
            n_sentences = count_sentences(gen_text)

            # Determine which source the model followed
            follows_image = (extracted == item["image_answer"]) if extracted else None
            follows_text = (extracted == item["text_answer"]) if extracted else None

            item_results[arm_name] = {
                "generated_text": gen_text[:500],
                "extracted_answer": extracted,
                "follows_image": follows_image,
                "follows_text": follows_text,
                "n_tokens": n_tokens,
                "n_sentences": n_sentences,
                "wall_seconds": round(wall_s, 2),
            }

            tlog(f"  [{i+1}/{len(pilot_items)}] {arm_name}: "
                 f"extracted={extracted}, img={follows_image}, txt={follows_text}, "
                 f"tok={n_tokens}, sent={n_sentences}")

        results.append(item_results)

    # ═══════════════════════════════════════════════════════════════════════
    # STEP 6: Analysis
    # ═══════════════════════════════════════════════════════════════════════
    tlog("=" * 60)
    tlog("STEP 6: ANALYSIS")
    tlog("=" * 60)

    for arm_name in ARMS:
        parse_ok = sum(1 for r in results if r[arm_name]["extracted_answer"] is not None)
        follows_img = sum(1 for r in results if r[arm_name]["follows_image"] is True)
        follows_txt = sum(1 for r in results if r[arm_name]["follows_text"] is True)
        neither = sum(1 for r in results
                      if r[arm_name]["extracted_answer"] is not None
                      and not r[arm_name]["follows_image"]
                      and not r[arm_name]["follows_text"])
        avg_tokens = sum(r[arm_name]["n_tokens"] for r in results) / len(results)
        avg_sentences = sum(r[arm_name]["n_sentences"] for r in results) / len(results)

        tlog(f"\n  === {arm_name.upper()} ===")
        tlog(f"  Parse success: {parse_ok}/{len(results)} ({100*parse_ok/len(results):.0f}%)")
        tlog(f"  Follows IMAGE: {follows_img}/{len(results)} ({100*follows_img/len(results):.0f}%)")
        tlog(f"  Follows TEXT:  {follows_txt}/{len(results)} ({100*follows_txt/len(results):.0f}%)")
        tlog(f"  Neither:       {neither}/{len(results)}")
        tlog(f"  Avg tokens:    {avg_tokens:.1f}")
        tlog(f"  Avg sentences: {avg_sentences:.1f}")

    # Instruction-following check (2-sentence constraint)
    tlog("\n  === INSTRUCTION-FOLLOWING CHECK ===")
    for arm_name in ["placebo", "conflict_verbalization"]:
        sentence_counts = [r[arm_name]["n_sentences"] for r in results]
        in_range = sum(1 for s in sentence_counts if 1 <= s <= 4)
        tlog(f"  {arm_name}: {in_range}/{len(results)} outputs have 1-4 sentences "
             f"(target: 2). Distribution: {Counter(sentence_counts)}")

    # Length matching check
    tlog("\n  === LENGTH MATCHING CHECK ===")
    for arm_name in ["placebo", "conflict_verbalization"]:
        tokens = [r[arm_name]["n_tokens"] for r in results]
        direct_tokens = [r["direct"]["n_tokens"] for r in results]
        tlog(f"  {arm_name}: avg={sum(tokens)/len(tokens):.1f} tokens "
             f"(direct avg={sum(direct_tokens)/len(direct_tokens):.1f})")

    # Baseline modality preference (ceiling/floor check)
    tlog("\n  === BASELINE MODALITY PREFERENCE (DIRECT ARM) ===")
    direct_img = sum(1 for r in results if r["direct"]["follows_image"] is True)
    direct_txt = sum(1 for r in results if r["direct"]["follows_text"] is True)
    direct_parse = sum(1 for r in results if r["direct"]["extracted_answer"] is not None)
    tlog(f"  Image-following: {direct_img}/{direct_parse}")
    tlog(f"  Text-following:  {direct_txt}/{direct_parse}")
    if direct_parse > 0:
        img_pct = 100 * direct_img / direct_parse
        txt_pct = 100 * direct_txt / direct_parse
        tlog(f"  Image%: {img_pct:.0f}%, Text%: {txt_pct:.0f}%")
        if img_pct > 95 or txt_pct > 95:
            tlog("  ⚠️  WARNING: CEILING/FLOOR DETECTED — model almost always "
                 "follows one source. Verbalization intervention may have no room "
                 "to shift preference. Consider testing a different model or "
                 "adding degradation levels to break the default preference.")
        else:
            tlog("  ✅ Baseline shows mixed preference — room for intervention effect.")

    # ═══════════════════════════════════════════════════════════════════════
    # STEP 7: Save results
    # ═══════════════════════════════════════════════════════════════════════
    output = {
        "config": {
            "model_id": cfg.model_id,
            "dataset_id": cfg.dataset_id,
            "pilot_n": cfg.pilot_n,
            "seed": cfg.seed,
        },
        "dataset_stats": {
            "total_examples": len(ds),
            "clean_pairs_degradation_0": len(clean),
            "sources": dict(sources),
            "conflict_types": dict(ctypes),
        },
        "results": results,
    }

    with open(cfg.output_file, "w", encoding="utf-8") as f:
        json.dump(output, f, indent=2, default=str)
    tlog(f"\nResults saved to {cfg.output_file}")

    # Final VRAM report
    if torch.cuda.is_available():
        tlog(f"Peak VRAM: {torch.cuda.max_memory_allocated()/2**30:.2f} GB")

    tlog("\n" + "=" * 60)
    tlog("PRE-FREEZE PILOT COMPLETE")
    tlog("=" * 60)
    tlog("\nNEXT STEPS:")
    tlog("1. If parse rate < 80%: add 2-shot ICL examples or constrained decoding")
    tlog("2. If ceiling/floor detected: test with degradation_level > 0 or different model")
    tlog("3. If instruction-following fails: add ICL demonstrations")
    tlog("4. If all checks pass: FREEZE THE TOPIC and begin full-scale experiment")


if __name__ == "__main__":
    main()
