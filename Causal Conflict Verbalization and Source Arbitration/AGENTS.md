# AGENTS.md — Thesis Research & Development Directives

> **Workspace:** Causal Conflict Verbalization and Source Arbitration  
> **Principal Researcher:** Mohammad Zahed Hossen (Technical Lead, Final-Year BSc CSE)  
> **Target Horizon:** 2026–2027  
> **Applicable Agents:** Antigravity, Claude, and all LLM Pair Programmers  

---

## 1. Project Overview

- **Parent Field:** Multimodal / Vision-Language Learning and Systems (**FROZEN**)
- **Locked Research Topic:** Causal Conflict Verbalization and Source Arbitration in VLMs (**FROZEN; exploratory pilot only, N=1,619; not confirmed**)
- **Core Question:** Does explicit conflict verbalization causally steer multimodal decision arbitration, or merely rationalize prompt-induced visual capture?
- **Reference Model:** `Qwen/Qwen2.5-VL-3B-Instruct`
- **Primary Benchmark:** `vlm-modality-research/modality-conflict-arbitration-v2`
- **Current Phase:** Feasibility & pilot validation complete; entering structured thesis planning, refining experimental design for formal production runs, and supervisor review.

### Preliminary Pilot Findings (Validation of Viability)
- Confirmed working pipeline on `Qwen/Qwen2.5-VL-3B-Instruct`
- Preliminary pilot runs demonstrate significant arbitration shift between Placebo and Conflict Verbalization conditions
- Exact-match arithmetic cross-over detected in preliminary pilot data, validating that the effect is computationally measurable.

---

## 2. CRITICAL: File Trust Levels

> [!IMPORTANT]
> **All `.md` files in `Docs/` are AI-generated tracking documents.** They are NOT ground truth. They may contain inaccuracies or stale plans.

| Location | Trust Level | What It Contains |
|:---------|:-----------|:-----------------|
| `Experiment/*.py` | **Ground truth** | Active v4 code; start at `Experiment/README.md` |
| `Experiment/results_v4/`, `Experiment/results_v3/` | **Ground truth** | Run outputs and analysis; each has a README |
| `Experiment/archive/` | **Historical** | v3 harness and early pilots |
| `Docs/` | **Reference only** | AI-generated narrative, tracking, and decision logs |
| `Archive/` | **Historical** | Parked explorations, not active |

---

## 3. Agent Behavioral Rules

1. **Scientific Rigor (Level 3):** Causal mechanism discovery with controlled factorial interventions. No leaderboard chasing.
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
