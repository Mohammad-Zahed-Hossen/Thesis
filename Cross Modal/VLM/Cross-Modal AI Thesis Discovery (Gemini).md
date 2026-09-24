# **Cross-Modal Evidence Attribution, Conflict Arbitration, and Inferential Reliability in Vision-Language Models: An Adversarial Thesis Discovery Audit**

# **A. Research-question tree**

Recent empirical evaluations from 2024 through 2026 reveal that vision-language models (VLMs) frequently generate correct factual answers without utilizing visual evidence, while simultaneously attending to relevant visual regions without achieving inferential reliability. The fundamental bottleneck for undergraduate-scale empirical research is isolating which modality causally shifts a model's decision, under what controlled intervention, and at what cost to calibration and reliability.

The scientific question space within Multimodal and Vision-Language Learning is organized systematically across twelve core research families. The taxonomy links observable phenomena, failure modes, explanatory mechanisms, controlled interventions, and measurable outcomes:

> * Multimodal / Vision-Language Learning and Systems  
  * &nbsp;  
    1. Cross-Modal Evidence Use and Grounding Sensitivity  
    * Failure Mode: The model produces correct textual predictions while ignoring visual inputs, or hallucinates visual attributes unsupported by the pixel space.  
    * Explanatory Hypothesis: Parametric language priors override visual inputs, versus cross-modal fusion layers failing to allocate capacity to dense spatial tokens.  
    * Controlled Intervention: Progressive pixel corruption, semantic masking, attribute replacement, and unimodal ablation.  
    * Measurable Outcome: Paired accuracy change (\\Delta\_{\\text{acc}}), counterfactual sensitivity, and visual grounding faithfulness.  
    * Research Question: When visual evidence is progressively degraded or ablated, does prediction degradation correlate with visual attention allocation, or do language priors dominate until a catastrophic collapse threshold?  
  * &nbsp;  
    1. Cross-Modal Conflict Arbitration and Modality Dominance  
    * Failure Mode: When image and text provide mutually contradictory facts, the model defaults to a dominant modality rather than evaluating relative source reliability.  
    * Explanatory Hypothesis: Systematic modality bias driven by unimodal text pretraining, versus representation collapse in intermediate cross-modal projection layers.  
    * Controlled Intervention: Counterbalanced synthetic or natural image-text contradictions with varying degradation levels.  
    * Measurable Outcome: Modality Preference Bias (MPB), source-following rate, and arbitration accuracy.  
    * Research Question: When visual and textual inputs supply conflicting assertions, does an explicit disagreement-detection step reduce modality dominance errors compared to direct zero-shot arbitration?  
  * &nbsp;  
    1. Evidence Sufficiency, Calibration, and Selective Abstention  
    * Failure Mode: The model outputs high-confidence, fabricated assertions on queries where decisive evidence is missing, cropped, or ambiguous.  
    * Explanatory Hypothesis: Softmax confidence reflects language sequence fluency rather than cross-modal evidence sufficiency, versus attention dispersion over uninformative background tokens.  
    * Controlled Intervention: Systematic evidence-stripping ladder paired with unanswerable versus answerable query framing.  
    * Measurable Outcome: Brier score, Expected Calibration Error (ECE), Area Under the Risk-Coverage Curve (AURC), and selective risk.  
    * Research Question: Does visual evidence removal produce a calibrated increase in predictive entropy, or do models maintain uniform confidence across sufficient and insufficient evidence regimes?  
  * &nbsp;  
    1. Visual Re-Examination and Grounding Drift in Multi-Step Reasoning  
    * Failure Mode: In multi-step or chain-of-thought (CoT) visual reasoning, generated tokens progressively drift away from visual premises, anchoring exclusively to prior generated text.  
    * Explanatory Hypothesis: Autoregressive context growth drowns fixed-length visual prefix embeddings, versus loss of visual attention entropy caused by causal masking.  
    * Controlled Intervention: Dynamic prompt-based visual re-examination, token copy mechanisms, or image re-injection during decoding.  
    * Measurable Outcome: Late-stage visual attention weight, CoT grounding drift rate, and multi-step reasoning accuracy.  
    * Research Question: Does prompt-directed visual re-examination mitigate grounding drift during long-chain reasoning, or does it introduce verbal rationalization without altering pixel dependencies?  
  * &nbsp;  
    1. Visual-Token Compression and Selective Evidence Pruning  
    * Failure Mode: Token-pruned VLMs preserve macro-level benchmark scores while failing catastrophically on fine-grained spatial, counting, or OCR tasks.  
    * Explanatory Hypothesis: Token selection metrics prioritize visually salient background clusters over sparse, query-critical tokens, versus information loss in early-layer projection.  
    * Controlled Intervention: Uniform spatial pooling, query-aware cross-attention pruning, and representation coverage maximization across token retention ladders.  
    * Measurable Outcome: Per-task accuracy retention, evidence-sensitive error rate, and hallucination frequency under pruning.  
    * Research Question: Does visual-token pruning exhibit an interaction with evidence locality, disproportionately degrading localized fine-grained evidence while preserving global scene classification?  
  * &nbsp;  
    1. Modality Attribution, Modality Gaps, and Feature Contribution  
    * Failure Mode: Post-hoc attribution methods attribute decisions to visual features that, when masked, produce no change in output logits.  
    * Explanatory Hypothesis: Feature attribution conflates feature presence with causal counterfactual utility, versus geometric modality gaps preventing true cross-modal alignment.  
    * Controlled Intervention: Shapley-style counterfactual modality replacement, geometric modality gap measurement, and projection space manipulation.  
    * Measurable Outcome: Counterfactual Modality Attribution (CMA) accuracy, Modality Dominance Score (MDS), and causal faithfulness.  
    * Research Question: How closely do gradient-based visual saliency maps correspond to causal counterfactual modality reliance when evaluated across balanced multimodal tasks?  
  * &nbsp;  
    1. Missing-Modality Dynamics and Graceful Degradation  
    * Failure Mode: Abrupt accuracy collapse or spontaneous hallucination when an expected modality channel is entirely blank or corrupted.  
    * Explanatory Hypothesis: Architectural fragility in cross-modal attention maps when key/value tokens are uniform, versus distributional shift away from paired pretraining data.  
    * Controlled Intervention: Modality dropout, Gaussian noise replacement, and zero-embedding injection at inference time.  
    * Measurable Outcome: Graceful degradation slope, hallucination proliferation rate, and unimodal fallback accuracy.  
    * Research Question: When an image is completely missing, does an instruction-tuned VLM transition to calibrated textual reasoning or default to hallucinatory visual grounding?  
  * &nbsp;  
    1. Multimodal Counterfactual Faithfulness and Invariance  
    * Failure Mode: Editing a non-decisive visual detail alters the model's answer, while editing the decisive visual attribute leaves the answer unchanged.  
    * Explanatory Hypothesis: Spurious correlation with background context features, versus memorization of paired benchmark prompts.  
    * Controlled Intervention: Minimal counterfactual image edits (inpainting attribute changes) paired with unchanged queries.  
    * Measurable Outcome: Counterfactual update rate, semantic invariance score, and spurious flip rate.  
    * Research Question: Does counterfactual visual editing expose higher spurious sensitivity in large generative VLMs than in compact, parameter-efficient architectures?  
  * &nbsp;  
    1. Test-Time Adaptation and Shortcut Formation under Distribution Shift  
    * Failure Mode: Test-time adaptation (TTA) improves accuracy on out-of-distribution images while worsening cross-modal calibration and inducing catastrophic forgetting.  
    * Explanatory Hypothesis: Entropy-minimization objectives collapse cross-modal representations toward dominant text classes, versus gradient updates corrupting vision-bridge alignment.  
    * Controlled Intervention: Test-time prompt tuning, dynamic multi-rank adaptation, and entropy-filtered updates on shifted visual domains.  
    * Measurable Outcome: Out-of-distribution (OOD) accuracy, source retention, Brier score, and modality reliance shift.  
    * Research Question: Does test-time entropy minimization on shifted visual inputs improve cross-modal grounding, or does it amplify language-prior shortcuts?  
  * &nbsp;  
    1. Cross-Lingual Morphological Fragmentation and Modality Reliance  
    * Failure Mode: Presenting identical visual queries in low-resource or morphologically rich scripts alters the model's reliance on visual evidence.  
    * Explanatory Hypothesis: High subword fertility (morphological shattering) weakens textual semantic representations, forcing reliance on visual tokens, versus degraded textual understanding causing complete reasoning collapse.  
    * Controlled Intervention: Parallel cross-lingual queries (English vs. Bengali/Indic) across identical visual stimuli with controlled morphological complexity.  
    * Measurable Outcome: Modality reliance shift, token fertility ratio, cross-lingual consistency, and grounding accuracy.  
    * Research Question: Does high tokenizer fragmentation in low-resource scripts systematically shift a VLM's reliance toward visual evidence in visual question answering?  
  * &nbsp;  
    1. Claim-Level Visual Verification and Hallucination Control  
    * Failure Mode: Post-hoc reasoning traces generate plausible factual rationales containing micro-claims unsupported by visual evidence.  
    * Explanatory Hypothesis: Decoupled visual-linguistic decoding pipelines fail to enforce token-level verification, versus autoregressive decoding favoring narrative coherence over perceptual fidelity.  
    * Controlled Intervention: Claim decomposition followed by isolated bounding-box cross-checking or verification prompting.  
    * Measurable Outcome: Claim-level precision, unnecessary correction rate, and net factual accuracy.  
    * Research Question: Does explicit claim decomposition and visual verification reduce ungrounded assertions without inducing false-positive retractions of correct answers?  
  * &nbsp;  
    1. Multimodal Benchmark Validity, Contamination, and Shortcut Auditing  
    * Failure Mode: State-of-the-art VLMs achieve high benchmark scores on multimodal benchmarks even when visual inputs are completely removed or masked.  
    * Explanatory Hypothesis: High textual mutual information between question phrasing and answer options, versus web-scale benchmark memorization in language pretraining.  
    * Controlled Intervention: Blind text-only evaluation, blank-image evaluation, and question-option permutation across standard benchmarks.  
    * Measurable Outcome: Unimodal shortcut score, score inflation delta, and ranking stability across models.  
    * Research Question: What proportion of benchmark performance on modern multimodal datasets is driven by unimodal linguistic shortcuts rather than genuine cross-modal fusion?

