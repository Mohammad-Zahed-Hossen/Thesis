# results_v5

Current v5 dev rerun (`2026-11-15/16`) across all three models (`Qwen2-VL-2B-Instruct`, `Qwen2.5-VL-3B-Instruct`, `Qwen2.5-VL-7B-Instruct`), run on an NVIDIA L4 in `torch.bfloat16` (`torch 2.14.1+cu130`, `transformers 5.22.1`, `cuda 13.0`, recorded in `pip_freeze.txt` and `*.manifest.json`) after the pre-freeze code/scorer/provenance fixes (`F2`, `F3`, `F5`–`F13`, `Upgrades 1–5`).

**Status:** **Dev data only — do not cite as confirmatory findings.**
- **Total stored root artifacts:** **49 data/env files** (`20` `.jsonl`, `20` `.manifest.json`, `8` `.gates.json`, and `pip_freeze.txt`, plus this `README.md`), **34,920 rows**, covering the 6 main `200704` dev blocks plus the 2 `px501k` (`501760`) ChartQA R8.4 comparison blocks.
- **`analysis_dev/`:** Holds the current `analyze_v5.py` and `lme4` outputs computed on the 6 main `200704` dev blocks (`analysis_v5.md`, `analysis_v5.json`, `long_v5.csv`, `analyze_v5_lme4.R`, `lme4_out.txt`; excluding `px501k` to avoid duplicate dev-item pooling).
- **Previous dev pass archived:** The initial `2026-11-12/13` dev pass (`29,880` rows + its `analysis_dev/` and dev audits) is preserved in [../archive/results_v5_Prev_backup/](../archive/results_v5_Prev_backup/README.md).
- **Donor consistency:** All 6 main `donor` files (`120` ChartQA rows, `800` Math rows per model) are **0-diff byte-identical** to the archived `2026-11-12/13` donor generations, so the existing [../coding_v5/](../coding_v5/) human-coding sheets (`200` verdicts + `150` flips) match this rerun with zero drift (coded and adjudicated 2026-11-20; see [../coding_v5/evaluation_v5.json](../coding_v5/evaluation_v5.json)).

> **Token tip for agents:** Never `cat` the `.jsonl` files (the `*_tp_*` files are up to 23 MB). Read `*.gates.json`, `*.manifest.json`, `analysis_dev/analysis_v5.md`, or `analysis_dev/lme4_out.txt` instead.

---

## Naming convention

