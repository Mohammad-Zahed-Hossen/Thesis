# Idea: Does the Verdict Decide?

*Rewritten 2026-11-10. This replaces the earlier AI-generated narrative, which claimed a "100% untouched gap" and causal steering from v3. Neither claim survived the audit.*

**Sources:**
- `Archive/Paper/lit-dossier-verdict-transplant/lit-dossier-verdict-transplant.md` (the dossier)
- the PDFs in `Archive/Paper/`
- the dev data in `Experiment/results_v4/`

The design specification is `Docs/PREREGISTRATION_VERDICT_TRANSPLANT.md`.

---

## 1. The question

When an image and a typed text support different answers, a vision-language model can state which source it considers more reliable before answering. **Does that stated verdict causally determine which source's answer the model then gives, or does the answer come from somewhere else?**

The test is prefix forcing:
1. Write a verdict into the model's own response turn.
2. Hold the instruction, evidence order and wording template fixed.
3. Compare the answer when the verdict names the image with the answer when it names the typed text.

This identifies a **controlled direct effect** of the verdict. It is not a natural indirect effect, so we do not call it "mediation".

---

## 2. What prior work already covers

Read depth for each paper is listed in the dossier, §0.

| Paper | What it already does | What it leaves open for us |
|---|---|---|
| *Which Source Wins?* (arXiv:2608.17205) | Builds the GSM8K/SVAMP and ChartQA-Conflict stimuli we use; forced arbitration under degradation | "we do not test whether models detect the contradiction, express uncertainty, or abstain"; no verbalization |
| *Mixed Signals* (arXiv:2504.08974) | Verbalized, CoT and Decomposed prompts for *detecting* mismatches | Whether a stated verdict steers the answer |
| Deng et al., *Words or Vision* (arXiv:2503.02199) | Blind faith in text; source instructions move preference only slightly; effect of token order | No reasoning or verdict intervention |
| Zhang et al. (arXiv:2511.02243) | Modality following is set by relative single-source uncertainty and a per-model balance point | No verbalization; supplies our stratification variable |
| Sánchez Villegas et al. (arXiv:2604.14888) | Answer inertia in VLM chain-of-thought; the CoT only partly reveals text-hint reliance | The CoT is never edited; no source verdict |
| CoT-Mediate (Bhowal et al., arXiv:2607.27304) | Prefix-forced edits of the model's own reasoning vs. re-prompting, with a paraphrase floor | Medical VQA with clinical attributes; no modality conflict |
| *Hidden Commitment* (arXiv:2610.38296) | Text LLMs: choosing a source and disclosing a conflict are separable internal states | Text-only; concerns disclosure, not a reliability verdict; no prefix forcing |
| Noncommutativity (arXiv:2609.26986) | Evidence order shifts source following by about 15 pp in Qwen2.5-VL-3B | No verbalization; sets our order protocol |

**The open space (dossier §4.1).** In the sources examined, no study prefix-forces opposite source-reliability verdicts into a VLM's own generation under image–text conflict, while holding evidence order, wording template and instruction fixed and testing whether a binding instruction makes the verdict decision-relevant. Novelty is claimed only within these sources.

Still unread in full: *Grounding on Request* (arXiv:2610.33841), the closest neighbour for the binding arm, and arXiv:2610.19407.

---

## 3. Hypotheses: "saying is not choosing" and its rival

- **H₁ (the verdict decides).** Forcing the verdict to name the image rather than the typed text raises image-following answers by more than the pre-registered equivalence margin. The effect should be larger under the binding instruction.
- **H₀ (saying is not choosing).** Reversing the verdict changes image-following by less than the margin, even under binding. The answer comes from the instruction, evidence order or the model's own commitment, not from what the verdict says.

Each outcome would mean something different.

| Outcome | Interpretation |
|---|---|
| H₁ holds under binding but not without it | The verdict is usable, but only when the prompt makes it decision-relevant. The dev null was instruction dominance, not unfaithfulness. |
| H₀ holds even under binding, while the explicit-source ceiling moves answers | A real faithfulness failure: the model can follow a source instruction but does not follow its own stated verdict. |
| Even the explicit ceiling barely moves answers | Prompt-level control is weak for this model. Neither H₁ nor H₀ can be read from the binding arm. |

**Expected asymmetry** (Tang et al., arXiv:2602.14518). The model's own verdict says "the typed text is more reliable" about 89% of the time. Flipping the verdict against that may do less than keeping it. So we test the two directions separately and do not rely only on the pooled estimate.

---

## 4. Design: four-way factorial

Each item is crossed with:

| Factor | Levels |
|---|---|
| Verdict direction **D** | Names the image / names the typed text. Built as a minimal edit of the model's own verdict, plus a no-verdict level |
| Wording template **K** | 4 paraphrases of the instruction |
| Evidence order **O** | Image first / typed text first. The instruction stays fixed before both sources |
| Binding instruction **B** | Non-binding / binding ("solve only the problem from the source you named as more reliable") |

**Controls run alongside the factorial:**
- **Explicit-source ceilings** (`explicit_image`, `explicit_text`): how far a direct source instruction moves answers.
- **Wording floor:** same direction, reworded clause.
- **Single-source baselines** (`base_image`, `base_text`): define the competency subset.

**Outcomes:**
- Primary: the answer after a forced `####`, as a short greedy decode and as a length-normalized log-likelihood margin between the image answer and the text answer.
- Secondary: free-form solving.

**Two conflict regimes:**
- Task-selection (GSM8K/SVAMP): neither problem is wrong, so "reliability" is ill-posed.
- Evidence conflict (ChartQA-Conflict): the chart is correct and the report is counterfactual.

**Models:** Qwen2.5-VL-3B-Instruct and Qwen2-VL-2B-Instruct.

---

## 5. What the dev data say (tuning only, not findings)

Computed on the 110 of 200 dev items that both single-source arms solve (dossier §2.2). These come from the v4 long-horizon design, which v5 replaces.

| Instruction | Contrast | Items whose answer changes | Δ image answers |
|---|---|---|---|
| Neutral | verdict image vs. text | 35.5% | +20.9 pp |
| Neutral | wording a vs. b | 24.5% | +7.3 pp |
| Conflict | verdict image vs. text | 7.3% | −1.8 pp |
| Conflict | wording a vs. b | 22.7% | −1.8 pp |

The verdict is not inert in general; it is inert only under the conflict instruction. That is why the binding arm and the explicit ceilings are needed before any "saying is not choosing" claim.

---

## 6. Known weak points

1. "Reliability" is ill-posed in GSM8K/SVAMP. Reliability claims belong to ChartQA-Conflict.
2. ChartQA-Conflict has only 229 items. With the harness default `--dev_size 200`, almost nothing would be left for confirmation (see the pre-registration, §3.2).
3. Forced verdicts are off-policy even after minimal edits. The perplexity of each forced verdict is recorded as a covariate.
4. Verdict and attempt labels in `score_v4.py` are regex heuristics. About 200 items will be double-coded and κ reported.
5. Two small models from one family. A second family would be needed for a main-venue paper.
