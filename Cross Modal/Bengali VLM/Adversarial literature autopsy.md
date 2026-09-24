
# Chat Transcript: Thesis field Bangla VLM

## User

(File attachment: text/plain)

(File attachment: text/markdown)

I am investigating a possible thesis field:
Evidence-Grounded Selective Prediction for Reliable Bangla Cultural Vision-Language Models

## Aurelle

> **Conducting research for user task**
>
> I need to conduct research based on the detailed task and thesis the user provided. I’ll use tool calls to find the top 10 papers from 2025-26. There are known IDs from the user's file, and I’ll discover some broad topics before reading the actual papers. I plan to use the answer_pdf feature for these IDs in parallel, sticking to about ten PDFs at a time. I'll make sure to include key papers in the search.

> **Searched Papers**
> 6 searches · 120 papers · SAVOR: Self-Aware Visual Grounding via Confidence-Calibrated Reinforcement Learning for Multimodal Hallucination Mitigation · Uncertainty-Aware Decision Making in Multimodal Large Language Models · The Mirage of Calibrated Confidence: Trajectory-Independence of Verbalized Confidence in Vision-Language Models · Spatial-Semantic Uncertainty in VLM-Based Target Search: Balancing Exploration and Identification · UR$^{2}$-MLLM: Uncertainty-aware Revisit Reasoning in Multimodal Large Language Models for Radiology Report Generation · Separating Capability from Confidence: Grounded Dual-State Calibration for GRPO-Trained Medical Vision-Language Models · Where to Look Matters: Learning Influential Views for VLM-based 3D Visual Grounding · HalluPrism: When Multimodal Uncertainty Should Diagnose, Not Decide · Reconstruction: A Blind Benchmark for Recovering Research Ideas from Pre-Publication Bibliographies · A Pathway to General-Purpose Scientific AI: Multimodal Comprehension of Scientific Images · LitTraceQA: A Benchmark for Multi-Stage Grounding and Verification in Scientific Question Answering · Confidence Estimation for Financial Vision-Language Models in Chart and Document Understanding · Localized Conformal Prediction for Image Classification with Vision-Language Models · SIEVES: Selective Prediction Generalizes through Visual Evidence Scoring · Entropy-Gradient Grounding: Training-Free Evidence Retrieval in Vision-Language Models · Vision Language Models: A Survey of 26K Papers · STSG-VQA: Evidence-Grounded Temporal Question Answering from Surgical Spatio-Temporal Scene Graphs · Inter-3D VQA: A Roadside Multimodal Benchmark for 3D Spatiotemporally Grounded Visual Question Answering · Option-Aware Retrieval and Task-Specific VLM Adaptation for Medical VQA · Register Shifts Break LLM Safety: A Bengali Benchmark with Culturally Grounded Harms · BanglaShop-CRS: A User-Centric Bangla Dataset for Conversational Recommendation · Harnessing Image Question Dependence for Better VLM Test-time Reinforcement Learning · LogiScope-VQA: Benchmarking Vision-Language Models for Logistics Hazard Identification in Industrial Scenarios · From Reasoning to Pixels: Grounded Medical Multimodal LLMs for VQA and Segmentation · BanglaMemeX: Advancing Cultural Metaphoric Image Interpretation in Bangla with a Multimodal Explainable Dataset · FinAbstain: Uncertainty-Calibrated Multimodal RAG for Selective Financial Forecasting · When a Name Is Not a Name: A Benchmark Dataset and Distilled Reasoning for Culturally Entangled Bangla Homographs in Low-Resource LLMs · Knowing When Not to Answer: Evaluating Abstention in Multimodal Reasoning Systems · ValueGround: Evaluating Culture-Conditioned Visual Value Grounding in MLLMs · Many Dialects, Many Languages, One Cultural Lens: Evaluating Multilingual VLMs for Bengali Culture Understanding Across Historically Linked Languages and Regional Dialects · BodyCam-VQA: Enhanced Body-Worn Camera Video Captioning via Multimodal Reasoning and Probe Question Generation · High-Fidelity Video Quality Assessment with VQA-Specific Saliency · Selective Tool Use for Agentic Change Visual Question Answering in Remote Sensing · Leveraging Visual Signals for Robust Token-Level Uncertainty in Vision-Language Generation · Entropy Alone is Insufficient for Safe Selective Prediction in LLMs · Once Correct, Still Wrong: Counterfactual Hallucination in Multilingual Vision-Language Models · CultureVLM: Characterizing and Improving Cultural Understanding of Vision-Language Models for over 100 Countries
> **Read 10 results**
> Many Dialects, Many Languages, One Cultural Lens: Evaluating Multilingual VLMs for Bengali Culture Understanding Across Historically Linked Languages and Regional Dialects · SIEVES: Selective Prediction Generalizes through Visual Evidence Scoring · Look Again Before You Abstain:Budgeted Conformal Evidence Acquisition for Reliable Vision-Language Model · Grounded or Guessing? LVLM Confidence Estimation via Blind-Image Contrastive Ranking · Confidence Estimation for Financial Vision-Language Models in Chart and Document Understanding · TRAPSBench: Vision-Language Models Encode but Fail to Express Epistemic Restraint · Benchmarking Retrieval-Augmented Generation for Chemistry · Less is More: Making Smaller Language Models Competent Subgraph Retrievers for Multi-hop KGQA · https://aclanthology.org/2024.findings-acl.767/ · https://aclanthology.org/2024.findings-emnlp.285/

> **Formulating the report**
>
> I'm thinking about how to present the 2026 papers. Should I use a chart? Maybe a matrix might be more fitting, but then again, I wonder if numbers are really necessary. It feels like a chart might be unnecessary for this comparison, which makes me rethink how I want to formulate the information. I need to clarify what the best visual representation for these findings will be!

# Adversarial literature autopsy

The proposed field is **not pre-empted as a whole**, but its claimed novelty is substantially narrower than the proposal currently suggests: **visual-evidence-aware confidence, selective abstention, risk–coverage analysis, and evidence acquisition have already been experimentally established in general VLMs**.

