# Canonical Research Proposal: Proposal 1 (Field A Refined)

**Project Title:** Decomposing Multimodal Reasoning Trace Degradation: Causal Reasoning vs. Positional and Attention Dilution Artifacts  
**Domain:** Multimodal Reasoning & Mechanistic Interpretability in Vision-Language Models (VLMs)  
**Primary Anchor Literature:** 
- *RH-Bench: More Thinking, Less Seeing?* (NeurIPS 2025, `arXiv:2505.21523`)
- *Seeing or Knowing? Visual Context Sensitivity in MLLMs* (`arXiv:2607.26326`)
- *VIG: Visual Information Gain as Reward Signal for MLLM CoT Compression* (`arXiv:2608.21883`)
- *Remember-R1: Mitigating Long-Context Visual Forgetting in MLLM CoT* (`arXiv:2608.01314`)
**Document Type:** Standalone Canonical Research Specification & Execution Protocol  
**Version:** 1.0 (Post-RH-Bench Pre-emption & Causal Refinement)

---

## 1. Executive Summary & Problem Formulation

Recent 2025–2026 literature (*RH-Bench*, *Remember-R1*, *VIG*) observes that as vision-language models generate longer chains-of-thought ($T_{\text{CoT}} > 200$ tokens), their attention to visual tokens decreases, and visual hallucination increases. 

However, existing literature treats trace length as an **endogenous, correlational variable** confounded by:
1. **Absolute Sequence Position (RoPE Decay):** As reasoning unfolds, the answer token moves further away from the visual tokens. Rotary Position Embeddings naturally attenuate attention between distant tokens.
2. **Context Length Expansion (Softmax Denominator Dilution):** In self-attention, the softmax denominator sums across all $N$ tokens. An invariant visual block of $M$ tokens mathematically receives a uniform probability share of $M/N$. As $N$ grows, raw attention mass must decay even if visual information processing is unaffected.
3. **Information Availability vs. Utilization:** Whether visual features actually decay in internal hidden states or remain linearly decodable while output heads merely fail to route them.

### The Research Question
> **When visual evidence utilization declines during extended multimodal reasoning, is the degradation causally driven by the cognitive computation of the reasoning trace, or is it a measurement artifact of Rotary Position Embedding (RoPE) distance and uniform softmax denominator dilution?**

---

## 2. Competing Hypotheses & Falsifiable Signatures

* **Hypothesis $H_1$ (Cognitive Autoregressive Drift / True Forgetting):**  
  Generating intermediate deductive reasoning tokens actively drives the language model's hidden states toward linguistic attractors, overriding and discarding visual evidence representations beyond what is explained by token distance or context growth.  
  *Observable Signature:* Under teacher-forced prefix slicing, inserting 150 reasoning tokens causes a significantly larger decline in the counterfactual Image Causal Effect (ICE) and visual attention mass than inserting 150 neutral non-reasoning tokens at the exact same sequence index ($\Delta_{\text{reasoning}} \gg \Delta_{\text{neutral}}, p < 0.001$).

* **Hypothesis $H_0$ (Positional & Softmax Measurement Artifact):**  
  Visual tokens are not "forgotten" because of reasoning computation. The decline in attention mass tracks the theoretical $M/N$ uniform dilution curve, and inserting neutral non-reasoning text produces an identical degradation. Visual evidence remains linearly decodable in intermediate residual streams throughout the entire sequence.  
  *Observable Signature:* Equivalence bounds (TOST within $\theta = \pm 0.05$) confirm that a 150-token neutral filler prefix produces an indistinguishable drop from a 150-token reasoning prefix, and visual attribute decodability remains $> 75\%$ AUC.

---

## 3. Scientific Gap & Boundary Conditions

| What Prior Work Established | What Prior Work Did NOT Establish (The Live Gap) |
| :--- | :--- |
| *RH-Bench* (`arXiv:2505.21523`) showed longer traces correlate with more hallucination using budget forcing and latent steering. | Did not isolate reasoning content from token position; did not compare against neutral padding; did not test softmax dilution null. |
| *Remember-R1* (`arXiv:2608.01314`) used RL rewards to slow down attention mass $\Omega(t)$ decay. | Treated raw attention mass as a ground-truth proxy for evidence utilization; did not control for token distance. |
| *Seeing or Knowing?* (`arXiv:2607.26326`) proved visual evidence is preserved in final-layer image tokens on single-turn VQA. | Evaluated only single-turn prompts without any multi-step chain-of-thought reasoning traces. |

---

## 4. Complete 4-Arm Experimental Factorial Design

To eliminate sample difficulty and length endogeneity, all experiments use **teacher-forced prefix slicing** across 500 paired counterfactual samples from `WhatIfVis` (where an image edit flips the ground truth):

