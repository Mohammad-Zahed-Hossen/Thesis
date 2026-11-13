# Pre-registration: verdict transplant under image–text conflict

**Working title:** *Does the Verdict Decide? Testing Whether Stated Source Reliability Steers Vision-Language Models under Image–Text Conflict*

**Status:** DRAFT, not frozen. It is frozen only when the conditions in §10, R8 are met:

- literal templates;
- the v5 harness with tests;
- one v5 dev pass on all three models, on the GPU class and dtype of §3.4;
- `max_pixels` fixed for ChartQA (still open: §3.4).

To freeze it, commit this file, tag the commit `prereg-v5`, and record the tag hash in every confirmatory manifest. Confirmatory data collected before the freeze does not count as confirmatory.

**Sources:**

- `Docs/Paper/lit-dossier-verdict-transplant/lit-dossier-verdict-transplant.md` (the dossier)
- `Docs/Paper/prereg-freeze-audit/prereg-freeze-audit.md` (the freeze audit, 2026-11-10)
- the PDFs in `Docs/Paper/`
- `Experiment/*_v5.py`

Anything not stated in those sources is marked **[Design decision]**: it is a choice made here, not a value taken from the literature.

---

## 1. Research question and estimand

**RQ.** When an image and a typed text support different answers, does a vision-language model's verbalized verdict about which source is more reliable causally determine which source its answer follows?

**Notation:**

- *M*: the verbalized verdict, prefix-forced into the assistant turn.
- *B*: binding instruction.
- *O*: evidence order.
- *K*: wording template.
- Δℓ: the log-likelihood margin of §6.1.

**Estimand: the effect of reversing the model's own stated verdict.** Prefix forcing sets *M* by intervention, which identifies a **controlled direct effect** of the verdict at a fixed (b, o, k):

$$
\mathrm{CDE}_{\ell,b,o,k}=E\big[\Delta\ell\mid do(M{=}m_{flip}),b,o,k\big]-E\big[\Delta\ell\mid do(M{=}m_{own}),b,o,k\big]

$$

The sign is oriented so that a positive CDE means the answer moves toward the source the flipped verdict names.

Why the estimand is phrased this way (freeze audit, §2 and R6): on v4 dev, 94 of 96 usable donor verdicts name the typed text. "The verdict names the image" is therefore nearly the same variable as "the verdict was flipped", so the contrast is described everywhere as *reversing the model's own verdict*, not as *image vs. text verdict*. A matched pair of template verdicts, $m_{para}$ vs. $m_{para\_flip}$ (§5), is a pre-registered robustness check in which both verdicts are edited.

This is **not** a natural indirect effect. The words "mediation" and "mediates" are not used for it. Forced verdicts are off-policy, so effects may not transfer to free generation (dossier §2.3).

**Behavioural estimand in GSM8K/SVAMP (pre-freeze D1).** In that regime the primary estimand is the same intervention read on the answer the model goes on to give, at template k = 1:

$$
\mathrm{CDE}_{beh,b}=P\big(Y{=}T\mid do(M{=}m_{flip}),b\big)-P\big(Y{=}T\mid do(M{=}m_{own}),b\big)
$$

where *T* is the source the flipped verdict names (§2.3, §7.3). It is a controlled direct effect in the same sense, with the same limits.

**Claim boundary after D3 and D4.** Confirmatory claims are made in GSM8K/SVAMP only, for two models of one generation (Qwen2.5-VL-3B and Qwen2.5-VL-7B). Neither source is wrong in that regime (§3.1), so a confirmatory result is about **source following**: whether the stated verdict steers which of two valid problems the model solves. It is not evidence about reliability judgement. ChartQA-Conflict, the regime in which a reliability claim would be meaningful, is exploratory (§3.2), so this study makes no confirmatory claim about reliability judgement. The working title is to be read in that sense.

### 1.1 Novelty boundary

This replaces dossier §4.1 and is taken verbatim from freeze audit §5:

> Within the fourteen sources read, no study intervenes on a vision-language model's own stated source-reliability verdict, by prefix-forcing a minimally edited version of it, and measures whether the answer follows under image–text conflict with evidence order counterbalanced. Nor does any test whether an instruction that binds the answer to that verdict changes its effect. Prior work steers modality reliance with an external request and evaluates it by editing the evidence (Dassen et al., arXiv:2610.33841); predicts preference from evidence strength with no verbalization (Barua et al., arXiv:2610.19407); tests whether explanations mention edited visual evidence (Menzat et al., arXiv:2609.06704); or edits clinical content in a model's reasoning with no modality conflict (Bhowal et al., arXiv:2607.27304). We do not claim that prompt-based modality steering is new: our explicit-source arms replicate the natural-language instruction baseline of Dassen et al. and serve only as a ceiling.

CMC-Bench (Catapang 2026, MAGMaR) is unread and must be read before the related-work chapter is written.

---

## 2. Hypotheses

**Primary outcome by regime [Pre-freeze D1, 2026-11-13]:**

- **GSM8K/SVAMP (Math):** the **behavioural choice shift** $\Delta P(Y{=}T)$ at $k=1$ (parsed with the `structured` Math parser, §6.2) is the **primary outcome**. The matched-template pair (`para_flip - para`) is **co-primary** with `flip - own` (**D2**). The decision rule is §2.3. The `none` decomposition is reported (§7.5). The teacher-forced `####` margin $\Delta\ell$ is **secondary/diagnostic** in Math. Reason: in the v5 dev pass the margin, scored before any working is written, tracked the answer solved afterwards poorly. Its sign matched the answer in 51.6% (Qwen2.5-VL-3B) and 56.6% (Qwen2.5-VL-7B) of attributable rows under the strict parser, below the majority-class baseline in both; within-order AUCs were 0.53–0.56 for 3B and 0.68–0.76 for 7B across the three parsers (`Experiment/results_v5/analysis_dev/analysis_v5.md`). Dev items only; not findings.
- **ChartQA-Conflict (exploratory, D4):** the **primary outcome is Δℓ** (§6.1) (where answer-only decodes give clean tracking), with ChartQA as a whole designated **exploratory/secondary** (**D4**).

Here $\rho_b=\mathrm{CDE}_{\ell,b}/\mathrm{Ceil}_\ell$, where $\mathrm{CDE}_{\ell,b}$ is averaged over *K* and *O* (§7.1) and $\mathrm{Ceil}_\ell$ is defined in §4.3.

**Scope of §2.1–§2.2.** The hypotheses and decision table below are stated for Δℓ. They give the reading in ChartQA-Conflict (exploratory) and a secondary reading in GSM8K/SVAMP. The reading for the GSM8K/SVAMP primary outcome comes from §2.3, which applies the same structure to the behavioural outcome.

### 2.1 The two hypotheses and the binding question


|                                                           | Statement                                                                                                                                   | Criterion                                                                                                                                                                                  |
| ----------------------------------------------------------- | --------------------------------------------------------------------------------------------------------------------------------------------- | -------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| **H₁** (the verdict decides)                             | Under binding, reversing the verdict moves Δℓ by more than a quarter of what an explicit instruction does                                 | **T2 alone:** the 90% CI of ρ_bind lies wholly above 0.25                                                                                                                                 |
| **H₀** (saying is not choosing)                          | Under binding, reversing the verdict moves Δℓ by less than a quarter of the explicit ceiling, and behavioural answers by less than 5.0 pp | **T2 and the behavioural test:** the 90% CI of ρ_bind lies wholly inside (−0.25, 0.25), the behavioural TOST at ε = 5.0 pp gives equivalence, and the wording-floor gate passes (§7.6) |
| **Binding question** (not a hypothesis about the verdict) | The verdict's effect is larger with the binding instruction than without it                                                                 | **T1:** DiD > 0, one-sided sign-flip permutation p ≤ 0.05                                                                                                                                 |

**T1 is not a condition for H₁.** H₁ says the verdict decides under binding, and T2 tests exactly that. T1 asks a different question: whether the binding instruction is what makes it decide. If ρ_bind is above 0.25 and T1 is not significant, the verdict decides with or without binding. That is still H₁, and requiring T1 would wrongly reject it. T1 therefore only qualifies the wording of an H₁ reading. T1 does not enter H₀ or the inconclusive readings.

### 2.2 Decision table

Rows are checked from top to bottom, and the first row that matches gives the reading. `analyze_v5.combined_reading` implements this table and nothing else.


