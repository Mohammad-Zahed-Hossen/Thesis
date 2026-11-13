# Experiment

Start here. This folder holds all experiment code and data for the thesis. **It is ground truth** (AGENTS.md §2): code + raw rows outrank every `.md` report, including this one.

**Last updated:** 2026-11-14
**Stage:** The v5 **dev pass has run** on an L4 in `bfloat16` for all three models (29,880 rows in [results_v5/](results_v5/)). It has been audited ([../Thesis/docs/Archive/](../Thesis/docs/Archive/)), and `analyze_v5.py` has been run on it ([results_v5/analysis_dev/](results_v5/analysis_dev/)). The pre-freeze decisions D1–D5 are made and written into the pre-registration: behaviour is the primary outcome in Math, ChartQA is exploratory, Qwen2-VL-2B is diagnostic only. On 2026-11-14 three gates were tightened after an audit of the post-v5 plan ([../Thesis/docs/Archive/claude_v4_vs_v5_plan_audit.md](../Thesis/docs/Archive/claude_v4_vs_v5_plan_audit.md)): a fixed wording-floor limit, a Math decision rule on Δ itself, and an explicit inconclusive reading. The pre-registration is **not frozen**. **No confirmatory data exists.**
**Design spec:** [../Docs/PREREGISTRATION_VERDICT_TRANSPLANT.md](../Docs/PREREGISTRATION_VERDICT_TRANSPLANT.md) (draft; freeze conditions in §10, R8).
**Next action:** Finish the open pre-freeze items listed in the pre-registration (§3.4 and the R8 note): human coding of verdict labels ([coding_v5/](coding_v5/)), the ChartQA `max_pixels` decision and render check, a short GPU check of the new `verdict_nll` span, and the researcher's decision on the thesis scope and title (source following vs. reliability). Then freeze (tag `prereg-v5`).

> **Token tip for agents:** Never `cat` the JSONL files. The `*_tp_*` files are 10–16 MB. Read the `*.manifest.json` / `*.gates.json` files, the result-folder READMEs, or summarise rows with a short script.

---

## v5 dev pass at a glance (dev only, not findings)

Counts come from `results_v5/*.gates.json`. The interpretation is from the [independent deep audit](../Thesis/docs/Archive/claude_v5_independent_deep_audit.md) (2026-11-13).

| Model | Math (GSM8K/SVAMP), 200 items: competent → passed gates | ChartQA, 30 items: competent → passed gates |
|---|---|---|
| Qwen2-VL-2B (`qwen2`) | **0 → 0.** Writes no `####` in any of its 1,200 generations, so it fails the format rule (eligibility, not accuracy). No transplant JSONL. | 10 → 0 (`own_absent` 18, `own_undetermined` 2). No transplant JSONL. |
| Qwen2.5-VL-3B (`qwen25`) | 80 → 80 | 13 → 6 |
| Qwen2.5-VL-7B (`qwen25_7b`) | 124 → 115 | 13 → 2 |

Blocking issues the audit verified (details and the decisions they need are in §10):
1. **Δℓ validity in Math:** the sign of Δℓ at `####` agrees with the actual answer source in only 51.6% (3B) and 56.6% (7B) of rows, and it follows evidence order more than the explicit instruction.
2. **7B flip contrast:** mostly driven by deleting the model's own verdict, not by the reversed verdict. `flip` vs. `none` adds 0.10 [−0.09, 0.29] out of a CDE of 1.62.
3. **Replay churn:** replaying the model's own verdict unchanged already shifts the answer source in 6–8% of cells, above the pre-registered 5% churn limit. The behavioural wording floor fails in Math (20–28% churn).
4. **ChartQA attrition:** 6 / 2 / 0 items retained. The §8 "≥ 60% pass edit gates" rule fails and is not implemented in code. The render gate, the `max_pixels` decision (R8.4) and human coding are still open.
5. **Provenance:** manifests describe only the last invocation, and `resolved_model_commit` is null.

---

## What v5 adds over v4

