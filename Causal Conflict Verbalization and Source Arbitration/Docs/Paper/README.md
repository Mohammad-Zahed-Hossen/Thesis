# Docs/Paper — Primary Sources & Literature Audits

Downloaded primary papers (14 local PDFs) and audited literature syntheses grounding the pre-registration [../PREREGISTRATION_VERDICT_TRANSPLANT.md](../PREREGISTRATION_VERDICT_TRANSPLANT.md).

**Trust level:** PDFs are **primary sources** (highest trust for literature claims). All `.md` reports here are AI-prepared from primary PDFs and AlphaXiv reads; always verify any verbatim quote against the PDF before putting it in the dissertation.
**Moved:** This folder was `Archive/Paper/` until commit `7fd3219`. Older files (`Docs/Decision_Audits/Idea.md`, the 2026-11-10 dossier) may still say `Archive/Paper/…` — read that as `Docs/Paper/…`.

> **Token tip for agents:** Don't open raw PDFs (1–23 MB each) unless verifying a specific quote. Start at [THESIS_LITERATURE_KNOWLEDGE_BASE.md](THESIS_LITERATURE_KNOWLEDGE_BASE.md) for all 18 core papers + CMC-Bench.

---

## Layout

```
Docs/Paper/
├── README.md                              This file
├── THESIS_LITERATURE_KNOWLEDGE_BASE.md    ★ Complete 18-paper + CMC-Bench dossier (start here)
├── lit-dossier-verdict-transplant/        Original 10+4 dossier (2026-11-10) + 4 PNG figure crops
├── prereg-freeze-audit/                   Pre-registration freeze audit (2026-11-10) + 3 PNG figure crops
├── <14 local arXiv PDFs>                  Present locally (see §1)
└── Archive/                               Old-topic papers and peer theses — NOT cited by v5
```

---

## Audit & Knowledge Documents

| File | Date | What it is | Key sections |
|---|---|---|---|
| [THESIS_LITERATURE_KNOWLEDGE_BASE.md](THESIS_LITERATURE_KNOWLEDGE_BASE.md) | 2026-11-14 | **Complete 18-paper + CMC-Bench report.** Merges local PDF audits + AlphaXiv Passes 1 & 2, fixes cross-pass errors, and reconciles design rules against D1–D5. | §0 PDF inventory & missing downloads · §1 verification fixes · §2 19-source matrix · §3 full spec sheets · §4 design rules · §5 pre-freeze checklist |
| [lit-dossier-verdict-transplant.md](lit-dossier-verdict-transplant/lit-dossier-verdict-transplant.md) | 2026-11-10 | Initial evidence base (10 core + 4 discovered). Superseded as primary index by the Knowledge Base above, but retains verbatim quotes and 4 PNG crops. | §0 scope & corrections · §1 matrix · §2 mechanistic deep dive · §3 countermeasures · §4 novelty boundary · §5 reviewer objections |
| [prereg-freeze-audit.md](prereg-freeze-audit/prereg-freeze-audit.md) | 2026-11-10 | Freeze-readiness audit of the initial pre-registration draft. Autopsies of `2610.33841`, `2610.19407`, `2609.06704`, `2608.17205`, R1–R8 resolutions, and 3 PNG crops. | §1 paper autopsies · §2 dev data · §4 missing templates · §5 replacement novelty claim |

---

## 1. The 14 Primary Sources Locally Present (`Docs/Paper/*.pdf`)

| File | Short name | Why it matters to the thesis | Audit coverage |
|---|---|---|---|
| [2608.17205.pdf](2608.17205.pdf) | *Which Source Wins?* (Ghosh et al., 2026) | **Source of both stimulus sets** (GSM8K/SVAMP + ChartQA-Conflict); `####` margin precedent | Freeze audit §1.4 + AlphaXiv Pass 1 |
| [2610.33841.pdf](2610.33841.pdf) | *Grounding on Request* (Dassen et al., 2026) | Benchmark for explicit-source control arms & directional asymmetry | Freeze audit §1.1 + AlphaXiv Pass 1 |
| [2610.19407.pdf](2610.19407.pdf) | *Biased Bayesian Observers* (Barua et al., 2026) | Length-normalized log-odds margin; 1.4–3.8× text-evidence dominance | Freeze audit §1.2 + AlphaXiv Pass 1 |
| [2609.06704.pdf](2609.06704.pdf) | *Counterfactual Tests for CoT Faithfulness* (Menzat et al., 2026) | Continuous vs. saturating binary scores; no-op control; B=10,000 permutation | Freeze audit §1.3 + AlphaXiv Pass 2 |
| [2609.26986.pdf](2609.26986.pdf) | *Evidence Noncommutativity* (Li et al., 2026) | +15–16.7 pp order effect in Qwen2.5-VL-3B → **counterbalanced order without letters** | Dossier pp. 1–5 + AlphaXiv Pass 1 |
| [2610.38296.pdf](2610.38296.pdf) | *Hidden Commitment* (Assefa & Cho, ICML 2026) | Internal source commitment vs. conflict disclosure (text-only) | Dossier pp. 1–7 + AlphaXiv Pass 1 |
| [2607.27304.pdf](2607.27304.pdf) | *Position, Not Provenance / CoT-Mediate* (Bhowal et al., ICVGIP 2026) | Prefix-forcing > re-prompting; minimal-edit gates; short-horizon paraphrase floor 1.7–3.3% | Dossier pp. 1–6 + AlphaXiv Pass 1 |
| [2604.14888.pdf](2604.14888.pdf) | *Answer Inertia* (Sánchez Villegas et al., COLM 2026) | Early CoT commitment across 18 VLMs incl. Qwen2.5-VL-3B/7B | Dossier pp. 1–9, 20 + AlphaXiv Pass 1 |
| [2511.02243.pdf](2511.02243.pdf) | *When Modalities Conflict* (Zhang et al., 2025) | Competency conditioning precedent; $\Delta H_{\text{rel}}$ balance points | Dossier pp. 1–8 + AlphaXiv Pass 1 |
| [2503.02199.pdf](2503.02199.pdf) | *Words or Vision* (Deng et al., 2025) | Modality bias & weak prompt control (~2.6 pp shift) | Dossier + AlphaXiv Pass 2 |
| [2504.08974.pdf](2504.08974.pdf) | *Mixed Signals* (Pezeshkpour et al., 2025) | Task/difficulty-dependent bias (+56.8 to −74.4) | Dossier + AlphaXiv Pass 2 |
| [2602.14518.pdf](2602.14518.pdf) | *Diagnosing Knowledge Conflict* (Tang et al., 2026) | Truth-anchor directional steering asymmetry | Dossier + AlphaXiv Pass 2 |
| [2606.28273.pdf](2606.28273.pdf) | *Vision-Default, Prior-Override* (Lietzow et al., 2026) | Perception vs. parametric memory sparse prior-head ablation | Dossier + AlphaXiv Pass 2 |
| [2505.23945.pdf](2505.23945.pdf) | *Bias & CoT Faithfulness of L(V)LMs* (Balasubramanian et al., 2025) | Visual bias under-articulation & abrupt CoT flips | Dossier + AlphaXiv Pass 2 |

