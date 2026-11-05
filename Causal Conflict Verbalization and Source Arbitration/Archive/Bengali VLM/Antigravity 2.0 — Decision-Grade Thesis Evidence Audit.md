# Antigravity 2.0 — Decision-Grade Thesis Evidence Audit

**Candidate Topic:**
*Evidence-Grounded Selective Prediction for Reliable Bangla Cultural Vision-Language Models*

**Documents Audited:**
1. `Evidence-Grounded Selective Prediction for Reliable Bangla Cultural Vision-Language Models.md` (Initial System-Building Proposal)
2. `bangla-cultural-vlm-synthesis.md` (Cross-Paper Synthesis & 40+ Paper Literature Map)
3. `Bangla Cultural VLM Thesis Audit.md` & `Adversarial literature autopsy.md` (Adversarial Field Mapping & Primary Source Autopsy)

---

## 1. Audit Methodology and Primary Evidence Verification

Each critical claim across the audited files has been verified against primary scientific literature, empirical benchmark records, and methodological standards. In accordance with strict epistemic standards, contradictions between files are explicitly identified rather than silently resolved.

| Critical Proposal Claim | Epistemic Status | Source & Evidence Justification |
| :--- | :--- | :--- |
| **VLM confidence miscalibration is severe under domain and cultural shift** | **VERIFIED** | *Khanmohammadi et al.* (`arXiv:2608.06532`, 2026; FinMME) and *MVC-Bench* (`arXiv:2608.27004`, 2026): Expected Calibration Error (ECE) ranges from 0.25 to 0.58 on open LVLMs, with confident-error rates exceeding 85% for verbalized confidence under domain shifts. |
| **Selective prediction and risk–coverage formalisms are established for VLMs** | **VERIFIED** | *Whitehead et al.* (ECCV 2022); *Traub et al.* (NeurIPS 2024, AUGRC); *SIEVES* (`arXiv:2604.25855`, 2026). Standardized formalisms ($C@r$, AURC, AUGRC) govern selective abstention in multimodal systems. |
| **Visual grounding and reliance correlate with answer correctness in generic VQA** | **VERIFIED (in Western/OOD settings)** | *BICR* (`arXiv:2605.10893`, 2026) shows blind-image contrastive ranking improves AUROC (+3.32) across 5 open LVLMs on GQA/POPE. *SIEVES* (`arXiv:2604.25855`, 2026) demonstrates visual localization quality ($c_{\text{loc}}$) predicts correctness. |
| **Grounding-derived confidence reliably outperforms native softmax confidence** | **CONTRADICTED** | *Xin et al.* (ACL Findings 2022) across 17 datasets proved no confidence estimator consistently and considerably outperforms raw MaxProb (softmax). *Evidence-Order Calibration* (`arXiv:2609.09184`, 2026) proved native model confidence remained stronger for selective risk ranking than evidence-supervised auxiliary heads. |
| **VLMs encode internal uncertainty that autoregressive text generation suppresses** | **VERIFIED** | *TRAPSBench* (`arXiv:2608.13167`, 2026): Linear probes on internal hidden states decode answerability at 0.91 AUROC, whereas autoregressive text generation yields PECS scores of only 0.292 (a ~4× visual-vs-textual gap). |
| **Bengali cultural entity recognition failures are empirically documented** | **VERIFIED** | *BanglaVerse* (`arXiv:2603.21165`, 2026): 1,152 images across 9 domains; 42.6% of coded failures are local entity/artifact misidentifications. *BanglaProtha* (WACV 2026): documents systemic failure on long-tail Bengali cultural distractors. |
| **Existing Bengali cultural benchmarks evaluate calibration or selective prediction** | **CONTRADICTED** | *BanglaVerse* and *BanglaProtha* evaluate accuracy, ROUGE, BERTScore, and LLM-as-a-judge quality only. Neither computes ECE, Brier score, selective risk–coverage, or internal state probes. |
| **The failure bottleneck on Bengali data is visual grounding failure** | **CONTRADICTED / CONFLICTING** | *BanglaVerse* explicitly concludes the failure bottleneck is **missing cultural parametric knowledge**, *not* visual grounding. Conversely, *ChitraMiti* (`arXiv:2609.12509`, 2026) reports that Bengali VLMs suffer severe cross-modal verification flaws (ignoring swapped visual relations). The files directly conflict on whether the failure is perceptual or parametric. |
| **External cultural text retrieval provides an unconfounded confidence signal** | **CONTRADICTED** | Text passages describing localized cultural entities (e.g., "Nakshi Kantha", "Shorshe Ilish") contain the gold entity name verbatim. Providing retrieved passages turns visual recognition into text extraction (catastrophic label leakage). *M4-RAG* (`arXiv:2512.05959`, 2025) further proves that external evidence degrades multimodal performance in multilingual settings (−32.4 pp). |
| **Heuristic linear fusion ($w_1 C_{\text{ans}} + w_2 C_{\text{vis}} + w_3 C_{\text{ev}}$) is a valid scientific contribution** | **UNVERIFIED / REJECTED** | Fusing three scalar scores via logistic regression or fixed weights is standard pipeline engineering. It offers no mechanistic explanation of cross-modal representation. |
| **Bengali cultural data creates a distinct uncertainty distribution shift** | **INFERRED (UNPROVEN)** | Plausible hypothesis based on asymmetric pretraining (weak Bengali vision tokens + coarse text priors), but empirically unproven. It remains unknown whether this shift is distinct from generic long-tail OOD epistemic uncertainty. |
| **Compact open-weight VLMs possess reliable zero-shot Bengali tokenization and language representation for cultural MCQA** | **SUPPORTED WITH UNCERTAINTY** | `Qwen2.5-VL-3B-Instruct` has strong Indic/Bengali token vocabulary, but *Where Do Multilingual VLM Encoders Fail?* (`arXiv:2608.30725`, 2026) proves that Bengali hidden-state trajectories in multilingual VLMs suffer severe alignment drift compared to English, risking token-level probability distortions. |

