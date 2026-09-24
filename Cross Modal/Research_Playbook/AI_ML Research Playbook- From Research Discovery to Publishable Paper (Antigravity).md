
# AI/ML Research Playbook: From Research Discovery to Publishable Paper

### *A Practical Research Operating Manual Reconstructed from Senior AI/ML Practice and an Undergraduate Empirical Journey*

---

## Metadata & Evidence Provenance

* **Principal Researcher / Candidate:** Mohammad Zahed Hossen (Technical Lead, Final-Year BSc CSE)
* **Hardware & Compute Boundaries:** Local AMD Ryzen 5 5600G (6C/12T, 8 GB RAM, no local CUDA) $\Longleftrightarrow$ Google Colab Pro (NVIDIA T4 / V100 16 GB VRAM, CUDA 13.0, PyTorch 2.x SDPA, $\le 3\text{B}$ parameter models).
* **Evidence Base:** Complete workspace forensic audit across 87 research dossiers, candidate comparison scorecards, diagnostic pilot traces (`prefreeze_pilot.py`, `prefreeze_pilot_v2.py`), production harnesses (`production_experiment_harness_v3.py`), and the full population empirical census ($N = 1,619$, $\Delta_{\text{arb}} = +63.74\text{ pp}$, $p = 1.20 \times 10^{-215}$).
* **Three Knowledge Levels Enforced Throughout:**
  * **`[L1 — Established Practice]`**: Standard operating procedures, methodologies, and norms practiced by elite academic and industrial AI/ML researchers.
  * **`[L2 — Inferred from Your Record]`**: Behavioral patterns, structural failure modes, dead-ends, and breakthroughs reverse-engineered from your documented exploration across Medical Imaging, Federated Learning, Multimodal Agents, and Vision-Language Arbitration.
  * **`[L3 — Workflow Recommendation]`**: Concrete, non-negotiable operational directives designed for your exact compute, team, and undergraduate timeline constraints.

---

# SECTION 1: Executive Overview & The Epistemic Core

### 1.1 The Two Research Paradigms

Most junior researchers get trapped in **Level 2 Benchmark Tinkering**:

$$
\text{Take Architecture } A + \text{Loss Function } B \longrightarrow \text{Apply to Dataset } C \longrightarrow \text{Tune until } +1.2\% \longrightarrow \text{Claim "Novelty"}

$$

This paradigm is intellectually exhausting, methodologically fragile, and psychologically destabilizing. You live in constant fear that an industrial lab with 1,000 H100s will release a scaled checkpoint that obsoletes your six months of work overnight.

Senior AI/ML researchers operate under **Level 3 Causal Mechanism Discovery**:

$$
\text{Observe Anomaly} \longrightarrow \text{Isolate Competing Explanations } (H_1 \text{ vs } H_0) \longrightarrow \text{Design Single-Difference Contrast} \longrightarrow \text{Execute Placebo-Controlled Experiment} \longrightarrow \text{Defensible Causal Claim}

$$

In Level 3 research:

1. Science is the systematic reduction of uncertainty about how artificial cognitive systems function, fail, and arbitrate representations.
2. A contribution is not a fragile leaderboard score; it is an **empirical explanation backed by counterfactual evidence** that separates competing hypotheses.
3. Negative and null results carry identical scientific value to positive results, provided the experiment was equipped with a positive control capable of producing the effect.

```
       [ Level 2: Benchmark Tinkering ]              [ Level 3: Causal Mechanism Discovery ]
  Goal:    Beat benchmark by +1.5%             Goal:    Explain why the system behaves this way
  Action:  Stack methods, tune tricks          Action:  Isolate variables, run placebo controls
  Output:  Fragile leaderboard score           Output:  Defensible causal explanation
  Risk:    Crushed by scale and compute        Durability: Survives scale; adds permanent knowledge
```

### 1.2 The Five Core Axioms of This Playbook

* **C1: Research questions are found, not invented.** Strong questions emerge from empirical anomalies, missing controls, or contradictions in published literature—never from open-ended ideation.
* **C2: A gap is an unperformed experiment, not an unspoken sentence.** The fact that "nobody has written your exact sentence" is meaningless. Novelty exists only when nobody has run the specific empirical contrast that separates two plausible explanations.
* **C3: The most valuable early research activity is destructive.** The first 14 days of an investigation must be dedicated to aggressively attempting to *kill* your idea before investing months of compute and engineering.
* **C4: Novelty is a property of the closest-work comparison, not of your proposal in isolation.** You cannot evaluate novelty by contemplating your idea. You can only evaluate novelty by placing your experimental design side-by-side against the single closest prior paper.
* **C5: The Single-Difference Law governs all interpretable experiments:**
  $$
  \text{Treatment Output} - \text{Control Output} = \text{Causal Effect of Exactly One Manipulated Variable}

  $$

  If your treatment modifies prompt instructions, token length, formatting, and sampling parameters simultaneously, your experiment has four unmodeled confounds and is scientifically uninterpretable.

---

# SECTION 2: How Experienced Researchers Actually Work

### 2.1 Working from Anomalies Rather than Broad Fields

**`[L1]`** Novices pick a broad field (e.g., "Multimodal Agents"), try to "read the field," and become paralyzed because literature has no physical boundary. Senior researchers maintain a private ledger of **concrete anomalies**:

* *An anomaly in a figure:* A curve in an influential paper that dips unexpectedly at a specific scale.
* *An anomaly in a baseline:* A complex method outperforming a baseline only because the baseline was undertuned or denied matched test-time compute.
* *An anomaly in model output:* An open-weight model solving an arithmetic problem directly, but hallucinating wildly when a syntactically identical but conflicting premise is prepended.
* *An anomaly in the limitations section:* An author conceding: *"We evaluated exclusively under forced-choice prediction; we did not test whether models detect the contradiction or express uncertainty."* (The exact crack in *Which Source Wins?* [§6] that unlocked your canonical thesis).

### 2.2 The Reading Inversion

**`[L1]`** Senior researchers do not read 200 papers cover-to-cover. They read across four tiered speeds:

1. **The 60-Second Sweep:** Title, abstract, Figure 1, and Conclusion. Goal: *Does this paper investigate the identical causal contrast?* If yes $\to$ download and scrutinize. If no $\to$ discard.
2. **The 10-Minute Card:** Extract into your field map: *What was the claim? What was the intervention? What was the control? What was the primary limitation?*
3. **The 2-Hour Interrogation:** Read methodology, ablation tables, and appendices of the 3–5 anchor papers. Goal: *What confound did the authors fail to control for? What did they assume without proving?*
4. **The Codebase Autopsy:** Clone the official repository and inspect the data-loader and evaluation scripts. You often discover that reported benchmark scores rely on undisclosed prompt engineering, filtering tricks, or data leakage.

### 2.3 The Mindset: Adversarial Prosecutor vs. Passive Student

* **The Passive Student:** Reads a paper, accepts the authors' explanation at face value, and looks for an incremental extension: *"They tested this on English; maybe I can test it on Bengali."*
* **The Adversarial Prosecutor:** Reads assuming the authors may be suffering from confirmation bias. Asks:
  * *"Did the authors' intervention cause the gain, or was it simply an artifact of increased token length (extra test-time compute)?"*
  * *"Did the representation probe isolate a genuine cognitive circuit, or did it fit a linear shortcut in the residual stream?"*
  * *"Could a 1-line heuristic achieve 85% of this reported performance?"*

