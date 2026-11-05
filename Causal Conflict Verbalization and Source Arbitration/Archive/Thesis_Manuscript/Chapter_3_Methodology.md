# Chapter 3: Methodology & Experimental Framework

## 3.1 Research Design

### 3.1.1 Paired Controlled Intervention Design
To investigate whether explicit conflict verbalization causally steers multimodal source arbitration, this study employs a **within-item, paired controlled factorial intervention design**. In multimodal reasoning evaluations, between-subject designs (evaluating different subsets of items under different prompt conditions) introduce item-difficulty confounding, as arithmetic complexity, visual layout, and lexical difficulty vary substantially across word problems. To eliminate between-item variance, every individual conflict item $i \in \{1, \dots, N\}$ in the evaluation census is evaluated under all experimental conditions:

$$\mathcal{D} = \{ (x_i^{\text{img}}, x_i^{\text{txt}}, y_i^{\text{img}}, y_i^{\text{txt}}) \}_{i=1}^{N}, \quad N = 1,619$$

Where $x_i^{\text{img}}$ is the rendered visual arithmetic problem, $x_i^{\text{txt}}$ is the competing textual arithmetic problem, and $y_i^{\text{img}} \neq y_i^{\text{txt}}$ represent their respective ground-truth integer solutions.

```
                    THE PAIRED FACTORIAL INTERVENTION DESIGN
                    
    Item i: Clean Image (Problem A) + Symmetrically Clean Text (Problem B)
       │
       ├───> Arm 1: Direct Baseline        (Zero-Shot Unprompted Solve)
       │
       ├───> Arm 2: Neutral Placebo        (2-Sentence Descriptive Control)
       │
       ├───> Arm 3: Conflict Intervention  (2-Sentence Conflict & Reliability Evaluation)
       │
       ├───> Arm 4a: Prefill Image         (Exploratory Forced Image Direction)
       │
       └───> Arm 4b: Prefill Text          (Exploratory Forced Text Direction)
```

### 3.1.2 The Causal Object: The Complete Prompt Intervention
A central methodological principle of this design is the precise definition of the causal object. In prior prompting literature, intervention effects are occasionally characterized as isolating "pure semantic awareness" or "internal reasoning." We explicitly reject this characterization. 

In this study, the causal entity under investigation is **the complete conflict-verbalization and source-arbitration prompt intervention** (Arm 3), compared directly against a **neutral verbalization control** (Arm 2). The intervention instructs the model to perform a multi-step task:
1. Identify whether the visual and textual sources agree or contradict;
2. Articulate which information source is considered more reliable; and
3. Solve "that problem" to yield a final numerical answer.

Because instruction-following is an inherent component of autoregressive language generation, the observed behavioral effect measures the model's response to this complete evaluative directive, rather than an isolated, unprompted cognitive state.

---

## 3.2 Dataset Construction & Curation

### 3.2.1 Benchmark Origin and Composition
The experimental benchmark is curated from `vlm-modality-research/modality-conflict-arbitration-v2`, an open-access multimodal evaluation suite derived from standard arithmetic reasoning benchmarks: **GSM8K** (Grade School Math 8K) and **SVAMP** (Simple Variations on Arithmetic Math Problems). 

The full repository comprises 12,952 cross-modal pairs partitioned across two transmission channels (`channel = image` and `channel = text`) and four degradation levels ($\lambda \in \{0, 1, 2, 3\}$). To isolate cognitive source arbitration from perceptual failure, this study evaluates the **complete population census of pristine image-conflict pairs**:
* **Channel:** `image` (the primary problem is rendered visually; the competing problem is supplied as text).
* **Degradation Level:** $\lambda = 0$ (completely clean, uncorrupted, high-resolution rendering).
* **Total Census Size:** Exactly **$N = 1,619$ items** (comprising 1,319 GSM8K multi-step reasoning pairs and 300 SVAMP single/dual-step reasoning pairs).

