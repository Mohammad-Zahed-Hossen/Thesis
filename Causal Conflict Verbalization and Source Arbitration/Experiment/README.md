# Experiment

Start here. This folder holds all experiment code and data for the thesis. **It is ground truth** (AGENTS.md §2): code + raw rows outrank every `.md` report, including this one.

**Last updated:** 2026-11-20
**Stage:** The fresh post-fix v5 dev rerun (`2026-11-15/16`) is **complete** in [results_v5/](results_v5/) (**34,920 rows** across `20` `.jsonl` files, `20` `.manifest.json`, `8` `.gates.json`, and `pip_freeze.txt` on an NVIDIA L4 in `bfloat16`), including the `px501k` (`501760`) R8.4 ChartQA comparison and `analyze_v5.py` + `lme4` dev outputs in [results_v5/analysis_dev/](results_v5/analysis_dev/). The initial `2026-11-12/13` dev pass (`29,880` rows + its `analysis_dev/` and dev audits) is preserved in [archive/results_v5_Prev_backup/](archive/results_v5_Prev_backup/README.md). All **255** CPU unit tests pass (`unittest`) and `preflight_v5.py` passes locally (`8/8` scripts verified). Pre-freeze decisions D1–D5, 2026-11-14 gate tightenings, Fable 5.2 forensic fixes (`F2`, `F3`, `F5`–`F13`, `Upgrades 1–5`), and 2026-11-15 `lit-audit` §1.3/§4 + title/scope updates are integrated into the pre-registration. The pre-registration is **frozen** on `main` at tag `prereg-v5` (2026-11-20). **No confirmatory data exists yet.**
**Design spec:** [../Docs/PREREGISTRATION_VERDICT_TRANSPLANT.md](../Docs/PREREGISTRATION_VERDICT_TRANSPLANT.md) (frozen at `prereg-v5`, 2026-11-20; R8 conditions met).
**Next action:** Run confirmatory phase (`--phase confirm`) on GPU from tag `prereg-v5` (see [RUNBOOK_v5.md](RUNBOOK_v5.md) §6). Double human coding is complete and adjudicated ([coding_v5/](coding_v5/): `evaluation_v5.json`, `adjudication_v5.csv`; prereg §8 gate as revised 2026-11-20 passes), and ChartQA `max_pixels` is locked at `200704` in `PREREGISTRATION_VERDICT_TRANSPLANT.md` §3.4.

> **Token tip for agents:** Never `cat` the JSONL files. The `*_tp_*` files are 10–16 MB. Read the `*.manifest.json` / `*.gates.json` files, the result-folder READMEs, or summarise rows with a short script.

---

## v5 dev pass at a glance (dev only, not findings)

Counts come from the current `results_v5/*.gates.json` (`2026-11-15/16` complete post-fix rerun under `structured` competency; the prior `2026-11-12/13` pass and its [independent deep audit](<../Thesis/docs/Archive/dev v5/claude_v5_independent_deep_audit.md>) are archived in [archive/results_v5_Prev_backup/](archive/results_v5_Prev_backup/README.md)).

| Model | Math (GSM8K/SVAMP), 200 items: competent → passed gates | ChartQA (`200704`), 30 items: competent → passed gates | ChartQA `px501k` (`501760`), 30 items |
|---|---|---|---|
| Qwen2-VL-2B (`qwen2`) | **0 → 0.** Writes no `####` in any of its 1,200 generations, so it fails the format rule (eligibility, not accuracy). No transplant JSONL. | **10 → 0** (`own_absent` 18, `own_undetermined` 2). No transplant JSONL. | *(diagnostic-only; not run)* |
| Qwen2.5-VL-3B (`qwen25`) | **95 → 95** (`11,400` transplant rows complete). | **13 → 5** (`600` transplant rows complete; `own_absent` 10, `gate_answer_leakage` 2). | **16 → 1** (`120` rows; `own_absent` 27, `gate_answer_leakage` 1, `gate3_too_many_swaps` 1). |
| Qwen2.5-VL-7B (`qwen25_7b`) | **154 → 140** (`16,800` transplant rows complete; `gate3_too_many_swaps` 13, `own_undetermined` 1). | **13 → 0** (`gate_answer_leakage` 15, `gate3_too_many_swaps` 9). No transplant JSONL. | **17 → 0** (`gate_answer_leakage` 21, `gate3_too_many_swaps` 12). |

