# Thesis

Writing guides, conceptual FAQs, execution runbooks, compute evaluations, and v5 dev-pass audits for the BSc CSE thesis (*Does the Verdict Decide? Testing Whether Stated Source Reliability Steers Vision-Language Models under Image–Text Conflict*).

**Last updated:** 2026-11-15
**Status:** The v5 dev pass has run on all three models (39 root files in [../Experiment/results_v5/](../Experiment/results_v5/) + `analysis_dev/`) and `analyze_v5.py` has been run after pre-freeze decisions D1–D5 and the 2026-11-14 gate updates ([../Experiment/results_v5/analysis_dev/](../Experiment/results_v5/analysis_dev/)). All **248** CPU unit tests pass (`Experiment/tests/`) and `Experiment/preflight_v5.py` (`8/8` scripts) passes cleanly after Fable 5.2 forensic fixes (`F2`, `F3`, `F5`–`F13`, `Upgrades 1–5`). The 18-paper + CMC-Bench literature base is consolidated in [../Docs/Paper/THESIS_LITERATURE_KNOWLEDGE_BASE.md](../Docs/Paper/THESIS_LITERATURE_KNOWLEDGE_BASE.md), alongside the 2026-11-15 literature audit and Fable 5.2 forensic audit + 16 related-work repo snapshots. The pre-registration is **not frozen**, and **no confirmatory data exists**. No dissertation chapters have been drafted here yet.
**Ground truth:** Active code and raw outputs live in [../Experiment/](../Experiment/) (start at [../Experiment/README.md](../Experiment/README.md)). The pre-registration draft is [../Docs/PREREGISTRATION_VERDICT_TRANSPLANT.md](../Docs/PREREGISTRATION_VERDICT_TRANSPLANT.md).

> [!NOTE]
> See [../Experiment/README.md](../Experiment/README.md) and [../AGENTS.md](../AGENTS.md) for current v5 dev-pass status and pre-freeze decisions.

---

## Quick start for AI agents (read in this order, stop when you have enough)

1. **This file**: what is in `Thesis/`.
2. [docs/Archive/dev v5/claude_v5_independent_deep_audit.md](<docs/Archive/dev v5/claude_v5_independent_deep_audit.md>) §1 and §10: the current evidence boundary and the blockers before freezing.
3. [../Docs/PREREGISTRATION_VERDICT_TRANSPLANT.md](../Docs/PREREGISTRATION_VERDICT_TRANSPLANT.md): the design spec (freeze conditions §10, R8).
4. [../Docs/RESEARCH_OBJECTIVE.md](../Docs/RESEARCH_OBJECTIVE.md) and [../Docs/Paper/README.md](../Docs/Paper/README.md): the post-2026-11-15 onboarding brief, complete 18-paper + CMC-Bench knowledge base ([THESIS_LITERATURE_KNOWLEDGE_BASE.md](../Docs/Paper/THESIS_LITERATURE_KNOWLEDGE_BASE.md)), pre-freeze literature audit ([lit-audit-2026-11-15/](../Docs/Paper/lit-audit-2026-11-15/lit-audit-2026-11-15.md)), Fable 5.2 pre-freeze forensic audit ([fable52-prefreeze-audit-2026-11-15.md](../Docs/Paper/fable52-prefreeze-audit-2026-11-15.md)) + 16 snapshotted repos ([related_repos/](../Docs/Paper/related_repos/README.md)), post-v5 direct PDF audit ([post-v5-pdf-audit.md](../Docs/Paper/post-v5-pdf-audit/post-v5-pdf-audit.md)), and **29 local PDFs** (20 core/lead + 6 audit A-papers + 3 cited B-papers; 0 core missing).
5. [THESIS_NARRATIVE_AND_FRAMING_GUIDE.md](THESIS_NARRATIVE_AND_FRAMING_GUIDE.md): only when you are drafting thesis prose.

Folder indexes elsewhere: [../Docs/README.md](../Docs/README.md) · [../Docs/Context/README.md](../Docs/Context/README.md) · [../Archive/README.md](../Archive/README.md) · [../Experiment/README.md](../Experiment/README.md).

---

## Layout

