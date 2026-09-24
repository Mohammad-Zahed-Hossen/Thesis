## D:/Thesis/Canonical Thesis Field Specification.docx
**THESIS RESEARCH GROUND**

Canonical Thesis Field Specification

Multimodal / Vision-Language Learning and Systems

*One frozen parent field. Three ranked research fields. Topic discovery remains active.*

|  |  |
| --- | --- |
| **Version** | 1.0 |
| **Status** | Field Frozen | Topic Not Frozen |
| **Effective date** | 22 August 2026 |
| **Use** | Private canonical reference for thesis research and publication planning |

*This document governs field and topic decisions. It is not a university form, schedule, or promise of publication.*

# Executive Field Decision

|  |
| --- |
| **CANONICAL DECISION** The frozen parent field is Multimodal / Vision-Language Learning and Systems. The ranked research fields are: (1) Trustworthy and Reliable VLMs, (2) VLM Generalization, Adaptation and Distribution Shift, and (3) Efficient and Scalable VLMs. A thesis topic has not been selected. |

* **Primary research field:** Trustworthy and Reliable VLMs.
* **Secondary research field:** VLM Generalization, Adaptation and Distribution Shift.
* **Conditional research field:** Efficient and Scalable VLMs.
* **Publication strategy:** design the work to publication standards from the beginning, complete a defensible thesis first, then submit or extend only when the evidence is mature.
* **Operating rule:** no unrelated field may be reopened without a written change request and evidence that the frozen field has become infeasible.

## How to Use This Document

Use this specification before starting a literature review, creating a candidate topic, selecting a dataset, choosing a model, or accepting a claimed research gap. Every decision-changing research session must end with a verdict, evidence, limitation, next action, and decision-log entry.

* Sections 1–4 define the field, ranked research directions, and boundaries.
* Sections 5–8 govern topic discovery, feasibility, contribution quality, and experiments.
* Sections 9–12 govern compute, data, reproducibility, publication, and workflow.
* Sections 13–15 provide templates, checklists, and change control.

## Document Authority and Revision Rules

This is the single source of truth for personal thesis research. ChatGPT, Claude, Perplexity, Kimi, notebooks, and temporary notes are workbenches. A suggestion from any platform is provisional until it is checked against this document and recorded in the Decision Log.

* Field changes require a major version and evidence that the current parent field cannot produce a feasible topic.
* Research-lane ranking changes require a minor version and a written evidence update.
* A topic is not frozen until it passes the Topic Feasibility Gate and the Topic Freeze Record is completed.
* Dates and university administration are intentionally excluded because this is a private research specification.

# 1. Researcher Profile and Operating Constraints

The specification is calibrated for a final-year undergraduate CSE researcher in Bangladesh whose primary career direction is AI/ML engineering and research. The research plan assumes substantial self-direction and does not count on continuous supervisor involvement.

| **Dimension** | **Canonical position** |
| --- | --- |
| Academic foundation | Algorithms, Pattern Recognition, Artificial Intelligence, Computer Networks, Object-Oriented Programming, and Operating Systems. |
| Technical foundation | Classical machine learning, deep learning, CNNs, transformers and LLM basics, Python, scikit-learn, PyTorch/TensorFlow familiarity, and web/API development. |
| Career objective | Build credible AI/ML research ability and end-to-end engineering evidence for employment, while preserving a path to funded graduate study. |
| Research team | Three members, with the principal researcher expected to lead most research design, implementation, evaluation, and writing. |
| Supervision assumption | Treat the thesis as largely self-directed. External feedback is useful but not a feasibility dependency. |
| Local compute | Ryzen 5 5600G, 8 GB RAM, integrated graphics. Local work is for coding, small preprocessing, documentation, and lightweight tests. |
| GPU compute | Google Colab Pro is the normal GPU environment. Limited temporary access to stronger GPUs may be used only after a Colab-feasible pilot succeeds. |
| Financial boundary | No dependence on expensive model APIs, private datasets, custom hardware, large cloud bills, or paid annotation. |
| Publication objective | Publication-aware design from day one; completion of a strong thesis takes priority over forcing an early submission. |

## 1.1 Non-negotiable Research Properties

* The core contribution must remain AI/CSE-heavy and understandable without unavailable domain experts.
* Data and model weights must be publicly accessible or obtainable under clear academic-use terms.
* A strong baseline must be reproducible before a new method is proposed.
* The main claim must be tested by direct metrics, ablations, and error analysis.
* The minimum experiment must fit Colab Pro and remain repeatable across seeds or controlled runs.
* The contribution must be more than applying a known model to a new dataset.

|  |
| --- |
| **HARD TRUTH** A fashionable field does not create a publishable thesis. Publication depends on a defensible question, credible evidence, controlled experiments, and honest limitations. Venue acceptance is never treated as guaranteed. |

# 2. Frozen Parent Field

## 2.1 Canonical Definition

Multimodal / Vision-Language Learning and Systems studies models and evaluation methods that connect visual information with natural language for perception, grounding, retrieval, reasoning, generation, and decision support. In this specification, the field includes model behavior, evaluation, adaptation, and deployment efficiency. It excludes training frontier foundation models from scratch.

## 2.2 Evidence for the Field Lock

The field lock is based on fit and continuity, not on the ordering of an AI-generated topic list. The official CVPR 2025 and CVPR 2026 calls both include multimodal learning, vision-language reasoning, datasets and evaluation, efficient and scalable vision, and transfer or continual learning [1, 2]. CVPR 2026 also scheduled dedicated oral sessions for multimodal vision and efficient reasoning, providing additional evidence of active research attention [3].

| **Decision factor** | **Assessment** | **Consequence** |
| --- | --- | --- |
| Background fit | Strong | Builds directly on existing ML, deep learning, transformer, Python, and AI engineering preparation. |
| Research continuity | Strong | The parent field and all three research lanes appear across 2025 and 2026 primary venue materials. |
| Supervisor dependence | Manageable | The field can be pursued through public papers, repositories, models, and benchmarks without specialist hardware or clinical access. |
| Compute fit | Conditional but workable | Evaluation, PEFT, quantization, pruning, and small-model studies are feasible; full model pretraining is not. |
| Career transfer | Strong | Skills transfer to multimodal evaluation, model serving, data pipelines, reliability testing, and deployment. |
| Publication opportunity | Real but competitive | Strong venues publish work in all three lanes, but incremental comparisons are insufficient. |

## 2.3 What Is Frozen and What Remains Open

| **Frozen** | **Open for evidence-based selection** |
| --- | --- |
| Parent field: Multimodal / Vision-Language Learning and Systems | Exact thesis title and research question |
| Three ranked research fields | Dataset, model family, benchmark, language, and application setting |
| Public-data and Colab-first constraints | Whether the contribution is a method, evaluation, system, or empirical study |
| Publication-aware experimental standards | Final venue and submission timing |

## 2.4 Why Choose Multimodal / Vision-Language Over Other Fields

### Direct Answer

You should choose **Multimodal / Vision-Language Learning and Systems** because it gives you the strongest combination of:
* Alignment with your existing Transformer, LLM, CV, and Python knowledge;
* Multiple testable research problems;
* Public benchmarks and open implementations;
* Feasible experiments using small pretrained VLMs on Colab Pro;
* Relevance to both AI research and end-to-end AI engineering;
* The ability to incorporate efficiency, XAI, adaptation, and other learning methods without changing fields.

