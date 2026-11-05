---

## 29. Reusable research workspace

Seven artifacts. Not thirty. Each has a job, a moment of creation, and a moment when it can be discarded. **[L3]**

### 29.1 Research Map

- **Purpose:** current understanding of the territory — claims, measures, disagreements, unknowns, available assets (ten slots in §11.2).
- **Created:** day 1 of a territory.
- **Updated:** whenever a search changes the map, and always before freezing (frontier date).
- **Contains:** one page, `?` for uncertain entries, ranked candidate questions with kill reasons.
- **Discard:** when the territory is parked or the project is published; keep it as an appendix note.

### 29.2 Question Ledger

- **Purpose:** every candidate question and its status, so decisions are not re-litigated.
- **Created:** as soon as a first candidate exists.
- **Updated:** every time a candidate is killed, narrowed, or promoted.
- **Contains:** per row — candidate (one line), design vector, closest work, kill reason, reopen condition, date.
- **Discard:** never; it doubles as your thesis's "open problems" section.

```text
| Candidate | Design vector (M/M/P) | Closest work | Status | Kill reason / next step | Reopen if | Date |
```

### 29.3 Evidence Ledger

- **Purpose:** what you believe and why, traceable to a primary source or your own result.
- **Created:** with the first serious reading.
- **Updated:** with every claim you intend to use.
- **Contains:** claim | source (paper DOI/arXiv ID, or own run ID) | evidence (number/figure/table) | control present? | limitation | date verified.
- **Discard:** never; it writes your related-work section.

### 29.4 Experiment Specification

- **Purpose:** the frozen design; the contract with your future self.
- **Created:** at freeze (§24).
- **Updated:** only through a documented re-open (§24.4).
- **Contains:** hypotheses with signatures, arms, prompts verbatim, budgets, control matching tolerance, dataset/split/exclusions, metric and parsing rules, seeds, model revision, analysis plan, failure interpretations.
- **Discard:** never during the project.

### 29.5 Research Log

- **Purpose:** chronological decisions, dead ends, bugs, surprises.
- **Created:** day 1; append-only.
- **Updated:** every working session (5 lines is enough).
- **Contains:** date | what I tried | what happened | decision | what I would do differently.
- **Discard:** never (it is your defense preparation material).

### 29.6 Results and Analysis Record

- **Purpose:** all numbers and their interpretation, including diagnostics and robustness.
- **Created:** as the first real run finishes.
- **Updated:** with each run, analysis, and robustness check.
- **Contains:** table of all results (including failures and discarded runs), effect sizes with CIs, diagnostics, what each result rules out, and versioned artifact paths.
- **Discard:** never; this is Table 1 of the paper.

### 29.7 Paper Story

- **Purpose:** the single claim and the evidence chain that supports it.
- **Created:** when analysis stabilizes.
- **Updated:** during compression from thesis to paper.
- **Contains:** one-sentence claim | closest work and design difference | claim-supporting figures in order | rebuttals to the three strongest objections | boundary statement.
- **Discard:** never; it is the abstract's skeleton.

### 29.8 Minimal file layout

```text
research/
  map.md
  question_ledger.md
  evidence_ledger.md
  research_log.md
  results_record.md
  paper_story.md
  experiment_specification.md
```

Seven files, each updatable in minutes. That is the whole system. **[L3]**

### 29.9 What *not* to build

- A large citation database with hundreds of entries and no decisions attached.
- Multiple "canonical," "final," or "master" documents restating the same content.
- Templates for phases you have not reached.
- Dashboards and trackers that must be maintained instead of used.

**Evidence from your corpus [L2]:** the cost of over-documentation is visible — the ratio of synthesis documents to executed experiments was extremely high, and the document set had to be re-summarized repeatedly by different tools. The seven-artifact system above would have carried all the information that mattered with roughly an order of magnitude less text.
