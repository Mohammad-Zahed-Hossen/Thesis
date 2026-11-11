# 🚀 GPU & Local Execution Guide for v4 (End-to-End)

> **Workspace:** Causal Conflict Verbalization and Source Arbitration  
> **Study:** Version 4 (v4) Methodological Redesign & Causal Transplant  
> **Reference File:** [`Experiment/RUNBOOK_v4.md`](file:///d:/Thesis/Important/Causal%20Conflict%20Verbalization%20and%20Source%20Arbitration/Experiment/RUNBOOK_v4.md)  
> **Target Models:** `Qwen/Qwen2.5-VL-3B-Instruct`, `Qwen/Qwen2-VL-2B-Instruct`  

---

## 📌 Executive Summary of v4 Architecture

Version 4 (v4) systematically resolves every confound and heuristic failure identified during the v3 pilot audit:
1. **Causal Direction ($m$ vs. $z$):** Crosses instructions ($z$) with model verbalizations ($m$) via prefilled transplants to distinguish causal steering from post-hoc rationalization.
2. **Repetition Penalty Isolation:** Disentangles the default `repetition_penalty = 1.05` (which penalized typed text and artificially inflated visual capture) from true baseline arbitration (`repetition_penalty = 1.0`).
3. **Chain-of-Thought (CoT) Preservation:** Enforces explicit step-by-step reasoning before concluding with `#### <answer>` to eliminate answer-only collapse.
4. **Dev vs. Confirmatory Partitioning:** Tunes prompts and thresholds exclusively on 200 dev items, leaving confirmatory test items completely untouched.
5. **Exact Statistical Rigor:** Uses exact problem-clustered paired McNemar tests and exports long-format data for crossed mixed-effects models in R (`lme4`).

---

## Phase 1: Local Pre-GPU Verification & Human Coding (Ryzen / CPU)

These steps run entirely locally on your PC without requiring a CUDA GPU.

### 1.1 Run the Full Test Suite
Verify that all unit tests, chat templates, and scoring regexes pass:
```bash
cd Experiment
python -m unittest tests.test_v4
```
*(All 114 unit tests must report `OK`).*

### 1.2 Verify v3 Audit Reproduction
Ensure the stored v3 data reproduces the audit metrics exactly:
```bash
python reanalyze_v3.py --check --output_dir results_v3/reanalysis_v3
python statistical_analysis.py --results_file "results_v3/full_experiment_results v3.0.json" --output_dir results_v3/stats_v3_paired
```

### 1.3 Human Coding Protocol (Inter-Rater Reliability)
1. **Blind Sampling (Already generated in `Experiment/coding_v3/`):**
   - Provide `coding_v3/coder_A.csv`, `coding_v3/coder_B.csv`, and `coding_v3/CODEBOOK.md` to two independent coders.
   - **Do not open** `coding_v3/KEY_do_not_open.csv` until coding is finished.
2. **Evaluate Agreement & Scorer Accuracy:**
   Once both coders have filled their sheets, evaluate Cohen's Kappa ($\kappa$) and scorer calibration:
   ```bash
   python sample_for_coding.py evaluate --coder_a coding_v3/coder_A.csv --coder_b coding_v3/coder_B.csv --key coding_v3/KEY_do_not_open.csv
   ```

---

## Phase 2: GPU Environment Setup (Google Colab / Dedicated GPU)

For any GPU session (Google Colab T4/V100/A100 or local NVIDIA GPU $\ge 12$ GB VRAM):

### 2.1 File Staging
Upload the following **3 core Python files** into the working root directory:
* `harness_v4.py`
* `transplant_v4.py`
* `score_v4.py`

### 2.2 Dependency Installation
```bash
# 1. Install dependencies
pip install transformers accelerate datasets pillow qwen-vl-utils

# 2. Initialize results directory
mkdir -p results_v4
pip freeze > results_v4/pip_freeze.txt
```

---

## Phase 3: Pre-Flight Smoke Test (8 Items)

Run a fast smoke test to confirm GPU loading, SDPA attention, image processing, and chat template execution:
```bash
python harness_v4.py --phase dev --arm_set core --limit 8 --run_tag smoke
```
*Verification Check:* Open `results_v4/smoke.jsonl`. Confirm the model loaded without errors and that `base_image` correctly reads and solves the rendered arithmetic problem.

---

## Phase 4: Development Phase (`dev2` Suite, 200 Items)

The dev pass tunes prompt phrasing, measures the repetition-penalty effect, and verifies transplant fidelity on spent dev items.

> [!NOTE]
> **Crash-Proof & Resumable:** All scripts flush outputs to disk batch by batch. If interrupted or disconnected, re-running the exact same command automatically resumes by key.

### Block 4A: Core 15 Arms with CoT Reasoning (`repetition_penalty = 1.0`)
```bash
python harness_v4.py --phase dev --arm_set core --run_tag dev2_qwen25
```
*Time Estimate:* ~1h 50m on T4 GPU (3,000 requests across 15 arms).

### Block 4B: Repetition Penalty Check (`repetition_penalty = 1.05`)
```bash
python harness_v4.py --phase dev --arm_set penalty_check --repetition_penalty 1.05 --run_tag dev2_qwen25_rp105
```
*Time Estimate:* ~25m on T4 GPU (600 requests across the 3 v3 arms).

### Block 4C: Mediator Transplant Run
```bash
python transplant_v4.py --phase dev --donor_file results_v4/dev2_qwen25.jsonl --run_tag dev2_transplant_qwen25
```
*Time Estimate:* ~1h 35m on T4 GPU (2,800 requests across 14 cells).

### Block 4D: Local Quality Gate Audit
Download `results_v4/dev2_*.jsonl` to your local machine and run:
```bash
cd Experiment
python analyze_v4.py --runs results_v4/dev2_qwen25.jsonl results_v4/dev2_transplant_qwen25.jsonl results_v4/dev2_qwen25_rp105.jsonl --gates --output_dir results_v4/analysis_dev2
```

---

## Phase 5: Confirmatory Phase (Frozen Test Split)

> [!IMPORTANT]
> **Freeze Before Execution:** The confirmatory split contains unspent, unseen test items. The pre-registration contrast specification and `--max_new_tokens 512` must be frozen before executing this phase. No prompt changes are permitted after this begins.

```bash
# 1. Confirmatory Core Arms on Qwen2.5-VL-3B
python harness_v4.py --phase confirm --arm_set core --max_new_tokens 512 --run_tag confirm_qwen25

# 2. Confirmatory Mediator Transplant
python transplant_v4.py --phase confirm --max_new_tokens 512 --donor_file results_v4/confirm_qwen25.jsonl --run_tag transplant_qwen25

# 3. Confirmatory Penalty Check
python harness_v4.py --phase confirm --arm_set penalty_check --repetition_penalty 1.05 --max_new_tokens 512 --run_tag confirm_qwen25_rp105
```

---

## Phase 6: Replication & External Validity

To prove cross-model generalization and benchmark robustness, replicate across a second architecture and a second modality conflict regime.

### 6.1 Model Replication: `Qwen/Qwen2-VL-2B-Instruct`
```bash
# Core arms on 2B model
python harness_v4.py --phase confirm --arm_set replication_model --model_id Qwen/Qwen2-VL-2B-Instruct --max_new_tokens 512 --run_tag confirm_qwen2

# Transplant on 2B model
python transplant_v4.py --phase confirm --model_id Qwen/Qwen2-VL-2B-Instruct --max_new_tokens 512 --donor_file results_v4/confirm_qwen2.jsonl --run_tag transplant_qwen2
```

### 6.2 Benchmark Replication: ChartQA Evidence Conflict
```bash
# ChartQA Core Arms on Qwen2.5-VL-3B
python harness_v4.py --split chartqa --phase all --arm_set chartqa --max_new_tokens 512 --run_tag chartqa_qwen25

# ChartQA Transplant on Qwen2.5-VL-3B
python transplant_v4.py --split chartqa --phase all --max_new_tokens 512 --donor_file results_v4/chartqa_qwen25.jsonl --run_tag transplant_chartqa_qwen25
```
*(Note: ChartQA loads 230 rows and drops `conflict_id = 45`, leaving 229 analyzed items matching the literature standard).*

---

## Phase 7: Variance Estimation (Paraphrase & Sampling)

Since greedy decoding ($\text{temperature} = 0$) has no sampling variance, variance is measured across instruction paraphrases and random seeds:

```bash
# Paraphrase phrasing variance
python harness_v4.py --phase dev --arm_set paraphrase --paraphrase 1 --run_tag para1_qwen25
python harness_v4.py --phase dev --arm_set paraphrase --paraphrase 2 --run_tag para2_qwen25

# Sampling stochasticity variance
python harness_v4.py --phase dev --arm_set paraphrase --do_sample --seed 1 --run_tag sample1_qwen25
python harness_v4.py --phase dev --arm_set paraphrase --do_sample --seed 2 --run_tag sample2_qwen25
```

---

## Phase 8: Final Statistical Analysis & Mixed-Effects Modeling

Download all confirmatory `.jsonl` runs into your local `Experiment/results_v4/` directory.

### 8.1 Primary Local Report & Dataset Export
```bash
cd Experiment
python analyze_v4.py \
  --runs results_v4/confirm_qwen25.jsonl \
         results_v4/transplant_qwen25.jsonl \
         results_v4/confirm_qwen25_rp105.jsonl \
         results_v4/confirm_qwen2.jsonl \
         results_v4/transplant_qwen2.jsonl \
         results_v4/chartqa_qwen25.jsonl \
         results_v4/transplant_chartqa_qwen25.jsonl \
  --output_dir results_v4/analysis \
  --export_long
```

### 8.2 Crossed Mixed-Effects Regression in R (`lme4`)
The script exports `results_v4/analysis/long.csv`. Fit the crossed mixed model in R:
```R
library(lme4)

data <- read.csv("results_v4/analysis/long.csv")
model <- glmer(
  chose_text ~ instruction * verbalization + (1 | item_id) + (1 | prompt_paraphrase),
  data = data,
  family = binomial(link = "logit")
)
summary(model)
```

---

## 📊 Scientific Interpretation Matrix

| Observed Pattern in Confirmatory Run | Methodological Meaning | Thesis Conclusion |
|:---|:---|:---|
| **$m$ moves the answer while $z$ is fixed** in the stated direction | Stated conflict verbalization causally steers output choices | **Verbalization is causally faithful** (Steering Effect confirmed). |
| **$z$ moves the answer while $m$ is fixed**; $m$ has no effect | Output shift is driven solely by user instruction prompts | **Verbalization is post-hoc commentary** (Rationalization confirmed). |
| `filler` matches `direct`, while description order flips source | Visual capture in v3 was an artifact of prompt wording | v3 "visual capture" was an artifact of the placebo prompt. |
| Same-meaning prefills (`eq_a` vs `eq_b`) change answers as much as $m$ | Model output is unstable across syntactic paraphrases | Effect is driven by surface wording sensitivity, not semantic content. |
| Repetition penalty 1.05 shows $+35$ pp image shift vs 1.0 | Repetition penalty repels model from repeating prompt tokens | Confirms v3's visual capture was partly an optimization artifact. |
