# Archive — Parked Explorations & Superseded Material

Everything the project explored and set aside: rival thesis fields, early experiment outputs under the old v3-era framing, superseded manuscript drafts, study plans, and research-method playbooks.

**Trust level (per [../AGENTS.md](../AGENTS.md) §2):** Historical. Nothing here is active. Nearly all files are AI-generated reports or raw chat/agent transcripts. **Do not reopen a parked field without new primary evidence** (AGENTS.md §3.5).
**Decision summaries** for these explorations live in [../Docs/Context/Canonical_Rejected_and_Parked_Thesis_Fields_Report.md](../Docs/Context/Canonical_Rejected_and_Parked_Thesis_Fields_Report.md) and [../Docs/Decision_Audits/](../Docs/Decision_Audits/). Read those before opening anything here.
**Primary papers** are no longer here: `Archive/Paper/` moved to [../Docs/Paper/](../Docs/Paper/README.md) (commit `7fd3219`).

> **Token tip for agents:** Files here are large (often 50–275 KB) and repetitive (several are multiple AI drafts of the same report). Use this README to pick one file; never bulk-read a folder.

---

## Layout

```
Archive/
├── README.md                    This file
├── Bengali VLM/                 PARKED field: Bangla cultural VLM selective prediction / steering
├── Medical Imaging & FL/        PARKED field: medical imaging, federated learning (± VLM)
├── Multimodal Agent/            PARKED field: agent tool use & active perception (found occupied)
├── VLM/                         Cross-modal discovery reports that led to the current topic area
├── Extra Field Exploration/     Phase 1–3 landscape scans, backup candidates Q1/Q2, CPU pilot code
├── Experiment_History/          OLD v3-era N=500 production-run outputs & stats (truncated generations)
├── Thesis_Manuscript/           SUPERSEDED Ch. 1 & Ch. 3 drafts under the old framing
├── Knowledge/                   Study plans & free course maps
└── Research_Playbook/           Generic AI/ML research-method playbook (multiple AI drafts)
```

---

## Parked thesis fields

### `Bengali VLM/` — Evidence-grounded selective prediction for Bangla cultural VLMs
Candidate "Proposal 3". Deprecated 2026-09-23: the layer-18 bottleneck was an unverified assumption and the method was partly pre-empted (BabelSteering); BanglaProtha image-leakage and blank-image checks were decisive boundary tests.

| File | What it is |
|---|---|
| `Evidence-Grounded Selective Prediction for Reliable Bangla Cultural Vision-Language Models.md` | The original proposal (converted `.docx`). |
| `bangla-cultural-vlm-synthesis.md` | Cross-paper synthesis / 40+ paper literature map. |
| `Bangla Cultural VLM Thesis Audit.md` | Field-mapping report: finds the proposal conflates calibration, grounding and RAG. |
| `Adversarial literature autopsy.md` | Chat transcript: adversarial literature autopsy. |
| `Antigravity 2.0 — Decision-Grade Thesis Evidence Audit.md` | Decision audit; names the two boundary checks the decision hinges on. |
| `Final Boundary Verification (Antigravity).md`, `Final Boundary Verification- Candidate Proposal 3 (OpenResearch).md` | Agent transcripts running those boundary checks against BanglaProtha. |
| `Canonical_Proposal_3_Cultural_Multimodal_Causal_Steering.md`, `Canonical_Proposal_3_Cultural_VLM_Modality_Decoupling.md` | Two refined Proposal 3 variants (copies in `Docs/Parked_Proposals/`). |
| `Idea_First_Thesis_Research_and_Recommendation.md` | Early four-question ideation (newer copy in `Docs/Context/`). |

### `Medical Imaging & FL/` — Medical imaging and federated learning
Audited 2026-09-20 as reopen candidates; judged high-risk / crowded for an undergraduate thesis.

| File | What it is |
|---|---|
| `Adversarial Thesis Audit_ Medical Imaging vs Federated Learning.md` | Overall adversarial audit of both areas. |
| `Medical Imaging without VLM.md`, `Medical Imaging With VLM.md`, `Medical Imaging With & Without VLM.md` | Discovery audits per variant (the last is a chat transcript). |
| `Federated Learning (non-VLM).md`, `Federated Learning + Medical Vision-Language Models (VLM variant).md` | Reopen audits; verdict for non-VLM FL was "time-boxed gated pilot" only. |

### `Multimodal Agent/` — Tool use & active perception
Found **occupied** (AdaTooler-V, VTool-R1, Thyme, MED, NTEP-R, etc.).

| File | What it is |
|---|---|
| `Adversarial Audit_ Multimodal Agent Tool Use & Active Perception Thesis Gap.md` | Final adversarial audit and verdict. |
| `AlphaxiV Report.md`, `OpenResearch Report.md` | Tool-specific discovery transcripts. |
| `Perflexity Source Finder.md` | Discovery table of 2025–2026 agent papers (code/data availability, baselines). |

---

## Discovery history toward the current topic

### `VLM/` — Cross-modal evidence use & source arbitration discovery (≈ 2026-09-20)
The reports that narrowed the field to image–text conflict and source arbitration.