# **B. Research families**

### **Family 1: Cross-Modal Evidence Use and Grounding Sensitivity**

In multimodal reasoning, models frequently rely on language priors rather than grounding their outputs in visual evidence. A model often answers questions about an image using statistical correlations learned during pretraining without confirming whether the target objects exist. This produces accurate answers to visual questions even when decisive pixels are occluded or replaced. Scientifically, when benchmark scores reward text-based guessing, they misrepresent genuine perceptual reasoning, creating brittle deployments in high-stakes visual domains.

Candidate independent variables include visual masking ratio (ranging from 0% to 100%), semantic region blurring, and distractor patch injection. Dependent variables focus on output token probability margins, paired accuracy change (\\Delta\_{\\text{acc}}), and visual grounding attribution faithfulness. Controlled interventions mask decisive image patches identified via ground-truth bounding boxes while leaving background pixels intact. Standard baselines comprise text-only unimodal models, frozen VLMs evaluated on complete images, and inputs paired with uniform random Gaussian noise. Applicable datasets include VQA v2, GQA, TextVQA, and DocVQA.

A central candidate research question asks whether visual evidence degradation induces a smooth decline in answer confidence or whether models maintain overconfidence until reaching a catastrophic collapse point. A meaningful negative result occurs if accuracy and confidence decline linearly and identically across all question types, indicating that language priors do not selectively compensate for missing visual data. The primary undergraduate feasibility hazard is the compute cost of retraining; investigations must be restricted to zero-shot inference on compact open-weight models.

### **Family 2: Cross-Modal Conflict Arbitration and Modality Dominance**

When visual and textual inputs provide contradictory evidence, vision-language architectures exhibit selective modality dominance rather than arbitrating based on relative channel reliability. If an image and its paired text caption conflict, the network defaults to following one modality while ignoring the other. This failure mode represents modality collapse, wherein the model follows text over vision—or vision over text—regardless of whether one channel is noisy or corrupted. Multimodal systems must learn to identify which channel is corrupted rather than adhering to rigid modality hierarchies.

Independent variables include modality corruption magnitude, conflict classification (factual, numeric, or entity), and instruction prompt framing. Dependent variables comprise Modality Preference Bias (MPB), arbitration accuracy, and contradiction detection rate. The controlled intervention constructs counterbalanced contradictory pairs and contrasts direct answering against explicit conflict classification. Baselines include direct answering without conflict prompts, text-only inputs, and image-only inputs. Testbeds utilize ChartQA-Conflict, MMMU-Conflict (CMC-Bench), and Visual-Counterfact.

A focal research question investigates whether explicit conflict-detection prompting eliminates text-dominance bias in chart and document reasoning. A meaningful negative result emerges if prompting for conflict detection increases verbal acknowledgment of disagreement while leaving final decision tokens locked to the dominant modality. This family carries minimal feasibility risk and can be executed via zero-shot batched inference on Google Colab Pro.

### **Family 3: Evidence Sufficiency, Calibration, and Selective Abstention**

Vision-language models exhibit poorly calibrated predictive uncertainty when visual evidence is incomplete, ambiguous, or missing. When confronted with an image lacking the evidence required to answer a question, models frequently fabricate an answer with high confidence instead of abstaining. This failure mode manifests as confident hallucination on unanswerable multimodal queries. Autonomous decision systems require calibrated uncertainty to detect when information is absent, enabling fallback or human clarification workflows.

Independent variables involve decisive evidence presence (present, partially occluded, fully absent), query specificity, and candidate answer space constraints. Dependent variables include Expected Calibration Error (ECE), Brier score, selective risk across coverage levels, and abstention precision/recall. The controlled intervention crops or inpainting-masks the specific visual region that answers the query, paired with an abstention-enabled prompt. Baselines consist of always-answer rules, maximum softmax probability thresholds, and raw token entropy. Suitable benchmarks include VizWiz-Priv, unanswerable splits of VQA v2, and ChartQA.

The primary research question asks whether token sequence entropy reliably separates unanswerable queries from answerable queries across different task complexities. A meaningful negative result occurs if predictive entropy remains indistinguishable between answerable and unanswerable samples, demonstrating that output confidence is uncoupled from evidence sufficiency. The main feasibility challenge involves the overhead of verifying answerability annotations, which is mitigated by using established unanswerability splits.

### **Family 4: Visual Re-Examination and Grounding Drift in Multi-Step Reasoning**

During multi-step autoregressive generation, vision-language models demonstrate progressive visual grounding degradation. As the generated reasoning chain extends, the model gradually stops conditioning on visual tokens and generates subsequent claims based entirely on text tokens produced earlier in the decoding sequence. This failure mode is termed visual drift, wherein late-stage reasoning steps diverge from physical image constraints, leading to false conclusions despite correct initial perception. This phenomenon illustrates that long reasoning chains can undermine multimodal grounding rather than reinforcing it.

Independent variables include reasoning chain length, prompt-directed look-back triggers, and periodic visual token re-injection. Dependent variables track attention entropy over image tokens, step-level hallucination rate, and overall trajectory accuracy. Controlled interventions interleave visual verification prompts or scheduled look-back tokens during autoregression. Baselines comprise standard chain-of-thought, direct answer generation (No-Thinking), and post-hoc textual self-correction. Target datasets include MathVista, V\*-Bench, and multi-step subsets of ChartQA.

The primary research question tests whether prompt-scheduled visual re-examination halts the decay of image-token attention entropy and rescues late-stage reasoning errors. A meaningful negative result occurs if re-examination prompts increase token length and rationalization phrases without increasing cross-attention to visual tokens or improving accuracy. Feasibility hazards stem from per-sample inference latency, requiring bounded context lengths on Colab Pro.

### **Family 5: Visual-Token Compression and Selective Evidence Pruning**

Visual-token pruning and compression techniques exhibit non-uniform evidence degradation across distinct visual task types. Discarding visual tokens accelerates inference and preserves macro-level benchmark scores, but can eliminate tokens containing small objects, text fragments, and fine coordinates. This failure mode constitutes silent evidence destruction, where high-level scene classification remains stable while local factual reasoning fails. This establishes a tension between inference efficiency and perceptual reliability that aggregate benchmark averages obscure.

Independent variables include token retention ratio (10% to 100%) and pruning mechanism (spatial pooling, attention-norm, or coverage-based selection). Dependent variables encompass task-stratified accuracy, token attribution density, and fine-grained error rates. The controlled intervention applies training-free pruning across stratified task tiers (global classification vs. small-object counting vs. dense OCR). Baselines include full-token models, random token dropout, and uniform bilinear spatial pooling. Evaluated benchmarks include DocVQA, TextVQA, POPE, and Visual Spatial Reasoning (VSR).

The primary research question asks whether visual-token pruning disproportionately harms localized spatial and textual evidence while preserving global scene comprehension. A meaningful negative result occurs if accuracy degrades at identical rates across fine-grained and global tasks, refuting the hypothesis of selective locality destruction. The primary feasibility hazard is the technical difficulty of hooking into internal transformer attention layers; researchers must leverage standardized, modular pruning codebases.

### **Family 6: Modality Attribution, Modality Gaps, and Feature Contribution**

Post-hoc feature attribution methods diverge from counterfactual causal reliance in vision-language models. Saliency heatmaps frequently highlight an image region even though removing that region produces no change in output logits. This manifests as spurious visual grounding, where attention visualizations act as post-hoc rationalizations rather than faithful representations of decision drivers. Evaluating multimodal interpretability requires confirming whether visual attributions reflect true counterfactual mechanisms.

Independent variables include attribution methodology (integrated gradients, attention rollout, counterfactual ablation) and model scale. Dependent variables track deletion-curve area under the curve (AUC), Modality Dominance Score (MDS), and counterfactual faithfulness. The controlled intervention masks image patches in descending order of attributed importance and measures logit degradation. Baselines comprise random patch masking, raw cross-attention weights, and input gradient norms. Datasets include controlled synthetic shapes/attributes, PointingQA, and GQA.

The primary research question asks whether gradient-based saliency methods correlate with counterfactual pixel interventions better than raw cross-attention weights. A meaningful negative result occurs if saliency-guided deletions degrade performance no faster than random patch masking, demonstrating that existing saliency maps lack causal fidelity. Computing full integrated gradients on multi-billion-parameter models is computationally prohibitive on Colab; lightweight perturbation-based approximations are necessary.

### **Family 7: Missing-Modality Dynamics and Graceful Degradation**

Multimodal systems display unstable degradation behavior when an input modality is omitted at inference time. When a model receives an image without a query, or a query with a blank image, its internal activation dynamics often destabilize due to joint-pretraining assumptions. This produces abrupt output collapse or repetitive hallucination loops when input channels are incomplete. Practical deployments frequently face dropped feeds, corrupted files, or missing metadata, necessitating graceful degradation to unimodal behavior.

Independent variables include missingness configuration (missing image, missing text, missing localized patch) and input replacement values. Dependent variables include prediction perplexity, hallucination frequency, and confidence calibration. The controlled intervention supplies blank frames, Gaussian noise, or learned missing-token embeddings across multimodal tasks. Baselines consist of native unimodal text models and standard zero-shot VLM inference. Suitable datasets include ScienceQA and MMBench paired with unimodal controls.

