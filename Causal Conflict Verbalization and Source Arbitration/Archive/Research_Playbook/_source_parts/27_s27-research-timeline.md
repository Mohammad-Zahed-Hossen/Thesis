---

## 27. Research timeline

Ranges, not promises. Adjust for coursework, defense dates, and compute availability. **[L3]**

### Phase 0 — Orientation (3–7 days)

| Aspect | Detail |
|---|---|
| Objective | Know the area's arguments, vocabulary, and data landscape |
| Do | Read 10–15 abstracts/intros; build the one-page map (§11); collect vocabulary variants |
| Do not | Take detailed notes; read full papers; start writing a proposal |
| Move forward when | You can name the field's 3 main claims and its 2 main disagreements |
| Go backward when | You cannot find any disagreement or any data you could use |
| Output | One-page field map; 3 candidate territories |

### Phase 1 — Territory selection (1–2 weeks)

| Aspect | Detail |
|---|---|
| Objective | Choose ≤2 executable territories |
| Do | Score candidates (§5.3); check data/model/compute feasibility in 48 hours each |
| Do not | Explore a third territory, or extend a territory because it is comfortable |
| Forward | One territory scores clearly higher and yields a candidate phenomenon |
| Backward | All candidates blocked by data, annotation, or environment requirements |
| Output | Territory decision + parked list with one-line reasons |

### Phase 2 — Question formation (1–2 weeks)

| Aspect | Detail |
|---|---|
| Objective | Produce a question with two competing explanations and a discriminating observation |
| Do | Write the ladder (§7.1); write H₁/H₀ signatures; draft the design vector |
| Do not | Search for novelty by vocabulary; write long specifications |
| Forward | The four tests in §7.3 pass |
| Backward | You cannot name a discriminating observation |
| Output | Question Ledger entry with ranked candidates |

### Phase 3 — Adversarial verification (3–7 days)

| Aspect | Detail |
|---|---|
| Objective | Try to kill your own question |
| Do | Closest-work search (§12); gap verification (§13); attack list (§15.2) |
| Do not | Move to implementation to escape the discomfort of the search |
| Forward | Closest work differs in design; both outcomes informative |
| Backward | Matching manipulation+measurement found → next candidate or pivot |
| Output | Completed closest-work table + design-difference statement |

### Phase 4 — Feasibility and MDE (3–7 days)

| Aspect | Detail |
|---|---|
| Objective | Reduce the idea to a minimum discriminating experiment with an affordable compute line |
| Do | Compute the budget; write the failure interpretations; specify the control |
| Do not | Design the full thesis pipeline before the MDE is defined |
| Forward | Compute affordable; measure deterministic; control matchable |
| Backward | Any condition blocked by assets you do not have |
| Output | One-page experiment specification |

### Phase 5 — Pilot and instrument validation (1–2 weeks)

| Aspect | Detail |
|---|---|
| Objective | Validate the measurement before spending main-run compute |
| Do | 20–50 items; run the gates (§21.2); inspect outputs by hand |
| Do not | Interpret pilot results as findings; run the main experiment on an unvalidated instrument |
| Forward | All gates pass |
| Backward | Parse rate, truncation, or matching fails |
| Output | Gate table + revised prompts/budgets + classifier validation note |

### Phase 6 — Freeze and baseline (3–5 days)

| Aspect | Detail |
|---|---|
| Objective | Lock design and establish the trivial/strongest baselines |
| Do | Complete the freeze checklist; run baselines; archive raw outputs |
| Do not | Keep editing prompts; add arms for completeness |
| Forward | Baselines produce interpretable, non-degenerate behavior |
| Backward | Baseline cannot represent the behavior → narrow population |
| Output | `PROTOCOL.md`, `ANALYSIS_PLAN.md`, `BOUNDARY.md`, baseline numbers |

### Phase 7 — Main experiment (1–3 weeks)

| Aspect | Detail |
|---|---|
| Objective | Produce the decisive contrast at full population |
| Do | Checkpoint, resume, monitor diagnostics, archive everything |
| Do not | Tune mid-run; peek at hypotheses and adjust |
| Forward | Run completes with gates still passing |
| Backward | Systematic failure → stop, re-pilot |
| Output | Raw results, checkpoint, diagnostic summary |

### Phase 8 — Analysis, ablations, robustness (2–4 weeks)

| Aspect | Detail |
|---|---|
| Objective | Quantify, attribute, and stress-test the effect |
| Do | Primary analysis first; then strongest objection; then fragility checks |
| Do not | Fish for significant subgroups; report only the favorable split |
| Forward | Effect stable under diagnostics and at least one robustness check |
| Backward | Effect disappears under a fair robustness check → re-scope the claim |
| Output | Statistical report, tables, figures, Results Record |

### Phase 9 — Writing (4–8 weeks)

| Aspect | Detail |
|---|---|
| Objective | Produce a thesis whose claims match its evidence |
| Do | Write method and results first; keep limitations adjacent to results |
| Do not | Write introduction first; overclaim to make the story smoother |
| Forward | Each claim traced to a script and file |
| Backward | A claim cannot be traced → cut or weaken it |
| Output | Chapters, figures, tables, boundary statement |

### Phase 10 — Paper conversion (2–4 weeks after the thesis)

| Aspect | Detail |
|---|---|
| Objective | Extract one claim with the evidence needed to believe it |
| Do | Compress to one figure-led argument; add the strongest ablation |
| Do not | Submit the thesis; include every exploratory analysis |
| Output | Abstract, intro, method, results, limitations, reviewer-response plan |

**Schedule reality [L3]:** phases 2–5 are where projects die or become defensible, and they are the easiest to compress if you work with the two-day kill window (§16.5) and pilot gates. Phases 6–8 are the most predictable. If you are behind, cut *scope* (arms, datasets, models), never *controls* or *diagnostics* — cutting controls turns work into noise.
