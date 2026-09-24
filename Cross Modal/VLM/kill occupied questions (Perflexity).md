<img src="https://r2cdn.perplexity.ai/pplx-full-logo-primary-dark%402x.png" style="height:64px;margin-right:32px"/>

# A. Research-question tree

This is a **discovery report, not a final thesis decision**. The initial literature scan shows that generic hallucination, confidence, VQA comparison, RAG, and visual-token compression are already heavily occupied. The strongest remaining opportunities are narrower questions about **controlled evidence use, intervention effects, cross-modal conflict, and evaluation validity**.

```text
Multimodal / Vision-Language Learning and Systems
│
├── 1. Evidence use and grounding
│   ├── Failure: answer is correct without using the image
│   ├── Failure: rationale contains unsupported visual claims
│   ├── Hypothesis: models rely on language priors or shortcuts
│   ├── Intervention: remove, corrupt, crop, or replace visual evidence
│   └── Outcome: paired answer change, evidence sensitivity, grounding accuracy
│
├── 2. Cross-modal conflict arbitration
│   ├── Failure: model prefers text, vision, or parametric knowledge incorrectly
│   ├── Hypothesis: arbitration depends on modality reliability or answer type
│   ├── Intervention: controlled counterfactual image/text conflict
│   └── Outcome: modality preference, conflict accuracy, confidence, harm rate
│
├── 3. Evidence sufficiency and answerability
│   ├── Failure: model answers when available evidence is insufficient
│   ├── Hypothesis: confidence reflects language fluency rather than evidence
│   ├── Intervention: vary evidence completeness while preserving question form
│   └── Outcome: abstention quality, selective risk, unsupported-answer rate
│
├── 4. Cross-modal verification
│   ├── Failure: generated claims are not checked against the image
│   ├── Hypothesis: verification improves factuality only when claims are localized
│   ├── Intervention: claim decomposition plus visual evidence checking
│   └── Outcome: claim precision, correction rate, unnecessary correction rate
│
├── 5. Missing and incomplete modalities
│   ├── Failure: model fails unpredictably when image, text, or region is missing
│   ├── Hypothesis: robustness depends on which modality carries decisive evidence
│   ├── Intervention: modality removal, masking, blur, occlusion, paraphrase
│   └── Outcome: performance degradation, recovery, modality sensitivity
│
├── 6. Modality reliance and causal contribution
│   ├── Failure: benchmark score hides whether both modalities are used
│   ├── Hypothesis: reliance varies by task, model, and dataset
│   ├── Intervention: matched unimodal and multimodal counterfactuals
│   └── Outcome: incremental multimodal value, reliance asymmetry, shortcut rate
│
├── 7. Distribution shift and cross-cultural generalization
│   ├── Failure: VLM performs well on familiar visual-language distributions
│   ├── Hypothesis: failure is caused by perception, language, or cultural knowledge
│   ├── Intervention: hold out source, entity, dialect, culture, or image style
│   └── Outcome: transfer accuracy, repair effect, error-type shift
│
├── 8. Multilingual and low-resource multimodal transfer
│   ├── Failure: translation or language switching changes visual understanding
│   ├── Hypothesis: language affects grounding rather than only text processing
│   ├── Intervention: parallel questions, dialect variants, meaning-preserving rewrites
│   └── Outcome: semantic consistency, visual evidence use, translation harm
│
├── 9. Counterfactual multimodal reasoning
│   ├── Failure: model follows memorized world knowledge over altered visual facts
│   ├── Hypothesis: conflict behavior depends on visual salience and prior strength
│   ├── Intervention: controlled image edits and matched textual conflicts
│   └── Outcome: counterfactual accuracy, arbitration curve, confidence calibration
│
├── 10. Efficient VLM inference and reliability
│   ├── Failure: token reduction preserves average accuracy but damages evidence use
│   ├── Hypothesis: compression selectively removes task-critical regions
│   ├── Intervention: resolution, token budget, pruning, quantization
│   └── Outcome: accuracy–latency–memory–reliability frontier
│
├── 11. Adaptive information acquisition
│   ├── Failure: model knows it is uncertain but chooses the wrong help
│   ├── Hypothesis: action value is task-specific, not confidence-specific
│   ├── Intervention: zoom, retrieve, clarify, or stop under a fixed budget
│   └── Outcome: gain per cost, regret, harmful action rate
│
└── 12. Benchmark validity and contamination
    ├── Failure: scores reflect answer priors, templates, captions, or leakage
    ├── Hypothesis: apparent multimodal reasoning is partly unimodal
    ├── Intervention: unimodal controls, grouped splits, counterfactual tests
    └── Outcome: score inflation, ranking changes, validity diagnostics
```


# B. Research families

| Family | Core phenomenon and failure mode | Candidate variables and intervention | Baseline, data, and useful negative result | Undergraduate suitability |
| :-- | :-- | :-- | :-- | :-- |
| Evidence use | A VLM answers correctly without using visual evidence | Image removal, blur, crop, irrelevant replacement; measure paired answer change and evidence sensitivity | Text-only, image-only, frozen VLM; VQA, MMMU-style, cultural VQA | Medium; benchmark leakage is a major risk |
| Conflict arbitration | Vision, text, and model knowledge disagree | Counterfactual images, contradictory captions, reliability cues; measure modality preference and harm | Text-only/image-only, majority rule, prompting; Visual-Counterfact-style data | Medium; already rapidly expanding |
| Evidence sufficiency | Model gives confident answers when evidence is absent | Remove decisive evidence or make it ambiguous; measure abstention and selective risk | Always-answer, confidence threshold, random abstention; VQA with answerability labels | Medium-low; answerability annotation is difficult |
| Cross-modal verification | Generated claims are unsupported or only partially supported | Decompose claims and verify each against regions or image descriptions | No verification, textual self-check, simple image-question recheck | Medium; claim labels and faithfulness evaluation are costly |
| Missing modalities | Performance collapse differs by missing modality | Remove image, question context, OCR, region, or retrieved evidence | Full input, unimodal input, random masking | High; controlled perturbations are feasible |
| Modality reliance | Average accuracy hides the incremental value of each modality | Matched multimodal/unimodal/counterfactual inputs | Majority and modality-only baselines | High; strong candidate if leakage is carefully controlled |
| Distribution shift | Model fails on new source, style, culture, or language | Grouped source/entity/dialect splits; optional repair interventions | Frozen VLM, retrieval, translation, crop/description help | Medium; dataset provenance must be audited |
| Bengali cultural repair | Cultural VLM error may arise from visual, linguistic, or knowledge limitations | Independent visual clarification, language clarification, cultural knowledge; full factorial design | No help, each help alone, simple combinations; BanglaVerse plus external data | Medium-high; annotation is the main burden |
| Counterfactual reasoning | Model follows parametric priors over altered visual facts | Image edits with matched text and salience controls | Image-only, text-only, conflict prompts | Medium; existing 2024–2026 work is close |
| Efficient reliability | Compression may preserve accuracy while damaging evidence use | Token budget, resolution, pruning, quantization; measure reliability and task-specific damage | Full-token model, random token selection, 4/8-bit baseline | High computationally, but novelty is weak unless narrowly framed |
| Adaptive acquisition | Confidence does not identify which action will help | Zoom, retrieve, clarify, stop; compare action policies under cost | Fixed policies, confidence rules, oracle action policy | Medium-high; infrastructure and action labels are substantial |
| Benchmark validity | Scores reflect shortcuts rather than multimodal understanding | Unimodal controls, grouped splits, template/source checks | Published score, text-only model, shuffled/blank image | High; contribution can be an audit, but must target an unresolved benchmark issue |

## Candidate research questions

