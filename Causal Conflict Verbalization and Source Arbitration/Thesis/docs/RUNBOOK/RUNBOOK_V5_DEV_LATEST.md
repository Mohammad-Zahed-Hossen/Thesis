# Google Colab Pro End-to-End Execution Guide: `v5dev_latest` (Option 3 Full Fresh Pass)

This step-by-step runbook executes a full fresh v5 dev pass (`Option 3: v5dev_latest`) end to end on Google Colab Pro after the pre-freeze parser (`score_v5.py`), blinding-hygiene (`.gitignore` + `preflight_v5.py`), and duplicate-run (`analyze_v5.py`) patches, and closes the remaining GPU pre-freeze checks (`F1` and `F4 / R8.4`).

- **Canonical short reference:** [`Experiment/RUNBOOK_v5.md`](../../../Experiment/RUNBOOK_v5.md)
- **Pre-registration design spec:** [`Docs/PREREGISTRATION_VERDICT_TRANSPLANT.md`](../../../Docs/PREREGISTRATION_VERDICT_TRANSPLANT.md)
- **Hardware & precision rules:** Use an **NVIDIA L4 (23,034 MiB / 24 GB)** or **NVIDIA A100 (40/80 GB)** GPU (`Compute Capability >= 8.0`, `>= 22 GiB` usable VRAM, `bfloat16` precision). **Never use a T4 or V100** — `harness_v5.py` refuses `float16`.
- **Dev scope reminder:** Dev runs execute on the spent dev pools (`200` GSM8K/SVAMP Math items and `30` ChartQA-Conflict items). Nothing in this runbook produces confirmatory data.

---

## Unattended Overnight Execution Summary

- **What you must stay awake for (~2–3 minutes):** Only **Cell 1** (clicking the Google Drive OAuth permission popup), **Cell 2** (`preflight_v5.py --check_gpu`), and **Cell 3** (automated render gate). Once Cell 3 prints `ALL 6 RENDER CHECKS PASSED AUTOMATICALLY.`, you can leave **Runtime -> Run all** running overnight.
- **What `Experiment/*.py` already enforces automatically in code:**
  - `preflight_v5.py --check_gpu`: GPU compute capability `>= 8.0`, VRAM `>= 22.0 GiB`, exact pinned package versions, `8/8` script SHA-256 hashes, and preregistration pin/template/lexicon consistency.
  - `harness_v5.HFBackend`: refuses non-`torch.bfloat16` loads (`check_dtype`), verifies `render_chat` prefill suffix integrity (`RuntimeError`), verifies ChartQA pinned item counts (`230` raw -> `229` analysed), splits batches in half automatically on `cuda.OutOfMemoryError` (`_safe`), flushes + `os.fsync`s every batch, repairs truncated trailing JSONL lines on resume (`ensure_trailing_newline`), and returns exit code `1` (`report_missing`) if any request is missing.
- **What the fail-fast Colab wrappers below add for overnight safety:**
  - In IPython/Colab, multi-line `!python ...` cells do **not** halt subsequent commands or cells when a subprocess exits non-zero.
  - **Cell 1** defines `run_checked(...)` (streams live output and raises `RuntimeError` immediately on any unexpected non-zero exit code) and `assert_jsonl_rows(...)` (verifies `base` and `donor` JSONL row counts before `transplant_v5.py` starts).
  - **Cell 3** programmatically asserts every render-gate check on `--print_example` stdout so you do not have to inspect 6 long prompts manually.
  - **Cells 4–10** pass `allow_zero_passed_tag` only on ChartQA transplant where `passed == 0` in `.gates.json` (exit code `2`) is an expected possible gate outcome, while still halting on any other error.
  - **Cell 11** runs hard `assert` checks on `F1` (`verdict_nll_tokens > 0`, `verdict_span_exact`, `none` nulls, `boundary_mismatch <= 1%`) and manifest `resolved_model_commit`.

---

## Step 0: Local Pre-Launch Commit & Blinding Hygiene (Before Uploading to Drive)

> [!CAUTION]
> **Make the GitHub repository Private before sharing any coding sheets.**
> Untracking the `KEY_*` sheets via `git rm --cached` removes them from future commits only; historical commits (`5b57529` and earlier) still contain those files. Before giving `Experiment/coding_v5/` sheets to Coder A and Coder B, toggle `Mohammad-Zahed-Hossen/Thesis` to **Private** on GitHub (`Settings -> General -> Danger Zone -> Change repository visibility -> Make private`).