```
               POPULATION CENSUS DERIVATION & FILTERING
               
      Total Dataset: vlm-modality-research/modality-conflict-arbitration-v2
                                (12,952 items)
                                      │
            ┌─────────────────────────┴─────────────────────────┐
            ▼                                                   ▼
     channel = text                                      channel = image
      (6,476 items)                                       (6,476 items)
                                                                │
                                            ┌───────────────────┴───────────────────┐
                                            ▼                                       ▼
                                     Degradation 1–3                         Degradation 0
                                     (4,857 corrupted)                       (Clean Pristine)
                                                                                    │
                                                                                    ▼
                                                                        CANONICAL EVALUATION CENSUS
                                                                                (N = 1,619)
                                                                        • 1,319 GSM8K Multi-Step
                                                                        •   300 SVAMP Dual-Step
```

### 3.2.2 Inclusion and Exclusion Criteria
1. **Pristine Legibility Criterion:** Only items with `degradation_level == 0` are included. Items subject to Gaussian blur, salt-and-pepper noise, downsampling, or typographical dropout ($\lambda \in \{1, 2, 3\}$) are excluded. This guarantees that visual illegibility cannot act as an unmodeled physical confounder.
2. **Ground-Truth Determinism:** Every included item provides an unambiguous, verified ground-truth integer or float answer for both the image problem ($y_i^{\text{img}}$) and the text problem ($y_i^{\text{txt}}$).
3. **Mutual Exclusivity:** All pairs satisfy $y_i^{\text{img}} \neq y_i^{\text{txt}}$, ensuring that the two sources cannot be satisfied simultaneously by a single answer.

### 3.2.3 Conflict Construction
Each benchmark item is constructed by pairing an arithmetic word problem rendered into a high-contrast typographical image with a syntactically matched but numerically conflicting problem presented in the prompt text. The conflict mechanisms fall into three categories:
* **Numerical Replacement:** Retaining character names and scenario context while altering key numerical values (e.g., Image: "Janet has 16 ducks..."; Text: "Janet has 24 ducks...").
* **Entity / Contextual Swap:** Maintaining arithmetic structure while altering entities and relations (e.g., Image describes calculating cupcake sales; Text describes calculating bolt requirements for robes).
* **Relational Inversion:** Altering operations (e.g., "half as many" versus "twice as many").

Images are rendered as standard RGB PNG files formatted with black text on white backgrounds, ensuring high visual clarity across standard vision transformer patch sizes.

---

## 3.3 Model Architecture & Inference Configuration

### 3.3.1 Primary Evaluated Model
The primary model under investigation is **Qwen2.5-VL-3B-Instruct** (`Qwen/Qwen2.5-VL-3B-Instruct`). Qwen2.5-VL is an autoregressive vision-language model featuring:
* **Architectural Parameters:** 36 Transformer layers, hidden dimension of 2,048, and 16 attention heads.
* **Native Dynamic Resolution Vision Transformer:** Employs dynamic 2D patch grids with a base patch size of $14 \times 14$ pixels, grouped into $28 \times 28$ spatial tokens, allowing variable aspect ratio processing without artificial distortion.
* **Pretrained & Instruction-Tuned:** Equipped with native multi-turn chat templates and instruction alignment.

### 3.3.2 Hardware Environment & Runtime Optimizations
Inference was conducted on Google Colab Pro instances equipped with **NVIDIA T4 GPUs** (16 GB VRAM, Turing architecture, compute capability `sm_75`) running Ubuntu 22.04 LTS, CUDA 13.0, and PyTorch 2.11.0. To execute 8,095 forward passes across 1,619 items within a standard compute allocation, four specific runtime optimizations were implemented:

1. **Hardware-Aware Precision Selection:** On Turing architectures (`sm_75`), bfloat16 lacks native Tensor Core acceleration and triggers software emulation. The inference harness queries device compute capability and executes in native `torch.float16`, maximizing hardware Tensor Core throughput.
2. **PyTorch Scaled Dot-Product Attention (SDPA):** PyTorch 2.x fused FlashAttention/Memory-Efficient attention kernels (`attn_implementation="sdpa"`) were enforced, reducing attention memory complexity from $\mathcal{O}(N^2)$ to $\mathcal{O}(N)$.
3. **Dynamic Resolution Constraints:** Image preprocessing was constrained to `min_pixels = 100,352` ($128 \times 28 \times 28$) and `max_pixels = 200,704` ($256 \times 28 \times 28$), capping visual sequence length at approximately 256 vision tokens per item while preserving typographical legibility.
4. **CUDA 13 / NVRTC Dynamic JIT Patch:** On PyTorch 2.11 with CUDA 13.0, the Qwen2.5-VL vision processor invokes integer tensor reductions (`image_grid_thw.prod(-1)`). On CUDA 13, this operation triggers a runtime NVRTC JIT compilation that fails if `libnvrtc-builtins.so` is missing from system dynamic link paths. Harness v3.0 injects an in-memory monkey-patch intercepting `.prod(-1)` on 2D/3D integer tensors and evaluating them on the CPU in $< 1\,\mu\text{s}$, eliminating driver crashes.

```python
# In-Memory PyTorch CUDA 13 NVRTC JIT Fallback Patch
_orig_tensor_prod = torch.Tensor.prod

def _safe_tensor_prod(self, *args, **kwargs):
    if self.is_cuda and self.dtype in (torch.int64, torch.int32, torch.int16, torch.int8):
        return _orig_tensor_prod(self.cpu(), *args, **kwargs).to(self.device)
    return _orig_tensor_prod(self, *args, **kwargs)

torch.Tensor.prod = _safe_tensor_prod
```

### 3.3.3 Generation Hyperparameters & Decoding Configuration
All generation was performed deterministically using **greedy decoding**:
* `do_sample = False`
* `temperature = None`
* `top_p = None`
* `repetition_penalty = 1.0`

Greedy decoding guarantees that output distributions reflect the maximum-likelihood trajectory under the given prompt, ensuring $100\%$ reproducibility.

---

## 3.4 Experimental Conditions & Prompt Specifications

Each item in the census is evaluated across four distinct conditions comprising five evaluation arms:

### 3.4.1 Literal Prompt Specifications

| Arm Identifier | Condition Classification | Literal Prompt Template / Prefix | Generation Token Budget |
| :--- | :--- | :--- | :---: |
| **Arm 1** | Direct Zero-Shot Baseline | `Look at the image and read the text problem below.\n{text_question}\n\nSolve the problem. Conclude with: #### <answer>\n` | 80 tokens |
| **Arm 2** | Neutral Placebo Control | `Look at the image and read the text problem below.\n{text_question}\n\nIn two sentences, neutrally describe what is presented in the image and what is stated in the text without comparing them. Then solve the problem. Conclude with: #### <answer>\n` | 200 tokens |
| **Arm 3** | Conflict Verbalization (Treatment) | `Look at the image and read the text problem below.\n{text_question}\n\nIn two sentences, state whether the image and the text agree or contradict each other, and explain which source you consider more reliable. Then solve that problem. Conclude with: #### <answer>\n` | 200 tokens |
| **Arm 4a** | Exploratory Rationale Prefill (Image) | User Prompt: Arm 1 template.<br>Assistant Prefill: `The image and text contradict each other because they present different problems. Following the image problem, the answer is: #### ` | 20 tokens |
| **Arm 4b** | Exploratory Rationale Prefill (Text) | User Prompt: Arm 1 template.<br>Assistant Prefill: `The image and text describe consistent premises. Following the text problem, the answer is: #### ` | 20 tokens |

