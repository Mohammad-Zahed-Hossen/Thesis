---

## 14. Competing explanations and hypotheses

### 14.1 Why this section exists

Most wasted effort in ML research comes from a design that cannot distinguish the intended cause from a boring one. The remedy is mechanical: **list every plausible explanation, then build a condition that separates them.** **[L3]**

### 14.2 The alternative-explanation taxonomy

For any behavioral effect, check for these. Most real effects are contaminated by at least two.

| Class | Concrete form | Cheap check |
|---|---|---|
| Compute / length | Longer generations get more layer passes | Token and step counts per arm |
| Prompt framing | Wording, politeness, role, format, position | Neutral rewording arm |
| Instruction burden | Arm asks for more work, not different work | Equal-format instruction |
| Measurement artifact | Parser, classifier, or regex picks up the wrong thing | Manual inspection of 20 outputs |
| Data artifact | Templated items, label leakage, duplicate items | Item inspection, dedup, label statistics |
| Class imbalance | Effect driven by a majority class | Per-class breakdown |
| Model-specific quirk | One model's prompt sensitivity | Second model of different family/size |
| Decoding parameters | Temperature, top-p, max tokens, stop criteria | Fixed decoding across arms |
| Preprocessing | Resolution, resizing, image normalization | Same pipeline verified by checksum |
| Seed variance | Run-to-run variation mistaken for effect | Repeat on 2–3 seeds or deterministic setting |
| Contamination | Test items present in training data | Check dataset provenance and model card |
| Annotator/judge bias | Subjective labels or LLM judge drift | Inter-rater agreement; judge calibration set |
| Selection of examples | Hand-picked items that favor the story | Random sampling with a fixed seed |
| Truncation / failure | Output cut off before the behavior appears | Truncation counters per arm |

### 14.3 Turn explanations into competing hypotheses

For each explanation, write a **signature**: what the data must look like if it is the true cause.

```text
H_effect : behavior B is caused by the manipulated construct C
           signature: B rises only when C is present; matched neutral arm shows no rise

H_confound_length : B is caused by additional computation
           signature: a neutral arm with the same token budget shows the same rise

H_confound_format : B is caused by output-format instructions
           signature: an arm with identical format but no C shows the same rise

H_artifact : B is caused by the classifier/parser
           signature: manual annotation of a sample disagrees with the automatic labels

H_null : B does not exist; observed difference is noise
           signature: effect disappears on rerandomized splits or additional seeds
```

### 14.4 The control matrix

Draw the arms as rows, the explanations as columns, and mark which arm can rule out which explanation. Every column must have at least one arm marked, or you cannot rule that explanation out.

| Arm | rules out length | rules out framing | rules out format | rules out artifact |
|---|---|---|---|---|
| Direct baseline | – | – | – | – |
| Neutral placebo, matched length | ✔ | partial | – | – |
| Neutral placebo with identical output format | ✔ | ✔ | ✔ | – |
| Manual annotation audit (20 items) | – | – | – | ✔ |
| Repeat with alternate seed / second model | – | – | – | – |

If a cell is empty on the diagonal, your design cannot attribute the effect. Fix the design or weaken the claim. **[L3]**

### 14.5 Worked instance (your design, reconstructed) **[L2]**

Your protocol's four arms map onto this matrix as follows:

- **Arm 1 (direct zero-shot):** establishes the unaided behavior — and revealed the text-following default (85.5% text; 13.8% image).
- **Arm 2 (neutral placebo):** controls for deliberation/length — and produced 89.5% image-following, exposing a large prompt-framing effect.
- **Arm 3 (conflict verbalization):** the manipulation of interest — 25.8% image-following, 13.7% abstention.
- **Arm 4 (prefill probes):** attempts to distinguish "explanation steers behavior" from "explanation is post-hoc," by injecting opposing rationale prefixes and observing divergence (41.4% divergence; +5.3 pp text alignment in one direction).

The residual weakness, stated honestly: **Arm 2 matched length on average but not per item** in the early run (61.2 vs 3.4 tokens for direct), and prompt framing differs between the direct and placebo arms in ways that may themselves be the cause of the "visual capture" pattern. A reviewer will attack this before anything else. Writing that sentence yourself, in the thesis, converts a fatal flaw into a stated limitation with a concrete future experiment. **[L2/L3]**

### 14.6 Rules for hypothesis hygiene **[L3]**

- Exactly two primary hypotheses (H₁ and H₀), each with a signature.
- Both outcomes must be publishable statements; if a null result would be embarrassing rather than informative, your question is not scientific enough yet.
- Record the decision rule *before* the run: threshold, test, and the interpretation of each outcome.
- Do not stack many secondary hypotheses to fish for significance. Label exploratory analyses as exploratory.
- If a third explanation appears after the data arrive, report it as exploratory and plan a follow-up; do not silently re-frame the original hypothesis.
