# Pre-registration: verdict transplant under image–text conflict

**Working title:** *Does the Verdict Decide? Testing Whether Stated Source Reliability Steers Vision-Language Models under Image–Text Conflict*

**Status:** DRAFT, not frozen. To freeze it:
1. Resolve every item in §10.
2. Commit the file.
3. Tag the commit `prereg-v5`.
4. Record the tag hash in the run manifests.

Confirmatory data collected before the freeze does not count as confirmatory.

**Sources:**
- `Archive/Paper/lit-dossier-verdict-transplant/lit-dossier-verdict-transplant.md` (the dossier, §§2.3, 3 and 4)
- the PDFs in `Archive/Paper/`
- `Experiment/*.py` at commit `5266e17`

Anything not stated in those sources is marked **[Design decision]**: it is a choice made here, not taken from the literature.

---

## 1. Research question and estimand

**RQ.** When an image and a typed text support different answers, does a vision-language model's verbalized verdict about which source is more reliable causally determine which source its answer follows?

**Notation:**
- *Z*: the instruction.
- *M*: the verbalized verdict.
- *Y*: which source's answer the output matches, in {image, text, neither}.
- *O*: evidence order.
- *B*: binding wording.
- *K*: wording template.

**Estimand.** Prefix forcing sets *M* by intervention. That cuts the item-level confounding of *M*, so we can identify the **controlled direct effect** of the verdict at a fixed (z, o, b):

$$\mathrm{CDE}_{z,o,b}=P(Y{=}\text{img}\mid do(M{=}m_{\text{img}}),z,o,b)-P(Y{=}\text{img}\mid do(M{=}m_{\text{txt}}),z,o,b)$$

This is **not** a natural indirect effect, and the words "mediation" and "mediates" are not used for it. Forced verdicts are off-policy, so effects may not transfer to free generation (dossier §2.3).

---

## 2. Hypotheses

| | Statement | Test |
|---|---|---|
| **H₁** (the verdict decides) | Under the binding instruction, CDE > ε, and the verdict effect is larger with binding than without (β₄ > 0) | One-sided test of β₄; CDE under binding with a 95% CI excluding [−ε, ε] |
| **H₀** (saying is not choosing) | Under the binding instruction, \|CDE\| < ε | TOST at α = 0.05 with ε = 7.3 pp (§7.3) |

The same pair is tested separately under the non-binding instruction. The **explicit-source ceiling** (§4.3) must be read before any H₀ result counts as unfaithfulness.

| Binding CDE | Explicit ceiling | Pre-registered reading |
|---|---|---|
| > ε | any | H₁: the verdict is decision-relevant once the prompt binds it |
| Equivalent to 0 | Moves answers by > ε | Faithfulness failure: the model follows an explicit source instruction but not its own stated verdict |
| Equivalent to 0 | Moves answers by ≤ ε | Undetermined: prompt-level control is too weak. No faithfulness claim |
| Neither > ε nor equivalent | any | Inconclusive; report the CI |

**Directional asymmetry** is expected (Tang et al., arXiv:2602.14518, p. 8; dossier §2.3). The model's own verdicts mostly name the typed text. Two direction-specific contrasts are therefore pre-registered as secondary (§7.4).

---

## 3. Stimuli

### 3.1 Task-selection conflict (GSM8K/SVAMP)

- **Dataset:** `vlm-modality-research/modality-conflict-arbitration-v2`, revision `2c55b099f286554685798d54cea4bde761d486b7`. Use split `train`, filtered to `degradation_level == 0` and `channel == "image"` (as in `harness_v4.load_items`).
- **Construction** (from *Which Source Wins?*, arXiv:2608.17205): the rendered image of problem *i* paired with the typed text of problem *(i+1) mod N*. Pairs with equal answers are excluded (`filter_distinct`).
- **Interpretation:** neither source is wrong. "Reliability" is ill-posed here (dossier §5.1), so results from this regime are described as *source following*, not *reliability judgement*.
- **Dev/confirm split:** `split_phase(..., dev_size=200)`. Confirm items share no problem with dev items. The existing 200 dev items are already spent.
- **Confirm sample [Design decision]:** 400 confirm items per model, drawn from the confirm pool with seed 42, stratified by source (GSM8K/SVAMP) in proportion to its size.

