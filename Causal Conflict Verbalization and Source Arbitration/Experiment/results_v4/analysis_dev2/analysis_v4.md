# v4 analysis

Attempt, refusal and verdict labels are heuristics until validated by `sample_for_coding.py evaluate`.

## Gate failures

- Qwen/Qwen2.5-VL-3B-Instruct | conflict | dev | repetition_penalty=1.0 | paraphrase=0 | base_image: token cap 5.5% (limit <5%)
- Qwen/Qwen2.5-VL-3B-Instruct | conflict | dev | repetition_penalty=1.0 | paraphrase=0 | base_text: token cap 13.0% (limit <5%)
- Qwen/Qwen2.5-VL-3B-Instruct | conflict | dev | repetition_penalty=1.0 | paraphrase=0 | conflict_full: token cap 5.0% (limit <5%)
- Qwen/Qwen2.5-VL-3B-Instruct | conflict | dev | repetition_penalty=1.0 | paraphrase=0 | congruent_direct: token cap 6.5% (limit <5%)
- Qwen/Qwen2.5-VL-3B-Instruct | conflict | dev | repetition_penalty=1.0 | paraphrase=0 | desc_image_first: answer or refusal 65.5% (limit >=90%)
- Qwen/Qwen2.5-VL-3B-Instruct | conflict | dev | repetition_penalty=1.0 | paraphrase=0 | detect_only: token cap 6.5% (limit <5%)
- Qwen/Qwen2.5-VL-3B-Instruct | conflict | dev | repetition_penalty=1.0 | paraphrase=0 | direct: token cap 8.0% (limit <5%)
- Qwen/Qwen2.5-VL-3B-Instruct | conflict | dev | repetition_penalty=1.0 | paraphrase=0 | direct_v3: token cap 8.5% (limit <5%)
- Qwen/Qwen2.5-VL-3B-Instruct | conflict | dev | repetition_penalty=1.0 | paraphrase=0 | placebo_v3: answer or refusal 81.0% (limit >=90%)
- Qwen/Qwen2.5-VL-3B-Instruct | conflict | dev | repetition_penalty=1.0 | paraphrase=0 | z1_filler: token cap 6.5% (limit <5%)
- Qwen/Qwen2.5-VL-3B-Instruct | conflict | dev | repetition_penalty=1.0 | paraphrase=0 | z1_m0: token cap 6.5% (limit <5%)

## Repetition penalty, same arm and items

| Arm | Measure | n | Low penalty | High penalty | High only / low only | Exact McNemar p |
|---|---|---:|---:|---:|---:|---:|
| direct_v3 | exact image | 200 | 4.5% (1.0) | 8.0% (1.05) | 9 / 2 | 0.0654 |
| direct_v3 | exact text | 200 | 68.0% (1.0) | 62.0% (1.05) | 15 / 27 | 0.0884 |
| direct_v3 | attempt image | 200 | 5.0% (1.0) | 12.5% (1.05) | 17 / 2 | 7.29e-4 |
| direct_v3 | attempt text | 200 | 89.5% (1.0) | 85.5% (1.05) | 5 / 13 | 0.0963 |
| direct_v3 | stops without solving | 200 | 2.5% (1.0) | 1.5% (1.05) | 1 / 3 | 0.6250 |
| direct_v3 | v3 abstention label | 200 | 0.0% (1.0) | 0.0% (1.05) | 0 / 0 | 1 |
| placebo_v3 | exact image | 200 | 14.5% (1.0) | 52.0% (1.05) | 81 / 6 | 7.03e-18 |
| placebo_v3 | exact text | 200 | 2.5% (1.0) | 3.5% (1.05) | 7 / 5 | 0.7744 |
| placebo_v3 | attempt image | 200 | 52.5% (1.0) | 82.5% (1.05) | 69 / 9 | 1.38e-12 |
| placebo_v3 | attempt text | 200 | 6.5% (1.0) | 7.0% (1.05) | 10 / 9 | 1 |
| placebo_v3 | stops without solving | 200 | 35.0% (1.0) | 7.5% (1.05) | 8 / 63 | 1.03e-11 |
| placebo_v3 | v3 abstention label | 200 | 0.0% (1.0) | 0.5% (1.05) | 1 / 0 | 1 |
| conflict_v3 | exact image | 200 | 4.5% (1.0) | 18.0% (1.05) | 34 / 7 | 2.53e-5 |
| conflict_v3 | exact text | 200 | 41.5% (1.0) | 48.5% (1.05) | 39 / 25 | 0.1034 |
| conflict_v3 | attempt image | 200 | 7.0% (1.0) | 24.0% (1.05) | 43 / 9 | 2.04e-6 |
| conflict_v3 | attempt text | 200 | 67.5% (1.0) | 71.5% (1.05) | 46 / 38 | 0.4452 |
| conflict_v3 | stops without solving | 200 | 0.0% (1.0) | 0.0% (1.05) | 0 / 0 | 1 |
| conflict_v3 | v3 abstention label | 200 | 0.5% (1.0) | 12.5% (1.05) | 25 / 1 | 8.05e-7 |

