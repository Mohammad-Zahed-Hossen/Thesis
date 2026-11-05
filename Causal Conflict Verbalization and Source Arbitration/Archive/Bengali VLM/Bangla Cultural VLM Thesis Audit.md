# **Research Evaluation and Field Mapping Report: Evidence-Grounded Selective Prediction for Reliable Bangla Cultural Vision-Language Models**

## **Executive Finding**

The proposed research field, provisionally titled "Evidence-Grounded Selective Prediction for Reliable Bangla Cultural Vision-Language Models," does not constitute a defensible, standalone Computer Science and Engineering thesis in its current formulation. The proposal conflates three orthogonal technical mechanisms: multimodal confidence calibration, visual grounding verification, and external retrieval-augmented generation (RAG). By attempting to assemble these components across a regional linguistic and cultural benchmark, the proposed topic risks being evaluated as an engineering pipeline or a localized dataset substitution rather than a fundamental scientific contribution.

A systematic audit of the 2024–2026 multimodal literature reveals that the general algorithmic foundations of the proposal are already occupied. Selective prediction via localized visual evidence was formalized by Rodriguez and Rohrbach in SIEVES (April 2026); contrastive visual reliance calibration was established by Khanmohammadi et al. in BICR (May 2026); and distribution-free evidence acquisition under abstention was solved by Xu et al. in BCEA (June 2026).

Furthermore, introducing an external cultural retrieval component creates an immediate methodological hazard: external text passages routinely leak the ground-truth entity name verbatim, converting the task from visual entity identification into reading comprehension and corrupting visual calibration measurements.

The field becomes scientifically viable only if it is reformulated from a constructive system build into a controlled diagnostic audit. Specifically, the research must isolate whether localized cultural entities induce a distinct distribution shift where language priors systematically override visual evidence, and whether parameter-free or probe-based visual grounding signals can predict model failure better than standard logit or verbal confidence baselines without external retrieval.

If bounded within an inference-only framework on compact open-weight models such as Qwen2.5-VL-3B under Google Colab Pro constraints, the topic can yield a publishable diagnostic evaluation.

However, when benchmarked against the researcher's existing department proposals—which possess verified synthetic-to-natural interventions and zero-leakage test harnesses—this candidate carries higher annotation overhead, greater leakage risk, and lower mechanistic depth.

## **1\. Research Landscape**

Multimodal vision-language models (VLMs) and multimodal large language models (MLLMs) have transitioned from raw parameter scaling and static benchmark evaluation toward deployment reliability, epistemic restraint, and behavioral trustworthiness. Standard autoregressive VLMs frequently generate fluent, grammatically flawless responses that are factually unsupported by visual evidence, a pathology broadly categorized under visual hallucination and cross-modal miscalibration. In high-stakes, safety-critical, or culturally localized environments, forced answering introduces severe systemic risks. As a consequence, selective prediction—the framework wherein a model is equipped with a selection function g(x) \\in \\{0, 1\\} that decides whether to answer or abstain based on an uncertainty threshold \\tau—has become an active area of investigation in multimodal machine learning.

Concurrently, the evaluation of vision-language architectures has expanded globally to expose severe geographic and cultural imbalances. Standard foundation models are pretrained predominantly on Western, English-centric image-text corpora scraped from the public web. When exposed to culturally specific artifacts, traditional regional attire, indigenous culinary dishes, historical personalities, and geographically bounded rituals, VLMs exhibit acute performance degradation.

Recent regional benchmarks such as BanglaVerse and BanglaProtha demonstrate that these failures stem not merely from tokenizer vocabulary gaps, but from missing cultural parametric world knowledge and deep visual-semantic misalignment, where the model defaults to high-frequency global concepts.

The intersection of these two paradigms—selective prediction for reliable decision-making and culturally localized multimodal understanding—defines the research territory of the candidate proposal. The central problem is determining whether an open-weight vision-language model can reliably quantify its own visual and epistemic limitations when reasoning about localized cultural entities, selectively abstaining when sensory or contextual evidence is insufficient.

## **2\. Selective Prediction Literature**

Selective prediction in classification dates back to Chow's canonical error-reject trade-off and was modernized for deep neural networks by Geifman and El-Yaniv. In modern multimodal settings, the primary objective is to maximize coverage \\mathcal{C} (the proportion of queries answered) subject to a user-defined risk tolerance \\mathcal{R} (the error rate among answered queries):

\\mathcal{C}(\\tau) \= \\mathbb{E}\_{(x, y) \\sim \\mathcal{D}} \[\\mathbf{1}(g(x) \\ge \\tau)\] \\mathcal{R}(\\tau) \= \\frac{\\mathbb{E}\_{(x, y) \\sim \\mathcal{D}} \[\\ell(f(x), y) \\cdot \\mathbf{1}(g(x) \\ge \\tau)\]}{\\mathcal{C}(\\tau)}

where f(x) denotes the predictive model, g(x) represents the selection function or confidence estimator, y is the ground-truth target, \\ell(\\cdot) is the task loss function, and \\tau is the operational threshold.

Historically, selective visual question answering (Selective VQA) evaluated closed-vocabulary classification heads using softmax output distributions. Whitehead et al. (ECCV 2022\) established that raw softmax scores from standard VQA architectures are poorly calibrated for selective answering, restricting models to answering fewer than 8% of queries on VQA v2 to maintain a 1% risk of error (C@1\\%). They demonstrated that training an auxiliary multimodal selection network to directly predict answer correctness tripled coverage at low error tolerances.

Dancette et al. (2023) extended this through peer-learning ensembles, optimizing selection functions across data splits without requiring additional manual annotations. Srinivasan et al. (ACL Findings 2024\) introduced ReCoVERR, targeting the converse failure mode: mitigating unnecessary abstention in vision-language reasoning by recovering cases where models were overly conservative.

The state of the art in generative selective VQA evaluates risk-coverage profiles via the Area Under the Risk-Coverage Curve (AURC) and the Area Under the Generalized Risk-Coverage Curve (AUGRC) formalized by Traub et al. (NeurIPS 2024), which eliminates baseline accuracy variance when comparing models. In generative MLLMs, selective prediction cannot rely on raw output sequence probabilities. Because generative decoders emit variable-length autoregressive text, sequence likelihoods decay exponentially with sequence length, confounding uncertainty with generation length.

Consequently, modern selective prediction for generative VLMs relies on length-normalized log-likelihoods, semantic entropy over sampled response clusters, external verification selectors, or split conformal risk control to establish rigorous, finite-sample statistical risk guarantees.

## **3\. Multimodal Calibration Literature**

Multimodal calibration evaluates whether a model's stated confidence matches its empirical likelihood of being correct across an evaluation cohort:

P(\\hat{Y} \= Y \\mid \\hat{P} \= p) \= p, \\quad \\forall p \\in \[0, 1\]

The standard empirical evaluation metrics include Expected Calibration Error (ECE), Brier Score (BS), and the Area Under the Receiver Operating Characteristic curve (AUROC) for discriminating between correct and incorrect outputs.

The literature establishes sharp boundaries regarding confidence signal efficacy in generative VLMs:

### **Verbalized Self-Reported Confidence**

Prompting a model to verbalize its confidence (for example, generating "Answer: \[X\], Confidence: 90%") fails across open and proprietary architectures. Xiong et al. (ICLR 2024\) demonstrated that verbalized confidence in large language models suffers from severe overconfidence, clustering heavily between 80% and 100% and reflecting human conversational patterns rather than Bayesian uncertainty.

In multimodal settings, Khanmohammadi et al. (ICAIF 2026\) evaluated verbal self-probing across five open-weight LVLMs and documented Expected Calibration Errors between 0.25 and 0.58. Their analysis revealed confident-error rates exceeding 85%, meaning that more than eight out of ten incorrect predictions were accompanied by self-reported confidence exceeding 0.80. Verbalized confidence is completely unsuitable as a primary selection function.

