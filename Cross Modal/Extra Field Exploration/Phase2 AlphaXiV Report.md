
# Phase 2 — Deep Research, Gap Autopsy & Experimental Protocol Validation

## 1. Executive Summary

**Q1 does not survive in its original form.** The claim that visual grounding weakens during long multimodal reasoning is now directly occupied by recent work, including [Remember-R1: Mitigating Long-Context Visual Forgetting](https://www.alphaxiv.org/abs/2608.01314) and [ReGround: Restoring Visual Grounding in Multi-Step Reasoning](https://www.alphaxiv.org/abs/2608.04385). [VIG](https://www.alphaxiv.org/abs/2608.21883) also reports that visual information density decreases as reasoning chains become longer. These papers do not fully resolve every position, length, and normalization confound, but they substantially pre-empt the broad phenomenon.

A narrower Q1 question remains defensible:

> **At matched generation positions and matched textual-prefix lengths, does the causal effect of image evidence on the next-token distribution decline over a reasoning trajectory?**

This is importantly different from simply measuring attention decline. It treats reasoning length as a conditional analysis variable and measures image dependence through counterfactual image removal or replacement. The original claim—“visual utilization degrades causally as a function of trace length”—is too strong because generated length is endogenous: difficult examples naturally produce longer traces, and the model’s own reasoning content changes the hidden state.

The original four-arm Q1 design is therefore rejected. “Semantic-neutral padding” is not genuinely neutral in an autoregressive transformer, and repeated visual-token injection changes token positions, rotary embeddings, attention patterns, KV-cache structure, and possibly the model’s distribution. It can test whether visual re-presentation helps, but not cleanly prove why it helps.

**Q2 survives only with modification.** The two anchor papers do establish causal binding-like behavior, but they study highly controlled synthetic scenes. [Investigating Mechanisms for In-Context Vision Language Binding](https://openaccess.thecvf.com/content/CVPR2025W/MIV/papers/Saravanan_Investigating_Mechanisms_for_In-Context_Vision_Language_Binding_CVPRW_2025_paper.pdf) uses a Blender-generated Shapes task and LLaVA-OneVision-7B. [Uncovering Grounding IDs](https://www.alphaxiv.org/abs/2509.24072) uses symbol-partitioned synthetic scenes, primarily Qwen2.5-VL-7B, and also reports smaller-model and InternVL3.5 results. Neither demonstrates transfer to ordinary natural photographs.

However, “universal, architecture-independent Binding IDs” is too ambitious. The existing evidence suggests at least three distinct phenomena: entity-binding vectors, symbol-induced grounding identifiers, and partition-specific visual-textual routing. These should not be assumed to be the same mechanism.

The defensible Q2 formulation is:

> **Do causal activation-swap effects found in controlled synthetic visual-binding tasks persist under progressively more natural visual variation, while preserving specificity for the intended object–attribute relation?**

This is narrower than claiming universal Binding IDs. It also allows a scientifically meaningful negative result: the representation may be causal in synthetic scenes but fail to transfer to natural images.

For Q1, the strongest remaining contribution is a **measurement and causal-control study** rather than discovery of visual forgetting itself. For Q2, the strongest remaining contribution is a **transfer and specificity study** rather than discovery of Binding IDs.

Both directions are technically possible in principle with open-weight models, but not symmetrically. Q1 can be performed with inference and hidden-state/logit extraction on a small model. Q2 requires locating image-token regions, aligning source and target activations, and verifying that patching does not corrupt unrelated computation. Q2 is therefore substantially more fragile.

The main practical conclusion is:

- **Q1: SURVIVES WITH MODIFICATION**, but only as a controlled causal measurement question.
- **Q2: SURVIVES WITH MODIFICATION**, but only as a synthetic-to-natural-transfer and specificity question.
- Neither should proceed to Phase 3 without a runtime pre-flight test.
- Q2 has higher mechanistic novelty potential but higher implementation and dataset risk.
- Q1 is easier to execute but has greater pre-emption risk.

## 2. Four Paper Autopsies

### A1 — [Seeing or Knowing? Visual Context Sensitivity in Multimodal Large Language Models](https://www.alphaxiv.org/abs/2607.26326)

Authors: Jiaang Li, Chengzu Li, Zhaochong An, Yifei Yuan, Xi Liu, Serge Belongie, and Vésteinn Snæbjarnarson. arXiv version 2 dated August 25, 2026.

| Category                 | Evidence                                                                                                                                                                                                                                                                                         |
| ------------------------ | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------ |
| Exact research question  | Does an MLLM fail because visual evidence is not preserved, or because it is preserved but used unreliably relative to the language prior? The paper explicitly distinguishes perception failure from utilization failure.[Research hypotheses](https://www.alphaxiv.org/abs/2607.26326v2?page=2) |
| Mechanism                | Vision-versus-prior conflict and controllable visual-context sensitivity.                                                                                                                                                                                                                        |
| Models                   | Qwen2.5-VL-3B/7B, Qwen3.5-4B/9B, and Gemma-4-E2B/E4B are listed in the implementation appendix. The main study covers six model/checkpoint combinations.[Model set](https://www.alphaxiv.org/abs/2607.26326v2?page=8)                                                                             |
| Dataset                  | WhatIfVis: 3,049 manually inspected counterfactual samples across Spatial/Temporal, Color, Count, Size, and Weight.[WhatIfVis composition](https://www.alphaxiv.org/abs/2607.26326v2?page=20)                                                                                                     |
| Experimental unit        | A paired question/evidence example with two possible answers: one following visual context and one following prior knowledge.                                                                                                                                                                    |
| Prompts                  | “Consider only the image” versus “Ignore the image” for visual context; matched textual statements for the text channel.[Prompt conditions](https://www.alphaxiv.org/abs/2607.26326v2?page=6)                                                                                                 |
| Decoding                 | Greedy decoding for exact-match evaluation; probability scoring compares the likelihoods of the context and prior answer candidates.[Metrics](https://www.alphaxiv.org/abs/2607.26326v2?page=7)                                                                                                   |
| Visual-context metric    | PairAcc requires both correct context-following and correct prior-following on the same example. The probability version compares candidate-answer likelihoods rather than decoded strings.                                                                                                      |
| Representation           | Final-layer image tokens for reconstruction; residual-stream activation at the final token for patching and steering.                                                                                                                                                                            |
| Reconstruction procedure | A learned reconstruction system attempts to reconstruct image content from final-layer image tokens. The models use 256 image tokens and a six-layer connector in the appendix.[Reconstruction setup](https://www.alphaxiv.org/abs/2607.26326v2?page=20)                                          |
| Main finding             | Coarse visual attributes remain recoverable from final-layer image tokens, while model utilization of those attributes is unstable.[Main result](https://www.alphaxiv.org/abs/2607.26326v2?page=4)                                                                                                |
| Causal intervention      | Activation patching localizes a vision-versus-prior decision to architecture-specific layer bands. A learned one-dimensional residual-space direction is then used to steer visual-context sensitivity.                                                                                          |
| Layer findings           | Representative layer bands include Qwen3.5-9B L13–18 and L14–21, and Gemma-4-E4B L20–25 and L20–27. The full set is model-specific.[Layer localization](https://www.alphaxiv.org/abs/2607.26326v2?page=9)                                                                                     |
| Control                  | Random rank-1 steering vectors perform substantially worse than learned vectors; this tests whether the learned direction is specific rather than merely an arbitrary rank-1 perturbation.[Random-vector control](https://www.alphaxiv.org/abs/2607.26326v2?page=22)                              |
| Sample sizes             | WhatIfVis contains 3,049 examples; Spatial/Temporal contains 1,537, Color 282, Count 390, Size 773, and Weight 67. The paper also reports 50-sample reconstruction analyses for some attributes.[Dataset counts](https://www.alphaxiv.org/abs/2607.26326v2?page=20)                               |
| Main limitation          | The benchmark excludes intermediate reasoning traces and focuses mainly on coarse attributes. Count and Weight require additional reasoning and remain difficult.[Limitations](https://www.alphaxiv.org/abs/2607.26326v2?page=19)                                                                 |
| Code                     | The paper identifies a code project as`visual-context-sensitivity` on page 1. The exact repository URL was not independently verified here. **VERIFIED as a paper-listed code name; URL UNKNOWN.**                                                                                       |
| Data                     | Dataset composition and source datasets are described in Appendix B; direct downloadable dataset URL was not verified here.**UNKNOWN for runtime accessibility.**                                                                                                                          |
| Reproduction difficulty  | Moderate for probability-based PairAcc; high for reconstruction and activation steering.                                                                                                                                                                                                         |
| Relevance to Q1          | It directly establishes visual utilization as a real phenomenon, but does not test utilization as a function of generated CoT length.                                                                                                                                                            |

The important distinction is that this paper studies **whether visual information is available and controllable**, not whether its causal influence declines with reasoning-trace length. Its benchmark explicitly excludes intermediate reasoning traces. [Scope limitation](https://www.alphaxiv.org/abs/2607.26326v2?page=19)

### A2 — [VIG: Visual Information Gain as a Reward Signal for Multimodal Chain-of-Thought Compression](https://www.alphaxiv.org/abs/2608.21883)

Authors: Wen Luo, Xiaohan Yi, Xiaotao Huang, and Liqun Huang. arXiv version 2 dated August 27, 2026.

| Category                                 | Evidence                                                                                                                                                                                                                                                      |
| ---------------------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| Exact research question                  | Can multimodal CoT be compressed by rewarding reasoning tokens whose predictive distributions depend on the image?                                                                                                                                            |
| Mechanism                                | Per-token visual information gain, defined as the reduction in next-token entropy caused by including the image.                                                                                                                                              |
| Model                                    | Qwen3-VL-2B-Thinking, 4B-Thinking, and 8B-Thinking.                                                                                                                                                                                                           |
| Dataset                                  | Training mixture: 2,948 examples from MMStar, MathVista, and LogicVista. Evaluation includes WeMath, MMMU, MathVision, DynaMath, MMK12, Geo3K, and R1-Onevision-Bench.[Datasets](https://www.alphaxiv.org/abs/2608.21883v2?page=13)                            |
| Exact VIG formula                        | For token$t_\tau$, $VIG(t_\tau)=H_{\mathrm{txt}}(t_\tau)-H_{\mathrm{vis}}(t_\tau)$, where the first distribution is generated without visual tokens and the second with the image. [VIG definition](https://www.alphaxiv.org/abs/2608.21883v2?page=5)      |
| Sequence reward                          | The mean VIG over the`<think>` block is clipped to $[-1,1]$: $R_{\mathrm{VIG}}=\operatorname{clip}(\frac{1}{|T|}\sum_{t\in T}VIG(t),-1,1)$. [Sequence reward](https://www.alphaxiv.org/abs/2608.21883v2?page=5)                                          |
| Training                                 | Full-parameter GRPO, group size 8, batch size 1 per device, gradient accumulation 4, learning rate$10^{-6}$, up to 500 steps, DeepSpeed ZeRO-2. [Training setup](https://www.alphaxiv.org/abs/2608.21883v2?page=14)                                          |
| Inference/reward computation             | Two forward passes over the same generated chain: one with visual tokens and one with the visual span removed.[Two-pass algorithm](https://www.alphaxiv.org/abs/2608.21883v2?page=12)                                                                          |
| Main result                              | On Qwen3-VL-8B-Thinking, VIG reaches 64.92 average accuracy and 1,524 average reasoning tokens, versus 62.55 accuracy and 1,921 tokens for ThinkPrune.[Main result](https://www.alphaxiv.org/abs/2608.21883v2?page=7)                                          |
| Length relationship                      | On 1,740 WeMath generations, average VIG decreases with chain length, Pearson$r=-0.569$, $p<0.001$. [Length correlation](https://www.alphaxiv.org/abs/2608.21883v2?page=8)                                                                                 |
| Causality                                | The authors call the correlation descriptive and attribute causal evidence to reward ablations. The paper does not establish that longer reasoning itself causes lower visual dependence.[Causal limitation](https://www.alphaxiv.org/abs/2608.21883v2?page=9) |
| Controls                                 | No-VIG GRPO, confidence-only reward$-H_{\mathrm{vis}}$, masked-image comparison, reward-weight sweep, stratification by text-solvable versus vision-required items, and deletion probes.                                                                    |
| Important limitation                     | VIG measures visual dependence, not visual correctness or causal necessity. A hallucinated visual reading can obtain high VIG.[Metric limitation](https://www.alphaxiv.org/abs/2608.21883v2?page=9)                                                            |
| Strong counterevidence to naïve pruning | Deleting low-VIG sentences can be more damaging than deleting high-VIG sentences because low-VIG algebraic steps may be computationally load-bearing.[Deletion probe](https://www.alphaxiv.org/abs/2608.21883v2?page=15)                                       |
| Compute                                  | On 8×H20, VIG training took 41.3 GPU-hours versus 35.3 for GRPO, a 1.17× overhead.[Training cost](https://www.alphaxiv.org/abs/2608.21883v2?page=16)                                                                                                         |
| Code                                     | GitHub URL is provided in the paper:`https://github.com/chaser682/vig`.                                                                                                                                                                                     |
| Data                                     | The paper reports public evaluation datasets and gives licensing descriptions, but each dataset’s live download path should still be checked before use.[Dataset licensing](https://www.alphaxiv.org/abs/2608.21883v2?page=17)                                |
| Reproduction difficulty                  | High for GRPO training; moderate for inference-only VIG measurement.                                                                                                                                                                                          |
| Relevance to Q1                          | Directly occupies the length–visual-dependence association, but not the proposed matched-control causal test.                                                                                                                                                |

VIG is the most important pre-emption for Q1. It reports the exact descriptive pattern the question anticipated: longer chains have lower average visual information gain. However, the paper itself explicitly treats this as descriptive, and its measure is an image-versus-no-image entropy contrast—not a causal intervention on reasoning length.

VIG also reveals a serious measurement problem: image dependence is not equivalent to correct visual grounding. The authors explicitly show a failure where high VIG accompanies an incorrect visual reading. [High-VIG failure](https://www.alphaxiv.org/abs/2608.21883v2?page=17)

### C1 — [Uncovering Grounding IDs: How External Cues Shape Multimodal Binding](https://www.alphaxiv.org/abs/2509.24072)

Authors: Hosein Hasani, Amirmohammad Izadi, Fatemeh Askari, Mobin Bagherian, Sadegh Mohammadian, Mohammad Izadi, and Mahdieh Soleymani Baghshah. The retrieved version is v4 dated February 25, 2026.

| Category                  | Evidence                                                                                                                                                                                                                                                                                               |
| ------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------ |
| Exact research question   | Why do external image/text cues—symbols and partition lines—improve visual-textual grounding?                                                                                                                                                                                                        |
| Mechanism                 | “Grounding IDs”: partition-specific identifiers induced by shared external symbols in the image and prompt.                                                                                                                                                                                          |
| Main model                | Qwen2.5-VL-7B without fine-tuning for the principal causal analysis.                                                                                                                                                                                                                                   |
| Additional models         | Qwen2.5-VL-3B and InternVL3.5-8B in Appendix N.                                                                                                                                                                                                                                                        |
| Dataset                   | Synthetic images with rows, symbols, and geometric objects. The main causal appendix uses 100 scenes, each with four rows, one symbol, and one object per row.[Synthetic data](https://www.alphaxiv.org/abs/2509.24072v4?page=20)                                                                       |
| Scene contents            | Four distinct shapes, eight colors selected from a nine-color palette, one unique shape–color pair per row.                                                                                                                                                                                           |
| Main structured dataset   | Scene-description images with 15 unique objects from 35 shape–color combinations; objects occupy one 28×28 patch and do not cross adjacent patches.[Scene data](https://www.alphaxiv.org/abs/2509.24072v4?page=3)                                                                                     |
| Representation            | Residual-stream hidden activations at visual patch and text-token positions.                                                                                                                                                                                                                           |
| Layer analysis            | Cross-modal alignment increases especially at layers 22–27 in Qwen2.5-VL. Causal swap effects emerge in late layers 20–27, while head-level signal is highlighted around layer 16.[Layer analysis](https://www.alphaxiv.org/abs/2509.24072v4?page=6)                                                  |
| Intervention              | Object-image-token activation swapping between source and target contexts. The image-token mask is derived from object bounding boxes and dilated by one token. Text symbol tokens and symbol-glyph image tokens are not swapped.[Swap intervention](https://www.alphaxiv.org/abs/2509.24072v4?page=20) |
| Metric                    | Swap accuracy: whether the post-swap answer follows the source-bound symbol–object relation rather than the host image’s local object.                                                                                                                                                               |
| Main causal finding       | On Qwen2.5-VL-7B, standard accuracy after swapping falls to 0.02, while accuracy measured against the transferred binding is 0.98.[Swap result](https://www.alphaxiv.org/abs/2509.24072v4?page=5)                                                                                                       |
| Disjoint-symbol control   | Source symbols and target symbols are non-overlapping; querying absent source symbols tests whether binding is carried by patched object activations rather than local symbol tokens.                                                                                                                  |
| Alternative-model results | InternVL3.5-8B swap accuracy: 0.75 shape and 0.82 color; Qwen2.5-VL-3B: 0.93 shape and 0.73 color.[Alternative models](https://www.alphaxiv.org/abs/2509.24072v4?page=21)                                                                                                                               |
| Random-vector control     | **Not clearly reported as a random-vector placebo for the Grounding-ID swap.** The paper uses disjoint-symbol and object-only controls, but the requested random-vector control is not verified in the retrieved appendix.                                                                       |
| Natural-image experiment  | The paper reports MS-COCO hallucination experiments with structured cues, but the causal Grounding-ID swap itself remains synthetic.[Natural-image scope](https://www.alphaxiv.org/abs/2509.24072v4?page=21)                                                                                            |
| Code/data                 | No independently verified official code or dataset repository was located in the retrieved paper.**UNKNOWN.**                                                                                                                                                                                    |
| Reproduction difficulty   | Moderate for synthetic Qwen2.5-VL-3B; high for 7B and cross-model activation swapping; natural-image extension is high.                                                                                                                                                                                |

The paper’s strongest result is causal, but the mechanism is more specific than “universal Binding ID.” Its Grounding IDs are explicitly induced by external symbols and partitions. The paper itself contrasts them with prior Binding IDs and suggests they may be closer to lexical binding than context-independent entity binding. [Mechanism distinction](https://www.alphaxiv.org/abs/2509.24072v4?page=6)

### C2 — [Investigating Mechanisms for In-Context Vision Language Binding](https://openaccess.thecvf.com/content/CVPR2025W/MIV/papers/Saravanan_Investigating_Mechanisms_for_In-Context_Vision_Language_Binding_CVPRW_2025_paper.pdf)

Authors: Darshana Saravanan, Makarand Tapaswi, and Vineet Gandhi. arXiv:2505.22200, May 28, 2025; CVPR 2025 workshop paper.

| Category                | Evidence                                                                                                                                                                                                                                                           |
| ----------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------ |
| Exact research question | Do VLMs use Binding-ID-like latent vectors to associate visual objects with textual references and attributes?                                                                                                                                                     |
| Mechanism               | Factorized object, color, and item representations containing content vectors plus binding vectors.                                                                                                                                                                |
| Model                   | LLaVA-OneVision-7B with SigLIP vision encoder.                                                                                                                                                                                                                     |
| Dataset                 | Blender-generated Shapes task with two 3D objects, distinct colors and shapes, textual references, and arbitrary item labels.                                                                                                                                      |
| Scene vocabulary        | Four shapes, six colors, randomly selected uppercase item letters for the main task.                                                                                                                                                                               |
| Representation          | Residual-stream activations$Z^p\in\mathbb{R}^{L\times D}$ at visual object patch, color-token, and item-token positions. [Representation notation](https://www.alphaxiv.org/abs/2505.22200v1?page=2)                                                              |
| Proposed factorization  | $Z^O_k=f^O(O_k)+b^O(k)$, with analogous terms for colors and items.                                                                                                                                                                                              |
| Intervention            | Cache activations from two samples and replace object, item, or color activation blocks.                                                                                                                                                                           |
| Factorizability result  | Replacing object activations transfers object–item association; replacing item activations changes the queried item; color activation replacement does not change the object–item association.[Factorizability](https://www.alphaxiv.org/abs/2505.22200v1?page=3) |
| Position control        | Object, item, and color activations are progressively shifted and swapped. The association remains stable under position changes.                                                                                                                                  |
| Mean intervention       | Binding-vector differences are approximated by mean activation differences across samples, then added/subtracted to object or item activations.                                                                                                                    |
| Metric                  | Fraction of samples where the correct item has the highest log probability among candidate items.                                                                                                                                                                  |
| Random-vector control   | Random vectors with matched magnitude do not alter the binding response, while mean intervention vectors do.[Random control](https://www.alphaxiv.org/abs/2505.22200v1?page=4)                                                                                      |
| Layers                  | The paper defines activations across all model layers but does not report a single universal Binding-ID layer in the main text. Exact layer-specific localization is therefore**UNKNOWN** from the retrieved paper.                                          |
| Natural images          | No natural photographic transfer experiment is reported. The task is synthetic and controlled.                                                                                                                                                                     |
| Sample size             | Exact number of generated training/evaluation samples is not reported in the retrieved main text.**UNKNOWN.**                                                                                                                                                |
| Controls                | Object/item/color replacement, position independence, random-vector interventions, and token-padding around object patches.                                                                                                                                        |
| Reproduction details    | Images are 384×384; each object appears in two crops and occupies 5×5 patch tokens; three-token padding was empirically used for object-token intervention.[Implementation details](https://www.alphaxiv.org/abs/2505.22200v1?page=4)                             |
| Code/data               | No official repository or data-release URL is supplied in the retrieved paper.**UNKNOWN.**                                                                                                                                                                   |
| Reproduction difficulty | High on LLaVA-OneVision-7B; moderate if adapted to a smaller model and synthetic task.                                                                                                                                                                             |
| Relevance to Q2         | Directly establishes synthetic causal binding, but provides no evidence for natural-image transfer or architecture independence.                                                                                                                                   |

The paper supports causal binding in a highly controlled setting, but its conclusions should not be generalized to ordinary photographs. The images have fixed object positions, controlled shapes and colors, and explicit object-to-patch correspondence. That is precisely why it is useful as a replication baseline—and precisely why it does not answer Q2.

## 3. Q1 Gap Autopsy

### 3.1 Terminology substitution

The proposed phrase “visual evidence utilization degradation” appears under several labels:

- visual forgetting;
- visual grounding decay;
- visual attention decay;
- visual evidence persistence;
- declining image–text mutual information;
- visual information density;
- visual re-examination;
- visual re-focusing;
- long-context visual forgetting;
- visual relay windows;
- attention sinks;
- take-along visual conditioning.

The terminology substitution search found substantial direct overlap.

### 3.2 Q1 antithesis classification

| Question                                                                                        | Classification                                  | Evidence                                                                                                                                                                                                                                                                                           |
| ----------------------------------------------------------------------------------------------- | ----------------------------------------------- | -------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| **Q1-A:** Does visual evidence utilization decline as generated reasoning becomes longer? | **DIRECTLY TESTED**                       | [Remember-R1](https://www.alphaxiv.org/abs/2608.01314) defines early-to-late visual attention decline during reasoning; [ReGround](https://www.alphaxiv.org/abs/2608.04385) reports visual-grounding decay; [VIG](https://www.alphaxiv.org/abs/2608.21883) reports lower VIG at longer chain lengths. |
| **Q1-B:** Does the decline survive sequence-position controls?                            | **NOT FOUND** in the retrieved literature | Existing studies analyze attention by decoding step or reasoning length but do not establish a complete position-matched causal control.                                                                                                                                                           |
| **Q1-C:** Does it survive context-length controls?                                        | **PARTIALLY TESTED**                      | Papers compare long and short reasoning or image re-injection, but the exact neutral-context-length control is not established.                                                                                                                                                                    |
| **Q1-D:** Does it survive attention-normalization controls?                               | **NOT FOUND**                             | Existing studies use attention ratios or entropy; they acknowledge proxy limitations but do not provide the complete proposed normalization audit.                                                                                                                                                 |
| **Q1-E:** Does it survive content-matched or length-matched textual controls?             | **PARTIALLY TESTED**                      | [ReGround](https://www.alphaxiv.org/abs/2608.04385) compares text-only reflection with visual re-injection, but this is not a neutral length-matched control.                                                                                                                                       |
| **Q1-F:** Can visual utilization be causally restored by additional visual information?   | **DIRECTLY TESTED**                       | ReGround re-injects the image and measures recovery; earlier visual re-introduction and Look-Back-style methods also address this. ReGround reports entropy recovery after re-injection in 94.4% of 2,510 samples.[Re-injection evidence](https://www.alphaxiv.org/abs/2608.04385v1?page=1)         |
| **Q1-G:** Has the proposed experiment already been performed under another name?          | **DIRECTLY/PARTIALLY TESTED**             | The broad experiment has been performed as visual forgetting, visual grounding decay, visual information density, and visual re-examination. The exact fully controlled causal estimand remains not found.                                                                                         |

### 3.3 Important pre-emption papers

#### [Remember-R1](https://www.alphaxiv.org/abs/2608.01314)

Remember-R1 explicitly studies “long-context visual forgetting.” It defines visual attention mass $\Omega(t)$ and measures early-to-late decline:

$$
\Delta_{\mathrm{vis}}
=
\mathbb{E}_{t\in T_{\mathrm{early}}}[\Omega(t)]
-
\mathbb{E}_{t\in T_{\mathrm{late}}}[\Omega(t)].
$$

The paper uses Qwen2.5-VL-3B and reports improvements from rewards for visual-keyword coverage, later-step visual persistence, and question-relevant regions. [Visual forgetting metric](https://www.alphaxiv.org/abs/2608.01314v1?page=3)

It therefore directly occupies Q1-A and Q1-F. However, its principal mechanism measurement remains attention-based and the paper does not show that attention is a causal measure of visual evidence use.

#### [ReGround](https://www.alphaxiv.org/abs/2608.04385)

ReGround analyzes 2,510 samples from four benchmarks and reports that attention entropy over image tokens typically narrows during the first reasoning round and rebounds after image re-injection. The paper explicitly labels entropy as a proxy, not a direct grounding measure. [Proxy limitation](https://www.alphaxiv.org/abs/2608.04385v1?page=8)

The paper’s controlled ablation is valuable:

- CoT-only SFT;
- text-only second-round reflection;
- visual second-round re-injection;
- visual re-injection plus GRPO.

Visual second-round reasoning outperforms text-only reflection on MathVista, MathVision, and HallusionBench. [Mechanism ablation](https://www.alphaxiv.org/abs/2608.04385v1?page=7)

This directly occupies visual-evidence restoration. It does not answer whether the original decline survives exact position and context-length controls.

#### [VIG](https://www.alphaxiv.org/abs/2608.21883)

VIG reports a significant negative correlation between chain length and average per-token visual information gain. However, the paper explicitly calls this descriptive and acknowledges that VIG is not visual correctness or indispensability. [Scope of result](https://www.alphaxiv.org/abs/2608.21883v2?page=15)

### 3.4 Q1 conclusion

The original Q1:

> Does visual evidence utilization degrade as a causal function of multimodal reasoning trace length?

is **too close to existing work** and **not causally identified by the proposed design**.

The modified Q1:

> At matched generation positions and matched textual-prefix lengths, does the image-conditioned causal effect on next-token predictions decline over a reasoning trajectory?

remains distinct enough for Phase 3, provided it is presented as a measurement study rather than a discovery claim.

## 4. Q2 Gap Autopsy

### 4.1 Terminology substitution

“Binding IDs” may be described as:

- entity-binding vectors;
- grounding identifiers;
- lexical binding;
- object–attribute binding;
- visual-language binding;
- symbolic indexing;
- spatial indices;
- object-centric routing;
- cross-modal referential consistency;
- activation-mediated binding;
- compositional grounding;
- relation binding;
- latent world-state variables.

The search confirms that the mechanism family is active and fragmented.

### 4.2 Q2 antithesis classification

| Question                                                                              | Classification                                        | Evidence                                                                                                                                                |
| ------------------------------------------------------------------------------------- | ----------------------------------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------- |
| **Q2-A:** Do synthetic binding representations transfer to natural photographs? | **NOT FOUND** as a direct causal transfer study | The retrieved anchor papers remain synthetic for their activation-swap experiments.                                                                     |
| **Q2-B:** Do they transfer across object appearances?                           | **PARTIALLY TESTED**                            | C1 varies shapes/colors and evaluates Qwen2.5-VL-3B and InternVL3.5, but still in synthetic scenes. C2 uses held-out shapes/colors but not photographs. |
| **Q2-C:** Do they survive background clutter?                                   | **NOT FOUND**                                   | No verified causal swap study tests cluttered natural backgrounds.                                                                                      |
| **Q2-D:** Do they survive different composition?                                | **PARTIALLY TESTED**                            | C1 varies row arrangements and symbol assignments, but the composition remains a partitioned synthetic layout.                                          |
| **Q2-E:** Do they transfer across architectures?                                | **PARTIALLY TESTED**                            | C1 reports Qwen2.5-VL-3B, Qwen2.5-VL-7B, and InternVL3.5-8B, but all are evaluated on the same synthetic causal task. C2 uses only LLaVA-OneVision-7B.  |
| **Q2-F:** Are they causally involved in binding?                                | **DIRECTLY TESTED**                             | Both C1 and C2 use activation interventions and report binding changes.                                                                                 |
| **Q2-G:** Can activation swapping change binding behavior?                      | **DIRECTLY TESTED**                             | C1 reports 0.98 transferred-binding accuracy on its main causal setting; C2 reports object/item activation swaps change binding.                        |
| **Q2-H:** Has the phenomenon been studied under another name?                   | **DIRECTLY/PARTIALLY TESTED**                   | Entity tracking, symbolic visual mechanisms, grounding IDs, object-centric representations, and visual-semantic circuit tracing all overlap.            |

### 4.3 New 2026 related work

[EditCLEVR: A Paired-Scene Intervention Benchmark for Compositional Faithfulness of Object-Centric Representations](https://www.alphaxiv.org/abs/2607.22705) is relevant to the evaluation problem. It suggests that paired-scene interventions and compositional faithfulness are becoming an explicit benchmark direction. It does not, from the available discovery record, establish that VLM Binding IDs transfer to natural photographs.

[Grounding Isn&#39;t Knowing: Do VLMs Need Object Localization for Spatial Reasoning?](https://www.alphaxiv.org/abs/2608.23074) is relevant to the distinction between localization and reasoning. It is not a direct Binding-ID transfer study, but it reinforces the need not to equate object localization or attention with binding.

[Dual-Pathway Circuits of Object Hallucination in Vision-Language Models](https://www.alphaxiv.org/abs/2605.13156) is mechanistically adjacent to Q2 because it studies separate visual and linguistic routes in object hallucination. It may pre-empt broad claims that one binding mechanism explains all compositional failures, but it does not directly test synthetic-to-natural Binding-ID transfer.

### 4.4 Q2 conclusion

The original Q2:

> Are latent visual Binding IDs universal, architecture-independent mechanisms?

is **not appropriately formulated**. “Universal” and “architecture-independent” require a much larger model and task family than a BSc project can establish.

The modified Q2:

> Do causal activation-swap effects found in controlled synthetic binding tasks persist under progressively more natural visual variation, and are they specific to the intended object–attribute relation?

is defensible. It does not require claiming universality. It tests transfer, specificity, and causal stability.

## 5. 2026 Pre-Emption Scan

### Q1 pre-emption result

**Answer:** Yes, the broad phenomenon has already been tested. No, I did not identify a paper that fully performs the exact proposed sequence-position, context-length, attention-normalization, and content-matched causal control in one design.

| Paper                                                                          | What it tests                                                                                 | Overlap with Q1                            |
| ------------------------------------------------------------------------------ | --------------------------------------------------------------------------------------------- | ------------------------------------------ |
| [Remember-R1](https://www.alphaxiv.org/abs/2608.01314)                          | Early-to-late visual attention decline during generated reasoning; rewards visual persistence | Direct mechanism and phenomenon overlap    |
| [ReGround](https://www.alphaxiv.org/abs/2608.04385)                             | Attention entropy narrowing during reasoning and recovery after image re-injection            | Direct phenomenon and restoration overlap  |
| [VIG](https://www.alphaxiv.org/abs/2608.21883)                                  | Per-token visual information gain decreases with chain length                                 | Direct length–visual-dependence overlap   |
| [The Ebb and Flow of Multimodal Focus](https://www.alphaxiv.org/abs/2607.11436) | Visual relay-window scheduling during reasoning                                               | Direct intervention and scheduling overlap |
| Position Rebinding Cache Reuse                                                 | Replaying/revisiting visual evidence at new positions                                         | Mechanistic overlap with re-presentation   |
| [Look Light, Think Heavy](https://www.alphaxiv.org/abs/2606.22565)              | What multimodal CoT can and cannot do                                                         | Broad reasoning overlap                    |

The unresolved scientific difference is therefore **not the existence of visual forgetting**. It is whether current evidence survives a causal measurement audit.

### Q2 pre-emption result

**Answer:** I did not identify a paper that directly tests whether synthetic Binding/Grounding IDs transfer causally to natural photographic scenes.

The nearest papers are:

| Paper                                                                                                                                                                                                                       |                                       Natural images? |          Causal activation swap? | Overlap                                                     |
| --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | ----------------------------------------------------: | -------------------------------: | ----------------------------------------------------------- |
| [Investigating Mechanisms for In-Context Vision Language Binding](https://openaccess.thecvf.com/content/CVPR2025W/MIV/papers/Saravanan_Investigating_Mechanisms_for_In-Context_Vision_Language_Binding_CVPRW_2025_paper.pdf) |                                                    No |                              Yes | Synthetic causal baseline                                   |
| [Uncovering Grounding IDs](https://www.alphaxiv.org/abs/2509.24072)                                                                                                                                                          | MS-COCO for hallucination evaluation, not causal swap |          Yes on synthetic scenes | Strongest closest work                                      |
| Visual Symbolic Mechanisms                                                                                                                                                                                                  |                                   Primarily synthetic |     Mechanistic/circuit evidence | Adjacent symbolic-binding mechanism                         |
| [Circuit Tracing in Vision–Language Models](https://www.alphaxiv.org/abs/2602.20330)                                                                                                                                        |     ImageNet/Cauldron and internet-image case studies |    Feature steering and patching | General causal multimodal circuits, not Binding-ID transfer |
| [EditCLEVR](https://www.alphaxiv.org/abs/2607.22705)                                                                                                                                                                         |                              Controlled paired scenes | Intervention benchmark direction | Evaluation overlap, not the same mechanism                  |

The absence of a direct match is **NOT FOUND**, not proof of novelty.

## 6. Dataset Audit

### Q1 datasets

| Dataset    | Access status                                                                                                                                     | Suitability                                                                                                            | Main problem                                                     |
| ---------- | ------------------------------------------------------------------------------------------------------------------------------------------------- | ---------------------------------------------------------------------------------------------------------------------- | ---------------------------------------------------------------- |
| WhatIfVis  | Dataset composition is documented in[Seeing or Knowing?](https://www.alphaxiv.org/abs/2607.26326); direct live download path was not verified here | Strong for image-versus-prior sensitivity; not suitable for long CoT because it excludes intermediate reasoning traces | Small Weight subset and generated/counterfactual image artifacts |
| WeMath     | Public benchmark reported by[VIG](https://www.alphaxiv.org/abs/2608.21883); exact repository/license requires runtime verification                 | Good for visual math reasoning and paired trace analysis                                                               | Template, OCR, and mathematical prior shortcuts                  |
| MathVista  | Public benchmark; exact live access path/license not independently checked here                                                                   | Useful for visual reasoning                                                                                            | Many questions require external knowledge or OCR                 |
| MathVision | Public benchmark; runtime access not verified                                                                                                     | Useful for diagrams and visual math                                                                                    | Difficult items may produce very long traces and truncation      |
| LogicVista | Public benchmark; runtime access not verified                                                                                                     | Useful for multi-step visual logic                                                                                     | Synthetic/template effects                                       |
| MMStar     | Public benchmark; runtime access not verified                                                                                                     | Useful for image-text alignment                                                                                        | Broad capability mixture, not mechanism-isolating                |
| DynaMath   | Public benchmark; runtime access not verified                                                                                                     | Useful for robustness to visual perturbation                                                                           | May conflate reasoning robustness with visual utilization        |

For Q1, no dataset alone is sufficient. The core dataset should be a **paired subset** where the same image/question is run under multiple forced-prefix or decoding conditions.

### Q2 datasets

| Dataset                              | Access status                                                                     | Suitability                                      | Main problem                                                         |
| ------------------------------------ | --------------------------------------------------------------------------------- | ------------------------------------------------ | -------------------------------------------------------------------- |
| Blender/CLEVR-style synthetic scenes | Generator concept is verified from C2; exact released generator not verified      | Best for replication and causal swaps            | Synthetic geometry and fixed layouts                                 |
| C1 synthetic four-row scenes         | Exact generation protocol is documented in Appendix L; released data path unknown | Direct replication baseline                      | It tests partition binding, not ordinary object-attribute binding    |
| MS-COCO                              | Public dataset; exact license/access route not checked in this phase              | Natural-image source with object annotations     | Attribute annotations and object identity are incomplete for binding |
| SugarCrepe                           | Public benchmark in general; exact official access/license not verified here      | Compositional image-caption evaluation           | Caption/edit artifacts and no direct hidden-state swap target        |
| Winoground                           | Public benchmark in general; exact access path not verified here                  | Tests compositional image-caption distinction    | Very small and not designed for activation intervention              |
| WhatIfVis                            | Dataset source composition documented                                             | Counterfactual visual-prior conflict             | Does not provide object-level binding annotations                    |
| EditCLEVR                            | Discovery result indicates paired-scene intervention design                       | Potentially useful for controlled generalization | Natural-photo transfer is not established                            |

The main dataset problem for Q2 is not download availability. It is **semantic sufficiency**. Ordinary natural images often do not contain clean, unambiguous object–attribute pairs with controlled counterfactual alternatives. A photograph of a red object beside a blue object does not automatically provide a valid binding intervention unless object identity, attribute, and answer target are all annotated.

## 7. Model Architecture Audit

### Qwen2.5-VL-3B-Instruct

**VERIFIED from official Hugging Face documentation:**

- It is available as a 3B open-weight multimodal model.
- The family uses a vision encoder and language decoder.
- The vision encoder uses window attention optimizations.
- Hugging Face Transformers provides a Qwen2.5-VL implementation.
- The model supports image inputs and multimodal generation.

The official documentation confirms that the model exposes standard language-model-style configuration and forward-generation interfaces, but exact hidden size, number of decoder layers, visual-token count per image, and exact internal module names must be read from the installed checkpoint configuration. The retrieved sources do not justify inventing those values.

**Likely accessible:**

- final logits;
- hidden states when `output_hidden_states=True`;
- attention outputs when supported by the installed implementation;
- image-token positions through the processor’s image-grid metadata;
- forward hooks on decoder layers.

**Requires runtime verification:**

- exact image-token index mapping after dynamic resolution;
- whether attention tensors are returned for all layers and heads under the selected attention implementation;
- whether hidden-state replacement at image-token positions preserves shape and device compatibility;
- whether generation with modified cached states is supported without recomputing the entire sequence.

The official model page and Transformers implementation should be used rather than hard-coded module paths: [Qwen2.5-VL documentation](https://huggingface.co/docs/transformers/model_doc/qwen2_5_vl), [Qwen2.5-VL-3B-Instruct](https://huggingface.co/Qwen/Qwen2.5-VL-3B-Instruct).

### Gemma 3 4B IT

**VERIFIED from official documentation and the inspected multimodal circuit paper:**

- It uses a SigLIP-based vision encoder.
- Visual features are transformed into compact image or “soft” tokens.
- The language component uses hybrid local/global attention.
- The inspected Gemma-3-4B circuit paper reports a 34-layer decoder, hidden size 2,560, and 256 soft image tokens for its model configuration. [Gemma-3 architecture](https://www.alphaxiv.org/abs/2602.20330v1?page=5)
- It supports image-token hidden-state and attention analysis in the authors’ extended TransformersLens implementation, not necessarily out of the box.

The official Transformers documentation is [Gemma 3 model documentation](https://huggingface.co/docs/transformers/en/model_doc/gemma3).

**Important limitation:** The circuit-tracing paper required custom VLM support for TransformersLens and reported high compute. Therefore “the model exposes hidden states” does not imply that full causal circuit tracing is easy.

### Autoregressive intervention feasibility

- **Q1 image ablation:** technically straightforward in a teacher-forced forward pass: run the same prefix with the image and with the image removed or replaced.
- **Q1 attention extraction:** possible in principle but implementation-dependent.
- **Q1 intervention during generation:** difficult if the aim is to modify already-generated text without changing the generation process. Teacher-forced evaluation is cleaner.
- **Q2 activation swap:** possible in principle if source and target have identical architecture, token-grid shape, layer width, and compatible image-token indexing.
- **Q2 natural-image patching:** technically fragile because object regions may map to different numbers and locations of image tokens across images.
- **Random-vector placebo:** possible, but not sufficient by itself. A matched random vector controls direction only; it does not control norm, token position, distribution shift, or reconstruction error.

## 8. Q1 Causal Protocol

### 8.1 Validity of the original four-arm design

| Arm                             | Technical feasibility                                                                                        | Causal interpretation                                                                          | Decision                                                              |
| ------------------------------- | ------------------------------------------------------------------------------------------------------------ | ---------------------------------------------------------------------------------------------- | --------------------------------------------------------------------- |
| Zero-CoT/immediate answer       | Feasible                                                                                                     | Establishes baseline image effect without generated reasoning                                  | Retain as baseline                                                    |
| Natural extended reasoning      | Feasible for a thinking model; difficult with Qwen2.5-VL-3B-Instruct unless it naturally emits long traces   | Length is endogenous and correlated with difficulty                                            | Retain as observational condition only                                |
| Semantic-neutral padding        | Technically possible with forced prefixes, but no token sequence is semantically and computationally neutral | Padding changes position, hidden state, attention, and model distribution                      | Reject as primary causal arm                                          |
| Repeated visual-token injection | Possible only with architecture-specific multimodal input manipulation or re-encoding                        | Tests visual re-presentation, not pure length causality; changes positions and cache structure | Reject as Q1 causal arm; retain only as separate restoration ablation |

### 8.2 Revised research question

> **For the same image-question pair, does the image-conditioned causal effect on the next-token distribution decrease over matched reasoning-prefix positions, after controlling for prefix length, token position, answer format, and task difficulty?**

This is a conditional causal measurement question, not a claim that “length causes forgetting” in the interventionist sense.

### 8.3 Hypotheses

**H1:** The image-conditioned causal effect decreases at later matched reasoning positions, even after sequence-length and position controls.

**H0:** The apparent decline disappears after controls and is explained by position, prefix content, image-token dilution, or task difficulty.

### 8.4 Experimental unit

One image-question item evaluated under multiple teacher-forced prefixes generated from the same model and the same initial prompt.

A single item may produce measurements at positions $t_1,t_2,\ldots,t_k$.

### 8.5 Recommended measurement

The primary metric should not be raw attention.

Define a contrastive image causal effect for candidate answer tokens $a_c$ and $a_p$:

$$
\mathrm{ICE}_t
=
\left[
\log p(a_c\mid I,q,p_{<t})
-
\log p(a_p\mid I,q,p_{<t})
\right]
-
\left[
\log p(a_c\mid I',q,p_{<t})
-
\log p(a_p\mid I',q,p_{<t})
\right],
$$

where $I$ is the original image and $I'$ is an image-ablated or counterfactual image condition.

For non-binary answers, use a symmetric image-sensitivity measure over the full next-token distribution:

$$
\mathrm{JS}_t
=
\mathrm{JS}\!\left(
p_\theta(\cdot\mid I,q,p_{<t}),
p_\theta(\cdot\mid I',q,p_{<t})
\right).
$$

Interpretation:

- **ICE** measures whether the image changes the relative probability of the answer alternatives.
- **JS divergence** measures whether the image changes the entire next-token distribution.
- Neither proves that the model uses the image correctly.
- Correctness must be evaluated separately using counterfactual answer labels.

### 8.6 Candidate metrics

| Metric                       | Formula/definition                                                            | What it measures                             | What it does not measure         | Causal status                                            |
| ---------------------------- | ----------------------------------------------------------------------------- | -------------------------------------------- | -------------------------------- | -------------------------------------------------------- |
| Visual attention ratio       | $\sum_{j\in V}\alpha_{t,j}$                                                 | Allocation of attention mass to image tokens | Information use or correctness   | Correlational                                            |
| Image ablation logit effect  | Difference in logits with versus without image                                | Output sensitivity to image input            | Whether sensitivity is correct   | Causal relative to image removal                         |
| JS divergence                | Distributional divergence between image and ablated conditions                | Full next-token image dependence             | Correct grounding                | Causal input effect                                      |
| Counterfactual answer effect | Change in probability toward the correct answer under controlled image change | Correct use of visual evidence               | Internal mechanism location      | Causal behavioral effect                                 |
| Hidden-state distance        | $\|h_t(I)-h_t(I')\|$                                                        | Representation change caused by image        | Whether change affects answer    | Causal representation difference, not causal sufficiency |
| VIG                          | Entropy difference with versus without image                                  | Image-dependent uncertainty reduction        | Correctness and indispensability | Input-contrast measure, not intervention on length       |

**Primary metric:** paired counterfactual answer log-odds or JS divergence at matched positions.

**Secondary diagnostics:**

1. visual attention ratio;
2. VIG-style entropy contrast;
3. answer accuracy under image counterfactuals;
4. hidden-state difference at the answer position.

### 8.7 Minimum valid protocol

1. Use a model that actually produces reasoning traces, or use teacher-forced traces from an open reasoning checkpoint.
2. Construct a dataset of image-question items with two controlled images that differ in one answer-relevant visual attribute.
3. Generate one or more natural reasoning traces.
4. Evaluate the same trace prefix at matched positions under:
   - original image;
   - answer-counterfactual image;
   - image-ablated condition.
5. Compare image causal effects across early, middle, and late prefixes.
6. Match or regress out:
   - total prefix length;
   - number of visual words;
   - token position;
   - answer format;
   - item difficulty;
   - trace identity.
7. Repeat with at least two small architectures if possible.

This design does not claim that a generated trace length was randomly assigned. It estimates whether the image effect changes conditionally along a fixed trace.

### 8.8 Why repeated visual injection should not be the primary intervention

Re-injection is scientifically useful but causally ambiguous:

- the image appears at new token positions;
- RoPE or other positional encoding changes;
- the prompt becomes longer;
- the model receives a fresh visual encoding or cache;
- the second image may act as a reset or attention anchor;
- the intervention changes both visual availability and context layout.

Therefore, an image-reinjection improvement would justify:

> “Re-presenting visual evidence can restore performance.”

It would not justify:

> “Reasoning length caused visual degradation.”

## 9. Q2 Causal Protocol

### 9.1 Validity of the original four-arm design

| Arm                                    | Technical feasibility                                                         | Main problem                                                                                         | Decision                                                |
| -------------------------------------- | ----------------------------------------------------------------------------- | ---------------------------------------------------------------------------------------------------- | ------------------------------------------------------- |
| Synthetic geometry replication         | Feasible                                                                      | Required for validating the implementation                                                           | Retain                                                  |
| Natural photographic scenes            | Possible only with object/attribute annotations or carefully constructed data | Ordinary photo datasets do not guarantee valid binding structure                                     | Retain only after dataset feasibility gate              |
| Natural scenes with controlled clutter | Difficult                                                                     | Segmentation and editing introduce distribution shift and may alter the causal object representation | Replace with progressive visual randomization           |
| Random-vector placebo                  | Feasible                                                                      | Does not control all consequences of activation replacement                                          | Retain as one of several controls, not the only placebo |

### 9.2 Revised research question

> **Do causal object-region activation swaps that transfer a binding relation in controlled synthetic scenes retain behavioral specificity under increased visual variation and, where valid annotations exist, natural photographic scenes?**

The question deliberately avoids “universal” and “architecture-independent.”

### 9.3 Required detection/intervention/separation distinction

#### Detection

Can a representation predict the object–attribute or symbol–object relation?

Use:

- linear probe accuracy;
- cross-scene retrieval;
- held-out object/color combinations;
- cross-layout generalization.

Detection alone is correlational.

#### Intervention

Does swapping or editing the representation change the binding behavior?

Use:

- source-to-target activation swap;
- pre/post answer-logit change;
- transferred-binding accuracy.

#### Specificity

Does the intervention alter only the intended relation?

Measure:

- intended binding change;
- preservation of unrelated attributes;
- preservation of answer format;
- effect on non-target objects;
- effect of random-vector and wrong-source swaps.

#### Generalization

Does the effect survive:

- held-out shapes and colors;
- different layouts;
- texture/background variation;
- natural images;
- another architecture?

### 9.4 Binding-ID swap success metrics

Let $y_{\mathrm{local}}$ be the answer associated with the host image and $y_{\mathrm{source}}$ the answer associated with the source activation.

Define:

$$
\mathrm{TransferAcc}
=
\frac{1}{N}
\sum_i
\mathbf{1}
\left[
\hat y_i^{\mathrm{patched}}=y_{i,\mathrm{source}}
\right].
$$

Define the causal effect:

$$
\mathrm{SwapEffect}
=
\frac{1}{N}
\sum_i
\left[
\Delta \log p_i(y_{\mathrm{source}})
-
\Delta \log p_i(y_{\mathrm{local}})
\right],
$$

where $\Delta$ is post-intervention minus pre-intervention log probability.

Define specificity:

$$
\mathrm{Specificity}
=
\mathrm{SwapEffect}_{\mathrm{target}}
-
\mathrm{SwapEffect}_{\mathrm{non-target}}.
$$

Define preservation:

$$
\mathrm{Preservation}
=
1-
\frac{
\text{change in unrelated-attribute score}
}{
\text{change in intended-binding score}+\epsilon
}.
$$

A valid binding intervention should show:

1. high baseline binding accuracy;
2. high transferred-binding accuracy;
3. positive target logit effect;
4. low non-target effect;
5. superiority to random-vector, wrong-source, and spatially adjacent swaps.

### 9.5 Recommended Q2 progression

#### Stage 1 — Exact replication

Replicate the C1 or C2 synthetic task on a small model, preferably Qwen2.5-VL-3B if the image-token mapping works.

Do not alter the task until:

- baseline accuracy is adequate;
- object-region token masks are verified;
- activation swapping changes the expected answer;
- random-vector and wrong-region controls fail.

#### Stage 2 — Synthetic variation

Add one variation at a time:

- held-out shapes and colors;
- object texture changes;
- background changes;
- object scale;
- object position;
- clutter objects;
- non-grid layouts.

This establishes whether the mechanism generalizes within synthetic-to-rendered images.

#### Stage 3 — Natural-image feasibility gate

Proceed to natural images only if each example has:

- a uniquely identifiable target object;
- an explicit attribute label;
- a second object with a contrasting attribute;
- a valid object mask or bounding box;
- an answer that changes under an object–attribute swap;
- no dependence on caption text.

If those conditions cannot be met, the natural-photograph arm should be rejected rather than approximated with weak labels.

#### Stage 4 — Natural-image diagnostic

Use natural images only for representation detection and behavioral counterfactual evaluation unless token-aligned activation swapping can be validated. Do not claim a causal natural-image result from a patch that has not passed synthetic controls.

### 9.6 Random-vector control assessment

A random-vector intervention is useful but insufficient.

It should be matched for:

- Euclidean norm;
- layer;
- token positions;
- number of replaced tokens;
- source/target context;
- activation distribution.

Additional controls are required:

1. wrong-source activation swap;
2. spatially adjacent region swap;
3. same-object different-layer swap;
4. zero-vector ablation;
5. source activation permutation;
6. unrelated-object activation swap.

The strongest placebo is not one random vector; it is a **control family** showing that only the correct source relation transfers the intended binding.

## 10. Causal Validity & Confound Analysis

### Q1

| Component               | Specification                                                                                                                                  |
| ----------------------- | ---------------------------------------------------------------------------------------------------------------------------------------------- |
| Manipulated variable    | Image availability or image content at a fixed reasoning prefix; reasoning position is analyzed conditionally                                  |
| Controlled variables    | Image/question, prefix tokens, answer format, decoding temperature, candidate answer set, token position, image-token count where possible     |
| Outcome                 | Counterfactual answer log-odds and JS divergence between image conditions                                                                      |
| Alternative explanation | Longer traces are harder, contain more self-generated text, or change answer uncertainty independently of visual use                           |
| Control                 | Same trace prefix under original, counterfactual, and ablated image conditions                                                                 |
| Causal interpretation   | The image has a smaller or larger causal effect on next-token predictions at a given prefix position                                           |
| Overclaim not justified | That trace length alone causes visual forgetting; that attention decline proves information loss; that image re-injection identifies the cause |

### Q2

| Component               | Specification                                                                                                                                             |
| ----------------------- | --------------------------------------------------------------------------------------------------------------------------------------------------------- |
| Manipulated variable    | Hidden-state patch from source object region into target object region                                                                                    |
| Controlled variables    | Same model, layer, token width, prompt, target query, object-mask size, source-target attribute contrast                                                  |
| Outcome                 | Transferred-binding accuracy, logit effect, specificity, unrelated-attribute preservation                                                                 |
| Alternative explanation | Patch transfers object identity, color, spatial position, or generic visual salience rather than a binding relation                                       |
| Control                 | Wrong-source, adjacent-region, random-vector, zero-vector, and source/target attribute swaps                                                              |
| Causal interpretation   | The patched representation is causally sufficient to alter the queried relation under the tested task                                                     |
| Overclaim not justified | That the representation is a universal Binding ID; that the same mechanism exists in every architecture; that natural-image failures imply absent binding |

## 11. Colab Feasibility

### Q1

| Component                                | Status                                                                           |
| ---------------------------------------- | -------------------------------------------------------------------------------- |
| Inference with Qwen2.5-VL-3B             | **ESTIMATED feasible** on 16 GB with quantization and batch size 1         |
| Full-precision model loading             | **UNKNOWN; requires runtime test**                                         |
| Hidden-state extraction                  | **REQUIRES RUNTIME TEST**                                                  |
| Attention extraction                     | **REQUIRES RUNTIME TEST** and may substantially increase memory            |
| Teacher-forced image/ablated comparisons | **ESTIMATED feasible**, but requires roughly two forward passes per prefix |
| Long CoT generation                      | **Moderate-to-high burden** because KV cache grows with reasoning length   |
| Batch size                               | Likely 1 on 16 GB; exact value**UNKNOWN**                                  |
| Storage                                  | Low-to-moderate for logits; high if storing all hidden states and attention maps |
| Main bottleneck                          | Repeated forward passes and activation storage, not parameter count alone        |

Q1 should avoid storing full attention maps for every token and layer. Store only:

- selected answer logits;
- selected layer hidden states;
- visual-token aggregate measures;
- a small number of attention summaries.

### Q2

| Component                         | Status                                                                        |
| --------------------------------- | ----------------------------------------------------------------------------- |
| Synthetic Qwen2.5-VL-3B inference | **ESTIMATED feasible** with quantization                                |
| Activation capture                | **REQUIRES RUNTIME TEST**                                               |
| Object-token mask mapping         | **REQUIRES RUNTIME TEST**                                               |
| Activation swapping               | **REQUIRES RUNTIME TEST**                                               |
| LLaVA-OneVision-7B replication    | Likely difficult on 16 GB without aggressive quantization                     |
| Qwen2.5-VL-7B replication         | High burden on 16 GB; not a first target                                      |
| Multiple architectures            | Likely impractical in the first implementation stage                          |
| Storage                           | Moderate for selected layer activations; high for all-layer/all-token caching |
| Main bottleneck                   | Correct token-region alignment and intervention engineering                   |

The C1 paper’s own results show that activation masks and padding are model-specific. Q2 therefore requires a small synthetic proof-of-concept before any natural-image expansion.

## 12. Canonical Topic Comparison

The canonical topic is evaluated here only from the supplied description, not independently redesigned.

| Criterion                 | Canonical Conflict Verbalization                                                    | Q1                                                               | Q2                                                                    |
| ------------------------- | ----------------------------------------------------------------------------------- | ---------------------------------------------------------------- | --------------------------------------------------------------------- |
| Core scientific question  | Can a VLM verbalize and arbitrate conflicting sources?                              | Does image causal influence change along a reasoning trace?      | Does a causal binding representation transfer under visual variation? |
| Closest prior work        | Visual conflict, hallucination, source attribution, visual-versus-prior sensitivity | Remember-R1, ReGround, VIG, visual re-focusing                   | C1, C2, symbolic binding, visual circuit papers                       |
| Remaining gap             | Depends on exact conflict-verbalization formulation                                 | Matched causal measurement after existing visual-forgetting work | Synthetic-to-natural and specificity transfer                         |
| Causal testability        | Potentially high with source-swapped evidence and verbalized attribution            | High for image counterfactual effect; lower for length causality | High in synthetic setting; fragile in natural setting                 |
| Dataset accessibility     | Likely high if public conflict data are used                                        | High, but no dataset alone isolates Q1                           | Synthetic high; natural binding data less straightforward             |
| Model accessibility       | High with small VLMs                                                                | High for inference; moderate for hidden states                   | Moderate for synthetic; high risk for natural patching                |
| Internal-state access     | Helpful but not necessarily essential                                               | Important for mechanism claims                                   | Essential for the proposed intervention                               |
| Engineering complexity    | Moderate                                                                            | Moderate                                                         | High                                                                  |
| Compute burden            | Low-to-moderate                                                                     | Moderate                                                         | Moderate-to-high                                                      |
| Main confound             | Models may repeat textual labels without source arbitration                         | Position, difficulty, and attention measurement                  | Patch may transfer content or salience rather than binding            |
| Negative-result value     | Could reveal verbalization is not faithful source arbitration                       | Could invalidate attention-based visual-forgetting explanations  | Could show synthetic binding mechanisms do not transfer               |
| Reproducibility           | Potentially strong with counterfactual prompts                                      | Strong if teacher-forced and paired                              | Fragile unless exact masks and hooks are released                     |
| Pre-emption risk          | Unknown from this audit; broad source-conflict literature is active                 | High for broad question; medium for modified question            | Medium for broad binding; lower for transfer-specific question        |
| Invalid-intervention risk | Moderate                                                                            | Moderate                                                         | High                                                                  |
| Main uncertainty          | Whether verbalized source reasoning is faithful                                     | Whether length has an independent causal effect                  | Whether synthetic binding is general or task-induced                  |

The canonical topic is not automatically superior. Its main advantage is that it may require less invasive internal intervention. Q2’s advantage is mechanistic distinctiveness, but its implementation risk is considerably higher.

## 13. Closest-Work Matrix

| Candidate   | Closest paper                                                |                        Same question? |                      Same mechanism? |           Same intervention? |           Same dataset? |             Same metric? | Remaining scientific difference                                                                     |
| ----------- | ------------------------------------------------------------ | ------------------------------------: | -----------------------------------: | ---------------------------: | ----------------------: | -----------------------: | --------------------------------------------------------------------------------------------------- |
| Q1 original | [VIG](https://www.alphaxiv.org/abs/2608.21883)                |                                Partly | Yes, visual dependence versus length |                           No |                      No |                   Partly | VIG correlates VIG with length; it does not estimate the controlled causal effect of trace position |
| Q1 original | [Remember-R1](https://www.alphaxiv.org/abs/2608.01314)        |                           Broadly yes |   Yes, visual persistence/forgetting |                           No |                      No |          Attention-based | It does not establish that attention decline is causal or independent of position                   |
| Q1 original | [ReGround](https://www.alphaxiv.org/abs/2608.04385)           |                           Broadly yes |          Yes, visual grounding decay |                 Re-injection |                      No |         Entropy/accuracy | It tests restoration and diagnosis, not exact matched-prefix causal measurement                     |
| Q1 modified | [Seeing or Knowing?](https://www.alphaxiv.org/abs/2607.26326) |                                    No |                   Visual utilization | Activation patching/steering |               WhatIfVis |                  PairAcc | Q1 studies changing image causal effect along reasoning prefixes; A1 excludes intermediate traces   |
| Q2 original | C2                                                           | No, but same claimed mechanism family |                                  Yes |  Yes, activation replacement |                      No |  Binding log probability | C2 does not test natural photographs or architecture transfer                                       |
| Q2 original | C1                                                           |    No, but strong mechanistic overlap |                 Yes/possibly related |  Yes, object-region swapping |   Same synthetic family |            Swap accuracy | C1 tests multiple models but not natural causal transfer                                            |
| Q2 modified | C1                                                           |                                    No |                                  Yes |                      Similar | Synthetic baseline only | Similar plus specificity | New question is whether effect survives natural variation and remains specific                      |
| Q2 modified | [Circuit Tracing](https://www.alphaxiv.org/abs/2602.20330)    |                                    No |     General visual-semantic circuits |    Feature steering/patching |       ImageNet/Cauldron |       Case-study outputs | Q2 focuses on binding transfer, not general circuit tracing                                         |
| Q2 modified | [EditCLEVR](https://www.alphaxiv.org/abs/2607.22705)          |                                    No |           Compositional faithfulness |    Paired-scene intervention |       Controlled scenes |       Benchmark-specific | Does not establish Binding-ID representation or natural-image transfer                              |

## 14. Phase-2 Kill Tests

### Q1

1. **Literature:** Broad question is pre-empted by [Remember-R1](https://www.alphaxiv.org/abs/2608.01314), [ReGround](https://www.alphaxiv.org/abs/2608.04385), and [VIG](https://www.alphaxiv.org/abs/2608.21883). **Fails in original form.**
2. **Mechanism:** Visual forgetting is not yet mechanistically settled because attention, VIG, and causal image effects are not equivalent. **Survives partially.**
3. **Intervention:** Neutral padding is invalid as a clean causal intervention. **Fails original design.**
4. **Dataset:** Public visual-reasoning datasets exist, but they need paired counterfactual image conditions. **Survives with construction/control work.**
5. **Model:** Small open models likely expose the required logits and hidden states. **Requires runtime test.**
6. **Compute:** Inference-only paired evaluation is plausible. **Survives.**
7. **Confound:** Position and difficulty can overwhelm the claimed effect. **Can be controlled, but not eliminated by attention alone.**
8. **Negative result:** A null result would show that reported visual forgetting is largely measurement artifact or difficulty confounding. **Scientifically useful.**
9. **Reproducibility:** Strong if using teacher-forced prefixes and releasing traces. **Survives.**
10. **Scope:** Focused enough if restricted to one primary metric, one model, and one paired dataset. **Survives with modification.**

### Q2

1. **Literature:** No direct natural-image causal transfer paper was found. **Survives literature test.**
2. **Mechanism:** Existing papers show synthetic causal effects but do not establish universal IDs. **Survives only as a transfer test.**
3. **Intervention:** Activation swapping is technically possible in synthetic scenes but fragile in natural images. **High risk.**
4. **Dataset:** Natural photographs may not contain valid object–attribute counterfactuals. **Potential kill condition.**
5. **Model:** Qwen2.5-VL-3B is a plausible first model, but exact token masks require implementation validation. **Requires runtime test.**
6. **Compute:** Synthetic small-model experiments are plausible; multi-model natural experiments are not guaranteed on 16 GB. **Moderate risk.**
7. **Confound:** Region swaps can transfer object identity, position, color, or low-level features rather than binding. **Requires extensive controls.**
8. **Negative result:** Failure to transfer would show synthetic binding is not a general mechanism. **Highly useful.**
9. **Reproducibility:** Possible only if exact scene generator, image-token masks, hooks, and checkpoints are released. **Currently weak.**
10. **Scope:** A full universal architecture-independent study is too broad. A single-model transfer ladder is thesis-sized. **Survives with modification.**

## 15. Final Status

### Q1 — Final Phase-2 Status

**SURVIVES WITH MODIFICATION**

The original claim that visual evidence utilization degrades with reasoning length is substantially pre-empted. Recent papers already report visual forgetting, visual grounding decay, visual re-examination, and decreasing visual information density with longer reasoning traces. The four-arm design is not causally clean because semantic-neutral padding is not neutral and repeated visual-token injection changes multiple architectural variables.

The defensible remaining question is whether the **image-conditioned causal effect on next-token predictions declines across matched reasoning prefixes after controlling for position, prefix length, and task difficulty**. This is a measurement-audit contribution, not a discovery of visual forgetting.

### Q2 — Final Phase-2 Status

**SURVIVES WITH MODIFICATION**

The original “universal, architecture-independent Binding IDs” claim is too broad and is not supportable with the proposed resources. Existing papers already show causal binding-like effects in synthetic scenes, and C1 reports multiple-model synthetic results. However, no verified paper in this search directly establishes causal transfer from synthetic scenes to natural photographs under controlled object–attribute intervention.

The defensible remaining question is whether causal activation-swap effects **transfer under progressively more natural visual variation while remaining specific to the intended binding relation**. The main risk is not literature pre-emption but invalid natural-image intervention.

### Canonical Thesis — Current Status

**REMAINS A VIABLE PRIMARY BASELINE, BUT WAS NOT RE-AUTOPSIED IN THIS PHASE**

Compared with Q1 and Q2, the canonical conflict-verbalization direction may require less invasive hidden-state intervention and may offer a cleaner behavioral causal design. Its scientific value depends on whether “verbalization” is evaluated against source-swapped counterfactual evidence rather than treated as a free-form explanation.

It should not be favored automatically, but Q1 and Q2 have not demonstrated enough advantage to displace it. Q2 has greater mechanistic distinctiveness but substantially higher engineering risk. Q1 is easier to implement but faces greater pre-emption risk.

### Top 2 Backup Candidates

1. **Matched-prefix causal visual evidence utilization**

   - **Precise question:** At matched reasoning-prefix positions, does the causal effect of image evidence on next-token answer probabilities decline over multimodal reasoning traces after controlling for prefix length, token position, and item difficulty?
   - **H1:** Image causal effect declines at later matched positions.
   - **H0:** The decline disappears under matched-prefix controls.
   - **Closest prior work:** [VIG](https://www.alphaxiv.org/abs/2608.21883), [Remember-R1](https://www.alphaxiv.org/abs/2608.01314), [ReGround](https://www.alphaxiv.org/abs/2608.04385).
   - **Remaining gap:** Existing work does not clearly isolate the controlled causal estimand.
   - **Dataset:** A paired counterfactual subset derived from a public visual-reasoning benchmark; WhatIfVis may be useful for the image/prior component but does not provide long CoT by itself.
   - **Model:** Qwen2.5-VL-3B or a small reasoning-capable open VLM, subject to runtime validation.
   - **Intervention:** Image ablation or counterfactual image replacement under teacher-forced prefixes.
   - **Primary metric:** Counterfactual answer log-odds or JS divergence.
   - **Major confound:** Prefix difficulty and sequence position.
   - **Key control:** Same prefix evaluated with original, counterfactual, and ablated images.
   - **Compute concern:** Repeated forward passes and KV-cache growth.
   - **Strongest failure reason:** The effect may disappear, showing that reported visual forgetting is mostly attention geometry or difficulty confounding.
2. **Synthetic-to-natural transfer of causal binding effects**

   - **Precise question:** Do object-region activation swaps that transfer binding in controlled synthetic scenes remain behaviorally effective and specific under natural visual variation?
   - **H1:** Transfer accuracy remains above wrong-source, random-vector, and adjacent-region controls as visual variation increases.
   - **H0:** The apparent effect collapses outside the synthetic partitioned setting.
   - **Closest prior work:** [Investigating Mechanisms for In-Context Vision Language Binding](https://openaccess.thecvf.com/content/CVPR2025W/MIV/papers/Saravanan_Investigating_Mechanisms_for_In-Context_Vision_Language_Binding_CVPRW_2025_paper.pdf) and [Uncovering Grounding IDs](https://www.alphaxiv.org/abs/2509.24072).
   - **Remaining gap:** No verified direct causal synthetic-to-natural transfer study was found.
   - **Dataset:** Exact replicated synthetic scenes first; natural images only after object–attribute annotation feasibility is established.
   - **Model:** Qwen2.5-VL-3B initially; second architecture only if the first intervention is stable.
   - **Intervention:** Object-region hidden-state swap at a validated layer, with matched source/target masks.
   - **Primary metric:** Transferred-binding accuracy.
   - **Major confound:** Patch transfers object appearance or spatial salience rather than binding.
   - **Key control:** Wrong-source, adjacent-region, zero-vector, norm-matched random-vector, and non-target preservation controls.
   - **Compute concern:** Token-region alignment, activation caching, and hidden-state replacement.
   - **Strongest failure reason:** Natural photographs may not support a valid object–attribute intervention, making the intended causal claim unidentifiable.

### What Phase 3 Must Verify

1. Load Qwen2.5-VL-3B and Gemma 3 4B in the exact intended Colab environment.
2. Record actual VRAM use with image inputs and one long teacher-forced prefix.
3. Verify `output_hidden_states` and attention extraction.
4. Map image regions to visual-token indices for several image resolutions.
5. Reproduce the C1 synthetic activation swap before designing any natural-image extension.
6. Test whether activation replacement preserves tensor shape, dtype, cache behavior, and output reproducibility.
7. Construct a small Q1 paired-counterfactual pilot and measure image-ablation logit effects at matched prefixes.
8. Verify whether the selected reasoning-capable model actually generates sufficiently long, stable multimodal reasoning traces.
9. Confirm licenses and live download paths for every proposed dataset.
10. Release exact prompts, model revisions, processor settings, image preprocessing, token masks, and intervention code before interpreting any result.

**Phase 3 should begin with runtime feasibility and exact replication—not with large-scale data collection or thesis implementation.**
