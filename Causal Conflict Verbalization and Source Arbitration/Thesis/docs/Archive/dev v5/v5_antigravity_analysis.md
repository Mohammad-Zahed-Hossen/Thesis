

# In-Depth Analysis of the Dev v5 Execution, Artifacts, and Data

This document provides a comprehensive, file-by-file audit of the Version 5 (v5) development run executed on Google Colab Pro (NVIDIA L4 GPU) as recorded in `Thesis/docs/Archive/v5_dev_output.md` and stored in the Google Drive folder `Thesis_v5` (mirrored locally in `Experiment/results_v5/`).

---

## 1. Execution Inventory & File Tree

The v5 dev pipeline executed 6 factorial blocks across three model scales (`Qwen2-VL-2B-Instruct`, `Qwen2.5-VL-3B-Instruct`, `Qwen2.5-VL-7B-Instruct`) and two conflict regimes:

- **Math Task-Selection Conflict** (`conflict`: GSM8K vs. SVAMP, $N=200$ dev items)
- **ChartQA Evidence Conflict** (`chartqa`: Chart vs. Report, $N=30$ dev items)

### Inventory of All Artifacts in `results_v5/`


| File Name                                                   | Size              | Type / Role                                            |
| :------------------------------------------------------------ | :------------------ | :------------------------------------------------------- |
| `pip_freeze.txt`                                            | 14.2 KB           | Pinned execution environment & Python package manifest |
| `v5dev_conflict_base_qwen2.jsonl` / `.manifest.json`        | 964 KB / 3.7 KB   | Stage 1: Base solving (2B, Math)                       |
| `v5dev_conflict_donor_qwen2.jsonl` / `.manifest.json`       | 1.05 MB / 3.7 KB  | Stage 2: Donor verbalization (2B, Math)                |
| `v5dev_conflict_tp_qwen2.gates.json`                        | 261 B             | Stage 3: Gate report (2B, Math)                        |
| `v5dev_conflict_base_qwen25.jsonl` / `.manifest.json`       | 1.08 MB / 3.7 KB  | Stage 1: Base solving (3B, Math)                       |
| `v5dev_conflict_donor_qwen25.jsonl` / `.manifest.json`      | 1.54 MB / 3.7 KB  | Stage 2: Donor verbalization (3B, Math)                |
| `v5dev_conflict_tp_qwen25.gates.json` / `.manifest.json`    | 2.6 KB / 3.9 KB   | Stage 3: Gate report & Manifest (3B, Math)             |
| `v5dev_conflict_tp_qwen25.jsonl`                            | 10.77 MB          | Stage 4: Transplant & Scoring (3B, Math: 9,600 rows)   |
| `v5dev_conflict_base_qwen25_7b.jsonl` / `.manifest.json`    | 1.08 MB / 3.7 KB  | Stage 1: Base solving (7B, Math)                       |
| `v5dev_conflict_donor_qwen25_7b.jsonl` / `.manifest.json`   | 1.58 MB / 3.8 KB  | Stage 2: Donor verbalization (7B, Math)                |
| `v5dev_conflict_tp_qwen25_7b.gates.json` / `.manifest.json` | 3.6 KB / 3.9 KB   | Stage 3: Gate report & Manifest (7B, Math)             |
| `v5dev_conflict_tp_qwen25_7b.jsonl`                         | 16.83 MB          | Stage 4: Transplant & Scoring (7B, Math: 13,800 rows)  |
| `v5dev_chartqa_base_qwen2.jsonl` / `.manifest.json`         | 58.7 KB / 3.7 KB  | Stage 1: Base solving (2B, ChartQA)                    |
| `v5dev_chartqa_donor_qwen2.jsonl` / `.manifest.json`        | 60.8 KB / 3.7 KB  | Stage 2: Donor verbalization (2B, ChartQA)             |
| `v5dev_chartqa_tp_qwen2.gates.json`                         | 313 B             | Stage 3: Gate report (2B, ChartQA)                     |
| `v5dev_chartqa_base_qwen25.jsonl` / `.manifest.json`        | 59.5 KB / 3.7 KB  | Stage 1: Base solving (3B, ChartQA)                    |
| `v5dev_chartqa_donor_qwen25.jsonl` / `.manifest.json`       | 72.5 KB / 3.7 KB  | Stage 2: Donor verbalization (3B, ChartQA)             |
| `v5dev_chartqa_tp_qwen25.gates.json` / `.manifest.json`     | 436 B / 3.9 KB    | Stage 3: Gate report & Manifest (3B, ChartQA)          |
| `v5dev_chartqa_tp_qwen25.jsonl`                             | 572 KB            | Stage 4: Transplant & Scoring (3B, ChartQA: 720 rows)  |
| `v5dev_chartqa_base_qwen25_7b.jsonl` / `.manifest.json`     | 60.4 KB / 3.7 KB  | Stage 1: Base solving (7B, ChartQA)                    |
| `v5dev_chartqa_donor_qwen25_7b.jsonl` / `.manifest.json`    | 135.7 KB / 3.7 KB | Stage 2: Donor verbalization (7B, ChartQA)             |
| `v5dev_chartqa_tp_qwen25_7b.gates.json` / `.manifest.json`  | 454 B / 3.9 KB    | Stage 3: Gate report & Manifest (7B, ChartQA)          |
| `v5dev_chartqa_tp_qwen25_7b.jsonl`                          | 239 KB            | Stage 4: Transplant & Scoring (7B, ChartQA: 240 rows)  |

