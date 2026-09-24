The verification pass confirmed all load-bearing papers and surfaced a decisive new find (the "Mirage of Calibrated Confidence" TGS paper, 2609.18453). I now have enough primary-source grounding to write the full audit. Here it is.

ADVERSARIAL THESIS DISCOVERY AUDIT — Medical Imaging + Vision-Language Models
Auditor role: adversarial senior reviewer deciding whether a precise, defensible thesis question exists at Medical Imaging × VLMs × Trustworthiness/Reliability, and whether it beats the held question (below). Evidence labels: [VERIFIED] = confirmed on the primary source this turn; [INFERRED] = sound inference from verified facts; [UNKNOWN] = not yet checked.

1. Research Context
Medical VLMs are now evaluated for more than accuracy. Since early 2026 a dense reliability literature has formed: calibration benchmarks (MVC-Bench, 2608.27004), behavioral safety audits on brain MRI (2608.02790), selective/deferral systems (2606.15910, 2607.28696, 2608.18833), grounding audits that decouple visual from textual contributions (2607.03647, 2608.12928, 2609.03261), conflict/hallucination benchmarks (2608.24118, 2605.10002, 2606.24115), and confidence-grounding metrics (2609.06419, 2609.18453). Two meta-findings define the frontier: (i) medical VLM confidence is systematically untethered from visual evidence — models overstate sufficiency, stay confident under NOTA/perturbation, and verbalized confidence barely tracks what the image actually shows; (ii) obvious mitigations (prompting, abstention rules, CoT) frequently fail, while counterfactual, evidence-anchored interventions partially work.

The researcher team is a final-year CSE undergrad team (Bangladesh, 3 people) with strong Transformer/VLM grounding, Colab Pro (≤16 GB VRAM), a small commercial-API budget, and a requirement that the thesis stay AI/CSE-heavy. A prior audit already PROCEEDED the held question in the general (non-medical) lane.

2. Central RQ of this audit
Does any candidate at Medical Imaging × VLMs × Reliability beat the held question — "When a VLM receives directly contradictory visual and textual premises, does explicitly verbalizing the conflict (stating the contradiction before answering) causally change which source the model arbitrates toward, or does it merely rationalize a latent modality preference?" — on novelty, publishability, implementability on ≤16 GB VRAM, and fit to the team's resources?

If nothing beats it, the audit ends with: MEDICAL VLM RESEARCH DOES NOT CURRENTLY BEAT THE HELD RQ.

3. Candidate families A–G
Family	Definition	Occupancy after this audit
A	Contradiction/conflict detection & arbitration between visual and textual evidence	Occupied — MC-CXR, SIGNPOST-Bench, Which-Source-Wins, Same-Semantics, CARGO-VL, GACL all live here
B	Confidence calibration under modality degradation (both image- and text-side perturbation)	Occupied — DualRead (CCG-AUC), Just-How-Sure-Are-You, MVC-Bench, Which-Source-Wins
C	Selective prediction / abstention for ambiguous or unsupported cases	Occupied — Calibrated-Triage-Not-Autonomy, CALCoDe, EVADE, PARITY, uncertainty-NOT-safety-net
D	PEFT (LoRA) fine-tuning: accuracy vs calibration/confidence cost	Partially occupied / mechanical — OneStage LoRA medgemma (FLARE), Federated-LoRA-BiomedCLIP (AUC-only), CORAL; nobody measures a clean calibration trade-off, but the question is engineering-flavored, not mechanism-flavored
E	Evidence-sufficiency predictivity (can model/deployer predict when evidence is missing before/at answer time; modality-missingness self-explanation)	Partially occupied — I-Don't-Miss-You (interventional protocol, non-medical), EVADE ("escape" gating); medical transfer UNVERIFIED — the one genuinely open cell
F	Hallucination detection & grounding (counterfactual image substitution, mirage metrics, stepwise hallucination)	Occupied — CORAL/VRS/VHR, Do-Pathology-VLMs-Truly-See, Med-StepBench, GI-hallucination benchmark, MedQA-MM, mirage-detection
G	Arbitration mechanism under conflict (is the losing source encoded-but-overridden vs missing; does verbalization move the winner)	Open at exactly one point — GACL proves "encoded-but-overridden" in audio-language models and same-arith vision transfer; MC-CXR's pilot shows conflict-RULE instructions flip answers (GPT-5.5 only) but no paper tests case-level conflict verbalization as a causal intervention in any VLM, and none in medical VLMs
G is the only cell that is open, and it is the held RQ itself. Every other family is occupied or occurs in a confounded/partial form. That is the central structural result of this audit.

