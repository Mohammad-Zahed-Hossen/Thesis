# Canonical AI/ML Research Playbook
## *The Complete Research Operating System: From Phenomenon Discovery to Publishable Science*

---

## Executive Overview & Epistemic Core

Welcome to the **Canonical AI/ML Research Playbook**. This document is designed to serve as your **primary, self-contained research reference manual**. It consolidates, reconciles, and synthesizes the deep methodological knowledge, experimental decision frameworks, stopping heuristics, error triage protocols, and personal thesis lessons distributed across multiple independent research playbooks (including Gemini, Claude, Antigravity, OpenResearch, and Cline sources).

The primary purpose of this playbook is to give you a rigorous, practical operating system for AI/ML research that prevents the single biggest mistake in undergraduate and early-stage research: **spending months searching, reading, comparing, and reconsidering research topics without transitioning decisively into actual experimentation.**

---

### Epistemic Labeling Key
Throughout this playbook, methodological assertions, heuristics, and guidelines are tagged with explicit epistemic labels to distinguish empirical scientific facts from operational recommendations:

* **`[Evidence-backed]`** — Claims supported by published methodology literature, statistical standards, or peer-reviewed empirical studies (e.g., Kapoor-Narayanan data leakage taxonomy, NeurIPS reproducibility guidelines).
* **`[Research-practice synthesis]`** — Established research patterns reconstructed from senior AI/ML researcher workflows and laboratory practices.
* **`[Practical heuristic]`** — Rule-of-thumb operational guidelines designed to accelerate decisions under uncertainty.
* **`[Personal workflow recommendation]`** — Specific operational rules tailored to prevent personal research failure modes (e.g., stopping rules for topic exploration).
* **`[Thesis forensic lesson]`** — Empirical lessons extracted from autopsies of abandoned thesis proposals and real-world project failures.
* **`[Needs verification]`** — Hypotheses or claims that require local experimental probing before being accepted.

---

## Master Table of Contents

