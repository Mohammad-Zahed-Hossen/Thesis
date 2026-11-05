# **Adversarial Thesis Audit: Medical Image Analysis & Federated Learning for an Undergraduate AI/ML Thesis**

## **Executive Summary**

An adversarial audit of the 2024–2026 research landscape reveals that pursuing generic medical image classification or conventional federated optimization represents an unacceptable thesis risk for a final-year undergraduate. Architectural comparisons (such as benchmarking Vision Transformers against convolutional networks on static splits) and standard federated learning (FL) algorithmic comparisons (such as evaluating FedAvg against FedProx under synthetic Dirichlet label skew) are intellectually exhausted, technically trivial, and scientifically uninformative.

Medical image analysis contains exactly one defensible research direction within the defined resource envelope: a rigorous, leakage-resistant empirical audit of selective classification (prediction with an abstention or reject option) under physical acquisition and demographic distribution shifts in dermatological imaging. While in-distribution calibration and automated referral are heavily populated in the recent literature, existing studies fail to isolate whether confidence scoring functions preserve sample-level risk-coverage rankings when evaluated under clinically grounded acquisition shifts (such as dermoscopy transferred to clinical smartphone cameras) and whether post-hoc recalibration genuinely repairs selective risk or merely shifts decision thresholds. Pervasive cross-release contamination in public skin-lesion datasets (notably HAM10000 nested within ISIC 2019\) and unstratified patient records have produced widespread over-optimism in published selective prediction baselines. This direction is executable on single-GPU Google Colab Pro, uses accessible public data, requires no specialized clinical partnerships, and provides a scientifically valuable negative result if confidence ranking breaks under shift.

Federated learning in medical imaging contains a narrow, active niche concerning site-conditional calibration and worst-client statistical risk control. While the core observation that naive pooled calibration violates institutional safety bounds has been demonstrated on 3D brain magnetic resonance imaging (MRI) by Fed-CRC-Seg in 2026, its operational boundary conditions—specifically client dropout, partial participation, and sample-complexity walls—remain unmapped. However, medical FL faces severe structural friction: genuine multi-institutional datasets with authentic clinical site identifiers are virtually non-existent in public archives, with FeTS-2022 serving as the lone defensible exception. Simulating federations by arbitrarily partitioning single-center datasets generates artificial statistical artifacts that cannot support credible claims regarding real hospital networks.

Neither candidate outranks the researcher's held trustworthy Vision-Language Model (VLM) thesis track concerning causal multimodal conflict verbalization and source arbitration. The VLM direction exhibits higher conceptual novelty, avoids the severe validation hazards of medical AI, and requires no multi-institutional data infrastructure. Consequently, the non-VLM dermoscopy selective prediction question is assigned **PROCEED TO PILOT** as an empirical safety audit, the FL conformal worst-site question is assigned **RESERVE**, and all generic classification, segmentation, and synthetic FL variants are **REJECTED**.

## **Section 1 — State of Medical Image Analysis**

The medical image analysis research landscape across the 2024–2026 period is characterized by an acute division between industrial foundation model pretraining and academic post-hoc reliability evaluation. Supervised diagnostic classification across mature 2D imaging modalities—including chest radiography, retinal fundus photography, and dermoscopy—is saturated. Demonstrating incremental improvements in Area Under the Receiver Operating Characteristic (AUROC) or F1-score on standard benchmarks no longer constitutes an acceptable scientific contribution for an academic thesis.

Saturated paradigms that must be summarily rejected include model architecture bake-offs (such as ConvNeXt versus Swin Transformer), standard supervised classification on HAM10000 or ChestX-ray14, in-distribution post-hoc temperature scaling, qualitative saliency map comparisons without falsifiable grounding metrics, and naive test-time adaptation (TTA) that fails to monitor source-domain representation collapse.

Active research frontiers focus on statistical guarantees and distribution-shift mechanics. Key active lines of inquiry include conformal risk control for distribution-free error bounding, selective classification systems that optimize the trade-off between coverage and retained risk, rigorous audits of shortcut learning wherein models exploit non-biological acquisition markers, and representation drift occurring during parameter-efficient fine-tuning (PEFT).

A critical methodological defect pervades published medical computer vision studies: widespread dataset contamination and artifactual confounding. Public benchmark archives are frequently assembled by aggregating disparate historical challenges without reconciling duplicate instances. For example, models trained on aggregate repositories while evaluated on benchmark subsets unknowingly suffer from severe patient-level and image-level leakage. Furthermore, medical image classifiers regularly learn spurious correlations with acquisition-specific artifacts—such as dermatological dermatoscope borders, calibration stickers, surgical skin pen markings, and high-frequency sensor noise—achieving inflated test set accuracy while experiencing catastrophic diagnostic failure upon external multi-center deployment.

Recent literature has progressed from forced-choice prediction toward selective classification, equipping models with a confidence scoring function and a rejection threshold to defer uncertain predictions to human experts. However, standard multi-threshold evaluation metrics such as the Area Under the Risk-Coverage Curve (AURC) have recently been proven mathematically flawed for comparing distinct base classifiers, necessitating the adoption of normalized frameworks like the Area Under the Generalized Risk-Coverage curve (AUGRC). Investigating whether selective classification mechanisms maintain sample ranking under physical distribution shifts represents one of the few defensible, accessible undergraduate research niches.

## **Section 2 — State of Federated Learning**

Federated learning in healthcare is routinely motivated by institutional data governance frameworks, such as HIPAA and GDPR, which restrict the pooling of patient records into centralized repositories. Despite this practical motivation, academic medical FL literature is saturated with studies that merely wrap standard distributed optimization algorithms (such as FedAvg, FedProx, or FedNova) around arbitrarily partitioned public datasets.

Paradigms within medical FL that must be rejected include standard algorithmic benchmarking over synthetic Dirichlet class-distribution skews, multi-center simulations on public datasets lacking native institutional provenance, FL workflows evaluated without a centralized matched-compute control, and studies reporting only population-level weighted average performance across communication rounds.

Active research frontiers in distributed medical systems include federated conformal prediction and risk control, disparity analyses exposing how global aggregation masks localized diagnostic collapse at tail institutions, feature space misalignment resulting from non-IID optimization trajectories, and parameter-efficient federated fine-tuning (Fed-PEFT/Fed-LoRA) aggregation operators.

The primary methodological weakness in published medical FL research is the reliance on unrealistic client simulation protocols. In authentic multi-institutional clinical consortia, client heterogeneity is not driven by Dirichlet label skew; it is governed by feature and acquisition shifts (disparate MRI field strengths, scanner manufacturers, slice thicknesses, and staining protocols), institutional disease prevalence differences, and massive disparities in local patient volume. Recent theoretical and empirical evaluations indicate that standard distributed optimization techniques often fail under genuine medical heterogeneity: algorithms designed to mitigate client drift (such as SCAFFOLD) can suffer severe instability or divergence when paired with adaptive optimizers in multimodal tasks, whereas FedAvg converges stably. Crucially, federated parameter aggregation regularly obscures critical failures: a global model can report acceptable average Dice coefficients or accuracy across a federation while experiencing total diagnostic failure on resource-constrained minority client sites.

## **Section 3 — Key Research Phenomena**

To establish scientific defensibility, an undergraduate thesis must isolate and interrogate a precise, measurable statistical failure mode rather than assemble standard software libraries. The literature supports five technically meaningful open phenomena across medical computer vision and distributed systems:

The first phenomenon is the disparity between marginal and site-conditional calibration in distributed systems \[VERIFIED\]. Global federated aggregation pools calibration residuals to satisfy population-level marginal error guarantees of the form \[span\_70\](start\_span)\[span\_70\](end\_span)P(Y \\notin C(X)) \\le \\alpha. However, because institutional data distributions P\_k(X, Y) diverge significantly, local coverage guarantees are routinely violated. Tail institutions with small sample sizes experience severe undercoverage (P\_k(Y \\notin C(X)) \\gg \\alpha), demonstrating that naive pooling protects the average clinic while shifting clinical risk onto vulnerable, low-volume healthcare centers.

The second phenomenon is rank-inversion and metric decoupling in selective prediction under domain shift \[VERIFIED\]. A confidence scoring function g(X) that effectively ranks samples by error likelihood in-distribution can suffer rank inversions under physical acquisition shift. While post-hoc recalibration techniques adjust absolute probabilities to match class frequencies, they apply monotonic transformations that cannot alter sample rankings. Consequently, selective triage fails precisely in external environments where referral is most needed.

The third phenomenon is shortcut invariance masquerading as generalizability \[VERIFIED\]. Convolutional networks exploit non-biological acquisition artifacts (such as dermatoscope vignette rings, ruler markings, or scanner calibration tags) as predictive proxies. When evaluated across institutions, classification performance collapses because the correlation between the artifact and the clinical label breaks. Standard data augmentations fail to mitigate this failure unless explicitly targeted at sensor physics.

The fourth phenomenon is aggregation-induced representation distortion in federated optimization \[VERIFIED\]. Parameter averaging across clients undergoing local optimization on non-IID manifolds distorts the geometry of the shared representation space. While linear diagnostic probes may recover basic accuracy, the underlying feature distributions drift, compromising post-hoc uncertainty quantification and confidence estimation.

The fifth phenomenon is the decoupling of prevalence shift from sensor shift in medical recalibration \[VERIFIED\]. Clinical distribution shifts conflate base-rate alterations P(Y) with physical sensor transformations P(X|Y). Adjusting predictions via prevalence recalibration corrects global marginal bias but leaves models vulnerable to feature corruption and image-level noise.

## **Section 4 — Literature Audit**

The following table compiles eighteen primary research papers from 2024 to 2026 addressing calibration, selective prediction, domain shift, and federated learning across medical computer vision.

