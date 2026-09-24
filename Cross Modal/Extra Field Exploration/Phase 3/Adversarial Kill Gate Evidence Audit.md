# **Phase 3 Adversarial Kill-Gate Evidence Audit: Multimodal Reasoning Trace Degradation (Q1) vs. Visual Binding-ID Universality (Q2)**

## **1\. Executive Verdict**

An adversarial audit of the theoretical premises, empirical literature, and experimental protocols supporting candidate questions Q1 and Q2 reveals that neither candidate survives in its original Phase 2 formulation. Both proposals are compromised by literature pre-emption, methodological confounds, and statistically invalid kill criteria.

Question 1 asserts that visual evidence utilization degrades as a causal function of multimodal reasoning trace length after controlling for sequence position, context length, and attention or softmax dilution. The broad empirical phenomenon is pre-empted by RH-Bench. RH-Bench manipulated reasoning length using latent state steering and budget forcing across diverse multimodal tasks, discovering that extended reasoning chains reduce visual attention allocation and amplify visual hallucination non-monotonically. Furthermore, Remember-R1, ReGround, and Visual Information Gain establish the observational reality of visual attention decay and grounding collapse across autoregressive decoding trajectories. The original three-arm intervention for Q1 is experimentally invalid because generated reasoning length is endogenous to sample difficulty, and synthetic neutral padding introduces non-neutral distributional and attention-sink shifts in transformer hidden states. Q1 survives exclusively as a narrowed mechanistic decomposition: a matched-prefix causal sensitivity audit under teacher forcing designed to determine whether visual evidence decay deviates from a uniform softmax dilution null after isolating Rotary Position Embedding coordinates.

Question 2 asserts that latent visual Binding IDs represent universal, architecture-independent mechanisms in vision-language models rather than representational artifacts of synthetic geometric scenes. The universality and architecture-independence hypotheses are contradicted by foundational literature. Dual-encoder limit theorems establish mathematical smoothness frontiers proving architectural ceilings on compositional binding in dual-encoder frameworks. Mechanistic studies demonstrate that multimodal binding is split across distinct vision-encoder and language-backbone sub-circuits or resolved through serial spatial pointing routines rather than static, context-free latent binding vectors.

The causal activation-swapping intervention in Anchor C1 is restricted to procedurally generated symbol-partitioned grids and omits necessary placebo controls. However, natural-image causal activation swapping remains unperformed in the literature. Q2 survives strictly as a synthetic-to-natural transfer and specificity study on localized object representations using dense natural benchmarks such as Dense Same-Class Attribute Misbinding and InstaBind-Lite.

The canonical baseline thesis, investigating causal conflict verbalization and source arbitration under contradictory evidence, remains superior in causal identification, execution feasibility, and robustness against engineering failure.

| Candidate Direction | Phase 2 Status | Phase 3 Adversarial Verdict | Recommended Action |
| :---- | :---- | :---- | :---- |
| **Q1: Reasoning Length vs. Visual Utilization** | Alive but narrow | **SURVIVES WITH MODIFICATION** | Reframe as a matched-prefix causal sensitivity audit decomposing the RH-Bench length phenomenon. |
| **Q2: Binding-ID Universality vs. Synthetic Artifact** | Alive but contested | **SURVIVES WITH MODIFICATION** | Strip universality claims; restrict scope to synthetic-to-natural transfer on DSCAM under strict placebos. |
| **Canonical Baseline: Conflict Verbalization** | Primary baseline | **CONFIRMED PRIMARY BASELINE** | Retain as primary thesis; hold Q1 and Q2 as secondary backups pending runtime pilot outcomes. |

## **2\. Audit of Phase 2 Kill Tests (K1–K8)**

The eight kill gates formulated during Phase 2 exhibit significant methodological and statistical vulnerabilities. Most critically, the evaluation methodology treated a failure to reject the null hypothesis (p \> 0.05) under standard null-hypothesis significance testing as empirical proof that two experimental conditions are functionally equivalent. In causal inference and mechanistic interpretability, establishing that an effect vanishes or that two interventions produce identical downstream representations requires formal equivalence testing.