---

## 2. Main Question: Decision-Readiness Assessment

> **Do I currently have enough evidence to make an honest thesis-topic decision, or is another targeted investigation still necessary?**

**Verdict: YES, you have enough evidence to make an honest thesis-topic decision.** Another broad literature sweep is unnecessary and counterproductive.

The audited files demonstrate decisively that:

1. **The initial constructive proposal (`Evidence-Grounded Selective Prediction...`) is fatally flawed as an academic thesis.** It combines pre-occupied components (*SIEVES*, *BICR*, *BCEA*), relies on an external retrieval pipeline that causes catastrophic answer leakage, and reduces to an engineering exercise ("apply Western pipeline to a Bengali benchmark").
2. **A scientifically defensible thesis exists only by pivoting to a diagnostic audit:** investigating the mechanistic competition between visual reliance and language priors under cultural shift (i.e., whether blank-image contrastive probes fail when cultural knowledge allows models to guess correctly without the image).
3. **The decision between this topic and your other canonical proposals (Proposals 1 and 2) does not hinge on undiscovered papers.** It hinges on whether you wish to commit to a diagnostic audit on Bengali data despite known dataset noise and language-prior confounds, or pursue the cleaner, more controlled mechanistic designs of Proposals 1 or 2.

### Systematic Audit of the 9 Core Sub-Criteria:

1. **A real technical research problem:** **SUPPORTED (with strict boundary).** VLM overconfidence and language-prior guessing on culturally localized entities is a genuine real-world problem (*BanglaVerse*, *BanglaProtha*). However, selective prediction itself is an already-solved formalism.
2. **A sufficiently specific research question:** **CONTRADICTED in initial proposal; SUPPORTED in diagnostic form.** The initial proposal bundled three orthogonal signals into a heuristic sum. The de-scoped diagnostic question (*"Does visual-grounding confidence remain a valid selective predictor when cultural knowledge produces correct answers without visual tokens?"*) is narrow, falsifiable, and specific.
3. **A genuine gap relative to existing work:** **OCCUPIED at component level; OPEN at interaction level.** *SIEVES*, *BICR*, *BCEA*, and *M4-RAG* occupy every algorithmic mechanism. The unoccupied scientific niche is strictly the **interaction between visual grounding penalties and cultural knowledge activation**.
4. **A meaningful contribution even if the proposed method does not improve the main metric:** **SUPPORTED under diagnostic framing only.** If visual grounding probes (*BICR*) fail to improve selective risk–coverage on Bengali cultural data over raw softmax logits, it provides a high-value negative result: proving that visual contrastive signals break down when errors stem from missing cultural world knowledge rather than lack of visual attention. Under the initial system-building formulation, a null result represents complete project failure.
5. **Public and usable datasets:** **VERIFIED.** *BanglaVerse* (`arXiv:2603.21165`, Hugging Face) and *BanglaProtha* (WACV 2026, GitHub) are publicly available.
6. **Reproducible open-weight baselines:** **VERIFIED.** `Qwen2.5-VL-3B-Instruct`, `Qwen2-VL-2B-Instruct`, and `google/gemma-3-4b-it` run natively in `bfloat16` within a 16 GB VRAM envelope.
7. **A feasible undergraduate-scale experimental path:** **VERIFIED for inference/probing only.** Running 500 items across original, blank, and scrambled visual inputs takes ~1,500 forward passes (~40 minutes on a Colab T4/V100). Training a full RAG retriever and multi-agent pipeline is heavily bottlenecked by engineering overhead.
8. **A leakage-resistant evaluation design:** **CONTRADICTED in initial proposal; FEASIBLE only without RAG.** The initial retrieval arm is fundamentally non-viable due to verbatim text entity leaks. A leakage-resistant evaluation requires strictly closed multiple-choice visual items (*BanglaProtha*) with image-hash deduplication.
9. **A research question that is not simply a superficial trope:**
   - The initial proposal fell squarely into the superficial trope: *"Bengali dataset + existing model + generic RAG + selective prediction."*
   - Only a mechanistic investigation of **language-prior dominance decoupling visual grounding from correctness** escapes this trap.

---

## 3. Adversarial Novelty Audit

### What is the closest existing work that could make this thesis redundant?

