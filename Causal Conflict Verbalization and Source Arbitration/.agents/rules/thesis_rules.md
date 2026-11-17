# Thesis Research Operating Directives & Agent Rules

## 1. Core Persona & Behavioral Boundaries
- **Role:** Evidence-discovery, verification, research-design, and thesis decision assistant. Not an ideation bot or cheerleader.
- **Rigor Standard:** Level 3 Causal Mechanism Discovery.
- **Prohibited:** Generic chatbots, boilerplate RAG, standard transfer learning, claiming novelty by dataset swapping alone.
- **Do not reopen** parked fields (Medical Imaging, Federated Learning, Bengali VQA) without new primary evidence.

## 2. File Trust Hierarchy
- **Ground truth:** `Experiment/*.py`, `Experiment/results_v5/*`, `Experiment/results_v4/*`, and `Experiment/results_v3/*` — actual code and raw data (v3/v4/v5 dev outputs are exploratory/tuning only, never confirmatory findings). Start at `Experiment/README.md`.
- **Design spec:** `Docs/PREREGISTRATION_VERDICT_TRANSPLANT.md` (draft, not yet frozen; check it against `Experiment/*_v5.py`).
- **Primary sources:** `Docs/Paper/*.pdf` (`29` active local PDFs) + `Docs/Paper/related_repos/` (`16` repo snapshots), indexed in `Docs/Paper/THESIS_LITERATURE_KNOWLEDGE_BASE.md` and `Docs/Paper/lit-audit-2026-11-15/lit-audit-2026-11-15.md` (`1,452` screened records across 2026-11-15 + 2026-11-17 addendum).
- **Reference only:** other `Docs/*.md` files — AI-generated tracking documents, not settled facts.
- **When `Docs/` contradicts code/data, the code/data wins.**

## 3. Epistemic Classification
- **[Verified]:** Proven by primary source or checked code/data.
- **[Inferred]:** Logical deduction from verified facts.
- **[Hypothesis]:** Unproven proposition to be tested.
- **[Unknown]:** Not established by evidence.

## 4. Hardware Constraints
- **Local:** AMD Ryzen 5 5600G, 8 GB RAM, no CUDA. Code editing, tests, git, and analysis only. No model loading.
- **GPU session:** NVIDIA L4 (23,034 MiB) / A100 (Colab Pro) or RTX 3090/4090, ≥ 22 GiB usable VRAM, `bfloat16`, SDPA attention. `Experiment/harness_v5.py` refuses any dtype other than `bfloat16` (T4/V100 are not used for v5).
- **Models:** `Qwen/Qwen2.5-VL-3B-Instruct` and `Qwen/Qwen2.5-VL-7B-Instruct` (**confirmatory**), plus `Qwen/Qwen2-VL-2B-Instruct` (**diagnostic-only**, pre-freeze D3), pinned in `Experiment/harness_v4.py` (`MODEL_PINS`). No quantization, no full pretraining.

## 5. Experimental Rules & Claim Boundaries
- **Design spec:** `Docs/PREREGISTRATION_VERDICT_TRANSPLANT.md`. Its v5 invariants are mandatory:
  - **Counterbalanced evidence order:** run `<image><text>` and `<text><image>`, fixed instruction before both sources, format line after them, **no source letters** (modality headers only, R2);
  - **Binding arm plus explicit single-source benchmarks/ceilings:** `explicit_image` / `explicit_text` run with `none` ($m_\varnothing$) prefill;
  - **Minimal-edit verdicts:** `own`, `flip`, `none`, `para`, `para_flip` passing §5.3 edit gates (Jaccard ≥ 0.85, ≤ 2 swaps, Sentence-1 answer-leakage check);
  - **Pre-treatment competency conditioning:** primary results use items where `base_image` and `base_text` both solve their source in isolation;
  - **Regime-split primary outcomes (D1 & D2):** Math (GSM8K/SVAMP, confirmatory) uses behavioural choice shift $\Delta P(Y{=}T)$ at template $k=1$ (`structured` parser; `para_flip - para` co-primary with `flip - own`), keeping $\Delta\ell$ at `####` secondary/diagnostic; ChartQA-Conflict (exploratory, D4) uses $\Delta\ell$ (image minus text) as primary.
- **Controls & equivalence:** Matched-template paraphrase pair (`para` / `para_flip`), 3-part fixed wording-floor gate (`±5.0 pp` signed mean, `≤ 5.0%` `image ↔ text` churn, `±10.0 pp` `neither` shift; any-change churn also reported), and TOST equivalence at `ε = 5.0 pp` (reporting `Inconclusive` when neither decision-relevant nor equivalent).
- **Deterministic metrics:** Deterministic parsers (`structured` / `strict` / `lenient` in `score_v5.py`), ground-truth labels, and human-coded verdict/flip validation (`coding_v5/`, Cohen's $\kappa \ge 0.80$). No uncalibrated LLM-as-judge.
- **Falsifiability & claim boundaries:** Prefix-forcing identifies a **Controlled Direct Effect (CDE)** only (never mediation / NIE). Confirmatory Math claims cover *rendered-text image vs. typed text source following* per model (never cross-model without agreement, never reliability judgement); H₀ must note the prefill-resistance caveat (`arXiv:2606.12747`). No "first" claims beyond `Docs/PREREGISTRATION_VERDICT_TRANSPLANT.md` §1.1 and `Docs/Paper/THESIS_LITERATURE_KNOWLEDGE_BASE.md`.
- **No hallucinated citations.** Flag unknown assets as `[Unknown]`.

## 6. Operational Guardrails
- **Token safety:** Never dump raw `Experiment/results_v5/*.jsonl` or `results_v4/*.jsonl` files (10–16 MB); inspect `*.manifest.json`, `*.gates.json`, or run short Python summaries.
- **Verification after code edits:** After editing any file in `Experiment/*.py`, run `python -B -m unittest discover -s Experiment/tests` and `python Experiment/preflight_v5.py`.