---

## 2. Core Papers Audited via AlphaXiv — PDFs to Download Later into `Docs/Paper/`

These 5 papers are fully extracted in [THESIS_LITERATURE_KNOWLEDGE_BASE.md](THESIS_LITERATURE_KNOWLEDGE_BASE.md), but their PDFs are **not yet stored locally**:

1. **`2603.01437.pdf`** — Cox, Kianersi & Garriga-Alonso (2026), *Post-Hoc Reasoning in Chain of Thought* ([PDF](https://arxiv.org/pdf/2603.01437)) — explains pre-CoT probe failure when CoT computes the answer (supports D1).
2. **`2510.27484.pdf`** — Macar et al. (ICLR 2026), *Thought Branches* ([PDF](https://arxiv.org/pdf/2510.27484)) — off-policy resilience & resampling vs. greedy single-rollout limitation.
3. **`2307.13702.pdf`** — Lanham et al. (2023), *Measuring Faithfulness in Chain-of-Thought Reasoning* ([PDF](https://arxiv.org/pdf/2307.13702)) — classic CoT interventions & paraphrase baseline.
4. **`2609.25366.pdf`** — Jia & Mu (TMLR 2026), *From Decorative to Load-Bearing* ([PDF](https://arxiv.org/pdf/2609.25366)) — task-difficulty CoT sensitivity & greedy continuation precedent.
5. **`2026.magmar-main.3.pdf`** — Catapang (MAGMaR 2026), *CMC-Bench* ([PDF](https://aclanthology.org/2026.magmar-main.3.pdf)) — multimodal RAG ChartQA/MMMU conflict benchmark (for Ch. 2 Related Work & §1.1 novelty boundary).

Optional Ch. 2 related-work leads (not yet read): `2606.22862.pdf` ([PDF](https://arxiv.org/pdf/2606.22862)) and *Testing Linguistic Invariance in Chain-of-Thought Monitoring* (2026).

---

## `Archive/` — not part of the v5 evidence base

Papers from earlier, abandoned topics (calibration / selective prediction / hallucination) and peer theses kept as formatting references. Do not cite these for v5 claims without re-checking relevance.

| Item | Content |
|---|---|
| `Causal_Source_Arbitration_VLM_Literature_Review.md/.pdf` | Old v3-era "30+ paper" review (4-arm factorial, placebo design). **Superseded.** |
| `CLASH - A Benchmark for Cross-Modal Contradiction Detection.pdf` | arXiv:2511.19199; contradiction-detection benchmark from topic selection. |
| `C3PO - …Omnimodal Models.pdf` | Cross-modal composition/counterfactual benchmark. |
| `13_Do_VLMs_See_What_Blind_User_Show_Them.md/.pdf` | VizWiz distribution-shift audit. |
| `Look Again Before You Abstain.pdf`, `Towards Statistical Factuality Guarantee for LVLMs.pdf`, `Unveiling Uncertainty … MLLM.pdf` | Abstention / calibration papers (old Bangla selective-prediction topic). |
| `Attention is all you need.pdf` | Background. |
| `15 Paper/` | Calibration & hallucination classics with `.md` text extractions (POPE object hallucination, Guo et al. calibration, selective classification, statistical factuality, MLLM uncertainty), plus `Paper.pdf` (unlabelled) and `Trustworthy_MLLM_Precise_Problem_Research_Report.docx`. |
| `Abrar-s-Thesis-Paper/` + `Abrar's Thesis Paper.pdf` | Peer undergraduate theses (Abrar Jawad: Bangla telephonic synthetic data; Shariful Islam: mixed-precision QAT on medical imaging) with `.md` extractions, `assets/` figures, and an AI digest `Thesis_Complete_Reference_Report.md`. Useful only as **thesis format/structure examples**. |
