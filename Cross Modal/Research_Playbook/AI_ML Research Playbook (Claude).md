
# AI/ML Research Playbook

### Reconstructing the End-to-End Working Process of an Experienced Researcher

A reference document, not a thesis-topic generator. It is meant to outlast any single project. Claims are marked **\[V\]** verified against a cited source, **\[SI\]** strong inference from methodology literature and observed research practice, or **\[PR\]** practical recommendation (my synthesis, not an established law). Where a claim is unmarked inside a worked example, treat it as narrative illustration, not doctrine.

---

## 1. Executive Summary

Research is not a checklist. It is an **adaptive evidence-building loop**: you form a belief about why something happens, you design the cheapest test that could prove the belief wrong, and you let the result — not your attachment to the idea — decide what happens next. Most of what separates a productive researcher from someone who wanders for a year is not intelligence. It is:

1. Knowing what "enough literature" looks like before acting **\[SI\]**
2. Turning vague interest into a falsifiable question quickly **\[SI\]**
3. Designing a minimum experiment that can discriminate between two explanations, instead of building a whole system first **\[SI\]**
4. Being willing to let a surprising result overturn the plan **\[SI\]**
5. Reading your own results the way a hostile reviewer would, before anyone else does **\[V\]** (this is the explicit purpose of checklists such as the NeurIPS Paper Checklist and reproducibility program) \[ref: NeurIPS Paper Checklist Guidelines, neurips.cc/public/guides/PaperChecklist\]

This document reconstructs the reasoning inside each of those five points.

---

## 2. What Research Actually Is

Engineering asks: *does it work?* Research asks: *why, and under what conditions would it stop working, and how do I know my explanation is the right one and not just a story that fits?*

A result is engineering output until it is attached to a **claim about a mechanism or a limit** that other people could test and potentially falsify. "We built a system that gets 91% accuracy" is an artifact. "We show that the 91% accuracy is driven by a positional bias in the dataset rather than semantic understanding, and that removing the bias drops accuracy to 54%" is research — it makes a falsifiable claim, and it survives an obvious attack (is the drop just noise? did you use a matched control?).

This distinction matters because undergraduate projects fail most often not from lack of skill but from stopping at the artifact stage and calling it a contribution. **\[SI\]**

---

## 3. The Researcher's Terminology Ladder

Beginners conflate these. Experienced researchers move fluidly between them because each level demands different evidence.


| Level                | Definition                                                                           | AI/ML example                                                                                                             |
| ---------------------- | -------------------------------------------------------------------------------------- | --------------------------------------------------------------------------------------------------------------------------- |
| Field                | A broad discipline                                                                   | Machine learning                                                                                                          |
| Area / subfield      | A recognized cluster of methods and venues                                           | Vision-language models                                                                                                    |
| Research territory   | A more specific zone within a subfield where active work is happening                | Hallucination in multimodal LLMs                                                                                          |
| Phenomenon           | A recurring, observable behavior                                                     | VLMs answer questions about objects that are not in the image                                                             |
| Observation          | A single instance of the phenomenon you personally noticed or reproduced             | Your model claims a "red car" is present in an image with no car                                                          |
| Existing explanation | What the literature currently says causes the phenomenon                             | "Language priors override visual evidence"                                                                                |
| Assumption           | Something the existing explanation depends on but hasn't directly tested             | That the failure is visual, not linguistic, in origin                                                                     |
| Tension / gap        | A place where evidence is missing, contradictory, or the explanation is under-tested | No paper has held the language constant while manipulating only the image to see if the hallucination persists            |
| Research question    | A specific, answerable question that targets the tension                             | "Does object hallucination persist when the image is edited to remove the object, holding the question text fixed?"       |
| Hypothesis           | A specific, falsifiable predicted answer                                             | "Hallucination rate will not significantly drop, because the cause is a language-side prior, not missing visual evidence" |
| Experiment           | The concrete test of the hypothesis                                                  | Counterfactual image-editing experiment with matched questions                                                            |
| Contribution         | What the evidence, once gathered, adds to the field's knowledge                      | A causal decomposition of hallucination into visual vs. linguistic sources                                                |

Beginners usually try to skip from "phenomenon" straight to "research question," which produces vague questions like "why do VLMs hallucinate?" That is a territory, not a question. A question must specify what varies, what is held constant, and what result would count as support versus refutation. **\[SI\]**

---

## 4. Entering an Unfamiliar Field (Orientation)

The goal of orientation is not mastery. It is enough situational awareness to recognize what counts as new, contested, or solved. Concretely, before touching a research question, an experienced researcher typically establishes:

- **Vocabulary**: the 15-30 terms that recur across abstracts in the area. Skipping this causes wasted search queries later.
- **Canonical papers**: the 3-8 papers everyone in the subfield cites as foundational. Found by looking at what recent papers' related-work sections cite in their first two paragraphs, not by searching "best papers in X."
- **Benchmarks and datasets**: what the community currently measures progress against, and what those benchmarks actually test versus claim to test.
- **Active tensions**: what recent papers (last 12-18 months) argue about with each other. This is usually visible in related-work sections that say "unlike X, we..." or "contrary to the claims of Y..."
- **What the community currently cares about**: workshop CFPs, recent survey papers, and the "future work" and "limitations" sections of 5-10 recent papers, read specifically for what they flag as unresolved.

**Common beginner mistake:** trying to read a subfield chronologically from its origin. **\[PR\]** Read backward from 2-3 strong recent papers instead: their related work gives you the field's own map of itself, curated by people who had to justify their framing to reviewers. This is faster and self-correcting, because if you misread the field, your first attempted research question will get killed quickly in section 11 below and you loop back.

**Stopping rule for orientation:** stop reading broadly once you can (a) state the central tension of the territory in two sentences, (b) name the closest 2-3 papers, and (c) predict roughly what a domain expert would say is still open. If you cannot do this after roughly 15-25 papers skimmed at the first-pass level (see section 8), the territory is probably still too broad; narrow it and re-orient. **\[PR\]**

---

## 5. Research Question Funnel

A compact, reusable filter. Each arrow is a real decision point, not a formality.

```
What field interests me?
        ↓  (pick based on curiosity + feasibility, not hype)
What is actually happening there right now?
        ↓  (orientation, section 4)
What specific phenomenon is interesting?
        ↓  (must be observable/reproducible by you, not just described in a paper)
What do current papers claim explains it?
        ↓  (the existing explanation — write it down in one sentence)
What remains uncertain about that explanation?
        ↓  (an assumption nobody tested, a result that doesn't fully fit, a contradiction)
What competing explanations exist?
        ↓  (if there is only one explanation and it's untested, that IS your gap)
What single result would distinguish between them?
        ↓  (this is your research question, stated as a discriminator)
What is the smallest experiment that could produce that result?
        ↓  (section 13, minimum discriminating experiment)
What result would change my belief, and what would not?
        ↓  (pre-register this to yourself before running it — prevents post-hoc rationalization)
```

The funnel fails quietly when someone answers "what remains uncertain" with "nobody has tried it yet" instead of naming an actual unresolved tension. Novelty-by-absence is a weak foundation; see section 11.

---

## 6. How Research Questions Are Actually Discovered

Real questions come from a small number of recurring mechanisms. Recognizing which one you're in tells you what evidence you still need.

### 6.1 Failure-driven discovery

A model fails in a way that surprises you. The move from "it fails" to a research question requires ruling out the boring explanations first: bug, wrong metric, wrong baseline, known issue already documented. Only after those are excluded does "what mechanism causes this" become a real question. **\[SI\]**

### 6.2 Contradiction-driven discovery

Two credible papers report incompatible findings. Before treating this as a gap, check: same dataset version? Same evaluation protocol? Same model scale? Many "contradictions" dissolve once you notice the two papers measured different things under the same name. If it survives that check, the contradiction is real and worth a discriminating experiment.

### 6.3 Assumption-driven discovery

A widely-cited method's success is often explained with a plausible-sounding mechanism that was never directly isolated. Example, real and verified: for years, strong performance on the SNLI natural language inference benchmark was attributed to models learning genuine entailment reasoning. Gururangan et al. (2018) tested a hidden assumption nobody had isolated — that the *premise* was actually necessary — by training a classifier on the hypothesis sentence alone. It recovered roughly 67% accuracy on SNLI and 53% on MultiNLI, far above chance, revealing that crowd-worker annotation habits left statistical clues (e.g., negation words correlating with "contradiction") that let models shortcut the task entirely. \[ref: Gururangan et al., "Annotation Artifacts in Natural Language Inference Data," NAACL 2018, aclanthology.org/N18-2017\] **\[V\]** This is the template for assumption-driven discovery: identify what the standard pipeline implicitly assumes is necessary, then design an ablation that removes it and see if performance survives.

### 6.4 Benchmark-driven discovery

A benchmark exposes a systematic weakness. The hard part is diagnosing *which* of several causes is responsible:


| Possible cause             | How to distinguish it                                                                                       |
| ---------------------------- | ------------------------------------------------------------------------------------------------------------- |
| Real model limitation      | Weakness persists across multiple datasets and model families                                               |
| Dataset artifact           | A trivial baseline (e.g., hypothesis-only, or a linear probe on shallow features) performs far above chance |
| Evaluation/metric artifact | Manual inspection shows the metric penalizes valid outputs or rewards degenerate ones                       |
| Shortcut                   | Performance collapses under a matched, minimally-edited counterfactual test set                             |
| Distribution shift         | Performance recovers when train/test come from the same distribution                                        |
| Annotation problem         | Inter-annotator agreement is low, or labels contradict the source text on manual audit                      |

Geirhos et al. (2020) formalize this general pattern across vision and language as "shortcut learning": decision rules that perform well on standard benchmarks but fail to transfer, because models exploit unintended statistical regularities rather than the intended task structure. \[ref: Geirhos et al., "Shortcut Learning in Deep Neural Networks," Nature Machine Intelligence 2, 665-673 (2020); arxiv.org/abs/2004.07780\] **\[V\]**

### 6.5 Method-driven discovery

A new method or trick produces an unexpected gain. The lazy move is to report the higher number. The research move is to ask what mechanism the gain came from, and to design an ablation that isolates it from confounds (more parameters, more compute, more training steps, better hyperparameter search).

### 6.6 Gap-driven discovery

The critical distinction: "nobody has done X" is not a research question. "There is an unresolved scientific question for which doing X would provide discriminating evidence" is. The test: if X had already been done and came out one way, would it change what the field believes? If not, doing X is an engineering exercise, not research. **\[SI\]**

### 6.7 Negative-result-driven discovery

A method you expected to work doesn't. If the null result is well-controlled (not just a bug or bad hyperparameters), it is often more informative than a positive result, because it rules out a plausible-sounding explanation the field was implicitly relying on. See section 18.

### 6.8 Opportunity-driven discovery

A new dataset, open model, or capability makes a previously untestable question testable. This is legitimate only if the new resource actually changes what evidence is obtainable, not merely because it's new and gets attention.

---

## 7. Literature Search: How Queries Evolve

Search is not one query. It is a sequence that narrows as your understanding sharpens.

```
"vision language models hallucination"          (broad concept)
        ↓
"object hallucination VQA"                       (terminology discovered)
        ↓
"CHAIR metric hallucination" / specific benchmark names
        ↓
"language prior hallucination multimodal"        (candidate mechanism)
        ↓
"counterfactual image editing hallucination"     (candidate method)
        ↓
"hallucination benchmark limitations" / "artifact"  (looking for evidence against your own idea)
```

Mechanisms an experienced researcher combines, not sequentially but as needed:

- **Backward search**: what does the closest paper cite for its method and its claims?
- **Forward/citation search**: who has cited the closest paper since, and did they challenge or extend it? (Google Scholar / Semantic Scholar "cited by")
- **Author/lab tracking**: does the group behind the closest paper have a follow-up or a workshop version with more detail?
- **Benchmark/dataset tracking**: what other papers report numbers on the exact same benchmark, and do their numbers agree?
- **Adversarial search**: explicitly search for evidence against your hypothesis ("X does not explain," "X is not sufficient," "limitations of X"). Beginners search only to confirm; this is the single most common self-inflicted blind spot. **\[PR\]**

**Stopping rule for search**: you have reached practical saturation, not exhaustive coverage, when new queries return papers you've already seen, or papers that cite the same 3-5 core works you've already read closely. **\[PR\]**

---

## 8. Reading Papers Without Drowning

Keshav's three-pass method remains the standard reference and is worth internalizing exactly because it prevents the default failure mode (reading start-to-finish, running out of time before the results section). \[ref: Keshav, "How to Read a Paper," ACM SIGCOMM CCR 2007\] **\[V\]**

- **First pass (5-10 min)**: title, abstract, headings, conclusions, skim references. Decide: relevant or not, and which of the passes below to do next.
- **Second pass (\~1 hour)**: read body carefully but skip proofs/derivations; note figures, tables, and the argument's skeleton. Enough to summarize the paper to someone else and to identify the parts you don't yet understand.
- **Third pass (1-5 hours)**: attempt to virtually re-implement the paper. Identify hidden assumptions, missing citations, and issues with experimental technique. This pass is reserved for the 3-8 papers that are genuinely closest to your question, not for everything you read.

For question discovery specifically, read with a narrower extraction target than "understand the paper":


| Extract                                                         | Where to look                                                                  |
| ----------------------------------------------------------------- | -------------------------------------------------------------------------------- |
| The central claim                                               | Abstract + last paragraph of intro                                             |
| What evidence supports it                                       | Results tables, not prose summaries of them                                    |
| What baselines were used, and whether they're strong or trivial | Experimental setup                                                             |
| What the authors admit they didn't test                         | Limitations / future work                                                      |
| What assumption the method depends on but never isolates        | Method section, read adversarially                                             |
| Anything left unexplained in the results                        | Look for hedged language ("we suspect," "interestingly," "it remains unclear") |

