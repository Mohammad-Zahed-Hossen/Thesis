---

## 26. From thesis to paper

### 26.1 Identify the single central claim

A paper is not a compressed thesis. It is **one claim with the evidence needed to believe it.** Write it as:

> "Under [conditions], [manipulation] [changes/does not change] [measure] relative to [control], which indicates [interpretation]."

Test: if your paper's title needs the word "and," you may have two papers. **[L3]**

### 26.2 What belongs in the paper

| Keep | Cut |
|---|---|
| The frozen question and why it was open | Exploratory branches that did not resolve |
| Design with controls and budgets | Implementation micro-details without inferential role |
| Primary result with effect size and CI | Every secondary statistic |
| Diagnostics that establish interpretability (parse/truncation) | Full hyperparameter tables (appendix instead) |
| Ablations answering the strongest objection | All ablations performed |
| Honest limitations and bounded claims | Speculative mechanism claims without evidence |
| One or two figures carrying the argument | Figures that duplicate tables |

### 26.3 Structure the evidence, not the chronology

Do not narrate the order in which you discovered things. Structure for the reader's inference:

```text
1. Phenomenon and why it is not yet explained
2. The closest work and the specific design difference
3. Hypotheses with opposite predictions
4. Design: manipulation, control, measurement, population
5. Primary result (with the diagnostic that makes it interpretable)
6. Controls/ablations that rule out the strongest rival explanation
7. Boundary conditions and limitations
8. What changes for the field
```

Step 6 is what distinguishes a paper from a report. **[L3]**

### 26.4 Framing the contribution honestly

Two different kinds of contribution; label the right one **[L3]**:

- **Novelty** — nobody has run this experiment / defined this construct this way. Must be justified by a design comparison (§12.4), not by vocabulary.
- **Empirical value** — the experiment is not novel in kind but resolves an ambiguity that matters: a matched control that was missing, a metric validity check, a boundary condition, a prompt-framing effect that reframes an earlier claim.

Your project's strongest defensible framing is primarily **empirical**, with a **measurement** element: a matched-control test of whether conflict verbalization changes which problem the model's reasoning engages, plus abstention as a distinguished outcome and a re-framing of "visual capture" as prompt-dependent. That framing is honest, verifiable from your artifacts, and still interesting. **[L2]**

### 26.5 Handling limitations without destroying the paper

- Put limitations in their own short section, in plain language.
- For each limitation, say whether it **bounds the claim** or **threatens the design**. Bounds are normal; threats need a mitigation or a stated decision.
- Never write "future work could explore X" when X would falsify your claim — say what would falsify it.
- Do not hide the confound; state it and quantify what it could account for.

### 26.6 Avoiding overclaiming: the phrase audit

Before submission, search your draft for: *proves, demonstrates causally, shows that models cannot, generalizes to, robust across models, state-of-the-art, novel architecture, we solve*.

For each hit, ask: does my evidence license this verb, and does the control support it? Replace with the strength your design supports: *provides evidence that, is consistent with, under our conditions, in this model family*. **[L1/L3]**

### 26.7 Choosing a venue for a first paper

| Option | Best when | Cost |
|---|---|---|
| Workshop | Result is narrow but clean; you want feedback | Low prestige, fast, useful |
| Findings/short paper track | Single clean claim with one strong control | Moderate |
| Main conference | Novel construct plus multiple controls plus generalization | High; expect multiple revisions |
| Journal | Extended empirical study with robustness | Slow |

For a first paper, a **workshop or short-paper submission of the single cleanest claim** is usually the highest expected value: it converts your thesis into a citable artifact, generates reviewer feedback, and does not require a second project's worth of generalization. **[L3]**

### 26.8 Revision as re-designed evidence

Reviewers rarely ask for prose changes; they ask for evidence. Keep a table:

| Reviewer comment | What evidence would answer it | Feasible now? | Planned |
|---|---|---|---|
| "The control is not matched" | Per-item token distribution table | Yes (already logged) | Add table |
| "Metric conflates X and Y" | Manual audit of 50 sampled outputs | Yes (few hours) | Add appendix |
| "Only one model" | Second model family | Maybe (GPU budget) | State as limitation |
| "Effect could be framing" | Additional neutral wording variant | Maybe | Add as ablation |

This table turns a rejection into a revision plan. **[L3]**