*This does not mean VLM is scientifically superior to federated learning, medical imaging, diffusion, or XAI. It means VLM is the most strategically useful parent field for your present thesis.*

### Conceptual Correction: Field vs. Mechanism

The most important conceptual correction is this:

| Candidate | What it actually is |
| --- | --- |
| **VLM / Multimodal LLM** | A model and systems field |
| **Federated learning** | A distributed learning setting |
| **Medical image analysis** | An application domain |
| **Efficient models** | A research objective |
| **Learning paradigms** | A broad collection of training strategies |
| **XAI** | A method and evaluation field |
| **Diffusion models** | A generative model family |
| **AI image generator** | Usually a product/application, not automatically a research field |

These are not equivalent alternatives. **VLM is the thesis identity.** Efficiency, XAI, adaptation, or a learning paradigm can become the contribution inside it.

### Why VLM Fits You Unusually Well

#### 1. It compounds your existing knowledge
You already understand:
* CNNs and computer vision
* Transformers
* LLM fundamentals
* Python and deep-learning workflows
* API and system development

A VLM combines a vision encoder, language model, multimodal connector or projector, and generation/evaluation pipeline. LLaVA is a clear representative architecture: it connects a pretrained visual encoder with an LLM and performs visual instruction tuning. Its original project released models, code, data, and evaluation material publicly. [Liu et al., NeurIPS 2023](https://papers.neurips.cc/paper_files/paper/2023/hash/6dcf277ea32ce3288914faf369fe6de0-Abstract-Conference.html)

Therefore, you are extending your current knowledge rather than restarting in distributed systems, clinical imaging, or generative-model training.

#### 2. It has several measurable failure modes
You do not need to invent a new foundation model. You can study:
* visual hallucination;
* calibration and uncertainty;
* robustness to corruptions;
* language or cultural distribution shift;
* prompt sensitivity;
* missing or misleading visual evidence;
* cross-model generalization;
* efficiency and accuracy trade-offs;
* parameter-efficient adaptation.

For example, POPE provides a reproducible protocol for testing object hallucination in VLMs. The original study found systematic hallucination across representative models and released its code and data. [Li et al., 2023](https://arxiv.org/abs/2305.10355)

MMMU contains 11,500 multimodal questions across 30 subjects and heterogeneous visual formats, showing that multimodal reasoning can be evaluated beyond simple captioning. [Yue et al., CVPR 2024](https://doi.org/10.1109/CVPR52733.2024.00913)

That gives you a clearer path from:
> research question → controlled intervention → measurable result → error analysis

#### 3. Small open models make bounded research feasible
VLM research is no longer restricted to training massive models. Hugging Face’s open SmolVLM family includes 2B, 500M, and 256M variants. Its reported 2B inference requirement is about 5 GB of GPU memory under its tested configuration, and the checkpoints, datasets, recipes, and fine-tuning scripts are public. [SmolVLM technical release](https://huggingface.co/blog/smolvlm), [smaller 256M/500M release](https://huggingface.co/blog/smolervlm)

This does not mean every VLM experiment will fit Colab. Full pretraining and large-scale multi-model evaluation remain unrealistic. But the following are plausible:
* inference-based evaluation;
* small-model comparison;
* frozen-backbone interventions;
* lightweight decoding modifications;
* calibration;
* controlled data perturbations;
* LoRA or QLoRA-style adaptation;
* limited ablations on carefully selected benchmarks.

QLoRA demonstrated that frozen quantized models can be adapted through low-rank parameters with much lower memory than full fine-tuning. The exact budget still needs a pilot for the selected VLM. [Dettmers et al., 2023](https://arxiv.org/abs/2305.14314)

#### 4. The ecosystem reduces engineering waste
The official VLMEvalKit repository currently integrates hundreds of multimodal models and dozens of benchmarks, handling parts of dataset preparation, inference, and metric calculation. [OpenCompass VLMEvalKit](https://github.com/open-compass/VLMEvalKit)

This matters because your thesis should not spend months rebuilding evaluation infrastructure. However, the toolkit does not create a contribution. You still need a focused claim, controlled baselines, and your own analysis.

#### 5. It supports your research and engineering goals simultaneously
A rigorous VLM thesis can develop:
* multimodal data processing;
* model inference and adaptation;
* evaluation-pipeline engineering;
* memory and latency measurement;
* robustness testing;
* experiment tracking;
* model serving;
* failure analysis;
* reproducible research design.

That is a stronger match to your AI/ML engineering and AI-research goals than a thesis that becomes mainly clinical preprocessing, federated simulation, explanation visualization, or image-generation UI work.

### Comparison Against Alternatives

*Scores are subjective decision aids, not mathematical facts. Supervisor availability is treated as neutral. Your limited medical-domain knowledge remains a constraint.*

| Direction | Fit as thesis identity | Main advantage | Main problem for you | Best decision |
| --- | --- | --- | --- | --- |
| **VLM / Multimodal LLM** | 4.5/5 | Broad research surface with open models and measurable failures | Crowded field; careless work becomes benchmark testing | **Choose as parent field** |
| **Efficient models** | 4.0/5 | Feasible, measurable, industry-relevant | “Make model smaller” is too broad and often incremental | **Use inside efficient VLM lane** |
| **Medical image analysis** | 3.5/5 | Mature datasets, baselines, social value | Clinical validity and novelty are harder than model accuracy | **Optional VLM application context** |
| **XAI** | 3.4/5 | Valuable for trust and debugging | Explanation correctness is difficult to validate | **Use inside trustworthy VLM lane** |
| **Federated learning** | 3.1/5 | Important privacy and distributed-learning problems | Simulated clients may not support real-world claims | **Preserve for later** |
| **Learning paradigms** | 3.0/5 | Scientifically fundamental | Too broad to serve as a topic or field decision | **Select one only when a VLM problem requires it** |
| **Diffusion models** | 2.7/5 | Strong generative-model research value | Training, evaluation, and novelty costs are high | **Do not use as parent field** |
| **AI image generator** | 1.8/5 | Attractive demo and product potential | Usually application engineering, not research | **Reject as thesis identity** |

#### Federated learning
Federated learning is real and important research. FedAvg established decentralized training through repeated local updates and model aggregation, with communication and non-IID data as central problems. [McMahan et al., AISTATS 2017](https://proceedings.mlr.press/v54/mcmahan17a.html)

The problem is not merely computation. It is experimental realism. With no real organizations or devices, you would usually partition one public dataset into simulated clients. You then need to justify:
* why the partition represents real clients;
* client availability and dropout assumptions;
* communication costs;
* heterogeneity;
* privacy or threat model;
* whether the findings generalize beyond the simulation.

A weak FL thesis becomes:
> Run FedAvg, FedProx, and another aggregator on artificially partitioned MNIST/CIFAR data.

That is reproducible, but often scientifically shallow.

**Verdict:** FL is valuable, but VLM provides a cleaner route to directly observable model failures. Preserve FL for a later systems-oriented project with realistic decentralized data or deployment conditions.

#### Medical image analysis
Medical imaging has strong public datasets. CheXpert, for example, contains 224,316 chest radiographs from 65,240 patients with associated reports. [Stanford AIMI](https://aimi.stanford.edu/datasets/chexpert-chest-x-rays)

Therefore, data access is not the automatic blocker. The deeper problem is that medical-image research requires defensible decisions about:
* patient-level splitting;
* clinical target definition;
* uncertain and weak labels;
* acquisition and hospital shifts;
* sensitivity, specificity, calibration, and confidence intervals;
* reference-standard validity;
* clinical meaning of false positives and false negatives.

The CLAIM guideline explicitly expects intended clinical use, ground-truth definitions, annotator qualifications, patient-level separation, robustness analysis, uncertainty reporting, and comparison with relevant clinical standards. [Mongan, Moy and Kahn, 2020](https://doi.org/10.1148/ryai.2020200029)

Without sufficient medical knowledge, you can train a model correctly while framing the clinical problem incorrectly.

**Verdict:** Medical imaging remains viable for a tightly technical CSE thesis, especially robustness, domain adaptation, segmentation, calibration, or efficiency. But it is not a stronger parent-field choice than VLM for you. Medical image-text data could later become a VLM application context, provided you avoid unsupported clinical claims.

#### Efficient models
This is the strongest apparent alternative, but it is not really an alternative to VLM. Efficiency research includes:
* quantization;
* pruning;
* distillation;
* low-rank adaptation;
* efficient attention;
* token reduction;
* early exiting;
* inference serving;
* memory and latency optimization.

These methods require a target model and task. You can apply them to CNNs, LLMs, diffusion models, or VLMs. A standalone “efficient AI” thesis risks producing predictable results:
> Quantize model → memory decreases → accuracy decreases slightly.

A stronger question would be:
> Can visual-token reduction lower VLM latency while preserving calibration and robustness under distribution shift?

That gives efficiency a concrete scientific target.

**Verdict:** Do not abandon VLM for efficient models. Make efficiency the contribution inside the Efficient and Scalable VLMs lane.

#### Learning paradigms
“Learning paradigms” includes supervised, self-supervised, contrastive, few-shot, continual, active, meta-, transfer, and reinforcement learning. It is too broad to guide a thesis. You cannot meaningfully choose “learning paradigms” until you know:
* what task is being learned;
* what supervision is available;
* what generalization claim is being tested;
* what baseline establishes improvement.

**Verdict:** Treat a learning paradigm as part of the methodology. For example, contrastive adaptation or self-training might support VLM distribution-shift research. It should not replace the parent field.

#### Explainable AI
XAI is valuable, but evaluation is its central weakness. A visually attractive heat map is not evidence that an explanation is faithful.

Adebayo et al. showed that some saliency methods can remain similar even after model parameters or labels are randomized. This means visual plausibility alone is unreliable. [Adebayo et al., NeurIPS 2018](https://proceedings.neurips.cc/paper/2018/hash/294a8ed24b1ad22ec2e7efea049b8737-Abstract.html)

Standalone XAI therefore requires a defensible definition of explanation quality:
* faithfulness;
* causal influence;
* stability;
* comprehensibility;
* task usefulness;
* human evaluation.

This can become more difficult than training the underlying model. Inside VLM research, XAI becomes more grounded:
> Does cross-modal attribution predict which VLM responses will hallucinate under image corruption?

Here, the explanation supports a named reliability claim rather than being the thesis identity.

**Verdict:** Use XAI only as a validated method inside Trustworthy and Reliable VLMs.

#### Diffusion models
Diffusion research is scientifically rich, but original model training remains expensive. The latent diffusion paper notes that earlier powerful diffusion systems could consume hundreds of GPU days; latent-space training reduced this burden but did not make serious foundation-model training cheap. [Rombach et al., CVPR 2022](https://doi.org/10.1109/CVPR52688.2022.01042)

Your realistic options would be:
* fine-tuning a pretrained diffusion model;
* modifying conditioning;
* efficient adapters;
* evaluating bias, faithfulness, or prompt adherence;
* synthetic-data generation.

Those can be research, but the risks are:
* expensive repeated sampling;
* difficult human or learned-metric evaluation;
* dependence on pretrained model behavior;
* crowded novelty landscape;
* large storage requirements;
* visually impressive results hiding weak scientific contribution.

**Verdict:** Do not choose diffusion training as the parent field. Use pretrained generation only if it directly supports a controlled VLM experiment.

#### AI image generator
Building an AI image generator normally means wrapping an existing diffusion checkpoint with prompts, controls, and a user interface. That can be a good engineering project. It is usually a weak thesis because the main intelligence comes from the pretrained model.

A thesis would require a testable contribution such as:
* measurable compositional faithfulness;
* bias mitigation;
* controllability;
* efficient generation;
* watermark robustness;
* evaluation under distribution shift.

At that point, the research field is no longer “AI image generator.” It becomes diffusion evaluation, trustworthy generative AI, or efficient generative modelling.

**Verdict:** Reject the generic generator as a thesis identity.

### Strategic Fit of the Three VLM Lanes

#### 1. Trustworthy and Reliable VLMs
This is your strongest lane because:
* it often permits inference-only or lightweight interventions;
* hallucination, calibration, robustness, and grounding are measurable;
* it does not require training a foundation model;
* it naturally incorporates XAI;
* failure analysis produces more scientific value than building another application.

#### 2. VLM Generalization, Adaptation and Distribution Shift
This is the strongest alternative when you find a credible dataset shift:
* clean versus corrupted images;
* English versus Bengali prompts;
* photographs versus diagrams;
* familiar versus rare objects;
* one benchmark/domain versus another;
* zero-shot versus lightweight adaptation.

The main difficulty is proving that the shift is meaningful rather than artificially convenient.

#### 3. Efficient and Scalable VLMs
This keeps the best parts of efficient-model research:
* quantization;
* adapters;
* visual-token pruning;
* latency;
* memory;
* throughput;
* accuracy-efficiency trade-offs.

But it gives efficiency a concrete multimodal target and prevents a generic compression thesis.

### Honest Warning & Boundary Rules

Choosing VLM is only rational if you do not attempt to:
* pretrain a VLM;
* fine-tune many 7B–70B models;
* evaluate dozens of huge benchmarks;
* rely primarily on proprietary judge models;
* create another visual-chat application;
* claim novelty from combining several frameworks;
* use “hallucination detection” without defining exact failure types;
* report only aggregate benchmark accuracy.

A bad VLM thesis is just as weak as a generic RAG or image-generator project. Your thesis must reduce to something like:
> For a bounded VLM failure under a verified dataset condition, does intervention X improve metric Y over strong baselines, within a tested compute budget, without harming Z?

Until you have that, you have selected only the field, not the thesis topic.

### Final Summary and Actionable Recommendations

* **Keep Multimodal / Vision-Language Learning and Systems as the parent field.**
* **Prioritize trustworthiness/reliability.**
* **Use distribution shift/adaptation as the second search area.**
* **Treat efficiency as a conditional contribution.**
* **Absorb XAI and suitable learning paradigms as supporting methods.**
* **Consider medical imaging only as a bounded multimodal application context.**
* **Keep FL and diffusion parked.**
* **Reject a generic AI image generator as thesis research.**

# 3. Ranked Top Three Research Fields

These are the only active fields for topic discovery. They are ranked by the combination of research value, execution feasibility, publication potential, compute cost, and compatibility with the researcher’s existing preparation.

## 3.1 Rank 1: Trustworthy and Reliable VLMs

This field studies whether a VLM is grounded in visual evidence, knows when it is uncertain, remains reliable under difficult inputs, and can be evaluated without misleading metrics. It is the primary field because it supports rigorous evaluation-centered work without requiring foundation-model pretraining.

### Suitable problem families

* Object, attribute, relation, action, temporal, or textual hallucination.
* Visual grounding and evidence attribution failures.
* Calibration, uncertainty estimation, selective prediction, and abstention.
* Robustness to misleading instructions, irrelevant context, image degradation, or modality conflict.
* Reliability of VLM-as-a-judge and automated evaluation pipelines.
* Multilingual or low-resource evaluation when language coverage is a genuine confound rather than a cosmetic application.

### Evidence of active research

CVPR 2025 included PhD, a large-scale visual hallucination evaluation dataset, Critic-V for catching VLM reasoning errors, and ClearSight for hallucination mitigation [4–6]. CVPR 2026 continued with multimodal decoding, visual-expert refinement, and structural probing of hallucination behavior [7–9]. These papers show that evaluation, mitigation, and mechanistic analysis are all active, but they also raise the novelty bar.

### Minimum acceptable contribution

* A new and justified failure condition or evaluation protocol, not only another model leaderboard.
* A reproducible measurement study with cross-model or cross-dataset evidence and meaningful error taxonomy.
* A lightweight mitigation with ablation showing why it works and what capability it harms.
* A calibration or abstention method evaluated for both reliability and retained task utility.

### Reject or narrow when

* The proposed work only runs several VLMs on an existing benchmark.
* The evaluation depends entirely on one proprietary LLM judge.
* The claimed hallucination metric cannot distinguish perception failure from language-generation style.
* The model cannot complete the benign task reliably enough for safety or robustness metrics to be interpretable.

## 3.2 Rank 2: VLM Generalization, Adaptation and Distribution Shift

This field studies performance when deployment data differ from training or benchmark data. It is less dependent on model hype because temporal, cross-source, linguistic, visual-style, corruption, and domain shifts remain fundamental deployment problems.

### Suitable problem families

* Cross-dataset and cross-source VLM evaluation.
* Domain generalization with few labels or missing modalities.
* Test-time adaptation and continual test-time adaptation.
* Robustness to visual corruptions, style changes, language shifts, or retrieval degradation.
* Generalization of AI-generated image detection across unseen generators, when treated as a visual robustness problem rather than a cybersecurity field.

### Evidence of active research

CVPR 2025 included test-time adaptation methods such as Free on the Fly and VLM generalization work such as SCAP [10, 11]. CVPR 2026 continued with multimodal domain generalization using few labels and robust vision-based retrieval-augmented generation under visual degradation [12, 13].

### Minimum acceptable contribution

* A deployment-relevant shift with a justified temporal, cross-source, or domain split.
* A strong no-adaptation baseline and comparison with simple recalibration, retraining, or prompting.
* Evidence across multiple shift conditions, not one corruption severity or one target domain.
* A method or analysis that identifies when adaptation helps, fails, or causes catastrophic side effects.

### Reject or narrow when

* The work is another small variation on CIFAR-C without a convincing VLM or deployment setting.
* Random splitting destroys the claimed temporal or domain-shift evaluation.
* The proposed method is compared only with a weak source-only baseline.
* The performance gain is within normal run-to-run noise and has no error analysis.

## 3.3 Rank 3: Efficient and Scalable VLMs

This field studies how to reduce inference cost, memory, latency, or visual-token processing while preserving useful capability. It is conditionally shortlisted because its engineering value is high, but publication becomes difficult when the contribution is only a quantization or pruning comparison.

### Suitable problem families

* Visual-token pruning or merging with task-aware selection.
* Adaptive compute, early exit, or dynamic resolution.
* Quantization or compression effects on hallucination, grounding, calibration, and reasoning.
* Small/open VLM capability retention under memory and latency constraints.
* Efficient document or long-context multimodal inference.
* Hardware-aware trade-offs using actual latency, peak memory, throughput, and energy where measurement is available.

### Evidence of active research

CVPR 2025 accepted original work on post-training quantization, data-free quantization, and visual-token pruning, including APHQ-ViT, Quantization without Tears, and DivPrune [14–16]. CVPR 2026 continued with collaborative multimode pruning for VLMs [17]. These examples disprove the claim that efficient AI cannot reach strong venues; they also demonstrate that strong publications introduce new methods or formulations and validate them broadly.

### Minimum acceptable contribution

* A new selection criterion, optimization objective, allocation mechanism, or reliability-aware compression strategy.
* A careful efficiency-reliability study that reveals a previously unmeasured failure and changes practical model-selection decisions.
* Real systems evidence beyond parameter compression, including latency, memory, throughput, or energy when the claim is deployment efficiency.
* Comparison with a size-matched or compute-matched random baseline when placement or allocation quality is claimed.

### Reject or narrow when

* The contribution is only applying INT8, LoRA, or pruning to a new dataset.
* Only accuracy and compression ratio are reported for a systems claim.
* The evaluation uses one architecture, one dataset, or one seed.
* The experiment budget requires repeated full-model training beyond the available compute.

| **Field** | **Default verdict** | **Primary contribution path** | **Main risk** |
| --- | --- | --- | --- |
| Trustworthy and Reliable VLMs | Explore first | Evaluation, analysis, or lightweight mitigation | Crowded benchmark-only work |
| Generalization and Distribution Shift | Explore second | Robust protocol, adaptation, or failure analysis | Artificial or weak shift design |
| Efficient and Scalable VLMs | Explore conditionally | New method or reliability-aware systems evidence | Incremental compression comparison |

# 4. Preferred Intersections and Scope Boundaries

## 4.1 Preferred Intersections

The strongest eventual topic may sit at the intersection of the ranked fields. However, the thesis should have one primary claim and at most one secondary lens.

| **Priority** | **Intersection** | **Why it is promising** | **Caution** |
| --- | --- | --- | --- |
| A | Reliability × Distribution Shift | Tests whether VLM trustworthiness survives realistic deployment changes. Supports clear protocols and strong failure analysis. | Do not combine too many shift types or trustworthiness metrics. |
| B | Reliability × Efficiency | Studies whether pruning, quantization, or small-model deployment changes grounding, hallucination, calibration, or reasoning. | Requires both task utility and real efficiency measurements. |
| C | Generalization × Efficiency | Studies whether an efficient model or inference strategy remains robust outside its benchmark distribution. | Can become experiment-heavy; use one efficiency intervention. |

|  |
| --- |
| **SCOPE RULE** Do not combine reliability, adaptation, efficiency, multilinguality, RAG, video, medical data, and a new dataset in one undergraduate thesis. One primary problem plus one controlled secondary lens is the maximum. |

## 4.2 Application Settings That May Be Used

Application settings are test environments, not new parent fields. They may be selected only when data, evaluation, and domain requirements pass the feasibility gate.

* Document and chart understanding.
* Image-text reasoning and visual question answering.
* AI-generated image detection as a generalization or trustworthiness problem.
* Low-resource or Bengali multimodal evaluation, if ground truth can be created or verified responsibly.
* Medical images only with public datasets and without unsupported clinical claims.
* Short-video understanding only if feature extraction and evaluation fit the compute budget.

## 4.3 Explicitly Parked Fields

The following are not active thesis fields. They may be revisited after the current thesis, but they must not consume literature-review time now.

| **Parked field** | **Reason for exclusion from current thesis discovery** |
| --- | --- |
| Standalone cybersecurity | New domain foundation, no dependable security supervision, and current goals are better served by AI-centered VLM research. |
| Federated learning | High methodological and systems burden with weaker direct fit to the frozen parent field. |
| Diffusion or generative-model training | High compute and crowded novelty landscape; may be used only as a tool, not the research field. |
| 3D, robotics, autonomous driving, specialized sensing | Geometry, simulation, hardware, or sensor requirements exceed current scope. |
| Standalone medical imaging | Requires domain validation that is not reliably available. |
| Standalone XAI | Evaluation is often weak or subjective; interpretability may be used only when tied to a measurable reliability claim. |
| Generic RAG or agent application | A working system alone is an engineering project, not a research contribution. |
| Generic image classification or detection | Highly saturated unless the research claim concerns reliability, shift, efficiency, or another defensible problem. |

# 5. Topic Discovery Protocol

## 5.1 Funnel

1. **Step 1, define the failure:** State what current VLMs fail to do, under what condition, and why the failure matters.
2. **Step 2, verify the gap:** Check recent primary papers, official repositories, benchmark leaderboards, and subsequent work. A model-generated novelty claim is never sufficient.
3. **Step 3, verify assets:** Confirm dataset access, license, schema, model weights, baseline code, and evaluation tooling.
4. **Step 4, reproduce a baseline:** Run the simplest strong baseline on a small sample before proposing a new method.
5. **Step 5, run a pilot:** Demonstrate that the claimed failure is measurable and that runtime is acceptable.
6. **Step 6, score and challenge:** Apply the scorecard and request a skeptical independent review.
7. **Step 7, freeze one topic:** Complete the Topic Freeze Record and replace field discovery with a versioned Thesis Specification.

## 5.2 Candidate Limit

Maintain no more than three active topic candidates, one per ranked research field. Investigate one candidate per chat or session. A candidate that lacks a dataset, baseline, evaluation plan, and stated risk is not active; it is only an idea.

## 5.3 Literature Search Standard

* Begin with one recent primary paper that precisely defines the problem and terminology.
* Trace backward to seminal methods and forward to 2025–2026 competing work.
* Use surveys only for orientation. Verify all decisive claims against original papers or official documentation.
* Record dataset, model, split, baseline, metric, compute, code availability, limitation, and exact relevance for every core paper.
* Do not perform a full literature review until the feasibility gate passes.

# 6. Mandatory Topic Feasibility Gate

Score each candidate from 1 to 5. A candidate needs at least 25/35, no score below 3 for Dataset Access, Colab Feasibility, or Baselines and Evaluation, and all hard gates must pass.

| **Criterion** | **1, weak** | **3, acceptable** | **5, strong** |
| --- | --- | --- | --- |
| Problem clarity | Vague task or solution first | Bounded failure and users | Precise claim, setting, and consequence |
| Evidence of a real gap | Blog or assumed novelty | Recent papers show limitation | Gap verified across primary sources and baselines |
| Dataset access and quality | Unavailable or unclear | Public with manageable caveats | Public, documented, licensed, and well matched |
| Colab Pro feasibility | Requires sustained large compute | Pilot and main runs fit with controls | Comfortable repeated runs with fallback |
| Baselines and evaluation | Weak or undefined | Reproducible strong baselines and direct metrics | Multiple strong baselines, ablations, robust protocol |
| Domain-dependence risk | Unavailable expert required | Some learnable domain knowledge | AI/CSE-centered with independently verifiable labels |
| Career and research value | Narrow demo | Transferable techniques | Strong research and engineering signal |

## 6.1 Hard Gates

* At least one official dataset or benchmark source is accessible and legally usable.
* At least one strong baseline can be reproduced without a paid API.
* A Colab pilot can finish within a practical session and yields interpretable outputs.
* The primary metric directly tests the main claim and cannot be replaced by accuracy alone.
* The contribution can be stated in one sentence without using 'apply', 'combine', or 'use model X on dataset Y' as the main novelty.
* The recent literature search does not show that the same contribution has already been completed.
* A fallback remains meaningful if the proposed method fails.

## 6.2 Kill Criteria

* Required data, labels, models, or baseline code cannot be accessed or legally used.
* The baseline cannot be reproduced after a bounded debugging effort and no equivalent baseline exists.
* The measured failure disappears under a correct split or stronger baseline.
* The main result depends on one stochastic LLM judge with no validation.
* The method needs sustained GPU resources beyond the available budget.
* The contribution reduces to a leaderboard comparison, application demo, or expected result.

# 7. Publication-Quality Contribution Standard

A strong thesis and a publishable paper are related but not identical. The thesis must be complete and defensible. Publication additionally requires a contribution that matters beyond the local dataset or implementation.

| **Contribution type** | **Acceptable form** | **Common weak form** |
| --- | --- | --- |
| Method | New objective, mechanism, architecture component, adaptation rule, or inference strategy with ablations. | Minor loss-term change with marginal gain. |
| Evaluation or benchmark | New capability definition, validated protocol, reliable annotations, strong baselines, and evidence that rankings or conclusions change. | Collect examples and report model scores. |
| Empirical measurement | Reveals a systematic failure, boundary, or trade-off across models and conditions with actionable conclusions. | Compare several models and restate known behavior. |
| Systems or efficiency | New efficiency method or verified accuracy-latency-memory-reliability trade-off on actual hardware. | Report parameter count and compression ratio only. |
| Dataset | Documented collection, license, representativeness, quality control, benchmark tasks, and reusable hosting. | Small scraped dataset with uncertain rights or labels. |
| Replication plus extension | Faithful reproduction followed by a substantive new condition, correction, or generalization result. | Reproduce published numbers with no new question. |

## 7.1 Publication Gate

* One primary research question and no more than two supporting questions.
* A contribution statement that names what is new, compared with what, and why it matters.
* At least two to four meaningful baselines, including a simple strong baseline and the closest prior method where feasible.
* Evidence across multiple models, datasets, domains, or shifts appropriate to the claim.
* Ablations that isolate each proposed component from preprocessing, prompt, or training confounds.
* Error analysis and limitations that explain failure cases rather than hiding them.
* Reproducible code, environment, split, prompt, seed, and evaluation details.

|  |
| --- |
| **VENUE REALITY** Efficient AI, trustworthy VLMs, and generalization work all appear in strong computer-vision venues. The field is not the obstacle. Incremental contribution, weak controls, and irreproducible evaluation are the obstacles. |

# 8. Experimental Design Standard

## 8.1 Research Question Template

Does [intervention or condition] change [primary outcome] for [model and task setting] under [dataset, shift, or constraint], compared with [strong baseline], while preserving [utility, robustness, or efficiency constraint]?

## 8.2 Baseline Policy

* Lower bound: a simple, transparent baseline or unmodified model.
* Strong practical baseline: a reproducible current method with public code.
* Closest scientific baseline: the method that most directly competes with the proposed contribution.
* Control baseline: random, size-matched, compute-matched, prompt-matched, or no-adaptation control when needed to isolate the claimed mechanism.
* Published numbers may be contextual references, but claims of improvement require locally comparable runs whenever practical.

## 8.3 Metric Policy

| **Claim type** | **Required metric families** | **Do not rely on** |
| --- | --- | --- |
| Task capability | Task-specific accuracy/F1/EM/retrieval metrics plus per-category analysis | Aggregate accuracy only |
| Hallucination/grounding | Capability-specific error rate, grounding score, precision/recall, and human-validated subset | One LLM judge score |
| Calibration/abstention | ECE or calibration error, risk-coverage curve, AUROC/AUPRC, retained utility | Confidence average |
| Distribution shift | In-domain versus shifted gap, worst-domain performance, degradation curve, recovery | Random split performance |
| Efficiency | Latency, throughput, peak memory, model size, compute estimate, and retained quality | Parameter count alone |
| Robustness/safety | Attack or failure success plus benign utility and false refusal | Failure rate without task utility |

## 8.4 Statistical and Reporting Rules

* Use fixed and documented train/validation/test splits. Use temporal or cross-source splits when the claim concerns shift.
* Report multiple seeds for training-based results when feasible. For expensive inference-only evaluations, use bootstrap confidence intervals or repeated decoding where stochasticity matters.
* Report variance, confidence intervals, or effect sizes when comparing small differences.
* Predefine the primary metric and avoid selecting the best metric after observing results.
* Document prompts, decoding parameters, quantization settings, preprocessing, and judge instructions.
* Treat LLM-as-a-judge as a measurement instrument that requires validation, not as ground truth.
* The NeurIPS checklist is the default rigor checklist for reproducibility, transparency, ethics, and societal impact [18].

# 9. Compute and Implementation Policy

## 9.1 Default Compute Strategy

* Prefer open-weight VLMs that can run through quantized inference or adapters on Colab Pro.
* Start with one small or medium model and a small benchmark slice. Expand only after the pipeline and metrics are verified.
* Prefer inference-only evaluation, parameter-efficient adaptation, feature caching, or lightweight heads over full-model training.
* Do not build a thesis that requires training a foundation model, repeated 30B+ model runs, or sustained multi-GPU infrastructure.
* Use stronger temporary hardware only to scale an already validated experiment, never to rescue an infeasible design.
* Record runtime, GPU type, peak memory, precision, batch size, model revision, and software versions for every reported experiment.

## 9.2 Escalation Rule

A candidate may request limited stronger compute only after it passes dataset access, baseline reproduction, metric validation, and a Colab pilot. The request must estimate the number of runs, expected hours, storage, and the scientific reason the stronger hardware changes the evidence.

## 9.3 Paid API Policy

* No primary result may depend on a paid proprietary API.
* A proprietary model may appear only as an optional contextual reference when published or free evaluation results are available.
* If API behavior changes over time, record model version, access date, parameters, and any non-reproducibility risk.
* A candidate fails if its central comparison cannot be reproduced without unaffordable API usage.

# 10. Data, Model, Ethics and Governance

## 10.1 Dataset Acceptance Checklist

* Official source and stable download location verified.
* License or terms permit the intended academic use and derived reporting.
* Schema, labels, collection process, time period, and known biases understood.
* Duplicates, leakage, benchmark contamination, class imbalance, and source overlap checked.
* Personally identifiable or sensitive data handled only when necessary, lawful, and ethically justified.
* Dataset limitations documented using a datasheet-style record [19].

## 10.2 Model Acceptance Checklist

* Weights, license, model card, revision, tokenizer/processor, and intended use verified.
* The model can complete the unmodified task well enough for the research metric to be meaningful.
* Training-data contamination and benchmark memorization risks considered where documentation exists.
* Quantization, chat templates, prompt format, and decoding settings are pinned.
* Performance and limitations are reported in a model-card-style summary [20].

## 10.3 Trustworthiness Scope

Trustworthiness is not a vague synonym for high accuracy. The NIST AI Risk Management Framework identifies valid and reliable, safe, secure and resilient, accountable and transparent, explainable and interpretable, privacy-enhanced, and fair characteristics [21]. A thesis should select only the characteristics directly connected to its research question and context of use.

|  |
| --- |
| **ETHICS RULE** Do not overclaim safety, fairness, medical utility, or real-world deployment. Report exactly what the benchmark supports, disclose untested populations and conditions, and state who could be harmed by model errors. |

# 11. Reproducibility and Engineering Standard

## 11.1 Required Project Artifacts

* README with research question, environment, data acquisition, and exact reproduction commands.
* Version-controlled source code with configuration files rather than notebook-only hidden state.
* Locked environment file, package versions, model revisions, and hardware notes.
* Deterministic or documented split generation and seeds.
* Baseline, proposed method, evaluation, ablation, and figure-generation scripts.
* Experiment registry recording run ID, commit, configuration, data version, result, and failure notes.
* Model and dataset documentation, including licenses and limitations.
* Final tables generated from machine-readable experiment outputs, not manually copied values.

## 11.2 Suggested Repository Shape

| **Path** | **Purpose** |
| --- | --- |
| configs/ | Versioned baseline, method, model, dataset, and ablation configurations. |
| data/README.md | Acquisition instructions, licenses, hashes, splits, and files that must not be committed. |
| src/ | Reusable data, model, method, and evaluation modules. |
| scripts/ | Explicit preprocessing, training, inference, evaluation, and figure commands. |
| experiments/ | Run manifests and machine-readable summaries, not large checkpoints. |
| notebooks/ | Exploration and presentation only; canonical results must be reproducible through scripts. |
| paper/ | Manuscript, bibliography, figures, tables, and submission checklist. |
| docs/ | Decision log, dataset card, model card, risk register, and experiment protocol. |

For dataset or evaluation contributions, current NeurIPS guidance emphasizes accessible code/data, long-term hosting, metadata, limitations, and responsible-AI documentation [22, 23]. These requirements are used as design guidance even when NeurIPS is not the target venue.

# 12. Thesis-to-Publication Strategy

## 12.1 Canonical Strategy

Design the thesis from day one so that its data, baselines, protocols, code, ablations, and limitations can support a reputable submission. Do not delay thesis completion to chase venue-specific novelty or endless additional experiments. Once the thesis evidence is complete, decide whether the work is submission-ready or needs a focused extension.

| **Stage** | **Thesis objective** | **Publication-aware action** |
| --- | --- | --- |
| Topic selection | Choose a finishable, defensible question | Verify the gap and identify the closest competing papers |
| Baseline | Establish a trustworthy reference result | Use public code, record versions, and reproduce locally |
| Method/evaluation | Test the central claim | Define contribution and ablation plan before full runs |
| Full experiments | Produce complete evidence | Use venue-level controls, seeds, error analysis, and limitations |
| Thesis writing | Explain the work transparently | Maintain paper-ready figures, tables, and bibliography |
| Post-thesis decision | Close the university deliverable | Submit if the contribution is mature; otherwise add one targeted extension |

## 12.2 Venue Families

Venue selection occurs after the contribution and evidence are known. Computer vision commonly values selective conferences as major publication venues, so a reputable conference is not inferior merely because it is not a journal. Potential venue families include CVPR, ICCV, ECCV, WACV, ACM Multimedia, Transactions on Machine Learning Research, Pattern Recognition, International Journal of Computer Vision, and IEEE Transactions on Pattern Analysis and Machine Intelligence. The final choice must follow the current official scope, quality bar, submission policy, page limit, and dual-submission rules.

## 12.3 Submission Readiness Gate

* The abstract states one clear contribution and does not rely on inflated novelty language.
* The closest prior work is reproduced or compared under a defensible protocol.
* Results support every title and abstract claim.
* Figures and tables expose trade-offs, variance, and failures, not only best scores.
* Ablations isolate the proposed mechanism.
* Code and data documentation are sufficient for independent reproduction.
* Limitations, ethical considerations, compute, and potential misuse are disclosed.
* The venue is reputable, in scope, and not selected merely because publication appears easy.

# 13. Research Workflow

## 13.1 Platform Roles

| **Platform** | **Primary role** | **Do not use it as** |
| --- | --- | --- |
| Perplexity | Find current papers, official datasets, repositories, benchmark pages, and citation trails. | Final judge of novelty or feasibility. |
| Claude | Read and synthesize a small set of full papers; compare methods, experiments, and limitations. | Source of unverified current facts. |
| ChatGPT | Research strategy, feasibility audit, RQ design, experiments, implementation support, and specification updates. | Storage for unrecorded final decisions. |
| Kimi | Independent skeptical review, stronger baseline search, hidden-complexity and novelty challenge. | Sole evidence source. |
| Canonical specification | Record the frozen field, accepted topic, rules, decisions, and changes. | A dumping ground for raw papers and temporary notes. |

## 13.2 Required Session Output

* Direct answer in three to eight bullets.
* Evidence table with claim, source, confidence, and limitation.
* Verdict: continue, narrow, park, or reject.
* One next action that can be completed in 30–90 minutes.
* Decision-log entry when direction, scope, dataset, method, or evaluation changes.

## 13.3 Research Phases Without Calendar Dates

1. **Phase A, orientation:** learn the field vocabulary and read a bounded set of primary papers.
2. **Phase B, candidate screening:** generate no more than three candidates and apply the feasibility gate.
3. **Phase C, pilot:** verify data, baseline, metrics, and compute on a small subset.
4. **Phase D, topic freeze:** complete the Topic Freeze Record and create Thesis Specification v1.
5. **Phase E, baseline system:** build a reproducible end-to-end baseline before implementing the contribution.
6. **Phase F, contribution:** implement one primary intervention or evaluation protocol and its ablations.
7. **Phase G, full evidence:** run controlled experiments, error analysis, robustness checks, and efficiency measurements.
8. **Phase H, thesis and paper:** write the thesis, audit claims, then decide on submission or one focused extension.

# 14. Operational Templates and Checklists

## 14.1 Candidate Topic Brief

| **Field** | **Required entry** |
| --- | --- |
| Candidate name | Short descriptive label, not a final title. |
| Primary research field | Rank 1, 2, or 3 from this specification. |
| Observed failure | What fails, under which condition, and for whom it matters. |
| Research question | Testable question with intervention/condition, outcome, setting, and baseline. |
| Gap evidence | Three to six primary papers and the precise unresolved point. |
| Dataset/benchmark | Official link, license, size, labels, split, known risks, and access status. |
| Models | Open weights, license, size, compute estimate, and benign task capability. |
| Baselines | Simple baseline, strong practical baseline, closest prior method, and necessary controls. |
| Evaluation | Primary metric, supporting metrics, ablations, error analysis, and success criterion. |
| Compute | Pilot and full-run estimate, GPU, storage, seeds, and fallback. |
| Contribution | Method, evaluation, empirical measurement, system, dataset, or replication plus extension. |
| Kill criteria | Conditions that force rejection or narrowing. |

## 14.2 Topic Freeze Checklist

* Research question is narrow and testable.
* Gap is verified against recent primary work.
* Dataset and model access are confirmed, not assumed.
* A strong baseline has been reproduced.
* A pilot demonstrates the failure or opportunity.
* Compute estimate includes repeated runs and ablations.
* Primary and supporting metrics directly test the claim.
* Contribution survives comparison with a simple strong baseline.
* Risk register and meaningful fallback are written.
* Score is at least 25/35 with no hard-gate failure.

## 14.3 Strong Security and Trustworthiness Paper Checks

Use this only when the selected VLM topic involves jailbreaks, adversarial robustness, privacy, harmful content, or security. Security is then a property of the VLM system, not a reopening of standalone cybersecurity.

* Define the protected property, attacker capability, attack surface, and success condition.
* Measure benign task utility alongside attack or failure success.
* Use a baseline attack, baseline defense, and no-attack control.
* Separate inability to perform the task from resistance to the attack.
* Report false refusal, transferability, stochasticity, and prompt/model version.
* Do not release harmful artifacts without a proportionate risk review.

## 14.4 Paper Writing Checklist

* Title and abstract match the actual evidence and scope.
* Introduction identifies the problem, gap, contribution, and evidence without unsupported market claims.
* Related work compares mechanisms and limitations, not one-paragraph summaries.
* Method is precise enough to reproduce, including prompts and preprocessing.
* Experimental setup names data, splits, models, baselines, compute, seeds, and metrics.
* Results answer each research question and include uncertainty where relevant.
* Ablations isolate every claimed component.
* Error analysis explains representative successes and failures.
* Limitations distinguish untested from failed conditions.
* Code, configuration, data instructions, and references are complete.

# 15. Topic Freeze Record

Complete this section only after a candidate passes the feasibility gate. When completed, create a separate versioned Thesis Specification v1. Do not overwrite this field-level specification.

| **Specification item** | **To be completed after topic freeze** |
| --- | --- |
| Working title |  |
| Primary research field |  |
| Research question |  |
| Problem setting and boundaries |  |
| Dataset and access status |  |
| Models and licenses |  |
| Proposed contribution |  |
| Explicit non-contributions |  |
| Reproducible baselines |  |
| Metrics, ablations, and success criteria |  |
| Compute budget and fallback |  |
| Core papers |  |
| Main risks and kill criteria |  |

# 16. Decision Log

| **Date** | **Decision** | **Status** | **Evidence-based reason** | **Next action** |
| --- | --- | --- | --- | --- |
| 20 Aug 2026 | Broad thesis exploration | Closed | Multiple fields were under consideration; no topic was frozen. | Apply a common feasibility framework. |
| 21 Aug 2026 | Cybersecurity field screening | Parked | Standalone cybersecurity added domain and supervision risk; reviewed candidates also contained dataset, baseline, or evaluation problems. | Retain security only as a future field or VLM property. |
| 22 Aug 2026 | Parent field freeze | Active | Multimodal/VLM research offers the best balance of background fit, active research, public assets, AI-career transfer, and self-directed feasibility. | Screen Rank 1 candidate topics first. |
| 22 Aug 2026 | Three ranked research fields | Active | Trustworthiness first, distribution shift second, efficiency conditional third. | Produce field-level feasibility cards before topic generation. |

## 16.1 Future Decision Entry

| **Date** | **Candidate/change** | **Verdict** | **Evidence and limitation** | **Next action** |
| --- | --- | --- | --- | --- |
|  |  | Continue / Narrow / Park / Reject |  |  |
|  |  | Continue / Narrow / Park / Reject |  |  |
|  |  | Continue / Narrow / Park / Reject |  |  |

# 17. Change Control

* **Patch update, v1.0.x:** wording, source links, minor clarification, or formatting with no decision change.
* **Minor update, v1.x:** research-lane ranking, feasibility threshold, or workflow change supported by new evidence.
* **Major update, v2.0:** parent-field change. Requires documented failure of the current field, a replacement feasibility audit, and explicit decision log.
* **Topic specification:** created as a separate document after topic freeze; it does not replace or silently rewrite this field specification.

# References and Primary Sources

[[1] IEEE/CVF, CVPR 2025 Call for Papers.](https://cvpr.thecvf.com/Conferences/2025/CallForPapers)

[[2] IEEE/CVF, CVPR 2026 Call for Papers.](https://cvpr.thecvf.com/Conferences/2026/CallForPapers)

[[3] IEEE/CVF, CVPR 2026 Tentative Schedule.](https://cvpr.thecvf.com/Conferences/2026/TentativeSchedule)

[[4] Liu et al., PhD: A ChatGPT-Prompted Visual Hallucination Evaluation Dataset, CVPR 2025.](https://openaccess.thecvf.com/content/CVPR2025/html/Liu_PhD_A_ChatGPT-Prompted_Visual_Hallucination_Evaluation_Dataset_CVPR_2025_paper.html)

[[5] Zhang et al., Critic-V: VLM Critics Help Catch VLM Errors in Multimodal Reasoning, CVPR 2025.](https://openaccess.thecvf.com/content/CVPR2025/html/Zhang_Critic-V_VLM_Critics_Help_Catch_VLM_Errors_in_Multimodal_Reasoning_CVPR_2025_paper.html)

[[6] Yin et al., ClearSight: Visual Signal Enhancement for Object Hallucination Mitigation in Multimodal LLMs, CVPR 2025.](https://openaccess.thecvf.com/content/CVPR2025/html/Yin_ClearSight_Visual_Signal_Enhancement_for_Object_Hallucination_Mitigation_in_Multimodal_CVPR_2025_paper.html)

[[7] Jiang et al., Breaking the Illusion: When Positive Meets Negative in Multimodal Decoding, CVPR 2026.](https://openaccess.thecvf.com/content/CVPR2026/papers/Jiang_Breaking_the_Illusion_When_Positive_Meets_Negative_in_Multimodal_Decoding_CVPR_2026_paper.pdf)

[[8] Jeong et al., Draft and Refine with Visual Experts, CVPR 2026.](https://openaccess.thecvf.com/content/CVPR2026/papers/Jeong_Draft_and_Refine_with_Visual_Experts_CVPR_2026_paper.pdf)

[[9] He et al., Structural Graph Probing of Vision-Language Models, CVPR 2026.](https://openaccess.thecvf.com/content/CVPR2026/papers/He_Structural_Graph_Probing_of_Vision-Language_Models_CVPR_2026_paper.pdf)

[[10] Dai et al., Free on the Fly: Enhancing Flexibility in Test-Time Adaptation with Online EM, CVPR 2025.](https://openaccess.thecvf.com/content/CVPR2025/html/Dai_Free_on_the_Fly_Enhancing_Flexibility_in_Test-Time_Adaptation_with_CVPR_2025_paper.html)

[[11] Zhang et al., SCAP: Transductive Test-Time Adaptation via Supportive Clique-based Attribute Prompting, CVPR 2025.](https://openaccess.thecvf.com/content/CVPR2025/html/Zhang_SCAP_Transductive_Test-Time_Adaptation_via_Supportive_Clique-based_Attribute_Prompting_CVPR_2025_paper.html)

[[12] Li et al., Towards Multimodal Domain Generalization with Few Labels, CVPR 2026.](https://openaccess.thecvf.com/content/CVPR2026/papers/Li_Towards_Multimodal_Domain_Generalization_with_Few_Labels_CVPR_2026_paper.pdf)

[[13] Chen et al., RobustVisRAG: Causality-Aware Vision-Based Retrieval-Augmented Generation under Visual Degradations, CVPR 2026.](https://openaccess.thecvf.com/content/CVPR2026/papers/Chen_RobustVisRAG_Causality-Aware_Vision-Based_Retrieval-Augmented_Generation_under_Visual_Degradations_CVPR_2026_paper.pdf)

[[14] Wu et al., APHQ-ViT: Post-Training Quantization with Average Perturbation Hessian Based Reconstruction for Vision Transformers, CVPR 2025.](https://openaccess.thecvf.com/content/CVPR2025/html/Wu_APHQ-ViT_Post-Training_Quantization_with_Average_Perturbation_Hessian_Based_Reconstruction_for_CVPR_2025_paper.html)

[[15] Fu et al., Quantization without Tears, CVPR 2025.](https://openaccess.thecvf.com/content/CVPR2025/html/Fu_Quantization_without_Tears_CVPR_2025_paper.html)

[[16] Alvar et al., DivPrune: Diversity-based Visual Token Pruning for Large Multimodal Models, CVPR 2025.](https://openaccess.thecvf.com/content/CVPR2025/html/Alvar_DivPrune_Diversity-based_Visual_Token_Pruning_for_Large_Multimodal_Models_CVPR_2025_paper.html)

[[17] Wu et al., Collaborative Multi-Mode Pruning for Vision-Language Models, CVPR 2026.](https://openaccess.thecvf.com/content/CVPR2026/papers/Wu_Collaborative_Multi-Mode_Pruning_for_Vision-Language_Models_CVPR_2026_paper.pdf)

[[18] NeurIPS, Paper Checklist Guidelines.](https://neurips.cc/public/guides/PaperChecklist)

[[19] Gebru et al., Datasheets for Datasets, Communications of the ACM, 2021.](https://dl.acm.org/doi/10.1145/3458723)

[[20] Mitchell et al., Model Cards for Model Reporting, FAT\* 2019.](https://dl.acm.org/doi/10.1145/3287560.3287596)

[[21] NIST, Artificial Intelligence Risk Management Framework 1.0.](https://www.nist.gov/publications/artificial-intelligence-risk-management-framework-ai-rmf-10)

[[22] NeurIPS 2026, Evaluations and Datasets Track Call for Papers.](https://neurips.cc/Conferences/2026/CallForEvaluationsDatasets)

[[23] NeurIPS 2026, Code and Data Submission Policy.](https://neurips.cc/public/guides/CodeSubmissionPolicy)

*Source note: The Paper Digest CVPR 2025 topic clustering was used only as an orientation aid. Field decisions and technical claims in this specification rely on official venue pages, primary papers, or recognized standards.*