**Anti-pattern**: literature review as paper collection. Reading 80 abstracts and saving them is not literature review; it produces the illusion of coverage without the ability to state what is actually contested. **\[PR\]** A useful discipline: for every paper you keep, write one sentence on what you would do differently or what it leaves untested, before moving to the next.

---

## 9. Finding the Closest Work

"Related work" is everything adjacent. "Closest work" is the specific paper(s) whose experimental setup already occupies the space you're about to test in. Confusing the two produces contributions that reviewers correctly flag as incremental or already-known.

To find it, ask: which paper, if it had run one more experiment, would have already answered my question? That paper is your closest work, and your contribution has to be stated relative to it: what exactly does it not test, and why does that matter?

**Worked distinction**: for a hallucination-in-VLMs project, "related work" includes every VLM paper and every hallucination-measurement paper. "Closest work" is the specific paper that already measures hallucination under image perturbation, if one exists — and if it does, your job is to identify precisely what perturbation type, model class, or confound it left untested, not to redo it with a different model checkpoint and call it new.

---

## 10. Verifying a Real Gap

A stated gap in a paper's limitations section is a *hint*, not a verified fact. Authors sometimes state gaps that are actually already closed by a paper they missed, or state gaps too vaguely for anyone to act on. Before committing:

1. Search specifically for work that might already close the gap (adversarial search, section 7).
2. Check whether the gap is narrow enough to be answerable, or so broad it's unfalsifiable ("we don't fully understand generalization" is not a gap you can test in a thesis).
3. Ask whether closing the gap would actually change anyone's belief (section 6.6 test).

---

## 11. Killing Weak Ideas: Pre-Mortem / Adversarial Validation

Before investing in a question, attack it the way a skeptical labmate or reviewer would. **\[SI\]** — this practice is well-documented in research-methodology and reproducibility literature as a way to catch avoidable failures before they cost months. Run through:

- Has this already been answered, even partially, under a different name?
- Is the "gap" real, or just unexplored-because-uninteresting?
- Is the phenomenon reproducible by you, independently, before you build anything around it?
- Could a trivial baseline (linear probe, hypothesis-only, nearest-neighbor, majority class) explain the result you're chasing? (Directly modeled on the Gururangan et al. hypothesis-only baseline, section 6.3.)
- Is there a shortcut the model could be exploiting instead of the mechanism you're attributing?
- Is the dataset split leaking information (near-duplicates across train/test, metadata correlated with the label)?
- Is the benchmark's metric actually measuring the construct you think it measures?
- Is the proposed method actually necessary, or does a simpler ablation achieve the same effect?
- Is the experiment computationally feasible on your actual hardware within your actual timeline?
- If the result comes back negative, is that still a publishable, informative outcome, or does the whole project collapse?
- Is the contribution scientific (explains a mechanism) or purely engineering (builds a thing)? Either can be valid, but know which one you're claiming.

An idea that survives this list honestly is worth a minimum experiment. An idea that requires you to rationalize away two or more of these questions is usually worth killing early. **\[PR\]**

---

## 12. Minimum Discriminating Experiment

The single highest-leverage skill in this whole process: designing the *smallest* experiment that distinguishes between two (or more) competing explanations, rather than building the full system first.

```
Hypothesis A: VLM hallucination is caused by missing visual evidence.
Hypothesis B: VLM hallucination is caused by a language-side prior
              that ignores the image.

Minimum discriminating experiment:
  Hold the question text constant.
  Manipulate only the image (remove/insert the queried object via editing).
  Measure whether the model's answer changes.

  If answer changes reliably with the image → evidence for A
  If answer stays the same regardless of image content → evidence for B
```

This is not the full research project. It is the cheapest test that could kill one of the two explanations. Building an entire new training pipeline before running something like this is a common and expensive undergraduate mistake, because it commits weeks of engineering to a question that a day of careful evaluation could have already resolved or reframed. **\[PR\]**

Design elements that make an experiment genuinely discriminating rather than merely suggestive:

- **Matched controls**: the counterfactual condition should differ in exactly one variable from the baseline condition, nothing else.
- **Negative controls**: a condition where you expect no effect, to confirm your measurement isn't just noise-sensitive.
- **Placebo conditions**: a manipulation that looks similar but shouldn't matter under your hypothesis, to rule out that any edit at all triggers the effect.
- **Randomization** where feasible, to prevent ordering or selection confounds.
- **Leakage-resistant splits**: verify the test items weren't seen, even indirectly (near-duplicate, same-source), during training.
- **Causal vs. correlational framing**: an experiment with a genuine intervention (you change X and observe Y) supports causal claims; an observational correlation does not, regardless of how large the correlation is.