Before uploading scripts to Google Drive, confirm your working tree has no uncommitted edits to `Experiment/` or `Docs/PREREGISTRATION_VERDICT_TRANSPLANT.md` (and no tracked `KEY_*` files) so every `.manifest.json` records clean, committed script SHA-256 hashes (established at commit `328c8af`+). Run in PowerShell from `d:\Thesis\Important\Causal Conflict Verbalization and Source Arbitration`:

```powershell
cd "d:\Thesis\Important\Causal Conflict Verbalization and Source Arbitration"
git status -sb
python -B Experiment/preflight_v5.py
```

If you have local changes to commit (such as this runbook), stage only project files, verify `git status -sb` shows no `KEY_*` files and no sibling-folder changes outside this directory, then commit and push:

```powershell
git add .
git status -sb
git commit -m "Update end-to-end v5dev_latest Colab execution runbook"
git push github main
git push origin main
```

---

## Step 1: Google Drive Staging (`MyDrive/Thesis_v5/`)

1. Open Google Drive and navigate to `MyDrive/Thesis_v5/` (create it if missing).
2. **Isolate prior dev outputs cleanly:**
   - **Option 3 (Full Fresh Pass — recommended):** If `MyDrive/Thesis_v5/results_v5/` already exists, rename it to `results_v5_prev_backup`, then create a fresh empty `MyDrive/Thesis_v5/results_v5/` folder.
   - *(Optional Option 2 — Smart Refresh only: keep existing `v5dev_*_base_*.jsonl` and `v5dev_*_donor_*.jsonl` in `results_v5/` and move only `v5dev_*_tp_*` to `results_v5_prev_backup/`.)*
3. Upload the **committed versions** of all **8 core Python scripts** from [`Experiment/`](../../../Experiment/) into `MyDrive/Thesis_v5/`:
   - `harness_v4.py`
   - `score_v4.py`
   - `harness_v5.py`
   - `score_v5.py`
   - `transplant_v5.py`
   - `sample_v5_for_coding.py`
   - `analyze_v5.py`
   - `preflight_v5.py`
4. Upload [`Docs/PREREGISTRATION_VERDICT_TRANSPLANT.md`](../../../Docs/PREREGISTRATION_VERDICT_TRANSPLANT.md) to `MyDrive/Thesis_v5/PREREGISTRATION_VERDICT_TRANSPLANT.md`.
5. Upload [`Experiment/results_v5/pip_freeze.txt`](../../../Experiment/results_v5/pip_freeze.txt) to `MyDrive/Thesis_v5/results_v5/pip_freeze.txt` so `preflight_v5.py --check_gpu` verifies exact package versions in flat Drive mode.

---

## Step 2: Colab Notebook Setup & Pre-Flight Cells (Cells 1–3)

Open a new Colab Pro notebook with an **L4 GPU** or **A100 GPU** runtime.

### Cell 1 — Mount Drive, Verify Staged Files & Define Fail-Fast Helpers

