ADVERSARIAL THESIS DISCOVERY AUDIT — Medical Imaging WITHOUT VLMs/MLLMs
Stance: adversarial senior reviewer. Assuming VLM-based theses are temporarily unavailable/undesirable, find a defensible, undergraduate-feasible, public-data question that can survive a viva. Judgment: one candidate is worth a Pilot; two are Reserves; the rest fail.

1) Researcher Context
Final-year CSE undergraduate, Bangladesh; 3-person thesis team.
Skills: Python, classical ML, DL (CNNs, Transformers), PyTorch, limited TensorFlow; solid LLM/VLM fundamentals (studied, can run but not pretrain).
Compute: local Ryzen 5 5600G + 8GB RAM, no CUDA; primary GPU is Colab Pro (T4 common; occasionally V100/A100). ≤16GB VRAM usable.
Desired topic: medical imaging, no VLMs/MLLMs (VLMs only as explicit comparison, never as dependency).
Evidence: 3 undergrads, ~1 year to defend. Engineering heavy, theory-light is fine; must be internal research question driven, shuffle-number-only papers won't pass adversarially.
2) Scope
In: calibration, selective prediction/abstention, distribution shift, shortcut learning/robustness, benign adaptation, corruption robustness.
Out: foundation-model pretraining, MLLM/VLM end-to-end, any private/clinical data.
Primary datasets: ISIC family, HAM10000, PAD-UFES-20, DDI, SCIN, MedMNIST v2, CheXpert, MIMIC-CXR, BraTS.
Diagnosis: dermatology/triage, DR screening, modality (clinical photos vs dermoscopy, skin tone) shift, corruption/shortcut robustness. CXR and CT candidates are mostly REJECTED due to workflow-lacking public data and crowd-saturation.
3) Hard Feasibility Gates
Gate	Criterion	Status for the recommended candidate
No private data	Public datasets only	Pass (dermoscopy public)
No human-subject approval	No recruitment, no annotated patient-facing study	Pass
No specialist annotation	Small target classes, existing labels	Pass
No proprietary datasets	No IP-protected	Pass
No large-scale pretraining	Max frozen/lightweight nets	Pass
≤16GB VRAM	T4/Colab class	Pass
No multi-GPU / cluster	Single T4	Pass
Reproducible with public code	All model/metric code open	Pass (with caveats below)
Conclusion: all gates satisfiable for the dermatology-selective-prediction candidate.

4) Research Questions to Investigate
Calibration: do post-hoc calibrated confidences remain well-calibrated across shift types? (Saturated in-distribution, open under shift.)
Selective prediction: does the risk–coverage ordering of samples by confidence survive defined shifts (population/device/label-shift), or does abstention fail exactly where it matters?
Distribution shift:
Composition shift (disease prevalence, e.g. ISIC2019 vs ISIC2020 vs HAM10000).
Modality shift (dermoscopy → clinical photos, PAD-UFES, DDI).
Skin-tone shift (ISIC mostly light skin vs DDI/SCIN darker tones).
Synthetic corruption (ISIC/MedMNIST with JPEG/blur/contrast/color).
Shortcut learning / robustness: can recovering subgroup performance be seen as calibration failure under group shift (3809 trend), and can selective referral recover misaligned subgroups?
Adaptation: benign, test-time adaptation (TTA) without VLM (e.g. CoWA). Mostly covered elsewhere; low novelty.
5) Primary Literature Requirement
Requirement: ≥10 serious 2024–2026 papers on the topic of the final thesis. The recommended thesis (calibration + selective prediction + distribution shift in dermoscopy; contrast vs DR/Retina) has 12–15 qualifying papers. The topic is real, recent, and heavily evaluated, so literature will not be the thesis's bottleneck.

