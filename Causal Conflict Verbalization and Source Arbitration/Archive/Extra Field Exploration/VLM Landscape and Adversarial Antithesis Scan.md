# **Multimodal Vision-Language Thesis Subfield Landscape and Adversarial Antithesis Audit**

## **Executive Finding**

An adversarial audit of the 2025–2026 multimodal vision-language learning literature demonstrates that the three candidate hypothesis spaces exhibit starkly unequal degrees of scientific maturity, terminological stability, and empirical crowding. The initial labels proposed for these candidate areas fail to match the operational taxonomy used in contemporary literature. Treating these research spaces at face value without systematic terminological substitution creates an illusion of novelty that dissolves under closer examination.

Candidate Area A, originally designated as multimodal chain-of-thought dynamics and visual attention drift, does not exist as an independent, recognized research discipline under that phrasing. Frontline investigations examine these mechanisms under the frameworks of multimodal test-time scaling, visual context sensitivity, post-perceptual visual evidence utilization, and interleaved reasoning trace dynamics. The broad assertion that vision-language models suffer from visual neglect or text-prior takeover is already heavily occupied. Recent studies demonstrate that visual representations often survive pretraining projection and remain linearly decodable in final transformer layers, yet fail to be causally integrated into autoregressive token generation when language priors conflict with visual context. While the broad phenomenon of visual neglect is occupied, a narrower, technically rigorous question remains open: whether visual token utilization degrades as a causal function of reasoning trace length when isolating length from sequence position, total context length, and attention normalization artifacts.

Candidate Area B, initially termed cross-modal in-context learning and multimodal induction, represents an active, recognizable, yet heavily occupied subfield. Recent literature has dissected multimodal in-context learning by separating task-mapping construction from task-mapping transfer, while isolating induction-style label-copying circuits using mechanistic head knockouts in both controlled architectures and open production models. Demonstrating that multimodal in-context learning is sensitive to prompt ordering or that models rely on unimodal textual shortcuts is already heavily documented. The primary unresolved uncertainty in this domain is whether genuine cross-modal task induction operates over natural, complex photographic scenes, or whether few-shot multimodal gains reduce entirely to in-context textual calibration paired with zero-shot visual classification.

Candidate Area C, presented as visual representation binding and compositional grounding, is fragmented across disparate literatures, including compositional zero-shot evaluation, mechanistic circuit tracing, and prompt-based visual scaffolding. The foundational observation that models fail to bind visual attributes to corresponding objects is heavily documented across classical and modern benchmarks. Recent mechanistic studies have isolated Binding IDs and Grounding IDs—abstract latent representations that route spatial coordinates and visual attributes to textual entities. However, these binding circuits have predominantly been demonstrated on synthetic images featuring geometric primitives. Whether these binding mechanisms represent universal transformer operations or brittle, task-specific artifacts on synthetic layouts remains largely unverified.

From a resource and infrastructure perspective, conducting full-scale mechanistic interpretability on frontier models (such as training cross-layer transcoders or computing complete attribution graphs) is computationally prohibitive on academic cloud environments. Transcoder training for Gemma-3-4B-it, for example, requires tens of hours across multi-node H100 clusters. Nevertheless, small open-weight models (such as Qwen2.5-VL-3B/7B, Gemma-3-4B, and SmolVLM) permit rigorous behavioral intervention, linear activation probing, and low-rank causal activation patching within single-GPU budgets.

Broad claims regarding language bias, demonstration sensitivity, and attention decay are thoroughly occupied. A viable thesis must abandon exploratory observational phenomenology and instead deploy counterfactual interventions, strict sequence-length controls, and falsifiable behavioral-mechanistic hypotheses.

## **Landscape Comparison**

The operational and mechanistic characteristics of the three surveyed research domains demonstrate varying levels of empirical saturation, confounding risks, and infrastructure requirements, as detailed in the comparative matrix below.

| Dimension | Field A: Visual Evidence Utilization & Inference Scaling | Field B: Multimodal In-Context Learning & Task Induction | Field C: Mechanistic Compositional Grounding & Binding |
| :---- | :---- | :---- | :---- |
| Scientific identity | Visual evidence utilization and multimodal inference-time reasoning | Cross-modal task induction and multimodal demonstration learning | Mechanistic compositional grounding and visual entity-attribute binding |
| Active 2025–2026 research | Visual context sensitivity, visual latent reasoning, test-time compute allocation, reasoning trace compression | Task-mapping construction vs. transfer, multimodal induction heads, modality asymmetry, paired counterfactual diagnosis | Grounding IDs, Binding IDs, visual symbolic mechanisms, layer-wise information routing, activation patching |
|  | Main mechanisms | Post-perceptual utilization failure, parametric prior suppression, visual token pruning, visual relay scheduling | Induction-style label copying, task-vector compression, cross-modal alignment bottlenecks, textual shortcuts |
| Major benchmarks | WhatIfVis, MathVista, MMMU, HallusionBench, VisReason | Open-MI, TrueMICL suites, OK-VQA, CLBench-V, TwinICL suites | Winoground, SugarCrepe, CLEVR, GQA, synthetic attribute-shape grids |
| Typical models | Qwen2.5-VL (3B/7B), Gemma-3-4B, LLaVA-NeXT, SmolVLM | Qwen2.5-VL, Gemma-3, IDEFICS-2/3, small controlled transformers | Gemma-3-4B, Qwen2.5-VL-7B, LLaVA-1.5/1.6, CLIP ViT |
| Main methodology | Paired counterfactual prompting, linear probing of final image tokens, token ablation, test-time search | Matched modality baselines, label permutation, head knockout, task-vector injection | Causal activation swapping, linear probing across layers, synthetic image generation, visual scaffolding |
| Literature crowding | Crowded in broad form; heavily crowded regarding generic language prior dominance | Heavily occupied in benchmark perturbation; moderately crowded in mechanistic circuits | Moderately crowded; mechanistic binding literature is nascent but growing rapidly |
| Mechanistic maturity | Medium; clear separation of encoding vs. utilization, but dynamic CoT tracking is unstable | High in synthetic setups; medium in large-scale open-weight MLLMs | Medium-low; established for toy geometric scenes, unverified on natural complex scenes |
| Shortcut/confound risk | Severe: sequence position, attention sink dynamics, answer formatting, pretraining priors | Severe: label distribution priors, in-context semantic matching, zero-shot visual bias | High: spatial template regularities, object frequency biases, visual saliency imbalances |
| Public-data availability | High; WhatIfVis, MMMU, MathVista readily accessible on Hugging Face | High; standard VQA and synthetic induction datasets publicly distributed | High; CLEVR, Winoground, and synthetic generation pipelines are public |
| Small-model feasibility | High for behavioral probing; low for full internal circuit discovery | High for behavioral and activation probing; low for large many-shot contexts | High for synthetic activation swapping; low for automated multi-layer transcoder training |
| Potential empirical contribution | High, if isolating trace length from positional confounds via causal interventions | Medium; limited unless testing natural image task-rule transfer against shortcuts | High, if rigorously testing whether latent binding IDs generalize beyond toy synthetic grids |
| Current uncertainty | Causality of visual token utilization decay across extended reasoning tokens | True rule transfer vs. surface lexical matching in natural multimodal demonstrations | Universality and architecture-independence of latent binding identifiers |

