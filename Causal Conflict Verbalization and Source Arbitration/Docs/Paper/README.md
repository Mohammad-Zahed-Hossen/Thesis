# Docs/Paper — Primary Sources & Literature Audits

Downloaded primary papers (arXiv PDFs) and the two audited literature documents that ground the pre-registration [../PREREGISTRATION_VERDICT_TRANSPLANT.md](../PREREGISTRATION_VERDICT_TRANSPLANT.md).

**Trust level:** PDFs are **primary sources** (highest trust for literature claims). The two `.md` audits are AI-prepared but quote page-cited text; re-check any quote against the PDF before putting it in the thesis.
**Moved:** This folder was `Archive/Paper/` until commit `7fd3219`. Older files (`AGENTS.md`, `Docs/Decision_Audits/Idea.md`, the dossier itself) may still say `Archive/Paper/…` — read that as `Docs/Paper/…`.

> **Token tip for agents:** Don't open the PDFs (1–23 MB each). Read the dossier §1 matrix or the freeze-audit §1 autopsies first; open a PDF only to verify a specific page-cited quote.

---

## Layout

```
Docs/Paper/
├── README.md                              This file
├── lit-dossier-verdict-transplant/        Literature dossier (10 core papers + 4 discovered)
│   ├── lit-dossier-verdict-transplant.md
│   └── figures/                           4 PNG crops from cited papers
├── prereg-freeze-audit/                   Freeze-readiness audit of the pre-registration
│   ├── prereg-freeze-audit.md
│   └── figures/                           3 PNG crops from cited papers
├── <14 arXiv PDFs>                        The "fourteen sources read" (see table)
└── Archive/                               Old-topic papers and peer theses — NOT cited by v5
```

---

## Audit documents (read these first)

| File | Date | What it is | Key sections |
|---|---|---|---|
| [lit-dossier-verdict-transplant.md](lit-dossier-verdict-transplant/lit-dossier-verdict-transplant.md) | 2026-11-10 | Evidence base for the verdict-transplant design. Read depth per paper, corrections to mis-titled IDs, evidence matrix, mechanistic "saying vs. choosing" deep dive, countermeasures, novelty boundary. | §0 scope & title corrections · §1 evidence matrix · §2 mechanistic deep dive · §3 countermeasure architecture · §4 framing & novelty boundary (**§4.1 = "first" claim limit, per AGENTS.md**) · §5 reviewer objections |
| [prereg-freeze-audit.md](prereg-freeze-audit/prereg-freeze-audit.md) | 2026-11-10 | Audit of the pre-registration draft. **Verdict: red light — do not tag `prereg-v5` yet.** Autopsies of the 4 discovered papers, dev-data implications, resolved decisions R1–R8, missing literal templates, replacement novelty claim. | §1 paper autopsies · §2 dev data · §10 resolved decisions (2026-11-10) · §4 missing templates · §5 novelty claim (replaces dossier §4.1) · §6 smaller corrections |

---

## The fourteen primary sources (PDFs)

"Read depth" is from dossier §0 / freeze-audit §1. Titles are as verified there — several IDs were mis-titled in the original brief.

