# Cross-Modal AI Thesis Research Repository

> **Project Title:** Causal Conflict Verbalization and Source Arbitration in Vision-Language Models  
> **Principal Researcher:** Mohammad Zahed Hossen (Technical Lead, Final-Year BSc in CSE, Bangladesh)  
> **Academic Horizon:** 2026–2027  
> **Status:** **Topic Frozen & Empirically Validated (Full Population Census $N = 1,619$ Complete)**  
> **Target Architecture:** `Qwen/Qwen2.5-VL-3B-Instruct` (36 Layers, Hidden Size 2048, 16 Attention Heads)  
> **Benchmark:** `vlm-modality-research/modality-conflict-arbitration-v2`  

---

## 1. Executive Summary & Core Empirical Findings

This repository serves as the definitive scientific workspace, literature audit dossier, and experimental codebase for our undergraduate computer science thesis.

The research investigates **cross-modal sensory conflict arbitration** in Vision-Language Models (VLMs / MLLMs): when visual input contradicts textual instruction or textual context, does prompting the model to explicitly articulate and verbalize the conflict **causally shift its arbitration decision**, or does the generated rationale merely serve as a post-hoc rationalization for an already entrenched visual bias?

### Central Empirical Discovery ($N = 1,619$)

Across a full-population empirical census executed on Google Colab Pro GPU runtimes, the intervention yielded a massive, statistically significant causal shift:

| Experimental Arm | Condition | Visual Capture Rate | Count ($N = 1,619$) | Statistical Significance |
| :--- | :--- | :---: | :---: | :--- |
| **Arm 1** | Direct QA Baseline | **91.17%** | 1,476 / 1,619 | Modality dominance baseline |
| **Arm 2** | Length-Matched Placebo Prompt | **89.50%** | 1,449 / 1,619 | Rules out compute/token expansion confound |
| **Arm 3** | Conflict Verbalization Prompt | **25.76%** | 417 / 1,619 | **Active causal intervention** |

$$\Delta_{\text{arb}} = +63.74\%\text{ net reduction in visual capture} \quad (\text{Odds Ratio } OR = 24.57 \text{ [95\% CI: 20.24, 29.83]},\; p < 10^{-15})$$

These findings prove that **explicit conflict verbalization is a genuine causal mechanism** capable of breaking reflexive visual modality capture in compact foundation models.

---

## 2. Global Structural Taxonomy

```text
MULTIMODAL / VISION-LANGUAGE LEARNING AND SYSTEMS (FROZEN PARENT FIELD)
│
├── 1. Primary Research Lane: Trustworthy and Reliable VLMs
│   ├── Grounding & Evidence Reliance (Visual Token Utilization Decay)
│   ├── Conflict & Inconsistency
│   │   └── [LOCKED PRIMARY TOPIC]: Causal Conflict Verbalization & Source Arbitration
│   ├── Explanatory Faithfulness & Reasoning Mechanics
│   │   └── [RESERVE PROPOSAL 1]: Reasoning Trace Degradation (Causal vs. Softmax/RoPE Dilution)
│   └── Uncertainty Calibration & Selective Abstention
│
├── 2. Secondary Research Lane: Generalization, Adaptation & Distribution Shift
│   └── [RESERVE PROPOSAL 2]: Visual Binding IDs Natural-Transfer Audit
│
├── 3. Active Exploratory Lane: Multimodal Agents & Decision Reliability
│   └── [RESERVE PROPOSAL 3]: Disentangling Tool Utility from Test-Time Compute in ActiView
│
└── 4. Supporting / Conditional Lane: Efficient and Scalable VLMs
    ├── Visual Token Pruning & Context Compression
    └── Parameter-Efficient Fine-Tuning (PEFT / QLoRA)
```

### Archived / Parked Domains & Rationales
- **Medical Imaging (ISIC/HAM10000):** Parked due to superficial benchmark saturation, high regulatory friction, and clinical credentialing requirements.
- **Federated Learning (FeTS-2022):** Parked due to platform-specific simulation bottlenecks and lack of direct cross-modal mechanistic relevance.
- **Bengali VQA Surface Translation:** Parked due to linguistic leakage and lack of algorithmic/cognitive novelty when solely translating standard datasets.

---

## 3. Repository Architecture & Directory Guide