```python
from google.colab import drive
import json
import os
import subprocess
import sys

drive.mount('/content/drive')

WORK_DIR = '/content/drive/MyDrive/Thesis_v5'
os.makedirs(os.path.join(WORK_DIR, 'results_v5'), exist_ok=True)
os.chdir(WORK_DIR)

print("Current Working Directory:", os.getcwd())

REQUIRED_FILES = [
    "harness_v4.py",
    "score_v4.py",
    "harness_v5.py",
    "score_v5.py",
    "transplant_v5.py",
    "sample_v5_for_coding.py",
    "analyze_v5.py",
    "preflight_v5.py",
    "PREREGISTRATION_VERDICT_TRANSPLANT.md",
    "results_v5/pip_freeze.txt",
]
missing_files = [p for p in REQUIRED_FILES if not os.path.exists(p)]
if missing_files:
    raise FileNotFoundError(f"Missing staged files in {WORK_DIR}: {missing_files}")
print(f"All {len(REQUIRED_FILES)} staged files verified.")


def run_checked(cmd: str, allow_zero_passed_tag: str | None = None) -> None:
    """Run a shell command with live streaming output and halt immediately on unexpected failure."""
    print(f"\n>>> {cmd}", flush=True)
    proc = subprocess.Popen(
        cmd,
        shell=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        text=True,
        bufsize=1,
    )
    assert proc.stdout is not None
    for line in proc.stdout:
        sys.stdout.write(line)
        sys.stdout.flush()
    rc = proc.wait()
    if rc != 0:
        if allow_zero_passed_tag and rc == 2:
            gpath = os.path.join("results_v5", f"{allow_zero_passed_tag}.gates.json")
            if os.path.exists(gpath):
                gates = json.load(open(gpath, encoding="utf-8"))
                if gates.get("passed") == 0:
                    print(
                        f"[INFO] {allow_zero_passed_tag}: passed == 0 "
                        f"(expected possible gate outcome; fails={gates.get('fail_reasons')}). Continuing.",
                        flush=True,
                    )
                    return
        raise RuntimeError(f"Command failed (exit={rc}): {cmd}")


def assert_jsonl_rows(path: str, expected_rows: int) -> None:
    """Verify prerequisite JSONL exists and has exact expected valid row count."""
    if not os.path.exists(path):
        raise FileNotFoundError(f"Prerequisite JSONL missing: {path}")
    count = 0
    with open(path, encoding="utf-8") as fh:
        for line in fh:
            if line.strip():
                json.loads(line)
                count += 1
    if count != expected_rows:
        raise RuntimeError(f"{path}: expected {expected_rows} rows, found {count}")
    print(f"[OK] {path}: {count}/{expected_rows} rows verified.", flush=True)
```

### Cell 2 — Install Exact Pinned Dependencies & Run `preflight_v5.py --check_gpu`

```python
run_checked(
    "pip install -q torch==2.14.1+cu130 transformers==5.22.1 accelerate==1.15.0 "
    "datasets==4.8.5 pillow==11.3.0 qwen-vl-utils==0.0.14"
)
run_checked("nvidia-smi")
run_checked("python -B preflight_v5.py --check_gpu")
```

*(Pass criterion: exits `0` and prints `[preflight_v5] OK`, `Scripts verified: 8/8`, and `GPU: ...` with Compute Capability `>= 8.0` and `>= 22 GiB` VRAM.)*

### Cell 3 — Automated Render Gate (`--print_example`) on Both `conflict` and `chartqa` (`F1 Part A`)

```python
import subprocess

MODELS = [
    "Qwen/Qwen2.5-VL-3B-Instruct",
    "Qwen/Qwen2-VL-2B-Instruct",
    "Qwen/Qwen2.5-VL-7B-Instruct",
]

for split in ("conflict", "chartqa"):
    img_hdr = "Image: " if split == "conflict" else "Chart: "
    txt_hdr = "Typed text:\n" if split == "conflict" else "Report:\n"
    vis = "<|vision_start|><|image_pad|><|vision_end|>"
    for model_id in MODELS:
        cmd = [
            "python", "-B", "harness_v5.py",
            "--print_example", "--split", split, "--phase", "dev",
            "--run_tag", "render_check", "--model_id", model_id,
        ]
        res = subprocess.run(cmd, capture_output=True, text=True, check=True)
        out = res.stdout
        assert "===== image.size:" in out, f"Missing image.size header for {split} {model_id}"
        if split == "chartqa":
            assert "800x557 (445600 px; min_pixels=100352, max_pixels=200704)" in out, (
                f"Unexpected ChartQA image.size line for {model_id}:\n{out[:400]}"
            )
        assert "Source A" not in out and "Source B" not in out, f"Forbidden Source A/B in {split} {model_id}"
        m1 = "===== image_first (binding, k=1) ====="
        m2 = "===== text_first (binding, k=1) ====="
        assert m1 in out and m2 in out, f"Missing order sections in {split} {model_id}"
        img_part, txt_part = out.split(m1, 1)[1].split(m2, 1)
        for label, part in (("image_first", img_part), ("text_first", txt_part)):
            assert f"{img_hdr}{vis}" in part, f"Vision tag misaligned in {split} {model_id} {label}"
            assert part.rstrip().endswith("The verdict.\n\n####"), f"Bad prefill suffix in {split} {model_id} {label}"
        assert img_part.index(vis) < img_part.index(txt_hdr), f"Wrong order in image_first ({split} {model_id})"
        assert txt_part.index(txt_hdr) < txt_part.index(vis), f"Wrong order in text_first ({split} {model_id})"
        print(f"[PASS] render_check: split={split} | model={model_id}")

print("\nALL 6 RENDER CHECKS PASSED AUTOMATICALLY.")
```

