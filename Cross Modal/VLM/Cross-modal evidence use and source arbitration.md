# A. Research-question tree

The 2025–2026 literature is converging on a central issue: **a VLM can produce a correct answer without using the intended modality, and can attend to relevant visual regions without producing a reliable answer**. The strongest undergraduate-scale questions therefore study *which evidence changes a decision, under what intervention, and with what reliability cost*.

```text
Multimodal / Vision-Language Learning
│
├── 1. Cross-modal evidence use
│   ├── Failure: one modality is ignored
│   ├── Hypothesis: reliance depends on task and evidence structure
│   ├── Intervention: degrade, remove, or contradict one modality
│   └── Outcome: modality reliance, paired accuracy, repair rate
│
├── 2. Cross-modal verification
│   ├── Failure: model accepts unsupported or contradictory evidence
│   ├── Hypothesis: explicit verification improves factual decisions
│   ├── Intervention: require evidence checking or answer verification
│   └── Outcome: contradiction detection, factual accuracy, selective risk
│
├── 3. Image–text conflict arbitration
│   ├── Failure: model follows the wrong source under contradiction
│   ├── Hypothesis: source preference is task-dependent, not fixed
│   ├── Intervention: counterbalance source roles and alter legibility
│   └── Outcome: source-following rate, arbitration accuracy, abstention
│
├── 4. Evidence sufficiency and insufficiency
│   ├── Failure: model answers confidently when evidence is incomplete
│   ├── Hypothesis: models distinguish “false” from “not answerable”
│   ├── Intervention: remove decisive evidence while preserving distractors
│   └── Outcome: abstention quality, selective risk, evidence sufficiency accuracy
│
├── 5. Multimodal consistency
│   ├── Failure: image description, rationale, and answer disagree
│   ├── Hypothesis: verbal explanations can be consistent but unfaithful
│   ├── Intervention: compare original, counterfactual, and modality-only inputs
│   └── Outcome: answer consistency, contradiction rate, causal faithfulness
│
├── 6. Modality reliance and attribution
│   ├── Failure: accuracy hides shortcut reliance
│   ├── Hypothesis: counterfactual modality interventions reveal hidden dependence
│   ├── Intervention: image-only, text-only, joint, and realistic counterfactuals
│   └── Outcome: modality effect, interaction effect, attribution accuracy
│
├── 7. Multimodal hallucination and uncertainty
│   ├── Failure: fluent but unsupported claims
│   ├── Hypothesis: token confidence and visual attention are poor reliability signals
│   ├── Intervention: compare output confidence, consistency, and hidden-state signals
│   └── Outcome: AUROC, Brier score, calibration error, hallucination rate
│
├── 8. Missing or incomplete modality
│   ├── Failure: performance collapses when image or text is absent
│   ├── Hypothesis: restoration, prompting, or graceful degradation helps differently
│   ├── Intervention: modality dropout, feature restoration, modality-aware prompting
│   └── Outcome: performance-vs-missingness curve, robustness, hallucination
│
├── 9. Counterfactual multimodal reasoning
│   ├── Failure: model cannot update when one modality changes
│   ├── Hypothesis: models preserve stale priors after visual or textual intervention
│   ├── Intervention: minimally change one modality while holding the other fixed
│   └── Outcome: counterfactual accuracy, update rate, causal consistency
│
├── 10. Distribution shift and adaptation
│   ├── Failure: performance changes across style, domain, language, or corruption
│   ├── Hypothesis: adaptation capacity should depend on input complexity
│   ├── Intervention: test-time augmentation, prompt tuning, LoRA/QLoRA
│   └── Outcome: OOD accuracy, adaptation gain, forgetting, calibration
│
├── 11. Visual-token efficiency
│   ├── Failure: compression removes answer-critical evidence
│   ├── Hypothesis: token demand depends on question type and evidence locality
│   ├── Intervention: prune tokens at fixed budgets using different selection rules
│   └── Outcome: accuracy retention, token demand, latency, reliability loss
│
└── 12. Multimodal learning paradigms
    ├── Contrastive/self-supervised learning
    ├── preference optimization or verification
    ├── retrieval-augmented multimodal learning
    ├── continual/test-time learning
    ├── distillation and parameter-efficient adaptation
    └── Outcome: whether the paradigm changes evidence use rather than only accuracy
```

A useful general experimental template is:

$$
\text{model behavior}
=
\text{baseline input}
\rightarrow
\text{controlled modality intervention}
\rightarrow
\text{paired behavioral comparison}
\rightarrow
\text{reliability and leakage audit}.
$$

# B. Research families

## 1. Cross-modal evidence use and source arbitration

**Precise question:** When image and text support different answers, does a VLM shift reliance toward the source that remains legible or informative?

