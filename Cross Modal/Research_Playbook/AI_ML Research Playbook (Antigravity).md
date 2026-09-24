

# AI/ML Research Playbook: From Research Discovery to Publishable Paper

### *A Rigorous Operating Manual for Level 3 Causal Mechanism Discovery, Controlled Experimentation, and Thesis Execution*

---

## 1. Executive Overview

### The Epistemic Core of AI/ML Research

Most junior researchers mistakenly treat machine learning research as an engineering feature-race: combine Architecture $A$ with Loss Function $B$, apply it to Dataset $C$, tune hyperparameters until the metric nudges upwards by $+1.2\%$, and claim "novelty."

This paradigm—**Level 2 Benchmark Tinkering**—is intellectually fragile, scientifically shallow, and psychologically exhausting. It forces you to constantly look over your shoulder, terrified that an industrial lab with 1,000 H100s will release a model that renders your six months of work obsolete overnight.

Experienced AI/ML researchers operate under an entirely different paradigm: **Level 3 Causal Mechanism Discovery**. Under this paradigm:

* Science is the systematic reduction of uncertainty about how artificial cognitive systems function, fail, and arbitrate representations.
* A research contribution is **not** an incremental score increase; it is an **empirical explanation backed by controlled counterfactual evidence** that separates competing hypotheses.
* The ultimate measure of research productivity is not how many papers you read or how many lines of boilerplate code you write, but **how rapidly you can kill false or trivial hypotheses** and how tightly you control surviving ones.

```
       [ Level 2: Benchmark Tinkering ]              [ Level 3: Causal Mechanism Discovery ]
  Goal:    Beat benchmark by +1.5%             Goal:    Explain why the system behaves this way
  Action:  Stack methods, tune tricks          Action:  Isolate variables, run placebo controls
  Output:  Fragile leaderboard score           Output:  Defensible causal explanation
  Vulnerability: Crushed by scale/compute      Resilience: Survives scale; adds permanent knowledge
```

### The Three Knowledge Levels Enforced in this Playbook

To maintain strict epistemic hygiene, every insight, protocol, and diagnostic in this manual is indexed across three distinct knowledge levels:

* **Level 1 — Established Research Practice (Normative Standard):** How elite academic and industrial AI/ML researchers formulate, stress-test, and execute defensible research programs.
* **Level 2 — Inferred Workspace Autopsy (Empirical Reality):** Structural patterns, failure modes, dead-ends, and breakthroughs reverse-engineered from your specific research journey across Medical Imaging, Bengali VLMs, and Causal Modality Conflict.
* **Level 3 — Actionable Operating Directives (Your Constraints):** Concrete, pragmatic procedures tailored specifically to an undergraduate researcher operating with an AMD Ryzen 5 5600G (6C/12T, 8 GB RAM, no local CUDA) workstation paired with a Google Colab Pro 16 GB VRAM envelope (`Qwen2.5-VL-3B`, FP16/SDPA).

---

## 2. How Experienced Researchers Actually Work

### The Dual-Engine Discovery Model

Senior researchers do not sit in front of Google Scholar waiting for inspiration. They discover questions through the continuous interaction of two operational engines:

```
                      ┌──────────────────────────────────────────┐
                      │    ENGINE A: The Phenomenological Audit  │
                      │  (Observing anomalous model behaviors,   │
                      │   failure modes, and metric fragilities) │
                      └────────────────────┬─────────────────────┘
                                           │
                                  Frictional Contact
                                           │
                      ┌────────────────────┴─────────────────────┐
                      │     ENGINE B: The Epistemic Inquest      │
                      │ (Deconstructing the unstated assumptions │
                      │  and missing controls in existing claims)│
                      └──────────────────────────────────────────┘
```

1. **Engine A (Phenomenon-Driven / Bottom-Up):** The researcher instruments a baseline model, feeds it edge cases, strips away prompt sugarcoating, and observes where the system breaks down. They look for behavior that violates the standard narrative (e.g., *"Why does a 3B model correctly identify an object when asked directly, but completely ignore it when a conflicting sentence is prepended?"*).
2. **Engine B (Assumption-Driven / Top-Down):** The researcher reads influential papers not to learn "what is true," but to audit **what the authors assumed without proving**. They search for the *missing control experiment*, the *untested confound*, and the *unstated boundary condition*.

### The Mindset: Adversarial Prosecutor vs. Passive Student

* **The Novice (Passive Student):** Reads a paper, accepts the authors' explanation at face value, assumes the authors tested all reasonable alternatives, and looks for an incremental extension (e.g., *"They tested this on English, maybe I can test it on Bengali"* or *"They used ResNet, maybe I can use a Transformer"*).
* **The Expert (Adversarial Prosecutor):** Reads the paper assuming the authors may be suffering from confirmation bias. They ask:
  * *"Did the authors' intervention actually cause the improvement, or was it an artifact of increased token length (test-time compute)?"*
  * *"Did the probe discover a genuine representation, or did it merely fit a linear shortcut in the residual stream?"*
  * *"Could a random baseline or a simple 1-line heuristic achieve 85% of this reported gain?"*

### Epistemic Classification Scheme

Senior researchers classify every proposition in their mental ledger into one of five categories:

* `[Verified]`: Directly proven by a primary peer-reviewed source or replicated on their own compute cluster under controlled conditions.
* `[Inferred]`: A logical deduction derived from multiple verified facts that has not yet been isolated experimentally.
* `[Hypothesis]`: A falsifiable, competing scientific proposition designed to be tested against a strict null ($H_1$ vs. $H_0$).
* `[Unknown]`: Critical information that neither current empirical literature nor local experiments have established.
* `[Historical Decision]`: Documented methodological decisions from past audits (subject to reopening only upon new primary evidence).

---

## 3. Why Research Is Not Linear (The Dual-Loop Architecture)

The single most destructive myth taught in universities is the linear research pipeline ($1 \to 2 \to 3 \to \dots \to 8$). When real research encounters empirical friction, linear thinkers freeze, abandon the project, or start over from scratch.

Research is governed by two interlocking loops: the **Outer Discovery Loop** (exploratory, fast, adversarial) and the **Inner Execution Pipeline** (rigid, deterministic, frozen).

```
========================================================================================
                        THE OUTER DISCOVERY LOOP (Flexible & Fast)
========================================================================================
         [Research Area]
                │
                ▼
      [Observed Phenomenon] ◄─────────────────────────────────────────────┐
                │                                                         │
                ▼                                                         │
       [Existing Literature] ───► [Identify Dominant Explanation]         │
                │                                                         │
                ▼                                                         │
   [Find Competing Explanation] (Confound / Artifact / Mechanism)         │
                │                                                         │
                ▼                                                         │
    [Candidate Question Ledger]                                           │
                │                                                         │
                ▼                                                         │
    [Feasibility Pre-Filter] (VRAM, Dataset, Compute Envelope)             │
                │                                                         │
                ▼                                                         │
   [Minimum Discriminating Experiment (MDE)]                              │
         (N = 50-100, 48-Hour Pilot)                                      │
                │                                                         │
       ┌────────┴────────┐                                                │
       ▼                 ▼                                                │
 [Effect Vanishes /]  [Strong Discriminative Effect]                      │
 [Killed by Baseline]    │                                                │
       │                 ▼                                                │
       │       [QUESTION FREEZE PROTOCOL]                                 │
       │                 │                                                │
       └─────────────────┴─────────────────► [Pivot, Refine, or Kill] ────┘
                                                          │
========================================================================================
                      THE INNER EXECUTION PIPELINE (Rigid & Deterministic)
========================================================================================
                                                          │
                                                          ▼
                                            [Frozen Research Question]
                                                          │
                                                          ▼
                                            [Full Factorial Design]
                                             (Treatment vs. Placebo)
                                                          │
                                                          ▼
                                           [Deterministic Evaluation]
                                          (Exact-Match / Regex / CIs)
                                                          │
                                                          ▼
                                          [Adversarial Failure Audit]
                                                          │
                                                          ▼
                                          [Thesis Narrative & Paper]
```

### The Signals that Force Loop Transitions

* **Back from MDE to Literature:** Your pilot experiment shows that the placebo control reproduces 95% of the effect. The phenomenon is real, but your proposed mechanism is an illusion. You must search the literature for *measurement confounds* and *token-length artifacts*.
* **Back from Literature to Territory:** You discover that three papers published in the last 60 days have fully mapped the exact causal graph you planned to study. You kill the question immediately, saving five months of redundant execution.
* **Forward from MDE to Question Freeze:** The MDE demonstrates a massive statistical divergence ($p < 0.001$, large Odds Ratio) between the active treatment and the length-matched placebo. The question is empirically anchored and ready to be locked.

---

## 4. The Researcher's Mental Model

### The Causal Graph of AI/ML Evidence

To design an experiment that commands scientific respect, you must conceptualize every ML setup as a causal directed acyclic graph (DAG):