Blocking issues verified across the dev audits and their current pre-freeze disposition (full numbers in [results_v5/README.md](results_v5/README.md) and [results_v5/analysis_dev/analysis_v5.md](results_v5/analysis_dev/analysis_v5.md)):
1. **Δℓ validity in Math (addressed by D1):** in both dev passes, Δℓ at `####` tracked the solved answer poorly (sign agreement `52.3%` on 3B, `57.4%` on 7B under `structured` in the fresh rerun; below majority-class baseline), following evidence order more than the explicit instruction. **D1** promotes behavioural choice shift $\Delta P(Y{=}T)$ at $k=1$ (`structured` parser) to primary in Math, keeping Δℓ secondary/diagnostic.
2. **7B flip contrast (addressed by D2):** driven largely by deleting the model's own verdict (`flip - none` = `0.114 [−0.044, 0.270]` vs `none - own` = `1.456` on Δℓ in the fresh rerun). **D2** elevates the matched paraphrase pair (`para_flip - para`) to co-primary alongside `flip - own` and reports the `none` decomposition.
3. **Replay & wording-floor churn (resolved in gate spec; non-binding fails on dev):** in the fresh rerun, replay flips (`donor` vs non-binding `own`) are `2.6%` (3B) and `0.9%` (7B), and the 3-part fixed wording-floor gate **passes** under binding (`−4.7 pp` / `4.5%` on 3B; `−1.1 pp` / `0.0%` on 7B) while **failing** under non-binding (`6.1%` churn on 3B; `−5.4 pp` and `5.8%` churn on 7B). Per the 2026-11-14 gate revision, a failing wording floor makes H₀ uninterpretable without blocking H₁.
4. **ChartQA attrition & R8.4 (D4, locked 2026-11-20):** `5 / 0 / 0` retained at `200704`, and `1 / 0` at `501760` (`px501k` raises competency `13 → 16/17` but lowers gate survival). **D4** designates ChartQA exploratory/secondary; `max_pixels` is locked at `200704` in `PREREGISTRATION_VERDICT_TRANSPLANT.md` §3.4, and ChartQA keeps the §8 minimal-edit gate (`5/13 = 38.5%` on 3B dev would read `NOT A READING`).
5. **Double human coding (complete, 2026-11-20):** verdict labels κ = `0.880` raw / `0.978` canonical (N = 200); adjudicated parser accuracy `168/168` on 3B+7B and `199/200` overall (one 2B error, `V0177`). Flip ratings: agreement `97.3%` / `99.3%`, Gwet's AC1 `0.972` / `0.993` (Cohen's κ `0.326` / `0.000` under near-ceiling base rates; the §8 flip gate now uses agreement + AC1). Coder sheets are kept as submitted; adjudication is in `coding_v5/adjudication_v5.csv`. Blinding was procedural (keys remain in git history). See prereg §11 (2026-11-20) and `Thesis/docs/Archive/claude_coding_v5_independent_audit.md`.
6. **Provenance & `F1` (`verdict_nll` span):** fixed and verified in the fresh rerun (`0` `boundary_mismatch` across `23,136` `dl` rows; `verdict_nll_tokens > 0` on all `15,424` verdict `dl` rows; `resolved_model_commit` populated in all `20` manifests).

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
├── results_v5/             Current v5 dev rerun (2026-11-15/16): 20 JSONL + 20 manifests + 8 gates + pip_freeze.txt + analysis_dev/ (34,920 rows; see its README)
├── results_v4/             v4 smoke, dev2 runs, analysis_dev2/, superseded/ (see its README)
├── results_v3/             Stored v3 pilot, N = 1,619, plus re-analysis (see its README)
├── coding_v5/              v5 human-coding sheets (CODEBOOK_v5.md, HUMAN_CODING_INSTRUCTIONS_v5.md, coder_A/B verdicts & flips as submitted, adjudication_v5.csv, evaluation_v5.json), coded and adjudicated
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
| Literature knowledge base & pre-freeze audit | Done (`29` active local PDFs: 20 core/lead + 6 audit A + 3 cited B; 0 core missing; `16` repo snapshots + 3 read-only comparisons; `1,452` screened records across 2026-11-15 + 2026-11-17 addendum, `6` A + `41` B) | [../Docs/Paper/THESIS_LITERATURE_KNOWLEDGE_BASE.md](../Docs/Paper/THESIS_LITERATURE_KNOWLEDGE_BASE.md), [../Docs/Paper/lit-audit-2026-11-15/lit-audit-2026-11-15.md](../Docs/Paper/lit-audit-2026-11-15/lit-audit-2026-11-15.md), [../Docs/RESEARCH_OBJECTIVE.md](../Docs/RESEARCH_OBJECTIVE.md) |
| Freeze audit (2026-11-10) | Received; red light. Its fixes were applied to the pre-registration. | [../Docs/Paper/prereg-freeze-audit/](../Docs/Paper/prereg-freeze-audit/) |
| Pre-registration | **Frozen** at tag `prereg-v5` (2026-11-20) | [../Docs/PREREGISTRATION_VERDICT_TRANSPLANT.md](../Docs/PREREGISTRATION_VERDICT_TRANSPLANT.md) |
| v5 harness (order, templates, minimal edits, margin, preflight) | Written; **255** CPU tests pass (`unittest`), `preflight_v5.py` `8/8` pass; **ran on an L4 (bf16)** | `harness_v5.py`, `transplant_v5.py`, `score_v5.py`, `preflight_v5.py`, `tests/` |
| v5 dev pass (2B, 3B, 7B; 200 + 30 items) | **Complete (`2026-11-15/16` rerun).** `34,920` rows across `20` JSONL files (`200704` + `px501k` R8.4 ChartQA comparison). Initial `29,880`-row pass archived in `archive/results_v5_Prev_backup/`. | `results_v5/`, `archive/results_v5_Prev_backup/` |
| v5 dev & plan audits | Done on initial pass: inventory, evidence audit, independent deep audit, forensic audits, v4 vs. post-v5 audit | [../Thesis/docs/Archive/dev v5/](<../Thesis/docs/Archive/dev v5/>), [../Docs/Paper/fable52-prefreeze-audit-2026-11-15.md](../Docs/Paper/fable52-prefreeze-audit-2026-11-15.md) |
| `analyze_v5.py` on dev rows | **Done** on current `results_v5/` (`results_v5/analysis_dev/` incl. `lme4_out.txt`); prior `analysis_dev/` archived in `archive/results_v5_Prev_backup/analysis_dev/` | `analyze_v5.py`, `results_v5/analysis_dev/` |
| Pre-freeze decisions (D1–D5), gate revisions, F2/F3/F5–F13 & `lit-audit` §1.3/§4 | **Applied** in pre-registration & code; R8.4 `px501k` comparison run; ChartQA `max_pixels` locked at `200704` in §3.4 (2026-11-20) | `PREREGISTRATION_VERDICT_TRANSPLANT.md` §3.4, §10–§11 |
| ChartQA render gate & `verdict_nll` span GPU check | **Verified** on `2026-11-15/16` GPU rerun (`0` boundary mismatches; `verdict_nll_tokens > 0` on all verdict rows) | [RUNBOOK_v5.md](RUNBOOK_v5.md), `results_v5/README.md` |
| Human coding of verdict & flip labels | Complete and adjudicated (`200` verdicts + `150` flips; verdict κ `0.978` canonical; parser `168/168` on 3B+7B; flip agreement `97.3%` / `99.3%`, AC1 `0.972` / `0.993`) | `coding_v5/`, `coding_v3/` |
| Confirmatory run | After the pre-registration freeze | GPU (L4/A100), `--phase confirm` |
| Mechanistic probe | Not planned for the thesis core | — |

---

## Rules for working here

- **Dev data is for tuning only.** Don't cite dev numbers (v4 `dev2` or `results_v5/v5dev_*`) as findings.
- **Use a new `--run_tag` after changing prompts or settings.** Reusing a tag resumes the run and skips rows it already has.
- **Primary outcome (regime-split per pre-freeze D1 & D2).** For v4 runs, exact-answer match. For v5 Math (GSM8K/SVAMP), behavioural choice shift $\Delta P(Y{=}T)$ at template $k=1$ (`structured` parser; `para_flip - para` co-primary with `flip - own`), with the log-likelihood margin $\Delta\ell$ at `####` secondary/diagnostic. For ChartQA-Conflict (exploratory per D4), $\Delta\ell$ remains primary. Verdict labels from `stated_reliable_source` are validated by `coding_v5/` human coding (`168/168` on 3B+7B, Wilson 95% lower bound `0.978`); attempt and refusal labels remain heuristic.
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
