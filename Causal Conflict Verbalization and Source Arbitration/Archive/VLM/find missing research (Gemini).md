### **1\. Adversarial Terminology Mapping: Uncovering Hidden Prior Work**

When conducting literature discovery in multimodal and vision-language learning, identical physical and algorithmic phenomena are frequently fragmented across disparate sub-communities using divergent vocabularies. Searching solely for terms such as "cross-modal evidence" or "image-text conflict" misses extensive parallel research in multimodal optimization, mechanistic interpretability, quantization, and autoregressive decoding dynamics.

&nbsp;

&nbsp;

| Target Phenomenon | Primary Terminology | Adjacent / Alternative Formulations in Literature | Missing Methodological Predecessors & Benchmarks | Key Mechanisms & Theoretical Distinctions |
| :---- | :---- | :---- | :---- | :---- |
| Evidence Ignorance & Modality Over-Reliance | Modality Dominance, Modality Reliance&nbsp; | Modality Collapse, Modality Competition, Strong-Modality Collapse, Modality Imbalance, Information Accessibility Gap ($A\_{\\text{access}}$), Shortcut Learning&nbsp; | Javaloy et al. (2022); Wang et al. (2020); Sim et al. (2025 survey); MoIR; Inverted Asymmetric Fusion (IAF); VLM2Rec&nbsp; | Distinguishes *optimization-level gradient competition* during training from *inference-time decodability bottlenecks* ($A\_{\\text{access}}$) where representations retain information but decoder Lipschitz sensitivity ignores non-text directions.&nbsp; |
| Autoregressive Grounding Decay | Visual Grounding Drift, Visual Drift&nbsp; | Visual Anchor Drifting, Visual Forgetting, Perceptual Fading, Attention Decay, Attention Concentration on Visual Sink Tokens, Endogenous Reasoning Drift&nbsp; | ReGround (ACM MM 2026); Visual Re-Examination (VRE); Think-After-Answer / No-Thinking-RFT; Counterfactual Preference Optimization \++ (CPO++); LASER; Add-One-In (AOI)&nbsp; | Proves that extended Chain-of-Thought (CoT) actively hurts pure perception. Attention entropy decays over visual tokens and collapses onto task-irrelevant visual sink tokens, unmooring decoding from physical pixels.&nbsp; |
| Visual-Token Redundancy & Compression | Visual-Token Pruning / Compression&nbsp; | Representational Coverage Maximization (RCM), Visual Over-Representation, Modality-Aware Calibration, Asymmetric Text-Visual Sparsity, Token Merging / Pooling / Dilution, Slot-based Region Tokens&nbsp; | CoverPruner; ATV-Pruning; FastV; VisionZip; DivPrune; CDPruner; Slot2Text; VLMQ; MBQ; MQuant&nbsp; | Uncovers *demand-side representation coverage* and *asymmetric modality sensitivity* (text pathway requires exact calibration, while vision pathway tolerates up to 60% unstructured sparsity). Identifies that token merging dilutes fine-grained localized coordinates.&nbsp; |
| Representation Space Separation | Modality Gap&nbsp; | Modality Dominance Score (MDS), Geometric Separation, Cross-Modal Relational Topology, Modality-Specific Directional Sensitivity&nbsp; | Liang et al. (2022); Beyond Cross-Modal Alignment (Yan et al., 2025/2026); VLM2Rec (2026)&nbsp; | Demonstrates that the modality gap is not merely a geometric separation in CLIP-like embeddings, but causes decoders to respond destructively to non-text directions, causing information loss bounded by the decoder scoring rule.&nbsp; |
| Contradiction & Knowledge Collision | Image-Text Conflict Arbitration&nbsp; | Evidential Conflict Detection, Cross-Modality Knowledge Conflict, Multimodal Polysemantic Collisions, Parametric Memory Override, Insight Over Sight, Modality Preference Bias (MPB)&nbsp; | CMC-Bench (Catapang, 2026); Which Source Wins? (2026); Visual-Counterfact \[cite: 7, source: 2\]; SIGNPOST-Bench; Pezeshkpour et al. (2025); SimpleOCR&nbsp; | Establishes that cross-modal conflict causes a drop of 17% to 46% in accuracy, which is task-dependent (text-leaning in arithmetic, image-leaning in charts). Revealing that failure stems from intermediate arbitration rather than visual perception alone \[cite: 7, source: 2\].&nbsp; |
| Low-Resource / Morphological Disruption | Cross-Lingual Grounding Degradation&nbsp; | Morphological Shattering, Indic Tax / Token Fertility, Subword Segmentation Penalty, Cross-Lingual Gap Persistence, Long-Text Grounding Sensitivity&nbsp; | SuTRA (2026); VLURes (Findings of ACL 2026); BanglaVerse (2026); Multimodal Cross-Attention Fusion (MAF, 2026); IndicCorp&nbsp; | Demonstrates that high subword token fertility shatters morphological roots in Indic scripts. In VLMs, this linguistic fragmentation impairs textual representations, causing an uncalibrated shift in reliance toward visual tokens.&nbsp; |
| Evidence Availability & Sufficiency | Evidence Sufficiency / Selective Abstention&nbsp; | Evidential Deep Learning, Unanswerability Calibration, Mismatched Decoding Gap, Disentangled Abstention vs. Fabrication, Selective Risk&nbsp; | EviVLM (2026); VizWiz-Priv; Catapang (2026); Huang et al. (2025); M-HalDetect&nbsp; | Establishes that conflating abstention with fabrication into an aggregate "hallucination" metric conceals whether models possess calibrated uncertainty or default to fluent linguistic fabrications.&nbsp; |