## Qwen/Qwen2.5-VL-3B-Instruct | conflict | dev | repetition_penalty=1.0 | paraphrase=0

### Arms

| Arm | n | Exact image | Exact text | Same gold | Neither | Attempt image | Attempt text | Refusal | v3 abstain label | Token cap | Stops unsolved | Answer only | Fallback answer | Mean tokens |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| base_image | 200 | 0.0% | 0.0% | 72.5% | 27.5% | 99.5% | 0.0% | 0.0% | 0.0% | 5.5% | 0.0% | 0.0% | 35.0% | 237.1 |
| base_text | 200 | 0.0% | 0.0% | 75.5% | 24.5% | 0.0% | 99.0% | 0.0% | 0.0% | 13.0% | 0.0% | 0.0% | 23.0% | 254.4 |
| conflict_full | 200 | 19.5% | 59.0% | 0.0% | 21.5% | 26.0% | 70.5% | 0.0% | 0.0% | 5.0% | 0.0% | 0.0% | 30.0% | 227.7 |
| conflict_v3 | 200 | 4.5% | 41.5% | 0.0% | 54.0% | 7.0% | 67.5% | 0.0% | 0.5% | 0.5% | 0.0% | 0.0% | 96.0% | 121.2 |
| congruent_conflict | 200 | 0.0% | 0.0% | 77.0% | 23.0% | 89.5% | 0.0% | 0.0% | 0.5% | 1.0% | 0.0% | 0.0% | 20.0% | 185.3 |
| congruent_detect | 200 | 0.0% | 0.0% | 77.5% | 22.5% | 91.5% | 0.0% | 0.0% | 0.5% | 0.5% | 4.0% | 0.0% | 13.5% | 155.6 |
| congruent_direct | 200 | 0.0% | 0.0% | 77.5% | 22.5% | 94.0% | 0.0% | 0.0% | 0.0% | 6.5% | 1.0% | 0.0% | 31.0% | 219.1 |
| desc_image_first | 200 | 24.0% | 3.5% | 0.0% | 72.5% | 37.0% | 13.0% | 0.5% | 0.0% | 2.0% | 46.5% | 0.0% | 42.0% | 120.9 |
| desc_text_first | 200 | 38.0% | 33.5% | 0.0% | 28.5% | 46.5% | 41.0% | 0.0% | 0.0% | 3.0% | 5.0% | 0.0% | 24.5% | 210.2 |
| detect_only | 200 | 22.0% | 44.5% | 0.0% | 33.5% | 31.0% | 58.5% | 0.0% | 0.5% | 6.5% | 0.5% | 0.0% | 23.5% | 206.5 |
| direct | 200 | 8.0% | 63.0% | 0.0% | 29.0% | 14.0% | 81.0% | 0.0% | 0.0% | 8.0% | 0.5% | 0.0% | 55.5% | 235.8 |
| direct_v3 | 200 | 4.5% | 68.0% | 0.0% | 27.5% | 5.0% | 89.5% | 0.0% | 0.0% | 8.5% | 2.5% | 1.0% | 89.5% | 231.7 |
| filler | 200 | 4.0% | 75.0% | 0.0% | 21.0% | 4.5% | 88.5% | 0.0% | 0.0% | 2.0% | 2.0% | 0.0% | 9.0% | 188.8 |
| placebo_v3 | 200 | 14.5% | 2.5% | 0.0% | 83.0% | 52.5% | 6.5% | 0.0% | 0.0% | 1.0% | 35.0% | 0.0% | 78.5% | 90.5 |
| reliability_only | 200 | 31.5% | 44.5% | 0.0% | 24.0% | 37.0% | 57.0% | 0.0% | 0.0% | 2.5% | 3.0% | 0.0% | 13.5% | 197.7 |
| z0_eq_a | 200 | 61.0% | 10.5% | 0.0% | 28.5% | 83.5% | 11.0% | 0.5% | 0.5% | 3.5% | 0.0% | 0.0% | 43.5% | 219.7 |
| z0_eq_b | 200 | 52.5% | 15.5% | 0.0% | 32.0% | 79.0% | 11.5% | 0.0% | 0.0% | 2.0% | 0.0% | 0.0% | 45.0% | 218.4 |
| z0_filler | 200 | 13.0% | 29.5% | 0.0% | 57.5% | 20.5% | 40.5% | 0.0% | 0.0% | 3.5% | 0.0% | 29.5% | 27.0% | 84.9 |
| z0_m0 | 200 | 47.5% | 12.0% | 0.0% | 40.5% | 73.5% | 20.0% | 0.0% | 0.5% | 2.0% | 0.0% | 2.0% | 39.5% | 154.6 |
| z0_m1 | 200 | 26.0% | 47.5% | 0.0% | 26.5% | 36.5% | 59.5% | 0.0% | 0.0% | 2.0% | 0.0% | 0.0% | 39.5% | 182.2 |
| z0_rel_image | 200 | 68.0% | 5.0% | 0.0% | 27.0% | 91.5% | 7.5% | 0.0% | 0.0% | 3.0% | 0.0% | 0.0% | 35.5% | 213.4 |
| z0_rel_text | 200 | 47.0% | 25.0% | 0.0% | 28.0% | 66.0% | 32.0% | 0.0% | 0.0% | 2.5% | 0.0% | 0.0% | 38.5% | 193.3 |
| z1_eq_a | 200 | 16.0% | 60.5% | 0.0% | 23.5% | 18.0% | 70.0% | 0.0% | 2.5% | 1.5% | 0.0% | 0.0% | 35.5% | 197.2 |
| z1_eq_b | 200 | 17.0% | 58.0% | 0.0% | 25.0% | 19.5% | 69.5% | 0.0% | 4.0% | 3.0% | 0.0% | 0.0% | 27.5% | 198.4 |
| z1_filler | 200 | 18.5% | 31.0% | 0.0% | 50.5% | 29.0% | 43.0% | 0.0% | 0.0% | 6.5% | 0.0% | 24.5% | 31.5% | 118.3 |
| z1_m0 | 200 | 35.0% | 30.5% | 0.0% | 34.5% | 40.5% | 49.5% | 0.5% | 2.0% | 6.5% | 0.0% | 0.0% | 35.0% | 234.2 |
| z1_m1 | 200 | 19.5% | 60.0% | 0.0% | 20.5% | 25.5% | 70.5% | 0.0% | 0.0% | 3.0% | 0.0% | 0.5% | 28.5% | 180.7 |
| z1_rel_image | 200 | 27.5% | 53.0% | 0.0% | 19.5% | 35.0% | 64.0% | 0.0% | 0.0% | 3.0% | 0.0% | 0.0% | 26.0% | 188.3 |
| z1_rel_text | 200 | 27.0% | 53.0% | 0.0% | 20.0% | 34.5% | 65.0% | 0.0% | 0.0% | 2.5% | 0.0% | 0.0% | 27.0% | 183.6 |