The thesis is primarily threatened by two concurrent 2026 papers:
1. **SIEVES** (*Rodriguez & Rohrbach, arXiv:2604.25855, April 2026*): Formalized selective prediction using visual evidence quality scoring ($c_{\text{loc}}, c_{\text{coh}}$) on VQA under distribution shift.
2. **BICR** (*Khanmohammadi et al., arXiv:2605.10893, May 2026*): Formalized blind-image contrastive ranking ($\Delta_{\text{blank}}$) on hidden states to detect ungrounded VLM predictions.

If the candidate thesis is framed as: *"We extract visual grounding confidence using image perturbations and use it to gate VQA answers via selective prediction,"* any competent reviewer will state:
> *"This is simply running BICR and SIEVES on a Bengali cultural benchmark. The algorithmic contribution is zero."*

### Detailed Competitor Deconstruction

| Competitor Paper | What They Actually Test | Dataset & Domain | Model | Confidence / Evidence Mechanism | Evaluation & Metrics | Overlap with Proposal | What This Proposal Tests That They Did Not |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| **SIEVES** (Apr 2026) | Selective VQA under severe OOD distribution shifts | V* Bench, HR-Bench-8k, VizWiz, AdVQA | Pixel-Reasoner, o3, Gemini-3-Pro; Gemma-3-4B selector | Auxiliary learned selector scoring correctness ($c_{\text{corr}}$), localization ($c_{\text{loc}}$), and crop-answer coherence ($c_{\text{coh}}$) | $C@1\%$, $C@5\%$, AURC, Risk–Coverage curves | Complete overlap on selective prediction formalisms, visual evidence gating, and risk–coverage evaluation | Whether localized visual evidence can distinguish errors when identification requires non-Western cultural knowledge rather than fine-grained spatial zoom. |
| **BICR** (May 2026) | Distinguishing genuine visual reliance from language-prior guessing | GQA, POPE, MME-Finance, MMMU-Pro | 5 open LVLMs (LLaVA-1.5, Qwen-VL, Yi-VL) | Blind-image contrastive ranking probe on hidden states: penalizes higher confidence on blank image | ECE, Brier Score, AUROC, AUCPR, reliability curves | Direct pre-emption of the blank-image contrastive confidence mechanism ($\Delta_{\text{blank}}$) | Tests whether blank-image contrastive probes transfer to low-resource non-Latin scripts and localized cultural entities where language priors might be uncalibrated. |
| **BCEA** (Jun 2026) | Epistemic abstention under formal finite-sample risk bounds | POPE, MS-COCO claims | LLaVA-1.5, Qwen3-VL, InternVL2 | Difference in claim logit between original and blank image; conformal 3-way decision (Answer / Abstain / Acquire) | Conformal coverage at $\le 5\%$ error, certified coverage, AUROC | Pre-empts visual evidence acquisition before abstention and distribution-free risk control | Tests complex entity-level cultural recognition rather than binary object-existence claims on COCO. |
| **TRAPSBench** (Aug 2026) | Epistemic abstention when visual evidence is insufficient; representation-output gap | 1,404 matched physics video pairs | 16 VLMs (Qwen, Gemma, LLaVA families) | Probes on internal states vs generated abstention tokens; Penalized Epistemic Calibration Score (PECS) | PECS, AUROC on linear probes | Establishes that verbalized abstention fails while internal hidden states encode uncertainty | Cultural entity unanswerability rather than physical simulation counterfactuals. |
| **Evidence-Order Calibration** (Sep 2026) | Selective visual reasoning under evidence loss; monotonicity of evidence | English GQA / VQA | Open LVLMs | Auxiliary reliability head trained on hidden states, logit confidence, and token entropy | Evidence-Monotonicity Violation Rate (EMVR), Risk-Coverage | Proves that evidence-supervised auxiliary heads fail to beat native MaxProb softmax for risk ranking | Tests non-Western cultural entity identification under asymmetric pretraining. |
| **SPC (Selective Prior Calibration)** (Jul 2026) | Language/commonsense prior overriding visual evidence | Counterfactual visual conflicts (e.g., 6-fingered hands) | LLaVA, InstructBLIP | Contrastive prior subtraction: penalizes output tokens favored by text-only priors | Accuracy, bias mitigation delta | Addresses text prior overriding visual evidence | Tests cultural knowledge distribution shifts rather than artificial counterfactual edits. |
| **M4-RAG** (Dec 2025) | Multilingual, multicultural, multimodal RAG evaluation | 42 languages, 189 countries (incl. CVQA, WorldCuisines) | Gemma-3, Qwen2.5-VL, GPT-4o | Passive retrieval using mmE5 and BGE-M3 text/multimodal passages | Accuracy, degradation delta across scale (−32.4 pp drop) | Evaluates multimodal cultural retrieval across languages | M4-RAG evaluates accuracy only; it does not evaluate confidence calibration, uncertainty, or selective prediction. |
| **ChitraMiti** (Sep 2026) | Multimodal geometric reasoning and modality reliance in Bengali | Bengali geometric diagrams and descriptions | Open-weight and API VLMs | Modality ablation (text-only vs image-only vs paired) | Accuracy drops under swapped visual relations | Demonstrates visual-reliance flaws specifically in Bengali VLMs | Does not evaluate cultural entities, confidence calibration, or selective prediction. |
| **CulturalMenuBench** (Sep 2026) | Cultural food recognition vs attribution (knowledge-application gap) | 10 languages, 18 regions, cultural cuisine | Open and closed VLMs | Visual trojan tests; text names vs image presentations | Accuracy on recognition vs cultural attribution | Directly establishes that cultural text priors outperform visual recognition by +7–18 pts | Evaluates Chinese/global cuisine; does not evaluate Bengali culture or selective prediction. |
| **BanglaVerse** (Mar 2026) | Bengali cultural multimodal benchmark | 1,152 images, 32.2K QA items, 9 domains | GPT-4o, Gemini-1.5, Qwen2.5-VL, Claude | None (Pure accuracy evaluation) | Accuracy, ROUGE, BERTScore, LLM-as-a-judge | Fully occupies the Bengali cultural benchmark domain and local-entity error taxonomy | Introduces uncertainty calibration, selective prediction, and internal state probing to this domain. |