---

# SECTION 3: Why Research Is Not Linear (The Dual-Loop Model)

**`[L1]`** Textbooks teach a fraudulent linear pipeline: $\text{Topic} \to \text{Literature} \to \text{Gap} \to \text{Question} \to \text{Code} \to \text{Experiment} \to \text{Thesis}$. When an experiment inevitably fails, linear thinkers freeze, assume their intellect is deficient, and abandon the project.

Real AI/ML research is governed by two interlocking loops: the **Outer Discovery Loop** (fast, flexible, destructive) and the **Inner Execution Pipeline** (rigid, deterministic, frozen).

```
========================================================================================
                        THE OUTER DISCOVERY LOOP (Fast & Destructive)
========================================================================================
         [Research Territory]
                 │
                 ▼
       [Observed Phenomenon] ◄─────────────────────────────────────────────┐
                 │                                                         │
                 ▼                                                         │
      [Literature Tension / Anomaly]                                       │
                 │                                                         │
                 ▼                                                         │
   [Competing Explanations (H1 vs H0)]                                     │
                 │                                                         │
                 ▼                                                         │
    [Feasibility & Data Access Gate] ─── FAIL ──► [Kill Idea Cheaply]     │
                 │ PASS                                                    │
                 ▼                                                         │
      [Minimum Diagnostic Pilot] (N = 20)                                  │
                 │                                                         │
                 ├──────────────────────── Unexpected Anomaly Discovered ──┘ (PIVOT)
                 │                                                         │
                 ▼ Robust Signal & Validated Controls                      │
===========================================================================│============
                        THE INNER EXECUTION PIPELINE (Rigid & Frozen)      │
===========================================================================│============
                 │                                                         │
                 ▼                                                         │
   [FREEZE: Experiment Specification] ─────────────────────────────────────┘
                 │
                 ▼
   [Production Harness Engineering (FP16/SDPA, Checkpointing, Regex)]
                 │
                 ▼
   [Full Population Census / Multi-Seed Run]
                 │
                 ▼
   [Deterministic Statistical Audit (McNemar, Fisher, Exact Match Cross-Over)]
                 │
                 ▼
   [Mechanistic Interpretation & Symmetrical Contribution Claim]
                 │
                 ▼
   [Thesis Defense / Peer-Reviewed Manuscript]
```

**`[L2]` Evidence from your record:** Your research journey stalled when you attempted to execute linear discovery across 5 distinct domains (Medical FL, Multimodal Agents, Long-Context VLM, Cultural Steering, Conflict Arbitration). The breakthrough occurred only when you ran the **diagnostic pilot ($N = 20$)** in Candidate A. That pilot discovered the unexpected "Neither" calculation ($85\%$ in Arm 1) and legitimate epistemic abstentions ($25\%$ in Arm 3), which dynamically shifted the research question from a simple preference measurement into an empirical discovery of epistemic source arbitration.

---

# SECTION 4: The Epistemic Taxonomy (Separating Concepts)

**`[L1 / L2]`** The most destructive intellectual failure during topic discovery is treating fundamentally different conceptual levels as interchangeable thesis topics. You must strictly enforce this 11-tier conceptual hierarchy:

```
[Level 1: Research Area]         Vision-Language Models (VLMs)
         │
[Level 2: Research Territory]    Multimodal decision arbitration under conflicting evidence
         │
[Level 3: Phenomenon]            When visual and textual inputs provide contradictory numerical premises,
                                 VLMs exhibit severe modality capture (~90% visual dominance)
         │
[Level 4: Observation]           In direct answering, Qwen2.5-VL-3B outputs the image-derived answer
                                 in 89.5% of clean arithmetic conflict pairs
         │
[Level 5: Existing Claim]        Prior literature asserts this occurs because cross-attention layers
                                 are hardwired to prioritize visual tokens in early layers
         │
[Level 6: Alternative Expl.]     The visual preference is an unfaithful, post-hoc rationalization;
                                 explicit verbalization of the conflict will steer internal circuits
                                 toward alternate textual evidence
         │
[Level 7: Research Gap]          Prior work evaluated models exclusively under direct forced-choice;
                                 whether conflict verbalization causally steers multimodal arbitration
                                 remains completely unmeasured
         │
[Level 8: Research Question]     Does explicit conflict verbalization causally steer multimodal decision
                                 arbitration toward alternate textual evidence, or does it merely
                                 rationalize an entrenched visual modality preference?
         │
[Level 9: Hypotheses]            H1: Verbalization breaks visual capture (Δ_arb > +20 pp, p < 0.001)
                                 H0: Verbalization is post-hoc rationalization (Δ_arb ≈ 0 pp)
         │
[Level 10: Experiment]           A 3-arm factorial protocol comparing Direct Answering (Arm 1),
                                 a Length-Matched Neutral Placebo Prompt (Arm 2), and an
                                 Explicit Conflict Verbalization Prompt (Arm 3) on N = 1,619 pairs
         │
[Level 11: Contribution]         Empirical proof that conflict verbalization causally reduces visual
                                 capture by 63.7 pp (OR = 24.57, p < 10^-215), triggering an exact-match
                                 arithmetic cross-over from 7.6x image dominance to 3.1x text dominance
```

### Contrast with an Architecture/Engineering Example:

* **Research Area:** Multimodal Agent Tool Use.
* **Research Territory:** Dynamic image resolution and active perception.
* **Phenomenon:** Agents invoke external zoom/crop tools even on images where target objects are clearly legible.
* **Observation:** AdaTooler-V calls `crop_image` on $42\%$ of queries that the base model answers correctly without tools.
* **Existing Claim:** Agents suffer from "blind invocation" due to coarse outcome-based RL rewards.
* **Alternative Explanation:** Performance gains attributed to visual crops are confounded by test-time compute (extra autoregressive tokens and reasoning steps generated after the tool call).
* **Research Gap:** No existing study has benchmarked learned active perception agents against a compute-matched placebo where the model receives an irrelevant blank crop of identical token dimensions.
* **Research Question:** Do learned active perception policies outperform static uniform image tiling when total inference FLOPs and context length are held strictly equal?
* **Hypothesis:** $H_1$: Learned policies identify spatial regions with information density exceeding uniform slicing. $H_0$: Performance differences collapse when uniform slicing receives matched compute.
* **Experiment:** Compare agent trajectory accuracy against uniform 4-quadrant tiling with equalized autoregressive token budgets.
* **Contribution:** Resolves whether active perception agents learn genuine spatial utility or simply exploit inference compute expansion.

---

# SECTION 5: Where Strong Research Questions Actually Come From

**`[L1]`** Elite research questions are not dreamed up in isolation. They are excavated from 14 concrete structural cracks in the literature:

```
                                 WHERE RESEARCH QUESTIONS COME FROM
                               
  [1. Surprising Failure Mode]        [2. Missing Control Experiment]     [3. Contradiction Between Papers]
  Model solves X alone and Y alone,   Method works, but authors didn't   Paper A claims text dominates;
  but collapses when X & Y co-occur.  run a length-matched placebo.      Paper B claims vision dominates.
               │                                    │                                    │
               └────────────────────────────────────┼────────────────────────────────────┘
                                                    │
  [4. Boundary Condition Failure]                   ▼                   [5. Measurement / Metric Defect]
  Claim demonstrated on 2D grids;     ┌──────────────────────────┐      Reported metric (e.g., AURC) penalizes
  does it hold on natural photos?     │  THE 14 SOURCES OF REAL  │      baseline error rather than ranking quality.
                                      │    RESEARCH QUESTIONS    │
  [6. Benchmark Artifact Shortcut]    └─────────────┬────────────┘      [7. Unexplained Empirical Phenomenon]
  Model achieves 80% accuracy by                    │                   Model generates correct numerical answer
  reading only the question prompt.                 │                   while citing incorrect visual evidence.
               ┌────────────────────────────────────┼────────────────────────────────────┐
               │                                    │                                    │
  [8. Unchecked Linear Extrapolation]  [9. Post-Hoc vs Causal Confusion] [10. Unmodelled Confounders]
  Assumed that scaling parameters     Does CoT actively steer decision,   Token count, prompt length, or image
  monotonically repairs calibration.  or rationalize prior logits?        resolution driving reported gains.
  
  [11. Unverified Architectural Hub]  [12. Fragile Toy-to-Real Transfer] [13. Negative Transfer of Adaptation]
  Claim that Layer 18 holds concept   Synthetic shape binding failing     Fine-tuning on target domain destroys
  without running linear probes.      on complex COCO scenes.             out-of-distribution calibration.
  
                                      [14. Epistemic Abstention Failure]
                                      Models forced into binary choices
                                      rationalizing false premises.
```

### Forensic Walkthrough of the Top 5 Sources:

1. **The Missing Control Experiment:** An author shows that adding a reasoning step improves performance. *The prosecutor asks:* Did the reasoning step help because of its semantic content, or because the model had $500$ additional tokens of test-time compute to disperse attention? *Your thesis exploited this exact crack by introducing Arm 2 (Length-Matched Neutral Placebo).*
2. **The Explicit Concession in "Future Work":** In Section 6 of *Which Source Wins?*, the authors explicitly state: *"We evaluate models exclusively under direct zero-shot answering. We do not test whether models detect the contradiction, express uncertainty, or abstain."* That sentence is an open invitation for a thesis.
3. **The Contradiction Between Papers:** Paper A (*Which Source Wins?*) claims language models exhibit overwhelming text dominance in multimodal conflicts. Paper B (*Mementos*) claims models exhibit overwhelming visual bias. *The question:* What unmodeled task property (e.g., degradation level, prompt phrasing, task complexity) causes this modality flip?
4. **The Boundary Condition Stress Test:** Hasani et al. (ICML 2026) claim "Grounding IDs" solve attribute binding in synthetic grid worlds. *The prosecutor asks:* Does this mechanism survive when tested on natural photographic scenes with cluttered backgrounds and overlapping objects?
5. **The Benchmark Shortcut Audit:** Models score $78\%$ on a visual question answering benchmark. *The prosecutor asks:* What happens if you blank out the image completely? If the model still gets $74\%$, the benchmark is measuring language priors, not multimodal reasoning.

---

# SECTION 6: How Senior Researchers Search Literature

**`[L1]`** Novices type broad keywords into Google Scholar (e.g., `"vision language model conflict"`), get 45,000 results, read five random abstracts, and feel overwhelmed.

Senior researchers execute a **10-Station Evolutionary Search Funnel**. They search by *causal intervention* and *measurement metric*, never by generic topic names:

```
                                THE 10-STATION SEARCH FUNNEL
                              
  [Station 1: Phenomenon Search]        "multimodal contradiction" "modality bias" "visual capture"
                 │
  [Station 2: Explanation Search]       "cross-attention dominance" "modality competition mechanics"
                 │
  [Station 3: Alternative Expl.]        "unfaithful rationalization" "post-hoc CoT" "visual inertia"
                 │
  [Station 4: Confound Search]          "test-time compute confounding" "prompt length bias VLM"
                 │
  [Station 5: Replication Search]       "Qwen2.5-VL modality conflict" "open-weight VLM arbitration"
                 │
  [Station 6: Boundary Search]          "clean image vs degraded visual conflict" "pristine legibility"
                 │
  [Station 7: Intervention Search]      "conflict verbalization" "explicit contradiction prompting"
                 │
  [Station 8: Benchmark Search]         "modality-conflict-arbitration" "CLASH benchmark" "WhatIfVis"
                 │
  [Station 9: Dataset Access Search]    site:huggingface.co/datasets "conflict" "arbitration"
                 │
  [Station 10: Pre-emption Sweep]       arxiv.org "Which Source Wins" "cross-modal source arbitration"
```

### Real-World Search Query Comparison:


| What the Novice Searches    | What the Senior Researcher Searches                                                                                           | Why the Senior Query Works                                                                                        |
| :---------------------------- | :------------------------------------------------------------------------------------------------------------------------------ | :------------------------------------------------------------------------------------------------------------------ |
| `VLM hallucinationBengali`  | `"representation steering" AND ("cross-lingual" OR "multilingual") AND ("activation addition" OR "CAA")`                      | Identifies the actual mathematical mechanism (*BabelSteering*) rather than surface-level geographic applications. |
| `multimodal agent tools`    | `("AdaTooler" OR "ToolGate") AND ("tool utility" OR "pre-call gating") AND ("counterfactual" OR "ablation")`                  | Immediately discovers that tool-utility prediction is already occupied by top-tier papers.                        |
| `image text conflict in AI` | `("modality dominance" OR "source arbitration") AND ("Chain-of-Thought" OR "verbalization") AND ("faithfulness" OR "causal")` | Surrounds the exact intersection of Lanham et al. (faithfulness) and*Which Source Wins?* (arbitration).           |

---

# SECTION 7: How Senior Researchers Read and Interrogate Papers

**`[L1]`** Reading a paper from beginning to end is the least efficient way to understand its scientific value. Use the **6-Pass Interrogation Protocol**:

```
                              THE 6-PASS INTERROGATION PROTOCOL
                            
  [Pass 1: 60 Seconds]   Abstract + Figure 1 + Conclusion
                         Q: What is the single causal claim? Does it directly overlap my contrast?
                                     │
  [Pass 2: 3 Minutes]    Inspect Tables 1 & 2 + Experimental Setup
                         Q: What baseline did they compare against? Did the baseline receive equal compute?
                                     │
  [Pass 3: 5 Minutes]    Inspect the Ablation Table (Table 3 or 4)
                         Q: Which component actually drove the score? Does the effect collapse without trick X?
                                     │
  [Pass 4: 10 Minutes]   Read the Limitations Section & Appendices
                         Q: What did the authors admit they did not test? Where did the model fail?
                                     │
  [Pass 5: 30 Minutes]   Audit Data Curation & Evaluation Metrics
                         Q: Was evaluation deterministic or LLM-judged? Is the benchmark publicly hosted?
                                     │
  [Pass 6: 2 Hours]      Codebase Autopsy (Only if Paper is Candidate Closest-Work)
                         Clone repo, inspect prompt strings, evaluate tokenization, check for test leakage.
```

### Red Flags That Immediately Devalue a Paper:

* **The Invisible Baseline:** The authors propose a complex 4-stage agent framework but compare it only to zero-shot direct answering, omitting a simple few-shot or length-matched CoT baseline.
* **The LLM-as-a-Judge Echo Chamber:** The authors evaluate their model using GPT-4-turbo without reporting human agreement, prompt sensitivity, or position bias.
* **The Aggregate-Only Mask:** The paper reports only macro-average accuracy across 12 datasets, concealing the fact that the method degraded performance on 7 of them.
* **The Un-reproducible Benchmark:** The dataset is hosted on a Google Drive link that requires email approval, or relies on deprecated private APIs.

---

# SECTION 8: Building a Field Map Without Drowning in Notes

**`[L1 / L3]`** Do not build massive, unreadable Notion or Obsidian databases with 500 paper summaries. A working field map is a **single living Markdown document (`Field_Map.md`)** that structures a territory into four quadrants:

```markdown
# FIELD MAP: Multimodal Conflict Arbitration & Modality Reliance

### Quadrant 1: The Foundational Bedrock (The 3 Classic Anchors)
- Lanham et al. (2023): *Measuring Faithfulness in Chain-of-Thought Reasoning* (Text-only CoT perturbation).
- Gururangan et al. (2018): *Annotation Artifacts in NLI* (Unimodal shortcut learning).
- Radford et al. (2021): *CLIP* (Cross-modal representation alignment).

### Quadrant 2: The Active Frontier (Top 3 Direct Competitors, Last 12 Months)
- Which Source Wins? (arXiv:2608.17205, Aug 2026): Proves task-dependent modality dominance under degradation. (Fatal Concession: Forced-choice direct answering only; no conflict detection or abstention).
- CLASH (arXiv:2511.19199, Nov 2025): Benchmarks cross-modal contradiction detection as a static classification task. (Limitation: Evaluates abstention trigger; does not test causal decision redirection).
- RH-Bench (NeurIPS 2025, arXiv:2505.21523): Proves long reasoning traces cause visual attention degradation.

### Quadrant 3: Public Benchmarks & Infrastructure
- `vlm-modality-research/modality-conflict-arbitration-v2` (Hugging Face, 12,952 pairs, clean subset N = 1,619).
- `WhatIfVis` (3,049 items) — STATUS: BROKEN / UN-DOWNLOADABLE.

### Quadrant 4: The Open Tension / Scientific Anomaly
- Community believes VLMs possess strong visual grounding, yet they default to text in arithmetic reasoning and exhibit 89.5% visual capture under conflict. Does CoT verbalization causally steer arbitration or act as post-hoc rationalization?
```

---

# SECTION 9: Finding the "Closest Existing Work"

**`[L1]`** The single most dangerous trap for an undergraduate is **false novelty**—believing an idea is novel simply because nobody used your exact phrasing.

To find the true closest work, construct a **Defensive Closest-Work Contrast Matrix**:

```
┌────────────────────────────────────────────────────────────────────────────────────────┐
│                          DEFENSIVE CLOSEST-WORK MATRIX                                 │
├──────────────────────┬──────────────────────────────┬──────────────────────────────────┤
│ Dimension            │ Closest Prior Work:          │ Your Proposed Research:          │
│                      │ Which Source Wins? (2026)    │ Causal Conflict Verbalization    │
├──────────────────────┼──────────────────────────────┼──────────────────────────────────┤
│ Primary Question     │ Which modality dominates     │ Does explicit verbalization      │
│                      │ under forced-choice zero-shot│ causally steer arbitration or    │
│                      │ direct answering?            │ rationalize visual capture?      │
├──────────────────────┼──────────────────────────────┼──────────────────────────────────┤
│ Experimental Arms    │ Arm 1: Direct Answering only │ Arm 1: Direct Answering          │
│                      │                              │ Arm 2: Length-Matched Placebo    │
│                      │                              │ Arm 3: Conflict Verbalization    │
├──────────────────────┼──────────────────────────────┼──────────────────────────────────┤
│ Confound Control     │ None (forced binary choice)  │ Matched token compute control    │
├──────────────────────┼──────────────────────────────┼──────────────────────────────────┤
│ Evaluated Behaviors  │ Visual vs. Text preference   │ Visual, Text, Epistemic          │
│                      │                              │ Abstention, Exact Match Cross    │
├──────────────────────┼──────────────────────────────┼──────────────────────────────────┤
│ Primary Finding      │ Task-dependent dominance     │ Verbalization cuts visual capture│
│                      │                              │ by 63.7 pp (p < 10^-215)         │
└──────────────────────┴──────────────────────────────┴──────────────────────────────────┘
```

**The Reviewer Kill-Test:** If a reviewer asks: *"How does this differ from Which Source Wins? (arXiv:2608.17205)?"*, your answer must be immediate and factual:

> *"Which Source Wins evaluated models exclusively under direct zero-shot answering, conceding in Section 6 that they did not test contradiction detection or uncertainty. We introduce a 3-arm factorial protocol with length-matched placebos to isolate whether verbalizing conflict causally redirects multi-step arithmetic circuits or merely rationalizes an entrenched visual prior."*

---

# SECTION 10: Verifying Whether a Literature Gap Is Real

**`[L1]`** Before committing to a candidate gap, subject it to the **10-Question Gap Reality Gauntlet**:

```
                         THE 10-QUESTION GAP REALITY GAUNTLET
                       
  1. Has the question been directly answered in the last 12 months?
     [Action: Search arXiv titles and abstracts with exact intervention verbs].
  
  2. Has it been indirectly answered under different vocabulary?
     [Action: Check if "source arbitration" was solved under "modality competition" or "cue integration"].
  
  3. Is the gap merely a geographic, linguistic, or dataset swap?
     [Action: Does testing this on Bengali reveal a new cognitive principle, or merely confirm English behavior?].
  
  4. Is the missing experiment important, or was it omitted because the outcome is obvious?
     [Action: If the result is 100% predictable from basic geometry or tokenization, kill it].
  
  5. Can the central effect be reproduced by a 1-line heuristic or trivial baseline?
     [Action: Check if a blind text-only model or random choice achieves the baseline score].
  
  6. Could the whole effect be explained by extra test-time tokens (compute confounding)?
     [Action: State the length-matched placebo condition].
  
  7. Is the required benchmark immediately downloadable via Python without credentials?
     [Action: Run load_dataset() in terminal; verify public weights and images].
  
  8. Does inference execute within your hardware envelope (< 16 GB VRAM, < 2 sec/item)?
     [Action: Load model in FP16/SDPA; test a 3-sample batch].
  
  9. Is the evaluation metric deterministic (regex / exact match) rather than LLM-judged?
     [Action: Write the parsing script; confirm zero reliance on proprietary API evaluators].
  
  10. Is the research value SYMMETRICAL?
     [Action: If H1 is rejected and H0 holds, does that negative result still falsify an established claim?].
```

---

# SECTION 11: How Experienced Researchers Kill Ideas Quickly

**`[L1 / L3]`** The most expensive mistake in research is spending four months realizing an idea was dead on Day 2. Senior researchers run an **Adversarial Red Team Sprint** within the first 48 hours of any candidate proposal:

```
                      THE 48-HOUR ADVERSARIAL RED TEAM SPRINT
                    
  [Hour 0–12]   The Pre-emption Attack
                Goal: Find the single paper that renders the proposal redundant.
                Action: Search Google Scholar / Semantic Scholar using method + measurement verbs.
              
  [Hour 12–24]  The Trivial Baseline Attack
                Goal: Prove the problem can be solved without the proposed method.
                Action: Test whether zero-shot prompting or a blind unimodal baseline solves the task.
              
  [Hour 24–36]  The Infrastructure Audit
                Goal: Break the data pipeline before writing a single proposal sentence.
                Action: Run load_dataset(). If data is gated, corrupted, or missing labels -> KILL.
              
  [Hour 36–48]  The Placebo Stress-Test
                Goal: Formulate the confound that will destroy the claim during peer review.
                Action: Design the placebo control. If you cannot isolate the causal variable -> KILL.
```

