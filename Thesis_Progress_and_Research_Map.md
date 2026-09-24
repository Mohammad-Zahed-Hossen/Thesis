Thesis Progress and Research Map

From selecting VLM and MLLM to the present topic discovery stage

Prepared for Mohammad Zahed Hossen
Record through 14 September 2026 | Consolidated from eleven supplied documents and visible project conversation

## Your current position

**You have made substantial progress in defining the research scope, identifying nearby work, and correcting weak candidate claims. You have not yet established one exact thesis question, a defensible original contribution, or experimental results. The most accurate description is: field selected, reliability subfield established, topic discovery audited but unresolved.**

Your work is more advanced than “I only know VLM/MLLM.” You have explored what can go wrong when a model answers from weak visual evidence, how confidence should be evaluated, and why several attractive topic formulations do not yet justify a thesis. However, the documents do not prove that you personally understand or have deeply read every paper they mention.

| **Settled** | **Still open** |
| --- | --- |
| Parent field: Multimodal / Vision-Language Learning and Systems | Exact question, contribution and final thesis title |
| Primary lane: trustworthy and reliable generative MLLMs | Final task, dataset, model and method |
| Open models, public data and bounded undergraduate scope | Demonstrated runtime, reproduced baselines and results |
| Five recently explored areas are now parked by your instruction | Whether an earlier reliability candidate deserves renewed attention |

## How to read this report

Read Sections 1–4 for the mental map and progress assessment. Sections 5–8 explain the candidate history and corrections. Sections 9–14 cover the five-area exploration, papers and research assets. Sections 15–18 give the current decisions, source record, limitations and a reusable handover.

This is a retrospective progress report, not another topic recommendation. It does not introduce an execution requirement or ask you to select a topic now. Source codes such as [S08] identify the attached documents listed in Section 16. [U1] and [U2] identify the latest visible user instructions.

# 1 Your research map

The hierarchy matters: a field is the broad territory; a lane identifies the type of problem; a subfield narrows the behavior of interest; an exact thesis question specifies what will be investigated. Your earlier reports sometimes used these levels interchangeably. [S01 §§2–4; S03 §§1–3; S04 §3]

## Your subfield in ordinary language

Can a model tell when the image actually supports its answer, and can it withhold an answer when its evidence or confidence is inadequate? Missing evidence, conflicting image and text, and degraded images are different possible conditions within that subfield. They are not three commitments to three separate theses.

The formal working label is “Trustworthy generative MLLMs: evidence-grounded calibration and selective abstention under missing, conflicting, or degraded visual evidence.” The shorter label is “Evidence-Grounded Uncertainty and Selective Prediction in Generative MLLMs.” [S03 §§1,9]

# 2 How the work developed

The sequence below uses document dates when available and relative order when dates are unclear. Several reports share a date; their logical dependencies are more reliable than an invented hour-by-hour chronology.

| **Period or step** | **Work recorded** | **What it changed** |
| --- | --- | --- |
| 22 August 2026 | Canonical field specification and parked-field record. [S01–S02] | Fixed the parent field, ranked three lanes and defined resource and contribution boundaries. |
| By 3 September | Early handover organized the trustworthy-MLLM subfield. [S03] | Moved from general VLM exploration to grounding, uncertainty and selective abstention. |
| Early September conversations | Paper-reading system, core reading suggestions and an end-to-end research mental model were discussed. [C] | Recognized the need to understand the workflow and use public datasets; no completed reading log was demonstrated. |
| By 13 September | Astra narrowing report examined internal probes, passive degradation and explicit answerability. [S10] | Separated three questions that had been mixed together; identified overlap and score-definition problems. |
| Subsequent threshold report | Gemini report promoted threshold transfer versus ranking failure. [S11] | Offered a more concrete direction, but its central absence claim was later contradicted. |
| 14 September handover and audit | Corrections were consolidated and eight focal papers compared. [S04, S08] | Kept the topic open; reframed the best-developed candidate as a possible replication and diagnostic extension. |
| 14 September expansion | Claude, Perplexity and a targeted report screened five additional areas. [S05–S07] | Opened a bounded long-context and multi-image branch, alongside memory, learning and planning. |
| 14 September cross-report audit | Compared the three reports and checked decisive claims. [S09] | Downgraded claimed novelty and feasibility; no exact topic was approved. |
| Latest project decision | You asked to park all five newly explored areas. [U1] | Overrides the earlier recommendation to investigate long context further. |
| Current request | You asked for a complete progress report and mental map. [U2] | The immediate goal is consolidation and understanding, not another direction search. |

The path was not a straight series of successful topic selections. It was a narrowing process with reversals: propose a question, inspect overlap, correct the claim, then either retain a narrower possibility or park it. That describes the work more accurately than counting reports as completed thesis chapters.

# 3 How much progress you have made