### **Token- and Logit-Based Confidence**

Maximum softmax probabilities and length-normalized average token log-likelihoods over the generated entity span provide a baseline, but remain vulnerable to post-training quantization and distribution shifts. Wieczorek et al. (EIML 2025 / arXiv:2602.13289) proved that post-training quantization (PTQ) severely degrades logit calibration in models such as Qwen2-VL-7B and Idefics3-8B, requiring explicit post-hoc calibration or auxiliary selection heads.

### **Semantic Uncertainty and Sampling Consistency**

Kuhn et al. (2023) established semantic entropy for language models, calculating predictive entropy over equivalence classes of generated strings to eliminate syntactic noise. While effective, semantic clustering requires generating 5 to 20 autoregressive trajectories per sample, increasing test-time compute requirements by an order of magnitude.

### **Internal Activation Probing**

Training lightweight linear or multilayer perceptron (MLP) probes on intermediate or final hidden states of frozen VLMs yields calibrated uncertainty estimates. Frameworks such as SAPLMA and BICR demonstrate that internal residual states retain linear representations of factual correctness that autoregressive decoding heads fail to express.

## **4\. Visual Grounding and Evidence Dependence**

A critical failure mode in vision-language models is visual ungroundedness: models produce fluent, confident, and correct answers driven entirely by language priors embedded in the LLM backbone, while visual tokens are largely ignored. In culturally localized tasks, this occurs when a model encounters a prompt such as "What traditional Bengali dessert is shown?" and predicts "Rasgulla" purely because it is the highest-frequency sweet in its pretraining corpus, without attending to discriminatory visual features.

To detect whether a model's prediction causally depends on visual evidence, the literature employs input perturbation and counterfactual intervention protocols:

### **Blank- and Masked-Image Controls**

Replacing the input image with a black, white, or mean-pixel canvas. If the model generates the identical entity prediction with comparable token likelihoods, the prediction is ungrounded and driven entirely by linguistic priors.

### **Cross-Modal Contrastive Ranking**

Khanmohammadi et al. (arXiv:2605.10893, May 2026\) introduced Blind-Image Contrastive Ranking (BICR). BICR extracts hidden states from a frozen VLM under two forward passes: once with the genuine image-question pair, and once with the image blacked out. A lightweight probe is trained with a pairwise ranking loss that penalizes higher confidence on the blind view. BICR demonstrated that conditioning confidence on visual reliance significantly outperforms standard logit baselines across VQA, medical imaging, and document benchmarks.

### **Counterfactual Image Substitution**

DualRead (arXiv:2609.06419, September 2026\) introduced Counterfactual Confidence Grounding AUC (CCG-AUC) for medical VLMs. By substituting the input image with a real hard-negative image that possesses a different reference label, the protocol evaluates whether model confidence drops when the answer flips from correct to incorrect. DualRead separates capability learning from confidence estimation by combining an answer commitment state (h^{\\text{close}}) with answer-conditioned visual pooling over image tokens (h^{\\text{evid}}), directly measuring visual-semantic alignment via cosine similarity:

\\alpha\_{i, j} \= \\frac{\\exp(\\cos(h\_i^{\\text{ans}}, v\_{i, j}) / \\kappa)}{\\sum\_k \\exp(\\cos(h\_i^{\\text{ans}}, v\_{i, k}) / \\kappa)}, \\quad h\_i^{\\text{evid}} \= \\sum\_j \\alpha\_{i, j} v\_{i, j}

These methodologies confirm that determining whether an answer is visually grounded is already a mature subfield. The remaining research challenge is not inventing a new grounding test, but determining whether visual grounding sensitivity alone is sufficient to identify failure when the visual tokens are fine-grained and culturally ambiguous.

## **5\. Evidence-Grounded Confidence**

The literature bifurcates "evidence" into intrinsic visual evidence (direct pixel observations) and extrinsic knowledge evidence (retrieved reference documents).

Intrinsic visual evidence scoring was formalized in SIEVES (Rodriguez & Rohrbach, arXiv:2604.25855, April 2026). SIEVES trains an auxiliary selector model to score the tuple of (\\text{question}, \\text{image}, \\t\[span\_102\](start\_span)\[span\_102\](end\_span)\[span\_112\](start\_span)\[span\_112\](end\_span)ext{reasoning}, \\text{answer}) along three orthogonal axes: answer correctness (c\_{\\text{corr}}), localization accuracy (c\_{\\text{loc}}, supervised via bounding-box intersection over ground truth), and crop-answer coherence (c\_{\\text{coh}}, whether the zoomed visual crop supports the claim). SIEVES demonstrated up to a 3\\times coverage improvement at low risk on out-of-distribution benchmarks (V\* Bench, VizWiz, AdVQA) without requiring internal model weights, operating entirely as a black-box verification module.

Extrinsic evidence modeling operates within Multimodal Retrieval-Augmented Generation (MM-RAG). Binz, Soudani, and Hasibi introduced LeMUQ (Learnable Multimodal Uncertainty Quantification, 2025/2026), which tracks token probability shifts under input modifications, such as dropping retrieved contexts or image features, encoding these shifts as tokens for a downstream uncertainty model. Large-scale cultural retrieval benchmarks such as M4-RAG (CVPR 2026; 80,000 pairs across 42 languages) and RAVENEA (ICLR 2026; 1,868 cultural instances with human-ranked Wikipedia documents) evaluate the impact of external text on culturally specific visual reasoning.

However, incorporating external cultural evidence into an undergraduate selective prediction pipeline introduces severe methodological hazards:

> * Answer Leakage: When an external document discussing a localized cultural entity (e.g., "Nakshi Kantha") is retrieved and provided to the model or selection function, the text almost always names the entity verbatim. The task then degenerates from visual entity identification into reading comprehension.  
> * Confounding Uncertainty: If the model abstains, one cannot disentangle whether the failure stemmed from perceptual misrecognition, retriever recall failure, or passage misinterpretation.  
> * Engineering Collapse: Building a dual multimodal retriever and verification pipeline shifts the thesis away from foundational AI/ML failure analysis into a software systems integration project.

## **6\. Multimodal Hallucination and Abstention**

Hallucination in MLLMs is defined as the generation of claims that are unfaithful to the visual context. Standard benchmarks evaluate object existence (POPE), visual illusions (HallusionBench), and object-attribute relationships in free-form generation (THRONE).

Li et al. (EMNLP 2024 Findings) conducted an extensive study on reference-free hallucination detection, demonstrating that supervised uncertainty quantification (SUQ) using internal token representations effectively identifies non-factual claims without external verification tools.

Pramono, Cai, and Kulkarni introduced TRAPSBench (COLM 2026, arXiv:2608.13167), proving that VLMs exhibit a severe "representation-output gap". Across 16 VLMs spanning five families (Qwen, Gemma, LLaVA), internal representations accurately encode when visual evidence is insufficient (linear probes achieve up to 0.91 AUROC on answerability decoding), yet autoregressive decoding suppresses this signal, leading to spontaneous abstention scores of only 0.292 under their Penalized Epistemic Calibration Score (PECS).

Xu et al. addressed this in "Look Again Before You Abstain: Budgeted Conformal Evidence Acquisition" (arXiv:2606.16667, June 2026). They demonstrated that while standard conformal prediction bounds hallucination below 5%, it forces models to abstain on over 80% of queries. By replacing binary abstention with a three-way decision—answer, abstain, or acquire visual evidence (zooming/cropping)—coverage can be preserved under distribution-free risk bounds, provided the acquisition policy is folded into the calibration score to maintain exchangeability.

