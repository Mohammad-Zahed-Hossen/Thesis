# AI/ML Research Playbook: From Research Discovery to Publishable Paper

**A practical research operating manual reconstructed from primary research practice and from one researcher's documented thesis journey**

| Field | Value |
| :--- | :--- |
| **Prepared for** | Mohammad Zahed Hossen — Final-year BSc CSE, Technical Lead (3-person thesis team), Bangladesh |
| **Prepared on** | 24 September 2026 |
| **Evidence base** | (a) 87 files / ~1.5 MB of the researcher's own discovery, audit, pre-registration, pilot, harness and results artifacts; (b) primary-source verification of the seven anchor papers appearing in those artifacts, performed during this reconstruction |
| **Purpose** | Not a thesis proposal. A reusable *operating manual* for how to think and work when doing serious AI/ML research |
| **Scope warning** | This manual deliberately does **not** propose, re-open, or re-rank thesis topics. Where it discusses your frozen topic it does so only as a *case study* of process |

---

## How to read this document

### The three knowledge levels used throughout

Every claim in this manual is tagged so you can tell established practice apart from my inference about you, and apart from my advice.

| Tag | Meaning | How to treat it |
| :--- | :--- | :--- |
| **[L1 — Established practice]** | What experienced researchers commonly do. Drawn from general research methodology and from how the primary literature I verified is actually written. | Trust as background, but adapt to your constraints. |
| **[L2 — Inferred from your record]** | A pattern I observed *in your documents* and inferred from them. Your files are evidence of behaviour, not ground truth. | Test it against your memory. Some inferences will be wrong. |
| **[L3 — Recommendation for your workflow]** | My synthesis of how *you specifically* should work, given your hardware, supervision, team, and time constraints. | Adopt or discard. It is advice, not fact. |

### The two evidence standards used for paper claims

| Tag | Meaning |
| :--- | :--- |
| **[PRIMARY — verified]** | I fetched the arXiv abstract page myself during this reconstruction and am quoting its metadata or abstract directly. |
| **[SYNTHESIS]** | A methodological claim that cannot reasonably be tied to a primary source. It is reasoning, not established fact. |
| **[UNVERIFIED — from your records]** | A claim that appears in your documents, which I did **not** independently verify. Treat as a lead requiring a click. |

### The single most important instruction in this document

> **Every arXiv ID, dataset name, benchmark name, author name, and venue in your own canonical documents is an unverified claim until you have opened its primary page and read the metadata with your own eyes. This manual contains a demonstration of exactly how that failure happens to a careful researcher.**

---

## Table of Contents

1. Executive Overview
2. How Experienced Researchers Actually Work
3. Why Research Is Not Linear
4. The Researcher's Mental Model
5. Finding Research Territories
6. Finding Phenomena and Failures
7. Turning Observations into Research Questions
8. Literature Exploration Strategy
9. How to Search Like a Researcher
10. How to Read and Interrogate Papers
11. Building a Field Map
12. Finding the Closest Existing Work
13. Verifying Whether a Gap Is Real
14. Competing Explanations and Hypotheses
15. Adversarial Idea Testing
16. Fast Idea-Killing
17. Feasibility During Discovery
18. Designing the Minimum Discriminating Experiment
19. From Research Question to Experimental System
20. Baselines, Controls, Metrics and Evaluation
21. Pilot → Main Experiment
22. Handling Unexpected and Negative Results
23. Iterating and Changing the Research Question
24. Freezing the Research Question
25. End-to-End Thesis Execution
26. From Thesis to Paper
27. Research Timeline
28. My Personal Failure Modes and How to Avoid Them
29. Reusable Research Workspace
30. Stop / Continue / Pivot / Kill Framework
31. One-Page Daily Research Playbook
32. Final "If I Start a New Research Area Tomorrow" Guide

Appendix A — Verified anchor-paper ledger for your current project
Appendix B — Evidence-integrity audit of your canonical documents

---

# 1. Executive Overview

## 1.1 What this manual is

This is the document a strong PhD student hands a first-year student and says: *"Read this before you waste six months. Here is how the work actually goes."*

It is written in the belief that **research skill is mostly a set of questions you learn to ask yourself at the right moment.** Senior researchers are not smarter in the abstract; they are faster at asking four specific questions:

1. *What is the smallest observation that would be surprising here?*
2. *What is the closest thing anyone has already done to it?*
3. *What would I have to see to conclude I was wrong?*
4. *Can I get that evidence on my current hardware, this week?*

Everything else — the searching, the reading, the experiments, the writing — is downstream of those four questions being asked early and asked hard. **[L1 — Established practice / SYNTHESIS]**

## 1.2 The five things this manual claims

These are the load-bearing claims. If you disagree with one, the rest of the manual changes shape, so it is worth arguing with them explicitly.

| # | Claim | Consequence for how you work |
| :--- | :--- | :--- |
| **C1** | **Research questions are found, not invented.** Strong questions come from anomalies in existing evidence, not from brainstorming new systems. | Stop generating ideas. Start collecting anomalies. Your "ideation" output should be *observations*, not *proposals*. |
| **C2** | **A gap is a statement about an unperformed experiment, not an unspoken sentence.** Nobody has written your exact sentence; that means nothing. Nobody has run your exact contrast; that is the only thing that matters. | Rewrite every candidate gap as: "The closest prior work ran experiment X under condition A; I would run X under condition B, and the outcome changes conclusion C." |
| **C3** | **The most valuable early work is destructive.** The purpose of the first two weeks of a research project is to kill as many of your own ideas as quickly and cheaply as possible. | Judge your discovery phase by *how many candidates you eliminated*, not by how many you generated. |
| **C4** | **Novelty is a property of the closest-work comparison, not of your idea.** You cannot know whether something is novel by thinking about it. You can only know by reading one specific paper carefully. | Every candidate question must have exactly one named "closest work" before it is allowed to consume any more of your time. |
| **C5** | **A negative result is only valuable if the experiment that produced it was capable of producing a positive one.** "It didn't work" is worthless. "My intervention had no effect while an equally long placebo did have an effect" is a contribution. | Design controls *before* you design the treatment. If you cannot state the control, you have not designed the experiment. |

## 1.3 The shape of a real research cycle

**[L1]** In practice, a research cycle looks like this, and it is not a checklist:

```text
    Something surprises you  ──────────────────────────────┐
             │                                             │
             ▼                                             │
    You try to explain it with the simplest story          │
             │                                             │
             ▼                                             │
    You search for who already told that story             │
             │                                             │
             ├──► They did, and their controls hold ────────┤ (idea dies, cheaply)
             │                                             │
             ▼ (they didn't, or their controls don't hold) │
    You write two rival explanations, H1 and H0             │
             │                                             │
             ▼                                             │
    You design the contrast that separates them            │
             │                                             │
             ▼                                             │
    You ask: can I run this by Friday? ─── no ────────────►┘ (question reshaped, not abandoned)
             │
             ▼ yes
    Cheapest possible pilot  ──► evidence  ──► the question MOVES
             │
             ▼
    You write down what you now believe and what you still can't rule out
             │
             └──────────► back into the loop, one level more precise
```

**The single most important structural fact about this loop: the pilot comes before the commitment.** **[L1]** Senior researchers almost never commit months to a question before they have spent a day getting *some* signal from it. Your own record demonstrates this principle in one place and violates it in another, and both are instructive — see §28.

## 1.4 What this manual will not do

- It will not give you a topic.
- It will not tell you that a "gap" exists.
- It will not make your literature search "complete". Completeness is not achievable and not the goal.
- It will not replace reading one paper all the way through, carefully, with the code open beside you. That remains the highest-yield activity in AI/ML research. **[L1]**

---

# 2. How Experienced Researchers Actually Work

## 2.1 They work from anomalies, not from areas

**[L1 — Established practice]** A common mental model of research is: pick a field → learn the field → find what's missing → fill it. This model is what causes most undergraduate wandering, because *"learn the field"* has no natural stopping point.

Senior researchers work from the other end. They maintain a small, personally owned list of **concrete anomalies** they have observed — usually in a paper's figure, a model's odd output, a failure in their own code, or a number that doesn't add up. An anomaly is small enough to be specific and strange enough to be worth explaining.

The *form* an anomaly takes (all drawn from your own corpus — **[L2]**):

- *"This paper reports a large effect, but the intervention it uses also lengthens the output. There is no length-matched control. So the effect might be compute, not mechanism."*
- *"These two papers claim the same phenomenon but describe the mechanism differently, and neither cites the other."*
- *"This benchmark reports a headline number that improves, but the ablation shows the improvement disappears when one component is removed."*
- *"This paper's limitations section says it never tested X. X is the interesting part."*
- *"This effect was demonstrated on procedurally generated grids. Nobody has tried it on natural photographs."*

Notice: **none of these is an idea for a system.** Each is a *discrepancy*. Discrepancies are cheap to find, hard to dismiss, and they already carry their own experimental design inside them — you know what the missing contrast is, because you noticed what was absent. **[L1 / SYNTHESIS]**

## 2.2 They read fewer papers than you think, and differently

**[L1]** The "read 200 papers" model survives because it sounds industrious. In practice a researcher in a healthy project has maybe **5–15 papers they know intimately** — closest works, method ancestors, the benchmark paper, the two papers they intend to beat — and a much larger set skimmed at abstract-and-figure level.

| Mode | Time per paper | Purpose | Trigger |
| :--- | :--- | :--- | :--- |
| **Sweep** | 30–90 seconds | Does this exist? Is it the same phenomenon? | Search results, related-work lists |
| **Card** | 5–10 minutes | Extract *claim / setting / control / limitation* into your field map | Paper survives the sweep |
| **Interrogate** | 1–3 hours | Find the exact experiment they did *not* run, and the exact wording in which they admit it | Paper is your candidate closest-work |
| **Reproduce** | hours–days | Make their number appear on your machine | You intend to build on their method or beat their baseline |

**The highest-yield transition in AI/ML research is Interrogate → Reproduce.** **[L1 / SYNTHESIS]** A paper whose code you have run teaches you more about the real frontier than fifty abstracts, because you discover *what they had to do to make it work* — and that is almost always where the next question lives.

## 2.3 They maintain a single, small, living artifact set

**[L1]** Productive researchers rarely keep elaborate note systems. They keep a small number of documents they actually reread:

- a **field map** (the lines of work, and who owns what),
- a **question ledger** (candidates, alive/dead, and *why*),
- a **reading card** per core paper,
- an **experiment spec** (frozen before running),
- a **log** (decisions, surprises, mistakes),
- a **results record** (what the numbers were and what they mean).

Your corpus already contains versions of nearly all of these, at very uneven quality. §29 turns them into a minimal, disciplined set. **[L2]**

## 2.4 They expect the question to change

**[L1]** The professional expectation is that the question will move. A researcher who runs the planned experiment and gets exactly the planned result with no surprise is usually doing an engineering validation, not research.

The skill is not preventing change. It is **noticing when the question has already moved** and updating the written artifact, rather than privately accumulating confusion while publicly maintaining a stale plan.

Your record contains a textbook example of a question moving on contact with pilot data:

> Your pre-freeze pilot (N=20) reframed the thesis from *"does verbalization shift source arbitration?"* to *"does conflict verbalization enable a qualitatively different cognitive mode — detection, problem selection, and conflict-aware abstention?"* because 25% of verbalization outputs legitimately abstained and 85% of direct-arm outputs matched **neither** stored answer. **[L2 — from `pilot_diagnostic_analysis.md`]**

That is exactly the behaviour senior researchers exhibit. The problem is not the reframing; it is how long the reframing took to reach the *written* plan. **[L3]**

## 2.5 They treat their own research tools as adversaries

**[L1]** Senior researchers use language models and search tools constantly, with a specific discipline:

- **Use them for retrieval, not for truth.** *"Find me papers that mention X"* is a good prompt. *"Is X novel?"* is a bad prompt, because the tool will answer, and its answer is a search result dressed as a judgement.
- **Use them for adversarial reading.** *"What is the strongest argument that this experiment is confounded?"* is a good prompt, because it generates hypotheses you then test by reading.
- **Never let them write a citation you have not clicked.**

**[L3 — and this one is not optional for you]** Any paper appearing in a document you call *"canonical"* must have its arXiv ID clicked and its metadata read by you. That is ~20 seconds per paper. Your corpus has ~40 anchor citations: about 15 minutes of work to eliminate an entire class of error. Appendix B shows this is not hypothetical.

---

# 3. Why Research Is Not Linear

## 3.1 The linear model is not a simplification — it is a different activity

**[L1]** The linear model:

```text
1. Choose field
2. Search papers
3. Find gap
4. Formulate question
5. Find dataset
6. Build model
7. Run experiment
8. Write thesis
```

This is not a compressed version of research. It describes **technical validation** — the activity you do *after* you already know the answer and want to demonstrate that a method works. Validation has a schedule. Research has a loop.

Why this matters practically: **if you follow the linear model, every step feels complete before the next begins.** You will search "enough", find a "gap", write a "question", and commit. Then step 6 destroys step 3, and you experience it as personal failure rather than as the normal mechanism of research.

## 3.2 The actual loop

**[L1]** The loop has five coupled stations. Every station can send you backwards. That is not a defect; backwards motion is where precision comes from.

```text
                       ┌──────────────────────────────┐
                       │  1. PHENOMENON               │
                       │  What behaviour is odd?      │
                       └──────────────┬───────────────┘
                                      │
        ┌─────────────────────────────▼─────────────────────────────┐
        │  2. LITERATURE                                             │
        │  Who has named this? Under what terminology?               │
        │  What did their controls rule out?                         │
        └───────┬───────────────────────────────────────┬────────────┘
                │  they ruled out my explanation        │  they didn't
                ▼                                       ▼
        ┌───────────────────┐                  ┌────────────────────────┐
        │  PIVOT or KILL    │                  │  3. COMPETING          │
        │  (still a result: │                  │     EXPLANATIONS       │
        │   the question is │                  │  H1 vs H0, both        │
        │   occupied)       │                  │  mechanically          │
        └───────────────────┘                  │  plausible             │
                                               └───────────┬────────────┘
                       ┌───────────────────────────────────▼──────────────┐
                       │  4. FEASIBILITY / DATA / BASELINE                 │
                       │  Can I run the separating contrast on Colab,      │
                       │  this week, with turnkey public data?             │
                       └───────┬───────────────────────────────┬───────────┘
                               │  no                           │  yes
                               ▼                               ▼
                    ┌────────────────────┐        ┌───────────────────────────┐
                    │  RESHAPE the       │        │  5. MINIMUM PILOT         │
                    │  question until    │        │  ~1 day, N≈20, one model  │
                    │  it fits the tool  │        └───────────┬───────────────┘
                    └─────────┬──────────┘                    │
                              │                               ▼
                              │                    ┌───────────────────────────┐
                              │                    │  6. NEW EVIDENCE          │
                              │                    │  The question has MOVED.  │
                              │                    │  Write the movement down. │
                              │                    └───────────┬───────────────┘
                              │                                │
                              └────────────────────────────────┘
                                        back to station 1 or 3
```

**[L3]** Practical rule: **at every station, before you advance, write one sentence naming the evidence that would send you back.** If you cannot name it, you have not understood your own question yet.

## 3.3 What the loop looks like in your own record

**[L2]** Your discovery arc, reconstructed from file timestamps and document contents, ran roughly 22 August → 24 September 2026:

| Approx. date | What happened | What triggered the move |
| :--- | :--- | :--- |
| 22 Aug | Parent field frozen: Multimodal / Vision-Language Learning and Systems. Three ranked lanes. Eight hard feasibility gates defined. | Compute, data-access and supervision constraints |
| 22 Aug – 3 Sep | Parked-field dossiers written (FL, medical imaging, security, diffusion, 3D, robotics, autonomous driving, generic RAG/agents) | Hard feasibility gates |
| ~14 Sep | Handover: "topic remains open"; several earlier claims contradicted by new evidence | Later audits falsified earlier audits |
| 20 Sep | Simultaneous four-field exploration: VLM, Medical Imaging, Multimodal Agents, FL | Breadth-first sweep |
| 21 Sep | Phase-1 landscape map + "antithesis scan"; Phase-2 feasibility audit (Q1/Q2); Phase-3 kill-gate filtering + pre-registration lock | Adversarial filtering |
| 22 Sep | Bengali cultural VLM audited; "Final Boundary Verification" of the cultural proposal | Second-domain sweep |
| 23 Sep | Four-proposal decision audit; topic frozen; two pilots; full-population census (N=1,619) — **all on one day** | Pilot evidence, then commitment |
| 24 Sep | Context, field specification, rejected/parked report, roadmap, master report consolidated as canonical | Documentation freeze |

Two structural observations to carry forward:

1. **The experimentation was fast; the discovery was slow.** The entire pilot → freeze → census sequence happened in roughly one day of compute. Discovery consumed five weeks. **[L2]**
2. **Exploration continued after the decision had effectively been made.** The Phase-1/2/3 kill-gate work (21 Sep), the Bengali audit (22 Sep), and the cultural "Final Boundary Verification" (22 Sep) all ran *after* the VLM conflict-arbitration direction was already the front-runner. This is the highest-value pattern to break. §21 and §28 analyse it.

## 3.4 Three signatures that you are in the linear model instead of the loop

**[L3]** Watch for these in yourself:

| Signature | What it looks like | What it actually is |
| :--- | :--- | :--- |
| **The completeness trap** | *"I should finish the literature review before designing the experiment."* | Deferring the only activity that would tell you which parts of the literature matter. Invert it: run the cheapest pilot as soon as you can state one contrast. |
| **The one-way door** | *"I've chosen this topic, so I should stop looking at alternatives."* or *"I'm still exploring, so I can't commit."* | The door is neither. You commit to a **question**, keep a **question ledger** of alternatives at card level, and never spend more than a bounded slice of time on them. |
| **Confirmation stacking** | Producing more and more documents that all point to the same conclusion. | The loop has stopped. Additional documents add *confidence*, not *knowledge*. Stop and run something. |

## 3.5 Why backwards motion feels like failure (and isn't)

**[L1 / SYNTHESIS]** When a station sends you back, the emotional reading is *"I lost time."* The accurate reading is: **you bought information about the shape of the problem at a known price.**

Compare:

- **Cheap backwards motion:** your candidate question dies in week 1 because the closest work already ran the contrast. Cost: 3 days. Benefit: you avoided 4 months.
- **Expensive backwards motion:** your candidate question dies in month 4 because a baseline you never reproduced behaves differently on your data. Cost: 3 months. Benefit: the same information, 25× more expensive.

**The entire purpose of the discovery loop is to force backwards motion to happen early, where it is cheap.** This single reframing is, in my assessment, the highest-leverage change available to your workflow. **[L3]**

---

# 4. The Researcher's Mental Model

## 4.1 The internal state: what a researcher is actually holding in mind

**[L1 — Established practice / SYNTHESIS]** When a senior researcher reads a paper or a result, they are not holding "the content of the paper". They are holding a **five-slot structure** that they update continuously:

| Slot | The question it answers | Why it matters |
| :--- | :--- | :--- |
| **CLAIM** | What does this work assert is true about the world? | Distinguishes a paper's *contribution* from its *method*. Many papers have a method but a weak claim. |
| **SETTING** | In which specific worlds was the claim tested? (data, model, task, resolution, language, compute) | Almost every literature dispute is a setting dispute. |
| **CONTROL** | What alternative explanation did the authors rule out, and how? | The control is where the science lives. Where controls are absent, the claim is *undetermined*, not false. |
| **CONCESSION** | What do the authors themselves say they did not test? | The highest-value sentences in a paper are usually in Limitations §. |
| **TENSION** | Where does this conflict with something else I believe or have read? | The tension is the seed of the next question. |

**[L3]** A cheap exercise that directly addresses your problem: take your three anchor papers and fill these five slots for each, on one page, using only the primary text. Then look at the TENSION column. That column is where your next project lives.

## 4.2 The four questions you must be able to answer at all times

**[L1]** A researcher at any moment should be able to answer these four without checking notes:

1. **"What is my phenomenon, in one sentence, in terms of observable behaviour?"**
   *Bad:* "Cross-modal conflict is important."
   *Good:* "With a neutral prompt, this model reproduces the arithmetic problem shown in the image rather than the one given in text, in ~90% of paired-conflict items."

2. **"What are the two competing explanations — and are both mechanically plausible?"**
   *Bad:* "The model prefers images."
   *Good:* "H1: verbalizing the conflict changes the computation. H0: the decision is fixed early and the verbalization is decorative."

3. **"What observation would distinguish them, and what is the strongest competing interpretation of that observation?"**
   *Bad:* "Measure accuracy."
   *Good:* "Measure which answer distribution shifts, under a length-matched neutral placebo. Strongest competing interpretation: any change is just extra test-time compute."

4. **"What am I doing this week that produces evidence rather than more reading?"**
   *Bad:* "More literature review."
   *Good:* "Run 20 items × 3 arms and check whether the output format parses."

**If you cannot answer all four, you are not yet in the execution phase, regardless of how much you have read.** **[L3]**

## 4.3 The distinction that most often breaks undergraduate projects

**[L2 / L3]** Your documents show this distinction blurred repeatedly across four different candidate fields, so it is worth stating with maximum precision. A researcher maintains three separate objects that feel identical when you are excited but are completely different:

| Object | Definition | Test it must pass | Failure symptom if conflated |
| :--- | :--- | :--- | :--- |
| **Interesting area** | A region of literature with active work | None. Anyone can have one. | You feel productive while learning nothing new. |
| **Phenomenon** | A measurable, reproducible behaviour with a named setting | Someone else's paper or your own script produces it on demand | You write a proposal with no numbers in it. |
| **Research question** | A contrast whose two possible outcomes change what a reader should believe | You can name the experiment and the control | You write a question whose answer is obviously "yes, sometimes". |

The practical failure mode: **a phenomenon feels exactly like a research question when you are reading about it.** *"VLMs forget visual information during long reasoning"* is a phenomenon. *"Does that forgetting persist when reasoning tokens are replaced by length-matched neutral tokens?"* is a question. The first is an observation. The second can be wrong.

## 4.4 The mental habit that separates senior from junior: thinking in contrasts

**[L1]** Junior researchers think in **conditions**: *"What happens if I use a better prompt?"*
Senior researchers think in **contrasts**: *"What is the difference between A and B, and what would each difference mean?"*

Every experimental design reduces to a contrast. Before writing code, fill in this table:

| | Condition A (control) | Condition B (treatment) | If B > A | If B ≈ A |
| :--- | :--- | :--- | :--- | :--- |
| Differs in exactly one thing | Neutral, length-matched | Conflict-verbatim | The semantic content of the intervention causes the effect | The effect is not caused by the intervention's content |
| Everything else held constant | Same model, length, seed, data | Same model, length, seed, data | — | — |