```
Cross Modal/
├── .agents/                      # Antigravity agent configuration and workspace rules root
│   └── rules/                    # Hierarchical rule specifications (thesis_rules.md)
├── Context/                      # Canonical single sources of truth and project operational directives
│   ├── Canonical_Context.md      # Master research operating system and baseline constraints
│   ├── Canonical Thesis Field Specification.md
│   └── Thesis_Progress_and_Research_Map.md
├── Finalize Topic/               # Canonical proposals, full census reports, and execution roadmaps
│   ├── CANONICAL_THESIS_MASTER_REPORT.md    # Definitive scientific record and census report
│   ├── CANONICAL_THESIS_PIPELINE_ROADMAP.md # End-to-end pipeline implementation schedule
│   ├── Pilot/                    # Pilot experiment scripts and diagnostic notebooks
│   └── Canonical_Proposal_1..3   # Audited proposal documents
├── Research_Playbook/            # Research methodologies, paper autopsy protocols, and workflows
│   ├── AI_ML Research Playbook.html
│   └── AI_ML_Research_Playbook.md
├── VLM/                          # Vision-language model literature synthesis and arbitration audits
│   ├── Canonical_Cross_Modal_Thesis_Synthesis.md
│   └── Cross-Modal AI Thesis Discovery (Gemini).md
├── Bengali VLM/                  # Cultural grounding and low-resource multimodal literature autopsies
│   ├── Adversarial literature autopsy.md
│   └── Bangla Cultural VLM Thesis Audit.md
├── Multimodal Agent/             # Literature reports on active perception, tool use, and agentic VLMs
│   ├── AlphaxiV Report.md
│   └── OpenResearch Report.md
├── Medical Imaging & FL/         # Archived adversarial audits of parked domains
├── Extra Field Exploration/      # Early-phase landscape maps and feasibility audits
├── AGENTS.md                     # Universal agent instructions (Antigravity, Claude, Cursor)
├── CLAUDE.md                     # Directives tailored for Claude Code CLI and Anthropic models
└── README.md                     # Repository documentation (this file)
```

---

## 4. Hardware Constraints & Computational Boundaries

To maintain reproducible and sustainable velocity, all experimental workflows adhere to strict compute boundaries:

| Dimension | Specification | Protocol |
| :--- | :--- | :--- |
| **Local Rig** | AMD Ryzen 5 5600G (6C/12T), 8 GB RAM, integrated graphics (no CUDA) | **Strictly documentation, lightweight data exploration, prompt templates, and VCS.** Zero heavy local model execution. |
| **Primary GPU** | **Google Colab Pro** (NVIDIA T4 16GB, V100 16GB, A100 when available) | Single-GPU execution envelope ($\le 16\text{ GB}$ VRAM). PyTorch 2.x SDPA, FP16/bfloat16 precision. |
| **Model Scope** | $\le 3\text{B}$ compact open-weight models (`Qwen2.5-VL-3B-Instruct`) | Factorial intervention, mechanistic probing, and parameter-efficient inference. No foundation model pretraining from scratch. |
| **APIs** | Frontier models (Gemini 1.5 Flash/Pro, GPT-4o) | Reference teacher baselines and cross-model validation ($\le \$5.00$ per run). |

---

## 5. Scientific Standards & Research Rigor

Every experiment in this repository must satisfy the **Level 3 Causal Mechanism Discovery** paradigm:

1. **Falsifiable Hypotheses:** Competing explanations ($H_1$: causal steering vs. $H_0$: post-hoc rationalization) capable of empirical rejection.
2. **Length-Matched Placebo Controls:** Any prompt-based reasoning intervention must be benchmarked against a neutral placebo matched in token count to rule out test-time compute confounding.
3. **Deterministic Metrics:** Predictions are evaluated with deterministic regex matching, ground-truth label verification, and rigorous odds ratio statistics with 95% confidence intervals.
4. **Epistemic Classification:** All documentation categorizes assertions into:
   - `[Verified]`: Directly confirmed by empirical data or peer-reviewed literature.
   - `[Inferred]`: Mathematically or logically derived from verified facts.
   - `[Hypothesis]`: Proposed causal mechanism under empirical test.
   - `[Unknown]`: Unobserved or untested variables.
   - `[Historical Decision]`: Archived decisions from earlier audit rounds.

---

## 6. AI Agent Pair-Programming Setup

This repository is configured for first-class pair-programming with autonomous and interactive AI assistants:

- **[Antigravity IDE](file:///d:/Thesis/Important/Cross%20Modal/.agents):** Customization rules loaded automatically from [`.agents/rules/thesis_rules.md`](file:///d:/Thesis/Important/Cross%20Modal/.agents/rules/thesis_rules.md).
- **[AGENTS.md](file:///d:/Thesis/Important/Cross%20Modal/AGENTS.md):** Unified multi-agent instructions recognized across modern agent platforms.
- **[CLAUDE.md](file:///d:/Thesis/Important/Cross%20Modal/CLAUDE.md):** Quick-reference guidance for Claude Code CLI and Anthropic workflows.