| **Work dimension** | **Documented status** | **Evidence and practical meaning** |
| --- | --- | --- |
| Field selection | Established | One parent field and three ranked lanes are recorded. This decision has survived later exploration. [S01–S04] |
| Subfield selection | Established working focus | Reliability through grounding, uncertainty and selective prediction is the consistent center. [S03–S04] |
| Scope control | Substantial | You have identified resource boundaries, unsuitable thesis identities and conditions for meaningful contribution. [S01–S02] |
| Literature discovery | Substantial exposure | The reports contain many named papers and method families. This establishes discovery, not personal mastery. [S03–S11] |
| Critical literature assessment | Substantial but incomplete | Two audits overturned important claims. Their primary-source checks are reported in the documents, not independently rerun here. [S08–S09] |
| Candidate formulation | Developed but unresolved | Several bounded questions exist; none has a settled contribution boundary. [S08–S10] |
| Personal paper understanding | Not demonstrable from files | No complete author-written reading log or comprehension record was supplied. Your current message reports continuing confusion. [U2] |
| Final experimental design | Provisional only | There are proposed tasks, splits, signals and metrics, but no final approved protocol. [S04, S08–S09] |
| Implementation and reproduction | Not documented | No thesis code, inference logs, reproduced baseline tables or resource measurements were supplied. [S04, S08–S09] |
| Research findings and thesis writing | Not documented as results | The artifacts are planning, screening and audit documents. They are not an empirical results chapter. |

## What counts as progress here

You have reduced several uncertainties about what the thesis should not claim. For example, you now have a record explaining why “visual perturbation estimates uncertainty” and “position affects visual answers” are insufficient novelty claims on their own. Avoiding those weak claims is useful research preparation.

## What the record cannot honestly quantify

There is no defensible “60 percent complete” estimate. The documents record neither hours spent nor demonstrated understanding, and research stages have unequal workloads. You are advanced in scoping and evidence checking, but still before an exact topic commitment and documented execution.

# 4 Why the work still feels unclear

My interpretation is that your information collection has advanced faster than its consolidation into a stable explanation. This is a diagnosis of the document pattern, not a claim about your ability.

## Different levels were mixed

VLM was discussed beside continual learning, memory, efficiency, charts, Bengali questions and token pruning. These are not equivalent choices. Some are fields, some are tasks, some are methods and some are conditions. Without a hierarchy, every new term looks like another possible thesis.

## Recommendations changed without a single visible status record

One report called a question promising; another called its central gap unsupported. The cross-report audit preferred long context, then you parked all five areas. If you remember the recommendations but not the later corrections, several incompatible “current directions” remain in your mind. [S08–S11; U1]

## The candidate labels were reused

“Candidate 1,” “Candidate 2” and “Candidate 3” did not have stable meanings across all reports. In particular, Candidate 3 meant explicit out-of-frame answerability in Astra, but object-scale/evidence-sufficiency analysis in later handover and audit material. Those are related interests, not the same research question. This report gives them separate descriptive names. [S04 §6; S08 §3; S10 §5]

## The reports created an impression of greater certainty

Some reports said “verified gap” or gave precise runtime numbers. Later audits challenged those claims. A long report with a detailed implementation plan can still rest on an incorrect description of one competing paper. [S08 §2; S09 §3]

## Research exposure was mistaken for learning completion

A generated extraction table can tell you which papers exist without giving you an intuitive understanding of their differences. None of the supplied files establishes that every listed paper was personally read, understood, annotated or reproduced by you. The inventory therefore records exposure and reported audit depth separately.

## The stable explanation you can retain

**I selected VLM/MLLM, then narrowed toward reliable answering from visual evidence. I explored uncertainty probes, degraded-input confidence and answerability, and found substantial prior-work overlap. I later screened five other areas and parked them. I have a clearer boundary and literature map, but I have not yet chosen the exact scientific question.**

# 5 The central concepts in plain English

Use one example throughout: a model receives a photograph and the question “Is there a bicycle?” The photograph may be clear, blurred, cropped, or accompanied by misleading text. The following distinctions were repeatedly developed in your reports. [S03 §6; S04 §§4,6; S08 §§2,4; S10 §§2,4]

| **Concept** | **Meaning in this example** | **Do not confuse it with** |
| --- | --- | --- |
| Visual grounding | The answer uses the relevant visible evidence about the bicycle. | Giving the correct answer by guessing from common scene patterns. |
| Scene truth | A bicycle existed in the original photographed scene. | Whether the current cropped or blurred picture still reveals it. |
| Answerability | The supplied picture contains enough information to answer the question. | Whether this particular model happens to answer correctly. |
| Native confidence | A score derived from the model’s answer probabilities. | A proven probability that the answer is correct. |
| Verbalized confidence | The model writes “I am 90 percent confident.” | The same measurement as internal answer probabilities. |
| Calibration | Across similar confidence levels, stated confidence agrees with observed correctness. | Simply having high accuracy or high confidence. |
| Error ranking | Correct answers tend to receive higher confidence than incorrect ones. | Having the right numerical confidence scale. |
| Acceptance threshold | A cutoff deciding which answers the system returns. | Changing the underlying visual information or answer model. |
| Selective prediction | Return some answers and withhold others. | Making every answer more accurate. |
| Selective risk and coverage | Risk is error among returned answers; coverage is the fraction returned. | Low error obtained by answering almost nothing. |
| Distribution shift | The evaluation or deployment inputs differ from the calibration setting. | A completely different research field. |

Illustration only: if a system returns 60 of 100 answers and 3 returned answers are wrong, coverage is 60 percent and selective risk is 5 percent. These numbers explain the terms; they are not your experimental results.