```
Thesis/
├── README.md                                  This file
├── THESIS_NARRATIVE_AND_FRAMING_GUIDE.md      Chapter-by-chapter framing & defense phrasing guide
├── dev v1_v5.md                               2026-11-13 visual/narrative snapshot of v1–v5 (historical; pre-dates 2026-11-14 updates)
└── docs/
    ├── Understanding/
    │   ├── Thesis Understanding FAQ (Opus 4.6).md
    │   └── Thesis Understanding FAQ (Gemini 3.8 Flash).md
    ├── RUNBOOK/
    │   ├── RUNBOOK_V4.md
    │   └── RUNBOOK_V5.md
    ├── Compute/
    │   ├── Compute_Platform_Evaluation_2026-11-11.md
    │   └── Thesis Cloude Compute Evaluation.md
    └── Archive/
        └── dev v5/
            ├── v5_dev_output.md
            ├── v5_antigravity_analysis.md
            ├── v5_dev_evidence_audit.md
            ├── claude_v5_independent_deep_audit.md
            ├── claude_v5_forensic_code_and_construct_audit.md
            └── claude_v4_vs_v5_plan_audit.md
```

---

## Contents

### Top-Level Writing Guide

- **[THESIS_NARRATIVE_AND_FRAMING_GUIDE.md](THESIS_NARRATIVE_AND_FRAMING_GUIDE.md)** — Permanent writing and defense guide for framing the methodological arc from exploratory v1/v3 pilots to the v5 prefix-forcing design, covering chapter roles (Introduction, Methodological Critique, Prefix-Forcing Paradigm), claim boundaries, and the three-model scope (`Qwen2-VL-2B-Instruct` diagnostic-only per D3; `Qwen2.5-VL-3B-Instruct` and `Qwen2.5-VL-7B-Instruct` confirmatory).
- **[dev v1_v5.md](<dev v1_v5.md>)** — Plain-English narrative walkthrough of the v1–v5 evolution and the five v5 dev-pass findings as of `2026-11-13` (prior to the 2026-11-14 `02eeca9`/`157c694` gate and literature updates; some links point to pre-reorganization paths).

### `docs/Understanding/` — Conceptual & Defense References

Two harmonized Q&A guides (AI-generated and audited on 2026-11-11 against code, `results_v4/dev2_*.jsonl`, the pre-registration draft, and primary papers) explaining the Controlled Direct Effect (CDE) estimand, datasets, pilot-to-v5 evolution, open risks, and defense preparation:

- **[Thesis Understanding FAQ (Opus 4.6).md](<docs/Understanding/Thesis Understanding FAQ (Opus 4.6).md>)** — Compact, citation-dense reference.
- **[Thesis Understanding FAQ (Gemini 3.8 Flash).md](<docs/Understanding/Thesis Understanding FAQ (Gemini 3.8 Flash).md>)** — Longer teaching-style companion.

### `docs/RUNBOOK/` — Thesis-Side Execution Guides

- **[RUNBOOK_V4.md](docs/RUNBOOK/RUNBOOK_V4.md)** — End-to-end local and GPU execution guide for v4 (mirrors/extends [../Experiment/RUNBOOK_v4.md](../Experiment/RUNBOOK_v4.md)).
- **[RUNBOOK_V5.md](docs/RUNBOOK/RUNBOOK_V5.md)** — Colab Pro guide for the v5 dev pass. **Note:** Audits in `docs/Archive/dev v5/` flag discrepancies between this file and [../Experiment/RUNBOOK_v5.md](../Experiment/RUNBOOK_v5.md) (for example, missing ChartQA render checks and omitted `--base` / `--donor` flags in the local `analyze_v5.py` command); defer to the `Experiment/` runbook.

### `docs/Compute/` — GPU Infrastructure Evaluations