4. Critical literature search
Sources: alphaXiv (keyword + embedding discovery; full-text reads on the load-bearing papers), OpenAlex (checks; returned nothing relevant beyond a reporting-checklist and an LLM-adoption meta-analysis, both discarded). arXiv IDs used throughout.
Window: 2025-12 → 2026-09, recency-priority on follow-ups; no exclusion for preprint status (MedQA-MM and SHROOM-Visions are EMNLP 2026; several others are COLM/ICLR-tracked).
Loop cap obeyed: one initial + one follow-up round (16 discovery calls) this turn, plus 5 full reads carried in from the prior session (MC-CXR 2608.24118, DualRead 2609.06419, SameSemantics 2609.00550, I-Don't-Miss-You 2609.07596, Uncertainty-Not-a-Safety-Net 2606.16583) whose raw reads are on disk.
Inclusion: papers that state a reliability quantity (calibration error, coverage, abstention, flip/switch rates, grounding scores), on medical or clearly-transferable general VLMs. Method-proposal papers kept only if they report such quantities.
Exclusion: accuracy-only benchmark papers; score-inflation audits with no behavioral intervention.
5. Primary-source rules
Every claim below links to its alphaXiv source; https://www.alphaxiv.org/abs/<id> links are used for arXiv items (no bare arxiv.org links).
Numbers are quoted only from papers read in full this/prior session [VERIFIED] or from their own abstract [VERIFIED-ABS]. Everything else is [INFERRED]/[UNKNOWN].
"Occupied" never rests on a single abstract: I require either a direct result I can quote, or corroboration from ≥2 independent sources, before marking a cell occupied.
A paper is not treated as proof a gap is empty; absence of a tested intervention across 20+ surveyed papers is what makes "apparently open" defensible — and even then the pilot in MC-CXR is flagged as the bounded counter-evidence.
6. Required evidence table
Paper (Year)	Plane	Reliability problem	Method	Key quantities	Code	Data	Limitation	Occupancy mark
MC-CXR 2608.24118 (2026)	Med, CXR	Text vs visual context arbitration; switch-to-wrong under misleading context	Paired-perturbation benchmark; per-source switch & label-aligned error rates; GPT-5.5 rule pilot (Appendix D)	Misleading text flips 45.6–78.1% of correct image-only decisions (74.6% label-aligned); misleading visual flips 35.7–61.7% (17.6%); 57.0-pp asymmetry; IOR accuracy 8.3–35.8%; PC rule cut switches 54.8→37.0% (p=.0023) and 76.7→41.1% (p<.0001), PI naming no effect [VERIFIED]	[UNKNOWN]	PhysioNet (credentialed)	Only 240 cases; image-only-condition error rate high; single frontier model in pilot	Occupied / edge-open (verbalization cell)
2609.06419 DualRead (2026)	Med	Verbalized confidence not grounded in visual support	CCG-AUC counterfactual confidence-grounding; dual-state pre-answer solvability + post-answer visual-support read	ECE ≈0.031–0.17; CCG-AUC reveals whether confidence tracks real-image substitution [VERIFIED]	[UNKNOWN]	SLAKE, VQA-RAD, PathVQA, PMC-VQA, OmniMed, ReXVQA, OOD6	GRPO-trained actors only (Qwen3VL-2B, MedGemma1.5-4B)	Occupied (B)
2609.00550 SameSemantics (2026)	General	Modality preference arbitrary & order-dependent under conflict	13 MLLMs; text-vs-rendered-image-vs-parametric-knowledge conflict; SFT/DPO/steering	Preference flips with preprocessing (Qwen 9.71→−37.23); flip ratio ≤66.55%; conflict-aware SFT modest (misleading-image following 92.89→83.26%); prompting/steering/DPO fail [VERIFIED]	[UNKNOWN]	Synthetic text-rendered images only	No natural/medical images; did not test conflict verbalization	Occupied (A)
2609.07596 I-Don't-Miss-You (2026)	General	Models overstate modality sufficiency	Interventional protocol (model predicts answer-change under modality loss; then executes)	Predicted change ≤8.8% median vs executed 72.1%; insufficiency claims rare but precise (78–100%); 62/64 settings underpredict [VERIFIED]	[UNKNOWN]	mm-IMDb, IsoBench, GoldenView (non-medical)	No medical datasets	Partially occupied (E); medical transfer open
2606.16583 (2026)	Med, 8 modalities	NOTA (wrong-surface text) collapses accuracy without moving uncertainty	8 UE methods × 12 VLMs on GMAI-MMBench 1,680 samples	Accuracy drop 12.3–32.7% under →correct+nota, uncertainty nearly flat; baseline UE predicts flips (AUROC ≤0.858) [VERIFIED]	[UNKNOWN]	GMAI-MMBench (Apache-2.0)	MCQA-only	Occupied (B)
2608.27004 MVC-Bench (2026)	Med, 3 modalities	Medical-VLM calibration under domain shift	1,638 experiments; ECE/MCE/ACE; MCM regularization	MCM lowest ECE in 10/12 in-domain settings [VERIFIED-ABS]	[UNKNOWN]	Fundus, histopathology, CXR	Classification-only	Occupied (B)
2606.15910 CalibratedTriage (2026)	Med	Which confidence signal supports medical deferral	9 estimators × 5 LVLMs × 3 medical VQA sets; bounded selective prediction	At 20% tolerance ≈¼ radiology deferred under guarantee; ≈0 pathology; no estimator reliably best [VERIFIED-ABS]	[UNKNOWN]	Public medical VQA	No conflict test	Occupied (C)
2608.02790 ConfidentButUnreliable (2026)	Med, brain MRI	Verbalized-confidence audit separate from accuracy	6 VLMs, 4,102 images (250 subjects + controls)	ECE 0.27–0.40; mean conf on errors 0.82–0.97; 33–46% high-confidence errors [VERIFIED-ABS]	[UNKNOWN]	Public metadata + released masks	MCQA focus	Occupied (B/C)
2607.28696 CALCoDe (2026)	Med, derm	Class-tail undercoverage after clinical shift	Class-tail adaptive localized conformal deferral	Only method hitting 0.95 marginal + worst-class coverage in all 8 settings (HAM10000→ISIC2019/PAD-UFES-20; BiomedCLIP/CLIP/PubMedCLIP/MedSigLIP) [VERIFIED-ABS]	[UNKNOWN]	HAM10000, ISIC2019, PAD-UFES-20	Frozen CLIP-style encoders, not generative VLMs	Occupied (C)
2608.18833 EVADE (2026)	Med	Verification-gated abstention; single-model self-check unreliability	Consistent zoomed-view verification gate ("escape")	ECE cut ≤45% vs zero-shot; only method improving calibration + selective risk together (Qwen2.5-VL-7B; VQA-RAD/SLAKE/PathVQA) [VERIFIED-ABS]	[UNKNOWN]	VQA-RAD, SLAKE, PathVQA	7B cannot use localization to revise	Occupied (C/E)
2607.03647 CORAL (2026)	Med	Do med-VLMs actually see (grounding)?	Counterfactual surrogates (blank/shuffled/absent/hard-negative); VRS & VHR; LoRA fine-tune with contrastive grounding	CORAL-Qwen2.5-VL-7B: +6.7 pp accuracy, −8.0 pp VHR; substitution harms ≤6.5 pp medical vs 48–61 pp general [VERIFIED-ABS]	yes	PathVQA, PMC-VQA, SLAKE, VQA-RAD (n=400)	Small paired eval; disclosed overlap	Occupied (F)
2608.12928 PolishMedVQA (2026)	Med	Visual evidence underutilization	Ablations (image/question/both) + answer-choice-only control	Best model 79.0% full; above-chance from answer choices alone; worse on image-dominant questions [VERIFIED-ABS]	[UNKNOWN]	Polish board-exam VQA	Single language	Occupied (F)
2609.03261 MedQA-MM (2026)	Med	Route-level "reasoning inflation"; shortcuts	Prompt/image-side audits; modality ablations; shortcut-mitigated subset	Full 62.63% vs text-only 53.96% vs options-only 29.71%; on MedQA-MM subset text-only 5.21% [VERIFIED-ABS]	[UNKNOWN]	6 med MCQ sets (EMNLP 2026)	MCQ format	Occupied (F)
2606.27023 JustHowSure (2026)	Med	Verbalized confidence training calibration	Composite loss w/ 2×2 image-presence × text-integrity factorial anchor	≥60% ECE cut, ≥26% discrimination gain, accuracy preserved (MedGemma-4B-IT, Qwen2-VL-7B) [VERIFIED-ABS]	yes	3 Med VQA benchmarks	Training-based; measures but doesn't test arbitration	Occupied (B)
2609.18453 MirageOfCalibration (2026)	General	Verbalized confidence ≈ trajectory-independent (rationalization-type evidence)	Trajectory-Grounding Scores (TGS-self/pair); TGS-Bench over 10 benchmarks	Models say "wait, recheck," stay wrong, remain confident; calibration training can worsen trajectory-independence; TGS rankings diverge from ECE rankings [VERIFIED-ABS]	[UNKNOWN]	TGS-Bench	Non-medical	Occupied (B, mechanistically relevant to Held RQ)
2606.05161 GACL (2026)	Audio→Vision transfer	"Encoded-but-overridden" arbitration mechanism	Same-audio counterfactual; activation patching to answer-position computation	64.1% of conflicts sign-flip when conflicting text removed; patching tracks candidate-score diffs (ρ=0.93); training-free GACL +17.8 nAUC, transfers to vision +40.5 pp [VERIFIED-ABS]	[UNKNOWN]	Audio tasks + vision-transfer	Not medical; decoding-level	Occupied (G-mechanism, non-medical)
2608.04509 CARGO-VL (2026)	General	Training-time counterfactual arbitration (A/V/T/N states)	Group-relative optimization w/ transition rewards + primal-dual risk control; XMC resource	Improves conflict handling & unsupported-answer avoidance over pointwise baselines [VERIFIED-ABS]	[UNKNOWN]	XMC, CMC-Bench, Modality-Bias	Training-based; doesn't isolate verbalization	Occupied (A, training side)
2608.17205 WhichSourceWins (2026)	General	Task-dependent modality reliance under degradation	Dirichlet of image/text degradation, 4 levels each; likelihood margins	5/6 models shift away from degraded text more than degraded image on arithmetic; reversal on ChartQA-Conflict across all 6 + 2 frontier APIs [VERIFIED-ABS]	yes	GSM8K/SVAMP conflicts; ChartQA-Conflict (229)	Not medical	Occupied (A/B, transferable)
2605.10002 Med-StepBench (2026)	Med, PET/CT	Stepwise hallucination; adversarial plausible explanations amplify	Hierarchical 4-stage reasoning, 1M+ image-statement pairs	Stage-level failure modes; plausible intermediate explanations amplify hallucination despite contradictory visuals [VERIFIED-ABS]	[UNKNOWN]	3D oncological PET/CT (12k+ images)	Volumetric; heavy	Occupied (F)
2606.24115 GI-hallucination (2026)	Med, endoscopy	Hallucination-detection across method access levels	9 detectors × 5 VLMs; white-box vs black-box	ReXTrust best (AUC 93.0 on MedGemma-4B); white-box avg +19.5 AUC pts; confident confabulation breaks consistency methods [VERIFIED-ABS]	[UNKNOWN]	Gut-VLM (4,392 pairs)	Detection only	Occupied (F)
Occupancy summary: 0 of 7 families is unoccupied; E and G are the only partially-open cells; and G's open point is specifically the held RQ's intervention.

7. Dataset audit
Dataset	Modalities	Size	Access / license	Status
[GMAI-MMBench]	USMLE-style medical MCQA, 8 imaging modalities	1,680 balanced subset used in 2606.16583	Apache-2.0 [VERIFIED]	✅ usable
SLAKE	CXR, MR, CT bilingual EN/ZH VQA	14,028 rows (train 9,840 / val 2,100 / test 2,090)	HF BoKelvin/SLAKE, CC-BY-4.0 [VERIFIED]	✅ usable
VQA-RAD	Radiology, 3,515 QA	~3.5k	Public [VERIFIED]; license text [UNKNOWN]	✅ usable
PathVQA	Pathology	~33k	Public [VERIFIED]; license [UNKNOWN]	✅ usable
PMC-VQA	Multi-modal biology	227k curated	Public; corpus-reuse screening warned by authors [INFERRED]	⚠️ check fair-use gate
MC-CXR	CXR, conflicting context pairs	240 cases / 2,522 instances	PhysioNet (credentialed) [VERIFIED]	⚠️ red-tape heavy for this team
CheXpert / MIMIC-CXR	CXR + reports	large	AIMI registration / PhysioNet+DUA [VERIFIED]	⚠️ restricted
HAM10000 / ISIC2019 / ISIC2020 / PAD-UFES-20	Derm	10k+	HAM10000 CC-BY-NC; ISIC20 CC-BY-NC; PAD-UFES CC BY 4.0 [VERIFIED]	✅ usable
DDI (derm)	Derm	656	Stanford AIMI research-use used by 2607.28696 [VERIFIED]	⚠️ agreement
SCIN	Derm clinical	10k+	SCIN license used by 2607.28696 [VERIFIED]	⚠️ agreement
Bottom line: there is a clean, freely-accessible stack — GMAI-MMBench (Apache-2.0, 1,680 fast subset), SLAKE (CC-BY-4.0), VQA-RAD, PathVQA — with derm datasets as backups. MC-CXR is the ideal substrate for any conflict question but its PhysioNet credential plus a 240-case ceiling makes it a delivery risk for a small undergrad team; a conflict corpus can instead be built from GMAI-MMBench/SLAKE by pairing a real image with a synthetically contradictory text premise (the exact construct MC-CXR and Which-Source-Wins already validate).

8. Model audit (with VRAM math on ≤16 GB)
Model	Params / size	License	VRAM feasibility	Notes
Qwen2.5-VL-7B-Instruct	8.29 B, 16.60 GB (fp16)	Apache-2.0 [VERIFIED]	⚠️ fp16 > 16 GB; 4-bit ~5 GB or A100 fine	Default open choice; used by EVADE, CORAL, Which-Source-Wins
Qwen3VL-2B	~2-3 B	Apache-2.0 [INFERRED]	✅ T4-safe	DualRead's actor; cheap pilot
MedGemma-4B (it)	~4 B	HF gated: Health AI Developer Foundations ToS [VERIFIED]	✅ ~8-10 GB fp16	GI-hallucination, JustHowSure, DualRead all use it; gate is per-user approval
LLaVA-Med-7B	~7 B	Weights on HF kms-healthcare/llava-med, Transformers/vLLM/SGLang-ready [VERIFIED]	⚠️ 4-bit feasible	Medical specialist; used in GI-hallucination benchmark
MedGemma1.5-4B	~4 B	HF gated (see above) [VERIFIED]	✅	DualRead backbone
InternVL3-8B / LLaVA-v1.6-7B / Molmo-7B	7-8 B	mix Apache/MIT/non-commercial per 2606.16583 Table 4 [INFERRED]	⚠️	Route only if needed
GPT-5.x / Gemini (API)	—	Proprietary	n/a (API $)	MC-CXR used GPT-5.5 in its pilot; small API budget usable for a control condition
Bottom line: everything needed for a causal verbalization study exists open: Qwen3VL-2B (T4-safe) and Qwen2.5-VL-7B (4-bit) for pilots, MedGemma-4B if the ToS gate clears (deliverable risk), LLaVA-Med as a medical-specialist control. No compute blocker for this team.

9. Candidate RQs (≤5, with H0/H1 blocks)
R1 — Verbalized conflict as a causal arbitration switch in medical VQA (= held RQ medicalized)
H0: Explicitly verbalizing a text-vs-image conflict before answering does not change which source wins (any apparent effect is preference rationalization). H1: It causally redirects arbitration (toward image when image is correct; toward text when text is correct).
Intervention: Wording condition at prompt level — (a) direct answer [BL], (b) "state the contradiction between the image and the text, if any" [VERB], (c) generic image-first naming control [PI, replication of MC-CXR no-effect], (d) explicit conflict rule "when text and image disagree, trust the image" [PC, replication of MC-CXR effect].
Control: same 4 conditions on non-conflict cases (must leave answers unchanged: instruction sensitivity check); case pairing so every conflict has a matched aligned twin.
Metrics: switch-to-wrong rate; label-aligned switch rate; answer-change rate under VERB vs PI vs PC; per-model × per-direction.
Expected failure (adversarial): VERB behaves like PI (no effect), i.e., verbalization is inert — which is itself the rationalization result.
Most likely negative-result form: "verbalizing the conflict changes nothing; only the rule changes arbitration" → clean, reportable, thesis-sized.
Novelty audit: MC-CXR's Appendix D is the only predecessor and it is confounded (bundled rule + preference + naming into single prompts; GPT-5.5 only; no clean VERB arm, no non-conflict control). [VERIFIED from full read] No published paper isolates VERB in medical VLMs. Appears open.
R2 — Transfer the I-Don't-Miss-You intervention to medical VQA (evidence-sufficiency predictivity)
H0: Medical VLMs' predicted answer-change under modality subtraction matches executed change (calibrated self-knowledge). H1: Systematic underprediction (like the general result), flaggable in advance.
Intervention: template protocol of 2609.07596 on GMAI-MMBench/SLAKE: ask "would your answer change without the image?" then actually abstain/answer and compare.
Metrics: predicted-vs-executed change rate, precision of insufficiency claims, by modality (CXR/MR/CT vs derm).
Expected failure: the general finding (72.1% executed vs ≤8.8% predicted) may be task-specific; medical MCQA might be less overclaiming because options carry the burden.
Novelty audit: protocol exists (general), medical transfer untested as of this pass. open but incremental — it ports a method, it doesn't expose a mechanism.
Status: RESERVE.
R3 — Confidence under simultaneous image-degradation + text-conflict (CCG-style) on open models
H0/H1: DualRead already answers "does confidence drop when the image flips the answer." Blending-in text conflict might disturb it, but the metric and directionality are pre-owned.
Status: REJECT as primary — overlaps B/G; would read as an ablation of 2609.06419 with different axes.
R4 — NOTA-flip predictability as a deployable gate (baseline uncertainty predicts which medical predictions flip)
2606.16583 already reports flip-prediction AUROC ≤0.858 under NOTA. A pure reproduction on one more dataset adds nothing; an image-side NOTA analog (perturb the image, predict flip) is the only new angle and has an ambiguous signal (image-side switches are smaller and less aligned).
Status: RESERVE-at-best / likely REJECT.
R5 — PEFT (LoRA) accuracy-vs-calibration audit on a medical VLM
LoRA-tuned med-VLM (e.g., One-Stage Mixture-of-LoRA on MedGemma1.5-4B, MedFG-VQA, FOLTMed) vs base on ECE/confident-error. Mechanical, no mechanism, easily scooped.
Status: REJECT.
10. Strong candidate patterns A–E — viability check
Pattern A (contradiction detection): Viable as task but saturated (MC-CXR, SIGNPOST-Bench, CARGO-VL, GACL). The only A-vacancy is mechanism-level (G), not detection-level (A).
Pattern B (confidence under degradation): Saturated (DualRead, JustHowSure, MVC-Bench, WhichSourceWins). Not viable as primary.
Pattern C (selective prediction for ambiguity): Saturated (CalibratedTriage, CALCoDe, EVADE, PARITY). Only a new failure axis (e.g., ambiguity that is induced by cross-modal conflict rather than by image difficulty) would be novel — that is again G, not C.
Pattern D (PEFT accuracy-vs-calibration): Not saturated as a measurement, but is an engineering audit with no mechanism; weak thesis core.
Pattern E (evidence-sufficiency predictivity): Open in medical; transferable protocol from I-Don't-Miss-You; moderate novelty, methodology risk; status RESERVE.
Only the intersection A∩C (conflict-driven selective behavior) — i.e., the held RQ — has both novelty and a mechanism.

11. Control requirements (for whichever candidate pilots)
Non-conflict control arm matched to every conflict case (rule out instruction sensitivity).
Directional control: conflict cases balanced so image-correct ≈ text-correct (else "arbitration" is just accuracy).
Placebo-verbalization control: a "talk about the image" instruction (verbal output without naming the contradiction) isolates verbalization from verbosity.
Confound-rule control: separate naming the discrepancy (informational) from specifying who wins (prescriptive) — the exact MC-CXR PI-vs-PC decomposition their pilot conflated.
Order randomization (which source is presented first; option ordering for MCQA) per 2609.00550 and MedQA-MM.
Answer-option leakage gate: include the options-only control of 2608.12928 to bound how much of any "arbitration" is from answer choices.
≥2 open model families (Qwen, MedGemma-or-LLaVA-Med) plus, if budget permits, one frontier API arm.
12. Closest-work autopsy (two strongest)
Autopsy 1 — MC-CXR Appendix-D pilot vs R1. The pilot is the only published test of "make the model aware of the conflict and see who wins." But it (i) bundles a prescriptive rule ("prefer the image") with the conflict acknowledgment into one prompt, (ii) had no naming-only arm (its PI naming arm showed no effect — strong prior against R1), (iii) ran one model (GPT-5.5), (iv) tested no non-conflict control, and (v) is buried in an appendix of a perturbation benchmark whose own headline is the failure of image-only conditions (IOR 8.3–35.8%). R1's delta vs this autopsy: a clean 2×2 (rule × naming) crossing on ≥2 open models with non-conflict controls. The pilot's PI-null is the honest-pre-registration concern: it suggests acknowledgment alone may be inert — which is precisely the rationalization hypothesis R1 is built to adjudicate, not a reason R1 is redundant.

Autopsy 2 — Mirage-of-Calibrated-Confidence (TGS) + GACL vs R1's mechanism. TGS proves verbalized confidence is trajectory-independent (the model reasons badly, keeps high confidence, even after calibration training) — the closest existing evidence that post-hoc verbal explanation rationalizes rather than reflects computation; GACL proves, in a different modality (audio), that the "losing" source is encoded-but-overridden at answer time (64.1% sign-flip under counterfactual, patching localized to answer-position computation). Both directly predict R1's outcome space, but neither applies its mechanism probe to medical VLMs nor to the verbalization intervention. R1 would be the first causal test of verbalization as the intervention, in both general and medical domains, with a direction the two autopsies already triangulate.

13. Feasibility autopsy (≤16 GB VRAM, Colab Pro, 3-person team, ~months of work)
Fine-grained: patience. Tens of thousands of runs on the 4-condition design across 2 model families × ~200 cases are trivially colab-able (CheXpert-mc-style deployment or GMAI-MMBench subset). No 100+ GPU-hour requirement.
VRAM: Qwen3VL-2B T4-safe; Qwen2.5-VL-7B works in 4-bit; LLaVA-Med 4-bit; MedGemma-4B ~8 GB fp16 but HF-ToS gate is a schedule risk. All four feasible.
Data: SLAKE + GMAI-MMBench + VQA-RAD cover the arcs with zero red tape; MC-CXR is a stretch goal, not a dependency.
Analysis cost: switch-rate + Fisher/matched-pair stats + AUROC — senior-thesis level.
Risk concentrated in one place: the PI-null prior (see autopsy 1). Mitigated by the fact that a null verbalization result is a clean negative thesis, and the 2×2 rule-arm (PC) is expected to replicate a positive effect, giving the thesis a finding either way.
14. Medical-scientific validity (skeptic pass)
Label quality: GMAI-MMBench/CheXpert-style MCQ labels can hide the shortcut routes that 2609.03261 exposes (from-options accuracy up to ~12% even after mitigation). Mitigate with the options-only and text-only controls in §11.6.
"Arbitration" as a proxy: a switch-to-wrong metric presupposes knowing which source is right; on real medical pairs this rests on release labels. Build conflates from verifiable contradictions (flipped presence/absence statements about known findings) rather than subtle disagreements.
ETHICS & CLAIM-SIZE: a thesis claiming "verbalization changes clinical arbitration" must not imply clinical deployability; the truthful claim is a mechanism result about arbitraation, not a diagnostic result. No human-subjects risk, no patient data (all public).
LLM-as-judge risks for any open-answer scoring: avoid by closed-set answer extraction with exact/near-match scoring; do not use a judge model as ground truth.
Generalizability: 2 model families × 1-2 modalities is pilot-grade; the thesis must present this as a controlled mechanism study, not a clinical evaluation.
15. Compare vs the held RQ (R1-in-medicine vs held RQ, 12 criteria, no numeric score)
#	Criterion	Medical R1	Held RQ (general)
1	Novelty of intervention	Same intervention (verbalization) — none has tested it, in either lane	Identical
2	Mechanism specificity	Equal (adjudicates rationalization vs causal arbitration)	Equal
3	Reader interest / motivation	Medical stakes raise NRT; conflicts are real (report-vs-image disagreements occur daily)	Clean, but abstract
4	Prior experimental risk	Higher: medical benchmarks carry more hidden shortcuts (MedQA-MM), weaker image-only baselines (MC-CXR IOR 8.3–35.8%)	Lower: synthetic conflicts have ground-truth arbitration
5	Data logistics	Public stack fine; ideal substrate credential-gated	Synthetic, zero friction
6	Compute fit (≤16GB)	Fits (all candidate models local)	Fits
7	Publishability	Distinct: first causal verbalization result on medical VLMs	Distinct: first in general VLMs
8	AI/CSE relevance	Strong — but "medical" may invite a clinical-reader bar the team cannot meet	Strongest fit to team background
9	Team risk (3 undergrads)	Medium-high (domain validation, leakage audits, ToS gates)	Low-Medium
10	Negative-result value	High (rationalization finding is clinically important)	High
11	Control-rigor needed	Higher (more confounds to design against)	Moderate
12	Distinctiveness vs both SOTA lanes	Beats both (nothing else isolates verbalization)	Beats both
Verdict on this row: the medical lane does not outrank the held RQ on novelty, fit, or publishability — it tightens the held RQ's motivation while raising data/validity risk. It is the same experiment in a stronger-motivation packaging.

16. Decision
R1 → PROCEED TO PILOT — but as the medical instantiation of the held RQ, not as a competitor. The pilot is the §17 task.
R2 (evidence-sufficiency transfer) → RESERVE — viable fallback whose protocol is pre-validated by 2609.07596.
R3, R4, R5 → REJECT (occupied by DualRead / uncertainty-NOT-safety-net / and mechanical-audit, respectively).
Net: the medical-VLM lane contains no independent question that beats the held RQ; its best question is the held RQ. So, as instructed:

MEDICAL VLM RESEARCH DOES NOT CURRENTLY BEAT THE HELD RQ.

The held RQ stands; the medical audit strengthens its claim by contributing the strongest existing motivation (report-vs-image conflict is a real clinical failure) and two useful empirical priors (PI-null → rationalization is plausible; PC-effect → a bound exists).

17. Strongest surviving question + verification task
Surviving question (held RQ, medicalized):

In medical VQA, when a model receives a direct contradiction between the image and a text premise, does explicitly verbalizing the contradiction before answering shift which source wins — or does it only rationalize an unchanged latent preference? Mediating split: naming the discrepancy (information) vs prescribing a winner (rule).

60–90 minute verification task (manual, no code):

Take 20 conflict cases from SLAKE or GMAI-MMBench (or public CXR pairs) where a text premise is constructed to directly contradict the image's correct answer (flip presence→absence of a finding). Prepare each case in 4 wordings: BL (direct), VERB (state the contradiction, then answer), PI (image-first naming), PC (rule: when text disagrees, trust the image). Same 20 cases also as aligned (non-conflicting) twins → 40 cases × 4 conditions.
Run Qwen3VL-2B (Colab T4, free) through the model's hosted chat UI or a minimal Colab snippet you already know how to run; no new code to write.
Tally switch-to-wrong and answer-change rate per condition, and compute the coarse split: does VERB behave like PI (no change → rationalization confirmed) or like PC (change → causal arbitration)?
Falsification bar (decision in one line): if VERB vs BL answer-change = 0/20 on conflict cases while PC vs BL > 0, R1's mechanism claim is falsified (verbalization is inert; rule is the active ingredient) — that negative result is still a complete, defensible thesis. If VERB moves ≥ 8/20 cases toward the image-correct side, the mechanism holds and the thesis design proceeds with the §11 control suite.
That single open-ended experiment takes well under 90 minutes, uses zero new code, fits the team's budget, and returns a binary-ish verdict that directly decides whether the piloted thesis is the rationalization claim or the causal claim.

The audit is delivered (§1–17 above). Remaining natural next steps, in order of value:

Persist the audit — save this as a durable artifact in the project artifacts directory (loads cleanly with orx-reports), so it isn't lost in chat.
Package the §17 verification task for the human — turn the 4-condition design into a short, executable checklist (cases + wordings + tally sheet) the team can run in one sitting.
Set up the pilot environment — if you authorize compute, I can lock in a Colab-style dependency snapshot (Qwen3VL-2B or 4-bit Qwen2.5-VL-7B) and draft the pilot script per the §11 control suite.
Which of these do you want next — or should I stop here and let the team run the §17 falsification task first?