### **2\. Missing Predecessors, Benchmarks, and Methods Uncovered**

The adversarial literature search across 2024–2026 preprints and conference proceedings exposes several critical works that redefine the state of the art and invalidate naive claims of novelty:

#### **A. Information Accessibility Gap & Mismatched Decoding Bottleneck**

* Predecessors: Liang et al. (2022); Javaloy et al. (2022).

* Recent Discovery: *Information Loss in Multimodal LLMs* (2026).

* Methodological Contribution: Formulates modality collapse as an information accessibility gap:  
  $$A\_{\\text{access}}(T) \= I(Z; S\_T) \- \\text{GMI}\_{P\_M}(S\_T \\mid q)$$  
  It demonstrates that intermediate representations preserve non-text information, but the transformer decoder is sensitive to non-text directions in an unproductive, destructive manner. Removing up to 98% of variation in modality-specific non-text directions actually improves decoder loss.

* Impact on Thesis Formulation: Proves that modality dominance is not merely an encoder-alignment or feature-missing problem, but an inference-time decoder scoring failure.

#### **B. Strong-Modality Collapse & Inverted Asymmetric Fusion**

* Recent Discovery: *Inverted Asymmetric Fusion* (2026); *VLM2Rec* (Kim et al., 2026).

* Methodological Contribution: Identifies "strong-modality collapse"—an architectural failure mode where symmetric cross-attention undermines the model's strongest modality, explaining why multimodal fusion often underperforms unimodal baselines. In parallel, *VLM2Rec* proves that contrastive supervised fine-tuning (SFT) amplifies modality collapse due to gradient imbalance, necessitating Relational Topology Regularization.

* Impact on Thesis Formulation: Proves that forcing mutual cross-attention between modalities can actively harm the dominant modality unless asymmetric anchors or topology regularizers are applied.

#### **C. Endogenous Reasoning Drift, Visual Sink Tokens, and No-Thinking Dynamics**

* Recent Discoveries:  
  1. *Think-After-Answer: When is Thinking Necessary in Multi-Modal Reasoning?* (2025/2026).

  2. *ReGround: Restoring Visual Grounding in Multi-Step Reasoning* (Peng et al., ACM MM 2026).

  3. *LASER / Attention Sink Tokens in LVLM Reasoning* (2026).

  4. *Visual Re-Examination (VRE)* (2026).

  5. *Counterfactual Preference Optimization \++ (CPO++)* (2026).

* Methodological Contribution:  
  * *Think-After-Answer* shows that explicit chain-of-thought (Thinking-RFT) degrades visual perception performance; "No-Thinking" direct answering converges faster and achieves higher accuracy.

  * *ReGround* proves across 2,510 samples that attention entropy over image tokens steadily decreases during reasoning steps, and demonstrates that visual re-examination hurts performance unless paired with targeted self-diagnosis.

  * *LASER* identifies that visual forgetting during long decoding is driven by attention collapsing onto task-irrelevant visual sink tokens.

* Impact on Thesis Formulation: Invalidates the assumption that adding step-by-step reasoning or visual re-examination automatically improves multimodal reliability. It isolates attention decay and sink-token capture as specific failure mechanisms.