An answer cutoff can become unsuitable after images get blurrier even if the score still orders many correct answers above wrong ones. Alternatively, the ordering itself can worsen. Both can happen together. This is why the project separated threshold behavior from ranking behavior.

# 6 The reliability candidates you explored

## A Internal visual probe for uncertainty

Question explored: when a clean image is available, does one internally resized or degraded copy help identify errors beyond the model’s ordinary confidence? The final answer concerns the original input. The extra view supplies a possible reliability signal. [S10 §5 Candidate 1; S04 §6 Candidate 1]

Why it attracted attention: it seemed possible to obtain a useful signal without retraining a large model. The problem is that perturbation-based uncertainty is already a substantial research family. VL-Uncertainty, semantic-perturbation calibration and VL-Calibration were identified as close conceptual overlap. A cheaper version is not automatically a new scientific contribution.

A further correction concerned the proposed score: Astra recovered a formula that rewarded disagreement, although the surrounding explanation described stability. Sensitivity to image changes may indicate dependence or brittleness; it does not by itself show which answer is correct. [S10 §2]

Latest recorded status: parked pending evidence of incremental value beyond native confidence. It is not a selected method or completed experiment. [S08 §§5,7]

## B Passive degraded input and acceptance policy transfer

Question explored: if the model receives a low-detail image, how do its confidence ranking and an acceptance cutoff fitted on clear images behave? A separate cutoff fitted using labeled degraded examples was proposed as an offline comparator. [S04 §§4,9; S08 §4]

The distinction from A is the information available at use time. In A, the system has the original image and creates an extra view. In B, the system receives the degraded image; it is not allowed to consult an unavailable clean original to make its decision.

Evolution: Astra recommended a closer literature check; Gemini then claimed the combined ranking-and-transfer comparison was missing; the later topic-selection audit reported that Bigger or Cheaper? already performed clean-threshold transfer and condition-wise ranking. The broad novelty justification therefore did not survive. [S10 → S11 → S08]

What remained: a possible replication and diagnostic extension involving independent calibration/testing and a risk-targeted policy. The audit stressed that better bookkeeping, a new dataset or another small model is insufficient unless the extension changes a meaningful conclusion.

Latest recorded status: the best-developed unresolved reliability candidate, not an approved topic and not automatically reactivated because other areas were parked. No personal experimental result establishes that its hypothesized behavior occurs. [S08 §§4,7; S09 §7]

# 7 Answerability and other reliability branches

## C1 Explicit missing evidence outside the frame

Astra’s third candidate asked: can confidence separate “the model may be wrong” from “the picture cannot answer this question”? Its proposed setting was evidence outside the image frame, using an answerable/unanswerable task rather than pretending that ordinary object labels establish visibility. [S10 §5 Candidate 3]

Example: asking the color of a bicycle that is outside the photograph is different from asking whether a clearly pictured bicycle is red. A YES/NO score cannot automatically express that the needed evidence is absent.

The report identified TUBench’s UVQA component and CARA/CASE as nearby work. The unresolved questions concerned existing overlap, usable category counts and independent image groups. This branch was proposed, but the supplied record does not show a later completed candidate-specific decision. Treat it as an unresolved historical option, not an active commitment.

## C2 Object scale and evidence sufficiency

Later material used Candidate 3 or Candidate C for a different question: do confidence and degradation effects differ for small, medium and large target objects? COCO geometry made this measurable, but object size did not establish whether evidence was sufficient. [S04 §6; S08 §§3–5]

Example: a large object can be occluded, while a small object can remain recognizable. An absent object has no target-object area. Several instances of the same category require an explicit aggregation rule. These complications make “small object” a subgroup description, not a ground-truth answerability label.

Latest recorded status: parked as a thesis identity; potentially an explanatory analysis within a separately justified question. Evidence-Order Calibration was a close conceptual comparator for targeted evidence loss. [S08 §7]

## Other themes inside the selected lane

| **Theme encountered** | **Role in the research history** | **Recorded boundary** |
| --- | --- | --- |
| Image and text conflict | CLASH and cross-modal evidence motivated the subfield. [S03] | No exact conflict-focused topic selected. |
| Charts and documents | Possible settings for grounding and OCR reliability. [S01, S03] | A setting does not supply the contribution. |
| Static spatial reasoning | Possible controlled visual failure condition. [S03] | Do not silently expand into robotics or 3D. |
| Bengali and English VLM answers | Discussed in project conversation. [C] | Language comparison alone was not established as a thesis contribution. |
| Reliability and efficiency | Quantization, pruning and token budgets were considered. [S01, S03] | Efficiency remains conditional on a clear reliability or systems claim. |

# 8 Corrections that changed the direction

These are conclusions recorded by the supplied audits. This report consolidates their effect on your progress; it does not claim to have rerun the external paper and repository checks.