Therefore, hallucination detection and selective prediction share near-identical mathematical formalisms. Claiming selective prediction as a novel framework without contrasting it against established hallucination detection benchmarks represents a major literature gap.

## **7\. Bengali/Bangla Cultural VLM Literature**

Bengali (Bangla) multimodal AI research has advanced rapidly through several core benchmarks:

### **BanglaVerse**

Sayeedi et al. (arXiv:2603.21165, August 2026; EMNLP 2026 Findings) introduced a culturally grounded benchmark built on 1,152 manually curated images spanning nine cultural domains: Culture, Food, History, Media & Movies, National Achievements, Nature, Personalities, Politics, and Sports.

The benchmark provides 20,727 VQA items and 10,368 captions expanded across four languages (Bangla, English, Hindi, Urdu) and five regional dialects (Barishal, Chittagong, Noakhali, Rangpur, Sylhet), totaling 32,247 evaluation artifacts.

Crucially, Sayeedi et al. conducted an error analysis revealing that the primary performance bottleneck across open and closed VLMs is missing cultural knowledge rather than visual perception alone. They documented that local entity and artifact misrecognition accounts for 42.6% of observed failures, establishing an empirical baseline for culturally induced hallucination.

### **BanglaProtha**

Fahim et al. (IEEE/CVF WACV 2026, pp. 1159–1169) presented a dedicated VQA dataset evaluating VLMs on underrepresented, long-tail Bengali cultural contexts. BanglaProtha features culturally rich imagery, questions formulated in native Bengali, and semantically similar multiple-choice distractors designed to prevent models from exploiting superficial language biases.

The authors demonstrated that open-weight VLMs struggle severely under fine-grained cultural distractors, defaulting to high-frequency global concepts.

### **KhatianDoc**

Nazi et al. (arXiv:2609.03597, September 2026\) benchmarked frontier VLMs on Bengali land records (RS Khatians) featuring the Ana-Ganda base-16 fraction system, documenting a complete reasoning floor where models scored 0% on complex domain-specific categories.

These studies confirm that cultural VLM degradation in Bengali is empirically verified. However, none of these benchmarks evaluate uncertainty calibration, risk-coverage trade-offs, internal state probing, or selective abstention mechanisms.

### **Critical Question: Does "Bangla" Create Real Scientific Novelty?**

To evaluate whether the Bengali setting provides scientific novelty, two competing claims must be contrasted:

> * Weak Claim: "Existing selective prediction methods have not been tested on Bengali cultural images." This claim represents superficial dataset substitution. Taking an established algorithm and evaluating it on a new language without uncovering a distinct failure mechanism does not meet top-tier CSE publication standards.  
> * Strong Claim: "Culturally specific entities create a measurable uncertainty and grounding failure mode that general-purpose calibration methods do not adequately capture." This claim is scientifically defensible only if empirical evidence demonstrates that cultural unfamiliarity induces a specific mechanistic failure.

The literature indicates that cultural unfamiliarity induces three distinct failure modes:

> 1. Language-Prior Dominance: When visual features of a regional artifact are underrepresented in pretraining, cross-modal attention shifts almost entirely to the language model's parametric text priors, causing the model to hallucinate common entities regardless of image content.  
> 2. Severe Representation-Output Suppression: As established in TRAPSBench, models may internally encode the ambiguity of an unfamiliar cultural scene, but instruction-tuning forces the autoregressive decoder to generate a confident guess rather than expressing epistemic restraint.  
> 3. Overconfidence on Semantically Close Cultural Distractors: Because fine-grained regional concepts share visual similarities (e.g., distinguishing different regional sweets or traditional sarees), softmax probabilities remain peaked on incorrect labels.

Therefore, the Bengali cultural context provides genuine scientific novelty only if it is leveraged as a diagnostic lens to expose and analyze these failure mechanisms, rather than treated as a routine benchmarking exercise.

## **8\. Dataset Landscape**

| Dataset | Year | Images | Questions / Items | Cultural Specificity | Entity Labels | Public Access | License | Splits Available | Leakage / Shortcut Risk | Suitable for Selective Prediction? |
| :---- | :---- | :---- | :---- | :---- | :---- | :---- | :---- | :---- | :---- | :---- |
| **BanglaVerse** | 2026 | 1,152 | 20,727 VQA, 10,368 Captions | Very High (9 Bengali cultural domains) | Implicit in QA pairs; gold answers provided | Public (Hugging Face / GitHub) | CC BY-NC-SA 4.0 / Research Only | Unofficial train/dev/test; needs stratification | Moderate: Repeated images across 9 dialects/languages | Yes (with strict image-level deduplication) |
| **BanglaProtha** | 2026 | \~1,200 | \~3,500 MCQA | High (Bengali traditions, attire, food) | Yes (structured MC options with fine distractors) | Public (GitHub: farhanishmam/BanglaProtha) | Open Research | Official test split released; dev split partial | Low: Distractors are semantically close, penalizing priors | Highly Suitable (MCQA provides clean discrete target space) |
| **CulturalVQA** | 2024 | 2,328 | 2,378 QA | High (Global: 11 countries, includes South Asia) | Yes | Public | CC BY 4.0 | Fixed train/val/test splits | Low | Suitable (serves as cross-cultural OOD baseline) |
| **CultureVLM** | 2025 | \>50,000 | \>100,000 | Broad (100+ countries, coarse regional) | Partial | Public | Academic Open | Standard splits | High: Web-scraped noisy labels | Moderate (too broad for local entity mechanics) |
| **M4-RAG** | 2026 | \>40,000 | \>80,000 | High (Multilingual RAG across 189 countries) | Context-grounded entities | Public | CC BY-SA 4.0 | Train/Dev/Test | Extreme: External text passages contain exact answer | Unsuitable for visual calibration; suitable for RAG |
| **POPE** | 2023 | \~3,000 | \~9,000 | Low (General MS-COCO objects) | Yes (Binary existence) | Public | MIT / Open | Standard splits | Negligible | Suitable only as generic non-cultural calibration anchor |

## **9\. Model Landscape**

Investigating selective prediction under Colab Pro constraints (single GPU, 16 GB VRAM envelope) requires models that natively support Bengali script, process visual inputs efficiently, and expose unnormalized output logits and intermediate hidden states.

| Model Candidate | Parameter Scale | Bengali Script / Tokenizer Fertility | Multimodal Architecture | 16 GB VRAM Colab Pro Feasibility | Logit / Activation Accessibility | Assessment & Suitability |
| :---- | :---- | :---- | :---- | :---- | :---- | :---- |
| **Qwen2-VL-2B-Instruct** | 2.2B | Excellent (Byte-level BPE, high Indic compression ratio) | ViT \+ Qwen2 LM backbone; native dynamic resolution | Runs natively in bfloat16 (\~4.5 GB VRAM); supports batch size \> 8 | Fully open weights; direct PyTorch hook access | Highly Suitable: Primary lightweight experimental workhorse |
| **Qwen2.5-VL-3B-Instruct** | 3.5B | Superior (Updated multilingual vocabulary, strong Indic OCR) | Dynamic resolution ViT \+ Qwen2.5 backbone | Runs comfortably in bfloat16 (\~7.5 GB VRAM); single-GPU inference | Fully open weights; direct hook access to all transformer layers | Optimal Primary Model: Balances cultural reasoning with strict Colab limits |
| **Qwen2.5-VL-7B-Instruct** | 7.6B | Superior | Dynamic ViT \+ Qwen2.5 backbone | Exceeds 16 GB in bfloat16; requires 4-bit quantization (BitsAndBytes) | Accessible via quantized hooks; backprop/probing slower | Secondary Model: Run in 4-bit inference only; risk of quantization-induced miscalibration |
| **Gemma-3-4B-IT** | 4.3B | Moderate (Good Indic coverage, higher fertility than Qwen) | SigLIP vision encoder \+ Gemma LM | Fits in bfloat16 (\~9.0 GB VRAM) on Colab T4/V100 | Fully accessible | Viable Cross-Family Baseline: Validates architectural generalization |
| **InternVL2-4B / InternVL3-8B** | 4.2B / 8.1B | Moderate (Optimized primarily for Chinese/English; Indic weaker) | InternViT \+ Hermit/Qwen LM | 4B fits in bfloat16; 8B requires 4-bit quantization | Accessible | Marginally Suitable: Weaker native Bengali cultural reasoning |
| **LLaVA-NeXT-7B** | 7.2B | Poor (LLaMA-3 tokenizer has high Bengali token split fertility) | CLIP-ViT-L \+ LLaMA-3 | Requires 4-bit quantization on 16 GB VRAM | Accessible | Unsuitable: Tokenizer splits single Bengali words into 4–8 sub-tokens, corrupting probability metrics |