$$
T \longrightarrow Y \longleftarrow Z

$$

* **Treatment ($T$):** The specific mechanistic intervention you introduce (e.g., prompting the model to explicitly verbalize conflict, or zeroing out an attention head).
* **Outcome ($Y$):** The downstream decision or metric (e.g., choice of visual entity vs. textual entity, task accuracy).
* **Confounder ($Z$):** Any unisolated variable that simultaneously influences or distorts the relationship between $T$ and $Y$ (e.g., token length, prompt format, instruction phrasing, label frequency, spatial layout).

```
         [Treatment T] ───────────────────────────► [Outcome Y]
       (Explicit Conflict                          (Arbitration Choice)
         Verbalization)                                   ▲
                ▲                                         │
                │                                         │
                └─────────────── [Confounder Z] ──────────┘
                            (Token Length / Compute,
                              Positional Skew, etc.)
```

**The Core Law:** If you alter $T$ but fail to hold $Z$ invariant, your experiment measures nothing more than the confounder.

### The Three Levels of Claims

1. **Correlation:** Model accuracy drops when conflicting visual and textual tokens are presented together.
2. **Intervention:** When we instruct the model to think before answering, accuracy improves.
3. **Counterfactual Mechanism (The Level 3 Standard):** Does the accuracy improvement occur *because* the model explicitly parsed the contradiction, or simply *because* generating additional intermediate tokens provided more computational capacity (SDPA attention passes)?
   * *The Placebo Test:* Replace the conflict verbalization prompt with a length-matched neutral reasoning prompt ("Explain the geometry of the bounding box..."). If the gain persists, your hypothesis of "conflict verbalization steering" is falsified.

---

## 5. Finding Research Territories

A **Research Area** is a continent (e.g., *Vision-Language Models*). You cannot build a defensible thesis on a continent. A **Research Territory** is a specific, high-friction operational borderland within that continent.

### Criteria for a Defensible Research Territory

1. **High Information Friction:** Two fundamental components of the architecture, data pipeline, or cognitive modalities are in tension (e.g., Vision vs. Language, Pretrained Prior vs. In-Context Evidence, Parametric Memory vs. Retrieved Context).
2. **Metric Brittleness:** The dominant benchmark displays wild variance or sudden drops under minor, semantics-preserving perturbations.
3. **Accessible Scale:** The core behavioral dynamics can be reproduced on models with $\le 3\text{B}$ parameters (`Qwen2.5-VL-3B`, `Qwen2-VL-2B`, `SmolVLM`) rather than requiring 70B+ distributed clusters.
4. **Epistemic Urgency:** The community is actively debating the phenomenon, but published explanations rely on correlational claims rather than controlled interventions.

```
TERRITORY SCOPING FUNNEL:
Broad Area:       Multimodal Artificial Intelligence
  Sub-Field:      Vision-Language Models (VLMs)
    Territory:    Cross-Modal Modality Bias under Sensory Discrepancy
      Niche:      Causal Mediation of Conflict Verbalization during Source Arbitration
```

---

## 6. Finding Phenomena and Failures

Where do strong AI/ML research questions actually originate? They do not come from thin air; they emerge from **12 Catalytic Failure Modes**:

```
                       THE 12 CATALYTIC ORIGINS OF RESEARCH QUESTIONS
  ┌─────────────────────────────────┬─────────────────────────────────┬─────────────────────────────────┐
  │ 1. Unexplained Empirical Failure│ 2. Inter-Paper Contradiction    │ 3. Missing Control Experiment   │
  │ Model collapses on trivial      │ Paper A claims text dominates;  │ Paper claims "reasoning" helps, │
  │ counterfactual perturbations.   │ Paper B claims visual capture.  │ but omits length-matched placebo│
  ├─────────────────────────────────┼─────────────────────────────────┼─────────────────────────────────┤
  │ 4. Boundary Condition Collapse  │ 5. Metric / Evaluation Gaming   │ 6. Representation vs. Artifact  │
  │ Effect works on synthetic CLEVR,│ Accuracy jumps due to label     │ Probe fits residual stream      │
  │ dies instantly on real images.  │ frequency or length skew.       │ shortcut, not true concept.     │
  ├─────────────────────────────────┼─────────────────────────────────┼─────────────────────────────────┤
  │ 7. Test-Time Compute Confound   │ 8. Uncalibrated Judge Scoring   │ 9. Distribution Shift Fragility │
  │ Chain-of-thought gains driven   │ LLM judge favors verbosity, not │ Minimal stylistic change causes │
  │ purely by token count.          │ factual correctness.            │ categorical decision flip.      │
  ├─────────────────────────────────┼─────────────────────────────────┼─────────────────────────────────┤
  │ 10. Untested Core Assumption    │ 11. Bottleneck Misattribution   │ 12. Loss vs. Inference Mismatch │
  │ Assuming bidirectional cross-   │ Blaming data volume when the    │ Pretraining loss drops, but     │
  │ attention treats tokens equally.│ cause is tokenizer misalignment.│ downstream decision boundary rots│
  └─────────────────────────────────┴─────────────────────────────────┴─────────────────────────────────┘
```

### Deep Dive into the Top Catalytic Triggers

* **Trigger 3 (Missing Control Experiment):** An influential paper claims that "Chain-of-Thought prompts enable VLMs to resolve visual ambiguity." You inspect their prompt: it adds 150 tokens of reasoning. You immediately ask: *What happens if I inject 150 tokens of completely unrelated text or neutral procedural steps?* If the model's accuracy jumps identically, the paper's cognitive claim is completely dismantled.
* **Trigger 2 (Inter-Paper Contradiction):** Paper A (2024) asserts that VLMs are fundamentally biased toward textual priors due to LLM pretraining dominance. Paper B (2025) shows that in multi-choice visual question answering, models suffer from 85% "visual capture," ignoring textual instructions. This direct empirical contradiction is a goldmine. The research question becomes: *What underlying variable arbitrates whether the vision or language modality captures the decision boundary?*

---

## 7. Turning Observations into Research Questions (The 11-Stage Conceptual Chain)

To prevent intellectual confusion, you must never collapse the stages of scientific discovery. Memorize and enforce this 11-stage operational chain:

```
[1. Area] ──► [2. Territory] ──► [3. Phenomenon] ──► [4. Observation] ──► [5. Existing Claim]
                                                                                  │
  ┌───────────────────────────────────────────────────────────────────────────────┘
  ▼
[6. Alternative Explanation] ──► [7. Research Gap] ──► [8. Research Question]
                                                               │
  ┌────────────────────────────────────────────────────────────┘
  ▼
[9. Falsifiable Hypotheses] ──► [10. Minimum Experiment] ──► [11. Contribution]
```

### Three Concrete AI/ML Case Studies

```
========================================================================================================================
STAGE                CASE STUDY 1: Modality Conflict     CASE STUDY 2: Visual Binding        CASE STUDY 3: Test-Time Compute
========================================================================================================================
1. Area              Vision-Language Learning            Multimodal Vision-Language          Reasoning in LLMs / VLMs
------------------------------------------------------------------------------------------------------------------------
2. Territory         Modality Conflict & Arbitration     Compositional Attribute Binding     Chain-of-Thought (CoT) Prompting
------------------------------------------------------------------------------------------------------------------------
3. Phenomenon        Visual Capture under contradiction  Attribute swap across objects       Accuracy jump on multi-step tasks
------------------------------------------------------------------------------------------------------------------------
4. Observation       When image says "red" and text says When image has red cube & blue ball, Model solves complex math only
                     "blue", model answers "red" (89%).  model reports "blue cube".          when outputting reasoning tokens.
------------------------------------------------------------------------------------------------------------------------
5. Existing Claim    "VLMs possess an unshakeable visual "Self-attention heads fail to bind  "The model learns to perform
                     perceptual prior during generation." visual tokens to spatial tags."    latent cognitive deduction."
------------------------------------------------------------------------------------------------------------------------
6. Alternative       The preference is an artifact of    The failure is caused by language   The gain is an artifact of test-
   Explanation       unconstrained decoding; verbalizing prior frequency, not attention     time compute (more attention
                     conflict causally unlocks text.     binding mechanics.                  layers per decision step).
------------------------------------------------------------------------------------------------------------------------
7. Research Gap      No work separates causal steering   Prior work intervened on attention  No work compares CoT against a
                     from post-hoc rationalization via   without controlling for unigram     length-matched neutral placebo
                     placebo compute controls.           prior text frequencies.             prompt on identical splits.
------------------------------------------------------------------------------------------------------------------------
8. Research Question Does explicit conflict verbalization Does attribute binding failure     Does CoT reasoning improve accuracy
                     causally shift source arbitration,  persist when text unigram priors    due to logical structure, or
                     or merely rationalize visual bias?  are counterbalanced?                merely due to token length?
------------------------------------------------------------------------------------------------------------------------
9. Hypotheses        H1: Verbalization cuts visual bias  H1: Binding failure is visual.      H1: Logic structure drives gain.
                     beyond length-matched placebo.      H0: Binding failure is predicted    H0: Neutral length placebo matches
                     H0: Placebo matches verbalization.  entirely by text language prior.    CoT accuracy within 1.5%.
------------------------------------------------------------------------------------------------------------------------
10. Minimum          3-Arm Factorial on N=100:           Evaluate attribute binding on       Compare Math500 on 3 arms:
    Experiment       Unconstrained vs. Placebo vs.       natural vs. synthetic images with   Direct vs. Length Placebo vs.
                     Conflict Verbalization.             inverted linguistic frequencies.    Step-by-step CoT.
------------------------------------------------------------------------------------------------------------------------
11. Contribution     Empirical proof that conflict       Causal evidence that "binding       Proof that 60% of CoT gain in 3B
                     verbalization is a causal steering  failures" are linguistic prior     models is compute-bound rather
                     mechanism (OR = 24.57, Δ = +63.7%). artifacts, not perceptual flaws.    than logic-bound.
========================================================================================================================
```