| Paper | Year | Research Problem | Dataset | Model | Method | Baselines | Metrics | Main Finding | Limitation | Code / Data Access |
| :---- | :---- | :---- | :---- | :---- | :---- | :---- | :---- | :---- | :---- | :---- |
| Fed-CRC-Seg | 2026 | Site-conditional calibration failure in FL | FeTS-2022 (1,251 subjects, 20 sites) | 3D U-Net | Federated Conformal Risk Control with risk-curve shrinkage (n\_0=19) | Pooled CRC, Local CRC, Macro-threshold averaging | Worst-site FNR, Marginal coverage, Violation rate | \[VERIFIED\] Naive pooled CRC violates coverage at 40% of institutions; worst site exceeds FNR budget by 7.8 percentage points. | Assumes full client participation; does not assess client dropout. | Code: Public. Data: Synapse (Registration required). |
| AUGRC Framework | 2024 | Flawed evaluation metrics in selective classification | 6 benchmarks (incl. CAMELYON-17) | ResNet-50, DenseNet-121 | Formalization of multi-threshold selective classification; AUGRC metric | AURC, E-AURC, AUROC | AUGRC, Generalized Risk, Selective Risk | \[VERIFIED\] AURC penalizes classifiers for baseline error rather than ranking quality; AUGRC isolates failure detection. | Omits post-hoc recalibration under structured sensor shifts. | Code: Public (NeurIPS). Data: Public. |
| MedFL-Stress | 2026 | Federated brain segmentation under scanner stress | BraTS 2020 (simulated 4 hospitals) | 3D U-Net | Configurable stress-testing across graded MRI appearance shifts | FedAvg, FedProx, FedBN | Mean Dice, Best-worst hospital Dice gap | \[VERIFIED\] FedBN closes inter-hospital Dice gap by 41% under appearance shifts while losing \<0.5% mean Dice. | Synthetic shifts applied to BraTS rather than natural multi-site acquisitions. | Code: Partial. Data: Public BraTS (CBICA). |
| Searching for Robust Augmentations | 2026 | Out-of-domain generalization in dermoscopy | 6 dermoscopic sources (25,903 images) | ConvNeXt-Large | Systematic search of augmentations under strict contamination control | Standard RandAugment, In-domain baseline | OOD ROC-AUC, Sensitivity | \[VERIFIED\] Photometric transformations improve OOD ROC-AUC by \+0.053 (p \< 0.001) under strictly source-disjoint splits. | Evaluates discriminative accuracy only; omits calibration and abstention. | Code: Partial. Data: Public ISIC archives. |
| Prevalence Calibration | 2025 | Shortcut learning under prevalence shift | CheXpert, SIIM-ACR Pneumothorax | DenseNet-121 | Post-hoc logit recalibration adjusting for demographic skew | ERM, GroupDRO, Subconscious Shortcut Removal | Worst-group AUROC, ECE, Subgroup accuracy | \[VERIFIED\] Recalibrating probabilities mitigates shortcuts, raising misaligned subgroup AUROC from 0.23 to 0.73. | Chest X-ray report-derived labels carry inherent text-mining noise. | Code: Public. Data: Public / Stanford terms. |
| MVC-Bench | 2026 | Medical VLM calibration under clinical shift | Fundus, Pathology, Chest X-rays | 8 Medical VLMs (BiomedCLIP, etc.) | Large-scale calibration benchmarking (1,638 runs); MCM regularization | Standard zero-shot VLM, Temp Scaling | ECE, MCE, Adaptive ECE, Accuracy | \[VERIFIED\] 0/30 transfer settings show positive calibration rank-transfer; models miscalibrate severely under shift. | Focuses on multi-choice VQA; does not evaluate selective prediction. | Code: Public. Data: Curated public benchmarks. |
| Fed-LoRA BiomedCLIP | 2026 | Multi-cohort chest X-ray adaptation under FL | 4 international CXR cohorts (NIH, CheXpert, etc.) | BiomedCLIP (ViT-B/16 \+ PubMedBERT) | Federated LoRA with product-space (FlexLoRA) aggregation | FedAvg, FedProx, Centralized pooled | Multi-label shared-class AUC | \[VERIFIED\] Product-space LoRA aggregation prevents a 0.097 AUC drop observed with naive factor averaging. | Single-seed experiments; completely ignores calibration and worst-site metrics. | Code: Partial. Data: Mixed public/restricted. |
| Uncertainty-Aware RETFound | 2025 | Selective referral under shift in retinal screening | APTOS-2019, DDR, Messidor-2 | RETFound (ViT-Large foundation model) | Uncertainty-aware last-layer adaptation (SNGP, Deep Ensembles) | Linear probing, MC-Dropout | Risk-coverage curves, AURC, NLL | \[VERIFIED\] SNGP exhibits negative transfer under camera shift; deep ensembles yield stable selective referral. | Compute-intensive backbone (ViT-L); limited to retinal imaging. | Code: Public. Data: Kaggle / Academic. |
| Disease Burden over Skin Tone | 2025 | Decomposing generalization gaps across metadata | HAM10000, ISIC 2019, DDI, SCIN | ResNet-50, EfficientNet-B4 | Empirical decomposition of error across disease prevalence vs. skin tone | Empirical Risk Minimization, Reweighted ERM | Top-1 Accuracy, Representation disparity | \[VERIFIED\] Clinical disease burden and taxonomy shifts contribute significantly more to error than skin tone. | Evaluates accuracy only; does not analyze confidence scoring or abstention. | Code: Public. Data: Public / Research agreement. |
| CRS-Bench | 2025 | Encoder reliability under clinical distribution shift | ISIC 2019, APTOS, CheXpert, MIMIC | Vision Encoders (DINOv2, CLIP, BioMed) | Cross-domain reliability benchmarking under structured clinical shifts | Standard linear probe, Fine-tuning | ECE, Brier score, Robust Accuracy | \[VERIFIED\] Self-supervised clinical foundation models do not inherently yield superior calibration to ImageNet baselines. | Broad benchmark suite; proposes no operational decision mechanism. | Code: Public. Data: Multi-source. |
| Probabilistic Robustness in Medical AI | 2025 | Robustness under natural and synthetic corruptions | MedMNIST v2 (DermaMNIST, PathMNIST) | ResNet-18, ViT-Tiny | Probabilistic robustness evaluation under ImageNet-C perturbations | Standard ERM, AugMix | Corrupted ECE, Perturbation score | \[VERIFIED\] Image corruptions disproportionately distort predictive entropy before degrading accuracy. | Evaluated on 28x28 MedMNIST images, failing to model clinical artifacts. | Code: Public. Data: Public package. |
| Calibrated Selective Ultrasound | 2026 | Selective prediction under ultrasound shift | Retrospective thyroid ultrasound cohorts | Deep Ensembles (ResNet-50) | Selective classification with ensemble disagreement under scanner shift | Softmax Probability, MC-Dropout | Selective risk at 80% coverage, AUGRC, ECE | \[VERIFIED\] Ensemble disagreement preserves selective risk ordering across ultrasound machines where single models fail. | Private retrospective clinical cohort; unverified reproducibility. | Code: Unavailable. Data: Private clinical data. |
| Subtype Robustness | 2026 | Calibration failure under unseen clinical subtypes | Histopathology, Dermoscopy | ConvNeXt, Swin Transformer | Subtype-stratified calibration and accuracy evaluation | Standard ERM, Focal Loss | Worst-subtype ECE, Subtype AUROC | \[VERIFIED\] High overall classification accuracy regularly conceals severe miscalibration on unobserved subtypes. | Subtype metadata manually annotated; difficult to scale to uncurated data. | Code: Partial. Data: Public subsets. |
| When Adaptation Hurts | 2026 | Representational drift during MedSAM fine-tuning | Multi-organ CT/MRI benchmarks | MedSAM (ViT-B) | Layer-wise representational drift analysis during parameter fine-tuning | Full fine-tuning, LoRA, Prompt tuning | OOD Dice score, Feature cosine drift | \[VERIFIED\] Fine-tuning on downstream domains causes representational drift and out-of-distribution failure. | Focuses entirely on segmentation Dice; omits probabilistic calibration. | Code: Public. Data: Public challenges. |
| Calibrated Triage, Not Autonomy | 2026 | Confidence estimation for clinical deferral | VQA-RAD, SLAKE, PathVQA | Medical VLMs | Selective prediction benchmarks comparing 9 confidence estimators | Softmax probability, Entropy, Verbalized confidence | Deferral rate under fixed error tolerance, AUGRC | \[VERIFIED\] At 20% error tolerance, \~25% of radiology cases are deferred under guarantees, but 0% of pathology cases succeed. | Multi-modal VLM focus; high inference compute requirements. | Code: Public. Data: Public VQA benchmarks. |
| Confident but Unreliable | 2026 | Overconfidence in vision models on brain MRI | Brain MRI (4,102 images, 250 subjects) | General and Medical VLMs | Behavioral audit quantifying high-confidence diagnostic confabulations | Zero-shot, Few-shot CoT | ECE (0.27–0.40), Error-confidence ratio | \[VERIFIED\] Vision-language models exhibit extreme overconfidence on brain MRI, with mean error-confidence reaching 0.82–0.97. | Observational behavioral study; develops no algorithmic fix. | Code: Partial. Data: Public metadata \+ masks. |
| MC-CXR | 2026 | Conflict arbitration in multimodal radiology | Paired Chest X-ray perturbation benchmark | GPT-5.5, Open VLMs | Paired visual vs. textual contradiction injection | Direct prompt, Chain-of-Thought | Switch-to-wrong rate, Label-aligned error | \[VERIFIED\] Misleading clinical text flips 45.6% to 78.1% of correct image-based decisions; conflict verbalization alone fails to alter decisions. | Requires PhysioNet credentialing; evaluation limited to 240 pairs. | Code: Partial. Data: Credentialed PhysioNet. |
| Data-Centric Non-IID Review | 2026 | Taxonomy of federated data heterogeneity | Benchmark survey across vision benchmarks | Standard FL models | Methodological comparison of Dirichlet, quantity, and domain partitioning | FedAvg, FedProx, FedNova, SCAFFOLD | Convergence rate, Heterogeneity ranking | \[VERIFIED\] Artificial Dirichlet label skews rank optimization algorithms differently than authentic feature shifts. | Meta-analysis paper; contains no original empirical benchmarks. | Code: N/A. Data: Literature meta-analysis. |

