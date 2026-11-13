# 🚀 Google Colab Pro Execution Guide for v5 Dev Pass

> [!WARNING]
> **Deprecated. Use [`Experiment/RUNBOOK_v5.md`](../../../Experiment/RUNBOOK_v5.md).** This copy is kept as the record of what the v5 dev pass followed. It is incomplete in three ways:
>
> - Cell 3 runs the render check for `--split conflict` only. The three `--split chartqa` checks were never run.
> - The analysis command in Step 4 lacked `--base` and `--donor`, which drops the manipulation check and the relative-uncertainty strata. It is corrected below.
> - It has no ChartQA `--max_pixels` step and no `Rscript` step.

> **Workspace:** Causal Conflict Verbalization and Source Arbitration
> **Study:** Version 5 (v5) Verdict Transplant & Log-Likelihood Margin Scoring
> **Hardware Target:** Google Colab Pro (NVIDIA A100 40/80GB or L4 24GB)
> **Pre-Registered Requirements:** Full `bfloat16` precision, Compute Capability $\ge 8$, 24GB+ VRAM

---

## ⚠️ Critical Setup Guidelines (Read Before Starting)

### 1. GPU Selection in Colab Pro

Go to **Runtime** $\rightarrow$ **Change runtime type**:

* **Hardware accelerator:** Select **A100 GPU** (recommended) or **L4 GPU**.
* **GPU type:** Standard or High-RAM.
* ❌ **DO NOT SELECT T4 or V100:** These legacy GPUs lack native `bfloat16` (compute capability < 8) and fall back to `float16`. `harness_v5.py` will intentionally abort with an error to preserve pre-registered numerical precision.
* ❌ **DO NOT SELECT TPU (v5e/v6e):** Hugging Face Vision-Language models (`Qwen-VL`) require standard CUDA kernels.

---

### 2. Eliminating Disconnect Losses (Google Drive Mount)

> [!IMPORTANT]
> **Never upload code directly to `/content/`!**
> If Colab disconnects, files in `/content/` are permanently wiped. By mounting Google Drive, your Python scripts and partial results live safely on Drive. If disconnected, simply reconnect, mount Drive, and resume—**zero re-uploading and zero lost progress**.

---

## 🛠️ Step 1: Google Drive Staging (One-Time Setup)

