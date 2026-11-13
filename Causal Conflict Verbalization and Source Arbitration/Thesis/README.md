# Thesis

Writing guides, conceptual FAQs, execution runbooks, compute evaluations, and v5 dev-pass audits for the BSc CSE thesis (*Does the Verdict Decide? Testing Whether Stated Source Reliability Steers Vision-Language Models under Image–Text Conflict*).

**Last updated:** 2026-11-13
**Status:** The v5 dev pass has run on all three models (39 files in [../Experiment/results_v5/](../Experiment/results_v5/)) and has been audited twice (`docs/Archive/`). The pre-registration is **not frozen**, and **no confirmatory data exists**. No dissertation chapters have been drafted here yet.
**Ground truth:** Active code and raw outputs live in [../Experiment/](../Experiment/) (start at [../Experiment/README.md](../Experiment/README.md)). The pre-registration draft is [../Docs/PREREGISTRATION_VERDICT_TRANSPLANT.md](../Docs/PREREGISTRATION_VERDICT_TRANSPLANT.md).

> [!NOTE]
> See [../Experiment/README.md](../Experiment/README.md) and [../AGENTS.md](../AGENTS.md) for current v5 dev-pass status and pre-freeze decisions.

---

## Quick start for AI agents (read in this order, stop when you have enough)

1. **This file**: what is in `Thesis/`.
2. [docs/Archive/claude_v5_independent_deep_audit.md](docs/Archive/claude_v5_independent_deep_audit.md) §1 and §10: the current evidence boundary and the blockers before freezing.
3. [../Docs/PREREGISTRATION_VERDICT_TRANSPLANT.md](../Docs/PREREGISTRATION_VERDICT_TRANSPLANT.md): the design spec (freeze conditions §10, R8).
4. [../Docs/Paper/README.md](../Docs/Paper/README.md): the 14 primary sources, the literature dossier and the freeze audit.
5. [THESIS_NARRATIVE_AND_FRAMING_GUIDE.md](THESIS_NARRATIVE_AND_FRAMING_GUIDE.md): only when you are drafting thesis prose.

Folder indexes elsewhere: [../Docs/README.md](../Docs/README.md) · [../Docs/Context/README.md](../Docs/Context/README.md) · [../Archive/README.md](../Archive/README.md) · [../Experiment/README.md](../Experiment/README.md).

---

## Layout

```
Thesis/
├── README.md                                  This file
├── THESIS_NARRATIVE_AND_FRAMING_GUIDE.md      Chapter-by-chapter framing & defense phrasing guide
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
        ├── v5_dev_output.md
        ├── v5_antigravity_analysis.md
        ├── v5_dev_evidence_audit.md
        └── claude_v5_independent_deep_audit.md
```

---

## Contents

### Top-Level Writing Guide

- **[THESIS_NARRATIVE_AND_FRAMING_GUIDE.md](THESIS_NARRATIVE_AND_FRAMING_GUIDE.md)** — Permanent writing and defense guide for framing the methodological arc from exploratory v1/v3 pilots to the v5 prefix-forcing design, covering chapter roles (Introduction, Methodological Critique, Prefix-Forcing Paradigm), claim boundaries, and the three-model scope (`Qwen2-VL-2B-Instruct`, `Qwen2.5-VL-3B-Instruct`, `Qwen2.5-VL-7B-Instruct`).

### `docs/Understanding/` — Conceptual & Defense References

Two harmonized Q&A guides (AI-generated and audited on 2026-11-11 against code, `results_v4/dev2_*.jsonl`, the pre-registration draft, and primary papers) explaining the Controlled Direct Effect (CDE) estimand, datasets, pilot-to-v5 evolution, open risks, and defense preparation:

- **[Thesis Understanding FAQ (Opus 4.6).md](<docs/Understanding/Thesis Understanding FAQ (Opus 4.6).md>)** — Compact, citation-dense reference.
- **[Thesis Understanding FAQ (Gemini 3.8 Flash).md](<docs/Understanding/Thesis Understanding FAQ (Gemini 3.8 Flash).md>)** — Longer teaching-style companion.

### `docs/RUNBOOK/` — Thesis-Side Execution Guides

- **[RUNBOOK_V4.md](docs/RUNBOOK/RUNBOOK_V4.md)** — End-to-end local and GPU execution guide for v4 (mirrors/extends [../Experiment/RUNBOOK_v4.md](../Experiment/RUNBOOK_v4.md)).
- **[RUNBOOK_V5.md](docs/RUNBOOK/RUNBOOK_V5.md)** — Colab Pro guide for the v5 dev pass. **Note:** Audits in `docs/Archive/` flag discrepancies between this file and [../Experiment/RUNBOOK_v5.md](../Experiment/RUNBOOK_v5.md) (for example, missing ChartQA render checks and omitted `--base` / `--donor` flags in the local `analyze_v5.py` command); defer to the `Experiment/` runbook.

### `docs/Compute/` — GPU Infrastructure Evaluations

- **[Compute_Platform_Evaluation_2026-11-11.md](docs/Compute/Compute_Platform_Evaluation_2026-11-11.md)** — Current evaluation on a \$10–15/month budget recommending Colab Pro / PAYG (L4 pinned) with RunPod Community Cloud as backup, and flagging the L4's ~22.5 GB VRAM vs. the pre-registration's "24 GB" wording. Replaces the earlier report below.
- **[Thesis Cloude Compute Evaluation.md](docs/Compute/Thesis%20Cloude%20Compute%20Evaluation.md)** — Earlier compute evaluation (superseded; assumed a \$50/month budget).

### `docs/Archive/` — v5 Dev-Pass Logs & Audits (Dev Only)

Records and independent AI audits of the v5 development run stored in [../Experiment/results_v5/](../Experiment/results_v5/) (39 artifacts, 29,880 rows). **Every number in these files comes from spent dev items; none are confirmatory findings.**

- **[v5_dev_output.md](docs/Archive/v5_dev_output.md)** — Raw Colab notebook command/output transcript from the v5 dev run.
- **[v5_antigravity_analysis.md](docs/Archive/v5_antigravity_analysis.md)** — File-by-file inventory and analysis of `results_v5/` and environment versions.
- **[v5_dev_evidence_audit.md](docs/Archive/v5_dev_evidence_audit.md)** — Evidence audit checking row integrity, provenance gaps, runbook discrepancies, and dev-only interpretation boundaries.
- **[claude_v5_independent_deep_audit.md](docs/Archive/claude_v5_independent_deep_audit.md)** — Second-pass independent forensic audit (2026-11-13) cross-checking `results_v5/`, active v5 code, ChartQA Hub gold answers, `Δℓ` vs. behavior coupling, own-verdict replay stability, and pre-freeze feasibility blockers (2B `####` format failure, ChartQA retention, and behavioral churn).

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

