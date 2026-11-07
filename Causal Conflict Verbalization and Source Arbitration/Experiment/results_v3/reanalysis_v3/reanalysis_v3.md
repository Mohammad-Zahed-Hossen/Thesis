# Re-analysis of the v3 outputs with score_v4

N = 1619; 1600 items have distinct answers and are used for answer-source rates.
score_v4 labels are heuristics until validated against human coding.

## Answer source (numeric exact match, distinct-answer items)

| Arm | Image | Text | Neither | Chance match | At token cap | Fallback extraction |
|---|---:|---:|---:|---:|---:|---:|
| arm1_direct | 1.6% | 5.1% | 93.2% | 1.9% | 98.1% | 99.3% |
| arm2_placebo | 35.7% | 4.2% | 60.1% | 1.3% | 37.6% | 72.9% |
| arm3_conflict | 11.8% | 36.1% | 52.2% | 1.3% | 44.2% | 83.7% |
| arm4_prefill_contradict | 1.3% | 15.8% | 82.9% | 1.1% | 0.7% | 0.0% |
| arm4_prefill_agree | 0.7% | 21.1% | 78.2% | 1.1% | 0.1% | 0.0% |

## Other labels (all items)

| Arm | Attempt image | Attempt text | Attempt unknown | Refusal | Tokens mean / median / p10 |
|---|---:|---:|---:|---:|---:|
| arm1_direct | 13.3% | 83.4% | 3.3% | 0 (0.0%) | 79.2 / 80 / 80 |
| arm2_placebo | 79.9% | 6.6% | 13.5% | 3 (0.2%) | 158.1 / 174 / 64 |
| arm3_conflict | 25.4% | 70.1% | 4.4% | 38 (2.3%) | 169.3 / 188 / 113 |

Arm 3 stated verdict: {'conflict': 886, 'no_info': 54, 'cannot_determine': 233, 'no_relation': 445, 'none': 1}
Arm 3 stated reliable source: {'absent': 890, 'text': 675, 'undetermined': 53, 'image': 1}
Arm 3 stated reliable source by answer: {'absent|image': 115, 'absent|neither': 503, 'absent|text': 265, 'image|neither': 1, 'text|image': 71, 'text|neither': 290, 'text|text': 302, 'undetermined|image': 2, 'undetermined|neither': 41, 'undetermined|text': 10}

## Paired contrasts on exact answer (distinct-answer items)

| Contrast : source | First only | Second only | Difference | 95% interval (problem-clustered) | Exact McNemar p |
|---|---:|---:|---:|---:|---:|
| arm2_vs_arm1:image | 558 | 13 | +34.1 pp | +30.0 to +38.5 | 2.54e-146 |
| arm2_vs_arm1:text | 58 | 73 | -0.9 pp | -3.4 to +1.5 | 0.2211 |
| arm3_vs_arm1:image | 184 | 22 | +10.1 pp | +7.3 to +13.2 | 4.93e-33 |
| arm3_vs_arm1:text | 525 | 30 | +30.9 pp | +26.6 to +35.3 | 6.51e-118 |
| arm3_vs_arm2:image | 77 | 460 | -23.9 pp | -28.2 to -19.9 | 1.93e-67 |
| arm3_vs_arm2:text | 535 | 25 | +31.9 pp | +27.5 to +36.3 | 1.05e-125 |

## Sensitivity

Finished in both Arms 2 and 3 (n = 624, conditioned on a post-treatment variable): Arm 2 image 52.6%, text 6.9%; Arm 3 image 18.9%, text 56.2%.

Problem solved in both roles, phi = 0.239.

| Arm | Token bin | n | Exact image | Exact text | Attempt image |
|---|---|---:|---:|---:|---:|
| arm2_placebo | 0-80 | 190 | 2.1% | 1.6% | 17.4% |
| arm2_placebo | 80-120 | 97 | 51.5% | 9.3% | 67.0% |
| arm2_placebo | 120-160 | 357 | 61.3% | 6.7% | 86.6% |
| arm2_placebo | 160-199 | 355 | 60.8% | 4.5% | 90.1% |
| arm2_placebo | 199-1000000 | 601 | 13.6% | 2.5% | 91.7% |
| arm3_conflict | 0-80 | 56 | 0.0% | 37.5% | 5.4% |
| arm3_conflict | 80-120 | 153 | 11.1% | 62.7% | 17.0% |
| arm3_conflict | 120-160 | 315 | 18.1% | 61.3% | 23.8% |
| arm3_conflict | 160-199 | 369 | 19.5% | 50.7% | 24.4% |
| arm3_conflict | 199-1000000 | 707 | 5.9% | 11.3% | 30.3% |

| Dataset | n | Arm | Exact image | Exact text |
|---|---:|---|---:|---:|
| gsm8k | 1304 | arm1_direct | 1.7% | 2.1% |
| gsm8k | 1304 | arm2_placebo | 35.1% | 2.8% |
| gsm8k | 1304 | arm3_conflict | 13.7% | 28.5% |
| gsm8k | 1304 | arm4_prefill_contradict | 1.4% | 8.7% |
| gsm8k | 1304 | arm4_prefill_agree | 0.8% | 14.2% |
| svamp | 296 | arm1_direct | 1.4% | 18.6% |
| svamp | 296 | arm2_placebo | 38.2% | 10.5% |
| svamp | 296 | arm3_conflict | 3.0% | 69.6% |
| svamp | 296 | arm4_prefill_contradict | 1.0% | 46.6% |
| svamp | 296 | arm4_prefill_agree | 0.0% | 51.7% |