Across these eighteen core papers, none evaluate whether multi-threshold selective classification metrics (AUGRC) survive physical sensor shifts when tested on contamination-controlled dermatological benchmarks. Concurrently, while site-conditional conformal risk control is established on 3D MRI by Fed-CRC-Seg, its sensitivity to partial client participation and institutional sample complexity remains completely unaddressed.

## **Section 5 — Dataset Audit**

Every candidate dataset must be evaluated based on immediate accessibility, data licensing, patient-level grouping, and leakage risks. Public documentation does not guarantee immediate usability for an uncredentialed undergraduate team.

| Dataset | Modality | Task | Scale | Labels | Access Status | License | Patient IDs? | Contamination / Leakage Risks | Domain Heterogeneity | Colab Pro Viability | Thesis Suitability Verdict |
| :---- | :---- | :---- | :---- | :---- | :---- | :---- | :---- | :---- | :---- | :---- | :---- |
| FeTS-2022 | 3D mpMRI (Brain) | Glioma sub-region segmentation | 1,251 train / 219 val subjects | Voxel-level multi-class masks | Synapse project registration required | Non-commercial research | Yes (Subject IDs provided) | Low if using native partitions; high if splitting slices across folds | High (23–33 authentic clinical institutions with native labels) | Low for scratch training; High for inference/calibration | **RESERVE** (Access friction; volumetric 3D training exceeds constraints) |
| ISIC 2020 | 2D Dermoscopy | Binary melanoma classification | 33,126 images (2,056 patients) | Malignant / Benign | Direct downloadable archive | CC-BY-NC 4.0 | Yes (patient\_id, lesion\_id) | Extreme: 425 exact/near duplicates documented; multi-image lesions | High (6 international clinical contributing centers) | High (224x224 / 256x256 JPEGs) | **PROCEED TO PILOT** (Primary training and validation spine) |
| ISIC 2019 | 2D Dermoscopy | 8-class diagnostic classification | 25,331 images | Biopsy-verified classes | Direct downloadable archive | CC-BY-NC 4.0 | Partial (lesion\_id present; lacks global patient\_id) | Critical: Wholly encompasses HAM10000; mixing splits causes 100% leakage | Moderate (Multi-center archive aggregation) | High | **PROCEED TO PILOT** (Secondary evaluation set) |
| HAM10000 | 2D Dermoscopy | 7-class diagnostic classification | 10,015 images | Diagnostic categories | Harvard Dataverse download | Custom Academic / CC-BY-NC | Partial (lesion\_id links multiple lesion crops) | High: \~10 images per patient; nested inside ISIC 2019 | Low (Two primary centers: Vienna and Queensland) | High | **RESERVE** (Usable strictly as a subset of ISIC 2019\) |
| PAD-UFES-20 | 2D Clinical Photos | 6-class skin lesion diagnosis | 2,298 images (1,373 patients) | Biopsy-proven categories | Open mirror (Mendeley/Kaggle) | CC-BY 4.0 | Yes (patient\_id) | Low if split by patient; distinct clinical smartphone capture | High (Clinical smartphone photos vs. dermoscopy) | High | **PROCEED TO PILOT** (Ideal external sensor shift test) |
| DDI (Diverse Derm) | 2D Clinical Photos | 18 diagnostic categories | 656 images | Biopsy-confirmed categories | Stanford AIMI Portal | Research Use Agreement | Yes | Exempt (Used strictly as held-out external test set) | High (Stratified Fitzpatrick skin tones I–VI) | High | **PROCEED TO PILOT** (Ideal demographic shift test) |
| SCIN | 2D Clinical Photos | Crowdsourced skin conditions | 10,000+ submissions | Crowdsourced condition labels | Hugging Face / Google | SCIN Data Use License | Yes | 15 known duplicate images (42 occurrences) | High (Crowdsourced smartphone submissions) | High | **RESERVE** (Diagnostic taxonomy differs from ISIC classes) |
| MedMNIST v2 | Standardized 2D/3D biomedical | Classification / Ordinal regression | 708,000+ standardized | Task-specific labels | Python API (pip install medmnist) | CC-BY 4.0 (Derma CC-BY-NC) | No (Standard API does not expose patient IDs) | Uncontrolled: Standard splits do not guarantee patient independence | Synthetic / Standardized (Low clinical realism) | Extremely High (Trivial compute) | **REJECT** (Too toy to support a serious research claim) |
| CheXpert | 2D Chest Radiographs | 14 frontal/lateral observations | 224,316 images (65,240 patients) | Multi-label NLP-extracted | Stanford AIMI Portal | Research-use registration | Yes (patient\_id, study\_id) | Moderate: multi-view exams per patient; report-mined label noise | Low internally (Single health system: Stanford) | Moderate | **RESERVE** (Access requires portal verification) |
| MIMIC-CXR | 2D Chest Radiographs \+ Text | Multi-label diagnostic classification | 377,110 images (64,588 patients) | DICOM \+ Free-text reports | PhysioNet Credentialed | PhysioNet DUA \+ CITI training | Yes (subject\_id, study\_id) | Low if subject splits are strictly enforced; severe storage overhead | High (Single-center longitudinal, multi-scanner) | Low–Moderate (Massive storage and preprocessing burden) | **REJECT** (Mandatory CITI training and DUA violate timeline) |
| BraTS 2020 | 3D mpMRI (Brain) | Brain tumor segmentation | 369 clinical subjects | Multi-modal segmentation masks | CBICA IPP Portal | Non-commercial research | No (TCGA mapping messy; lacks public site labels) | High if 2D slices are split instead of 3D patient volumes | Moderate (Multi-scanner clinical routine) | Low (Heavy 3D volumetric training) | **REJECT** (Lacks natural institutional site labels) |
| SLAKE / VQA-RAD | Multimodal Radiology VQA | Closed/Open Medical VQA | 642–314 images / 2k–14k QA | Text answers | Hugging Face / OSF | CC-BY 4.0 / CC0 | No | High: Template question leakage; identical images shared across QA | Low (Single curated collections) | High (Evaluation-only) | **RESERVE** (Viable only for VLM benchmark comparison) |

A rigorous dermatological thesis must manage patient-level leakage, near-duplicate images, and nested challenge releases. The official ISIC 2020 distribution includes 425 duplicate images that must be removed prior to partitioning. Furthermore, because ISIC 2019 subsumes HAM10000 entirely, any experimental design that trains on ISIC 2019 and evaluates on HAM10000 constitutes catastrophic cross-split leakage. Valid generalization testing requires training on patient-stratified ISIC data and testing on externally collected cohorts such as PAD-UFES-20 and DDI.

## **Section 6 — Baseline and Model Audit**

To maintain reproducibility and prevent runtime failures on single-GPU Colab Pro instances, candidate models and algorithmic baselines must operate within a 16 GB VRAM budget.

For standard convolutional architectures, ResNet-18 (11.2 million parameters) and DenseNet-121 (7.0 million parameters) serve as reliable baselines. At an input resolution of 224x224 with a batch size of 64 in mixed-precision (FP16), DenseNet-121 consumes approximately 3.8 GB of VRAM, executing an epoch over 25,000 images in roughly 45 seconds on an NVIDIA T4. This guarantees complete stability and rapid iteration. ConvNeXt-Tiny (28 million parameters) provides an alternative convolutional baseline, consuming under 6.0 GB of VRAM.

Confidence scoring baselines require minimal additional compute. Maximum Softmax Probability (MSP) introduces zero overhead. Post-hoc temperature scaling involves optimizing a single scalar parameter via negative log-likelihood on a patient-stratified validation set, taking seconds on a CPU. Monte Carlo Dropout requires 10 to 20 forward passes per test image at inference, taking under five minutes for a 2,000-image test set. Deep ensembles consisting of five separately seeded DenseNet-121 models require a linear 5\\times training multiplier (approximately 1.25 hours total compute on Colab Pro), serving as an established benchmark for predictive uncertainty. Multi-threshold selective classification performance must be evaluated using the official AUGRC implementation formalized by Traub et al. at NeurIPS 2024\.

Federated learning simulations can be executed on a single GPU using two distinct paradigms. The Flower framework (flwr) provides a Virtual Client Engine (VCE) that schedules virtual clients as Ray actors, allowing multi-client simulations where each client is assigned fractional GPU resources (for example, num\_gpus=0.25). However, Ray-based client scheduling introduces runtime overhead, memory spilling, and frequent framework API updates.

Alternatively, a native PyTorch sequential simulation loop executes federated training by iterating through client datasets in standard Python code. This native approach requires zero distributed systems dependencies, eliminates framework abstraction bugs, guarantees deterministic execution across fixed random seeds, and simplifies debugging. PySyft and FedML are explicitly rejected: PySyft has deprecated its classic machine learning orchestrator in favor of syft-rds, while FedML has pivoted toward commercial cloud platforms.

## **Section 7 — Medical Imaging Candidate Research Questions**

The following eight candidate research questions address medical image analysis without federated learning, each structured around a concrete failure mode, controlled variables, and a falsifiable hypothesis.

### **RQ-M1: Failure of Selective Classification Ranking Under Acquisition Sensor Shift**

Under physical sensor shift (transitioning from standardized dermoscopy to clinical smartphone photography), a model's confidence ranking can invert: it becomes overconfident on out-of-distribution diagnostic errors and underconfident on simple in-distribution cases, increasing the selective risk among retained predictions.

> * **Hypothesis (H\_1):** Selective prediction performance (measured by AUGRC) degrades significantly under sensor shift, and post-hoc temperature scaling fails to restore the in-distribution risk-coverage curve because calibration adjusts absolute probabilities without correcting rank inversions.  
> * **Dataset:** Training and validation: ISIC 2020 \+ ISIC 2019 (patient-partitioned dermoscopy). External test: PAD-UFES-20 (smartphone clinical photos) and DDI.  
> * **Baseline:** DenseNet-121 trained via standard cross-entropy with uncalibrated Maximum Softmax Probability (MSP).  
> * **Intervention:** Systematic application of post-hoc Temperature Scaling, MC-Dropout, and Deep Ensembles evaluated across in-domain and external test domains.  
> * **Metrics:** AUGRC (Area Under Generalized Risk-Coverage), AURC, Expected Calibration Error (ECE), Brier score, Selective Risk at 70%, 80%, and 90% coverage.  
> * **Falsification Condition (H\_0):** In-distribution and out-of-distribution AUGRC values remain statistically indistinguishable (p \> 0.05 via bootstrap resampling), indicating that confidence ranking is invariant to sensor shift.  
> * **Scientific Contribution if Positive:** Demonstrates that post-hoc calibration is insufficient for reliable automated triage under acquisition shift, establishing the necessity of rank-preserving uncertainty estimators.  
> * **Scientific Contribution if Negative:** Establishes that standard confidence scoring functions provide robust safety margins across imaging modalities, disproving the common assumption that sensor shift inevitably degrades selective ranking.

