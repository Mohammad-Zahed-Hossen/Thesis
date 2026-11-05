# Causal Conflict Verbalization and Source Arbitration in Vision-Language Models

> **Principal Researcher:** Mohammad Zahed Hossen (Final-Year BSc CSE, Bangladesh)  
> **Status:** Topic frozen, full-population experiment complete (N=1,619), thesis writing in progress  
> **Model:** `Qwen/Qwen2.5-VL-3B-Instruct`  
> **Dataset:** `vlm-modality-research/modality-conflict-arbitration-v2`

---

## What This Research Investigates

When a VLM receives contradictory visual and textual inputs, does prompting it to explicitly verbalize the contradiction **causally change** which modality it follows? Or is the verbalization just a post-hoc rationalization for an already-entrenched bias?

### Core Finding

Conflict verbalization reduced visual capture from **89.50%** (placebo) to **25.76%** (intervention), a net shift of **+63.74 percentage points** (OR=24.57, p<10⁻²¹⁵). This was confirmed by an exact-match mathematical cross-over.

---

## Repository Structure

```
├── Experiment/              Code + data (ground truth)
│   ├── production_experiment_harness_v3.py    Full census harness
│   ├── statistical_analysis.py                Hypothesis testing
│   ├── prefreeze_pilot.py                     Pilot v1
│   ├── prefreeze_pilot_v2.py                  Pilot v2
│   ├── prefreeze_pilot.ipynb                  Colab notebook
│   └── Results/
│       ├── full_experiment_results v3.0.json  Item-level data (5.3 MB)
│       ├── experiment_checkpoint v3.0.csv     Checkpoint data
│       ├── statistical_report v3.0.md         Statistical outputs
│       └── thesis_contingency_table v3.0.tex  LaTeX table
│
├── Docs/                    AI-generated tracking documents (reference only)
│   ├── Canonical_Thesis_Topic_Specification (Locked).md
│   ├── CANONICAL_THESIS_MASTER_REPORT.md
│   ├── CANONICAL_THESIS_PIPELINE_ROADMAP.md
│   ├── Context/             Historical project context
│   ├── Decision_Audits/     Topic selection audit trail
│   └── Parked_Proposals/    Deprecated proposal specifications
│
├── Thesis/                  Thesis chapters (in progress)
│
├── Archive/                 Parked explorations
│   ├── Bengali VLM/         Cultural grounding (deprecated)
│   ├── Medical Imaging & FL/ ISIC/FeTS (parked)
│   ├── Multimodal Agent/    Active perception (parked)
│   ├── VLM/                 Early VLM exploration
│   ├── Paper/               Reference papers
│   ├── Research_Playbook/   Methodology protocols
│   └── Experiment_History/  Older experiment versions (v1, v2)
│
├── CLAUDE.md                Claude directives
├── AGENTS.md                Universal agent instructions
└── .agents/                 Antigravity workspace config
```

## Hardware Constraints

| Component | Spec | Usage |
|:----------|:-----|:------|
| Local | AMD Ryzen 5 5600G, 8 GB RAM, no CUDA | Code editing, docs, analysis |
| GPU | Google Colab Pro (T4/V100, 16 GB VRAM) | All inference and experiments |
| Model | ≤3B params, FP16/bfloat16 | Inference-first, no pretraining |
