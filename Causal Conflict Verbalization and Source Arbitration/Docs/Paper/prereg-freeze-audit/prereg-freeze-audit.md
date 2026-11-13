# Pre-registration freeze audit: verdict transplant (`prereg-v5`)

*Prepared 2026-11-10. Audits `Docs/PREREGISTRATION_VERDICT_TRANSPLANT.md` as it stands, uncommitted, in the main checkout.*

## Verdict: red light. Do not tag `prereg-v5` yet

The design is sound in outline, but the draft cannot be frozen today. Five of the problems below would change what the confirmatory tests mean, and three pieces of the document are not yet literal text. None needs new confirmatory data; all can be fixed with edits plus one dev pass on items that are already spent.

| # | Blocking problem | Fix (details in §3) |
|---|---|---|
| 1 | Two outcomes are both called "primary", and H₁ mixes scales: the CDE is in percentage points while β₄ is on the logit scale. An interaction can have opposite signs on the two scales | One primary outcome: the log-likelihood margin Δℓ (R3) |
| 2 | The new primary outcome has never been observed, even on dev. The v5 harness does not exist: `render_chat` has no order argument, and there is no margin scoring or minimal-edit generator | One v5 dev pass before the freeze (R8) |
| 3 | In dev, the model's own verdict names the text in 94 of 96 usable donors. Verdict direction is therefore the same variable as "own vs. flipped" | Restate the estimand; add a matched pair of template verdicts (R6) |
| 4 | The explicit-source ceiling is measured with the model's own verdict prefilled. For the explicit-image arm that verdict contradicts the instruction in about 98% of items | Measure the ceiling with the no-verdict prefill (R6) |
| 5 | ε = 7.3 pp is larger than effects the neighbouring literature reports as real | ε = 5.0 pp; Δℓ equivalence relative to the ceiling (R4) |
| 6 | The template-level permutation test is not defined for β₄, and a version that respects the pairing cannot reach p < 0.05 with four templates | Replace with an item-level test (R7) |
| 7 | Templates 2–4 of the explicit arms and all ChartQA templates are placeholders | Literal text supplied in §4 |
| 8 | On ChartQA the verdict parser cannot work: `stated_reliable_source` only looks for "image" and "text", and the lexicon in §5.2 has no chart/report pair | Extend parser and lexicon; test on the 30 dev items |

Letter counterbalancing, sample size and statistics software are settled in §3 and do not block.

**How far I read.** All four new papers were downloaded from arXiv and read from page-level text; page numbers are 1-based PDF pages.
- *Grounding on Request*: pp. 1–9 in full, plus the prompt table on pp. 15–16.
- *Biased Bayesian Observers*: pp. 1–9 in full, plus Appendix B on pp. 17–19.
- *Counterfactual Tests*: pp. 1–6 in full; results sections only through the abstract.
- *Which Source Wins?*: pp. 1–6 in full, plus pp. 7, 9 and 15–19.