In single-source and congruent arms both gold answers are the same, so a correct answer appears under Same gold.

### Solvability: same problem from image alone and text alone

Image 72.8%, text 75.4% of 195 problems. Solved only from image / only from text: 16 / 21; exact McNemar p = 0.5114.

### Congruent arms: stated verdict (a conflict verdict here is a false alarm)

- congruent_conflict: {'agree': 192, 'conflict': 8}
- congruent_detect: {'agree': 195, 'conflict': 5}
- congruent_direct: {'none': 200}

### Fidelity: own verbalization prefilled, same answer as donor

- z0_m0 vs desc_image_first: 95.3% of 107 (93 donors without solving excluded)
- z1_m1 vs conflict_full: 96.5% of 200 (0 donors without solving excluded)

### Wording control: answer changed between same-meaning prefills

- z0_eq_a vs z0_eq_b: 39.0% of 200
- z1_eq_a vs z1_eq_b: 33.0% of 200

### Transplant, primary (exact answer)

| First vs second | Outcome | n | First | Second | Difference | 95% interval | First only / second only | Holm p |
|---|---|---:|---:|---:|---:|---:|---:|---:|
| z0_m1 vs z0_m0 | answer:image | 200 | 26.0% | 47.5% | -21.5 pp | -35.1 to -8.6 | 15 / 58 | 4.09e-6 |
| z0_m1 vs z0_m0 | answer:text | 200 | 47.5% | 12.0% | +35.5 pp | +23.7 to +48.5 | 73 / 2 | 2.41e-18 |
| z1_m1 vs z1_m0 | answer:image | 200 | 19.5% | 35.0% | -15.5 pp | -28.5 to -3.5 | 13 / 44 | 4.24e-4 |
| z1_m1 vs z1_m0 | answer:text | 200 | 60.0% | 30.5% | +29.5 pp | +17.9 to +41.6 | 63 / 4 | 1.66e-13 |
| z1_m0 vs z0_m0 | answer:image | 200 | 35.0% | 47.5% | -12.5 pp | -25.7 to +0.0 | 19 / 44 | 0.0111 |
| z1_m0 vs z0_m0 | answer:text | 200 | 30.5% | 12.0% | +18.5 pp | +8.0 to +29.9 | 44 / 7 | 1.45e-6 |
| z1_m1 vs z0_m1 | answer:image | 200 | 19.5% | 26.0% | -6.5 pp | -15.7 to +2.1 | 8 / 21 | 0.0965 |
| z1_m1 vs z0_m1 | answer:text | 200 | 60.0% | 47.5% | +12.5 pp | +1.5 to +23.5 | 34 / 9 | 0.0012 |
| z0_rel_image vs z0_rel_text | answer:image | 200 | 68.0% | 47.0% | +21.0 pp | +8.5 to +34.2 | 54 / 12 | 1.86e-6 |
| z0_rel_image vs z0_rel_text | answer:text | 200 | 5.0% | 25.0% | -20.0 pp | -30.9 to -10.0 | 5 / 45 | 5.47e-8 |
| z1_rel_image vs z1_rel_text | answer:image | 200 | 27.5% | 27.0% | +0.5 pp | -5.2 to +6.6 | 6 / 5 | 1 |
| z1_rel_image vs z1_rel_text | answer:text | 200 | 53.0% | 53.0% | +0.0 pp | -6.5 to +6.3 | 6 / 6 | 1 |
| z0_m1 vs z0_filler | answer:image | 200 | 26.0% | 13.0% | +13.0 pp | +1.4 to +25.1 | 39 / 13 | 0.0025 |
| z0_m1 vs z0_filler | answer:text | 200 | 47.5% | 29.5% | +18.0 pp | +3.1 to +32.3 | 58 / 22 | 5.61e-4 |
| z1_m1 vs z1_filler | answer:image | 200 | 19.5% | 18.5% | +1.0 pp | -9.7 to +12.4 | 24 / 22 | 1 |
| z1_m1 vs z1_filler | answer:text | 200 | 60.0% | 31.0% | +29.0 pp | +14.5 to +42.8 | 70 / 12 | 5.75e-10 |

