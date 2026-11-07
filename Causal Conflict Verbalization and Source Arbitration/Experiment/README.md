# Experiment

Start here. This folder holds all experiment code and data for the thesis.

**Last updated:** 2026-11-07
**Stage:** v4 dev phase, gates failing. No confirmatory data exists yet.
**Next action:** fix the dev gates, rerun the dev transplant, then see [RUNBOOK_v4.md](RUNBOOK_v4.md). See [results_v4/README.md](results_v4/README.md) for details.

## Layout

```
Experiment/
├── README.md               This file
├── RUNBOOK_v4.md           Exact commands, in order
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
| Harness on a real GPU | Works, T4 and transformers 5.22.0 | `results_v4/*.manifest.json` |
| Dev run, 15 arms, 200 items | 16 rows missing in `direct_v3`; gates failing | `results_v4/dev_qwen25.jsonl` |
| Penalty check, dev | Done | `results_v4/dev_qwen25_rp105.jsonl` |
| Dev transplant | **Invalid, must rerun** | `results_v4/superseded/` |
| Human coding of outputs | Not started; sheets are blank | `coding_v3/` |
| Pre-registration | Not written | None |
| Confirmatory run | Not started | None |
| Qwen2-VL-2B, ChartQA, variance runs | Not started | None |
| Mechanistic probe | Not started; no code yet | None |

## Rules for working here

- **Dev data is for tuning only.** Don't cite dev numbers as findings.
- **Use a new `--run_tag` after changing prompts or settings.** The same tag resumes, and it won't redo rows it already has.
- **Exact-answer match is the primary outcome.** Attempt, refusal and verdict labels stay heuristic until human coding validates them.
- **Keep v3 data read-only.** Prompts in `harness_v4.py` named `*_v3` must stay verbatim; a test enforces this.
- **Model code runs on Colab only.** Upload `harness_v4.py`, `transplant_v4.py` and `score_v4.py`. Everything else runs locally.
- **After changing code, run the tests:**

```bash
python -m unittest tests.test_v4
```

## Trust order

1. Rows in `results_v4/*.jsonl` and `results_v3/full_experiment_results v3.0.json`
2. Code in this folder
3. Generated reports, such as `results_v4/analysis_dev/`
4. READMEs like this one, which can go stale
5. `../Docs/`, AI-generated notes that describe older paths and overstate v3

`results_v3/statistical_report v3.0.md` and `thesis_contingency_table v3.0.tex` contain verdict wording that the audit rejected. They're kept as a record, so don't cite them.