A critical scientific vulnerability in multimodal interpretability research is the conflation of tasks, mechanisms, methods, and benchmarks. A research problem represents the fundamental failure mode or architectural anomaly under examination, such as why a model fails to bind an attribute to an object or why it ignores visual tokens during extended deduction. This problem must be distinguished from the underlying mechanism, which denotes the specific causal or representational operation occurring inside the model, such as late-layer parametric prior override, attention sink saturation, or induction-head label copying.

Similarly, tasks define functional behavioral objectives, such as visual question answering or outlier identification, which can often be solved through unintended statistical shortcuts rather than the targeted mechanism. Methods encompass the diagnostic or interventional tools applied to the system, such as linear activation probing, activation patching, or token ablation. Benchmarks represent static evaluation collections that may fail to isolate the intended mechanism due to formatting artifacts or text-only leakage. Experimental interventions denote the precise independent variables manipulated by the researcher—such as inserting length-matched neutral text padding, swapping activation vectors, or permuting demonstration label tokens—to establish causal relationships.

## **Paper Landscape**

### **Field A: Visual Evidence Utilization and Inference Scaling**

The literature on visual evidence utilization during multi-step reasoning focuses on diagnosing whether models maintain visual grounding throughout extended generative sequences or succumb to language prior dominance.

In *Seeing or Knowing? Visual Context Sensitivity in Multimodal Large Language Models*, the research addresses whether vision-centric reasoning failures stem from perceptual encoding degradation in the vision transformer or post-perceptual utilization failures in the language backbone. The investigation uses the WhatIfVis benchmark, comprising 3,108 manually inspected counterfactual samples spanning spatial-temporal, color, count, size, and weight dimensions, evaluated across six open-weight models from the Qwen and Gemma families. By training generative pixel-level reconstruction probes on the final-layer image tokens of frozen models, the study demonstrates that coarse visual attributes remain decodable, establishing that perceptual representation survives the visual encoder and multimodal projector. The observed behavioral failure is localized via activation patching to intermediate decoder layers, where an unstable decision setpoint causes strong parametric language priors to override visual evidence. The study introduces a one-dimensional steering vector capable of modulating visual context sensitivity, but its evaluation is confined to single-turn question answering without tracking extended multi-step reasoning traces.

In *Look Light, Think Heavy: What Multimodal Chain-of-Thought Reasoning Can and Cannot Do*, the analysis investigates whether scaling intermediate textual reasoning tokens improves visual grounding or primarily amplifies language-model fluency. Evaluating recent open-weight and proprietary reasoning models across MMMU, MathVista, and HallusionBench, the study manipulates the reasoning budget allocated to intermediate textual rationales. The authors observe that while extended textual deduction improves symbolic and mathematical performance, it fails to improve—and in specific instances degrades—fine-grained visual verification accuracy, establishing that test-time textual compute does not scale visual evidence reliance monotonically. The methodology remains primarily behavioral and does not perform internal activation probing to determine whether the visual signal degrades or is simply bypassed.

In *AIM-CoT: Active Information-Driven Multimodal Chain-of-Thought for Vision-Language Reasoning*, the authors examine the limitations of passive, static visual token insertion during multi-step reasoning. Across multi-discipline visual reasoning benchmarks, the intervention introduces an active information-gain trigger that dynamically queries sub-regions of the input image based on intermediate reasoning uncertainty, appending localized visual tokens into the reasoning context. The empirical findings reveal that dynamically triggered visual re-inspection outperforms static single-pass tokenization, indirectly indicating that standard autoregressive models experience visual token attenuation unless visual evidence is explicitly re-injected. However, the study relies on architectural prompting scaffolding rather than diagnosing native transformer attention dynamics.

In *Argus: Vision-Centric Reasoning with Grounded Chain-of-Thought*, the investigation targets the loss of visual focus during complex spatial reasoning tasks. Using vision-centric benchmarks requiring precise spatial localization, the method enforces object-centric bounding box generation at intermediate reasoning steps, training the model via supervised fine-tuning to anchor each reasoning hop to explicit visual coordinates. The authors demonstrate that enforcing visual region-of-interest engagement significantly reduces visual hallucinations and stabilizes reasoning trajectories. The work remains focused on supervised dataset engineering and architectural fine-tuning, leaving open how unconstrained base models behave internally during long reasoning.

In *Circuit Tracing in Vision-Language Models: Understanding the Internal Mechanisms of Multimodal Thinking*, the analysis isolates the causal sub-circuits responsible for integrating visual and semantic features in Gemma-3-4B-it. By applying cross-layer transcoders and computing causal attribution graphs on ImageNet and Cauldron subsets, the authors observe that visual and textual representations remain in separate processing streams across early and middle layers, converging into shared semantic decision representations only in the final third of the network. The primary limitation lies in its computational expense, requiring approximately 60 hours on eight H100 GPUs for transcoder extraction, while remaining restricted to static inputs within a single architecture.

In *VIG: Visual Information Gain as a Reward Signal for Multimodal Chain-of-Thought Compression*, the research quantifies the empirical contribution of visual tokens across extended reasoning sequences. Evaluated on long-form multimodal reasoning traces across open-weight models, the intervention uses visual information gain as a reinforcement learning reward to compress reasoning paths. The authors establish that a substantial proportion of textual reasoning tokens contribute negligible visual information gain, functioning as unimodal language filler. The paper focuses on trace compression rather than isolating the causal drivers of visual token neglect.

In *Structural Sequential Visual CoT (SSV-CoT)*, the investigation addresses the token redundancy and reasoning instability caused by repeatedly injecting dense visual patch tokens into reasoning contexts. Evaluating open-weight models on multi-step visual reasoning tasks, the method abstracts the input image into a structured region embedding bank and queries it sequentially via a discrete action policy. The findings confirm that dense visual patch sequences degrade autoregressive stability during extended generation, whereas structured, selective access preserves reasoning coherence. The approach relies on custom discrete policy training, leaving standard attention mechanics unaddressed.

