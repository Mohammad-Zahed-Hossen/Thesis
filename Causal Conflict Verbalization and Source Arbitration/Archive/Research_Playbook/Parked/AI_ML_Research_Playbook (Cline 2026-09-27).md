# AI/ML Research Playbook: From Research Discovery to Publishable Paper

> A working manual for turning a broad AI/ML interest into a defensible, experimentally answerable question — and then into a thesis and a paper. It is not a topic proposal, not a checklist, and not a writing guide.

**Prepared for:** Mohammad Zahed Hossen (final-year BSc CSE; local machine for editing/analysis, Google Colab Pro T4/V100 for compute; model scope ≤3B parameters)
**Date:** 24 September 2026

## Evidence labels used throughout

- **[L1] Established practice** — supported by established research practice and/or a primary source listed in Appendix A.
- **[L2] Workspace evidence** — reconstructed from the retained research corpus in this workspace. It describes what happened in this project; it is not a universal law.
- **[L3] Recommendation** — synthesis for your workflow, given your compute, time, and skill constraints.

## Table of contents

0. Scope and epistemic limits
1. Executive overview
2. How experienced researchers actually work
3. Why research is not linear
4. The researcher's mental model
5. Finding research territories
6. Finding phenomena and failures
7. Turning observations into research questions
8. Literature exploration strategy
9. How to search like a researcher
10. How to read and interrogate papers
11. Building a field map
12. Finding the closest existing work
13. Verifying whether a gap is real
14. Competing explanations and hypotheses
15. Adversarial idea testing
16. Fast idea-killing
17. Feasibility during discovery
18. Designing the minimum discriminating experiment
19. From research question to experimental system
20. Baselines, controls, metrics and evaluation
21. Pilot to main experiment
22. Handling unexpected and negative results
23. Iterating and changing the research question
24. Freezing the research question
25. End-to-end thesis execution
26. From thesis to paper
27. Research timeline
28. My personal failure modes and how to avoid them
29. Reusable research workspace
30. Stop / Continue / Pivot / Kill framework
31. One-page daily research playbook (including the discovery loop)
32. If I start a new research area tomorrow
- Appendix A: primary sources used
- Appendix B: reconstructed case-study chronology from this workspace
- Appendix C: printable cards

## 0. Scope and epistemic limits

I studied the retained workspace: the context and handover documents, the rejected/parked-field report, the VLM and Bengali-VLM exploration folders, the multimodal-agent and medical-imaging audits, four canonical proposals, the adversarial audits, the locked specification, the pilot code, the raw result files (JSON/CSV), the statistical suite, and the analysis reports. **[L2]**

Three limits follow directly from that evidence base:

1. **No Git history.** The repository was never committed, so chronology is reconstructed from content, cross-references, filenames, and experiment provenance — not from authorship timestamps.
2. **Retrospective documents are claims, not confirmation.** Several "canonical," "final," and "100% complete" reports restate earlier conclusions. A conclusion repeated in five documents is still one conclusion. This manual treats repetition as a process signal, not as replication.
3. **The conversation history is incomplete.** Where this playbook describes what you did in earlier sessions, it is an inference from surviving artifacts. Those inferences are marked **[L2]**, and I do not claim access to exchanges I cannot see.

One citation that appears in the workspace (`arXiv:2608.17205`, *"Which Source Wins?"*) could not be verified from a primary source when I checked it. Treat it as **[Unknown]** until you open the paper yourself. That is not a project failure; it is exactly the check this playbook formalizes in §12 and §13.

---

## 1. Executive overview

A strong researcher is not primarily someone who has read the most papers. They are someone who can:

- notice when a phenomenon is real versus a measurement artifact;
- hold two explanations at once and design the observation that separates them;
- estimate whether a question is answerable *before* spending months on it; and
- change the question when the evidence demands it.

The process is a loop, not a pipeline:

```text
research area
   ↓
concrete observation or failure
   ↕                      literature map
   ↕                      claims and mechanisms
   ↕                      competing explanations
   ↕                      closest existing experiments
   ↕                      a candidate question
   ↕                      feasibility, data, baselines
   ↓
minimum discriminating experiment
   ↓
evidence (including surprises)
   ↺  narrow / broaden / add control / change metric / pivot / kill
```

Only when the loop stops producing new information does it become a project:

```text
frozen question
 → hypotheses with opposite predictions
 → variables, controls, dataset, baselines, metrics
 → pilot
 → main experiment
 → ablations and robustness
 → analysis
 → interpretation
 → contribution
 → thesis → paper
```

**Central operating rule [L3]:** instead of asking "what is novel?", ask "what observation would change what we believe, and what is the smallest honest experiment that could produce it?"

Five questions to keep visible (printable form in Appendix C):

1. What exactly did I observe, and could my measurement have produced it?
2. What mechanism do the closest papers claim?
3. What alternative explanation would produce the same observation?
4. What result would separate the alternatives?
5. What would we know afterwards that we do not know now?

If question 4 cannot be answered in one sentence, you do not yet have a research question. You have a research area. **[L3]**

---

## 2. How experienced researchers actually work

### 2.1 The unit of work is a decision, not a paper read

Experienced researchers rarely work by "reading the literature until an idea appears." They work in short cycles whose output is a **decision**: continue, narrow, pivot, pilot, or kill. A day of work that ends with "I now know that two of my three explanations are indistinguishable with the data I have" is a successful day. **[L3]**

A realistic senior-style week looks like this:

| Day | Activity | Output |
|---|---|---|
| 1 | Orient: find the 5–10 papers that define the area, skim only | A one-page map, not notes |
| 2 | Trace the strongest claim to its evidence and its controls | A list of assumptions and missing controls |
| 3 | Attack: search for the closest existing experiment and for contradicting results | A closest-work table and one candidate question |
| 4 | Scope the minimum experiment; check data/model/logistics reality | A one-page experiment sketch, or a kill |
| 5 | Run or simulate a 10–30 item pilot | Evidence that either strengthens or destroys the candidate |

This cadence is not a rule; it is an illustration of the ratio that matters: **searching is always in service of a decision.** **[L1, L3]**

### 2.2 They think in predictions, not topics

Weak: "This thesis will study reasoning in multimodal models."

Stronger: "If explicit conflict verbalization changes which source a model's reasoning is about, then a length-matched neutral deliberation prompt — same instruction, same output budget, no conflict language — should reproduce the same shift. If both prompts shift behavior identically, the phenomenon is deliberation or length, not conflict verbalization."

The strong version contains, in one sentence:

- the manipulation (conflict language present/absent);
- the matched control (neutral deliberation at equal length);
- the measurement (which source the reasoning follows);
- and the failure interpretation (identical shift ⇒ the construct of interest is not isolated).

You performed a version of this reasoning in the pre-freeze pilot when you discovered that the neutral placebo averaged 61.2 tokens while the direct arm averaged 3.4, and concluded that the control was not actually matched. **[L2]** That is senior behavior: the control was inspected as an object of study, not trusted by its name.

### 2.3 They keep three ledgers

- **Claim ledger:** what is known, what is asserted, what is measured, and what is merely inferred — kept separate.
- **Decision ledger:** the exact evidence that would make you continue, narrow, pivot, pilot, freeze, or kill.
- **Evidence ledger:** the specific table, figure, script, seed, or primary source behind every important belief.

The workspace demonstrates why. In the cross-modal project, the archived reports repeatedly described "visual capture" and "causal arbitration." But the primary table shows the *direct* baseline follows the **text** problem 85.5% of the time and the image problem only 13.8%, while the *neutral placebo* prompt inverts this to 89.5% image. **[L2]** Two claims therefore need to be separated:

1. There is an extremely large effect of prompt framing on which problem the model engages. (Strongly supported by the recorded data.)
2. There is an entrenched *visual* modality preference in the model. (Not supported by the direct baseline in that run; it is suggested only under a specific neutral-descriptive prompt.)

A claim ledger catches that conflated pair in minutes.

### 2.4 What "senior" actually means operationally

Seniority, for these purposes, is the ability to:

- notice a hidden assumption quickly (e.g., "the model *selects* an answer" when it may *compute* one);
- choose the experiment with the highest information per unit of effort;
- distinguish claim, mechanism, and measurement;
- discard sunk cost without drama;
- write a complicated or negative result accurately; and
- stop reading when reading no longer changes the next decision.

### 2.5 They treat "interesting" as a testable claim

"Interesting" is not a property of a topic. It is a relation between a result and a prior belief. A result is interesting when it is:

- **surprising relative to a stated prediction** (not just surprising to you);
- **robust across plausible controls**; and
- **consequential** — it changes what someone would build, evaluate, or claim.

This is the practical content of [L1] falsifiability: state the prediction first, then let the data be surprising.

---

## 3. Why research is not linear

### 3.1 The false model

```text
choose field → search papers → find gap → formulate question
→ find dataset → build model → run experiment → write
```

### 3.2 The real loop

Any stage can send you backward:

```text
notice something
→ ask whether it is real
→ search for prior explanations
→ discover a competing explanation
→ inspect the measurement
→ discover the question is too broad
→ narrow the claim
→ run a pilot
→ discover the outcome does not measure the construct
→ repair the measure, narrow again, or abandon the branch
→ freeze a smaller question
```

### 3.3 Backtrack triggers — when going backward is correct

| Trigger | What it means | Local instance |
|---|---|---|
| Outcome does not measure the construct | The metric answers a different question | The diagnostic pilot showed 85% of direct-arm outputs matched *neither* precomputed answer, because the model **computed** a new answer instead of **selecting** one **[L2]** |
| Control is not matched | Arms differ in more than the intended variable | Neutral placebo averaged 61.2 tokens vs 3.4 for the direct arm **[L2]** |
| Baseline is a prompt artifact | Effect exists under one framing only | Direct baseline follows the **text** problem 85.5% of the time; the neutral placebo flips this to **89.5% image** **[L2]** |
| Closest work already answers it | The gap was terminology, not knowledge | Novelty repeatedly judged by phrase-variant searching rather than experiment comparison **[L2]** |
| Effect vanishes under controls | A nuisance variable drove it | Token truncation (15/90) invalidated exact-match accuracy for an entire run **[L2]** |
| Labels cannot support the reading | Benchmark tests a neighboring task | Detection/abstention benchmark used as if it measured arbitration **[L2]** |
| Result is trivially predictable | No belief would change | "Bigger model scores higher." |
| Only a p-value exists | No interpretable effect | Significant test on a metric that is not the construct. |

**Rule [L3]:** backtracking is not wasted time if it changes *what you measure*. It is wasted time if it only changes *how you write about the same measurement*.

### 3.4 Two kinds of stability

- **Conceptual stability** — the question names a construct the experiment can distinguish.
- **Operational stability** — implementation, metric, controls, seeds, and data quality are reliable enough to interpret.

You may freeze the concept before every engineering detail is final. You must not run the main experiment before the outcome is demonstrably able to measure that concept. **[L3]**

### 3.5 The price of pretending linearity

Research is written linearly; it is not performed linearly. Two costs appear in this workspace **[L2]**:

1. **Proposal-first commitment.** Long canonical specifications were produced before the measurement question was settled. When the pilot showed the metric was wrong, those documents already framed the question around the wrong measure — which raises the psychological cost of revising it.
2. **Freeze-by-repetition.** Declaring a phase "100% complete" in several documents does not create evidence. A freeze is credible only when the conditions in §24 hold.

### 3.6 The loop exit condition

Leave the discovery loop when **a new search or a new pilot no longer changes your next action**. Not when you feel certain — feelings do not converge — but when marginal information for the current decision is zero.

---

## 4. The researcher's mental model

### 4.1 All claims are conditional

Store every claim as:

> Under conditions **X**, intervention **Y** changed measure **Z** by **A** on population **D** under analysis **P**.

Then ask what would change the conclusion: a different population, seed, control, natural versus synthetic input, stronger or weaker model, corrected metric, or simpler baseline. Locating the boundary of a claim *is* the contribution. **[L1/L3]**

### 4.2 Three levels of explanation — never mix them silently

| Level | Question | VLM example | Supports |
|---|---|---|---|
| Descriptive | What happened? | "An intervention prompt reduced image-following from 89.5% to 25.8% of items." | Existence of a behavioral difference |
| Comparative | Under what conditions does it differ? | "The shift is absent with a neutral prompt matched in length." | Attribution to the manipulated variable |
| Mechanistic | Why? | "Attention to image tokens decreases as chains lengthen." | A hypothesis needing independent evidence |

A prompt-level intervention can establish a comparative result. It does not by itself establish a mechanistic one. Papers that blur these levels are the easiest place to find legitimate questions — and the easiest place to accidentally overclaim yourself. **[L3]**

### 4.3 The discrimination principle

An experiment exists to make explanations disagree. Before coding, write:

```text
If explanation A is true → we observe X
If explanation B is true → we observe Y
If X ≈ Y → this experiment cannot discriminate (redesign)
```

If X and Y can be the same number, do not run it. **[L3]**

### 4.4 The assumption audit

List what your claim needs, and mark each assumption tested / untested / untestable here:

1. The dataset conflict is genuine and correctly labeled.
2. The model can perceive the relevant image content at the chosen resolution.
3. Prompt arms differ only in the intended variable (length, format, position).
4. The output classifier measures what its name says.
5. Truncation did not remove the behavior of interest.
6. The sample is large and independent enough for the statistical test used.
7. The benchmark task matches the construct (choice vs detection vs computation).
8. A trivial baseline cannot reproduce the effect.

Every untested assumption is a reviewer's first question. Test the three cheapest **before** the main run. **[L1/L3]**

### 4.5 Name the boundary in one sentence

> This study asks whether **X** under **conditions** relative to **control**, using **measure**. It does not claim **Y** across other models, modalities, languages, or real-world settings.

### 4.6 Write down what would change your mind

Before collecting data, write two or three sentences: *"I will consider the conflict-specificity hypothesis weakened if …"* — for example: *"…if a length-matched neutral deliberation arm produces a visual-following rate within a small margin of the conflict arm on the same items."* This is lightweight pre-registration. It costs ten minutes and prevents post-hoc storytelling. **[L1: reproducibility and pre-registration practice; L3: workflow form]**

---

## 5. Finding research territories

### 5.1 Area versus territory

- **Area:** a community and its literature — *Vision-Language Models*.
- **Territory:** a family of phenomena plus the data, metrics, and models used to study it — *cross-modal evidence conflict and source arbitration under controlled intervention*.

You cannot execute a thesis on an area. You can execute one on a territory. **[L3]**

### 5.2 Five signals of a workable territory

1. **Phenomenon-rich, mechanism-poor.** Many papers document the behavior; few explain it.
2. **Measurement-poor.** Metrics are proxies for the construct people name.
3. **Compute-tractable.** Answerable with public ≤3B checkpoints and one 16 GB GPU by inference alone.
4. **Data-inspectable.** You can open the dataset, read items, and verify labels yourself.
5. **Negative-result valuable.** A null result constrains theory rather than merely failing to help.

Disqualifying signals for your situation: training from scratch, private clinical data, distributed simulation, months of annotation. **[L2/L3]**

### 5.3 Territory scoring grid

Score 1–5, weight, sum. Weights reflect *your* constraints, not universal truth.

| Criterion | Weight | 1 (bad) | 5 (good) |
|---|---|---|---|
| Phenomenon visibility | 2 | Vague, contested | Reproducible in a day |
| Measurement tractability | 3 | Needs large-scale human labeling | Deterministic parsing |
| Compute fit | 3 | >16 GB or training | Inference-only, ≤3B |
| Data access and quality | 2 | Private, unlabeled | Public, verifiable |
| Closest-work density | 1 | Saturated | Adjacent but unoccupied |
| Negative-result value | 2 | Teaches nothing | Constrains theory |
| Terminology stability | 1 | Incompatible names | Shared vocabulary |

**Calibration [L3]:** density has deliberately low weight. The enemy is not many papers; it is an *occupied experiment*. Judge §12, not keyword frequency.

### 5.4 Three territory archetypes with concrete instances