Files: `harness_v5.py`, `transplant_v5.py`, `score_v5.py`, `analyze_v5.py`. The v4 files are unchanged.
1. **Order counterbalancing without letters.** `build_content(..., order)` makes `[instruction, source 1, <image> or text, source 2, format]` with modality headers ("Image:", "Typed text:", "Chart:", "Report:"). Only the sources swap.
2. **Literal K = 4 templates** for the non-binding, binding and explicit arms, in both regimes. A test checks each string against the pre-registration text.
3. **Minimal-edit verdicts:** `own`, `flip`, `none`, `para`, `para_flip`, with the gates of pre-registration §5.3 and a per-run `gates.json`.
4. **Primary outcome Δℓ.** The length-normalized log-likelihood margin at `####`, image minus text, with an exact token-boundary check. Behavioural decodes are secondary: 512-token solving for GSM8K/SVAMP, 16-token answer-only for ChartQA.
5. **Ceilings** use the `none` prefill. Explicit arms run only with `none`.
6. **Three models** (2B, 3B, 7B), pinned in `MODEL_PINS` (`harness_v4.py`), all run in `bfloat16`. The harness refuses any other dtype. ChartQA defaults to `--dev_size 30`.

---

## Layout

```
Experiment/
├── README.md               This file
├── RUNBOOK_v4.md           Exact commands, in order (v4)
├── RUNBOOK_v5.md           Exact commands for the v5 dev pass, analysis, and confirm phase
│
├── harness_v5.py           v5 prompts; base and donor stages (GPU)
├── transplant_v5.py        v5 minimal-edit verdicts, gates, Δℓ scoring (GPU)
├── score_v5.py             v5 parser extensions and margin math
├── analyze_v5.py           v5 confirmatory tests (T1, ρ, TOST, floors), readings, lme4 export (local)
├── tests/test_v5.py        v5 harness/scorer tests; no GPU needed
├── tests/test_analyze_v5.py  analyze_v5 tests on synthetic rows
│
├── score_v4.py             v4 scorer; also imported by v5
├── harness_v4.py           v4 generation runs (GPU); holds MODEL_PINS and verbatim *_v3 prompts
├── transplant_v4.py        v4 mediator transplant runs (GPU)
├── analyze_v4.py           v4 gates, contrasts, penalty effects (local)
├── reanalyze_v3.py         Re-scores stored v3 outputs (local)
├── statistical_analysis.py Paired statistics for v3; shared helpers (local)
├── sample_for_coding.py    Human-coding sheets and scorer validation (local)
├── tests/test_v4.py        v4 test suite; no GPU needed
│
├── results_v5/             v5 dev pass: 16 JSONL + 16 manifests + 6 gates + pip_freeze.txt (see its README)
├── results_v4/             v4 smoke, dev2 runs, analysis_dev2/, superseded/ (see its README)
├── results_v3/             Stored v3 pilot, N = 1,619, plus re-analysis (see its README)
├── coding_v3/              Human-coding sheets (CODEBOOK, coder_A/B; KEY_do_not_open.csv), not yet coded
└── archive/                Superseded v3 harness and v1/v2 pilots (see its README)
```

### `results_v5/` naming

