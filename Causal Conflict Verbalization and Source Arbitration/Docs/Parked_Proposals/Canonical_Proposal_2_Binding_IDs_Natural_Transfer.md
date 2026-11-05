# Canonical Research Proposal: Proposal 2 (Field C Refined)

**Project Title:** Do Latent Visual Binding Identifiers Survive Beyond Synthetic Grids? A Placebo-Controlled Natural-Image Transfer Audit  
**Domain:** Multimodal Representation Learning & Mechanistic Interpretability in Vision-Language Models (VLMs)  
**Primary Anchor Literature:** 
- *Uncovering Grounding IDs: How External Cues Shape Multimodal Binding* (ICML 2026, `arXiv:2509.24072`, Anchor C1)
- *Investigating Mechanisms for In-Context Vision Language Binding* (CVPRW 2025, `arXiv:2505.22200`, Anchor C2)
- *Dual Mechanisms of Visual Binding in Vision-Language Models* (`arXiv:2603.22278`, Cui et al.)
- *InstaBind-Lite / DSCAM: Benchmarking Dense Same-Class Attribute Misbinding* (`arXiv:2608.16805`, Xu et al.)
**Document Type:** Standalone Canonical Research Specification & Execution Protocol  
**Version:** 1.0 (Post-C1 Re-evaluation & Placebo-Controlled Natural Transfer)

---

## 1. Executive Summary & Problem Formulation

In vision-language models, the **visual binding problem** asks how the model correctly associates an object's spatial tokens with its semantic attributes (e.g., "red shirt" vs. "blue jeans" in a crowded scene) rather than misbinding attributes across objects.

Recent mechanistic literature (*Anchor C1: Hasani et al., ICML 2026*) claimed to identify latent **"Grounding IDs"** or **"Binding IDs"** in Qwen2.5-VL and InternVL. By swapping the residual-stream hidden states of object patches between paired contexts in intermediate layers ($L20\text{--}27$), they reported that the model's generated text redirected toward the source object's attributes with 98% accuracy.

However, a critical adversarial autopsy reveals two fatal vulnerabilities in prior art:
1. **Zero Placebo Controls:** Anchor C1 swapped full multi-dimensional activation blocks without evaluating whether injecting random Gaussian noise or scrambled spatial patches reproduces the output change via destructive disruption.
2. **Synthetic Grid Confinement:** Anchor C1 proved the swap exclusively on artificial 28×28 geometric grids with prominent horizontal partition lines and non-ordinal symbol tags (`&`, `$`, `#`, `@`). They evaluated natural images (MS-COCO) *only observationally for hallucination*, **never running the causal activation swap on natural photographic instances**.

### The Research Question
> **Do the localized residual-stream activation swaps that transfer object-attribute binding in synthetic grid scenes represent genuine, relation-specific binding representations that transfer to natural photographic instances under strict placebo controls, or are they destructive perturbation artifacts induced by artificial geometric scaffolding?**

---

## 2. Competing Hypotheses & Falsifiable Signatures

* **Hypothesis $H_1$ (Genuine Localized Binding Subspace):**  
  The intermediate residual-stream hidden states of visual patch tokens encode a localized, modular object-attribute binding representation. When swapped between two real-world photographic instances of the same semantic class, the recipient object's generated attribute text flips to the source attribute while preserving non-target scene descriptions and linguistic fluency.  
  *Observable Signature:* On natural images from `InstaBind-Lite/DSCAM`, the Net Directed Flip Rate significantly exceeds the maximum placebo flip rate ($\text{NetFlip}_{\text{swap}} - \text{NetFlip}_{\text{placebo}} > 0.30, p < 0.001$) while non-target object attribute preservation remains $> 70\%$.

* **Hypothesis $H_0$ (Synthetic Cue Artifact / Destructive Disruption):**  
  The "Binding ID" is not a general visual mechanism. In natural cluttered scenes without grid lines, binding is resolved via distributed attention or serial spatial routines. Swapping activations on natural images either:
  1. Produces identical output flips under norm-matched Gaussian noise (proving it is a non-specific disruption that triggers default prior generation), or
  2. Completely collapses linguistic generation into repetitive token degeneration.  
  *Observable Signature:* On natural images, $\text{NetFlip}_{\text{swap}} \approx \text{NetFlip}_{\text{placebo}}$, or generation perplexity collapses ($> 50\%$ repetitive n-grams).

---

## 3. Scientific Gap & Boundary Conditions

| What Prior Work Established | What Prior Work Did NOT Establish (The Live Gap) |
| :--- | :--- |
| *Grounding IDs (C1)* (`arXiv:2509.24072`) proved activation swapping works on synthetic $2 \times 4$ grid scenes. | Omitted random-vector placebos; never executed activation swapping on natural photographic images. |
| *In-Context Binding (C2)* (`arXiv:2505.22200`) showed vector addition steers binding in Blender 3D shapes. | Tested a single architecture (LLaVA-1.5); restricted strictly to toy geometric shapes on plain backgrounds. |
| *DSCAM* (`arXiv:2608.16805`) quantified that 80.7% of misbinding in natural images occurs between adjacent instances. | Purely observational benchmark; executed zero internal activation patching or mechanistic interventions. |
| *Dual Mechanisms* (`arXiv:2603.22278`) proved that spatial signals diffuse across background tokens in natural scenes. | Evaluated global linear probes; did not isolate a localized patch-swapping mechanism. |

---

## 4. Complete Experimental Factorial Protocol

The protocol evaluates 50 test items: 25 synthetic grid scenes (rebuilt from Anchor C1 specifications) and 25 natural photographic pairs from `InstaBind-Lite/DSCAM` (containing dense instances of same-class objects, e.g., two cars or two people with distinct colors/attributes).