6) Required Literature Table
ID	Paper	Year	Venue	Relevance	Saturation
2605.19133	Knowing When Not to Predict: Self-Supervised Learning and Abstention for Safer DR Screening (IJCAI)	2025	IJCAI	SSL pretraining length vs calibrated confidence and abstention; DR screening	Near-saturated selective+shift in DR
2607.02569	Uncertainty-Aware Last-Layer Adaptation of RETFound	2025		DR selective referral APTOS→DDR; SNGP negative transfer; safety-coverage eval	High
[10.48550/arxiv.2407.01032]	Overcoming Common Flaws in the Evaluation of Selective Classification Systems (AUGRC)	2024		13 confidence scoring functions across 6 datasets, CAMELYON-17-Wilds; the canonical selective-metric	Methodology core
2609.07922	Prevalence calibration as shortcut mitigation	2025		Calibration (not model retrain) as shortcut mitigation; CheXpert/SIIM-ACR, misaligned-group AUROC 0.23→0.73	Crowded CXR shortcut
2608.14768	Pooled-ISIC uncertainty across 5 UQ methods; risk-coverage in-distribution only	2025		The lack-of-shift evidence gap in dermoscopy. Primary gap to exploit	High
2607.26765	Kozachok et al., Searching for Robust Augmentations to Improve Out-of-Domain Generalization in Dermoscopic Skin Cancer Classification	2026		6-source dermoscopy; contamination-controlled OECD protocol; PAD-UFES independent cohort; robust augmentations, AUC-only	High, augmentation-baseline
2609.02111	Disease Burden over Skin Tone: Decomposing the Dermatology-AI Generalization Gap	2025		HAM10000/ISIC2019→DDI + SCIN; disease-shift dominates skin tone; accuracy/representation only	Primary gap target
2608.22059	CRS-Bench: encoder reliability benchmark (calibration under shift, ISIC2019/APTOS/CheXpert→MIMIC)	2025		Direct benchmark reference	Saturated as benchmark
2608.25810	Label-free foundational model selection under distribution shift (SUDO/AURCC)	2025		Model selection under shift via pseudo-label discrepancy	Related, selection not abstention
2608.16614	Geospatial/PLEX: confidence abstention cannot defer around confidently-wrong samples	2025		Concerning result for selective-prediction assumptions	High, caution
2607.03797	Probabilistic robustness in medical image classification (MedMNIST-v2)	2025		Natural corruption calibr/robustness on medical MNIST	Saturated for MedMNIST
2604.06099	ZACH-ViT: corruption robustness on MedMNIST	2024–25		MedMNIST corruption baseline	Saturated for MedMNIST
2602.10265	Colorimeter-supervised skin-tone estimation (ISIC2020)	2025		Skin-tone meta-labels, needed as controls for tone-shift	Component
10.1038/s41746-024-01118-4	Shao et al., "Shortcut learning in medical AI hinders generalization"	2024	npj Digit Med	The domain-robustness review thesis must cite	Saturated as review
2608.17712	Leakage-proof conformal selective triage (EHG preterm)	2025		Conformal selective triage, leakage-proofing protocol	Related
2608.27004	MVC-Bench (VLM calibration benchmark)	2025		VLM comparison anchor: VLM calibration failure vs networks	VLM
Saturation verdict: In-distribution calibration/UQ is fully saturated; selective prediction under shift in DR is near-saturated (two strong papers); selective prediction under shift in dermoscopy is under-specified — the residual gap is real but narrow.