### **RQ-M2: Disentangling Prevalence Shift from Sensor Shift in Medical Recalibration**

Clinical distribution shifts conflate base-rate alterations P(Y) with physical sensor transformations P(X|Y). Applying label-shift correction alone adjusts global marginal calibration but can obscure severe sample-level predictive entropy degradation caused by sensor artifacts.

> * **Hypothesis (H\_1):** Prevalence recalibration improves marginal calibration metrics (ECE, Brier score) while failing to improve or actively degrading sample-level selective risk (AUGRC) under severe sensor shift.  
> * **Dataset:** ISIC 2020 (source) tested against synthetic prevalence-skewed partitions of PAD-UFES-20.  
> * Baseline: Unadjusted DenseNet-121 evaluated under shifted prevalence.  
> * **Intervention:** Analytical Bayesian logit correction for class prevalence versus full post-hoc feature recalibration.  
> * **Metrics:** ECE, Class-conditional ECE, AUGRC, Balanced Accuracy.  
> * **Falsification Condition (H\_0):** Prevalence adjustment restores both ECE and AUGRC to within 2% of in-distribution values, confirming that prevalence shift accounts for selective failure under domain transfer.  
> * **Scientific Contribution if Positive:** Proves that standard clinical calibration metrics (ECE) can produce dangerous illusions of safety when prevalence shift co-occurs with acquisition shift.  
> * **Scientific Contribution if Negative:** Confirms that correcting for clinical base-rate variations is sufficient to maintain operational safety under moderate domain transfer.

### **RQ-M3: Impact of Patient-Level Leakage on Selective Classification Benchmarks**

When multiple images of the same lesion or patient appear across training and test splits, the model memorizes patient-specific idiosyncrasies, yielding artificially low selective risk estimates that collapse on novel patient cohorts.

> * **Hypothesis (H\_1):** Random image-level splitting yields significantly superior AUGRC and lower selective risk compared to patient-disjoint splitting, with the performance gap widening at high coverage thresholds.  
> * **Dataset:** ISIC 2020 (leveraging verified patient\_id metadata).  
> * **Baseline:** Model evaluated on random 80/20 image-level splits (flawed baseline reflecting standard benchmark errors).  
> * **Intervention:** Model evaluated on strict patient-level grouped splits and lesion-deduplicated splits.  
> * **Metrics:** \\Delta\\text{AUGRC}, \\Delta\\tex\[span\_13\](start\_span)\[span\_13\](end\_span)t{ECE}, Selective Risk at 85% coverage, Duplicate identification rate.  
> * **Falsification Condition (H\_0):** The difference in AUGRC between random and patient-disjoint splits is statistically indistinguishable from zero (\\Delta\\text{AUGRC} \< 0.005).  
> * **Scientific Contribution if Positive:** Quantifies the exact extent to which published selective prediction literature overstates real-world clinical referral performance due to data leakage.  
> * **Scientific Contribution if Negative:** Establishes that lesion-level morphological features dominate patient-specific background features in deep representations, rendering patient leakage a minor factor in selective risk.

### **RQ-M4: Failure of Abstention Mechanics Around Spurious Acquisition Shortcuts**

Models predict diagnostic labels with high confidence because they rely on spurious non-biological artifacts (such as dermatoscope vignette rings or skin markings) that correlate with disease classes in the training distribution.

> * **Hypothesis (H\_1):** Confidence scoring functions assign high confidence to shortcut-dependent incorrect predictions, causing selective classification to fail at filtering out spurious feature reliance.  
> * **Dataset:** ISIC 2019 / 2020 augmented with controlled border and marker artifacts (following Nauta et al. protocols).  
> * **Baseline:** Standard ERM DenseNet-121.  
> * **Intervention:** Comparing standard MSP against energy-based out-of-distribution scores and Deep Ensemble variance on artifact-injected samples.  
> * **Metrics:** Error-detection AUROC on shortcut samples, False Referral Rate, AUGRC.  
> * **Falsification Condition (H\_0):** Predictive confidence drops significantly on shortcut-corrupted samples (p \< 0.001), allowing standard thresholding to abstain on \>90% of shortcut errors.  
> * **Scientific Contribution if Positive:** Exposes that confidence-based referral cannot serve as a clinical safety net for models compromised by shortcut learning.  
> * **Scientific Contribution if Negative:** Demonstrates that epistemic uncertainty estimators naturally register artifactual perturbations, functioning as an implicit defense against shortcuts.

### **RQ-M5: Photometric Domain-Generalization Augmentation versus Clean Calibration**

Heavy photometric augmentations (contrast adjustments, gamma variations, color jitter) enforce feature invariance across acquisition hardware but distort predicted class probabilities, causing probability miscalibration on clean, standard images.

> * **Hypothesis (H\_1):** Robust out-of-domain augmentations improve cross-dataset AUROC but cause a statistically significant degradation in in-domain ECE and AUGRC.  
> * **Dataset:** Training: ISIC multi-source archive. Evaluation: Clean in-domain validation versus OOD test (PAD-UFES-20). \* **Baseline:** ConvNeXt-Tiny / ResNet-50 trained with standard minimal cropping and flipping.  
> * **Intervention:** Training with the winning composite photometric augmentation policy from Kozachok et al. (2026).  
> * **Metrics:** In-domain vs. OOD AUROC, ECE, Brier score, AUGRC.  
> * **Falsification Condition (H\_0):** Photometric augmentations improve OOD generalization while leaving in-domain ECE and AUGRC unchanged or improved (\\Delta\\text{ECE} \\le 0).  
> * **Scientific Contribution if Positive:** Identifies an accuracy-calibration trade-off in medical domain generalization, proving that robustness interventions can impair clinical decision thresholds.  
> * **Scientific Contribution if Negative:** Demonstrates that sensor-grounded augmentations act as regularizers that simultaneously benefit discriminative transfer and uncertainty estimation.

### **RQ-M6: Instability of Test-Time Adaptation on Out-of-Domain Medical Calibration**

Test-time adaptation adjusting batch normalization statistics or minimizing Shannon entropy on unlabelled target streams can induce probability overconfidence on ambiguous minority classes.

> * **Hypothesis (H\_1):** TTA marginally improves target domain accuracy but severely degrades calibration error (ECE) and selective ranking (AUGRC), rendering outputs uncalibrated for clinical triage.  
> * **Dataset:** Source: ISIC 2020\. Target stream: PAD-UFES-20.  
> * **Baseline:** Frozen source model evaluated directly on the target stream.  
> * **Intervention:** Test-Time Entropy Minimization applied continuously to convolutional feature layers.  
> * **Metrics:** Target Accuracy, Target ECE, Target AUGRC, Source domain degradation upon reset.  
> * **Falsification Condition (H\_0):** TTA reduces target error while monotonically decreasing ECE and improving AUGRC across the adaptation stream.  
> * **Scientific Contribution if Positive:** Warns the medical AI community against deploying standard computer vision TTA techniques in clinical workflows requiring calibrated confidence.  
> * **Scientific Contribution if Negative:** Confirms that online entropy minimization safely aligns predictive representations across clinical imaging centers.

### **RQ-M7: Disparity of Selective Referral Across Diverse Skin Tones**

Due to representation imbalances in public training datasets, confidence scores for darker skin tones (Fitzpatrick V–VI) exhibit higher variance, resulting in disproportionate false abstentions or elevated diagnostic error rates among retained cases.

> * **Hypothesis (H\_1):** At an identical nominal coverage threshold (e.g., 80%), retained-case diagnostic error is significantly higher for Fitzpatrick types V–VI than for types I–II.  
> * **Dataset:** DDI (Diverse Dermatology Images) and Fitzpatrick-stratified subsets of ISIC 2020\.  
> * **Baseline:** Global thresholding calibrated on the aggregate validation set.  
> * **Intervention:** Group-conditional recalibration versus marginalized selective thresholding.  
> * **Metrics:** Subgroup Selective Risk, Subgroup Coverage, Disparity Ratio, AUGRC per skin-tone tier.  
> * **Falsification Condition (H\_0):** Error rates among retained predictions do not differ significantly across skin-tone categories (\\Delta\\text{Selective Risk} \< 0.02, p \> 0.05).  
> * **Scientific Contribution if Positive:** Proves that automated triage mechanisms can inadvertently amplify clinical health disparities even when global selective risk appears optimal.  
> * **Scientific Contribution if Negative:** Shows that confidence-based referral naturally absorbs skin-tone difficulty differences without generating subgroup safety disparities.

### **RQ-M8: Conformal Prediction Set Inflation Under Clinical Modality Transfer**

To preserve distribution-free coverage under distribution shift, conformal prediction sets expand until they contain nearly all diagnostic classes, destroying clinical utility.

> * **Hypothesis (H\_1):** Conformal prediction calibrated on dermoscopy guarantees nominal 90% coverage on clinical photos only by inflating the mean prediction set size beyond the threshold of clinical utility (\>3 classes in a 6-class problem).  
> * **Dataset:** Calibration: ISIC 2020\. Evaluation: PAD-UFES-20.  
> * **Baseline:** Standard softmax thresholding at fixed confidence.  
> * **Intervention:** Split-conformal prediction utilizing adaptive prediction sets (APS) and regularized prediction sets (RAPS).  
> * **Metrics:** Marginal Coverage, Mean Set Size, Frequency of Singleton Sets, Empty Set Rate.  
> * **Falsification Condition (H\_0):** Nominal coverage is maintained on the target domain while preserving average prediction set sizes below 1.5 classes.  
> * **Scientific Contribution if Positive:** Quantifies the operational cost of formal statistical guarantees in transferring medical AI, proving that distribution-free methods can become diagnostically empty under shift.  
> * **Scientific Contribution if Negative:** Establishes that conformal calibration remains compact and clinically actionable across major imaging sensor transitions.