#### **D. Representational Coverage Optimization & Asymmetric Calibration**

* Recent Discoveries:  
  1. *CoverPruner: Visual Token Pruning as Coverage Optimization* (Zhu et al., Sept 2026).

  2. *ATV-Pruning: Asymmetric Text-Visual Pruning under High Sparsity* (2026).

  3. *VLMQ: Importance-Aware Calibration for VLM Quantization* (2025/2026).

* Methodological Contribution:  
  * *CoverPruner* shifts pruning from asking "which tokens have high attention scores" to "which surviving tokens represent discarded visual tokens," framing compression as Representational Coverage Maximization (RCM).

  * *ATV-Pruning* discovers an extreme structural asymmetry: textual pathways require exact calibration, whereas visual pathways tolerate up to 60% unstructured sparsity with minimal macro-benchmark loss.

  * *VLMQ* shows that raw gradients for redundant visual tokens are dramatically smaller than text tokens, identifying a structural "visual over-representation" problem.

* Impact on Thesis Formulation: Standard token pruning based on attention magnitude is obsolete. The unresolved research frontier is whether coverage-based compression selectively eliminates sparse, localized factual evidence (OCR, coordinates) while maintaining macro-benchmark scores.

#### **E. Morphological Shattering as an Unintended Visual Reliance Inducer**

* Recent Discoveries:  
  1. *SuTRA: Structurally-Unified Tokenization with Root Awareness* (2026).

  2. *VLURes: Long-Text Multimodal Grounding across Languages* (Findings of ACL 2026).

* Methodological Contribution: *SuTRA* formalizes "morphological shattering" in Indic scripts, where subword tokenizers split multimorphemic words into non-semantic fragments, inflating token fertility (Indic Tax). *VLURes* demonstrates that cross-lingual gaps in VLMs persist even when the underlying LLM is multilingual, specifically degrading long-text grounding.

* Impact on Thesis Formulation: Provides a mechanistic basis for low-resource multimodal failure: high token fertility creates representation uncertainty in the text sequence, which forces the model's cross-attention layers to alter their reliance on visual evidence.

### **3\. Revised Research-Question Tree**

Integrating adjacent terminology, newly uncovered failure modes, and recent theoretical frameworks results in a revised Research-Question Tree organized into ten major research families:

* Multimodal / Vision-Language Learning and Systems  
  * &nbsp;  
    1. Cross-Modal Conflict Arbitration & Mismatched Decoding  
    * Phenomenon: Asymmetric channel reliance and arbitration failure under cross-modal contradiction.

    * Failure Mode: Modality Dominance / Strong-Modality Collapse, where the model follows a single modality regardless of relative channel corruption or evidential clarity.

    * Mechanism / Hypothesis:  
      * H1 (Information Accessibility Bottleneck): The LLM decoder possesses an asymmetric Lipschitz sensitivity that misinterprets non-text embedding directions as noise, defaulting to textual priors.

      * H2 (Pre-Fusion Information Disparity): Unimodal encoders produce imbalanced information density prior to fusion, which attention alone cannot rebalance.

    * Controlled Intervention: Counterbalanced factual/numeric contradictions across task structures (arithmetic vs. charts), paired with explicit disagreement classification and SVD information routing.

    * Measurable Outcome: Modality Preference Bias (MPB), Arbitration Accuracy ($Acc\_{\\text{arb}}$), Information Accessibility Gap ($A\_{\\text{access}}$).

    * Revised RQ: When visual and textual evidence conflict, does explicit disagreement recognition improve decisional arbitration accuracy, or does the decoder's directional sensitivity maintain a fixed modality preference?

  * &nbsp;  
    2. Evidence Sufficiency, Evidential Uncertainty & Abstention Disentanglement  
    * Phenomenon: Uncalibrated confidence and refusal failure on unanswerable or partially occluded visual queries.

    * Failure Mode: Overconfident Fabrication / False Grounding, where the model generates fluent, authoritative answers when decisive visual patches are missing or unresolvable.

    * Mechanism / Hypothesis:  
      * H1 (Fluency-Entropy Decoupling): Output softmax entropy reflects autoregressive language sequence likelihood rather than cross-modal evidence sufficiency.

      * H2 (Evidential Boundary Confusion): Models fail to distinguish "evidence supports false" from "insufficient evidence exists to verify" \[cite: 3, source: 1\].  
    * Controlled Intervention: Bounding-box parametric evidence-masking ladders (0% to 100% of decisive region) evaluated across answerable, unanswerable, and contradictory framing.

    * Measurable Outcome: Expected Calibration Error (ECE), Brier score, Selective Risk at coverage $\\alpha$ ($R(\\alpha)$), Disentangled Fabrication vs. Abstention Rate.

    * Revised RQ: Does continuous parametric masking of decisive visual evidence produce a monotonic increase in predictive sequence entropy, or does linguistic fluency maintain an overconfident prediction until catastrophic collapse \[cite: 3, source: 1\]?  
  * &nbsp;  
    3. Reasoning Drift, Attention Decay & Visual Sink Collapses  
    * Phenomenon: Perceptual ungrounding during extended autoregressive Chain-of-Thought (CoT) generation.

    * Failure Mode: Endogenous Reasoning Drift / Visual Forgetting, where intermediate reasoning steps drift away from visual premises and anchor exclusively to generated text tokens.  
    * Mechanism / Hypothesis:  
      * H1 (Visual Sink Capture): Visual attention entropy decays as probability mass concentrates on uninformative visual sink tokens across extended decoding steps.  
      * H2 (Perceptual Interference in Thinking): Explicit reasoning traces generate intermediate hypotheses that introduce misleading visual hallucinations, whereas direct answering preserves raw perceptual representations.  
    * Controlled Intervention: Direct answering (No-Thinking) vs. Standard CoT (Thinking-RFT) vs. Scheduled Look-Back / Visual Token Copy interventions.  
    * Measurable Outcome: Image Token Attention Entropy, Sink Token Attention Ratio, Step-level Hallucination Rate, Downstream Reasoning Accuracy.  
    * Revised RQ: In multi-step visual reasoning, does prompt-scheduled visual re-examination restore decaying image-token attention entropy, or does intermediate verbalization exacerbate visual sink-token capture?  
  * &nbsp;  
    4. Representational Coverage & Locality-Dependent Evidence Pruning  
    * Phenomenon: Selective factual reasoning collapse under visual-token compression and quantization.  
    * Failure Mode: Localized Evidence Dilution / Silent Spatial Failure, where aggregate benchmark scores are preserved while small-object, coordinate, and text-reading reasoning fails catastrophically.  
    * Mechanism / Hypothesis:  
      * H1 (Representational Coverage Failure): Magnitude and attention-norm pruning select redundant high-variance global tokens, leaving isolated, query-critical visual evidence unrepresented.  
      * H2 (Asymmetric Sparsity Tolerance): Text-side reasoning pathways require dense preservation, whereas visual pathways tolerate up to 60% sparsity only on global semantic tasks, collapsing on localized geometric evidence.  
    * Controlled Intervention: Stratified token retention ladders (10% to 100%) comparing Attention-Norm Pruning (FastV), Coverage Maximization (CoverPruner), and Uniform Bilinear Subsampling across task locality tiers \[cite: 24, source: 1\].  
    * Measurable Outcome: Accuracy Retention Ratio ($ARR\_{k,r}$), Locality-by-Retention Interaction $F$-statistic, POPE Hallucination Score.  
    * Revised RQ: Does visual-token compression exhibit a significant statistical interaction with evidence spatial footprint, disproportionately eliminating localized OCR and coordinate tokens while preserving global scene comprehension?  
  * &nbsp;  
    5. Morphological Shattering & Cross-Lingual Modality Reliance  
    * Phenomenon: Asymmetric cross-modal dependency shifts when queries are presented in morphologically complex, fragmented scripts.  
    * Failure Mode: Tokenizer-Induced Modality Shift, where subword token fragmentation impairs textual representation coherence, forcing reliance onto the visual channel.  
    * Mechanism / Hypothesis:  
      * H1 (Morphological Uncertainty Compensation): High token fertility (Indic Tax) and non-semantic subword splits create diffuse textual representations, causing multi-head attention to place higher relative weight on visual tokens.  
      * H2 (Linguistic Representation Breakdown): Subword fragmentation degrades syntactic parsing, producing comprehension failure without altering visual cross-attention weights.  
    * Controlled Intervention: Parallel English vs. Native Indic (Bengali) vs. Root-Preserved (SuTRA-style) queries over identical visual stimuli with controlled token fertility ratios \[cite: 114, source: 1\].  
    * Measurable Outcome: Modality Reliance Metric ($\\Delta\_{\\text{vis}}$), Token Fertility Ratio, Cross-Lingual Grounding Gap, Output Consistency.  
    * Revised RQ: Holding visual stimuli and semantic meaning constant, does higher tokenizer morphological shattering in Bengali queries causally increase reliance on visual tokens compared to English queries \[cite: 114, source: 1\]?  
  * &nbsp;  
    6. Causal Faithfulness vs. Post-Hoc Saliency Attribution  
    * Phenomenon: Divergence between post-hoc feature attribution maps and actual counterfactual model reliance \[cite: 20, source: 1\].  
    * Failure Mode: Spurious Saliency Rationalization, where gradient and attention heatmaps highlight image regions whose removal does not alter output logits \[cite: 20, source: 1\].  
    * Mechanism / Hypothesis:  
      * H1 (Attention-Causality Decoupling): Softmax attention maps reflect routing connectivity rather than counterfactual necessity, behaving as post-hoc rationalizations \[cite: 20, source: 1\].  
      * H2 (Modality Dominance Geometric Gap): Representations lie on disjoint manifolds where small gradient projections reflect geometric separation rather than predictive reliance.  
    * Controlled Intervention: Saliency-guided patch deletion vs. Counterfactual Shapley patch ablation (CMA) across balanced multimodal reasoning benchmarks \[cite: 20, source: 1\].  
    * Measurable Outcome: Deletion-curve Area Under the Curve (AUC), Faithfulness Correlation ($R\_{\\text{faith}}$), Modality Dominance Score (MDS).  
    * Revised RQ: How closely do gradient-based visual saliency attributions correlate with causal counterfactual patch removal across balanced multimodal reasoning tasks \[cite: 20, source: 1\]?  
  * &nbsp;  
    7. Graceful Degradation & Missing-Modality Dynamics  
    * Phenomenon: Catastrophic prediction collapse when an expected input modality is omitted or corrupted at inference time.  
    * Failure Mode: Unimodal Fallback Failure / Modality Hallucination, where an empty or zeroed visual input triggers unconstrained visual hallucinations rather than graceful fallback to text-only reasoning.  
    * Mechanism / Hypothesis:  
      * H1 (Missing Modality Distributional Shock): Zero or Gaussian replacement vectors fall outside the learned cross-modal manifold, destabilizing transformer layer normalization.  
      * H2 (Prompt-Signaled Graceful Routing): Providing explicit missingness semantic tokens allows the model to bypass cross-attention layers and execute calibrated text reasoning.  
    * Controlled Intervention: Systematic modality dropout (blank images, Gaussian noise, explicit missing-modality tokens) across joint vision-text tasks.  
    * Measurable Outcome: Graceful Degradation Slope, Output Perplexity, Hallucination Proliferation Rate.  
    * Revised RQ: When visual inputs are entirely missing, does explicit missing-modality token signaling enable calibrated textual fallback, or do models default to hallucinatory visual grounding \[cite: 4, source: 1\]?  
  * &nbsp;  
    8. Counterfactual Visual Invariance & Parametric Prior Override  
    * Phenomenon: Model failure to update inferential conclusions under controlled counterfactual visual edits.  
    * Failure Mode: Parametric Knowledge Dominance, where memorized real-world associations override visible counterfactual evidence \[cite: 4, 7, source: 2\].  
    * Mechanism / Hypothesis:  
      * H1 (Frequency-Driven Parametric Capture): Pretrained language priors dominate counterfactual visual features in proportion to the real-world co-occurrence frequency of the queried entity.  
      * H2 (Visual Patch Salience Threshold): Parametric memory is overridden only when counterfactual visual edit area exceeds a critical threshold of total image tokens.  
    * Controlled Intervention: Minimal counterfactual image edits (inpainting color, count, or spatial relations) paired with invariant queries across high-frequency vs. low-frequency entities \[cite: 4, source: 1\].  
    * Measurable Outcome: Counterfactual Update Rate ($Acc\_{\\text{cf}}$), Parametric Retention Rate, Semantic Invariance Score.  
    * Revised RQ: Does parametric memory override of counterfactual visual evidence scale as a function of pretraining co-occurrence frequency, or is it governed strictly by the spatial salience of the visual edit \[cite: 4, 24, source: 1\]?  
  * &nbsp;  
    9. Claim-Level Decomposed Verification vs. Indiscriminate Retraction  
    * Phenomenon: Disconnect between fluent multi-claim generation and localized visual factual grounding.  
    * Failure Mode: Fluent Partial Hallucination, where models generate factually accurate descriptions containing isolated, ungrounded visual claims.  
    * Mechanism / Hypothesis:  
      * H1 (Decoupled Verification Utility): Isolating claims into atomic subject-predicate-object triples allows cross-attention to focus on localized bounding boxes without narrative interference.  
      * H2 (Over-Correction Penalization): Prompting for self-verification induces conservative linguistic hedging, causing false-positive retractions of valid visual claims.  
    * Controlled Intervention: Monolithic generation vs. Claim decomposition \+ localized box verification vs. Text-only self-correction.  
    * Measurable Outcome: Atomic Claim Precision, Unnecessary Retraction Rate (Harm Rate), Net Factual Accuracy.  
    * Revised RQ: Does atomic claim decomposition and visual re-verification increase factual precision without increasing the false-positive retraction rate of valid visual observations?  
  * &nbsp;  
    10. Benchmark Shortcut Pathways & Unimodal Leakage Auditing  
    * Phenomenon: Benchmark score inflation driven by language-only mutual information and superficial dataset heuristics.  
    * Failure Mode: Spurious Multimodal Alignment, where state-of-the-art VLMs achieve high benchmark accuracy under complete visual ablation.  
    * Mechanism / Hypothesis:  
      * H1 (Linguistic Mutual Information Shortcut): Questions contain phrasing, syntactic markers, or option formatting that correlate with answers independently of image content.  
      * H2 (Benchmark Contamination): High-capacity foundation models memorized question-answer pairs during web-scale text pretraining.  
    * Controlled Intervention: Blind text-only evaluation, blank-image evaluation, option-order permutation, and grouped-split audits across standard benchmarks.  
    * Measurable Outcome: Unimodal Shortcut Delta ($\\text{Score}\_{\\text{multimodal}} \- \\text{Score}\_{\\text{blind}}$), Option Permutation Invariance, Benchmark Contamination Ratio.  
    * Revised RQ: What proportion of reported multimodal reasoning capability on domain benchmarks is driven by unimodal linguistic priors and option formatting shortcuts rather than cross-modal fusion?