1. **Evidence-use question:** When visual evidence is removed, corrupted, or replaced while the question remains unchanged, which VLM capabilities fail first, and do standard benchmark scores predict that sensitivity?
2. **Conflict question:** Under controlled visual–linguistic conflict, does a VLM select the modality with greater evidential reliability, or does it follow a fixed modality preference?
3. **Sufficiency question:** Can a VLM distinguish “the answer is false” from “the available evidence is insufficient,” and does its confidence reflect that distinction?
4. **Verification question:** Does claim-level visual verification reduce unsupported multimodal reasoning, or does it simply cause broad and unnecessary retractions?
5. **Missing-modality question:** Is multimodal performance degradation determined more by the missing modality itself or by whether that modality contains the decisive evidence?
6. **Reliance question:** How much additional information does the image contribute beyond question wording, answer priors, OCR, captions, and model knowledge?
7. **Shift question:** When a VLM fails under cultural or linguistic distribution shift, which controlled intervention—visual clarification, language clarification, or external knowledge—repairs the failure?
8. **Bengali question:** On Bengali cultural visual questions, when do visual, linguistic, and cultural interventions independently repair errors, and when is their combination necessary?
9. **Counterfactual question:** Does visual salience alter whether a VLM follows a counterfactual image over memorized world knowledge?
10. **Efficiency question:** Does visual-token reduction preserve average accuracy while selectively harming fine-grained evidence use, conflict resolution, or abstention?
11. **Action-selection question:** Can a VLM select the information-gathering action that maximizes expected answer improvement rather than merely responding to uncertainty?
12. **Validity question:** How much do language-only shortcuts, captions, templates, and source identity inflate reported VLM performance on a selected benchmark?

These are **question candidates**, not established gaps.

# C. Literature map

The current scan identifies the following occupied or rapidly developing areas.


| Branch | Representative work | What it establishes |
| :-- | :-- | :-- |
| Benchmark validity | *Are We on the Right Way for Evaluating Large Vision-Language Models?* | Some multimodal benchmarks can be solved partly without visual input, and leakage or language-only shortcuts can distort results. [^1_1] |
| Broad evaluation | MEGA-Bench | Large-scale evaluation across more than 500 realistic multimodal tasks, with many task-specific metrics. [^1_2] |
| Conflict arbitration | *How Vision-Language Models Resolve Visual-Linguistic Conflicts* | A 2026 study using Visual-Counterfact reports that conflict failures arise substantially from arbitration rather than only perception. [^1_3] |
| Conflict benchmarks | SIGNPOST-Bench | Controlled original, blank, similar, random, and adversarial image variants for studying text–vision conflict. [^1_4] |
| Vision–knowledge conflict | *Insight Over Sight?* | Benchmarks and analysis for conflicts between visual input and commonsense/world knowledge. [^1_5] |
| Parametric conflict | *Unraveling Cross-Modality Knowledge Conflicts* | Formalizes conflicts between visual and language components and proposes detection/mitigation procedures. [^1_6] |
| Grounded reasoning | CoRGI | Post-hoc decomposition and visual grounding of reasoning steps, evaluated on VCR, ScienceQA, MMMU, MathVista, and HallusionBench. [^1_7] |
| Visual grounding | *Uncovering Grounding IDs* | External cues and grounding-related interventions can affect faithful multimodal generation. [^1_8] |
| Efficient VLMs | SmolVLM | Open small VLMs make inference-first studies realistic; SmolVLM-256M is reported at under 1 GB inference memory. [^1_9] |
| Efficient inference | VisionTrim and token-compression literature | Visual-token reduction and compression are active research areas with many current methods and reviews. [^1_10][^1_11] |
| Routing | VL-RouterBench | VLM routing is now supported by a dedicated benchmark based on model quality–cost matrices. [^1_12] |
| Contextual grounding | MM-Conv | Recent work evaluates context-aware referring expressions and shows that linguistic rewriting can strongly affect grounding. [^1_13] |
| Multimodal benchmark generation | Scalable benchmark-generation framework | Automated or semi-automated benchmark construction is itself an active research direction. [^1_14] |
| Bengali cultural multimodality | BanglaVerse, M4-RAG, BLEnD-Vis | Prior project evidence identifies existing Bengali cultural VQA, knowledge augmentation, and visual/text alignment work. The remaining question is whether controlled intervention combinations can distinguish perception, language, and cultural-knowledge failure. [^1_15] |

## Important model feasibility evidence

Small open models reduce the entry cost for controlled experiments:

- SmolVLM-256M is documented as requiring under 1 GB GPU memory for one-image inference and supports quantized loading.[^1_16]
- SmolVLM-500M is documented at approximately 1.23 GB GPU memory for one-image inference.[^1_17]
- SmolVLM’s 2.2B family is designed for relatively low computational overhead and is reported as competitive with substantially larger models.[^1_9]
- LLaVA-NeXT supports 4-bit and 8-bit loading through the Hugging Face ecosystem.[^1_18]

These facts support **inference-first pilot studies**, not the assumption that every 7B model or fine-tuning plan is practical.

# D. Occupied questions

The following should not be treated as complete thesis questions without a substantially narrower unresolved mechanism.

- “Can VLM X outperform VLM Y on VQA?”
- “Can RAG improve VQA?”
- “Can confidence detect hallucination?”
- “Can a VLM abstain when uncertain?”
- “Can visual-token pruning reduce inference cost?”
- “Can a model resolve text–image conflict?”
- “Can Bengali VQA accuracy be improved?”
- “Can external knowledge improve cultural VQA?”
- “Can a model verify its own chain of thought?”
- “Can a model ask for clarification?”
- “Can multimodal memory update after a contradiction?”
- “Can we build a new benchmark for multimodal evaluation?”

The evidence base is now sufficiently crowded that these formulations lack a defensible boundary.

# E. Partially explored questions

These remain plausible only with precise experimental controls.

### 1. Reliability-aware conflict arbitration

Existing work has established conflict benchmarks and modality-arbitration failures. A remaining question could study whether **reliability cues** change arbitration consistently across task types, or whether models use a fixed prior.

### 2. Efficiency–evidence trade-off

Token compression is crowded, but many studies still emphasize average task scores. A narrower question could test whether compression selectively damages **evidence sensitivity**, not only accuracy.

### 3. Cross-modal repair under distribution shift

General robustness and multilingual evaluation exist. The stronger question is whether controlled assistance distinguishes **visual**, **linguistic**, and **knowledge** causes of failure.

### 4. Evidence sufficiency

Confidence and abstention are established. A narrower extension would distinguish incorrectness from **insufficient evidence**, using matched cases where the answer is unknown rather than false.

### 5. Benchmark shortcut diagnosis

The general problem is known. A publishable undergraduate study would need to identify a particular benchmark family where a grouped split or multimodal counterfactual changes the scientific conclusion.

# F. Underexplored questions

The strongest initial candidates are:

1. **Bengali cultural repair:** Which combinations of visual, linguistic, and cultural information repair the same VLM failure?
2. **Evidence-value selection:** Can a VLM choose whether zooming, clarification, retrieval, or stopping will improve the answer?
3. **Efficiency and evidence use:** Does visual-token reduction preserve average accuracy while damaging sensitivity to decisive visual evidence?
4. **Evidence sufficiency versus falsity:** Can a VLM distinguish “not supported” from “supported but false”?
5. **Reliability-conditioned conflict arbitration:** Does the model follow the more reliable modality, or merely the modality it generally prefers?
6. **Cross-source multimodal transfer:** Do VLM error types change when images, speakers, entities, or cultural sources are held out?
7. **Claim-level verification:** Does localized verification improve correctness without causing indiscriminate retraction?
8. **Counterfactual salience:** Does visual salience determine whether a VLM follows altered visual evidence over memorized knowledge?

“Underexplored” here means **not resolved by the targeted search**, not proven novel.

# G. Top 10 RQs

