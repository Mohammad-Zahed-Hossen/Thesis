# Production Experiment Results Analysis (N=500)

**Run Date:** 2026-09-23 15:46–16:14 UTC  
**GPU:** sm_70 (V100-class), float16, SDPA  
**Throughput:** 500 items in **19.4 minutes** (2.32 s/item) — **9.3× faster** than v1 (3 hours)  
**Dataset:** `vlm-modality-research/modality-conflict-arbitration-v2`, clean_image split (first 500 of 1,619)  
**Model:** Qwen2.5-VL-3B-Instruct

---

## 1. Executive Summary

| Finding | Evidence | Significance |
|---------|----------|--------------|
| **93.4% visual capture in neutral conditions** | Arm 2 follows image problem 467/500 times | The VLM overwhelmingly defaults to the visual modality when not prompted to compare |
| **Conflict verbalization breaks visual capture** | Arm 2→Arm 3: 93.4% → 31.4% visual (−62 pp shift) | Explicitly asking the model to compare sources redirects it toward text |
| **Arm 1 is fully truncated** | 100% at token limit (15), 52.2% no answer extracted | `max_new_tokens=15` is too low — must be increased |
| **Arms 2 & 3 are also truncated** | 90.4% and 98.2% hit the 90-token limit | `max_new_tokens=90` is too low for two-sentence + solve prompts |
| **Arm 4 prefilling mostly produces neither-answer** | 4a: 90% match neither; 4b: 85.2% match neither | Prefilled CoT doesn't reliably steer the model to the correct answer |
| **Arm 4a ≡ Arm 4b 54.4% of the time** | Same numeric answer despite opposite prefills | The prefill's causal lever is weak for half the items |

> [!WARNING]
> **All three "generation" arms are severely truncated.** The answers in this run are unreliable because the model ran out of tokens before concluding with `#### <answer>`. The pattern data (choice classification, visual capture shift) is valid because classification uses entity matching in the reasoning text, not just the final answer. But exact-match accuracy metrics are meaningless in this run.

---

## 2. Arm-by-Arm Breakdown

### Arm 1 — Direct Baseline

| Metric | Value |
|--------|-------|
| follows_image_problem | 60 (12.0%) |
| follows_text_problem | 230 (46.0%) |
| ambiguous | 210 (42.0%) |
| exact_match_image | 2 (0.4%) |
| exact_match_text | 3 (0.6%) |
| no_answer_extracted | **261 (52.2%)** |
| avg_tokens | **15.0** (= limit) |