### Transplant, secondary (attempt label)

| First vs second | Outcome | n | First | Second | Difference | 95% interval | First only / second only | Holm p |
|---|---|---:|---:|---:|---:|---:|---:|---:|
| z0_m1 vs z0_m0 | attempt:image | 200 | 36.5% | 73.5% | -37.0 pp | -50.3 to -23.9 | 7 / 81 | 6.72e-16 |
| z0_m1 vs z0_m0 | attempt:text | 200 | 59.5% | 20.0% | +39.5 pp | +27.2 to +52.8 | 85 / 6 | 9.25e-18 |
| z1_m1 vs z1_m0 | attempt:image | 200 | 25.5% | 40.5% | -15.0 pp | -28.6 to -1.1 | 20 / 50 | 0.0018 |
| z1_m1 vs z1_m0 | attempt:text | 200 | 70.5% | 49.5% | +21.0 pp | +8.0 to +33.8 | 56 / 14 | 3.87e-6 |
| z1_m0 vs z0_m0 | attempt:image | 200 | 40.5% | 73.5% | -33.0 pp | -45.6 to -18.8 | 14 / 80 | 2.97e-11 |
| z1_m0 vs z0_m0 | attempt:text | 200 | 49.5% | 20.0% | +29.5 pp | +17.1 to +41.5 | 68 / 9 | 3.18e-11 |
| z1_m1 vs z0_m1 | attempt:image | 200 | 25.5% | 36.5% | -11.0 pp | -19.5 to -3.2 | 2 / 24 | 8.39e-5 |
| z1_m1 vs z0_m1 | attempt:text | 200 | 70.5% | 59.5% | +11.0 pp | +2.6 to +19.9 | 25 / 3 | 1.92e-4 |
| z0_rel_image vs z0_rel_text | attempt:image | 200 | 91.5% | 66.0% | +25.5 pp | +14.5 to +37.9 | 57 / 6 | 1.97e-10 |
| z0_rel_image vs z0_rel_text | attempt:text | 200 | 7.5% | 32.0% | -24.5 pp | -36.0 to -13.8 | 5 / 54 | 2.10e-10 |
| z1_rel_image vs z1_rel_text | attempt:image | 200 | 35.0% | 34.5% | +0.5 pp | -5.2 to +6.7 | 6 / 5 | 1 |
| z1_rel_image vs z1_rel_text | attempt:text | 200 | 64.0% | 65.0% | -1.0 pp | -7.0 to +4.6 | 4 / 6 | 1 |
| z0_m1 vs z0_filler | attempt:image | 200 | 36.5% | 20.5% | +16.0 pp | +2.4 to +28.8 | 49 / 17 | 6.09e-4 |
| z0_m1 vs z0_filler | attempt:text | 200 | 59.5% | 40.5% | +19.0 pp | +1.4 to +35.0 | 70 / 32 | 0.0011 |
| z1_m1 vs z1_filler | attempt:image | 200 | 25.5% | 29.0% | -3.5 pp | -16.0 to +10.0 | 28 / 35 | 1 |
| z1_m1 vs z1_filler | attempt:text | 200 | 70.5% | 43.0% | +27.5 pp | +12.4 to +42.2 | 72 / 17 | 3.17e-8 |

