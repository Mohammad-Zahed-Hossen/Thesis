#!/usr/bin/env python3
"""Production Experiment Harness v3 (Full Population & Un-Truncated Token Budgets):
Causal Conflict Verbalization and Source Arbitration in Vision-Language Models.

Key Architectural Upgrades in v3:
1. 3-Group Generation Architecture (Zero Truncation):
   - Group 1 (Arm 4a & 4b Prefill Causal Probe): max_new_tokens=20 (ultra-fast, stops at EOS)
   - Group 2 (Arm 1 Direct Baseline): max_new_tokens=80 (enables full scratchpad + #### <answer>)
   - Group 3 (Arms 2 & 3 Placebo & Conflict Verbalization): max_new_tokens=200 (allows 2 sentences + full solve + #### <answer>)
2. Full Population Coverage:
   - Evaluates all 1,619 clean image pairs (degradation_level=0, channel=image) in modality-conflict-arbitration-v2
   - Configurable range via --limit and --offset
3. Transparent Auditing:
   - Stores image_question and text_question in both full_experiment_results.json and experiment_checkpoint.csv
   - Automatic truncation monitoring (flags if tokens reach limit - 1)
4. Robust Checkpointing & Seamless Resume:
   - --resume flag skips already-completed items automatically
5. Native FP16 on T4/V100 (sm_75) + PyTorch 2 SDPA Fused Kernel:
   - Sustains ~2.5s/item on Colab T4 (~65-75 minutes for entire 1,619 population).

Usage on Google Colab Pro (T4/V100/A100):
    !pip install transformers accelerate datasets qwen-vl-utils pillow
    
    # Run full population of 1,619 clean image pairs:
    !python production_experiment_harness.py --split clean_image --limit 1619

    # Or run slice (e.g. remaining 1,119 items starting from 500):
    !python production_experiment_harness.py --split clean_image --offset 500 --limit 1119

    # Or resume from existing checkpoint:
    !python production_experiment_harness.py --split clean_image --limit 1619 --resume
"""
from __future__ import annotations

import argparse
import csv
import glob
import json
import os
import re
import sys
import time
from collections import Counter
from dataclasses import dataclass
from typing import Any, Dict, List, Optional, Set, Tuple

# Auto-configure LD_LIBRARY_PATH for PyTorch CUDA 13/NVRTC shared libraries on Colab
for p in sys.path:
    for lib_dir in glob.glob(os.path.join(p, "nvidia", "*", "lib")):
        if lib_dir not in os.environ.get("LD_LIBRARY_PATH", ""):
            os.environ["LD_LIBRARY_PATH"] = f"{lib_dir}:{os.environ.get('LD_LIBRARY_PATH', '')}"

import torch
from datasets import load_dataset
from PIL import Image

# ─── Fix PyTorch NVRTC JIT Crash on CUDA 13 for Qwen2.5-VL image_grid_thw.prod(-1) ───
# In PyTorch on CUDA 13, integer tensor reduction .prod(-1) invokes NVRTC JIT compilation,
# which fails if libnvrtc-builtins.so.13.0 is missing from system dynamic linker path.
# Computing small integer product on CPU runs in <1 microsecond with zero JIT or driver dependency.
_orig_tensor_prod = torch.Tensor.prod

def _safe_tensor_prod(self, *args, **kwargs):
    if self.is_cuda and self.dtype in (torch.int64, torch.int32, torch.int16, torch.int8):
        return _orig_tensor_prod(self.cpu(), *args, **kwargs).to(self.device)
    return _orig_tensor_prod(self, *args, **kwargs)

torch.Tensor.prod = _safe_tensor_prod


@dataclass
class Config:
    model_id: str = "Qwen/Qwen2.5-VL-3B-Instruct"
    dataset_id: str = "vlm-modality-research/modality-conflict-arbitration-v2"
    secondary_dataset_id: str = "vlm-modality-research/chartqa-evidence-conflict-v2"
    min_pixels: int = 128 * 28 * 28   # 100,352 pixels
    max_pixels: int = 256 * 28 * 28   # 200,704 pixels
    batch_size: int = 8               # Items per batch
    seed: int = 42
    output_dir: str = "experiment_results"
    output_json: str = "full_experiment_results.json"
    checkpoint_csv: str = "experiment_checkpoint.csv"
    # Specialized token budgets per arm group
    max_tokens_direct: int = 80       # Arm 1 (Direct solve + answer)
    max_tokens_verbalize: int = 200   # Arms 2 & 3 (Two sentences + full solve + answer)
    max_tokens_prefill: int = 20      # Arms 4a & 4b (Prefilled prompt, just answer number)