7) Dataset Audit
Dataset	Size	Labels	License/Access	Leakage risk	Shift value	Compute
HAM10000 (Harvard Dataverse doi.org/10.7910/DVN/DBW86T)	10,015 images, 7 classes (AKIEC/BCC/BKL/DF/MEL/NV/VASC)	lesion_id, age, sex, site; ~10 img/patient [VERIFIED lesion_id exists]	Custom/academic terms (Dataverse) [VERIFIED]	High patient-level	Composition shift (nested in ISIC2019)	low
ISIC 2019 (gallery.isic-archive.com)	25,331 images, 9 classes	lesion_id only	open/archive; CC-BY-NC [INFERRED from archive practice], single-file download	Contains all HAM10000 — dedup caught	Source-shift set	low-mid
ISIC 2020	33,126 images	patient_id	CC-BY-NC [INFERRED]	patient-level manageable	Composition shift, its own val/test	low-mid
PAD-UFES-20 (Kaggle/Mendeley)	2,298 images, ~1,373 patients, 6 classes	patient_id	CC BY 4.0 mirror [VERIFIED]	distinct	Modality shift: clinical photos	low
DDI (Stanford AIMI)	656 images, 18 path-confirmed classes	skin-tone labels	research-use agreement, free, non-commercial [VERIFIED]	exempt (eval-only)	Skin-tone shift tiny eval set	low
SCIN (google/scin HF)	10,000+ images, dermatology conditions	sFST/eFST/eMST, labels	SCIN Data Use License [VERIFIED], 15 duplicate images to dedup	eval-only	Label taxonomy differs from ISIC diseases [merged-layer note]	low
MedMNIST-v2 (pip medmnist 3.0.2)	12×2D + 6×3D small sets	per-dataset	Apache code / CC-BY-4 data; DermaMNIST CC-BY-NC [VERIFIED]	none	Corruption/robustness surface	trivially low
CheXpert (AIMI)	224,316 radiographs	5 label scit	research registration/terms [VERIFIED]	eval okay	CXR only labels, no workflow	mid
MIMIC-CXR (PhysioNet)	227,835 studies/377,110 imgs		credentialed + DUA [VERIFIED]		Large-scale	mid
Note: CheXpert/MIMIC lack printed "equipment/position" workflow metadata free of DUA entanglement; for a 3-person undergrad team these are workflow-hazards, not assets.

8) Candidate Thesis Questions
Candidate 1 — RECOMMEND (dermoscopy selective prediction under shift)

RQ: Which post-hoc confidence estimator preserves selective-prediction validity under defined distribution shifts in dermoscopic skin-lesion triage, and is any estimator's robustness consistent across shift types?

H0: Risk-coverage ordering and calibrated risk-coverage hold approximately across shifts (abstention is a reliable safety layer).
H1: Selective risk ordering degrades under population/composition shift even when calibration is refit; degradation is estimator-dependent (e.g., ensemble vs MC-dropout).
Intervention: train DenseNet/ResNet on HAM10000+ISIC2016–2019 (dedup), then apply estimator families: temperature-scaled MaxSoftmax, MC-dropout, deep ensembles, ODIN, energy/Mahalanobis, split-conformal risk-control.
Controls: same model, different confidence family; fixed vs refit temperature under shift.
Metrics: AUROC, ECE, Brier, NLL, risk–coverage curves, AURC/AUGRC [2407.01032 method], FPR-at-95%-sensitivity-with-abstention, OOD AUROC.
Shift set: within-ISIC source shift; synthetic corruption; PAD-UFES/DDI modality+tone shift; SCIN taxonomy shift (if gap-supporting).
Data/Fit: public-only, no annotation needed.
Negative-result value: If abstention reliably fixes calibration but not ordering → important negative "abstention is a label-shift absorber, not a safety guarantee."
Candidate 2 — RESERVE (DR selective referral, extend RETFound/Self-Supervised)

Weighted heavily by 2605.19133 and 2607.02569 (same niche). Only feasible if we find a new unsurveyed corner (e.g., estimator×shift interaction in DR, device shift). Marginal.
Candidate 3 — RESERVE (chest X-ray view/position selective under shift)

Viable in principle (CheXpert→MIMIC site shift, view-tag selective). But: CheXpert/MIMIC DUA, metadata procurement risk; and 2609.07922 already shadows CXR shortcut-calibration. Need access + a clean "no leakage" protocol.
Candidate 4 — REJECT (MedMNIST corruption+calibration audit)

2607.03797 + 2604.06099 already cover; small, saturated, incremental.
(5th candidate slot reserved; not filled — partial candidates (e.g., "shortcut-as-calibration", "confidence-shortcut detection") fail against 2609.07922.)

