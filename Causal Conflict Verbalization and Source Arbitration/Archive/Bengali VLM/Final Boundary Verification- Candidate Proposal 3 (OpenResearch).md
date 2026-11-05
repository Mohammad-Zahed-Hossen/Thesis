The Read tool couldn't render that PDF directly, so I'll extract its text with pymupdf (as before).

I've read the Antigravity 2.0 audit (13 pp). It confirms the diagnosis and, critically, declares the decision hinges on exactly two empirical boundary checks (BanglaProtha image-leakage; blank-image sensitivity) plus a tokenizer-fertility check — which matches the tasks you've set. I'll now verify each item against primary sources, starting with the actual BanglaProtha repository.

The repo has no image files — only `data/data.csv` (24.7 KB) plus a vendored LLaMA-Factory tree. Images must be hosted elsewhere. Let me inspect the README and CSV.

Need `-UseBasicParsing` in PS 5.1 non-interactive mode. Retrying with `Invoke-RestMethod`.

The repo holds `data/data.csv` with columns `filename,question,options,answer,category,id` but **no images** (README points to a Kaggle dataset `sourove/bangla-culturally-relevant-vqa` and `data/images`). Let me parse the CSV properly and check `infer.py` for split structure.

Repo's `data.csv` is only **80 rows** (a preview) — the full dataset is on Kaggle. I need the WACV paper's dataset-construction section (primary source) plus the Kaggle page. Fetching both.

Extracting the WACV paper text (11.7 MB PDF) to read the dataset-construction details.

Now the paper's dataset facts are established. Let me try to access the Kaggle release metadata and check for a Hugging Face mirror of the full data.

Kaggle metadata confirms the full release is ~2.18 GB (images included). Let me inspect the raw resource structure for split information.

Kaggle metadata confirms the release exists (2.18 GB, version 5) but file listing/download require authentication — the split assignment and images are not obtainable. I'll classify that precisely. Now let me verify the no-image baselines in the BanglaProtha paper, and pull the two remaining primary sources (ChitraMiti, Evidence-Order) for the blank-image premise.

Both primary sources confirmed, and they're directly relevant. Let me pull the exact audit numbers from the Antigravity PDF to pin down what was overstated, and confirm the paper's own sentence about empty-image baselines.

## Boundary verification — Proposal 3 (evidence only, no design)

