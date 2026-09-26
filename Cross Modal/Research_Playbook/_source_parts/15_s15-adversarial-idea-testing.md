---

## 15. Adversarial idea testing

### 15.1 Purpose

You are not defending your idea. You are trying to destroy it as cheaply as possible, because the cost of destruction rises monotonically with time invested. **[L3]**

### 15.2 The attack list

| Attack | The question | Fatal hit |
|---|---|---|
| Prior-art | "Which single paper could already have killed this?" | A matching manipulation + measurement |
| Redundancy | "What result would make my contribution unnecessary?" | A trivial baseline reproduces the finding |
| Simplicity | "What is the simplest explanation for the expected result?" | Prompt length or formatting explains it |
| Data | "Could dataset construction produce the effect?" | Templated or synthetic conflicts unacknowledged by the paper |
| Baseline | "Could a trivial baseline reproduce it?" | Majority-class or prompt-only baseline matches it |
| Compute | "Could extra compute explain the gain?" | Unmatched tokens or steps |
| Prompt wording | "Could phrasing alone explain it?" | Rewording reproduces it |
| Measurement | "Does my experiment measure the thing I claim?" | Metric conflates selection with computation |
| Statistics | "What if the sample were smaller or split differently?" | Effect only under one arbitrary split |
| Generalization | "Does this depend on one model, dataset, language?" | Yes, while the mechanism story predicts universality |
| Reviewer | "What is the first sentence a skeptical reviewer writes?" | Unanswerable within one experiment |
| Publication risk | "Could someone publish this while I run it?" | Crowded, fast-moving space |

### 15.3 The strongest-objection discipline

Write the *strongest* objection (not a straw man), the evidence that answers it, and the residual vulnerability:

```text
STRONGEST OBJECTION: The effect is explained entirely by output length.
EVIDENCE TO ANSWER: A neutral deliberation arm with per-item token matching
                    shows no comparable shift.
RESIDUAL VULNERABILITY: Neutral arm wording still differs; add a second neutral
                    variant with different content at equal length.
```

If answering the objection needs more compute than you have, the question is currently infeasible (§17). That is a finding, not a failure.

### 15.4 Red-team with three personas **[L3]**

- **Statistician:** "Sample size, unit of analysis, paired or unpaired test, multiple comparisons?"
- **Hater:** "This is just prompt engineering." Your response must be a *design element*, not a paragraph of prose.
- **Replicator:** "I have one hour and your paper. Can I reproduce your numbers?" If not, your reporting is incomplete.

### 15.5 Worked adversarial audit of your frozen design **[L2]**

| Attack | Status in the retained evidence | What remains |
|---|---|---|
| Prior-art | Text-LLM faithfulness and multimodal detection benchmarks exist; no matching matched-legit control located in the workspace | Complete §12.4 statement and date-stamp the search |
| Simplicity (length) | Arm 2 is the intended answer, but early arms were unequal in tokens (61.2 vs 3.4) | Verify per-item token matching in the v3 run; report token distributions per arm |
| Simplicity (framing) | Direct arm follows text 85.5%; placebo follows image 89.5% | State explicitly that "visual capture" is framing-dependent; add a wording variant if budget allows |
| Measurement | Switched from exact match to engaged-problem classification after the pilot | Report classifier validation (manual audit of a sample, agreement rate) |
| Data | Synthetic arithmetic pairs with templated structure | Report item-level statistics; test a second domain (e.g., chart conflict) if feasible |
| Statistics | Paired McNemar plus Fisher's exact and effect sizes computed | Report the unit of analysis and independence assumptions; run a robustness check on a random half |
| Generalization | Single 3B model family | State as a boundary; second model of a different family is the natural follow-up |

This table is the artifact that turns a description into a defensible thesis: every weakness is named, bounded, and either answered or scheduled.
