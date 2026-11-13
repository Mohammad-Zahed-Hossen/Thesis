# Docs/Parked_Proposals — Alternative Thesis Proposals (Not Pursued)

Full "canonical" research proposals for the candidates that lost to the conflict-verbalization topic (now *Does the Verdict Decide?*) in September 2026. Each one gives a title, anchor papers, hypotheses, an experimental design on small open VLMs, metrics, and pre-stated **kill conditions**.

**Trust level:** Historical, AI-generated. Anchor-paper claims were not all re-verified, and several assume a "layer 18" locus that later audits could not confirm.
**Rule (AGENTS.md §3.5):** Do **not** reopen any of these without new primary evidence. Why each was parked: [../Decision_Audits/README.md](../Decision_Audits/README.md) and [../Context/Canonical_Rejected_and_Parked_Thesis_Fields_Report.md](../Context/Canonical_Rejected_and_Parked_Thesis_Fields_Report.md).

> **Token tip for agents:** These files are short (9–19 KB). The table below is enough unless you are writing a "considered alternatives" section of the thesis.

---

## Proposals

| File | Field | Title / question | Anchor literature | Kill conditions | Why parked |
|---|---|---|---|---|---|
| [Canonical_Proposal_1_Reasoning_Trace_Degradation.md](Canonical_Proposal_1_Reasoning_Trace_Degradation.md) | A (audit "Candidate B" / Phase 3 "Q1") | *Decomposing Multimodal Reasoning Trace Degradation: Causal Reasoning vs. Positional and Attention Dilution Artifacts.* Does visual-evidence use drop because of reasoning, or just sequence position and attention dilution? Linear probes at layers 18/30. | RH-Bench (arXiv:2505.21523, NeurIPS 2025); *Seeing or Knowing?* (2607.26326) | K1 position collapse (TOST, θ = 0.05); K2 dilution collapse (zero ΔVIG slope) | Headline claim **substantially pre-empted** by RH-Bench, Remember-R1 and ReGround. Classed RESERVE on 2026-09-23. Phase 3 kill-gate: it doesn't survive in its original form. |
| [Canonical_Proposal_2_Binding_IDs_Natural_Transfer.md](Canonical_Proposal_2_Binding_IDs_Natural_Transfer.md) | C (Candidate C / "Q2") | *Do Latent Visual Binding Identifiers Survive Beyond Synthetic Grids? A Placebo-Controlled Natural-Image Transfer Audit.* Activation-swap arms incl. noise/background placebos and intra-scene swap. | *Uncovering Grounding IDs* (2509.24072, ICML 2026); *In-Context Vision Language Binding* (2505.22200, CVPRW 2025) | K4 placebo failure; K5 natural-image collapse (net directed flip ≤ 0.10 or repetition > 0.40) | Gap was verified, but the topic lost on risk/fit when A was chosen. Phase 3 found the swap is applied across all layers, with no single causal layer. |
| [Canonical_Proposal_3_Cultural_VLM_Modality_Decoupling.md](Canonical_Proposal_3_Cultural_VLM_Modality_Decoupling.md) | D, v1.0 (diagnostic) | *Decoupling Visual Reliance from Correctness: A Placebo-Controlled Diagnostic of Cultural Prior Dominance and Selective Prediction in Multimodal VLMs.* | BICR (2605.10893); SIEVES (2604.25855); Evidence-Order Calibration (2609.09184) | Placebo/blank-image sensitivity; selective-risk (AUGRC) gates | **Superseded** by v2.1 (below) inside the four-proposal audit. |
| [Canonical_Proposal_3_Cultural_Multimodal_Causal_Steering.md](Canonical_Proposal_3_Cultural_Multimodal_Causal_Steering.md) | D, v2.1 (mechanistic) | *Disentangling Perceptual Deficit from Late-Layer Parametric Pre-emption: Causal Bottleneck Localization and Activation Steering in Low-Resource Cultural VLMs.* Layer-wise probes plus activation steering on Bengali cultural entities. | *Where Do Multilingual VLM Encoders Fail?* (2608.30725); TRAPSBench | Steering Recovery Rate < 10% or generation collapse (repetition > 0.40) | **Deprecated 2026-09-23.** The layer-18 bottleneck was an unverified assumption, the method was partly pre-empted by BabelSteering (Aug 2026), and the BanglaProtha image-leakage/blank-image boundary checks were unresolved. |

Both Proposal 3 files are duplicated in `Archive/Bengali VLM/`, alongside the original Bangla selective-prediction proposal and its audits.

---

## Reuse value

- **Design patterns worth borrowing:** pre-stated kill conditions, placebo arms, and TOST equivalence margins. The v5 pre-registration already uses the same discipline.
- **Not reusable as evidence:** anchor-paper summaries and any "verified gap" wording. Re-check against primary sources first.