---

## 8. Literature Exploration Strategy

### The 80 / 15 / 5 Pareto Reading Law

Novice researchers read every paper sequentially from Title to Conclusion, burning 40 hours a week and retaining nothing. Senior researchers operate via ruthless triage:

```
                              ┌───────────────────────────────┐
                              │     80% OF PAPERS: 5 MINUTES   │
                              │  Abstract, Fig 1, Claims Audit│
                              └───────────────┬───────────────┘
                                              │ Survives
                                              ▼
                              ┌───────────────────────────────┐
                              │    15% OF PAPERS: 30 MINUTES  │
                              │ Tables, Controls, Loss Setup  │
                              └───────────────┬───────────────┘
                                              │ Directly Competing
                                              ▼
                              ┌───────────────────────────────┐
                              │     5% OF PAPERS: DEEP AUDIT  │
                              │ Code, Appendices, Math Proofs │
                              └───────────────────────────────┘
```

### The Three-Dimensional Citation Traversal

Do not wander aimlessly through reference lists. Traverse the citation graph along three orthogonal axes:

1. **Backward Tracing (Foundational Ancestry):** Identify the mathematical formalization or seminal benchmark that every current paper cites as gospel (e.g., Radford et al. for CLIP contrastive loss). Find the original paper and check: *What warning did the original authors give that the community subsequently ignored?*
2. **Forward Tracing (Hostile Descendants):** Search Google Scholar for papers that cite the target paper using phrases like *"contrary to"*, *"in contrast to"*, or *"fails to generalize"*. Identify who has already attempted to challenge the claim.
3. **Orthogonal Tracing (Conceptual Parallels):** Search how other disciplines model the identical mathematical problem under different nomenclature. For example, *Vision-Language Modality Conflict* is called *Sensory Cue Integration* in cognitive neuroscience and *Multisensory Fusion Robustness* in robotics.

### The Literature Saturation Criterion

**When do you stop reading?** You stop when you encounter **The Saturation Horizon**: when five consecutive new papers cite no foundational papers you have not already audited, propose no mechanisms you have not already cataloged, and present no failure modes that are not already present in your Question Ledger.

---

## 9. How to Search Like a Researcher

A senior researcher does not type generic keywords like `"VLM conflict resolution"` into Google Scholar. They execute an evolving **10-Stage Investigative Query Progression**:

```
STAGE 1: Phenomenon Search
  Query: "multimodal conflict" OR "modality competition" OR "cross-modal bias"
  Goal: Find all papers documenting that models favor one modality over another.

STAGE 2: Mechanism / Explanation Search
  Query: "visual capture" AND ("mechanism" OR "attention routing" OR "modality preference")
  Goal: Discover what theory the original authors invented to explain the behavior.

STAGE 3: Alternative Explanation Search
  Query: ("visual bias" OR "hallucination") AND ("language prior" OR "unigram frequency" OR "decoding artifact")
  Goal: Find researchers arguing that the phenomenon is caused by something entirely different.

STAGE 4: Confound Search
  Query: "chain of thought" AND ("token length" OR "length matched" OR "compute confounding")
  Goal: Discover if intermediate reasoning gains are simply test-time compute artifacts.

STAGE 5: Replication & Fragility Search
  Query: ("modality bias" OR "conflict arbitration") AND ("failure" OR "brittle" OR "not robust")
  Goal: See where the claimed effect breaks down under distribution shift.

STAGE 6: Boundary Condition Search
  Query: "visual grounding" AND ("synthetic vs natural" OR "CLEVR" OR "real-world images")
  Goal: Determine if the effect is confined to synthetic toy benchmarks.

STAGE 7: Intervention Search
  Query: ("conflict verbalization" OR "explicit reasoning" OR "activation steering") AND "multimodal"
  Goal: Identify every technique attempted to steer or balance modality decisions.

STAGE 8: Benchmark & Artifact Search
  Query: ("modality conflict" OR "arbitration benchmark") AND ("dataset" OR "huggingface" OR "github")
  Goal: Find existing data pipelines to avoid wasting three weeks generating images from scratch.

STAGE 9: Terminology Disguise Search
  Query: "cue integration" OR "sensory arbitration" OR "modality capture" OR "visual neglect"
  Goal: Catch papers studying your exact question under non-standard terminology.

STAGE 10: Recency Scooping Search (Filter: Past 6 Months / arXiv only)
  Query: ("Qwen2.5-VL" OR "LLaVA-NeXT") AND ("modality conflict" OR "source arbitration")
  Goal: Verify that no group has uploaded an identical experiment in the last 90 days.
```

---

## 10. How to Read and Interrogate Papers (The 6-Pass Adversarial Audit)

Never read an AI/ML paper passively. Interrogate it like an adversarial auditor:

```
Pass 1: Claims Audit (Abstract + Intro + Conclusion)
  Questions: What is the exact scientific claim? Is it an architectural claim, a data claim,
             or a cognitive mechanism claim? Write down their claim in one falsifiable sentence.

Pass 2: The Empirical Reality Check (Figures 1, 2 & Table 1)
  Questions: Look strictly at the axes, error bars, and baseline comparisons. Did they compare
             against the strongest existing method or a crippled strawman? Are the y-axes truncated?

Pass 3: Threat-to-Validity Inspection (Methodology & Loss Formulations)
  Questions: What is held constant, and what is allowed to vary? If they tuned hyperparameters
             for their method, did they spend equal compute tuning the baseline?

Pass 4: The Omission Scan (What is NOT in the main text?)
  Questions: What happens at temperature = 0? What happens under random seeds? Did they report
             accuracy across all subgroups, or aggregate it into a single masking average?

Pass 5: Appendix & Ablation Autopsy (Tables in the Appendices)
  Questions: Go straight to Appendix C/D. Find the ablation table where they remove components.
             Does the proposed novelty actually provide the gain, or does a 1-line heuristic match it?

Pass 6: Code & Artifact Dissection (GitHub / Hugging Face)
  Questions: Open the evaluation script. How are answers parsed? Is there regex leakage? Are
             failed generations silently dropped from the denominator?
```

---

## 11. Building a Field Map

To prevent cognitive overwhelm, summarize your domain into a **One-Page Structured Field Map Matrix**. If your field map cannot fit onto a single screen, you do not understand the frontier; you have merely accumulated clutter.

### Canonical Field Map Architecture: Multimodal Source Arbitration

```
========================================================================================================================
DIMENSION               ORTHODOX PARADIGM                  DISSENTING / COUNTER-EVIDENCE      YOUR SCIENTIFIC NICHE
========================================================================================================================
1. Core Theory          VLMs have a dominant textual prior Models show 89% "Visual Capture"   Arbitration is not static; it is
                        inherited from LLM pretraining.     under explicit cross-modal         causally steerable via structured
                                                            contradiction (Arm 2 baseline).   verbalization protocols.
------------------------------------------------------------------------------------------------------------------------
2. Standard Benchmarks  MME, MMBench, Seed-Bench            Modality-Conflict-Arbitration-v2, Controlled factorial conflict sets
                        (Correlational / Standard VQA).     Counterfactual-VQA.                with balanced attribute swaps.
------------------------------------------------------------------------------------------------------------------------
3. Evaluation Metric    Raw VQA Accuracy (%)                Visual vs. Textual Capture Rate    Causal Shift (Δ_arb), Odds Ratios,
                        (Masks modality preference).        and Refusal Rate under conflict.   Length-Matched Placebo Margins.
------------------------------------------------------------------------------------------------------------------------
4. Primary Failure Mode Hallucination attributed to data    Arbitration failure: model sees    Visual Capture: model ignores text
                        co-occurrence statistics.           text but defaults to image tokens. truth even when it can read it.
------------------------------------------------------------------------------------------------------------------------
5. Unresolved Mystery   Does CoT reasoning fix conflict,    Reasoning often acts as post-hoc  Separating causal steering from
                        or merely generate more tokens?     rationalization of visual prior.  epiphenomenal rationalization.
========================================================================================================================
```