1. Open your [Google Drive](https://drive.google.com).
2. Create a folder named: `Thesis_v5` inside your Drive root (`MyDrive/Thesis_v5/`).
3. Drag and drop these **5 Python files** from your local machine (`Experiment/`) into that Google Drive `Thesis_v5/` folder:
   - `harness_v4.py`
   - `score_v4.py`
   - `harness_v5.py`
   - `score_v5.py`
   - `transplant_v5.py`

---

## 📓 Step 2: Colab Notebook Setup Cells

Open a new Colab notebook, ensure your runtime is set to **A100 GPU**, and run these cells:

### Cell 1: Mount Drive & Set Working Directory

```python
from google.colab import drive
import os

# Mount Google Drive
drive.mount('/content/drive')

# Navigate to your persistent folder
WORK_DIR = '/content/drive/MyDrive/Thesis_v5'
os.makedirs(WORK_DIR, exist_ok=True)
os.chdir(WORK_DIR)

print("Current Working Directory:", os.getcwd())
!ls -la
```

*(Verify you see the 5 Python files listed).*

---

### Cell 2: Install Pinned Dependencies & Check GPU

```bash
!pip install -q transformers accelerate datasets pillow qwen-vl-utils

# Verify GPU name and compute capability
!nvidia-smi

# Record environment package versions
!mkdir -p results_v5
!pip freeze > results_v5/pip_freeze.txt
```

*(Confirm `nvidia-smi` shows an NVIDIA A100 or L4).*

---

### Cell 3: Pre-Flight Chat Template Render Check (1 minute)

Confirm that the real Hugging Face tokenizer places vision tokens and assistant prefills in the exact pre-registered positions:

```bash
!python harness_v5.py --print_example --split conflict --phase dev --run_tag render_check --model_id Qwen/Qwen2.5-VL-3B-Instruct
!python harness_v5.py --print_example --split conflict --phase dev --run_tag render_check --model_id Qwen/Qwen2-VL-2B-Instruct
!python harness_v5.py --print_example --split conflict --phase dev --run_tag render_check --model_id Qwen/Qwen2.5-VL-7B-Instruct
```

*Verification Check: Output must show `<|vision_start|><|image_pad|><|vision_end|>` after `Image:` or `Chart:`, followed by the assistant prefill `The verdict.\n\n####`.*

---

## ⚡ Step 3: Run the 6 Dev Blocks

> [!TIP]
> **Recommended Batch Sizes:**
>
> * **On A100 (40/80 GB):** Use `--batch_size 8` for all models (including 7B).
> * **On L4 (24 GB):** Use `--batch_size 8` for 2B and 3B, and `--batch_size 2` for 7B.

---

### 🔹 BLOCK 1: `Qwen2.5-VL-3B` on Math Conflict (200 Dev Items)

```bash
# 1. Base Single-Source Competency Filter (~10-15 min)
!python harness_v5.py --stage base --split conflict --phase dev --model_id Qwen/Qwen2.5-VL-3B-Instruct --batch_size 8 --run_tag v5dev_conflict_base_qwen25

# 2. Donor Natural Verdict Generation (~10-15 min)
!python harness_v5.py --stage donor --split conflict --phase dev --model_id Qwen/Qwen2.5-VL-3B-Instruct --batch_size 8 --run_tag v5dev_conflict_donor_qwen25

# 3. Verdict Transplant & Log-Likelihood Margin Scoring (~15-20 min)
!python transplant_v5.py --split conflict --phase dev --model_id Qwen/Qwen2.5-VL-3B-Instruct --batch_size 8 \
  --base_file results_v5/v5dev_conflict_base_qwen25.jsonl \
  --donor_file results_v5/v5dev_conflict_donor_qwen25.jsonl \
  --run_tag v5dev_conflict_tp_qwen25
```

---

### 🔹 BLOCK 2: `Qwen2-VL-2B` on Math Conflict (200 Dev Items)

```bash
# 1. Base Single-Source Solving (~8-12 min)
!python harness_v5.py --stage base --split conflict --phase dev --model_id Qwen/Qwen2-VL-2B-Instruct --batch_size 8 --run_tag v5dev_conflict_base_qwen2

# 2. Donor Verdict Generation (~8-12 min)
!python harness_v5.py --stage donor --split conflict --phase dev --model_id Qwen/Qwen2-VL-2B-Instruct --batch_size 8 --run_tag v5dev_conflict_donor_qwen2

# 3. Verdict Transplant & Log-Likelihood Margin Scoring (~15-20 min)
!python transplant_v5.py --split conflict --phase dev --model_id Qwen/Qwen2-VL-2B-Instruct --batch_size 8 \
  --base_file results_v5/v5dev_conflict_base_qwen2.jsonl \
  --donor_file results_v5/v5dev_conflict_donor_qwen2.jsonl \
  --run_tag v5dev_conflict_tp_qwen2
```

---

### 🔹 BLOCK 3: `Qwen2.5-VL-3B` on ChartQA Evidence Conflict (30 Dev Items)

```bash
# 1. Base Single-Source Solving (~2-3 min)
!python harness_v5.py --stage base --split chartqa --phase dev --model_id Qwen/Qwen2.5-VL-3B-Instruct --batch_size 8 --run_tag v5dev_chartqa_base_qwen25

# 2. Donor Verdict Generation (~2-3 min)
!python harness_v5.py --stage donor --split chartqa --phase dev --model_id Qwen/Qwen2.5-VL-3B-Instruct --batch_size 8 --run_tag v5dev_chartqa_donor_qwen25

# 3. Verdict Transplant & Log-Likelihood Margin Scoring (~4-6 min)
!python transplant_v5.py --split chartqa --phase dev --model_id Qwen/Qwen2.5-VL-3B-Instruct --batch_size 8 \
  --base_file results_v5/v5dev_chartqa_base_qwen25.jsonl \
  --donor_file results_v5/v5dev_chartqa_donor_qwen25.jsonl \
  --run_tag v5dev_chartqa_tp_qwen25
```

---

### 🔹 BLOCK 4: `Qwen2-VL-2B` on ChartQA Evidence Conflict (30 Dev Items)

```bash
# 1. Base Single-Source Solving (~2-3 min)
!python harness_v5.py --stage base --split chartqa --phase dev --model_id Qwen/Qwen2-VL-2B-Instruct --batch_size 8 --run_tag v5dev_chartqa_base_qwen2

# 2. Donor Verdict Generation (~2-3 min)
!python harness_v5.py --stage donor --split chartqa --phase dev --model_id Qwen/Qwen2-VL-2B-Instruct --batch_size 8 --run_tag v5dev_chartqa_donor_qwen2

# 3. Verdict Transplant & Log-Likelihood Margin Scoring (~3-5 min)
!python transplant_v5.py --split chartqa --phase dev --model_id Qwen/Qwen2-VL-2B-Instruct --batch_size 8 \
  --base_file results_v5/v5dev_chartqa_base_qwen2.jsonl \
  --donor_file results_v5/v5dev_chartqa_donor_qwen2.jsonl \
  --run_tag v5dev_chartqa_tp_qwen2
```

---

### 🔹 BLOCK 5: `Qwen2.5-VL-7B` on Math Conflict (200 Dev Items)

> **L4 GPU Configuration:** Configured below with `--batch_size 2` to safely fit within L4's 24GB VRAM.
> *(If running on A100 40/80GB in the future, you can change `--batch_size 2` to `--batch_size 8` for faster throughput).*

```bash
# 1. Base Single-Source Solving (~20-25 min)
!python harness_v5.py --stage base --split conflict --phase dev --model_id Qwen/Qwen2.5-VL-7B-Instruct --batch_size 2 --run_tag v5dev_conflict_base_qwen25_7b

# 2. Donor Verdict Generation (~20-25 min)
!python harness_v5.py --stage donor --split conflict --phase dev --model_id Qwen/Qwen2.5-VL-7B-Instruct --batch_size 2 --run_tag v5dev_conflict_donor_qwen25_7b

# 3. Verdict Transplant & Log-Likelihood Margin Scoring (~30-40 min)
!python transplant_v5.py --split conflict --phase dev --model_id Qwen/Qwen2.5-VL-7B-Instruct --batch_size 2 \
  --base_file results_v5/v5dev_conflict_base_qwen25_7b.jsonl \
  --donor_file results_v5/v5dev_conflict_donor_qwen25_7b.jsonl \
  --run_tag v5dev_conflict_tp_qwen25_7b
```

---

### 🔹 BLOCK 6: `Qwen2.5-VL-7B` on ChartQA Evidence Conflict (30 Dev Items)

> **L4 GPU Configuration:** Configured below with `--batch_size 2` for L4 24GB.
> *(If running on A100 40/80GB in the future, you can change `--batch_size 2` to `--batch_size 8`).*

```bash
# 1. Base Single-Source Solving (~4-6 min)
!python harness_v5.py --stage base --split chartqa --phase dev --model_id Qwen/Qwen2.5-VL-7B-Instruct --batch_size 2 --run_tag v5dev_chartqa_base_qwen25_7b

# 2. Donor Verdict Generation (~4-6 min)
!python harness_v5.py --stage donor --split chartqa --phase dev --model_id Qwen/Qwen2.5-VL-7B-Instruct --batch_size 2 --run_tag v5dev_chartqa_donor_qwen25_7b

# 3. Verdict Transplant & Log-Likelihood Margin Scoring (~6-8 min)
!python transplant_v5.py --split chartqa --phase dev --model_id Qwen/Qwen2.5-VL-7B-Instruct --batch_size 2 \
  --base_file results_v5/v5dev_chartqa_base_qwen25_7b.jsonl \
  --donor_file results_v5/v5dev_chartqa_donor_qwen25_7b.jsonl \
  --run_tag v5dev_chartqa_tp_qwen25_7b
```

---

## 🔄 Disconnect Recovery Protocol

If Colab disconnects or times out at any moment:

1. Re-open the notebook and select your **A100** or **L4** runtime.
2. Run **Cell 1** (`drive.mount(...)` and `os.chdir('/content/drive/MyDrive/Thesis_v5')`).
3. Run **Cell 2** (`pip install ...`).
4. Re-run the command that was interrupted.
   - It will inspect the existing `.jsonl` file in your Drive and **instantly resume from the exact batch it left off**. No work is duplicated or lost.

---

## 📊 Step 4: Local Statistical Analysis

Once all 6 blocks finish on Google Colab:

1. All result files are already safely stored in your Google Drive at `MyDrive/Thesis_v5/results_v5/`.
2. Download that `results_v5/` folder to your local PC:
   `d:\Thesis\Important\Causal Conflict Verbalization and Source Arbitration\Experiment\results_v5\`
3. Run the complete local analysis script on your PC:

```bash
cd Experiment
python analyze_v5.py --runs results_v5/v5dev_*_tp_*.jsonl --gates results_v5/v5dev_*_tp_*.gates.json --base results_v5/v5dev_*_base_*.jsonl --donor results_v5/v5dev_*_donor_*.jsonl --output_dir results_v5/analysis_dev
```

This generates:

* `results_v5/analysis_dev/analysis_v5.md` & `.json` (Competency yield, edit-gate pass rates, log-likelihood margins $\Delta\ell$, TOST tests).
* `results_v5/analysis_dev/long_v5.csv` (Full dataset exported for mixed-effects regression in R).
