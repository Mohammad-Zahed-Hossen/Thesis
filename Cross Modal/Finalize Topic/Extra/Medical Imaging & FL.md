Searched for files: *Medical Imaging*
Listed directory Medical%20Imaging%20&%20FL
Viewed Federated%20Learning%20%28non-VLM%29.md:1-176
Viewed Federated%20Learning%20+%20Medical%20Vision-Language%20Models%20%28VLM%20variant%29.md:1-204
Viewed Medical%20Imaging%20without%20VLM.md:1-185
Viewed Medical%20Imaging%20With%20VLM.md:1-191
Viewed Medical%20Imaging%20With%20&%20Without%20VLM.md:1-800
Viewed Medical%20Imaging%20With%20&%20Without%20VLM.md:620-1334
Viewed Adversarial%20Thesis%20Audit_%20Medical%20Imaging%20vs%20Federated%20Learning.md:1-519
Viewed Adversarial%20Thesis%20Audit_%20Medical%20Imaging%20vs%20Federated%20Learning.md:230-519

# Critical Thesis Decision Audit: Medical Imaging & Federated Learning

**Auditor Role:** Senior Thesis Research Auditor & Adversarial Reviewer  
**Scope of Review:** Complete adversarial audit of all 6 research reports in `Medical Imaging & FL`  
**Lab & Resource Constraints:** 3 final-year CSE undergraduate researchers; compute limited to local Ryzen 5 5600G (8 GB RAM, no local CUDA) and Google Colab Pro ($\le$16 GB VRAM T4/V100/A100); public/credential-free data only; ~months to thesis defense  
**Reference Baseline:** Researcher’s held thesis direction in Trustworthy Multimodal Foundation Models (Causal conflict verbalization and source arbitration in VLMs)

---

## 1. Evidence Map Across All Reports

Consolidating the findings across all 6 files (`Federated Learning (non-VLM).md`, `Federated Learning + Medical Vision-Language Models (VLM variant).md`, `Medical Imaging without VLM.md`, `Medical Imaging With VLM.md`, `Medical Imaging With & Without VLM.md`, and `Adversarial Thesis Audit_ Medical Imaging vs Federated Learning.md`):

```
                                  [AUDIT CORPUS: 6 FILES]
                                             │
      ┌──────────────────────────────────────┼──────────────────────────────────────┐
      ▼                                      ▼                                      ▼
[Medical Imaging (Non-VLM)]             [Federated Learning]                [Medical VLMs / Multimodal]
• Saturated: CNN vs ViT,             • Saturated: FedAvg vs FedProx       • Saturated: VLM calibration
  HAM10000 classification,             on Dirichlet label skew              (MVC-Bench), hallucination
  in-distribution calibration        • Non-VLM Niche: Fed conformal       • Occupied: Multi-cohort CXR
• Surviving Niche: Selective           risk control (Fed-CRC-Seg)           Fed-LoRA (arXiv:2609.02101)
  classification (AUGRC) under       • VLM Niche: Fed-LoRA calibration    • Open Point: Causal conflict
  sensor shift (dermoscopy)            (Empty cell, high friction)          verbalization (Held RQ)
```

### 1. Research Areas Investigated
* **Area A: Medical Image Classification & Selective Prediction (Non-VLM):** Confidence calibration under distribution shift (demographic, sensor/acquisition, synthetic corruption); selective classification (prediction with abstention/reject option); shortcut learning mitigation via post-hoc recalibration.
* **Area B: Non-VLM Federated Learning (Medical FL):** Site-conditional calibration and conformal risk control (CRC) across decentralized clinical sites; worst-site/worst-client statistical error bounding; multi-site non-IID optimization drift (SCAFFOLD vs FedAvg/FedBN).
* **Area C: Federated Learning + Medical VLMs:** Federated parameter-efficient fine-tuning (Fed-LoRA / FlexLoRA) of medical vision-language foundation models (BiomedCLIP, Qwen2-VL) across multi-center cohorts; calibration and fairness disparity across decentralized clients.
* **Area D: Centralized Medical VLMs:** Medical VQA confidence grounding under progressive visual degradation; multimodal contradiction detection and evidence arbitration (image vs text context conflicts); selective triage and clinical hallucination detection.

### 2. Candidate Research Questions Proposed Across Files
* **RQ-M1 / Candidate 1:** Failure of selective classification ranking (AUGRC) under sensor shift (dermoscopy $\to$ clinical smartphone photography: ISIC 2020 $\to$ PAD-UFES-20 / DDI).
* **RQ-M2:** Disentangling clinical prevalence shift from sensor shift in medical post-hoc recalibration.
* **RQ-M3:** Impact of unstratified patient records and duplicate leakage on published selective prediction baselines.
* **RQ-M4 / RQ-5:** Shortcut learning invariance vs acquisition-specific failure under border/marker perturbations.
* **RQ-FL1 / RQ 1 (FL non-VLM):** Boundary conditions of site-conditional conformal risk control (risk-curve shrinkage) under partial client participation on FeTS-2022.
* **RQ-FL2 / RQ-FL5:** Impact of federated aggregation / federated LoRA on worst-client calibration disparity and selective prediction.
* **RQ-FL3 / RQ 4 (FL non-VLM):** Sample-complexity wall for site-conditional calibration in 2D medical FL simulations.
* **RQ-VLM-A / R1:** Causal conflict verbalization as an arbitration switch in medical VQA (the medicalized twin of the held general VLM question).
* **RQ-VLM-B:** Confidence degradation under progressive visual evidence removal (blur/masking) in medical VLMs.