In *VisReason: Advancing Visual Chain-of-Thought Reasoning*, the authors address the lack of step-by-step spatially grounded supervisory data for complex reasoning. Using a large-scale suite of depth-augmented scenes, the authors train open MLLMs (LLaVA, InternVL, Qwen2-VL) on multi-round global-to-local reasoning paths. The results show that fine-grained visual step supervision prevents models from adopting language shortcuts on spatial reasoning tasks. As a benchmark and dataset contribution, the study does not explore internal representation mechanics in unprompted models.

### **Field B: Multimodal In-Context Learning and Task Induction**

Research in multimodal in-context learning investigates whether few-shot demonstrations allow models to infer cross-modal mapping rules or whether performance relies on surface-level textual heuristics.

In *Dissecting Multimodal In-Context Learning: Modality Asymmetries and Circuit Dynamics in Modern Transformers*, the study examines the internal attention circuits executing multimodal in-context learning. Utilizing controlled synthetic visual primitives, Omniglot, Mini-ImageNet, and validation runs on Qwen2.5-VL, the authors perform causal attention head knockouts. They identify induction-style circuits where specific attention heads copy visual label associations, while demonstrating a severe modality asymmetry: zeroing out the visual modality drops accuracy catastrophically, but textual attention heads can readily bypass visual induction. The experiments focus on isolated classification symbols rather than interleaved natural image-text reasoning.

In *Why Multimodal In-Context Learning Lags Behind? Unveiling the Inner Mechanisms and Bottlenecks*, the research investigates why multimodal few-shot scaling fails to achieve the empirical gains observed in text-only language models. Across tasks including Clock Math, Outlier Detection, Operator Induction, and OK-VQA on Qwen2.5-VL and Gemma-3, the authors probe intermediate activations across layers. They discover that while intermediate transformer layers successfully construct task-mapping vectors from demonstrations, the network fails to transfer this mapping to the query instance at the final prediction layer, identifying cross-modal misalignment as the primary operational bottleneck. The study concentrates on operator induction, leaving open whether similar transfer bottlenecks occur during open-ended multimodal generation.

In *TwinICL: Diagnosing Multimodal In-Context Learning through Paired Counterfactuals*, the authors investigate whether few-shot multimodal accuracy reflects true cross-modal rule induction or unimodal text shortcuts. Using paired counterfactual demonstration suites where visual demonstrations are permuted while textual labels remain fixed, the authors evaluate diverse open-weight MLLMs. The results demonstrate that models frequently maintain high task accuracy despite mismatched or scrambled demonstration images, confirming that few-shot performance is largely sustained by textual label priors. The paper is strictly behavioral and does not identify the internal attention heads responsible for ignoring visual context.

In *When Is a Task Vector Enough? An Empirical Theory of Implicit Multimodal ICL*, the authors examine whether multimodal demonstrations compress into static task vectors within attention heads. Formulating a theoretical and empirical framework across implicit multimodal ICL benchmarks, the intervention evaluates task-vector extraction across varying task complexities. The study demonstrates that while task vectors capture simple linear mappings, they fail when demonstrations require dynamic relational binding between visual tokens. The work provides a strong theoretical baseline but lacks validation on natural photographic scenes.

In *Multimodal Task Vectors Enable Many-Shot Multimodal In-Context Learning*, the authors investigate the context length bottleneck associated with processing numerous high-dimensional visual demonstrations. Evaluating interleaved models (OpenFlamingo, IDEFICS) across diverse vision-language tasks, the method extracts Multimodal Task Vectors (MTV) compressed inside attention heads and prepends them as virtual tokens. The findings confirm that task vectors scale with demonstration quantity and generalize to out-of-domain queries without consuming context length. The paper approaches the topic from an inference-efficiency perspective rather than auditing the failure modes of the underlying induction mechanism.

### **Field C: Mechanistic Compositional Grounding and Visual Binding**

Mechanistic investigations into compositional grounding seek to isolate how vision-language architectures associate distinct visual features (such as color or shape) with spatial entities and language referents.

In *Investigating Mechanisms for In-Context Vision Language Binding*, the authors evaluate how vision-language models bind visual tokens of objects to their corresponding textual entity references in context. Using a synthetic CLEVR-derived dataset requiring models to associate 3D objects with linguistic descriptions, the authors perform causal activation swapping on LLaVA-1.5-7B. The study confirms the existence of a visual Binding ID mechanism: the model assigns a shared, distinct latent identifier to an object's image tokens and its corresponding textual phrase in early-to-middle layers, enabling correct attribute association. Interchanging these Binding ID vectors via activation patching causally redirects the model's textual description of object attributes. However, the experiments are restricted to synthetic 3D shapes on plain backgrounds within a single model family.

In *Uncovering Grounding IDs: How External Cues Shape Multimodal Binding*, the authors analyze the internal mechanism through which external visual structures (such as grids, partition lines, and coordinate labels) eliminate binding errors in large vision-language models. Evaluating inference-time reasoning on Qwen2.5-VL-7B without fine-tuning, the authors construct synthetic multi-object scenes containing 15 unique objects sampled from 35 shape-color combinations, where each object is confined to a single 28x28 pixel patch. The analyses reveal that external visual partitions induce latent Grounding IDs that propagate across attention layers, strengthening within-partition cross-modal alignment and reducing the embedding modality gap. Causal activation swapping verifies that these Grounding IDs operate additively in representation space to direct object-attribute binding. The primary limitation is the reliance on synthetic scenes with patch-aligned objects, leaving unaddressed whether Grounding IDs emerge in unprompted, natural photographic environments.

In *Diagnosing Visual Ignorance in Vision-Language Models*, the research investigates the specific layers where language priors suppress counter-attitudinal visual attributes. Evaluating modern open-weight VLMs on diagnostic image-text pairs containing counter-commonsense visual attributes, the authors probe intermediate token representations. They find that visual attribute representations are accurately encoded in early decoder layers, but linguistic self-attention circuits progressively overwrite visual attribute features in late layers whenever the visual attribute exhibits low textual probability. The study provides diagnostic probing but lacks causal interventions to rescue suppressed visual attributes.

In *Visual Symbolic Mechanisms: Emergent Symbol Processing in Vision Language Models*, the authors investigate whether vision-language models implement intermediate discrete symbolic routing for compositional visual problem solving. Using geometric visual puzzles and multi-object reasoning scenes, the authors trace intermediate activations across attention heads. They identify a three-stage internal circuit consisting of entity ID retrieval, spatial selection, and compositional feature binding, proving that models emulate discrete symbolic pipelines internally. The tasks are synthetic and geometric, leaving natural-image validity unverified.

## **Antithesis Findings**

An adversarial assessment tests candidate hypotheses against published literature to determine whether apparent research opportunities are directly occupied, mechanistically occupied, or methodologically occupied.

### **Field A: Visual Evidence Utilization and Inference Scaling**

The candidate hypothesis posits that during extended multimodal reasoning traces, autoregressive vision-language models suffer from visual attention drift, wherein late reasoning steps cease attending to or utilizing visual token representations, causing language priors to dominate the final answer.