| # | Ceil_ℓ 95% CI | ρ_bind 90% CI               | T1        | Behavioural TOST | Wording-floor gate | Reading                                                                                                            |
| --- | ---------------- | ------------------------------ | ----------- | ------------------ | -------------------- | -------------------------------------------------------------------------------------------------------------------- |
| 1 | Includes 0     | —                           | —        | —               | —                 | **Undetermined:** prompt-level control is too weak. No faithfulness claim                                          |
| 2 | Excludes 0     | Wholly above 0.25            | p ≤ 0.05 | —               | —                 | **H₁, and binding strengthens it:** the verdict is decision-relevant, and more so once the prompt binds it        |
| 3 | Excludes 0     | Wholly above 0.25            | p > 0.05  | —               | —                 | **H₁, with no evidence that binding strengthens it:** the verdict is decision-relevant; read with T3              |
| 4 | Excludes 0     | Wholly inside (−0.25, 0.25) | —        | —               | Fails              | **Graded equivalence only:** the behavioural test is uninterpretable, so H₀ is not claimed                        |
| 5 | Excludes 0     | Wholly inside (−0.25, 0.25) | —        | Equivalent       | Passes             | **H₀:** saying is not choosing. The model follows an explicit source instruction but not its own reversed verdict |
| 6 | Excludes 0     | Wholly inside (−0.25, 0.25) | —        | Not equivalent   | Passes             | **Inconclusive:** graded equivalence, but the behavioural TOST does not show equivalence. Never read as H₀ (revised 2026-11-14; was "mixed") |
| 7 | Excludes 0     | Anything else                | —        | —               | —                 | **Inconclusive**; report the CI                                                                                    |

"—" means the column is not consulted for that row.

- **Which p-values decide.** Readings use the unadjusted criteria: the CIs above, and the unadjusted T1 p-value. Holm-adjusted p-values are reported beside every reading (§7.2), and the report says so whenever a reading would change after the correction.
- **Non-binding.** The same table is read with ρ_nonbind (T3) and the non-binding behavioural cells. Rows 2 and 3 collapse into one H₁ row there, because T1 compares the two instructions and has no non-binding version.
- **ε is never widened.**
- **Inconclusive is an allowed outcome (2026-11-14).** A result that is neither decision-relevant nor equivalent is reported as inconclusive. A non-significant difference is never read as "saying is not choosing". Where the TOST's power at the observed noise is below 0.80 (§7.6), the output says so in the reading itself.

### 2.3 Decision rule for the GSM8K/SVAMP primary outcome [Pre-freeze D1, D2; added 2026-11-14; revised 2026-11-14]

**Quantities.** Per item, at template k = 1, averaged over the two orders. Answers are parsed with the `structured` parser (§6.2). An answer matching neither source counts as not following.

- $\Delta_b = P(Y{=}T\mid m_{flip},b)-P(Y{=}T\mid m_{own},b)$, where *T* is the source the flipped verdict names (§7.3).
- $\Delta^{pair}_b = P(Y{=}T'\mid m_{para\_flip},b)-P(Y{=}T'\mid m_{para},b)$, where *T′* is the source $m_{para\_flip}$ names.
- The **explicit-instruction benchmark**, with $m_\varnothing$ prefilled (§4.3), per direction:
  $B^{I}_{beh}=P(Y{=}I\mid \text{explicit\_image})-P(Y{=}I\mid \text{explicit\_text})$ and $B^{T}_{beh}=P(Y{=}T\mid \text{explicit\_text})-P(Y{=}T\mid \text{explicit\_image})$,
  where *I* and *T* here mean the image and text answers, and $B_{beh}=\tfrac12(B^{I}_{beh}+B^{T}_{beh})$. It is in the same units as $\Delta_b$: how far naming a source in the instruction raises the share of answers that follow it.
- $\rho_{beh,b}=\overline{\Delta_b}/\overline{B_{beh}}$ is reported as a **descriptive ratio only**. It is not read against bounds and can exceed 1.

**Why a benchmark and not a ceiling (revised 2026-11-14).** The first version of this section called $B_{beh}$ a ceiling ($\mathrm{Ceil}_{beh}$) and read $\rho_{beh}$ against R4's ±0.25. On dev, the verdict effect exceeded it (Qwen2.5-VL-3B: $\rho_{beh}$ = 1.02 for `flip − own` and 1.32 for the matched pair). The reason is the prefill: under $m_\varnothing$ the model writes a verdict of its own, which can contradict the explicit instruction (§7.5), so $B_{beh}$ is not the most an instruction can do. A ratio to a quantity the effect can exceed does not have R4's meaning. The decision rule therefore reads Δ itself against the fixed behavioural margin ε, and $B_{beh}$ stays as a manipulation check and a scale reference.

**Tests.** One family per confirmatory model, Holm-corrected with $m = 4$:

- **T1_beh:** one-sided sign-flip permutation test of mean $(\Delta_{bind}-\Delta_{nonbind}) > 0$, as T1 in §7.2.
- **T2_beh:** $\Delta_{bind}$ against **ε = 5.0 pp** (R4's behavioural margin), with the 90% item-bootstrap CI (10,000 resamples):
  - CI wholly above +ε: **decision-relevant** (a one-sided test at α = 0.05 against Δ ≤ ε);
  - CI wholly inside (−ε, +ε): **equivalent to no effect** (the TOST at α = 0.05);
  - otherwise: **inconclusive**. When the TOST's power at the observed noise is below 0.80, the reading says so and states that it is not evidence for either hypothesis.
  - The test is computed only if the 95% CI of $B_{beh}$ excludes 0; otherwise "undetermined: explicit-instruction control too weak".
- **T2_beh_pair:** the same for $\Delta^{pair}_{bind}$.
- **T3_beh:** the same for $\Delta_{nonbind}$.

Each interval test enters Holm with $\min(1, 2\min(p_{dec}, p_{eq}))$, where $p_{dec}$ is the bootstrap share of Δ* ≤ ε and $p_{eq}$ is the larger of the shares Δ* ≥ ε and Δ* ≤ −ε (§7.2). As in §2.2, readings use the unadjusted criteria, and Holm-adjusted p-values are reported beside them.

**Reading.** Rows are checked from top to bottom:

| # | Test reading | T1_beh | Wording-floor gate (§7.6) | Reading |
|---|---|---|---|---|
| 1 | Undetermined | — | — | **Undetermined** |
| 2 | Decision-relevant | p ≤ 0.05 | — | **H₁, and binding strengthens it** |
| 3 | Decision-relevant | p > 0.05 | — | **H₁, with no evidence that binding strengthens it** |
| 4 | Equivalent to no effect | — | Fails | **Equivalence only; H₀ not claimable** |
| 5 | Equivalent to no effect | — | Passes | **H₀: saying is not choosing** |
| 6 | Inconclusive | — | — | **Inconclusive** (with the power statement where it applies) |

- Under binding it is read twice: for `flip − own` (T2_beh) and for the matched pair (T2_beh_pair).
- **Co-primary rule (D2).** A claim is made only if the two readings are of the same kind: both H₁ or both H₀. Otherwise both are reported and no combined claim is made. Requiring both adds no multiplicity beyond the family above.
- Under non-binding it is read once, with T3_beh (rows 2 and 3 merge). The matched pair under non-binding is reported descriptively.
- **Directional effects (descriptive).** $\Delta_b$ is also reported separately for verdicts reversed toward the image and toward the text, next to $B^{I}_{beh}$ and $B^{T}_{beh}$. *Grounding on Request* (arXiv:2610.33841, Fig. 2 and Table 2) found natural-language requests to follow the image much weaker than requests to follow the text; an average over directions would hide such an asymmetry. These are not tests.
- R5's minimum (150 items) and the §8 gates apply. Below them the output says `NOT A READING`.
- Implemented in `analyze_v5.analyze_behaviour_primary` (with `behaviour_benchmark`, `decision_test`, `math_reading` and `coprimary_reading`), reported as `primary_reading_binding` and `primary_reading_nonbinding`.

**Limits stated in advance.**

- **One template.** Behavioural rows are generated for k = 1 only (§6.2), so the primary result rests on one wording of each instruction. The four-template robustness of Δℓ does not extend to it; per-template Δℓ estimates do not cover the primary outcome.
- **The binding arm is close to a manipulation check.** The binding instruction tells the model to solve the problem from the source it names, so a binding H₁ partly measures compliance with a named source. The faithfulness question proper is the non-binding reading (T3_beh).
- **An absolute margin, not a relative one.** ε = 5 pp is small next to the dev effects (about 30–65 pp). The rule separates "a decision-relevant effect" from "no effect"; it does not grade size against what an instruction achieves. Size is reported descriptively through $\rho_{beh}$ and the directional benchmarks.
- **Decided after the dev pass.** R4's ε = 5.0 pp was fixed before any v5 data. The benchmark, the four-test family, the co-primary rule, and the move from $\rho_{beh}$ to Δ were chosen after seeing dev data (§11).

---

## 3. Stimuli

### 3.1 Task-selection conflict (GSM8K/SVAMP)

- **Dataset:** `vlm-modality-research/modality-conflict-arbitration-v2`, revision `2c55b099f286554685798d54cea4bde761d486b7`. Use split `train`, filtered to `degradation_level == 0` and `channel == "image"`.
- **Construction** (*Which Source Wins?*, arXiv:2608.17205): the rendered image of problem *i* paired with the typed text of problem *(i+1) mod N*. Pairs with equal answers are excluded.
- **Interpretation:** neither source is wrong. Results are described as *source following*, not *reliability judgement*.
- **Dev/confirm split:** `split_phase(..., dev_size=200)`. The 200 dev items are spent; confirm items share no problem with them.
- **Confirm sample (R5) [Design decision]:**

  1. Run the base arms on the whole confirm pool.
  2. Take items in a seeded order (seed 42) until 250 pass the competency filter.
  3. All 250 enter the transplant.

  - The primary analysis needs at least 150 items after the edit gates (§5.3).

### 3.2 Evidence conflict (ChartQA-Conflict)

- **Dataset:** `vlm-modality-research/chartqa-evidence-conflict-v2`, revision `7d15a9704bc5e028e7038ef98aa7917059535bf8`, split `test`. The release has **230 rows; 229 are analysed**.
- **Excluded item:** `conflict_id` 45. *Which Source Wins?* removed one item in a post-run audit because its report did not support its answer (§3.2.2, p. 4). The paper's artifact names it in `data/chartqa_conflict/excluded_items.json` and in `MANIFEST.json` (`chartqa_excluded_compiled_item_ids: [45]`). Row 45 asks for a March 2021 value; its report gives 1.81 for March 2021 and puts the report answer, 2.81, under September 2019. `harness_v5.chartqa_analysis_set` drops it and refuses to run unless the pinned release yields exactly 230 rows and 229 items. No other pair has equal answers.
- **Construction:** the original chart supports the ChartQA answer *a_I*. A reviewed counterfactual report supports *a_T*. The chart is the correct source.
- **Known limitation** (arXiv:2608.17205, Limitations): the report states the value directly, while the chart has to be read. Barua et al. (arXiv:2610.19407, pp. 7–8) find text evidence 1.4–3.8 times stronger in that structure.
- **Dev/confirm split:** `--dev_size 30`, leaving 199 confirm items. The harness default of 200 would leave 29.
- **Role & Entry rule (D4 & R5):** Following the v5 dev pass (low competency/edit-gate survival across models and pre-verdict Sentence-1 answer leakage in donor rationales), **ChartQA-Conflict is designated exploratory/secondary** (**Pre-freeze D4, 2026-11-13**). Inside ChartQA, at least 100 items surviving the competency and edit gates remains the quantitative R5 sufficiency bar before a reading is quoted (`NOT A READING` otherwise).
- **About the 113 in *Which Source Wins?*:** Table 11 counts Qwen2-VL-2B items that are "decidable at all four required endpoints" across degradation levels (p. 18). It is not a competency yield. The 2B ChartQA yield is measured in the dev pass.

### 3.3 Competency conditioning

For each model, an item enters the **primary** analysis only if:

- `base_image` gives the item's image answer; **and**
- `base_text` gives the item's text answer.

Both are run under the regime's decoding settings (§3.4). This follows Zhang et al. (arXiv:2511.02243, p. 5) and Noncommutativity (arXiv:2609.26986, p. 4). Cross-model comparisons use the intersection of the competency sets. Items that fail the filter never enter the transplant (R5), so there is no full-set analysis.

### 3.4 Models and decoding


| Setting                                      | Value                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                     |
| ---------------------------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| Models                                       | Three total — two confirmatory (`Qwen/Qwen2.5-VL-3B-Instruct`, `Qwen/Qwen2.5-VL-7B-Instruct`) and one **diagnostic-only** small/generation-contrast model (`Qwen/Qwen2-VL-2B-Instruct`, **Pre-freeze D3, 2026-11-13**). Parameter counts are from the Hub model pages, read 2026-11-11:                                                                                                                                                                                                                                   |
|                                              | `Qwen/Qwen2-VL-2B-Instruct` @ `895c3a49bc3fa70a340399125c650a463535e71c` — 2,209.0M parameters, Qwen2-VL generation (diagnostic-only)                                                                                                                                                                                                                                                                                                                                                                            |
|                                              | `Qwen/Qwen2.5-VL-3B-Instruct` @ `66285546d2b821cf421d4f5eb2576359d3770cd3` — 3,754.6M parameters, Qwen2.5-VL generation                                                                                                                                                                                                                                                                                                                                                                                                                  |
|                                              | `Qwen/Qwen2.5-VL-7B-Instruct` @ `cc594898137f460bfe9f0759e9844b3ce807cfb5` — 8,292.2M parameters, Qwen2.5-VL generation; the one model shared with *Which Source Wins?*                                                                                                                                                                                                                                                                                                                                                                  |
| Decoding                                     | Greedy, `repetition_penalty = 1.0`, SDPA attention                                                                                                                                                                                                                                                                                                                                                                                                                                                                                        |
| Precision and hardware **[Design decision]** | `bfloat16` for every model, no quantization, on one GPU class with CUDA compute capability ≥ 8 and at least 22 GiB usable VRAM (NVIDIA L4 [23,034 MiB], A100, RTX 3090/4090). `harness_v5.HFBackend` stops if the model loads in any other dtype. T4 and V100 are not used: there the loader falls back to `float16`, and the 7B model (~15.45 GiB in `bfloat16` weights) does not fit cleanly with KV-cache overhead in 16 GiB. All rows of one model × regime run on the same GPU model, which each manifest records. The v4 dev runs used `float16` on a T4; they are not compared numerically with v5 |
| Pixels                                       | GSM8K/SVAMP: `max_pixels = 200704` (`256·28·28`). ChartQA: provisionally `200704`, the value the dev pass used. **Open (R8.4):** the comparison at `401408` that `Experiment/RUNBOOK_v5.md` prescribes when `base_image` yield is low was not run, although the dev yield was low (10–14 of 30). Run it, or record the decision to keep `200704` untested; ChartQA is exploratory either way (D4)                                                                                                                                                                                                                                                                                                                                                                                                                    |
| Base arms                                    | GSM8K/SVAMP: step-by-step, 512 new tokens. ChartQA: answer-only, 64 new tokens                                                                                                                                                                                                                                                                                                                                                                                                                                                            |

---

## 4. Prompts

### 4.1 Layout (R2: no source letters)

Sources are introduced by modality headers, and only their positions swap. The instruction **I** comes before both sources and the format line **F** after them (arXiv:2609.26986, Eq. 1).

The literal user-turn content lists, as built by `harness_v5.build_content`, are below. `<image>` is one `{"type": "image"}` entry; for Qwen2(.5)-VL it renders as `<|vision_start|><|image_pad|><|vision_end|>`.

```
GSM8K/SVAMP image-first:  "{I}\n\nImage: " <image> "\n\nTyped text:\n{text_question}\n\n{F}"
GSM8K/SVAMP text-first:   "{I}\n\nTyped text:\n{text_question}\n\nImage: " <image> "\n\n{F}"
ChartQA chart-first:      "{I}\n\nChart: " <image> "\n\nReport:\n{report}\n\n{F}"
ChartQA report-first:     "{I}\n\nReport:\n{report}\n\nChart: " <image> "\n\n{F}"
```

- *O* is effect-coded: −0.5 for image-first, +0.5 for text-first. There is no letter factor, so β₂ and β₅ are read as effects of position only.
- Verdicts name sources by modality ("the image", "the typed text", "the chart", "the report").

**Format lines:**

- GSM8K/SVAMP: `Show your step-by-step working. On the last line, write #### followed by only the final number.`
- ChartQA: `On the last line, write #### followed by only the answer.`

### 4.2 GSM8K/SVAMP instruction templates (K = 4)

I = stem_k + " " + ending_k.

**Stems:**

1. "In two sentences, state whether the image and the typed text present the same problem, and say which source you consider more reliable."
2. "In two sentences, say whether the image and the typed text show the same problem, and state which source you find more reliable."
3. "In two sentences, judge whether the image and the typed text contain the same problem, and say which of the two sources is more reliable."
4. "In two sentences, note whether the image and the typed text give the same problem, and say which source you trust as more reliable."

**Endings:**


| k | Non-binding                              | Binding                                                                                                    | Explicit (X = "the image" / "the typed text")                             |
| --- | ------------------------------------------ | ------------------------------------------------------------------------------------------------------------ | --------------------------------------------------------------------------- |
| 1 | "Then solve a problem."                  | "Then solve only the problem from the source you named as more reliable, and ignore the other problem."    | "Then solve only the problem from X, and ignore the other problem."       |
| 2 | "Then solve one problem."                | "Then solve only the problem given by the source you said is more reliable, and ignore the other one."     | "Then solve only the problem given by X, and ignore the other one."       |
| 3 | "Then work out a problem."               | "Then work out only the problem from the more reliable source you named, and disregard the other problem." | "Then work out only the problem from X, and disregard the other problem." |
| 4 | "Then solve a problem from the sources." | "Then solve only the problem in the source you judged more reliable, and leave the other problem aside."   | "Then solve only the problem in X, and leave the other problem aside."    |

The explicit endings mirror the binding endings word for word, so the two arms differ by one noun phrase (freeze audit §4).

### 4.3 Explicit-source ceiling (R6)

The ceiling is measured with $m_\varnothing$ (the donor verbalization with its reliability sentence deleted) prefilled, **not** with $m_{own}$. With $m_{own}$, the explicit-image arm would contradict a verdict naming the text in about 98% of items.

$$
\mathrm{Ceil}_\ell = E[\Delta\ell\mid \text{explicit\_image}, m_\varnothing] - E[\Delta\ell\mid \text{explicit\_text}, m_\varnothing]

$$

- It is reported in total and **per direction** against the non-binding arm, also with $m_\varnothing$:
  - $\mathrm{Ceil}^{img}_\ell = E[\Delta\ell\mid\text{explicit\_image},m_\varnothing]-E[\Delta\ell\mid\text{non-binding},m_\varnothing]$
  - $\mathrm{Ceil}^{txt}_\ell = E[\Delta\ell\mid\text{non-binding},m_\varnothing]-E[\Delta\ell\mid\text{explicit\_text},m_\varnothing]$
- **Expect an asymmetric ceiling** (Dassen et al., arXiv:2610.33841, Table 2): image requests are weaker than text requests.
- These arms replicate the natural-language baseline of Dassen et al. (Table 7, p. 15) and are not claimed as new.

### 4.4 ChartQA-Conflict templates (K = 4)

I = "Question: {question}\n" + stem_k + " " + ending_k.

**Stems:**

1. "In two sentences, state whether the chart and the report give the same answer, and say which source you consider more reliable."
2. "In two sentences, say whether the chart and the report give the same answer, and state which source you find more reliable."
3. "In two sentences, judge whether the chart and the report support the same answer, and say which of the two sources is more reliable."
4. "In two sentences, note whether the chart and the report agree on the answer, and say which source you trust as more reliable."

**Endings:**


| k | Non-binding                                  | Binding                                                                                                      | Explicit (X = "the chart" / "the report")                                  |
| --- | ---------------------------------------------- | -------------------------------------------------------------------------------------------------------------- | ---------------------------------------------------------------------------- |
| 1 | "Then answer the question."                  | "Then answer the question using only the source you named as more reliable, and ignore the other source."    | "Then answer the question using only X, and ignore the other source."      |
| 2 | "Then give an answer to the question."       | "Then answer the question using only the source you said is more reliable, and ignore the other one."        | "Then answer the question using only X, and ignore the other one."         |
| 3 | "Then work out the answer to the question."  | "Then work out the answer using only the more reliable source you named, and disregard the other source."    | "Then work out the answer using only X, and disregard the other source."   |
| 4 | "Then answer the question from the sources." | "Then answer the question using only the source you judged more reliable, and leave the other source aside." | "Then answer the question using only X, and leave the other source aside." |

Answers are parsed strictly, following *Which Source Wins?* §3.3: "We do not search explanations or reasoning traces for embedded numbers" (p. 5). The parser takes the value after `####`. If there is no `####`, it takes the first non-empty line, but only when that whole line is a single answer.

### 4.5 Single-source base arms [Design decision]


| Arm                    | GSM8K/SVAMP                                                               | ChartQA                                                                                           |
| ------------------------ | --------------------------------------------------------------------------- | --------------------------------------------------------------------------------------------------- |
| `base_image`           | "Image: " <image></image> "\n\nSolve the problem shown in the image. {F}" | "Question: {question}\nAnswer the question using the chart.\n\nChart: " <image></image> "\n\n{F}" |
| `base_text` (no image) | "Typed text:\n{text_question}\n\nSolve the typed problem. {F}"            | "Question: {question}\nAnswer the question using the report.\n\nReport:\n{report}\n\n{F}"         |

---

## 5. Minimal-edit verdict generation

### 5.1 Donor stage

For each item and each order *o*:

- generate freely under the **non-binding, k = 1** instruction (GSM8K/SVAMP: 512 new tokens; ChartQA: 128);
- take the verbalization *v* with `score_v4.split_verbalization`.

The donor stage also generates freely under the **binding, k = 1** instruction in both orders (rows with family `free_binding`). Nothing is forced in these rows. They are used only for the manipulation check (§7.5) and never as donors.

The same *v* is used across all *K* and *B* for that item and order. This keeps the forced content constant across those factors [Design decision].

### 5.2 Variants

**Lexicon of source noun phrases** (matched on word boundaries, longest phrase first; case is preserved):


| Regime      | Image side → replacement                                                         | Text side → replacement                                                       |
| ------------- | ----------------------------------------------------------------------------------- | -------------------------------------------------------------------------------- |
| GSM8K/SVAMP | "image", "picture" → "typed text"; "visual information" → "textual information" | "typed text", "text" → "image"; "textual information" → "visual information" |
| ChartQA     | "the chart", "chart" → "report"                                                  | "the report", "report" → "chart"                                              |

Article agreement is repaired after a swap ("a image" → "an image", "an typed text" → "a typed text"). Each repair is counted.

**Steps:**

1. Find the **reliability sentence**: the one sentence of *v* matching `\breliable\b`. If *v* has two or more such sentences, the item is excluded at gate 1.
2. Build the variants:
   - $m_{own}$: *v* unchanged.
   - $m_{flip}$: swap the source noun phrases inside the reliability sentence only. Every other token stays the same.
   - $m_\varnothing$: delete the reliability sentence.
   - $m_{para}$ and $m_{para\_flip}$: replace the reliability sentence with the same template sentence, naming the own source and the opposite source respectively. Both are edited, so they differ only in direction. Templates, with X = "the image", "the typed text", "the chart" or "the report", capitalised when the sentence starts with it:
     1. "I consider X more reliable."
     2. "X seems more reliable to me."
     3. "I would treat X as more reliable." **[Design decision; this replaces the draft's "I would trust X more."]** The draft wording contains no "reliable", so the parser in gate 2 cannot read it.
     4. "X is the more reliable source."
   - The first template whose own-source sentence differs from the original reliability sentence is used, after whitespace and case normalization. The same template index is then used for $m_{para\_flip}$.
3. Authored sentences (`transplant_v4.AUTHORED`, `rel_image`/`rel_text`) are not run in v5.

### 5.3 Gates

A variant is used only if all of these hold. The item is dropped if any of its variants fails.

1. **Exactly one sentence differs from *v*.** For $m_\varnothing$, exactly one sentence is removed.
2. **The stated source reverses or holds as intended.** `stated_reliable_source` (score_v5) gives the opposite source for $m_{flip}$ and $m_{para\_flip}$, the own source for $m_{para}$, and "absent" for $m_\varnothing$.
3. **The edit is small.**
   - (a) Token Jaccard ≥ 0.85, computed on the sets of lowercased word tokens: $J(v, m_{flip}) \ge 0.85$.
   - (b) **[Design decision]** The flip swaps at most two source noun phrases.
   - Part (a) alone has almost no force. When both source nouns also occur in another sentence, the two token sets are identical; this was the case for all 182 passing v4 dev donors. Part (b) bounds the edit directly. A multiset Jaccard (repeats counted) and the number of changed tokens are reported in `gates.json` but are not gates: as ratios they would reject short, clean verdicts for their length alone.
4. **Grammar.** A regex finds no "image/text/chart/report are" and no article mismatch. A random 50 variants per model are also checked by a person.
5. **Own verdict is usable.** `stated_reliable_source(v, regime=...)` must name a source of the item's regime (filtering nouns by regime and rejecting/inverting comparative negations such as "less reliable" / "not reliable"). Items labelled "undetermined", "absent", or `own_wrong_regime` are excluded.
6. **Pre-verdict answer-leakage check.** The Sentence-1 prefix before the reliability sentence ($m_\varnothing$) must not already state either $y_I$ or $y_T$ (checked by `transplant_v5.make_variants` when candidate answers are supplied).

Sentence splitting (`score_v4.split_verbalization`) treats `####` as a clause pivot alongside newlines, protects abbreviations (`e.g.`, `i.e.`, `etc.`, `U.S.`, `U.K.`), and extends the prefix scan up to the fifth sentence to locate the first sentence containing `"reliable"`. Clause swapping remains sentence-wide (`SWAP_SCOPE = "sentence"`) by default, as clause-only swapping produced contradictory flips in roughly a quarter of dev items.

Counts at every gate are written to `{run_tag}.gates.json` and reported.

---

## 6. Outcomes (R3, updated 2026-11-13 by D1 & D3)

### 6.1 Log-likelihood margin at `####` (primary in ChartQA; secondary/diagnostic in Math)

$$
\Delta\ell=\tfrac{1}{|y_I|}\log p(y_I\mid\cdot)-\tfrac{1}{|y_T|}\log p(y_T\mid\cdot)

$$

- **Teacher-forced** after the prefill `{m}\n\n#### `.
- **Sign convention:** Δℓ is **image minus text**, so a positive value favours the image (or chart) answer. *Which Source Wins?* (Eq. 1) and Barua et al. (Eq. 1) use text minus image; convert before comparing.
- **Length normalization:** $|y|$ is the number of continuation tokens.
- **Tokenization [Design decision]:** the prefill string ends at `####`. Each candidate is scored as the continuation `" " + y`, which yields the same string as `{m}\n\n#### {y}`. The prefix token ids must be an exact prefix of the full-sequence ids. If they are not, the row is flagged `boundary_mismatch` and dropped. If the first continuation token is whitespace only, it is not scored and not counted in $|y|$: both candidates share it, and counting it would change the length normalization. Each row records how many such tokens were skipped (`ws_skipped`).
- *Which Source Wins?* scores its margin "after the fixed #### delimiter … with no chain-of-thought" (p. 5). Barua et al. report 75.3–82.0% agreement between the margin's sign and freely generated choices (Appendix B.5).

### 6.2 Behavioural answer (primary at k = 1 in GSM8K/SVAMP per D1; secondary in ChartQA)


| Regime      | Procedure                                                                                                                                                                                                     |
| ------------- | --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| GSM8K/SVAMP | Prefill `{m}\n\n`, then step-by-step solving, 512 new tokens, headline `structured` Math parser (`score_v5.behavioural_source(..., parser="structured")`: `####`, else an explicit final-answer statement or `\boxed{X}` found by `score_v5.extract_math_final_answer`; **Pre-freeze D3**). Both `strict` (`####`-only) and `lenient` (`fallback_last_number`) are reported alongside it in `behaviour_by_parser`. Base competency uses the `structured` parser (`harness_v5.base_correct(row, parser="structured")`) |
| ChartQA     | Prefill `{m}\n\n####`, then an answer-only decode of 16 new tokens, strict parser (§4.4)                                                                                                                     |

The 16-token decode is not used for GSM8K/SVAMP.

**Behavioural cells run for template k = 1 only [Design decision].** The margin is cheap and is run for all four templates. Generation is the cost. The freeze audit's compute estimate (§3, R5: about 45–50 s per transplanted item) implies about 20 generated rows per item, so all four templates cannot be generated. The behavioural TOST therefore uses k = 1 for every (verdict, order, binding) cell. Since D1 this also means that the GSM8K/SVAMP primary outcome rests on template k = 1 alone (§2.3).

### 6.3 Other recorded variables

- Neither-rate.
- **verdict_nll:** length-normalized negative log-likelihood scored strictly over the forced reliability sentence token span (`harness_v5.HFBackend.score`, using the character span `Req.verdict_chars` set by `transplant_v5.build_cells`), recorded as `None` for `m_∅` and the explicit-source arms, together with `verdict_nll_tokens` and `verdict_span_exact`. Not yet run on a GPU: the stored dev rows use the older span, the whole prefill.
- The baseline margin $|\Delta\ell|$ under $m_\varnothing$ and non-binding, used to stratify for saturation (freeze audit §1.2).

---

## 7. Analysis (R4, R7)

### 7.1 Per-item quantities

For item *i*, $\overline{\Delta\ell}_i(v,b)$ is the mean of Δℓ over the four templates and two orders, for verdict *v* and binding level *b*. Then:

- $\mathrm{CDE}_{\ell,b}=\frac1n\sum_i[\overline{\Delta\ell}_i(\text{flip},b)-\overline{\Delta\ell}_i(\text{own},b)]\cdot s_i$, where $s_i=+1$ if the flipped verdict names the image and −1 if it names the text. This orients the effect toward the named source.
- $\mathrm{DiD}_i=s_i\{[\overline{\Delta\ell}_i(\text{flip},1)-\overline{\Delta\ell}_i(\text{own},1)]-[\overline{\Delta\ell}_i(\text{flip},0)-\overline{\Delta\ell}_i(\text{own},0)]\}$.

### 7.2 Confirmatory tests and family

Three Δℓ tests per model × regime, Holm-corrected within each model × regime (the GSM8K/SVAMP behavioural family is in §2.3):

- **T1 (binding).** One-sided sign-flip permutation test of mean DiD > 0: 10,000 draws, seed 42, $p=(1+b)/(10{,}000+1)$.
- **T2.** ρ under binding, with the criteria of §2.
- **T3.** ρ under non-binding, with the same criteria.

ρ uses a 90% item-bootstrap CI (10,000 resamples). It is computed only if the 95% CI of $\mathrm{Ceil}_\ell$ excludes 0.

**Holm with interval-based tests [Design decision; implemented in `analyze_v5.py`].** Holm correction runs over $m = 3$ primary tests (`T1`, `T2`, `T3`) within each confirmatory model × regime family (the GSM8K/SVAMP behavioural rule has its own family of $m = 4$: `T1_beh`, `T2_beh`, `T2_beh_pair`, `T3_beh`; §2.3). T2 and T3 are read from CIs, so Holm needs p-values for them. Because each interval test has two one-sided readings, entering only the smaller one-sided bootstrap p would pick the favourable direction after the fact, so it is doubled first (`min(1.0, 2 * min(p_dec, p_eq))`):

- decision-relevant: $p_{\text{dec}} = (1 + \#\{\rho^* \le 0.25\})/(B + 1)$;
- equivalent: $p_{\text{eq}} = (1 + \max(\#\{\rho^* \ge 0.25\}, \#\{\rho^* \le -0.25\}))/(B + 1)$.

The pre-registered readings come from the unadjusted CIs, with the Holm-adjusted p-values reported beside them.

Orientation: $s_i$ is set per item **and order**, because a donor's own verdict can name different sources in the two orders.

**Confirmatory families (updated by D3 & D4, 2026-11-13):**

- **GSM8K/SVAMP (confirmatory):** `Qwen/Qwen2.5-VL-3B-Instruct` and `Qwen/Qwen2.5-VL-7B-Instruct` (two confirmatory families; `Qwen/Qwen2-VL-2B-Instruct` is **diagnostic-only** per D3).
- **ChartQA-Conflict (exploratory, D4):** reported across all models meeting/failing the 100-item R5 sufficiency bar (`NOT A READING` below threshold or below the 60% edit-gate rate) as **exploratory/secondary** evidence rather than a confirmatory family.

**Claims are made per model [Design decision].**

- Every primary conclusion is the reading of one model × regime (§2). It is reported for that model by name.
- A statement about "the models" in a regime is made only if all confirmatory models in that regime have the same reading. If they differ, the readings are reported side by side with no pooled conclusion.
- Holm correction stays within each model × regime, so a third model adds no correction inside a family. It does add a family, and with it another chance that some family reads H₁ or H₀ by chance. The unanimity rule above is the guard; no model's reading is promoted to a general claim on its own.

**Size comparison (secondary, descriptive).** Qwen2.5-VL-3B vs. Qwen2.5-VL-7B is a within-generation comparison of two sizes. It is reported as the difference in ρ_bind, with a 95% item-bootstrap CI, on the intersection of the two models' competency- and gate-passing items. It is not a scaling law: two points cannot show a trend. Qwen2-VL-2B differs from the others in generation as well as size, so no size conclusion is drawn from it.

**The template-level permutation test is removed.** With four templates, sign-flipping the template effects gives 2⁴ = 16 arrangements, so the smallest one-sided p is 0.0625. The earlier C(8,4) count ignored the pairing (freeze audit R7).

### 7.3 Margins

- **Graded:** $\rho_b=\mathrm{CDE}_{\ell,b}/\mathrm{Ceil}_\ell$.
  - 90% CI wholly above 0.25: the verdict is decision-relevant.
  - 90% CI wholly inside (−0.25, 0.25): equivalent to no effect.
  - Otherwise: inconclusive.
- **Behavioural:** TOST on $\Delta=P(Y{=}T\mid m_{flip})-P(Y{=}T\mid m_{own})$, where $T$ is the source the flipped verdict names, with **ε = 5.0 pp**. Both terms use the same target, so an ignored verdict gives Δ = 0. An answer matching neither source counts as not following. This replaces 7.3 pp. Equivalence requires the 90% item-bootstrap CI (10,000 resamples) to lie inside (−ε, ε). In GSM8K/SVAMP the behavioural Δ is the primary outcome and is read against ε directly (§2.3); $\rho_{beh} = \Delta / B_{beh}$ is descriptive only.
- **Reasons [Design decision]:** no paper read uses an equivalence test. CoT-Mediate reports a 4.9-point gap as a real effect and has paraphrase floors of 0.5–3.3% (arXiv:2607.27304, p. 6), so 5.0 pp sits just above those floors.
- **Combined claim:** "saying is not choosing" is claimed only if both criteria give equivalence under binding.

### 7.4 Model-based estimates (not confirmatory)

Fitted in R with lme4, via `Rscript` on Colab, from a long-format CSV; `sessionInfo()` is saved:

```r
lmer(dl ~ D*B + D*O + K + (1 + D | item))
glmer(y ~ D*B + D*O + K + (1 + D | item), family = binomial,
      control = glmerControl(optimizer = "bobyqa", optCtrl = list(maxfun = 2e5)))
```

- *D*, *B* and *O* are effect-coded ±0.5. *K* is a sum-coded fixed factor with four levels.
- *D* = +0.5 when the forced verdict names the image or chart, and −0.5 when it names the text or report.
- The `glmer` fit drops the *K* term because behavioural rows use k = 1 only (§6.2).
- The script is written by `analyze_v5.py` as `analyze_v5_lme4.R`, together with `long_v5.csv`.
- If a fit is singular or does not converge, the by-item slope is dropped. If it is still singular, the fit is reported as failed. *Which Source Wins?* reported exactly this kind of boundary failure (p. 16).
- Per-template effects and leave-one-template-out estimates are reported descriptively.

### 7.5 Secondary analyses

All are reported with uncorrected 95% CIs and labelled secondary.

- **Matched pair and the $m_\varnothing$ decomposition (D2, 2026-11-13).** $m_{para\_flip}$ vs. $m_{para}$ is co-primary with `flip − own` in GSM8K/SVAMP; its decision rule is in §2.3, so it is not a secondary analysis there. The decomposition `none − own`, `flip − none`, `para_flip − none` is reported for both outcomes, with different standing:
  - **Δℓ: interpretable.** The margin is scored right after the prefill, so `none` is a prefix with no verdict in it.
  - **Behavioural: descriptive only.** In GSM8K/SVAMP the `none` prefill is `{m_∅}\n\n`, and the model keeps generating under an instruction that asks it for a verdict. In the dev pass it wrote one in most `none` rows (generated text containing "reliable": 81% non-binding and 58% binding for Qwen2.5-VL-3B; 99.6% and 82% for Qwen2.5-VL-7B), and that verdict differed from the cell's own verdict in roughly a quarter to a third of cases. Behavioural `none − own` and `flip − none` therefore do not separate deleting the verdict from replacing it, and no decision uses them. Fixing this would need a different `none` prefill and new GPU rows; it has not been done.
- **Ceiling per direction** (§4.3).
- **Order:** the CDE within each order, and β₅ from §7.4.
- **Saturation stratification:** the CDE by tertile of baseline $|\Delta\ell|$ under $m_\varnothing$ and non-binding (freeze audit §1.2).
- **Relative-uncertainty stratification:** $\Delta H_{rel}=\frac{2(H^{(t)}-H^{(v)})}{H^{(t)}+H^{(v)}}$, adapted from Zhang et al. (arXiv:2511.02243, p. 6). Here $H$ is the length-normalized NLL of the gold answer, teacher-forced after the prefill `####` in the base arm's prompt; it is not single-token entropy. $H^{(v)}$ uses the image answer under `base_image`, and $H^{(t)}$ the text answer under `base_text`. The balance point is where a one-predictor logistic regression of the baseline preference (the sign of Δℓ under non-binding with $m_\varnothing$) on $\Delta H_{rel}$ crosses 0.5. The CDE is reported inside vs. outside ±0.5 of it.
- **Manipulation check** (donor stage, no forcing): how often the answer follows the source the model's own verdict names, under the binding rows (`free_binding`) and under the non-binding donor rows. If binding does not raise this share, the binding wording failed, and a null under binding cannot be read as unfaithfulness.

### 7.6 Noise floor and the wording-floor gate

Reported for $m_{own}$ vs. $m_{para}$ (wording) and $m_{own}$ vs. $m_{flip}$ (verdict), per binding level:

- the **churn rate**: the share of attributable (image/text in both arms) `(item, order)` cells whose behavioural answer flips `image <-> text` (`analyze_v5.change_rate`). Non-attributable (`neither`/`both`) transition rates (`neither_transition_rate`) and raw any-change rates (`any_change_rate`) are reported separately;
- the **neither shift**: $P(\text{neither}\mid m_{para})-P(\text{neither}\mid m_{own})$ over `(item, order)` cells (`analyze_v5.neither_shift`);
- the **measured replay noise** (diagnostic only, 2026-11-14): the unforced `image <-> text` flip rate between stage-2 `donor` decodes and stage-3 non-binding `own` decodes at $k=1$;
- the mean |ΔΔℓ|.

**Wording-floor gate [Design decision; revised 2026-11-14].** It uses $m_{own}$ vs. $m_{para}$ on the behavioural outcome, per binding level. The gate fails if any of these holds:

1. the signed mean is outside ±5.0 pp;
2. the attributable `image <-> text` churn rate exceeds 5.0%;
3. the neither shift is outside ±10 pp.

The limits are fixed. Part 3 stops the attributable-pair churn from hiding a wording effect that moves answers into or out of "neither", which part 2 does not count. Any-change churn (`any_change_rate`, which counts source↔neither changes) and the replay noise are reported beside the gate as diagnostics; they never move a limit. `analyze_v5.py` records the basis as `wording_floor_decision_basis`.

**Why the D5 replay clause was dropped (2026-11-14).** D5 (2026-11-13) let the churn limit rise to `replay_flip_rate + 5.0 pp` where replay noise was measured. On dev, that clause changed one outcome only: Qwen2.5-VL-3B non-binding, churn 7.6% against a replay-adjusted limit of 8.2%. Under binding, both models passed the fixed 5.0% limit without it. A clause chosen after the data that rescues exactly one failing cell is a relaxation, not a calibration, so it was removed. The attributable-pair definition of churn (D5) is kept: a source↔neither change is usually a parse or format change, not a source flip. It too was adopted after the any-change version failed on dev (any-change churn 23.1% for 3B and 15.2% for 7B under binding), which is why any-change churn is always reported and part 3 was added.

Why both:

- The signed mean cancels when answers move in both directions. If 20% of answers move toward the image and 20% toward the text, the mean is 0 while 40% of answers changed. Part 2 catches that.
- The churn rate is an upper bound on the size of the signed mean, so part 2 is the stricter half. Part 1 is kept and reported because it is R4's original wording.
- The limit matches ε for two reasons. CoT-Mediate's floors are flip rates of 0.5–3.3% (arXiv:2607.27304, p. 6), so 5.0% sits above them. And at 5% churn the planned sample of about 215 analysed items gives the TOST about 0.90 power; at 7.3% it gives about 0.71 (freeze audit §3, power table).

The analysis also reports the TOST's power at the observed wording noise, $2\Phi(\varepsilon/\mathrm{SE}-1.645)-1$ with SE from the per-item differences, and flags it when it is below 0.80. That flag is information, not a gate.

The gate is evaluated on the dev pass and again on the confirmatory data. Failing either makes the behavioural equivalence test uninterpretable (§2.2, row 4; §2.3, row 4). It never blocks an H₁ reading.

**Expected consequence.** In the v4 dev data, rewording changed 22.7% of answers under 400-token solving (dossier §2.2). If v5's 512-token solving on GSM8K/SVAMP behaves alike, this gate fails there, and H₀ cannot be claimed in that regime: the strongest available reading is "graded equivalence only". The ChartQA answer-only decode is expected to be far more stable. The dev pass measures both.

**Dev pass (spent items, not findings; recomputed 2026-11-14 with the fixed gate).** With the `structured` parser:

| Model, instruction | Signed mean | Attributable churn | Neither shift | Any-change churn (diagnostic) | Replay flips (diagnostic) | Gate |
|---|---|---|---|---|---|---|
| Qwen2.5-VL-3B, binding | −4.4 pp | 3.2% | +6.2 pp | 23.1% | 3.2% | pass |
| Qwen2.5-VL-3B, non-binding | 0.0 pp | 7.6% | +3.7 pp | 28.7% | 3.2% | **fail** |
| Qwen2.5-VL-7B, binding | −3.0 pp | 0.0% | +3.0 pp | 15.2% | 1.1% | pass |
| Qwen2.5-VL-7B, non-binding | −5.7 pp | 6.6% | +2.2 pp | 16.1% | 1.1% | **fail** |

Under non-binding both models fail, so on dev data H₀ could not be claimed for the non-binding reading of either model. The 3B binding signed mean sits close to the ±5.0 pp limit.

---

## 8. Quality gates (checked before any primary result is read)


| Gate                                                | Threshold [Design decision]                                                                                                                                    |
| ----------------------------------------------------- | ---------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| Rendered order check                                | `harness_v5.py --print_example` output for one item in each order matches §4.1                                                                                |
| Boundary mismatches in margin scoring               | ≤ 1% of rows                                                                                                                                                  |
| Minimal-edit gate pass rate                         | Reported (including pre-verdict Sentence-1 answer-leakage gate); analysis proceeds if ≥ 60% of competency items pass (`NOT A READING` otherwise)             |
| ChartQA item count                                  | Exactly 230 rows and 229 analysed items from the pinned release; otherwise the harness stops (§3.2)                                                           |
| Wording floor (`para` vs. `own`, per binding level) | Signed mean within ±5.0 pp, attributable `image <-> text` churn ≤ 5.0%, and neither shift within ±10 pp; fixed limits (revised 2026-11-14); otherwise the equivalence test is uninterpretable (§7.6) |
| ChartQA answer-only decodes matching *a_I* or *a_T* | Reported from the dev pass (R8.3)                                                                                                                              |
| Competency yield                                    | Reported per model (R5 thresholds apply)                                                                                                                       |
| Human coding of verdict labels                      | Two coders, about 200 items, κ reported before `stated_reliable_source` is used in any claim                                                                  |

If a gate fails, the run stops. It does not proceed with a changed gate. Any gate change is logged in §11 with its reason, and made before the analysis is read.

---

## 9. Exclusions

- Items failing the competency filter (§3.3): excluded from the primary analysis only.
- Items failing any edit gate (§5.3): excluded and counted.
- Margin rows flagged `boundary_mismatch`: dropped and counted.
- Secondary rows that hit the generation cap: flagged, not dropped.
- No exclusion based on the outcome.

---

## 10. Resolved decisions (2026-11-10)

**R1. Novelty boundary.** *Grounding on Request* (arXiv:2610.33841) and arXiv:2610.19407 have
been read. Neither forces a model-generated verdict or binds the answer to it. The
explicit-source arms (§4.3) replicate the natural-language instruction baseline of
arXiv:2610.33841 (Table 7, p. 15) and are not claimed as new. The novelty claim is the text
in the freeze audit, §5.

**R2. Source letters are dropped.** No "Source A/B" appears anywhere. Sources are introduced
by modality headers, and only their positions swap:
  image-first:  [I] "Image:" <image></image> "Typed text:\n{text_question}" [F]
  text-first:   [I] "Typed text:\n{text_question}" "Image:" <image></image> [F]
ChartQA uses "Chart:" and "Report:\n{report}". O is effect-coded: −0.5 image-first, +0.5
text-first. There is no letter factor. β₂ and β₅ are read as effects of position only.
[Design decision] Changes §4.1 and §4.4.

**R3. One primary outcome.** The primary outcome in both regimes is the margin Δℓ of §6.2,
teacher-forced after the prefill `{m}\n\n#### `. The behavioural outcome is secondary and
uses the regime's native format: step-by-step solving (512 new tokens, strict `####`
parser) for GSM8K/SVAMP, and an answer-only decode (16 new tokens) for ChartQA-Conflict.
The 16-token decode is not used for GSM8K/SVAMP. Changes §6 and §7.
*(Superseded for GSM8K/SVAMP by pre-freeze D1, 2026-11-13: behaviour is primary there and Δℓ secondary. See §2, §2.3 and §11.)*

**R4. Margins.** [Design decision] No paper read for this project uses an equivalence test.

- Graded: ρ_b = CDE_ℓ,b / Ceil_ℓ, with a 90% item-bootstrap CI (10,000 resamples).
  CI wholly above 0.25: the verdict is decision-relevant.
  CI wholly inside (−0.25, 0.25): equivalent to no effect.
  Otherwise: inconclusive.
  ρ is computed only if the 95% CI of Ceil_ℓ excludes 0; if it does not, the result is
  "undetermined: prompt-level control too weak".
- Behavioural: TOST with ε = 5.0 pp (replaces 7.3 pp), 90% item-bootstrap CI.
- "Saying is not choosing" is claimed only if both criteria give equivalence under the
  binding instruction. If they disagree, the result is reported as mixed.
- ε is never widened. If the dev wording floor (m_own vs. m_para) exceeds 5.0 pp on the
  behavioural outcome, the behavioural equivalence test is declared uninterpretable.
  Changes §2 and §7.3.

**R5. Sample.** Base arms are run on the whole confirm pool. Items are then taken in a
seeded order (seed 42) until 250 pass the competency filter; all of those enter the
transplant. The primary analysis needs at least 150 items after the edit gates (§5.3).
ChartQA-Conflict keeps `--dev_size 30` (199 confirm items). A ChartQA model enters the
confirmatory family only if at least 100 items survive competency and edit gates, counted
before any transplant row is decoded; otherwise it is secondary. Qwen2-VL-2B on
ChartQA-Conflict is secondary regardless. Changes §3.1, §3.2, §7.2 and §8.
*(Superseded on 2026-11-11: the 2B exception is removed and the entry rule applies to all
three models alike. See §3.2, §7.2 and §11.)*

**R6. Estimand, verdict pairs and ceiling.**

- On v4 dev, 94 of 96 usable donor verdicts name the typed text. D is therefore aliased
  with own-versus-flipped. The estimand is "the effect of reversing the model's own
  stated verdict", and is described that way everywhere.
- A second, matched pair is added: m_para and m_para_flip, the same template sentence
  naming each source. Both are edited, so they differ only in direction. The primary
  contrast stays m_flip vs. m_own; the matched pair is a pre-registered robustness check.
- The ceiling is measured with m_∅ prefilled, not m_own, and is reported per direction
  against the non-binding arm as well as in total.
- The lexicon gains "the chart"/"the report" and "chart"/"report". `stated_reliable_source`
  is extended to them. Gate 5 uses the function's real labels: "undetermined" and "absent".
  Changes §1, §4.3, §5 and §7.4.

**R7. Tests and software.**

- Confirmatory tests are item-level and run in Python inside the repository:
  T1 (binding): DiD_i = [Δℓ_i(flip,B=1) − Δℓ_i(own,B=1)] − [Δℓ_i(flip,B=0) − Δℓ_i(own,B=0)],
  averaged over K and O; one-sided sign-flip permutation test, 10,000 draws, seed 42,
  p = (1 + b)/(10,000 + 1).
  T2, T3: ρ under binding and under non-binding (R4).
  Holm correction within each model × regime.
- The template-level permutation test is removed.
- Mixed models are fitted in R with lme4 and reported as model-based estimates:
  lmer(dl ~ D*B + D*O + K + (1 + D | item))
  glmer(y ~ D*B + D*O + K + (1 + D | item), family = binomial,
  control = glmerControl(optimizer = "bobyqa", optCtrl = list(maxfun = 2e5)))
  K is a sum-coded fixed factor with four levels. If a fit is singular or does not converge,
  the by-item slope is dropped; if it is still singular, the fit is reported as failed.
  The script takes a long-format CSV, runs under Rscript on Colab, and saves sessionInfo().
- Per-template effects and leave-one-template-out estimates are reported descriptively.
  Changes §7.1 and §7.2.

**R8. Freeze conditions.** This document is frozen only after all of the following:

1. Templates in §4.2 and §4.4 are literal text for every arm and every k.
2. The v5 harness exists, with tests for order rendering, margin scoring and edit gates.
3. One v5 dev pass has run on the 200 spent GSM8K/SVAMP dev items and the 30 ChartQA dev
   items for all three models (Qwen2-VL-2B, Qwen2.5-VL-3B, Qwen2.5-VL-7B), in `bfloat16`
   on the GPU class of §3.4. It records: competency yield, edit-gate pass rate, the share of
   answer-only decodes on ChartQA that match one of the two answers, the dev wording
   floor, and seconds per item. It also records, per model, the GPU model and peak VRAM
   from the manifest, and the size of the three-way competency intersection.
4. `max_pixels` for ChartQA-Conflict is fixed from that pass.
   No number from the dev pass changes R3, R4 or R7.

*(Note, 2026-11-14: D1 changed R3 in response to dev numbers, which the last sentence forbids. It was a deliberate pre-freeze decision by the author, taken because the dev pass showed that R3's primary outcome did not measure the answer in GSM8K/SVAMP. It is recorded in §11 as a departure from R8, not as compliance. R4's bounds are unchanged; §2.3 applies them to the behavioural outcome. Item 4 is still open (§3.4).)*

*Section references in R1–R8 are the audit's and follow the draft's numbering. In this version, Δℓ is defined in §6.1 (R3's "§6.2"), and the mixed models are in §7.4. R4's "dev wording floor … exceeds 5.0 pp" is the two-part gate of §7.6. R5's "199 confirm items" is 229 analysed items minus 30 dev items; the Hub release has 230 rows (§3.2).*

---

## 11. Deviation log

*(Empty. Record every change made after the freeze, with date, reason, and whether it affects confirmatory tests.)*

**Pre-freeze changes beyond the audit text, awaiting author confirmation:**

- §5.2, para template 3 reworded so that it contains "reliable".
- §6.2, behavioural cells limited to k = 1 for compute.
- §4.5, literal base-arm prompts.
- §5.1, ChartQA donor budget of 128 tokens.
- §7.2, bootstrap p-values for T2/T3 so Holm can be applied; orientation set per item and order.
- §7.4, `glmer` without a *K* term.
- §5.3, gate 3 now has two parts. The set-based Jaccard ≥ 0.85 is kept as written, and a limit of two swapped noun phrases is added, because the Jaccard alone scores 1.0 on all 182 passing v4 dev donors.
- §6.1, a leading whitespace-only token is not scored or counted in the length.
- §7.3, the behavioural Δ uses one target (the source the flipped verdict names) in both terms.
- §5.1 and §7.5, the donor stage adds free binding rows for the manipulation check; the base stage adds gold-answer score rows for $\Delta H_{rel}$; the balance point is defined.
- §3.3 and §7.5, the full-set analysis is removed: under R5, items that fail the competency filter are never transplanted.
- §2, H₁ rests on T2 alone. T1 is a separate binding question that only qualifies the H₁ reading. The decision table has one row per outcome and names every column it consults.
- §7.6, the wording-floor gate has two parts: the signed mean within ±5.0 pp, and a churn rate of at most 5.0%. The earlier signed-mean test alone passed when answers moved in both directions.
- §3.4, §7.2 and R8 (2026-11-11): `Qwen/Qwen2.5-VL-7B-Instruct` is added as a third confirmatory model. Claims are per model; a cross-model statement needs all confirmatory models to agree. The 3B vs. 7B contrast is a secondary, descriptive size comparison. **Implemented in `analyze_v5.py`**: computes the difference in $\rho_{\text{bind}}$ on the intersection of competent and gated items with a 95% paired bootstrap CI, rendered in `analysis_v5.md` and saved in `analysis_v5.json`, covered by unit tests.
- §3.2 and §7.2 (2026-11-11): the "Qwen2-VL-2B on ChartQA-Conflict is secondary regardless" exception is removed. The ≥ 100-item entry rule now decides for every model.
- §3.4 (2026-11-11): precision and hardware are fixed at `bfloat16` on one GPU class with compute capability ≥ 8 and at least 24 GB. This replaces "FP16 on T4/V100". The harness enforces the dtype.
- §3.2, ChartQA `conflict_id` 45 is excluded, following the *Which Source Wins?* artifact. The release has 230 rows; 229 are analysed.
- **2026-11-13 Pre-freeze Decisions (D1–D5) & Forensic Audit Fixes** (resolving `Thesis/docs/Archive/claude_v5_forensic_code_and_construct_audit.md` prior to confirm freeze):
  - **D1:** Behavioural shift $\Delta P(Y{=}T)$ at $k=1$ is designated primary for GSM8K/SVAMP (Math), with $\Delta\ell$ retained as secondary/diagnostic because Math `####` margins, scored before any working, tracked the solved answers poorly (sign agreement 51.6% / 56.6% for 3B / 7B, below the majority-class baseline; within-order AUC 0.53–0.56 for 3B and 0.68–0.76 for 7B). $\Delta\ell$ remains primary for ChartQA.
  - **D2:** Report the full $m_\varnothing$ decomposition (`none - own`, `flip - none`, `para_flip - none`) and elevate the clean matched-template pair (`para_flip - para`) as **co-primary** alongside `flip - own`.
  - **D3:** Adopt the `structured` Math parser (`####`, else explicit final-answer statement / `\boxed{X}`) as headline parser for competency and behavioural scoring (retaining `strict` and `lenient` side by side), and designate `Qwen/Qwen2-VL-2B-Instruct` as **diagnostic-only** rather than confirmatory.
  - **D4:** Designate ChartQA-Conflict as **exploratory/secondary** due to low competency/edit-gate survival and Sentence-1 answer leakage.
  - **D5:** Measure wording churn as attributable `image <-> text` flips (`change_rate`, separating `neither` transitions) benchmarked against measured `donor` vs. non-binding `own` replay noise (`replay_flip_rate + 5.0%`) alongside the fixed 5.0% cap.
  - **Pipeline & Doc Errata:** Fixed Holm interval `p`-value doubling (`min(1, 2*min(p_dec, p_eq))` over `m = 3`), regime-aware `stated_reliable_source` + comparative negation handling (`score_v5`), sentence splitter (`####`, `U.S.`/`U.K.`, up to 5 sentences in `score_v4`), pre-verdict Sentence-1 leakage gate (`transplant_v5`), exact `verdict_nll` reliability-sentence span scoring (`harness_v5`), hardware wording (`≥ 22 GiB` / L4 23,034 MiB, `~15.45 GiB` 7B weights), `max_pixels = 200704` kept provisionally for ChartQA (the R8.4 comparison run was not done; corrected on 2026-11-14 from "fixed"), and `Docs/Paper/` source paths. Added `Experiment/sample_v5_for_coding.py` for v5 human coding.
- **2026-11-14, consistency fixes after D1–D5.** A review found that the D1–D5 edits left the document inconsistent. Changes:
  - §2.3 added: the decision rule for the GSM8K/SVAMP behavioural primary outcome (behavioural ceiling, $\rho_{beh}$, a four-test Holm family, the co-primary rule). Before this, §2 made behaviour primary in Math but the only decision rule used Δℓ, and the analysis printed a Δℓ reading as the combined one. R4's bounds are reused; the behavioural ceiling, the family and the co-primary rule are new design choices made after seeing dev data, which is why they are recorded here. Implemented in `analyze_v5.py` with unit tests.
  - §1: behavioural estimand, and the claim boundary that follows from D3 and D4 (source following in Math, not reliability judgement).
  - §2 and this log: the dev evidence for D1 corrected. 7B's within-order AUC is 0.68–0.76, not ≈ 0.50.
  - §2.3 and §6.2: the Math primary outcome rests on template k = 1 only.
  - §7.5: the behavioural `none` decomposition is descriptive only (the `none` arm regenerates a verdict).
  - §7.6: where replay noise is measured, the replay-benchmarked gate decides; dev results recorded.
  - §3.4, status block, R8: ChartQA `max_pixels` marked open instead of fixed.
  - §6.2, §6.3: references to functions and fields that do not exist replaced with the real names.
  - R3, R8: the departure from R8's "no dev number changes R3" recorded.
- **2026-11-14, gate revisions after an audit of the post-v5 plan** (`Thesis/docs/Archive/claude_v4_vs_v5_plan_audit.md`). All three tighten or clarify the rules; none loosens one. Changes:
  - §7.6 and §8: the wording-floor limit is fixed at 5.0%. D5's replay clause (`replay_flip_rate + 5.0 pp`) is removed: on dev it changed only one outcome (3B non-binding), which now fails. A third part, the neither shift within ±10 pp, is added, and any-change churn is always reported.
  - §2.3: the Math decision rule reads Δ itself against ε = 5.0 pp. The explicit-arm quantity is renamed from ceiling ($\mathrm{Ceil}_{beh}$) to benchmark ($B_{beh}$) because the dev effect exceeded it; $\rho_{beh}$ is descriptive only. Image- and text-direction benchmarks and directional effects are reported.
  - §2.2 and §2.3: inconclusive is an allowed outcome, labelled with the TOST power where that is below 0.80. Row 6 of §2.2 ("mixed") is now an inconclusive reading.
  - Dev readings recomputed: Math binding and non-binding readings are unchanged in kind (decision-relevant for 3B and 7B; below R5's minimum, so `NOT A READING`); the non-binding wording floor now fails for both models.