### 3. Papers Repeatedly Cited Across Reports
* **Fed-CRC-Seg (arXiv:2606.20115, June 2026, Shahid):** The anchor for all FL calibration claims; proves pooled conformal risk control violates coverage at 40% of institutions on FeTS-2022; proposes risk-curve shrinkage ($n_0=19$).
* **AUGRC Metric (NeurIPS 2024, arXiv:2407.01032, Traub et al.):** Proves standard AURC is mathematically flawed for comparing base classifiers; formalizes AUGRC and generalized selective risk.
* **Kozachok et al. (arXiv:2607.26765, July 2026):** Establishes contamination-controlled protocol across 6 dermoscopic sources (25,903 images) and shows photometric augmentations yield $+0.053$ out-of-domain ROC-AUC.
* **Prevalence Calibration (arXiv:2609.07922, 2025, Kina & Petersen):** Demonstrates post-hoc logit recalibration raises misaligned shortcut group AUROC from 0.23 to 0.73 on CheXpert/SIIM-ACR.
* **MVC-Bench (arXiv:2608.27004, 2026):** Centralized benchmark of 8 medical VLMs across 1,638 runs; proves 0/30 transfer settings exhibit positive calibration rank-transfer across distribution shift.
* **Fed-LoRA BiomedCLIP (arXiv:2609.02101, Sept 2026):** Federates BiomedCLIP across 4 international CXR cohorts (USA, Vietnam, Spain); proves product-space (FlexLoRA) aggregation prevents a ~0.097 AUC drop over naive averaging.
* **MC-CXR (arXiv:2608.24118, 2026):** Paired CXR perturbation benchmark; shows misleading text flips 45.6–78.1% of correct image decisions; Appendix D pilot shows verbalizing contradiction alone does not alter decisions.
* **MedFL-Stress (arXiv:2605.09025, May 2026):** Stress-tests FedAvg, FedProx, FedBN on BraTS 2020 under synthetic MRI appearance shifts; FedBN closes worst-hospital gap by 41%.

### 4. Datasets Assessed & Their Viability
* **ISIC 2020 (33,126 images, 2,056 patients):** Directly downloadable, CC BY-NC 4.0. Contains verified `patient_id` and an official 425-image duplicate list. **Viable for 2D training.**
* **ISIC 2019 (25,331 images):** Subsumes HAM10000 entirely; contains `lesion_id` but lacks unified `patient_id`. **Viable only with strict deduplication.**
* **PAD-UFES-20 (2,298 images, 1,373 patients):** Clinical smartphone camera photos, CC BY 4.0. **Viable as external sensor shift test.**
* **DDI (Diverse Dermatology Images, 656 images):** Biopsy-confirmed, Stanford AIMI research agreement, Fitzpatrick skin tones I–VI. **Viable as external demographic shift test.**
* **FeTS-2022 (1,251 train / 219 val 3D mpMRI subjects):** The **only** public medical dataset with genuine institutional client partitions (23–33 institutions). **High friction:** Gated behind Synapse registration (`syn28546456`) with documented manual approval delays; 3D volumetric data.
* **CheXpert / NIH ChestXray14 / MIMIC-CXR:** CheXpert requires Stanford AIMI approval; NIH has noisy text-mined labels; MIMIC-CXR requires PhysioNet CITI training, credentialing, and DUA. **MIMIC is rejected on timeline/compliance grounds.**
* **SLAKE / VQA-RAD / GMAI-MMBench:** Curated medical VQA sets. Public and small, but single-site; GMAI-MMBench is Apache-2.0.

### 5. Models and Baselines
* **2D CNNs:** ResNet-18 (11.2M params), DenseNet-121 (7.0M params). Memory-efficient (3.8 GB VRAM on T4, 45s/epoch).
* **Uncertainty & Calibration:** Maximum Softmax Probability (MSP), Temperature Scaling, Vector Scaling, Monte Carlo Dropout (15 passes), 5-member Deep Ensembles, Split-Conformal Prediction (APS/RAPS).
* **FL Algorithms:** FedAvg, FedProx, FedBN, Fed-CRC-Seg (risk-curve shrinkage), FlexLoRA (SVD-based product-space adapter merge).
* **VLMs:** BiomedCLIP (ViT-B/16), Qwen2-VL-2B / Qwen3VL-2B (Apache-2.0, fits T4 in 4-bit QLoRA), MedGemma-4B (gated by HF Health ToS), LLaVA-Med (LLaMA license risks).