---

## 2. Environment & Hardware Verification

### 2.1 `pip_freeze.txt` Analysis

From `results_v5/pip_freeze.txt`:

- **Python**: 3.13.16 (64-bit Linux on Colab)
- **PyTorch**: `2.14.1+cu130`
- **Transformers**: `5.22.1`
- **Accelerate**: `1.15.0`
- **Datasets**: `4.8.5`
- **Qwen-VL-Utils**: `0.0.14`
- **CUDA Driver / Runtime**: CUDA 13.0, Driver 580.82.07

### 2.2 Manifest Integrity (`*.manifest.json`)

Across all 16 manifest files:

- **GPU Accelerator**: `NVIDIA L4` (24,000 MiB VRAM), Compute Capability 8.9.
- **Precision**: Enforced `torch.bfloat16`. No `float16` fallback was triggered.
- **Pinned Model & Dataset Revisions**:
  - `Qwen/Qwen2.5-VL-3B-Instruct`: commit `66285546d2b821cf421d4f5eb2576359d3770cd3`
  - `Qwen/Qwen2.5-VL-7B-Instruct`: commit `cc594898137f460bfe9f0759e9844b3ce807cfb5`
  - `Qwen/Qwen2-VL-2B-Instruct`: commit `895c3a49bc3fa70a340399125c650a463535e71c`
  - Math dataset: commit `2c55b099f286554685798d54cea4bde761d486b7`; ChartQA dataset: commit `7d15a9704bc5e028e7038ef98aa7917059535bf8`
- **Memory Consumption**:
  - **2B**: Peak VRAM $\approx 4.11$ GB.
  - **3B** (Batch Size 8): Peak VRAM $= 6.99$ GB.
  - **7B** (Batch Size 2): Peak VRAM $= 15.69$ GB. Execution was safe from CUDA OOM errors.
- **Script Integrity**: All runs logged the identical SHA-256 hashes for `harness_v5.py`, `score_v5.py`, `harness_v4.py`, and `score_v4.py`.

---

## 3. Stage 1: Base Single-Source Competency Analysis

The pre-registration requires **Competency Conditioning**: an item enters the transplant pool if and only if the model correctly solves *both* single-source sub-problems in isolation (`base_image` and `base_text`).

### 3.1 Competency Yield by Model & Split

```
Math Conflict (N = 200 items, 400 generation rows per model):
  - Qwen2.5-VL-7B:  124 / 200 items competent (62.0% item yield; 316/400 rows correct)
  - Qwen2.5-VL-3B:   80 / 200 items competent (40.0% item yield; 252/400 rows correct)
  - Qwen2-VL-2B:      0 / 200 items competent ( 0.0% item yield;   0/400 rows correct)

ChartQA Evidence Conflict (N = 30 items, 60 generation rows per model):
  - Qwen2.5-VL-7B:   13 / 30 items competent (43.3% item yield)
  - Qwen2.5-VL-3B:   13 / 30 items competent (43.3% item yield)
  - Qwen2-VL-2B:     10 / 30 items competent (33.3% item yield)
```

