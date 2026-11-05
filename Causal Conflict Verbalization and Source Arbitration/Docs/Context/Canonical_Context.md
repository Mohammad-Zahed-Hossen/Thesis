# Canonical Thesis Context & Research Operating System

**Single Source of Truth for Undergraduate AI/CSE Thesis Research**

- **Principal Researcher:** Mohammad Zahed Hossen (Technical Lead, Final-Year BSc CSE, Bangladesh)
- **Document Status:** Canonical Project Baseline & Operational Ground Truth (Topic Frozen & Empirically Validated across Full Population N=1,619)
- **Effective Horizon:** Academic Year 2026–2027 (Updated 24 September 2026)
- **Project Parent Field:** Multimodal / Vision-Language Learning and Systems (**FROZEN**)
- **Active Primary Subfield:** Trustworthy, Grounded, and Reliable Generative MLLMs
- **Locked Primary Research Topic:** Causal Conflict Verbalization and Source Arbitration in Vision-Language Models (**FROZEN & EMPIRICALLY CONFIRMED**)
- **Target Model & Hardware Stack:** `Qwen/Qwen2.5-VL-3B-Instruct` on Google Colab Pro (NVIDIA T4 / V100 GPU, FP16 Tensor Cores, PyTorch 2.0 SDPA, CUDA 13.0)
- **Active Research Stack & Tools:** **Gemini** (Deep Research & Frontier Validation), **alphaXiv** (Direct arXiv Analysis), **OpenResearch** (Complex Literature Synthesis). *(Note: Claude and Perplexity are formally retired / not used).*

---

# 1. AI Assistant Ingestion Guide & Operating Directives

When any AI model (or the researcher) ingests this document, it must immediately adopt the following persona and behavioral boundaries:

1. **Role Definition:** You are an evidence-discovery, verification, research-design, and thesis decision assistant. You are **not** a generic ideation bot, cheerleader, or application brainstormer.
2. **Standard of Scientific Rigor:** Treat thesis research as an evidence-building process:
   $$
   \text{Problem} \longrightarrow \text{Closest Work} \longrightarrow \text{Unresolved Uncertainty} \longrightarrow \text{Research Question} \longrightarrow \text{Dataset} \longrightarrow \text{Baseline} \longrightarrow \text{Controlled Experiment} \longrightarrow \text{Direct Metric} \longrightarrow \text{Interpretation} \longrightarrow \text{Contribution}

   $$
3. **No Incremental or Superficial Suggestions:** Do **not** propose generic chatbots, simple CRUD applications, boilerplate RAG pipelines, standard transfer learning, "applying Model X to Dataset Y," or claiming novelty merely by swapping a dataset to Bengali/regional imagery without a core algorithmic or cognitive mechanism.
4. **Strict Epistemic Taxonomy:** In every analysis, explicitly categorize claims:
   - **Verified:** Directly proven by a primary peer-reviewed source or checked codebase/dataset.
   - **Inferred:** A logical deduction derived from multiple verified facts.
   - **Hypothesis:** An unproven scientific proposition that our experiment is designed to test.
   - **Unknown:** Information that current searches and available records have not established.
   - **Historical Decision:** What was previously decided in past notes (subject to revision under new primary evidence).
5. **No Premature Reopening of Parked Fields:** Do not casually suggest Federated Learning, Medical Imaging, or Diffusion Models. Respect the adversarial audit history that parked them (see §5).
6. **No Fake Gaps or Hallucinated Citations:** Never invent papers, dataset names, or GitHub links. Never claim "no one has studied X" unless bounded by a specific search. Differentiate between an *unstudied gap* and an *occupied engineering domain with different terminology*.

---

# 2. Researcher Profile & Feasibility Boundaries

### 2.1 Academic & Technical Profile

- **Institution & Stage:** Final-year BSc in Computer Science and Engineering (CSE), Bangladesh.
- **Role:** Technical Lead of a 3-person undergraduate thesis group. The principal researcher is responsible for all core research ideation, mathematical formulation, PyTorch/Hugging Face pipeline development, experimental execution, and academic manuscript drafting.
- **Core Competencies:** Python, PyTorch, TensorFlow, classical machine learning, deep learning, CNNs, Transformers, LLM/VLM fundamentals, Hugging Face ecosystem, evaluation pipeline engineering, and web/API development (FastAPI/Django).
- **Primary Objectives:** Build publication-grade research capabilities, produce a defensible CSE undergraduate thesis, create tangible end-to-end AI engineering artifacts, and maintain a competitive profile for funded graduate admissions and elite AI engineering roles.

### 2.2 Hard Feasibility & Computational Constraints

All experimental designs must pass these strict feasibility filters:


| Dimension                   | Canonical Constraint & Boundary                                                                                                                                                                                                                                           |
| :---------------------------- | :-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| **Local Hardware**          | AMD Ryzen 5 5600G (6 cores / 12 threads), 8 GB RAM, integrated graphics (no local CUDA acceleration). Strictly reserved for code editing, lightweight data inspection, prompt engineering, and git operations.**Zero heavy model training locally.**                      |
| **Primary GPU Environment** | **Google Colab Pro** (NVIDIA T4 16GB, V100 16GB, and occasional A100 access). All baseline runs, inference passes, and lightweight fine-tuning must fit within a single 16 GB VRAM envelope.                                                                              |
| **Model Scale Limits**      | Compact open-weight foundation models:**2B to 3B parameters** (e.g., `Qwen/Qwen2-VL-2B-Instruct`, `Qwen/Qwen2.5-VL-3B-Instruct`) running in `bfloat16` or 4-bit quantization. Models $\ge 7\text{B}$ are restricted to pure inference or API access.                      |
| **Compute Paradigm**        | **Inference-First, Controlled Factorial Interventions, and Mechanistic Probing.** Full foundation model pretraining from scratch is completely out of scope. Parameter-Efficient Fine-Tuning (PEFT/LoRA/QLoRA) is permitted only when strictly necessary.                 |
| **Budgeted Frontier APIs**  | Commercial APIs (Gemini 1.5 Flash/Pro, GPT-4o) are approved and budgeted exclusively for: (a) reference teacher baselines, (b) cross-architecture validation, and (c) deterministic verification. Total API expenditure per experiment must remain$<\$5.00$.              |
| **Data Accessibility**      | **100% Public, Legal, and Instantly Accessible.** Zero dependence on private clinical partnerships, hospital NDAs, manual institutional credentialing (e.g., PhysioNet/Synapse approvals), web scraping subject to dynamic DOM drift, or proprietary enterprise datasets. |
| **Supervision Assumption**  | Self-directed research velocity. The project cannot rely on continuous day-to-day supervisor steering or specialist human annotation.                                                                                                                                     |