### 6. Summary of Synthesis: Single-Report Claims vs Independent Support
* **Multi-report consensus:** Generic medical image classification and standard FL optimization (FedAvg vs FedProx on Dirichlet splits) are completely saturated; public dermoscopy archives have severe contamination; FeTS-2022 is the only defensible multi-institution FL dataset; centralized VLM calibration is already benchmarked and fails under shift (MVC-Bench); VLM-based FL is an occupied dead-end for an undergraduate thesis.
* **Unsupported / Over-optimistic single-report claims:** 
  * `Federated Learning (non-VLM).md` claims FeTS-2022 access and calibration-only evaluation on Colab T4 is an easy "2-week gated pilot," ignoring Synapse manual approval lead times and the fact that an empirical evaluation on pre-extracted weights provides almost no algorithmic novelty over Shahid (2026).
  * `Medical Imaging without VLM.md` frames AUGRC evaluation on ISIC $\to$ PAD-UFES as a self-contained clinical contribution, glossing over the fact that it is fundamentally a computer vision benchmark audit using medicine as a test substrate.

---

## 2. Adversarial Gap Audit

| Claimed Research Gap | Supposed Anchor Paper(s) | Explicit or Inferred? | Do Cited Papers Actually Support the Claim? | Could Another Paper Already Answer It? | Genuinely Scientific vs Incremental Benchmark? | Negative Result Value | Audit Classification |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| **1. Site-conditional calibration breaks under FL; risk-curve shrinkage fixes it** | Shahid (arXiv:2606.20115, June 2026, *Fed-CRC-Seg*) | Explicit in Shahid | **Yes.** Shahid demonstrates pooled CRC violates coverage at 40% of institutions on FeTS-2022 and shrinkage fixes it. | **Already answered by Shahid.** The core gap is closed. Any extension to partial participation is a minor operational parameter sweep. | Merely another parameter variation / boundary check on Shahid’s code. | **Low:** If partial participation doesn't break it, Shahid's method is just slightly more robust. | **FALSE / ALREADY OCCUPIED** |
| **2. Post-hoc calibration fails to preserve selective prediction (AUGRC) under physical sensor shift** | Traub et al. (NeurIPS 2024, arXiv:2407.01032); Kozachok et al. (arXiv:2607.26765, 2026) | Inferred by combining Traub's metric with Kozachok's shift protocol | **Partially.** Traub tested histopathology (CAMELYON-17) in-distribution; Kozachok tested dermoscopy OOD but reported AUC only. | Highly likely that computer vision selective classification papers (e.g., PLEX, ImageNet-C selective benchmarks) already show confidence ranking inverts under sensor corruption. | **Benchmark application:** Applying an existing metric (AUGRC) to existing datasets (ISIC/PAD-UFES). No new algorithm. | **Moderate-High:** Confirms whether post-hoc recalibration can or cannot act as a triage safety net across camera hardware. | **PLAUSIBLE (Narrow)** |
| **3. Prevalence recalibration mitigates shortcut learning in medical imaging** | Kina & Petersen (arXiv:2609.07922, 2025) | Explicit in Kina & Petersen | **Yes.** Shows logit adjustment raises misaligned group AUROC from 0.23 to 0.73 on CheXpert. | **Already answered by Kina & Petersen.** Testing it on dermatoscope borders instead of CXR demographic tags is purely a dataset swap. | Merely another dataset application. | **Zero:** If it fails on physical borders, it just confirms base-rate adjustments don't fix spatial feature shortcuts. | **FALSE / ALREADY OCCUPIED** |
| **4. Federated LoRA of Medical VLMs exhibits worst-client calibration disparity** | arXiv:2609.02101 (BiomedCLIP FL); arXiv:2605.08992 (*FM Fairness Paradox*) | Inferred across unrelated domains | **No.** 2609.02101 did not measure calibration (AUC only). 2605.08992 studied text classification with DistilBERT on synthetic Dirichlet splits. | MVC-Bench (arXiv:2608.27004) already shows medical VLMs miscalibrate centrally under shift. The "federated aggregation causes this" claim is completely unproven. | **Manufactured intersection:** Stacking FL + VLM + Medical + Calibration without proof that aggregation is the causal driver. | **Low:** If null, central shift explains everything and FL added only engineering debt. | **WEAK** |
| **5. Causal verbalization resolves multimodal conflict arbitration in medical VLMs** | MC-CXR (arXiv:2608.24118, 2026, App. D); GACL (arXiv:2606.05161) | Inferred from MC-CXR's confounded pilot | **Yes, but with negative prior.** MC-CXR tested rule + naming on GPT-5.5; naming alone showed zero effect ($p > 0.05$). GACL showed audio "encoded-but-overridden" mechanism. | The general-domain VLM literature (SameSemantics, WhichSourceWins) addresses conflict, but none isolate verbalization as a causal intervention. | **Genuinely scientific:** Directly adjudicates whether model self-explanations are causal computation vs post-hoc rationalization. | **Exceptional:** A null proves verbalization is decorative rationalization; a positive proves prompt-level arbitration control. | **VERIFIED (as General VLM question; UNRESOLVED / Confounded in Medical)** |
| **6. Medical VLM confidence tracks visual evidence loss independently of correctness** | MVC-Bench (arXiv:2608.27004); DualRead (arXiv:2609.06419, Sept 2026) | Inferred | **No.** DualRead already developed CCG-AUC to measure whether confidence tracks counterfactual image substitution on SLAKE/VQA-RAD. | **Heavily occupied by DualRead (2609.06419) and JustHowSure (2606.27023).** | Benchmark replication / minor perturbation variation. | **Low:** Confirms existing findings that VLM confidence is untethered from pixels. | **FALSE / ALREADY OCCUPIED** |