## **Section 8 — Federated Learning Candidate Research Questions**

The following eight candidate research questions evaluate federated learning by isolating phenomena unique to distributed optimization and decentralized data constraints.

### **RQ-FL1: Boundary Conditions of Site-Conditional Conformal Risk Control Under Partial Client Participation**

Transmitting raw patient calibration scores to a central coordinator violates data privacy; institutions can only transmit localized, aggregated risk curves. Under low client participation rates, empirical prior precision (n\_0) misestimates the global risk curve, causing severe undercoverage at unobserved small institutions.

> * **Client Heterogeneity Model:** Real institutional partitioning using FeTS-2022 (20 institutions with native scanner and sample-size variations).  
> * **Centralized Control:** Centralized conformal risk control with access to pooled patient data.  
> * **Baselines:** Pooled Federated CRC, Macro-threshold averaging, Full-participation Fed-CRC-Seg.  
> * **Intervention:** Varying the client participation fraction (C \\in \\\[span\_24\](start\_span)\[span\_24\](end\_span){0.2, 0.4, 0.7, 1.0\\}) during risk-curve aggregation.  
> * **Metrics:** Worst-site False Negative Rate (FNR), Proportion of violating institutions, Mean-worst coverage gap.  
> * **Falsification Condition (H\_0):** Worst-site FNR remains within the target budget (\\alpha \= 0.10) regardless of client subsampling rates down to C \= 0.2.  
> * **Reproducibility:** Fully reproducible on single GPU via pre-extracted FeTS validation tensors and Python simulation scripts.

### **RQ-FL2: Impact of Federated Aggregation on Worst-Client Selective Prediction**

Global parameter aggregation pulls client weights toward the population center, improving average classification but disrupting the sharp confidence ordering required for local selective triage.

> * **Why FL is Required:** Investigates the direct mathematical consequence of parameter aggregation across non-IID manifolds on localized uncertainty ranking.  
> * **Client Heterogeneity Model:** 6 distinct dermoscopic contributing centers partitioned from ISIC archives.  
> * **Centralized Control:** Centralized training on pooled data with identical total optimization steps.  
> * **Baselines:** Local-only training (no federation), FedAvg, FedProx.  
> * **Intervention:** Evaluating local model checkpoints before and after global parameter aggregation across 50 communication rounds.  
> * **Metrics:** Client-specific AUGRC, Worst-client AUGRC, Mean AUGRC, Inter-client AUGRC variance.  
> * **Falsification Condition (H\_0):** Global parameter aggregation monotonically improves or preserves AUGRC for all participating clients without exception.  
> * **Reproducibility:** High on Colab Pro using native PyTorch sequential client simulation.

### **RQ-FL3: Sample-Complexity Wall for Site-Conditional Calibration in 2D Medical FL**

Privacy limits prohibit transferring validation images; small rural clinics must balance local empirical estimation against shrinkage toward an aggregated global prior. For institutions with local sample sizes n\_k \< 30, calibration variance is so extreme that shrinkage either fails to prevent violations or collapses to pooled calibration.

> * **Client Heterogeneity Model:** Controlled simulation of 8 client clinics with Pareto-distributed sample sizes (n\_k \\in \[10, 1000\]) and graded photometric shifts.  
> * **Centralized Control:** Fully pooled calibration set with complete data sharing.  
> * **Baselines:** Local-only thresholding, Naive pooled global thresholding.  
> * **Intervention:** Sweeping shrinkage precision parameter n\_0 across varying local institutional sample budgets.  
> * **Metrics:** Worst-client coverage violation rate, Threshold variance, Local sample efficiency.  
> * **Falsification Condition (H\_0):** Site-conditional shrinkage provides zero statistically significant coverage benefit over naive pooled calibration across all sample regimes (n\_k \\ge 10).  
> * **Reproducibility:** High; executes in minutes using pre-computed model outputs.

### **RQ-FL4: Feature Normalization Localization (FedBN) versus Global Model Calibration**

FedBN restricts batch normalization statistics to local clients during training to resolve non-IID optimization divergence. Because it never synchronizes normalization statistics, the global model lacks canonical feature scaling, causing severe miscalibration when transferred to a novel clinical site.

> * **Why FL is Required:** Studies an algorithmic adaptation designed explicitly for non-IID federated communication.  
> * **Client Heterogeneity Model:** 4 simulated clinical centers with graded sensor shifts (following MedFL-Stress protocols).  
> * **Centralized Control:** Centralized model trained with Domain-Adversarial training.  
> * **Baselines:** Standard FedAvg, FedProx.  
> * **Intervention:** Freezing local normalization statistics versus federating running mean and variance parameters.  
> * **Metrics:** Unseen-client AUROC, Unseen-client ECE, Worst-client calibration error.  
> * **Falsification Condition (H\_0):** FedBN models display equal or superior calibration on completely unseen clinical test clients compared to standard FedAvg.  
> * **Reproducibility:** High on single-GPU Colab Pro.

### **RQ-FL5: Federated Parameter-Efficient Fine-Tuning (PEFT) and Worst-Client Calibration Disparity**

Parameter-efficient communication (transmitting low-rank adapter matrices A and B) is essential for edge-medical federation. Under class skew, low-rank parameter updates align with majority classes on large clients, causing adapter rank collapse and severe miscalibration on minority clients.

> * **Client Heterogeneity Model:** Multi-center dermoscopy partition with heavy prevalence skew across client nodes.  
> * **Centralized Control:** Centralized LoRA fine-tuning on pooled multi-center data.  
> * **Baselines:** Full-network FedAvg, Local-only LoRA tuning.  
> * **Intervention:** Factor-wise LoRA aggregation versus Product-space (FlexLoRA/SVD) aggregation.  
> * **Metrics:** Inter-client ECE spread, Worst-client ECE, Average F1-score, Gradient divergence norm.  
> * **Falsification Condition (H\_0):** Federated LoRA yields an inter-client calibration spread identical to or smaller than full-parameter federated training.  
> * **Reproducibility:** Moderate; requires careful implementation of SVD-based adapter merging.

### **RQ-FL6: Vulnerability of Federated Conformal Predictors to Adversarial Client Poisoning**

Central coordinators in healthcare federations cannot audit patient data directly to verify the integrity of transmitted empirical risk curves. Standard empirical Bayes shrinkage averages a poisoned curve into the prior, causing honest hospitals to under-segment critical clinical targets.

> * **Client Heterogeneity Model:** 10 simulated clinical clients, with 1 client executing Byzantine risk-curve manipulation.  
> * **Centralized Control:** Outlier-filtered centralized validation.  
> * **Baselines:** Standard non-robust risk-curve shrinkage (Fed-CRC-Seg).  
> * **Intervention:** Injection of artificially deflated empirical loss curves from the compromised client node.  
> * **Metrics:** Global violation rate across honest clients, Worst honest-client FNR, Attack detection rate.  
> * **Falsification Condition (H\_0):** The global threshold is inherently robust; injecting an adversarial risk curve alters honest-site coverage by less than 1 percentage point.  
> * **Reproducibility:** Extremely high; operates entirely on transmitted scalar risk arrays.

### **RQ-FL7: Client Drift in Self-Supervised Federated Pretraining and its Downstream Calibration Costs**

Contrastive parameter averaging under feature shift fragments the representation space, yielding representations that achieve acceptable linear separability but distorted softmax margins.

> * **Why FL is Required:** Evaluates whether distributed self-supervised learning introduces geometric distortions that persist through local downstream task tuning.  
> * **Client Heterogeneity Model:** 5 clinical client partitions exhibiting severe non-biological acquisition shifts.  
> * **Centralized Control:** Centralized SimCLR trained on identical pooled data.  
> * **Baselines:** Supervised ImageNet transfer, Supervised FedAvg.  
> * **Intervention:** Freezing the federated self-supervised encoder and training identical linear heads across local clients.  
> * **Metrics:** Downstream ECE, Maximum Calibration Error (MCE), AUGRC, Representation cosine similarity across clients.  
> * **Falsification Condition (H\_0):** Downstream calibration metrics for Fed-SSL match centralized SSL within standard error bounds (\\Delta\\text{ECE} \\le 0.01).  
> * **Reproducibility:** High compute demand; borderline for Colab Pro if trained from scratch.

### **RQ-FL8: Personalization versus Calibration Parity in Federated Medical Image Classification**

Personalization optimizes local discriminative accuracy on small sample sizes, leading to overconfident probability outputs and heightened inter-site calibration variance.

> * **Why FL is Required:** Investigates the trade-off between local adaptation and global standardization in multi-center healthcare collaborations.  
> * **Client Heterogeneity Model:** 6 distinct dermoscopic contributing centers from public archives.  
> * **Centralized Control:** Centralized multi-task learning with hospital-specific heads. \* **Baselines:** Pure Global FedAvg, Pure Local-only training.  
> * **Intervention:** Evaluating a spectrum of personalization: from shared global backbone with local head fine-tuning to FedRep.  
> * **Metrics:** Client-wise Accuracy, Client-wise ECE, Inter-client Calibration Disparity, Worst-client AUGRC.  
> * **Falsification Condition (H\_0):** Personalization monotonically decreases both classification error and calibration error (ECE) across all client sites simultaneously.  
> * **Reproducibility:** High on single-GPU Colab Pro.

## **Section 9 — Closest-Work Autopsy**

This section provides an adversarial autopsy of the closest published papers for the primary research directions, determining whether the proposed thesis questions are genuinely open or duplicate existing literature.

### **Autopsy 1: Dermoscopy Selective Classification Under Shift vs. Traub et al. (2024)**

In *"Overcoming Common Flaws in the Evaluation of Selective Classification Systems"* (NeurIPS 2024), Traub et al. established the mathematical flaws of standard selective prediction evaluation (AURC), defined five core requirements for multi-threshold metrics, proposed AUGRC, and benchmarked 13 confidence scoring functions across six general datasets, including CAMELYON-17 histopathology.

