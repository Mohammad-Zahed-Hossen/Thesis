# Docs — Design Spec, Literature & Decision Records

Everything about the thesis that is **not code or data**: the pre-registration draft, the primary-source literature folder, and the AI-generated decision trail from topic discovery.

**Trust level (per [../AGENTS.md](../AGENTS.md) §2):** All `.md` files here are AI-generated tracking documents, **not ground truth**. Exceptions in practice: the pre-registration is the *design spec* (check it against `Experiment/*.py`), and the PDFs in `Paper/` are primary sources.
**Ground truth** lives in [../Experiment/](../Experiment/) (code + raw results).

> **Token tip for agents:** For almost any current task you need only three things here: [RESEARCH_OBJECTIVE.md](RESEARCH_OBJECTIVE.md) (quick brief), [PREREGISTRATION_VERDICT_TRANSPLANT.md](PREREGISTRATION_VERDICT_TRANSPLANT.md), and [Paper/README.md](Paper/README.md). Everything else is September-2026 history under the old topic framing.

---

## Layout

```
Docs/
├── README.md                                     This file
├── RESEARCH_OBJECTIVE.md                         ★ CURRENT onboarding brief (RQ, estimand, narrowed novelty, reading order)
├── PREREGISTRATION_VERDICT_TRANSPLANT.md         ★ CURRENT design spec (draft, not frozen)
├── Paper/                                        ★ CURRENT 29 PDFs + 16 related_repos/ + lit KB + lit-audit-2026-11-15 + Fable 5.2 audit + dossier + freeze audit → Paper/README.md
├── Context/                                      Historical project context (Sept 2026)               → Context/README.md
├── Decision_Audits/                              Topic-selection audits (Sept 2026; Idea.md is Nov)  → Decision_Audits/README.md
├── Parked_Proposals/                             Full proposals for parked alternatives               → Parked_Proposals/README.md
├── CANONICAL_THESIS_MASTER_REPORT.md             STALE — v3-era "definitive record"
├── CANONICAL_THESIS_PIPELINE_ROADMAP.md          STALE — v3-era execution roadmap
└── Canonical_Thesis_Topic_Specification (Locked).md  STALE — v3-era locked topic/protocol
```

---

## Current documents

| File | Status | What it is |
|---|---|---|
| [RESEARCH_OBJECTIVE.md](RESEARCH_OBJECTIVE.md) | **Current** (post-2026-11-15 audit) | Concise brief for future agents: RQ, CDE estimand, pre-registered hypotheses, narrowed novelty claim, claim boundaries, prioritized 13-paper reading order, and open pre-freeze questions. |
| [PREREGISTRATION_VERDICT_TRANSPLANT.md](PREREGISTRATION_VERDICT_TRANSPLANT.md) | **Draft, not frozen** | Pre-registration for *Does the Verdict Decide?*. Models, stimuli, factorial arms (non-binding / binding / explicit ceilings), minimal-edit verdicts (`own`, `flip`, `none`, `para`, `para_flip`), regime-split primary outcomes (behavioural in Math per D1, Δℓ in exploratory ChartQA per D4), competency conditioning, equivalence margins, narrowed novelty claim. Pre-freeze decisions D1–D5, 2026-11-14 gate updates, Fable 5.2 forensic fixes (`F2`, `F3`, `F5`–`F13`, `Upgrades 1–5`), 2026-11-15 audit §1.3/§4 sync, and the 2026-11-16 fresh dev rerun (`34,920` rows + `px501k` R8.4 comparison + `analysis_dev/` incl. `lme4_out.txt`) are integrated into §10–§11; `coding_v5/` human coding and locking ChartQA `max_pixels` in §3.4 remain before tagging `prereg-v5`. The [freeze audit](Paper/prereg-freeze-audit/prereg-freeze-audit.md) gave it a **red light** on 2026-11-10; initial v5 dev audits live in [../Thesis/docs/Archive/dev v5/](<../Thesis/docs/Archive/dev v5/>) and [fable52-prefreeze-audit-2026-11-15.md](Paper/fable52-prefreeze-audit-2026-11-15.md). |
| [Paper/](Paper/README.md) | Current | Complete 18-paper + CMC-Bench knowledge base ([THESIS_LITERATURE_KNOWLEDGE_BASE.md](Paper/THESIS_LITERATURE_KNOWLEDGE_BASE.md)), pre-freeze literature audit + 2026-11-17 gap-closure addendum ([lit-audit-2026-11-15/](Paper/lit-audit-2026-11-15/lit-audit-2026-11-15.md), `1,452` records, `6` A + `41` B), Fable 5.2 pre-freeze forensic audit ([fable52-prefreeze-audit-2026-11-15.md](Paper/fable52-prefreeze-audit-2026-11-15.md)) + 16 snapshotted repos ([related_repos/](Paper/related_repos/README.md)), post-v5 direct PDF audit ([post-v5-pdf-audit.md](Paper/post-v5-pdf-audit/post-v5-pdf-audit.md)), **29 active local PDFs** (20 core/lead + 6 audit A-papers + 3 cited B-papers; 0 core missing), the 2026-11-10 dossier, and the pre-registration freeze audit. |

---

## Stale v3-era top-level documents

Written ≈ 2026-09-24 under the old title *Causal Conflict Verbalization and Source Arbitration in VLMs*, with the single model Qwen2.5-VL-3B and the v3 4-arm placebo design. They present the v3 instruction contrast (N = 1,619, +63.74 pp) as causal proof of verbalization; later audits withdrew that reading. Use only for history.

