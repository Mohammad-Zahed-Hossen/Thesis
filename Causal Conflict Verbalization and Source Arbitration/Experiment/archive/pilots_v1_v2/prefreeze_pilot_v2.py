#!/usr/bin/env python3
"""Pre-Freeze Pilot v2: Revised based on Pilot v1 diagnostic findings.

Key changes from v1:
1. Problem-choice classification (keyword entity matching + exact-match)
2. Abstention detection as explicit outcome category
3. Structured output format with 2-shot ICL demonstrations
4. Stop-at-#### truncation for length control
5. Dataset count investigation (channel field analysis)

Run on Google Colab Pro (T4/V100):
    !pip install transformers accelerate datasets qwen-vl-utils pillow
    !python prefreeze_pilot_v2.py
"""
from __future__ import annotations

import json
import os
import re
import time
from collections import Counter
from dataclasses import dataclass

import torch
from datasets import load_dataset


@dataclass
class Config:
    model_id: str = "Qwen/Qwen2.5-VL-3B-Instruct"
    dataset_id: str = "vlm-modality-research/modality-conflict-arbitration-v2"
    dtype: str = "bfloat16"
    max_pixels: int = 448 * 448
    pilot_n: int = 20
    seed: int = 42
    max_new_tokens: int = 150
    output_file: str = "prefreeze_pilot_v2_results.json"


# ─── 2-Shot ICL Demonstrations ──────────────────────────────────────────────

ICL_DEMO_DIRECT = """Example 1:
Q: Tim has 5 apples and buys 3 more. How many apples does Tim have?
#### 8

Example 2:
Q: A store sells 12 widgets at $5 each. What is the total revenue?
#### 60

"""

ICL_DEMO_PLACEBO = """Example 1:
The image shows a math problem about Tim buying apples. The text asks about total revenue from widgets.
#### 8

Example 2:
The image shows a geometry problem about triangles. The text describes a speed calculation.
#### 120

"""

ICL_DEMO_CONFLICT = """Example 1:
The image and text CONTRADICT: the image asks about apples while the text asks about widget revenue. These are two different problems.
#### 8

Example 2:
The image and text CONTRADICT: the image shows a geometry problem while the text describes a speed calculation. They are unrelated.
#### 120

"""

# ─── Prompt Templates (revised with structured output) ──────────────────────

PROMPT_DIRECT = (
    "{icl}"
    "Look at the image and read the text problem below.\n"
    "{text_question}\n\n"
    "Give ONLY the final numerical answer after '####'. No explanation.\n"
    "#### "
)

PROMPT_PLACEBO = (
    "{icl}"
    "Look at the image and read the text problem below.\n"
    "{text_question}\n\n"
    "In one sentence, describe what you see in the image and what the text says. "
    "Then give ONLY the final numerical answer after '####'.\n"
)

PROMPT_CONFLICT = (
    "{icl}"
    "Look at the image and read the text problem below.\n"
    "{text_question}\n\n"
    "In one sentence, state whether the image and text agree or contradict. "
    "Then give ONLY the final numerical answer after '####'.\n"
)

ARMS = {
    "direct": (PROMPT_DIRECT, ICL_DEMO_DIRECT),
    "placebo": (PROMPT_PLACEBO, ICL_DEMO_PLACEBO),
    "conflict_verbalization": (PROMPT_CONFLICT, ICL_DEMO_CONFLICT),
}


def tlog(*args):
    print(f"[{time.strftime('%H:%M:%S')}]", *args, flush=True)


def extract_answer_after_hashes(text: str) -> str | None:
    """Extract the number immediately after ####."""
    m = re.search(r"####\s*([+-]?\d[\d,]*\.?\d*)", text)
    if m:
        return m.group(1).replace(",", "").rstrip(".")
    # Fallback: last number in text
    numbers = re.findall(r"[+-]?\d[\d,]*\.?\d*", text)
    if numbers:
        return numbers[-1].replace(",", "").rstrip(".")
    return None