---

# 3. Scientific Research Standards & Evaluation Framework

### 3.1 The Three Levels of Research Contributions

Examiners and top-tier venues (NeurIPS, ICML, CVPR, ACL) evaluate work according to an implicit hierarchy:

```
[Level 1: Passive Prediction & Leaderboard Chasing]  <-- REJECTED / BANNED
  • "We trained Model A and Model B on Dataset C; Model A scored 74% and Model B scored 69%."
  • Zero mechanistic insight. Pure engineering report. Unpublishable.

[Level 2: Uncontrolled Benchmark Collection]          <-- REJECTED / INSUFFICIENT
  • "We gathered 500 new images from our local area and tested off-the-shelf models."
  • Confounded by annotation noise, lack of controlled hypotheses, and shallow novelty.

[Level 3: Causal Mechanism Discovery & Explanatory Audit] <-- CANONICAL STANDARD
  • We formulate competing scientific explanations for a known failure mode.
  • We surgically intervene in the reasoning trace or internal activation stream using strict
    placebos and counterfactual controls to isolate genuine causes from measurement artifacts.
  • The work produces high scientific value REGARDLESS of whether the hypothesis is confirmed.
```

### 3.2 What Makes a Valid Thesis Candidate

Every proposed experiment must satisfy seven hard criteria:

1. **Concrete Problem:** Identifies a specific model failure mode, behavioral illusion, or representation bottleneck.
2. **Falsifiable Question with Competing Explanations:** The research question must pit two legitimate hypotheses ($H_1$ vs. $H_0$) against each other. The experiment must be capable of rejecting either.
3. **Leakage-Resistant Data Split:** Samples must be stratified by underlying entities, original source images, or templates. Correlated variants or translations must never leak across splits.
4. **Reproducible Baseline:** At least one strong, open-source model pipeline runnable in $<100$ lines of clean PyTorch/Transformers code on Colab Pro.
5. **Length-Matched Placebo & Structural Controls:** Whenever testing a prompt or reasoning intervention, the protocol must include a **neutral placebo condition** matched for token length and generation budget to rule out the trivial confound of extra test-time compute.
6. **Direct, Deterministic Metrics:** Evaluation must rely on deterministic exact match, regex mathematical extraction, or verified labels. Avoid subjective, uncalibrated LLM-as-a-judge scoring whenever possible.
7. **High-Value Negative Result:** If the proposed mechanism fails or shows no effect, the finding must still constitute a publication-grade scientific rebuttal (e.g., proving that a celebrated capability is merely a measurement artifact or post-hoc rationalization).

---

# 4. Global Structural Taxonomy & Topic Hierarchy

### 4.1 Structural Mind Map of the Research Space

```text
MULTIMODAL / VISION-LANGUAGE LEARNING AND SYSTEMS (FROZEN PARENT FIELD)
│
├── 1. Primary Research Lane: Trustworthy and Reliable VLMs
│   ├── Grounding & Evidence Reliance
│   │   ├── Modality Dominance & Bias (Image vs. Text Prioritization)
│   │   └── Visual Token Utilization Decay across Autoregressive Generation
│   ├── Conflict & Inconsistency
│   │   ├── Cross-Modal Contradiction (Conflicting Sensory Inputs)
│   │   └── [LOCKED PRIMARY TOPIC]: Causal Conflict Verbalization & Source Arbitration
│   ├── Explanatory Faithfulness & Reasoning Mechanics
│   │   ├── Cognitive Control vs. Post-Hoc Rationalization in Multimodal CoT
│   │   └── [RESERVE PROPOSAL 1]: Reasoning Trace Degradation (Causal vs. Softmax/RoPE Dilution)
│   └── Uncertainty Calibration & Selective Abstention
│
├── 2. Secondary Research Lane: Generalization, Adaptation & Distribution Shift
│   ├── Multimodal Representation Alignment & Feature Binding
│   │   ├── Object-Attribute Spatial Binding in Cluttered Natural Scenes
│   │   └── [RESERVE PROPOSAL 2]: Visual Binding IDs Natural-Transfer Audit
│   └── Cross-Domain & Cross-Lingual Evaluation
│
├── 3. Active Exploratory Lane: Multimodal Agents & Decision Reliability
│   ├── Active Perception (Dynamic Zooming, Cropping, Sub-view Selection)
│   └── [RESERVE PROPOSAL 3]: Disentangling Tool Utility from Test-Time Compute in ActiView
│
└── 4. Supporting / Conditional Lane: Efficient and Scalable VLMs
    ├── Visual Token Pruning & Context Compression (Supporting mechanism only)
    └── Parameter-Efficient Fine-Tuning (PEFT / QLoRA)
```

### 4.2 Core Concepts in Plain English


| Concept                              | Plain-English Definition                                                                                                         | Critical Distinction (What It Is NOT)                                                      |
| :------------------------------------- | :--------------------------------------------------------------------------------------------------------------------------------- | :------------------------------------------------------------------------------------------- |
| **Visual Grounding**                 | The model's answer is causally driven by the relevant visual features in the image.                                              | Giving the correct answer by exploiting language priors or statistical scene correlations. |
| **Scene Truth vs. Answerability**    | The image contains sufficient, uncorrupted visual evidence to resolve the query.                                                 | Whether a specific model guesses correctly despite degraded or missing pixels.             |
| **Modality Dominance**               | The systematic tendency of a VLM to default to text tokens over visual tokens (or vice versa) during conflict.                   | Symmetrical, balanced cross-modal fusion.                                                  |
| **Native vs. Verbalized Confidence** | Output logit softmax probability ($p_{\max}$) vs. the model explicitly stating *"I am 90% sure"*.                                | Verbalized confidence is generated text and frequently exhibits extreme miscalibration.    |
| **Calibration vs. Accuracy**         | Stated probability matches the empirical likelihood of being correct across a cohort.                                            | High overall accuracy. A model can be 95% accurate but severely uncalibrated.              |
| **Reasoning Faithfulness**           | Intermediate chain-of-thought tokens causally steer the final decision.                                                          | Post-hoc storytelling that rationalizes an answer already locked in by early layers.       |
| **Softmax Dilution ($M/N$)**         | Self-attention weights must sum to 1. As text length$N$ grows, the share of attention to $M$ image tokens decays mathematically. | A cognitive failure or genuine neural forgetting of visual evidence.                       |
| **Visual Binding**                   | Correctly associating an object's spatial location with its semantic properties (e.g., "red car" vs. "blue truck").              | Independent detection of classes and colors without relational pairing.                    |