The primary research question asks whether explicit missing-modality token prompting outperforms raw image blanking in preventing hallucination when visual inputs are lost. A meaningful negative result occurs if replacing missing images with explicit prompt flags yields identical performance to black frames, indicating that cross-modal layers do not leverage explicit missingness markers. Feasibility hazards are minimal for this family, as it requires only inference-only perturbations.

### **Family 8: Multimodal Counterfactual Faithfulness and Invariance**

Vision-language models frequently fail to update inferential conclusions under controlled counterfactual visual edits. When an image attribute is modified (such as changing an apple from red to blue), the model often continues to predict the original attribute because linguistic priors override visual evidence. This failure mode represents parametric memory override, where memorized real-world training associations supersede physical pixel observations. This boundary determines whether multimodal models perform genuine perceptual grounding or simply retrieve memorized correlations.

Independent variables focus on the nature of the counterfactual visual edit (color, size, object count, physical orientation). Dependent variables measure counterfactual update accuracy, parametric retention rate, and answer flip probability. Controlled interventions generate minimal counterfactual edits on natural images paired with invariant control queries. Baselines evaluate clean image performance and text-only counterfactual prompts. Testbeds include Visual-Counterfact, Insight Over Sight, and Counterfactual VQA.

The central research question evaluates whether parametric override correlates positively with the frequency of the object in pretraining corpora, holding visual edit salience constant. A meaningful negative result occurs if counterfactual update success is independent of real-world object frequency, refuting the hypothesis that web-scale memorization drives parametric override. Generating diffusion-based counterfactual images is difficult to standardize; researchers should evaluate pre-curated counterfactual datasets.

### **Family 9: Test-Time Adaptation and Shortcut Formation under Distribution Shift**

Unsupervised test-time parameter adaptation can encourage the formation of spurious shortcuts under distribution shift. When adapting a model on the fly to blurry or stylized images, target benchmark scores often improve because the model exploits background artifacts rather than acquiring robust representations. This produces spurious alignment, where adapted weights elevate accuracy on corrupted benchmarks while degrading clean cross-modal grounding. While unsupervised adaptation is widely explored for domain robustness, its impact on internal cross-modal evidence use remains largely unverified.

Independent variables include adaptation algorithm (Test-Time Prompt Tuning, Tent, dynamic LoRA) and visual corruption category (blur, weather, artistic style). Dependent variables track clean source accuracy retention, out-of-distribution accuracy, and evidence attribution faithfulness. The controlled intervention performs test-time updates and measures both target accuracy and shortcut reliance. Baselines include frozen zero-shot VLMs and linear probing. Applicable datasets combine ImageNet-C/R with VQA adaptations.

The primary research question asks whether test-time entropy minimization on corrupted images preserves genuine visual grounding or accelerates collapse toward dominant textual priors. A meaningful negative result occurs if test-time adaptation improves out-of-distribution accuracy while preserving clean visual attention maps, demonstrating that adaptation does not sacrifice grounding integrity. The main feasibility risk is the instability of streaming optimization on Colab Pro.

### **Family 10: Cross-Lingual Morphological Fragmentation and Modality Reliance**

Subword tokenizer fragmentation in non-Latin scripts causally shifts cross-modal reliance in vision-language models. When an Indic or low-resource query is fragmented into numerous subword pieces, the model's textual processing is compromised, altering how it utilizes the visual stream. This failure mode represents morphological-shattering vulnerability, where subword splitting impairs textual representations and forces asymmetric reliance on visual tokens. This provides a mechanistic, linguistically grounded explanation for cross-lingual performance gaps beyond generic claims of data scarcity.

Independent variables include query script/language (English vs. Bengali native vs. Bengali romanized) and token fertility ratio (subword tokens per word). Dependent variables measure modality reliance scores, cross-modal attention ratios, and visual ablation sensitivity (\\Delta\_{\\text{vis}}). The controlled intervention translates identical VQA prompts into Bengali and measures visual dependency as a function of subword token fertility. Baselines comprise original English prompts, morpheme-aligned tokenized text (e.g., SuTRA-style segmentation), and text-only IndicLLMs. Benchmarks include BanglaVerse, IndicVQA, and translated subsets of TextVQA.

The primary research question asks whether higher subword token fertility in Bengali queries correlates with increased reliance on visual tokens relative to syntactically equivalent English queries. A meaningful negative result occurs if visual dependency remains identical between English and Bengali queries across token fertility levels, showing that tokenizer fragmentation does not alter cross-modal reliance. Feasibility requires native linguistic verification to eliminate translation artifacts.

### **Family 11: Claim-Level Visual Verification and Hallucination Control**

Vision-language models exhibit a structural asymmetry between multi-claim generation fluency and localized visual support. A model often generates a detailed description where several facts are visually supported, but ungrounded assertions are interspersed seamlessly throughout the response. This failure mode represents partial hallucination acceptance, where fluent truthful details mask isolated false assertions. Coarse-grained hallucination metrics (such as binary sample-level labels) obscure these fine-grained factual calibration dynamics.

Independent variables involve claim granularity (sentence-level vs. subject-predicate-object triple) and verification prompting structure. Dependent variables measure claim precision, unnecessary correction rate, and net factual accuracy. The controlled intervention decomposes responses into atomic claims and prompts the VLM to verify each claim against cropped image regions. Baselines consist of end-to-end generation, standard CoT, and monolithic self-correction. Testbeds include POPE, M-HalDetect, and HallusionBench.

The research question asks whether isolated claim-level visual verification increases factual precision without causing false-positive retractions of valid details. A meaningful negative result occurs if atomic verification prompts reduce hallucinations only by aggressively deleting ambiguous but valid claims, yielding zero net improvement in precision. The primary feasibility hazard is the cost of evaluating free-form claims, which can be addressed by focusing on structured QA triples.

### **Family 12: Multimodal Benchmark Validity, Contamination, and Shortcut Auditing**

Benchmark score inflation frequently stems from unimodal linguistic mutual information and pretraining contamination. Modern VLMs can achieve high scores on multimodal benchmarks even when visual inputs are completely removed or masked. This failure mode represents benchmark shortcut exploitation, where evaluation metrics measure language-prior matching rather than genuine cross-modal reasoning. Auditing shortcut pathways is necessary to identify inflated performance claims in the multimodal literature.

Independent variables include multimodal input masking (image-blind, text-blind, option-scrambled) and question phrasing variations. Dependent variables track unimodal baseline scores, multimodal gain scores (\\text{Score}\_{\\text{multimodal}} \- \\text{Score}\_{\\text{blind}}), and model ranking stability. The controlled intervention audits standard benchmark splits by evaluating open models under complete visual ablation and randomizing answer option orders. Baselines comprise published official benchmark scores and uniform random guessing. Applicable datasets include MMMU, MathVista, ScienceQA, and BanglaVerse.

The research question asks what percentage of benchmark items in domain-specific multimodal benchmarks can be solved above chance without image inputs. A meaningful negative result occurs if all audited benchmarks exhibit near-chance accuracy without visual inputs, confirming that current benchmarks are resistant to unimodal shortcuts. While computationally lightweight, pure auditing studies risk limited scientific novelty unless paired with a mechanistic intervention.

# **C. Literature map**

The vision-language research ecosystem between 2024 and 2026 has transitioned from scaling models toward diagnosing why multimodal networks fail to ground their representations in physical evidence. The major empirical and methodological efforts cluster across five primary axes:

The first axis examines conflict arbitration and modality dominance. Catapang (2026) introduced CMC-Bench, demonstrating that cross-modal disagreement induces accuracy drops between 17% and 46% and exposes systematic Modality Preference Bias (MPB) across open-weight models. In parallel, *Which Source Wins? Task-Dependent Reliance in Vision-Language Models* (2026) demonstrated that modality reliance is not a fixed architectural trait: models shift away from text in arithmetic conflicts, but shift away from visual inputs in chart-based conflicts. Kim, Prabhushankar, and AlRegib (2026) introduced MoIR, showing that modality dominance manifests as an information disparity occurring prior to fusion, which can be mitigated by routing information across channels via truncated singular value decomposition (SVD). Complementary benchmarks like Visual-Counterfact (2026) and SIGNPOST-Bench (2026) confirm that conflict failures stem from arbitration mechanisms rather than perception errors.

The second axis focuses on multi-step reasoning and visual grounding drift. Peng, Lv, and Hu (2026) introduced ReGround, proving that during extended reasoning chains, attention entropy over image tokens steadily decreases, causing models to revert to language priors. Concurrently, *Visual Re-Examination in MLLMs* (2026) demonstrated that models possess a latent ability for implicit visual look-backs that can be unlocked through reflection prompting. In contrast, *Think-After-Answer* (2025/2026) demonstrated that explicit chain-of-thought thinking can degrade visual perception tasks during reinforcement fine-tuning, whereas direct answering converges faster and achieves higher final accuracy. Counterfactual Preference Optimization \++ (2026) established that autoregressive decoding triggers internal visual drift, which can be penalized to maintain visual grounding.

The third axis investigates visual-token efficiency and evidence pruning. While early pruning methods focused primarily on speedup, 2026 studies such as *CoverPruner* (Zhu et al., 2026\) formulate pruning as representational coverage maximization, retaining up to 80% of accuracy under aggressive compression. Similarly, *ATV-Pruning* (2026) documented asymmetric pruning sensitivity across modalities, proving that the visual pathway can tolerate up to 60% unstructured sparsity with minimal macro-benchmark loss. However, *How Many Visual Tokens Do Multimodal Language Models Need?* (2026) noted that average benchmark preservation conceals how pruning affects localized, fine-grained evidence.

