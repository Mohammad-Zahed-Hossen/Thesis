# Thesis Understanding FAQ

**Document purpose:** A Q&A reference for understanding the thesis *"Does the Verdict Decide?"*. It is suitable for sharing with collaborators, supervisors or AI assistants for context loading.

**Status of this document:** AI-generated (originally by Opus 4.6), then audited line by line on 2026-11-11 against the code, the raw v4 dev rows, the pre-registration and the primary papers. It is a reference aid, not ground truth. The companion file `Thesis Understanding FAQ (Gemini 3.8 Flash).md` covers the same material in a longer teaching style; the two were harmonized in the same audit and share the numbers in §10.1.

**What "audited" means here:** file and line references were opened and checked; dev numbers were recomputed from `Experiment/results_v4/dev2_*.jsonl`; paper claims were checked against the arXiv text. The audit was done by an AI session inside this project. It is not an outside review.

**Updated 2026-11-14** after the v5 dev pass (run 2026-11-12) and the pre-freeze decisions D1–D5 (2026-11-13). Changed sections are marked *[Updated 2026-11-14]*. v5 numbers come from `Experiment/results_v5/` and are dev data on spent items, not findings. Line links point at the files as of 2026-11-14.

**Epistemic tags:** [Verified] = checked against code, data or the paper itself. [Inferred] = a conclusion drawn from verified facts. [Hypothesis] = awaiting the confirmatory run. [Unknown] = cannot be stated without new data.

---

## Table of Contents