---

## 12. Finding the Closest Existing Work

### The Fatal Keyword Illusion

Novice researchers search for: `"Causal Conflict Verbalization in Qwen2.5-VL-3B"`. When Google Scholar returns zero results, they celebrate: *"My idea is 100% novel!"*

This is an illusion. You did not discover a novel scientific territory; you simply searched an overly specific string of adjectives. Somewhere in the literature, a researcher has already executed the functional equivalent of your experiment under completely different terminology.

### Searching by Functional Invariance

To find the true "closest work," strip away the model name and surface task. Search for the **Functional Invariant**:

```
SURFACE SEARCH (Useless):
  "Conflict verbalization in Qwen2.5-VL-3B on Bengali images"

FUNCTIONAL INVARIANT SEARCH (Rigorous):
  1. Invariant Mechanism: "Forced intermediate tokens under contradictory multimodal cues"
  2. Alternative Names:   "Modality competition", "Cross-modal sensory override",
                          "Faithful reasoning under counterfactual premise",
                          "Unimodal shortcut learning in vision-language models"
  3. Experimental Match:  "Comparing unconstrained generation vs. prompted intermediate steps
                          when visual tokens contradict textual instruction tokens"
```

### The 4-Question Closest Work Audit

Before claiming novelty, locate the single paper that is closest to your idea and answer:

1. *What is the exact mathematical or experimental difference between their setup and mine?*
2. *If their paper were published tomorrow, would my paper look like a minor configuration tweak or a genuine conceptual advance?*
3. *Did they include the critical control experiment that I am proposing?*
4. *Did they explain the underlying mechanism, or merely report an empirical observation?*

---

## 13. Verifying Whether a Gap Is Real

Not all gaps are worth investigating. A gap may exist simply because it is trivial, uninteresting, or already answered indirectly.

```
                                  THE 10-STAGE GAP AUDIT
  ┌───────────────────────────────────────────────┬───────────────────────────────────────────────┐
  │ 1. Direct Answer Test                         │ 2. Indirect Answer Test                       │
  │ Has this exact experiment been performed?     │ Did a related paper answer this as a side-    │
  │ If YES ──► KILL.                              │ observation in Table 7? If YES ──► KILL.      │
  ├───────────────────────────────────────────────┼───────────────────────────────────────────────┤
  │ 3. Terminology Disguise Test                  │ 4. Recency Closure Test                       │
  │ Is this solved under another name?            │ Has an arXiv preprint closed this in the last │
  │ Check "cue integration" / "shortcut learning".│ 90 days? If YES ──► KILL.                     │
  ├───────────────────────────────────────────────┼───────────────────────────────────────────────┤
  │ 5. Superficial Wrapper Test                   │ 6. Scientific Leverage Test                   │
  │ Is the novelty merely a dataset/language swap?│ If answered, does this change how we train,   │
  │ If NO algorithmic mechanism ──► KILL.         │ prompt, or understand models?                 │
  ├───────────────────────────────────────────────┼───────────────────────────────────────────────┤
  │ 7. Non-Triviality / Falsifiability Test       │ 8. Symmetric Value Test                       │
  │ Could anyone predict the result using simple  │ If the result is completely negative (H0), is │
  │ logic? If obvious ──► KILL.                   │ it still publishable? If NO ──► KILL.         │
  ├───────────────────────────────────────────────┼───────────────────────────────────────────────┤
  │ 9. Compute Realism Test                       │ 10. Direct Measurement Test                   │
  │ Can this be decisively answered within 16 GB  │ Can the effect be measured deterministically, │
  │ VRAM? If requires 8xH100 ──► KILL.            │ or does it rely on noisy LLM judges?          │
  └───────────────────────────────────────────────┴───────────────────────────────────────────────┘
```

---

## 14. Competing Explanations and Hypotheses ($H_1$ vs. $H_0$)

A research question without mutually exclusive, competing hypotheses is not science; it is a fishing expedition.

### The Anatomy of an Adversarial Null Hypothesis

Never set up a strawman null hypothesis like $H_0: \text{"The model does nothing"}$. Your null hypothesis must be **the most plausible, boring alternative explanation** that could account for the observed phenomenon without invoking your favored theory.

```
SCIENTIFIC HYPOTHESIS PAIRING (Example: Thesis Modality Arbitration):

Primary Hypothesis (H1 - Causal Steering):
  Explicit verbalization of conflict actively steers internal attention routing, causally
  overriding the visual capture default and shifting source arbitration toward textual evidence.

Adversarial Null Hypothesis (H0 - Compute Confound / Rationalization):
  The reduction in visual capture is not caused by semantic conflict awareness, but is an
  epiphenomenon of test-time compute. A length-matched neutral placebo prompt that forces the
  generation of an equal number of non-conflict tokens will produce an identical shift in arbitration.

THE FALSIFICATION CRITERION:
  If Accuracy(H1) - Accuracy(H0_Placebo) < 5.0% OR Odds Ratio < 1.5,
  H1 is formally FALSIFIED. The verbalization theory is rejected.
```

---

## 15. Adversarial Idea Testing (The Self-Prosecution Protocol)

Before spending a single hour writing PyTorch code, subject your research idea to the **Reviewer 2 Self-Prosecution Protocol**:

```
                       THE REVIEWER 2 SELF-PROSECUTION AUDIT
  ┌────────────────────────────────────────────────────────────────────────────────────────┐
  │ 1. The Trivial Baseline Attack:                                                        │
  │    "Can a 1-line heuristic, random prompt, or unigram frequency table achieve 85%      │
  │     of my proposed effect?"                                                            │
  ├────────────────────────────────────────────────────────────────────────────────────────┤
  │ 2. The Compute Confound Attack:                                                        │
  │    "If I match the number of generated tokens using a neutral placebo, does my entire  │
  │     novelty evaporate?"                                                                │
  ├────────────────────────────────────────────────────────────────────────────────────────┤
  │ 3. The Dataset Leakage Attack:                                                         │
  │    "Does the model already have the answer memorized in its pretraining corpus via     │
  │     text-image co-occurrence statistics?"                                              │
  ├────────────────────────────────────────────────────────────────────────────────────────┤
  │ 4. The Prompt Engineering Attack:                                                      │
  │    "Does the effect disappear if I change the phrasing of my prompt by two words,      │
  │     meaning I have discovered a prompt artifact rather than an architectural property?"│
  ├────────────────────────────────────────────────────────────────────────────────────────┤
  │ 5. The Metric Artifact Attack:                                                         │
  │    "Is the accuracy gain an artifact of how my regex parses answers from the output?"  │
  ├────────────────────────────────────────────────────────────────────────────────────────┤
  │ 6. The 'Who Cares?' Attack:                                                            │
  │    "If my hypothesis is 100% correct, what can an ML engineer or researcher do today  │
  │     that they could not do yesterday?"                                                 │
  └────────────────────────────────────────────────────────────────────────────────────────┘
```

If your proposed idea cannot survive all six questions on paper, **do not implement it**. Refactor the question until it is immune to trivial destruction.

---

## 16. Fast Idea-Killing

The defining characteristic of an elite researcher is **speed of hypothesis rejection**. Novices take three months to discover that an idea is a dead end. Senior researchers kill dead ideas within **48 hours**.

### The 48-Hour Idea Kill Checklist

```
DAY 1: MORNING (Literature Execution)
  [ ] Run the 10-Stage Search Progression on arXiv and Google Scholar.
  [ ] Identify the 3 closest papers.
  [ ] Audit their appendices: Did they already test this? If yes -> KILL (Elapsed: 3 hours).

DAY 1: AFTERNOON (Functional Invariance Check)
  [ ] Strip away all domain terminology. Search for the abstract causal mechanism.
  [ ] Verify that no parallel field (e.g., NLP, Cognitive Science) has already solved it.
  [ ] If a canonical paper solved it 2 years ago -> KILL (Elapsed: 6 hours).

DAY 2: MORNING (Micro-Feasibility & Dataset Audit)
  [ ] Inspect the candidate dataset on Hugging Face.
  [ ] Download 20 samples locally. Manually inspect them for label errors, formatting noise,
      and trivial shortcuts.
  [ ] If dataset requires > 50 hours of manual cleaning -> KILL (Elapsed: 12 hours).

DAY 2: AFTERNOON (The Zero-Shot Sanity Run)
  [ ] Spin up a Colab Pro T4/V100 instance. Load Qwen2.5-VL-3B (FP16/SDPA).
  [ ] Run N = 20 samples across Treatment vs. Placebo.
  [ ] Check for signal: If the model output is completely invariant or collapses into gibberish,
      the effect size is near zero -> KILL (Elapsed: 24 hours).
```

