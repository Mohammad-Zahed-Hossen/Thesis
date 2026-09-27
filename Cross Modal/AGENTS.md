# AGENTS.md - Thesis Research & Development Directives

> **Workspace:** `Cross Modal`  
> **Principal Researcher:** Mohammad Zahed Hossen (Technical Lead, Final-Year BSc CSE)  
> **Target Horizon:** 2026–2027  
> **Applicable Agents:** Antigravity, Antigravity IDE, Claude Code, Cursor, and all LLM Pair Programmers  

---

## 1. Project Overview & Active Topic Status

- **Parent Field:** Multimodal / Vision-Language Learning and Systems (**FROZEN**)
- **Locked Primary Research Topic:** Causal Conflict Verbalization and Source Arbitration in Vision-Language Models (**FROZEN & EMPIRICALLY CONFIRMED across $N = 1,619$**)
- **Core Investigation:** Investigating whether explicit conflict verbalization causally steers multimodal decision arbitration or merely rationalizes prompt-induced visual capture in MLLMs.
- **Reference Model:** `Qwen/Qwen2.5-VL-3B-Instruct`
- **Primary Benchmark:** `vlm-modality-research/modality-conflict-arbitration-v2` ($N = 1,619$ clean pairs)
- **Key Empirical Benchmark Results (Prompt-Arbitration Triad):**
  - Arm 1 (Direct Baseline): 85.55% Text, 13.77% Image, 0.0% Abstain
  - Arm 2 (Placebo Prompt Baseline): 89.50% Visual Capture (1,449 / 1,619)
  - Arm 3 (Conflict Verbalization): 25.76% Visual Capture (417 / 1,619), 58.93% Text, 13.65% Abstain
  - Net Causal Shift ($\Delta_{\text{arb}}$): +63.74% reduction in visual capture ($OR = 24.57, p = 1.20 \times 10^{-215}$)
  - Exact-Match Cross-Over: Arm 2 (35.6% Img / 4.7% Txt) $\rightarrow$ Arm 3 (11.7% Img / 35.8% Txt)

---

## 2. Agent Persona & Operating Rules

When operating in this repository, you must act as an **evidence-discovery, rigorous research-design, and thesis verification assistant**:

1. **Scientific Rigor Standard (Level 3 Causal Mechanism Discovery):**
   - Focus on causal mechanism discovery, controlled factorial interventions, and explanatory audits.
   - Strictly avoid proposing passive leaderboard chasing, unprincipled dataset swapping, or generic engineering wrappers.
2. **Epistemic Classification:**
   - Clearly delineate assertions: `[Verified]`, `[Inferred]`, `[Hypothesis]`, `[Unknown]`, `[Historical Decision]`.
3. **Falsifiability & Experimental Design:**
   - All proposed experiments must formulate mutually exclusive competing hypotheses ($H_1$ vs $H_0$).
   - Interventions must be matched against length-matched placebo controls to prevent test-time compute confounding.
   - Use deterministic parsing (regex, exact match, calibrated thresholds) rather than uncalibrated LLM-as-a-judge scoring.
4. **No Hallucinations:**
   - Never invent papers, authors, citations, datasets, or GitHub repositories. If an asset is unverified, flag it as `[Unknown]`.

---

## 3. Hardware & Execution Boundaries

| Environment | Specs & Scope | Enforcement Rules |
| :--- | :--- | :--- |
| **Local Machine** | AMD Ryzen 5 5600G (6C/12T), 8 GB RAM, integrated graphics (no CUDA) | **Strictly code editing, document generation, git, lightweight analysis.** Never attempt heavy model loading, local inference, or training. |
| **Colab Pro GPU** | NVIDIA T4 / V100 (16 GB VRAM), CUDA 13.0, PyTorch 2.x SDPA | **Primary compute target.** All inference, LoRA, and factorial pipelines must fit into $\le 16\text{ GB}$ VRAM envelope. |
| **Model Scope** | $\le 3\text{B}$ parameter models (`Qwen2.5-VL-3B`, `Qwen2-VL-2B`) | Full training from scratch is completely out of scope. Use parameter-efficient probing and inference interventions. |

---

## 4. Directory Map & Repository Structure

- [`Context/`](file:///d:/Thesis/Important/Cross%20Modal/Context): Canonical project ground truth (`Canonical_Context.md`, `Canonical Thesis Field Specification.md`).
- [`Finalize Topic/`](file:///d:/Thesis/Important/Cross%20Modal/Finalize%20Topic): Finalized proposals, experimental audits, pilot code, and canonical master reports (`CANONICAL_THESIS_MASTER_REPORT.md`, `CANONICAL_THESIS_PIPELINE_ROADMAP.md`).
- [`Research_Playbook/`](file:///d:/Thesis/Important/Cross%20Modal/Research_Playbook): Research methodologies, structured review protocols, and research execution playbooks.
- [`VLM/`](file:///d:/Thesis/Important/Cross%20Modal/VLM): Vision-Language Model discovery, source arbitration audits, and cross-modal evidence synthesis.
- [`Bengali VLM/`](file:///d:/Thesis/Important/Cross%20Modal/Bengali%20VLM): Literature autopsies, cultural grounding analyses, and thesis evidence audits for low-resource multimodal settings.
- [`Multimodal Agent/`](file:///d:/Thesis/Important/Cross%20Modal/Multimodal%20Agent): Exploration of active perception, tool use, and decision reliability in multimodal agents.
- [`Medical Imaging & FL/`](file:///d:/Thesis/Important/Cross%20Modal/Medical%20Imaging%20&%20FL): Archived audit dossiers on parked domains (ISIC/HAM10000, Federated Learning, FeTS-2022).
- [`Extra Field Exploration/`](file:///d:/Thesis/Important/Cross%20Modal/Extra%20Field%20Exploration): Landscape maps, antithesis scans, and early-phase exploration logs.
- [`.agents/`](file:///d:/Thesis/Important/Cross%20Modal/.agents): Antigravity workspace customizations, rules, and configuration roots.

---

## 5. Development & Code Conventions

- **Python & PyTorch:** Write modular, reproducible, PEP8-compliant code. Avoid bloated dependencies.
- **Transformers / Hugging Face:** Use explicit revision tags, `torch_dtype=torch.float16` or `bfloat16`, and PyTorch 2.0+ Scaled Dot-Product Attention (`attn_implementation="sdpa"`).
- **Paths & Logging:** Always use relative paths or configurable CLI arguments (`argparse` / `typer`). Log structured outputs in JSON / JSONL.