1. [The Research Question](#1-the-research-question)
2. [Title Evolution: Old vs. New](#2-title-evolution-old-vs-new)
3. [The Experimental Method: Prefix-Forcing](#3-the-experimental-method-prefix-forcing)
4. [Version History: Pilots → V3 → V4 → V5](#4-version-history-pilots--v3--v4--v5)
5. [The Dataset Choice](#5-the-dataset-choice)
6. [Prompt Engineering vs. Intervening on the Model's Own Text](#6-prompt-engineering-vs-intervening-on-the-models-own-text)
7. [Why Not Build a New Architecture?](#7-why-not-build-a-new-architecture)
8. [The Base Paper and Theoretical Foundations](#8-the-base-paper-and-theoretical-foundations)
9. [Why a 3B Model Matters](#9-why-a-3b-model-matters)
10. [What the Evidence Actually Shows (So Far)](#10-what-the-evidence-actually-shows-so-far) — including the v5 dev pass (§10.4)
11. [Open Risks and Possible Negative Outcomes](#11-open-risks-and-possible-negative-outcomes)
12. [Key Technical Concepts Glossary](#12-key-technical-concepts-glossary)
13. [File Trust Levels and Navigation](#13-file-trust-levels-and-navigation)
14. [Defence Preparation](#14-defence-preparation)

---

## 1. The Research Question

### Q: What is the core research question of this thesis?

**A:** When a Vision-Language Model (VLM) is shown an image and a typed text that support different answers, and it writes a reliability verdict such as *"I consider the typed text more reliable"*, **does that stated verdict steer which source's answer the model then gives?** The alternative is that the verdict is commentary that does not affect the answer.

> **Source:** Pre-registration §1 — *"When an image and a typed text support different answers, does a vision-language model's verbalized verdict about which source is more reliable causally determine which source its answer follows?"*
> **File:** [`Docs/PREREGISTRATION_VERDICT_TRANSPLANT.md`, line 27](../../../Docs/PREREGISTRATION_VERDICT_TRANSPLANT.md#L27) [Verified]

### Q: What does "Does the Verdict Decide?" mean exactly?

**A:**
- **"The Verdict"** = the one sentence in which the model declares a source more reliable.
- **"Decide"** = when that sentence is reversed by intervention, does the answer move toward the source it now names?

The full working title is *"Does the Verdict Decide? Testing Whether Stated Source Reliability Steers Vision-Language Models under Image–Text Conflict"* ([prereg line 3](../../../Docs/PREREGISTRATION_VERDICT_TRANSPLANT.md#L3)).

### Q: What is the formal estimand?

**A:** The **Controlled Direct Effect (CDE)** of reversing the model's own stated verdict on the log-likelihood margin Δℓ, at a fixed binding level *b*, order *o* and wording template *k*:

$$\mathrm{CDE}_{\ell,b,o,k}=E\big[\Delta\ell\mid do(M{=}m_{flip}),b,o,k\big]-E\big[\Delta\ell\mid do(M{=}m_{own}),b,o,k\big]$$

*[Updated 2026-11-14]* **Which outcome carries the claim depends on the regime (pre-freeze D1).** In GSM8K/SVAMP the primary outcome is now the behavioural answer: the same intervention, read on which problem the model goes on to solve (prereg §1 and §2.3). Δℓ is primary only in ChartQA-Conflict, which is exploratory. §10.4 gives the reason.

A positive CDE means the answer moves toward the source the flipped verdict names ([prereg lines 37–44](../../../Docs/PREREGISTRATION_VERDICT_TRANSPLANT.md#L37-L44)).

**Four boundaries on what this estimand can support:**

1. **It is not mediation.** It is not a natural indirect effect, and the words "mediation" and "mediates" are not used for it ([prereg line 48](../../../Docs/PREREGISTRATION_VERDICT_TRANSPLANT.md#L48)).
2. **It is off-policy.** A forced verdict is not one the model chose. The effect may not transfer to free generation (prereg line 42, dossier §2.3). A CDE says what happens when the text is set by hand; it does not say what role the verdict plays when the model writes it itself.
3. **It is a population average.** The CDE is a mean over items. A positive average does not show that the verdict decides the answer on any particular item, and a zero average does not show it never does (opposite effects on different items can cancel). The confirmatory tests are item-level means, so the thesis makes average claims only. [Inferred from prereg §7.1]
4. **It is about source following, not reliability judgement.** *[Updated 2026-11-14]* After D3 and D4, every confirmatory claim is made in GSM8K/SVAMP, where neither source is wrong, by Qwen2.5-VL-3B and Qwen2.5-VL-7B. A confirmatory result can say whether the stated verdict steers which problem the model solves; it cannot say anything about judging reliability. ChartQA-Conflict, where reliability has a right answer, is exploratory (prereg §1).

**Why "reversing the model's own verdict" and not "image verdict vs. text verdict":** on v4 dev, 94 of 96 parseable verdicts name the typed text. "The verdict names the image" is therefore almost the same variable as "the verdict was edited" ([prereg line 46](../../../Docs/PREREGISTRATION_VERDICT_TRANSPLANT.md#L46)). The matched pair `para` / `para_flip`, in which both verdicts are edited, is the pre-registered check for this.

---

## 2. Title Evolution: Old vs. New

### Q: What was the original title, and why did it change?

**A:** The original title was **"Causal Conflict Verbalization and Source Arbitration in VLMs"**. It comes from the September 2026 topic synthesis, where the research question was headed *"RQ 1: Causality of Conflict Verbalization in Cross-Modal Decision Arbitration"* (`Archive/VLM/Canonical_Cross_Modal_Thesis_Synthesis.md`, line 159, dated 20 September 2026). [Verified]

| Dimension | Old title | Current title |
|:---|:---|:---|
| **What it sounds like** | Building an arbitration system or a general theory | One measurable, hypothesis-driven question |
| **The core object** | "Verbalization" and "arbitration" (broad processes) | "The verdict" (one reliability sentence) |
| **Manipulated variable** | The instruction (Z): ask for a conflict statement or not | The verdict content (M), by prefix-forcing, at fixed Z, order and wording |
| **Can it detect rationalization?** | **No.** A large instruction effect is compatible with the verbalization doing nothing | **Partly.** It tests the controlled direct effect of a forced verdict, with the limits in §1 |
| **Possible outcomes** | Hard to state in advance | Five pre-registered readings (§10.3), two of which are "inconclusive" and "undetermined" |

### Q: Why exactly is the old title no longer accurate?

**A:** Three reasons:

1. **"Conflict Verbalization" named an instruction-level manipulation.** The pilots and v3 changed the user prompt, not the model's generated text.
   > [`Experiment/results_v3/README.md`, line 41](../../../Experiment/results_v3/README.md#L41): the claim "Verbalization causes the shift" fails because *"Only the instruction was randomized"*. [Verified]

2. **"Causal" referred to the instruction effect.** That effect is real and randomized, but it is the effect of an instruction. It cannot show whether the words the model then writes do any work.

3. **Claims attached to the old title did not survive re-analysis.** "13.65% refusals" is 38 items (2.3%) under `score_v4.py`, and "reverses default visual capture" is not supported (Arm 1 is 13.8% visual).
   > [`Experiment/results_v3/README.md`, lines 37–38](../../../Experiment/results_v3/README.md#L37-L38); `results_v3/reanalysis_v3/reanalysis_v3.md`, row `arm3_conflict`: 38 (2.3%). The 2.3% label is itself an unvalidated heuristic. [Verified]

4. **"Arbitration" is ill-posed for GSM8K/SVAMP.** Both problems are valid; neither source is wrong. Reliability claims belong to ChartQA-Conflict (prereg §3.1).

### Q: Isn't the new title just a shortcut or downgrade from the original idea?

**A:** No, but the history is less tidy than "the pilots took a shortcut".

The September specification asked: *"does requiring it to explicitly verbalize and explain the contradiction causally change its decisional arbitration, or does the explanation merely act as a post-hoc rationalization of an entrenched modality preference?"* (`Canonical_Cross_Modal_Thesis_Synthesis.md`, §12, line 347). So the post-hoc rationalization question was the founding motivation. [Verified]

However, the same specification stated its own H₁/H₀ predictions as a **conflict prompt vs. length-matched placebo prompt** contrast (lines 350–353). That is an instruction contrast. It also listed a "Lanham-style prefilling" condition (lines 171 and 380–385), but with an authored contradiction statement, not a reversal of the model's own reliability verdict. [Verified]

So the pilots and v3 mostly ran what the September plan specified. The weakness was in the plan's primary contrast, and the v3 re-analysis exposed it. The current design is the first in the repository that holds the instruction fixed and intervenes on the model's own verdict. [Inferred]

---

## 3. The Experimental Method: Prefix-Forcing

### Q: How does the experiment work?

**A:** The method is **prefix-forcing (prefilling)**. The start of the assistant turn is written by the experimenter, and the model continues from it.

```
INSTRUCTION CONTRAST (pilots and v3 — not what v5 does):
  User prompt [CHANGES]  →  model output [CHANGES]
  (Measures the effect of the instruction.)

PREFIX-FORCING (v4/v5):
  User prompt [identical within a contrast]
           │
           ▼
  Assistant turn starts with the model's OWN earlier verbalization, either
    unchanged (own)            → margin Δℓ at "####"
    or with the source noun in its reliability sentence swapped (flip)
                               → margin Δℓ at "####"
  (Measures the effect of the verdict text at a fixed instruction.)
```

In Pearl's notation this is treated as $do(M = m)$: the instruction, the image, the typed text, the evidence order and the wording template stay fixed, and only the verdict sentence changes. What it identifies is the controlled direct effect in §1, no more.

> **Code:** [`Experiment/harness_v5.py`, lines 250–263](../../../Experiment/harness_v5.py#L250-L263) — `render_chat()` appends the prefill as the assistant turn, strips the closing `<|im_end|>`, and raises an error if the chat template altered the prefill. [Verified]

**Two measurements; which one decides depends on the regime.** *[Updated 2026-11-14]* (1) **Δℓ:** after the prefill `{m}\n\n####`, the two candidate answers are teacher-forced and their length-normalized log-probabilities compared (image minus text). (2) **The behavioural answer:** the model continues from the prefill and solves the problem, and its answer is parsed. In GSM8K/SVAMP the behavioural answer is primary and Δℓ secondary; in ChartQA-Conflict (exploratory) Δℓ is primary (prereg §2, §6).

### Q: What are the verdict variants?

**A:** Five variants are built from the model's own donor verbalization (prereg §5.2):

| Variant | Description | Purpose |
|:---|:---|:---|
| `own` | The model's verbalization, unchanged | Baseline |
| `flip` | Source noun phrases swapped inside the reliability sentence only | Primary intervention |
| `none` | The reliability sentence deleted | Prefill for the explicit-source ceilings; also the "verdict deleted" step of the decomposition (§10.4) |
| `para` | Reliability sentence replaced by a template naming the own source | Wording floor; matched pair |
| `para_flip` | The same template naming the opposite source | Matched pair (both verdicts edited) |

> **Code:** [`Experiment/transplant_v5.py`, line 51](../../../Experiment/transplant_v5.py#L51) — `VERDICTS = ("own", "flip", "none", "para", "para_flip")`. [Verified]

The paraphrase templates ([`transplant_v5.py`, lines 52–57](../../../Experiment/transplant_v5.py#L52-L57)) [Verified]:
1. "I consider {X} more reliable."
2. "{X} seems more reliable to me."
3. "I would treat {X} as more reliable."
4. "{X} is the more reliable source."

Authored sentences from v4 (`rel_image` / `rel_text`) are not run in v5 (prereg §5.2, step 3).

---

## 4. Version History: Pilots → V3 → V4 → V5

### Q: What did each stage do, and what did it get wrong?

> **Correction from the audit:** earlier versions of this FAQ described a "V2 stimulus layer". There is no such stage. The "-v2" is part of the Hugging Face dataset names. In the repository, v1 and v2 are two 20-item pre-freeze pilots (`Experiment/archive/pilots_v1_v2/`), and a 500-item production run is stored in `Archive/Experiment_History/`. [Verified]

```mermaid
flowchart TD
    P["Pilots (Sept 2026)<br>• Two 20-item pre-freeze pilots, then N=500<br>• Instruction contrast"] --> V3["V3 pilot (N=1,619)<br>• Placebo vs. conflict instruction<br>• FLAW: the instruction was randomized, not the verbalization"]
    V3 --> V4["V4 prefix-forced transplants (dev N=200)<br>• Instruction fixed; verbalization transplanted<br>• FLAWS: fixed evidence order, whole-text swaps, authored verdicts, high wording churn"]
    V4 --> V5["V5 (dev pass run 2026-11-12, 29,880 rows)<br>• Both evidence orders<br>• Binding arm and explicit ceilings<br>• Minimal-edit flips<br>• After the dev pass: behaviour primary in Math, Δℓ in ChartQA"]
```

#### Stimuli (all stages)
- From *Which Source Wins?* (Ghosh, Gupta & Wang, arXiv:2608.17205): the rendered image of problem *i* paired with the typed text of problem *(i+1) mod N*; equal-answer pairs excluded.
- Dataset and revision pins: [`Experiment/harness_v4.py`, lines 51–54](../../../Experiment/harness_v4.py#L51-L54). [Verified]

#### V3 — the instruction-contrast pilot (N = 1,619; 1,600 distinct-answer items)
- **What it did:** the same conflict stimuli under different instructions, including a placebo (describe) instruction and a conflict instruction (state whether the sources conflict and which is more reliable).
- **Result that holds:** v3's "visual" label fell from 89.5% to 25.8%, a 63.7 pp shift (problem-clustered 95% interval 59.4 to 68.0 pp). On exact answers, text-matching answers rose from 4.2% to 36.1%.
- **Why it cannot test faithfulness:** only the instruction was randomized.
- **Claims that did not hold:**
  - "13.65% refusals" → 38 items (2.3%) [Verified]
  - "Zero truncation" → 98.1%, 37.6% and 44.2% of Arms 1–3 hit the token cap [Verified]
  - "Deterministic #### parsing" → exact matches via a numeric `####` were 1, 0 and 0 in Arms 1–3; the last-number fallback did the work [Verified]
- v3 also ran with `repetition_penalty` 1.05, which the dev penalty check shows raises image answers and abstention labels.

> [`Experiment/results_v3/README.md`, lines 28–44](../../../Experiment/results_v3/README.md#L28-L44); code in `Experiment/archive/harness_v3/`.

#### V4 — prefix-forced transplants (dev, N = 200, Qwen2.5-VL-3B only)
- **Step forward:** the instruction is held fixed and the opening of the model's response is prefilled.
- **Limitations found:**
  1. **Evidence order was fixed.** The v4 prompt always puts the image first. Order was never varied in v4, so no recency effect was measured in this project. The concern comes from the literature: with the instruction fixed, placing an image after conflicting text raised image-matching answers for Qwen2.5-VL-3B by +16.7 pp (GQA) and +15.0 pp (VQAv2) on natural images (arXiv:2609.26986, Table 1). Whether a similar effect exists on these stimuli is [Unknown] until the v5 dev pass.
  2. **Whole-text swaps.** The `m0` vs. `m1` contrasts replace the entire verbalization, so content, length and verdict are confounded.
  3. **Authored verdicts.** `rel_image` / `rel_text` are sentences written by the experimenter, not edits of the model's own words.
  4. **High wording churn.** Two same-meaning prefills changed the answer-source label on 23–25% of the 110 competent items (§10.1).
  5. **No verdict effect under the conflict instruction** (−1.8 pp). Instruction dominance is one explanation; unfaithfulness is another. Dev data cannot separate them. [Hypothesis]

> [`Experiment/results_v4/README.md`](../../../Experiment/results_v4/README.md); `Experiment/results_v4/analysis_dev2/analysis_v4.md`; code in `Experiment/harness_v4.py` and `Experiment/transplant_v4.py`.

> [!WARNING]
> `results_v4/README.md` §3 used to say the dev numbers "confirm the central causal hypothesis". **That was an overclaim**, corrected on 2026-11-11: those contrasts swap the whole verbalization. They are dev data for tuning, not findings.

#### V5 — the confirmatory harness
- **Status** *[Updated 2026-11-14]*: the dev pass ran on 2026-11-12 on an NVIDIA L4 in `bfloat16` for all three models (29,880 rows in `Experiment/results_v5/`) and has been audited (`Thesis/docs/Archive/`). The pre-freeze decisions D1–D5 followed (§10.4). Tests: `python -B -m unittest discover -s Experiment/tests` from the repository root (235 pass as of 2026-11-14). No confirmatory data exists, and the pre-registration is not frozen.
- **Design rules:**

| Rule | What it addresses |
|:---|:---|
| **Counterbalanced order** | Every item is run in both `<image><text>` and `<text><image>`. This balances any order effect across the contrast and lets it be estimated. It does not remove it. |
| **Minimal-edit verdict flips** | Only source noun phrases inside the model's own reliability sentence are swapped. Gates: one sentence changed; the parsed source reverses; token Jaccard ≥ 0.85; at most two noun phrases swapped; grammar check. |
| **Binding arm** | "Then solve only the problem from the source you named as more reliable, and ignore the other problem." Without it, a null cannot be told apart from the instruction dominating. |
| **Explicit-source ceilings** | `explicit_image` / `explicit_text` with the `none` prefill. A reference for how far a direct instruction moves Δℓ. It is a yardstick, not a proven maximum. |
| **Competency filter** | Only items the model solves from the image alone and from the text alone enter the transplant. Answers are parsed with the `structured` parser (`####`, else an explicit "the final answer is X"; D3). |
| **Primary outcome by regime** *[Updated 2026-11-14]* | GSM8K/SVAMP: the behavioural answer at template k = 1, with the matched template pair co-primary (D1, D2). ChartQA (exploratory): Δℓ, teacher-forced at `####`, image minus text, length-normalized. |
| **K = 4 instruction templates** | Four wordings of each instruction. Δℓ is scored for all four; the behavioural answer only for k = 1, so the Math primary outcome rests on one wording. (The wording *floor* is a different thing: it is `own` vs. `para`.) |
| **Greedy decoding, repetition penalty 1.0, pinned revisions** | Reproducibility; avoids the v3 penalty artefact. |

> [`Experiment/README.md`](../../../Experiment/README.md); code in [`harness_v5.py`](../../../Experiment/harness_v5.py), [`transplant_v5.py`](../../../Experiment/transplant_v5.py), [`score_v5.py`](../../../Experiment/score_v5.py), [`analyze_v5.py`](../../../Experiment/analyze_v5.py). [Verified]

---

## 5. The Dataset Choice

### Q: Which datasets are used, and why?

| Dataset | Hugging Face ID | Size | Type of conflict | What "reliability" means |
|:---|:---|:---|:---|:---|
| **GSM8K/SVAMP** | `vlm-modality-research/modality-conflict-arbitration-v2` | 13.0K rows in split `train` (all degradation levels and channels). Filtered to clean image-channel rows: 1,304 GSM8K + 296 SVAMP distinct-answer pairs. 200 are spent as dev. | Task selection: two different valid problems | Nothing. Neither source is wrong. Results are described as **source following**. |
| **ChartQA-Conflict** | `vlm-modality-research/chartqa-evidence-conflict-v2` | Split `test`. 230 rows at the pinned revision; `conflict_id` 45 is excluded, leaving 229. 30 dev, 199 confirm. | Evidence: the chart supports one answer, a counterfactual report another | The chart is the original evidence. This is the regime where a reliability claim is meaningful. Exploratory since D4. |

> Prereg [lines 151–154](../../../Docs/PREREGISTRATION_VERDICT_TRANSPLANT.md#L151-L154) and [lines 165–168](../../../Docs/PREREGISTRATION_VERDICT_TRANSPLANT.md#L165-L168); Hub dataset viewer, read 2026-11-11; arXiv:2608.17205 §3.4. [Verified]

> **229 vs. 230 (resolved):** the pinned release has 230 rows. *Which Source Wins?* excluded `conflict_id` 45 after an audit; `harness_v5.chartqa_analysis_set` drops it and checks both counts, so 229 items are analysed. [Verified, Hub and code, 2026-11-13]

### Q: Is the dataset the problem? What if I chose another one?

**A:** The datasets are a reasonable fit, with known limits:

1. **Two known candidate answers per item.** Each item carries the image-supported and the text-supported answer, so the response shows which source was followed and a margin between the two can be scored. GSM8K/SVAMP answers are numbers. ChartQA answers are not all numbers (they include labels and yes/no), which is why v5 has a typed normalizer and a strict parser (prereg §4.4).
2. **A published reference point.** *Which Source Wins?* built these stimuli. Direct numerical comparison is limited, though: that paper tested Qwen2-VL-2B and Qwen2.5-VL-**7B** (not the 3B), used "Source A/B" labels, and reports its margin as text minus image. [Verified, arXiv:2608.17205 §3.1, §3.3]
3. **The fix was reframing.** Calling GSM8K/SVAMP "arbitration" was the error. Treated as source choice under conflict, it is well defined.

Other datasets are possible. Barua et al. (arXiv:2610.19407) score candidate-answer log-odds on DocVQA, VQAv2 and RealworldQA. Switching would mean building new conflict pairs and re-doing the competency and dev work, not that the method breaks.

### Q: What is the known limitation of ChartQA-Conflict?

**A:** The report states the value directly; the chart has to be read. Text is therefore likely to be the stronger evidence for a reason unrelated to trust. Barua et al. measured this kind of asymmetry on other datasets (DocVQA, VQAv2, RealworldQA): on clean inputs, mean text evidence exceeded mean visual evidence by a factor of 1.4–3.8, "expected given how the stimuli are constructed: the text states the answer while the image must be interpreted" (arXiv:2610.19407, pp. 7–8). That figure was not measured on ChartQA-Conflict; it is cited by analogy. [Verified for the paper; Inferred for this dataset]

---

## 6. Prompt Engineering vs. Intervening on the Model's Own Text

### Q: Am I just doing prompt engineering?

| Stage | Assessment | Why |
|:---|:---|:---|
| **Pilots and v3** | An instruction contrast | The user prompt differs between conditions. That measures the effect of the instruction. |
| **v4 and v5** | An intervention on the response prefix | Within each contrast the user prompt is identical. What differs is text in the assistant turn. |

The distinction:
- **Changing the instruction** tests how the model responds to what it is told.
- **Prefix-forcing** tests whether text in the model's own turn (here, a verdict it wrote, minimally edited) changes what follows.

Be precise about the limit: prefix-forcing edits *output tokens*. It does not read or edit internal representations. It is a behavioural intervention, not mechanistic interpretability.

**Related methods (checked against the papers):**
- Lanham et al. (2023), *Measuring Faithfulness in Chain-of-Thought Reasoning* (arXiv:2307.13702): intervene on the CoT itself (truncation, inserted mistakes, paraphrasing, filler tokens) and measure whether the answer changes. This is the direct methodological ancestor.
- Turpin et al. (NeurIPS 2023), *Language Models Don't Always Say What They Think* (arXiv:2305.04388): perturb the **input** with biasing features and show the CoT does not mention them. This motivates the question but is not prefix-forcing.
- CoT-Mediate (arXiv:2607.27304): prefix-forces an edited version of the model's own CoT in medical VQA. The dossier identifies it as the closest method.

> [!IMPORTANT]
> If the instruction wording differs between the two sides of a contrast, the comparison is an instruction contrast again. In v5 the templates are literal strings ([`harness_v5.py`, lines 57–109](../../../Experiment/harness_v5.py#L57-L109)) and [`tests/test_v5.py`](../../../Experiment/tests/test_v5.py) checks them against the pre-registration text. Note that the binding and non-binding arms *do* differ in instruction by design; the verdict contrast is always made within one arm.

---

## 7. Why Not Build a New Architecture?

### Q: Why am I not building a new system? Isn't that higher value?

**A:**

1. **Compute.** The project runs inference on a single Colab GPU (an NVIDIA L4 with about 22.5 GiB in the dev pass). Training a competitive VLM is out of reach at that scale; inference-only experiments on open-weight models are not.
2. **Diagnostic work is an established contribution type.** Lanham et al. (2023) and Turpin et al. (2023) proposed no new model. Lanham et al. found "large variation across tasks in how strongly [models] condition on the CoT"; Turpin et al. found that biasing features changed answers (accuracy drops of up to 36%) without being mentioned in the explanation. [Verified]
3. **Diagnosis informs design.** Whether a stated verdict carries any decision weight is useful to know before building anything that relies on such statements. Either outcome is informative, within the scope of two small models and two datasets. It would not by itself show that architectural change is needed.

---

## 8. The Base Paper and Theoretical Foundations

### Q: Is *Which Source Wins?* the base paper?

**A:** For the stimuli, yes. For the scientific question, no.

| Role | Paper | What it provides |
|:---|:---|:---|
| **Stimuli** | *Which Source Wins?* — Ghosh, Gupta & Wang (arXiv:2608.17205) | The GSM8K/SVAMP conflict construction and ChartQA-Conflict. It measures how preference shifts as one source is degraded. Its margin is scored "with no chain-of-thought, so the margin measures direct-answer preference, not reasoning-trace attribution" (p. 5). It contains no faithfulness analysis. |
| **Method ancestry** | Lanham et al. (arXiv:2307.13702) | Intervening on the CoT to test whether the answer depends on it. |
| **Motivation** | Turpin et al. (arXiv:2305.04388, NeurIPS 2023) | CoT explanations can omit what actually drove the answer. |
| **Closest method** | CoT-Mediate (arXiv:2607.27304) | Prefix-forced edits of the model's own CoT; paraphrase floors of 0.5–3.3%. |
| **Order protocol** | Li et al., *Evidence Noncommutativity* (arXiv:2609.26986) | Fixed instruction, swapped evidence order. |
| **Ceiling baseline** | Dassen et al., *Grounding on Request* (arXiv:2610.33841) | Natural-language modality requests; they give weak control, especially for image requests. Our explicit-source arms replicate this baseline and are not claimed as new. That paper does not prefix-force any model text. |
| **Evidence strength** | Barua, Mahowald & Rudman (arXiv:2610.19407) | Text evidence 1.4–3.8× stronger than visual evidence on clean inputs in their datasets. |

### Q: What is the novelty boundary?

**A:** From pre-registration §1.1 ([line 64](../../../Docs/PREREGISTRATION_VERDICT_TRANSPLANT.md#L64)), verbatim:

> *"Within the fourteen sources read, no study intervenes on a vision-language model's own stated source-reliability verdict, by prefix-forcing a minimally edited version of it, and measures whether the answer follows under image–text conflict with evidence order counterbalanced. Nor does any test whether an instruction that binds the answer to that verdict changes its effect."*

This is a statement about fourteen sources, not about the field. CMC-Bench (Catapang 2026) is still unread and must be read before the related-work chapter. Do not write "first" or "novel" beyond this boundary.

---

## 9. Why a 3B Model Matters

### Q: Much larger models exist. Why does work on a ~3B model matter?

#### Reason A: the method needs continuation scoring
The primary outcome requires (1) writing an arbitrary prefix into the assistant turn and (2) scoring the log-probability of two given continuations. *Which Source Wins?* reports that GPT-5.6-Luna, Gemini-3.5-Flash and InternVL2-8B "lack the continuation-scoring interface the CLL margin requires", so it used them for generated answers only (arXiv:2608.17205, §3.1). Open weights give both. [Verified]

> **Code:** [`Experiment/harness_v5.py`, lines 529–579](../../../Experiment/harness_v5.py#L529-L579) — `HFBackend.score()` teacher-forces both candidates and returns `dl`.

#### Reason B: the model can do the single-source tasks, most of the time
On v4 dev, Qwen2.5-VL-3B solved 72.8% of problems from the image alone and 75.4% from the text alone (195 distinct problems; McNemar p = 0.51). Both from the same item: 110 of 200. So the competency filter keeps about 55% of items.

*[Updated 2026-11-14]* In the v5 dev pass (`structured` parser), Math competency was 80/200 for Qwen2.5-VL-3B, 124/200 for Qwen2.5-VL-7B and 0/200 for Qwen2-VL-2B, which never writes `####`.

> `Experiment/results_v4/analysis_dev2/analysis_v4.md`, "Solvability"; 110/200 recomputed in this audit. [Verified]

Qwen2.5-VL-3B is also used by neighbouring work (arXiv:2609.26986, arXiv:2610.19407), which gives comparison points.

#### Reason C: size and faithfulness
Lanham et al. report that "as models become larger and more capable, they produce less faithful reasoning on most tasks we study" (text-only LLMs, 13B vs. 175B). This is from Lanham et al., **not** Turpin et al.; Turpin et al. tested GPT-3.5 and Claude 1.0 and make no size comparison. To investigate whether this extends to modern VLMs without confounding architecture generations, this thesis evaluates the **Qwen Triad**: two compact models (2B and 3B) plus a flagship 7B model. While three models across two generations cannot establish a general scaling law, comparing `Qwen2.5-VL-3B` against `Qwen2.5-VL-7B` provides a clean, within-generation size comparison on the intersection of competent items.

#### Models (The Qwen Triad)

| Model | Pinned revision | Parameters (Hub) | Role |
|:---|:---|:---|:---|
| `Qwen/Qwen2.5-VL-3B-Instruct` | `66285546d2b821cf421d4f5eb2576359d3770cd3` | 3,754.6M | Confirmatory (workhorse) |
| `Qwen/Qwen2.5-VL-7B-Instruct` | `cc594898137f460bfe9f0759e9844b3ce807cfb5` | 8,292.2M | Confirmatory (flagship, matches *Which Source Wins?*) |
| `Qwen/Qwen2-VL-2B-Instruct` | `895c3a49bc3fa70a340399125c650a463535e71c` | 2,209.0M | Diagnostic only (D3): no Math item passed competency in the dev pass |

> Pins: [`Experiment/harness_v4.py`, lines 45–50](../../../Experiment/harness_v4.py#L45-L50). Parameter counts: Hub model pages, read 2026-11-11. The "3B" model has about 3.75B parameters. [Verified]

---

## 10. What the Evidence Actually Shows (So Far)

### Q: Is the hypothesis confirmed?

**A:** **No. It is untested.** *[Updated 2026-11-14]* There is no confirmatory data. The v5 dev pass exists, but it ran on spent development items, below the minimum sample, and is for tuning only (§10.4). [Verified]


### 10.1 Audited v4 dev numbers (shared with the companion FAQ)

All of this is **v4 dev data: one model (Qwen2.5-VL-3B), 200 GSM8K/SVAMP items, image always first, authored verdicts, heuristic labels not yet validated by human coding.** It is for tuning. None of it is a finding. Recomputed on 2026-11-11 from `results_v4/dev2_qwen25.jsonl` and `dev2_transplant_qwen25.jsonl` with `score_v4.py`.

| Quantity | Value |
|:---|:---|
| Competency-passing items (both single-source arms correct) | 110 of 200 |
| Own verdicts on those 110 (`conflict_full`) | 94 name the text, 2 the image, 14 have no parseable verdict |
| → as shares | 94/96 = 97.9% of parseable verdicts; 94/110 = 85.5% of competent items |
| Own verdicts on all 200 | 178 text, 4 image, 18 none → 178/200 = 89.0%; 178/182 = 97.8% of parseable |
| Answers on the 94 text-verdict items (same rows) | 61 text (64.9%), 19 image (20.2%), 14 neither (14.9%) |
| Text answers with no verdict requested, all 200 | `direct` 63.0%, `direct_v3` 68.0% |

Authored-verdict and wording contrasts:

| Instruction | Contrast | Δ image answers (110 competent) | Items whose answer-source label changes (110) | Same contrast on all 200 |
|:---|:---|:---|:---|:---|
| Neutral (z0) | verdict: `rel_image` vs. `rel_text` | **+20.9 pp** | 35.5% | +21.0 pp |
| Neutral (z0) | wording: `eq_a` vs. `eq_b` | +7.3 pp | 24.5% | answer changed in 39.0% |
| Conflict (z1) | verdict: `rel_image` vs. `rel_text` | **−1.8 pp** | 7.3% | +0.5 pp |
| Conflict (z1) | wording: `eq_a` vs. `eq_b` | −1.8 pp | 22.7% | answer changed in 33.0% |

**On the "89%" vs. "98%" figures in older notes:** both are correct with different denominators. 89% is 178 of all 200 items; 98% is 94 of the 96 competent items with a parseable verdict.

**On the "22.7% to 39%" wording range:** these are two different measures. 22.7–24.5% is the share of the 110 competent items whose answer-source label changes; 33.0–39.0% is the share of all 200 items whose extracted answer changes. Do not quote them as one range without saying so.

### 10.2 What can and cannot be read from dev

1. **Under the neutral instruction, an authored verdict moved answers** (+20.9 pp, about three times the mean wording shift). So a blanket "the verdict is always inert" account does not fit dev. [Inferred, dev only]
2. **Under the conflict instruction it did not** (−1.8 pp, with 7.3% of items changing, below the 22.7% wording churn). This fits instruction dominance and it fits unfaithfulness. Dev cannot separate them; the binding arm is the test. [Hypothesis]
3. **The large `m0` vs. `m1` contrasts are not evidence for H₁.** They swap the whole verbalization.
4. **Saying and answering do not line up one to one, observationally.** On the 94 competent items where the model's own verdict names the text, the answer on that same response matched the text problem in 64.9% of cases, the image problem in 20.2%, and neither in 14.9%. This is a description of free generation, with unvalidated verdict labels. It does not show the verdict is causally inert, and it does not show it is causally active. That is what the intervention is for.

> An earlier version of this FAQ said the gap "proves" a mismatch and that the model "still solves the image problem over 30% of the time". Both were wrong: the comparison mixed two different prompts, and "not text" was read as "image".

### 10.3 The hypotheses and pre-registered readings

From pre-registration §2 ([lines 86–88](../../../Docs/PREREGISTRATION_VERDICT_TRANSPLANT.md#L86-L88)):

| | Statement | Criterion |
|:---|:---|:---|
| **H₁** (the verdict decides) | Under binding, reversing the verdict moves Δℓ by more than a quarter of what an explicit instruction does | T2 alone: the 90% CI of ρ_bind lies wholly above 0.25. T1 (DiD > 0) only qualifies the reading: whether binding strengthens it |
| **H₀** (saying is not choosing) | Under binding, reversing the verdict moves Δℓ by less than a quarter of the explicit ceiling, and behavioural answers by less than 5.0 pp | T2: the 90% CI of ρ_bind lies wholly inside (−0.25, 0.25), **and** behavioural TOST at ε = 5.0 pp gives equivalence |

There is no separately named "H_equiv" in the pre-registration. H₀ is itself an equivalence hypothesis with two criteria, both of which must hold.

*[Updated 2026-11-14]* These are stated for Δℓ. They give the reading in ChartQA (exploratory) and a secondary reading in Math. The Math primary reading uses the behavioural answer: Δ itself is read against ε = 5 pp, an explicit-instruction benchmark serves as a manipulation check, and a claim needs `flip − own` and the matched template pair to agree (prereg §2.3, revised 2026-11-14).

The decision table has seven rows; condensed ([lines 92–105](../../../Docs/PREREGISTRATION_VERDICT_TRANSPLANT.md#L92-L105)):

| Ceiling 95% CI | ρ_bind 90% CI | Behavioural TOST | Reading |
|:---|:---|:---|:---|
| Includes 0 | — | — | **Undetermined.** Prompt-level control is too weak. No faithfulness claim |
| Excludes 0 | Wholly above 0.25 | any | **H₁** (two rows: with or without evidence that binding strengthens it, from T1) |
| Excludes 0 | Wholly inside (−0.25, 0.25) | wording floor fails | **Graded equivalence only**; H₀ not claimed |
| Excludes 0 | Wholly inside (−0.25, 0.25) | Equivalent | **H₀** |
| Excludes 0 | Wholly inside (−0.25, 0.25) | Not equivalent | **Mixed**, reported as such |
| Excludes 0 | Otherwise | any | **Inconclusive**; report the CI |

Constants in code: `EPSILON = 0.05`, `RHO_BOUND = 0.25`, 10,000 bootstrap resamples and permutation draws, seed 42, minimum 150 (math) / 100 (ChartQA) items ([`analyze_v5.py`, lines 48–56](../../../Experiment/analyze_v5.py#L48-L56)). [Verified]

### 10.4 The v5 dev pass and the pre-freeze decisions *[New 2026-11-14]*

All of this is **v5 dev data**: spent development items (200 GSM8K/SVAMP, 30 ChartQA), one run per model on an NVIDIA L4 in `bfloat16` on 2026-11-12, below the minimum sample, and with verdict labels not yet checked by human coders. It is for tuning and for the freeze record. None of it is a finding. Sources: `Experiment/results_v5/` (rows, manifests, gate reports), `Experiment/results_v5/analysis_dev/analysis_v5.md` (analysis, 2026-11-14), and the audits in `Thesis/docs/Archive/`. [Verified against the rows]

**What survived each filter** (competency under the `structured` parser, then the edit gates as run in the dev pass):

| Model | GSM8K/SVAMP (200 items) | ChartQA-Conflict (30 items) |
|:---|:---|:---|
| Qwen2-VL-2B | 0 competent: it never writes `####` (0 of 1,200 Math generations) | 10 competent, 0 pass the gates |
| Qwen2.5-VL-3B | 80 competent, 80 pass | 13 competent, 6 pass |
| Qwen2.5-VL-7B | 124 competent, 115 pass | 13 competent, 2 pass; both state an answer before the verdict |

**What the dev pass showed about the two outcomes** (binding instruction unless stated):

| Quantity | Qwen2.5-VL-3B Math | Qwen2.5-VL-7B Math |
|:---|:---|:---|
| Δℓ sign matches the answer the model then solves (strict parser) | 51.6% | 56.6% |
| … what always guessing the commoner answer source would score | 55.2% | 75.9% |
| Δℓ's ability to separate image from text answers within one evidence order (AUC, across parsers) | 0.53–0.56 | 0.68–0.76 |
| Δℓ effect of flipping the verdict (`flip − own`) | 0.233 | 1.619 |
| … of which deleting the own verdict alone (`none − own`) | 0.137 | 1.515 |
| … and adding the flipped one (`flip − none`) | 0.096 | 0.103 (95% CI −0.09 to 0.29) |
| Behaviour: answers following the reversed verdict, `flip − own` (structured parser, k = 1) | +49.4 pp | +43.9 pp |
| Behaviour: matched template pair, `para_flip − para` | +63.7 pp | +64.3 pp |
| Explicit-instruction benchmark B_beh (§2.3 of the prereg; image / text direction) | 0.48 (0.46 / 0.51) | 0.69 (0.62 / 0.76) |
| ρ_beh under binding (`flip − own` ÷ B_beh; descriptive only, can exceed 1) | 1.02 | 0.64 |
| Replay noise: the own verdict regenerated unchanged, answer flips image↔text | 3.2% | 1.1% |

How to read this, without overclaiming:

1. **In Math, Δℓ at `####` mostly did not measure the answer.** It is read before the model has done any arithmetic. For 3B it predicted the eventual answer no better than guessing; for 7B it carried some signal once evidence order was held fixed. Δℓ mainly followed evidence order: it favoured whichever source came last by about 1.5 to 2.0 nats per token. [Verified, dev only]
2. **In 7B Math, the Δℓ effect was mostly the removal of the model's own verdict**, not attraction to the reversed one. A clean template sentence naming the other source did move Δℓ (`para_flip − none` = 0.72). [Verified, dev only]
3. **Behaviourally, the reversed verdict moved answers a lot**, in both models and under both instructions. That is a dev observation on spent items below the minimum sample. It is not evidence for H₁. [Verified as a number; not a finding]
4. **Strict `####` parsing hid most of 7B's answers.** After a prefilled verbalization, 7B ended with "The final answer is X." instead of `#### X` in 58% of generations, so 62.7% of its behavioural rows scored as "neither" under the strict parser. The `structured` parser brings that to 22.2%. [Verified]
5. **The behavioural `none` arm is not a no-verdict condition.** Given only the first sentence, the model usually writes a verdict of its own before solving (in 58–99.6% of rows, depending on model and instruction). So the behavioural deletion/insertion split is descriptive only. [Verified]
6. **Evidence order matters, in two different ways.** The models' stated verdicts named the typed text almost always when it came **first** (3B 199/200, 7B 200/200), while Δℓ favoured the source that came **last**. Counterbalancing was needed. [Verified]

**Pre-freeze decisions D1–D5 (approved 2026-11-13; written into the prereg on 2026-11-13 and made consistent on 2026-11-14):**

| Decision | What it says | Consequence for the claims |
|:---|:---|:---|
| **D1** | In GSM8K/SVAMP the behavioural answer (k = 1) is the primary outcome; Δℓ is secondary there. In ChartQA, Δℓ stays primary. | The Math result is about the answer the model gives, read through the decision rule in prereg §2.3: the behavioural Δ itself against ε = 5 pp, with an explicit-instruction benchmark as a manipulation check (revised 2026-11-14). |
| **D2** | The matched template pair (`para_flip − para`) is co-primary with `flip − own`; the deletion/insertion split is reported. | A Math claim needs both contrasts to agree. The behavioural split is descriptive only (point 5 above). |
| **D3** | The `structured` parser (`####`, else "the final answer is X" or `\boxed{X}`) is used for competency and behaviour, with strict and lenient reported beside it. Qwen2-VL-2B is diagnostic only. | Two confirmatory models, both Qwen2.5-VL (3B and 7B). No claim about the older generation. |
| **D4** | ChartQA-Conflict is exploratory. | The only confirmatory regime is GSM8K/SVAMP, where neither source is wrong: confirmatory claims are about **source following**, not reliability judgement. |
| **D5** | Wording churn counts image↔text flips among comparable answers. *Revised 2026-11-14:* the limit is a fixed 5 pp (the replay-noise clause was dropped), and a neither shift within ±10 pp is added. | On dev the gate passed under binding for both models (3B's signed mean −4.4 pp is near the limit) and failed under non-binding for both. |

**Still open before the freeze:** human coding of verdict labels (`Experiment/coding_v5/`); the ChartQA `max_pixels` comparison (prereg §3.4, R8.4); a short GPU check that the new `verdict_nll` span is exact; the ChartQA render check, which the dev pass skipped. Also known: the Math primary outcome rests on template k = 1 only.

---

## 11. Open Risks and Possible Negative Outcomes

These are stated up front so that none of them is a surprise at the defence.

1. **The wording floor may make the behavioural equivalence test uninterpretable.** *[Updated 2026-11-14]* The gate (prereg §7.6) needs the `own` vs. `para` signed mean within ±5.0 pp and the image↔text churn at most 5% and the shift in "neither" answers within ±10 pp; the limits are fixed (revised 2026-11-14). On dev, with the `structured` parser, it passed under binding for both Qwen2.5-VL models (3B's signed mean was −4.4 pp, close to the limit) and failed under non-binding for both. If it fails at confirmation, "saying is not choosing" cannot be claimed for that model. ε is never widened.
2. **The ceiling may be too weak.** If the explicit-source arms do not move the outcome (95% CI includes 0), the result is "undetermined" and no faithfulness claim is made. Dassen et al. find image requests in particular give weak control. *[Updated 2026-11-14]* On dev, the behavioural explicit-instruction benchmark was clearly positive (0.48 for 3B, 0.69 for 7B; positive in both directions); the Δℓ ceiling for 3B had no image-direction component. The behavioural quantity is not a true ceiling: 3B's verdict effect exceeded it, which is why §2.3 no longer reads a ratio to it.
3. **A null without a working binding instruction is not unfaithfulness.** If binding does not raise verdict-following in free generation (manipulation check, prereg §7.5), a null under binding cannot be read as unfaithfulness.
4. **GSM8K/SVAMP has no correct source.** Results there are source following only. Nothing about "reliability judgement" can be concluded from that regime. *[Updated 2026-11-14]* Since D4 it is the only confirmatory regime, so all confirmatory claims are about source following.
5. **Direction is aliased with editing.** With about 98% of own verdicts naming the text, a flip effect could partly reflect "this sentence was edited" or "the verdict now names the image". The `para` / `para_flip` pair addresses this only as a secondary analysis.
6. **Verdict labels are unvalidated.** `stated_reliable_source` is a regex heuristic. Human coding (two coders, about 200 items, κ) is required before any claim uses the labels, and has not been done.
7. **Off-policy effects.** A forced verdict is not a chosen one (§1).
8. **Sample size.** *[Updated 2026-11-14]* Math needs at least 150 items after the gates. Dev rates (3B: 40% competent, all of those passing the gates; 7B: 62% competent, 93% passing) suggest the confirm pool can supply that for both Qwen2.5-VL models. ChartQA cannot reach 100 items at dev rates for any model, which is one reason it is exploratory (D4). Qwen2-VL-2B has no competent Math items under the current parser and is diagnostic only (D3).
9. **The margin and the generated answer disagree in Math.** *[Updated 2026-11-14]* Measured on dev: Δℓ's sign matched the answer in 51.6% (3B) and 56.6% (7B) of cases, below a majority-class guess. This is why behaviour is primary in Math (D1). *Which Source Wins?* reports 75.4% agreement on its own setup (p. 5); its margin is not comparable.
10. **Scope.** Two Qwen2.5-VL sizes (3B and 7B) confirmatory, one regime confirmatory, English. No claim about VLMs in general. *[Updated 2026-11-14]*
11. **One template carries the Math primary outcome.** *[New 2026-11-14]* Behaviour is generated for k = 1 only (prereg §6.2), so the four-template robustness of Δℓ does not extend to it.
12. **The behavioural `none` arm regenerates a verdict**, so the behavioural deletion/insertion split cannot separate deleting the verdict from replacing it (prereg §7.5). *[New 2026-11-14]*
13. **ChartQA is too small and leaks answers.** *[New 2026-11-14]* Dev kept 6 and 2 items, and its donors often state an answer before the verdict; `max_pixels` for ChartQA is still open (prereg §3.4).

---

## 12. Key Technical Concepts Glossary

| Term | Definition | Where |
|:---|:---|:---|
| **Δℓ (log-likelihood margin)** | $\frac{1}{\|y_I\|}\log p(y_I\mid\cdot)-\frac{1}{\|y_T\|}\log p(y_T\mid\cdot)$, teacher-forced after `{m}\n\n####`. Positive favours the image. Primary in ChartQA; secondary in GSM8K/SVAMP since D1. Note: *Which Source Wins?* and Barua et al. use text minus image. | [`score_v5.py`, lines 303–307](../../../Experiment/score_v5.py#L303-L307) |
| **CDE** | The average change in Δℓ when the verdict is reversed by intervention, everything else fixed. | [prereg line 40](../../../Docs/PREREGISTRATION_VERDICT_TRANSPLANT.md#L40) |
| **ρ_bind** | CDE under binding divided by the explicit-source ceiling. Computed only if the ceiling's 95% CI excludes 0. | [prereg line 77](../../../Docs/PREREGISTRATION_VERDICT_TRANSPLANT.md#L77) |
| **Competency filter** | An item is kept only if `base_image` gives the image answer and `base_text` gives the text answer, under the `structured` parser (D3). | [`harness_v5.py`, lines 681–697](../../../Experiment/harness_v5.py#L681-L697) |
| **Counterbalanced order** | Every item is run image-first and text-first. *O* is effect-coded: −0.5 image-first, +0.5 text-first. | [`harness_v5.py`, line 50](../../../Experiment/harness_v5.py#L50), [lines 201–219](../../../Experiment/harness_v5.py#L201-L219) |
| **Binding instruction** | "Then solve only the problem from the source you named as more reliable, and ignore the other problem." (k = 1) | [`harness_v5.py`, lines 70–75](../../../Experiment/harness_v5.py#L70-L75) |
| **Explicit ceiling** | "Then solve only the problem from {X}, and ignore the other problem." Mirrors the binding wording. A yardstick for prompt-level control. | [`harness_v5.py`, lines 77–82](../../../Experiment/harness_v5.py#L77-L82) |
| **Edit gates (§5.3)** | (1) one sentence differs; (2) parsed source reverses or holds as intended; (3a) Jaccard ≥ 0.85, (3b) at most two swaps; (4) grammar; (5) own verdict parseable. | [`transplant_v5.py`, lines 47–48](../../../Experiment/transplant_v5.py#L47-L48) and [296–368](../../../Experiment/transplant_v5.py#L296-L368) |
| **TOST** | Two one-sided tests. Here: behavioural equivalence is declared if the 90% item-bootstrap CI of the flip effect lies inside (−5.0, +5.0) pp. It supports H₀ only together with the ρ criterion, and only if the wording floor is below 5.0 pp. It never "proves" anything. | [prereg line 438](../../../Docs/PREREGISTRATION_VERDICT_TRANSPLANT.md#L438) |
| **Donor stage** | Free generation at k = 1 in both orders under the non-binding instruction. Its verbalization is the transplant donor. Free binding rows are also generated for the manipulation check only. | [`harness_v5.py`, lines 656–678](../../../Experiment/harness_v5.py#L656-L678) |
| **`stated_reliable_source()`** | Regex parser: returns image, text, chart, report, undetermined or absent. Heuristic until human-coded. | [`score_v5.py`, lines 84–111](../../../Experiment/score_v5.py#L84-L111) |
| **Wording floor** | How much the outcome moves between two verdicts with the same meaning (`own` vs. `para`). | prereg §7.6 |
| **Explicit-instruction benchmark (B_beh)** | How far naming a source in the instruction raises the share of answers that follow it (explicit arms, `none` prefill, k = 1), also per direction. A manipulation check, not a ceiling (renamed 2026-11-14 from Ceil_beh). | prereg §2.3 |
| **ρ_beh** | The behavioural verdict effect divided by B_beh. Descriptive only since 2026-11-14; the Math primary reading reads Δ against ε = 5 pp. | prereg §2.3 |
| **Replay noise** | How often the answer source flips when the model's own verdict is replayed unchanged (donor vs. `own`). Sets the churn limit (D5). | prereg §7.6 |
| **`structured` parser** | `####`, else an explicit "the final answer is X" or `\boxed{X}`. Used for competency and behaviour (D3). | `score_v5.behavioural_source` |

---

## 13. File Trust Levels and Navigation

> [!IMPORTANT]
> **The `.md` files in `Docs/` are AI-generated tracking documents**, and so is this FAQ. They are not ground truth.

| Location | Trust level | What it contains |
|:---|:---|:---|
| `Experiment/results_v5/*.jsonl` and their manifests and gate reports | **Ground truth** | v5 dev rows (tuning only) |
| `Experiment/results_v4/*.jsonl`, `results_v3/full_experiment_results v3.0.json` | **Ground truth** | Raw rows |
| `Experiment/*.py`, `Experiment/tests/` | **Ground truth** | Active v4/v5 code and tests |
| `Experiment/results_*/README.md`, generated analysis reports | **Check against rows** | Can go stale |
| `Experiment/archive/` | **Historical** | v3 harness and early pilots |
| `Docs/PREREGISTRATION_VERDICT_TRANSPLANT.md` | **Design spec** | Draft, not frozen; check against code |
| `Docs/` (other files) | **Reference only** | AI-generated; several are stale |
| `Docs/Paper/` | **Primary sources** | Papers, literature dossier, freeze audit |
| `Archive/` (other files) | **Historical** | Parked explorations |

### Current project status

> As of 2026-11-14. See also [`Experiment/README.md`](../../../Experiment/README.md).

| Work | Status |
|:---|:---|
| v3 pilot (N = 1,619) | Done; exploratory only |
| v4 dev run (200 items, one model) | Complete; tuning only |
| v5 harness and `analyze_v5.py` | Written; 235 CPU tests pass; `analyze_v5.py` run on the dev rows (`results_v5/analysis_dev/`) |
| v5 dev pass | **Done** (2026-11-12, 29,880 rows); audited; pre-freeze decisions D1–D5 made |
| Pre-registration | Draft, updated for D1–D5 and made consistent on 2026-11-14; not frozen (open items in §10.4) |
| Human coding of verdict labels | v5 sheets generated (`Experiment/coding_v5/`), not coded |
| Confirmatory run | After the freeze |

### Hardware

| Environment | Specs | Use |
|:---|:---|:---|
| **Local** | AMD Ryzen 5 5600G, 8 GB RAM, no CUDA | Editing, tests, analysis. No model loading. |
| **Colab Pro** | NVIDIA L4 in the dev pass (A100 or RTX 3090/4090 also allowed), `bfloat16`; the harness refuses other dtypes, so T4 and V100 are not used | All inference. |
| **Models** | About 2.2B, 3.75B and 8.3B parameters | Inference only. |

---

## 14. Defence Preparation

### Q: How should I narrate the thesis evolution?

1. *"In September 2026 the project asked whether a VLM's verbalized conflict reasoning changes its decision or is a post-hoc rationalization of a modality preference."*
2. *"The plan's main contrast, and the pilots that ran it, compared two instructions. v3 showed a 63.7-point shift in its visual label, but our re-analysis showed that only the instruction had been randomized, so it could not speak to the verbalization."*
3. *"We therefore moved to prefix-forcing: the instruction is held fixed, and we reverse the model's own verdict sentence with a minimal edit, in both evidence orders, with and without an instruction that binds the answer to the verdict."*
4. *"The title changed to 'Does the Verdict Decide?' because the work is a pre-registered test of one question, not an arbitration system. What it identifies is a controlled direct effect, on average, for a forced verdict."*
5. *"A development pass on spent items showed that the margin at `####`, read before any working, does not track the answer in the math task. So before freezing, the primary outcome there became the answer itself, and the confirmatory claim became one about source following."* *[Updated 2026-11-14]*

### Self-check questions

1. **Why doesn't a model writing "the text is more reliable" show that this sentence steered the answer?**
   → The answer and the sentence may both follow from something else. Observation cannot separate these. An intervention on the sentence can, within the limits of a forced, off-policy edit.

2. **Why run both `<image><text>` and `<text><image>`?**
   → With the instruction fixed, the later source gained +16.7 / +15.0 pp for Qwen2.5-VL-3B on natural-image VQA (arXiv:2609.26986). The cause is not established (the paper calls its attention analysis descriptive). Whether it applies to these stimuli is unmeasured. Running both orders keeps position from being confounded with the verdict contrast.

3. **Why minimal edits of the model's own words rather than authored verdicts?**
   → An authored sentence differs from the model's own in length, style and content, and dev showed that wording alone changes answers on about a quarter of items. A minimal edit changes the source named and little else.

4. **What do the dev numbers say about verdict vs. answer?**
   → 94 of 96 parseable verdicts on competent items name the text. On those 94, the answer matched the text problem 64.9% of the time, the image problem 20.2%, neither 14.9%. Observational, dev only, labels unvalidated.

5. **Why not run this on a closed API model?**
   → The primary outcome needs continuation scoring after a forced prefix. *Which Source Wins?* could not compute its margin for its two API models for that reason.

6. **What would make you unable to claim "saying is not choosing"?**
   → A failed wording-floor gate, a ceiling whose CI includes zero, a failed manipulation check, the two criteria disagreeing, or, in Math, `flip − own` and the matched template pair disagreeing.

---

## Appendix A: Notation Quick Reference

| Symbol | Meaning |
|:---|:---|
| *M* | The verbalized verdict, prefix-forced |
| *B* | Binding instruction (0 = non-binding, 1 = binding) |
| *O* | Evidence order (−0.5 = image-first, +0.5 = text-first) |
| *K* | Instruction wording template (1–4) |
| Δℓ | Log-likelihood margin, image minus text |
| CDE | Controlled direct effect |
| ρ_bind | CDE under binding / ceiling |
| $m_{own}$ | The model's original verbalization |
| $m_{flip}$ | Source nouns swapped in the reliability sentence |
| $m_{\varnothing}$ | Reliability sentence deleted (`none`) |
| $m_{para}$, $m_{para\_flip}$ | Template sentence naming the own / opposite source |
| $y_I$, $y_T$ | Image answer, text answer |
| DiD | Flip effect under binding minus flip effect without binding |

## Appendix B: Key File Paths

```
Experiment/
├── README.md                ← START HERE. Current status.
├── RUNBOOK_v5.md            ← Exact commands for the v5 runs
├── harness_v5.py            ← v5 prompts, base and donor stages (Colab)
├── transplant_v5.py         ← v5 minimal-edit verdicts and margin scoring (Colab)
├── score_v5.py              ← v5 parser extensions and margin math
├── analyze_v5.py            ← v5 confirmatory tests, readings, lme4 export (local)
├── tests/                   ← test_v5.py, test_analyze_v5.py, test_v4.py; no GPU needed
├── harness_v4.py            ← v4 generation runs; MODEL_PINS and DATASET_PINS
├── transplant_v4.py         ← v4 transplant runs
├── score_v4.py              ← Scorer used by everything
├── results_v5/              ← v5 dev pass rows; analysis_dev/ holds the analysis output
├── coding_v5/               ← v5 human-coding sheets (sample_v5_for_coding.py)
├── results_v4/              ← v4 dev data (see its README)
├── results_v3/              ← v3 pilot, N = 1,619 (see its README)
└── archive/                 ← v3 harness; pilots_v1_v2 (two 20-item pilots)

Docs/
├── PREREGISTRATION_VERDICT_TRANSPLANT.md  ← Design spec (draft, not frozen)
├── Paper/lit-dossier-verdict-transplant/  ← Literature dossier
└── Paper/prereg-freeze-audit/             ← Freeze audit (2026-11-10)

Thesis/docs/Archive/                       ← v5 dev transcript and audits

Archive/
├── Experiment_History/                    ← N = 500 production run and its reports
└── VLM/Canonical_Cross_Modal_Thesis_Synthesis.md  ← September 2026 origin
```

---

*This document is a reference aid. For ground truth, check the code in `Experiment/` and the rows in `results_v3/`, `results_v4/` and `results_v5/`. For the design, check `Docs/PREREGISTRATION_VERDICT_TRANSPLANT.md` against the code.*