---

# 5. Historical Research Evolution & Parked Fields Dossier

Between August and September 2026, twelve exploratory fields and dozens of candidate questions were systematically audited. Below is the permanent decision record of why specific domains were parked or rejected.

```
                           HISTORICAL AUDIT & DISCOVERY FUNNEL
                                            │
   ┌──────────────────────┬─────────────────┴─────────────────┬──────────────────────┐
   ▼                      ▼                                   ▼                      ▼
[Medical Imaging]     [Federated Learning]              [Multimodal Agents]    [Bengali VQA Repair]
• ISIC/HAM10000       • FeTS-2022 Synapse Gating        • Broad Gating Occupied• Answer Leakage
  Data Leakage        • Synthetic Dirichlet Discredited   (AdaTooler, ToolGate)• Severe Manual
• Clinical Viva Trap  • Shahid (2026) Solved Shrinkage  • RL Training Fails      Annotation Burden
  (No Clinician)        (Fed-CRC-Seg Pre-emption)         on Colab (OOM)       • Non-Orthogonal
       │                      │                                   │                      │
       ▼                      ▼                                   ▼                      ▼
 [PARKED/REJECTED]      [PARKED/REJECTED]                   [RESERVE ONLY]         [PARKED/DEFERRED]
```

### 5.1 Federated Learning (FL) — **PARKED / REJECTED**

- **The Pitched Ideas:** Site-conditional conformal risk control on FeTS-2022; Federated LoRA of medical VLMs.
- **Why It Was Rejected:**
  1. *Core Gap Pre-Empted:* Shahid (*Fed-CRC-Seg*, June 2026, `arXiv:2606.20115`) already established that pooled conformal calibration violates coverage across clinical sites and proved empirical Bayes risk-curve shrinkage ($n_0=19$) on FeTS-2022. Extending this to partial client participation is an incremental parameter sweep.
  2. *Fatal Infrastructure Gate:* Genuine multi-institutional data exists only in FeTS-2022 (3D mpMRI), which is gated behind manual Synapse administrative approval (`syn28546456`) with documented multi-week delays.
  3. *Methodological Discredit:* Artificially partitioning 2D datasets using Dirichlet label distributions ($\alpha=0.1$) was proven scientifically invalid by *Neurocomputing 2026 (`doi:10.1016/j.neucom.2026.135005`)*, showing synthetic partitions produce ranking artifacts that do not replicate on authentic multi-center clinical cohorts.
  4. *Engineering Debt:* Debugging distributed simulation frameworks (Flower/Ray) on Colab Pro leads to severe timeline collapse.

### 5.2 Medical Image Analysis (Standalone / Non-VLM) — **PARKED / REJECTED**

- **The Pitched Ideas:** Selective classification (AUGRC) under sensor shift (ISIC 2020 dermatoscope $\to$ PAD-UFES smartphone camera); post-hoc shortcut recalibration.
- **Why It Was Rejected:**
  1. *The "Medical Imaging Is Not Enough" Trap:* Fails to provide an AI/CSE algorithmic contribution. It merely applies an existing metric (Traub et al., NeurIPS 2024, `arXiv:2407.01032`) to existing image datasets.
  2. *Catastrophic Data Contamination:* Public dermatology archives have massive hidden leakage (ISIC 2019 completely subsumes HAM10000; ISIC 2020 has 425 duplicate images across patients; PAD-UFES has distinct biopsy-verification standards). A student team would burn 8 weeks on manual deduplication.
  3. *CS Viva Vulnerability:* CSE examiners inevitably ask: *"Did you validate this with a certified clinician? How did you correct for biopsy-selection bias?"* If answered with *"This is an evaluation of Traub's metric,"* examiners retort: *"Then why evaluate it on messy medical data instead of standardized CV benchmarks?"*

### 5.3 Multimodal Agents (Constructive RL / Browser Environments) — **PARKED / RESERVE**

