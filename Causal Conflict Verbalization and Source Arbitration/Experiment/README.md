# Experiment

Start here. This folder holds all experiment code and data for the thesis. **It is ground truth** (AGENTS.md §2): code + raw rows outrank every `.md` report, including this one.

**Last updated:** 2026-11-16
**Stage:** The initial v5 dev pass (`2026-11-12/13`, 29,880 rows + `analysis_dev/`) has been archived in [archive/results_v5_Prev_backup/](archive/results_v5_Prev_backup/), and a post-fix v5 dev rerun (`2026-11-15/16`) is in [results_v5/](results_v5/) (**31,352 rows** across 13 `.jsonl` files on an NVIDIA L4 in `bfloat16`; **7B is not yet complete**: Math transplant has `14,072 / 16,800` rows and 7B ChartQA has not run yet). The initial pass was audited ([../Thesis/docs/Archive/dev v5/](<../Thesis/docs/Archive/dev v5/>); [fable52-prefreeze-audit-2026-11-15.md](../Docs/Paper/fable52-prefreeze-audit-2026-11-15.md)) and analysed (`archive/results_v5_Prev_backup/analysis_dev/`). All **248** CPU unit tests pass (`unittest`) and `preflight_v5.py` passes locally (`8/8` scripts verified). Pre-freeze decisions D1–D5, 2026-11-14 gate tightenings, Fable 5.2 forensic fixes (`F2`, `F3`, `F5`–`F13`, `Upgrades 1–5`), and 2026-11-15 `lit-audit` §1.3/§4 + title/scope updates are integrated into the pre-registration. The pre-registration is **not frozen**. **No confirmatory data exists.**
**Design spec:** [../Docs/PREREGISTRATION_VERDICT_TRANSPLANT.md](../Docs/PREREGISTRATION_VERDICT_TRANSPLANT.md) (draft; freeze conditions in §10, R8).
**Next action:** Finish the 7B dev rerun in [results_v5/](results_v5/) (resume `v5dev_conflict_tp_qwen25_7b` and run 7B ChartQA if needed) and run `analyze_v5.py` on the completed `results_v5/`; complete double human coding ([coding_v5/](coding_v5/)); run GPU pre-freeze checks (`preflight_v5.py --check_gpu`, ChartQA `--print_example` render check, `--limit 20` transplant smoke check, and ChartQA `--max_pixels` `200704` vs `501760` on the 30 spent dev items); lock ChartQA `max_pixels` in §3.4; and freeze (commit + tag `prereg-v5`).

> **Token tip for agents:** Never `cat` the JSONL files. The `*_tp_*` files are 10–16 MB. Read the `*.manifest.json` / `*.gates.json` files, the result-folder READMEs, or summarise rows with a short script.

---

## v5 dev pass at a glance (dev only, not findings)

Counts come from the current `results_v5/*.gates.json` (`2026-11-15/16` post-fix rerun under `structured` competency; the prior `2026-11-12/13` pass and its [independent deep audit](<../Thesis/docs/Archive/dev v5/claude_v5_independent_deep_audit.md>) are archived in [archive/results_v5_Prev_backup/](archive/results_v5_Prev_backup/)).

| Model | Math (GSM8K/SVAMP), 200 items: competent → passed gates | ChartQA, 30 items: competent → passed gates |
|---|---|---|
| Qwen2-VL-2B (`qwen2`) | **0 → 0.** Writes no `####` in any of its 1,200 generations, so it fails the format rule (eligibility, not accuracy). No transplant JSONL. | **10 → 0** (`own_absent` 18, `own_undetermined` 2). No transplant JSONL. |
| Qwen2.5-VL-3B (`qwen25`) | **95 → 95** (`11,400` transplant rows complete). | **13 → 5** (`600` transplant rows complete; `own_absent` 10, `gate_answer_leakage` 2). |
| Qwen2.5-VL-7B (`qwen25_7b`) | **154 → 140** (`14,072 / 16,800` transplant rows — **partial**; `gate3_too_many_swaps` 13, `own_undetermined` 1). | **Not yet run** in current `results_v5/` (was `13 → 2` in `archive/results_v5_Prev_backup/`). |