| **Earlier claim or confusion** | **Correction retained** | **Effect on your decisions** |
| --- | --- | --- |
| No paper compares clean-threshold transfer with ranking under degradation. | S08 reports that Bigger or Cheaper? does both; S09 also confirms the broad transfer overlap. | The central novelty claim for B must be withdrawn. |
| Ranking survives because degraded AUROC is high. | A matched clean-to-degraded comparison is needed to assess change. [S04, S08] | Do not infer preserved ranking from one high score. |
| Threshold drift versus ranking loss is a strict binary. | They can coexist; retuning does not causally decompose their shares. [S04, S08] | Keep policy behavior and ranking as separate measurements. |
| A copied percentage is AUROC. | S04/S08 identify VL-Uncertainty detection accuracy being mislabeled. | Do not compare unlike metrics. |
| Original POPE labels identify answerability after blur. | They concern source-scene object existence; transformed visibility needs separate support. [S08] | Use narrower claims about correctness under perception shift. |
| 400 images and 800 questions are the original POPE setting. | S08 records 500 source images and 3,000 questions per original sampling setting. | Smaller designs must be labeled custom subsets. |
| A 5 percent target is a deployment guarantee. | A target and observed error rate are not a proved guarantee under shift or dependence. [S08–S09] | Avoid unsupported safety language. |
| The position by length by modality combination is new. | S09 reports that MMLongBench already includes these dimensions. | Perplexity’s broad novelty claim is rejected. |
| LAD omits small models and similar visual distractors. | S09 reports Qwen2.5-VL-3B and similar-distractor experiments. | The targeted report’s main gap justification fails. |
| SoFA is a runnable baseline; 11.7 GB and 320 ms are measured. | S09 found a release-placeholder repository and no supporting profiling record. | Code readiness and measured feasibility remain unestablished. |
| Memory requires proprietary judges; hierarchy requires RL; visual planning is not real VLM work. | S09 rejects these universal claims. | Park for specific scope and workload reasons, not false categorical rules. |

A traceability disagreement also remains: S08 records a pinned code inspection of the calibration split, while S09 could not reverify that assertion from S07’s damaged citation. This is an evidence-access difference, not proof that the inspected code did or did not change. No empirical reproduction is documented in either audit.

# 9 The five area exploration and its outcome

You explicitly explored continual learning, memory systems, long context, long-horizon planning and hierarchical planning. “Continue learning” in those requests was interpreted as the research area continual learning. The reports did not approve a replacement parent field. [S05–S09]

| **Area** | **What you examined** | **Current status** |
| --- | --- | --- |
| Continual learning | Learning from successive tasks while retaining earlier capabilities; replay, adapters, forgetting and VLM alignment. | Parked by U1. S09 corrected claims that every version is outside VLM scope or necessarily infeasible. |
| Memory systems | External records, episodic/semantic/procedural memory, retrieval, updating and preservation of visual detail. | Parked by U1. Integration burden and a weakly isolated research question remained concerns. |
| Long context and multi-image use | Evidence position, context length, image order, distractors, citation fidelity and confidence. | Parked by U1, despite S09 previously ranking a bounded version first for further investigation. |
| Long-horizon planning | Execution over many steps, state tracking, delayed consequences, error recovery and environment setup. | Parked by U1. No bounded justified candidate was established. |
| Hierarchical planning | High-level subgoals, low-level actions, validity of decomposition and propagation of errors. | Parked by U1. Hierarchy alone was not a scientific contribution or reason to change field. |

## How the three reports differed

Claude explicitly described a screening-depth search and withheld topic approval. Perplexity more strongly favored visual position and context-length analysis. The targeted feasibility report promoted a distractor/position intervention and supplied detailed resource estimates. [S05–S07]

The cross-report audit found that their agreement on a broad area was not independent proof of a gap. MMLongBench, MMLongCite and LAD already covered important parts of the proposed territory. It retained only a conditional selective-reliability question and a separately gated degradation reserve. It did not establish an execution-ready thesis. [S09 §§2–7]

## What this branch contributed to your progress

It clarified that storing information, fitting information into a context window, learning new parameters and executing plans are different research objects. It also exposed a recurring mistake: a problem can be real and interesting while the proposed contribution is already known, insufficiently isolated, or too costly to evaluate.

Your later instruction parks all five. This report preserves their history without turning the formerly highest-ranked option into a current recommendation. [U1]

# 10 Core paper inventory

Inventory rule: “audit-reported inspection” means a supplied audit says it inspected primary material. It does not mean this progress report independently authenticated it, or that you personally read it. No personal reproduction is documented for any item below.

## POPE

Role: the central object-existence evaluation lead. It helped turn broad hallucination discussion into a constrained image question with an external correctness label.

Status: core foundation, discussed since early reading suggestions; source and construction examined in S08 §4.3. Its labels do not establish post-degradation answerability.

