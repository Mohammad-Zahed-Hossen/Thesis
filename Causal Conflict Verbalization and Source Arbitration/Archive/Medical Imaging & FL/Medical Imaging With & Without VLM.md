# Chat Transcript: Medical Resolution No VLM

## User

(File attachment: text/plain)

Medical Imaging without VLM

## Aurelle

> **Planning a research audit**
> 
> I need to conduct a large audit focused on the 2024-2026 timeframe. I think I should research and identify relevant papers and official datasets. Maybe I can use a tool to discover one call and look for official dataset pages simultaneously. I want to gather citations and links to ensure I'm sourcing accurately. My goal is to explore broad aspects of medical imaging calibration, considering the robustness shift in selective public datasets.

> **Searched Papers**
> 2 searches · 40 papers · Learning to Adapt and Calibrate: Score Distribution Alignment for Few-Shot Uncertainty Prediction in Medical VLMs · Prevalence calibration as shortcut mitigation · MVC-Bench: Benchmarking Calibration of Medical Vision-Language Models · What Do Medical Vision-Language Models Learn in Radiology? Transfer, Alignment, and Source-Proxy Leakage Under Distribution Shift · ControlledShifts: Towards Standardizing Robustness Evaluation in Trajectory Prediction Under Distribution Shifts · Reliable Financial Named Entity Recognition Under Domain Shift: Confidence Estimation and Selective Prediction · Learning the Pareto Frontier of Predictive Models under Distribution Shift · Subtype Robustness Is Not Just Accuracy: Calibration Under Unseen Subtype Shift · Foundation Models for Medical Imaging: Status, Challenges, and Directions · Neural Radiance Fields in Medical Imaging: A Survey · On The Robustness of Foundational 3D Medical Image Segmentation Models Against Imprecise Visual Prompts · Automatic Medical Report Generation: Methods and Applications · MedM-VL: What Makes a Good Medical LVLM? · Medical Visual Question Answering: A Survey · On the limits of cross-domain generalization in automated X-ray
>   prediction · Continual Learning in Medical Imaging: A Survey and Practical Analysis

> **Searching for datasets**
> 
> I'm looking for serious papers and datasets related to a future date in September 2026. Since the user is asking for an audit, I want to ensure I provide reliable, bounded evidence without overclaiming. To gather this information, I’ll utilize web search to find known papers and official pages. I think I can query multiple resources in one go, which might be efficient for getting the dataset details I need.

> **Searched Papers and Sources**
> 7 searches · 120 papers · 10 sources · NIH Chest X-ray dataset | Cloud Healthcare API | Google Cloud Documentation · ISIC Challenge Datasets · Copycats: the many lives of a publicly available medical imaging dataset · The HAM10000 dataset, a large collection of multi-source ... · CheXpert: Chest X-rays | Center for Artificial Intelligence in Medicine & Imaging · alkzar90/NIH-Chest-X-ray-dataset · Datasets at Hugging Face · VinDr-CXR: An open dataset of chest X-rays with radiologist’s annotations - PMC · GitHub - m-aryayi/Medical-Imaging-Datasets: Publicly available medical imaging datasets for research and analysis. · GitHub · Prevalence calibration as shortcut mitigation · Learning to Adapt and Calibrate: Score Distribution Alignment for Few-Shot Uncertainty Prediction in Medical VLMs · MVC-Bench: Benchmarking Calibration of Medical Vision-Language Models · Towards Autonomous and Auditable Medical Imaging Model Development · What Do Medical Vision-Language Models Learn in Radiology? Transfer, Alignment, and Source-Proxy Leakage Under Distribution Shift · Reliable Financial Named Entity Recognition Under Domain Shift: Confidence Estimation and Selective Prediction · ConfTriage: A Calibration-Aware LLM Triage Framework for Pulmonary Nodule Malignancy with Selective Specialist Deferral · Calibrated Selective Prediction Using Deep Ensembles for ROI-Based Thyroid Nodule Ultrasound Classification Under Dataset Shift: A Retrospective Evaluation · Medical-Checklist: Assessing the Comprehension of Medical Images by Multimodal Models · Evaluating and Understanding Model Editing for Medical Vision Language Models · Benchmarking the Robustness of Foundation Models for Mammography under Domain Shift · MedFM-Robust: Benchmarking Robustness of Medical Foundation Models · A Dataset for Dynamic Human Preferences for Vision Language Models · A Large Scale Benchmark for Test Time Adaptation Methods in Medical Image Segmentation · Rethinking Benchmarks for Differentially Private Image Classification · CHILD: Human-in-the-Loop OOD Detection for Safe Clinical Deployment · When Adaptation Hurts: Connecting Representational Drift to OOD Failures in MedSAM Fine-Tuning · PROTON: Prototype-Based Test-Time Online OOD Detection for Medical VLMs · Unified Multi-Layer Subspace Modeling for Cross-Domain OOD Detection · TTL: Test-time Textual Learning for OOD Detection with Pretrained Vision-Language Models · Layer Selection in VLMs for Zero-Shot OOD Detection via Multi-Resolution Entropy Estimation · Confident but Unreliable: A Behavioral Safety Audit of Vision-Language Models on Brain MRI · TCLA: Training-Free Class-wise Logit Adaptation for Medical Vision-Language Models · BioMedVR: Confusion-Aware Mixture-of-Prompt Experts for Biomedical Visual Reprogramming · MedObvious: Exposing the Medical Moravec's Paradox in VLMs via Clinical Triage · Harnessing Image Question Dependence for Better VLM Test-time Reinforcement Learning · Memory-Supported Synergistic Adaptation for Training-Free Test-Time Medical Image Segmentation · Evaluating the Diagnostic Robustness of Vision-Language Models Under Visual and Textual Perturbations · Probabilistic Robustness in Medical Image Classification · An Empirical Analysis of Continual Learning for Heterogeneous Medical Visual Question Answering

> **Considering data sources**
> 
> I need to find around 10 serious and specific recent titles, but it seems like my current knowledge isn't enough. Maybe I should look up known titles through a search query. As I frame this, I realize that evidence is limited, and an audit may terminate. So, I need to gather a detailed dataset for the audit and read official pages from sources like ISIC, CheXpert, NIH, MedMNIST, BraTS, and VinDr.

> **Read 5 webpages**
> challenge.isic-archive.com · medmnist.com · aimi.stanford.edu · nihcc.app.box.com · physionet.org

# Medical Imaging Without VLMs: Adversarial Thesis Audit

## Executive verdict

**Medical imaging without VLMs does contain one defensible undergraduate research direction, but it does not currently beat your held VLM thesis on conceptual novelty.**

The strongest surviving direction is not another classifier or robustness method. It is a **leakage-resistant audit of calibration and selective prediction under acquisition/source shift in skin-lesion imaging**, using public ISIC datasets with patient and source metadata.

> **Provisional verdict: RESERVE, with a narrowly defined pilot.**  
> **MEDICAL IMAGING WITHOUT VLM DOES NOT CURRENTLY BEAT THE HELD VLM DIRECTION.**

That conclusion is based on three findings:

1. Generic medical-image classification is saturated and usually produces weak thesis contributions.
2. Robustness, calibration, test-time adaptation, shortcut learning, and uncertainty remain scientifically important, but recent work is rapidly occupying the obvious questions.
3. Public datasets make a rigorous audit feasible, but they do not provide a clean substitute for real prospective clinical validation.

The viable contribution is therefore a **controlled benchmark and failure analysis**, not a new architecture.

## 1. Candidate space after the feasibility gates

### Immediately rejected directions

