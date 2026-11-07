# Paired analysis of stored v3 labels

N = 1619. Labels are the stored v3 heuristics, not validated against human coding.
This compares two instructions; it does not isolate the effect of the verbalization.

## Arm summary

| Arm | Image label | Text label | Abstain label | Ambiguous | Exact image | Exact text | At token cap | Mean tokens |
|---|---:|---:|---:|---:|---:|---:|---:|---:|
| arm1_direct | 223 | 1385 | 0 | 11 | 26 (1.6%) | 83 (5.1%) | 1588 (98.1%) | 79.2 |
| arm2_placebo | 1449 | 145 | 4 | 21 | 577 (35.6%) | 76 (4.7%) | 608 (37.6%) | 158.1 |
| arm3_conflict | 417 | 954 | 221 | 27 | 190 (11.7%) | 579 (35.8%) | 716 (44.2%) | 169.3 |
| arm4_prefill_contradict | 0 | 0 | 0 | 0 | 25 (1.5%) | 256 (15.8%) | 12 (0.7%) | 3.0 |
| arm4_prefill_agree | 0 | 0 | 0 | 0 | 15 (0.9%) | 342 (21.1%) | 2 (0.1%) | 2.7 |

## Arm 2 vs Arm 3: image label

| | Arm 3 image | Arm 3 other |
|---|---:|---:|
| Arm 2 image | 392 | 1057 |
| Arm 2 other | 25 | 145 |

- Arm 2: 1449 (89.5%); Arm 3: 417 (25.8%)
- Difference, Arm 2 minus Arm 3: 63.7 pp (problem-clustered 95% interval 59.4 to 68.0)
- Exact McNemar p = 1.38e-275
- Paired odds ratio = 42.28 (95% interval 28.44 to 62.86)
- Cohen's h = 1.42

## Label migration, Arm 2 (rows) to Arm 3 (columns)

| | follows_image_problem | follows_text_problem | abstains | ambiguous |
|---|---:|---:|---:|---:|
| follows_image_problem | 392 | 832 | 201 | 24 |
| follows_text_problem | 20 | 103 | 20 | 2 |
| abstains | 1 | 3 | 0 | 0 |
| ambiguous | 4 | 16 | 0 | 1 |

## Arm 4 prefills

Arm 4a and 4b differ in rationale and named source together, so these contrasts can't separate the two.

- Identical answers: 948 (58.6%)
- Text match, 4b only vs 4a only: 105 vs 19 (exact McNemar p = 1.31e-15)
- Image match, 4a only vs 4b only: 16 vs 6 (exact McNemar p = 0.0525)