---

## 3. Strongest Surviving Research Questions

Only two candidates survive the initial screening as defensible undergraduate research directions. Here is their adversarial breakdown:

### Candidate 1 (Medical Imaging / Trustworthy ML): RQ-M1
* **RQ:** Under physical acquisition sensor shift (dermoscopy $\to$ clinical smartphone photography), does post-hoc confidence scoring preserve sample-level risk-coverage ordering (AUGRC), or does selective prediction fail specifically where automated clinical referral is required?
* **Failure Mode:** A dermatological triage model deployed on smartphone photos assigns high confidence to out-of-distribution diagnostic errors, causing selective risk to inflate catastrophically at operating coverage (e.g., 80%), while temperature scaling fails to fix the ranking.
* **Scientific Variable:** 
  * *Manipulated (IV):* Domain shift condition (In-distribution patient-held-out ISIC 2020 vs external clinical sensor shift PAD-UFES-20 vs skin-tone shift DDI) $\times$ Confidence estimator (MSP, Temperature Scaling, MC-Dropout, Deep Ensembles).
* **Outcome:** Sample-level generalized selective risk and Area Under the Generalized Risk-Coverage curve (AUGRC), selective risk at fixed coverage ($\kappa \in \{0.7, 0.8, 0.9\}$), and ECE.
* **Closest Work:** Traub et al. (NeurIPS 2024, AUGRC formulation); Kozachok et al. (arXiv:2607.26765, 2026, dermoscopy OOD augmentations).
* **Remaining Gap:** Traub formalized AUGRC in-distribution; Kozachok evaluated OOD accuracy (AUC) only. Neither evaluated whether confidence scoring functions maintain sample error-ranking across physical camera shifts under strict contamination filtering.
* **Evaluation:** Train DenseNet-121 and ResNet-18 on patient-partitioned ISIC 2020 (deduplicated). Fit temperature scaling on in-distribution validation. Evaluate AUGRC across clean test, PAD-UFES-20, and DDI.
* **Negative-Result Value:** High. If AUGRC is invariant to sensor shift and temperature scaling preserves ranking, it disproves the prevailing clinical assumption that acquisition shift inevitably breaks selective triage safety nets.
* **Feasibility:** High. Single T4 GPU requires ~5.25 hours total compute. Datasets are open and credential-free.

### Candidate 2 (Federated Learning / Distributed Systems): RQ-FL1
* **RQ:** How resilient is site-conditional federated conformal risk control (risk-curve shrinkage) to partial client participation, and at what local sample size threshold $n_k$ does shrinkage fail to prevent worst-site false-negative-rate (FNR) violations?
* **Failure Mode:** In a distributed clinical network, intermittent connectivity results in only 20–40% of hospitals participating in calibration rounds. The central coordinator aggregates an incomplete empirical risk prior, causing low-volume clinics to violate their pre-declared clinical risk budgets ($\alpha = 0.10$).
* **Scientific Variable:**
  * *Manipulated (IV):* Client participation fraction $C \in \{0.2, 0.4, 0.7, 1.0\}$ $\times$ shrinkage hyperparameter $n_0 \times$ local institutional sample size $n_k$.
* **Outcome:** Worst-site False Negative Rate (FNR), percentage of violating institutions ($> \alpha$), and mean-to-worst coverage gap.
* **Closest Work:** Shahid (arXiv:2606.20115, June 2026, *Fed-CRC-Seg*).
* **Remaining Gap:** Shahid evaluated risk-curve shrinkage on FeTS-2022 assuming 100% client availability. The stability of conformal guarantees under client dropout and low local sample regimes ($n_k < 15$) was not investigated.
* **Evaluation:** Run Monte Carlo client subsampling simulations over pre-computed FeTS-2022 validation prediction tensors across 20 institutions. Sweep participation rates and measure empirical FNR across 50 trials.
* **Negative-Result Value:** Moderate-High. If shrinkage is robust down to $C=0.2$, it proves that federated conformal guarantees do not require strict participation quotas.
* **Feasibility:** Gated/Fragile. Requires Synapse manual approval for FeTS-2022 (`syn28546456`). If using pre-computed validation tensors, compute is $<2$ GPU hours. If forced into a 2D simulated federation, feasibility is high (~20 GPU hours) but clinical validity collapses.

