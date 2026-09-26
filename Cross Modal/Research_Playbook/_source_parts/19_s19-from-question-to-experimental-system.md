---

## 19. From research question to experimental system

### 19.1 The transition, with the reasoning at each step

```text
Question
  → Hypotheses            (why: make predictions falsifiable)
  → Variables             (why: make the comparison operational)
  → Controls              (why: exclude rival causes)
  → Dataset               (why: fix the population and the unit of analysis)
  → Baseline              (why: define "no effect" and the trivial alternative)
  → Evaluation            (why: define what counts as evidence)
  → Pilot                 (why: validate the instrument before committing)
  → Main experiment       (why: produce the decisive contrast at scale)
  → Ablations             (why: attribute the effect to the intended component)
  → Robustness            (why: test boundary conditions and fragility)
  → Analysis              (why: quantify and test, with stated assumptions)
  → Interpretation        (why: separate what was shown from what is suggested)
  → Contribution          (why: state what changed in the field's knowledge)
```

Each arrow is a *commitment*. Freezing an earlier step reduces the freedom of later steps, which is why freezes should be minimal and deliberate. **[L3]**

### 19.2 Operationalization: the step students skip

A question is not executable until each term becomes a measurable operation:

| Abstract term | Operational decision | Risk if left vague |
|---|---|---|
| "Follows the image" | Classifier over entity mentions + exact answer match as secondary | Construct drift; disputes about interpretation |
| "Conflict verbalization" | Exact prompt template with fixed sentence count and format | Unreproducible intervention |
| "Matched control" | Per-item token count within tolerance, same format | Confound with compute |
| "Abstention" | Explicit refusal patterns parsed deterministically, plus manual audit | Inflated abstention from truncation |
| "Longer reasoning" | Token count of the reasoning segment, not the whole output | Circular measurement |

Write the operational table into the Experiment Specification (§29). If two people would implement different things from your description, it is not yet operational. **[L3]**

### 19.3 Unit of analysis

Decide once: is the unit the item, the item×arm pair, the model, or the seed? This determines the statistical test. For paired within-item comparisons (as in your design), the natural unit is the item, and discordant pairs drive McNemar's test. Getting this wrong is one of the most common reviewer objections. **[L1/L3]**

### 19.4 What to freeze and what to leave free

| Freeze before the main run | Leave flexible until analysis |
|---|---|
| Prompt templates (verbatim, in the repo) | Exploratory subgroup analyses |
| Token budgets per arm | Additional descriptive statistics |
| Model revision and dtype | Visualization choices |
| Dataset split and item selection | Follow-up experiments for future work |
| Parsing/classification rules and thresholds | Secondary outcome definitions |
| Primary hypothesis, primary metric, decision rule | Narrative emphasis |
| Seeds and decoding parameters | Discussion framing |

Flexibility in the left column is a risk, not a virtue. Flexibility in the right column is normal science. **[L3]**

### 19.5 Pre-specify the analysis plan (one page)

```text
PRIMARY:    metric, comparison, test, threshold, direction
SECONDARY:  exploratory analyses, clearly labeled
EXCLUSIONS: items dropped and why (unparseable, degenerate, truncated)
PARSING:    exact rules, fallbacks, and manual-audit procedure
REPORTING:  distributions, effect sizes, CIs, and per-arm token statistics
FAILURE:    what each null result implies
```

### 19.6 Engineering that serves science

Your harness already contains the right instincts and is worth reusing as a template: deterministic seeds, checkpointing with resume, per-item token and truncation flags, storing both prompt and raw outputs, fixed output directories, and a separate statistical suite that emits markdown plus a LaTeX table. **[L2]**

Three improvements worth making in the next project **[L3]**:

1. **Log the token distribution per arm**, and assert the per-item matching tolerance in code — so the control's validity is machine-checked, not assumed.
2. **Log classifier inputs and outputs** for a random sample, so manual validation is a script, not a memory.
3. **Write a `PROTOCOL.md`** with the frozen config, commit-like hash of prompt templates, and the analysis plan *before* the main run. In a project without Git history, this file is your reproducibility backbone. (See §25.6 and [arXiv:2003.12206](https://arxiv.org/abs/2003.12206).)
