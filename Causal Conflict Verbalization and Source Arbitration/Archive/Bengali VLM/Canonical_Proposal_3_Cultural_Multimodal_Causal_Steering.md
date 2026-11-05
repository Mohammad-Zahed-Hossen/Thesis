# Canonical Research Proposal: Proposal 3 (Field D Refined — Causal & Mechanistic Formulation)

**Project Title:** Disentangling Perceptual Deficit from Late-Layer Parametric Pre-emption: Causal Bottleneck Localization and Activation Steering in Low-Resource Cultural VLMs  
**Domain:** Multimodal Representation Learning, Cross-Modal Mechanistic Interpretability & Representation Steering in Vision-Language Models (VLMs)  
**Primary Anchor Literature:** 
- *Where Do Multilingual VLM Encoders Fail?* (`arXiv:2608.30725`, August 2026, Anchor D1)
- *TRAPSBench: Probing Internal Uncertainty vs. Autoregressive Verbalization in VLMs* (`arXiv:2608.13167`, August 2026, Anchor D2)
- *Dual Mechanisms of Visual Binding in Vision-Language Models* (`arXiv:2603.22278`, Cui et al., March 2026, Anchor D3)
- *CulturalMenuBench: Quantifying the Knowledge-Application Gap in Multimodal Culture* (`arXiv:2609.03526`, September 2026, Anchor D4)
- *ChitraMiti: Modality Reliance and Cross-Modal Verification Flaws in Bengali VLMs* (`arXiv:2609.12509`, September 2026, Anchor D5)
- *BanglaProtha: Evaluating Vision Language Models in Underrepresented Long-Tail Cultural Contexts* (IEEE/CVF WACV 2026, pp. 1159–1169)  
**Document Type:** Standalone Canonical Research Specification & Execution Protocol  
**Version:** 2.1 (Production-Grade Decision-Ready Blueprint with Exact Math, Data Slicing, and Execution Roadmap)

---

## 1. Executive Summary & Problem Formulation

When modern vision-language models (e.g., Qwen2.5-VL, Gemma-3) encounter culturally localized, non-Western visual tasks (such as Bengali cultural artifacts, attire, and cuisine in *BanglaProtha* and *BanglaVerse*), they exhibit severe failure rates and hallucination. 

Existing literature approaches this failure through two superficial, conflicting narratives:
1. **The "Perceptual Blindness" Narrative:** Vision transformers (ViTs) pre-trained primarily on Western web-scraped data cannot extract discriminatory low-level visual features for localized cultural entities (*ChitraMiti*).
2. **The "Missing Cultural Knowledge" Narrative:** The model's language backbone simply lacks encyclopedic factual knowledge about regional entities (*BanglaVerse*).

Because prior art relies almost exclusively on **passive benchmark evaluation** (measuring final-token accuracy or ablated selective risk curves), it treats the VLM as an impenetrable black box. It fails to answer the foundational scientific question: **Where and why does the multimodal computational pipeline actually break down?**

### The Core Mechanistic Mystery: The Three-Stage Bottleneck
In a foundation VLM processing a cultural stimulus $(\text{Image } I, \text{Bengali Prompt } q)$, visual tokens pass through three critical phases:
* **Stage 1 (Vision Encoder ViT):** Does the ViT extract distinguishing spatial/semantic features into visual patch tokens?
* **Stage 2 (Multimodal Projector & Cross-Lingual Alignment):** Does the cross-modal projection correctly map visual tokens into the lexical semantic space of low-resource Bengali tokens, or does it only align with dominant English tokens?
* **Stage 3 (Deep Transformer Residual Stream):** Are visual tokens successfully injected into early LLM layers, only to be **actively pre-empted and extinguished by strong autoregressive language priors** in intermediate-to-late transformer layers ($L18\text{--}28$)?

If Stage 3 dominates—a phenomenon we define as **Late-Layer Parametric Pre-emption**—the model does not fail because it is "blind" or "ignorant." It fails because its late transformer layers overwrite active perceptual evidence with high-frequency language attractors.

### The Research Question
> **When a vision-language model fails on a culturally localized multimodal task, is the failure caused by early perceptual blindness in the vision encoder (Stage 1), cross-lingual lexical misalignment in the projector (Stage 2), or late-layer parametric pre-emption where language priors overwrite preserved visual representations in the residual stream (Stage 3)? Furthermore, can a localized causal intervention—residual activation steering—prevent this pre-emption and restore grounded cultural recognition without retraining?**

---

## 2. Competing Hypotheses & Falsifiable Signatures