**Sources this pass:** WACV 2026 BanglaProtha full text (open-access, 11 pp), GitHub repo `farhanishmam/BanglaProtha` (tree, `data.csv`, `infer.py`), Kaggle metadata endpoint (`sourove/bangla-culturally-relevant-vqa'), full reads: BICR [2605.10893](https://arxiv.org/abs/2605.10893), Evidence-Order [2609.09184](https://arxiv.org/abs/2609.09184), ChitraMiti [2609.12509](https://arxiv.org/abs/2609.12509), plus prior full reads (SIEVES, BCEA, BanglaVerse, M²CQA, M4-RAG).

**Task 1 — BanglaProtha, repo + data + paper (not summary):**

| Property | Finding | Status |
|---|---|---|
| Scale | 6,942 images / 8,034 QA pairs (Table 1: BNATURE 2079/2517, BORNON 1402/1638, BANGLALEKHA 2541/2816, Websites 920/1063) | VERIFIED |
| Same image, multiple questions | Per-source #Q:#I = 1.11–1.21 → ≥1,092 images carry ≥1 extra question (design property, from Table 1) | VERIFIED |
| Multi-question in the released preview | `data.csv` = 80 rows, every filename unique | VERIFIED |
| Split structure | Single sentence: "divided into the standard 80:20 train-test splits." No validation split; **no statement of image-disjointness, dedup, or entity stratification anywhere in the paper** | VERIFIED (absence) |
| Author split image-disjoint | Split assignment lives only in the 2.18 GB Kaggle release (version 5, license "Unknown", 10 downloads); no image file hashes are publishable/verifiable without authentication | UNKNOWN |
| Cross-split duplicate images | Undetectable without the Kaggle archive | UNKNOWN |
| Near-duplicate / re-encoded images | No documentation anywhere in paper or repo | UNKNOWN (undocumented) |
| Same entity across different images | No entity-level annotation; 80-row preview shows repeated answer labels (ধান ×2, সরিষা ×2) on distinct images | INFERRED from sample |
| `filename` exposed per row | Schema verified in `data.csv` → third-party **image-level re-split is constructible** | VERIFIED |

**Which threats bite (the distinction the task demands):** (i) multiple questions per image matters only if a QA-pair-level random split straddles a shared image — preventable because we control the split; it also inflates the image-level sample, so image-level aggregation is required analytically, not fatally. (ii) cross-split duplicate images — preventable by construction under our own split; byte-level dedup is easy once images are in hand. (iii) same entity across different images is **not leakage** but a genuine confound to report (correlated label priors). (iv) near-duplicates are the only unverifiable form. Net: leakage is an **operational, experimenter-controlled constraint**, not a scientific disqualifier.

**Task 2 — Blank-image premise from primary papers:**
- BICR [2605.10893](https://arxiv.org/abs/2605.10893): perturbation is a **solid black image of identical dimensions**; the signal is a **hidden-state contrastive rank** (not a %-unchanged rule); predicts correctness (best AUROC 78.63; ECE 7.09). Domain: English/medical/financial VQA and open-ended QA; **multilingual and culturally localized settings explicitly untested**.
- Evidence-Order [2609.09184](https://arxiv.org/abs/2609.09184): progressive masking of question-critical regions (GQA). Aggregate: critical masking −28.2 pp vs −0.6 pp non-critical (paired diff 27.6, 95% CI [20.0, 34.7]) — so **visual-evidence reliance predicts accuracy in aggregate**; but per-item evidence-unmonotonicity is severe (EMVR 0.436) and **native confidence ≥ trained evidence heads for selective-risk ranking** (AUROC/Brier/AURC diffs inconclusive).
- ChitraMiti [2609.12509](https://arxiv.org/abs/2609.12509) (Bengali): description-only ≈ diagram+description accuracy, and models are "frequently misled by a swapped spatial relation even when they answer the unmodified item correctly" — a Bengali-domain proof-of-concept that correct items can be weakly image-dependent.
- **Bayes on thresholds:** the audit's ">85% unchanged ⇒ functionally blind" and any "Δlogit > 0.30" cutoffs at lines 1144–1146 of its text appear in **no primary source**; BICR's whole premise is that answer-stability under blanking does *not* imply signal irrelevance. Those are **proposed experimental thresholds, not verified scientific thresholds** — and under BanglaProtha's semantically-similar-option design (verified in the paper: "four semantically similar and question-relevant answer choices"), prior-guessing is deliberately made harder, so the "priors answer without the image" failure mode is weakened, not strengthened, by the audit's preferred dataset.

**Task 3 — Narrow pre-emption:** Nowhere located does a primary study test visual-grounding-sensitivity signals as *reliability predictors* under cultural/regional distribution shift with low-resource language items. Component results all exist (blind-image memory shortcuts SIEVES; region-masking evidence monotonicity BCEA; black-image contrastive ranking BICR; evidence-order heads [2609.09184](https://arxiv.org/abs/2609.09184); Bengali modality reliance ChitraMiti; names-beat-images CulturalMenuBench) — but the conjunctive, per-item diagnostic claim is open. **Not pre-empted.**

**Task 4 — Competing explanations bounded:** (a) ordinary OOD miscalibration is real and large (FinMME: ECE 0.25–0.58, >85% confident-error) but is a *general* covariate, not an explanation of why grounding-sensitivity would fail while accuracy survives; (b) cultural priors/answer-prior guessing is exactly the boundary variable, and BanglaProtha's semantically-similar options give a discriminating design; (c) tokenizer fertility/translation effects are measurable covariates (audit's check #3), not a confound that resolves the question; (d) class imbalance/minority images: answer space is near-open (78 unique answers / 80 items in preview), so 25%-guessing baselines don't dominate; (e) generic hallucination is distinguishable by cross-language calibration comparison. **No single explanation fully substitutes for the targeted measurement.**

**Task 5 — Contribution audit:** if a grounding-sensitivity signal separates correct/incorrect under Bengali cultural shift → new knowledge: a reliability signal that survives cultural distribution shift (and the first native-Bengali test of grounding-consistency-based selection). If it fails → new knowledge: it quantifies how far cultural priors can sustain correct-but-ungrounded answers, i.e., a dual-use diagnostic on VLM modality reliance in long-tail cultures. Both branches are publishable; the broader phenomenon generalizes to "reliability of visual grounding under distribution shifts with strong domain priors," contingent on the reliability-*signal* claim, not on Bangladesh specifics. **Contribution survives either branch.**

**Task 6 — Closest papers:**

| Paper | Exact question | Method | Dataset-domain | Main finding | Overlap | Remaining gap |
|---|---|---|---|---|---|---|
| Evidence-Order [2609.09184](https://arxiv.org/abs/2609.09184) | Does evidence-order consistency add reliability value over confidence? | Progressive question-critical masking + reliability head | GQA (English) | Masking −28 pp critical vs −0.6 pp non-critical; heads ≤ native confidence | Sensitivity→reliability mechanism | Not cultural shift; no benefit over confidence shown |
| BICR [2605.10893](https://arxiv.org/abs/2605.10893) | Do blind-image contrastive probes predict correctness? | Black-image hidden-state ranking | English/med/finance VQA | AUROC 78.63, ECE 7.09 | Signal family, exact method | Multilingual/cultural untested |
| BCEA [2606.16667](https://arxiv.org/abs/2606.16667) | Can evidence-region sensitivity gate abstention? | Region-mask log-likelihood + conformal coverage | POPE/MS-COCO (English) | Masking diff 0.109; abstains >80% at 5% hal. rate | Grounding-dependent abstention | Not cultural; heavy abstention |
| ChitraMiti [2609.12509](https://arxiv.org/abs/2609.12509) | Do Beng. VLMs check text against diagrams? | Diagram/desc/text-only protocol + swapped relations | Bengali geometry | Desc-only ≈ full; correct items fail swapped checks | Bengali modality reliance | Geometry; no reliability signals |
| BanglaProtha (WACV 2026) | VLM accuracy across Bengali cultural aspects | Datasets + prompt/fine-tune/scale sweeps | Bengali cultural MCQA | Behavioral gaps across aspects | **Target dataset** | Accuracy only; no selectivity |
| BanglaVerse [2603.21165](https://arxiv.org/abs/2603.21165) | Robustness to dialectal variation | 9 dialect/language expansions of 1,152 images | Bengali cultural | High sensitivity to linguistic form | Cultural benchmark | Same-image reuse across variants; accuracy only |
| CulturalMenuBench [2609.03526](https://arxiv.org/abs/2609.03526) | Are names or images decisive? | Name-only vs image-only ablation | Multi-culture menus | Names beat images +7–18 pts | What prior/reliance distorts | No per-item reliability use |
| FinMME [2608.06532](https://arxiv.org/abs/2608.06532) | VLM calibration under domain shift | Verbalized/logit calibration, ECE | Financial (English) | ECE 0.25–0.58; >85% confident-error | Overconfidence under shift | No grounding signal |

---

### A — What Is Now Verified
- BanglaProtha is **6,942 images / 8,034 QA pairs**, 9 categories, semantically-similar options (anti-prior design), single "80:20" split sentence with **no documented image-disjointness, dedup, or entity stratification**; 2.18 GB Kaggle-only images, license "Unknown".
- Same-image multi-question reuse is a real design property (~1.16 #Q:#I); leakage is **fully controllable** by an experimenter-defined image-disjoint re-split (schema exposes `filename`).
- Blank-image/perturbation methodology exists in primary literature (BICR black-image contrastive ranking; Evidence-Order progressive critical-region masking; ChitraMiti description-only protocol) and consistently shows: **aggregate visual reliance predicts accuracy, but per-item reliability gain over plain confidence is not established even in-domain, and none is tested under cultural/low-resource shift**.
- The audit's decision-critical issues reduce to **one** really unmeasured quantity (per-item sensitivity-signal value for Bengali cultural MCQA), plus a **data-access** dependency (Kaggle).

### B — What Was Wrong or Overstated in the Previous Audit
1. **Scale wrong:** "~1,200 images / ~3,500 questions" (its §Data/BanglaProtha) — actual 6,942/8,034; the 500-item/1,500-pass cost model was built on ~6× too small a number.
2. **Threshold invented as if established:** ">85% unchanged ⇒ functionally blind" is not a scientific threshold in any primary source and contradicts BICR's own premise; same for any "Δlogit>0.30" rule. These are **proposed experimental thresholds**, to be pre-registered.
3. **Leakage over-weighted:** cross-split leakage was treated as a decision-critical unknown; it is experimenter-controllable and non-fatal once images are obtainable and hashed.
4. **Missing the real hinge:** the literature (Evidence-Order) makes the true decision variable "does the sensitivity signal beat native confidence under shift" — the audit's blank-image framing silently equates answer-stability with signal absence.

### C — Remaining Scientific Gap
No primary work establishes per-item reliability of a visual-grounding sensitivity signal for culturally long-tail, low-resource-language MCQA, nor whether it adds over calibrated confidence there. Aggregate direction is supported (shifted-domain calibration collapses); the per-item value-over-confidence branch is open, with priors from GQA/English data leaning neutral-to-skeptical.

### D — Remaining Fatal Risks
1. **Per-item signal deficit:** if Bengali cultural items behave like GQA (Evidence-Order), the sensitivity head may fail to beat plain confidence under shift, collapsing the contribution to "use calibrated confidence" — falsifying Proposal 3's distinctness.
2. **Data-access barrier:** the full archive (incl. split/hashes) is inaccessible without Kaggle credentials; license "Unknown" (10 downloads) jeopardizes reproducibility of any leakage claim.
3. **Saturation/confound:** if prior-resistant options make sensitivity rare or if tokenizer-fertility effects masquerade as grounding changes, statistical power may be insufficient.

### E — Decision Status
**NEEDS ONE MORE TARGETED CHECK**

Reasoning for the single allowed status: Task 1 resolved — leakage is controlled at the design level, not fatal; Tasks 3–6 resolved — the conjunctive claim is un-pre-empted, competing explanations are bounded, the contribution survives both branches, and the closest-papers table leaves exactly one empty cell. That cell — the blank-image/visual-sensitivity measurement (with corrected, pre-registered thresholds plus the tokenizer-fertility covariate) on a leakage-controlled Bengali cultural sample — is precisely the audit's unresolved hinge, it is decisive, and it has not been run. Choosing "SURVIVES" would repeat the "overstated" failure; choosing "DROP" would ignore that the only disconfirmation pathway is an un-run measurement. Until that single measurement exists, Proposal 3 stays in the working set, unranked.