---

## 13. When Experiments Change the Question

Research is rarely: question → experiment → answer. It is closer to:

```
question → experiment → surprising result → return to literature
   → revised question → redesigned experiment → stronger evidence → contribution
```

**Realistic AI/ML pattern**: you hypothesize hallucination is purely visual (H_A above). Your counterfactual experiment shows partial support: answers change for common objects but not for rare ones. This doesn't cleanly support A or B — it suggests a third variable (object frequency / prior strength) that neither original hypothesis specified. At this point an experienced researcher does not force the messy result into the original binary. They:

- **Narrow** the question if only part of it is answerable with available resources ("under what image-editing conditions does hallucination persist" rather than "why does hallucination happen").
- **Split** into subquestions if the result reveals two distinct mechanisms operating together (frequency-driven prior + genuine visual insensitivity).
- **Broaden** if the mechanism turns out to generalize further than expected (e.g., also present in a different model family).
- **Pivot** to the newly discovered mechanism (object frequency) if it turns out to be the stronger and more explanatory variable — this is the "return to literature, revise" branch, and is often where the actual contribution lives, not in the original question.
- **Abandon** only if the discriminating experiment shows the phenomenon isn't reproducible or reduces entirely to a known artifact.

Treat the first experiment's result as data about your model of the field, not just data about the model under test. **\[SI\]**

---

## 14. From Question to Experimental Design


| Component                   | What it specifies                                                                 |
| ----------------------------- | ----------------------------------------------------------------------------------- |
| Independent variable(s)     | What you deliberately manipulate                                                  |
| Dependent variable(s)       | What you measure as the outcome                                                   |
| Controls                    | Conditions that isolate the variable of interest from confounds                   |
| Baselines                   | What "no effect" or "standard practice" looks like, to compare against            |
| Ablations                   | Systematic removal of components to attribute effect to cause                     |
| Metrics                     | What quantifies the dependent variable, and whether it's valid for the construct  |
| Repeated runs / variance    | Multiple seeds; a single run cannot distinguish signal from noise                 |
| Compute-matched comparisons | Comparing methods at equal training/inference budget, not just equal architecture |
| Data splits                 | Train/val/test with leakage checked, not assumed                                  |
| Robustness checks           | Does the effect hold across datasets, seeds, and minor implementation choices     |

A high score alone is not evidence of a contribution. **\[SI\]** It is evidence of task performance. The contribution requires showing the score means what you claim it means (see sections 6.4, 11).

---

## 15. Baselines and Controls, Precisely


| Term                | Meaning                                                                                                                   |
| --------------------- | --------------------------------------------------------------------------------------------------------------------------- |
| Baseline            | The standard method you compare against                                                                                   |
| Strong baseline     | A carefully-tuned version of the standard method, not a strawman                                                          |
| Trivial baseline    | Something absurdly simple (majority class, hypothesis-only, nearest neighbor) that should lose badly if your task is real |
| Oracle              | A method given information it wouldn't have at deployment time, defining an upper bound                                   |
| Ablation            | Your full method with one component removed                                                                               |
| Negative control    | A condition expected to show no effect, validating your measurement isn't just noisy                                      |
| Positive control    | A condition with a known, expected effect, validating your pipeline can detect real effects at all                        |
| Upper / lower bound | Best-case / worst-case reference points for interpreting where your result sits                                           |

Choosing controls is choosing which alternative explanations you're allowed to rule out. A missing trivial baseline is one of the most common reasons a claimed effect turns out, on later scrutiny, to be an artifact (again, section 6.3).

---

## 16. Data, Evaluation Validity, and Computational Feasibility

"I have a dataset" and "this dataset can discriminate between my hypotheses" are different claims. Before relying on a dataset, check: provenance and licensing, label quality (spot-check a sample by hand), train/test contamination and near-duplicates, distribution shift between splits, subgroup coverage, and whether the metric can be gamed by a shortcut (section 6.4 table).

For an undergraduate on limited hardware (no dedicated GPU, Colab-class compute), feasibility triage matters as much as scientific design: **\[PR\]**

- Prefer questions answerable with **inference-time interventions and smaller models** over questions requiring full pretraining or large-scale fine-tuning.
- Reduce scope by narrowing the dataset (a well-controlled subset) rather than abandoning statistical rigor (fewer seeds, no repeated runs) — scope reduction should preserve the ability to detect signal, not remove it.
- Budget for the experiment count actually needed: a single-condition test rarely survives review; matched-control experiments need at minimum a treatment and a comparison condition, ideally with multiple seeds.
- Prefer publicly available checkpoints and datasets to avoid both cost and reproducibility risk.