The fourth axis explores modality attribution and geometric gaps. Yan et al. (2026) proposed the Modality Dominance Score (MDS), measuring geometric distance in representation space to quantify modality separation. Complementary work in *Which Modality Decides?* (2026) formulated Counterfactual Modality Attribution (CMA) via Shapley values, demonstrating that gradient-based feature attribution diverges substantially from causal counterfactual reliance. In parallel, *Visuals Lie, Consistency Speaks* (2026) challenged attention-based explainability by showing near-zero correlation between spatial attention metrics and correctness, whereas internal hidden states provide reliable confidence signals.

The fifth axis analyzes cross-lingual transfer and low-resource multimodal representations. In text-only NLP, *SuTRA* (2026) demonstrated that standard subword tokenizers induce severe "morphological shattering" in Indic scripts, leading to high token fertility. Multimodal benchmarks such as *VLURes* (2026) and *BanglaVerse* (2026) observed that cross-lingual gaps persist in long-text grounding and cultural reasoning, while domain frameworks like *Multimodal Cross-Attention Fusion* (2026) demonstrated that cross-attention mechanisms help ground low-resource multimodal tasks like Bengali meme classification.

# **D. Occupied questions**

The following research questions are heavily explored or resolved in the recent literature and should not serve as primary undergraduate thesis topics:

> 1. Can visual-token pruning reduce inference latency without hurting average benchmark accuracy? This question is occupied by extensive 2025–2026 literature, including *How Many Visual Tokens Do Multimodal Language Models Need?*, *CoverPruner*, *VisionTrim*, and *ATV-Pruning*. These works establish that 50% to 70% of visual tokens can be removed with negligible degradation on aggregate benchmarks such as MMBench or ScienceQA. Demonstrating that token pruning saves memory while maintaining aggregate task scores is well understood.  
> 2. Do vision-language models uniformly prefer text over images? This formulation is occupied and contradicted by recent findings. *Which Source Wins?* (2026) demonstrates that modality reliance is task- and structure-dependent: models shift away from text in arithmetic conflicts, but shift away from visual inputs in chart-based conflicts. Catapang (2026) similarly demonstrates task-conditioned modality preference across ChartQA and MMMU. Treating modality dominance as a static preference ignores established task-contingent reversals.  
> 3. Can we build a new general benchmark for multimodal hallucination or Bengali VQA? This area is crowded with benchmarks including POPE, AMBER, HallusionBench, M-HalDetect, BanglaVerse, and BLEnD-Vis. Assembling another general VQA dataset or basic Bengali image-caption evaluation provides limited scientific insight unless paired with an experimental intervention.  
> 4. Does visual attention explain why a VLM gets an answer right? This assumption has been directly evaluated and challenged. *Visuals Lie, Consistency Speaks* (2026) demonstrates near-zero correlation between spatial attention metrics and correctness across LLaVA-1.5, PaliGemma, and Qwen2-VL. Asserting that attention maps serve as direct explanations of model reliability is empirically unsupported.  
> 5. Can parameter-efficient fine-tuning (LoRA) improve out-of-distribution VLM performance? This application is documented across standard adaptation literature (e.g., *MuRA*, 2026). Applying LoRA or QLoRA to a shifted visual distribution and reporting marginal accuracy gains does not answer an open scientific question.

# **E. Partially explored questions**

The following scientific questions have been established at a high level, but critical boundary conditions and mechanistic interactions remain open:

> 1. Does explicit conflict detection improve arbitration decisions or merely increase verbal rationalization? Recent work demonstrates that cross-modal contradictions trigger modality dominance failures, but these evaluations force models into direct single-choice answers. They do not establish whether requiring a model to explicitly classify conflict status before answering improves decision accuracy or merely generates ungrounded explanatory text.  
> 2. Does visual-token compression selectively destroy localized evidence while preserving global understanding? Current token-reduction studies evaluate overall benchmark performance retention. However, whether compression exhibits an interaction effect with evidence locality—selectively degrading fine-grained spatial coordinates, dense numbers, and small text while leaving high-level scene semantics untouched—remains unquantified in a controlled multi-task audit.  
> 3. Does progressive evidence degradation induce calibrated uncertainty or uncalibrated fluency? *Which Source Wins?* (2026) notes as an explicit limitation that its degradation protocol does not test uncertainty calibration or selective abstention. It remains unverified whether predictive entropy tracks lost visual evidence or whether models maintain overconfident generation until complete failure.  
> 4. Can visual grounding drift in multi-step reasoning be arrested without external re-injection tools? *ReGround* (2026) relies on training-time capability bootstrapping and test-time image re-injection, while *Visual Re-Examination* (2026) investigates self-reflective traces. It remains partially explored whether inference-only, zero-shot structured prompts can restore visual attention entropy during multi-step reasoning without architectural modifications or retraining.  
> 5. Does subword tokenizer fragmentation in non-Latin scripts causally alter cross-modal reliance? Cross-lingual multimodal benchmarks document performance drops in low-resource and Indic languages. Concurrently, NLP literature demonstrates severe morphological shattering in Indic tokenizers. However, whether high tokenizer fragmentation causally forces the vision-language projection to lean more heavily on the visual channel remains an open hypothesis.

# **F. Underexplored questions**

The following candidate research questions survive adversarial audit, possess identifiable experimental manipulations, have clean baselines, and are executable on Colab Pro:

### **U1. Disagreement Recognition vs. Arbitration Fidelity**

When image and text inputs present mutually contradictory assertions, does forcing an explicit conflict-identification step improve the accuracy of the final answer, or does it merely produce unfaithful verbal rationalization while preserving the underlying modality dominance bias?

> * Independent Variable: Elicitation format (Direct Answer vs. Conflict Detection \+ Answer vs. Evidence Attribution \+ Answer).  
> * Dependent Variables: Arbitration accuracy, Modality Preference Bias (MPB), Contradiction Detection Accuracy, Explanation Faithfulness.  
> * Competing Hypotheses: Explicitly attending to cross-modal divergence breaks attention capture by the dominant modality and routes computation through reasoning tokens, versus early-layer cross-modal projection dynamics and parametric priors fixing the decision logit before rationalization tokens are generated.  
> * Negative Result: Explicit conflict detection increases verbal acknowledgment of contradiction while leaving final arbitration accuracy unchanged, proving that verbal reasoning is causally decoupled from decisional arbitration.

### **U2. Evidence-Sufficiency Calibration Under Progressive Masking**

When decisive visual evidence is systematically masked while preserving context, does a VLM's predictive uncertainty calibrate proportionally to the lost evidence, or does language fluency maintain artificially low entropy?

> * Independent Variable: Target patch masking ratio (0% to 100% of decisive bounding box) across answerable and unanswerable prompts.  
> * Dependent Variables: Predictive entropy, Expected Calibration Error (ECE), Brier score, selective risk at coverage \\alpha.  
> * Competing Hypotheses: Softmax distribution over candidate answers broadens as visual token embeddings lose discriminative information, versus autoregressive language decoding maintaining low-entropy predictions based on linguistic priors regardless of visual evidence ablation.  
> * Negative Result: Output entropy remains static across 0% to 100% masking, demonstrating that predictive confidence is evidence-blind and reflects autoregressive language fluency rather than evidential grounding.

### **U3. Locality-Dependent Evidence Destruction in Visual-Token Pruning**

Does training-free visual-token pruning exhibit a significant interaction effect with task evidence locality, selectively destroying fine-grained OCR, counting, and spatial evidence while preserving macro-semantic classification?

> * Independent Variable: Token retention ratio (100%, 75%, 50%, 25%, 10%) across diverse pruning criteria (spatial pooling vs. attention-norm vs. coverage maximization).  
> * Dependent Variables: Accuracy retention ratio, Hallucination rate (POPE), Fine-grained spatial/OCR error rate.  
> * Competing Hypotheses: Pruning mechanisms systematically favor high-variance global scene tokens, discarding isolated tokens carrying decisive localized evidence, versus visual features broadcasting redundantly across adjacent patches, allowing localized reasoning to survive aggressive pruning.  
> * Negative Result: Accuracy degrades at identical rates across both localized OCR/spatial tasks and global scene classification, refuting the hypothesis of selective locality destruction.

### **U4. Mitigation of Visual Grounding Drift via Structured Prompt Schedules**

In multi-step visual reasoning, can prompt-scheduled intermediate visual queries prevent visual drift and decay of attention entropy without external image re-injection?

> * Independent Variable: Reasoning protocol (Standard CoT vs. Prompt-Scheduled Visual Re-check vs. Direct Answer).  
> * Dependent Variables: Late-stage cross-attention weight on image tokens, final answer accuracy, step-level hallucination rate.  
> * Competing Hypotheses: Periodic prompt anchors trigger internal cross-attention mechanisms, forcing the decoder to re-attend to the visual prefix, versus increasing textual context length irreversibly diminishing visual attention weights due to softmax normalization over long sequences.  
> * Negative Result: Scheduled prompts produce surface-level re-examination phrases but fail to restore attention entropy on image tokens or rescue reasoning errors.

\#\#\# U5. Tokenizer Morphological Shattering as a Driver of Modality Bias Holding visual stimuli and semantic meaning constant, does the higher subword token fertility of Bengali queries causally increase the model's reliance on visual tokens compared to English queries?

> * Independent Variable: Query language/script (English vs. Bengali native vs. Bengali romanized) and token fertility level.  
> * Dependent Variables: Modality reliance score, visual ablation sensitivity (\\Delta\_{\\text{vis}}), output consistency.  
> * Competing Hypotheses: Fragmented textual representations exhibit higher semantic uncertainty, causally increasing the relative weight of visual embeddings in multi-head attention, versus tokenizer fragmentation degrading sentence comprehension and producing ungrounded errors without shifting visual reliance.  
> * Negative Result: Visual dependency remains identical between English and Bengali queries across token fertility levels, demonstrating that tokenizer fragmentation does not shift cross-modal reliance.