1. **Behavioral phenomenon with an unverified mechanism.** Longer multimodal reasoning chains correlate with increased hallucination and reduced visual focus; the authors report attention analysis supporting the link ([RH-AUC / RH-Bench, arXiv:2505.21523](https://arxiv.org/abs/2505.21523)). Legitimate follow-ups: does it hold under matched compute, with perturbed-but-legible images, or with length added without reasoning?
2. **Claim whose measurement is the phenomenon.** Apparent "emergent abilities" appear or vanish depending on whether the metric is discontinuous or continuous ([arXiv:2304.15004](https://arxiv.org/abs/2304.15004)). Legitimate follow-up: run the same metric-sensitivity audit on a newer claimed discontinuity in your field.
3. **Benchmark measuring a neighboring task.** A benchmark formulated as contradiction *detection*/abstention ([CLASH, arXiv:2511.19199](https://arxiv.org/abs/2511.19199)) used to support *reliance* or *arbitration* claims. Legitimate follow-up: build the missing measure and test whether detection and arbitration dissociate.

### 5.5 Rejecting a territory without guilt

Reject a territory not because it is uninteresting but because your constraints make it untestable in the window, or because the closest experiment already answers your question. Record one line in the Question Ledger. Two lines of "why parked" beat an entire report **[L3]**.

### 5.6 What your own history shows **[L2]**

The territories that survived into serious consideration were **inference-only**, **benchmark-anchored**, and **measurable by deterministic parsing**. The parked fields (medical imaging plus federated learning; cultural/Bangla VLM repair; multimodal agents) each required an asset you lacked: clinical data with domain labels, annotation-heavy cultural evaluation, or multi-step tool/robotics environments.

Two conclusions:

- **The parked fields were not stupid choices.** They were rejected late, after large amounts of document production — because feasibility was applied at the *end* of exploration instead of *during* it.
- **The productive move was structural, not inspirational.** The direction that survived asked what a controlled intervention does, not what system should be improved.

**[L3] Rule:** explore at most **two** territories concurrently; time-box each to two weeks. If no candidate question with available data and a deterministic measure appears, park it in writing and stop reading about it.

---

## 6. Finding phenomena and failures

A phenomenon is a repeatable, describable behavior or outcome — not a topic, a method, or an opinion about a paper.

| Source of a question | How to recognize it | Cheapest check | Question it yields |
|---|---|---|---|
| Unexplained empirical phenomenon | Reported, unexplained | One ablation table | What causes this? |
| Surprising failure | Fails where it "should" succeed | Run 10 hand-picked items | When does it fail? |
| Contradiction between papers | Opposite directions reported | Compare dataset, prompt, metric | What differs between setups? |
| Obvious-but-untested alternative | Reviewers say "couldn't it be…?" | Design the matched control | Does it survive the alternative? |
| Limitation in an influential paper | Stated in §Limitations | Read that paragraph | Does the claim hold outside it? |
| Missing control | Intervention has no placebo | List nuisance variables | Is the cause the intended variable? |
| Boundary condition | Works in one setting only | Change one factor | Where exactly does it break? |
| Measurement problem | Metric proxies the construct | Re-read its definition | Does the metric measure the claim? |
| Benchmark weakness | Templated, leaky, or adjacent task | Read 20 items | What is actually measured? |
| Replication divergence | Your rerun disagrees | Compare published config | Is the effect setup-dependent? |
| Toy-only method | No realistic evaluation | Add realistic perturbation | Does it survive realism? |
| Unclear mechanism | Behavior real, cause unknown | Ask what distinguishes causes | Which mechanism explains it? |
| Untested assumption | Universally assumed | Pick cheapest test | Does it hold? |
| Engineering bottleneck | A fix changes results oddly | Ablate the fix | Is the result an artifact? |

Three of these are the highest-yield sources for a short thesis.

### 6.1 Missing or mismatched control

**Recognition.** Read the intervention and ask "compared to what?" If the answer is "not doing it," the comparison is confounded with length, format, token budget, instruction burden, and layout.

**Cheapest check.** Count tokens per arm on 20 items. If arms differ by more than roughly 20%, the control is unmatched — unless you can argue the difference is irrelevant, in which case it is also irrelevant to the effect you claim.

**Failure mode to avoid.** A control matched in tokens but not in *content*, *difficulty*, or *instruction type*, or matched on average while diverging per item. Prefer per-item matching. **[L3]**

### 6.2 A metric that is a proxy

**Recognition.** Ask of any metric: what construct is named, what does it operationally count, and can the first be true while the second misleads?

**Cheapest check.** Manually inspect 20 outputs beside the metric value. Disagreements reveal the gap immediately.

**Worked instance [L2].** In your pre-freeze pilot, "which source the model followed" was measured by exact match to one of two precomputed answers. Inspecting 20 items showed the model was **solving** problems rather than **selecting** answers; 85% of direct-arm outputs matched neither answer. The remedy — classify *which problem the reasoning engages with* from entity evidence, and add abstention as an explicit outcome — is the general pattern: **classify the behavior, not the answer key** **[L2/L3]**.

**What it yields.** A measurement-validity contribution: "the common metric conflates X and Y; we propose and validate a measure that separates them." For an undergraduate thesis this is often more defensible than a new method.

### 6.3 Contradiction between papers, or between a paper and your rerun

**Recognition.** Opposite directions for the same effect, or a rerun that disagrees.

**Cheapest check.** Build one column per difference: model revision, prompt template, decoding parameters, token budget, preprocessing resolution, split, metric definition, seeds. One difference usually explains the discrepancy.

**What it yields.** A boundary condition ("holds only up to resolution R") or a correction ("the gain disappears under matched decoding").

### 6.4 Low-yield sources (use with care)

These can produce well-written theses with little scientific content. Do not build on them unless they expose a real measurement or causal question **[L3]**:

- "Apply method M to dataset D" — a substitution, not a question.
- "Improve accuracy of X" — an objective, not a phenomenon.
- "Build a system that…" — engineering, unless the system exists to answer a question.
- "No paper uses my exact phrase" — almost always a terminology gap.
- "Combine two papers' methods" — a recipe, not a result, unless the combination is theoretically forced.

---

## 7. Turning observations into research questions

### 7.1 The ladder, with definitions that do work

```text
Research area → Research territory → Phenomenon → Observation
→ Existing claim → Alternative explanation → Gap → Research question
→ Hypothesis → Experiment → Contribution
```

| Rung | Definition | Practical note |
|---|---|---|
| Area | Community and its literature | Not executable |
| Territory | Family of phenomena + data/metrics | Executable unit |
| Phenomenon | Repeatable behavior or outcome | Describable without your method |
| Observation | A specific, dated, quantified instance | Say where and how much |
| Existing claim | What prior work says explains it | Attribute precisely |
| Alternative explanation | Another cause producing the same observation | At least one must be non-trivial |
| Gap | A missing **experiment**, not a missing sentence | The decisive distinction |
| Research question | Answer differs under competing explanations | Must name the comparison |
| Hypothesis | Directional prediction with a failure condition | State H₁ and H₀ |
| Experiment | Smallest procedure separating the hypotheses | Controls + metric included |
| Contribution | What a reader knows afterwards | Written last, honestly |

### 7.2 Phenomenon ≠ question ≠ gap

**Phenomenon:** "When visual and textual premises conflict, the model's reasoning commits to one source." (Descriptive, no comparison required.)

**Question:** "Does requiring explicit conflict verbalization change which source the reasoning engages, relative to a neutral prompt matched in length?" (Names conditions and a comparison.)

**Gap (correctly stated):** "No recorded experiment compares conflict verbalization against a length-matched neutral deliberation on the same items with the same output budget." (States a missing experiment.)

**Gap (incorrectly stated):** "No paper uses the term 'conflict verbalization'." (States a missing string.)

**Hypothesis:** H₁ — the shift is specific to conflict semantics, so a length-matched neutral prompt will not reproduce it. H₀ — a neutral prompt of equal length produces an equal shift, meaning deliberation/length explains the effect.

**Experiment:** four arms on identical items with per-arm token budgets fixed in advance, plus classification of the problem the reasoning engages and abstention as an explicit outcome.

**Contribution:** evidence about whether explicit explanation steers behavior or rationalizes it — and a validated measure of *engaged problem* rather than *matched answer*.

### 7.3 The four tests every candidate question must pass

**Test 1 — Discrimination.** Does the question predict different observable outcomes under competing explanations? If yes, name both outcomes in writing.

**Test 2 — Measurement.** Is there a deterministic, inspectable procedure that produces the observation? If the answer is "an LLM judge will tell us," either calibrate the judge against human labels on a sample or find a parseable proxy. **[L1: evaluation and reproducibility practice; L3: your stated preference for deterministic parsing.]**

**Test 3 — Scope.** Can you state population, conditions, and control in one sentence? "How do VLMs use multimodal evidence?" fails; "does X change Y relative to Z, on benchmark B with model M?" passes.

**Test 4 — Value.** If the answer is "no effect," does the field learn something? If not, either strengthen the theory it constrains or change the question.

### 7.4 Three anti-patterns at this stage **[L3]**

1. **Method-first questions.** "Can we improve X using Y?" Start from the behavior, then ask whether Y discriminates explanations.
2. **Scope inflation.** Adding modalities, languages, and tasks to look impressive makes the experiment uninterpretable and unfinishable.
3. **Question/questionnaire confusion.** A *question* has an answer discoverable by measurement. A *research programme* ("How does grounding work?") does not. You want a question that a single experiment can move decisively.

### 7.5 Worked ladder A — the question your project actually froze **[L2]**

| Rung | Content |
|---|---|
| Area | Vision-Language Models |
| Territory | Cross-modal evidence conflict and source arbitration |
| Phenomenon | Under conflicting premises, the model commits to one source |
| Observation | With a neutral descriptive prompt, reasoning follows the *image* problem on 89.5% (1,449/1,619) of items; with conflict verbalization, 25.8% (417/1,619) |
| Existing claim | Modality dominance influenced by legibility (as summarized in the workspace) |
| Alternatives | (i) conflict semantics; (ii) extra computation/length; (iii) prompt framing alone; (iv) instruction-following burden; (v) benchmark arithmetic structure |
| Gap | No recorded comparison of conflict verbalization against a length-matched neutral deliberation on the same items |
| Question | Under length-matched controls, does verbalizing the conflict change which problem the reasoning engages? |
| Hypotheses | H₁ shift is specific to conflict semantics; H₀ neutral equal-length prompt produces an equal shift |
| Experiment | Identical items, fixed per-arm budgets, placebo + prefill probe arms, engaged-problem classification, abstention as outcome |
| Contribution | Causal evidence about steering versus rationalization, plus a validated measure |

**Note on the observation row.** The 89.5% figure is a *placebo-arm* result. The direct baseline in the same run follows the **text** problem 85.5% of the time. So the honest phenomenon is *prompt-framing sensitivity plus arm-dependent source preference*, not simply "the model prefers images." This distinction is exactly what a claim ledger exists to catch, and it changes what your thesis can assert. **[L2]**

### 7.6 Worked ladder B — a branch the pilot opened and you did not pursue

| Rung | Content |
|---|---|
| Observation | Under conflict verbalization, abstention is 13.7% (221/1,619) versus 0.2% in the neutral arm and 0.0% in the direct arm |
| Alternatives | (i) genuine conflict-aware abstention; (ii) instruction-induced verbosity; (iii) degenerate refusal templates; (iv) arithmetic difficulty |
| Question | Is abstention induced by conflict awareness or by instruction format? |
| Discriminating experiment | Add a neutral arm that also invites uncertainty reporting without conflict language; compare abstention rates and inspect refusal text |
| Why it matters | Separates *detection* from *arbitration*, precisely the dissociation left open by detection-only formulations such as CLASH ([arXiv:2511.19199](https://arxiv.org/abs/2511.19199)) |

Writing Ladder B down instead of silently merging it into Ladder A is the discipline this playbook asks for. It also gives you an honest "future work" section that is grounded in your own data rather than invented. **[L3]**

### 7.7 The terminology trap

The most common false gap is a vocabulary gap. You think:

> "Nobody has studied whether explicit conflict verbalization causally steers arbitration."

What you must actually test is:

> "Has anyone compared an explicit conflict explanation against a length-matched neutral deliberation control on the same items, and measured which source the reasoning engages?"

The first is about words. The second is about experiments. Different groups call the same manipulation "faithfulness testing," "self-explanation," "rationale generation," "verbalized reasoning," "contrastive explanation," or "conflict detection." Your novelty search must be **phenomenon-first and design-first**, not phrase-first (§9 and §12). **[L1/L3]**

Two concrete reminders from verified sources:

- CoT unfaithfulness was demonstrated with biasing features on text tasks and no matched multimodal conflict control ([arXiv:2305.04388](https://arxiv.org/abs/2305.04388)). That leaves a **transfer-and-control** question open, not a vocabulary question.
- Cross-modal contradiction benchmarks evaluate *detection*, with downstream effects on conflict recognition; they do not establish which source a model's reasoning engages under a matched neutral prompt ([arXiv:2511.19199](https://arxiv.org/abs/2511.19199)).

Neither statement shows your project is novel. Both show how to phrase the check as a design comparison rather than a phrase search. **[L3]**

---

## 8. Literature exploration strategy

### 8.1 Reading is a resource allocation problem

You have a fixed budget of attention. Allocate it by *decision value*, not by paper importance as judged by others. **[L3]**

A practical allocation for a new territory:

| Portion of reading time | Purpose | Depth |
|---|---|---|
| 25% | Orientation: what is this field arguing about? | Abstract + intro + figures |
| 25% | The 3–5 papers that define the phenomenon | Full read of method, results, limitations |
| 20% | Closest-work search (§12) | Method and experiment sections only |
| 15% | Alternative explanations and confound literature | Targeted sections |
| 10% | Benchmark/dataset documentation and code | Data cards, README, item inspection |
| 5% | Frontiers: newest 3–6 months | Abstracts only, until one matters |

### 8.2 When to start reading deeply

Read deeply (full method, results, appendices) only when a paper satisfies at least one of:

- it defines the phenomenon you are studying;
- it contains the experiment closest to yours;
- it supplies your dataset, metric, or method;
- it proposes a mechanism that competes with your explanation;
- it is the *strongest possible objection* to your idea.

Everything else gets a five-minute pass. **[L3]**

### 8.3 When to stop reading — saturation criteria

Stop expanding the literature when all of the following are true:

1. **Coverage:** the last five papers you found introduced no new *experiment design*, no new *alternative explanation*, and no new *metric*.
2. **Closest work:** you can name the closest existing experiment and explain, in two sentences, why yours differs in design rather than vocabulary.
3. **Vocabulary:** you know the 3–5 terms different communities use for your phenomenon.
4. **Boundary:** you can state what the field already knows and what remains unknown without hedging.
5. **Marginal decision value:** further reading no longer changes your experiment plan.

If criteria 1–4 hold but your *design* is still unclear, the blocker is design, not literature. Go to §18, not to the search bar. **[L3]**

### 8.4 Breadth-first, then depth-first — and never the reverse

**Breadth-first (days 1–3).** Find the defining papers and the vocabulary. Read abstracts, intros, and figures. Build the field map (§11). Do not take notes on details you cannot yet use.

**Depth-first (days 4–10).** Choose the 4–8 papers that matter and interrogate them (§10). Extract: their claim, their data, their control, their metric, their limitation, and the exact experiment they did *not* run.

**Why order matters [L2].** In your workspace, several folders contain long, detailed audits produced early, and later folds re-audit the same space with clearer questions. Depth-first reading before the phenomenon was sharp produced detail that could not be used, then had to be re-derived.

### 8.5 Managing the reading queue

Keep one file with three lists only **[L3]**:

```text
TO-READ        (max 10 entries; each with the decision it informs)
READ-RELEVANT  (each with: claim / evidence / control / metric / limitation / what they did not test)
IRRELEVANT     (one line why; never revisit)
```

If the TO-READ list exceeds ten items, stop collecting and start deciding. An unbounded queue is a symptom of avoiding the decision, not of thoroughness.

### 8.6 Search engines, catalogs, and where AI fits

- **Use** arXiv (full text + version history), the venue's official proceedings, Semantic Scholar/Google Scholar for citation chains, and dataset/model cards on Hugging Face for provenance and known limitations.
- **Use citation chains deliberately:** backward (what does this paper build on?) and forward (who challenged or extended it?). Forward citations are where refutations live. **[L1]**
- **AI assistants** are excellent at: summarizing a paper you already have, generating search-term variants, translating between community vocabularies, and listing candidate confounds. They are unreliable at: asserting that a gap exists, judging novelty, and reporting what a paper's experiment actually did when you have not checked it. (§28 covers this in depth.)

### 8.7 A stopping story from your own project **[L2]**

The workspace contains many large synthesis documents and multiple "canonical" restatements. Their volume reflects genuine effort, but the *decision-relevant* content stops growing well before the documents stop being written. The useful pivot happened when the work shifted from producing audits to running a 20-item pilot that falsified a metric. Total new knowledge per hour of effort rose sharply at that moment.

**Rule [L3]:** if two consecutive reading sessions produce no change in your experiment sketch, the reading phase is over for now.

---

## 9. How to search like a researcher

### 9.1 Search is a sequence of questions, not one query

Suppose you notice:

> "A multimodal model appears to lose image-grounded content as its reasoning chain gets longer."

Below is the actual search sequence a researcher runs, in order, with the decision each search informs.

| # | Search intent | Example query strings | Decision it informs |
|---|---|---|---|
| 1 | Phenomenon | `"long reasoning" multimodal hallucination`, `reasoning length visual grounding degradation`, `longer chains less visual` | Does the phenomenon exist in the literature at all? |
| 2 | Explanation | append `mechanism`, `attention analysis`, `why`, plus the paper's §Discussion | What cause do authors propose? |
| 3 | Alternative explanation | `modality prior`, `language prior`, `distribution shift`, `prompt length`, `decoding` | What else could produce it? |
| 4 | Confound | `test-time compute control`, `matched compute`, `token budget`, `length-matched` | Has anyone ruled out the boring cause? |
| 5 | Replication / challenge | forward citations of the phenomenon paper; `fails to replicate`, `does not hold`, `reassessment`, `critique` | Has anyone challenged or reinterpreted it? |
| 6 | Boundary condition | `resolution`, `image degradation`, `task type`, `model scale`, `out-of-domain` | Where does the effect stop? |
| 7 | Intervention | `intervention`, `causal`, `prefill`, `activation patching`, `ablation of reasoning` | What manipulations already exist? |
| 8 | Benchmark | `benchmark`, `diagnostic`, `evaluation suite`, plus the metric name | Is there a standard measure, and what does it actually score? |
| 9 | Dataset | `dataset`, `corpus`, plus Hugging Face dataset search | Is there reusable data with known provenance? |
| 10 | Recent work | arXiv listings for the last 3–6 months; author pages; venue accepted-paper lists | Is the space moving under me right now? |

Searches 1–2 tell you what the field believes. Searches 3–5 tell you what the field has *not* ruled out. Searches 6–7 tell you what is testable. Searches 8–9 tell you what is feasible. Search 10 tells you whether to hurry. **[L3]**

### 9.2 Search by design, not by topic wording

Keyword search fails precisely where novelty matters, because your idea's *design* may exist under different words. Search on each design dimension separately **[L2/L3]**:

| Dimension | What to search | Why |
|---|---|---|
| Phenomenon | Behavior descriptions and their synonyms | Finds the field's own name for it |
| Intervention | The manipulation type (prompting, prefill, activation, perturbation) | Finds the closest *causal* design |
| Measurement | The metric or construct (faithfulness, reliance, arbitration, abstention) | Finds the closest *analysis* |
| Dataset | Benchmark or corpus name, plus derivative works | Finds papers using identical items |
| Model | Model family name, e.g. a specific VLM generation | Finds replication and model-specific studies |
| Protocol | "length-matched", "placebo", "control condition", "same items" | Finds the closest *control design* |
| Evaluation | Annotation scheme, inter-annotator agreement, judge calibration | Finds measurement-validity work |

**Worked example.** Searching "conflict verbalization" may return little. Searching the *design* — "matched neutral control + source-attribution + multimodal contradiction" — returns faithfulness studies, explanation-evaluation work, and benchmark papers. One of those may already contain your experiment. **[L3]**

### 9.3 Techniques that find what keyword search misses

1. **Backward citation chain** from the phenomenon paper: which earlier result is being relied upon? Check whether that result was ever controlled. **[L1]**
2. **Forward citation chain:** who cited it, and did they disagree? Use "cited by" on Semantic Scholar/Google Scholar, then filter by title patterns like *revisiting*, *re-examining*, *limitations*, *critique*, *replication*. **[L1]**
3. **Author-and-lab tracking:** the same group often publishes the follow-up. If you are building on their limitation, you are racing them.
4. **Code and README search:** implementation details (prompt templates, decoding settings, preprocessing) are usually only in the repo or appendix, not the abstract. Differences in these often explain contradictory results. **[L1]**
5. **Dataset and model card search:** provenance, licensing, filter criteria, and known biases live there. **[L1: Datasheets for Datasets, arXiv:1803.09010]**
6. **Venue accepted lists:** scan titles for a conference's most recent edition; preprint search alone misses camera-ready changes.
7. **Negative-result search:** search for the null framing ("does not improve", "no significant difference", "under matched compute") to find the papers that quietly falsify popular claims.
8. **Metrics-literature search:** look for papers about *evaluation validity* in your area — these are goldmines for defensible, small-scope contributions.

### 9.4 Practical search hygiene

- Record **every** query that mattered and what it returned, in the Research Log. Six weeks later you will not remember whether you already checked a design.
- Keep a **one-line verdict** per source: `(claim) / (evidence) / (control?) / (what they did not test)`.
- Treat "not found" as weak evidence. Absence of a hit is often a search-vocabulary failure, not a genuine gap.
- Prefer primary text: open the paper's method and results. An AI summary of a paper is not evidence about that paper. **[L1/L3]**

---

## 10. How to read and interrogate papers

### 10.1 Three passes with three different purposes

**Pass 1 — Triage (5 minutes).** Read title, abstract, figures, and the first and last paragraphs of the introduction *and* of the conclusion. Then answer in one line each:

1. What problem does this paper claim to solve?
2. What did they actually measure?
3. Does it threaten my idea? (If yes, go to Pass 2.)
4. Does it supply something I need: data, metric, baseline, method, or vocabulary?

Stop here for most papers. Write a one-line verdict and move on. **[L3]**

**Pass 2 — Method and evidence (20–40 minutes).** Read the method section, the main results tables, and the limitations paragraph. Extract:

| Field | What you are looking for |
|---|---|
| Claim | The narrow, defensible claim (often narrower than the abstract) |
| Population | Model(s), dataset, split, sample size |
| Manipulation | What varied, and what was held constant |
| Control | The comparison that makes the causal claim meaningful |
| Metric | Construct named vs what is operationally counted |
| Main number | Effect size, not just significance |
| Failure interpretation | What the authors say a null result would mean |
| Limitation | Authors' own admitted boundary |
| **Not tested** | The experiment this paper conspicuously avoided |

The "not tested" column is where your questions come from. **[L3]**

**Pass 3 — Deep interrogation (2–4 hours, only for the handful that matter).** Read appendices, prompt templates, decoding settings, and the code if available. Reproduce one headline number, or at least recompute it from their released outputs. Check whether the metric is computed as described. Check whether the sample is balanced. Check whether the training/test split leaks. This is also the pass where you often discover that a claim is *narrower* than the abstract implies — which reshapes your own question. **[L1/L3]**

### 10.2 Where to look for what

| You want | Look here |
|---|---|
| The real claim | Last paragraph of the intro; limitations |
| What actually changed | Method section, "Experimental Setup" |
| Whether the effect is real | Results tables + effect sizes, not figures alone |
| Whether the comparison is fair | Appendices, prompt templates, hyperparameters |
| Whether the data supports it | Dataset card, item inspection, label statistics |
| Whether it reproduces | Code repo, released outputs, version history on arXiv |
| Whether it was challenged | Forward citations, later papers, review discussion |
| What they avoided | The gap between their claim and their strongest control |

### 10.3 Six questions that make a paper yield its limits

1. What is the **control**, exactly?
2. What **else** differs between conditions?
3. Does the **metric** measure the construct named in the title?
4. What happens to the result if the **metric** is changed to a continuous/linear variant? (A lesson from the emergent-abilities reassessment: [arXiv:2304.15004](https://arxiv.org/abs/2304.15004).)
5. What is the **strongest simpler explanation** the paper does not rule out?
6. What would the paper look like if the **effect did not exist** — is any figure or statistic incompatible with that?

Question 6 is a compact falsifiability test. If nothing in the paper is incompatible with "no effect," the paper is descriptive, and you now know exactly what experiment is missing. **[L3]**

### 10.4 Reading with AI assistance — rules that keep you honest

**Safe uses [L3]:**
- Summarize a paper you have already opened, then verify each claim against the PDF.
- Generate query variants and vocabulary synonyms.
- Extract a structured table (claim/data/control/metric/limitation) for a paper you paste in.
- Explain a technical method or statistic you do not know.

**Unsafe uses:**
- Asking "is this gap novel?" and treating the answer as evidence.
- Asking "what did paper X find?" without reading paper X.
- Accepting invented citations. Every reference must be opened before it enters your thesis.
- Letting a summary of a summary become your description of a paper's design.

**Rule [L3]:** AI may compress your reading; it may not replace the act of verification. One fabricated citation in a thesis is far more costly than an extra hour of reading.

### 10.5 When to stop reading a paper

Stop immediately if any is true:

- the paper's question is not your question, and it supplies no data, metric, baseline, or design idea;
- you are reading it only because it appeared in a search list;
- you cannot state its main claim after ten minutes;
- you are reading the same background section for the fourth time;
- you already have its one relevant sentence.

Deep reading is reserved for the papers that can change your experiment. Everything else is five minutes. **[L3]**

---

## 11. Building a field map

### 11.1 Purpose and size

A field map is **one page** (or two screens) that lets you answer: what do people believe, how do they measure it, what do they disagree about, and where is the frontier? It is a thinking tool, not a bibliography. A 300-entry Zotero library is not a field map; it is a pile. **[L3]**

### 11.2 The ten slots

| Slot | Content | How to fill it fast |
|---|---|---|
| 1. Foundational work | 2–4 papers everyone cites | Follow references from two survey/position papers |
| 2. Recent influential work | 3–6 papers from the last 12–18 months | Sort arXiv by date; check venue accepted lists |
| 3. Competing directions | 2–4 schools of thought | Ask "what do these papers argue against?" |
| 4. Benchmarks | Named evaluation suites | Search `benchmark` + area term; check dataset cards |
| 5. Datasets | Public corpora with provenance | Hugging Face datasets search; dataset cards |
| 6. Common methods | The 3–6 techniques used repeatedly | Method sections of the defining papers |
| 7. Known failure modes | Documented weaknesses of current systems | Limitations sections; error analyses |
| 8. Unresolved questions | Explicitly posed open problems | Limitations + "future work" + position papers |
| 9. Controversies | Where results contradict | Compare papers reporting opposite directions |
| 10. Terminology variants | Different names for the same thing | Track synonyms across communities |

### 11.3 A compact format that works

```text
TERRITORY: <name>

WHAT THE FIELD BELIEVES
  • <claim> — [paper A] — evidence: <one line> — control: yes/no
  • <claim> — [paper B] — evidence: <one line> — control: yes/no

HOW IT MEASURES
  • metric M1 — counts: <what> — weakness: <what it conflates>
  • metric M2 — ...

WHAT IT DISAGREES ABOUT
  • A vs B on <issue> — likely cause of disagreement: <setup difference>

WHAT IT HAS NOT RULED OUT
  • <alternative explanation> — no matched control found on <date of search>

DATA / MODELS / COMPUTE I CAN USE
  • dataset: <name, size, license, inspection status>
  • model: <name, size, VRAM fit>
  • baseline: <what I can reproduce>

MY CANDIDATE QUESTIONS (ranked, with kill reasons)
  1. ...
  2. ...
```

This fits on one screen and is updated in place. **[L3]**

### 11.4 How it evolves

| Stage | Map shape |
|---|---|
| Day 1 | Slots 1, 4, 6 filled crudely; everything else "unknown" |
| Day 3 | Slots 2, 5, 10 filled; slot 8 has candidate questions |
| Day 7 | Slot 3 (competing directions) and slot 7 (failure modes) filled; slot 9 has real disagreements |
| After closest-work search | Slot 8 becomes a ranked list with kill reasons |
| After pilot | Map gains an "evidence from my own data" section |

An empty slot is informative. "I cannot name any controversy in this territory" usually means either the field is stable (good but hard to contribute to) or you have not read enough to see the fault lines. **[L3]**

### 11.5 Building a map in two focused days

**Day 1 (4 hours).**
- Find two recent surveys or position papers; extract slots 1, 3, 6, 8.
- Pull the 6 most-cited recent papers; skim each for slot 7 and their §Limitations.
- Note vocabulary variants as you go (slot 10).

**Day 2 (4 hours).**
- Search benchmarks and datasets; open each dataset card; write one line on provenance and known bias (slots 4, 5).
- Compare two papers that seem to disagree; identify the setup difference (slot 9).
- Write the map in the format above. Mark every uncertain entry with `?`.
- End the day by writing **three candidate questions** and their current kill reasons.

### 11.6 What the map is for

The map is not a deliverable. It is the object you use when deciding:

- Is my question already answered? (§13)
- Which experiment is closest to mine? (§12)
- Do I have the data and compute? (§17)
- Which control would a reviewer demand? (§20)

**Anti-pattern [L2/L3]:** the workspace contains very large audit reports whose size was treated as progress. In practice, the *decisions* they produced were small in number. When the map no longer changes your plan, stop expanding it — that is the signal that exploration has reached diminishing returns.

### 11.7 One more habit: the "frontier date"

Write today's date next to slot 2 and update it whenever you search. If the frontier date is more than a month old, the space may have moved. Before freezing a question, re-run search #10 from §9.1 (recent work) one final time. Half an hour here prevents the worst outcome in §28: writing a full thesis on a question published while you were writing it. **[L3]**

---

## 12. Finding the closest existing work

### 12.1 The definition that matters

> The closest work is not the paper with the most similar title. It is the paper whose **(manipulation, measurement, population)** triple most nearly equals yours.

A paper can share your vocabulary and none of your design; another can use completely different words and have already run your exact experiment. Search on the triple, not the title. **[L1/L3]**

### 12.2 Decompose your experiment into a design vector

Write yours down first:

```text
manipulation : <what I vary>
control      : <what is held constant / the matched baseline>
measurement  : <what I count and how>
population   : <models, datasets, sizes, languages>
protocol     : <budget, seeds, parsing, statistics>
```

Then search each component independently (§9.2), and score candidate overlaps:

| Overlap | Meaning | Action |
|---|---|---|
| All five match | Already published | Kill or pivot |
| Manipulation + measurement match, population differs | Dataset/model-substitution gap | Ask whether the difference is scientifically meaningful (§13) |
| Manipulation differs, measurement matches | Your measure may be the contribution | Validate the measure |
| Measurement differs, manipulation matches | Your metric may be the contribution | Validate the metric |
| Only the phenomenon matches | Normal | Read their limitations |
| Nothing matches, but their limitations name your question | Strong signal | Proceed to §13 |

### 12.3 Where to look, in order

1. **The related-work section of the phenomenon paper** — authors name the closest work and often state what they did not do.
2. **Forward citations of that paper, newest first** — extensions, critiques, concurrent work.
3. **Full-text search on design terms**, not topic terms: `length-matched`, `placebo`, `matched budget`, `source attribution`, `control condition`.
4. **Papers using your dataset or benchmark** (dataset name + task filter).
5. **Papers using your model** — model-specific studies reveal quirks you would otherwise attribute to your manipulation.
6. **Venue accepted-paper lists for the last two editions** — camera-ready versions often add the control requested in review.
7. **Preprints from the last 3–6 months** at the venues you would target.
8. **Public review/discussion pages** — if reviewers demanded your intended control, the control is regarded as important and currently missing.

### 12.4 The two-sentence design-difference statement

Do not proceed until both sentences are true and specific:

> **Closest work:** [Paper] varies [manipulation] and measures [measurement] on [population].
> **My work differs in design because** [structural difference], and this matters because [expected divergence in outcomes].

Bad: "My work differs because I use a length-matched control" — with no statement of why that changes the interpretation.
Good: "…because their comparison confounds conflict language with increased output length; my control varies conflict semantics at fixed length, so an identical shift under the neutral arm would falsify the conflict-specificity hypothesis."

The second version names the falsifying outcome. That is the standard. **[L3]**

### 12.5 Worked closest-work table (verified anchors)

| Closest work | Manipulation | Measurement | Population | Design difference that remains open |
|---|---|---|---|---|
| CoT faithfulness under biasing features ([arXiv:2305.04388](https://arxiv.org/abs/2305.04388)) | Input biasing (e.g., answer-position bias) | Whether the stated rationale mentions the bias | Text LLMs, MCQ and bias tasks | Multimodal premise conflict; length-matched neutral deliberation control; measure of which source the reasoning engages |
| CLASH benchmark ([arXiv:2511.19199](https://arxiv.org/abs/2511.19199)) | Controlled object/attribute contradictions; fine-tuning | Contradiction detection, MCQ and open-ended | COCO-based pairs, several VLMs | Detection-oriented; does not measure post-detection arbitration; whether detection and arbitration dissociate |
| RH-AUC / RH-Bench ([arXiv:2505.21523](https://arxiv.org/abs/2505.21523)) | Reasoning length, natural and induced | Perception accuracy versus reasoning length; attention analysis | Multimodal reasoning models, several tasks | Whether trajectory change is due to conflict semantics rather than compute |
| Grounding IDs ([arXiv:2509.24072](https://arxiv.org/abs/2509.24072)) | External symbolic cues (partitions, annotations) | Embedding alignment, modality gap, attention, causal interventions | LVLMs across grounding tasks | Cue-induced binding versus cue-induced arbitration under conflicting premises |

**How to use this table.** It is not a novelty claim; it is an audit trail. For each row you can state which design element is shared and which is missing. If no row matches both your manipulation and your measurement, your question is probably unoccupied — but confirm via §13 first. **[L3]**

### 12.6 Practical tricks

- **Search the control, not the claim.** Added controls often appear only in a table caption or appendix.
- **Search the phenomenon under its measurement names:** faithfulness, reliance, arbitration, conflict detection, sycophancy, grounding degradation.
- **Borrow mature methodology from other fields.** Matched placebo, blinding, and pre-registration are late imports into ML; importing one correctly can itself be a contribution.
- **Date-stamp your closest-work table.** Novelty decays; the frontier moves fastest in crowded subfields.

---

## 13. Verifying whether a gap is real

### 13.1 The ten questions, with the evidence that answers each

| # | Question | How to answer it | Verdict if true |
|---|---|---|---|
| 1 | Has it been answered directly? | Find a paper whose manipulation + measurement match yours | Gap is **occupied** — kill or pivot |
| 2 | Has it been answered indirectly? | Look for a paper that answers your question as a side-effect of another study; check its tables | Gap likely **occupied** |
| 3 | Has an equivalent experiment been done under different terminology? | Search by design vector (§12.2), not by words | Occupied — re-frame your framing, not your experiment |
| 4 | Has later work closed the gap? | Forward citations, newest first; search the last 6 months | Occupied |
| 5 | Is it only a dataset/language/model difference? | Ask whether the effect could plausibly reverse; if not, it is a replication | **Weak gap** — insufficient alone |
| 6 | Is that difference scientifically meaningful? | Name a mechanism that would change across that difference | If you can name one → gap may be real |
| 7 | Is the missing experiment important? | Ask what claim currently rests on the untested assumption | If nothing rests on it → unimportant |
| 8 | Would the result change understanding? | Write the two sentences you would add to the field's knowledge under each outcome | If both sentences are dull → kill |
| 9 | Could the result be trivially predicted? | Ask whether a competent practitioner would bet on the outcome | If yes → not a research question |
| 10 | Would a negative result still teach something? | State what a null result rules out | If nothing → redesign or kill |

### 13.2 The three verdicts

- **REAL** — no matching manipulation+measurement found by two independent searches; the closest work's own limitations name your question; and both positive and negative outcomes carry meaning.
- **UNCLEAR** — searches are inconclusive, or you suspect terminology/dataset variants you cannot rule out. Cost of resolution: one more focused search session. Do not spend more than that before asking "could I answer my own question with a 20-item pilot instead?"
- **OCCUPIED** — a paper (or combination of two) already answers it. Record the citation, write one line, and move to your next candidate question. This is a win, not a failure: it cost you a day instead of three months.

### 13.3 Classes of "gap" and what they are actually worth **[L3]**

| Gap class | Typical value for a thesis |
|---|---|
| Missing control on a causal claim | **High** — small, decisive, defensible |
| Measurement validity (metric conflates constructs) | **High** — often generalizes beyond one dataset |
| Boundary condition (works only under X) | Medium–high — needs a mechanism story |
| Contradiction between two papers | Medium–high — a rerun with matched settings can resolve it |
| New dataset/benchmark | Medium — strong only if it exposes a new behavior, not just new items |
| Language/culture transfer | Medium — needs an argument that findings should not transfer |
| New method outperforming baselines | Medium — high risk, needs compute and careful baselines |
| Dataset substitution (M on D) | Low |
| Scale-up of an existing study | Low–medium |
| Exact-phrase novelty | Near zero |

### 13.4 Gap verification worksheet

```text
CANDIDATE GAP: <one sentence>
MY MANIPULATION / MEASUREMENT / POPULATION: <design vector>
SEARCH 1 (phenomenon terms):       queries used / hits / closest match
SEARCH 2 (design terms):           queries used / hits / closest match
SEARCH 3 (forward citations):      papers citing the anchor work / any with my control?
SEARCH 4 (recent 6 months):        anything new?
CLOSEST WORK:                      <citation> — manipulation/measurement/population
DESIGN DIFFERENCE:                 <two sentences from §12.4>
IF POSITIVE RESULT → field learns: <one sentence>
IF NEGATIVE RESULT → field learns: <one sentence>
VERDICT:                           REAL / UNCLEAR / OCCUPIED
DATE OF VERIFICATION:              <date>
NEXT ACTION:                       pilot / second search / kill
```

### 13.5 The self-deception test

Ask: **"If a competent reviewer were trying to reject my novelty claim, what paper would they cite?"** Then go find that paper. If you find it and it does not have your control or your measure, you have *strengthened* your claim and produced the related-work paragraph at the same time. If you find it and it does have them, you have saved months. **[L3]**

### 13.6 Your history at this step **[L2]**

Novelty in the workspace was repeatedly adjudicated by **vocabulary** ("no paper uses this term") and by **volume of audit documents**, rather than by design comparison. Two concrete consequences appear in the retained material:

1. Candidate branches (reasoning-trace degradation; binding-IDs natural transfer; cultural causal steering) were argued against literature that was summarized at high abstraction, making it hard to see whether a *matching control* existed.
2. The branch that ultimately survived did so because its design became concrete enough to compare: length-matched placebo, same items, per-item budgets, deterministic classification. Once the design vector existed, the novelty question became answerable in an afternoon.

**Rule [L3]:** you may not claim novelty until you can fill in §13.4 completely, including the closest work's manipulation and measurement. Abstract novelty claims are not falsifiable; design comparisons are.

---

## 14. Competing explanations and hypotheses

### 14.1 Why this section exists

Most wasted effort in ML research comes from a design that cannot distinguish the intended cause from a boring one. The remedy is mechanical: **list every plausible explanation, then build a condition that separates them.** **[L3]**

### 14.2 The alternative-explanation taxonomy

For any behavioral effect, check for these. Most real effects are contaminated by at least two.

| Class | Concrete form | Cheap check |
|---|---|---|
| Compute / length | Longer generations get more layer passes | Token and step counts per arm |
| Prompt framing | Wording, politeness, role, format, position | Neutral rewording arm |
| Instruction burden | Arm asks for more work, not different work | Equal-format instruction |
| Measurement artifact | Parser, classifier, or regex picks up the wrong thing | Manual inspection of 20 outputs |
| Data artifact | Templated items, label leakage, duplicate items | Item inspection, dedup, label statistics |
| Class imbalance | Effect driven by a majority class | Per-class breakdown |
| Model-specific quirk | One model's prompt sensitivity | Second model of different family/size |
| Decoding parameters | Temperature, top-p, max tokens, stop criteria | Fixed decoding across arms |
| Preprocessing | Resolution, resizing, image normalization | Same pipeline verified by checksum |
| Seed variance | Run-to-run variation mistaken for effect | Repeat on 2–3 seeds or deterministic setting |
| Contamination | Test items present in training data | Check dataset provenance and model card |
| Annotator/judge bias | Subjective labels or LLM judge drift | Inter-rater agreement; judge calibration set |
| Selection of examples | Hand-picked items that favor the story | Random sampling with a fixed seed |
| Truncation / failure | Output cut off before the behavior appears | Truncation counters per arm |

### 14.3 Turn explanations into competing hypotheses

For each explanation, write a **signature**: what the data must look like if it is the true cause.

```text
H_effect : behavior B is caused by the manipulated construct C
           signature: B rises only when C is present; matched neutral arm shows no rise

H_confound_length : B is caused by additional computation
           signature: a neutral arm with the same token budget shows the same rise

H_confound_format : B is caused by output-format instructions
           signature: an arm with identical format but no C shows the same rise

H_artifact : B is caused by the classifier/parser
           signature: manual annotation of a sample disagrees with the automatic labels

H_null : B does not exist; observed difference is noise
           signature: effect disappears on rerandomized splits or additional seeds
```

### 14.4 The control matrix

Draw the arms as rows, the explanations as columns, and mark which arm can rule out which explanation. Every column must have at least one arm marked, or you cannot rule that explanation out.

| Arm | rules out length | rules out framing | rules out format | rules out artifact |
|---|---|---|---|---|
| Direct baseline | – | – | – | – |
| Neutral placebo, matched length | ✔ | partial | – | – |
| Neutral placebo with identical output format | ✔ | ✔ | ✔ | – |
| Manual annotation audit (20 items) | – | – | – | ✔ |
| Repeat with alternate seed / second model | – | – | – | – |

If a cell is empty on the diagonal, your design cannot attribute the effect. Fix the design or weaken the claim. **[L3]**

### 14.5 Worked instance (your design, reconstructed) **[L2]**

Your protocol's four arms map onto this matrix as follows:

- **Arm 1 (direct zero-shot):** establishes the unaided behavior — and revealed the text-following default (85.5% text; 13.8% image).
- **Arm 2 (neutral placebo):** controls for deliberation/length — and produced 89.5% image-following, exposing a large prompt-framing effect.
- **Arm 3 (conflict verbalization):** the manipulation of interest — 25.8% image-following, 13.7% abstention.
- **Arm 4 (prefill probes):** attempts to distinguish "explanation steers behavior" from "explanation is post-hoc," by injecting opposing rationale prefixes and observing divergence (41.4% divergence; +5.3 pp text alignment in one direction).

The residual weakness, stated honestly: **Arm 2 matched length on average but not per item** in the early run (61.2 vs 3.4 tokens for direct), and prompt framing differs between the direct and placebo arms in ways that may themselves be the cause of the "visual capture" pattern. A reviewer will attack this before anything else. Writing that sentence yourself, in the thesis, converts a fatal flaw into a stated limitation with a concrete future experiment. **[L2/L3]**

### 14.6 Rules for hypothesis hygiene **[L3]**

- Exactly two primary hypotheses (H₁ and H₀), each with a signature.
- Both outcomes must be publishable statements; if a null result would be embarrassing rather than informative, your question is not scientific enough yet.
- Record the decision rule *before* the run: threshold, test, and the interpretation of each outcome.
- Do not stack many secondary hypotheses to fish for significance. Label exploratory analyses as exploratory.
- If a third explanation appears after the data arrive, report it as exploratory and plan a follow-up; do not silently re-frame the original hypothesis.

---

## 15. Adversarial idea testing

### 15.1 Purpose

You are not defending your idea. You are trying to destroy it as cheaply as possible, because the cost of destruction rises monotonically with time invested. **[L3]**

### 15.2 The attack list

| Attack | The question | Fatal hit |
|---|---|---|
| Prior-art | "Which single paper could already have killed this?" | A matching manipulation + measurement |
| Redundancy | "What result would make my contribution unnecessary?" | A trivial baseline reproduces the finding |
| Simplicity | "What is the simplest explanation for the expected result?" | Prompt length or formatting explains it |
| Data | "Could dataset construction produce the effect?" | Templated or synthetic conflicts unacknowledged by the paper |
| Baseline | "Could a trivial baseline reproduce it?" | Majority-class or prompt-only baseline matches it |
| Compute | "Could extra compute explain the gain?" | Unmatched tokens or steps |
| Prompt wording | "Could phrasing alone explain it?" | Rewording reproduces it |
| Measurement | "Does my experiment measure the thing I claim?" | Metric conflates selection with computation |
| Statistics | "What if the sample were smaller or split differently?" | Effect only under one arbitrary split |
| Generalization | "Does this depend on one model, dataset, language?" | Yes, while the mechanism story predicts universality |
| Reviewer | "What is the first sentence a skeptical reviewer writes?" | Unanswerable within one experiment |
| Publication risk | "Could someone publish this while I run it?" | Crowded, fast-moving space |

### 15.3 The strongest-objection discipline

Write the *strongest* objection (not a straw man), the evidence that answers it, and the residual vulnerability:

```text
STRONGEST OBJECTION: The effect is explained entirely by output length.
EVIDENCE TO ANSWER: A neutral deliberation arm with per-item token matching
                    shows no comparable shift.
RESIDUAL VULNERABILITY: Neutral arm wording still differs; add a second neutral
                    variant with different content at equal length.
```

If answering the objection needs more compute than you have, the question is currently infeasible (§17). That is a finding, not a failure.

### 15.4 Red-team with three personas **[L3]**

- **Statistician:** "Sample size, unit of analysis, paired or unpaired test, multiple comparisons?"
- **Hater:** "This is just prompt engineering." Your response must be a *design element*, not a paragraph of prose.
- **Replicator:** "I have one hour and your paper. Can I reproduce your numbers?" If not, your reporting is incomplete.

### 15.5 Worked adversarial audit of your frozen design **[L2]**

| Attack | Status in the retained evidence | What remains |
|---|---|---|
| Prior-art | Text-LLM faithfulness and multimodal detection benchmarks exist; no matching matched-legit control located in the workspace | Complete §12.4 statement and date-stamp the search |
| Simplicity (length) | Arm 2 is the intended answer, but early arms were unequal in tokens (61.2 vs 3.4) | Verify per-item token matching in the v3 run; report token distributions per arm |
| Simplicity (framing) | Direct arm follows text 85.5%; placebo follows image 89.5% | State explicitly that "visual capture" is framing-dependent; add a wording variant if budget allows |
| Measurement | Switched from exact match to engaged-problem classification after the pilot | Report classifier validation (manual audit of a sample, agreement rate) |
| Data | Synthetic arithmetic pairs with templated structure | Report item-level statistics; test a second domain (e.g., chart conflict) if feasible |
| Statistics | Paired McNemar plus Fisher's exact and effect sizes computed | Report the unit of analysis and independence assumptions; run a robustness check on a random half |
| Generalization | Single 3B model family | State as a boundary; second model of a different family is the natural follow-up |

This table is the artifact that turns a description into a defensible thesis: every weakness is named, bounded, and either answered or scheduled.

---

## 16. Fast idea-killing

### 16.1 Why fast killing is a skill

An idea killed in two days returns three months. An idea killed in month three costs a thesis. The objective is high *decision throughput*, not low ambition. **[L3]**

### 16.2 One-hour kill checklist

Answer yes/no with a one-line reason for each:

1. Can I state the phenomenon in one sentence without my method? (no → not a phenomenon yet)
2. Can I state the comparison in one sentence? (no → not a question yet)
3. Can I name at least two explanations? (no → it is an observation, not a question)
4. Does a matched control for the naive comparison exist? (no → the gap may be real)
5. Do data and compute exist today? (no → infeasible unless obtainable within a week)
6. Is there a deterministic measure? (no → high risk)
7. Would a null result be informative? (no → kill)
8. Can I run a 20-item pilot this week? (no → the plan is too large)
9. Is the closest experiment different in design, not just wording? (no → kill)
10. Can I state what the field believes now and what it would believe afterwards? (no → not yet valuable)

Score: 8–10 yes → pilot. 5–7 → narrow or repair. 0–4 → kill now, in writing, with one line of reason.

### 16.3 The pre-mortem

Write the post-mortem before starting:

> "We abandoned this project in month three because ______."

Fill in the three most likely causes, then schedule the earliest cheap experiment that tests the most likely one. Anxiety becomes a plan. **[L3]**

### 16.4 Kills and parks from your own history, reconstructed **[L2]**

| Field | Reason parking it was correct | Killed early? |
|---|---|---|
| Medical imaging and federated learning | Required clinical data, domain labels, multi-institution simulation | No — large audits first |
| Cultural / Bangla VLM repair | Required annotation-heavy cultural evaluation and local benchmark assets | No — extensive autopsies first |
| Multimodal agents (tool use, robotics) | Needed multi-step environments and unbounded evaluation | No — parked after large explorations |
| Binding-IDs natural transfer | Depended on reproducing an external mechanism on new data with unclear controls | Partially |
| Reasoning-trace degradation | Crowded and moving quickly; needs matched-compute controls | Partially |

**Pattern [L2]:** the verdicts were mostly right; the *timing* was late. Each field consumed weeks of reading and document production before the disqualifying constraint (data access, annotation cost, environment complexity, concurrency) was actually evaluated.

### 16.5 The two-day kill window

**[L3] Adopt as a standing rule:**

> Every candidate direction is killed or promoted within **two working days**. Promotion requires a written design vector, a started closest-work table, a feasibility check, and a specified 20-item pilot. Anything else is parked in writing.

Applied consistently, this single rule would have removed the majority of the time cost visible in the retained history. It also makes killing cheap emotionally: parking is the *default*, and promotion is an earned status.

### 16.6 Writing a kill note

Keep it to five lines and store it in the Question Ledger:

```text
CANDIDATE: <one sentence>
KILLED BY: <citation | data unavailable | non-deterministic measure | no discriminating experiment | trivial baseline>
WHAT I LEARNED: <one sentence usable in future>
REOPEN IF: <explicit condition, e.g., "a public Bangla cultural benchmark is released">
DATE: <date>
```

"Reopen if" is important: it prevents both premature killing of good ideas and endless re-litigation of bad ones. **[L3]**

---

## 17. Feasibility during discovery

### 17.1 Feasibility is a research instrument, not a gate at the end

Feasibility questions are *scientific* questions in disguise. "Can I measure this deterministically?" is the same as "what is the construct, operationally?" "Can this run in 16 GB?" constrains how many conditions you can compare, which constrains which explanations you can test. **[L3]**

Evaluate feasibility **while** evaluating the question, with a one-page budget:

| Dimension | Concrete question | Your constraint |
|---|---|---|
| Data | Does the dataset exist, is it licensed, inspectable, correctly labeled? | Public HF datasets only |
| Model access | Weights available? Revision pinned? Fits in 16 GB? | ≤3B, FP16 inference |
| Instrumentation | Can behavior be observed without training? | Inference-only; logits/attention optional |
| Compute | Items × arms × tokens × seconds per item → total GPU hours | Colab sessions, session time limits |
| Implementation | Days to a working harness, including parsing and checkpointing | ≤5 days |
| Evaluation | Deterministic parsing possible? Judge needed? | Prefer regex/exact classification |
| Experiment count | How many arms and replications are needed to rule out the main confounds? | ≤6 arms |
| Reproducibility | Seeds, pinned versions, released configs, saved raw outputs | Required |
| Time | Weeks available from now to defense | Fixed |

### 17.2 The two opposite mistakes

**Mistake A — rejecting a good question too early.** "[X] looks hard, so I will not try." Fix: separate *hard* from *blocked*. Hard means it takes weeks; blocked means an asset does not exist. Convert the question to the smallest version that is not blocked, then check whether that version still answers something (usually it does). **[L3]**

**Mistake B — developing a beautiful question that cannot be tested.** You produce an elegant causal story that requires six model families, human annotation in two languages, and 300 GPU hours. Fix: write the compute line *first*, before the theory. If the arithmetic exceeds your budget, either drop conditions or drop the question. **[L3]**

### 17.3 The compute line, computed honestly

```text
GPU hours ≈ items × arms × avg_tokens × seconds_per_token / 3600

Example: 1,619 items × 3 arms × 120 tokens ≈ 583k forward-decoded tokens.
On a T4 at ~2.3 s per item per arm (measured in your harness):
1,619 × 3 ≈ 4,857 item-passes × ~2.3 s ≈ 3.1 hours of GPU time,
plus checkpointing and restarts → plan for 5 hours and two sessions.
```

Notice the two consequences: (i) the full population across arms is affordable, and (ii) *adding* arms is cheap compared with *adding* rounds of annotation. For inference-only behavioral research, **more arms beat more items** — arms buy causal discrimination, items buy statistical precision. Pay for discrimination first. **[L2/L3; your own harness measured ~2.32 s/item at FP16 with SDPA.]**

### 17.4 Feasibility scoring for candidate questions

| Question | Data | Model | Instrument | Compute | Implementation | Verdict |
|---|---|---|---|---|---|---|
| Does conflict verbalization change engaged source under matched length? | ready | ready | deterministic classifier (validated) | ~5 GPU-hours | harness exists | **Feasible** |
| Is abstention conflict-specific or instruction-induced? | ready (add neutral uncertainty arm) | ready | classifier + refusal text inspection | ~2 GPU-hours added | modest | **Feasible, high value** |
| Does the effect generalize to chart reasoning conflicts? | secondary dataset exists in config | ready | domain-specific parsing needed | ~3 GPU-hours | 2–4 days | **Feasible later** |
| Does the effect arise from attention reallocation? | ready | ready | attention instrumentation required, unclear validity | unknown | high | **Blocked for now** |
| Does the mechanism transfer across three model families? | ready | requires additional checkpoints | ready | ~15 GPU-hours | moderate | **Deferred to future work** |

**[L3] Rule:** every candidate question gets a feasibility verdict on the same day it is proposed: Feasible / Feasible later / Blocked. Blocked items go to the Question Ledger with a reuse condition, not into the thesis plan.

### 17.5 Feasibility's second face: interpretability

A run is only worth doing if the outcome can be interpreted under every possible result. Before running, complete:

```text
If the effect appears            → I conclude ______
If the effect is absent          → I conclude ______
If the effect appears only in X  → I conclude ______
If the data are unparseable      → my fallback analysis is ______
```

If any line is blank, the run is not yet feasible in the scientific sense, regardless of compute. **[L3]**

---

## 18. Designing the minimum discriminating experiment

### 18.1 Definition

> The **minimum discriminating experiment (MDE)** is the smallest procedure that makes two live explanations predict different observations.

It is not the smallest experiment that produces a number. It is the smallest one that produces a *decision*. **[L1/L3]**

### 18.2 Why this is decisive for a short thesis

A short thesis cannot win by scale — you cannot out-train a lab. It wins by **design leverage**: a small, well-controlled experiment can produce a strong causal claim, while a huge, uncontrolled one produces nothing interpretable. **[L3]**

The reduction procedure:

```text
1. State the claim you want to be able to make.
2. State the two explanations it must separate.
3. Ask: what is the smallest observable difference between them?
4. Choose the minimum population that can show that difference.
5. Fix every other variable.
6. Define the failure interpretation.
```

### 18.3 Five worked reductions

| Instead of… | Run the MDE… | Why it works |
|---|---|---|
| "Build a new VLM architecture for conflict handling" | Does injecting an opposing rationale as a prefix change the final answer more often than a matched neutral prefix? | Isolates the causal contribution of the *explanation* without changing the model |
| "Build a new benchmark for cross-modal conflict" | Take 50 existing conflict items and test whether the standard metric conflates detection with arbitration | Tests a *claim about measurement*, cheaply and generally |
| "Train a culturally adapted multimodal model" | Does providing locally-grounded context (versus a length-matched generic context) change answers on the same 50 items? | Tests cultural-context sensitivity without training |
| "Perform full attention/representation analysis" | Does a length-matched neutral prompt reproduce the behavioral shift? | Removes the dominant confound before any mechanism work |
| "Show that long reasoning degrades perception" | Recompute the reported trend using a continuous perception metric on the *published* outputs | A metric-choice audit is hours of work and can change the conclusion ([arXiv:2304.15004](https://arxiv.org/abs/2304.15004)) |

### 18.4 How small can a pilot be?

For an **instrument-validation pilot**, 20–50 items is usually enough, because the goal is not significance but *parseability and direction*:

- Are outputs parseable at a target rate (e.g., ≥90%)?
- Do the arms produce distinguishable behavior at all?
- Are token budgets sufficient (no truncation at the ceiling)?
- Does the classifier agree with manual inspection on this sample?
- Are there degenerate outputs (refusals, repetition, format collapse)?

If the pilot cannot answer these questions, do not proceed to the main run. Your own project demonstrates the cost of skipping this: a 500-item run was invalidated by a 15-token budget that produced 100% truncation in one arm. **[L2]**

For the **main experiment**, sample size follows the effect size you are willing to detect and the precision you need for the estimate. With paired within-item designs and large effects, a few hundred items can be highly informative; with small effects, you need many more. Report confidence intervals, not only p-values. **[L1/L3]**

### 18.5 The "one comparison at a time" rule

A design where two things vary cannot attribute the effect. If you must vary two, include the factorial cell that isolates them. Your four-arm structure is exactly this logic: direct, neutral, conflict, and prefill-probe, with one manipulated dimension between the key arms. **[L2/L3]**

### 18.6 The one-GPU-hour exercise

Before designing a full study, ask: **"What can I learn in one GPU-hour?"** Then design that experiment and run it. It forces you to choose the most discriminating comparison. In your case, one GPU-hour covers roughly 1,500 item-passes — enough for a 500-item two-arm comparison, which is precisely the scope that revealed both the metric problem and the truncation problem. **[L2/L3]**

### 18.7 MDE acceptance checklist

The MDE is ready when all are true:

- [ ] Claim, explanations, and discriminating observation are written.
- [ ] Control is matched per item on the nuisance variables (length, format, budget).
- [ ] Outcome measure is deterministic and has been validated on 20 outputs by hand.
- [ ] Failure interpretation is written for each possible result.
- [ ] Compute estimate is under budget.
- [ ] You can explain the design to a peer in 60 seconds.

---

## 19. From research question to experimental system

### 19.1 The transition, with the reasoning at each step

```text
Question
  → Hypotheses            (why: make predictions falsifiable)
  → Variables             (why: make the comparison operational)
  → Controls              (why: exclude rival causes)
  → Dataset               (why: fix the population and the unit of analysis)
  → Baseline              (why: define "no effect" and the trivial alternative)
  → Evaluation            (why: define what counts as evidence)
  → Pilot                 (why: validate the instrument before committing)
  → Main experiment       (why: produce the decisive contrast at scale)
  → Ablations             (why: attribute the effect to the intended component)
  → Robustness            (why: test boundary conditions and fragility)
  → Analysis              (why: quantify and test, with stated assumptions)
  → Interpretation        (why: separate what was shown from what is suggested)
  → Contribution          (why: state what changed in the field's knowledge)
```

Each arrow is a *commitment*. Freezing an earlier step reduces the freedom of later steps, which is why freezes should be minimal and deliberate. **[L3]**

### 19.2 Operationalization: the step students skip

A question is not executable until each term becomes a measurable operation:

| Abstract term | Operational decision | Risk if left vague |
|---|---|---|
| "Follows the image" | Classifier over entity mentions + exact answer match as secondary | Construct drift; disputes about interpretation |
| "Conflict verbalization" | Exact prompt template with fixed sentence count and format | Unreproducible intervention |
| "Matched control" | Per-item token count within tolerance, same format | Confound with compute |
| "Abstention" | Explicit refusal patterns parsed deterministically, plus manual audit | Inflated abstention from truncation |
| "Longer reasoning" | Token count of the reasoning segment, not the whole output | Circular measurement |

Write the operational table into the Experiment Specification (§29). If two people would implement different things from your description, it is not yet operational. **[L3]**

### 19.3 Unit of analysis

Decide once: is the unit the item, the item×arm pair, the model, or the seed? This determines the statistical test. For paired within-item comparisons (as in your design), the natural unit is the item, and discordant pairs drive McNemar's test. Getting this wrong is one of the most common reviewer objections. **[L1/L3]**

### 19.4 What to freeze and what to leave free

| Freeze before the main run | Leave flexible until analysis |
|---|---|
| Prompt templates (verbatim, in the repo) | Exploratory subgroup analyses |
| Token budgets per arm | Additional descriptive statistics |
| Model revision and dtype | Visualization choices |
| Dataset split and item selection | Follow-up experiments for future work |
| Parsing/classification rules and thresholds | Secondary outcome definitions |
| Primary hypothesis, primary metric, decision rule | Narrative emphasis |
| Seeds and decoding parameters | Discussion framing |

Flexibility in the left column is a risk, not a virtue. Flexibility in the right column is normal science. **[L3]**

### 19.5 Pre-specify the analysis plan (one page)

```text
PRIMARY:    metric, comparison, test, threshold, direction
SECONDARY:  exploratory analyses, clearly labeled
EXCLUSIONS: items dropped and why (unparseable, degenerate, truncated)
PARSING:    exact rules, fallbacks, and manual-audit procedure
REPORTING:  distributions, effect sizes, CIs, and per-arm token statistics
FAILURE:    what each null result implies
```

### 19.6 Engineering that serves science

Your harness already contains the right instincts and is worth reusing as a template: deterministic seeds, checkpointing with resume, per-item token and truncation flags, storing both prompt and raw outputs, fixed output directories, and a separate statistical suite that emits markdown plus a LaTeX table. **[L2]**

Three improvements worth making in the next project **[L3]**:

1. **Log the token distribution per arm**, and assert the per-item matching tolerance in code — so the control's validity is machine-checked, not assumed.
2. **Log classifier inputs and outputs** for a random sample, so manual validation is a script, not a memory.
3. **Write a `PROTOCOL.md`** with the frozen config, commit-like hash of prompt templates, and the analysis plan *before* the main run. In a project without Git history, this file is your reproducibility backbone. (See §25.6 and [arXiv:2003.12206](https://arxiv.org/abs/2003.12206).)

---

## 20. Baselines, controls, metrics and evaluation

### 20.1 Baselines: three kinds, all required

| Kind | Purpose | Example in a VLM study |
|---|---|---|
| **Trivial baseline** | Shows the effect is not achievable without the intervention | Always answer with the text answer; always answer with the image answer; majority-class |
| **Strongest available baseline** | Shows the intervention beats the competitive alternative | Best published prompt/decoding strategy; a second reasoning scaffold |
| **Matched-compute baseline** | Shows the effect is not merely extra computation | Neutral deliberation prompt with equal token budget, equal format, equal position |

Missing the *trivial* baseline lets reviewers ask whether a constant strategy already does as well. Missing the *matched-compute* baseline makes any causal claim about the intervention unsupportable. Your design's Arm 2 is exactly a matched-compute baseline, and its early inequality (61.2 vs 3.4 tokens) is exactly why such a baseline must be verified, not assumed. **[L2/L3]**

### 20.2 Controls: four useful kinds

1. **Placebo control** — same form, no active ingredient (neutral deliberation of matched length).
2. **Negative control** — a condition where no effect is expected (aligned, non-conflicting input).
3. **Positive control** — a condition where an effect is known to exist (a manipulation that must move the metric), catching a broken pipeline.
4. **Dose–response control** — vary the strength of the manipulation (e.g., partial vs explicit conflict statements) to check monotonicity.

A design with all four can survive most reviewer objections. Two are usually enough for a thesis: placebo plus negative. **[L3]**

### 20.3 Metrics: construct validity first

For each metric, write three lines:

```text
CONSTRUCT: what it is supposed to measure
OPERATION: exactly what is counted
KNOWN CONFLATION: what else could move it
```

**Metric-validity contributions are among the safest thesis contributions.** A verified example is the selective-classification literature, where common multi-threshold metrics fail stated requirements and a replacement metric changes rankings on most datasets ([AUGRC, arXiv:2407.01032](https://arxiv.org/abs/2407.01032)). The lesson generalizes: *if a metric changes the ranking, the metric is part of the science.*

Practical requirements **[L3]**:

- **Deterministic** where possible: regex, exact match, entity classification with stated rules.
- **Insensitive to the confound** you claim to control: e.g., a measure of engaged problem, not of answer correctness.
- **Reported as distributions**: per-arm token counts, truncation rates, per-class breakdowns — not just means.
- **Reported with uncertainty**: effect size plus confidence interval, not only a p-value.
- **Validated**: manual audit of a random sample, with agreement rate reported.

### 20.4 If you must use an LLM judge

- Build a small human-labeled calibration set (50–100 items) and measure agreement with the judge.
- Freeze the judge prompt and model revision.
- Report judge agreement in the thesis; never present judge outputs as ground truth.
- Prefer a deterministic classifier whenever one is defensible; use judging only for genuinely semantic categories.

### 20.5 Statistical reporting checklist

- Unit of analysis stated explicitly.
- Paired vs unpaired test justified by the design.
- Effect size with CI (odds ratio, risk difference, Cohen's h, etc.).
- Multiple-comparison handling for secondary analyses (label exploratory).
- Sensitivity check: does the conclusion hold on a random half, or with an alternative valid metric?
- Robustness to seed/decoding variation.
- All raw numbers reproducible from released outputs.

**[L1]** Experiment-reporting variance and reproducibility issues are well documented in ML; the standard remedy is transparency about variance, seeds, and configuration ([Deep RL That Matters, arXiv:1709.06560](https://arxiv.org/abs/1709.06560); [NeurIPS 2019 Reproducibility Program, arXiv:2003.12206](https://arxiv.org/abs/2003.12206)).

### 20.6 The evaluation trap specific to your domain

When reporting a behavioral shift, three quantities must always be reported together, or the result is uninterpretable **[L2/L3]**:

1. **The shift** (e.g., image-following 89.5% → 25.8%).
2. **The outcome composition change** (text-following and abstention rates), because a shift can be produced by abstention rather than arbitration.
3. **The token/quality diagnostics** (per-arm token counts, truncation rates, parse rates), because a "shift" can be produced by output truncation.

Your v3 report demonstrates why: the raw shift was accompanied by 13.7% abstention and, in earlier runs, by near-total truncation. Reporting all three keeps the claim honest and makes the analysis robust to the most likely reviewer objection. **[L2]**

---

## 21. Pilot to main experiment

### 21.1 What a pilot is actually for

A pilot is **instrument validation**, not a miniature version of the study. Its jobs **[L3]**:

1. Verify parse rate and format compliance.
2. Verify token budgets — no arm should hit the ceiling.
3. Verify the classifier against manual labels on a sample.
4. Verify that arms produce distinguishable behavior at all.
5. Measure wall-clock time per item to size the main run.
6. Detect degenerate outputs (refusals, repetition, format collapse).
7. Check that the control is matched per item.

A pilot need not have statistical power. It needs to be *diagnostic*.

### 21.2 Pilot acceptance gates (numeric, written in advance)

```text
GATE 1  parse rate ≥ 90% per arm
GATE 2  truncation at ceiling ≤ 5% per arm
GATE 3  classifier manual-agreement ≥ 90% on 20 sampled outputs
GATE 4  per-item token matching within ±20% for the matched control arms
GATE 5  no arm produces > 10% degenerate outputs
GATE 6  both directions of the contrast are observable (the metric can move)
```

If a gate fails, fix the instrument and re-pilot. Do not run the main experiment to "see what happens." **[L2/L3: your 500-item run failed GATE 2 at 100% truncation in one arm and had to be discarded.]**

### 21.3 The main run

- **Freeze the config** (prompts, budgets, model revision, dtype, decoding, seeds) and record it in `PROTOCOL.md`.
- **Checkpoint every item** with resume support; store raw outputs, not only labels.
- **Log diagnostics** continuously: token counts, truncation flags, parse failures, wall time.
- **Monitor, do not tune.** If you change a template mid-run, you must restart; post-hoc tuning destroys the inferential claim.
- **Watch for systematic failures** in the first 50 items; if a gate breaks wholesale, stop and re-pilot.
- **Do not analyze the hypothesis until the run finishes**, or use a pre-registered interim rule.

### 21.4 What your own pilot changed **[L2]**

The pilot's value is visible in the artifacts:

| Pilot discovery | Design change | Consequence |
|---|---|---|
| 85% of direct outputs matched neither answer: the model **computes** rather than **selects** | Replaced exact-match "source arbitration" with engaged-problem classification; abstention became an explicit category | The construct now matches the measure; abstention became a reportable finding |
| Placebo 61.2 tokens vs direct 3.4 tokens | Enforced structured output format and longer budgets; later v3 used 80/200/20 tokens by arm group | The control became plausibly matched; truncation was eliminated |
| 100% truncation at 15 tokens; 90–98% at 90 tokens | Raised budgets; added truncation flags per item | Exact-match accuracy became interpretable at all |
| Conflict arm abstained 25% in 20 items | Abstention modeled as an outcome rather than an anomaly | Produced a second, publishable research question (§7.6) |

That table is the empirical argument for piloting, drawn from your own work rather than from generic advice.

### 21.5 Pilot-to-main decision rule **[L3]**

```text
All gates pass + direction observable + compute affordable → run main
Any gate fails + fixable in ≤2 days                     → fix, re-pilot
Any gate fails + not fixable in ≤2 days                 → narrow the question
Direction not observable even at pilot scale            → the effect is too small for
                                                          the available scale: re-scope
```

### 21.6 Ablations and robustness after the main run

**Ablations** attribute the effect to the intended component: remove the conflict sentence, shorten the explanation, vary the instruction verb, change the position of the conflict statement. **Robustness** tests fragility: alternate dataset slice, alternate model, alternate decoding temperature, alternate classification threshold, random half-split replication. **[L3]**

Order of operations: main result → ablations that answer the strongest objection → robustness on the most fragile assumption. Do not ablate before you know the main effect exists.

---

## 22. Handling unexpected and negative results

### 22.1 Three different things are often confused

| Situation | Definition | What it means |
|---|---|---|
| **Useful negative result** | The hypothesis is falsified by valid evidence; the design could have detected the effect | A scientific finding: the field learns the effect is absent under these conditions |
| **Experiment failure** | The pipeline could not have detected the effect (truncation, parsing, mismatch, crash) | No information: fix and re-run |
| **Uninterpretable result** | The effect appeared, but a confound could explain it equally well | Incomplete finding: add the control or weaken the claim |

The deciding question: **could my design have produced the opposite result if the effect existed?** If no, you have a failure, not a finding. **[L1/L3]**

### 22.2 How controls make negative results interpretable

A null result is only as strong as the controls that would have revealed an effect:

- **Positive control** — a condition known to move the metric, proving the pipeline works.
- **Measurement validation** — a manual audit showing the classifier responds to real differences.
- **Sensitivity margin** — a stated minimum detectible effect, so "no effect" means "no effect above X."
- **Power/precision statement** — confidence interval around the null, so readers know what was excluded.

Without these, "no effect" is ambiguous between "the effect is absent" and "my instrument is blind." **[L1/L3]**

### 22.3 A failed hypothesis can become the contribution

This is common in strong publications and is exactly where your project's most interesting material sits. Patterns to recognize:

| Pattern | Example of the general shape |
|---|---|
| The claimed phenomenon is an artifact of the metric | Emergent abilities appear or disappear with metric choice ([arXiv:2304.15004](https://arxiv.org/abs/2304.15004)) |
| The claimed explanation is unfaithful to the mechanism | CoT rationales omit the actual biasing cause of predictions ([arXiv:2305.04388](https://arxiv.org/abs/2305.04388)) |
| Widely used evaluation metrics fail their own stated requirements | Selective-classification metrics and the proposed replacement ([arXiv:2407.01032](https://arxiv.org/abs/2407.01032)) |
| A behavioral effect is dominated by an unmodeled confound | Your length/framing confound, which reframed "visual capture" as prompt-dependent **[L2]** |
| The effect is real but the mechanism differs | Prefill probes diverge only 41.4% of the time, bounding the causal strength of the rationale **[L2]** |

In each case, the *negative or complicating* finding required the same experimental rigor as a positive one — and it produced a claim the field could not have made before.

### 22.4 Decision tree for a surprising result **[L3]**

```text
Result is surprising
  ├─ Is the measurement valid? (manual audit)        no → fix measurement, re-run
  ├─ Is the control matched? (per-item check)         no → fix control, re-run
  ├─ Could truncation/format explain it?              yes → fix budget, re-run
  ├─ Is it driven by a subgroup? (stratified view)    yes → report subgroup, re-frame claim
  ├─ Does a trivial baseline reproduce it?            yes → the effect is not the intervention
  └─ Otherwise: it is a finding → state it, bound it, and test its robustness
```

### 22.5 Re-scoping instead of hiding

When a result contradicts your hypothesis, you have four legitimate responses **[L3]**:

1. **Narrow the claim** — "the effect holds for explicit conflict statements, not for implicit mismatches."
2. **Change the question** — from "does verbalization steer arbitration?" to "under what conditions does verbalization change the *composition* of outcomes (text, image, abstain)?"
3. **Elevate the confound** — if prompt framing dominates, framing *is* the finding, and the original claim becomes a boundary condition.
4. **Report the null with full diagnostics** — and state the minimum effect size excluded.

What you must not do: silently re-label the metric, drop the arms that failed, or describe an uncontrolled comparison as causal. Each of those converts a scientific result into a questionable one.

### 22.6 What was a failure and what was a finding in your project **[L2]**

| Observation | Classification | Why |
|---|---|---|
| 100% truncation at 15 tokens; 90–98% at 90 tokens | **Experiment failure** | The pipeline could not have detected the behavior; fixed in v3 |
| 85% of direct outputs matching neither answer | **Measurement discovery** | Revealed the construct/metric mismatch — this changed the design for the better |
| Placebo arm at 61.2 tokens vs direct at 3.4 | **Design flaw** | Control not matched; repaired via structured format and budgets |
| 13.7% abstention under conflict verbalization | **Finding** | Not predicted by the original hypothesis; opened a second question (Ladder B) |
| 41.4% divergence between opposing prefill rationales | **Bounded finding** | Indicates the rationale has causal influence on a minority of items, not a decisive one |
| 89.5% image-following under neutral prompt vs 85.5% text-following under direct prompt | **Finding requiring re-framing** | Undermines a simple "visual dominance" reading; supports prompt-framing sensitivity |

That last row is the most scientifically valuable line in the entire workspace, because it constrains the interpretation of everything else. It was not framed that way in the retrospective summaries. **[L2]**

### 22.7 How to write a negative or complicating result

Structure that survives review **[L3]**:

1. **State the hypothesis and the prediction** (including what would have falsified it).
2. **State the design's ability to detect the effect** (positive control, measured sensitivity, precision).
3. **Report the result with uncertainty** (effect size, CI, per-arm diagnostics).
4. **Report the confounds you ruled out, and the ones you could not.**
5. **State what the null excludes**, using the precision statement: "effects larger than X are excluded at 95% confidence."
6. **State what remains open**, and the concrete experiment that would settle it.

Avoid these phrases unless literally true: "we prove that…", "the model cannot…", "there is no effect" (without a sensitivity bound), and "future work could explore…" as a substitute for a stated open question.

### 22.8 The emotional discipline

Negative results feel like failure. Treat them as the *most* informative outcome available, because they constrain the space of explanations. Two habits make this easier **[L3]**:

- **Write the "what would we learn if this fails" line at hypothesis time**, before any data exist. When the data arrive, the line is already written.
- **Keep a 'constraint log'** — every result, positive or negative, recorded as a constraint on future theory. Your thesis is the union of those constraints.

---

## 23. Iterating and changing the research question

### 23.1 Experiments change questions — this is normal and expected

| Evidence | Correct response | Incorrect response |
|---|---|---|
| Baseline fails | Check the baseline implementation; fix if broken; if the baseline genuinely cannot represent the behavior, narrow the population | Declare the baseline "not applicable" and keep the claim |
| Dataset unsuitable | Inspect items; verify labels; find or filter a coherent subset; document exclusions | Silently drop bad items to make the run succeed |
| Effect disappears | Add the omitted control; check per-item matching; reconsider the construct | Report the earlier run and ignore the new one |
| Effect appears in one model only | Report as a boundary condition; test a second family if budget allows | Claim the effect is general |
| Control reproduces the result | The confound *is* the finding; re-frame the contribution | Keep the original causal language |
| Unexpected subgroup behavior | Stratify and report; form a new question | Average it away |
| Intervention works for the wrong reason | Report the mechanism honestly; the artifact is now the contribution | Describe only the intended mechanism |
| Result contradicts hypothesis | Write the constraint; re-scope; possibly pivot (§23.3) | Hark back to earlier drafts that agreed with the hypothesis |

### 23.2 The five legitimate responses to new evidence **[L3]**

1. **Broaden** — the effect holds across more conditions than expected; extend scope carefully, one dimension at a time.
2. **Narrow** — restrict to the condition where the effect is robust; state the boundary.
3. **Replace** — the original question is answered or confounded; promote a better question that the data actually address.
4. **Add a control** — the effect survives but needs one more rival ruled out.
5. **Change the measurement** — the construct was mis-operationalized; rebuild the measure and re-run.

**Abandon** is the sixth option, and it is legitimate when the question is occupied, the effect is unmeasurable at your scale, or the result cannot be interpreted under any available design.

### 23.3 Worked iteration from your project **[L2]**

```text
Q0  "Does explicit conflict verbalization shift source arbitration?"
     ↓ pilot: model does not select between answers; it computes new ones
Q1  "Which problem does the model's reasoning engage, and does verbalization change that?"
     ↓ length mismatch discovered between arms
Q2  "Do the arms differ in engaged problem under per-item matched length?"
     ↓ abstention appears at 13.7%
Q3  "Is abstention conflict-specific or instruction-induced?"  → Ladder B (open)
     ↓ prefill probes diverge only 41.4%
Q4  "On how many items does an injected rationale causally change the answer?"  (bounded claim)
```

Three question changes, all driven by evidence, all recorded. That sequence is a *stronger* thesis narrative than the original single question, because each step is defensible and traceable. The failure mode to avoid is having this sequence happen privately and then writing only the original question as if nothing changed — which is what the retrospective reports tended to do. **[L2]**

### 23.4 The change-control rule

**[L3]** A research question may change only when accompanied by the evidence that forced the change, recorded in the Research Log:

```text
DATE:            <date>
OLD QUESTION:    <verbatim>
EVIDENCE:        <file, table, number>
NEW QUESTION:    <verbatim>
WHAT IS PRESERVED: <which parts of the original design remain valid>
WHAT IS DISCARDED: <which analyses are now moot>
```

This single habit turns chaotic pivoting into a documented, reviewable trajectory — and it is exactly what your workspace lacks, because the pivots were real but the records were rewritten rather than appended. **[L2]**

---

## 24. Freezing the research question

### 24.1 What "freeze" means

A freeze is a **contract with your future self**: the question, hypotheses, primary metric, controls, budgets, and analysis plan stop moving, so that later analyses cannot be tuned to a preferred outcome. It is not a declaration that the science is finished or that no interpretation will change. **[L1/L3]**

### 24.2 Freeze checklist (all required)

- [ ] **Question** is one sentence, names the comparison, and is answerable by the design.
- [ ] **H₁ and H₀** each have a written signature (what the data look like under each).
- [ ] **Primary metric** is operationally defined, deterministic (or judge-calibrated), and validated on a sample by hand.
- [ ] **Controls** are specified per item (matched length/format/budget), with tolerance written down.
- [ ] **Population** is fixed: model revision, dataset split, item count, exclusions.
- [ ] **Pilot gates** have passed (§21.2), with numbers recorded.
- [ ] **Analysis plan** is written before the main run: test, unit of analysis, thresholds, secondary analyses labeled exploratory.
- [ ] **Compute budget** is estimated and affordable within the session limits.
- [ ] **Boundary statement** is written: what this study does *not* claim.
- [ ] **Closest-work table** is complete and date-stamped, with the design-difference statement.
- [ ] **Failure interpretations** are written for each possible outcome.

If any box is unchecked, the honest status is "pre-freeze", and the correct action is one more pilot, not one more document.

### 24.3 What is *not* frozen

- **Interpretation** — must follow the data, including surprises.
- **Related work** — may be updated until submission; new papers can be cited as concurrent work.
- **Additional robustness checks** — allowed if reported as exploratory and not used to replace the pre-registered analysis.
- **Future work** — grows from your constraints and open branches.

### 24.4 Re-opening conditions

A freeze may be lifted only under pre-declared conditions, recorded with the change-control entry (§23.4). Typical legitimate triggers:

1. A pilot gate fails in a way that invalidates the measurement.
2. The main run reveals the metric cannot move (ceiling/floor).
3. A concurrent publication appears with the same design and construct.
4. A confound is discovered that no arm can rule out.

Illegitimate triggers: the result is not significant; the effect is smaller than hoped; a reviewer or advisor prefers a different story; you found a newer, shinier idea.

### 24.5 Freeze artifacts (produce these three files)

```text
PROTOCOL.md        frozen design, prompts verbatim, budgets, seeds, model revision
ANALYSIS_PLAN.md   primary/secondary analyses, tests, exclusions, thresholds
BOUNDARY.md        one paragraph on what the study does not claim
```

Together these cost an afternoon and are worth more than a chapter of prose. **[L1: reproducibility and pre-registration practice; L3: format.]**

### 24.6 What happened in your own project, and the lesson **[L2]**

From the retained artifacts:

- **2026-09-23:** 20-item pre-freeze pilot produced five findings, including the "neither answer" discovery, the length mismatch, and the abstention result. Its action list ended with: *"Re-run the 20-item pilot with the revised prompts and verify parse rate ≥ 90%. Only THEN freeze the topic."*
- **2026-09-24:** the post-freeze handover declares the topic locked and the empirical run complete across N = 1,619.

The v3 harness *does* implement the pilot's fixes (structured format, per-arm budgets of 80/200/20, truncation flags, checkpointing, stored raw outputs). But the retained corpus does not show a documented second pilot with gate numbers before the main run, nor a recorded classifier-agreement audit. **[L2]**

**Lesson [L3]:** the freeze was probably right in substance — the design improvements were real — but the *evidence trail* for the freeze is missing. In future projects, freeze **after** pasting gate results into `PROTOCOL.md`. The freeze date should be a consequence of the evidence, not a calendar decision made the next morning. This is a process fix, not a criticism of the result: the resulting full-population statistics (89.5% → 25.8%, McNemar p = 1.2e-215) are strong, and the truncation problem was genuinely resolved.

---

## 25. End-to-end thesis execution

### 25.1 The pipeline, with the purpose of each element

```text
data preparation   → makes the population explicit and reproducible
baseline           → defines "no effect" and the trivial alternative
experiment harness → controls the manipulation, budgets, and logging
logging            → preserves raw evidence so claims can be re-derived
reproducibility    → pins versions, seeds, and configs
analysis           → quantifies the contrast under stated assumptions
visualization      → makes one claim visible per figure
statistical testing→ separates signal from noise, with uncertainty
failure analysis   → explains where and why the design broke
robustness checks  → tests fragility of the conclusion
documentation      → lets a stranger reproduce and audit the work
```

### 25.2 Design upfront vs keep flexible

| Decide before implementation | Decide during/after implementation |
|---|---|
| Item selection and exclusion rules | Figure aesthetics |
| Prompt templates (verbatim) and output format | Additional descriptive statistics |
| Arm structure and token budgets | Exploratory subgroup analyses |
| Primary metric and parsing rules | Secondary visualizations |
| Seeds, dtype, model revision, attention implementation | Narrative structure and emphasis |
| Output schema for logs and checkpoints | Related-work additions |
| Statistical tests and unit of analysis | Future-work branches |
| Directory layout and file naming | — |

### 25.3 A directory layout that prevents chaos

```text
project/
  PROTOCOL.md            frozen design
  ANALYSIS_PLAN.md       pre-registered analyses
  BOUNDARY.md            claims this study does not make
  src/                   one module per responsibility: data, prompts, model, classify, stats
  configs/               one YAML/JSON per experiment revision (v1, v2, v3)
  results/               raw JSONL per run + checkpoint CSV
  analysis/              scripts that read results/ and emit tables/ + reports/
  figures/               generated only, never hand-edited
  notes/                 research log, question ledger, evidence ledger
  drafts/                thesis chapters
```

Your existing project already approximates this (harness, statistical suite, results, LaTeX table output). The missing pieces are `PROTOCOL.md`, `ANALYSIS_PLAN.md`, and a `configs/` record per version — the three artifacts that make a re-run reproducible months later. **[L2/L3]**

### 25.4 The reproducibility minimum

- One command reproduces the main table from raw outputs.
- Raw outputs are archived and never overwritten (new version = new filename).
- Model revision, library versions, dtype, and attention implementation are recorded.
- Determinism: seeds set; note where nondeterminism remains (GPU kernels, sampling).
- Every number in the thesis traces to a script and a file.

**[L1]** This is the substance of community reproducibility expectations ([arXiv:2003.12206](https://arxiv.org/abs/2003.12206)) and of variance-reporting guidance in ML ([arXiv:1709.06560](https://arxiv.org/abs/1709.06560)). It is also the cheapest defense against the "did you really run this?" question.

### 25.5 Analysis and visualization discipline

- **One figure, one claim.** If a figure needs two paragraphs to explain, split it.
- **Show distributions, not only means** — per-arm token counts, truncation rates, per-class behavior.
- **Annotate uncertainty** on every reported effect.
- **Keep a "figure provenance" line** in the caption: script, run ID, and date.
- **Plot the diagnostics**, not only the headline result: parse rate and truncation by arm belong in the thesis, because they establish interpretability.

### 25.6 Documentation as scientific work

Write, as you go, not at the end:

| Document | Written when | Contents |
|---|---|---|
| Research Log | Daily | decisions, dead ends, bugs, surprises |
| Question Ledger | At each candidate question | status, kill reason, reopen condition |
| Evidence Ledger | At each finding | claim, source, script, file, date |
| `PROTOCOL.md` | At freeze | everything needed to re-run |
| Results Record | During analysis | numbers + interpretation + limitations |

### 25.7 Writing the thesis while running experiments

Draft sections in the order in which they become stable, not in the order they appear in the document:

1. **Method** — drafted at freeze, revised as the harness changes.
2. **Results** — drafted incrementally as runs complete, including diagnostics.
3. **Related work** — written continuously; it is the only chapter that never freezes.
4. **Discussion/limitations** — written with the results, while the confounds are fresh in mind.
5. **Introduction and abstract** — written last, when the contribution is actually known.

This ordering is why the common "write it in chapter order" plan fails: chapters 1 and 2 depend on what chapters 4 and 5 turn out to say. Your current plan (Chapters 3–4 first, then 1–2, then 5) is consistent with this principle. **[L2]**

---

## 26. From thesis to paper

### 26.1 Identify the single central claim

A paper is not a compressed thesis. It is **one claim with the evidence needed to believe it.** Write it as:

> "Under [conditions], [manipulation] [changes/does not change] [measure] relative to [control], which indicates [interpretation]."

Test: if your paper's title needs the word "and," you may have two papers. **[L3]**

### 26.2 What belongs in the paper

| Keep | Cut |
|---|---|
| The frozen question and why it was open | Exploratory branches that did not resolve |
| Design with controls and budgets | Implementation micro-details without inferential role |
| Primary result with effect size and CI | Every secondary statistic |
| Diagnostics that establish interpretability (parse/truncation) | Full hyperparameter tables (appendix instead) |
| Ablations answering the strongest objection | All ablations performed |
| Honest limitations and bounded claims | Speculative mechanism claims without evidence |
| One or two figures carrying the argument | Figures that duplicate tables |

### 26.3 Structure the evidence, not the chronology

Do not narrate the order in which you discovered things. Structure for the reader's inference:

```text
1. Phenomenon and why it is not yet explained
2. The closest work and the specific design difference
3. Hypotheses with opposite predictions
4. Design: manipulation, control, measurement, population
5. Primary result (with the diagnostic that makes it interpretable)
6. Controls/ablations that rule out the strongest rival explanation
7. Boundary conditions and limitations
8. What changes for the field
```

Step 6 is what distinguishes a paper from a report. **[L3]**

### 26.4 Framing the contribution honestly

Two different kinds of contribution; label the right one **[L3]**:

- **Novelty** — nobody has run this experiment / defined this construct this way. Must be justified by a design comparison (§12.4), not by vocabulary.
- **Empirical value** — the experiment is not novel in kind but resolves an ambiguity that matters: a matched control that was missing, a metric validity check, a boundary condition, a prompt-framing effect that reframes an earlier claim.

Your project's strongest defensible framing is primarily **empirical**, with a **measurement** element: a matched-control test of whether conflict verbalization changes which problem the model's reasoning engages, plus abstention as a distinguished outcome and a re-framing of "visual capture" as prompt-dependent. That framing is honest, verifiable from your artifacts, and still interesting. **[L2]**

### 26.5 Handling limitations without destroying the paper

- Put limitations in their own short section, in plain language.
- For each limitation, say whether it **bounds the claim** or **threatens the design**. Bounds are normal; threats need a mitigation or a stated decision.
- Never write "future work could explore X" when X would falsify your claim — say what would falsify it.
- Do not hide the confound; state it and quantify what it could account for.

### 26.6 Avoiding overclaiming: the phrase audit

Before submission, search your draft for: *proves, demonstrates causally, shows that models cannot, generalizes to, robust across models, state-of-the-art, novel architecture, we solve*.

For each hit, ask: does my evidence license this verb, and does the control support it? Replace with the strength your design supports: *provides evidence that, is consistent with, under our conditions, in this model family*. **[L1/L3]**

### 26.7 Choosing a venue for a first paper

| Option | Best when | Cost |
|---|---|---|
| Workshop | Result is narrow but clean; you want feedback | Low prestige, fast, useful |
| Findings/short paper track | Single clean claim with one strong control | Moderate |
| Main conference | Novel construct plus multiple controls plus generalization | High; expect multiple revisions |
| Journal | Extended empirical study with robustness | Slow |

For a first paper, a **workshop or short-paper submission of the single cleanest claim** is usually the highest expected value: it converts your thesis into a citable artifact, generates reviewer feedback, and does not require a second project's worth of generalization. **[L3]**

### 26.8 Revision as re-designed evidence

Reviewers rarely ask for prose changes; they ask for evidence. Keep a table:

| Reviewer comment | What evidence would answer it | Feasible now? | Planned |
|---|---|---|---|
| "The control is not matched" | Per-item token distribution table | Yes (already logged) | Add table |
| "Metric conflates X and Y" | Manual audit of 50 sampled outputs | Yes (few hours) | Add appendix |
| "Only one model" | Second model family | Maybe (GPU budget) | State as limitation |
| "Effect could be framing" | Additional neutral wording variant | Maybe | Add as ablation |

This table turns a rejection into a revision plan. **[L3]**

---

## 27. Research timeline

Ranges, not promises. Adjust for coursework, defense dates, and compute availability. **[L3]**

### Phase 0 — Orientation (3–7 days)

| Aspect | Detail |
|---|---|
| Objective | Know the area's arguments, vocabulary, and data landscape |
| Do | Read 10–15 abstracts/intros; build the one-page map (§11); collect vocabulary variants |
| Do not | Take detailed notes; read full papers; start writing a proposal |
| Move forward when | You can name the field's 3 main claims and its 2 main disagreements |
| Go backward when | You cannot find any disagreement or any data you could use |
| Output | One-page field map; 3 candidate territories |

### Phase 1 — Territory selection (1–2 weeks)

| Aspect | Detail |
|---|---|
| Objective | Choose ≤2 executable territories |
| Do | Score candidates (§5.3); check data/model/compute feasibility in 48 hours each |
| Do not | Explore a third territory, or extend a territory because it is comfortable |
| Forward | One territory scores clearly higher and yields a candidate phenomenon |
| Backward | All candidates blocked by data, annotation, or environment requirements |
| Output | Territory decision + parked list with one-line reasons |

### Phase 2 — Question formation (1–2 weeks)

| Aspect | Detail |
|---|---|
| Objective | Produce a question with two competing explanations and a discriminating observation |
| Do | Write the ladder (§7.1); write H₁/H₀ signatures; draft the design vector |
| Do not | Search for novelty by vocabulary; write long specifications |
| Forward | The four tests in §7.3 pass |
| Backward | You cannot name a discriminating observation |
| Output | Question Ledger entry with ranked candidates |

### Phase 3 — Adversarial verification (3–7 days)

| Aspect | Detail |
|---|---|
| Objective | Try to kill your own question |
| Do | Closest-work search (§12); gap verification (§13); attack list (§15.2) |
| Do not | Move to implementation to escape the discomfort of the search |
| Forward | Closest work differs in design; both outcomes informative |
| Backward | Matching manipulation+measurement found → next candidate or pivot |
| Output | Completed closest-work table + design-difference statement |

### Phase 4 — Feasibility and MDE (3–7 days)

| Aspect | Detail |
|---|---|
| Objective | Reduce the idea to a minimum discriminating experiment with an affordable compute line |
| Do | Compute the budget; write the failure interpretations; specify the control |
| Do not | Design the full thesis pipeline before the MDE is defined |
| Forward | Compute affordable; measure deterministic; control matchable |
| Backward | Any condition blocked by assets you do not have |
| Output | One-page experiment specification |

### Phase 5 — Pilot and instrument validation (1–2 weeks)

| Aspect | Detail |
|---|---|
| Objective | Validate the measurement before spending main-run compute |
| Do | 20–50 items; run the gates (§21.2); inspect outputs by hand |
| Do not | Interpret pilot results as findings; run the main experiment on an unvalidated instrument |
| Forward | All gates pass |
| Backward | Parse rate, truncation, or matching fails |
| Output | Gate table + revised prompts/budgets + classifier validation note |

### Phase 6 — Freeze and baseline (3–5 days)

| Aspect | Detail |
|---|---|
| Objective | Lock design and establish the trivial/strongest baselines |
| Do | Complete the freeze checklist; run baselines; archive raw outputs |
| Do not | Keep editing prompts; add arms for completeness |
| Forward | Baselines produce interpretable, non-degenerate behavior |
| Backward | Baseline cannot represent the behavior → narrow population |
| Output | `PROTOCOL.md`, `ANALYSIS_PLAN.md`, `BOUNDARY.md`, baseline numbers |

### Phase 7 — Main experiment (1–3 weeks)

| Aspect | Detail |
|---|---|
| Objective | Produce the decisive contrast at full population |
| Do | Checkpoint, resume, monitor diagnostics, archive everything |
| Do not | Tune mid-run; peek at hypotheses and adjust |
| Forward | Run completes with gates still passing |
| Backward | Systematic failure → stop, re-pilot |
| Output | Raw results, checkpoint, diagnostic summary |

### Phase 8 — Analysis, ablations, robustness (2–4 weeks)

| Aspect | Detail |
|---|---|
| Objective | Quantify, attribute, and stress-test the effect |
| Do | Primary analysis first; then strongest objection; then fragility checks |
| Do not | Fish for significant subgroups; report only the favorable split |
| Forward | Effect stable under diagnostics and at least one robustness check |
| Backward | Effect disappears under a fair robustness check → re-scope the claim |
| Output | Statistical report, tables, figures, Results Record |

### Phase 9 — Writing (4–8 weeks)

| Aspect | Detail |
|---|---|
| Objective | Produce a thesis whose claims match its evidence |
| Do | Write method and results first; keep limitations adjacent to results |
| Do not | Write introduction first; overclaim to make the story smoother |
| Forward | Each claim traced to a script and file |
| Backward | A claim cannot be traced → cut or weaken it |
| Output | Chapters, figures, tables, boundary statement |

### Phase 10 — Paper conversion (2–4 weeks after the thesis)

| Aspect | Detail |
|---|---|
| Objective | Extract one claim with the evidence needed to believe it |
| Do | Compress to one figure-led argument; add the strongest ablation |
| Do not | Submit the thesis; include every exploratory analysis |
| Output | Abstract, intro, method, results, limitations, reviewer-response plan |

**Schedule reality [L3]:** phases 2–5 are where projects die or become defensible, and they are the easiest to compress if you work with the two-day kill window (§16.5) and pilot gates. Phases 6–8 are the most predictable. If you are behind, cut *scope* (arms, datasets, models), never *controls* or *diagnostics* — cutting controls turns work into noise.

---

## 28. My personal failure modes and how to avoid them

Everything here is grounded in the retained corpus **[L2]** plus explicit recommendations **[L3]**.

### 28.1 Why topic discovery became so time-consuming

**Cause 1 — Feasibility was evaluated last, not first.** The parked fields (medical imaging/federated learning; cultural and Bangla VLM work; multimodal agents) were eliminated by constraints knowable on day one: no clinical data or domain labels; annotation-heavy cultural evaluation; multi-step environments with unbounded evaluation cost. Each instead received large literature audits, adversarial reports, and syntheses before the disqualifying constraint was applied. **[L2]**

**Cause 2 — Novelty was adjudicated by vocabulary and document volume.** Checks took the form "no paper uses this phrasing," rather than "the closest experiment has manipulation M, measurement X, population P; mine differs by D." Vocabulary searches cannot detect an occupied *design*; they detect occupied *sentences*. **[L2]**

**Cause 3 — Exploration and documentation were fused.** The corpus contains roughly 67 Markdown documents against 7 Python files. Exploration generated documents, documents created the sensation of progress, and that sensation removed the pressure to decide. The decisions actually made were few: a handful of fields parked, four candidates considered, one frozen. **[L2]**

**Cause 4 — Previously closed questions were re-opened.** The handover explicitly forbids re-opening parked fields, which indicates re-opening had been a recurring failure mode. Each re-open resets sunk cost and restarts reading. **[L2]**

**Cause 5 — The decision threshold was never written down.** No document defines the evidence required to continue, narrow, pivot, pilot, freeze, or kill. Without thresholds, doubt is resolved by reading more — which changes confidence, not evidence. **[L2/L3]**

### 28.2 Behaviors that caused unnecessary loops

| Behavior | Why it loops | Replacement |
|---|---|---|
| Breadth-first reading without a decision target | Each paper suggests three more | Read only papers that can change the next action (§8.2) |
| Treating AI summaries as evidence | Summaries compress away design detail — exactly what you need | Open primary text for the closest 4–8 papers (§10.5) |
| Canonical reports as the main work product | Reports can be rewritten forever | Decide inside the two-day kill window (§16.5) |
| Judging novelty by terminology | Terms differ; designs do not | Design-vector closest-work search (§12) |
| Broadening scope for novelty | Scope inflation makes experiments uninterpretable | Narrow to a construct fitting ≤6 arms |
| Checking feasibility after the literature audit | Wasted audits on unusable fields | 48-hour feasibility probe per territory (§17) |

### 28.3 Activities that produced real evidence

- The **20-item pre-freeze pilot**: falsified the metric, exposed the length mismatch, revealed abstention. Highest information per hour in the corpus. **[L2]**
- **Reading raw result files** (JSON/CSV) rather than summary reports: exposed truncation, token distributions, and the direct-arm text-following default (85.5%). **[L2]**
- **Hypotheses with signatures** (H₁/H₀ in the locked specification): made the design auditable. **[L2]**
- **Adversarial audits that changed the design** (notably introducing the placebo arm). **[L2]**
- **A reusable harness** with checkpointing and diagnostics, making re-runs cheap. **[L2]**

### 28.4 Activities that created the illusion of progress

- Long canonical specifications restating the same plan.
- Multiple "final" audits of the same candidates with the same evidence.
- Literature autopsies whose conclusions did not change the next action.
- Novelty claims from phrase searches and document enumeration.
- Counting files produced instead of decisions resolved.

**Test [L3]:** after any session ask "what decision changed?" If the answer is "my understanding deepened," ask "in a way that changes the next experiment?" If not, that session was reading for comfort, not research.

### 28.5 When broad exploration should have stopped

**[L2/L3]** Three stopping points were available and were passed:

1. **After the feasibility screen of the candidate fields.** Two were blocked by assets, not by literature. A two-day probe per field would have settled them.
2. **After the closest-work table for each surviving candidate.** Two were crowded or transfer-dependent; that was determinable by design comparison rather than by further reading.
3. **Immediately after the 20-item pilot.** The pilot produced a metric change, a design change, and a new question. That is the moment to stop exploring and start executing.

### 28.6 What should have been done earlier

- A written **continue/narrow/pivot/kill** rule set applied to every candidate (see §30).
- A **design vector** for each candidate, since design comparability settles novelty.
- A **20-item pilot** as the default first experiment, not the final validation step.
- A **feasibility one-pager** per candidate before writing any audit document.
- A **change log**, so question changes were appended rather than overwritten.

### 28.7 What to stop doing

1. Producing large reports to resolve uncertainty only evidence can resolve.
2. Equating keyword absence with novelty.
3. Exploring more than two territories at once.
4. Deferring feasibility.
5. Freezing on a calendar date instead of on gate results.
6. Treating a repeated conclusion in a restated document as confirmation.
7. Letting AI synthesis substitute for the closest 4–8 primary papers.

### 28.8 What must remain human

**[L3]** These cannot be delegated without losing the point of the research:

- Choosing what counts as an interesting phenomenon.
- Deciding which explanation is scientifically important.
- The final judgment on whether a control is fair.
- Interpretation and the boundary statement.
- The decision to kill, pivot, or freeze.
- Writing claims in your own voice, with your own conviction.

### 28.9 Where AI accelerates the work

- **Search-vocabulary expansion** across communities (synonyms for a construct).
- **Structured extraction** from papers you have already opened (claim/data/control/metric/limitation).
- **Design critique:** given your design vector, enumerate confounds and missing controls. One of the highest-value uses available.
- **Code scaffolding** for harnesses, parsing, checkpointing, and statistical reports.
- **Diagnostics review:** scanning raw outputs for degeneracy (repetition, refusals, truncation).
- **Draft support** for method and limitations prose grounded in your own artifacts.

### 28.10 Where AI creates false confidence or false novelty

- **"This gap appears unexplored."** Cannot be trusted: it depends on a qualitative search of designs that the model cannot inspect reliably.
- **Fabricated or misattributed citations.** Verify every reference against the primary source.
- **Confident summaries of papers it cannot fully read.** The design details that determine your novelty claim are exactly what compression removes.
- **Design flattery.** Asked "is my design good?", a model will explain why it is. Ask instead: "What is the strongest objection, and what result would falsify my claim?"
- **Metric acceptance.** A model will happily compute statistics on a metric that does not measure your construct; only manual inspection catches it. Your own pilot is the example **[L2]**.

**[L3] Rule:** use AI to generate *candidates and critiques*; use primary sources, manual inspection, and pilots to *decide*.

### 28.11 The one-line summary of your history **[L2]**

> The research judgment was sound; the *sequencing* was inverted — feasibility was checked after exploration instead of during it, novelty was checked by vocabulary instead of by design, and freezing happened by calendar instead of by gate.

Fix the sequencing and the same judgment produces results in a fraction of the time.

---

## 29. Reusable research workspace

Seven artifacts. Not thirty. Each has a job, a moment of creation, and a moment when it can be discarded. **[L3]**

### 29.1 Research Map

- **Purpose:** current understanding of the territory — claims, measures, disagreements, unknowns, available assets (ten slots in §11.2).
- **Created:** day 1 of a territory.
- **Updated:** whenever a search changes the map, and always before freezing (frontier date).
- **Contains:** one page, `?` for uncertain entries, ranked candidate questions with kill reasons.
- **Discard:** when the territory is parked or the project is published; keep it as an appendix note.

### 29.2 Question Ledger

- **Purpose:** every candidate question and its status, so decisions are not re-litigated.
- **Created:** as soon as a first candidate exists.
- **Updated:** every time a candidate is killed, narrowed, or promoted.
- **Contains:** per row — candidate (one line), design vector, closest work, kill reason, reopen condition, date.
- **Discard:** never; it doubles as your thesis's "open problems" section.

```text
| Candidate | Design vector (M/M/P) | Closest work | Status | Kill reason / next step | Reopen if | Date |
```

### 29.3 Evidence Ledger

- **Purpose:** what you believe and why, traceable to a primary source or your own result.
- **Created:** with the first serious reading.
- **Updated:** with every claim you intend to use.
- **Contains:** claim | source (paper DOI/arXiv ID, or own run ID) | evidence (number/figure/table) | control present? | limitation | date verified.
- **Discard:** never; it writes your related-work section.

### 29.4 Experiment Specification

- **Purpose:** the frozen design; the contract with your future self.
- **Created:** at freeze (§24).
- **Updated:** only through a documented re-open (§24.4).
- **Contains:** hypotheses with signatures, arms, prompts verbatim, budgets, control matching tolerance, dataset/split/exclusions, metric and parsing rules, seeds, model revision, analysis plan, failure interpretations.
- **Discard:** never during the project.

### 29.5 Research Log

- **Purpose:** chronological decisions, dead ends, bugs, surprises.
- **Created:** day 1; append-only.
- **Updated:** every working session (5 lines is enough).
- **Contains:** date | what I tried | what happened | decision | what I would do differently.
- **Discard:** never (it is your defense preparation material).

### 29.6 Results and Analysis Record

- **Purpose:** all numbers and their interpretation, including diagnostics and robustness.
- **Created:** as the first real run finishes.
- **Updated:** with each run, analysis, and robustness check.
- **Contains:** table of all results (including failures and discarded runs), effect sizes with CIs, diagnostics, what each result rules out, and versioned artifact paths.
- **Discard:** never; this is Table 1 of the paper.

### 29.7 Paper Story

- **Purpose:** the single claim and the evidence chain that supports it.
- **Created:** when analysis stabilizes.
- **Updated:** during compression from thesis to paper.
- **Contains:** one-sentence claim | closest work and design difference | claim-supporting figures in order | rebuttals to the three strongest objections | boundary statement.
- **Discard:** never; it is the abstract's skeleton.

### 29.8 Minimal file layout

```text
research/
  map.md
  question_ledger.md
  evidence_ledger.md
  research_log.md
  results_record.md
  paper_story.md
  experiment_specification.md
```

Seven files, each updatable in minutes. That is the whole system. **[L3]**

### 29.9 What *not* to build

- A large citation database with hundreds of entries and no decisions attached.
- Multiple "canonical," "final," or "master" documents restating the same content.
- Templates for phases you have not reached.
- Dashboards and trackers that must be maintained instead of used.

**Evidence from your corpus [L2]:** the cost of over-documentation is visible — the ratio of synthesis documents to executed experiments was extremely high, and the document set had to be re-summarized repeatedly by different tools. The seven-artifact system above would have carried all the information that mattered with roughly an order of magnitude less text.

---

## 30. Stop / Continue / Pivot / Kill framework

### 30.1 The six decisions and the evidence each requires

| Decision | Meaning | Evidence required | Typical next artifact |
|---|---|---|---|
| **CONTINUE** | The question is strengthening; keep working the current line | New evidence from the literature or a pilot *increases* discrimination between explanations | Updated map + next pilot |
| **NARROW** | Promising but too broad | You cannot state the population/condition in one sentence, or too many arms are needed | Reduced design vector |
| **PIVOT** | The evidence changed the scientific question | A measurement discovery, a confound, or an occupied sub-question changes what can be claimed | Change-control entry (§23.4) |
| **PILOT** | The question is strong enough to test at small scale | Four tests of §7.3 pass; data and model available; 20–50 item plan written | Pilot run + gate table |
| **FREEZE** | Design is stable enough for the main run | Every box of the §24.2 checklist is ticked, including gate numbers | `PROTOCOL.md`, `ANALYSIS_PLAN.md` |
| **KILL** | The question cannot produce useful knowledge now | Closest work matches manipulation+measurement; or no deterministic measure; or no discriminating experiment; or a null result teaches nothing | Five-line kill note (§16.6) |

### 30.2 The questions that trigger each decision

**CONTINUE if:**
- the newest search/experiment gave you a *stronger* control or a *sharper* contrast;
- the effect survives an additional rival explanation;
- you can name the next experiment without hesitation.

**NARROW if:**
- the design needs more than ~6 arms;
- the claim requires more than one model family, language, or domain to be interesting;
- your boundary statement keeps growing.

**PIVOT if:**
- the outcome measure turned out to measure something else (as in the exact-match → engaged-problem change) **[L2]**;
- the dominant effect is a confound (prompt framing), making the confound the finding;
- a concurrent publication occupies the sub-question but leaves an adjacent one open.

**PILOT if:**
- you can describe the discriminating observation in one sentence;
- a deterministic or validated measure exists;
- a 20-item version fits in one GPU-hour.

**FREEZE if:**
- gates passed with numbers on record;
- prompts and budgets are frozen verbatim;
- the analysis plan is written;
- failure interpretations exist for every outcome.

**KILL if:**
- the closest-work table shows a matching manipulation *and* measurement;
- the measure cannot be made deterministic or validated within your window;
- the experiment would need assets you cannot obtain (clinical data, annotation at scale, multi-step environments) **[L2 on parked fields]**;
- the honest "what we would learn" sentence is boring;
- answering the strongest objection requires more compute than exists.

### 30.3 Thresholds, so the decision is not a mood

**[L3]** Write these into the Question Ledger and apply mechanically:

```text
CONTINUE  if  ≥1 new design-relevant fact appeared in the last 5 working days
NARROW    if  design arms > 6  OR  scope sentence needs the word "and"
PIVOT     if  a measurement audit contradicts the construct  OR  a confound dominates
PILOT     if  4/4 tests in §7.3 pass  AND  compute ≤ 1 GPU-hour for 20 items
FREEZE    if  11/11 freeze checklist items pass with recorded numbers
KILL      if  closest-work match found  OR  no deterministic measure in ≤2 days of work
              OR  required asset unavailable  OR  null result uninformative
```

### 30.4 Decision review cadence

- **Daily (5 minutes):** append to the Research Log; note the decision state.
- **Weekly (30 minutes):** re-evaluate every open candidate against §30.3; update the Question Ledger.
- **At each gate (pilot, freeze):** paste numbers into `PROTOCOL.md`; the gate decides, not the calendar.

### 30.5 Applied to your current project **[L2]**

| Candidate | Decision today | Reason |
|---|---|---|
| Conflict verbalization → engaged-source shift, N=1,619 | **CONTINUE (execution)** | Frozen; main run complete; analysis and writing are the work |
| Abstention as conflict-specific vs instruction-induced (Ladder B) | **PILOT** | High value, cheap (one added neutral-uncertainty arm), directly supported by 13.7% vs 0.2% |
| Chart/domain transfer of the effect | **PILOT LATER** | Same harness; parsing work only |
| Attention/representation mechanism | **KILL (for now)** | Instrumentation validity unclear; needs a design you do not have |
| Per-item length-matching verification | **FREEZE-SUPPORT ACTION** | Needed to defend the placebo control; report token distributions per arm |
| Classifier manual-validation audit | **FREEZE-SUPPORT ACTION** | Needed to defend the engaged-problem measure; 50 sampled outputs, report agreement |
| Parked fields (imaging/FL, cultural VLM, agents) | **KILL (documented)** | Asset-blocked; reopen conditions recorded |

Two of these are *not* research work but **defensive evidence work**, and they are the highest-value hours you can spend before submission: they convert your two most attackable aspects (control matching and classifier validity) into reported diagnostics. **[L2/L3]**

### 30.6 The eight-factor intersection before freezing **[L3]**

Never optimize for a single factor. Score each candidate question 1–5 on eight dimensions and require *no zeros*:

| Factor | Question to ask | Why it matters |
|---|---|---|
| Scientific importance | If answered, what claim in the field changes? | Prevents trivial work |
| Novelty | Does the closest experiment differ in design? | Prevents duplication |
| Evidence feasibility | Can I produce decisive evidence with my assets? | Prevents beautiful untestable questions |
| Clarity | One sentence, no hedging? | Prerequisite for a clean experiment |
| Reproducibility | Deterministic measure, public data, pinned configs? | Protects the claim and your defense |
| Contribution size | Thesis-sized, not career-sized? | Prevents incomplete work |
| Risk of occupancy | Could someone publish this in the next 6 months? | Determines urgency |
| Time fit | Does the full pipeline fit the remaining weeks? | Determines survival |

**The intersection rule.** A question is freeze-worthy when all eight are at least 3, at least four are ≥4, and the *lowest* two factors have written mitigations. Example: if "risk of occupancy" is 2, mitigate by publishing a preprint or narrowing the claim; if "time fit" is 2, cut scope, not controls.

**Two failure shapes to name explicitly:**

- **Novel but untestable** (novelty 5, evidence 1): an interesting theory paper you cannot run. Convert it into a smaller question, or park it with a reopen condition.
- **Easy but trivial** (evidence 5, importance 1): a clean experiment nobody needs. Reattach it to a claim people rely on, or drop it.

Most students drift toward one of these two shapes. The intersection table makes the drift visible in ninety seconds.

---

## 31. One-page daily research playbook

### 31.1 The discovery loop, with the question to ask at each node

```text
EXPLORE
   │  "Which two or three territories are executable with the assets I have?"
   ▼
NOTICE A PHENOMENON
   │  "Can I state it without my method? Where did I see it, and how much?"
   ▼
TRACE THE LITERATURE
   │  "Who named this? What do they claim causes it?"
   ▼
UNDERSTAND THE EXPLANATIONS
   │  "What alternatives produce the same observation?"
   ▼
SEARCH FOR ALTERNATIVES AND CONFOUNDS
   │  "Has anyone tested this with a matched control?"
   ▼
TEST NOVELTY BY DESIGN
   │  "What is the closest manipulation+measurement triple?"
   ▼
ESTIMATE FEASIBILITY
   │  "Data? Model? Deterministic measure? GPU-hours? Days to implement?"
   ▼
FORMULATE COMPETING QUESTIONS
   │  "What is the one-sentence discriminating observation?"
   ▼
DESIGN THE MINIMUM EXPERIMENT
   │  "Can I test this on 20 items in one GPU-hour?"
   ▼
ATTACK IT
   │  "What is the strongest objection, and what result would falsify my claim?"
   ▼
DECIDE
   └→ CONTINUE / NARROW / PIVOT / PILOT / FREEZE / KILL   (§30)
      then loop again — with each cycle costing hours, not weeks
```

**Target cycle time:** one full loop in **2 working days**. If a loop is taking longer, the blocker is almost always an unwritten decision rule or an unrun pilot, not insufficient reading. **[L3]**

### 31.2 The daily structure

| Block | Duration | Activity | Output |
|---|---|---|---|
| 1 | 15 min | Review question ledger; pick today's single decision | Written decision target |
| 2 | 90 min | The work that changes the decision (search, design, code, pilot) | Something concrete |
| 3 | 90 min | Continue the same target (no context switching) | Progress |
| 4 | 30 min | Record: log entry, evidence ledger, ledger updates | Files updated |
| 5 | 15 min | Ask "what decision changed?" and set tomorrow's target | Next target |

**Rules:** one decision target per day; no opening a new territory mid-week; every day ends with the Research Log updated.

### 31.3 Daily self-check (5 questions, 2 minutes)

1. What did I learn that changes my next action?
2. Did I verify anything against a primary source today?
3. Is my measurement still measuring my construct?
4. What is currently the weakest part of my claim?
5. Am I avoiding a decision by reading or writing more?

### 31.4 Weekly review (30 minutes)

- Update the Research Map frontier date; run one "recent work" search (§9.1, #10).
- Re-score every open candidate with §30.3 thresholds.
- Close or park anything that has not moved in two weeks.
- Confirm the next seven days' decision targets.

### 31.5 Printable loop card

```text
PHENOMENON:   ________________________________________
CLAIMED CAUSE:________________________________________
RIVAL CAUSES: ________________________________________
CLOSEST WORK: ____ / manipulation ____ / measure ____
MY DESIGN DIFF:_______________________________________
DISCRIMINATING OBSERVATION: __________________________
CONTROL (matched how?): ______________________________
MEASURE (deterministic? validated?): _________________
GPU-HOURS: ____   ITEMS: ____   ARMS: ____
IF NULL → WE LEARN: __________________________________
STRONGEST OBJECTION: _________________________________
DECISION: CONTINUE / NARROW / PIVOT / PILOT / FREEZE / KILL
```

---

## 32. If I start a new research area tomorrow

A concrete eleven-day walkthrough. It assumes almost no prior knowledge, one 16 GB GPU, public data, and no advisor available for the first week. **[L3]**

### Day 1 — Orientation, not depth (4 hours)

- Search the area name plus `survey` and `position paper`; take the two most recent.
- Read only abstracts, figures, and conclusions. Do not take detailed notes.
- Write the Research Map skeleton: claims, measures, disagreements, unknowns, assets.
- Collect vocabulary variants as you go (slot 10).
- **Output:** one-page map with many `?` marks.

### Day 2 — Find the fault lines (4 hours)

- For each of the three main claims you found, write what the claim is based on and whether its control exists.
- Search explicitly for disagreement: `re-examining`, `limitations`, `does not hold`, `critique`, `under matched`.
- List the area's benchmarks, datasets, and models in the map.
- **Output:** map with competing directions and known failure modes; three candidate phenomena.

### Day 3 — Pick two territories, run a 48-hour feasibility probe

For each candidate: is there public data, an inspectable label, a ≤3B model that can express the behavior, and a deterministic measure? Write the one-page feasibility card (§17.1).

### Day 4 — Finish feasibility and kill one

- Compute the budget line honestly (§17.3).
- Apply §16.2 kill checklist.
- Park one candidate in writing with a reopen condition; promote one.
- **Output:** Question Ledger with one survivor and one documented park.

### Day 5 — Write the ladder for the survivor

- Write Area → Territory → Phenomenon → Observation → Existing claim → Alternatives → Gap → Question → Hypotheses → Experiment → Contribution (§7.1).
- Write the H₁/H₀ signatures.
- If any row is empty, today's work is to fill it — not to read more.
- **Output:** first draft of the Question Ledger entry.

### Day 6 — Closest work by design

- Decompose your design vector (§12.2).
- Run searches 1–10 from §9.2 using design terms.
- Complete the closest-work table and the two-sentence design-difference statement (§12.4).
- **Output:** novelty verdict: REAL / UNCLEAR / OCCUPIED (§13.2).

### Day 7 — Gap verification and adversarial attack

- Complete §13.4 worksheet, including the "if positive/if negative the field learns" lines.
- Run the §15.2 attack list. Write the strongest objection and your answer.
- **Output:** verdict and a mitigation list, or a kill note.

### Day 8 — Minimum discriminating experiment

- Reduce to the smallest procedure that separates the explanations (§18).
- Fix arms (≤6), budgets, control-matching tolerance, and metric.
- Write failure interpretations for every outcome.
- **Output:** one-page Experiment Specification draft; compute estimate.

### Day 9 — Build the smallest honest instrument

- Write the harness for 20 items only: prompts verbatim, structured output, token logging, truncation flags, raw output storage.
- Include a checkpoint so the pilot is resumable.
- **Output:** ~150–250 lines of code (your existing harness is a template).

### Day 10 — Run the pilot and inspect by hand

- Run 20 items across all arms.
- Read every output. Count parse rate, truncation, degenerate outputs, and whether the arms differ visibly.
- Apply the gates (§21.2).
- **Output:** gate table. If a gate fails, fix and re-run tomorrow.

### Day 11 — Decide, then scale or stop

- If the effect is observable and gates pass → freeze the design, expand to the main population.
- If the effect is not observable at 20 items → check instrument, then consider whether the effect is too small at your scale; re-scope or kill.
- **Output:** a frozen protocol with gate numbers, or a five-line kill note with a reopen condition.

### If you only have three weeks

Compress to:

```text
Days 1–2   orientation + map + feasibility (two territories)
Days 3–4   closest work + gap verification + attack
Day 5      experiment specification
Days 6–7   instrument + pilot + gates
Days 8–12  main run (inference-only, checkpointed)
Days 13–17 analysis + diagnostics + robustness
Days 18–21 write the thesis chapters that carry the claim
```

Note what is *not* compressed: controls, diagnostics, and the closest-work check. Scope shrinks first; rigor shrinks never. **[L3]**

### The three sentences to remember

1. **A phenomenon is not a question until two explanations predict different observations.**
2. **A gap is not a gap until you have compared designs, not words.**
3. **A design is not a design until the control is matched, the measure is validated, and the failure interpretation is written.**

---

# Appendix A: primary sources used

Every external claim in this playbook that concerns a specific paper is anchored below. All were opened at their primary arXiv record during preparation of this document (24 September 2026). Claims about general research practice that are not tied to one of these sources are labeled synthesis/recommendation **[L3]**.

| # | Source (primary record) | Used in this playbook for |
|---|---|---|
| 1 | Turpin, Michael, Perez, Bowman. *Language Models Don't Always Say What They Think: Unfaithful Explanations in Chain-of-Thought Prompting.* [arXiv:2305.04388](https://arxiv.org/abs/2305.04388) (NeurIPS 2023) | Illustrating unfaithful rationalization under input biasing in **text** models; the shape of the faithfulness question; its multimodal transfer as an open design gap (§12.5, §7.7) |
| 2 | Popordanoska, Li, Blaschko. *CLASH: A Benchmark for Cross-Modal Contradiction Detection.* [arXiv:2511.19199](https://arxiv.org/abs/2511.19199) | Example of a contradiction **detection** benchmark (controlled object/attribute contradictions, MCQ and open-ended, fine-tuning gains, reported modality biases); used to show why detection ≠ arbitration (§5.4, §6.3, §7.6, §12.5) |
| 3 | Liu et al. *More Thinking, Less Seeing? Assessing Amplified Hallucination in Multimodal Reasoning Models.* [arXiv:2505.21523](https://arxiv.org/abs/2505.21523) | Example of a behavioral phenomenon (longer chains ↔ reduced visual grounding) with RH-AUC/RH-Bench as a length–perception metric, plus attention analysis as a proposed mechanism (§5.4, §12.5) |
| 4 | Hasani et al. *Uncovering Grounding IDs: How External Cues Shape Multimodal Binding.* [arXiv:2509.24072](https://arxiv.org/abs/2509.24072) | Example of a mechanism claim supported by representation analysis plus causal intervention; used to distinguish binding from arbitration and to illustrate how mechanism claims are argued (§12.5, §4.2) |
| 5 | Traub et al. *Overcoming Common Flaws in the Evaluation of Selective Classification Systems.* [arXiv:2407.01032](https://arxiv.org/abs/2407.01032) | Replaces a widely used metric (AURC) with AUGRC because current metrics fail stated requirements, changing rankings on 5 of 6 datasets — the model case for **measurement-validity** contributions (§20.3, §22.3) |
| 6 | Schaeffer, Miranda, Koyejo. *Are Emergent Abilities of Large Language Models a Mirage?* [arXiv:2304.15004](https://arxiv.org/abs/2304.15004) | The canonical example of a "phenomenon" that depends on metric choice (discontinuous vs continuous), tested on published outputs — the model for a cheap, decisive metric audit (§5.4, §18.3, §22.3) |
| 7 | Gebru et al. *Datasheets for Datasets.* [arXiv:1803.09010](https://arxiv.org/abs/1803.09010) | Standard for documenting dataset motivation, composition, collection, preprocessing, uses, distribution, and maintenance; used for data-provenance discipline (§9.3, §17.1) |
| 8 | Henderson et al. *Deep Reinforcement Learning that Matters.* [arXiv:1709.06560](https://arxiv.org/abs/1709.06560) | Evidence that variance and reporting practice make results hard to interpret, with recommendations for significance metrics and tighter experimental reporting (§20.5, §25.4) |
| 9 | Pineau et al. *Improving Reproducibility in Machine Learning Research (NeurIPS 2019 Reproducibility Program).* [arXiv:2003.12206](https://arxiv.org/abs/2003.12206) | Code-submission policy, reproducibility challenge, and ML reproducibility checklist: the basis for `PROTOCOL.md`, pinned revisions, seeds, and archived raw outputs (§19.6, §24.5, §25.4) |

### A.1 Citation that could not be verified

The workspace's locked specification cites **`arXiv:2608.17205`, "Which Source Wins?"**, as reporting modality dominance under legibility degradation. I could not verify this identifier against a primary record during preparation, so it is marked **[Unknown]** in this playbook. **Action [L3]:** open the paper directly and record its manipulation, measurement, and population in the Evidence Ledger before relying on the claim. If it cannot be found, remove the citation and rebuild the "anchor literature" paragraph from verified sources. This is the single most consequential verification task remaining in the current project.

### A.2 Evidence standard applied

- Primary records (arXiv listings with version history, official proceedings) were used for every paper-specific statement above.
- No paper, author, dataset, or repository in this playbook was invented; where a claim could not be traced, it was labeled **[Unknown]** or omitted.
- Statements about your own project come from the retained files listed in Appendix B, not from memory or summary.
- General methodological advice that is not attributable to a specific source is labeled **[L3]** synthesis.

---

# Appendix B: reconstructed case-study chronology from this workspace

## B.1 What the corpus contains

Approximately **68 Markdown documents** and **7 Python files**, plus raw results (JSON, CSV), LaTeX tables, a notebook, and two PDFs — spread across `Context/`, `Finalize Topic/`, `VLM/`, `Bengali VLM/`, `Multimodal Agent/`, `Medical Imaging & FL/`, and `Extra Field Exploration/`. There is **no Git history**, so ordering below is reconstructed from content, cross-references, filenames, and experiment provenance **[L2]**.

## B.2 Reconstructed sequence

| Stage | Evidence in the corpus | What it demonstrates |
|---|---|---|
| 1. Broad area orientation | `Extra Field Exploration/Plan.md`, `phase-1---landscape-map---antithesis-scan-turn-1.md`, `VLM Landscape and Adversarial Antithesis Scan.md`, `VLM MLLM Antithesis Scan.md` | Orientation was genuinely broad: multiple subfields scanned and mapped |
| 2. Candidate-field audits | `Medical Imaging & FL/*` (6 docs), `Multimodal Agent/*` (4 docs), `Bengali VLM/*` (10 docs) | Each field received a large audit before a feasibility verdict |
| 3. Consolidation into canonical candidates | `Finalize Topic/Canonical_Proposal_1_Reasoning_Trace_Degradation.md`, `..._2_Binding_IDs_Natural_Transfer.md`, `..._3_Cultural_*` (two variants), plus `Clean Explanation (All 4 Idea).md` | Four candidates were developed in parallel to proposal depth |
| 4. Adversarial audits and decisions | `Final Four-Proposal Thesis Decision Audit.md`, `final_adversarial_thesis_decision_audit.md`, `Extra/FINAL THESIS DECISION AUDIT.md`, `Structural Taxonomy Mind Map...` | Decision documents existed, but were produced after large audits |
| 5. Locked specification | `Canonical_Thesis_Topic_Specification (Locked).md` (four arms; H₁ deliberative control vs H₀ post-hoc rationalization; threats-to-validity table) | The final question had a genuine competing-hypothesis structure — a real methodological step forward |
| 6. Pre-freeze pilot | `Pilot/prefreeze_pilot.py`, `prefreeze_pilot_v2.py`, `pilot_diagnostic_analysis.md` (2026-09-23, 20 items) | The single highest-value artifact: falsified the metric, found the length mismatch, discovered abstention |
| 7. Production runs | `production_experiment_harness.py` (+`_v3`), `Experiment_Result/experiment_results_analysis.md` (N=500), `statistical_report v2.0/v3.0.md`, `full_experiment_results*.json`, checkpoint CSVs, LaTeX table | Truncation failure at N=500 discovered and diagnosed; budgets raised (80/200/20) in v3; full population N=1,619 executed |
| 8. Post-freeze handover | `Thesis_Topic_Discovery_Handover.md` (2026-09-24) | Declares discovery closed; freezes the topic; begins writing schedule |

## B.3 Verified numbers used in this playbook

| Quantity | Value | Source |
|---|---|---|
| Population | N = 1,619 clean image pairs | `statistical_report v3.0.md`, `Thesis_Topic_Discovery_Handover.md` |
| Arm 2 (neutral placebo) visual following | 89.5% (1,449/1,619) | same |
| Arm 3 (conflict verbalization) visual following | 25.8% (417/1,619) | same |
| **Net shift** | **+63.7 pp** reduction; OR = 24.57 (95% CI 20.24–29.83); Cohen's h = 1.42; McNemar χ² = 982.40, p ≈ 1.2e-215 | same |
| Arm 1 (direct) source following | **text 85.5% (1,385), image 13.8% (223)** | `Thesis_Topic_Discovery_Handover.md` contingency table |
| Abstention, Arm 3 | 13.7% (221) vs 0.2% Arm 2, 0.0% Arm 1 | same |
| Prefill probe agreement | 41.4% divergence between opposing prefixes; +5.3 pp text alignment one direction | `statistical_report v3.0.md` §4 |
| Pilot metric failure | 85% of direct-arm outputs matched neither precomputed answer | `pilot_diagnostic_analysis.md` Finding 1 |
| Pilot length mismatch | Placebo 61.2 tokens vs direct 3.4 tokens | `pilot_diagnostic_analysis.md` Finding 3 |
| N = 500 truncation | Arm 1 100% at 15-token ceiling; Arms 2/3 90.4%/98.2% at 90 tokens | `experiment_results_analysis.md` §3 |

## B.4 Case studies extracted (phenomenon → literature → alternative → missing control → causal question → experiment)

1. **Metric–construct mismatch.** Exact-match selection did not measure source arbitration because the model computed new answers. *General behavior:* validate the metric against manual inspection before the main run. **[L2]**
2. **Unmatched control discovered late.** The neutral arm differed by ~18× in tokens. *General behavior:* check per-item matching numerically, not nominally. **[L2]**
3. **Prompt framing dominates the headline phenomenon.** Direct arm follows text (85.5%); neutral prompt follows image (89.5%). *General behavior:* always run a baseline under more than one neutral framing before naming a modality preference. **[L2]**
4. **Freeze by calendar.** Pilot on 2026-09-23 ended with "only THEN freeze"; handover on 2026-09-24 locked the topic. *General behavior:* freeze on recorded gate numbers. **[L2]**
5. **Novelty by vocabulary and document volume.** Many canonical restatements; novelty argued in prose. *General behavior:* novelty is a design comparison. **[L2]**
6. **Feasibility evaluated after exploration.** Three fields were parked for asset reasons after large audits. *General behavior:* 48-hour feasibility probe per territory. **[L2]**

## B.5 Limits of this reconstruction

- No commit history, so chronology is inferred; two documents may have been written in the opposite order from that suggested here.
- The conversation history is incomplete; statements about earlier sessions are inferences from artifacts.
- Retrospective summary documents were treated as claims; where a claim conflicted with raw results, the raw results were used.
- The playbook deliberately does not re-litigate which thesis topic was "best." Its purpose is to extract reusable process behavior.

---

# Appendix C: printable cards

## C.1 The five questions (keep visible while working)

1. What exactly did I observe, and could my measurement have produced it?
2. What mechanism do the closest papers claim?
3. What alternative explanation would produce the same observation?
4. What result would separate the alternatives?
5. What would we know afterwards that we do not know now?

## C.2 One-hour kill checklist

```text
[ ] Phenomenon statable without my method
[ ] Comparison statable in one sentence
[ ] At least two explanations named
[ ] Matched control exists (and I must exceed it)
[ ] Data + model + compute available today
[ ] Deterministic or validated measure
[ ] Null result would be informative
[ ] 20-item pilot feasible this week
[ ] Closest experiment differs in DESIGN, not wording
[ ] I can state what the field believes before and after

8–10 yes → pilot      5–7 → narrow/repair      0–4 → kill now, in writing
```

## C.3 Freeze checklist

```text
[ ] Question: one sentence, names the comparison
[ ] H1 and H0 with written signatures
[ ] Primary metric: operational, deterministic/validated by hand
[ ] Controls: per-item matched, tolerance written
[ ] Population: model revision, split, N, exclusions fixed
[ ] Pilot gates passed with numbers recorded
[ ] Analysis plan written (test, unit, thresholds, exploratory labeled)
[ ] Compute estimate affordable
[ ] Boundary statement written
[ ] Closest-work table complete and date-stamped
[ ] Failure interpretations written for every outcome
```

## C.4 Metric-validity card

```text
CONSTRUCT:      what it is supposed to measure
OPERATION:      exactly what is counted
CONFLATION:     what else could move it
VALIDATION:     manual agreement on N=___ outputs = ___%
INSENSITIVE TO: the confound I claim to control
REPORTED AS:    distribution + uncertainty, not just a mean
```

## C.5 Closest-work card

```text
CLOSEST PAPER:        ______________________________
ITS MANIPULATION:     ______________________________
ITS MEASUREMENT:      ______________________________
ITS POPULATION:       ______________________________
ITS CONTROL:          ______________________________
MY DESIGN DIFFERENCE: ______________________________
WHY IT MATTERS:       ______________________________
SEARCH DATE:          ______   FILES/QUERIES REVIEWED: ______
VERDICT:              REAL / UNCLEAR / OCCUPIED
```

## C.6 Decision card

```text
CONTINUE  evidence strengthened the question
NARROW    too broad: >6 arms or scope needs "and"
PIVOT     measurement discovery or dominant confound
PILOT     4/4 question tests pass; ≤1 GPU-hour for 20 items
FREEZE    11/11 freeze items pass with recorded numbers
KILL      closest-work match / no deterministic measure / asset-blocked / null uninformative
```

## C.7 The three sentences

1. A phenomenon is not a question until two explanations predict different observations.
2. A gap is not a gap until you have compared designs, not words.
3. A design is not a design until the control is matched, the measure is validated, and the failure interpretation is written.

---

*End of playbook.*