---

## 17. Research Engineering (Why, Not How)

The scientific reason these practices matter, not a software-engineering checklist: **\[SI\]**

- **Seeds and repeated runs** exist because a single run cannot distinguish a real effect from noise.
- **Configuration/version tracking** exists because a result that can't be traced back to its exact code+data+hyperparameters can't be defended when questioned, and can't be reproduced by you three months later.
- **Deterministic evaluation scripts** exist because manual or ad-hoc scoring silently introduces experimenter bias into the exact numbers meant to be your evidence.
- **Dataset snapshots** exist because "the benchmark" quietly changes version over time, and a claim tied to the wrong version is not the claim you think it is.

The NeurIPS reproducibility program (2019 onward) institutionalized exactly this logic at the field level: a checklist requiring authors to state, for every empirical claim, how the experiment was run and whether it can be reproduced. Analysis of the 2019 program found that even at a top venue, disclosure of basic experimental methodology was inconsistent before the checklist was introduced, which is why it became a mandatory submission component. \[ref: Pineau et al., "Improving Reproducibility in Machine Learning Research," JMLR 22(164), 2021; NeurIPS Paper Checklist Guidelines, neurips.cc/public/guides/PaperChecklist\] **\[V\]**

---

## 18. Error Analysis as Research

```
Aggregate score → error categories → failure patterns → hypothesis
   → controlled test → mechanistic explanation
```

Error analysis is frequently where the actual contribution is discovered, not confirmed. A researcher who only reports the aggregate score misses the fact that the errors cluster in a specific, explainable way (e.g., hallucinations cluster on rare objects, not objects in general). Turning a cluster into a mechanism requires the same discipline as section 12: form a hypothesis about *why* the errors cluster there, then design a controlled test, not just a bigger table of examples.

**Negative results**: a well-controlled "our method did not help" is scientifically valuable when it rules out a plausible mechanism the field assumed was doing the work (this is exactly what happened structurally in the NLI annotation-artifacts case: the "obvious" explanation — models understand entailment — was ruled out by a negative-result-style baseline check). A negative result is *not* valuable when it's confounded (bad hyperparameters, undertrained baseline, wrong metric) — that's not evidence, it's an unfinished experiment.

---

## 19. Deciding to Continue, Narrow, Pivot, or Kill


| Decision                | Trigger                                                                                  |
| ------------------------- | ------------------------------------------------------------------------------------------ |
| Continue as-is          | Result matches prediction with adequate controls and variance                            |
| Narrow the question     | Original scope too broad to answer with available resources/time                         |
| Broaden                 | Effect generalizes further than expected, and you have time/compute to test it           |
| Split into subquestions | Result reveals more than one mechanism operating together                                |
| Pivot                   | A discovered mechanism is more explanatory than the original hypothesis                  |
| Kill the idea           | Phenomenon doesn't reproduce, or reduces entirely to a known artifact/trivial baseline   |
| Stop adding experiments | Additional runs would not change the interpretation of the existing evidence             |
| Start writing           | You can state the evidence chain end-to-end without gaps you're hoping no one asks about |

These are evidence-based heuristics, not fixed rules. **\[PR\]**

---

## 20. From Evidence to Contribution


| Contribution type | What it claims                                 | Example framing                                                    |
| ------------------- | ------------------------------------------------ | -------------------------------------------------------------------- |
| Engineering       | "We built X"                                   | A working, documented system others can use                        |
| Empirical         | "We measured Y across Z conditions"            | Systematic benchmarking that didn't exist before                   |
| Diagnostic        | "The apparent failure is caused by X, not Y"   | Annotation-artifacts style decomposition                           |
| Methodological    | "We introduce a method that enables..."        | A new technique with demonstrated necessity, not just a score bump |
| Mechanistic       | "We identify the mechanism responsible for..." | Causal isolation via controlled intervention                       |
| Benchmark         | "Existing evaluation fails to measure..."      | A new test set or metric with demonstrated discriminating power    |

An undergraduate thesis most often produces an honest empirical or diagnostic contribution. That is legitimate and defensible; it does not need to masquerade as a new method to be worthwhile. **\[PR\]**

---

## 21. Writing the Thesis and the Paper

The thesis should mirror the actual evidence chain, not a template of disconnected chapters: Introduction states the tension; Related Work establishes the closest work and what it leaves untested; Methodology and Experimental Design follow directly from the minimum discriminating experiment (section 12) and its escalations; Results present what actually happened, including the surprising turn if there was one (section 13); Discussion and Limitations state, explicitly, what alternative explanations remain uneliminated.

