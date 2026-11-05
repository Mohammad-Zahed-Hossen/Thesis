# Statistical Hypothesis Testing & Evidence Audit Report

**Dataset Sample Size ($N$):** 500 clean image conflict pairs  
**Model:** Qwen2.5-VL-3B-Instruct  
**Protocol:** 4-Arm Causal Factorial Experiment  

---

## 1. Primary Empirical Findings & Hypothesis Tests

| Hypothesis / Metric | Value | Statistical Significance | Scientific Implication |
|:---|:---|:---|:---|
| **Placebo Visual Capture Rate ($P_{\text{vis}}(\text{Arm 2})$)** | **93.4%** (467/500) | Baseline Grounding | Multimodal descriptive prompts exhibit extreme visual bias |
| **Conflict Verbalization Visual Rate ($P_{\text{vis}}(\text{Arm 3})$)** | **31.4%** (157/500) | Post-Intervention | Conflict verbalization breaks default visual grounding |
| **Net Arbitration Shift ($\Delta_{\text{arb}}$)** | **+62.0 pp** | **p < 0.0001** | **Verbalization causally shifts decision arbitration** |
| **McNemar's Paired Test ($\chi^2_{\text{McNemar}}$)** | **$\chi^2 = 300.25$** | **p = 2.90e-67** | Within-subject shift is statistically definitive |
| **Fisher's Exact Test** | **p = 5.39e-101** | Two-sided exact | Reject independence of modality choice and verbalization |
| **Odds Ratio ($OR$)** | **30.92** | 95% CI: [20.72, 46.14] | Odds of visual grounding are 30.9x higher in placebo |
| **Cohen's $h$** | **1.43** | **Very Large Effect** ($h > 0.8$) | Strongest possible effect size magnitude |
| **Deliberative Abstention Rate** | **15.0%** | Novel Category | Verbalization enables legitimate epistemic refusal |

---

## 2. 2x2 Paired Contingency Matrix (Within-Subject Transition)

| Condition | Arm 3: Visual Capture | Arm 3: Non-Visual | Total |
|:---|:---:|:---:|:---:|
| **Arm 2: Visual Capture** | 153 (Persistent Visual) | 314 (Arbitrated / Abstained) | **467** |
| **Arm 2: Non-Visual** | 4 | 29 | **33** |
| **Total** | **157** | **343** | **500** |

McNemar's Test Discordant Pairs: $b = 314$, $c = 4$.  
$\chi^2_{\text{McNemar}} = \frac{(|314 - 4| - 1)^2}{314 + 4} = 300.2547$ ($p = 2.8992e-67$).

---

## 3. Full 4x4 Choice Transition Matrix

```
                          Arm 3 Output Choice
Arm 2 Output Choice    Image       Text      Abstain    Ambiguous    Total
Image                    153        220         73           21        467
Text                       4         20          2            3         29
Abstain                    0          0          0            0          0
Ambiguous                  0          4          0            0          4
Total                    157        244         75           24        500
```

---

## 4. Arm 4 Causal Rationale Steering Power

- **Divergence Rate ($1 - \text{Agreement}$):** 45.6% of items produce divergent answers under opposing rationale prefills.
- **Text Alignment Boost:** Arm 4b achieves a **+5.4 pp** increase in exact text-answer matching over Arm 4a.
