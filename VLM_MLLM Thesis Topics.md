**Recommendation: proceed to a short pilot auditing whether VLM confidence predicts errors beyond answer identity and queried-object priors—and whether that added value survives changes in negative-question sampling.**

This is materially stronger than returning to generic degradation-and-threshold transfer. It has a precise diagnostic question, existing labels, inexpensive controls, and a useful outcome even if confidence performs well. It merits a pilot; it is **not yet a frozen thesis topic or a demonstrated novel result**.

I read all seven attachments in full before searching. I applied the canonical field specification and rejected/parked report as authorities, and treated the handovers as records requiring verification. The two Topic Discovery Handovers supplied here contain the same selection standard. Literature checking covers 2023–15 September 2026, with emphasis on recent work. No GPU experiments were performed during this review.

**A. Evidence audit of prior directions**

“Verified” below means supported by the inspected primary source—not independently reproduced experimentally.

| Prior direction or claim                                                                       | What the attached records say                                                                       | Independent verification                                                                                                                                                                                                 | Correction or limitation                                                                                                                                           | Current status                                                |
| ---------------------------------------------------------------------------------------------- | --------------------------------------------------------------------------------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------ | ------------------------------------------------------------------------------------------------------------------------------------------------------------------ | ------------------------------------------------------------- |
| An empirical evaluation may constitute the thesis                                              | Canonical specification permits diagnostics, robustness studies, audits and substantive replication | Consistent with the research designs of the papers below                                                                                                                                                                 | An existing benchmark enables research; it does not establish that every question about it is answered                                                             | **Retain this standard**                                      |
| Clean-input perturbations can reveal unreliable answers                                        | Earlier Candidate A proposed internal perturbation probes; later records identify overlap           | **Verified:** [VL-Uncertainty](https://arxiv.org/html/2411.11919v2) uses image/text perturbations, repeated answers and semantic clustering                                                                              | “Perturb and measure inconsistency” is already established. Incremental value over inexpensive confidence remains necessary                                        | **Broad version parked**                                      |
| VL-Uncertainty percentages were AUROC                                                          | Later records explicitly correct this earlier mistake                                               | **Correction verified:** its main table reports hallucination-detection **accuracy**, using an uncertainty threshold                                                                                                     | Those percentages cannot support an AUROC comparison                                                                                                               | **Earlier metric attribution contradicted**                   |
| No prior work jointly studies ranking and unchanged clean-threshold transfer under degradation | An earlier novelty claim was subsequently withdrawn                                                 | **Contradicted:** [Bigger or Cheaper?](https://arxiv.org/html/2607.24440v1), §§3.8/4.4, evaluates a clean-selected threshold unchanged under degradation alongside confidence metrics                                    | Its small Food-101 experiment limits generality, but does not erase the overlap. Independent splitting or a different risk target needs a consequential question   | **Do not revive the broad novelty claim**                     |
| Evidence-order training establishes better selective prediction                                | Records describe it as a close comparator, with limitations                                         | **Partially supported:** [Evidence-Order Calibration](https://arxiv.org/html/2609.09184v1) improves ordering under targeted evidence loss; selective-prediction gains over native confidence are not clearly established | Evidence monotonicity and error discrimination are different properties. Question-ID grouping also does not establish source-image disjointness                    | **Useful comparator, not proof that learned confidence wins** |
| BCEA demonstrates passive degradation transfer                                                 | Records correctly distinguish active acquisition                                                    | **Verified distinction:** [BCEA](https://arxiv.org/html/2606.16667v4) acquires additional views and recalibrates the acquisition policy                                                                                  | Its exact certificate uses an image-level design; practical multi-claim/POPE results have different assumptions. Neither licenses guarantees under arbitrary shift | **Relevant statistical comparator**                           |
| VL-Calibration supplies a frozen, inference-only method                                        | Later records describe RL post-training                                                             | **Verified:** [official ACL paper](https://aclanthology.org/2026.acl-long.2074/) uses decoupled visual/reasoning calibration with reinforcement learning                                                                 | Conceptual relevance does not make its full method a suitable Colab baseline                                                                                       | **Related work; not minimum baseline**                        |
| RobustBench leaves reliability unexplored                                                      | Records distinguish task robustness from confidence evaluation                                      | [VLM-RobustBench](https://arxiv.org/abs/2603.06148) supports extensive augmentation-based robustness evaluation                                                                                                          | That paper’s scope cannot establish a literature-wide calibration gap                                                                                              | **Robustness context only**                                   |
| IntroConformal proves shifted-condition reliability                                            | Records warn about both scope and publication status                                                | The [official arXiv record](https://arxiv.org/abs/2609.01375) supports an introspective conformal approach; full-text verification was incomplete here                                                                   | I cannot verify a degradation-transfer guarantee or independently confirm the recorded venue claim                                                                 | **Partially verified; not decision-bearing**                  |
| Original POPE labels establish answerability after blur/crop                                   | Later records reject this interpretation                                                            | [POPE](https://aclanthology.org/2023.emnlp-main.20/) labels object presence in the source image                                                                                                                          | Scene annotation, visible evidence after transformation, answerability, and model correctness are distinct constructs                                              | **Correction retained**                                       |
| Original POPE contains 400 images/800 questions                                                | Later records correct the count                                                                     | Original COCO construction uses **500 images and 3,000 questions per sampling setting**                                                                                                                                  | Smaller counts describe a custom subset, not the original benchmark                                                                                                | **Earlier count contradicted**                                |
| High degraded AUROC proves ranking survives; low ECE proves useful abstention                  | Records identify these interpretation errors                                                        | Neither conclusion follows from those metrics alone                                                                                                                                                                      | Compare matched conditions; report calibration, ranking, risk and coverage separately. AURC also depends on underlying error rate                                  | **Corrections retained**                                      |
| A 5% empirical risk target is a safety guarantee                                               | Later records explicitly withdraw that claim                                                        | BCEA illustrates how much additional statistical structure an actual certificate requires                                                                                                                                | Small grouped samples and distribution shift invalidate casual guarantee language                                                                                  | **Use “empirical target” only**                               |
| Answerability is equivalent to model ignorance                                                 | Earlier exploration sometimes blurred these constructs                                              | [UNK-VQA](https://arxiv.org/html/2310.10942v3) includes ambiguity, missing concepts and knowledge difficulty; [MM-AQA](https://arxiv.org/html/2604.14799v1) separately evaluates answerability and answer outcomes       | A model can answer an answerable question incorrectly, or guess an unsupported answer correctly                                                                    | **Answerability remains viable, with label restrictions**     |
| Efficiency is automatically a contribution                                                     | Canonical specification requires a reliability question                                             | Bigger or Cheaper already links quantization to uncertainty; [The Cost of Reasoning](https://arxiv.org/html/2603.16728v2) links inference choices to overconfidence                                                      | “Compare precisions/models” is insufficient. The residual mechanism must be isolated                                                                               | **Only a narrower interaction study remains**                 |
| Strong learned selectors make simple audits obsolete                                           | Records mention learned evidence selection                                                          | [SIEVES](https://arxiv.org/html/2604.25855v1) studies learned scoring of localized evidence and OOD transfer                                                                                                             | That does not establish whether cheap answer/object cues explain confidence-based selection in binary existence benchmarks                                         | **No blanket rejection warranted**                            |

Two additional limitations matter:

* The older corruption study [Know What You Do Not Know](https://aclanthology.org/2025.trustnlp-main.16.pdf) evaluates proprietary models, small image sets and verbalized confidence; refusals are excluded from ordinary correctness/confidence analysis. Its findings should not be generalized directly to native logits in small open models.
* The records contain **no documented successful baseline execution**. A reported paper inspection, available repository, or proposed notebook is not experimental reproduction.

Long-context, continual-learning, planning, clinical and hardware-dependent directions remain parked. Nothing found here warrants reopening them.

**B. Candidate comparison**

These are contribution spaces, not three proposed finished theses.

| Candidate contribution space                                              | Exact question                                                                                                                                                       | Closest-work overlap                                                                                                 | Remaining testable uncertainty                                                                                                      | Dataset and split                                                                                   | Open models/baselines                                                                               | Metrics and controls                                                                                                           | Colab feasibility                                                                                 | Useful negative result                                                                                          | Verdict              |
| ------------------------------------------------------------------------- | -------------------------------------------------------------------------------------------------------------------------------------------------------------------- | -------------------------------------------------------------------------------------------------------------------- | ----------------------------------------------------------------------------------------------------------------------------------- | --------------------------------------------------------------------------------------------------- | --------------------------------------------------------------------------------------------------- | ------------------------------------------------------------------------------------------------------------------------------ | ------------------------------------------------------------------------------------------------- | --------------------------------------------------------------------------------------------------------------- | -------------------- |
| **1. Incremental value of confidence beyond answer/object priors**        | Does confidence add error-ranking and selection value beyond predicted answer and queried object, and does that increment transfer across negative-sampling regimes? | POPE studies sampling; Mirage studies yes-bias; recent work studies grounding and detectors                          | Whether pooled confidence performance mostly reflects easy-to-estimate group differences, versus useful within-group discrimination | COCO POPE; source-image-disjoint selector fitting, calibration and testing; paired sampling regimes | Qwen2-VL-2B; SmolVLM2-2.2B; native confidence, answer-only and object-aware selectors               | Conditional AUROC; nested-selector improvement; matched-coverage risk; unchanged-policy transfer; prompt/tokenization controls | Strongest: frozen inference, binary labels, no annotation campaign                                | Confidence retains useful conditional discrimination and transfers: a bounded positive validation of the signal | **Proceed to pilot** |
| **2. Transfer of answerability detection across construction mechanisms** | Does an answerability score trained/calibrated on one perturbation family recognize unanswerability in another, beyond question artifacts?                           | UNK-VQA, TUBench, CARA, MM-AQA and UQBench already study abstention/insufficiency                                    | Mechanism-held-out transfer after separating ambiguous questions, missing evidence and ordinary answer errors                       | UNK-VQA preferred; connected source/variant groups; hold out perturbation families                  | Same small VLMs; explicit answerability score, question-only classifier, simple calibrated selector | Answerability AUROC/F1; false refusal; unsupported answering; answer accuracy conditional on answerability                     | Inference plausible; usable grouped label counts and full release permissions remain unverified   | Failure isolated to one construction family, or transfer survives artifact controls                             | **Reserve**          |
| **3. Quantization × confidence-scoring interaction**                      | Does the apparent reliability cost of 4-bit inference persist when answer representation and confidence extraction are controlled?                                   | Bigger or Cheaper directly studies quantization; other papers show confidence depends on output format and reasoning | Whether precision changes error discrimination itself, or the measured effect is dominated by answer formatting/scoring             | Food-101 with fixed options; image-disjoint development/calibration/test and duplicate checks       | Qwen2-VL-2B FP16 versus NF4; identical processor/decoding; native and candidate-normalized scores   | Accuracy, AUROC, Brier, matched-coverage risk, paired precision×scoring interaction                                            | Small paired experiment plausible; package/configuration reproduction and dataset terms need care | Quantization effect remains stable across scoring definitions, constraining the artifact explanation            | **Reserve**          |

Candidate 1 wins because the question can be tested using existing labels **without claiming to measure transformed-image answerability**, retraining a VLM, or reproducing a complex detector.

**Closest-work comparison for Candidate 1**

The proposed distinction is narrow: *incremental correctness prediction beyond answer/object metadata, under source-image-disjoint negative-sampling transfer*. It is not a claim to invent selective prediction or expose language priors for the first time.

| Closest paper                                                                                | Task, models and data                                                                                      | Intervention/signal and evaluation design                                                                                                                         | Established result                                                                       | Exact overlap and remaining distinction                                                                                                                                 |
| -------------------------------------------------------------------------------------------- | ---------------------------------------------------------------------------------------------------------- | ----------------------------------------------------------------------------------------------------------------------------------------------------------------- | ---------------------------------------------------------------------------------------- | ----------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| [POPE — Evaluating Object Hallucination, 2023](https://aclanthology.org/2023.emnlp-main.20/) | Object existence; LLaVA, MiniGPT-4, mPLUG-Owl, InstructBLIP; COCO, with additional benchmark constructions | Random/popular/adversarial absent-object sampling; accuracy, precision, recall, F1 and yes-rate; benchmark evaluation rather than selector fitting                | Hallucination relates to object frequency/co-occurrence; sampling affects evaluation     | Supplies the task and shift. Does not establish confidence’s conditional added value over answer/object selectors                                                       |
| [The Mirage of Performance Gains…, 2025](https://arxiv.org/html/2504.10020v1)                | Binary hallucination evaluation; LLaVA-1.5 7B/13B and Qwen-VL-Chat; POPE settings                          | Contrasts decoding methods with simple probability/bias controls; evaluates answer accuracy/F1 across sampling settings                                           | Some apparent decoding improvements are explained by simpler output-distribution effects | Direct motivation for strong controls. Candidate holds answers fixed while auditing which answers to retain                                                             |
| [Seeing without Looking, 2026](https://arxiv.org/html/2605.22903v1)                          | Grounding evaluation; LLaVA, Qwen3-VL, Gemma, InternVL and Molmo; POPE, A-OKVQA, MME, AMBER                | Token removal, image interventions, question reformulation and answer-space expansion; paired behavioral/probability analyses                                     | Accuracy can conceal weakened support for an answer                                      | Already studies benchmark shortcuts and probability changes. Candidate tests held-out correctness discrimination conditional on answer/object cues                      |
| [HALP, EACL 2026](https://aclanthology.org/2026.eacl-long.287.pdf)                           | Hallucination prediction; eight VLMs including SmolVLM2; 10,000 examples from six benchmarks               | MLP probes on pre-generation representations; GPT-4-derived outcome labels; stratified 80/20 split; AUROC                                                         | Pre-generation features predict hallucination labels                                     | Strong adjacent detector. Candidate uses deterministic binary correctness, source-image grouping and metadata-conditioned evaluation; does not claim to outperform HALP |
| [BCEA, 2026](https://arxiv.org/html/2606.16667v4)                                            | Claim verification; LLaVA-1.5 and additional open backbones; COCO/POPE                                     | Image-dependence likelihood scores plus acquisition; exact image-level calibration and separate practical evaluations                                             | Acquisition-aware calibration can improve retained coverage                              | Overlaps selective grounding. Candidate uses unchanged images/answers and tests cheap-prior explanations, without acquisition or certificates                           |
| [Density Ridge Selective Prediction, 2026](https://arxiv.org/pdf/2606.10198)                 | QA correctness detection; includes LLaVA-1.5, Idefics3 and SmolVLM; POPE and other QA datasets             | Hidden-trajectory features and repeated generations; 200 calibration queries/60 test queries in the reported setup; queries filtered by correct-generation counts | Reports advantages over several uncertainty baselines in its selected setting            | Already evaluates POPE selection. Candidate avoids success-conditioned sample filtering and tests conditional utility and sampling transfer                             |

I found no inspected experiment in these papers that answers the candidate’s complete question. That supports **pilot differentiation**, not an unrestricted “first-ever” novelty claim.

**Feasibility gate for Candidate 2**

**Exact question:** When source images and their variants are held out together, does an answerability score learned from one construction mechanism generalize to another beyond question-only cues?

Competing explanations can coexist:

* The score detects genuine insufficiency.
* It detects a construction artifact such as unusual wording or a visible mask.
* It primarily detects model difficulty, confusing answerable-but-hard questions with unanswerable ones.
* Apparent transfer differences arise from different label meanings or class proportions.

| Closest paper                                             | Task, models and data                                                                                     | Signal/intervention and evaluation design                                                                                  | Main conclusion                                                              | Overlap and remaining distinction                                                                                                 |
| --------------------------------------------------------- | --------------------------------------------------------------------------------------------------------- | -------------------------------------------------------------------------------------------------------------------------- | ---------------------------------------------------------------------------- | --------------------------------------------------------------------------------------------------------------------------------- |
| [UNK-VQA, 2023/2024](https://arxiv.org/html/2310.10942v3) | Abstention; Otter, OpenFlamingo, InstructBLIP; perturbed COCO/VQAv2 questions                             | Five text/image perturbation types; human answerability labels; zero/few-shot and explanation settings                     | Existing models struggle with appropriate abstention                         | Same core data. Candidate specifically holds out construction mechanisms and controls source linkage/question artifacts           |
| [TUBench, 2024](https://arxiv.org/html/2410.04107v1)      | Answerability across natural images, code, geometry and tables; 28 open/proprietary models                | Ten construction strategies; answerability accuracy, unanswerable F1 and overall answering accuracy                        | Recognition of unanswerability remains weak                                  | Establishes the broad failure. Candidate asks whether a fitted signal transfers between mechanisms, not whether models fail again |
| [CARA/CASE, 2024](https://arxiv.org/html/2405.11145v4)    | Insufficient-context detection; VL-BERT, BLIP/BLIP2 and others; event benchmarks and VQA transfer         | Context-based pseudo-labels and trained detector; source-task training, CASE evaluation and cross-benchmark tests          | Learned insufficiency detection can generalize                               | Transfer is already studied. Candidate isolates perturbation-family transfer in frozen small VLMs with explicit artifact controls |
| [MM-AQA, 2026](https://arxiv.org/html/2604.14799v1)       | Abstention; GPT-5, Claude Sonnet 4.5, Qwen2.5-VL-32B; 2,079 MMMU/document-derived items                   | Evidence sufficiency/modality dependency; prompting and confidence baselines, including oracle threshold selection         | Abstention remains difficult; simple confidence baselines can be competitive | Candidate must add untouched mechanism-held-out policy evaluation, not just another confidence comparison                         |
| [VLM-UQBench, 2026](https://arxiv.org/html/2602.09214v1)  | Modality-specific uncertainty; Kosmos-2, Qwen-VL, LLaVA and GPT-4o-mini; VizWiz, ambiguity data and CLEVR | Token/semantic uncertainty methods; labeled groups and controlled perturbations; AUROC, oracle F1 and sensitivity measures | Signals respond unevenly to different uncertainty sources                    | Candidate separates answerability from correctness and evaluates transfer without target-threshold optimization                   |

**Data gate.** UNK-VQA reports 10,000 examples, split 7,000/1,000/2,000. Its [official repository](https://github.com/guoyang9/UNK-VQA) exposes original-question/image identifiers and perturbation types. However, the full downloadable manifest was not counted here, and original image, replacement image and derived variants must form connected groups. Merely grouping by current filename is insufficient.

Its label taxonomy mixes comprehension, knowledge, missing concepts and ambiguity. Therefore, “all unanswerable items represent absent visual evidence” would be invalid. Repository Apache licensing must also be distinguished from the upstream image rights.

TUBench is an alternative with **2,354 questions**, including a **500-question natural-image subset**, but usable per-mechanism counts and source grouping must be checked in its [release](https://github.com/NLPCode/TUBench). Its small natural-image subset may not support the intended transfer experiment.

**Baseline and controls.** First reproduce the released answerability evaluation. Then compare explicit answerability probability against a question-only bag-of-words classifier, class-prior prediction and a simple calibrated confidence selector. Keep model correctness separate. Required ablations: mechanism-held-out versus mixed-mechanism splits, source grouping, prompt, answerability prevalence and question-only performance.

**Metrics.** Answerability AUROC, unanswerable precision/recall, false-refusal rate on answerable questions, unsupported-answer rate, and answer accuracy on answerable items. Report unchanged-policy results separately from target-retuned diagnostics.

**Compute.** Qwen2-VL-2B and SmolVLM2-2.2B, one answer plus one answerability-scoring pass per item; no VLM training. Actual memory/runtime: **unknown until pilot**. Minimum pipeline check: 100 linked examples spanning two mechanisms. The principal bottleneck is valid labels/groups, not GPU capacity.

**Outcome value.** Transfer failure surviving artifact controls is useful; strong transfer is also defensible. It fails as a thesis if the retained labels cannot distinguish insufficiency from ordinary difficulty, or mechanism groups are too small/disconnected for interpretable estimates. **Reserve because this label-and-group gate remains unresolved.**

**Feasibility gate for Candidate 3**

**Exact question:** For the same small VLM and fixed visual questions, does the FP16-to-NF4 change in error discrimination depend materially on how the answer and its confidence are represented?

Competing explanations:

* Quantization damages useful discrimination between correct and incorrect answers.
* It mainly shifts the confidence scale.
* Formatting, answer length, invalid outputs or confidence-token parsing create much of the observed difference.
* Quantization changes which examples are wrong, altering the evaluated error population.

| Closest paper                                                                           | Task, models and data                                                            | Signal/intervention and evaluation design                                                                    | Main conclusion                                                       | Overlap and remaining distinction                                                                                          |
| --------------------------------------------------------------------------------------- | -------------------------------------------------------------------------------- | ------------------------------------------------------------------------------------------------------------ | --------------------------------------------------------------------- | -------------------------------------------------------------------------------------------------------------------------- |
| [Bigger or Cheaper?, 2026](https://arxiv.org/html/2607.24440v1)                         | Four-option Food-101; Qwen2-VL 2B FP16/NF4 and 7B NF4                            | 100 base items, 19 conditions; internal/verbal confidence; calibration, ranking and clean-threshold transfer | Quantization effects on uncertainty can exceed effects on accuracy    | Direct overlap. Remaining question is the precision×scoring interaction under controlled output representation             |
| [The Cost of Reasoning, 2026](https://arxiv.org/html/2603.16728v2)                      | VQA/reasoning; Gemma, InternVL and Qwen3-VL; OKVQA, MathVista, MMMU-Pro and pets | CoT versus direct answering; token and consistency signals; length/answer-masking controls                   | Reasoning can induce overconfidence; scoring location matters         | Rules out a simplistic “longer answers explain everything” claim. Does not establish the proposed quantization interaction |
| [Unveiling Uncertainty, COLING 2025](https://aclanthology.org/2025.coling-main.208.pdf) | Calibration; LLaVA 7B/13B and Qwen-VL variants; multiple VQA subsets             | Training-stage and modality comparisons using likelihood confidence and calibration errors                   | Calibration changes are not uniformly explained by instruction tuning | Establishes score/context sensitivity; not a matched precision experiment                                                  |
| [VL-Uncertainty, 2024/2025](https://arxiv.org/html/2411.11919v2)                        | Error detection; ten VLMs; MMMU, ScienceQA, MM-Vet, LLaVA-Bench                  | Five perturbation/sampling rounds, semantic clustering and fixed detection threshold                         | Perturbation-based uncertainty can improve detection accuracy         | Supplies an alternative signal family; candidate studies native-score sensitivity to precision without expensive sampling  |
| [Know What You Do Not Know, 2025](https://aclanthology.org/2025.trustnlp-main.16.pdf)   | Corrupted-image QA/counting; GPT-4V, Gemini Pro Vision, Claude 3 Opus; VQA/JUS   | Three corruptions, five severities; verbal confidence/ECE and interval coverage                              | Corruption can worsen confidence–accuracy alignment                   | Establishes older degradation/calibration overlap; does not address open-weight quantization or scoring controls           |

**Data gate.** The [official Food-101 page](https://data.vision.ee.ethz.ch/cvl/datasets_extra/food-101/) specifies 101,000 images: 750 training and 250 reviewed test images per category. Use the reviewed split, fixed distractors and fixed answer order; partition by image and audit duplicates before making prompt variants. Dish-class labels support classification correctness, not post-degradation answerability.

Its [dataset card](https://huggingface.co/datasets/ethz/food101) reproduces terms referring to scientific fair use and original picture owners. This is not a blanket permissive image license. I would not describe its legal gate as fully closed merely because the download is public.

**Baseline and controls.** Reproduce the small-model arms from the [released repository](https://github.com/Asif-Ferdous/vlm-scale-quant) before adding comparisons. Then vary only precision and scoring: free answer-span likelihood versus fixed candidate likelihood; preserve processor resolution, prompt, options and decoding. Score the same fixed candidate under both precisions as an additional diagnostic. Agreement-only subsets are descriptive controls, not unbiased causal estimates.

**Metrics.** Paired precision×scoring differences in AUROC and selective risk, plus accuracy, invalid-output rate, Brier and latency/memory. Distinguish scale recalibration from ranking change. Do not select the confidence definition using final-test performance.

**Compute.** Qwen2-VL-2B, loaded sequentially in FP16 and NF4; 100 images × two precisions × two answer formats for the smallest pilot. Actual peak memory/runtime and package compatibility are **unknown until pilot**. If the full-precision reference cannot run consistently, this comparison fails; substituting a different model would not preserve the question.

**Outcome value.** Either scoring-sensitive or scoring-stable quantization effects are useful. It fails if differences reduce entirely to an obvious parser bug with no remaining scientific uncertainty, or the original result cannot be reproduced. **Reserve: narrower than the original direction, but direct-overlap and reproduction risks exceed Candidate 1.**

**C. Selected pilot: confidence beyond answer/object priors**

**Working title**

*Beyond Answer Bias: Auditing Confidence-Based Selection in Small Vision–Language Models*

**Exact research question**

> On binary object-existence questions, how much additional correctness-prediction value does native VLM confidence provide beyond predicted answer and queried-object identity, and does that increment transfer from random to popular/adversarial negative sampling on unseen source images?

This is an evaluation-validity question. A confidence score can be operationally useful because “yes” answers are less reliable than “no” answers. That is real predictive information. The audit asks whether it also identifies **which answers within those groups are unreliable**.

Even a successful conditional result would not, by itself, prove that confidence measures visual grounding.

**Falsifiable hypothesis**

Let

$$
\Delta_k=R_k(\text{metadata selector})-
R_k(\text{metadata + confidence selector})
$$

at 80% coverage in sampling condition \(k\), where lower selective risk is better.

The pilot hypothesis is:

> Confidence’s incremental risk reduction is smaller on adversarial negatives than on random negatives by at least two percentage points.

The two-point margin is a proposed practically meaningful effect, not a literature-derived constant. Fix it before inspecting the final test. The pilot should estimate whether the available number of independent images can resolve an effect of that size.

This hypothesis can be rejected without invalidating the thesis space.

| Explanation                                                          | Evidence that would support it                                                                                        |
| -------------------------------------------------------------------- | --------------------------------------------------------------------------------------------------------------------- |
| **Group composition explains much of pooled confidence performance** | Answer-only/object-aware selectors match confidence; within-answer discrimination is weak                             |
| **Confidence carries additional instance-level information**         | Adding confidence improves held-out prediction and selective risk beyond metadata; within-answer AUROC remains useful |
| **Confidence’s value depends on negative sampling**                  | Incremental benefit changes across regimes even after metadata controls                                               |
| **Scale transfer fails more than ranking**                           | Ranking remains similar, while unchanged thresholds produce different coverage/risk; independent recalibration helps  |
| **Output representation drives the finding**                         | The conclusion changes under controlled tokenization, answer-format or prompt checks                                  |

These explanations are not mutually exclusive.

**Dataset and leakage-resistant design**

Use the **COCO portion of POPE**, retaining its random, popular and adversarial negative sets. The accessible [evaluation mirror](https://huggingface.co/datasets/lmms-lab-encoder/POPE) displays 9,000 rows and 500 image sources. Treat the [official POPE release](https://github.com/RUCAIBox/POPE) as authoritative and verify mirror correspondence during setup.

The three sampling conditions are **not independent train/validation/test splits**.

Proposed partition:

| Partition                    | Source images | Permitted use                                                         |
| ---------------------------- | ------------: | --------------------------------------------------------------------- |
| Selector fitting/development |           150 | Fit metadata selectors; choose regularization and finalize extraction |
| Calibration                  |           100 | Fit probability mapping or select operating thresholds                |
| Final test                   |           250 | Evaluate all three sampling regimes without adaptation                |

Assign every question, repeated positive query and sampling variant from an image to the same partition. Add exact-image hashes and near-duplicate checks; merge duplicate groups before partitioning, adjusting counts if necessary.

For the pilot, use 100 images **inside the fitting/development pool**, internally divided for fitting/calibration/testing. The eventual 250-image final test remains untouched.

Additional validity requirements:

* Keep repeated positives paired across regimes; do not count them as independent evidence.
* Bootstrap source-image groups, preserving all associated questions and conditions.
* Use only fitting-set information to derive object frequencies or metadata features.
* Do not fit on target-regime labels for the primary transfer comparison.
* Audit annotation disagreements on a small sample; retain an explicit “benchmark correctness” interpretation.
* Source-image disjointness prevents selector leakage, **not unknown VLM pretraining contamination**.

**Access and license.** POPE’s repository is MIT-licensed. COCO’s [displayed terms](https://cocodataset.org/#termsofuse), inspected directly, license annotations under CC BY 4.0 but leave photograph rights with their owners under the linked Flickr conditions. Preserve image provenance/license metadata; distribute code, IDs, manifests and derived scores rather than assuming unrestricted photograph redistribution. Per-image provenance confirmation belongs in the first-day manifest check.

**Baseline reproduction first**

1. Load Qwen2-VL-2B using its official processor and chat template.
2. Run ordinary deterministic short-answer inference on the pilot subset.
3. Evaluate with POPE’s released evaluator and independently reconcile the confusion matrix, yes-rate and invalid responses.
4. Save raw outputs and exact software/model revisions.
5. Only after this works, add confidence extraction and selectors.

This reproduces the **open evaluation pipeline**. It is not a claim to reproduce a historical headline score obtained with another checkpoint or prompt.

**Minimum viable experiment and simple baselines**

Use the same frozen model answers when comparing selection policies.

| Baseline/comparison                                                | Purpose                                                                      |
| ------------------------------------------------------------------ | ---------------------------------------------------------------------------- |
| Random acceptance                                                  | Establish expected risk without informative selection                        |
| Answer-only selector: estimated correctness given predicted yes/no | Test whether response-class asymmetry explains apparent utility              |
| Object + answer selector, with regularization/shrinkage            | Strong inexpensive control for queried-object difficulty and sampling priors |
| Native answer confidence                                           | Establish ordinary confidence-based selection                                |
| Object + answer + confidence selector                              | Measure confidence’s incremental held-out value                              |
| Explicit “is this answer correct?” score on a capped subset        | Optional stronger simple comparator if native confidence adds little         |

The proposed contribution is the **controlled audit and reusable protocol**. No new VLM intervention is required.

For confidence extraction:

* Record raw likelihood for the actual answer.
* Separately evaluate a fixed yes/no candidate-scoring formulation.
* Verify tokenizer behavior and valid-answer probability mass.
* Report when candidate-constrained answers differ from ordinary generated answers; do not silently replace one task with the other.
* Do not present binary entropy, maximum probability and margin as three independent signals when they are monotonic transformations of the same normalized binary distribution.

Required ablations are removal of object features, removal of answer identity, two fixed prompt templates, and ordinary versus candidate-constrained answering. Keep input resolution fixed in the main experiment. A small resolution sensitivity check can be secondary; it is not a return to the previous degradation thesis.

**Metrics and interpretation**

| Claim                                                  | Direct measurement                                                                                                         |
| ------------------------------------------------------ | -------------------------------------------------------------------------------------------------------------------------- |
| The model answers correctly                            | Accuracy, confusion matrix, yes-rate, invalid-output rate                                                                  |
| Confidence discriminates errors within response groups | AUROC separately for predicted yes/no; pooled AUROC reported alongside                                                     |
| Confidence adds value beyond cheap cues                | Held-out difference between metadata and metadata-plus-confidence selectors; log loss/Brier and selective-risk differences |
| Selection improves retained answers                    | Risk at fixed 50%, 80% and 90% coverage; risk–coverage curves                                                              |
| A fitted policy transfers                              | Freeze fitting/calibration on random negatives; report realized risk **and coverage** on popular/adversarial test sets     |
| Calibration transfers                                  | Reliability plots and Brier; ECE secondary with disclosed bins                                                             |
| Effects generalize across the tested conditions        | Condition-specific results and paired source-image confidence intervals                                                    |

Fixed-coverage curves are offline ranking diagnostics: they may use the test score distribution, but not test labels, to retain a specified fraction. They must be distinguished from an unchanged deployment threshold.

For tied metadata scores, use a prespecified randomized tie policy and report tie variability. If an answer group has no errors, its AUROC is undefined—not perfect.

AURC is secondary because comparisons across models/conditions also reflect base accuracy. No safety guarantee is claimed.

**Compute and reproducibility**

| Component                  | Plan and evidence                                                                                                                                                                                            |
| -------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------ |
| Primary model              | [Qwen2-VL-2B-Instruct](https://huggingface.co/Qwen/Qwen2-VL-2B-Instruct), nominal 2B, Apache 2.0; official Transformers example available                                                                    |
| Independent model/fallback | [SmolVLM2-2.2B-Instruct](https://huggingface.co/HuggingFaceTB/SmolVLM2-2.2B-Instruct), Apache 2.0; official inference code available                                                                         |
| Memory                     | Qwen peak memory for this configuration: **unknown until pilot**. SmolVLM2’s card reports 5.2 GB for its video-inference setting; that is supporting feasibility evidence, not a guarantee for this notebook |
| Precision                  | Start with ordinary half-precision inference; avoid making quantization an uncontrolled difference between models                                                                                            |
| Pilot workload             | At most 100 images × 18 question rows × two models = 3,600 question–model evaluations, before duplicate reuse and capped prompt checks                                                                       |
| Full core workload         | 9,000 rows × two models = 18,000 question–model evaluations; generation/scoring may require more than one forward pass                                                                                       |
| Training                   | CPU-scale regularized selectors only; no LoRA or backbone training                                                                                                                                           |
| Bottlenecks                | Model download/loading, image preprocessing, visual-token count, confidence extraction and Colab interruptions                                                                                               |
| Runtime                    | **Unknown until pilot**; measure warm latency, total elapsed time, peak allocated/reserved memory and restart cost                                                                                           |
| Reproducibility            | Pin checkpoint/repository/package revisions; cache raw answers and scores; preserve split hashes, prompts, exclusions and seeds                                                                              |

Both models have maintained ecosystem inference paths, but the exact Colab environment is untested. If Qwen fails, SmolVLM2 can validate the pipeline. A one-model thesis would need an explicit limitation; the fallback does not automatically replace independent replication.

**Positive, negative and failure outcomes**

| Outcome                                                                               | Interpretation and value                                                                                             |
| ------------------------------------------------------------------------------------- | -------------------------------------------------------------------------------------------------------------------- |
| Cheap cues explain most pooled confidence utility                                     | Useful audit result, provided estimates are precise and the finding survives prompt/model controls                   |
| Confidence adds value on random negatives but loses it under adversarial sampling     | Useful transfer limitation, with a diagnostic separation of composition, scale and ranking                           |
| Confidence remains useful within groups and transfers                                 | Useful negative result for the shortcut hypothesis; supports this confidence signal within a clearly bounded setting |
| Different model families behave differently                                           | Valuable if the distinction survives the same controls; not a license to generalize from two models                  |
| Wide intervals, too few within-group errors, unresolved labels or unstable extraction | **Pilot failure/inconclusive**, not evidence for or against the hypothesis                                           |
| Only a parser bug or already-known yes-rate difference remains                        | Insufficient thesis contribution unless a separate substantive uncertainty survives                                  |

A careful null result can be a defensible undergraduate empirical thesis. Publication is possible, not assured; it would require convincing precision, reproducibility and significance beyond one arbitrary model–prompt combination.

**Five-working-day pilot**

| Day                                          | Concrete work                                                                                                                                   | Deliverable and decision gate                                                                                                                                    |
| -------------------------------------------- | ----------------------------------------------------------------------------------------------------------------------------------------------- | ---------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| **1 — Verify data and reproduce evaluation** | Build provenance manifest; reconcile official/mirror labels; group images/variants; freeze final-test IDs; run a small ordinary-inference batch | Manifest, license/provenance record, split file, raw outputs and reconciled POPE confusion matrix. Stop if data alignment or permitted use cannot be established |
| **2 — Validate confidence extraction**       | Finish primary-model pilot; check yes/no tokenization, raw versus normalized probabilities, invalid responses and deterministic reruns          | Cached prediction/score table; extraction checks; measured memory/runtime. Stop if scores do not reliably correspond to the evaluated answers                    |
| **3 — Test cheap explanations**              | Fit answer-only, object-aware and confidence-augmented selectors using internal pilot partitions                                                | Pooled/conditional AUROC and matched-coverage risk plots with image-group intervals; explicit tie handling                                                       |
| **4 — Test transfer and replication**        | Freeze random-condition policies; evaluate popular/adversarial conditions; run second model and capped prompt ablation                          | Paired transfer table, realized coverage/risk, and model/prompt sensitivity report                                                                               |
| **5 — Make the thesis decision**             | Examine error counts, confidence-interval width, simple-control explanations and projected full-study precision                                 | Short go/no-go memo, reproducible notebook, locked protocol and full-study workload estimate                                                                     |

The day-five decision must not depend on obtaining a flattering result. Continue if the pipeline is reproducible, the estimand is supported by the labels, and the full experiment can distinguish a meaningful incremental effect—or meaningfully rule one out.

**Decisive recommendation: run Candidate 1’s five-day pilot and keep the thesis title provisional until its data, extraction and statistical-information gates pass.**
