# Canonical Research Proposal: Proposal 3 (Field D Refined)

**Project Title:** Decoupling Visual Reliance from Correctness: A Placebo-Controlled Diagnostic of Cultural Prior Dominance and Selective Prediction in Multimodal VLMs  
**Domain:** Multimodal Representation Learning, Uncertainty Calibration & Selective Prediction in Vision-Language Models (VLMs)  
**Primary Anchor Literature:**
- *Grounded or Guessing? LVLM Confidence Estimation via Blind-Image Contrastive Ranking (BICR)* (`arXiv:2605.10893`, May 2026)
- *SIEVES: Selective Prediction Generalizes through Visual Evidence Scoring* (`arXiv:2604.25855`, April 2026)
- *Evidence-Order Calibration: Selective Visual Reasoning Under Progressive Masking* (`arXiv:2609.09184`, September 2026)
- *CulturalMenuBench: Quantifying the Knowledge-Application Gap in Multimodal Culture* (`arXiv:2609.03526`, September 2026)
- *ChitraMiti: Modality Reliance and Geometric Diagnostics in Bengali VLMs* (`arXiv:2609.12509`, September 2026)
- *BanglaProtha: Evaluating Vision Language Models in Underrepresented Long-Tail Cultural Contexts* (IEEE/CVF WACV 2026, pp. 1159–1169)
**Document Type:** Standalone Canonical Research Specification & Execution Protocol  
**Version:** 1.0 (Post-RAG Excision & Modality-Decoupling Diagnostic Refinement)

---

## 1. Executive Summary & Problem Formulation

In general Western vision-language benchmarks (GQA, POPE, V* Bench), recent literature (*BICR*, *SIEVES*, *BCEA*) establishes that multimodal hallucinations frequently stem from **visual ungroundedness**—models outputting confident responses driven purely by autoregressive language priors while ignoring visual tokens. To prevent dangerous overconfident errors, modern selective prediction systems penalize ungrounded answers by measuring visual sensitivity (e.g., using blind-image contrastive hidden-state ranking $\Delta_{\text{blank}}$ or visual crop localization quality), achieving significant risk-coverage gains ($C@1\%$, AUGRC).

However, in culturally localized and low-resource multimodal domains (exemplified by Bengali cultural artifacts, attire, food, and historical sites), foundation VLMs operate under **Asymmetric Cross-Modal Pretraining Representation**:
1. **Visual Representation Sparsity:** Pretraining visual tokens for regional cultural entities (*Nakshi Kantha*, *Shorshe Ilish*, *Kula*, *Pitha*) are sparse and low-resolution in foundation Vision Transformer (ViT) weights.
2. **Textual Prior Dominance:** The underlying LLM backbone possesses moderate-to-high textual memorization of these entities from web-scraped corpora.
3. **The Correct-but-Ungrounded Anomaly:** As proven by *CulturalMenuBench* and *ChitraMiti*, models frequently predict the *correct* cultural entity via textual context heuristics without attending to discriminatory visual features.

This creates a fundamental scientific tension: **BICR and SIEVES assume that visually ungrounded answers are incorrect hallucinations that must be penalized.** In cultural domains, penalizing ungrounded predictions may systematically suppress answers that are **empirically correct due to ungrounded cultural text priors**, causing visual-grounding selective prediction to degrade below simple native softmax calibration (the *Evidence-Order Trap*).

### The Research Question
> **When vision-language models encounter culturally localized entities under asymmetric pretraining, does visual grounding sensitivity remain a valid predictor of answer correctness ($H_1$), or does the presence of correct-but-ungrounded cultural knowledge decouple correctness from visual reliance, causing visual-grounding-based selective prediction to penalize true positive answers and fail to outperform native softmax confidence ($H_0$)?**

---

## 2. Competing Hypotheses & Falsifiable Signatures

* **Hypothesis $H_1$ (Grounding Anchors Reliability Across Shift):**  
  Even under regional cultural distribution shift, correct predictions causally require discriminatory visual tokens. When visual tokens are ablated ($I = \mathbf{0}$) or scrambled, confidence collapses significantly more for correct answers than for hallucinations. Gating selective abstention via visual contrastive sensitivity ($\Delta_{\text{blank}}$) achieves a strictly superior Area Under Generalized Risk-Coverage Curve ($\Delta \text{AUGRC} > 0.05, p < 0.001$) over native temperature-scaled softmax confidence.  
  *Observable Signature:* The Modality Reliance Index (MRI) of correct answers is significantly higher than that of incorrect answers ($\text{MRI}_{\text{correct}} \gg \text{MRI}_{\text{incorrect}}, p < 0.001$), and selective coverage at 5% error tolerance triples ($C@5\% \ge 2.5 \times \text{Baseline}$).