---

## 4. The "Why FL?" Test

For every FL candidate in the audit corpus, we ask:
> **"If I remove Federated Learning, does the underlying scientific question remain?"**

```
[Underlying Statistical Question]
"Does pooled calibration fail local worst-site error bounds under multi-site distribution shift?"
                                      │
                                      ▼
                        Can we pool the data centrally?
                                      │
                 ┌────────────────────┴────────────────────┐
                 ▼                                         ▼
               [YES]                                     [NO]
        Centralized Shift /                      True Privacy / FL Constraint
       Group Robustness Question                  Requires Non-IID Aggregation
  (FL adds ONLY distributed overhead)             AND Multi-Site Provenance
```

### 1. Analysis of Candidate FL1 (Site-Conditional Conformal Risk Control)
* **If FL is removed:** The question becomes: *"Under multi-center distribution shift, does pooled conformal calibration fail worst-site coverage compared to hierarchical/shrinkage Bayes calibration?"*
* **Does the scientific question survive?** **YES.** Hierarchical conformal prediction and group-conditional calibration under domain shift are well-known centralized statistics problems.
* **What does FL specifically add?** FL adds one precise constraint: **privacy-preserving communication**. Sites cannot send raw continuous non-conformity scores $(s_1, \dots, s_n)$ to the server; they can only transmit discretized empirical risk curves $\hat{R}_k(\lambda)$ or local scalar summaries.
* **Verdict:** FL adds genuine methodological value **only** if the inquiry is strictly bounded to the communication constraint (scalar curves vs raw scores) and partial client participation under decentralized aggregation.

### 2. Analysis of Candidate FL2 / FL5 (Federated LoRA / Calibration Disparity)
* **If FL is removed:** The question becomes: *"Does PEFT (LoRA) miscalibrate under cross-site distribution shift?"*
* **Does the scientific question survive?** **YES.** In fact, MVC-Bench (arXiv:2608.27004) already answered it centrally across 1,638 runs.
* **What does FL add?** Nothing except parameter averaging noise (FedAvg). The reports fail to prove that federated aggregation causes a unique miscalibration phenomenon that centralized training at matched data volume does not produce.
* **Verdict:** **FL IS UNNECESSARY AND UNJUSTIFIED.** It introduces distributed systems complexity to mask what is fundamentally a standard domain-shift problem.

### 3. Client Partitioning Reality Check
* **Real Multi-Site Heterogeneity:** Exists **only** in FeTS-2022 (23–33 real clinical institutions with native acquisition differences and extreme sample count skews, where ~61% of sites have $<15$ cases).
* **Synthetic Partitioning (The Simulation Trap):** Partitioning HAM10000, ISIC, or CXR datasets via Dirichlet label skew ($\alpha = 0.1$) is an artificial artifact. Neurocomputing 2026 (`doi:10.1016/j.neucom.2026.135005`) explicitly proved that Dirichlet label skew ranks FL algorithms differently than authentic acquisition shifts.
* **Audit Rule:** Claims about "hospital federations" based on artificially split public datasets are scientifically illegitimate and must not be accepted.

---

## 5. The "Medical Imaging Is Not Enough" Test

For Candidate M1 (Dermoscopy Selective Classification), we ask:
> **"Is medical imaging itself necessary to the scientific question, or is it simply being used as a convenient dataset?"**

```
                    [Candidate M1: Selective Prediction Under Shift]
                                          │
                  Is the question clinically distinct or methodological?
                                          │
       ┌──────────────────────────────────┴──────────────────────────────────┐
       ▼                                                                     ▼
[Genuine Medical Necessity]                                       [Trustworthy ML Core]
• Requires radiologist-in-the-loop                                • Failure of confidence ranking under shift
• Complex multi-slice 3D spatial reasoning                        • Ineffectiveness of post-hoc monotonic scaling
• Modality-specific biological physics                            • Selective risk evaluation via AUGRC
       │                                                                     │
       └───────────────────────────────┬─────────────────────────────────────┘
                                       ▼
                       [AUDIT VERDICT: 85% TRUSTWORTHY ML]
        Dermoscopy is merely a convenient 2D benchmark with sensor tags.
```

1. **Deconstructing the Contribution:**
   * The core phenomenon being tested is: *Does post-hoc temperature scaling fail to correct sample misranking under physical distribution shift, causing selective risk (AUGRC) to inflate?*
   * This is a **Trustworthy Machine Learning / Distribution Shift** question. It is not unique to skin lesions; it applies identically to autonomous driving camera shifts, satellite sensor shifts, or industrial defect inspection.