# ─── Prompt Specifications (Frozen Zero-Shot Protocol) ──────────────────────

PROMPT_ARM1_DIRECT = (
    "Look at the image and read the text problem below.\n"
    "{text_question}\n\n"
    "Solve the problem. Conclude with: #### <answer>\n"
)

PROMPT_ARM2_PLACEBO = (
    "Look at the image and read the text problem below.\n"
    "{text_question}\n\n"
    "In two sentences, neutrally describe what is presented in the image and what is stated in the text without comparing them. "
    "Then solve the problem. Conclude with: #### <answer>\n"
)

PROMPT_ARM3_CONFLICT = (
    "Look at the image and read the text problem below.\n"
    "{text_question}\n\n"
    "In two sentences, state whether the image and the text agree or contradict each other, and explain which source you consider more reliable. "
    "Then solve that problem. Conclude with: #### <answer>\n"
)

PREFILL_ARM4_CONTRADICTION = (
    "The image and text contradict each other because they present different problems. "
    "Following the image problem, the answer is: #### "
)

PREFILL_ARM4_AGREEMENT = (
    "The image and text describe consistent premises. "
    "Following the text problem, the answer is: #### "
)


def tlog(*args):
    print(f"[{time.strftime('%H:%M:%S')}]", *args, flush=True)


# ─── Hardware Detection ─────────────────────────────────────────────────────

def select_dtype() -> torch.dtype:
    """FP16 for T4/V100 (sm_75), BF16 for A100+ (sm_80+)."""
    if not torch.cuda.is_available():
        return torch.float32
    major, _ = torch.cuda.get_device_capability()
    if major >= 8:
        tlog(f"GPU sm_{major}0 -> using bfloat16 (native BF16 Tensor Cores)")
        return torch.bfloat16
    tlog(f"GPU sm_{major}0 -> using float16 (no native BF16; FP16 Tensor Cores are ~3x faster)")
    return torch.float16


def select_attn_impl(requested: Optional[str] = None) -> str:
    """Selects the fastest attention backend for current hardware."""
    if requested and requested != "auto":
        return requested
    if not torch.cuda.is_available():
        return "eager"
    try:
        import flash_attn
        major, _ = torch.cuda.get_device_capability()
        if major >= 8:
            tlog("FlashAttention-2 available (sm80+). Using flash_attention_2.")
            return "flash_attention_2"
    except Exception:
        pass
    if hasattr(torch.nn.functional, "scaled_dot_product_attention"):
        tlog("Using PyTorch SDPA (fused kernel).")
        return "sdpa"
    tlog("Falling back to eager attention.")
    return "eager"


# ─── Text / Answer Utilities ────────────────────────────────────────────────

def extract_answer_after_hashes(text: str) -> Optional[str]:
    """Extract numeric answer following #### delimiter."""
    m = re.search(r"####\s*([+-]?\d[\d,]*\.?\d*)", text)
    if m:
        return m.group(1).replace(",", "").rstrip(".")
    numbers = re.findall(r"[+-]?\d[\d,]*\.?\d*", text)
    if numbers:
        return numbers[-1].replace(",", "").rstrip(".")
    return None


def detect_abstention(text: str) -> bool:
    """Detect if model explicitly refused to answer."""
    phrases = [
        "cannot be determined", "no numerical answer", "no need to provide",
        "cannot determine", "not possible to", "no direct connection",
        "cannot be answered", "not enough information", "unrelated problems",
        "contradict each other, so", "different problems, so there is no",
    ]
    t_lower = text.lower()
    return any(p in t_lower for p in phrases)


def extract_entities(question: str) -> Set[str]:
    """Extract domain and entity keywords for problem-choice classification."""
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
    words = re.findall(r"[A-Z][a-z]+(?:'s)?", question)
    proper_nouns = {w.lower().rstrip("'s") for w in words if len(w) > 2}
    all_words = re.findall(r"[a-z]{4,}", question.lower())
    domain_nouns = {w for w in all_words if w not in stop_words}
    return proper_nouns | {n for n in domain_nouns if n not in {
        "make", "take", "give", "sell", "buy", "cost", "paid", "gets", "want", "need", "work", "runs"
    }}