---

## 4. Audit of the "Bangla Cultural" Justification

### Is Bengali Cultural Data a Scientifically Meaningful Test Condition or Mere Application?

**Under the original proposal: It is a mere application domain (Level 1/2 engineering).**
Simply running an existing confidence estimator on Bengali images does not constitute a methodological advance.

**Under a mechanistic diagnostic framing: It represents a scientifically meaningful test condition.**
The specific, measurable failure mechanism exposed by Bengali cultural data is **Asymmetric Cross-Modal Pretraining Representation**:

1. **The Representation Asymmetry:** Foundation VLMs undergo pretraining where Western visual concepts (e.g., "hamburger", "statue of liberty") appear millions of times in paired image-text data, aligning visual and textual tokens tightly. In contrast, Bengali cultural entities (e.g., *Nakshi Kantha*, *Shorshe Ilish*, *Kula*, *Pitha*) have **sparse, low-resolution visual representation**, but **moderate textual presence** in web-scraped corpora.
2. **Language-Prior Attentional Capture:** When presented with a cultural image, the visual encoder extracts weak, ambiguous patch tokens. The autoregressive language decoder defaults to its high-frequency language prior (e.g., predicting a generic Western or pan-Indian concept with high confidence). The model suffers from **functional blindness**: it generates a fluent, confident answer while bypassing visual evidence.
3. **The Unresolved Interaction:**
   *BICR* assumes that ungrounded answers are bad and should be penalized by blind-image contrastive loss. But in cultural domains, as proven by *CulturalMenuBench* and *BanglaVerse*, **the model often arrives at the correct answer purely through language priors without grounding on the image**.
   Therefore, an off-the-shelf visual grounding selector will penalize the exact population of answers that are *correct due to cultural text memory*.

If the Bengali data is used to expose this fundamental tension—**why visual reliance probes fail when cultural knowledge answers without the image**—the contribution is scientifically profound and generalizes beyond Bengali to all low-resource cultural domains.

---

## 5. Audit of the Proposed Evidence Mechanism

The initial proposal formulated confidence as a composite score:
$$C_{\text{combined}} = w_1 C_{\text{answer}} + w_2 C_{\text{visual}} + w_3 C_{\text{evidence}}$$

### Fatal Flaws in This Proposed Mechanism:

1. **Catastrophic Answer Leakage via External Text Retrieval:**
   When a retriever fetches a Wikipedia or cultural passage for an item (e.g., querying for an image depicting *Nakshi Kantha*), the retrieved text explicitly states: *"Nakshi Kantha is a type of embroidered quilt from Bengal..."*
   Feeding this passage to the model converts a difficult visual recognition task into a **trivial reading comprehension task**. The VLM identifies the entity from the text string, completely bypassing the image. This destroys the validity of the visual calibration experiment.
2. **Confounding Retrieval Quality with Model Uncertainty:**
   If the selective prediction system abstains, what failed? Did the vision encoder fail to see the entity? Did the retriever fail to find a passage? Did the reranker hallucinate? Or did the weights miscalibrate? Fusing retrieval with visual confidence creates an intractable multi-variable confound.
3. **Negative Utility of Multimodal RAG:**
   *M4-RAG* (`arXiv:2512.05959`) proved that external multimodal retrieval actually causes an **inverse scaling degradation** (−1.75 pp on Gemma3-27B) and degrades multilingual performance by **−32.4 pp**. The assumption that external retrieval improves cultural VLM reliability is directly contradicted by empirical literature.
4. **Heuristic Linear Ensembling:**
   Fitting logistic regression weights ($w_1, w_2, w_3$) on a small validation set is curve-fitting. It provides no theoretical or mechanistic insight into how transformers arbitrate cross-modal uncertainty.
5. **Unreliability of Visual-Grounding Measurements:**
   Under severe distribution shift, blank-image logit drops ($\Delta_{\text{blank}}$) can be noisy if the text prompt itself induces strong priors.
