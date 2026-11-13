# Docs/Decision_Audits — How the Thesis Topic Was Chosen

Adversarial audits, syntheses and agent transcripts from topic selection, mostly dated 2026-09-20 to 09-23. Four directions were compared:

| Code in audits | Direction | Outcome |
|---|---|---|
| **A** / Canonical | Trustworthy VLM: conflict verbalization & source arbitration | **Chosen.** Later re-framed as the verdict transplant, *Does the Verdict Decide?* |
| **B** / Proposal 1 | Multimodal reasoning-trace degradation | Reserve → parked. Headline claim pre-empted by RH-Bench (arXiv:2505.21523). |
| **C** / Proposal 2 | Visual binding-IDs natural-image transfer | Gap verified, but parked when A was chosen. |
| **D** / Proposal 3 | Bengali cultural VLM (selective prediction → causal steering) | Deprecated. The layer-18 bottleneck was unverified, and BabelSteering partly pre-empted it. |
| — | Medical Imaging & FL; Multimodal Agents | Rejected earlier: crowded/occupied or too risky for a viva. |

**Trust level:** Historical, AI-generated decision records. Several are raw chat or agent transcripts ("Viewed…", "Listed directory…").

> [!WARNING]
> Most files here pre-date the November audits. They repeat two withdrawn claims: a "100% genuine / untouched gap", and that v3 showed verbalization *causally* steers arbitration. Only [Idea.md](Idea.md) reflects the current framing. Current design: [../PREREGISTRATION_VERDICT_TRANSPLANT.md](../PREREGISTRATION_VERDICT_TRANSPLANT.md). Current novelty boundary: [freeze audit §5](../Paper/prereg-freeze-audit/prereg-freeze-audit.md).

> **Token tip for agents:** Read [Idea.md](Idea.md) (7 KB) first; it is usually all you need. Open the others only to answer "why was X rejected?". For that, [../Context/Canonical_Rejected_and_Parked_Thesis_Fields_Report.md](../Context/Canonical_Rejected_and_Parked_Thesis_Fields_Report.md) is the consolidated record.

---

## Files (newest / most useful first)

| File | Size | Date | Type | What it contains |
|---|---|---|---|---|
| [Idea.md](Idea.md) | 7 KB | **2026-11-10** | Rewritten summary | **Current idea statement** for *Does the Verdict Decide?* (write a verdict into the model's own turn, flip it, see if the answer follows). Explicitly retracts the "100% untouched gap" and v3 causal-steering claims. Its `Archive/Paper/…` paths now live at `Docs/Paper/…`. |
| [final_adversarial_thesis_decision_audit.md](final_adversarial_thesis_decision_audit.md) | 67 KB | 2026-09-23 | Audit (Claude Opus 4.6) | Independent adversarial audit of candidates A–D. A and C have verified gaps, B is substantially pre-empted (RESERVE), and D passes with caveats (later deprecated). The audit that settled topic A. |
| [Final Four-Proposal Thesis Decision Audit.md](<Final Four-Proposal Thesis Decision Audit.md>) | 96 KB | ≈ 2026-09-23 | Audit | Evidence verification and decision readiness for all four proposals. Gives each one's core question, hypotheses H₀/H₁, arms (incl. Arm 4 Lanham-style prefilling, the ancestor of the verdict transplant), and Proposal 3 v1.0 → v2.1 deprecation. |
| [Clean Explanation (All 4 Idea).md](<Clean Explanation (All 4 Idea).md>) | 91 KB | ≈ 2026-09-23 | Plain-English explainer | Walks through the four-proposal audit for a human reader. Warns it is "a decision audit, not proof the thesis is validated". |
| [Structural Taxonomy Mind Map & Plain-English Explanations.md](<Structural Taxonomy Mind Map & Plain-English Explanations.md>) | 26 KB | Sept 2026 | Explainer | Where each candidate sits in the multimodal-AI taxonomy (ASCII mind map), with lay explanations. Useful for the thesis introduction and related-work framing. |
| [Canonical Thesis Topic Related Paper.md.md](<Canonical Thesis Topic Related Paper.md.md>) | 63 KB | Sept 2026 | Chat transcript | Feasibility autopsy of **CLASH** (2511.19199; its label is "a contradiction exists", not which source wins) and **Which Source Wins?** (2608.17205; GSM8K/SVAMP two-candidate ground truth). Explains why the stimulus set comes from *Which Source Wins?*. |
| [Cross_Modal_Discovery_Synthesis_and_Handover (MA & MVLM).md](<Cross_Modal_Discovery_Synthesis_and_Handover (MA & MVLM).md>) | 14 KB | 2026-09-20 | Synthesis / handover | Consolidates AlphaXiv, Gemini, Perplexity and Claude discovery reports for the Multimodal Agent and Multimodal VLM streams; records the surviving RQ held in queue. |
| [FINAL THESIS DECISION AUDIT.md](<FINAL THESIS DECISION AUDIT.md>) | 25 KB | Sept 2026 | Agent transcript + audit | Earlier cross-field audit: Cross-Modal vs. Medical Imaging (selective classification under sensor shift; AUGRC already formalised by Traub et al.) vs. Multimodal Agent, with kill gates. |
| [Medical Imaging & FL.md](<Medical Imaging & FL.md>) | 40 KB | Sept 2026 | Agent transcript + audit | Reads the four `Archive/Medical Imaging & FL/` reports. Maps areas A–D (non-VLM selective prediction, FL, medical VLMs) and the one surviving niche (Fed-CRC-Seg / Fed-LoRA). |
| [Multimodal Agent.md](<Multimodal Agent.md>) | 14 KB | Sept 2026 | Audit | Primary-literature autopsy (AdaTooler-V, VTool-R1, ACTIVE-o3, Thyme, …). Active perception and action-value prediction are occupied. |
| [Proposed Idea Related Paper.md](<Proposed Idea Related Paper.md>) | 36 KB | ≈ 2026-09-21 | Paper autopsies | RH-Bench and binding-ID anchors for backup candidates Q1/Q2. Verdict: narrows Q1 but doesn't kill the mechanistic version, and there is no single causal layer 18. Duplicate of `Archive/Extra Field Exploration/Phase 3/Paper Autopsys.md`. |

---

## Related

- [../Parked_Proposals/](../Parked_Proposals/README.md): full write-ups of candidates B, C, D.
- [../Context/](../Context/README.md): September project context and the consolidated rejected/parked fields report.
- [../../Archive/](../../Archive/README.md): raw exploration reports per domain (`Bengali VLM/`, `Medical Imaging & FL/`, `Multimodal Agent/`, `VLM/`, `Extra Field Exploration/`).
- Per [../../AGENTS.md](../../AGENTS.md) §3.5: **no reopening parked fields without new primary evidence.**