* **Hypothesis $H_1$ (Late-Layer Parametric Pre-emption & Restorable Grounding):**  
  The vision encoder and projector successfully encode and inject fine-grained cultural visual features into early-to-mid LLM residual stream layers ($L \le 16$). However, between Layers 18 and 28, strong parametric language priors dominate the residual stream, actively extinguishing visual token decodability and driving the final logit head to hallucinate or guess.  
  *Observable Signatures:*
  1. **Probe Decodability Trajectory:** A linear probe trained to classify the ground-truth cultural entity achieves high classification accuracy ($\text{AUC} > 0.80$) in intermediate residual layers ($L12\text{--}16$), followed by a sharp monotonic collapse ($\Delta \text{AUC} > -0.30$) in late layers ($L22\text{--}30$).
  2. **Causal Activation Steering Recovery:** Subtracting the language-prior direction and reinforcing the visual direction at Layer 18 causally restores the correct grounded token prediction at the output head ($\text{Steering Recovery Rate} \ge 35\%, p < 0.001$) without inducing linguistic repetition or degeneration.

* **Hypothesis $H_0$ (Early Perceptual / Alignment Bottleneck):**  
  Visual representations of low-resource cultural entities never penetrate the LLM backbone. Due to pretraining representation sparsity, the vision encoder outputs isotropic, uninformative patch tokens, or the projector fails to align them with non-Latin lexical representations.  
  *Observable Signatures:*
  1. Residual stream linear probes fail to decode the cultural entity across **all** layers ($\text{AUC} \le 0.55$ at all layers $L1\text{--}32$, indistinguishable from chance).
  2. The failure is completely invariant to language-prior steering; intermediate layer activation interventions produce only random token degeneration ($\mathcal{D}_{\text{rep}} > 0.40$).

---

## 3. Scientific Gap & Boundary Conditions

| What Prior Work Established | What Prior Work Did NOT Establish (The Live Gap) |
| :--- | :--- |
| *BanglaProtha* (WACV 2026) & *BanglaVerse* (`arXiv:2603.21165`) evaluated black-box accuracy on Bengali cultural MCQA. | Purely observational benchmarks. Evaluated zero internal representations, zero layer-wise probing, and zero causal interventions. |
| *Where Do Multilingual VLM Encoders Fail?* (`arXiv:2608.30725`) showed language alignment drift in multilingual encoders. | Analyzed encoder token cosine similarities; did not track residual stream propagation or test causal activation steering. |
| *TRAPSBench* (`arXiv:2608.13167`) proved linear probes decode uncertainty in physics videos better than text generation. | Evaluated Western physics simulation counterfactuals; did not investigate cultural distribution shift or late-layer pre-emption. |
| *BICR* (`arXiv:2605.10893`) & *SIEVES* (`arXiv:2604.25855`) used blind-image ablations to score output confidence. | Passive black-box scoring; treated ungroundedness as an output error rather than an internal layer-wise causal competition. |
| *CulturalMenuBench* (`arXiv:2609.03526`) identified a knowledge-application gap between food text names and image plates. | Evaluated behavioral prompt variations; executed no mechanistic probing or internal representation repair. |

---

## 4. Complete 4-Arm Experimental Factorial Design

The protocol evaluates 200 cultural MCQA items from *BanglaProtha* (strictly 50 Food, 50 Attire, 50 Architecture, 50 Traditional Craft/Heritage; deduplicated across unique images) across four controlled experimental arms:

```
                        INPUT: Multimodal Stimulus (Image I + Bengali MCQA Prompt q)
                                                      │
       ┌───────────────────────┬──────────────────────┴───────────────────────┬───────────────────────┐
       ▼                       ▼                                              ▼                       ▼
  [Arm 1: Standard]      [Arm 2: Cross-Lingual]                        [Arm 3: Patch Zoom]    [Arm 4: Steering Intervention]
  Original Image I       Original Image I                              Cropped Cultural Entity  Residual Activation Steering
  + Bengali MCQA Prompt  + English Parallel Prompt                     + Bengali MCQA Prompt    at Layer L* = 18
  (Full Cultural End-to- (Isolates Cross-Lingual Lexical               (Isolates ViT Perceptual (Causal Test of Late-Layer
   End Pipeline)          Alignment from Perceptual Features)           Sparsity from Semantics) Parametric Pre-emption)
```

### Protocol Specifications
1. **Arm 1 (Standard Multimodal Baseline):** Standard forward pass with original cultural image and Bengali MCQA prompt. Records token probabilities, attention maps, and extracts residual-stream activation vectors $h_L \in \mathbb{R}^{D}$ at every transformer layer $L \in \{0, 4, 8, \dots, 32\}$.
2. **Arm 2 (Cross-Lingual Alignment Control):** Feeds the exact same visual image paired with a verified, meaning-preserving English translation of the question and options.  
   *Diagnostic Function:* If the model correctly identifies the entity in English but fails in Bengali, the vision encoder (Stage 1) is exonerated, isolating the bottleneck to cross-lingual lexical projection (Stage 2).
