---

## 16. Fast idea-killing

### 16.1 Why fast killing is a skill

An idea killed in two days returns three months. An idea killed in month three costs a thesis. The objective is high *decision throughput*, not low ambition. **[L3]**

### 16.2 One-hour kill checklist

Answer yes/no with a one-line reason for each:

1. Can I state the phenomenon in one sentence without my method? (no → not a phenomenon yet)
2. Can I state the comparison in one sentence? (no → not a question yet)
3. Can I name at least two explanations? (no → it is an observation, not a question)
4. Does a matched control for the naive comparison exist? (no → the gap may be real)
5. Do data and compute exist today? (no → infeasible unless obtainable within a week)
6. Is there a deterministic measure? (no → high risk)
7. Would a null result be informative? (no → kill)
8. Can I run a 20-item pilot this week? (no → the plan is too large)
9. Is the closest experiment different in design, not just wording? (no → kill)
10. Can I state what the field believes now and what it would believe afterwards? (no → not yet valuable)

Score: 8–10 yes → pilot. 5–7 → narrow or repair. 0–4 → kill now, in writing, with one line of reason.

### 16.3 The pre-mortem

Write the post-mortem before starting:

> "We abandoned this project in month three because ______."

Fill in the three most likely causes, then schedule the earliest cheap experiment that tests the most likely one. Anxiety becomes a plan. **[L3]**

### 16.4 Kills and parks from your own history, reconstructed **[L2]**

| Field | Reason parking it was correct | Killed early? |
|---|---|---|
| Medical imaging and federated learning | Required clinical data, domain labels, multi-institution simulation | No — large audits first |
| Cultural / Bangla VLM repair | Required annotation-heavy cultural evaluation and local benchmark assets | No — extensive autopsies first |
| Multimodal agents (tool use, robotics) | Needed multi-step environments and unbounded evaluation | No — parked after large explorations |
| Binding-IDs natural transfer | Depended on reproducing an external mechanism on new data with unclear controls | Partially |
| Reasoning-trace degradation | Crowded and moving quickly; needs matched-compute controls | Partially |

**Pattern [L2]:** the verdicts were mostly right; the *timing* was late. Each field consumed weeks of reading and document production before the disqualifying constraint (data access, annotation cost, environment complexity, concurrency) was actually evaluated.

### 16.5 The two-day kill window

**[L3] Adopt as a standing rule:**

> Every candidate direction is killed or promoted within **two working days**. Promotion requires a written design vector, a started closest-work table, a feasibility check, and a specified 20-item pilot. Anything else is parked in writing.

Applied consistently, this single rule would have removed the majority of the time cost visible in the retained history. It also makes killing cheap emotionally: parking is the *default*, and promotion is an earned status.

### 16.6 Writing a kill note

Keep it to five lines and store it in the Question Ledger:

```text
CANDIDATE: <one sentence>
KILLED BY: <citation | data unavailable | non-deterministic measure | no discriminating experiment | trivial baseline>
WHAT I LEARNED: <one sentence usable in future>
REOPEN IF: <explicit condition, e.g., "a public Bangla cultural benchmark is released">
DATE: <date>
```

"Reopen if" is important: it prevents both premature killing of good ideas and endless re-litigation of bad ones. **[L3]**
