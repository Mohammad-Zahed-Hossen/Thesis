

# 🚀 GPU Execution Guide for v5 Dev Pass

### ⚠️ Important Hardware Note (16 GB VRAM)

* **Compute Capability:** The RTX 5060 Ti / 4060 Ti natively supports `bfloat16` (Compute Capability $\ge 8$), satisfying our strict pre-registration requirement.
* **VRAM Capacity:**
  * **Blocks 1 to 4 (2B and 3B models):** Will run smoothly on 16 GB VRAM using `--batch_size 4`.
  * **Blocks 5 & 6 (7B model):** Takes ~16.6 GB VRAM just to load weights and requires a 24 GB+ GPU (e.g. RTX 3090/4090 or A100). **Run Blocks 1 through 4 on this 16 GB card.**

---

### Step 1: Environment Setup (One-Time)

1. Put these **5 Python files** into a single working folder (e.g., `Thesis_v5/`):

   - `harness_v4.py`
   - `score_v4.py`
   - `harness_v5.py`
   - `score_v5.py`
   - `transplant_v5.py`
2. Open a terminal (PowerShell, Command Prompt, or Bash) in that folder and run:

```bash
# 1. Install dependencies
pip install transformers accelerate datasets pillow qwen-vl-utils

# 2. Create results directory
mkdir results_v5
```

---

### Step 2: Pre-Flight Sanity Check (1 minute)

Run this quick command to verify that the chat template and vision tokens render correctly:

```bash
python harness_v5.py --print_example --split conflict --phase dev --run_tag render_check --model_id Qwen/Qwen2.5-VL-3B-Instruct
```

*If it prints the system prompt, user prompt with `Image:` and `Typed text:`, and assistant prefill ending in `The verdict.\n\n####`, everything is ready.*

---

### Step 3: Run the Experiments (Block by Block)

> [!NOTE]
> **Crash-Proof & Resumable:** Every command flushes progress to disk batch by batch. If interrupted for any reason, re-running the exact same command will automatically resume right where it stopped.

---

#### 🔹 BLOCK 1: `Qwen2.5-VL-3B` on Math Conflict (200 Dev Items)

```bash
# 1. Base Single-Source Solving (~15-20 min)
python harness_v5.py --stage base --split conflict --phase dev --model_id Qwen/Qwen2.5-VL-3B-Instruct --batch_size 4 --run_tag v5dev_conflict_base_qwen25

# 2. Donor Verdict Generation (~15-20 min)
python harness_v5.py --stage donor --split conflict --phase dev --model_id Qwen/Qwen2.5-VL-3B-Instruct --batch_size 4 --run_tag v5dev_conflict_donor_qwen25

# 3. Verdict Transplant & Log-Likelihood Margin Scoring (~25-30 min)
python transplant_v5.py --split conflict --phase dev --model_id Qwen/Qwen2.5-VL-3B-Instruct --batch_size 4 --base_file results_v5/v5dev_conflict_base_qwen25.jsonl --donor_file results_v5/v5dev_conflict_donor_qwen25.jsonl --run_tag v5dev_conflict_tp_qwen25
```

---

#### 🔹 BLOCK 2: `Qwen2-VL-2B` on Math Conflict (200 Dev Items)

```bash
# 1. Base Single-Source Solving (~10-15 min)
python harness_v5.py --stage base --split conflict --phase dev --model_id Qwen/Qwen2-VL-2B-Instruct --batch_size 4 --run_tag v5dev_conflict_base_qwen2

# 2. Donor Verdict Generation (~10-15 min)
python harness_v5.py --stage donor --split conflict --phase dev --model_id Qwen/Qwen2-VL-2B-Instruct --batch_size 4 --run_tag v5dev_conflict_donor_qwen2

# 3. Verdict Transplant & Log-Likelihood Margin Scoring (~20-25 min)
python transplant_v5.py --split conflict --phase dev --model_id Qwen/Qwen2-VL-2B-Instruct --batch_size 4 --base_file results_v5/v5dev_conflict_base_qwen2.jsonl --donor_file results_v5/v5dev_conflict_donor_qwen2.jsonl --run_tag v5dev_conflict_tp_qwen2
```

---

#### 🔹 BLOCK 3: `Qwen2.5-VL-3B` on ChartQA Conflict (30 Dev Items)