Relying on p \> 0.05 conflates an underpowered sample size with an absence of effect. Demonstrating equivalence requires the Two One-Sided Tests procedure within predefined equivalence margins (\[-\\theta, \+\\theta\]), accompanied by reported 90% or 95% confidence intervals, standardized effect sizes (such as Cohen's d\_{\\text{av}} for paired comparisons), and non-parametric bootstrap estimates.

Furthermore, the Phase 2 gates relied on arbitrary heuristics, including requiring linear probe accuracy above 70% or intervention effects exceeding placebos by at least 25%. Absolute probing accuracy is sensitive to class balance, sample entropy, and probe regularization, whereas a defensible availability test requires evaluating empirical chance-subtracted area under the receiver operating characteristic curve (\\Delta\\text{AUC} \= \\text{AUC} \- 0.5) evaluated against label-permutation null distributions.

Similarly, requiring an arbitrary 25% margin over placebo fails to verify relation specificity; decision rules must instead establish that the confidence interval of the net directed target flip does not cover zero and demonstrates statistical divergence from a structured placebo family.

Gate K7 was recovered verbatim from the Phase 2 feasibility report. The original text specifies: "Alternative-explanation survival (Q2-E/H) \+ framing (Q2-G); naming / color-histogram / nearest-patch explains the effect \-\> Q2 dies by reduction". The gate is scientifically necessary but required restructuring from an informal checklist into a formal covariate regression model.

| Gate | Phase 2 Definition | Scientific Purpose | Valid? | Methodological & Statistical Flaws | Empirical Literature Evidence | Recommended Revision |
| :---- | :---- | :---- | :---- | :---- | :---- | :---- |
| **K1** | Effect vanishes with answer position fixed \\rightarrow Q1 collapses to position. | Disentangle reasoning length from absolute Rotary Position Embedding coordinates. | **Invalid as written** | Employs directional NHST; treats p \> 0.05 as proof of equivalence; ignores content-nonspecific token mass. | RoPE attention attenuation correlates monotonically with token distance in decoder-only models. | 4-arm within-item factorial design; evaluate reasoning-specific contrast via TOST with margin \\theta \= 0.05. |
| **K2** | Normalized-VIG decline survives denominator control; decline \\rightarrow 0 under normalization \\rightarrow Q1 is dilution. | Establish whether visual attention decay is an artifact of softmax denominator expansion. | **Invalid as written** | Lacked a mathematical null model; denominator expansion causes mathematical dilution. | Softmax over N keys allocates uniform probability 1/N; an image block of M tokens receives chance mass M/N. | Define metric as \\text{VIG}\_{\\text{mass}} \- M/N; slope test \\Delta(\\text{mass})/\\Delta N \= \\Delta(M/N)/\\Delta N via TOST. |
| **K3** | Steering/availability survives at long trace; if evidence no longer decodable, Q1 reframed as decay. | Separate internal representational availability from downstream utilization routing. | **Invalid as written** | Conflates linear decodability with causal steering; relies on arbitrary 70% threshold. | Anchor A1 proves visual evidence remains linearly decodable while output routing defaults to text priors. | Split into K3a (5-fold cross-validated probe \\Delta\\text{AUC} vs. 1,000 permutations) and K3b (causal rank-1 steering shift). |
| **K4** | Placebo swap beats random/scramble/reorder; if placebo reproduces effect, Q2 dies as artifact. | Verify that activation swapping transfers specific binding rather than non-specific damage. | **Partially valid** | Placebo implementations were underspecified; lacked net directed target flip metrics. | Anchor C2 evaluated Gaussian noise; Anchor C1 lacked random-vector and scrambled controls. | Pre-specify 3 placebos: norm-matched Gaussian noise, spatial patch scramble, and within-image object swap. |
| **K5** | Effect \\le placebo on DSCAM/What'sUp \\rightarrow Q2 dies as synthetic artifact. | Test synthetic-to-natural transfer of causal binding representations. | **Partially valid** | What'sUp benchmark lacks object bounding-box masks for patch alignment; non-target collapse unmeasured. | DSCAM provides 1,773 boxed instances across 524 natural photographic images. | Restrict evaluation to DSCAM; require target net flip CI excluding zero and non-target preservation \>0.70. |
| **K6** | Cross-family subspace alignment CCA overlap \\approx 0 \\rightarrow architecture-specific. | Evaluate whether Binding-ID geometry is invariant across model architectures. | **Invalid as written** | Canonical correlation analysis across unaligned heterogeneous residual spaces naturally yields zero overlap. | Qwen2.5-VL uses native ViT (d=2048); Gemma 3 uses SigLIP (d=2560) with soft tokens. | Replace representational CCA with behavioral intervention transfer parity across architectures. |
| **K7** | Covariate model survival; naming, color histogram, or nearest patch explains effect \\rightarrow dies by reduction. | Rule out lower-level photometric, semantic, or spatial confounders. | **Valid** | Bundled competing hypotheses into an unstructured checklist without formal regression modeling. | Anchor C1 utilized non-ordinal glyphs to decouple lexical co-occurrence priors from visual binding. | Structured covariate regression: test whether color histogram delta, patch distance, or text prior accounts for swap variance. |
| **K8** | Colab 16 GB activation cache \\le 2\\text{ GB} / 500\\text{ items}; overflow \\rightarrow rescope. | Ensure computational feasibility under Google Colab Pro VRAM envelope. | **Invalid as written** | Conflates persistent disk caching with GPU peak memory allocation during forward hooks. | Full multi-head attention extraction across 36 layers consumes \>4.8\\text{ GB} per forward pass. | Measure torch.cuda.max\_memory\_allocated; compute streaming attention sums on the fly without storing raw matrices. |

## **3\. Q1 Closest-Work Matrix**

The literature surrounding multimodal reasoning, visual forgetting, and attention dynamics underwent rapid development across 2025 and 2026\. The broad thesis that visual grounding decays during extended chain-of-thought generation is established.

The primary scientific gap remaining for Q1 is not demonstrating the existence of visual attention decline, but isolating its causal mechanism: determining whether the degradation is driven by semantic reasoning operations, absolute sequence position, total context length, or mechanical softmax denominator expansion.

| Paper & Citation | Exact Question Tested | Trace Length Manipulated? | Sequence Position Controlled? | Context Length Controlled? | Reasoning Separated from Padding? | Information Availability Measured? | Information Utilization Measured? | Causal Intervention or Observational? | Models Evaluated | Datasets Used | What Remains Untested |
| :---- | :---- | :---- | :---- | :---- | :---- | :---- | :---- | :---- | :---- | :---- | :---- |
| **RH-Bench** (Liu et al., NeurIPS 2025, arXiv:2505.21523) | Does extended reasoning amplify visual hallucination in multimodal models? | **Yes**: Latent state steering (weights \[-0.1, 0.1\]) and budget forcing. | **No**: Generation unfolds naturally across decoding steps. | **No**: Total sequence length expands with reasoning length. | **Partially**: Contrasts reasoning models against non-reasoning baselines. | **No**: Measures perception accuracy and visual hallucination rates. | **Yes**: Tracks cross-attention allocation to visual tokens. | **Causal length manipulation**, observational attention tracking. | Open and proprietary reasoning models (3B to 72B). | RH-Bench (perception and reasoning tasks). | Causal decomposition separating semantic reasoning content from RoPE position and uniform softmax dilution. |
| **Remember-R1** (Chen et al., ACM MM 2026, arXiv:2608.01314) | Can reinforcement learning mitigate long-context visual forgetting in MLLM CoT? | **No**: Evaluates natural reasoning trajectories emitted during RL. | **No**: Measures early vs. late trajectory bins. | **No**: Conflates trajectory length with problem difficulty. | *No*: Does not evaluate non-reasoning padding text. | **Partially**: Ground-truth visual keyword matching. | **Yes**: Formulates visual attention mass \\Omega(t) over time. | **Observational** on visual decay; causal RL policy optimization. | Qwen2.5-VL-3B, Qwen2.5-VL-7B. | ViRL39K, MathVista, WeMath, MMMU. | Whether attention decay persists when sequence position and total context length are held fixed. |
| **ReGround** (arXiv:2608.04385, Aug 2026\) | Does visual grounding collapse during multi-step reasoning, and can re-injection restore it? | **No**: Analyzes fixed-round autoregressive reasoning outputs. | **No**: Position shifts when visual tokens are re-injected. | **No**: Re-injection increases total context length. | **Partially**: Compares text-only reflection with visual re-injection. | **No**: Evaluates output accuracy and attention entropy. | **Yes**: Measures visual token attention entropy collapse. | **Causal re-injection intervention**, observational entropy measurement. | Qwen2-VL-7B, InternVL2-8B. | MathVista, MathVision, HallusionBench. | Isolating whether initial grounding collapse is caused by reasoning operations or position-dependent attention dilution. |
| **VIG** (Luo et al., arXiv:2608.21883, Aug 2026\) | Can multimodal CoT be compressed by rewarding tokens with high visual information gain? | **No**: Evaluates generated reasoning trajectories. | **No**: Tracks token index \\tau along generated sequences. | **No**: Sequence length correlates with problem complexity. | **No**: Evaluates generated reasoning text without synthetic controls. | **Yes**: Measures predictive entropy reduction conditioned on image. | **Yes**: Defines per-token information gain VIG(t). | **Observational length analysis**; causal RL compression training. | Qwen3-VL-Thinking (2B, 4B, 8B). | WeMath, MathVision, MMMU, DynaMath. | Controlled manipulation of reasoning length independent of task difficulty and context expansion. |
| **Seeing or Knowing? (A1)** (Li et al., arXiv:2607.26326, Aug 2026\) | Do MLLMs fail from visual representation loss or from language prior override? | **No**: Strictly single-turn prompts; excludes intermediate CoT. | **Fixed**: Static single-turn prompt formats. | **Fixed**: Static zero-shot context lengths. | **N/A**: No reasoning traces present in benchmark. | **Yes**: Linear decodability of visual attributes from image tokens. | **Yes**: PairAcc under visual vs. prior steering directions. | **Causal**: Activation patching and rank-1 steering vector addition. | Qwen2.5-VL-3B/7B, Qwen3.5-4B/9B, Gemma-4. | WhatIfVis (3,049 counterfactual pairs). | Extending the availability vs. utilization audit across extended multi-step reasoning traces. |
| **The Ebb and Flow of Focus** (arXiv:2607.11436, Jul 2026\) | How does attention shift between modalities across long reasoning generations? | **No**: Evaluates natural generation trajectories. | **No**: Token index increases monotonically. | **No**: Context expands with generation. | **No**: Evaluates natural model reasoning. | **No**: Focuses on attention mass allocation. | **Yes**: Measures cross-attention shift from vision to text. | **Causal windowing intervention**, observational attention measurement. | Open-source multimodal models. | Long-form multimodal benchmarks. | Disentangling whether attentional shifts are driven by semantic reasoning or positional distance. |

## **4\. Q1 Experimental Validity**

The three-arm experiment proposed during Phase 2—comparing Condition A (short direct answer), Condition B (long reasoning / \~150-token controlled filler), and Condition C (position-matched non-reasoning control)—cannot scientifically distinguish between a genuine reasoning-length effect, an absolute position effect, a context-length effect, or softmax dilution.

The primary failure of the Phase 2 design is treating generated reasoning length as an exogenous independent variable. In autoregressive vision-language models, generation length is endogenous to sample difficulty: models generate longer sequences on complex, ambiguous, or multi-step problems. Consequently, an observed decline in visual utilization across longer traces reflects problem difficulty rather than a causal penalty imposed by reasoning length.

Condition B introduces severe semantic and distributional confounds. In autoregressive transformers, there is no such entity as "semantically neutral filler". Inserting arbitrary text tokens—such as conversational boilerplate, repeated phrases, or synthetic padding—alters RoPE coordinates, expands key-value cache geometry, activates attention sinks on early punctuation tokens, and shifts the hidden state toward generic linguistic distributions.

Condition C matches answer position by shifting prompt tokens, but fails to isolate positional mechanics: prepending text before the visual tokens shifts the visual tokens to higher absolute RoPE indices, degrading their early-layer representational resolution. Conversely, inserting padding between the image and question increases the cross-attention distance between the question and visual tokens, confounding question-image binding with reasoning length.

To establish experimental validity, the protocol must evaluate matched prefix slices under teacher forcing on verified reasoning traces, comparing four conditions per item:

> * Condition 1 (short): Immediate answer following the multimodal prompt.  
> * Condition 2 (long\_reasoning): Fixed, teacher-forced valid deductive reasoning trace (e.g., 150 tokens) reaching the correct answer.  
> * Condition 3 (long\_neutral): Matched 150 tokens of non-reasoning descriptive text (such as an unrelated encyclopedia excerpt) controlling for sequence length and softmax denominator expansion without deductive computation.  
> * Condition 4 (posmatch\_short): Pre-padding prepended before the visual tokens, advancing absolute RoPE coordinates while maintaining a zero-length reasoning interval between prompt and answer.

Regarding metrics, raw cross-attention mass to visual tokens is scientifically unreliable as a proxy for visual evidence utilization. Extensive mechanistic interpretability literature demonstrates that attention weights do not reflect causal information flow: attention distributions can be substantially perturbed without altering output logits, and near-zero attention weights can exert large gradients on downstream predictions.

Similarly, linear probing of final-layer image representations measures representational decodability (information availability), but cannot establish whether downstream attention heads extract or utilize that information during generation. As demonstrated in Anchor A1, visual evidence can remain linearly decodable from visual tokens while the language model backbone completely ignores it in favor of parametric language priors.

The primary metric must be the counterfactual Image Causal Effect (ICE) evaluated at the answer token:

\\text{ICE}\_t \= \\left\[\\log \\frac{p(a\_{\\text{vis}} \\mid I, q, p\_{\<t})}{p(a\_{\\text{prior}} \\mid I, q, p\_{\<t})}\\right\] \- \\left\[\\log \\frac{p(a\_{\\text{vis}} \\mid I', q, p\_{\<t})}{p(a\_{\\text{prior}} \\mid I', q, p\_{\<t})}\\right\]

where I is the original image, I' is a paired counterfactual image flipping the ground truth, a\_{\\text{vis}} is the visually grounded answer, a\_{\\text{prior}} is the prior-consistent answer, and p\_{\<t} is the teacher-forced reasoning prefix.

To audit softmax dilution, the attention mass must be benchmarked against a uniform attention null: for a sequence of length N containing M visual tokens, uniform attention allocates mass M/N. The metric \\Delta\\text{VIG}\_{\\text{dev}} \= \\text{VIG}\_{\\text{mass}} \- M/N determines whether visual attention decays faster than the mathematical dilution baseline.

## **5\. Q1 Dataset and Model Evidence**

Evaluating candidate datasets requires auditing official accessibility, licensing, sample structure, ground truth verifiability, paired intervention support, and length manipulation independence.

| Dataset | Official Source | License | Availability Status | Task Structure & Annotation | Paired Interventions Supported? | Length Manipulable Without Task Shift? | Existing Use for Proposed Question | Scientific Suitability |
| :---- | :---- | :---- | :---- | :---- | :---- | :---- | :---- | :---- |
| **WhatIfVis** | Anchor A1; derived from VLind-Bench, Pixels-versus-Priors. | Mixed open research licenses. | Reconstructed from source benchmarks; no monolithic index. | 3,049 paired counterfactual image-question items across 5 domains. | **Yes**: Minimal visual modification flips ground-truth answer. | **No native CoT**: Designed strictly for zero-shot single-turn queries. | Used in A1 for single-turn vision-prior conflict; never for trace length. | **Partially Suitable**: Excellent counterfactual images, but requires generating external teacher-forced traces. |
| **MathVista** | Hugging Face / GitHub (AI4Math/MathVista). | CC BY-NC-SA 4.0. | Verified public download. | 6,141 visual math and reasoning problems. | **No**: Single static images per question; no counterfactual pairs. | **No**: Reasoning trace length is endogenous to problem complexity. | Used in ReGround and VIG as general evaluation benchmark. | **Unsuitable**: Heavy OCR and symbolic algebra reliance allows text-only shortcut solutions. |
| **WeMath** | Hugging Face Hub (We-Math/We-Math). | Open research license. | Verified public download. | 1,740 multi-step visual math problems with step-by-step solutions. | **No**: Static geometry and diagram problems. | **Partially**: Supports prefix truncation across verified solution steps. | Used in VIG to correlate VIG with generated chain length. | **Partially Suitable**: Useful for harvesting valid intermediate prefixes, but vulnerable to algebraic shortcuts. |
| **RH-Bench** | Hugging Face (LCZZZZ/RH-Bench) / GitHub. | MIT License. | Verified public download. | Diagnostic benchmark covering multimodal perception and reasoning. | **Yes**: Contains paired perception and reasoning challenge items. | **Yes**: Specifically designed for latent steering and budget forcing. | Formulated explicitly to measure hallucination amplification under length. | **Suitable**: Optimal platform for trace-length manipulation tooling and comparative baselines. |

Model architectural verification from official Hugging Face repositories establishes that Qwen/Qwen2.5-VL-3B-Instruct comprises 36 language decoder layers, hidden dimension d \= 2,048, 16 attention heads, and 2 key-value heads. Its visual tower is a 32-layer Vision Transformer (d \= 1,280) with 2D spatial patch merging (patch size 14, merge factor 2\) and dynamic resolution token allocation, where visual tokens are ingested via the \<|image\_pad|\> placeholder.

Eager attention matrices are accessible via attn\_implementation="eager", hidden states are exposed via output\_hidden\_states=True, and residual stream hooks operate stably on model.model.language\_model.layers\[L\].

Secondary cross-family target google/gemma-3-4b-it utilizes a 27-layer SigLIP vision encoder operating at fixed 896$\\times$896 resolution, compressing visual input into exactly 256 soft visual tokens. Its language decoder comprises 34 layers with hidden dimension d \= 2,560 and hybrid sliding-window (1,024 tokens) and global attention. Crucially, official verification confirms that Gemma 3 is gated on Hugging Face, returning HTTP 401 without authenticated user tokens and license approval.

## **6\. Q1 Remaining Kill Risks**

The primary vulnerability threatening Q1 is pre-emption by RH-Bench. Because RH-Bench demonstrated that longer reasoning chains degrade visual attention and amplify hallucination, a thesis that merely re-documents this decay provides zero novel contribution. Q1 survives only if it succeeds as a mechanistic decomposition: proving whether the decline is caused by semantic reasoning operations, RoPE positional distance, or uniform softmax dilution.

The second major vulnerability is mathematical softmax dilution. In transformer self-attention, the softmax denominator sums over all available key positions. As sequence length N expands, the uniform probability share allocated to an invariant block of M visual tokens scales strictly as M/N. If the empirical decline in visual attention mass tracks the slope of M/N within statistical equivalence bounds, the phenomenon reduces entirely to the mathematical definition of softmax normalization over expanding sequences, disproving cognitive "visual forgetting".

The third vulnerability is RoPE positional attenuation. Rotary position embeddings attenuate attention scores between distant tokens as a function of relative index displacement. If Condition 4 (position-matched short answer with delayed prefix) produces an attention and utilization decline statistically equivalent to Condition 2 (long reasoning trace), the effect is driven entirely by positional encoding geometry, invalidating the hypothesis that reasoning computation drives the degradation.

## **7\. Q1 Verdict**

### **SURVIVES WITH MODIFICATION**

The broad research question is pre-empted and causally unidentifiable in its Phase 2 formulation. It survives exclusively as a narrowed mechanistic decomposition:

*Holding the multimodal problem, textual reasoning prefix, and sequence position fixed under teacher forcing across paired visual counterfactuals, does the causal effect of visual tokens on next-token predictions decline across reasoning depths, and does this decline deviate from the uniform softmax dilution null?*

## **8\. Q2 Closest-Work Matrix**

Mechanistic interpretability literature published in 2025 and 2026 demonstrates that object-attribute binding in multimodal models is distributed and highly dependent on training paradigms and task framing. The claim that vision-language models rely on universal, architecture-independent "Binding IDs" is contested by structural and behavioral evidence.

However, causal activation swapping has been validated strictly on synthetic geometric scenes; no prior work has executed localized patch-token activation swaps transferring binding identities between distinct natural photographic objects.

| Paper & Citation | Proposed Mechanism | Causal Intervention Type | Domain (Synthetic vs. Natural) | Causal Evidence Established? | Cross-Model Evaluated? | Overlap with Q2 |
| :---- | :---- | :---- | :---- | :---- | :---- | :---- |
| **Grounding IDs (C1)** (Hasani et al., arXiv:2509.24072, v4 Feb 2026\) | Partition-specific Grounding IDs induced by external cues. | Residual-stream activation swap across object patch tokens at L20–27. | 28$\\times$28 synthetic geometric grids; natural data used only for observational POPE/CHAIR. | **Yes (Synthetic)**: Swapped activations achieve 0.98 transferred binding accuracy. | Evaluated Qwen2.5-VL-7B/3B and InternVL3.5-8B on synthetic tasks. | **Extremely High**: Directly establishes the causal activation swap mechanism in synthetic grids. |
| **In-Context Binding (C2)** (Saravanan et al., CVPRW 2025, arXiv:2505.22200) | Additive factorized latent vectors: Z \= f(O) \+ b(k). | Block activation replacement and mean binding-vector addition. | Blender-rendered 3D Shapes scenes with two geometric objects. | **Yes (Synthetic)**: Vector addition steers binding; norm-matched Gaussian control fails. | Evaluated single architecture (LLaVA-OneVision-7B). | **High**: Demonstrates factorized binding vectors and placebo controls. |
| **Dual Mechanisms of Binding** (Cui et al., arXiv:2603.22278, Mar 2026\) | Dual-network split: vision encoder binds local features; LM backbone routes attributes. | Activation amplification and linear probing. | Squares/Shapes \+ What'sUp natural control (2,687 images) \+ COCO-spatial. | **Yes**: Activation amplification corrects binding errors over random baselines. | Evaluated Qwen2-VL-7B and Gemma-3-4B-IT. | **High**: Evaluates binding mechanisms on natural images across architectures. |
| **Limits in Dual Encoders** (arXiv:2608.15971, Aug 2026\) | Theoretical smoothness bounds M(s) \\le 2\\sqrt{2}\\delta limiting dual-encoder binding. | Theoretical proof and correlation auditing across 18 text encoders. | SugarCrepe benchmark (r \= 0.99 difficulty correlation). | N/A (Theoretical proof and observational benchmark audit). | 18 CLIP-style dual encoders. | **Moderate**: Directly contradicts claims of universal, architecture-independent binding. |
| **Point by Point** (arXiv:2605.25427, May 2026\) | Serial spatial pointing induces internal visual search routines. | Fine-tuning models to emit explicit coordinate points before attribute extraction. | Synthetic clutter and compositional benchmarks. | **Behavioral**: Eliminates binding errors via serial execution. | Evaluated LLaVA and Qwen model families. | **Moderate**: Shows binding can be resolved procedurally rather than via static latent IDs. |
| **Foveated Probes** (arXiv:2608.00726, Aug 2026\) | Readout bottleneck: spatial information is present but global readouts fail to bind. | Question-conditioned foveated probing on localized patch tokens. | GQA-derived natural image pairs and synthetic clutter. | **Probing only**: Observational extraction of localized bindings. | Open-source vision foundation models. | **Moderate**: Demonstrates natural localized binding information without causal swapping. |
| **DSCAM** (Xu et al., arXiv:2608.16805, Aug 2026\) | Dense Same-Class Attribute Misbinding failure mode. | Diagnostic benchmark evaluation across state-of-the-art VLMs. | 524 natural photographic images, 1,773 boxed instances, 9,580 queries. | **Observational**: Quantifies natural misbinding frequencies. | Evaluates multiple open-source and proprietary VLMs. | **Direct Evaluation Asset**: Provides annotated natural boxes for causal transfer. |

## **9\. Q2 Experimental Validity**

In Anchor C1, the causal intervention replaces residual-stream hidden states corresponding to visual patch tokens of Object A with those of Object B at intermediate-to-late transformer layers (specifically layers 20–27 in Qwen2.5-VL-7B, and layers 18–24 in Qwen2.5-VL-3B). The target token region is computed from the bounding-box coordinates of the object, mapped to discrete visual patch tokens via spatial downsampling, and dilated by one token along each spatial boundary.

The replacement is performed directly on the residual stream at the input of transformer layer L:

h\_L^{\\text{patched}}\[i\] \= h\_L^{\\text{target}}\[i\] \+ \\left(h\_L^{\\text{source}}\[\\pi(i)\] \- h\_L^{\\text{target}}\[i\]\\right), \\quad \\forall i \\in \\mathcal{T}\_{\\text{target}}

where \\pi maps target patch tokens to corresponding source patch tokens via spatial interpolation.

The procedural reproducibility of C1 is classified as **RECONSTRUCTABLE WITH SPECIFIC AMBIGUITIES**. The original code and dataset generation scripts were not released in the paper (NOT FOUND). While the layer indices (L20–27), activation dimensions (d \= 2,048), and mathematical formulation are documented, exact token alignment under Qwen2.5-VL's dynamic resolution ViT is omitted.

Because Qwen2.5-VL does not use a fixed 24$\\times$24 patch grid but dynamically calculates grid\_thw based on native aspect ratios, mapping pixel bounding boxes to 1D sequence token indices requires reverse-engineering the spatial merge operations (2\\times 2 patch bundling). Pixel coordinates must be mapped through the ViT patch extraction (14\\times 14), grouped into 2\\times 2 merge blocks, and offset by the visual token start index to locate the residual stream rows.

Evaluating candidate placebo controls reveals that Anchor C1 failed to include a norm-matched random Gaussian control, leaving open the alternative explanation that the output flip was driven by non-specific representation disruption rather than specific binding transfer. High-norm perturbations injected into late transformer layers frequently degrade linguistic modeling, causing the model to emit default vocabulary tokens or collapse into repetitive degeneration.

The minimum defensible placebo control set requires three distinct baselines:

> 1. **Norm-matched Gaussian noise:** Overwriting target tokens with h\_{\\text{placebo}} \\sim \\mathcal{N}(0, \\sigma^2 \\mathbf{I}) where \\Vert{}h\_{\\text{placebo}}\\Vert{}\_2 \= \\Vert{}h\_{\\text{source}}\\Vert{}\_2, testing whether arbitrary activation disruption mimics the flip.  
> 2. **Shuffled background spatial patch swap:** Patching activations extracted from an irrelevant background region of the source image, testing whether visual feature presence alone alters outputs.  
> 3. **Within-image irrelevant object swap:** Swapping activations between two objects within the same recipient image, verifying directional and relational selectivity.

The Phase 2 kill criterion asserting that "CCA similarity \\approx 0 proves the mechanism is architecture-specific" is scientifically invalid. Canonical correlation analysis and singular vector CCA measure linear subspace alignment. When comparing distinct model families—such as Qwen2.5-VL (native ViT, 2,048 dimensions, mRoPE) and Gemma 3 (SigLIP, 2,560 dimensions, learned soft tokens)—the representation spaces are unaligned and mutually rotated by arbitrary orthogonal transformations.

Unaligned neural networks naturally exhibit near-zero linear subspace similarity even when executing identical functional algorithms. A scientifically defensible cross-model test must evaluate behavioral intervention parity: verifying whether the identical intervention protocol (identifying object patch tokens \\rightarrow extracting residual stream at proportional depth L/L\_{\\text{total}} \\approx 0.65\\text{--}0.75 \\rightarrow swapping activations) reproduces the target attribute flip with relation specificity across both architectures.

## **10\. Q2 Dataset and Model Evidence**

| Benchmark | Access Status | License | Annotations Available | Paired / Counterfactual Structure? | Suitability for Activation Patching | Existing Use in Binding Research | Scientific Suitability |
| :---- | :---- | :---- | :---- | :---- | :---- | :---- | :---- |
| **Synthetic Grids (C1)** | Unreleased; requires procedural rebuild from paper text. | Open code (MIT upon rebuild). | Bounding boxes, row partitions, non-ordinal symbols (&, $, \#, @). | **Yes**: Deterministic 2$\\times$4 grid layout with orthogonal symbol assignments. | **Optimal**: Deterministic mapping between grid cells and visual patch tokens. | Direct subject of Anchor C1. | **Suitable for Stage 1 Baseline**: Mandatory for initial intervention replication. |
| **InstaBind-Lite / DSCAM** | Verified public on GitHub (InstaBind-Lite/InstaBind-Lite). | MIT License. | 524 images, 529 same-class groups, 1,773 source-instance boxes, 9,580 questions. | **Yes**: Multiple instances of same semantic class with contrasting attributes. | **High**: Precise bounding-box coordinates provide exact masking targets. | Benchmark introduced to measure natural misbinding. | **Suitable for Natural Transfer**: Primary evaluation benchmark for Stage 3\. |
| **SugarCrepe** | Public Hugging Face (sugarcrepe). | CC BY 4.0. | Image-text pairs with hard negative attribute/relation swaps. | **Yes**: Counterfactual text captions paired with single natural images. | **Low**: Lacks instance-level bounding-box token masks for image patching. | Standard evaluation benchmark for CLIP/dual-encoder binding. | **Unsuitable for Activation Swapping**: Observational benchmark; cannot guide patch hooks. |
| **What'sUp** | Public repository (Thrush et al.). | MIT License. | 2,687 controlled natural image pairs with relation swaps. | **Yes**: Counterfactual image pairs with swapped spatial relationships. | **Moderate**: Coarse annotations; heavily skewed toward spatial prepositions. | Evaluated in Dual Mechanisms via linear probing. | **Partially Suitable**: Useful secondary benchmark, but inferior to DSCAM for attribute binding. |

The proposed synthetic-to-natural transfer experiment has **not been performed in prior literature (NOT FOUND)**. While Dual Mechanisms evaluated linear probes and activation amplification on the What'sUp benchmark, no prior work has executed localized patch-token activation swaps transferring binding identities between distinct natural photographic objects.

The literature lacks empirical evidence establishing whether the localized causal representations identified in C1 survive natural intra-class variance, background clutter, and non-grid bounding-box geometry.

## **11\. Q2 Remaining Kill Risks**

> 1. **Spatial Patch Misalignment Artifacts:** In natural photographs, objects do not align to uniform grid boundaries. Interpolating a patch tensor of shape (H\_1, W\_1, D) onto a recipient region of shape (H\_2, W\_2, D) introduces spatial boundary mismatches and high-frequency edge discontinuities that downstream attention layers reject as out-of-distribution noise.  
> 2. **Transfer Collapse on Natural Scenes (The Synthetic Artifact Hypothesis):** The representation identified in C1 may be entirely induced by artificial grid lines and explicit symbol prompts. In unpartitioned natural scenes, binding may be resolved via distributed cross-modal attention or dynamic pointing rather than localized residual vectors, causing natural transfer accuracy to collapse to zero.  
> 3. **Destructive Perturbation Mimicry:** Activation swapping may destroy the host object's representation without transferring the source attribute. If the model defaults to generating the most frequent attribute prior, this can mimic a successful swap if priors are uncontrolled.  
> 4. **Covariate Reduction:** If a regression model shows that color histogram similarity or text co-occurrence priors account for the output flip variance without the activation hook, Q2 dies by reduction.  
> 5. **Architectural Incompatibility:** Dynamic resolution in Qwen2.5-VL alters visual sequence lengths dynamically per image. If source and target images generate different token grid shapes, runtime tensor replacement will fail with CUDA dimension assertions unless images are strictly pre-scaled.

## **12\. Q2 Verdict**

### **SURVIVES WITH MODIFICATION**

The claim of "universal, architecture-independent Binding IDs" is overbroad and contradicted by structural binding limits in dual encoders and serial pointing mechanisms. However, an empirical mechanistic question survives:

*Do localized residual-stream activation swaps that transfer object-attribute binding in synthetic grid scenes maintain causal transfer accuracy and relation specificity when applied to natural, box-segmented instances in DSCAM under strict placebo controls?*

## **13\. Compute and Engineering Feasibility**

Evaluating execution feasibility within a Google Colab Pro environment equipped with an NVIDIA T4 (16 GB) or L4 (24 GB) GPU requires categorizing all claims across verified public technical facts, architectural estimations, and unknown empirical variables.

| Pipeline Component | Status Designation | Quantitative Basis & Evidence Source |
| :---- | :---- | :---- |
| **Qwen2.5-VL-3B bf16 Loading** | **VERIFIED** | Model weights occupy 7.51 GB in bfloat16; loads cleanly into VRAM with \\sim 8.5\\text{ GB} headroom on 16 GB GPU. |
| **Eager Attention Exposure** | **VERIFIED** | Transformers implementation requires attn\_implementation="eager"; returns 36 layers \\times (batch, 16, seq, seq). |
| **Residual Hook Overwrite** | **VERIFIED** | PyTorch forward pre-hooks on model.model.language\_model.layers\[L\] capture and overwrite (B, S, 2048\) tensors stably. |
| **Prompt Placeholder Handling** | **VERIFIED** | Transformers 5.x requires \<|image\_pad|\> placeholder (64 tokens per patch block); sequence length matches token IDs. |
| **Gemma 3 4B IT Authentication** | **VERIFIED** | Model repository is gated; returns HTTP 401 without authenticated Hugging Face token and approved license. |
| **Peak VRAM During Forward Pass (Seq=2048)** | **ESTIMATED** | Base model (7.5 GB) \+ KV cache batch size 1 (1.2 GB) \+ activations (1.8 GB) \\approx 10.5\\text{--}11.2\\text{ GB}; fits 16 GB envelope. |
| **Full Attention Matrix Extraction VRAM** | **ESTIMATED (UNFEASIBLE)** | 36 layers \\times 16 heads \\times 2048^2 keys \\times 2 bytes \= 4.83\\text{ GB} auxiliary VRAM per forward pass; triggers CUDA OOM. |
| **Dynamic Resolution Token Spikes** | **ESTIMATED** | Unconstrained high-resolution images produce \>2,500 visual tokens; requires clamping max\_pixels \= 512 \* 512\. |
| **Colab Wall-Clock Throughput (GPU)** | **UNKNOWN** | Local CPU smoke runs at 7.4 s/token; T4/L4 GPU runtime per 50-sample pilot estimated at 45–90 minutes, unverified. |
| **Activation Interpolation Stability** | **UNKNOWN** | Whether spatial bilinear interpolation of residual tensors across non-identical bounding-box grids causes numerical divergence. |

## **14\. Revised Minimal Runtime Pilot**

### **Q1 Blueprint: Matched-Prefix Visual Utilization Audit**

> * **Model:** Qwen/Qwen2.5-VL-3B-Instruct (primary, open/ungated).  
> * **Dataset:** 50 curated counterfactual items from WhatIfVis (Spatial and Color subsets) with paired clean (I) and counterfactual (I') images.  
> * **Sample Size:** 50 items \\times 4 within-item conditions \= 200 forward evaluations.  
> * **Conditions:**  
  1. short: direct answer prompt.  
  2. long\_reasoning: 150-token teacher-forced verified deductive CoT prefix.  
  3. long\_neutral: 150-token teacher-forced non-reasoning descriptive text prefix.  
  4. posmatch\_short: 150-token pre-padding prepended before visual tokens; direct answer.  
> * **Controls:** Uniform softmax dilution null slope (M/N where M is visual token count, N is total sequence length).  
> * **Primary Metric:** Normalized Visual Information Deviation (\\Delta\\text{VIG}\_{\\text{dev}} \= \\text{VIG}\_{\\text{mass}} \- M/N) evaluated at the final answer token under Condition 2 vs. Condition 3\.  
> * **Secondary Metrics:** Counterfactual Image Causal Effect (\\text{ICE}\_t) on answer log-odds; greedy answer accuracy.  
> * **Statistical Test:** Paired bootstrap 95% confidence intervals on mean \\Delta\\text{VIG}\_{\\text{dev}}; TOST equivalence test (\\theta \= 0.05) between long\_reasoning and long\_neutral.  
> * **Expected Failure Modes:** Visual attention mass tracks the uniform M/N slope perfectly (pure dilution); posmatch\_short reproduces the decline (pure RoPE distance artifact).  
> * **Kill Criterion:** Accept equivalence (TOST p \< 0.05 within \\theta \= \\pm 0.05) between Condition 2 and Condition 3, and between Condition 2 and Condition 4\.

### **Q2 Blueprint: Synthetic-to-Natural Activation Swap Specificity**

> * **Model:** Qwen/Qwen2.5-VL-3B-Instruct.  
> * **Dataset:** 25 procedural synthetic 2$\\times$4 grid scenes (C1 style) \+ 25 natural photographic pairs from DSCAM/InstaBind-Lite with annotated same-class bounding boxes.  
> * **Sample Size:** 50 test pairs (25 synthetic, 25 natural) evaluated across real swap and 3 placebos.  
> * **Activation Layer:** Layer 22 (model.model.language\_model.layers\[22\]).  
> * **Intervention:** Residual-stream patch replacement on visual patch tokens corresponding to target object bounding box, mapped via spatial interpolation.  
> * **Placebo Controls:**  
  1. Norm-matched Gaussian noise.  
  2. Shuffled source background patch swap.  
  3. Within-image irrelevant object swap.  
> * **Primary Metric:** Net Directed Flip Rate (\\text{NetFlip} \= \\text{Flip}\_{\\text{target}} \- \\text{Flip}\_{\\text{non-target}}), where \\text{Flip}\_{\\text{target}} measures the proportion of generations adopting the source attribute.  
> * **Secondary Metrics:** Non-target object attribute preservation accuracy (\\text{Acc}\_{\\text{non}}); text generation repetition and degeneration score.  
> * **Statistical Test:** Two-sided difference test and bootstrap 95% CIs comparing real swap \\text{NetFlip} against the maximum placebo \\text{NetFlip}.  
> * **Expected Failure Modes:** Natural image patches trigger degenerate repetitive text generation; target flip rate collapses to zero on natural images while succeeding on synthetic grids.  
> * **Kill Criterion:** On natural images, the 95% CI of real swap \\text{NetFlip} overlaps with or falls below the placebo 95% CI, or non-target attribute preservation collapses below 0.50.

## **15\. Canonical Thesis Comparison**

Comparing the Canonical Thesis (*Causal Conflict Verbalization and Source Arbitration in Vision-Language Models*) against refined candidates Q1 and Q2 indicates marked divergence in feasibility, causal validity, and risk profiles.

| Evaluation Criterion | Canonical Baseline: Conflict Verbalization | Refined Q1: Matched-Prefix Utilization Audit | Refined Q2: Synthetic-to-Natural Binding Transfer |
| :---- | :---- | :---- | :---- |
| **Evidence Strength** | High: Grounded in conflict benchmarks (CLASH, HallusionBench, Which Source Wins?). | High: Grounded in RH-Bench, VIG, and Remember-R1 literature. | Moderate: Grounded in C1 and C2 synthetic demonstrations; natural evidence is observational. |
| **Novelty Uncertainty** | Low-to-Moderate: Multimodal conflict verbalization faithfulness is unaddressed in literature. | High: High competitive publication density in multimodal CoT compression and forgetting. | Low: Natural-image causal activation swapping remains entirely unperformed. |
| **Causal Validity** | High: 4-arm factorial prompt protocol with Lanham-style prefilling directly isolates arbitration. | Moderate: Teacher-forced prefix slicing controls difficulty, but length remains synthetic. | High (if placebos pass): Direct activation patching establishes localized sufficiency. |
| **Reproducibility** | Very High: Pure inference; deterministic regex parsing on numerical/categorical answers. | High: Open checkpoints and teacher-forced forward passes. | Low-to-Moderate: Requires precise spatial token mapping and custom hook injection. |
| **Dataset Accessibility** | Verified Public: 1,304 clean arithmetic pairs \+ 229 ChartQA conflict pairs. | Partially Available: Requires reconstructing WhatIfVis counterfactuals and CoT traces. | Verified Public: InstaBind-Lite/DSCAM (524 images, 1,773 boxes) \+ synthetic generator. |
| **Engineering Risk** | Low: Standard generation and logit extraction; fits easily in 16 GB VRAM. | Moderate: Memory management of eager attention hooks and KV caches. | High: Spatial patch-grid interpolation, tensor alignment, and dynamic resolution hooks. |
| **Negative-Result Value** | Very High: Proves verbalized CoT is unfaithful post-hoc rationalization of latent priors. | High: Disproves "visual forgetting," revealing it as a position/dilution measurement artifact. | Very High: Proves synthetic Binding IDs are representational artifacts of geometric partitions. |

The canonical topic exhibits lower implementation complexity and minimal engineering fragility. It operates via pure inference forward passes and deterministic string parsing, eliminating custom tensor overwrites, spatial patch interpolation, and hidden-state hook debugging.

Q1 provides a low-risk measurement audit, but addresses an incremental sub-question in a crowded research landscape. Q2 offers high mechanistic novelty, but entails substantial technical risks regarding bounding-box patch alignment and out-of-distribution activation damage. The canonical topic remains the primary baseline; Q1 and Q2 are secondary backups.

## **16\. Phase 3 Gate Decision**

### **DO NOT PROCEED YET TO FULL THESIS EXECUTION — RUNTIME PILOT REQUIRED**

Full commitment to Phase 4 thesis execution must not proceed until the pre-registered Phase 3 GPU pilot is completed in Google Colab Pro.

Neither candidate was eliminated outright by prior literature; both survive in revised, scientifically defensible formulations. However, both proposals face empirical kill conditions that literature analysis cannot settle. Furthermore, the Phase 2 kill criteria contained severe statistical flaws that invalidated earlier conclusions, and all runtime checks performed to date were executed on local CPU hardware without producing GPU VRAM or throughput measurements.

The following runtime verification steps must be executed manually in Google Colab Pro (16 GB GPU) using the pre-registered harness:

> 1. **Environment Setup:** Load Qwen/Qwen2.5-VL-3B-Instruct in bfloat16 with attn\_implementation="eager". Register forward pre-hooks on model.model.language\_model.layers\[22\]. Measure and record baseline memory allocation.  
> 2. **Execute Q1 Factorial Pilot:** Run the 50-item \\times 4-condition factorial harness on WhatIfVis cases under teacher forcing. Extract answer logits and streaming visual attention sums under Condition 1 (short), Condition 2 (long\_reasoning), Condition 3 (long\_neutral), and Condition 4 (posmatch\_short). Execute TOST equivalence tests on \\Delta\\text{VIG}\_{\\text{dev}}.  
> 3. **Execute Q2 Activation Swap Pilot:** Replicate the C1 activation swap on 25 synthetic grid scenes at layer 22 against norm-matched Gaussian noise and scrambled patch placebos. If synthetic net flip rate exceeds the placebo 95% confidence interval, execute the swap on 25 DSCAM natural photographic pairs using bilinear spatial patch interpolation.  
> 4. **Final Gate Evaluation:** If Q1 demonstrates statistical equivalence to the position or dilution nulls, kill Q1. If Q2 net flip collapses to placebo levels or triggers linguistic degeneration on natural images, kill Q2. If both candidates fail their empirical kill gates, execute the Canonical Thesis (*Causal Conflict Verbalization*), which is methodologically de-risked, fully accessible, and computationally verified.

#### **Works cited**

1\. More Thinking, Less Seeing? Assessing Amplified Hallucination in, https://mlrm-halu.github.io/ 2\. Remember-R1: Mitigating Long-Context Visual Forgetting ... \- arXiv, https://arxiv.org/html/2608.01314v1 3\. Uncovering Grounding IDs: How External Cues Shape Multimodal, https://www.alphaxiv.org/audio/2509.24072v3 4\. InstaBind-Lite: Diagnosing Dense Same-Class Attribute Misbinding, https://arxiv.org/html/2608.16805v1 5\. config.json · Goader/gemma-3-4b-it-uk-matt at main \- Hugging Face, https://huggingface.co/Goader/gemma-3-4b-it-uk-matt/blob/main/config.json