2. **Why Dermoscopy Was Chosen:**
   * It is a convenient public 2D image archive where camera transitions (dermatoscope $\to$ smartphone) happen to be labeled.
   * There is no specialized biological modeling, no clinical workflow integration, and no radiologist-in-the-loop evaluation.
3. **The Viva Vulnerability:**
   * In a rigorous computer science defense, examiners will ask: *"Why is this a medical thesis rather than a standard benchmark evaluation of Traub et al.'s AUGRC metric on out-of-domain computer vision?"*
   * Framing this work as a "medical AI diagnostic system" will invite immediate clinical validity challenges (biopsy ground-truth errors, label taxonomy mismatches between ISIC and PAD-UFES). Framing it honestly as an empirical safety audit of selective classification under sensor shift reduces it to an incremental benchmarking paper.

---

## 6. Feasibility Kill Test

Evaluating both surviving candidates against the hard operational constraints of a final-year undergraduate team:

| Feasibility Dimension | Candidate M1: Selective Dermoscopy (Non-VLM) | Candidate FL1: Conformal FL (FeTS-2022) |
| :--- | :--- | :--- |
| **1. Dataset Availability** | **High.** ISIC 2020, PAD-UFES-20, and DDI are completely public. | **Low.** FeTS-2022 is restricted to Synapse challenge participants. |
| **2. Licensing / Access** | **Immediate.** Direct download; CC BY-NC 4.0 and CC BY 4.0. | **Delayed.** Requires Synapse account, challenge registration, manual admin approval (`syn28546456`). Synapse forums show unanswered/delayed requests. |
| **3. Model Availability** | **Immediate.** `torchvision.models` (DenseNet-121, ResNet-18). | **Moderate.** Pretrained 3D U-Net weights on GitHub (`FeTS-AI/Models`); open Flower simulation scripts. |
| **4. GPU / VRAM Envelope** | **Trivial.** 3.8 GB VRAM on NVIDIA T4; FP16 batch size 64. | **Conditional.** Calibration-only on pre-extracted feature tensors: $<4$ GB VRAM. Training 3D U-Net from scratch: **FAILS** ($>16$ GB VRAM, days of compute). |
| **5. Experiment Count** | 2 architectures $\times$ 3 seeds $\times$ 3 test sets $\times$ 4 calibrators = **36 evaluation runs**. | 4 participation rates ($C$) $\times$ 5 shrinkage levels ($n_0$) $\times$ 50 Monte Carlo trials = **1,000 statistical runs** (inference only). |
| **6. Training Complexity** | Low. Standard 2D cross-entropy training (~15 min/run). | Zero (if using pre-computed tensors) to Extreme (if training 3D MRI). |
| **7. Evaluation Complexity** | Moderate. Requires exact implementation of AUGRC metric (Traub et al. code). | High. Requires per-site FNR curve integration and empirical Bayes shrinkage math across 20 silos. |
| **8. Leakage Risk** | **Critical Operational Hazard.** Must eliminate 425 official ISIC duplicates, enforce strict `patient_id` splits, and prevent HAM10000 overlap. | Moderate. Must maintain strict silo separation between calibration and evaluation splits. |
| **9. Implementation Burden** | Manageable applied CV pipeline (~300 lines PyTorch). | High risk of getting trapped in FL simulation scaffolding (Flower/Ray memory leaks). |
| **10. Reproducibility** | High. Deterministic data loaders and fixed seeds. | Fragile. Distributed seed synchronization across simulated processes is error-prone. |

> **Undergraduate Thesis Feasibility Verdict:**
> * **Candidate M1:** **FEASIBLE.** An undergraduate team can complete and defend this within 8–10 weeks.
> * **Candidate FL1:** **HIGH RISK OF SCHEDULE FAILURE.** A single administrative delay on Synapse or a single distributed simulation bug in Flower/Ray will paralyze the team for weeks.

---

## 7. Cross-File Contradiction Audit

The 6 files contain sharp internal disagreements that must not be silently smoothed over:

| Topic | File A Says | File B Says | Actual Evidence from Corpus | Resolution / Ground Truth |
| :--- | :--- | :--- | :--- | :--- |
| **FL Non-VLM Status** | `Federated Learning (non-VLM).md`: **"REOPEN FOR A TIME-BOXED, GATED PILOT"** | `Adversarial Thesis Audit_ Medical Imaging vs FL.md`: **"Candidate FL1 is assigned RESERVE"**; `Medical Imaging With & Without VLM.md`: **"Reject for primary thesis"** | FeTS-2022 is access-gated; Shahid (June 2026) already published the headline claim; FL simulation is high friction. | **RESERVE / DO NOT REOPEN.** The reopen verdict in the non-VLM report was based on an over-optimistic 2-week schedule assumption that ignored Synapse red tape. |
| **FeTS-2022 Compute Feasibility** | `Federated Learning (non-VLM).md`: FeTS-2022 calibration-only on Colab T4 is **"Yes, comfortably (minutes-hours)"** | `Adversarial Thesis Audit...md`: Training 3D U-Net from scratch **"exceeds single-GPU Colab Pro limits, triggering a compute failure (kill gate)"** | Pretrained weights exist on GitHub (`FeTS-AI/Models`), but training from scratch requires 128³ patches on 3D mpMRI. | **COMPUTE KILL GATE APPLIES TO TRAINING.** Only inference on pre-extracted tensors is feasible. If access to pre-trained weights or Synapse fails, the project cannot be rescued locally. |
| **Dermoscopy Novelty vs Saturation** | `Medical Imaging without VLM.md`: Candidate 1 is a **"defensible undergraduate question that can survive a viva"** | `Medical Imaging With & Without VLM.md`: **"MEDICAL IMAGING WITHOUT VLM DOES NOT CURRENTLY BEAT THE HELD VLM DIRECTION"** | Traub et al. (2024) already published the AUGRC metric; Kozachok et al. (2026) already published contamination-controlled dermoscopy OOD splits. | **INCREMENTAL BENCHMARK AUDIT.** It is scientifically defensible as an empirical stress test, but conceptually secondary to the held VLM research question. |
| **Public Multi-Site VLM Data** | `FL + Medical VLM.md`: Proposes evaluating federated LoRA on medical VQA sets (VQA-RAD, SLAKE) | `FL + Medical VLM.md` (Section 5): **"There is NO public dataset with real multi-site labels AND image+text VQA content."** | CXR cohorts have real sites but no open-ended text; VQA datasets have text but are single-center. | **FATAL DATASET GAP FOR FL-VLM.** Any federated VLM study on VQA-RAD or SLAKE is forced to use synthetic client partitioning, violating the realism requirement. |
| **Shortcut Mitigation via Calibration** | `Medical Imaging without VLM.md`: Proposes shortcut learning calibration as a candidate topic | `Adversarial Thesis Audit...md`: **"Kina & Petersen (arXiv:2609.07922, 2025) heavily shadows the core conceptual insight... Weak Separation."** | Kina & Petersen already proved logit recalibration raises misaligned group AUROC from 0.23 to 0.73 on CheXpert. | **REJECT SHORTCUT TOPIC.** The conceptual discovery is published; testing it on skin markers is trivial parameter replication. |

---

## 8. Evidence Quality Audit

Classifying the core factual assertions across the reports into evidentiary tiers:

```
┌────────────────────────────────────────────────────────────────────────────┐
│ HIGH CONFIDENCE (Supported by multiple strong primary sources & verified)   │
├────────────────────────────────────────────────────────────────────────────┤
│ • Naive pooled conformal calibration fails worst-site coverage on FeTS-2022│
│   (Fed-CRC-Seg, arXiv:2606.20115).                                         │
│ • Standard AURC is mathematically flawed; AUGRC isolates failure detection  │
│   (Traub et al., NeurIPS 2024).                                            │
│ • Public dermoscopy benchmarks suffer from catastrophic nesting: ISIC 2019  │
│   subsumes HAM10000; ISIC 2020 has 425 duplicate images.                   │
│ • Federated LoRA on CXR cohorts requires product-space aggregation          │
│   (FlexLoRA) to prevent a 0.097 AUC drop (arXiv:2609.02101).               │
│ • Centralized medical VLMs exhibit zero positive calibration rank-transfer  │
│   under shift (MVC-Bench, arXiv:2608.27004).                               │
└────────────────────────────────────────────────────────────────────────────┘
┌────────────────────────────────────────────────────────────────────────────┐
│ MEDIUM CONFIDENCE (Supported by literature but incomplete / indirect)       │
├────────────────────────────────────────────────────────────────────────────┤
│ • FedBN closes inter-hospital Dice gap by 41% under MRI scanner stress     │
│   (MedFL-Stress, arXiv:2605.09025 — synthetic shifts on BraTS).            │
│ • Verbalized conflict in medical VLMs is non-causal rationalization         │
│   (MC-CXR App. D pilot on GPT-5.5; GACL audio transfer).                    │
│ • Conformal prediction sets inflate to meaningless sizes under modality    │
│   transfer (CALCoDe, arXiv:2607.28696).                                    │
└────────────────────────────────────────────────────────────────────────────┘
┌────────────────────────────────────────────────────────────────────────────┐
│ LOW CONFIDENCE / UNPROVEN (Mainly inference, unverified assumptions)       │
├────────────────────────────────────────────────────────────────────────────┤
│ • FeTS-2022 Synapse access can be approved within a 2-week pilot window.   │
│ • Federated aggregation inherently causes calibration disparity in VLMs     │
│   beyond what centralized domain shift already explains.                   │
│ • Single-machine Ray/Flower simulation will run reliably on Colab without   │
│   memory spilling or framework version churn.                              │
└────────────────────────────────────────────────────────────────────────────┘
```