6. **Calibration Alone as Competing Explanation:**
   Simple post-hoc temperature scaling of softmax probabilities often achieves equivalent risk-coverage curves without requiring any multi-signal fusion (*Xin et al., 2022*).

> **Minimum Defensible Scientific Claim:** If the proposed combination fails, the only defensible finding is: *"External cultural retrieval induces catastrophic label leakage, while blind-image contrastive penalties degrade selective prediction in culturally shifted domains because correct predictions frequently rely on ungrounded textual priors."*
>
> **Definitive Finding:** External cultural text retrieval **must be completely excised**. The investigation must focus strictly on intrinsic model signals: **visual perturbation sensitivity vs. internal hidden-state probes vs. output logit calibration**.

---

## 6. Audit of the Research Question

### Evaluation of the Current Main Question:

> *"Can evidence-grounded uncertainty estimation identify unreliable local-entity predictions in Bangla VLMs and improve the risk–coverage trade-off through selective prediction?"*

- **Status:** **REJECTED in its current form.**
  It is an engineering feasibility query ("can we build a pipeline that works?") rather than a falsifiable scientific question. Furthermore, "evidence-grounded" smuggles in the flawed retrieval pipeline.

### Competing Explanations for Selective Prediction Gains:

If selective prediction achieves lower risk at 80% coverage, what actually caused it?
- **Class Frequency Prior:** The selector simply learned which cultural categories are hard (e.g., abstaining on all textile artifacts and answering only on famous landmarks).
- **Logit Temperature Scaling:** Simple post-hoc temperature scaling of native softmax probabilities achieves 95% of the gain without any perturbation or evidence machinery (*Xin et al., 2022*).
- **Answer Length / Token Entropy:** The model produces longer Bengali token sequences on unfamiliar words, inflating sequence-level uncertainty.
- **Model Capacity:** Larger models have better memorized textual associations, not better visual calibration.

### Reformulated, Falsifiable Scientific Question:

> **Under regional cultural distribution shift, do visual-grounding contrastive probes separate correct from incorrect predictions ($H_1$), or does the presence of correct-but-ungrounded cultural knowledge cause grounding-based selective prediction to penalize true positive answers ($H_0$)?**

- **Hypothesis $H_1$ (Grounding Predicts Correctness):** Even in low-resource cultural domains, correct answers require visual grounding. When the image is ablated ($I = \emptyset$), logit confidence collapses for correct answers but remains static for hallucinations. Selective prediction driven by $\Delta_{\text{blank}}$ improves AUGRC over raw softmax.
- **Hypothesis $H_0$ (The Cultural Knowledge Decoupling):** Models frequently predict the correct cultural entity via unimodal text priors. Consequently, blank-image ablation penalizes correct and incorrect answers equally, rendering visual grounding probes ineffective or harmful for risk-controlled selective prediction.

---

## 7. Audit of Evaluation Quality

### Potential Evaluation Confounders and Required Controls

| Hazard | Source in Pipeline | Impact on Validity | Mandatory Protocol Control |
| :--- | :--- | :--- | :--- |
| **Answer-Leaking Passages** | External RAG passages | Converts visual recognition to reading comprehension; 100% false victory. | **Excise external retrieval completely.** |
| **Image Duplication across Splits** | *BanglaVerse* has 1,152 images expanded into 32.2K dialect/QA items. | Identical images in calibration and test splits cause massive memorization. | **Image-level MD5 hash deduplication; strictly disjoint image splits.** |
| **Subjective Aliasing / Spelling** | Free-form Bengali generation | Phonetic variations (e.g., "নকশী কাঁথা" vs "নকশিকাঁথা") misclassified as errors. | **Use closed multiple-choice benchmarks (*BanglaProtha*) with verified distractors.** |
| **Threshold Tuning Overfitting** | Tuning $\tau$ directly on the test set | Artificially inflates $C@5\%$ coverage. | **Strict 50/50 Calibration/Test split or Split Conformal Risk Control.** |
| **Accuracy-Confounded Metrics** | Using raw Selective Accuracy | Misleading when base accuracy varies across categories. | **Area Under Generalized Risk-Coverage Curve (AUGRC)** (*Traub et al., NeurIPS 2024*). |
| **Model-Generated Explanations as Evidence** | Treating self-generated CoT rationales as evidence | Models confabulate persuasive explanations for hallucinated entities. | **Never score self-generated text as evidence; probe frozen internal states only.** |

### Missing Baselines Required for Valid Interpretation:
1. **Raw Maximum Softmax Probability (MaxProb):** Standard uncalibrated softmax confidence.
2. **Temperature-Scaled Softmax (Platt Scaling):** Standard post-hoc calibration baseline on the validation split.
3. **Blind-Image Prior Baseline ($I = \emptyset$):** VLM evaluated with a completely black canvas to measure pure language-prior accuracy.
4. **Text-Only LLM Baseline:** Evaluating the language backbone (e.g., Qwen2.5-3B) with question text only.
5. **Random Spatial Patch Perturbation:** Shuffling visual patches to verify spatial coherence.

---

## 8. Dataset and Model Reality Check

### Dataset Status