### 3.4.2 Distinction Between Primary and Exploratory Arms
* **Primary Experimental Arms (Arms 1, 2, and 3):** Constitute the confirmatory behavioral factorial design. Arm 1 measures unprompted zero-shot source selection. Arm 2 provides the critical length-matched descriptive control. Arm 3 evaluates the causal effect of the conflict-verbalization prompt.
* **Secondary Exploratory Arms (Arms 4a and 4b):** Adapt the counterfactual rationale prefilling methodology of Lanham et al. (2023). By pre-populating the assistant turn in the key-value (KV) cache, Arm 4 directly measures whether the model's answer generation is causally bound to an externally injected rationale in the absence of intermediate scratchpad tokens.

---

## 3.5 Operational Definitions & Classification Framework

To evaluate model outputs with scientific rigor, the evaluation pipeline employs a **dual-track classification engine**: (1) semantic entity-based choice classification and (2) deterministic ground-truth exact matching.

```
                     DUAL-TRACK EVALUATION PIPELINE
                     
                      Raw Model Generated Text
                                 │
                 ┌───────────────┴───────────────┐
                 ▼                               ▼
       [ Track 1: Semantic ]           [ Track 2: Numerical ]
      Entity & Abstention Parse         Answer String Extraction
                 │                               │
                 ▼                               ▼
       • img_unique hits               • Regex: r"####\s*([+-]?\d+)"
       • txt_unique hits               • Match against y_img
       • Abstention regex              • Match against y_txt
                 │                               │
                 ▼                               ▼
     Categorical State:               Binary Ground-Truth Matches:
     - follows_image_problem          - exact_img (True/False)
     - follows_text_problem           - exact_txt (True/False)
     - abstains
     - ambiguous
```

### 3.5.1 Answer Extraction Protocol
Numerical answers are parsed deterministically from the generated output text using a two-stage regular expression extractor:
1. **Primary Extraction:** Matches the explicit delimiter:
   $$\text{Regex: } \verb|####\s*([+-]?\d[\d,]*\.?\d*)|$$
2. **Fallback Extraction:** If the delimiter is missing (e.g., due to mid-sentence truncation), the parser extracts the final numerical token appearing in the text:
   $$\text{Regex: } \verb|[+-]?\d[\d,]*\.?\d*|$$
3. Extracted strings are normalized by stripping commas and trailing periods.

### 3.5.2 Definition of Categorical Behavioral States
For each generation, the model's behavior is classified into one of four mutually exclusive states:

1. **Follows Image Problem (`follows_image_problem`):**  
   The model's reasoning chain or final calculation demonstrates that it solved the problem depicted in the image. Operationally defined when:
   * The count of unique image-problem entities exceeds unique text-problem entities by $\ge 2$ ($E_{\text{img}} > E_{\text{txt}} + 1$); or
   * $E_{\text{img}} > E_{\text{txt}}$ and the extracted answer matches $y^{\text{img}}$; or
   * Entity counts are tied ($E_{\text{img}} = E_{\text{txt}}$), but the extracted answer matches $y^{\text{img}}$ and does not match $y^{\text{txt}}$.

2. **Follows Text Problem (`follows_text_problem`):**  
   The model's reasoning chain or final calculation demonstrates that it solved the problem stated in the text prompt. Operationally defined when:
   * Unique text-problem entities exceed unique image-problem entities by $\ge 2$ ($E_{\text{txt}} > E_{\text{img}} + 1$); or
   * $E_{\text{txt}} > E_{\text{img}}$ and the extracted answer matches $y^{\text{txt}}$; or
   * Entity counts are tied ($E_{\text{txt}} = E_{\text{img}}$), but the extracted answer matches $y^{\text{txt}}$ and does not match $y^{\text{img}}$.

3. **Contradiction-Conditioned Abstention (`abstains`):**  
   The model explicitly recognizes the contradiction and refuses to produce a numerical calculation. Detected via deterministic case-insensitive regex matching against verified refusal indicators:
   $$\mathcal{P}_{\text{abstain}} = \left\{ \begin{array}{l} \text{"cannot be determined"}, \text{"no numerical answer"}, \text{"no need to provide"}, \\ \text{"cannot determine"}, \text{"not possible to"}, \text{"no direct connection"}, \\ \text{"cannot be answered"}, \text{"not enough information"}, \text{"unrelated problems"}, \\ \text{"contradict each other, so"}, \text{"different problems, so there is no"} \end{array} \right\}$$