### Critical Epistemic Separation:
* **"The reports claim X":** The reports claim that a 3-person undergraduate team can execute a clean federated conformal prediction extension in 2 weeks, or that evaluating AUGRC on dermoscopy constitutes a major clinical triage breakthrough.
* **"The collected evidence establishes X":** The evidence establishes that (1) FeTS-2022 is administrative quicksand, (2) the core conformal FL discovery was already claimed by Shahid three months ago, (3) selective prediction on dermoscopy is an incremental application of Traub et al. (2024), and (4) **neither direction matches the conceptual sharpness, causal rigor, or clean execution of the held VLM thesis.**

---

# 9. FINAL DECISION

### Field 1: Medical Image Analysis (Without VLMs)
## **STOP EXPLORING**
*(Retain Candidate M1 strictly as an unworked paper fallback on the shelf, but do not invest another hour of active research time.)*
* **Rationale:** Candidate M1 (AUGRC on dermoscopy under sensor shift) is technically executable on Colab Pro, but it fails the "Medical Imaging Is Not Enough" test. It is fundamentally an empirical benchmark comparison of off-the-shelf confidence scoring functions (Traub et al., 2024) across existing public datasets (ISIC/PAD-UFES). It develops no new learning mechanism, creates no new statistical theory, and carries severe data-cleaning and leakage-auditing overhead (patient ID deduplication, nested challenge filtering) that yields low intellectual return in a computer science thesis viva.

---

### Field 2: Federated Learning (Non-VLM & VLM Variants)
## **STOP EXPLORING**
* **Rationale:** The burden of proof to reopen Federated Learning was deliberately set high, and FL completely failed to meet it:
  1. **Fails the "Why FL?" Test:** The VLM variant is a manufactured intersection where central domain shift explains all observed miscalibration; FL adds only engineering debt.
  2. **Core Niche Occupied:** The only defensible non-VLM question—worst-site conformal calibration failure—was already established by Shahid (*Fed-CRC-Seg*, arXiv:2606.20115, June 2026). Measuring partial participation is a minor parameter sweep on Shahid's code, not a thesis.
  3. **Data & Infrastructure Gate Triggered:** Authentic clinical site labels exist only in FeTS-2022, which is locked behind manual Synapse review and involves heavy 3D volumetric data. Simulating clients via 2D Dirichlet splits is an artificial academic exercise explicitly discredited by recent 2026 literature.

---

### Field 3: Medical Vision-Language Models (Centralized)
## **STOP EXPLORING**
* **Rationale:** The medical VLM reliability space is heavily occupied by recent 2026 papers (MVC-Bench, DualRead, CalibratedTriage, EVADE). The only surviving question in this domain—causal conflict verbalization and source arbitration (R1)—is literally the researcher's **held general VLM thesis question** wrapped in medical images. However, instantiating it in medicine introduces massive confounding variables: question-template leakage, non-expert answers, noisy report text, and clinical validity bars that 3 undergraduate computer science students cannot defensibly clear.

---

### Comparison with the Held Thesis Direction

| Dimension | Medical Imaging (M1) | Federated Learning (FL1) | Held Direction: Causal VLM Conflict Verbalization |
| :--- | :--- | :--- | :--- |
| **Conceptual Novelty** | Low–Moderate (Benchmark audit) | Moderate (Operational extension) | **High (Causal mechanistic probe of transformer reasoning)** |
| **Core Scientific Question** | Does AUGRC degrade on smartphone photos? | Does CRC survive client dropout? | **Does verbalizing contradiction causally change arbitration or merely rationalize latent preference?** |
| **Negative-Result Value** | Moderate (confirms/refutes safety margin) | Moderate (confirms/refutes dropout robustness) | **Exceptional (Null proves explanations are post-hoc rationalizations)** |
| **Infrastructure Overhead** | Image deduplication, split hygiene | Synapse access, FL simulation loops | **Zero (Inference on open APIs / quantized local models)** |
| **Viva Defensibility** | Vulnerable to "Why is this CS?" | Vulnerable to "Is this real FL?" | **Rock-solid within core Artificial Intelligence & NLP/CV** |

---

# 10. MOST IMPORTANT OUTPUT

## What should I do next?

> **Stop investing research time in Medical Image Analysis and Federated Learning immediately, formally terminate both exploratory tracks, and return 100% of your thesis focus to the held Trustworthy Multimodal VLM thesis direction (Causal Conflict Verbalization and Source Arbitration).**

Do not run the dermoscopy pilot. Do not register for FeTS-2022 on Synapse. Do not attempt federated simulations. All evidence in your audit corpus demonstrates that continuing in Medical Imaging or FL will consume your remaining semester on data deduplication, credentialing friction, and distributed systems debugging for an incremental benchmark contribution. The held VLM direction is conceptually superior, methodologically cleaner, and fully within your computational reach.