The closest published baselines are *Seeing or Knowing? Visual Context Sensitivity in Multimodal Large Language Models* and *VIG: Visual Information Gain as a Reward Signal for Multimodal Chain-of-Thought Compression*. Direct overlap is substantial: the claim that models ignore visual context in favor of language priors is directly occupied. The literature demonstrates that models encode coarse visual attributes into final-layer representations, yet fail to utilize them downstream during decision generation.

A terminology substitution scan reveals that researchers examine this phenomenon under alternative labels: visual context sensitivity, visual focus scheduling, visual information gain, and language prior override. The mechanism of late-layer visual evidence suppression is already documented by multiple independent groups.

What remains genuinely uncertain is whether visual token utilization degrades as a causal function of reasoning trace length when isolating length from token position. Existing literature evaluates static, single-step answers or treats reasoning traces in the aggregate. If an identical visual question is answered via 50 tokens versus 500 tokens of reasoning, does visual token utilization decay because of reasoning trace length, or is the observed decline an artifact of sequence position, softmax attention dilution across long contexts, or autoregressive attention sinks? No paper identified in this search provides a length-matched, position-controlled causal intervention.

Confidence in openness is rated as **Medium**. While the broad phenomenon is occupied, the controlled relationship between reasoning length and visual utilization remains unverified in existing literature.

### **Field B: Multimodal In-Context Learning and Task Induction**

The candidate hypothesis proposes that few-shot multimodal in-context learning is driven by cross-modal induction circuits that infer latent task mappings from interleaved image-text demonstrations and transfer those rules to query instances.

The closest published works are *Dissecting Multimodal In-Context Learning: Modality Asymmetries and Circuit Dynamics in Modern Transformers* and *Why Multimodal In-Context Learning Lags Behind? Unveiling the Inner Mechanisms and Bottlenecks*. Direct overlap is extensive: the mechanistic hypothesis is directly occupied. *Dissecting Multimodal ICL* explicitly isolates induction-style circuits using causal attention head ablations, establishing that induction heads copy label associations across multimodal sequences. Furthermore, *Why Multimodal ICL Lags Behind?* identifies the precise failure mode: intermediate layers construct the task mapping, but the model fails to transfer this representation to the final query token.

A terminology substitution scan reveals that studies examining multimodal prompt configuration, label permutation sensitivity, and task vector compression collectively confirm that few-shot multimodal performance often reduces to textual label bias or in-context semantic retrieval rather than genuine visual induction.

What remains genuinely uncertain is whether the failure to transfer task mappings in natural-image settings is caused by cross-modal feature misalignment in early projection layers or by attention competition from textual label tokens during the demonstration sequence. Existing mechanistic literature focuses on synthetic primitives (Omniglot, symbolic grids) or standard classification benchmarks (OK-VQA).

Confidence in openness is rated as **Low to Medium**. The core mechanics have been published at premier venues, and an empirical thesis here risks replicating existing circuit ablation findings unless restricted to natural image counterfactuals.

### **Field C: Mechanistic Compositional Grounding and Visual Binding**

The candidate hypothesis states that vision-language models fail at compositional grounding because they cannot bind object features to attribute representations in intermediate activations, a failure caused by linguistic priors overriding visual bindings.

The closest published baselines are *Investigating Mechanisms for In-Context Vision Language Binding* and *Uncovering Grounding IDs: How External Cues Shape Multimodal Binding*. Direct overlap is pronounced regarding the existence and characterization of binding identifiers. The literature establishes that VLMs assign distinct Binding IDs in activation space to connect visual tokens with textual descriptors, validated via activation swapping. Furthermore, researchers have proven that spatial partition cues induce linear Grounding IDs that causally govern object-attribute assignment in Qwen2.5-VL.

A terminology substitution scan indicates that whether compositional failure is an encoder defect or an LLM backbone defect is heavily explored: early vision tokens carry bound features, but cross-attention and language-prior interference disrupt binding retrieval in deep transformer layers.

What remains genuinely uncertain is whether latent Binding IDs and Grounding IDs operate as universal representations in transformer activations across natural photographic scenes. Grounding IDs and Binding IDs have been validated almost exclusively on synthetic, highly structured data (CLEVR primitives, grid partitions with isolated shape-color combinations). It is unknown whether latent binding identifiers exist as a general mechanism across natural, cluttered photographic images, or whether they represent artifacts emerging under geometric, high-contrast synthetic task constraints.

Confidence in openness is rated as **Medium**. While the mechanism is established on synthetic data, its cross-model generality and existence in natural visual distributions represent an open scientific question.

## **Dataset and Benchmark Audit**

The following audit evaluates prominent benchmarks across these subfields, assessing accessibility, data modality, shortcut risks, saturation levels, and suitability for causal mechanistic intervention.

| Dataset / Benchmark | Primary Task | Size / Splits | Data Modality | Leakage & Shortcut Risks | Saturation Status | Causal Intervention Suitability |
| :---- | :---- | :---- | :---- | :---- | :---- | :---- |
| WhatIfVis | Visual context vs. prior conflict QA | 3,108 samples; 5 categories | Natural images with counterfactual edits | High risk if exact-match formatting is used; requires probability scoring | Low; vanilla open models show severe failure | Exceptional; designed specifically with matched text/image controls |
| SugarCrepe | Compositional attribute / relation matching | \~3.5k image-text pairs | Real images; synthetically generated negative captions | Text-only leakage; negative captions contain unnatural linguistic artifacts | Moderate-high; frontier models achieve \>85% | Moderate; interventions limited to text caption manipulations |
| Winoground | Minimal pair compositional matching | 400 paired image-caption examples | Real photographs | Severe dataset noise; photographic ambiguities, tiny sample size | Saturated on text score; erratic on group score | Poor; insufficient scale for statistical activation probing |
| CLEVR | Synthetic multi-object compositional reasoning | 100k images; 850k questions | Synthetic 3D geometric shapes | Regular spatial layouts; severe linguistic template exploitation | Saturated (\>98% on modern VLMs) | High for synthetic probing; zero validity for natural photography |
| VisReason | Spatially grounded visual chain-of-thought | Large-scale multi-round visual traces | Depth-augmented real scenes | Annotation template artifacts; bounding-box coordinate memorization | Low; newly introduced | High; supports step-by-step intermediate trace inspection |
| OK-VQA | Knowledge-based visual question answering | 14,055 questions | Real COCO images | Unimodal language priors; high answer frequency biases | Moderately saturated | Poor for binding; moderate for demonstration ablation in ICL |
| CLBench-V | Multimodal in-context learning evaluation | Multi-task suites | Real & synthetic interleaved tasks | Interleaved formatting dependencies, prompt template sensitivity | Low to moderate | High; supports permutation of demonstration components |