---

## 17. Feasibility During Discovery (The 16 GB VRAM Envelope)

A brilliant research question that requires 8 NVIDIA H100 GPUs for four weeks is completely useless for an undergraduate thesis. You must treat **computational feasibility as a first-class filter during question formulation**, not as an afterthought during implementation.

### The Feasibility Envelope Matrix

```
========================================================================================================================
RESEARCH PARADIGM           COMPUTE REQUIREMENT        FEASIBILITY STATUS   ACTION DIRECTIVE
========================================================================================================================
Full Pretraining            Cluster (128+ A100s)       IMPOSSIBLE           Strictly prohibited. Do not propose.
------------------------------------------------------------------------------------------------------------------------
Full Fine-Tuning (7B+)      Multi-GPU (4x A100 80GB)   OUT OF ENVELOPE      Prohibited. Avoid 7B+ fine-tuning pipelines.
------------------------------------------------------------------------------------------------------------------------
LoRA Fine-Tuning (7B)       1x A100 / V100 (High Risk) MARGINAL             Avoid unless strictly required by the question.
------------------------------------------------------------------------------------------------------------------------
Inference Interventions     1x T4 / V100 (16GB VRAM)   GOLDEN ENVELOPE      PRIMARY PARADIGM. Perfectly suited for
(Qwen2.5-VL-3B, Qwen2-VL-2B) (FP16 / 4-bit / SDPA)     (100% Achievable)    causal steering, prompt interventions, and MDEs.
------------------------------------------------------------------------------------------------------------------------
Mechanistic Probing         1x T4 / V100 (16GB VRAM)   GOLDEN ENVELOPE      PRIMARY PARADIGM. Extracting residual streams,
(Linear Probes, Activations)(Local 8GB RAM for stats)  (100% Achievable)    attention maps, and attribution scores.
========================================================================================================================
```

### Avoiding the Two Fatal Mistakes

* **Mistake A (Premature Defeatism):** Abandoning a profound scientific question because you cannot train a model from scratch. *Correction:* Reformulate the question as an inference-time intervention or mechanistic audit on existing open-weight models (`Qwen2.5-VL-3B`).
* **Mistake B (Computational Fantasy):** Designing an elaborate multi-agent reinforcement learning loop with vision tokens that runs out of memory on batch size 1. *Correction:* Restrict all hypothesis designs to single-GPU, batch-size-1 inference with explicit KV-cache management.

---

## 18. Designing the Minimum Discriminating Experiment (MDE)

The **Minimum Discriminating Experiment (MDE)** is the smallest, cheapest controlled intervention that forces Nature to choose between your primary hypothesis ($H_1$) and your null hypothesis ($H_0$).

```
                    THE MDE SPECIFICATION BLUEPRINT
  ┌─────────────────────────────────────────────────────────────────┐
  │ Parameter                 Specification                         │
  ├───────────────────────────┼─────────────────────────────────────┤
  │ Sample Size               N = 50 to 100 balanced samples        │
  │ Model Target              Qwen2.5-VL-3B-Instruct (FP16/SDPA)     │
  │ Hardware Target           1x Colab Pro GPU (T4 / V100, 16GB)    │
  │ Wall-Clock Budget         <= 60 minutes total execution         │
  │ Factorial Arms            Arm 1: Unconstrained Baseline         │
  │                           Arm 2: Length-Matched Placebo Control │
  │                           Arm 3: Active Mechanistic Treatment   │
  │ Output Parsing            Deterministic regex (Strict 0/1 match)│
  │ Decision Threshold        Odds Ratio > 3.0 AND p < 0.01         │
  └───────────────────────────┴─────────────────────────────────────┘
```

If your MDE on $N = 100$ does not show a statistically distinguishable divergence between Arm 2 (Placebo) and Arm 3 (Treatment), **it will not magically become significant on $N = 10,000$**. Stop and reformulate.

---

## 19. From Research Question to Experimental System

Once your MDE validates the presence of an empirical signal, you scale the question into a full factorial experimental system:

```
                  OPERATIONALIZING THE EXPERIMENTAL VARIABLES
  ┌───────────────────────────────────────────────────────────────────────────────┐
  │ 1. Independent Variables (What You Manipulate):                               │
  │    * Prompt Intervention Arm: [Unconstrained, Placebo Control, Verbalization] │
  │    * Conflict Topology: [Visual Attribute Mismatch vs. Spatial Mismatch]      │
  │    * Perturbation Magnitude: [Subtle Color Shift vs. Complete Entity Swap]    │
  ├───────────────────────────────────────────────────────────────────────────────┤
  │ 2. Dependent Variables (What You Measure):                                    │
  │    * Source Capture Rate: P(Choice = Visual) vs. P(Choice = Textual)          │
  │    * Refusal / Epistemic Uncertainty Rate: P(Choice = "Cannot be determined") │
  │    * Generation Perplexity / Entropy across critical decision tokens          │
  ├───────────────────────────────────────────────────────────────────────────────┤
  │ 3. Controlled Invariant Variables (What You Lock Down):                       │
  │    * Model weights, revision tag, and quantization precision                  │
  │    * Decoding parameters: Temperature = 0.0 (Argmax deterministic)            │
  │    * Total input resolution (prevent dynamic aspect-ratio resizing shifts)    │
  │    * System prompt prefix and instruction syntax                              │
  └───────────────────────────────────────────────────────────────────────────────┘
```

---

## 20. Baselines, Controls, Metrics, and Evaluation

### The Anatomy of Scientific Controls

An experiment without controls is merely an engineering demonstration. Every valid AI/ML experiment requires at least three types of controls:

```
                                  THE TRIAD OF CONTROLS
  ┌─────────────────────────────────┬─────────────────────────────────┬─────────────────────────────────┐
  │ Positive Control                │ Negative Control                │ Placebo / Confound Control      │
  │ (Sanity Benchmark)              │ (Zero-Signal Baseline)          │ (Confound Neutralizer)          │
  │ Provide clean, non-conflicting  │ Provide totally corrupt or      │ Provide length-matched neutral  │
  │ inputs where ground truth is    │ randomized inputs where the     │ reasoning tokens to ensure that │
  │ unambiguous. Model must achieve │ expected capture rate is        │ gains are not driven by extra   │
  │ > 95% accuracy here.            │ random chance (50/50).          │ compute/time.                   │
  └─────────────────────────────────┴─────────────────────────────────┴─────────────────────────────────┘
```

### Deterministic Parsing vs. The "LLM-as-a-Judge" Delusion

* **Prohibited:** Passing model generations to GPT-4o with the prompt: *"Rate whether the model resolved the conflict on a scale of 1 to 5."* This introduces an uncalibrated, stochastic judge that suffers from length bias, sycophancy, and self-preference.
* **Enforced:** Deterministic parsing. Force the model to format its final decision into a constrained token set (e.g., `[[V]]` for visual, `[[T]]` for text) and extract it using a pre-compiled regular expression:
  ```python
  import re
  DECISION_REGEX = re.compile(r"\[\[(Visual|Textual|Uncertain)\]\]", re.IGNORECASE)
  ```

  If a model generation fails regex extraction, log it explicitly as a parsing failure; **never silently discard it**.

### Core Statistical Metrics

Report statistical shifts using formal epidemiological and causal metrics, not raw accuracy alone:

* **Net Causal Shift ($\Delta_{\text{arb}}$):**
  $$
  \Delta_{\text{arb}} = \text{Capture Rate}_{\text{Placebo}} - \text{Capture Rate}_{\text{Treatment}}

  $$
* **Odds Ratio ($OR$):**
  $$
  OR = \frac{P(\text{Textual} \mid \text{Treatment}) / P(\text{Visual} \mid \text{Treatment})}{P(\text{Textual} \mid \text{Placebo}) / P(\text{Visual} \mid \text{Placebo})}

  $$
* **Statistical Significance:** McNemar's Test for paired binary categorical decisions across matched samples ($p < 0.001$). Always report $95\%$ Confidence Intervals.

---

## 21. Pilot → Main Experiment

Never transition from an idea directly to running your full benchmark ($N = 1,600+$). Follow the three-tier phased deployment:

```
                              THE THREE-TIER DEPLOYMENT PIPELINE
  ┌────────────────────────────────────────────────────────────────────────────────────────┐
  │ TIER 1: The Micro-Pilot (N = 20 Samples)                                               │
  │ Objectives: Verify zero OOM errors in 16GB VRAM, validate regex match rate = 100%,     │
  │             confirm JSONL logging integrity, measure seconds-per-sample.               │
  │ Wall-Clock Time: 10 minutes on Colab GPU.                                              │
  ├────────────────────────────────────────────────────────────────────────────────────────┤
  │ TIER 2: The Calibrated Pilot (N = 100 to 200 Samples)                                  │
  │ Objectives: Check for presence of statistically significant effect size, calculate     │
  │             preliminary Odds Ratio, verify that Arm 2 (Placebo) does not match Arm 3.  │
  │ Wall-Clock Time: 60 minutes on Colab GPU.                                              │
  ├────────────────────────────────────────────────────────────────────────────────────────┤
  │ TIER 3: The Full Benchmark Execution (N = 1,000 to 2,000 Samples)                      │
  │ Objectives: Compute definitive 95% CIs, run McNemar's paired test, perform subgroup    │
  │             stratification (e.g., color vs. shape vs. count), execute ablations.       │
  │ Wall-Clock Time: 6 to 10 hours on Colab GPU (batched with checkpoints).               │
  └────────────────────────────────────────────────────────────────────────────────────────┘
```