4. **Ambiguous (`ambiguous`):**  
   The output cannot be reliably mapped to either source (e.g., tied entity counts with neither answer matched, or severe truncation prior to entity introduction).

### 3.5.3 Entity Extraction Methodology
To prevent keyword noise, domain entities are extracted using part-of-speech heuristic filtering:
* Proper nouns ($\verb|[A-Z][a-z]+(?:'s)?|$) with character length $> 2$.
* Content nouns ($\verb|[a-z]{4,}|$) excluding a curated 60-word stop list of common mathematical and English functional terms (e.g., *calculate, solve, problem, total, hours, days, each, more, make, give*).
* Unique entity sets are computed via set differences:
  $$\mathcal{E}_{\text{img\_unique}} = \mathcal{E}_{\text{img}} \setminus \mathcal{E}_{\text{text}}, \qquad \mathcal{E}_{\text{txt\_unique}} = \mathcal{E}_{\text{text}} \setminus \mathcal{E}_{\text{img}}$$

### 3.5.4 Source-Conditioned Exact-Match Execution
Independent of entity presence, the output is directly scored against ground truth:
* $\text{exact\_img}_i = \mathbb{I}(\text{ans}_i = y_i^{\text{img}})$
* $\text{exact\_txt}_i = \mathbb{I}(\text{ans}_i = y_i^{\text{txt}})$

This metric provides uncalibrated, mathematically verifiable confirmation of which problem the model executed.

---

## 3.6 Primary Outcome & Statistical Analysis Framework

### 3.6.1 Primary Outcome Variable
The primary confirmatory outcome is the **binary visual-capture indicator**:
$$V_i^{(k)} = \mathbb{I}\left( \text{choice}_i^{(k)} = \text{"follows\_image\_problem"} \right) \in \{0, 1\}$$
where $k \in \{\text{Arm 1}, \text{Arm 2}, \text{Arm 3}\}$ denotes the experimental condition for item $i$.

### 3.6.2 The Paired Confirmatory Test: McNemar's Test
Because every item $i \in \{1, \dots, N\}$ is evaluated under both Arm 2 (Neutral Control) and Arm 3 (Conflict Treatment), observations are **paired repeated measures**. Standard independent tests (such as Pearson's Chi-Square or two-sample Fisher's exact test) assume sample independence and violate statistical validity by treating $N$ paired items as $2N$ independent subjects.

Accordingly, the primary statistical hypothesis test is **McNemar's Paired Test with Edwards' Continuity Correction** applied to the $2 \times 2$ within-subject transition table:

```
                      PAIRED CONTINGENCY TABLE FORMAT
                      
                                  Arm 3 (Treatment)
                              Visual (1)     Non-Visual (0)
                           ┌──────────────┬──────────────────┐
               Visual (1)  │      a       │        b         │
   Arm 2                   │ (Persistent) │ (Arbitrated/Abs) │
   (Control)               ├──────────────┼──────────────────┤
               Non-Vis (0) │      c       │        d         │
                           └──────────────┴──────────────────┘
```

Where:
* $a$: Items visually captured under both conditions.
* $b$: Discordant items visually captured under Arm 2, but arbitrated to text, abstained, or ambiguous under Arm 3.
* $c$: Discordant items non-visual under Arm 2, but visually captured under Arm 3.
* $d$: Items non-visual under both conditions.

The test statistic is formulated with Edwards' continuity correction:
$$\chi^2_{\text{McNemar}} = \frac{(|b - c| - 1)^2}{b + c}, \quad \text{df} = 1$$
The exact two-sided $p$-value is computed directly via the complementary error function:
$$p = \text{erfc}\left( \sqrt{\frac{\chi^2_{\text{McNemar}}}{2}} \right)$$

### 3.6.3 Effect Size Metrics & Confidence Intervals
To quantify the substantive magnitude of the intervention, four standardized effect sizes are reported:

1. **Net Visual Capture Reduction ($\Delta_{\text{visual}}$):**
   $$\Delta_{\text{visual}} = P_{\text{vis}}(\text{Arm 2}) - P_{\text{vis}}(\text{Arm 3}) = \frac{a + b}{N} - \frac{a + c}{N} = \frac{b - c}{N}$$
   The 95% confidence interval is computed using the Newcombe paired score method.

2. **Paired Discordance Odds Ratio ($OR_{\text{paired}}$):**
   $$OR_{\text{paired}} = \frac{b}{c}$$
   With 95% confidence interval computed via Woolf's method:
   $$\text{CI}_{95\%} = \exp\left( \ln(OR_{\text{paired}}) \pm 1.95996 \sqrt{\frac{1}{b} + \frac{1}{c}} \right)$$

3. **Relative Risk of Visual Capture ($RR$):**
   $$RR = \frac{P_{\text{vis}}(\text{Arm 3})}{P_{\text{vis}}(\text{Arm 2})} = \frac{a + c}{a + b}$$

4. **Cohen's $h$ Standardized Effect Size:**
   $$h = 2 \arcsin\left(\sqrt{P_{\text{vis}}(\text{Arm 2})}\right) - 2 \arcsin\left(\sqrt{P_{\text{vis}}(\text{Arm 3})}\right)$$
   Convention: $h = 0.20$ (small), $h = 0.50$ (medium), $h \ge 0.80$ (large).

---

## 3.7 Secondary Evaluation Protocols

### 3.7.1 Source-Conditioned Exact-Match Crossover Analysis
To confirm that source arbitration reflects actual mathematical problem solving, we evaluate the proportion of outputs achieving exact integer matches against $y^{\text{img}}$ and $y^{\text{txt}}$ across Arm 2 and Arm 3. If an intervention merely triggers random generation drift, exact match rates on both problems would drop toward zero. A simultaneous surge in text exact match and collapse in image exact match confirms problem-solving redirection.

### 3.7.2 Contradiction-Conditioned Abstention Analysis
The proportion of items classified as `abstains` in Arm 3 is evaluated relative to baseline (Arm 1) and placebo (Arm 2). Abstentions are audited qualitatively to verify that they correspond to semantic recognition of contradictory premises.

### 3.7.3 Paired $4 \times 4$ State-Transition Dynamics
We construct a full $4 \times 4$ state migration matrix mapping every item's transition:
$$\mathcal{M}_{r, s} = \sum_{i=1}^{N} \mathbb{I}\left( \text{choice}_i^{(\text{Arm 2})} = r \;\land\; \text{choice}_i^{(\text{Arm 3})} = s \right)$$
where $r, s \in \{\text{Image}, \text{Text}, \text{Abstain}, \text{Ambiguous}\}$. This isolates the specific trajectories of items suffering visual capture in the control condition.

### 3.7.4 Exploratory Rationale Prefill Analysis (Arm 4)
We evaluate the proportion of items in which opposing prefilled prefixes (Arm 4a vs. Arm 4b) produce:
* Invariant final answers ($\text{ans}_i^{(4a)} = \text{ans}_i^{(4b)}$);
* Divergent final answers ($\text{ans}_i^{(4a)} \neq \text{ans}_i^{(4b)}$);
* Exact-match steering delta ($\Delta_{\text{prefill}} = \text{exact\_txt}^{(4b)} - \text{exact\_txt}^{(4a)}$).

---

## 3.8 Output Truncation & Robustness Sensitivity Protocol

### 3.8.1 Operational Definition of Truncation
In autoregressive generation, complex multi-step reasoning can exceed allocated token limits before outputting the final delimiter. In the production harness, an item is operationally classified as **truncated** if generated length reaches within 1 token of the generation ceiling:
$$\text{truncated}_i = \mathbb{I}\left( \text{actual\_tokens}_i \ge \text{max\_new\_tokens} - 1 \right)$$
For Arms 2 and 3, where `max_new_tokens = 200`, truncation is flagged when $\text{actual\_tokens}_i \ge 199$.

### 3.8.2 Sensitivity Partitioning Protocol
Because $37.6\%$ of Arm 2 and $44.2\%$ of Arm 3 reach 199+ tokens due to extensive multi-step arithmetic chains, we enforce a mandatory **robustness sensitivity analysis** that evaluates the primary arbitration shift across three isolated cohorts:
1. **The Arm-Specific Non-Truncated Cohort:** Items terminating naturally at `EOS` prior to token 199 in each respective arm.
2. **The Strict Paired Non-Truncated Cohort:** The subset of items ($N = 632$) that terminated naturally prior to token 199 in *both* Arm 2 and Arm 3.
3. **The Truncated Cohort:** Items reaching the 200-token ceiling.

This protocol verifies whether the arbitration effect survives when token ceiling constraints are entirely absent.

---

## 3.9 Threats to Validity & Experimental Controls

To ensure defensibility during thesis examination, potential validity threats and their corresponding experimental controls are explicitly documented:

```
+----------------------------------------------------------------------------------------------------+
|                                    VALIDITY THREATS & CONTROLS                                     |
+------------------------------------+--------------------------------+------------------------------+
| Threat to Validity                 | Potential Confound             | Experimental Control Applied |
+------------------------------------+--------------------------------+------------------------------+
| 1. Test-Time Compute Confounder    | Longer CoT generation allows   | Arm 2 placebo matches token  |
|                                    | more autoregressive compute.   | generation depth (158 tok vs |
|                                    |                                | 169 tok).                    |
| 2. Prompt Length Confounder        | Longer prompt triggers         | Arm 2 prompt (36 words) is   |
|                                    | different attention patterns.  | length-matched to Arm 3      |
|                                    |                                | (38 words).                  |
| 3. Context Recency Bias            | Model follows text in Arm 1    | Arm 2 forces a descriptive   |
|                                    | because text prompt is last.   | preamble, reversing recency  |
|                                    |                                | to 89.5% visual capture.     |
| 4. Task Structure Asymmetry        | Arm 3 says "solve that         | Transparently acknowledged as|
|                                    | problem"; Arm 2 says "solve    | part of the complete prompt  |
|                                    | the problem."                  | intervention.                |
| 5. Pretraining Memorization        | Model memorized GSM8K answers. | Symmetric competition: both  |
|                                    |                                | sources are GSM8K problems;  |
|                                    |                                | memorization prior is equal. |
| 6. Mechanistic Overclaiming        | Assuming behavioral shift      | Explicit boundary: no internal|
|                                    | proves attention routing.      | activations or circuits      |
|                                    |                                | claimed.                     |
+------------------------------------+--------------------------------+------------------------------+
```

---

## 3.10 Reproducibility & Software Provenance

All code, data, and configuration parameters are organized for deterministic reproduction:

* **Codebase Repository:** All execution scripts reside in `Finalize Topic/Pilot/`.
  * Production inference harness: `production_experiment_harness_v3.py`.
  * Hypothesis testing suite: `statistical_analysis.py`.
* **Execution Environment:** PyTorch 2.11.0, Transformers 4.49.0, Datasets 3.2.0, Accelerate 1.3.0, Pillow 10.4.0.
* **Random Seed:** Globally fixed at `seed = 42`.
* **Raw Execution Provenance:**
  * Full JSON record: `Experiment_Result/full_experiment_results v3.0.json` (76,095 lines, containing complete prompt inputs, generated texts, token counts, and execution timestamps).
  * Tabular checkpoint: `Experiment_Result/experiment_checkpoint v3.0.csv` (8,096 logged rows).
  * Automated LaTeX export: `Experiment_Result/thesis_contingency_table v3.0.tex`.
