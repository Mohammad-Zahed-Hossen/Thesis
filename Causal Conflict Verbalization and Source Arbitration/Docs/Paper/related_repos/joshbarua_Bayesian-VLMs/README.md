# Bayesian Cue Combination Explains Modality Preferences in Vision-Language Models

[![Dataset](https://img.shields.io/badge/🤗%20Dataset-conflicting__modality-yellow)](https://huggingface.co/datasets/joshbarua/conflicting_modality)
[![Paper](https://img.shields.io/badge/Paper-coming%20soon-red)]()

## Authors
- [Josh Barua](https://joshbarua.github.io/)
- [William Rudman](https://wrudman.github.io/)
- [Kyle Mahowald](https://mahowak.github.io/)

*The University of Texas at Austin*

## Project Overview

When a vision-language model (VLM) is given a text passage and an image that
support **different** answers to the same question, which one does it follow?
This repository accompanies our paper, which shows that VLM modality
preferences are well explained by a **Bayesian cue-combination** model: the
model integrates evidence independently across modalities and weights each
source by its reliability.

We test this at two levels of analysis:

- **Behavioral (computational level).** We score each VLM's preference between
  the text-supported answer `a_T` and the vision-supported answer `a_V` while
  independently degrading textual reliability (token noise `p`) and visual
  reliability (Gaussian blur `σ`) over a 6×6 grid. A two-weight linear
  cue-combination model in log-odds space,

  ```
  s_J = β_T · (s_T − π₀) + β_V · (s_V − π₀) + π₀,
  ```

  predicts per-example joint preferences `s_J` from the unimodal probes
  (`s_T`, `s_V`) and a prior probe (`π₀`), including on held-out
  out-of-distribution degradation conditions.

- **Mechanistic (algorithmic level).** At the first divergent answer token, we
  measure how full-softmax attention is allocated between image and passage
  spans as their reliabilities change. We then use attention knockout to block
  the image, passage, or question route to that readout. For Qwen3.5's hybrid
  stack, we additionally zero the linear-attention write at the readout.

  The reported intervention is `Δ_KO = s_KO - s`, in nats of log-odds;
  positive values move toward the text-supported answer and negative values
  toward the vision-supported answer.

**Models studied behaviorally:** Qwen2.5-VL, Qwen3.5-4B, Gemma3, and
GLM-4.6V-Flash, chosen
to span different vision encoders, LLM attention patterns, and vision–language
fusion strategies. The attention experiments reported in the paper use
Qwen2.5-VL-3B and Qwen3.5-4B only; their adapters live under
`attention/adapters/`. The behavioral and MCQ pipelines remain
adapter-independent.

**Repository Structure:**
```
Bayesian-VLMs/
├── config.py                       # paths, grid preset (6×6), per-model prior settings
├── data/                           # dataset construction (optional; needs Gemini API key)
│   ├── build_dataset.py            #   DocVQA / VQAv2 conflicting tuples
│   ├── build_realworldqa.py        #   RealworldQA conflicting tuples
│   └── build_normalized_dataset.py #   pixel-count normalization across domains
├── scoring/                        # VLM probing core
│   ├── vlm_scorer.py               #   teacher-forced log-likelihood scorer
│   ├── degradation.py              #   blur + token-noise grid helpers
│   └── hooks.py                    #   residual-stream hook abstractions
├── fitting/                        # cue-combination predictors (fit interface)
│   ├── models.py                   #   naive-Bayes / linear / bilinear nn.Modules
│   ├── ols.py  train.py  fit.py    #   OLS variant + training loop + fit driver
│   └── support.py                  #   ID / OOD degradation-cell masks
├── utils/splits.py                 # stratified train/val/test splits by example ID
├── transitions/                    # BEHAVIORAL pipeline
│   ├── generate_text_degradations.py  # token-noise text variants
│   ├── run_degradation_scoring.py     # score probes over the (σ, p) grid (GPU)
│   ├── fit_degraded.py                # fit predictors under ID & OOD → metrics/params JSON
│   └── build_results_table.py         # predictor-comparison table (paper §4–5)
├── attention/                      # ATTENTION ALLOCATION + KNOCKOUT
│   ├── run_allocation.py           #   readout attention over the 6×6 grid (GPU)
│   ├── run_knockout.py             #   image/passage/question route knockout (GPU)
│   ├── run_linear_output_knockout.py # Qwen3.5 linear-attention ablation (GPU)
│   ├── summarize.py                #   bootstrap knockout confidence intervals
│   ├── plot_allocation.py          #   paper allocation heatmaps
│   ├── make_table.py               #   paper knockout CSV + LaTeX table
│   └── adapters/                   #   Qwen2.5-VL and Qwen3.5 adapters
├── mcq/                            # open-ended generation validation (appendix)
│   ├── generate.py                 #   two-alternative forced-choice generation (GPU)
│   └── analysis.py                 #   agreement of generated choice with sign(s_J)
└── requirements.txt
```

## Installation

### Prerequisites
- Python 3.10+
- CUDA-capable GPU(s) for scoring and attention sweeps (analysis is CPU-only)

### Setup

1. **Clone the repository:**
```bash
git clone https://github.com/joshbarua/Bayesian-VLMs.git
cd Bayesian-VLMs
```

2. **Create an environment and install dependencies:**
```bash
conda create -n bayesian-vlms python=3.10 -y
conda activate bayesian-vlms
pip install -r requirements.txt
```

3. **(Optional) Set the Hugging Face cache location** so models and datasets
   download to a directory with enough space:
```bash
export HF_HOME=/path/to/hf_cache
export HF_CACHE_DIR=$HF_HOME/hub
```

4. **(Optional) Gemini API key** — only needed if you regenerate the dataset
   from scratch with `data/build_*.py`. Create a `.env` file in the repo root:
```bash
echo "GEMINI_API_KEY=your_api_key_here" > .env
```

## Dataset

The unified conflicting-VQA dataset (2,765 examples pooled from **DocVQA**,
**VQAv2**, and **RealworldQA**) is hosted on Hugging Face and is downloaded
automatically by the scoring scripts:

- 🤗 [`joshbarua/conflicting_modality`](https://huggingface.co/datasets/joshbarua/conflicting_modality)

Each example is a tuple `(q, t, v, a_T, a_V)`: a question `q`, a text passage
`t` supporting answer `a_T`, and an image `v` supporting a different answer
`a_V` (`a_T ≠ a_V`).

To reproduce the **pixel-normalized** dataset used in the paper (which equalizes
the ~15× pixel-count gap between document scans and natural photos), pass a
local `--dataset_path` pointing at the output of `data/build_normalized_dataset.py`.
Reconstructing the dataset from the source benchmarks (optional) requires a
Gemini API key and runs:

```bash
python data/build_dataset.py             # DocVQA + VQAv2 conflicting tuples
python data/build_realworldqa.py         # RealworldQA conflicting tuples
python data/build_normalized_dataset.py  # pixel-count normalization
```

> **Note.** All scripts below read `config.py`, which uses module-relative
> imports, so run them from the repository root (e.g. `python transitions/...`).
> Outputs are written under `runs/<run_id>/`.

## Pipeline 1 — Behavioral (Bayesian cue combination)

Reproduces the predictor-comparison tables and preference surfaces (paper §4–5).

```bash
# (a) Generate token-noise text degradations for the 6×6 grid
python transitions/generate_text_degradations.py --grid 6x6

# (b) Score text / vision / joint / prior probes over the (σ, p) grid (GPU)
python transitions/run_degradation_scoring.py \
  --run_id deg_qwen25vl \
  --model_name Qwen/Qwen2.5-VL-3B-Instruct \
  --grid 6x6 \
  --splits train val test

# (c) Fit all predictors under the ID and OOD protocols (CPU)
python transitions/fit_degraded.py --run_id deg_qwen25vl

# (d) Predictor-comparison table: long-format CSV + a wide pivot to stdout (CPU)
python transitions/build_results_table.py --run_id deg_qwen25vl
```

Step (c) writes the data structures that back every behavioral table:
- `runs/deg_qwen25vl/degraded_metrics.json` — KL and R² per predictor, per
  protocol (`id` / `ood`), per experiment
- `runs/deg_qwen25vl/id_params.json`, `ood_params.json` — fitted `β_T`, `β_V`
  (and bilinear `β_I`)

Step (d) turns those metrics into the paper's predictor-comparison table:
- `runs/deg_qwen25vl/paper_results_table.csv` — one row per
  (dataset, protocol, predictor) with KL and R²

The paper's main-text table averages the three within-dataset experiments at
`protocol == ood`; the appendix reports the per-dataset breakdown. Run step (d)
once per model — it takes a single `--run_id`.

**Predictors compared:** Best Single Probe, Calibrated Naive Bayes, Linear Cue
Combination, Bilinear Cue Combination, and an Unconstrained Linear baseline.

**Protocols:**
- **ID** — train/val/test on the full 6×6 grid (split by example ID).
- **OOD** — train/val on the singly-degraded "L-shape" `{(σ,0)} ∪ {(0,p)}`,
  test on the held-out interior `{(σ,p) : σ>0, p>0}`.

## Pipeline 2 — Attention allocation and knockout

This reproduces the attention-allocation figure and attention-knockout table.
It reuses `splits.json`, `degradation_meta.json`, and the token-noise variants
from Pipeline 1. Use the same pixel-normalized dataset for both pipelines.

The paper uses the held-out `test` split with `--n_examples 416`; after the
fixed split and answer-pair validity checks this is exactly the 413 examples
reported in the captions. All attention measurements use fp32.

```bash
DATA=/path/to/dataset_pixnorm

# Qwen2.5-VL-3B: allocation surface and whole-stack span knockout
python attention/run_allocation.py \
  --run_id attn_qwen25 --deg_run_id deg_qwen25vl \
  --model_name Qwen/Qwen2.5-VL-3B-Instruct \
  --dataset_path "$DATA" --split test --n_examples 416 --dtype float32
python attention/run_knockout.py \
  --run_id attn_qwen25 --deg_run_id deg_qwen25vl \
  --model_name Qwen/Qwen2.5-VL-3B-Instruct \
  --dataset_path "$DATA" --split test --n_examples 416 --dtype float32

# Qwen3.5-4B: eight full-attention layers plus 24 linear-attention layers
python attention/run_allocation.py \
  --run_id attn_qwen35 --deg_run_id deg_qwen35 \
  --model_name Qwen/Qwen3.5-4B \
  --dataset_path "$DATA" --split test --n_examples 416 --dtype float32
python attention/run_knockout.py \
  --run_id attn_qwen35 --deg_run_id deg_qwen35 \
  --model_name Qwen/Qwen3.5-4B \
  --dataset_path "$DATA" --split test --n_examples 416 --dtype float32
python attention/run_linear_output_knockout.py \
  --run_id attn_qwen35 --deg_run_id deg_qwen35 \
  --model_name Qwen/Qwen3.5-4B \
  --dataset_path "$DATA" --split test --n_examples 416 --dtype float32

# Bootstrap summaries, paper figure, and paper table (CPU)
python attention/summarize.py --run_id attn_qwen25
python attention/summarize.py --run_id attn_qwen35
python attention/plot_allocation.py \
  --run 'Qwen2.5-VL-3B=attn_qwen25' \
  --run 'Qwen3.5-4B=attn_qwen35' \
  --out runs/attention_allocation.png
python attention/make_table.py \
  --qwen25_run_id attn_qwen25 --qwen35_run_id attn_qwen35 \
  --out runs/attention_knockout.tex
```

The knockout defaults target the whole stack, exactly as in the paper.
Optional diagnostic subranges can be supplied with `--blocks`.
`summarize.py` checks two no-op controls before
reporting results: an empty span knockout and a scale-one linear-attention
hook. Outputs are:

- `allocation.parquet`: per-example, per-cell, per-full-attention-layer masses;
- `knockout.parquet`: span knockouts for clean (`C`), text-degraded (`T`), and
  vision-degraded (`V`) conditions;
- `linear_output_knockout.parquet`: Qwen3.5 readout-write ablations;
- `summary_*.csv`: means and 95% bootstrap confidence intervals;
- `attention_allocation.{png,pdf}` and `attention_knockout.{csv,tex}`.

For multi-GPU runs, pass `--shard_id i --num_shards N` to each GPU process.
The analysis scripts read shard parquets directly, so no manual merge is
required.

## Pipeline 3 — Open-ended generation validation (appendix)

Checks that `sign(s_J)` agrees with the answer the model actually generates
under free-form reasoning.

```bash
# (a) Two-alternative forced-choice generation, both label assignments (GPU)
python mcq/generate.py \
  --run_id mcq_qwen25vl \
  --model_name Qwen/Qwen2.5-VL-3B-Instruct \
  --dataset_path /path/to/dataset_pixnorm \
  --grid 6x6 --n_per_dataset 100

# (b) Agreement analysis vs. sign(s_J)
python mcq/analysis.py \
  --runs "Qwen2.5-VL-3B=runs/mcq_qwen25vl=runs/deg_qwen25vl/degradation_scores.parquet" \
  --out_dir runs/mcq_qwen25vl/analysis
```

## Notes on reproducibility

- **GPU vs CPU.** Degradation scoring, the three `attention/run_*` sweeps, and
  `mcq/generate` need a GPU. Fitting, summaries, plots, and tables are CPU-only.
- **Sharding (recommended for the full dataset).** Scoring is ~100 s/example,
  so the full 2,765-example grid is best split across GPUs. The commands above
  run a single process and write the unsharded output directly. To shard, pass
  `--shard_id i --num_shards N` (one process per GPU); each shard writes
  `*_shard_<i>.parquet`, which you then concatenate into the unsuffixed parquet
  that the fitting steps read:
  ```bash
  RUN=deg_qwen25vl; N=8
  for i in $(seq 0 $((N-1))); do
    CUDA_VISIBLE_DEVICES=$i python transitions/run_degradation_scoring.py \
      --run_id $RUN --model_name Qwen/Qwen2.5-VL-3B-Instruct --grid 6x6 \
      --splits train val test --shard_id $i --num_shards $N &
  done; wait
  python -c "import pandas as pd, glob; d='runs/'+'$RUN'+'/'; \
    pd.concat([pd.read_parquet(f) for f in sorted(glob.glob(d+'degradation_scores_shard_*.parquet'))], \
    ignore_index=True).sort_values('id').to_parquet(d+'degradation_scores.parquet', index=False)"
  ```
  Attention sweeps also accept these sharding flags, checkpoint every five
  examples, resume interrupted shards, and can be summarized without a manual
  merge.
- **Gemma3 prior probe.** For Gemma3, `config.py` sets `π₀ = 0` at fit time
  (question-only contexts trigger refusals/hedging that destabilize the prior
  probe); the linear model reduces to `s_J = β_T·s_T + β_V·s_V`.

## Citation

If you find this work useful, please cite our paper:

```bibtex
@misc{barua2026bayesian,
  title  = {Bayesian Cue Combination Explains Modality Preferences in Vision-Language Models},
  author = {Josh Barua and William Rudman and Kyle Mahowald},
  year   = {2026}
}
```
