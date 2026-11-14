# v5 Dev Pass: Evidence Audit and Interpretation Boundary

**Audit date:** 2026-11-13
**Scope:** The v5 Colab transcript, every artifact in `Experiment/results_v5/`, active v5 code, manifests, gate reports, and the two available runbooks.
**Status:** Development data only. No confirmatory result or claim is established by this report.

## Executive assessment

[Verified] The v5 development pass produced a complete, parseable, internally consistent set of stored rows for all six planned model × regime blocks. The primary likelihood-margin computation has no recorded token-boundary failures and is numerically reproducible from the stored transplant rows.

[Verified] The pass identifies several matters that must be decided or recorded before preregistration freeze: Qwen2-VL-2B has no strictly valid Math competency rows; ChartQA retains too few items after the donor/edit gates; the recorded Colab transcript lacks the three ChartQA template-render checks required by the active runbook; and the behavioural wording-floor diagnostic fails in both retained Math models.

[Inferred] The large dev likelihood effects in the retained Math samples are useful for checking the machinery and calibrating the design, but they are not findings. They come from spent dev items and both retained counts are below the analysis code's 150-item minimum.

## Evidence hierarchy and inventory

The stored JSONL rows, gate reports, manifests, and active code are the evidence base. The README and the Thesis-side runbook are tracking documents; they are useful for comparison but are not treated as authoritative when they conflict with code or outputs.

`results_v5/` contains 39 artifacts: 16 JSONL files, 16 paired manifests, six gate reports, and `pip_freeze.txt`. There are 29,880 JSONL rows in total:

| Stage | Rows | Structure |
|---|---:|---|
| Base | 2,760 | generation and gold-answer likelihood rows |
| Donor | 2,760 | `donor` and `free_binding` generations in both orders |
| Transplant | 24,360 | 19,488 primary `dl` rows and 4,872 secondary `beh` rows |

Every JSONL line parses. Each `(id, key, outcome)` tuple occurs once. Every transplant file has the expected 120 rows per gate-passing item: 96 primary likelihood rows and 24 behavioural rows. All primary rows have finite `dl` values and `boundary_mismatch: false`; all have `ws_skipped: 2`, meaning a separate whitespace token was skipped before both candidate answers.

## Execution environment and provenance

[Verified] All manifests record an NVIDIA L4, CUDA 13.0, Python 3.13.16, and `torch.bfloat16`. `pip_freeze.txt` records `torch==2.14.1+cu130`, `transformers==5.22.1`, `accelerate==1.15.0`, `datasets==4.8.5`, `pillow==11.3.0`, and `qwen-vl-utils==0.0.14`.

| Model | Requested revision | Batch size | Peak recorded VRAM |
|---|---|---:|---:|
| Qwen2-VL-2B-Instruct | `895c3a49bc3fa70a340399125c650a463535e71c` | 8 | 4.11 GB |
| Qwen2.5-VL-3B-Instruct | `66285546d2b821cf421d4f5eb2576359d3770cd3` | 8 | 6.99 GB |
| Qwen2.5-VL-7B-Instruct | `cc594898137f460bfe9f0759e9844b3ce807cfb5` | 2 | 15.70 GB |

The requested dataset revisions are distinct: Math conflict uses `2c55b099f286554685798d54cea4bde761d486b7`, while ChartQA uses `7d15a9704bc5e028e7038ef98aa7917059535bf8`. The hashes recorded in the manifests match the currently audited `harness_v5.py`, `transplant_v5.py`, `score_v5.py`, `harness_v4.py`, and `score_v4.py`.

[Caveat] `environment.resolved_model_commit` is blank in all manifests. The configured revision is present and code passes it to the Hugging Face loaders, but the runtime did not independently record the resolved commit.

## Runbook and transcript audit

The Colab transcript verifies the L4 selection and real chat-template render check for all three models on the Math split. It shows the correct modality headers, vision-token placement, evidence-order swap, and assistant prefill ending `The verdict.\n\n####`.

[Verified] The active `Experiment/RUNBOOK_v5.md` requires six render checks: three Math and three ChartQA. The Thesis-side runbook and saved transcript contain only the three Math checks. This is an incomplete recorded render-gate audit, even though the later ChartQA rows are present.

The two runbooks also differ in their local analysis command. The active runbook supplies base and donor files, allowing manipulation and uncertainty diagnostics; the Thesis-side runbook omits those inputs. No saved `results_v5/analysis_dev/` directory or logged local `analyze_v5.py` execution is present. The calculations reported below were recomputed read-only from the stored rows using the active analysis functions; no output files were created during this audit.

## Stage 1: strict competency conditioning

| Regime | Model | Valid generation rows | Strictly correct rows | Competent items |
|---|---|---:|---:|---:|
| Math, 200 dev items | 2B | 400 | 0 | 0 |
| Math, 200 dev items | 3B | 400 | 252 | 80 |
| Math, 200 dev items | 7B | 400 | 316 | 124 |
| ChartQA, 30 dev items | 2B | 60 | 30 | 10 |
| ChartQA, 30 dev items | 3B | 60 | 40 | 13 |
| ChartQA, 30 dev items | 7B | 60 | 41 | 13 |

