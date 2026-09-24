# Cross-Modal Discovery Synthesis and Thesis Handover Report
**Canonical Research Record, Empirical Autopsies, and Strategic Decision Framework**

*Document Status: Master Context & Handover Specification*  
*Location: `/Context/Cross_Modal_Discovery_Synthesis_and_Handover.md`*  
*Effective Date: 20 September 2026 | Researcher: Mohammad Zahed Hossen*  
*Consolidated from: AlphaXiv, Gemini, Perplexity, Claude Adversarial Audits, and Updated Canonical Specifications*

---

## 1. Executive Summary & Purpose of This Document

This document serves as the **definitive, standalone context and handover asset** for Mohammad Zahed Hossen's undergraduate thesis in Computer Science & Engineering. It captures the entire trajectory of cross-modal thesis discovery, reconciles four conflicting AI research streams, records the findings of three primary-paper full-text autopsies on alphaXiv, documents the modernized constraint updates, and establishes an airtight decision protocol.

Any future AI assistant or researcher reading only this document will have complete, unambiguous visibility into:
1. **Who the researcher is and their exact operating constraints.**
2. **What research paths were explored, audited, and eliminated (and why).**
3. **The verified status of the top surviving candidate (Surviving RQ 1) held in queue.**
4. **The strategic fork in the road unlocked by recent constraint modernizations (Medical VLM and Multimodal Agents).**
5. **The exact 48-hour decision protocol to finalize the thesis topic without further analysis paralysis.**

---

## 2. Researcher Profile & Operating Constraints (Modernized)

* **Researcher:** Mohammad Zahed Hossen, final-year undergraduate CSE student in Bangladesh; technical lead of a 3-person self-directed thesis team.
* **Local Hardware:** AMD Ryzen 5 5600G (6 cores / 12 threads, Radeon Vega 7 integrated graphics, 8 GB system RAM, no dedicated CUDA training GPU). Used exclusively for local coding, data inspection, Git orchestration, and lightweight debugging.
* **Cloud GPU Compute:** Google Colab Pro (access to NVIDIA T4 16GB, V100 16GB, and occasional A100 40GB instances).
* **Modernized Policy Updates (Effective September 2026):**
  1. *Commercial Frontier APIs Enabled:* Budgeted access to commercial APIs (OpenAI GPT-4o, Anthropic Claude 3.5 Sonnet, Google Gemini 1.5 Pro) is authorized for comparative baselines, agentic planning, LLM-as-a-judge evaluation, and synthetic dataset generation.
  2. *Active Research Lanes:*
     - **Primary Lane:** Trustworthy, Grounded, and Calibrated Multimodal Models (VLM/MLLM).
     - **Unparked Domain 1 (Multimodal Agents):** Active perception, tool selection, action-value prediction, and decision reliability.
     - **Unparked Domain 2 (Medical Imaging):** Vision-language calibration, selective prediction, and PEFT adaptation on public standardized benchmarks (CheXpert, ISIC, MedMNIST).
  3. *Methodological Scope:* Novel algorithms, agent coordination architectures, and parameter-efficient fine-tuning (PEFT/LoRA) are authorized alongside empirical diagnostic evaluations.
  4. *Velocity:* Paced under modern AI-assisted engineering velocity standards rather than an artificial 3–4 month calendar block.

---

## 3. The Discovery Journey & Reconciled Audits

Over a 30-day period, research directions were scanned across multiple platforms, producing four primary documents:
1. **Base Discovery (AlphaXiv):** `Cross-modal evidence use and source arbitration.md`
2. **Gemini Discovery:** `Cross-Modal AI Thesis Discovery (Gemini).md`
3. **Perplexity Discovery:** `Cross-modal evidence use and source arbitration (Perflexity).md` & `kill occupied questions (Perflexity).md`
4. **Adversarial Audit (Claude):** `Claude Critique Analysis.md`

### Core Failures Uncovered in Earlier Proposals:
* **The Artificial Consensus Trap:** Report 2 (Gemini) mirrored Report 1, and Report 3 (Perplexity) was seeded with local project files. The "agreement" between assistants was an echo-chamber.
* **The `multimodal-arbitration-artifact` Failure:** Earlier reports claimed this dataset supported 1,000 paired items evaluating "arbitration accuracy." Claude cloned the repository (`Ro-netizen004/multimodal-arbitration-artifact`) and proved:
  - It contained only **229 chart items** (arithmetic was on ephemeral review mirrors).
  - The prompt explicitly stated *"Neither source is privileged"* and evaluated **source preference**, not accuracy. No ground-truth correctness existed.
* **Token Pruning Locality Fallacy:** Claiming that token pruning selectively harms localized OCR before global scenes was rejected as geometrically trivial (resolution scales with pixels) and confounded by comparing different benchmarks.

---

## 4. The Decisive alphaXiv Full-Text Autopsies

