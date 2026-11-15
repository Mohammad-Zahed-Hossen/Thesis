# Research objective: read this first

**Date:** 2026-11-15. **AI-generated** (Claude Code, OpenResearch session) from the repo at commit `9ad1853`.

**Verified against:**
- the PDFs in `Docs/Paper/`: the 20 earlier ones plus 2609.00550, 2610.30953, 2610.20805, 2609.29278, 2606.12747, 2610.37070;
- `Docs/PREREGISTRATION_VERDICT_TRANSPLANT.md` (draft, not frozen) and `CLAUDE.md`.

If this brief contradicts the prereg, the code or a PDF, those win.

## 1. The question in one sentence

When an image and a typed text support different answers, does a vision-language model's stated verdict about which source is more reliable causally change which source's answer it gives?

**Estimand.** A **controlled direct effect** (CDE):
- *What is set:* a verdict is prefix-forced into the model's own assistant turn. The model's own verdict and a minimally edited reversal of it are compared.
- *What is held fixed:* instruction (binding or not), evidence order and wording.
- *Never call it* mediation or a natural indirect effect. Forced verdicts are off-policy.

## 2. Hypotheses in plain language (prereg §2)

- **H₁, "the verdict decides".** Under the binding instruction, reversing the verdict moves the answer by more than a quarter of what an explicit "use the image / use the text" instruction does.
  - *Math primary outcome:* the behavioural shift in P(answer follows the named source) at template k = 1, with `para_flip − para` co-primary.
  - *Meaning if it holds:* the stated verdict is decision-relevant for source following.
- **H₀, "saying is not choosing".** All three must hold:
  - the reversal moves the answer by less than a quarter of that ceiling;
  - the behavioural TOST shows equivalence at ε = 5.0 pp;
  - the wording-floor gate passes.

  *Meaning if it holds:* the model follows an explicit instruction but not its own reversed verdict. Read it with one caveat: a null can also mean the model **resists an off-preference prefill** (arXiv:2606.12747).
- **Binding question (T1).** Is the verdict's effect larger with the binding instruction ("…solve only the problem from the source you named…") than without it?
  - T1 qualifies an H₁ reading; it is not a condition for H₁.
  - Prior evidence suggests instructions barely loosen own-turn content (arXiv:2610.20805), so a null T1 is plausible. Check the manipulation check (§7.5) first.
- **Other allowed outcomes:** *Undetermined* (the ceiling CI includes 0) and *Inconclusive*. A non-significant difference is never H₀.

## 3. Defensible novelty claim (after the 2026-11-15 audit)

> Within the 18 core sources, CMC-Bench, two Chapter 2 leads, and the 1,260 records screened in `Docs/Paper/lit-audit-2026-11-15/`, no study:
> - prefix-forces a minimally edited version of a VLM's **own source-reliability verdict**, with a matched-template control;
> - measures which source the answer follows under **image–text** conflict with counterbalanced order;
> - tests whether a **binding instruction** changes that effect.
>
> Each ingredient has precedent on its own, and none is claimed as new.

How this thesis differs from the closest papers:

| Paper | What it does | How this thesis differs |
|---|---|---|
| Bhowal et al., *Position, Not Provenance* (2607.27304) | Prefix-forces minimally edited clinical content in medical VQA | No source conflict, no verdict |
| Manalu et al., *Reasoning–Action Coupling* (2610.30953) | Edits a driving VLA's own decision sentence and subtracts a paraphrase response | Trajectory outcome, no image–text conflict |
| Li, Shi & Li, *Reasoning Traces vs Evidence* (2610.20805) | Puts a stored trace in the model's own thinking block under conflict; a verify instruction fails to loosen it | Text-only, whole-trace transplant, no verdict |
| Lee et al., *Same Semantics* (2609.00550) | Rendered-passage vs typed-passage conflict, with order flipping the winner | No verbalization intervention |
| Dassen et al., *Grounding on Request* (2610.33841) | Steers modality with external requests | Never forces the model's own text |
| Ghosh et al., *Which Source Wins?* (2608.17205) | Source of our stimuli; Δℓ margins | Source A/B letters, no verdict, no faithfulness test |
| Li et al., *Evidence Noncommutativity* (2609.26986) | Order (recency) effects in Qwen2.5-VL-3B | Closed choice, no rationale edits |
| Nemitz et al., *When to Call an Apple Red* (2604.06422) | VLMs violate their own stated rule | Observational; not intervening on the stated rule |