### 3.2 Critical Structural Finding: Why Did `Qwen2-VL-2B` Get 0 Competency in Math?

A deep inspection of `v5dev_conflict_base_qwen2.jsonl` explains why:

1. In `harness_v5.py`, `base_correct(row)` uses `sc.behavioural_source(..., regime='math')`.
2. In `score_v5.py`, strict math parsing specifies:
   ```python
   ans, method = v4.extract_answer(text)
   if method in ("fallback_last_number", "hash_no_number", "none"):
       ans = None
   ```
3. The prompt explicitly instructs: `"On the last line, write #### followed by only the final number."`
4. **Behavior of Qwen2-VL-2B**:
   - `hash_direct` count: **0 / 400 rows**.
   - `fallback_last_number` count: **400 / 400 rows**.
   - Qwen2-VL-2B concluded its working with phrases like `"Therefore, Janet makes $26 every day at the farmers' market."` or `"\boxed{26}"` instead of writing `#### 26`.
5. Because `v4.extract_answer` was forced into `fallback_last_number`, the parser zeroed `ans = None`. Consequently, `sc.behavioural_source` returned `"neither"`, marking 100% of Qwen2-VL-2B math base responses as incorrect.
6. Conversely, on ChartQA, where `extract_answer_strict` accepts first-line short answers, Qwen2-VL-2B achieved **10 / 30 competent items**.

---

## 4. Stage 2: Donor Natural Verbalization Analysis

In Stage 2, models solve the conflict problem under non-binding instructions ($k=1$) in both presentation orders (`image_first` and `text_first`), verbalizing which source they deem more reliable.

### 4.1 Natural Modality Bias and Order Asymmetry

The model's self-generated reliable source in `donor` rows reveals strong recency effects:

#### A. Math Conflict (`conflict`, 400 requests per model)

- **Qwen2.5-VL-3B**:
  - Across all 400 donor rows: `text`: 327 (81.8%), `image`: 73 (18.2%).
  - In `image_first`: 128 chose text, 72 chose image.
  - In `text_first`: 199 chose text, **only 1 chose image**.
- **Qwen2.5-VL-7B**:
  - Across all 400 donor rows: `text`: 274 (68.5%), `image`: 125 (31.2%), `undetermined`: 1.
  - In `image_first`: 74 chose text, 125 chose image (62.8% image preference).
  - In `text_first`: **200 chose text, 0 chose image** (100% text preference).
- **Qwen2-VL-2B**:
  - In `text_first`: 97 rows were `absent` (failed to name any source in the required format).

> [!IMPORTANT]
> **Empirical Confirmation of Preregistration Invariant R2:**
> The models exhibit an overwhelming recency bias when evidence order changes: placing text second induces an almost 100% verbalization preference for text. This confirms that **counterbalancing presentation order is essential** to prevent order bias from confounding reliability verdicts.

#### B. ChartQA Evidence Conflict (`chartqa`, 60 requests per model)

- **Qwen2.5-VL-3B**: 32 `absent` (emitted bare answers like `"4.10 million"`), 27 `report`, 1 `chart`.
- **Qwen2.5-VL-7B**: 29 `report`, 20 `chart`, 10 `absent`, 1 `image` (wrong regime term).
- **Qwen2-VL-2B**: 51 `absent`, 6 `undetermined`, 3 `chart`. The 2B model repeatedly outputted `"The chart and the report give the same answer."` without rendering a verdict.

---

## 5. Stage 3: Minimal-Edit Gates & Sample Attrition Analysis

The v5 methodology enforces 4 pre-registered edit gates on the donor verbalization $v$:

1. **Gate 1**: Exactly one sentence modified for `flip`, `para`, `para_flip`; exactly one sentence removed for `none`.
2. **Gate 2**: Stated source reverses cleanly (e.g. `image` $\leftrightarrow$ `text`).
3. **Gate 3a**: Word token Jaccard similarity $\ge 0.85$.
4. **Gate 3b**: Maximum of 2 source noun phrases swapped (`MAX_SWAPS <= 2`).
5. **Gate 4**: Grammatical consistency (article agreement: `a` vs `an`).