### Forensic Autopsy of Your Workspace's Three Deprecated Candidates:

1. **Proposal 1 (Reasoning Trace Degradation):**
   * *The Claim:* Long multimodal reasoning traces degrade visual grounding in VLMs.
   * *Why it was killed:* **Pre-emption + Data Failure.** *RH-Bench* (Liu et al., NeurIPS 2025) had already established this exact phenomenon and formalized the $RH\text{-}AUC$ metric. Concurrently, the target benchmark (*WhatIfVis*) was un-downloadable from public hubs.
2. **Proposal 2 (Binding IDs Natural Image Transfer):**
   * *The Claim:* Grounding IDs from synthetic grid worlds transfer to Layer 22 of Qwen2.5-VL to solve natural attribute binding.
   * *Why it was killed:* **Extreme Generalization Risk + Hallucinated Architectural Hub.** The anchor paper (Hasani et al., ICML 2026) operated exclusively on colored geometric shapes. The assumption that visual binding in natural photography resides in Layer 22 was completely unverified by probing.
3. **Proposal 3 (Bengali Cultural VLM Steering):**
   * *The Claim:* Steering activation vectors at Layer 18 injects missing Bengali cultural concepts into VLMs.
   * *Why it was killed:* **Methodological Pre-emption + Linguistic Prior Confound.** *BabelSteering* (arXiv:2608.16577) had already established cross-lingual representation steering to Bengali. Concurrently, *ChitraMiti* proved that VLMs in low-resource settings fail due to overpowering language priors, not missing internal vectors.

---

# SECTION 12: Feasibility During Discovery (The 4 Hard Gates)

**`[L3]`** Never evaluate an idea's scientific elegance independently of its physical execution constraints. An idea must pass all **Four Feasibility Gates** before receiving a single line of production code:

```
┌────────────────────────────────────────────────────────────────────────────────────────┐
│                               THE FOUR FEASIBILITY GATES                               │
├────────────────────┬───────────────────────────────────────────────────────────────────┤
│ Gate 1: Turnkey    │ Can the dataset be loaded via `load_dataset()` or direct open     │
│ Data Access        │ download in under 5 minutes without private agreements or forms?   │
│                    │ [Rule: If data access requires email or CITI training -> REJECT]  │
├────────────────────┼───────────────────────────────────────────────────────────────────┤
│ Gate 2: Compute    │ Does baseline model inference fit completely within single-GPU    │
│ Envelope Bounds    │ Colab Pro (16 GB VRAM) using FP16 / SDPA at <= 2 sec per sample?   │
│                    │ [Rule: 70B models, RL fine-tuning, or multi-GPU training -> REJECT│
├────────────────────┼───────────────────────────────────────────────────────────────────┤
│ Gate 3: Determin-  │ Can outputs be classified using exact-match, numerical regex, or  │
│ istic Evaluation   │ verified ground truth labels without LLM-as-a-judge scoring?      │
│                    │ [Rule: If evaluation requires GPT-4 API grading -> REJECT]        │
├────────────────────┼───────────────────────────────────────────────────────────────────┤
│ Gate 4: Symmetric  │ Is the finding publishable if H1 is supported AND if H1 is rejected│
│ Research Value     │ (null result falsifies an established assumption)?                 │
│                    │ [Rule: If null result means "my code had a bug" -> REJECT]        │
└────────────────────┴───────────────────────────────────────────────────────────────────┘
```

---

# SECTION 13: Designing the Minimum Discriminating Experiment (MDE)

**`[L1]`** Novices design monolithic software architectures that take three months to build before generating a single data point. Senior researchers design the **Minimum Discriminating Experiment (MDE)**—the smallest, simplest controlled contrast capable of separating $H_1$ from $H_0$.

```
                       THE MINIMUM DISCRIMINATING EXPERIMENT
                     
   [Input Item] ──► Conflicting Image-Text Arithmetic Problem (Pristine Legibility)
                            │
         ┌──────────────────┼──────────────────┐
         ▼                  ▼                  ▼
    [ Arm 1 ]          [ Arm 2 ]          [ Arm 3 ]
    Direct Answering   Length-Matched     Conflict
    Baseline           Neutral Placebo    Verbalization
    (Zero-Shot)        ("Describe image   ("State conflict
                       in detail...")     explicitly...")
         │                  │                  │
         ▼                  ▼                  ▼
    [ Output 1 ]       [ Output 2 ]       [ Output 3 ]
    Raw Choice         Choice under       Choice under
                       Compute Scaling    Causal Intervention
         │                  │                  │
         └──────────────────┴──────────────────┘
                            │
                            ▼
     [ Contrast A: Compute Confound ] = Arm 2 - Arm 1
     [ Contrast B: Pure Causal Effect ] = Arm 3 - Arm 2
```

### The Power of the 3-Arm Factorial Protocol:

* If $\text{Arm 3} \neq \text{Arm 1}$, but $\text{Arm 3} = \text{Arm 2}$: **The effect is 100% confounded by test-time compute.** Verbalization did nothing; the model simply benefited from generating more tokens.
* If $\text{Arm 3} \neq \text{Arm 2}$ with $p < 0.001$: **The effect is a genuine causal cognitive shift.** Semantic verbalization physically altered source arbitration independent of token length.

---

# SECTION 14: Baselines, Controls, Metrics, and Evaluation

### 14.1 The Positive Control Requirement

**`[L1]`** An experiment without a positive control is uninterpretable. If your intervention shows zero effect, how do you know your measurement harness was functioning?

* *In Modality Conflict:* Arm 1 (Direct Answering) serves as the positive control for visual capture. If Arm 1 did not exhibit $\sim 85–90\%$ visual capture on clean images, the benchmark would be defective.

### 14.2 Deterministic Parsing vs. LLM-as-a-Judge

**`[L1 / L3]`** LLM-as-a-judge introduces stochastic noise, prompt sensitivity, and self-preference bias. For rigorous thesis defense:

* Use **exact numerical matching**: Strip formatting, extract numbers via strict regex, compare directly against `image_answer` and `text_answer`.
* Separate categorical outcomes deterministically:
  1. `visual_capture`: Model outputs `image_answer`.
  2. `textual_capture`: Model outputs `text_answer`.
  3. `epistemic_abstention`: Model emits verified refusal phrases (*"cannot be determined"*, *"contradictory premises"*).
  4. `neither_arithmetic`: Model executes hybrid arithmetic blending both premises.

---

# SECTION 15: Pilot $\longrightarrow$ Main Experiment Transition

**`[L1 / L2]`** Never launch a full production run ($N > 1,000$) directly from a code editor. Always execute a **Two-Stage Diagnostic Pilot** ($N = 20$ each):