`v5dev_<split>_<stage>_<model>.<ext>`
- `split`: `conflict` (GSM8K/SVAMP Math regime) or `chartqa`.
- `stage`: `base` (single-source competency), `donor` (the model's own verdicts), or `tp` (transplant, where Δℓ is scored).
- `model`: `qwen2` = 2B, `qwen25` = 3B, `qwen25_7b` = 7B.
- `ext`: `.jsonl` (rows), `.manifest.json` (run config of the last invocation), `.gates.json` (edit-gate report, `tp` only).

`pip_freeze.txt` records the Colab environment.

---

## Status

| Work | Status | Where |
|---|---|---|
| v3 pilot, N = 1,619 | Done; exploratory only | `results_v3/` |
| v3 re-analysis | Done | `results_v3/reanalysis_v3/`, `results_v3/stats_v3_paired/` |
| Harness on a real GPU (v4) | Works on a T4 with transformers 5.22.2 | `results_v4/*.manifest.json` |
| v4 dev run (dev2), 15 arms, 200 items | Complete (3,000 rows, CoT working enabled) | `results_v4/dev2_qwen25.jsonl` |
| v4 penalty check (dev2) | Complete (600 rows, rp = 1.05) | `results_v4/dev2_qwen25_rp105.jsonl` |
| v4 dev transplant (dev2) | Complete and valid (2,800 rows, fidelity > 95%) | `results_v4/dev2_transplant_qwen25.jsonl` |
| v4 dev analysis (dev2) | Done. The verdict moves answers under the neutral instruction but not under the conflict instruction. Dev only, not a finding. | `results_v4/analysis_dev2/`, dossier §2.2 |
| Literature dossier | Done | [../Docs/Paper/lit-dossier-verdict-transplant/](../Docs/Paper/lit-dossier-verdict-transplant/) |
| Freeze audit (2026-11-10) | Received; red light. Its fixes were applied to the pre-registration. | [../Docs/Paper/prereg-freeze-audit/](../Docs/Paper/prereg-freeze-audit/) |
| Pre-registration | Drafted, **not frozen** | [../Docs/PREREGISTRATION_VERDICT_TRANSPLANT.md](../Docs/PREREGISTRATION_VERDICT_TRANSPLANT.md) |
| v5 harness (order, templates, minimal edits, margin) | Written; CPU tests pass; **ran on an L4 (bf16)** | `harness_v5.py`, `transplant_v5.py`, `score_v5.py`, `tests/test_v5.py` |
| v5 dev pass (2B, 3B, 7B; 200 + 30 items) | **Done.** 29,880 rows, internally consistent. No 2B transplant (0 eligible items). | `results_v5/` |
| v5 dev audits | Done: inventory, evidence audit, independent deep audit | [../Thesis/docs/Archive/](../Thesis/docs/Archive/) |
| `analyze_v5.py` on dev rows | **Not run yet.** Tested only on synthetic rows. | `analyze_v5.py`, `tests/test_analyze_v5.py` |
| Pre-freeze decisions (2B format rule, Δℓ validity in Math, churn limit, ChartQA gates and `max_pixels`, ρ ceiling) | **Next.** Needs the researcher's rulings, logged as deviations. | deep audit §10 |
| ChartQA render gate | Not recorded | [RUNBOOK_v5.md](RUNBOOK_v5.md) |
| Human coding of verdict labels | Sheets generated, not yet coded. Needed before any claim based on verdict labels. One mislabel already found. | `coding_v3/` |
| Confirmatory run | After the pre-registration freeze | GPU (L4/A100), `--phase confirm` |
| Mechanistic probe | Not planned for the thesis core | — |

---

## Rules for working here

- **Dev data is for tuning only.** Don't cite dev numbers (v4 `dev2` or `results_v5/v5dev_*`) as findings.
- **Use a new `--run_tag` after changing prompts or settings.** Reusing a tag resumes the run and skips rows it already has.
- **Primary outcome.** For v4 runs, exact-answer match. For v5 runs, the log-likelihood margin Δℓ after a forced `####` only. Generated answers are secondary (pre-registration §6). Attempt, refusal and verdict labels stay heuristic until human coding validates them.
- **v5 invariants are mandatory:** counterbalanced order, binding and ceiling arms, minimal-edit verdicts, and competency-filtered primary results. See [../AGENTS.md](../AGENTS.md) §1 and `../CLAUDE.md`.
- **Pre-freeze changes must be logged deviations.** The pre-registration says dev numbers may not change R4/R6. Any change to the competency rule, the ρ definition or the gates needs an explicit, recorded ruling.
- **Keep v3 data read-only.** Prompts in `harness_v4.py` named `*_v3` must stay verbatim; a test enforces this.
- **Model code runs on the GPU session only** (Colab Pro L4/A100 or RunPod; ≥ 24 GB, `bfloat16`; not T4/V100).
  - v5: upload `harness_v4.py`, `score_v4.py`, `harness_v5.py`, `score_v5.py`, `transplant_v5.py`.
  - v4: upload `harness_v4.py`, `transplant_v4.py`, `score_v4.py`.
  - Everything else runs locally. No model loading on the local machine.
- **After changing code, run the tests:**

```bash
python -m unittest discover tests
```

---

## Trust order

1. Rows in `results_v5/*.jsonl`, `results_v4/*.jsonl` and `results_v3/full_experiment_results v3.0.json`, plus the `*.manifest.json` / `*.gates.json` files
2. Code in this folder
3. Generated reports, such as `results_v4/analysis_dev2/` and the v5 audits in `../Thesis/docs/Archive/`
4. READMEs like this one, which can go stale
5. `../Docs/` (except the pre-registration and `Docs/Paper/` PDFs): AI-generated notes that describe older paths and overstate v3

`results_v3/statistical_report v3.0.md` and `thesis_contingency_table v3.0.tex` contain verdict wording that the audit rejected. They're kept as a record, so don't cite them.