## **10\. Closest 10–15 Papers**

The 12 closest published and preprint papers directly addressing the components of this research are detailed below, ranked by conceptual overlap with the candidate proposal.

| Paper | Year | Core Problem Addressed | Dataset Evaluated | Target Model Family | Confidence Signal Examined | Grounding Signal Used | Extrinsic Evidence Signal | Abstention Mechanism | Risk-Coverage Evaluated? | Cultural / Bengali Focus? | Conceptual Overlap Assessment |
| :---- | :---- | :---- | :---- | :---- | :---- | :---- | :---- | :---- | :---- | :---- | :---- |
| **SIEVES** (Rodriguez & Rohrbach) | 2026 | Selective prediction under OOD visual shift | V\* Bench, VizWiz, AdVQA, HR-Bench | Pixel-Reasoner, o3, Gemini-3-Pro | Learned auxiliary correctness score (c\_{\\text{corr}}) | Bounding-box localization (c\_{\\text{loc}}) \+ crop coherence (c\_{\\text{coh}}) | None (Intrinsic visual evidence only) | Confidence thresholding on fused score | Yes (C@1\\%, C@5\\%, AURC) | No (General OOD vision) | High on SP mechanics; zero on cultural domain |
| **Grounded or Guessing? (BICR)** (Khanmohammadi et al.) | 2026 | Separating visual reliance from language priors | GQA, POPE, MMMU-Pro, MME-Finance | LLaVA, Qwen-VL, Yi-VL (5 LVLMs) | Contrastive ranking loss on internal hidden states | Real vs. blacked-out blind image contrast | None | Soft thresholding / calibration scoring | Yes (ECE, Brier score, AUROC) | No | Very High on grounding confidence; zero on cultural domain |
| **Look Again Before You Abstain (BCEA)** (Xu et al.) | 2026 | Over-abstention in conformal selective prediction | POPE, MS-COCO | LLaVA-1.5, Qwen3-VL, InternVL2 | Conformal non-conformity scores | Image removal drop vs. zoomed crop intervention | None (Active visual acquisition) | 3-way: Answer, Abstain, Acquire Evidence | Yes (Conformal coverage at \\le 5\\% risk) | No | High on evidence acquisition and abstention bounds |
| **DualRead** (Anonymous / ResearchGate) | 2026 | Capability vs confidence in RLVR-trained VLMs | Medical VQA, PathVQA | Frozen GRPO actors (Qwen-VL) | Decoupled pre-answer & post-answer state probes | Counterfactual hard-negative image substitution (CCG-AUC) | None | Thresholded deferral policy | Yes (AURC, ECE, CCG-AUC) | No (Medical domain) | High on counterfactual grounding mechanics |
| **BanglaVerse** (Sayeedi et al.) | 2026 | Multilingual & multidialectal cultural VLM evaluation | BanglaVerse (1,152 images, 9 domains) | GPT-4o, Gemini, Qwen2-VL, Claude | None (Accuracy evaluation only) | None (Observational accuracy) | Multi-dialect textual context | None (Forced generation) | No | Yes (Core Bengali benchmark) | Identical benchmark setting; zero uncertainty modeling |
| **BanglaProtha** (Fahim et al.) | 2026 | Long-tail cultural VLM evaluation with fine distractors | BanglaProtha (\~1.2k images, Bengali culture) | LLaVA, Qwen-VL, BLIP-2 | None (MCQA accuracy) | None | None | None | No | Yes (Bengali cultural VQA) | High domain overlap; zero calibration/abstention |
| **TRAPSBench** (Pramono et al.) | 2026 | Representation-output gap in epistemic abstention | TRAPSBench (1,404 matched physics video pairs) | 16 VLMs (Qwen, Gemma, LLaVA families) | Linear probes on internal states vs output text | Minimal visual intervention (occlusion, chaos) | None | Spontaneous abstention / verbalized restraint | Yes (PECS: Penalized Epistemic Calibration) | No (Physical reasoning) | High on internal probing vs output abstention |
| **Confidence Estimation for Financial VLMs** (Khanmohammadi et al.) | 2026 | Trustworthy deferral in chart/doc understanding | FinMME, FinChart-Bench | 5 open-weight LVLMs | Comparison of 7 estimators (verbal, logits, probes) | Figure-grounding check via blind-view contrast | None | Error-budgeted deferral policy | Yes (ConfErr, ECE, AUROC, Brier) | Partial (Includes bilingual condition) | Very High on methodology; applied to finance |
| **Reference-free Hallucination Detection** (Li et al.) | 2024 | Detecting unsupported claims without external tools | POPE, GQA, IHAD | LLaVA-1.5, MiniGPT-4 (5 LVLMs) | Uncertainty (AvgProb, AvgEnt), consistency, SUQ | None explicitly (implicit in token distribution) | None | Threshold-based hallucination filtering | Yes (AUC-PR, F1-score) | No | High overlap with confidence signal baselines |
| **LeMUQ** (Binz et al.) | 2025 | Uncertainty quantification in Multimodal RAG | Multimodal RAG benchmarks | Open-weight MLLMs | Token probability shifts under modality drop | Dropping visual modality tokens | Dropping retrieved textual context | Confidence thresholding | Yes (AUROC, Calibration) | No | High on external evidence \+ visual uncertainty fusion |
| **Selective Selective Prediction (ReCoVERR)** (Srinivasan et al.) | 2024 | Reducing unnecessary abstention in VLMs | ScienceQA, VQA v2 | InstructBLIP, LLaVA | Internal model confidence \+ second-pass verification | Cross-modal agreement checks | None | Dynamic re-evaluation of abstained queries | Yes (Risk vs Coverage trade-offs) | No | Moderate; foundational generative selective VQA |
| **M4-RAG** (Satar et al. survey / CVPR) | 2026 | Multilingual, multi-cultural multimodal retrieval | 80k QA pairs, 42 languages, 189 countries | Frontier & open VLMs \+ dense retrievers | Dense retrieval similarity score | Context-image joint attention | Multilingual cultural document corpus | Retrieval score filtering | Partial (Recall vs Precision) | Broad global culture (includes South Asia) | High on cultural retrieval; low on model calibration |

### **Closest-Work Matrix**