- **BanglaProtha (WACV 2026):**
  - *Public Availability & License:* Verified public on GitHub (`farhanishmam/BanglaProtha`). Open academic license.
  - *Size & Structure:* ~1,200 cultural images, ~3,500 multiple-choice questions with verified, culturally relevant distractors.
  - *Cultural Categories:* Clothing, food, historical sites, folk art, rural instruments, traditional rituals.
  - *Splits & Leakage:* Pre-divided splits exist, but require image-level MD5 hash checking to verify zero cross-split image reuse.
  - *Suitability:* **HIGH.** Closed-vocabulary multiple-choice structure eliminates string-matching ambiguities and provides an exact logit distribution over options (A, B, C, D).
- **BanglaVerse (EMNLP 2026 Findings / arXiv:2603.21165):**
  - *Public Availability & License:* Verified public on Hugging Face.
  - *Size & Structure:* 1,152 images across 9 domains; 20.7K VQA items.
  - *Cultural Categories:* Comprehensive coverage of Bangladeshi daily life and heritage.
  - *Splits & Leakage:* High risk of duplicate images across dialectal splits; requires extensive manual cleaning to extract an entity-disjoint subset.
  - *Suitability:* **MODERATE.** Free-form text answers require complex fuzzy matching.
- **External Cultural Text Corpora (M4-RAG / Wikipedia):**
  - *Suitability:* **FATAL / UNSUITABLE.** Causes immediate verbatim label leakage.

### Model Feasibility on Google Colab (16 GB VRAM Envelope)

- **Qwen2.5-VL-3B-Instruct:**
  - *Footprint:* ~7.5 GB VRAM in native `bfloat16`. Fits comfortably on a free/Pro T4/V100/A100.
  - *Capability:* State-of-the-art compact VLM; excellent native Indic script tokenizer; full open access to hidden states and attention matrices.
  - *Status:* **OPTIMAL PRIMARY WORKHORSE.**
- **Gemma-3-4B-IT:**
  - *Footprint:* ~9.0 GB VRAM in native `bfloat16`.
  - *Status:* **VERIFIED FEASIBLE.** Cross-family architectural control.
- **Qwen2.5-VL-7B-Instruct:**
  - *Footprint:* Exceeds 16 GB in `bfloat16` (~16.8 GB with KV cache); requires 4-bit quantization (BitsAndBytes) on a 16 GB GPU.
  - *Status:* Quantization degrades calibration (*Wieczorek et al., 2026*). Do not use as the primary model; reserve for secondary inference checks if an A100 (40 GB) is available.
- **Fine-Tuning:** **NOT NECESSARY.** The entire investigation is inference-first, evaluating zero-shot forward passes, visual perturbation passes, and linear probing on frozen activations.

---

## 9. Contribution Test: The Null-Result Analysis

**Scenario:** *Experiments reveal that visual-grounding contrastive probes (BICR) do NOT improve selective prediction risk–coverage curves over raw temperature-scaled softmax logits on Bengali cultural entities.*

### Would the Thesis Still Produce a Valuable Scientific Contribution?

- **Under the Initial Pipeline Formulation:** **NO.**
  The thesis would conclude: *"We built a multi-signal fusion system, but it failed to outperform baseline softmax on BanglaVerse."* This is an unpublishable negative engineering outcome.
- **Under the Mechanistic Diagnostic Formulation:** **YES (HIGH-VALUE SCIENTIFIC CONTRIBUTION).**
  A null result provides a landmark finding:
  1. It demonstrates the **failure boundary of visual grounding probes**: while *BICR* works on Western objects (*GQA/COCO*), it breaks down under asymmetric cultural pretraining.
  2. It proves that in culturally localized domains, **correct answers are frequently decoupled from visual evidence**—the model answers correctly from language memory despite visual ambiguity. Penalizing ungrounded answers degrades overall model utility.
  3. This provides a direct, publishable empirical refutation of the prevailing assumption that visual contrastive probing is a universal cure for multimodal hallucination.

---

## 10. Side-by-Side Comparison: Proposals 1, 2, and 3

