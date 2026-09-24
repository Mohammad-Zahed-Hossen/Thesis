# Cross-Paper Synthesis: Evidence-Grounded Selective Prediction for Reliable Bangla Cultural VLMs

Candidate field under evaluation (candidate Proposal 3):

> Combining answer confidence, visual-grounding confidence, and external cultural evidence can improve uncertainty calibration and selective prediction for Bengali cultural entity recognition.

Status: **evidence discovery, verification, and synthesis only.** No pilot design, no research-question freeze, no proposal ranking, no thesis decision. Inferences are explicitly labeled as such.

Method: primary-source verification via alphaXiv / OpenAlex retrieval (each cited work was verified against its source record; six load-bearing papers read in full text), plus two user-supplied prior audits treated as context to verify, not gospel.

---

## 1. Literature map

Eight clusters. IDs are verified primary sources; full links in §8.

### A. Selective prediction foundations (text/classification)
- SelectiveNet [1901.09192](https://arxiv.org/abs/1901.09192) — end-to-end reject option; risk–coverage optimization.
- Xin et al. [2022.findings-acl.158](https://aclanthology.org/2022.findings-acl.158/) — 17 datasets, IID/OOD/ADV: **no method consistently and considerably outperforms the MaxProb (softmax) baseline**.
- A-CRC-QA [2608.12008](https://arxiv.org/abs/2608.12008) — post-hoc conformal risk-controlled selective QA (asymptotic control for non-monotone loss).
- CAUC [2609.11446](https://arxiv.org/abs/2609.11446) — calibrated confidence gives thresholds an *explicit selective-risk interpretation*.
- "Know Your Limits" [10.1162/tacl_a_00754](https://doi.org/10.1162/tacl_a_00754) — abstention survey for LLMs.

### B. Multimodal selective prediction / selective VQA
- Whitehead et al., *Reliable VQA: Abstain Rather Than Answer Incorrectly* [2204.13631](https://arxiv.org/abs/2204.13631) — softmax abstention covers <7.5% of questions at 1% risk; a *learned multimodal selection function* gives 2.3× coverage (6.8% → 15.6%).
- *Learning from Your Peers* (LYP) [2306.08751](https://arxiv.org/abs/2306.08751) — 32.92% C@1% in-domain (doubling prior best); 25.38% C@1% under mixed ID/OOD vs <5% for softmax.
- *Selectively Answering Visual Questions* [2024.findings-acl.250](https://aclanthology.org/2024.findings-acl.250/) — calibration of in-context LMMs on answerability benchmarks; AVG BLEU score.
- ReCoVERR [2024.findings-acl.767](https://aclanthology.org/2024.findings-acl.767/) — inference-time clue collection reduces over-abstention; up to +20% answered without accuracy loss.
- FinReliable [2608.19558](https://arxiv.org/abs/2608.19558) — selective NER under domain shift; confidence *ranking* changes under shift; gating fails under extreme shift.

### C. VLM confidence estimation & calibration
- BICR [2605.10893](https://arxiv.org/abs/2605.10893) — *visual ungroundedness*; blind-image contrastive ranking; best calibration + discrimination simultaneously across 5 LVLMs.
- TRAPSBench [2608.13167](https://arxiv.org/abs/2608.13167) — VLMs encode but fail to *express* epistemic restraint; probes decode answerability at 0.91 AUROC; visual vs textual uncertainty gap ~4×.
- MVC-Bench [2608.27004](https://arxiv.org/abs/2608.27004) — calibration-centric benchmark; ECE/MCE/ACE across backbones/domains.
- Instinct vs. Reflection [2604.17274](https://arxiv.org/abs/2604.17274) — token vs verbalized confidence.
- Rethinking Correctness for UE [2609.15180](https://arxiv.org/abs/2609.15180) — correctness criterion changes UE conclusions (up to 0.146 AUROC).
- MLLM uncertainty survey [2608.17084](https://arxiv.org/abs/2608.17084).

### D. Visual grounding as a reliability signal
- SIEVES [2604.25855](https://arxiv.org/abs/2604.25855) — explicit localized visual evidence → learned selector; ~3× coverage on OOD; transfers to closed models (o3, Gemini-3-Pro).
- CVE-SAI [2608.25023](https://arxiv.org/abs/2608.25023) — counterfactual visual evidence → risk-controlled selective admission (e-commerce attribute completion).
- SPC [2607.29240](https://arxiv.org/abs/2607.29240) — commonsense prior overrides visual evidence; *selective prior calibration* (e.g., six-fingered hand).
- Evidence-Order Calibration [2609.09184](https://arxiv.org/abs/2609.09184) — evidence-monotonicity violations (EMVR 0.436) separable from correctness discrimination; native confidence stayed stronger for risk ranking.
- SAVOR [2609.16601](https://arxiv.org/abs/2609.16601) — GRPO with confidence-calibrated objective; revisit evidence on uncertainty.
- ChitraMiti [2609.12509](https://arxiv.org/abs/2609.12509) — Bengali visual-grounding / modality-reliance diagnostics.
- VCD / VL-Uncertainty / SVAR / TVI — contrastive-degradation family (referenced within BICR).

### E. Evidence acquisition / externalization
- BCEA [2606.16667](https://arxiv.org/abs/2606.16667) — budgeted conformal evidence acquisition; answer/abstain/acquire.
- M4-RAG [2512.05959](https://arxiv.org/abs/2512.05959) — massive multilingual-multicultural-multimodal RAG evaluation.
- FinAbstain [2607.24875](https://arxiv.org/abs/2607.24875) — multimodal RAG selective forecasting (explicitly labeled simulated results).
- ERAG/EvidentialRAG [2607.10491](https://arxiv.org/abs/2607.10491) — information conflict in RAG.
- CARGO-VL [2608.04509](https://arxiv.org/abs/2608.04509) — counterfactual evidence states; abstain when sources disagree.
- Dynamic evidence reading [2211.12707](https://arxiv.org/abs/2211.12707).
- Conformal abstention via self-consistency [2405.01563](https://arxiv.org/abs/2405.01563).
- "Don't Hallucinate, Abstain" [2024.acl-long.786](https://aclanthology.org/2024.acl-long.786/) — knowledge gap detection via answerability.

### F. Hallucination & knowledge-application gaps
- M²CQA [2602.05437](https://arxiv.org/abs/2602.05437) — counterfactual reasoning hallucination (MENA/multilingual); **reasoning-first prompting increases counterfactual hallucination**.
- CulturalMenuBench [2609.03526](https://arxiv.org/abs/2609.03526) — knowledge-application gap: >94% on recognition drops to ≤56% on cultural attribution; dish names beat images by +7–18 pts; error patterns consistent with random guessing.
- "Staying VIGILant" [2606.26387](https://arxiv.org/abs/2606.26387) — visual laziness.
- VisER [2608.30480](https://arxiv.org/abs/2608.30480) — visual-evidence-reliance hallucination detection.
- GopherCite [2203.11147](https://arxiv.org/abs/2203.11147) — evidence + abstention helps, but "evidence-supported ≠ true".

### G. Culture / language benchmarks & resources
- BanglaVerse [2603.21165](https://arxiv.org/abs/2603.21165) — Bengali cultural VQA: 1,152 images, 9 domains, ~32.2K artifacts.
- BanglaProtha [10.1109/wacv61042.2026.00119](https://doi.org/10.1109/wacv61042.2026.00119) — WACV 2026; Bengali culture, multiple-choice, aspect-based.
- KhatianDoc [2609.03597](https://arxiv.org/abs/2609.03597) — Bengali land-records QA; zero correct on 39.3% of categories.
- CVQA + WORLDCUISINES — absorbed into M4-RAG evaluation.
- ImageEval 2026 / AynVQA + CRAI-Bench [2608.30475](https://arxiv.org/abs/2608.30475) — Arabic, culturally grounded multimodal evaluation incl. hallucination detection.
- CultureVLM [2501.01282](https://arxiv.org/abs/2501.01282).
- Figurative-and-cultural transfer [2608.18361](https://arxiv.org/abs/2608.18361) — cultural fine-tuning can *destabilize* historically grounded factual knowledge.

### H. Bengali / low-resource VLM internals & NLP
- Where Do Multilingual VLM Encoders Fail? [2608.30725](https://arxiv.org/abs/2608.30725) — Bengali an explicit low-resource case; failure located in the **EOS hidden-state trajectory** (substituting the English-aligned value lifts Swahili 22.1 → 69.1 pp); linear language bias is a symptom, not cause.
- BengaliMCQ [2608.15547](https://arxiv.org/abs/2608.15547) — structure-aware Bengali retrieval for academic MCQs.
- BnBERT-iPET [2608.05104](https://arxiv.org/abs/2608.05104) — sparse few-shot Bengali LM.
- DocTalkBN [2608.27110](https://arxiv.org/abs/2608.27110) — Bengali telemedicine dataset.

---

## 2. Closest-work matrix

Full-depth reads marked †.

| Paper | Task | Confidence / selection signal | Visual grounding | External evidence | Culture / language | Gap re: thesis |
|---|---|---|---|---|---|---|
| SIEVES † [2604.25855](https://arxiv.org/abs/2604.25855) | Selective VQA | learned selector on localization quality | **core** | none | none | Selection-from-grounding solved; no culture, no external evidence |
| BCEA † [2606.16667](https://arxiv.org/abs/2606.16667) | VQA with acquire option | conformal filter + acquisition | partial (masking test) | **acquired per claim** | none | Naive acquisition breaks, gating restores; no culture, no low-resource |
| BICR † [2605.10893](https://arxiv.org/abs/2605.10893) | Confidence estimation | probe on hidden states + blind-image rank | **core** | none | English only | Grounding→confidence solved; multilingual transfer *explicitly untested* (their limitation) |
| TRAPSBench [2608.13167](https://arxiv.org/abs/2608.13167) | Epistemic restraint | PECS, probes, uncertainty-gap analysis | secondary | none | multilingual (non-Bengali) | Diagnosis tool; no selection mechanism |
| M4-RAG † [2512.05959](https://arxiv.org/abs/2512.05959) | Multilingual-multicultural-multimodal RAG eval | none (accuracy only) | passive (mmE5/B3 retrieval) | **core** | **42 langs, 189 countries** | External-evidence landscape characterized; integration bottleneck + inverse scaling; no confidence/selection |
| FinAbstain [2607.24875](https://arxiv.org/abs/2607.24875) | Selective forecasting + RAG | composite uncertainty + abstain/acquire | modality-specific agents | **core** | none (finance) | Same architecture; no culture, no vision grounding |
| CARGO-VL [2608.04509](https://arxiv.org/abs/2608.04509) | VQA selective, counterfactual evidence states | abstain when sources disagree | counterfactual states | evidence states | none | No acquisition/budget |
| ChitraMiti [2609.12509](https://arxiv.org/abs/2609.12509) | Bengali multimodal geometry | none (accuracy + modality reliance) | **core (modality checks)** | none | **Bengali** | Closest existing Bengali visual-grounding diagnostic; no cultural entities, no selection, no confidence |
| CulturalMenuBench [2609.03526](https://arxiv.org/abs/2609.03526) | Cultural food attribution | none | active (trojan tests) | none | 10 langs / 18 regions | Demonstrates the cultural *knowledge-application gap* the thesis leans on; no confidence/selection; not Bengali |
| BanglaVerse † [2603.21165](https://arxiv.org/abs/2603.21165) | Bengali cultural VQA benchmark | none | diagnosis only | none | **Bengali** | Supplies the task domain; its conclusion conflicts with thesis premise (§3) |
| Evidence-Order [2609.09184](https://arxiv.org/abs/2609.09184) | Selective visual reasoning under evidence loss | reliability head on states+conf+entropy | **core** | none | English/GQA | Order-consistency ≠ correctness ranking; native confidence stayed stronger |
| SPC [2607.29240](https://arxiv.org/abs/2607.29240) | Commonsense-vs-image conflict | prior subtraction, instance-weighted | **core** | none | none | Shows text prior overriding visual evidence — the mechanism "grounding confidence" targets |
| Reliable VQA [2204.13631](https://arxiv.org/abs/2204.13631) / LYP [2306.08751](https://arxiv.org/abs/2306.08751) | Selective VQA foundations | learned selection functions | weak | none | none | Baseline machinery; culture-free |

---

## 3. Contradiction table

| # | Paper A | Paper B | Where they conflict | Why it matters / unresolved |
|---|---|---|---|---|
| 1 | BanglaVerse: bottleneck is *missing cultural knowledge*, not visual grounding | TRAPSBench: VLMs *encode* answerability (0.91 AUROC) but fail to *express* it | Location of failure: absent knowledge vs present-but-inaccessible | If knowledge is absent, confidence-based selection can't help. If present-but-inexpressible, internal/probe signals could. No Bengali test arbitrates |
| 2 | BanglaVerse: knowledge absent | CulturalMenuBench: knowledge *present* but *cannot be activated through visual input* (names beat images +7–18 pts) | Channel of failure: memory vs perception-to-knowledge activation | Two hypotheses the thesis's "grounding + evidence" framing straddles; they predict opposite research programs |
| 3 | M4-RAG: external evidence *hurts* larger models (−1.75 pp Gemma3-27B); text-based retrieval degrades below no-RAG; multilingual evidence −32.4 pp | BCEA / FinAbstain / ReCoVERR design assumption: retrieving evidence at abstention time *improves* reliability | Evidence utility is not monotonic; depends on scale, language, retrieval modality | The "external cultural evidence improves selection" component is the most vulnerable; M4-RAG already characterizes when it fails |
| 4 | SIEVES: grounding-based evidence scoring generalizes OOD (~3× coverage) | Evidence-Order: evidence-supervised heads *don't beat native confidence* for risk ranking; Xin 2022: nothing beats MaxProb consistently | Grounding supervision's marginal value over simple confidence, and across benchmarks | Bears on whether a *combined* confidence is more than a trivial ensemble |
| 5 | BICR: visual ungroundedness must be trained against; suppressing correct-but-ungrounded confidence is *desired* | BanglaVerse / CulturalMenuBench: correct answers plausibly arrive *without* image grounding exactly when cultural knowledge fills in | BICR's L_rank penalizes the *knowledge-answered-without-image* population — which cultural benchmarks say is large and *correct* | Charged interaction: in Bengali cultural VQA, the population BICR deems "ungrounded" may overlap heavily with the population the thesis wants to answer |
| 6 | M4-RAG: oracle context → 94–99% (perfect evidence drives near-perfect accuracy) | Bangla audit (user-supplied): external retrieval returns ground-truth entity names verbatim → task degrades to reading comprehension | "Evidence helps" can be an artifact of answer leakage, not visual identification | Threatens construct validity of any external-evidence arm in cultural entity recognition |
| 7 | BICR needs hidden states (open-weight only) | This project: resource-constrained local compute, no runs yet | — | Operational constraint, not literature; noted for later phases, not this synthesis |

---

## 4. Pre-emption audit

| Claim component | Occupying work | Verdict |
|---|---|---|
| Grounding-based selective prediction | SIEVES, CVE-SAI, Evidence-Order, SPC | **Occupied** (2026) |
| Confidence calibration for VLM hallucination | BICR, TRAPSBench, SAVOR, MVC-Bench | **Occupied** |
| Answer/abstain/acquire with budget | BCEA, ReCoVERR, FinAbstain, CVE-SAI | **Occupied as a framework** |
| Multilingual-multicultural multimodal RAG landscape | M4-RAG | **Occupied as a measurement** |
| Cultural knowledge-application gap in VLMs | CulturalMenuBench, BanglaVerse, ImageEval/Arabic | **Occupied as a diagnosis** (cuisine, Bengali, Arabic variants) |
| Bengali visual-grounding modality checks | ChitraMiti | **Occupied as a diagnostic** |
| Bengali cultural VQA dataset | BanglaVerse, BanglaProtha, KhatianDoc | **Occupied** |

**Exact intersection — "selective prediction for Bengali cultural entity recognition, with grounding-confidence and external cultural evidence combined" — is NOT occupied by any verified work.** But pre-emption is asymmetric: each *building block* is pre-empted, and the audit's core objection (a combination of pre-occupied parts is an engineering call, not a scientific claim) holds unless the interaction itself is specified.

The strongest candidate non-trivial interaction, supported by §3:

> *The visual-ungroundedness population (BICR) and the cultural-knowledge-application population (BanglaVerse, CulturalMenuBench) may substantially overlap in Bengali cultural entity recognition, so that a grounding-confidence-driven selector and an evidence-driven selector trade off on the same samples — and this trade-off direction may be measurable.*

This is a testable, falsifiable interaction claim — not a pipeline claim. (Whether it is *true* is unknown; see §5, §7.)

---

## 5. Evidence-gap matrix

| Question | Established evidence | Remaining unknown | Gap strength |
|---|---|---|---|
| Are VLM confidence signals usable for selection in English VQA? | Yes — selection functions beat raw softmax (Whitehead, LYP); probes work (TRAPSBench) | Whether gains generalize to cultural VQA | Moderate (English) → open (cultural) |
| Is visual grounding an independent reliability signal? | Yes — BICR (rank loss = +3.32 AUROC), SIEVES (3× OOD coverage) | Whether the signal survives when cultural knowledge answers *without* the image | **Open — the key unknown** |
| Does external/retrieved evidence improve reliability? | **Mixed, mostly negative** — M4-RAG (inverse scaling, text-RAG degradation, −32.4 pp multilingual); answer-leakage risk (audit) | Whether any acquisition policy beats gating without culture-specific hazards | **Strongly open; prior points to risk** |
| Does combined confidence + grounding + evidence beat components alone? | No work tests the triple | Decomposition/interaction absent | **Strongly open** |
| Is Bengali cultural entity recognition reliability different from generic Bengali VQA? | BanglaVerse (knowledge bottleneck), ChitraMiti (modality-reliance flaws), KhatianDoc (0-correct categories) | Is the failure *confidence-related* at all? No Bengali confidence labels exist | **Unmeasured** |
| Does the "knowledge-application gap" exist for Bengali entities specifically? | Analogous result in Chinese cuisine (CulturalMenuBench); Bangladeshi proximity untested | Bengali cultural-specific activation gap | **Open (analogy only)** |
| Do low-resource-language encoders add independent difficulty? | Yes — Where-Encoders-Fail (Bengali LRL; EOS-alignment bottleneck), M4-RAG English-centricity | Interaction with reliability signals untested | Partially established |

---

## 6. Bengali-specific evidence (A–E classification)

Evidence that is genuinely *Bengali*, separated from generic multilingual claims:

- **Knowledge is the reported bottleneck**: BanglaVerse [2603.21165](https://arxiv.org/abs/2603.21165) — failure attributed to missing cultural knowledge, *not* visual grounding.
- **Bengali VLMs fail cross-modal verification**: ChitraMiti [2609.12509](https://arxiv.org/abs/2609.12509) — description-only ≈ diagram+description; models misled by swapped spatial relations even when correct on the item.
- **Capability collapse on Bengali-script documents**: KhatianDoc [2609.03597](https://arxiv.org/abs/2609.03597) — zero correct on 39.3% of QA categories; base-16 (Ana-Ganda-Kora-Kranti-Til) fraction system.
- **Bengali as an explicit low-resource encoder-layer liability**: [2608.30725](https://arxiv.org/abs/2608.30725) — Bengali among LRLs with 30+ pp retrieval gaps; EOS hidden-state divergence is the causal location.
- **Bengali RAG works when the evidence channel is text and in-domain**: BengaliMCQ [2608.15547](https://arxiv.org/abs/2608.15547).
- **Behavioral, aspect-based benchmark only**: BanglaProtha [10.1109/wacv61042.2026.00119](https://doi.org/10.1109/wacv61042.2026.00119) — no confidence labels.

**A–E classification** (A = untested data; B = ordinary distribution shift; C = distinct uncertainty problem; D = culturally dependent grounding failure; E = insufficient evidence):

- The distinct-uncertainty-mechanism reading (**C**) is **not established**: no Bengali confidence/uncertainty labels exist; BanglaVerse contradicts pure grounding-failure.
- The pure grounding-failure reading (**D**) is **directly contested** by BanglaVerse.
- **Classification: E (insufficient evidence)**, with the two live, mutually exclusive sub-hypotheses: (a) *knowledge-application/activation gap* (CulturalMenuBench-style) and (b) *grounding/prior-bypass failure* (BICR/ChitraMiti-style). They are separated by measuring whether Bengali cultural entities are answered correctly *without* the image, i.e., sizing the ungrounded-but-correct population.
- **Inference (labeled)**: the two audit PDFs' skepticism plus the consensus of BanglaVerse + CulturalMenuBench make (a) appear more likely than (b); TRAPSBench's "representation present, expression absent" is a third modality of the same split.

---

## 7. Thesis-field assessment

**Critical claim, component-by-component** ("answer confidence + visual-grounding confidence + external cultural evidence → better calibration & selective prediction for Bengali cultural entity recognition"):

1. *Answer confidence is miscalibrated in VLMs* — **established** (BICR, TRAPSBench, Whitehead). Trivially true in Bengali by analogy, but untested; the calibration *fix* machinery is pre-empted.
2. *Visual-grounding confidence is an independent reliability signal* — **established for English/open-weight** (BICR, SIEVES). The scientific novelty would be testing whether it stays valid when knowledge answers without the image — the one component with a real open question.
3. *External cultural evidence improves selective prediction* — **not established; prior points the other way.** M4-RAG (integration bottleneck, inverse scaling), answer-leakage (audit), and "evidence-supported ≠ true" (GopherCite analysis) argue this is the load-bearing *risk*, not a safe assumption.
4. *The triple, in Bengali* — **never tested; risks being a composite.** The audit's central verdict stands: as enumerated, this is three pre-occupied subsystems and a dataset. What is *not* pre-empted is the interaction in (2)×(3): does the ungrounded-but-correct population (where grounding-confidence fails) overlap the population where cultural knowledge is present-but-not-visually-activatable, and does either correlate with entity category? This is best modeled as a *diagnostic* question, not a system.

**Gap taxonomy:**

- *Occupied*: the full machinery of each signal type (SIEVES, BICR, BCEA, M4-RAG, TRAPSBench).
- *Partially occupied*: Bengali visual reliability diagnostics (ChitraMiti answers grounding of Bengali *geometry*, not cultural entities); cultural knowledge-application gap (Chinese cuisine, Arabic; analogy only for Bengali).
- *Terminology-only false gap*: "selective prediction for cultural entities" as a task family — add Bengali + globals and it is M4-RAG − confidence + selection, i.e., mostly renaming.
- *Potentially meaningful gap*: the **interaction between grounding-confidence and cultural-knowledge activation in a low-resource language**, measured as a controlled diagnostic audit (no external retrieval; or an external-retrieval arm kept as an explicitly labeled leakage check).
- *Strongly supported open question* (the defensible core): **"Does visual-grounding confidence remain a valid reliability signal for Bengali cultural entity recognition when cultural knowledge can produce correct answers without the image?"** BanglaVerse, CulturalMenuBench, and BICR impose three contradictory pressures, making the answer non-obvious and load-bearing; no verified work measures it.

**Bottom line.** The field *as formulated* is pre-empted at the component level; the audit's objection is confirmed. A legitimate, non-engineering thesis remains only if the question is the interaction above and the method is a diagnostic that reports (a) the size / behavior of the ungrounded-but-correct population in Bengali cultural VQA, (b) whether grounding-confidence is calibrated there, and (c) whether external evidence shifts the selective curve only through leakage artifacts. Anything else assembles occupied parts.

---

## 8. References (verified primary sources)

Read in full depth:
- SIEVES — Selective Prediction Generalizes through Visual Evidence Scoring — <https://www.alphaxiv.org/abs/2604.25855>
- BCEA — Look Again Before You Abstain — <https://www.alphaxiv.org/abs/2606.16667>
- BanglaVerse — Bengali cultural benchmark — <https://www.alphaxiv.org/abs/2603.21165>
- M²CQA — Once Correct, Still Wrong (MENA counterfactual hallucination) — <https://www.alphaxiv.org/abs/2602.05437>
- M4-RAG — A Massive-Scale Multilingual Multi-Cultural Multimodal RAG — <https://www.alphaxiv.org/abs/2512.05959>
- BICR — Grounded or Guessing? LVLM Confidence Estimation via Blind-Image Contrastive Ranking — <https://www.alphaxiv.org/abs/2605.10893>

Verified via retrieval (abstract / full text as available):
- TRAPSBench — <https://www.alphaxiv.org/abs/2608.13167>
- ChitraMiti — <https://www.alphaxiv.org/abs/2609.12509>
- CulturalMenuBench — <https://www.alphaxiv.org/abs/2609.03526>
- FinAbstain — <https://www.alphaxiv.org/abs/2607.24875>
- KhatianDoc — <https://www.alphaxiv.org/abs/2609.03597>
- BanglaProtha — <https://doi.org/10.1109/wacv61042.2026.00119>
- ReCoVERR — <https://www.aclanthology.org/2024.findings-acl.767/>
- Reliable VQA — <https://www.alphaxiv.org/abs/2204.13631>
- Learning from Your Peers — <https://www.alphaxiv.org/abs/2306.08751>
- Xin et al. (Investigate Selective Prediction) — <https://www.aclanthology.org/2022.findings-acl.158/>
- SelectiveNet — <https://www.alphaxiv.org/abs/1901.09192>
- A-CRC-QA — <https://www.alphaxiv.org/abs/2608.12008>
- CAUC — <https://www.alphaxiv.org/abs/2609.11446>
- SPC — <https://www.alphaxiv.org/abs/2607.29240>
- CVE-SAI — <https://www.alphaxiv.org/abs/2608.25023>
- Evidence-Order Calibration — <https://www.alphaxiv.org/abs/2609.09184>
- Where Do Multilingual VLM Encoders Fail? — <https://www.alphaxiv.org/abs/2608.30725>
- BengaliMCQ — <https://www.alphaxiv.org/abs/2608.15547>
- SAVOR — <https://www.alphaxiv.org/abs/2609.16601>
- CARGO-VL — <https://www.alphaxiv.org/abs/2608.04509>
- MVC-Bench — <https://www.alphaxiv.org/abs/2608.27004>
- ImageEval 2026 — <https://www.alphaxiv.org/abs/2608.30475>
- FinReliable NER — <https://www.alphaxiv.org/abs/2608.19558>
- Selectively Answering Visual Questions — <https://www.aclanthology.org/2024.findings-acl.250/>
- Know Your Limits — <https://doi.org/10.1162/tacl_a_00754>
- GopherCite — <https://www.alphaxiv.org/abs/2203.11147>
- Don't Hallucinate, Abstain — <https://www.aclanthology.org/2024.acl-long.786/>
- Instinct vs. Reflection — <https://www.alphaxiv.org/abs/2604.17274>
- Staying VIGILant — <https://www.alphaxiv.org/abs/2606.26387>
- VisER — <https://www.alphaxiv.org/abs/2608.30480>
- MLLM uncertainty survey — <https://www.alphaxiv.org/abs/2608.17084>
- ERAG/EvidentialRAG — <https://www.alphaxiv.org/abs/2607.10491>
- CultureVLM — <https://www.alphaxiv.org/abs/2501.01282>
- Figurative and Cultural Knowledge — <https://www.alphaxiv.org/abs/2608.18361>
- Rethinking Correctness for UE — <https://www.alphaxiv.org/abs/2609.15180>
- LeMUQ — <https://www.alphaxiv.org/abs/2605.29956>
- BnBERT-iPET — <https://www.alphaxiv.org/abs/2608.05104>
- DocTalkBN — <https://www.alphaxiv.org/abs/2608.27110>

User-supplied context (not primary evidence for claims in this report, treated as hypothesis sources):
- "Adversarial Literature Autopsy" (chat transcript, 22 pp) — partially pre-empted; Bangla reliability question open.
- "Bangla Cultural VLM Thesis Audit" (19 pp) — not a defensible standalone thesis as formulated; strongest framing = diagnostic audit without external retrieval; cites SIEVES/BICR/BCEA; warns of answer leakage.