\---

# **G. Top 10 RQs**

| RQ | Scientific Phenomenon | Closest Work | What Remains Unknown | Dataset | Baseline | Main Metric | Leakage Risk | Compute | Novelty Confidence | Feasibility |
| :---- | :---- | :---- | :---- | :---- | :---- | :---- | :---- | :---- | :---- | :---- |
| 1 | Conflict Arbitration | Catapang (2026); Which Source Wins? (2026) | Does explicit conflict detection improve decisions or only rationalizations? | ChartQA-Conflict, CMC-Bench | Direct answer, Unimodal inputs | Paired arbitration accuracy, MPB | Medium (prompt cueing) | Low (inference only) | Strong | High |
| 2 | Evidence Sufficiency | Which Source Wins? (2026); EviVLM (2026) | Does confidence track lost visual evidence or reflect language fluency? | VizWiz, ChartQA with masked evidence | Softmax confidence, Maximum entropy | ECE, Brier score, Selective Risk | Low (objective masking) | Low (inference only) | Strong | High |
| 3 | Visual-Token Compression | CoverPruner (2026); ATV-Pruning (2026) | Does token pruning selectively destroy localized fine-grained evidence? | POPE, TextVQA, VSR, AI2D | Full-token, Uniform spatial pooling | Retention ratio, Interaction F-stat | Low (public benchmarks) | Medium (layer interventions) | Moderate | High |
| 4 | Visual Grounding Drift | ReGround (2026); VRE (2026) | Can zero-shot prompt schedules halt visual drift without retraining? | MathVista, V\*-Bench | Greedy CoT, Direct Answer | Image attention entropy, Accuracy | Medium (CoT template leak) | Medium (long generation) | Moderate | High |
| 5 | Cross-Lingual Modality Bias | SuTRA (2026); VLURes (2026) | Does tokenizer shattering force higher reliance on visual evidence? | Parallel English-Bengali VQA | English query baseline, Text-only IndicLLM | Modality reliance shift, \\Delta\_{\\text{vis}} | High (translation quality) | Low (inference only) | Moderate | Medium |
| 6 | Claim-Level Verification | CoRGI (2025); ReGround (2026) | Does atomic verification improve precision without over-retraction? | M-HalDetect, POPE | End-to-end generation, Self-correction | Claim precision, Net correction rate | Medium (parsing artifacts) | Medium (multi-call) | Moderate | Medium |
| 7 | Modality Attribution | Beyond Alignment / MDS (2026); CMA (2026) | Do saliency maps match counterfactual ablation across balanced tasks? | GQA, PointingQA | Random patch masking, Cross-attention rollout | Deletion-curve AUC, Faithfulness | Low (counterfactual images) | Medium (multiple passes) | Moderate | Medium |
| 8 | Missing-Modality Fallback | Missing Modality Restoration (2026) | Does explicit missingness signaling prevent hallucination loops? | ScienceQA, MMBench (blanked) | Zero-image baseline, Text-only model | Perplexity, Hallucination frequency | Low (direct ablations) | Low (inference only) | Weak–Mod | High |
| 9 | Test-Time Adaptation Shortcuts | MuRA (2026); MoIR (2026) | Does test-time entropy minimization strengthen shortcut reliance? | ImageNet-C, corrupted VQA subsets | Frozen zero-shot VLM | Target accuracy vs. Grounding drift | High (streaming order) | High (TTA optimization) | Moderate | Low |
| 10 | Benchmark Validity Audit | Mega-Bench (2024); Scalable Bench Gen (2025) | What fraction of multi-image reasoning is solvable via language alone? | MMIU, MultiHaystack | Text-only blind LLM, Shuffled image | Blind accuracy, Shortcut score | Low (direct audit) | Low (inference only) | Weak (pure audit) | High |

# **H. Top 5**

### **1\. Disagreement Recognition vs. Arbitration Fidelity in Cross-Modal Conflicts**

This inquiry addresses the tension between explicit conflict awareness and decisional arbitration under cross-modal contradiction.

The closest investigation is Catapang (2026), which benchmarked 3,768 instances from ChartQA and MMMU across four open VLMs and established that cross-modal conflict degrades accuracy by 17% to 46%, exposing systematic Modality Preference Bias (MPB). However, Catapang evaluated models exclusively under forced-choice generation settings and did not examine whether prompting for conflict detection alters or repairs MPB.

A second closely related study, *Which Source Wins? Task-Dependent Reliance in Vision-Language Models* (2026), evaluated six open VLMs across GSM8K, SVAMP, and ChartQA under source degradation. It established that reliance shifts are task-dependent (text-leaning in arithmetic, image-leaning in charts), but explicitly identified in its limitations that it did not evaluate uncertainty, contradiction detection, or abstention.

A third related work by Kim, Prabhushankar, and AlRegib (2026) proposed MoIR, an architectural module routing information via truncated SVD prior to LLM decoding. While MoIR establishes that modality dominance is an information-availability issue, it requires architectural intervention and fine-tuning.

The gap boundary is well-defined: existing work establishes that cross-modal contradictions induce performance degradation and task-dependent modality dominance, but it does not establish whether prompting a model to explicitly detect and classify contradiction status breaks this dominance, or whether the final decision remains bound to the pre-existing logit bias. The proposed experiment tests this boundary by holding contradiction stimuli fixed and manipulating the elicitation path (direct answering vs. conflict detection followed by answering).

### **2\. Evidence-Sufficiency Calibration Under Progressive Visual Masking**

This question evaluates cross-modal predictive overconfidence and calibration failure under incomplete evidence regimes.

The closest investigation is *Which Source Wins?* (2026), which degraded image and text sources across mathematical and chart reasoning, showing asymmetrical reallocation. However, the authors did not measure predictive uncertainty, calibration error, or selective risk.

A second related investigation, *Visuals Lie, Consistency Speaks* (2026), probed reliability signals across LLaVA-1.5, PaliGemma, and Qwen2-VL, showing that attention geometry does not correlate with correctness (R \\approx 0), whereas self-consistency and internal probes correlate moderately (R \= 0.429). That study evaluated static benchmarks and did not evaluate progressive, controlled evidence ablation ladders.

A third related study, Catapang (2026), evaluated abstention versus fabrication in multimodal RAG conflicts, showing that Qwen3-VL-4B abstains on 31.7% of conflicts while Gemma-3n-E2B fabricates on 51.9%. However, Catapang evaluated fixed conflicting retrievals without parametrically varying the degree of evidence removal.

The gap boundary is specific: existing work establishes that VLMs hallucinate under unanswerable conditions and that attention is a poor proxy for reliability, but it does not test how predictive confidence scales when decisive visual evidence is parametrically ablated in continuous increments. The proposed experiment tests this by applying localized bounding-box masking ladders (0%, 25%, 50%, 75%, 100%) to chart and natural VQA tasks and measuring the response curve of output entropy and selective risk.

### **3\. Locality-Dependent Evidence Destruction in Visual-Token Pruning**

This investigation isolates the selective failure of localized fine-grained evidence under visual token compression.

The closest related work, *CoverPruner* (Zhu et al., 2026), introduced representational coverage maximization, demonstrating that up to 80% of tokens can be pruned while maintaining overall benchmark accuracy. However, CoverPruner focused entirely on aggregate accuracy and FLOP reductions, omitting stratified evaluations across evidence locality or spatial reasoning bounds.

A second study, *How Many Visual Tokens Do Multimodal Language Models Need?* (2026), evaluated token demand across Qwen3-VL models (2B to 235B) across eleven benchmarks. The authors explicitly highlighted in their limitations that evidence-level reliability and counterfactual behavior under compression remain unstudied.

A third related paper, *ATV-Pruning* (2026), identified asymmetric pruning sensitivity across modalities (the text pathway is sensitive, whereas the visual pathway tolerates up to 60% sparsity). However, ATV-Pruning focused on model weight pruning rather than inference-time dynamic token selection.

The gap boundary is clear: existing work establishes that visual tokens can be removed with minimal impact on aggregate benchmark scores, but it does not establish whether this aggregate preservation conceals catastrophic failures on tasks where decisive evidence occupies a tiny spatial footprint. The proposed experiment tests this by evaluating multiple pruning policies across a multi-task ladder stratified by evidence area (bounding box percentage of total image area).

### **4\. Visual Grounding Drift vs. Zero-Shot Prompt Schedules in Multi-Step Reasoning**

This inquiry addresses attention decay over visual prefix tokens during long autoregressive generation.

The closest study is *ReGround* (Peng, Lv, and Hu, 2026), which documented that attention entropy over image tokens steadily decreases during reasoning across 2,510 samples. ReGround solved this via capability bootstrapping from a 72B teacher and test-time image re-injection.

A second study, *Visual Re-Examination in MLLMs* (2026), identified the visual drift bottleneck and developed an RLVR-SFT self-evolution training framework to induce visual look-backs, requiring extensive reinforcement fine-tuning.

A third study, *Think-After-Answer* (2025/2026), showed that explicit thinking processes can degrade visual perception tasks during reinforcement fine-tuning, whereas direct answering converges faster and achieves higher accuracy.

The gap boundary is distinct: existing work establishes that long-chain reasoning induces visual grounding drift and that heavy training frameworks (RLVR, bootstrapping) or physical image re-injection can counteract it, but it does not test whether simple, inference-only prompt-scheduling interventions (e.g., forcing intermediate structured perceptual grounding checkpoints) can halt attention entropy decay in frozen open models.

### **5\. Morphological Tokenizer Fragmentation and Asymmetric Modality Reliance in Indic VLMs**

This question investigates cross-modal reliance shifting induced by subword segmentation fragmentation in morphologically rich scripts.

The closest study, *SuTRA* (2026), documented severe morphological shattering and high token fertility (Indic Tax) in standard BPE tokenizers across Hindi, Marathi, and Gujarati. However, SuTRA focused exclusively on text-only NLP and detokenization purity, without evaluating multimodal grounding.