### **4\. Methodological Audit & Threat Analysis**

Integrating the newly discovered literature refines the experimental requirements and identifies specific failure points for an undergraduate thesis:

#### **Threat 1: Conflating Inference-Time Decoder Bias with Architectural Fusion**

* Literature Insight: As established by *Information Loss in Multimodal LLMs* (2026), an information accessibility gap ($A\_{\\text{access}}$) can occur purely in the LLM decoder's scoring rule, even when the encoder and projector preserve visual features.  
* Threat: An undergraduate researcher might conclude that a model's failure to answer from an image means the visual projector or encoder failed.  
* Control: The experimental protocol must incorporate logit-level probes or gradient isotropy checks on intermediate cross-modal hidden states. If intermediate states contain the visual information while output tokens fail to express it, the failure is verified as a decoder decodability bottleneck rather than perceptual feature loss.

#### **Threat 2: The CoT Degradation Hazard ("Overthinking" Perception)**

* Literature Insight: *Think-After-Answer* (2025/2026) demonstrated that multi-step reasoning (Thinking-RFT) can actually harm visual perception tasks compared to direct answering (No-Thinking). Concurrently, *ReGround* (2026) showed that visual re-examination without targeted self-diagnosis harms accuracy.  
* Threat: Assuming that prompting a VLM with chain-of-thought or "examine the image step-by-step" will improve conflict arbitration or evidence use.  
* Control: Every multi-step reasoning intervention must include a direct-answering baseline and an explicit "Think-After-Answer" control. Experiments must verify whether intermediate tokens improve perceptual accuracy or merely generate unfaithful post-hoc rationalizations.