---

## 22. Handling Unexpected and Negative Results

### Classifying the Two Types of Negative Results

When your experiment fails to confirm your hypothesis, you must immediately classify the failure into one of two categories:

```
                            CLASSIFYING EXPERIMENTAL ANOMALIES
  ┌───────────────────────────────────────────────┬───────────────────────────────────────────────┐
  │ CLASS A: Experimental Pathology (A Bug)       │ CLASS B: Scientific Refutation (A Discovery!) │
  ├───────────────────────────────────────────────┼───────────────────────────────────────────────┤
  │ * Tokenizer silently truncating prompts.      │ * Experiment was executed flawlessly.         │
  │ * Model degenerating into repetitive loops.   │ * Controls operated as intended.              │
  │ * Data leakage between premise and label.     │ * The hypothesized effect is genuinely zero.  │
  │ * Regex failing to parse valid responses.     │ * The dominant literature claim is false!     │
  │ Action: Fix code, re-instrument, re-run.      │ Action: WRITE THE PAPER IMMEDIATELY.          │
  └───────────────────────────────────────────────┴───────────────────────────────────────────────┘
```

### Turning a Class B Negative Result into a High-Impact Publication

In machine learning, proving that an influential technique **fails under controlled conditions** is often more valuable than introducing an incremental +1% trick:

* If you show that *Conflict Verbalization does NOT steer the decision* and that models maintain 90% visual capture regardless of what they verbalize, you have **not** failed. You have just produced empirical proof that **VLM Chain-of-Thought reasoning is post-hoc rationalization rather than faithful computation**.
* That is an oral-presentation-level paper at NeurIPS or ICLR, provided your placebo controls are airtight.

---

## 23. Iterating and Changing the Research Question

When empirical evidence forces a change, senior researchers execute one of five calibrated branching operations:

```
                               THE FIVE BRANCHING OPERATIONS
  ┌──────────────┬─────────────────────────────────────────┬─────────────────────────────────────────┐
  │ Operation    │ Empirical Trigger                       │ Concrete Action Example                 │
  ├──────────────┼─────────────────────────────────────────┼─────────────────────────────────────────┤
  │ 1. NARROW    │ The effect exists, but only on a        │ Restrict study from "All VLMs" to       │
  │              │ specific subgroup of spatial conflicts. │ "High-resolution cross-attention VLMs". │
  ├──────────────┼─────────────────────────────────────────┼─────────────────────────────────────────┤
  │ 2. BROADEN   │ The effect is identical regardless of   │ Expand study from "Color swaps" to a    │
  │              │ whether vision or text is perturbed.    │ general "Bimodal Sensory Conflict" law. │
  ├──────────────┼─────────────────────────────────────────┼─────────────────────────────────────────┤
  │ 3. PIVOT     │ Active treatment matches placebo, but   │ Shift question from "How to steer" to   │
  │              │ both reveal massive rationalization.    │ "Measuring unfaithful rationalization". │
  ├──────────────┼─────────────────────────────────────────┼─────────────────────────────────────────┤
  │ 4. REFACTOR  │ Metric variance is dominated by output  │ Replace raw accuracy with Odds Ratio    │
  │              │ length rather than correctness.         │ under strict length-matched controls.   │
  ├──────────────┼─────────────────────────────────────────┼─────────────────────────────────────────┤
  │ 5. KILL      │ The entire effect disappears when random│ Kill project within 24 hours. Log autopsy│
  │              │ seed is altered or temperature = 0.     │ in Research Log. Move to next idea.     │
  └──────────────┴─────────────────────────────────────────┴─────────────────────────────────────────┘
```

---

## 24. Freezing the Research Question

Research wanderlust is the disease of never stopping the exploration phase. At some point, you must declare a **Question Freeze**.

### The Freeze Gate Criteria (All 5 Must Be Checked)

1. [X]  **Primary Hypothesis ($H_1$) and Null Hypothesis ($H_0$)** are written in formal mathematical terms.
2. [X]  **The Minimum Discriminating Experiment (MDE)** has been run on $N \ge 50$ and demonstrated a significant effect size ($OR > 2.0$ or $\Delta > 15\%$).
3. [X]  **The Placebo Control** is locked down and proven not to replicate the full treatment effect.
4. [X]  **The Model Architecture (`Qwen2.5-VL-3B`) and Dataset Split** are downloaded, checksummed, and cached.
5. [X]  **The Metric and Deterministic Regex Parser** have achieved a 0% crash rate on pilot data.

Once frozen, **you are forbidden from changing the research question**. You execute the pipeline to completion, regardless of whether the final result confirms or refutes $H_1$.

---

## 25. End-to-End Thesis Execution

A professional research codebase is not a disorganized collection of Jupyter Notebooks named `untitled_final_v2.ipynb`. It is a modular, deterministic, automated pipeline.

```
THESIS REPOSITORY DIRECTORY ARCHITECTURE:
├── configs/
│   ├── base_config.yaml           # Frozen seeds, precision (FP16), hardware flags
│   └── experiments/
│       ├── arm1_unconstrained.yaml
│       ├── arm2_placebo.yaml
│       └── arm3_verbalization.yaml
├── src/
│   ├── data/
│   │   ├── loader.py              # Deterministic dataset streaming & caching
│   │   └── validator.py           # Verification of conflict pairs and image hashes
│   ├── models/
│   │   └── vlm_runner.py          # Qwen2.5-VL loader with SDPA attention optimization
│   ├── interventions/
│   │   ├── prompt_templates.py    # Exact, immutable prompt strings across all arms
│   │   └── placebos.py            # Length-matched neutral control generators
│   └── evaluation/
│       ├── parser.py              # Deterministic regex answer extractor
│       └── metrics.py             # Odds Ratio, McNemar's, Δ_arb, and 95% CIs
├── scripts/
│   ├── run_pilot.py               # N = 100 fast verification script
│   ├── run_full_benchmark.py      # Resumable, checkpointed main execution script
│   └── generate_figures.py        # Publication-ready KaTeX/matplotlib plotting
└── outputs/
    ├── logs/                      # Structured JSONL run logs (per-sample outputs)
    ├── checkpoints/               # Progress states for long Colab runs
    └── tables/                    # Auto-generated LaTeX tables for the thesis
```

### Defensive Engineering Directives

* **Checkpoint Every 50 Samples:** Google Colab Pro will disconnect without warning. Your runner must save state after every 50 samples to a local JSONL file. On restart, the script reads existing sample IDs and resumes automatically.
* **Log Everything in JSONL:** Every logged sample must contain:
  `{"sample_id": 1042, "arm": "arm3_verbalization", "prompt_tokens": 142, "generated_text": "...", "parsed_decision": "Textual", "ground_truth": "Textual", "wall_time_sec": 1.42}`.
* **Never Copy-Paste into Excel:** All final tables and figures must be generated directly from raw JSONL logs via Python scripts (`generate_figures.py`). Zero human intervention between raw logs and LaTeX tables.

---

## 26. From Thesis to Paper

A thesis is comprehensive and documents everything you tried, including failed pilots and exploratory background. A **conference paper** is an aerodynamic, compressed scientific narrative.

```
                    THE PAPER COMPRESSION FORMULA (8-to-9 Pages)
  ┌───────────────────────────────┬────────────────────────────────────────────────────────┐
  │ Paper Section                 │ Target Compression & Focus                             │
  ├───────────────────────────────┼────────────────────────────────────────────────────────┤
  │ 1. Abstract (200 words)       │ Problem -> Gap -> Causal Mechanism -> Result (Δ, OR). │
  ├───────────────────────────────┼────────────────────────────────────────────────────────┤
  │ 2. Introduction (1.5 pages)   │ Figure 1 (The Core Phenomenon) -> The Mystery ->       │
  │                               │ Competing Hypotheses -> The 3 Contributions.           │
  ├───────────────────────────────┼────────────────────────────────────────────────────────┤
  │ 3. Related Work (1 page)      │ Grouped strictly by theoretical paradigm, not paper-by-│
  │                               │ paper summaries. Highlight the missing control.        │
  ├───────────────────────────────┼────────────────────────────────────────────────────────┤
  │ 4. Methodology (2 pages)      │ Mathematical formulation of conflict -> The 3-Arm     │
  │                               │ Factorial Design -> The Placebo Control Specification. │
  ├───────────────────────────────┼────────────────────────────────────────────────────────┤
  │ 5. Experiments & Results      │ Table 1: Main Factorial Result (Δ_arb, OR, p-value).   │
  │    (2.5 pages)                │ Figure 2: Subgroup Stratification.                     │
  │                               │ Table 2: Compute Confound Ablations.                   │
  ├───────────────────────────────┼────────────────────────────────────────────────────────┤
  │ 6. Discussion & Limitations   │ Honest boundary conditions. Where does the mechanism   │
  │    (1 page)                   │ break down? What remains an open question?             │
  └───────────────────────────────┴────────────────────────────────────────────────────────┘
```