## 4. Claim boundaries (never claim these)

From `CLAUDE.md`:
- The effect is a CDE at fixed instruction, order and wording. It is not mediation and not a natural indirect effect.
- No "first" or "novel" beyond §3 above, always scoped to the records screened.
- In GSM8K/SVAMP both problems are valid. Confirmatory claims are about **source following**, not reliability judgement. ChartQA-Conflict (where reliability is meaningful) is exploratory (D4).
- Dev numbers (v3, v4, v5 dev) are for tuning, never findings. v3 compares two instructions, not verbalizations.
- Claims are made per model (Qwen2.5-VL-3B, -7B). A cross-model statement needs both to agree. 3B vs 7B is not a scaling law. Qwen2-VL-2B is diagnostic only.
- Literature traps:
  - *Which Source Wins?* tested 2B and 7B, not 3B.
  - The +16.7 / +15.0 pp order effect is natural-image VQA.
  - "Larger models are less faithful" is Lanham, not Turpin.
  - Dassen et al. do not prefix-force.

New from this audit:
- In Math, "image" means a **rendered image of a problem's text**. Results are about rendered-text vs typed-text arbitration, not visual evidence in general.
- An H₀ reading must name the **prefill-resistance** alternative explanation.
- Primary results are **conditional on dual-competent items**. Say so whenever an effect size is quoted.
- Do not cite Δℓ at `####` in Math as a measure of the answer the model goes on to give. It measures a different event (arXiv:2609.29278).

## 5. Reading order for a newcomer (13 papers)

1. Lanham et al. 2023 (2307.13702): the canonical CoT interventions.
2. Turpin et al. 2023 (2305.04388): unfaithful explanations under bias.
3. Bhowal et al. (2607.27304): the prefix-forcing and minimal-edit template this design follows.
4. Ghosh et al. (2608.17205): our stimuli and the Δℓ convention.
5. Li et al. (2609.26986): why order is counterbalanced and letters are banned.
6. Lee et al. (2609.00550): order flips the winner with rendered-vs-typed text, as in our stimuli.
7. Dassen et al. (2610.33841): the explicit-instruction baseline that our ceilings replicate.
8. Barua et al. (2610.19407): text evidence dominates; log-odds cue model.
9. Sánchez Villegas et al. (2604.14888): early answer commitment in VLM CoT.
10. Cox et al. (2603.01437) and Li et al. (2609.29278): why pre-CoT margins fail in Math (D1).
11. Manalu et al. (2610.30953): the closest edit-plus-paraphrase-control design.
12. Li, Shi & Li (2610.20805): own-turn traces dominate; instructions barely help.
13. Wang et al. (2606.12747): prefill awareness, the main validity threat to forcing.

## 6. Open questions

**This thesis can answer (per model, Math):**
- Does a reversed own verdict move source following beyond the wording floor?
- Does binding change that?
- How large is the effect relative to an explicit instruction?
- Does order moderate it (descriptively)?

**This thesis cannot answer:**
- Whether free (unforced) verdicts mediate choices. The study identifies a CDE only.
- Reliability judgement on natural images. Math uses rendered text, and ChartQA is exploratory.
- Generalization beyond the Qwen2.5-VL family or beyond dual-competent items.
- Whether a null reflects irrelevance or prefill resistance. This can only be partly probed via `verdict_nll`.
- Mechanism: which heads arbitrate (see 2611.12883, 2507.01790). That is future work.

**The literature does not yet answer:** any of the combined intervention in §3; no screened paper tests it.

## 7. Pointers

- Design spec: `Docs/PREREGISTRATION_VERDICT_TRANSPLANT.md`. §1.1 rewording proposed in the audit §1.3.
- Knowledge base: `Docs/Paper/THESIS_LITERATURE_KNOWLEDGE_BASE.md`
- This audit: `Docs/Paper/lit-audit-2026-11-15/` (report, `papers.csv`, `search_log.csv`, `references.bib`)
- Status and next steps: `Experiment/README.md`
- Rules: `CLAUDE.md`
