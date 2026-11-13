# results_v5

v5 dev pass outputs across all three models (`Qwen2-VL-2B-Instruct`, `Qwen2.5-VL-3B-Instruct`, `Qwen2.5-VL-7B-Instruct`), run on an NVIDIA L4 in `torch.bfloat16` (`torch 2.14.1+cu130`, `transformers 5.22.1`, `cuda 13.0`, recorded in `pip_freeze.txt` and `*.manifest.json`).

**Status:** **Dev data only — do not cite as confirmatory findings.**
- Total stored artifacts: 39 files (16 `.jsonl`, 16 `.manifest.json`, 6 `.gates.json`, plus `pip_freeze.txt`), **29,880 rows**.
- Audited twice in [../../Thesis/docs/Archive/](../../Thesis/docs/Archive/) (`v5_dev_evidence_audit.md` and `claude_v5_independent_deep_audit.md`).
- `analyze_v5.py` has **not** yet been run on these files (there is no `analysis_dev/` folder yet). To generate it, follow the analysis step in [../RUNBOOK_v5.md](../RUNBOOK_v5.md).

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
| `v5dev_conflict_base_qwen2` | 800 | — | 200 items × 2 orders × 2 sources |
| `v5dev_conflict_donor_qwen2` | 800 | — | |
| `v5dev_conflict_tp_qwen2` | *(none)* | `200 → 0 → 0` | 2B wrote no `####` in Math; no transplant `.jsonl` |
| `v5dev_conflict_base_qwen25` | 800 | — | |
| `v5dev_conflict_donor_qwen25` | 800 | — | |
| `v5dev_conflict_tp_qwen25` | 9,600 | `200 → 80 → 80` | |
| `v5dev_conflict_base_qwen25_7b` | 800 | — | |
| `v5dev_conflict_donor_qwen25_7b` | 800 | — | |
| `v5dev_conflict_tp_qwen25_7b` | 13,800 | `200 → 124 → 115` | |
| `v5dev_chartqa_base_qwen2` | 120 | — | 30 items × 2 orders × 2 sources |
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

From [claude_v5_independent_deep_audit.md](../../Thesis/docs/Archive/claude_v5_independent_deep_audit.md) §1 and §10:
1. **Integrity:** All 29,880 rows are internally consistent, with zero `boundary_mismatch` across all 20,868 scored rows.
2. **Provenance gap:** Manifests record only the last invocation, `resolved_model_commit` is null, and unrecorded sessions ran some batches.
3. **Pre-freeze blockers:** 2B `####` format eligibility (0/200 in Math), ChartQA attrition (6/2/0 retained), Math Δℓ–behaviour sign agreement (51.6% on 3B, 56.6% on 7B), 7B flip contrast driven mostly by removing the own verdict, and replay/wording churn above the 5% limit.

