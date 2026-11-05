
# Chat Transcript: VLM MLLM Antithesis Scan

## User

(File attachment: text/plain)

VLM/MLLM Subfield Landscape & Antithesis Scan

## Aurelle

> **Searched Papers**
> 4 searches · 80 papers · DRT: Dense Reasoning Trace for Efficient and Grounded Multimodal Reasoning · Beyond Generation and Accuracy: Diagnosing and Enhancing Visual Chain-of-Thought for Geometry Problem Solving · VIG: Visual Information Gain as a Reward Signal for Multimodal Chain-of-Thought Compression · SinkPruner: Sink-Free Visual Token Pruning for Multimodal Large Language Models · GLaQ: Grounding Latent Queries in Visual Evidence for Multimodal Reasoning · Visual Saliency Steering Distillation for Multimodal Chain-of-Thought Reasoning · Mixture-of-Thought-Tokens: Unifying Perception and Reasoning for Free-form Multimodal Grounding · LEMUR: Latent Entropy-aware Multimodal Unlearning via Visual-anchored Reasoning Redirection · A Pathway to General-Purpose Scientific AI: Multimodal Comprehension of Scientific Images · Multimodal Chain-of-Thought Reasoning: A Comprehensive Survey · Circuit Tracing in Vision-Language Models: Understanding the Internal Mechanisms of Multimodal Thinking · A Survey on Multimodal Large Language Models · Vision Language Models: A Survey of 26K Papers · Speaking of Language: Reflections on Metalanguage Research in NLP · Explain Before You Answer: A Survey on Compositional Visual Reasoning · Reinforced MLLM: A Survey on RL-Based Reasoning in Multimodal Large  Language Models · TwinICL: Diagnosing Multimodal In-Context Learning through Paired Counterfactuals · V-ICAL Bench: Evaluating Video In-Context Learning for Multimodal Agents in Interactive Environments · Beyond Surface Imitation: Contrastive Modeling for Reasoning Path Alignment in Multimodal In-Context Learning · Understanding In-Context Multimodal Jailbreaks via Posterior Reweighting · MAG: MAnifold Guided Semi-Supervised Multi-modal In-Context Learning · When Is a Task Vector Enough? An Empirical Theory of Implicit Multimodal ICL · ZOMP: Zeroth-Order Multi-Modal Prompt Tuning for Vision-Language Models · In-Context Learning for Wound Classification with Small Multimodal Language Models · Why Multimodal In-Context Learning Lags Behind? Unveiling the Inner Mechanisms and Bottlenecks · Towards LLM-Centric Multimodal Fusion: A Survey on Integration  Strategies and Techniques · UniICL: Systematizing Unified Multimodal In-context Learning through a Capability-Oriented Taxonomy · Exploring Embodied Multimodal Large Models: Development, Datasets, and  Future Directions

> **Exploring research tools**
>
> Oh no, I might have some doubts about the tool regarding future papers, as they could likely be fabricated. The current date is September 2026, and I'm trying to figure out how to find the remaining information. We’ve used two searches already, but they didn’t yield results. I think I could potentially use a direct query for known titles and search the web with specific terminology. It looks like I might need to make a single search call for better results.

> **Searched Sources**
> 1 search · 10 sources · Investigating Mechanisms for In-Context Vision Language Binding · Pith Review · Towards Understanding Visual Grounding in Vision-Language Models · A systematic review of vision language models: Comprehensive analysis of architectures, applications, datasets and challenges towards robust multimodal intelligence - ScienceDirect · Diagnosing Visual Ignorance in Vision-Language Models · Understanding and improving vision-language models through the lens of the binding problem · [Paper Note] Visual Symbolic Mechanisms: Emergent Symbol Processing in Vision Language Models · In-Context Vision Language Binding · Investigating Mechanisms for In-Context Vision Language Binding
> **Read 4 papers**
> Circuit Tracing in Vision-Language Models: Understanding the Internal Mechanisms of Multimodal Thinking · Dissecting Multimodal In-Context Learning: Modality Asymmetries and Circuit Dynamics in modern Transformers · Why Multimodal In-Context Learning Lags Behind? Unveiling the Inner Mechanisms and Bottlenecks · Seeing or Knowing? Visual Context Sensitivity in Multimodal Large Language Models

# Phase 1 — VLM/MLLM Subfield Landscape & Antithesis Scan

## 1. Executive Finding

The three proposed labels do not have equal scientific status. **Field B is already a recognizable research area**: multimodal in-context learning, or more precisely, *cross-modal task induction and multimodal context learning*. **Field C is also recognizable**, but “visual representation binding” combines several distinct problems—attribute binding, compositional generalization, visual grounding, and mechanistic interpretability—that should not be treated as one unified field. **Field A is the least stable label**: “multimodal chain-of-thought dynamics” and “visual attention drift” describe a cluster of active questions inside the broader areas of multimodal reasoning, visual evidence utilization, modality reliance, and inference-time/test-time scaling.