| RQ | Scientific phenomenon | Closest work | What remains unknown | Dataset | Baseline | Main metric | Leakage risk | Compute | Novelty confidence | Feasibility |
| :-- | :-- | :-- | :-- | :-- | :-- | :-- | :-- | :-- | :-- | :-- |
| 1 | Cross-modal repair | BanglaVerse, M4-RAG, BLEnD-Vis | Whether visual, language, and cultural help have separable or interactive effects | BanglaVerse; possible BanglaProtha extension | Frozen small VLM, no-help, single-help controls | Paired repair/harm rate, interaction effect | High | Medium | Strong–moderate | Medium |
| 2 | Action-specific information value | BCEA, ClearVQA, TRUST | Whether action choice generalizes beyond confidence and seen action/task pairs | Constructed offline action-outcome set | Fixed action policies, confidence rule | Gain per cost, regret | High | High | Moderate | Medium-low |
| 3 | Token efficiency and evidence sensitivity | Token-compression methods, VisionTrim | Whether compression damages evidence use disproportionately | POPE, MME, VQA, targeted perturbations | Full-token, random pruning, quantized model | Accuracy change, evidence sensitivity, latency | Medium | Low-medium | Weak–moderate | High |
| 4 | Evidence sufficiency | Abstention/calibration literature | Whether models distinguish unknown from false and calibrate to evidence availability | Answerable/unanswerable VQA subset | Always-answer, confidence threshold | Selective risk, coverage, Brier score | High | Medium | Moderate | Medium |
| 5 | Reliability-conditioned arbitration | Visual-Counterfact, SIGNPOST-Bench | Whether explicit reliability cues change modality arbitration | Controlled conflict benchmark | Text-only, image-only, majority rule | Conflict accuracy, modality preference, harm | Medium | Low-medium | Moderate | High |
| 6 | Claim-level visual verification | CoRGI and grounding work | Whether localized verification improves claims without overcorrection | VCR, ScienceQA, MMMU subset | No verification, textual self-check | Claim precision, correction, unnecessary correction | High | Medium | Moderate | Medium |
| 7 | Source-shift failure mechanism | BanglaVerse and multilingual benchmarks | Whether shift failures are perceptual, linguistic, cultural, or source-specific | Grouped cultural/multilingual data | Frozen VLM, translation, retrieval | Transfer accuracy and error-type change | High | Medium | Moderate | Medium |
| 8 | Counterfactual visual salience | Visual-Counterfact, conflict papers | Whether salience determines visual versus parametric reliance | Synthetic controlled edits | Image-only/text-only | Counterfactual accuracy, arbitration curve | Medium | Low | Weak–moderate | High |
| 9 | Missing-modality dependence | Multimodal robustness studies | Whether failure depends on modality identity or decisive evidence location | VQA with region/context annotations | Full, image-only, text-only | Modality sensitivity and recovery | Medium | Low | Moderate | High |
| 10 | Benchmark shortcut audit | Evaluation-validity literature | Whether a specific benchmark ranking changes after leakage-resistant controls | One selected benchmark family | Published score, unimodal controls | Score inflation and ranking stability | High | Low | Moderate | High |

# H. Top 5

## RQ 1 — Cross-modal repair in Bengali cultural VQA

**Question:** On Bengali cultural visual questions, when do visual clarification, faithful language clarification, and relevant cultural knowledge repair the same model error individually, and when is their combination necessary?

### Closest work

1. **BanglaVerse**, 2026, provides Bengali cultural multimodal evaluation and discusses difficulty and error patterns. Its prior analysis does not, by itself, identify whether a failure is caused by perception, language, or cultural knowledge.[^1_15]
2. **M4-RAG**, 2025, makes cultural knowledge available and studies retrieval/knowledge augmentation. This means “knowledge helps cultural VQA” is already too weak as a contribution.[^1_15]
3. **BLEnD-Vis**, 2025, studies aligned cultural questions across textual and visual forms. A simple image-versus-text or Bengali-versus-English comparison would also be too close.[^1_15]

### Gap boundary

- Existing work establishes that Bengali/cultural VLM evaluation is difficult and that knowledge or representation changes can affect performance.
- It does not yet establish, in the inspected work, the **interaction structure of independently controlled visual, linguistic, and cultural interventions on the same items**.
- The experiment would manipulate those intervention factors while holding the underlying image, question intent, and answer space fixed.


### Minimum experiment

Use eight conditions:

$$
\varnothing,\ V,\ L,\ K,\ V+L,\ V+K,\ L+K,\ V+L+K
$$

where:

- $V$: visual clarification without naming the target answer.
- $L$: native-speaker-validated linguistic clarification.
- $K$: relevant cultural information without directly revealing the answer.

Include initially correct and initially incorrect cases.

### Strong controls

- Text-only question control.
- Unrelated-knowledge control.
- Candidate-balanced knowledge descriptions.
- Option-order randomization.
- Image crop versus textual visual description as separate interventions.
- Human review for answer leakage.
- Grouped splits by image, entity, source, and cultural practice.


### Meaningful negative result

If knowledge alone explains nearly all repairs and combinations add nothing, that would show that the proposed perception–language interaction is weak under the chosen setting. If interventions frequently damage initially correct answers, that would reveal a reliability problem in assistance itself.

### Main risk

The question requires high-quality native-speaker and cultural annotation. The scientific validity depends more on intervention independence than on GPU capacity.

## RQ 2 — Can a VLM choose useful information actions?

**Question:** Among zooming, clarification, retrieval, and stopping, can a VLM select the action with the greatest expected answer improvement per cost?

### Existing boundary

Generic uncertainty-triggered intervention is already crowded. BCEA studies budgeted evidence acquisition; ClearVQA studies clarification; TRUST studies tool/action decisions under uncertainty.[^1_15]

### What would remain distinct

The study must test **action-specific expected value**, not merely whether uncertainty triggers an action. The controller should choose among actions that have comparable offline outcomes and should be evaluated on unseen domains or action combinations.

### Required baselines

- Always answer.
- Always retrieve.
- Always zoom.
- Confidence-threshold policy.
- Prompted action selector.
- Learned action-value model.
- Oracle action selector, clearly marked as an upper bound.


### Main risks

- Action datasets may encode action identity through source or task.
- A controller may learn dataset classification rather than action value.
- Cost definitions are subjective.
- Annotation and environment construction are substantial.

This is technically attractive but less undergraduate-safe than RQ 1.

## RQ 3 — Bengali dialect normalization with meaning preservation

**Question:** Can downstream multimodal or language understanding improve after Bengali dialect normalization without changing critical meaning or resolving ambiguity that the original utterance leaves open?

### Existing boundary

Prior work already covers dialect corpora, normalization, translation, and evaluation. Generic dialect-to-standard conversion is therefore occupied.[^1_15]

### Distinct contribution

The contribution would be an **ambiguity-preserving representation** evaluated by downstream decisions. The model should be penalized for unsupported disambiguation, not merely rewarded for fluent output.

### Evaluation

- Direct downstream model input.
- Ordinary normalization.
- Original plus normalized text.
- Conservative normalization.
- Ambiguity-preserving output.

Metrics should include:

- Downstream task accuracy.
- Critical meaning-change rate.
- Unsupported disambiguation rate.
- Coverage of useful normalization.
- Native-speaker judgment.


### Main risk

This requires sustained native-speaker collaboration and careful distinction between true ambiguity and annotator unfamiliarity.

## RQ 4 — Reliability-conditioned visual–linguistic arbitration

**Question:** When image and text conflict, does a VLM follow the modality with greater experimentally controlled reliability, or does it exhibit a fixed modality preference?

### Existing work

Conflict datasets and 2026 arbitration studies already establish that the problem exists.[^1_3][^1_4][^1_5]

### Remaining question

A narrow extension could manipulate reliability systematically:

- Clear versus blurred image.
- Specific versus vague text.
- High versus low visual salience.
- Direct versus indirect textual assertion.
- Consistent versus conflicting parametric knowledge.


### Metrics

- Conflict resolution accuracy.
- Modality preference rate.
- Harm rate relative to the reliable modality.
- Confidence shift.
- Calibration under conflict.


### Main risk

The topic may already be occupied by very recent 2026 work, including conflict-aware routing and arbitration methods. A full paper-by-paper comparison is required before treating this as a gap.[^1_19][^1_20]

## RQ 5 — Does token reduction damage evidence use?

**Question:** Does visual-token reduction preserve average VLM accuracy while selectively damaging sensitivity to decisive visual evidence?

### Existing boundary

Visual-token compression is highly active, with current methods such as VisionTrim and newer budget-adaptive token selection.[^1_10][^1_21]

### Distinct contribution

Do not propose another compression method. Test whether existing compression changes:

- Fine-grained evidence use.
- Conflict resolution.
- Object-existence hallucination.
- Spatial or count reasoning.
- Confidence and abstention.


### Metrics

- Task accuracy.
- Paired full-versus-compressed answer change.
- Evidence sensitivity.
- Latency and memory.
- Reliability–efficiency Pareto frontier.


### Main risk

Novelty is weaker than RQ 1. It is best used as a fallback empirical audit if a clean token-compression setup is easier to reproduce.

# I. Top 3

## 1. Cross-modal repair of Bengali cultural VLM failures

### Exact hypothesis structure

There are at least three competing explanations for a wrong answer:

1. The relevant visual entity or attribute was not recognized.
2. The question or dialect was misunderstood.
3. The model lacked the cultural association needed after perception and language understanding.

