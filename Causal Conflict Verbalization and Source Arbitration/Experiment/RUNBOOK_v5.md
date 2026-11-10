# v5 Runbook: verdict transplant

These are the exact commands for the v5 dev pass, which the pre-registration requires before it can be frozen (`../Docs/PREREGISTRATION_VERDICT_TRANSPLANT.md`, §10 R8). "Local" means the Ryzen machine, which has no CUDA. "Colab" means a T4 or V100 session.

The dev pass uses **items that are already spent**: the 200 GSM8K/SVAMP dev items and the 30 ChartQA dev items. Nothing here produces confirmatory data.

## 1. Local, before any GPU

```bash
cd Experiment
python -m unittest discover tests
python harness_v5.py --dry_run --print_example --run_tag x
```

The second command prints the prompt layout using the fake template. It should show the instruction first, then the two sources (image first, then typed text, then the reverse), then the format line, and no "Source A/B".

## 2. Colab setup

Upload these files into one folder: `harness_v4.py`, `score_v4.py`, `harness_v5.py`, `score_v5.py`, `transplant_v5.py`. Then:

```bash
pip install transformers accelerate datasets pillow qwen-vl-utils
```

Use the versions recorded in the v4 manifests if you can (transformers 5.22.2 on T4). Run `pip freeze > results_v5/pip_freeze.txt` once, before step 3.

## 3. Render gate (prereg §8): real chat template, both orders

```bash
python harness_v5.py --print_example --split conflict --phase dev --run_tag render_check --model_id Qwen/Qwen2.5-VL-3B-Instruct
python harness_v5.py --print_example --split conflict --phase dev --run_tag render_check --model_id Qwen/Qwen2-VL-2B-Instruct
python harness_v5.py --print_example --split chartqa  --phase dev --run_tag render_check --model_id Qwen/Qwen2.5-VL-3B-Instruct
```

Check every printout:
- `<|vision_start|><|image_pad|><|vision_end|>` sits right after `Image: ` (or `Chart: `).
- The typed text or report block is on the other side of the image in each order.
- The instruction comes before both sources and the format line after them.
- The assistant turn ends in the prefill `The verdict.\n\n####`.

If anything differs from §4.1, **stop**: the real template doesn't match the test double in `harness_v5.fake_qwen_chat_template`.

## 4. Dev pass: one block per model and regime

Run all four blocks:

| Block | MODEL | TAG | SPLIT |
|---|---|---|---|
| 1 | `Qwen/Qwen2.5-VL-3B-Instruct` | `qwen25` | `conflict` |
| 2 | `Qwen/Qwen2-VL-2B-Instruct` | `qwen2` | `conflict` |
| 3 | `Qwen/Qwen2.5-VL-3B-Instruct` | `qwen25` | `chartqa` |
| 4 | `Qwen/Qwen2-VL-2B-Instruct` | `qwen2` | `chartqa` |

Set the variables for one block, then run its three stages:

```bash
MODEL=Qwen/Qwen2.5-VL-3B-Instruct; TAG=qwen25; SPLIT=conflict
```

```bash
python harness_v5.py --stage base  --split $SPLIT --phase dev --model_id $MODEL --run_tag v5dev_${SPLIT}_base_$TAG
```

```bash
python harness_v5.py --stage donor --split $SPLIT --phase dev --model_id $MODEL --run_tag v5dev_${SPLIT}_donor_$TAG
```

```bash
python transplant_v5.py --split $SPLIT --phase dev --model_id $MODEL \
  --base_file results_v5/v5dev_${SPLIT}_base_$TAG.jsonl \
  --donor_file results_v5/v5dev_${SPLIT}_donor_$TAG.jsonl \
  --run_tag v5dev_${SPLIT}_tp_$TAG
```

Notes:
- ChartQA uses `--dev_size 30` automatically. The harness refuses values of 100 or more.
- Every stage resumes if it is interrupted: rerun the same command with the same `--run_tag`. A new tag is needed only after changing code, prompts or settings.
- To see the gate counts without decoding anything, add `--gates_only` to the transplant command. It writes `results_v5/<run_tag>.gates.json`.
- `--batch_size` applies to generation only. Margin scoring runs one request at a time; each request is two teacher-forced forward passes.

### ChartQA `max_pixels` (R8.4)

The default is `--max_pixels 200704` (256·28·28), the same as GSM8K/SVAMP. Charts carry small text. If the ChartQA `base_image` yield in block 3 is low, rerun **only blocks 3 and 4** under new tags with `--max_pixels 401408` (512·28·28). Keep whichever value the pre-registration records before the freeze. Do not change it afterwards.

## 5. What to bring back

Copy `results_v5/` to the local machine. For each block, record these into the pre-registration's deviation log, or into a dev-pass note beside it (R8.3):

| Quantity | Where it comes from |
|---|---|
| Competency yield | `gates.json`: `competent` out of `items` |
| Edit-gate pass rate | `gates.json`: `passed` out of `competent`, plus `fail_reasons_by_order` |
| ChartQA answer-only decodes matching *a_I* or *a_T* | `beh` rows, scored with `score_v5.behavioural_source` |
| Dev wording floor | `beh` rows: change rate and mean difference, `para` vs `own`, per binding level |
| Boundary mismatches | Share of `dl` rows with `boundary_mismatch: true` (gate: ≤ 1%) |
| Whitespace token | `ws_skipped` in `dl` rows: 2 means a separate space token was skipped for both candidates, 0 means the tokenizer has none |
| Manipulation check | `free_binding` vs `donor` rows of the donor file: share of answers that follow the stated verdict |
| Seconds per item | Sum of `wall_s` over an item's rows, from the transplant file |

Then run the analysis locally. It reports most of the quantities above, plus T1, ρ, TOST and every secondary analysis:

```bash
python analyze_v5.py --runs results_v5/v5dev_*_tp_*.jsonl --gates results_v5/v5dev_*_tp_*.gates.json \
  --base results_v5/v5dev_*_base_*.jsonl --donor results_v5/v5dev_*_donor_*.jsonl --output_dir results_v5/analysis_dev
```

It writes:
- `analysis_v5.md` and `analysis_v5.json`;
- `long_v5.csv`;
- `analyze_v5_lme4.R`, for the model-based fits.

R is not installed locally, so run the fits on Colab:

```bash
apt-get install -y r-base && Rscript -e 'install.packages("lme4", repos="https://cloud.r-project.org")'
```

```bash
Rscript results_v5/analysis_dev/analyze_v5_lme4.R results_v5/analysis_dev/long_v5.csv results_v5/analysis_dev/lme4_out.txt
```

Dev numbers go into the freeze record. They are not findings, and they don't change R3, R4 or R7.

## 6. After the freeze (not yet)

1. Tag `prereg-v5`.
2. Run the base stage with `--phase confirm` over the whole confirm pool.
3. Run the donor stage.
4. Run `transplant_v5.py --phase confirm --n_competent 250`. Record the tag hash in each manifest.