| Dimension | Proposal 1: Multimodal Reasoning Trace Degradation | Proposal 2: Natural-Image Transfer Audit of Binding IDs | Proposal 3: Modality Dominance & Cultural VLM Calibration |
| :--- | :--- | :--- | :--- |
| **Core Research Question** | Is visual attention decay in extended CoT causal cognitive forgetting ($H_1$) or a RoPE distance / softmax ($M/N$) dilution artifact ($H_0$)? | Do latent "Binding IDs" transfer to natural photographic scenes ($H_1$) or are they destructive perturbation artifacts of synthetic grids ($H_0$)? | Under cultural shift, does miscalibration stem from visual feature ambiguity ($H_1$) or language-prior attentional capture decoupling correctness from grounding ($H_0$)? |
| **Closest Existing Work** | *RH-Bench* (NeurIPS 2025); *Remember-R1* (`arXiv:2608.01314`); *Seeing or Knowing?* (`arXiv:2607.26326`) | *Grounding IDs* (Hasani et al., ICML 2026); *DSCAM* (`arXiv:2608.16805`); *Dual Mechanisms* (`arXiv:2603.22278`) | *SIEVES* (`arXiv:2604.25855`); *BICR* (`arXiv:2605.10893`); *BanglaVerse* (`arXiv:2603.21165`); *CulturalMenuBench* (`arXiv:2609.03526`) |
| **Main Novelty Risk** | Low: Prior literature observed decay but never introduced length-matched neutral placebos or RoPE controls. | Very Low: Direct placebo-controlled refutation of a published ICML 2026 claim. | Moderate-High: Reviewers may view it as applying existing methods (*BICR/SIEVES*) to a regional dataset unless framed strictly as a diagnostic audit. |
| **Experimental Complexity** | Low-Moderate: Teacher-forced prefix slicing, attention mass logging, linear probing. | Moderate: Layer-22 residual stream activation patching, norm-matched Gaussian placebos. | Moderate: Multi-condition visual perturbations (Original, Blank, Mismatched), probe training, AUGRC calculation. |
| **Dataset Risk** | Zero: Turnkey public Hugging Face dataset (`WhatIfVis` counterfactual pairs). | Zero: Synthetic 28×28 grid generator script + public `InstaBind-Lite/DSCAM` images. | Low-Moderate: Public *BanglaProtha*, but requires strict deduplication and category balancing. |
| **Evaluation Risk** | Deterministic: Exact-match regex on counterfactual answer tokens. | Deterministic: Net directed target flip rate ($\text{NetFlip}$) and repetition n-grams. | Deterministic if using *BanglaProtha* MCQA; Fatal if using free-form text or RAG. |
| **Compute Risk** | Negligible: Single forward passes on Colab T4 (~3 hours total). | Negligible: Activation overwrites on Colab T4 (~2 hours total). | Low: 1,500 forward passes on Colab T4 (~45 minutes total). |
| **Leakage Risk** | Zero: Matched counterfactual image pairs. | Zero: Isolated token representations. | Low (if external RAG is excised; Fatal if RAG is included). |
| **Negative-Result Value** | **Outstanding:** Disproves "visual forgetting" as a mathematical artifact of softmax normalization. | **Landmark:** Rebuts published "Grounding IDs" as artifacts of artificial geometric borders. | **Moderate-High:** Proves visual grounding probes fail when models lack cultural world knowledge. |
| **Evidence Confidence** | High (Rooted in formal attention and positional mathematics). | High (Direct replication and extension of an established ICML paper). | Moderate (Empirical calibration varies heavily across model checkpoints). |
| **Remaining Unknowns** | Baseline decay rate in Qwen2.5-VL-3B. | Token alignment between natural images in DSCAM. | Whether language-prior dominance completely suppresses visual logit sensitivity on Bengali MCQA. |

---

## 11. Specific Unresolved Uncertainties

### Classification of Remaining Uncertainties for Proposal 3:

#### Decision-Critical (Could change the thesis decision)
1. **Extent of Language-Prior Dominance on Bengali MCQA:**
   If running `Qwen2.5-VL-3B` on *BanglaProtha* reveals that logit distributions and top predictions remain identical whether the image is present or replaced by a blank canvas ($I = \emptyset$) on >85% of samples, the model is **functionally blind** to visual tokens on Bengali prompts. If a model completely ignores visual inputs, investigating "visual grounding confidence" is impossible.
2. **Image Duplication and Contamination in Bengali Benchmarks:**
   Whether the public splits of *BanglaProtha* or *BanglaVerse* have identical underlying image files appearing across multiple questions or across train/test splits. If image leakage is pervasive, clean out-of-distribution selective calibration cannot be evaluated without rebuilding the dataset from scratch.

#### Important (Worth resolving, but unlikely to change the decision)
3. **Tokenizer Fertility for Cultural Entities in Qwen2.5-VL:**
   Whether Bengali cultural entity names (e.g., "নকশিকাঁথা") are tokenized into 1–2 subwords or fragmented into 6+ byte-level tokens. High fragmentation dilutes sequence-level logit probabilities, requiring length-normalized confidence scores.
4. **Probe Transferability:**
   Whether a linear calibration probe trained on English VQA (*GQA*) transfers zero-shot to Bengali cultural hidden states, or whether it must be retrained on an in-domain Bengali calibration split.

#### Minor (Can be resolved during implementation)
5. **Impact of 4-bit Quantization on Calibration:**
   Whether BitsAndBytes introduces slight calibration drift compared to native `bfloat16`. (Easily resolved by using `Qwen2.5-VL-3B` in unquantized `bfloat16`).

---

## 12. Final Decision-Readiness Report

### A. Current Evidence Status

**MATURE AND AUDITED.**
The evidence base comprehensively maps modern (2024–2026) selective prediction (*SIEVES*, *BCEA*), calibration probing (*BICR*, *TRAPSBench*), and regional cultural benchmarking (*BanglaVerse*, *BanglaProtha*, *ChitraMiti*, *CulturalMenuBench*). No further broad literature searching is required.

### B. Strongest Evidence Supporting the Proposal