#### **Threat 3: Visual Sink Tokens Distorting Attention Audits**

* Literature Insight: *LASER* (2026) showed that attention decay over visual tokens during long decoding collapses onto task-irrelevant visual sink tokens.  
* Threat: Measuring raw attention weights on image tokens across decoding steps can produce false positives if attention is captured by sink tokens rather than informative pixels.  
* Control: When tracking visual attention entropy or grounding drift across reasoning chains, researchers must mask or factor out visual sink tokens (identified via high attention mass across all prompts) before computing semantic visual grounding metrics.

#### **Threat 4: Positional Embedding Distortion in Token Pruning**

* Literature Insight: When visual tokens are dropped, 2D rotary positional embeddings (RoPE) can undergo distributional shifts, degrading performance due to coordinate distortion rather than evidence removal.  
* Threat: Attributing accuracy drops under token compression to "evidence destruction" when the model simply suffered from corrupted position indices.  
* Control: Token pruning evaluations must test both unstructured token dropping and regular 2D spatial pooling (e.g., DeCo or bilinear pooling), which preserves grid geometry, ensuring that coordinate degradation does not act as an unmeasured confound.

#### **Threat 5: Translation & Dialect Artifacts in Cross-Lingual Audits**

* Literature Insight: *SuTRA* (2026) demonstrated that standard subword tokenizers induce severe morphological shattering in Indic scripts.  
* Threat: Translating English VQA benchmarks into Bengali via commercial APIs can introduce unnatural phrasing, loanwords, or syntax that conflate translation artifacts with cross-modal grounding mechanisms.  
* Control: Bengali evaluation sets must undergo native-speaker review to enforce natural morphological phrasing, and token fertility ratios (subwords per word) must be explicitly calculated and included as a covariate in statistical analyses.