Turning it into a paper means cutting, not adding: identify the one central claim the evidence actually supports, remove experiments that don't serve that claim (even if they took real effort), and position precisely against the closest work identified in section 9.

**Reviewer-mindset self-attack, before anyone else does it to you:**

```
Claim → Evidence? → Alternative explanation ruled out? → Control present?
   → Leakage checked? → Baseline strong enough? → Generalizes beyond one setting?
   → Variance/uncertainty reported? → Overclaimed relative to evidence?
```

Common AI/ML reviewer objections worth pre-answering: "is this just dataset size / compute advantage?", "would a simpler baseline match this?", "is the effect significant across seeds or a single lucky run?", "does this generalize beyond the one model/dataset tested?"

---

## 22. Tool-Assisted Research: What to Delegate and What Not To


| Task                   | Best tool type                                                          | Role                                                                                          |
| ------------------------ | ------------------------------------------------------------------------- | ----------------------------------------------------------------------------------------------- |
| Broad discovery        | Search engines, Semantic Scholar, arXiv, OpenReview                     | Surface candidates fast                                                                       |
| Paper retrieval        | Scholarly databases, arXiv, alphaXiv                                    | Get the actual text                                                                           |
| Paper comprehension    | LLM + full paper text                                                   | Faster first/second-pass extraction, not a replacement for third-pass reading of closest work |
| Evidence verification  | Primary source, not the LLM's paraphrase                                | Confirm a claim before relying on it                                                          |
| Implementation         | Coding environment (Colab, local)                                       | Build and run the experiment                                                                  |
| Experiment tracking    | Lightweight logging (even a spreadsheet is fine at undergraduate scale) | Preserve what was run and why                                                                 |
| Synthesis and judgment | You                                                                     | Decide what the evidence means                                                                |

**Never delegate to an LLM**: final interpretation of evidence, unsupported novelty claims ("this is the first work to..." without verifying it), fabricated or unverified citations, causal conclusions from correlational data, and the decision that a literature gap is real without independently verifying it (section 10). An LLM can accelerate every stage of search, reading, and drafting; it cannot substitute for the judgment call of whether your evidence actually supports your claim. **\[PR\]**

---

## 23. The Realistic Undergraduate Version

What can be simplified without lowering scientific standard, and what cannot: **\[PR\]**

**Can simplify:** scale (smaller models, subsetted data), infrastructure (a spreadsheet instead of a full experiment-tracking platform), breadth of literature review (saturate on the closest 15-25 papers rather than hundreds), scope of the contribution (one well-isolated mechanism, not a new general-purpose method).

**Cannot compromise:** the presence of a real control/baseline for every claim, checking for leakage and trivial-baseline explanations, reporting variance across at least a few seeds instead of one run, being honest in limitations about what remains untested, and verifying (not assuming) that a claimed gap is real.

**Where undergraduate projects typically fail:** committing to full implementation before running a minimum discriminating experiment; treating "no one has done exactly this" as sufficient justification; skipping the trivial-baseline check because it feels like it would undercut the exciting result; and writing the thesis narrative before the evidence chain is actually complete, then quietly hoping the gaps go unnoticed.

---

## 24. A Personal Research Operating System

Lightweight artifacts, not heavy process, sized for one researcher:

- **Research inbox**: a running list of observations and half-formed questions as they occur, so you don't lose them and don't have to restart discovery from zero each week.
- **Evidence table**: claim → source → evidence → confidence (verified / inferred / uncertain) → limitation. This is the backbone of both your literature review and your related-work section.
- **Experiment ledger**: hypothesis → experiment → result → interpretation → next decision (continue/narrow/pivot/kill, section 19). This becomes your methodology and results chapters almost directly.
- **Decision log**: one line per major pivot, stating what evidence caused it. This prevents you from later forgetting *why* you abandoned a direction and re-exploring it from scratch.

---

## 25. Complete Worked Example

This walks a realistic, evidence-grounded trajectory through the whole process, composited from the real, verified research pattern in sections 6.3, 6.4, and 11 above (Gururangan et al. 2018; Geirhos et al. 2020). It illustrates the reasoning, not a fabricated citation trail.