### The Strict Writing Order

Never write a paper from Introduction to Conclusion. Follow the professional sequence:

1. **Figures 1 & 2 + Tables 1 & 2** (The empirical proof must exist before words are typed).
2. **Methodology** (Formalize what was actually executed).
3. **Experiments & Results** (Describe the data in the tables).
4. **Introduction** (Set up the mystery that the results solve).
5. **Discussion & Limitations** (Bound your claims).
6. **Related Work** (Position against closest papers).
7. **Abstract & Title** (Distill the complete story into 200 words).

---

## 27. Realistic Research Timeline for an Undergrad Researcher

```
                                  16-WEEK RESEARCH TIMELINE
  ┌──────────────┬─────────────────────────────────────────────────────────────────────────┐
  │ Weeks 1 - 2  │ THE DISCOVERY & TRIAGE PHASE                                            │
  │              │ * Audit failure modes in Qwen2.5-VL-3B.                                 │
  │              │ * Run 10-Stage Literature Search; catalog closest work.                 │
  │              │ * Formulate 3 competing candidate questions in Question Ledger.         │
  ├──────────────┼─────────────────────────────────────────────────────────────────────────┤
  │ Weeks 3 - 4  │ THE ADVERSARIAL KILL PHASE                                              │
  │              │ * Execute the 48-Hour Idea Kill Checklist on all 3 ideas.               │
  │              │ * Run Micro-Pilot (N = 50) for the surviving candidate.                 │
  │              │ * Verify that placebo control does not explain the effect.              │
  ├──────────────┼─────────────────────────────────────────────────────────────────────────┤
  │ Week 5       │ THE QUESTION FREEZE                                                     │
  │              │ * Lock H1 vs H0. Checksum dataset split. Lock prompt templates.         │
  │              │ * Produce formal 2-page Experiment Specification document.              │
  ├──────────────┼─────────────────────────────────────────────────────────────────────────┤
  │ Weeks 6 - 8  │ INFRASTRUCTURE & CALIBRATED PILOT                                       │
  │              │ * Build modular pipeline: vlm_runner.py, parser.py, metrics.py.         │
  │              │ * Run N = 200 Calibrated Pilot. Confirm 0% parser crashes.              │
  │              │ * Verify memory consumption <= 14GB VRAM on Colab GPU.                  │
  ├──────────────┼─────────────────────────────────────────────────────────────────────────┤
  │ Weeks 9 - 11 │ FULL BENCHMARK EXECUTION & ABLATIONS                                    │
  │              │ * Execute N = 1,600+ across all 3 arms (batched with checkpoints).      │
  │              │ * Run subgroup stratification (color, shape, spatial, complex).         │
  │              │ * Run compute confound ablations (token length sweeps).                 │
  ├──────────────┼─────────────────────────────────────────────────────────────────────────┤
  │ Weeks 12 - 13│ STATISTICAL ANALYSIS & AUDIT                                            │
  │              │ * Calculate Odds Ratios, McNemar's paired tests, and 95% CIs.           │
  │              │ * Perform adversarial failure audit: why did the remaining 25% fail?    │
  │              │ * Generate publication-quality vector plots (PDF/SVG).                  │
  ├──────────────┼─────────────────────────────────────────────────────────────────────────┤
  │ Weeks 14 - 15│ THESIS DRAFTING & LATEX COMPILATION                                     │
  │              │ * Compile thesis chapters directly from experimental logs.              │
  │              │ * Solicit adversarial review from peers / advisors.                     │
  ├──────────────┼─────────────────────────────────────────────────────────────────────────┤
  │ Week 16      │ THESIS DEFENSE & CONFERENCE PAPER CONDENSATION                          │
  │              │ * Finalize undergraduate thesis submission.                             │
  │              │ * Compress into 8-page conference draft (CVPR / NeurIPS / ICLR track).  │
  └──────────────┴─────────────────────────────────────────────────────────────────────────┘
```

---

## 28. Personal Failure Modes Autopsy (Reverse-Engineered from Workspace)

By auditing your historical trajectory across Medical Imaging, Bengali VLMs, and Causal Modality Conflict, we can isolate the exact cognitive traps that caused topic-search overwhelm:

```
========================================================================================================================
HISTORICAL PHASE         THE FAILURE TRAP                      THE ROOT CAUSE                  THE PERMANENT PROTOCOL FIX
========================================================================================================================
Phase 1:                 The "High-Prestige Domain Trap"       Choosing a topic based on       Strict Compute Pre-Filter:
Medical Imaging & FL     (HAM10000, FeTS-2022,                 perceived domain importance     Every idea must fit within 16GB
(ISIC Melanoma, Tumor    Federated Learning).                  rather than mechanistic         VRAM and utilize open, non-
Segmentation)                                                  tractability on local compute.  gated datasets.
------------------------------------------------------------------------------------------------------------------------
Phase 2:                 The "Dataset Swap Trap"               Believing that applying an      The Mechanistic Imperative:
Bengali VLM Exploration  (Translating English VQA benchmarks   existing model to a regional    Never swap a dataset without an
(Cultural Grounding,     to Bengali without an algorithmic     dataset constitutes scientific  accompanying cognitive, causal,
Language Translation)    or causal mechanism).                 novelty.                        or algorithmic mechanism.
------------------------------------------------------------------------------------------------------------------------
Phase 3:                 The "Unbounded Reading Trap"          Reading 80+ papers sequentially Stop reading at the Saturation
Literature Exploration   (Becoming overwhelmed by infinite     without an adversarial question Horizon. Enforce the 80/15/5
                         competing claims and terminology).    or an MDE kill test.            Pareto Reading Rule.
------------------------------------------------------------------------------------------------------------------------
Phase 4:                 The "AI Sycophancy Trap"              Asking LLMs to "brainstorm      Use AI to attack ideas and write
AI-Assisted Ideation     (Relying on LLMs to suggest novel     topics," which produces fluent  parsing scripts; NEVER rely on AI
                         gaps, yielding synthetic buzzwords).  but untestable academic fluff.  to judge novelty.
------------------------------------------------------------------------------------------------------------------------
Phase 5:                 THE BREAKTHROUGH                      Transitioning to Level 3        THE CANONICAL OPERATING MODEL.
Modality Conflict        (Causal conflict verbalization vs.    Causal Mechanism Discovery      Lock this protocol for all
Arbitration (N = 1,619)  placebo on Qwen2.5-VL-3B).            with controlled interventions.  future research projects.
========================================================================================================================
```

---

## 29. Reusable Research Workspace (The 6 Minimal Artifacts)

Do not drown yourself in dozens of complex productivity templates. A professional researcher maintains exactly **six minimal markdown ledgers** in their repository root:

```
WORKSPACE ARTIFACT ARCHITECTURE:
├── RESEARCH_MAP.md        # The 1-page visual and conceptual map of the territory
├── QUESTION_LEDGER.md     # Surviving vs. Killed research questions and their autopsies
├── EVIDENCE_LEDGER.md     # Primary peer-reviewed claims, exact numbers, and DOIs
├── EXPERIMENT_SPEC.md     # The frozen, immutable specification for the current study
├── RESEARCH_LOG.md        # Daily chronological log of anomalies, decisions, and bugs
└── PAPER_STORY.md         # The evolving 1-page scientific narrative of the paper
```

### Detailed Templates for Core Ledgers

#### 1. `QUESTION_LEDGER.md`

```markdown
# Question Ledger

## Active Frozen Question
* **ID:** Q-03
* **Question:** Does explicit conflict verbalization causally shift source arbitration in Qwen2.5-VL-3B, or is the shift an artifact of test-time compute?
* **Primary Hypothesis (H1):** Verbalization actively steers arbitration away from visual capture, exceeding a length-matched placebo by >= 15% (OR >= 2.0).
* **Null Hypothesis (H0):** A length-matched neutral placebo prompt reproduces the verbalization arbitration shift within 3.0%.
* **Freeze Date:** 2026-03-15
* **Status:** FROZEN & IN EXECUTION

## Killed Questions Ledger
* **ID:** Q-01
  * **Question:** Can federated learning improve melanoma segmentation across heterogeneous hospital silos?
  * **Kill Date:** 2025-10-12
  * **Kill Reason:** Out of compute envelope; requires multi-client simulation exceeding local RAM; lacks novel causal mechanism (pure engineering wrapper).
* **ID:** Q-02
  * **Question:** Evaluating zero-shot Bengali cultural grounding in multimodal LLMs.
  * **Kill Date:** 2025-12-04
  * **Kill Reason:** Dataset swap trap. Lacks an algorithmic or cognitive intervention; risks being dismissed as passive evaluation.
```