*(Once this cell prints `ALL 6 RENDER CHECKS PASSED AUTOMATICALLY.`, you can leave the remaining cells running unattended overnight via **Runtime -> Run after** or **Run all**.)*

---

## Step 3: Run the 6 Dev Blocks at Default `max_pixels=200704` (Cells 4–9)

> [!TIP]
> - **Batch sizes:** On **L4 (24 GB)**, keep `--batch_size 8` for `3B`/`2B` and `--batch_size 2` for `7B`. On **A100 (40/80 GB)**, you can set `BS_7B = 8` (replace `--batch_size 2` with `--batch_size 8` in Cells 8, 9, and 10).
> - **Option 2 note:** Only if reusing prior `base` and `donor` files, comment out the `base` and `donor` `run_checked(...)` lines and keep `assert_jsonl_rows(...)` + `transplant_v5.py`.

### Cell 4 — Block 1: `Qwen2.5-VL-3B` on Math Conflict (`200` Dev Items, `BS=8`)

Expected under updated `structured` parser on prior dev data: `95 -> 95` (`competent -> passed`).

```python
run_checked(
    "python -B harness_v5.py --stage base --split conflict --phase dev "
    "--model_id Qwen/Qwen2.5-VL-3B-Instruct --batch_size 8 --run_tag v5dev_conflict_base_qwen25"
)
assert_jsonl_rows("results_v5/v5dev_conflict_base_qwen25.jsonl", 800)

run_checked(
    "python -B harness_v5.py --stage donor --split conflict --phase dev "
    "--model_id Qwen/Qwen2.5-VL-3B-Instruct --batch_size 8 --run_tag v5dev_conflict_donor_qwen25"
)
assert_jsonl_rows("results_v5/v5dev_conflict_donor_qwen25.jsonl", 800)

run_checked(
    "python -B transplant_v5.py --split conflict --phase dev "
    "--model_id Qwen/Qwen2.5-VL-3B-Instruct --batch_size 8 "
    "--base_file results_v5/v5dev_conflict_base_qwen25.jsonl "
    "--donor_file results_v5/v5dev_conflict_donor_qwen25.jsonl "
    "--run_tag v5dev_conflict_tp_qwen25"
)
```

### Cell 5 — Block 2: `Qwen2-VL-2B` on Math Conflict (`200` Dev Items, Diagnostic-Only D3, `BS=8`)

`Qwen/Qwen2-VL-2B-Instruct` is diagnostic-only (D3; `0/200` Math competency under `structured`), so run `--gates_only` on transplant to write `gates.json` cleanly in `< 5 s`.

```python
run_checked(
    "python -B harness_v5.py --stage base --split conflict --phase dev "
    "--model_id Qwen/Qwen2-VL-2B-Instruct --batch_size 8 --run_tag v5dev_conflict_base_qwen2"
)
assert_jsonl_rows("results_v5/v5dev_conflict_base_qwen2.jsonl", 800)

run_checked(
    "python -B harness_v5.py --stage donor --split conflict --phase dev "
    "--model_id Qwen/Qwen2-VL-2B-Instruct --batch_size 8 --run_tag v5dev_conflict_donor_qwen2"
)
assert_jsonl_rows("results_v5/v5dev_conflict_donor_qwen2.jsonl", 800)

run_checked(
    "python -B transplant_v5.py --gates_only --split conflict --phase dev "
    "--model_id Qwen/Qwen2-VL-2B-Instruct --batch_size 8 "
    "--base_file results_v5/v5dev_conflict_base_qwen2.jsonl "
    "--donor_file results_v5/v5dev_conflict_donor_qwen2.jsonl "
    "--run_tag v5dev_conflict_tp_qwen2"
)
```

### Cell 6 — Block 3: `Qwen2.5-VL-3B` on ChartQA Conflict (`30` Dev Items, `BS=8`)