### Behaviour, primary (exact answer)

| First vs second | Outcome | n | First | Second | Difference | 95% interval | First only / second only | Holm p |
|---|---|---:|---:|---:|---:|---:|---:|---:|
| conflict_v3 vs placebo_v3 | answer:image | 200 | 4.5% | 14.5% | -10.0 pp | -21.3 to +0.5 | 9 / 29 | 0.0083 |
| conflict_v3 vs placebo_v3 | answer:text | 200 | 41.5% | 2.5% | +39.0 pp | +26.8 to +51.1 | 80 / 2 | 2.39e-20 |
| conflict_full vs filler | answer:image | 200 | 19.5% | 4.0% | +15.5 pp | +6.4 to +26.3 | 33 / 2 | 2.94e-7 |
| conflict_full vs filler | answer:text | 200 | 59.0% | 75.0% | -16.0 pp | -29.0 to -5.0 | 12 / 44 | 1.46e-4 |
| desc_image_first vs filler | answer:image | 200 | 24.0% | 4.0% | +20.0 pp | +8.6 to +31.0 | 46 / 6 | 9.29e-8 |
| desc_image_first vs filler | answer:text | 200 | 3.5% | 75.0% | -71.5 pp | -82.4 to -59.8 | 0 / 143 | 3.23e-42 |
| desc_text_first vs filler | answer:image | 200 | 38.0% | 4.0% | +34.0 pp | +22.7 to +45.8 | 70 / 2 | 1.67e-17 |
| desc_text_first vs filler | answer:text | 200 | 33.5% | 75.0% | -41.5 pp | -55.3 to -27.7 | 6 / 89 | 7.52e-19 |
| desc_image_first vs desc_text_first | answer:image | 200 | 24.0% | 38.0% | -14.0 pp | -28.3 to +1.0 | 26 / 54 | 0.0083 |
| desc_image_first vs desc_text_first | answer:text | 200 | 3.5% | 33.5% | -30.0 pp | -42.1 to -17.7 | 4 / 64 | 8.22e-14 |
| detect_only vs filler | answer:image | 200 | 22.0% | 4.0% | +18.0 pp | +7.8 to +28.6 | 39 / 3 | 5.63e-8 |
| detect_only vs filler | answer:text | 200 | 44.5% | 75.0% | -30.5 pp | -42.9 to -17.9 | 5 / 66 | 1.43e-13 |
| reliability_only vs filler | answer:image | 200 | 31.5% | 4.0% | +27.5 pp | +16.5 to +39.3 | 57 / 2 | 8.22e-14 |
| reliability_only vs filler | answer:text | 200 | 44.5% | 75.0% | -30.5 pp | -43.3 to -17.9 | 7 / 68 | 1.28e-12 |
| filler vs direct | answer:image | 200 | 4.0% | 8.0% | -4.0 pp | -12.2 to +4.0 | 7 / 15 | 0.2676 |
| filler vs direct | answer:text | 200 | 75.0% | 63.0% | +12.0 pp | -0.5 to +24.1 | 40 / 16 | 0.0083 |
| conflict_full vs direct | answer:image | 200 | 19.5% | 8.0% | +11.5 pp | +0.6 to +22.4 | 32 / 9 | 0.0026 |
| conflict_full vs direct | answer:text | 200 | 59.0% | 63.0% | -4.0 pp | -18.2 to +9.8 | 26 / 34 | 0.3663 |