The experiment should test whether these explanations produce different intervention signatures.


| Intervention | Intended information | Main validity condition |
| :-- | :-- | :-- |
| Visual clarification | More access to existing visible attributes | Must not name or identify the answer |
| Linguistic clarification | Better-preserved question meaning and referents | Must not add cultural facts |
| Cultural knowledge | Relevant factual context | Must not directly disclose image–answer correspondence |
| Combined interventions | Interaction of information types | Each component must remain independently auditable |

### Dataset plan

Start with BanglaVerse as a candidate pool, but audit:

- Image provenance and redistribution permissions.
- Existing captions for answer leakage.
- Repeated images or entities.
- Cultural-domain distribution.
- Dialect labels and translation alignment.
- Source and entity overlap.
- Whether external BanglaProtha data is genuinely independent.

The attached project evidence specifically warns that BanglaVerse captions should not automatically be treated as neutral visual descriptions and that mixed image origins require provenance checking.[^1_15]

### Baselines

- Frozen small open VLM.
- Text-only language model or text-only prompt condition.
- Image-only or image-plus-neutral-question condition where applicable.
- No-help baseline.
- Each single intervention.
- Random or unrelated knowledge.
- Human-validated answer-bearing assistance as a separately labeled upper bound.


### Metrics

Let $Y(V,L,K)$ denote correctness under a specified intervention combination.

- Repair rate: initially incorrect items corrected.
- Harm rate: initially correct items made incorrect.
- Paired accuracy change.
- Visual–knowledge interaction:

$$
Y(1,0,1)-Y(1,0,0)-Y(0,0,1)+Y(0,0,0)
$$
- Linguistic–knowledge interaction.
- Minimum tested assistance set producing correction.
- Transfer across held-out entities, sources, domains, and dialects.

Use cluster-aware confidence intervals by original image or entity, not by translated or augmented row.

### Leakage threats

- Caption names the answer.
- Cultural knowledge identifies the entity directly.
- Translation resolves the intended answer rather than preserving ambiguity.
- Image duplicates cross splits.
- Question templates predict labels.
- “Visual descriptions” include non-visible cultural facts.
- External knowledge source overlaps with benchmark text.


### Compute plan

**Minimum experiment:**

- One small open VLM, such as SmolVLM-500M or 2.2B.
- Inference-only evaluation.
- 200–500 carefully validated items.
- Eight intervention conditions.
- Batched generation where possible.
- Repeated sampling only for a smaller uncertainty subset.

**Optional extension:**

- Second model family.
- LoRA/QLoRA repair method selected after diagnosing the failure.
- Independent cultural test set.

SmolVLM’s official materials indicate that small variants support low-memory and quantized inference, making an inference-first pilot realistic on Colab-style hardware.[^1_9][^1_16][^1_17]

### Negative-result value

The study remains useful if:

- Visual intervention does not help more than language intervention.
- Knowledge helps only when visual recognition is already correct.
- Combined interventions interfere rather than interact.
- A simple text-only baseline explains most gains.
- Results fail to transfer to an independent cultural source.

These outcomes would constrain claims about what cultural VLM systems actually need.

### Current verdict

**Continue to targeted verification, not yet proceed to thesis selection.**

Novelty confidence: **moderate to strong for the precise interaction question**, but only after checking all recent 2026 cultural VLM and intervention papers.

Feasibility: **medium**.

Primary bottleneck: **annotation and leakage control**, not model training.

## 2. Action-specific information acquisition

### Scientific question

A model can be uncertain but still choose the wrong intervention. The core question is whether action selection requires estimating the expected value of each action rather than using confidence alone.

### Experimental design

For the same initial question, construct outcomes for:

- Zoom.
- Crop.
- Retrieval.
- Clarification.
- Stop.

The policy chooses before seeing the action result. Use offline replay to avoid expensive interactive data collection.

### Evaluation

$$
\text{Value per cost} =
\frac{\text{post-action correctness} - \text{initial correctness}}{\text{action cost}}
$$

Also report:

- Harmful action rate.
- Unnecessary action rate.
- Regret relative to the measured oracle.
- Performance on unseen domains.
- Performance on action combinations absent during training.


### Verdict

**Reserve.**

Novelty confidence: **moderate**.

Feasibility: **medium-low** because action comparability, cost modeling, and leakage-resistant environment construction are difficult.

## 3. Token reduction and evidence sensitivity

### Scientific question

Average accuracy may remain stable after compression while evidence-sensitive behavior deteriorates. This would expose a reliability cost hidden by ordinary benchmark reporting.

### Controlled setup

Compare:

- Full-resolution/full-token input.
- Reduced resolution.
- Existing token-pruning method.
- Random token reduction.
- 4-bit quantized model.
- Optional pruning plus quantization.

Evaluate matched perturbations:

- Object removal.
- Color change.
- Spatial relocation.
- Text–image conflict.
- Fine-grained counting.
- Irrelevant background change.


### Verdict

**Reserve as a fallback pilot.**

Novelty confidence: **weak to moderate** because current token-efficiency literature is extensive and recent methods are appearing quickly.[^1_11][^1_21][^1_10]

Feasibility: **high** for inference-only evaluation.

# J. Dataset and baseline feasibility

| Top candidate | Accessible data | Split design | Minimum baseline | Main data concern |
| :-- | :-- | :-- | :-- | :-- |
| Bengali repair | BanglaVerse candidate pool; BanglaProtha possible external material | Group by original image, cultural entity, source, practice, and translated family | Small frozen VLM, no-help and single-intervention controls | Provenance, annotation quality, answer leakage |
| Action selection | Must construct matched action-outcome data from public VQA/visual reasoning tasks | Group by image, question family, task source, and action template | Fixed action policies and confidence-only rule | Dataset identity and action leakage |
| Token/evidence efficiency | POPE, MME, VQA, targeted counterfactual image edits | Group by source image and generated variant | Full-token model, random reduction, quantization | Synthetic edit artifacts and model-specific effects |

For all three, a random row split is unsafe if multiple questions, translations, captions, or generated variants share the same original image.

# K. Leakage and evaluation risks

## Bengali repair

This is the most vulnerable to intervention leakage. A cultural fact may function as an answer key, while a caption may already contain the target entity. The study should pre-register which question types are eligible for each intervention and separate answer-bearing help from non-answer-bearing help.

## Action selection

If retrieval examples come from one dataset and zoom examples from another, the policy can choose based on dataset identity. All actions need to be available for the same underlying instances, at least in an offline evaluation environment.

## Token efficiency

Synthetic edits may introduce detectable artifacts. A model may respond to editing style rather than the intended visual property. Use natural perturbations where possible and test edit-quality controls.

# L. Compute feasibility

| Candidate | Core training requirement | Approximate model strategy | Colab feasibility | Main cost |
| :-- | :-- | :-- | :-- | :-- |
| Bengali repair | None initially; optional LoRA later | SmolVLM-500M/2.2B or another small quantized VLM | High for a pilot | Number of condition–item generations |
| Action selection | Small controller training optional | Offline logs from one small VLM; train a lightweight classifier/regressor | Medium | Action-outcome construction |
| Token/evidence efficiency | None | One small VLM plus several compression settings | High | Repeated inference and image preprocessing |

Do not begin with multiple 7B models. First verify the phenomenon on one reproducible open model. Only add a second family if the effect is large enough to justify cross-model testing.

# M. Negative-result value

| Candidate | Useful negative result |
| :-- | :-- |
| Bengali repair | No interaction between help types; knowledge-only repair dominates; interventions harm correct answers; effects fail to transfer |
| Action selection | Confidence-only policies match learned value selection; no policy generalizes across action types; action costs erase gains |
| Token efficiency | Compression does not selectively damage evidence use; reliability remains on the same Pareto frontier as accuracy; effects are model-specific |

RQ 1 has the strongest negative-result value because it can reject competing explanations rather than merely report a small score difference.

# N. Recommended next investigation

## One next investigation

Conduct a **targeted literature and data audit of RQ 1: controlled visual–linguistic–cultural repair of Bengali cultural VLM failures**.

Do not yet build the full intervention dataset. In a 30–90 minute session:

1. Read the full methodology, experiments, and limitations of BanglaVerse, M4-RAG, and BLEnD-Vis.
2. Search 2025–2026 papers for the exact combinations:
    - cultural VLM error attribution;
    - visual clarification plus cultural knowledge;
    - Bengali cultural VQA intervention;
    - perception–language–knowledge bottleneck decomposition;
    - multimodal repair interaction.
3. Inspect BanglaVerse and BanglaProtha metadata, licenses, provenance, duplicates, and answer leakage.
4. Select 20 candidate items and manually classify:
    - visual-observation question;
    - language/dialect-sensitive question;
    - cultural-knowledge question;
    - answer-bearing assistance risk;
    - likely intervention independence.
5. Record a provisional verdict:
    - **continue** if at least 15 of 20 items support independently controllable interventions;
    - **narrow** if only one question family is clean;
    - **park** if intervention independence cannot be established;
    - **reject** if the dataset is mostly answer-leaking or source-dependent.

This is the most informative next action because it tests the two uncertainties that literature alone cannot resolve: whether the claimed gap survives the newest papers and whether the available data can support a valid intervention experiment.

**Decision-log entry**


| Date | Candidate | Verdict | Evidence-based reason | Next action |
| :-- | :-- | :-- | :-- | :-- |
| 2026-09-20 | Cross-modal AI — controlled Bengali cultural VLM repair | Continue to targeted verification; not chosen | Existing work supports cultural VLM difficulty and knowledge/representation interventions, but the interaction among independently controlled visual, linguistic, and cultural help remains unresolved in the inspected evidence. Feasibility depends on leakage-resistant annotations and provenance checks. | Audit full closest papers and inspect 20 BanglaVerse/BanglaProtha items for intervention independence, licensing, duplicates, and answer leakage. |

<span style="display:none">[^1_22][^1_23][^1_24][^1_25][^1_26][^1_27][^1_28][^1_29][^1_30][^1_31][^1_32][^1_33][^1_34][^1_35][^1_36][^1_37][^1_38][^1_39][^1_40][^1_41][^1_42][^1_43][^1_44][^1_45][^1_46][^1_47][^1_48][^1_49][^1_50][^1_51][^1_52][^1_53][^1_54][^1_55][^1_56][^1_57][^1_58][^1_59][^1_60][^1_61][^1_62][^1_63][^1_64][^1_65][^1_66][^1_67][^1_68][^1_69][^1_70][^1_71][^1_72][^1_73]</span>

<div align="center">⁂</div>

[^1_1]: https://arxiv.org/abs/2403.20330

[^1_2]: https://arxiv.org/html/2410.10563

[^1_3]: https://arxiv.org/html/2604.09364v1

[^1_4]: https://arxiv.org/html/2608.04244v1

[^1_5]: https://arxiv.org/html/2410.08145

[^1_6]: https://arxiv.org/abs/2410.03659

[^1_7]: https://arxiv.org/html/2508.00378v2

[^1_8]: https://arxiv.org/html/2509.24072v1

[^1_9]: https://arxiv.org/html/2504.05299v1

[^1_10]: https://arxiv.org/pdf/2601.22674.pdf

[^1_11]: https://aclanthology.org/2026.acl-long.328.pdf

[^1_12]: https://openaccess.thecvf.com/content/CVPR2026/papers/Huang_VL-RouterBench_A_Benchmark_for_Vision-Language_Model_Routing_CVPR_2026_paper.pdf

[^1_13]: https://arxiv.org/html/2605.21796v1

[^1_14]: https://arxiv.org/html/2502.15563v1

[^1_15]: Idea_First_Thesis_Research_and_Recommendation.md

[^1_16]: https://huggingface.co/HuggingFaceTB/SmolVLM-256M-Instruct

[^1_17]: https://huggingface.co/HuggingFaceTB/SmolVLM-500M-Instruct

[^1_18]: https://huggingface.co/docs/transformers/v4.45.2/model_doc/llava_next

[^1_19]: https://arxiv.org/html/2608.04509v1

[^1_20]: https://arxiv.org/html/2607.28991v1

[^1_21]: https://arxiv.org/html/2609.16841v1

[^1_22]: Thesis_Topic_Discovery_Handover.md

[^1_23]: Cross-modal-evidence-use-and-source-arbitration.md

[^1_24]: https://arxiv.org/abs/2501.02189

[^1_25]: https://aclanthology.org/2026.findings-acl.1416.pdf

[^1_26]: https://arxiv.org/abs/2307.06281

[^1_27]: https://openaccess.thecvf.com/content/CVPR2026/papers/Wu_Grounded_Chain-of-Thought_for_Multimodal_Large_Language_Models_CVPR_2026_paper.pdf

[^1_28]: https://aclanthology.org/2026.magmar-main.14.pdf

[^1_29]: https://arxiv.org/abs/2405.08807

[^1_30]: https://arxiv.org/abs/2408.07543

[^1_31]: https://arxiv.org/abs/2308.02490

[^1_32]: https://arxiv.org/html/2402.14973v4

[^1_33]: https://arxiv.org/abs/2603.13370

[^1_34]: https://arxiv.org/abs/2306.13549

[^1_35]: https://web3.arxiv.org/pdf/2601.04777

[^1_36]: https://arxiv.org/html/2604.24396v1

[^1_37]: https://arxiv.org/abs/2404.05465

[^1_38]: https://arxiv.org/html/2605.30912v1

[^1_39]: https://arxiv.org/abs/2403.00231

[^1_40]: https://arxiv.org/html/2605.16411v1

[^1_41]: https://arxiv.org/abs/2502.00718

[^1_42]: https://arxiv.org/html/2606.28273

[^1_43]: https://arxiv.org/abs/2403.14972

[^1_44]: https://pmc.ncbi.nlm.nih.gov/articles/PMC11645129/

[^1_45]: https://huggingface.co/blog/smolvlm

[^1_46]: https://huggingface.co/HuggingFaceTB/SmolVLM-Base

[^1_47]: https://arxiv.org/abs/2408.01050

[^1_48]: https://github.com/LLaVA-VL/LLaVA-NeXT

[^1_49]: https://arxiv.org/abs/2311.01282

[^1_50]: https://github.com/LLaVA-VL/LLaVA-NeXT/tree/inference

[^1_51]: https://arxiv.org/html/2503.15798

[^1_52]: https://arxiv.org/abs/2404.03353

[^1_53]: https://arxiv.org/abs/2402.04624

[^1_54]: https://huggingface.co/HuggingFaceTB/SmolVLM2-2.2B-Instruct

[^1_55]: https://arxiv.org/html/2409.15889

[^1_56]: https://arxiv.org/abs/2312.17238

[^1_57]: https://github.com/haotian-liu/LLaVA

[^1_58]: https://arxiv.org/abs/2311.03079

[^1_59]: https://github.com/LLaVA-VL/LLaVA-NeXT/blob/main/docs/LLaVA-NeXT-Video_0716.md

[^1_60]: https://arxiv.org/abs/2409.11887

[^1_61]: https://arxiv.org/html/2508.04227v3

[^1_62]: https://arxiv.org/abs/2512.03794

[^1_63]: https://openreview.net/pdf/14c4e508bf4be46736eead41b02786b05f4ebf4f.pdf

[^1_64]: https://arxiv.org/html/2604.12033

[^1_65]: https://arxiv.org/html/2504.03748v2

[^1_66]: https://arxiv.org/html/2511.21717

[^1_67]: https://arxiv.org/html/2501.02699v1

[^1_68]: https://arxiv.org/html/2605.22902

[^1_69]: https://raw.githubusercontent.com/LLaVA-VL/LLaVA-NeXT/main/docs/LLaVA-NeXT.md

[^1_70]: https://codersera.com/blog/run-smolvlm2-22b-on-macos-installation-guide/

[^1_71]: https://llava-vl.github.io/blog/2024-04-30-llava-next-video/

[^1_72]: https://llava-vl.github.io/blog/2024-05-10-llava-next-stronger-llms/

[^1_73]: https://ossmodeldb.com/models/qwen2-5-vl-7b-instruct/q2-k-l


---

# Candidate-by-candidate novelty audit

This pass treats every candidate as **guilty until proven innocent**. For each question I searched for 2024–2026 work that already answers it or makes it substantially occupied, then judged whether any remaining difference is scientifically meaningful.

All literature claims below come from the attached cross-modal report and targeted 2024–2026 searches. Where the report cites specific papers, I treat those as the closest work unless a newer paper directly supersedes them.

