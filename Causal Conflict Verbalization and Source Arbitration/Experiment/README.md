# Experiment

Start here. This folder holds all experiment code and data for the thesis.

**Last updated:** 2026-11-10
**Stage:** v4 dev phase is closed. The harness is being upgraded to v5 for the verdict-transplant study. No confirmatory data exists yet.
**Design spec:** [../Docs/PREREGISTRATION_VERDICT_TRANSPLANT.md](../Docs/PREREGISTRATION_VERDICT_TRANSPLANT.md) (draft, not frozen).
**Next action:** implement the v5 upgrade (see the list below). Then do a dev smoke run on both models, resolve the open decisions in pre-registration §10, and freeze it.

The v5 upgrade adds:
1. **Order counterbalancing.** `render_chat` takes an order argument: `[instruction, source 1, source 2, format]`, with the instruction fixed and only the sources swapped. Today the image always comes first (`harness_v4.py:290-292`).
2. **Binding and ceiling arms.** Non-binding, binding and explicit image/text templates, K = 4 paraphrases each (pre-registration §4).
3. **Minimal-edit transplants.** `m_own` / `m_flip` / `m_none` / `m_para`, built from each item's own verbalization, with the Jaccard ≥ 0.85 and single-clause gates (pre-registration §5).
4. **Short-horizon outcome.** A forced `####`, a decode of at most 16 tokens, and the log-likelihood margin between the image and text answers (pre-registration §6).
5. **Dual-model execution.** `Qwen/Qwen2.5-VL-3B-Instruct` and `Qwen/Qwen2-VL-2B-Instruct`, pinned in `MODEL_PINS`.
6. **ChartQA dev size.** ChartQA needs `--dev_size 30`; the default of 200 leaves only 29 confirm items.

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
| Dev run (dev2), 15 arms, 200 items | **Complete** (3000 rows, CoT working enabled) | `results_v4/dev2_qwen25.jsonl` |
| Penalty check (dev2) | **Complete** (600 rows, rp=1.05) | `results_v4/dev2_qwen25_rp105.jsonl` |
| Dev transplant (dev2) | **Complete & Valid** (2800 rows, fidelity >95%) | `results_v4/dev2_transplant_qwen25.jsonl` |
| Dev analysis (dev2) | Done. The verdict moves answers under the neutral instruction but not under the conflict instruction; this is dev only, not a finding | `results_v4/analysis_dev2/`, dossier §2.2 |
| Literature dossier | Done | `../Archive/Paper/lit-dossier-verdict-transplant/` |
| Pre-registration | Drafted, not frozen | `../Docs/PREREGISTRATION_VERDICT_TRANSPLANT.md` |
| v5 harness upgrade (order, binding/ceiling, minimal edits, short horizon) | **In progress** | `harness_v4.py`, `transplant_v4.py`, `score_v4.py` |
| Qwen2-VL-2B runs | After the v5 upgrade | Colab GPU |
| ChartQA-Conflict runs | After the v5 upgrade, with `--dev_size 30` | Colab GPU |
| Human coding of verdict labels | Sheets generated; not yet coded. Needed before any claim based on verdict labels | `coding_v3/` |
| Confirmatory run | After the pre-registration freeze | Colab GPU |
| Mechanistic probe | Not planned for the thesis core | — |

## Rules for working here

- **Dev data is for tuning only.** Don't cite dev numbers as findings.
- **Use a new `--run_tag` after changing prompts or settings.** The same tag resumes, and it won't redo rows it already has.
- **Primary outcome.** For v4 runs, exact-answer match. For v5 runs, the short-horizon decode and log-likelihood margin after a forced `####` (pre-registration §6). Attempt, refusal and verdict labels stay heuristic until human coding validates them.
- **v5 invariants are mandatory:** counterbalanced order, binding and ceiling arms, minimal-edit verdicts, and competency-filtered primary results. See `../CLAUDE.md`.
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