3. **Arm 3 (Localized Crop / Spatial Zoom):** Feeds an isolated high-resolution bounding-box crop of the diagnostic cultural object (e.g., the specific embroidery motif of a *Nakshi Kantha* or the spice pattern of *Shorshe Ilish*).  
   *Diagnostic Function:* If accuracy and probe decodability remain at chance, the vision encoder is genuinely blind to cultural micro-features (Stage 1 failure). If accuracy surges, the failure was background clutter / spatial dilution.
4. **Arm 4 (Causal Activation Steering at Layer $L^* = 18$):** Intercepts the forward pass at intermediate layer $L^* = 18$ (identified via layer-wise probing) and applies a contrastive steering vector $\vec{v}_{\text{steer}}$ that suppresses the language-prior direction while amplifying visual token attention:
   $$h_{L^*}^{\text{steered}} = h_{L^*} - \alpha \vec{v}_{\text{prior}} + \beta \vec{v}_{\text{vis}}$$
   *Diagnostic Function:* Causal proof of Stage 3. If modifying intermediate residual states flips incorrect outputs into correct cultural identifications, the information was present internally and pre-empted by late-layer autoregression.

---

## 5. Mathematical Metrics & Mechanistic Formulations

### 1. Layer-Wise Probe Decodability ($\text{AUC}_L$)
Train a 5-fold cross-validated ridge-regularized logistic regression probe on residual-stream activations $h_L(t_{\text{last}})$ at each layer $L$ to predict the ground-truth cultural class:
$$\mathcal{L}_{\text{probe}}(\mathbf{w}_L) = \sum_{i=1}^{N_{\text{train}}} \ell\left(\mathbf{w}_L^T h_{L}^{(i)}, y_i\right) + \lambda \|\mathbf{w}_L\|_2^2$$
We record the decodability curve $\text{AUC}(L)$ across all layers. The **Pre-emption Gradient** is defined as:
$$\nabla_{\text{preempt}} = \max_{L \le 16} \text{AUC}(L) - \text{AUC}(L_{\text{final}})$$
A positive gradient ($\nabla_{\text{preempt}} > 0.25$) formally confirms late-layer representation suppression.

### 2. Exact Steering Vector Construction
Extract the contrastive steering components on a disjoint 20-sample validation set:
* **Language Prior Direction:** The mean residual activation vector under blind-image input ($I = \mathbf{0}$):
  $$\vec{v}_{\text{prior}} = \frac{1}{N_{\text{val}}} \sum_{i=1}^{N_{\text{val}}} h_{L^*}(t_{\text{last}} \mid \mathbf{0}, q_i)$$
* **Contrastive Visual Evidence Direction:** The mean residual shift between full image and blind image:
  $$\vec{v}_{\text{vis}} = \frac{1}{N_{\text{val}}} \sum_{i=1}^{N_{\text{val}}} \left( h_{L^*}(t_{\text{last}} \mid I_i, q_i) - h_{L^*}(t_{\text{last}} \mid \mathbf{0}, q_i) \right)$$
* **Steering Hyperparameters:** $\alpha, \beta \in [0.5, 2.0]$ are selected on the validation split via grid search to maximize target logit margin.

### 3. Causal Steering Recovery Rate ($\text{SRR}$)
Among the subset of items where the baseline model predicts an incorrect cultural distractor ($\hat{y} \ne y^*$), measure the fraction converted to the ground-truth entity under Layer 18 activation steering:
$$\text{SRR} = \frac{\sum_{i \in \text{Errors}} \mathbf{1}\left( \text{argmax } p(y \mid I, q, \vec{v}_{\text{steer}}) = y_i^* \right)}{|\text{Errors}|}$$

### 4. Linguistic Fluency Preservation ($\mathcal{D}_{\text{rep}}$)
Verify that activation steering does not break the language model's autoregressive coherence using 3-gram repetition frequency:
$$\mathcal{D}_{\text{rep}} = 1 - \frac{\text{Unique 3-grams}}{\text{Total 3-grams}}$$
Steering is rejected as destructive disruption if $\mathcal{D}_{\text{rep}} > 0.35$.

---

## 6. Execution Architecture & Engineering Blueprint

