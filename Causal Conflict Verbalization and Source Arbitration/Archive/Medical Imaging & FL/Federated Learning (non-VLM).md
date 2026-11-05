Adversarial Thesis Reopening Audit - Federated Learning (non-VLM)
Project: Thesis. Auditor role: skeptical senior reviewer. Status of topic before this audit: FL is a PARKED direction; higher burden of proof required to reopen. Audit date: 2026-09-20. Scope: Federated Learning for medical imaging WITHOUT vision/language models. VLM-based FL is out of scope.

1. Executive Verdict
REOPEN FOR A TIME-BOXED, GATED PILOT - not an unconditional reopen.

A narrow but genuinely defensible niche still exists, and it is recently crowded:

The most attractive single problem - site-conditional calibration under real multi-institutional data - was already attacked by Fed-CRC-Seg (arXiv:2606.20115, June 2026), which shows on real FeTS-2022 data that naive pooled conformal calibration violates worst-site guarantees, and proposes risk-curve shrinkage.
Therefore "average calibration fails" is no longer a novel headline claim; it is an anchored, reproducible result you can replicate, confirm, and extend. The defensible contribution is independent replication + characterization + an unclaimed extension (partial participation, shift-type taxonomy, or a cheap 2D accessible variant), not a new mechanism.
The area is clearly active in 2026 (calibration x FL, worst-hospital evaluation, benchmark frameworks). Treat the closest paper as a moving target and re-audit the literature before any submission.
Reopen only if all gates in section 17 pass within the timebox. Otherwise keep parked.

2. Kill Criteria (re-read filters applied this audit)
Any one of these implies KEEP PARKED:

Minimum meaningful experiment requires an A100 or multi-GPU training step. (Gate: section 9 - verdict: does NOT trigger reject.)
Infrastructure effort (distribution, networking, deployment) dominates research effort. (Gate: section 10 - verdict: avoidable by design, does NOT trigger reject, but only if you commit to single-machine simulation.)
The proposed question dies when you remove the word "federated". (Gate: section 11 - verdict: partially. The core conformal question survives without FL, so novelty must come from the multi-site / privacy constraint plus real site labels, not from the calibration idea itself.)
No realistic public dataset with defensible site partitions exists. (Gate: section 4 - verdict: FeTS-2022 qualifies; HAM10000 requires documented simulation.)
You cannot produce a falsifiable H0 that a 60-90 minute experiment could disprove. (Gate: section 17.)
None of the five triggers fully fires; two (3 and 4) fire partially and must be managed, which is why the verdict is a gated pilot, not a reopen.

3. Lab Inventory & Operating Constraints (re-confirmed)
Compute: Ryzen 5 5600G, 8 GB RAM, no local CUDA; Colab Pro (T4/V100/A100 allocation varies per session).
People: 3 undergraduate students, self-directed, thesis scope.
Stack allowed: PyTorch, Flower, FedML, PEFT. No real hospitals, no private data, no multi-node infrastructure.
Data policy: public datasets only; simulated or real-labeled-site clients.
4. Dataset Audit
Dataset	Task / size	Site labels?	License / access	Verdict for you
FeTS-2022 (federated tumor segmentation)	3D mpMRI, ~1,251 train + ~219 val subjects / patients, 4 modalities, glioma segmentation	YES - real de-identified per-institution partition labels (23-33 institutions; ~61% of institutions own under 15 samples)	Non-commercial; access via Synapse project syn28546456 after registering for the challenge (form + manual approval + team invite); organizers confirm data still available for research	Best-in-class for a real site split. Access friction is real (forum shows delayed approvals) and 3D training is heavy; calibration-only experiments can reuse FeTS pre-trained weights (github FeTS-AI/Models)
HAM10000 / ISIC	2D dermoscopy, 10,015 training images (11,720 in archive collection), 7 classes	Two real sites (Vienna, Queensland) documented in the data paper but no per-image site column in the release metadata, so sites must be simulated	CC BY-NC 4.0 (non-commercial only)	Easy, fast, Colab-friendly. Caveat: patient/lesion leakage across partitions documented in arXiv:2401.14497; use patient-stratified splits
MedMNIST v2 / DermaMNIST	Standardized 28x28 (now 64/128/224 variants); DermaMNIST = HAM10000 re-split 7:1:2 (7007/1003/2005)	No site metadata; fixed academic split	CC BY 4.0 except DermaMNIST CC BY-NC 4.0; code Apache-2.0; pip install medmnist	Infrastructure/debugging only - too small/clean to carry a calibration claim; fixed DermaMNIST split has documented leakage
BraTS 2020	3D MRI segmentation, multi-institutional routine clinical scans	Effectively no public per-institution labels (TCGA mapping exists but is messy)	Registration via CBICA IPP (manual review, ~3-4 days); non-commercial; val/test gated	Usable only with a simulated hospital split (as MedFL-Stress does). Good as a second modality, not as a site-labeled dataset
Inference, not observation: FeTS-2022 is the only public medical imaging dataset where "federated clients = real institutions" can be claimed without a hand-wave. Everything else requires you to state and defend a simulation mapping (section 5).