A second investigation, *VLURes* (2026), evaluated long-text multimodal grounding across high- and low-resource languages across 10 VLMs, demonstrating that cross-lingual sensitivity persists. However, it treated language shift as an empirical black box without isolating tokenizer fertility.

A third paper, *Which Source Wins?* (2026), established that degrading text legibility shifts reliance toward visual inputs, but evaluated synthetic character-level corruption in English rather than natural morphological fragmentation across languages.

The gap boundary centers on this mechanism: existing work establishes that subword tokenizers fragment Indic text and that degrading textual readability shifts VLM reliance toward vision, but it does not test whether natural tokenizer fragmentation across languages acts as an organic legibility degrader that shifts cross-modal attention toward the visual stream.

# **I. Top 3**

### **Top 1: Disagreement Recognition vs. Arbitration Fidelity in Cross-Modal Conflicts**

The investigation into disagreement recognition versus arbitration fidelity evaluates whether explicit contradiction awareness translates into reliable decisional arbitration. Recent studies demonstrate that VLMs experience severe performance drops of 17% to 46% when image and text inputs present mutually contradictory assertions. However, existing benchmarks evaluate models under forced single-choice generation settings.

Existing work establishes that cross-modal conflict induces systematic Modality Preference Bias, that modality dominance reverses between arithmetic and chart reasoning tasks, and that dominance can be adjusted by retraining cross-modal projection modules with SVD-based information routing. Existing work does not establish whether a frozen VLM prompted to explicitly recognize, localize, and state a contradiction can overcome its intrinsic modality dominance to arbitrate correctly, or whether contradiction awareness is functionally decoupled from decision arbitration. The proposed experiment manipulates the elicitation path across matched arithmetic and chart conflict stimuli to measure its causal effect on final arbitration accuracy and Modality Preference Bias.

Two competing hypotheses explain this interaction:

> * Deliberative Arbitration Hypothesis: Generating an intermediate token sequence that identifies the contradiction forces the autoregressive attention mechanism to attend to tokens from both modalities, breaking unimodal attention capture and restoring balanced arbitration.  
> * Post-Hoc Rationalization Hypothesis: The final decision token is determined by early-layer cross-modal projection dynamics and parametric priors; prompting for conflict detection produces superficial linguistic commentary without altering the dominant logit trajectory.

The minimum experimental design applies a 2 \\times 4 \\times 3 factorial structure. Factor 1 tests Domain Benchmark (ChartQA-Conflict vs. GSM8K-Conflict). Factor 2 tests Evidence Alignment Condition (Aligned Gold, Image-Correct/Text-False, Text-Correct/Image-False, Insufficient-Both). Factor 3 tests Elicitation Protocol (Direct Answer, Conflict-Aware Prompting, Evidence Attribution Prompting).

| Protocol | Prompt Structure | Model Task |
| :---- | :---- | :---- |
| Direct Answer | \[Image\] \[Question\] Output only the final answer. | Direct generation |
| Conflict-Aware | \[Image\] \[Question\] Step 1: State whether the image and text agree or conflict. Step 2: Provide the final correct answer. | Detection then prediction |
| Evidence Attribution | \[Image\] \[Question\] Step 1: Extract evidence from Image. Step 2: Extract evidence from Text. Step 3: Identify discrepancies. Step 4: Final answer. | Decomposed audit |

Evaluation relies on three primary metrics. Arbitration Accuracy (Acc\_{\\text{arb}}) evaluates accuracy strictly on conflicting instances where exactly one modality supports the ground truth:

Acc\_{\\text{arb}} \= \\frac{1}{\\vert{}D\_{\\text{conf}}\\vert{}} \\sum\_{i \\in D\_{\\text{conf}}} \\mathbb{I}(\\hat{y}\_i \= y\_i^\*)

Modality Preference Bias toward images (MPB\_{\\text{img}}) among conflict errors isolates channel leaning:

MPB\_{\\text{img}} \= \\frac{\\sum\_{i \\in D\_{\\text{conf}}} \\mathbb{I}(\\hat{y}\_i \= y\_{\\text{img}})}{\\sum\_{i \\in D\_{\\te\[span\_95\](start\_span)\[span\_95\](end\_span)xt{conf}}} \[\\mathbb{I}(\\hat{y}\_i \= y\_{\\text{img}}) \+ \\mathbb{I}(\\hat{y}\_i \= y\_{\\text{txt}})\]}

The paired intervention gain (\\Delta\_{\\text{arb}}) measures the delta between intervention and direct generation:

\\Delta\_{\\text{arb}} \= Acc\_{\\text{arb}}(\\text{Intervention}) \- Acc\_{\\text{arb}}(\\text{Direct})

Evaluation risks require strict controls. Prompt cueing leakage—where prompting the model to look for conflicts causes it to hallucinate disagreement on aligned inputs—is mitigated by evaluating an equal 50/50 mix of aligned and conflicting items. Surface formatting shortcuts are controlled by generating conflicting text using identical syntactic templates to the gold text. Option-ordering bias is controlled by randomizing candidate choice orders across inference runs.

The implementation relies on public artifacts (multimodal-arbitration-artifact), requires no manual annotation, and operates via inference-only script execution. Evaluating 1,000 items across three prompt conditions requires approximately 6,000 forward passes, executing in under 2.5 hours on a single Colab Pro T4 or V100 GPU.

### **Top 2: Evidence-Sufficiency Calibration Under Progressive Visual Masking**

Evidence-sufficiency calibration examines how predictive uncertainty responds when decisive visual evidence is parametrically removed. Modern VLMs produce overconfident hallucinations when visual queries contain false premises or missing details. While attention geometry fails to correlate with correctness (R \\approx \[span\_368\](start\_span)\[span\_368\](end\_span)0), and likelihood margins shift under coarse image blur, the functional relationship between predictive uncertainty and continuous, physical evidence ablation remains unmapped.

Existing work establishes that models produce hallucinations on unanswerable inputs and that internal probes provide better error detection than attention maps. Existing work does not establish whether output token entropy, sequence margins, or selective risk calibrate smoothly to the fractional removal of decisive visual evidence, or whether confidence remains frozen at an overconfident baseline until an arbitrary collapse threshold. The proposed experiment establishes this functional response curve by masking decisive bounding-box regions in continuous increments.

Two competing hypotheses explain uncertainty behavior under evidence loss:

> * Information-Theoretic Calibration Hypothesis: As physical evidence is occluded, cross-modal attention distributes probability across competing vocabulary tokens, yielding an entropy increase that tracks evidence loss monotonically.  
> * Linguistic Autoregressive Inertia Hypothesis: Visual tokens provide weak steering signals relative to language priors; autoregressive decoding maintains sharp, low-entropy predictions regardless of whether the visual patch contains decisive information or blank pixels.

The experimental design applies an evidence-ablation ladder across 500 samples from DocVQA and ChartQA where ground-truth answer coordinates are known. Masking is applied to the decisive bounding box in five steps: 0% masked (clean baseline), 25% masked, 50% masked, 75% masked, and 100% masked (fully ablated evidence). A control condition applies identical masking areas to task-irrelevant visual background patches to verify that degradation is caused by evidence removal rather than general visual distortion.

| Masking Step | Visual Intervention | Target Information State |
| :---- | :---- | :---- |
| Step 0 | 0% Area of Target Bounding Box Masked | Full Evidence Baseline |
| Step 1 | 25% Area of Target Bounding Box Masked | Minor Occlusion / Legible |
| Step 2 | 50% Area of Target Bounding Box Masked | Critical Occlusion / Ambiguous |
| Step 3 | 75% Area of Target Bounding Box Masked | Sub-threshold Evidence |
| Step 4 | 100% Area of Target Bounding Box Masked | Zero Decisive Evidence |
| Control | Equivalent Area Masked on Background | Non-Informative Occlusion Control |

Evaluation tracks Normalized Sequence Entropy (H\_{\\text{seq}}) across generated tokens:

H\_{\\text{seq}} \= \-\\frac{1}{K} \\sum\_{k=1}^K \\sum\_{v \\in V} P(v \\vert{} t\_{\<k}, I) \\log P(v \\vert{} t\_{\<k}, I)

Calibration quality is quantified via Expected Calibration Error (ECE) across confidence bins B\_m:

\\text{ECE} \= \\sum\_{m=1}^M \\frac{\\vert{}B\_m\\vert{}}{N} \\vert{}\\text{acc}(B\_m) \- \\text{conf}(B\_m)\\vert{}

Selective Risk at Coverage \\alpha (R(\\alpha)) measures decision accuracy when the model is permitted to abstain on queries with confidence below threshold \\tau\_\\alpha:

R(\\alpha) \= \\mathbb{E}\_{(\\hat{y}, y^\*)} \[\\ell(\\hat{y}, y^\*) \\vert{} c \\ge \\tau\_\\alpha\]

The sensitivity slope (\\beta\_{\\text{mask}}) is estimated via linear regression (H\_{\\text{seq}} \= \\beta\_{\\text{mask}} \\cdot M \+ \\epsilon).

Evaluation risks center on contextual redundancy—where answers appear in both chart legends and axis titles—which is prevented by using OCR bounding-box registries to verify that all instances of the answer string are occluded. Language-only leakage is controlled by testing queries with a blind text-only LLM. The protocol requires approximately 3,000 forward passes, executing in under 1.5 hours on Colab Pro.

### **Top 3: Locality-Dependent Evidence Destruction in Visual-Token Pruning**

Visual-token pruning investigations examine whether compression mechanisms selectively destroy localized fine-grained evidence. Current pruning techniques report that 50% to 70% of visual tokens can be discarded without harming macro-benchmark accuracy on datasets such as MMBench or ScienceQA. However, these benchmarks are dominated by coarse-grained visual recognition and conversational reasoning.