| Work | What It Already Establishes | What It Does NOT Establish | Relevance to Proposal 3 | Pre-emption Risk | | :--- | :--- | :--- | :--- | :--- | | **SIEVES** (Rodriguez & Rohrbach, 2026\) | Visual evidence quality (localization and coherence) triples selective prediction coverage under OOD shifts. | Does not test non-Western cultural entities, multilingual prompts, or external knowledge integration. | Direct methodological predecessor for evidence-based selective VQA. | Partially Occupied: Method is solved; application to culture is unstudied. | | **BICR** (Khanmohammadi et al., 2026\) | Contrastive ranking against a blind image removes language-prior bias and produces calibrated confidence probes. | Does not evaluate fine-grained cultural recognition or low-resource non-Latin linguistic settings. | Directly occupies the "blank-image contrastive confidence" mechanism. | Pre-empted (Method): Blind-image contrastive probing is established. | | **BCEA** (Xu et al., 2026\) | Distribution-free conformal risk bounds for VLMs using adaptive visual acquisition to maintain coverage. | Does not evaluate textual retrieval, world knowledge ambiguity, or cultural benchmarks. | Establishes the theoretical ceiling for evidence-acquisition abstention. | Partially Occupied: Conformal abstention machinery is mature. | | **BanglaVerse** (Sayeedi et al., 2026\) | VLM error rates across Bengali culture; 42.6% of failures are local entity misrecognitions. | Does not evaluate confidence calibration, abstention, selective prediction, or internal probing. | Primary benchmark candidate providing cultural visual assets. | Open (Calibration): Domain is tested for accuracy, not reliability. | | **BanglaProtha** (Fahim et al., 2026\) | Culturally specific VQA with semantically similar distractors exposes long-tail failure modes in VLMs. | Does not evaluate uncertainty calibration, risk-coverage trade-offs, or selective abstention. | Alternative benchmark candidate with cleaner discrete MCQA targets. | Open (Calibration): Evaluated purely on forced accuracy. |

## **11\. Pre-emption Audit**

The candidate proposal attempts to combine visual evidence scoring, external cultural knowledge, and selective prediction on Bengali imagery. The pre-emption risk across the three most dangerous papers must be analyzed:

### **1\. SIEVES: Selective Prediction Generalizes through Visual Evidence Scoring**

Hector G. Rodriguez and Marcus Rohrbach (arXiv:2604.25855, April 2026; official repository: hector-gr/SIEVES).

SIEVES solves the core selective prediction problem for VQA under out-of-distribution visual shifts by replacing internal logit confidence with explicit visual evidence scoring. The authors train an auxiliary selector model (using Pixel-Reasoner trajectories) to predict answer correctness (c\_{\\text{corr}}), localization precision (c\_{\\text{loc}}), and crop-answer coherence (c\_{\\text{coh}}). On benchmarks including V\* Bench, HR-Bench-8k, VizWiz, and AdVQA, SIEVES triples coverage at low error tolerances (C@1\\% and C@5\\%) and generalizes to black-box proprietary reasoners (o3, Gemini-3-Pro).

SIEVES does not evaluate non-Western cultural benchmarks, does not assess multilingual prompts, and relies exclusively on visual crops rather than external factual knowledge.

Pre-emption Status: PARTIALLY OCCUPIED. The foundational concept of using visual evidence quality to drive selective prediction risk-coverage curves is claimed and occupied. Applying SIEVES directly to Bengali images is an incremental domain transfer.

### **2\. Grounded or Guessing? LVLM Confidence Estimation via Blind-Image Contrastive Ranking**

Reza Khanmohammadi, Erfan Miahi, Simerjot Kaur, Charese H. Smiley, Ivan Brugere, Kundan Thind, Mohammad M. Ghassemi (arXiv:2605.10893, May 2026; official repository: ledengary/BICR).

BICR directly solves the problem of distinguishing whether an open-weight VLM's confidence is driven by authentic visual evidence or by language priors. BICR extracts hidden states from a frozen VLM under two forward passes: once with the genuine image-question pair, and once with the image blacked out. A lightweight probe is trained with a ranking loss penalizing higher confidence on the blind view, producing a calibrated confidence estimator at zero inference cost that outperforms all standard logit and verbal baselines across GQA, POPE, and MME.

In a companion study (arXiv:2608.06532), the authors prove that BICR isolates non-grounding from fluent guessing in specialized visual document tasks. BICR was evaluated only on English-centric and general benchmarks; it was not tested under localized cultural distribution shifts where both visual and linguistic features belong to a low-resource domain.

Pre-emption Status: PRE-EMPTED (Methodological Mechanism). The hypothesis that visual perturbation (blank-image contrast) provides a superior confidence signal over verbal or logit baselines is fully established. Using this exact contrastive ranking loss on Bengali data is an application of BICR rather than an original algorithmic contribution.

### **3\. Look Again Before You Abstain: Budgeted Conformal Evidence Acquisition for Reliable Vision-Language Models**

Jian Xu, Yanning Wu, Delu Zeng, John Paisley, Qibin Zhao (arXiv:2606.16667, June 2026).

Xu et al. solve the formal abstention trade-off under visual uncertainty using distribution-free conformal prediction. The paper proves that naive conformal selective prediction suffers from severe over-abstention (abstaining on \>80\\% of cases to guarantee \<5\\% error), and formalizes Budgeted Conformal Evidence Acquisition (BCEA). BCEA introduces an "answer, abstain, or acquire visual evidence" framework with exact theoretical certificates, maintaining coverage by re-examining image regions while preserving exchangeability.

Xu et al. evaluate only synthetic and object-existence benchmarks (POPE, MS-COCO). They do not explore external document retrieval or culturally specific entity recognition.

Pre-emption Status: PARTIALLY OCCUPIED. The theoretical machinery connecting evidence acquisition to conformal selective prediction is rigorously solved.

## **12\. Evidence Table**

| Claim / Hypothesis | Primary Evidence Source | Exact Document Location | Epistemic Status | Degree of Confidence | Core Limitation / Boundary |
| :---- | :---- | :---- | :---- | :---- | :---- |
| VLM miscalibration is a severe, active problem | Khanmohammadi et al. (2026) | arXiv:2608.06532, §1, Table 1 | VERIFIED | Certain | Inference baselines exhibit ECE up to 0.58 on specialized visual tasks. |
| Selective prediction is established for VLMs | Whitehead et al. (2022); Rodriguez & Rohrbach (2026) | ECCV 2022; arXiv:2604.25855, §1–§3 | VERIFIED | Certain | Problem formulation, metrics (C@R, AURC), and selectors are mature. |
| Visual grounding can predict correctness | Khanmohammadi et al. (2026) (BICR) | arXiv:2605.10893, §3, Table 2 | VERIFIED | Certain | Proved across 5 open LVLMs on standard VQA benchmarks. |
| Visual perturbation confidence is established | Khanmohammadi et al. (2026); DualRead (2026) | arXiv:2605.10893; arXiv:2609.06419, Eq. 1–6 | VERIFIED | Certain | Blank images and hard-negative replacements are standard baseline tools. |
| External evidence improves multimodal confidence | Binz et al. (LeMUQ, 2025/2026) | ResearchGate / arXiv:2505.21068, §2 | VERIFIED | High | Established in Multimodal RAG; vulnerable to text passage answer leakage. |
| Cultural VLM errors are measurable in Bengali | Sayeedi et al. (BanglaVerse, 2026\) | arXiv:2603.21165, §1, §4, Table 2 | VERIFIED | Certain | Documented on 1,152 images; 42.6% of failures are local entity misidentifications. |
| Dedicated Bengali cultural VQA benchmarks exist | Fahim et al. (BanglaProtha, 2026\) | IEEE/CVF WACV 2026, pp. 1159–1169 | VERIFIED | Certain | Curated Bengali images with native questions and semantically close distractors. |
| Bangla calibration has been systematically studied | Literature Audit across arXiv, ACL, CVPR (2024–2026) | Comprehensive search across BanglaVerse / BanglaProtha | CONTRADICTED | High | Existing Bangla multimodal papers evaluate accuracy/ROUGE/BLEU only; zero calibration. |
| Cultural unfamiliarity creates unique uncertainty shift | Theoretical inference from Sayeedi et al. & Nayak et al. | Inferred from knowledge-bottleneck findings | HYPOTHESIS | Moderate | Unproven whether this shift is distinct from general long-tail epistemic uncertainty. |
| Evidence-grounded abstention has been studied | Xu et al. (BCEA, 2026); Rodriguez & Rohrbach (2026) | arXiv:2606.16667; arXiv:2604.25855 | VERIFIED | Certain | Established theoretically and empirically on general CV benchmarks. |
| The exact proposed combination is occupied | Literature Cross-Search (SIEVES \+ BanglaVerse) | No prior paper combines SIEVES \+ BanglaVerse | CONTRADICTED | High | The literal combination of these specific assets has not been published. |
| The proposed combination represents an unaddressed gap | Synthesis of Section 10 & 11 | Conceptual mapping | INFERRED (As Weak/False Gap) | High | Novelty exists only as geographic dataset substitution, not algorithmic discovery. |