[Verified] In Math, all 400 Qwen2-VL-2B base generations were parsed as `fallback_last_number`, which the v5 strict rule deliberately treats as invalid. This is a formatting/parser eligibility failure, not evidence that every numerical answer was wrong. The 3B and 7B models respectively had 90 and 51 Math responses on this fallback path; remaining strict-format rates were 310/400 and 349/400.

## Stage 2 and gates: donor-verdict quality

The natural Math verdicts show a large order asymmetry. For Qwen2.5-VL-3B, `text_first` led to a typed-text verdict in 199/200 donor rows; for Qwen2.5-VL-7B it did so in 200/200. This is a direct empirical reason to retain counterbalanced order in the design.

| Regime | Model | Competent | Passed gates | Pass rate among competent | Primary attrition |
|---|---|---:|---:|---:|---|
| Math | 2B | 0 | 0 | — | no competent items |
| Math | 3B | 80 | 80 | 100.0% | none |
| Math | 7B | 124 | 115 | 92.7% | 8 too-many-swaps; 1 undetermined |
| ChartQA | 2B | 10 | 0 | 0.0% | 18 absent; 2 undetermined |
| ChartQA | 3B | 13 | 6 | 46.2% | 11 absent |
| ChartQA | 7B | 13 | 2 | 15.4% | 8 too-many-swaps; 3 absent; 1 wrong-regime label |

The retained flip edits meet the specified Jaccard threshold: Math 3B mean/min 0.9455/0.8800; Math 7B 0.9549/0.8750; ChartQA 3B 0.8936/0.8667; and ChartQA 7B 0.9774/0.9481. Therefore, attrition is primarily an eligibility issue rather than a failure of edit similarity among retained items.

## Primary likelihood-margin calculations

The following values are reproducible from the transplant JSONLs with the active `analyze_v5.py` functions and seed 42. They are descriptive dev calculations only.

| Model and regime | Analysed items | Code minimum | Mean ceiling | Binding CDE / rho | Non-binding CDE / rho | Binding DiD |
|---|---:|---:|---:|---:|---:|---:|
| 3B Math | 80 | 150 | 0.1524 | 0.2330 / 1.529 | 0.1499 / 0.984 | 0.0830 |
| 7B Math | 115 | 150 | 1.4228 | 1.6188 / 1.138 | 1.3421 / 0.943 | 0.2767 |
| 3B ChartQA | 6 | 100 | 1.1479 | 0.4608 / 0.401 | 0.3567 / 0.311 | 0.1041 |
| 7B ChartQA | 2 | 100 | 0.9562 | 0.2330 / 0.244 | 0.1722 / 0.180 | 0.0609 |

[Verified] The Math 3B and 7B raw calculations have positive one-sided sign-flip statistics (`p=0.00010`, Holm `p=0.00050` for each). The 3B ChartQA calculation has raw `p=0.01570`, Holm `p=0.04710`. These values must not be presented as confirmatory hypothesis-test results because these are dev items and none of the four groups meets its coded minimum sample size.

[Interpretation boundary] A rho above one is mathematically possible: the minimal verdict transplant may change likelihood more than the explicit-instruction ceiling contrast. It is not evidence that the effect is physically bounded by one, nor a reason to call the dev result confirmatory.

## Secondary diagnostics

[Verified] The behavioural wording-floor check fails in both retained Math models. Binding/non-binding paraphrase churn is 25.6%/28.1% for 3B and 20.4%/20.4% for 7B, exceeding the 5% ceiling. This restricts inference from discrete behavioural decodes; it does not invalidate the separately computed primary teacher-forced likelihood margins.

[Verified] In the Math size comparison, the 3B/7B common retained set is 50 items. The corresponding binding rho values are 1.369 and 1.056, respectively; the paired difference (7B minus 3B) is -0.314 with 95% bootstrap CI [-0.784, 0.050]. This is a secondary, descriptive comparison only.

The 3B Math transplant has 13 behavioural rows that hit the generation cap (13/1,920); no other transplant behavioural file has capped rows. The primary `dl` outcomes are unaffected by that generation cap.

## Required interpretation boundary

1. All reported values come from the spent development split. They must inform the freeze record and design decisions, not the thesis's substantive empirical claims.
2. The active analysis code marks every available group as `meets_min_items: false`: Math requires 150 retained items and ChartQA requires 100.
3. No Qwen2-VL-2B Math primary result exists because no item passed strict competency. No Qwen2-VL-2B ChartQA primary result exists because no item passed all gates.
4. ChartQA has a design-feasibility issue: even its full 199-item confirm pool may not yield 100 retained items at the observed dev rates. This is a planning concern, not a conclusion about the models.
5. The existing Antigravity report contains several corrected factual and interpretive statements. It should be read only after the targeted corrections recorded in this audit cycle.

## Files audited

- `Thesis/docs/Archive/v5_dev_output.md`
- `Thesis/docs/Archive/v5_antigravity_analysis.md`
- `Thesis/docs/RUNBOOK/RUNBOOK_V5.md`
- `Experiment/RUNBOOK_v5.md`, `Experiment/README.md`
- all JSONL, manifest, gate, and environment files under `Experiment/results_v5/`
- `Experiment/harness_v4.py`, `harness_v5.py`, `score_v5.py`, `transplant_v5.py`, and `analyze_v5.py`