The strongest antithesis result is that several apparently open Field A hypotheses are already directly or mechanistically occupied. Recent work studies visual-context sensitivity, visual-versus-prior conflicts, visual information preservation, multimodal test-time scaling, visual latent reasoning, and circuit-level multimodal reasoning. In particular, the hypothesis that a model may preserve visual information internally but fail to use it reliably is no longer merely speculative. A 2026 study explicitly separates *perception failure* from *visual-context utilization failure* and reports that coarse visual evidence remains decodable in final-layer image tokens while model behavior remains unstable. [Main finding](https://www.alphaxiv.org/abs/2607.26326v2?page=3)

The most important occupied subproblem in Field B is the distinction between genuine multimodal induction and textual or semantic shortcuts. Recent work finds that multimodal ICL can construct task mappings from demonstrations but fail to transfer them reliably to query-time reasoning. The studied mechanism is therefore already close to the proposed questions about demonstration effects, visual utilization, and cross-modal transfer. [Mechanistic bottleneck](https://www.alphaxiv.org/abs/2604.13403v1?page=2) Another 2026 study identifies induction-style label-copying circuits and causally tests them with head ablations, substantially occupying the “multimodal induction mechanism” hypothesis. [Induction circuits](https://www.alphaxiv.org/abs/2601.20796v2?page=8)

Field C survives the antithesis scan somewhat better, but only after narrowing the question. Attribute binding and visual grounding are not new. Recent work directly investigates mechanisms for in-context vision-language binding, while a 2026 mechanistic paper reports a causal circuit-tracing framework for visual and semantic features. The remaining uncertainty is less “does binding exist?” and more “how reliably do identified binding mechanisms generalize across models, image layouts, attributes, relations, and natural images?” The current literature is rich in demonstrations and case studies but weaker in systematic cross-model causal tests.

The three fields also differ in methodological maturity. Field B has relatively clear behavioral controls: modality ablation, label permutation, matched text/image tasks, demonstration ordering, and task-mapping transfer tests. Field A has strong behavioral and representational diagnostics, but attention-based explanations are vulnerable to positional and normalization confounds. Field C has the most scientifically interesting mechanistic possibilities, but causal probing and circuit extraction are expensive and often model-specific.

For a BSc-level project using Colab Pro or moderate cloud GPUs, none of the fields supports full mechanistic interpretability of frontier MLLMs. A feasible project would need to use small open models, inference-time interventions, carefully controlled synthetic or counterfactual data, and a limited number of layers or representations. Full transcoder-based circuit tracing is not a realistic default: one recent implementation used Gemma-3-4B but reported approximately 60 hours on eight H100 GPUs for transcoder training and around 20 minutes per attribution graph on one H100. [Compute cost](https://www.alphaxiv.org/abs/2602.20330v1?page=6)

The areas that should be deprioritized immediately are broad versions of “visual attention decreases during long CoT,” “multimodal ICL is sensitive to demonstrations,” and “VLMs have language bias.” Each is either directly occupied or too underspecified to support a defensible thesis. Narrower variants involving matched controls, causal interventions, cross-model transfer, or separating perception from utilization remain worth investigating.

The preliminary conclusion is therefore not that one field has won. **Field A is crowded and terminology-fragmented; Field B is established and mechanistically occupied, with narrower gaps; Field C is moderately crowded but still has the clearest room for a carefully bounded mechanistic investigation.** This is a Phase-2 prioritization signal, not a final thesis selection.

## 2. Landscape Comparison

| Dimension                        | Field A                                                                                                                                           | Field B                                                                                                    | Field C                                                                                                                   |
| -------------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------- | ---------------------------------------------------------------------------------------------------------- | ------------------------------------------------------------------------------------------------------------------------- |
| Scientific identity              | Visual evidence utilization and multimodal inference-time reasoning                                                                               | Multimodal in-context learning and cross-modal task induction                                              | Mechanistic compositional grounding and visual binding in VLMs                                                            |
| Active 2025–26 research         | Visual-context sensitivity, visual latent reasoning, adaptive visual computation, multimodal test-time scaling, reasoning traces                  | Task mapping, modality asymmetry, visual-context underuse, induction circuits, demonstration configuration | Attribute binding, visual grounding, binding IDs, layer-wise information flow, language-prior interference                |
| Main mechanisms                  | Visual evidence preservation, visual-versus-prior competition, repeated visual inspection, visual token routing, test-time computation allocation | Task mapping construction, task mapping transfer, induction-style label copying, cross-modal alignment     | Object-attribute binding, relation binding, compositional feature retrieval, modality-specific and shared representations |
| Major benchmarks                 | MMMU, MathVista, MathVista-like reasoning suites, HallusionBench, WhatIfVis, visual reasoning and grounding benchmarks                            | Open-MI/TrueMICL-style tasks, OK-VQA, VQA, synthetic outlier/operator tasks, CLBench-V                     | Winoground, SugarCrepe, CLEVR, GQA, ARO-style datasets, WhatIfVis, synthetic binding tasks                                |
| Typical models                   | Qwen2.5-VL, Gemma multimodal models, LLaVA-family models, unified multimodal reasoning models                                                     | Qwen2.5-VL, Gemma-3, IDEFICS, small controlled transformers                                                | Gemma-3, Qwen-VL models, CLIP-like encoders, LLaVA-family models                                                          |
| Main methodology                 | Behavioral evaluation, activation/attention analysis, patching, inference-time scaling, visual ablations                                          | Matched task formulations, demonstration permutation, modality ablation, attention analysis, head knockout | Counterfactual image swaps, probing, activation patching, feature steering, circuit tracing                               |
| Literature crowding              | Crowded in broad form; very crowded for generic visual neglect/language bias                                                                      | Crowded and rapidly expanding                                                                              | Moderately crowded; binding mechanisms are emerging but fragmented                                                        |
| Mechanistic maturity             | Medium; causal localization exists, but long-CoT dynamics remain unstable to measure                                                              | Medium-high for simplified settings; medium for production MLLMs                                           | Medium-low to medium; causal case studies exist, systematic replication is limited                                        |
| Shortcut/confound risk           | Very high: position, sequence length, decoding format, textual priors, image-token count                                                          | Very high: labels, semantics, answer frequency, retrieval, order, textual context                          | Very high: templates, object size, color priors, tokenization, spatial arrangement                                        |
| Public-data availability         | High                                                                                                                                              | High                                                                                                       | High, though high-quality counterfactual binding data is less abundant                                                    |
| Small-model feasibility          | Moderate for behavior; low for full circuit tracing                                                                                               | High for behavioral and small-transformer studies                                                          | Moderate for probing; low for full circuit discovery                                                                      |
| Potential empirical contribution | Narrowly promising if focused on causal visual utilization rather than attention curves                                                           | Promising only for a sharply controlled unresolved mechanism                                               | Promising for cross-model generalization and causal binding tests                                                         |
| Current uncertainty              | Whether long reasoning creates a distinct visual-utilization failure beyond ordinary context/position effects                                     | Whether findings from synthetic or controlled ICL transfer to natural multimodal prompts                   | Whether reported binding circuits are general mechanisms or model/task-specific artifacts                                 |

### Mechanism, task, method, and benchmark distinctions

The following distinctions are necessary:

- **Research problem:** Why does a model assign the wrong attribute or relation to an object?
- **Mechanism:** Language-prior interference, induction-style copying, visual evidence suppression, or binding-ID routing.
- **Task:** VQA, visual counting, outlier detection, image classification, visual question answering.
- **Method:** Activation patching, probing, logit lens, attention analysis, transcoder-based circuit tracing.
- **Benchmark:** Winoground, WhatIfVis, OK-VQA, CLEVR, SugarCrepe, GQA.
- **Intervention:** Image counterfactual swap, modality zeroing, head knockout, activation steering, demonstration permutation.

## 3. Paper Landscape

The table below is a screened map rather than a claim that every listed paper is equally mature. Papers marked as recent preprints should not be treated as settled evidence. Full-paper claims are cited where the PDF was inspected; other entries are discovery-level records requiring Phase 2 verification.

### Field A — Visual evidence utilization and multimodal inference-time reasoning

| Paper                                                                                                                                 |   Year/status | Exact problem and mechanism                                                                 | Data/models                                        | Main finding and relevance                                                                                                                                                                                                                                |
| ------------------------------------------------------------------------------------------------------------------------------------- | ------------: | ------------------------------------------------------------------------------------------- | -------------------------------------------------- | --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| [Look Light, Think Heavy: What Multimodal Chain-of-Thought Reasoning Can and Cannot Do](https://www.alphaxiv.org/abs/2606.22565)       | 2026 preprint | What does multimodal CoT improve, and where does it fail?                                   | Multimodal reasoning benchmarks; recent MLLMs      | Directly challenges the assumption that longer reasoning automatically means better visual grounding. High relevance to Field A.                                                                                                                          |
| [UniT: Unified Multimodal Chain-of-Thought Test-time Scaling](https://www.alphaxiv.org/abs/2602.12279)                                 | 2026 preprint | Can multimodal reasoning benefit from unified test-time scaling?                            | Unified multimodal models; reasoning tasks         | Occupies the broad “multimodal test-time compute” direction.                                                                                                                                                                                            |
| [Circuit Tracing in Vision–Language Models](https://www.alphaxiv.org/abs/2602.20330)                                                  | 2026 preprint | How do visual and semantic features form causal circuits?                                   | Gemma-3-4B-it; ImageNet, Cauldron, text data       | Reports hierarchical visual-semantic integration and causal feature interventions. It occupies broad visual-information-flow questions but is limited to one model and expensive tooling.[Core findings](https://www.alphaxiv.org/abs/2602.20330v1?page=7) |
| [Seeing or Knowing? Visual Context Sensitivity in Multimodal Large Language Models](https://www.alphaxiv.org/abs/2607.26326)           | 2026 preprint | Does failure reflect missing visual information or unreliable use of preserved information? | WhatIfVis; six models from Qwen and Gemma families | Finds that coarse visual evidence can remain decodable while visual-versus-prior control is unstable. This directly occupies the “text-only prior takeover” hypothesis.[WhatIfVis](https://www.alphaxiv.org/abs/2607.26326v2?page=7)                     |
| [Diagnosing Visual Ignorance in Vision-Language Models](https://www.alphaxiv.org/abs/2606.06890)                                       | 2026 preprint | How do linguistic expectations suppress visual evidence?                                    | VLM diagnostic tasks and internal representations  | Directly overlaps language-prior override and layer-wise visual information routing.                                                                                                                                                                      |
| [The Ebb and Flow of Multimodal Focus](https://www.alphaxiv.org/abs/2607.11436)                                                        | 2026 preprint | How should visual evidence be scheduled during multimodal reasoning?                        | Multimodal reasoning benchmarks                    | Mechanistically close to visual relay windows and repeated visual inspection; direct overlap with Field A.                                                                                                                                                |
| [VIG: Visual Information Gain as a Reward Signal for Multimodal Chain-of-Thought Compression](https://www.alphaxiv.org/abs/2608.21883) | 2026 preprint | Can visual information gain determine which reasoning tokens to retain?                     | Multimodal CoT data                                | Occupies visual redundancy, reasoning compression, and visual-utilization allocation.                                                                                                                                                                     |
| [DRT: Dense Reasoning Trace for Efficient and Grounded Multimodal Reasoning](https://www.alphaxiv.org/abs/2609.21675)                  | 2026 preprint | Can reasoning traces preserve visual grounding more efficiently?                            | Recent multimodal reasoning models                 | Very recent and not yet sufficient to establish a settled mechanism, but it directly overlaps grounded CoT.                                                                                                                                               |
| [Visual Information Gain as a Reward Signal for Multimodal Chain-of-Thought Compression](https://www.alphaxiv.org/abs/2608.21883)      | 2026 preprint | Does repeated visual description contribute useful information?                             | Multimodal reasoning traces                        | Directly occupies the proposed repeated visual re-inspection and redundancy hypothesis.                                                                                                                                                                   |
| [Towards Understanding Visual Grounding in Vision-Language Models](https://www.alphaxiv.org/abs/2509.10345)                            | 2025 preprint | How is visual grounding represented and compressed?                                         | VLM grounding and token-compression settings       | Relevant background for visual-token utilization, though not necessarily a long-CoT study.                                                                                                                                                                |

The strongest directly verified Field A evidence is the visual-context-sensitivity work. It constructs paired counterfactual examples where the model must either follow the image or ignore it, and reports that standard end-to-end benchmarks conflate perception with utilization. [Perception versus utilization](https://www.alphaxiv.org/abs/2607.26326v2?page=2) This makes “visual neglect” scientifically meaningful, but also means a generic project on visual-versus-language reliance is already occupied.

### Field B — Multimodal in-context learning and cross-modal task induction

| Paper                                                                                                                               |   Year/status | Exact problem and mechanism                                                           | Data/models                                                                                  | Main finding and relevance                                                                                                                                                            |
| ----------------------------------------------------------------------------------------------------------------------------------- | ------------: | ------------------------------------------------------------------------------------- | -------------------------------------------------------------------------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| [Dissecting Multimodal In-Context Learning](https://www.alphaxiv.org/abs/2601.20796)                                                 |     2026 ICML | What circuits implement multimodal ICL?                                               | Synthetic controlled transformers; Omniglot, Mini-ImageNet; Qwen2.5-VL                       | Finds induction-style circuits, modality asymmetry, and causal head dependence. This directly occupies “multimodal induction heads.”                                                |
| [Why Multimodal In-Context Learning Lags Behind?](https://www.alphaxiv.org/abs/2604.13403)                                           | 2026 preprint | Why does few-shot multimodal ICL lag text-only ICL?                                   | Controlled outlier detection, Clock Math, Operator Induction, OK-VQA; Qwen2.5-VL and Gemma-3 | Separates task-mapping construction from transfer and identifies cross-modal misalignment as a bottleneck.[Few-shot performance gap](https://www.alphaxiv.org/abs/2604.13403v1?page=4) |
| [TwinICL: Diagnosing Multimodal In-Context Learning through Paired Counterfactuals](https://www.alphaxiv.org/abs/2609.15028)         | 2026 preprint | Can paired text/image counterfactuals isolate genuine multimodal ICL?                 | Paired multimodal/text diagnostic tasks                                                      | Directly addresses modality shortcuts and is therefore a major antithesis paper for Field B.                                                                                          |
| [When Is a Task Vector Enough? An Empirical Theory of Implicit Multimodal ICL](https://www.alphaxiv.org/abs/2608.13385)              | 2026 preprint | Are demonstrations compressed into task vectors or query-conditioned transformations? | Implicit multimodal ICL settings                                                             | Occupies representation-level explanations of multimodal demonstrations.                                                                                                              |
| [CLBench-V: Evaluating Multimodal Context Learning from Grounding to Knowledge Acquisition](https://www.alphaxiv.org/abs/2607.25294) | 2026 preprint | How should multimodal context learning be evaluated across capabilities?              | Grounding and knowledge-acquisition tasks                                                    | Benchmark work; useful evaluation asset but not itself a mechanism explanation.                                                                                                       |
| [Enhancing Multimodal In-Context Learning via Inductive-Deductive Reasoning](https://www.alphaxiv.org/abs/2605.02378)                | 2026 preprint | Can explicit induction/deduction improve fragile multimodal ICL?                      | Multimodal ICL benchmarks                                                                    | Occupies method space and reports analyses of multimodal ICL weakness.                                                                                                                |
| [Many-Shot CoT-ICL: Making In-Context Learning Truly Learn](https://www.alphaxiv.org/abs/2605.13511)                                 | 2026 preprint | How does many-shot ICL interact with reasoning traces?                                | Reasoning tasks                                                                              | Relevant to demonstration quantity and reasoning, though not necessarily visual-specific in all experiments.                                                                          |
| True Multimodal In-Context Learning Needs Attention to the Visual Context                                                           | 2025 preprint | Does apparent multimodal ICL require actual visual attention?                         | Multimodal ICL tasks                                                                         | Directly overlaps the proposed visual-demonstration-utilization hypothesis.                                                                                                           |
| Mimicking or Reasoning: Rethinking Multi-Modal In-Context Learning in Vision-Language Models                                        | 2025 preprint | Are models learning a task or imitating demonstration patterns?                       | VLM ICL tasks                                                                                | Occupies the shortcut-versus-genuine-induction question.                                                                                                                              |
| [Multimodal Task Vectors Enable Many-Shot Multimodal In-Context Learning](2408)                                                      |  2024 NeurIPS | Can many demonstrations be compressed into task vectors?                              | Multimodal ICL                                                                               | Foundational but not within the requested window; important because it pre-empts broad task-vector questions.                                                                         |

The final row is intentionally not linked because the exact paper identifier was not verified in this search. The paper should not be used as a decisive source until its official URL is checked.

The 2026 ICML study provides unusually strong evidence against a naïve “multimodal induction is unexplored” claim. In controlled experiments, knocking out identified previous-token and induction heads reduces ICL accuracy, and zeroing the secondary modality causes a major performance drop. [Causal ablation](https://www.alphaxiv.org/abs/2601.20796v2?page=8) It does not prove that all natural-image MLLM ICL reduces to the same mechanism, but it makes the broad mechanism already occupied.

### Field C — Mechanistic compositional grounding and visual binding

| Paper                                                                                                                                                                                                                       |        Year/status | Exact problem and mechanism                                                   | Data/models                                    | Main finding and relevance                                                                                                                                         |
| --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | -----------------: | ----------------------------------------------------------------------------- | ---------------------------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------ |
| [Investigating Mechanisms for In-Context Vision Language Binding](https://openaccess.thecvf.com/content/CVPR2025W/MIV/papers/Saravanan_Investigating_Mechanisms_for_In-Context_Vision_Language_Binding_CVPRW_2025_paper.pdf) | 2025 CVPR workshop | How are visual entities bound to textual references in context?               | Synthetic and vision-language binding settings | Reports binding-ID-like activation behavior and causal swapping. Directly occupies object-attribute/reference binding.                                             |
| Visual Symbolic Mechanisms: Emergent Symbol Processing in Vision Language Models                                                                                                                                            |   2025/2026 status | Do VLMs develop symbolic intermediate mechanisms for visual binding?          | Synthetic geometric visual tasks; VLMs         | Reports a multi-stage mechanism involving ID retrieval, selection, and feature retrieval. This is close to the proposed binding mechanism.                         |
| [Diagnosing Visual Ignorance in Vision-Language Models](https://www.alphaxiv.org/abs/2606.06890)                                                                                                                             |      2026 preprint | How do linguistic priors override visual attributes?                          | Counterfactual and internal diagnostic tasks   | Mechanistically overlaps attribute binding and language-prior interference.                                                                                        |
| [Seeing or Knowing? Visual Context Sensitivity in Multimodal Large Language Models](https://www.alphaxiv.org/abs/2607.26326)                                                                                                 |      2026 preprint | Are attributes represented but inconsistently used?                           | WhatIfVis; Qwen and Gemma families             | Relevant because binding errors can reflect utilization failure rather than missing representations.                                                               |
| [Towards Understanding Visual Grounding in Vision-Language Models](https://www.alphaxiv.org/abs/2509.10345)                                                                                                                  |      2025 preprint | How are visual tokens mapped into language representations?                   | Grounding and visual-token analysis            | Provides representation and token-flow background.                                                                                                                 |
| [Circuit Tracing in Vision–Language Models](https://www.alphaxiv.org/abs/2602.20330)                                                                                                                                        |      2026 preprint | Can causal circuits be extracted from VLMs?                                   | Gemma-3-4B-it; ImageNet, Cauldron              | Finds separate visual and semantic pathways with late convergence and demonstrates feature patching.[Limitations](https://www.alphaxiv.org/abs/2602.20330v1?page=8) |
| [Do VLMs Have Bad Eyes? Diagnosing Compositional Failures via Mechanistic Interpretability](2505)                                                                                                                            |        2025 status | Are compositional failures caused by visual encoding or later reasoning?      | Compositional visual tasks                     | Relevant foundational direction, but exact identifier was not verified here.                                                                                       |
| [Winoground](https://github.com/facebookresearch/理解)                                                                                                                                                                       |     2022 benchmark | Can models distinguish captions that differ only in compositional assignment? | 400 image-caption pairs                        | Foundational compositionality benchmark, but too small and saturated to serve as sole evidence for a 2026 mechanism.                                               |
| SugarCrepe                                                                                                                                                                                                                  |     2024 benchmark | Can models distinguish controlled compositional image-caption changes?        | Synthetic/edited image-caption pairs           | Useful but vulnerable to generated-edit and caption artifacts; exact official paper URL requires verification.                                                     |
| CLEVR                                                                                                                                                                                                                       |     2017 benchmark | Can models reason over object attributes and relations?                       | Synthetic scenes with symbolic programs        | Foundational diagnostic asset, but its synthetic regularity limits natural-image conclusions.                                                                      |

Field C is not a blank space. However, the literature is less unified than Field B. “Binding” may mean reference binding, attribute binding, compositional caption matching, relation tracking, or a causal mechanism in intermediate representations. A thesis would need to choose one meaning.

## 4. Antithesis Findings

### Field A: Visual evidence utilization and multimodal inference-time reasoning

#### A. Proposed hypothesis/mechanism

Candidate hypotheses include:

1. visual attention decreases as reasoning length increases;
2. visual-token utilization decays during long CoT;
3. textual priors take over after visual evidence is initially encoded;
4. models need repeated visual re-inspection during extended reasoning;
5. additional test-time compute is allocated mostly to language rather than vision.

#### B. Closest existing work

The closest verified work is [Seeing or Knowing?](https://www.alphaxiv.org/abs/2607.26326), which explicitly separates visual information availability from visual evidence utilization. It reconstructs images from final-layer image tokens and introduces WhatIfVis, where context and prior answers conflict. The study reports that the visual evidence for coarse attributes survives in the representation, while the model’s policy for using or ignoring it is unstable. [Representation evidence](https://www.alphaxiv.org/abs/2607.26326v2?page=4)

[Circuit Tracing](https://www.alphaxiv.org/abs/2602.20330) also occupies general visual-semantic information-flow questions. It identifies progressive integration across layers, parallel visual and semantic pathways, and causal feature interventions. [Visual-semantic pathways](https://www.alphaxiv.org/abs/2602.20330v1?page=8)

Recent 2026 papers on multimodal test-time scaling, visual latent reasoning, visual-state updates, and visual reasoning compression occupy the broader compute-allocation space.

#### C. Direct overlap

- **Visual utilization versus reasoning length:** I did not identify a verified paper in this search that cleanly tests visual-token utilization as a function of CoT length under length-matched and compute-matched controls.
- **Visual-versus-prior reliance:** Directly occupied by [Seeing or Knowing?](https://www.alphaxiv.org/abs/2607.26326).
- **Visual redundancy and repeated inspection:** Directly or mechanistically occupied by [VIG](https://www.alphaxiv.org/abs/2608.21883) and [The Ebb and Flow of Multimodal Focus](https://www.alphaxiv.org/abs/2607.11436).
- **Internal visual circuits during reasoning:** Occupied at case-study level by [Circuit Tracing](https://www.alphaxiv.org/abs/2602.20330).

#### D. Mechanistic overlap

Terminology substitution reveals the following equivalents:

| User terminology                                | Literature terminology found                                                        |
| ----------------------------------------------- | ----------------------------------------------------------------------------------- |
| Visual attention drift                          | Visual-context sensitivity, visual focus scheduling, visual information utilization |
| Text-only prior takeover                        | Language-prior override, visual ignorance, vision-versus-prior conflict             |
| Visual-token utilization                        | Visual evidence preservation, visual grounding, visual information gain             |
| Repeated visual re-inspection                   | Visual relay windows, visual state updates, adaptive visual computation             |
| Allocation of reasoning between vision and text | Multimodal test-time scaling, visual latent reasoning, grounded reasoning traces    |

#### E. What remains genuinely uncertain

The unresolved question is not whether VLMs can ignore visual evidence. That is occupied. The more precise uncertainty is:

> Does visual evidence utilization change systematically with reasoning length after controlling for token position, total sequence length, output format, image-token count, and the number of visual re-encodings?

I did not identify a paper testing this exact causal formulation in the searched literature.

#### F. Confidence in openness

**Confidence: Medium.** The broad phenomenon is occupied, but the carefully controlled relationship between reasoning length and visual utilization remains **not found**, not verified novel.

### Field B: Multimodal in-context learning and cross-modal task induction

#### A. Proposed hypothesis/mechanism

Candidate hypotheses include:

1. multimodal demonstrations induce a task rule rather than merely providing semantic similarity;
2. image-to-image or image-to-text induction is implemented by an induction-like circuit;
3. demonstration ordering changes cross-modal task transfer;
4. label permutation reveals whether the model is using demonstrations rather than memorized answer priors;
5. visual demonstrations are often ignored while textual labels drive performance.

#### B. Closest existing work

[Dissecting Multimodal In-Context Learning](https://www.alphaxiv.org/abs/2601.20796) directly tests induction-style circuits and modality asymmetry. It uses controlled synthetic data to distinguish ICL from in-weight learning, varies data complexity and architecture, and validates some results on Qwen2.5-VL. [Controlled testbed](https://www.alphaxiv.org/abs/2601.20796v2?page=2)

[Why Multimodal In-Context Learning Lags Behind?](https://www.alphaxiv.org/abs/2604.13403) directly studies task-mapping construction and transfer in Qwen2.5-VL and Gemma-3. It reports that demonstrations can ground labels to visual evidence at intermediate layers, even when the final query answer is wrong. [Task mapping construction](https://www.alphaxiv.org/abs/2604.13403v1?page=6)

#### C. Direct overlap

- **Multimodal ICL exists:** established.
- **Demonstration sensitivity:** established by multiple configuration and benchmark papers.
- **Visual-context underuse:** directly occupied.
- **Induction heads:** directly occupied in controlled transformers and partially validated in production MLLMs.
- **Task mapping transfer:** directly occupied by the 2026 bottleneck study.
- **Cross-modal induction in natural-image tasks:** partially occupied; the degree to which the synthetic induction mechanism explains natural prompts remains uncertain.

#### D. Mechanistic overlap

The terminology substitution search found:

- multimodal induction → induction-style label matching;
- cross-modal pattern transfer → task mapping transfer;
- image-to-text induction → modality alignment and label-copying;
- demonstration ordering → sequence configuration and context sensitivity;
- label permutation → swapped-label ICL evaluation;
- textual shortcut → text-driven multimodal ICL or visual-context underutilization.

#### E. What remains genuinely uncertain

The strongest remaining uncertainty is:

> When a natural-image MLLM succeeds under multimodal ICL, does it use a transferable cross-modal task mapping, or does it combine textual label cues, semantic similarity, and query-image recognition without transferring the intended rule?

This remains only partially answered because existing studies use different tasks, models, and operational definitions.

#### F. Confidence in openness

**Confidence: Low to Medium.** Broad questions are occupied. A cross-model, natural-image, counterfactual diagnosis could remain open, but the area is highly crowded and recent work is rapidly closing the obvious gaps.

### Field C: Mechanistic compositional grounding and visual binding

#### A. Proposed hypothesis/mechanism

Candidate hypotheses include:

1. models fail because they do not bind attributes to the correct objects;
2. linguistic priors override object-attribute representations;
3. object and attribute information travel through separable intermediate pathways;
4. binding is implemented by content-independent identifiers or routing vectors;
5. compositional failures arise in the decoder rather than the vision encoder.

#### B. Closest existing work

[Investigating Mechanisms for In-Context Vision Language Binding](https://openaccess.thecvf.com/content/CVPR2025W/MIV/papers/Saravanan_Investigating_Mechanisms_for_In-Context_Vision_Language_Binding_CVPRW_2025_paper.pdf) is the closest direct binding paper. It studies how image tokens become associated with textual references and uses causal activation swapping to test binding-related representations.

Visual Symbolic Mechanisms reports a staged symbolic mechanism for visual binding. This means that “do VLMs have a binding mechanism?” is already occupied.

[Circuit Tracing](https://www.alphaxiv.org/abs/2602.20330) provides broader mechanistic evidence: early layers remain more modality-specific, higher layers integrate visual and semantic concepts, and intervention on visual features can alter outputs. [Hierarchical integration](https://www.alphaxiv.org/abs/2602.20330v1?page=7)

#### C. Direct overlap

- **Attribute binding:** directly occupied.
- **Reference/object binding:** directly occupied.
- **Compositional benchmarks:** heavily occupied.
- **Layer-wise visual information flow:** occupied.
- **Language-prior interference:** occupied in broad form.
- **Cross-model generality of causal binding mechanisms:** not clearly established.
- **Binding under natural-image variation and adversarial counterfactuals:** partially occupied.

#### D. Mechanistic overlap

| Proposed term                           | Literature equivalent                                           |
| --------------------------------------- | --------------------------------------------------------------- |
| Attribute binding                       | Object-attribute binding, binding IDs, visual-language binding  |
| Feature swapping                        | Activation patching, feature intervention, circuit patching     |
| Linguistic prior override               | Visual ignorance, language bias, vision-versus-prior conflict   |
| Visual token versus language-token flow | Cross-modal information flow, modality-specific/shared pathways |
| Compositional grounding                 | Compositional generalization, systematicity, visual grounding   |
| Intermediate representation probing     | Representation probing, activation patching, circuit tracing    |

#### E. What remains genuinely uncertain

The most defensible remaining question is not whether binding failures exist. It is:

> Are proposed binding representations and causal pathways stable across models, layouts, attributes, relations, and natural-image distributions, or are they artifacts of a narrow synthetic task and one architecture?

I did not identify a paper that answers this comprehensively.

#### F. Confidence in openness

**Confidence: Medium.** The phenomenon and several mechanisms are occupied, but systematic cross-model causal validation remains incompletely answered.

## 5. Dataset & Benchmark Audit

| Dataset/benchmark                 | Task                                           | Size/accessibility                                            | Synthetic/real                                      | Leakage and shortcut risk                                                                  | Suitability                                                                        |
| --------------------------------- | ---------------------------------------------- | ------------------------------------------------------------- | --------------------------------------------------- | ------------------------------------------------------------------------------------------ | ---------------------------------------------------------------------------------- |
| WhatIfVis                         | Follow image context versus parametric prior   | 3,049 manually inspected samples; introduced with public work | Counterfactual images derived from existing sources | Answer vocabulary, paired prompt templates, source-image artifacts, exact-match formatting | Strong for visual-utilization diagnostics; not a generic benchmark                 |
| OK-VQA                            | Knowledge-intensive VQA                        | Publicly available; commonly used                             | Real images                                         | OCR, question priors, answer-frequency bias, external knowledge leakage                    | Useful for multimodal ICL and visual evidence, weak for isolating mechanisms alone |
| MMMU                              | Multidisciplinary multimodal reasoning         | Public benchmark                                              | Mostly real/document-style data                     | Subject knowledge, answer-position and formatting effects                                  | Good broad reasoning test; poor causal mechanism isolation                         |
| MathVista                         | Mathematical visual reasoning                  | Public benchmark                                              | Real and synthetic/document images                  | OCR and question-template shortcuts; memorization risk                                     | Useful for reasoning, weak for visual-token mechanism claims                       |
| HallusionBench                    | Hallucination and visual conflict              | Public benchmark                                              | Real and constructed examples                       | Language priors and question framing can dominate                                          | Strong for hallucination/conflict, not sufficient for layer-level claims           |
| Winoground                        | Image-caption compositional matching           | Small public benchmark                                        | Real images with paired captions                    | Small size, caption style, dataset saturation                                              | Good stress test, insufficient as sole evaluation                                  |
| SugarCrepe                        | Controlled compositional image-caption changes | Public benchmark                                              | Edited/generated variants and real images           | Edit artifacts, caption templates, object-name priors                                      | Useful for compositional contrast, needs artifact controls                         |
| CLEVR                             | Synthetic object-attribute-relation reasoning  | Public                                                        | Synthetic                                           | Strong templates, regular layouts, symbolic language leakage                               | Excellent causal control, weak natural-image validity                              |
| GQA                               | Compositional VQA and scene reasoning          | Public                                                        | Real images with structured questions               | Question templates, annotation bias, answer priors                                         | Useful for compositional evaluation, not mechanism-isolating by itself             |
| TrueMICL/Open-MI-style tasks      | Multimodal task induction                      | Public code/data associated with recent work                  | Synthetic plus natural-image tasks                  | Labels, ordering, textual demonstrations, answer frequency                                 | Strong when paired with modality and label-permutation controls                    |
| Omniglot                          | Few-shot visual classification                 | Public                                                        | Real handwritten characters                         | Low semantic complexity; encoder quality confound                                          | Good controlled ICL asset                                                          |
| Mini-ImageNet                     | Few-shot image classification                  | Public                                                        | Real images                                         | Class semantics and pretrained recognition leakage                                         | Useful for ICL, not necessarily binding                                            |
| ImageNet                          | Visual representation analysis                 | Public with licensing conditions                              | Real images                                         | Pretraining contamination and class-label priors                                           | Useful representation source; weak as a causal binding test                        |
| Cauldron-style multimodal mixture | VLM training/analysis corpus                   | Public components vary by subset                              | Real image-text                                     | Mixture heterogeneity and contamination                                                    | Useful for representation extraction, difficult to interpret causally              |

The strongest benchmark for Field A is currently a **paired counterfactual visual-context test** such as WhatIfVis, because ordinary VQA cannot distinguish failure to encode an attribute from failure to use it. The benchmark itself warns that exact-match metrics can introduce formatting failures; its probability scorer is therefore important. [Benchmark scoring](https://www.alphaxiv.org/abs/2607.26326v2?page=7)

For Field B, the strongest assets are matched text/image task formulations, label permutation, modality zeroing, and demonstration-order perturbations. Any benchmark without these controls is weak evidence for genuine cross-modal induction.

For Field C, CLEVR offers the best causal control, while Winoground and SugarCrepe offer greater natural-image relevance. Neither alone proves a binding mechanism. Synthetic benchmarks risk language and layout leakage; natural benchmarks risk image duplication, captions, and semantic priors.

## 6. Model & Compute Audit

| Model family                        | Open weights            | Vision component/architecture                                   | Approximate practical burden                                           | Relevant fields                       |
| ----------------------------------- | ----------------------- | --------------------------------------------------------------- | ---------------------------------------------------------------------- | ------------------------------------- |
| Qwen2.5-VL small variants           | Yes                     | Vision encoder plus language decoder with multimodal projection | Moderate inference; activation extraction can become high-memory       | A, B, C                               |
| Gemma-3 multimodal small variants   | Yes                     | SigLIP-based vision pathway and multimodal transformer          | Moderate inference; relatively attractive for hooks and layer analysis | A, B, C                               |
| SmolVLM family                      | Yes                     | Small VLM architecture                                          | Low-to-moderate inference; weaker reasoning ceiling                    | A, B, C for pilot controls            |
| LLaVA-family models                 | Yes                     | CLIP/SigLIP-style encoder plus LLM projector                    | Low-to-moderate for smaller checkpoints; architecture varies           | A, C; some B                          |
| IDEFICS family                      | Open variants available | Interleaved vision-language architecture                        | Moderate to high depending on size                                     | B                                     |
| Unified multimodal reasoning models | Some open checkpoints   | May include visual latent/state generation                      | Often high and architecture-specific                                   | A; less suitable for first experiment |

A small open model is sufficient for:

- inference-only counterfactual evaluation;
- modality ablations;
- demonstration permutations;
- output-logit comparisons;
- limited hidden-state extraction;
- linear probing on selected layers.

A small model is not automatically sufficient for:

- full circuit tracing;
- large-scale transcoder training;
- stable conclusions about frontier-model reasoning;
- comparing many architectures with long image sequences.

The circuit-tracing paper illustrates the engineering risk. Its Gemma-3-4B setup uses 256 image tokens, a 34-layer decoder, transcoder training on eight H100 GPUs, and expensive attribution-graph computation. [Model and graph cost](https://www.alphaxiv.org/abs/2602.20330v1?page=5) The authors also report that feature discovery is substantially more expensive for images than text and that their current method is limited to one model. [Limitations](https://www.alphaxiv.org/abs/2602.20330v1?page=8)

### Compute tiers

| Tier                     | Field A                  | Field B                       | Field C                                   |
| ------------------------ | ------------------------ | ----------------------------- | ----------------------------------------- |
| 1. Pure inference        | Feasible                 | Highly feasible               | Feasible                                  |
| 2. Activation extraction | Feasible on small models | Feasible                      | Feasible but memory-intensive             |
| 3. Linear probing        | Feasible                 | Feasible                      | Feasible and useful                       |
| 4. PEFT/LoRA             | Moderate                 | Moderate                      | Moderate-to-high                          |
| 5. Full fine-tuning      | Usually unnecessary      | Usually unnecessary           | Usually unnecessary for mechanism studies |
| 6. Large-scale training  | Impractical              | Impractical for a BSc project | Impractical                               |

The minimum viable experiment for Field A is inference plus hidden-state/logit analysis on a paired counterfactual benchmark. For Field B it is a controlled demonstration suite with modality ablation, label permutation, and order perturbation. For Field C it is a synthetic compositional suite with object/attribute swaps plus layer-wise probes and at least one causal activation intervention.

## 7. Shortcut & Confound Audit

### Field A

**Apparent finding:** visual attention decreases with longer reasoning.

**Easiest alternative explanations:**

- later generated tokens naturally attend differently;
- the visual-token denominator changes with sequence length;
- output-format tokens have distinct attention patterns;
- repeated image tokens or image encodings alter normalization;
- longer answers contain more language-only intermediate steps;
- attention weights are not causal measures of information use;
- the model may retrieve visual information through residual activations without direct attention.

**Minimum controls:**

1. length-matched short and long traces;
2. same output format and answer position;
3. attention normalized separately over visual and textual token groups;
4. matched total sequence length using text padding;
5. visual-token ablation and image replacement;
6. hidden-state or logit intervention, not attention alone;
7. at least two model architectures.

### Field B

**Apparent finding:** multimodal demonstrations improve query accuracy.

**Easiest alternative explanations:**

- textual labels reveal the answer distribution;
- demonstrations are semantically similar to the query;
- the model recognizes the query image independently;
- answer position or token frequency drives performance;
- demonstration order creates recency effects;
- the model copies labels without learning the intended task;
- multimodal gains are actually text-only ICL gains.

**Minimum controls:**

1. label permutation;
2. image-only, text-only, and image-plus-text conditions;
3. shuffled demonstrations;
4. semantically mismatched but structurally valid demonstrations;
5. answer-frequency balancing;
6. novel labels or synthetic label tokens;
7. query image ablation;
8. exact task-mapping probes separate from final-answer accuracy.

### Field C

**Apparent finding:** a model fails attribute binding.

**Easiest alternative explanations:**

- color or object frequency prior;
- object size or salience;
- spatial arrangement;
- question wording;
- tokenization;
- caption or label priors;
- image-edit artifacts;
- vision encoder resolution;
- answer-position bias;
- the model may represent the binding but fail to use it at decoding.

**Minimum controls:**

1. paired feature swaps with identity held constant;
2. balanced attribute/object frequencies;
3. position-balanced layouts;
4. image-only and text-only controls;
5. counterfactual captions;
6. multiple object sizes and distances;
7. representation probes before and after the connector;
8. activation patching or causal ablation;
9. evaluation on both synthetic and natural images.

## 8. Negative-Result Analysis

### Field A

A negative result could show that apparent visual degradation with long CoT is fully explained by position, sequence length, or decoding format. That would be scientifically useful because it would distinguish a real multimodal computation problem from an artifact of attention measurement. A further useful result would be that visual evidence remains encoded but is not causally used, supporting a perception-utilization distinction.

### Field B

A negative result could show that apparent multimodal ICL disappears under label permutation or image ablation. That would establish that the model is using textual or semantic shortcuts rather than cross-modal task induction. Conversely, if performance survives those controls, the result would strengthen the case for genuine cross-modal induction.

### Field C

A negative result could show that apparent binding failures are caused by benchmark templates, object salience, or language priors rather than absent internal binding. This would be useful even without improving accuracy because it would invalidate common interpretations of compositional benchmark scores. A cross-model failure to reproduce a proposed binding circuit would also be valuable evidence about mechanistic instability.

## 9. Closest-Work Matrix

| Proposed mechanism                             | Closest paper                                                                                                                                                                                                               | What it already tests                                      | What it does not establish                                  | Overlap            | Remaining question                                                       |
| ---------------------------------------------- | --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | ---------------------------------------------------------- | ----------------------------------------------------------- | ------------------ | ------------------------------------------------------------------------ |
| Visual attention decreases with CoT length     | [Seeing or Knowing?](https://www.alphaxiv.org/abs/2607.26326)                                                                                                                                                                | Visual evidence presence and visual-versus-prior control   | Not a clean CoT-length intervention                         | Mechanistic        | Does utilization change with reasoning length under matched controls?    |
| Text-only prior takeover                       | [Diagnosing Visual Ignorance](https://www.alphaxiv.org/abs/2606.06890)                                                                                                                                                       | Layer-wise linguistic suppression of visual evidence       | Generality across models/tasks remains uncertain            | Direct             | Which routing changes are causal and architecture-independent?           |
| Visual information decay during long reasoning | [VIG](https://www.alphaxiv.org/abs/2608.21883)                                                                                                                                                                               | Visual redundancy and information gain in reasoning traces | Exact decay law under controlled length is unclear          | Mechanistic        | Is the apparent decay true information loss or reduced direct attention? |
| Repeated visual re-inspection                  | [The Ebb and Flow of Multimodal Focus](https://www.alphaxiv.org/abs/2607.11436)                                                                                                                                              | Scheduling visual focus windows                            | General causal necessity remains uncertain                  | Direct/mechanistic | When is re-inspection actually needed?                                   |
| Multimodal test-time compute allocation        | [UniT](https://www.alphaxiv.org/abs/2602.12279)                                                                                                                                                                              | Unified multimodal CoT test-time scaling                   | Does not isolate visual versus textual compute              | Direct             | Can compute be allocated adaptively to visual evidence?                  |
| Multimodal induction heads                     | [Dissecting Multimodal ICL](https://www.alphaxiv.org/abs/2601.20796)                                                                                                                                                         | Induction-style circuits and head knockout                 | Natural-image generality is limited                         | Direct             | How much of natural MLLM ICL uses the same circuit?                      |
| Demonstration task mapping transfer            | [Why Multimodal ICL Lags Behind?](https://www.alphaxiv.org/abs/2604.13403)                                                                                                                                                   | Construction and transfer across layers                    | Broad task and architecture generality                      | Direct             | Can transfer failure be predicted from representations?                  |
| Visual demonstrations are ignored              | True Multimodal ICL Needs Attention                                                                                                                                                                                         | Relationship between visual attention and ICL              | Attention may not equal causal use                          | Direct             | What causal intervention separates attention from utilization?           |
| Object-attribute binding                       | [Investigating Mechanisms for In-Context Vision Language Binding](https://openaccess.thecvf.com/content/CVPR2025W/MIV/papers/Saravanan_Investigating_Mechanisms_for_In-Context_Vision_Language_Binding_CVPRW_2025_paper.pdf) | Binding representations and activation swaps               | Cross-model and natural-image stability                     | Direct             | Are binding IDs universal or task-specific?                              |
| Binding through symbolic stages                | Visual Symbolic Mechanisms                                                                                                                                                                                                  | Multi-stage visual symbolic processing                     | Generality beyond synthetic tasks                           | Direct             | Do these stages survive realistic visual variation?                      |
| Visual-semantic circuit separation             | [Circuit Tracing](https://www.alphaxiv.org/abs/2602.20330)                                                                                                                                                                   | Causal tracing and feature steering                        | One model; high compute; human annotation                   | Mechanistic        | Can a lightweight quantitative version generalize?                       |
| Language prior overrides attributes            | [Seeing or Knowing?](https://www.alphaxiv.org/abs/2607.26326)                                                                                                                                                                | Counterfactual context/prior conflict                      | Does not focus specifically on object-attribute permutation | Mechanistic        | How does binding interact with prior suppression?                        |

## 10. Research Crowding Map

### Field A: **Crowded**

The broad field is crowded because visual neglect, language-prior interference, multimodal reasoning, visual grounding, visual latent reasoning, and test-time scaling are all active. The narrower question of *visual utilization as a function of reasoning length under rigorous controls* appears less directly occupied, but this is an inferred gap rather than a verified novelty claim.

### Field B: **Crowded**

There are established benchmark, method, behavioral, and mechanistic strands. The 2026 papers already address task mapping, induction circuits, modality asymmetry, visual-context underuse, and paired counterfactual diagnosis. Only a sharply bounded natural-image causal question should proceed.

### Field C: **Moderately crowded**

The field has established benchmarks and several direct mechanistic studies, but terminology remains fragmented and systematic cross-model causal validation is limited. This creates opportunity but also risk: an apparent gap may reflect inconsistent naming rather than genuine absence of work.

## 11. Candidate Question Inventory

### Field A

| Candidate question                                                                                         | Mechanism                                   | Closest work                                                                                                | Current gap status | Main confound                              | Negative-result value                                      | Phase-2 worthiness |
| ---------------------------------------------------------------------------------------------------------- | ------------------------------------------- | ----------------------------------------------------------------------------------------------------------- | ------------------ | ------------------------------------------ | ---------------------------------------------------------- | ------------------ |
| Does visual evidence utilization change with reasoning length after position and sequence-length controls? | Visual utilization versus textual reasoning | [Seeing or Knowing?](https://www.alphaxiv.org/abs/2607.26326), [VIG](https://www.alphaxiv.org/abs/2608.21883) | Partially occupied | Position and attention normalization       | Could show “drift” is an artifact                        | High               |
| Does additional test-time compute improve visual grounding or only language fluency?                       | Modality-specific compute allocation        | [UniT](https://www.alphaxiv.org/abs/2602.12279)                                                              | Partially occupied | Longer output and self-consistency effects | Separates reasoning improvement from grounding improvement | Medium             |
| Does repeated visual re-encoding causally improve counterfactual attribute reasoning?                      | Visual re-inspection                        | [The Ebb and Flow of Multimodal Focus](https://www.alphaxiv.org/abs/2607.11436)                              | Weakly explored    | More compute, not better visual use        | Shows whether reinspection is necessary or cosmetic        | High               |
| Can a visual-versus-prior conflict be localized consistently across small open VLMs?                       | Modality competition                        | [Seeing or Knowing?](https://www.alphaxiv.org/abs/2607.26326)                                                | Partially occupied | Architecture-specific layer placement      | Tests generality of the proposed mechanism                 | Medium             |
| Does attention predict visual use better than activation/logit interventions?                              | Attention versus causal information use     | [Circuit Tracing](https://www.alphaxiv.org/abs/2602.20330)                                                   | Weakly explored    | Attention-as-explanation fallacy           | Clarifies measurement validity                             | High               |

### Field B

| Candidate question                                                                     | Mechanism                        | Closest work                                                                                                           | Current gap status | Main confound                                   | Negative-result value                                         | Phase-2 worthiness |
| -------------------------------------------------------------------------------------- | -------------------------------- | ---------------------------------------------------------------------------------------------------------------------- | ------------------ | ----------------------------------------------- | ------------------------------------------------------------- | ------------------ |
| Do natural-image multimodal ICL gains survive label permutation and image ablation?    | Genuine cross-modal induction    | [Dissecting Multimodal ICL](https://www.alphaxiv.org/abs/2601.20796), [TwinICL](https://www.alphaxiv.org/abs/2609.15028) | Partially occupied | Textual label copying                           | Could establish that “multimodal ICL” is mostly text-driven | Medium             |
| Can task-mapping transfer failure be predicted from intermediate representations?      | Construction-transfer decoupling | [Why Multimodal ICL Lags Behind?](https://www.alphaxiv.org/abs/2604.13403)                                              | Weakly explored    | Probe leakage and task-specific representations | Could show transfer diagnostics are not general               | High               |
| Does demonstration order change visual grounding independently of recency?             | Demonstration routing            | Configuration studies and[Why Multimodal ICL Lags Behind?](https://www.alphaxiv.org/abs/2604.13403)                     | Partially occupied | Recency and position                            | Disentangles order from simple positional bias                | Medium             |
| Are induction-head mechanisms shared between text-only and multimodal ICL?             | Circuit inheritance/refinement   | [Dissecting Multimodal ICL](https://www.alphaxiv.org/abs/2601.20796)                                                    | Partially occupied | Small-model-to-MLLM transfer                    | Tests whether the proposed circuit is genuinely multimodal    | Medium             |
| Can paired image/text tasks distinguish visual task induction from semantic retrieval? | Cross-modal task transfer        | [TwinICL](https://www.alphaxiv.org/abs/2609.15028)                                                                      | Partially occupied | Matched-pair artifacts                          | Useful even if no genuine induction is found                  | Medium             |

### Field C

| Candidate question                                                                                 | Mechanism                         | Closest work                                                                                                                                                                                                              | Current gap status | Main confound                                    | Negative-result value                               | Phase-2 worthiness |
| -------------------------------------------------------------------------------------------------- | --------------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | ------------------ | ------------------------------------------------ | --------------------------------------------------- | ------------------ |
| Do proposed binding representations generalize across object layouts and attributes?               | Binding IDs/routing               | [Investigating Mechanisms for In-Context Vision Language Binding](https://openaccess.thecvf.com/content/CVPR2025W/MIV/papers/Saravanan_Investigating_Mechanisms_for_In-Context_Vision_Language_Binding_CVPR2025_paper.pdf) | Weakly explored    | Synthetic layout regularity                      | Tests whether binding is real or task-specific      | High               |
| Are binding failures caused by missing visual information or failure to use preserved information? | Perception-utilization separation | [Seeing or Knowing?](https://www.alphaxiv.org/abs/2607.26326)                                                                                                                                                              | Partially occupied | Probe head capacity                              | Separates encoder and decoder explanations          | High               |
| Do visual and language pathways converge at consistent layers across VLM architectures?            | Layer-wise information flow       | [Circuit Tracing](https://www.alphaxiv.org/abs/2602.20330)                                                                                                                                                                 | Weakly explored    | Architecture-specific depth                      | Tests generality of pathway claims                  | High               |
| Does activation patching restore correct attribute binding across models?                          | Causal feature routing            | Visual Symbolic Mechanisms                                                                                                                                                                                                | Partially occupied | Patch-site selection and representation mismatch | Shows whether the mechanism is causally useful      | Medium             |
| Can counterfactual image swaps distinguish binding failure from language-prior failure?            | Object-attribute assignment       | [Diagnosing Visual Ignorance](https://www.alphaxiv.org/abs/2606.06890)                                                                                                                                                     | Weakly explored    | Image-edit artifacts and captions                | Improves interpretation of compositional benchmarks | High               |

# Phase 1 Conclusion

### Field A

**Status:** Crowded, but with a narrower unresolved subproblem.

**Why:** Broad questions about visual neglect, visual-versus-prior conflict, visual grounding, multimodal test-time scaling, and visual reasoning traces are already active. The label “visual attention drift” is not a stable research-area name and should be replaced by *visual evidence utilization during multimodal inference*.

**Most important occupied area:** Visual evidence may be represented internally but used unreliably relative to parametric language priors. This is directly studied by [Seeing or Knowing?](https://www.alphaxiv.org/abs/2607.26326).

**Most interesting unresolved uncertainty:** Whether visual utilization changes systematically with reasoning length after controlling for sequence length, token position, output format, visual-token count, and total compute.

**Phase 2:** YES

### Field B

**Status:** Crowded and mechanistically occupied.

**Why:** Multimodal ICL is a legitimate field, but broad questions about demonstration effects, visual-context underuse, task mapping, and induction circuits have already been studied. The proposed phrase “multimodal induction heads” is now substantially occupied by controlled circuit work.

**Most important occupied area:** Induction-style label matching and task-mapping construction/transfer have been directly analyzed, including causal head ablations and layer-wise transfer diagnostics.

**Most interesting unresolved uncertainty:** Whether natural-image MLLM ICL success reflects genuine cross-modal task induction or a mixture of textual label copying, semantic retrieval, and independent query-image recognition.

**Phase 2:** UNCERTAIN

### Field C

**Status:** Moderately crowded, fragmented, and potentially promising after narrowing.

**Why:** Attribute binding, compositional generalization, visual grounding, binding IDs, language-prior interference, and layer-wise visual information flow are distinct but related areas. Direct binding mechanisms already exist, but their cross-model and natural-image generality is not established.

**Most important occupied area:** Binding representations and causal activation-swapping mechanisms have already been reported, including binding-ID-like behavior and symbolic processing stages.

**Most interesting unresolved uncertainty:** Whether proposed binding mechanisms generalize across architectures, object layouts, attributes, relations, and natural-image distributions, or are artifacts of narrow synthetic tasks.

**Phase 2:** YES

## Phase-2 Shortlist

1. **Does visual evidence utilization change with multimodal reasoning length after controlling for sequence position, total context length, output format, visual-token count, and inference compute?**

   - **Why it survived the antithesis scan:** Broad visual-utilization failure is occupied, but I did not identify a verified study testing this exact controlled relationship between reasoning length and visual use.
   - **Closest known work:** [Seeing or Knowing? Visual Context Sensitivity](https://www.alphaxiv.org/abs/2607.26326); [VIG](https://www.alphaxiv.org/abs/2608.21883).
   - **Unresolved issue:** Whether apparent visual “drift” represents real loss of visual influence or merely changing attention geometry.
   - **Main confound:** Sequence position, length normalization, and output-format effects.
   - **Why the negative result matters:** It could show that a prominent visual-drift explanation is an artifact and clarify how visual evidence should be measured.
2. **Are visual binding mechanisms stable across model architectures, object layouts, attributes, and natural-image counterfactuals?**

   - **Why it survived the antithesis scan:** Direct binding mechanisms are occupied, but systematic cross-model causal validation remains insufficiently established.
   - **Closest known work:** [Investigating Mechanisms for In-Context Vision Language Binding](https://openaccess.thecvf.com/content/CVPR2025W/MIV/papers/Saravanan_Investigating_Mechanisms_for_In-Context_Vision_Language_Binding_CVPR2025_paper.pdf); Visual Symbolic Mechanisms; [Circuit Tracing](https://www.alphaxiv.org/abs/2602.20330).
   - **Unresolved issue:** Whether binding-ID-like or symbolic stages are general mechanisms or task/model-specific representations.
   - **Main confound:** Synthetic layouts, image-edit artifacts, object salience, and language priors.
   - **Why the negative result matters:** Failure to reproduce the mechanism would substantially constrain claims about mechanistic binding and improve interpretation of compositional benchmarks.
3. **Can intermediate representations predict whether multimodal task mappings will transfer from demonstrations to the query in natural-image ICL?**

   - **Why it survived the antithesis scan:** Task-mapping construction and transfer are already identified as separate processes, but their predictive diagnostics and cross-model generality remain unclear.
   - **Closest known work:** [Why Multimodal In-Context Learning Lags Behind?](https://www.alphaxiv.org/abs/2604.13403); [Dissecting Multimodal In-Context Learning](https://www.alphaxiv.org/abs/2601.20796).
   - **Unresolved issue:** Whether a representation-level transfer score predicts genuine task induction rather than query similarity or label copying.
   - **Main confound:** Textual demonstration information and semantic retrieval.
   - **Why the negative result matters:** It could show that current task-mapping probes are non-predictive and that apparent multimodal ICL mechanisms do not transfer beyond controlled settings.
