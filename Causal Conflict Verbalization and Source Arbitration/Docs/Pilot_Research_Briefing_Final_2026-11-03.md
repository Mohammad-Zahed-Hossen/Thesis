# Causal Conflict Verbalization and Source Arbitration in Vision-Language Models

**Candidate:** Mohammad Zahed Hossen, Final-Year BSc, Computer Science & Engineering
**Target architecture:** `Qwen/Qwen2.5-VL-3B-Instruct` · **Date:** 3 November 2026
**Classification:** *Pre-Registration Feasibility Study & Empirical Pilot Progress Report*

---

## 1. Executive Summary and Scientific Gap

A cross-modal contradiction arises when image $I$ and text $T$ specify different problems with answers $y_I \neq y_T$. The output then reveals an *arbitration* decision $S \in \{\text{image}, \text{text}, \text{abstain}\}$. *Which Source Wins?* (arXiv:2608.17205) measures modality reliance passively under forced choice. *CLASH* (arXiv:2511.19199) treats detected contradiction only as a refusal target. Neither manipulates an **intermediate verbalization** of the conflict, so it is untested whether verbalization *steers* arbitration or merely *rationalizes* it.

**Research question.** Does conflict verbalization causally change $\Pr(S)$ beyond a length-matched control?

$$H_0:\ \Pr(S{=}\text{image}\mid\text{Arm 3}) = \Pr(S{=}\text{image}\mid\text{Arm 2}) \qquad H_1:\ \text{the two differ}$$

## 2. Controlled 4-Arm Factorial Protocol

**Data.** $N = 1{,}619$ clean (degradation level 0) image-channel conflict pairs from `vlm-modality-research/modality-conflict-arbitration-v2`: 1,319 from GSM8K and 300 from SVAMP. Each pairs an image-rendered word problem with a *different* text problem. Every item passes through every arm (within-item design).

| Arm | Instruction before solving | Budget | Role |
|---|---|---|---|
| 1 Direct QA | None | 80 tok | Baseline |
| 2 Placebo | Two sentences *neutrally describing* image and text, no comparison | 200 tok | Compute / length control |
| 3 Conflict verbalization | Two sentences on *agreement vs. contradiction* and *source reliability* | 200 tok | Intervention |
| 4a/4b Prefill | Forced "contradict → image" vs. "agree → text" rationale prefix | 20 tok | Rationale-sensitivity probe |

**Why Arm 2 matters.** Extra test-time compute alone can change answers. Arm 2 matches Arm 3 in sentence count, budget, and output length (mean 158 vs. 169 tokens), so $\text{Arm 3} - \text{Arm 2}$ isolates verbalization *content*.

## 3. Preliminary Pilot Arbitration Findings

| Condition | Visual | Text | Abstention | Ambiguous |
|---|---|---|---|---|
| Arm 1: Direct QA | 223 (13.8%) | 1,385 (85.5%) | 0 (0.0%) | 11 (0.7%) |
| Arm 2: Placebo | **1,449 (89.5%)** | 145 (9.0%) | 4 (0.2%) | 21 (1.3%) |
| Arm 3: Conflict verbalization | **417 (25.8%)** | 954 (58.9%) | **221 (13.7%)** | 27 (1.7%) |

Paired visual vs. non-visual table (discordant pairs $b = 1057$ for Arm 2 visual → Arm 3 non-visual, $c = 25$ for the reverse):

$$\Delta_{\text{arb}} = \hat P_{\text{vis}}(2) - \hat P_{\text{vis}}(3) = +63.7\ \text{pp}, \qquad \chi^2_{\text{McNemar}} = \frac{(|b-c|-1)^2}{b+c} = 982.40,\ p = 1.2\times10^{-215}$$

Exact binomial McNemar: $p \approx 10^{-275}$. Paired odds ratio $b/c = 42.3$ (95% CI 28.4–62.9); marginal odds ratio $24.57$ (95% CI 20.24–29.83). Cohen's $h = 1.42$, well above the large-effect threshold of $0.8$.

<div style="page-break-after: always;"></div>

## 4. Computational Verification: the Exact-Match Cross-Over

Lexical labels could reflect surface wording rather than actual computation. Exact match against each source's ground truth checks this:

| Condition | Exact match $y_I$ (image problem) | Exact match $y_T$ (text problem) |
|---|---|---|
| Arm 2: Placebo | **35.6%** (577) | 4.7% (76) |
| Arm 3: Conflict verbalization | 11.7% (190) | **35.8%** (579) |

The correctly solved problem flips almost symmetrically, so verbalization changes *which problem the model computes*. This is not degradation: total correctness is similar (40.3% vs. 47.5%). Arm 3 also yields **13.65%** (221/1,619) explicit refusals stating the premises cannot be reconciled, against $\le 0.25\%$ in Arms 1–2.

## 5. Computational Envelope and Engineering Robustness

- **Runtime.** Single Colab T4, FP16 + PyTorch SDPA, batch 8, greedy decoding (seed 42). Recorded generation time: 102.5 min for all five conditions (project logs: 104.5 min end-to-end). Peak VRAM is *not* in the retained outputs and must be re-logged.
- **Deterministic scoring.** Regex answer extraction after `####` (last-number fallback), a fixed abstention lexicon, and entity-overlap source labels with exact-match tie-breaking. No human or LLM judges.
- **Checkpointing.** Per-batch CSV with resume-on-restart; all $1{,}619 \times 5$ records complete.
- **Truncation (disclosed).** Outputs hit the token cap in 98.1% (Arm 1), 37.6% (Arm 2), and 44.2% (Arm 3) of runs. Exact-match rates are *lower bounds*, and Arm 1 needs a budget-matched re-run.

## 6. Scientific Significance and Validity Boundaries

**Rejecting the compute/inertia null ($H_0$).** A 63.7 pp paired shift between length-matched arms cannot come from extra tokens or a fixed default modality preference. Verbalization is not inert commentary on a decision already made.

**Causal steering ($H_1$, instruction level).** Conflict verbalization breaks the visual capture seen under neutral description, and the model then executes the other problem. Caveat: describing the image (Arm 2) itself raises visual reliance above Arm 1 (89.5% vs. 13.8%). The effect is best stated as *description-induced capture, reversed by conflict verbalization*.

**Open mechanism question.** Arms 2 and 3 differ in both the *instruction* and the *generated verbalization*, and the pilot does not yet show which mediates the effect. Arm 4 is mixed: opposing prefixes change 41.3% of answers, yet the "image" prefix almost never yields the image answer (1.5%). This partial rationale–answer dissociation needs mediation controls in the formal study.

**Pathways to trustworthiness.** Under contradiction, conflict verbalization yields selective prediction (abstaining instead of silently defaulting to vision). This is a low-cost, inference-only lever for compact VLMs.