### **5\. Surviving Top 3 Research Questions: Deep Re-Assessment**

Following this adversarial terminology audit, the top three candidate research questions are refined to ensure they test distinct mechanisms that survive recent literature scrutiny:

#### **Candidate 1: Disagreement Recognition vs. Decoder Accessibility in Cross-Modal Conflict Arbitration**

* Refined Formulation: When visual and textual evidence provide contradictory facts, does prompting for explicit contradiction detection overcome the decoder's directional sensitivity ($A\_{\\text{access}}$), or does the model remain bound to its task-dependent Modality Preference Bias (MPB)?  
* Core Mechanism: Tests whether verbalizing a contradiction enables the decoder to re-weight non-text embedding directions, or whether early-layer projection dynamics and parametric priors fix the output logit regardless of intermediate reasoning tokens.  
* Primary Metric: Paired Arbitration Gain ($\\Delta\_{\\text{arb}}$) and Modality Preference Bias shift ($\\Delta\_{\\text{MPB}}$) across matched arithmetic and chart contradictions from multimodal-arbitration-artifact.  
* Compute on Colab Pro: Requires approximately 6,000 forward passes on Qwen2.5-VL-3B-Instruct, executing in under 2.5 hours with zero training.

#### **Candidate 2: Continuous Evidence-Sufficiency Calibration Under Parametric Bounding-Box Ablation**

* Refined Formulation: When decisive visual evidence is parametrically ablated in continuous spatial increments (0% to 100%), does predictive sequence entropy calibrate proportionally to lost evidential support, or does linguistic fluency maintain an overconfident prediction until catastrophic collapse \[cite: 3, source: 1\]?  
* Core Mechanism: Distinguishes information-theoretic calibration (entropy scales monotonically with evidence loss) from linguistic autoregressive inertia (fluency dominates confidence until complete perceptual void).  
* Primary Metric: Normalized Sequence Entropy slope ($\\beta\_{\\text{mask}}$), Expected Calibration Error (ECE), and Disentangled Fabrication vs. Abstention Rate.  
* Compute on Colab Pro: Requires 3,000 forward passes on DocVQA and ChartQA splits, executing in under 1.5 hours.

#### **Candidate 3: Representational Coverage vs. Locality-Dependent Evidence Destruction in Visual-Token Pruning**

* Refined Formulation: Does visual-token compression exhibit a statistically significant interaction effect with evidence spatial footprint, disproportionately degrading localized OCR and coordinate tokens while preserving macro-scene classification under Representational Coverage Maximization?  
* Core Mechanism: Compares the Representational Coverage hypothesis (coverage-based pruning preserves localized evidence) against the Selective Locality Destruction hypothesis (attention-based pruning favors global scene tokens at the expense of sparse localized coordinates).  
* Primary Metric: Locality-by-Retention Interaction $F$-statistic from two-way ANOVA across stratified task tiers (MMBench vs. POPE vs. TextVQA/VSR) \[cite: 16, source: 1\].  
* Compute on Colab Pro: Requires 6,000 forward passes across four retention ratios (100%, 75%, 50%, 25%) using training-free pruning hooks, executing in under 3.5 hours.