def detect_abstention(text: str) -> bool:
    """Check if the model explicitly refused to give an answer."""
    abstention_phrases = [
        "cannot be determined",
        "no numerical answer",
        "no need to provide",
        "cannot determine",
        "not possible to",
        "no direct connection",
        "cannot be answered",
        "no answer",
        "not enough information",
    ]
    text_lower = text.lower()
    return any(phrase in text_lower for phrase in abstention_phrases)


def extract_entities(question: str) -> set[str]:
    """Extract key noun entities from a math word problem for matching."""
    # Extract proper nouns and key domain nouns
    # Remove common math/filler words
    stop_words = {
        "how", "many", "much", "what", "the", "is", "are", "was", "were",
        "does", "did", "will", "would", "can", "could", "should", "has",
        "have", "had", "been", "being", "each", "every", "all", "some",
        "any", "per", "for", "from", "with", "and", "but", "or", "not",
        "she", "he", "her", "his", "they", "their", "them", "its", "this",
        "that", "these", "those", "then", "than", "more", "less", "total",
        "if", "in", "on", "at", "to", "of", "by", "an", "a", "it",
        "number", "problem", "step", "answer", "solve", "find", "calculate",
        "first", "second", "third", "next", "last", "day", "days", "hour",
        "hours", "minute", "minutes", "week", "weeks", "month", "year",
        "time", "times", "one", "two", "three", "four", "five", "six",
        "seven", "eight", "nine", "ten", "end", "also", "after", "before",
    }

    # Find capitalized words (proper nouns) and domain-specific nouns
    words = re.findall(r"[A-Z][a-z]+(?:'s)?", question)
    proper_nouns = {w.lower().rstrip("'s") for w in words if len(w) > 2}

    # Also extract key domain nouns (non-stopword nouns 4+ chars)
    all_words = re.findall(r"[a-z]{4,}", question.lower())
    domain_nouns = {w for w in all_words if w not in stop_words}

    # Combine, prioritizing proper nouns
    entities = proper_nouns | {n for n in domain_nouns
                               if n not in {"make", "take", "give", "sell",
                                            "buy", "cost", "paid", "gets",
                                            "want", "need", "work", "runs"}}
    return entities


def classify_problem_choice(
    generated_text: str,
    image_question: str,
    text_question: str,
    extracted_answer: str | None,
    image_answer: str,
    text_answer: str,
) -> str:
    """Classify which problem the model engaged with.

    Returns one of:
      'follows_image_problem' - model engaged with image problem content
      'follows_text_problem' - model engaged with text problem content
      'abstains' - model explicitly refused to answer
      'ambiguous' - can't determine which problem
    """
    if detect_abstention(generated_text):
        return "abstains"

    # Extract entities from both problems
    img_entities = extract_entities(image_question)
    txt_entities = extract_entities(text_question)

    # Remove shared entities
    shared = img_entities & txt_entities
    img_unique = img_entities - shared
    txt_unique = txt_entities - shared

    gen_lower = generated_text.lower()

    # Count entity mentions
    img_hits = sum(1 for e in img_unique if e in gen_lower)
    txt_hits = sum(1 for e in txt_unique if e in gen_lower)

    # Also check exact answer match as tiebreaker
    exact_img = (extracted_answer == image_answer) if extracted_answer else False
    exact_txt = (extracted_answer == text_answer) if extracted_answer else False

    # Decision logic
    if img_hits > txt_hits + 1:
        return "follows_image_problem"
    elif txt_hits > img_hits + 1:
        return "follows_text_problem"
    elif img_hits == txt_hits:
        if exact_img and not exact_txt:
            return "follows_image_problem"
        elif exact_txt and not exact_img:
            return "follows_text_problem"
        elif img_hits > 0:
            return "ambiguous"
        else:
            # No entity hits at all - check if direct arm (very short)
            if len(generated_text.split()) < 5:
                # For very short outputs, rely on exact match only
                if exact_img:
                    return "follows_image_problem"
                elif exact_txt:
                    return "follows_text_problem"
            return "ambiguous"
    else:
        # One has slightly more hits
        if img_hits > txt_hits:
            return "follows_image_problem"
        else:
            return "follows_text_problem"