Expected at `max_pixels=200704`: `13 -> 5` (`competent -> passed` after answer-leakage gate).

```python
run_checked(
    "python -B harness_v5.py --stage base --split chartqa --phase dev "
    "--model_id Qwen/Qwen2.5-VL-3B-Instruct --batch_size 8 --run_tag v5dev_chartqa_base_qwen25"
)
assert_jsonl_rows("results_v5/v5dev_chartqa_base_qwen25.jsonl", 120)

run_checked(
    "python -B harness_v5.py --stage donor --split chartqa --phase dev "
    "--model_id Qwen/Qwen2.5-VL-3B-Instruct --batch_size 8 --run_tag v5dev_chartqa_donor_qwen25"
)
assert_jsonl_rows("results_v5/v5dev_chartqa_donor_qwen25.jsonl", 120)

run_checked(
    "python -B transplant_v5.py --split chartqa --phase dev "
    "--model_id Qwen/Qwen2.5-VL-3B-Instruct --batch_size 8 "
    "--base_file results_v5/v5dev_chartqa_base_qwen25.jsonl "
    "--donor_file results_v5/v5dev_chartqa_donor_qwen25.jsonl "
    "--run_tag v5dev_chartqa_tp_qwen25",
    allow_zero_passed_tag="v5dev_chartqa_tp_qwen25",
)
```

### Cell 7 — Block 4: `Qwen2-VL-2B` on ChartQA Conflict (`30` Dev Items, Diagnostic-Only D3, `BS=8`)

Expected under current gates: `0` passed items; run `--gates_only` to record `gates.json`.

```python
run_checked(
    "python -B harness_v5.py --stage base --split chartqa --phase dev "
    "--model_id Qwen/Qwen2-VL-2B-Instruct --batch_size 8 --run_tag v5dev_chartqa_base_qwen2"
)
assert_jsonl_rows("results_v5/v5dev_chartqa_base_qwen2.jsonl", 120)

run_checked(
    "python -B harness_v5.py --stage donor --split chartqa --phase dev "
    "--model_id Qwen/Qwen2-VL-2B-Instruct --batch_size 8 --run_tag v5dev_chartqa_donor_qwen2"
)
assert_jsonl_rows("results_v5/v5dev_chartqa_donor_qwen2.jsonl", 120)

run_checked(
    "python -B transplant_v5.py --gates_only --split chartqa --phase dev "
    "--model_id Qwen/Qwen2-VL-2B-Instruct --batch_size 8 "
    "--base_file results_v5/v5dev_chartqa_base_qwen2.jsonl "
    "--donor_file results_v5/v5dev_chartqa_donor_qwen2.jsonl "
    "--run_tag v5dev_chartqa_tp_qwen2"
)
```

### Cell 8 — Block 5: `Qwen2.5-VL-7B` on Math Conflict (`200` Dev Items, `BS=2` on L4)

Expected under updated `structured` parser: `154 -> 140` (`competent -> passed`). Check `peak_vram_gb` in the first 7B manifest.

```python
run_checked(
    "python -B harness_v5.py --stage base --split conflict --phase dev "
    "--model_id Qwen/Qwen2.5-VL-7B-Instruct --batch_size 2 --run_tag v5dev_conflict_base_qwen25_7b"
)
assert_jsonl_rows("results_v5/v5dev_conflict_base_qwen25_7b.jsonl", 800)

run_checked(
    "python -B harness_v5.py --stage donor --split conflict --phase dev "
    "--model_id Qwen/Qwen2.5-VL-7B-Instruct --batch_size 2 --run_tag v5dev_conflict_donor_qwen25_7b"
)
assert_jsonl_rows("results_v5/v5dev_conflict_donor_qwen25_7b.jsonl", 800)

run_checked(
    "python -B transplant_v5.py --split conflict --phase dev "
    "--model_id Qwen/Qwen2.5-VL-7B-Instruct --batch_size 2 "
    "--base_file results_v5/v5dev_conflict_base_qwen25_7b.jsonl "
    "--donor_file results_v5/v5dev_conflict_donor_qwen25_7b.jsonl "
    "--run_tag v5dev_conflict_tp_qwen25_7b"
)
```

