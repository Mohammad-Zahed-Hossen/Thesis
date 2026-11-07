# v4 analysis

Attempt, refusal and verdict labels are heuristics until validated by `sample_for_coding.py evaluate`.

## Gate failures

- Qwen/Qwen2.5-VL-3B-Instruct | conflict | dev | repetition_penalty=1.0 | paraphrase=0 | direct_v3: 16 missing rows, e.g. ['gsm8k-image-L0-0032', 'gsm8k-image-L0-0033']
- Qwen/Qwen2.5-VL-3B-Instruct | conflict | dev | repetition_penalty=1.0 | paraphrase=0 | base_text: token cap 8.0% (limit <5%)
- Qwen/Qwen2.5-VL-3B-Instruct | conflict | dev | repetition_penalty=1.0 | paraphrase=0 | desc_image_first: answer or refusal 72.5% (limit >=90%)
- Qwen/Qwen2.5-VL-3B-Instruct | conflict | dev | repetition_penalty=1.0 | paraphrase=0 | direct_v3: token cap 8.7% (limit <5%)
- Qwen/Qwen2.5-VL-3B-Instruct | conflict | dev | repetition_penalty=1.0 | paraphrase=0 | placebo_v3: answer or refusal 81.0% (limit >=90%)

## Repetition penalty, same arm and items

| Arm | Measure | n | Low penalty | High penalty | High only / low only | Exact McNemar p |
|---|---|---:|---:|---:|---:|---:|
| direct_v3 | exact image | 184 | 3.8% (1.0) | 8.2% (1.05) | 9 / 1 | 0.0215 |
| direct_v3 | exact text | 184 | 67.4% (1.0) | 60.9% (1.05) | 13 / 25 | 0.0730 |
| direct_v3 | attempt image | 184 | 4.3% (1.0) | 12.5% (1.05) | 16 / 1 | 2.75e-4 |
| direct_v3 | attempt text | 184 | 90.2% (1.0) | 85.9% (1.05) | 4 / 12 | 0.0768 |
| direct_v3 | stops without solving | 184 | 2.7% (1.0) | 1.6% (1.05) | 1 / 3 | 0.6250 |
| direct_v3 | v3 abstention label | 184 | 0.0% (1.0) | 0.0% (1.05) | 0 / 0 | 1 |
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
| base_image | 200 | 0.0% | 0.0% | 54.5% | 45.5% | 64.5% | 0.0% | 0.0% | 0.0% | 3.0% | 35.0% | 33.5% | 70.5% | 161.7 |
| base_text | 200 | 0.0% | 0.0% | 77.5% | 22.5% | 0.0% | 89.0% | 0.0% | 0.0% | 8.0% | 9.5% | 7.5% | 67.0% | 228.8 |
| conflict_full | 200 | 10.5% | 32.0% | 0.0% | 57.5% | 13.0% | 33.0% | 0.0% | 0.0% | 1.0% | 0.0% | 0.0% | 72.0% | 113.6 |
| conflict_v3 | 200 | 4.5% | 41.5% | 0.0% | 54.0% | 7.0% | 67.5% | 0.0% | 0.5% | 0.5% | 0.0% | 0.0% | 96.0% | 121.2 |
| congruent_conflict | 200 | 0.0% | 0.0% | 41.0% | 59.0% | 45.5% | 0.0% | 0.0% | 0.0% | 0.0% | 0.0% | 0.0% | 56.0% | 63.2 |
| congruent_detect | 200 | 0.0% | 0.0% | 54.5% | 45.5% | 54.0% | 0.0% | 1.0% | 0.5% | 0.0% | 26.5% | 0.0% | 43.0% | 86.0 |
| congruent_direct | 200 | 0.0% | 0.0% | 56.5% | 43.5% | 44.0% | 0.0% | 0.0% | 0.0% | 1.5% | 54.0% | 50.0% | 77.5% | 117.1 |
| desc_image_first | 200 | 22.0% | 8.0% | 0.0% | 70.0% | 38.5% | 13.5% | 0.0% | 0.0% | 1.0% | 38.5% | 0.0% | 56.5% | 104.3 |
| desc_text_first | 200 | 23.0% | 24.5% | 0.0% | 52.5% | 41.0% | 36.5% | 0.5% | 0.0% | 1.0% | 5.0% | 0.0% | 43.5% | 140.9 |
| detect_only | 200 | 10.0% | 19.0% | 0.0% | 71.0% | 19.0% | 26.5% | 14.0% | 4.0% | 2.5% | 0.0% | 0.0% | 50.5% | 97.9 |
| direct | 200 | 7.0% | 30.5% | 0.0% | 62.5% | 9.0% | 26.5% | 0.0% | 0.0% | 2.0% | 63.0% | 59.5% | 57.5% | 93.1 |
| direct_v3 | 184 | 3.8% | 67.4% | 0.0% | 28.8% | 4.3% | 90.2% | 0.0% | 0.0% | 8.7% | 2.7% | 1.1% | 90.8% | 229.0 |
| filler | 200 | 1.0% | 63.5% | 0.0% | 35.5% | 3.5% | 86.0% | 0.0% | 0.0% | 0.5% | 3.5% | 0.0% | 12.0% | 130.1 |
| placebo_v3 | 200 | 14.5% | 2.5% | 0.0% | 83.0% | 52.5% | 6.5% | 0.0% | 0.0% | 1.0% | 35.0% | 0.0% | 78.5% | 90.5 |
| reliability_only | 200 | 22.0% | 38.0% | 0.0% | 40.0% | 28.0% | 46.0% | 0.0% | 0.0% | 2.5% | 19.5% | 0.0% | 43.0% | 149.7 |