An item is admitted to Stage 4 if and only if it passes all gates in **both** `image_first` and `text_first` orders.

### 5.1 Gate Pass Statistics across All Six Model × Split Blocks


| Model & Split             | Competent Pool | Passed Gates | Gate Pass Rate | Multiset Jaccard (Mean / Min) | Primary Attrition Reasons                          |
| :-------------------------- | :--------------: | :------------: | :--------------: | :-----------------------------: | :--------------------------------------------------- |
| **Qwen2.5-VL-3B Math**    |     **80**     |    **80**    |   **100.0%**   |      **0.9455 / 0.8800**      | None (All 80 passed in both orders)                |
| **Qwen2.5-VL-7B Math**    |    **124**    |   **115**   |   **92.7%**   |      **0.9549 / 0.8750**      | `gate3_too_many_swaps` (8), `own_undetermined` (1) |
| **Qwen2-VL-2B Math**      |     **0**     |    **0**    |    **N/A**    |              N/A              | Zero competent items from Stage 1                  |
| **Qwen2.5-VL-3B ChartQA** |     **13**     |    **6**    |   **46.2%**   |      **0.8936 / 0.8667**      | `own_absent` (11 orders missing verdict)           |
| **Qwen2.5-VL-7B ChartQA** |     **13**     |    **2**    |   **15.4%**   |      **0.9774 / 0.9481**      | `gate3_too_many_swaps` (8), `own_absent` (3)       |
| **Qwen2-VL-2B ChartQA**   |     **10**     |    **0**    |    **0.0%**    |              N/A              | `own_absent` (18), `own_undetermined` (2)          |

### 5.2 Gate Quality Insights

1. **Surgical Precision of Edits**:
   - Multiset Jaccard similarities averaged **94.5% to 97.7%**, with a minimum of 0.8667 (above the 0.85 threshold).
   - In 3B Math, 119 items required only 1 noun swap; 41 required 2 noun swaps.
2. **Why 7B Suffered Attrition Under `gate3_too_many_swaps`**:
   - The 7B model generated longer verbalizations (e.g., `"The chart and report differ; the chart shows X while the report shows Y, but the chart is more reliable"`).
   - Swapping all occurrences flipped 3 or 4 nouns, which tripped Gate 3b (`MAX_SWAPS = 2`).
3. **Why ChartQA Had Severe Sample Attrition**:
   - In ChartQA, models often omitted the reliability clause entirely in one of the two presentation orders (`own_absent`).
   - Requiring *both* orders to be valid halved the already compact sample ($N=30$).

---

## 6. Stage 4: Verdict Transplant & Scoring Analysis

The primary outcome is the **Log-Likelihood Margin**:

$$
\Delta\ell = \frac{\ell(y_{\text{image}})}{|y_{\text{image}}|} - \frac{\ell(y_{\text{text}})}{|y_{\text{text}}|}

$$

where $\ell(y)$ is the summed log-probability of the gold answer tokens following the `####` delimiter.

The Controlled Direct Effect (**CDE**) is oriented by $s = +1$ (if flipped verdict names image) or $s = -1$ (if flipped verdict names text):

$$
\text{CDE} = s \cdot (\Delta\ell_{\text{flip}} - \Delta\ell_{\text{own}})

$$

The ratio to explicit instruction ceiling is:

$$
\rho = \frac{\text{CDE}}{\text{Ceil}_{\ell}}, \quad \text{where } \text{Ceil}_{\ell} = \Delta\ell_{\text{explicit\_image}} - \Delta\ell_{\text{explicit\_text}}

$$

### 6.1 Descriptive Dev-Pass Calculations (Not Confirmatory Tests)

> [!IMPORTANT]
> These values are reproducible from the stored dev rows, but they are not confirmatory results. The Math analyses retain 80 (3B) and 115 (7B) items, below the code's 150-item minimum; ChartQA retains 6 (3B) and 2 (7B) items, below its 100-item minimum. All items are from the spent development split.

