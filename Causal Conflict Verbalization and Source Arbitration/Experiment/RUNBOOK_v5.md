# v5 Runbook: verdict transplant

These are the exact commands for the v5 dev pass, which the pre-registration requires before it can be frozen (`../Docs/PREREGISTRATION_VERDICT_TRANSPLANT.md`, §10 R8). "Local" means the Ryzen machine, which has no CUDA. "GPU" means a session on the pre-registered GPU class (§3.4): CUDA compute capability ≥ 8 and at least 24 GB, for example an NVIDIA L4 or A100 on Colab Pro, or an RTX 3090/4090. **Do not use a T4 or V100.** On those the loader falls back to `float16`, and `harness_v5.HFBackend` stops with an error; the 7B model would not fit anyway.

Three models are run, all confirmatory: `Qwen/Qwen2-VL-2B-Instruct`, `Qwen/Qwen2.5-VL-3B-Instruct` and `Qwen/Qwen2.5-VL-7B-Instruct`. Run every stage of one model × regime on the same GPU model.

The dev pass uses **items that are already spent**: the 200 GSM8K/SVAMP dev items and the 30 ChartQA dev items. Nothing here produces confirmatory data.

## 1. Local, before any GPU

```bash
cd Experiment
python -B -m unittest discover -s tests
python harness_v5.py --dry_run --print_example --run_tag x
python harness_v5.py --dry_run --print_example --model_id Qwen/Qwen2.5-VL-7B-Instruct --run_tag test_7b_render
```

The second command prints the prompt layout using the fake template. It should show the instruction first, then the two sources (image first, then typed text, then the reverse), then the format line, and no "Source A/B". The dry run uses the same fake template for every model, so the third command only confirms that the 7B model id is accepted. The real 7B template is checked in step 3.

## 2. GPU session setup

Upload these files into one folder: `harness_v4.py`, `score_v4.py`, `harness_v5.py`, `score_v5.py`, `transplant_v5.py`. Then:

```bash
pip install transformers accelerate datasets pillow qwen-vl-utils
```

Use the transformers version recorded in the v4 manifests if you can (5.22.2), and the same versions for all three models. Check the GPU first: `nvidia-smi` should show an L4, A100 or RTX 3090/4090. Run `pip freeze > results_v5/pip_freeze.txt` once, before step 3.

## 3. Render gate (prereg §8): real chat template, both orders

```bash
python harness_v5.py --print_example --split conflict --phase dev --run_tag render_check --model_id Qwen/Qwen2.5-VL-3B-Instruct
python harness_v5.py --print_example --split conflict --phase dev --run_tag render_check --model_id Qwen/Qwen2-VL-2B-Instruct
python harness_v5.py --print_example --split conflict --phase dev --run_tag render_check --model_id Qwen/Qwen2.5-VL-7B-Instruct
python harness_v5.py --print_example --split chartqa  --phase dev --run_tag render_check --model_id Qwen/Qwen2.5-VL-3B-Instruct
python harness_v5.py --print_example --split chartqa  --phase dev --run_tag render_check --model_id Qwen/Qwen2-VL-2B-Instruct
python harness_v5.py --print_example --split chartqa  --phase dev --run_tag render_check --model_id Qwen/Qwen2.5-VL-7B-Instruct
```

Each command prints both orders (`image_first`, then `text_first`). `--print_example` loads only the processor, so it needs no GPU memory. The three pinned revisions ship the same chat template (checked on the Hub on 2026-11-11), so the six printouts should differ only in the item text.

Check every printout:

- `<|vision_start|><|image_pad|><|vision_end|>` sits right after `Image: ` (or `Chart: `).
- The typed text or report block is on the other side of the image in each order.
- The instruction comes before both sources and the format line after them.
- The assistant turn ends in the prefill `The verdict.\n\n####`.

If anything differs from §4.1, **stop**: the real template doesn't match the test double in `harness_v5.fake_qwen_chat_template`.

## 4. Dev pass: one block per model and regime

Run all six blocks:


| Block | MODEL                         | TAG         | SPLIT      |
| ------- | ------------------------------- | ------------- | ------------ |
| 1     | `Qwen/Qwen2.5-VL-3B-Instruct` | `qwen25`    | `conflict` |
| 2     | `Qwen/Qwen2-VL-2B-Instruct`   | `qwen2`     | `conflict` |
| 3     | `Qwen/Qwen2.5-VL-3B-Instruct` | `qwen25`    | `chartqa`  |
| 4     | `Qwen/Qwen2-VL-2B-Instruct`   | `qwen2`     | `chartqa`  |
| 5     | `Qwen/Qwen2.5-VL-7B-Instruct` | `qwen25_7b` | `conflict` |
| 6     | `Qwen/Qwen2.5-VL-7B-Instruct` | `qwen25_7b` | `chartqa`  |

Set the variables for one block, then run its three stages:

```bash
MODEL=Qwen/Qwen2.5-VL-3B-Instruct; TAG=qwen25; SPLIT=conflict; BS=8
```

**Batch size for the 7B model (mandatory on 24 GB).** The 7B weights take about 16.6 GB in `bfloat16`, which leaves roughly 6 GB on a 24 GB card.


