---

## 13. Verifying whether a gap is real

### 13.1 The ten questions, with the evidence that answers each

| # | Question | How to answer it | Verdict if true |
|---|---|---|---|
| 1 | Has it been answered directly? | Find a paper whose manipulation + measurement match yours | Gap is **occupied** — kill or pivot |
| 2 | Has it been answered indirectly? | Look for a paper that answers your question as a side-effect of another study; check its tables | Gap likely **occupied** |
| 3 | Has an equivalent experiment been done under different terminology? | Search by design vector (§12.2), not by words | Occupied — re-frame your framing, not your experiment |
| 4 | Has later work closed the gap? | Forward citations, newest first; search the last 6 months | Occupied |
| 5 | Is it only a dataset/language/model difference? | Ask whether the effect could plausibly reverse; if not, it is a replication | **Weak gap** — insufficient alone |
| 6 | Is that difference scientifically meaningful? | Name a mechanism that would change across that difference | If you can name one → gap may be real |
| 7 | Is the missing experiment important? | Ask what claim currently rests on the untested assumption | If nothing rests on it → unimportant |
| 8 | Would the result change understanding? | Write the two sentences you would add to the field's knowledge under each outcome | If both sentences are dull → kill |
| 9 | Could the result be trivially predicted? | Ask whether a competent practitioner would bet on the outcome | If yes → not a research question |
| 10 | Would a negative result still teach something? | State what a null result rules out | If nothing → redesign or kill |

### 13.2 The three verdicts

- **REAL** — no matching manipulation+measurement found by two independent searches; the closest work's own limitations name your question; and both positive and negative outcomes carry meaning.
- **UNCLEAR** — searches are inconclusive, or you suspect terminology/dataset variants you cannot rule out. Cost of resolution: one more focused search session. Do not spend more than that before asking "could I answer my own question with a 20-item pilot instead?"
- **OCCUPIED** — a paper (or combination of two) already answers it. Record the citation, write one line, and move to your next candidate question. This is a win, not a failure: it cost you a day instead of three months.

### 13.3 Classes of "gap" and what they are actually worth **[L3]**

| Gap class | Typical value for a thesis |
|---|---|
| Missing control on a causal claim | **High** — small, decisive, defensible |
| Measurement validity (metric conflates constructs) | **High** — often generalizes beyond one dataset |
| Boundary condition (works only under X) | Medium–high — needs a mechanism story |
| Contradiction between two papers | Medium–high — a rerun with matched settings can resolve it |
| New dataset/benchmark | Medium — strong only if it exposes a new behavior, not just new items |
| Language/culture transfer | Medium — needs an argument that findings should not transfer |
| New method outperforming baselines | Medium — high risk, needs compute and careful baselines |
| Dataset substitution (M on D) | Low |
| Scale-up of an existing study | Low–medium |
| Exact-phrase novelty | Near zero |

### 13.4 Gap verification worksheet

```text
CANDIDATE GAP: <one sentence>
MY MANIPULATION / MEASUREMENT / POPULATION: <design vector>
SEARCH 1 (phenomenon terms):       queries used / hits / closest match
SEARCH 2 (design terms):           queries used / hits / closest match
SEARCH 3 (forward citations):      papers citing the anchor work / any with my control?
SEARCH 4 (recent 6 months):        anything new?
CLOSEST WORK:                      <citation> — manipulation/measurement/population
DESIGN DIFFERENCE:                 <two sentences from §12.4>
IF POSITIVE RESULT → field learns: <one sentence>
IF NEGATIVE RESULT → field learns: <one sentence>
VERDICT:                           REAL / UNCLEAR / OCCUPIED
DATE OF VERIFICATION:              <date>
NEXT ACTION:                       pilot / second search / kill
```

### 13.5 The self-deception test

Ask: **"If a competent reviewer were trying to reject my novelty claim, what paper would they cite?"** Then go find that paper. If you find it and it does not have your control or your measure, you have *strengthened* your claim and produced the related-work paragraph at the same time. If you find it and it does have them, you have saved months. **[L3]**

### 13.6 Your history at this step **[L2]**

Novelty in the workspace was repeatedly adjudicated by **vocabulary** ("no paper uses this term") and by **volume of audit documents**, rather than by design comparison. Two concrete consequences appear in the retained material:

1. Candidate branches (reasoning-trace degradation; binding-IDs natural transfer; cultural causal steering) were argued against literature that was summarized at high abstraction, making it hard to see whether a *matching control* existed.
2. The branch that ultimately survived did so because its design became concrete enough to compare: length-matched placebo, same items, per-item budgets, deterministic classification. Once the design vector existed, the novelty question became answerable in an afternoon.

**Rule [L3]:** you may not claim novelty until you can fill in §13.4 completely, including the closest work's manipulation and measurement. Abstract novelty claims are not falsifiable; design comparisons are.
