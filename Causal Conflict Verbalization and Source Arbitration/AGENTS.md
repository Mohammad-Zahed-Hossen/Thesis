# AGENTS.md — Thesis Research & Development Directives

> **Workspace:** Causal Conflict Verbalization and Source Arbitration  
> **Principal Researcher:** Mohammad Zahed Hossen (Technical Lead, Final-Year BSc CSE)  
> **Target Horizon:** 2026–2027  
> **Applicable Agents:** Antigravity, Claude, and all LLM Pair Programmers  

---

## 1. Project Overview

- **Parent Field:** Multimodal / Vision-Language Learning and Systems (**FROZEN**)
- **Working Title (pre-registration):** *Does the Verdict Decide? Testing Whether Stated Source Reliability Steers Vision-Language Models under Image–Text Conflict*
  - Replaces "Causal Conflict Verbalization and Source Arbitration in VLMs"; the folder name is unchanged.
- **Research Focus:** Multimodal chain-of-thought faithfulness. Under image–text conflict, does a prefix-forced reliability verdict causally steer which source's answer the model gives?
  - Held fixed: instruction, counterbalanced evidence order, and wording template.
  - Varied: with vs. without a binding instruction.
- **Models:** `Qwen/Qwen2.5-VL-3B-Instruct` and `Qwen/Qwen2-VL-2B-Instruct`. Both run on Colab Pro 16 GB GPUs; revisions are pinned in `Experiment/harness_v4.py` (`MODEL_PINS`).
- **Stimuli:**
  - Task-selection conflict: `vlm-modality-research/modality-conflict-arbitration-v2` (GSM8K/SVAMP).
  - Evidence conflict: `vlm-modality-research/chartqa-evidence-conflict-v2` (229 items).
  - Both come from *Which Source Wins?* (arXiv:2608.17205).
- **Design Spec:** `Docs/PREREGISTRATION_VERDICT_TRANSPLANT.md` (draft, not yet frozen). Evidence base: `Archive/Paper/lit-dossier-verdict-transplant/lit-dossier-verdict-transplant.md`.
- **Current Phase:** v3 pilot and v4 dev runs are done (exploratory only), and the literature audit is done. Next: upgrade the harness to v5, then freeze the pre-registration. **No confirmatory data exists.**

### What the Pilot Does and Does Not Show
- The pipeline works on `Qwen/Qwen2.5-VL-3B-Instruct` on a T4 [Verified].
- The v3 contrast (placebo vs. conflict prompt) is large, but it compares two *instructions*, not verbalizations [Verified, `Experiment/results_v3/README.md`].
- In v4 dev, on the 110 items solvable from both sources, reversing a forced verdict moved image answers by +20.9 pp under the neutral instruction and −1.8 pp under the conflict instruction. This is dev data only, not a finding [Verified, dossier §2.2].

### Mandatory Methodological Invariants (v5 onward)
1. **Evidence order counterbalanced.** Run `<image><text>` and `<text><image>`. Keep the instruction fixed before both sources and the format line after them, and counterbalance the A/B labels. This controls the roughly +15 pp recency effect in Qwen2.5-VL-3B (arXiv:2609.26986).
2. **Binding arm plus explicit single-source ceilings.** Binding: "solve only the problem from the source you named as more reliable". Ceilings: `explicit_image` / `explicit_text`. These remove prompt ambiguity and bound the binding effect.
3. **Minimal-edit verdicts.** Swap only the source noun in the model's own generated reliability clause. Gates: one clause changed; the stated source actually flips; token Jaccard ≥ 0.85. Foreign authored verdicts are a secondary arm only.
4. **Competency conditioning.** Primary results use only items where `base_image` and `base_text` both solve their problems in isolation.
5. **Short-horizon primary outcome.** Force `####` right after the verdict, then score a short decode and the log-likelihood margin. Free solving is secondary.
6. **Claim boundary.** Prefix-forcing identifies a controlled direct effect, not mediation. No "first" claims beyond the dossier's §4.1 boundary.

---

## 2. CRITICAL: File Trust Levels

> [!IMPORTANT]
> **All `.md` files in `Docs/` are AI-generated tracking documents.** They are NOT ground truth. They may contain inaccuracies or stale plans.

| Location | Trust Level | What It Contains |
|:---------|:-----------|:-----------------|
| `Experiment/*.py` | **Ground truth** | Active v4 code; start at `Experiment/README.md` |
| `Experiment/results_v4/`, `Experiment/results_v3/` | **Ground truth** | Run outputs and analysis; each has a README |
| `Experiment/archive/` | **Historical** | v3 harness and early pilots |
| `Docs/PREREGISTRATION_VERDICT_TRANSPLANT.md` | **Design spec** | Pre-registration draft; check it against code |
| `Docs/` (other files) | **Reference only** | AI-generated narrative, tracking, and decision logs; several are stale |
| `Archive/Paper/` | **Primary sources** | Downloaded papers and the literature dossier |
| `Archive/` (other files) | **Historical** | Parked explorations, not active |

---

## 3. Agent Behavioral Rules

1. **Scientific Rigor (Level 3):** Controlled factorial interventions with pre-registered contrasts, wording-noise floors and instruction ceilings. No leaderboard chasing.
2. **Epistemic Tags:** `[Verified]`, `[Inferred]`, `[Hypothesis]`, `[Unknown]`.
3. **No Hallucinations:** Never invent papers, citations, datasets, or repos.
4. **Don't treat Docs/ as truth:** Cross-check narrative claims against actual code and data.
5. **No reopening parked fields** without new primary evidence.

---

## 4. Hardware & Execution Boundaries

| Environment | Specs | Rules |
|:-----------|:------|:------|
| **Local** | AMD Ryzen 5 5600G, 8 GB RAM, no CUDA | Code editing, docs, git, analysis only. No model loading. |
| **Colab Pro** | NVIDIA T4/V100 (16 GB VRAM), CUDA 13.0, PyTorch 2.x | Primary compute. All inference must fit ≤16 GB VRAM. |
| **Model** | ≤3B parameters (Qwen2.5-VL-3B, Qwen2-VL-2B) | Inference-first. No full pretraining. |

---

## 5. Directory Structure

```
├── Experiment/          ← CODE + DATA (ground truth)
│   ├── README.md        ← Current status; read first
│   ├── *.py, tests/     ← Active v4 code and tests
│   ├── results_v4/      ← v4 runs and dev analysis
│   ├── results_v3/      ← v3 pilot outputs and re-analysis
│   ├── coding_v3/       ← Human-coding sheets
│   └── archive/         ← v3 harness and early pilots
├── Docs/                ← AI-generated tracking (reference only)
│   ├── PREREGISTRATION_VERDICT_TRANSPLANT.md ← Design spec (draft)
│   ├── Context/         ← Historical context
│   ├── Decision_Audits/ ← Topic selection audits
│   └── Parked_Proposals/← Deprecated proposals
├── Thesis/              ← Thesis chapters (writing in progress)
├── Archive/             ← Parked exploration domains
├── CLAUDE.md            ← Claude-specific directives
└── .agents/             ← Antigravity agent config
```

---

## 6. Code Conventions

- **Python & PyTorch:** Modular, reproducible, PEP8-compliant.
- **Transformers:** Explicit revision tags, `torch_dtype=torch.float16`, `attn_implementation="sdpa"`.
- **Paths:** Relative or configurable CLI args. Structured JSON/JSONL logging.