```
                               THE DIAGNOSTIC PILOT LIFECYCLE
                             
     [ Pilot 1: Free-Form Prompting (N = 20) ]
     Script: prefreeze_pilot.py
     Discovered Failures:
     • 85% of direct outputs matched NEITHER answer (hybrid calculation).
     • 25% legitimate epistemic abstentions misclassified as regex parse failures.
     • Extreme token length variance (12 to 240 tokens).
                 │
                 ▼
     [ Structural Repair & Refinement ]
     • Implement strict output formatting contract (#### <answer>).
     • Update regex parser to extract epistemic abstention as a valid outcome.
     • Design length-matched neutral placebo prompt to fix token budget.
                 │
                 ▼
     [ Pilot 2: Structured 2-Shot Prompting (N = 20) ]
     Script: prefreeze_pilot_v2.py
     Discovered Failures:
     • In-context few-shot examples contaminated model arbitration.
     • Pragmatic contradiction impasse under forced binary formatting.
                 │
                 ▼
     [ Production Synthesis & FREEZE ]
     • Eliminate all few-shot demonstrations (Zero-Shot strict system prompting).
     • Lock production harness v3 with automated checkpointing.
     • Launch Full Population Census (N = 1,619).
```

---

# SECTION 16: Handling Unexpected and Negative Results

**`[L1]`** Novices panic when results contradict their hypothesis. Senior researchers understand that **an unexpected, rigorously controlled result is often a superior publication**:

```
┌────────────────────────────────────────────────────────────────────────────────────────┐
│                        THE 4 CLASSES OF EXPERIMENTAL OUTCOMES                          │
├─────────────────────────┬──────────────────────────────────────────────────────────────┤
│ Outcome 1: Positive     │ Intervention outperforms placebo control as predicted.       │
│ Discovery (H1 Confirmed)│ Narrative: Demonstrates causal efficacy of mechanism.        │
├─────────────────────────┼──────────────────────────────────────────────────────────────┤
│ Outcome 2: Clean        │ Intervention and placebo produce statistically identical     │
│ Negative (H0 Confirmed) │ results, but positive control functions correctly.          │
│                         │ Narrative: Falsifies widespread assumption; proves that CoT  │
│                         │ is unfaithful post-hoc rationalization. Top-tier paper.      │
├─────────────────────────┼──────────────────────────────────────────────────────────────┤
│ Outcome 3: Emergent     │ Experiment reveals an unpredicted behavioral mode.           │
│ Phenomenon (Pivot)      │ Example: Discovery of spontaneous epistemic refusal and      │
│                         │ the "Neither" calculation in your Pilot 1.                   │
│                         │ Narrative: Expands problem ontology from binary arbitration  │
│                         │ to active epistemic triage. Highest scientific impact.       │
├─────────────────────────┼──────────────────────────────────────────────────────────────┤
│ Outcome 4: Muddled      │ High variance, broken parser, placebo produces conflicting   │
│ Mess (Fatal Confound)   │ results, baseline fails.                                     │
│                         │ Diagnosis: Flawed experimental design. Do not publish. Kill. │
└─────────────────────────┴──────────────────────────────────────────────────────────────┘
```

---

# SECTION 17: Freezing the Research Question

**`[L1 / L3]`** Research cannot proceed to production while the question is continuously shifting. You must formally execute a **Question Freeze**:

```markdown
# EXPERIMENT SPECIFICATION (LOCKED & FROZEN)
- Target Model: Qwen2.5-VL-3B-Instruct (FP16, PyTorch SDPA)
- Benchmark: vlm-modality-research/modality-conflict-arbitration-v2 (N = 1,619 pristine pairs)
- Factorial Protocol:
  * Arm 1: Direct Answering (Zero-Shot)
  * Arm 2: Length-Matched Neutral Placebo Prompt
  * Arm 3: Explicit Conflict Verbalization Prompt
- Primary Metric: \Delta_{arb} = P(\text{Visual Capture} \mid \text{Arm 2}) - P(\text{Visual Capture} \mid \text{Arm 3})
- Statistical Test: McNemar's paired within-item test (\alpha = 0.001) + Exact-Match Cross-Over
- Rule: Zero code modifications or prompt tweaks permitted during production execution.
```

---

# SECTION 18: End-to-End Thesis Execution Architecture

**`[L3]`** Structure your thesis repository with complete modular isolation. Never write sprawling 2,000-line scripts:

```
thesis-cross-modal/
├── configs/
│   └── experiment_spec_v3.json       # Immutable hyperparameters, prompt templates, seeds
├── data/
│   ├── download_census.py            # Turnkey download and verification script
│   └── raw/                          # Cached pristine conflict cohort (N = 1,619)
├── harness/
│   ├── model_loader.py               # Qwen2.5-VL-3B loader (FP16, SDPA, device mapping)
│   ├── prompt_generators.py          # Factorial arm prompt templates (Arm 1, Arm 2, Arm 3)
│   ├── response_parser.py            # Strict regex, number extractor, abstention classifier
│   └── production_runner.py          # Checkpoint loop with automated resume and JSONL logging
├── analysis/
│   ├── contingency_tables.py         # 3x3 behavioral transition matrices
│   ├── statistical_tests.py          # McNemar, Fisher exact, Cohen's h, Odds Ratio
│   └── cross_over_audit.py           # Exact-match arithmetic inversion calculator
├── figures/                          # Publication-ready PDF/SVG vector plots
└── reports/
    └── CANONICAL_THESIS_MASTER_REPORT.md # Definitive empirical record
```

---

# SECTION 19: From Thesis to Publishable Paper

**`[L1]`** A thesis is exhaustive, documenting every negative pilot, script iteration, and background literature review. A **publishable research paper is an arrow**:

```
                       THE PUBLISHABLE RESEARCH PAPER ARROW
                     
  [Introduction: 4 Paragraphs]
  • P1: The Core Tension (VLMs rely on visual tokens, yet default to text in math reasoning).
  • P2: The Unresolved Mystery (Prior work measured forced-choice capture; does verbalization steer or rationalize?).
  • P3: The Controlled Intervention (3-arm factorial protocol with length-matched placebos on N = 1,619 pairs).
  • P4: The Punchline (63.7 pp drop in visual capture, OR = 24.57, exact-match cross-over from 7.6x to 3.1x).
             │
             ▼
  [The Three Core Figures (The Entire Story in Pictures)]
  • Figure 1: The Causal Shift Bar Chart (Arm 2: 89.5% -> Arm 3: 25.8% Visual Capture).
  • Figure 2: The "Smoking Gun" Cross-Over (Image arithmetic collapses from 35.6% to 11.7%; text surges 4.7% to 35.8%).
  • Figure 3: Spontaneous Epistemic Abstention (Emergence of 13.65% refusal under conflicting evidence).
             │
             ▼
  [Defensive Related Work]
  Side-by-side contrast table against Which Source Wins?, CLASH, and Lanham et al.
             │
             ▼
  [Honest Limitations]
  Evaluated on 3B open-weight model; arithmetic domain; scaling transfer across 72B remains open.
```

---

# SECTION 20: The Realistic Research Timeline

**`[L3]`** A realistic, milestone-gated timeline for an undergraduate AI/ML thesis:

```
┌────────────────────────────────────────────────────────────────────────────────────────┐
│                              THE 16-WEEK THESIS TIMELINE                               │
├──────────────┬────────────────────────────────────────┬────────────────────────────────┤
│ Phase        │ Core Objective                         │ Exit Criteria / Milestone      │
├──────────────┼────────────────────────────────────────┼────────────────────────────────┤
│ Weeks 1–2    │ Field Map & Adversarial Red Team       │ 3 Anchor Papers Identified;    │
│              │ (Kill weak candidates early)           │ Closest-Work Matrix completed   │
├──────────────┼────────────────────────────────────────┼────────────────────────────────┤
│ Weeks 3–4    │ Feasibility Check & Diagnostic Pilots  │ Pilot 1 & 2 executed (N = 20); │
│              │ (Uncover confounds, parser failures)   │ Anomaly & abstention audit done│
├──────────────┼────────────────────────────────────────┼────────────────────────────────┤
│ Week 5       │ Protocol Refinement & QUESTION FREEZE  │ Experiment Specification signed│
│              │ (Lock prompts, placebos, regex parsers)│ off; Git commit tagged FROZEN  │
├──────────────┼────────────────────────────────────────┼────────────────────────────────┤
│ Weeks 6–8    │ Production Harness & Population Census │ Full population run complete;   │
│              │ (Execute N = 1,619 across all arms)    │ Checkpoint CSV/JSONL validated │
├──────────────┼────────────────────────────────────────┼────────────────────────────────┤
│ Weeks 9–10   │ Deterministic Statistical Analysis     │ McNemar p-values, odds ratios, │
│              │ & Mechanistic Cross-Over Audits        │ contingency tables generated   │
├──────────────┼────────────────────────────────────────┼────────────────────────────────┤
│ Weeks 11–13  │ Thesis Draft Writing                   │ Chapters 1–6 complete;         │
│              │ (Follow the Paper Arrow narrative)     │ Publication vector plots drawn │
├──────────────┼────────────────────────────────────────┼────────────────────────────────┤
│ Weeks 14–16  │ Defense Presentation & Conference Prep │ Slide deck audited; workshop   │
│              │ (Format for ACL/CVPR/EMNLP workshop)   │ or conference preprint uploaded│
└──────────────┴────────────────────────────────────────┴────────────────────────────────┘
```

---

# SECTION 21: Forensic Analysis of Your Historical Failure Modes

**`[L2]`** A rigorous post-mortem of your workspace reveals why topic discovery took five exhausting weeks:

### 1. The Collection Trap (Mistaking Cataloging for Progress)

Across August and September 2026, your workspace accumulated 87 research files and 11 handover reports. Downloading surveys, extracting comparison tables, and reading about continual learning, token pruning, medical imaging, and active agents felt intellectually productive. But collecting information about what *others* have done is cataloging, not research.

* **The Remedy:** Cap literature reading at **14 days maximum**. If a candidate does not produce a testable MDE by Day 14, kill it immediately.

### 2. Candidate Churn (Mixing Conceptual Levels)

In early reports, "Candidate 1" shifted from *Internal Uncertainty Probes* to *Reasoning Trace Degradation*. "Candidate 3" shifted from *Out-of-Frame Answerability* to *Bengali Cultural Steering*. Furthermore, fields, tasks, methods, and evaluation conditions were treated as interchangeable topics.

* **The Remedy:** Never label an idea "Candidate 1". Name it by its **Causal Contrast**:
  $$
  \text{Project} = [\text{Intervention}] \times [\text{Target Behavior}] \text{ on } [\text{Setting}]

  $$

### 3. The Illusion of Certainty from AI-Generated Extractions

LLM discovery assistants (Gemini, Perplexity, AlphaXiv) confidently generated claims of "novel, unstudied gaps," proposed unverified architectural hubs ("Layer 18 controls cultural steering," "Layer 22 is the binding hub"), and listed un-downloadable datasets (*WhatIfVis*).

* **The Remedy:** Maintain strict cognitive division of labor:

```
┌───────────────────────────────────────────────┬───────────────────────────────────────────────┐
│        DELEGATE AGGRESSIVELY TO AI            │        RESERVE STRICTLY FOR HUMAN JUDGMENT    │
├───────────────────────────────────────────────┼───────────────────────────────────────────────┤
│ • Generating boilerplate PyTorch harness code │ • Declaring whether a literature gap is REAL  │
│ • Writing complex regex parsers & JSON loggers│ • Deciding whether an idea is worth 3 months  │
│ • Brainstorming 30 keyword synonyms for search│ • Auditing anchor paper Limitation sections   │
│ • Formatting LaTeX tables & BibTeX entries    │ • Inspecting raw model output text in pilots  │
│ • Generating Matplotlib / Seaborn visualizers │ • Verifying that datasets actually download   │
│ • Drafting initial section summaries          │ • Checking whether controls isolate confounds │
│ • Identifying typos and grammatical flaws     │ • Signing off on the Experiment Specification │
└───────────────────────────────────────────────┴───────────────────────────────────────────────┘
```

---

# SECTION 22: The Reusable Research Workspace (Minimal Artifact Set)

**`[L3]`** Do not create dozens of scattered files. Maintain exactly **Seven Living Artifacts** in your research root:

```
research-workspace/
├── 1_Field_Map.md              # 4 quadrants: Bedrock, Frontier, Benchmarks, Open Tension
├── 2_Question_Ledger.md        # Candidates tracked: Alive, Killed, or Pivoted (with exact reasons)
├── 3_Evidence_Ledger.md        # Verified primary sources (arXiv ID, verified claim, concession)
├── 4_Experiment_Spec.md        # FROZEN design: Model, data, factorial arms, placebos, metrics
├── 5_Research_Log.md           # Chronological record of script runs, hardware stats, anomalies
├── 6_Results_Record.md         # Contingency tables, p-values, odds ratios, cross-over stats
└── 7_Paper_Story.md            # 1-page narrative arc, 3 core figures, paper outline
```

---

# SECTION 23: The Stop / Continue / Pivot / Kill Decision Engine

**`[L1]`** Research decisions must be dictated by objective evidence, not emotional attachment:

```
┌────────────────────────────────────────────────────────────────────────────────────────┐
│                              THE 6-STATE DECISION ENGINE                               │
├───────────┬───────────────────────────────────┬────────────────────────────────────────┤
│ Decision  │ Triggering Evidence               │ Concrete Action                        │
├───────────┼───────────────────────────────────┼────────────────────────────────────────┤
│ CONTINUE  │ Pilot on N = 20 produces signal   │ Scale immediately to production sample │
│           │ (\Delta > 15 pp) with zero bugs.  │ size (N >= 500 or full census).        │
├───────────┼───────────────────────────────────┼────────────────────────────────────────┤
│ NARROW    │ Proposal attempts to solve 4      │ Strip away peripheral tasks; retain    │
│           │ problems simultaneously.          │ strictly the single causal contrast.   │
├───────────┼───────────────────────────────────┼────────────────────────────────────────┤
│ PIVOT     │ Pilot uncovers an unpredicted     │ Reframe question around newly observed │
│           │ empirical anomaly (e.g. refusal). │ cognitive behavior.                    │
├───────────┼───────────────────────────────────┼────────────────────────────────────────┤
│ PILOT     │ Feasibility gates pass; closest   │ Build 200-line harness; run N = 20.    │
│           │ work matrix verified open.        │ Inspect raw text outputs.              │
├───────────┼───────────────────────────────────┼────────────────────────────────────────┤
│ FREEZE    │ Pilot eliminates confounds; regex │ Lock Experiment Specification. Stop    │
│           │ stabilized; placebos matched.     │ literature search; run production.     │
├───────────┼───────────────────────────────────┼────────────────────────────────────────┤
│ KILL      │ Competitor paper ran exact test;  │ Record autopsy in Question Ledger.     │
│           │ data un-downloadable; or placebo  │ Discard idea immediately.              │
│           │ reproduces treatment effect.      │                                        │
└───────────┴───────────────────────────────────┴────────────────────────────────────────┘
```