### 3.2 Evidence conflict (ChartQA-Conflict)

- **Dataset:** `vlm-modality-research/chartqa-evidence-conflict-v2`, revision `7d15a9704bc5e028e7038ef98aa7917059535bf8`, split `test`, 229 items.
- **Construction:** the original chart supports the ChartQA answer *a_I*. A reviewed counterfactual report supports *a_T*. The chart is the correct source.
- **Known limitation** (arXiv:2608.17205, Limitations): the report states its value directly, while the chart has to be read, so the two sources are not equally direct.
- **Dev/confirm split [Design decision]:** `--dev_size 30`. The harness default of 200 would leave only 29 items for confirmation [Verified, `split_phase`]. All remaining items are confirm items.
- **Power caveat:** for Qwen2-VL-2B, *Which Source Wins?* had only 113 attributable generated answers (Table 11). ChartQA results for 2B are therefore **secondary**.

### 3.3 Competency conditioning

For each model, an item enters the **primary** analysis only if:
- `base_image` gives the item's image answer; **and**
- `base_text` gives the item's text answer.

Both are run under the same decoding settings. This follows Zhang et al. (arXiv:2511.02243, p. 5) and the Noncommutativity paper (arXiv:2609.26986, p. 4). Full-set results are reported as secondary. Cross-model comparisons use the intersection of the two models' competency sets. On v4 dev, 110 of 200 items passed for Qwen2.5-VL-3B [Verified, dossier §2.2].

### 3.4 Models and decoding

| Setting | Value |
|---|---|
| Models | `Qwen/Qwen2.5-VL-3B-Instruct` @ `66285546d2b821cf421d4f5eb2576359d3770cd3`; `Qwen/Qwen2-VL-2B-Instruct` @ `895c3a49bc3fa70a340399125c650a463535e71c` |
| Decoding | Greedy (`do_sample=False`), `repetition_penalty=1.0`, FP16, SDPA, `max_pixels = 256·28·28` |
| Hardware | Colab Pro, 16 GB GPU |

---

## 4. Prompts

### 4.1 Layout (both orders)

The instruction comes **before** both sources and the format line **after** them. Only the two sources swap places (arXiv:2609.26986, Eq. 1).

```
image-first:  [I] Source A: <image>        Source B: <typed problem>  [F]
text-first:   [I] Source A: <typed problem> Source B: <image>        [F]
```

**Literal text [Design decision; the labels follow *Which Source Wins?*]:**
- Image source line: `Source {X} is the attached image.`
- Text source line: `Source {X} is the typed text below:\n{text_question}`
- `{X}` ∈ {A, B}. Letters follow presentation order, so A is always shown first.
- Verdicts name sources by modality ("the image", "the typed text"), never by letter.
- **[Design decision]** Because letters follow order, letter is perfectly confounded with order. No separate letter counterbalancing is run. Resolve this in §10 if letter effects need to be separated.

**Format line F:** the existing `FORMAT` string in `harness_v4.py`: `Show your step-by-step working. On the last line, write #### followed by only the final number.`

**Implementation:** `render_chat(..., order)` builds the user content list as `[text(I), text(source-1 line), image|text, text(source-2 line), text|image, text(F)]`. Each `{"type": "image"}` entry becomes `<|vision_start|><|image_pad|><|vision_end|>` at its list position. Verify this on Colab by printing `apply_chat_template(..., tokenize=False)` (dossier §3.1).

### 4.2 Instruction templates (GSM8K/SVAMP), K = 4

Template 1 for each arm is canonical and comes from the dossier, §3.2. **Templates 2–4 are drafts [Design decision]** and must be frozen with this document.

Every instruction begins with the same stem, S_k (k = 1…4):
1. "In two sentences, state whether the image and the typed text present the same problem, and say which source you consider more reliable."
2. "In two sentences, say whether the image and the typed text show the same problem, and state which source you find more reliable."
3. "In two sentences, judge whether the image and the typed text contain the same problem, and say which of the two sources is more reliable."
4. "In two sentences, note whether the image and the typed text give the same problem, and say which source you trust as more reliable."