Existing work establishes that token pruning accelerates inference and reduces KV-cache memory, that attention-guided pruning outperforms random dropping on aggregate metrics, and that pruning sensitivity is asymmetric across modalities. Existing work does not establish whether aggregate accuracy preservation conceals systematic failures on tasks where decisive evidence occupies a tiny spatial footprint. The proposed experiment tests the statistical interaction between token retention ratio and evidence locality tier across multiple pruning policies.

Two competing hypotheses explain performance under token compression:

> * Selective Locality Destruction Hypothesis: Attention-norm and clustering pruning methods favor tokens from large, homogeneous image regions with high collective attention mass, systematically discarding isolated tokens carrying decisive localized evidence.  
> * Uniform Semantic Redundancy Hypothesis: Visual representations in pretrained vision transformers diffuse semantic information across adjacent patch tokens, allowing localized factual reasoning to survive aggressive pruning.

The experimental design structures evaluation across three stratified visual task tiers using Qwen2.5-VL-3B-Instruct: Tier 1 (Macro-Scene) evaluates scene classification and high-level activity recognition on MMBench; Tier 2 (Medium-Object) assesses object existence and hallucination on POPE; and Tier 3 (Micro-Locality) evaluates fine-grained text extraction on TextVQA and spatial positioning on Visual Spatial Reasoning (VSR). Four pruning conditions are evaluated: Full Tokens (100%), Uniform Spatial Pooling, First-Layer Attention-Norm Pruning (FastV-style), and Coverage Maximization Pruning (CoverPruner-style).

| Task Tier | Benchmark Dataset | Target Visual Evidence Footprint | Primary Evaluation Metric |
| :---- | :---- | :---- | :---- |
| Tier 1: Macro-Scene | MMBench (Scene Subset) | Global Scene Semantics (\>50% image area) | Accuracy Retention Ratio (ARR) |
| Tier 2: Medium-Object | POPE (Random & Adversarial) | Medium Object Existence (10%–50% area) | Hallucination Rate / F1 Score |
| Tier 3: Micro-Locality | TextVQA & VSR | Localized Text & Coordinates (\<10% area) | Exact Match / Spatial Accuracy |

Evaluation measures the Accuracy Retention Ratio (ARR\_{k,r}) for task tier k at retention ratio r:

ARR\_{k,r} \= \\frac{\\text{Accuracy}\_{k}(r)}{\\text{Accuracy}\_{k}(1.0)}

The primary hypothesis is tested via two-way ANOVA modeling:

\\text{Error} \\sim \\text{Retention} \+ \\text{LocalityTier} \+ (\\text{Retention} \\times \\text{LocalityTier})

A statistically significant interaction term (p \< 0.01) demonstrates selective locality destruction.

Evaluation risks involve positional encoding distortion, where dropping tokens disrupts 2D rotary positional embeddings (RoPE) and causes output degradation unrelated to information loss. This is controlled by validating uniform bilinear pooling (which maintains a regular 2D grid) alongside token dropping. Image resolution is held strictly static across all tiers. The protocol evaluates 1,500 samples across four retention ratios, requiring approximately 6,000 forward passes and completing in 3.5 hours on Colab Pro.

# **J. Dataset and baseline feasibility**

| Candidate RQ | Official Dataset Source & License | Sample Size Audit | Provenance & Splitting Protocol | Leakage & Shortcut Controls | Minimum Viable Baselines |
| :---- | :---- | :---- | :---- | :---- | :---- |
| RQ 1: Conflict Arbitration | Hugging Face: multimodal-arbitration-artifact; Licenses: GPL-3.0 (ChartQA) & MIT (GSM8K) | 1,000 paired instances (500 chart, 500 arithmetic) | Derived from ChartQA and GSM8K; balanced across chart structures | Group all synthetic variations of an underlying chart into the same split; counterbalance image-correct and text-correct targets | Direct zero-shot generation; Text-only LLM; Image-only VLM |
| RQ 2: Evidence Sufficiency | DocVQA & ChartQA; Licenses: CC BY 4.0 & Apache-2.0 | 500 clean samples with verified bounding boxes | Scanned documents and public charts with annotated text bounding boxes | Mask all redundant instances of the target entity; run blind text-only evaluation to discard language-guessable items | Greedy generation confidence; Max token entropy; Random uninformative patch masking |
| RQ 3: Token Compression | POPE, TextVQA, VSR; Licenses: MIT & CC BY 4.0 | 500 items per tier (1,500 total evaluation instances) | MS-COCO natural images (POPE), open document images (TextVQA), natural spatial relations (VSR) | Keep input image dimensions fixed at 448 \\times 448; verify zero benchmark overlap with pretraining validation sets | Full visual tokens (100%); Uniform spatial bilinear subsampling; Random token dropout |

All three research directions rely on publicly accessible, permissively licensed benchmarks requiring no proprietary API access, private institutional data, or manual raw data collection.

# **K. Leakage and evaluation risks**

### **Leakage and Evaluation Risks for RQ 1 (Conflict Arbitration)**

Prompt framing artifacts present the primary risk in cross-modal conflict experiments. Directly instructing a model to check for contradictions can introduce a conversational bias that leads it to hallucinate disagreement on aligned inputs. To isolate this confound, evaluations must include an equal proportion of aligned control pairs where image and text agree, penalizing false-positive conflict declarations in the final score.

Syntactic and length discrepancies present another confound. If conflicting textual choices are systematically longer, more complex, or formatted differently than gold assertions, the language decoder may select them based on text fluency priors rather than multimodal arbitration. Conflicting text must be generated using identical grammatical templates to gold descriptions, differing solely in the target quantity or entity.

Positional bias in multiple-choice answering also threatens validity. VLMs display pronounced option-order preferences (such as favoring option 'A'). Evaluators must counterbalance option ordering across inference passes and report mean accuracy across permutations.

### **Leakage and Evaluation Risks for RQ 2 (Evidence Sufficiency)**

Incomplete patch masking can distort calibration assessments. High-resolution documents and charts frequently contain redundant information, such as values repeated in headers, legends, or explanatory footnotes. If the primary bounding box is occluded while a secondary reference remains visible, an overconfident prediction reflects valid perceptual grounding rather than uncalibrated hallucination. Evaluators must cross-reference OCR bounding-box annotations to guarantee that every instance of the decisive string is masked.

Probability distribution distortions in open-ended generation also undermine calibration measurements. Assessing confidence across unconstrained vocabulary distributions is noisy because probability mass scatters across synonymous phrases. Masking evaluations should be restricted to short-answer extractions or fixed multiple-choice candidates where log-likelihoods can be evaluated over constrained tokens.

### **Leakage and Evaluation Risks for RQ 3 (Token Compression)**

Positional encoding disruptions represent a significant risk when implementing token pruning. Selectively dropping visual token sequences can distort 2D rotary position embeddings (RoPE) or standard 1D position indices, causing the language model to fail due to coordinate misalignment rather than missing visual information. Experimental scripts must verify positional integrity, testing uniform bilinear pooling (which preserves a regular 2D grid) alongside token dropping.

Dynamic resolution rescaling presents an additional confound. Many modern vision encoders dynamically re-pad or adjust patch counts based on aspect ratio. Image dimensions must remain fixed at static square resolutions across all compression levels to ensure that patch geometry remains identical across experimental conditions.

# **L. Compute feasibility**

The resource requirements for the top three candidate questions are evaluated below against the operational constraints of Google Colab Pro:

Google Colab Pro provides access to NVIDIA T4 (16GB VRAM), V100 (16GB VRAM), or A100 (40GB VRAM) instances with 25GB to 50GB of system RAM and 12 to 24 hours of continuous runtime per session.

The compute audit relies on open-weight models with documented memory footprints:

> 1. SmolVLM-2.2B-Instruct: Consumes \\approx 4.5 GB VRAM in bfloat16; single-image inference consumes \\a\[span\_501\](start\_span)\[span\_501\](end\_span)pprox 1.8 GB VRAM, fitting easily on entry-level GPUs.  
> 2. Qwen2.5-VL-3B-Instruct: Consumes \\approx 7.0 GB VRAM in bfloat16; 4-bit quantized loading (AWQ) consumes \\approx 2.7 to 3.1 GB VRAM. Single forward passes execute in \\approx 120 ms on a T4 GPU.  
> 3. Qwen2.5-VL-7B-Instruct: Requires \\approx 15.5 GB VRAM in bfloat16, which is near the memory ceiling of a 16GB T4, but operates stably on an A100 or in 4-bit AWQ consuming \\approx 6.5 GB VRAM.

| Compute Dimension | Candidate RQ 1 (Conflict Arbitration) | Candidate RQ 2 (Evidence Sufficiency) | Candidate RQ 3 (Token Compression) |
| :---- | :---- | :---- | :---- |
| Evaluation Sample Size (N) | 1,000 paired instances | 500 validated instances | 1,500 instances (3 tiers \\times 500\) |
| Evaluated Conditions | 3 prompts \\times 2 benchmarks \= 6 passes | 5 masking levels \+ 1 control \= 6 passes | 4 retention ratios \\times 3 pruners \= 12 passes |
| Total Forward Passes | 1,000 \\times 6 \= 6,000 | 500 \\times 6 \= 3,000 | 1,500 \\times 4 \= 6,000 |
| Target Base Architecture | Qwen2.5-VL-3B-Instruct (bfloat16) | Qwen2.5-VL-3B-Instruct (bfloat16) | Qwen2.5-VL-3B-Instruct (bfloat16) |
| Mean Forward Pass Latency | \\approx 0.15 seconds | \\approx 0.15 seconds | \\approx 0.12 seconds (pruned visual prefix) |
| Net GPU Compute Time | \\approx 25 minutes | \\approx 12 minutes | \\approx 20 minutes |
| Total Session Runtime (with I/O) | \\approx 1.5 \- 2.5 hours | \\approx 1.0 \- 1.5 hours | \\ap\[span\_468\](start\_span)\[span\_468\](end\_span)prox 2.0 \- 3.5 hours |
| Training / Fine-Tuning Required | None (Zero-shot evaluation) | None (Zero-shot evaluation) | None (Training-free pruning) |
| Colab Pro Hardware Feasibility | 100% executable on single T4/V100 | 100% executable on single T4/V100 | 100% executable on single T4/V100 |