In single-source and congruent arms both gold answers are the same, so a correct answer appears under Same gold.

### Solvability: same problem from image alone and text alone

Image 55.9%, text 77.4% of 195 problems. Solved only from image / only from text: 8 / 50; exact McNemar p = 1.57e-8.

### Congruent arms: stated verdict (a conflict verdict here is a false alarm)

- congruent_conflict: {'agree': 194, 'none': 1, 'conflict': 5}
- congruent_detect: {'agree': 190, 'conflict': 10}
- congruent_direct: {'none': 200}

### Behaviour, primary (exact answer)

| First vs second | Outcome | n | First | Second | Difference | 95% interval | First only / second only | Holm p |
|---|---|---:|---:|---:|---:|---:|---:|---:|
| conflict_v3 vs placebo_v3 | answer:image | 200 | 4.5% | 14.5% | -10.0 pp | -21.3 to +0.5 | 9 / 29 | 0.0083 |
| conflict_v3 vs placebo_v3 | answer:text | 200 | 41.5% | 2.5% | +39.0 pp | +26.8 to +51.1 | 80 / 2 | 2.39e-20 |
| conflict_full vs filler | answer:image | 200 | 10.5% | 1.0% | +9.5 pp | +2.9 to +17.5 | 20 / 1 | 1.47e-4 |
| conflict_full vs filler | answer:text | 200 | 32.0% | 63.5% | -31.5 pp | -46.2 to -17.2 | 14 / 77 | 1.26e-10 |
| desc_image_first vs filler | answer:image | 200 | 22.0% | 1.0% | +21.0 pp | +10.6 to +31.6 | 44 / 2 | 3.08e-10 |
| desc_image_first vs filler | answer:text | 200 | 8.0% | 63.5% | -55.5 pp | -68.2 to -43.4 | 1 / 112 | 3.95e-31 |
| desc_text_first vs filler | answer:image | 200 | 23.0% | 1.0% | +22.0 pp | +12.3 to +33.0 | 46 / 2 | 1.09e-10 |
| desc_text_first vs filler | answer:text | 200 | 24.5% | 63.5% | -39.0 pp | -53.1 to -24.9 | 9 / 87 | 5.46e-16 |
| desc_image_first vs desc_text_first | answer:image | 200 | 22.0% | 23.0% | -1.0 pp | -13.5 to +11.5 | 26 / 28 | 1 |
| desc_image_first vs desc_text_first | answer:text | 200 | 8.0% | 24.5% | -16.5 pp | -28.3 to -5.7 | 6 / 39 | 4.33e-6 |
| detect_only vs filler | answer:image | 200 | 10.0% | 1.0% | +9.0 pp | +2.6 to +16.9 | 19 / 1 | 2.40e-4 |
| detect_only vs filler | answer:text | 200 | 19.0% | 63.5% | -44.5 pp | -57.7 to -31.2 | 7 / 96 | 6.73e-20 |
| reliability_only vs filler | answer:image | 200 | 22.0% | 1.0% | +21.0 pp | +12.2 to +31.5 | 42 / 0 | 6.37e-12 |
| reliability_only vs filler | answer:text | 200 | 38.0% | 63.5% | -25.5 pp | -40.4 to -11.5 | 18 / 69 | 2.99e-7 |
| filler vs direct | answer:image | 200 | 1.0% | 7.0% | -6.0 pp | -13.7 to +0.0 | 2 / 14 | 0.0167 |
| filler vs direct | answer:text | 200 | 63.5% | 30.5% | +33.0 pp | +18.1 to +47.1 | 83 / 17 | 1.44e-10 |
| conflict_full vs direct | answer:image | 200 | 10.5% | 7.0% | +3.5 pp | -4.1 to +11.4 | 15 / 8 | 0.6301 |
| conflict_full vs direct | answer:text | 200 | 32.0% | 30.5% | +1.5 pp | -12.6 to +15.5 | 37 / 34 | 1 |

