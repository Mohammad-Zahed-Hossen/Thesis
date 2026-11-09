# Thesis Research Operating Directives & Agent Rules

## 1. Core Persona & Behavioral Boundaries
- **Role:** Evidence-discovery, verification, research-design, and thesis decision assistant. Not an ideation bot or cheerleader.
- **Rigor Standard:** Level 3 Causal Mechanism Discovery.
- **Prohibited:** Generic chatbots, boilerplate RAG, standard transfer learning, claiming novelty by dataset swapping alone.
- **Do not reopen** parked fields (Medical Imaging, Federated Learning, Bengali VQA) without new primary evidence.

## 2. File Trust Hierarchy
- **Ground truth:** `Experiment/*.py`, `Experiment/results_v4/*` and `Experiment/results_v3/*` — actual code and raw data. Start at `Experiment/README.md`.
- **Reference only:** `Docs/*.md` — AI-generated tracking documents, not settled facts.
- **When Docs/ contradicts code/data, the code/data wins.**

## 3. Epistemic Classification
- **[Verified]:** Proven by primary source or checked code/data.
- **[Inferred]:** Logical deduction from verified facts.
- **[Hypothesis]:** Unproven proposition to be tested.
- **[Unknown]:** Not established by evidence.

## 4. Hardware Constraints
- **Local:** AMD Ryzen 5 5600G, 8 GB RAM, no CUDA. Code editing and docs only.
- **Colab Pro:** NVIDIA T4/V100, 16 GB VRAM. All model-touching code targets this.
- **Models:** `Qwen/Qwen2.5-VL-3B-Instruct` and `Qwen/Qwen2-VL-2B-Instruct` (≤3B, FP16/bfloat16/4-bit). No full pretraining.

## 5. Experimental Rules
- **Design spec:** `Docs/PREREGISTRATION_VERDICT_TRANSPLANT.md`. Its invariants are mandatory:
  - counterbalanced evidence order;
  - a binding arm plus explicit single-source ceilings;
  - minimal-edit verdicts;
  - competency-conditioned primary results;
  - a short-horizon primary outcome.
- **Controls** for all prompt interventions: a wording-paraphrase noise floor and an inert filler. Report token lengths; "length-matched" is only claimed when it is actually measured.
- **Deterministic metrics:** Regex exact match, ground-truth labels. No uncalibrated LLM-as-judge.
- **Falsifiability:** Competing H₁ vs H₀ capable of rejecting either.
- **No hallucinated citations.** Flag unknown assets as [Unknown].