## **13\. Gap Map**

The research space surrounding multimodal selective prediction and cultural understanding contains distinct categories of maturity:

> * Occupied: Multimodal selective prediction algorithms and risk-coverage formalisms (SIEVES, ReCoVERR); blind-image contrastive ranking for visual reliance calibration (BICR); the representation-output gap in VLM epistemic restraint (TRAPSBench); and the empirical demonstration that VLMs fail on Bengali cultural entities (BanglaVerse, BanglaProtha).  
> * Partially Occupied: Conformal risk control under adaptive evidence acquisition (BCEA—solved on object-existence benchmarks like POPE, but open on external textual RAG); and the calibration robustness of compact open-weight models under post-training quantization.  
> * False Gaps: "Evidence-Grounded Selective Prediction" is formally identical to selective VQA with auxiliary visual and textual verification signals; and "Local-Entity Hallucination Mitigation" is a rebranding of out-of-distribution entity abstention.  
> * Weak Gaps: Applying off-the-shelf BICR or SIEVES code directly to BanglaVerse to generate a localized leaderboard; and comparing verbal confidence against temperature-scaled logits on Bengali prompts.  
> * Stronger Candidate Gaps: Modality Prior Dominance under Cultural Shift—evaluating whether cultural unfamiliarity systematically flips a VLM's decisional arbitration toward language priors, rendering visual tokens inert; and Probe Transferability across Cultural Strata—testing whether a confidence probe trained on high-resource Western imagery reliably predicts correctness on long-tail cultural entities without retraining.

## **14\. Competing Research Questions**

If this field is to be pursued as a defensible thesis, it cannot ask a descriptive engineering question such as *"Can we build an evidence-grounded selective prediction system for Bangla VLMs?"*. It must formulate a precise scientific question governed by competing, falsifiable hypotheses:

### **Candidate Core Research Question**

Under regional cultural distribution shift, does model miscalibration stem primarily from visual feature misidentification (H\_1) or from language-prior overconfidence suppressing visual reliance (H\_0), and can contrastive visual grounding signals isolate these errors without external textual retrieval?

#### **Competing Hypothesis Pair 1: Nature of Cultural Unreliability**

Under Hypothesis H\_1 (Visual Perceptual Grounding Failure), the VLM extracts non-discriminative or entangled visual features from culturally unfamiliar entities, producing low internal visual-token alignment that directly correlates with prediction error.

The empirical signature of this mechanism is that probing visual token representations (h^{\\text{evid}}) yields low alignment scores on incorrect cultural items; furthermore, blank-image ablation (I \= \\emptyset) causes a substantial drop in output likelihood, proving that the model attempted to utilize the visual input.

Conversely, under Hypothesis H\_0 (Language-Prior Attentional Capture), the VLM’s language model backbone defaults to high-frequency cultural priors regardless of visual inputs, rendering the prediction functionally blind.

The empirical signature is that logit distributions and generated entity text remain invariant when replacing the culturally specific image with a blank or mismatched image; model confidence is driven entirely by language-token unigram frequencies.

#### **Competing Hypothesis Pair 2: Utility of External Evidence**

Under Hypothesis H\_1 (True Epistemic Calibration via Factual Grounding), external cultural knowledge passages improve selective prediction risk-coverage curves by resolving genuine visual-semantic ambiguities.

The empirical signature is that risk-coverage improvements persist even when retrieved text passages are entity-masked (replacing the gold entity name with generic placeholders like \[ENTITY\]).

Under Hypothesis H\_0 (Trivial Shortcut Leakage), apparent calibration gains from external cultural evidence are artifacts of label leakage, where the text passage names the entity verbatim and allows the model to bypass visual processing entirely.

The empirical signature is that masking entity tokens in external text causes selective prediction AUROC to collapse to the baseline logit level.

## **15\. Main Scientific Risks**

Pursuing the topic under its current formulation exposes the researcher to four severe scientific risks:

> * Catastrophic Answer Leakage via External Retrieval: As established in the Canonical Project Baseline (Section 5.4), retrieving external cultural passages creates non-orthogonal interventions. If a passage contains the text *"Shorshe Ilish is a traditional Bengali hilsa fish curry..."*, the VLM does not perform visual grounding; it performs reading comprehension. This completely invalidates any claim of measuring visual uncertainty calibration.  
> * Confounding Multi-Signal Fusion: Combining verbal confidence, logit stability, visual perturbations, and retrieval scores via a learned logistic regression head (C\_{\\text{combined}} \= \\sum w\_i C\_i) is a shallow heuristic. If the classifier achieves 0.85 AUROC, the thesis cannot determine which underlying mechanism provided the signal, or whether the classifier simply memorized category-level difficulty priors.  
> * Severe Coverage Collapse at Operational Risk Levels: As proven by Xu et al. (2026), enforcing strict risk bounds (\\mathcal{R} \\le 5\\%) on uncalibrated models forces the selection function to abstain on 80% to 90% of queries. A selective prediction system that abstains on nearly every culturally specific query provides zero practical utility, converting a machine learning capability study into a trivial demonstration of conservative refusal.  
> * Annotation Subjectivity and Cultural Ambiguity: Bengali cultural artifacts often lack discrete ontological boundaries (e.g., regional culinary variants, overlapping textile weaves like Jamdani vs. Tangail). If the ground-truth annotations are subjective, calibration metrics (ECE, Brier Score) will penalize the model for genuine semantic ambiguity rather than model failure, confounding aleatoric data uncertainty with epistemic model ignorance.

## **16\. Feasibility Under Local Constraints**

The principal researcher’s computational environment is strictly bounded: Google Colab Pro (single GPU, 16 GB VRAM envelope), an AMD Ryzen 5 5600G local workstation (no local CUDA), and compact open-weight models. Foundation-model training from scratch is entirely ruled out.

| Experimental Component | Operational Requirement | Feasibility Status | Controlling Verification / Feasibility Rationale | | :--- | :--- | :--- | :--- | | **Model Hosting (Qwen2.5-VL-3B)** | 7.5 GB VRAM in bfloat16 | VERIFIED FEASIBLE | Fits comfortably within Colab T4/V100 (16 GB) with ample headroom for KV cache. | | **Model Hosting (Qwen2.5-VL-7B)** | 15.5 GB in bfloat16; 5.5 GB in 4-bit | VERIFIED FEASIBLE (Quantized Only) | bfloat16 triggers immediate CUDA OOM during multi-image inference; 4-bit BitsAndBytes is mandatory. | | **Inference Budget (Baseline QA)** | 500 items \\times 1 pass \= 500 passes | VERIFIED FEASIBLE | 500 greedy generations on Qwen2.5-VL-3B take \~12 minutes on a Colab T4 GPU. | | **Visual Perturbation Suite** | 500 items \\times 3 conditions (Original, Blank, Mismatched) | VERIFIED FEASIBLE | 1,500 forward passes take \~36 minutes on Colab T4. | | **Sampling Consistency** | 500 items \\times 10 sampled passes (T=0.7) | ESTIMATED FEASIBLE | 5,000 autoregressive passes take \~2.5 hours; requires careful session management. | | **Internal Hidden State Probing** | Extracting layer activations (L\_{18}, L\_{28}) | VERIFIED FEASIBLE | Teacher-forced forward passes extract residual activations instantly without autoregressive decoding. | | **External Vector Retrieval Pipeline** | FAISS \+ BGE-M3 \+ 10k passages | VERIFIED FEASIBLE (High Engineering) | Feasible in memory, but adds 3–4 weeks of indexing, chunking, and scraper maintenance. | | **Statistical Sample Size** | 300–500 evaluation samples | MARGINALLY SUFFICIENT | While adequate for gross accuracy, 300 samples yield very wide Wilson confidence intervals for low-risk coverage (C@1\\% or C@5\\%). |

