---

## 3. Why research is not linear

### 3.1 The false model

```text
choose field → search papers → find gap → formulate question
→ find dataset → build model → run experiment → write
```

### 3.2 The real loop

Any stage can send you backward:

```text
notice something
→ ask whether it is real
→ search for prior explanations
→ discover a competing explanation
→ inspect the measurement
→ discover the question is too broad
→ narrow the claim
→ run a pilot
→ discover the outcome does not measure the construct
→ repair the measure, narrow again, or abandon the branch
→ freeze a smaller question
```

### 3.3 Backtrack triggers — when going backward is correct

| Trigger | What it means | Local instance |
|---|---|---|
| Outcome does not measure the construct | The metric answers a different question | The diagnostic pilot showed 85% of direct-arm outputs matched *neither* precomputed answer, because the model **computed** a new answer instead of **selecting** one **[L2]** |
| Control is not matched | Arms differ in more than the intended variable | Neutral placebo averaged 61.2 tokens vs 3.4 for the direct arm **[L2]** |
| Baseline is a prompt artifact | Effect exists under one framing only | Direct baseline follows the **text** problem 85.5% of the time; the neutral placebo flips this to **89.5% image** **[L2]** |
| Closest work already answers it | The gap was terminology, not knowledge | Novelty repeatedly judged by phrase-variant searching rather than experiment comparison **[L2]** |
| Effect vanishes under controls | A nuisance variable drove it | Token truncation (15/90) invalidated exact-match accuracy for an entire run **[L2]** |
| Labels cannot support the reading | Benchmark tests a neighboring task | Detection/abstention benchmark used as if it measured arbitration **[L2]** |
| Result is trivially predictable | No belief would change | "Bigger model scores higher." |
| Only a p-value exists | No interpretable effect | Significant test on a metric that is not the construct. |

**Rule [L3]:** backtracking is not wasted time if it changes *what you measure*. It is wasted time if it only changes *how you write about the same measurement*.

### 3.4 Two kinds of stability

- **Conceptual stability** — the question names a construct the experiment can distinguish.
- **Operational stability** — implementation, metric, controls, seeds, and data quality are reliable enough to interpret.

You may freeze the concept before every engineering detail is final. You must not run the main experiment before the outcome is demonstrably able to measure that concept. **[L3]**

### 3.5 The price of pretending linearity

Research is written linearly; it is not performed linearly. Two costs appear in this workspace **[L2]**:

1. **Proposal-first commitment.** Long canonical specifications were produced before the measurement question was settled. When the pilot showed the metric was wrong, those documents already framed the question around the wrong measure — which raises the psychological cost of revising it.
2. **Freeze-by-repetition.** Declaring a phase "100% complete" in several documents does not create evidence. A freeze is credible only when the conditions in §24 hold.

### 3.6 The loop exit condition

Leave the discovery loop when **a new search or a new pilot no longer changes your next action**. Not when you feel certain — feelings do not converge — but when marginal information for the current decision is zero.

---

## 4. The researcher's mental model

### 4.1 All claims are conditional

Store every claim as:

> Under conditions **X**, intervention **Y** changed measure **Z** by **A** on population **D** under analysis **P**.

Then ask what would change the conclusion: a different population, seed, control, natural versus synthetic input, stronger or weaker model, corrected metric, or simpler baseline. Locating the boundary of a claim *is* the contribution. **[L1/L3]**

### 4.2 Three levels of explanation — never mix them silently

| Level | Question | VLM example | Supports |
|---|---|---|---|
| Descriptive | What happened? | "An intervention prompt reduced image-following from 89.5% to 25.8% of items." | Existence of a behavioral difference |
| Comparative | Under what conditions does it differ? | "The shift is absent with a neutral prompt matched in length." | Attribution to the manipulated variable |
| Mechanistic | Why? | "Attention to image tokens decreases as chains lengthen." | A hypothesis needing independent evidence |

A prompt-level intervention can establish a comparative result. It does not by itself establish a mechanistic one. Papers that blur these levels are the easiest place to find legitimate questions — and the easiest place to accidentally overclaim yourself. **[L3]**

### 4.3 The discrimination principle

An experiment exists to make explanations disagree. Before coding, write:

```text
If explanation A is true → we observe X
If explanation B is true → we observe Y
If X ≈ Y → this experiment cannot discriminate (redesign)
```

If X and Y can be the same number, do not run it. **[L3]**