| Direction | Decision | Reason |
|---|---|---|
| Chest-X-ray calibration using MIMIC-CXR | Reject for this thesis | [VERIFIED] MIMIC-CXR requires credentialing, CITI training, and a signed data-use agreement; it is not directly downloadable for an uncredentialed user. [MIMIC-CXR](https://physionet.org/content/mimic-cxr/2.1.0/) |
| Chest-X-ray work depending on CheXpert labels or reports | Reserve only | [VERIFIED] CheXpert is publicly described and downloadable through Stanford’s portal, but its access is mediated by Stanford terms and should be tested before committing. It contains 224,316 radiographs from 65,240 patients. [CheXpert](https://aimi.stanford.edu/datasets/chexpert-chest-x-rays) |
| Large-scale medical foundation-model pretraining | Reject | It violates the compute constraint and is unnecessary for the scientific questions under consideration. |
| Clinical deployment or prospective diagnostic evaluation | Reject | It requires clinical access, specialist evaluation, and likely institutional approval. |
| New segmentation architecture on BraTS | Reject as a default thesis | The benchmark is heavily occupied, computationally more demanding, and a small architectural change is unlikely to constitute a meaningful contribution. |
| Generic “CNN versus Transformer” classification | Reject | It tests an engineering comparison rather than a scientifically sharp failure mode. |
| Federated learning | Reject for the primary thesis | It introduces a separate systems problem—client partitioning, communication, privacy, and aggregation—without solving the core validity problem. |
| Explainability without a measurable failure hypothesis | Reject | Saliency-map visualizations alone do not establish that a model uses clinically meaningful evidence. |

### Saturated problems

These are poor thesis choices unless attached to a very specific audit:

- model architecture comparisons;
- binary lesion classification on HAM10000;
- ordinary pneumonia classification;
- “improve accuracy using attention”;
- generic data augmentation;
- single-dataset segmentation improvement;
- saliency-map comparisons;
- post-hoc calibration on one random train/test split.

### Moderately occupied problems

These remain scientifically useful but require careful positioning:

- calibration under cross-dataset shift;
- selective prediction and abstention;
- shortcut learning from acquisition artifacts;
- corruption robustness;
- lightweight test-time adaptation;
- subgroup calibration by sex, age, or anatomical site.

### Potentially open enough for an undergraduate thesis

The best opportunity is:

> **How much do patient-level splitting, acquisition-source splitting, and random image splitting change conclusions about calibration and selective prediction in skin-lesion classifiers?**

This is a benchmark-audit question. It is not glamorous, but it is falsifiable, reproducible, computationally manageable, and valuable even if every proposed intervention fails.

## 2. Recent literature autopsy

The recent literature shows that the area is active rather than empty. It also shows why simply proposing “robust calibration for medical images” would be too broad.

| Paper | Year | Problem | Dataset | Model | Method | Main metric | Code | Data | Compute | Limitation | Remaining gap |
|---|---:|---|---|---|---|---|---|---|---|---|---|
| [Prevalence calibration as shortcut mitigation](https://www.alphaxiv.org/abs/2609.07922) | 2026 | Shortcut learning and prevalence shift | [UNKNOWN] | Classifier | Prevalence-aware calibration | Calibration / shortcut metrics [UNKNOWN] | [UNKNOWN] | [UNKNOWN] | [UNKNOWN] | Very recent; full experimental details require inspection | Whether conclusions hold under patient- and source-level splits |
| [Probabilistic Robustness in Medical Image Classification](https://www.alphaxiv.org/abs/2607.03797) | 2026 | Reliability under perturbation and shift | [UNKNOWN] | Image classifier | Probabilistic robustness evaluation | [UNKNOWN] | [UNKNOWN] | [UNKNOWN] | [UNKNOWN] | Exact datasets and code not verified here | Whether selective risk remains valid when shift is source-dependent |
| [Useful nonrobust features are ubiquitous in biomedical images](https://www.alphaxiv.org/abs/2604.22579) | 2026 | Non-robust but predictive features | [UNKNOWN] | Deep networks | Perturbation-based feature analysis | Robustness / accuracy [UNKNOWN] | [UNKNOWN] | [UNKNOWN] | [UNKNOWN] | Strong conceptual overlap with shortcut investigations | Whether calibration identifies these failures better than accuracy |
| [Mitigating Shortcut Learning via Feature Disentanglement in Medical Imaging: A Benchmark Study](https://www.alphaxiv.org/abs/2602.18502) | 2026 | Shortcut learning | [UNKNOWN] | Deep image models | Feature disentanglement | Accuracy and shortcut metrics [UNKNOWN] | [UNKNOWN] | [UNKNOWN] | [UNKNOWN] | Benchmark scope and exact split design need verification | Whether interventions preserve calibration and abstention quality |
| [Leveraging Pathology Co-occurrence for Test-Time Adaptation in Chest X-Ray Diagnosis](https://www.alphaxiv.org/abs/2607.03715) | 2026 | Domain shift in chest X-ray diagnosis | Chest X-ray data [dataset unspecified in retrieved record] | Multi-label classifier | Pathology co-occurrence for TTA | Out-of-domain diagnostic performance [UNKNOWN] | [UNKNOWN] | [UNKNOWN] | [UNKNOWN] | Likely depends on chest-X-ray infrastructure not guaranteed to be accessible | Whether adaptation improves reliability without source-domain damage |
| [When Adaptation Hurts: Connecting Representational Drift to OOD Failures in MedSAM Fine-Tuning](https://www.alphaxiv.org/abs/2608.21300) | 2026 | Adaptation failure in segmentation | [UNKNOWN] | MedSAM | Analysis of representational drift | OOD segmentation performance [UNKNOWN] | [UNKNOWN] | [UNKNOWN] | [UNKNOWN] | Foundation-model dependency and possible GPU burden | Whether lightweight adaptation can be audited on smaller public data |
| [Memory-Supported Synergistic Adaptation for Training-Free Test-Time Medical Image Segmentation](https://www.alphaxiv.org/abs/2607.17693) | 2026 | Training-free TTA | [UNKNOWN] | Segmentation foundation model | Memory-supported adaptation | Segmentation metrics [UNKNOWN] | [UNKNOWN] | [UNKNOWN] | [UNKNOWN] | The method may be too large for the minimum hardware | Whether calibration or selective segmentation is improved |
| [Calibrated Selective Prediction Using Deep Ensembles for ROI-Based Thyroid Nodule Ultrasound Classification Under Dataset Shift](https://www.alphaxiv.org/abs/2607.12075) | 2026 | Calibration and referral under shift | Thyroid ultrasound [UNKNOWN] | Deep ensembles | Selective prediction | Calibration, coverage, selective risk [UNKNOWN] | [UNKNOWN] | [UNKNOWN] | [UNKNOWN] | The retrospective dataset and access conditions are not verified | Whether cheaper single-model methods produce the same conclusions |
| [Audited Conformal Prediction for Classification under Unknown Distribution Shift](https://www.alphaxiv.org/abs/2606.14909) | 2026 | Uncertainty under unknown shift | [UNKNOWN] | Classifier | Audited conformal prediction | Coverage / risk [UNKNOWN] | [UNKNOWN] | [UNKNOWN] | [UNKNOWN] | Not established here as a medical-imaging paper | Whether it applies cleanly to image-source shift |
| [Subtype Robustness Is Not Just Accuracy: Calibration Under Unseen Subtype Shift](https://www.alphaxiv.org/abs/2608.00928) | 2026 | Calibration under unseen subtypes | [UNKNOWN] | Classifier | Subtype-shift evaluation | Accuracy and calibration [UNKNOWN] | [UNKNOWN] | [UNKNOWN] | [UNKNOWN] | Exact medical datasets and implementation need checking | Whether acquisition source and patient identity produce similar failures |

### What this table actually establishes

[VERIFIED] Recent work explicitly studies calibration, shortcut learning, probabilistic robustness, selective prediction, and test-time adaptation rather than only accuracy.

[INFERRED] The broad claims “medical models are poorly calibrated under shift” and “test-time adaptation can improve robustness” are no longer sufficient thesis contributions.

[UNKNOWN] I have not verified the exact code, licenses, dataset splits, or compute requirements of every paper above from its full text and repository. They must not be presented as reproducible baselines until checked.

The strongest gap is not “nobody has studied calibration.” It is:

> **Existing work does not automatically establish that calibration and selective-prediction conclusions survive leakage-resistant patient/source splits, duplicate removal, prevalence changes, and multiple acquisition domains on a fully accessible dataset.**

That is a narrower and more defensible claim.

## 3. Dataset audit

| Dataset | Modality | Images | Labels | License/access | Patient IDs | Leakage risk | Shift potential | Compute |
|---|---|---:|---|---|---|---|---|---|
| [ISIC 2019](https://challenge.isic-archive.com/data/) | Dermoscopy | 25,331 train; 8,238 test | Lesion diagnoses; metadata | [VERIFIED] Direct downloadable archive; CC-BY-NC | [VERIFIED] Metadata includes common lesion identifier in training data | High if lesion groups or sources are ignored | High: multiple contributing institutions and metadata | Low–moderate |
| [ISIC 2020](https://challenge.isic-archive.com/data/) | Dermoscopy / DICOM | 33,126 train; 10,982 test | Melanoma diagnosis; patient, lesion, sex, age, site | [VERIFIED] Direct files; CC-BY-NC | [VERIFIED] Patient ID, lesion ID, and duplicate list are supplied | High; official page lists 425 duplicate images | High: six contributing sources and clinical metadata | Moderate; JPEG subset is manageable |
| [SLICE-3D / ISIC 2024](https://challenge.isic-archive.com/data/) | Total-body photography lesion crops | 401,059 images; permissive subset 217,477 | Malignancy; patient and lesion metadata | [VERIFIED] Direct download; permissive subset is CC-BY | [VERIFIED] Common patient identifier supplied | Very high if image-level splitting is used | High: multiple institutions and acquisition context | Moderate–high; use a subset |
| [HAM10000](https://doi.org/10.1038/sdata.2018.161) | Dermoscopy | 10,015 | Seven lesion categories | [VERIFIED] Public dataset; source license must be preserved | [VERIFIED] Lesion/image grouping information exists in the ISIC distribution | High because it is multi-source and related lesions may recur | Moderate–high | Low–moderate |
| [MedMNIST](https://medmnist.com/) | Multiple biomedical modalities | [VERIFIED] Approximately 708,000 2D and 10,000 3D images across 18 datasets | Binary, multiclass, multilabel, ordinal | [VERIFIED] Official API; generally CC-BY 4.0, with DermaMNIST CC-BY-NC 4.0 | [UNKNOWN] Patient-level identifiers are not generally exposed through the standardized interface | Unknown to high depending on source subset | Limited for realistic acquisition shift; useful for controlled corruption | Very low |
| [NIH ChestX-ray14](https://nihcc.app.box.com/v/ChestXray-NIHCC) | Chest X-ray | [VERIFIED] 112,120 images from 30,805 patients | 14 text-mined disease labels | [VERIFIED] Official NIH download exists; license terms need checking before redistribution | [VERIFIED] Patient identifiers are available in metadata | High; labels are report-derived and multiple images per patient exist | Moderate; mostly one institution | Moderate |
| [CheXpert](https://aimi.stanford.edu/datasets/chexpert-chest-x-rays) | Chest X-ray | [VERIFIED] 224,316 images from 65,240 patients | Five competition labels plus uncertainty labels | [VERIFIED] Stanford download page exists; terms must be checked | [VERIFIED] Patient count and patient-based structure are documented | High | Low for single-site evaluation; cross-dataset shift possible | Moderate–high |
| [MIMIC-CXR](https://physionet.org/content/mimic-cxr/2.1.0/) | Chest X-ray | [VERIFIED] 377,110 images from 227,835 studies | Reports and derived labels | [VERIFIED] Credentialed access, CITI training, and DUA required | [VERIFIED] Subject and study identifiers are provided | High but controllable | High for cross-institution studies | High storage and preprocessing burden |
| BraTS | MRI brain tumors | [UNKNOWN] Version-dependent | Tumor segmentation labels | [UNKNOWN] Official access and current license need independent verification | [UNKNOWN] Must verify for selected release | Potentially high if slices rather than subjects are split | High across scanners/protocols, but benchmark definitions vary | High for 3D segmentation |

### Dataset conclusion

The best dataset for this thesis is **ISIC 2020**, potentially combined with **ISIC 2019** or the permissive **SLICE-3D** subset.

Why:

- [VERIFIED] official files are directly downloadable;
- [VERIFIED] patient, lesion, source-related, demographic, and anatomical metadata are available;
- [VERIFIED] the official page explicitly provides a duplicate-image list for ISIC 2020;
- [VERIFIED] the data are large enough for repeated evaluation;
- the images can be handled with pretrained 2D CNNs on a T4;
- the dataset naturally supports patient-level and source-aware audits.

The important limitation is that **ISIC source/domain labels and patient structure must be inspected carefully before the experiment is finalized**. If the exact acquisition source cannot be reconstructed reliably from the released metadata, the candidate should be downgraded to a corruption-and-prevalence audit rather than called a domain-generalization study.

## 4. Serious thesis candidates

### Candidate 1 — Patient/source leakage-resistant calibration audit

#### Exact question

> **When a skin-lesion classifier is evaluated using patient-level and acquisition-source-aware splits instead of random image splits, how do its calibration, selective risk, and subgroup performance change, and which lightweight recalibration method remains reliable under the resulting shift?**

#### Competing hypotheses

**H0:** Random, patient-level, and source-aware splits produce statistically comparable calibration and selective-prediction conclusions after controlling for class prevalence.

**H1:** Random image splits produce systematically over-optimistic calibration and selective-risk estimates, while source-aware evaluation reveals degradation that is only partially repaired by recalibration.

#### Intervention

Compare:

- no calibration;
- temperature scaling;
- vector or classwise scaling;
- isotonic regression only if the validation size supports it;
- optionally a small deep ensemble as an upper-cost control.

The contribution is not claiming that temperature scaling is novel. The contribution is measuring **whether apparently reliable predictions remain reliable under leakage-resistant shift**.

#### Controls

- ImageNet-pretrained ResNet-18 or EfficientNet-B0;
- identical preprocessing and training budget;
- fixed patient-level validation;
- random image split as a deliberately unsafe baseline;
- duplicate removal;
- source-stratified and source-held-out evaluation;
- class-balanced and natural-prevalence evaluation;
- three random seeds;
- bootstrap confidence intervals.

#### Metrics

- AUROC;
- AUPRC;
- sensitivity and specificity at a predeclared operating point;
- ECE;
- adaptive ECE;
- Brier score;
- NLL;
- risk-coverage curve;
- selective risk at fixed coverage;
- subgroup calibration by source, sex, age band, and anatomical site where sample sizes permit.

#### Negative-result value

If H1 fails, the study still establishes that the evaluated dataset and interventions are more stable than expected under the tested shifts. That is useful only if the splits and metadata audit are rigorous. A null result would not justify claiming universal robustness.

**Status: PROCEED TO PILOT.**

This is the strongest candidate.

---

### Candidate 2 — Can abstention detect acquisition shift?

#### Exact question

> **Can a low-cost abstention rule identify source-shifted or unreliable skin-lesion cases more effectively than ordinary softmax confidence while preserving diagnostic sensitivity on retained cases?**

#### H0

Softmax confidence and uncertainty scores do not differ materially in their ability to identify errors or shifted samples.

#### H1

A calibrated uncertainty or ensemble-disagreement score improves error detection and risk-coverage performance, especially on source-held-out data.

#### Intervention

Compare:

- maximum softmax probability;
- entropy;
- temperature-scaled confidence;
- Monte Carlo dropout;
- a three-member deep ensemble;
- optional conformal prediction as a separate method, not as a replacement for risk-coverage evaluation.

#### Controls

- same classifier and splits as Candidate 1;
- no access to labels during test-time abstention;
- predeclare the coverage levels;
- evaluate separately on in-domain, source-shifted, and corruption-shifted cases.

#### Metrics

- risk-coverage area;
- selective risk at 50%, 75%, and 90% coverage;
- error-detection AUROC;
- OOD AUROC only where a defensible OOD set exists;
- sensitivity among retained cases;
- calibration of the retained predictions.

#### Negative-result value

A negative result would show that commonly used confidence scores do not provide meaningful triage under the chosen shifts. That is a valuable warning against interpreting confidence as a referral mechanism.

**Status: RESERVE.**

It is scientifically good, but the novelty is weaker because selective prediction and ensemble uncertainty are already well established. It should probably be combined with Candidate 1 rather than run independently.

---

### Candidate 3 — Robustness interventions versus calibration preservation

#### Exact question

> **Which lightweight image-corruption interventions improve out-of-domain diagnostic performance without worsening calibration on clean skin-lesion images?**

#### H0

Corruption augmentation or preprocessing improves robustness without materially affecting clean-domain calibration.

#### H1

Robustness interventions trade off clean-domain calibration, sensitivity, or specificity for gains under corruption.

#### Intervention

Compare:

- clean training;
- severity-controlled brightness/contrast/compression/blur augmentation;
- AugMix or RandAugment;
- histogram normalization;
- test-time augmentation;
- temperature scaling after each intervention.

#### Controls

- synthetic corruption generated only after the train/validation/test split;
- corruption severity fixed before model selection;
- no corruption statistics computed from the test set;
- a second real dataset if possible, such as ISIC 2019 versus ISIC 2020.

#### Metrics

- AUROC/AUPRC;
- sensitivity and specificity;
- ECE, Brier, and NLL;
- risk-coverage;
- clean-versus-corrupted calibration gap.

#### Negative-result value

A negative result would identify interventions that improve robustness while making probabilities less trustworthy. That directly matters to reliable AI.

**Status: RESERVE.**

The question is feasible but synthetic corruptions can become an artificial benchmark. It should not be the main thesis unless a real cross-source shift is included.

---

### Candidate 4 — Lightweight test-time adaptation

#### Exact question

> **Can entropy-minimization or batch-statistics test-time adaptation improve source-held-out skin-lesion performance without causing prediction collapse or source-domain calibration damage?**

#### H0

Test-time adaptation improves shifted-domain performance without materially damaging source-domain behavior.

#### H1

Adaptation gains are unstable and can reduce calibration, increase error concentration, or damage the source domain.

#### Intervention

- source model without adaptation;
- batch normalization adaptation;
- entropy minimization;
- test-time augmentation;
- optional pseudo-label adaptation.

#### Controls

- no target labels during adaptation;
- fixed stream order and shuffled stream;
- single-image versus batch adaptation;
- source-domain replay set;
- reset model state between domain conditions.

#### Metrics

- AUROC/AUPRC;
- ECE, Brier, NLL;
- risk-coverage;
- prediction entropy;
- performance after adaptation and after resetting;
- source-domain degradation.

#### Negative-result value

A failure would be useful because it would demonstrate that adaptation can improve accuracy while reducing reliability.

**Status: REJECT as the primary thesis; RESERVE as an extension.**

Recent work already occupies TTA, and a clean medical-imaging result would require a carefully justified shift protocol. This is too easy to turn into a collection of unstable engineering experiments.

---

### Candidate 5 — Shortcut sensitivity audit

#### Exact question

> **Can a skin-lesion classifier maintain calibration and selective performance when source-correlated nuisance cues—background, borders, compression, color, and metadata-associated acquisition patterns—are systematically altered or removed?**

#### H0

Removing or perturbing nuisance cues changes little after adequate training.

#### H1

The classifier loses performance or becomes miscalibrated, indicating reliance on acquisition-related shortcuts.

#### Intervention

- lesion crop versus full image;
- border/background masking;
- controlled color normalization;
- JPEG recompression;
- hair and ruler perturbations;
- source-balanced sampling;
- metadata-blind model versus metadata-augmented model.

#### Controls

- perturbations applied independently to train, validation, and test;
- no use of labels or source information in the image transformation;
- patient-level split;
- compare several backbones;
- retain a clean untouched test set.

#### Metrics

- AUROC/AUPRC;
- sensitivity and specificity;
- calibration gap under perturbation;
- error-detection AUROC;
- attribution stability only as a secondary diagnostic.

#### Negative-result value

A null result would provide evidence that the chosen nuisance transformations are not decisive for that model/data combination.

**Status: RESERVE.**

The question is meaningful, but “shortcut learning” claims are easy to overstate. A performance drop after masking does not by itself prove that the model relied on clinically invalid features.

## 5. Leakage audit for the leading candidate

The leading candidate fails unless the following are explicitly handled.

### Patient leakage

[VERIFIED] ISIC 2020 supplies patient identifiers and lesion identifiers. All images from the same patient must be assigned to one partition.

**Required rule:** split by patient before any augmentation, oversampling, or calibration fitting.

### Duplicate and near-duplicate images

[VERIFIED] ISIC 2020 provides a duplicate-image list containing 425 duplicate images.

Additional checks should include:

- perceptual hashing;
- image embeddings with nearest-neighbor inspection;
- exact duplicate hashes;
- lesion-ID grouping;
- checking whether the same lesion appears in multiple challenge releases.

### Augmentation leakage

Augmentations must be created only after partitioning. No augmented copy of a training image may enter validation or test data.

### Acquisition-source leakage

The model must not receive source, camera, site, or metadata features unless the experiment explicitly studies metadata use.

Source-balanced sampling should be reported separately from source-held-out evaluation. Balancing a training set does not establish domain generalization.

### Metadata leakage

Age, sex, anatomical site, lesion ID, and acquisition-related fields must not enter the image model in the primary experiment.

If metadata are used for subgroup analysis, they must be used only after predictions are generated.

### Class imbalance

Report both:

- natural-prevalence performance;
- balanced or reweighted performance.

AUPRC, sensitivity, specificity, Brier score, and NLL are especially sensitive to prevalence and threshold selection.

### Preprocessing leakage

Mean/std normalization, color statistics, calibration parameters, thresholds, and augmentation policies must be fitted using training data or a designated validation set only.

### Test-set reuse

The test set must not be used to choose:

- calibration method;
- threshold;
- corruption severity;
- source grouping;
- backbone;
- number of ensemble members.

If the study needs multiple design decisions, use nested validation or a locked final test set.

## 6. Compute audit

For Candidate 1:

| Component | Estimate |
|---|---|
| Backbone | ResNet-18, EfficientNet-B0, or similar |
| Parameters | Approximately 10–15 million for ResNet-18-class models |
| Input | 224–256 px JPEG |
| Minimum VRAM | Approximately 4–8 GB, depending on batch size |
| T4 requirement | Sufficient |
| V100/A100 | Not required |
| Training time | Roughly 20–60 minutes per run after data preparation; [INFERRED] depends heavily on storage and augmentation |
| Number of runs | Approximately 15–30 for three seeds, split conditions, and calibration methods |
| Colab sessions | Approximately 4–10 organized sessions |
| Inference | Fast enough for full-test evaluation on a T4 |
| Storage issue | ISIC 2020 JPEG is manageable; DICOM and SLICE-3D full-scale use are unnecessary |

The project is feasible on Colab Pro if the team avoids:

- full-resolution DICOM processing;
- large vision transformers;
- large ensembles;
- repeated hyperparameter searches;
- training on all 401,059 SLICE-3D images.

A clean implementation should begin with a 5–10% pilot subset and only scale after the split logic and leakage tests pass.

## 7. Closest-work autopsy

### Closest work to Candidate 1

1. [Calibrated Selective Prediction Using Deep Ensembles for ROI-Based Thyroid Nodule Ultrasound Classification Under Dataset Shift](https://www.alphaxiv.org/abs/2607.12075)  
   It directly studies calibration, deep ensembles, selective prediction, and shift. The remaining gap is whether a cheaper, leakage-resistant image-only benchmark reaches the same conclusion across patient/source splits.

2. [Probabilistic Robustness in Medical Image Classification](https://www.alphaxiv.org/abs/2607.03797)  
   It appears to frame robustness probabilistically rather than through accuracy alone. The remaining gap is a transparent public-data audit where split construction, duplicate handling, and prevalence are central experimental variables.

3. [Mitigating Shortcut Learning via Feature Disentanglement in Medical Imaging: A Benchmark Study](https://www.alphaxiv.org/abs/2602.18502)  
   It studies interventions against shortcuts. The remaining gap is whether these interventions preserve calibration and selective risk under source shift.

4. [Prevalence calibration as shortcut mitigation](https://www.alphaxiv.org/abs/2609.07922)  
   It connects prevalence calibration with shortcut mitigation. The remaining gap is the distinction between prevalence shift, patient leakage, and acquisition-source shift in a conventional image-only setting.

5. [Subtype Robustness Is Not Just Accuracy: Calibration Under Unseen Subtype Shift](https://www.alphaxiv.org/abs/2608.00928)  
   It reinforces the idea that accuracy alone is inadequate under unseen variation. The remaining gap is whether the same phenomenon appears when the “subtype” is operationalized as acquisition source or patient-disjoint domain.

### What these papers already establish

[INFERRED] They establish that calibration, uncertainty, and robustness are legitimate research questions—not merely deployment afterthoughts.

They do **not automatically establish**:

- that random image splits are adequate;
- that their public data are credential-free;
- that a particular intervention generalizes across datasets;
- that performance gains correspond to better selective decisions;
- that source shift has been separated from prevalence shift;
- that the conclusions survive duplicate and near-duplicate removal.

### Novelty classification

Candidate 1 is best described as:

> **A diagnostic extension and benchmark audit with a possible methodological component if the team develops a statistically principled split/calibration protocol.**

It is not a genuinely novel learning algorithm. That is acceptable for a thesis if the experimental question is sharp and the audit is stronger than existing evaluations.

The main danger is that a 2025–2026 paper may already perform nearly the same audit. Therefore, the 60–90 minute verification task at the end is essential before approval.

## 8. Comparison with the held VLM candidate

| Criterion | Medical imaging candidate | Held VLM candidate |
|---|---|---|
| Question clarity | Clear if limited to split construction, calibration, and selective risk | Very clear and causally framed around conflict verbalization and source arbitration |
| Literature crowding | Calibration, shortcut learning, and TTA are moderately to heavily occupied | More distinctive intersection of causal probing, multimodal conflict, and explanation behavior |
| Dataset access | Strong with ISIC 2019/2020; weak for MIMIC-CXR | Depends on the chosen VLM and image-text benchmark, but public evaluation sets are likely available |
| Baseline reproducibility | Strong with pretrained CNNs and official ISIC downloads | Potentially weaker because model versions, prompts, APIs, and stochasticity matter |
| Compute | Low to moderate; T4 is sufficient | Can be low if using APIs, but API cost and version drift become concerns |
| Leakage risk | High but concrete and auditable | Prompt contamination, benchmark leakage, memorization, and modality-order effects are possible |
| Evaluation validity | Strong for a benchmark audit; weak as a clinical claim | Strong if source arbitration is operationalized causally rather than inferred from prose |
| Novelty | Moderate; likely diagnostic extension | Higher conceptual novelty |
| Negative-result value | Good: can show which evaluation practices change conclusions | Very good: failure to change arbitration can distinguish causal influence from rationalization |
| Engineering burden | Manageable but data audit is meticulous | Manageable, but requires careful prompt/control design and API experiment management |
| Thesis scope | Easy to keep within a 3-person undergraduate thesis | Also manageable, but causal claims require more conceptual discipline |

### What would change my mind?

Medical imaging would become competitive if the pilot demonstrates that:

1. commonly used public evaluations produce materially different calibration or abstention conclusions under patient/source-aware splitting;
2. the effect is replicated across at least two independent dataset releases;
3. existing recent work does not already perform that audit;
4. the result changes how robustness or clinical reliability should be measured.

Without those findings, the medical-imaging project is a competent benchmark study but not stronger than the held VLM question.

## 9. Final classification

| Candidate | Classification | Reason |
|---|---|---|
| Patient/source leakage-resistant calibration audit | **PROCEED TO PILOT** | Public data, reproducible CNN baseline, manageable compute, precise question, meaningful negative-result value |
| Abstention under acquisition shift | **RESERVE** | Strong extension of Candidate 1; standalone novelty is weaker |
| Robustness interventions versus calibration preservation | **RESERVE** | Feasible, but synthetic corruption can make the result artificial |
| Lightweight test-time adaptation | **REJECT as primary** | Crowded, unstable, and easy to turn into incremental engineering |
| Shortcut sensitivity audit | **RESERVE** | Valuable, but causal claims about shortcuts require unusually careful controls |

## Bottom Line

1. **Best surviving question:** When patient-level and acquisition-source-aware splits replace random image splits, how do calibration and selective prediction change for skin-lesion classifiers?

2. **Closest competing paper:** [Calibrated Selective Prediction Using Deep Ensembles for ROI-Based Thyroid Nodule Ultrasound Classification Under Dataset Shift](https://www.alphaxiv.org/abs/2607.12075).

3. **Exact remaining gap:** A credential-free, leakage-resistant audit separating patient leakage, acquisition-source shift, prevalence shift, calibration failure, and selective-risk failure in public skin-lesion data.

4. **Dataset:** [ISIC 2020](https://challenge.isic-archive.com/data/), with [ISIC 2019](https://challenge.isic-archive.com/data/) as a replication dataset if metadata alignment is feasible.

5. **Baseline:** ImageNet-pretrained ResNet-18, patient-level split, temperature scaling, classwise calibration, and a deliberately unsafe random-image split as a comparison.

6. **Minimum experiment:** Three random seeds; random-image versus patient-level versus source-aware splits; clean versus source-held-out evaluation; AUROC, AUPRC, sensitivity, specificity, ECE, Brier, NLL, and risk-coverage.

7. **Main risk:** The source metadata may not support a clean independent-domain split, or a recent 2025–2026 paper may already perform essentially the same audit.

8. **Negative-result value:** If calibration and abstention remain stable across leakage-resistant shifts, that is evidence against a common assumption that random image splits necessarily overstate reliability. If they fail, the thesis identifies a concrete evaluation hazard.

9. **Verdict:** **PROCEED TO PILOT, but keep the VLM thesis as the stronger primary option until the pilot demonstrates a real evaluation reversal.**

10. **One 60–90 minute verification task:** Download the official ISIC 2020 JPEG archive and metadata, confirm that patient ID, lesion ID, source-related fields, labels, and the 425-image duplicate list are usable; then run perceptual-hash duplicate detection and produce counts for random-image, patient-level, and source-stratified splits. If source grouping cannot be reconstructed without guesswork, reject the domain-shift version and retain only the patient-leakage/calibration audit.

## User

(File attachment: text/plain)

Medical Imaging with VLM

## Aurelle

> **Researching VLM Papers**
> 
> I need to focus on our research efforts. I should search for existing papers on VLM (visual language models) to see if any are already available. My goal is to gather around ten relevant studies or sources. It’s essential to be broad in my approach, considering different models and datasets that might help in our investigation. Let’s discover what we can find on the web about this topic!

> **Searched Papers**
> 5 searches · 105 papers · SAVOR: Self-Aware Visual Grounding via Confidence-Calibrated Reinforcement Learning for Multimodal Hallucination Mitigation · Option-Aware Retrieval and Task-Specific VLM Adaptation for Medical VQA · Separating Capability from Confidence: Grounded Dual-State Calibration for GRPO-Trained Medical Vision-Language Models · Uncertainty-Aware Decision Making in Multimodal Large Language Models · Two-Token Features and Small-Large Ensembles for VLM Hallucination Detection · Learning to Adapt and Calibrate: Score Distribution Alignment for Few-Shot Uncertainty Prediction in Medical VLMs · Where to Look Matters: Learning Influential Views for VLM-based 3D Visual Grounding · MVC-Bench: Benchmarking Calibration of Medical Vision-Language Models · A Pathway to General-Purpose Scientific AI: Multimodal Comprehension of Scientific Images · The Path to Self-Evolving Clinical Systems: Scaling Medical Agents from Assistance to Autonomy · An Empirical Analysis of Continual Learning for Heterogeneous Medical Visual Question Answering · Aloe-Vision: Robust Vision-Language Models for Healthcare · MMBU: A Massive Multi-modal Biomedical Understanding Benchmark to Probe the Perception Capabilities of Vision-Language Models · Why Does Grounding Hurt Medical VQA? Benchmarking, Diagnosis, and Fine-Tuning of Vision-Language Models · Vision Language Models: A Survey of 26K Papers · LoRA-TSD: Tangent-Space Spectral Descent for LoRA via Muon-Style Updates · Rank-Efficient LoRA via Joint Tangent-Space Optimization under Isotropic Curvature · RW-LoRA: Communication-Efficient Decentralized LoRA Fine-Tuning via Random Walks · LiST: Local-Simplex Test-Time LoRA Fusion · FedPA-LoRA: Product-Aligned Framework for Mitigating Aggregation and Initialization Errors in Heterogeneous Federated LoRA · ST-LoRA: Single Trajectory LoRA Ensemble for Uncertainty Aware Agricultural Segmentation · \k{appa}-LoRA: Condition Numbers Reveal Which LoRA Matrices Worth Updating · CARE-LoRA: Compressed Activation REconstruction for Memory-Efficient LoRA · MedProb: Probing Internal Representations of Vision-Language Models for Medical Question Answering · Harnessing Image Question Dependence for Better VLM Test-time Reinforcement Learning · CARE: Confidence-Aware Reasoning for Reliable Medical VQA · Counterfactual Anatomy-guided Spatial-Temporal Decoding for Annotation-Free Hallucination Mitigation in Medical VLMs · Rethinking Correctness for Uncertainty Estimation in Clinical Prediction with Vision-Language Models · What Do Medical Vision-Language Models Learn in Radiology? Transfer, Alignment, and Source-Proxy Leakage Under Distribution Shift · EVADE: Evidence-Verified Agentic Diagnosis with Escape · Confident but Unreliable: A Behavioral Safety Audit of Vision-Language Models on Brain MRI · Beyond the Leaderboard: Design Lessons for Trustworthy Multimodal VQA · Detecting Clinical Hallucinations in LVLMs via Counterfactual Visual Grounding Uncertainty

> **Evaluating research questions**
> 
> I'm noting that today's date is September 20, 2026, and I need to audit answers, but I haven't read all the papers. I can clearly highlight areas of uncertainty, especially regarding the strongest candidate possibly addressing conflicts. There's a focus on medical adaptation under visual degradation, which might align with calibration issues. I should avoid making overclaims and stick to verified resources for datasets. Since user queries are extensive, I'll aim for a moderately detailed response.

> **Organizing paper citations**
> 
> I'm considering that I can provide a partial answer that includes labels for clarity. I need to make sure to cite paper links instead of using PDFs since I haven't read them fully. Every important claim should be backed up with evidence. It’s key to ensure everything is properly attributed to maintain credibility and ensure the user can find original sources easily. Let’s keep this structured and clear!

# Medical Imaging with VLMs: Adversarial Thesis Audit

## Executive verdict

**The medical-VLM reliability space is already substantially occupied.** Recent work now directly targets calibration, confidence, hallucination, visual grounding, selective triage, and distribution shift. The strongest undergraduate-feasible question is therefore not “are medical VLMs unreliable?” but:

> **Does a medical VLM’s verbalized confidence track image evidence separately from answer correctness when visual evidence is progressively degraded or removed?**

This is narrower than a generic calibration study and technically distinct from simply measuring whether the answer is correct.

However:

> **MEDICAL VLM RESEARCH DOES NOT CURRENTLY BEAT THE HELD RQ.**

Your held question—whether explicit conflict verbalization causally changes source arbitration or merely rationalizes an existing modality preference—has a sharper causal structure and a more distinctive scientific claim. A medical-VLM project becomes competitive only if it demonstrates that confidence is sensitive to **visual evidence sufficiency**, not merely to answer difficulty or language priors.

## 1. What recent work already occupies

The literature is no longer missing basic reliability studies.

[VERIFIED] Recent search results include work explicitly on medical-VLM calibration, confidence estimation, selective triage, hallucination stages, visual grounding, distribution shift, and source-proxy leakage.

[UNKNOWN] I have not inspected the full PDF, official repository, or data card for every recent result below. Therefore, code, exact datasets, compute, and claimed limitations must not be treated as verified until the corresponding primary sources are opened.

| Paper | Year | Medical task | Model | Dataset | Reliability problem | Method | Metrics | Code | Data | Limitation | Remaining gap | Status |
|---|---:|---|---|---|---|---|---|---|---|---|---|---|
| [MVC-Bench: Benchmarking Calibration of Medical Vision-Language Models](https://www.alphaxiv.org/abs/2608.27004) | 2026 | Medical VQA / evaluation | Medical VLMs | [UNKNOWN] | Calibration | Calibration benchmark | [UNKNOWN] | [UNKNOWN] | [UNKNOWN] | Benchmark scope and model coverage require full-text inspection | Whether confidence reflects visual evidence rather than answer familiarity | Occupied |
| [Confidence Calibration for Multimodal LLMs: An Empirical Study through Medical VQA](https://www.alphaxiv.org/abs/2606.19950) | 2026 | Medical VQA | MLLMs | Medical VQA data [UNKNOWN] | Confidence misalignment | Empirical confidence analysis | Accuracy/calibration [UNKNOWN] | [UNKNOWN] | [UNKNOWN] | Exact elicitation protocol and model versions require verification | Confidence conditioned on controlled visual evidence removal | Occupied |
| [Calibrated Triage, Not Autonomy: Confidence Estimation for Medical Vision-Language Models](https://www.alphaxiv.org/abs/2606.15910) | 2026 | Chest X-ray/pathology question answering | Medical VLMs | [UNKNOWN] | Overconfident answers and language-prior reliance | Confidence estimation for triage | [UNKNOWN] | [UNKNOWN] | [UNKNOWN] | May already overlap strongly with abstention and evidence-sufficiency questions | Separating correctness confidence from evidence sufficiency under paired interventions | Occupied |
| [Confident but Unreliable: A Behavioral Safety Audit of Vision-Language Models on Brain MRI](https://www.alphaxiv.org/abs/2608.02790) | 2026 | Brain MRI understanding | VLMs, including medical specialists | Brain MRI [UNKNOWN] | Overconfidence | Behavioral audit | [UNKNOWN] | [UNKNOWN] | [UNKNOWN] | Exact scoring and MRI dataset access need verification | Whether confidence changes monotonically with controlled visual degradation | Occupied |
| [ClinHallu: A Benchmark for Diagnosing Stage-Wise Hallucinations in Medical MLLM Reasoning](https://www.alphaxiv.org/abs/2606.14697) | 2026 | Medical reasoning/VQA | Medical MLLMs | [UNKNOWN] | Hallucination during reasoning | Stage-wise hallucination benchmark | [UNKNOWN] | [UNKNOWN] | [UNKNOWN] | Benchmark may depend on synthetic or evaluator-generated annotations | Whether hallucination is predicted by image-evidence uncertainty before the final answer | Occupied |
| [Detecting Clinical Hallucinations in LVLMs via Counterfactual Visual Grounding Uncertainty](https://www.alphaxiv.org/abs/2606.28520) | 2026 | Clinical image understanding | LVLMs | [UNKNOWN] | Unsupported claims | Counterfactual visual grounding uncertainty | Hallucination detection [UNKNOWN] | [UNKNOWN] | [UNKNOWN] | Exact counterfactual construction and evaluator reliability require inspection | Whether the method generalizes across modalities and open-ended answers | Occupied |
| [Attention Without Grounding: Causal Evaluation of Visual Explanations in Medical VLMs](https://www.alphaxiv.org/abs/2607.18577) | 2026 | Chest X-ray explanation | Medical VLMs | Chest X-ray [UNKNOWN] | Explanations not causally grounded | Causal explanation evaluation | [UNKNOWN] | [UNKNOWN] | [UNKNOWN] | May focus on saliency rather than confidence or abstention | Whether grounding quality predicts calibration and selective risk | Partially occupied |
| [What Do Medical Vision-Language Models Learn in Radiology? Transfer, Alignment, and Source-Proxy Leakage Under Distribution Shift](https://www.alphaxiv.org/abs/2608.25251) | 2026 | Radiology transfer | Medical VLMs | Radiology data [UNKNOWN] | Source-proxy leakage and domain shift | Transfer/alignment audit | [UNKNOWN] | [UNKNOWN] | [UNKNOWN] | Exact source split and model-training provenance require verification | Confidence and hallucination under the same shift | Occupied |
| [Medical Context Distorts Decisions in Clinical Vision Language Models](https://www.alphaxiv.org/abs/2605.17436) | 2026 | Clinical multimodal decision-making | Clinical VLMs | [UNKNOWN] | Textual context distorting visual decisions | Context intervention | Decision accuracy [UNKNOWN] | [UNKNOWN] | [UNKNOWN] | Very close to multimodal conflict and source arbitration | Whether explicit conflict verbalization causally changes the final arbitration | Occupied and directly relevant |
| [CARE: Confidence-Aware Reasoning for Reliable Medical VQA](https://www.alphaxiv.org/abs/2608.10964) | 2026 | Medical VQA | Medical MLLMs | [UNKNOWN] | Unreliable reasoning/confidence | Confidence-aware reasoning or reinforcement fine-tuning | [UNKNOWN] | [UNKNOWN] | [UNKNOWN] | Training cost and evaluator dependence require verification | Whether confidence improves because of visual evidence or merely learned response style | Occupied |
| [From Reasoning to Pixels: Grounded Medical Multimodal LLMs for VQA and Segmentation](https://www.alphaxiv.org/abs/2608.26856) | 2026 | VQA and segmentation | Medical MLLMs | [UNKNOWN] | Poor spatial grounding | Joint reasoning and pixel grounding | VQA/segmentation metrics [UNKNOWN] | [UNKNOWN] | [UNKNOWN] | Likely requires fine-tuning and segmentation annotations | Whether pixel grounding improves calibration or only localization | Occupied |
| [EVADE: Evidence-Verified Agentic Diagnosis with Escape](https://www.alphaxiv.org/abs/2608.18833) | 2026 | Medical diagnosis | Medical VLMs | [UNKNOWN] | Overconfidence and failure to abstain | Evidence verification plus escape/abstention | [UNKNOWN] | [UNKNOWN] | [UNKNOWN] | Agentic pipeline may be too complex for a controlled undergraduate comparison | A minimal evidence-sufficiency intervention without an agent loop | Occupied |
| [Separating Capability from Confidence: Grounded Dual-State Calibration for GRPO-Trained Medical Vision-Language Models](https://www.alphaxiv.org/abs/2609.06419) | 2026 | Medical VQA/reasoning | GRPO-trained medical VLMs | [UNKNOWN] | Confidence conflating correctness and evidence | Dual-state calibration | [UNKNOWN] | [UNKNOWN] | [UNKNOWN] | Likely training-heavy and too recent for independent reproduction | A training-free diagnostic test of the same distinction | Occupied |
| [Mitigating Class-Tail Undercoverage in Medical Vision-Language Models under Clinical Shift](https://www.alphaxiv.org/abs/2607.28696) | 2026 | Clinical prediction | Medical VLMs | [UNKNOWN] | Class-conditional undercoverage | Shift-aware coverage method | Coverage [UNKNOWN] | [UNKNOWN] | [UNKNOWN] | Likely requires structured labels and shift metadata | Evidence-level uncertainty for individual cases | Partially occupied |

### Literature conclusion

The obvious questions are occupied:

- “Are medical VLMs calibrated?” — occupied.
- “Do medical VLMs hallucinate?” — occupied.
- “Can a medical VLM abstain?” — occupied.
- “Are explanations grounded?” — occupied.
- “Do medical VLMs fail under domain shift?” — occupied.
- “Does text influence medical image decisions?” — occupied.

The more defensible remaining question is the intersection:

> **Can confidence distinguish “I am likely correct” from “the image contains enough evidence to justify an answer”?**

Those are not identical. A model may answer correctly using a dataset prior, label prevalence, or textual cue while lacking sufficient image evidence.

## 2. Dataset audit

| Dataset | Modality | Public? | Access | License | Size | Labels | VQA? | Patient IDs | Leakage risk |
|---|---|---|---|---|---:|---|---|---|---|
| [ISIC 2019](https://challenge.isic-archive.com/data/) | Dermoscopy | [VERIFIED] Yes | Direct archive download | CC-BY-NC | [VERIFIED] 25,331 training and 8,238 test images | Diagnosis, metadata | No | [VERIFIED] Lesion/group identifiers are supplied | High if image-level splits are used |
| [ISIC 2020](https://challenge.isic-archive.com/data/) | Dermoscopy/DICOM | [VERIFIED] Yes | Direct JPEG/DICOM download | CC-BY-NC | [VERIFIED] 33,126 training and 10,982 test images | Melanoma, patient/lesion metadata | No | [VERIFIED] Patient and lesion IDs | High; official duplicate list includes 425 duplicate images |
| [SLICE-3D / ISIC 2024](https://challenge.isic-archive.com/data/) | Total-body photography crops | [VERIFIED] Yes | Direct download; permissive subset available | CC-BY-NC and CC-BY for permissive subset | [VERIFIED] 401,059 images, or 217,477 in permissive subset | Malignancy and metadata | No | [VERIFIED] Common patient identifier | Very high |
| [HAM10000](https://doi.org/10.1038/sdata.2018.161) | Dermoscopy | [VERIFIED] Publicly available through its published distribution | Download path must be checked for the exact version | Source-specific terms | [VERIFIED] 10,015 images | Seven lesion categories | No | Lesion grouping available through associated distributions | High |
| [MedMNIST](https://medmnist.com/) | X-ray, OCT, ultrasound, CT, microscopy and others | [VERIFIED] Yes | Official Python API | [VERIFIED] Mostly CC-BY 4.0; DermaMNIST is CC-BY-NC 4.0 | [VERIFIED] About 708,000 2D and 10,000 3D images | Binary, multiclass, multilabel, ordinal | No | [UNKNOWN] Standardized interface does not generally expose full patient identifiers | Unknown; unsuitable for strong patient-level claims |
| NIH ChestX-ray14 | Chest X-ray | [VERIFIED] Download site exists | NIH/Box archive | Terms require checking | [VERIFIED] 112,120 images from 30,805 patients | Fourteen text-mined labels | No | [VERIFIED] Patient identifiers in metadata | High; weak report-derived labels |
| CheXpert | Chest X-ray | [VERIFIED] Stanford dataset page exists | Stanford download portal | Access terms must be checked | [VERIFIED] 224,316 images from 65,240 patients | Five diseases plus uncertainty labels | No | [VERIFIED] Patient structure is documented | High; single-site and label uncertainty issues |
| MIMIC-CXR | Chest X-ray plus reports | [VERIFIED] Public research resource but not openly downloadable | Credentialing, CITI training, DUA | PhysioNet Credentialed Health Data License | [VERIFIED] 377,110 images from 227,835 studies | Reports and derived labels | Multimodal source, but not a ready-made VQA dataset | [VERIFIED] Subject and study identifiers | High but controllable |
| VQA-RAD | Radiology images and questions | [UNKNOWN] Public status must be checked against the official source | [UNKNOWN] | [UNKNOWN] | [UNKNOWN] | VQA answers | Yes | [UNKNOWN] | Potential patient/image duplication |
| SLAKE | Radiology VQA | [UNKNOWN] Public status must be checked | [UNKNOWN] | [UNKNOWN] | [UNKNOWN] | VQA plus semantic information | Yes | [UNKNOWN] | Potential question-template and image leakage |
| PathVQA | Pathology images and questions | [UNKNOWN] Public status must be checked | [UNKNOWN] | [UNKNOWN] | [UNKNOWN] | VQA answers | Yes | [UNKNOWN] | Caption/template leakage and duplicate-source risk |
| PMC-VQA | Biomedical figures/images and questions | [UNKNOWN] Public status must be checked | [UNKNOWN] | [UNKNOWN] | [UNKNOWN] | VQA answers | Yes | [UNKNOWN] | Text and figure-caption leakage |

### Dataset decision

For a trustworthy medical-VLM thesis, the best dataset is not automatically the largest VQA dataset.

The strongest practical options are:

1. **A closed-set VQA benchmark with image-level paired interventions**, if its download and license are confirmed.
2. **ISIC or chest-X-ray data converted into controlled question-answer tasks**, but only if the questions are generated from existing labels and the experiment is explicitly framed as a controlled diagnostic benchmark rather than natural medical VQA.
3. **MIMIC-CXR only if credentialing is feasible**, which contradicts your current assumption that access should be immediate and credential-free.

A major validity problem is that many medical VQA datasets contain:

- repetitive question templates;
- answers predictable from the question;
- captions or reports that leak the label;
- multiple questions per image;
- unclear patient-level splitting;
- weak or non-expert answer scoring.

Therefore, a thesis should not claim clinical reasoning competence from a high VQA exact-match score.

## 3. Model audit

### Models that are plausible for evaluation

| Model family | Likely use | Training required? | Colab feasibility | Main concern |
|---|---|---:|---|---|
| [BiomedCLIP](https://huggingface.co/microsoft/BiomedCLIP-PubMedBERT_256-vit_base_patch16_224) | Image-text similarity, zero-shot classification, evidence probes | No for the pilot | Strong on T4 | It is primarily a contrastive encoder, not a free-form medical VQA assistant |
| [LLaVA-Med](https://github.com/haotian-liu/LLaVA) | Open medical image dialogue/VQA | Usually yes or heavy inference | Model-specific; likely T4 with quantization if weights are accessible | Official repository and current checkpoint availability must be verified |
| Med-Flamingo | Few-shot medical VQA | No training for inference | Likely difficult on a T4 depending on checkpoint | Model/checkpoint accessibility and context length |
| [Qwen2-VL](https://github.com/QwenLM/Qwen2-VL) family | General VLM control baseline | No training for inference | Smaller variants may fit T4 quantized | Not inherently medical; clinical validity must be tested |
| Qwen-VL family | General VLM control baseline | No training for inference | Variant-dependent | Older checkpoints and license/version drift |
| Med-PaLM / Med-PaLM 2 | Medical VLM comparison | No local training | Not a practical open baseline | Access is not equivalent to reproducible open evaluation |
| Open medical MLLMs discovered in recent papers | Medical VQA | Usually optional inference, PEFT for adaptation | Model-dependent | Many papers do not guarantee stable public checkpoints |

[UNKNOWN] Exact parameter counts, VRAM requirements, checkpoint licenses, and inference throughput for the latest medical models must be verified from their current official model cards before committing to one.

### Recommended model design

Do not begin with PEFT.

Start with:

- one small open medical VLM, if its weights and license are usable;
- one general VLM control model;
- optionally BiomedCLIP as an image-text similarity control;
- 4-bit quantization if supported;
- frozen weights;
- repeated generation with fixed decoding settings.

PEFT should be added only if the research question is specifically about adaptation. Otherwise, it adds confounding variables:

- training data selection;
- prompt-format changes;
- checkpoint instability;
- calibration changes caused by optimization rather than by the proposed mechanism.

## 4. Candidate research questions

### Candidate A — Explicit contradiction detection and source arbitration

#### Research question

> **When visual and textual medical premises conflict, does explicitly requiring the model to identify the conflict change its final modality arbitration, or merely change the explanation attached to an unchanged decision?**

#### H0

Conflict verbalization changes the textual explanation but does not change the final answer distribution or modality preference.

#### H1

Conflict verbalization causes a measurable and reproducible change in the final answer distribution, with improved arbitration when one modality is controlled as unreliable.

#### Intervention

Compare:

1. image only;
2. text only;
3. image plus text;
4. image plus contradictory text;
5. image plus contradictory text with explicit conflict detection;
6. contradictory text with a placebo instruction unrelated to conflict.

#### Controls

- swap which modality contains the correct answer;
- use semantically matched contradiction prompts;
- randomize modality order;
- include neutral text;
- include contradictions that are visually resolvable and contradictions that are genuinely ambiguous;
- repeat stochastic generation;
- score final answers separately from explanations.

#### Metrics

- modality arbitration accuracy;
- answer flip rate;
- contradiction detection accuracy;
- confidence change;
- calibration;
- unsupported-claim rate.

#### Expected failure mode

The model detects contradiction linguistically but continues to follow the same modality, or produces a convincing explanation without changing its answer.

#### Negative result

This is still highly valuable: it would support the claim that conflict verbalization is primarily post-hoc rationalization rather than a causal intervention on multimodal evidence integration.

**Status: PROCEED TO PILOT.**

This is your held RQ and remains the strongest candidate.

---

### Candidate B — Calibration under progressive visual degradation

#### Research question

> **Does a medical VLM’s confidence decrease in proportion to the loss of diagnostic visual evidence when image quality is progressively degraded while the textual prompt and label remain fixed?**

#### H0

Confidence decreases monotonically and calibration remains approximately stable as visual evidence is degraded.

#### H1

Confidence remains high, decreases non-monotonically, or becomes dominated by language priors despite visual evidence loss.

#### Intervention

Apply pre-registered degradation levels:

- blur;
- downsampling;
- contrast reduction;
- masking of the lesion or relevant region;
- random image replacement;
- modality-preserving compression.

#### Controls

- text-only condition;
- clean-image condition;
- semantically irrelevant image condition;
- label-preserving geometric transformation;
- random degradation with matched image statistics.

#### Metrics

- confidence-versus-degradation slope;
- ECE;
- Brier score;
- NLL;
- correctness;
- risk-coverage;
- answer agreement between clean and degraded conditions.

#### Expected failure mode

The model retains high confidence after the diagnostic region is masked or the image is replaced, showing confidence that is not grounded in visual evidence.

#### Negative result

A monotonic confidence decline would be evidence that the evaluated model’s confidence is at least responsive to controlled image evidence loss. It would not prove clinical reliability.

**Status: PROCEED TO PILOT, but only after checking overlap with the recent calibration and brain-MRI audit papers.**

This is the strongest medical-specific alternative to the held RQ.

---

### Candidate C — Selective prediction for medical VQA

#### Research question

> **Can a medical VLM abstain on visually insufficient cases without simply abstaining on particular disease classes or long-tail answer types?**

#### H0

Abstention improves accuracy only by discarding difficult classes or low-frequency answers.

#### H1

A calibrated evidence-sufficiency score improves risk-coverage while retaining balanced coverage across classes.

#### Intervention

Compare:

- verbalized confidence;
- token probability where available;
- repeated-sampling agreement;
- image-text similarity;
- evidence-sufficiency prompt;
- abstention threshold.

#### Controls

- class-balanced evaluation;
- difficulty-matched non-abstention baseline;
- answer-length control;
- random abstention;
- confidence calibration on validation data only.

#### Metrics

- risk-coverage;
- selective accuracy;
- coverage by class;
- false-confidence rate;
- abstention parity across answer categories;
- calibration among retained cases.

#### Expected failure mode

The model abstains mainly on rare classes, ambiguous wording, or long answers rather than genuinely insufficient images.

#### Negative result

It would show that verbalized uncertainty is not a valid triage signal, even if overall risk-coverage improves.

**Status: RESERVE.**

The question is good, but recent work already directly addresses selective triage and confidence estimation.

---

### Candidate D — PEFT improves accuracy but damages calibration

#### Research question

> **Does LoRA adaptation improve medical-VQA accuracy while degrading calibration under a held-out image or question distribution?**

#### H0

LoRA improves or preserves both accuracy and calibration.

#### H1

LoRA improves accuracy but increases overconfidence or worsens risk-coverage under shift.

#### Intervention

Compare:

- frozen model;
- LoRA on language layers;
- LoRA on multimodal projection;
- LoRA on selected attention modules;
- full fine-tuning only if feasible.

#### Controls

- same training examples;
- same number of optimization steps;
- frozen-encoder adapter;
- held-out question templates;
- held-out image source;
- multiple LoRA ranks.

#### Metrics

- task accuracy;
- ECE;
- Brier score;
- NLL;
- risk-coverage;
- calibration under shift.

#### Expected failure mode

Adaptation memorizes answer templates or dataset priors, improving in-distribution exact match while increasing confidence on unsupported answers.

#### Negative result

It would establish that the chosen PEFT intervention does not introduce the expected accuracy-reliability trade-off.

**Status: REJECT as the primary thesis.**

It is a feasible engineering study, but unless the dataset and shift are unusually well controlled, the causal interpretation is weak.

---

### Candidate E — Evidence sufficiency independent of answer correctness

#### Research question

> **Can a medical VLM predict whether an image contains sufficient visual evidence for a question independently of whether its final answer happens to be correct?**

#### H0

Evidence-sufficiency judgments are equivalent to answer correctness and provide no additional information.

#### H1

Evidence sufficiency predicts when the answer is unjustified, including cases where the answer is accidentally correct.

#### Intervention

Construct paired cases:

- clear image and answerable question;
- degraded image and same question;
- irrelevant image and same question;
- ambiguous image with multiple plausible answers;
- image-text agreement;
- image-text conflict.

Ask separately for:

1. answer;
2. confidence in answer;
3. whether the image contains enough evidence;
4. what evidence is required.

#### Controls

- image-only and text-only conditions;
- random image-question pairing;
- human-authored sufficiency labels only if feasible;
- label-derived sufficiency rules for closed-set tasks;
- blinded scoring of evidence claims.

#### Metrics

- sufficiency classification accuracy;
- calibration of sufficiency probabilities;
- correlation with human or rule-based evidence labels;
- answer correctness conditional on predicted sufficiency;
- false-sufficiency rate;
- unsupported-evidence rate.

#### Expected failure mode

The model calls an image “sufficient” whenever its answer is likely, including cases where it is exploiting textual or prevalence priors.

#### Negative result

A negative result would demonstrate that self-reported evidence sufficiency is not independent of answer correctness and should not be used as an abstention signal.

**Status: RESERVE.**

This is scientifically attractive, but it has the largest annotation-validity problem. Without expert or carefully designed synthetic evidence labels, “sufficiency” becomes an LLM-judge construct.

## 5. Closest-work autopsy

## Strong candidate 1: visual degradation and confidence

### Closest papers

- [MVC-Bench: Benchmarking Calibration of Medical Vision-Language Models](https://www.alphaxiv.org/abs/2608.27004)
- [Confidence Calibration for Multimodal LLMs: An Empirical Study through Medical VQA](https://www.alphaxiv.org/abs/2606.19950)
- [Confident but Unreliable: A Behavioral Safety Audit of Vision-Language Models on Brain MRI](https://www.alphaxiv.org/abs/2608.02790)
- [Calibrated Triage, Not Autonomy: Confidence Estimation for Medical Vision-Language Models](https://www.alphaxiv.org/abs/2606.15910)

### What they appear to establish

[VERIFIED] The retrieved records explicitly describe confidence misalignment, calibration, overconfidence, and triage as medical-VLM problems.

[UNKNOWN] The exact visual-degradation protocol, whether image regions are masked, whether confidence is measured independently of correctness, and whether source code is available are not verified from the full papers.

### Exact remaining gap

A defensible remaining gap would be:

> **A paired, image-preserving degradation study that measures whether confidence responds specifically to loss of visual evidence, while holding the prompt, expected answer, and answer format constant.**

This is not equivalent to another calibration benchmark. The intervention isolates visual evidence availability.

### Risk of duplication

High. A recent paper may already include blur, masking, image replacement, or brain-MRI degradation. If so, the thesis must change the contribution to:

- modality-specific comparison;
- causal comparison of degradation types;
- confidence versus evidence sufficiency;
- cross-model replication with strict controls.

A new dataset alone would not be enough.

**Classification: PROCEED TO PILOT, conditional on duplication check.**

## Strong candidate 2: evidence sufficiency

### Closest papers

- [Calibrated Triage, Not Autonomy: Confidence Estimation for Medical Vision-Language Models](https://www.alphaxiv.org/abs/2606.15910)
- [Detecting Clinical Hallucinations in LVLMs via Counterfactual Visual Grounding Uncertainty](https://www.alphaxiv.org/abs/2606.28520)
- [Attention Without Grounding: Causal Evaluation of Visual Explanations in Medical VLMs](https://www.alphaxiv.org/abs/2607.18577)
- [EVADE: Evidence-Verified Agentic Diagnosis with Escape](https://www.alphaxiv.org/abs/2608.18833)
- [From Reasoning to Pixels: Grounded Medical Multimodal LLMs for VQA and Segmentation](https://www.alphaxiv.org/abs/2608.26856)

### What they appear to establish

[VERIFIED] Recent work already treats visual grounding, evidence verification, hallucination detection, and escape/abstention as explicit reliability problems.

### Exact remaining gap

The plausible gap is not “medical VLMs hallucinate.” It is:

> **Whether a model can identify insufficient visual evidence independently of whether its answer is correct.**

That distinction matters because accidental correctness can conceal unsupported reasoning.

### Main validity risk

A model-generated “evidence sufficient” label is not a ground truth. If a human expert is needed to validate it, your current feasibility assumptions are violated. If no expert is used, the thesis must define sufficiency operationally through controlled image interventions rather than through free-form medical judgment.

**Classification: RESERVE.**

## 6. Recommended pilot design

The best pilot should not begin with fine-tuning or open-ended diagnosis.

Use a closed-set task:

1. Choose a publicly downloadable image dataset whose labels and split metadata are verified.
2. Ask the VLM a constrained question with a fixed answer vocabulary.
3. Evaluate image-only, text-only, clean-image, degraded-image, and irrelevant-image conditions.
4. Require:
   - final answer;
   - confidence from 0–100%;
   - “image evidence sufficient: yes/no”;
   - one short evidence statement.
5. Use only controlled image transformations; do not ask an LLM to judge medical explanations.
6. Score the final answer from ground-truth labels.
7. Score confidence numerically.
8. Score evidence sufficiency from the experimental condition, not from the model’s prose.

The critical comparison is:

> **Does confidence fall when image evidence is removed even when the text prompt and answer prior remain unchanged?**

If not, you have a precise reliability failure.

## 7. Feasibility and compute

### Evaluation-only pilot

A small open VLM or commercial API can make the first pilot feasible.

| Component | Estimate |
|---|---|
| Training | None |
| Models | One medical/open VLM plus one general VLM control |
| Image conditions | 5–8 per original image |
| Repeated generations | 3–5 per condition for stochastic APIs |
| Dataset size | 100–500 images for the first pilot |
| Local compute | Minimal if using an API |
| T4 requirement | Sufficient for small quantized open models |
| V100/A100 | Not required for inference-only pilot, but model-dependent |
| Main cost | API calls or GPU inference, not training |
| Main engineering burden | Prompt normalization, paired transformations, logging, and scoring |

### PEFT version

A LoRA extension is not automatically feasible. It requires:

- a model with accessible weights;
- a permissive license;
- a training script;
- a multimodal data collator;
- enough VRAM for image encoder activations and language-model states;
- a held-out distribution for calibration evaluation.

The minimum PEFT experiment may fit on a T4 only for a relatively small quantized model and modest sequence length. Larger medical MLLMs may require more than 16 GB VRAM or careful offloading.

**Recommendation:** do not include PEFT in the thesis core. Add it only if the evaluation-only failure mechanism is confirmed first.

## 8. Leakage and validity audit

A medical-VLM thesis must control more than ordinary train/test leakage.

### Dataset leakage

Check:

- patient-level identity;
- repeated images;
- multiple questions per image;
- near-duplicate crops;
- train/test image overlap;
- source dataset overlap;
- answer distributions by question template.

### Caption and report leakage

If reports, captions, filenames, or question text contain the diagnosis, the model may answer without using the image.

Use:

- image-only prompts;
- neutral question templates;
- text-only controls;
- report-free inputs;
- template-balanced evaluation.

### Prompt leakage

The question must not encode the answer through terms such as:

- “Is there a melanoma?” when the label distribution is highly skewed;
- answer-bearing filenames;
- disease-specific instructions;
- class names in the image path.

### Open-ended scoring

Do not use LLM-as-a-judge as the primary medical correctness metric.

Use:

- constrained answer options;
- exact normalized labels;
- deterministic post-processing;
- manual review only for a small ambiguous subset.

### Explanation validity

A medically plausible explanation is not evidence that the model used the image.

Treat explanations as a secondary output. The primary evidence is the paired intervention:

- same prompt;
- same expected answer;
- altered visual evidence;
- measured change in answer and confidence.

### Repeated generation

For APIs and stochastic open models:

- fix temperature where possible;
- report seed or sampling settings;
- repeat each condition;
- separate epistemic variation from prompt-format variation.

## 9. Comparison with the held RQ

| Criterion | Strongest medical-VLM candidate: confidence under visual degradation | Held RQ: conflict verbalization and source arbitration |
|---|---|---|
| Scientific question clarity | Clear if “visual evidence loss” is operationalized through paired interventions | Sharper: directly asks whether an intervention changes modality arbitration |
| Literature occupancy | High; recent papers directly study medical-VLM calibration and confidence | Moderate to high; multimodal conflict and contextual distortion are active, but the causal verbalization framing remains distinctive |
| Public data | Potentially good with a verified VQA or image-label dataset | Similar data requirement, but conflict examples can be constructed more directly |
| Baseline reproducibility | Good for API evaluation; open medical-model access is uncertain | Good if the same models and prompts are used |
| Compute | Low for evaluation-only experiments | Low to moderate |
| Evaluation validity | Strong for confidence response to controlled degradation; weaker for clinical sufficiency claims | Stronger causal interpretation if modality correctness is experimentally controlled |
| Novelty confidence | Moderate at best until recent calibration papers are inspected in full | Higher because the intervention targets explanation versus decision causality |
| Negative-result value | Good: confidence may be ungrounded despite stable correctness | Excellent: unchanged arbitration despite verbalized conflict is itself a mechanistic result |
| Engineering burden | Moderate: many paired transformations and confidence protocols | Moderate: requires carefully balanced conflict construction |
| Thesis risk | Dataset and model/checkpoint availability; duplication with 2026 work | Construct validity of “source arbitration” and ensuring contradictions are medically meaningful |

The held RQ remains preferable because it asks **what changes the decision process**, not merely whether a score is calibrated.

The medical candidate would become stronger if it shows a new dissociation:

- answer correctness remains high;
- confidence remains high;
- evidence sufficiency falls;
- the model still produces unsupported visual claims.

That would identify a failure mechanism rather than only a poor metric.

## 10. Final decisions

| Candidate | Decision | Reason |
|---|---|---|
| A. Explicit contradiction detection and source arbitration | **PROCEED TO PILOT** | Precise causal intervention, strong negative-result value, directly aligned with the held RQ |
| B. Confidence under progressive visual degradation | **PROCEED TO PILOT, conditional** | Feasible and scientifically meaningful, but recent work may already cover it |
| C. Selective prediction for medical VQA | **RESERVE** | Occupied by confidence/triage literature and vulnerable to class-based abstention |
| D. PEFT improves accuracy but damages calibration | **REJECT** | Too many confounds; likely becomes an incremental LoRA comparison |
| E. Evidence sufficiency independent of answer correctness | **RESERVE** | Conceptually strong, but ground-truth sufficiency is difficult without expert validation |

If Candidate B is already tested in the closest papers, downgrade it to **RESERVE** and retain the held RQ.

# Strongest Surviving Medical-VLM Question

- **Exact RQ:** Does a medical VLM’s confidence decrease in proportion to the loss of diagnostic visual evidence when the textual prompt and expected answer remain fixed?

- **H0:** Confidence decreases monotonically with controlled visual degradation and remains calibrated relative to correctness.

- **H1:** Confidence remains high, decreases non-monotonically, or becomes dominated by language and prevalence priors after diagnostic visual evidence is removed.

- **Dataset:** A verified, directly downloadable medical image dataset with labels and no unresolved report/caption leakage. ISIC 2020 is a practical image source, but it is not inherently a VQA dataset; a medical VQA dataset must be independently verified before commitment.

- **Model:** One accessible medical VLM or open VLM plus one general VLM control. BiomedCLIP may serve as an image-text similarity control, but it is not a substitute for a generative VQA model.

- **Baseline:** Clean image, image-only prompt, fixed answer vocabulary, deterministic decoding, and unmodified model confidence.

- **Intervention:** Paired blur, downsampling, contrast reduction, lesion masking, and irrelevant-image replacement while preserving the text prompt and answer format.

- **Controls:** Text-only, clean-image, random-image, degradation-severity controls, multiple models, repeated generations, and patient/duplicate leakage checks.

- **Metrics:** Accuracy, confidence-versus-degradation slope, ECE, Brier score, NLL, risk-coverage, confidence on incorrect answers, and answer stability.

- **Expected result:** Confidence will not reliably track visual evidence loss; some models will remain overconfident when the image becomes uninformative.

- **Meaningful negative result:** If confidence does track evidence loss, the evaluated models show a measurable grounding property under the tested conditions. That would be a useful positive reliability result, although not a clinical validation.

- **Closest paper:** [MVC-Bench: Benchmarking Calibration of Medical Vision-Language Models](https://www.alphaxiv.org/abs/2608.27004), with close overlap from [Confidence Calibration for Multimodal LLMs](https://www.alphaxiv.org/abs/2606.19950) and [Confident but Unreliable](https://www.alphaxiv.org/abs/2608.02790).

- **Exact remaining gap:** Whether confidence is responsive to **controlled loss of visual evidence**, rather than merely correlated with answer correctness, dataset prevalence, question difficulty, or language priors.

- **Main feasibility risk:** A 2026 paper may already implement the same degradation intervention, or the chosen medical VLM may not have reproducible weights and a reliable confidence interface.

- **Verdict:** **PROCEED TO PILOT, but do not replace the held RQ unless the pilot reveals a distinct, non-duplicated failure mechanism.**

## 60–90 Minute Verification Task

Take one candidate medical-VLM paper from the table—start with [MVC-Bench](https://www.alphaxiv.org/abs/2608.27004)—and inspect its full paper, supplementary material, official repository, and dataset card for one question:

> **Does it already evaluate confidence after paired visual degradation or diagnostic-region masking while holding the prompt and answer fixed?**

Record only:

- exact model names and versions;
- dataset and license;
- whether image degradation is used;
- whether confidence is measured numerically;
- whether text-only and random-image controls exist;
- whether code and checkpoints are downloadable.

If the answer is yes, **reject Candidate B as insufficiently novel** and retain the held conflict-verbalization direction.