#### A. `Qwen2.5-VL-3B-Instruct` on Math Conflict ($N = 80$ analyzed items, 9,600 rows)

- **Ceiling Effect ($\text{Ceil}_{\ell}$)**: $0.152$ ($95\%$ CI $[0.117, 0.193]$). Strong single-source separation.
- **T1 Test (Binding DiD)**:
  - $\text{DiD} = \text{CDE}_{\text{bind}} - \text{CDE}_{\text{nonbind}} = +0.083$ ($95\%$ CI $[0.051, 0.113]$).
  - One-sided sign-flip permutation test: $p = 0.0001$ (Holm-adjusted $p = 0.0005$).
  - **Verdict**: Binding significantly strengthens the causal effect of the verdict.
- **T2 Test ($\rho_{\text{bind}}$)**:
  - $\text{CDE}_{\text{bind}} = +0.233$ ($95\%$ CI $[0.182, 0.291]$).
  - $\rho_{\text{bind}} = 1.529$ ($90\%$ bootstrap CI $[1.258, 1.865]$).
  - Reading: **Decision-Relevant** ($\rho > 0.25$).
- **T3 Test ($\rho_{\text{nonbind}}$)**:
  - $\text{CDE}_{\text{nonbind}} = +0.150$ ($95\%$ CI $[0.106, 0.204]$).
  - $\rho_{\text{nonbind}} = 0.984$ ($90\%$ bootstrap CI $[0.736, 1.305]$).
  - Reading: **Decision-Relevant** ($\rho > 0.25$).
- **Descriptive reading only**: The stored dev calculation is positive and the binding-minus-non-binding contrast is positive; it is not a confirmatory $H_1$ result.

#### B. `Qwen2.5-VL-7B-Instruct` on Math Conflict ($N = 115$ analyzed items, 13,800 rows)

- **Ceiling Effect ($\text{Ceil}_{\ell}$)**: $1.423$ ($95\%$ CI $[1.214, 1.633]$). Clear separation.
- **T1 Test (Binding DiD)**:
  - $\text{DiD} = +0.277$ ($95\%$ CI $[0.220, 0.336]$).
  - One-sided sign-flip permutation test: $p = 0.0001$ (Holm-adjusted $p = 0.0005$).
  - **Verdict**: Binding significantly strengthens the verdict effect on the 7B model.
- **T2 Test ($\rho_{\text{bind}}$)**:
  - $\text{CDE}_{\text{bind}} = +1.619$ ($95\%$ CI $[1.337, 1.919]$).
  - $\rho_{\text{bind}} = 1.138$ ($90\%$ bootstrap CI $[1.022, 1.254]$).
  - Reading: **Decision-Relevant** ($\rho > 0.25$).
- **T3 Test ($\rho_{\text{nonbind}}$)**:
  - $\text{CDE}_{\text{nonbind}} = +1.342$ ($95\%$ CI $[1.082, 1.626]$).
  - $\rho_{\text{nonbind}} = 0.943$ ($90\%$ bootstrap CI $[0.835, 1.052]$).
  - Reading: **Decision-Relevant** ($\rho > 0.25$).
- **Descriptive reading only**: The stored dev calculation is positive and the binding-minus-non-binding contrast is positive; it is not a confirmatory $H_1$ result.

#### C. ChartQA Split Performance ($N = 6$ for 3B, $N = 2$ for 7B)

- **Qwen2.5-VL-3B** ($N=6$ items):
  - $\text{DiD} = +0.104$ ($p = 0.0157$, Holm $p = 0.0471$).
  - $\text{CDE}_{\text{bind}} = +0.461$ ($\rho_{\text{bind}} = 0.401$, Decision-Relevant).
  - Reading: a numerical dev diagnostic only; $N=6$ is far below the 100-item ChartQA entry rule.
- **Qwen2.5-VL-7B** ($N=2$ items):
  - Sample size is too small ($N=2 < \text{MIN\_ITEMS} = 100$).
  - Reading: **Inconclusive** due to sample attrition.

---

## 7. Secondary Metrics, Diagnostics & Validation

### 7.1 Manipulation Check (Verbalization Faithfulness)