```
                 INTERVENTION: Residual Stream Overwrite at Layer L (L = 22)
                                              │
      ┌───────────────────────┬───────────────┴───────────────┬───────────────────────┐
      ▼                       ▼                               ▼                       ▼
 [Arm 1: Real Swap]      [Arm 2: Gaussian Placebo]       [Arm 3: Background Placebo] [Arm 4: Intra-Scene Swap]
 Source Object Patches   Norm-Matched Random             Irrelevant Background       Swapping Object 1 and
 Patched into Target     Gaussian Noise Vector           Source Patches Patched      Object 2 within Same
 Bounding Box Region     Overwriting Target Box          into Target Bounding Box    Recipient Image
```

### Intervention Specifications
1. **Bounding Box Mapping:** Map pixel bounding box coordinates $(x_{\min}, y_{\min}, x_{\max}, y_{\max})$ to discrete 1D visual token indices in `Qwen2.5-VL` by calculating spatial ViT patches ($14 \times 14$), applying $2 \times 2$ spatial merge offsets, and adding a 1-token spatial dilation boundary.
2. **Spatial Bilinear Interpolation:** If source and target object bounding boxes have different patch grid dimensions $(H_1 \times W_1 \ne H_2 \times W_2)$, apply spatial bilinear interpolation to the activation tensor before residual overwriting.
3. **Residual Stream Hook:** Intercept the residual stream at Layer 22 (`model.model.language_model.layers[22]`):
   $$h_{L=22}^{\text{patched}}[i] = h_{L=22}^{\text{target}}[i] + \left( \text{Interp}(h_{L=22}^{\text{source}})[\pi(i)] - h_{L=22}^{\text{target}}[i] \right), \quad \forall i \in \mathcal{T}_{\text{target}}$$
4. **Arm 2 (Gaussian Placebo):** Overwrite the target token region with $h_{\text{placebo}} \sim \mathcal{N}(0, \sigma^2 \mathbf{I})$ scaled such that $\|h_{\text{placebo}}\|_2 = \|h_{\text{source}}\|_2$. Tests whether non-specific corruption triggers the flip.
5. **Arm 3 (Background Placebo):** Overwrite target tokens with activations extracted from an empty background quadrant of the source image. Tests whether raw image feature presence mimics the swap.
6. **Arm 4 (Intra-Scene Swap):** Swap Object 1 and Object 2 within the same image to verify relational selectivity.

---

## 5. Mathematical Metrics & Evaluation Formulations

### 1. Net Directed Target Flip Rate ($\text{NetFlip}$)
Measure the proportion of generations where the target object's predicted attribute flips to the source attribute, penalizing non-target attribute corruption:
$$\text{NetFlip} = \text{Flip}_{\text{target}} - \text{Flip}_{\text{non-target}}$$
Where:
- $\text{Flip}_{\text{target}} = 1$ if generated text matches the swapped source attribute.
- $\text{Flip}_{\text{non-target}} = 1$ if the non-target object in the scene incorrectly flips or hallucinates.

### 2. Linguistic Coherence & Degeneration Score ($\mathcal{D}_{\text{ling}}$)
Quantify whether the activation swap damages the language backbone using 3-gram repetition frequency and language model perplexity:
$$\mathcal{D}_{\text{rep}} = 1 - \frac{\text{Unique 3-grams}}{\text{Total 3-grams}}$$
If $\mathcal{D}_{\text{rep}} > 0.40$, the intervention is classified as a *destructive perturbation failure*.

### 3. Covariate Reduction Model
Fit a logistic regression predicting swap success from low-level covariates:
$$\text{Logit}(\text{Success}) = \beta_0 + \beta_1 \Delta_{\text{color}} + \beta_2 \Delta_{\text{patch\_dist}} + \beta_3 \text{Prior}_{\text{unigram}} + \beta_4 \mathbf{1}_{\text{RealSwap}}$$
If $\beta_4$ is statistically non-significant ($p > 0.05$), the binding swap reduces entirely to color histogram margin or spatial proximity.

---

## 6. Execution Architecture & Engineering Blueprint

* **Primary Model:** `Qwen/Qwen2.5-VL-3B-Instruct` (open, native ViT, sequence length manageable).
* **Secondary Model:** `google/gemma-3-4b-it` (SigLIP vision tower, for cross-architecture verification).
* **Environment:** PyTorch 2.4+, Hugging Face Transformers, `torchvision.transforms.functional.interpolate`.
* **Hardware Footprint:** Single GPU (16GB VRAM, e.g., T4/V100/L4).
* **Engineering Precaution:** Dynamic resolution in Qwen2.5-VL dynamically changes token sequence length per image. Images must be passed through a strict `max_pixels = 512 * 512` resize filter to prevent CUDA shape assertion mismatches during activation injection.

---

## 7. Decisive Kill Tests & Scientific Utility

* **Kill Condition K4 (Placebo Failure):** If Gaussian noise (Arm 2) or background patches (Arm 3) produce a target flip rate statistically indistinguishable from the real swap (Arm 1), kill the proposal. The "Binding ID" is a destructive perturbation artifact.
* **Kill Condition K5 (Natural Image Collapse):** If the Net Directed Flip Rate on natural images falls to $\le 0.10$ or triggers linguistic degeneration ($\mathcal{D}_{\text{rep}} > 0.40$), kill the universality claim. Binding IDs are toy-domain artifacts of synthetic geometric grids.
* **Why the Negative Result is High-Value:**  
  Publishable in ICML/CVPR as a landmark corrective paper: *"Mechanistic Fragility of Multimodal Binding: Latent Binding IDs Fail Beyond Synthetic Geometric Grids."* It provides empirical boundary conditions on synthetic mechanistic interpretability, proving that models resolve real-world binding through dynamic distributed attention rather than modular residual vectors.