### Cell 9 — Block 6: `Qwen2.5-VL-7B` on ChartQA Conflict (`30` Dev Items, `BS=2` on L4)

Expected at `max_pixels=200704`: `13 -> 0` (`competent -> passed` under answer-leakage and swap gates; `allow_zero_passed_tag` lets the notebook proceed cleanly if `passed == 0`).

```python
run_checked(
    "python -B harness_v5.py --stage base --split chartqa --phase dev "
    "--model_id Qwen/Qwen2.5-VL-7B-Instruct --batch_size 2 --run_tag v5dev_chartqa_base_qwen25_7b"
)
assert_jsonl_rows("results_v5/v5dev_chartqa_base_qwen25_7b.jsonl", 120)

run_checked(
    "python -B harness_v5.py --stage donor --split chartqa --phase dev "
    "--model_id Qwen/Qwen2.5-VL-7B-Instruct --batch_size 2 --run_tag v5dev_chartqa_donor_qwen25_7b"
)
assert_jsonl_rows("results_v5/v5dev_chartqa_donor_qwen25_7b.jsonl", 120)

run_checked(
    "python -B transplant_v5.py --split chartqa --phase dev "
    "--model_id Qwen/Qwen2.5-VL-7B-Instruct --batch_size 2 "
    "--base_file results_v5/v5dev_chartqa_base_qwen25_7b.jsonl "
    "--donor_file results_v5/v5dev_chartqa_donor_qwen25_7b.jsonl "
    "--run_tag v5dev_chartqa_tp_qwen25_7b",
    allow_zero_passed_tag="v5dev_chartqa_tp_qwen25_7b",
)
```

---

## Step 4: Close `F4 / R8.4` — ChartQA `--max_pixels 501760` Comparison (Cell 10)

Compare native-scale ChartQA (`800x557` px -> `--max_pixels 501760`) against default `200704` on the `30` spent ChartQA dev items for both confirmatory models (`3B` and `7B`). Distinct `v5dev_chartqa_px501k_*` tags keep these runs isolated from default dev files.

> *(Note: `RUNBOOK_v5.md` also allows passing `--gates_only` on the transplant command below if you only need gate survival counts; running full `transplant_v5.py` without `--gates_only` takes only a few extra minutes and also records margin/behavioural outputs for `501760`.)*

### Cell 10 — Run `3B` and `7B` ChartQA at `--max_pixels 501760`

```python
# 3B ChartQA at max_pixels=501760 (BS=8)
run_checked(
    "python -B harness_v5.py --stage base --split chartqa --phase dev --max_pixels 501760 "
    "--model_id Qwen/Qwen2.5-VL-3B-Instruct --batch_size 8 --run_tag v5dev_chartqa_px501k_base_qwen25"
)
assert_jsonl_rows("results_v5/v5dev_chartqa_px501k_base_qwen25.jsonl", 120)

run_checked(
    "python -B harness_v5.py --stage donor --split chartqa --phase dev --max_pixels 501760 "
    "--model_id Qwen/Qwen2.5-VL-3B-Instruct --batch_size 8 --run_tag v5dev_chartqa_px501k_donor_qwen25"
)
assert_jsonl_rows("results_v5/v5dev_chartqa_px501k_donor_qwen25.jsonl", 120)

run_checked(
    "python -B transplant_v5.py --split chartqa --phase dev --max_pixels 501760 "
    "--model_id Qwen/Qwen2.5-VL-3B-Instruct --batch_size 8 "
    "--base_file results_v5/v5dev_chartqa_px501k_base_qwen25.jsonl "
    "--donor_file results_v5/v5dev_chartqa_px501k_donor_qwen25.jsonl "
    "--run_tag v5dev_chartqa_px501k_tp_qwen25",
    allow_zero_passed_tag="v5dev_chartqa_px501k_tp_qwen25",
)

# 7B ChartQA at max_pixels=501760 (BS=2 on L4)
run_checked(
    "python -B harness_v5.py --stage base --split chartqa --phase dev --max_pixels 501760 "
    "--model_id Qwen/Qwen2.5-VL-7B-Instruct --batch_size 2 --run_tag v5dev_chartqa_px501k_base_qwen25_7b"
)
assert_jsonl_rows("results_v5/v5dev_chartqa_px501k_base_qwen25_7b.jsonl", 120)

run_checked(
    "python -B harness_v5.py --stage donor --split chartqa --phase dev --max_pixels 501760 "
    "--model_id Qwen/Qwen2.5-VL-7B-Instruct --batch_size 2 --run_tag v5dev_chartqa_px501k_donor_qwen25_7b"
)
assert_jsonl_rows("results_v5/v5dev_chartqa_px501k_donor_qwen25_7b.jsonl", 120)

run_checked(
    "python -B transplant_v5.py --split chartqa --phase dev --max_pixels 501760 "
    "--model_id Qwen/Qwen2.5-VL-7B-Instruct --batch_size 2 "
    "--base_file results_v5/v5dev_chartqa_px501k_base_qwen25_7b.jsonl "
    "--donor_file results_v5/v5dev_chartqa_px501k_donor_qwen25_7b.jsonl "
    "--run_tag v5dev_chartqa_px501k_tp_qwen25_7b",
    allow_zero_passed_tag="v5dev_chartqa_px501k_tp_qwen25_7b",
)
```