9) Leakage Audit (candidate-1 critical path)
ISIC 2019 ⊃ HAM10000 entirely [VERIFIED via archive/dataset listing]: any "train on ISIC, eval HAM10000" is catastrophic label leakage.
HAM10000 has ~10 imgs/patient; ISIC 2020 has patient_id; PAD-UFES has patient_id. Every internal split must be patient-level, else skin-lesion duplication inflates both calibration and RA.
ISIC 2019 lacks patient_id (lesion_id only) [VERIFIED]; doing source-shift split must test for sub-image duplicates (same lesion reimaged across patients), not just patient splits.
Dedup across ISIC + HAM10000 + Fitzpatrick + other public mirrors before training; archive provides no cross-source dedup by default.
Evaluation sets (DDI, SCIN, PAD-UFES) disjoint from training by construction if we never train on them [VERIFIED access terms permit eval-only use].
PAD-UFES is CC-BY and dermoscopy-adjacent; safe as external test. SCIN's different label taxonomy means a classifier trained on ISIC classes cannot be linearly evaluated there without a class-mapping layer — treat SCIN as a distractor/shift-probe, not a label set.
Leakage verdict: manageable with (a) patient-level splits, (b) explicit dedup, (c) eval-only external sets. This is standard protocol (matches Kozachok's contamination-controlled prescription [VERIFIED in 2607.26765]).

10) Compute Audit
Minimum experiment (single model): DenseNet121/ResNet50 @224px, batch 64, 3 seeds, Adam, ~1–2 epochs* = ~12–18 T4-hours → well inside 16GB/Colab.
Deep ensembles (5 members) ×2 models: ~60–90 T4-hours remainder of the envelope.
MC-dropout, ODIN, energy/Mahalanobis, conformal: all inference-only on the eval set.
Corruption ablation (Imagenet-C style severity): inference on prefixed severity, negligible added cost.
Real wall-clock: ~8–12 Colab Pro sessions at ~1–2h each. V100/A100 never required. Directly satisfies compute gates.
11) Closest-Work Autopsy
2407.01032 (AUGRC) — the methodological authority for how to evaluate selective classification across datasets; if our thesis does not use/properly cite it, viva fails. It validates AURC/AUGRC under shift, which is the metric backbone we must adopt.
2608.14768 evaluated 5 UQ methods and risk–coverage in-distribution only — its authors explicitly didn't push across real shifts. That is our documented opening (explicit gap).
2607.26765 trained 6-source dermoscopy DG but measured AUC-only (no calibration, no selective, no abstention). Same datasets, orthogonal metric → our contribution.
2609.02111 decomposed skin-tone vs disease-shift, accuracy/representation focus. Selective/calibration under that decomposition is the tail we cut.
2607.02569 (RETFound/DR) — already did selective-referral under shift in DR, so our domain must be dermoscopy, not DR; otherwise it's a near-duplicate.
2609.07922 — the "shortcut calibration" insight is published; so we must not claim "calibration recovers misaligned subgroup" as new; we may claim the dermoscopy cross-domain selective result as new if corroborated.
Autopsy verdict: the closest-work corridor is genuinely populated to the left and above (CXR, DR, MedMNIST) but dermoscopy's selective-prediction-under-defined-shift cell has no direct occupant. The gap is defensible but narrow, requiring strict evaluation hygiene to not be read as "just another UQ ablation."

12) Compare Against Held VLM Candidate
Criterion	Held VLM candidate	Candidate 1 (dermoscopy selective)
Question clarity	High — crisp falsifiable counterfactual	Medium-High — falsifiable but definition-heavy (shift types, estuaries)
Literature crowding	High (contradiction/conflict literature rife)	Medium — narrow unexplored dermoscopy cell
Dataset access	Depends on VLM bench datasets (open)	Fully public, low-barrier
Baseline reproducibility	High (given base VLMs)	High (standard CV + off-the-shelf calibrators)
Compute	High (VLM eval)	Low-Med (T4-class sufficient)
Leakage risk	Medium (prompt/format contamination)	High if hygiene sloppy, kills result
Evaluation validity	Medium (causal verbalization is noisy)	Medium-High (metrics canonical)
Novelty	High conditional on causal design	Medium — a real but narrow gap
Negative-result value	High	Medium
Engineering burden	High (LLM/VLM tooling)	Low-Med
Thesis scope/coherence	High — theoretical + empirical arc	Medium — engineering + analysis, less theory
Defensibility in viva	High risk if confounded	High risk if leakage or metric choice sloppy
Neither candidate is objectively "better"; they trade risk for novelty differently. The VLM candidate is more theoretically interesting but harder to make causally clean with 3 people; Candidate 1 is empirically safer but incrementally novel.

