---

## 21. Pilot to main experiment

### 21.1 What a pilot is actually for

A pilot is **instrument validation**, not a miniature version of the study. Its jobs **[L3]**:

1. Verify parse rate and format compliance.
2. Verify token budgets — no arm should hit the ceiling.
3. Verify the classifier against manual labels on a sample.
4. Verify that arms produce distinguishable behavior at all.
5. Measure wall-clock time per item to size the main run.
6. Detect degenerate outputs (refusals, repetition, format collapse).
7. Check that the control is matched per item.

A pilot need not have statistical power. It needs to be *diagnostic*.

### 21.2 Pilot acceptance gates (numeric, written in advance)

```text
GATE 1  parse rate ≥ 90% per arm
GATE 2  truncation at ceiling ≤ 5% per arm
GATE 3  classifier manual-agreement ≥ 90% on 20 sampled outputs
GATE 4  per-item token matching within ±20% for the matched control arms
GATE 5  no arm produces > 10% degenerate outputs
GATE 6  both directions of the contrast are observable (the metric can move)
```

If a gate fails, fix the instrument and re-pilot. Do not run the main experiment to "see what happens." **[L2/L3: your 500-item run failed GATE 2 at 100% truncation in one arm and had to be discarded.]**

### 21.3 The main run

- **Freeze the config** (prompts, budgets, model revision, dtype, decoding, seeds) and record it in `PROTOCOL.md`.
- **Checkpoint every item** with resume support; store raw outputs, not only labels.
- **Log diagnostics** continuously: token counts, truncation flags, parse failures, wall time.
- **Monitor, do not tune.** If you change a template mid-run, you must restart; post-hoc tuning destroys the inferential claim.
- **Watch for systematic failures** in the first 50 items; if a gate breaks wholesale, stop and re-pilot.
- **Do not analyze the hypothesis until the run finishes**, or use a pre-registered interim rule.

### 21.4 What your own pilot changed **[L2]**

The pilot's value is visible in the artifacts:

| Pilot discovery | Design change | Consequence |
|---|---|---|
| 85% of direct outputs matched neither answer: the model **computes** rather than **selects** | Replaced exact-match "source arbitration" with engaged-problem classification; abstention became an explicit category | The construct now matches the measure; abstention became a reportable finding |
| Placebo 61.2 tokens vs direct 3.4 tokens | Enforced structured output format and longer budgets; later v3 used 80/200/20 tokens by arm group | The control became plausibly matched; truncation was eliminated |
| 100% truncation at 15 tokens; 90–98% at 90 tokens | Raised budgets; added truncation flags per item | Exact-match accuracy became interpretable at all |
| Conflict arm abstained 25% in 20 items | Abstention modeled as an outcome rather than an anomaly | Produced a second, publishable research question (§7.6) |

That table is the empirical argument for piloting, drawn from your own work rather than from generic advice.

### 21.5 Pilot-to-main decision rule **[L3]**

```text
All gates pass + direction observable + compute affordable → run main
Any gate fails + fixable in ≤2 days                     → fix, re-pilot
Any gate fails + not fixable in ≤2 days                 → narrow the question
Direction not observable even at pilot scale            → the effect is too small for
                                                          the available scale: re-scope
```

### 21.6 Ablations and robustness after the main run

**Ablations** attribute the effect to the intended component: remove the conflict sentence, shorten the explanation, vary the instruction verb, change the position of the conflict statement. **Robustness** tests fragility: alternate dataset slice, alternate model, alternate decoding temperature, alternate classification threshold, random half-split replication. **[L3]**

Order of operations: main result → ablations that answer the strongest objection → robustness on the most fragile assumption. Do not ablate before you know the main effect exists.