**If your design has no row that differs in exactly one thing, you do not have a falsifiable experiment — you have a demonstration.** **[L1]**

## 4.5 The mental habit that prevents false novelty

**[L1]** When a researcher has a promising question, the instinct is *"nobody has done this."* The trained reflex is instead:

> **"Who is the single most likely person to have already done this, and what would their paper be titled?"**

Then you go and look for *that paper* — not your paper. If you search your own phrasing you will find nothing, because nobody uses your phrasing. If you search by phenomenon, intervention, dataset and measurement, you will find the paper that would pre-empt you, or you will find that the space is genuinely clear.

This reframing is developed fully in §12. It is the highest-value searching skill in this manual. **[L3]**

---

# 5. Finding Research Territories

## 5.1 What a "territory" is and why it is the wrong place to stop

**[L1 — Established practice]** A **research territory** is a sub-area with an active community, shared benchmarks, shared vocabulary and recurring failure modes. Examples: *visual grounding failures*, *selective prediction and abstention*, *multimodal chain-of-thought dynamics*, *visual binding and compositional grounding*, *test-time compute allocation*.

Your own record contains a well-formed territory hierarchy:

```text
Parent field: Multimodal / Vision-Language Learning and Systems
│
├── Rank 1: Trustworthy and Reliable VLMs
│     ├── Grounding & evidence reliance
│     ├── Conflict & inconsistency            ← the territory you eventually worked in
│     ├── Explanatory faithfulness & reasoning mechanics
│     └── Uncertainty calibration & selective abstention
├── Rank 2: Generalization, Adaptation & Distribution Shift
├── Rank 3 (conditional): Efficient & Scalable VLMs
└── Supporting: XAI, PEFT, prompting, interpretability
```
**[L2 — reconstructed from your field specification and context documents]**

**The trap is that a territory is comfortable.** You can read in a territory indefinitely and feel you are making progress, because each paper teaches you something. But a territory contains thousands of open micro-questions and no criterion for which one to pick. That is precisely the state that produced your five weeks of wandering.

## 5.2 How to choose a territory in 1–2 days, not 2 weeks

**[L3 — my recommendation for your workflow]** Use four filters, applied as gates, in this order. Each is a yes/no. Do not score.

| Gate | Question | Disqualifies when |
| :--- | :--- | :--- |
| **G1 — Turnkey evidence** | Is there at least one dataset on which this territory's phenomena are already measured, publicly downloadable, licensed for academic use, and loadable by HuggingFace `datasets` in under 30 minutes? | You need credentials, a manual request form, scraping, or a multi-week approval |
| **G2 — Reproducible baseline** | Can at least one strong baseline for this territory be run by *you* in under 200 lines of PyTorch/Transformers on a 16 GB Colab GPU? | Baseline requires ≥7B fine-tuning, a distributed framework, or proprietary APIs as the only implementation |
| **G3 — Deterministic metric** | Does the territory already have a metric that is a deterministic function of the model output and the ground truth? | The only metric is LLM-as-judge without a validated ground-truth subset |
| **G4 — Negative-result value** | If the headline hypothesis is false, is there a specific published belief that your result would weaken? | A negative result would be "we found nothing" with no named recipient |

**Your own field specification already contains a version of these gates, and it worked.** **[L2]** It is worth noticing what those gates eliminated: federated learning (G1 and G2 failed), standalone 3D/robotics/autonomous driving (G1 and G2 failed), diffusion training (G2 failed), generic RAG/agents (G4 failed), standalone medical imaging (G4 failed — no algorithmic contribution to a CSE examiner), generic cybersecurity (G1 and G4 failed).

**[L3]** The improvement to make is **speed of application**. Those eliminations were correct. Reaching them took weeks and eight full dossiers. Applied as gates, the same conclusion takes a morning, and you can spend the saved time on the territory you keep.

## 5.3 The three-territory rule

**[L3]** Cap active territories at three. For each, spend at most **3–4 hours** of "carding" (see §10.2) before ranking them. Produce, for each territory, exactly:

- one paragraph naming the territory and its recurring failure modes,
- 3–5 named papers (foundational + two most recent influential),
- one named benchmark and one named dataset, with a verified link,
- two candidate phenomena written as measured statements (see §6),
- one sentence on why the territory might die under G1–G4.

Then rank. Then run §6 and §12 on the top two only. **Do not card a fourth territory.** This is the rule that would have saved you the most time. **[L3]**

## 5.4 What to do when a territory looks occupied

**[L2 / L3]** Your own record shows the correct behaviour and its cost. You audited four fields (VLM, medical imaging, multimodal agents, federated learning + a Bengali cultural variant) and, in every case, discovered that the **broad constructive formulation was occupied**, leaving only a *narrow diagnostic formulation*. Your documents phrase this identically four times:

> *"The broad question is not an open research gap; it is an occupied engineering domain."*
> *"Candidate 2 survives only if it pivots away from proposing algorithmic architectures … toward a rigorous, adversarial measurement and confound audit."*
> *"The field becomes scientifically viable only if it is reformulated from a constructive system build into a controlled diagnostic audit."*
> *"Q1 must be reframed, not killed, by RH-Bench."*

That is not four findings. It is **one pattern discovered four times** — and detecting it once is a genuine research skill you now own. **[L2]**

The generalised rule, worth memorising:

> **[L1 / SYNTHESIS] In a crowded AI/ML subfield, the frontier has almost entirely migrated from *constructive* contributions ("here is a method that improves X") to *diagnostic* contributions ("here is evidence that the measured improvement of X is partly an artifact").** For an undergraduate with 16 GB of GPU and no supervisor bandwidth, diagnostic contributions are not a consolation prize — they are the rationally correct target, because they require no training compute, produce deterministic evidence, and remain publishable when the effect is absent.

**Consequence:** when you discover a broad question is occupied, do not leave the territory. Look for *which measurement in that occupied literature has no control*, and build the control. **[L3]**

---

# 6. Finding Phenomena and Failures

## 6.1 The core move

**[L1 — Established practice]** A **phenomenon** is a reproducible, measurable behaviour under a stated setting. It is not a topic, not a claim, and not a gap. It is an observation with numbers attached.

The trained move is:

> **Read papers looking for the sentence that describes a behaviour, not the sentence that describes a contribution.**

Contribution sentences look like: *"We propose X, which improves Y by 3.2%."*
Phenomenon sentences look like: *"We observe that as generations become longer, models tend to drift away from image-grounded content."*

The second sentence is the raw material. The first is the packaging.

**[PRIMARY — verified]** That example is real: it is paraphrased closely from the abstract of arXiv:2505.21523, *"More Thinking, Less Seeing? Assessing Amplified Hallucination in Multimodal Reasoning Models"* (Liu, Xu, Wei, Wu, Zou, Wang, Zhou, Liu; v1 23 May 2025, v3 20 Jun 2025). The authors also introduce **RH-AUC**, "a metric that quantifies how a model's perception accuracy changes with reasoning length," and release **RH-Bench**. Read that abstract again and notice how much of the value sits in the *observed behaviour*, not in the proposed metric.

## 6.2 Where phenomena actually come from — and how to recognise each one

**[L1]** For each source below: what it is, how you recognise it in practice, and a concrete AI/ML example. **Recognition is the skill** — the list is easy, the noticing is hard.

### (a) An unexplained empirical phenomenon

**What it is:** a behaviour reported without a mechanism, or with a mechanism asserted rather than demonstrated.

**How you recognise it:** the paper reports an effect and then explains it using "because" or "due to" *without* an experiment that isolates that cause. Also: the effect is measured with one metric and the explanation invokes a different quantity.

**Practical tell:** a nice figure showing the effect, and a discussion section attributing it to something never measured.

**AI/ML example [PRIMARY — verified]:** arXiv:2505.21523 reports that longer reasoning chains lead to reduced focus on visual inputs and that "attention analysis shows" this contributes to hallucination. The attention-mass measurement and the hallucination measurement are separate metrics; the causal link between them is asserted via attention analysis rather than isolated with an intervention. *The phenomenon is measured. The mechanism is a lead, not a result.*

### (b) A surprising failure

**What it is:** a model fails at something it is "obviously" supposed to do.

**How you recognise it:** the output is not merely wrong but *wrong in a structured way* — wrong consistently, and wrong in a way that reveals what the model was actually computing.

**AI/ML example [L2 — from your pilot data]:** your pre-freeze pilot found that in the direct-answer arm, **85% of responses matched neither the image answer nor the text answer**. The model was not "choosing a source" — it was *computing* its own answer, sometimes blending both problems. That is a structured failure, and it is the most valuable sentence in your entire pilot record, because it invalidates the metric the original framing assumed. It is the canonical example of an experiment *changing the question*.

### (c) A contradiction between papers

**What it is:** two credible works assert incompatible things about the same phenomenon.

**How you recognise it:** you read paper B and think *"that contradicts the figure in paper A"*, and you cannot tell whether the difference is a real disagreement or a different setting.

**AI/ML example [L2 — from your Phase-1 landscape map]:** your scan observed that one family of phenomena (visual-evidence decline during reasoning) had been published under at least six different names by independent groups — "text-only takeover", "visual-reflection decline", "long-context visual forgetting", "visual insensitivity gap", "visual relay window", "losing focus with more compute". **Multiple names for the same phenomenon, produced independently, is itself a finding.** It means nobody has unified the terminology, which means nobody has verified that the measurements agree. A unification study is a legitimate contribution.

### (d) An obvious but untested alternative explanation

**What it is:** the result has a boring explanation that nobody controlled for.

**How you recognise it:** you ask *"what is the dumbest reason this effect could appear?"* and no paper in the area answers you. The two most common boring explanations in AI/ML are **more compute** and **different data**.