`v5dev_<split>[_px501k]_<stage>_<model>.<ext>`
- `split`: `conflict` (GSM8K/SVAMP Math, 200 dev items) or `chartqa` (ChartQA-Conflict, 30 dev items).
- `_px501k`: optional R8.4 comparison run on ChartQA at `max_pixels = 501760` (default blocks use `200704`).
- `stage`: `base` (single-source competency), `donor` (model's own verdicts + `free_binding`), `tp` (transplant + Δℓ & behavioural scoring).
- `model`: `qwen2` (2B, diagnostic-only per D3), `qwen25` (3B, confirmatory), `qwen25_7b` (7B, confirmatory).
- `ext`: `.jsonl` (rows), `.manifest.json` (run config, `invocations[]`, `resolved_model_commit`, `peak_vram_gb`), `.gates.json` (edit-gate counts, `tp` only).

---

## Artifact inventory

### 1. Main dev blocks (`max_pixels = 200704`, analysed in `analysis_dev/`)

| File prefix | Rows (`.jsonl`) | Gates (`items → competent → passed`) | Notes |
|---|---|---|---|
| `v5dev_conflict_base_qwen2` | 800 | — | 2B diagnostic-only (D3); peak 4.50 GB |
| `v5dev_conflict_donor_qwen2` | 800 | — | |
| `v5dev_conflict_tp_qwen2` | *(none)* | `200 → 0 → 0` | 2B wrote no `####` in Math; no transplant `.jsonl` |
| `v5dev_conflict_base_qwen25` | 800 | — | `structured` competency; peak 7.38 GB |
| `v5dev_conflict_donor_qwen25` | 800 | — | |
| `v5dev_conflict_tp_qwen25` | 11,400 | `200 → 95 → 95` | 95 items × 120 rows; `0` boundary mismatches |
| `v5dev_conflict_base_qwen25_7b` | 800 | — | `structured` competency; peak 15.59 GB |
| `v5dev_conflict_donor_qwen25_7b` | 800 | — | |
| `v5dev_conflict_tp_qwen25_7b` | 16,800 | `200 → 154 → 140` | 140 items × 120 rows (`gate3_too_many_swaps` 13, `own_undetermined` 1); `0` boundary mismatches |
| `v5dev_chartqa_base_qwen2` | 120 | — | 30 items × 2 arms × 2 rows |
| `v5dev_chartqa_donor_qwen2` | 120 | — | |
| `v5dev_chartqa_tp_qwen2` | *(none)* | `30 → 10 → 0` | Failed gates (`own_absent` 18, `own_undetermined` 2) |
| `v5dev_chartqa_base_qwen25` | 120 | — | |
| `v5dev_chartqa_donor_qwen25` | 120 | — | |
| `v5dev_chartqa_tp_qwen25` | 600 | `30 → 13 → 5` | 5 items × 120 rows (`own_absent` 10, `gate_answer_leakage` 2) |
| `v5dev_chartqa_base_qwen25_7b` | 120 | — | |
| `v5dev_chartqa_donor_qwen25_7b` | 120 | — | |
| `v5dev_chartqa_tp_qwen25_7b` | *(none)* | `30 → 13 → 0` | Failed gates (`gate_answer_leakage` 15, `gate3_too_many_swaps` 9) |

### 2. ChartQA `max_pixels` R8.4 comparison blocks (`max_pixels = 501760`)

| File prefix | Rows (`.jsonl`) | Gates (`items → competent → passed`) | Notes |
|---|---|---|---|
| `v5dev_chartqa_px501k_base_qwen25` | 120 | — | Peak 7.89 GB (`16/30` competent vs `13/30` at `200704`) |
| `v5dev_chartqa_px501k_donor_qwen25` | 120 | — | |
| `v5dev_chartqa_px501k_tp_qwen25` | 120 | `30 → 16 → 1` | 1 item × 120 rows (`own_absent` 27, `gate_answer_leakage` 1, `gate3_too_many_swaps` 1) |
| `v5dev_chartqa_px501k_base_qwen25_7b` | 120 | — | Peak 15.76 GB (`17/30` competent vs `13/30` at `200704`) |
| `v5dev_chartqa_px501k_donor_qwen25_7b` | 120 | — | |
| `v5dev_chartqa_px501k_tp_qwen25_7b` | *(none)* | `30 → 17 → 0` | Failed gates (`gate_answer_leakage` 21, `gate3_too_many_swaps` 12) |

---

## Key dev-pass takeaways (`analysis_dev/`, dev only — not findings)

From [analysis_dev/analysis_v5.md](analysis_dev/analysis_v5.md) and [analysis_dev/lme4_out.txt](analysis_dev/lme4_out.txt):
1. **Integrity & `F1` verification:**
   - **0** `boundary_mismatch` across all **23,136** `dl` rows (`9,120` 3B Math, `13,440` 7B Math, `480` 3B ChartQA, `96` 3B `px501k`).
   - `verdict_nll_tokens > 0` on all **15,424** non-`none` / non-explicit `dl` rows, and `verdict_nll` is `null` on all **7,712** `none` `dl` rows.
   - All 20 `.manifest.json` files record `NVIDIA L4`, `torch.bfloat16`, and populated `resolved_model_commit` matching `MODEL_PINS`.
2. **GSM8K/SVAMP Math (`structured` parser; below R5 `n = 150` minimum → `NOT A READING`):**
   - **Qwen2.5-VL-3B (`N = 95`):** Primary `Δ_bind (flip − own)` = `+50.5 pp` (90% CI `[0.442, 0.568]`, `p = 0.0001`), co-primary `para_flip − para` = `+60.5 pp` (`[0.542, 0.668]`, `p = 0.0001`), `T1_beh` DiD = `0.153` (`p = 0.0010`), `B_beh` = `0.471`. Wording floor **passes** under binding (signed mean `−4.7 pp`, attributable churn `4.5%`, neither shift `+5.3 pp`; replay flips `2.6%`) and **fails** under non-binding (`6.1%` > `5.0%` attributable churn).
   - **Qwen2.5-VL-7B (`N = 140`):** Primary `Δ_bind (flip − own)` = `+45.7 pp` (90% CI `[0.411, 0.500]`, `p = 0.0001`), co-primary `para_flip − para` = `+66.8 pp` (`[0.618, 0.714]`, `p = 0.0001`), `T1_beh` DiD = `0.146` (`p = 0.0001`), `B_beh` = `0.811`. Wording floor **passes** under binding (signed mean `−1.1 pp`, attributable churn `0.0%`, neither shift `+1.1 pp`; replay flips `0.9%`) and **fails** under non-binding (signed mean `−5.4 pp` and `5.8%` attributable churn).
   - **3B vs. 7B intersection (`N = 80`):** Behavioural `Δ_bind (7B − 3B) = −4.4 pp` (`95% CI [-0.144, 0.056]`) and `Δ_bind_pair = +6.9 pp` (`[-0.044, 0.175]`).
   - **Mixed-effects (`lme4_out.txt`):** On 7B Math both `lmer` and `glmer` converged with the full `(1 + D | item)` random slope; on 3B Math and 3B ChartQA the by-item random slope was dropped cleanly to `(1 | item)`.
3. **ChartQA-Conflict & R8.4 `max_pixels` comparison (exploratory, D4):**
   - Raising `max_pixels` from `200704` to `501760` raised single-source competency slightly (`13 → 16` on 3B; `13 → 17` on 7B) but reduced gate-passing survival (`5 → 1` on 3B due to `own_absent: 27`; `0 → 0` on 7B due to `gate_answer_leakage: 21`, `gate3_too_many_swaps: 12`).
4. **Before freezing `prereg-v5`:**
   - Done (2026-11-20): double human coding in [../coding_v5/](../coding_v5/), adjudicated (`adjudication_v5.csv`, `evaluation_v5.json`; prereg §8 as revised, §11).
   - Done (2026-11-20): ChartQA `max_pixels` locked at `200704` in [../../Docs/PREREGISTRATION_VERDICT_TRANSPLANT.md](../../Docs/PREREGISTRATION_VERDICT_TRANSPLANT.md) §3.4.
   - Open: commit and tag `prereg-v5`.
   - Note: `analysis_dev/` was produced before `manipulation_check` switched to the `structured` parser (dev shift ≤ 0.8 pp); it was not re-run.

To regenerate `analysis_dev/` locally (excluding `px501k` to avoid duplicate-item pooling), run from `Experiment/` (in Git Bash, or expand globs explicitly in PowerShell):

```bash
python -B analyze_v5.py \
  --runs results_v5/v5dev_conflict_tp_*.jsonl results_v5/v5dev_chartqa_tp_*.jsonl \
  --gates results_v5/v5dev_conflict_tp_*.gates.json results_v5/v5dev_chartqa_tp_*.gates.json \
  --base results_v5/v5dev_conflict_base_*.jsonl results_v5/v5dev_chartqa_base_*.jsonl \
  --donor results_v5/v5dev_conflict_donor_*.jsonl results_v5/v5dev_chartqa_donor_*.jsonl \
  --output_dir results_v5/analysis_dev
```
