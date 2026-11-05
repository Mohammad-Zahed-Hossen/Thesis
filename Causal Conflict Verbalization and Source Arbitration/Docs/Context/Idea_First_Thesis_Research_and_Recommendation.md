# Research Priorities and Candidate Directions (Historical Ideation Archive)

> [!IMPORTANT]
> **DOCUMENT STATUS: HISTORICAL ARCHIVE — SUPERSEDED & RESOLVED (24 September 2026)**  
> This document records early exploratory ideation from September 2026. On 23–24 September 2026, an exhaustive adversarial audit (`final_adversarial_thesis_decision_audit.md`) evaluated all candidates against primary literature:
> - **Candidate 1 (Cultural VLM Repair / Proposal 3):** **DEPRECATED** — Layer 18 bottleneck was an unverified assumption; method partially pre-empted by *BabelSteering* (Aug 2026).
> - **Candidate 2 (Multimodal Agents):** **PARKED** — Reinforcement learning policies triggered CUDA OOMs on Colab; literature saturated by *AdaTooler-V* and *ToolGate*.
> - **Candidate 3 (Medical Imaging):** **PARKED** — Severe cross-dataset contamination between ISIC/HAM10000; lacks AI/CSE algorithmic novelty.
> 
> **CANONICAL TOPIC FROZEN & VALIDATED:**  
> **"Causal Conflict Verbalization and Source Arbitration in Vision-Language Models"**  
> *Has been 100% executed across the full population ($N=1,619$), confirming $+63.74\text{ pp}$ shift ($p = 1.20 \times 10^{-215}$). Refer to [`CANONICAL_THESIS_MASTER_REPORT.md`](file:///d:/Thesis/Important/Cross%20Modal/Finalize%20Topic/CANONICAL_THESIS_MASTER_REPORT.md) for the active single source of truth.*

## Historical Strategic Decision (Preserved for Context)

Under the modernized constraints—with commercial API budgets (GPT-4o, Claude 3.5 Sonnet, Gemini 1.5 Pro) permitted, rigid time bottlenecks removed, and methodological/agentic contributions welcomed—two premier candidates were initially evaluated:

1. **Candidate 1 (Cultural VLM Repair):** *Which combinations of visual, linguistic, and cultural information repair Bengali cultural VLM errors?* (High cultural relevance, grounded failure analysis, supported by frontier API baselines and judges).
2. **Candidate 2 (Multimodal Agent Active Perception & Tool Selection):** *Can a multimodal agent predict action value across active perception (zooming, cropping), tool invocation, and abstention to maximize answer accuracy under budget?* (Elevated to co-equal primary priority due to API-powered tool environments, agentic execution benchmarks, and methodological novelty).

## Candidate Comparison Under Modernized Constraints

| Priority | Research question | Main contribution to pursue | Strategic advantage with APIs & Modern Velocity |
|---|---|---|---|
| **1 — Premier: Bengali + VLM Repair** | Which information repairs cultural VQA failures, alone or in combination? | Controlled within-question intervention data and empirical repair dynamics | Frontier APIs (GPT-4o, Gemini 1.5) serve as strong reference baselines and validated evaluators |
| **2 — Premier: Multimodal Agent Actions** | Can an agent learn action-value prediction across zooming, tool invocation, and abstention? | Novel active perception policy, tool calibration, and executable agent benchmark | API planners and tool environments make execution benchmarking rapid and reproducible |
| **3 — Active Domain: Medical Multimodal VLM** | Can multimodal VLMs accurately calibrate uncertainty and abstain on ambiguous pathology/radiology? | Diagnostic calibration, PEFT adaptation on public benchmarks (CheXpert, ISIC, BraTS) | Public expert-labeled benchmarks provide ground truth without clinical co-supervisors |
| **4 — Bengali Language** | Can dialect normalization improve downstream understanding while preserving unresolved meaning? | Ambiguity-preserving normalization and semantic-loss evaluation | Strong linguistic baseline; text-heavy focus |
| **5 — Multimodal Reasoning** | When visual/text sources are retracted, can an MLLM revise only dependent conclusions? | Provenance-sensitive belief revision and counterfactual grounding | High conceptual novelty; requires careful synthetic benchmark design |

These are alternatives. You do not need to combine them into one thesis. In particular, ideas 1 and 2 are related but distinct: the first experimentally supplies information to understand repair; the second must choose an action before observing its outcome.

## 1. Which information actually repairs Bengali cultural VLM errors?

### Why this question survived the literature check

BanglaVerse already evaluates Bengali cultural content across languages and dialects. Its latest inspected version includes manual error analysis. Crucially, Section 5 explicitly acknowledges that its domain-difficulty heuristic cannot cleanly distinguish missing knowledge from weak entity recognition or confusing options. Thus, the opening is a controlled test of competing explanations, not a claim that nobody has analyzed Bengali VLM errors. [BanglaVerse, v3, Sections 5–6](https://arxiv.org/html/2603.21165v3)

M4-RAG already compares cultural VQA with oracle knowledge and retrieved context, including language conditions. Supplying cultural facts and observing improvement is therefore insufficient as the contribution. [M4-RAG, Sections 3 and 9](https://arxiv.org/html/2512.05959v1)

BLEnD-Vis already aligns cultural questions across textual rephrasing and visual formats. Merely comparing image versus text, or English versus Bengali, would also be too close to existing work. [BLEnD-Vis, Sections 3–4](https://arxiv.org/html/2510.11178v1)

Perception-oracle experiments also exist outside cultural VQA, including work separating perception from abstract reasoning. The contribution must lie in the cultural setting’s controlled repair interactions and the conclusions they support, not in inventing oracle assistance. [Perception bottleneck study](https://arxiv.org/html/2512.21329v1)

**Proposed difference:** hold the underlying image, question intent, and answer fixed; cross independently validated forms of help; measure which repairs succeed, fail, or interfere on the same instances. The inspected predecessors motivate this experiment but do not establish its outcome. I did not find this exact combined protocol in the closest work inspected; that is a bounded literature judgment, not proof of absence throughout the field.

### A concrete illustration

Imagine a photograph of a regional agricultural practice and a question written in a regional variety of Bengali. A model gives the wrong activity name. Three explanations are plausible:

- It missed the relevant tool or the relation between the tool, animal, and crop.
- It misread the dialectal wording.
- It saw the scene and understood the wording, but lacked the relevant cultural association.

These can coexist. A dictionary-style explanation of a practice may be useless if the wrong object is being identified. Translating the question may also erase a culturally important distinction. Those are experimental possibilities, not findings we already have.

### What the experiment would contain

Construct three intervention families:

| Help | Intended change | What must be prevented |
|---|---|---|
| Visual clarification, V | Better access to relevant observable attributes, through a crop or an independently verified attribute description | Supplying the cultural entity name when that is the target answer; inventing detail absent from the image |
| Linguistic clarification, L | A native-speaker-validated rendering that preserves question intent, referents, and ambiguity | Adding missing facts, narrowing the answer, or treating English as a perfect semantic oracle |
| Cultural knowledge, K | A small verified set of relevant facts or candidate descriptions | A statement that directly identifies which answer belongs to the current image |

Evaluate all eight combinations: no help; V; L; K; V+L; V+K; L+K; V+L+K. Include initially correct questions as well as errors, because assistance can damage correct answers.

For entity-identification questions, a useful knowledge intervention might provide comparable descriptions of all candidate entities. The model still has to connect the visible attributes to the right candidate. For questions where a fact necessarily discloses the answer, classify that condition as answer-bearing assistance and analyze it separately. Do not conceal that distinction behind the word “oracle.”

A crop and a textual visual description are different interventions. Analyze them separately. A crop tests access to existing pixels; a description bypasses part of perception and changes modality. Agreement across both strengthens an interpretation, but neither proves an internal neural mechanism.

### What you would contribute

A strong completion would contain three connected outputs:

1. **An intervention resource:** questions paired with validated, source-specific forms of assistance and leakage controls.
2. **An empirical explanation:** which help works, how effects interact, and whether patterns transfer across entities, domains, dialects, and model families.
3. **An improvement informed by that explanation:** for example, better entity grounding before retrieval, or adaptation examples selected for the observed interaction. Choose the improvement after learning what fails.

The first two can form a complete scientific study if the result is substantial. Training a new router or building a chat interface is optional; neither should distract from identifying the phenomenon.

### Measurements that distinguish an answer from a leaderboard

Let Y(V,L,K) denote correctness under one intervention combination. Estimate paired population contrasts such as:

- Visual help alone: mean[Y(1,0,0) − Y(0,0,0)].
- Visual–knowledge interaction without language help: mean[Y(1,0,1) − Y(1,0,0) − Y(0,0,1) + Y(0,0,0)].
- Harm rate: fraction of initially correct answers made incorrect by a specified intervention.
- Repair rate: fraction of initially incorrect answers corrected by a specified intervention.

For each item, also record the smallest tested assistance set that produces reliable correction. Repeat model generation where stochastic variation could alter that classification. “Smallest tested set” is not proof that this is the only possible repair.

Use confidence intervals clustered by original image or entity, not by translated row. Report interactions on a declared scale; an interaction on accuracy can be influenced by floor and ceiling effects. These are causal effects of the specified input interventions under controlled evaluation, not a clean causal decomposition of hidden “vision,” “language,” and “knowledge” modules.

A text-only control, an unrelated-knowledge control, option-order changes, and answer-leakage review are essential. Where the question remains answerable without the image, report it in a separate stratum. Otherwise a language or retrieval gain can masquerade as improved visual understanding.

### Data and resource reality

The public [BanglaVerse dataset](https://huggingface.co/datasets/FaiyazAbdullah114708/BanglaVerse) provides a starting pool with aligned image/question material. Its existing captions must not automatically become neutral visual descriptions: a caption can name the answer. The paper’s Appendix A describes mixed image origins, so source-level reuse and redistribution need checking rather than inferring blanket rights from a dataset-card license. [BanglaVerse data provenance](https://arxiv.org/html/2603.21165v3)

An external Bengali cultural set could help establish generalization. [BanglaProtha’s official repository](https://github.com/farhanishmam/BanglaProtha) is a candidate, subject to checking overlap, access, and allowed reuse. Do not treat two public datasets as independent without image/entity inspection.

The scarce resource is likely qualified annotation: native dialect speakers, culturally knowledgeable reviewers, and independent checks that each intervention changes only what it claims. More GPU time cannot solve an invalid intervention. A starting design might curate several hundred original questions across contrasting cultural domains, then expand based on the uncertainty of the effects. That is a planning proposal, not a power calculation or a fixed dataset requirement.

### Conceptual execution map, after you choose

| Phase | Work | Concrete output |
|---|---|---|
| 1. Define the phenomenon | Specify what counts as observable, linguistic, cultural, ambiguous, and answer-bearing information | Annotation manual and explicit competing explanations |
| 2. Construct controlled cases | Select and supplement real questions; author V/L/K assistance independently; adjudicate leakage and ambiguity | Versioned paired intervention set |
| 3. Measure repair patterns | Evaluate full combinations and controls across several model families | Item-level repair profiles and aggregate effects |
| 4. Test generality | Hold out entities, images, domains, and dialects; test independent cultural material | Evidence about transfer and limits |
| 5. Improve the actual bottleneck | Implement one response to the strongest observed failure mechanism | An intervention or adaptation method with matched comparisons |
| 6. Package the contribution | Release permitted data/annotations, code, failure cases, and bounded conclusions | Reproducible research artifact and thesis argument |

### What could weaken or defeat the idea?

If knowledge-only assistance accounts for almost all gains and combinations add little, the result may mainly reinforce M4-RAG. It could still be useful for Bengali, but the conceptual contribution would be smaller. If leakage-free knowledge help cannot be constructed for the chosen question type, change the question type rather than making an unjustified causal claim. If effects depend on one model or one familiar entity category, the result needs narrower interpretation.

**Why I still rank it first:** it asks a consequential question already exposed by primary research, uses Bengali as a scientifically meaningful setting, and has clear outcomes that could change how people improve cultural VLMs.

## 2. Can a VLM choose the kind of help that will actually improve its answer?

### Precise question

> Among zooming, asking for clarification, retrieving external knowledge, and stopping, can a VLM select the action with the greatest expected answer improvement per cost on unfamiliar tasks?

The central distinction is between probability of being wrong and probability of benefiting from a particular action. Two questions can have similar initial confidence yet need entirely different help. A blurred object may benefit from zooming; an unclear referent from a question to the user; an unseen cultural association from knowledge retrieval. Some questions cannot be repaired with any available action.

### Closest work and the remaining burden

BCEA already studies budgeted evidence acquisition before abstention in VLMs, including visual interventions and calibration of the resulting policy. Generic “look again when uncertain” is occupied. [BCEA](https://arxiv.org/html/2606.16667v4)

ClearVQA already studies clarification of ambiguous visual questions. Asking a user rather than guessing is also occupied. [ClearVQA](https://aclanthology.org/2025.acl-long.182/)

TRUST studies uncertainty-aligned agent decisions among direct answering, tools, asking, and inability to answer. A generic uncertainty-aware action controller would be very close. [TRUST](https://arxiv.org/html/2606.06976v1)

**Proposed difference:** learn action-specific expected answer improvement from outcomes of several available information actions on the same multimodal instances, and test whether that knowledge transfers beyond the action/task combinations seen during training. This is an empirical transfer question. Expected value of information is an established principle, not a new theory to claim.

### How to make it substantial

Build an environment in which each question can be evaluated after every permitted action during offline dataset construction. Preserve the initial information available to the policy. Do not let it inspect future retrieved documents, user answers, or oracle outcomes before choosing.

On held-out examples, compare:

- Always answer, always retrieve, always zoom, and confidence-threshold rules.
- A prompted controller and a learned controller using initial uncertainty alone.
- A controller predicting the value of each action.
- An oracle that chooses the best measured action, clearly labeled unattainable at decision time.

Use a shared task construction process. If every zoom example comes from one dataset and every clarification example from another, the controller may only learn dataset identity. Include cases with several useful actions and cases with no useful action. Keep simulated clarification separate from evaluations with real human responses.

Measure correct-answer gain at matched acquisition cost, unnecessary actions, harmful actions, and regret relative to the measured action oracle. Specify costs transparently: a user interruption, retrieval request, and additional image pass are not interchangeable. Show a frontier across cost choices rather than hiding an arbitrary conversion in one score.

The research sequence is: define action semantics → collect comparable action outcomes → establish strong fixed and uncertainty-based policies → train action-value prediction → test held-out domains and action combinations → demonstrate the complete decision loop.

### Why choose it, and why not rank it first?

Choose it if you want a method-centered VLM thesis with an eventual interactive system. Its ambition is broader than idea 1. However, the literature is crowded and annotation/action infrastructure is substantial. Its contribution collapses if it simply repackages existing active perception or if a cheap task classifier matches the controller. Gap confidence is therefore moderate, even though practical importance is high.

## 3. Can Bengali dialect normalization preserve what the speaker did—and did not—say?

### Precise question

> Can a system improve downstream understanding of Bengali dialect text without changing critical meaning or resolving ambiguity that the original utterance leaves open?

A normalization can sound fluent while changing negation, who did something, quantity, time, or the range of possible interpretations. A single polished standard-Bengali sentence may commit to a meaning the original did not uniquely specify. The objective is not to regard dialect as defective; it is to understand whether an optional intermediate representation helps another model without distorting the speaker’s meaning.

### Existing work prevents an easy novelty claim

5-Dialects-BN already includes aligned dialect, transliteration, standard Bengali, and English, and investigates normalization and linguistic errors. Generic dialect-to-standard conversion and ordinary error categorization are not the gap. [5-Dialects-BN](https://arxiv.org/html/2609.09964v1)

Meaning Over Morphology already evaluates Bangla dialect translation with multiple metrics. Merely replacing BLEU with a semantic metric is also insufficient. [Meaning Over Morphology](https://aclanthology.org/2026.dialres-1.24/)

A published parallel corpus provides another possible starting point, but its single standard-language references do not automatically specify all valid interpretations. [Regional dialect parallel corpus](https://data.mendeley.com/datasets/42gvc83xkg/2)

**Proposed difference:** normalization that explicitly preserves unresolved interpretation, evaluated by the downstream decisions it changes. This could output a conservative rendering, mark a locally ambiguous span, retain the original alongside the rendering, or give a bounded set of interpretations. Each is a hypothesis to compare, not an assumed solution.

### What the research would produce

Construct a native-speaker-adjudicated set of utterances with contextual variants. Label critical semantic facts and, where necessary, multiple acceptable interpretations. Separate true linguistic ambiguity from annotator unfamiliarity and from corrupt text. A dialect expert disagreeing with a nonexpert is not automatically evidence of ambiguity.

Use natural utterances as the main evidence. Carefully validated minimal edits can test mechanisms such as negation and participant changes, but should not substitute entirely for real dialect use. Split by source, speaker where known, and shared semantic content so paraphrases do not cross train/test boundaries.

Compare direct downstream understanding, ordinary normalization, original-plus-normalized input, conservative edit constraints, and ambiguity-preserving output. Start with bounded question answering about participants, polarity, time, and quantities; free-form response evaluation can follow.

Measure downstream accuracy jointly with critical meaning changes, unsupported disambiguation, unresolved-case coverage, and useful normalization coverage. A system that copies every input or always refuses to normalize must not win by avoiding all risk. Back-translation and embedding similarity are useful diagnostics but not substitutes for native judgments on critical meaning.

The execution sequence is: define meaning invariants → annotate natural ambiguous and unambiguous cases → establish direct and normalization baselines → design one ambiguity-preserving representation → test downstream consequences → evaluate transfer to another dialect or source.

### Decision assessment

This is the best choice here if you prefer Bengali language research over vision. Its potential contribution concerns representation and downstream behavior, not simply an additional dialect dataset. It requires sustained native-speaker collaboration. If ordinary original-plus-normalized input preserves meaning just as well as the proposed method, that baseline may settle the question; inventing a complex architecture would not rescue a weak contribution.

## 4. Can a multimodal model withdraw unsupported conclusions without forgetting valid ones?

### Precise question

> After an image or text source is declared invalid, can a multimodal system remove exactly the claims that depended on it, retain independently supported claims, and propagate the change through multi-step conclusions?

Suppose an assistant concludes from two photographs and a notice that an event occurred at a particular location. One photograph is later identified as belonging to a different event. The appropriate update depends on whether the remaining evidence independently establishes the location. Removing the source does not necessarily make the earlier claim false; it may make it unknown or still supported.

### Existing work and proposed distinction

MMA already studies multimodal memory, conflicting evidence, reliability, and belief updating. Generic “update memory when evidence changes” is not a defensible gap. [MMA](https://arxiv.org/html/2602.16493v1)

DeltaLogic tests logical belief revision following minimal premise edits. Retraction and stability under changing premises are established research questions. [DeltaLogic](https://arxiv.org/html/2604.02733v1)

SpaMEM studies changing spatial situations, including removal events. Physical disappearance and withdrawal of a source’s evidential validity should be distinguished. [SpaMEM](https://arxiv.org/html/2604.22409v1)

**Proposed difference:** multimodal evidence withdrawal with explicit source dependencies and independent corroboration. The target is whether a conclusion is warranted by the remaining authorized evidence, not whether a pretrained model can still recall a fact. This is not machine unlearning.

### A complete research design

Construct evidence bundles whose support relationships can be independently checked. Include direct visual observations, statements about images, duplicate reports, genuinely independent corroboration, and multi-step consequences. Start with controlled scene-based bundles, then test whether conclusions hold for realistic documents or photo reports.

For each bundle create matched updates: remove a sole supporting source; remove redundant independent support; withdraw an irrelevant source; contradict a proposition; and reinstate a previously withdrawn source. Keep “unsupported” distinct from “false.” Define how duplicate sources share provenance rather than counting copies as independent evidence.

Compare full-context reanswering, an explicitly prompted revision system, an external claim-and-source ledger, and a symbolic dependency-tracking baseline with manually supplied graphs. The oracle graph baseline tests reasoning given perfect extraction; the end-to-end system also has to extract the right claims and support links from pixels and text. Report these separately.

Measure obsolete-claim persistence, unnecessary retractions, retained valid claims, dependency propagation, and source attribution accuracy. A system that retracts everything cannot score well. Test graph depth, duplicated-source count, and modality changes separately.

The execution sequence is: define warranted claims → create evidence and support graphs → design matched withdrawal operations → compare symbolic and model baselines → improve extraction or revision, according to the measured bottleneck → test real evidence bundles.

### Decision assessment

This is intellectually attractive and potentially useful for multimodal research assistants. It is also the least secure recommendation: a full comparison with truth-maintenance, provenance, and recent agent-memory literature is necessary before asserting methodological novelty. I include it as an ambitious alternative, not as an equally confirmed gap. It should not displace idea 1 solely because its wording sounds more novel.

## Why the earlier shortlist is no longer the main recommendation

The earlier ASR confidence, POPE confidence, Bengali answerability, and quantization/scoring questions were selected partly for inexpensive implementation and clean audits. Those are reasonable engineering constraints, but they can favor modest contributions. Under your updated objective, I would retain them as fallback projects rather than call them the strongest ideas available.

Similarly, I would not recommend generic Bengali VQA benchmarking, ordinary cultural RAG, standard dialect normalization, “ask when uncertain,” or “update memory after contradiction” as complete thesis ideas. Close predecessors already exist. The substantive opportunities above come from the specific unresolved comparisons and the evidence a study could produce.

## Research confidence and what remains open

This pass checked primary papers, relevant methods and limitations, official repositories, and dataset pages. It followed the closest conceptual overlaps rather than using missing keywords or a lack of a Bengali paper as proof of novelty. Paper versions are explicit where important, including BanglaVerse v3; a preprint’s presence is not treated as peer-review validation.

The remaining uncertainty is not a missing thesis title. It is whether the proposed phenomenon survives a properly controlled experiment. No literature search can supply that result in advance.

For idea 1, confidence is strongest in the **documented unresolved distinction** and the **value of testing repair interactions**. Confidence is lower in the independence of the assistance channels until annotations are validated. For idea 2, the main uncertainty is differentiation from existing decision policies. For idea 3, it is whether preserving ambiguity improves downstream behavior beyond strong simple baselines. For idea 4, it is both novelty and ecological validity.

My recommendation is therefore to take **idea 1** into your next deep dive, with the main question intact. Learn whether the failure needs better perception, better language access, better cultural knowledge, or their combination. Let that evidence determine the eventual method and thesis title.