5. Simulated-Client Validity
The standard Dirichlet label-skew split is an artifact, not a hospital. Source: data-centric review of non-IID FL (Neurocomputing 2026, doi:10.1016/j.neucom.2026.135005), which connects split protocols to real acquisition phenomena and ranks non-IID traits by convergence influence.

Defensible mappings, ranked:

Real site partition (FeTS-2022 provided partition labels). The gold standard. Matches how Fed-CRC-Seg, FL-MedSegBench (9 clients, institutions with >=30 patients), and the FeTS challenge itself are evaluated.
Graded imaging-appearance shift covering scanner/acquisition physics (brightness/contrast, resolution, blur, noise). This is what MedFL-Stress (arXiv:2605.09025: 4 simulated hospitals from BraTS 2020 with gamma, scale, noise+blur shifts) validates, and what "When to Adapt?" (arXiv:2605.00892) analyses across 6 medical settings (appearance-based shift -> harmonization helps; structural shift -> personalization helps).
Label/Population skew (patient subgroup mixes per site). The weakest mapping to real hospitals; acceptable only as a control condition, never as the primary claim.
Key empirical guardrails from the literature:

OmniMed-FL (arXiv:2609.10364; 3-20 hospital clients, Dirichlet partitioning): naive methods collapse - SCAFFOLD-AdamW got 0.070 +- 0.015 vs FedAvg 0.662 +- 0.074 and FedProx 0.737 +- 0.085. Any claim must anchor against FedAvg/FedProx baselines.
MedFL-Stress: FedAvg global mean Dice 0.8159 on BraTS 2020 with a best-worst hospital gap of 0.0850; FedBN closes the gap by 41% (to 0.0503) while losing under 0.5pt mean Dice (0.8109). Worst-site metrics should be PRIMARY, not a robustness afterthought.
6. Framework Audit
Framework	Status (as of Sep 2026)	Simulation on one Colab GPU	Verdict
Flower	Actively maintained (v1.26 Feb 2026, v1.28 Apr 2026, v1.31 Jun 2026; docs updated Sep 2026). Simulation Runtime based on Ray/Virtual Client Engine supports single-machine, many-client simulation. High API churn (SuperLink, federation-config, app layout keep moving)	Yes	Best-maintained general choice. Pin a version and follow only the "Run simulations" docs. Budget some days for version churn
FedML	Open-source library exists, but the org has pivoted to the commercial FedML AI / TensorOpera platform (federated LLMs, cloud-GPU training)	Yes (older recipes)	Weaker fit; benchmarks exist but ecosystem now platform-centric
PySyft	Active, but the project was rewritten (v2; 0.10.0 Aug 2026) into a private-compute-over-file-transports library (syft-rds); the classic Flask/Grid FL orchestrator is deprecated (legacy API pinned at syft<0.10)	No (not its focus anymore)	Not suitable as the FL trainer for this thesis
Lightweight scaffolds	microsoft/fl-simulation (MIT; FedAvg/FedProx/SCAFFOLD simulation loop); PRR-FL (MICCAI'21, FedBN-style, dermoscopy, ready-made client A/B/C/D folders); FL-MedSegBench (hospital-split preprocessing for FeTS); OpenFL (what the real FeTS federation uses)	Yes	Strong candidates to copy structure before layering Flower on top
Recommendation: start with a manual or microsoft/fl-simulation-style loop for the pilot (automates least), then optionally port to Flower pinned to a single version to back the "standard framework" claim. Avoid PySyft and FedML cloud paths entirely.

7. Literature Landscape
#	Paper	Theme	Why it matters	Undergrad-feasible to build on
1	2606.20115 Fed-CRC-Seg (site-conditional federated conformal risk control)	Calibration on real sites	Closest prior. Pooled CRC violates coverage at 40% of institutions on real FeTS-2022; worst site exceeds target FNR by 7.8pp. Fix: risk-curve shrinkage (site sends G-scalar risk curve + n0). Code public	Yes - replicate/extend on FeTS-2022 or a 2D analog
2	2605.09025 MedFL-Stress	Worst-hospital evaluation	Graded MRI shift taxonomy; FedBN 41% gap closure	Partial - BraTS registration + 3D training heavy; methodology transferable
3	2605.00892 When to Adapt? (harmonization vs personalization)	Domain-shift remedy choice	Appearance vs structural shift decision rule across 6 medical settings; code public	Yes (conceptual/method transfer)
4	2512.23043 Mechanistic Evidence for Preserved-but-Misaligned Representations in non-IID FedAvg	Theory	Explains why federated feature spaces drift; motivation for calibration, not a medical result	No (research-grade, non-medical)
5	10.1016/j.neucom.2026.135005 From data heterogeneity to convergence: a data-centric review	Simulation validity	Ranks non-IID traits by convergence influence; documents protocol artifacts	Yes (read + cite for section 5)
6	2609.10364 OmniMed-FL	Multimodal hospital FL benchmark	SCAFFOLD-AdamW collapse (0.070 vs FedAvg 0.662); naive methods fail on hospital heterogeneity	Partial - multimodal stack heavy; numbers are a baseline anchor
7	2609.15625 FedLTLib	Long-tail FL benchmark	Reproducible long-tail FL benchmarks	Yes
8	2608.25114 Flower Hub	Reproducible benchmarking platform	Standardized FL benchmarking infrastructure	Yes (as citation + potential scaffold)
9	2608.25873 How Edge of Stability Hinders SCAFFOLD	Optimization theory	Explains SCAFFOLD instability trend in medical/other workloads	Yes (read)
10	2607.13386 FM^2 (federated foundation models)	Medical foundation models in FL	Context: where the field is migrating; not needed to reach your niche	No
11	2607.19532 Multimodal FL for breast cancer	Near-domain application	Demonstrates FL performance parity work on public medical data	Partial
12	2609.13303 AdaConRed (conformal, ISIC)	Conformal + skin lesions	A cheap 2D conformal anchor on ISIC-derived data; natural baseline family	Yes - ideal 2D baseline
13	2512.04305 How (Mis)calibrated is your Federated CLIP	Calibration, but VLM	Documents calibration failure in FL for the VLM branch; compare only, not inheritance	No (VLM, out of scope)
14	2605.14590 FedStain / 2510.18268 TreeFedDG	Pathology federated domain generalization	Adjacent FedDG methods on pathology	Partial
15	2401.14497 Investigating the Quality of DermaMNIST/Fitzpatrick17k	Data-quality	Documents leakage/mislabeling in HAM10000-derived splits; you must clean or stratify	Yes (methodological)
Analysis (inference): the calibration-on-real-sites row (paper 1) is the only paper that occupies exactly your proposed niche, and it is months old. Papers 2-3 define your evaluation language (worst-site/worst-hospital). Papers 5 and 15 define your simulation-validity and data-hygiene obligations. No VLM approaches are required to compete in this niche.

8. Candidate Research Questions (5, ranked)
RQ1 (flagship): Under realistic, per-site heterogeneous calibration data, does site-conditional conformal risk control reduce worst-site violations of a per-site risk budget relative to pooled calibration, holding the federated training scheme fixed?

IV: calibration scheme (pooled vs site-conditional vs risk-curve shrinkage) x shift condition (real site split on FeTS-2022; simulated photometric shift on a 2D analog).
DV: worst-site risk (segmentation FNR under conformal risk control) and mean-worst tradeoff; per-site coverage for prediction-set variants.
H0: pooled calibration satisfies worst-site risk within tolerance (nuisance: with small site counts conformal is conservative, so pooled may already "look fine").
H1: site-conditional calibration materially reduces worst-site FNR violation vs pooled.
Controls: same backbone, same data budget, same metric; FedAvg and FedProx baselines; report per-site size distribution.
Negative result: pooled is already within budget (phenomenon does not reproduce in your setting) or site-conditional blows up variance on small sites.
Feasibility: yes - replication of Fed-CRC-Seg; cheapest on the 2D analog.
RQ2 (characterization / taxonomy): Which shift families (photometric, blur, label skew, size skew) actually produce worst-site calibration failure, in what ordering?

Runs on RQ1's harness. Negative result is informative (no single shift family drives the failure).
RQ3 (extension, highest novelty per unit effort): Does client sampling / partial participation (e.g., 40% of sites per round) degrade worst-site calibration guarantees under site-conditional calibration vs full participation?

Fed-CRC-Seg assumes all sites contribute a risk curve. Partial participation is a natural, unclaimed extension.
Negative result: threshold-dominated by pooled curve, no effect.
RQ4 (minimum viable, cheap): On 2D dermoscopy segmentation/classification with simulated but explicitly documented site shifts, at what site sample size n_site does site-conditional calibration stop winning over pooled (the sample-complexity wall)?

All-Colab feasible; establishes the regime where the method works. Strong support for RQ1.
Negative result: wall is so high it is unusable at medical site sizes.
RQ5 (does FL hurt calibration beyond accuracy?): For a fixed data budget, do federated-trained models (FedAvg, FedProx, FedBN) show worse worst-site calibration than a centralized model trained on pooled data?

Directly relevant to the "FL is just accuracy" critique; the non-VLM sibling of 2512.04305. Negative result (parity) is a publishable null.
9. Compute Kill Gate (T4 sufficiency)
Workload	T4 (16 GB) feasibility	Notes
2D dermoscopy classification/segmentation + conformal calibration (RQ4, low-cost RQ1)	Yes, comfortably (minutes-hours)	Courtesy of 224x224 inputs and small nets; AdaConRed family runs here
FeTS-2022 3D MRI calibration using FeTS pretrained weights (FeTS-AI/Models)	Yes (inference + risk-curve computation only)	No federated training needed for the calibration claim
Training a 3D U-Net from scratch on FeTS-2022 (128^3 patches)	Borderline (hours-days, 8-16 GB; small-batch + patience)	Do not build the thesis on this; use pretrained weights or deprioritize
VLM fine-tuning (out of scope)	Not assessed	Out of scope
Kill-gate verdict: T4 is sufficient for the minimum meaningful experiment; an A100 or multi-GPU is NOT required, so the kill criterion does not fire. The recommended thesis math is: one cheap 2D full-pipeline run plus one FeTS-2022 calibration-only run on pretrained weights.

10. Distributed-Systems Rabbit Hole
This is where FL theses usually die. Containment plan (non-negotiable):

Single-machine simulation only. No cross-machine networking, no real clients, no deployment. The FL server and clients are threads/processes on one Colab/desktop machine.
Use a manual or microsoft/fl-simulation-style loop; treat Flower as an optional compatibility layer pinned to one version.
Do NOT touch PySyft legacy orchestration, Grid/WebRTC, MPI, or Ray clusters.
Budget at most ~1-2 weeks of the pilot for infrastructure, including the Flower port. If that slips, infrastructure wins - a Parked signal.
Verdict: the rabbit hole is avoidable by design, so it does not independently trigger rejection - but only if you commit to the single-machine discipline.

11. Novelty Stress Test (remove the word "federated")
RQ1 without FL: "Does pooled conformal calibration violate worst-site guarantees under distribution shift?" - Almost certainly studied in centralized distribution-shift conformal literature (conditional/hedged/risk-control variants). The calibration idea alone is not new.
The novelty therefore lives in the multi-site constraint + genuine site labels + privacy-shaped information limits (per-site risk curves, not raw calibration scores) and in the unclaimed extension (partial participation). That is enough for an undergraduate thesis only if the report frames the contribution as replication + characterization, not as a new headline mechanism.
RQ5 is the honest framing that survives the test: it asks what the federated setting specifically "adds" - a question reviewers accept.
12. Experimental Design for the Strongest RQ
Recommended primary: RQ1 (feasibility/validity first) with RQ3 as the extension, on FeTS-2022 real site split, backed by the 2D analog (RQ4) as the cheap iteration loop.

Backbone: start on HAM10000-derived 2D (ISIC-2018 segmentation or classification) to iterate in minutes on Colab; then FeTS-2022 with pretrained FeTS weights.
Sites: FeTS-2022 provided institution partition; for the 2D analog, simulate 4-8 sites with controlled photometric shifts and patient-stratified splits (documented; never Dirichlet-only).
Calibration: pooled CRC threshold vs per-site threshold vs risk-curve shrinkage (n0 sweep) - replicate Fed-CRC-Seg's procedure; then add partial participation (RQ3).
Metrics (primary): worst-site FNR (segmentation), coverage of 90% target per site, mean-worst tradeoff, per-site calibration sample sizes. Report CIs via site subsample replication.
Baselines: centralized pooled-data trainer, FedAvg, FedProx (and FedBN for the appearance-shift condition, per MedFL-Stress).
Pre-registration: state H0 and effect sizes before running, because per-site metrics on 23 institutions (~61% with under 15 samples) are high-variance; power skepticism is mandatory.
13. Closest Existing Paper - Parsed Gap
Fed-CRC-Seg (arXiv:2606.20115), June 2026 - the paper you will be measured against.

What it does: real FeTS-2022; pooled CRC violates worst-site coverage at 40% of institutions; worst site exceeds the false-negative-rate budget by 7.8pp; proposes risk-curve shrinkage (each site transmits a G-scalar empirical risk curve and one hyperparameter n0, interpolating between site-local and pooled calibration). Privacy-preserving: no images/volumes leave sites. Code at github.com/NafisFuadShahid/Fed-CRC-Seg.

What it does NOT do (your opening):

Partial participation / client sampling effects on worst-site guarantees (its guarantee assumes all participating sites transmit risk curves).
A shift-type taxonomy (which acquisition shifts most produce worst-site miscalibration).
A 2D/lightweight accessible reproduction (cheap validation of the phenomenon's generality beyond 3D MRI).
Interaction with domain-shift remedies (FedBN/harmonization) that change the calibration problem while preserving privacy.
Also worth noting: it is arXiv-only, single-author, and recent - exactly the profile to verify independently before leaning on it.

14. Exact Gap Statement
"Under genuine multi-institutional data (real site labels on FeTS-2022) and realistic simulated shifts (graded appearance shift), the worst-site violation of pooled conformal calibration has been shown once (Fed-CRC-Seg) but the boundary conditions are unknown: which shift types break it, how mandatory full participation is for the guarantee, and at what site sample size the fix stops working. An undergraduate thesis can establish these boundaries with a cheap 2D spine plus one FeTS-2022 confirmation - a replication-and-characterization contribution, defensible without a new mechanism."

15. Main Failure Risks (ranked)
Literature clock: the niche is hot; by submission time someone may publish partial participation x conformal FL. Mitigation: re-run this audit before writing up; choose speed-of-execution over scope.
FeTS-2022 access friction: manual approval, possibly delayed (Synapse forum shows unanswered requests). Mitigation: submit on day one; parallel-track the 2D dataset so nothing blocks.
Weak statistical power: 23 institutions, most with very small samples; per-site worst-case metrics are noisy. Mitigation: site subsample replication, CIs, pre-registered effect sizes.
Conformal conservatism at small n: pooled may "look fine" only because guarantees are conservative - the motivating failure may not reproduce in your subsample. This is a genuine kill risk for RQ1; the falsification task in section 17 tests it.
Data leakage in public 2D sets: HAM10000/DermaMNIST partitions have documented leakage (2401.14497). Mitigation: patient-stratified splits and cleaning; state it in the thesis.
3D compute overrun: training a U-Net from scratch on FeTS-2022 can eat the semester. Mitigation: pretrained FeTS weights; keep 3D training optional.
16. Timebox / Pilot Plan (2 weeks, 3 students)
Day 0: submit FeTS-2022 Synapse access request (someone's full job); set up Colab + repo; define shift configs.
Days 1-2: 2D spine running (ISIC dermoscopy, 4-8 simulated sites, patient-stratified); pooled vs site-conditional calibration numbers.
Days 3-5: 60-90 min falsification task (section 17) executed and interpreted.
Days 6-9: FeTS-2022 replicate (pretrained weights) once access lands; RQ3 partial-participation grid if the phenomenon reproduces.
Days 10-14: write-up of the replication + characterization; re-audit literature; formal reopen/keep decision.
Exit criteria for a passing pilot: the falsification task shows worst-site violations existing and being reduced by site-conditional calibration in the 2D spine; FeTS-2022 confirms on at least the two largest site groups; partial-participation grid shows a measurable effect or a clean null.

17. Verdict + Falsification Task
Reopening Verdict: REOPEN FOR PILOT (2-week gated). Conditions attached:

Worst-site metrics are primary; mean is reported but never alone.
Real site labels on FeTS-2022, or explicitly documented simulated appearance shifts; never a bare Dirichlet split.
Position explicitly and charitably against Fed-CRC-Seg (2606.20115) as replication + extension.
Re-audit the literature at pilot end before any submission.
The 60-90 minute falsification task (run first):

Build a small 2D pipeline on HAM10000/ISIC-2018 (any small model; even logistic on features).
Create 4 "hospitals" by patient-stratified partition + controlled photometric shift (contrast/illumination), documented.
Compute pooled split-conformal calibration; measure per-site coverage (target 90%); record the worst-site shortfall across 8-10 shift configurations.
Then compute site-conditional thresholds; record worst-site shortfall again.
Kill rule: if no configuration shows a worst-site undercoverage of more than 2pp under pooled calibration that site-conditional reduces, the flagship premise ("pooled calibration fails the vulnerable hospital") does not reproduce in your cheap setting - then the thesis thesis would depend entirely on FeTS-2022 3D, which is low-power and expensive, and the direction should stay PARKED.
Thrive rule: violations appear and shrink with site-conditional calibration -> proceed to the FeTS-2022 confirmation and RQ3.
This task directly attacks the H0 of RQ1 with a finite, cheap experiment, which is what an adversarial audit of a parked direction demands.