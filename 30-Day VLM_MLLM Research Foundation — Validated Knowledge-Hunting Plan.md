
# 30-Day VLM/MLLM Research Foundation — Validated Knowledge-Hunting Plan

**Principal Researcher:** Mohammad Zahed Hossen
**Locked Thesis Topic:** Causal Conflict Verbalization and Source Arbitration in Vision-Language Models
**Reference Model:** `Qwen/Qwen2.5-VL-3B-Instruct`
**Primary Benchmark:** `vlm-modality-research/modality-conflict-arbitration-v2` ($N = 1,619$ Clean Pairs)
**Evaluated Codebase:** [`production_experiment_harness_v3.py`](file:///d:/Thesis/Important/Cross%20Modal/Finalize%20Topic/Pilot/production_experiment_harness_v3.py), [`statistical_analysis.py`](file:///d:/Thesis/Important/Cross%20Modal/Finalize%20Topic/Pilot/statistical_analysis.py), [`CANONICAL_THESIS_MASTER_REPORT.md`](file:///d:/Thesis/Important/Cross%20Modal/Finalize%20Topic/CANONICAL_THESIS_MASTER_REPORT.md), [`Chapter_1_Introduction.md`](file:///d:/Thesis/Important/Cross%20Modal/Thesis_Manuscript/Chapter_1_Introduction.md), [`Chapter_3_Methodology.md`](file:///d:/Thesis/Important/Cross%20Modal/Thesis_Manuscript/Chapter_3_Methodology.md)

---

## 1. Executive Audit

### Is the Original 30-Day Plan Sound?

**Verdict:** **Flawed in premise, mismatched in scope, and dangerously oblivious to the primary literature of your thesis.**

While the original draft in [`Knowledge/30-Day VLM_MLLM Research Foundation.md`](file:///d:/Thesis/Important/Cross%20Modal/Knowledge/30-Day%20VLM_MLLM%20Research%20Foundation.md) correctly identified the need to avoid giant generic LLM courses, it committed four fatal structural errors when audited against your actual codebase:

1. **Pedagogical Condescension vs. Codebase Reality:**
   The draft assigned days to "run basic inference tests (Test A, B, C, D)" and "learn what generation parameters mean" as if you were beginning from scratch. In reality, you have **already engineered and completed** a full-population census of $N = 1,619$ items across 5 arms using batched FP16 inference, left-padding masks, dynamic token budgeting, and custom CUDA 13 monkey-patching in [`production_experiment_harness_v3.py`](file:///d:/Thesis/Important/Cross%20Modal/Finalize%20Topic/Pilot/production_experiment_harness_v3.py). Spending days running toy prompts wastes your preparation runway.
2. **Total Omission of Primary Anchor Literature:**The draft completely omitted the seminal papers upon which your thesis, dataset, and methodology are directly founded:
   * *Which Source Wins? Task-Dependent Reliance in Vision-Language Models* (Ghosh et al., 2026, [arXiv:2608.17205](https://arxiv.org/abs/2608.17205)) — the direct creators of your primary benchmark `modality-conflict-arbitration-v2`!
   * *CLASH: A Benchmark for Cross-Modal Contradiction Detection* (Popordanoska et al., 2025, [arXiv:2511.19199](https://arxiv.org/abs/2511.19199)).
   * *Mixed Signals: Decoding VLMs' Reasoning and Underlying Bias in Vision-Language Conflict* (Pezeshkpour et al., EMNLP Findings 2025).
   * *Source-Modality Monitoring in Vision-Language Models* (Hua et al., 2026, [arXiv:2604.22038](https://arxiv.org/abs/2604.22038)).
   * *Words or Vision: Do VLMs Have Blind Faith in Text?* (Deng et al., CVPR 2025).
3. **Archaic Architectural Detours:**
   Spending separate days on Flamingo (2022) and BLIP-2 (2023) is historical trivia for your model. Qwen2.5-VL does not use a Perceiver Resampler or a Q-Former; it uses a native dynamic-resolution ViT, 2D/3D spatial patch merging, and Multimodal Rotary Position Embeddings (MRoPE) projecting directly into a unified decoder-only LLM.
4. **Superficial Statistical Treatment:**
   The draft treated McNemar's test as a generic formula rather than addressing the core statistical machinery in [`statistical_analysis.py`](file:///d:/Thesis/Important/Cross%20Modal/Finalize%20Topic/Pilot/statistical_analysis.py): discordant pairs ($b=1057, c=25$), paired odds ratio ($42.28$) vs. marginal odds ratio ($24.57$), Edwards' continuity correction, Cohen's $h$, and $4 \times 4$ Markovian state migration modeling.

---

### Audit Decisions: Topic-by-Topic Validation


| Topic in Draft                                   |      Decision      | Why                                                                                                                        | Evidence from Code/Thesis                                                                            | Required Depth                                                                                        |
| :------------------------------------------------- | :------------------: | :--------------------------------------------------------------------------------------------------------------------------- | :----------------------------------------------------------------------------------------------------- | :------------------------------------------------------------------------------------------------------ |
| **Attention Is All You Need**                    |     **REDUCE**     | You already know basic Transformers. Don't spend a day on standard self-attention equations.                               | Code uses SDPA and pretrained Hugging Face classes.                                                  | Technical intuition of causal masking & autoregression.                                               |
| **Autoregressive Decoding & Logits**             |     **EXPAND**     | Generation hyperparameters in your code (`do_sample=False`, `max_new_tokens`) directly dictate determinism and truncation. | `max_tokens_direct=80`, `max_tokens_verbalize=200`, `max_tokens_prefill=20` in harness.              | Technical + Implementation: understand logits, greedy argmax, EOS stop criteria, and KV-cache reuse.  |
| **LLM Training Pipeline**                        |     **REDUCE**     | You are doing inference-first research on frozen weights. RLHF/PPO training details are irrelevant.                        | Hardware constraint: local AMD APU + Colab T4. Zero pretraining.                                     | Intuitive distinction between base models, SFT, and instruction-following alignment.                  |
| **CLIP**                                         |     **REDUCE**     | Foundational for contrastive dual-encoders, but Qwen2.5-VL is an autoregressive generative VLM.                            | Contrastive cosine similarity is not used in generation.                                             | Understand visual-text embedding spaces and why contrastive encoders differ from generative decoders. |
| **Flamingo & BLIP-2**                            | **REMOVE / MERGE** | Perceiver resamplers and Q-Formers are architectural dead ends for modern native ViT VLMs like Qwen2.5-VL.                 | Qwen2.5-VL uses dynamic ViT + patch merge + linear projector, not a cross-attention Q-Former.        | High-level 30-minute historical contrast only.                                                        |
| **LLaVA & Visual Instruction Tuning**            |      **KEEP**      | The foundational paper for projection-based visual tokens entering an autoregressive LLM.                                  | Qwen2.5-VL builds upon the visual instruction tuning paradigm.                                       | Technical: patch projection into word embedding space.                                                |
| **Qwen-VL → Qwen2-VL Evolution**                |     **EXPAND**     | Crucial to understand why static 224x224 patches failed and how native dynamic resolution was solved.                      | Harness sets`min_pixels=100352`, `max_pixels=200704`.                                                | Technical: 2D spatial grid tokens (`image_grid_thw`).                                                 |
| **Qwen2.5-VL Architecture**                      |     **EXPAND**     | Your thesis model. You must understand window attention, MRoPE, and dynamic patch tokenization.                            | Target model in all scripts. JIT patch intercepts`image_grid_thw.prod(-1)`.                          | **Implement & Defend:** explain every step from pixel matrix to decoder attention.                    |
| **Toy Inference Testing (Day 11)**               |     **REMOVE**     | You have already completed a 1,619-sample census. Toy testing is obsolete.                                                 | `production_experiment_harness_v3.py` executed on Colab.                                             | Replaced by**Codebase & Harness Architectural Audit**.                                                |
| **Multimodal Information Flow**                  |     **EXPAND**     | Where do image tokens sit relative to prompt text tokens? How does token position affect attention?                        | Text recency in Arm 1 (85.5% text) vs. visual capture in Arm 2 (89.5% image).                        | Causal understanding of attention competition and position bias.                                      |
| **Generic Hallucination (HallusionBench, POPE)** |     **REDUCE**     | Your thesis is NOT object hallucination; it is**modality conflict arbitration under contradiction**.                       | Benchmark is arithmetic GSM8K/SVAMP, not COCO object presence.                                       | Conceptual contrast between perceptual hallucination and cross-modal semantic contradiction.          |
| **Modality Conflict Literature**                 | **ADD (CRITICAL)** | *Which Source Wins?* (2026), *Mixed Signals* (2025), *CLASH* (2025), *Source Monitoring* (2026).                           | Direct foundation of your benchmark and thesis claims.                                               | **Defend Experimentally:** master findings, gaps, and metrics of these anchor papers.                 |
| **CoT Prompting & Faithfulness**                 |     **EXPAND**     | Lanham et al. (2023), Turpin et al. (2023), Balasubramanian et al. (2025). Core question of thesis.                        | Arm 4 prefill causal probe tests if rationale steering is causally binding.                          | **Explain Mathematically & Defend:** why CoT does not guarantee faithful causal reasoning.            |
| **Causal Intervention & Placebos**               |     **EXPAND**     | Why Arm 2 (Neutral Placebo) isolates verbalization from token-budget confounding.                                          | Arm 2: 89.5% Image$\rightarrow$ Arm 3: 25.8% Image ($\Delta_{\text{arb}} = +63.74\text{ pp}$).       | **Defend Scientifically:** counterfactual reasoning, test-time compute confounding, matched controls. |
| **Paired Statistics & McNemar**                  |     **EXPAND**     | Exact mathematical derivations for discordant pairs, odds ratios, Cohen's$h$, and state transitions.                       | Script`statistical_analysis.py` computes $\chi^2 = 982.40, p = 1.20 \times 10^{-215}$.               | **Explain Mathematically:** why independent tests (Fisher/Chi-square) violate paired exchangeability. |
| **Exact-Match Validation**                       |     **EXPAND**     | Proving that arbitration shift reflects genuine mathematical execution, not categorical label drift.                       | Image exact match collapses ($35.6\% \rightarrow 11.7\%$), text surges ($4.7\% \rightarrow 35.8\%$). | Technical & Methodological: task accuracy vs. source arbitration.                                     |
| **Truncation Sensitivity Audit**                 | **ADD (CRITICAL)** | Proving that the 200-token ceiling in Arms 2 and 3 did not artificially create the visual shift.                           | Sensitivity split: non-truncated ($-65.0\text{ pp}$) vs. truncated ($-61.5\text{ pp}$).              | **Defend Experimentally:** internal validity against ceiling artifacts.                               |
| **Abstention & Selective Prediction**            |      **ADD**      | Why explicit refusal ($13.7\%$ in Arm 3) is a valid epistemic response to contradiction.                                   | Abstention regex in harness; emergence of 221 abstentions in Arm 3.                                  | Technical: risk-coverage trade-off, selective classification.                                         |

---

## 2. Codebase → Knowledge Gap Analysis


| What Your Code Already Does (Implementation)                                | What You May Understand Only Implicitly                 | The Deep Theoretical / Conceptual Knowledge Required to Defend It                                                                                                                                                                                                                                                           |
| :---------------------------------------------------------------------------- | :-------------------------------------------------------- | :---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `AutoProcessor(..., min_pixels=100352, max_pixels=200704)`                  | "It resizes images so they don't blow up VRAM."         | **Dynamic ViT Tokenization:** Qwen2.5-VL maps variable aspect-ratio images to a dynamic grid of $14 \times 14$ patches, merged into $2 \times 2$ spatial tokens ($28 \times 28$ pixels/token). Setting pixel bounds strictly controls the visual token budget ($\approx 128 \text{ to } 256$ tokens) entering the sequence. |
| `torch.Tensor.prod` monkey patch for `image_grid_thw`                       | "It fixes a Colab CUDA 13 crash."                       | **NVRTC Dynamic JIT Compilation:** PyTorch on CUDA 13 invokes NVRTC for integer tensor reductions on device. Without `libnvrtc-builtins.so`, it crashes. Understanding tensor shape tracking (`thw`: Temporal, Height, Width) in 3D-RoPE.                                                                                   |
| `processor.apply_chat_template(messages, tokenize=False)`                   | "It formats text into standard`<                        | im_start                                                                                                                                                                                                                                                                                                                    |
| `processor.tokenizer.padding_side = "left"`                                 | "A setting required for batching."                      | **Causal Decoder Batched Generation:** Autoregressive decoder models with causal attention masks MUST left-pad batch inputs so that the final prompt token aligns at the same index for all batch items, ensuring valid autoregressive continuation without mask contamination.                                             |
| `attn_implementation="sdpa"`                                                | "Makes attention fast."                                 | **Memory-Efficient & Fused Attention Kernels:** Scaled Dot-Product Attention eliminates the explicit $N \times N$ attention matrix materialization in GPU global memory, computing softmax and reduction in SRAM ($\mathcal{O}(N)$ memory vs $\mathcal{O}(N^2)$).                                                           |
| `max_tokens_direct=80`, `max_tokens_verbalize=200`, `max_tokens_prefill=20` | "Different token limits for different arms."            | **Token-Budget Confounding & Test-Time Compute:** Longer generation allows intermediate chain-of-thought calculation. Without Arm 2's 200-token neutral preamble, an Arm 1 vs Arm 3 difference is confounded by computation depth.                                                                                          |
| `extract_entities(question)` & `classify_problem_choice`                    | "Extracts keywords to see which question was answered." | **Observable Operationalization of Source Selection:** Disentangling semantic source adherence from numerical arithmetic correctness. How keyword hit margins establish source identity even when arithmetic fails.                                                                                                         |
| `mcnemar_test_2x2` with Edwards' continuity correction                      | "Runs a statistical test for p-values."                 | **Repeated-Measures Inferential Validity:** Why paired observations violate the independent-sample assumption of Pearson's $\chi^2$ and Fisher's exact tests. The mathematical foundation of discordant pairs ($b$ vs $c$) under the binomial null.                                                                         |
| Arm 4 Prefill Rationale (`make_chat_text` with assistant prefill)           | "Puts words in the model's mouth before generating."    | **Counterfactual Rationale Probing (Lanham/Turpin):** Invariant completion under contradictory prefixes ($58.6\%$ identical answers) proves that prefix assertions alone do not deterministically bind multi-step arithmetic execution.                                                                                     |
| Sensitivity split on`truncated = True`                                      | "Checks if hitting max tokens ruined the results."      | **Internal Construct Validity:** Demonstrating that the $+63.74\text{ pp}$ shift is an invariant cognitive phenomenon, not an artifact of sentence cutoffs.                                                                                                                                                                 |

---

## 3. Revised 30-Day Plan

```
                                  THE 30-DAY PROGRESSION ARCHITECTURE

  ┌──────────────────────────────────────────────────────────────────────────────────────────────────┐
  │ WEEK 1 (Days 1–7): Modern Generative VLM Architecture & Hardware Execution Engine               │
  │ • Autoregressive decoding, KV-cache, left-padding, ViT dynamic tokenization, Qwen2.5-VL, MRoPE  │
  └─────────────────────────────────┬────────────────────────────────────────────────────────────────┘
                                    ▼
  ┌──────────────────────────────────────────────────────────────────────────────────────────────────┐
  │ WEEK 2 (Days 8–14): Primary Anchor Literature: Modality Conflict & Modality Bias                │
  │ • Which Source Wins?, Mixed Signals, CLASH, Source Monitoring, Words or Vision, Detection/Resol  │
  └─────────────────────────────────┬────────────────────────────────────────────────────────────────┘
                                    ▼
  ┌──────────────────────────────────────────────────────────────────────────────────────────────────┐
  │ WEEK 3 (Days 15–21): Reasoning, Faithfulness & Causal Intervention Methodology                  │
  │ • CoT mechanisms, Lanham/Turpin unfaithfulness, matched placebos, counterfactual prefilling     │
  └─────────────────────────────────┬────────────────────────────────────────────────────────────────┘
                                    ▼
  ┌──────────────────────────────────────────────────────────────────────────────────────────────────┐
  │ WEEK 4 (Days 22–28): Paired Statistics, Evaluation Metrics & Empirical Results Audit             │
  │ • McNemar, odds ratios, Cohen's h, Markov state migration, exact-match crossover, truncation    │
  └─────────────────────────────────┬────────────────────────────────────────────────────────────────┘
                                    ▼
  ┌──────────────────────────────────────────────────────────────────────────────────────────────────┐
  │ WEEK 5 (Days 29–30): Defense Mastery, Adversarial Cross-Examination & Thesis Finalization       │
  │ • Reconstruct thesis from first principles, defend against committee attacks, freeze manuscript │
  └──────────────────────────────────────────────────────────────────────────────────────────────────┘
```

---

### Phase 1: Modern Generative VLM Architecture & Hardware Execution Engine (Days 1–7)

#### Day 1 — The Autoregressive LLM Decoder: Logits, Softmax & Greedy Decoding

* **WHAT:** The exact causal token-generation loop: input IDs $\to$ embedding lookup $\to$ decoder layers $\to$ RMSNorm $\to$ language modeling head (unembedding projection) $\to$ logits $\mathbf{z} \in \mathbb{R}^{V} \to$ greedy argmax token selection.
* **WHY:** Your experiment strictly uses `do_sample=False`, `temperature=None`, `top_p=None`. You must understand that greedy decoding makes every forward trajectory deterministic, isolating prompt intervention effects from stochastic sampling variance.
* **WHERE:**
  * Primary: *Attention Is All You Need* ([arXiv:1706.03762](https://arxiv.org/abs/1706.03762)), Section 3.1 & 3.2.
  * Secondary: Hugging Face Text Generation Strategies Guide ([Hugging Face Docs](https://huggingface.co/docs/transformers/generation_strategies)).
* **HOW DEEP:** Understand technically and be able to trace mathematically from logit vector to token ID.
* **KNOWLEDGE LAYERS:**
  * *Layer 1 (Core):* Next-token prediction, causal attention mask (lower triangular), greedy decoding vs sampling.
  * *Layer 2 (Thesis Connection):* Why determinism is required to establish causal claims in paired prompting experiments.
  * *Layer 3 (Optional Depth):* Temperature scaling mathematics: $P(w_i) = \frac{\exp(z_i / T)}{\sum_j \exp(z_j / T)}$ and top-$p$ nucleus filtering.
* **PRACTICAL / NO-AI TASK:** On paper, write out the dimensions of the tensors for a sequence of 5 tokens passing through an LLM with hidden size $d=2048$ and vocabulary size $V=151643$ (Qwen dimensions) up to the argmax operation.
* **MASTERY TEST:**
  1. What is the exact mathematical operation performed by the LM Head on the final hidden state $\mathbf{h}_L$?
  2. Why does `temperature` have no effect when `do_sample=False`?
  3. What causes generation to stop in an autoregressive loop?
* **DELIVERABLE:** A 1-page structured note: `Autoregressive_Decoding_Mechanics.md`.

---

#### Day 2 — The KV-Cache & Autoregressive Batch Generation Mechanics

* **WHAT:** Key-Value (KV) caching across Transformer layers during generation, and the absolute requirement of **left-padding** for batched causal decoding.
* **WHY:** In [`production_experiment_harness_v3.py`](file:///d:/Thesis/Important/Cross%20Modal/Finalize%20Topic/Pilot/production_experiment_harness_v3.py#L566), you explicitly configure `processor.tokenizer.padding_side = "left"`. In Arm 4, you inject assistant prefill tokens directly into the prefix. You must understand how the KV cache processes prompt prefill vs. single-token decode steps.
* **WHERE:**
  * Primary: *Fast Transformer Decoding: One Write-Head is All You Need* (Shazeer, 2019, [arXiv:1911.02150](https://arxiv.org/abs/1911.02150)).
  * Secondary: Hugging Face Padding and Truncation Guide ([Hugging Face Docs](https://huggingface.co/docs/transformers/pad_truncation)).
* **HOW DEEP:** Understand technically.
* **KNOWLEDGE LAYERS:**
  * *Layer 1 (Core):* Prefill phase ($\mathcal{O}(T^2)$) vs. decode phase ($\mathcal{O}(T)$ with KV-cache). Why past keys and values are cached.
  * *Layer 2 (Thesis Connection):* Why right-padding in batched generation causes causal decoder models to generate gibberish or attend to pad tokens, and why left-padding is mandatory.
  * *Layer 3 (Optional Depth):* Multi-Query Attention (MQA) and Grouped-Query Attention (GQA) memory bandwidth savings.
* **PRACTICAL / NO-AI TASK:** Draw two diagrams: (1) a batched generation pass with right-padding showing why the next-token position is corrupted; (2) a batched pass with left-padding showing proper alignment at the generation frontier.
* **MASTERY TEST:**
  1. During generation of token $T+1$, what are the inputs to the attention operation when the KV-cache is enabled?
  2. Why does right-padding fail during batched autoregressive generation in causal decoders?
  3. In Arm 4 prefill, does the model recalculate the prefilled assistant tokens or simply append them to the prefix KV-cache?
* **DELIVERABLE:** KV-cache and padding architecture schematic added to `VLM_Architecture_Map.md`.

---

#### Day 3 — Hardware Kernels: PyTorch SDPA, FP16 vs BF16 & Memory Scaling

* **WHAT:** Fused attention algorithms (Scaled Dot-Product Attention), numerical precision formats (FP16 vs. BF16), and memory allocation in GPU VRAM during inference.
* **WHY:** In [`production_experiment_harness_v3.py`](file:///d:/Thesis/Important/Cross%20Modal/Finalize%20Topic/Pilot/production_experiment_harness_v3.py#L128-L159), you wrote automated hardware detection that selects `torch.float16` on Turing T4 (`sm_75`) and enables `attn_implementation="sdpa"`. You must defend why this was necessary to achieve 2.5s/item without OOM crashes.
* **WHERE:**
  * Primary: *FlashAttention: Fast and Memory-Efficient Exact Attention with IO-Awareness* (Dao et al., 2022, [arXiv:2205.14135](https://arxiv.org/abs/2205.14135)), Sections 1–3.
  * Secondary: PyTorch Documentation on `torch.nn.functional.scaled_dot_product_attention` ([PyTorch Docs](https://pytorch.org/docs/stable/generated/torch.nn.functional.scaled_dot_product_attention.html)).
* **HOW DEEP:** Technical understanding of memory hierarchies (SRAM vs. HBM) and numerical range/precision differences.
* **KNOWLEDGE LAYERS:**
  * *Layer 1 (Core):* Standard attention materializes $S \times S$ attention weights in HBM. SDPA fuses softmax and reduction into SRAM in tiles.
  * *Layer 2 (Thesis Connection):* Turing T4 (`sm_75`) hardware: native FP16 Tensor Cores vs lack of native BF16 (which triggers slow software emulation). Why FP16 gave a $3\times$ speedup.
  * *Layer 3 (Optional Depth):* Exponent and mantissa bit allocations: FP32 (1+8+23), FP16 (1+5+10), BF16 (1+8+7). Dynamic range vs precision.
* **PRACTICAL / NO-AI TASK:** Calculate the memory required to store the weights of a 3B parameter model in FP32, FP16, and 4-bit quantization. Show why a 3B model in FP16 easily fits inside a 16 GB T4 GPU.
* **MASTERY TEST:**
  1. Why does PyTorch SDPA reduce peak memory during long-context generation?
  2. What is the fundamental hardware difference between an NVIDIA T4 (Turing, `sm_75`) and an A100 (Ampere, `sm_80`) regarding bfloat16 support?
  3. If your batch size is 8 and prompt length is 500 tokens, why does memory consumption spike during the initial forward pass compared to single-token decoding?
* **DELIVERABLE:** Technical log: `GPU_Inference_Optimization_Notes.md`.

---

#### Day 4 — Visual Tokenization: From Pixels to Patch Embeddings

* **WHAT:** Vision Transformers (ViT), patch extraction, 2D convolutional projections, and how continuous 2D images are converted into discrete 1D token sequences.
* **WHY:** Modern VLMs do not feed pixels into an LLM. They convert image patches into vector representations that occupy the same latent dimension as text token embeddings.
* **WHERE:**
  * Primary: *An Image is Worth 16x16 Words: Transformers for Image Recognition at Scale* (Dosovitskiy et al., 2020, [arXiv:2010.11929](https://arxiv.org/abs/2010.11929)), Sections 1–3.
  * Secondary: LLaVA: *Visual Instruction Tuning* (Liu et al., 2023, [arXiv:2304.08485](https://arxiv.org/abs/2304.08485)), Section 3.
* **HOW DEEP:** Technical & Mathematical: understand patch slicing, linear projection, and sequence flattening.
* **KNOWLEDGE LAYERS:**
  * *Layer 1 (Core):* Image $X \in \mathbb{R}^{H \times W \times C} \to$ flattened patches $X_p \in \mathbb{R}^{N \times (P^2 \cdot C)} \to$ linear projection to $d$.
  * *Layer 2 (Thesis Connection):* How visual tokens enter the sequence alongside text tokens, and how the projector (linear layer or MLP) aligns vision encoder dimensions to the LLM hidden size.
  * *Layer 3 (Optional Depth):* Difference between early cross-attention bridges (Flamingo/BLIP-2) and direct sequence concatenation (LLaVA/Qwen).
* **PRACTICAL / NO-AI TASK:** Draw a $224 \times 224 \times 3$ image being divided into $14 \times 14$ patches. Calculate exactly how many patch tokens are produced ($N = (H \cdot W)/P^2 = 256$).
* **MASTERY TEST:**
  1. What is the exact mathematical formulation of the ViT linear patch projection?
  2. What is the purpose of the multimodal connector/projector between the vision encoder and LLM?
  3. In a unified decoder VLM, does the LLM "see" colors and textures, or does it attend to a sequence of vectors?
* **DELIVERABLE:** Visual tokenization diagram in `VLM_Architecture_Map.md`.

---

#### Day 5 — Native Dynamic Resolution & Spatial Patch Merging

* **WHAT:** Dynamic resolution ViTs, variable aspect-ratio handling, and spatial $2 \times 2$ patch merging into macro-tokens.
* **WHY:** In [`production_experiment_harness_v3.py`](file:///d:/Thesis/Important/Cross%20Modal/Finalize%20Topic/Pilot/production_experiment_harness_v3.py#L76-L77), you set `min_pixels = 128 * 28 * 28` ($100,352$) and `max_pixels = 256 * 28 * 28` ($200,704$). You must understand why Qwen2.5-VL uses dynamic resolution instead of fixed resizing, and how spatial pooling compresses tokens.
* **WHERE:**
  * Primary: *Qwen2-VL: To See the World More Clearly* (Wang et al., 2024, [arXiv:2409.12191](https://arxiv.org/abs/2409.12191)), Section 2.1 & 2.2.
  * Secondary: *Qwen2.5-VL Technical Report* (Bai et al., 2025, [arXiv:2502.13923](https://arxiv.org/abs/2502.13923)), Section 2.
* **HOW DEEP:** Technical & Architectural.
* **KNOWLEDGE LAYERS:**
  * *Layer 1 (Core):* Why traditional fixed-size resizing ($224 \times 224$ or $448 \times 448$) distorts text and fine typographical structures in document/math images.
  * *Layer 2 (Thesis Connection):* Qwen2.5-VL's NaViT-style dynamic resolution: dynamically slicing images into variable $H \times W$ grids without padding or warping. Spatial $2 \times 2$ merge compresses 4 adjacent $14 \times 14$ patches into a single $28 \times 28$ visual token.
  * *Layer 3 (Optional Depth):* Calculating visual token count: $N_{\text{tokens}} = \frac{H}{28} \times \frac{W}{28}$. For your bounds, token budget is strictly capped at $\approx 256$ tokens.
* **PRACTICAL / NO-AI TASK:** Calculate the exact number of visual tokens produced for an image of dimensions $560 \times 280$. Show both raw $14 \times 14$ patches and merged $28 \times 28$ tokens.
* **MASTERY TEST:**
  1. Why is dynamic resolution critical for rendered typographical problems (GSM8K/SVAMP) compared to natural photographs?
  2. What is the role of spatial patch merging in reducing computational complexity in the LLM backbone?
  3. If an image is $448 \times 448$ pixels, how many tokens enter the Qwen2.5-VL language backbone?
* **DELIVERABLE:** Analysis note: `Dynamic_Resolution_and_Token_Budgets.md`.

---

#### Day 6 — Multimodal Rotary Position Embeddings (MRoPE) & 3D Spatial-Temporal Grids

* **WHAT:** Multimodal Rotary Position Embeddings (MRoPE), decomposing positional frequencies into 3D components: temporal ($T$), height ($H$), and width ($W$).
* **WHY:** In your harness, you encountered a PyTorch CUDA 13 crash caused by `image_grid_thw.prod(-1)`. You must understand what `image_grid_thw` represents and how MRoPE provides spatial coordinate awareness to the language backbone.
* **WHERE:**
  * Primary: *Qwen2-VL Technical Report* ([arXiv:2409.12191](https://arxiv.org/abs/2409.12191)), Section 2.2 ("Multimodal Rotary Position Embedding").
  * Secondary: *RoFormer: Enhanced Transformer with Rotary Position Embedding* (Su et al., 2021, [arXiv:2104.09864](https://arxiv.org/abs/2104.09864)).
* **HOW DEEP:** Mathematical formulation of RoPE and 3D rotational coordinate splitting.
* **KNOWLEDGE LAYERS:**
  * *Layer 1 (Core):* Standard 1D RoPE rotates query and key vectors in complex 2D planes to encode relative token distances: $\mathbf{R}_{\Theta, m}^d \mathbf{x}$.
  * *Layer 2 (Thesis Connection):* MRoPE assigns three independent position IDs $(t, h, w)$ to each token. Text tokens have identical coordinates across $H$ and $W$ ($h=w=t$), while image tokens share the same temporal slice $t$ but possess unique 2D spatial coordinates $(h, w)$.
  * *Layer 3 (Optional Depth):* The CUDA 13 NVRTC bug: why `image_grid_thw.prod(-1)` (computing total tokens per image from 3D grid dimensions) triggered JIT compilation, and why CPU evaluation is mathematically identical.
* **PRACTICAL / NO-AI TASK:** Write down the 3D position tuple $(t, h, w)$ for: (1) a text token preceding an image; (2) a visual token located at row 2, column 3 of an image grid; (3) a text token following the image.
* **MASTERY TEST:**
  1. Why is 1D positional encoding insufficient for modeling spatial adjacency in 2D images?
  2. How does MRoPE allow the model to distinguish between horizontal and vertical distance between visual patches?
  3. Why does evaluating `image_grid_thw.prod(-1)` on CPU in Python avoid the CUDA 13 JIT crash without changing model predictions?
* **DELIVERABLE:** Mathematical derivation note: `MRoPE_and_3D_Position_Embeddings.md`.

---

#### Day 7 — The Full Qwen2.5-VL Architecture & Codebase Harness Walkthrough

* **WHAT:** Complete end-to-end trace of `Qwen2.5-VL-3B-Instruct`: from raw PIL image and string prompt to final generated token string.
* **WHY:** This is the capstone day of Phase 1. You must be able to walk through your actual production harness line-by-line and map every function to the underlying neural network architecture.
* **WHERE:**
  * Primary: *Qwen2.5-VL Technical Report* (Bai et al., 2025, [arXiv:2502.13923](https://arxiv.org/abs/2502.13923)).
  * Secondary: Your codebase: [`production_experiment_harness_v3.py`](file:///d:/Thesis/Important/Cross%20Modal/Finalize%20Topic/Pilot/production_experiment_harness_v3.py).
* **HOW DEEP:** **Implement & Defend:** explain every component from memory.
* **KNOWLEDGE LAYERS:**
  * *Layer 1 (Core):* 36 Transformer layers, hidden size 2048, 16 attention heads, SwiGLU activation, RMSNorm.
  * *Layer 2 (Thesis Connection):* Chat template structure (`<|im_start|>user\n<|vision_start|>...<|vision_end|>prompt<|im_end|>\n<|im_start|>assistant\n`). How image placeholders are replaced by visual tokens.
  * *Layer 3 (Optional Depth):* The 3-group generation budget architecture in your harness (Arms 4a/b: 20 tokens, Arm 1: 80 tokens, Arms 2/3: 200 tokens).
* **PRACTICAL / NO-AI TASK:** Close your code editor. On a blank sheet of paper, sketch the complete pipeline of `process_batch_v3`: prompt building $\to$ chat formatting $\to$ processor call $\to$ model.generate $\to$ decode_outputs $\to$ regex extraction $\to$ choice classification.
* **MASTERY TEST:**
  1. What happens inside `AutoProcessor` when both an image and text prompt are passed?
  2. How are the `<|vision_start|>` and `<|vision_end|>` special tokens used by the model?
  3. Why did you create three separate generation groups with different `max_new_tokens` instead of running all arms with 200 tokens?
* **DELIVERABLE:** Complete architecture blueprint: `Qwen2.5VL_Architecture_Notes.md`.

---

### Phase 2: Primary Anchor Literature: Modality Conflict & Bias (Days 8–14)

#### Day 8 — Anchor Paper 1: *Which Source Wins?* (Ghosh et al., 2026)

* **WHAT:** The foundational paper behind your benchmark: *Which Source Wins? Task-Dependent Reliance in Vision-Language Models* (Ghosh, Gupta & Wang, August 2026, [arXiv:2608.17205](https://arxiv.org/abs/2608.17205)).
* **WHY:** This is the closest prior work to your thesis. It established that multimodal reliance varies across tasks and legibility levels, but left the explicit conflict verbalization and abstention gap open in Section 6.
* **WHERE:**
  * Paper: [https://arxiv.org/abs/2608.17205](https://arxiv.org/abs/2608.17205).
  * Read: Abstract, Section 1 (Intro), Section 3 (Benchmark Construction), Section 4 (Modality Reliance Metric / CLL), Section 6 (Discussion & Limitations).
* **HOW DEEP:** **Defend Experimentally:** master the benchmark origin and articulate exactly where your thesis departs from it.
* **KNOWLEDGE LAYERS:**
  * *Layer 1 (Core):* How `modality-conflict-arbitration-v2` was constructed: pairing GSM8K and SVAMP arithmetic word problems with typographical image renderings.
  * *Layer 2 (Thesis Connection):* Ghosh et al. evaluated reliance under physical degradation (blur, noise, corruption). Your thesis restricts evaluation to **pristine clean pairs ($\lambda = 0$)** to isolate pure cognitive arbitration from perceptual failure.
  * *Layer 3 (Optional Depth):* Ghosh et al.'s Section 6 explicit limitation: *"We do not test whether models detect the contradiction, express uncertainty, or abstain."* This is your primary citation of an open research gap.
* **PRACTICAL / NO-AI TASK:** Write a 1-page comparative audit contrasting Ghosh et al.'s degradation methodology with your causal prompt intervention methodology.
* **MASTERY TEST:**
  1. How did Ghosh et al. construct the conflicting arithmetic pairs in `modality-conflict-arbitration-v2`?
  2. Why did Ghosh et al. use asymmetric image degradation (levels 1–3)?
  3. What explicit open question in Ghosh et al.'s Section 6 does your thesis directly answer?
* **DELIVERABLE:** Anchor paper breakdown in `Paper_Reading_Matrix.md`.

---

#### Day 9 — Anchor Paper 2: *CLASH* — Cross-Modal Contradiction Detection (Popordanoska et al., 2025)

* **WHAT:** *CLASH: A Benchmark for Cross-Modal Contradiction Detection* (Popordanoska, Li & Blaschko, Nov 2025, [arXiv:2511.19199](https://arxiv.org/abs/2511.19199)).
* **WHY:** CLASH formalizes cross-modal contradiction detection as an open failure mode across modern VLMs, but frames contradiction purely as a binary classification task.
* **WHERE:**
  * Paper: [https://arxiv.org/abs/2511.19199](https://arxiv.org/abs/2511.19199).
  * Read: Abstract, Section 1, Section 2 (Related Work), Section 3 (Benchmark Design), Section 5 (Model Failures).
* **HOW DEEP:** Technical & Conceptual understanding.
* **KNOWLEDGE LAYERS:**
  * *Layer 1 (Core):* The definition of cross-modal contradiction: an image and text premise that cannot simultaneously be true in the real world.
  * *Layer 2 (Thesis Connection):* Why **contradiction detection $\neq$ source arbitration**. Detecting that two sources disagree is an isolated diagnostic; deciding which source to execute or whether to abstain is an active decision process.
  * *Layer 3 (Optional Depth):* Why models overlook visual-text contradictions due to strong visual or linguistic priors.
* **PRACTICAL / NO-AI TASK:** Draw a flowchart showing the distinction between CLASH (Input $\to$ Is there contradiction? $\to$ Yes/No) and your thesis (Input $\to$ Verbalize Contradiction $\to$ Which source is executed in problem solving?).
* **MASTERY TEST:**
  1. How does the CLASH benchmark define a cross-modal contradiction?
  2. Why is high contradiction detection accuracy insufficient to guarantee that a model will solve the correct problem?
  3. How does your thesis extend beyond the CLASH paradigm?
* **DELIVERABLE:** Conceptual contrast analysis added to `VLM_Reliability_Notes.md`.

---

#### Day 10 — Anchor Paper 3: *Mixed Signals* (Pezeshkpour et al., EMNLP Findings 2025)

* **WHAT:** *Mixed Signals: Decoding VLMs' Reasoning and Underlying Bias in Vision-Language Conflict* (Pezeshkpour, Aminnaseri & Hruschka, EMNLP 2025, [ACL Anthology](https://aclanthology.org/2025.findings-emnlp.1351.pdf)).
* **WHY:** Mixed Signals directly tests prompt modifications and explicit conflict-handling instructions in VLMs. It represents your primary novelty threat and must be critically understood.
* **WHERE:**
  * Paper: [https://aclanthology.org/2025.findings-emnlp.1351.pdf](https://aclanthology.org/2025.findings-emnlp.1351.pdf).
  * Read: Abstract, Section 3 (Conflict Datasets), Section 4 (Prompting & Mitigation Strategies), Section 6 (Discussion).
* **HOW DEEP:** **Defend Experimentally:** understand why generic conflict prompting failed to show consistent improvements in Mixed Signals, and why your length-matched placebo and exact-match crossover design provide stronger causal evidence.
* **KNOWLEDGE LAYERS:**
  * *Layer 1 (Core):* How VLMs exhibit inconsistent preferences across vision-centric vs text-centric conflict tasks.
  * *Layer 2 (Thesis Connection):* Mixed Signals observed that prompt interventions often produce fragile, model-dependent results. Your thesis shows that in Qwen2.5-VL, conflict verbalization produces a massive, statistically definitive shift ($\Delta_{\text{arb}} = +63.74\text{ pp}, p = 1.20 \times 10^{-215}$).
  * *Layer 3 (Optional Depth):* Why your 4-arm design with a neutral descriptive placebo (Arm 2) controls for prompt length confounds that uncalibrated prompting studies ignore.
* **PRACTICAL / NO-AI TASK:** List the three prompt interventions tested in Mixed Signals and write a paragraph explaining why your Arm 2 (Neutral Placebo) provides a stricter control than their baselines.
* **MASTERY TEST:**
  1. What did Pezeshkpour et al. discover about the consistency of prompt-based conflict mitigation across different VLM architectures?
  2. Why is "telling the model to consider both sources" not a sufficient causal experiment without a length-matched neutral control?
  3. How do your exact-match crossover results ($35.6\%$ Img $\to 35.8\%$ Txt) strengthen the evidence compared to Mixed Signals?
* **DELIVERABLE:** Critical literature audit in `Paper_Reading_Matrix.md`.

---

#### Day 11 — Anchor Paper 4: *Source-Modality Monitoring* (Hua et al., 2026)

* **WHAT:** *Source-Modality Monitoring in Vision-Language Models* (Hua, Yun & Pavlick, April 2026, [arXiv:2604.22038](https://arxiv.org/abs/2604.22038)).
* **WHY:** Introduces the concept of "source monitoring" (borrowed from cognitive psychology) into VLMs: testing whether a model internally tracks which modality supplied a specific piece of information.
* **WHERE:**
  * Paper: [https://arxiv.org/abs/2604.22038](https://arxiv.org/abs/2604.22038).
  * Read: Abstract, Section 1, Section 3 (Source Monitoring Tasks), Section 5 (Probing & Interventions).
* **HOW DEEP:** Conceptual and Theoretical understanding.
* **KNOWLEDGE LAYERS:**
  * *Layer 1 (Core):* Source monitoring theory (Johnson et al., 1993): how cognitive agents distinguish between memories derived from vision vs reading.
  * *Layer 2 (Thesis Connection):* Hua et al. show that VLMs track source modality imperfectly and confuse sources under semantic overlap. Your thesis shows that forcing the model to explicitly evaluate source reliability breaks visual capture.
  * *Layer 3 (Optional Depth):* The distinction between passive source representation (probing) and behavioral source arbitration (downstream execution).
* **PRACTICAL / NO-AI TASK:** Write a short essay: "Why Source Monitoring is a Pre-requisite for Rational Source Arbitration in Multimodal Systems."
* **MASTERY TEST:**
  1. What is "source-modality monitoring" in a neural network?
  2. How do syntactic and semantic cues affect a VLM's ability to track where evidence came from?
  3. In your Arm 3 prompt, how does asking "which source you consider more reliable" connect directly to source monitoring?
* **DELIVERABLE:** Synthesis note in `VLM_Reliability_Notes.md`.

---

#### Day 12 — Anchor Paper 5: *Words or Vision* — Modality Dominance & Position Bias (Deng et al., CVPR 2025)

* **WHAT:** *Words or Vision: Do Vision-Language Models Have Blind Faith in Text?* (Deng et al., CVPR 2025, [CVF Open Access](https://openaccess.thecvf.com/content/CVPR2025/papers/Deng_Words_or_Vision_Do_Vision-Language_Models_Have_Blind_Faith_in_Text_CVPR_2025_paper.pdf)).
* **WHY:** Demonstrates that modality preference is heavily influenced by token ordering, prompt framing, and language priors. Crucial for understanding why Arm 1 (Direct) has an 85.5% text bias while Arm 2 (Placebo) has an 89.5% visual bias!
* **WHERE:**
  * Paper: [CVF Open Access PDF](https://openaccess.thecvf.com/content/CVPR2025/papers/Deng_Words_or_Vision_Do_Vision-Language_Models_Have_Blind_Faith_in_Text_CVPR_2025_paper.pdf).
  * Read: Abstract, Section 3 (Modality Preference Analysis), Section 4 (Token Order & Positional Bias).
* **HOW DEEP:** Technical & Empirical understanding.
* **KNOWLEDGE LAYERS:**
  * *Layer 1 (Core):* Text dominance vs visual capture. When does an autoregressive model favor the text prompt over visual tokens?
  * *Layer 2 (Thesis Connection):* **The Positional Bias Revelation:** In Arm 1, the prompt ends with the text question immediately before `Solve the problem`. Due to recency bias in causal attention, the model defaults to text ($85.5\%$). In Arm 2, the prompt asks to describe the image and text, focusing attention on the image first, triggering massive visual capture ($89.5\%$)!
  * *Layer 3 (Optional Depth):* Attention sink tokens and position decay in autoregressive Transformer attention heads.
* **PRACTICAL / NO-AI TASK:** Analyze your literal prompts for Arm 1, Arm 2, and Arm 3. Explain how the wording and sequence of instructions change the recency and salience of visual vs textual tokens.
* **MASTERY TEST:**
  1. According to Deng et al., why do VLMs often exhibit blind faith in text prompts over visual evidence?
  2. Why did your Arm 1 direct baseline result in $85.5\%$ text selection, while Arm 2 placebo resulted in $89.5\%$ image selection?
  3. How does this demonstrate that "modality preference" is not a fixed model property, but dynamically modulated by prompt structure?
* **DELIVERABLE:** Positional bias and prompt salience report: `Modality_Dominance_and_Prompt_Structure.md`.

---

#### Day 13 — Anchor Paper 6: *Challenges in Modality Conflict* (Nguyen et al., 2025)

* **WHAT:** *Challenges in Understanding Modality Conflict in Vision-Language Models* (Nguyen, Michaels, Fiterau & Jensen, Sept 2025, [arXiv:2509.02805](https://arxiv.org/abs/2509.02805)).
* **WHY:** Provides the formal theoretical separation between **conflict detection** (recognizing discrepancy) and **conflict resolution** (deciding how to act on it).
* **WHERE:**
  * Paper: [https://arxiv.org/abs/2509.02805](https://arxiv.org/abs/2509.02805).
  * Read: Abstract, Section 1, Section 3 (Separating Detection from Resolution), Section 4 (Attention Pattern Shifts).
* **HOW DEEP:** Technical and Conceptual.
* **KNOWLEDGE LAYERS:**
  * *Layer 1 (Core):* Linear probing reveals that conflict representations emerge in middle layers, but final layers often fail to resolve them correctly.
  * *Layer 2 (Thesis Connection):* Your thesis shows that explicit verbalization bridges this gap: by forcing early generation tokens to articulate the conflict, downstream generation is steered toward resolution or abstention.
  * *Layer 3 (Optional Depth):* Why synthetic shape/color conflict benchmarks fail to capture the complexity of multi-step arithmetic conflicts.
* **PRACTICAL / NO-AI TASK:** Draw a two-stage diagram showing the neural pipeline: Detection (internal hidden states) vs Resolution (autoregressive generation). Annotate where your prompt intervention operates.
* **MASTERY TEST:**
  1. What is the fundamental difference between conflict detection and conflict resolution in VLMs?
  2. At what stage of the network did Nguyen et al. find conflict detection signals using linear probes?
  3. Why does an unprompted model often detect conflict internally but still fail to resolve it in its output generation?
* **DELIVERABLE:** Detection vs Resolution framework summary in `VLM_Reliability_Notes.md`.

---

#### Day 14 — Mid-Curriculum Literature Synthesis & Epistemic Boundary Audit

* **WHAT:** Consolidating the six anchor papers into a unified related-work narrative, and establishing strict claim boundaries.
* **WHY:** You must prevent your thesis from overclaiming. You must be able to state what prior work proved, what your thesis proves, and what remains unknown.
* **WHERE:**
  * Primary: [`Chapter_1_Introduction.md`](file:///d:/Thesis/Important/Cross%20Modal/Thesis_Manuscript/Chapter_1_Introduction.md), Sections 1.2–1.6, and [`CANONICAL_THESIS_MASTER_REPORT.md`](file:///d:/Thesis/Important/Cross%20Modal/Finalize%20Topic/CANONICAL_THESIS_MASTER_REPORT.md), Section 1 & Section 8.
* **HOW DEEP:** **Defend Scientifically:** write the definitive Related Work positioning for your thesis.
* **KNOWLEDGE LAYERS:**
  * *Layer 1 (Core):* Synthesis of Ghosh (degradation reliance), Popordanoska (contradiction detection), Pezeshkpour (prompt fragility), Hua (source monitoring), Deng (position bias), Nguyen (detection vs resolution).
  * *Layer 2 (Thesis Connection):* The 5 defensible thesis contributions vs the "Do Not Write" directives in [`CANONICAL_THESIS_MASTER_REPORT.md`](file:///d:/Thesis/Important/Cross%20Modal/Finalize%20Topic/CANONICAL_THESIS_MASTER_REPORT.md#L534-L537).
  * *Layer 3 (Optional Depth):* Why behavioral prompt interventions cannot claim internal circuit rewiring or attention head rerouting.
* **PRACTICAL / NO-AI TASK:** Fill out a 6-row table: [Paper Name | Established Finding | Unanswered Gap | How My Thesis Differs].
* **MASTERY TEST:**
  1. Why is it scientifically inaccurate to say your thesis proves "internal attention heads are redirected"?
  2. What is the exact difference between Ghosh et al.'s reliance metric and your causal arbitration shift ($\Delta_{\text{arb}}$)?
  3. If a committee member asks, "Hasn't Pezeshkpour et al. already tested conflict prompts?", what is your exact rebuttal?
* **DELIVERABLE:** Master Related Work chapter synthesis: `Chapter_2_Related_Work_Synthesis.md`.

---

### Phase 3: Reasoning, Faithfulness & Causal Intervention Methodology (Days 15–21)

#### Day 15 — The Mechanism of Chain-of-Thought Prompting in Autoregressive LLMs

* **WHAT:** Intermediate reasoning tokens, scratchpad computation, and why conditioning on prior output tokens increases effective computational capacity.
* **WHY:** Arms 2 and 3 generate two-sentence rationales before producing `#### <answer>`. You must understand why generating intermediate tokens changes the probability distribution of the final answer token.
* **WHERE:**
  * Primary: *Chain-of-Thought Prompting Elicits Reasoning in Large Language Models* (Wei et al., 2022, [arXiv:2201.11903](https://arxiv.org/abs/2201.11903)).
  * Secondary: *Why think step by step of reasoning in LLMs?* (Feng et al., 2024, [arXiv:2305.15408](https://arxiv.org/abs/2305.15408)).
* **HOW DEEP:** Technical & Mathematical: understand autoregressive sequence conditioning: $P(Y \mid X) = \sum_Z P(Y \mid X, Z) P(Z \mid X)$.
* **KNOWLEDGE LAYERS:**
  * *Layer 1 (Core):* Standard direct generation forces the model to compute complex reasoning in a single forward pass through fixed depth $L$.
  * *Layer 2 (Thesis Connection):* CoT spreads computation across sequential forward passes: each generated token $z_t$ can attend to all prior reasoning tokens $z_{<t}$, effectively expanding total serial depth.
  * *Layer 3 (Optional Depth):* The computational expressive power of Transformer decoders with CoT (constant depth Transformer + polynomial scratchpad can simulate circuits).
* **PRACTICAL / NO-AI TASK:** Write out the mathematical expression for the conditional probability of the final answer $Y$ with and without intermediate reasoning tokens $Z$.
* **MASTERY TEST:**
  1. Why does a fixed-layer Transformer struggle to compute multi-step arithmetic in a single forward pass without intermediate tokens?
  2. How does generating intermediate tokens increase the effective computational depth of the model?
  3. In your experiment, does Arm 2 (Neutral Placebo) provide intermediate tokens? Why is this crucial?
* **DELIVERABLE:** Analysis report: `Reasoning_Tokens_and_Effective_Depth.md`.

---

#### Day 16 — Chain-of-Thought Unfaithfulness & Post-Hoc Rationalization

* **WHAT:** Rationale unfaithfulness: when generated reasoning traces misrepresent the true underlying features driving the decision.
* **WHY:** The core question of your thesis: does conflict verbalization causally steer source selection, or does it merely rationalize a decision the model would have made anyway?
* **WHERE:**
  * Primary: *Language Models Don't Always Say What They Think: Unfaithful Explanations in Chain-of-Thought Prompting* (Turpin et al., NeurIPS 2023, [arXiv:2305.04388](https://arxiv.org/abs/2305.04388)).
  * Secondary: *A Closer Look at Bias and Chain-of-Thought Faithfulness of Large (Vision) Language Models* (Balasubramanian et al., EMNLP Findings 2025, [ACL Anthology](https://aclanthology.org/2025.findings-emnlp.723.pdf)).
* **HOW DEEP:** **Defend Scientifically:** explain how Turpin et al. proved unfaithfulness and why post-hoc rationalization is a persistent hazard in LLMs/VLMs.
* **KNOWLEDGE LAYERS:**
  * *Layer 1 (Core):* Turpin et al. injected biased features (e.g. "Suggested answer is (A)") that heavily swayed the model's prediction, yet the model's generated CoT never mentioned the biased prompt!
  * *Layer 2 (Thesis Connection):* In VLMs, visual features can silently drive the decision while the generated text produces plausible post-hoc explanations.
  * *Layer 3 (Optional Depth):* The epistemic danger of anthropomorphizing "explanations": treating model-generated English sentences as sincere human justifications.
* **PRACTICAL / NO-AI TASK:** Write down the definition of "faithful rationale" vs "unfaithful rationale" from Turpin et al. and formulate how it applies to multimodal conflict.
* **MASTERY TEST:**
  1. What experimental intervention did Turpin et al. use to prove that language models produce unfaithful reasoning traces?
  2. How did Balasubramanian et al. demonstrate that multimodal models often fail to articulate visual biases in their CoT?
  3. If a model generates "I chose the text problem because it is clearer", how can you prove whether that statement was causal or post-hoc?
* **DELIVERABLE:** Synthesis chapter in `Reasoning_and_Faithfulness_Notes.md`.

---

#### Day 17 — Causal Rationale Interventions & Rationale Prefilling (Lanham et al., 2023)

* **WHAT:** Counterfactual rationale interventions: truncating, corrupting, or forcing prefixes into the reasoning chain to measure downstream prediction changes.
* **WHY:** This is the exact methodological origin of your **Arm 4 (Prefill Causal Probe)** in [`production_experiment_harness_v3.py`](file:///d:/Thesis/Important/Cross%20Modal/Finalize%20Topic/Pilot/production_experiment_harness_v3.py#L111-L119).
* **WHERE:**
  * Primary: *Measuring Faithfulness in Chain-of-Thought Reasoning* (Lanham et al., 2023, [arXiv:2307.13702](https://arxiv.org/abs/2307.13702)).
  * Read: Abstract, Section 2 (Faithfulness Metrics), Section 3 (Interventions: Truncation, Adding Mistakes, Paraphrasing), Section 5 (Results).
* **HOW DEEP:** **Implement & Defend:** understand how rationale prefilling tests causal conditioning in the KV cache.
* **KNOWLEDGE LAYERS:**
  * *Layer 1 (Core):* Lanham et al.'s causal test: if an intermediate step is causally necessary, altering it MUST change the final answer. If the answer remains unchanged, the step was non-causal.
  * *Layer 2 (Thesis Connection):* In your Arm 4, you prefill contradictory vs agreement prefixes into the assistant turn:
    * Arm 4a: `The image and text contradict... Following the image problem, the answer is: #### `
    * Arm 4b: `The image and text describe consistent premises. Following the text problem, the answer is: #### `
  * *Layer 3 (Optional Depth):* Your empirical finding: **$58.55\%$ of items produced identical final answers** across Arm 4a and 4b ($948 / 1,619$). Short prefix assertions without multi-step scratchpads have weak steering power!
* **PRACTICAL / NO-AI TASK:** Diagram the KV-cache state during an Arm 4 prefill pass, showing how the prefilled prefix acts as a fixed context prompt for the final answer token.
* **MASTERY TEST:**
  1. What are the three CoT intervention tests proposed by Lanham et al.?
  2. In your results, what percentage of items produced identical answers when forced with opposing rationales in Arm 4a vs Arm 4b?
  3. Why does this exploratory finding show that short prefix assertions are a weaker causal lever than full multi-step scratchpad generation?
* **DELIVERABLE:** Rationale intervention report: `Arm4_Prefill_Causal_Probing_Analysis.md`.

---

#### Day 18 — The Causal Design: Interventions, Confounders & The Length-Matched Placebo

* **WHAT:** Principles of causal inference in prompt engineering: treatment variables, confounding variables, and the role of the length-matched neutral placebo.
* **WHY:** The single most important methodological defense of your thesis. You must be able to explain why comparing Arm 1 directly to Arm 3 is a flawed experiment, and why Arm 2 is mandatory.
* **WHERE:**
  * Primary: *Causality: Models, Reasoning, and Inference* (Pearl, 2009), Chapter 1 & Chapter 3 (The `do`-calculus and back-door criterion).
  * Secondary: [`Chapter_3_Methodology.md`](file:///d:/Thesis/Important/Cross%20Modal/Thesis_Manuscript/Chapter_3_Methodology.md), Section 3.1.2.
* **HOW DEEP:** **Defend Scientifically:** master the causal DAG of your experiment.
* **KNOWLEDGE LAYERS:**
  * *Layer 1 (Core):* Confounding: when a third variable $Z$ influences both the treatment condition and the outcome, creating a spurious association.
  * *Layer 2 (Thesis Connection):* If you compare Arm 1 (Direct, 0 reasoning tokens) to Arm 3 (Conflict Verbalization, $\approx 50$ reasoning tokens), the treatment is confounded by **test-time compute depth** and **syntactic preamble structure**.
  * *Layer 3 (Optional Depth):* Arm 2 (Neutral Placebo) requires a 2-sentence descriptive preamble of equal token length without evaluative conflict phrasing. This controls for token compute, isolating the specific effect of **semantic conflict evaluation**.
* **PRACTICAL / NO-AI TASK:** Draw the causal Directed Acyclic Graph (DAG) of your experiment: Nodes = [Prompt Directive, Test-Time Compute / Token Budget, Conflict Semantic Evaluation, Observable Source Selection]. Show which back-door path Arm 2 closes.
* **MASTERY TEST:**
  1. What is the definition of a confounder in an experimental intervention?
  2. If Arm 3 had shown a shift compared to Arm 1, what alternative explanation could a skeptic raise?
  3. Exactly how does Arm 2 (Neutral Placebo) neutralize the test-time compute alternative explanation?
* **DELIVERABLE:** Causal DAG and methodological defense document: `Causal_Intervention_and_Placebo_Design.md`.

---

#### Day 19 — Disentangling Source Selection from Answer Correctness

* **WHAT:** The conceptual and empirical separation between **source arbitration** (which problem the model attempted to solve) and **task accuracy** (whether the arithmetic calculation was correct).
* **WHY:** A model can successfully arbitrate to the text problem but still calculate $24 \times 7$ incorrectly. Conflating accuracy with source selection leads to false conclusions.
* **WHERE:**
  * Primary: [`Chapter_3_Methodology.md`](file:///d:/Thesis/Important/Cross%20Modal/Thesis_Manuscript/Chapter_3_Methodology.md), Section 3.5.
  * Secondary: [`CANONICAL_THESIS_MASTER_REPORT.md`](file:///d:/Thesis/Important/Cross%20Modal/Finalize%20Topic/CANONICAL_THESIS_MASTER_REPORT.md), Section 6.
* **HOW DEEP:** Technical & Methodological.
* **KNOWLEDGE LAYERS:**
  * *Layer 1 (Core):* Dual-track classification: Track 1 = Semantic entity extraction and problem choice (`follows_image`, `follows_text`, `abstains`); Track 2 = Deterministic ground truth exact-match (`exact_img`, `exact_txt`).
  * *Layer 2 (Thesis Connection):* In Arm 3, the model selects the text source in $58.9\%$ of items ($954 / 1,619$), but only achieves exact match on the text answer in $35.8\%$ ($579 / 1,619$). Why? Because GSM8K is hard; the model makes arithmetic calculation errors even after selecting the correct source!
  * *Layer 3 (Optional Depth):* Why entity-based classification correctly captures source intent when arithmetic fails.
* **PRACTICAL / NO-AI TASK:** Trace Item `gsm8k_pair_442`: Image Question, Text Question, Model Generated Scratchpad, Final Extracted Answer. Determine its source classification vs its exact-match status.
* **MASTERY TEST:**
  1. Why is `follows_text_problem` not identical to `exact_txt == True`?
  2. If a model exhibits $35.8\%$ exact match on the text problem in Arm 3, does that mean it failed to arbitrate in the other $64.2\%$ of cases?
  3. How does the entity extraction algorithm in your code prevent keyword noise when classifying source intent?
* **DELIVERABLE:** Metric formalization report: `Source_Selection_vs_Task_Accuracy.md`.

---

#### Day 20 — Contradiction-Conditioned Abstention & Selective Classification

* **WHAT:** Selective prediction, abstention mechanisms, and why explicit refusal is an optimal epistemic response to mutually contradictory premises.
* **WHY:** In Arm 3, the model refused to solve the problem and explicitly abstained in **$13.65\%$ of items ($221 / 1,619$)**, compared to $0.2\%$ ($4 / 1,619$) in Arm 2.
* **WHERE:**
  * Primary: *Selective Classification for Deep Neural Networks* (Geifman & El-Yaniv, NeurIPS 2017, [arXiv:1705.08500](https://arxiv.org/abs/1705.08500)).
  * Secondary: *Look Again Before You Abstain: Regulating Abstention in VLMs* (2024, in your `Paper/` directory).
* **HOW DEEP:** Technical & Conceptual understanding.
* **KNOWLEDGE LAYERS:**
  * *Layer 1 (Core):* Selective classification: allowing a model to output a reject option $\perp$ when confidence is low or inputs are unresolvable, improving precision on the covered subset.
  * *Layer 2 (Thesis Connection):* In your harness, [`detect_abstention`](file:///d:/Thesis/Important/Cross%20Modal/Finalize%20Topic/Pilot/production_experiment_harness_v3.py#L174-L184) uses deterministic regex patterns (`cannot be determined`, `different problems, so there is no`, etc.).
  * *Layer 3 (Optional Depth):* Why naive benchmark parsers misclassify abstentions as "parse failures" ($0\%$ accuracy), masking genuine epistemic competence.
* **PRACTICAL / NO-AI TASK:** Review 5 generated texts from `full_experiment_results v3.0.json` that were classified as `abstains`. Confirm that each generation represents genuine refusal to arbitrate contradictory premises.
* **MASTERY TEST:**
  1. What is the risk-coverage trade-off in selective classification?
  2. Why did Arm 3 exhibit a $68\times$ increase in abstention compared to Arm 2 ($13.7\%$ vs $0.2\%$)?
  3. Why should abstention be treated as a distinct behavioral category rather than lumped into "ambiguous" or "incorrect"?
* **DELIVERABLE:** Epistemic abstention chapter in `VLM_Reliability_Notes.md`.

---

#### Day 21 — Token Truncation & Internal Validity Sensitivity Protocol

* **WHAT:** Ceiling effects, max generation length boundaries, and operational sensitivity splitting.
* **WHY:** In your full run, $37.6\%$ of Arm 2 and $44.2\%$ of Arm 3 reached the 200-token ceiling (`tokens >= max_new_tokens - 1`). You must prove to your defense committee that truncation did NOT create the observed shift.
* **WHERE:**
  * Primary: [`CANONICAL_THESIS_MASTER_REPORT.md`](file:///d:/Thesis/Important/Cross%20Modal/Finalize%20Topic/CANONICAL_THESIS_MASTER_REPORT.md), Section 4 ("Truncation Sensitivity & Robustness Analysis").
  * Secondary: [`production_experiment_harness_v3.py`](file:///d:/Thesis/Important/Cross%20Modal/Finalize%20Topic/Pilot/production_experiment_harness_v3.py#L428-L452).
* **HOW DEEP:** **Defend Scientifically:** present the sensitivity split numbers from memory.
* **KNOWLEDGE LAYERS:**
  * *Layer 1 (Core):* Token budgets: why multi-step arithmetic CoT requires substantial token lengths.
  * *Layer 2 (Thesis Connection):* The Sensitivity Proof:
    * Full Population ($N=1619$): Net shift $\Delta = -63.7\text{ pp}$ ($89.5\% \to 25.8\%$).
    * Strict Paired Non-Truncated ($N=632$): Net shift $\Delta = -59.8\text{ pp}$ ($85.1\% \to 25.3\%$).
    * Arm-Specific Non-Truncated ($N=1011$ A2, $N=903$ A3): Net shift $\Delta = -65.0\text{ pp}$ ($86.6\% \to 21.6\%$).
  * *Layer 3 (Optional Depth):* Truncation merely curtailed exact-match regex parsing on long scratchpads; it did not inflate or create the source arbitration shift.
* **PRACTICAL / NO-AI TASK:** Reconstruct the 4-row Truncation Sensitivity Table from memory.
* **MASTERY TEST:**
  1. What was the operational definition of a truncated generation in your harness?
  2. If a reviewer claims, "Your Arm 3 results are just an artifact of the model being cut off at 200 tokens," what exact numbers refute this?
  3. Why does the visual capture rate drop by $\approx 60\text{ to } 65\text{ percentage points}$ regardless of whether truncated items are included or excluded?
* **DELIVERABLE:** Sensitivity defense dossier: `Truncation_Sensitivity_and_Internal_Validity.md`.

---

### Phase 4: Paired Statistics, Evaluation Metrics & Empirical Results Audit (Days 22–28)

#### Day 22 — Paired Experimental Design & The Fallacy of Independent Testing

* **WHAT:** Within-item paired designs vs. between-subject designs, and why independent two-sample tests violate statistical assumptions on repeated measures.
* **WHY:** In [`statistical_analysis.py`](file:///d:/Thesis/Important/Cross%20Modal/Finalize%20Topic/Pilot/statistical_analysis.py#L227-L287), you compute both McNemar's paired test and marginal independent tests (Pearson $\chi^2$, Fisher's exact). You must defend why McNemar is the primary inferential test.
* **WHERE:**
  * Primary: *Statistical Methods for Rates and Proportions* (Fleiss, Levin & Paik, 2003), Chapter 10 ("Comparing Proportions in Paired Samples").
  * Secondary: [`Chapter_3_Methodology.md`](file:///d:/Thesis/Important/Cross%20Modal/Thesis_Manuscript/Chapter_3_Methodology.md), Section 3.6.2.
* **HOW DEEP:** **Explain Mathematically:** derive why independent tests violate exchangeability.
* **KNOWLEDGE LAYERS:**
  * *Layer 1 (Core):* Between-subject variance: different math problems have different difficulties. An independent design would require testing different items across arms, introducing difficulty confounding.
  * *Layer 2 (Thesis Connection):* Paired design evaluates item $i$ under all conditions. The unit of variation is the *within-item transition*, eliminating between-item variance.
  * *Layer 3 (Optional Depth):* Independent tests (Pearson $\chi^2$, Fisher) assume $2N$ independent items. Treating $N=1,619$ paired items as $3,238$ independent observations falsely inflates degrees of freedom and ignores positive within-subject correlation.
* **PRACTICAL / NO-AI TASK:** Write a formal proof/explanation showing why applying a two-sample $z$-test of proportions to paired data produces biased standard errors.
* **MASTERY TEST:**
  1. What is the fundamental difference between independent sampling and paired repeated-measures sampling?
  2. Why does evaluating the exact same 1,619 items across all arms make the experiment paired?
  3. Why are Fisher's exact test and Pearson's $\chi^2$ reported only as marginal references rather than primary confirmatory tests?
* **DELIVERABLE:** Statistical methodology chapter: `Paired_Experimental_Design_and_Validity.md`.

---

#### Day 23 — Mathematical Derivation: McNemar's Test & Discordant Pairs

* **WHAT:** Mathematical derivation of McNemar's test, Edwards' continuity correction, and the paired odds ratio.
* **WHY:** Your primary p-value ($\chi^2 = 982.40, p = 1.20 \times 10^{-215}$) is computed using this exact derivation. You must be able to write it on a whiteboard during your thesis defense.
* **WHERE:**
  * Primary: McNemar, Q. (1947). *Note on the sampling error of the difference between correlated proportions or percentages.* Psychometrika, 12(2), 153-157.
  * Secondary: [`statistical_analysis.py`](file:///d:/Thesis/Important/Cross%20Modal/Finalize%20Topic/Pilot/statistical_analysis.py#L100-L119).
* **HOW DEEP:** **Be able to explain mathematically and derive from scratch.**
* **KNOWLEDGE LAYERS:**
  * *Layer 1 (Core):* The $2 \times 2$ paired contingency table: $a$ (concordant visual), $d$ (concordant non-visual), $b$ (discordant: Arm 2 Vis $\to$ Arm 3 Non-Vis), $c$ (discordant: Arm 2 Non-Vis $\to$ Arm 3 Vis).
  * *Layer 2 (Thesis Connection):* Under the null hypothesis $H_0: P(b) = P(c)$, the discordant count follows a binomial distribution $B(b+c, 0.5)$. For large $b+c$, the normal approximation yields:

    $$
    \chi^2 = \frac{(|b - c| - 1)^2}{b + c}

    $$
  * *Layer 3 (Optional Depth):* Plugging in your empirical values: $b = 1057$, $c = 25$.

    $$
    \chi^2 = \frac{(|1057 - 25| - 1)^2}{1057 + 25} = \frac{1031^2}{1082} = \frac{1062961}{1082} = 982.4039

    $$

    Degrees of freedom $df=1 \implies p = 1.20 \times 10^{-215}$.
  * Paired Odds Ratio: $\text{OR}_{\text{paired}} = \frac{b}{c} = \frac{1057}{25} = 42.28$!
* **PRACTICAL / NO-AI TASK:** On a blank sheet of paper, write out the $2 \times 2$ table with values $a=392, b=1057, c=25, d=145$. Manually calculate $\chi^2$ step-by-step using a basic calculator.
* **MASTERY TEST:**
  1. Why do concordant pairs ($a$ and $d$) drop out of McNemar's test statistic?
  2. What is the role of the $-1$ term in Edwards' continuity correction?
  3. What does the paired odds ratio of $42.28$ mean in plain English?
* **DELIVERABLE:** Mathematical derivation sheet: `McNemar_Test_Mathematical_Derivation.md`.

---

#### Day 24 — Effect Sizes: Risk Difference ($\Delta_{\text{arb}}$), Relative Risk & Cohen's $h$

* **WHAT:** Standardized effect size metrics for categorical differences: Risk Difference / Net Shift ($\Delta_{\text{arb}}$), Relative Risk ($RR$), and Cohen's $h$ (arcsin transformation).
* **WHY:** A tiny p-value ($p < 10^{-200}$) only proves that an effect is not noise; it does not prove it is large! You must report standardized effect sizes to prove the magnitude of the discovery.
* **WHERE:**
  * Primary: Cohen, J. (1988). *Statistical Power Analysis for the Behavioral Sciences*, Chapter 6 ("Differences Between Proportions").
  * Secondary: [`statistical_analysis.py`](file:///d:/Thesis/Important/Cross%20Modal/Finalize%20Topic/Pilot/statistical_analysis.py#L121-L131, L267-L282).
* **HOW DEEP:** Mathematical and Statistical interpretation.
* **KNOWLEDGE LAYERS:**
  * *Layer 1 (Core):* Why raw percentage difference is unstandardized: shifting from $90\% \to 25\%$ represents a much larger cognitive variance than $50\% \to 45\%$.
  * *Layer 2 (Thesis Connection):*
    * **Net Shift ($\Delta_{\text{arb}}$):** $89.50\% - 25.76\% = +63.74\text{ percentage points}$.
    * **Relative Risk ($RR$):** $25.76\% / 89.50\% = 0.2878$ ($71.2\%$ reduction in visual capture risk).
    * **Cohen's $h$ Formulation:**

      $$
      h = 2 \arcsin\sqrt{P_1} - 2 \arcsin\sqrt{P_2} = 2 \arcsin\sqrt{0.8950} - 2 \arcsin\sqrt{0.2576} = 2.493 - 1.076 = 1.4170

      $$

      Cohen's benchmarks: $0.2 = \text{Small}, 0.5 = \text{Medium}, 0.8 = \text{Large}$. Your value ($1.42$) is **extraordinarily large**.
  * *Layer 3 (Optional Depth):* Confidence interval calculations for proportions and odds ratios via Woolf's method with Haldane-Anscombe correction.
* **PRACTICAL / NO-AI TASK:** Calculate Cohen's $h$ for a hypothetical shift of $55\% \to 45\%$ ($h = 0.20$, small) vs your shift of $89.5\% \to 25.8\%$ ($h = 1.42$, very large).
* **MASTERY TEST:**
  1. What is the difference between statistical significance (p-value) and practical significance (effect size)?
  2. Why does Cohen's $h$ apply an arcsin square-root transformation to proportions?
  3. How do you interpret a Relative Risk of $0.288$ in the context of visual capture?
* **DELIVERABLE:** Effect size audit dossier: `Effect_Size_Analysis_and_Interpretation.md`.

---

#### Day 25 — The "Smoking Gun": Source-Conditioned Exact-Match Cross-Over

* **WHAT:** Exact agreement with ground-truth mathematical integers ($y^{\text{img}}$ vs $y^{\text{txt}}$) across experimental arms.
* **WHY:** Reviewers will ask: "Did your prompt intervention actually make the model solve the other problem, or did it just scramble the words?" The exact-match cross-over is your definitive proof.
* **WHERE:**
  * Primary: [`CANONICAL_THESIS_MASTER_REPORT.md`](file:///d:/Thesis/Important/Cross%20Modal/Finalize%20Topic/CANONICAL_THESIS_MASTER_REPORT.md), Section 6 ("The Decisive Exact-Match Cross-Over Discovery").
  * Secondary: [`statistical_report v3.0.md`](file:///d:/Thesis/Important/Cross%20Modal/Finalize%20Topic/Pilot/Experiment_Result/statistical_report%20v3.0.md).
* **HOW DEEP:** **Defend Scientifically:** present the numbers, curves, and implications from memory.
* **KNOWLEDGE LAYERS:**
  * *Layer 1 (Core):* Every item in `modality-conflict-arbitration-v2` has two ground-truth integers: $y^{\text{img}} \neq y^{\text{txt}}$.
  * *Layer 2 (Thesis Connection):*
    * **Arm 2 (Placebo):** Exact match on image problem = **$35.6\%$** ($577 / 1,619$); exact match on text problem = **$4.7\%$** ($76 / 1,619$).
    * **Arm 3 (Conflict Verbalization):** Exact match on text problem surges to **$35.8\%$** ($579 / 1,619$); exact match on image problem collapses to **$11.7\%$** ($190 / 1,619$).
  * *Layer 3 (Optional Depth):* The $35.8\%$ text exact match matches the model's natural unconstrained competence ceiling on GSM8K/SVAMP! The model redirected its actual multi-step calculation engine to the text problem.
* **PRACTICAL / NO-AI TASK:** Sketch the Exact-Match Cross-Over plot (X-axis: Arm 2 vs Arm 3; Y-axis: Exact Match %; two crossing lines: Image Match collapsing from $35.6\% \to 11.7\%$, Text Match surging from $4.7\% \to 35.8\%$).
* **MASTERY TEST:**
  1. What was the exact-match accuracy on the text problem in Arm 2 vs Arm 3?
  2. Why does the exact-match cross-over refute the counter-hypothesis that Arm 3 caused random confusion?
  3. Why does the text exact match level off at $\approx 35.8\%$ rather than reaching $100\%$?
* **DELIVERABLE:** Graphic schematic and written narrative: `Exact_Match_Cross_Over_Analysis.md`.

---

#### Day 26 — Markovian Behavioral State Transitions: The 4x4 Migration Matrix

* **WHAT:** Within-item behavioral state modeling: mapping how individual items migrate across categorical states (`Image`, `Text`, `Abstain`, `Ambiguous`) between Arm 2 and Arm 3.
* **WHY:** Aggregate statistics hide individual item dynamics. Tracking within-item migration reveals that the 1,449 visual-capture items in Arm 2 branch into three distinct cognitive fates.
* **WHERE:**
  * Primary: [`CANONICAL_THESIS_MASTER_REPORT.md`](file:///d:/Thesis/Important/Cross%20Modal/Finalize%20Topic/CANONICAL_THESIS_MASTER_REPORT.md), Section 6 ("Within-Subject Transition Dynamics").
  * Secondary: [`statistical_analysis.py`](file:///d:/Thesis/Important/Cross%20Modal/Finalize%20Topic/Pilot/statistical_analysis.py#L289-L300).
* **HOW DEEP:** Technical & Analytical.
* **KNOWLEDGE LAYERS:**
  * *Layer 1 (Core):* The $4 \times 4$ contingency matrix: Rows = Arm 2 Choice; Columns = Arm 3 Choice.
  * *Layer 2 (Thesis Connection):* The fate of the 1,449 Arm 2 visual-capture items:
    1. **Flipped to Text Problem:** $832$ items ($57.41\%$) — verbalization successfully redirects computation to text.
    2. **Transitioned to Abstention:** $201$ items ($13.87\%$) — model identifies contradiction and refuses to arbitrate.
    3. **Persisted in Visual Capture:** $392$ items ($27.05\%$) — hardened visual capture resistant to verbalization.
    4. **Ambiguous / Truncated:** $24$ items ($1.66\%$).
  * *Layer 3 (Optional Depth):* What about the 145 items that followed text in Arm 2? $103$ stayed text, $20$ stayed visual, $20$ abstained, $2$ ambiguous.
* **PRACTICAL / NO-AI TASK:** Recreate the $4 \times 4$ Transition Matrix on paper and verify that the row sums and column sums match the aggregate margins: Row total = 1,449, 145, 4, 21 ($N=1,619$); Column total = 417, 954, 221, 27 ($N=1,619$).
* **MASTERY TEST:**
  1. What happened to the 1,449 items that were visually captured in Arm 2 when subjected to Arm 3?
  2. What percentage of visually captured items successfully arbitrated to text?
  3. How many items abstained in Arm 2 vs Arm 3?
* **DELIVERABLE:** State transition dossier: `State_Migration_and_Transition_Dynamics.md`.

---

#### Day 27 — Resistant Cases: Why Did 392 Items Persist in Visual Capture?

* **WHAT:** Error analysis and phenomenological inspection of the $27.05\%$ resistant items ($392 / 1,449$) that remained visually captured in Arm 3.
* **WHY:** Good science does not hide failures. Investigating why $392$ items resisted the conflict verbalization intervention demonstrates scientific maturity and provides future work directions.
* **WHERE:**
  * Primary: Inspect specific resistant records in [`full_experiment_results v3.0.json`](file:///d:/Thesis/Important/Cross%20Modal/Finalize%20Topic/Pilot/Experiment_Result/full_experiment_results%20v3.0.json).
  * Secondary: [`CANONICAL_THESIS_MASTER_REPORT.md`](file:///d:/Thesis/Important/Cross%20Modal/Finalize%20Topic/CANONICAL_THESIS_MASTER_REPORT.md), Section 6 & 8 (Chapter 5 blueprint).
* **HOW DEEP:** **Phenomenological & Diagnostic.**
* **KNOWLEDGE LAYERS:**
  * *Layer 1 (Core):* What characterizes resistant items? Are they concentrated in GSM8K or SVAMP? Do they feature specific visual layouts?
  * *Layer 2 (Thesis Connection):* Three discovered failure modes in resistant items:
    1. *Superficial Verbalization:* The model outputs "The image and text contradict each other," but immediately follows with "Following the image problem..." without articulating a reliability justification.
    2. *OCR Visual Saliency:* High typographical contrast or large font sizes in the rendered image overpowering textual prompt tokens in early attention layers.
    3. *Arithmetic Inertia:* The model initiates calculation using image numbers in its first verbal sentence, creating an autoregressive commitment trap.
  * *Layer 3 (Optional Depth):* How activation patching or probing in Layer 18–24 could locate the circuit of resistance in future work.
* **PRACTICAL / NO-AI TASK:** Open `full_experiment_results v3.0.json`, locate 3 items where `arm2_placebo.choice == 'follows_image_problem'` and `arm3_conflict.choice == 'follows_image_problem'`. Transcribe their exact Arm 3 generated text and annotate where the failure occurred.
* **MASTERY TEST:**
  1. What proportion of items remained in visual capture despite the conflict intervention?
  2. What is an "autoregressive commitment trap" in chain-of-thought generation?
  3. What are two plausible architectural/perceptual reasons why an item might resist verbalized arbitration?
* **DELIVERABLE:** Qualitative error taxonomy: `Qualitative_Audit_Resistant_Cases.md`.

---

#### Day 28 — Exploratory Arm 4: Rationale Prefilling vs Full Verbalization

* **WHAT:** Comparing the behavioral steering effect of full deliberative verbalization (Arm 3) against short forced rationale prefilling (Arm 4a and Arm 4b).
* **WHY:** Directly tests whether forcing an assertion ("The image and text contradict... Following the image problem, the answer is: #### ") is sufficient to steer multi-step arithmetic without intermediate scratchpads.
* **WHERE:**
  * Primary: [`CANONICAL_THESIS_MASTER_REPORT.md`](file:///d:/Thesis/Important/Cross%20Modal/Finalize%20Topic/CANONICAL_THESIS_MASTER_REPORT.md), Section 6 ("Arm 4: Exploratory Rationale Prefilling Analysis").
  * Secondary: [`statistical_analysis.py`](file:///d:/Thesis/Important/Cross%20Modal/Finalize%20Topic/Pilot/statistical_analysis.py#L302-L320).
* **HOW DEEP:** **Defend Scientifically:** explain why prefilling showed weak steering and how it contrasts with Arm 3.
* **KNOWLEDGE LAYERS:**
  * *Layer 1 (Core):* Assistant prefilling bypasses the generation of reasoning scratchpads by placing text directly after `<|im_start|>assistant\n`.
  * *Layer 2 (Thesis Connection):* Empirical findings:
    * Invariant Answer Rate: **$58.55\%$** of items ($948 / 1,619$) output the exact same integer answer regardless of whether they were prefilled with the "image" or "text" directive!
    * Text Alignment Gain: Arm 4b achieved only a **$+5.31\text{ pp}$** increase in exact text-answer matching over Arm 4a ($21.1\%$ vs $15.8\%$).
  * *Layer 3 (Optional Depth):* Scientific Conclusion: Short prefilled assertions without scratchpad computation provide a very weak causal lever for multi-step multimodal arithmetic. Full verbalization (Arm 3) is required for robust arbitration.
* **PRACTICAL / NO-AI TASK:** Reconstruct the Arm 4 comparison table from memory and write a 1-paragraph interpretation of why $58.6\%$ of outputs were identical.
* **MASTERY TEST:**
  1. How was Arm 4 implemented in the KV cache using `apply_chat_template`?
  2. What was the exact text-alignment gain of Arm 4b over Arm 4a?
  3. Why does this exploratory result reinforce the necessity of full multi-step scratchpad verbalization (Arm 3)?
* **DELIVERABLE:** Technical report: `Arm4_Prefill_vs_Full_Verbalization.md`.

---

### Phase 5: Defense Mastery, Adversarial Cross-Examination & Thesis Finalization (Days 29–30)

#### Day 29 — First-Principles Thesis Reconstruction & The 10-Point Defense Ledger

* **WHAT:** Reconstructing the entire thesis from scratch without consulting code, notes, or AI.
* **WHY:** If you cannot explain the entire thesis from memory, you are not ready to defend it before an academic committee.
* **WHERE:**
  * Primary: A completely blank document.
  * Target Reference: [`CANONICAL_THESIS_MASTER_REPORT.md`](file:///d:/Thesis/Important/Cross%20Modal/Finalize%20Topic/CANONICAL_THESIS_MASTER_REPORT.md).
* **HOW DEEP:** **Mastery from memory.**
* **KNOWLEDGE LAYERS:**
  * *Layer 1 (Core):* Reconstructing the 10 core elements:
    1. Problem: Multimodal contradiction under clean legibility.
    2. Phenomenon: Extreme visual capture under descriptive prompt ($89.5\%$).
    3. Existing Explanation: Modality dominance / reliance under degradation (Ghosh).
    4. Gap: Does explicit conflict verbalization causally change source arbitration when compute is controlled?
    5. Primary RQ: RQ1.
    6. Null Hypothesis $H_0$: $\Delta_{\text{visual}} = 0$.
    7. Alternative Hypothesis $H_1$: $\Delta_{\text{visual}} \neq 0$ ($p < 0.001$).
    8. Intervention: Arm 3 (Conflict & Reliability evaluation) vs Arm 2 (Neutral placebo).
    9. Confirmatory Test: McNemar's paired test on discordant pairs ($b=1057, c=25$).
    10. Smoking Gun: Exact-match cross-over ($35.6\% \to 35.8\%$).
* **PRACTICAL / NO-AI TASK:** Close all windows. Take a blank sheet of paper and write out all 10 points in full prose without pausing.
* **MASTERY TEST:**
  1. State your primary research question in one sentence.
  2. State your null hypothesis $H_0$ mathematically.
  3. What is the single most compelling piece of evidence that proves your intervention changed actual problem solving rather than superficial output words?
* **DELIVERABLE:** Hand-written or typed 3-page thesis reconstruction: `Thesis_Reconstruction_First_Principles.md`.

---

#### Day 30 — The Adversarial Defense Simulation (Oral Examination Trial)

* **WHAT:** Simulating a hostile oral defense committee grilling you on every methodological choice, boundary, and potential flaw.
* **WHY:** The ultimate trial. You must be able to withstand hostile questions without wavering or appealing to authority.
* **WHERE:**
  * Source Material: [`CANONICAL_THESIS_MASTER_REPORT.md`](file:///d:/Thesis/Important/Cross%20Modal/Finalize%20Topic/CANONICAL_THESIS_MASTER_REPORT.md), Section 5, 8, & 9.
* **HOW DEEP:** **Defend under adversarial cross-examination.**
* **PRACTICAL / NO-AI TASK:** Answer the 7 Hostile Committee Attacks below in writing, completely from memory, with no AI assistance:
  * *Attack 1:* "Isn't Arm 3 simply telling the model to follow the text? If you tell a model to solve the text problem, of course it solves the text problem!"
  * *Attack 2:* "Why did you use McNemar's test instead of a standard Chi-Square test or logistic regression?"
  * *Attack 3:* "Your model suffered $40\%$ truncation at 200 tokens. Aren't your findings completely confounded by incomplete generations?"
  * *Attack 4:* "Does your thesis prove that the internal attention heads in Layer 20 shifted their attention weights from image tokens to text tokens?"
  * *Attack 5:* "Your images are just rendered text. How does this generalize to autonomous vehicles or medical imaging?"
  * *Attack 6:* "Why did Arm 1 choose text 85% of the time, while Arm 2 chose image 89% of the time?"
  * *Attack 7:* "What is the scientific value of this thesis if your primary hypothesis had been rejected ($\Delta_{\text{arb}} \approx 0$)?"
* **DELIVERABLE:** Complete defense transcript: `Thesis_Oral_Defense_Question_Bank.md`.

---

## 4. Weekly Mastery Gates

### Gate 1 — VLM Architecture & Hardware Execution (End of Day 7)

*You cannot proceed to literature until you pass this gate.*

* [ ]  Can draw the complete architecture of `Qwen2.5-VL-3B-Instruct` from memory, including dynamic ViT, spatial patch merge ($14 \times 14 \to 28 \times 28$), linear projection, MRoPE 3D position tuples, and the 36-layer decoder backbone.
* [ ]  Can explain why causal decoder batching requires **left-padding** and why right-padding corrupts generation.
* [ ]  Can explain why PyTorch SDPA and native FP16 Tensor Cores were necessary to execute 8,095 forward passes in $\approx 1.7$ hours on a Colab T4.
* [ ]  Can explain why `image_grid_thw.prod(-1)` crashed on CUDA 13 and why the CPU monkey-patch is mathematically exact.

### Gate 2 — Anchor Literature & Research Gap (End of Day 14)

*You cannot proceed to methodology until you pass this gate.*

* [ ]  Can cite the 6 primary anchor papers (*Which Source Wins?*, *CLASH*, *Mixed Signals*, *Source Monitoring*, *Words or Vision*, *Challenges in Modality Conflict*) with authors, years, and core findings.
* [ ]  Can articulate the exact gap left open in Section 6 of Ghosh et al. (2026).
* [ ]  Can explain the conceptual and operational distinction between **contradiction detection** (Popordanoska) and **source arbitration** (your thesis).
* [ ]  Can explain why Arm 1 defaults to text ($85.5\%$) and Arm 2 defaults to image ($89.5\%$) based on Deng et al.'s findings on token recency and visual salience.

### Gate 3 — Reasoning, Faithfulness & Causal Control (End of Day 21)

*You cannot proceed to results until you pass this gate.*

* [ ]  Can define CoT unfaithfulness and explain Turpin et al.'s demonstration of post-hoc rationalization.
* [ ]  Can explain why Arm 2 (Length-Matched Neutral Placebo) is mandatory to eliminate test-time compute and preamble syntax confounds.
* [ ]  Can explain the difference between source arbitration and task accuracy.
* [ ]  Can present the Truncation Sensitivity Table proving that the visual reduction ($\sim 60\text{ to } 65\text{ pp}$) is invariant across non-truncated and truncated cohorts.

### Gate 4 — Paired Statistics & Quantitative Discovery (End of Day 28)

*You cannot proceed to defense until you pass this gate.*

* [ ]  Can derive McNemar's test with Edwards' continuity correction on paper and explain why concordant pairs drop out.
* [ ]  Can state all primary empirical results from memory:
  * Arm 2 Placebo Visual Capture: $89.50\%$ ($1,449 / 1,619$)
  * Arm 3 Conflict Visual Capture: $25.76\%$ ($417 / 1,619$)
  * Net Shift $\Delta_{\text{arb}}$: $+63.74\text{ pp}$ ($OR = 24.57, p = 1.20 \times 10^{-215}$)
  * Cohen's $h$: $1.4170$ (Very Large)
  * Discordant pairs: $b = 1057, c = 25$
* [ ]  Can present the Exact-Match Cross-Over from memory: Image match collapses from $35.6\% \to 11.7\%$, text match surges from $4.7\% \to 35.8\%$.
* [ ]  Can explain the $4 \times 4$ Markov migration matrix and the three fates of the 1,449 visual items ($832$ text, $201$ abstain, $392$ visual).
* [ ]  Can explain why Arm 4 prefill had $58.6\%$ identical answers and why short prefixes provide weak steering.

### Gate 5 — Oral Defense & Epistemic Humility (End of Day 30)

* [ ]  Can answer all 7 hostile committee attacks without looking at notes.
* [ ]  Can clearly delineate what your thesis claims vs what it explicitly does NOT claim (the "Do Not Write" directives).
* [ ]  Can articulate the symmetric value of the thesis in one paragraph.

---

## 5. Code → Concept Map


| Exact Function / Variable in Repository | What It Does in Code                                                                                                                                                                                                           | Underlying ML / NLP Concept                            | Underlying VLM / Architectural Concept                                                                                                                                                               | Why You Must Understand It to Defend the Thesis                                                                   |
| :---------------------------------------- | :------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | :------------------------------------------------------- | :----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | :------------------------------------------------------------------------------------------------------------------ |
| `select_dtype()`                        | Checks GPU compute capability; returns`float16` for `sm_75`, `bfloat16` for `sm_80+`                                                                                                                                           | Hardware-aware floating-point precision                | Tensor Core architecture; emulation overhead vs native execution                                                                                                                                     | Explains why inference sustained$\approx 2.5\text{s/item}$ on T4 without running out of compute budget.           |
| `select_attn_impl()`                    | Selects`sdpa` kernel if available                                                                                                                                                                                              | Fused kernel computation, GPU IO complexity            | Scaled Dot-Product Attention in multi-head attention blocks                                                                                                                                          | Proves you understand how$\mathcal{O}(N^2)$ memory bottleneck was bypassed.                                       |
| `_safe_tensor_prod`                     | CPU fallback patch for`.prod(-1)` on integer CUDA tensors                                                                                                                                                                      | PyTorch dynamic JIT compilation (NVRTC)                | 3D grid token tracking (`thw`) in MRoPE                                                                                                                                                              | Demonstrates deep systems engineering: debugging low-level CUDA driver-framework incompatibilities.               |
| `min_pixels`, `max_pixels`              | Caps image pixel boundaries in`AutoProcessor`                                                                                                                                                                                  | Image resolution preprocessing bounds                  | Native dynamic ViT token budgeting ($14\times 14$ patches $\to 28\times 28$ tokens) | Proves visual sequence length was strictly bounded to$\approx 256$ tokens, preventing visual token domination. |                                                                                                                   |
| `tokenizer.padding_side = "left"`       | Sets tokenizer pad direction to left                                                                                                                                                                                           | Causal autoregressive decoding alignment               | Left vs right padding in batched decoder generation                                                                                                                                                  | Explains why batched inference generated coherent tokens instead of corrupting generation prompts.                |
| `make_chat_text(...)`                   | Calls`apply_chat_template`, strips `<                                                                                                                                                                                          | im_end                                                 | >` for prefill                                                                                                                                                                                       | Special token serialization and turn boundaries                                                                   |
| `PROMPT_ARM2_PLACEBO`                   | Prompts for 2-sentence neutral description without comparison                                                                                                                                                                  | Experimental control, nuisance variable neutralization | Test-time compute matching, prompt preamble syntax matching                                                                                                                                          | **The core causal control.** Eliminates the counter-argument that extra reasoning tokens caused the shift.        |
| `PROMPT_ARM3_CONFLICT`                  | Prompts for 2-sentence agreement/contradiction & reliability evaluation                                                                                                                                                        | Causal experimental intervention                       | Evaluative task decomposition; source monitoring prompt                                                                                                                                              | **The primary treatment variable.** Steers model to evaluate source conflict prior to solving.                    |
| `PREFILL_ARM4_...`                      | Pre-populates assistant answer with forced rationale prefix                                                                                                                                                                    | Rationale prefilling intervention (Lanham et al.)      | Counterfactual prefix conditioning in KV-cache                                                                                                                                                       | Proves you tested whether short prefix steering alone is causally binding ($58.6\%$ invariant).                   |
| `extract_answer_after_hashes`           | Two-stage regex: primary on`#### <val>`, fallback on last numeric token                                                                                                                                                        | Deterministic string extraction                        | Delimiter-constrained output contracts                                                                                                                                                               | Eliminates subjective LLM-as-a-judge scoring; guarantees 100% deterministic reproducibility.                      |
| `detect_abstention`                     | Matches refusal phrases (`cannot be determined`, etc.)                                                                                                                                                                         | Selective classification, reject option ($\perp$)      | Contradiction-conditioned epistemic refusal                                                                                                                                                          | Proves that 221 Arm 3 abstentions were genuine epistemic refusals, not pipeline parse errors.                     |
| `extract_entities`                      | Regex extraction of proper nouns and content nouns with stoplist                                                                                                                                                               | Lexical and semantic entity filtering                  | Evidence grounding and source identification                                                                                                                                                         | Allows disentangling which problem the model solved when arithmetic calculation failed.                           |
| `classify_problem_choice`               | Evaluates entity margins and ground truth matches                                                                                                                                                                              | Operational decision categorization                    | Behavioral source arbitration classification                                                                                                                                                         | Maps continuous text generation into discrete states:`follows_image`, `follows_text`, `abstains`, `ambiguous`.    |
| `mcnemar_test_2x2`                      | Calculates$\chi^2 = (|b-c|-1)^2 / (b+c)$ on discordant pairs                                                                                                                                                                   | Repeated-measures hypothesis testing                   | Within-item behavioral state transition significance                                                                                                                                                 | **Your primary confirmatory statistical test.** Explains why $p = 1.20 \times 10^{-215}$ is mathematically sound. |
| `cohens_h`                              | $2 \arcsin\sqrt{P_1} - 2 \arcsin\sqrt{P_2}$ | Standardized proportion effect size | Magnitude estimation for categorical shifts | Proves the effect size ($h=1.42$) is "Very Large", not just a large-sample p-value artifact. |                                                        |                                                                                                                                                                                                      |                                                                                                                   |
| `truncated` flag                        | Flags if`tokens >= max_new_tokens - 1`                                                                                                                                                                                         | Ceiling effect monitoring, censoring analysis          | Autoregressive generation length bounds                                                                                                                                                              | Enables the sensitivity split proving that truncation did not create the visual reduction shift.                  |

---

## 6. Thesis Claim → Required Knowledge Map


| Formal Thesis Claim / Research Question                                                                                               | Underlying Hypothesis                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                | Empirical Finding                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                               | Deep Knowledge Required to Defend It                                                                                                     | How to Defend Against Committee Skepticism                                                                                                      |
| :-------------------------------------------------------------------------------------------------------------------------------------- | :--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | :-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | :----------------------------------------------------------------------------------------------------------------------------------------- | :------------------------------------------------------------------------------------------------------------------------------------------------ |
| **Claim 1 (Primary):** Conflict verbalization causally shifts observable source arbitration away from visual capture.                 | $H_1: P(V\mid A_2) \neq P(V\mid A_3)$                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                | $\Delta_{\text{arb}} = +63.74\text{ pp}$ ($89.50\% \to 25.76\%$), $\chi^2 = 982.40$, $p = 1.20 \times 10^{-215}$. | Causal DAGs, paired experimental design, McNemar test, discordant pairs. | Cite the paired odds ratio ($42.28$); point to discordant pairs ($b=1057$ vs $c=25$); emphasize that items are identically paired.                                                                                                                                                                                                                                               |                                                                                                                                          |                                                                                                                                                 |
| **Claim 2 (Placebo Control):** The shift is caused by semantic conflict evaluation, not by extra reasoning tokens.                    | $H_1$: Arm 3 shift survives length-matched neutral control.                       | Arm 2 has$\approx 50$ tokens of neutral text but exhibits $89.50\%$ visual capture. | Confounding, back-door criterion, test-time compute, CoT length matching. | Explain that Arm 2 gave the model the exact same token and preamble headroom; visual capture actually *increased* in Arm 2 ($89.5\%$) relative to Arm 1 ($13.8\%$).                                                                                                                                                                                                                                            |                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                 |                                                                                                                                          |                                                                                                                                                 |
| **Claim 3 (Problem Execution):** The shift reflects actual execution of the competing problem, not random drift or verbal scrambling. | $H_2$: Exact-match accuracy inverts toward the selected source.                   | Arm 2:$35.6\%$ Img / $4.7\%$ Txt $\to$ Arm 3: $11.7\%$ Img / **$35.8\%$ Txt**.                                                                                                                                                                                                                                                        | Ground-truth mathematical determinism, task competence ceiling vs source selection.         | Present the Exact-Match Cross-Over plot. Text exact match surged by$+31.1\text{ pp}$, reaching the model's natural GSM8K accuracy ceiling. |                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                 |                                                                                                                                          |                                                                                                                                                 |
| **Claim 4 (Abstention):** Conflict verbalization enables legitimate epistemic refusal when premises contradict.                       | $H_3$: Verbalization increases abstention under contradiction.                    | Arm 2:$0.2\%$ ($4 / 1619$) $\to$ Arm 3: **$13.7\%$** ($221 / 1619$).                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                             | Selective prediction, reject option, epistemic uncertainty vs perceptual hallucination.                                                                                                                                                                                                                                                                                                                                                                                                                                                                                         | Show that the model explicitly states that the problems contradict and therefore no single answer exists; verify regex patterns in code. |                                                                                                                                                 |
| **Claim 5 (Behavioral Heterogeneity):** Items exhibit distinct behavioral migration; some resist the intervention.                    | $H_4, H_5$: Non-uniform transition matrix; non-trivial resistance.                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                   | $57.4\%$ flip to text, $13.9\%$ abstain, **$27.1\%$ persist in visual capture**.                                                                                                                                                                                                                                                      | Markov transition matrices, OCR typographical saliency, autoregressive commitment.          | Walk through the$4 \times 4$ matrix. Explain that $392$ items resisted due to high visual saliency and early arithmetic commitment traps. |                                                                                                                                          |                                                                                                                                                 |
| **Claim 6 (Prefilling Limitation):** Short rationale prefilling is a weak causal lever for multi-step arithmetic.                     | Exploratory probe: prefilling has lower steering efficacy than full CoT.                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                             | **$58.55\%$ identical answers** across opposing prefills; text gain was only $+5.3\text{ pp}$.                                                                                                                                                                                                                                                                                                                                                                                                                                                                                  | Lanham et al. faithfulness methodology, KV-cache prefix conditioning, scratchpad necessity.                                              | Contrast Arm 4 with Arm 3: without multi-step scratchpad computation, prefix assertions fail to steer the autoregressive arithmetic trajectory. |
| **Claim 7 (Internal Validity):** Results are not an artifact of the 200-token generation ceiling.                                     | Robustness check:$\Delta_{\text{visual}}$ is invariant across truncation subsets. | Non-truncated cohort:$-65.0\text{ pp}$; Truncated cohort: $-61.5\text{ pp}$. | Right-censoring, ceiling effects, sensitivity analysis in empirical design. | Show that visual reduction is virtually identical ($\approx 60\text{ to } 65\text{ pp}$) in both non-truncated ($N=1011/903$) and truncated ($N=608/716$) splits.                                                                                                                                                                                                                                                   |                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                 |                                                                                                                                          |                                                                                                                                                 |
| **Claim 8 (Scope & Epistemic Limit):** We do NOT claim internal attention rerouting or human epistemic competence.                    | Epistemic boundary: behavioral prompt intervention only.                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                             | Behavioral outputs only; no internal mechanistic probing was executed.                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                          | Mechanistic interpretability boundaries, Level-3 causal claim boundaries.                                                                | Direct committee to Chapter 1, Section 1.11: transparently concede that internal circuits were not probed, preserving scientific credibility.   |

---

## 7. Critical vs. Important vs. Optional Knowledge

```
                          KNOWLEDGE TAXONOMY FOR THESIS MASTERY

   CRITICAL KNOWLEDGE (Must Master Before Defense — Zero Tolerance for Gaps)
   ├── 1. Exact architecture & inference flow of Qwen2.5-VL-3B-Instruct (MRoPE, dynamic ViT, SDPA).
   ├── 2. The 6 Anchor Papers (Which Source Wins?, CLASH, Mixed Signals, Source Monitoring, Deng, Nguyen).
   ├── 3. Paired experimental design & McNemar's test mathematical derivation (b=1057, c=25, p < 10^-200).
   ├── 4. Causal role of Arm 2 (Neutral Placebo) in closing the test-time compute back-door path.
   ├── 5. Exact-Match Cross-Over empirical discovery (Image: 35.6% -> 11.7%, Text: 4.7% -> 35.8%).
   ├── 6. Truncation sensitivity audit proving robustness across non-truncated and truncated subsets.
   └── 7. Methodological boundaries: behavioral prompt intervention vs internal circuit claims.

   IMPORTANT KNOWLEDGE (Substantially Elevates Quality & Context of Thesis)
   ├── 1. Lanham et al. (2023) and Turpin et al. (2023) CoT unfaithfulness and post-hoc rationalization.
   ├── 2. 4x4 Markovian state migration dynamics of the 1,449 visual capture items.
   ├── 3. Selective classification theory and risk-coverage trade-offs (Geifman & El-Yaniv).
   ├── 4. Token recency vs visual salience mechanisms in autoregressive attention (Deng et al.).
   └── 5. Exploratory Arm 4 findings: why short prefix prefilling yielded 58.6% invariant answers.

   USEFUL BUT NON-ESSENTIAL (Can Wait Until Post-Thesis Independent Research)
   ├── 1. Early VLM bridge architectures (Flamingo Perceiver resamplers, BLIP-2 Q-Former).
   ├── 2. Linear probing of intermediate layers for conflict detection (Nguyen et al.).
   ├── 3. General VQA benchmarks (ScienceQA, TextVQA, GQA, DocVQA).
   └── 4. Multi-Query / Grouped-Query Attention memory bandwidth derivations.

   IRRELEVANT / DO NOT STUDY (Actively Harmful Distractions for This Thesis)
   ├── 1. Foundation model pretraining from scratch, multi-node distributed training (Megatron/DeepSpeed).
   ├── 2. RLHF, PPO, DPO, GRPO loss function derivations and reward modeling.
   ├── 3. Mixture-of-Experts (MoE) routing, expert capacity factors, load balancing losses.
   ├── 4. Diffusion models, flow matching, video generation architectures.
   ├── 5. Vision-Language-Action (VLA) robotics and autonomous agent frameworks.
   └── 6. CUDA C++/Triton kernel programming (you already solved the NVRTC issue with your Python patch).
```

---

## 8. Papers / Videos / Documentation Master List

### 1. Primary Anchor Research Papers (Must Read Deeply)

1. **Which Source Wins? Task-Dependent Reliance in Vision-Language Models**
   *Authors:* S. Ghosh, A. Gupta, Y. Wang (Aug 2026).
   *URL:* [arXiv:2608.17205](https://arxiv.org/abs/2608.17205) | [PDF](https://arxiv.org/pdf/2608.17205)
   *Sections to Master:* §1, §3 (Benchmark Construction), §4 (Reliance Metric), §6 (Explicit Limitations & Gaps).
2. **CLASH: A Benchmark for Cross-Modal Contradiction Detection**
   *Authors:* T. Popordanoska, M. Li, M. B. Blaschko (Nov 2025).
   *URL:* [arXiv:2511.19199](https://arxiv.org/abs/2511.19199) | [PDF](https://arxiv.org/pdf/2511.19199)
   *Sections to Master:* §1, §3 (Contradiction Types), §5 (Failure Analysis).
3. **Mixed Signals: Decoding VLMs' Reasoning and Underlying Bias in Vision-Language Conflict**
   *Authors:* P. Pezeshkpour, M. Aminnaseri, E. Hruschka (EMNLP Findings 2025).
   *URL:* [ACL Anthology](https://aclanthology.org/2025.findings-emnlp.1351/) | [PDF](https://aclanthology.org/2025.findings-emnlp.1351.pdf)
   *Sections to Master:* §1, §4 (Prompt Modifications & Mitigations), §6 (Discussion).
4. **Source-Modality Monitoring in Vision-Language Models**
   *Authors:* W. Hua, K. Yun, E. Pavlick (Apr 2026).
   *URL:* [arXiv:2604.22038](https://arxiv.org/abs/2604.22038) | [PDF](https://arxiv.org/pdf/2604.22038)
   *Sections to Master:* §1, §3 (Source Tasks), §5 (Probing).
5. **Words or Vision: Do Vision-Language Models Have Blind Faith in Text?**
   *Authors:* Y. Deng, J. Cao, H. Chen, W. Hooi (CVPR 2025).
   *URL:* [CVF Open Access](https://openaccess.thecvf.com/content/CVPR2025/papers/Deng_Words_or_Vision_Do_Vision-Language_Models_Have_Blind_Faith_in_Text_CVPR_2025_paper.pdf)
   *Sections to Master:* §3 (Modality Preference), §4 (Token Order & Positional Bias).
6. **Challenges in Understanding Modality Conflict in Vision-Language Models**
   *Authors:* T. Nguyen, J. Michaels, M. Fiterau, D. Jensen (Sept 2025).
   *URL:* [arXiv:2509.02805](https://arxiv.org/abs/2509.02805) | [PDF](https://arxiv.org/pdf/2509.02805)
   *Sections to Master:* §1, §3 (Separating Detection from Resolution).
7. **Qwen2.5-VL Technical Report**
   *Authors:* S. Bai et al. (Qwen Team, Feb 2025).
   *URL:* [arXiv:2502.13923](https://arxiv.org/abs/2502.13923) | [PDF](https://arxiv.org/pdf/2502.13923)
   *Sections to Master:* §2 (Architecture, Dynamic ViT, MRoPE), §3 (Inference Configuration).
8. **Qwen2-VL: To See the World More Clearly**
   *Authors:* P. Wang et al. (Sept 2024).
   *URL:* [arXiv:2409.12191](https://arxiv.org/abs/2409.12191) | [PDF](https://arxiv.org/pdf/2409.12191)
   *Sections to Master:* §2.1 (Dynamic Resolution), §2.2 (MRoPE).
9. **Language Models Don't Always Say What They Think: Unfaithful Explanations in Chain-of-Thought Prompting**
   *Authors:* M. Turpin, J. Michael, E. Perez, S. R. Bowman (NeurIPS 2023).
   *URL:* [arXiv:2305.04388](https://arxiv.org/abs/2305.04388) | [PDF](https://arxiv.org/pdf/2305.04388)
   *Sections to Master:* §1, §3 (Biased Context Experiment), §5 (Discussion).
10. **Measuring Faithfulness in Chain-of-Thought Reasoning**
    *Authors:* T. Lanham et al. (Anthropic, July 2023).
    *URL:* [arXiv:2307.13702](https://arxiv.org/abs/2307.13702) | [PDF](https://arxiv.org/pdf/2307.13702)
    *Sections to Master:* §2 (Definitions), §3 (Interventions), §5 (Early Answering & Prefilling).

---

### 2. Methodological & Statistical Foundations

11. **Note on the Sampling Error of the Difference Between Correlated Proportions or Percentages**
    *Author:* Quinn McNemar (Psychometrika, 1947, 12(2):153–157).
    *Core Topic:* Mathematical derivation of the paired discordant $\chi^2$ test.
12. **Statistical Power Analysis for the Behavioral Sciences (2nd Edition)**
    *Author:* Jacob Cohen (1988), Lawrence Erlbaum Associates.
    *Core Topic:* Chapter 6: The arcsin transformation effect size (Cohen's $h$).
13. **FlashAttention: Fast and Memory-Efficient Exact Attention with IO-Awareness**
    *Authors:* T. Dao et al. (NeurIPS 2022).
    *URL:* [arXiv:2205.14135](https://arxiv.org/abs/2205.14135) | [PDF](https://arxiv.org/pdf/2205.14135)
    *Core Topic:* Fused kernel GPU SRAM memory hierarchy.
14. **Selective Classification for Deep Neural Networks**
    *Authors:* Y. Geifman, R. El-Yaniv (NeurIPS 2017).
    *URL:* [arXiv:1705.08500](https://arxiv.org/abs/1705.08500) | [PDF](https://arxiv.org/pdf/1705.08500)
    *Core Topic:* Mathematical formalization of the reject option ($\perp$) and risk-coverage curves.

---

### 3. Official Repositories & Authoritative Documentation

* **Qwen2.5-VL Official GitHub Repository:** [https://github.com/QwenLM/Qwen2.5-VL](https://github.com/QwenLM/Qwen2.5-VL)
  *Files to Inspect:* `qwen_vl_utils/vision_process.py` (dynamic patch calculation) and model loading templates.
* **Hugging Face Transformers Qwen2_5_VL Documentation:** [Hugging Face Qwen2_5_VL Docs](https://huggingface.co/docs/transformers/main/en/model_doc/qwen2_5_vl)
* **PyTorch SDPA Documentation:** [PyTorch Fused Attention Docs](https://pytorch.org/docs/stable/generated/torch.nn.functional.scaled_dot_product_attention.html)
* **Primary Thesis Dataset on Hugging Face:** `vlm-modality-research/modality-conflict-arbitration-v2` ([Hugging Face Dataset Page](https://huggingface.co/datasets/vlm-modality-research/modality-conflict-arbitration-v2))

---

### 4. Authoritative Video Lectures (For Intuition Only)

* **Andrej Karpathy — Let's build GPT: from scratch, in code, spelled out:** [YouTube Link](https://www.youtube.com/watch?v=kCc8FmEb1nY)
  *Watch:* Minutes 15:00 to 50:00 (Self-attention matrices, causal masking, logits, and generation loop).
* **Umar Jamil — Attention is all you need (Transformer) & RoPE Detailed Walkthrough:** [YouTube Link](https://www.youtube.com/watch?v=bCz4OMemCcA)
  *Watch:* Rotary Position Embedding derivation and 2D complex rotation visualization.

---

## 9. What Not to Study

To guarantee completion in 30 days without cognitive burnout, you are explicitly forbidden from spending time on the following topics:

1. **Pretraining from Scratch & Large-Scale Distributed Systems:**
   *Forbidden:* DeepSpeed ZeRO-3, Megatron-LM tensor/pipeline parallelism, FSDP sharding mathematics, gradient accumulation across multi-node InfiniBand clusters.
   *Reason:* You are an undergraduate researcher running inference on a frozen 3B parameter model on Colab. You will never pretrain a foundation model for this thesis.
2. **Alignment & Preference Training Optimization:**
   *Forbidden:* Reinforcement Learning from Human Feedback (RLHF), PPO advantage estimation, Direct Preference Optimization (DPO), Kahneman-Tversky Optimization (KTO), Group Relative Policy Optimization (GRPO).
   *Reason:* You are studying the behavioral outputs of an existing instruction-tuned model. Deriving policy gradients has zero bearing on your research questions.
3. **Mixture-of-Experts (MoE) Architecture:**
   *Forbidden:* Top-$k$ gating routers, expert load balancing loss, capacity factors, Switch Transformers, Mixtral routing.
   *Reason:* `Qwen2.5-VL-3B-Instruct` is a dense Transformer backbone, not an MoE.
4. **Diffusion Models & Generative Vision:**
   *Forbidden:* DDPM, DDIM, score-based generative modeling, classifier-free guidance, Stable Diffusion, VAE latents.
   *Reason:* You are working exclusively in autoregressive text generation from visual inputs. Pixel generation is completely unrelated.
5. **Embodied AI & Robotics (VLA):**
   *Forbidden:* OpenVLA, RT-2, action tokenization, robot manipulation benchmarks.
   *Reason:* Completely outside the scope of cross-modal reasoning.
6. **Mechanistic Probing Code Implementation:**
   *Forbidden:* Writing PyTorch activation cache hooks, training linear probes on Layer 18, residual stream intervention, sparse autoencoders (SAEs).
   *Reason:* You explicitly defined your thesis as a **behavioral causal prompt intervention** and placed mechanistic circuit probing outside your claim boundary. Attempting ad-hoc probing now would jeopardize your thesis defense timeline.

---

## 10. Final Day-30 Competency Checklist

On the morning of Day 30, test yourself against these 10 definitive exit competencies:

- [ ]  **1. Architecture Fluency:** I can draw Qwen2.5-VL from memory (Dynamic ViT $\to$ Spatial Merge $\to$ Projector $\to$ MRoPE $\to$ 36 Layers $\to$ RMSNorm $\to$ LM Head $\to$ Greedy Argmax) and calculate exact token counts from pixel dimensions.
- [ ]  **2. Codebase Mastery:** I can open [`production_experiment_harness_v3.py`](file:///d:/Thesis/Important/Cross%20Modal/Finalize%20Topic/Pilot/production_experiment_harness_v3.py) and explain the exact mechanical necessity of left-padding, SDPA, FP16 precision, the CUDA 13 JIT monkey-patch, and the 3-group token budgets.
- [ ]  **3. Anchor Literature Positioning:** I can explain the core findings of Ghosh et al. (2026), Popordanoska et al. (2025), Pezeshkpour et al. (2025), and Hua et al. (2026), and articulate why my thesis fills a gap that none of them addressed.
- [ ]  **4. Causal Identification:** I can draw the causal DAG of my experiment and explain why Arm 2 (Neutral Placebo) is required to close the test-time compute back-door path.
- [ ]  **5. Statistical Proof:** I can derive McNemar's test with Edwards' continuity correction on a whiteboard, explain why concordant pairs drop out, and calculate $\chi^2 = 982.40$ from discordant counts $b=1057$ and $c=25$.
- [ ]  **6. Empirical Command:** I know all key thesis metrics from memory:
  * Arm 2 Placebo Visual Capture: $89.50\%$ ($1,449 / 1,619$)
  * Arm 3 Conflict Visual Capture: $25.76\%$ ($417 / 1,619$)
  * Net Visual Reduction: $+63.74\text{ pp}$ ($p = 1.20 \times 10^{-215}$)
  * Paired Odds Ratio: $42.28$ | Marginal Odds Ratio: $24.57$
  * Cohen's $h$: $1.4170$ (Very Large Effect)
  * Contradiction Abstention: $13.65\%$ ($221 / 1,619$)
- [ ]  **7. Exact-Match Defense:** I can present the exact-match cross-over (Image collapses $35.6\% \to 11.7\%$; Text surges $4.7\% \to 35.8\%$) and prove that the intervention altered actual arithmetic problem solving rather than superficial vocabulary.
- [ ]  **8. State Transition Dynamics:** I can explain the $4 \times 4$ Markov migration matrix and account for the fate of all 1,449 visual items ($832$ text, $201$ abstain, $392$ visual).
- [ ]  **9. Truncation Robustness:** I can cite the sensitivity split proving that the $\approx 60\text{ to } 65\text{ pp}$ visual reduction holds across both non-truncated and truncated subsets.
- [ ]  **10. Strict Epistemic Discipline:** I know exactly what NOT to say in my defense: I will never claim "internal attention head rerouting", "feed-forward rewiring", "general safety filter", or "proof of human epistemic competence." I defend my findings strictly as a **statistically definitive behavioral prompt intervention in Qwen2.5-VL under clean typographical contradiction**.

---

## 11. Remaining Knowledge Gaps After Day 30

Even after completing this 30-day mastery curriculum, you must maintain transparent awareness of what remains beyond your current knowledge boundary. Acknowledge these limitations during your defense:

1. **Internal Mechanistic Localization:**
   *What is unknown:* Which specific Transformer layers or attention heads mediate the arbitration shift between Arm 2 and Arm 3.
   *Defense posture:* Transparently state: *"Our study is a behavioral causal intervention protocol. Localizing the internal circuit via activation patching or path patching is the immediate priority for future post-graduate work."*
2. **Cross-Architectural Universality:**
   *What is unknown:* Whether the $+63.74\text{ pp}$ shift replicates with identical magnitude in LLaVA-OneVision, InternVL-2.5, or proprietary models (GPT-4o, Gemini 1.5 Pro).
   *Defense posture:* Emphasize: *"Our primary census was conducted on Qwen2.5-VL-3B-Instruct. While our protocol provides the turnkey blueprint for cross-model evaluation, claims of universality are deliberately withheld pending cross-model execution."*
3. **Natural Photographic Ambiguity:**
   *What is unknown:* How the model arbitrates when the visual contradiction is presented in complex natural photographic scenes (e.g., visual illusions, object occlusion) rather than high-contrast rendered typographical arithmetic.
   *Defense posture:* State clearly: *"We deliberately selected rendered typographical arithmetic to eliminate perceptual noise and guarantee deterministically verifiable ground-truth integer solutions ($y^{\text{img}} \neq y^{\text{txt}}$). Extending source arbitration to natural photographic ambiguities represents an important domain expansion."*
4. **Autonomous Calibration without Explicit Directives:**
   *What is unknown:* Whether compact VLMs can be trained via preference optimization (DPO) to exhibit contradiction-conditioned abstention automatically, without requiring explicit verbalization prompts in the system turn.
   *Defense posture:* Frame this as the ultimate practical implication of your thesis: *"Our empirical findings prove that the latent capability for source arbitration exists in the model's weights and can be elicited via prompting. The next logical step for the field is distilling this verbalized behavior into native model weights via preference alignment."*

---

*This validated knowledge-hunting plan is now fully aligned with your codebase, research artifacts, statistical reports, and thesis manuscript. Execute each day sequentially, enforce the weekly mastery gates, and produce the specified deliverables.*