- *BanglaVerse* (EMNLP 2026 Findings) proves that 42.6% of VLM errors on Bengali cultural data are local entity misidentifications.
- *TRAPSBench* (COLM 2026) proves that VLMs exhibit a severe representation-output gap: models internally encode uncertainty that autoregressive text generation suppresses.
- *BICR* (`arXiv:2605.10893`, 2026) confirms that contrastive blank-image probes extract calibrated confidence without auxiliary generative reasoners.

### C. Strongest Evidence Against the Proposal

- *SIEVES* and *BCEA* already occupy the combination of visual evidence scoring, abstention, and risk–coverage formalisms.
- Incorporating external cultural retrieval introduces catastrophic verbatim entity leakage, destroying the construct validity of visual calibration.
- *Xin et al.* (ACL 2022) and *Evidence-Order Calibration* (2026) prove that complex evidence-based confidence heads frequently fail to beat simple native softmax confidence for risk ranking.

### D. Most Serious Novelty Threat

**Pre-emption by Methodological Domain Transfer:**
Reviewers will identify the core components as *BICR* (Khanmohammadi et al., 2026) and *SIEVES* (Rodriguez & Rohrbach, 2026) applied to *BanglaVerse* (Sayeedi et al., 2026), dismissing the work as an incremental empirical application unless strictly formulated as a diagnostic audit of cross-modal representation asymmetry.

### E. Most Serious Experimental Threat

**Label Leakage & Unimodal Language Collapse:**
If external retrieval is retained, text passages leak the answer. If external retrieval is excised, compact models may ignore the image entirely, rendering visual perturbation probes inert.

### F. Remaining Decision-Critical Unknowns

1. Does *Qwen2.5-VL-3B* display measurable visual token sensitivity on *BanglaProtha*, or are predictions driven entirely by language priors?
2. Does *BanglaProtha* contain image-level duplicate leakage across its existing splits?

---

### G. Decision Readiness

## **TARGETED VERIFICATION REQUIRED**

*Rationale:* The broad literature investigation is 100% complete, and the constructive "RAG + Selective Prediction" pipeline is definitively invalidated. However, before deciding whether to formally adopt the de-scoped **Diagnostic Audit** as Proposal 3 or discard it in favor of Proposals 1 or 2, exactly two empirical boundary checks must be verified.

---

### H. Targeted Verification Tasks

#### Task 1: Check for Image-Level Duplicate Leakage in the BanglaProtha Repository
- **Exact Question:** Do identical image files (verified via MD5 hashes) appear across multiple question instances or across the official train and test splits in `farhanishmam/BanglaProtha`?
- **Why It Matters:** If multiple-choice questions share identical underlying cultural images across splits, any trained probe or calibrated threshold will overfit to memorized visual features, invalidating the evaluation.
- **Source Type:** Direct inspection of the public GitHub metadata and image files in `farhanishmam/BanglaProtha`.
- **Strengthens Proposal:** Proof that splits are strictly image-disjoint and entity-stratified.
- **Weakens/Rejects Proposal:** Discovery that identical images are reused across splits with different question phrasings.

#### Task 2: Audit Language-Prior Collapse (Blind-Image Sensitivity Check)
- **Exact Question:** When running a zero-shot pass of `Qwen2.5-VL-3B-Instruct` on 20 sample items from *BanglaProtha*, what percentage of predictions and top logits change when replacing the cultural image with a blank black canvas ($I = \emptyset$)?
- **Why It Matters:** If prediction and confidence remain identical on >85% of items, the model is completely blind to visual tokens on Bengali cultural prompts. A thesis on "visual calibration" cannot be conducted on a model that ignores visual inputs.
- **Source Type:** Headless inspection measuring logit delta $\Delta_{\text{logit}} = \max \ell(I, q) - \max \ell(\emptyset, q)$ on a small sample of *BanglaProtha* instances.
- **Strengthens Proposal:** $\Delta_{\text{logit}} > 0.30$ on the majority of samples, confirming active cross-modal attention.
- **Weakens/Rejects Proposal:** $\Delta_{\text{logit}} \approx 0$ across >85% of samples, proving complete language-prior attentional capture.

#### Task 3: Inspect Tokenizer Fertility for Cultural Entities in Qwen2.5-VL
- **Exact Question:** Does the `Qwen2.5-VL` tokenizer segment Bengali cultural entity names (e.g., "নকশিকাঁথা", "রসগোল্লা", "পহেলা বৈশাখ") into 1–2 tokens, or does it split them into byte-level fragments ($\ge 6$ tokens)?
- **Why It Matters:** If entity names undergo severe token fragmentation, sequence-level likelihoods and logit-derived confidence scores decay exponentially with token length, confounding uncertainty estimation with morphological segmentation.
- **Source Type:** `AutoTokenizer.from_pretrained("Qwen/Qwen2.5-VL-3B-Instruct")` executed on the list of target entity names from *BanglaProtha*.
- **Strengthens Proposal:** High tokenizer compression ratio ($\le 2.5$ tokens per cultural entity name).
- **Weakens/Rejects Proposal:** Severe fragmentation ($\ge 6$ tokens per word), which distorts token-level calibration metrics.