| GPU                       | 2B and 3B | 7B     |
| --------------------------- | ----------- | -------- |
| 24 GB (L4, RTX 3090/4090) | `BS=8`    | `BS=2` |
| 40 or 80 GB (A100)        | `BS=8`    | `BS=8` |

- `--batch_size` matters in **all three stages**, because each one generates: the base stage (512-token solving), the donor stage, and the behavioural rows of the transplant.
- Margin scoring ignores it: it always runs one request at a time.
- Batch size is not expected to change greedy outputs, but padding can shift low-order bits. Use one value for all stages of a model × regime, and record it (it is in the manifest).
- An out-of-memory batch is split in half and retried automatically. If that happens often, lower `BS` and start again under a new tag.
- The 24 GB figures are estimates, not measurements. Read `peak_vram_gb` in the first 7B manifest before running the rest.

So for block 5:

```bash
MODEL=Qwen/Qwen2.5-VL-7B-Instruct; TAG=qwen25_7b; SPLIT=conflict; BS=2
```

```bash
python harness_v5.py --stage base  --split $SPLIT --phase dev --model_id $MODEL --batch_size $BS --run_tag v5dev_${SPLIT}_base_$TAG
```

```bash
python harness_v5.py --stage donor --split $SPLIT --phase dev --model_id $MODEL --batch_size $BS --run_tag v5dev_${SPLIT}_donor_$TAG
```

```bash
python transplant_v5.py --split $SPLIT --phase dev --model_id $MODEL --batch_size $BS \
  --base_file results_v5/v5dev_${SPLIT}_base_$TAG.jsonl \
  --donor_file results_v5/v5dev_${SPLIT}_donor_$TAG.jsonl \
  --run_tag v5dev_${SPLIT}_tp_$TAG
```

Notes:

- ChartQA uses `--dev_size 30` automatically. The harness refuses values of 100 or more.
- ChartQA loads 230 rows and drops `conflict_id` 45, leaving 229 (30 dev, 199 confirm). If the counts differ, the harness stops: the dataset is not the pinned release.
- Every stage resumes if it is interrupted: rerun the same command with the same `--run_tag`. A new tag is needed only after changing code, prompts or settings.
- To see the gate counts without decoding anything, add `--gates_only` to the transplant command. It writes `results_v5/<run_tag>.gates.json`.
- `--batch_size` applies to generation only. Margin scoring runs one request at a time; each request is two teacher-forced forward passes.

### ChartQA `max_pixels` (R8.4)

The default is `--max_pixels 200704` (256·28·28), the same as GSM8K/SVAMP. Charts carry small text. If the ChartQA `base_image` yield in block 3 is low, rerun **only the ChartQA blocks (3, 4 and 6)** under new tags with `--max_pixels 401408` (512·28·28). Keep whichever value the pre-registration records before the freeze. Do not change it afterwards.

## 5. What to bring back

Copy `results_v5/` to the local machine. For each block, record these into the pre-registration's deviation log, or into a dev-pass note beside it (R8.3):


| Quantity                                            | Where it comes from                                                                                                                                    |
| ----------------------------------------------------- | -------------------------------------------------------------------------------------------------------------------------------------------------------- |
| Competency yield                                    | `gates.json`: `competent` out of `items`                                                                                                               |
| Edit-gate pass rate                                 | `gates.json`: `passed` out of `competent`, plus `fail_reasons_by_order`                                                                                |
| ChartQA answer-only decodes matching *a_I* or *a_T* | `beh` rows, scored with `score_v5.behavioural_source`                                                                                                  |
| Dev wording floor                                   | `beh` rows, `para` vs `own`, per binding level: the signed mean (limit ±5.0 pp) and the churn rate (limit 5.0%). The gate fails if either is exceeded |
| Boundary mismatches                                 | Share of `dl` rows with `boundary_mismatch: true` (gate: ≤ 1%)                                                                                        |
| Whitespace token                                    | `ws_skipped` in `dl` rows: 2 means a separate space token was skipped for both candidates, 0 means the tokenizer has none                              |
| Manipulation check                                  | `free_binding` vs `donor` rows of the donor file: share of answers that follow the stated verdict                                                      |
| Seconds per item                                    | Sum of `wall_s` over an item's rows, from the transplant file                                                                                          |
| GPU, dtype, peak VRAM                               | Each manifest: `gpu`, `dtype` (must be `torch.bfloat16`), `peak_vram_gb`, `batch_size`                                                                 |
| Competency intersection                             | Item ids that pass competency for all three models, per regime (from the three `gates.json` files or base files)                                       |

Then run the analysis locally. It reports most of the quantities above, plus T1, ρ, TOST and every secondary analysis:

```bash
python analyze_v5.py --runs results_v5/v5dev_*_tp_*.jsonl --gates results_v5/v5dev_*_tp_*.gates.json \
  --base results_v5/v5dev_*_base_*.jsonl --donor results_v5/v5dev_*_donor_*.jsonl --output_dir results_v5/analysis_dev
```

On Windows PowerShell the `*` patterns are not expanded; list the files or run the command from Git Bash. The script refuses output from the fake `echo` model unless `--allow_dry_run` is given.

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
2. For each of the three models, on the same GPU class and with the batch size used in the dev pass: run the base stage with `--phase confirm` over the whole confirm pool.
3. Run the donor stage.
4. Run `transplant_v5.py --phase confirm --n_competent 250`. Record the tag hash in each manifest.
