# v4 Runbook

Exact order for the v4 study. Local means the Ryzen machine; Colab means a T4 or V100 session.

Status on 2026-11-07: steps 2 and 3 have run once, and the gates failed. **Resume at step 3, using the "Dev reruns" commands.** `README.md` holds current status, and `results_v4/README.md` holds the dev details.

## 1. Local, before any GPU

```bash
cd Experiment
python -m unittest tests.test_v4
python reanalyze_v3.py --check --output_dir results_v3/reanalysis_v3
python statistical_analysis.py --results_file "results_v3/full_experiment_results v3.0.json" --output_dir results_v3/stats_v3_paired
python sample_for_coding.py sample --output_dir coding_v3  # already done; don't rerun, it would replace the sheets
```

Give `coding_v3/coder_A.csv`, `coder_B.csv` and `CODEBOOK.md` to two people who code independently. Keep `KEY_do_not_open.csv` away from them. Then run:

```bash
python sample_for_coding.py evaluate --coder_a coding_v3/coder_A.csv --coder_b coding_v3/coder_B.csv --key coding_v3/KEY_do_not_open.csv
```

`evaluate` re-scores the sample with the current `score_v4.py`, so scorer fixes don't require recoding. Check differential accuracy between arms as well as the average. Fix `score_v4.py` if needed, on a fresh sample if the coders have already seen the first. Before step 4, write the pre-registration and freeze the contrasts in `analyze_v4.py`.

## 2. Colab setup

Upload `harness_v4.py`, `transplant_v4.py` and `score_v4.py`, then install:

```bash
pip install transformers accelerate datasets pillow qwen-vl-utils
```

Each run's manifest records the package versions it used. After step 3, `pip freeze` once and use those versions for every later session, so all confirmatory runs share one environment.

## 3. Smoke test and dev phase (uses the first 200 items, proportional by dataset)

```bash
python harness_v4.py --phase dev --arm_set core --limit 8 --run_tag smoke
```

Read the `smoke.jsonl` outputs by eye. Confirm the image reached the model and that `base_image` solves the problem in the picture. Then:

```bash
python harness_v4.py --phase dev --arm_set core --run_tag dev_qwen25
python harness_v4.py --phase dev --arm_set penalty_check --repetition_penalty 1.05 --run_tag dev_qwen25_rp105
python transplant_v4.py --phase dev --donor_file results_v4/dev_qwen25.jsonl --run_tag dev_transplant_qwen25
```

Copy `results_v4/` back and run:

```bash
python analyze_v4.py --runs results_v4/dev_qwen25.jsonl results_v4/dev_transplant_qwen25.jsonl --gates
```

**Gate:** every arm has all its rows, under 5% of outputs hit the token cap, and at least 90% give an answer or a refusal. If not, change `FORMAT` or `--max_new_tokens` and rerun dev under a new `--run_tag`. Dev may be used only for this kind of tuning.

### Dev reruns (current position)

Upload the updated `harness_v4.py`, `transplant_v4.py` and `score_v4.py` first. To fill the 16 missing rows only:

```bash
python harness_v4.py --phase dev --arm_set core --run_tag dev_qwen25
```

To rerun the transplant, whose first run is invalid:

```bash
python transplant_v4.py --phase dev --donor_file results_v4/dev_qwen25.jsonl --run_tag dev_transplant_qwen25_v2
```

If `FORMAT` or another prompt changes, rerun all of it under new tags instead:

```bash
python harness_v4.py --phase dev --arm_set core --run_tag dev2_qwen25
python harness_v4.py --phase dev --arm_set penalty_check --repetition_penalty 1.05 --run_tag dev2_qwen25_rp105
python transplant_v4.py --phase dev --donor_file results_v4/dev2_qwen25.jsonl --run_tag dev2_transplant_qwen25
```

The runs print `INCOMPLETE` and exit 1 if any row is missing.

Also check here:

- **`base_image` accuracy.** v3 limited images to `max_pixels` of about 200k, while source images are 900 pixels wide. If rendered text is hard to read, raise `--max_pixels` for every arm before step 4.
- **Fidelity.** Prefilling a model's own verbalization should mostly reproduce its own answer. If it doesn't, transplant effects can't be interpreted.
- **Penalty.** Pass both runs to `analyze_v4.py`, which prints the paired comparison. A large difference means v3's results depended partly on the penalty. The first dev run showed one, so decide how to report the penalty before freezing.

## 4. Confirmatory phase (freeze first; no changes after this)

```bash
python harness_v4.py --phase confirm --arm_set core --run_tag confirm_qwen25
python transplant_v4.py --phase confirm --donor_file results_v4/confirm_qwen25.jsonl --run_tag transplant_qwen25
python harness_v4.py --phase confirm --arm_set penalty_check --repetition_penalty 1.05 --run_tag confirm_qwen25_rp105
```

Sessions can die. Rerun the same command with the same `--run_tag` and it resumes. Save `results_v4/` to Drive between batches.

## 5. Replication and external validity

```bash
python harness_v4.py --phase confirm --arm_set replication_model --model_id Qwen/Qwen2-VL-2B-Instruct --run_tag confirm_qwen2
python transplant_v4.py --phase confirm --model_id Qwen/Qwen2-VL-2B-Instruct --donor_file results_v4/confirm_qwen2.jsonl --run_tag transplant_qwen2
python harness_v4.py --split chartqa --phase all --arm_set chartqa --run_tag chartqa_qwen25
python transplant_v4.py --split chartqa --phase all --donor_file results_v4/chartqa_qwen25.jsonl --run_tag transplant_chartqa_qwen25
```

ChartQA's dataset page shows 230 rows while Ghosh et al. report 229 after a post-run audit. Find out which item failed, and record the decision before analysing.

## 6. Variance (replaces multi-seed, since greedy decoding has no seed variance)

```bash
python harness_v4.py --phase dev --arm_set paraphrase --paraphrase 1 --run_tag para1_qwen25
python harness_v4.py --phase dev --arm_set paraphrase --paraphrase 2 --run_tag para2_qwen25
python harness_v4.py --phase dev --arm_set paraphrase --do_sample --seed 1 --run_tag sample1_qwen25
python harness_v4.py --phase dev --arm_set paraphrase --do_sample --seed 2 --run_tag sample2_qwen25
```

## 7. Analysis, local

```bash
python analyze_v4.py --runs results_v4/confirm_qwen25.jsonl results_v4/transplant_qwen25.jsonl results_v4/confirm_qwen25_rp105.jsonl results_v4/confirm_qwen2.jsonl results_v4/transplant_qwen2.jsonl results_v4/chartqa_qwen25.jsonl results_v4/transplant_chartqa_qwen25.jsonl --output_dir results_v4/analysis --export_long
```

Fit the crossed mixed model in R from `results_v4/analysis/long.csv`. The formula is at the top of `analyze_v4.py`.

## Reading the result


| Pattern                                                           | Interpretation                                              |
| ------------------------------------------------------------------- | ------------------------------------------------------------- |
| m moves the answer with z fixed, in the stated direction          | Evidence for steering                                       |
| z moves the answer with m fixed; m doesn't                        | Instruction effect; the verbalization looks like commentary |
| `filler` is near `direct`, and description order flips the source | v3's "visual capture" came from the placebo                 |
| Same-meaning prefills change answers about as much as m does      | Sensitivity to wording; don't claim a content effect        |