Methodological inspection of these benchmarks reveals substantial trade-offs. WhatIfVis represents the most robust public asset for Field A because it provides matched counterfactual visual pairs where textual prompts can steer the model toward either the image context or the parametric prior, allowing researchers to isolate perceptual availability from post-perceptual utilization.

For Field B, general benchmarks like OK-VQA are problematic when used without controls because language models can exploit unigram frequencies to achieve high few-shot scores without inspecting images.

For Field C, while CLEVR provides clean symbolic annotations, its regularities fail to reflect real-world visual features. Conversely, Winoground contains severe photographic noise and is too compact for layer-wise linear probing. Consequently, an experimental study in Field C requires augmenting natural photographic pairs (e.g., from COCO or SugarCrepe) with counterfactual attribute swaps while controlling for text-only fluency.

## **Model and Compute Audit**

Conducting mechanistic multimodal research within academic compute constraints (such as Google Colab Pro or single NVIDIA A100/L4 GPU instances) mandates selecting open-weight architectures that support intermediate hidden-state extraction and forward hook registration without exceeding memory limits, as outlined below.

| Model Candidate | Parameter Scale | Open Weights | Vision Encoder & Projector Design | Inference Footprint (bfloat16) | Activation Extraction Feasibility | Implementation Complexity |
| :---- | :---- | :---- | :---- | :---- | :---- | :---- |
| Qwen2.5-VL-3B-Instruct | 3.1 Billion | Yes; Apache 2.0 | Dynamic resolution ViT; spatial merge projector into Qwen2.5 backbone | \~7 GB VRAM | High; native Hugging Face support for PyTorch forward hooks | Low-Medium; dynamic resolution requires careful token indexing |
| Qwen2.5-VL-7B-Instruct | 7.6 Billion | Yes; Apache 2.0 | Dynamic resolution ViT; spatial merge projector | \~16 GB VRAM | High; fits single 24GB/40GB GPU for inference and linear probing | Low-Medium; memory management critical during activation caching |
| Gemma-3-4B-it | 4.3 Billion | Yes; Gemma Terms | SigLIP vision backbone; concatenated multimodal tokens | \~9 GB VRAM | High; transformer blocks cleanly separated, ideal for residual patching | Low; highly standardized architectural implementation |
| SmolVLM-Instruct | 2.2 Billion | Yes; Apache 2.0 | Compact SigLIP encoder; lightweight projection into SmolLM backbone | \~5 GB VRAM | Exceptional; minimal memory overhead during activation extraction | Very Low; ideal for rapid prototyping and sanity controls |
| LLaVA-v1.6-7B (NeXT) | 7.2 Billion | Yes; Apache 2.0 | CLIP ViT-L/14; two-layer MLP connector into Vicuna/Mistral | \~15 GB VRAM | High; widely supported across mechanistic interpretability toolkits | Low; standard baseline across prior mechanistic binding work |

An evaluation of computational tiers establishes realistic boundaries for academic experimentation. Tier 1 (pure inference) and Tier 2 (activation extraction and caching) are fully viable on a single 24GB or 40GB GPU for models up to 7B parameters. Dynamic token counts in Qwen2.5-VL require tracking visual token coordinate slices when caching representations. Tier 3 (linear probing on frozen layer representations) requires training logistic regressors or linear probes on cached activations, which consumes negligible GPU compute and runs comfortably in system memory. Tier 4 (parameter-efficient fine-tuning via LoRA/QLoRA) is feasible on 24GB–40GB GPUs for learning steering vectors, though it introduces optimization hyperparameters that can complicate purely mechanistic inquiries.

Tiers 5 and 6 (full fine-tuning and large-scale circuit tracing via transcoders or sparse autoencoders) are impractical for a single-GPU thesis. As documented in recent literature, training transcoders across all layers of Gemma-3-4B requires multi-node H100 clusters, consuming approximately 60 GPU hours across eight H100s. Full-model circuit discovery must therefore be avoided in favor of targeted causal activation swapping on selected intermediate layers.

## **Shortcut and Confound Audit**

To prevent experimental artifacts from being mistaken for novel mechanisms, candidate phenomena must be paired with controls capable of falsifying the hypothesized effect, as mapped in the table below.

| Candidate Phenomenon | Hypothesized Mechanism | Alternative / Confound Explanation | Mandatory Experimental Control | | :--- | :--- | :--- | :--- | | Visual attention degradation in long CoT | Visual evidence is progressively forgotten as textual reasoning unfolds | **Sequence Position & Attention Normalization:** Later tokens attend less to early tokens due to softmax denominator expansion and positional decay | **Compute-Matched Text Padding:** Replace reasoning steps with semantically irrelevant text tokens (e.g., repeated characters or neutral prose) of identical length. If visual attention decays identically, the effect is a sequence length artifact, not a reasoning failure. | | Demonstration gains in multimodal ICL | Model induces a cross-modal input-output mapping rule | **Label Distribution & Lexical Bias:** Few-shot demonstrations merely provide valid answer token formats and prime label frequencies | **Label Permutation:** Randomly swap label assignments in demonstrations (e.g., systematically mapping class A to label B). If performance remains unchanged, the model is executing zero-shot recognition with format priming, not task induction. | | Demonstration gains in multimodal ICL | Model learns from visual-text pairings | **Unimodal Textual Driving:** Demonstration images are ignored; textual task descriptions drive performance | **Modality Ablation:** Black out or noise-scramble demonstration images while preserving textual templates. If accuracy matches full multimodal ICL, visual induction is absent. | | Failure on compositional attribute binding | Model lacks intermediate binding representations between objects and attributes | **Unigram Frequency Prior:** Training data pairs the object heavily with a canonical attribute (e.g., "yellow banana") | **Attribute Counterbalancing:** Test minimal pairs where attributes are strictly swapped across identical visual objects under symmetric language prompts. | | Failure on compositional attribute binding | Representation level binding failure | **Spatial / Saliency Dominance:** Model attends exclusively to the larger or center-most visual object | **Spatial Position Inversion:** Mirror or permute object coordinates across quadrants to confirm binding failure is invariant to layout geometry. |

Understanding the mechanics of these alternative explanations illustrates why uncalibrated experiments fail. In autoregressive transformers, as generated sequence length increases, the cumulative attention budget across early tokens decays due to the expanding denominator in softmax normalization. Furthermore, causal masking and rotary positional embeddings (RoPE) naturally introduce a decay in attention weight over larger token distances. Consequently, an apparent decrease in attention toward visual tokens during extended chain-of-thought may simply reflect the mathematics of the attention operation over expanding contexts rather than any cognitive degradation of visual grounding.