---

# SECTION 24: The One-Page Daily Research Playbook

*Keep this pinned beside your keyboard. Review it daily.*

### 🌅 Morning Calibration (5 Minutes)

1. **What is my phenomenon, in one sentence?** *(Observable input-output behavior).*
2. **What is the exact contrast I am testing today?** *(Condition A [Control] vs. Condition B [Treatment], differing in exactly one variable).*
3. **What is today's evidence target?** *(Not "read papers" or "work on code"; e.g., "Run 20 pilot items and inspect parse failures").*
4. **What is the simplest alternative explanation for what I hope to see?** *(And does my control eliminate it?).*

### ⚖️ The Daily Contrast Test

$$
\text{Treatment Output} - \text{Control Output} = \text{Causal Effect of the Single Manipulated Variable}

$$

If your treatment adds CoT reasoning *and* alters formatting *and* triples token length, you have three unmodeled confounds. Strip it down.

### 🚨 Daily Red Flags (Stop Immediately If:)

* ❌ Reading survey papers for $> 2$ consecutive hours without writing a testable hypothesis.
* ❌ Downloading $> 5$ papers into your reference manager in a single day.
* ❌ Tweaking prompts endlessly based on 2 cherry-picked examples.
* ❌ Spending 3 days building a complex "framework" before running a 50-line baseline.
* ❌ Believing an AI summary when it claims "this gap has never been studied."
* ❌ Looking only at aggregate accuracy numbers while ignoring raw model output text.

### 🌇 Evening Shutdown Audit (2 Minutes)

> **"Did today produce verifiable physical evidence (a working script, verified dataset, parsed pilot log, statistical table), or did it merely produce more reading notes?"**
> *If it produced only notes for three consecutive days, you are trapped in exploration. Tomorrow, you are forbidden from reading. You must run code.*

---

# SECTION 25: The 14-Day Sprint: "If I Start a New Research Area Tomorrow"

**`[L3]`** Follow this strict 14-day protocol when entering an unfamiliar AI/ML territory:

```
┌────────────────────────────────────────────────────────────────────────────────────────┐
│                          THE 14-DAY NEW RESEARCH SPRINT                                │
├──────────┬─────────────────────────────────────────────────────────────────────────────┤
│ Day 1    │ Landscape Sweep: Skim 2 top-venue papers (last 6 mos); extract 20 keywords. │
│ Day 2    │ Backward Citation Trace: Find the 3 canonical anchor papers they cite.     │
│ Day 3    │ Isolate Tension: Read Limitations of the 3 anchors; identify missing test.  │
│ Day 4    │ Closest-Work Attack: Search by intervention/measurement; build Matrix.      │
│ Day 5    │ Formulate Competing Hypotheses: Define H1 (mechanism) vs. H0 (confound).   │
│ Day 6    │ Feasibility Check: Run load_dataset(); test model FP16 inference on Colab.  │
│ Day 7    │ Design MDE: Define 3-arm factorial protocol (Direct, Placebo, Treatment).  │
│ Day 8    │ Red Team Attack: Apply 10-Question Gauntlet. Kill or pivot if confounded.   │
│ Day 9    │ Build Harness: Write 200-line Python runner with JSONL logging and regex.   │
│ Day 10   │ Execute Diagnostic Pilot: Run N = 20 items across all arms.                │
│ Day 11   │ Pilot Autopsy: Read all raw outputs; identify parse failures and refusals.  │
│ Day 12   │ Refine Controls: Equalize placebo token lengths; fix regex classifiers.     │
│ Day 13   │ FREEZE SPECIFICATION: Sign off Experiment_Spec.md; commit frozen code.     │
│ Day 14   │ Launch Production: Run census / multi-seed evaluation. Exploration closed.  │
└──────────┴─────────────────────────────────────────────────────────────────────────────┘
```

---

## Appendix: Verified Anchor-Paper Ledger (Canonical Cross-Modal Thesis)

**`[PRIMARY — Verified from Source Manuscripts]`**


| Paper ID | Authors, Venue & Year                                                                          | Verified Primary Claim from Source                                                                                                                  | Verified Experimental Setting                                                     | Crucial Concession in Source Manuscript                                                                                                                                                 |
| :--------- | :----------------------------------------------------------------------------------------------- | :---------------------------------------------------------------------------------------------------------------------------------------------------- | :---------------------------------------------------------------------------------- | :---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| **P1**   | *Which Source Wins? Task-Dependent Reliance in VLMs* (Aug 2026, arXiv:2608.17205)              | Multimodal models exhibit systematic modality preference when presented with conflicting text and image inputs under progressive degradation.       | Qwen2-VL-7B, LLaVA-v1.6 on synthetic & paired image-text reasoning tasks.         | **Section 6 Concession:** *"We evaluate models exclusively under direct zero-shot answering. We do not test whether models detect the contradiction, express uncertainty, or abstain."* |
| **P2**   | *CLASH: Multimodal Contradiction Benchmark* (Zhang et al., Nov 2025, arXiv:2511.19199)         | Evaluates whether VLMs can detect contradictory inputs and refuse to answer unanswerable multimodal queries.                                        | Frontier & open-source VLMs; contradiction detection evaluated as classification. | Frames contradiction detection purely as an abstention trigger, without measuring causal steering or problem arbitration.                                                               |
| **P3**   | *Measuring Faithfulness in Chain-of-Thought Reasoning* (Lanham et al., 2023, arXiv:2307.13702) | Tests CoT faithfulness in LLMs by perturbing or truncating reasoning traces; shows models often arrive at answers independently of reasoning steps. | Text-only LLMs (Claude-1, GPT-3.5, PaLM-2) on math, QA, and symbolic reasoning.   | Tested strictly in unimodal language models; does not explore cross-modal evidence arbitration.                                                                                         |
| **P4**   | *RH-Bench* (Liu et al., NeurIPS 2025, arXiv:2505.21523)                                        | Proves that extended reasoning traces degrade visual grounding, causing cross-modal forgetting in long-context VLMs.                                | Long-context multimodal LLMs; introduces standardized$RH\text{-}AUC$ metric.      | Focuses on trace degradation over time, leaving active conflict verbalization unexamined.                                                                                               |
| **P5**   | *Annotation Artifacts in Natural Language Inference Data* (Gururangan et al., NAACL 2018)      | Standard benchmark success can be achieved through superficial linguistic shortcuts in the hypothesis alone, bypassing the premise entirely.        | SNLI and MultiNLI benchmarks across multiple neural architectures.                | Exemplar study proving why single-modality baseline controls are mandatory in representation learning.                                                                                  |

---

### Master File Sync Notice

The definitive, exhaustive 32-section markdown manual (3,779 lines, fully annotated with KaTeX mathematics, forensic code snippets, and complete artifact schemas) is permanently mirrored and synchronized in your local research workspace at:
[`Research_Playbook/AI_ML_Research_Playbook.md`](file:///d:/Thesis/Important/Cross%20Modal/Research_Playbook/AI_ML_Research_Playbook.md).