- **[Compute_Platform_Evaluation_2026-11-11.md](docs/Compute/Compute_Platform_Evaluation_2026-11-11.md)** — Current evaluation on a \$10–15/month budget recommending Colab Pro / PAYG (L4 pinned) with RunPod Community Cloud as backup, and flagging the L4's ~22.5 GB VRAM vs. the pre-registration's earlier "24 GB" wording (subsequently updated to `≥ 22 GiB` / `L4 [23,034 MiB]` in `PREREGISTRATION_VERDICT_TRANSPLANT.md` §3.4). Replaces the earlier report below.
- **[Thesis Cloude Compute Evaluation.md](docs/Compute/Thesis%20Cloude%20Compute%20Evaluation.md)** — Earlier compute evaluation (superseded; assumed a \$50/month budget).

### `docs/Archive/dev v5/` — v5 Dev-Pass Logs & Audits (Dev Only)

Records and independent AI audits of the v5 development run stored in [../Experiment/results_v5/](../Experiment/results_v5/) (39 artifacts, 29,880 rows). **Every number in these files comes from spent dev items; none are confirmatory findings.**

- **[v5_dev_output.md](<docs/Archive/dev v5/v5_dev_output.md>)** — Raw Colab notebook command/output transcript from the v5 dev run.
- **[v5_antigravity_analysis.md](<docs/Archive/dev v5/v5_antigravity_analysis.md>)** — File-by-file inventory and analysis of `results_v5/` and environment versions.
- **[v5_dev_evidence_audit.md](<docs/Archive/dev v5/v5_dev_evidence_audit.md>)** — Evidence audit checking row integrity, provenance gaps, runbook discrepancies, and dev-only interpretation boundaries.
- **[claude_v5_independent_deep_audit.md](<docs/Archive/dev v5/claude_v5_independent_deep_audit.md>)** — Second-pass independent forensic audit (2026-11-13) cross-checking `results_v5/`, active v5 code, ChartQA Hub gold answers, `Δℓ` vs. behavior coupling, own-verdict replay stability, and pre-freeze feasibility blockers (2B `####` format failure, ChartQA retention, and behavioral churn).
- **[claude_v5_forensic_code_and_construct_audit.md](<docs/Archive/dev v5/claude_v5_forensic_code_and_construct_audit.md>)** — Forensic code & construct audit motivating pre-freeze decisions D1–D5 (2026-11-13).
- **[claude_v4_vs_v5_plan_audit.md](<docs/Archive/dev v5/claude_v4_vs_v5_plan_audit.md>)** — Objective comparison of the v4 dev plan vs. the post-v5 plan grounded in primary papers (2026-11-14), leading to the fixed 5% churn limit, `B_beh` benchmark renaming, and explicit inconclusive readings.

---

## Trust & Epistemic Rules

1. **Documents here are reference aids, not ground truth.** Always verify numbers, prompts, and implementation details against [../Experiment/](../Experiment/) (raw JSONL rows → manifests/gates → active Python code).
2. **Do not cite dev data as findings.** Figures in `docs/Understanding/` (v4 `dev2`) and `docs/Archive/` (v5 dev pass) are exploratory/diagnostic only.
3. **Preserve epistemic tags** (`[Verified]`, `[Inferred]`, `[Hypothesis]`, `[Unknown]`) when drafting thesis text from these references, per [../AGENTS.md](../AGENTS.md).
4. **Do not reuse the old chapter drafts.** [../Archive/Thesis_Manuscript/](../Archive/Thesis_Manuscript/) holds Chapter 1 and Chapter 3 written under the withdrawn v3 claim that verbalization causally steers arbitration (N = 1,619). New chapters go in this folder and follow the framing guide.
5. **Avoid the stale September documents.** The `CANONICAL_*` files and `Docs/Context/` present the v3 instruction contrast as validated causal proof. See [../Docs/README.md](../Docs/README.md) for which files are current.

---

## Where new work should go

| Artifact | Location |
|---|---|
| Dissertation chapter drafts | `Thesis/` (e.g. `Thesis/chapters/`, to be created) |
| Thesis-side runbooks, compute notes | `Thesis/docs/RUNBOOK/`, `Thesis/docs/Compute/` |
| New dev or confirmatory run audits | `Thesis/docs/Archive/`, or a dated subfolder |
| Code, raw results, analysis outputs | [../Experiment/](../Experiment/), never here |
| Literature PDFs and dossiers | [../Docs/Paper/](../Docs/Paper/) |

Update the **Layout** and **Contents** sections of this file whenever you add a file here.