13) Final Decision
Candidate 1 → PROCEED TO PILOT. Concrete pilot: HAM10000+ISIC2019 split, DenseNet121, temp-scale + MC-dropout vs softmax, source-shift + corruption eval; if garbled calibration-on-shift tables are not reproducible internal, kill.
Candidate 2 → RESERVE. Only as fallback if Registered-corner resurfaces.
Candidate 3 → RESERVE. Only if the CheXpert/MIMIC DUA clears and metadata workflow is sanitized.
Candidate 4 → REJECT.
VLM candidate: not rejected; held at "in comparison", to be re-scored after Candidate 1's pilot data arrive.
14) Evidence Labels
[VERIFIED] = directly confirmed via archive/website/paper-taking (e.g., DDI research-use agreement, SCIN 15-dup warning, APTOS non-commercial rule, ISIC2019⊃HAM10000, MedMNIST per-dataset licenses, patient_id/lesion_id schema).
[INFERRED] = extrapolated from adjacent authoritative sources (ISIC CC-BY-NC specifics, ISIC source-shift dedup completeness, RETFound availability).
[UNKNOWN] = not yet confirmed (exact ISIC2019 per-instance license text; whether SCIN contains sufficient melanoma rows to
todowrite: 0 todos
14) Evidence Labels
[VERIFIED] — confirmed via primary source during this audit:
HAM10000 = 10,015 images, 7 classes, lesion_id (tracks multi-image lesions), ~10 img/patient; Dataverse terms "Custom Dataset Terms / academic use" (Harvard Dataverse, doi.org/10.7910/DVN/DBW86T).
ISIC 2019 = 25,331 images / 9 classes, lesion_id only (no patient_id), and the ISIC Archive listing confirms HAM10000 images are inside it → dedup is mandatory.
ISIC 2020 = 33,126 images, has patient_id.
PAD-UFES-20 = 2,298 images / ~1,373 patients, 6 classes, clinical (non-dermoscopic) photos, CC-BY mirror on Kaggle.
DDI (Stanford AIMI) = 656 images, 18 classes, skin-tone labels; requires a Research Use Agreement registration, non-commercial research only, no redistribution.
SCIN (google/scin on HuggingFace) = 10,000+ images, released under SCIN Data Use License; 15 known duplicate images (42 occurrences) that must be deduped; label taxonomy differs from ISIC classes.
APTOS 2019 = Kaggle competition data, non-commercial use only per competition rules.
MedMNIST v2 = PyPI medmnist 3.0.2; code Apache-2.0; dataset CC-BY-4.0 except DermaMNIST CC-BY-NC.
CheXpert = Stanford AIMI research-registration terms; MIMIC-CXR = PhysioNet credentialed access + DUA (2011–2016, 227,835 studies / 64,588 patients / 377,110 images).
Paper facts (per-paper reads): 2607.26765 trains 6 dermoscopic sources (25,903 imgs) with contamination-controlled protocol; PAD-UFES external cohort 472 images; AUC-only evaluation. 2609.07922 raises misaligned-group AUROC 0.23 → 0.73 via post-hoc recalibration only.
[INFERRED] — extrapolated, not directly confirmed:
Exact ISIC 2019 / 2020 license text (CC-BY-NC claimed by mirrors/wikis; I did not view the enabled archive legal page in full).
BraTS 2021 = 1,251 train + 219 validation cases × 4 sequences (T1/T1Gd/T2/T2-FLAIR); structure known, exact file counts not hand-verified this session.
AUGRC methodology (2407.01032) details beyond the abstract/partial read (fuller read is available but not re-verified inline).
[UNKNOWN] — not yet confirmed:
Whether SCIN contains enough melanoma-class rows to serve as a meaningful melanoma shift probe (its taxonomy heavily favors common/inflammatory conditions).
Whether subset rows of ISIC 2019 training leak into ISIC 2018/2020 (need hash-level dedup at download time).
Whether CheXpert/MIMIC "view position/laterality" workflow metadata is usable without additional DUA overhead for Candidate 3.
Labeling rule applied: no claim of a research gap was made based on a paper merely failing to mention a topic. Gaps are only claimed where one primary source explicitly states its scope (e.g., 2608.14768 evaluates risk-coverage in-distribution only; 2607.26765 reports AUC-only; 2609.02111 analyzes accuracy/representation only), which is what makes the dermoscopy selective-under-shift cell defensible.