______________________________________________________________________

## F1 — “Does the VLM use the image or a language prior?”

**Closest direct paper**

- *Are We on the Right Way for Evaluating Large Vision-Language Models?* (2024) explicitly shows that many VQA-style items can be answered without visual input, and that language priors and shortcuts explain a substantial part of reported performance.[^2_1]
- Multiple 2025–2026 hallucination and evidence-use surveys and benchmarks (e.g., POPE, HallusionBench, CHAIR-based analyses) operationalize “image use” via blind tests and counterfactuals.[^2_2][^2_3]

**Closest benchmark**

- POPE, MME, MMBench, HallusionBench, and related object-existence / hallucination benchmarks already implement image-removed or adversarial splits to test reliance on non-visual priors.[^2_4][^2_5]

**Closest methodology**

- Blind (no-image) baselines, text-only controls, and counterfactual image edits are now standard in hallucination and evaluation-validity work.[^2_1][^2_2]

**Exact overlap**

- The core question—“does the model use the image or just language priors?”—is already the central motivation for a large subfield of hallucination and benchmark-validity research.
- Your own attached report notes that “a correct answer is not evidence of evidence use” and that counterfactual image edits are required; that is exactly what POPE/HallusionBench-style work already does.[^2_6]

**Remaining difference**

- You could narrow to a specific task family (e.g., Bengali cultural VQA, scientific figures, charts) or a specific failure mode (e.g., spatial relations, counting).
- You could add a more refined intervention (e.g., evidence-region masking versus full image removal).

**Is the difference scientifically meaningful?**

- Only if the narrow setting exposes a mechanism that existing benchmarks cannot distinguish (e.g., cultural knowledge versus perception versus language).
- As stated, the general question is **occupied**.

**Verdict:** **OCCUPIED**

______________________________________________________________________

## F2 — “When image and text disagree, what decides the answer?” (graded evidence quality, single-source filter)

**Closest direct paper**

- *Which Source Wins? Task-Dependent Reliance in Vision-Language Models* (arXiv 2608.17205, 2026) constructs image–text conflicts from GSM8K, SVAMP, and ChartQA, degrades either modality, and evaluates six open VLMs. It reports task-dependent reversal of modality reliance and adjusts for unimodal accuracy loss.[^2_6]
- C³PO (arXiv 2608.05381, 2026) and CMC-Bench (2026) are cited in your reports as evaluating cross-modal composition, conflict types, and abstention.[^2_6]

**Closest benchmark**

- ChartQA-Conflict and the GSM8K/SVAMP conflict stimuli from *Which Source Wins?* are direct conflict benchmarks with degradation.[^2_6]
- SIGNPOST-Bench (2026) provides controlled counterfactual image variants for text–vision conflict.[^2_7]

**Closest methodology**

- Counterbalanced source roles, graded degradation, and single-source accuracy measurement are all present or closely approximated in *Which Source Wins?* and related conflict papers.[^2_6]

**Exact overlap**

- Your proposed design (counterbalanced conflicts, degraded image/text, single-source sufficiency filter, quality-tracking curve) is largely a **refinement** of an existing protocol rather than a new question.
- The attached report explicitly states: “My F2 recommendation is mostly undercut” by *Which Source Wins?*, which already has counterbalanced A/B labels, both degradation arms, and severity adjustment.[^2_6]

**Remaining difference**

- Finer grading of quality levels.
- Severity matched by measured single-source accuracy rather than level index.
- Same-question conflicts with directness controlled (e.g., chart computations versus text-stated numbers).

**Is the difference scientifically meaningful?**

- These are **incremental identification improvements**, not a new phenomenon.
- They matter methodologically but do not establish a new research question.

**Verdict:** **PARTIALLY OCCUPIED** (core question answered; narrow identification refinements remain)

______________________________________________________________________

## F3 — “After a source is declared invalid, does the model retract only dependent conclusions?”

**Closest direct paper**

- MMA (multimodal memory and belief updating, 2026) and DeltaLogic (logical belief revision under premise edits, 2026) study retraction and stability when evidence or premises change.[^2_8]
- SpaMEM (2026) studies changing spatial situations, including removal events, though focused on physical disappearance rather than evidential validity.[^2_8]

**Closest benchmark**

- No widely adopted benchmark specifically for “source-withdrawal with dependency graphs” in generative VLMs is yet dominant, but belief-revision and memory-updating benchmarks exist in adjacent areas.[^2_8]

**Closest methodology**

- Claim-and-source ledgers, symbolic dependency graphs, and prompted revision are all explored in multimodal memory and agent-memory work.[^2_8]

**Exact overlap**

- The general question—“does the model update conclusions when a source is invalidated?”—is already studied in multimodal memory and belief-revision contexts.
- Your attached report classifies this as “partially explored” and notes that a full comparison with truth-maintenance and provenance literature is needed before asserting novelty.[^2_8]

**Remaining difference**

- A tightly controlled VLM experiment with explicit dependency labels and independent corroboration checks, focusing on **evidence withdrawal** rather than physical scene changes.

**Is the difference scientifically meaningful?**

- Potentially, if you can construct clean dependency graphs and show that existing memory/updating work does not cover your specific evidential-withdrawal setting.
- However, the conceptual space is already occupied; the contribution would be a **narrow, well-identified variant**, not a new question.

**Verdict:** **PARTIALLY OCCUPIED**

______________________________________________________________________

## F4 — “Does an acceptance threshold fit on clean inputs transfer under degradation?” (calibration / selective prediction)

**Closest direct paper**

- *Knowing When Not to Answer: Evaluating Abstention in Multimodal Reasoning Systems* (2026) studies abstention clauses, selective risk, and calibration under multimodal reasoning.[^2_9]
- *Explicit Abstention Knobs for Predictable Reliability* (2026) evaluates confidence thresholds, coverage, and risk under evidence degradation in video-language settings.[^2_10]
- *Respect Your Zero-Shot Uncertainty: Conservative Calibration* (2026) shows that test-time adaptation can degrade calibration and that entropy reduction does not imply better reliability.[^2_11]

**Closest benchmark**

- Selective prediction and abstention benchmarks for LLMs and VLMs increasingly report selective risk, coverage, and calibration under corruption or distribution shift.[^2_9][^2_10]

**Closest methodology**

- Fixed clean thresholds, degradation ladders, and selective-risk curves are already used in abstention and calibration studies.[^2_10][^2_9]

**Exact overlap**

- Your own audit already reports “direct overlap” for F4.[^2_6]
- The attached report lists “modality degradation and calibrated uncertainty” as a top candidate but explicitly ties it to *Which Source Wins?*’s limitation that uncertainty/abstention is untested.[^2_6]

**Remaining difference**

- A specific combination of task, degradation type, and threshold-transfer analysis could still be novel in detail.
- But the **phenomenon** (thresholds learned on clean data may not transfer under degradation; calibration may worsen) is already established.

**Is the difference scientifically meaningful?**

- Only if you identify a specific, previously unmeasured interaction (e.g., modality-specific degradation, language-conditioned calibration failure).
- As a general question, it is **partially occupied**.

**Verdict:** **PARTIALLY OCCUPIED**

______________________________________________________________________

## F5 — “Does a VLM judge actually look at the image?” (VLM-as-judge grounding)

**Closest direct paper**

- *Visuals Lie, Consistency Speaks* (2025/2026) evaluates whether attention and visual signals correlate with correctness, finding weak structural correlations and stronger signals from self-consistency and hidden states.[^2_6]
- Multiple 2024–2026 works on VLM-as-judge and automated evaluation implicitly or explicitly test whether judges are sensitive to visual changes.

**Closest benchmark**

- VLM-as-judge setups in RLHF, preference optimization, and automated evaluation often include image-swapped or perturbed controls, though not always systematically.

**Closest methodology**

- Image-swap controls, unrelated-image baselines, and text-only judge conditions are already used to test judge grounding.

**Exact overlap**

- The core suspicion—“judges may mostly read the answer text, not the image”—is already a known concern in automated evaluation and consistency studies.
- Your attached report classifies this as “Reserve. Cheap, but a measurement note more than a thesis.”[^2_6]

**Remaining difference**

- A focused audit on a specific judge setup (e.g., a particular VLM-as-judge protocol for VQA or cultural evaluation) could still be useful as a **measurement study**.