## **17\. Comparison with Proposals 1 and 2**

To evaluate whether Candidate Proposal 3 warrants inclusion in the formal thesis portfolio, its core properties must be compared against the existing active proposals defined in the Canonical Context.

| Dimension | Proposal 1: Reasoning Trace Degradation | Proposal 2: Visual Binding IDs Transfer | Candidate Proposal 3: Evidence-Grounded SP |
| :---- | :---- | :---- | :---- |
| **Core Failure Mode Studied** | Visual attention decay and forgetting in extended multimodal reasoning chains. | Failure of localized visual binding representations to transfer beyond synthetic grids. | Uncalibrated, overconfident hallucinations on localized cultural entities. |
| **Research Question Clarity** | Extremely High: Is decay causal reasoning computation or a RoPE / softmax (M/N) artifact? | Extremely High: Are binding IDs genuine neural features or geometric perturbation artifacts? | Moderate-Low: Conflates confidence calibration, visual grounding, and external retrieval. |
| **Existing Literature Density** | Moderate: Observational literature exists, but dilution artifact controls are completely unstudied. | Moderate: Grounding IDs claimed in ICML 2026; natural image placebo audit is completely open. | Dense: Selective VQA, BICR, and conformal abstention are heavily studied on standard CV data. |
| **Novelty Risk** | Very Low: Clear causal mechanistic audit. | Very Low: Landmark placebo-controlled rebuttal. | High: Risks being dismissed as applying existing methods (BICR/SIEVES) to a local dataset. |
| **Dependence on Bengali Data** | Zero (Evaluates on WhatIfVis counterfactual pairs). | Zero (Evaluates on DSCAM / synthetic grids). | 100% Dependent (Requires BanglaVerse / BanglaProtha). |
| **Mechanistic Depth** | Deep: Layer hooks, RoPE coordinate manipulation, linear probes, attention head profiling. | Deep: Layer-22 residual stream activation patching, Gaussian placebos, interpolation. | Shallow-Moderate: Output logits, image blanking, external text matching, post-hoc classifier. |
| **Evaluation Maturity** | Deterministic: Exact-match target parsing on counterfactual physics questions. | Deterministic: Directed target flip rates (\\text{NetFlip}) and repetition metrics. | Mixed: Accuracy on MCQA is deterministic; free-form entity matching requires subjective aliasing. |
| **Dataset Availability** | Turnkey: Public Hugging Face datasets (WhatIfVis). | Turnkey: Synthetic grid scripts \+ public DSCAM images. | Turnkey: BanglaVerse / BanglaProtha public on Hugging Face and GitHub. |
| **Compute Feasibility** | Flawless: Pure inference and probing on Colab Pro T4 (\~3 hours). | Flawless: Pure inference and activation overwrites on Colab Pro T4 (\~2 hours). | Feasible, but multi-pass perturbations and sampling multiply inference time by 15\\times. |
| **Annotation Burden** | Zero: Pre-existing ground truths. | Zero: Automated bounding box and category generation. | High: Requires manual verification of acceptable entity aliases and cultural distractors. |
| **Leakage Risk** | Zero: Strictly controlled counterfactual pairs. | Zero: Parametric interventions on isolated tokens. | Severe: External cultural passages frequently leak the gold entity name. |
| **Negative-Result Value** | Outstanding: Proves visual forgetting is an artifact of RoPE and softmax normalization. | Landmark: Refutes claimed "Binding IDs" as artifacts of synthetic geometric grids. | Moderate: Shows that visual grounding does not calibrate cultural models, leaving causes uncertain. |
| **Main Confound** | Confounding reasoning token length with sequence position. | Destructive activation patching causing global linguistic incoherence. | Answer leakage from text hints; retriever error vs. model error. |
| **Potential Contribution Type** | Mechanistic and Diagnostic. | Mechanistic and Diagnostic. | Empirical and Evaluative. |

## **18\. What Would Make Proposal 3 Defensible?**

For Proposal 3 to achieve the scientific rigor of an elite CSE undergraduate thesis, it must undergo radical de-scoping and restructuring:

> 1. Eliminate the External Retrieval Pipeline Entirely (Adopt Variant A): Discard external document retrieval, vector databases, and cultural text passages. This completely removes the answer leakage confound and prevents the project from degenerating into a standard RAG engineering application.  
> 2. Shift Focus from System Construction to Diagnostic Audit: Reframe the thesis not as *"building a selective prediction tool,"* but as an explanatory investigation into why current confidence calibration mechanisms fail under cultural distribution shifts.  
> 3. Isolate Modality Dominance via Paired Interventions: Measure the causal effect of visual tokens by comparing prediction distributions across three strictly controlled conditions:  
   * Condition 1: Original image \+ Native Bengali question.  
   * Condition 2: Blind image (blacked-out canvas) \+ Native Bengali question (isolates pure language prior).  
   * Condition 3: Mismatched cultural image (e.g., swapping a picture of *Shorshe Ilish* with *Chotpoti*) \+ Native Bengali question.  
> 4. Deploy Rigorous Selective Prediction Metrics: Replace naive threshold sweeps with formal Area Under the Generalized Risk-Coverage Curve (AUGRC) and distribution-free split conformal prediction. This provides mathematically verifiable coverage bounds that satisfy publication standards.  
> 5. Utilize Pre-Existing Structured Benchmarks: Restrict the evaluation data to the verified multiple-choice split of BanglaProtha, avoiding subjective free-form string matching and ad-hoc alias creation.

## **19\. Strongest Arguments Against Proposal 3**

The following adversarial arguments challenge the pursuit of Candidate Proposal 3:

> 1. The Regional Dataset Trap: CSE thesis evaluation committees frequently reject projects that simply take an established algorithm from the literature and apply it to local data. Because selective prediction (SIEVES), contrastive visual calibration (BICR), and conformal abstention (BCEA) have already been published in 2026, reviewers may view this work as an incremental application of existing tools to Bengali images without core algorithmic or theoretical novelty.  
> 2. The Non-Orthogonal Intervention Dilemma: As formally recorded in the project's Canonical Baseline (Section 5.4), intervening on cultural knowledge through multimodal prompts is notoriously non-orthogonal. In natural images of cultural artifacts, the visual features, cultural associations, and linguistic labels are deeply entangled. It is methodologically difficult to prove whether an abstention was triggered by a failure to extract visual pixels or by a lack of parametric world knowledge about Bangladesh.  
> 3. High Operational Overhead for Low Mechanistic Yield: Unlike Proposal 1 (which isolates RoPE coordinates and attention denominators) and Proposal 2 (which hooks specific transformer layers and applies norm-matched Gaussian placebos), Candidate Proposal 3 operates primarily at the input-output level. It requires verifying hundreds of cultural images, translating questions, and checking dialectal aliases, but yields little mechanistic insight into the internal representations of transformer models.  
> 4. Risk of Engineering Collapse: If the external evidence component is retained, the principal researcher will spend the majority of the thesis timeline debugging web scrapers, FAISS vector embeddings, chunking boundaries, and text matching heuristics, rather than conducting deep empirical AI research.

