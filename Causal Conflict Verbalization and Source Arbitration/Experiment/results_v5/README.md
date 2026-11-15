# results_v5

v5 dev pass outputs across all three models (`Qwen2-VL-2B-Instruct`, `Qwen2.5-VL-3B-Instruct`, `Qwen2.5-VL-7B-Instruct`), run on an NVIDIA L4 in `torch.bfloat16` (`torch 2.14.1+cu130`, `transformers 5.22.1`, `cuda 13.0`, recorded in `pip_freeze.txt` and `*.manifest.json`).

**Status:** **Dev data only — do not cite as confirmatory findings.**
- Total stored root artifacts: 39 files (16 `.jsonl`, 16 `.manifest.json`, 6 `.gates.json`, plus `pip_freeze.txt`), **29,880 rows**, alongside `analysis_dev/` (4 generated analysis files).
- Audited in [../../Thesis/docs/Archive/dev v5/](<../../Thesis/docs/Archive/dev v5/>) (`v5_dev_evidence_audit.md`, `claude_v5_independent_deep_audit.md`, `claude_v5_forensic_code_and_construct_audit.md`, and `claude_v4_vs_v5_plan_audit.md`).
- `analysis_dev/` holds the current output of `analyze_v5.py` on these files (`analysis_v5.md`, `analysis_v5.json`, `long_v5.csv`, `analyze_v5_lme4.R`), reflecting pre-freeze decisions D1–D5 and the 2026-11-14 gate updates. To regenerate it, follow the analysis step in [../RUNBOOK_v5.md](../RUNBOOK_v5.md).
- The `*.gates.json` and transplant rows were produced during the 2026-11-12/13 Colab L4 dev pass (whose manifest `scripts_sha256` digests pre-date the versions committed in git). Scorers and gates have since been updated (D3 `structured` competency, Sentence-1 answer-leakage gate, foil/grammar hardening), so re-evaluating the stored dev files (`competent -> passed`) changes counts from stored (`80 -> 80` / `124 -> 115` on Math 3B / 7B; `13 -> 6` / `13 -> 2` on ChartQA 3B / 7B; `0 -> 0` / `10 -> 0` on 2B) to **`93 -> 93`** / **`154 -> 140`** on Math under `structured` (`80 -> 80` / `124 -> 113` under `strict`) and **`13 -> 5`** / **`13 -> 0`** on ChartQA (`2B` unchanged). The stored files record what was actually decoded during dev.

> **Token tip for agents:** Never `cat` the `.jsonl` files (the `*_tp_*` files are 10–16 MB). Read the `*.gates.json` / `*.manifest.json` files or the audit reports instead.

---

## Naming convention

`v5dev_<split>_<stage>_<model>.<ext>`
- `split`: `conflict` (GSM8K/SVAMP Math, 200 dev items) or `chartqa` (ChartQA-Conflict, 30 dev items)
- `stage`: `base` (single-source competency), `donor` (model's own verdicts), `tp` (transplant + Δℓ scoring)
- `model`: `qwen2` (2B), `qwen25` (3B), `qwen25_7b` (7B)
- `ext`: `.jsonl` (rows), `.manifest.json` (last-invocation run config/environment), `.gates.json` (edit-gate counts, `tp` only)

---

## Artifact inventory

| File prefix | Rows (`.jsonl`) | Gates (`items → competent → passed`) | Notes |
|---|---|---|---|
| `v5dev_conflict_base_qwen2` | 800 | — | 200 items × 2 single-source arms (`base_image`, `base_text`) × 2 rows (one generation, one gold-answer score). No evidence order |
| `v5dev_conflict_donor_qwen2` | 800 | — | |
| `v5dev_conflict_tp_qwen2` | *(none)* | `200 → 0 → 0` | 2B wrote no `####` in Math; no transplant `.jsonl` |
| `v5dev_conflict_base_qwen25` | 800 | — | |
| `v5dev_conflict_donor_qwen25` | 800 | — | |
| `v5dev_conflict_tp_qwen25` | 9,600 | `200 → 80 → 80` | |
| `v5dev_conflict_base_qwen25_7b` | 800 | — | |
| `v5dev_conflict_donor_qwen25_7b` | 800 | — | |
| `v5dev_conflict_tp_qwen25_7b` | 13,800 | `200 → 124 → 115` | |
| `v5dev_chartqa_base_qwen2` | 120 | — | 30 items × 2 single-source arms × 2 rows. No evidence order |
| `v5dev_chartqa_donor_qwen2` | 120 | — | |
| `v5dev_chartqa_tp_qwen2` | *(none)* | `30 → 10 → 0` | Failed gates (`own_absent` 18, `own_undetermined` 2); no `.jsonl` |
| `v5dev_chartqa_base_qwen25` | 120 | — | |
| `v5dev_chartqa_donor_qwen25` | 120 | — | |
| `v5dev_chartqa_tp_qwen25` | 720 | `30 → 13 → 6` | |
| `v5dev_chartqa_base_qwen25_7b` | 120 | — | |
| `v5dev_chartqa_donor_qwen25_7b` | 120 | — | |
| `v5dev_chartqa_tp_qwen25_7b` | 240 | `30 → 13 → 2` | |

---

## Key audit takeaways (dev only)

From [claude_v5_independent_deep_audit.md](<../../Thesis/docs/Archive/dev v5/claude_v5_independent_deep_audit.md>) §1 and §10, and [claude_v5_forensic_code_and_construct_audit.md](<../../Thesis/docs/Archive/dev v5/claude_v5_forensic_code_and_construct_audit.md>):
1. **Integrity:** All 29,880 rows are internally consistent, with zero `boundary_mismatch` across all 20,868 scored rows.
2. **Provenance gap (fixed post-dev):** Historical stored dev manifests record only the last invocation and have `resolved_model_commit: null`, and unrecorded sessions ran some batches. Closed for future runs in `harness_v4.py`, `harness_v5.py`, `transplant_v5.py`, and `preflight_v5.py` (append-only `invocations[]`, git commit/tag provenance ignoring untracked `results_v5/`/`results_v4/` outputs, `requested_model_revision` + `resolved_model_commit` resolved from loaded model config or local HF cache `snapshots/`/`refs/`, and confirm tag/pixel guards).
3. **Pre-freeze dispositions:**
   - **Addressed in pre-registration & code (D1–D5, 2026-11-13/14):** Math primary outcome shifted to behavioural choice (`structured` parser; `para_flip - para` co-primary); `Qwen2-VL-2B` set to diagnostic-only; ChartQA set to exploratory/secondary; Sentence-1 answer-leakage gate and exact `verdict_nll` span scoring implemented; wording-floor gate fixed at `±5.0 pp` signed mean / `≤ 5.0%` attributable `image <-> text` churn / `±10 pp` neither shift (non-binding Math still fails on dev, making H₀ uninterpretable there without blocking H₁).
   - **Still open before freeze:** Double human coding ([../coding_v5/](../coding_v5/)), ChartQA `max_pixels` comparison (`200704` vs `501760`, R8.4), ChartQA `--print_example` render gate, GPU `--limit 20` smoke check of `verdict_nll` spans, and tagging `prereg-v5`.

