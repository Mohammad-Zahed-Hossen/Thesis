
# Paper 1 — [RH-Bench: “More Thinking, Less Seeing?”](https://www.alphaxiv.org/abs/2505.21523)

## 1. Hypothesis

**[VERIFIED]** The paper tests whether multimodal reasoning models become more hallucination-prone than their non-reasoning counterparts, and whether increasing reasoning-chain length further reduces visual grounding. The authors interpret declining attention to image tokens and increasing attention to instruction tokens as evidence that models increasingly rely on language priors. [Core Hypothesis](https://www.alphaxiv.org/abs/2505.21523?page=1)

The paper also claims that the relationship between reasoning length and the reasoning–hallucination tradeoff is generally non-monotonic: very short reasoning can be insufficient, moderate reasoning can help, and excessive reasoning can hurt. [Length Effect](https://www.alphaxiv.org/abs/2505.21523?page=6)

However, the paper’s central causal language is stronger than its design supports. Its strongest defensible claim is:

> **Longer generated reasoning is associated with lower measured visual attention and worse perception/hallucination performance in the tested models and tasks.**

The stronger claim—**reasoning length itself causes visual evidence under-utilization**—is not isolated from position, context, or content effects.

## 2. Models and architectural level

**[VERIFIED]** The main evaluation covers multimodal reasoning models built around the Qwen2.5-VL family, including 3B- and 7B-scale models such as LLM-R1, Curr-ReFT, Ocean-R1, R1-OneVision, ThinkLite-VL, OpenVLThinker, MM-Eureka, and MM-R1. The paper explicitly states that the study is limited to models built on the Qwen2.5-VL backbone. [Model Limitation](https://www.alphaxiv.org/abs/2505.21523?page=9)

**[VERIFIED]** Attention analysis is conducted across layers and separates attention directed toward visual tokens, instruction tokens, and system tokens. The paper’s figures show layer-wise attention trends, but the main text does not establish a causal circuit or identify a particular attention head as responsible. [Attention Analysis](https://www.alphaxiv.org/abs/2505.21523?page=4)

**[NOT FOUND]** The paper does not provide, in the sections examined, a controlled analysis of the exact image-token positions under each length condition, nor a position-matched answer-token experiment.

**[NOT FOUND]** It does not report a causal intervention on visual activations, visual-token ablation, activation patching, or visual-information restoration.

## 3. Data

**[VERIFIED]** RH-Bench contains 1,000 samples:

- 500 reasoning samples from MathVision, MathVista, MMMU, and ScienceQA;
- 500 perception/hallucination samples from MMHalu, MMVP, HallusionBench, and VMCBench.

Multiple-choice items are scored by answer matching. Open-ended items are evaluated with GPT-4o, with perception responses receiving scores from 0 to 6; scores below 3 are classified as hallucinations. The paper states that ground-truth and evaluation answers were manually inspected. [RH-Bench Setup](https://www.alphaxiv.org/abs/2505.21523?page=7)

**[VERIFIED]** The official [MLRM-Halu repository](https://github.com/MLRM-Halu/MLRM-Halu) provides links to the paper, RH-Bench, evaluation scripts, visualization utilities, and length-control code.

**[INFERRED]** Because the benchmark combines heterogeneous datasets and task types, a change in performance with generated length could reflect task-specific sensitivity rather than one general visual-utilization mechanism.

## 4. Length manipulation

The paper uses three different mechanisms.

### A. Token budget forcing

**[VERIFIED]** The model is given a predefined generation budget that limits the number of reasoning tokens. This is a decoding-level constraint. [Budget Forcing](https://www.alphaxiv.org/abs/2505.21523?page=5)

This changes at least several variables simultaneously:

- maximum available reasoning length;
- possible answer position;
- total number of generated tokens;
- amount of intermediate content;
- potentially the model’s stopping behavior.

**[INFERRED]** Budget forcing alone cannot distinguish a genuine reasoning-content effect from a sequence-length or position effect.

### B. Test-time scaling

**[VERIFIED]** The procedure first generates partial reasoning under a 4,096-token constraint, then appends “Wait” and asks the model to continue. [Test-Time Scaling](https://www.alphaxiv.org/abs/2505.21523?page=5)

**[INFERRED]** This is not a neutral length intervention. Appending “Wait” changes the textual context and may induce a specific continuation policy. The added reasoning is therefore not merely extra tokens; it is also a prompt-mediated behavioral manipulation.

### C. Latent-state steering

**[VERIFIED]** The authors compute average hidden representations over reasoning tokens from long and short trajectories. They define a layer-wise direction

$$
d^\ell = S^\ell_{\mathrm{long}} - S^\ell_{\mathrm{short}},
$$

and modify hidden states using

$$
S^\ell_{\mathrm{steering}} = S^\ell + \alpha d^\ell.
$$

The steering direction is applied across decoder layers, with $\alpha$ controlling the direction and magnitude of steering. [Latent Steering](https://www.alphaxiv.org/abs/2505.21523?page=6)

The official repository states that directions can be extracted in either text mode or vision mode and then applied to control reasoning length.

**Important limitation:** the direction is estimated from naturally occurring long-versus-short representations. It is therefore not a pure “length axis” by construction.

**[INFERRED]** The direction may contain correlated changes in:

- reasoning style;
- uncertainty;
- verbosity;
- answer difficulty;
- instruction-following behavior;
- visual attention;
- language-prior reliance.

Therefore, steering along $d^\ell$ establishes that a learned latent direction changes output length and behavior. It does not establish that length is the only manipulated variable.

## 5. Controls

**[VERIFIED]** The paper compares:

- reasoning models against non-reasoning backbones;
- normal thinking against overthinking;
- different reasoning lengths;
- different model scales;
- different training paradigms;
- different benchmark/task types.

It also includes a “zerothink” condition in which the model retains a reasoning structure but lacks substantive reasoning content. The paper reports that this condition performs worse on both reasoning and perception tasks. [Zerothink Control](https://www.alphaxiv.org/abs/2505.21523?page=6)

**[NOT FOUND]** The paper does not report a control that:

1. keeps the final answer position fixed while varying only the semantic content between image and answer;
2. adds neutral filler of equal length;
3. keeps total context length fixed while changing reasoning content;
4. matches the number of image-to-answer positional steps;
5. explicitly models the expected $M/N$ visual-attention share;
6. separates visual-information availability from utilization.

The “zerothink” condition is not sufficient for this purpose. It removes substantive reasoning content but does not necessarily match the normal condition in token positions, hidden-state dynamics, or decoding trajectory.

## 6. Dependent variables

### A. Accuracy and hallucination

**[VERIFIED]** RH-Bench measures reasoning accuracy and perception/hallucination performance at different generated reasoning lengths. RH-AUC integrates the resulting reasoning–hallucination curve after min–max normalization. [RH-AUC](https://www.alphaxiv.org/abs/2505.21523?page=7)

**[INFERRED]** RH-AUC is a useful summary metric for model evaluation, but it cannot identify the mechanism behind a performance change. A lower RH-AUC could result from:

- visual information loss;
- answer-position effects;
- altered stopping behavior;
- reasoning-content errors;
- increased language-prior reliance;
- evaluator sensitivity to longer outputs.

### B. Attention

**[VERIFIED]** The paper reports lower attention to visual tokens in reasoning models and under longer or “overthinking” conditions, with increased attention to instruction tokens. [Longer Reasoning](https://www.alphaxiv.org/abs/2505.21523?page=5)

**[INFERRED]** The attention result is an observational association. It does not demonstrate that reduced attention caused hallucination.

The paper does not show that:

- increasing visual attention restores correctness;
- reducing visual attention causes hallucination while all other variables remain fixed;
- raw attention mass tracks visual evidence utilization;
- visual evidence remains or ceases to remain decodable in residual representations.

## 7. Exact answers to the requested Q1 audit

| Question                                                         | Finding                                                                                                                                                             |
| ---------------------------------------------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| Did RH-Bench decouple token length from absolute sequence index? | **[NOT FOUND]** No answer-position-matched control is reported.                                                                                               |
| Did it control RoPE or positional effects?                       | **[NOT FOUND]** No explicit RoPE intervention or positional correction is reported.                                                                           |
| Did it control total context length?                             | **[NOT FOUND]** The length manipulations change the generated context.                                                                                        |
| Did it control visual-token distance from the answer?            | **[NOT FOUND]** No such control is reported.                                                                                                                  |
| Did it model the softmax denominator$M/N$?                     | **[NOT FOUND]** No uniform-attention dilution null is defined.                                                                                                |
| Did it separate reasoning content from neutral padding?          | **[NOT FOUND]** Zerothink is not an equivalent neutral-padding condition.                                                                                     |
| Did it measure visual-information availability?                  | **[NOT FOUND]** No decodability or causal recoverability test is reported.                                                                                    |
| Did it measure visual-information utilization causally?          | **[NOT FOUND]** Attention and accuracy are observational.                                                                                                     |
| Can its code run answer-position-fixed experiments?              | **[NOT FOUND]** The repository documents length control and latent steering, but its README does not document a position-matched internal-token intervention. |
| Does the code provide a useful starting point?                   | **[VERIFIED]** Yes. It provides budget forcing, test-time scaling, latent-state direction extraction, steering, and RH-Bench evaluation scripts.              |

The repository describes latent-state extraction from residual inputs and supports text-only and vision-inclusive modes, but the documented workflow is still designed to alter reasoning behavior rather than to isolate answer position as an experimental factor.

## 8. What RH-Bench genuinely establishes

**[VERIFIED]** In the tested Qwen2.5-VL-derived models and benchmark tasks:

1. multimodal reasoning models can show more hallucination than their non-reasoning counterparts;
2. longer or overextended reasoning is associated with reduced visual-token attention;
3. reasoning length has a non-monotonic relationship with the combined reasoning/perception score;
4. the optimal length depends on task type;
5. larger models generally show better reasoning–hallucination balance in their evaluation.

**[INFERRED]** The evidence is consistent with visual grounding degradation during long reasoning, but it does not identify whether the degradation is caused by reasoning content, sequence position, context growth, attention dilution, or another correlated factor.

**[VERIFIED]** The authors themselves state that their conclusions about training data are observational and may not represent causal effects. [Study Limitation](https://www.alphaxiv.org/abs/2505.21523?page=9)

## 9. What RH-Bench does not establish

**[NOT FOUND]** RH-Bench does not establish that:

- reasoning length is an independent causal variable;
- a fixed answer position would preserve or eliminate the effect;
- the effect is not explained by visual-token distance;
- the effect exceeds uniform softmax dilution;
- image information becomes unavailable rather than merely unused;
- attention mass is a valid proxy for evidence utilization;
- the phenomenon generalizes beyond Qwen2.5-VL-derived models.

## 10. Overlap with Q1

RH-Bench directly overlaps with the original Q1 headline claim:

> Longer multimodal reasoning may reduce visual grounding.

That part of Q1 is therefore **not novel as a broad empirical observation**.

It does **not** resolve the narrower mechanistic decomposition proposed by Q1:

- reasoning content versus neutral filler;
- answer position and visual-token distance;
- context-length and softmax dilution;
- information availability versus utilization;
- causal restoration or intervention.

## 11. Verdict on Q1

**Verdict: NARROWS Q1; does not kill the mechanistic version.**

The original broad question—“does longer reasoning reduce visual evidence use?”—is substantially pre-empted by [RH-Bench](https://www.alphaxiv.org/abs/2505.21523).

The defensible remaining question is:

> After matching answer position and total context length, does reasoning content produce a visual-utilization change beyond the uniform $M/N$ attention dilution predicted by added tokens, and is visual evidence still available in the residual stream?

That is a materially narrower question. It is not answered by the paper.

---

# Paper 2 — [Uncovering Grounding IDs: How External Cues Shape Multimodal Binding](https://www.alphaxiv.org/abs/2509.24072)

## 1. Hypothesis

**[VERIFIED]** The paper proposes that external visual and textual cues—symbols, row partitions, and grid lines—induce latent “Grounding IDs” that bind visual regions to corresponding textual symbols. Its central hypothesis is that shared cues across the image and prompt reduce the modality gap and improve object–symbol binding. [Grounding-ID Hypothesis](https://www.alphaxiv.org/abs/2509.24072?page=2)

The paper tests two broad claims:

1. structured cues increase visual–textual alignment;
2. the resulting internal representations causally mediate object–symbol binding.

## 2. Model and layer details

**[VERIFIED]** The main mechanistic experiments use Qwen2.5-VL 7B without fine-tuning. The structured-input analysis uses four horizontal partitions, four symbols, and synthetic scenes. [Main Model](https://www.alphaxiv.org/abs/2509.24072?page=3)

**[VERIFIED]** The paper reports that cross-modal alignment improvements become particularly visible in layers 22–27 for its 7B Qwen2.5-VL analysis. [Alignment Layers](https://www.alphaxiv.org/abs/2509.24072?page=4)

**[VERIFIED]** The causal swap appendix states that activations are extracted across all layers and that object-region activations are swapped between paired contexts. It also describes a one-token spatial dilation around the object mask. [Swap Implementation](https://www.alphaxiv.org/abs/2509.24072?page=20)

**[NOT FOUND]** The paper does not specify a single hidden-state dimensionality in the causal-method description.

**[NOT FOUND]** The paper does not identify a single causal layer at which the primary object swap is performed. Its main intervention description says that activations are swapped across all layers. The layer-18 value in the appendix refers to the selected attention-extraction layer for Qwen2.5-VL in an attention-recalibration analysis, not clearly to the causal swap layer. This distinction is important for reproducing C1.

**[VERIFIED]** The paper also reports qualitative replication of the swap behavior on Qwen2.5-VL 3B and InternVL3.5 8B, with swap accuracies above the stated chance levels. [Alternative Models](https://www.alphaxiv.org/abs/2509.24072?page=21)

## 3. Data

### A. Structured alignment dataset

**[VERIFIED]** The structured alignment analysis uses synthetic images containing 15 unique objects drawn from 35 shape–color combinations. Each object occupies a single patch and is designed not to cross adjacent patches. Four horizontal partitions are marked with symbols. [Synthetic Data](https://www.alphaxiv.org/abs/2509.24072?page=3)

The use of unique objects makes regex-based matching between generated object descriptions and image objects straightforward.

### B. Causal swap dataset

**[VERIFIED]** Appendix L describes 100 synthetic four-row scenes. Each scene contains:

- one symbol per row;
- one object per row;
- four distinct shapes;
- four distinct shape–color pairs;
- randomly permuted symbols;
- paired source and target contexts;
- object mismatches across the paired contexts in both shape and color.

[Causal Dataset](https://www.alphaxiv.org/abs/2509.24072?page=20)

### C. Natural-image evaluation

**[VERIFIED]** The paper evaluates the structured-cue strategy on MS-COCO for hallucination metrics and reports experiments on counting and visual-search benchmarks. It reports CHAIR scores for structured versus baseline inputs. [COCO Evaluation](https://www.alphaxiv.org/abs/2509.24072?page=8)

**[NOT FOUND]** The paper does not perform the proposed natural-image object-instance activation-swap experiment with real object bounding boxes.

This is the most important distinction for Q2. The paper has natural-image **performance evaluation**, but not natural-image **causal binding intervention**.

## 4. Equation 3: ICG

**[VERIFIED]** Equation 3 defines the intra-cluster gap, or ICG, as the difference between average within-row patch similarity and average between-row patch similarity:

$$
\mathrm{ICG}
=
\frac{1}{R}
\sum_{r=1}^{R}
\mathrm{Sim}_{\mathrm{intra}}(r)
-
\frac{1}{R(R-1)}
\sum_{r\ne r'}
\mathrm{Sim}_{\mathrm{inter}}(r,r').
$$

Here:

- $R$ is the number of rows;
- $\mathrm{Sim}_{\mathrm{intra}}(r)$ is the mean cosine similarity between patches within row $r$;
- $\mathrm{Sim}_{\mathrm{inter}}(r,r')$ is the average similarity between patches in different rows.

A higher ICG means stronger row-wise clustering in the visual representation. [ICG Definition](https://www.alphaxiv.org/abs/2509.24072?page=13)

ICG is therefore a **representational clustering metric**, not itself a causal alignment metric and not proof of a Grounding-ID variable.

## 5. Intervention mechanism

The intervention is an interchange activation patch.

Let:

- $c$ be the target context;
- $c'$ be the source context;
- $h^{(\ell)}(c)$ be the residual activation at layer $\ell$;
- $c^*$ be the patched context.

**[VERIFIED]** The paper replaces selected object-region visual activations in the target run with corresponding activations from the source run, then runs the remaining computation and records the resulting predictions. [Activation Swap](https://www.alphaxiv.org/abs/2509.24072?page=5)

The causal dataset is designed so that the source and target objects differ in both shape and color for the selected symbols. This makes it harder for the result to be explained by the symbol token alone.

**[VERIFIED]** The implementation described in Appendix L:

- maps object bounding boxes to image-token indices;
- dilates each object mask by one token in each axis;
- swaps object-region activations;
- leaves symbol text tokens unchanged;
- leaves image tokens occupied by symbol glyphs unchanged;
- queries the patched scene afterward.

[Object-Only Patch](https://www.alphaxiv.org/abs/2509.24072?page=20)

## 6. What is actually causal here?

**[VERIFIED]** The intervention changes internal activations while holding the downstream model parameters fixed. The output changes toward the source-associated binding. In that limited interventionist sense, the swap is causal: changing the selected activation region changes the model’s output.

The reported main result is:

- standard, locally expected accuracy after swapping: approximately $0.02$;
- accuracy measured against the transferred source binding: approximately $0.98$.

[Swap Result](https://www.alphaxiv.org/abs/2509.24072?page=5)

But the causal conclusion needs to be stated more narrowly:

> **The selected object-region activation contains information sufficient to redirect the symbol-to-object output under this synthetic task and this intervention.**

That is weaker than proving that:

- the activation contains a distinct Grounding-ID vector;
- the effect is specific to Grounding IDs rather than general object information;
- the representation is architecture-independent;
- the effect transfers to natural photographs;
- the intervention is non-destructive;
- a matched random perturbation would not cause a similar output change.

## 7. Controls and placebos

### A. Symbol mismatch control

**[VERIFIED]** The paper uses a disjoint-symbol experiment. The source image uses one set of symbols, while the target image uses a non-overlapping symbol set. The source object activations are patched into the target while symbol tokens remain unpatched. [Disjoint Symbols](https://www.alphaxiv.org/abs/2509.24072?page=20)

The paper restricts evaluation to cases where the unpatched baseline correctly answers “none” for a symbol that is absent. This reduces one obvious hallucination bias. [Bias Control](https://www.alphaxiv.org/abs/2509.24072?page=21)

This is a useful control for whether the object-region activation can carry a symbol-related association independently of a locally present symbol token.

### B. Random Gaussian placebo

**[NOT FOUND]** The paper does not report a random Gaussian perturbation control for the principal causal swap.

### C. Norm-matched random perturbation

**[NOT FOUND]** No norm-matched random-vector placebo is reported.

### D. Scrambled activation swap

**[NOT FOUND]** No explicit scrambled-source or randomly permuted binding-direction control is reported.

### E. Irrelevant-object swap

**[NOT FOUND]** The paper does not report swapping an irrelevant object region while matching layer, position, norm, and intervention size.

### F. Destructive-perturbation control

**[NOT FOUND]** The paper does not establish that the effect is larger than the generic output disruption caused by replacing a visual activation block with an unrelated activation block.

This is the central weakness for the proposed Q2 placebo gate.

## 8. Dependent variables

The paper uses several different measurements.

### A. Attention matrices

**[VERIFIED]** The authors take the maximum attention over heads for each token, average across tokens in each partition, and form a $4\times4$ matrix. This produces stronger diagonal structure under structured inputs. [Attention Aggregation](https://www.alphaxiv.org/abs/2509.24072?page=3)

**[INFERRED]** Taking a maximum over heads is especially vulnerable to noisy-head selection and does not measure total information flow. It should not be treated as evidence that Grounding IDs are causal.

### B. Cosine similarity

**[VERIFIED]** The paper computes layer-wise cosine similarity between visual and textual embeddings corresponding to correctly generated objects. Structured inputs show higher similarity, especially in later layers. [Cosine Alignment](https://www.alphaxiv.org/abs/2509.24072?page=4)

**[INFERRED]** Conditioning on correctly generated objects can introduce selection bias: the alignment measurement is taken on examples where the model has already succeeded.

### C. ICG

**[VERIFIED]** ICG measures within-row versus across-row patch similarity.

**[INFERRED]** A higher ICG could reflect spatial regularity, image construction, or the visual effect of drawing lines and symbols. It does not uniquely identify a Grounding-ID representation.

### D. Swap accuracy

**[VERIFIED]** Swap accuracy is the fraction of queries where the post-intervention answer matches the source-associated binding rather than the locally present target object. [Swap Accuracy](https://www.alphaxiv.org/abs/2509.24072?page=5)

This is the most causally relevant metric in the paper.

## 9. Confounds in the intervention

### A. Source-activation transplantation

**[INFERRED]** A source object activation contains much more than a binding ID. It can contain:

- object shape;
- color;
- local texture;
- spatial location;
- boundary information;
- positional encoding;
- interactions with the source scene;
- artifacts from the source prompt and image layout.

The fact that the output follows the source binding does not determine which component was transferred.

### B. Object-region intervention is not a one-dimensional intervention

**[VERIFIED]** The intervention swaps all selected object-region activations, with one-token dilation, rather than a separately identified Grounding-ID direction. [Patch Scope](https://www.alphaxiv.org/abs/2509.24072?page=20)

**INFERRED]** The intervention therefore tests whether a region of the hidden state is sufficient to transmit the association. It does not isolate a low-dimensional binding direction.

### C. Synthetic regularity

**[VERIFIED]** The causal scenes contain exactly four rows, one object per row, unique shape–color combinations, and explicit symbols. [Synthetic Scene Structure](https://www.alphaxiv.org/abs/2509.24072?page=20)

**INFERRED]** The task makes the desired binding unusually explicit. A model can solve it with a structured spatial-routing strategy that may not resemble binding in natural cluttered images.

### D. Spatial and positional cues

The paper attempts to prevent simple ordinal-row shortcuts by randomly permuting symbols over rows.

**[VERIFIED]** The symbols are non-ordinal and randomly assigned to physical rows. [Randomized Symbols](https://www.alphaxiv.org/abs/2509.24072?page=20)

**[INFERRED]** This reduces one shortcut but does not eliminate:

- spatial proximity;
- row boundaries;
- object-to-symbol distance;
- source-target layout correspondence;
- the model’s learned top-to-bottom traversal bias.

The paper itself reports that structured inputs sharpen row-aligned attention and reinforce an inherent traversal bias. [Traversal Bias](https://www.alphaxiv.org/abs/2509.24072?page=12)

## 10. Natural-image evidence

The paper’s natural-image evidence must not be overstated.

**[VERIFIED]** It evaluates structured prompting and cue-based hallucination reduction on MS-COCO and reports improvements in CHAIR metrics. For Qwen2.5-VL, the structured condition reports lower sentence- and instance-level hallucination rates than the baseline. [MS-COCO Results](https://www.alphaxiv.org/abs/2509.24072?page=8)

**[NOT FOUND]** It does not perform:

- source-instance activation swaps on natural photographs;
- bounding-box-defined object-region patching on natural images;
- natural-image counterfactual binding transfer;
- placebo-controlled natural-image activation intervention;
- synthetic-to-natural transfer of the same causal swap mechanism.

Thus, the paper demonstrates that **external structure can improve natural-image benchmark performance**, not that its synthetic Grounding-ID intervention transfers to natural-image object binding.

## 11. Cross-model evidence

**[VERIFIED]** The paper reports qualitatively similar swap behavior on Qwen2.5-VL 3B and InternVL3.5 8B. InternVL3.5 reports shape and color swap accuracies of 0.75 and 0.82; Qwen2.5-VL 3B reports 0.93 and 0.73. [Cross-Model Swap](https://www.alphaxiv.org/abs/2509.24072?page=21)

This is evidence that a similar behavioral intervention can work in more than one model.

**[NOT FOUND]** It does not establish:

- a shared linear subspace across models;
- cross-model CCA or SVCCA similarity;
- a common direction in aligned coordinates;
- architecture-independent representation geometry;
- a model-independent intervention layer;
- equivalence of the transferred mechanisms.

The correct conclusion is behavioral replication, not representation universality.

## 12. What the paper genuinely establishes

**[VERIFIED]** Within its synthetic partitioned-scene setup, [Uncovering Grounding IDs](https://www.alphaxiv.org/abs/2509.24072) establishes that:

1. shared visual and textual cues improve object–symbol task performance;
2. structured inputs produce stronger row-wise attention and representation clustering;
3. object-region activation swaps can redirect the model toward source-associated bindings;
4. this swap behavior appears in at least Qwen2.5-VL 7B, Qwen2.5-VL 3B, and InternVL3.5 8B;
5. the structured prompting strategy improves some natural-image benchmark scores.

## 13. What it does not establish

**[NOT FOUND]** The paper does not establish that Grounding IDs are:

- universal across VLM architectures;
- a distinct low-dimensional representation;
- independent of object identity and spatial features;
- naturally present without explicit external cues;
- transferable to ordinary photographs;
- robust under natural-image clutter;
- specific relative to norm-matched random activation replacement;
- demonstrated through a placebo-controlled intervention.

## 14. Overlap with Q2

The overlap is extremely high.

Q2 proposes to test whether the C1-style binding mechanism:

1. survives a matched placebo;
2. transfers from synthetic scenes to natural images;
3. survives covariate controls;
4. generalizes behaviorally or representationally across architectures.

C1 already supplies:

- a synthetic object-region activation swap;
- a causal intervention in the limited interventionist sense;
- a disjoint-symbol control;
- small-scale replication across Qwen2.5-VL and InternVL3.5.

But C1 leaves open the decisive Q2 questions:

- placebo specificity;
- natural-image causal transfer;
- separation from source-object information;
- cross-architecture representation alignment;
- whether the mechanism is a general binding circuit or a cue-induced routing strategy.

## 15. Verdict on Q2

**Verdict: NARROWS Q2; does not kill the natural-transfer and specificity version.**

C1 substantially pre-empts the claim that a symbol-partition activation swap can causally redirect object–symbol answers in synthetic scenes. A thesis presenting that synthetic result alone would be weakly novel.

C1 does **not** pre-empt:

> Whether the same intervention remains specific relative to matched perturbations and transfers to natural-image object-instance binding.

That is the part of Q2 that remains empirically open.

However, the proposed Q2 intervention must be described accurately. It should not claim to test a pre-identified, universal “Binding-ID direction” unless the student adds a direction-identification procedure. The C1 intervention is primarily a **region-level activation interchange**, not a clean one-dimensional direction swap.

# Direct comparison for the Phase 3 gates

| Issue                              | [RH-Bench](https://www.alphaxiv.org/abs/2505.21523)                 | [Grounding IDs](https://www.alphaxiv.org/abs/2509.24072)                                                 |
| ---------------------------------- | ------------------------------------------------------------------ | ------------------------------------------------------------------------------------------------------- |
| Main contribution                  | Length-conditioned reasoning–hallucination evaluation             | Cue-induced object–symbol binding mechanism                                                            |
| Main manipulation                  | Budget forcing, test-time continuation, latent steering            | Object-region activation interchange                                                                    |
| Causal variable isolated?          | **[NO]** Length remains confounded with content and position | **[PARTLY]** Activation replacement changes outputs, but the replaced content is multidimensional |
| Position controlled?               | **[NOT FOUND]**                                              | **[PARTLY]** Symbol rows are randomized, but spatial structure remains                            |
| Neutral filler control?            | **[NOT FOUND]**                                              | Not applicable to the main question                                                                     |
| Random placebo?                    | Not applicable                                                     | **[NOT FOUND]**                                                                                   |
| Natural-image causal intervention? | Not applicable                                                     | **[NOT FOUND]**                                                                                   |
| Cross-model evidence               | Limited to Qwen2.5-VL-derived models                               | Behavioral swap replication in Qwen2.5-VL and InternVL3.5                                               |
| Main threat to thesis              | Broad Q1 headline is pre-empted                                    | Synthetic causal binding result is substantially pre-empted                                             |
| Remaining opening                  | Mechanistic length decomposition                                   | Specificity, natural transfer, and causal covariate control                                             |

# Immediate revisions to the Phase 3 runtime plan

## Q1

The Q1 experiment should not ask whether longer reasoning reduces visual attention; [RH-Bench](https://www.alphaxiv.org/abs/2505.21523) already provides evidence consistent with that claim.

The runtime test should instead ask:

1. Does **reasoning content** differ from equally long neutral filler?
2. Does that difference remain after matching the answer position?
3. Does the effect exceed the uniform $M/N$ dilution prediction?
4. Does residual-stream decodability remain stable while attention changes?

A result showing only lower raw visual attention under longer traces would replicate [RH-Bench](https://www.alphaxiv.org/abs/2505.21523), not establish the proposed Q1 mechanism.

## Q2

The Q2 experiment should not describe C1’s swap as an already validated universal Binding-ID direction.

The minimum decisive extension is:

1. replicate the C1-style synthetic swap;
2. add a same-region, same-layer, norm-matched irrelevant-source swap;
3. add a shuffled or mismatched source-region swap;
4. preserve non-target accuracy;
5. perform the same intervention on boxed natural-image instances;
6. report target flips minus placebo flips;
7. distinguish output disruption from binding-specific transfer.

A natural-image result without a matched placebo would show that activation replacement changes answers, but it would not show binding-specific causality.

## Bottom-line autopsy verdict

- **[RH-Bench](https://www.alphaxiv.org/abs/2505.21523):** threatens and narrows Q1, but does not answer its mechanistic version.
- **[Uncovering Grounding IDs](https://www.alphaxiv.org/abs/2509.24072):** substantially pre-empts synthetic Grounding-ID activation swapping, but does not establish placebo-controlled natural-image transfer or architecture-independent representation universality.
- The most dangerous mistake would be to treat either paper’s attention or activation-swap result as proof of a unique causal mechanism. Both papers provide strong evidence that the model’s behavior changes under their manipulations; neither fully identifies the mechanism claimed by the corresponding thesis question.