| File | What it was |
|---|---|
| [CANONICAL_THESIS_MASTER_REPORT.md](CANONICAL_THESIS_MASTER_REPORT.md) | 54 KB "definitive scientific record & thesis architecture" for the v3 design. |
| [CANONICAL_THESIS_PIPELINE_ROADMAP.md](CANONICAL_THESIS_PIPELINE_ROADMAP.md) | End-to-end execution roadmap (local LaTeX/analysis + Colab inference). Paths point to an old `Finalize Topic/` folder. |
| [Canonical_Thesis_Topic_Specification (Locked).md](<Canonical_Thesis_Topic_Specification (Locked).md>) | "Locked" topic spec and experimental protocol for v3. |

---

## `Context/` — historical project context

Frozen parent field, ranked/rejected fields, September progress map and handover. Full index: [Context/README.md](Context/README.md).

---

## `Decision_Audits/` — how the topic was chosen

Adversarial audits and syntheses (mostly 2026-09-20 → 09-23) comparing four directions: Trustworthy VLM / conflict verbalization (chosen), Bengali cultural VLM, Medical Imaging & FL, Multimodal Agents. Some are raw chat/agent transcripts. Full index with candidate-outcome table: [Decision_Audits/README.md](Decision_Audits/README.md).

| File | What it is |
|---|---|
| [Idea.md](Decision_Audits/Idea.md) | **Most recent (rewritten 2026-11-10).** Plain statement of the *Does the Verdict Decide?* idea; explicitly retracts the earlier "100% untouched gap" and v3 causal-steering claims. Its `Archive/Paper/` paths now mean `Docs/Paper/`. Best single entry point in this folder. |
| [final_adversarial_thesis_decision_audit.md](Decision_Audits/final_adversarial_thesis_decision_audit.md) | 2026-09-23 independent adversarial audit (Claude Opus 4.6) that deprecated the cultural-VLM candidate and selected the conflict-verbalization topic. |
| [Final Four-Proposal Thesis Decision Audit.md](<Decision_Audits/Final Four-Proposal Thesis Decision Audit.md>) | Evidence verification and decision-readiness comparison of all four proposals. |
| [Clean Explanation (All 4 Idea).md](<Decision_Audits/Clean Explanation (All 4 Idea).md>) | Plain-English explanation of the four-proposal audit; warns it is a decision audit, not validation. |
| [FINAL THESIS DECISION AUDIT.md](<Decision_Audits/FINAL THESIS DECISION AUDIT.md>) | Agent transcript of an earlier decision audit across the `Cross Modal`, `Medical Imaging & FL`, `Multimodal Agent` folders. |
| [Cross_Modal_Discovery_Synthesis_and_Handover (MA & MVLM).md](<Decision_Audits/Cross_Modal_Discovery_Synthesis_and_Handover (MA & MVLM).md>) | 2026-09-20 synthesis of AlphaXiv/Gemini/Perplexity/Claude discovery reports; handover spec. |
| [Canonical Thesis Topic Related Paper.md.md](<Decision_Audits/Canonical Thesis Topic Related Paper.md.md>) | Chat transcript: feasibility autopsy of CLASH (2511.19199) and *Which Source Wins?* (2608.17205). |
| [Proposed Idea Related Paper.md](<Decision_Audits/Proposed Idea Related Paper.md>) | Paper autopsies for backup candidates (RH-Bench etc.). Duplicate of `Archive/Extra Field Exploration/Phase 3/Paper Autopsys.md`. |
| [Medical Imaging & FL.md](<Decision_Audits/Medical Imaging & FL.md>) | Agent transcript auditing the medical imaging / federated learning reports. |
| [Multimodal Agent.md](<Decision_Audits/Multimodal Agent.md>) | Adversarial audit of the multimodal-agent active-perception gap (found occupied). |
| [Structural Taxonomy Mind Map & Plain-English Explanations.md](<Decision_Audits/Structural Taxonomy Mind Map & Plain-English Explanations.md>) | Where each candidate sits in the multimodal-AI taxonomy, with lay explanations. Handy for the thesis introduction. |

---

## `Parked_Proposals/` — alternatives not pursued

Full index with anchors, kill conditions and why each was parked: [Parked_Proposals/README.md](Parked_Proposals/README.md).

| File | Proposal |
|---|---|
| [Canonical_Proposal_1_Reasoning_Trace_Degradation.md](Parked_Proposals/Canonical_Proposal_1_Reasoning_Trace_Degradation.md) | Field A: reasoning-trace degradation vs. positional/attention dilution (anchors RH-Bench, *Seeing or Knowing?*). |
| [Canonical_Proposal_2_Binding_IDs_Natural_Transfer.md](Parked_Proposals/Canonical_Proposal_2_Binding_IDs_Natural_Transfer.md) | Field C: do visual binding IDs transfer from synthetic grids to natural images? |
| [Canonical_Proposal_3_Cultural_Multimodal_Causal_Steering.md](Parked_Proposals/Canonical_Proposal_3_Cultural_Multimodal_Causal_Steering.md) | Field D (mechanistic): bottleneck localization + activation steering in low-resource cultural VLMs. |
| [Canonical_Proposal_3_Cultural_VLM_Modality_Decoupling.md](Parked_Proposals/Canonical_Proposal_3_Cultural_VLM_Modality_Decoupling.md) | Field D (diagnostic): placebo-controlled cultural-prior dominance and selective prediction. |

Copies of both Proposal 3 files also sit in `Archive/Bengali VLM/`. Per AGENTS.md §3.5, **do not reopen these without new primary evidence.**