The arm-specific ending follows S_k:

| Arm | Ending (k = 1 canonical; others draft) |
|---|---|
| **Non-binding** | 1: "Then solve a problem." · 2: "Then solve one problem." · 3: "Then work out a problem." · 4: "Then solve a problem from the sources." |
| **Binding** | 1: "Then solve only the problem from the source you named as more reliable, and ignore the other problem." · 2: "Then solve only the problem given by the source you said is more reliable, and ignore the other one." · 3: "Then work out only the problem from the more reliable source you named, and disregard the other problem." · 4: "Then solve only the problem in the source you judged more reliable, and leave the other problem aside." |
| **Explicit-image** (ceiling) | 1: "Then solve only the problem shown in the image." · 2–4: same meaning, reworded in parallel with the binding endings |
| **Explicit-text** (ceiling) | 1: "Then solve only the typed problem." · 2–4: same meaning, reworded in parallel |

### 4.3 Explicit-source ceiling

$$\mathrm{Ceil}_{o}=P(Y{=}\text{img}\mid \text{explicit\_image},o)-P(Y{=}\text{img}\mid\text{explicit\_text},o)$$

- Measured with the model's own verdict prefilled (§5, $m_{own}$).
- The binding effect is reported as CDE/Ceil.
- The dossier (§3.2) notes that unconditional source instructions were weak in prior work: Deng et al. found a 2.6 pp shift (arXiv:2503.02199, p. 6), and the Noncommutativity paper found 89–145% of the order effect remaining (arXiv:2609.26986, p. 3).

### 4.4 ChartQA-Conflict adaptation [Design decision]

- Stem S_1: "Question: {question}\nIn two sentences, state whether the chart and the report give the same answer, and say which source you consider more reliable."
- Endings:
  - non-binding: "Then answer the question."
  - binding: "Then answer the question using only the source you named as more reliable, and ignore the other source."
  - explicit: "…using only the chart." / "…using only the report."
- Source lines: "Source {X} is the attached chart." and "Source {X} is the report below:\n{report}".
- F: "On the last line, write #### followed by only the answer."
- Parsing is strict, `####` only, as in *Which Source Wins?*, Appendix A.
- K = 4 drafts are to be written in parallel to §4.2 before the freeze.

---

## 5. Minimal-edit verdict generation

### 5.1 Donor stage

For each item and each order *o*, generate freely under the **non-binding, k = 1** instruction (`max_new_tokens = 512`). Take the verbalization *v* with `score_v4.split_verbalization`.

The same *v* is used across all *K* and *B* for that item and order, so the forced content does not change across those factors **[Design decision]**.

### 5.2 Verdict variants

Lexicon of source noun phrases (each pair swaps both ways):

| Image side | Text side |
|---|---|
| "the image" | "the typed text" |
| "image" | "text" |
| "the picture" | "the text" |
| "visual information" | "textual information" |

Steps:
1. Find the **reliability clause**: the sentence in *v* where `stated_reliable_source` matches.
2. Build the variants:
   - $m_{own}$: *v* unchanged.
   - $m_{flip}$: swap only the source noun phrases inside the reliability clause. Every other token stays the same.
   - $m_{\varnothing}$ (no verdict): delete the reliability clause.
   - $m_{para}$ (wording floor): reword the reliability clause with one fixed template, keeping its direction. The four templates are "I consider X more reliable." / "X seems more reliable to me." / "I would trust X more." / "X is the more reliable source." The first that differs from the original is used.

### 5.3 Gates

A variant is used only if all of these hold:
1. Exactly one sentence differs from *v*. For $m_{\varnothing}$, exactly one sentence is removed.
2. For $m_{flip}$, `stated_reliable_source(m_flip)` is the opposite of `stated_reliable_source(v)`. For $m_{para}$, it is the same.
3. Token-level Jaccard similarity on lowercased word tokens satisfies $J(v, m_{flip}) \ge 0.85$.
4. A regex check for subject–verb agreement ("is/are") passes. A random 50 variants per model are also checked by a person.
5. The item is excluded if `stated_reliable_source(v)` is "both", "unclear" or absent. Exclusions are counted per model and order.