The proposed thesis adopts AUGRC as its diagnostic foundation but redirects the inquiry to physical clinical distribution shifts (dermoscopy transferred to smartphone photography, stratified Fitzpatrick skin tones) and evaluates whether post-hoc recalibration recovers selective ranking. This difference is scientifically meaningful because Traub et al. focused on metric formalization and general in-distribution benchmarking, leaving unexamined whether selective rankings invert under physical sensor shifts.

However, if the empirical rank-order of confidence estimators on external clinical test sets remains identical to their in-distribution baseline, the study risks being perceived as an incremental confirmation of Traub et al.'s findings on another dataset. The decision is **Strong Separation**, representing a distinct clinical domain-shift stress test built upon a rigorous methodological foundation.

### **Autopsy 2: Dermoscopy Selective Classification Under Shift vs. Kozachok et al. (2026)**

In *"Searching for Robust Augmentations to Improve Out-of-Domain Generalization in Dermoscopic Skin Cancer Classification"* (arXiv:2607.26765, July 2026), Kozachok et al. trained ConvNeXt-Large models across six dermoscopic sources (25,903 images) with contamination filtering (removing shared lesions across HAM10000 and MILK10k) and demonstrated an out-of-domain ROC-AUC gain of \+0.053 on held-out sources using sensor-modeled photometric augmentations.

The proposed thesis evaluates probability calibration, confidence ranking, selective classification (AUGRC), and automated clinical abstention under an identical contamination-filtered protocol. This difference is scientifically meaningful because high discriminative accuracy under domain shift does not guarantee reliable probabilities for automated triage; augmentations that maximize ROC-AUC can simultaneously distort predictive entropy, causing selective triage to fail.

The vulnerability is that Kozachok et al. have already established the contamination-filtering protocol and demonstrated the dominance of photometric augmentations, meaning the thesis could be viewed as a secondary metric evaluation. The decision is **Moderate Separation**, occupying an orthogonal metric space on top of an established training protocol.

### **Autopsy 3: Site-Conditional Conformal Risk Control vs. Fed-CRC-Seg (Shahid, 2026\)**

In *"When Average Calibration Fails: Site-Conditional Federated Conformal Risk Control"* (arXiv:2606.20115, June 2026), Nafis Fuad Shahid demonstrated that naive pooled conformal risk control satisfies marginal guarantees while violating coverage at 40% of institutions on FeTS-2022 3D brain tumor MRI, proved that aggregation weighting causes this failure, and proposed risk-curve shrinkage (n\_0=19) to restore institutional coverage.

The proposed thesis investigates the stability and boundary conditions of risk-curve shrinkage under partial client participation (client dropout during aggregation rounds), maps failure modes across structural versus photometric shifts, and constructs an accessible 2D analog. This difference is scientifically meaningful because Shahid assumed 100% client availability, whereas real-world distributed healthcare systems face intermittent connectivity, making it vital to establish whether partial participation destroys local statistical coverage.

However, Shahid already established the core failure mode and proposed the shrinkage mechanism; an undergraduate thesis exploring partial participation is an operational extension rather than a new algorithmic paradigm. The decision is **Moderate Separation**, representing an empirical replication and boundary condition analysis.

### **Autopsy 4: Shortcut Learning Recalibration vs. Kina & Petersen (2025)**

In *"Prevalence calibration as shortcut mitigation"* (arXiv:2609.07922, 2025), Kina & Petersen demonstrated that shortcut learning in chest radiographs (CheXpert and SIIM-ACR) can be interpreted as a calibration failure under group shift, proving that post-hoc recalibration adjusting output logits for demographic skew raises worst-group AUROC from 0.23 to 0.73 without retraining.

The proposed thesis tests whether prevalence recalibration holds when spurious shortcuts are physical acquisition artifacts (such as dermatoscope vignette rings) rather than demographic base-rate disparities, evaluating its impact on selective referral. This difference is scientifically meaningful because base-rate recalibration alters class priors but cannot resolve non-biological image feature correlations that directly mislead convolutional extractors.

Nevertheless, claiming that post-hoc recalibration mitigates shortcuts is no longer novel; Kina & Petersen have already established the core principle. The decision is **Weak Separation**, as it represents a near duplicate of conceptual insight differing primarily in imaging modality.

### **Autopsy 5: Federated Vision-Language Model Adaptation vs. arXiv:2609.02101 (2026)**

In *"Federated LoRA Adaptation of BiomedCLIP Across Four International Chest X-Ray Cohorts"* (arXiv:2609.02101, 2026), the authors federated parameter-efficient LoRA tuning of BiomedCLIP across four international chest X-ray cohorts, demonstrating that product-space (FlexLoRA) aggregation prevents a 0.097 AUC drop observed with naive factor averaging.

The proposed thesis evaluates calibration and uncertainty quantification metrics on top of the exact same federated BiomedCLIP cohort setup. While aggregating adapters across institutions may preserve classification rankings while distorting predictive confidence, the engineering pipeline, datasets, and federated PEFT aggregation mechanics are already occupied by arXiv:2609.02101. Merely computing calibration curves on top of another group's published pipeline represents a superficial contribution. The decision is **Essentially Duplicate / Superficial Extension**, warranting rejection.

## **Section 10 — Feasibility and Compute Audit**

All experimental designs must be validated against the constraints of an undergraduate research environment: a single-GPU Google Colab Pro subscription (NVIDIA T4 with 16 GB VRAM; periodic V100/A100 allocations) and a local development workstation (AMD Ryzen 5 5600G, 8 GB RAM, integrated graphics). Large proprietary foundation models, expensive commercial APIs, and multi-node clusters are excluded.

For Candidate M1 (Dermoscopy Selective Classification), the training data consists of resized 256x256 JPEGs from ISIC 2020 and ISIC 2019, totaling approximately 12 GB of storage, which fits within standard Google Drive allocations. Using DenseNet-121 or ResNet-18 at batch size 64 in FP16 mixed precision, peak VRAM consumption is 3.8 GB on an NVIDIA T4, well below the 16 GB ceiling. Training requires approximately 45 seconds per epoch; a 20-epoch training run completes in 15 minutes.

The experimental matrix comprises three random seeds across two architectures (DenseNet-121 and ResNet-18), requiring six primary runs totaling 1.5 GPU hours. Adding a five-member deep ensemble requires five additional runs totaling 1.25 GPU hours. Inference-only post-hoc calibration, Monte Carlo Dropout (15 forward passes), and AUGRC evaluation across test sets require approximately 2.5 GPU hours. The entire experimental budget for Candidate M1 is roughly 5.25 GPU hours, fitting within a single Colab Pro compute window.

For Candidate FL1 (Site-Conditional Conformal Risk Control), two implementations are possible. Training a 3D U-Net from scratch on FeTS-2022 3D volumes (128x128x128 patches) exceeds single-GPU Colab Pro session limits, triggering a compute failure (kill gate).

However, evaluating conformal risk control on pre-computed validation feature tensors and prediction volumes requires only inference and empirical risk-curve optimization. Computing risk curves across 20 institutions and sweeping shrinkage parameters (n\_0) requires under 2.0 GPU hours.

Alternatively, constructing a 2D dermoscopy analog with eight simulated client clinics using ResNet-18 requires 30 communication rounds with one local epoch per round. Simulating eight clients sequentially takes approximately 100 minutes per federated run. Across four participation fractions (C \\in \\{0.2, 0.4, 0.7, 1.0\\}) and three random seeds (12 simulations), total compute reaches approximately 20.4 GPU hours, which can be completed across three to four Colab Pro sessions.

## **Section 11 — Top Candidate Research Designs**

The following detailed experimental designs represent the two surviving candidates that satisfy all feasibility, novelty, and compute gates.

### **Candidate 1 — Leakage-Resistant Audit of Selective Classification Under Clinical Shift**

> * **Exact Research Question:** Does post-hoc confidence scoring preserve sample-level risk-coverage ordering (AUGRC) under physical acquisition and skin-tone shift in dermoscopy, or does selective prediction fail where automated referral is required?  
> * **Concrete Failure Mode:** A dermatological triage system is configured with an abstention threshold to refer high-risk cases to specialists while autonomously diagnosing low-risk cases. Under sensor shift (such as smartphone images from external clinics), the model's confidence ranking inverts: it becomes overconfident on out-of-distribution diagnostic errors and underconfident on simple in-distribution cases. As a result, the selective risk among retained predictions increases, rendering automated referral unsafe.  
> * **Why it Matters:** Clinical deployment of AI requires safe degradation under uncertainty. If selective classification systems fail to identify their own errors under sensor and demographic shifts, they cannot be safely integrated into clinical triage workflows.  
> * **Closest Existing Work:** Traub et al., NeurIPS 2024 (AUGRC formulation); Kozachok et al., 2026 (Augmentation for OOD dermoscopy); Kina & Petersen, 2025 (Shortcut calibration).  
> * **What Existing Work Already Establishes:** AURC is structurally flawed for cross-model selective evaluation; photometric transformations improve OOD discriminative accuracy; post-hoc calibration can resolve demographic prevalence shift.  
> * **Remaining Unanswered Question:** Does an intervention that improves OOD discriminative accuracy (photometric augmentation) or fixes prevalence shift actually restore multi-threshold selective ranking (AUGRC) on novel acquisition devices, or does sample-level error ordering degrade regardless of calibration?  
> * **Dataset:**  
  * *Training & Validation:* ISIC 2020 (33,126 images) filtered using official duplicate lists (removing 425 duplicates) and partitioned strictly by patient\_id (80% train / 20% val).  
  * *External Test Sets:* PAD-UFES-20 (2,298 smartphone images, clinical camera shift) and DDI (656 images, Fitzpatrick skin tone shift).  
> * **Model:** DenseNet-121 and ResNet-18 initialized with ImageNet-1k pretrained weights.  
> * **Baselines:**  
  1. Uncalibrated Maximum Softmax Probability (MSP).  
  2. Post-Hoc Temperature Scaling (fitted on clean validation data).  
  3. Monte Carlo Dropout (15 forward passes at test time).  
  4. 5-Member Deep Ensemble (gold standard uncertainty control).  
