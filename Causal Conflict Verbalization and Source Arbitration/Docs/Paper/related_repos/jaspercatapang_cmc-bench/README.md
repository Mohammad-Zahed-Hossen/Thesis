# CMC-Bench

Code and data for the paper:

> **When Image and Text Disagree: Cross-Modal Evidence Conflict in Multimodal Retrieval-Augmented Generation**  
> Jasper Kyle Catapang  
> *2nd Workshop on Multimodal Augmented Generation via MultimodAl Retrieval (MAGMaR), ACL 2026.*  
> Workshop: <https://nlp.jhu.edu/magmar/>

**CMC-Bench** (Cross-Modal Conflict Benchmark) is a controlled benchmark for evaluating vision-language models when **retrieved image and text evidence disagree**, in a multimodal RAG-style setting.

The suite builds instances from **ChartQA** and **MMMU** (evaluation splits only), applies four evidence conditions per example, and supports local VLM inference via **mlx-vlm** on Apple Silicon (4-bit weights). Optional **LLM-as-judge** scoring uses an OpenAI-compatible API (e.g. Azure OpenAI); see `src/.env.example`.

## Requirements

- Python 3.10+
- Apple Silicon Mac if using the default **mlx-vlm** evaluation path
- Hugging Face access for dataset download
- For judge scoring: API credentials as in `src/.env.example`

## Setup

```bash
make install
cp src/.env.example src/.env   # edit with your judge API settings (judge only)
```

## Data and instances

One-time download of ChartQA + configured MMMU subsets into `data_cache/`:

```bash
make download
```

Build `outputs/cmc_bench_instances.jsonl` (paths and quotas in `src/configs/default.yaml`):

```bash
make data
```

## VLM evaluation

Runs all models listed in the config and writes predictions under `outputs/`:

```bash
make eval
```

`make all` runs `data` then `eval`.

## LLM judge and metrics

After you have `*_predictions_complete.jsonl` under `outputs/predictions/`, run the judge script (see module docstring for flags):

```bash
PYTHONPATH=src python src/scripts/run_llm_judge_metrics.py --help
```

To aggregate **behavioral** JSONL into a summary JSON without calling the API:

```bash
PYTHONPATH=src python src/scripts/aggregate_judge_metrics.py --help
```

## Layout

| Path | Role |
|------|------|
| `src/configs/default.yaml` | Paths, datasets, model IDs, scale |
| `src/data/` | Download helpers, schema, instance generation |
| `src/evaluation/` | Inference, metrics, judge client |
| `src/scripts/` | CLI entrypoints |

## Citation

```bibtex
@inproceedings{catapang2026cmcbench,
  title     = {When Image and Text Disagree: Cross-Modal Evidence Conflict in Multimodal Retrieval-Augmented Generation},
  author    = {Catapang, Jasper Kyle},
  booktitle = {Proceedings of the 2nd Workshop on Multimodal Augmented Generation via MultimodAl Retrieval (MAGMaR) at ACL 2026},
  year      = {2026},
  url       = {https://nlp.jhu.edu/magmar/}
}
```

## License

TBA.