Similarly, multimodal in-context learning often appears effective only because demonstration examples provide structural formatting that reduces output perplexity. Unless models are subjected to label permutation (which breaks the mapping between visual semantic classes and textual tokens), researchers risk attributing performance gains to in-context rule induction when the model is merely executing zero-shot classification under improved formatting constraints.

## **Negative-Result Analysis**

A defensible scientific thesis must yield informative findings even if the core hypothesis fails. The table below formalizes the scientific utility of both positive (H\_1) and negative (H\_0) outcomes across the investigated questions.

| Candidate Question | Hypothesized Effect (H\_1) | Null Hypothesis (H\_0) | Scientific Utility of Negative Finding (H\_0) | Research Risk Profile |
| :---- | :---- | :---- | :---- | :---- |
| **Q1:** Dynamic visual utilization vs. sequence position confounds | Visual token utilization causally decreases as reasoning length increases, beyond sequence-length effects. | Visual token utilization does not degrade with reasoning length; decay is an artifact of positional attenuation. | **High:** Refutes the visual attention drift narrative; proves test-time compute does not degrade visual grounding, redirecting focus to decoding heads. | Low; both outcomes resolve an active debate on test-time scaling. |
| **Q2:** Generality of latent binding IDs in natural scenes | Latent Binding IDs operate as universal representations binding attributes to objects in natural images. | Latent Binding IDs collapse in natural photographic scenes, emerging only under rigid synthetic constraints. | **High:** Exposes synthetic mechanistic interpretability as non-generalizable, constraining claims regarding visual binding representations. | Medium; requires careful natural image dataset curation. |
| **Q3:** Task-mapping transfer in natural multimodal ICL | Intermediate layers construct transferable cross-modal task mappings from natural image demonstrations. | Natural multimodal ICL relies on zero-shot visual features and text label priming; no task mapping is formed. | **High:** Demonstrates that multimodal ICL is an in-context text calibration process rather than genuine few-shot vision learning. | Low; cleanly falsifiable via head knockout and label permutation. |

The negative results articulated above possess substantial scientific value because they serve a corrective function within the literature. Demonstrating that visual attention drift is an artifact of positional encoding would prevent the development of unnecessary architectural patches designed to fix a non-existent degradation. Similarly, demonstrating that Binding IDs fail to replicate in natural photographic scenes would establish empirical boundary conditions on synthetic mechanistic interpretability, providing critical guidance for future vision-language architecture design.

## **Closest-Work Matrix**

The matrix below compares potential candidate investigations directly against the closest published baselines to establish exact points of departure.

| Proposed Mechanistic Inquiry | Closest Published Baseline | What Baseline Already Tests | What Baseline Does NOT Establish | Degree of Overlap | Remaining Scientific Gap |
| :---- | :---- | :---- | :---- | :---- | :---- |
| Dynamic decay of visual evidence utilization as a causal function of CoT length | *Seeing or Knowing?* (Li et al., 2026\) | Probes visual feature availability in final layers on single-turn VQA; identifies static vision-vs-prior knob | Does not test multi-step reasoning traces or vary reasoning length dynamically | Mechanistic overlap | Isolating whether extended textual CoT actively suppresses decodability of visual tokens. |
| Visual token relevance across reasoning steps | *VIG: Visual Information Gain* (2026) | Quantifies visual information gain across tokens to compress reasoning traces via RL | Does not provide causal activation interventions; does not isolate length from position | High methodological overlap | Establishing whether visual information loss is causal or an attention measurement artifact. |
| Circuit-level validation of multimodal induction heads | *Dissecting Multimodal ICL* (ICML 2026\) | Identifies induction heads and executes head knockout on synthetic symbol grids and Omniglot | Does not evaluate natural image tasks or interleaved real-world visual demonstrations | Direct overlap on synthetic setups | Testing whether natural-image MLLM few-shot success utilizes the same induction circuits. |
| Decoupling task-mapping construction from transfer | *Why Multimodal ICL Lags Behind?* (2026) | Measures task-vector formation in intermediate layers across operator induction tasks | Does not test whether intermediate task mappings can be causally steered or patched | Direct overlap on diagnostic probing | Determining if cross-modal task transfer can be recovered via activation patching. |
| Latent binding IDs in visual grounding | *Uncovering Grounding IDs* (Hasani et al., ICML 2026\) | Causal activation swapping of partition IDs on synthetic 15-object geometric grids | Does not test complex natural scenes, occlusions, or un-partitioned natural images | Direct overlap on synthetic grids | Verifying if latent binding identifiers exist in open-weight models without external visual grids. |
| Object-attribute binding mechanisms in context | *Investigating Mechanisms for Binding* (Saravanan et al., CVPRW 2025\) | Probes and swaps binding IDs for 3D synthetic shapes in LLaVA-1.5 | Does not evaluate modern dynamic-resolution models (Qwen2.5-VL) or natural photography | Direct overlap on synthetic binding | Determining whether binding IDs generalize across modern architectures and natural images. |

## **Research Crowding Map**

The multimodal literature is categorized into empirical density tiers based on verified publications from 2025–2026:

### **Heavily Occupied**

Research areas in this tier are characterized by numerous competing papers addressing identical mechanisms using standard benchmarks, offering minimal opportunity for a novel thesis contribution:

> * Parametric language prior override and visual neglect in static, single-turn question answering (heavily documented across WhatIfVis, HallusionBench, and related benchmarks).  
> * Behavioral demonstration order sensitivity, recency bias, and label permutation degradation in multimodal in-context learning.  
> * Supervised region-grounded reasoning data generation pipelines (exemplified by Argus and VisReason).  
> * Standard benchmark-level compositional evaluation on Winoground, SugarCrepe, and CLEVR without internal representation interventions.

### **Moderately Occupied**

These areas possess an established body of foundational work with emerging mechanistic frameworks, though investigations remain restricted to specific model families or stylized setups:

> * Mechanistic isolation of induction heads in small, controlled synthetic transformers on classification tasks (ICML 2026).  
> * Identification and causal swapping of latent Binding IDs and Grounding IDs in synthetic geometric grid environments (CVPRW 2025, ICML 2026).  
> * Static cross-layer circuit tracing using sparse autoencoders or transcoders on single models (such as Gemma-3-4B-it).  
> * Visual information gain metrics for pruning and compressing multimodal reasoning traces (VIG).

### **Partially Occupied and Emerging Gaps**

These domains feature identifiable, unanswered scientific questions where existing literature provides necessary diagnostics but lacks conclusive causal validation:

> * Disentangling the causal degradation of visual token utilization from sequence-length attenuation and positional artifacts in extended reasoning traces.  
> * Assessing the cross-model generality and existence of latent binding identifiers in natural photographic scenes containing continuous textures and complex backgrounds.  
> * Causal activation patching to recover task-mapping transfer failures during natural-image multimodal in-context learning.