**AI/ML example [L2 — this is your thesis's core design, and the instinct is correct]:** a prompt that asks a model to verbalize a conflict also makes it generate more tokens. Longer generation means more forward passes, more computation, and more opportunity to condition on its own output. The boring explanation for any improvement is therefore *"it just thought longer."* The control — a **neutral prompt of matched length** — is the entire scientific content of the design. **[SYNTHESIS on the general principle; the specific design is documented in your own records]**

### (e) A limitation in an influential paper

**What it is:** the authors state what they did not test.

**How you recognise it:** go to Limitations **first**, not last. Look for sentences of the form *"we do not / we leave to future work / our framework measures X rather than Y."*

**AI/ML example [PRIMARY — partially verified]:** the abstract of arXiv:2608.17205 (*"Which Source Wins? Task-Dependent Reliance in Vision-Language Models"*, Ghosh, Gupta, Wang; submitted 17 Aug 2026) describes a controlled setup that degrades either the image or the text across four legs of legibility, builds conflicts from GSM8K and SVAMP by pairing the rendered image of one arithmetic problem with the text of another, and introduces ChartQA-Conflict (229 manually reviewed chart-report conflicts). Its measured object is **preference shift under legibility degradation**.

Your canonical documents record that its §6 explicitly disclaims testing whether models detect the contradiction, express uncertainty, or abstain. **[UNVERIFIED — from your records: I verified the paper's existence, authors, date and abstract, but not the wording of §6. Read §6 with your own eyes before you write it into a thesis.]**

This example deserves care. **A limitation-derived question is the cheapest legitimate source of a research question, and simultaneously the most dangerous — because a disclaimer in §6 does not mean the experiment is worth running.** §13 tells you how to test that.

### (f) A missing control experiment

**What it is:** the headline contrast has more than one difference between conditions.

**How you recognise it:** draw the §4.4 table for *their* experiment. If more than one row changes between A and B, you have found a missing control.

**Practical tell:** treatment and control differ in *length*, *phrasing*, *number of demonstrations*, *number of forward passes*, or *which model* — in addition to the thing being tested.

**AI/ML example [L2 — from your own Phase-3 kill-gate report]:** your audit identified that a flagship binding study placed its causal claim on activation swapping performed **only on procedurally generated symbol-partitioned grids, with no placebo swap**. Without a placebo — a swap of equal magnitude at matched location and norm that should not produce the effect — a replication cannot distinguish genuine information transfer from destructive perturbation of the host representation. That is a missing control, and building it is a legitimate contribution.

### (g) A boundary condition

**What it is:** a claim that is probably true, but only in a region nobody has mapped.

**How you recognise it:** the claim is stated universally ("models prefer X") but every experiment ran inside a narrow setting (one task type, one language, one image style, one model family). The question *"outside which boundary does this stop being true?"* is unasked.

**AI/ML example [PRIMARY — verified]:** arXiv:2608.17205 documents a genuine reversal at a boundary. On GSM8K and SVAMP, five of six models shifted more strongly away from degraded **text**; on ChartQA-Conflict, all six likelihood-scored models showed the **opposite** pattern, shifting more strongly away from the degraded **visual** source. The authors state: "modality reliance in VLMs is not fixed, but varies across tasks, evidence structures, models, and evaluation settings." **A documented reversal is a boundary marker**, and boundary-mapping is one of the highest-value, lowest-cost contributions available. **[L1 / SYNTHESIS]**

### (h) A measurement problem

**What it is:** the metric does not measure the construct the paper names.

**How you recognise it:** the metric is a proxy. Attention mass is a proxy for "visual information use". Log-probability margin is a proxy for "preference". Exact-match equality of two candidate answers is a proxy for "which source was followed".

**Practical tell:** you can describe two different mechanisms that would produce the *same* value of the metric.

**AI/ML example [L2 — from your own results analysis]:** your records show choice classification resting on entity matching producing an "ambiguous" bucket, with the reason documented in your own diagnostics: image and text problems can share domain vocabulary, and the model's reasoning text can mention entities from both problems. A metric that cannot decide in 42% of items is measuring *something*, but not cleanly "which source was chosen". **[L2]** The right research response is not to abandon the metric. It is to (i) report the ambiguity rate as a first-class result and (ii) triangulate with a second, independent measurement.

### (i) A benchmark weakness

**What it is:** the benchmark's construction creates artifacts, or its metric hides the thing you care about.

**How you recognise it:** read the benchmark's *construction procedure*, not its leaderboard. Ask: *how were the negatives made? Are the images synthetic? Do the "hard" examples share a template? Is the label learnable from a shortcut?*

**AI/ML example [PRIMARY — verified]:** arXiv:2608.16805 (*"Diagnosing Dense Same-Class Attribute Misbinding in Large Vision-Language Models"*, Xu et al., 17 Aug 2026) is *itself* a benchmark-weakness paper and states the weakness precisely: "Generic visual-question-answering accuracy marks the response as wrong, while object-hallucination metrics may regard both the object and attribute as image-supported; neither reveals the transfer." It releases InstaBind-Lite: 524 images, 529 curated groups of 3–6 same-class entities, 1,773 boxed instances, 9,580 deterministically evaluated questions; open-source models average a **19.84%** Misbinding Rate versus **7.55%** for commercial/API systems, and among identifiable transfers **80.70% / 81.51%** originate from adjacent instances. **The contribution is that existing metrics hide a failure, and a new benchmark makes it visible.** That is the clean template for a diagnostic thesis.

### (j) A replication that behaves differently

**What it is:** you reproduce a number and get a different one.

**How you recognise it:** this only happens if you reproduce something. It is the most reliable generator of research questions, and the one undergraduates skip most often. **[L1]**

**Practical tell:** your implementation is "obviously the same" and yet the curve differs. **Stop and investigate for one hour.** Either you found something or you found a bug — and both outcomes are worth more than another day of reading.

**AI/ML example [L2 — from your harness lineage]:** your production harness went v1 → v2 → v3 because earlier runs truncated outputs (100% of Arm 1 outputs hit a 15-token ceiling; ~90% of other arms hit a 90-token ceiling). Those were bugs, not findings. But notice what the process bought: v3 has *per-group* token budgets and a strict output contract. **A replication attempt is also an instrumentation audit.**

### (k) A method that works in a toy environment but has never been tested under realistic conditions

**What it is:** the mechanism was demonstrated on synthetic or procedurally generated data and never transferred.

**How you recognise it:** the words "synthetic", "procedurally generated", "grid", "controlled", "template" in the setup. Then ask directly: *has anyone run this on natural data?*

**AI/ML example [L2 — your Phase-2/3 record]:** the anchor work used non-ordinal symbol sets in a 2×4 grid with partition structure built in. The natural-transfer question — does the same representational effect survive intra-class variance, background clutter, and non-grid bounding-box geometry? — was recorded by your own audit as **not found** in the literature, and simultaneously flagged as *high risk of complete transfer failure*. That is an honest, well-characterised question with a legitimate negative outcome. **[L2]**

### (l) An observed behaviour whose mechanism is unclear

**What it is:** a behaviour is measurable and reproducible, but the *reason* is not established.

**How you recognise it:** you can write a clean description of the behaviour **without using the word "because"**. If you cannot, the mechanism is clear enough already. If you can, you have a mechanism question.

**AI/ML example [L2 — from your own pilots]:** 25% of conflict-verbalization outputs in your N=20 pilot explicitly refused to answer after correctly identifying the contradiction. The naive regex pipeline scored these as *parse failures* (0%). The behaviour — spontaneous, correct epistemic abstention — was real and reproducible; why it emerges under verbalization and not otherwise is a mechanism question. **It is also an example of a metric bug hiding a result.**

### (m) An assumption nobody has properly tested

**What it is:** a shared methodological assumption in a subfield that is used, cited, and never validated.

**How you recognise it:** everyone does X the same way, and you cannot find a paper that *justifies* X. **Search for the justification, not the usage.**

**AI/ML example [L2 — from your Phase-3 pre-registration]:** your pre-registration implements a *dilution null* — if attention were spread uniformly over `N` key positions, mass on any one position would scale as `M/N`, so a fall in visual attention mass must be compared against that baseline before being called "decay". Your own adversarial audit then wrote down the counter-argument: attention is never uniform in practice, so deviation from an idealised uniform null may not be meaningful. **That is a well-formed assumption test**, precisely because the null is stated *in advance* and its weakness is recorded.

### (n) An engineering bottleneck that reveals a scientific question

**What it is:** the thing that makes the implementation hard is itself evidence about the model.

**How you recognise it:** you spend a day fighting something — dynamic image token counts, a tokenizer mismatch, a gating failure, an OOM that scales super-linearly — and you ask *"why is this hard?"* instead of only *"how do I fix it?"*

**AI/ML example [L2 — from your pre-registration]:** tensor replacement between two images fails at runtime because Qwen2.5-VL's dynamic resolution produces different visual sequence shapes per image. The engineering fix is "pre-scale the images". The scientific question underneath is whether **the representation you are swapping between is index-comparable across images with different token counts at all.** If it is not, a "successful swap" may be an artifact of shape coercion. **[L2 / SYNTHESIS]**

## 6.3 The recognition table

**[L1 / L3]** Put this where you can see it while reading. When a paper gives you a small jolt of curiosity, identify which cell it fell into. You then immediately know the *shape* of the question you are holding — and the shape tells you the experiment.

| What you felt | Source | Question type | First action |
| :--- | :--- | :--- | :--- |
| "How does that work?" | (a) unexplained phenomenon | Mechanism | Find the intervention that would isolate the proposed cause |
| "That's weird — it shouldn't do that." | (b) structured failure | Diagnostic | Characterise the failure taxonomy before measuring rates |
| "But paper A said the opposite." | (c) contradiction | Reconciliation | Build the setting table for both; find the differing row |
| "It might just be longer answers." | (d) untested alternative | Confound control | Design the matched placebo |
| "They admit they never tested it." | (e) limitation | Extension / control | Test whether the untested thing is *important* (§13) |
| "Those two conditions differ in three ways." | (f) missing control | Control | Isolate one row |
| "But only on one task." | (g) boundary condition | Boundary map | Add the second task; predict the direction |
| "That metric doesn't show that." | (h) measurement | Construct validity | Find the construct the metric actually tracks |
| "The benchmark makes this easy to fake." | (i) benchmark weakness | Benchmark audit | Compute the shortcut performance |
| "Mine gives a different number." | (j) replication | Instrumentation or finding | 1 hour: bug or discovery? |
| "Only on synthetic grids." | (k) toy-to-real | Transfer | Find the natural analogue + the placebo |
| "I can describe it but not explain it." | (l) unclear mechanism | Mechanism | Write both explanations side by side |
| "Everyone assumes this and nobody shows it." | (m) untested assumption | Null construction | State the null, then break it |
| "This was painful to build." | (n) bottleneck | Hidden constraint | Ask what the difficulty implies about the model |

## 6.4 The phenomenon statement format

**[L3]** Force every phenomenon into this template. If you cannot complete it, you do not have a phenomenon yet.

```text
SETTING:    [model, version, dataset, split, N, decoding params]
STIMULUS:   [exactly what the input looks like]
BEHAVIOUR:  [observable output, as a rate or distribution]
COMPARISON: [what it is being compared against]
SURPRISE:   [what you would have expected instead, and why]
NULL:       [the boring explanation you cannot yet exclude]
```

**Worked example — your frozen project, in this format [L2, reconstructed from your master report and results record]:**

```text
SETTING:    Qwen2.5-VL-3B-Instruct, FP16, single T4-class GPU, deterministic parsing
STIMULUS:   image of arithmetic problem A + text of a different arithmetic problem B (paired conflict)
BEHAVIOUR:  under a neutral two-sentence descriptive prompt, the model's reasoning and final
            computation follow the IMAGE problem in ~89.5% of 1,619 items
COMPARISON: under a conflict-verbalization prompt of matched generation budget, image-following
            falls to ~25.8%; under a direct zero-shot prompt, text-following is ~85.5%
SURPRISE:   the reversal between the direct arm (text-dominant) and the neutral-description arm
            (image-dominant) is not obvious a priori; it is itself a finding
NULL:       the neutral and conflict arms may differ in effective computation despite matched
            token budgets; the entity-matching classifier has a non-zero ambiguity rate
```

**Notice what the NULL row does.** It is the row that turns an observation into a science project. If you cannot fill it in, your observation is not yet interesting — because there is nothing to rule out. **[L1]**

## 6.5 The phenomenon-quality checklist

**[L1]** Before you allow a phenomenon to become a research question, verify all six:

- [ ] **Reproducible:** you have seen it more than once, from more than one script/run.
- [ ] **Quantified:** it has a number and a sample size.
- [ ] **Bounded:** you can state the setting in which it appears and the setting in which you do not know whether it appears.
- [ ] **Non-trivial:** it is not a direct restatement of the model's training objective or of the dataset's construction.
- [ ] **Not already explained:** you have searched for its explanation, not just its description.
- [ ] **Has a named NULL:** you can articulate the boring explanation.

**If it fails 5 or 6, you have an observation, not a phenomenon.** That is fine — observations are the raw material. But do not build a thesis on a naked observation. **[L3]**

---

# 7. Turning Observations into Research Questions

## 7.1 The ladder

**[L1 — Established practice]** These eleven objects are not synonyms, and the most common cause of a stalled project is treating an earlier rung as if it were a later one.

```text
 1. RESEARCH AREA            a broad literature region
 2. RESEARCH TERRITORY       a sub-area with shared benchmarks and vocabulary
 3. PHENOMENON               a reproducible, measurable behaviour
 4. OBSERVATION              a specific instance of the phenomenon, with a number
 5. EXISTING CLAIM           the explanation someone has published for it
 6. ALTERNATIVE EXPLANATION  a rival explanation that nobody has excluded
 7. RESEARCH GAP             the claim that the rival explanation is unseparated
 8. RESEARCH QUESTION        the contrast that separates them
 9. HYPOTHESIS               the directional prediction for that contrast
10. EXPERIMENT                the smallest run that tests it
11. CONTRIBUTION              what a reader must now believe differently
```

**Rungs 1–3 are cheap and consume time without producing research. Rungs 4–7 are the actual work of discovery. Rungs 8–11 are execution.** Your five weeks of wandering were spent heavily on rungs 1–3 and 7, with insufficient time on 4–6 — which is why rung 7 kept collapsing. **[L2 / L3]**

## 7.2 The ladder, worked three times

### Example A — the diagnostic-control pattern

```text
1  AREA:                  Vision-Language Models
2  TERRITORY:             cross-modal conflict and evidence arbitration
3  PHENOMENON:            performance changes when image and text carry contradictory answers
4  OBSERVATION:           with a neutral descriptive prompt, the model's computation follows the
                          image problem in ~89.5% of paired-conflict items; with a direct prompt,
                          it follows text in ~85.5%
5  EXISTING CLAIM:        modality reliance is a property of the model's priors and is
                          task-dependent, degrading with source legibility
6  ALTERNATIVE EXPLANATION: the shift could be produced by additional test-time computation
                          (longer outputs = more forward passes), not by the semantic content of
                          the intervention
7  GAP:                   the semantic-content effect has not been separated from the
                          computation-length effect with a matched neutral placebo
8  QUESTION:              holding generation length fixed, does the semantic content of
                          conflict verbalization causally change which problem the model solves?
9  HYPOTHESIS:            if the content is causal, the conflict arm diverges from the
                          length-matched neutral arm; if not, the two are equivalent
10 EXPERIMENT:            matched-budget arms (direct / neutral-matched / conflict-matched /
                          forced-rationale prefill) over the paired-conflict population
11 CONTRIBUTION:          evidence on whether verbalized conflict awareness is a causal driver or
                          a decoration — and a reusable matched-budget protocol
```
**[L2 — this is your project on the ladder. Note that rung 6 is where the science is, and it was reached early. That is the strongest part of your process.]**

### Example B — the toy-to-real transfer pattern

```text
1  AREA:                  Vision-Language Models
2  TERRITORY:             visual binding and compositional grounding
3  PHENOMENON:            models assign an attribute to the wrong instance of the same class
4  OBSERVATION:           misbinding is invisible to both VQA accuracy and object-hallucination
                          metrics; measurable rates are ~19.8% (open) / ~7.6% (API), with ~80% of
                          identifiable transfers originating from an adjacent instance
5  EXISTING CLAIM:        a latent identifier induced by external visual structure (partitions,
                          annotations) binds objects to their designated slots, detectable by
                          within-partition alignment and causally manipulable by swapping
6  ALTERNATIVE EXPLANATION: the identifier is an artifact of the synthetic grid — of the
                          partition lines and symbol prompt themselves — and the apparent causal
                          effect of swapping is destructive perturbation of the host
                          representation rather than information transfer
7  GAP:                   the swap has never been given a matched placebo, and has never been run
                          on natural photographs with real bounding boxes
8  QUESTION:              does the representational effect survive on natural images, and does a
                          matched placebo swap produce it too?
9  HYPOTHESIS:            genuine transfer predicts target-specific changes under real swap and
                          none under matched placebo; artifact predicts both
10 EXPERIMENT:            pre-registered real swap vs. three matched placebos on natural images,
                          with covariate controls (colour histogram, spatial proximity, prior
                          naming, co-occurrence)
11 CONTRIBUTION:          determines whether a published mechanistic claim generalises beyond its
                          synthetic setting — and a negative result is a specific, publishable
                          correction
```
**[L2 — this is your reserve "binding" candidate on the ladder.]**

### Example C — the measurement-artifact pattern

```text
1  AREA:                  Multimodal Large Language Models
2  TERRITORY:             multimodal chain-of-thought and test-time compute
3  PHENOMENON:            visual grounding degrades as generated reasoning gets longer
4  OBSERVATION:           longer reasoning chains are associated with reduced attention to visual
                          inputs and increased perceptual hallucination; a metric (RH-AUC)
                          quantifies how perception accuracy changes with reasoning length
5  EXISTING CLAIM:        attention analysis indicates that longer reasoning chains reduce focus
                          on visual inputs, which contributes to hallucination
6  ALTERNATIVE EXPLANATION: the measured decline is partly mechanical — as key-sequence length `N`
                          grows, per-position uniform-attention mass scales as `M/N`, and rotary
                          positional distances change; a length-matched non-reasoning filler block
                          could produce a similar decline with no reasoning content
7  GAP:                   the reasoning-content contribution has not been isolated from
                          length, position and normalisation contributions
8  QUESTION:              with answer position and answer content held fixed, does inserting
                          reasoning tokens differ from inserting length-matched non-reasoning
                          tokens?
9  HYPOTHESIS:            content-specific decay predicts `long ≫ neutral`; dilution predicts
                          `long ≈ neutral`, with both tracking the `M/N` slope
10 EXPERIMENT:            matched-prefix teacher-forced conditions (short / long reasoning /
                          position-matched neutral / length-matched neutral) on counterfactual
                          image-question pairs, plus a residual-stream decodability probe
11 CONTRIBUTION:          separates a cognitive account from a measurement account of an
                          already-published phenomenon — high value under both outcomes
```
**[L2 — this is your reasoning-trace reserve candidate on the ladder. Your records correctly recorded that the naive version of rung 5's phenomenon is already published, leaving only rungs 6–8. That is an honest downgrade and it is the right kind of honesty.]**

## 7.3 The ladder is a filter, not a form to fill in

**[L1]** The purpose of walking the ladder is that **each rung can kill the candidate.** Everything below rung 8 is cheap; everything above is expensive.

| Rung reached | Cost so far | What a failure here means |
| :--- | :--- | :--- |
| 3 (phenomenon) | hours | You were reading, which is not wasted — but this is not a project |
| 5 (existing claim) | ~1 day | Someone already explained it; now find whether their explanation is *tested* |
| 6 (alternative) | 1–2 days | You cannot think of a rival explanation → the phenomenon may be trivial or already settled |
| 7 (gap) | 2–4 days | The rival is already separated by an existing control → **the candidate dies here, cheaply and correctly** |
| 8 (question) | 3–5 days | You cannot write the contrast as a table with one differing row → the question is not yet operational |
| 10 (experiment) | ~1 week | The smallest test needs ≥7B fine-tuning, gated data, or >12 GPU-hours → reshape (§17, §18) |

**The most valuable column is rung 7.** Almost all of your documented candidate casualties died at rung 7 — which is the right place for them to die. The improvement to make is *time-to-rung-7*, from weeks to days. **[L3]**

## 7.4 The three ways people cheat on this ladder (and what it costs)

**[L1 / L2]**

| Cheat | What it looks like in prose | What actually happens |
| :--- | :--- | :--- |
| **Skipping rung 4** | *"VLMs exhibit modality dominance."* | No number, no setting, no N. You cannot tell whether the phenomenon exists in your model at your resolution. You will discover at rung 10. |
| **Merging rungs 5 and 6** | *"Prior work claims X, but there might be other explanations."* | "Might be" is not a rival explanation. A rival must be *mechanically specific* and must make a *different prediction*. Vague rivals produce vague experiments. |
| **Jumping from 3 to 8** | *"I will investigate whether conflict reasoning improves VLM reliability."* | The rung you skipped (6) is the one that generates the contrast. Skipping it produces questions that cannot be wrong, which are not experiments. |

**Test for the third cheat:** try to write the sentence *"if I observe X, my hypothesis is false."* If you cannot, you skipped rung 6. **[L3]**

---

# 8. Literature Exploration Strategy

## 8.1 When to stop reading

**[L1 — Established practice]** This is the question that caused most of your lost time, so it deserves a mechanical answer rather than "when you feel ready".

**You stop reading when your reading stops changing your experiment.** More precisely, you stop when *three consecutive papers produce no change to any of the following*:

1. your phenomenon statement (§6.4),
2. your rival explanation (§7.1 rung 6),
3. your named closest work,
4. your controls or metrics,
5. your feasibility estimate.

That is a testable criterion. Keep a counter. If papers 12, 13 and 14 changed nothing, stop.

**The second stopping criterion, which is stronger:** you stop when you cannot name the experiment you would run. **At that point more reading is not the bottleneck — your question is.** Reading more will not fix an under-specified question; it will make it vaguer. **[L1]**

**The third, for the discovery phase specifically:** cap the total discovery reading. For an undergraduate thesis, **10–15 papers carded + 2–3 interrogated + 1 reproduced** is a defensible literature foundation. Beyond that, the marginal paper adds confidence, not capability. **[L3]**

## 8.2 Reading as a targeted instrument

**[L1]** The mistake is reading to "understand the field". The field is unbounded; you will never finish. Read to answer a specific question that is blocking your next decision.

| You need to decide... | Then read... | And stop when... |
| :--- | :--- | :--- |
| Is this phenomenon real? | The primary measurement paper's figures and methods | You have seen the figure and know how the number was computed |
| Is it already explained? | The explanation paper's method + ablation | You know which control they ran and which they did not |
| Is it already explained *under another name*? | Citation networks of the explanation paper | You have the terminology set (see §9.4) |
| Can I run a baseline? | The official repo's README, config, and eval script | You have reproduced one printed number |
| Is my contrast unperformed? | Closest-work methods sections (§12) | You can state exactly what they held fixed |
| What dataset do I use? | The dataset card + the benchmark paper's construction § | You know how negatives were built and what the leak risks are |
| Why did my run differ? | The paper's appendix on hyperparameters | You found the differing setting |

**Reading with a decision attached is roughly 5–10× faster than reading to learn, because your attention has a filter.** **[L1 / SYNTHESIS]**

## 8.3 The exploration funnel

**[L3]** The shape you want, with time budgets for an undergraduate project:

```text
   Landscape sweep                 ~2 days
   ├── 30-60 items screened at title/abstract level
   ├── 3 territories identified and gated (G1-G4, §5.2)
   └── output: one field map page per territory

        ▼
   Carding                         ~3 days
   ├── 10-15 papers carded (5-10 min each) -> claim/setting/control/concession/tension
   ├── terminology set collected (all the names for the same phenomenon)
   └── output: field map + reading cards

        ▼
   Interrogation                   ~3 days
   ├── 2-3 anchor papers interrogated (1-3 h each), full text + appendix + code
   ├── exact statements of what they did NOT test, quoted verbatim with section numbers
   └── output: closest-work table, limitations ledger

        ▼
   Closest-work search             ~2 days
   ├── 6-10 targeted searches from §12.3
   ├── every candidate dead or alive, with a reason
   └── output: question ledger v1

        ▼
   Minimum experiment              ~1-3 days
   ├── N≈20 items, 2-3 conditions, one model
   ├── purpose: make the question MOVE, or die
   └── output: pilot log + revised phenomenon statement

        ▼
   FREEZE or PIVOT
```

**Total: 2–3 weeks for a fresh area, if the gates are applied as gates.** Note that your five weeks were mostly justified by the fact that you were entertaining four territories plus a late fifth (Bengali cultural). Three territories, gated hard, is the fix. **[L3]**

## 8.4 What you should never do in the exploration phase

**[L2 / L3]** Each of these appears in your own corpus:

| Anti-pattern | Why it feels productive | Why it isn't |
| :--- | :--- | :--- |
| **Writing a "canonical" document before the question is frozen** | It feels like progress and it looks professional | It converts *provisional* claims into *authoritative* ones. §28 and Appendix B show the cost: two citation errors became "canonical". |
| **Commissioning a full audit for every candidate** | It genuinely eliminates wrong candidates | It also costs ~1–2 days each, and you ran it five times. Audit the top two only. |
| **Re-auditing a decided question to "confirm conviction"** | Prudence | It cannot change the decision without new evidence, so it is not decision-relevant. It only consumes schedule. |
| **Letting an AI tool produce your literature map** | It is 50× faster | Its output is unverified. §28 documents a real, propagated citation error. Use it to *find* papers; click every ID yourself. |
| **Treating "occupied" as failure** | Preservation instinct | Occupied is the normal state of AI/ML. The question is which *uncontrolled measurement* remains. §5.4. |

---

# 9. How to Search Like a Researcher

## 9.1 The principle: search for the *paper that would kill you*, not for your idea

**[L1 — Established practice]** Almost every failed novelty claim in your corpus has the same shape: a search was performed for the candidate's own framing, nothing was found, and "no one has studied X" was concluded. Later, a search performed by a different tool with different vocabulary found the pre-empting work immediately.

The behaviour to replace it:

> **Never search for your idea. Search for the experiment that would make your idea redundant, and search for it in the vocabulary of the people who would have run it.**

Terminology mismatch is the dominant failure mode of AI/ML literature search, and it is severe. Empirical reality: **different research communities publish the same phenomenon under names that share almost no tokens.** Your own Phase-1 landscape map documented this for a single phenomenon family — visual-evidence decline during reasoning — under at least six names across independent groups. **[L2]**

## 9.2 The search ladder

**[L1]** A research search is not one query. It is a **sequence of queries, each attached to a decision.** Here is the ladder. Run it in order; at each step, record what you found and what it changes.

```text
 1. PHENOMENON SEARCH        -> "is this behaviour real and named?"
 2. NAMING SEARCH            -> "what do different communities call it?"
 3. EXPLANATION SEARCH       -> "what mechanism is claimed?"
 4. MECHANISM SEARCH         -> "has the claimed mechanism been isolated?"
 5. ALTERNATIVE SEARCH       -> "has anyone proposed the boring explanation?"
 6. CONFOUND SEARCH          -> "has anyone controlled for it?"
 7. CLOSEST-WORK SEARCH      -> "what is the nearest experiment to mine?"
 8. REPLICATION SEARCH       -> "has anyone re-run it?"
 9. BOUNDARY SEARCH          -> "has anyone found where it stops being true?"
10. DATASET/ASSET SEARCH     -> "can I actually get the materials?"
11. RECENT-WORK SEARCH       -> "has this been closed in the last 6 months?"
12. SUCCESSOR SEARCH         -> "who cites the closest work, and what did they add?"
```

## 9.3 What each rung is for, and what it decides

**[L1 / L3]** Assume a starting phenomenon: *"VLMs appear to forget visual information during long reasoning."* Watch how the search evolves.

### Rung 1 — Phenomenon search

**Query:** `vision language model visual information loss long reasoning chain`
**Purpose:** establish that the phenomenon is real and has been measured.
**You are looking for:** a figure, a metric, a benchmark.
**Decision it informs:** does this phenomenon exist in published evidence at all? If nothing, your phenomenon is either novel (suspicious) or mis-described (likely).
**Typical discovery [PRIMARY — verified]:** you find arXiv:2505.21523, which measures exactly this and releases RH-Bench and RH-AUC.

### Rung 2 — Naming search

**Query:** try each of: `visual forgetting`, `visual attention decay`, `perception decline reasoning`, `visual grounding drift`, `attention sink visual tokens`, `modality collapse`, `text-only takeover`, `visual insensitivity gap`, `reflection decay`.
**Purpose:** find the *same phenomenon under other names*. This is the step most people skip and the one that saves the most time.
**Decision:** have you found the same phenomenon, or a different one? Different names with different measurement procedures means **nobody has verified that the measurements agree** — which is itself a contribution (§6.2(c)).
**Typical discovery [L2]:** your own landscape scan found this family named at least six ways by independent groups, including "text-only takeover", "visual-reflection decline", "long-context visual forgetting", "visual insensitivity gap", "visual relay window".

### Rung 3 — Explanation search

**Query:** `why visual attention decreases longer reasoning multimodal`, `attention analysis multimodal chain of thought hallucination`
**Purpose:** find the claimed mechanism.
**Decision:** is the mechanism *demonstrated* or *asserted*?
**Typical discovery [PRIMARY — verified]:** the paper says "attention analysis shows that longer reasoning chains lead to reduced focus on visual inputs, which contributes to hallucination." That is an *attention-mass* measurement linked to hallucination by interpretation.

### Rung 4 — Mechanism isolation search

**Query:** `causal reasoning trace length visual grounding controlled`, `position versus content ablation chain of thought attention`, `filler token control reasoning length`
**Purpose:** has anyone isolated the mechanism with an intervention rather than a correlation?
**Decision:** if yes, your mechanism question is occupied. If no, this is your gap.
**Critical supporting search:** `filler tokens chain of thought`, `test-time compute control CoT`. **[PRIMARY — verified]** arXiv:2307.13702 (Lanham et al., *Measuring Faithfulness in Chain-of-Thought Reasoning*, 17 Jul 2023) reports that "CoT's performance boost does not seem to come from CoT's added test-time compute alone or from information encoded via the particular phrasing of the CoT." **That sentence is the historical origin of the length-matched-placebo idea**, and it is why rung 4 is a legitimate place to look for prior art on controls.

### Rung 5 — Alternative-explanation search

**Query:** `attention dilution softmax normalization artifact reasoning length`, `RoPE distance bias long context attention decay`
**Purpose:** has anyone proposed the *boring* explanation before you?
**Decision:** if the alternative explanation is published, your question may already be answered — or may be a *refutation* of it. Either way you must know.
**What you are looking for:** a paper whose contribution is "the effect is an artifact."

### Rung 6 — Confound search

**Query:** `length matched control prompt intervention`, `compute matched baseline reasoning`, `token budget control chain of thought`
**Purpose:** has anyone already built the control you are planning?
**Decision:** if the control exists in a comparable setting, your contribution is the *result*, not the *method*. If it exists in a different setting, transferring it is a mild contribution. If it does not exist at all, **name it as your methodological contribution** and make sure it is described precisely enough to be reused.
**What to record:** who held what fixed, and what they left varying.

### Rung 7 — Closest-work search

**Query:** the ones from §12.3 (by phenomenon, intervention, measurement, dataset, model).
**Purpose:** find the single nearest experiment.
**Decision:** this is rung 7 of §7.1 — the candidate lives or dies here.
**Output:** one named paper, one sentence of what they held fixed, one sentence of what they left varying.

### Rung 8 — Replication search

**Query:** `[closest work title] replication`, `[method] fails to reproduce`, `[benchmark] criticism`, `[benchmark] flawed`
**Purpose:** has the closest work already been weakened by someone else?
**Decision:** if the closest work is itself disputed, your contribution may shift from *extension* to *arbitration* — which is often stronger.
**Why this rung matters most:** a critic-paper is a gift. It tells you exactly which claim is fragile.

### Rung 9 — Boundary search

**Query:** `[phenomenon] across tasks`, `[phenomenon] chart vs arithmetic`, `[method] fails on natural images`, `[method] scaling limits`
**Purpose:** has anyone mapped the region in which the claim holds?
**Decision:** if the boundary is known, do not re-map it. If it is unknown, boundary-mapping is a low-cost, high-value contribution.
**Typical discovery [PRIMARY — verified]:** arXiv:2608.17205's chart/arithmetic reversal is a *boundary* result: the direction of modality preference flips with the evidence structure.

### Rung 10 — Dataset and asset search

**Query:** the dataset card, the official repo, the model card, the license.
**Purpose:** can you actually obtain the materials, today, legally?
**Decision:** G1 and G2 of §5.2.
**What you must record:** exact dataset ID, size, split names, license, last-updated date, and how the negatives/labels were constructed.
**Typical discovery [PRIMARY — verified]:** a benchmark paper with 1,773 boxed instances and 9,580 deterministically evaluated questions and explicit source-instance annotations is far more usable for an intervention study than a benchmark that only provides image-caption pairs.

### Rung 11 — Recent-work search

**Query:** same as rungs 1–7 restricted to `submittedDate:[NOW-180DAYS TO NOW]` or the venue's 2026 proceedings.
**Purpose:** has this been closed since the closest work?
**Decision:** this is the rung that decides whether your *three-week-old* gap analysis is still valid. **Run it again the week you freeze.** In a fast area, a 3-month-old scan is not evidence.

### Rung 12 — Successor search

**Query:** Google Scholar / Semantic Scholar "cited by" on the closest work; arXiv "references & citations".
**Purpose:** find who built on it and what they added.
**Decision:** this is how you discover that your "gap" was quietly closed by a paper that does not share your vocabulary.
**Practical note:** this is the *single most reliable* way to find pre-emption. Pre-empting papers almost always cite the work you were going to extend.

## 9.4 Building the terminology set (the highest-value 30 minutes in discovery)

**[L1 / L3]** Before you search rungs 3–7 seriously, spend 30 minutes collecting the vocabulary. Procedure:

1. Take the closest work. List every noun phrase in its title, abstract, and the headings of its method section.
2. For each phrase, search it alone and collect the synonyms in the titles of the results.
3. Add the synonyms from the *adjacent-field* version of the phenomenon — the same thing described by the optimization, interpretability, or efficiency community. **[L2 — your own `find missing research` document does exactly this, mapping a target phenomenon to "adjacent / alternative formulations" and to "missing methodological predecessors". That table is the single most reusable artifact in your corpus. Keep doing it.]**
4. Write the resulting 8–20 terms as your **terminology set** at the top of the field map.

Then run every one of rungs 3–7 against the whole set, not one phrase.

## 9.5 Search hygiene rules

**[L1 / L3]**

| Rule | Reason |
| :--- | :--- |
| **Record the query and the date.** | A gap claim is only as fresh as the search behind it. `SEARCHED 2026-09-24: "length matched placebo multimodal" -> 0 relevant` is evidence. "I searched" is not. |
| **Search restricted-by-date at least once.** | A 2026 area's decisive pre-emption is often 60 days old. |
| **Search at least two engines/tools with different coverage.** | Different tools index different things; agreement between two is meaningful, one result is not. |
| **Follow citations, not just keywords.** | The successor search (rung 12) outperforms keyword search for pre-emption. |
| **Never accept "not found" from an assistant without a query trail.** | Your own Phase-3 kill-gate report is a model of good behaviour here: it reported **four of five required input files as MISSING (never found)** rather than reconstructing them. **[L2]** Insist on that from yourself and from your tools. |
| **Click every arXiv ID.** | Appendix B. |
| **Distinguish "not found" from "found and dismissed".** | Use four labels in your notes: `FOUND-OCCUPIED`, `FOUND-DISTINCT`, `NOT-FOUND (searched: <queries>)`, `REQUIRES CHECK`. |

---

# 10. How to Read and Interrogate Papers

## 10.1 The wrong model and the right model

**[L1 — Established practice]** The wrong model: read from beginning to end, understand everything, then decide whether it matters. This fails because (a) it costs hours per paper, (b) most papers do not matter to your question, and (c) "understanding" is not a decision.

The right model: **reading is a sequence of increasingly expensive passes, each of which can terminate the paper.** You are not trying to understand the paper. You are trying to extract the *one thing* that changes your project — or to establish that there is no such thing and move on.

## 10.2 The seven-pass ladder

**[L1 / L3]** An improvement on the standard three-pass approach, ordered so the cheapest passes come first.

```text
 PASS 0  TITLE + VENUE + DATE + AUTHORS          10 s   -> right era? right community?
   |
 PASS 1  ABSTRACT + FIGURE 1                      90 s   -> what is claimed, and what does the
   |                                                       headline figure actually show?
   |
 PASS 2  CLAIM/SETTING/CONTROL/CONCESSION card     6 min  -> the five-slot card (§4.1)
   |
 PASS 3  TABLES + ABLATIONS                       15 min  -> what survives component removal?
   |
 PASS 4  METHOD SECTION, with a pencil            30 min  -> what did they hold fixed?
   |
 PASS 5  LIMITATIONS + APPENDIX + CODE            60 min  -> the concession, quoted verbatim
   |
 PASS 6  REPRODUCE one number                    1-6 h   -> make their result appear on your machine
```

**Rule: each pass must terminate the paper or justify the next pass.** You should be able to say out loud *"I am reading Pass 4 because Pass 3 showed the ablation is missing."* **[L3]**

## 10.3 What each pass is actually looking for

### Pass 0 — Title, venue, date, authors (10 seconds)

**Looking for:** era and community. A 2023 paper on a 2026 phenomenon is a *foundational* reference; a 2026 paper is *potential pre-emption*. Venue tells you the reviewer bar. Authors tell you which group's vocabulary to search next (§9.4).
**Terminates when:** the paper predates the model/benchmark era you care about and is not a method ancestor.

**Note on venue:** **[L1 / PRIMARY lesson]** Verifying venue requires *primary* metadata. My own verification during this reconstruction found that arXiv metadata does not always state acceptance, and that "under review at X" is not "accepted at X" — see Appendix B. Record `venue: NOT STATED IN ARXIV METADATA` rather than guessing.

### Pass 1 — Abstract + Figure 1 (90 seconds)

**Looking for:** an explicit phenomenon sentence and a headline figure.
**Ask:**
- Does the abstract contain a sentence of the form *"we observe that…"* or *"we find that…"*? (Phenomenon — valuable.)
- Does Figure 1 show the *effect* or a *system diagram*? An effect figure means the paper has a measurement. A system diagram means it has a pipeline.
- How many rows differ in the headline comparison?

**Terminates when:** the phenomenon is not the one you care about, or the setting is far from yours (different modality pair, different task family).

### Pass 2 — The card (6 minutes)

Fill five slots. **Do not summarise.** Card the paper into your field map. **[L1]**

```text
PAPER:      <short name> (<arXiv id>, <date>, venue if verified in primary metadata>)
CLAIM:      <one sentence: what they assert about the world>
SETTING:    <model(s) + version, dataset(s), task(s), N, resolution, language, compute>
CONTROL:    <what alternative explanation they ruled out, and the mechanism of the control>
CONCESSION: <what they say they did not test — quote with section number>
TENSION:    <where this conflicts with something else, or is silent where it should speak>
RELEVANCE:  <one line: what this changes in MY project, or "nothing">
```

**This is the artifact that saves you time.** Fifteen cards is a working field map. You will reread the cards, not the papers. **[L3]**

### Pass 3 — Tables and ablations (15 minutes)

**Looking for:** fragility. Where does the effect actually live?
**Ask:**
- Which component removal costs the most? Is that component the *claimed* contribution, or a support component?
- Is there an ablation in which the effect disappears? If so, that ablation is the real story.
- Are the "improvements" larger than run-to-run variance? If no variance is reported, note that.
- In a measurement paper: do the sub-population breakdowns agree with the headline or contradict it?

**Terminates when:** the method is not relevant to your contrast and Pass 2 already answered whether they controlled for your confound.

### Pass 4 — Method with a pencil (30 minutes)

**Looking for:** what they held fixed. This is the closest-work comparison (§12).
**Do this:** draw the §4.4 contrast table for their main comparison. Fill in *every* difference between conditions, including uninteresting ones: length, decoding, prompt, number of demonstrations, image resolution, seeds.

**The output you want** is a sentence of the form: *"They varied X and Y while holding A, B, C fixed; therefore a difference in Z could come from X or Y."* That sentence is your gap — if it survives §13.

**Terminates when:** you can state the table and the ambiguity.

### Pass 5 — Limitations, appendix, code (60 minutes)

**Looking for:** the verbatim concession, and the real hyperparameters.
**Sources, in order of value:**
1. **Limitations section** — quote verbatim with section number. Do not paraphrase; you will need the exact wording in a thesis.
2. **Appendix** — where caveats live: dataset filtering, excluded items, prompt templates, hardware, failed runs.
3. **Official code** — where the truth lives. Read the data loader (where the leak, the filter and the truncation hide), the eval script (where the metric is defined), and the prompt templates (what the model actually saw).
4. **Dataset card** — license, split definitions, known issues.

**This pass confirms or destroys a gap.** Nearly every gap in your corpus was confirmed or destroyed here. **[L2]**

### Pass 6 — Reproduce one number (1–6 hours)

**Looking for:** whether the number is real on your machine.
**Do this:** run their eval on a small slice; produce one printed number; compare.
**What you get beyond the number:**
- the true runtime and memory footprint (feasibility, §17),
- the parse-failure rate (metric reliability),
- intuition for *what is hard* — which is where the next question lives.

**This is the pass most undergraduates skip and the pass that most reliably produces research questions.** **[L1]**

## 10.4 When to stop reading a paper

**[L1 / L3]** Terminate immediately, without guilt, when any of these is true:

| Termination trigger | Why |
| :--- | :--- |
| The dataset or task family is different enough that no transfer argument is plausible | You cannot use it as closest work |
| The contribution is a system/pipeline with no measurement | It cannot be closest work for a diagnostic question |
| The claimed effect is already the accepted explanation, and the explanation is untested | You have what you needed (a TENSION entry); stop |
| You have filled the card and the RELEVANCE line says "nothing" | The card is the deliverable |
| You are reading the related-work section for the fifth time | You are browsing, not researching |
| Pass 5 has given you the verbatim concession | The gap analysis is complete |

**One more rule, which matters for your specific failure mode:** if you find yourself opening a paper *to feel reassured that your direction is right*, close it. **Reassurance is not decision-relevant.** Only evidence that could change your decision is. Run the experiment instead. **[L3]**

## 10.5 Reading a paper adversarially: the interrogation script

**[L3]** When a paper is your candidate closest work, run this script explicitly and write the answers down. This is what "interrogation" means, and it takes 1–3 hours.

```text
1. CLAIM LADDER
   - What is the strongest claim the paper makes, in the authors' own words? (quote)
   - What is the weakest claim they actually need for their story? (quote)
   - Is the strongest claim supported by the weakest claim, or by a separate experiment?

2. SETTING ENVELOPE
   - List every dimension on which the setting could vary:
     model(s), model size, task family, dataset, image resolution, language, decoding,
     number of demonstrations, prompt phrasing, hardware, evaluation protocol.
   - For each dimension, state whether they VARIED it, FIXED it, or never mentioned it.
   - The dimensions they FIXED are your extension space.
     The dimensions they never mentioned are your validity risks.

3. CONTROL AUDIT
   - Draw the one-differing-row table for their main comparison.
   - Which rival explanations survive their controls? (list them)
   - Which rival explanations did they not consider at all? (list them)

4. CONCESSION HARVEST
   - Quote every sentence in Limitations / Discussion containing:
     "we do not", "we leave", "future work", "rather than", "does not", "limited to",
     "beyond the scope".
   - For each quote: does the concession correspond to an experiment you could run cheaply?
   - Record section numbers.

5. FALSIFIER SEARCH
   - What observation would have made the authors abandon this claim?
   - Did they report any measurement that came close to it?
   - If you cannot identify a falsifier, the claim is a description, not a hypothesis.

6. SUCCESSOR CHECK
   - Who cites this paper, and what did they add?
   - Did any successor already fill the concession you found?

7. THE ONE SENTENCE
   - Complete: "They held _____ fixed. I would vary _____. If the result changes,
     the reader should believe _____ differently."
```

**Rung 7 output.** If you cannot complete item 7, you do not have a candidate. **[L3]**

---

# 11. Building a Field Map

## 11.1 What a field map is for

**[L1 — Established practice]** A field map answers one question: **"if I have an idea here, who has already thought about it and what did they decide?"**

It is not a literature review. It is not a bibliography. It is not comprehensive. **It is a lookup table for pre-emption.** If it does not help you decide whether an idea is already occupied, it is the wrong artifact.

**[L2]** Your corpus contains several large documents that are *field analyses* but not *field maps* — they are excellent prose, but they do not let you look up "who owns this micro-question". The `Structural Taxonomy Mind Map` document comes closest, and its taxonomy structure is worth keeping. **[L3]**

## 11.2 The one-page field map

**[L3 — my recommendation]** Use exactly this. One page per territory. No more.

```markdown
# FIELD MAP: <territory name>
Last updated: <date>   |   Searches run: <queries + dates>

## 1. Terminology set (see §9.4)
<8-20 terms for the same phenomenon, with which community uses which term>

## 2. Lines of work (max 5)
| Line | Owned by | Central claim | State |
| --- | --- | --- | --- |
| <name> | <groups/paper shortnames> | <claim in one line> | ACTIVE / SATURATING / SETTLED |

## 3. The frontier (what is contested right now)
- <contested claim 1> -- contested by <whom>
- <contested claim 2> -- contested by <whom>

## 4. Benchmark ledger
| Benchmark | Shape | Size | Metric | Determinism | Verdict |
| <name> | <what it contains> | <N> | <metric> | deterministic / judge | usable / fragile |

## 5. Dataset ledger
| Dataset | HF ID | License | Split | Negatives constructed how | Leak risk |
| <name> | <id> | <license> | <splits> | <procedure> | <risk> |

## 6. Common methods
<the 3-6 methods everyone uses; note which are inference-only>

## 7. Known failure modes
<the failure taxonomy the field has settled on, with citations>

## 8. Unresolved questions
<the questions the field itself names as open -- quote, with source>

## 9. Controversies
<where two credible works disagree; the setting difference that explains it>

## 10. What is NOT in this map (explicitly)
<the regions you have not searched, so you never over-claim>
```

**Section 10 is the most important and the most often omitted.** Writing down what you have *not* searched is how you avoid "no one has studied X". **[L3]**

## 11.3 How the map evolves

**[L1]** The map is alive but must not grow. Rules:

| Phase | What changes | Size limit |
| :--- | :--- | :--- |
| During sweep | Lines of work and terminology set appear | 1 page |
| During carding | Benchmark/dataset ledgers fill in | 1–2 pages |
| During interrogation | Frontiers, controversies, unresolved questions get *sharper*, not longer | 2 pages |
| After pilot | Failure modes get rewritten from your own evidence | 2 pages |
| After freeze | **Frozen.** Only the date changes. New papers go into the question ledger as future work | 2 pages |

**If your map exceeds 3 pages, you are writing a review, not a map.** **[L3]**

## 11.4 Mapping your own corpus onto this structure

**[L2]** Mapping what you already have:

| Field-map section | Your best existing source | Gap to fix |
| :--- | :--- | :--- |
| Terminology set | `VLM/find missing research (Gemini).md` — the adversarial terminology-mapping table | Needs its claims verified ID-by-ID |
| Lines of work | `Extra Field Exploration/VLM Landscape and Adversarial Antithesis Scan.md` | Too long; needs compressing to ≤5 lines of work |
| Frontier | `phase-1---landscape-map---antithesis-scan-turn-1.md` — the crowding map by research cluster | Good; needs a "last searched" date |
| Benchmark ledger | `Adversarial Kill Gate Evidence Audit.md` — the dataset table | Strong; add license column |
| Dataset ledger | your master report's provenance ledger | Excellent; add license + "who created it" |
| Common methods | `Structural Taxonomy Mind Map` | Compress |
| Failure modes | your pilots' taxonomies ("neither", abstention, truncation) | Promote to first-class |
| Unresolved questions | your audits' "what remains untested" columns | Already good |
| Controversies | `Audit-to-Audit Contradiction Table` (Multimodal Agent audit) | This table is a superb pattern — reuse it |
| What is NOT in the map | **missing entirely** | Add it |

**The `Audit-to-Audit Contradiction Table` is worth naming as a reusable pattern.** When two research reports disagree, build a table with columns *Dimension / Report A claim / Report B claim / Agreement? / Stronger evidence / Verification resolution*. That is how you arbitrate between two AI-generated audits instead of picking the one you like. **[L2 — you invented this pattern; keep it.]**

---

# 12. Finding the Closest Existing Work

## 12.1 The one question that prevents false novelty

**[L1 — Established practice]** For every candidate question, ask exactly this:

> **"What is the single closest *experiment* anyone has already performed?"**

Not the closest *topic*. Not the closest *paper*. The closest **experiment**.

Why the distinction matters: a paper can be topically adjacent and experimentally distant, or topically distant and experimentally identical. Your novelty lives or dies at the level of *what was run*, not *what was written about*.

## 12.2 "Nobody has written my exact sentence" vs "nobody has answered my scientific question"

**[L1 — This is the single most important conceptual distinction in this manual.]**

| | Statement | Why it is worthless / valuable |
| :--- | :--- | :--- |
| **Type 1** | *"No paper contains the sentence: 'a length-matched neutral placebo is required to isolate the causal effect of conflict verbalization in VLMs.'"* | **Worthless.** Papers are not written in your sentences. The absence of a phrasing is evidence of nothing. |
| **Type 2** | *"No paper has run the matched-budget neutral-minus-conflict contrast on paired image/text numeric conflicts with a deterministic parser and reported the resulting contingency table."* | **Valuable.** This is a statement about an *unperformed experiment* and it can be falsified by finding one paper. |

**The rewrite rule:** take any novelty claim and mechanically rewrite it as *"no one has run [intervention] on [population] with [control], measured by [metric]."* If you cannot produce that sentence, you do not have a novelty claim — you have a hope.

## 12.3 How to search for the closest experiment

**[L1]** Search by *experimental anatomy*, not by topic. Six independent axes. **Run all six.** A single-axis search is how false novelty is manufactured.

| Axis | What you are looking for | Example query shapes |
| :--- | :--- | :--- |
| **1. Phenomenon** | Someone who measured the same behaviour | `modality dominance conflicting image text`, `visual forgetting long reasoning` |
| **2. Intervention** | Someone who applied the same or equivalent manipulation | `rationale prefill chain of thought`, `neutral filler token control`, `activation swap binding` |
| **3. Measurement** | Someone who operationalised the construct the same way | `length normalized likelihood margin modality`, `risk coverage curve abstention VLM` |
| **4. Dataset** | Someone who used the same stimulus construction | `GSM8K SVAMP image text conflict pairing`, `contradictory captions object attribute` |
| **5. Model** | Someone who ran the same model family at the same scale | `Qwen2.5-VL 3B probing`, `small open-weight VLM inference study` |
| **6. Causal design + evaluation protocol** | Someone who used the same design logic | `matched control prompt intervention`, `pre-registered ablation multimodal`, `compute matched baseline` |

**Why six axes:** each axis catches pre-emptions the others miss. A paper that changes the dataset is invisible to a phenomenon search. A paper that changes the vocabulary is invisible to a measurement search. A paper that changes only the model scale is invisible to everything except axis 5. **[L1]**

## 12.4 The closest-work table

**[L3]** Produce this. It is the most important table in your discovery phase.

| # | Closest work | What they already establish | What they leave unperformed | Overlap type | Redundancy risk |
| :--- | :--- | :--- | :--- | :--- | :--- |
| 1 | <name> (<id>, <date>) | <their measured result, one line> | <the specific unrun experiment> | conceptual / methodological / measurement / dataset | LOW / MED / HIGH |
| 2 | … | | | | |
| 3 | … | | | | |

**Rules:**
- **Every row must name a specific unperformed experiment.** "They don't do X" is not enough; "they report Y but never hold Z fixed" is.
- **Exactly one row is your PRIMARY closest work.** Your entire novelty claim is a statement about that one paper. The rest are supporting risks.
- **Assign redundancy risk honestly.** "High" is not failure — it means your contribution must be the *result*, not the *design*.
- **Re-run rung 12 (successor search) on the PRIMARY row before freezing.** **[L1]**

## 12.5 Worked example of the procedure

**[L2 — what your own process produced, formalised.]** Your four-proposal audit already contains a table with exactly the right columns: *Paper / What It Already Establishes / What Remains Untested / Type of Overlap / Redundancy Risk*. That structure is correct; keep it. Applying §12.3 to your frozen project's closest-work row:

```text
AXIS 1 PHENOMENON   -> FOUND: the anchor paper measures forced source reliance under
                       legibility degradation across arithmetic and chart tasks
AXIS 2 INTERVENTION -> FOUND: the anchor paper never verbalizes the conflict; a separate line
                       of work manipulates the reasoning trace (prefill / truncation /
                       paraphrasing), but only for single-modality text tasks
AXIS 3 MEASUREMENT  -> FOUND: the anchor paper uses generated answers plus a length-normalized
                       conditional log-likelihood margin; it does not measure arbitration as a
                       state transition across matched arms
AXIS 4 DATASET      -> FOUND: the stimulus construction (render one arithmetic problem as an
                       image, pair it with another problem's text) is published and reusable
AXIS 5 MODEL        -> FOUND: 6 open-weight VLMs + 2 frontier APIs; small open models included
AXIS 6 DESIGN       -> NOT FOUND: a matched-generation-budget placebo contrast that separates
                       semantic conflict awareness from additional test-time computation

=> PRIMARY CLOSEST WORK: the anchor paper
   ESTABLISHES: task-dependent modality preference shifts under legibility degradation
   LEAVES UNPERFORMED: separating the semantic content of conflict awareness from
                       computation length, with matched generation budgets
   OVERLAP TYPE: conceptual -- LOW redundancy
```

**Note the discipline:** five axes found overlap; one axis produced the contribution. Had you run only axis 1, you would have concluded "pre-empted" and abandoned a viable question. Had you run only axis 6, you would have concluded "totally novel" and never found the paper whose stimulus construction you are reusing. **You need both extremes.** **[L3]**

## 12.6 The novelty-triangulation rule

**[L3]** A novelty claim is only trustworthy when **two independent methods agree**:

1. **Keyword-and-axis search** (§12.3, all six axes) → not found.
2. **Citation-graph search** (successor search on the closest work, and on the closest work's own closest work) → not found.

If keyword search says clear but citation search finds a hitting paper, **the citation search wins.** Keyword-search failures are common; citation-search failures are rare, because pre-empting papers cite their targets. **[L1]**

## 12.7 What "closest work" is not

**[L1 / L2]**

| Not this | Because |
| :--- | :--- |
| A related-work paragraph in the paper you read | It is curated to make that paper look novel |
| A "similar papers" recommendation | It measures text similarity, not experimental similarity |
| A survey's taxonomy | Surveys lag; a 2026 survey may not include 2026 work |
| An assistant's summary of "papers on this topic" | Unverified; see Appendix B |
| The oldest paper on the topic | Foundational ≠ closest. Closest is nearest in *experiment*, and is usually recent |

## 12.8 How long this should take

**[L3]** For an undergraduate project: **2 days**, covering 6–10 searches, producing one closest-work table with 3–5 rows and one named PRIMARY row. If it is taking a week, you are carding instead of comparing. If it takes a morning, you probably skipped axes 3 and 6.

---

# 13. Verifying Whether a Gap Is Real

## 13.1 The gap-verification protocol

**[L1 / L3]** A gap is a *claim*. Like any claim it must be tested. Here is the complete protocol: **ten questions, each with a decision rule.** Run all ten before you spend a week on a candidate.

Time budget: **~4 hours** if the anchor paper is in hand. Your own audits effectively ran versions of these questions — but as free-form prose across multiple large documents, which is why they could not be re-run cheaply. Make them a checklist. **[L2 / L3]**

## 13.2 The ten questions

### Q1 — Has the question already been directly answered?

**How to test:** write your question as one sentence. Search it three ways: phenomenon-first, intervention-first, measurement-first. Then run the successor search on the closest work.

**Decision rule:** if a paper answers it in a comparable setting with a control, the gap is closed. **KILL or PIVOT.** If it answers it in an incomparable setting, the gap shrinks to a transfer question (→ Q5).

**Trap:** "directly answered" does not require your exact wording. If a paper measured the same contrast with different names for the variables, it is a direct answer. **[L1]**

### Q2 — Has it been indirectly answered?

**How to test:** ask *"what would have to be true for my result to be implied by existing work?"* Then look for that work.

**Decision rule:** if two existing results *together* imply your answer, your experiment is a confirmation. That is publishable only as a replication with a difference. **NARROW to the part that is not implied.**

**Worked example [L2]:** your own audit recorded that the "universality and architecture-independence" claim for a latent binding mechanism is *contradicted by foundational literature* — dual-encoder limit theorems and mechanistic studies showing binding is split across sub-circuits or resolved by serial pointing. That is a case where the answer was indirectly settled by theory, and the correct response was recorded: **strip the universality claim and keep only the transfer-and-specificity question.**

### Q3 — Has an equivalent experiment been performed under different terminology?

**How to test:** the terminology set (§9.4). Re-run Q1 against all 8–20 terms.

**Decision rule:** if yes, your gap is a *vocabulary gap*, not a scientific gap. **KILL.** Reporting a terminology gap as a scientific gap is the most common form of false novelty in AI/ML commentary.

**Worked example [L2 — a real one from your corpus]:** your canonical documents consistently use **"Binding IDs"** for a mechanism whose primary paper calls them **"Grounding IDs"**. Same mechanism, different name. Anyone searching only for your term would conclude the concept is unstudied. Anyone searching the primary term finds it immediately. **Naming drift creates the illusion of novelty.** Appendix B documents this.

### Q4 — Has later work closed the gap?

**How to test:** rung 11 (date-restricted re-search) + rung 12 (successors). **Re-run at freeze time, not just at discovery time.**

**Decision rule:** if a successor closed it, KILL. If a successor partly closed it, rewrite the gap as the remaining part. If a successor *claims* to have closed it but without a control, you now have a better question than your original one.

**Worked example [L2]:** your Phase-3 report records exactly this dynamic — a candidate was not killed but "must be reframed" because a later benchmark had already shown the headline phenomenon, leaving only the mechanism decomposition. **That reframe was correct, and it was only visible because the search was re-run.** Make that a standing rule.

### Q5 — Is the gap merely a dataset, language, or model difference?

**How to test:** strip your proposal down to its bare difference from the closest work. Then classify it:

| Difference | Scientific status | Verdict |
| :--- | :--- | :--- |
| Different dataset, same design | Transfer question | Weak unless the dataset has a *structurally different* property |
| Different language, same task | Domain-shift question | Weak unless a mechanism argument predicts a *different outcome* |
| Different model size, same design | Scaling question | Weak alone |
| **Different counterfactual contrast** | Causal-identification question | **Strong** |
| **Different measurement of the same construct** | Construct-validity question | **Strong** |
| **Different control** | Confound-isolation question | **Strong** |

**Decision rule:** if your difference falls in the top three rows, **NARROW or PIVOT.** If it falls in the bottom three, you have a real gap. **[L1 / SYNTHESIS]**

### Q6 — Is that difference scientifically meaningful?

**How to test:** complete the sentence: *"If the result goes one way rather than the other, then the paper I am extending is wrong about ___, and readers should change ___."*

**Decision rule:** if you cannot name the belief that changes, the difference is cosmetic. **KILL or NARROW.** A different setting that produces the same conclusion changes nothing.

**Worked example [L2 — from your own audit record, and it is the correct call]:** your medical-imaging dossier recorded that applying an existing metric to a different image dataset, on top of another group's published pipeline, is a "superficial contribution" and in one case "essentially duplicate". Your Bengali dossier recorded the same reasoning: applying an existing selective-prediction mechanism to Bengali images is "an incremental domain transfer". **That is exactly Q5+Q6 reasoning, applied correctly.** The improvement is speed, not method.

### Q7 — Is the missing experiment actually important?

**How to test:** find the *consequence*. Ask *"what downstream decision depends on this being answered?"* Three legitimate answers:

1. **A published intervention depends on it.** E.g. a training or decoding method optimises a quantity that your experiment might show is an artifact.
2. **A published interpretation depends on it.** E.g. a paper attributes an effect to a mechanism that your control might eliminate.
3. **A published benchmark or metric depends on it.** E.g. a benchmark's scores are computed in a way your experiment might show conflates two constructs.

**Decision rule:** if none of the three applies, the experiment is *curiosity*. Curiosity-driven work is legitimate research, but **it is not an undergraduate thesis with a deadline**. **KILL or PARK.** **[L3]**

### Q8 — Would the result change scientific understanding?

**How to test:** run the two-outcome test. Write both headlines:

```text
IF POSITIVE: "X causes Y, beyond confound Z."   -> who cares? what changes?
IF NEGATIVE: "X does NOT cause Y; the reported effect is attributable to Z."
                                                -> who cares? what changes?
```

**Decision rule:** at least one headline must name a specific *consequence*. If both headlines are "interesting", you have an excellent question. If both are "unsurprising", you have a weak one. **[L1]**

**Why the negative headline matters more for you [L3]:** with 16 GB of GPU and one semester, you cannot out-engineer a well-funded group. You *can* produce a result nobody else will produce, because producing it requires no new capability — only the discipline to run the control. **Your competitive advantage is the control, not the model.**

### Q9 — Could the proposed result be trivially predicted?

**How to test:** ask *"what would a competent reader guess the answer is, without running anything?"*

**Decision rule:** if ≥80% of competent readers would guess correctly, the experiment confirms the obvious. It may still be worth running as a sanity check, but **it is not a contribution.** Unless — and this is the useful exception — the literature currently asserts the *opposite* of what readers would guess. In that case a "trivial" result becomes a correction, which is highly valuable.

**Worked example [L2]:** your own project contains a genuinely non-obvious result: under a neutral description prompt the model follows the **image** (~89.5%), while under a direct zero-shot prompt it follows the **text** (~85.5%). A competent reader would not predict that reversal a priori. **That reversal is the most publishable single number in your results file, and it should be foregrounded.** It is a natural experiment on prompt framing, embedded inside your main design.

### Q10 — Would a negative result still teach us something?

**How to test:** write the negative-result paragraph in advance. *"We found that [intervention] had no effect on [outcome] relative to [control], implying that [published belief] should be revised because [reason]."*

**Decision rule:** if you cannot write this paragraph before running, the design has no fallback and a null result will be uninterpretable. **REDESIGN before running.**

**The strongest version of this test:** the negative result should be *the more interesting outcome*. In your frozen project's design, if verbalization had turned out to be decorative (post-hoc rationalization), that is arguably a *more* important finding than the positive one. **A question whose null outcome is more interesting than its alternative is a well-chosen question.** **[L3]**

## 13.3 The gap scorecard

**[L3]** Collate the ten answers into one line. This is what you put in the question ledger.

```text
CANDIDATE:  <one-sentence question>
CLOSEST:    <primary closest work + arXiv id + date verified>
Q1  direct answer?        YES / NO / PARTIAL       evidence:
Q2  indirect answer?      YES / NO / PARTIAL       evidence:
Q3  other terminology?    YES / NO                 terms searched:
Q4  closed by later work? YES / NO / PARTIAL       evidence:
Q5  nature of difference  transfer / scale / CONTRAST / MEASUREMENT / CONTROL
Q6  belief changed        "<the belief that changes>"
Q7  consequence type      intervention / interpretation / benchmark  (or NONE)
Q8  positive headline     "<one line>"
Q9  trivially predicted?  YES / NO   (if YES, is the literature asserting the opposite?)
Q10 negative paragraph    "<written in advance>"

VERDICT: KILL / PARK / NARROW / PILOT / FREEZE
NEXT ACTION: <the smallest experiment that would change this verdict>
DATE: <date>   RE-VERIFY BY: <date + 6 weeks>
```

**The `RE-VERIFY BY` field is not decoration.** In your frozen project's territory — and in most of multimodal AI/ML right now — a gap analysis has a shelf life of roughly **6–10 weeks**. Your own history contains at least one instance where an earlier audit's central absence claim was later contradicted by other reports. **[L2]**

## 13.4 The five false-gap archetypes

**[L1 / L2]** These are the shapes a false gap takes. Learn them by name.

| Archetype | Signature | Test |
| :--- | :--- | :--- |
| **The vocabulary gap** | "No one has studied X" where X is a renamed Y | Q3. Build the terminology set. |
| **The recency gap** | The search found nothing because it was run on a corpus that predated the pre-emption | Q4 + rung 11. Re-search with a date filter. |
| **The setting gap** | "No one did X on data Z" — where Z changes nothing mechanistically | Q5 + Q6. Name the belief that changes. |
| **The importance gap** | The experiment is unrun because it does not matter | Q7. Name the downstream decision. |
| **The artifactual gap** | The apparent gap is created by the metric or the benchmark, not by the science | §6.2(h) and (i). Audit the metric's construct validity. |

## 13.5 What to do when a gap dies

**[L3]** A dead gap is *output*, not failure. Record it and move. Concretely:

1. Move the candidate to the **DEAD** section of the question ledger, with the reason and the date.
2. Add the killing paper to the **Evidence Ledger** with its verified ID.
3. **Do not re-open it without materially new evidence.** Your own reconsideration protocol already requires thirteen items of evidence before reopening a parked field. **[L2]** That discipline is correct; apply it to dead *questions*, not just dead *fields*.
4. Spend the reclaimed time on the next candidate, not on re-litigating this one.

**A useful metric for your discovery phase: gaps killed per week.** A week in which you killed three candidates with documented reasons was a *productive* week. A week in which you confirmed one candidate that later died was not. **[L2 / L3]**

---

# 14. Competing Explanations and Hypotheses

## 14.1 Why two explanations are the minimum

**[L1 — Established practice]** A single explanation is not a scientific position; it is a belief. Science begins when you hold **at least two mechanically specific explanations that make different predictions.**

Why two, specifically:
- With one explanation, *any* observation confirms it (you will interpret noise as support).
- With two, every observation *discriminates*.
- With two, a surprising result is informative instead of confusing.

**The practical rule: if your phenomenon statement has a NULL row filled in (§6.4), you already have two.** If the NULL row is empty, you have a story, not a hypothesis.

## 14.2 The rival-explanation generator

**[L3]** When you cannot think of a rival, generate one from each of these templates. In AI/ML, these seven cover almost everything.

| # | Template | The rival it generates | The control it implies |
| :--- | :--- | :--- | :--- |
| 1 | **Compute** | The effect is from more computation, not from the content | Length- or FLOP-matched control |
| 2 | **Lexical/format** | The effect is from the *phrasing*, not the semantics | Paraphrase control; different wording, same meaning |
| 3 | **Data construction** | The effect is an artifact of how stimuli were built | Rebuild stimuli with a different construction; check a second source |
| 4 | **Datum/measurement** | The metric tracks a correlate, not the construct | Second independent metric triangulation |
| 5 | **Position/order** | The effect is from sequence position or ordering | Position-matched control; order-permuted replication |
| 6 | **Model specificity** | The effect is a property of this checkpoint, not of the mechanism | Second model family, ideally a different architecture |
| 7 | **Destructive intervention** | The manipulation damages the system rather than changing the target | Matched placebo manipulation of equal magnitude at matched location |

**Template 7 is the one most often forgotten, and it is the one that destroys the most neural-interpretability claims.** If you ablate, swap, or steer, you must show that a *matched but semantically meaningless* manipulation does not produce the same effect. Your own Phase-3 pre-registration contains a placebo trio for exactly this reason and it is the strongest methodological element in your corpus. **[L2]**

## 14.3 The hypothesis format

**[L1]** A hypothesis is only usable if it has four parts:

```text
H1 (name):      <the mechanism you believe>
  PREDICTION:   <the specific numeric pattern H1 requires>
  FALSIFIER:    <the specific observation that would reject H1>

H0 (name):      <the rival mechanism>
  PREDICTION:   <the specific numeric pattern H0 requires>
  FALSIFIER:    <the specific observation that would reject H0>
```

**The critical requirement:** the two PREDICTION lines must be *different in a way you can measure*. If H1 predicts "better" and H0 predicts "no change", the design must specify **better by how much** and **what counts as no change**.

**Worked example — your frozen project's hypothesis pair [L2, from your specification]:**

```text
H1 (Deliberative cognitive control):
  MECHANISM: generating tokens that articulate the contradiction forces cross-modal
             attention and causally updates the answer distribution
  PREDICTION: source-following under conflict verbalization differs from a length-matched
             neutral placebo by a nonzero amount, at a pre-specified significance level
  FALSIFIER:  conflict and length-matched neutral arms produce statistically equivalent
             source-following distributions (test of equivalence, not merely a null)

H0 (Post-hoc rationalization / attentional inertia):
  MECHANISM: the decision trajectory is fixed early by parametric priors; verbalization is
             linguistically fluent but does not steer the output
  PREDICTION: conflict and matched-neutral arms are statistically equivalent
  FALSIFIER:  a detectable, directional divergence that exceeds the placebo arm
```

**Note two design details that should be preserved, because they are good practice:**
1. **The H0 falsifier requires an equivalence test, not just a failure to reject.** "p > 0.05" is not evidence of no effect; you need *TOST-style equivalence* or a pre-specified smallest effect size of interest. Your own Phase-3 pre-registration uses TOST explicitly for its kill rules — **that is the correct instrument, and it should be used consistently.** **[L2]**
2. **H0 is a *substantive* hypothesis, not a null.** It makes its own positive prediction (early entrenchment). Designs where H0 is a bare "nothing happens" are weaker.

## 14.4 The three-hypothesis rule

**[L3]** If your data could be explained by a third mechanism, and the third mechanism is plausible, **add it to the design as a third condition.** Two-way designs lose to three-way designs when the third explanation is cheap to test.

**Worked example:** in your project's territory the three live explanations are: (i) conflict awareness is causal; (ii) verbalization is decorative; (iii) intermediate arbitration is unreliable/ambiguous by construction. The third is not a hypothesis about mechanism — it is a hypothesis about **measurement** — and it deserves its own arm or its own reported statistic (an ambiguity rate). Your design already reports an "ambiguous" category. **[L2]** Treat that as a first-class hypothesis, not as a data-cleaning problem: *"H2: the arbitration state is not well-defined for a substantial fraction of items."*

---

# 15. Adversarial Idea Testing

## 15.1 The mindset shift

**[L1 — Established practice]** The default mode of a junior researcher is to *build a case* for their idea. The mode of a senior researcher is to **build the case against it, as hard as possible, before anyone else does.**

This is not pessimism; it is strategy. The asymmetry:

| | Attack your own idea now | Let someone else attack it |
| :--- | :--- | :--- |
| **Cost** | hours | months, or a failed defense, or a rejected paper |
| **Information** | you learn the real weakness while it is fixable | you learn it after the structure is frozen |
| **Effect on the project** | the idea is narrowed into something defensible | the project collapses |

**Your record contains excellent instances of doing this** — the four-property kill-gate suite, a pre-registration with pre-specified kill rules, and a "strongest invalidation risk" field on surviving-question cards. **[L2]** The improvement is not the *method*; it is the *timing*. Adversarial testing belongs in the **first two weeks**, not after the topic is frozen.

## 15.2 The adversarial question battery

**[L3]** Run every candidate through all twelve questions and write the answers down. **A question you cannot answer is a finding about the candidate, not an embarrassment.**

| # | Question | What an unsatisfying answer means |
| :--- | :--- | :--- |
| 1 | **What is the strongest paper that could already have killed this?** | You have not found your closest work yet. Go do §12. |
| 2 | **What experiment would make my contribution redundant?** | If you cannot name it, you cannot know whether it exists. Name it, then search for it. |
| 3 | **What is the simplest explanation for the result I expect?** | If the simplest explanation is your explanation, it is probably not novel. |
| 4 | **Could the whole effect be caused by dataset construction?** | Then the result is about the dataset, not the model. Rebuild stimuli or find a second source. |
| 5 | **Could a trivial baseline reproduce it?** | Then there is no effect to explain. Run the trivial baseline **first**. |
| 6 | **Could extra compute explain the improvement?** | Then the content is not causal. Add a compute-matched arm. |
| 7 | **Could prompt wording explain it?** | Then it is a lexicographic effect, not a mechanism. Paraphrase the prompt and re-run. |
| 8 | **Is my experiment actually measuring the thing I claim?** | Then the construct is wrong. Triangulate with a second metric; report the ambiguity rate. |
| 9 | **Would this result be different on a larger model?** | If probably not, it may be a general property — or an obvious one. If probably yes, your single-model result is fragile. Say so. |
| 10 | **What would I conclude if the effect were half the size I expect?** | If your conclusion depends on a large effect, pre-specify the smallest effect size you would consider meaningful. |
| 11 | **If I got the opposite result, would I believe it?** | If no, you have a confirmation-bias problem, not a hypothesis. |
| 12 | **Who is the reviewer who will reject this, and what will they say?** | Write the rejection. Then fix it or accept it. |

## 15.3 The pre-mortem

**[L1]** Before running anything, write a **pre-mortem**: two paragraphs, past tense, explaining *why the project failed.*

```text
PRE-MORTEM — <project name>                        <date>

It is six months from now and this project failed to produce a defensible contribution.

Primary failure mode:
  <the single most likely reason, stated concretely>

Contributing factors:
  1. <...>
  2. <...>
  3. <...>

Earliest observable warning sign:
  <the first measurement that would have told us, and when it would have appeared>

Mitigation already in the design:
  <what the current design already does about this>

Mitigation still missing:
  <what must be added before the main run>
```

**Why this works:** it converts vague anxiety into a list of testable risks, and it makes the earliest warning sign explicit so you can instrument for it. **[L1 / SYNTHESIS]**

**Worked example of a good pre-mortem [L2 — derived from your own diagnostic documents, which recorded exactly these risks]:**

```text
Primary failure mode:
  The dependent variable is not well-posed. The model does not choose between the two
  candidate answers; it computes its own answer that matches neither. A "source arbitration"
  metric then measures classifier behaviour more than model behaviour.

Contributing factors:
  1. Entity-matching classification cannot decide on a large share of items and defaults to
     "ambiguous", so the headline statistic is computed on a shrinking denominator.
  2. Output truncation removes the final answer token, so exact-match accuracy is measured on
     a subset selected by generation length.
  3. A single model family at a single scale, so the result may be checkpoint-specific.

Earliest observable warning sign:
  In a 20-item pilot, the share of outputs matching neither stored answer is high, and the
  share of outputs hitting the token ceiling is nonzero.

Mitigation already in the design:
  A neutral length-matched placebo arm; deterministic regex parsing; a separate ambiguity
  category.

Mitigation still missing:
  A second, independent measurement of the construct; a sensitivity analysis excluding
  truncated items; a second model family.
```

**Notice:** factors 1 and 2 were written in *your own* pilot post-mortem. Your pilot **found** the failure modes — which is exactly what pilots are for. A pre-mortem makes you look for them one week earlier. **[L2 / L3]**

## 15.4 Adversarial reading of your own results

**[L1 / L3]** Once you have results, run the same adversarial pass on them. Five habits:

1. **Report the denominator, always.** Every rate needs its N, and every N needs its exclusion rule.
2. **Report the failure-to-parse rate as a result, not a footnote.** A 52% parse failure is a finding about the instrument. **[L2 — your own analysis document flagged exactly this.]**
3. **Check whether the effect survives removing the most suspicious subset.** If it does, that is a robustness result. If it does not, that is your real finding.
4. **Check whether the direction is consistent across sub-groups.** A reversal across task families is a *boundary result*, not noise, and is often more interesting than the aggregate. **[PRIMARY — verified]** arXiv:2608.17205 is a published example: modality-preference direction reverses between arithmetic conflicts and chart conflicts.
5. **Do not report behavioural evidence as mechanistic evidence.** **[L3 — important for your current thesis.]** Behavioural and intervention evidence can show *that* an output distribution changed, and *that* the change is caused by the intervention rather than by length. It cannot, on its own, show *which internal circuits were rerouted*. Claims of the form "this physically re-routes the attention heads and feed-forward pathways" require mechanistic measurements — attention extraction, activation patching, probing — not a contingency table. Either **scope the claim as behavioural**, or add a mechanistic experiment, or explicitly bridge to someone else's mechanistic result with a citation. A viva examiner will attack the stronger version, and the attack is correct. **[L3, SYNTHESIS]**

## 15.5 When to stop attacking an idea

**[L3]** Adversarial testing must terminate, or it becomes a new form of wandering. **Stop attacking and move to pilot when all four hold:**

1. You have named the closest work and stated what it leaves unperformed.
2. You can state both rival hypotheses and their falsifiers.
3. You have answered adversarial questions 1–8 without an unresolved fatal objection.
4. The remaining objections are *empirical* (answerable by measurement) rather than *conceptual* (not answerable by any measurement).

**A remaining conceptual objection means the question is not yet scientific. A remaining empirical objection means the question is ready.** That distinction is the stopping criterion. **[L3]**

---

# 16. Fast Idea-Killing

## 16.1 The economics of killing

**[L1 — Established practice / SYNTHESIS]** Killing ideas quickly is not a personality trait; it is an economic policy. Two facts drive it:

1. **The value of an early kill is enormous.** A kill in week 1 saves ~4 months. A kill in month 4 costs those months and damages morale.
2. **The cost of a kill is near zero** *if* the kill is recorded properly. A documented dead candidate is itself a field-map entry.

The policy: **make kills cheap and fast by making them testable.** An idea you cannot kill in a day is an idea you have not specified.

## 16.2 The 90-minute falsification task

**[L2 / L3]** Your medical-imaging audit contains a genuinely excellent artifact: a **60–90 minute falsification task** scripted minute-by-minute — verify dataset hygiene (min 0–20), run a zero-cost frozen-feature inference loop (min 20–50), compute the metric and the calibration refit (min 50–75), then decide. That is the single most reusable methodological pattern in your corpus, and it should be standing procedure for every candidate.

Here is the generalised version:

```text
THE 90-MINUTE FALSIFICATION TASK — <candidate name>        <date>

HYPOTHESIS BEING TESTED:
  <the one claim that must be true for this candidate to be worth a month>

MINUTES 0-20  — ASSET CHECK (no GPU)
  [ ] Dataset ID resolves; license recorded; N and split names printed
  [ ] Negatives/labels inspected for the property I need (print 5 raw examples)
  [ ] Model ID resolves; config.json prints parameter count and hidden size
  [ ] If any check fails -> STOP. This is a G1/G2 kill. Record it.

MINUTES 20-50 — CHEAPEST POSSIBLE MEASUREMENT (one T4-class GPU, or CPU)
  [ ] Load the smallest usable model (prefer 2-3B, bf16 or 4-bit)
  [ ] Run N=20 items through the MINIMAL version of my contrast (2 arms, not 4)
  [ ] Print: parse-success rate, the raw outputs of 5 items, and the two-arm split
  [ ] Do NOT build the full harness. Do NOT add metrics yet.

MINUTES 50-75 — THE DECIDING STATISTIC
  [ ] Compute the ONE number that decides: e.g. does arm B differ from arm A at all?
  [ ] Print a 2x2 table. If it is degenerate (one cell holds everything) -> STOP.
  [ ] Note the failure mode observed in the 5 raw outputs

MINUTES 75-90 — VERDICT
  [ ] SURVIVES  -> the effect exists in the right direction; scale up
  [ ] REFRAME   -> the effect exists but is not what I modelled; rewrite the phenomenon statement
  [ ] KILL      -> assets fail, or the table is degenerate, or the parse rate is unusable
  [ ] Record: verdict, evidence, the exact command, the date

HARD RULES:
  - No harness engineering before minute 75.
  - No additional arms before minute 75.
  - No metric design before minute 75.
  - If it takes more than 90 minutes, the experiment is too big to be a falsification test,
    which is itself the answer: the candidate is too expensive. Reshape it.
```

**[L3]** The hard rules are the entire value. Your history shows why: you built an elegant 4-arm pre-registered harness and a full statistical suite — correctly — but the *decision-relevant* information was available from 20 items. **Do the 20 items first.** Everything else is justified only after the 20 items say the question is alive.

## 16.3 The kill-fast allocation

**[L3]** Budget the discovery phase explicitly. For ~5 weeks of discovery:

| Allocation | Activity | Expected output |
| :--- | :--- | :--- |
| 25% | Sweep + card + terminology set | Field map (≤2 pages), 10–15 cards |
| 25% | Interrogation of top 3 candidates | Closest-work table, concession quotes |
| 15% | Gap verification (10 questions, all candidates) | Gap scorecards |
| **25%** | **90-minute falsification tasks** | **At least 3 tasks run; at least 1 kill** |
| 10% | Decision + freeze | Experiment spec |

**The 25% for falsification tasks is the part that was missing.** **[L2]** Nearly all of your discovery effort went to the first three rows and almost none to the fourth. Reading and auditing can tell you an idea is *occupied*; only running something tells you whether it is *true*.

## 16.4 The kill signals

**[L1 / L2]** Kill immediately, without further investment, when you observe any of these:

| Kill signal | Why it is fatal |
| :--- | :--- |
| The deciding 2×2 table is **degenerate** — one cell holds ~everything | There is no contrast to measure; the phenomenon is saturated |
| The **parse/extraction success rate is below ~70%** on gold labels | The instrument cannot measure the construct. Fix the instrument or change the metric — do not proceed |
| You need **gated or credential-restricted data** as the only route to the claim | G1 fails; there is no fallback |
| The only implementation requires **≥7B fine-tuning** or distributed infrastructure | G2 fails |
| The closest work **already ran your contrast** in a comparable setting | Q1 fails |
| You cannot write the **negative-result paragraph** | Q10 fails; there is no interpretable fallback |
| The effect requires **one specific prompt string** to appear | It is a lexicographic artifact, not a mechanism |
| A **trivial baseline** reproduces the effect | There is no effect to explain |
| Every adjudication requires a **human or an unvalidated LLM judge** | G3 fails; the evidence will not be defensible |
| After 90 minutes you have **no output at all**, only setup | The candidate is over-scoped for a falsification test. Reshape or kill |

## 16.5 What a good kill record looks like

**[L3]** Every kill produces a five-line entry. This is what makes kills cheap to repeat and impossible to relitigate.

```text
KILL RECORD
Candidate:   <question in one sentence>
Date:        <date>
Killed by:   <Q1 direct pre-emption / Q5 setting-only difference / degenerate table /
              parse rate 41% / gated data / trivial baseline reproduced it>
Evidence:    <paper id / command / the table>
Reusable for something else? <e.g. "the failure taxonomy from this pilot is reusable">
Re-open only if: <the specific new evidence required>
```

**Your corpus already does this correctly for parked fields** — each dossier has a "What would justify reconsideration?" section, and there is a formal thirteen-item reconsideration protocol. **[L2]** Apply the same structure to dead *questions*, at one-fiftieth of the length.

## 16.6 The two failure modes of fast killing

**[L3]** Fast killing has its own pathologies. Guard against both.

| Pathology | What it looks like | Guard |
| :--- | :--- | :--- |
| **Trigger-happy killing** | Every candidate dies in 20 minutes because the first check failed for a trivial reason (a typo'd dataset ID, a missing `pip install`) | Rule: **three distinct kill attempts on a candidate before it is killed for an asset reason.** Distinguish *"the asset does not exist"* from *"I could not access it in 20 minutes."* Your own Phase-3 report models this distinction correctly with its F1–F6 failure taxonomy: environment and machinery failures (F1–F3) get **repaired and rerun**; only architecture mismatch (F4), infrastructure (F5) and scientifically fatal (F6) failures count against the science. **[L2]** Adopt that taxonomy exactly. |
| **Never killing** | Every candidate "survives with modification", and the ledger fills with 12 live candidates | Rule: **at least one kill per discovery week, or your kill criteria are too soft.** |

**The F1–F6 taxonomy is worth restating because it is one of the best ideas in your corpus:**

```text
F1 configuration/environment  -> fix, rerun.      NOT evidence against the science
F2 harness/machinery          -> fix, rerun.      NOT evidence against the science
F3 dataset/asset fetch        -> use the pre-registered fallback, record it
F4 model-architecture mismatch -> can bear against the science; document
F5 compute/infrastructure     -> rescope or move, not a scientific failure
F6 scientifically fatal       -> stop and report
```

**[L2 — your Phase-3 pre-registration implemented exactly this, including pre-registered fallbacks for each asset and a "hard stops" list. That is professional-grade. It is the standard to hold every future pilot to.]**

---

# 17. Feasibility During Discovery

## 17.1 Feasibility is not a post-selection filter

**[L1 — Established practice]** The common mistake is: find an interesting question → build the plan → check feasibility → discover it is infeasible → start over. This wastes weeks and produces the experience of "I lost another direction".

The correct model: **feasibility is a discovery variable, evaluated continuously and in parallel with scientific interest.** Every candidate question carries a live feasibility score from day one.

This is *not* pessimism. Feasibility analysis is what tells you **how to reshape** a question. A question that is scientifically excellent but 40× too expensive is not dead — it is *unshaped*. The shaping move is always the same: **shrink the population, shrink the model, shrink the intervention, shrink the metric** (§17.6).

## 17.2 The seven feasibility dimensions

**[L1 / L3]** Evaluate all seven for every candidate. Score each `OK / RISKY / FATAL` **with a one-line reason**.

| # | Dimension | The question | FATAL when |
| :--- | :--- | :--- | :--- |
| **1** | **Data** | Can I get the dataset, legally, today, at the size I need? | The only route is gated, credentialed, or scraped |
| **2** | **Model access** | Can I load a model that exhibits the phenomenon? | Only ≥7B or API-only models exhibit it; no local checkpoints |
| **3** | **Instrumentation** | Can I measure the construct with standard tooling? | Requires custom kernels, unavailable `output_attentions`, or hooks you cannot write |
| **4** | **Compute** | Runs × runtime × memory, on a single 16 GB session? | Estimated >12 GPU-hours for the *main* run, or peak VRAM >16 GB with no batching fix |
| **5** | **Evaluation** | Is the metric deterministic and validated? | The primary claim requires an unvalidated LLM-as-judge |
| **6** | **Experiment count** | How many arms × datasets × models × seeds? | >~6 arms without factorial justification, or >3 datasets |
| **7** | **Time to first evidence** | How many hours until *any* signal? | >1 day for a *falsification* task |

**Compute arithmetic you should be able to do in your head [L2 — your own harness logs give the calibration]:**

- A 3B VLM in FP16 on a T4-class GPU at batch 16–24: roughly **2–3 s per item** for ~90-token generations. Your production harness achieved **2.32 s/item** for 500 items in 19.4 minutes, and the full 1,619-item census in ~104 minutes.
- Therefore **~1,600 items × 4 arms ≈ 1.5–2 GPU-hours** — the scale of experiment your hardware supports *cheaply*.
- Therefore a candidate needing **>10,000 forward passes with long generations** is at the edge, and one needing **fine-tuning** is out.

## 17.3 The parallelism rule: think about feasibility *while* reading

**[L3]** While you card a paper, run three feasibility checks in parallel:

```text
While reading a paper about the phenomenon, simultaneously ask:

  1. DATA   -> "Do they name the dataset? Is it a HF id, a GitHub repo, or 'available on request'?"
  2. MODEL  -> "How big are their models? Could my 3B stand-in exhibit this?"
  3. METRIC -> "Is their headline metric a deterministic function, or a model-based score?"
```

Put these on the card as their own fields. **Never end a carding session without knowing whether the assets exist.** **[L3]**

## 17.4 Mistake A: rejecting a good question too early

**[L1]** The failure pattern: the question needs a dataset you have not tried to download or a model you have not tried to load, and you decide "too hard" from the paper's *description*.

**Guards:**
- **Never reject for a reason you have not tested in 20 minutes.** "The dataset is probably gated" is not evidence. Open the URL.
- **Distinguish "requires a *different* resource" from "requires *more* resources."** A different model family is cheap; a different compute class is not.
- **Ask the reshaping question before rejecting:** *"Is there a version of this claim I can test with what I have?"* A claim about a 72B model can often be partially tested at 3B — and for a mechanistic question the smaller model is often *cleaner*, with fewer scale confounds.

**Your record contains a correct version of this call [L2]:** your pre-registration identified a secondary model as **gated** — an unauthenticated `config.json` request returned HTTP 401 — and instead of abandoning the cross-family leg, it **pre-registered explicit open fallbacks** (two alternative models) plus a note that the comparison would be at the level of *mechanism* rather than token identity, because vision tokenisation differs across families. **That is the right handling of a feasibility risk: reshape the claim and pre-specify the fallback.**

## 17.5 Mistake B: developing a beautiful question you cannot test

**[L1]** The failure pattern: months of refinement on a question whose test requires something you do not have — and whose requirement was never actually checked.

**Guards:**
- **The 90-minute rule (§16.2).** If you cannot get *any* signal in 90 minutes, the candidate is mis-scoped for discovery. (This is a rule about discovery, not about the final experiment.)
- **The "one number" test.** Name the single number that will decide the question. Then name the smallest run that produces it. If that run is not runnable this week, the question is not ready — reshape it.
- **The asset-freeze rule.** Before refining a question further, freeze the asset list: dataset ID, model ID, metric implementation — each with a verified link and license. **If any asset is unverified, stop refining and verify it.** Your corpus shows how much refinement can accumulate on top of unverified assets — see Appendix B.

## 17.6 How to reshape rather than abandon

**[L3]** When a candidate is `FATAL` on one dimension, do not abandon it. Apply the four shaping levers **in this order**:

| Lever | The move | Typically saves |
| :--- | :--- | :--- |
| **1. Shrink the population** | Test a stratified subset instead of the full population. Report the subset definition and its limits. | 5–20× compute |
| **2. Shrink the model** | Use the smallest open checkpoint that exhibits the phenomenon. Report the scale explicitly as a boundary. | 3–10× memory and time |
| **3. Shrink the intervention** | Test the *core* contrast only (2 arms); move auxiliary arms to a secondary experiment. | 2–4× |
| **4. Shrink the metric** | Replace a model-based judge with a deterministic parse on a validated subset; validate on ~100 human-checked items. | Removes an entire unreproducible component |

**Order matters.** Population shrinkage is cheapest and most defensible; metric shrinkage is riskiest because it changes the construct. **[L3]**

**Worked example of the levers applied [L2]:** your records show a plan moving from **500 items to 50 items** in a later phase, with a note that zero GPU measurements existed at that point. Population shrinkage is the correct lever — but it was applied **without asset verification**, which is the risk. **Shrink the population *and* verify the assets. Not one without the other.**

## 17.7 The feasibility one-liner

**[L3]** Every candidate in your ledger carries this line. It forces the estimate to be explicit and makes it comparable across candidates.

```text
FEASIBILITY: <model + size> x <N items> x <arms> ≈ <GPU-hours>   |   peak VRAM ≈ <GB>
             |   data: <id> (<license>)   |   metric: <deterministic? >
             |   time-to-first-signal: <hours>   |   FATAL DIMENSION: <none / which / both>
```

**Worked example [L2, calibrated from your harness logs]:**

```text
FEASIBILITY: Qwen2.5-VL-3B (FP16) x 1,619 items x 4 arms ≈ 1.7 GPU-hours  |  peak VRAM < 16 GB
             |  data: paired-conflict set (verify license + split definition)
             |  metric: deterministic regex parse (ambiguity rate must be reported)
             |  time-to-first-signal: ~25 minutes for 20 items x 3 arms
             |  FATAL DIMENSION: none for the core contrast; model diversity is the weak point
```

**Note the last entry.** Single-model-family dependence is *not* fatal, but it is a **stated limitation** — and stating it in advance is what lets you write an honest limitations section later instead of being ambushed in a viva. **[L3]**

## 17.8 The feasibility ledger

**[L3]** Keep all candidates' feasibility one-liners in one table. This is the artifact that prevents you from developing a beautiful question you cannot test.

| Candidate | Model × N × arms | GPU-hours | Time-to-signal | FATAL dimension | Verdict |
| :--- | :--- | :--- | :--- | :--- | :--- |
| A | 3B × 1,619 × 4 | ~1.7 | ~25 min | none | PROCEED |
| B | 3B × 500 × 4 + probes | ~3–4 | hours | dataset not downloadable | RESHAPE (rebuild or find source) |
| C | 3B + 4B × 50 × 8 | ~6 | hours | requires hooks + gated second model | RESHAPE (fallbacks pre-registered) |

---

# 18. Designing the Minimum Discriminating Experiment

## 18.1 The concept

**[L1 — Established practice]** The **minimum discriminating experiment (MDE)** is the smallest run whose outcome separates your two competing explanations.

It is defined by three constraints, in this priority order:

1. **Separating power:** the outcome must actually differ under H1 and H0. (First priority — this is the whole point.)
2. **Minimality:** every element not needed for separating power is removed. (Second priority.)
3. **Cost:** it runs in hours, not weeks. (Third priority — but if it cannot meet this, go back to (2).)

**The MDE is not a small version of your final experiment.** It is a *different kind of experiment*: a single-purpose instrument that answers one binary question. Your final experiment answers several questions with power; the MDE answers one question with almost no power. That is why it costs 1% as much.

**[L3]** For your situation specifically: the MDE is the single most powerful tool available, because your binding constraint is *time to a defensible claim*, not compute. Your hardware runs a 1,619-item × 4-arm study in ~1.7 GPU-hours. **You can afford MDEs. What you cannot afford is a month of refinement before the first measurement.**

## 18.2 The reduction procedure

**[L3]** Apply these six reductions, in order, to any proposed design. Stop as soon as the design is affordable *and* still separating.

```text
REDUCTION 1: Remove all arms not needed for the core contrast.
             (Start with 2 arms. Add a third only if the rival explanation requires it.)

REDUCTION 2: Remove all metrics not needed to decide.
             (One deciding statistic. Everything else is for the paper, not for the decision.)

REDUCTION 3: Shrink N to the smallest size that can show the effect if it exists.
             (N=20 for a pilot. N=100 for a direction check. Full N for the paper.)

REDUCTION 4: Replace the expensive stimulus with the cheapest stimulus that carries the property.
             (A rendered template beats a hand-collected photo. A synthetic grid beats a natural image,
              IF the property you are testing survives the substitution.)

REDUCTION 5: Replace any model with the smallest one that exhibits the phenomenon.
             (Say which one and why; report the scale.)

REDUCTION 6: Replace any judged metric with a deterministic one.
             (If you cannot, you must validate the judge on a labelled subset before using it.)
```

**The dangerous one is Reduction 4.** Substituting an easier stimulus can destroy the property you are studying. Test the substitution explicitly: *"does the cheap stimulus preserve the difference between my two conditions?"* That is itself a one-hour MDE. **[L1]**

## 18.3 The MDE worksheet

**[L3]** Fill this in before writing any code.

```text
MINIMUM DISCRIMINATING EXPERIMENT                              <date>
Question:      <one sentence>
H1 predicts:   <specific outcome>
H0 predicts:   <specific different outcome>

THE ONE DECIDING STATISTIC:  <name it, exactly>
  - how it is computed:      <formula or procedure>
  - H1 requires:             <value / relation>
  - H0 requires:             <value / relation>

ARMS (minimum 2):
  A (control):   <what varies least>
  B (treatment): <differs from A in EXACTLY ONE thing: ______>

FIXED ACROSS ARMS (must be identical, and I will verify):
  [ ] model + revision      [ ] prompt template (except the one varied thing)
  [ ] generation budget     [ ] decoding parameters
  [ ] items (paired)        [ ] image preprocessing
  [ ] metric implementation [ ] parsing procedure

STIMULUS:  <dataset id, split, N used, how items are paired>
MODEL:     <id, size, precision>
ESTIMATED: <minutes> on <GPU>   |   peak VRAM <approx>

ABORT CRITERIA (pre-registered, decide now):
  - parse success < ___%  -> stop, fix instrument, do not analyse
  - one cell of the 2x2 holds > ___% -> stop, table is degenerate
  - generation hits the token ceiling for > ___% -> stop, increase budget
  - VRAM exceeds budget after the prescribed fix -> rescope

WHAT I WILL CONCLUDE IF:
  H1 pattern -> ______
  H0 pattern -> ______
  NEITHER    -> ______ (this is the most common outcome; plan for it)

TIME BOX: 90 minutes. If exceeded, the design is not minimal.
```

**The `NEITHER` row is not optional.** In practice, the most common pilot outcome is that the data supports neither H1 nor H0 as stated, because the metric is imperfect or the effect is partial. **A design that cannot classify a "neither" outcome will produce confusion instead of information.** **[L3]**

## 18.4 Four worked MDEs

**[L3]** Note in each case how much smaller the MDE is than the "obvious" experiment.

### MDE 1 — Does the intervention change anything at all?

```text
Question:    does the conflict-verbalization prompt change which problem the model computes?
H1 predicts: the conflict arm's computed problem differs from the neutral arm's
H0 predicts: the two arms compute the same problem
Statistic:   share of items where the arm-B classification differs from arm-A (paired)
Arms:        A = neutral two-sentence description; B = conflict two-sentence explanation
             both with the SAME generation budget
N:           20 items, one model
Cost:        ~10 minutes
Concludes if: B differs from A on >= ~20% of items -> alive. On 0-1 items -> dead or
              instrument failure (check the raw outputs before concluding).
```
**What this replaces:** the full 1,619 × 4-arm study. **What it does not give you:** significance, effect size, generality. **What it gives you:** whether to spend a month.

### MDE 2 — Is the improvement just extra computation?

```text
Question:    could a length-matched non-semantic condition reproduce the effect?
H1 predicts: neutral-length condition does NOT reproduce the effect
H0 predicts: it does
Statistic:   the paired difference between (long-semantic) and (long-neutral), in the SAME direction
Arms:        A = long non-semantic filler of matched length; B = long semantic reasoning
             (answer position and answer content held fixed)
N:           20 items
Cost:        ~15 minutes
```
**This is the single most valuable MDE pattern in AI/ML**, because it kills the most common reviewer objection before you build anything.

### MDE 3 — Does the effect survive outside the toy setting?

```text
Question:    does the representational effect transfer to natural inputs?
H1 predicts: the intervention changes the output on natural inputs
H0 predicts: it does not (the effect was a property of the synthetic construction)
Statistic:   net flip rate, real intervention minus matched placebo, on natural items
Arms:        A = real intervention; B = matched placebo (equal magnitude, matched location)
N:           25 natural items + 25 synthetic items as an internal control
Cost:        ~30-60 minutes
Concludes if: natural net-flip CI excludes the placebo CI -> transferred.
              Natural net-flip overlaps placebo -> the effect is synthetic-specific (a result!)
```
**What makes this an MDE rather than a study:** the synthetic arm is retained purely as an instrument check. If the synthetic arm *also* fails, your harness is broken and you learn nothing about transfer. **[L3]**

### MDE 4 — Is the metric measuring the construct?

```text
Question:    does my automatic classifier agree with a human reading of the output?
H1 predicts: high agreement (kappa > 0.7) -> the metric is usable
H0 predicts: low agreement -> the metric measures something else
Statistic:   agreement rate and Cohen's kappa on 40 outputs, hand-labelled by me
Arms:        one arm only (this is a measurement-validation MDE, not a treatment MDE)
Cost:        ~45 minutes of human labelling
```
**This MDE is the most commonly skipped and the most commonly needed.** Your own diagnostics identified entity-matching ambiguity as a real risk; a kappa check on 40 outputs would have quantified it in under an hour. **[L2 / L3]**

## 18.5 Why the MDE is especially powerful for undergraduate research

**[L3]** Four structural reasons:

| Reason | Explanation |
| :--- | :--- |
| **It matches your resource profile** | You have 16 GB of GPU-hours and a semester; you do not have a cluster or an army of annotators. MDEs convert a resource limit into a methodological style. |
| **It converts anxiety into evidence** | The dominant emotional cost of your discovery phase was uncertainty about whether ideas were worth pursuing. An MDE converts that uncertainty into a number in 90 minutes. |
| **It produces a *result* even when negative** | "The effect does not transfer" or "the effect does not survive length matching" is a finding. The MDE is therefore not a wasted run. |
| **It forces specification** | You cannot run an MDE without naming the one deciding statistic. That forces you to complete §4.2 question 3 — which is where most vague projects die. |

## 18.6 Anti-patterns

**[L2 / L3]**

| Anti-pattern | Signal | Cost |
| :--- | :--- | :--- |
| **Building the final harness first** | You are writing batch scheduling, checkpointing and logging before you have seen a single model output | Days lost per candidate; you will rewrite it anyway after the pilot changes the metric |
| **Designing the metric before the contrast** | You are computing five statistics and no longer sure which one decides | The metric becomes the project. Your own record contains an instance where the pipeline was reframed around a new classifier *after* a pilot — correct, but it should have come first **[L2]** |
| **Adding arms "to be safe"** | 4 arms before 2 arms have ever run | 4× cost for 0 extra decision-relevant information in the pilot |
| **Running the MDE on the full population** | Using N=1,619 for a directional check | 80× cost for the same binary answer |
| **Treating the pilot as a paper experiment** | Computing p-values, effect sizes and confidence intervals on 20 items | False confidence. Report the pattern, not the significance |
| **Skipping the "neither" category** | The pilot produces outputs that fit neither hypothesis and you have no plan | Confusion instead of information |

---

# 19. From Research Question to Experimental System

## 19.1 The transition

**[L1 — Established practice]** Once the question survives §13 and the MDE (§18) says it is alive, you make a transition that people often mishandle: **you stop exploring and start building.** The failure mode is to keep the exploratory looseness while building — changing the metric mid-run, adding arms opportunistically, re-specifying the hypothesis after seeing the data.

The correct transition has a name: **you freeze the specification and pre-register the analysis.** Everything after that is execution.

**[L2]** Your corpus already contains the right instrument. Your Phase-3 pre-registration locks models, datasets, hypotheses, kill rules, a failure taxonomy, budget, order of execution, hard stops, and a deviation protocol — *before* any measurement existed. **That is genuine professional practice and it is the reason the phase produced a defensible verdict.**

**[L3]** Make it permanent: **no main run without a pre-registration file.**

## 19.2 The specification checklist

**[L3]** Freeze all ten items **before** the main run. Each item gets a written value; "TBD" is not a value.

| # | Item | What must be written down |
| :--- | :--- | :--- |
| 1 | **Question** | One sentence, and what would make you abandon it |
| 2 | **Hypotheses** | H1, H0, and their explicit patterns (§14.3) |
| 3 | **Conditions** | Every arm, the exact prompt/dataset/intervention, and the single thing each varies |
| 4 | **Population** | Dataset ID, split, N, inclusion/exclusion rules, pairing rule |
| 5 | **Model(s)** | ID, revision/commit, precision, decoding parameters, hardware |
| 6 | **Primary outcome** | The one statistic that decides, its formula, and the direction that supports each hypothesis |
| 7 | **Secondary outcomes** | Exploratory; explicitly labelled as exploratory so they cannot become primary post hoc |
| 8 | **Controls** | What is held fixed, and the check that verifies it |
| 9 | **Decision rules** | Thresholds for accept / reject / rerun, written before running |
| 10 | **Deviation protocol** | How a deviation is recorded, in what file, before which analysis |

**Item 10 matters more than it looks.** A pre-registration that cannot accommodate real-world failures becomes a document you quietly ignore — which is worse than no pre-registration, because it manufactures an illusion of rigour. **[L3]** Your own protocol handles this correctly: deviations require editing the pre-registration file with a dated `DEVIATION` note *before* the affected analysis runs.

## 19.3 What "one thing varies" means in practice

**[L1]** This is the requirement most often violated in AI/ML experiments. Between your control and treatment, everything except the intended manipulation must be identical. In practice that means these must be **programmatically identical**, not "similar":

- the prompt template, character for character except the intended difference,
- the generation budget (max new tokens, and the stop criteria),
- the decoding parameters (temperature, top-p, seed, repetition penalty),
- the item set (paired — the same items in every arm),
- the image preprocessing (resolution, pixel budget, normalisation),
- the parser and the metric code (the same function object).

**The verification habit [L3]:** after writing the harness, print the full prompt for arm A and arm B for one item, diff them, and confirm the diff is *exactly* the intended manipulation. Then print the token counts for both prompts. **If the token counts differ, you do not have a matched control.** This single check catches most confounds before they cost you a run. **[L1 / SYNTHESIS]**

## 19.4 Why length matching is harder than it looks

**[L1 / SYNTHESIS]** Length matching is not one number; it is at least four:

| What must be matched | Why | How |
| :--- | :--- | :--- |
| **Prompt length** | The prompt is part of the context the model attends to | Count tokens of the full rendered prompt |
| **Generated length** | Generated tokens add forward passes and self-conditioning | Match the generation budget *and* verify the observed mean generated length per arm |
| **Total sequence length at the answer position** | Positional encodings and attention normalisation depend on it | Fix the answer position, not just the budget |
| **Compute** | Wall-clock is not the causal quantity; FLOPs and step count are | Same model, same precision, same batch shape |

**The subtle one is #2.** If you set the same `max_new_tokens` for both arms but one arm's outputs systematically stop earlier, the arms differ in compute despite "matched" budgets. **Always report the observed mean generated length per arm.** Your own run analyses did exactly this — reporting average tokens and the share of items hitting the token ceiling per arm. **That is the right instrumentation, and it should be a required field in every experiment spec.** **[L2]**

## 19.5 The control-check table

**[L3]** Add this to every experiment spec. It is a five-minute check that saves a re-run.

```text
CONTROL-CHECK TABLE                                    <date>

                        Arm A            Arm B            Match?
Prompt tokens           ___              ___               [ ]
max_new_tokens          ___              ___               [ ]
observed gen. length    ___ ± ___        ___ ± ___         [ ]
% hitting ceiling       ___%             ___%              [ ]
answer position         ___              ___               [ ]
items (paired)          N=___            same items        [ ]
decoding params         t=__, p=__, s=__ t=__, p=__, s=__   [ ]
image preprocessing     ___              ___               [ ]
parser function         <name>           <same name>       [ ]

ONLY INTENDED DIFFERENCE BETWEEN ARMS: __________________________
```

**If any row is unchecked, fix it before running.** **[L3]**

---

# 20. Baselines, Controls, Metrics and Evaluation

## 20.1 The hierarchy of evidence quality

**[L1 — Established practice]** Not all "results" are equal. Ranked strongest to weakest:

```text
STRONGEST
  1. Paired, within-item intervention with a matched placebo, deterministic metric,
     reported as a state transition on the full population
  2. Paired intervention with a matched placebo on a subset
  3. Between-condition comparison on matched items without a placebo
  4. Between-condition comparison on different items
  5. Observational correlation across a benchmark
  6. A single model's outputs, qualitatively described
  7. "The model seems to..."
WEAKEST
```

**Your frozen project's design sits at level 1** — the strongest class available for a behavioural question without mechanistic instrumentation. That is worth recognising explicitly, because it is what makes the result defensible regardless of direction. **[L2]**

**Practical implication:** if you cannot reach level 1–2, say so *in the same sentence as the claim*. Claim strength must match evidence rank. **[L3]**

## 20.2 Baselines: what "strong baseline" means

**[L1]** A baseline is strong when it is **the thing a reasonable expert would try first**, not the thing that is easiest to beat.

| Baseline type | For which claims | Why it is mandatory |
| :--- | :--- | :--- |
| **Trivial / majority / constant** | Any accuracy claim | If a constant answer beats your method, you have no method |
| **Prompt-only / zero-shot** | Any method that adds components | Isolates the contribution of the added machinery |
| **Unimodal (image-only, text-only)** | Any multimodal claim | Tells you whether the other modality contributed at all |
| **Compute-matched** | Any claim of improvement from "thinking more" | Isolates mechanism from compute |
| **Published method reproduced** | Any "our method is better" claim | Otherwise you compare your code to their paper |
| **Random / permutation** | Any structured-intervention claim | Establishes the noise floor of your metric |

**Your project's most valuable baseline was the direct-answer arm**, because it revealed the text-dominance that the neutral-description arm inverted. Note that it was not designed to be the star of the analysis — it became one because it produced the surprising number (§13 Q9). **[L2]**

**[L3]** Rule: **always include the baseline that could embarrass you.** If you do not include it, a reviewer will ask for it.

## 20.3 Controls: the complete inventory

**[L1]** In AI/ML behavioural research, these are the controls and what each rules out.

| Control | Rules out | Cost |
| :--- | :--- | :--- |
| **Neutral, length-matched placebo** | Additional test-time computation / generation length | Low |
| **Paraphrase control** | Specific wording of the instruction | Low |
| **Position/order control** | Sequence-position and ordering effects | Low |
| **Random/permuted intervention** | Any structured-intervention claim | Low |
| **Placebo manipulation (matched magnitude, wrong target)** | Destructive-perturbation explanations in interpretability work | Low–Medium |
| **Second dataset, same construction** | Dataset-specific construction artifacts | Medium |
| **Second model family** | Checkpoint-specific effects | Medium |
| **Congruent / aligned items (no conflict present)** | False-positive detection — the model claiming conflict where there is none | Low |
| **Difficulty-matched subset** | Task-difficulty confounds | Medium |
| **Seed / decoding variation** | Stochastic decoding as the source of the effect | Low |

**[L2]** Your specification includes an explicit threat-to-validity table with a matched safeguard per threat — including an aligned-control set to penalise false-conflict reporting, and a filter for items where the baseline confidence margin is saturated. **That is a well-constructed threat model, and it was written in the specification, which is the right place.** Make it the template for every future project.

**[L3]** The control most often omitted by undergraduates and most often demanded by examiners is the **congruent/aligned control**: how often does your intervention claim to detect a conflict that isn't there? If that number is high, your "detection" result is partly fabrication. Add it.

## 20.4 Metrics: five properties of a usable metric

**[L1]** A metric is usable when it is:

| Property | Test | Failure symptom |
| :--- | :--- | :--- |
| **Construct-valid** | It changes when the construct changes, and only then | Two different mechanisms give the same value |
| **Deterministic** | The same input gives the same value, with no model in the loop | Scores drift between runs |
| **Sensitive to the effect size you care about** | A 5% change is visible above noise | The metric saturates — everything is 0% or 100% |
| **Robust to irrelevant variation** | Paraphrasing the output does not change the score | Different phrasings score differently |
| **Reportable with its failure rate** | You always know how many items it could not score | The headline silently excludes unscored items |

**The fifth damages real papers.** A metric with a 40% unscorable rate produces a headline computed on the 60% that happened to be scorable — and if scorable-ness correlates with the treatment (e.g. one arm's answers get truncated), the headline is biased by construction. **[L1 / L2 — your own analyses identified exactly this pattern: nearly all outputs in some arms hit the token ceiling before emitting a final answer.]**

**Rule [L3]:** every primary metric is reported as **`value (N_scored / N_total)`**, never as a bare value.

## 20.5 When LLM-as-judge is unavoidable

**[L1]** Sometimes there is no deterministic ground truth (free-form faithfulness, open-ended rationale quality). Then:

1. **Validate the judge.** Hand-label 40–100 items; report agreement (rate + Cohen's kappa). If kappa < 0.6, it is not a usable instrument.
2. **Freeze the judge.** Record exact model snapshot, temperature, system prompt, rubric.
3. **Test the known biases.** Position bias (swap candidate order and re-score); verbosity bias (does the longer answer win?); self-enhancement bias (does it prefer outputs from its own family?).
4. **Never let the judge be the only evidence** for the headline claim. Use it for triangulation.

**[L2]** Your context document already states this policy correctly — validate against ground-truth subsets or human correlation, and check positional, verbosity and self-enhancement biases. **The policy is right. Enforce it.** **[L3]**

## 20.6 Statistical testing for inference-only studies

**[L1 / L3]** Most AI/ML behavioural studies are inference-only, which constrains the statistics. Choose the test *before* looking at the data.

| Situation | Correct test | Note |
| :--- | :--- | :--- |
| Paired, same items in both arms, binary outcome | **McNemar's test** | The right test for within-item state changes |
| Unpaired 2×2 contingency, small cells | **Fisher's exact** | Use when any expected cell < 5 |
| Unpaired 2×2 contingency, large cells | **Pearson χ²** | Report with an effect size, never alone |
| Effect size for two proportions | **Cohen's h**, relative risk, odds ratio | Report all three; they answer different questions |
| Claim of *no* effect | **TOST equivalence test**, with a pre-specified equivalence bound | "p > 0.05" is **not** evidence of no effect |
| Stochastic decoding / sampling variation | **Bootstrap CI** over items, or repeated decoding | Do not treat one greedy run as exact |
| Many exploratory comparisons | Pre-specify the primary; label the rest exploratory | Post-hoc metric selection is the classic inflation |

**Two rules that matter most [L3]:**
1. **Report the paired test when the design is paired.** Your design evaluates all arms on the same items; the paired test is both more powerful and more appropriate. Your statistical suite uses McNemar — correct.
2. **If you intend to claim equivalence, use TOST.** Your Phase-3 kill rules use TOST for exactly the equivalence claims. **That is the rigorous choice and it is rare in undergraduate work. Keep it.**

## 20.7 Reporting the numbers honestly

**[L3]** A short checklist for every results table you ever produce.

```text
[ ] Every rate has its N: "89.5% (1449/1619)", not "89.5%"
[ ] Every exclusion rule is stated before the number it affects
[ ] The parse/extraction success rate is reported as a row, not a footnote
[ ] The share of items hitting a generation ceiling is reported per arm
[ ] Ambiguous/unclassifiable items are reported as their own category, not dropped
[ ] The test used, its statistic, its p-value and its effect size are all given
[ ] For equivalence claims, the bound and the test are given
[ ] Stochasticity handling is stated (greedy? seed? bootstrap?)
[ ] Model revision, precision, hardware and software versions are recorded
[ ] A "limitations" line accompanies every claim that exceeds evidence level 1-2
```

**[L2]** Your own production analyses do most of these already — they report average tokens, the share at the limit, and a separate ambiguous category. **The two to add are the exclusion rule and the model revision hash.** Both are one-line changes that a reproducible-research checklist will require.

---

# 21. Pilot → Main Experiment

## 21.1 What a pilot is for

**[L1 — Established practice]** A pilot has **one** job: to tell you whether the main experiment is worth running, and to tell you what to fix. It is not a small version of the main experiment, and it is not for producing results.

Therefore a pilot is judged by whether it *changed something*. A pilot that produced no change to the design, the metric, or the question was not a pilot — it was a wasted run. **[L2 — your own pilots did exactly what pilots should: they changed the metric, the output contract, the prompt design, and the framing of the question.]**

**Five things a pilot must test, ordered by likelihood of failure:**

| # | What the pilot tests | Typical failure discovered |
| :--- | :--- | :--- |
| 1 | **Instruction following** | The model does not produce the required output format |
| 2 | **Parseability** | The parser cannot extract the answer from the output |
| 3 | **Generation budget** | Outputs are truncated before the decisive token |
| 4 | **Contrast visibility** | The arms produce the same distribution, or a degenerate one |
| 5 | **The construct** | The metric classifies something other than what you claimed |

**[L2]** Your two pilots discovered (2), (3), (4) and (5) — a remarkably complete set:

- **Pilot 1 (free-form)**: a naive parser scored correct abstentions as parse failures (0%); free-form lengths varied from 12 to 240 tokens, introducing a token-budget confound; and 85% of direct-arm outputs matched **neither** stored answer — a construct problem, not a metric problem.
- **Pilot 2 (structured + 2-shot)**: few-shot demonstrations *biased the model's arbitration* (treatment contamination); forcing a binary choice with no abstention escape valve produced degenerate rationalisation loops.
- **Architectural response**: eliminate demonstrations, impose a strict output contract, keep a length-matched placebo, add an entity-based transition classifier. **That is a pilot doing its job perfectly.**

## 21.2 The pilot protocol

**[L3]** Standardise it. This protocol would have reached the same conclusions in a day rather than a sequence of iterations.

```text
PILOT PROTOCOL — <project>                        <date>

PURPOSE: make or break the current design. Not to produce results.

SIZE:      N = 20 items (drawn to span the strata you care about, not at random)
ARMS:      the minimum needed to see the contrast (2, or 3 if a placebo is needed)
MODEL:     the smallest model that exhibits the phenomenon
BUDGET:    <= 60 minutes wall clock

REQUIRED OUTPUTS (print all of these, even if ugly):
  [ ] 5 complete raw outputs per arm, verbatim, unedited
  [ ] per-arm parse-success rate
  [ ] per-arm mean generated length and std
  [ ] per-arm share hitting the token ceiling
  [ ] the 2x2 (or 2x3) contingency table
  [ ] the deciding statistic, whatever it is

DO NOT DO during the pilot:
  [ ] no hyperparameter tuning
  [ ] no additional arms
  [ ] no significance testing
  [ ] no figure production
  [ ] no writing of the methods section

DECISION (must be recorded, in writing):
  [ ] DESIGN OK -> pre-register and scale up
  [ ] METRIC BROKEN -> fix the instrument (parse/classifier), rerun pilot
  [ ] BUDGET TOO SMALL -> increase and rerun pilot (this is F2, not a failure)
  [ ] CONTRAST ABSENT -> the design does not separate the hypotheses. Reshape or kill.
  [ ] QUESTION MOVED -> write the new phenomenon statement and restart from §7
```

**The requirement to print raw outputs verbatim is not cosmetic.** It is the only way to see the failure modes you did not anticipate — the "neither" answer, the hybrid computation, the spontaneous abstention. **Every one of your best findings came from reading raw outputs, not from a table.** **[L2]**

## 21.3 The pilot-to-main gate

**[L3]** Do not start the main run until every box is checked. This is the gate.

```text
GATE: PILOT -> MAIN RUN

Design
  [ ] The deciding statistic is computed and it moves in a direction
  [ ] The contingency table is not degenerate
  [ ] A third category (ambiguous/neither) is defined and its rate is reported

Instrument
  [ ] Parse success >= 90% on a gold subset of >= 30 items
  [ ] Classifier agreement validated (kappa reported) on >= 30 hand-labelled items
  [ ] Truncation below 10% per arm at the chosen budget
  [ ] Control-check table (§19.5) fully green

Specification
  [ ] Pre-registration file written and saved, with a timestamp
  [ ] Kill rules and abort criteria recorded
  [ ] Deviation protocol recorded
  [ ] Failure taxonomy (F1-F6) recorded, with a fallback per asset

Scale
  [ ] Compute estimate for the main run is < 6 GPU-hours
  [ ] Checkpointing / resumption works (kill it mid-run and restart)
  [ ] Output artifacts have a naming scheme and a version number
  [ ] Raw data is written before any aggregation

Re-verification
  [ ] Search-ladder rungs 11 & 12 re-run within the last 7 days
```

**The last box saves you from a late pre-emption.** It takes 20 minutes and it is the cheapest insurance in the process. **[L3]**

## 21.4 The harness requirements you will regret skipping

**[L2 / L3]** Your harness lineage (v1 → v2 → v3) shows what actually matters. Derived from what v3 had to add:

| Requirement | Why | Failure it prevents |
| :--- | :--- | :--- |
| **Checkpointing every K items** | Colab sessions die | Losing a 100-minute run |
| **Resume from checkpoint** | Same | Re-running from scratch |
| **Per-group token budgets** | Different arms need different budgets | Universal truncation (the v1/v2 bug) |
| **A strict output contract with a delimiter** | Deterministic parsing | Parse failures scored as model failures |
| **Deterministic parsing, no regex guessing** | Reproducibility | Different scores on re-run |
| **Record everything, aggregate later** | You cannot re-run what you did not save | Re-running just to compute a new statistic |
| **Separate raw output from derived labels** | You will change the classifier | Losing the ability to relabel |
| **Warm-up / JIT once, not per batch** | Throughput | 9× slower runs **[L2 — your v2→v3 optimisation]** |
| **Same dtype/precision throughout** | Comparability | Silent precision-change confounds |

**The most valuable single property is that raw outputs are stored verbatim and separately from labels.** With raw outputs you can re-derive any metric later. Without them, every metric change costs a full re-run. **Your v3.0 results file did this correctly, and it is why you could re-analyse without re-running.** **[L2]**

## 21.5 Ordering: what to run first

**[L1 / L3]** When you scale up, run in this order. Each step is cheaper than the next and can abort the run.

```text
1. SMOKE      : 3 items x all arms. Does it execute end to end?        (~2 min)
2. SMALL      : 20 items x all arms. Does the contrast appear?         (~10 min)
3. STRATIFIED : 100 items, spanning strata. Is the effect homogeneous?  (~30 min)
4. FULL       : all items x all arms.                                  (~1-2 h)
5. SECONDARY  : robustness / second model / ablations. Only if 4 worked.
```

**Never skip step 3.** The stratified run is what reveals that your effect is confined to one task family, one difficulty band, or one sub-population — which is often the most important and most publishable finding in the whole project. **[L3]**

---

# 22. Handling Unexpected and Negative Results

## 22.1 The taxonomy of surprise

**[L1 — Established practice]** "Unexpected result" is not one thing. There are five distinct categories, and **they require completely different responses.** Conflating them is why unexpected results cause panic instead of progress.

| Category | What you observe | What it usually means | Response |
| :--- | :--- | :--- | :--- |
| **U1 Instrument failure** | The numbers are impossible, or outputs are malformed | Your harness, parser, or budget is broken | **F1/F2** — fix and rerun. Do not interpret. |
| **U2 Absent effect** | Both arms behave identically | Either H0 is true, or the design has no power, or the manipulation is too weak | Run the power/positive-control check, then decide |
| **U3 Reversed effect** | The arms differ, but backwards | Your theory's mechanism is wrong, or a hidden variable dominates | Investigate; this is often the best possible outcome |
| **U4 Unexpected subgroup** | The aggregate is one thing, a stratum is the opposite | A boundary condition exists | Report it as the headline; check it replicates |
| **U5 Unanticipated behaviour** | The model does something your categories do not contain | The construct is mis-specified | **This is a discovery.** Rewrite the phenomenon statement (§6.4). |

**The decisive question for every surprise: is this F1–F3 (fixable machinery) or F4–F6 (about the science)?** Your own Phase-3 failure taxonomy gives you the instrument. Apply it mechanically and the panic disappears. **[L2 / L3]**

## 22.2 When a negative result is valuable

**[L1]** A negative result is valuable when **all four** of these hold:

1. **The experiment had power.** You can show the design could have detected the effect if it existed — either with a power calculation, a positive control, or a much larger observed effect in a related condition.
2. **The measurement was validated.** Parse success high; the metric's construct validity checked.
3. **The intervention actually did something.** A *manipulation check*: you can show the treatment changed *some* observable, even if not the one you predicted.
4. **There is a named belief that the result bears on.** You can write: *"this weakens the claim in [paper] that [claim]."*

**A negative result missing (1) or (2) is not a negative result. It is an experiment failure.** And an experiment failure is not publishable — it is repairable. **[L1]**

**The distinction in one line:**

> **A negative result says "the world is not like that." An experiment failure says "my instrument was broken."**
> The first is knowledge. The second is a bug.

## 22.3 Positive controls: the antidote to ambiguous nulls

**[L1 / SYNTHESIS]** This is the single most under-used technique in undergraduate AI/ML research. When you get a null, you cannot tell whether your theory is wrong or your design is dull. The fix is a **positive control**: a condition in the same experiment where you *know* the effect must appear.

**Three kinds of positive control:**

| Type | Example | What it proves |
| :--- | :--- | :--- |
| **Known-effect manipulation** | A manipulation from the literature known to shift the outcome | Your harness can detect *some* effect of that magnitude |
| **Ceiling condition** | An extreme version of your treatment (e.g. forced prefill of the answer) | Your measurement responds when the effect is large |
| **Sensitivity check** | Artificially inject the effect into the data and confirm your statistic recovers it | Your analysis pipeline is not degenerate |

**[L2]** Your frozen project's design contains a natural positive control and it is worth naming: the **forced-rationale prefill arm**. That arm forces the model to commit to a specific rationale, and its measured divergence rate is substantially lower than the natural verbalization effect. **That contrast is exactly what a positive control is for**: it shows the measurement *can* move a lot, and it shows the natural effect is not merely an artifact of the measurement being unstable. **Foreground this as a control, not just as a secondary result.**

**[L3]** For your future pilots: **always include one condition where the effect must appear.** It converts every null into either a finding or a bug report.

## 22.4 The surprise-response protocol

**[L3]** Run this whenever a result contradicts your expectation. Thirty minutes; prevents both panic and premature conclusions.

```text
SURPRISE RESPONSE PROTOCOL                          <date>

1. WRITE THE SURPRISE
   "I expected ____. I observed ____."

2. CLASSIFY (U1-U5 from §22.1)
   U1 instrument / U2 absent / U3 reversed / U4 subgroup / U5 unanticipated

3. IF U1 -> apply F1-F6. Fix and rerun. STOP HERE. Do not interpret.

4. IF U2 (absent effect) -> check the three null-explanations:
   [ ] POWER: could this design have detected the effect? (positive-control result)
   [ ] MANIPULATION: did the treatment change ANYTHING? (manipulation check)
   [ ] WEAKNESS: was the treatment strong enough? (compare to the ceiling condition)
   If all three check out -> accept the null and write the negative-result paragraph.

5. IF U3 or U4 -> investigate before concluding:
   [ ] Is there a stratum where the direction is the predicted one?
   [ ] Is the reversal an artifact of one sub-population? (check N per cell)
   [ ] Does the reversal replicate on a fresh sample of the same stratum?
   [ ] Is the reversal a *published* boundary condition? (search for it)

6. IF U5 -> this is the most valuable outcome:
   [ ] Print the raw outputs verbatim
   [ ] Name the unanticipated category
   [ ] Rewrite the phenomenon statement (§6.4) with the new category
   [ ] Re-derive whether the original metric is still meaningful
   [ ] Update the question ledger: the question has MOVED, not failed

7. RECORD in the research log:
   surprise, classification, decision, evidence command, date
```

**Step 6 is where your project's strongest single finding came from.** The discovery that the model frequently produces an answer matching *neither* stored answer came from reading raw outputs, not from a hypothesis. It invalidated the original metric and produced a better thesis. **Treat U5 as the goal state, not as a problem.** **[L2]**

## 22.5 How a failed hypothesis becomes the contribution

**[L1]** This is a skill with a mechanical form. Take the failed hypothesis and answer three questions:

1. **What did the failed hypothesis assume that turned out to be false?** (Name the assumption.)
2. **What does the data support instead?** (Name the alternative.)
3. **What published claim, method, or evaluation depends on the false assumption?** (Name the recipient.)

If you can answer all three, **the failed hypothesis is a better contribution than the original would have been**, because it corrects a live belief rather than confirming an expected one.

**The mechanical template:**

```text
FAILED HYPOTHESIS:     "X causes Y."
REVERSED CONTRIBUTION: "X is a smaller part of Y than assumed; Z accounts for a
                        substantial share. This matters because [published method/claim]
                        assumes X is dominant."
```

**Worked example [L2 / SYNTHESIS]:** a published line of work treats raw attention mass on visual tokens as the quantity to defend, and builds training interventions that reward keeping that mass high. If a matched-control study showed that a large share of the observed mass decline is attributable to sequence length and softmax normalisation rather than to a cognitive process, then **those interventions are optimising a partly mechanical quantity.** That is a correction with a named recipient — and it does not require the intervention to fail, only the assumption to be shown partly wrong.

## 22.6 Writing a negative result honestly

**[L1 / L3]** Five rules. Follow them and the result reads as rigorous; break them and it reads as an excuse.

| Rule | Do | Don't |
| :--- | :--- | :--- |
| **State the positive claim you tested, first** | "We tested whether [specific claim]." | Lead with the null |
| **Report power / positive control before the null** | "Our design detects a known effect of size δ." | Report only the null and hope |
| **Use equivalence language properly** | "Equivalent within a pre-specified bound of Δ." | "No significant difference (p = 0.4)" |
| **Name the recipient belief** | "This constrains [paper]'s mechanism claim." | "This may be useful for future work" |
| **Separate what you showed from what you did not** | "We show X under condition C; we do not speak to condition D." | Imply generality |

**Structural template for the negative-result paragraph:**

```text
We tested whether <intervention> <causes / improves / changes> <outcome> relative to
<matched control>. Across <N items / conditions / models>, the two conditions produced
<equivalent / indistinguishable> outcomes (<test>, equivalence bound = <bound>, <statistic>).
This contrasts with <the expectation set by prior work / our H1>.
A positive control in the same experiment (<which condition>) produced a
<large> effect, indicating the design had adequate sensitivity to detect an effect of that
kind. These results constrain <specific published claim> by showing that
<the mechanism / the improvement> is not attributable to <the proposed cause> in
<the tested setting>. We do not speak to <the untested setting>.
```

**Every clause is doing work.** The positive-control sentence is what makes it a result rather than an apology. Without it, the reviewer's first question — *"maybe your method just cannot detect anything"* — is unanswerable. **[L3]**

## 22.7 The rule about not falling in love with a result

**[L3]** One behavioural rule, because it is the failure mode that would most damage your current thesis: **the moment a number looks good is the moment to attack it hardest — not the moment to stop.**

When a result is *stronger than you expected*:

- Re-run it on a fresh sample of the same design. A large effect should reappear.
- Check whether the effect is concentrated in a subset (a stratum that happened to be easy).
- Check the denominator. A large effect computed on a small *scored* subset is not a large effect.
- Check the control arms for anomalies. If the *control* moved, the effect is a harness shift.
- Ask: *"what would make this effect appear artificially large?"* — then check that thing.

**A result that survives this is worth far more than a result that was never attacked.** And a result that does not survive is much better discovered in week 3 than in a viva. **[L3]**

## 22.8 The five most common negative-result traps

**[L1 / L2]**

| Trap | What it looks like | Fix |
| :--- | :--- | :--- |
| **The underpowered null** | N=20, no effect, concluded "the effect does not exist" | Report the smallest effect the design could have detected; or run the positive control |
| **The broken-instrument null** | Parse rate 55%, no effect | Fix the instrument first; a broken instrument cannot produce a negative result |
| **The wrong-construct null** | Metric does not move, but the raw outputs clearly differ | The metric is wrong, not the phenomenon. Relabel from raw outputs |
| **The saturated null** | One cell holds everything; no variance to explain | Redesign the stimulus set; the phenomenon is saturated in this population |
| **The laundry-list null** | "We tried many things and none worked" | Pick the one that matters; re-design it properly; report the others as exploratory |

---

# 23. Iterating and Changing the Research Question

## 23.1 The decision tree when evidence arrives

**[L1 — Established practice]** Evidence arrives and your question no longer fits it. You have **seven** options, and they are not interchangeable. Choosing the wrong one is the most expensive mistake in research execution.

```text
                    NEW EVIDENCE ARRIVES
                            |
        +-------------------+-------------------+
        |                                       |
  Question still fits?                    Question does not fit?
        |                                       |
   [PROCEED]              +---------+---------+---------+---------+---------+
                          |         |         |         |         |         |
                      BROADEN    NARROW   REPLACE    ADD A    CHANGE    CHANGE
                                                    CONTROL  THE METRIC THE DATA
                          |         |         |         |         |         |
                          +---------+---------+---------+---------+---------+
                                              |
                                        (last resort)
                                           ABANDON
```

## 23.2 Choosing the right response

**[L3]** The decision logic, with the trigger for each.

| Response | Trigger | What it looks like | Risk |
| :--- | :--- | :--- | :--- |
| **PROCEED** | The evidence supports the question as stated | Run the main experiment | Low |
| **BROADEN** | The effect is real but confined; you suspect a family of related conditions | Add a second task family / model family / dataset | Dilution; you may lose focus |
| **NARROW** | The effect is real only in a specific condition | Restrict the claim to that condition and *name it in the title* | Looks incremental unless the boundary is interesting |
| **REPLACE** | The original question was answered, but the data raises a better one | Rewrite the question around what you actually observed | Loses prior literature grounding; re-run §12 |
| **ADD A CONTROL** | The effect may be produced by an uncontrolled variable | Add the missing arm | Cost; may collapse the effect |
| **CHANGE THE METRIC** | The metric does not track your construct | Define a new metric and validate it | Reputational risk if selective; must be re-derived from raw data |
| **CHANGE THE DATA** | The population cannot support the claim | Swap dataset or stimulus construction | Loses comparability with the closest work |
| **ABANDON** | The design cannot be repaired within budget | Kill and record | Sunk-cost resistance |

**The critical discipline: choose exactly one.** The failure mode is doing several at once — adding a control *and* changing the metric *and* broadening the population — after which nothing is interpretable. **[L1]**

**A rule that prevents the worst version of this [L3]:** *never change the primary metric and the population in the same iteration.* If you must do both, run one pilot per change separately so the effect can be attributed.

## 23.3 The evidence-to-decision table

**[L3]** The operational form of §23.2 for the situations you will actually hit.

| Evidence | Correct response | Correct framing of the new question |
| :--- | :--- | :--- |
| **Baseline fails** (the model cannot do the task at all) | NARROW or CHANGE THE DATA | "Under what condition *does* the model perform the task, and does the effect appear there?" — or choose a task where performance sits mid-range |
| **Dataset unsuitable** (no variance, or the needed property is absent) | CHANGE THE DATA (F3) | Use the pre-registered fallback; if none, rebuild the stimulus differently (that rebuild is itself a validity test) |
| **Effect disappears** in the larger sample | ADD A CONTROL; if that fails, ABANDON | "Was the pilot effect a small-sample artifact?" becomes a reportable methodological finding |
| **Effect appears only in one model** | NARROW | "The effect is checkpoint-specific" — a genuine limitation; then test a second family to see whether it is *architecture*-specific |
| **Control reproduces the result** (placebo does the same thing) | REPLACE the interpretation | "The effect is attributable to X, not to my hypothesised mechanism." **This is a result, not a failure** — it is exactly the correction a control exists to produce |
| **Unexpected subgroup behaviour** | NARROW into a BOUNDARY question | Promote the subgroup to the headline; check it replicates on a fresh sample |
| **Intervention works for the wrong reason** | ADD A CONTROL | "Which component of the intervention is doing the work?" → ablation |
| **Result contradicts the hypothesis** | REPLACE or BROADEN | Apply §22.5. What assumption was false, and who depends on it? |

## 23.4 What "the question changed" actually looks like

**[L2]** Your own record contains a clean, well-documented instance. It is worth studying closely.

```text
BEFORE THE PILOT:
  "Does conflict verbalization shift source arbitration?"   [a preference/source question]

WHAT THE PILOT SHOWED:
  - 85% of direct-arm outputs matched NEITHER stored answer -> the model computes its
    own answer; it does not "select" between two
  - 25% of verbalization outputs legitimately abstained after detecting the conflict
  - free-form lengths ranged 12-240 tokens -> the comparison was confounded by length
  - few-shot demonstrations biased arbitration (treatment contamination)

AFTER THE PILOT:
  "Does conflict verbalization enable deliberative problem selection and
   conflict-aware abstention?"   [a mode/capability question, with abstention as a
                                   first-class outcome and a matched-budget control]
```

**Three things to notice:**

1. **The change was triggered by raw-output inspection, not by a statistic.** No p-value was needed.
2. **The new question is strictly better**, because it accounts for behaviour the old metric literally could not represent.
3. **The change was recorded as an architectural response** — "eliminate few-shot demonstrations; strict output contract; length-matched neutral placebo; entity-based transition classifier". **That is the right way to record a question change: as a design decision with reasons.**

**[L3]** What was missing was **speed**. That reframing cost two pilot iterations plus a redesigned analysis pipeline. Under the §21.2 protocol it is a single morning. **This is the concrete, repeatable saving available to you.**

## 23.5 When to abandon

**[L1 / L3]** Abandon only when **all three** hold:

1. The design cannot be repaired within budget, and you have identified a *structural* problem (not a bug).
2. Every repair you can imagine either breaks the control, exceeds the compute budget, or requires an asset you cannot obtain.
3. You can write the negative-result paragraph *for the abandonment itself*: *"the hypothesis is not testable under constraints X, Y, Z because …"* — which is itself a methodological contribution if X, Y, Z are general.

**If only (1) and (2) hold, do not abandon — NARROW.** Abandoning is the most expensive option and should be the rarest.

**[L3]** When you do abandon: **write the kill record (§16.5), file the reusable artifacts** (harness code, failure taxonomy, pilot observations), **and note the conditions under which you would reopen it.** Your abandoned work is not lost, it is *parked* — and every one of your parked dossiers contains material that was later reused.

---

# 24. Freezing the Research Question

## 24.1 What "frozen" means

**[L1 — Established practice]** Freezing is not a feeling of confidence. It is a **decision with a date, a set of fixed parameters, and a defined unfreeze condition.**

```text
FROZEN means:
  - the question is written in one sentence, in one file
  - the hypotheses and their patterns are written down
  - the primary metric is named and its formula fixed
  - the population, model, and arms are fixed
  - the analysis plan is pre-registered
  - no new arms, metrics, or populations will be added to the PRIMARY analysis

FROZEN does NOT mean:
  - you stop exploring (exploration moves to the ledger as future work)
  - you can never change anything (deviations are allowed, and recorded)
  - you stop reading (you keep watching for pre-emption)
```

**The most common misunderstanding:** freezing is not the end of thinking. It is the end of *changing the primary analysis while looking at the results.* That property is what makes a result defensible. **[L1]**

## 24.2 The freeze criteria

**[L3]** Freeze when all of these are true. Do not freeze earlier (you will freeze something underspecified); do not wait for more (you will never freeze).

```text
FREEZE CHECKLIST

[ ] The question fits in ONE sentence and contains no "and"
[ ] H1 and H0 each have a written PREDICTION and a written FALSIFIER
[ ] The primary metric is named, formula written, and validated (kappa or parse rate reported)
[ ] The pilot shows a non-degenerate contrast
[ ] The control-check table (§19.5) is fully green
[ ] The closest work is named, with its unperformed experiment stated
[ ] Search-ladder rungs 11 and 12 were re-run within 7 days and found nothing new
[ ] The pre-registration file exists with a timestamp
[ ] The compute estimate for the main run is < 6 GPU-hours
[ ] The negative-result paragraph is already written
[ ] I can state what would make me UNFREEZE, in one sentence
```

**The second-to-last item is the sharpest test in the list.** If you cannot write the negative-result paragraph *before* running, your design is not frozen — it is unfinished. **[L3]**

## 24.3 The unfreeze protocol

**[L1 / L3]** Freezing is not permanent, but unfreezing is expensive and must be governed. Unfreeze only for one of three reasons:

| Reason | Evidence required | Cost |
| :--- | :--- | :--- |
| **Pre-emption** | A paper (verified, primary source) performing your contrast in a comparable setting | Rewrite the contribution as extension/arbitration; do not restart |
| **Structural infeasibility** | A measured failure of an asset or the compute envelope, after the prescribed fix | Apply a §23.2 response; usually NARROW |
| **New evidence from your own runs** | A pilot or stratified run showing the construct is mis-specified | Apply §23.4; this is the legitimate and most valuable unfreeze |

**And a fourth, which is not a reason:** *"I found a more interesting paper and want to work on that instead."* That is the pattern that produced your five weeks of wandering. Park it in the question ledger as a one-line card, and re-verify it after the current freeze completes. **Your own reconsideration protocol — thirteen items of written evidence before re-opening a parked field — is exactly the right instrument. Apply it to the temptation to unfreeze, not only to parked fields.** **[L2]**

## 24.4 The frozen artifact

**[L3]** Freezing produces exactly one short file. Not a large document. One page.

```text
FROZEN SPECIFICATION — <project>          FROZEN ON: <date>   UNFROZEN ON: (none)

QUESTION (one sentence):
  ____

H1: <mechanism>   PREDICTION: ____   FALSIFIER: ____
H0: <mechanism>   PREDICTION: ____   FALSIFIER: ____

PRIMARY METRIC: ____   (formula: ____)   (validated by: ____, rate/kappa = ____)
POPULATION: <dataset id> <split> N=____   exclusions: ____
MODEL: <id>@<revision> <precision>   decoding: ____
ARMS: A=____  B=____  C=____   (only intended difference per arm: ____)
CONTROLS: ____
PRIMARY TEST: ____   EQUIVALENCE BOUND (if any): ____

CLOSEST WORK: <id>   WHAT IT LEAVES UNPERFORMED: ____
RE-VERIFIED (rungs 11/12) ON: <date>

NEGATIVE-RESULT PARAGRAPH (written in advance):
  ____

WHAT WOULD UNFREEZE THIS: ____
```

**That is the whole artifact.** If you can produce this page, you have a thesis. If you cannot, you have a direction. **[L3]**

---

# 25. End-to-End Thesis Execution

## 25.1 The reasoning behind each transition

**[L1]** The pipeline below is the standard one. What matters is **why** each transition exists — the reason is what tells you what to do when it goes wrong.

```text
Question  ──► Hypotheses  ──► Variables ──► Controls ──► Dataset ──► Baseline
   │                                                                    │
   └──────────────(everything below feeds back up if it breaks)──────────┘
                                                                        │
   Evaluation ◄── Pilot ◄── Harness ◄── Logging ◄── Metric ◄───────────┘
        │
        ▼
   Main experiment ──► Ablations ──► Robustness ──► Analysis
                                                      │
                                                      ▼
                                    Interpretation ──► Contribution
```

| Transition | The reasoning | What breaks if skipped |
| :--- | :--- | :--- |
| **Question → Hypotheses** | A question is not testable until it predicts two different observations | You will design an experiment with no decision rule |
| **Hypotheses → Variables** | The prediction tells you *what to measure* and *what to vary* | You measure everything and decide nothing |
| **Variables → Controls** | A variable's effect is only visible against a fixed background | Every result is confounded |
| **Controls → Dataset** | The control determines which items the contrast is meaningful on | You use the full dataset when you need a stratum |
| **Dataset → Baseline** | The baseline tells you whether there is an effect at all | You interpret noise |
| **Baseline → Metric** | The baseline's behaviour reveals what the metric must be sensitive to | The metric saturates |
| **Metric → Logging** | You must log the primitives the metric is derived from | You re-run to compute a new statistic |
| **Logging → Harness** | The logging requirements dictate the harness structure | The harness cannot produce the artifact you need |
| **Harness → Pilot** | The pilot tests the harness on the smallest case | You discover bugs at full scale |
| **Pilot → Main** | The pilot validates the design, not the result | The main run answers the wrong question |
| **Main → Ablations** | The main run shows *that*; ablations show *which component* | The contribution is a black box |
| **Ablations → Robustness** | The effect is only credible if it survives perturbation | A single-configuration result |
| **Robustness → Analysis** | Only now do you choose statistics | Post-hoc metric selection |
| **Analysis → Interpretation** | Interpretation requires the analysis to be fixed | Confirmation bias |
| **Interpretation → Contribution** | A contribution names who should believe differently | The thesis has no claim |

**Print that table. When a transition goes wrong, it tells you which one to go back to.** **[L3]**

## 25.2 Design-before vs design-flexible

**[L1 / L3]** A common and expensive error: freezing everything at the start, so the pipeline cannot adapt; or freezing nothing, so the pipeline drifts.

**The rule:** design the *invariants* up front; keep the *presentation layer* flexible.

| Component | Design before implementation? | Why |
| :--- | :--- | :--- |
| **The question and hypotheses** | **YES — frozen** | Changing them after seeing data is the cardinal sin |
| **The primary metric's definition** | **YES — frozen** | Post-hoc metric choice inflates results |
| **Raw-output logging schema** | **YES — frozen** | You will need to re-derive; log the primitives |
| **Row identity / item IDs / arm labels** | **YES — frozen** | Joins and pairing depend on it |
| **Preprocessing and pairing rules** | **YES — frozen** | Determines comparability across arms |
| **Model and decoding configuration** | **YES — frozen** | Determines comparability across runs |
| **Checkpoint/resume behaviour** | **YES — frozen** | A crashed run must be resumable identically |
| **Analysis code structure** | **YES — frozen (as a plan)** | Prevents analysis drift |
| **Number of arms** | **Mostly frozen** | Add an arm only as a *recorded deviation* before analysis |
| **Visualisation choices** | Flexible | Presentation, not evidence |
| **Auxiliary statistics** | Flexible, labelled exploratory | They cannot become primary post hoc |
| **Additional datasets/models (secondary)** | Flexible | Kept out of the primary claim |
| **Failure taxonomy categories for error analysis** | Flexible | You will discover categories mid-analysis |
| **Appendix content** | Flexible | Written last |

**The invariant that matters most: the raw logging schema.** Everything else can be re-derived if you logged the primitives. If you logged only the labels, nothing can be recovered. **[L3]**

## 25.3 Reproducibility minimum

**[L1]** The minimum bar for a defensible undergraduate thesis:

```text
REPRODUCIBILITY CHECKLIST
[ ] Repository with a README that runs the experiment end to end
[ ] Pinned dependency versions (requirements.txt with == pins, or a lockfile)
[ ] Exact model identifier and revision (the commit hash, not just the name)
[ ] Dataset identifier, split name, and any filtering applied
[ ] All prompts in the repo as templates, not inline strings
[ ] Random seeds recorded (and a statement of what is deterministic vs stochastic)
[ ] One command reproduces one table or figure (or a documented mapping table -> command)
[ ] Hardware and software recorded: GPU, driver, CUDA, PyTorch, Transformers
[ ] Raw outputs archived (with a pointer, not necessarily in the repo)
[ ] A "what is NOT reproducible" statement (e.g. API-only frontier comparisons)
```

**The last item is the one that builds credibility.** Stating honestly what cannot be reproduced is a mark of rigour, not a weakness. **[L3]**

---

# 26. From Thesis to Paper

## 26.1 The compression problem

**[L1 — Established practice]** A thesis and a paper are different genres answering different questions.

| | Thesis | Paper |
| :--- | :--- | :--- |
| **Answers** | "Did the candidate understand and execute research?" | "What should the field now believe?" |
| **Audience** | Examiners, some of whom know the area less well than you | Reviewers who know the area at least as well as you |
| **Structure** | Chapters: intro, literature, method, results, discussion | Sections: intro, related work, method, results, discussion |
| **Length** | 40–120 pages | 4–9 pages |
| **What earns credit** | Comprehensiveness, correctness, honest limitations, clear reasoning | One claim, well-evidenced, tied to prior work |
| **Failure mode** | Being too thin | Being unfocused |

**The critical fact: the paper is not a compressed thesis.** It is a compressed *contribution*. Anything that does not serve the contribution is removed — including material your examiners valued. **[L1]**

## 26.2 Finding the central claim

**[L1 / L3]** Write it in one sentence, with a fixed grammatical form:

```text
"In [setting], [intervention] changes / does not change [outcome] relative to
 [matched control], implying that [specific published belief] is [supported / needs revision]."
```

**Worked examples from your own material:**

```text
[Positive outcome version]
  "In paired image/text numeric conflicts with a small open-weight VLM, explicitly
   verbalizing the conflict shifts the model's attempted problem relative to a
   length-matched neutral description, implying that the explanation is a causal
   driver of source arbitration rather than a post-hoc decoration."

[Negative outcome version]
  "In paired image/text numeric conflicts with a small open-weight VLM, explicitly
   verbalizing the conflict produces output distributions statistically equivalent to a
   length-matched neutral description, implying that reported gains from chain-of-thought
   prompting in this setting are attributable to additional test-time computation rather
   than to the content of the explanation."
```

**Both versions name a belief that changes.** That is what makes them claims rather than descriptions.

**Test:** can you state it in one sentence, without "and"? If your claim needs "and", you have two claims and should choose one for the paper. **[L3]**

## 26.3 What belongs in the paper

**[L1]** Sort every piece of content into one of three buckets.

| Bucket | Content | Destination |
| :--- | :--- | :--- |
| **Core** | The phenomenon, the rival explanations, the contrast, the controls, the primary result, the effect size, the limitations | **Paper** |
| **Supporting** | The ablation showing which component does the work; the boundary result; ambiguity/parse rates; the robustness check | **Paper (short) or appendix** |
| **Remove** | Exploration history; every rejected candidate; the full field map; implementation war stories; the harness optimisation narrative; redundant tables; anything included for the examiners | **Thesis only, or nothing** |

**With respect to your own corpus [L2 / L3]:**

- **Keep:** the matched-budget design and its justification; the state-transition framing; per-arm ambiguity and truncation rates; the sensitivity analysis; the closest-work comparison; the negative-result paragraph.
- **Remove from a paper:** the four-candidate decision audit; the parked-field dossiers; the harness version lineage; the eight-phase execution roadmap; the defence FAQ.
- **Move to appendix:** full prompt templates; the full contingency table; per-stratum breakdowns; the hyperparameter table.
- **Rebuild for the paper:** the introduction (a paper introduction states the claim by paragraph two) and the related work (organised around *your* claim, not around the field).

<!--APPEND-HERE-->














