**Is the difference scientifically meaningful?**

- As a standalone thesis question, it is weak; as a **diagnostic** within a larger study, it is valuable.
- The general phenomenon is already recognized.

**Verdict:** **PARTIALLY OCCUPIED** (better as a measurement tool than a thesis core)

______________________________________________________________________

## F6 — “Does visual-token reduction hurt evidence-critical tokens or redundant ones?”

**Closest direct paper**

- *How Many Visual Tokens Do Multimodal Language Models Need?* (2026) studies training-free token pruning across Qwen3-VL models, showing that token demand varies with scale, task, and retention level.[^2_6]
- *Visual Token Compression Enhances Robustness of MLLMs* (2026) claims that pruning can reduce hallucinations and improve robustness.[^2_12]
- *When Does Visual Token Pruning Improve Calibration?* (2026) directly studies how pruning affects calibration and overconfidence, showing that which tokens are kept matters for reliability.[^2_13]
- AgilePruner (2026) and SeeMe (2026) analyze attention-based versus diversity-based pruning and their effects on hallucination.[^2_14][^2_15]

**Closest benchmark**

- POPE, HallusionBench, CHAIR, and other hallucination/robustness benchmarks are already used to evaluate pruning methods’ reliability effects.[^2_12][^2_13]

**Closest methodology**

- Random versus importance-based pruning, evidence-region overlap analysis, and calibration metrics under pruning are all present in 2025–2026 work.[^2_16][^2_13][^2_12]

**Exact overlap**

- Your attached report explicitly lists “visual-token efficiency” as occupied for method development, with the remaining question being whether compression causes **selective evidence loss**.[^2_6]
- Recent papers already show that pruning can change hallucination rates and calibration, and that kept-set coverage is strongly associated with accuracy and overconfidence.[^2_13][^2_12]

**Remaining difference**

- A narrow audit focusing on **evidence-type stratification** (OCR, spatial, small-object, conflict-resolution) rather than average accuracy could still add value.
- But the core idea—“pruning may selectively damage evidence-critical tokens”—is already being studied.

**Is the difference scientifically meaningful?**

- Yes, if you show that certain evidence types degrade earlier than others under realistic pruning, and that this is not captured by existing benchmarks.
- However, this is now a **refinement** within an active subfield, not a new question.

**Verdict:** **PARTIALLY OCCUPIED**

______________________________________________________________________

## F7 — “Bengali VQA failure: language understanding or cross-lingual visual grounding?”

**Closest direct paper**

- *Evaluating Multilingual VLMs for Bengali Culture Understanding* (BanglaVerse, 2026) evaluates Bengali cultural VQA with native questions and answer options, and explicitly studies dialect variation and robustness.[^2_17]
- M4-RAG (2025) and BLEnD-Vis (2025) study cultural knowledge augmentation and aligned cultural questions across textual and visual forms.[^2_8]

**Closest benchmark**

- BanglaVerse is a direct Bengali cultural VQA benchmark with dialect and language-shift analysis.[^2_17]

**Closest methodology**

- Translate-test controls, image-only-answerable items, and parallel-question designs are all discussed in your attached report and in the Bengali VLM literature.[^2_8][^2_6]

**Exact overlap**

- The generic question—“is Bengali VQA failure due to language or visual grounding?”—is already a central motivation for BanglaVerse and related work.
- Your attached report downgrades F8 (Bengali cultural repair) for answer leakage, regression to the mean, and annotation burden, and notes that generic Bengali-VLM application questions are weak and likely occupied.[^2_8][^2_6]

**Remaining difference**

- A tightly controlled decomposition that isolates comprehension versus alignment versus knowledge, with parallel data and leakage-resistant splits, could still be scientifically useful.
- But the broad question is already being asked.

**Is the difference scientifically meaningful?**

- Only if the decomposition reveals a mechanism that existing Bengali/multilingual evaluations cannot distinguish.
- As stated, the question is **partially occupied**.

**Verdict:** **PARTIALLY OCCUPIED**

______________________________________________________________________

## F8 — “Which intervention combination ‘repairs’ Bengali cultural VQA errors?”

**Closest direct paper**

- M4-RAG (2025) already compares cultural VQA with oracle knowledge and retrieved context, including language conditions.[^2_8]
- BanglaVerse (2026) evaluates Bengali cultural VQA and discusses difficulty and error patterns.[^2_17]
- BLEnD-Vis (2025) aligns cultural questions across textual rephrasing and visual formats.[^2_8]

**Closest benchmark**

- BanglaVerse and M4-RAG together provide cultural VQA with knowledge and language interventions.[^2_17][^2_8]

**Closest methodology**

- Factorial designs with visual, linguistic, and knowledge help are conceptually similar to M4-RAG’s knowledge-augmentation experiments and BanglaVerse’s dialect analysis.

**Exact overlap**

- Your attached report explicitly downgrades F8: “Downgrade. The causal reading is not defensible at undergraduate annotation scale.”[^2_6]
- It also notes that “knowledge helps cultural VQA” is already too weak as a contribution given M4-RAG.[^2_8]

**Remaining difference**

- A fully leakage-controlled factorial design with native-speaker validation could still be stronger than existing work.
- But the core idea—“interventions can repair cultural VQA errors”—is already explored.

**Is the difference scientifically meaningful?**

- Only if you show **interaction effects** that existing work does not measure, and if you can control leakage convincingly.
- Given annotation burden and leakage risks, this is a **high-risk, partially occupied** direction.

**Verdict:** **PARTIALLY OCCUPIED** (high burden, leakage risk)

______________________________________________________________________

## F9 — “Can a predictor pick the action (zoom, crop, resolution) with real gain?”

**Closest direct paper**

- BCEA (2026) studies budgeted evidence acquisition before abstention in VLMs, including visual interventions and calibration of the resulting policy.[^2_8]
- ClearVQA (2025) studies clarification of ambiguous visual questions.[^2_8]
- TRUST (2026) studies uncertainty-aligned agent decisions among direct answering, tools, asking, and inability to answer.[^2_8]
- VL-RouterBench (CVPR 2026) benchmarks VLM routing systems.[^2_18]

**Closest benchmark**

- BCEA and VL-RouterBench provide direct precedents for action selection and routing evaluation.

**Closest methodology**

- Offline action-outcome construction, oracle action policies, and uncertainty-based baselines are all present in BCEA/TRUST-style work.

**Exact overlap**

- Your attached report keeps only the zoom/resolution version and rejects clarify/retrieve actions for scope reasons, but acknowledges “close overlap with active-perception and abstain-then-look-again work.”[^2_6]

**Remaining difference**

- A narrow focus on **zoom/resolution** with deterministic decoding and paired runs could still be a clean undergraduate study.
- But the general question—“can a model choose useful information actions?”—is already occupied.

**Is the difference scientifically meaningful?**

- Only if you show that expected gain prediction generalizes beyond uncertainty and seen task/action pairs.
- As a broad question, it is **occupied**; as a narrow zoom/resolution audit, it is **partially occupied**.

**Verdict:** **PARTIALLY OCCUPIED** (narrow zoom/resolution variant may survive)

______________________________________________________________________

## F10 — “Is the same fact stored differently when cued by an image vs a name?” (cross-modal knowledge consistency)

**Closest direct paper**

- Cross-modal knowledge consistency and modality-specific storage are explored in multimodal representation and probing work, including studies of shared versus modality-specific knowledge.

**Closest benchmark**

- Multimodal probing and consistency benchmarks (e.g., MM-Vet, MEGA-Bench) include tasks that indirectly test cross-modal knowledge access.[^2_19][^2_20]

**Closest methodology**

- Matched entity cues, consistency metrics, and modality-specific probing are established methods.

**Exact overlap**

- Your attached report classifies F10 as “Likely occupied.”[^2_6]

**Remaining difference**

- A specific fact family or domain (e.g., cultural facts, scientific concepts) could still be interesting.
- But the general question is already studied in multimodal representation research.

**Verdict:** **OCCUPIED**

______________________________________________________________________

## F11 — “Do alignment scores (CLIP-style) track meaning or bag-of-words?”

**Closest direct paper**

- Compositional versus lexical alignment is heavily studied in vision-language representation work, including hard-negative benchmarks and compositional reasoning evaluations.

**Closest benchmark**