```
                        INPUT: Multimodal Stimulus (Image + Question)
                                              │
      ┌───────────────────────┬───────────────┴───────────────┬───────────────────────┐
      ▼                       ▼                               ▼                       ▼
 [Condition 1]           [Condition 2]                   [Condition 3]           [Condition 4]
 Direct Answer           Long Reasoning Prefix           Long Neutral Padding    Pos-Matched Short
 Zero Reasoning          Teacher-Forced 150 Tokens       Teacher-Forced 150      150 Tokens Prepended
 (T ≈ 10 tokens)         Deductive Steps                 Non-Reasoning Text      BEFORE Visual Tokens
```

### Protocol Specifications
1. **Condition 1 (Direct Short):** Prompt + Question $\to$ Model generates answer immediately. Establishes baseline zero-length accuracy and evidence sensitivity.
2. **Condition 2 (Long Reasoning Prefix):** Prompt + Question + 150 tokens of verified, teacher-forced deductive reasoning trace $\to$ Model predicts final answer token.
3. **Condition 3 (Long Neutral Padding - Softmax Control):** Prompt + Question + 150 tokens of neutral descriptive text (e.g., encyclopedia passage matched for perplexity and token frequency) $\to$ Model predicts final answer token. Isolates sequence length and attention denominator expansion from reasoning computation.
4. **Condition 4 (Position-Matched Short - RoPE Control):** 150 tokens of neutral text prepended *before* the prompt and image, advancing the absolute RoPE sequence index of the image and answer by 150 positions, followed immediately by direct answer prediction. Isolates absolute token coordinate displacement.

---

## 5. Mathematical Metrics & Evaluation Formulations

### 1. Counterfactual Image Causal Effect (ICE)
At the final answer token $t$, measure the log-odds shift between visually grounded answer $a_{\text{vis}}$ and language-prior answer $a_{\text{prior}}$ across paired clean ($I$) and counterfactual ($I'$) images:
$$\text{ICE}_t = \left[ \log \frac{p(a_{\text{vis}} \mid I, q, p_{<t})}{p(a_{\text{prior}} \mid I, q, p_{<t})} \right] - \left[ \log \frac{p(a_{\text{vis}} \mid I', q, p_{<t})}{p(a_{\text{prior}} \mid I', q, p_{<t})} \right]$$

### 2. Softmax-Dilution Deviation ($\Delta \text{VIG}_{\text{dev}}$)
Benchmark cross-attention mass against the theoretical uniform distribution null. For a sequence of length $N$ containing $M$ visual patch tokens:
$$\text{Uniform Null} = \frac{M}{N}$$
$$\Delta \text{VIG}_{\text{dev}} = \text{AttnMass}(\text{visual tokens}) - \frac{M}{N}$$
If $\Delta \text{VIG}_{\text{dev}} \approx 0$, visual attention decline is entirely explained by softmax denominator expansion.

### 3. Residual Stream Decodability (Availability Probe)
Train a 5-fold cross-validated linear probe on intermediate residual-stream hidden states $h_L$ at Layer 18 and Layer 30 to predict the visual attribute (e.g., color or count) across all conditions:
$$\Delta \text{AUC} = \text{AUC}_{\text{probe}} - 0.5$$

---

## 6. Execution Architecture & Engineering Blueprint

* **Primary Model:** `Qwen/Qwen2.5-VL-3B-Instruct` (and `7B-Instruct` for scaling checks).
* **Environment:** Python 3.11+, PyTorch 2.4+, Hugging Face Transformers (`attn_implementation="eager"`).
* **Hardware Footprint:** Single GPU (16GB VRAM, e.g., T4/V100/L4).
* **VRAM Safety:** Do NOT store raw $36 \times 16 \times N \times N$ attention tensors. Compute running attention sums across visual token slice indices `[vis_start : vis_end]` on the fly during the forward pass. Peak VRAM: $< 11.5\text{ GB}$.

---

## 7. Decisive Kill Tests & Scientific Utility

* **Kill Condition K1 (Position Collapse):** If Condition 2 (reasoning) and Condition 4 (position-matched) show statistically equivalent ICE drops (TOST $p < 0.05$ with margin $\theta = 0.05$), kill the "reasoning degradation" claim. The effect is 100% RoPE positional attenuation.
* **Kill Condition K2 (Dilution Collapse):** If $\Delta \text{VIG}_{\text{dev}}$ slope is zero across sequence length, kill the "cognitive forgetting" claim. The effect is a mathematical property of softmax normalization.
* **Why the Negative Result is High-Value:**  
  Publishable in NeurIPS/ICLR as a definitive rebuttal: *"Visual Forgetting in Multimodal Reasoning is an Artifact of Sequence Dilution and Positional Encoding, Not Cognitive Decay."* It stops researchers from designing unnecessary RL loss functions to prevent a non-existent cognitive failure.
