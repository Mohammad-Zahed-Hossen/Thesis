# Experiment

Start here. This folder holds all experiment code and data for the thesis.

**Last updated:** 2026-11-10
**Stage:** The v5 harness is written and passes its CPU tests. The v5 dev pass on Colab has not run. No confirmatory data exists yet.
**Design spec:** [../Docs/PREREGISTRATION_VERDICT_TRANSPLANT.md](../Docs/PREREGISTRATION_VERDICT_TRANSPLANT.md) (draft, not frozen; freeze conditions in §10, R8).
**Next action:** run the v5 dev pass with [RUNBOOK_v5.md](RUNBOOK_v5.md) (two models, 200 GSM8K/SVAMP and 30 ChartQA dev items). Then run `analyze_v5.py` on it, record the dev-pass numbers, and freeze.

What v5 adds (`harness_v5.py`, `transplant_v5.py`, `score_v5.py`; the v4 files are unchanged):
1. **Order counterbalancing without letters.** `build_content(..., order)` makes `[instruction, source 1, <image> or text, source 2, format]` with modality headers ("Image:", "Typed text:", "Chart:", "Report:"). Only the sources swap.
2. **Literal K = 4 templates** for the non-binding, binding and explicit arms, in both regimes. A test checks each string against the pre-registration text.
3. **Minimal-edit verdicts:** `own`, `flip`, `none`, `para`, `para_flip`, with the gates of pre-registration §5.3 and a per-run `gates.json`.
4. **Primary outcome Δℓ.** The length-normalized log-likelihood margin at `####`, image minus text, with an exact token-boundary check. Behavioural decodes are secondary (512-token solving for GSM8K/SVAMP, 16-token answer-only for ChartQA).
5. **Ceilings** use the `none` prefill. Explicit arms run only with `none`.
6. **Two models**, pinned in `MODEL_PINS`. ChartQA defaults to `--dev_size 30`.

## Layout

```
Experiment/
├── README.md               This file
├── RUNBOOK_v4.md           Exact commands, in order (v4)
├── RUNBOOK_v5.md           Exact commands for the v5 dev pass
│
├── harness_v5.py           v5 prompts, base and donor stages (Colab)
├── transplant_v5.py        v5 minimal-edit verdicts and margin scoring (Colab)
├── score_v5.py             v5 parser extensions and margin math
├── analyze_v5.py           v5 confirmatory tests, readings, lme4 export (local)
├── tests/test_v5.py        v5 tests; needs no GPU
│
├── score_v4.py             Scorer used by everything below
├── harness_v4.py           Generation runs (Colab)
├── transplant_v4.py        Mediator transplant runs (Colab)
├── analyze_v4.py           Gates, contrasts, penalty effects (local)
├── reanalyze_v3.py         Re-scores stored v3 outputs (local)
├── statistical_analysis.py Paired statistics for v3; shared helpers (local)
├── sample_for_coding.py    Human-coding sheets and scorer validation (local)
├── tests/test_v4.py        Test suite; needs no GPU
│
├── results_v4/             v4 runs and dev analysis (see its README)
├── results_v3/             Stored v3 pilot, N = 1,619 (see its README)
├── coding_v3/              Human-coding sheets, not yet coded
└── archive/                Superseded code and early pilots (see its README)
```

## Status

| Work | Status | Where |
|---|---|---|
| v3 pilot, N = 1,619 | Done; exploratory only | `results_v3/` |
| v3 re-analysis | Done | `results_v3/reanalysis_v3/`, `results_v3/stats_v3_paired/` |
| Harness on a real GPU | Works, T4 and transformers 5.22.2 | `results_v4/*.manifest.json` |
| Dev run (dev2), 15 arms, 200 items | **Complete** (3000 rows, CoT working enabled) | `results_v4/dev2_qwen25.jsonl` |
| Penalty check (dev2) | **Complete** (600 rows, rp=1.05) | `results_v4/dev2_qwen25_rp105.jsonl` |
| Dev transplant (dev2) | **Complete & Valid** (2800 rows, fidelity >95%) | `results_v4/dev2_transplant_qwen25.jsonl` |
| Dev analysis (dev2) | Done. The verdict moves answers under the neutral instruction but not under the conflict instruction; this is dev only, not a finding | `results_v4/analysis_dev2/`, dossier §2.2 |
| Literature dossier | Done | `../Archive/Paper/lit-dossier-verdict-transplant/` |
| Pre-registration | Drafted, not frozen | `../Docs/PREREGISTRATION_VERDICT_TRANSPLANT.md` |
| Freeze audit | Received; its fixes are applied to the pre-registration | `../Archive/Paper/prereg-freeze-audit/` |
| v5 harness (order, templates, minimal edits, margin) | **Written; CPU tests pass**; not yet run on a GPU | `harness_v5.py`, `transplant_v5.py`, `score_v5.py`, `tests/test_v5.py` |
| v5 dev pass (both models, 200 + 30 items) | **Next** | [RUNBOOK_v5.md](RUNBOOK_v5.md) |
| `analyze_v5.py` (T1, ρ, TOST, floors, lme4 export) | **Written; tested on synthetic rows** | `analyze_v5.py`, `tests/test_analyze_v5.py` |
| Human coding of verdict labels | Sheets generated; not yet coded. Needed before any claim based on verdict labels | `coding_v3/` |
| Confirmatory run | After the pre-registration freeze | Colab GPU |
| Mechanistic probe | Not planned for the thesis core | — |

## Rules for working here

- **Dev data is for tuning only.** Don't cite dev numbers as findings.
- **Use a new `--run_tag` after changing prompts or settings.** The same tag resumes, and it won't redo rows it already has.
- **Primary outcome.** For v4 runs, exact-answer match. For v5 runs, the log-likelihood margin Δℓ after a forced `####` only; generated answers are secondary (pre-registration §6). Attempt, refusal and verdict labels stay heuristic until human coding validates them.
- **v5 invariants are mandatory:** counterbalanced order, binding and ceiling arms, minimal-edit verdicts, and competency-filtered primary results. See `../CLAUDE.md`.
- **Keep v3 data read-only.** Prompts in `harness_v4.py` named `*_v3` must stay verbatim; a test enforces this.
- **Model code runs on Colab only.** Upload `harness_v4.py`, `transplant_v4.py` and `score_v4.py`. Everything else runs locally.
- **After changing code, run the tests:**

```bash
python -m unittest discover tests
```

## Trust order

1. Rows in `results_v4/*.jsonl` and `results_v3/full_experiment_results v3.0.json`
2. Code in this folder
3. Generated reports, such as `results_v4/analysis_dev/`
4. READMEs like this one, which can go stale
5. `../Docs/`, AI-generated notes that describe older paths and overstate v3

`results_v3/statistical_report v3.0.md` and `thesis_contingency_table v3.0.tex` contain verdict wording that the audit rejected. They're kept as a record, so don't cite them.