- Multiple compositional VQA and image-text retrieval benchmarks explicitly test bag-of-words versus compositional understanding.

**Exact overlap**

- Your attached report classifies F11 as “Heavily worked already.”[^2_6]

**Verdict:** **OCCUPIED**

______________________________________________________________________

## F12 — “Modality imbalance, test-time adaptation, RL-based methods”

**Closest direct paper**

- MuRA (2026) studies dynamic multi-rank adaptation for CLIP under multiple ImageNet variants and cross-domain datasets.[^2_6]
- Multiple 2025–2026 TTA papers for VLMs study entropy minimization, reliability-aware regularization, and majorization-guided adaptation.[^2_21][^2_22][^2_11]

**Closest benchmark**

- ImageNet-A/R/V2/S and cross-domain classification benchmarks are standard for TTA evaluation.

**Exact overlap**

- Your attached report explicitly rejects F12 for this scope: “Algorithmic TTA is occupied and rapidly moving. A thesis should not reproduce another adaptive-rank method.”[^2_6]

**Verdict:** **OCCUPIED** (for method development; audit of side effects may survive)

______________________________________________________________________

# Summary table

| Family | Verdict | Reason |
| :-- | :-- | :-- |
| F1 (image vs prior) | OCCUPIED | Blind tests and counterfactuals are standard in hallucination/evaluation-validity work. |
| F2 (graded conflict arbitration) | PARTIALLY OCCUPIED | *Which Source Wins?* and C³PO/CMC-Bench already address core design; only incremental refinements remain. |
| F3 (source withdrawal) | PARTIALLY OCCUPIED | Multimodal memory/belief-revision work exists; narrow evidential-withdrawal variant may survive. |
| F4 (threshold transfer / calibration) | PARTIALLY OCCUPIED | Abstention and calibration under degradation are already studied; specific interactions may remain. |
| F5 (VLM judge grounding) | PARTIALLY OCCUPIED | Known concern; better as a diagnostic than a thesis core. |
| F6 (token pruning vs evidence) | PARTIALLY OCCUPIED | Pruning–reliability–hallucination links are already studied; evidence-type stratification may add value. |
| F7 (Bengali failure decomposition) | PARTIALLY OCCUPIED | BanglaVerse and related work already ask this; narrow decomposition could still be useful. |
| F8 (Bengali repair combinations) | PARTIALLY OCCUPIED | M4-RAG and BanglaVerse already explore interventions; leakage and annotation burden are major risks. |
| F9 (action-value prediction) | PARTIALLY OCCUPIED | BCEA, TRUST, VL-RouterBench occupy the general question; narrow zoom/resolution audit may survive. |
| F10 (cross-modal knowledge storage) | OCCUPIED | Multimodal representation/probing work already addresses this. |
| F11 (alignment scores vs meaning) | OCCUPIED | Compositional alignment is heavily studied. |
| F12 (TTA / modality imbalance) | OCCUPIED | TTA and adaptation methods are crowded; audit of side effects may survive. |


______________________________________________________________________

# Surviving cores (if any)

After this adversarial pass, the only branches that still have **scientifically meaningful** unresolved questions are:

1. **F2 refined:** Does explicit **conflict detection** (not just forced arbitration) improve decisions and calibrated uncertainty? This builds on *Which Source Wins?*’s limitation that uncertainty/abstention is untested.[^2_6]
2. **F6 refined:** Does visual-token compression selectively damage **evidence-type-specific reliability** (OCR, spatial, small-object, conflict) rather than uniformly degrading accuracy? Recent work shows pruning affects calibration and hallucination, but evidence-type stratification is not fully mapped.[^2_12][^2_13]
3. **F4/F9 refined:** Under modality degradation, do **uncertainty/abstention mechanisms** and **action-selection policies** generalize across tasks and modalities, or do they learn dataset/action shortcuts? BCEA/TRUST/abstention papers exist, but cross-task generalization is not fully settled.[^2_9][^2_10][^2_8]

All other families are either **occupied** or only survivable as narrow measurement studies rather than primary thesis questions.

<span style="display:none">[^2_23][^2_24][^2_25][^2_26][^2_27][^2_28][^2_29][^2_30][^2_31][^2_32][^2_33][^2_34][^2_35][^2_36][^2_37][^2_38][^2_39][^2_40][^2_41][^2_42][^2_43][^2_44][^2_45][^2_46][^2_47][^2_48][^2_49][^2_50][^2_51][^2_52][^2_53][^2_54][^2_55][^2_56]</span>

<div align="center">⁂</div>

[^2_1]: https://arxiv.org/abs/2403.20330

[^2_2]: https://arxiv.org/abs/2404.18930

[^2_3]: https://arxiv.org/html/2507.19024v2

[^2_4]: https://aclanthology.org/2026.acl-long.328.pdf

[^2_5]: https://arxiv.org/abs/2307.06281

[^2_6]: Cross-modal-evidence-use-and-source-arbitration.md

[^2_7]: https://arxiv.org/html/2608.04244v1

[^2_8]: Idea_First_Thesis_Research_and_Recommendation.md

[^2_9]: https://arxiv.org/html/2604.14799

[^2_10]: https://arxiv.org/html/2601.00138v1

[^2_11]: https://arxiv.org/html/2608.05945v1

[^2_12]: https://arxiv.org/html/2607.22716v1

[^2_13]: https://arxiv.org/html/2604.12035v2

[^2_14]: https://arxiv.org/html/2603.01236

[^2_15]: https://arxiv.org/html/2607.04163v1

[^2_16]: https://arxiv.org/html/2607.01444v1

[^2_17]: https://arxiv.org/html/2603.21165v1

[^2_18]: https://openaccess.thecvf.com/content/CVPR2026/papers/Huang_VL-RouterBench_A_Benchmark_for_Vision-Language_Model_Routing_CVPR_2026_paper.pdf

[^2_19]: https://arxiv.org/abs/2308.02490

[^2_20]: https://arxiv.org/html/2410.10563

[^2_21]: https://arxiv.org/html/2506.24000

[^2_22]: https://arxiv.org/html/2604.24602v1

[^2_23]: https://arxiv.org/abs/2404.11129

[^2_24]: https://arxiv.org/html/2605.27906v1

[^2_25]: https://arxiv.org/abs/2310.16045

[^2_26]: https://arxiv.org/abs/2402.09801

[^2_27]: https://arxiv.org/html/2408.09429v2

[^2_28]: https://arxiv.org/abs/2408.01355

[^2_29]: https://arxiv.org/html/2306.14565

[^2_30]: https://arxiv.org/html/2608.23921

[^2_31]: https://arxiv.org/html/2503.00361v1

[^2_32]: https://arxiv.org/html/2607.28341v1

[^2_33]: https://direct.mit.edu/tacl/article/doi/10.1162/tacl_a_00695/124459/Investigating-Hallucinations-in-Pruned-Large

[^2_34]: https://arxiv.org/html/2604.21360v2

[^2_35]: https://aclanthology.org/2022.findings-emnlp.48.pdf

[^2_36]: https://arxiv.org/html/2608.17084v1

[^2_37]: https://arxiv.org/abs/2306.01265

[^2_38]: https://arxiv.org/abs/2310.00647

[^2_39]: https://arxiv.org/abs/2402.10884

[^2_40]: https://arxiv.org/abs/2503.15850

[^2_41]: https://arxiv.org/abs/2408.02340

[^2_42]: https://arxiv.org/abs/2408.16625

[^2_43]: https://arxiv.org/html/2501.18864

[^2_44]: https://arxiv.org/abs/2309.16412v1

[^2_45]: https://arxiv.org/html/2506.10085

[^2_46]: https://arxiv.org/abs/2407.21174

[^2_47]: https://arxiv.org/html/2412.14660v2

[^2_48]: https://arxiv.org/html/2605.14115v1

[^2_49]: https://arxiv.org/html/2510.19183v1

[^2_50]: https://arxiv.org/html/2606.24165v1

[^2_51]: https://arxiv.org/html/2506.10085v5

[^2_52]: https://arxiv.org/html/2605.18111

[^2_53]: https://arxiv.org/html/2604.18347v1

[^2_54]: https://arxiv.org/html/2608.18339v1

[^2_55]: https://arxiv.org/html/2607.24875v1

[^2_56]: https://arxiv.org/html/2504.18346v4