The genuinely unresolved part is the intersection of those mechanisms with **culturally unfamiliar Bangla entities and externally retrieved cultural evidence**—provided that the study demonstrates something beyond simply applying an existing selector to a new dataset.

## Executive verdict


| Proposed component                                                                                   | Status in prior work                              |
| ------------------------------------------------------------------------------------------------------ | --------------------------------------------------- |
| Answer correctness confidence                                                                        | **Established**                                   |
| Calibration of VLM confidence                                                                        | **Established**                                   |
| Selective prediction / abstention                                                                    | **Established**                                   |
| Risk–coverage evaluation                                                                            | **Established**                                   |
| Visual-dependence or visual-grounding confidence                                                     | **Established**                                   |
| Visual evidence quality scoring                                                                      | **Established**                                   |
| Evidence acquisition before abstention                                                               | **Established**                                   |
| Conformal risk control for visual claims                                                             | **Established**                                   |
| External textual cultural evidence supporting an entity                                              | **Not established in the closest VLM literature** |
| Bangla cultural entity uncertainty/calibration                                                       | **Potential gap**                                 |
| Joint answer confidence + visual evidence + external cultural evidence + abstention + risk–coverage | **Not found as an established combination**       |

The most serious pre-emption risk is therefore not that someone has already studied Bangla cultural uncertainty. It is that the central methodological idea—**use evidence about the image to decide whether a VLM answer should be accepted or rejected**—has already been demonstrated by several papers.

## Top 10 closest papers