Blocking issues the audits verified on the `2026-11-12/13` pass and their current pre-freeze disposition:
1. **Δℓ validity in Math (addressed by D1):** in the initial pass, the sign of Δℓ at `####` agreed with the actual answer source in only 51.6% (3B) and 56.6% (7B) of rows, and followed evidence order more than the explicit instruction. **D1** promotes behavioural choice shift $\Delta P(Y{=}T)$ at $k=1$ (`structured` parser) to primary in Math, keeping Δℓ secondary/diagnostic.
2. **7B flip contrast (addressed by D2):** in the initial pass, mostly driven by deleting the model's own verdict (`flip` vs. `none` adds 0.10 [−0.09, 0.29] out of a CDE of 1.62). **D2** elevates the matched paraphrase pair (`para_flip - para`) to co-primary alongside `flip - own` and reports the `none` decomposition.
3. **Replay & wording-floor churn (partially open):** on the initial pass, replaying the model's own verdict unchanged shifted the answer source in 6.4% (3B) and 8.2% (7B) of cells (`strict`), and non-binding attributable `image <-> text` churn failed the fixed 5.0% gate in Math dev (7.6% on 3B, 6.6% on 7B; binding passed at 3.2% and 0.0%). Per the 2026-11-14 gate revision, a failing wording floor makes H₀ uninterpretable without blocking H₁.
4. **ChartQA attrition & open checks (D4 + open R8.4):** 5 / (7B pending) / 0 items retained under the current gates. **D4** designates ChartQA exploratory/secondary; the Sentence-1 answer-leakage gate is implemented in `transplant_v5.py`. Finishing 7B in `results_v5/`, running `analyze_v5.py` on the rerun, ChartQA `max_pixels` comparison (R8.4), ChartQA `--print_example` render gate, `verdict_nll` span verification, and double human coding (`coding_v5/`) remain open.
5. **Provenance:** Archived `2026-11-12/13` manifests record only the last invocation and have `resolved_model_commit: null`; fixed in `harness_v4.py`, `harness_v5.py`, `transplant_v5.py`, and `preflight_v5.py` (append-only `invocations[]`, git commit/tag tracking, `resolved_model_commit` populated in the current `results_v5/*.manifest.json`, and `--phase confirm` tag guards).

---

## What v5 adds over v4

Files: `harness_v5.py`, `transplant_v5.py`, `score_v5.py`, `analyze_v5.py`, `sample_v5_for_coding.py`, `preflight_v5.py` (with post-dev fixes also applied to `score_v4.py` and `harness_v4.py`).
1. **Order counterbalancing without letters.** `build_content(..., order)` makes `[instruction, source 1, <image> or text, source 2, format]` with modality headers ("Image:", "Typed text:", "Chart:", "Report:"). Only the sources swap.
2. **Literal K = 4 templates** for the non-binding, binding and explicit arms, in both regimes. A test checks each string against the pre-registration text.
3. **Minimal-edit verdicts:** `own`, `flip`, `none`, `para`, `para_flip`, with the gates of pre-registration §5.3 (including Sentence-1 answer-leakage check) and a per-run `gates.json`.
4. **Regime-split primary outcomes (D1).** Behavioural choice shift $\Delta P(Y{=}T)$ at $k=1$ (`structured` parser; `para_flip - para` co-primary with `flip - own` per D2) in GSM8K/SVAMP (Math), and length-normalized log-likelihood margin Δℓ at `####` (image minus text, with exact token-boundary check) in exploratory ChartQA (D4) and secondary Math. Decoding budgets: 512-token solving for Math, 16-token answer-only for ChartQA. Exact `verdict_nll` span scoring added post-dev.
5. **Benchmarks / ceilings** use the `none` prefill. Explicit arms run only with `none`.
6. **Three models** (2B diagnostic-only per D3; 3B and 7B confirmatory), pinned in `MODEL_PINS` (`harness_v4.py`), all run in `bfloat16`. The harness refuses any other dtype. ChartQA defaults to `--dev_size 30`.

---

## Layout

