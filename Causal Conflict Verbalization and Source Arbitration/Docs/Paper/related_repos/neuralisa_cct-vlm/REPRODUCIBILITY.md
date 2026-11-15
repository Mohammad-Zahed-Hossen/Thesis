# Reproducibility

## Environments

The release was validated on Linux with Python 3.12, CUDA 12.8, and an NVIDIA
H100 80 GB GPU. Exact model and component revisions are recorded in
`metadata/`.

Different model families require different Transformers versions:

| Model family | Requirements file | Transformers |
|---|---|---:|
| Qwen, InternVL, R-4B | `requirements.txt` | 5.3.0 |
| Ovis2.5 | `requirements-ovis.txt` | 4.51.3 |
| Kimi-VL | `requirements-kimi.txt` | 4.48.2 |

Create a separate virtual environment for each incompatible family. For the
primary environment:

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

## Pipeline

Each run has four stages:

1. Generate or load `data/generator.csv`.
2. Run PE or CoT inference and write `data/model.csv`.
3. Judge change mentions and write `data/evaluator.csv`.
4. Compute vCCT/vCT and, unless disabled, render examples.

Runs are resumable. When `override=false`, an existing stage CSV is loaded and
the pipeline continues from the next stage.

For prepared image pairs, use `scripts/run_prepared.py` as shown in the main
README. The runnable `configs/examples/aokvqa_generate.json` configuration
shows the image-generation settings.

## Paths used by image generation

Paths can be supplied directly in the configuration or through:

```bash
export CCT_DATA_DIR=/path/to/datasets
export CCT_CACHE_DIR=/path/to/cache
export CCT_SAM_CHECKPOINT=/path/to/sam_vit_h_4b8939.pth
export CCT_QWEN_IMAGE_EDIT_MODEL=Qwen/Qwen-Image-Edit
```

The SAM ViT-H checkpoint is available from the
[official Segment Anything repository](https://github.com/facebookresearch/segment-anything#model-checkpoints).
Its expected SHA-256 hash is recorded in `metadata/components.json`.

The expected A-OKVQA layout is:

```text
$CCT_DATA_DIR/
├── AOKVQA/aokvqa_v1p0_train.json
└── COCO2017/train2017/000000000000.jpg
```

For SNLI-VE, `$CCT_DATA_DIR/Flickr30k` is passed to the Hugging Face SNLI-VE
loader.

## Validation

Check the compact artifacts without model dependencies:

```bash
python analysis/regenerate_camera_ready.py
```

After installing the primary environment, test the pipeline with mock data:

```bash
python smoke_test.py --output-dir /tmp/cct-smoke
```

For a real one-example editor/localizer check:

```bash
python scripts/integration_smoke.py \
  --data-dir /path/to/aokvqa-layout \
  --sam-checkpoint /path/to/sam_vit_h_4b8939.pth \
  --output-dir /tmp/cct-integration
```

The last full validation is summarized in `metadata/validation.md`.