All three experimental designs require under four hours of execution, leaving substantial headroom within standard Colab Pro session limits for multiple random seeds, parameter sweeps, and diagnostic error logging.

# **M. Negative-result value**

A rigorous empirical thesis requires that a negative outcome definitively falsifies a core hypothesis rather than yielding an uninterpretable failure:

For RQ 1 (Conflict Arbitration), if explicit contradiction recognition produces no improvement in arbitration accuracy or Modality Preference Bias, the study establishes a meaningful negative finding: explicit contradiction awareness is causally decoupled from decisional arbitration in vision-language models. This outcome demonstrates that verbalizing a contradiction fails to alter the underlying token-level logit bias, proving that intermediate reasoning tokens act as post-hoc rationalizations rather than computational control mechanisms. This would challenge the common assumption that step-by-step verification prompting improves multi-modal reliability.

For RQ 2 (Evidence Sufficiency), if predictive sequence entropy and confidence scores remain invariant across the 0% to 100% masking ladder, the study establishes that softmax uncertainty in vision-language models is evidence-blind and governed by autoregressive language fluency. Demonstrating that a model displays identical confidence when an image is completely occluded versus fully visible provides empirical evidence that raw confidence scores cannot be used for selective prediction or risk-gated abstention in autonomous pipelines.

For RQ 3 (Token Compression), if accuracy degrades at an identical, uniform rate across macro-scene, medium-object, and micro-OCR tasks, the study refutes the hypothesis of selective locality destruction. This negative outcome demonstrates that visual token representations in modern vision transformers are fully distributed, showing that spatial pruning does not selectively starve small visual details. This would provide empirical justification for applying aggressive token pruning uniformly across fine-grained and global tasks alike.

# **N. Recommended next investigation**

The single most informative next empirical investigation to pursue is:

An empirical study testing whether explicit cross-modal conflict recognition resolves modality dominance or merely rationalizes errors across matched chart and arithmetic contradictions.

This investigation evaluates the intersection of three major findings from 2025–2026: Catapang's identification of persistent Modality Preference Bias, the demonstration by *Which Source Wins?* that modality reliance reverses across tasks, and Kim et al.'s proof that modality dominance manifests prior to decoder fusion.

The investigation provides high disconfirmation value by testing two competing hypotheses: deliberative cognitive control via reasoning scaffolding versus immutable early-layer logit entrenchment. Either outcome yields an actionable contribution to multimodal reliability research.

The project carries minimal feasibility risk: it requires no model fine-tuning, avoids hacking transformer cross-attention matrices, requires no synthetic diffusion generation, and utilizes established, peer-reviewed artifacts (multimodal-arbitration-artifact) on an open model (Qwen2.5-VL-3B-Instruct) within Colab Pro resource limits.

The experimental protocol should proceed through five steps:

> 1. Clone the artifact repository at https://github.com/Ro-netizen004/multimodal-arbitration-artifact to access verified conflict pairs from ChartQA-Conflict and GSM8K-Conflict.  
> 2. Construct a balanced diagnostic split containing 400 chart items and 400 arithmetic items, counterbalancing aligned controls, image-correct/text-false, and text-correct/image-false conditions.  
> 3. Implement the three standardized prompt templates (Direct Answer, Conflict-Aware, and Evidence-Attribution) in Python using Hugging Face Transformers.  
> 4. Run inference on Qwen2.5-VL-3B-Instruct in bfloat16 on Google Colab Pro, logging full generation traces, predicted answers, and output token log-probabilities.  
> 5. Compute Modality Preference Bias (MPB\_{\\text{img}}) and paired arbitration change (\\Delta\_{\\text{arb\[span\_219\](start\_span)\[span\_219\](end\_span)}}). Test whether samples where the model explicitly identifies a conflict exhibit a statistically significant increase (p \< 0.01) in selecting the correct source compared to direct answering.

| Date | Candidate Investigation | Experimental Status | Evidence-Based Rationale | Immediate Action Item |
| :---- | :---- | :---- | :---- | :---- |
| 2026-09-20 | Explicit Conflict Recognition vs. Modality Dominance Arbitration | Recommended for Immediate Investigation | Resolves whether contradiction awareness is causally coupled to arbitration fidelity across task-dependent reliance reversals. Requires zero model training, relies on verified public data, and is executable within Colab Pro limits. | Clone the multimodal-arbitrati\[span\_34\](start\_span)\[span\_34\](end\_span)on-artifact repository, verify split balance across 800 items, and run a zero-shot pilot evaluation on Qwen2.5-VL-3B-Instruct. |

#### **Works cited**

1\. Information Router for Mitigating Modality Dominance in Vision, https://arxiv.org/html/2604.16264v1 2\. Which Source Wins? Task-Dependent Reliance in Vision-Language, https://arxiv.org/pdf/2608.17205 3\. Cross-Modal Evidence Conflict in Multimodal Retrieval-Augmented, https://aclanthology.org/2026.magmar-main.3.pdf 4\. Seulgi Kim, https://skvictoria.github.io/ 5\. Empowering LVLM Reasoning with Multimodal Tree Search, https://www.researchgate.net/publication/394299473\_VisuoThink\_Empowering\_LVLM\_Reasoning\_with\_Multimodal\_Tree\_Search 6\. Token-Region Guided Cross-Attention Fusion for Multimodal Affect, https://arxiv.org/html/2607.23493v1 7\. Boosting Multimodal Reasoning via Information-Gain-Driven ... \- arXiv, https://arxiv.org/html/2603.26348v1 8\. Unifying Drift Adaptation in Non-Stationary Tuning \- arXiv, https://arxiv.org/html/2604.15705v1 9\. Restoring Visual Grounding in Multi-Step Reasoning through Self, https://arxiv.org/abs/2608.04385 10\. A Study of Thinking in Rule-Based Visual Reinforcement Fine-Tuning, https://openreview.net/forum?id=YexxvBGwQM\&noteId=XPYyZGjNJG 11\. Reflect to Inform: Boosting Multimodal Reasoning via ... \- alphaXiv, https://www.alphaxiv.org/abs/2603.26348 12\. Guanyu Wang's research works | Peking University, Beijing (PKU, https://www.researchgate.net/scientific-contributions/Guanyu-Wang-2303887457 13\. Who Speaks for the Pruned? Visual Token Pruning as Coverage, https://papers.cool/arxiv/2609.03158 14\. Asymmetric Text-Visual Pruning for Large Vision-Language Models, https://arxiv.org/html/2603.16001v1 15\. Daily Papers \- Hugging Face, https://huggingface.co/papers?q=VLM%20backbones 16\. Slot2Text: Object-Centric Visual Tokenization for Efficient and ... \- arXiv, https://arxiv.org/html/2608.01473v2 17\. Measuring and Leveraging Modality Gap in Vision-Language Models, https://aclanthology.org/2026.findings-acl.588.pdf 18\. Measuring the Cross-Lingual Comprehension Gap \- arXiv, https://arxiv.org/html/2608.06506v1 19\. SuTRA : Structurally-Unified Tokenization with Root Awareness, https://openreview.net/pdf/e7862aaaf9a3f2c446bd130b25e960bdc37d36c6.pdf 20\. Benchmarking Long-Text Grounding and Cross-Lingual Robustness, https://aclanthology.org/2026.findings-acl.1367.pdf 21\. ReGround: Restoring Visual Grounding in Multi-Step Reasoning, https://arxiv.org/html/2608.04385v1 22\. MoIR: Multi-modal Information Router \- GitHub, https://github.com/olivesgatech/MoIR 23\. Qwen2.5 VL 3B Instruct 3bit by mlx-community \- LLM Explorer, https://llm-explorer.com/model/mlx-community%2FQwen2.5-VL-3B-Instruct-3bit,1Xr3aw8M77t4rkDKmfYbOz 24\. Qwen2.5-VL for Chart and Table Analysis \- Google Colab, https://colab.research.google.com/drive/164RpRhjdAZCwx4fBIMWG3ITrFUxIY2SG?usp=sharing 25\. Vision Encoders in Vision-Language Models: A Survey \- Jina AI, https://jina.ai/vision-encoder-survey.pdf 26\. Qwen/Qwen2.5-VL-3B-Instruct \- Hugging Face, https://huggingface.co/Qwen/Qwen2.5-VL-3B-Instruct 27\. Junjun Hu's research works \- ResearchGate, https://www.researchgate.net/scientific-contributions/Junjun-Hu-2326402685 28\. Aquiles-ai/Qwen2.5-VL-3B-Instruct-Img2Code \- Hugging Face, https://huggingface.co/Aquiles-ai/Qwen2.5-VL-3B-Instruct-Img2Code 29\. wangkanai/qwen2.5-vl-3b-instruct \- Hugging Face, https://huggingface.co/wangkanai/qwen2.5-vl-3b-instruct 30\. Qwen/Qwen2.5-VL-7B-Instruct · Hardware and vram requiremnt to, https://huggingface.co/Qwen/Qwen2.5-VL-7B-Instruct/discussions/18 31\. Memory requirements \- Qwen/Qwen2.5-VL-3B-Instruct \- Hugging Face, https://huggingface.co/Qwen/Qwen2.5-VL-3B-Instruct/discussions/6