[Source link recorded in the supplied reports](https://aclanthology.org/2023.emnlp-main.20/)

## Unveiling Uncertainty and MLLM calibration

Role: an early foundation for understanding whether model confidence agrees with actual correctness. This connected the VLM field to the selected uncertainty and calibration subfield.

Status: recommended/discussed in S03 and visible early-September conversation. A completed personal extraction or reproduction is not documented.

[Source link recorded in the supplied reports](https://aclanthology.org/2025.coling-main.208/)

## Know What You Do Not Know

Role: uncertainty under corrupted images. It challenged any claim that corruption-aware confidence evaluation was entirely absent.

Status: audit-reported full-text inspection in S08 §2. The audit distinguishes proprietary-model verbalized confidence from native token-confidence behavior. Earlier S11 corruption counts and model details should not be reused uncritically.

[Source link recorded in the supplied reports](https://aclanthology.org/2025.trustnlp-main.16/)

## VLM RobustBench

Role: visual degradation and task robustness. It supplied context for transformations and controls, but task degradation alone did not answer the selective-policy question.

Status: audit-reported full-text inspection in S08 §2. Relevant as robustness context, not proof that calibration or threshold transfer is unexplored.

[Source link recorded in the supplied reports](https://arxiv.org/abs/2603.06148)

## VL Uncertainty

Role: a close competitor to internal perturbation probes. The reports describe repeated image and text perturbations with uncertainty from variation in generated answers.

Status: full-text comparison reported in S10 §3 and v2 inspection in S08 §2. Substantial overlap with A; detection accuracy must not be relabeled AUROC.

[Source link recorded in the supplied reports](https://arxiv.org/abs/2411.11919)

# 11 The most decision relevant comparison papers

## Evidence Order Calibration

Role: targeted loss of question-critical evidence and selective reliability. It challenged the assumption that a learned evidence-order signal must outperform native confidence for choosing answers.

Status: only abstract-level access reported in S10; later full-text inspection reported in S08. The latest audit distinguishes question grouping from source-image grouping, and local masking from global resolution loss.

[Source link recorded in the supplied reports](https://arxiv.org/abs/2609.09184)

## Look Again Before You Abstain and BCEA

Role: acquiring additional visual evidence before withholding an answer, with a statistical calibration framework. It helped distinguish active acquisition from passive degraded input.

Status: unavailable primary full text in S10, later PDF inspection reported in S08. Exact checkpoint naming and the scope of any guarantee require care; acquisition is not B’s deployment setting.

[Source link recorded in the supplied reports](https://arxiv.org/abs/2606.16667)

## Bigger or Cheaper

Role: the decisive competing study for B. S08 reports comparisons of internal and verbalized uncertainty, scale and quantization, plus unchanged clean-threshold transfer under degradation.

Status: limited access in S10; described incorrectly as omitting transfer in S11; corrected by S08 and broad overlap corroborated in S09. A narrower independent-calibration extension remained unresolved.

[Source link recorded in the supplied reports](https://arxiv.org/abs/2607.24440)

## VL Calibration

Role: separating visual and reasoning confidence. It showed overlap between altered visual evidence and calibration, even though its full method involves post-training.

Status: full-text inspection reported in S10 and S08. A trained method can still supply relevant conceptual prior art for a frozen-model idea. It was not selected for reproduction.

[Source link recorded in the supplied reports](https://arxiv.org/abs/2604.09529)

## IntroConformal

Role: internal signals for factuality filtering and statistical control. It provided an adjacent alternative to visual probes and raised questions about judge-dependent labeling.

Status: full-text inspection reported in S10/S08. S08 treats it as a preprint with author-stated acceptance not independently verified, correcting S11’s stronger venue claim. Its guarantees are not automatically transferable to visual shift.

[Source link recorded in the supplied reports](https://arxiv.org/abs/2609.01375)

# 12 Adjacent reliability papers and evidence leads

These items broadened the comparison beyond the eight focal papers. Their roles below summarize the supplied reports; links are retained as discovery pointers. They are not a new recommended reading queue.

| **Paper or method** | **Why it appeared** | **Recorded depth or unresolved issue** |
| --- | --- | --- |
| [ConfLVLM or Towards Statistical Factuality Guarantee for LVLMs](https://aclanthology.org/2025.emnlp-main.576/) | Statistical control of factuality in generated responses. | S03 foundation; S10 reports inspection of the guarantee’s target loss. Not automatically conditional error among accepted answers. |
| [ReCoVERR](https://aclanthology.org/2024.findings-acl.767/) | Gather additional evidence before giving up. | S10 reports full-text examination; its discussed evaluation uses a GPT-based evaluator. |
| [CARA and CASE](https://arxiv.org/abs/2405.11145) | Insufficient visual context and abstention. | S10 reports inspected primary material. Close overlap with explicit answerability. |
| [TUBench and UVQA](https://arxiv.org/abs/2410.04107) | Out-of-frame and other unanswerable visual questions. | S10 identifies paper/release; exact usable subgroup size and overlap comparison remain open. |
| [Object-Level Verbalized Confidence Calibration via Semantic Perturbation](https://arxiv.org/abs/2504.14848) | Object-region changes connected to confidence learning. | S10 reports full-text comparison. Substantial conceptual overlap with A. |
| [Grounding-based uncertainty calibration](https://arxiv.org/abs/2505.03788) | Why self-consistency is not equivalent to correctness. | S10 discusses inspected primary material. Adjacent confidence family, not a selected baseline. |
| [Visual Contrastive Decoding or VCD](https://arxiv.org/abs/2311.16922) | Contrast original and distorted views to change generation. | S10 discusses method boundary: changing answers differs from filtering fixed answers. |
| [Seeing without Looking](https://arxiv.org/abs/2605.22903) | Visual dependence, interventions and benchmark shortcuts. | Discussed in S03/S10. Correct answers are not sufficient proof of image use. |
| [CLASH](https://arxiv.org/abs/2511.19199) | Cross-modal contradiction detection. | Named in S03 as an early conflict-setting reference; no complete personal reading record. |
| [C³PO](https://arxiv.org/abs/2608.05381) | Cross-modal composition and counterfactual evaluation. | Named in S03; historical lead, not a selected experiment. |
| [SIEVES](https://arxiv.org/abs/2604.25855) | Evidence-based learned selection in visual question answering. | S08 reports primary inspection; adds overlap pressure to generic selective VQA. |
| [Do VLMs See What Blind Users Show Them](https://openreview.net/pdf?id=MCEkYcej8d) | VizWiz distribution-shift and protocol audit. | S08 reports inaccessible primary endpoints. A separately mentioned file is not among these eleven attachments. Content and later resolution are not established here. |

# 13 Papers encountered in the five area branch

The inventory emphasizes named studies that shaped the screening, rather than counting every bibliography entry. Duplicate links to the same paper are not separate readings. All five areas are now parked. [S05–S09; U1]

| **Study or family** | **Role in the exploration** | **Evidence status in the record** |
| --- | --- | --- |
| [Lost in the Middle](https://arxiv.org/abs/2307.03172) | Text context-position foundation. | S05/S06 orientation; S06 explicitly discloses abstract/metadata-level reading. |
| V2PE | Visual position encoding and long-context capability. | S05 candidate justification; full experimental details were not inspected there. |
| [MMLongBench](https://arxiv.org/abs/2505.10610) | Closest benchmark for position, length and modality. | S05/S06 partial coverage; S09 reports primary check contradicting the broad claimed gap. |
| [MMLongCite](https://arxiv.org/abs/2510.13276) | Citation fidelity across evidence depth and context length. | Initially unresolved in S06; S09 reports primary inspection, including a small-model setting. |
| Position Bias in Multi-Image VLMs and SoFA | Image-order bias and attention correction. | Central in S07; S09 checks repository and finds no ready implementation in the inspected main branch. |
| [Logit–Attention Divergence or LAD](https://arxiv.org/abs/2605.11591) | Disagreement between internal attention and output choice. | S09 reports direct small-model and distractor overlap, overturning S07’s description. |
| MMNeedle | Retrieval from multi-image haystacks. | S07 literature matrix; useful task distinction, no reproduced run. |
| [Retrieval Quality at Context Limit](https://arxiv.org/abs/2511.05850) | Counterexample to universal lost-in-the-middle claims. | S06 reports abstract/metadata-only access; do not generalize to all models/tasks. |
| [Continual Learning for VLMs survey](https://arxiv.org/abs/2508.04227) | Taxonomy beyond forgetting. | S05/S06 screening; survey maturity does not prove that no feasible gap exists. |
| Continual Learning of LLMs survey and FOREVER | Continual-training stages and replay scheduling. | S05 condensed extraction; screening leads, not personal deep-reading evidence. |
| CoIN and CLiMB | Multimodal continual-learning benchmarks. | S07 uses them to discuss sequential tuning burden; no measured local feasibility. |
| [MemLens](https://arxiv.org/abs/2605.14906) | Multisession visual memory and loss of visual fidelity. | S07 discussion; S09 checks primary evidence and corrects judge and performance generalizations. |
| HiPlan or HIPLAN and Why Web Agents Fail | Milestones, planning and execution bottlenecks. | S06/S07 screening; detailed reported claims not independently authenticated here. |
| PlanGenLLMs and long-term-memory surveys | Conceptual maps for planning and memory. | S05 orientation and partial-access disclosure; not evidence of a selected thesis gap. |
| [VisualWebArena](https://github.com/web-arena-x/visualwebarena) | Genuinely visually grounded web tasks. | S09 official-source counterexample to the claim that planning is necessarily text-only. |

Additional named leads in S06: MemGPT, Mem0, A-MEM, MemoryBench, LongMemEval, LoCoMo, EvolMem, SMMBench, Mem-Gallery, Omni-SimpleMem, SSGM, MiRA, Plan-and-Act, SCOPE and HiAgent. CLIP-style adaptation leads included TDA, DOTA, ReTA, SubTTA and Bayesian TTA. These were surfaced during screening; this record does not establish detailed personal reading or reproduction of them.

# 14 Research assets and the unfinished decisions

A dataset, model or metric appearing in a report is a candidate resource, not proof that it has been downloaded, understood, licensed for the intended use, or successfully run. [S01 §§9–11; S08 §6; S09 §3]

| **Asset group** | **Items encountered** | **What the record supports** |
| --- | --- | --- |
| Core data lead | POPE and MS-COCO | Best-developed binary existence setting; custom image-grouped partitions discussed. No final dataset selection or local run documented. |
| Evidence and answerability | GQA; TUBench/UVQA; VizWiz lead | Different label needs: object relations, explicit unanswerability, naturally difficult user photos. They are not interchangeable. |
| Hallucination evaluation context | CHAIR, AMBER, HallusionBench, MMHal-Bench | Named benchmark/metric leads in S03/S10 and conversation. No evidence all were personally inspected or adopted. |
| Multi-image and context | MMLongBench, MMLongCite, MMNeedle, BLINK, Mantis-Eval, MuirBench, PQA, Visual Haystack | Assets considered during the now-parked five-area branch. |
| Planning environments | ALFWorld, WebShop, WebArena, VisualWebArena, Mind2Web, PlanBench, TravelPlanner, Blocksworld | Screening context, not an implemented thesis environment. |
| Small model candidates | Qwen2.5-VL-3B-Instruct; SmolVLM2-2.2B-Instruct | Plausible starting checkpoints in reports; no selected checkpoint, measured memory or demonstrated confidence extraction. |
| Other model families | Qwen2-VL, Qwen3-VL, LLaVA, InternVL, Molmo and Gemma families | Mostly models used by cited papers or considered as alternatives, not models you have demonstrably evaluated. |
| Possible software | Python, PyTorch, Transformers, datasets, PEFT/bitsandbytes, VLMEvalKit | Proposed tooling. No final thesis repository or environment is evidenced by the attachments. |

## What the metric names were trying to answer

Accuracy asks whether the answer is right. ECE and Brier concern probability quality. AUROC concerns ordering correct and incorrect answers by a score. Risk–coverage curves describe error as the system returns more or fewer answers; AURC summarizes that trade-off. A fixed threshold is one operating point, not a new curve. [S04 §4; S08 §4; S09 §7]

These were protocol concepts under discussion, not reported performance. In particular, the precise memory and latency figures in the targeted report were not your measurements. Your actual Colab capacity for any proposed full configuration remains undocumented.

# 15 What is settled and what remains unresolved

| **Decision** | **Current record** | **Reason** |
| --- | --- | --- |
| Parent field | Keep VLM/MLLM as the established identity. | No later instruction selected a replacement field. [S01; U1] |
| Subfield | Keep trustworthy generative MLLMs as the established working focus. | Repeated in both handovers; exact topic remains open. [S03–S04] |
| Five-area expansion | Park all five. | Your latest explicit decision supersedes the cross-report ranking. [U1] |
| Internal-probe idea | Historical parked candidate. | Incremental value and score semantics were unresolved. [S08, S10] |
| Passive degradation | Unresolved candidate, not a final topic. | Broad gap claim contradicted; narrower contribution unestablished. [S08–S09] |
| Explicit answerability | Historical unresolved branch. | Not the same as object-scale analysis; no later completed branch-specific selection is supplied. [S10] |
| Object-scale thesis identity | Parked in latest topic audit. | Geometry cannot substitute for evidence-sufficiency labels. [S08] |
| Topic, contribution and method | Not frozen. | No candidate has a fully settled scientific contribution in the supplied record. |
| Experimental achievements | Do not claim any yet from these files. | No personal baseline replication, result table or runtime log is documented. |

## Your place in the full thesis journey

A useful six-stage mental structure is: understand the field; define one research question; specify the data and evaluation; implement and reproduce baselines; run the study and analyze evidence; write and package the thesis. This is an explanatory map, not a newly imposed schedule.

You have completed the major field-selection decisions and repeatedly worked on question definition and evaluation reasoning. You have not documented completion of question selection, a final data protocol, baseline reproduction, experimental analysis or a results-based thesis. Work on later-stage planning does not mean those stages are complete.

## The unresolved questions are now identifiable

- Which specific failure do you want to understand well enough to explain in your own words?
- What does the closest existing study already establish, and what would your study add?
- What label would distinguish success from failure without pretending to measure something else?
- What conclusion would remain useful if the expected effect or improvement does not occur?

No new candidate is selected by this report. The immediate achievement is a consolidated record that can support understanding and handover without reopening the parked branches.

# 16 Source record and evidence boundaries

This report is grounded in the eleven supplied documents and visible project context. It is not a fresh systematic literature review. Claims about what an earlier audit verified remain attributed to that audit. Source material was examined for scope, decisions, candidate histories, paper discussions and relevant supporting sections; bibliography size is not treated as evidence of reading depth.

| **ID** | **Supplied document** | **Role and limitation** |
| --- | --- | --- |
| S01 | Canonical Thesis Field Specification.md | Scope authority; effective 22 August 2026. Defines field, three lanes and topic-selection standards. |
| S02 | 02-Canonical/_Rejected/_and/_Parked/_Thesis/_Fields/_Report.md | Boundary authority; cutoff 22 August. Eight parked groups expanded into thirteen dossiers, not thirteen new recent decisions. |
| S03 | AI/_Conversation/_Handover/_Report.md | Early handover dated 3 September. Documents reliability subfield and absence of implementation. |
| S04 | AI/_Conversation/_Handover/_Report/_2026-09-14.md | Later handover; candidate history and corrections. Its pending checks are partly superseded by S08. |
| S05 | Five Area Perflexity Research Report.md | Five-area screening; optimistic long-context recommendation later challenged. |
| S06 | Five Area Claude Research Report.md | Explicitly screening-depth coverage; cautious long-context lead and parked alternatives. |
| S07 | Targeted Feasibility & Evidence Assessment for Und.md | Detailed candidate cards; contains novelty, traceability and unsupported resource claims corrected by S09. |
| S08 | MLLM/_Thesis/_Topic/_Selection/_Audit/_2026-09-14.md | Decision-critical reliability audit; topic remains open, broad threshold-transfer gap contradicted. |
| S09 | # Cross-Report Evidence Audit and Ranked Feasibility Decision for Five Candidate Research Areas.md | Decision-critical comparison of S05–S07; later user parking overrides its long-context priority. |
| S10 | Trustworthy-MLLM-Evidence-Based-Narrowing-Report (Astra).md | 13 September narrowing; three distinct predictive targets and explicit recent-source access limitations. |
| S11 | MLLM Threshold Transfer vs Ranking Failure Research(1).md | Gemini-origin diagnostic report as identified in handover; useful leads, central absence claim later contradicted. |

[U1] Latest visible project instruction: park continual learning, different memory systems, long context windows, long-term planning and hierarchical planning. [U2] Current request: consolidate progress and clarify the mental map. [C] Other visible project conversation summaries, used only for historical discussion context, not as proof of paper reading or experiments.

# 17 Important limits of this progress record

## The exact amount of personal learning is unknown

The attached reports show what was proposed, discussed and audited. They cannot establish how many hours you worked, how many original papers you read end to end, which concepts you can explain unaided, or what you ran outside the supplied record. “Not documented” does not mean “definitely never happened.”

## Historical and current evidence are different

This report preserves the recorded chain of reasoning. It does not revalidate every recent preprint, conference claim, model license, repository or paper result against today’s external sources. Titles, identifiers and descriptions in the paper inventory are traceable leads from the attached documents. Any future technical claim should return to the relevant primary source rather than cite this progress report as scientific proof.

## The supplied files do not cover every mentioned artifact

Earlier landscape documents, the Gemini pre-pilot audit referenced by Astra, a separate VizWiz audit file mentioned in project conversation, and any completed cross-domain research result are not among the eleven supplied files. This report does not invent their contents or claim their requested work was completed. Astra’s discussion of a recovered equation is reported through S10.

## Older status wording needed reconciliation

S03 calls the subfield “ready to freeze” in one place and “frozen” elsewhere. S04 consistently treats the reliability lane as fixed. This report therefore calls the subfield an established working focus, while reserving “exact thesis selected” for a decision that has not been documented.

S02 records eight parked parent-field groups and thirteen expanded dossiers, while listing several other fields as unassessed. Later user preferences narrow what is acceptable further. Those unassessed labels are not invitations to reopen discovery, and this report does not relabel every unassessed area as scientifically rejected.

## Publication ambition is not the same as thesis completion

The canonical specification explicitly distinguishes a defensible undergraduate thesis from a publishable contribution. The audits often tested ambitious novelty claims. Their rejection of a claim does not by itself prove that the entire field is unsuitable, or that a university would reject a well-designed replication and extension. No supervisor or departmental decision on that point is supplied. [S01 §§7,12]

## What can be stated with confidence

The field choice, primary reliability focus, existence of multiple candidate formulations, important reversals in the audits, and your latest parking instruction are documented. A final topic, completed personal literature mastery and experimental success are not established. This separation is the basis of the handover on the next page.

# 18 Handover for another researcher or assistant

The following summary is written in the first person so it can be shared directly. It describes the current record, without claiming unrecorded work.

## My project and constraints

I am Mohammad Zahed Hossen, a final-year CSE student in Bangladesh working toward an undergraduate thesis. My parent field is Multimodal / Vision-Language Learning and Systems. My established primary focus is trustworthy generative MLLMs, especially evidence-grounded uncertainty and selective prediction when visual evidence is weak, missing, conflicting or degraded. My exact thesis question and title are not selected.

I prefer public datasets, open-weight models, reproducible evaluation and a bounded AI/CSE contribution. My normal GPU environment is Colab Pro; my local desktop has 8 GB RAM and no usable training GPU. Occasional stronger GPU access should not justify a large training project. My planning horizon has been approximately three to four months, but this record does not establish a confirmed submission deadline.

## What I have done

I have created and reviewed a canonical field specification, a parked-field record, handover reports, candidate-narrowing reports and two decision-focused audits. I explored internal visual probes, passive degradation and acceptance-policy transfer, explicit answerability, and object-scale analysis. I also screened continual learning, memory systems, long context, long-horizon planning and hierarchical planning, then asked to park all five.

## What changed after the audits

The earlier claim that clean-threshold transfer alongside confidence ranking was missing from prior work did not survive the later audit. Bigger or Cheaper? was identified as direct overlap. A narrower independent-calibration diagnostic extension remains unresolved. Perturbation uncertainty and multi-image position effects also have substantial prior art. Do not present these broad mechanisms as newly discovered gaps.

## What has not been established

I do not yet have a frozen contribution, final dataset/model/method, or documented experimental findings in this record. The reports contain many paper references, but they do not prove that I personally understand or have fully read every paper. My immediate difficulty is seeing how the accumulated work fits together.

## How to continue from here

Use this report to orient me before adding more research. Keep established decisions separate from historical proposals. Explain the research question and the role of each important paper in plain English. Do not automatically reactivate long context or another parked branch. Do not choose an exact topic merely to make the process feel finished, and do not mistake an earlier AI-generated plan for completed implementation.

**Current status in one sentence: I have selected the VLM/MLLM field and a reliability-centered subfield, built a substantial but unevenly understood literature and decision record, and remain at unresolved exact-topic selection.**
