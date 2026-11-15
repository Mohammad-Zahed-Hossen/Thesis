# Data

## What is included

The `artifacts/` directory contains the compact, anonymized values needed to
check the paper's tables and robustness analyses. It contains no source images,
generated images, credentials, server paths, or annotator identities.

## Image pairs

Counter-SNLI-VE and Counter-A-OKVQA are derived from
[SNLI-VE](https://huggingface.co/datasets/HuggingFaceM4/SNLI-VE)/Flickr30k
and [A-OKVQA](https://github.com/allenai/aokvqa)/COCO, respectively. Their
images are not stored in this Git repository because they remain subject to
the upstream datasets' licenses and terms.

The editing pipeline can rebuild pairs from locally obtained source data:

- SNLI-VE uses the `validation` split and Flickr30k images.
- A-OKVQA uses the `train` split, COCO 2017 training images, and the original
  four answer choices.

This repository therefore releases the construction code and compact analysis
artifacts, rather than redistributing the underlying images. Any separate
archive of generated pairs must preserve the upstream identifiers and licensing
information.

## Prepared-pair format

The easiest way to evaluate an existing set is a `generator.csv` whose image
paths resolve on the current machine. Required columns are:

| Column | Meaning |
|---|---|
| `image_a` | Original image path |
| `image_b` | Edited image path |
| `question` | Question or visual-entailment hypothesis |
| `labels` | Fixed answer choices, encoded as `<<json>>[...]` |
| `changed` | Description of the removed or modified object |
| `task` | `vqa` or `ve` |
| `error` | Whether the generation row failed a quality filter |

The pipeline also accepts `change_actual_mask`, `change_description_mask`,
`reason`, and `metadata`. See `generator.py` for the complete schema.

## Included analyses

The compact artifacts cover:

- the primary PE, CoT, and no-prefix comparisons;
- same-answer, source-image-clustered, directional-mention, relevance, and
  reconstruction controls;
- the blinded 60-pair human audit;
- the matched color-change experiment.

See [artifacts/README.md](artifacts/README.md) for individual files.