> * **Experimental Design:** Models are trained on patient-partitioned ISIC data. Evaluated across three distinct test environments: (i) Clean in-distribution patient-held-out test, (ii) PAD-UFES-20 (sensor shift), and (iii) DDI (skin-tone shift). Selective classification is audited by computing generalized risk across all rejection thresholds \\tau \\in \[0, 1\].  
> * **Metrics:** AUGRC (primary), AURC, ECE, Brier Score, Selective Risk at fixed coverages (70%, 80%, 90%), and Subgroup AUGRC across Fitzpatrick tiers.  
> * **Leakage Controls:** Strict patient-level grouping (patient\_id); elimination of the 425 ISIC 2020 duplicates; verification that HAM10000 images are not duplicated into test folds; augmentations generated strictly on the fly post-partitioning.  
> * **Hypothesis (H\_1):** Selective prediction performance (AUGRC) degrades significantly under physical sensor shift (p \< 0.001), and standard temperature scaling yields no statistically significant improvement in AUGRC because it applies a monotonic logit scaling that cannot reverse incorrect ranking orders.  
> * **Falsification Condition (H\_0):** Post-hoc temperature scaling preserves the in-distribution AUGRC on PAD-UFES-20 and DDI within a 2% margin (\\Delta\\text{AUGRC} \\le 0.02, p \> 0.05).  
> * **Negative-Result Value:** A null result proves that post-hoc calibrated confidence scores are surprisingly stable across camera and demographic shifts in dermatology, demonstrating that standard calibrators provide reliable triage safety nets.  
> * **Compute Estimate:** \~5.25 GPU hours on NVIDIA T4. Completely Colab Pro feasible.  
> * **Main Implementation Risks:** Poor alignment between ISIC 2020 binary diagnostic labels and multi-class PAD-UFES / DDI labels (mitigated by collapsing to Malignant vs. Benign binary triage classification).  
> * **Novelty Confidence:** Medium-High.  
> * **Evidence Confidence:** High.  
> * **Verdict:** **PROCEED TO PILOT**.

### **Candidate 2 — Boundary Conditions of Federated Conformal Risk Control**

> * **Exact Research Question:** How resilient is site-conditional federated conformal risk control to partial client participation, and at what local sample threshold does shrinkage fail to prevent worst-site safety violations?  
> * **Concrete Failure Mode:** A federated medical consortium implements risk-curve shrinkage to prevent marginal calibration from violating coverage at small institutions. During deployment, communication dropouts mean only a fraction of hospitals participate per round. The central server aggregates an incomplete risk prior, resulting in coverage collapse and missed diagnoses at non-participating clinics.  
> * **Why it Matters:** Formal statistical safety guarantees (conformal bounds) are meaningless if they collapse under routine distributed systems phenomena like client dropout and intermittent connectivity.  
> * **Closest Existing Work:** Shahid, arXiv:2606.20115 (Fed-CRC-Seg); Lu et al., 2025 (Federated Conformal Prediction).  
> * **What Existing Work Already Establishes:** Pooled conformal calibration violates coverage at 40% of sites on FeTS-2022; empirical Bayes risk-curve shrinkage with n\_0=19 resolves violations under full participation.  
> * **Remaining Unanswered Question:** Shahid assumes 100% client availability. Does the shrinkage guarantee hold when client participation drops to realistic levels (C \\in \[0.2, 0.5\]), and what is the minimum local validation sample size n\_k required for an institution to benefit from federation?  
> * **Dataset:**  
  * *Option A (Primary):* Pre-computed validation predictions and feature tensors from FeTS-2022 (20 institutions, native site partitions).  
  * *Option B (2D Accessible Analog):* Multi-center ISIC dermoscopy partitioned into 8 client centers with graded sensor shifts.  
> * **Model:** Pretrained 3D U-Net features (for FeTS) or ResNet-18 (for 2D analog).  
> * **Baselines:** Naive Pooled Federated CRC, Unweighted Site-Average CRC, Full-Participation Fed-CRC-Seg.  
> * **Experimental Design:** Simulate federated calibration rounds where clients communicate empirical risk curves \\hat{R}\_k(\\lambda). Systematically vary client availability C \\in \\{0.2, 0.4, 0.7, 1.0\\} across 50 Monte Carlo dropout trials. Measure coverage violation rates on both participating and non-participating clients.  
> * **Metrics:** Worst-Site False Negative Rate (FNR), Proportion of violating institutions (\> \\alpha), Mean-worst coverage gap, Required prior precision n\_0.  
> * **Leakage Controls:** Rigid separation of calibration sets from testing sets within each institutional silo; no raw images or volume scores transmitted across silos.  
> * **Hypothesis (H\_1):** Client participation rates below C \= 0.5 cause the empirical risk prior to diverge, doubling the worst-site violation rate compared to full participation.  
> * **Falsification Condition (H\_0):** Worst-site coverage violations remain statistically invariant (\\le 1 additional violation across 20 institutions) for all participation rates C \\ge 0.2.  
> * **Negative-Result Value:** Establishes that federated risk-curve shrinkage is robust to communication dropouts, confirming that distributed conformal guarantees can be deployed without strict participation quotas.  
> * **Compute Estimate:** \~2.0 GPU hours for inference and risk-curve optimization on pre-computed predictions.  
> * **Main Implementation Risks:** Synapse administrative delay in approving FeTS-2022 dataset access (mitigated by implementing the 2D dermoscopy analog first).  
> * **Novelty Confidence:** Medium.  
> * **Evidence Confidence:** High.  
> * **Verdict:** \**RESERVE*\*.

## **Section 12 — Medical Imaging versus Federated Learning**

Evaluating Medical Image Analysis against Federated Learning involves distinct methodological and logistical trade-offs.

| Dimension | Medical Image Analysis (Candidate M1) | Federated Learning (Candidate FL1) |
| :---- | :---- | :---- |
| Research-Question Depth | High: Investigates the breakdown of selective prediction ranking under physical sensor shifts. | Moderate: Investigates operational boundary conditions of an existing distributed statistical guarantee. |
| Current Research Activity | Extremely Active: Post-hoc reliability and selective prediction are actively published in 2024–2026. | Extremely Active: Conformal prediction in FL is an emerging topic (2025–2026). |
| Crowding / Saturation | High on general calibration; Low on AUGRC multi-threshold selective evaluations under physical sensor shifts. | High on standard optimization (FedAvg/FedProx); Low on federated conformal risk control. |
| Public Dataset Availability | Excellent: Directly downloadable public archives (ISIC 2020, PAD-UFES-20, DDI). | Limited: FeTS-2022 requires manual Synapse approval; most public datasets lack natural site labels. |
| Baseline Availability | Complete: torchvision backbones, scikit-learn, and public AUGRC metric code. | Good: Fed-CRC-Seg code is public on GitHub; Flower framework provides simulation scaffolding. |
| Reproducibility | High: Deterministic data loaders, public image files, fixed seeds. | Moderate: Distributed simulation requires strict seed handling across virtual client processes. |
| Compute Burden | Minimal: \~5.25 total GPU hours. Fits easily within single Colab sessions. | Low–Moderate: \~2.0 hours for calibration-only FeTS; \~20 hours for full 2D training simulations. |
| Implementation Complexity | Low–Moderate: Standard PyTorch training pipelines and metric scripts. | Moderate–High: Requires configuring multi-client simulation loops and handling shrinkage math. |
| Leakage Risk | High operational risk, but completely auditable via metadata (p\[span\_128\](start\_span)\[span\_128\](end\_span)atient\_id, duplicate lists). | Moderate: Client partitions must remain strictly disjoint; validation sets must not leak across rounds. |
| Evaluation Difficulty | Low: Closed-set classification, deterministic thresholds, standard ROC/AUGRC integrations. | Moderate: Statistical coverage bounds require bootstrap confidence intervals over multiple site partitions. |
| Undergraduate Feasibility | High: Can be reliably executed and analyzed by an undergraduate team in 3–4 months. | Moderate: Requires diligence to avoid the distributed-systems infrastructure trap. |
| Potential Empirical Contribution | Strong empirical safety audit that exposes the limitations of clinical automated triage. | Replication and characterization study that establishes operational boundary conditions for FL. |
| Risk of Becoming Generic | Low, provided that the AUGRC metric and physical sensor shifts are strictly enforced. | High if the project abandons conformal calibration and defaults to comparing FedAvg vs. FedProx. |
| Risk of Being a "Model Comparison" | Low: The independent variable is the confidence estimator and domain shift, not the architecture. | Low: The independent variable is the participation rate and local sample size. |
| Risk of Superficial Novelty | Low: Formal evaluation protocol directly targets an unaddressed clinical safety failure mode. | Moderate: Risk of being perceived as a minor hyperparameter extension of Fed-CRC-Seg. |
| Negative-Result Value | High: A finding that selective prediction is invariant to sensor shift is a clinically important result. | High: A finding that partial participation does not degrade worst-site coverage simplifies FL deployments. |

The medical imaging track offers superior dataset accessibility and lower implementation risk, relying entirely on open, credential-free archives and established single-GPU vision libraries. Conversely, federated learning addresses a sophisticated systems-statistical intersection but requires navigating access approvals for FeTS-2022 or defending a simulated 2D federation.

## **Section 13 — Comparison With Existing Trustworthy-VLM Direction**

The researcher is concurrently evaluating an alternative thesis topic in multimodal foundations: investigating whether explicit conflict verbalization (prompting a vision-language model to articulate contradictions between conflicting visual and textual premises before answering) causally changes which source the model arbitrates toward, or merely rationalizes an existing latent modality preference.

