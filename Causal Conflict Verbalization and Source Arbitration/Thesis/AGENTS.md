# Thesis/AGENTS.md — Scoped Directives for Thesis Drafting & Defense Prose

> Applies only when working inside `Thesis/`. Zero token cost when coding in `Experiment/`.

## 1. Required Context Before Drafting Chapters
1. Read `Thesis/THESIS_NARRATIVE_AND_FRAMING_GUIDE.md` for chapter narrative structure and approved vs. forbidden phrasing.
2. Read `Docs/RESEARCH_OBJECTIVE.md` and `Docs/PREREGISTRATION_VERDICT_TRANSPLANT.md` (§1–§2, §10–§11) for exact hypotheses, estimands, and claim boundaries.
3. Ground all citations in `Docs/Paper/THESIS_LITERATURE_KNOWLEDGE_BASE.md` (`18` core + CMC-Bench), `Docs/Paper/lit-audit-2026-11-15/lit-audit-2026-11-15.md` (`1,452` screened records; `references.bib` with `47` entries), and local PDFs in `Docs/Paper/`.

## 2. Ground-Truth & Numeric Integrity Rules
- **Verify every number from ground truth:** Cross-check counts, CIs, $p$-values, and model metrics against `Experiment/results_v5/` (or confirmatory outputs once `--phase confirm` runs), `*.manifest.json` / `*.gates.json`, and `Experiment/*.py`. Never copy numbers blindly from narrative `.md` files.
- **Dev vs. confirmatory boundary:** Never present v3 pilot (`results_v3/`), v4 dev (`results_v4/`), or v5 dev (`results_v5/v5dev_*`) numbers as confirmatory findings. Label them explicitly as exploratory/dev-tuning only.
- **Do not cite deprecated material:** Never cite `Docs/Paper/Archive/` papers or superseded v3 reports (`results_v3/statistical_report v3.0.md`, `thesis_contingency_table v3.0.tex`).

## 3. Mandatory Framing & Claim Boundaries
- **Estimand:** Prefix-forcing identifies a **Controlled Direct Effect (CDE)** at fixed instruction, order, and wording—never call it mediation or a natural indirect effect.
- **Regime & model scope:** Confirmatory claims apply **per model** (`Qwen2.5-VL-3B-Instruct`, `Qwen2.5-VL-7B-Instruct`) in Math (GSM8K/SVAMP) and cover *rendered-text image vs. typed-text source following* (not reliability judgement or general natural visual evidence). `ChartQA-Conflict` is exploratory (D4); `Qwen2-VL-2B-Instruct` is diagnostic-only (D3). `3B vs. 7B` is a within-generation size comparison, never a scaling law.
- **Equivalence & H₀ caveat:** Report `Inconclusive` whenever neither decision-relevant nor TOST-equivalent (`ε = 5.0 pp`). Any H₀ reading must explicitly state the off-preference **prefill-resistance** caveat (`arXiv:2606.12747`) alongside `verdict_nll` stratification.
- **Citation accuracy:** Verify exact author names, titles, arXiv IDs/DOIs, venues, and table/page numbers against `Docs/Paper/*.pdf` or `lit-audit-2026-11-15/references.bib` before including any citation or BibTeX entry.