def classify_problem_choice(
    generated_text: str,
    image_question: str,
    text_question: str,
    extracted_answer: Optional[str],
    image_answer: str,
    text_answer: str,
) -> str:
    """Classifies whether output follows image problem, text problem, or abstains."""
    if detect_abstention(generated_text):
        return "abstains"

    img_entities = extract_entities(image_question)
    txt_entities = extract_entities(text_question)
    shared = img_entities & txt_entities
    img_unique = img_entities - shared
    txt_unique = txt_entities - shared

    gen_lower = generated_text.lower()
    img_hits = sum(1 for e in img_unique if e in gen_lower)
    txt_hits = sum(1 for e in txt_unique if e in gen_lower)

    exact_img = (extracted_answer == image_answer) if extracted_answer else False
    exact_txt = (extracted_answer == text_answer) if extracted_answer else False

    if img_hits > txt_hits + 1:
        return "follows_image_problem"
    elif txt_hits > img_hits + 1:
        return "follows_text_problem"
    elif img_hits == txt_hits:
        if exact_img and not exact_txt:
            return "follows_image_problem"
        elif exact_txt and not exact_img:
            return "follows_text_problem"
        return "ambiguous"
    else:
        return "follows_image_problem" if img_hits > txt_hits else "follows_text_problem"


# ─── Chat Template Builder ──────────────────────────────────────────────────

def make_chat_text(processor, prompt: str, prefill: Optional[str] = None) -> str:
    """Build a tokenizer-ready chat string with optional assistant prefill."""
    messages = [
        {"role": "user", "content": [
            {"type": "image"},
            {"type": "text", "text": prompt},
        ]}
    ]
    if prefill:
        messages.append({"role": "assistant", "content": prefill})

    text = processor.apply_chat_template(
        messages, tokenize=False,
        add_generation_prompt=(prefill is None),
    )

    if prefill:
        for suffix in ("<|im_end|>\n", "<|im_end|>"):
            if text.endswith(suffix):
                text = text[:-len(suffix)]
                break
    return text


# ─── Batched Decode Helper ───────────────────────────────────────────────────

def decode_outputs(output_ids, prompt_len: int, tokenizer, prefill: Optional[str] = None) -> List[Tuple[str, int]]:
    """Decode batched generate() output into list of (text, n_actual_tokens)."""
    pad_id = tokenizer.pad_token_id or 0
    eos_id = tokenizer.eos_token_id
    results = []
    for j in range(output_ids.shape[0]):
        gen_ids = output_ids[j, prompt_len:].tolist()
        n_tok = 0
        for tid in gen_ids:
            if tid == eos_id or tid == pad_id:
                break
            n_tok += 1
        text = tokenizer.decode(gen_ids[:max(n_tok, 1)], skip_special_tokens=True)
        if prefill:
            text = prefill + text
        results.append((text, n_tok))
    return results


# ─── Core: 3-Group Batch Processing Pipeline ────────────────────────────────