* **Hypothesis $H_0$ (Cultural Decoupling & Evidence-Order Collapse):**  
  Correct cultural predictions are driven primarily by unimodal language priors, decoupling answer accuracy from visual perception. Consequently, blank-image ablation penalizes correct and incorrect predictions equally, or penalizes correct answers more heavily. Gating selective prediction via visual grounding suppresses true positives, resulting in selective risk-coverage curves that fail to beat or are strictly inferior to simple post-hoc temperature-scaled softmax logits ($\Delta \text{AUGRC} \le 0$).  
  *Observable Signature:* The Correct-but-Ungrounded Disparity $\delta_{\text{CUG}}$ exceeds $35\%$ across cultural categories, and raw Platt-scaled softmax matches or outperforms visual-grounding selectors for selective risk ranking.

---

## 3. Scientific Gap & Boundary Conditions

| What Prior Work Established | What Prior Work Did NOT Establish (The Live Gap) |
| :--- | :--- |
| *BICR* (`arXiv:2605.10893`) proved blind-image contrastive ranking penalizes ungrounded answers and calibrates VLM confidence on English VQA. | Explicitly left multilingual and culturally localized settings untested; assumed ungrounded answers are always hallucinations. |
| *SIEVES* (`arXiv:2604.25855`) showed visual evidence localization scores improve selective VQA under severe OOD distribution shift. | Tested exclusively on fine-grained Western spatial reasoning (V* Bench); did not test non-Western cultural parametric gaps. |
| *Evidence-Order* (`arXiv:2609.09184`) proved that visual evidence-supervised heads fail to outperform raw softmax confidence for selective risk ranking on English GQA. | Evaluated English spatial reasoning; did not test whether modality reliance failure is magnified under cultural pretraining asymmetry. |
| *CulturalMenuBench* (`arXiv:2609.03526`) proved that cultural food names in text outperform image presentations by +7–18 pts (knowledge-application gap). | Evaluated accuracy only; evaluated zero uncertainty calibration, selective prediction, or risk-coverage formalisms. |
| *BanglaProtha* (WACV 2026) benchmarked open VLMs on Bengali cultural MCQA with semantically similar distractors. | Evaluated accuracy and prompting strategies only; evaluated zero uncertainty calibration or selective abstention. |

---

## 4. Complete 4-Arm Experimental Factorial Design

To eliminate sequence length, prompt formatting, and distractor confounds, all experiments use a **strictly image-disjoint, entity-stratified subset of 500 items from BanglaProtha** (evaluated as 4-way Multiple-Choice Question Answering predicting single-token option letters $A, B, C, D$):

```
                        INPUT: Multimodal Stimulus (Image + Bengali MCQA Prompt)
                                                   │
         ┌─────────────────────────┬───────────────┴───────────────┬─────────────────────────┐
         ▼                         ▼                               ▼                         ▼
    [Condition 1]             [Condition 2]                   [Condition 3]             [Condition 4]
  Full Multimodal          Blind-Image Ablation            Spatial Patch Scramble      Text-Only LLM
  Original Image I         Solid Black Image I = 0         Randomized 14x14 Patches    Vision Encoder Bypassed
  + Bengali MCQA           + Identical MCQA Prompt         + Identical MCQA Prompt     Question + Options Only
  (Baseline Accuracy)      (Unimodal Language Prior)       (Spatial Coherence Control) (Parametric Knowledge Bound)
```

### Protocol Specifications
1. **Condition 1 (Full Multimodal Stimulus - $I_{\text{full}}$):** Standard forward pass with original cultural image and prompt. Extracts top predicted option letter $y^* \in \{A, B, C, D\}$ and option softmax probability distribution $p(y \mid I_{\text{full}}, q)$.
2. **Condition 2 (Blind-Image Ablation - $I_{\text{blank}}$):** Forward pass replacing the image with a blank black canvas ($I = \mathbf{0}$) of identical pixel resolution, keeping the prompt and option order identical. Computes the unimodal prior logit distribution $p(y \mid \mathbf{0}, q)$ and the contrastive logit sensitivity:
   $$\Delta_{\text{blank}} = \ell(y^* \mid I_{\text{full}}, q) - \ell(y^* \mid \mathbf{0}, q)$$
3. **Condition 3 (Spatial Patch Scramble - $I_{\text{scramble}}$):** Divides the image into $14 \times 14$ visual patches and randomly permutes their 2D grid coordinates before ViT encoding. Controls for low-level color histogram and background texture distribution while destroying semantic geometry. Isolates semantic visual recognition from global color shortcuts.
4. **Condition 4 (Text-Only LLM Control - No Vision Encoder):** Passes the textual prompt and options directly to the frozen text-decoder backbone (e.g., `Qwen2.5-3B-Instruct` text model). Directly measures pure parametric world knowledge in the language model, bounding the *knowledge-application gap*.

---

## 5. Mathematical Metrics & Evaluation Formulations