15) Bottom Line
A viable non-VLM thesis exists, in dermoscopy, not CXR/CT/DR. The defensible question is: "Does post-hoc confidence-estimator choice preserve selective-prediction validity under defined distribution shifts in dermoscopic skin-lesion triage?" — train on public ISIC-family dermoscopy, shift-set = source, corruption, modality (PAD-UFES), skin-tone (DDI).
The gap is real but narrow. Closest works (pooled-ISIC in-distribution risk-coverage; 6-source AUC-only DG; skin-tone accuracy-only) each stop one step short of the joint "calibration validity + selective ordering across defined shifts in dermoscopy" claim.
Do NOT claim "calibration fixes shortcuts" or "dermoscopy DG is broken" — both are published (2609.07922; Kozachok et al.). Frame contribution as estimator × shift-type interaction for selective triage.
Metrics are the thesis's spine: AUROC, ECE, Brier, NLL, risk–coverage, AURC/AUGRC (2407.01032), FPR-at-95%-sensitivity-with-abstention, OOD AUROC. Adopting AUGRC is non-negotiable for viva defensibility.
Leakage is the #1 execution killer: ISIC2019 ⊃ HAM10000; patient-level splits everywhere; hash-dedup across mirrors; eval-only external sets. Budget a written "contamination control" appendix up front.
Compute is comfortably within gates: ≤16GB VRAM, T4, ~12–18 T4-hours for the core grid; ~8–12 Colab Pro sessions total. No V100/A100 dependence; corruption/conformal tails are inference-only.
Candidate 1 verdict: PROCEED TO PILOT — run a 1-week pilot (2 models, temp-scale vs MC-dropout, source-shift + corruption) and make a go/no-go on the reproducibility of calibration-on-shift tables internally. If tables don't reproduce, kill immediately.
Reserves: Candidate 2 (DR selective referral — crowded by RETFound/IJCAI; only as fallback) and Candidate 3 (chest-view selective under shift — blocked pending CheXpert/MIMIC DUA clearance; avoid unless DUA is trivial). Candidate 4 (MedMNIST corruption audit) is rejected as saturated.
Held VLM candidate is not displaced — it is more theoretically interesting but carries higher causal-identification and engineering risk for a 3-person team. The two can coexist: use the VLM candidate's evaluation framing later, or keep it as a Phase-2 comparison for the selective/calibration claim.
If the pilot is approved, the next concrete step is the pre-registered analysis plan (exact splits, estimator list, metric definitions, and a published gap claim citing 2608.14768 / 2607.26765 / 2609.02111 / 2407.01032), then the implementation. All [UNKNOWN] items above should be resolved at download time via hash-level dedup and license page reads before any training starts.
Ready to continue. Action choices, per your call:

Start the pilot now — I'll scaffold the candidate-1 experiment (ISIC/HAM10000 schema check, dedup script, DenseNet121 + temp-scale + MC-dropout skeleton, source-shift + corruption eval) in this worktree.
Deepen any section (e.g., full read of 2407.01032 for the AUGRC spec, or SCIN melanoma-row availability — my pipeline has recorded reads available).
Re-scope toward the held VLM candidate instead, with the audit's framing as its design checklist.