```
Experiment/
├── README.md               This file
├── RUNBOOK_v4.md           Exact commands, in order (v4)
├── RUNBOOK_v5.md           Exact commands for the v5 dev pass, analysis, and confirm phase
│
├── preflight_v5.py         Pre-flight pin, template, lexicon, script-hash, and GPU/tag checks
├── harness_v5.py           v5 prompts; base and donor stages (GPU)
├── transplant_v5.py        v5 minimal-edit verdicts, gates, Δℓ scoring (GPU)
├── score_v5.py             v5 parser extensions and margin math
├── analyze_v5.py           v5 confirmatory tests (T1, ρ, TOST, floors), readings, lme4 export (local)
├── tests/test_v5.py        v5 harness/scorer tests; no GPU needed
├── tests/test_v5_fixes.py  Regression tests for D1–D5, leakage/split fixes, and coding sampler
├── tests/test_analyze_v5.py  analyze_v5 tests on synthetic rows
│
├── score_v4.py             v4 scorer; also imported by v5
├── harness_v4.py           v4 generation runs (GPU); holds MODEL_PINS and verbatim *_v3 prompts
├── transplant_v4.py        v4 mediator transplant runs (GPU)
├── analyze_v4.py           v4 gates, contrasts, penalty effects (local)
├── reanalyze_v3.py         Re-scores stored v3 outputs (local)
├── statistical_analysis.py Paired statistics for v3; shared helpers (local)
├── sample_for_coding.py    v3 human-coding sheets and scorer validation (local)
├── sample_v5_for_coding.py v5 stratified human-coding sampler & κ evaluator (local)
├── tests/test_v4.py        v4 test suite; no GPU needed
│
├── results_v5/             Current v5 dev rerun (2026-11-15/16): 13 JSONL + 13 manifests + 5 gates + pip_freeze.txt (31,352 rows; 7B partial)
├── results_v4/             v4 smoke, dev2 runs, analysis_dev2/, superseded/ (see its README)
├── results_v3/             Stored v3 pilot, N = 1,619, plus re-analysis (see its README)
├── coding_v5/              v5 human-coding sheets (CODEBOOK_v5.md, HUMAN_CODING_INSTRUCTIONS_v5.md, coder_A/B verdicts & flips), not yet coded
├── coding_v3/              Human-coding sheets (CODEBOOK, coder_A/B; KEY_do_not_open.csv), not yet coded
└── archive/                Superseded v3 harness, v1/v2 pilots, and results_v5_Prev_backup/ (2026-11-12/13 dev pass + analysis_dev/)
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
| Literature knowledge base & pre-freeze audit | Done (`29` local PDFs: 20 core/lead + 6 audit A + 3 cited B; 0 core missing; `16` repo snapshots + 3 read-only comparisons) | [../Docs/Paper/THESIS_LITERATURE_KNOWLEDGE_BASE.md](../Docs/Paper/THESIS_LITERATURE_KNOWLEDGE_BASE.md), [../Docs/Paper/lit-audit-2026-11-15/lit-audit-2026-11-15.md](../Docs/Paper/lit-audit-2026-11-15/lit-audit-2026-11-15.md), [../Docs/RESEARCH_OBJECTIVE.md](../Docs/RESEARCH_OBJECTIVE.md) |
| Freeze audit (2026-11-10) | Received; red light. Its fixes were applied to the pre-registration. | [../Docs/Paper/prereg-freeze-audit/](../Docs/Paper/prereg-freeze-audit/) |
| Pre-registration | Drafted, **not frozen** | [../Docs/PREREGISTRATION_VERDICT_TRANSPLANT.md](../Docs/PREREGISTRATION_VERDICT_TRANSPLANT.md) |
| v5 harness (order, templates, minimal edits, margin, preflight) | Written; **248** CPU tests pass (`unittest`), `preflight_v5.py` `8/8` pass; **ran on an L4 (bf16)** | `harness_v5.py`, `transplant_v5.py`, `score_v5.py`, `preflight_v5.py`, `tests/` |
| v5 dev pass (2B, 3B, 7B; 200 + 30 items) | **Initial pass archived; rerun in progress.** `2026-11-12/13` pass (`29,880` rows) in `archive/results_v5_Prev_backup/`. `2026-11-15/16` rerun in `results_v5/` (`31,352` rows): 2B/3B done; 7B Math transplant `14,072 / 16,800`, 7B ChartQA not yet run. | `results_v5/`, `archive/results_v5_Prev_backup/` |
| v5 dev & plan audits | Done on initial pass: inventory, evidence audit, independent deep audit, forensic audits, v4 vs. post-v5 audit | [../Thesis/docs/Archive/dev v5/](<../Thesis/docs/Archive/dev v5/>), [../Docs/Paper/fable52-prefreeze-audit-2026-11-15.md](../Docs/Paper/fable52-prefreeze-audit-2026-11-15.md) |
| `analyze_v5.py` on dev rows | Done on archived initial pass (`archive/results_v5_Prev_backup/analysis_dev/`); **pending** on current `results_v5/` once 7B finishes | `analyze_v5.py`, `archive/results_v5_Prev_backup/analysis_dev/` |
| Pre-freeze decisions (D1–D5), gate revisions, F2/F3/F5–F13 & `lit-audit` §1.3/§4 | **Applied** in pre-registration & code; ChartQA `max_pixels` (R8.4: `200704` vs `501760`) open | `PREREGISTRATION_VERDICT_TRANSPLANT.md` §10–§11 |
| ChartQA render gate & `verdict_nll` span GPU check | Open | [RUNBOOK_v5.md](RUNBOOK_v5.md) |
| Human coding of verdict & flip labels | Sheets generated (`200` verdicts + `150` flips; instructions ready), not yet coded | `coding_v5/`, `coding_v3/` |
| Confirmatory run | After the pre-registration freeze | GPU (L4/A100), `--phase confirm` |
| Mechanistic probe | Not planned for the thesis core | — |

---

## Rules for working here

- **Dev data is for tuning only.** Don't cite dev numbers (v4 `dev2` or `results_v5/v5dev_*`) as findings.
- **Use a new `--run_tag` after changing prompts or settings.** Reusing a tag resumes the run and skips rows it already has.
- **Primary outcome (regime-split per pre-freeze D1 & D2).** For v4 runs, exact-answer match. For v5 Math (GSM8K/SVAMP), behavioural choice shift $\Delta P(Y{=}T)$ at template $k=1$ (`structured` parser; `para_flip - para` co-primary with `flip - own`), with the log-likelihood margin $\Delta\ell$ at `####` secondary/diagnostic. For ChartQA-Conflict (exploratory per D4), $\Delta\ell$ remains primary. Attempt, refusal, and verdict labels stay heuristic until `coding_v5/` human coding validates them.
- **v5 invariants are mandatory:** counterbalanced order, binding and ceiling arms, minimal-edit verdicts, and competency-filtered primary results. See [../AGENTS.md](../AGENTS.md) §1 and `../CLAUDE.md`.
- **Pre-freeze changes must be logged deviations.** The pre-registration says dev numbers may not change R4/R6. Any change to the competency rule, the ρ definition or the gates needs an explicit, recorded ruling.
- **Keep v3 data read-only.** Prompts in `harness_v4.py` named `*_v3` must stay verbatim; a test enforces this.
- **Model code runs on the GPU session only** (Colab Pro L4/A100 or RunPod; ≥ 22 GiB usable VRAM [L4 23,034 MiB], `bfloat16`; not T4/V100).
  - v5: for dev-phase GPU checks, upload `harness_v4.py`, `score_v4.py`, `harness_v5.py`, `score_v5.py`, `transplant_v5.py`, `sample_v5_for_coding.py`, `analyze_v5.py`, `preflight_v5.py`, and a copy of `Docs/PREREGISTRATION_VERDICT_TRANSPLANT.md`; for `--phase confirm`, run inside a git clone checked out at `prereg-v5` (untracked confirm outputs in `results_v5/` do not dirty `git_provenance()`).
  - v4: upload `harness_v4.py`, `transplant_v4.py`, `score_v4.py`.
  - Everything else runs locally. No model loading on the local machine.
- **After changing code, run the tests:**

```bash
python -B -m unittest discover -s tests
```

---

## Trust order

1. Rows in `results_v5/*.jsonl`, `results_v4/*.jsonl` and `results_v3/full_experiment_results v3.0.json`, plus the `*.manifest.json` / `*.gates.json` files
2. Code in this folder
3. Generated reports, such as `results_v4/analysis_dev2/` and the v5 audits in `../Thesis/docs/Archive/`
4. READMEs like this one, which can go stale
5. `../Docs/` (except the pre-registration and `Docs/Paper/` PDFs): AI-generated notes that describe older paths and overstate v3

`results_v3/statistical_report v3.0.md` and `thesis_contingency_table v3.0.tex` contain verdict wording that the audit rejected. They're kept as a record, so don't cite them.