| Dimension | Medical Imaging (Candidate M1) | Federated Learning (Candidate FL1) | Trustworthy VLM Direction (Held Candidate) |
| :---- | :---- | :---- | :---- |
| Research-Question Clarity | High: Tests whether selective classification ranking degrades under physical sensor shift. | Moderate: Tests whether partial participation degrades worst-site conformal coverage. | High: Crisp causal question adjudicating between mechanistic arbitration and post-hoc rationalization. |
| Literature Saturation | High on calibration; Low on selective prediction under physical dermoscopic shifts. | High on standard optimization; Low on federated conformal risk control. | Moderate: Multimodal conflict is active, but causal verbalization remains unmapped. |
| Novelty Confidence | Medium: Primarily an empirical safety audit using established metrics and datasets. | Medium: Operational characterization and replication of Shahid (2026). | High: Investigates an unaddressed mechanistic phenomenon in transformer reasoning. |
| Experimental Controllability | Moderate: Real clinical distribution shifts contain uncontrollable nuisance confounds. | Moderate: Confounded by natural variance in institutional sample sizes and protocols. | High: Synthetic contradiction injection permits precise, paired counterfactual control. |
| Dataset Accessibility | High: ISIC 2020 and PAD-UFES-20 are directly downloadable without credentials. | Low–Moderate: FeTS-2022 requires manual Synapse challenge approval. | High: Open multimodal benchmarks (e.g., GMAI-MMBench, SLAKE) are immediately usable. |
| Baseline Accessibility | High: Standard torchvision models and public AUGRC metric code. | High: Fed-CRC-Seg code is public on GitHub. | High: Open-weights VLMs (Qwen2.5-VL-7B 4-bit, Qwen3VL-2B) run out of the box. |
| Compute Feasibility | High: \~5.25 total GPU hours on single T4. | High: \~2.0 GPU hours on pre-computed FeTS features. | High: Inference-only evaluation fits comfortably inside single-GPU Colab Pro. |
| Leakage Risk | High: Requires strict patient-level deduplication and cross-release filtering. | Moderate: Requires rigid silo separation of calibration splits. | Moderate: Benchmark question contamination in pretraining corpora must be audited. |
| Evaluation Reliability | High: Evaluated against objective biopsy ground truth and AUGRC integrations. | High: Evaluated against exact empirical coverage bounds. | High if restricted to closed-set choices; Low if relying on LLM-as-a-judge. |
| Implementation Burden | Moderate: Requires data cleaning, caching, and model training pipelines. | Moderate–High: Requires distributed simulation logic and shrinkage math. | Low–Moderate: Focuses on prompt pipelines, generation parsing, and statistical testing. |
| Undergraduate Feasibility | High: Standard applied computer vision engineering workflow. | Moderate: Risk of getting bogged down in FL framework orchestration. | High: Fast turnaround; highly modular for a small undergraduate team. |
| Potential Scientific Contribution | Empirical safety benchmark informing automated clinical triage deployment. | Operational boundary condition analysis for distributed medical risk control. | Mechanistic insight into how multimodal models resolve conflicting evidence. |
| Risk of Becoming Application-Only | High: Evaluators may dismiss the work as a straightforward application of CNNs. | Moderate: Risk of being perceived as a secondary benchmarking exercise. | Low: Targets a core theoretical question in foundation model reasoning. |
| Negative-Result Value | High: Confirming selective ranking stability provides reassurance for clinical AI. | High: Proving robustness to dropout simplifies distributed hospital deployments. | Exceptional: Proving verbalization is inert demonstrates that explanations are post-hoc. |

The trustworthy VLM direction possesses higher conceptual novelty and lower data-hygiene risks than both medical tracks. The medical imaging candidate (M1), while technically grounded and Colab-feasible, remains an empirical reliability audit rather than a mechanistic discovery. If the primary goal is conceptual originality and mechanistic insight into modern multimodal architectures, the VLM direction is structurally superior. If the goal is a concrete clinical safety audit backed by biopsy-grounded ground truth, Candidate M1 represents a defensible option.

## **Section 14 — Final Verdicts**

The research directions are classified into clear operational verdicts based on the adversarial audit:

Candidate M1 (Leakage-Resistant Dermoscopy Selective Classification Under Shift) is assigned **PROCEED TO PILOT**. The failure mode is clinically meaningful, datasets (ISIC 2020, PAD-UFES-20, DDI) are verified and accessible without credentials, the evaluation metric (AUGRC) is mathematically established, the compute footprint (\<6 GPU hours) fits within single Colab Pro sessions, and a negative result provides immediate scientific value regarding clinical triage safety.

Candidate FL1 (Boundary Conditions of Federated Conformal Risk Control) is assigned **RESERVE**. While site-conditional risk control on real multi-institutional data is an active topic, the core phenomenon was demonstrated by Fed-CRC-Seg in 2026\. Furthermore, FeTS-2022 access requires manual administrative review on Synapse. This topic should be reconsidered only if FeTS-2022 approval is granted immediately or if the 2D dermoscopy analog passes its initial falsification test.

Candidate M2 (Shortcut Learning Recalibration vs. Acquisition Invariance) is assigned **RESERVE**. While evaluating post-hoc recalibration on physical artifacts is meaningful, recent work by Kina & Petersen (2025) heavily shadows the core conceptual insight, reducing the potential novelty of the contribution.

All generic architectural comparisons (such as "CNN vs. Transformer on HAM10000/ChestX-ray") are **REJECTED** as saturated engineering exercises devoid of research-question depth.

All standard FL algorithmic comparisons (such as "FedAvg vs. FedProx under Dirichlet Skew") are **REJECTED** as methodologically invalid simulations that fail to reflect authentic clinical heterogeneity.

Federated Medical Vision-Language Model Adaptation is **REJECTED** because the exact engineering pipeline, datasets, and LoRA aggregation mechanics are already occupied by arXiv:2609.02101, leaving no defensible undergraduate niche.

## **Section 15 — 60–90 Minute Falsification Task**

Before committing months of research effort to Candidate M1 (Selective Classification Under Clinical Shift), the researcher must execute a targeted falsification task designed to test the core experimental premise: that acquisition sensor shift degrades selective classification ranking.

The objective is to evaluate whether an off-the-shelf pretrained vision backbone exhibits selective ranking degradation (AUGRC collapse) when transferred from dermoscopy to clinical smartphone images, and whether post-hoc temperature scaling fails to restore this ranking.

The falsification protocol comprises four sequential steps:

First, conduct a dataset hygiene and metadata smoke test within minutes 00 to 20\. Download the official ISIC 2020 metadata CSV and the PAD-UFES-20 metadata CSV. Programmatically verify that patient\_id exists for all training rows in ISIC 2020, load the official ISIC 2020 duplicate list (425 images), and verify that deduplication scripts correctly isolate unique lesions. Confirm that the diagnostic labels from both archives can be mapped into a shared binary triage task: Malignant (Melanoma, Basal Cell Carcinoma, Squamous Cell Carcinoma) versus Benign (Nevus, Seborrheic Keratosis).

Second, execute a zero-cost feature inference loop within minutes 20 to 50\. Open a Google Colab Pro notebook running on a standard GPU instance. Load an ImageNet-pretrained ResNet-18 via torchvision.models without retraining. Pass 200 random images from the clean ISIC 2020 validation split and 200 images from the PAD-UFES-20 clinical smartphone test set through the frozen network to extract baseline softmax logits.

Third, compute AUGRC and selective risk within minutes 50 to 75\. Fit a single temperature parameter T via negative log-likelihood minimization on the 200 ISIC validation logits using standard numerical optimization. Apply this temperature parameter to scale the logits of the PAD-UFES-20 set. Using the public AUGRC implementation from Traub et al. (NeurIPS 2024), compute the Area Under the Generalized Risk-Coverage curve for both in-domain validation and out-of-domain test sets, and calculate the selective risk at 80% coverage.

Fourth, apply the decision rules within minutes 75 to 90\.

The Kill Rule triggers if the selective risk of uncalibrated ResNet-18 on PAD-UFES-20 at 80% coverage does not increase relative to in-domain validation, or if temperature scaling completely restores the out-of-domain risk-coverage curve to within 1% of in-domain performance. If this occurs, the experimental premise is falsified: selective ranking does not break under sensor shift, temperature scaling is already sufficient, and the topic should be killed immediately in favor of the held trustworthy VLM research direction.

The Thrive Rule triggers if out-of-domain selective risk inflates substantially and post-hoc temperature scaling fails to reverse sample misranking (demonstrating AUGRC collapse). This confirms that the failure mode is real, reproducible, and ready for full thesis investigation.

#### **Works cited**

1\. Overcoming Common Flaws in the Evaluation of Selective ... \- NIPS, https://proceedings.neurips.cc/paper\_files/paper/2024/file/047c84ec50bd8ea29349b996fc64af4b-Paper-Conference.pdf 2\. Site-Conditional Federated Conformal Risk Control \- arXiv, https://arxiv.org/pdf/2606.20115 3\. Searching for Robust Augmentations to Improve Out-of-Domain, https://arxiv.org/html/2607.26765v2 4\. (PDF) Uncovering and Correcting Shortcut Learning in Machine, https://www.researchgate.net/publication/357344560\_Uncovering\_and\_Correcting\_Shortcut\_Learning\_in\_Machine\_Learning\_Models\_for\_Skin\_Cancer\_Diagnosis 5\. Overcoming Common Flaws in the Evaluation of Selective ... \- arXiv, https://arxiv.org/abs/2407.01032 6\. Federated Learning: Distributed AI in the Age | MI \- 超智諮詢, https://www.meta-intelligence.tech/en/insight-federated-learning 7\. Prevalence calibration as shortcut mitigation \- arXiv, https://arxiv.org/html/2609.07922v1 8\. Build a strategy from scratch \- Flower Framework, https://flower.ai/docs/framework/1.20/en/tutorial-series-build-a-strategy-from-scratch-pytorch.html 9\. Run simulations \- Flower Framework, https://flower.ai/docs/framework/how-to-run-simulations.html 10\. Privacy-Preserving ML in 2026 — Federated Learning / Flower, https://labhub.hopto.org/blog/culture/2026-05-16-privacy-preserving-ml-2026-federated-learning-flower-nvidia-flare-opacus-zama-concrete-openmined-pysyft-deep-dive?lang=en 11\. \[core\] Slow performance and probable memory leak with iterative, https://github.com/ray-project/ray/issues/31961 12\. MedFL-Stress: A Systematic Robustness Evaluation of Federated, https://arxiv.org/abs/2605.09025 13\. Federated Supervised Finetuning using Flower AI \- Medium, https://medium.com/mitb-for-all/how-to-train-your-llm-simultaneously-with-10-different-teachers-ba556d4ed2c1