---

## Step 5: Verify `F1`, Compare `R8.4` (`200704` vs `501760`), and Run Analysis + `lme4` (Cells 11–12)

### Cell 11 — Hard Assertions for `F1` (`verdict_nll` Spans), Provenance, and `R8.4` Gates

```python
import glob, json, os

print("=== F1 & F2 Verification on Transplant Files ===")
tp_files = sorted(glob.glob("results_v5/v5dev_*_tp_*.jsonl"))
assert len(tp_files) >= 2, f"Expected at least 2 Math transplant JSONLs, found {tp_files}"

for path in tp_files:
    rows = [json.loads(line) for line in open(path, encoding="utf-8") if line.strip()]
    mpath = path.replace(".jsonl", ".manifest.json")
    assert os.path.exists(mpath), f"Missing manifest for {path}"
    m = json.load(open(mpath, encoding="utf-8"))
    dl_rows = [r for r in rows if r.get("outcome") == "dl"]
    verdict_dl = [r for r in dl_rows if r.get("verdict") in ("own", "flip", "para", "para_flip")]
    none_dl = [r for r in dl_rows if r.get("verdict") == "none"]
    n_tok = sum(1 for r in verdict_dl if (r.get("verdict_nll_tokens") or 0) > 0 and r.get("verdict_nll") is not None)
    n_exact = sum(1 for r in verdict_dl if r.get("verdict_span_exact") is True)
    n_none = sum(1 for r in none_dl if r.get("verdict_nll") is None and r.get("verdict_nll_tokens") is None)
    bm = sum(1 for r in dl_rows if r.get("boundary_mismatch")) / max(1, len(dl_rows))
    print(
        f"{path}: rows={len(rows)} | tok>0={n_tok}/{len(verdict_dl)} | "
        f"exact={n_exact}/{len(verdict_dl)} | none_null={n_none}/{len(none_dl)} | "
        f"bm={bm:.2%} | commit={m.get('resolved_model_commit')}"
    )
    assert m.get("resolved_model_commit"), f"Missing resolved_model_commit in {mpath}"
    assert n_tok == len(verdict_dl), f"F1 failure: verdict_nll missing/0 tokens in {path}"
    assert n_exact == len(verdict_dl), f"F1 failure: verdict_span_exact != True in {path}"
    assert n_none == len(none_dl), f"F1 failure: non-null verdict_nll on 'none' rows in {path}"
    assert bm <= 0.01, f"Boundary mismatch exceeded 1% ({bm:.2%}) in {path}"

print("\n=== R8.4 ChartQA max_pixels Comparison (200704 vs 501760) ===")
for tag in (
    "v5dev_chartqa_tp_qwen25",
    "v5dev_chartqa_px501k_tp_qwen25",
    "v5dev_chartqa_tp_qwen25_7b",
    "v5dev_chartqa_px501k_tp_qwen25_7b",
):
    gpath = f"results_v5/{tag}.gates.json"
    assert os.path.exists(gpath), f"Missing R8.4 gate file: {gpath}"
    g = json.load(open(gpath, encoding="utf-8"))
    print(f"{tag}: items={g['items']} -> competent={g['competent']} -> passed={g['passed']} | fails={g.get('fail_reasons')}")

print("\nALL F1, F2, AND R8.4 CHECKS PASSED.")
```