#### 2. `EXPERIMENT_SPEC.md`

```markdown
# Experiment Specification: Modality Arbitration Factorial

## 1. Model & Environment
* **Model ID:** Qwen/Qwen2.5-VL-3B-Instruct (Revision: main, torch_dtype: float16)
* **Attention Kernel:** PyTorch 2.x Scaled Dot-Product Attention (`attn_implementation="sdpa"`)
* **Hardware Target:** 1x NVIDIA Tesla T4 / V100 (16GB VRAM)
* **Decoding Parameters:** `temperature=0.0`, `max_new_tokens=256`, `do_sample=False`

## 2. Dataset Split
* **Benchmark:** `vlm-modality-research/modality-conflict-arbitration-v2`
* **Total Sample Count:** N = 1,619 balanced conflict pairs
* **Checksum:** sha256:4a8b...9f

## 3. Factorial Treatment Arms
* **Arm 1 (Unconstrained Baseline):** Direct VQA prompt without reasoning instructions.
* **Arm 2 (Placebo Control):** Length-matched neutral prompt ("Examine the image structure and explain its geometry before answering...").
* **Arm 3 (Active Treatment):** Explicit Conflict Verbalization prompt ("Identify any discrepancy between image and text before answering...").

## 4. Evaluation & Parsing
* **Deterministic Regex:** `r"\[\[(Visual|Textual|Uncertain)\]\]"`
* **Primary Metric:** Net Causal Shift (Δ_arb), Odds Ratio (OR), McNemar's paired test (p < 0.001).
```

---

## 30. Stop / Continue / Pivot / Kill Framework

When reviewing your research progress at the end of each week, evaluate your project against this strict operational logic:

```
                            THE DECISION LOGIC TABLE
  ┌───────────┬────────────────────────────────────────────────────────────────────────────┐
  │ DECISION  │ REQUIRED EMPIRICAL EVIDENCE                                                │
  ├───────────┼────────────────────────────────────────────────────────────────────────────┤
  │ CONTINUE  │ Pilot shows statistically significant divergence between Treatment and     │
  │           │ Placebo (OR > 2.0). Parser crash rate = 0%. VRAM stays under 14GB.         │
  ├───────────┼────────────────────────────────────────────────────────────────────────────┤
  │ NARROW    │ Treatment works, but effect is heavily concentrated in one subgroup        │
  │           │ (e.g., color attributes). Narrow question to that specific cognitive mechanism.│
  ├───────────┼────────────────────────────────────────────────────────────────────────────┤
  │ PIVOT     │ Active treatment matches placebo, but both reveal a major unexpected       │
  │           │ phenomenon (e.g., post-hoc rationalization). Pivot to study the new discovery.│
  ├───────────┼────────────────────────────────────────────────────────────────────────────┤
  │ FREEZE    │ MDE on N = 100 succeeds. All 5 Freeze Gate criteria are satisfied.        │
  │           │ Cease all literature search and lock repository for production execution. │
  ├───────────┼────────────────────────────────────────────────────────────────────────────┤
  │ KILL      │ Gap is occupied by a recent preprint; OR placebo matches treatment exactly;│
  │           │ OR dataset requires manual cleaning exceeding 40 hours. Kill immediately. │
  └───────────┴────────────────────────────────────────────────────────────────────────────┘
```

---

## 31. One-Page Daily Research Playbook

Keep this checklist pinned to your workstation screen. Review it every morning before opening VS Code or reading papers:

```
========================================================================================
                      THE RESEARCHER'S DAILY MORNING CHECKLIST
========================================================================================

[ ] 1. EPISTEMIC SANITY CHECK
    - Am I working on my FROZEN research question, or did I get distracted by a shiny new
      paper on Twitter/arXiv this morning?
    - If my idea is not in QUESTION_LEDGER.md, I am forbidden from coding it today.

[ ] 2. COMPUTE ENVELOPE VERIFICATION
    - Will what I plan to run today execute completely within my 16GB Colab Pro envelope?
    - Am I logging per-sample outputs in structured JSONL with automated checkpoints?

[ ] 3. THE ADVERSARIAL CONTROLS CHECK
    - Am I running an unconstrained intervention without its length-matched placebo?
    - If yes, STOP. Write the placebo control before launching the script.

[ ] 4. DETERMINISTIC METRIC CHECK
    - Am I evaluating outputs with an uncalibrated LLM judge or stochastic scoring?
    - If yes, STOP. Write a deterministic regex parser.

[ ] 5. RESEARCH LOGGING
    - Did I log yesterday's anomalies, memory spikes, or failed runs in RESEARCH_LOG.md?
    - Every failure is empirical data; never let a failed run vanish without an autopsy.
========================================================================================
```

---

## 32. Final "If I Start a New Research Area Tomorrow" Guide

When entering a completely unfamiliar AI/ML territory tomorrow (e.g., *Diffusion Model Safety*, *State-Space Models*, or *Agentic Tool Grounding*), execute this exact 7-day bootstrap sequence:

```
                            THE 7-DAY BOOTSTRAP PROTOCOL
  ┌──────────────┬─────────────────────────────────────────────────────────────────────────┐
  │ DAY 1        │ TERRITORY SCOPING & BENCHMARK DISCOVERY                                 │
  │              │ * Read 3 survey papers strictly for terminology and benchmark names.    │
  │              │ * Identify the #1 open-source model and the #1 standard benchmark.      │
  │              │ * Construct the initial 1-page Field Map.                               │
  ├──────────────┼─────────────────────────────────────────────────────────────────────────┤
  │ DAY 2        │ INSTRUMENTATION & BASELINE REPLICATION                                  │
  │              │ * Download the open-source model and 50 samples of the benchmark.        │
  │              │ * Run zero-shot inference locally or on Colab.                          │
  │              │ * Confirm that you can reproduce standard baseline accuracy on N = 50.  │
  ├──────────────┼─────────────────────────────────────────────────────────────────────────┤
  │ DAY 3        │ PERTURBATION & ANOMALY HARVESTING                                       │
  │              │ * Subject the model to edge cases: corrupt inputs, invert tokens, swap  │
  │              │   premises, introduce conflicting priors.                               │
  │              │ * Observe where the system breaks down. Record the top 3 anomalies.     │
  ├──────────────┼─────────────────────────────────────────────────────────────────────────┤
  │ DAY 4        │ FOCUSED LITERATURE & ADVERSARIAL SEARCH                                 │
  │              │ * Execute the 10-Stage Literature Search on the observed anomalies.     │
  │              │ * Identify the dominant explanation in the literature.                  │
  │              │ * Formulate the competing alternative explanation (confound/artifact).  │
  ├──────────────┼─────────────────────────────────────────────────────────────────────────┤
  │ DAY 5        │ MDE FORMULATION & THE 48-HOUR KILL TEST                                 │
  │              │ * Formulate H1 vs H0.                                                   │
  │              │ * Design a 3-arm MDE: Baseline, Placebo Control, Active Treatment.      │
  │              │ * Write the deterministic regex parser and JSONL logger.                │
  ├──────────────┼─────────────────────────────────────────────────────────────────────────┤
  │ DAY 6        │ EXECUTION OF THE MDE (N = 100)                                          │
  │              │ * Execute the MDE script on Colab Pro (<= 60 minutes compute).           │
  │              │ * Calculate Odds Ratio and Net Causal Shift (Δ).                        │
  │              │ * DECISION GATE: Did the effect survive the placebo? If NO -> KILL.     │
  ├──────────────┼─────────────────────────────────────────────────────────────────────────┤
  │ DAY 7        │ QUESTION FREEZE & PIPELINE SCALING                                      │
  │              │ * If the MDE survived, lock the question in QUESTION_LEDGER.md.         │
  │              │ * Author EXPERIMENT_SPEC.md.                                            │
  │              │ * Transition to the Inner Execution Pipeline.                           │
  └──────────────┴─────────────────────────────────────────────────────────────────────────┘
```

---

### Epilogue: The Scientific Mindset

Science does not reward the researcher who reads the most papers or runs the most unprincipled experiments. It rewards the researcher who has the discipline to **isolate a single causal mystery, construct an airtight placebo control, and follow the empirical evidence wherever it leads—especially when it proves their initial hypothesis wrong.**

This playbook is your operational compass. Keep it beside your keyboard, execute its protocols without compromise, and produce research that withstands the most hostile scientific scrutiny.
