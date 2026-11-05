---

## 32. If I start a new research area tomorrow

A concrete eleven-day walkthrough. It assumes almost no prior knowledge, one 16 GB GPU, public data, and no advisor available for the first week. **[L3]**

### Day 1 — Orientation, not depth (4 hours)

- Search the area name plus `survey` and `position paper`; take the two most recent.
- Read only abstracts, figures, and conclusions. Do not take detailed notes.
- Write the Research Map skeleton: claims, measures, disagreements, unknowns, assets.
- Collect vocabulary variants as you go (slot 10).
- **Output:** one-page map with many `?` marks.

### Day 2 — Find the fault lines (4 hours)

- For each of the three main claims you found, write what the claim is based on and whether its control exists.
- Search explicitly for disagreement: `re-examining`, `limitations`, `does not hold`, `critique`, `under matched`.
- List the area's benchmarks, datasets, and models in the map.
- **Output:** map with competing directions and known failure modes; three candidate phenomena.

### Day 3 — Pick two territories, run a 48-hour feasibility probe

For each candidate: is there public data, an inspectable label, a ≤3B model that can express the behavior, and a deterministic measure? Write the one-page feasibility card (§17.1).

### Day 4 — Finish feasibility and kill one

- Compute the budget line honestly (§17.3).
- Apply §16.2 kill checklist.
- Park one candidate in writing with a reopen condition; promote one.
- **Output:** Question Ledger with one survivor and one documented park.

### Day 5 — Write the ladder for the survivor

- Write Area → Territory → Phenomenon → Observation → Existing claim → Alternatives → Gap → Question → Hypotheses → Experiment → Contribution (§7.1).
- Write the H₁/H₀ signatures.
- If any row is empty, today's work is to fill it — not to read more.
- **Output:** first draft of the Question Ledger entry.

### Day 6 — Closest work by design

- Decompose your design vector (§12.2).
- Run searches 1–10 from §9.2 using design terms.
- Complete the closest-work table and the two-sentence design-difference statement (§12.4).
- **Output:** novelty verdict: REAL / UNCLEAR / OCCUPIED (§13.2).

### Day 7 — Gap verification and adversarial attack

- Complete §13.4 worksheet, including the "if positive/if negative the field learns" lines.
- Run the §15.2 attack list. Write the strongest objection and your answer.
- **Output:** verdict and a mitigation list, or a kill note.

### Day 8 — Minimum discriminating experiment

- Reduce to the smallest procedure that separates the explanations (§18).
- Fix arms (≤6), budgets, control-matching tolerance, and metric.
- Write failure interpretations for every outcome.
- **Output:** one-page Experiment Specification draft; compute estimate.

### Day 9 — Build the smallest honest instrument

- Write the harness for 20 items only: prompts verbatim, structured output, token logging, truncation flags, raw output storage.
- Include a checkpoint so the pilot is resumable.
- **Output:** ~150–250 lines of code (your existing harness is a template).

### Day 10 — Run the pilot and inspect by hand

- Run 20 items across all arms.
- Read every output. Count parse rate, truncation, degenerate outputs, and whether the arms differ visibly.
- Apply the gates (§21.2).
- **Output:** gate table. If a gate fails, fix and re-run tomorrow.

### Day 11 — Decide, then scale or stop

- If the effect is observable and gates pass → freeze the design, expand to the main population.
- If the effect is not observable at 20 items → check instrument, then consider whether the effect is too small at your scale; re-scope or kill.
- **Output:** a frozen protocol with gate numbers, or a five-line kill note with a reopen condition.

### If you only have three weeks

Compress to:

```text
Days 1–2   orientation + map + feasibility (two territories)
Days 3–4   closest work + gap verification + attack
Day 5      experiment specification
Days 6–7   instrument + pilot + gates
Days 8–12  main run (inference-only, checkpointed)
Days 13–17 analysis + diagnostics + robustness
Days 18–21 write the thesis chapters that carry the claim
```

Note what is *not* compressed: controls, diagnostics, and the closest-work check. Scope shrinks first; rigor shrinks never. **[L3]**

### The three sentences to remember

1. **A phenomenon is not a question until two explanations predict different observations.**
2. **A gap is not a gap until you have compared designs, not words.**
3. **A design is not a design until the control is matched, the measure is validated, and the failure interpretation is written.**