The closest inspected work is [*Which Source Wins? Task-Dependent Reliance in Vision-Language Models*](https://www.alphaxiv.org/abs/2608.17205), which creates conflicts from GSM8K, SVAMP, and ChartQA, then degrades either the image or text. It evaluates six open VLMs using generated answers and conditional log-likelihood margins. On arithmetic conflicts, most models moved away more strongly from degraded text; on ChartQA-Conflict, all likelihood-scored models moved more strongly away from degraded visual evidence. The reversal remained after adjustment for unimodal accuracy loss and a chart-to-table control. [Main findings](https://www.alphaxiv.org/abs/2608.17205?page=8)

This establishes that **modality reliance is task- and representation-dependent**, not simply “VLMs prefer text” or “VLMs prefer images.” It does not identify a single causal mechanism, because the arithmetic and chart experiments differ in task structure, source directness, and conflict construction. The authors also explicitly do not test contradiction detection, uncertainty expression, or abstention. [Limitations](https://www.alphaxiv.org/abs/2608.17205?page=9)

**Status:** The broad question is **partially explored**. A strong remaining question is whether task-dependent reliance is explained by *evidence accessibility*, *semantic complexity*, or *learned modality priors*.

**Datasets and code:** GSM8K and SVAMP are publicly available; ChartQA-Conflict, rendered conflict stimuli, degradation metadata, and outputs are released through the paper’s Hugging Face datasets. The paper reports MIT licensing for GSM8K/SVAMP and GPL-3.0 for ChartQA. The authors provide an artifact repository at [multimodal-arbitration-artifact](https://github.com/Ro-netizen004/multimodal-arbitration-artifact).

**Undergraduate experiment:** Reproduce the image/text degradation design on one open VLM and add a *third condition*: conflict detection followed by either answer, verification, or abstention. This is more scientifically useful than merely comparing models.

## 2. Cross-modal conflict and counterfactual composition

**Precise question:** Can a model combine complementary information and override a misleading modality when modalities conflict?

[*C³PO: Evaluating Cross-Modal Composition and Counterfactual Performance in Omnimodal Models*](https://www.alphaxiv.org/abs/2608.05381) studies information composition and counterfactual conflict across video, audio, image, and text. Its benchmark contains 3,404 samples, 25 templates, and four modality-combination tiers. It reports that 86–95% of failures in the analyzed open models were dominance failures, where one modality was followed while another was ignored. [Failure analysis](https://www.alphaxiv.org/abs/2608.05381?page=8)

This establishes that **multimodal failure is often selective modality dominance rather than uniformly poor fusion**. It does not yet establish whether dominance is caused by attention allocation, modality quality, task structure, training imbalance, or the synthetic construction pipeline. The benchmark also uses generated complementary media and an LLM judge; the authors note possible advantage for Gemini because Gemini was involved in generation, and some probes were unavailable because of GPU constraints. [Limitations](https://www.alphaxiv.org/abs/2608.05381?page=9)

**Status:** **Partially explored**, but the four-modality setting is probably too expensive for a small thesis. A vision-language-only version is more feasible.

**Undergraduate experiment:** Construct paired image–text items with three conditions: complementary evidence, irrelevant text, and contradictory text. Measure whether an intervention such as “list evidence from each modality before answering” improves arbitration or merely increases verbal rationalization.

## 3. Cross-modal verification and evidence sufficiency

**Precise question:** Can a VLM distinguish between “the evidence supports answer A,” “the evidence supports answer B,” and “the evidence is insufficient”?

The inspected 2026 work above shows that conflict benchmarks generally force a single answer. It does not test whether the model recognizes the conflict or abstains. This is an important boundary: **source-following is not the same as verification**.

A scientifically precise undergraduate question would be:

> When decisive visual evidence is removed or contradicted, does explicit evidence verification reduce unsupported answers, or does it merely increase the length and apparent plausibility of explanations?

**Status:** **Weakly explored in the specific controlled form**, but it requires targeted verification against recent contradiction-detection, abstention, and evidence-grounding papers before a novelty claim.

**Datasets:** ChartQA, TextVQA, DocVQA, ScienceQA-IMG, and synthetic paired image–text examples. The key requirement is that answerability labels be created independently of the model being evaluated.

**Undergraduate experiment:** For each item, create evidence-preserving, evidence-removing, and misleading-evidence variants. Compare direct answering with verification prompts. Metrics should include:

- answer accuracy when evidence is sufficient;
- false-answer rate when evidence is insufficient;
- abstention precision and recall;
- selective risk at fixed coverage;
- contradiction detection rate.

The negative result remains meaningful: if verification prompts do not reduce unsupported answers, that is evidence against a common assumption about “reasoning first, answering second.”

## 4. Modality attribution and hidden reliance

**Precise question:** Which modality causally changes a model’s decision, and how much of the apparent multimodal success is actually unimodal shortcut use?

[*Which Modality Decides? Counterfactual Modality Attribution for Multimodal LLMs*](https://www.alphaxiv.org/abs/2608.00076) proposes Counterfactual Modality Attribution, using generated image-only, text-only, and joint counterfactuals with Shapley-style modality scores. It evaluates controlled colored-MNIST tasks with known modality reliance and a constructed OpenI chest-X-ray classification task. On the controlled benchmark, it reports 98% attribution accuracy, while several feature-attribution baselines failed badly on image-biased cases. [Controlled attribution](https://www.alphaxiv.org/abs/2608.00076v2?page=6)

The paper establishes that **feature importance and modality-level causal reliance are different objects**. It does not establish causal effects in the real-world data-generating process: the authors describe the results as model-relative and reference-dependent. It also requires diffusion-based counterfactual generation, which is computationally unsuitable as a core undergraduate method. [Limitations](https://www.alphaxiv.org/abs/2608.00076v2?page=7)

**Status:** The attribution-method question is **occupied at the framework level**, but simpler controlled experiments remain open.

**Undergraduate experiment:** Avoid diffusion. Use realistic paired interventions:

1. image and text both correct;
2. image replaced with a matched distractor;
3. text replaced with a matched distractor;
4. both replaced;
5. image and text deliberately disagree.

Estimate paired modality effects and the interaction term:

$$
\Delta_I = f(I,T)-f(I',T),\qquad
\Delta_T = f(I,T)-f(I,T'),
$$

and compare them against accuracy. This can test whether a model’s correct answer is supported by both sources without claiming full causal attribution.

## 5. Multimodal consistency and explanation faithfulness

**Precise question:** Does a model’s answer change appropriately when the evidence changes, and do its explanations identify the evidence that actually caused the change?

The [*Circuit Tracing in Vision–Language Models*](https://www.alphaxiv.org/abs/2602.20330) paper studies internal mechanisms in Gemma-3-4B using transcoders, attribution graphs, attention analysis, feature steering, and circuit patching. It reports hierarchical integration of visual and semantic concepts, with joint features emerging mainly in higher layers, and demonstrates interventions involving visual concepts such as arithmetic, Mars, and finger-counting hallucinations. [Findings](https://www.alphaxiv.org/abs/2602.20330v1?page=8)

This establishes a promising mechanistic-analysis route and provides code at [UIUC-MONET/vlm-circuit-tracing](https://github.com/UIUC-MONET/vlm-circuit-tracing). However, the study focuses on one model, uses substantial computation, and relies partly on human feature annotation. The authors state that attention localization can be difficult, cross-layer superposition is not captured, and systematic quantitative evaluation remains limited. [Limitations](https://www.alphaxiv.org/abs/2602.20330v1?page=8)

**Status:** Mechanistic circuit tracing is **occupied and high burden**. Behavioral consistency experiments are more realistic for an undergraduate thesis.

**Undergraduate experiment:** Compare answer changes under minimally edited image/text evidence and test whether free-form rationales predict those changes. Treat explanation faithfulness as a separate metric from explanation quality.

## 6. Multimodal hallucination and reliability signals

**Precise question:** Which low-cost signal best predicts whether a VLM’s answer is correct: token confidence, visual attention structure, self-consistency, or hidden-state probes?

[*Visuals Lie, Consistency Speaks*](https://www.alphaxiv.org/abs/2606.17389) evaluates LLaVA-1.5, PaliGemma, and Qwen2-VL on POPE, LLaVA-Bench, custom counting/spatial tasks, VQA v2, and TextVQA. It reports near-zero correlation between spatial attention metrics and correctness, while self-consistency and hidden-state probes provide stronger signals. The reported structural correlations are approximately zero, whereas self-consistency reaches $R=0.429$ and hidden-state probes can reach high AUROC on some model-specific splits. [Reliability prediction](https://www.alphaxiv.org/abs/2606.17389v1?page=7)

This establishes that **sharp visual attention is not a reliable proxy for correctness** in the tested models. It does not establish a universal reliability monitor: probe performance is architecture- and benchmark-dependent, and self-consistency costs ten model calls. The study also uses supervised probes, so leakage between probe training and evaluation must be carefully controlled.

**Status:** The general “attention is not enough” claim is **already substantially occupied**. The strongest remaining undergraduate question is an *efficiency–reliability comparison*, not another attention visualization study.

**Undergraduate experiment:** Compare:

- token probability;
- entropy;
- one-pass answer margin;
- two- or three-sample self-consistency;
- a lightweight frozen hidden-state probe.

Use held-out datasets and report AUROC, AUPRC, Brier score, expected calibration error, and selective risk. A useful negative result would be that no cheap signal transfers across model families.

## 7. Missing modality and graceful degradation

**Precise question:** When one modality is absent, does the model degrade gracefully, hallucinate missing content, or invent a semantically plausible but incorrect replacement?

[*Enhancing Foundation VLM Robustness to Missing Modality*](https://www.alphaxiv.org/abs/2602.03151) proposes diffusion-based bidirectional feature restoration with dynamic modality gating and mutual learning. It evaluates MM-IMDb, N24News, MMHS11K, and Food101 under missing-modality settings, using CLIP backbones and lightweight decoders. The paper reports experiments with 70% missingness and improvements over several baselines, including prompt-based, retrieval-based, and parameter-efficient methods. [Missing-modality results](https://www.alphaxiv.org/abs/2602.03151v2?page=5)

This establishes that feature restoration can improve downstream classification under the paper’s missingness protocol. It does not establish that restored features correspond to the true missing content, that the method works for generative VLMs, or that it avoids hallucination. The method is trained on CC3M and evaluated with additional compute; the reported training used an A800 and downstream training used an RTX A5000, so reproducing the complete method is not a natural Colab core project. [Compute setup](https://www.alphaxiv.org/abs/2602.03151v2?page=5)

**Status:** Method development is **heavily occupied**. The behavioral question—what happens when missingness is selective, semantically important, or correlated with the label—is more defensible.

**Undergraduate experiment:** Evaluate a frozen open VLM under:

- random missing image regions;
- missing OCR text;
- missing captions;
- complete image absence;
- complete text absence;
- selective removal of the evidence needed for the answer.

Measure accuracy, hallucination rate, calibration, and whether the model appropriately signals insufficiency. This requires no training.

## 8. Counterfactual multimodal reasoning

**Precise question:** After changing only one modality, does the model update the answer in the direction implied by the changed evidence while preserving unrelated conclusions?

This family overlaps with modality attribution but emphasizes **behavioral invariance and causal update** rather than attribution scores. The controlled conflict studies above establish that models can follow one source while ignoring another. The CMA paper establishes a framework for modality-level counterfactuals. Together, they imply that a useful gap is not “can we create counterfactuals?” but:

> Are VLM updates localized to the changed evidence, or do small cross-modal edits cause unrelated answer drift?

**Status:** **Partially explored.**

**Undergraduate experiment:** Use image–question pairs with one factual attribute changed—color, count, orientation, or object presence—while keeping the question and all other content fixed. Compare output changes against expected changes. Report:

- counterfactual update accuracy;
- unintended-change rate;
- answer invariance on unaffected questions;
- modality-specific repair rate.

A negative result is informative: if the model changes unrelated answers, that reveals poor compositionality rather than merely low accuracy.

## 9. Distribution shift and test-time adaptation

**Precise question:** Does adaptation improve generalization uniformly, or does it help some visual conditions while causing confirmation bias, forgetting, or calibration failure in others?

[*MuRA: Multi-Rank Adaptation for Efficient and Effective Test-Time Vision-Language Generalization*](https://www.alphaxiv.org/abs/2608.03885) studies test-time adaptation of CLIP under ImageNet-A, ImageNet-V2, ImageNet-R, ImageNet-S, and ten cross-domain datasets. It argues that fixed-rank LoRA is inappropriate because visual complexity varies, and proposes dynamic multi-rank adaptation. The paper evaluates TPT, TDA, TTL, retrieval-based methods, and other baselines. [Experimental setup](https://www.alphaxiv.org/abs/2608.03885v1?page=5)

This establishes that parameter-efficient test-time adaptation is an active and competitive area. It does not establish that entropy is a sufficient causal measure of adaptation difficulty, nor that gains transfer from CLIP classification to generative VLM reasoning. The study also uses 63 augmented views per image, which is expensive for Colab-scale experiments.

**Status:** Algorithmic TTA is **occupied and rapidly moving**. A thesis should not reproduce another adaptive-rank method.

**Undergraduate experiment:** Compare frozen inference, entropy-minimization prompt adaptation, and a small LoRA adapter under one shift family. Measure not only accuracy but also:

- adaptation gain;
- per-sample variance;
- calibration change;
- catastrophic forgetting on source data;
- order sensitivity in streaming adaptation.

The scientific contribution would be a controlled audit of *when adaptation helps and when it harms*, not a new TTA architecture.

## 10. Visual-token efficiency

**Precise question:** Does visual-token compression preserve reliability uniformly, or does it selectively remove evidence required for fine-grained, spatial, OCR, or conflict-resolution questions?

[*How Many Visual Tokens Do Multimodal Language Models Need?*](https://www.alphaxiv.org/abs/2605.16359) studies training-free visual-token pruning across Qwen3-VL models from 2B to 235B, using eleven benchmarks and retention ratios of 20%, 40%, and 60%. It proposes F³A and compares it with FastV, VisionZip, DivPrune, and CDPruner. At 20% retention, it reports 93.86% of full-token performance on average and lower token requirements for a 97%-fidelity target. [Token demand](https://www.alphaxiv.org/abs/2605.16359v1?page=8)

This establishes that token demand varies with model scale, pruning method, and task. It does not establish that This establishes that token demand varies with model scale, pruning method, and task. It does **not** establish that compressed models preserve *reliability*, *evidence use*, or *counterfactual behavior* uniformly. The evaluation is dominated by accuracy and efficiency metrics, and the main experiments were conducted on eight H200 GPUs, which is not a realistic reproduction requirement for an undergraduate project. [Compute setup](https://www.alphaxiv.org/abs/2605.16359v1?page=6)

**Status:** Fixed-ratio token pruning is **occupied as a method-development problem**. The strongest remaining question is whether compression causes *selective evidence loss*.

**Undergraduate experiment:** Use one 2B–8B VLM and compare full-token inference with 75%, 50%, 25%, and 10% retention using simple pruning rules. Evaluate separately on:

- global scene questions;
- small-object questions;
- OCR and document questions;
- spatial-relation questions;
- hallucination probes;
- image–text conflict items.

Measure accuracy retention, hallucination increase, evidence-sensitive error rate, latency, and memory. The key question is not “which pruner wins?” but:

> Does token reduction degrade all evidence types proportionally, or does it selectively destroy the evidence needed for reliable decisions?

## 11. Parameter-efficient adaptation and learning paradigms

**Precise question:** Can lightweight adaptation change a VLM’s evidence-use behavior without merely increasing task accuracy?

The recent adaptation literature mostly evaluates whether prompt tuning, LoRA, retrieval, or test-time optimization improves classification accuracy under shift. The inspected [MuRA paper](https://www.alphaxiv.org/abs/2608.03885) is representative: its central evaluation concerns OOD and cross-domain accuracy, throughput, and memory rather than whether adaptation makes the model more faithful to visual evidence. [Adaptation benchmarks](https://www.alphaxiv.org/abs/2608.03885v1?page=5)

A stronger scientific question is:

> When lightweight adaptation improves performance under distribution shift, does it improve genuine cross-modal evidence use, or does it strengthen a new shortcut?

**Status:** Adaptation methods are **occupied**; evidence-use effects of adaptation are **partially explored**.

**Undergraduate experiment:** Start with a frozen VLM and a small LoRA or prompt adapter. Evaluate before and after adaptation on matched clean, corrupted, missing-evidence, and conflict conditions. Report paired accuracy, modality reliance, calibration, and source-following rate. This design can produce a meaningful result even if adaptation improves ordinary accuracy but worsens evidence use.

## 12. Cross-lingual and low-resource multimodal learning

**Precise question:** Does language shift alter which modality a VLM relies on, and can a low-resource language expose a failure mechanism that English-only evaluation misses?

The important distinction is between “testing Bengali” and testing a scientifically meaningful **language-conditioned modality interaction**. A defensible question would be:

> When the visual evidence is held constant, does changing the question language alter visual reliance, uncertainty, conflict arbitration, or evidence sufficiency?

**Status:** The generic Bengali-VLM application question is weak and likely occupied in many forms. The language-conditioned evidence-use question is **underexplored but requires targeted search** before a novelty claim.

**Datasets:** Multilingual versions of visual question-answering or image-caption data, translated questions with human verification, and independently authored low-resource evaluation items. Translation must be treated as a possible confound, not automatically as independent data.

**Undergraduate experiment:** Use English and Bengali versions of the same image-question pairs, with:

- language-balanced prompts;
- native-speaker verification;
- separate image-only and text-only baselines;
- translated-row and source-image grouping;
- conflict and missing-evidence variants.

Measure whether language changes the image–text arbitration pattern rather than merely changing answer accuracy.

# C. Literature map

The inspected 2025–2026 papers cluster into five broad research programs.

| Literature branch | Closest inspected work | What it establishes | Main boundary |
|---|---|---|---|
| Source arbitration | [Which Source Wins?](https://www.alphaxiv.org/abs/2608.17205) | Reliance shifts asymmetrically and reverses across task settings | Does not test contradiction detection or abstention |
| Cross-modal composition and conflict | [C³PO](https://www.alphaxiv.org/abs/2608.05381) | Many failures are modality-dominance failures rather than incomplete fusion | Generated multimodal data and LLM judging create validity risks |
| Modality attribution | [Which Modality Decides?](https://www.alphaxiv.org/abs/2608.00076) | Modality-level counterfactual attribution differs from feature attribution | Counterfactual quality is a major dependency |
| Reliability and hallucination | [Visuals Lie, Consistency Speaks](https://www.alphaxiv.org/abs/2606.17389) | Attention geometry is weak as a reliability signal; hidden states and self-consistency can be stronger | Probe transfer and causal interpretation remain uncertain |
| Mechanistic interpretability | [Circuit Tracing in Vision–Language Models](https://www.alphaxiv.org/abs/2602.20330) | Visual and semantic circuits can be traced and intervened on in Gemma-3-4B | One model, high compute, substantial manual analysis |
| Missing modality | [Enhancing Foundation VLM Robustness to Missing Modality](https://www.alphaxiv.org/abs/2602.03151) | Feature restoration can improve classification under high missingness | Does not establish semantic faithfulness or generative reliability |
| Test-time adaptation | [MuRA](https://www.alphaxiv.org/abs/2608.03885) | Dynamic adaptation capacity can outperform fixed-rank adaptation under shift | Primarily CLIP classification; expensive evaluation |
| Visual-token efficiency | [How Many Visual Tokens Do Multimodal Language Models Need?](https://www.alphaxiv.org/abs/2605.16359) | Token demand varies with scale, task, retention level, and pruning rule | Accuracy retention does not equal evidence or reliability retention |

# D. Occupied questions

These questions should be removed or substantially reformulated:

1. **“Can a new prompt reduce hallucination?”**  
   Hallucination prompting and verification prompting are already crowded. A viable version must isolate a specific mechanism, such as unsupported-answer suppression under controlled evidence removal.

2. **“Do VLMs prefer text or images?”**  
   This is too broad. [Which Source Wins?](https://www.alphaxiv.org/abs/2608.17205) shows that the answer depends on task, representation, and evaluation method. The surviving question must explain the reversal.

3. **“Can we build a modality-attribution method?”**  
   [Which Modality Decides?](https://www.alphaxiv.org/abs/2608.00076) already proposes a dedicated counterfactual framework. A simpler empirical audit could still be valid, but not as an unqualified “first method.”

4. **“Does visual attention explain model reliability?”**  
   [Visuals Lie, Consistency Speaks](https://www.alphaxiv.org/abs/2606.17389) directly challenges this premise across multiple VLM families.

5. **“Can diffusion restore missing modalities?”**  
   This is now an active method-development branch, including [Enhancing Foundation VLM Robustness to Missing Modality](https://www.alphaxiv.org/abs/2602.03151). Reproducing it would be compute-heavy and scientifically narrow.

6. **“Can visual-token pruning improve accuracy?”**  
   [How Many Visual Tokens Do Multimodal Language Models Need?](https://www.alphaxiv.org/abs/2605.16359) and related work already establish strong accuracy–efficiency comparisons.

7. **“Can LoRA improve VLM generalization?”**  
   This is too generic. The question must concern adaptation side effects, reliability, shortcut formation, or evidence preservation.

# E. Partially explored questions

These have real scientific value, but the proposed boundary must be narrow.

### 1. Does conflict detection improve arbitration?

Existing work shows that models often follow a dominant modality under conflict. It does not establish whether explicitly detecting disagreement improves the final decision. A meaningful experiment would compare direct answering with conflict detection plus answer selection, using the same paired items.

### 2. Does modality degradation cause calibrated uncertainty?

[Which Source Wins?](https://www.alphaxiv.org/abs/2608.17205) degrades image or text and measures source reliance, but explicitly states that it does not test uncertainty or abstention. [Uncertainty boundary](https://www.alphaxiv.org/abs/2608.17205?page=9) This is a promising extension, provided the task includes answerable and unanswerable examples.

### 3. Does visual-token compression selectively destroy evidence?

The efficiency literature measures average accuracy and latency. A stronger audit would stratify by evidence type and test whether compression disproportionately harms fine-grained, OCR, spatial, or conflict-resolution questions.

### 4. Does test-time adaptation improve evidence use or only confidence?

Adaptation papers generally report classification gains. A paired pre/post adaptation evaluation under modality conflict, missing evidence, and distribution shift would test whether adaptation improves the intended mechanism.

### 5. Does language shift change modality reliance?

This is potentially valuable for Bengali or another low-resource language, but only if the study measures a general cross-lingual phenomenon rather than reporting English-versus-Bengali accuracy.

# F. Underexplored questions

The following questions survive the initial audit better than generic benchmark or model-comparison questions.

## U1. Does explicit conflict detection reduce wrong-modality decisions?

**Question:** When image and text conflict, does requiring a model to identify the disagreement before answering reduce source-dominance errors?

- **Independent variable:** direct answering versus conflict-detection intervention.
- **Dependent variables:** arbitration accuracy, contradiction detection, abstention, calibration.
- **Competing explanations:** the intervention may improve genuine evidence comparison, or merely provide a useful textual scaffold.
- **Negative result:** if conflict detection does not improve arbitration, explicit verbal reasoning is not sufficient.
- **Main risk:** the prompt may reveal the expected conflict structure.

## U2. Does modality degradation produce calibrated uncertainty?

**Question:** When one modality becomes unreadable or is removed, does the model reduce confidence in proportion to the loss of decisive evidence?

- **Independent variable:** image/text corruption, removal, or evidence-targeted masking.
- **Dependent variables:** Brier score, ECE, selective risk, coverage, abstention precision.
- **Competing explanations:** confidence may track output fluency or answer entropy rather than evidence sufficiency.
- **Negative result:** unchanged confidence under evidence removal would reveal a specific reliability failure.
- **Main risk:** token probabilities are often not comparable across free-form answers.

## U3. Does token compression selectively destroy evidence?

**Question:** Does visual-token reduction preserve ordinary accuracy while damaging fine-grained evidence use and hallucination resistance?

- **Independent variable:** retention ratio and pruning rule.
- **Dependent variables:** accuracy retention, hallucination rate, evidence-sensitive error, latency.
- **Competing explanations:** errors may result from lower visual information generally, or from selective loss of small answer-critical regions.
- **Negative result:** uniform degradation across task types would refute the selective-loss hypothesis.
- **Main risk:** implementation differences in token selection and positional encoding.

## U4. Does adaptation improve cross-modal faithfulness?

**Question:** When parameter-efficient adaptation improves shifted-domain accuracy, does it also improve the model’s use of visual evidence under conflict and missingness?

- **Independent variable:** frozen model versus prompt/LoRA adaptation.
- **Dependent variables:** shifted-domain accuracy, modality effect, calibration, shortcut rate.
- **Competing explanations:** adaptation may learn target-domain shortcuts rather than better alignment.
- **Negative result:** accuracy gains with worse evidence use would be a valuable warning.
- **Main risk:** adaptation can overfit the evaluation distribution.

## U5. Does language change modality arbitration?

**Question:** Given the same image and task, does the language of the question alter the model’s reliance on visual versus textual evidence?

- **Independent variable:** language condition.
- **Dependent variables:** modality reliance, conflict resolution, calibration, answer consistency.
- **Competing explanations:** differences may arise from translation quality, tokenizer coverage, or language-specific priors.
- **Negative result:** no language effect would itself constrain claims about low-resource multimodal failure.
- **Main risk:** translated examples may share images and create contamination or paraphrase leakage.

# G. Top 10 RQs

| RQ | Scientific phenomenon | Closest work | What remains unknown | Dataset | Baseline | Main metric | Leakage risk | Compute | Novelty confidence | Feasibility |
|---|---|---|---|---|---|---|---|---|---|---|
| 1. Does explicit conflict detection reduce wrong-modality decisions? | Conflict arbitration | [C³PO](https://www.alphaxiv.org/abs/2608.05381); [Which Source Wins?](https://www.alphaxiv.org/abs/2608.17205) | Whether detection improves decisions rather than explanations | ChartQA-style and synthetic image–text conflicts | Direct answer; modality-only | Arbitration accuracy, contradiction detection, ECE | Prompt may expose conflict | Low–medium | Moderate–strong | High |
| 2. Does modality degradation produce calibrated uncertainty? | Evidence sufficiency | [Which Source Wins?](https://www.alphaxiv.org/abs/2608.17205) | Whether confidence responds to lost evidence | GSM8K/SVAMP conflict stimuli; ChartQA | Token entropy; answer margin | Brier, ECE, selective risk | Confidence extraction | Low–medium | Strong | High |
| 3. Does token compression selectively remove answer-critical evidence? | Efficient inference | [How Many Visual Tokens](https://www.alphaxiv.org/abs/2605.16359) | Reliability and error-type effects of compression | POPE, TextVQA, AI2D, VSR, small custom set | Full tokens; random pruning | Accuracy retention, hallucination, latency | Benchmark memorization | Medium | Moderate | High |
| 4. Does adaptation improve evidence use or only target accuracy? | Test-time adaptation | [MuRA](https://www.alphaxiv.org/abs/2608.03885) | Whether adaptation reduces shortcut reliance | ImageNet shifts plus conflict subset | Frozen VLM; prompt TTA | Adaptation gain and modality effect | Test-stream leakage | Medium | Moderate | Medium |
| 5. Does language alter image–text arbitration? | Cross-lingual shift | [Which Source Wins?](https://www.alphaxiv.org/abs/2608.17205) | Whether language changes reliance independent of translation quality | Parallel English/Bengali or multilingual VQA | English condition; text-only | Reliance asymmetry, consistency | Translation and duplicate-image leakage | Medium | Moderate | Medium |
| 6. Do missing modalities trigger calibrated abstention? | Missing modality | [Missing Modality Restoration](https://www.alphaxiv.org/abs/2602.03151) | Whether models know when restoration is unreliable | COCO/VQA/TextVQA variants | Image-only, text-only, blank input | Selective risk, abstention quality | Captions leak answers | Low–medium | Moderate | High |
| 7. Are explanations faithful under modality intervention? | Consistency | [CMA](https://www.alphaxiv.org/abs/2608.00076) | Whether stated evidence predicts counterfactual behavior | Controlled image–text pairs | Direct answer; rationale | Counterfactual faithfulness | Rationale judged by same model | Medium | Moderate | Medium |
| 8. Does self-consistency transfer across VLM families? | Uncertainty | [Visuals Lie, Consistency Speaks](https://www.alphaxiv.org/abs/2606.17389) | Whether reliability signals generalize without retraining | POPE, VQA v2, TextVQA | Token confidence; entropy | AUROC, Brier, ECE | Probe split contamination | Medium | Moderate | High |
| 9. Does visual evidence update remain localized? | Counterfactual reasoning | [CMA](https://www.alphaxiv.org/abs/2608.00076) | Whether changing one fact causes unrelated answer drift | Synthetic attribute-edit image pairs | Image-only/text-only | Update accuracy, unintended-change rate | Generated edits may be unrealistic | Medium | Moderate | Medium |
| 10. Are modality-dominance failures caused by accessibility or priors? | Modality reliance | [C³PO](https://www.alphaxiv.org/abs/2608.05381); [Which Source Wins?](https://www.alphaxiv.org/abs/2608.17205) | Whether task structure or modality legibility drives dominance | Matched visual/text evidence | Clean conflict baseline | Source-following curves | Unequal corruption severity | Low–medium | Moderate | High |

# H. Top 5

## 1. Explicit conflict detection and arbitration

This is the strongest candidate because it builds directly on two recent findings without simply reproducing them. [C³PO](https://www.alphaxiv.org/abs/2608.05381) finds that dominance accounts for most open-model failures, while [Which Source Wins?](https://www.alphaxiv.org/abs/2608.17205) shows that source reliance changes with task and evidence structure. Neither result establishes that a model can *recognize* conflict and then arbitrate correctly.

**Proposed experiment**

Use matched image–text pairs with:

1. complementary evidence;
2. irrelevant evidence;
3. contradictory evidence;
4. insufficient evidence.

Compare:

- direct answer;
- “identify whether sources agree” then answer;
- “state which source supports the answer” then answer;
- answer with abstention allowed.

The primary result should be a paired change in arbitration accuracy, not average benchmark accuracy.

**Minimum baseline:** one small open VLM, direct answering, modality-only inputs, and a simple rule-based contradiction detector for structured items.

**Why it is feasible:** no model training is required, conflict data can be generated from public datasets, and the core experiment can run with hundreds rather than tens of thousands of items.

**Main concern:** if the prompt explicitly says “the sources may conflict,” the intervention may alter task framing rather than improve reasoning. A neutral version should also be tested.

## 2. Modality degradation and calibrated uncertainty

This is the cleanest reliability question because it has a controlled intervention and a useful negative result. [Which Source Wins?](https://www.alphaxiv.org/abs/2608.17205) already provides a strong degradation protocol, but its limitation explicitly leaves uncertainty and abstention untested. [Uncertainty limitation](https://www.alphaxiv.org/abs/2608.17205?page=9)

**Proposed experiment**

For each conflict item, create:

- both sources clean;
- image degraded;
- text degraded;
- decisive evidence removed;
- both sources insufficient.

Ask for an answer plus a confidence score or an abstention decision. The model should not be told which source is degraded.

**Primary metrics**

- Brier score;
- expected calibration error;
- AUROC for correctness;
- selective risk at multiple coverage levels;
- false-answer rate on insufficient-evidence items;
- confidence change under matched evidence loss.

**Competing hypotheses**

1. Confidence reflects evidence quality.
2. Confidence mostly reflects language-model fluency and answer preference.
3. Confidence responds to visual degradation but not textual degradation, or vice versa.

**Why it is feasible:** it is inference-first and can use open models with accessible log probabilities or explicit confidence outputs.

**Main concern:** free-form token probabilities are an imperfect measure of answer confidence. Structured short answers, fixed candidate answers, or calibrated self-reports should be compared.

## 3. Selective evidence loss under visual-token compression

This is the strongest efficiency question because it connects computational savings to trustworthiness. [How Many Visual Tokens Do Multimodal Language Models Need?](https://www.alphaxiv.org/abs/2605.16359) shows that token pruning can preserve average benchmark performance at low retention ratios, but its main contribution is efficiency rather than reliability. Its own limitations identify systematic study of other modality structures as future work. [Scope limitation](https://www.alphaxiv.org/abs/2605.16359v1?page=16)

**Proposed experiment**

Use a single accessible VLM and compare:

- full visual tokens;
- random token removal;
- uniform spatial subsampling;
- attention-based pruning;
- one simple question-conditioned pruning rule.

Stratify questions by evidence type:

- global scene;
- small object;
- OCR;
- spatial relation;
- counting;
- hallucination;
- image–text conflict.

**Primary metrics**

- accuracy retention relative to full tokens;
- hallucination rate;
- evidence-sensitive error rate;
- latency;
- peak memory;
- token count;
- calibration change.

**Key result**

The central analysis should estimate an interaction:

$$
\text{error}
\sim
\text{retention ratio}
+
\text{question type}
+
\text{retention ratio}\times\text{question type}.
$$

A significant interaction would show that token compression has a selective, not merely uniform, reliability cost.

**Main concern:** pruning implementations may alter image-token positions or model preprocessing. The full-token pipeline must be validated first.

## 4. Adaptation and evidence use

This question is more ambitious but potentially valuable:

> Does parameter-efficient adaptation improve a model’s actual use of visual evidence, or does it improve shifted-domain accuracy through new shortcuts?

The recent [MuRA](https://www.alphaxiv.org/abs/2608.03885) paper demonstrates the maturity of dynamic adaptation methods but evaluates primarily classification accuracy and efficiency. A thesis should therefore audit adaptation effects, not propose another rank-selection mechanism.

**Proposed experiment**

Compare frozen inference with:

- prompt-only test-time adaptation;
- small LoRA adaptation;
- no adaptation.

Evaluate source-domain and shifted-domain data, then add a smaller conflict set. Measure:

- accuracy;
- modality reliance;
- calibration;
- source-domain forgetting;
- order sensitivity;
- adaptation variance across examples.

**Main concern:** test-time learning is highly sensitive to batch ordering and augmentation policy. A fixed stream protocol and multiple seeds are necessary.

## 5. Language-conditioned modality reliance

This is the best candidate for a Bengali angle, but only if framed internationally:

> Does changing the question language change how a VLM arbitrates between image evidence and textual evidence?

The contribution would not be “Bengali VQA.” It would be an analysis of whether low-resource language conditions expose a change in cross-modal evidence use.

**Proposed experiment**

Construct parallel English/Bengali items with:

- native review;
- independent test images;
- image-only and text-only baselines;
- conflict and missing-evidence variants;
- no shared generated variants across train and test.

Measure language-conditioned changes in:

- image reliance;
- conflict resolution;
- calibration;
- consistency;
- abstention.

**Main concern:** translation quality and tokenization may explain the entire effect. The experiment must include a high-resource control language and report language-only performance.

# I. Top 3

## Top 1: Does explicit conflict detection reduce wrong-modality decisions?

### Exact gap boundary

**Existing work establishes:** VLMs often exhibit modality dominance, and source reliance changes with task and evidence structure. [C³PO](https://www.alphaxiv.org/abs/2608.05381) reports that 86–95% of analyzed failures were dominance-driven. [Dominance failures](https://www.alphaxiv.org/abs/2608.05381?page=8) [Which Source Wins?](https://www.alphaxiv.org/abs/2608.17205) shows asymmetric reallocation when one source is degraded.

**It does not test:** whether the model can explicitly detect cross-modal disagreement and use that detection to improve arbitration.

**The proposed experiment tests:** whether a conflict-detection intervention changes the model’s decision, contradiction recognition, uncertainty, and source attribution.

### Two competing explanations

- **Evidence-comparison explanation:** detecting disagreement makes the model compare sources and improves the decision.
- **Scaffolding explanation:** the intervention improves results only because it gives the model a helpful task decomposition or reveals the expected answer format.

A neutral prompt condition and a conflict-present/absent condition are therefore essential.

### Minimum experimental design

| Condition | Input | Output |
|---|---|---|
| Direct | image + text | answer |
| Conflict-aware | image + text | agreement status, answer |
| Evidence-aware | image + text | evidence from each source, answer |
| Abstention | image + text | answer or insufficient evidence |

Use matched items where the correct answer is determined by:

- image only;
- text only;
- both;
- neither because evidence is insufficient.

### Evaluation

The core metric should be **paired arbitration improvement**:

$$
\Delta_{\text{arb}}
=
\text{accuracy}_{\text{intervention}}
-
\text{accuracy}_{\text{direct}}.
$$

Also report:

- contradiction detection accuracy;
- source-following rate;
- false-answer rate on insufficient items;
- calibration error;
- abstention precision and recall;
- explanation–behavior consistency.

### Leakage audit

Potential shortcuts include:

- explicit conflict wording;
- answer options indicating which source is correct;
- different image and text styles;
- source order;
- question wording revealing the decisive modality;
- generated text containing the answer;
- repeated source images across variants.

The dataset should counterbalance source order and group all variants of an image or question family into one split.

### Feasibility

- Data burden: **low–medium**
- Annotation burden: **medium**
- Implementation: **low**
- Compute: **low–medium**
- Statistical analysis: **medium**
- Training requirement: **none**
- Colab suitability: **high**

## Top 2: Does modality degradation produce calibrated uncertainty?

### Exact gap boundary

**Existing work establishes:** degradation changes source reliance, and confidence or likelihood margins can quantify source preference. [Which Source Wins?](https://www.alphaxiv.org/abs/2608.17205) explicitly notes that its protocol measures forced arbitration rather than uncertainty, factual reliability, or abstention. [Uncertainty boundary](https://www.alphaxiv.org/abs/2608.17205?page=9)

**It does not test:** whether confidence tracks the loss of answer-relevant evidence.

**The proposed experiment tests:** whether confidence decreases appropriately when one modality is degraded, removed, or made insufficient.

### Minimum experimental design

For each item, create a matched ladder:

1. clean image and clean text;
2. image degraded;
3. text degraded;
4. decisive image evidence removed;
5. decisive text evidence removed;
6. both sources insufficient.

Use a fixed-answer format where possible. Include answerable and unanswerable examples.

### Metrics

- **Brier score:** tests probabilistic correctness.
- **ECE:** tests calibration across confidence bins.
- **AUROC:** tests whether confidence separates correct from incorrect answers.
- **Selective risk:** tests whether abstaining on low-confidence cases is useful.
- **Evidence-loss response:** measures whether confidence changes in the expected direction.

A model can have high accuracy but poor calibration, so accuracy alone is not adequate.

### Negative-result value

If confidence remains high when decisive evidence is removed, the study demonstrates that confidence is not evidence-sensitive. If confidence decreases only for text but not image degradation, it reveals modality-specific uncertainty failure.

### Feasibility

- Data burden: **low**
- Annotation burden: **low–medium**
- Implementation: **low**
- Compute: **low–medium**
- Training: **none or lightweight calibration only**
- Colab suitability: **high**

## Top 3: Does visual-token compression selectively destroy answer-critical evidence?

### Exact gap boundary

**Existing work establishes:** visual-token pruning can substantially reduce token count while preserving average benchmark performance. [How Many Visual Tokens Do Multimodal Language Models Need?](https://www.alphaxiv.org/abs/2605.16359) reports broad compression experiments and a fixed-fidelity token-demand analysis. [Compression results](https://www.alphaxiv.org/abs/2605.16359v1?page=3)

**It does not test:** whether the preserved average accuracy hides systematic failures on particular evidence types, nor whether compression harms hallucination resistance or confidence.

**The proposed experiment tests:** whether the effect of token reduction interacts with evidence locality, OCR, spatial reasoning, counting, or cross-modal conflict.

### Minimum experimental design

Use one model and four token budgets:

- 100%;
- 75%;
- 50%;
- 25%.

Compare at least two simple pruning policies against full-token inference. Avoid reproducing a large-scale pruning system.

### Metrics

- accuracy retention;
- hallucination rate;
- evidence-sensitive error;
- answer consistency between full and compressed inference;
- calibration;
- visual-token count;
- latency and memory.

### Leakage audit

- Ensure the question is not used to select tokens unless that is the intervention being studied.
- Preserve image-token order and positional information.
- Group generated variants of the same image.
- Check whether answer text appears in captions or metadata.
- Use question-type labels that are created independently of the evaluated outputs.

### Feasibility

- Data burden: **low–medium**
- Annotation burden: **medium**
- Implementation: **medium**
- Compute: **medium**
- Training: **none**
- Colab suitability: **medium–high**, depending on model and image resolution

# J. Dataset and baseline feasibility

## Top 1: Conflict detection

**Recommended dataset construction**

Start from public image-question data and create controlled text variants:

- correct complementary text;
- irrelevant text;
- contradictory text;
- insufficient text.

The most important split rule is grouping by original image, source document, entity, and question family. Do not place clean and contradictory variants of the same underlying example in different splits.

**Baseline set**

1. image-only VLM;
2. text-only model or text-only prompt;
3. direct multimodal answer;
4. rule-based contradiction detector for structured examples;
5. conflict-aware prompt;
6. answer-plus-abstention prompt.

## Top 2: Uncertainty under modality degradation

**Recommended data**

The released stimuli associated with [Which Source Wins?](https://www.alphaxiv.org/abs/2608.17205) are a useful starting point because the paper reports rendered GSM8K/SVAMP conflicts and a reviewed ChartQA conflict set. The work provides public metadata and datasets for the conflict constructions. [Data release](https://www.alphaxiv.org/abs/2608.17205?page=6)

For a thesis, use a subset and add evidence-insufficient examples. Do not treat translated or generated variants as independent test examples unless their source groups are separated.

**Baseline set**

- greedy answer;
- token entropy;
- normalized answer margin;
- self-reported confidence;
- two- or three-sample self-consistency;
- optional temperature scaling on a validation split.

## Top 3: Visual-token compression

**Recommended datasets**

The inspected token-efficiency paper evaluates HallusionBench, MME, AI2D, RealWorldQA, ScienceQA-IMG, POPE, MMBench, CCBench, VSR, and Visual7W. [Evaluation suite](https://www.alphaxiv.org/abs/2605.16359v1?page=13)

A smaller undergraduate subset should include:

- POPE for hallucination;
- AI2D for diagrams;
- TextVQA for OCR;
- VSR for spatial relations;
- one general VQA dataset.

**Baseline set**

- full-token inference;
- uniform spatial subsampling;
- random token selection;
- one existing simple pruning implementation if reproducible;
- fixed retention ratios.

# K. Leakage and evaluation risks

## Conflict detection

The greatest risk is that the intervention tells the model that conflict exists. Include:

- no-conflict controls;
- conflict-present examples;
- prompts that do not mention disagreement;
- balanced source ordering;
- equivalent prompt variants.

A second risk is **answer leakage through construction**. If contradictory text is generated with distinctive wording, the model can classify the template rather than inspect the evidence.

## Uncertainty

Confidence estimates are difficult for generative models. A model may assign high probability to a fluent but wrong answer. The study should distinguish:

- token-level confidence;
- answer-level confidence;
- self-reported confidence;
- empirical correctness frequency.

Never treat one of these as ground-truth uncertainty without calibration analysis.

## Token compression

Average accuracy can hide severe subgroup failures. Report per-question-type results and confidence intervals. A token-pruning method may also introduce a confound if it changes image resolution, token positions, or attention masks. The full-token and compressed pipelines must be identical except for the intended token intervention.

# L. Compute feasibility

## Top 1: Conflict detection

**Minimum experiment**

- one 2B–8B open VLM;
- 300–1,000 paired examples;
- four prompt conditions;
- greedy decoding;
- one evaluation seed.

This is feasible on Colab Pro if images are resized consistently and evaluation is batched where the model permits it.

**Optional extension**

- second model family;
- three decoding seeds;
- hidden-state or logit analysis;
- Bengali or multilingual condition.

Do not make the second model or multilingual extension part of the core question.

## Top 2: Uncertainty

This is the cheapest of the three. The main cost is the number of forward passes:

- greedy baseline: one call per item;
- self-consistency with three samples: approximately three calls;
- ten-sample consistency: approximately ten calls.

A practical core study should use one- and three-sample signals. Ten-sample self-consistency is an optional extension because [Visuals Lie, Consistency Speaks](https://www.alphaxiv.org/abs/2606.17389) identifies its reliability benefit but also notes its approximately tenfold inference cost. [Consistency cost](https://www.alphaxiv.org/abs/2606.17389v1?page=7)

## Top 3: Token compression

The minimum feasible setup is:

- one 2B–8B VLM;
- one image resolution;
- four retention ratios;
- four small evaluation subsets;
- no fine-tuning;
- no large-scale model comparison.

The main risk is model availability and implementation complexity. Some recent token-pruning papers evaluate across model scales using large GPU clusters; that scale should not be copied into an undergraduate thesis.

# M. Negative-result value

## Top 1: Conflict detection

A negative result remains useful if:

- conflict detection does not improve arbitration;
- it improves contradiction detection but not final answers;
- it increases abstention without improving selective risk;
- it helps only when the conflict is explicit.

These outcomes distinguish recognition from reliable resolution.

## Top 2: Uncertainty

A negative result is particularly informative if:

- confidence remains high after decisive evidence removal;
- confidence reacts asymmetrically to image and text degradation;
- self-consistency improves AUROC but worsens calibration;
- confidence transfers poorly across question types.

The result would show that confidence is not automatically evidence-sensitive.

## Top 3: Token compression

A negative result is useful if:

- average accuracy is preserved but hallucination increases;
- OCR and spatial reasoning fail before ordinary VQA;
- compressed and full-token answers disagree even when both are correct;
- confidence remains unchanged despite selective evidence loss.

This would reveal a reliability–efficiency trade-off that ordinary accuracy tables miss.

# N. Recommended next investigation

The single most informative next investigation is:

> **Test whether explicit cross-modal conflict detection improves arbitration and calibrated uncertainty on a small, leakage-resistant image–text conflict set.**

This should come before implementing token pruning, LoRA adaptation, or a Bengali extension.

The reason is that it simultaneously tests several unresolved boundaries:

1. [C³PO](https://www.alphaxiv.org/abs/2608.05381) shows that modality dominance is common.
2. [Which Source Wins?](https://www.alphaxiv.org/abs/2608.17205) shows that source reliance depends on task and evidence structure.
3. [Which Modality Decides?](https://www.alphaxiv.org/abs/2608.00076) shows that predictive accuracy does not reveal modality reliance.
4. [Visuals Lie, Consistency Speaks](https://www.alphaxiv.org/abs/2606.17389) shows that common visual-attention and confidence signals may be unreliable.
5. The conflict literature does not yet establish that recognizing disagreement leads to better decisions.

The recommended first experiment should therefore contain four paired conditions—clean, irrelevant, contradictory, and insufficient evidence—and compare direct answering with conflict detection, evidence listing, and abstention. The primary outcome should be **paired arbitration accuracy plus selective risk**, not a new model’s overall benchmark score.

If that experiment shows a robust improvement across models and conflict types, the next investigation should examine whether the improvement survives modality degradation and language shift. If it fails, the negative result will still sharply constrain the thesis space by showing that explicit conflict reasoning does not automatically repair modality dominance.