## **20\. Final Research-Status Assessment**

### **1\. Is "Evidence-Grounded Selective Prediction for Reliable Bangla Cultural Vision-Language Models" a legitimate research field?**

It is not a distinct, recognized scientific field. It is a localized composite application that merges three established subfields: selective classification in VQA, multimodal uncertainty estimation, and multilingual cultural evaluation.

### **2\. Is the exact current formulation sufficiently novel?**

No. The broad formulation in the working document combines established tools—visual perturbation tests from BICR, evidence scoring from SIEVES, and retrieval augmentation—and applies them to a regional dataset. Under top-tier evaluation criteria, this constitutes an application study rather than a fundamental scientific contribution.

### **3\. Which parts are already crowded?**

The general machinery of selective prediction in VLMs (AUGRC, coverage at risk), blind-image contrastive confidence estimation (BICR), conformal abstention algorithms (BCEA), and empirical benchmarking of VLMs on Bengali cultural images (BanglaVerse, BanglaProtha) are crowded and heavily occupied by 2025–2026 literature.

### **4\. Which parts are potentially open?**

The intersection of modality dominance and calibration under localized distribution shift remains open. Specifically, no prior work has systematically audited whether compact open-weight VLMs experience a severe collapse in internal visual-token reliance when transitioning from Western to Bengali cultural entities, or whether internal probes can decode entity-level answerability under cultural shift.

### **5\. Does the Bangla/Bengali cultural context provide scientific value beyond localization?**

Only if it is utilized as an authentic real-world distribution shift to test the boundary conditions of multimodal calibration. If used merely as a substitute dataset to rerun existing algorithms, it lacks scientific depth. If used to test whether cultural unfamiliarity forces models into extreme language-prior dominance that blinds them to visual evidence, it provides genuine diagnostic value.

### **6\. Is the external-evidence component scientifically justified or likely to become RAG engineering?**

It is not scientifically justified in a BSc thesis on visual reliability. It introduces answer leakage, confounds retriever recall with model calibration, and inevitably collapses into generic RAG systems engineering. It should be completely excised.

### **7\. What is the strongest plausible research question that remains after accounting for existing literature?**

Does cultural distribution shift systematically induce language-prior dominance over visual evidence in compact open-weight VLMs, and can parameter-free visual contrastive probes improve selective prediction calibration without external knowledge retrieval?

### **8\. What is the strongest argument AGAINST pursuing this field?**

The project carries severe risks of superficial novelty, high annotation burden, and answer leakage, while lacking the mechanistic depth and rigorous experimental controllability of Proposal 1 (Attention Dilution Artifacts) and Proposal 2 (Binding IDs Natural-Transfer Audit).

### **9\. What evidence would be required before calling it a thesis candidate?**

The researcher would need:

> 1. Verified proof that a compact model (e.g., Qwen2.5-VL-3B) exhibits a statistically significant drop in visual feature reliance on Bengali cultural images compared to standard benchmarks;  
> 2. A leakage-free, fully deduplicated evaluation split derived from BanglaProtha with closed multiple-choice options;  
> 3. Mathematical confirmation that visual-contrastive probes improve AUGRC over logit baselines without requiring external text retrieval.

### **10\. Can it reasonably be added as Proposal 3?**

It can be added as a reserve candidate only under the de-scoped "Variant A" diagnostic audit formulation. Under its current multi-signal, retrieval-heavy formulation, it should be reserved or discarded. Active Proposals 1 and 2 remain substantially superior in mechanistic clarity, experimental elegance, and publication defensibility.

#### **Works cited**

1\. Selective Prediction Generalizes through Visual Evidence Scoring, https://arxiv.org/abs/2604.25855 2\. \[2605.10893\] Grounded or Guessing? LVLM Confidence Estimation, https://arxiv.org/abs/2605.10893 3\. \[2606.16667\] Look Again Before You Abstain:Budgeted Conformal, https://arxiv.org/abs/2606.16667 4\. Look Again Before You Abstain:Budgeted Conformal Evidence, https://arxiv.org/pdf/2606.16667 5\. Confidence Estimation for Financial Vision-Language Models ... \- arXiv, https://arxiv.org/html/2608.06532 6\. Evaluating Multilingual VLMs for Bengali Culture Understanding, https://arxiv.org/html/2603.21165v2 7\. BanglaProtha \- WACV 2026 Open Access Repository, https://openaccess.thecvf.com/content/WACV2026/html/Fahim\_BanglaProtha\_Evaluating\_Vision\_Language\_Models\_in\_Underrepresented\_Long-tail\_Cultural\_Contexts\_WACV\_2026\_paper.html 8\. Spencer Whitehead's research works | Meta and other places, https://www.researchgate.net/scientific-contributions/Spencer-Whitehead-2220283176 9\. TRAPSBench: Vision-Language Models Encode but Fail to Express, https://arxiv.org/html/2608.13167v1 10\. Reference-free Hallucination Detection for Large Vision-Language, https://arxiv.org/html/2408.05767v2 11\. The Art of Abstention: Selective Prediction and Error Regularization, https://www.researchgate.net/publication/353492014\_The\_Art\_of\_Abstention\_Selective\_Prediction\_and\_Error\_Regularization\_for\_Natural\_Language\_Processing 12\. Cultural VLM Resources \- Burak Satar, https://buraksatar.github.io/resources/ 13\. \[论文评述\] Selective "Selective Prediction": Reducing Unnecessary, https://www.themoonlight.io/zh/review/selective-selective-prediction-reducing-unnecessary-abstention-in-vision-language-reasoning 14\. Evaluating the Impact of Post-Training Quantization on Reliable, https://www.researchgate.net/publication/400854947\_Evaluating\_the\_Impact\_of\_Post-Training\_Quantization\_on\_Reliable\_VQA\_with\_Multimodal\_LLMs 15\. Grounded Dual-State Calibration for GRPO-Trained Medical Vision, https://arxiv.org/html/2609.06419v1 16\. Can LLMs Express Their Uncertainty? An Empirical Evaluation of, https://www.alphaxiv.org/abs/2306.13063 17\. Confidence Estimation for Medical Vision-Language Models \- arXiv, https://arxiv.org/pdf/2606.15910 18\. Grounded or Guessing? LVLM Confidence Estimation via Blind, https://arxiv.org/html/2605.10893v1 19\. HARMONY: Hidden Activation Representations and Model Output, https://www.researchgate.net/publication/395622493\_HARMONY\_Hidden\_Activation\_Representations\_and\_Model\_Output-Aware\_Uncertainty\_Estimation\_for\_Vision-Language\_Models 20\. Hector Garcia Rodriguez, https://hector.gr/ 21\. GitHub \- hector-gr/SIEVES, https://github.com/hector-gr/SIEVES 22\. (PDF) TRAPSBench: Vision-Language Models Encode but Fail to, https://www.researchgate.net/publication/412248199\_TRAPSBench\_Vision-Language\_Models\_Encode\_but\_Fail\_to\_Express\_Epistemic\_Restraint 23\. KhatianDoc: A Human-Verified Benchmark Diagnosing Multimodal, https://arxiv.org/html/2609.03597v1 24\. \[WACV'26\] BanglaProtha: Evaluating Vision Language Models in, https://github.com/farhanishmam/BanglaProtha 25\. GitHub \- Ledengary/BICR, https://github.com/ledengary/BICR/ 26\. Confidence Estimation for Financial Vision-Language Models in, https://arxiv.org/abs/2608.06532 27\. Look Again Before You Abstain: Budgeted Conformal Evidence, https://arxiv.org/html/2606.16667v2