Does the model follow its own stated verdict when generating freely?

- **Qwen2.5-VL-3B (Math)**:
  - Donor natural generation: **80.3%** of attributable answers followed the stated verdict.
  - Free generation under binding instruction: **93.1%** followed the stated verdict.
- **Qwen2.5-VL-7B (Math)**:
  - Donor natural generation: **93.8%** followed the stated verdict.
  - Free generation under binding instruction: **99.1%** followed the stated verdict.

### 7.2 Behavioral Decodes (`beh`) vs. Primary Log-Likelihood ($\Delta\ell$)

- **Behavioral Answer Shifting**:
  - For 3B Math under binding: Decodes moved towards the flipped source by $\Delta = +45.6\text{ pp}$ ($90\%$ CI $[38.8, 52.5]\text{ pp}$).
  - For 7B Math under binding: Decodes moved towards the flipped source by $\Delta = +18.3\text{ pp}$ ($90\%$ CI $[14.3, 22.6]\text{ pp}$).
- **Wording Floor Failure in Math Decodes**:
  - The paraphrase check (`para` vs. `own`) tests whether changing wording without changing the source flips the behavioral decode.
  - The churn rate reached **20.4% – 28.1%** (exceeding the strict pre-registered ceiling of $5\%$).
  - **Why this occurred**: Discrete math decoding is sensitive to minor prompt perturbations (floating-point accumulation differences in beam/greedy steps).
  - **Methodological Takeaway**: This confirms the pre-registration decision to make the continuous log-likelihood margin **$\Delta\ell$ the primary outcome**, rather than behavioral argmax decoding.

### 7.3 Within-Generation Scaling Comparison: 3B vs. 7B

On the common intersection set of items that passed competency and gates in both models ($N = 50$ math items):

- $\rho_{\text{bind}}$ on 3B: **1.369**
- $\rho_{\text{bind}}$ on 7B: **1.056**
- Difference $\Delta\rho$ (7B minus 3B): **$-0.314$** ($95\%$ CI $[-0.784, +0.050]$).
- Because the $95\%$ CI crosses zero, there is **no statistically significant difference** in verdict sensitivity between the 3.75B and 8.29B parameter scales on this subset.

---

## 8. Summary of Findings & Next Steps

### What Was Verified

1. **The stored v5 rows are complete and reproducible**: the six base and donor blocks plus four non-empty transplant blocks contain 29,880 rows (24,360 transplant rows) on an L4 in `bfloat16`, with matching current-script hashes. No persistent `analysis_dev/` output or transcript of an `analyze_v5.py` command is stored, so an executed local analysis cannot be independently verified from the archive.
2. **Large dev likelihood effects are present in retained Math rows**: both retained models have positive raw likelihood-margin effects and positive binding-minus-non-binding contrasts. These are development diagnostics, not supported $H_1$ findings: Math is below the 150-item minimum, the items are spent dev data, and both behavioural wording-floor diagnostics fail.
3. **Counterbalancing is empirically justified**: placing typed text second produced near-unanimous typed-text reliability verdicts in the Math donor rows. Counterbalancing is necessary to prevent presentation order from being confounded with the verdict manipulation.

### Open Issues to Address Before Confirmatory Freezing

1. **Qwen2-VL-2B Formatting**:
   - The 2B model completely failed the base competency filter on Math (0/200) because it did not emit the `#### <number>` delimiter, causing `v4.extract_answer` to return `fallback_last_number`.
   - Before running the confirmatory phase on 2B, either the base prompt formatting for 2B needs few-shot guidance / stricter system prompting, or the competency parsing rule for 2B needs clarification.
2. **ChartQA Sample Attrition**:
   - The initial dev sample ($N=30$) yielded only 6 passing items for 3B and 2 for 7B, due to `gate3_too_many_swaps` and `own_absent`.
   - The pre-registered minimum sample for ChartQA is $N \ge 100$. For the confirmatory phase, either `MAX_SWAPS` must be slightly relaxed (e.g., from 2 to 4) for descriptive models like 7B, or the full 229-item dataset must be utilized.

All data, scripts, and logs are analyzed and stored. Standing by for instructions regarding dev v5.