### **Sparse or Uncertain**

Areas where empirical literature is scarce and foundational methodologies remain unstandardized:

> * A unified, architecture-independent mechanistic theory of multimodal test-time scaling across heterogeneous vision backbones.

## **Candidate Question Inventory**

The following candidate questions emerge directly from the literature gaps identified in the audit.

| Candidate Question | Investigated Mechanism | Closest Prior Work | Current Gap Status | Primary Confound to Control | Negative Result Value (H\_0) | Phase 2 Feasibility |
| :---- | :---- | :---- | :---- | :---- | :---- | :---- |
| **Q1:** Does visual evidence utilization degrade as a causal function of reasoning trace length, or is it an artifact of positional attenuation? | Post-perceptual visual evidence decay vs. positional encoding bias | Li et al. (2026); VIG (2026) | Partially occupied; unverified under length-matched controls | Sequence length, softmax normalization, text padding tokens | High; refutes visual attention drift narrative | **High** (Tier 2/3 compute; WhatIfVis data) |
| **Q2:** Do latent Binding IDs identified in synthetic scenes generalize to natural photographic object-attribute compositions? | Latent identifier routing across visual and textual tokens | Saravanan et al. (2025); Hasani et al. (2026) | Weakly explored on natural images; occupied on synthetic | Visual clutter, background texture, unaligned patch boundaries | High; demonstrates that binding IDs are synthetic artifacts | **High** (Tier 2/3 compute; Qwen2.5-VL / Gemma-3) |
| **Q3:** Can intermediate task-mapping transfer failures in multimodal ICL be causally rescued via activation steering? | Task-mapping construction vs. transfer decoupling | Why Multimodal ICL Lags Behind? (2026) | Weakly explored intervention; occupied diagnostic | Semantic label similarity, in-context hallucination | High; proves transfer bottleneck is structural | **Medium** (Requires precise layer localization) |
| **Q4:** Does repeated visual token re-injection causally improve fine-grained attribute deduction in open MLLMs? | Multi-round visual evidence retrieval vs. compute inflation | AIM-CoT (2025); SSV-CoT (2026) | Partially occupied methodologically | Total parameter FLOPs; language model reasoning capacity | Medium; shows re-injection provides marginal utility | **Medium** (Engineering overhead for interleaved inputs) |
| **Q5:** Do multimodal induction circuits operate over natural image tokens or bypass them entirely in favor of text heads? | Induction head circuit dynamics across modalities | Dissecting Multimodal ICL (ICML 2026\) | Partially occupied on synthetic data | Visual pretraining quality, label distribution priors | High; proves multimodal ICL is largely a text shortcut | *Medium-Low* (Circuit tracing requires head-level patching) |

## **Anti-Anchoring Check**

An anti-anchoring audit of adjacent 2025–2026 multimodal research reveals three alternative subfields outside candidate areas A, B, and C that offer clean causality, lower compute requirements, and leakage-resistant evaluation protocols:

### **1\. Representation Steering for Decoding-Time Hallucination Mitigation**

Instead of updating vision encoders or fine-tuning language backbones, researchers extract one-dimensional grounding or truthfulness vectors from intermediate transformer activations and apply linear steering during autoregressive generation. This direction provides high experimental control on a single 24GB GPU, utilizing established public datasets (WhatIfVis, HallusionBench) without requiring complex circuit extraction.

### **2\. Cross-Modal Confidence Calibration under Perceptual Conflict**

This subfield evaluates whether an MLLM's internal token output entropy or semantic logit uncertainty reflects true visual grounding when textual prompts contradict image evidence. Requiring strictly pure inference and logit extraction (Tier 1 compute), this direction offers high reproducibility and direct quantitative metrics without needing internal circuit interventions.

### **3\. Dynamic Visual Token Pruning and Information Preservation in Middle Layers**

Middle-to-late transformer layers often treat the vast majority of visual tokens as redundant. Researchers analyze whether pruning non-attended visual tokens mid-network alters reasoning faithfulness or functions purely as a compression mechanism. This subfield provides a concrete computer systems and efficiency focus, evaluated through quantitative latency, FLOPs, and accuracy trade-offs implemented via forward hooks on small open-weight models.

## **Evidence Table**

The methodological audit trail supporting the primary scientific findings of this report is detailed below.

| Claim | Supporting Evidence / Primary Source | Evidence Type | Confidence Level | Limitations & Nuances |
| :---- | :---- | :---- | :---- | :---- |
| Visual evidence is preserved in final-layer image tokens but goes unused due to parametric prior override. | Li et al. (2026), *Seeing or Knowing?* (arXiv:2607.26326v2) | Direct paper evidence | High | Probed primarily on coarse attributes (color, size, count) on WhatIfVis; fine-grained textures unverified. |
| Latent Binding IDs causally bind visual object tokens to textual references in activation space. | Saravanan et al. (2025), *Investigating Mechanisms for Binding* (arXiv:2505.22200v1) | Direct paper evidence | High | Validated strictly on synthetic 3D shape objects from CLEVR variants; cross-architecture testing limited. |
| External partition cues induce Grounding IDs that resolve binding errors via additive latent vectors. | Hasani et al. (2025/2026), *Uncovering Grounding IDs* (arXiv:2509.24072v4) | Direct paper evidence | High | Objects were synthetic and constrained to single 28x28 pixel patches; does not test natural photography. |
| Multimodal in-context learning uses specialized induction heads that exhibit severe modality asymmetry. | *Dissecting Multimodal In-Context Learning* (ICML 2026, arXiv:2601.207\[span\_237\](start\_span)\[span\_237\](end\_span)\[span\_242\](start\_span)\[span\_242\](end\_span)96v2) | Direct paper evidence | High | Evaluated predominantly on synthetic symbol datasets and Omniglot; natural image transfer unverified. |
| Multimodal ICL constructs task mappings at intermediate layers but fails to transfer them to query tokens. | *Why Multimodal In-Context Learning Lags Behind?* (arXiv:2604.13403v1) | Direct paper evidence | High | Tested across four structured tasks (Clock Math, Outliers, etc.); generative reasoning unexplored. |
| Full transcoder training and circuit tracing is computationally prohibitive for single-GPU academic setups. | *Circuit Tracing in Vision-Language Models* (arXiv:2602.20330v1, Page 6\) | Direct paper evidence | High | Gemma-3-4B required \~60 hours on 8xH100s; inference and probing remain feasible on single GPUs. |
| Extended textual CoT fails to monotonically scale visual grounding. | *Look Light, Think Heavy* (arXiv:2606.22565) | Direct paper evidence | High | Behavioral evaluation across standard benchmarks; does not perform internal layer patching. |
| Causal relationship between reasoning length and visual utilization remains untested under length controls. | Exhaustive literature search across 2025–2026 arXiv, OpenReview, CVPR, ICML | Gap falsification / NOT FOUND | Medium | Absence of matching papers indicates an unverified gap, not proof of absolute novelty. |