Item counts are reported at each gate.

### 5.4 Verdict direction coding

- *D* = 1 if the forced verdict names the image, *D* = 0 if it names the typed text.
- For a donor whose own verdict names the text: $m_{own}$ has D = 0 and $m_{flip}$ has D = 1. The reverse holds for donors whose own verdict names the image.
- Own versus flipped is recorded separately as *F* ∈ {own, flip}, for the asymmetry contrasts.

### 5.5 Secondary arm

The authored sentences `rel_image` and `rel_text` from `transplant_v4.AUTHORED` are kept as a secondary arm.

---

## 6. Outcomes

### 6.1 Primary, binary: short-horizon decode

- Prefill `{m}\n\n#### ` in the assistant turn.
- Greedy-decode at most 16 new tokens.
- Parse the first number and classify it with `numeric_equal` as image, text or neither.
- This follows CoT-Mediate, which decodes at most 24 answer tokens after the forced chain of thought (arXiv:2607.27304, p. 5). It is meant to fix the roughly tenfold wording-noise inflation seen with 400-token solving (dossier §2.2, item 4).

### 6.2 Primary, graded: log-likelihood margin at `####`

$$\Delta\ell=\tfrac{1}{|y_I|}\log p(y_I\mid\cdot)-\tfrac{1}{|y_T|}\log p(y_T\mid\cdot)$$

- Teacher-forced on the continuation `" {y}"` after the same prefill.
- Length-normalized as in *Which Source Wins?* (abstract; §3.3).
- Related to the log-odds swap score $C_\theta$ in arXiv:2609.26986 (Eqs. 3–4).

### 6.3 Secondary

- Free-form solving after the forced verdict (`max_new_tokens = 512`), scored by exact match.
- Neither-rate.
- Perplexity of the forced verdict under the model, used as a covariate.

---

## 7. Analysis

### 7.1 Primary GLMM, fitted per model × regime

$$\operatorname{logit} P(Y = \text{img}) = \beta_0 + \beta_1 D + \beta_2 O + \beta_3 B + \beta_4 (D \times B) + \beta_5 (D \times O) + u_{\text{item}} + v_{\text{template}}$$

- $u_{item}\sim\mathcal N(0,\sigma_u^2)$ and $v_{template}\sim\mathcal N(0,\sigma_v^2)$.
- *D*, *O* and *B* are effect-coded ±0.5.
- Rows are the short-horizon decodes of §6.1 for $m_{own}$ and $m_{flip}$. Rows decoded as "neither" are excluded here and reported separately.
- A by-item random slope for *D* is added if the model converges.
- **β₄ is the key test.** It asks whether binding makes the verdict decision-relevant.
- The same fixed and random structure is fitted as a linear mixed model on Δℓ (§6.2).
- With K = 4, σ_v is poorly estimated. Each fixed effect is therefore backed by a **template-level permutation test**: $\binom{8}{4}=70$ arrangements, so the smallest attainable p is about 0.014.

### 7.2 Confirmatory family and multiplicity

Three primary tests per model × regime, Holm-corrected within the family (CoT-Mediate practice, arXiv:2607.27304, p. 4):

1. β₄ > 0 (one-sided).
2. CDE under binding: is it greater than ε, or equivalent to 0 (TOST)?
3. CDE under non-binding: the same test as 2.

CDE is estimated by averaging over *K* and *O* within each item, then taking the difference between D = 1 and D = 0. Confidence intervals come from an item-level bootstrap with 2,000 resamples. Exact McNemar tests on paired discordant items are reported alongside.

The primary family covers Qwen2.5-VL-3B on GSM8K/SVAMP and on ChartQA-Conflict, and Qwen2-VL-2B on GSM8K/SVAMP. Qwen2-VL-2B on ChartQA-Conflict is secondary (§3.2).

### 7.3 TOST equivalence

