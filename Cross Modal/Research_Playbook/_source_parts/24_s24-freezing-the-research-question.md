---

## 24. Freezing the research question

### 24.1 What "freeze" means

A freeze is a **contract with your future self**: the question, hypotheses, primary metric, controls, budgets, and analysis plan stop moving, so that later analyses cannot be tuned to a preferred outcome. It is not a declaration that the science is finished or that no interpretation will change. **[L1/L3]**

### 24.2 Freeze checklist (all required)

- [ ] **Question** is one sentence, names the comparison, and is answerable by the design.
- [ ] **H₁ and H₀** each have a written signature (what the data look like under each).
- [ ] **Primary metric** is operationally defined, deterministic (or judge-calibrated), and validated on a sample by hand.
- [ ] **Controls** are specified per item (matched length/format/budget), with tolerance written down.
- [ ] **Population** is fixed: model revision, dataset split, item count, exclusions.
- [ ] **Pilot gates** have passed (§21.2), with numbers recorded.
- [ ] **Analysis plan** is written before the main run: test, unit of analysis, thresholds, secondary analyses labeled exploratory.
- [ ] **Compute budget** is estimated and affordable within the session limits.
- [ ] **Boundary statement** is written: what this study does *not* claim.
- [ ] **Closest-work table** is complete and date-stamped, with the design-difference statement.
- [ ] **Failure interpretations** are written for each possible outcome.

If any box is unchecked, the honest status is "pre-freeze", and the correct action is one more pilot, not one more document.

### 24.3 What is *not* frozen

- **Interpretation** — must follow the data, including surprises.
- **Related work** — may be updated until submission; new papers can be cited as concurrent work.
- **Additional robustness checks** — allowed if reported as exploratory and not used to replace the pre-registered analysis.
- **Future work** — grows from your constraints and open branches.

### 24.4 Re-opening conditions

A freeze may be lifted only under pre-declared conditions, recorded with the change-control entry (§23.4). Typical legitimate triggers:

1. A pilot gate fails in a way that invalidates the measurement.
2. The main run reveals the metric cannot move (ceiling/floor).
3. A concurrent publication appears with the same design and construct.
4. A confound is discovered that no arm can rule out.

Illegitimate triggers: the result is not significant; the effect is smaller than hoped; a reviewer or advisor prefers a different story; you found a newer, shinier idea.

### 24.5 Freeze artifacts (produce these three files)

```text
PROTOCOL.md        frozen design, prompts verbatim, budgets, seeds, model revision
ANALYSIS_PLAN.md   primary/secondary analyses, tests, exclusions, thresholds
BOUNDARY.md        one paragraph on what the study does not claim
```

Together these cost an afternoon and are worth more than a chapter of prose. **[L1: reproducibility and pre-registration practice; L3: format.]**

### 24.6 What happened in your own project, and the lesson **[L2]**

From the retained artifacts:

- **2026-09-23:** 20-item pre-freeze pilot produced five findings, including the "neither answer" discovery, the length mismatch, and the abstention result. Its action list ended with: *"Re-run the 20-item pilot with the revised prompts and verify parse rate ≥ 90%. Only THEN freeze the topic."*
- **2026-09-24:** the post-freeze handover declares the topic locked and the empirical run complete across N = 1,619.

The v3 harness *does* implement the pilot's fixes (structured format, per-arm budgets of 80/200/20, truncation flags, checkpointing, stored raw outputs). But the retained corpus does not show a documented second pilot with gate numbers before the main run, nor a recorded classifier-agreement audit. **[L2]**

**Lesson [L3]:** the freeze was probably right in substance — the design improvements were real — but the *evidence trail* for the freeze is missing. In future projects, freeze **after** pasting gate results into `PROTOCOL.md`. The freeze date should be a consequence of the evidence, not a calendar decision made the next morning. This is a process fix, not a criticism of the result: the resulting full-population statistics (89.5% → 25.8%, McNemar p = 1.2e-215) are strong, and the truncation problem was genuinely resolved.