| Paper                                                                                                                                                                                                                               | Why it is close                                                                                                                         | Autopsy classification   |
| ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | ----------------------------------------------------------------------------------------------------------------------------------------- | -------------------------- |
| [SIEVES: Selective Prediction Generalizes through Visual Evidence Scoring](https://www.alphaxiv.org/abs/2604.25855)                                                                                                                 | Directly combines selective prediction, visual evidence, localization quality, evidence–answer coherence, and risk–coverage.          | **PARTIALLY OCCUPIED**   |
| [Look Again Before You Abstain](https://www.alphaxiv.org/abs/2606.16667)                                                                                                                                                            | Combines visual evidence scoring, abstention, additional image acquisition, recalibration, and finite-sample risk control.              | **PARTIALLY OCCUPIED**   |
| [Grounded or Guessing?](https://www.alphaxiv.org/abs/2605.10893)                                                                                                                                                                    | Uses real-image versus blank-image hidden-state contrast to detect visually ungrounded confidence.                                      | **PARTIALLY OCCUPIED**   |
| [Confidence Estimation for Financial Vision-Language Models](https://www.alphaxiv.org/abs/2608.06532)                                                                                                                               | Evaluates seven confidence estimators, calibration, grounding-aware confidence, and automate-or-defer risk–coverage across five LVLMs. | **PARTIALLY OCCUPIED**   |
| [TRAPSBench](https://www.alphaxiv.org/abs/2608.13167)                                                                                                                                                                               | Tests whether VLMs abstain when visual evidence is insufficient and distinguishes encoded uncertainty from expressed abstention.        | **RELATED BUT DISTINCT** |
| [BANGLAVERSE](https://www.alphaxiv.org/abs/2603.21165)                                                                                                                                                                              | Establishes the Bangla cultural evaluation setting, local-entity failures, dialect variation, and knowledge-intensive cultural errors.  | **PARTIALLY OCCUPIED**   |
| [Selective “Selective Prediction” / ReCoVERR](https://aclanthology.org/2024.findings-acl.767/)                                                                                                                                    | Acquires additional visual clues before converting an abstention into an answer.                                                        | **PARTIALLY OCCUPIED**   |
| [HallusionBench](https://openaccess.thecvf.com/content/CVPR2024/html/Guan_HallusionBench_An_Advanced_Diagnostic_Suite_for_Entangled_Language_Hallucination_and_Visual_Illusion_in_Large_Vision-Language_Models_CVPR2024_paper.html) | Diagnoses visual illusion and language-induced hallucination using controlled visual reasoning tests.                                   | **RELATED BUT DISTINCT** |
| [THRONE](https://openaccess.thecvf.com/content/CVPR2024/html/Kaul_Throne_An_Object-Based_Hallucination_Benchmark_for_the_Free-form_Generations_of_Large_Vision-Language_Models_CVPR2024_paper.html)                                 | Measures object-level hallucination in free-form LVLM generations.                                                                      | **RELATED BUT DISTINCT** |
| [POPE](https://aclanthology.org/2023.emnlp-main.20/)                                                                                                                                                                                | Established object-hallucination evaluation through positive and negative object-existence questions.                                   | **RELATED BUT DISTINCT** |

The first five should be treated as the principal methodological threats. BANGLAVERSE is the principal domain-specific threat.

# 1. Detailed paper autopsies

## 1. SIEVES

### Exact research question

SIEVES asks whether selective prediction for VQA becomes more generalizable when the answering reasoner produces explicit visual evidence—particularly localized crops—and a separate selector evaluates that evidence rather than relying only on logits or language patterns.

The paper explicitly frames the problem as maximizing coverage under a user-defined risk level. Its selector receives the question, image, multimodal chain of thought, crops, and final answer. [Research Question](https://www.alphaxiv.org/abs/2604.25855?page=2)

### Hypothesis

The central hypothesis is that **explicit visual localization makes answer correctness easier to estimate**, especially under distribution shift. The selector should benefit from knowing:

- whether the relevant region was localized;
- whether the answer is coherent with that visual evidence;
- whether the final answer is correct.

SIEVES therefore predicts three values:

$$
c_{\mathrm{corr}},\quad c_{\mathrm{loc}},\quad c_{\mathrm{coh}}.

$$

The paper argues that predicting visual evidence quality is superior to predicting answer correctness alone. [Method](https://www.alphaxiv.org/abs/2604.25855?page=4)

### Model and data

- Reasoner: Pixel-Reasoner, plus evaluations with o3 and Gemini-3-Pro.
- Selector: Gemma-3-4B with three value heads.
- Selector training: Thyme and TAT-DQA.
- Evaluation: V*-Bench, HR-Bench-8k, MME-RealWorld-Lite, VizWiz, and AdVQA.
- Evaluation is deliberately out-of-distribution.

The selector is trained on traces from Pixel-Reasoner and tested on other reasoners without model-specific adaptation. [Experimental Setup](https://www.alphaxiv.org/abs/2604.25855?page=6)

### Confidence, grounding, and evidence definitions

- **Confidence:** a scalar derived from the selector’s correctness, localization, and coherence outputs.
- **Grounding:** whether the reasoner localized the relevant visual region.
- **Evidence:** zoomed-in image crops and the multimodal reasoning trace.
- **External evidence:** not used.
- **Abstention:** answers below a threshold are filtered.
- **Evidence acquisition:** the reasoner uses zoom-in localization while answering, but SIEVES itself is primarily a selector, not a budgeted look-again policy.

### Metrics and controls

SIEVES reports:

- coverage at fixed risk, $C@r$;
- AURC;
- answer accuracy;
- risk–coverage curves.

Its controls include:

1. Pixel-Reasoner with and without localization;
2. log-probability confidence;
3. zero-shot verbal confidence;
4. zero-shot logit confidence;
5. a correctness-only selector;
6. ablations removing correctness, localization, or coherence objectives.

The paper defines:

$$
C@r=\max_{\tau} C(\tau)\quad \text{subject to}\quad R(\tau)\leq r.

$$

[Metrics](https://www.alphaxiv.org/abs/2604.25855?page=14)

### Strongest result

SIEVES substantially improves low-risk coverage. For example, on Pixel-Reasoner with localization, it reports:

- V*-Bench: $C@5=9.7$;
- HR-Bench-8k: $C@5=2.3$;
- MME-RealWorld-Lite: $C@5=4.0$;
- VizWiz: $C@20=7.6$;
- AdVQA: $C@10=2.8$.

It also transfers to o3 and Gemini-3-Pro despite being trained only on Pixel-Reasoner traces. [Results](https://www.alphaxiv.org/abs/2604.25855?page=7)

The ablation evidence is especially important: removing any of correctness, localization, or coherence damages performance. [Ablations](https://www.alphaxiv.org/abs/2604.25855?page=9)

### Limitations and non-tests

SIEVES does **not** test:

- Bangla or culturally unfamiliar entities;
- external textual cultural evidence;
- retrieval quality;
- cultural knowledge uncertainty;
- whether the localized crop is semantically sufficient for an entity-level identification;
- whether the answer is supported by an authoritative cultural source;
- formal conformal guarantees;
- culturally conditioned calibration.

### Autopsy

**PARTIALLY OCCUPIED.**

SIEVES already occupies the proposal’s combination of:

> answer confidence + visual evidence dependence + selective abstention + risk–coverage.

It does not occupy:

> external cultural evidence + Bangla cultural entity recognition.

However, “visual evidence improves selective prediction” is no longer a defensible primary novelty claim.

## 2. Look Again Before You Abstain

This is the strongest methodological pre-emption risk.

### Exact research question

The paper asks whether a VLM can obtain more reliable coverage by **acquiring additional visual evidence before abstaining**, while preserving a distribution-free selective-risk guarantee.

It explicitly identifies a failure in naive evidence acquisition: calibrating a threshold before acquisition and applying it after acquisition can invalidate the guarantee because acquisition changes the score distribution. [Core Problem](https://www.alphaxiv.org/abs/2606.16667?page=2)

### Model and data

- Main model: LLaVA-1.5-7B.
- Generality experiments: Qwen3-VL-7B, LLaVA-NeXT, InternVL2.
- Data: COCO-derived object-existence and spatial-relation claims; POPE; free-form captions.
- Evidence acquisition: crops, zooms, and claim-specific interventions such as horizontal flips.

### Confidence, grounding, evidence, and abstention

- **Confidence:** an evidence-sufficiency score based on the difference between the claim score with the image and with a blank image.
- **Grounding:** dependence of the claim likelihood on the visual input.
- **Evidence:** original images, crops, masked regions, and claim-specific transformations.
- **Abstention:** reject claims below a conformally calibrated threshold.
- **Acquisition:** a three-way policy: answer, abstain, or acquire more evidence.

The deployed score includes acquisition itself:

$$
s_{\mathcal A}(x,c)=
\max\left(\ell(x,c),\max_b\ell(x^{(b)},c)\right)-\ell(\varnothing,c).

$$

The paper’s key theoretical point is that calibration must be performed on the score actually used after acquisition. [BCEA](https://www.alphaxiv.org/abs/2606.16667?page=4)

### Metrics and controls

It reports:

- coverage;
- selective hallucination risk;
- AUROC;
- certified coverage;
- empirical risk–coverage frontiers;
- violation frequency across repeated calibration/test splits.

Controls include:

- abstention without acquisition;
- naive acquisition with pre-acquisition calibration;
- uniform grid crops;
- CLIP-guided crops;
- claim-specific horizontal flips;
- multiple VLM backbones;
- exact and practical calibration variants.

### Strongest result

On balanced existence claims, abstention alone reaches only 18% empirical coverage at 5% risk. Acquisition raises the empirical frontier. The global evidence score has AUROC $0.838$, while acquisition raises it to $0.879$. [Evidence Acquisition](https://www.alphaxiv.org/abs/2606.16667?page=5)

For self-generated free-form object claims, BCEA certifies 34% of claims at a guaranteed hallucination rate of at most 10%, compared with 24% for abstention alone. [Free-Form Claims](https://www.alphaxiv.org/abs/2606.16667?page=7)

### Limitations and non-tests

The paper explicitly does not test:

- cultural entities;
- multilingual or Bangla questions;
- external documentary evidence;
- entity disambiguation;
- cultural knowledge errors;
- the distinction between a visually identifiable object and a historically or culturally identified entity;
- full free-form claim decomposition beyond object mentions;
- attributes, relations, and counts in the free-form pipeline.

The paper states that the free-form parser handles object mentions only; attributes, relations, and counts remain outside scope. [Scope Boundary](https://www.alphaxiv.org/abs/2606.16667?page=13)

### Autopsy

**PARTIALLY OCCUPIED**, very close to **PRE-EMPTED** for the generic methodology.

The proposal’s “answer or abstain” framing is actually less advanced than BCEA’s answer/abstain/acquire formulation. If the thesis does not use formal risk control, it should not claim novelty from evidence acquisition or risk-aware abstention.

## 3. Grounded or Guessing? / BICR

### Exact research question

BICR asks whether confidence estimation can distinguish a genuinely image-grounded answer from a fluent answer produced primarily from language priors.

The paper uses a real image and a blank-image counterfactual during training. A probe is encouraged to assign lower confidence to the blank-image representation. [BICR Objective](https://www.alphaxiv.org/abs/2605.10893?page=2)

### Model and data

- Five open-weight LVLMs.
- VLCB benchmark containing seven visual-question-answering sources.
- Training confidence probes on GQA.
- Testing on GQA, POPE, GMAI-MMBench, MME-Finance, MMMU-Pro, and LLaVA-in-the-Wild.

### Confidence and grounding

- **Confidence:** a learned probability that the generated answer is correct.
- **Grounding:** operationalized as the difference between hidden states produced by the real image and a blank image.
- **Evidence:** not human-readable evidence or retrieved sources; it is an internal representational contrast.
- **Abstention:** not the principal deployed decision mechanism.
- **Selective metrics:** calibration and discrimination are central; risk–coverage is not the main contribution.

The paper is unusually explicit that its grounding notion is only an operational proxy. It does not directly measure semantic grounding. [Limitation](https://www.alphaxiv.org/abs/2605.10893?page=10)

### Metrics and controls

- ECE;
- Brier score;
- AUROC;
- AUCPR;
- reliability diagrams;
- cluster-aware statistical testing;
- ablations removing the ranking loss.

### Strongest result

BICR obtains pooled ECE $0.056$, compared with $0.078$ for InternalInspector and much larger errors for verbal and prompt-based methods. [Calibration](https://www.alphaxiv.org/abs/2605.10893?page=8)

The paper also reports that removing the ranking loss reduces AUROC by 3.32 points. [Ranking Loss](https://www.alphaxiv.org/abs/2605.10893?page=9)

### Limitations and non-tests

BICR does not test:

- Bangla;
- multilingual cultural data;
- external evidence;
- retrieval;
- user-facing evidence citations;
- answer-level conformal risk control;
- whether a cultural identity is visually present but not culturally known;
- whether blank-image invariance reliably diagnoses culturally unsupported answers.

It also requires hidden-state access and does not transfer directly to closed models. Its authors explicitly state that results may not transfer cleanly to multilingual settings. [Limitations](https://www.alphaxiv.org/abs/2605.10893?page=10)

### Autopsy

**PARTIALLY OCCUPIED.**

The proposal’s visual-grounding confidence component is already represented by BICR, although the proposed perturbation design is different. A blank, blurred, or mismatched-image test is therefore not automatically novel. The scientific question must concern **which visual-dependence signal is valid for culturally specific entity recognition**, not merely whether perturbing the image changes the answer.

## 4. Confidence Estimation for Financial Vision-Language Models

This paper is especially important because it directly combines confidence estimation, grounding awareness, calibration, and deployment-oriented deferral.

### Exact research question

The paper asks which confidence estimators can identify trustworthy answers from financial VLMs under out-of-distribution transfer and an automate-or-escalate error budget.

It distinguishes calibration from ranking: a score may order correct answers above incorrect ones while still being too miscalibrated to support a safe threshold. [Calibration Versus Ranking](https://www.alphaxiv.org/abs/2608.06532?page=2)

### Model and data

- Five open-weight LVLMs.
- FinMME;
- FinChart-Bench;
- MME-Finance in English and Chinese;
- confidence probes trained on GQA and transferred without financial adaptation.

### Confidence and grounding

It evaluates seven estimators:

- verbal or prompt-based confidence;
- P(True);
- Self-Probing;
- Prompt Ensemble;
- SAPLMA;
- CCPS;
- InternalInspector;
- BICR.

Grounding is assessed through figure-invariance behavior: whether the answer remains unchanged when the chart is replaced by a blank or random image. BICR is the only estimator explicitly trained with a grounding contrast.

### Metrics and controls

- ECE;
- Brier score;
- AUROC;
- AUCPR;
- confident-error rate;
- risk–coverage curves;
- safe yield at 5% and 10% error budgets.

Controls are unusually strong:

- five models;
- four evaluation conditions;
- common correctness judging;
- five probe-training seeds;
- image-invariant subpopulation analysis;
- per-task and per-language analysis.

### Strongest results

Inference-only methods are often competitive at ranking but severely overconfident. Self-Probing labels nearly nine out of ten errors with confidence above 0.8. Trained probes reduce this confident-error rate substantially. [Main Finding](https://www.alphaxiv.org/abs/2608.06532?page=3)

BICR and InternalInspector provide the strongest calibration, but no method dominates all model-condition cells. The best method changes with task and model. [No Universal Estimator](https://www.alphaxiv.org/abs/2608.06532?page=3)

Risk–coverage results show that safe automation is highly constrained by base-model competence. On hard financial conditions, even good confidence estimators provide little safe coverage. [Deployment](https://www.alphaxiv.org/abs/2608.06532?page=7)

### Limitations and non-tests

It does not test:

- external evidence retrieval;
- culturally unfamiliar entities;
- Bangla;
- historical or cultural knowledge;
- human-authored evidence support;
- answerability separate from correctness;
- a claim-level evidence verifier.

It also uses an LLM judge and a first-token invariance proxy for some grounding tests. [Limitations](https://www.alphaxiv.org/abs/2608.06532?page=7)

### Autopsy

**PARTIALLY OCCUPIED.**

This paper undermines the proposal’s assumption that combining several confidence signals will straightforwardly improve reliability. It finds that:

1. calibration and discrimination are different;
2. confidence quality is task-dependent;
3. the best estimator is not universal;
4. safe coverage depends strongly on base-model competence;
5. grounding-aware confidence is useful but not sufficient.

## 5. TRAPSBench

TRAPSBench is not a direct competitor in cultural VQA, but it attacks an important assumption: that models will express uncertainty when uncertainty is internally available.

### Research question

Do VLMs recognize when visual evidence is insufficient, and if they recognize it internally, do they express that uncertainty through abstention?

The benchmark uses matched simulated videos: one answerable control and one minimally modified unanswerable “void” case. [Benchmark Design](https://www.alphaxiv.org/abs/2608.13167?page=2)

### Model and task

- 16 VLMs;
- 1,404 matched physics pairs;
- visual occlusion;
- chaotic sensitivity;
- ill-posed questions.

### Confidence and abstention definition

- **Answerability:** whether the visual evidence licenses a deterministic answer.
- **Abstention:** failure to provide an answer on void cases.
- **Confidence:** not a scalar confidence score in the proposal’s sense.
- **Metric:** Penalized Epistemic Calibration Score:

$$
\mathrm{PECS}
=
\mathrm{Acc}
\cdot
\max(0,\mathrm{AbsRec}-\mathrm{FalseAbs}).

$$

This penalizes both never abstaining and abstaining indiscriminately. [PECS](https://www.alphaxiv.org/abs/2608.13167?page=4)

### Strongest result

The best standard-regime PECS is only 0.292. Linear probes recover answerability from hidden states with AUROC up to 0.91, while output behavior remains poorly restrained. Guided prompts improve abstention, revealing a representation–output gap. [Main Results](https://www.alphaxiv.org/abs/2608.13167?page=6)

Models detect textual impossibility much more readily than missing visual evidence—approximately four times more readily on average, with larger gaps in some settings. [Visual Versus Textual](https://www.alphaxiv.org/abs/2608.13167?page=6)

### Non-tests

TRAPSBench does not test:

- cultural knowledge;
- entity identification;
- external evidence;
- retrieval;
- ordinary image VQA;
- calibration curves or risk–coverage in the standard selective-classification sense;
- whether a model knows an entity but cannot name it.

### Autopsy

**RELATED BUT DISTINCT.**

It pre-empts the proposal’s implicit assumption that prompting for confidence or abstention reveals genuine uncertainty. Verbal confidence may reflect output behavior rather than a reliable epistemic state.

## 6. BANGLAVERSE

BANGLAVERSE provides the strongest evidence that the target domain is scientifically nontrivial, but it does not study uncertainty.

### Research question

BANGLAVERSE asks whether multilingual VLMs genuinely understand Bengali culture across standard Bangla, English, Hindi, Urdu, and five Bangla dialects, rather than merely performing well in standard Bangla.

### Model, data, and task

- 1,152 manually curated images;
- nine domains;
- approximately 32.2K language/dialect artifacts;
- VQA and captioning;
- Gemma 3, Qwen2.5-VL, Qwen3-VL, and GPT-4.1-mini;
- zero-shot, few-shot, and chain-of-thought prompting.

### Confidence, grounding, evidence, abstention

BANGLAVERSE has:

- no confidence score;
- no calibration metric;
- no answerability label;
- no selective abstention;
- no risk–coverage curve;
- no external evidence-support condition.

It evaluates accuracy, BERTScore, and LLM-as-a-judge caption quality. [Evaluation Metrics](https://www.alphaxiv.org/abs/2603.21165?page=6)

### Strongest results

Dialect variation causes a small but significant VQA drop and a substantially larger caption-quality drop. For GPT-4.1-mini, VQA falls 2.29 points from standard Bangla to the dialect average, while caption quality falls 14.84 points. [Dialect Results](https://www.alphaxiv.org/abs/2603.21165?page=7)

The most relevant result is the error analysis: local entity and artifact misrecognition accounts for 42.6% of coded failures, while surface-level descriptive fallback accounts for 30.8%. [Error Analysis](https://www.alphaxiv.org/abs/2603.21165?page=9)

The paper also finds that knowledge-intensive domains such as politics and media/movies are harder than visually concrete food tasks. [Domain Difficulty](https://www.alphaxiv.org/abs/2603.21165?page=9)

### Limitations and non-tests

BANGLAVERSE explicitly does not establish:

- whether a model is calibrated;
- whether confidence predicts local-entity correctness;
- whether dialect difficulty causes overconfidence;
- whether cultural evidence can repair an entity error;
- whether a model should abstain;
- whether a local entity is visually identifiable without external knowledge.

The authors also state that none of the evaluated systems is Bangla-specific. [Scope](https://www.alphaxiv.org/abs/2603.21165?page=10)

### Autopsy

**PARTIALLY OCCUPIED**, but in the opposite direction: BANGLAVERSE occupies the domain, not the reliability question.

The proposal can legitimately build on BANGLAVERSE. It cannot claim that BANGLAVERSE already demonstrates Bangla calibration or evidence-grounded uncertainty.

## 7. ReCoVERR

ReCoVERR is particularly relevant to the phrase “evidence acquisition before abstention.”

It asks whether a low-confidence VLM answer should be rejected immediately or whether the system should ask related visual questions to gather additional clues. It uses an LLM to generate follow-up questions and accepts an answer when the collected evidence is sufficiently consistent. The paper reports up to 20% more answered questions without reducing system accuracy on VQAv2 and A-OKVQA. [ReCoVERR](https://aclanthology.org/2024.findings-acl.767/)

However, ReCoVERR:

- does not use cultural evidence;
- does not study Bangla;
- does not provide conformal guarantees;
- does not evaluate local-entity recognition;
- uses heuristic evidence aggregation;
- does not make external evidence provenance central.

Classification: **PARTIALLY OCCUPIED**.

## 8. HallusionBench, THRONE, and POPE

These papers are not selective-prediction papers, but they invalidate a common proposal shortcut: treating every incorrect answer as a single kind of “hallucination.”

- [POPE](https://aclanthology.org/2023.emnlp-main.20/) focuses on object-existence hallucination using positive and negative questions.
- [THRONE](https://openaccess.thecvf.com/content/CVPR2024/html/Kaul_Throne_An_Object-Based_Hallucination_Benchmark_for_the_Free-form_Generations_of_Large_Vision-Language_Models_CVPR2024_paper.html) evaluates object-level hallucination in free-form generation.
- [HallusionBench](https://openaccess.thecvf.com/content/CVPR2024/html/Guan_HallusionBench_An_Advanced_Diagnostic_Suite_for_Entangled_Language_Hallucination_and_Visual_Illusion_in_Large_Vision-Language_Models_CVPR2024_paper.html) separates language-induced hallucination from visual illusion through controlled diagnostic cases.

They do not establish calibration or culturally grounded selective prediction, but they occupy the broader diagnostic territory of visual hallucination and visual-versus-language failure analysis.

Classification: **RELATED BUT DISTINCT**.

# 2. Technical overlap matrix

Legend:

- **✓**: directly tested;
- **△**: related proxy or partial test;
- **—**: not tested.


| Paper                     | Answer confidence | Visual grounding | External evidence | Evidence acquisition | Abstention | Calibration | Risk–coverage | Cultural/Bangla |
| --------------------------- | ------------------: | -----------------: | ------------------: | ---------------------: | -----------: | ------------: | ---------------: | ----------------: |
| SIEVES                    |                ✓ |               ✓ |                — |                   △ |         ✓ |          △ |             ✓ |              — |
| Look Again                |                ✓ |               ✓ |                — |                   ✓ |         ✓ |          ✓ |             ✓ |              — |
| BICR                      |                ✓ |               ✓ |                — |                   — |         △ |          ✓ |             △ |              — |
| Financial LVLM confidence |                ✓ |               ✓ |                — |                   — |         ✓ |          ✓ |             ✓ |              — |
| TRAPSBench                |                △ |               ✓ |                — |                   — |         ✓ |          △ |             — |              — |
| BANGLAVERSE               |                — |               △ |                — |                   — |         — |          — |             — |              ✓ |
| ReCoVERR                  |                ✓ |               ✓ |                — |                   ✓ |         ✓ |          △ |             △ |              — |
| HallusionBench            |                — |               ✓ |                — |                   — |         — |          — |             — |              — |
| THRONE                    |                — |               △ |                — |                   — |         — |          — |             — |              — |
| POPE                      |                — |               △ |                — |                   — |         — |          — |             — |              — |

The crucial observation is that **no row contains all five of the proposal’s central components**:

1. answer confidence;
2. visual evidence dependence;
3. external cultural evidence;
4. selective abstention;
5. risk–coverage.

But the first two, plus abstention and risk–coverage, are already jointly present in SIEVES and partly in the financial-confidence study. Evidence acquisition and calibrated risk control are present in Look Again.

# 3. Is the full combination already established?

## Short answer

**No, not in the literature inspected.**

The combination appears to be:

> answer confidence + visual evidence dependence + external cultural evidence + selective abstention + risk–coverage

The closest decomposition is:

- **SIEVES:** answer confidence + visual evidence + abstention + risk–coverage;
- **BICR:** confidence + visual-dependence contrast + calibration;
- **Look Again:** visual evidence + acquisition + abstention + conformal risk control;
- **ReCoVERR:** confidence-triggered evidence acquisition before answering;
- **BANGLAVERSE:** Bangla cultural entity and dialect evaluation;
- **Financial LVLM confidence:** calibration and deferral under domain shift.

The missing link is **external cultural evidence used as a calibrated support or contradiction signal for image-grounded entity answers**.

## Is that a meaningful scientific question or merely an engineering combination?

It is meaningful only if the study tests a substantive hypothesis such as:

> When a VLM encounters a culturally unfamiliar entity, does external cultural evidence improve the calibration of its confidence, or does retrieval merely increase answer accuracy while leaving confidence overconfident and untrustworthy?

That is a scientific question because it separates several mechanisms:

- visual recognition;
- language-prior reliance;
- cultural knowledge availability;
- retrieval quality;
- evidence interpretation;
- answer confidence;
- abstention behavior.

It becomes an engineering combination if the claim is only:

> Add retrieval, visual perturbations, and a logistic-regression confidence score, then measure whether accuracy improves.

That would mainly be a pipeline integration study. The scientific value must come from **disentangling why the combined system succeeds or fails**, especially when external evidence is:

- correct but irrelevant;
- relevant but contradictory;
- generic rather than entity-specific;
- available only in Bangla;
- available in English but not Bangla;
- retrieved because of the model’s prior answer rather than the image.

# 4. Strongest pre-emption risks

## Risk 1: “Visual-grounding confidence is novel”

This is no longer defensible in general form.

BICR explicitly trains confidence using blank-image contrast. SIEVES explicitly scores localization and evidence–answer coherence. The financial-confidence paper evaluates grounding-aware confidence under multiple models and tasks.

A defensible narrower claim would be:

> Existing grounding-confidence methods have not been validated for culturally unfamiliar Bangla entity identification, where visual evidence may be insufficient to distinguish visually similar local entities.

## Risk 2: “Evidence before abstention is novel”

This is directly challenged by both ReCoVERR and Look Again.

The distinction that remains is:

- ReCoVERR acquires additional visual clues;
- Look Again acquires additional visual evidence with conformal recalibration;
- the proposal introduces **external cultural evidence**, which is a different evidence modality.

The thesis must not describe evidence acquisition itself as novel.

## Risk 3: “Risk–coverage for VLMs is novel”

It is well established in SIEVES, Look Again, and the financial-confidence work.

The possible contribution is instead:

> risk–coverage behavior under cultural and linguistic distribution shift.

That must be demonstrated with appropriate controls, not assumed from using BANGLAVERSE.

## Risk 4: “A combined confidence score is novel”

The proposed weighted score

$$
C_{\text{combined}}
=
w_1 C_{\text{answer}}
+
w_2 C_{\text{visual}}
+
w_3 C_{\text{evidence}}

$$

is methodologically ordinary. A learned logistic-regression fusion model is also standard.

The novelty cannot reside in the weighted sum. It would have to reside in the finding that **different signals fail differently across cultural categories**, or that external evidence changes calibration in a way not explained by accuracy improvement.

## Risk 5: “Verbal self-confidence is a meaningful confidence signal”

TRAPSBench and the confidence-estimation studies warn against this assumption. Verbal confidence is an output behavior and may not reflect the model’s internal uncertainty. TRAPSBench shows that models can encode uncertainty yet fail to express it, while the financial study finds severe overconfidence in prompt-based estimators. [Representation–Output Gap](https://www.alphaxiv.org/abs/2608.13167?page=10)

Therefore, verbal confidence should be treated as a weak baseline, not as a principled confidence definition.

# 5. Claims in the proposal that are too strong or incorrectly assumed

## Claim: “Existing work has not systematically evaluated evidence-grounded selective prediction”

Too broad.

SIEVES is explicitly a study of selective prediction through visual evidence scoring. Look Again is explicitly evidence acquisition before abstention with calibrated risk control.

A corrected version would be:

> Existing work has studied visual-evidence-aware selective prediction and evidence acquisition, but their interaction with external cultural evidence and Bangla cultural entity recognition remains untested.

## Claim: “External cultural evidence is part of the established reliability literature”

Not established by the closest papers.

The external evidence component is the most plausible remaining gap, but it is also the most difficult to define scientifically. Retrieved text can support an entity without proving that the image depicts that entity. It may only confirm that the entity exists.

## Claim: “Visual perturbation measures whether the answer depends on the image”

Only partially.

BICR explicitly calls its blank-image hidden-state difference an operational proxy rather than a direct measurement of semantic grounding. Look Again also finds that global image-dependence scores fail for relational claims; a claim-specific intervention is needed. [Relational Grounding](https://www.alphaxiv.org/abs/2606.16667?page=13)

For Bangla cultural identity, blank-image invariance may reveal language-prior reliance, but it cannot establish that the model visually recognized the correct local entity.

## Claim: “Bangla VLM errors are mainly visual recognition failures”

BANGLAVERSE points in a more complicated direction. Its domain analysis identifies missing cultural knowledge and fine-grained entity recognition as major bottlenecks, not merely visual perception. Its authors explicitly caution that low performance may also reflect entity-recognition and answer-option confusability. [Cultural Bottlenecks](https://www.alphaxiv.org/abs/2603.21165?page=9)

## Claim: “A local entity can be labeled as visually identifiable”

This requires careful separation.

A person’s face, a food shape, or a garment may be visually observable. The culturally specific name, historical significance, regional identity, or political affiliation may not be visually identifiable without external knowledge.

The annotation schema should therefore distinguish:

1. visual observability;
2. visual discriminability among candidate entities;
3. cultural identifiability;
4. answerability with external evidence;
5. answerability without external evidence.

Without this separation, an abstention may be incorrectly interpreted as a model failure when the question is not visually answerable.

## Claim: “A combined score should outperform each component”

This is a hypothesis, not a safe assumption.

The financial-confidence study finds that estimator quality changes by model and task, and no method dominates across all model-condition cells. [Estimator Dependence](https://www.alphaxiv.org/abs/2608.06532?page=3)

A fusion score may improve ranking while worsening calibration, or improve calibration while reducing coverage.

# 6. Bengali-specific audit

## Bengali VQA and BANGLAVERSE

BANGLAVERSE is the key domain paper. It covers Bengali cultural images, standard Bangla, English, Hindi, Urdu, and five regional dialects. Its relevant findings are:

- dialectal changes degrade VQA and captioning;
- caption generation is more fragile than answer-constrained VQA;
- knowledge-intensive domains are harder;
- local entity and artifact misrecognition is the largest coded error category;
- culturally specific errors include foreign-entity substitutions, generic descriptions, political bias, and gender stereotyping.

However, it does **not** link cultural unfamiliarity to calibration, confidence, abstention, or risk–coverage.

## Bengali/Bangla cultural VLMs

The inspected literature does not establish a mature Bangla-specific cultural VLM reliability line. BANGLAVERSE states that its evaluated models are multilingual general-purpose models, not Bangla-specific VLMs. [Model Scope](https://www.alphaxiv.org/abs/2603.21165?page=10)

That supports a potential gap, but not automatically a thesis contribution. The gap may simply reflect the small size and recent emergence of the benchmark.

## BanglaVerse and local entity recognition

The local-entity issue is clearly present. The error table reports:

- 40 of 94 notable errors as entity or artifact misrecognition;
- 29 as surface-level descriptive fallback;
- 14 as societal or cultural bias;
- 11 as language-constraint violations.

[Error Categories](https://www.alphaxiv.org/abs/2603.21165?page=23)

This creates a strong domain rationale for uncertainty research, but BANGLAVERSE does not show whether the model knows that it is uncertain.

## Culturally unfamiliar visual entities

The closest general literature supports the existence of this problem indirectly:

- BICR shows that an answer can be correct while visually ungrounded.
- SIEVES shows that localization and evidence coherence help selective prediction.
- TRAPSBench shows that visual information gaps are harder to detect than textual impossibility.
- BANGLAVERSE shows that cultural entity errors are common.

What is missing is a controlled test separating:

1. an entity that is visually obvious but culturally unknown;
2. an entity that is culturally known but visually ambiguous;
3. an entity that is visually and culturally answerable;
4. an entity for which external evidence is available but image evidence is insufficient.

That four-way distinction is more scientifically valuable than simply reporting Bangla accuracy.

# 7. False gaps caused by terminology differences

Several apparent gaps disappear once terminology is normalized.

## “Evidence-grounded confidence”

This may refer to at least four different things:

1. hidden-state difference between image and blank image — BICR;
2. localization quality — SIEVES;
3. coherence between crop evidence and answer — SIEVES;
4. claim likelihood under image interventions — Look Again.

These are not interchangeable. A thesis must specify which evidence notion it studies.

## “Grounding”

Grounding may mean:

- the model attended to relevant pixels;
- the answer changes when the image changes;
- the claim likelihood drops when the image is removed;
- the model’s crop overlaps the relevant object;
- the answer is semantically supported by the image.

The literature already shows these can disagree. Therefore, saying “grounding confidence” without an operational definition is too vague.

## “Evidence support”

External text that says “fuchka is a Bangladeshi food” supports the existence and cultural meaning of fuchka. It does not prove that the pictured object is fuchka.

Textual evidence support and image–entity support are different relations.

## “Hallucination”

POPE and THRONE mostly study nonexistent objects or unsupported visual claims. BANGLAVERSE also contains:

- entity substitution;
- generic fallback;
- cultural misinterpretation;
- political bias;
- language violations.

These should not all be collapsed into one hallucination rate.

## “Uncertainty”

The literature distinguishes:

- answer correctness confidence;
- visual grounding;
- epistemic answerability;
- response inconsistency;
- calibration;
- confidence ranking;
- selective risk.

The proposal currently treats these as related signals, but sometimes describes them as if they measured the same latent variable.

# 8. Genuine unresolved questions

These are stronger than simply “apply the method to BanglaVerse.”

## Question 1: Does cultural unfamiliarity produce distinctive miscalibration?

BANGLAVERSE establishes lower accuracy in culturally difficult domains, but not whether the confidence error increases disproportionately.

A meaningful question is whether models are:

- less accurate but equally calibrated;
- less accurate and more overconfident;
- accurate on generic visual description but overconfident on local identity;
- calibrated on food and clothing but miscalibrated on personalities, politics, and historical events.

## Question 2: Does visual grounding predict local-entity correctness?

A model may genuinely use the image and still identify the wrong local entity. BICR’s visual-dependence signal may therefore detect “looked at the image” without detecting “recognized the correct culture-specific identity.”

This is a major unresolved distinction:

> grounded wrongness versus ungrounded wrongness.

## Question 3: Does external cultural evidence improve calibration or only accuracy?

Retrieval may increase the number of correct answers while making confidence worse. A model may retrieve a passage about the entity it already guessed and then treat that passage as confirmation.

The important result may be negative:

> external evidence improves answer accuracy but does not improve selective reliability because retrieval is conditioned on the model’s unsupported hypothesis.

## Question 4: Can external evidence distinguish answerability from plausibility?

A retrieved passage can make a wrong prediction sound plausible. The system needs to determine whether evidence:

- supports the predicted entity;
- distinguishes it from alternatives;
- merely describes the category;
- contradicts the image;
- is irrelevant.

## Question 5: Does Bangla evidence behave differently from English evidence?

BANGLAVERSE already shows cross-language differences in VQA and captioning. The unresolved issue is whether confidence calibration changes with:

- Bangla evidence;
- English evidence;
- dialectal evidence;
- bilingual evidence;
- translated evidence.

## Question 6: Does selective prediction preserve cultural coverage?

A system may reduce risk by abstaining disproportionately on:

- minority dialects;
- regional foods;
- indigenous or less documented cultural practices;
- women and local personalities;
- politically sensitive entities.

This would be a central fairness and cultural-coverage question, not merely a performance issue.

# 9. Papers that absolutely need to be read in full

If time is limited, read these in this order:

1. [SIEVES](https://www.alphaxiv.org/abs/2604.25855) — closest direct methodological overlap.
2. [Look Again Before You Abstain](https://www.alphaxiv.org/abs/2606.16667) — strongest evidence-acquisition and risk-control pre-emption.
3. [Grounded or Guessing?](https://www.alphaxiv.org/abs/2605.10893) — closest visual-dependence confidence method.
4. [Confidence Estimation for Financial Vision-Language Models](https://www.alphaxiv.org/abs/2608.06532) — strongest deployment-oriented calibration and risk–coverage comparison.
5. [BANGLAVERSE](https://www.alphaxiv.org/abs/2603.21165) — essential domain and failure-analysis paper.
6. [TRAPSBench](https://www.alphaxiv.org/abs/2608.13167) — essential for answerability and representation–output gaps.
7. [ReCoVERR](https://aclanthology.org/2024.findings-acl.767/) — evidence acquisition before abstention.
8. [HallusionBench](https://openaccess.thecvf.com/content/CVPR2024/html/Guan_HallusionBench_An_Advanced_Diagnostic_Suite_for_Entangled_Language_Hallucination_and_Visual_Illusion_in_Large_Vision-Language_Models_CVPR2024_paper.html) — controlled visual-illusion versus language-hallucination diagnosis.
9. [THRONE](https://openaccess.thecvf.com/content/CVPR2024/html/Kaul_Throne_An_Object-Based_Hallucination_Benchmark_for_the_Free-form_Generations_of_Large_Vision-Language_Models_CVPR2024_paper.html) — object-level free-form hallucination.
10. [POPE](https://aclanthology.org/2023.emnlp-main.20/) — foundational object-hallucination evaluation.

# 10. Conservative assessment of whether the field remains plausible

A **Proposal 3 research field remains plausible**, but not under the broad novelty statement currently used.

The field is strongest if framed as:

> **Cultural-shifted selective reliability of multimodal entity predictions: separating visual dependence, cultural knowledge support, and answer correctness in Bangla VLMs.**

The field is weak if framed as:

> A new combination of confidence, visual grounding, evidence, abstention, and risk–coverage.

That combination is already substantially represented in SIEVES, Look Again, BICR, ReCoVERR, and the financial-confidence study.

The defensible remaining contribution is narrower:

1. BANGLAVERSE establishes culturally difficult Bangla entity recognition failures.
2. Existing reliability studies do not evaluate whether those failures are calibrated.
3. Existing visual-grounding confidence methods do not test culturally unfamiliar entities.
4. Existing evidence-acquisition methods do not use external cultural evidence.
5. Existing Bangla cultural benchmarks do not evaluate abstention or risk–coverage.
6. The interaction between language, culture, retrieval evidence, visual dependence, and selective risk remains unresolved.

So the conservative conclusion is:

> **The general methodological idea is partially pre-empted, but the Bangla cultural reliability question remains open. The scientific field is plausible only if its contribution is the diagnosis of how cultural unfamiliarity changes calibration and selective risk—not the mere assembly of existing confidence signals into a pipeline.**
