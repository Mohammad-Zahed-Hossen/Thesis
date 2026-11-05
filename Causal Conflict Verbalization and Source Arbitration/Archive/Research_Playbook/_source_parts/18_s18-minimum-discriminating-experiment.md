---

## 18. Designing the minimum discriminating experiment

### 18.1 Definition

> The **minimum discriminating experiment (MDE)** is the smallest procedure that makes two live explanations predict different observations.

It is not the smallest experiment that produces a number. It is the smallest one that produces a *decision*. **[L1/L3]**

### 18.2 Why this is decisive for a short thesis

A short thesis cannot win by scale — you cannot out-train a lab. It wins by **design leverage**: a small, well-controlled experiment can produce a strong causal claim, while a huge, uncontrolled one produces nothing interpretable. **[L3]**

The reduction procedure:

```text
1. State the claim you want to be able to make.
2. State the two explanations it must separate.
3. Ask: what is the smallest observable difference between them?
4. Choose the minimum population that can show that difference.
5. Fix every other variable.
6. Define the failure interpretation.
```

### 18.3 Five worked reductions

| Instead of… | Run the MDE… | Why it works |
|---|---|---|
| "Build a new VLM architecture for conflict handling" | Does injecting an opposing rationale as a prefix change the final answer more often than a matched neutral prefix? | Isolates the causal contribution of the *explanation* without changing the model |
| "Build a new benchmark for cross-modal conflict" | Take 50 existing conflict items and test whether the standard metric conflates detection with arbitration | Tests a *claim about measurement*, cheaply and generally |
| "Train a culturally adapted multimodal model" | Does providing locally-grounded context (versus a length-matched generic context) change answers on the same 50 items? | Tests cultural-context sensitivity without training |
| "Perform full attention/representation analysis" | Does a length-matched neutral prompt reproduce the behavioral shift? | Removes the dominant confound before any mechanism work |
| "Show that long reasoning degrades perception" | Recompute the reported trend using a continuous perception metric on the *published* outputs | A metric-choice audit is hours of work and can change the conclusion ([arXiv:2304.15004](https://arxiv.org/abs/2304.15004)) |

### 18.4 How small can a pilot be?

For an **instrument-validation pilot**, 20–50 items is usually enough, because the goal is not significance but *parseability and direction*:

- Are outputs parseable at a target rate (e.g., ≥90%)?
- Do the arms produce distinguishable behavior at all?
- Are token budgets sufficient (no truncation at the ceiling)?
- Does the classifier agree with manual inspection on this sample?
- Are there degenerate outputs (refusals, repetition, format collapse)?

If the pilot cannot answer these questions, do not proceed to the main run. Your own project demonstrates the cost of skipping this: a 500-item run was invalidated by a 15-token budget that produced 100% truncation in one arm. **[L2]**

For the **main experiment**, sample size follows the effect size you are willing to detect and the precision you need for the estimate. With paired within-item designs and large effects, a few hundred items can be highly informative; with small effects, you need many more. Report confidence intervals, not only p-values. **[L1/L3]**

### 18.5 The "one comparison at a time" rule

A design where two things vary cannot attribute the effect. If you must vary two, include the factorial cell that isolates them. Your four-arm structure is exactly this logic: direct, neutral, conflict, and prefill-probe, with one manipulated dimension between the key arms. **[L2/L3]**

### 18.6 The one-GPU-hour exercise

Before designing a full study, ask: **"What can I learn in one GPU-hour?"** Then design that experiment and run it. It forces you to choose the most discriminating comparison. In your case, one GPU-hour covers roughly 1,500 item-passes — enough for a 500-item two-arm comparison, which is precisely the scope that revealed both the metric problem and the truncation problem. **[L2/L3]**

### 18.7 MDE acceptance checklist

The MDE is ready when all are true:

- [ ] Claim, explanations, and discriminating observation are written.
- [ ] Control is matched per item on the nuisance variables (length, format, budget).
- [ ] Outcome measure is deterministic and has been validated on 20 outputs by hand.
- [ ] Failure interpretation is written for each possible result.
- [ ] Compute estimate is under budget.
- [ ] You can explain the design to a peer in 60 seconds.
