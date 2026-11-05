## D:/Thesis/Evidence-Grounded Selective Prediction for Reliable Bangla Cultural Vision-Language Models.docx
**Thesis Proposal**

**Evidence-Grounded Selective Prediction for Reliable Bangla Cultural Vision-Language Models**

**1. Executive summary**

Vision-language models can answer questions about images, but they may confidently provide incorrect answers when the image contains culturally specific Bengali/Bangladeshi entities such as food, clothing, artifacts, landmarks, personalities, and traditional activities.

This thesis will investigate whether a Bangla-capable open-weight vision-language model can estimate when its answer is unreliable. The proposed system will combine three signals:

1. the model’s answer confidence;
2. whether the answer depends on the visual input;
3. whether external cultural evidence supports the predicted entity.

The model will either answer or abstain when evidence is insufficient. The central evaluation will measure whether abstention reduces the error rate among accepted answers while retaining useful coverage.

The thesis is not intended to develop a new foundation model. It is a controlled empirical study of **evidence-grounded uncertainty calibration and selective prediction for Bangla cultural visual question answering**.

**2. Why this topic is valid**

The topic is valid for four reasons.

**2.1 Bangla cultural VLM errors are real**

[BANGLAVERSE](file:///C%3A%5Cabs%5C2603.21165%3FchatId%3D01a0be14-1205-7d2e-9824-3c477fe3099d) evaluates VLMs on Bengali culture using 1,152 manually curated images across nine domains and reports approximately 32,247 multilingual and dialectal evaluation artifacts. Its manual analysis identifies local entity and artifact misrecognition as 42.6% of observed failures.

Error Analysis

This establishes a concrete problem: current VLMs can describe a Bengali image superficially while failing to identify the relevant local entity.

**2.2 Accuracy alone is insufficient**

A VLM may be correct for the wrong reason, or incorrect while expressing high confidence. Therefore, the important question is not only:

How accurate is the model?

It is also:

Which answers should a user trust?

Recent work distinguishes calibration from ordinary accuracy and studies risk–coverage trade-offs for multimodal models. [SIEVES](file:///C%3A%5Cabs%5C2604.25855%3FchatId%3D01a0be14-1205-7d2e-9824-3c477fe3099d) uses visual evidence quality to improve selective prediction on challenging VQA tasks.

Selective Prediction

**2.3 Visual evidence can reveal unsupported answers**

A model may produce the same answer even when its image is replaced by a blank or mismatched image. This suggests that the answer may come from language priors rather than visual evidence.

[Grounded or Guessing?](file:///C%3A%5Cabs%5C2605.10893%3FchatId%3D01a0be14-1205-7d2e-9824-3c477fe3099d) studies this type of visual grounding and confidence estimation. Similarly, [Confidence Estimation for Financial Vision-Language Models](file:///C%3A%5Cabs%5C2608.06532%3FchatId%3D01a0be14-1205-7d2e-9824-3c477fe3099d) reports that grounding-aware confidence can identify fluent answers that do not genuinely use the visual input.

Grounding-Aware Confidence

**2.4 Selective prediction is more useful than forced answering**

[Look Again Before You Abstain](file:///C%3A%5Cabs%5C2606.16667%3FchatId%3D01a0be14-1205-7d2e-9824-3c477fe3099d) studies a three-way decision: answer, abstain, or acquire more evidence. It shows that naive evidence acquisition can invalidate calibration guarantees, while recalibration on the deployed evidence pipeline restores valid risk control.

Evidence Acquisition

The proposed thesis will implement a simpler BSc-level version: answer when confidence is high and abstain when confidence is low.

**3. Research gap and novelty**

The general topics of multimodal calibration, abstention, visual grounding, and hallucination detection are already active research areas. Therefore, the thesis should not claim that uncertainty calibration in MLLMs is entirely new.

The remaining gap is more specific:

Existing work has not systematically evaluated evidence-grounded selective prediction for local Bengali cultural entity recognition in open-weight VLMs.

The proposed novelty lies in the combination of:

* Bangla cultural visual question answering;
* local-entity recognition;
* visual-grounding confidence;
* external cultural evidence;
* selective prediction;
* risk–coverage evaluation;
* fine-grained failure analysis.

The contribution will primarily be **empirical and diagnostic**, not algorithmic.

**Defensible novelty statement**

This thesis presents a controlled empirical study of whether visual-grounding and cultural-evidence signals improve uncertainty calibration and selective prediction for local-entity recognition in open Bangla vision-language models.

**Claims not made**

The thesis will not claim that it:

* develops a new VLM;
* solves hallucination generally;
* introduces a universal uncertainty estimator;
* provides a guaranteed safety mechanism for all MLLMs;
* represents Bengali culture completely;
* develops a fundamentally new multimodal retrieval algorithm.

**4. Research problem**

A Bangla VLM may fail in several different ways:

* it may not perceive the relevant object;
* it may recognize the object but assign the wrong local identity;
* it may know the entity but misunderstand its cultural significance;
* it may ignore relevant external evidence;
* it may generate unsupported claims;
* it may answer confidently despite insufficient evidence.

This thesis will study whether a confidence system can identify unreliable cases before they are presented to a user.

**5. Main research question**

**Can evidence-grounded uncertainty estimation identify unreliable local-entity predictions in Bangla VLMs and improve the risk–coverage trade-off through selective prediction?**

**6. Research questions**

**RQ1**

How accurately can an open-weight Bangla-capable VLM identify Bengali/Bangladeshi cultural entities in image-grounded questions?

**RQ2**

Which confidence signals best distinguish correct and incorrect local-entity predictions?

**RQ3**

Does combining answer confidence, visual-grounding confidence, and cultural-evidence support improve calibration?

**RQ4**

Can selective prediction reduce local-entity hallucination among accepted answers without causing excessive abstention?

**7. Hypotheses**

**H1**

Verbal self-reported confidence will be poorly calibrated and will remain high for some incorrect local-entity predictions.

**H2**

Visual-grounding confidence based on image perturbations will better identify visually unsupported answers than verbal confidence alone.

**H3**

A combined confidence score using answer stability, visual dependence, and evidence support will outperform individual confidence signals.

**H4**

Selective prediction will reduce the local-entity error rate among accepted answers, although stricter error limits will reduce coverage.

**8. Proposed methodology**

**8.1 Dataset**

The primary evaluation source will be a filtered subset of [BANGLAVERSE](file:///C%3A%5Cabs%5C2603.21165%3FchatId%3D01a0be14-1205-7d2e-9824-3c477fe3099d). The benchmark contains manually curated Bengali cultural images and VQA annotations across culture, food, history, media, personalities, politics, sports, nature, and national achievements.

Dataset Statistics

Recommended dataset size:

* 300–500 entity-focused image-question pairs;
* 6–8 cultural categories;
* 40–80 items per category;
* 50–100 additional development items;
* an optional 50–100 item challenge set using new images.

Recommended categories:

* Bengali food;
* traditional clothing;
* cultural artifacts;
* landmarks;
* public personalities;
* historical events;
* sports and media;
* traditional activities.

**8.2 Dataset annotation**

Each item should contain:

text

image\_id

image\_source

question\_bn

question\_en

gold\_entity

acceptable\_aliases

category

visual\_difficulty

knowledge\_dependence

gold\_evidence

source\_url

license

annotator\_notes

At least two Bangla-proficient annotators should verify:

* the gold entity;
* acceptable aliases;
* whether the entity is visually identifiable;
* whether external cultural knowledge is necessary;
* whether the image is ambiguous.

Disagreements should be resolved by an adjudicator.

**8.3 Model**

Use **Qwen2.5-VL-7B-Instruct** as the primary model.

It is recommended because it is:

* open-weight;
* relatively practical on an RTX 3090 or RTX 4090;
* compatible with quantized inference;
* capable of image-question answering;
* widely evaluated in recent multimodal research.

Use one optional secondary model only after the primary system is complete:

* Gemma 3 4B;
* InternVL3-8B;
* LLaVA-NeXT 7B.

**8.4 Confidence signals**

**C1: Verbal confidence**

Ask the model to produce:

text

Answer: ...

Confidence: 0–100

Explanation: ...

This is a baseline and should not be assumed reliable.

**C2: Sampling consistency**

Generate multiple answers under controlled sampling. The confidence score is the proportion of generations that produce the same entity.

This measures stability, but stability does not guarantee correctness.

**C3: Visual-grounding confidence**

Run the same question under:

* the original image;
* a blank image;
* a blurred image;
* a mismatched image.

If the predicted entity remains unchanged, the answer may rely on language priors rather than visual evidence.

**C4: Evidence-support confidence**

Retrieve or provide a cultural passage and determine whether it:

* supports the predicted entity;
* contradicts the prediction;
* is irrelevant;
* contains insufficient information.

This can initially be evaluated using rule-based matching and human verification rather than training a new evidence-verification model.

**C5: Combined confidence**

Combine the signals:

$$
C\_{\text{combined}} = w\_1C\_{\text{answer}} + w\_2C\_{\text{visual}} + w\_3C\_{\text{evidence}}
$$

The weights should be learned only on a calibration split. A simple logistic-regression model may be used to predict whether an answer is correct.

**9. Selective prediction**

The system will make one of two decisions:

* answer;
* abstain because evidence is insufficient.

For confidence threshold $\tau$:

$$
\text{Answer if } C\_{\text{combined}}\geq\tau
$$

Otherwise:

“I do not have sufficient visual or cultural evidence to answer confidently.”

The system should not be rewarded merely for abstaining on everything. It must answer correctly when possible and abstain selectively.

**10. Experimental conditions**

| **Condition** | **Description** | **Purpose** |
| --- | --- | --- |
| B0 | VLM answers every question | Ordinary accuracy baseline |
| B1 | Verbal confidence | Self-report baseline |
| B2 | Sampling consistency | Stability baseline |
| B3 | Visual perturbation confidence | Tests visual dependence |
| B4 | Evidence-support confidence | Tests cultural evidence |
| B5 | Combined confidence | Main proposed system |
| B6 | Oracle human labels | Diagnostic upper bound |

The main comparison is:

**B1/B2/B3/B4 versus B5 under matched risk levels.**

**11. Evaluation metrics**

**Primary metrics**

* Local-entity accuracy;
* Local-entity error rate;
* unsupported-entity rate;
* Expected Calibration Error;
* Brier score;
* risk–coverage curve;
* coverage at 5%, 10%, and 20% error;
* Area Under the Risk–Coverage Curve.

**Secondary metrics**

* AUROC for correct versus incorrect answers;
* average precision;
* false-abstention rate;
* evidence-supported answer rate;
* answer-language compliance;
* performance by cultural category;
* performance on visually clear versus visually ambiguous images.

**Key deployment metric**

How many questions can the system answer while keeping the error rate among accepted answers below a selected threshold?

**12. Error taxonomy**

For each incorrect or abstained answer, assign the earliest failure category:

* **E1 — Visual perception failure:** relevant visual features were not perceived.
* **E2 — Local entity identification failure:** the object or person was seen but assigned the wrong identity.
* **E3 — Cultural knowledge failure:** the entity was recognized but its cultural meaning or association was wrong.
* **E4 — Evidence failure:** relevant evidence was unavailable or not retrieved.
* **E5 — Evidence integration failure:** relevant evidence was available but ignored or misinterpreted.
* **E6 — Unsupported generation:** the model generated a claim unsupported by the image or evidence.

Not every incorrect answer should be called a hallucination. “Hallucination” should mainly refer to confident unsupported claims. The multimodal hallucination literature similarly distinguishes nonexistent objects from inaccurate descriptions and relationships.

Hallucination Categories

**13. Statistical analysis**

Use:

* 95% bootstrap confidence intervals;
* paired bootstrap comparisons between confidence systems;
* McNemar’s test for paired correctness differences;
* risk–coverage curves;
* AUROC confidence intervals;
* Wilson intervals for error rates;
* Cohen’s $\kappa$ or Krippendorff’s $\alpha$ for human annotations.

Use image-level or question-level resampling carefully. If multiple questions use the same image, bootstrap by image rather than treating every question as fully independent.

**14. Resources required**

**Hardware**

* RTX 3090 or RTX 4090 with 24 GB VRAM;
* 32–64 GB RAM;
* 100 GB or more storage;
* Google Colab as backup.

**Software**

* Python;
* PyTorch;
* Hugging Face Transformers;
* Accelerate;
* BitsAndBytes;
* PEFT, optional;
* Sentence Transformers;
* FAISS;
* NumPy;
* pandas;
* scikit-learn;
* SciPy;
* matplotlib/seaborn;
* Git/GitHub;
* Weights & Biases or MLflow.

**Optional retrieval resources**

If external evidence is included:

* 5,000–10,000 licensed Bangla cultural passages;
* multilingual-e5-base or multilingual-e5-large;
* BGE-M3 as an alternative;
* FAISS vector index;
* verified source metadata.

**15. Hardware and time feasibility**

The project is **feasible with careful scope**.

A quantized 7B VLM should be practical on a single RTX 3090/4090. The main computational cost will be repeated inference for:

* original images;
* blank images;
* blurred images;
* mismatched images;
* sampling consistency;
* evidence-supported conditions.

To remain feasible:

* use 300–500 test questions;
* use one primary VLM;
* use deterministic decoding for the main experiment;
* limit sampling to a smaller subset;
* avoid training a new VLM or multimodal retriever;
* avoid large-scale reinforcement learning.

**16. Six-month work plan**

| **Month** | **Deliverable** |
| --- | --- |
| 1 | Literature review, final protocol, model setup |
| 2 | Dataset filtering, annotation, calibration/test split |
| 3 | Baseline inference and verbal/consistency confidence |
| 4 | Visual-grounding and evidence-support experiments |
| 5 | Confidence fusion, selective prediction, statistics |
| 6 | Error analysis, thesis writing, code and documentation |

**17. Required papers and resources**

**Bengali cultural VLM evaluation**

* [BANGLAVERSE — Bengali Cultural VLM Benchmark](file:///C%3A%5Cabs%5C2603.21165%3FchatId%3D01a0be14-1205-7d2e-9824-3c477fe3099d)

**Selective prediction and visual evidence**

* [SIEVES: Selective Prediction Generalizes through Visual Evidence Scoring](file:///C%3A%5Cabs%5C2604.25855%3FchatId%3D01a0be14-1205-7d2e-9824-3c477fe3099d)
* [Look Again Before You Abstain: Budgeted Conformal Evidence Acquisition](file:///C%3A%5Cabs%5C2606.16667%3FchatId%3D01a0be14-1205-7d2e-9824-3c477fe3099d)
* [TRAPSBench: Vision-Language Models Encode but Fail to Express Epistemic Restraint](file:///C%3A%5Cabs%5C2608.13167%3FchatId%3D01a0be14-1205-7d2e-9824-3c477fe3099d)
* [Selective “Selective Prediction”: Reducing Unnecessary Abstention in Vision-Language Reasoning](https://aclanthology.org/2024.findings-acl.767/)

**Visual grounding and confidence**

* [Grounded or Guessing? LVLM Confidence Estimation via Blind-Image Contrastive Ranking](file:///C%3A%5Cabs%5C2605.10893%3FchatId%3D01a0be14-1205-7d2e-9824-3c477fe3099d)
* [Confidence Estimation for Financial Vision-Language Models](file:///C%3A%5Cabs%5C2608.06532%3FchatId%3D01a0be14-1205-7d2e-9824-3c477fe3099d)
* [Reference-free Hallucination Detection for Large Vision-Language Models](https://aclanthology.org/2024.findings-emnlp.285/)

**Hallucination and reliability**

* [Detecting and Preventing Hallucinations in Large Vision Language Models](file:///C%3A%5Cabs%5C2308.06394%3FchatId%3D01a0be14-1205-7d2e-9824-3c477fe3099d)
* [HallusionBench](https://openaccess.thecvf.com/content/CVPR2024/html/Guan_HallusionBench_An_Advanced_Diagnostic_Suite_for_Entangled_Language_Hallucination_and_Visual_Illusion_in_Large_Vision-Language_Models_CVPR_2024_paper.html)
* [THRONE: An Object-Based Hallucination Benchmark](https://openaccess.thecvf.com/content/CVPR2024/html/Kaul_Throne_An_Object-Based_Hallucination_Benchmark_for_the_Free-form_Generations_of_Large_Vision-Language_Models_CVPR_2024_paper.html)
* [POPE: Evaluating Object Hallucination in Large Vision-Language Models](https://aclanthology.org/2023.emnlp-main.20/)

**Models**

* Qwen2.5-VL technical report
* Gemma 3 technical report
* InternVL3 technical report
* [LLaVA-NeXT](https://github.com/LLaVA-VL/LLaVA-NeXT)

Check the license and current availability of every dataset and model before using them in the thesis.

**18. Expected contribution**

The thesis will provide:

1. A Bangla-specific evaluation of uncertainty calibration in an open VLM.
2. A comparison of verbal, consistency-based, visual-grounding, and evidence-based confidence.
3. A selective prediction system for reducing accepted local-entity errors.
4. Risk–coverage analysis for culturally grounded VLM answering.
5. A human-validated taxonomy of perception, cultural knowledge, evidence, and generation failures.
6. Reproducible code, prompts, evaluation scripts, and metadata.

**19. Limitations**

The results will be limited to:

* selected Bengali cultural categories;
* one primary VLM;
* a finite evaluation set;
* the chosen confidence signals;
* the quality of available annotations and evidence.

The study will not establish that all Bangla VLMs are calibrated or that the method generalizes to every cultural domain.

**20. Final recommendation**

**Decision: Proceed after scope control**

This is a valid and timely BSc thesis topic because it combines:

* an established Bangla-specific reliability problem;
* a current research area in multimodal uncertainty;
* a measurable selective-prediction objective;
* realistic computation on one RTX 3090/4090;
* a clear empirical contribution.

The final topic should be stated as:

**Evidence-Grounded Selective Prediction for Reliable Bangla Cultural Vision-Language Models**

The project should focus on **one model, one curated Bangla cultural evaluation set, three or four confidence signals, and risk–coverage analysis**. Do not expand it into a new VLM, a new multimodal retriever, or a general theory of uncertainty.

**Short analysis for your supervisor**

**Why valid:** Bengali VLMs exhibit substantial local-entity and cultural recognition failures, while recent research shows that multimodal models are often overconfident and may not genuinely use visual evidence.

**Why novel:** Existing studies separately address Bengali cultural evaluation, visual hallucination, calibration, and selective prediction. This thesis combines them in the underexplored setting of **local Bengali cultural entities** and evaluates whether evidence-grounded confidence can support selective answering.

**What the thesis contributes:** Not a new foundation model, but a reproducible empirical framework showing which confidence signals identify unreliable Bangla VLM answers and how much error can be avoided through calibrated abstention.

**Final scope:** One open-weight VLM, 300–500 Bangla cultural questions, visual-grounding tests, cultural evidence support, confidence fusion, risk–coverage evaluation, and human error analysis.