### Cell 12 — Run Full `analyze_v5.py` and `lme4` Mixed-Effects Models

Pass the explicit `v5dev_conflict_*` and `v5dev_chartqa_{tp,base,donor}_*` globs below so `v5dev_chartqa_px501k_*` files are excluded (otherwise `analyze_v5.py`'s duplicate-row guard refuses with exit code `2` because both ChartQA runs cover the same dev items):

```python
run_checked(
    "python -B analyze_v5.py "
    "--runs results_v5/v5dev_conflict_tp_*.jsonl results_v5/v5dev_chartqa_tp_*.jsonl "
    "--gates results_v5/v5dev_conflict_tp_*.gates.json results_v5/v5dev_chartqa_tp_*.gates.json "
    "--base results_v5/v5dev_conflict_base_*.jsonl results_v5/v5dev_chartqa_base_*.jsonl "
    "--donor results_v5/v5dev_conflict_donor_*.jsonl results_v5/v5dev_chartqa_donor_*.jsonl "
    "--output_dir results_v5/analysis_dev"
)

run_checked("apt-get update -qq && apt-get install -y -qq r-base")
run_checked("Rscript -e 'install.packages(\"lme4\", repos=\"https://cloud.r-project.org\")'")
run_checked("Rscript results_v5/analysis_dev/analyze_v5_lme4.R results_v5/analysis_dev/long_v5.csv results_v5/analysis_dev/lme4_out.txt")
run_checked("cat results_v5/analysis_dev/lme4_out.txt")
```

---

## Step 6: Disconnect Recovery & Post-Run Local Handoff

### If Colab Disconnects Mid-Run

1. Reconnect to an **L4** or **A100** runtime.
2. Re-run **Cell 1** and **Cell 2**.
3. Re-run the interrupted cell (and remaining cells). `harness_v5.py` and `transplant_v5.py` automatically skip completed request keys and repair any half-written trailing line in `.jsonl`.

### Bring Outputs Back & Check Donor Drift Locally

1. Before copying new Colab results into [`Experiment/results_v5/`](../../../Experiment/results_v5/), move your previous local `v5dev_*` files into a temporary backup folder (e.g., `Experiment/results_v5_prev_backup/`, outside `results_v5/`) so old and new dev files are never pooled.
2. Download the contents of `MyDrive/Thesis_v5/results_v5/` into [`Experiment/results_v5/`](../../../Experiment/results_v5/).
3. Diff old vs. new `donor` generations (`v5dev_*_donor_*.jsonl`) locally before deciding whether [`Experiment/sample_v5_for_coding.py`](../../../Experiment/sample_v5_for_coding.py) needs to regenerate `Experiment/coding_v5/` sheets for Coder A and Coder B:

```python
import glob, json, os

old_dir = "Experiment/results_v5_prev_backup"
new_dir = "Experiment/results_v5"
for new_path in sorted(glob.glob(os.path.join(new_dir, "v5dev_*_donor_*.jsonl"))):
    old_path = os.path.join(old_dir, os.path.basename(new_path))
    if not os.path.exists(old_path):
        print(os.path.basename(new_path), "-> no prior donor file")
        continue
    key_fn = lambda r: (r["item_id"], r["order"], r.get("arm"))
    old_rows = {key_fn(json.loads(l)): json.loads(l).get("raw_text") for l in open(old_path, encoding="utf-8") if l.strip()}
    new_rows = {key_fn(json.loads(l)): json.loads(l).get("raw_text") for l in open(new_path, encoding="utf-8") if l.strip()}
    diffs = sum(1 for k in set(old_rows) | set(new_rows) if old_rows.get(k) != new_rows.get(k))
    print(f"{os.path.basename(new_path)}: diffs={diffs}/{len(new_rows)}")
```

4. Using Cell 11's `200704` vs `501760` comparison, lock `CONFIRM_MAX_PIXELS["chartqa"]` in code and `Docs/PREREGISTRATION_VERDICT_TRANSPLANT.md` §3.4 together, re-run `python -B Experiment/preflight_v5.py` and `unittest`, and commit + tag `prereg-v5` only after double human coding (`kappa >= 0.80`) is complete.
