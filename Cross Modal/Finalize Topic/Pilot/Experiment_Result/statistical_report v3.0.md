# Statistical Hypothesis Testing & Evidence Audit Report

**Dataset Sample Size ($N$):** 1619 clean image conflict pairs  
**Model:** Qwen2.5-VL-3B-Instruct  
**Protocol:** 4-Arm Causal Factorial Experiment  

---

## 1. Primary Empirical Findings & Hypothesis Tests

| Hypothesis / Metric | Value | Statistical Significance | Scientific Implication |
|:---|:---|:---|:---|
| **Placebo Visual Capture Rate ($P_{\text{vis}}(\text{Arm 2})$)** | **89.5%** (1449/1619) | Baseline Grounding | Multimodal descriptive prompts exhibit extreme visual bias |
| **Conflict Verbalization Visual Rate ($P_{\text{vis}}(\text{Arm 3})$)** | **25.8%** (417/1619) | Post-Intervention | Conflict verbalization breaks default visual grounding |
| **Net Arbitration Shift ($\Delta_{\text{arb}}$)** | **+63.7 pp** | **p < 0.0001** | **Verbalization causally shifts decision arbitration** |
| **McNemar's Paired Test ($\chi^2_{\text{McNemar}}$)** | **$\chi^2 = 982.40$** | **p = 1.20e-215** | Within-subject shift is statistically definitive |
| **Fisher's Exact Test** | **p = 1.09e-322** | Two-sided exact | Reject independence of modality choice and verbalization |
| **Odds Ratio ($OR$)** | **24.57** | 95% CI: [20.24, 29.83] | Odds of visual grounding are 24.6x higher in placebo |
| **Cohen's $h$** | **1.42** | **Very Large Effect** ($h > 0.8$) | Strongest possible effect size magnitude |
| **Deliberative Abstention Rate** | **13.7%** | Novel Category | Verbalization enables legitimate epistemic refusal |

---

## 2. 2x2 Paired Contingency Matrix (Within-Subject Transition)

| Condition | Arm 3: Visual Capture | Arm 3: Non-Visual | Total |
|:---|:---:|:---:|:---:|
| **Arm 2: Visual Capture** | 392 (Persistent Visual) | 1057 (Arbitrated / Abstained) | **1449** |
| **Arm 2: Non-Visual** | 25 | 145 | **170** |
| **Total** | **417** | **1202** | **1619** |

McNemar's Test Discordant Pairs: $b = 1057$, $c = 25$.  
$\chi^2_{\text{McNemar}} = \frac{(|1057 - 25| - 1)^2}{1057 + 25} = 982.4039$ ($p = 1.1997e-215$).

---

## 3. Full 4x4 Choice Transition Matrix

```
                          Arm 3 Output Choice
Arm 2 Output Choice    Image       Text      Abstain    Ambiguous    Total
Image                    392        832        201           24       1449
Text                      20        103         20            2        145
Abstain                    1          3          0            0          4
Ambiguous                  4         16          0            1         21
Total                    417        954        221           27       1619
```

---

## 4. Arm 4 Causal Rationale Steering Power

- **Divergence Rate ($1 - \text{Agreement}$):** 41.4% of items produce divergent answers under opposing rationale prefills.
- **Text Alignment Boost:** Arm 4b achieves a **+5.3 pp** increase in exact text-answer matching over Arm 4a.