### Behaviour, secondary (attempt label)

| First vs second | Outcome | n | First | Second | Difference | 95% interval | First only / second only | Holm p |
|---|---|---:|---:|---:|---:|---:|---:|---:|
| conflict_v3 vs placebo_v3 | attempt:image | 200 | 7.0% | 52.5% | -45.5 pp | -59.0 to -31.2 | 8 / 99 | 6.11e-20 |
| conflict_v3 vs placebo_v3 | attempt:text | 200 | 67.5% | 6.5% | +61.0 pp | +46.2 to +74.3 | 130 / 8 | 2.76e-28 |
| conflict_full vs filler | attempt:image | 200 | 26.0% | 4.5% | +21.5 pp | +11.6 to +33.0 | 46 / 3 | 5.58e-10 |
| conflict_full vs filler | attempt:text | 200 | 70.5% | 88.5% | -18.0 pp | -31.0 to -4.9 | 14 / 50 | 4.24e-5 |
| desc_image_first vs filler | attempt:image | 200 | 37.0% | 4.5% | +32.5 pp | +20.3 to +44.8 | 69 / 4 | 2.93e-15 |
| desc_image_first vs filler | attempt:text | 200 | 13.0% | 88.5% | -75.5 pp | -86.1 to -63.2 | 2 / 153 | 9.53e-42 |
| desc_text_first vs filler | attempt:image | 200 | 46.5% | 4.5% | +42.0 pp | +30.4 to +54.2 | 85 / 1 | 3.60e-23 |
| desc_text_first vs filler | attempt:text | 200 | 41.0% | 88.5% | -47.5 pp | -61.6 to -32.7 | 10 / 105 | 5.94e-20 |
| desc_image_first vs desc_text_first | attempt:image | 200 | 37.0% | 46.5% | -9.5 pp | -25.7 to +6.5 | 34 / 53 | 0.0888 |
| desc_image_first vs desc_text_first | attempt:text | 200 | 13.0% | 41.0% | -28.0 pp | -41.5 to -13.7 | 12 / 68 | 8.41e-10 |
| detect_only vs filler | attempt:image | 200 | 31.0% | 4.5% | +26.5 pp | +16.0 to +38.0 | 56 / 3 | 1.19e-12 |
| detect_only vs filler | attempt:text | 200 | 58.5% | 88.5% | -30.0 pp | -44.3 to -15.9 | 12 / 72 | 1.25e-10 |
| reliability_only vs filler | attempt:image | 200 | 37.0% | 4.5% | +32.5 pp | +21.7 to +44.6 | 66 / 1 | 1.20e-17 |
| reliability_only vs filler | attempt:text | 200 | 57.0% | 88.5% | -31.5 pp | -45.2 to -18.1 | 8 / 71 | 1.07e-12 |
| filler vs direct | attempt:image | 200 | 4.5% | 14.0% | -9.5 pp | -19.8 to +0.5 | 8 / 27 | 0.0075 |
| filler vs direct | attempt:text | 200 | 88.5% | 81.0% | +7.5 pp | -5.2 to +20.6 | 32 / 17 | 0.0888 |
| conflict_full vs direct | attempt:image | 200 | 26.0% | 14.0% | +12.0 pp | +1.0 to +24.2 | 38 / 14 | 0.0060 |
| conflict_full vs direct | attempt:text | 200 | 70.5% | 81.0% | -10.5 pp | -23.0 to +1.5 | 18 / 39 | 0.0225 |