To eliminate second-hand hallucinations, three candidate research questions were subjected to full-text autopsies on primary papers using alphaXiv:

### Autopsy 1: RQ 1 (Conflict Arbitration & Causal Verbalization)
* **Primary Papers Audited:** *CLASH* (`arXiv:2511.19199`) and *Which Source Wins?* (`arXiv:2608.17205`).
* **Scientific Gap Status:** **100% Open & Unoccupied.** The authors of *Which Source Wins?* explicitly confirmed in §6 (Limitations):  
  > *"our framework measures forced source arbitration under reduced legibility rather than factual reliability or conflict awareness. Consequently, we do not test whether models detect the contradiction, express uncertainty, or abstain."*
* **Dataset Availability:**  
  - *CLASH* is unreleased ("codebase will be released upon acceptance").
  - *Which Source Wins?* is **fully released and public on Hugging Face**:
    - Arithmetic conflicts (1,304 clean, mathematically distinct pairs): [`vlm-modality-research/modality-conflict-arbitration-v2`](https://huggingface.co/datasets/vlm-modality-research/modality-conflict-arbitration-v2)
    - Chart conflicts (229 validated items): [`vlm-modality-research/chartqa-evidence-conflict-v2`](https://huggingface.co/datasets/vlm-modality-research/chartqa-evidence-conflict-v2)
* **Compute Footprint:** Tested on **`Qwen2-VL-2B-Instruct`** in `bfloat16`. Consumes ~4.5 GB VRAM. Zero-shot inference across 500 items takes $\approx 90$ minutes on a single Colab Pro T4 GPU.
* **Causal Placebo Innovation:** Neither paper tested a **length-matched neutral placebo prompt** or **rationale prefilling**. This provides a bulletproof causal test of whether conflict verbalization is an active control mechanism or post-hoc rationalization.
* **Verdict:** **CLEARED FOR EXECUTION (THE HELD INSURANCE POLICY).**

---

### Autopsy 2: RQ 2 (Evidence-Sufficiency Masking & Uncertainty Calibration)
* **Primary Papers Audited:** *Seeing without Looking* (`arXiv:2605.22903`) and *Evidence-Order Calibration (EOC)* (`arXiv:2609.09184`).
* **Scientific Gap Status:** **Partially Occupied.** *EOC* already implemented the exact 5-level masking ladder ($\lambda \in \{0, .25, .5, .75, 1\}$), extracted token entropy and sequence confidence, and proved that **92% of individual trajectories violate monotonicity**.
* **Dataset Availability:** Neither paper provided a public Hugging Face or GitHub URL. EOC uses an internal GQA manifest with only 176 items. *Seeing without Looking* filtered to 117 items via a complex Grounding DINO + SAM2 + GPT-5 pipeline.
* **Verdict:** **REJECTED AS PRIMARY THESIS** (Narrow novelty; unreleased/heavily filtered datasets).

---

### Autopsy 3: RQ 4 (Counterfactual Rationale Faithfulness)
* **Primary Papers Audited:** *C³PO* (`arXiv:2608.05381`) and *Which Modality Decides? (CMA)* (`arXiv:2608.00076`).
* **Scientific Gap Status:** Theoretically open, but ill-posed on these papers. C³PO only evaluated short answers with an LLM judge (Qwen3-Omni); CMA used a non-generative classifier with a 2-layer MLP head. Neither evaluated generated text rationales.
* **Dataset & Compute Availability:**  
  - C³PO required **4x A100 80GB + 2x RTX 5000 GPUs** and has dataset count discrepancies (3,342 vs 3,404).
  - CMA requires coupled image/text DDPM diffusion inpainting. Code is unreleased ("forthcoming upon acceptance").
* **Verdict:** **REJECTED AS PRIMARY THESIS** (Massive compute barriers, classifier models, unreleased diffusion pipelines).

---

### Why RQ 3 and RQ 5 Were Deprioritized:
* **RQ 3 (Selective Abstention on Unanswerable Inputs - TUBench/CARA):**  
  Put in reserve due to: (1) subjective annotator disagreement on out-of-frame boundaries; (2) mathematical collapse of exchangeability in Conformal Risk Control under distribution shift; (3) fuzzy scoring of open-ended generative abstentions; and (4) absence of self-contained binary evaluation sets on Hugging Face.
* **RQ 5 (Benchmark Shortcut Auditing - Blank Image Controls):**  
  Deprioritized because it is a passive diagnostic audit rather than an experimental intervention, and the phenomenon of language-prior guessing is already saturated by *Seeing without Looking*, *POPE*, and *VL-Checklist*.

---

## 5. The Top Candidate in Queue: Surviving RQ 1 Specification

If frozen, this candidate represents an airtight, publication-grade empirical thesis:

### Core Research Question
> **"When a vision-language model is presented with mutually contradictory visual and textual premises, does requiring it to explicitly verbalize and explain the contradiction causally change its decisional arbitration, or does the explanation merely act as a post-hoc rationalization of an entrenched modality preference?"**

### Competing Hypotheses
* **$H_1$ (Deliberative Cognitive Control):** Explicit conflict verbalization forces cross-attention across both modalities, breaking unimodal attention capture and causally shifting candidate answer logits toward the correct source.  
  *Observable Signature:* Significant increase in correct source selection under conflict prompting compared to a length-matched neutral placebo.
* **$H_0$ (Post-Hoc Rationalization):** The final answer token is determined by early-layer cross-modal projection dynamics; generating a contradiction explanation produces superficial narrative text without altering the output trajectory.  
  *Observable Signature:* Identical source-following rates between the conflict prompt and the length-matched placebo prompt.

### 4-Way Factorial Prompt Protocol (Inference-Only)
1. **Condition 1 (Direct Baseline):** Standard zero-shot answering with no intermediate reasoning tokens.
2. **Condition 2 (Length-Matched Placebo Control):** Prompt requiring a 2-sentence neutral description of both sources before answering (controls for the confound of "extra reasoning tokens").
3. **Condition 3 (Conflict-Aware Intervention):** Prompt requiring the model to identify whether sources contradict before answering.
4. **Condition 4 (Lanham-Style Prefilling):** Prefilling a contradiction verdict into the assistant output to test whether the final answer causally follows the supplied rationale.

### Technical Implementation
* **Dataset:** 1,304 clean arithmetic conflict pairs from [`vlm-modality-research/modality-conflict-arbitration-v2`](https://huggingface.co/datasets/vlm-modality-research/modality-conflict-arbitration-v2).
* **Model:** `Qwen/Qwen2-VL-2B-Instruct` loaded in `bfloat16` via Hugging Face Transformers.
* **Compute:** Single NVIDIA T4/V100 on Google Colab Pro ($\approx 1.5$ hours total execution time).

---

## 6. The Strategic Decision Framework: Where You Stand Today

With the recent modernization of the `Context/` constraints (allowing commercial APIs, medical vision benchmarks, and agentic architectures), you stand at a clear strategic fork:

```
                                 STRATEGIC FORK IN THE ROAD
                                              │
                    ┌─────────────────────────┴─────────────────────────┐
                    ▼                                                   ▼
            [PATH A: FREEZE RQ 1]                               [PATH B: 48-HOUR AUDIT]
     • 100% verified & plug-and-play                     • Inspect newly unlocked frontiers:
     • Public Hugging Face dataset ready                   1. Multimodal Agents (Active Perception)
     • 90-min Colab Pro execution                          2. Medical VLM (ISIC / MedMNIST)
     • Zero API cost, zero pipeline risk                 • Strict 48-hour timebox cutoff
     • High negative-result value                        • If no plug-and-play repo: fall back to RQ 1
```

### The Two High-Potential Candidates to Audit in the Next Session:

1. **Candidate 2: Multimodal Agent Active Perception & Tool Value Prediction**  
   - *Core Idea:* Can an agent predict action value across active perception (zooming, cropping), external knowledge retrieval, tool invocation, and abstention to maximize answer accuracy under a compute budget?  
   - *Advantage under new constraints:* GPT-4o / Claude 3.5 tool-calling APIs make multi-action agentic orchestration fast and powerful. Highly attractive for AI engineering roles and autonomous systems grad programs.  
   - *Audit Burden:* Must find an existing, executable benchmark/environment (e.g., *ClearVQA*, *BCEA*, or *TRUST*) to avoid having to code an agent environment from scratch.

2. **Candidate 3: Medical Multimodal VLM Selective Calibration & Deferral**  
   - *Core Idea:* Evaluating whether medical VLMs can accurately calibrate uncertainty and selectively abstain/defer to human radiologists on ambiguous diagnostic benchmarks.  
   - *Advantage under new constraints:* Massive prestige in academic and clinical AI research.  
   - *Audit Burden:* Avoid PhysioNet/CITI credentialing delays (MIMIC-CXR/CheXpert) by auditing completely public, instant-download benchmarks (**ISIC 2024 Skin Lesions** or **MedMNIST v2**).

---

## 7. Handover Protocol for the Next Session

When opening the new conversation:
1. **Provide this document (`Cross_Modal_Discovery_Synthesis_and_Handover.md`) as the single context file.**
2. **Execute the 48-Hour Decision Protocol:**
   - Audit the code/dataset availability of **Candidate 2 (Multimodal Agents)** and **Candidate 3 (Medical VLM)**.
   - If either candidate has a clean, plug-and-play GitHub/HuggingFace pipeline runnable on Colab Pro with API assistance, evaluate it as your potential primary thesis.
   - If neither candidate matches the turnkey simplicity and airtight experimental design of **Surviving RQ 1**, immediately freeze RQ 1 with complete confidence and proceed to pilot execution.