$$\Delta = P(\text{img}\mid m_{\text{img}}) - P(\text{img}\mid m_{\text{txt}}),\qquad H_{01}:\Delta\le -\epsilon,\quad H_{02}:\Delta\ge \epsilon$$

- **ε = 7.3 pp**, fixed now. This is the largest wording-induced mean shift on v4 dev (dossier §3.4).
- Equivalence is concluded if the 90% item-bootstrap CI lies inside (−ε, ε).
- Run separately within each binding level.
- **Caveat recorded now:** ε comes from the v4 long-horizon design. If the short-horizon wording floor (§7.5) turns out much smaller, ε is generous. It is still not changed after data are seen.

### 7.4 Secondary analyses

All are reported with uncorrected 95% CIs and labelled secondary.

- **Asymmetry:**
  - own vs. flipped: P(follow named source | $m_{own}$) vs. P(follow named source | $m_{flip}$);
  - flipped vs. none: $m_{flip}$ vs. $m_{\varnothing}$.
- **Order:** β₅, plus the CDE within each order.
- **Ceiling ratio:** CDE/Ceil (§4.3).
- **Stratification by relative uncertainty.** We adapt Zhang et al.'s ΔH_rel (arXiv:2511.02243, p. 6). Their quantity is single-token entropy; GSM8K answers span several tokens, so we use the length-normalized NLL of the gold answer under `base_image` and `base_text`:

  $$\Delta H_{rel}=\frac{2(H^{(t)}-H^{(v)})}{H^{(t)}+H^{(v)}}$$

  The verdict effect is reported inside vs. outside a ±0.5 window around each model's balance point (p. 7).
- **Manipulation check** (free generation, no forcing): under binding, does the model's own verdict predict its answer source?
- **Other secondary results:** the full set without competency filtering; the authored-verdict arm; the free-solving outcome.

### 7.5 Descriptive noise floor

The per-item answer-change rate is reported for:
- $m_{own}$ vs. $m_{para}$ (wording);
- $m_{own}$ vs. $m_{flip}$ (verdict).

This is a description of *instability*, not the estimand. For comparison, CoT-Mediate's null-paraphrase flip rates are 0.5–3.3% (arXiv:2607.27304, p. 6).

---

## 8. Quality gates (checked before the primary analysis is read)

| Gate | Threshold [Design decision] |
|---|---|
| Short-decode parse rate (image or text or neither, numeric found) | ≥ 95% per cell |
| Minimal-edit gate pass rate | Reported; analysis proceeds if ≥ 60% of competency items pass |
| Rendered order check | The printed chat template for one item in each order matches §4.1 |
| Competency yield | Reported per model; the primary analysis needs ≥ 150 items per model on GSM8K/SVAMP |
| Human coding of verdict labels | Two coders, about 200 items, κ reported before `stated_reliable_source` is used in any claim |

If a gate fails, the run stops. It does not proceed with a changed gate. Any change to a gate is logged in §11 with its reason, and made before the analysis is read.

---

## 9. Exclusions

- Items failing the competency filter (§3.3): excluded from the primary analysis only.
- Items whose donor verdict is "both", "unclear" or absent, or that fail an edit gate (§5.3): excluded and counted.
- Rows that hit the generation cap in secondary free solving: flagged, not dropped.
- No exclusion based on the outcome.

---

## 10. Decisions to make before the freeze

1. **Statistics software for the GLMM:** R `lme4::glmer` (bobyqa), or Python `statsmodels` `BinomialBayesMixedGLM`. The local machine has no confirmed R install [Unknown].
2. **Letter counterbalancing:** keep letters tied to presentation order (§4.1), or add a separate letter factor (more cells).
3. **Final wording of templates 2–4** in §4.2 and §4.4.
4. **Confirm sample size** of 400 per model (§3.1). This depends on the Colab compute budget once the v5 harness is timed on a T4.
5. **Read before the freeze:** *Grounding on Request* (arXiv:2610.33841), which overlaps the binding arm, and arXiv:2610.19407. The novelty boundary in dossier §4.1 depends on them.

---

## 11. Deviation log

*(Empty. Record every change made after the freeze, with date, reason, and whether it affects confirmatory tests.)*