## Qwen/Qwen2.5-VL-3B-Instruct | conflict | dev | repetition_penalty=1.05 | paraphrase=0

### Arms

| Arm | n | Exact image | Exact text | Same gold | Neither | Attempt image | Attempt text | Refusal | v3 abstain label | Token cap | Stops unsolved | Answer only | Fallback answer | Mean tokens |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| conflict_v3 | 200 | 18.0% | 48.5% | 0.0% | 33.5% | 24.0% | 71.5% | 1.5% | 12.5% | 1.5% | 0.0% | 0.0% | 79.5% | 203.7 |
| direct_v3 | 200 | 8.0% | 62.0% | 0.0% | 30.0% | 12.5% | 85.5% | 0.0% | 0.0% | 4.5% | 1.5% | 0.0% | 84.5% | 229.3 |
| placebo_v3 | 200 | 52.0% | 3.5% | 0.0% | 44.5% | 82.5% | 7.0% | 0.5% | 0.5% | 0.5% | 7.5% | 0.0% | 62.0% | 175.3 |

In single-source and congruent arms both gold answers are the same, so a correct answer appears under Same gold.

### Behaviour, primary (exact answer)

| First vs second | Outcome | n | First | Second | Difference | 95% interval | First only / second only | Holm p |
|---|---|---:|---:|---:|---:|---:|---:|---:|
| conflict_v3 vs placebo_v3 | answer:image | 200 | 18.0% | 52.0% | -34.0 pp | -46.8 to -20.8 | 7 / 75 | 1.73e-15 |
| conflict_v3 vs placebo_v3 | answer:text | 200 | 48.5% | 3.5% | +45.0 pp | +32.5 to +57.5 | 91 / 1 | 7.51e-26 |

### Behaviour, secondary (attempt label)

| First vs second | Outcome | n | First | Second | Difference | 95% interval | First only / second only | Holm p |
|---|---|---:|---:|---:|---:|---:|---:|---:|
| conflict_v3 vs placebo_v3 | attempt:image | 200 | 24.0% | 82.5% | -58.5 pp | -70.3 to -46.6 | 2 / 119 | 5.55e-33 |
| conflict_v3 vs placebo_v3 | attempt:text | 200 | 71.5% | 7.0% | +64.5 pp | +52.9 to +75.8 | 129 / 0 | 5.88e-39 |
