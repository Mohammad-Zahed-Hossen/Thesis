---

## 20. Baselines, controls, metrics and evaluation

### 20.1 Baselines: three kinds, all required

| Kind | Purpose | Example in a VLM study |
|---|---|---|
| **Trivial baseline** | Shows the effect is not achievable without the intervention | Always answer with the text answer; always answer with the image answer; majority-class |
| **Strongest available baseline** | Shows the intervention beats the competitive alternative | Best published prompt/decoding strategy; a second reasoning scaffold |
| **Matched-compute baseline** | Shows the effect is not merely extra computation | Neutral deliberation prompt with equal token budget, equal format, equal position |

Missing the *trivial* baseline lets reviewers ask whether a constant strategy already does as well. Missing the *matched-compute* baseline makes any causal claim about the intervention unsupportable. Your design's Arm 2 is exactly a matched-compute baseline, and its early inequality (61.2 vs 3.4 tokens) is exactly why such a baseline must be verified, not assumed. **[L2/L3]**

### 20.2 Controls: four useful kinds

1. **Placebo control** — same form, no active ingredient (neutral deliberation of matched length).
2. **Negative control** — a condition where no effect is expected (aligned, non-conflicting input).
3. **Positive control** — a condition where an effect is known to exist (a manipulation that must move the metric), catching a broken pipeline.
4. **Dose–response control** — vary the strength of the manipulation (e.g., partial vs explicit conflict statements) to check monotonicity.

A design with all four can survive most reviewer objections. Two are usually enough for a thesis: placebo plus negative. **[L3]**

### 20.3 Metrics: construct validity first

For each metric, write three lines:

```text
CONSTRUCT: what it is supposed to measure
OPERATION: exactly what is counted
KNOWN CONFLATION: what else could move it
```

**Metric-validity contributions are among the safest thesis contributions.** A verified example is the selective-classification literature, where common multi-threshold metrics fail stated requirements and a replacement metric changes rankings on most datasets ([AUGRC, arXiv:2407.01032](https://arxiv.org/abs/2407.01032)). The lesson generalizes: *if a metric changes the ranking, the metric is part of the science.*

Practical requirements **[L3]**:

- **Deterministic** where possible: regex, exact match, entity classification with stated rules.
- **Insensitive to the confound** you claim to control: e.g., a measure of engaged problem, not of answer correctness.
- **Reported as distributions**: per-arm token counts, truncation rates, per-class breakdowns — not just means.
- **Reported with uncertainty**: effect size plus confidence interval, not only a p-value.
- **Validated**: manual audit of a random sample, with agreement rate reported.

### 20.4 If you must use an LLM judge

- Build a small human-labeled calibration set (50–100 items) and measure agreement with the judge.
- Freeze the judge prompt and model revision.
- Report judge agreement in the thesis; never present judge outputs as ground truth.
- Prefer a deterministic classifier whenever one is defensible; use judging only for genuinely semantic categories.

### 20.5 Statistical reporting checklist

- Unit of analysis stated explicitly.
- Paired vs unpaired test justified by the design.
- Effect size with CI (odds ratio, risk difference, Cohen's h, etc.).
- Multiple-comparison handling for secondary analyses (label exploratory).
- Sensitivity check: does the conclusion hold on a random half, or with an alternative valid metric?
- Robustness to seed/decoding variation.
- All raw numbers reproducible from released outputs.

**[L1]** Experiment-reporting variance and reproducibility issues are well documented in ML; the standard remedy is transparency about variance, seeds, and configuration ([Deep RL That Matters, arXiv:1709.06560](https://arxiv.org/abs/1709.06560); [NeurIPS 2019 Reproducibility Program, arXiv:2003.12206](https://arxiv.org/abs/2003.12206)).

### 20.6 The evaluation trap specific to your domain

When reporting a behavioral shift, three quantities must always be reported together, or the result is uninterpretable **[L2/L3]**:

1. **The shift** (e.g., image-following 89.5% → 25.8%).
2. **The outcome composition change** (text-following and abstention rates), because a shift can be produced by abstention rather than arbitration.
3. **The token/quality diagnostics** (per-arm token counts, truncation rates, parse rates), because a "shift" can be produced by output truncation.

Your v3 report demonstrates why: the raw shift was accompanied by 13.7% abstention and, in earlier runs, by near-total truncation. Reporting all three keeps the claim honest and makes the analysis robust to the most likely reviewer objection. **[L2]**