- [PART I — UNDERSTANDING RESEARCH](#part-i--understanding-research)
  - [1. What Research Actually Is](#1-what-research-actually-is)
  - [2. How Experienced Researchers Think](#2-how-experienced-researchers-think)
  - [3. Research vs Learning vs Engineering](#3-research-vs-learning-vs-engineering)
  - [4. The Research Concept Ladder](#4-the-research-concept-ladder)
- [PART II — FINDING A RESEARCH QUESTION](#part-ii--finding-a-research-question)
  - [5. Entering a New Research Area](#5-entering-a-new-research-area)
  - [6. Mapping the Research Territory](#6-mapping-the-research-territory)
  - [7. Finding Interesting Phenomena and Problems](#7-finding-interesting-phenomena-and-problems)
  - [8. Types of Research Gaps (The 11 Gap Mechanisms)](#8-types-of-research-gaps)
  - [9. Finding a Genuine Gap](#9-finding-a-genuine-gap)
  - [10. Verifying the Gap (Adversarial Search)](#10-verifying-the-gap)
  - [11. Finding the Closest Existing Work](#11-finding-the-closest-existing-work)
  - [12. Forming a Research Question (The 7 Maturity Levels)](#12-forming-a-research-question)
  - [13. Forming Competing Hypotheses](#13-forming-competing-hypotheses)
- [PART III — ESCAPING ENDLESS TOPIC EXPLORATION](#part-iii--escaping-endless-topic-exploration)
  - [14. Why Researchers Get Stuck Searching](#14-why-researchers-get-stuck-searching)
  - [15. The Collection Trap and Candidate Churn](#15-the-collection-trap-and-candidate-churn)
  - [16. Exploration vs Commitment](#16-exploration-vs-commitment)
  - [17. When Is Literature Search Enough? (Saturation Rules)](#17-when-is-literature-search-enough)
  - [18. Allowed vs Not Allowed Commitment Matrix](#18-allowed-vs-not-allowed-commitment-matrix)
  - [19. Research Decision Gates](#19-research-decision-gates)
  - [20. Kill / Pivot / Narrow / Continue Decision Protocol](#20-kill--pivot--narrow--continue-decision-protocol)
  - [21. The "No More Topic Hunting" Gate](#21-the-no-more-topic-hunting-gate)
- [PART IV — TURNING THE QUESTION INTO RESEARCH](#part-iv--turning-the-question-into-research)
  - [22. Minimum Discriminating Experiments (MDEs)](#22-minimum-discriminating-experiments)
  - [23. Experimental Design and Variables](#23-experimental-design-and-variables)
  - [24. Baselines and the Baseline Hierarchy](#24-baselines-and-the-baseline-hierarchy)
  - [25. Controls and Alternative Explanations](#25-controls-and-alternative-explanations)
  - [26. Dataset and Evaluation Design](#26-dataset-and-evaluation-design)
  - [27. The AI Failure Triad: Leakage, Shortcuts, and Underspecification](#27-the-ai-failure-triad)
  - [28. Reproducibility and Code Integrity](#28-reproducibility-and-code-integrity)
  - [29. Research Engineering Architecture](#29-research-engineering-architecture)
- [PART V — RUNNING RESEARCH AND NAVIGATING FAILURE](#part-v--running-research-and-navigating-failure)
  - [30. Experiment → Evidence → Interpretation](#30-experiment--evidence--interpretation)
  - [31. Systematic Error Analysis](#31-systematic-error-analysis)
  - [32. Unexpected Results: Bug vs Finding Triage](#32-unexpected-results)
  - [33. Value and Recovery of Negative Results](#33-value-and-recovery-of-negative-results)
  - [34. Mandatory Failure-Recovery Protocols (Scenarios 1–8)](#34-mandatory-failure-recovery-protocols)
- [PART VI — TURNING EVIDENCE INTO CONTRIBUTION](#part-vi--turning-evidence-into-contribution)
  - [35. Revising the Research Question](#35-revising-the-research-question)
  - [36. Scope Control and Creep Prevention](#36-scope-control)
  - [37. Research Logs and Decision Tracking](#37-research-logs-and-decision-tracking)
  - [38. What Counts as a Scientific Contribution?](#38-what-counts-as-a-scientific-contribution)
  - [39. From Results to Scientific Explanation](#39-from-results-to-scientific-explanation)
  - [40. Building the Evidence Chain](#40-building-the-evidence-chain)
  - [41. Knowing When Research Is Done](#41-knowing-when-research-is-done)
- [PART VII — THESIS AND PAPER COMPLETION](#part-vii--thesis-and-paper-completion)
  - [42. Thesis Completion Pipeline](#42-thesis-completion-pipeline)
  - [43. Paper Completion Pipeline](#43-paper-completion-pipeline)
  - [44. Reviewer / Adversarial Analysis ("Pre-Mortem")](#44-reviewer--adversarial-analysis)
  - [45. Publication Preparation and Writing Strategy](#45-publication-preparation-and-writing-strategy)
- [PART VIII — THE REUSABLE RESEARCH OPERATING SYSTEM](#part-viii--the-reusable-research-operating-system)
  - [46. Formal Research State Machine](#46-formal-research-state-machine)
  - [47. Practical Research Artifact Templates](#47-practical-research-artifact-templates)
  - [48. Research Control Center](#48-research-control-center)
  - [49. Future Project Bootstrap](#49-future-project-bootstrap)
  - [50. Common Research Failure Modes](#50-common-research-failure-modes)
  - [51. Master Research Pre-Flight Checklist](#51-master-research-pre-flight-checklist)
  - [52. One-Page Research Desk Reference](#52-one-page-research-desk-reference)
- [APPENDICES](#appendices)
  - [Appendix A — Thesis Autopsies](#appendix-a--thesis-autopsies)
  - [Appendix B — Hardware and Execution Boundaries](#appendix-b--hardware-and-execution-boundaries)
  - [Appendix C — Canonical Terminology Map](#appendix-c--canonical-terminology-map)
  - [Appendix D — Source Synthesis and Evidence Base](#appendix-d--source-synthesis-and-evidence-base)

---

# PART I — UNDERSTANDING RESEARCH

## 1. What Research Actually Is

**`[Research-practice synthesis]`** Scientific research in AI/ML is **not** software engineering, nor is it benchmark score optimization ("SOTA chasing").

Engineering asks: *"Does this system meet specified performance requirements?"*
Learning asks: *"Do I understand how this existing method works?"*
Research asks: *"Why does this phenomenon occur, under what exact boundary conditions does it fail, and what falsifiable principle explains its behavior?"*

```text
┌─────────────────────────────────────────────────────────────────────────┐
│                           ENGINEERING APPROACH                          │
│  Goal: Build artifact -> Tune parameters -> Accuracy = 88% -> Deploy.   │
└─────────────────────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────────────────────┐
│                            RESEARCH APPROACH                            │
│  Goal: Test whether mechanism X drives the 88% accuracy or if performance│
│        is an artifact of shortcut learning in visual feature norms.    │
└─────────────────────────────────────────────────────────────────────────┘
```

A result is merely an engineering artifact until it is attached to a **falsifiable claim about a mechanism or a limit**. "We built a model that achieves 91% accuracy" is an artifact. "We prove that the 91% accuracy is driven by background texture shortcuts, and that removing texture features drops accuracy to 52%" is research—it makes a falsifiable claim and survives an obvious adversarial attack.

---

## 2. How Experienced Researchers Think

**`[Research-practice synthesis]`** What separates productive researchers from beginners who wander for months without progress is not raw intelligence, but mental models and operational habits:

1. **Working from Anomalies, Not Broad Fields:** Novices start with broad domains ("I want to work on Large Language Models"). Experts start with specific anomalies ("Why does chain-of-thought prompting degrade performance when spatial coordinate order is inverted?").
2. **Adversarial Prosecutor Mindset:** Novices design experiments to prove their idea works. Experts act as prosecutors trying to prove their own hypothesis wrong using the cheapest possible test.
3. **Cheapest Discriminating Test First:** Before spending weeks training a 70B parameter model, an expert designs a 10-minute synthetic experiment that can discriminate between competing explanations.
4. **Expecting Questions to Evolve:** Experts treat initial research questions as disposable probes. When empirical evidence contradicts the initial premise, experts pivot the question to match the new evidence.

---

## 3. Research vs Learning vs Engineering

**`[Research-practice synthesis]`** Beginners frequently confuse three distinct activities:

| Dimension | Learning | Engineering | Scientific Research |
| :--- | :--- | :--- | :--- |
| **Primary Goal** | Acquire existing mental models | Build reliable target artifact | Uncover new mechanisms or limits |
| **Output** | Notes, tutorials, mastery | Codebase, API, model weights | Falsifiable claims & empirical evidence |
| **Success Metric** | Personal comprehension | System performance & uptime | Claim survival against controls |
| **Failure Meaning** | Misunderstanding to correct | System bug to patch | Scientific discovery / boundary signal |

> **`[Practical heuristic]`** If you spend 3 weeks reading 40 papers without writing an experimental script, you are *learning*. If you spend 3 weeks refactoring a PyTorch training loop to run 15% faster without testing a hypothesis, you are *engineering*. You are only doing *research* when collecting empirical evidence to discriminate between competing hypotheses.

---

## 4. The Research Concept Ladder

**`[Research-practice synthesis]`** Beginners fail most often by trying to conduct research at too high a level of abstraction. To create actionable research, climb down the **Concept Ladder**:

```text
Level 1: Broad Field (e.g., Artificial Intelligence)
  └─ Level 2: Sub-Field (e.g., Multimodal Vision-Language Models)
       └─ Level 3: Research Territory / Paradigm (e.g., VLM Object Hallucination)
            └─ Level 4: Observed Phenomenon / Anomaly (e.g., Hallucination increases under low contrast)
                 └─ Level 5: Verified Research Gap (e.g., Visual feature norm collapse unmeasured in cross-attention)
                      └─ Level 6: Falsifiable Research Question (e.g., Does norm collapse cause text prior dominance?)
                           └─ Level 7: Competing Hypotheses (e.g., $H_A$: Norm Collapse vs $H_B$: Attention Diffusion)
                                └─ Level 8: Discriminating Experiment (e.g., Synthetic contrast step probe)
```

### Concrete Case Study 1: The BatchNorm Myth vs Reality
* **Level 1 (Field):** Deep Learning Optimization
* **Level 2 (Sub-Field):** Normalization Layers in Neural Networks
* **Level 3 (Territory):** Accelerating Convergence in Deep Convolutional Networks
* **Level 4 (Observed Phenomenon):** Batch Normalization (BatchNorm) dramatically accelerates training stability and convergence speed.
* **Level 5 (Verified Gap):** Original authors (Ioffe & Szegedy, 2015) claimed BatchNorm works by reducing **Internal Covariate Shift (ICS)**. However, no paper had directly measured whether ICS actually correlates with gradient predictive stability.
* **Level 6 (Research Question):** Does BatchNorm accelerate training by reducing Internal Covariate Shift, or by smoothing the optimization landscape?
* **Level 7 (Competing Hypotheses):**
  * **$H_A$ (ICS Reduction):** BatchNorm stabilizes internal layer activation distributions, preventing subsequent layers from constantly adapting to shifting distributions.
  * **$H_B$ (Landscape Smoothing):** BatchNorm reparameterizes the optimization problem to make the loss landscape significantly smoother (Lipschitz continuity), stabilizing gradients regardless of distribution shift.
* **Level 8 (Discriminating Experiment - Santurkar et al., 2018):** Inject non-zero, uncalibrated random noise immediately *after* BatchNorm layers. This explicitly re-introduces massive Internal Covariate Shift while preserving the mathematical Lipschitz smoothing properties of the layer.
* **Empirical Outcome:** Networks with injected noise (high ICS) trained just as fast as clean BatchNorm networks, completely falsifying $H_A$ and confirming $H_B$!

---

# PART II — FINDING A RESEARCH QUESTION

## 5. Entering a New Research Area

**`[Practical heuristic]`** When entering an unfamiliar research field:

1. **Find 2 Anchor Survey Papers:** Read recent (last 12–18 months) survey papers to master domain terminology, canonical benchmarks, and taxonomy.
2. **Identify Top 3 Paradigm Papers:** Find the 3 seminal papers that established current state-of-the-art architectures or formulations.
3. **Trace Terminology:** Identify exact technical keywords used by senior authors. Searching generic terms yields noise; searching mechanism terms yields target literature.
4. **Three-Pass Reading Protocol:**
   * **Pass 1 (5–10 mins):** Title, Abstract, Figures, Conclusion. Decision: Keep or discard.
   * **Pass 2 (30 mins):** Introduction, Main Claims, Method Diagram, Key Results.
   * **Pass 3 (Deep execution):** Re-derive equations, inspect code implementation, re-evaluate baselines.

---

## 6. Mapping the Research Territory

**`[Research-practice synthesis]`** Construct a **4-Quadrant Field Map** to structure an unfamiliar territory:

```text
┌───────────────────────────────────────┬───────────────────────────────────────┐
│ QUADRANT 1: Foundational Bedrock      │ QUADRANT 2: Active Frontier           │
│ Classic baseline methods (> 2 years)  │ Top 3–5 direct SOTA competitors       │
│ that established the domain.          │ published in the last 12 months.      │
├───────────────────────────────────────┼───────────────────────────────────────┤
│ QUADRANT 3: Benchmarks & Infrastructure│ QUADRANT 4: Open Tension / Anomalies │
│ Standard evaluation datasets, metrics,│ Unexplained failures, contradictions  │
│ and official evaluation suites.       │ between papers, or edge cases.        │
└───────────────────────────────────────┴───────────────────────────────────────┘
```

---

## 7. Finding Interesting Phenomena and Problems

**`[Research-practice synthesis]`** Strong research questions originate from observed phenomena and failures, not abstract brainstorming:

1. **Failure-Driven:** A top-performing model collapses under simple, realistic perturbations (e.g., rain reflections on asphalt breaking autonomous driving vision).
2. **Contradiction-Driven:** Paper A claims attention entropy regularizes representations, while Paper B proves attention entropy causes representation collapse in deep layers.
3. **Assumption-Driven:** Method X assumes training samples are independent and identically distributed (i.i.d.), but real-world video streams exhibit heavy temporal correlation.
4. **Shortcut-Driven (Clever Hans Effect):** A medical AI model achieves 95% accuracy by detecting hospital watermark tags in image corners rather than lung pathology.

---

## 8. Types of Research Gaps (The 11 Gap Mechanisms)

**`[Evidence-backed]`** A research gap is **not** simply something nobody has tried. It is an unresolved scientific uncertainty.

| Gap Mechanism | Detection Signal | Evidence Required | False Positive Pattern | Verification Protocol | Real AI/ML Example |
| :--- | :--- | :--- | :--- | :--- | :--- |
| **1. Failure-Driven** | SOTA breaks on simple input shifts | Log files of model collapse | Input is out-of-domain noise | Perturb input systematically | Autonomous vision failing on wet road reflections |
| **2. Contradiction-Driven** | Paper A conflicts with Paper B | Conflicting published charts | Different hyperparameter regimes | Re-evaluate both under matched setups | Context length claims in LLM retrieval |
| **3. Assumption-Driven** | Hidden assumption violated | Theoretical proof of violation | Assumption is practically valid | Test performance when assumption fails | Assuming i.i.d. image patches in Transformers |
| **4. Mechanistic** | High performance, unknown cause | Ablation showing component redundancy | Component actually matters | Isolate component via ablation probe | Internal Covariate Shift in BatchNorm |
| **5. Evaluation** | Metric increases, human quality drops | Divergence between metric & human score | Metric is imperfect but correlated | Human alignment audit | BLEU score gaming in translation |
| **6. Robustness** | Clean score high, noisy score zero | Adversarial sensitivity curve | Perturbation is unrealistically severe | Evaluate under natural perturbations | Perturbation sensitivity in Vision Transformers |
| **7. Generalization** | In-domain high, OOD low | Performance drop on domain shift | Shift is completely out-of-scope | Evaluate on 3 OOD datasets | Medical imaging trained on Hospital A vs B |
| **8. Methodological** | Flawed baseline tuning in prior work | Retrained baseline beating SOTA | Baseline was already optimal | Retrain baseline with equal compute | Metric learning baselines beating new losses |
| **9. Replication** | Published code fails to produce result | Multi-seed reproduction failure | Wrong package version used | Re-run with fixed seeds & dependencies | Reinforcement learning seed variance |
| **10. Boundary/Limit** | Method works in regime X, unmeasured in Y | Performance boundary curve | Method works everywhere | Test extreme scaling regimes | Scaling laws breaking at small batch sizes |
| **11. Combination/Extension** | Two methods uncombined | Unresolved interaction mechanism | Obvious combination without insight | Test if combination reveals interaction | Combining LoRA with quantization |

---

## 9. Finding a Genuine Gap

**`[Research-practice synthesis]`** Avoid the trap of "Nobody has done this before." Test your candidate gap against the **Gap Qualification Protocol**:

1. **Non-Triviality Check:** Is the gap unaddressed because it is obvious and uninteresting, or because it presents a real mechanism challenge?
2. **Insight Check:** Will resolving this gap teach us a general principle about model behavior, or merely yield a single metric number?
3. **Feasibility Check:** Can this gap be evaluated using available compute hardware and accessible datasets?

---

## 10. Verifying the Gap (Adversarial Search)

**`[Practical heuristic]`** Before committing to a gap, execute **Adversarial Gap Verification**:

* Search Google Scholar, arXiv, and Semantic Scholar using queries explicitly designed to find papers that have *already solved* your idea.
* Combine mechanism keywords with negative terms:
  * `"[Mechanism Name]" "evaluation failure"`
  * `"[Mechanism Name]" "norm collapse"`
  * `"[Method A]" vs "[Method B]" benchmark`
* If 10 adversarial search variations return 0 direct hits, your gap has survived verification.

---

## 11. Finding the Closest Existing Work

**`[Research-practice synthesis]`** Construct a **Closest-Work Matrix** comparing your proposed work against the top 3 direct competitors:

| Paper | Problem Addressed | Core Assumption | Primary Failure Mode / Limitation | How Your Work Differs |
| :--- | :--- | :--- | :--- | :--- |
| *Smith et al. (2023)* | Object Hallucination | High-contrast inputs | Fails under low light / noise | Tests norm collapse in low contrast |
| *Zhang et al. (2024)* | Attention Shift | Text-only drivers | Requires prompt tuning | Modifies visual encoder directly |
| **Your Work** | Contrast Hallucination | Feature Norm Collapse | To be evaluated via ablation | Mechanistic explanation & plug-in fix |

---

## 12. Forming a Research Question (The 7 Maturity Levels)

**`[Evidence-backed]`** Progress your research question through the **7 Question Maturity Levels**:

```text
Level 0 — Broad Topic ("I want to study VLMs.")
Level 1 — Observed Problem ("VLMs hallucinate objects.")
Level 2 — Identified Phenomenon ("VLMs hallucinate more in dark images.")
Level 3 — Verified Gap ("No paper measures visual token norm collapse under low contrast.")
Level 4 — Formal Research Question ("Does visual token norm collapse cause hallucination under low contrast?")
Level 5 — Falsifiable Hypotheses ($H_A$: Norm Collapse vs $H_B$: Attention Diffusion)
Level 6 — Discriminating Experiment (Synthetic 2-hour contrast step probe)
```

---

## 13. Forming Competing Hypotheses

**`[Research-practice synthesis]`** Never evaluate a single hypothesis ($H_1$: "My method works"). Frame **Competing Hypotheses** to eliminate confirmation bias:

* **$H_A$ (Primary Mechanism):** Improvement is driven by stabilizing visual feature token norms, preventing language priors from overriding visual embeddings in cross-attention layers.
* **$H_B$ (Parameter/Capacity Control):** Improvement is merely due to adding extra trainable parameters and compute capacity to the visual bottleneck.
* **$H_C$ (Regularization Control):** Improvement is caused by implicitly smoothing gradient updates, acting as a simple weight-decay regularizer.

---

# PART III — ESCAPING ENDLESS TOPIC EXPLORATION

## 14. Why Researchers Get Stuck Searching

**`[Thesis forensic lesson]`** Beginner researchers frequently fall into **Exploration Paralysis**:

```text
Find Idea A ──> Search Literature ──> Find Idea B ──> Compare A & B ──> Doubt Both ──> Search Literature ──> Repeat Indefinitely
```

This paralysis occurs because beginners seek **certainty before experimentation**. They want a guaranteed successful outcome before writing code. In research, certainty comes *only* from empirical evidence, never from reading more papers.

---

## 15. The Collection Trap and Candidate Churn

**`[Thesis forensic lesson]`**
* **The Collection Trap:** Accumulating dozens of PDF papers, bookmarking repositories, and organizing folder hierarchies feels like research progress, but is actually **commitment avoidance**.
* **Candidate Churn:** Constantly swapping candidate research questions every 3 days because a newly read paper seems slightly more interesting. Candidate churn mixes up broad fields, tasks, methods, and evaluation settings, creating artificial complexity.

```text
┌──────────────────────────────────────────────────────────────────────────┐
│                          THE COLLECTION TRAP LOOP                        │
│  Read Paper -> Download Code -> Discover Challenge -> Feel Anxious       │
│  -> Search New Topic -> Download 5 New Papers -> Repeat Indefinitely     │
└──────────────────────────────────────────────────────────────────────────┘
```

---

## 16. Exploration vs Commitment

**`[Research-practice synthesis]`** Research requires a strict phase transition from **Exploration** (divergent searching) to **Commitment** (convergent execution):

```text
   EXPLORATION PHASE                        COMMITMENT PHASE
┌──────────────────────┐               ┌────────────────────────┐
│ - Read broad literature│               │ - Freeze research Q    │
│ - Collect anomalies  │  =======>     │ - Build MDE experiment │
│ - Map field topology │ Decision Gate │ - Collect evidence     │
└──────────────────────┘               └────────────────────────┘
```

Commitment does not mean certainty. Commitment means: *The remaining uncertainty is better resolved by experimentation than by reading more papers.*

---

## 17. When Is Literature Search Enough? (Saturation Rules)

**`[Practical heuristic]`** Stop searching literature immediately when you meet the **3 Saturation Rules**:

1. **Citation Closure:** Every new paper you open cites papers you have already read or cataloged.
2. **Method Predictability:** You can accurately predict the baselines, datasets, and evaluation metrics a new paper will use before reading its experimental section.
3. **Competitor Identification:** You can confidently name the top 3 direct competitor papers and explain how your hypothesis differs from theirs.

---

## 18. Allowed vs Not Allowed Commitment Matrix

**`[Personal workflow recommendation]`** Enforce strict operational boundaries depending on project state:

| Activity | Exploration State | Committed State |
| :--- | :--- | :--- |
| Reading survey papers | **ALLOWED** | **FORBIDDEN** |
| Searching for new topic ideas | **ALLOWED** | **FORBIDDEN** |
| Writing Minimum Discriminating Experiment scripts | **ALLOWED** | **MANDATORY** |
| Running benchmark baselines | **FORBIDDEN** | **MANDATORY** |
| Re-evaluating core research question | **ALLOWED** | **FORBIDDEN (Unless MDE falsifies $H_A$)** |

---

## 19. Research Decision Gates

**`[Research-practice synthesis]`** Progress through your project using strict **Decision Gates**:

```text
[Gate 1: Gap Verified] ──> [Gate 2: Closest Work Mapped] ──> [Gate 3: MDE Passed] ──> [Gate 4: Full Commitment]
```

At each gate, evaluate whether to proceed, pivot, or kill the project based on objective empirical evidence rather than emotional attachment.

---

## 20. Kill / Pivot / Narrow / Continue Decision Protocol

**`[Research-practice synthesis]`** When evaluating a candidate direction at a Decision Gate, apply this protocol:

* **KILL Condition:** Baseline already solves the problem; or the exact gap was published yesterday in a top venue. $\longrightarrow$ *Action:* Terminate project.
* **PIVOT Condition:** Main mechanism fails, but uncovers a clear, unexpected failure mode. $\longrightarrow$ *Action:* Re-formulate research question around the new phenomenon.
* **NARROW Condition:** Phenomenon is real, but scope is too broad to evaluate robustly with available compute. $\longrightarrow$ *Action:* Restrict evaluation to a single sub-domain.
* **CONTINUE Condition:** MDE confirms $H_A$ over $H_B/H_C$ with statistical significance. $\longrightarrow$ *Action:* Proceed to full baseline evaluation.

---

## 21. The "No More Topic Hunting" Gate

**`[Personal workflow recommendation]`** Enforce the **14-Day Hard Rule** to eliminate endless topic hunting:

> **The 14-Day Hard Rule:** If you spend 14 consecutive days searching literature and comparing topic ideas without writing an experimental script or testing a pilot sample, you MUST freeze your top candidate question and execute a 48-hour Minimum Discriminating Experiment. No further topic searching is permitted until the 48-hour experiment completes and produces log files.

---

# PART IV — TURNING THE QUESTION INTO RESEARCH

## 22. Minimum Discriminating Experiments (MDEs)

**`[Research-practice synthesis]`** A **Minimum Discriminating Experiment (MDE)** is the smallest, fastest, and cheapest experimental setup that can falsify at least one competing hypothesis while keeping another alive.

```text
┌────────────────────────────────────────────────────────────────────────┐
│                         SLOW APPROACH (Bad)                            │
│ Build full transformer pipeline -> Train on 1M images for 4 days       │
│ -> Evaluate full benchmark -> Discover outcome is uninterpretable.     │
└────────────────────────────────────────────────────────────────────────┘

┌────────────────────────────────────────────────────────────────────────┐
│                         FAST MDE APPROACH (Good)                        │
│ Synthesize 100 perturbed samples -> Measure feature token norms in 5m  │
│ -> Directly confirm or reject $H_A$ vs $H_B$ in 1 hour.                 │
└────────────────────────────────────────────────────────────────────────┘
```

### Characteristics of a Valid MDE:
* **Execution Time:** Runs in under 2 hours on available local GPU or free Colab instance.
* **Minimal Intervention:** Uses synthetic data, toy setups, or frozen pre-trained checkpoints rather than training full models from scratch.
* **Targeted Outcome:** Explicitly discriminates between $H_A$ (Primary Mechanism) and $H_B$ (Parameter/Capacity Control).

---

## 23. Experimental Design and Variables

**`[Evidence-backed]`** Every rigorous AI/ML experiment must explicitly define its variable structure:

* **Independent Variable (IV):** The specific mechanism component you manipulate (e.g., visual token norm stabilization ON vs OFF).
* **Dependent Variable (DV):** The metric measuring the outcome (e.g., Object Hallucination Rate on low-contrast images).
* **Controlled Variables (CV):** Factors held strictly constant across all runs:
  * Model architecture backbones and frozen weights
  * Deterministic random seeds across PyTorch/CUDA
  * Optimizer learning rate schedules and weight decay
  * Prompt templates and tokenization parameters
  * Evaluation sampling temperature ($T=0.0$ for deterministic decoding)

---

## 24. Baselines and the Baseline Hierarchy

**`[Evidence-backed]`** A research claim is invalid if evaluated against weak, untuned, or compute-starved baselines. Adhere strictly to the **Baseline Hierarchy**:

```text
Level 4: Direct SOTA Competitors (Top 2–3 recent papers from top venues)
Level 3: Standard Established Method (Tuned with EQUAL compute and hyperparameter optimization)
Level 2: Ablated Version of Your Method (Your method with the key mechanism removed)
Level 1: Naive / Random Heuristic Baseline (Random guessing, majority class prediction)
```

### Case Study 2: The Metric Learning Baseline Trap (Musgrave et al., 2020)
* **Context:** Over 50 papers published in top venues (CVPR, ICCV, ECCV) claimed massive gains in deep metric learning (e.g., Contrastive Loss, Margin Loss, ArcFace, N-pair Loss).
* **Flaw Discovered:** Authors were comparing their newly proposed losses (which underwent extensive hyperparameter tuning) against standard baselines (e.g., Triplet Loss) using default, untuned hyperparameters from 2015!
* **Scientific Re-evaluation:** Musgrave et al. retrained all classic loss functions using equal hyperparameter search budgets, equal neural network backbones, and equal embedding dimensions.
* **Empirical Outcome:** When baselines were tuned with equal compute, the performance gap between classic Triplet Loss and modern complex loss functions shrank to within random seed noise (< 0.5%), proving that 5 years of reported "SOTA progress" was an artifact of flawed baseline tuning!

---

## 25. Controls and Alternative Explanations

**`[Research-practice synthesis]`** To prove your mechanism is responsible for an observed gain, run explicit **Control Conditions**:

1. **Negative Control:** Test your method in a setup where the mechanism should provide *zero* benefit (e.g., high-contrast images where feature norm collapse does not occur). If your method still shows a gain, the improvement is caused by a general regularizer or artifact, not your hypothesized mechanism!
2. **Placebo / Parameter Control:** Replace your intelligent module with a random projection matrix or parameter-matched MLP. If it performs identically, your specific architectural design is unnecessary.
3. **Data Control / Shuffle Test:** Train or evaluate on randomly shuffled labels. If performance remains above random chance, data leakage or shortcut learning is present in your pipeline.

---

## 26. Dataset and Evaluation Design

**`[Evidence-backed]`** Evaluation design determines whether your results reflect real capabilities or evaluation artifacts:

* **Split Integrity:** Never evaluate on data that shares source domains, time windows, or prompt structures with the training set.
* **Entity-Level Grouping:** Group dataset splits by entity (e.g., all medical images from Patient X must be in Train, never split across Train and Test).
* **Out-of-Distribution (OOD) Test Sets:** Always include at least one evaluation set that tests generalization under distribution shift (e.g., corrupted images, domain shifts, adversarial rephrasings).
* **Metric Sanity:** Never rely on a single aggregate metric (e.g., mean accuracy). Report precision, recall, variance, error distributions, and qualitative failure samples.

---

## 27. The AI Failure Triad: Leakage, Shortcuts, and Underspecification

**`[Evidence-backed]`** When evaluating AI/ML models, be vigilant against the **AI Failure Triad**:

```text
                                  ┌────────────────────────┐
                                  │    AI FAILURE TRIAD    │
                                  └───────────┬────────────┘
                                              │
         ┌────────────────────────────────────┼────────────────────────────────────┐
         ▼                                    ▼                                    ▼
  [1. DATA LEAKAGE]                 [2. SHORTCUT LEARNING]              [3. UNDERSPECIFICATION]
  Test set samples leak into        Model exploits spurious correlation Model parameters achieve identical
  training data or pre-training     (e.g., hospital tags, background    train score but diverge wildly on
  corpora (contamination).          grass pixels) instead of concepts.  out-of-distribution data.
```

### Forensic Mitigation Protocols:
* **For Leakage (Kapoor-Narayanan Taxonomy):** Perform n-gram string matching and feature embedding cosine overlap checks between train and test splits. Audit preprocessing pipelines for test-set statistic leakage (e.g., calculating dataset mean/std across entire dataset instead of train split only).
* **For Shortcuts (Clever Hans Effect):** Evaluate models on background-swapped counterfactual evaluation sets. Apply saliency probes to verify model attention focuses on pathology/concepts rather than background artifacts.
* **For Underspecification:** Train models across 5+ random seeds and report standard deviations. Evaluate performance across multiple distinct OOD test splits.

---

## 28. Reproducibility and Code Integrity

**`[Evidence-backed]`** Unreproducible research is not science. Enforce the following software rules:

1. **Deterministic Random Seeds:** Explicitly set random seeds across PyTorch, NumPy, Python `random`, and CUDA backend deterministic flags:
   ```python
   import random, os, numpy as np, torch
   def seed_everything(seed=42):
       random.seed(seed)
       os.environ['PYTHONHASHSEED'] = str(seed)
       np.random.seed(seed)
       torch.manual_seed(seed)
       torch.cuda.manual_seed(seed)
       torch.backends.cudnn.deterministic = True
       torch.backends.cudnn.benchmark = False
   ```
2. **Environment Locking:** Store complete `environment.yml` or `requirements.txt` with exact pinned version numbers (`torch==2.1.2`).
3. **Commit Hash Logging:** Every experiment output file must automatically save the current Git commit hash (`git rev-parse HEAD`) into its metadata header.

---

## 29. Research Engineering Architecture

**`[Research-practice synthesis]`** Maintain a modular, reproducible **Repository Hierarchy**:

```text
my-research-project/
├── configs/             # YAML configuration files for every run
├── src/
│   ├── models/          # Isolated model architectures & baseline implementations
│   ├── data/            # Data loaders, preprocessing, and leak checks
│   ├── mechanisms/      # Your specific novel mechanism modules
│   └── utils/           # Deterministic seeds, logging, metrics
├── experiments/         # Standalone, runnable experiment execution scripts
├── tests/               # Unit tests for data shapes, loss functions, & gradient flow
├── logs/                # Raw metric outputs, JSON logs, and artifacts
└── RESEARCH_CONTROL_CENTER.md
```

---

# PART V — RUNNING RESEARCH AND NAVIGATING FAILURE

## 30. Experiment → Evidence → Interpretation

**`[Research-practice synthesis]`** Do not confuse raw experimental output with scientific evidence:

* **Raw Output:** Model A achieved 84.2% accuracy; Model B achieved 81.0% accuracy.
* **Evidence:** Model A out-performed Model B by 3.2% on low-contrast samples across 5 random seeds ($p < 0.01$).
* **Interpretation:** Stabilizing feature token norms mitigates performance degradation under visual signal attenuation.

Bridge raw output to interpretation using statistical significance testing ($t$-test or Wilcoxon signed-rank test across seeds) and control conditions.

---

## 31. Systematic Error Analysis

**`[Research-practice synthesis]`** When an experiment completes, do not look only at aggregate scores. Conduct **Manual Error Analysis**:

1. Randomly sample **50 misclassified outputs** (failed images, hallucinated text outputs, incorrect predictions).
2. Manually inspect and categorize every failure into a taxonomy matrix:
   * 40% ambiguous ground-truth labels
   * 35% low-contrast visual norm collapse
   * 20% out-of-vocabulary prompt tokens
   * 5% random noise
3. Plot error category distributions to discover the true underlying model bottlenecks.

---

## 32. Unexpected Results: Bug vs Finding Triage

**`[Research-practice synthesis]`** When an experiment produces surprising or counter-intuitive results, execute the **Bug vs Finding Triage Protocol**:

```text
                            Unexpected Result Detected
                                         │
                   ┌─────────────────────┴─────────────────────┐
                   ▼                                           ▼
         [Possibility 1: BUG]                      [Possibility 2: FINDING]
         - Gradient overflow / NaNs                - Core assumption was wrong!
         - Incorrect data loader split              - Discovered new failure mode
         - Inverted evaluation metric               - Model exploited new shortcut
                   │                                           │
                   ▼                                           ▼
         Fix code and re-run                       Formulate NEW hypothesis!
```

---

## 33. Value and Recovery of Negative Results

**`[Research-practice synthesis]`** A negative result ($H_A$ failed to improve baseline performance) is **not a failed project**. A negative result is valuable science if:

1. You prove *why* the intuitive idea failed using rigorous diagnostic probes.
2. You show that a widely cited paper's claims do not generalize under realistic conditions.
3. You establish a clear boundary condition where existing methods break down.

---

## 34. Mandatory Failure-Recovery Protocols (Scenarios 1–8)

**`[Thesis forensic lesson]`** When research encounters roadblocks, execute these step-by-step recovery protocols containing all required diagnostic items:

### Scenario 1: "I discovered the gap already exists."
1. **Immediate Action:** Freeze all new feature coding immediately. Do NOT delete your codebase!
2. **What NOT To Do:** Do NOT panic, drop your project, or restart from scratch on a new topic.
3. **Diagnostic Questions:** Does the existing paper test under your exact evaluation conditions, datasets, and perturbation regimes?
4. **Evidence To Collect:** Extract their exact claims, dataset splits, code implementation, and reported limitations into your Closest-Work Matrix.
5. **Decision Branches:**
   * *Branch A:* Their evaluation is comprehensive $\longrightarrow$ Execute **Scenario 8 Salvage Audit**.
   * *Branch B:* Their evaluation omitted a critical domain/perturbation $\longrightarrow$ Pivot research question to focus explicitly on that remaining boundary condition.
6. **How To Preserve Work:** Keep your baseline training scripts and data loaders intact.
7. **Kill/Pivot Criteria:** Pivot if a clean boundary exists; Kill only if their code is publicly released and beats your baseline on all splits.
8. **Record Update Rule:** Log the discovered paper in `decision_log.md` and update `RESEARCH_CONTROL_CENTER.md` to state the new narrowed boundary.

### Scenario 2: "My baseline already solves the problem."
1. **Immediate Action:** Audit the baseline for data leakage or metric calculation errors.
2. **What NOT To Do:** Do NOT modify your novel method to artificially beat the baseline.
3. **Diagnostic Questions:** Is the baseline benefiting from shortcut learning or train-test split contamination?
4. **Evidence To Collect:** Calculate train-test n-gram overlap and evaluate baseline on background-swapped counterfactuals.
5. **Decision Branches:**
   * *Branch A:* Baseline contains leakage $\longrightarrow$ Fix leakage; baseline score will drop, restoring the gap.
   * *Branch B:* Baseline genuinely solves clean dataset $\longrightarrow$ Shift evaluation to a harder out-of-distribution (OOD) perturbation split where baseline collapses.
6. **How To Preserve Work:** Retain the baseline as Level 3 benchmark infrastructure.
7. **Kill/Pivot Criteria:** Pivot evaluation split if baseline collapses under OOD; Kill topic if baseline solves OOD splits effortlessly.
8. **Record Update Rule:** Document baseline audit in `decision_log.md`.

### Scenario 3: "My hypothesis is wrong."
1. **Immediate Action:** Run representation probes to measure internal activation distributions.
2. **What NOT To Do:** Do NOT manipulate random seeds or hyperparameter grids to force a false positive.
3. **Diagnostic Questions:** Which competing hypothesis ($H_B$ parameter count or $H_C$ regularization) actually explains the data?
4. **Evidence To Collect:** Collect layer-wise activation norms, gradient variance, and parameter-matched control metrics.
5. **Decision Branches:**
   * *Branch A:* $H_B$ explains performance $\longrightarrow$ Rewrite claim to prove that prior gains in literature were parameter-capacity artifacts.
   * *Branch B:* $H_A$ failed completely $\longrightarrow$ Re-frame paper around explaining *why* the intuitive mechanism fails (negative result paper).
6. **How To Preserve Work:** Convert $H_A$ experimental scripts into ablated control conditions.
7. **Kill/Pivot Criteria:** Pivot research question from "We propose method X" to "We reveal why method X fails."
8. **Record Update Rule:** Log hypothesis falsification in `Hypothesis Sheet` and update `RESEARCH_CONTROL_CENTER.md`.

### Scenario 4: "The experiment is noisy."
1. **Immediate Action:** Plot evaluation metric distributions across 10 random seeds.
2. **What NOT To Do:** Do NOT report results from a single cherry-picked random seed.
3. **Diagnostic Questions:** Is noise driven by small test-set sample size, unpinned seeds, or non-deterministic CUDA operations?
4. **Evidence To Collect:** Calculate standard deviation, standard error of the mean, and confidence intervals ($95\%$ CI).
5. **Decision Branches:**
   * *Branch A:* Test set is too small $\longrightarrow$ Increase evaluation sample size by $5\times$.
   * *Branch B:* CUDA non-determinism present $\longrightarrow$ Set `torch.backends.cudnn.deterministic = True`.
6. **How To Preserve Work:** Retain all multi-seed run logs in `/logs/`.
7. **Kill/Pivot Criteria:** Continue if mean effect size exceeds $2\times$ standard deviation; Narrow scope if variance remains intrinsically unconstrained.
8. **Record Update Rule:** Log variance analysis in `experiment_ledger.csv`.

### Scenario 5: "I discovered a more interesting question during experiments."
1. **Immediate Action:** Record the discovery in your Idea Backlog inside `decision_log.md`.
2. **What NOT To Do:** Do NOT abandon your active experiment loop mid-run to chase the new idea!
3. **Diagnostic Questions:** Can the new question be evaluated using the exact same codebase and data loaders?
4. **Evidence To Collect:** Save checkpoint outputs and failure samples that revealed the new phenomenon.
5. **Decision Branches:**
   * *Branch A:* Active experiment is near completion $\longrightarrow$ Finish active hypothesis test first, then evaluate backlog item.
   * *Branch B:* Active experiment is stuck in a dead-end $\longrightarrow$ Execute formal Pivot Protocol to switch to the new question.
6. **How To Preserve Work:** Save active run checkpoints to `/logs/` before switching configs.
7. **Kill/Pivot Criteria:** Pivot only after active hypothesis is explicitly supported or falsified.
8. **Record Update Rule:** Update active state in `RESEARCH_CONTROL_CENTER.md`.

### Scenario 6: "The project is becoming too large."
1. **Immediate Action:** Execute the Scope Reduction Protocol.
2. **What NOT To Do:** Do NOT try to evaluate 10 models across 15 datasets simultaneously.
3. **Diagnostic Questions:** What is the single core claim required to make this research scientifically complete?
4. **Evidence To Collect:** Identify the primary dataset and the single top competitor baseline.
5. **Decision Branches:**
   * *Branch A:* Multiple backbones cluttering analysis $\longrightarrow$ Freeze backbone to single standard architecture (e.g., ResNet-50 or ViT-B/16).
   * *Branch B:* Too many secondary benchmarks $\longrightarrow$ Move secondary datasets to Appendix / Future Work.
6. **How To Preserve Work:** Move extra benchmark configs to `/configs/backlog/`.
7. **Kill/Pivot Criteria:** Narrow evaluation scope to 1 primary dataset and 1 OOD split.
8. **Record Update Rule:** Document narrowed scope in `RESEARCH_CONTROL_CENTER.md`.

### Scenario 7: "I have spent 14 days exploring and cannot commit."
1. **Immediate Action:** Enforce the 14-Day Hard Rule. Freeze all paper searching!
2. **What NOT To Do:** Do NOT download more papers or search for new topic ideas.
3. **Diagnostic Questions:** Which candidate question in your `Question Ledger` has the highest maturity level?
4. **Evidence To Collect:** Select the candidate with the verified gap and strongest MDE potential.
5. **Decision Branches:**
   * *Branch A:* Candidate has clear MDE $\longrightarrow$ Write a 2-hour MDE script within 48 hours.
   * *Branch B:* No candidate passed gap check $\longrightarrow$ Take top candidate and run adversarial search immediately.
6. **How To Preserve Work:** Save all read PDFs into `/docs/archive/`.
7. **Kill/Pivot Criteria:** Lock state to `PILOT MDE`. No further literature searching permitted until MDE logs exist.
8. **Record Update Rule:** Set state to `PILOT MDE` in `RESEARCH_CONTROL_CENTER.md`.

### Scenario 8: "I already spent months going in the wrong direction."
1. **Immediate Action:** Perform a Research Salvage Audit.
2. **What NOT To Do:** Do NOT delete your codebase, hide previous work, or restart from zero!
3. **Diagnostic Questions:** What code, baselines, data loaders, and literature notes can be reused as infrastructure?
4. **Evidence To Collect:** Audit past experimental logs to identify reliable baseline runs.
5. **Decision Branches:**
   * *Branch A:* Codebase is functional but idea failed $\longrightarrow$ Re-frame past experiments as negative controls proving why the old direction failed (Negative Result Paper).
   * *Branch B:* Baseline is solid, novel method failed $\longrightarrow$ Convert codebase into a new diagnostic benchmark suite testing model limits.
6. **How To Preserve Work:** Preserve all data loading pipelines, evaluation scripts, and baseline checkpoints.
7. **Kill/Pivot Criteria:** Pivot research question to leverage existing codebase infrastructure.
8. **Record Update Rule:** Document salvage plan in `decision_log.md` and reset `RESEARCH_CONTROL_CENTER.md`.

---

# PART VI — TURNING EVIDENCE INTO CONTRIBUTION

## 35. Revising the Research Question

**`[Research-practice synthesis]`** Scientific progress is non-linear. When experimental evidence invalidates your initial premise, update your research question using the **Dynamic Question Revision Protocol**:

```text
Initial Question: "Does mechanism X improve accuracy on task Y?"
      │
      ▼ [Evidence shows mechanism X fails, but uncovers severe token collapse in Layer 8]
Revised Question: "Why does mechanism X induce feature norm collapse in layer 8 during cross-attention alignment?"
```

This pivoting process converts unexpected experimental roadblocks into genuine scientific discoveries.

---

## 36. Scope Control and Creep Prevention

**`[Personal workflow recommendation]`** Prevent **Scope Creep** during experimentation:

* If an exciting idea occurs to you during coding that is not directly required to test your current active hypothesis, **do not implement it immediately**.
* Write it down in your **Idea Backlog** (`decision_log.md`).
* Finish testing your active hypothesis first before evaluating backlog items.

---

## 37. Research Logs and Decision Tracking

**`[Research-practice synthesis]`** Maintain two living text artifacts throughout execution:

### 1. The Experiment Ledger (`experiment_ledger.csv`)

| Run ID | Date | Git Commit | Hypothesis Tested | Changes Made | Primary Metric | Result Status | Artifact Path |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| `EXP-001` | Oct 12 | `a1b2c3d` | $H_0$ Baseline | Baseline ResNet-50 | Acc: 74.2% | Baseline set | `/logs/exp001` |
| `EXP-002` | Oct 12 | `e4f5g6h` | $H_A$ Norm fix | Added norm clamp layer | Acc: 78.5% | $H_A$ supported | `/logs/exp002` |

### 2. The Decision Log (`decision_log.md`)
```markdown
## Decision 2024-10-14: Switching Evaluation Benchmark
- **Context:** Benchmark X contains 15% mislabeled background patches.
- **Decision:** Switch primary evaluation to Benchmark Y.
- **Evidence:** Manual audit of 100 samples in Benchmark X revealed label ambiguity.
```

---

## 38. What Counts as a Scientific Contribution?

**`[Evidence-backed]`** In AI/ML, a scientific contribution is **not** merely getting a higher benchmark score ("SOTA chasing"). A valid contribution falls into one of four categories:

1. **Mechanistic Explanation:** Explaining *why* an existing class of models succeeds or fails.
2. **Boundary Discovery:** Proving the precise breakdown conditions of an established paradigm.
3. **Novel Methodology:** Introducing a new technique that yields significant, validated improvements with clear mechanistic justification.
4. **New Diagnostic Benchmark:** Designing a benchmark that isolates a previously unmeasured failure mode or capability gap.

---

## 39. From Results to Scientific Explanation

**`[Research-practice synthesis]`** Transform raw experimental results into a scientific narrative using the **Evidence Translation Chain**:

$$\text{Raw Metric Shift} \longrightarrow \text{Ablation Isolation} \longrightarrow \text{Diagnostic Probe Confirmation} \longrightarrow \text{General Scientific Claim}$$

* **Example:**
  * *Raw Shift:* Model accuracy increases from 72% to 81%.
  * *Ablation:* 8% of the 9% gain disappears when norm stabilization is removed.
  * *Probe:* Feature space visualization confirms token norm variance drops by 65%.
  * *Scientific Claim:* Token norm stabilization prevents language prior dominance during low-contrast multimodal cross-attention.

---

## 40. Building the Evidence Chain

**`[Research-practice synthesis]`** Your paper or thesis must build an unbroken **Evidence Chain** where every claim is backed by a specific experiment:

```text
Claim 1: Low visual contrast causes token norm collapse in VLM encoders.
  └─► Verified by Experiment 1 (Layer-wise norm probing across contrast levels).

Claim 2: Token norm collapse allows language priors to dominate predictions (Hallucination).
  └─► Verified by Experiment 2 (Cross-attention weight analysis & text-only ablation).

Claim 3: Norm stabilization eliminates low-contrast hallucination without degrading clean performance.
  └─► Verified by Experiment 3 (Benchmark evaluation vs SOTA baselines + controls).
```

---

## 41. Knowing When Research Is Done

**`[Practical heuristic]`** You have completed your research project when you satisfy the **3 Completion Criteria**:

1. **Claim Coverage:** Every core claim listed in your introduction is directly supported by an experiment with controls and error bars.
2. **Alternative Explanations Ruled Out:** You have executed negative controls or ablations that rule out parameter count, hyperparameter tuning, or data leakage as explanations.
3. **Failure Boundary Identified:** You can explicitly describe the conditions under which your proposed method stops working.

---

# PART VII — THESIS AND PAPER COMPLETION

## 42. Thesis Completion Pipeline

**`[Research-practice synthesis]`** Execute the **Thesis Assembly Pipeline**:

```text
[Phase 1: Skeleton & Claims] ──> [Phase 2: Methods & Setup] ──> [Phase 3: Results & Evidence Chain] ──> [Phase 4: Discussion & Limitations]
```

* Write Chapter 3 (Methodology) and Chapter 4 (Experimental Setup) *while running experiments*, not after!
* Draft figures and tables first, then write narrative prose to explain them.

---

## 43. Paper Completion Pipeline

**`[Research-practice synthesis]`** When targeting peer-reviewed conferences (e.g., NeurIPS, ICML, ICLR, CVPR, ACL):

1. **Title & Abstract:** Draft early to force crisp framing of problem, mechanism, and quantitative findings.
2. **Introduction (1.5 pages):** State problem, gap, key insight, core claims, and summary of results.
3. **Related Work (1 page):** Position your work against Quadrant 2 direct competitors; do not write a history textbook.
4. **Methodology (2 pages):** Formalize your approach with clear notation, architecture diagrams, and mechanistic rationale.
5. **Experiments (3 pages):** Present Main Results, Ablations, Diagnostic Probes, and Qualitative Failure Analyses.
6. **Limitations & Ethics (0.5 page):** Frankly detail failure modes and computational requirements.

---

## 44. Reviewer / Adversarial Analysis ("Pre-Mortem")

**`[Practical heuristic]`** Before submitting your manuscript, conduct a **Reviewer Pre-Mortem**. Act as an aggressive reviewer and attack your paper with standard objections:

* *"The baseline is untuned or weak."* $\longrightarrow$ **Fix:** Add tuned SOTA baselines with equal compute.
* *"The improvement is just due to more parameters."* $\longrightarrow$ **Fix:** Add parameter-matched MLP control.
* *"The method was only tested on one benchmark."* $\longrightarrow$ **Fix:** Evaluate on a second distinct dataset split.
* *"The paper lacks mechanistic understanding."* $\longrightarrow$ **Fix:** Include internal representation probes/visualizations.

---

## 45. Publication Preparation and Writing Strategy

**`[Practical heuristic]`**
* **Active Voice:** "We demonstrate that visual norm collapse drives hallucination" instead of "It was demonstrated that hallucination might be driven by norm collapse."
* **Self-Contained Figures:** Every figure caption must be completely self-contained—a reviewer reading *only* your figures and captions should understand your key findings.
* **Open Source Release:** Prepare a clean GitHub repository containing a one-click reproduction script (`run_all_experiments.sh`) and pre-trained weights. Open code dramatically increases paper acceptance rates.

---

# PART VIII — THE REUSABLE RESEARCH OPERATING SYSTEM

## 46. Formal Research State Machine

**`[Personal workflow recommendation]`** Treat your research project as a formal **State Machine**:

```text
                       ┌───────────────┐
                       │  1. EXPLORE   │
                       └───────┬───────┘
                               │ Saturation Heuristics Met
                               ▼
                       ┌───────────────┐
                       │  2. CANDIDATE │
                       └───────┬───────┘
                               │ Gap Verified Adversarially
                               ▼
                       ┌───────────────┐
                       │ 3. PILOT MDE  │
                       └───────┬───────┘
                               │ MDE Validates Mechanism ($H_A$)
                               ▼
                       ┌───────────────┐
                       │ 4. COMMITTED  │
                       └───────┬───────┘
                               │ Full Experiments Completed
                               ▼
                       ┌───────────────┐
                       │  5. ANALYZING │
                       └───────┬───────┘
                               │ Evidence Chain Complete
                               ▼
                       ┌───────────────┐
                       │  6. WRITING   │
                       └───────────────┘
```

### State Operating Rules:

| Property | `EXPLORE` | `CANDIDATE` | `PILOT MDE` | `COMMITTED` | `ANALYZING` | `WRITING` |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| **Purpose** | Map domain topology | Verify candidate gap | Test core mechanism | Run full baselines | Audit error taxonomy | Draft thesis/paper |
| **Entry Condition** | Project start | Saturation reached | Gap verified | MDE confirms $H_A$ | Experiments done | Evidence chain set |
| **Exit Condition** | Saturation met | Adversarial check OK | $H_A$ supported | Metrics gathered | 50 errors audited | Final submission |
| **Allowed Work** | Survey reading | Closest-Work Matrix | Toy 2h script | Full benchmark runs | Failure probes | Writing manuscript |
| **Forbidden Work** | Full model training | Topic hunting | Full benchmark training | New topic hunting | Code refactoring | New experiments |
| **Failure Mode** | Endless searching | Candidate churn | Premature scaling | Scope creep | Ignoring errors | Unbacked claims |
| **Recovery Path** | Saturation rules | Freeze candidate | Simplify to toy probe | Scope Reduction | Error Taxonomy | Pre-mortem review |

---

## 47. Practical Research Artifact Templates

### Template 1: Field Map
```markdown
# Field Map: [Domain Name]

## Quadrant 1: Foundational Bedrock
- Paper A (2020): [Core contribution]
- Paper B (2021): [Core contribution]

## Quadrant 2: Active Frontier (Top Competitors)
- Paper C (2023): [SOTA Method]
- Paper D (2024): [SOTA Method]

## Quadrant 3: Benchmarks & Infrastructure
- Benchmark X: [Metric, Sample count]
- Evaluation Suite Y: [Official split]

## Quadrant 4: Open Tension / Anomalies
- Anomaly 1: [Observed contradiction or failure mode]
```

### Template 2: Question Ledger
```markdown
# Question Ledger

| Q ID | Candidate Question | Maturity Level (0-6) | Gap Type | MDE Status | Decision |
| :--- | :--- | :--- | :--- | :--- | :--- |
| `Q-01` | Does norm collapse cause VLM hallucination? | Level 4 | Mechanistic | Passed | Committed |
```

### Template 3: Gap Verification Record
```markdown
# Gap Verification Record

## Candidate Claim
Low visual contrast causes feature norm collapse in VLM encoders, leading to text decoder hallucination.

## Adversarial Search Queries Tested
1. `"visual encoder feature norm collapse contrast"` -> 0 direct hits
2. `"VLM low contrast object hallucination cross-attention"` -> 2 papers (neither measures norms)

## Closest Work Identified
- Smith et al. (2023): Evaluates hallucination under text prompt noise, NOT visual contrast.
- Zhang et al. (2024): Proposes cross-attention re-weighting, NO norm measurement.

## Decision
[X] Verified Genuine Gap -> Proceed to Candidate State
```

### Template 4: Closest-Work Matrix
```markdown
# Closest-Work Matrix

| Paper | Problem Addressed | Core Assumption | Primary Limitation | How Our Work Differs |
| :--- | :--- | :--- | :--- | :--- |
| Smith et al. | Hallucination | High contrast | Text-only prompts | Measures visual token norm collapse |
| Zhang et al. | Attention Drift | Uniform attention | Requires extra tuning | Modifies encoder norm layers directly |
```

### Template 5: Hypothesis Sheet
```markdown
# Hypothesis Sheet: [Project Name]

- **$H_A$ (Primary Mechanism):** Visual token norm stabilization prevents language prior dominance during low-contrast cross-attention.
- **$H_B$ (Parameter Control):** Performance gain is caused by adding extra trainable parameters in the bottleneck.
- **$H_C$ (Regularization Control):** Performance gain is caused by implicit gradient smoothing.
```

### Template 6: Experiment Specification / Pre-Registration
```markdown
# Experiment Specification: `EXP-002`

- **Hypothesis Tested:** $H_A$ vs $H_B$
- **Independent Variable:** Norm stabilization module (ON vs Parameter-Matched MLP)
- **Dependent Variable:** Hallucination rate on Low-Contrast Benchmark
- **Controlled Variables:** Seed=42, ResNet-50 backbone, $T=0.0$, Batch Size=32
- **Compute Budget:** 1.5 GPU hours on Colab Pro
```

### Template 7: Experiment Ledger
```markdown
# Experiment Ledger

| Run ID | Date | Git Commit | Config | Metric Score | Result / Status | Artifact Path |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| `EXP-001` | 2024-10-12 | `a1b2c3d` | Baseline | 74.2% | Expected baseline | `/logs/exp001` |
| `EXP-002` | 2024-10-12 | `e4f5g6h` | Norm Fix ($H_A$) | 78.5% | $H_A$ supported | `/logs/exp002` |
```

### Template 8: Decision Log
```markdown
# Decision Log

## Decision 2024-10-14: Benchmark Switch
- **Context:** Benchmark X contains 15% mislabeled background patches.
- **Decision:** Switch primary evaluation to Benchmark Y.
- **Evidence:** Manual audit of 100 samples in Benchmark X revealed label ambiguity.
```

### Template 9: Evidence Matrix
```markdown
# Evidence Matrix

| Introduction Claim | Supporting Experiment | Figure/Table Path | Control Condition | Confidence |
| :--- | :--- | :--- | :--- | :--- |
| Claim 1: Norm collapse occurs in low contrast | `EXP-001` Probe | `fig_2_norms.pdf` | High contrast control | High |
```

### Template 10: Error Analysis Sheet
```markdown
# Error Analysis Sheet (Sample Size = 50)

| Error Category | Count | Percentage | Representative Sample ID | Action / Fix |
| :--- | :--- | :--- | :--- | :--- |
| Low Contrast Norm Collapse | 20 | 40% | `IMG_042.jpg` | Target for $H_A$ fix |
| Label Ambiguity in Ground Truth | 15 | 30% | `IMG_108.jpg` | Exclude corrupt labels |
| Out-of-Vocabulary Terms | 10 | 20% | `IMG_211.jpg` | Document in limitations |
| Random Noise | 5 | 10% | `IMG_305.jpg` | Expected variance |
```

### Template 11: Research Control Center
```markdown
# RESEARCH_CONTROL_CENTER.md

- **Active State:** COMMITTED
- **Frozen Question:** Does visual encoder token norm collapse cause object hallucination in low contrast?
- **Active Hypothesis:** $H_A$ (Norm stabilization prevents text prior dominance)
- **Next Action:** Run `EXP-003` parameter-matched control script
- **Scope Boundary:** Frozen to ResNet-50 backbone on Low-Contrast Benchmark Y
```

---

## 48. Research Control Center

Implement `RESEARCH_CONTROL_CENTER.md` in your project root as your daily operational dashboard. Never write code or read papers without updating this file first!

---

## 49. Future Project Bootstrap

When initializing a new AI/ML research initiative:

```bash
mkdir -p my_research/{configs,src/{models,data,mechanisms,utils},experiments,tests,logs,docs}
touch my_research/{RESEARCH_CONTROL_CENTER.md,experiment_ledger.csv,decision_log.md,README.md}
git init && git add . && git commit -m "Bootstrap research repository"
```

---

## 50. Common Research Failure Modes

**`[Thesis forensic lesson]`** Avoid these 5 lethal research traps:

1. **SOTA Chasing Without Mechanism:** Tweaking hyperparameter grids endlessly to beat a benchmark by 0.2% without knowing why.
2. **The Monolithic Architecture Trap:** Writing 2,000 lines of complex PyTorch code before testing the core mechanism on a 2-hour synthetic probe.
3. **The Collection Trap:** Accumulating 100 PDFs to avoid committing to a single experiment.
4. **Confirmation Bias:** Celebrating metric increases that are actually caused by random seed noise or parameter inflation.
5. **Ignoring Failure Cases:** Looking only at average accuracy tables without inspecting raw misclassified images/text outputs.

---

## 51. Master Research Pre-Flight Checklist

Before declaring your research project finished, verify every item:

- [ ] **Question Precision:** Is the research question specific, mechanistic, and falsifiable?
- [ ] **Gap Verification:** Have adversarial search queries confirmed the gap is unaddressed in recent literature?
- [ ] **Closest-Work Matrix:** Are the top 3 competitor papers cataloged with explicit differences noted?
- [ ] **Competing Hypotheses:** Are $H_A, H_B, H_C$ explicitly formulated?
- [ ] **MDE Executed:** Did a cheap pilot experiment confirm mechanism viability before full training?
- [ ] **Baseline Rigor:** Are baselines evaluated with equal compute, hyperparameter tuning, and parameter matching?
- [ ] **Failure Triad Checks:** Have data leakage, shortcut learning, and seed variance been audited?
- [ ] **Reproducibility:** Are deterministic seeds set, dependencies locked, and commit hashes logged?
- [ ] **Error Analysis:** Have 50+ raw error samples been manually categorized?
- [ ] **Evidence Chain Complete:** Does an unbroken link connect every intro claim to a figure/table?
- [ ] **Pre-Mortem Conducted:** Have major reviewer objections been addressed with control experiments?

---

## 52. One-Page Research Desk Reference

```text
┌────────────────────────────────────────────────────────────────────────────────────────┐
│                          ONE-PAGE AI/ML RESEARCH DESK REFERENCE                        │
├────────────────────────────────────────────────────────────────────────────────────────┤
│ 1. CONCEPT LADDER: Field -> Sub-field -> Topic -> Phenomenon -> Gap -> Question -> $H_A$│
│ 2. GAP CHECK: "Nobody tried X on Y" is NOT a gap. Search adversarial mechanism terms.  │
│ 3. SATURATION RULE: Stop reading when citations loop and competitors are clear.         │
│ 4. 14-DAY RULE: Max 14 days in exploration before executing a 2-hour MDE script.      │
│ 5. MDE: Smallest experiment that falsifies $H_A$ vs $H_B/H_C$ in < 2 hours compute.     │
│ 6. BASELINE RULE: Tune baselines with EQUAL compute and match total parameter counts.  │
│ 7. FAILURE TRIAD: Audit data contamination, shortcut correlations, & seed variance.     │
│ 8. ERROR AUDIT: Manually inspect 50 raw misclassified samples; categorize failure types.│
│ 9. REVISION: Pivoting your research question based on empirical data IS progress!      │
│ 10. PRE-MORTEM: Attack your paper like a hostile reviewer before submitting.           │
└────────────────────────────────────────────────────────────────────────────────────────┘
```

---

# APPENDICES

## Appendix A — Thesis Autopsies

**`[Thesis forensic lesson]`** Forensic case studies of abandoned thesis proposals and real-world project failures analyzed to extract general research lessons:

### Autopsy 1: Unverified Layer-Hub / Layer-Center Claims
* **Original Proposal:** Claiming that intermediate Transformer layers act as universal hub centers for multimodal cross-attention alignment.
* **Attractive Assumption:** High cosine similarity between visual and text tokens in layer 8 was assumed to represent semantic cross-modal alignment.
* **Evidence Discovered:** Diagnostic probes revealed that activation vectors in layer 8 had uncentered LayerNorm statistics, causing all embeddings to collapse into a single narrow cone regardless of input content (Representation Collapse).
* **Failure Mechanism:** The "hub center" was an artifact of uncentered feature norms, not semantic alignment.
* **Why Killed:** The core mechanism was a mathematical artifact of LayerNorm, not an alignment phenomenon.
* **General Research Lesson:** Never build a thesis on unverified claims about internal model representations without running an independent diagnostic probe first!

### Autopsy 2: Inaccessible / Unhosted Datasets
* **Original Proposal:** Evaluating multimodal medical reasoning on a specialized clinical dataset cited in a 2022 paper.
* **Attractive Assumption:** The published paper provided a GitHub link to the dataset.
* **Evidence Discovered:** The GitHub link led to a 404 error. Author contact attempts revealed the dataset was locked under hospital institutional review board (IRB) restrictions and could not be released publicly.
* **Failure Mechanism:** Three weeks were wasted waiting for dataset access before discovering the data was inaccessible.
* **Why Killed:** Total lack of accessible evaluation infrastructure.
* **General Research Lesson:** Always verify dataset availability, hosting status, and download links before committing to a research question!

### Autopsy 3: AI-Assisted Research Errors (Hallucinated Papers & Claims)
* **Original Proposal:** Building a novel attention module based on a cited paper "Zhang et al. (2023) Multimodal Cross-Norm Alignment."
* **Evidence Discovered:** Searching Google Scholar and arXiv revealed that "Zhang et al. (2023)" was completely hallucinated by an LLM during initial literature exploration.
* **General Research Lesson:** Never trust AI-generated citations or literature summaries without manually downloading and reading the original PDF paper!

---

## Appendix B — Hardware and Execution Boundaries

**`[Thesis forensic lesson]`** Operational boundaries for local and cloud compute execution setups:

| Hardware Setup | VRAM / System RAM | Suitable Research Tasks | Forbidden Tasks |
| :--- | :--- | :--- | :--- |
| **Local CPU (AMD Ryzen 5 5600G)** | 8 GB System RAM | Code editing, unit testing data loaders, toy synthetic probes | Full model training, multi-gigabyte dataset loading |
| **Google Colab Free (T4 GPU)** | 15 GB VRAM | 2-hour MDEs, feature probing, small backbone tuning (ResNet-50) | Full 70B LLM fine-tuning, 100-epoch runs |
| **Google Colab Pro (A100 GPU)** | 40 GB VRAM | Full baseline benchmark evaluation, 7B model LoRA fine-tuning | Massive pre-training from scratch |

---

## Appendix C — Canonical Terminology Map

**`[Research-practice synthesis]`** Harmonized definitions reconciling terminology differences across source documents:

| Concept | Alternative Source Terms | Canonical Term | Precise Meaning |
| :--- | :--- | :--- | :--- |
| **Minimal Test** | Pilot run, Toy probe, Cheap test | **Minimum Discriminating Experiment (MDE)** | Smallest experiment designed to falsify $H_A$ vs $H_B$ |
| **Data Contamination** | Test leak, Overlap, Memory leak | **Data Leakage** | Information flow from test set into training pipeline |
| **Spurious Correlation** | Background bias, Clever Hans | **Shortcut Learning** | Model exploiting non-causal background artifacts |
| **Search Stopping** | Literature closure, Reading limit | **Literature Saturation** | Point where new papers yield zero new information |
| **Topic Paralysis** | Idea churn, Paper hoarding | **The Collection Trap** | Accumulating papers to avoid experimental commitment |

---

## Appendix D — Source Synthesis and Evidence Base

This canonical playbook was created by conducting a complete synthesis and reconciliation of multiple research playbook sources in the `Research_Playbook/` repository, including:
* `AI Research Methodology Playbook (Gemini).md` (89 KB)
* `AI_ML Research Playbook (Claude).md` (48 KB)
* `AI_ML Research Playbook (Antigravity).md` (98 KB)
* `AI_ML Research Playbook- From Research Discovery to Publishable Paper (Antigravity).md` (74 KB)
* `ai-ml-research-playbook (OpenResearch).md` (119 KB)
* `AI_ML_Research_Playbook (Cline).md` (281 KB)

### Synthesis Method:
1. **Deduplication:** Repeated conceptual explanations across sources (e.g., gap definitions, search queries, baseline setups) were unified into single, high-clarity canonical definitions.
2. **Reconciliation:** Methodological differences between sources (e.g., linear vs dual-loop models, reading depth ratios) were reconciled by establishing context-dependent guidelines (e.g., Phase Shift from Exploration to Commitment).
3. **Technical Preservation:** Core technical mechanisms—including the Concept Ladder, Failure Triad, Baseline Hierarchy, Minimum Discriminating Experiments, and Research State Machine—were fully preserved and enhanced with concrete AI/ML examples.
4. **Actionable Restructuring:** The unified document was reorganized into 8 Parts and 52 standalone sections designed to guide a researcher sequentially from initial curiosity to thesis and paper completion.