```bash
# 1. Base Single-Source Solving (~3-5 min)
python harness_v5.py --stage base --split chartqa --phase dev --model_id Qwen/Qwen2.5-VL-3B-Instruct --batch_size 4 --run_tag v5dev_chartqa_base_qwen25

# 2. Donor Verdict Generation (~3-5 min)
python harness_v5.py --stage donor --split chartqa --phase dev --model_id Qwen/Qwen2.5-VL-3B-Instruct --batch_size 4 --run_tag v5dev_chartqa_donor_qwen25

# 3. Verdict Transplant & Log-Likelihood Margin Scoring (~5-8 min)
python transplant_v5.py --split chartqa --phase dev --model_id Qwen/Qwen2.5-VL-3B-Instruct --batch_size 4 --base_file results_v5/v5dev_chartqa_base_qwen25.jsonl --donor_file results_v5/v5dev_chartqa_donor_qwen25.jsonl --run_tag v5dev_chartqa_tp_qwen25
```

---

#### 🔹 BLOCK 4: `Qwen2-VL-2B` on ChartQA Conflict (30 Dev Items)

```bash
# 1. Base Single-Source Solving (~2-4 min)
python harness_v5.py --stage base --split chartqa --phase dev --model_id Qwen/Qwen2-VL-2B-Instruct --batch_size 4 --run_tag v5dev_chartqa_base_qwen2

# 2. Donor Verdict Generation (~2-4 min)
python harness_v5.py --stage donor --split chartqa --phase dev --model_id Qwen/Qwen2-VL-2B-Instruct --batch_size 4 --run_tag v5dev_chartqa_donor_qwen2

# 3. Verdict Transplant & Log-Likelihood Margin Scoring (~4-6 min)
python transplant_v5.py --split chartqa --phase dev --model_id Qwen/Qwen2-VL-2B-Instruct --batch_size 4 --base_file results_v5/v5dev_chartqa_base_qwen2.jsonl --donor_file results_v5/v5dev_chartqa_donor_qwen2.jsonl --run_tag v5dev_chartqa_tp_qwen2
```

---


#### 🔹 BLOCK 5: `Qwen2.5-VL-7B` on Math Conflict (200 Dev Items)

```bash
# 1. Base Single-Source Solving
python harness_v5.py --stage base --split conflict --phase dev --model_id Qwen/Qwen2.5-VL-7B-Instruct --batch_size 1 --run_tag v5dev_conflict_base_qwen25_7b

# 2. Donor Verdict Generation
python harness_v5.py --stage donor --split conflict --phase dev --model_id Qwen/Qwen2.5-VL-7B-Instruct --batch_size 1 --run_tag v5dev_conflict_donor_qwen25_7b

# 3. Verdict Transplant & Log-Likelihood Margin Scoring
python transplant_v5.py --split conflict --phase dev --model_id Qwen/Qwen2.5-VL-7B-Instruct --batch_size 1 --base_file results_v5/v5dev_conflict_base_qwen25_7b.jsonl --donor_file results_v5/v5dev_conflict_donor_qwen25_7b.jsonl --run_tag v5dev_conflict_tp_qwen25_7b
```

---

#### 🔹 BLOCK 6: `Qwen2.5-VL-7B` on ChartQA Conflict (30 Dev Items)

```bash
# 1. Base Single-Source Solving
python harness_v5.py --stage base --split chartqa --phase dev --model_id Qwen/Qwen2.5-VL-7B-Instruct --batch_size 1 --run_tag v5dev_chartqa_base_qwen25_7b

# 2. Donor Verdict Generation
python harness_v5.py --stage donor --split chartqa --phase dev --model_id Qwen/Qwen2.5-VL-7B-Instruct --batch_size 1 --run_tag v5dev_chartqa_donor_qwen25_7b

# 3. Verdict Transplant & Log-Likelihood Margin Scoring
python transplant_v5.py --split chartqa --phase dev --model_id Qwen/Qwen2.5-VL-7B-Instruct --batch_size 1 --base_file results_v5/v5dev_chartqa_base_qwen25_7b.jsonl --donor_file results_v5/v5dev_chartqa_donor_qwen25_7b.jsonl --run_tag v5dev_chartqa_tp_qwen25_7b
```

### Step 4: What Your Friend Sends Back

Once the runs finish, have your friend zip and send you the **`results_v5/`** folder containing:

- All `*.jsonl` files
- All `*.manifest.json` files
- All `*.gates.json` files

### Step 5: Local Analysis (On Your PC)

Place the `results_v5/` folder into `d:\Thesis\Important\Causal Conflict Verbalization and Source Arbitration\Experiment\results_v5` and run:

```bash
cd Experiment
python analyze_v5.py --runs results_v5/v5dev_*_tp_*.jsonl --gates results_v5/v5dev_*_tp_*.gates.json --output_dir results_v5/analysis_dev
```

This will automatically calculate:

1. **Competency yield** (single-source isolation pass rate)
2. **Minimal-edit verdict pass rate**
3. **Log-likelihood margin ($\Delta\ell$)** causal steering effects
4. **Two One-Sided Equivalence Tests (TOST)** and permutation statistics.