**Corrections to the brief.**
- 2610.33841 is titled *Grounding on Request: Learning Modality Control in Vision-Language Models*. Its strong control comes from trained components, not prompting.
- Neither *Which Source Wins?* nor *Noncommutativity* separates source letters from presentation order (§3, R2). The A/B labels in *Noncommutativity* are answer-option letters, not source labels.
- None of the 14 papers read for this project uses an equivalence test or reports a mixed-model package. No ε and no "venue-standard" package can be taken from them; both are design decisions and are labelled as such.
- **A correction to my own dossier:** CMC-Bench exists. It is Catapang (2026), *When Image and Text Disagree: Cross-Modal Evidence Conflict in Multimodal Retrieval-Augmented Generation*, MAGMaR 2026 ([doi](https://doi.org/10.18653/v1/2026.magmar-main.3)). *Which Source Wins?* cites it as building "image-text conflicts using ChartQA and MMMU" to "evaluate accuracy and abstention" ([p. 3](https://www.alphaxiv.org/pdf/2608.17205?page=3)). I have not read it. The dossier also repeated the C(8,4) permutation scheme without checking it; see R7.

---

## 1. Paper autopsies

### 1.1 Grounding on Request (arXiv:2610.33841)

**What it asks.** "When an image and its caption disagree, can a user reliably control which one a vision-language model (VLM) follows?" ([p. 1](https://www.alphaxiv.org/pdf/2610.33841?page=1))

**Setup.**
- Models: Gemma-3-4B, Qwen3.5-4B, Qwen3.5-2B ([p. 5](https://www.alphaxiv.org/pdf/2610.33841?page=5)). Neither of the thesis models.
- Outcome: forced choice among fixed candidates by summed token log-likelihood, $m_s(y\mid C)=\sum_t \log p(y_t\mid C, r_s, y_{<t})$ (Eq. 1, [p. 4](https://www.alphaxiv.org/pdf/2610.33841?page=4)). No generation and no reasoning text.
- Metrics (Eq. 2, [p. 4](https://www.alphaxiv.org/pdf/2610.33841?page=4)): FLIP asks whether the answer follows an edit to the *requested* modality; STAY asks whether it holds when the *competing* modality is edited. Both are conjunctive with initial correctness.
- The natural-language baseline is one sentence placed at the end of the prompt: "According to the image (and only the image), what is the answer?" (Table 7, [p. 15](https://www.alphaxiv.org/pdf/2610.33841?page=15)). The text request swaps "image" for "caption".
- Order: "image/text order alternates across items while remaining fixed across the original example and its twins" ([p. 15](https://www.alphaxiv.org/pdf/2610.33841?page=15)). No source letters.

**Result.** Prompting alone gives weak control, and weaker for images than for text. Strong control needs trained embeddings or LoRA.

![Grounding on Request, Table 2](figures/grounding-on-request-table2-control.png "Grounding on Request, Table 2: accuracy (A), FLIP (F) and STAY (S), averaged over three models and four benchmarks. A plain instruction lifts image-request FLIP only from .208 to .367, against .784 for text requests; learned tokens and LoRA do much better. [p. 7](https://www.alphaxiv.org/pdf/2610.33841?page=7)")

> "Across all 12 model–benchmark settings, every image request loses at least a 10% of its initially correct answers under the requested-modality intervention, and in 9 settings at least 25% fail to follow the image edit" ([p. 6](https://www.alphaxiv.org/pdf/2610.33841?page=6))

**One finding that touches the thesis directly.** The paper reports control without verbalization: "the learned words can control behavior without the model being able to clearly explain or self-verbalize their meaning" ([p. 8](https://www.alphaxiv.org/pdf/2610.33841?page=8)). That is the mirror image of "saying is not choosing" and should be cited.

**What it means for the design.**
- The binding arm survives. This paper never uses a model-generated verdict, never forces a prefix, and never makes the instruction conditional on the model's own judgement. It edits the *evidence* with the request held fixed; the thesis edits the *self-stated verdict* with the evidence held fixed.
- The explicit-source ceiling is **not** new. It is this paper's "Instruction" baseline. Say so in the thesis.
- Expect an asymmetric ceiling: weak for "use the image", strong for "use the text". The ceiling must be reported per direction (R6).

### 1.2 Biased Bayesian Observers (arXiv:2610.19407)

**Model.** Preference is the log-odds between the two candidate answers:

$$s_J=\log\frac{P(a_T\mid t,v,q)}{P(a_V\mid t,v,q)}\quad\text{(Eq. 1, p. 3)}$$

Each candidate is scored "by its log-likelihood averaged over its tokens" ([p. 3](https://www.alphaxiv.org/pdf/2610.19407?page=3)). Under cross-modal conditional independence and modality-specific weights, the paper derives

$$s_J=\beta_T e_T+\beta_V e_V+\pi_0\quad\text{(Eq. 6, p. 5)}$$

where $e_T=s_T-\pi_0$ and $e_V=s_V-\pi_0$ are the unimodal Bayes factors and $\pi_0$ is the question-only prior ([pp. 4–5](https://www.alphaxiv.org/pdf/2610.19407?page=4)).

**Evidence.** Qwen2.5-VL-3B is one of the four models. The two-parameter rule reaches R² = 0.852 on held-out degradation combinations for it, against 0.609 for "follow the more confident modality" (Table 1, [p. 6](https://www.alphaxiv.org/pdf/2610.19407?page=6)). An interaction term adds at most 0.001 R² ([p. 7](https://www.alphaxiv.org/pdf/2610.19407?page=7)).

![Biased Bayesian Observers, Table 3](figures/bayesian-observers-table3-weights.png "Biased Bayesian Observers, Table 3: Qwen2.5-VL-3B weights text slightly more than vision (βT/βV 1.06–1.45), and on clean inputs text evidence is 1.4–2.7 times stronger than visual evidence. [p. 8](https://www.alphaxiv.org/pdf/2610.19407?page=8)")

**Validity of the likelihood outcome.** After free reasoning, the model's choice "agrees with sign(sJ) on 75.3–82.0% of retained pairs, rising to 81.8–93.9% in the highest |sJ| tertile" (Appendix B.5, [p. 19](https://www.alphaxiv.org/pdf/2610.19407?page=19)).

**Does it support the CDE estimand?** It supports the estimand and challenges the scale. *The following is my extension, not the paper's:* if a forced verdict shifts the log-odds by δ towards the image answer, the verdict's effect is constant on the log-odds scale but not on the probability scale. There, with $s_i$ the item's baseline log-odds for the text answer,

$$\mathrm{CDE}_i=\sigma(\delta-s_i)-\sigma(-s_i)$$

shrinks towards zero whenever the baseline $|s_i|$ is large. A null in percentage points can therefore be saturation, not irrelevance. This is the main reason R3 makes Δℓ the primary outcome and stratifies by baseline margin. The paper also notes that when "the text states the answer while the image must be interpreted", text evidence is 1.4–3.8 times stronger ([pp. 7–8](https://www.alphaxiv.org/pdf/2610.19407?page=7)). ChartQA-Conflict has exactly that structure.

The paper never touches verbalization or reasoning, so it does not overlap the contribution.

### 1.3 Counterfactual Tests for CoT faithfulness in VLMs (arXiv:2609.06704)

**What it does.** It edits the *image* (removing one object) and asks whether the explanation mentions the removed object. It does not edit the chain of thought. The paper itself places CoT-editing work in a separate paradigm, "CoT Interventions", which "assess whether the answer depends on the CoT" ([p. 2](https://www.alphaxiv.org/pdf/2609.06704?page=2)). The thesis belongs to that paradigm, not to this paper's.

**Formulas** ([pp. 5–6](https://www.alphaxiv.org/pdf/2609.06704?page=5)):
- Score shift: $\mathrm{TVD}(p_a,p_b)=\tfrac12\sum_k|p_{a,k}-p_{b,k}|$ over the answer options (Eq. 5).
- vCCT: the correlation between score shift and a binary "change mentioned" flag (Eq. 6).
- vCT: $1-\frac1N\sum_i\Delta_i(1-\mathrm{CM}_i)$, where $\Delta_i$ marks a flipped top answer (Eq. 8).

**Thresholds and statistics.** There is **no equivalence bound** anywhere in the paper. What it uses ([pp. 4, 6](https://www.alphaxiv.org/pdf/2609.06704?page=6)):
- Edit-quality gates: changed-pixel fraction ≤ 0.20 and mask consensus ≥ 0.5. These are gates on the stimulus, not margins on the effect.
- 95% percentile bootstrap CIs with B = 10,000.
- Permutation tests with $p=\frac{1+|\{i:|T_{null,i}|\ge|T_{obs}|\}|}{B+1}$ (Eq. 10), α = 0.05, and paired permutation for within-item comparisons.
- A human audit: 141 examples, 87.9% correct edits and 92.2% correct mention detection; three blinded annotators with κ = 0.651–0.795.

**What transfers.**
- "binary vCT scores are often nearly saturated" ([p. 1](https://www.alphaxiv.org/pdf/2609.06704?page=1)). A second, independent reason to prefer a graded outcome.
- A no-op control: images "pass through the same editing pipeline without object removal". The thesis analogue is the paraphrase verdict.
- The permutation p-value formula and B = 10,000.

### 1.4 Source labels and order in *Which Source Wins?* and *Noncommutativity*

- ***Which Source Wins?*** swaps labels between items, not within them: "For odd-indexed items, the Source A/B labels are swapped, so neither modality is always Source A" ([p. 3](https://www.alphaxiv.org/pdf/2608.17205?page=3)). For ChartQA-Conflict, the labels are "counterbalanced … with the A source shown first" ([p. 18](https://www.alphaxiv.org/pdf/2608.17205?page=18)). So A is always first: letter and position are the same variable there too. Its §4.4 compares two prompt framings, not letters against order.
- ***Noncommutativity*** uses no source letters. Sources are named by role ("the image attachment", "the image description"), and only their positions swap. The A/B it counterbalances are answer options ([p. 2](https://www.alphaxiv.org/pdf/2609.26986?page=2)).

One more fact from *Which Source Wins?* bears on the outcome choice. Its margin is scored "after the fixed #### delimiter … with no chain-of-thought, so the margin measures direct-answer preference, not reasoning-trace attribution" ([p. 5](https://www.alphaxiv.org/pdf/2608.17205?page=5)). Agreement with the generated answer is modest, and lowest for the 2B model:

![Which Source Wins, Table 5](figures/which-source-wins-table5-margin-agreement.png "Which Source Wins?, Table 5: how often the sign of the likelihood margin agrees with the generated answer on GSM8K/SVAMP. For Qwen2-VL-2B it is 72.6% in the image-degradation arm and 58.6% in the text-degradation arm. [p. 15](https://www.alphaxiv.org/pdf/2608.17205?page=15)")

The same paper adopted the margin as its primary measure and kept generated answers "as a behavioral cross-check" ([p. 5](https://www.alphaxiv.org/pdf/2608.17205?page=5)). Its own mixed model failed: "The random-item-intercept variance reached the boundary at zero … We therefore do not use the resulting mixed-model p-values" ([p. 16](https://www.alphaxiv.org/pdf/2608.17205?page=16)).

---

## 2. What the dev data add

Recomputed from `results_v4/dev2_*.jsonl` (Qwen2.5-VL-3B, 200 dev items, T4, batch 8).

| Quantity | Value |
|---|---|
| Competency-passing items | 110 of 200 |
| Their `conflict_full` verdicts | 94 name the text, 2 name the image, 14 have no parseable verdict |
| Donors with exactly one reliability sentence | 96 of 110 (87%) |
| Measured generation speed | 2.40 s per row at 188 new tokens (78 tokens/s) |

Two consequences:
- **Direction is aliased with editing.** With 94 of 96 verdicts naming the text, "verdict names the image" means "the verdict was flipped" in about 98% of rows. The asymmetry analysis in §7.4 of the draft cannot separate the two.
- **The edit gate is passable.** 87% is above the draft's 60% threshold. These donors were written under the v4 instruction, so the v5 rate still has to be measured.

---

## 3. Replacement text for §10

Paste the block below over §10. Each resolution names the sections it changes; those sections must be edited to match before the freeze. Everything marked **[Design decision]** is a choice made here, not a value from the literature.

```markdown
## 10. Resolved decisions (2026-11-10)

**R1. Novelty boundary.** *Grounding on Request* (arXiv:2610.33841) and arXiv:2610.19407 have
been read. Neither forces a model-generated verdict or binds the answer to it. The
explicit-source arms (§4.3) replicate the natural-language instruction baseline of
arXiv:2610.33841 (Table 7, p. 15) and are not claimed as new. The novelty claim is the text
in the freeze audit, §5.

**R2. Source letters are dropped.** No "Source A/B" appears anywhere. Sources are introduced
by modality headers, and only their positions swap:
  image-first:  [I] "Image:" <image> "Typed text:\n{text_question}" [F]
  text-first:   [I] "Typed text:\n{text_question}" "Image:" <image> [F]
ChartQA uses "Chart:" and "Report:\n{report}". O is effect-coded: −0.5 image-first, +0.5
text-first. There is no letter factor. β₂ and β₅ are read as effects of position only.
[Design decision] Changes §4.1 and §4.4.

**R3. One primary outcome.** The primary outcome in both regimes is the margin Δℓ of §6.2,
teacher-forced after the prefill `{m}\n\n#### `. The behavioural outcome is secondary and
uses the regime's native format: step-by-step solving (512 new tokens, strict `####`
parser) for GSM8K/SVAMP, and an answer-only decode (16 new tokens) for ChartQA-Conflict.
The 16-token decode is not used for GSM8K/SVAMP. Changes §6 and §7.

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
   items for both models. It records: competency yield, edit-gate pass rate, the share of
   answer-only decodes on ChartQA that match one of the two answers, the dev wording
   floor, and seconds per item.
4. `max_pixels` for ChartQA-Conflict is fixed from that pass.
No number from the dev pass changes R3, R4 or R7.
```

### Reasoning behind each resolution

**R1 (your Decision 1).** See §1.1 and the claim wording in §5.

**R2 (Decision 2): drop the letters.**
- If letters follow order, the design matrix has O and L identical, so their effects cannot be separated. The full 2 × 2 fixes that by doubling every cell.
- Letters do no work in this design. The verdict already names sources by modality, and the instruction stem already says "the image and the typed text".
- Of the four conflict papers that state their layout, only *Which Source Wins?* uses letters, and it ties A to the first position.

**R3 and R4 (Decision 3).**
- 7.3 pp is too lax. CoT-Mediate reports a 4.9-point gap as a real effect, and its paraphrase floors are 0.5–3.3% ([p. 6](https://www.alphaxiv.org/pdf/2607.27304?page=6)). A margin that calls 4.9 points "equivalent to zero" will not survive review. 5.0 pp sits above those floors and at the smallest effect a neighbour reports as real.
- There is no literature value for a log-likelihood margin. Tying it to the explicit-instruction ceiling gives it a plain reading: the verdict moves the answer by less than a quarter of what a direct instruction does.
- On GSM8K, forcing `####` straight after the verdict asks for a multi-step answer with no working. The margin still exists for every item; a 16-token decode may mostly match neither answer. That is why the short decode is dropped there. *This is my inference from the design; the dev pass in R8 measures the ChartQA side.*

Power for the 5 pp behavioural test, by number of analysable items *n* and share of items whose answer changes between verdicts *p* (normal approximation, true effect zero):

| *p* | n = 87 | n = 121 | n = 150 | n = 215 |
|---|---|---|---|---|
| 3% | 0.71 | 0.87 | 0.94 | 0.99 |
| 5% | 0.34 | 0.58 | 0.73 | 0.90 |
| 7.3% | 0.06 | 0.30 | 0.47 | 0.71 |

**R5 (Decision 4 and the draft's sample-size item).**
- 250 competency-passing items and an 87% edit-gate rate give about 215 analysable items, which is the right-hand column above.
- The 113 in *Which Source Wins?* is not a competency yield. It counts items "decidable at all four required endpoints" across degradation levels ([p. 18](https://www.alphaxiv.org/pdf/2608.17205?page=18)). The paper gives no clean chart-only accuracy for Qwen2-VL-2B that I could find, so the 2B yield has to be measured.
- Scenarios for 2B on the 199 confirm items, at an 87% edit-gate rate: a 30% competency yield leaves 52 items, 50% leaves 87, and 70% leaves 121. Only the best case has usable power, and only if answers are very stable. Secondary is the right status.
- For 3B the same arithmetic says ChartQA is borderline, hence the 100-item entry rule.
- Compute, extrapolated from the measured 2.40 s per 188-token row: about 2 hours for base arms on the roughly 1,400-item confirm pool, plus an estimated 45–50 s per transplanted item, so about 5–6 T4-hours per model for GSM8K/SVAMP. The per-item figure is an estimate; the dev pass measures it.

**R6.** See §2 for the numbers. The explicit-image arm currently asks the model to follow the image right after it has "said" the text is more reliable, which depresses the ceiling for a reason unrelated to instruction strength.

**R7 (Decision 5).**
- The local machine has no R and no `statsmodels`; the existing analysis code is standard-library Python with exact McNemar and Holm already written.
- `statsmodels` has no maximum-likelihood binomial mixed model. `BinomialBayesMixedGLM` fits by variational Bayes or MAP and returns posterior summaries, not the fit and Wald tests `glmer` gives. `pymer4` calls lme4 through R, so it needs R anyway.
- lme4 is the reference implementation; that is my background knowledge, since none of the 14 papers names a package.
- Mixed models stay out of the confirmatory path because convergence choices are forks, and the closest paper's mixed model failed outright (§1.4).
- The removed permutation test: with four templates, flipping the sign of each template's effect gives 2⁴ = 16 arrangements, so the smallest one-sided p is 1/16 = 0.0625. The C(8,4) = 70 count treats eight template-by-direction cells as exchangeable, which ignores the pairing and does not define a test for an interaction.
- Four levels are too few to estimate a random-effect variance, so K becomes a fixed factor.

---

## 4. Literal templates still missing

Proposed text **[Design decision]**. The explicit endings mirror the binding endings word for word, so the two arms differ by one noun phrase.

**GSM8K/SVAMP explicit endings** (X = "the image" or "the typed text"):
1. "Then solve only the problem from X, and ignore the other problem."
2. "Then solve only the problem given by X, and ignore the other one."
3. "Then work out only the problem from X, and disregard the other problem."
4. "Then solve only the problem in X, and leave the other problem aside."

This changes explicit ending 1 in the draft, which has no "ignore" clause.

**ChartQA-Conflict stems** (each begins "Question: {question}\n"):
1. "In two sentences, state whether the chart and the report give the same answer, and say which source you consider more reliable."
2. "In two sentences, say whether the chart and the report give the same answer, and state which source you find more reliable."
3. "In two sentences, judge whether the chart and the report support the same answer, and say which of the two sources is more reliable."
4. "In two sentences, note whether the chart and the report agree on the answer, and say which source you trust as more reliable."

**ChartQA-Conflict endings:**

| k | Non-binding | Binding (explicit: replace the bold phrase with "the chart" or "the report") |
|---|---|---|
| 1 | "Then answer the question." | "Then answer the question using only **the source you named as more reliable**, and ignore the other source." |
| 2 | "Then give an answer to the question." | "Then answer the question using only **the source you said is more reliable**, and ignore the other one." |
| 3 | "Then work out the answer to the question." | "Then work out the answer using only **the more reliable source you named**, and disregard the other source." |
| 4 | "Then answer the question from the sources." | "Then answer the question using only **the source you judged more reliable**, and leave the other source aside." |

---

## 5. Novelty claim (replaces dossier §4.1)

> Within the fourteen sources read, no study intervenes on a vision-language model's own stated source-reliability verdict, by prefix-forcing a minimally edited version of it, and measures whether the answer follows under image–text conflict with evidence order counterbalanced. Nor does any test whether an instruction that binds the answer to that verdict changes its effect. Prior work steers modality reliance with an external request and evaluates it by editing the evidence (Dassen et al., arXiv:2610.33841); predicts preference from evidence strength with no verbalization (Barua et al., arXiv:2610.19407); tests whether explanations mention edited visual evidence (Menzat et al., arXiv:2609.06704); or edits clinical content in a model's reasoning with no modality conflict (Bhowal et al., arXiv:2607.27304). We do not claim that prompt-based modality steering is new: our explicit-source arms replicate the natural-language instruction baseline of Dassen et al. and serve only as a ceiling.

Two guards against dismissal:
- Lead with what is intervened on. *Grounding on Request* holds the request fixed and edits the evidence; the thesis holds the evidence fixed and edits the self-stated verdict.
- CMC-Bench is unread. Read it before the related-work chapter is written.

---

## 6. Smaller corrections to the draft

- §4.4 cites *Which Source Wins?*, Appendix A, for strict parsing. The rule is in §3.3: "We do not search explanations or reasoning traces for embedded numbers" ([p. 5](https://www.alphaxiv.org/pdf/2608.17205?page=5)). Appendix A lists software versions.
- §6.2 defines Δℓ as image minus text. *Which Source Wins?* (Eq. 1) and Barua et al. (Eq. 1) use text minus image. State the sign convention next to the formula.
- §3.2 should say what the 113 counts (R5).
