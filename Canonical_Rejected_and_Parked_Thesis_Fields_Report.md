## D:/Thesis/Canonical_Rejected_and_Parked_Thesis_Fields_Report.docx
**THESIS RESEARCH GROUND**

Canonical Rejected and Parked
Thesis Fields Report

Long-term decision record for a frozen Multimodal / Vision-Language Learning and Systems parent field

|  |
| --- |
| **CANONICAL STATUS** Parent field frozen. Final thesis topic not frozen. Only the three ranked VLM lanes are active for current topic discovery. |

| **Document control** | **Canonical value** |
| --- | --- |
| Research cutoff | 22 August 2026 |
| Authority | Canonical Thesis Field Specification v1.0 |
| Researcher | Final-year undergraduate CSE student; technical lead in a three-person team |
| Compute boundary | Local CPU/8 GB RAM; Google Colab Pro as primary GPU environment |
| Document purpose | Prevent casual reopening of inferior field choices under current constraints |

*Private research specification | Evidence-based judgment, not a claim that excluded fields are scientifically weak*

# 1. Document Purpose

This report records what each canonically parked field studies, how credible research is normally conducted, why the field is valuable, why it is currently inferior to the frozen VLM direction, whether any component may support a VLM thesis, and what observable evidence would be required for reconsideration.

The report is a decision-control document, not a general textbook and not a claim that every possible topic in a parked field is impossible. “Parked” and “rejected” refer to suitability under the researcher’s present constraints.

|  |
| --- |
| **DIRECT RULE** An attractive paper, framework, benchmark score, or demo does not reopen a field. Reconsideration requires the written protocol in Section 14. |

# 2. Status and Authority

Authority order used in this report: (1) Canonical Thesis Field Specification; (2) Thesis Control Center; (3) supplied evaluation material; (4) conversation context. The Canonical Thesis Field Specification v1.0 is the controlling source.

The supplied Paper Digest CVPR 2025 topic clustering was read as orientation material only. Consistent with the canonical source note, it was not used to assign status or prove feasibility.

No unresolved contradiction prevents this report. The older Thesis Control Center described broad topic discovery; the later Canonical Thesis Field Specification formally freezes the VLM parent field. Under the authority order, the later canonical freeze controls.

# 3. Researcher Profile and Constraints

* Final-year undergraduate CSE student with strongest preparation in AI/ML, deep learning, Transformers, LLM/VLM fundamentals, Python, and web/API development.
* Three-person thesis team; the principal researcher is expected to lead most design, implementation, evaluation, and writing.
* No reliable medical, pharmaceutical, biological, nanotechnology, robotics, electronics, cybersecurity, or sensor-domain supervisor.
* Local machine: AMD Ryzen 5 5600G, 8 GB RAM, integrated AMD graphics, and no usable local training GPU.
* Google Colab Pro is the normal GPU environment; stronger temporary compute may scale a validated pilot but cannot rescue an infeasible design.
* No paid datasets, primary dependence on paid APIs, private institutional data, hospital partnership, wet lab, robot, vehicle, special sensor, or custom hardware.
* Required thesis properties: public/legal data, reproducible strong baseline, direct measurable evaluation, controlled scope, and a contribution beyond applying an existing model.
* Career objective: AI/ML engineering or AI research; build a strong thesis first while keeping data, code, protocols, and experiments publication-ready.

# 4. Frozen Field and Ranked VLM Lanes

|  |
| --- |
| **FROZEN PARENT FIELD** Multimodal / Vision-Language Learning and Systems |

| **Rank** | **Authorized lane** | **Operating meaning** |
| --- | --- | --- |
| 1 | Trustworthy and Reliable VLMs | Primary lane: grounding, hallucination, calibration, abstention, robustness, and valid evaluation. |
| 2 | VLM Generalization, Adaptation and Distribution Shift | Secondary lane: cross-source/domain/language/style/corruption shifts and carefully controlled adaptation. |
| 3 | Efficient and Scalable VLMs | Conditional lane: latency, memory, visual-token processing, compression, and reliability-aware efficiency. |

The parent field must not be reopened by this report. The final thesis topic remains open and must separately pass dataset, baseline, evaluation, compute, contribution, and fallback validation.

# 5. Meaning of the Status Labels

| **Label** | **Operational definition** |
| --- | --- |
| Active | A field or lane currently authorized for thesis-topic investigation. |
| Parked | A potentially valuable field deliberately deferred because it is currently less suitable than the frozen direction. It must not consume present literature-review or experimentation time. |
| Rejected | A field or candidate that fails important feasibility, evaluation, contribution, supervision, data-access, or scope requirements for this thesis. |
| Narrowed | A broad field unsuitable as the thesis identity but containing a smaller problem compatible with the active VLM field. |
| Supporting Method Only | A method that may be used inside the final VLM thesis but must not become a separate thesis field. |
| Unassessed | A field for which the supplied authoritative documents contain insufficient evidence. It must not be silently converted into parked or rejected. |

Important consistency finding: the canonical specification records all eight excluded groups as Parked. It records no parent field as Rejected, Narrowed, or Supporting Method Only. Some parked fields contain methods or application contexts that may support VLM work, but their canonical status remains Parked.

# 6. Decision Framework and Hard Feasibility Gates

The 1–5 scores in this report are decision aids, not mathematical measurements. Each criterion receives a one-sentence justification in the relevant dossier. Scores do not replace the canonical topic feasibility gate and cannot compensate for a failed hard gate.

## 6.1 Hard gates

* At least one official dataset or benchmark is accessible and legally usable.
* At least one strong baseline can be reproduced without a paid API.
* A Colab pilot finishes in a practical session and yields interpretable output.
* The primary metric directly tests the main claim; aggregate accuracy alone is insufficient when the claim concerns reliability, shift, safety, privacy, or efficiency.
* The contribution can be stated without “apply,” “combine,” or “use model X on dataset Y” as the main novelty.
* Recent primary literature does not show that the same contribution is already complete.
* A meaningful fallback remains if the proposed method fails.
* Unavailable specialist supervision, private data, human experts, hardware, or sustained compute are treated as gates when the main claim depends on them.

## 6.2 Report score criteria

| **Criterion** | **Required question** |
| --- | --- |
| Problem clarity | Can a specific, testable research question be formulated? |
| Dataset access | Is appropriate data publicly and legally accessible? |
| Baseline reproducibility | Can at least one strong baseline be reproduced? |
| Compute feasibility | Can the minimum experiment run reliably on Colab Pro? |
| Evaluation validity | Do the metrics directly test the proposed claim? |
| Domain dependence | Can work finish without unavailable specialist supervision? |
| Contribution potential | Is there room for more than applying an existing model? |
| Scope control | Can three undergraduates complete it? |
| Engineering burden | Will infrastructure overwhelm research? |
| Career alignment | Does it strengthen relevant AI/ML skills? |
| Opportunity cost | Is it more rational than continuing in the frozen VLM field? |

# 7. Executive Decision Summary

| **Field dossier** | **Canonical status** | **Controlling reason** | **Possible VLM relationship** |
| --- | --- | --- | --- |
| Standalone Cybersecurity | Parked | Domain-supervision and evaluation-validity risk outweigh current fit. | Compatible application context |
| Federated Learning | Parked | Systems and methodological burden is high relative to fit with the frozen VLM direction. | Compatible only after major narrowing |
| Diffusion or Generative-Model Training as the Main Field | Parked | Compute and evaluation burden are disproportionate to an undergraduate thesis. | Compatible supporting method |
| 3D Vision | Parked | Geometry, preprocessing, and tooling add a new foundation that the current thesis does not need. | Compatible only after major narrowing |
| Robotics | Parked | Unavailable hardware and robotics supervision make credible validation impractical. | Compatible application context |
| Autonomous-Driving Research | Parked | The field requires industrial-scale data and safety-valid evaluation that the team cannot provide. | Compatible application context |
| Specialized Sensing | Parked | Sensor-specific validation and infrastructure are unavailable. | Compatible only after major narrowing |
| Standalone Medical Imaging | Parked | Clinical validation and error interpretation cannot be defended without a domain expert. | Compatible application context |
| Standalone Explainable AI (XAI) | Parked | Evaluation validity is too weak for standalone XAI under present conditions. | Compatible supporting method |
| Generic RAG Applications | Parked | Generic RAG is an engineering pattern, not a research field or contribution. | Compatible supporting method |
| Generic Agentic-AI Applications | Parked | Framework integration is easy, while rigorous, reproducible agent evaluation is expensive. | Compatible only after major narrowing |
| Generic Image Classification | Parked | The implementation is feasible, but the generic contribution is too weak and saturated. | Compatible supporting method |
| Generic Object Detection | Parked | A generic fine-tuned detector is an implementation project with weak novelty. | Compatible supporting method |

## 7.1 Requested fields without an authorized status

The task asked that these fields be checked. The canonical specification does not authorize a parked or rejected verdict for them; therefore they remain Unassessed. This is a status-control finding, not an invitation to investigate them now.

| **Field** | **Status** | **Reason** |
| --- | --- | --- |
| Broader healthcare AI | Unassessed as a parent field | The canonical specification only parks standalone medical imaging and permits medical images as a constrained application setting; it does not decide all healthcare AI. |
| Pharmaceutical or nanomedicine AI | Unassessed | The Thesis Control Center listed it as a candidate pool item, but the canonical specification does not assign a parked/rejected status. |
| Privacy-focused AI | Unassessed | Privacy appears as a trustworthiness characteristic and in the earlier candidate pool, not as a canonically decided standalone field. |
| LLM systems | Unassessed | Generic RAG/agents are parked, but the broader LLM-systems field is not assigned a canonical status. |
| Machine unlearning | Unassessed | It is not listed in the canonical parked-field table; no stronger status is authorized. |
| Video understanding or generation | Unassessed as a standalone field | Short-video understanding is allowed conditionally as a VLM application setting; standalone video generation may overlap parked generative training, but no independent canonical verdict exists. |

## 7.2 Canonical grouping preserved

The canonical table groups (a) 3D, robotics, autonomous driving, and specialized sensing; (b) generic RAG and agents; and (c) generic classification and detection. This report preserves those groups in summaries but separates dossiers because their data, infrastructure, evaluation, and supervision requirements differ substantially.

# 8. Individual Field Dossiers

Each dossier applies the same evidence-based structure. Suitability conclusions are reasoned judgments based on the cited evidence and the canonical researcher constraints; they are not claims made by the sources themselves.

## 8.1 Standalone Cybersecurity

|  |
| --- |
| **CANONICAL STATUS** Parked. Canonical group: Standalone cybersecurity. |

### A. What is this field?

Cybersecurity studies how to prevent, detect, understand, contain, and recover from attacks on software, networks, identities, data, and infrastructure. AI-based subfields include intrusion detection, malware classification, phishing or abuse detection, adversarial ML, threat intelligence, and automated vulnerability analysis. Important terms include threat model (who can attack and with what capability), attack surface (where the system can be attacked), false positive (benign activity flagged as malicious), and concept drift (attacks and normal behavior changing over time).

Major subfields: Network security; malware analysis; application and cloud security; cryptography; privacy; digital forensics; usable security; adversarial ML; AI system security.

Research versus implementation: A basic project trains a classifier on a public CSV and reports accuracy. Genuine research defines a realistic attacker and deployment setting, prevents leakage, uses temporal or cross-environment splits, compares against security baselines, measures operational false positives, and establishes that the result survives adaptive or shifted attacks.

### B. How does research in this field work?

* Data: packet captures and flow records, binaries or extracted features, logs, URLs, source code, vulnerability records, or controlled attack traces. CIC-IDS2017 and EMBER illustrate two very different data regimes [S02, S03].
* Preprocessing: reconstruct sessions, extract protocol or binary features, de-duplicate related samples, remove leakage, preserve time, and document label provenance. Random splitting is often invalid when near-duplicates or later samples leak into training.
* Models and baselines: rules/signatures, logistic regression or tree ensembles, anomaly detectors, CNN/Transformer encoders, graph models, and security-specific systems. A simple operational baseline is mandatory.
* Experiments: define attacker knowledge, train on past or source environments, test on future or different environments, and vary attack family, prevalence, evasion, or data drift.
* Metrics: precision, recall, F1, ROC-AUC or PR-AUC, false-positive rate at an operational threshold, time-to-detect, robustness over time, and cost. Accuracy alone is unsafe under class imbalance.
* Ablations and robustness: temporal vs random split, feature-family removal, evasion or obfuscation, unseen family tests, and prevalence sensitivity. TESSERACT shows why space-time bias can inflate results [S04].
* Reproducibility and infrastructure: dataset versions, capture conditions, safe sample handling, isolated environments, feature extractors, seeds, and exact attack scripts must be recorded.

### C. Why is this field valuable?

The field protects real systems and develops rigorous thinking about threats, distribution shift, monitoring, and failure costs. It initially looked attractive because security problems can appear highly publishable and employ ML. The transferable skills are useful, but the security reasoning is not optional: without it, the result is merely a generic classifier with a security label.

### D. Why is it parked for this researcher?

The following is a reasoned suitability judgment based on the cited technical evidence and the researcher profile.

**1. Hard blockers**

* No dependable cybersecurity supervisor to validate threat models, attack realism, or operational claims.
* The frozen parent field is VLM research; a standalone security thesis would require a formal major-version field change.

**2. Major risks**

* Public datasets can be stale, synthetic, imbalanced, duplicated, or easy to leak; a high score may not reflect deployment.
* Safe malware or exploit handling and realistic red-team evaluation add domain and infrastructure risk.
* Novelty is weak when the work is only a new classifier on CIC-IDS2017 or a benchmark comparison.

**3. Manageable limitations**

* Some tabular intrusion or malware baselines can run on Colab or CPU.
* Public datasets and reproducible code exist for carefully bounded tasks.

**4. Opportunity-cost reasons**

* Time spent learning security foundations and validating attacks displaces VLM paper reading, baseline reproduction, and pilot work.
* The same transferable robustness skills can be developed inside the active trustworthiness or distribution-shift lanes without changing domain.

### E. Why parked rather than permanently rejected?

Cybersecurity is scientifically valuable and viable with the right supervision, current threat data, and evaluation environment. It is parked, not condemned. A funded security lab, security co-supervisor, or later master’s project could make the domain-learning cost rational.

### F. Can it appear inside the frozen VLM field?

Relationship classification: Compatible application context.

Security may appear inside VLM work only as a measured VLM property, for example multimodal prompt-injection robustness, manipulated-image detection under unseen generators, or malicious image-text conflict. The thesis identity must remain VLM reliability or generalization, not network or malware security.

### G. What would justify reconsideration?

* A named cybersecurity co-supervisor agrees to validate the threat model and evaluation.
* A current, legally usable dataset with provenance and a deployment-faithful split is verified.
* A strong security baseline is reproduced and an adaptive or temporal evaluation is demonstrated.
* A written comparison shows the candidate is stronger than all three VLM lanes and documents the opportunity cost.

### Feasibility scorecard (1–5 decision aid)

| **Criterion** | **Score** | **One-sentence justification** |
| --- | --- | --- |
| Problem clarity | 4 | A specific task can be testable, but the broader field is too wide without a threat model. |
| Dataset access | 3 | Some public data exist, yet freshness, realism, and labels are recurring weaknesses. |
| Baseline reproducibility | 3 | Baselines exist, but reproducing a credible security evaluation is harder than fitting the model. |
| Compute feasibility | 4 | Many tabular or static-analysis experiments fit Colab, although dynamic or large-scale studies may not. |
| Evaluation validity | 2 | Metrics are clear only after the attacker, prevalence, and deployment conditions are correctly defined. |
| Domain dependence | 1 | Unavailable security supervision is a direct present constraint. |
| Contribution potential | 3 | Real gaps exist, but generic classifier substitutions have low contribution value. |
| Scope control | 2 | The domain-learning and validation burden is high for an undergraduate team. |
| Engineering burden | 3 | Safe environments, attack generation, and time-aware pipelines can dominate the research. |
| Career alignment | 3 | Security ML skills are useful but less direct than the frozen VLM lanes. |
| Opportunity cost | 1 | Changing fields would discard the strongest continuity and consume scarce discovery time. |

Unweighted mean: 2.64/5. This mean is descriptive only; hard blockers remain controlling.

### Curated evidence for this dossier