def main():
    cfg = Config()
    torch.manual_seed(cfg.seed)

    # ═══════════════════════════════════════════════════════════════════════
    # STEP 1: Dataset investigation — explain the 3238 vs 1304 discrepancy
    # ═══════════════════════════════════════════════════════════════════════
    tlog("STEP 1: Downloading and investigating dataset structure...")
    ds = load_dataset(cfg.dataset_id, split="train")
    tlog(f"  Total examples: {len(ds)}")

    # Analyze degradation levels
    deg_levels = Counter(ds["degradation_level"])
    tlog(f"  Degradation levels: {dict(sorted(deg_levels.items()))}")

    # Analyze channel values
    channels = Counter(ds["channel"])
    tlog(f"  Channel values: {dict(channels)}")

    # Filter clean
    clean = ds.filter(lambda x: x["degradation_level"] == 0)
    tlog(f"  Clean pairs (degradation_level=0): {len(clean)}")

    # Check unique problem pairs at level 0
    clean_channels = Counter(clean["channel"])
    tlog(f"  Clean pairs by channel: {dict(clean_channels)}")

    # Check unique (image_problem_id, text_problem_id) pairs
    unique_pairs = set()
    for item in clean:
        unique_pairs.add((item["image_problem_id"], item["text_problem_id"]))
    tlog(f"  Unique (image_problem_id, text_problem_id) pairs at level 0: {len(unique_pairs)}")

    # Subset by channel='image' only (likely what "1304" referred to)
    clean_image = clean.filter(lambda x: x["channel"] == "image")
    tlog(f"  Clean pairs with channel='image': {len(clean_image)}")

    clean_image_gsm8k = clean_image.filter(lambda x: x["source"] == "gsm8k")
    clean_image_svamp = clean_image.filter(lambda x: x["source"] == "svamp")
    tlog(f"    gsm8k: {len(clean_image_gsm8k)}, svamp: {len(clean_image_svamp)}")
    tlog(f"  >>> HYPOTHESIS: '1304' may refer to GSM8K-only or channel='image'-only subset")

    sources = Counter(clean["source"])
    tlog(f"  Sources: {dict(sources)}")

    # ═══════════════════════════════════════════════════════════════════════
    # STEP 2: Sample pilot items (channel='image' only for consistency)
    # ═══════════════════════════════════════════════════════════════════════
    tlog(f"\nSTEP 2: Sampling {cfg.pilot_n} items for pilot (channel='image')...")
    import random
    random.seed(cfg.seed)
    indices = list(range(len(clean_image)))
    random.shuffle(indices)
    pilot_indices = indices[:cfg.pilot_n]
    pilot_items = clean_image.select(pilot_indices)

    # ═══════════════════════════════════════════════════════════════════════
    # STEP 3: Load model
    # ═══════════════════════════════════════════════════════════════════════
    tlog("STEP 3: Loading model...")
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
    # STEP 4: Run 3-arm pilot with revised prompts
    # ═══════════════════════════════════════════════════════════════════════
    tlog("\nSTEP 4: Running 3-arm pilot with revised prompts + 2-shot ICL...")

    results = []

    for i in range(len(pilot_items)):
        item = pilot_items[i]
        item_results = {
            "item_index": i,
            "id": item["id"],
            "image_answer": item["image_answer"],
            "text_answer": item["text_answer"],
            "image_question": item["image_question"][:200],
            "text_question": item["text_question"][:200],
            "source": item["source"],
        }

        for arm_name, (prompt_template, icl_demo) in ARMS.items():
            prompt_text = prompt_template.format(
                text_question=item["text_question"],
                icl=icl_demo,
            )

            messages = [
                {
                    "role": "user",
                    "content": [
                        {"type": "image", "image": item["image"]},
                        {"type": "text", "text": prompt_text},
                    ],
                }
            ]

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

            gen_ids = output_ids[0, inputs["input_ids"].shape[1]:]
            gen_text = processor.tokenizer.decode(gen_ids, skip_special_tokens=True)
            wall_s = time.time() - t0

            # Truncate at #### if present (take answer after last ####)
            extracted = extract_answer_after_hashes(gen_text)
            n_tokens = len(gen_ids)
            is_abstention = detect_abstention(gen_text)

            # Exact-match checks
            follows_image_exact = (extracted == item["image_answer"]) if extracted else False
            follows_text_exact = (extracted == item["text_answer"]) if extracted else False

            # Problem-choice classification
            problem_choice = classify_problem_choice(
                gen_text,
                item["image_question"],
                item["text_question"],
                extracted,
                item["image_answer"],
                item["text_answer"],
            )

            item_results[arm_name] = {
                "generated_text": gen_text[:500],
                "extracted_answer": extracted,
                "exact_match_image": follows_image_exact,
                "exact_match_text": follows_text_exact,
                "problem_choice": problem_choice,
                "is_abstention": is_abstention,
                "n_tokens": n_tokens,
                "wall_seconds": round(wall_s, 2),
            }

            tlog(f"  [{i+1}/{cfg.pilot_n}] {arm_name}: "
                 f"ans={extracted}, choice={problem_choice}, "
                 f"img_exact={follows_image_exact}, txt_exact={follows_text_exact}, "
                 f"tok={n_tokens}")

        results.append(item_results)

    # ═══════════════════════════════════════════════════════════════════════
    # STEP 5: Analysis
    # ═══════════════════════════════════════════════════════════════════════
    tlog("\n" + "=" * 70)
    tlog("STEP 5: ANALYSIS")
    tlog("=" * 70)

    n = len(results)

    # Per-arm problem-choice distribution
    for arm_name in ["direct", "placebo", "conflict_verbalization"]:
        choices = Counter(r[arm_name]["problem_choice"] for r in results)
        exact_img = sum(1 for r in results if r[arm_name]["exact_match_image"])
        exact_txt = sum(1 for r in results if r[arm_name]["exact_match_text"])
        parse_ok = sum(1 for r in results if r[arm_name]["extracted_answer"] is not None)
        abstains = sum(1 for r in results if r[arm_name]["is_abstention"])
        avg_tok = sum(r[arm_name]["n_tokens"] for r in results) / n

        tlog(f"\n  === {arm_name.upper()} ===")
        tlog(f"  Parse success:        {parse_ok}/{n}")
        tlog(f"  Problem-choice distribution:")
        for choice in ["follows_image_problem", "follows_text_problem", "abstains", "ambiguous"]:
            count = choices.get(choice, 0)
            tlog(f"    {choice}: {count}/{n} ({100*count/n:.0f}%)")
        tlog(f"  Exact-match image:    {exact_img}/{n}")
        tlog(f"  Exact-match text:     {exact_txt}/{n}")
        tlog(f"  Explicit abstentions: {abstains}/{n}")
        tlog(f"  Avg tokens:           {avg_tok:.1f}")

    # Cross-arm comparison
    tlog(f"\n  === CROSS-ARM PROBLEM-CHOICE COMPARISON ===")
    header = f"  {'':20s} {'Direct':>10s} {'Placebo':>10s} {'Conflict':>10s}"
    tlog(header)
    for choice in ["follows_image_problem", "follows_text_problem", "abstains", "ambiguous"]:
        direct_n = sum(1 for r in results if r["direct"]["problem_choice"] == choice)
        placebo_n = sum(1 for r in results if r["placebo"]["problem_choice"] == choice)
        conflict_n = sum(1 for r in results if r["conflict_verbalization"]["problem_choice"] == choice)
        tlog(f"  {choice:20s} {direct_n:10d} {placebo_n:10d} {conflict_n:10d}")

    # Length matching check
    tlog(f"\n  === LENGTH MATCHING ===")
    for arm_name in ["direct", "placebo", "conflict_verbalization"]:
        tokens = [r[arm_name]["n_tokens"] for r in results]
        avg = sum(tokens) / len(tokens)
        tlog(f"  {arm_name}: avg={avg:.1f} tokens (min={min(tokens)}, max={max(tokens)})")

    # Per-item shifts
    tlog(f"\n  === PER-ITEM CHOICE SHIFTS (Placebo → Conflict) ===")
    shifts = {"same": 0, "to_image": 0, "to_text": 0, "to_abstain": 0, "other": 0}
    for r in results:
        p = r["placebo"]["problem_choice"]
        c = r["conflict_verbalization"]["problem_choice"]
        if p == c:
            shifts["same"] += 1
        elif c == "follows_image_problem":
            shifts["to_image"] += 1
        elif c == "follows_text_problem":
            shifts["to_text"] += 1
        elif c == "abstains":
            shifts["to_abstain"] += 1
        else:
            shifts["other"] += 1
    tlog(f"  Same choice: {shifts['same']}/{n}")
    tlog(f"  Shifted to image problem: {shifts['to_image']}/{n}")
    tlog(f"  Shifted to text problem: {shifts['to_text']}/{n}")
    tlog(f"  Shifted to abstention: {shifts['to_abstain']}/{n}")
    tlog(f"  Other shifts: {shifts['other']}/{n}")

    # ═══════════════════════════════════════════════════════════════════════
    # STEP 6: Save results
    # ═══════════════════════════════════════════════════════════════════════
    output = {
        "config": {
            "model_id": cfg.model_id,
            "dataset_id": cfg.dataset_id,
            "pilot_n": cfg.pilot_n,
            "seed": cfg.seed,
            "changes_from_v1": [
                "2-shot ICL demonstrations added",
                "Structured output format with #### delimiter",
                "Problem-choice classification (entity matching + exact match)",
                "Abstention detection as explicit category",
                "max_new_tokens reduced to 150 (from 200)",
                "1-sentence constraint (from 2-sentence)",
            ],
        },
        "dataset_investigation": {
            "total_examples": len(ds),
            "degradation_levels": dict(sorted(deg_levels.items())),
            "channels": dict(channels),
            "clean_pairs_total": len(clean),
            "clean_pairs_channel_image": len(clean_image),
            "clean_pairs_channel_breakdown": dict(clean_channels),
            "unique_problem_pairs_at_level_0": len(unique_pairs),
            "sources": dict(sources),
        },
        "results": results,
    }

    with open(cfg.output_file, "w", encoding="utf-8") as f:
        json.dump(output, f, indent=2, default=str)
    tlog(f"\nResults saved to {cfg.output_file}")

    if torch.cuda.is_available():
        tlog(f"Peak VRAM: {torch.cuda.max_memory_allocated()/2**30:.2f} GB")

    tlog("\n" + "=" * 70)
    tlog("PRE-FREEZE PILOT V2 COMPLETE")
    tlog("=" * 70)
    tlog("\nKEY METRICS TO EVALUATE:")
    tlog("1. Is conflict arm length now closer to placebo arm? (Target: <20% difference)")
    tlog("2. Does problem-choice distribution shift between placebo and conflict arms?")
    tlog("3. What is the abstention rate in the conflict arm?")
    tlog("4. Is parse rate >= 90% across all arms?")
    tlog("5. What does the channel/count investigation reveal about the 3238 vs 1304 discrepancy?")
    tlog("\nIf all checks pass: FREEZE THE TOPIC")


if __name__ == "__main__":
    main()
