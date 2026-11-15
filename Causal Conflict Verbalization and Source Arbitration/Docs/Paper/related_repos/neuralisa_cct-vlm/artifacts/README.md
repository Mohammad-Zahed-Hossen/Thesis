# Result artifacts

These compact files let readers check the reported analyses without source
images or model weights.

## Main results

- `main/normalized_group_metrics.csv`: vCCT, vCT, uncertainty, shifts, and flip
  counts for PE, CoT, and the no-prefix ablation.
- `main/normalized_paired_inference.csv`: the 16 paired PE-CoT comparisons.
- `main/main_table_rows.tex`: values used in the main vCCT table.

## Robustness checks

- `controls/same_answer_subset_metrics.csv`: comparison restricted to examples
  where PE and CoT choose the same original-image answer.
- `controls/normalized_clustered_inference.csv`: inference clustered by source
  image.
- `controls/directional_cm.csv`: original- and edited-image mention rates and
  flip-conditioned results.
- `controls/paired_noop_normalized.json`: source-matched reconstruction control.
- `controls/linked_unlinked_normalized.csv`: exploratory relevance partition.

## Extensions and validation

- `color/`: matched color-change results.
- `audit/`: anonymized human-audit summaries and agreement statistics.
- `reproducibility/`: construction counts and per-model diagnostics.

Run `python analysis/regenerate_camera_ready.py` from the repository root to
validate these files and recreate the compact result tables.