### Behaviour, secondary (attempt label)

| First vs second | Outcome | n | First | Second | Difference | 95% interval | First only / second only | Holm p |
|---|---|---:|---:|---:|---:|---:|---:|---:|
| conflict_v3 vs placebo_v3 | attempt:image | 200 | 7.0% | 52.5% | -45.5 pp | -59.0 to -31.2 | 8 / 99 | 5.24e-20 |
| conflict_v3 vs placebo_v3 | attempt:text | 200 | 67.5% | 6.5% | +61.0 pp | +46.2 to +74.3 | 130 / 8 | 2.59e-28 |
| conflict_full vs filler | attempt:image | 200 | 13.0% | 3.5% | +9.5 pp | +0.5 to +19.8 | 25 / 6 | 0.0044 |
| conflict_full vs filler | attempt:text | 200 | 33.0% | 86.0% | -53.0 pp | -65.3 to -40.0 | 8 / 114 | 5.45e-24 |
| desc_image_first vs filler | attempt:image | 200 | 38.5% | 3.5% | +35.0 pp | +22.4 to +47.0 | 74 / 4 | 9.96e-17 |
| desc_image_first vs filler | attempt:text | 200 | 13.5% | 86.0% | -72.5 pp | -82.6 to -60.0 | 2 / 147 | 5.64e-40 |
| desc_text_first vs filler | attempt:image | 200 | 41.0% | 3.5% | +37.5 pp | +24.6 to +50.2 | 80 / 5 | 1.99e-17 |
| desc_text_first vs filler | attempt:text | 200 | 36.5% | 86.0% | -49.5 pp | -63.9 to -34.0 | 12 / 111 | 3.93e-20 |
| desc_image_first vs desc_text_first | attempt:image | 200 | 38.5% | 41.0% | -2.5 pp | -17.1 to +12.4 | 43 / 48 | 0.6752 |
| desc_image_first vs desc_text_first | attempt:text | 200 | 13.5% | 36.5% | -23.0 pp | -36.3 to -9.5 | 14 / 60 | 4.36e-7 |
| detect_only vs filler | attempt:image | 200 | 19.0% | 3.5% | +15.5 pp | +6.1 to +25.6 | 36 / 5 | 4.70e-6 |
| detect_only vs filler | attempt:text | 200 | 26.5% | 86.0% | -59.5 pp | -71.1 to -45.9 | 4 / 123 | 2.13e-30 |
| reliability_only vs filler | attempt:image | 200 | 28.0% | 3.5% | +24.5 pp | +14.0 to +35.3 | 51 / 2 | 2.54e-12 |
| reliability_only vs filler | attempt:text | 200 | 46.0% | 86.0% | -40.0 pp | -53.7 to -25.1 | 13 / 93 | 4.09e-15 |
| filler vs direct | attempt:image | 200 | 3.5% | 9.0% | -5.5 pp | -13.7 to +1.1 | 4 / 15 | 0.0768 |
| filler vs direct | attempt:text | 200 | 86.0% | 26.5% | +59.5 pp | +45.3 to +72.9 | 126 / 7 | 3.63e-28 |
| conflict_full vs direct | attempt:image | 200 | 13.0% | 9.0% | +4.0 pp | -5.3 to +14.3 | 20 / 12 | 0.5624 |
| conflict_full vs direct | attempt:text | 200 | 33.0% | 26.5% | +6.5 pp | -8.6 to +21.7 | 48 / 35 | 0.5624 |

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