def process_batch_v3(
    model, processor, batch_items: List[Dict[str, Any]], cfg: Config,
) -> List[Dict[str, Any]]:
    """Evaluates all 5 arms for a batch using 3 tailored generation groups:
    - Group 1: Arms 4a, 4b (Prefill Causal Probe, budget: max_tokens_prefill)
    - Group 2: Arm 1 (Direct Baseline, budget: max_tokens_direct)
    - Group 3: Arms 2, 3 (Placebo & Conflict Verbalization, budget: max_tokens_verbalize)
    """
    N = len(batch_items)
    images = [item["image"].convert("RGB") for item in batch_items]
    txt_qs = [item.get("text_question", item.get("question", "")) for item in batch_items]
    img_qs = [item.get("image_question", "") for item in batch_items]
    img_ans = [str(item.get("image_answer", item.get("chart_answer", ""))) for item in batch_items]
    txt_ans = [str(item.get("text_answer", item.get("report_answer", ""))) for item in batch_items]

    # Pre-build prompts
    p_a1 = [PROMPT_ARM1_DIRECT.format(text_question=q) for q in txt_qs]
    p_a2 = [PROMPT_ARM2_PLACEBO.format(text_question=q) for q in txt_qs]
    p_a3 = [PROMPT_ARM3_CONFLICT.format(text_question=q) for q in txt_qs]

    tokenizer = processor.tokenizer

    # ═════ GROUP 1: Arms 4a + 4b (Prefill Causal Probe, budget: 20 tokens) ═════
    # Stride 2 layout: [a4a_0, a4b_0, a4a_1, a4b_1, ...]
    g1_texts, g1_images = [], []
    for k in range(N):
        g1_texts.append(make_chat_text(processor, p_a1[k], PREFILL_ARM4_CONTRADICTION))
        g1_texts.append(make_chat_text(processor, p_a1[k], PREFILL_ARM4_AGREEMENT))
        g1_images.extend([images[k], images[k]])

    inputs_1 = processor(
        text=g1_texts, images=g1_images,
        return_tensors="pt", padding=True,
    ).to(model.device)
    plen_1 = inputs_1["input_ids"].shape[1]

    t0 = time.time()
    with torch.inference_mode():
        out_1 = model.generate(
            **inputs_1, max_new_tokens=cfg.max_tokens_prefill,
            do_sample=False, temperature=None, top_p=None,
        )
    g1_time = time.time() - t0
    res_a4a = decode_outputs(out_1[0::2], plen_1, tokenizer, PREFILL_ARM4_CONTRADICTION)
    res_a4b = decode_outputs(out_1[1::2], plen_1, tokenizer, PREFILL_ARM4_AGREEMENT)
    del inputs_1, out_1
    torch.cuda.empty_cache()

    # ═════ GROUP 2: Arm 1 (Direct Zero-Shot Baseline, budget: 80 tokens) ═════
    g2_texts = [make_chat_text(processor, p_a1[k]) for k in range(N)]
    inputs_2 = processor(
        text=g2_texts, images=images,
        return_tensors="pt", padding=True,
    ).to(model.device)
    plen_2 = inputs_2["input_ids"].shape[1]

    t0 = time.time()
    with torch.inference_mode():
        out_2 = model.generate(
            **inputs_2, max_new_tokens=cfg.max_tokens_direct,
            do_sample=False, temperature=None, top_p=None,
        )
    g2_time = time.time() - t0
    res_a1 = decode_outputs(out_2, plen_2, tokenizer)
    del inputs_2, out_2
    torch.cuda.empty_cache()

    # ═════ GROUP 3: Arms 2 + 3 (Placebo & Conflict Verbalize, budget: 200 tokens) ═════
    # Stride 2 layout: [a2_0, a3_0, a2_1, a3_1, ...]
    g3_texts, g3_images = [], []
    for k in range(N):
        g3_texts.append(make_chat_text(processor, p_a2[k]))
        g3_texts.append(make_chat_text(processor, p_a3[k]))
        g3_images.extend([images[k], images[k]])

    inputs_3 = processor(
        text=g3_texts, images=g3_images,
        return_tensors="pt", padding=True,
    ).to(model.device)
    plen_3 = inputs_3["input_ids"].shape[1]

    t0 = time.time()
    with torch.inference_mode():
        out_3 = model.generate(
            **inputs_3, max_new_tokens=cfg.max_tokens_verbalize,
            do_sample=False, temperature=None, top_p=None,
        )
    g3_time = time.time() - t0
    res_a2 = decode_outputs(out_3[0::2], plen_3, tokenizer)
    res_a3 = decode_outputs(out_3[1::2], plen_3, tokenizer)
    del inputs_3, out_3
    torch.cuda.empty_cache()

    # ═════ Merge, Classify, Check Truncation & Build Records ═════
    batch_wall = g1_time + g2_time + g3_time
    per_item_s = batch_wall / N

    batch_results = []
    for k in range(N):
        item = batch_items[k]
        item_id = item.get("id", f"item_{item.get('idx', k)}")
        iq, tq = img_qs[k], txt_qs[k]
        ia, ta = img_ans[k], txt_ans[k]

        t_a1, tok_a1 = res_a1[k]
        ans_a1 = extract_answer_after_hashes(t_a1)
        ch_a1 = classify_problem_choice(t_a1, iq, tq, ans_a1, ia, ta)

        t_a2, tok_a2 = res_a2[k]
        ans_a2 = extract_answer_after_hashes(t_a2)
        ch_a2 = classify_problem_choice(t_a2, iq, tq, ans_a2, ia, ta)

        t_a3, tok_a3 = res_a3[k]
        ans_a3 = extract_answer_after_hashes(t_a3)
        ch_a3 = classify_problem_choice(t_a3, iq, tq, ans_a3, ia, ta)

        t_a4a, tok_a4a = res_a4a[k]
        ans_a4a = extract_answer_after_hashes(t_a4a)

        t_a4b, tok_a4b = res_a4b[k]
        ans_a4b = extract_answer_after_hashes(t_a4b)

        record = {
            "id": item_id,
            "image_question": iq,
            "text_question": tq,
            "image_answer": ia,
            "text_answer": ta,
            "arms": {
                "arm1_direct": {
                    "text": t_a1, "ans": ans_a1, "choice": ch_a1,
                    "tokens": tok_a1, "truncated": (tok_a1 >= cfg.max_tokens_direct - 1),
                    "wall_s": round(per_item_s, 3),
                },
                "arm2_placebo": {
                    "text": t_a2, "ans": ans_a2, "choice": ch_a2,
                    "tokens": tok_a2, "truncated": (tok_a2 >= cfg.max_tokens_verbalize - 1),
                    "wall_s": round(per_item_s, 3),
                },
                "arm3_conflict": {
                    "text": t_a3, "ans": ans_a3, "choice": ch_a3,
                    "tokens": tok_a3, "truncated": (tok_a3 >= cfg.max_tokens_verbalize - 1),
                    "wall_s": round(per_item_s, 3),
                },
                "arm4_prefill_contradict": {
                    "text": t_a4a, "ans": ans_a4a,
                    "tokens": tok_a4a, "truncated": (tok_a4a >= cfg.max_tokens_prefill - 1),
                    "wall_s": round(per_item_s, 3),
                },
                "arm4_prefill_agree": {
                    "text": t_a4b, "ans": ans_a4b,
                    "tokens": tok_a4b, "truncated": (tok_a4b >= cfg.max_tokens_prefill - 1),
                    "wall_s": round(per_item_s, 3),
                },
            },
        }
        batch_results.append(record)

    return batch_results