### 1. Modality Reliance Index (MRI)
Quantifies the normalized causal contribution of the image to the model's top predicted answer:
$$\text{MRI}_i = \frac{p(y^* \mid I_{\text{full}}, q_i) - p(y^* \mid \mathbf{0}, q_i)}{p(y^* \mid I_{\text{full}}, q_i)}$$
* $\text{MRI}_i \approx 1$: Completely visually grounded prediction.
* $\text{MRI}_i \le 0$: Unimodal text-prior prediction (model is equally or more confident without the image).

### 2. Correct-but-Ungrounded Disparity ($\delta_{\text{CUG}}$)
Measures the proportion of correct cultural predictions that occur under near-zero visual reliance ($\text{MRI} < 0.10$):
$$\delta_{\text{CUG}} = \frac{\sum_{i=1}^N \mathbf{1}(y_i = y_i^* \land \text{MRI}_i < 0.10)}{\sum_{i=1}^N \mathbf{1}(y_i = y_i^*)}$$
If $\delta_{\text{CUG}} > 0.30$, cultural knowledge decoupling is pervasive.

### 3. Area Under the Generalized Risk-Coverage Curve (AUGRC)
Following *Traub et al. (NeurIPS 2024)*, evaluate selective prediction by ordering samples by selection score $g(x)$ and computing risk $\mathcal{R}(\tau)$ across coverage $\mathcal{C}(\tau) \in [0, 1]$:
$$\text{AUGRC} = \int_0^1 \mathcal{R}(c) \, dc$$
Compare three selection functions:
1. **Raw MaxProb Softmax:** $g_{\text{raw}}(x) = \max_y p(y \mid I, q)$
2. **Temperature-Scaled Softmax (Platt):** $g_{\text{temp}}(x) = \max_y \text{Softmax}(\ell(x) / T^*)$
3. **Grounding-Contrastive Score:** $g_{\text{ground}}(x) = \Delta_{\text{blank}}(x)$
4. **Residual Hidden-State Probe:** $g_{\text{probe}}(x) = \sigma(w^T h_L(x) + b)$ trained with BICR ranking loss.

### 4. Relative Selective Advantage ($\Delta \text{AUGRC}$)
$$\Delta \text{AUGRC} = \text{AUGRC}(g_{\text{temp}}) - \text{AUGRC}(g_{\text{ground}})$$
A positive $\Delta \text{AUGRC}$ indicates visual grounding successfully improves selective prediction risk-coverage; a non-positive score ($\le 0$) confirms the Evidence-Order trap.

---

## 6. Execution Architecture & Engineering Blueprint

* **Primary Model:** `Qwen/Qwen2.5-VL-3B-Instruct` (native Indic script vocabulary, open access to hidden states, unquantized `bfloat16`).
* **Cross-Architecture Control:** `google/gemma-3-4b-it` (SigLIP vision tower vs. Qwen ViT tower).
* **Dataset Infrastructure:**
  * Sourced from verified WACV 2026 *BanglaProtha* release (6,942 images / 8,034 QA pairs).
  * Sample 500 items strictly balanced across 5 representative cultural domains: Food, Clothing & Fashion, Social Life, Arts & History, Nature.
  * Compute image-level MD5 hashes to guarantee 100% image-disjoint partitioning between calibration (250 items) and test (250 items) splits.
* **Hardware Footprint:** Single GPU with $\ge 15\text{ GB}$ VRAM (Google Colab Free/Pro T4, V100, or L4).
* **Compute Budget:**
  * 500 items $\times$ 3 image conditions (Original, Blank, Scrambled) = 1,500 forward passes.
  * Inference execution time: $\approx 40\text{ minutes}$ total on a single T4 GPU. Zero training required.

---

## 7. Decisive Kill Tests & Scientific Utility

* **Kill Condition K1 (Total Visual Insensitivity):** If $> 80\%$ of samples exhibit $|\Delta_{\text{blank}}| < 0.02$ (logit invariance under complete image black-out), kill the proposal. The model is functionally blind to visual tokens on Bengali prompts; investigating visual calibration is physically impossible.
* **Kill Condition K2 (The Evidence-Order Trap):** If the visual grounding selection score $g_{\text{ground}}$ fails to beat simple temperature-scaled softmax by at least $\Delta \text{AUGRC} > 0.02$, kill the claim that visual grounding aids selective reliability.
* **Why the Result is High-Value Either Way (Publication Symmetry):**
  * **If $H_1$ holds:** Publishable as the first empirical confirmation that visual-reliance contrastive probes transfer zero-shot to non-Western cultural distribution shifts, refuting the fear of cultural language-prior dominance.
  * **If $H_0$ holds:** Publishable in ACL/EMNLP/CVPR as a landmark diagnostic discovery: *"Why Visual Grounding Fails to Calibrate Multimodal VLMs: Cultural Knowledge Decoupling under Asymmetric Pretraining."* It proves that in low-resource cultures, foundation VLMs answer correctly via ungrounded text memory, demonstrating why Western hallucination-mitigation techniques (penalizing ungrounded tokens) actively backfire when deployed globally.