1. **Initial vague interest**: "I'm interested in why language models seem to do so well on inference/reasoning benchmarks."
2. **Field exploration**: orient in NLI (natural language inference) and its major benchmarks (SNLI, MultiNLI).
3. **First observation**: a simple model, or even a shallow classifier, scores suspiciously high considering how "hard" the task is claimed to be.
4. **Paper discovery / closest work**: prior NLI papers attribute high scores to genuine entailment reasoning learned from large-scale crowd-sourced data.
5. **Potential gap**: no paper has isolated whether the *premise* is actually necessary for the model's decision. This is an assumption everyone relies on but nobody directly tested (section 6.3).
6. **Gap verification**: check whether anyone has run a hypothesis-only ablation. If not, the gap is real and testable cheaply.
7. **Competing explanations**: (A) models learn genuine cross-sentence inference; (B) models exploit surface statistical cues in the hypothesis sentence alone, introduced by how crowd workers write entailments/contradictions/neutrals.
8. **Research question**: does a classifier trained on the hypothesis alone, with the premise withheld, perform far above chance?
9. **Hypothesis**: if B is true, hypothesis-only accuracy will be well above the majority-class baseline.
10. **Minimum discriminating experiment**: train a simple text classifier on hypothesis sentences only, no premise, same labels, same splits.
11. **Result**: accuracy far above chance (in the real study, about 67% on SNLI, 53% on MultiNLI, against a 3-class near-33% baseline) — a genuinely surprising result if you expected explanation A.
12. **Question revision**: the finding doesn't just complicate A, it reframes the whole question: not "how well do models reason" but "what specific linguistic cues correlate with each label, and how much of reported model performance is explained by them rather than by cross-sentence reasoning."
13. **Expanded experiment / error analysis**: identify which lexical/syntactic cues (e.g., negation words correlating with "contradiction," vague quantifiers with "neutral") drive the effect.
14. **Final evidence**: a documented, mechanistic account of *why* the benchmark overestimates model reasoning ability, not just the fact that it does.
15. **Contribution**: diagnostic — the field's success metric was measuring something other than what it claimed to measure; this reframes how the benchmark's numbers should be interpreted going forward.
16. **Thesis/paper**: written around this evidence chain, with the hypothesis-only ablation as the load-bearing experiment and the cue analysis as the mechanistic explanation.

The pivot point, step 11 to 12, is the part beginners skip. The instinct is to report "surprising baseline result" as a footnote and continue the original plan. The actual research move is to let that result redefine the question. \[ref: Gururangan et al., NAACL 2018, aclanthology.org/N18-2017\]

---

## 26. Researcher's Desk Reference

**Before exploring**: what's the field's vocabulary, canonical papers, and current benchmarks? **While exploring**: what's the phenomenon, the existing explanation, and what's under-tested about it? **When something looks interesting**: is it reproducible by me? Is there a trivial explanation I haven't ruled out? **Before committing**: have I adversarially searched for work that already closes this gap? Would the answer, either way, change anyone's belief? **Before implementing**: can I state the minimum discriminating experiment in one paragraph, with a clear prediction for each hypothesis? **During experiments**: seeds, exact config, exact data version, logged before you move to the next run. **When results surprise you**: return to literature before continuing; ask whether the question itself needs to change. **Before claiming a contribution**: have I ruled out a trivial baseline, a leakage explanation, and a confound in compute/data? **Before writing**: can I state the full evidence chain, gap to conclusion, without a step I'm hoping goes unquestioned? **Before submission**: what would a skeptical reviewer attack first, and have I addressed it in the text, not just in my head?

---

## Evidence Base

**Research methodology**

- Hamming, R. "You and Your Research," Bell Communications Research Colloquium, 1986. Full transcript: fs.blog/great-talks/richard-hamming-your-research **\[V\]**

**AI/ML research practice — worked examples**

- Gururangan et al., "Annotation Artifacts in Natural Language Inference Data," NAACL-HLT 2018. aclanthology.org/N18-2017 **\[V\]**
- Geirhos et al., "Shortcut Learning in Deep Neural Networks," Nature Machine Intelligence 2, 665-673, 2020. arxiv.org/abs/2004.07780 **\[V\]**

**Reproducibility**

- Pineau et al., "Improving Reproducibility in Machine Learning Research: A Report from the NeurIPS 2019 Reproducibility Program," JMLR 22(164), 2021. arxiv.org/pdf/2003.12206 **\[V\]**
- NeurIPS Paper Checklist Guidelines. neurips.cc/public/guides/PaperChecklist **\[V\]**

**Reading and literature practice**

- Keshav, S. "How to Read a Paper," ACM SIGCOMM Computer Communication Review, 2007 (updated 2016). Widely mirrored; e.g. cs.princeton.edu/courses/archive/fall10/cos597B/papers/howtoread-keshav.pdf **\[V\]**

Everything not attributed to one of the sources above is either strong inference from documented research practice or an explicit practical recommendation, marked inline as **\[SI\]** or **\[PR\]**. Treat the funnel, the terminology ladder, the personal operating-system artifacts, and the desk reference as synthesis tools, not as claims about how all researchers universally work.
