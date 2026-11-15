# Counterfactual Tests for VLM Explanations

Official code and evaluation artifacts for **Counterfactual Tests for Measuring
Chain-of-Thought Faithfulness in Visual Language Models** (Findings of EMNLP 2026).

[Paper](https://arxiv.org/abs/2609.06704)

We remove objects from images, measure the resulting prediction shifts, and
test whether the explanations mention the removed objects.

Across eight VLMs and two datasets, Predict-then-Explain has higher vCCT than
pre-answer CoT in all 16 comparisons.

![PE has higher vCCT than CoT for all eight models on A-OKVQA and SNLI-VE. Error bars show 95% bootstrap confidence intervals.](assets/main_result.png)

## Reproduce the main results

```bash
python analysis/regenerate_camera_ready.py
```

Tables are written to `reproduced/`. Expected result: 16 positive PE–CoT
comparisons, with a mean vCCT gap of `0.1192`.

## Run the evaluation

Use Python 3.12 and CUDA-enabled PyTorch:

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt

python scripts/run_prepared.py \
  --generator-csv /path/to/generator.csv \
  --model qwen35 \
  --mode pe \
  --output-dir outputs/qwen35-pe
```

Modes: `pe` (answer, then explain), `cot` (step-by-step explanation, then answer),
and `ep` (explain first, without the step-by-step prefix).
See [model aliases and revisions](metadata/models.json) and
[environment requirements](REPRODUCIBILITY.md#environments).

## Generate counterfactual pairs

After setting up the source images and checkpoints described in
[REPRODUCIBILITY.md](REPRODUCIBILITY.md), run the A-OKVQA example:

```bash
python main.py configs/examples/aokvqa_generate.json
```

## Data and documentation

[DATA.md](DATA.md) describes the prepared-pair format and data availability.
This repository includes construction code, prompts, and compact result
artifacts; source and edited images are not included.

- [Result artifacts](artifacts/README.md)
- [Reproduction and setup instructions](REPRODUCIBILITY.md)
- [Citation](CITATION.cff)

## License

[MIT](LICENSE). Source datasets, model weights, and third-party components
retain their original licenses.
