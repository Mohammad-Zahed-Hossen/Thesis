# Docs/Context — Project Context & Master Technical Audit

This folder contains two tiers of contextual documentation:

1. **Primary Contextual & Technical Audit Reference (Nov 2026 — Highest Priority):**
   - **[End-to-End Technical & Scientific Audit.md](<End-to-End Technical & Scientific Audit.md>)** (`2026-11-13`): Comprehensive, bottom-up multi-agent verification of the entire codebase (`Experiment/*.py`, `Experiment/tests/`), stored datasets (`results_v5/`, `results_v4/`, `results_v3/`), pre-registration specification ([../PREREGISTRATION_VERDICT_TRANSPLANT.md](../PREREGISTRATION_VERDICT_TRANSPLANT.md)), runbooks, and `Thesis/` docs. **Prioritize this report (immediately after actual ground-truth data and active code, and over all other AI-generated files)** for project state, code bugs, pre-freeze blockers, and the step-by-step roadmap to completion.
2. **Historical Project Context (Sept 2026 — Reference Only):**
   - Background documents written during topic discovery and immediately after the v3 pilot (≈ 14–24 September 2026). They explain **how the project got here**: the frozen parent field, which research fields were ranked, parked or rejected, and the original topic lock.

> [!IMPORTANT]
> **Trust Hierarchy for `Docs/Context/`:**
> - **[End-to-End Technical & Scientific Audit.md](<End-to-End Technical & Scientific Audit.md>)** (`2026-11-13`) is verified directly against Tier 1–3 ground truth (`Experiment/results_v5/`, `Experiment/*.py`, `Docs/PREREGISTRATION_VERDICT_TRANSPLANT.md`) and supersedes older AI summaries and READMEs where they conflict.
> - **All September 2026 files below are historical reference only** and contain claims that later audits withdrew (e.g., stating the topic is "frozen & empirically validated" on $N = 1,619$ with $\Delta_{\text{arb}} = +63.74\text{ pp}$, $p = 1.2 \times 10^{-215}$, and that verbalization *causally* steers arbitration). That v3 contrast compared two **instructions**, not verbalizations (see [../../Experiment/results_v3/README.md](../../Experiment/results_v3/README.md)). The current design is the verdict transplant in [../PREREGISTRATION_VERDICT_TRANSPLANT.md](../PREREGISTRATION_VERDICT_TRANSPLANT.md), and **no confirmatory data exists**. The old title "Causal Conflict Verbalization and Source Arbitration in VLMs" has been replaced by *Does the Verdict Decide?*.

> **Token tip for agents:** For current project state, code/spec discrepancies, and next steps, read **[End-to-End Technical & Scientific Audit.md](<End-to-End Technical & Scientific Audit.md>)**, [../../Experiment/README.md](../../Experiment/README.md), and [../../Thesis/README.md](../../Thesis/README.md). Open the large September 2026 files (up to 174 KB) only to answer "why was field X rejected?" or "what did the project look like in September?".

---

## Files

| File | Size | Date | What it contains | Still useful for |
|---|---|---|---|---|
| **[End-to-End Technical & Scientific Audit.md](<End-to-End Technical & Scientific Audit.md>)** | **44 KB** | **2026-11-13** | **Independent end-to-end technical & scientific audit** across `results_v5/` (29,880 rows), `results_v4/`, `results_v3/`, `Experiment/*.py`, `Experiment/tests/` (196 tests), `PREREGISTRATION_VERDICT_TRANSPLANT.md`, runbooks, and `Thesis/docs/Archive/`. Documents 5 pre-freeze blockers, 7 code/pipeline bugs, consistency matrix, verified cell-level tables, and a 4-phase action plan. | **Primary contextual reference** (prioritize alongside ground-truth data/code and over all other AI-generated files). |
| [Canonical Thesis Field Specification.md](<Canonical Thesis Field Specification.md>) | 72 KB | Sept 2026 (v2.0) | Converted `.docx`. Defines the **frozen parent field** (Multimodal / Vision-Language Learning and Systems) and three ranked research fields while topic discovery was still open. | Parent-field definition and the original field ranking. |
| [Canonical_Context.md](Canonical_Context.md) | 54 KB | updated 2026-09-24 | "Research operating system": researcher profile, hardware, frozen field, locked topic, v3 census results, operating rules. | Researcher/hardware background. **Results section is stale** (see warning). |
| [Canonical_Rejected_and_Parked_Thesis_Fields_Report.md](Canonical_Rejected_and_Parked_Thesis_Fields_Report.md) | 174 KB | Sept 2026 | Converted `.docx`. Long-term decision record of every rejected/parked field (Bengali cultural VLM, medical imaging, federated learning, multimodal agents, reasoning-trace degradation, binding IDs, …) and why. | The authoritative "why not X?" record. Pairs with [../../Archive/](../../Archive/) (raw evidence) and [../Parked_Proposals/](../Parked_Proposals/). |
| [Idea_First_Thesis_Research_and_Recommendation.md](Idea_First_Thesis_Research_and_Recommendation.md) | 27 KB | 2026-09-16, marked superseded 09-24 | Early ideation: four candidate research questions (cultural VLM repair recommended at the time). Banner marks it **historical, superseded & resolved**. Earlier copy in `Archive/Bengali VLM/`. | Origin of the candidate list. |
| [Thesis_Progress_and_Research_Map.md](Thesis_Progress_and_Research_Map.md) | 51 KB | through 2026-09-14, updated 09-24 | Narrative timeline from choosing VLM/MLLM to topic lock, consolidated from eleven documents. | Chronology for the thesis "research journey" / methodology-evolution narrative. |
| [Thesis_Topic_Discovery_Handover.md](Thesis_Topic_Discovery_Handover.md) | 7 KB | 2026-09-24 | Post-freeze handover telling agents how to proceed to execution and manuscript drafting under the old topic. | Shortest summary of the September state. Its execution plan is obsolete. |

---

## Related folders

- [../Decision_Audits/](../Decision_Audits/) — the adversarial audits that produced these decisions.
- [../Parked_Proposals/](../Parked_Proposals/) — full proposals for the parked alternatives.
- [../../Archive/](../../Archive/) — raw exploration reports per parked domain.
- [../../Thesis/THESIS_NARRATIVE_AND_FRAMING_GUIDE.md](../../Thesis/THESIS_NARRATIVE_AND_FRAMING_GUIDE.md) — how to present this history honestly in the thesis.