[S01] National Institute of Standards and Technology. Cybersecurity Framework 2.0. 2024. Official standard/framework. [Official/primary link](https://www.nist.gov/cyberframework). Relevance: Shows that cybersecurity spans governance, identification, protection, detection, response, and recovery rather than only an ML classifier.

[S02] Canadian Institute for Cybersecurity, University of New Brunswick. Intrusion Detection Evaluation Dataset (CIC-IDS2017). 2017. Official dataset page. [Official/primary link](https://www.unb.ca/cic/datasets/ids-2017.html). Relevance: Provides labeled flows and packet captures but also illustrates the specialized traffic-generation and labeling assumptions behind IDS research.

[S03] Joyce et al.. EMBER2024: A Benchmark Dataset for Holistic Evaluation of Malware Classifiers. 2025. arXiv preprint and official repository. [Official/primary link](https://arxiv.org/abs/2506.05074). Relevance: Documents a modern 3.2-million-file malware benchmark and the continuing dependence of malware research on industry-scale data curation.

[S04] Pendlebury et al.. TESSERACT: Eliminating Experimental Bias in Malware Classification across Space and Time. 2019. USENIX Security Symposium paper. [Official/primary link](https://www.usenix.org/conference/usenixsecurity19/presentation/pendlebury). Relevance: Shows how random or unrealistic splits can inflate malware-classification results and why temporal, deployment-aware evaluation matters.

### Direct verdict

| **Verdict element** | **Controlling statement** |
| --- | --- |
| Decision | Parked |
| Primary reason | Domain-supervision and evaluation-validity risk outweigh current fit. |
| Strongest blocker | No reliable security expert to validate whether the threat model and experiment are realistic. |
| What would change this decision | Verified expert supervision plus a current dataset, reproduced baseline, and deployment-faithful evaluation. |
| Present action | Preserve for later; use security only as a named VLM reliability/generalization context. |

## 8.2 Federated Learning

|  |
| --- |
| **CANONICAL STATUS** Parked. Canonical group: Federated learning. |

### A. What is this field?

Federated learning (FL) trains a shared model across multiple clients while raw data remain local. Cross-device FL models phones or edge devices; cross-silo FL models institutions such as hospitals or banks. Non-IID means client data distributions differ. Client drift is the divergence caused by local updates on heterogeneous data. Secure aggregation hides individual updates, while differential privacy limits what the final updates reveal.

Major subfields: Federated optimization; personalization; client selection; communication efficiency; privacy and secure aggregation; robustness to malicious clients; vertical FL; federated continual learning; evaluation under statistical and systems heterogeneity.

Research versus implementation: A basic project partitions MNIST, runs Flower, and compares FedAvg with centralized training. Genuine research defines realistic client distributions and participation, compares against strong FL optimizers, measures per-client and global outcomes, models communication or privacy cost, and isolates the claimed mechanism across heterogeneity levels.

### B. How does research in this field work?

* Data: naturally partitioned client data or defensible synthetic partitions. LEAF provides benchmark datasets and reference implementations for federated settings [S06, S07].
* Preprocessing: construct clients without leakage; specify client size, label skew, feature skew, temporal drift, availability, and train/validation/test separation.
* Architecture: a server selects clients, clients train locally, updates are aggregated, and the process repeats. FedAvg is the foundational baseline [S05].
* Baselines: centralized training, local-only models, FedAvg, FedProx or SCAFFOLD-like controls, plus size- and round-matched variants appropriate to the claim.
* Metrics: global and per-client accuracy, worst-client performance, fairness dispersion, convergence rounds, transmitted bytes, wall-clock time, privacy budget when used, and attack success for adversarial studies.
* Ablations: heterogeneity severity, clients per round, local steps, participation rate, aggregation rule, communication budget, and privacy/noise settings.
* Infrastructure: simulate many clients, cache or reload client data, manage repeated local training, and log round-level results. Flower explicitly schedules clients against available CPU/GPU resources [S08].

### C. Why is this field valuable?

FL addresses collaboration when data cannot be centralized and develops distributed-systems, optimization, privacy, and evaluation skills. It looked attractive because healthcare and privacy applications appear socially meaningful. The hard truth is that simulation makes implementation accessible but does not automatically make the research assumption realistic.

### D. Why is it parked for this researcher?

The following is a reasoned suitability judgment based on the cited technical evidence and the researcher profile.

**1. Hard blockers**

* The canonical specification explicitly parks FL because its methodological and systems burden has weaker direct fit to the frozen VLM field.
* A convincing cross-silo claim normally needs realistic institutional partitions or a defensible proxy; random client splits do not establish that claim.

**2. Major risks**

* Client simulation multiplies training cost and experiment count even when each model is small.
* It is easy to add differential privacy, secure aggregation, personalization, and RAG until the thesis becomes an uncontrolled stack.
* Novelty risk is high for a minor aggregation-weight or privacy-schedule variation without theory or broad empirical validation.

**3. Manageable limitations**

* Small-model FedAvg experiments and framework learning are feasible on Colab.
* Public benchmarks and open frameworks make baseline reproduction possible after careful scoping.

**4. Opportunity-cost reasons**

* FL would require a new literature base in distributed optimization and privacy while all three VLM lanes already match existing preparation.
* Federating a VLM would combine two costly problem families and is not justified during topic discovery.

### E. Why parked rather than permanently rejected?

FL remains appropriate for a later master’s thesis, a hospital or industry collaboration, or a project with stronger distributed-systems supervision and realistic client data. It is not the best present thesis identity.

### F. Can it appear inside the frozen VLM field?

Relationship classification: Compatible only after major narrowing.

A federated VLM study is theoretically possible, but it is an unnecessary intersection now. FL should not be added unless the VLM research question inherently requires decentralized data and the minimum experiment remains Colab-feasible.

### G. What would justify reconsideration?

* A public benchmark provides defensible natural client partitions matching the intended claim.
* FedAvg and at least one strong heterogeneity baseline are reproduced within a measured Colab budget.
* The contribution isolates one FL mechanism without adding unrelated privacy or RAG components.
* A written comparison shows that the FL candidate beats the three VLM lanes on evidence, feasibility, and opportunity cost.

### Feasibility scorecard (1–5 decision aid)

| **Criterion** | **Score** | **One-sentence justification** |
| --- | --- | --- |
| Problem clarity | 4 | FL questions can be precise once the client and heterogeneity assumptions are fixed. |
| Dataset access | 4 | LEAF and other public benchmarks are accessible, though realism may remain limited. |
| Baseline reproducibility | 4 | FedAvg and framework baselines are reproducible with open code. |
| Compute feasibility | 2 | Repeated client training and sweeps can exceed practical Colab sessions. |
| Evaluation validity | 4 | Standard metrics exist, but validity depends on realistic partition and systems assumptions. |
| Domain dependence | 3 | The work is AI-centered, although privacy or institutional claims may need specialist input. |
| Contribution potential | 3 | Contribution is possible, but incremental optimizer variants are crowded. |
| Scope control | 2 | The number of rounds, clients, seeds, and heterogeneity settings expands quickly. |
| Engineering burden | 2 | Simulation orchestration and round-level logging can overwhelm the research. |
| Career alignment | 4 | The skills are valuable for distributed ML engineering. |
| Opportunity cost | 1 | It is less rational than continuing in the already frozen VLM field. |

Unweighted mean: 3.00/5. This mean is descriptive only; hard blockers remain controlling.

### Curated evidence for this dossier

[S05] McMahan et al.. Communication-Efficient Learning of Deep Networks from Decentralized Data. 2017. AISTATS paper, PMLR. [Official/primary link](https://proceedings.mlr.press/v54/mcmahan17a.html). Relevance: Foundational FedAvg paper defining iterative local training and server aggregation under decentralized data.

[S06] Caldas et al.. LEAF: A Benchmark for Federated Settings. 2018. arXiv paper and benchmark. [Official/primary link](https://arxiv.org/abs/1812.01097). Relevance: Provides federated datasets, evaluation, and reference implementations designed around realistic heterogeneity.

[S07] Talwalkar Lab. LEAF: A Benchmark for Federated Settings. 2018. Official repository. [Official/primary link](https://github.com/TalwalkarLab/leaf). Relevance: Shows the preprocessing and baseline infrastructure needed to construct federated partitions and run reference experiments.

[S08] Flower Labs. Run Simulations - Flower Framework. 2026. Official framework documentation. [Official/primary link](https://flower.ai/docs/framework/how-to-run-simulations.html). Relevance: Documents resource-aware client simulation and the CPU/GPU scheduling burden even when no real institutions participate.

### Direct verdict

| **Verdict element** | **Controlling statement** |
| --- | --- |
| Decision | Parked |
| Primary reason | Systems and methodological burden is high relative to fit with the frozen VLM direction. |
| Strongest blocker | A defensible client/data setting plus repeated training cannot yet be shown within the thesis budget. |
| What would change this decision | Natural client partitions, reproduced strong baselines, and a tested Colab pilot. |
| Present action | Preserve for later; do not federate a VLM during current discovery. |

## 8.3 Diffusion or Generative-Model Training as the Main Field

|  |
| --- |
| **CANONICAL STATUS** Parked. Canonical group: Diffusion or generative-model training. |

### A. What is this field?

Generative modeling learns a data distribution so a model can create new images, video, audio, text, or other samples. Diffusion models learn to reverse a noise process; GANs train a generator against a discriminator; autoregressive models predict the next token or patch; VAEs learn a probabilistic latent representation; flow models learn invertible or transport-based transformations.

Major subfields: Image and video synthesis; editing and controllable generation; personalization; compositional generation; inverse problems; data augmentation; safety and provenance; efficient sampling; generative evaluation.

Research versus implementation: A basic project fine-tunes Stable Diffusion or builds a prompt-to-image interface. Genuine research introduces or tests a new objective, architecture, control mechanism, data formulation, sampling method, or validated evaluation protocol against strong generators and human or task-grounded evidence.

### B. How does research in this field work?

* Data: large image-text pairs or domain-specific image collections with captions, filtering, rights, duplicates, and safety review.
* Preprocessing: resize/crop, caption cleaning, deduplication, latent caching, concept filtering, and data-quality auditing.
* Models: DDPM-style denoisers [S09], latent diffusion [S10], diffusion transformers, autoregressive image models, GANs, VAEs, or flows.
* Training: sample timesteps or tokens, optimize denoising/generation objectives, checkpoint large models, and run many validation generations; parameter-efficient adaptation reduces but does not remove cost.
* Baselines: pretrained generator, standard LoRA or DreamBooth, established control methods, and compute-matched ablations.
* Metrics: FID or distributional quality, CLIP-like alignment, compositional correctness, diversity, human preference, safety, and task-specific measures. GenEval shows why one holistic score is insufficient [S12].
* Compute: official Diffusers guidance says optimized text-to-image training targets a 24 GB GPU and larger GPUs are preferred for speed or batch size [S11].

### C. Why is this field valuable?

Generative models are scientifically influential and teach representation learning, large-model training, data curation, and multimodal evaluation. They looked attractive because their outputs are visible and current. Visibility is not evidence of a thesis contribution, and a polished generator demo can hide weak experimental science.

### D. Why is it parked for this researcher?

The following is a reasoned suitability judgment based on the cited technical evidence and the researcher profile.

**1. Hard blockers**

* Training frontier or foundation generative models from scratch is outside the canonical compute policy.
* The specification explicitly parks generative-model training as the main field and permits it only as a tool.

**2. Major risks**

* Fine-tuning is accessible, so many candidates collapse into a standard adapter recipe with no new research claim.
* Evaluation is expensive and partly subjective; automated metrics can miss compositional, safety, or diversity failures.
* Data licensing, deduplication, and caption quality can dominate the result.

**3. Manageable limitations**

* Small LoRA pilots, inference-only studies, and use of pretrained diffusion for augmentation may fit Colab.
* A narrow evaluation or reliability question can be measured without training a large generator.

**4. Opportunity-cost reasons**

* The active VLM lanes allow evaluation-centered research with much lower training cost.
* Chasing each new generator or framework would repeatedly reset the literature base.

### E. Why parked rather than permanently rejected?

Generative modeling remains valuable for a funded project, stronger GPU access, or a later method-focused thesis. It can also be a component in a VLM experiment without becoming the field identity.

### F. Can it appear inside the frozen VLM field?

Relationship classification: Compatible supporting method.

A pretrained diffusion model may generate controlled corruptions, counterfactual images, or synthetic shift conditions for a VLM reliability/generalization study. The thesis claim must concern the VLM behavior and must validate whether the synthetic intervention represents the intended condition.

### G. What would justify reconsideration?

* A precise gap can be tested primarily through inference or parameter-efficient training.
* A strong baseline and evaluation protocol, including human validation where needed, are reproduced.
* The full experiment fits a measured Colab GPU and storage budget across required seeds and ablations.
* The contribution is more than changing prompts, adapters, or datasets.

### Feasibility scorecard (1–5 decision aid)

| **Criterion** | **Score** | **One-sentence justification** |
| --- | --- | --- |
| Problem clarity | 4 | A narrow generation claim can be testable, but “better generation” is vague. |
| Dataset access | 3 | Public datasets exist, while rights, scale, captions, and deduplication remain difficult. |
| Baseline reproducibility | 3 | Open models and code exist, but exact training reproduction can be hardware-sensitive. |
| Compute feasibility | 2 | Full or repeated fine-tuning is a weak fit for Colab Pro; inference studies are better. |
| Evaluation validity | 2 | Human preference and automated scores often disagree or test only part of the claim. |
| Domain dependence | 4 | The work is mostly AI-centered, though application evaluation may need experts. |
| Contribution potential | 3 | Strong contributions exist, but the novelty bar is high and rapidly moving. |
| Scope control | 2 | Models, prompts, seeds, metrics, and ablations expand quickly. |
| Engineering burden | 2 | Data pipelines, checkpoints, and generation/evaluation cost are substantial. |
| Career alignment | 4 | Generative-model skills are relevant to modern AI engineering. |
| Opportunity cost | 1 | The VLM lanes offer stronger feasibility and continuity for the current thesis. |

Unweighted mean: 2.73/5. This mean is descriptive only; hard blockers remain controlling.

### Curated evidence for this dossier

[S09] Ho, Jain, and Abbeel. Denoising Diffusion Probabilistic Models. 2020. NeurIPS paper. [Official/primary link](https://proceedings.neurips.cc/paper/2020/hash/4c5bcfec8584af0d967f1ab10179ca4b-Abstract.html). Relevance: Foundational diffusion-model formulation based on iterative denoising.

[S10] Rombach et al.. High-Resolution Image Synthesis with Latent Diffusion Models. 2022. CVPR paper. [Official/primary link](https://openaccess.thecvf.com/content/CVPR2022/html/Rombach_High-Resolution_Image_Synthesis_With_Latent_Diffusion_Models_CVPR_2022_paper.html). Relevance: Representative modern architecture that reduces pixel-space cost by operating in a learned latent space.

[S11] Hugging Face. Text-to-image Training Guide. 2026. Official Diffusers documentation. [Official/primary link](https://huggingface.co/docs/diffusers/training/text2image). Relevance: States that even optimized text-to-image fine-tuning targets a 24 GB GPU, with larger GPUs preferred for higher batch sizes or speed.

[S12] Ghosh, Hajishirzi, and Schmidt. GenEval: An Object-Focused Framework for Evaluating Text-to-Image Alignment. 2023. arXiv paper and official repository. [Official/primary link](https://arxiv.org/abs/2310.11513). Relevance: Shows that generative evaluation requires fine-grained alignment tests, not only visual appeal or one aggregate score.

### Direct verdict

| **Verdict element** | **Controlling statement** |
| --- | --- |
| Decision | Parked |
| Primary reason | Compute and evaluation burden are disproportionate to an undergraduate thesis. |
| Strongest blocker | A publication-quality training and evaluation loop has not been shown to fit Colab Pro. |
| What would change this decision | An inference-first or PEFT contribution with validated metrics and a tested compute budget. |
| Present action | Use pretrained generation only as a controlled tool inside a named VLM lane. |

## 8.4 3D Vision

|  |
| --- |
| **CANONICAL STATUS** Parked. Canonical group: 3D, robotics, autonomous driving, specialized sensing. |

### A. What is this field?

3D vision reconstructs or understands geometry from point clouds, depth sensors, multiple images, video, or neural scene representations. It studies depth estimation, pose, reconstruction, 3D detection and segmentation, novel-view synthesis, scene graphs, and embodied spatial reasoning. Calibration maps measurements into a common coordinate system; registration aligns scans; a point cloud is a set of 3D samples; a mesh represents connected surfaces.

Major subfields: Multi-view geometry; RGB-D understanding; point-cloud learning; NeRF and Gaussian splatting; 3D detection/segmentation; pose estimation; SLAM; 3D generation and reconstruction.

Research versus implementation: A basic project runs a pretrained point-cloud model or reconstructs one scene. Genuine research defines a geometry or representation problem, respects calibration and coordinate systems, evaluates across scenes or sensors, compares with strong 3D baselines, and measures both geometric and semantic quality.

### B. How does research in this field work?

* Data: calibrated images, RGB-D sequences, point clouds, meshes, camera poses, and 3D labels. ScanNet and ScanNet++ show the multimodal capture and annotation complexity [S13, S14].
* Preprocessing: calibration, pose alignment, registration, voxelization or point sampling, coordinate normalization, visibility handling, and scene-level splitting.
* Models: PointNet-like point encoders, sparse 3D CNNs, voxel/BEV models, multi-view transformers, NeRFs, Gaussian splats, and image-depth fusion.
* Baselines: classical geometry, pretrained 3D networks, 2D-only controls, and representation-matched methods.
* Metrics: depth error, Chamfer distance, intersection-over-union, average precision, pose error, reconstruction quality, rendering PSNR/SSIM/LPIPS, and runtime/memory.
* Robustness: sensor noise, pose error, sparse views, missing depth, unseen scenes, scale changes, and cross-dataset transfer.
* Infrastructure: large scene files, custom CUDA/sparse libraries, visualization, coordinate debugging, and per-scene caching; the ScanNet++ toolkit exposes this engineering [S16].

### C. Why is this field valuable?

3D vision develops geometry, representation learning, perception, and high-value spatial AI skills. It looked attractive because it is visually impressive and central to robotics, AR/VR, and autonomy. The learning curve in geometry and tooling is materially larger than ordinary 2D or VLM evaluation.

### D. Why is it parked for this researcher?

The following is a reasoned suitability judgment based on the cited technical evidence and the researcher profile.

**1. Hard blockers**

* The canonical specification parks 3D because geometry and sensor requirements exceed the current scope.
* The researcher has no reliable robotics, geometry, or sensing supervisor and no local GPU for interactive 3D iteration.

**2. Major risks**

* Dataset storage, preprocessing, and custom operators can consume more time than the research question.
* Scene leakage or view-level random splits can invalidate generalization claims.
* Novelty often requires stronger 3D representation or reconstruction work, not a straightforward model swap.

**3. Manageable limitations**

* Small pretrained point-cloud or depth models can run on selected scenes in Colab.
* Public datasets and official toolkits exist.

**4. Opportunity-cost reasons**

* The active VLM lanes use the researcher’s current transformer and multimodal foundation more directly.
* Learning geometry, CUDA tooling, and scene processing now delays the baseline-first VLM funnel.

### E. Why parked rather than permanently rejected?

3D vision is suitable for later study with stronger compute, geometry mentorship, and a preprocessed benchmark. It is not permanently excluded from the researcher’s career.

### F. Can it appear inside the frozen VLM field?

Relationship classification: Compatible only after major narrowing.

A small 3D or depth cue could be an input condition in a VLM grounding study, but a thesis centered on reconstruction, SLAM, or 3D detection is directly outside the frozen scope.

### G. What would justify reconsideration?

* A small, preprocessed, legally accessible dataset and official baseline are verified.
* Required sparse/3D libraries run reliably in Colab and the pilot completes in one session.
* A geometry mentor can review preprocessing, metrics, and failure cases.
* The candidate’s primary claim remains VLM-centered or passes a formal field-change request.

### Feasibility scorecard (1–5 decision aid)

| **Criterion** | **Score** | **One-sentence justification** |
| --- | --- | --- |
| Problem clarity | 4 | Many 3D tasks are testable once the representation is fixed. |
| Dataset access | 3 | Public data exist but can be large, access-controlled, and preprocessing-heavy. |
| Baseline reproducibility | 3 | Code exists, though custom operators and dataset preparation are fragile. |
| Compute feasibility | 2 | Selected inference fits Colab, but training and scene sweeps are expensive. |
| Evaluation validity | 4 | Geometry and detection metrics are clear when calibration is correct. |
| Domain dependence | 2 | Unavailable geometry or sensing guidance creates a substantial validation risk. |
| Contribution potential | 3 | Novel representation contributions are possible but difficult at undergraduate scope. |
| Scope control | 2 | Data, models, scenes, and robustness settings make scope expansion likely. |
| Engineering burden | 2 | Coordinate systems, visualization, storage, and CUDA extensions add heavy overhead. |
| Career alignment | 3 | 3D skills are useful but less aligned than VLM reliability and systems evaluation. |
| Opportunity cost | 1 | The field change would sacrifice the strongest present fit for a steep new foundation. |

Unweighted mean: 2.64/5. This mean is descriptive only; hard blockers remain controlling.

### Curated evidence for this dossier

[S13] Dai et al.. ScanNet: Richly-Annotated 3D Reconstructions of Indoor Scenes. 2017. CVPR paper and official dataset. [Official/primary link](https://www.scan-net.org/). Relevance: Provides 2.5 million RGB-D views, camera poses, reconstructions, and semantic annotations across more than 1,500 scans.

[S14] Yeshwanth et al.. ScanNet++: A High-Fidelity Dataset of 3D Indoor Scenes. 2023. ICCV paper and official project. [Official/primary link](https://scannetpp.mlsg.cit.tum.de/scannetpp/). Relevance: Illustrates current 3D data complexity through laser scans, DSLR images, RGB-D streams, calibration, and semantic labels.

[S15] Geiger, Lenz, and Urtasun. Are We Ready for Autonomous Driving? The KITTI Vision Benchmark Suite. 2012. CVPR paper and official benchmark. [Official/primary link](https://www.cvlibs.net/datasets/kitti/). Relevance: Defines calibrated stereo, optical-flow, odometry, 3D detection, and tracking benchmarks collected from a sensor-equipped vehicle.

[S16] ScanNet++ authors. ScanNet++ Toolkit. 2023. Official repository. [Official/primary link](https://github.com/scannetpp/scannetpp). Relevance: Shows the practical calibration, undistortion, depth rendering, downscaling, storage, and evaluation tooling required for 3D experiments.

### Direct verdict

| **Verdict element** | **Controlling statement** |
| --- | --- |
| Decision | Parked |
| Primary reason | Geometry, preprocessing, and tooling add a new foundation that the current thesis does not need. |
| Strongest blocker | No demonstrated Colab-stable 3D baseline and no geometry supervision. |
| What would change this decision | A preprocessed benchmark, reproduced baseline, bounded claim, and geometry mentor. |
| Present action | Do not pursue as a parent field; allow only a tightly controlled VLM input condition. |

## 8.5 Robotics

|  |
| --- |
| **CANONICAL STATUS** Parked. Canonical group: 3D, robotics, autonomous driving, specialized sensing. |

### A. What is this field?

Robotics studies agents that perceive, plan, and act in a physical or simulated world. Learning-based robotics includes imitation learning, reinforcement learning, visuomotor policies, navigation, manipulation, sim-to-real transfer, and embodied language. Proprioception is the robot’s internal state; a policy maps observations to actions; sim-to-real is the gap between simulator success and physical performance.

Major subfields: Manipulation; navigation; robot perception; control; planning; imitation and reinforcement learning; human-robot interaction; embodied AI; multi-robot systems.

Research versus implementation: A basic project runs an existing policy in simulation. Genuine robotics research defines a task and control setting, compares against planning or learning baselines, reports success over many trials and seeds, analyzes safety and failure modes, and usually validates simulator assumptions or real-world transfer.

### B. How does research in this field work?

* Data: demonstrations, trajectories, RGB/RGB-D, robot state, actions, rewards, object models, and simulator scenes. RLBench supplies 100 tasks and multiple observation modalities [S17].
* Preprocessing: synchronize observations/actions, define controllers, normalize state, generate demonstrations, and create train/test object or task splits.
* Models: behavior cloning, diffusion policies, reinforcement learning, vision-language-action models, planning, or hybrid sense-plan-act systems.
* Experiments: train across tasks or objects, evaluate repeated rollouts, vary initial states, and test disturbances or unseen objects.
* Metrics: success rate, completion time, collisions, intervention count, path or grasp quality, sample efficiency, and sim-to-real performance.
* Baselines and ablations: scripted or classical controller, behavior cloning, state-only vs vision, task-specific vs multi-task, and controller/action-space variants.
* Infrastructure: physics simulation, rendering, assets, GPU policy training, large demonstrations, and sometimes real robots. ManiSkill2 and FurnitureBench expose this scale and the real-world gap [S18, S19].

### C. Why is this field valuable?

Robotics integrates AI with action and develops perception, control, systems, and evaluation skills. It is attractive because the demonstrations feel advanced and embodied. For this researcher, the absent hardware and control background are not small inconveniences; they remove the strongest route for validating physical claims.

### D. Why is it parked for this researcher?

The following is a reasoned suitability judgment based on the cited technical evidence and the researcher profile.

**1. Hard blockers**

* No robot, custom hardware, lab, sensors, or robotics/electronics supervisor is available.
* A simulation-only result cannot support a real-robot claim without carefully bounded language and transfer evidence.

**2. Major risks**

* Physics-engine setup, rendering, assets, controller design, and training instability can dominate the thesis.
* Repeated rollouts and multi-seed policy training are compute-intensive.
* A vision-language model connected to a simulator can become an integration demo rather than robotics research.

**3. Manageable limitations**

* Simulation-only imitation-learning pilots are technically possible.
* Open environments and demonstrations exist, including RLBench code [S20].

**4. Opportunity-cost reasons**

* All robotics foundation work would be new, while the active VLM field already matches current skills.
* A simulator setup does not advance the frozen VLM topic funnel unless the research question is explicitly VLM reliability in an embodied benchmark.

### E. Why parked rather than permanently rejected?

Robotics could become viable in a funded lab, master’s program, or industry collaboration with hardware and control mentorship. It remains a future field, not a present thesis priority.

### F. Can it appear inside the frozen VLM field?

Relationship classification: Compatible application context.

An embodied VLM benchmark could test instruction grounding or uncertainty in simulation, but it must remain inference/evaluation-centered and avoid claims about real robot deployment.

### G. What would justify reconsideration?

* A robotics lab provides hardware or a validated simulator protocol and ongoing supervision.
* A strong benchmark policy reproduces within a tested compute budget.
* The contribution can be evaluated through repeated executable success metrics without unsupported sim-to-real claims.
* A written change request shows why the VLM-only lanes are infeasible.

### Feasibility scorecard (1–5 decision aid)

| **Criterion** | **Score** | **One-sentence justification** |
| --- | --- | --- |
| Problem clarity | 4 | Robot tasks can be clear and executable. |
| Dataset access | 4 | Simulation datasets are public, but physical validation assets are unavailable. |
| Baseline reproducibility | 3 | Benchmark code exists but simulator versions and control stacks are fragile. |
| Compute feasibility | 2 | Policy training and repeated rollouts are costly for Colab sessions. |
| Evaluation validity | 4 | Success and safety metrics are direct when the task environment is valid. |
| Domain dependence | 1 | Robotics, control, and hardware supervision are unavailable. |
| Contribution potential | 3 | Meaningful contribution is possible but usually needs deeper control or embodied-learning expertise. |
| Scope control | 1 | The end-to-end stack is too broad for the team’s current foundation. |
| Engineering burden | 1 | Simulator, rendering, assets, controllers, and rollout management can overwhelm research. |
| Career alignment | 3 | Embodied AI is relevant but not the most direct career preparation under current resources. |
| Opportunity cost | 1 | The opportunity cost against frozen VLM work is severe. |

Unweighted mean: 2.45/5. This mean is descriptive only; hard blockers remain controlling.

### Curated evidence for this dossier

[S17] James et al.. RLBench: The Robot Learning Benchmark & Learning Environment. 2019. arXiv paper and official benchmark. [Official/primary link](https://arxiv.org/abs/1909.12271). Relevance: Defines 100 manipulation tasks with RGB, depth, masks, proprioception, and demonstration generation.

[S18] Gu et al.. ManiSkill2: A Unified Benchmark for Generalizable Manipulation Skills. 2023. arXiv paper and open benchmark. [Official/primary link](https://arxiv.org/abs/2302.04659). Relevance: Provides dynamic simulation, 20 task families, over 2,000 objects, and millions of demonstration frames, showing the experiment scale of modern robot learning.

[S19] Heo et al.. FurnitureBench: Reproducible Real-World Benchmark for Long-Horizon Complex Manipulation. 2023. arXiv paper and benchmark. [Official/primary link](https://arxiv.org/abs/2305.12821). Relevance: Demonstrates the gap between simulation and real robot evaluation and the physical setup required for long-horizon manipulation claims.

[S20] Stephen James et al.. RLBench Repository. 2019. Official repository. [Official/primary link](https://github.com/stepjam/RLBench). Relevance: Provides the simulator integration and code base needed to reproduce robot-learning baselines.

### Direct verdict

| **Verdict element** | **Controlling statement** |
| --- | --- |
| Decision | Parked |
| Primary reason | Unavailable hardware and robotics supervision make credible validation impractical. |
| Strongest blocker | No route to physical validation or expert review of the control setting. |
| What would change this decision | Lab access, robotics co-supervision, reproduced benchmark policy, and bounded evaluation. |
| Present action | Preserve for later; simulation may be used only as a VLM evaluation context. |

## 8.6 Autonomous-Driving Research

|  |
| --- |
| **CANONICAL STATUS** Parked. Canonical group: 3D, robotics, autonomous driving, specialized sensing. |

### A. What is this field?

Autonomous-driving research builds perception, prediction, planning, control, simulation, and safety systems for vehicles. Perception detects lanes, objects, occupancy, and geometry; prediction forecasts other agents; planning chooses a safe trajectory; control executes steering and acceleration. End-to-end driving maps sensor inputs more directly to actions.

Major subfields: Camera/lidar/radar perception; 3D detection; tracking; motion forecasting; mapping/localization; planning/control; simulation; end-to-end driving; safety validation.

Research versus implementation: A basic project trains a detector on road images. Genuine autonomous-driving research defines an operational design domain, uses calibrated multi-sensor or scenario data, compares strong perception/planning baselines, evaluates rare and safety-critical cases, and avoids claiming vehicle safety from one offline metric.

### B. How does research in this field work?

* Data: synchronized camera, lidar, radar, GPS/IMU, maps, 3D boxes, trajectories, and scenario metadata. nuScenes uses a full sensor suite [S21]; Waymo spans perception, motion, and end-to-end datasets [S22].
* Preprocessing: calibration, timestamp synchronization, coordinate transforms, sweeps, map alignment, tracking IDs, scenario slicing, and privacy/license compliance.
* Models: BEV fusion, 3D detectors, trackers, trajectory predictors, occupancy networks, planners, or end-to-end policies.
* Baselines: sensor-specific and fusion baselines, classical tracking/planning, leaderboard models, and simple constant-velocity or rule controls.
* Metrics: 3D mAP, translation/scale/orientation error, tracking scores, displacement error, collision/off-road rate, route completion, comfort, latency, and scenario coverage.
* Robustness: weather, night, sensor dropout, geographic shift, rare agents, calibration error, and closed-loop simulation.
* Infrastructure: terabyte-scale data, calibrated sensor libraries, GPU preprocessing, simulator operation, map tooling, and server-side evaluation. KITTI alone lists large modality downloads [S24].

### C. Why is this field valuable?

The field is high-impact and develops multimodal perception and safety systems skills. It is attractive because it combines vision, systems, and a socially visible application. Its industrial scale and safety context make it one of the weakest fits for the current thesis resources.

### D. Why is it parked for this researcher?

The following is a reasoned suitability judgment based on the cited technical evidence and the researcher profile.

**1. Hard blockers**

* No vehicle, sensor suite, driving simulator workstation, autonomy supervisor, or field-testing route is available.
* Safety or deployment claims cannot be supported by a small offline dataset experiment.

**2. Major risks**

* Large calibrated datasets and multi-sensor preprocessing exceed practical storage and iteration budgets.
* Open-loop perception gains may not improve closed-loop driving.
* Benchmark competition is mature, and small architecture substitutions are unlikely to be defensible novelty.

**3. Manageable limitations**

* A small camera-only perception or VLM evaluation slice can run on Colab.
* CARLA is open and supports controlled scenarios [S23], but simulator access does not erase validation complexity.

**4. Opportunity-cost reasons**

* The VLM lanes offer multimodal reliability research without full autonomy infrastructure.
* Entering autonomy would add geometry, sensors, simulation, safety, and control simultaneously.

### E. Why parked rather than permanently rejected?

Autonomous-driving research is appropriate for a funded lab or industry partnership with data infrastructure and safety expertise. It should remain parked for this undergraduate thesis.

### F. Can it appear inside the frozen VLM field?

Relationship classification: Compatible application context.

Road-scene VQA or VLM uncertainty under weather/sensor conflict may be used as a bounded VLM benchmark. Do not claim autonomous driving capability or safety.

### G. What would justify reconsideration?

* A lab provides preprocessed data, simulator infrastructure, and autonomy supervision.
* A baseline and closed-loop or deployment-relevant evaluation are reproduced.
* Data storage and compute are tested rather than estimated vaguely.
* The research claim remains narrow enough to avoid a perception-prediction-planning stack.

### Feasibility scorecard (1–5 decision aid)

| **Criterion** | **Score** | **One-sentence justification** |
| --- | --- | --- |
| Problem clarity | 3 | Subtasks are testable, but field-level safety questions are too broad. |
| Dataset access | 3 | Public datasets exist, yet scale, licenses, and preprocessing are substantial. |
| Baseline reproducibility | 2 | Strong baselines often assume multi-GPU systems and specialized libraries. |
| Compute feasibility | 1 | Full datasets, 3D models, and simulation are a poor Colab fit. |
| Evaluation validity | 3 | Offline metrics are clear but may not validate closed-loop safety claims. |
| Domain dependence | 1 | Autonomy, sensor, control, and safety expertise are unavailable. |
| Contribution potential | 3 | Contribution is possible but benchmark maturity raises the bar. |
| Scope control | 1 | Even one subsystem can expand into a large engineering program. |
| Engineering burden | 1 | Calibration, maps, sensor fusion, simulation, and storage are overwhelming. |
| Career alignment | 3 | Multimodal perception skills transfer, but the setup is disproportionate. |
| Opportunity cost | 1 | The active VLM lanes capture relevant skills at far lower cost. |

Unweighted mean: 2.00/5. This mean is descriptive only; hard blockers remain controlling.

### Curated evidence for this dossier

[S21] Caesar et al.. nuScenes: A Multimodal Dataset for Autonomous Driving. 2020. CVPR paper and official dataset. [Official/primary link](https://www.nuscenes.org/). Relevance: Combines six cameras, five radars, one lidar, maps, and 3D labels across 1,000 driving scenes.

[S22] Waymo. Waymo Open Dataset: About. 2026. Official dataset documentation. [Official/primary link](https://waymo.com/open/about/). Relevance: Documents perception, motion, and end-to-end datasets at a scale that creates substantial storage and preprocessing demands.

[S23] Dosovitskiy et al.. CARLA: An Open Urban Driving Simulator. 2017. CoRL paper, PMLR. [Official/primary link](https://proceedings.mlr.press/v78/dosovitskiy17a.html). Relevance: Provides controlled autonomous-driving simulation but requires scenario design, simulator operation, and careful transfer claims.

[S24] KITTI authors. KITTI 3D Object Detection Evaluation. 2026. Official benchmark page. [Official/primary link](https://www.cvlibs.net/datasets/kitti/eval_object.php?obj_benchmark=3d). Relevance: Lists data volumes, sensor modalities, labels, and server-side evaluation for a canonical driving-perception task.

### Direct verdict

| **Verdict element** | **Controlling statement** |
| --- | --- |
| Decision | Parked |
| Primary reason | The field requires industrial-scale data and safety-valid evaluation that the team cannot provide. |
| Strongest blocker | No credible closed-loop or domain-expert validation path. |
| What would change this decision | Autonomy lab partnership with preprocessed data, infrastructure, and evaluation support. |
| Present action | Do not pursue; use road scenes only as a bounded VLM test context. |

## 8.7 Specialized Sensing

|  |
| --- |
| **CANONICAL STATUS** Parked. Canonical group: 3D, robotics, autonomous driving, specialized sensing. |

### A. What is this field?

Specialized sensing develops perception from non-standard modalities such as lidar, radar, event cameras, thermal, hyperspectral, polarization, or single-photon sensors. These modalities measure different physical signals and require sensor-specific calibration, noise models, representations, and ground truth. Event cameras output brightness-change events rather than ordinary frames; hyperspectral images contain many wavelength bands; lidar returns 3D ranges.

Major subfields: Event vision; lidar point-cloud learning; radar perception; RGB-thermal fusion; hyperspectral classification; polarization imaging; sensor fusion; computational imaging.

Research versus implementation: A basic project converts a specialized modality to an image and applies a standard network. Genuine research respects the sensor physics and sampling process, compares modality-specific baselines, evaluates calibration/noise/fusion, and establishes why the new representation improves a physically meaningful outcome.

### B. How does research in this field work?

* Data: asynchronous events, point clouds, radar tensors, aligned RGB-thermal pairs, spectral cubes, calibration files, and synchronized ground truth.
* Preprocessing: decode proprietary/binary formats, synchronize modalities, calibrate extrinsics/intrinsics, compensate motion, voxelize or bin events, normalize bands, and manage missing data.
* Models: spiking or event encoders, sparse point networks, range-view CNNs, radar fusion, multispectral fusion, and spectral-spatial networks.
* Baselines: modality-only, frame/RGB-only, early/late fusion, classical signal processing, and sensor-specific published models.
* Metrics: task accuracy/mAP/IoU plus latency, temporal precision, calibration error, noise robustness, and modality contribution.
* Robustness: illumination, weather, motion, sparse returns, sensor dropout, timing offset, and cross-sensor transfer.
* Infrastructure: DSEC combines event, stereo, lidar, and GPS [S25]; the Prophesee event dataset is 200 GB compressed and 750 GB uncompressed [S28].

### C. Why is this field valuable?

The field can solve conditions where ordinary cameras fail and develops multimodal fusion, signal processing, and efficient perception skills. It looked attractive because it is technically distinctive and less generic. Distinctive hardware does not create feasibility when the researcher cannot inspect or reproduce the sensing process.

### D. Why is it parked for this researcher?

The following is a reasoned suitability judgment based on the cited technical evidence and the researcher profile.

**1. Hard blockers**

* No specialized sensors, hardware access, electronics background, or sensing supervisor is available.
* The canonical specification explicitly parks specialized sensing because sensor and infrastructure requirements exceed scope.

**2. Major risks**

* Published datasets may permit offline work but do not let the team validate calibration, collection artifacts, or new sensor claims.
* Data formats and storage can overwhelm the local 8 GB RAM environment.
* A standard CNN after format conversion is unlikely to be a strong contribution.

**3. Manageable limitations**

* Some preprocessed subsets and official APIs can support inference experiments.
* Public benchmarks such as SemanticKITTI and KAIST have defined metrics [S26, S27].

**4. Opportunity-cost reasons**

* The VLM parent field already provides multimodality without requiring new sensor physics.
* Learning sensor-specific pipelines offers less direct benefit to the current AI/ML and VLM research plan.

### E. Why parked rather than permanently rejected?

Specialized sensing can become viable in a lab that owns the sensor and can explain calibration, artifacts, and evaluation. It is rational to defer it.

### F. Can it appear inside the frozen VLM field?

Relationship classification: Compatible only after major narrowing.

Thermal, depth, or event-derived frames could appear in a VLM robustness study only if an accessible benchmark and validated preprocessing exist. The research claim must not depend on unverified sensor physics.

### G. What would justify reconsideration?

* A domain mentor and official, preprocessed dataset with calibration documentation are secured.
* The dataset subset fits local storage and Colab RAM/VRAM in a tested pilot.
* A modality-specific baseline is reproduced and its metric is understood.
* The contribution tests a clear VLM reliability/generalization claim rather than merely fusing modalities.

### Feasibility scorecard (1–5 decision aid)

| **Criterion** | **Score** | **One-sentence justification** |
| --- | --- | --- |
| Problem clarity | 4 | Sensor tasks can be precise after the modality is understood. |
| Dataset access | 3 | Public data exist, but files are often very large and specialized. |
| Baseline reproducibility | 3 | Official APIs and baselines exist for some modalities. |
| Compute feasibility | 2 | Data decoding and model training can exceed Colab storage and session limits. |
| Evaluation validity | 4 | Metrics are direct when calibration and ground truth are trustworthy. |
| Domain dependence | 1 | Sensor physics and electronics supervision are unavailable. |
| Contribution potential | 3 | Real contribution is possible but requires modality-specific insight. |
| Scope control | 2 | A narrow benchmark is possible, yet fusion quickly expands scope. |
| Engineering burden | 1 | Formats, synchronization, calibration, and storage create severe overhead. |
| Career alignment | 3 | Fusion skills are transferable but less direct than VLM work. |
| Opportunity cost | 1 | The parent-field change would buy hardware risk without a clear advantage. |

Unweighted mean: 2.45/5. This mean is descriptive only; hard blockers remain controlling.

### Curated evidence for this dossier

[S25] Gehrig et al.. DSEC: A Stereo Event Camera Dataset for Driving Scenarios. 2021. IEEE Robotics and Automation Letters paper and official dataset. [Official/primary link](https://dsec.ifi.uzh.ch/). Relevance: Shows event-camera research depends on synchronized event streams, stereo frames, lidar, GPS, and specialized representations.

[S26] Behley et al.. SemanticKITTI: A Dataset for Semantic Scene Understanding of LiDAR Sequences. 2019. ICCV paper and official benchmark. [Official/primary link](https://semantic-kitti.org/). Relevance: Provides dense point-wise LiDAR annotations and sequence-based evaluation for 3D semantic understanding.

[S27] Hwang et al.. Multispectral Pedestrian Detection: Benchmark Dataset and Baseline. 2015. CVPR paper and official project. [Official/primary link](https://soonminhwang.github.io/rgbt-ped-detection/). Relevance: Provides 95,000 aligned color-thermal pairs captured with specialized beam-splitter hardware.

[S28] Prophesee. GEN1 Automotive Detection Dataset. 2020. Official dataset and documentation. [Official/primary link](https://docs.prophesee.ai/stable/datasets.html). Relevance: Documents event-data formats and a 200 GB compressed, 750 GB uncompressed detection dataset, exposing the storage burden of specialized sensing.

### Direct verdict

| **Verdict element** | **Controlling statement** |
| --- | --- |
| Decision | Parked |
| Primary reason | Sensor-specific validation and infrastructure are unavailable. |
| Strongest blocker | No access to the sensing process or expert who can validate calibration and artifacts. |
| What would change this decision | Sensor-lab supervision plus a preprocessed, Colab-tested benchmark and baseline. |
| Present action | Do not pursue as a field; permit only validated modality inputs inside VLM work. |

## 8.8 Standalone Medical Imaging

|  |
| --- |
| **CANONICAL STATUS** Parked. Canonical group: Standalone medical imaging. |

### A. What is this field?

Medical imaging AI analyzes radiographs, CT, MRI, ultrasound, pathology slides, retinal images, or other clinical images for classification, detection, segmentation, reconstruction, registration, report generation, and prognosis. A reference standard is the label used as ground truth, often created by experts or clinical follow-up. External validation tests a different institution or population.

Major subfields: Computer-aided diagnosis; segmentation; radiomics; reconstruction; registration; multimodal image-report models; clinical decision support; generalization and fairness.

Research versus implementation: A basic project fine-tunes a CNN on a disease dataset and reports accuracy. Genuine research defines a clinically meaningful target, uses patient-level splits, understands label creation, evaluates calibration and subgroup/external performance, compares strong medical baselines, and avoids translating benchmark performance into unsupported clinical claims.

### B. How does research in this field work?

* Data: DICOM images, reports, clinical metadata, masks, pathology labels, and patient/study identifiers. MIMIC-CXR contains 377,110 images with reports [S29].
* Preprocessing: de-identification checks, DICOM windowing, view selection, patient-level splitting, label extraction, uncertainty handling, normalization, and leakage checks.
* Models: CNNs, vision transformers, U-Nets, detection networks, self-supervised encoders, and medical VLMs.
* Baselines: clinical rule or simple model, established CNN/ViT/U-Net, published medical baseline, and external-domain or subgroup controls.
* Metrics: sensitivity, specificity, AUROC/AUPRC, calibration, Dice/IoU, clinically relevant thresholds, subgroup results, and confidence intervals.
* Evaluation: expert reference standards, patient-level and temporal/external splits, error review, uncertainty, prevalence shift, and clinical-utility limits. CheXpert uses radiologist-labeled evaluation sets [S30].
* Governance: controlled access, data-use training, privacy, reporting, and explicit limitations; CLAIM 2024 defines transparent medical-imaging AI reporting expectations [S31, S32].

### C. Why is this field valuable?

Medical imaging can improve diagnosis and access and develops rigorous data, calibration, segmentation, and responsible-AI skills. It looked attractive because it is socially meaningful and has public datasets. Social value does not replace clinical validation, and public data do not make a researcher qualified to interpret medical errors.

### D. Why is it parked for this researcher?

The following is a reasoned suitability judgment based on the cited technical evidence and the researcher profile.

**1. Hard blockers**

* No reliable medical or radiology supervisor is available to validate labels, task meaning, or error analysis.
* The specification parks standalone medical imaging and allows medical images only as an application setting with public data and no unsupported clinical claims.

**2. Major risks**

* Dataset labels may come from reports, billing codes, or weak extraction rather than definitive diagnosis.
* Single-site random splits can exaggerate generalization.
* A standard transfer-learning classifier is saturated and unlikely to add contribution.

**3. Manageable limitations**

* Public controlled-access datasets and medical-imaging frameworks exist.
* Inference, PEFT, or small segmentation/classification baselines may fit Colab.

**4. Opportunity-cost reasons**

* VLM trustworthiness can use medical images only as a bounded test setting while keeping the claim about model reliability.
* Standalone medical work adds domain study and validation risk that do not improve the core VLM method.

### E. Why parked rather than permanently rejected?

The field remains valuable for a later collaboration with a clinician, a funded health-AI lab, or graduate study. The present team should not claim clinical significance it cannot verify.

### F. Can it appear inside the frozen VLM field?

Relationship classification: Compatible application context.

A public chest-X-ray VQA benchmark could test VLM hallucination or calibration, provided the team states that it is a benchmark study, validates labels, and makes no diagnostic or deployment claim.

### G. What would justify reconsideration?

* A clinician or medical-imaging researcher agrees to review the question, labels, metrics, and errors.
* The dataset’s access terms, patient-level splits, and reference standard are verified.
* A strong baseline is reproduced and external or cross-source evaluation is feasible.
* Human expert annotation is not required beyond available supervision and the contribution remains measurable.

### Feasibility scorecard (1–5 decision aid)

| **Criterion** | **Score** | **One-sentence justification** |
| --- | --- | --- |
| Problem clarity | 4 | Medical tasks can be specific, but clinical meaning must be defined correctly. |
| Dataset access | 4 | Large public or controlled-access datasets exist. |
| Baseline reproducibility | 4 | Many strong baselines are open and reproducible on subsets. |
| Compute feasibility | 3 | Small or PEFT experiments fit Colab; full-resolution 3D work may not. |
| Evaluation validity | 3 | Metrics are established, yet clinical validity depends on reference standards and external testing. |
| Domain dependence | 1 | Unavailable clinical supervision is a hard present gate. |
| Contribution potential | 3 | Contribution is possible through reliability/generalization, but generic diagnosis models are crowded. |
| Scope control | 3 | A narrow public benchmark can be controlled. |
| Engineering burden | 3 | DICOM, labels, patient splits, and governance add moderate burden. |
| Career alignment | 4 | Responsible health-AI work has strong research value. |
| Opportunity cost | 2 | A VLM reliability study offers similar skills with less domain risk. |

Unweighted mean: 3.09/5. This mean is descriptive only; hard blockers remain controlling.

### Curated evidence for this dossier

[S29] Johnson et al.. MIMIC-CXR Database v2.1.0. 2024. PhysioNet official dataset. [Official/primary link](https://physionet.org/content/mimic-cxr/). Relevance: Provides 377,110 de-identified radiographs with reports under controlled-access requirements.

[S30] Irvin et al.. CheXpert: A Large Chest Radiograph Dataset with Uncertainty Labels and Expert Comparison. 2019. AAAI paper and official dataset. [Official/primary link](https://stanfordmlgroup.github.io/competitions/chexpert/). Relevance: Shows that high-quality evaluation uses uncertainty labels and radiologist-annotated reference sets.

[S31] Tejani et al.. Checklist for Artificial Intelligence in Medical Imaging: 2024 Update. 2024. Radiology: Artificial Intelligence guideline. [Official/primary link](https://pubs.rsna.org/doi/abs/10.1148/ryai.240300). Relevance: Defines reporting expectations for medical-imaging AI, including data, reference standards, evaluation, and limitations.

[S32] RSNA. Checklist for Artificial Intelligence in Medical Imaging (CLAIM). 2024. Official guideline page. [Official/primary link](https://pubs.rsna.org/page/ai/claim). Relevance: Confirms that classification, segmentation, and reconstruction studies need domain-appropriate transparent reporting.

### Direct verdict

| **Verdict element** | **Controlling statement** |
| --- | --- |
| Decision | Parked |
| Primary reason | Clinical validation and error interpretation cannot be defended without a domain expert. |
| Strongest blocker | No reliable medical supervisor to validate the problem and reference standard. |
| What would change this decision | Named clinical supervision plus verified patient-level data, baseline, and evaluation. |
| Present action | Use only as a public-data VLM application context with no clinical claim. |

## 8.9 Standalone Explainable AI (XAI)

|  |
| --- |
| **CANONICAL STATUS** Parked. Canonical group: Standalone XAI. |

### A. What is this field?

Explainable AI studies methods that make model behavior understandable to people. Local explanations describe one prediction; global explanations summarize a model; feature attribution assigns importance to inputs; concept methods use human-meaningful factors; counterfactuals describe changes that would alter an output; mechanistic interpretability studies internal computations.

Major subfields: Feature attribution; surrogate models; concept-based explanations; counterfactual explanations; example-based explanations; mechanistic interpretability; explanation evaluation; human-centered interpretability.

Research versus implementation: A basic project runs SHAP, LIME, or Grad-CAM and displays heatmaps. Genuine research defines who needs the explanation and for what decision, measures faithfulness and stability, uses sanity checks or task-grounded human evaluation, compares strong explanation baselines, and distinguishes explanation plausibility from causal evidence.

### B. How does research in this field work?

* Inputs: trained models, selected instances, concepts/features, perturbation distributions, and sometimes human tasks or expert annotations.
* Methods: local surrogates such as LIME [S33], additive feature attributions such as SHAP [S34], gradients, attention analysis, concept probes, counterfactual search, and causal interventions.
* Baselines: random attribution, gradients, integrated gradients, perturbation methods, simple probes, and task-specific evidence maps.
* Metrics: faithfulness or deletion/insertion tests, sensitivity, stability, localization, sparsity, completeness, human task performance, and computation cost.
* Validity tests: parameter/data randomization, input invariance, adversarial manipulation, explanation consistency, and model-behavior interventions. Saliency sanity checks show why visual appeal is not enough [S35].
* Ablations: explanation hyperparameters, baselines/reference inputs, layer choice, model family, and alternative ground truths.
* Reproducibility: pin model, input transforms, background distribution, perturbation process, and explanation implementation; Captum makes methods easy to run but does not validate their meaning [S37].

### C. Why is this field valuable?

XAI aims to support debugging, auditing, scientific discovery, and human decisions. It aligns strongly with trustworthy AI and teaches careful measurement. It looked attractive because visual explanations are intuitive, but intuition creates a trap: a heatmap that looks sensible can be independent of the learned model.

### D. Why is it parked for this researcher?

The following is a reasoned suitability judgment based on the cited technical evidence and the researcher profile.

**1. Hard blockers**

* The canonical specification explicitly parks standalone XAI because evaluation is often weak or subjective.
* An explanation without a defined user, purpose, and validity test cannot support a research claim.

**2. Major risks**

* Ground truth for “correct explanation” is often absent.
* Applying existing libraries produces an implementation, not a contribution.
* Human studies add protocol, recruitment, ethics, and statistical burden.

**3. Manageable limitations**

* Most explanation methods are inference-only and Colab-feasible.
* A measurable faithfulness or reliability question can be integrated into VLM research.

**4. Opportunity-cost reasons**

* XAI is most valuable here as an instrument for the primary trustworthiness lane, not a competing parent field.
* A standalone XAI literature review would duplicate effort without improving the frozen field decision.

### E. Why parked rather than permanently rejected?

The methods remain scientifically useful and may be central to a later interpretability-focused project with a validated task and evaluation protocol. For the current thesis, XAI must serve a VLM claim.

### F. Can it appear inside the frozen VLM field?

Relationship classification: Compatible supporting method.

Use visual evidence attribution, concept probes, attention intervention, or counterfactual images to test whether a VLM’s answer is grounded. The primary outcome must be reliability or generalization, not the production of an attractive explanation.

### G. What would justify reconsideration?

* A target user and decision are defined.
* A faithfulness or task-grounded evaluation with validated controls is available.
* At least two strong explanation baselines and randomization controls are reproduced.
* The new contribution changes what can be measured or improves a directly tested VLM reliability outcome.

### Feasibility scorecard (1–5 decision aid)

| **Criterion** | **Score** | **One-sentence justification** |
| --- | --- | --- |
| Problem clarity | 4 | A precise explanation-validity question can be formulated. |
| Dataset access | 5 | Models and benchmark data are readily accessible. |
| Baseline reproducibility | 5 | LIME, SHAP, Captum, and saliency baselines are easy to reproduce. |
| Compute feasibility | 5 | Most experiments are inference-only and fit Colab. |
| Evaluation validity | 2 | The central weakness is the lack of universally valid explanation ground truth. |
| Domain dependence | 4 | Generic XAI is AI-centered, though user studies may need domain participants. |
| Contribution potential | 3 | Contribution exists in evaluation or interventions, not routine heatmaps. |
| Scope control | 4 | A narrow method-and-metric study can be controlled. |
| Engineering burden | 4 | Library use is light, but human evaluation can become heavy. |
| Career alignment | 5 | Interpretability supports trustworthy-AI research and engineering. |
| Opportunity cost | 3 | It is better used inside Rank 1 than reopened as a parent field. |

Unweighted mean: 4.00/5. This mean is descriptive only; hard blockers remain controlling.

### Curated evidence for this dossier

[S33] Ribeiro, Singh, and Guestrin. Why Should I Trust You? Explaining the Predictions of Any Classifier. 2016. KDD paper. [Official/primary link](https://arxiv.org/abs/1602.04938). Relevance: Introduces LIME and illustrates local surrogate explanations and human-centered evaluation.

[S34] Lundberg and Lee. A Unified Approach to Interpreting Model Predictions. 2017. NeurIPS paper. [Official/primary link](https://arxiv.org/abs/1705.07874). Relevance: Introduces SHAP and formalizes additive feature-attribution methods.

[S35] Adebayo et al.. Sanity Checks for Saliency Maps. 2018. NeurIPS paper. [Official/primary link](https://papers.nips.cc/paper/8160-sanity-checks-for-saliency-maps). Relevance: Demonstrates that visually plausible explanations can fail model- and data-randomization tests.

[S36] Doshi-Velez and Kim. Towards a Rigorous Science of Interpretable Machine Learning. 2017. arXiv position paper. [Official/primary link](https://arxiv.org/abs/1702.08608). Relevance: Explains why interpretability needs a defined user, task, and evaluation rather than an attractive visualization alone.

[S37] Meta PyTorch. Captum: Model Interpretability for PyTorch. 2026. Official framework documentation. [Official/primary link](https://captum.ai/). Relevance: Shows that applying attribution algorithms is easy; the research challenge lies in validating what the explanations mean.

### Direct verdict

| **Verdict element** | **Controlling statement** |
| --- | --- |
| Decision | Parked |
| Primary reason | Evaluation validity is too weak for standalone XAI under present conditions. |
| Strongest blocker | No direct, validated ground truth for the intended explanation claim. |
| What would change this decision | A task-grounded faithfulness protocol with controls and a clear user. |
| Present action | Use only within Trustworthy and Reliable VLMs for a named, measurable claim. |

## 8.10 Generic RAG Applications

|  |
| --- |
| **CANONICAL STATUS** Parked. Canonical group: Generic RAG or agent application. |

### A. What is this field?

Retrieval-augmented generation (RAG) retrieves external documents or passages and conditions a generator on them. A retriever finds candidates; a reranker reorders them; a generator answers; provenance links the answer to evidence. RAG research covers retrieval, indexing, query formulation, grounding, long context, multimodal retrieval, freshness, and evaluation.

Major subfields: Sparse/dense/hybrid retrieval; reranking; knowledge-intensive QA; grounded generation; adaptive retrieval; multimodal RAG; retrieval robustness; RAG evaluation and systems efficiency.

Research versus implementation: A basic project loads PDFs into a vector database and connects an LLM. Genuine research defines a retrieval or grounded-generation failure, compares BM25/dense/hybrid and no-retrieval controls, evaluates provenance and answer correctness separately, controls corpus/split leakage, and establishes a new method, protocol, or systematic result.

### B. How does research in this field work?

* Data: a document corpus, queries, relevance judgments, answers, and evidence spans. KILT evaluates both downstream outputs and provenance [S40].
* Preprocessing: parse documents, preserve metadata, chunk and deduplicate, build sparse/dense indexes, and create leakage-safe query/corpus splits.
* Models: BM25, dense encoders, late interaction, rerankers, seq2seq or instruction models, query routers, and retrieval planners.
* Baselines: no retrieval, BM25, dense retrieval, hybrid retrieval, oracle evidence, and prompt/context-matched generator controls.
* Metrics: Recall@k, nDCG, MRR, answer EM/F1, citation precision/recall, faithfulness, completeness, latency, and cost. BEIR supports heterogeneous retrieval evaluation [S39].
* Diagnostics: retrieval failure vs generation failure, irrelevant context, contradictory evidence, chunking, context order, and query shift. RAGChecker explicitly separates these modules [S41].
* Reproducibility: pin corpus snapshot, parser, chunking, embedding model, index, prompts, model revision, and judge; the original RAG paper is a model contribution, not a vector-database tutorial [S38].

### C. Why is this field valuable?

RAG is important for factuality, provenance, updating knowledge, and production AI systems. It develops retrieval, data-pipeline, evaluation, and serving skills. It looked attractive because frameworks make a usable demo quickly. That ease is precisely why a generic application has almost no research identity.

### D. Why is it parked for this researcher?

The following is a reasoned suitability judgment based on the cited technical evidence and the researcher profile.

**1. Hard blockers**

* The canonical specification says a working RAG system alone is an engineering project, not a research contribution.
* Generic text RAG is outside the frozen VLM parent field unless retrieval is necessary to test a multimodal claim.

**2. Major risks**

* Framework defaults can hide weak retrieval, leakage, and unvalidated LLM judges.
* The contribution can collapse into chunk-size, embedding, or prompt comparisons.
* Paid proprietary LLM dependence undermines reproducibility and budget constraints.

**3. Manageable limitations**

* Open retrievers and smaller generators can support baseline experiments.
* Retrieval metrics are computationally manageable when the corpus is bounded.

**4. Opportunity-cost reasons**

* The active VLM lanes already require rigorous evaluation; adding RAG without necessity creates a second system to debug.
* Building a polished assistant would consume time better spent reproducing a VLM baseline and measuring a real failure.

### E. Why parked rather than permanently rejected?

RAG remains valuable for engineering projects and later retrieval research. It can be used in a thesis only where the retrieval mechanism is scientifically necessary and directly evaluated.

### F. Can it appear inside the frozen VLM field?

Relationship classification: Compatible supporting method.

Use image-text or document retrieval to test whether a VLM remains reliable under missing, degraded, contradictory, or shifted evidence. Retrieval must have its own baselines and metrics but remain subordinate to the VLM question.

### G. What would justify reconsideration?

* A precise retrieval or grounding failure is verified in recent primary literature.
* A public corpus, queries, relevance labels, and provenance evaluation are available.
* BM25, dense, no-retrieval, and oracle controls are reproduced.
* The contribution is not framework integration and does not depend on a paid model judge.

### Feasibility scorecard (1–5 decision aid)

| **Criterion** | **Score** | **One-sentence justification** |
| --- | --- | --- |
| Problem clarity | 4 | A retrieval or grounding failure can be formulated precisely. |
| Dataset access | 4 | Many public corpora and benchmarks exist, though domain corpora may have licensing issues. |
| Baseline reproducibility | 5 | BM25, dense retrieval, and RAG baselines are open and reproducible. |
| Compute feasibility | 4 | Bounded corpora and small models fit Colab; large indexes or generators may not. |
| Evaluation validity | 3 | Retrieval metrics are clear, while long-form answer faithfulness remains harder. |
| Domain dependence | 5 | The work is AI/CSE-centered with low external-domain dependence. |
| Contribution potential | 2 | Generic applications have very low novelty; method or evaluation work is required. |
| Scope control | 4 | A narrow corpus and claim can be controlled. |
| Engineering burden | 3 | Parsing, indexing, retrieval, generation, and evaluation create a moderate stack. |
| Career alignment | 5 | RAG engineering skills are highly transferable. |
| Opportunity cost | 2 | It should support a VLM claim, not compete with the frozen field. |

Unweighted mean: 3.73/5. This mean is descriptive only; hard blockers remain controlling.

### Curated evidence for this dossier

[S38] Lewis et al.. Retrieval-Augmented Generation for Knowledge-Intensive NLP Tasks. 2020. NeurIPS paper. [Official/primary link](https://proceedings.neurips.cc/paper/2020/hash/6b493230205f780e1bc26945df7481e5-Abstract.html). Relevance: Foundational RAG work combining parametric generation with non-parametric retrieval.

[S39] Thakur et al.. BEIR: A Heterogeneous Benchmark for Zero-shot Evaluation of Information Retrieval Models. 2021. NeurIPS Datasets and Benchmarks paper. [Official/primary link](https://datasets-benchmarks-proceedings.neurips.cc/paper/2021/hash/65b9eea6e1cc6bb9f0cd2a47751a186f-Abstract-round2.html). Relevance: Provides 18 retrieval datasets and shows why retrieval must be evaluated across heterogeneous tasks.

[S40] Petroni et al.. KILT: A Benchmark for Knowledge Intensive Language Tasks. 2021. NAACL paper and official repository. [Official/primary link](https://aclanthology.org/2021.naacl-main.200/). Relevance: Requires both downstream-task performance and evidence provenance, not answer fluency alone.

[S41] Ru et al.. RAGChecker: A Fine-grained Framework for Diagnosing Retrieval-Augmented Generation. 2024. NeurIPS paper and official repository. [Official/primary link](https://github.com/amazon-science/RAGChecker). Relevance: Separates retrieval and generation diagnostics and validates metrics against human judgments.

### Direct verdict

| **Verdict element** | **Controlling statement** |
| --- | --- |
| Decision | Parked |
| Primary reason | Generic RAG is an engineering pattern, not a research field or contribution. |
| Strongest blocker | No independently testable gap beyond assembling existing components. |
| What would change this decision | A verified multimodal retrieval failure, public benchmark, strong controls, and direct evaluation. |
| Present action | Use only if necessary for a named VLM research question. |

## 8.11 Generic Agentic-AI Applications

|  |
| --- |
| **CANONICAL STATUS** Parked. Canonical group: Generic RAG or agent application. |

### A. What is this field?

Agentic AI uses a model to choose actions, call tools, observe results, update plans, and continue toward a goal. Components can include planning, memory, retrieval, tool APIs, execution environments, reflection, and multi-agent coordination. An agent benchmark evaluates end-to-end task success, not only whether the model produced a plausible plan.

Major subfields: Tool use; web and software agents; planning and search; memory; self-correction; multi-agent systems; embodied agents; safety and evaluation.

Research versus implementation: A basic project wires an LLM to tools with LangChain or another framework. Genuine research defines a reproducible environment and task distribution, compares against non-agent and simpler-agent baselines, measures executable success, controls tool/API changes, and isolates the mechanism through ablation.

### B. How does research in this field work?

* Data/environment: tasks, tool schemas, executable websites or repositories, initial state, success conditions, and action logs.
* Architecture: observe, reason/plan, act, receive feedback, update memory, and stop. ReAct is a foundational reasoning-and-action pattern [S42].
* Baselines: direct prompting, fixed workflow, retrieval-only, ReAct, planning/search, and tool-ablation controls.
* Metrics: exact task success, steps, invalid actions, recovery rate, latency, token/API cost, safety violations, and reproducibility across runs.
* Evaluation: deterministic environments, hidden tests, repeated stochastic runs, task difficulty, contamination checks, and model-version control. WebArena and SWE-bench use executable outcomes [S44, S45].
* Ablations: memory, reflection, tool set, planner, search depth, retries, and prompt/model.
* Infrastructure: containers or web services, tool mocks, state resets, long traces, rate limits, failures, and expensive repeated inference. AgentBench spans eight distinct environments [S43].

### C. Why is this field valuable?

Agent research matters for dependable automation and teaches orchestration, evaluation, software systems, and model behavior. It looked attractive because agents are modern and demos feel powerful. Framework ease lowers implementation cost but does not supply a research question or valid benchmark.

### D. Why is it parked for this researcher?

The following is a reasoned suitability judgment based on the cited technical evidence and the researcher profile.

**1. Hard blockers**

* The canonical specification parks generic agent applications because a working system alone is not a contribution.
* Strong agent evaluation often depends on paid frontier APIs or substantial open-model inference, conflicting with the no-paid-primary-result rule.

**2. Major risks**

* Model/API updates, nondeterminism, website changes, and environment failures can make results irreproducible.
* “More agents,” memory, or reflection can be superficial unless isolated against simpler controls.
* Benchmark contamination and hidden engineering heuristics can distort the measured capability.

**3. Manageable limitations**

* Small tool-use environments and open models can support pilot studies.
* Executable success metrics can be strong when the environment is stable.

**4. Opportunity-cost reasons**

* Building and maintaining an agent environment would displace VLM failure measurement and baseline work.
* A VLM thesis can study multimodal tool-use reliability only if the agent layer is minimal and necessary.

### E. Why parked rather than permanently rejected?

Agent research may be suitable later with stable environments, sufficient inference resources, and a validated benchmark. Generic workflow automation should remain an engineering portfolio project, not the thesis.

### F. Can it appear inside the frozen VLM field?

Relationship classification: Compatible only after major narrowing.

A multimodal agent could be used to test whether visual misperception propagates into tool actions, but the research claim must be about VLM reliability and the environment must provide exact success/failure labels.

### G. What would justify reconsideration?

* A fully reproducible executable benchmark with resets and hidden tests is available.
* A no-agent or fixed-workflow baseline and a recognized agent baseline are reproduced.
* Open-model inference fits a measured budget across repeated runs.
* A single mechanism is isolated and the result is not merely a framework comparison.

### Feasibility scorecard (1–5 decision aid)

| **Criterion** | **Score** | **One-sentence justification** |
| --- | --- | --- |
| Problem clarity | 4 | Executable agent tasks can be precise. |
| Dataset access | 4 | Public benchmarks exist, though environment setup and licensing vary. |
| Baseline reproducibility | 3 | Reference code exists but can be brittle and model-version dependent. |
| Compute feasibility | 2 | Repeated long-context inference or frontier APIs are costly. |
| Evaluation validity | 4 | Exact task success is valid when environments and tests are stable. |
| Domain dependence | 5 | The work is AI/CSE-centered and needs little external domain supervision. |
| Contribution potential | 2 | Generic orchestration has weak novelty; benchmark or algorithm contributions are needed. |
| Scope control | 3 | A small environment can be bounded, but tool and memory scope expands easily. |
| Engineering burden | 2 | Containers, services, state reset, traces, and failures create heavy engineering. |
| Career alignment | 5 | Agent evaluation and orchestration are valuable industry skills. |
| Opportunity cost | 2 | The active VLM lanes are more feasible and already frozen. |

Unweighted mean: 3.27/5. This mean is descriptive only; hard blockers remain controlling.

### Curated evidence for this dossier

[S42] Yao et al.. ReAct: Synergizing Reasoning and Acting in Language Models. 2023. ICLR paper. [Official/primary link](https://openreview.net/forum?id=WE_vluYUL-X). Relevance: Foundational agent pattern that interleaves reasoning traces with environment actions.

[S43] Liu et al.. AgentBench: Evaluating LLMs as Agents. 2024. ICLR paper. [Official/primary link](https://openreview.net/forum?id=zAdUB0aCTQ). Relevance: Evaluates agents across eight environments and identifies long-horizon reasoning and instruction-following failures.

[S44] Zhou et al.. WebArena: A Realistic Web Environment for Building Autonomous Agents. 2024. ICLR paper. [Official/primary link](https://openreview.net/forum?id=oKn9c6ytLx). Relevance: Shows that realistic web-agent evaluation needs reproducible websites, executable actions, and end-to-end task success.

[S45] Jimenez et al.. SWE-bench: Can Language Models Resolve Real-World GitHub Issues?. 2024. ICLR paper and benchmark. [Official/primary link](https://openreview.net/forum?id=VTF8yNQM66). Relevance: Uses executable repository tests to evaluate agents, illustrating the infrastructure and contamination risks of agent benchmarks.

### Direct verdict

| **Verdict element** | **Controlling statement** |
| --- | --- |
| Decision | Parked |
| Primary reason | Framework integration is easy, while rigorous, reproducible agent evaluation is expensive. |
| Strongest blocker | No stable, low-cost executable benchmark that isolates a new scientific mechanism. |
| What would change this decision | Reproducible environment, open-model budget, strong baselines, and one isolated contribution. |
| Present action | Do not build a generic agent thesis; use only a minimal agent layer for a VLM reliability question. |

## 8.12 Generic Image Classification

|  |
| --- |
| **CANONICAL STATUS** Parked. Canonical group: Generic image classification or detection. |

### A. What is this field?

Image classification maps an image to one or more labels. Single-label classification chooses one class; multi-label classification predicts multiple attributes; fine-grained classification distinguishes similar categories; open-set recognition handles unknown classes. The field also studies representations, imbalance, robustness, calibration, and distribution shift.

Major subfields: Supervised and self-supervised representation learning; long-tail and fine-grained recognition; open-set/OOD detection; calibration; robustness; few-shot learning; domain generalization.

Research versus implementation: A basic project fine-tunes ResNet or ViT on a custom dataset and reports accuracy. Genuine research changes representation or optimization, constructs and validates a benchmark, or studies a defensible failure such as shift, imbalance, uncertainty, spurious correlation, or efficiency with strong controls.

### B. How does research in this field work?

* Data: labeled images, class taxonomy, patient/source/group identifiers, and sometimes unlabeled pretraining data.
* Preprocessing: deduplication, source-aware splitting, resizing, augmentation, class balancing, and leakage checks.
* Models: CNNs such as ResNet [S47], vision transformers, self-supervised encoders, linear probes, and lightweight networks.
* Baselines: majority/classical baseline, pretrained ResNet/ViT, simple augmentation, frozen-feature linear probe, and closest published method.
* Metrics: accuracy, macro-F1, balanced accuracy, per-class recall, calibration, worst-group performance, OOD degradation, and efficiency as appropriate.
* Ablations: pretraining, augmentations, class balance, loss, backbone size, source split, and random seeds.
* Research standard: ImageNet shaped large-scale recognition [S46], while WILDS shows how classification remains valuable when the question concerns real distribution shift [S48].

### C. Why is this field valuable?

Classification is foundational, easy to prototype, and useful for learning experiment design. It looked attractive because datasets and models are abundant and Colab-friendly. Those advantages also make “model X on dataset Y” one of the most saturated and weakest thesis patterns.

### D. Why is it parked for this researcher?

The following is a reasoned suitability judgment based on the cited technical evidence and the researcher profile.

**1. Hard blockers**

* The canonical specification parks generic classification unless the claim concerns reliability, shift, efficiency, or another defensible problem.
* A new application dataset and small accuracy gain are not enough to satisfy the canonical contribution gate.

**2. Major risks**

* Random splits can leak sources or duplicates.
* Benchmark chasing encourages weak architecture swaps and hyperparameter advantages.
* Small datasets produce unstable gains and underpowered conclusions.

**3. Manageable limitations**

* Baseline reproduction and multi-seed experiments are usually Colab-feasible.
* Evaluation metrics and public implementations are mature.

**4. Opportunity-cost reasons**

* Classification can be a task within a VLM reliability/generalization experiment without becoming the parent field.
* Standalone classification uses thesis capacity on a lower-novelty identity than the frozen VLM lanes.

### E. Why parked rather than permanently rejected?

Classification remains useful as a method, baseline, or task. It can be reconsidered only when the actual contribution is a rigorous reliability, shift, efficiency, or dataset problem, at which point the thesis identity should be named after that problem rather than “classification.”

### F. Can it appear inside the frozen VLM field?

Relationship classification: Compatible supporting method.

Image classification may provide a visual-only baseline, an AI-generated image detector, or a corruption/shift probe inside Rank 1, 2, or 3. The comparison must answer the VLM question.

### G. What would justify reconsideration?

* A non-generic failure condition is verified and cannot be answered by existing VLM lanes.
* Source-aware splits and sufficient sample size are confirmed.
* Strong pretrained baselines reproduce with multiple seeds.
* The contribution survives comparison against a simple representation or augmentation baseline.

### Feasibility scorecard (1–5 decision aid)

| **Criterion** | **Score** | **One-sentence justification** |
| --- | --- | --- |
| Problem clarity | 5 | Classification questions and labels are easy to define. |
| Dataset access | 5 | Many public datasets are accessible. |
| Baseline reproducibility | 5 | Pretrained baselines and mature libraries make reproduction straightforward. |
| Compute feasibility | 5 | Most bounded experiments fit Colab comfortably. |
| Evaluation validity | 5 | Metrics are direct, with known extensions for imbalance, shift, and calibration. |
| Domain dependence | 5 | Generic classification is AI-centered and needs little domain supervision unless the labels are specialized. |
| Contribution potential | 2 | The contribution ceiling is low for a routine transfer-learning study. |
| Scope control | 5 | The task can be tightly bounded. |
| Engineering burden | 5 | Engineering overhead is low. |
| Career alignment | 4 | Core modeling skills are useful, though the signal is less modern than VLM research. |
| Opportunity cost | 2 | It is rational only as a supporting task, not a replacement field. |

Unweighted mean: 4.36/5. This mean is descriptive only; hard blockers remain controlling.

### Curated evidence for this dossier

[S46] Russakovsky et al.. ImageNet Large Scale Visual Recognition Challenge. 2015. International Journal of Computer Vision paper. [Official/primary link](https://arxiv.org/abs/1409.0575). Relevance: Defines the large-scale classification and detection benchmark that shaped modern visual recognition.

[S47] He et al.. Deep Residual Learning for Image Recognition. 2016. CVPR paper and official models. [Official/primary link](https://arxiv.org/abs/1512.03385). Relevance: Representative architecture contribution showing that genuine classification research changes optimization or representation, not only the application dataset.

[S48] Koh et al.. WILDS: A Benchmark of in-the-Wild Distribution Shifts. 2021. ICML paper, PMLR. [Official/primary link](https://proceedings.mlr.press/v139/koh21a.html). Relevance: Shows how classification becomes research-worthy when the claim concerns real distribution shifts and worst-group performance.

[S53] ImageNet. Large Scale Visual Recognition Challenge. 2010–2017. Official benchmark page. [Official/primary link](https://www.image-net.org/challenges/LSVRC/). Relevance: Provides the official classification and detection challenge context, tasks, and evaluation motivation.

### Direct verdict

| **Verdict element** | **Controlling statement** |
| --- | --- |
| Decision | Parked |
| Primary reason | The implementation is feasible, but the generic contribution is too weak and saturated. |
| Strongest blocker | No defensible novelty beyond applying a standard model to a labeled dataset. |
| What would change this decision | A verified reliability, shift, or efficiency question with strong controls. |
| Present action | Use only as a baseline or task inside a named VLM lane. |

## 8.13 Generic Object Detection

|  |
| --- |
| **CANONICAL STATUS** Parked. Canonical group: Generic image classification or detection. |

### A. What is this field?

Object detection predicts what objects are present and where they are, usually with bounding boxes; instance segmentation also predicts masks; tracking links detections over time. IoU measures overlap, AP summarizes precision-recall across thresholds, and non-maximum suppression removes duplicate boxes in many detector families.

Major subfields: Two-stage and one-stage detection; transformer detectors; open-vocabulary detection; few-shot and long-tailed detection; domain adaptation; tracking; segmentation; efficient edge deployment.

Research versus implementation: A basic project annotates images and fine-tunes YOLO. Genuine research introduces a detection mechanism, studies a difficult setting such as long tails or open vocabulary, builds a rigorously documented dataset, or evaluates robustness/efficiency with strong detector baselines and error analysis.

### B. How does research in this field work?

* Data: images, boxes/masks, category ontology, crowd/ignore regions, source metadata, and sometimes video identities. COCO is a canonical benchmark [S49].
* Preprocessing: annotation QA, image/source splitting, resizing, augmentation, class-frequency analysis, and format conversion.
* Models: Faster/Mask R-CNN, RetinaNet, YOLO families, DETR-like transformers, open-vocabulary detectors, and lightweight variants.
* Baselines: pretrained detector, simple fine-tune, frozen backbone, size-matched detector, and closest method. Detectron2 provides strong model-zoo baselines [S51].
* Metrics: AP across IoU thresholds, AP by size/class frequency, precision/recall, localization errors, latency, memory, and calibration/robustness when claimed.
* Ablations: backbone, resolution, augmentation, label amount, matching/loss, threshold, and compute-matched controls.
* Research standard: DETR changed the detection formulation [S50]; LVIS studies large-vocabulary long tails [S52]. Merely running a modern detector is not comparable contribution.

### C. Why is this field valuable?

Detection is useful for production vision and develops annotation, localization, training, and deployment skills. It looked attractive because the result is visible and tools make fine-tuning easy. A working detector can still be a good capstone while being a weak thesis contribution.

### D. Why is it parked for this researcher?

The following is a reasoned suitability judgment based on the cited technical evidence and the researcher profile.

**1. Hard blockers**

* The canonical specification parks generic detection unless a defensible reliability, shift, efficiency, or other research problem is primary.
* High-quality custom box annotation is time-consuming, and existing-domain fine-tuning rarely establishes novelty.

**2. Major risks**

* Tool defaults and pretrained data can conceal leakage or category overlap.
* Small AP gains can result from resolution, augmentation, or training budget rather than the proposed method.
* Large detectors and multi-seed COCO-scale training exceed the budget.

**3. Manageable limitations**

* Small pretrained detectors on bounded datasets fit Colab.
* Metrics, libraries, and model zoos are mature.

**4. Opportunity-cost reasons**

* Detection can serve as a grounding baseline or automated evaluator for VLM hallucination, but it should not replace the VLM question.
* A generic detection thesis would underuse the frozen multimodal direction and face a crowded benchmark landscape.

### E. Why parked rather than permanently rejected?

Object detection remains a useful supporting task and engineering skill. It is suitable later when a strong non-generic problem, dataset, or efficiency/reliability contribution is verified.

### F. Can it appear inside the frozen VLM field?

Relationship classification: Compatible supporting method.

Use a detector to verify object presence in a VLM hallucination protocol, compare visual-only and VLM robustness, or measure open-vocabulary grounding. Validate detector errors so they are not mistaken for VLM errors.

### G. What would justify reconsideration?

* A public dataset and annotation protocol directly match a non-generic failure.
* A strong detector baseline reproduces within the compute budget.
* The evaluation separates classification, localization, calibration, and shift errors.
* The method contributes more than a model or dataset substitution.

### Feasibility scorecard (1–5 decision aid)

| **Criterion** | **Score** | **One-sentence justification** |
| --- | --- | --- |
| Problem clarity | 5 | Detection outputs and hypotheses are precise. |
| Dataset access | 4 | Large public datasets exist, while custom boxes are expensive to create. |
| Baseline reproducibility | 5 | Pretrained YOLO, Detectron2, and DETR baselines are available. |
| Compute feasibility | 4 | Small fine-tunes fit Colab; full COCO-scale training and multiple seeds may not. |
| Evaluation validity | 5 | AP and error taxonomies directly test detection, provided annotation quality is sound. |
| Domain dependence | 4 | Generic tasks are AI-centered, though specialized domains need expert labels. |
| Contribution potential | 2 | Routine fine-tuning has low novelty in a mature field. |
| Scope control | 4 | A bounded dataset is manageable, but annotation and training sweeps expand scope. |
| Engineering burden | 4 | Libraries reduce overhead, while annotation QA remains substantial. |
| Career alignment | 5 | Detection and deployment skills are strong engineering signals. |
| Opportunity cost | 2 | It is more rational as a VLM grounding tool than a new thesis identity. |

Unweighted mean: 4.00/5. This mean is descriptive only; hard blockers remain controlling.

### Curated evidence for this dossier

[S49] Lin et al.. Microsoft COCO: Common Objects in Context. 2014. ECCV paper and official dataset. [Official/primary link](https://cocodataset.org/). Relevance: Defines large-scale object detection, instance segmentation, and captioning with standardized annotations.

[S50] Carion et al.. End-to-End Object Detection with Transformers. 2020. ECCV paper and official code. [Official/primary link](https://arxiv.org/abs/2005.12872). Relevance: Representative detection contribution that reframed detection as direct set prediction and removed hand-designed pipeline components.

[S51] Meta AI Research. Detectron2 Model Zoo. 2026. Official repository documentation. [Official/primary link](https://github.com/facebookresearch/detectron2/blob/main/MODEL_ZOO.md). Relevance: Shows that strong pretrained detection baselines are readily available but many were trained on multi-GPU infrastructure.

[S52] Gupta, Dollár, and Girshick. LVIS: A Dataset for Large Vocabulary Instance Segmentation. 2019. CVPR paper and official dataset. [Official/primary link](https://www.lvisdataset.org/). Relevance: Illustrates research-level detection problems such as long-tailed categories and rare-class evaluation.

### Direct verdict

| **Verdict element** | **Controlling statement** |
| --- | --- |
| Decision | Parked |
| Primary reason | A generic fine-tuned detector is an implementation project with weak novelty. |
| Strongest blocker | No research contribution beyond standard detector training. |
| What would change this decision | A verified grounding, shift, long-tail, or efficiency problem with direct controls. |
| Present action | Use as a validated VLM grounding/evaluation baseline only. |

# 9. Cross-Field Decision Matrix

| **Field** | **Status** | **What it studies** | **Typical process** | **Main attraction** | **Hard blocker** | **Major risk** | **Colab Pro** | **Domain need** | **Evaluation** | **Contribution risk** | **VLM relation** | **Reconsideration trigger** |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| Standalone Cybersecurity | Parked | Security of systems/data | Threat data → security features → time/attack tests | Impact and security rigor | No security supervision | Unrealistic/stale data | Moderate | High | Conditional | High | Context | Verified expert supervision plus a current dataset, reproduced baseline, and deployment-faithful evaluation. |
| Federated Learning | Parked | Decentralized training | Client partitions → local rounds → aggregation | Privacy/distributed ML | No proven realistic clients | Simulation/experiment explosion | Low–moderate | Medium | Good if partitions valid | Medium–high | Major narrowing | Natural client partitions, reproduced strong baselines, and a tested Colab pilot. |
| Diffusion or Generative-Model Training as the Main Field | Parked | Learning to generate data | Curate → train/fine-tune → sample → human/task eval | Visible modern outputs | Training/eval budget | Metric subjectivity and crowded novelty | Low for main training | Low | Conditional | High | Supporting tool | An inference-first or PEFT contribution with validated metrics and a tested compute budget. |
| 3D Vision | Parked | Geometry and 3D scene understanding | Calibrate → reconstruct/encode → geometric tests | Spatial AI | No geometry pipeline/mentor | Storage and custom operators | Low | High | Good after calibration | High | Major narrowing | A preprocessed benchmark, reproduced baseline, bounded claim, and geometry mentor. |
| Robotics | Parked | Perceive-plan-act systems | Sim/robot data → policy → repeated rollouts | Embodied intelligence | No robot/lab/control mentor | Sim-to-real and unstable training | Low | Very high | Good in valid environment | High | Application context | Lab access, robotics co-supervision, reproduced benchmark policy, and bounded evaluation. |
| Autonomous-Driving Research | Parked | Vehicle perception to control | Calibrated sensors → models → scenario/closed-loop tests | High-impact multimodal systems | No safety-valid evaluation path | Industrial data and benchmark maturity | Low | Very high | Conditional | High | Application context | Autonomy lab partnership with preprocessed data, infrastructure, and evaluation support. |
| Specialized Sensing | Parked | Non-standard physical modalities | Decode/calibrate → modality model/fusion → sensor tests | Unique signal advantages | No sensors/physics expertise | Formats, calibration, data size | Low | Very high | Good after calibration | High | Major narrowing | Sensor-lab supervision plus a preprocessed, Colab-tested benchmark and baseline. |
| Standalone Medical Imaging | Parked | Clinical-image analysis | Patient data → medical preprocessing → expert-standard eval | Social value and rigorous AI | No clinical validator | Weak labels and single-site bias | Moderate | Very high | Conditional | Medium–high | Application context | Named clinical supervision plus verified patient-level data, baseline, and evaluation. |
| Standalone Explainable AI (XAI) | Parked | Explanations of model behavior | Explain → sanity/faithfulness tests → user/task eval | Debugging and trust | No validated explanation target | Plausible but unfaithful output | High | Low–medium | Weak unless task-grounded | Medium | Supporting method | A task-grounded faithfulness protocol with controls and a clear user. |
| Generic RAG Applications | Parked | Retrieval-grounded generation | Corpus → index → retrieve/rerank → generate → diagnose | Production relevance | No research gap in assembly | Component confounding/judges | High | Low | Mixed end-to-end | Very high if generic | Supporting method | A verified multimodal retrieval failure, public benchmark, strong controls, and direct evaluation. |
| Generic Agentic-AI Applications | Parked | Models taking tool actions | Environment → plan/act loop → executable tests | Automation and orchestration | No stable low-cost benchmark | Nondeterminism/API drift | Low–moderate | Low | High if executable | Very high if generic | Major narrowing | Reproducible environment, open-model budget, strong baselines, and one isolated contribution. |
| Generic Image Classification | Parked | Image-to-label prediction | Split → preprocess → fine-tune → multi-seed eval | Simple and foundational | No defensible generic novelty | Saturation/leakage | High | Low | High | Very high if generic | Supporting task | A verified reliability, shift, or efficiency question with strong controls. |
| Generic Object Detection | Parked | Locate and classify objects | Annotate → train detector → AP/error analysis | Production vision | No defensible generic novelty | Annotation and training confounds | Moderate–high | Low–medium | High | Very high if generic | Supporting baseline | A verified grounding, shift, long-tail, or efficiency problem with direct controls. |

## 9.1 Ranked present-suitability aid

This ranking compares only the parked fields under present conditions. It does not reopen the frozen parent field. A higher score can mean “useful as a supporting method,” not “authorize as a standalone thesis.”

| **Rank** | **Field** | **Current suitability** | **Future value** | **Present action** |
| --- | --- | --- | --- | --- |
| 1 | Standalone Explainable AI (XAI) | Low standalone; high as Rank 1 method | High | Use only within Trustworthy and Reliable VLMs for a named, measurable claim. |
| 2 | Generic Image Classification | Low standalone; high as baseline/task | Moderate to high | Use only as a baseline or task inside a named VLM lane. |
| 3 | Generic Object Detection | Low standalone; high as grounding baseline | Moderate to high | Use as a validated VLM grounding/evaluation baseline only. |
| 4 | Generic RAG Applications | Low standalone; conditional support | High | Use only if necessary for a named VLM research question. |
| 5 | Standalone Medical Imaging | Low; clinical gate fails | High | Use only as a public-data VLM application context with no clinical claim. |
| 6 | Generic Agentic-AI Applications | Very low; contribution/cost gates fail | Moderate to high | Do not build a generic agent thesis; use only a minimal agent layer for a VLM reliability question. |
| 7 | Federated Learning | Very low; systems/fit gates fail | High | Preserve for later; do not federate a VLM during current discovery. |
| 8 | Diffusion or Generative-Model Training as the Main Field | Very low; compute/evaluation gates fail | Moderate to high | Use pretrained generation only as a controlled tool inside a named VLM lane. |
| 9 | Standalone Cybersecurity | Very low; supervision gate fails | Moderate to high | Preserve for later; use security only as a named VLM reliability/generalization context. |
| 10 | 3D Vision | Very low; geometry/tooling gates fail | High | Do not pursue as a parent field; allow only a tightly controlled VLM input condition. |
| 11 | Specialized Sensing | Very low; sensor-supervision gate fails | Moderate to high | Do not pursue as a field; permit only validated modality inputs inside VLM work. |
| 12 | Robotics | Very low; hardware/control gates fail | High | Preserve for later; simulation may be used only as a VLM evaluation context. |
| 13 | Autonomous-Driving Research | Very low; safety/infrastructure gates fail | Moderate to high | Do not pursue; use road scenes only as a bounded VLM test context. |

# 10. Opportunity-Cost Analysis

Opportunity cost is not a vague preference. Every new field requires terminology, seminal papers, recent baselines, dataset infrastructure, evaluation norms, failure analysis, and supervisor calibration. The frozen VLM field already converts the researcher’s transformer/multimodal foundation into three feasible research lanes.

| **If attention shifts to...** | **Immediate cost** | **What is delayed in the frozen field** |
| --- | --- | --- |
| A new domain | Weeks of domain and evaluation learning | Rank 1 paper synthesis and hallucination/calibration baseline reproduction |
| A new framework | Environment and integration work | A direct measurement pilot on a public VLM benchmark |
| A new large model | Model-specific setup and generation/inference cost | Cross-model protocol design and controlled ablations |
| A new dataset | Access, schema, license, preprocessing, leakage audit | Validation of the already shortlisted VLM dataset/baseline pair |
| A new hardware field | Geometry, sensors, simulation, or control stack | Colab-first inference/PEFT experiments and reproducible tooling |

|  |
| --- |
| **RATIONAL DEFAULT** Continue in the frozen VLM field unless materially new evidence passes the formal reconsideration protocol. Boredom and novelty attraction are not evidence. |

# 11. Relationship of Parked Fields to the Frozen VLM Lanes

| **Parked field** | **Relationship class** | **Most plausible VLM lane** | **Boundary example** |
| --- | --- | --- | --- |
| Standalone Cybersecurity | Compatible application context | Primarily Rank 1: Trustworthy/Reliable VLMs | Security may appear inside VLM work only as a measured VLM property, for example multimodal prompt-injection robustness, manipulated-image detection under unseen generators, or malicious image-text conflict. |
| Federated Learning | Compatible only after major narrowing | No default lane; intersection is currently unnecessary | A federated VLM study is theoretically possible, but it is an unnecessary intersection now. |
| Diffusion or Generative-Model Training as the Main Field | Compatible supporting method | Rank 1 or 2 as controlled data/intervention tool | A pretrained diffusion model may generate controlled corruptions, counterfactual images, or synthetic shift conditions for a VLM reliability/generalization study. |
| 3D Vision | Compatible only after major narrowing | Primarily Rank 2: Generalization/Shift | A small 3D or depth cue could be an input condition in a VLM grounding study, but a thesis centered on reconstruction, SLAM, or 3D detection is directly outside the frozen scope. |
| Robotics | Compatible application context | Rank 1 only as bounded embodied evaluation context | An embodied VLM benchmark could test instruction grounding or uncertainty in simulation, but it must remain inference/evaluation-centered and avoid claims about real robot deployment. |
| Autonomous-Driving Research | Compatible application context | Primarily Rank 2: Generalization/Shift | Road-scene VQA or VLM uncertainty under weather/sensor conflict may be used as a bounded VLM benchmark. |
| Specialized Sensing | Compatible only after major narrowing | Primarily Rank 2: Generalization/Shift | Thermal, depth, or event-derived frames could appear in a VLM robustness study only if an accessible benchmark and validated preprocessing exist. |
| Standalone Medical Imaging | Compatible application context | Primarily Rank 1: Trustworthy/Reliable VLMs | A public chest-X-ray VQA benchmark could test VLM hallucination or calibration, provided the team states that it is a benchmark study, validates labels, and makes no diagnostic or deployment claim. |
| Standalone Explainable AI (XAI) | Compatible supporting method | Primarily Rank 1: Trustworthy/Reliable VLMs | Use visual evidence attribution, concept probes, attention intervention, or counterfactual images to test whether a VLM’s answer is grounded. |
| Generic RAG Applications | Compatible supporting method | Rank 1 or 2 when retrieval is the tested failure source | Use image-text or document retrieval to test whether a VLM remains reliable under missing, degraded, contradictory, or shifted evidence. |
| Generic Agentic-AI Applications | Compatible only after major narrowing | Primarily Rank 1: Trustworthy/Reliable VLMs | A multimodal agent could be used to test whether visual misperception propagates into tool actions, but the research claim must be about VLM reliability and the environment must provide exact success/failure labels. |
| Generic Image Classification | Compatible supporting method | Primarily Rank 2: Generalization/Shift | Image classification may provide a visual-only baseline, an AI-generated image detector, or a corruption/shift probe inside Rank 1, 2, or 3. |
| Generic Object Detection | Compatible supporting method | Primarily Rank 1: Trustworthy/Reliable VLMs | Use a detector to verify object presence in a VLM hallucination protocol, compare visual-only and VLM robustness, or measure open-vocabulary grounding. |

# 12. When I Become Attracted to Another Field Again

## A new paper makes a parked field exciting

* Excitement: one result and polished framing.
* Feasibility: verified data, baseline, compute, supervision, and direct metric.
* Gap: closest work and stronger controls still leave the claim unresolved.
* Change request? Only if all evidence is written; normally no.

## A framework makes implementation easy

* Excitement: reduced coding friction.
* Feasibility: end-to-end experiment and repeated evaluation fit the budget.
* Gap: framework use isolates a new mechanism rather than assembling components.
* Change request? No; ease of implementation is not novelty.

## A benchmark reports impressive results

* Excitement: headline score.
* Feasibility: the benchmark and strong baseline reproduce under correct splits.
* Gap: the proposed claim changes conclusions, not only the score.
* Change request? Only after contamination, saturation, and metric validity checks.

## A topic sounds more prestigious or advanced

* Excitement: status language.
* Feasibility: observable assets and bounded experiments, not prestige.
* Gap: supported by primary literature and controls.
* Change request? No, unless evidence beats all VLM lanes.

## Another student chooses a different field

* Excitement: social comparison.
* Feasibility: their supervision, data, and compute are not yours.
* Gap: must be independently verified.
* Change request? No.

## RAG or agent tools make a demo easy

* Excitement: rapid visible system.
* Feasibility: stable open models and executable evaluation.
* Gap: retrieval/agent failure is isolated against simpler baselines.
* Change request? Usually no; keep it as an engineering project.

## A medical/pharmaceutical idea looks socially meaningful

* Excitement: valuable application.
* Feasibility: verified labels, legal data, expert validation, and no clinical overclaim.
* Gap: task and evaluation are clinically meaningful, not merely available.
* Change request? Only with named domain supervision and full evidence.

## Cybersecurity or FL looks publishable

* Excitement: active venues and serious terminology.
* Feasibility: realistic threat/client setting, strong baseline, and validated evaluation.
* Gap: not a classifier or aggregation tweak.
* Change request? Only after domain/system burden is tested.

## A new generative model becomes popular

* Excitement: novelty and visible outputs.
* Feasibility: repeated training/evaluation fits Colab and storage.
* Gap: method or validated evaluation, not a new adapter.
* Change request? No for popularity alone.

## A demo looks technically impressive

* Excitement: many components and polished UI.
* Feasibility: irrelevant unless the claim is testable.
* Gap: each component must be necessary and ablated.
* Change request? No; demos are not evidence.

## VLM paper reading feels slow or boring

* Excitement: switching creates temporary novelty.
* Feasibility: unchanged; the frozen lanes remain better supported.
* Gap: boredom provides no literature evidence.
* Change request? No. Finish the next bounded reading or pilot task.

# 13. Formal Reconsideration Protocol

A parked or rejected field cannot be reopened casually. Submit a written change request containing all thirteen items below. Missing evidence means the request is rejected without further literature review.

1. Name of the field.
2. Current canonical status.
3. Materially new evidence that did not exist during the original decision.
4. Verified public dataset, official link, license/access state, schema, size, labels, and known risks.
5. Reproducible strong baseline with environment, code, result, and discrepancy log.
6. Evaluation plan with primary metric, controls, ablations, and error analysis.
7. Tested compute estimate: GPU type, VRAM, runtime, storage, number of runs, seeds, and fallback.
8. Required specialist supervision and named availability.
9. One-sentence proposed research contribution and closest competing work.
10. Comparison against all three frozen VLM lanes under the same feasibility criteria.
11. Opportunity cost of changing direction, including discarded reading, code, and schedule.
12. Fallback plan if the method, data, or evaluation fails.
13. Final verdict: retain current direction or authorize reconsideration.

|  |
| --- |
| **INSUFFICIENT EVIDENCE** A new paper, popular model, repository, social-media discussion, attractive application, or easy framework alone is not sufficient. |

# 14. Final Boundary Statement

|  |
| --- |
| **FORMAL BOUNDARY** Multimodal / Vision-Language Learning and Systems remains the frozen parent field. The three ranked VLM lanes remain the only authorized lanes for current topic discovery. Parked fields are retained for future reference but must not consume present research time. Rejected fields, if any are recorded in a future revision, must not be reopened without materially new evidence. Supporting methods may be used only when they directly serve a defensible VLM research question. The final thesis topic still requires separate dataset, baseline, evaluation, compute, contribution, and fallback validation. This report does not claim that excluded fields are scientifically weak; it records why they are currently inferior choices under the researcher’s constraints. |

# 15. References

## 15.1 Governing and supplied sources

[C1] Canonical Thesis Field Specification, version 1.0, effective 22 August 2026. Uploaded Word document. Highest-authority source for statuses, frozen field, ranked lanes, feasibility gates, and change control.

[C2] Thesis Control Center. Project-authoritative instruction and decision-workflow source. Used only where it does not conflict with C1.

[C3] Paper Digest, CVPR 2025 Topics. Supplied Markdown orientation file. Not used as a status authority or decisive technical evidence.

## 15.2 Technical and benchmark sources

[S01] National Institute of Standards and Technology. Cybersecurity Framework 2.0. 2024. Official standard/framework. <https://www.nist.gov/cyberframework>. Relevance: Shows that cybersecurity spans governance, identification, protection, detection, response, and recovery rather than only an ML classifier.

[S02] Canadian Institute for Cybersecurity, University of New Brunswick. Intrusion Detection Evaluation Dataset (CIC-IDS2017). 2017. Official dataset page. <https://www.unb.ca/cic/datasets/ids-2017.html>. Relevance: Provides labeled flows and packet captures but also illustrates the specialized traffic-generation and labeling assumptions behind IDS research.

[S03] Joyce et al.. EMBER2024: A Benchmark Dataset for Holistic Evaluation of Malware Classifiers. 2025. arXiv preprint and official repository. <https://arxiv.org/abs/2506.05074>. Relevance: Documents a modern 3.2-million-file malware benchmark and the continuing dependence of malware research on industry-scale data curation.

[S04] Pendlebury et al.. TESSERACT: Eliminating Experimental Bias in Malware Classification across Space and Time. 2019. USENIX Security Symposium paper. <https://www.usenix.org/conference/usenixsecurity19/presentation/pendlebury>. Relevance: Shows how random or unrealistic splits can inflate malware-classification results and why temporal, deployment-aware evaluation matters.

[S05] McMahan et al.. Communication-Efficient Learning of Deep Networks from Decentralized Data. 2017. AISTATS paper, PMLR. <https://proceedings.mlr.press/v54/mcmahan17a.html>. Relevance: Foundational FedAvg paper defining iterative local training and server aggregation under decentralized data.

[S06] Caldas et al.. LEAF: A Benchmark for Federated Settings. 2018. arXiv paper and benchmark. <https://arxiv.org/abs/1812.01097>. Relevance: Provides federated datasets, evaluation, and reference implementations designed around realistic heterogeneity.

[S07] Talwalkar Lab. LEAF: A Benchmark for Federated Settings. 2018. Official repository. <https://github.com/TalwalkarLab/leaf>. Relevance: Shows the preprocessing and baseline infrastructure needed to construct federated partitions and run reference experiments.

[S08] Flower Labs. Run Simulations - Flower Framework. 2026. Official framework documentation. <https://flower.ai/docs/framework/how-to-run-simulations.html>. Relevance: Documents resource-aware client simulation and the CPU/GPU scheduling burden even when no real institutions participate.

[S09] Ho, Jain, and Abbeel. Denoising Diffusion Probabilistic Models. 2020. NeurIPS paper. <https://proceedings.neurips.cc/paper/2020/hash/4c5bcfec8584af0d967f1ab10179ca4b-Abstract.html>. Relevance: Foundational diffusion-model formulation based on iterative denoising.

[S10] Rombach et al.. High-Resolution Image Synthesis with Latent Diffusion Models. 2022. CVPR paper. <https://openaccess.thecvf.com/content/CVPR2022/html/Rombach_High-Resolution_Image_Synthesis_With_Latent_Diffusion_Models_CVPR_2022_paper.html>. Relevance: Representative modern architecture that reduces pixel-space cost by operating in a learned latent space.

[S11] Hugging Face. Text-to-image Training Guide. 2026. Official Diffusers documentation. <https://huggingface.co/docs/diffusers/training/text2image>. Relevance: States that even optimized text-to-image fine-tuning targets a 24 GB GPU, with larger GPUs preferred for higher batch sizes or speed.

[S12] Ghosh, Hajishirzi, and Schmidt. GenEval: An Object-Focused Framework for Evaluating Text-to-Image Alignment. 2023. arXiv paper and official repository. <https://arxiv.org/abs/2310.11513>. Relevance: Shows that generative evaluation requires fine-grained alignment tests, not only visual appeal or one aggregate score.

[S13] Dai et al.. ScanNet: Richly-Annotated 3D Reconstructions of Indoor Scenes. 2017. CVPR paper and official dataset. <https://www.scan-net.org/>. Relevance: Provides 2.5 million RGB-D views, camera poses, reconstructions, and semantic annotations across more than 1,500 scans.

[S14] Yeshwanth et al.. ScanNet++: A High-Fidelity Dataset of 3D Indoor Scenes. 2023. ICCV paper and official project. <https://scannetpp.mlsg.cit.tum.de/scannetpp/>. Relevance: Illustrates current 3D data complexity through laser scans, DSLR images, RGB-D streams, calibration, and semantic labels.

[S15] Geiger, Lenz, and Urtasun. Are We Ready for Autonomous Driving? The KITTI Vision Benchmark Suite. 2012. CVPR paper and official benchmark. <https://www.cvlibs.net/datasets/kitti/>. Relevance: Defines calibrated stereo, optical-flow, odometry, 3D detection, and tracking benchmarks collected from a sensor-equipped vehicle.

[S16] ScanNet++ authors. ScanNet++ Toolkit. 2023. Official repository. <https://github.com/scannetpp/scannetpp>. Relevance: Shows the practical calibration, undistortion, depth rendering, downscaling, storage, and evaluation tooling required for 3D experiments.

[S17] James et al.. RLBench: The Robot Learning Benchmark & Learning Environment. 2019. arXiv paper and official benchmark. <https://arxiv.org/abs/1909.12271>. Relevance: Defines 100 manipulation tasks with RGB, depth, masks, proprioception, and demonstration generation.

[S18] Gu et al.. ManiSkill2: A Unified Benchmark for Generalizable Manipulation Skills. 2023. arXiv paper and open benchmark. <https://arxiv.org/abs/2302.04659>. Relevance: Provides dynamic simulation, 20 task families, over 2,000 objects, and millions of demonstration frames, showing the experiment scale of modern robot learning.

[S19] Heo et al.. FurnitureBench: Reproducible Real-World Benchmark for Long-Horizon Complex Manipulation. 2023. arXiv paper and benchmark. <https://arxiv.org/abs/2305.12821>. Relevance: Demonstrates the gap between simulation and real robot evaluation and the physical setup required for long-horizon manipulation claims.

[S20] Stephen James et al.. RLBench Repository. 2019. Official repository. <https://github.com/stepjam/RLBench>. Relevance: Provides the simulator integration and code base needed to reproduce robot-learning baselines.

[S21] Caesar et al.. nuScenes: A Multimodal Dataset for Autonomous Driving. 2020. CVPR paper and official dataset. <https://www.nuscenes.org/>. Relevance: Combines six cameras, five radars, one lidar, maps, and 3D labels across 1,000 driving scenes.

[S22] Waymo. Waymo Open Dataset: About. 2026. Official dataset documentation. <https://waymo.com/open/about/>. Relevance: Documents perception, motion, and end-to-end datasets at a scale that creates substantial storage and preprocessing demands.

[S23] Dosovitskiy et al.. CARLA: An Open Urban Driving Simulator. 2017. CoRL paper, PMLR. <https://proceedings.mlr.press/v78/dosovitskiy17a.html>. Relevance: Provides controlled autonomous-driving simulation but requires scenario design, simulator operation, and careful transfer claims.

[S24] KITTI authors. KITTI 3D Object Detection Evaluation. 2026. Official benchmark page. <https://www.cvlibs.net/datasets/kitti/eval_object.php?obj_benchmark=3d>. Relevance: Lists data volumes, sensor modalities, labels, and server-side evaluation for a canonical driving-perception task.

[S25] Gehrig et al.. DSEC: A Stereo Event Camera Dataset for Driving Scenarios. 2021. IEEE Robotics and Automation Letters paper and official dataset. <https://dsec.ifi.uzh.ch/>. Relevance: Shows event-camera research depends on synchronized event streams, stereo frames, lidar, GPS, and specialized representations.

[S26] Behley et al.. SemanticKITTI: A Dataset for Semantic Scene Understanding of LiDAR Sequences. 2019. ICCV paper and official benchmark. <https://semantic-kitti.org/>. Relevance: Provides dense point-wise LiDAR annotations and sequence-based evaluation for 3D semantic understanding.

[S27] Hwang et al.. Multispectral Pedestrian Detection: Benchmark Dataset and Baseline. 2015. CVPR paper and official project. <https://soonminhwang.github.io/rgbt-ped-detection/>. Relevance: Provides 95,000 aligned color-thermal pairs captured with specialized beam-splitter hardware.

[S28] Prophesee. GEN1 Automotive Detection Dataset. 2020. Official dataset and documentation. <https://docs.prophesee.ai/stable/datasets.html>. Relevance: Documents event-data formats and a 200 GB compressed, 750 GB uncompressed detection dataset, exposing the storage burden of specialized sensing.

[S29] Johnson et al.. MIMIC-CXR Database v2.1.0. 2024. PhysioNet official dataset. <https://physionet.org/content/mimic-cxr/>. Relevance: Provides 377,110 de-identified radiographs with reports under controlled-access requirements.

[S30] Irvin et al.. CheXpert: A Large Chest Radiograph Dataset with Uncertainty Labels and Expert Comparison. 2019. AAAI paper and official dataset. <https://stanfordmlgroup.github.io/competitions/chexpert/>. Relevance: Shows that high-quality evaluation uses uncertainty labels and radiologist-annotated reference sets.

[S31] Tejani et al.. Checklist for Artificial Intelligence in Medical Imaging: 2024 Update. 2024. Radiology: Artificial Intelligence guideline. <https://pubs.rsna.org/doi/abs/10.1148/ryai.240300>. Relevance: Defines reporting expectations for medical-imaging AI, including data, reference standards, evaluation, and limitations.

[S32] RSNA. Checklist for Artificial Intelligence in Medical Imaging (CLAIM). 2024. Official guideline page. <https://pubs.rsna.org/page/ai/claim>. Relevance: Confirms that classification, segmentation, and reconstruction studies need domain-appropriate transparent reporting.

[S33] Ribeiro, Singh, and Guestrin. Why Should I Trust You? Explaining the Predictions of Any Classifier. 2016. KDD paper. <https://arxiv.org/abs/1602.04938>. Relevance: Introduces LIME and illustrates local surrogate explanations and human-centered evaluation.

[S34] Lundberg and Lee. A Unified Approach to Interpreting Model Predictions. 2017. NeurIPS paper. <https://arxiv.org/abs/1705.07874>. Relevance: Introduces SHAP and formalizes additive feature-attribution methods.

[S35] Adebayo et al.. Sanity Checks for Saliency Maps. 2018. NeurIPS paper. <https://papers.nips.cc/paper/8160-sanity-checks-for-saliency-maps>. Relevance: Demonstrates that visually plausible explanations can fail model- and data-randomization tests.

[S36] Doshi-Velez and Kim. Towards a Rigorous Science of Interpretable Machine Learning. 2017. arXiv position paper. <https://arxiv.org/abs/1702.08608>. Relevance: Explains why interpretability needs a defined user, task, and evaluation rather than an attractive visualization alone.

[S37] Meta PyTorch. Captum: Model Interpretability for PyTorch. 2026. Official framework documentation. <https://captum.ai/>. Relevance: Shows that applying attribution algorithms is easy; the research challenge lies in validating what the explanations mean.

[S38] Lewis et al.. Retrieval-Augmented Generation for Knowledge-Intensive NLP Tasks. 2020. NeurIPS paper. <https://proceedings.neurips.cc/paper/2020/hash/6b493230205f780e1bc26945df7481e5-Abstract.html>. Relevance: Foundational RAG work combining parametric generation with non-parametric retrieval.

[S39] Thakur et al.. BEIR: A Heterogeneous Benchmark for Zero-shot Evaluation of Information Retrieval Models. 2021. NeurIPS Datasets and Benchmarks paper. <https://datasets-benchmarks-proceedings.neurips.cc/paper/2021/hash/65b9eea6e1cc6bb9f0cd2a47751a186f-Abstract-round2.html>. Relevance: Provides 18 retrieval datasets and shows why retrieval must be evaluated across heterogeneous tasks.

[S40] Petroni et al.. KILT: A Benchmark for Knowledge Intensive Language Tasks. 2021. NAACL paper and official repository. <https://aclanthology.org/2021.naacl-main.200/>. Relevance: Requires both downstream-task performance and evidence provenance, not answer fluency alone.

[S41] Ru et al.. RAGChecker: A Fine-grained Framework for Diagnosing Retrieval-Augmented Generation. 2024. NeurIPS paper and official repository. <https://github.com/amazon-science/RAGChecker>. Relevance: Separates retrieval and generation diagnostics and validates metrics against human judgments.

[S42] Yao et al.. ReAct: Synergizing Reasoning and Acting in Language Models. 2023. ICLR paper. <https://openreview.net/forum?id=WE_vluYUL-X>. Relevance: Foundational agent pattern that interleaves reasoning traces with environment actions.

[S43] Liu et al.. AgentBench: Evaluating LLMs as Agents. 2024. ICLR paper. <https://openreview.net/forum?id=zAdUB0aCTQ>. Relevance: Evaluates agents across eight environments and identifies long-horizon reasoning and instruction-following failures.

[S44] Zhou et al.. WebArena: A Realistic Web Environment for Building Autonomous Agents. 2024. ICLR paper. <https://openreview.net/forum?id=oKn9c6ytLx>. Relevance: Shows that realistic web-agent evaluation needs reproducible websites, executable actions, and end-to-end task success.

[S45] Jimenez et al.. SWE-bench: Can Language Models Resolve Real-World GitHub Issues?. 2024. ICLR paper and benchmark. <https://openreview.net/forum?id=VTF8yNQM66>. Relevance: Uses executable repository tests to evaluate agents, illustrating the infrastructure and contamination risks of agent benchmarks.

[S46] Russakovsky et al.. ImageNet Large Scale Visual Recognition Challenge. 2015. International Journal of Computer Vision paper. <https://arxiv.org/abs/1409.0575>. Relevance: Defines the large-scale classification and detection benchmark that shaped modern visual recognition.

[S47] He et al.. Deep Residual Learning for Image Recognition. 2016. CVPR paper and official models. <https://arxiv.org/abs/1512.03385>. Relevance: Representative architecture contribution showing that genuine classification research changes optimization or representation, not only the application dataset.

[S48] Koh et al.. WILDS: A Benchmark of in-the-Wild Distribution Shifts. 2021. ICML paper, PMLR. <https://proceedings.mlr.press/v139/koh21a.html>. Relevance: Shows how classification becomes research-worthy when the claim concerns real distribution shifts and worst-group performance.

[S49] Lin et al.. Microsoft COCO: Common Objects in Context. 2014. ECCV paper and official dataset. <https://cocodataset.org/>. Relevance: Defines large-scale object detection, instance segmentation, and captioning with standardized annotations.

[S50] Carion et al.. End-to-End Object Detection with Transformers. 2020. ECCV paper and official code. <https://arxiv.org/abs/2005.12872>. Relevance: Representative detection contribution that reframed detection as direct set prediction and removed hand-designed pipeline components.

[S51] Meta AI Research. Detectron2 Model Zoo. 2026. Official repository documentation. <https://github.com/facebookresearch/detectron2/blob/main/MODEL_ZOO.md>. Relevance: Shows that strong pretrained detection baselines are readily available but many were trained on multi-GPU infrastructure.

[S52] Gupta, Dollár, and Girshick. LVIS: A Dataset for Large Vocabulary Instance Segmentation. 2019. CVPR paper and official dataset. <https://www.lvisdataset.org/>. Relevance: Illustrates research-level detection problems such as long-tailed categories and rare-class evaluation.

[S53] ImageNet. Large Scale Visual Recognition Challenge. 2010–2017. Official benchmark page. <https://www.image-net.org/challenges/LSVRC/>. Relevance: Provides the official classification and detection challenge context, tasks, and evaluation motivation.

# 16. Appendix: One-Page Decision Cards

Each card compresses the controlling decision. The detailed dossier remains authoritative when the card omits nuance.

**DECISION CARD 1 OF 13**

# Standalone Cybersecurity

|  |
| --- |
| **STATUS** Parked |

| **Decision element** | **Canonical card** |
| --- | --- |
| What it is | Cybersecurity studies how to prevent, detect, understand, contain, and recover from attacks on software, networks, identities, data, and infrastructure. |
| How research works | Data: packet captures and flow records, binaries or extracted features, logs, URLs, source code, vulnerability records, or controlled attack traces; Preprocessing: reconstruct sessions, extract protocol or binary features, de-duplicate related samples, remove leakage, preserve time, and document label provenance; Models and baselines: rules/signatures, logistic regression or tree ensembles, anomaly detectors, CNN/Transformer encoders, graph models, and security-specific systems; Experiments: define attacker knowledge, train on past or source environments, test on future or different environments, and vary attack family, prevalence, evasion, or data drift. |
| Why attractive | The field protects real systems and develops rigorous thinking about threats, distribution shift, monitoring, and failure costs. |
| Why unsuitable now | Domain-supervision and evaluation-validity risk outweigh current fit. |
| Strongest blocker | No reliable security expert to validate whether the threat model and experiment are realistic. |
| Possible role inside VLM | Compatible application context: Security may appear inside VLM work only as a measured VLM property, for example multimodal prompt-injection robustness, manipulated-image detection under unseen generators, or malicious image-text conflict. |
| Reconsideration condition | Verified expert supervision plus a current dataset, reproduced baseline, and deployment-faithful evaluation. |
| Present instruction | Preserve for later; use security only as a named VLM reliability/generalization context. |

**Do not reopen from excitement. Use the formal reconsideration protocol.**

**DECISION CARD 2 OF 13**

# Federated Learning

|  |
| --- |
| **STATUS** Parked |

| **Decision element** | **Canonical card** |
| --- | --- |
| What it is | Federated learning (FL) trains a shared model across multiple clients while raw data remain local. |
| How research works | Data: naturally partitioned client data or defensible synthetic partitions; Preprocessing: construct clients without leakage; specify client size, label skew, feature skew, temporal drift, availability, and train/validation/test separation; Architecture: a server selects clients, clients train locally, updates are aggregated, and the process repeats; Baselines: centralized training, local-only models, FedAvg, FedProx or SCAFFOLD-like controls, plus size- and round-matched variants appropriate to the claim. |
| Why attractive | FL addresses collaboration when data cannot be centralized and develops distributed-systems, optimization, privacy, and evaluation skills. |
| Why unsuitable now | Systems and methodological burden is high relative to fit with the frozen VLM direction. |
| Strongest blocker | A defensible client/data setting plus repeated training cannot yet be shown within the thesis budget. |
| Possible role inside VLM | Compatible only after major narrowing: A federated VLM study is theoretically possible, but it is an unnecessary intersection now. |
| Reconsideration condition | Natural client partitions, reproduced strong baselines, and a tested Colab pilot. |
| Present instruction | Preserve for later; do not federate a VLM during current discovery. |

**Do not reopen from excitement. Use the formal reconsideration protocol.**

**DECISION CARD 3 OF 13**

# Diffusion or Generative-Model Training as the Main Field

|  |
| --- |
| **STATUS** Parked |

| **Decision element** | **Canonical card** |
| --- | --- |
| What it is | Generative modeling learns a data distribution so a model can create new images, video, audio, text, or other samples. |
| How research works | Data: large image-text pairs or domain-specific image collections with captions, filtering, rights, duplicates, and safety review; Preprocessing: resize/crop, caption cleaning, deduplication, latent caching, concept filtering, and data-quality auditing; Models: DDPM-style denoisers [S09], latent diffusion [S10], diffusion transformers, autoregressive image models, GANs, VAEs, or flows; Training: sample timesteps or tokens, optimize denoising/generation objectives, checkpoint large models, and run many validation generations; parameter-efficient adaptation reduces but does not remove cost. |
| Why attractive | Generative models are scientifically influential and teach representation learning, large-model training, data curation, and multimodal evaluation. |
| Why unsuitable now | Compute and evaluation burden are disproportionate to an undergraduate thesis. |
| Strongest blocker | A publication-quality training and evaluation loop has not been shown to fit Colab Pro. |
| Possible role inside VLM | Compatible supporting method: A pretrained diffusion model may generate controlled corruptions, counterfactual images, or synthetic shift conditions for a VLM reliability/generalization study. |
| Reconsideration condition | An inference-first or PEFT contribution with validated metrics and a tested compute budget. |
| Present instruction | Use pretrained generation only as a controlled tool inside a named VLM lane. |

**Do not reopen from excitement. Use the formal reconsideration protocol.**

**DECISION CARD 4 OF 13**

# 3D Vision

|  |
| --- |
| **STATUS** Parked |

| **Decision element** | **Canonical card** |
| --- | --- |
| What it is | 3D vision reconstructs or understands geometry from point clouds, depth sensors, multiple images, video, or neural scene representations. |
| How research works | Data: calibrated images, RGB-D sequences, point clouds, meshes, camera poses, and 3D labels; Preprocessing: calibration, pose alignment, registration, voxelization or point sampling, coordinate normalization, visibility handling, and scene-level splitting; Models: PointNet-like point encoders, sparse 3D CNNs, voxel/BEV models, multi-view transformers, NeRFs, Gaussian splats, and image-depth fusion; Baselines: classical geometry, pretrained 3D networks, 2D-only controls, and representation-matched methods. |
| Why attractive | 3D vision develops geometry, representation learning, perception, and high-value spatial AI skills. |
| Why unsuitable now | Geometry, preprocessing, and tooling add a new foundation that the current thesis does not need. |
| Strongest blocker | No demonstrated Colab-stable 3D baseline and no geometry supervision. |
| Possible role inside VLM | Compatible only after major narrowing: A small 3D or depth cue could be an input condition in a VLM grounding study, but a thesis centered on reconstruction, SLAM, or 3D detection is directly outside the frozen scope. |
| Reconsideration condition | A preprocessed benchmark, reproduced baseline, bounded claim, and geometry mentor. |
| Present instruction | Do not pursue as a parent field; allow only a tightly controlled VLM input condition. |

**Do not reopen from excitement. Use the formal reconsideration protocol.**

**DECISION CARD 5 OF 13**

# Robotics

|  |
| --- |
| **STATUS** Parked |

| **Decision element** | **Canonical card** |
| --- | --- |
| What it is | Robotics studies agents that perceive, plan, and act in a physical or simulated world. |
| How research works | Data: demonstrations, trajectories, RGB/RGB-D, robot state, actions, rewards, object models, and simulator scenes; Preprocessing: synchronize observations/actions, define controllers, normalize state, generate demonstrations, and create train/test object or task splits; Models: behavior cloning, diffusion policies, reinforcement learning, vision-language-action models, planning, or hybrid sense-plan-act systems; Experiments: train across tasks or objects, evaluate repeated rollouts, vary initial states, and test disturbances or unseen objects. |
| Why attractive | Robotics integrates AI with action and develops perception, control, systems, and evaluation skills. |
| Why unsuitable now | Unavailable hardware and robotics supervision make credible validation impractical. |
| Strongest blocker | No route to physical validation or expert review of the control setting. |
| Possible role inside VLM | Compatible application context: An embodied VLM benchmark could test instruction grounding or uncertainty in simulation, but it must remain inference/evaluation-centered and avoid claims about real robot deployment. |
| Reconsideration condition | Lab access, robotics co-supervision, reproduced benchmark policy, and bounded evaluation. |
| Present instruction | Preserve for later; simulation may be used only as a VLM evaluation context. |

**Do not reopen from excitement. Use the formal reconsideration protocol.**

**DECISION CARD 6 OF 13**

# Autonomous-Driving Research

|  |
| --- |
| **STATUS** Parked |

| **Decision element** | **Canonical card** |
| --- | --- |
| What it is | Autonomous-driving research builds perception, prediction, planning, control, simulation, and safety systems for vehicles. |
| How research works | Data: synchronized camera, lidar, radar, GPS/IMU, maps, 3D boxes, trajectories, and scenario metadata; Preprocessing: calibration, timestamp synchronization, coordinate transforms, sweeps, map alignment, tracking IDs, scenario slicing, and privacy/license compliance; Models: BEV fusion, 3D detectors, trackers, trajectory predictors, occupancy networks, planners, or end-to-end policies; Baselines: sensor-specific and fusion baselines, classical tracking/planning, leaderboard models, and simple constant-velocity or rule controls. |
| Why attractive | The field is high-impact and develops multimodal perception and safety systems skills. |
| Why unsuitable now | The field requires industrial-scale data and safety-valid evaluation that the team cannot provide. |
| Strongest blocker | No credible closed-loop or domain-expert validation path. |
| Possible role inside VLM | Compatible application context: Road-scene VQA or VLM uncertainty under weather/sensor conflict may be used as a bounded VLM benchmark. |
| Reconsideration condition | Autonomy lab partnership with preprocessed data, infrastructure, and evaluation support. |
| Present instruction | Do not pursue; use road scenes only as a bounded VLM test context. |

**Do not reopen from excitement. Use the formal reconsideration protocol.**

**DECISION CARD 7 OF 13**

# Specialized Sensing

|  |
| --- |
| **STATUS** Parked |

| **Decision element** | **Canonical card** |
| --- | --- |
| What it is | Specialized sensing develops perception from non-standard modalities such as lidar, radar, event cameras, thermal, hyperspectral, polarization, or single-photon sensors. |
| How research works | Data: asynchronous events, point clouds, radar tensors, aligned RGB-thermal pairs, spectral cubes, calibration files, and synchronized ground truth; Preprocessing: decode proprietary/binary formats, synchronize modalities, calibrate extrinsics/intrinsics, compensate motion, voxelize or bin events, normalize bands, and manage missing data; Models: spiking or event encoders, sparse point networks, range-view CNNs, radar fusion, multispectral fusion, and spectral-spatial networks; Baselines: modality-only, frame/RGB-only, early/late fusion, classical signal processing, and sensor-specific published models. |
| Why attractive | The field can solve conditions where ordinary cameras fail and develops multimodal fusion, signal processing, and efficient perception skills. |
| Why unsuitable now | Sensor-specific validation and infrastructure are unavailable. |
| Strongest blocker | No access to the sensing process or expert who can validate calibration and artifacts. |
| Possible role inside VLM | Compatible only after major narrowing: Thermal, depth, or event-derived frames could appear in a VLM robustness study only if an accessible benchmark and validated preprocessing exist. |
| Reconsideration condition | Sensor-lab supervision plus a preprocessed, Colab-tested benchmark and baseline. |
| Present instruction | Do not pursue as a field; permit only validated modality inputs inside VLM work. |

**Do not reopen from excitement. Use the formal reconsideration protocol.**

**DECISION CARD 8 OF 13**

# Standalone Medical Imaging

|  |
| --- |
| **STATUS** Parked |

| **Decision element** | **Canonical card** |
| --- | --- |
| What it is | Medical imaging AI analyzes radiographs, CT, MRI, ultrasound, pathology slides, retinal images, or other clinical images for classification, detection, segmentation, reconstruction, registration, report generation, and prognosis. |
| How research works | Data: DICOM images, reports, clinical metadata, masks, pathology labels, and patient/study identifiers; Preprocessing: de-identification checks, DICOM windowing, view selection, patient-level splitting, label extraction, uncertainty handling, normalization, and leakage checks; Models: CNNs, vision transformers, U-Nets, detection networks, self-supervised encoders, and medical VLMs; Baselines: clinical rule or simple model, established CNN/ViT/U-Net, published medical baseline, and external-domain or subgroup controls. |
| Why attractive | Medical imaging can improve diagnosis and access and develops rigorous data, calibration, segmentation, and responsible-AI skills. |
| Why unsuitable now | Clinical validation and error interpretation cannot be defended without a domain expert. |
| Strongest blocker | No reliable medical supervisor to validate the problem and reference standard. |
| Possible role inside VLM | Compatible application context: A public chest-X-ray VQA benchmark could test VLM hallucination or calibration, provided the team states that it is a benchmark study, validates labels, and makes no diagnostic or deployment claim. |
| Reconsideration condition | Named clinical supervision plus verified patient-level data, baseline, and evaluation. |
| Present instruction | Use only as a public-data VLM application context with no clinical claim. |

**Do not reopen from excitement. Use the formal reconsideration protocol.**

**DECISION CARD 9 OF 13**

# Standalone Explainable AI (XAI)

|  |
| --- |
| **STATUS** Parked |

| **Decision element** | **Canonical card** |
| --- | --- |
| What it is | Explainable AI studies methods that make model behavior understandable to people. |
| How research works | Inputs: trained models, selected instances, concepts/features, perturbation distributions, and sometimes human tasks or expert annotations; Methods: local surrogates such as LIME [S33], additive feature attributions such as SHAP [S34], gradients, attention analysis, concept probes, counterfactual search, and causal interventions; Baselines: random attribution, gradients, integrated gradients, perturbation methods, simple probes, and task-specific evidence maps; Metrics: faithfulness or deletion/insertion tests, sensitivity, stability, localization, sparsity, completeness, human task performance, and computation cost. |
| Why attractive | XAI aims to support debugging, auditing, scientific discovery, and human decisions. |
| Why unsuitable now | Evaluation validity is too weak for standalone XAI under present conditions. |
| Strongest blocker | No direct, validated ground truth for the intended explanation claim. |
| Possible role inside VLM | Compatible supporting method: Use visual evidence attribution, concept probes, attention intervention, or counterfactual images to test whether a VLM’s answer is grounded. |
| Reconsideration condition | A task-grounded faithfulness protocol with controls and a clear user. |
| Present instruction | Use only within Trustworthy and Reliable VLMs for a named, measurable claim. |

**Do not reopen from excitement. Use the formal reconsideration protocol.**

**DECISION CARD 10 OF 13**

# Generic RAG Applications

|  |
| --- |
| **STATUS** Parked |

| **Decision element** | **Canonical card** |
| --- | --- |
| What it is | Retrieval-augmented generation (RAG) retrieves external documents or passages and conditions a generator on them. |
| How research works | Data: a document corpus, queries, relevance judgments, answers, and evidence spans; Preprocessing: parse documents, preserve metadata, chunk and deduplicate, build sparse/dense indexes, and create leakage-safe query/corpus splits; Models: BM25, dense encoders, late interaction, rerankers, seq2seq or instruction models, query routers, and retrieval planners; Baselines: no retrieval, BM25, dense retrieval, hybrid retrieval, oracle evidence, and prompt/context-matched generator controls. |
| Why attractive | RAG is important for factuality, provenance, updating knowledge, and production AI systems. |
| Why unsuitable now | Generic RAG is an engineering pattern, not a research field or contribution. |
| Strongest blocker | No independently testable gap beyond assembling existing components. |
| Possible role inside VLM | Compatible supporting method: Use image-text or document retrieval to test whether a VLM remains reliable under missing, degraded, contradictory, or shifted evidence. |
| Reconsideration condition | A verified multimodal retrieval failure, public benchmark, strong controls, and direct evaluation. |
| Present instruction | Use only if necessary for a named VLM research question. |

**Do not reopen from excitement. Use the formal reconsideration protocol.**

**DECISION CARD 11 OF 13**

# Generic Agentic-AI Applications

|  |
| --- |
| **STATUS** Parked |

| **Decision element** | **Canonical card** |
| --- | --- |
| What it is | Agentic AI uses a model to choose actions, call tools, observe results, update plans, and continue toward a goal. |
| How research works | Data/environment: tasks, tool schemas, executable websites or repositories, initial state, success conditions, and action logs; Architecture: observe, reason/plan, act, receive feedback, update memory, and stop; Baselines: direct prompting, fixed workflow, retrieval-only, ReAct, planning/search, and tool-ablation controls; Metrics: exact task success, steps, invalid actions, recovery rate, latency, token/API cost, safety violations, and reproducibility across runs. |
| Why attractive | Agent research matters for dependable automation and teaches orchestration, evaluation, software systems, and model behavior. |
| Why unsuitable now | Framework integration is easy, while rigorous, reproducible agent evaluation is expensive. |
| Strongest blocker | No stable, low-cost executable benchmark that isolates a new scientific mechanism. |
| Possible role inside VLM | Compatible only after major narrowing: A multimodal agent could be used to test whether visual misperception propagates into tool actions, but the research claim must be about VLM reliability and the environment must provide exact success/failure labels. |
| Reconsideration condition | Reproducible environment, open-model budget, strong baselines, and one isolated contribution. |
| Present instruction | Do not build a generic agent thesis; use only a minimal agent layer for a VLM reliability question. |

**Do not reopen from excitement. Use the formal reconsideration protocol.**

**DECISION CARD 12 OF 13**

# Generic Image Classification

|  |
| --- |
| **STATUS** Parked |

| **Decision element** | **Canonical card** |
| --- | --- |
| What it is | Image classification maps an image to one or more labels. |
| How research works | Data: labeled images, class taxonomy, patient/source/group identifiers, and sometimes unlabeled pretraining data; Preprocessing: deduplication, source-aware splitting, resizing, augmentation, class balancing, and leakage checks; Models: CNNs such as ResNet [S47], vision transformers, self-supervised encoders, linear probes, and lightweight networks; Baselines: majority/classical baseline, pretrained ResNet/ViT, simple augmentation, frozen-feature linear probe, and closest published method. |
| Why attractive | Classification is foundational, easy to prototype, and useful for learning experiment design. |
| Why unsuitable now | The implementation is feasible, but the generic contribution is too weak and saturated. |
| Strongest blocker | No defensible novelty beyond applying a standard model to a labeled dataset. |
| Possible role inside VLM | Compatible supporting method: Image classification may provide a visual-only baseline, an AI-generated image detector, or a corruption/shift probe inside Rank 1, 2, or 3. |
| Reconsideration condition | A verified reliability, shift, or efficiency question with strong controls. |
| Present instruction | Use only as a baseline or task inside a named VLM lane. |

**Do not reopen from excitement. Use the formal reconsideration protocol.**

**DECISION CARD 13 OF 13**

# Generic Object Detection

|  |
| --- |
| **STATUS** Parked |

| **Decision element** | **Canonical card** |
| --- | --- |
| What it is | Object detection predicts what objects are present and where they are, usually with bounding boxes; instance segmentation also predicts masks; tracking links detections over time. |
| How research works | Data: images, boxes/masks, category ontology, crowd/ignore regions, source metadata, and sometimes video identities; Preprocessing: annotation QA, image/source splitting, resizing, augmentation, class-frequency analysis, and format conversion; Models: Faster/Mask R-CNN, RetinaNet, YOLO families, DETR-like transformers, open-vocabulary detectors, and lightweight variants; Baselines: pretrained detector, simple fine-tune, frozen backbone, size-matched detector, and closest method. |
| Why attractive | Detection is useful for production vision and develops annotation, localization, training, and deployment skills. |
| Why unsuitable now | A generic fine-tuned detector is an implementation project with weak novelty. |
| Strongest blocker | No research contribution beyond standard detector training. |
| Possible role inside VLM | Compatible supporting method: Use a detector to verify object presence in a VLM hallucination protocol, compare visual-only and VLM robustness, or measure open-vocabulary grounding. |
| Reconsideration condition | A verified grounding, shift, long-tail, or efficiency problem with direct controls. |
| Present instruction | Use as a validated VLM grounding/evaluation baseline only. |

**Do not reopen from excitement. Use the formal reconsideration protocol.**

# Controlling Close

|  |
| --- |
| **FINAL BOUNDARY** Multimodal / Vision-Language Learning and Systems remains the frozen parent field. The three ranked VLM lanes remain the only authorized lanes for current topic discovery. Parked fields are retained for future reference but must not consume present research time. Rejected fields, if any are recorded in a future revision, must not be reopened without materially new evidence. Supporting methods may be used only when they directly serve a defensible VLM research question. The final thesis topic still requires separate dataset, baseline, evaluation, compute, contribution, and fallback validation. This report does not claim that excluded fields are scientifically weak; it records why they are currently inferior choices under the researcher’s constraints. |

*Consistency audit completed against Canonical Thesis Field Specification v1.0: all eight canonical parked groups are preserved; grouped fields are separated only for analysis; no rejected or narrowed status was invented; unassessed requested fields remain unassessed; the frozen VLM parent field and lane ranking are unchanged; every dossier answers what, how, and why; score justifications and concrete reconsideration conditions are included; technical claims are supported by curated primary or official sources with direct links.*
---

# Temporary Parking Update 14 September 2026

| Decision | Record |
| --- | --- |
| **Status** | **Parked for the current topic-discovery cycle** |
| **Areas** | Continual learning; AI memory systems; long-context windows; long-term planning; hierarchical planning. |
| **Reason** | The cross-report evidence audit did not establish a pilot-ready, scope-compatible, reproducible thesis contribution in any of these five areas under the current VLM/MLLM constraints. |
| **Scope effect** | No change. The frozen parent remains Multimodal / Vision-Language Learning and Systems. The ranked lanes remain trustworthy and reliable VLMs; VLM generalization, adaptation and distribution shift; and efficient and scalable VLMs. |
| **Research effect** | Do not spend current topic-discovery time on these five areas or treat a previously proposed pilot as approved. |
| **Reconsideration condition** | Reopen only through a documented candidate-level case showing a verified gap, public data, reproducible baseline, valid evaluation, realistic compute plan, and a direct contribution inside the frozen VLM field. |
| **Not a rejection** | This is a time-bounded prioritization decision. It does not claim that the areas are scientifically unimportant or permanently incompatible with VLM research. |

This update supersedes the 14 September 2026 provisional ranking that left a narrow long-context or multi-image reliability candidate under investigation. That candidate is now parked with the other four areas. The thesis topic remains unfrozen.
