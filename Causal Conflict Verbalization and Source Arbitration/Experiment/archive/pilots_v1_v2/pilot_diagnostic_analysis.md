# Pre-Freeze Pilot Diagnostic Analysis

**Date:** 2026-09-23
**Items tested:** 20 conflict pairs from `modality-conflict-arbitration-v2` (degradation_level=0)
**Model:** Qwen2.5-VL-3B-Instruct (bfloat16, 7.19 GB VRAM)
**Arms:** Direct (zero-shot), Placebo (neutral description), Conflict Verbalization

---

## ⚠️ Five Critical Findings

### Finding 1: The "Neither" Problem — The Model Computes, It Doesn't Arbitrate

> **85% of Direct-arm responses match NEITHER `image_answer` NOR `text_answer`.**

This is the single most important finding. The current source-arbitration metric (Δ_arb) assumes the model selects one of two pre-existing answers. In reality, the model *tries to solve the math problem* and produces its own (often incorrect) numerical answer.

**Evidence from the generated text:**

| Item | image_answer | text_answer | Model output | What happened |
|:---|:---|:---|:---|:---|
| 0 | 31 (Ram's pens) | 90 (Johnny's allowance) | 60 | Model attempted Johnny's problem, got wrong answer |
| 5 | 1 (balloons) | 17017 (grapes/drums) | 16477 | Model attempted text problem, nearly correct (off by 540) |
| 7 | 120 (oranges) | 79 (states) | 10 | Model attempted neither problem correctly |
| 8 | 270 (trains) | 240 (taxes) | 48 | Model attempted text problem arithmetic, wrong |

**Why this matters:** The thesis question "does verbalization shift which SOURCE the model follows?" assumes the model FOLLOWS a source. But it doesn't — it COMPUTES. The model reads one problem (either from image or text), attempts to solve it, and often gets a wrong answer that doesn't match either ground truth.

**Implication:** The metric must be reframed. Instead of checking `output == image_answer` or `output == text_answer` (exact match), the analysis needs to determine **which PROBLEM the model attempted to solve** — regardless of whether it solved it correctly.

---

### Finding 2: Conflict Verbalization Unlocks a Qualitatively Different Behavior

When instructed to verbalize the conflict, the model:

1. **Correctly identifies the contradiction in 100% of parseable cases** — Every single conflict-verbalization output correctly states "The image and the text do not agree" and identifies the two different problems.

2. **Then decides which problem to solve** — After verbalizing, it picks one problem and attempts to solve it.

3. **Sometimes solves the chosen problem correctly:**

| Item | Behavior under conflict verbalization |
|:---|:---|
| 7 (image=120, text=79) | Identifies conflict → solves text problem → gets "79." (**text-correct!**) |
| 15 (image=120, text=300) | Identifies conflict → solves image problem → gets 120 (**image-correct!**) |
| 5 (image=1, text=17017) | Identifies conflict → solves text problem → gets 16,497 (close to 17017) |
| 6 (image=40, text=3) | Identifies conflict → solves text problem → gets 3 (**text-correct!**) |

4. **Sometimes REFUSES to answer** (5/20 = 25%): The model correctly detects the conflict and concludes "there is no need to provide a numerical answer" — a legitimate abstention response.

**This is actually a more interesting finding than the original thesis anticipated.** The verbalization doesn't just "shift source preference" — it enables a qualitatively different cognitive mode where the model:
- Recognizes the conflict (never happens in direct mode)
- Chooses which problem to engage with
- Sometimes correctly solves the chosen problem
- Sometimes abstains entirely

---

### Finding 3: Length Mismatch Breaks the Control

| Arm | Avg tokens | Target |
|:---|:---|:---|
| Direct | 3.4 | ~10 |
| Placebo | 61.2 | ~75 |
| **Conflict Verbalization** | **103.3** | **~75** |

The conflict arm is **69% longer** than the placebo arm (103 vs 61 tokens). This means any difference between placebo and conflict arms could be attributed to extra computation, not the semantic content of conflict detection.

**Root cause:** The model, after verbalizing the conflict, frequently continues to solve one of the problems step-by-step — sometimes hitting the 200-token max_new_tokens limit (items 3, 10, 11, 12, 13, 18). The placebo arm produces shorter outputs because it just describes the image without solving.

**Required fix:** Either (a) enforce length matching via truncation/constrained generation, or (b) add an explicit "stop after analysis, then answer" formatting constraint, or (c) reframe the control — instead of length-matching, use the placebo arm's *answer* as the baseline and measure whether the conflict arm shifts the *problem choice*.

---

### Finding 4: Parse Failures in Conflict Arm (25%)

| Arm | Parse success |
|:---|:---|
| Direct | 20/20 (100%) |
| Placebo | 19/20 (95%) |
| Conflict Verbalization | **15/20 (75%)** |

5 items failed to extract a number from the conflict arm. Examining these:

| Item | Conflict output (summary) | Why no parse |
|:---|:---|:---|
| 1 | "there is no numerical answer to provide based on the given image" | Model **abstained** — legitimate conflict response |
| 9 | "there is no need to provide a numerical answer for this question" | **Abstained** |
| 11 | "there is no need to provide a numerical answer as they are unrelated" | **Abstained** |
| 17 | "the correct answer is that the image and the text contradict each other" | **Abstained** — gave verdict instead of number |
| 19 | "The number of goldfish that disappeared cannot be determined" | **Abstained** |

**All 5 parse failures are DELIBERATE ABSTENTIONS, not random failures.** The model correctly identified the conflict and chose not to answer — which is actually an important and informative outcome.

**Implication:** Abstention must be classified as a separate response category (not a parse failure). The metric should have three outcomes: follows-image-problem, follows-text-problem, abstains.

---

### Finding 5: Dataset Count Discrepancy (3,238 vs ~1,304)

The clean pair count (degradation_level=0) is **3,238**, not the ~1,304 cited in the thesis specification.

Looking at the data: 2,638 from GSM8K + 600 from SVAMP = 3,238. The "1,304" figure may have referred to an earlier dataset version or a different filtering criterion (e.g., only one `channel` direction, or unique `image_problem_id` pairs).

**This is GOOD news** — more data means higher statistical power. But the discrepancy should be investigated and documented.

---

## Revised Experimental Design

Based on these findings, the experiment needs three modifications:

### Modification 1: Reframe the Primary Metric

**Old metric:** Δ_arb = P(output == image_answer | conflict) − P(output == image_answer | placebo)

**Problem:** 85% of outputs match neither answer, making this metric very noisy.

**New metric — Problem-Choice Classification:**

For each output, classify which **problem** the model attempted to solve:

```
1. FOLLOWS-IMAGE-PROBLEM: The model's reasoning/description references the 
   image-problem's entities (e.g., "Ram", "pens", "cupcakes")
   
2. FOLLOWS-TEXT-PROBLEM: The model's reasoning/description references the 
   text-problem's entities (e.g., "Johnny", "allowance", "taxes")

3. ABSTAINS: The model explicitly refuses to give a numerical answer because 
   it detects the conflict

4. CONFUSED: The model's output doesn't clearly reference either problem
```

This can be measured by:
- **Keyword matching:** Check if generated text mentions entities from the image-problem or text-problem
- **Exact-match (where available):** When the output happens to match image_answer or text_answer
- **LLM-as-judge (backup):** Classify which problem the model engaged with

**Primary analysis:**
```
Δ_choice = P(follows-image-problem | conflict) − P(follows-image-problem | placebo)
Abstention_rate = P(abstains | conflict)
```

### Modification 2: Fix Length Matching

Option A (Recommended): **Enforce structured output format:**
```
"In exactly two sentences, [describe/analyze]. Then write ONLY the final 
numerical answer on a new line after '####'."
```
Add 2-shot demonstrations showing the exact format. This constrains both arms to ~2 sentences + 1 answer token.

Option B: **Truncate at the "####" delimiter** — stop generation as soon as "####" is detected.

Option C: **Add a 4th condition (Long Conflict)** — accept the length mismatch and add a "long neutral padding" arm at ~103 tokens to control for it.

### Modification 3: Classify Abstention as a Primary Outcome

The conflict arm's 25% abstention rate is scientifically informative — it shows that verbalization enables conflict *detection*, not just arbitration. The analysis should report:

```
| Arm      | Follows Image Problem | Follows Text Problem | Abstains | Confused |
|----------|----------------------|---------------------|----------|----------|
| Direct   | ?%                   | ?%                  | 0%       | ?%       |
| Placebo  | ?%                   | ?%                  | 0%       | ?%       |
| Conflict | ?%                   | ?%                  | 25%      | ?%       |
```

---

## Verdict: Should We Freeze?

> **YES — but with the revised metric.** The pilot reveals that the thesis question is MORE interesting than originally framed, not less interesting.

The original question was: "Does verbalization shift source arbitration?"

The pilot shows the answer is richer: **Verbalization doesn't just shift preference — it enables a qualitatively different cognitive mode** where the model:
1. Recognizes the conflict (100% detection)
2. Explicitly separates the two problems
3. Chooses one to solve (sometimes correctly)
4. Sometimes abstains entirely

This is a *stronger* finding than a simple Δ_arb shift. The thesis should reframe from "source arbitration shift" to **"does conflict verbalization enable deliberative problem selection and conflict-aware abstention?"**

### Pre-Freeze Action Items

- [ ] Implement structured output format with 2-shot ICL to fix length matching
- [ ] Implement problem-choice classifier (keyword-based + exact-match)
- [ ] Add abstention as an explicit outcome category
- [ ] Investigate the 3,238 vs 1,304 count discrepancy
- [ ] Re-run the 20-item pilot with the revised prompts and verify parse rate ≥ 90%
- [ ] Only THEN freeze the topic