## **Phase 1 Conclusion**

### **Field A**

> * **Status:** Crowded in broad form, but containing a narrow, defensible causal research gap.  
> * **Why:** Broad assertions that vision-language models suffer from visual neglect, language prior dominance, or static visual context insensitivity are directly occupied by published 2025–2026 literature. However, the dynamic utilization of visual tokens across extended reasoning sequences remains confounded by sequence length and positional attenuation.  
> * **Most important occupied area:** The diagnostic separation of visual perception from visual utilization, and the extraction of static steering vectors to modulate vision-versus-prior trade-offs in single-turn question answering.  
> * **Most interesting unresolved uncertainty:** Whether visual evidence utilization degrades as a direct causal consequence of multi-step reasoning trace length, or whether the observed decay is an experimental artifact of sequence position and softmax attention dilution.  
> * **Phase 2:** YES

### **Field B**

> * **Status:** Heavily crowded and mechanistically occupied.  
> * **Why:** Recent ICML 2026 and preprint literature has mapped multimodal induction circuits, modality asymmetries, task-vector compression, and the decoupling of task-mapping construction from query transfer. Proposing an exploratory investigation into multimodal induction risks direct collision with existing mechanistic papers.  
> * **Most important occupied area:** Causal head ablation demonstrating the existence of multimodal induction circuits in synthetic architectures, and intermediate probing revealing task-mapping construction bottlenecks.  
> * **Most interesting unresolved uncertainty:** Whether few-shot demonstration gains in natural-image MLLM reasoning represent genuine cross-modal rule induction or reduce entirely to unimodal text-label priming paired with zero-shot image classification.  
> * **Phase 2:** UNCERTAIN

### **Field C**

> * **Status:** Moderately crowded on synthetic benchmarks; open and promising regarding cross-model and natural-scene generalization.  
> * **Why:** Foundational mechanistic work has successfully isolated Binding IDs and Grounding IDs via causal activation swapping. However, the empirical literature is bottlenecked on synthetic geometric scenes (CLEVR primitives and structured 28x28 visual grids). Establishing whether these binding mechanisms operate across natural photographic images represents an open scientific frontier.  
> * **Most important occupied area:** Causal activation swapping of latent Binding IDs and externally induced Grounding IDs in synthetic multi-object scenes.  
> * **Most interesting unresolved uncertainty:** Whether latent binding identifiers are fundamental, architecture-independent transformer mechanisms that scale to natural visual distributions, or brittle artifacts arising exclusively from stylized, high-contrast synthetic primitives.  
> * **Phase 2:** YES

## **Phase-2 Shortlist**

### **Question 1**

Does visual evidence utilization degrade as a causal function of multimodal reasoning trace length after strictly controlling for sequence position, context length, and attention normalization?

The question survived Phase 1 because while broad visual neglect is heavily occupied, the literature review failed to locate any study that causally decouples reasoning trace length from transformer sequence-position confounds via length-matched text padding. The closest published baselines are *Seeing or Knowing? Visual Context Sensitivity in Multimodal Large Language Models* and *VIG: Visual Information Gain as a Reward Signal for Multimodal Chain-of-Thought Compression*.

The primary unresolved issue is determining whether visual token representations suffer from actual post-perceptual utilization decay as intermediate reasoning expands, or if apparent decay is an artifact of attention distribution over longer sequences. The main experimental confounds to control are autoregressive attention sinks, token position indices, and sequence-length dilution in softmax denominators. The negative result is scientifically valuable because proving \[span\_99\](start\_span)\[span\_99\](end\_span)H\_0 demonstrates that the visual attention drift narrative is an experimental illusion caused by positional confounds, redirecting the multimodal reasoning community toward output decoding heads rather than intermediate visual attention mechanisms.

### **Question 2**

Are latent visual Binding IDs universal, architecture-independent mechanisms in vision-language models, or are they representational artifacts of synthetic geometric scenes?

The question survived Phase 1 because Binding IDs and Grounding IDs have been mechanistically verified and causally swapped almost exclusively on stylized synthetic primitives (CLEVR and 28x28 grid patches). Systematic cross-architecture validation on natural photographic scenes remains absent. The closest known baselines are *Investigating Mechanisms for In-Context Vision Language Binding* and *Uncovering Grounding IDs: How External Cues Shape Multimodal Binding*.

The primary unresolved issue is whether linear activation patching can swap object-attribute bindings in realistic, cluttered natural images containing continuous textures and complex backgrounds. The main experimental confounds to control are visual clutter, background co-occurrence priors, object saliency imbalances, and patch boundary splitting. The negative result is scientifically valuable because proving H\_0 establishes that recent mechanistic binding discoveries are toy-domain artifacts that cannot explain real-world vision-language compositionality, exposing fundamental limitations in synthetic mechanistic interpretability methodologies.

#### **Works cited**

1\. AIM-CoT: Active Information-driven Multimodal Chain-of-Thought for, https://arxiv.org/html/2509.25699 2\. Seeing or Knowing? Visual Context Sensitivity in Multimodal Large, https://arxiv.org/abs/2607.26326 3\. Yixuan Li \- Underline.io, https://underline.io/speakers/219335-yixuan-li 4\. Uncovering Grounding IDs: How External Cues Shape Multi-Modal, https://openreview.net/pdf/724e8cc7d5e266d83c9e96e20f3149303863321a.pdf 5\. Investigating Mechanisms for In-Context Vision Language Binding, https://arxiv.org/abs/2505.22200 6\. Mechanistic Interpretability for Vision \- CVF Open Access, https://openaccess.thecvf.com/CVPR2025\_workshops/MIV 7\. Uncovering Grounding IDs: How External Cues Shape Multimodal, https://arxiv.org/abs/2509.24072 8\. Argus: Vision-Centric Reasoning with Grounded Chain-of-Thought, https://arxiv.org/abs/2505.23766 9\. Structured Sequential Visual Chain-of-Thought Reasoning \- arXiv, https://arxiv.org/html/2603.26737v2 10\. A Large-Scale Dataset for Visual Chain-of-Thought Reasoning \- arXiv, https://arxiv.org/html/2511.17731v2 11\. Multimodal Task Vectors Enable Many-Shot Multimodal In-Context, https://arxiv.org/html/2406.15334v1 12\. \[2406.15334\] Multimodal Task Vectors Enable Many-Shot ... \- arXiv, https://arxiv.org/abs/2406.15334 13\. GitHub \- itsqyh/Awesome-LMMs-Mechanistic-Interpretability, https://github.com/itsqyh/Awesome-LMMs-Mechanistic-Interpretability