| arXiv ID | Short name | Why it matters to the thesis | Read depth |
|---|---|---|---|
| [2608.17205](2608.17205.pdf) | *Which Source Wins?* | **Source of both stimulus sets** (GSM8K/SVAMP image-of-one-problem conflict; ChartQA-Conflict). Must be cited. | Abstract + targeted (freeze audit §1.4) |
| [2610.33841](2610.33841.pdf) | *Grounding on Request: Learning Modality Control in VLMs* | Closest to the binding arm: can a user control which modality a VLM follows? Strong control comes from trained components, not prompting. Novelty boundary R1. | Freeze audit §1.1 |
| [2610.19407](2610.19407.pdf) | *VLMs Integrate Conflicting Evidence Like Biased Bayesian Observers* (Barua et al.) | Includes Qwen2.5-VL-3B; log-likelihood margin outcome; text evidence 1.4–2.7× stronger. Main reason Δℓ is primary and stratified by baseline margin. | Freeze audit §1.2 |
| [2609.06704](2609.06704.pdf) | *Counterfactual Tests for CoT Faithfulness in VLMs* | Edits the image, not the CoT; no equivalence bound; binary scores saturate. | Freeze audit §1.3 |
| [2609.26986](2609.26986.pdf) | *Noncommutativity* | Evidence-order effect: attachment last raises matching answers +9.8 to +28.1 pp; Qwen2.5-VL-3B +16.7 (GQA) / +15.0 (VQAv2) → **invariant 1: counterbalanced order**. | pp. 1–5 full |
| [2610.38296](2610.38296.pdf) | *Hidden Commitment* (ICML 2026) | Text-only (Qwen 0.8B, Gemma 3 1B); "surfacing" and "source choice" read at different layers/positions. Does **not** prove decoupled circuits. | pp. 1–7 full |
| [2607.27304](2607.27304.pdf) | *Position, Not Provenance* (CoT-Mediate; Bhowal et al., ICVGIP 2026) | Prompt-string-level prefix forcing in medical VLMs; paraphrase floors 0.5–3.3% → equivalence margin. | pp. 1–6 full |
| [2604.14888](2604.14888.pdf) | Sánchez Villegas et al. (COLM 2026) | Answer inertia across 18 VLMs incl. Qwen2.5-VL-3B; hint/monitorability parts use 7B/32B only. | pp. 1–9 + p. 20 |
| [2511.02243](2511.02243.pdf) | *When Modalities Conflict* (Zhang et al.) | Unimodal uncertainty governs preference; balance points; competency conditioning precedent. Models are 7B, not 3B. | pp. 1–8 full |
| [2503.02199](2503.02199.pdf) | *Words or Vision* (Deng et al., CVPR 2025) | "Blind faith in text" across 10 VLMs. | Targeted pp. 1–2, 4–7 |
| [2504.08974](2504.08974.pdf) | *Mixed Signals* | Modality bias on five conflict datasets; "Verbalized/CoT/Decomposed" are mitigation prompts. | Abstract + pp. 1–4, 7 |
| [2602.14518](2602.14518.pdf) | *Diagnosing Knowledge Conflict in Multimodal Long-Chain Reasoning* (Tang et al.) | Probing/steering 7B/11B reasoning models. | Abstract + pp. 2, 7–8, 17, 19 |
| [2606.28273](2606.28273.pdf) | *Vision-Default, Prior-Override* (Lietzow et al.) | Perception vs. parametric knowledge (not image vs. text); activation patching. | Abstract + p. 2 |
| [2505.23945](2505.23945.pdf) | *A Closer Look at Bias and CoT Faithfulness of Large (Vision) Language Models* (Balasubramanian et al.) | Whether CoTs articulate biasing cues; not source arbitration. | Abstract + pp. 2, 5 |

**Not found:** "CMC-Bench" (searched; never cited — dossier §0).

---

## `Archive/` — not part of the v5 evidence base

Papers from earlier, abandoned topics (calibration / selective prediction / hallucination) and peer theses kept as formatting references. Do not cite these for v5 claims without re-checking relevance.

| Item | Content |
|---|---|
| `Causal_Source_Arbitration_VLM_Literature_Review.md/.pdf` | Old v3-era "30+ paper" review (4-arm factorial, placebo design). **Superseded** by the dossier. |
| `CLASH - A Benchmark for Cross-Modal Contradiction Detection.pdf` | arXiv:2511.19199; contradiction-detection benchmark from topic selection. |
| `C3PO - …Omnimodal Models.pdf` | Cross-modal composition/counterfactual benchmark. |
| `13_Do_VLMs_See_What_Blind_User_Show_Them.md/.pdf` | VizWiz distribution-shift audit. |
| `Look Again Before You Abstain.pdf`, `Towards Statistical Factuality Guarantee for LVLMs.pdf`, `Unveiling Uncertainty … MLLM.pdf` | Abstention / calibration papers (old Bangla selective-prediction topic). |
| `Attention is all you need.pdf` | Background. |
| `15 Paper/` | Calibration & hallucination classics with `.md` text extractions (POPE object hallucination, Guo et al. calibration, selective classification, statistical factuality, MLLM uncertainty), plus `Paper.pdf` (unlabelled) and `Trustworthy_MLLM_Precise_Problem_Research_Report.docx`. |
| `Abrar-s-Thesis-Paper/` + `Abrar's Thesis Paper.pdf` | Peer undergraduate theses (Abrar Jawad: Bangla telephonic synthetic data; Shariful Islam: mixed-precision QAT on medical imaging) with `.md` extractions, `assets/` figures, and an AI digest `Thesis_Complete_Reference_Report.md`. Useful only as **thesis format/structure examples**. |