* **Primary Model:** `Qwen/Qwen2.5-VL-3B-Instruct` (open weights, native ViT, full hidden-state access).
* **Secondary Model:** `google/gemma-3-4b-it` (SigLIP architecture, cross-family architectural validation).
* **Hardware Footprint:** Single GPU (16 GB VRAM, e.g., T4 / L4 on Google Colab or local workstation).
* **Compute Budget:** $200 \text{ items} \times 4 \text{ arms} = 800 \text{ forward passes}$. Total run time: $\approx 25\text{--}35 \text{ minutes}$ on a single T4 GPU.
* **Hook Implementation:**
  - Register PyTorch forward hooks on `model.model.language_model.layers[L]` to extract and inject hidden states dynamically.
  - Compute running probe projections on the fly to avoid storing multi-gigabyte activation tensors in memory.
  - Set `torch.inference_mode()` with selective tensor detachment.

---

## 7. Decision Thresholds & Falsification Matrix

| Experimental Metric | Positive Result ($H_1$: Pre-emption / Live Research Contribution) | Null / Boundary Result ($H_0$: Early Perceptual / Projection Failure) | Scientific Consequence |
| :--- | :--- | :--- | :--- |
| **Layer-Wise Probe Trajectory** | $\max_{L \le 16} \text{AUC}_L \ge 0.75$ and $\nabla_{\text{preempt}} \ge 0.25$ ($p < 0.001$) | $\text{AUC}_L \le 0.55$ across all layers $L \in [0, 32]$ | Confirms whether cultural features are encoded internally or lost before entering the LLM. |
| **Cross-Lingual Alignment Gap** | $\text{Acc}_{\text{EN}} \approx \text{Acc}_{\text{BN}}$ (Gap $< 5\%$) | $\text{Acc}_{\text{EN}} - \text{Acc}_{\text{BN}} > 25\%$ ($p < 0.001$) | Exonerates vs. convicts cross-lingual lexical projection as the primary failure point. |
| **Steering Recovery Rate ($\text{SRR}$)** | $\text{SRR} \ge 35\%$ with $\mathcal{D}_{\text{rep}} < 0.25$ | $\text{SRR} < 10\%$ or generation collapses ($\mathcal{D}_{\text{rep}} > 0.40$) | Validates whether internal representations can be actively steered to repair cultural errors without fine-tuning. |

---

## 8. Four-Week Milestone & Execution Roadmap

To guarantee a clean, polished, completed thesis within undergraduate time constraints:

```
┌──────────────────────────────────────────────────────────────────────────────────────┐
│ Week 1: Data Preparation & Multimodal Baseline Runs                                  │
│ - Curate 200 image-disjoint items from BanglaProtha across 4 categories.             │
│ - Author verified parallel English prompts for Arm 2.                                │
│ - Execute Arms 1-3 forward passes; record base accuracy & logit distributions.       │
├──────────────────────────────────────────────────────────────────────────────────────┤
│ Week 2: Layer-Wise Residual Extraction & Linear Probe Training                       │
│ - Hook residual streams at layers L ∈ {0, 4, 8, ..., 32}.                            │
│ - Train 5-fold cross-validated linear probes; plot layer-wise AUC trajectory curves. │
│ - Calculate Pre-emption Gradient ∇_preempt to locate optimal steering layer L*.      │
├──────────────────────────────────────────────────────────────────────────────────────┤
│ Week 3: Causal Activation Steering & Recovery Audit                                  │
│ - Compute contrastive steering vectors (v_prior, v_vis) on 20-sample validation set. │
│ - Apply Layer 18 steering hooks on incorrect baseline items; compute SRR.            │
│ - Run linguistic fluency controls (D_rep, perplexity) to ensure generation safety.   │
├──────────────────────────────────────────────────────────────────────────────────────┤
│ Week 4: Statistical Consolidation, Thesis Chapter Drafting & Visualizations          │
│ - Generate publication-ready layer-wise probe curves, recovery bar charts, and       │
│   qualitative error-to-correction visualizations. Complete draft chapter.            │
└──────────────────────────────────────────────────────────────────────────────────────┘
```

---

## 9. The "No-Loss" Thesis Defense Guarantee

A major hallmark of polished research is having **zero dead ends**:
* **If $H_1$ holds:** You deliver a landmark mechanistic discovery—proving that foundation VLMs actually perceive low-resource cultural artifacts but suppress them in late layers—and you present a training-free **activation steering method** that repairs errors at test-time.
* **If $H_0$ holds:** You deliver the first rigorous empirical refutation of the prevailing claim in prior literature (*BanglaVerse*) that cultural errors stem from "missing knowledge." You prove conclusively that the failure is an early **perceptual/projection bottleneck**, establishing a foundational baseline that redirects future research toward cultural visual pre-training.

Both outcomes produce a complete, polished, publishable undergraduate thesis.