# ─── Main ────────────────────────────────────────────────────────────────────

def main():
    parser = argparse.ArgumentParser(description="Production Experiment Harness v3 (Full Population & Un-Truncated)")
    parser.add_argument("--limit", type=int, default=1619,
                        help="Number of items to evaluate (default: 1619 = entire clean_image population)")
    parser.add_argument("--offset", type=int, default=0,
                        help="Start offset in dataset (default: 0)")
    parser.add_argument("--batch_size", type=int, default=8,
                        help="Items per outer batch (default: 8)")
    parser.add_argument("--split", type=str, default="clean_image",
                        choices=["clean_image", "clean_all", "chartqa"])
    parser.add_argument("--attn", type=str, default="auto",
                        choices=["auto", "flash_attention_2", "sdpa", "eager"])
    parser.add_argument("--max_tokens_direct", type=int, default=80,
                        help="Token budget for Arm 1 direct baseline (default: 80)")
    parser.add_argument("--max_tokens_verbalize", type=int, default=200,
                        help="Token budget for Arms 2 & 3 deliberation (default: 200)")
    parser.add_argument("--max_tokens_prefill", type=int, default=20,
                        help="Token budget for Arms 4a & 4b prefill causal probe (default: 20)")
    parser.add_argument("--output_dir", type=str, default="experiment_results")
    parser.add_argument("--resume", action="store_true",
                        help="Skip items already completed in checkpoint CSV")
    args = parser.parse_args()

    cfg = Config()
    cfg.batch_size = args.batch_size
    cfg.max_tokens_direct = args.max_tokens_direct
    cfg.max_tokens_verbalize = args.max_tokens_verbalize
    cfg.max_tokens_prefill = args.max_tokens_prefill
    cfg.output_dir = args.output_dir
    os.makedirs(cfg.output_dir, exist_ok=True)
    torch.manual_seed(cfg.seed)

    # ── STEP 1: Dataset ──
    tlog("=== STEP 1: Loading Dataset ===")
    if args.split == "chartqa":
        ds = load_dataset(cfg.secondary_dataset_id, split="test")
        tlog(f"Loaded ChartQA conflict benchmark: {len(ds)} items")
        raw_items = [ds[i] for i in range(len(ds))]
    else:
        ds = load_dataset(cfg.dataset_id, split="train")
        clean = ds.filter(lambda x: x["degradation_level"] == 0)
        if args.split == "clean_image":
            clean = clean.filter(lambda x: x["channel"] == "image")
        tlog(f"Filtered clean base pairs ({args.split}): {len(clean)} items available")
        raw_items = [clean[i] for i in range(len(clean))]

    # Apply offset and limit
    end_idx = min(args.offset + args.limit, len(raw_items))
    items = raw_items[args.offset : end_idx]
    for i, it in enumerate(items):
        it["idx"] = args.offset + i

    tlog(f"Configured dataset slice: offset={args.offset}, limit={args.limit} -> {len(items)} items to process.")

    # Checkpoint & Resume Logic
    ckpt_path = os.path.join(cfg.output_dir, cfg.checkpoint_csv)
    done_count = 0
    if args.resume and os.path.exists(ckpt_path):
        with open(ckpt_path, "r", encoding="utf-8") as f:
            reader = csv.reader(f)
            header = next(reader, None)
            arm_counts = Counter()
            for row in reader:
                if len(row) >= 2:
                    arm_counts[row[1]] += 1
            # An item is complete if all 5 arms are logged
            fully_done_ids = {item_id for item_id, count in arm_counts.items() if count >= 5}
        done_count = len(fully_done_ids)
        if done_count > 0:
            tlog(f"Resuming: {done_count} items already completed in {ckpt_path}. Skipping them...")
            items = [it for it in items if it.get("id", f"item_{it.get('idx', -1)}") not in fully_done_ids]

    tlog(f"Remaining items to evaluate: {len(items)} (batch_size={cfg.batch_size}, "
         f"budgets: Direct={cfg.max_tokens_direct}, Verbalize={cfg.max_tokens_verbalize}, Prefill={cfg.max_tokens_prefill})")

    if not items:
        tlog("All requested items are already completed! Nothing to run.")
        return

    # ── STEP 2: Model ──
    tlog("=== STEP 2: Loading Model ===")
    dtype = select_dtype()
    attn_impl = select_attn_impl(args.attn)

    from transformers import AutoProcessor, Qwen2_5_VLForConditionalGeneration

    try:
        model = Qwen2_5_VLForConditionalGeneration.from_pretrained(
            cfg.model_id, torch_dtype=dtype,
            device_map="auto", attn_implementation=attn_impl,
        )
    except Exception as e:
        tlog(f"Warning: {attn_impl} failed ({e}). Falling back to sdpa.")
        attn_impl = "sdpa"
        model = Qwen2_5_VLForConditionalGeneration.from_pretrained(
            cfg.model_id, torch_dtype=dtype,
            device_map="auto", attn_implementation=attn_impl,
        )

    model.eval()

    processor = AutoProcessor.from_pretrained(
        cfg.model_id, min_pixels=cfg.min_pixels, max_pixels=cfg.max_pixels,
    )
    processor.tokenizer.padding_side = "left"
    if processor.tokenizer.pad_token_id is None:
        processor.tokenizer.pad_token_id = processor.tokenizer.eos_token_id

    tlog(f"Model loaded: attn={attn_impl}, dtype={dtype}, "
         f"VRAM={torch.cuda.max_memory_allocated()/2**30:.2f} GB, "
         f"max_pixels={cfg.max_pixels}")

    # ── STEP 3: Execute Protocol ──
    results: List[Dict[str, Any]] = []

    # Initialize CSV header if file doesn't exist
    if not os.path.exists(ckpt_path):
        with open(ckpt_path, "w", newline="", encoding="utf-8") as f:
            writer = csv.writer(f)
            writer.writerow([
                "item_idx", "id", "arm", "extracted_answer", "choice", "is_abstain",
                "exact_img", "exact_txt", "tokens", "truncated", "wall_s",
                "image_question", "text_question"
            ])

    tlog(f"=== STEP 3: Executing Factorial Protocol ({len(items)} items in batches of {cfg.batch_size}) ===")
    total_t0 = time.time()

    for b_start in range(0, len(items), cfg.batch_size):
        batch = items[b_start : b_start + cfg.batch_size]

        try:
            b_results = process_batch_v3(model, processor, batch, cfg)
        except torch.cuda.OutOfMemoryError:
            tlog(f"⚠️ OOM at index {b_start} (N={len(batch)}). Halving batch...")
            torch.cuda.empty_cache()
            half = len(batch) // 2 or 1
            b_results = []
            for sub_start in range(0, len(batch), half):
                sub_batch = batch[sub_start : sub_start + half]
                try:
                    b_results.extend(process_batch_v3(model, processor, sub_batch, cfg))
                except torch.cuda.OutOfMemoryError:
                    tlog(f"⚠️ OOM even at N={len(sub_batch)}. Processing one-by-one...")
                    torch.cuda.empty_cache()
                    for single in sub_batch:
                        b_results.extend(process_batch_v3(model, processor, [single], cfg))

        results.extend(b_results)

        # Checkpoint to CSV
        with open(ckpt_path, "a", newline="", encoding="utf-8") as f:
            writer = csv.writer(f)
            for res in b_results:
                r_id = res["id"]
                r_img, r_txt = res["image_answer"], res["text_answer"]
                iq, tq = res["image_question"], res["text_question"]

                for arm_key in ["arm1_direct", "arm2_placebo", "arm3_conflict", "arm4_prefill_contradict", "arm4_prefill_agree"]:
                    ad = res["arms"][arm_key]
                    writer.writerow([
                        done_count + len(results) - len(b_results),
                        r_id, arm_key, ad["ans"], ad.get("choice", "n/a"),
                        (ad.get("choice") == "abstains"),
                        (ad["ans"] == r_img), (ad["ans"] == r_txt),
                        ad["tokens"], ad.get("truncated", False), ad["wall_s"],
                        iq, tq
                    ])

        done = done_count + len(results)
        elapsed = time.time() - total_t0
        spi = elapsed / len(results)
        remaining = len(items) - len(results)
        eta_m = remaining * spi / 60

        last = b_results[-1]["arms"]
        # Check truncation in latest batch
        trunc_count = sum(1 for r in b_results for a in r["arms"].values() if a.get("truncated", False))
        trunc_flag = f" [⚠️ {trunc_count} truncated]" if trunc_count > 0 else ""

        tlog(f"[{done}/{done_count + len(items)}] {spi:.2f}s/item, ETA: {eta_m:.1f}m{trunc_flag} | "
             f"A1={last['arm1_direct']['choice']}(ans={last['arm1_direct']['ans']}), "
             f"A2={last['arm2_placebo']['choice']}, "
             f"A3={last['arm3_conflict']['choice']}")

    # ── STEP 4: Save Full Structured JSON & Summary ──
    json_path = os.path.join(cfg.output_dir, cfg.output_json)
    
    # If resuming, load existing JSON if present and merge
    final_output_results = results
    if args.resume and os.path.exists(json_path):
        try:
            with open(json_path, "r", encoding="utf-8") as f:
                prev_results = json.load(f)
            prev_ids = {r["id"] for r in prev_results}
            final_output_results = prev_results + [r for r in results if r["id"] not in prev_ids]
        except Exception:
            pass

    with open(json_path, "w", encoding="utf-8") as f:
        json.dump(final_output_results, f, indent=2)

    total_min = (time.time() - total_t0) / 60
    tlog("=== STEP 4: Experiment Complete ===")
    tlog(f"Batch completed: {len(results)} items in {total_min:.1f} min ({len(results)/max(total_min, 0.01):.1f} items/min)")
    tlog(f"Total accumulated results: {len(final_output_results)}")
    tlog(f"JSON saved to: {json_path}")
    tlog(f"CSV saved to: {ckpt_path}")

    # Print summary statistics
    tlog("=== Aggregate Choices Summary ===")
    for arm_key in ["arm1_direct", "arm2_placebo", "arm3_conflict"]:
        counts = Counter(r["arms"][arm_key]["choice"] for r in final_output_results)
        tlog(f"  {arm_key}: " + ", ".join(f"{k}={v}" for k, v in sorted(counts.items())))


if __name__ == "__main__":
    main()