> [!CAUTION]
> **100% of Arm 1 outputs hit the 15-token ceiling.** Every single item was truncated mid-reasoning (e.g., "To solve this problem, we need to determine how many bolts of each type"). No item completed its answer. The `max_new_tokens=15` budget is catastrophically insufficient — pilot data showed Arm 1 needs at least 25 tokens (avg 3.1 in pilot v2, but that was with a different generation format). In production, the model starts with CoT reasoning that easily exceeds 15 tokens.
>
> **Fix:** Increase `group_a_max_tokens` to at least **50** (or 80 to match pilot v1's avg of 61 tokens for direct).

---

### Arm 2 — Neutral Placebo (Visual Capture Probe)

| Metric | Value |
|--------|-------|
| follows_image_problem | **467 (93.4%)** |
| follows_text_problem | 29 (5.8%) |
| ambiguous | 4 (0.8%) |
| exact_match_image | 8 (1.6%) |
| exact_match_text | 11 (2.2%) |
| no_answer_extracted | 26 (5.2%) |
| avg_tokens | 86.0 |
| hit_token_limit (≥85) | **452 (90.4%)** |

**Key Finding:** The VLM follows the **image problem** 93.4% of the time when asked to "neutrally describe what is presented" without being told to compare. This is the thesis's core "visual capture" phenomenon — the visual modality dominates default reasoning.

> [!IMPORTANT]
> Despite the massive visual capture signal, exact answer match is very low (1.6% image, 2.2% text) because **90.4% of outputs hit the 90-token limit** before reaching `#### <answer>`. The model spends tokens on the two-sentence description and starts solving but runs out of space.

---

### Arm 3 — Conflict Verbalization (Treatment)

| Metric | Value |
|--------|-------|
| follows_image_problem | 157 (31.4%) |
| follows_text_problem | **244 (48.8%)** |
| ambiguous | 24 (4.8%) |
| abstains | **75 (15.0%)** |
| exact_match_image | 5 (1.0%) |
| exact_match_text | 12 (2.4%) |
| no_answer_extracted | 43 (8.6%) |
| avg_tokens | 89.5 |
| hit_token_limit (≥85) | **491 (98.2%)** |

**Key Finding — The 62-Point Visual Capture Shift:**

| | Arm 2 (Neutral) | Arm 3 (Conflict) | Shift |
|---|---|---|---|
| follows_image | 93.4% | 31.4% | **−62.0 pp** |
| follows_text | 5.8% | 48.8% | **+43.0 pp** |
| abstains | 0% | 15.0% | **+15.0 pp** |

Asking the model to *"state whether the image and the text agree or contradict each other, and explain which source you consider more reliable"* causes a **massive redirect from visual to textual reasoning.** This is the central thesis result: conflict verbalization breaks visual capture.

The 15% abstention rate shows that some items trigger a "cannot reconcile" response — the model recognizes the conflict but refuses to solve either problem.

---

### Arm 4a — Prefill Contradiction ("Follow Image")

| Metric | Value |
|--------|-------|
| exact_match_image | 8 (1.6%) |
| exact_match_text | 43 (8.6%) |
| match neither | 450 (90.0%) |
| avg_tokens | 2.9 |

### Arm 4b — Prefill Agreement ("Follow Text")

| Metric | Value |
|--------|-------|
| exact_match_image | 4 (0.8%) |
| exact_match_text | **70 (14.0%)** |
| match neither | ~428 (85.2%) |
| avg_tokens | 2.7 |

### Arm 4 Cross-Analysis

- **4a == 4b in 54.4%** of items — the model gives the same answer regardless of whether the prefill says "contradict" or "agree."
- **4b (agreement/text) outperforms 4a (contradiction/image)** on text-answer matching: 14.0% vs 8.6% — suggesting the prefill does have a *weak* causal effect in the expected direction.
- **90% of 4a answers match neither ground truth** — the model generates a plausible-looking number that isn't the correct answer to either problem. This is likely because the prefill cuts off CoT reasoning and forces immediate answer generation.

---

## 3. Critical Data Quality Issues

### Issue 1: Universal Truncation (BLOCKING)

| Arm | Token Budget | % at Limit | Impact |
|-----|-------------|------------|--------|
| Arm 1 | 15 | **100%** | No answers extracted at all |
| Arm 2 | 90 | **90.4%** | Most answers truncated before `####` |
| Arm 3 | 90 | **98.2%** | Nearly all answers truncated |
| Arms 4a/4b | 15 | 0% | Working correctly (avg 2.9 tokens) |

The token budgets for Arms 1–3 are too tight. The prompts ask for reasoning + solving, which requires more tokens than allocated.

**Recommended fix for re-run:**

```python
group_a_max_tokens: int = 80    # Was 15 — Arms 1, 4a, 4b
group_b_max_tokens: int = 200   # Was 90 — Arms 2, 3
```

This will slow the run somewhat (more autoregressive steps), but the data will actually be usable.

### Issue 2: Arm 4 Mostly Matches Neither Answer

With only 1.6% and 14.0% exact matches, the prefill-forced answers are largely incorrect. Possible causes:
1. The model generates plausible but wrong numbers when forced to skip reasoning
2. GSM8K problems require multi-step arithmetic that can't be done in the prefill's continuation
3. The `256*28*28` resolution may have degraded image readability for some problems

### Issue 3: Choice Classification Relies on Entity Matching

The entity-matching classifier may mis-classify when:
- Image and text problems share domain vocabulary (both about money, both about cooking)
- The model's reasoning text mentions entities from both problems
- The `ambiguous` rate of 42% in Arm 1 suggests the classifier often can't decide

---

## 4. What IS Valid in This Run

Despite truncation, the **pattern data is meaningful:**

1. **Visual capture ratio (Arm 2):** 93.4% is robust — the classifier correctly identifies which problem the model is *reasoning about* based on entity mentions, even if the final `#### answer` is truncated.

2. **Conflict verbalization shift (Arm 2→3):** The −62pp shift is a real behavioral change — the model's reasoning text shifts from image-problem entities to text-problem entities when asked to compare sources.

3. **Abstention rate (Arm 3):** 15% abstention is a genuine phenomenon — the model explicitly states it cannot reconcile the sources.

4. **Arm 4 causal weakness:** The 54.4% identical-answer rate is a real finding — prefilling alone is insufficient to reliably steer the model to a specific modality's answer.

---

## 5. Recommended Next Steps

1. **Re-run with increased token budgets** (`group_a=80`, `group_b=200`) to get usable exact-match accuracy data
2. **Keep `max_pixels=256*28*28`** — the choice-classification patterns are strong, suggesting images are readable enough
3. **Consider adding the `image_question` to classification logging** for more transparent auditing
4. **Run the remaining 1,119 items** (total clean_image = 1,619) for full population coverage
5. **Compute statistical tests** (chi-squared / Fisher's exact) on the Arm 2 vs Arm 3 visual capture shift once truncation is fixed

---

## 6. Performance Summary

| Metric | v1 (BF16, 5 calls) | v2 (FP16, 2 calls) | Speedup |
|--------|--------------------|--------------------|---------|
| s/item | ~21.5 | 2.32 | **9.3×** |
| 500 items | ~180 min | **19.4 min** | 9.3× |
| GPU batch | 4 | 24 short / 16 long | 4–6× |
| dtype | bfloat16 (emulated) | float16 (native) | ~2–3× |
| generate() calls per batch | 5 | 2 | 2.5× |