| File | What it is |
|---|---|
| `Canonical_Cross_Modal_Thesis_Synthesis.md` | Consolidated synthesis of all discovery streams. **Start here** for this folder. |
| `Claude Critique Analysis.md` | Methodology critique: "arbitration accuracy" doesn't exist on the recommended data; nothing cleared PROCEED TO PILOT. Important corrective. |
| `Cross-Modal AI Thesis Discovery (Gemini).md` | Gemini adversarial discovery audit. |
| `Cross-modal evidence use and source arbitration.md`, `… (Perflexity).md`, `kill occupied questions (Perflexity).md` | Research-question trees and occupancy kills (the two Perplexity files share most content). |
| `find missing research (Gemini).md` | Terminology mapping to find hidden prior work. |

### `Extra Field Exploration/` — Phase 1–3 landscape scans and backup candidates
Broad VLM/MLLM landscape scans, then a kill-gate for two backup questions: **Q1** reasoning-trace length vs. visual evidence use, **Q2** binding-ID universality. Neither survived.

| File | What it is |
|---|---|
| `Plan.md` | Agent transcript planning the exploration phases. |
| `phase-1---landscape-map---antithesis-scan-turn-1.md`, `VLM Landscape and Adversarial Antithesis Scan.md`, `VLM MLLM Antithesis Scan.md` | Phase 1 landscape & antithesis scans. |
| `phase2-report.md`, `Phase2 AlphaXiV Report.md`, `Multimodal AI Thesis Feasibility Audit (Phase 2).md` | Phase 2 gap autopsies for Q1/Q2. |
| `Adversarial literature autopsy.pdf`, `Bangla Cultural VLM Thesis Audit.pdf` | PDF exports of the Bengali VLM reports. |
| `Phase 3/phase3-report.md` | Phase 3 kill-gate report. |
| `Phase 3/preregistration.md` | Q1/Q2 pilot pre-registration (locked before results). |
| `Phase 3/Adversarial Kill Gate Evidence Audit.md`, `Phase 3/Paper Autopsys.md` | Evidence audit and paper autopsies (RH-Bench etc.). |
| `Phase 3/pilot_harness.py`, `Phase 3/pilot_run.py` | CPU pre-flight pilot code for Q1/Q2. Not part of the active pipeline. |
| `Phase 3/thesis-openresearch.md` | OpenResearch session export. |

---

## Superseded experiment & manuscript material

### `Experiment_History/` — v3-era production run, N = 500 (2026-09-23)
Qwen2.5-VL-3B, V100 `float16`, first 500 clean-image items, 4-arm factorial (placebo / neutral / conflict / prefill). **Generations are heavily truncated** (`max_new_tokens` 15/90), so exact-match metrics are void. The "conflict verbalization breaks visual capture" reading was later withdrawn: the arms differ in **instruction**, not verbalization. Current re-analysis of v3 is in [../Experiment/results_v3/](../Experiment/results_v3/README.md); the harness is in [../Experiment/archive/](../Experiment/archive/README.md).

| File | What it is |
|---|---|
| `experiment_results_analysis.md` | AI analysis of the run (includes the truncation warning). |
| `statistical_report.md`, `statistical_report v2.0.md` | Hypothesis-test summaries (near-identical). |
| `thesis_contingency_table.tex`, `… v2.0.tex` | LaTeX contingency tables. |
| `experiment_checkpoint.csv` (203 KB), `full_experiment_results.json` (942 KB) | Raw outputs. Don't load into context; inspect with scripts if needed. |

### `Thesis_Manuscript/` — superseded chapter drafts
`Chapter_1_Introduction.md` and `Chapter_3_Methodology.md` were written for the old claim that conflict verbalization causally steers arbitration (N = 1,619 census, single model, paired 4-arm design). **Do not reuse their claims.** Reuse only background prose after checking it against [../Thesis/THESIS_NARRATIVE_AND_FRAMING_GUIDE.md](../Thesis/THESIS_NARRATIVE_AND_FRAMING_GUIDE.md).

---

## Learning & method resources

### `Knowledge/` — study plans and course maps

| File | What it is |
|---|---|
| `30-Day Thesis Understanding & Defense Plan.md` | Plan to pay down "knowledge debt": Transformer → VLM → Qwen2.5-VL → experiment → causal inference → stats → defense. Still broadly useful; experiment details are v3-era. |
| `Thesis Knowledge Acquisition — Complete Course & Resource Map.md` | Free-course map aligned to the thesis topic. |
| `Canonical AI_ML & Multimodal Course Explorer.md` | Stanford/MIT/Harvard free course catalogue. |
| `Archieve/` | Older plans: two 30-day VLM/MLLM foundation plans, a Stanford/MIT/Harvard course list, and a YouTube Custom Feeds manual. |

### `Research_Playbook/` — generic AI/ML research-method playbook
Not thesis-specific. A reusable manual (gap discovery → question → experiment → thesis → paper), drawn from this project's journey.

| Item | What it is |
|---|---|
| `Canonical_AI_ML_Research_Playbook.md` (229 KB) | Full canonical version. |
| `Canonical_AI_ML_Research_Playbook (Consolidate).md` (52 KB) | Shorter consolidated version. **Read this one** if you need the playbook at all. |
| `Parked/` | Seven alternative drafts by different AI tools (Gemini, OpenResearch, Antigravity ×2, Claude, Cline ×2). |
| `_source_parts/` | The Cline 2026-09-27 playbook split into ~38 numbered section files, with its own [README.md](Research_Playbook/_source_parts/README.md), `_MANIFEST.md` (ordering rule) and `_rebuild_playbook.py` (reassembles them). `_superseded/` holds a duplicate part. |