- **The Pitched Ideas:** Training agents to predict action-value across zooming, cropping, and tool execution before taking the action.
- **Why Constructive Builds Failed:**
  1. *Literature Saturation:* The broad question is fully occupied by 2025–2026 primary literature: *AdaTooler-V* (`arXiv:2512.16918`) explicitly optimizes sample-level Tool Benefit Scores $\Delta S = S^+ - S^-$; *ToolGate* (`arXiv:2606.03054`) trains pre-call gating controllers; *CAM-DF* (`arXiv:2607.27083`) formalizes decision-focused stopping.
  2. *Compute & Stability Wall:* Training 7B+ RL policies via PPO/GRPO triggers immediate CUDA OOMs on Colab Pro. Browser agent harnesses (Playwright, Docker, live Web APIs) suffer from software drift, rate limits, and non-deterministic timeouts.
  3. *Surviving Niche:* Only a pure diagnostic confound audit on [ActiView](https://github.com/THUNLP-MT/ActiView) survives (see Reserve Proposal 3).

### 5.4 Bengali Cultural VLM Repair — **PARKED / DEFERRED**

- **The Pitched Ideas:** 3-way factorial intervention (Visual, Linguistic, Cultural Knowledge) on Bengali cultural VQA (BanglaVerse).
- **Why It Was Deferred:**
  1. *Intervention Non-Orthogonality:* A textual visual description is itself language; hints frequently leak the answer directly, confounding perception with answer injection.
  2. *Severe Annotation Overhead:* Requires qualified native dialect speakers and cultural scholars to independently verify hundreds of counterfactual prompts.
  3. *Local Benchmark Limitation:* Does not investigate fundamental multimodal architecture mechanics.

### 5.5 Diffusion Models & Standalone AI Image Generators — **REJECTED**

- Standalone diffusion training requires massive GPU resources. Building a web UI wrapper around an existing diffusion checkpoint is an engineering application, not an academic thesis.

### 5.6 Master Audit Dossier of All 12 Candidate Fields & 5 Detour Areas

For permanent reference and historical audit continuity, below is the status and controlling rationale for all 12 candidate domains investigated across the project's history:


| Domain                                 | Historical Status       | Controlling Rationale for Status                                                                                    | Possible Relation to VLM Thesis              |
| :--------------------------------------- | :------------------------ | :-------------------------------------------------------------------------------------------------------------------- | :--------------------------------------------- |
| **1. Trustworthy & Reliable VLMs**     | **ACTIVE (PRIMARY)**    | Foundational, high scientific depth, 100% turnkey public datasets, fits single Colab Pro GPU.                       | Primary thesis home.                         |
| **2. VLM Shift & Adaptation**          | **ACTIVE (SECONDARY)**  | Directly probes multimodal representation robustness under natural/synthetic distribution shift.                    | Secondary analysis / Reserve home.           |
| **3. Multimodal Agents & Tool Use**    | **ACTIVE (AUDIT ONLY)** | Constructive RL tool policies are pre-empted/infeasible; diagnostic compute confound audit survives.                | Reserve Proposal 3 (ActiView).               |
| **4. Efficient & Scalable VLMs**       | **SUPPORTING ONLY**     | Token pruning/compression is valid only as an analytical lens or mechanism, not an isolated thesis.                 | Supporting mechanism only.                   |
| **5. Medical Image Analysis (2D)**     | **PARKED / REJECTED**   | Fails CSE novelty (applies Traub's metric to known shift); severe ISIC/HAM10000 data contamination; viva trap.      | Incompatible without clinical co-supervisor. |
| **6. Federated Learning (FL)**         | **PARKED / REJECTED**   | Core conformal shrinkage solved by Shahid (June 2026); FeTS-2022 gated by Synapse; synthetic Dirichlet discredited. | Incompatible with Colab constraints.         |
| **7. Standalone Diffusion Training**   | **REJECTED**            | Pretraining/fine-tuning requires massive multi-GPU clusters; wrapper apps lack CSE scientific depth.                | Incompatible with Colab constraints.         |
| **8. Standalone Cybersecurity**        | **PARKED**              | Network intrusion detection lacks domain supervision, has poor ground-truth labels, and diverges from MLLMs.        | Excluded application domain.                 |
| **9. 3D Vision / NeRF / Splats**       | **PARKED**              | Coordinate geometry, rendering tooling, and preprocessing add steep learning curves unnecessary for MLLMs.          | Excluded.                                    |
| **10. Physical Robotics & Embodiment** | **PARKED**              | Hardware dependence and physical simulation gaps prevent credible undergraduate experimental validation.            | Excluded.                                    |
| **11. Autonomous Driving**             | **PARKED**              | Industrial-scale multi-sensor data requirements and safety certification out of scope for undergraduate team.       | Excluded.                                    |
| **12. Bengali Cultural VQA Repair**    | **PARKED / DEFERRED**   | Non-orthogonal interventions (text hints leak answers); extreme manual cultural annotation overhead.                | Deferred regional study.                     |

**The 5 Detour Areas (Officially Parked via Instruction U1):**

1. *Continual / Lifelong Learning in VLMs:* Catastrophic forgetting benchmarks suffer from non-standard rehearsal budgets.
2. *External Memory Systems (Retrieval-Augmented Memories):* Engineering-heavy key-value caching without deep architectural insights.
3. *Long-Context Retrieval & Needle-in-a-Haystack:* Pre-empted by frontier models (Gemini 1.5 Pro); synthetic needles lack cognitive depth.
4. *Test-Time Planning & Tree Search (MCTS/Search-over-Thought):* Massive multi-pass inference cost collapses on Colab Pro limits.
5. *Multi-Image Temporal Reasoning:* Video benchmark processing and frame-extraction pipelines exceed single-GPU memory limits.

---

# 6. Locked Primary Thesis Topic Specification

## Project Title

**Causal Conflict Verbalization and Source Arbitration in Vision-Language Models**

```
                       PRIMARY RESEARCH PROTOCOL: 4-ARM FACTORIAL
                                           │
                         INPUT: Contradictory Stimulus (Image ≠ Text)
                                           │
         ┌───────────────────┬─────────────┴─────────────┬───────────────────┐
         ▼                   ▼                           ▼                   ▼
    [Arm 1: Direct]     [Arm 2: Placebo]            [Arm 3: Conflict]   [Arm 4: Prefill]
    Direct Answer       Neutral 2-Sentence          2-Sentence Conflict Forced Contradiction
    Zero CoT            Description                 Verbalization       vs. Agreement Rationale
    (T ≈ 10 tokens)     (T ≈ 75 tokens)             (T ≈ 75 tokens)     (T ≈ 75 tokens)
```

### 6.1 Problem Formulation & Intuition ("The Lie-Detector for AI Reasoning")

When an image and accompanying text provide conflicting information, VLMs display strong, prompt-dependent modality arbitration—under unprompted direct conditions, they default heavily to text, whereas requesting a neutral description induces dramatic visual capture.

**The Core Scientific Question:**

> *When a vision-language model receives contradictory visual and textual problems, does an explicit conflict-verbalization intervention causally change its subsequent source arbitration compared with a neutral verbalization control?*

### 6.2 Competing Falsifiable Hypotheses

- **Hypothesis $H_1$ (Deliberative Cognitive Control):** Explicit conflict verbalization and reliability assessment causally steer source selection away from default visual capture, breaking unimodal attentional capture and redirecting multi-step problem solving.
  - *Signature:* Net Visual Reduction $\Delta_{\text{visual}} > 0$ ($p < 0.001$) relative to the length-matched neutral placebo, accompanied by exact-match problem solving inversion.
- **Hypothesis $H_0$ (Post-Hoc Rationalization / Attentional Inertia):** Source selection is entrenched prior to intermediate reasoning. Conflict verbalization generates fluent text without steering the output distribution.
  - *Signature:* $\Delta_{\text{visual}} \approx 0$; source-following distributions under conflict verbalization match the length-matched neutral placebo.

### 6.3 The Primary Literature Anchor & Unoccupied Gap

- **Anchor Paper 1:** *Which Source Wins? Task-Dependent Reliance in VLMs* (`arXiv:2608.17205`, August 2026). The authors evaluated forced-choice reliance across arithmetic and chart tasks. In Section §5 (Limitations), the authors explicitly state:
  > *"our framework measures forced source arbitration under reduced legibility rather than factual reliability or conflict awareness. Consequently, we do not test whether models detect the contradiction, express uncertainty, or abstain."*
  >
- **Anchor Paper 2:** *Lanham et al. — Measuring Faithfulness in Chain-of-Thought Reasoning* (`arXiv:2307.13702`). Pioneered rationale prefilling and truncation exclusively in text LLMs. Has never been applied to cross-modal sensory conflict arbitration.
- **Anchor Paper 3:** *CLASH* (`arXiv:2511.19199`). Evaluated contradiction detection only as an abstention task (*"Cannot answer"*); never tested active resolution or causal arbitration.

### 6.4 The 4-Arm Factorial Experimental Protocol

To eliminate the trivial confound of additional test-time compute (extra reasoning tokens), all evaluations compare four strictly controlled prompt arms on every sample using the frozen production prompts:

1. **Arm 1 (Direct Zero-Shot Baseline):**
   - *Literal Prompt:* `"Look at the image and read the text problem below.\n{text_question}\n\nSolve the problem. Conclude with: #### <answer>\n"`
   - *Token Budget:* 80 tokens. Establishes native unguided modality bias (85.5% Text).
2. **Arm 2 (Length-Matched Neutral Placebo Control):**
   - *Literal Prompt:* `"Look at the image and read the text problem below.\n{text_question}\n\nIn two sentences, neutrally describe what is presented in the image and what is stated in the text without comparing them. Then solve the problem. Conclude with: #### <answer>\n"`
   - *Token Budget:* 200 tokens. Controls for extra forward passes and descriptive preamble (induces 89.5% Visual Capture).
3. **Arm 3 (Conflict Verbalization Intervention):**
   - *Literal Prompt:* `"Look at the image and read the text problem below.\n{text_question}\n\nIn two sentences, state whether the image and the text agree or contradict each other, and explain which source you consider more reliable. Then solve that problem. Conclude with: #### <answer>\n"`
   - *Token Budget:* 200 tokens. Directs conflict evaluation and source reliability (breaks visual capture to 25.8% Visual, 58.9% Text, 13.7% Abstain).
4. **Arm 4 (Lanham-Style Rationale Prefilling):**
   - Assistant output stream is teacher-prefilled with an explicit prefix (20 tokens):
     - *Arm 4a (Prefill Contradiction):* `"The image and text contradict each other because they present different problems. Following the image problem, the answer is: #### "`
     - *Arm 4b (Prefill Agreement):* `"The image and text describe consistent premises. Following the text problem, the answer is: #### "`
   - Directly measures the causal steering power of intermediate tokens on final logits.

### 6.5 Datasets, Models, and Metrics

- **Datasets:**
  1. *Primary Full Population Benchmark:* [`vlm-modality-research/modality-conflict-arbitration-v2`](https://huggingface.co/datasets/vlm-modality-research/modality-conflict-arbitration-v2) (12,952 total examples across 4 degradation levels and 2 channels; exactly **1,619 clean image pairs** [`degradation_level=0`, `channel=image`] containing 1,319 GSM8K and 300 SVAMP conflict items).
  2. *Secondary Generalization Benchmark:* [`vlm-modality-research/chartqa-evidence-conflict-v2`](https://huggingface.co/datasets/vlm-modality-research/chartqa-evidence-conflict-v2) (229 verified ChartQA conflict pairs).
- **Target Model & Hardware Architecture:**
  - Evaluated Model: `Qwen/Qwen2.5-VL-3B-Instruct` (36 Layers, Hidden Size 2048, 16 Heads).
  - Runtime Precision: `torch.float16` with native Turing Tensor Cores (`sm_75` on T4).
  - Attention Kernel: PyTorch 2.0 SDPA (Scaled Dot-Product Attention) fused kernel.
  - Generation Pipeline: 3-tier specialized token budgets (Group 1: 20 tokens for Arms 4a/4b; Group 2: 80 tokens for Arm 1; Group 3: 200 tokens for Arms 2/3), completely eliminating token truncation (0% truncation).
  - Dynamic Linker Patch: Intercepts CUDA 13 integer `image_grid_thw.prod(-1)` NVRTC JIT crashes via CPU fallback.
- **Mathematical Metrics:**
  - *Net Arbitration Shift:* $\Delta_{\text{arb}} = P(\text{Visual Capture} \mid \text{Arm 2}) - P(\text{Visual Capture} \mid \text{Arm 3})$.
  - *Within-Subject Paired Test:* McNemar's Chi-Squared Test ($\chi^2_{\text{McNemar}}$) with continuity correction on discordant pairs.
  - *Effect Sizes:* Relative Risk ($RR$), Odds Ratio ($OR$) with 95% Confidence Intervals, and Cohen's $h$.
  - *Exact Numerical Cross-Over:* Deterministic arithmetic exact-match against ground truth `image_answer` and `text_answer`.

### 6.6 Empirically Confirmed Findings Across Full Population ($N = 1,619$)

The complete population census was executed on Google Colab Pro in 104.5 minutes ($3.87\,\text{s/item}$) and confirmed the central thesis hypothesis ($H_1$):

```
+---------------------------------------------------------------------------------------------------+
|                        FULL POPULATION EXPERIMENTAL RESULTS (N = 1,619)                          |
|                                                                                                   |
|   Arm 1 (Direct Baseline):                13.77% Visual | 85.55% Text |  0.0% Abstain             |
|   Arm 2 (Placebo Control):                89.50% Visual |  8.96% Text |  0.2% Abstain             |
|   Arm 3 (Conflict Verbalization):         25.76% Visual | 58.93% Text | 13.65% Abstain             |
|                                                                                                   |
|   Net Arbitration Shift (Δ_arb):          +63.74 percentage points (p < 0.0001***)                |
|   Odds Ratio (OR):                        24.57 [95% CI: 20.24, 29.83]                            |
|   Cohen's h Effect Size:                  1.4170 ("Very Large" effect; benchmark > 0.8)           |
|   McNemar's Paired Within-Item Test:      χ² = 982.40, p = 1.20 × 10⁻²¹⁵                          |
|   Fisher's Exact Test:                    p = 1.09 × 10⁻³²²                                       |
|   The Smoking Gun Cross-Over:             Arm 2 solves Image 7.6x > Text (35.6% vs 4.7%);         |
|                                           Arm 3 solves Text 3.1x > Image (35.8% vs 11.7%)!        |
+---------------------------------------------------------------------------------------------------+
```

*Full empirical data, checkpoint tables, and LaTeX source are stored in [`Experiment_Result/`](file:///d:/Thesis/Important/Cross%20Modal/Finalize%20Topic/Experiment_Result) and detailed in [`CANONICAL_THESIS_MASTER_REPORT.md`](file:///d:/Thesis/Important/Cross%20Modal/Finalize%20Topic/CANONICAL_THESIS_MASTER_REPORT.md).*

#### 6.7 Threats to Validity & Engineered Safeguards


| Threat to Validity                  | Confound Mechanism                                                                               | Engineered Safeguard                                                                                                             |
| :------------------------------------ | :------------------------------------------------------------------------------------------------- | :--------------------------------------------------------------------------------------------------------------------------------- |
| **Compute / Token Length Confound** | Longer outputs yield better reasoning purely due to additional transformer layer forward passes. | **Arm 2 Placebo:** Enforces strict length matching (~75 tokens) without contradiction semantics.                                 |
| **Instruction-Following Collapse**  | Small 2B models skip explanations and output raw answers or degenerate text.                     | Use 2-shot in-context demonstrations illustrating the required 2-sentence intermediate structure; logit masking.                 |
| **Evaluator Subjectivity**          | LLM judges introduce scoring bias and non-deterministic grading variance.                        | 100% deterministic ground-truth regex parsing on mathematical and categorical exact-match answers.                               |
| **False-Conflict Hallucination**    | Models primed to find contradictions begin hallucinating conflicts in valid data.                | Evaluate model on 500 aligned control pairs; penalize models that report contradictions on congruent inputs.                     |
| **Rigid Modality Fixation**         | Model has a 100% hardcoded preference for text, making deltas unobservable.                      | Filter analysis by items where baseline confidence margin is not saturated, and test reciprocal visual-authoritative conditions. |

---

# 7. Active Reserve Proposals (Pre-Audited Alternatives)

If the primary topic encounters an unexpected failure during the pilot phase, the project pivots immediately to one of two fully specified, pre-audited reserve proposals.

### 7.1 Reserve Proposal 1: Multimodal Reasoning Trace Degradation

- **Project Title:** *Decomposing Multimodal Reasoning Trace Degradation: Causal Reasoning vs. Positional and Attention Dilution Artifacts*
- **The Phenomenon:** As VLMs generate longer chains-of-thought ($T_{\text{CoT}} > 200$ tokens), attention to visual tokens decays and hallucinations spike (*RH-Bench*, NeurIPS 2025; *Remember-R1*, 2026; *VIG*, 2026).
- **The Core Scientific Question:**
  > *When visual evidence utilization declines during extended multimodal reasoning, is the degradation causally driven by the cognitive computation of the reasoning trace, or is it a measurement artifact of Rotary Position Embedding (RoPE) distance and uniform softmax denominator dilution ($M/N$)?*
  >
- **Plain-English Intuition:** *"Did the AI really forget the picture because it was thinking hard, or did attention drop simply because attention must mathematically sum to 100% and adding 500 words naturally dilutes the image's mathematical share?"*
- **Experimental Design:** Teacher-forced prefix slicing on 500 counterfactual pairs from `WhatIfVis`.
  - *Arm 1 (Direct Short):* Prompt + Question $\to$ Direct answer ($T \approx 10$ tokens).
  - *Arm 2 (Long Reasoning Prefix):* Prompt + Question + 150 teacher-forced reasoning tokens $\to$ Predict answer.
  - *Arm 3 (Long Neutral Padding - Softmax Control):* Prompt + Question + 150 neutral non-reasoning tokens (matched for perplexity) $\to$ Predict answer.
  - *Arm 4 (Position-Matched Short - RoPE Control):* 150 neutral tokens prepended *before* image and prompt, advancing absolute RoPE sequence coordinates by 150 positions, followed by direct answer.
- **Mathematical Metrics & Formulations:**
  1. *Counterfactual Image Causal Effect (ICE):* Measured at final answer token $t$ between clean ($I$) and counterfactual ($I'$) images:
     $$
     \text{ICE}_t = \left[ \log \frac{p(a_{\text{vis}} \mid I, q, p_{<t})}{p(a_{\text{prior}} \mid I, q, p_{<t})} \right] - \left[ \log \frac{p(a_{\text{vis}} \mid I', q, p_{<t})}{p(a_{\text{prior}} \mid I', q, p_{<t})} \right]

     $$
  2. *Softmax-Dilution Deviation ($\Delta \text{VIG}_{\text{dev}}$):* Benchmarked against uniform distribution null ($M$ visual patches over $N$ total tokens):
     $$
     \text{Uniform Null} = \frac{M}{N}, \quad \Delta \text{VIG}_{\text{dev}} = \text{AttnMass}(\text{visual tokens}) - \frac{M}{N}

     $$
  3. *Residual Stream Decodability (Availability Probe):* 5-fold cross-validated linear probe on Layer 18 and Layer 30 hidden states $h_L$: $\Delta \text{AUC} = \text{AUC}_{\text{probe}} - 0.5$.
- **Decisive Kill Conditions:**
  - *Kill Condition K1 (Position Collapse):* If Arm 2 (reasoning) and Arm 4 (position-matched) exhibit statistically equivalent ICE drops (TOST $p < 0.05, \theta = \pm 0.05$), the effect is 100% RoPE positional attenuation.
  - *Kill Condition K2 (Dilution Collapse):* If $\Delta \text{VIG}_{\text{dev}}$ slope is flat across sequence length, visual attention decline is purely a mathematical property of softmax normalization.
- **Negative-Result Value:** High-impact rebuttal: proves that "visual forgetting" is an artifact of sequence dilution and positional encoding, invalidating complex RL loss functions designed to fix a non-existent cognitive decay.

### 7.2 Reserve Proposal 2: Visual Binding IDs Natural Transfer Audit

- **Project Title:** *Do Latent Visual Binding Identifiers Survive Beyond Synthetic Grids? A Placebo-Controlled Natural-Image Transfer Audit*
- **The Phenomenon:** ICML 2026 literature (*Grounding IDs*, Hasani et al., `arXiv:2509.24072`) claimed to discover modular "Binding IDs" in intermediate residual streams ($L20\text{--}27$) of Qwen2.5-VL, reporting 98% accuracy in transferring object attributes via activation swapping on synthetic $2 \times 4$ grids.
- **The Core Scientific Question:**
  > *Do the localized residual-stream activation swaps that transfer object-attribute binding in synthetic grid scenes represent genuine, relation-specific binding representations that transfer to natural photographic instances under strict placebo controls, or are they destructive perturbation artifacts induced by artificial geometric scaffolding?*
  >
- **Plain-English Intuition:** *"Did scientists actually discover the neural 'glue' tying colors to objects, or did they just find a toy trick that only works on clean computer drawings and breaks into static noise on real photographs?"*
- **Experimental Design:** Layer 22 residual stream overwrite across 25 synthetic grid scenes vs. 25 natural photographic pairs from `InstaBind-Lite/DSCAM` (dense same-class instances, e.g., two cars).
  - *Arm 1 (Real Swap):* Source object patch activations patched into target bounding box.
  - *Arm 2 (Gaussian Placebo):* Target tokens overwritten with norm-matched random Gaussian noise $\mathcal{N}(0, \sigma^2 \mathbf{I})$.
  - *Arm 3 (Background Placebo):* Target tokens overwritten with activations from an empty background quadrant.
  - *Arm 4 (Intra-Scene Swap):* Swapping Object 1 and Object 2 within the same image.
- **Mathematical Metrics & Formulations:**
  1. *Net Directed Target Flip Rate ($\text{NetFlip}$):*
     $$
     \text{NetFlip} = \text{Flip}_{\text{target}} - \text{Flip}_{\text{non-target}}

     $$
  2. *Linguistic Coherence & Degeneration Score ($\mathcal{D}_{\text{rep}}$):*
     $$
     \mathcal{D}_{\text{rep}} = 1 - \frac{\text{Unique 3-grams}}{\text{Total 3-grams}}

     $$

     (If $\mathcal{D}_{\text{rep}} > 0.40$, classified as destructive perturbation failure).
  3. *Covariate Reduction Model:* Logistic regression isolating binding swap from low-level covariates:
     $$
     \text{Logit}(\text{Success}) = \beta_0 + \beta_1 \Delta_{\text{color}} + \beta_2 \Delta_{\text{patch\_dist}} + \beta_3 \text{Prior}_{\text{unigram}} + \beta_4 \mathbf{1}_{\text{RealSwap}}

     $$
- **Decisive Kill Conditions:**
  - *Kill Condition K4 (Placebo Failure):* If Gaussian noise (Arm 2) or background patches (Arm 3) produce a target flip rate statistically indistinguishable from the real swap (Arm 1), the "Binding ID" is a destructive perturbation artifact.
  - *Kill Condition K5 (Natural Image Collapse):* If NetFlip on natural images falls to $\le 0.10$ or triggers linguistic degeneration ($\mathcal{D}_{\text{rep}} > 0.40$), binding IDs are toy-domain artifacts of synthetic geometric grids.
- **Negative-Result Value:** Landmark corrective paper in ICML/CVPR establishing the mechanistic boundary conditions of multimodal interpretability.

### 7.3 Reserve Proposal 3: Multimodal Agent Active Perception Confound Audit

- **Project Title:** *Disentangling Visual Information Gain from Test-Time Compute in Multimodal Agent Active Perception*
- **The Core Scientific Question:**
  > *When visual tool actions (crop/zoom) appear to improve an agent's answer, does the gain stem from the acquisition of high-resolution visual pixels, or is it an experimental artifact of auxiliary test-time compute (extra forward passes and extended reasoning tokens)?*
  >
- **Benchmark & Protocol:** 300 curated instances from [ActiView](https://github.com/THUNLP-MT/ActiView) (turnkey PIL-based sub-views on Colab Pro).
  - Compares: Direct baseline vs. Compute-matched direct CoT (matching token budget) vs. Active perception agent vs. Masked-observation placebo (agent crops, but crop is replaced with gray mask).
- **Execution:** Pure inference, $\approx 75$ minutes on Colab T4.

---

# 8. Literature & Tooling Strategy

### 8.1 Primary Research Literature Retrieval Stack

The researcher actively utilizes three specialized platforms to ensure rigorous, evidence-grounded literature tracking:

1. **Gemini (Advanced Deep Research):** Used for comprehensive state-of-the-art literature mapping, deep synthesis, identifying conceptual blindspots, and cross-referencing multi-document claims.
2. **alphaXiv:** Used for direct, granular exploration of open-access arXiv preprints, inspecting equations, reading appendices, and examining author commentary.
3. **OpenResearch:** Used for complex academic search queries, citation mapping, identifying foundational lineages, and isolating verified benchmark results.
   *(Retired Tools: Perplexity and Claude are no longer utilized in the active research loop).*

### 8.2 Primary Literature Anchor Registry


| Citation Key        | Formal Title                                                                 | Venue / Identifier                | Core Finding & Significance to Thesis                                                                               |
| :-------------------- | :----------------------------------------------------------------------------- | :---------------------------------- | :-------------------------------------------------------------------------------------------------------------------- |
| **WhichSourceWins** | *Which Source Wins? Task-Dependent Reliance in Vision-Language Models*       | `arXiv:2608.17205` (Aug 2026)     | Proves task-dependent modality dominance; explicitly leaves conflict awareness and verbalization unstudied in §5.  |
| **Lanham2023**      | *Measuring Faithfulness in Chain-of-Thought Reasoning*                       | `arXiv:2307.13702` (2023)         | Formalizes rationale prefilling, truncation, and corruption to test whether CoT is causal or post-hoc in LLMs.      |
| **Turpin2023**      | *Language Models Don't Always Say What They Think: Unfaithful Explanations*  | `arXiv:2305.04388` (NeurIPS 2023) | Demonstrates biased explanations in CoT; CoT rationalizes answer choices without stating true cause.                |
| **CLASH**           | *CLASH: A Benchmark for Cross-Modal Contradiction Detection*                 | `arXiv:2511.19199` (2025)         | Evaluates contradiction detection exclusively as an abstention task; zero active source arbitration.                |
| **RHBench**         | *RH-Bench: More Thinking, Less Seeing? Limits of Long Multimodal Reasoning*  | `arXiv:2505.21523` (NeurIPS 2025) | Demonstrates visual attention decay during long CoT, but confounds reasoning with sequence length and RoPE.         |
| **RememberR1**      | *Remember-R1: Mitigating Long-Context Visual Forgetting in MLLM CoT*         | `arXiv:2608.01314` (Aug 2026)     | Applies RL to prevent visual attention mass decay; treats raw attention as ground truth without dilution controls.  |
| **GroundingIDs**    | *Uncovering Grounding IDs: How External Cues Shape Multimodal Binding*       | `arXiv:2509.24072` (ICML 2026)    | Claims 98% swap accuracy of binding vectors on synthetic grids; lacks Gaussian placebos and natural transfers.      |
| **DSCAM**           | *InstaBind-Lite / DSCAM: Benchmarking Dense Same-Class Attribute Misbinding* | `arXiv:2608.16805` (Aug 2026)     | Evaluates natural image attribute binding on 524 photographs; purely observational, zero activation patching.       |
| **ActiView**        | *ActiView: Active Multimodal Perception Benchmark*                           | `arXiv:2410.04659` (THUNLP)       | Turnkey active perception benchmark; confounds tool-assisted cropping with extra test-time reasoning tokens.        |
| **Traub2024**       | *Evaluating Selective Prediction Metrics (AUGRC)*                            | `arXiv:2407.01032` (NeurIPS 2024) | Mathematically disproves standard AURC; establishes generalized risk-coverage bounds for selective classification.  |
| **FedCRCSeg**       | *Fed-CRC-Seg: Site-Conditional Conformal Risk Control in Medical FL*         | `arXiv:2606.20115` (June 2026)    | Proves pooled conformal calibration violates coverage on FeTS-2022; solves it with risk-curve shrinkage ($n_0=19$). |

---

# 9. Master Comparison of Thesis Candidates


| Candidate                                  | Problem Studied                                                                                      | Literature Gap Certainty                                                 | Dataset & Baseline Readiness                                                  | Experimental Controllability                                              | Compute on Colab Pro                                | Engineering Burden                                                            | Negative Result Value                                                         | Thesis Status          |  |
| :------------------------------------------- | :----------------------------------------------------------------------------------------------------- | :------------------------------------------------------------------------- | :------------------------------------------------------------------------------ | :-------------------------------------------------------------------------- | :---------------------------------------------------- | :------------------------------------------------------------------------------ | :------------------------------------------------------------------------------ | :----------------------- | :- |
| **Primary: Causal Conflict Verbalization** | Does intermediate conflict explanation causally steer VLM decisions or act as post-hoc storytelling? | **100% Open.** Explicitly admitted by *Which Source Wins?* (§6).        | **Turnkey HF:** `modality-conflict-arbitration-v2` (1,619 clean pairs).       | **Flawless:** 4-arm factorial with length-matched neutral placebo.        | Full population completed in 104.5 min on Colab T4. | **Zero:** Complete production harness v3 built.                               | **Outstanding:** Proves CoT is an active causal driver (+63.74 pp shift).     | **FROZEN & VALIDATED** |  |
| **Reserve 1: Reasoning Trace Degradation** | Is visual forgetting in long CoT real cognitive decay or a softmax ($M/N$) and RoPE artifact?        | **Pre-empted.** RH-Bench (NeurIPS 2025) already showed attention decay.  | **Failed:** WhatIfVis not directly downloadable.                              | **High:** Teacher-forced prefix slicing with neutral text padding.        | $\approx 3$ hours on Colab T4 (Qwen2.5-VL-3B).      | **Moderate:** Hooking attention heads and running linear probes.              | **Moderate:** Rebuts published literature on visual forgetting.               | **DEPRECATED**         |  |
| **Reserve 2: Visual Binding IDs Transfer** | Do internal "Binding ID" vectors survive beyond synthetic grids on natural photos?                   | **High.** C1 paper had zero placebos and zero natural image swaps.       | **High:** DSCAM natural images + synthetic 28x28 grid builder.                | **Moderate-High:** Gaussian noise placebo and background patch controls.  | $\approx 2$ hours on Colab T4 (Layer 22 hooks).     | **Moderate:** ViT patch mapping, bounding box slicing, spatial interpolation. | **High Risk:** High probability of complete transfer failure.                 | **RESERVE ONLY**       |  |
| **Reserve 3: ActiView Confound Audit**     | Does active perception gain stem from pixels or test-time compute expansion?                         | **Moderate.** Algorithmic gating occupied; only confound audit survives. | **Turnkey GitHub:** ActiView repo with local sub-views.                       | **Moderate:** Compute-matching direct CoT against tool agent.             | $\approx 75$ mins on Colab T4.                      | **Low:** PIL image cropping and token length budgeting.                       | **Moderate:** Confirms that agent gains reduce to test-time thinking compute. | **PARKED**             |  |
| **Medical Imaging (ISIC $\to$ PAD-UFES)**  | Selective prediction under camera sensor shift.                                                      | **Low / Saturated.** Traub's metric applied to existing shift.           | **Deceptive:** Severe cross-dataset duplicates and label ontology mismatches. | **Low-Moderate:** Confounded by illumination, artifacts, and biopsy bias. | $\approx 5$ hours 2D CNN training.                  | **High:** 6–8 weeks of medical data cleaning and deduplication.              | **Low:** Confirms known OOD degradation.                                      | **PARKED**             |  |
| **Federated Learning (FeTS-2022)**         | Conformal risk control under client drift and dropout.                                               | **Occupied.** Core shrinkage theorem solved by Shahid (June 2026).       | **Fatal Gate:** FeTS-2022 locked behind manual Synapse approval.              | **Low:** Confounded by non-IID partitions and communication latency.      | Fails on Colab (3D MRI U-Net OOM).                  | **Extreme:** Multi-node distributed simulation, memory leaks.                 | **Zero:** Minor parameter variation on Shahid's code.                         | **PARKED**             |  |

---

# 10. Operational Execution Roadmap & Next Immediate Action

```text
                                 UPDATED THESIS OPERATIONAL ROADMAP
                                                 │
  ┌──────────────────────────┬───────────────────┴───────────────────┬───────────────────────────┐
  ▼                          ▼                                       ▼                           ▼
[Phase 1: Diagnostic Pilots][Phase 2: Population Census]            [Phase 3: Deep Analysis]    [Phase 4: Manuscript & Defense]
STATUS: 100% COMPLETE       STATUS: 100% COMPLETE                   STATUS: ACTIVE FROM TOMORROW STATUS: FINAL DELIVERABLE
• Pilot 1 (Free-Form N=20)  • Harness v3 3-group budget             • Stratified error audit    • LaTeX Thesis Drafting
• Pilot 2 (ICL N=20)        • Full N=1,619 execution on Colab       • GSM8K vs SVAMP contrast   • Chapter 1 to 5 writeup
• Autopsy of failure modes  • McNemar χ²=982.40 (p=1.20e-215)       • Qualitative error autopsy • Final Defense Slide Deck
• Placebo baseline isolated • Exact-Match Cross-Over proved         • Frontier cross-eval (API) • Oral Viva Defense rehearsal
```

### The Single Concrete Action to Take Next

> **From tomorrow, transition from empirical data collection to deep thesis analysis and manuscript drafting. Begin with Section 8 of [`CANONICAL_THESIS_MASTER_REPORT.md`](file:///d:/Thesis/Important/Cross%20Modal/Finalize%20Topic/CANONICAL_THESIS_MASTER_REPORT.md): set up the LaTeX project workspace, insert the publication-ready contingency table (`thesis_contingency_table v3.0.tex`), and draft Chapter 3 (Methodology & 4-Arm Protocol) and Chapter 4 (Empirical Results & The Exact-Match Cross-Over).**
