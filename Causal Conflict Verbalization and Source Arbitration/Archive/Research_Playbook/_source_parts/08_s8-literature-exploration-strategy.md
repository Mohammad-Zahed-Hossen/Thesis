---

## 8. Literature exploration strategy

### 8.1 Reading is a resource allocation problem

You have a fixed budget of attention. Allocate it by *decision value*, not by paper importance as judged by others. **[L3]**

A practical allocation for a new territory:

| Portion of reading time | Purpose | Depth |
|---|---|---|
| 25% | Orientation: what is this field arguing about? | Abstract + intro + figures |
| 25% | The 3–5 papers that define the phenomenon | Full read of method, results, limitations |
| 20% | Closest-work search (§12) | Method and experiment sections only |
| 15% | Alternative explanations and confound literature | Targeted sections |
| 10% | Benchmark/dataset documentation and code | Data cards, README, item inspection |
| 5% | Frontiers: newest 3–6 months | Abstracts only, until one matters |

### 8.2 When to start reading deeply

Read deeply (full method, results, appendices) only when a paper satisfies at least one of:

- it defines the phenomenon you are studying;
- it contains the experiment closest to yours;
- it supplies your dataset, metric, or method;
- it proposes a mechanism that competes with your explanation;
- it is the *strongest possible objection* to your idea.

Everything else gets a five-minute pass. **[L3]**

### 8.3 When to stop reading — saturation criteria

Stop expanding the literature when all of the following are true:

1. **Coverage:** the last five papers you found introduced no new *experiment design*, no new *alternative explanation*, and no new *metric*.
2. **Closest work:** you can name the closest existing experiment and explain, in two sentences, why yours differs in design rather than vocabulary.
3. **Vocabulary:** you know the 3–5 terms different communities use for your phenomenon.
4. **Boundary:** you can state what the field already knows and what remains unknown without hedging.
5. **Marginal decision value:** further reading no longer changes your experiment plan.

If criteria 1–4 hold but your *design* is still unclear, the blocker is design, not literature. Go to §18, not to the search bar. **[L3]**

### 8.4 Breadth-first, then depth-first — and never the reverse

**Breadth-first (days 1–3).** Find the defining papers and the vocabulary. Read abstracts, intros, and figures. Build the field map (§11). Do not take notes on details you cannot yet use.

**Depth-first (days 4–10).** Choose the 4–8 papers that matter and interrogate them (§10). Extract: their claim, their data, their control, their metric, their limitation, and the exact experiment they did *not* run.

**Why order matters [L2].** In your workspace, several folders contain long, detailed audits produced early, and later folds re-audit the same space with clearer questions. Depth-first reading before the phenomenon was sharp produced detail that could not be used, then had to be re-derived.

### 8.5 Managing the reading queue

Keep one file with three lists only **[L3]**:

```text
TO-READ        (max 10 entries; each with the decision it informs)
READ-RELEVANT  (each with: claim / evidence / control / metric / limitation / what they did not test)
IRRELEVANT     (one line why; never revisit)
```

If the TO-READ list exceeds ten items, stop collecting and start deciding. An unbounded queue is a symptom of avoiding the decision, not of thoroughness.

### 8.6 Search engines, catalogs, and where AI fits

- **Use** arXiv (full text + version history), the venue's official proceedings, Semantic Scholar/Google Scholar for citation chains, and dataset/model cards on Hugging Face for provenance and known limitations.
- **Use citation chains deliberately:** backward (what does this paper build on?) and forward (who challenged or extended it?). Forward citations are where refutations live. **[L1]**
- **AI assistants** are excellent at: summarizing a paper you already have, generating search-term variants, translating between community vocabularies, and listing candidate confounds. They are unreliable at: asserting that a gap exists, judging novelty, and reporting what a paper's experiment actually did when you have not checked it. (§28 covers this in depth.)

### 8.7 A stopping story from your own project **[L2]**

The workspace contains many large synthesis documents and multiple "canonical" restatements. Their volume reflects genuine effort, but the *decision-relevant* content stops growing well before the documents stop being written. The useful pivot happened when the work shifted from producing audits to running a 20-item pilot that falsified a metric. Total new knowledge per hour of effort rose sharply at that moment.

**Rule [L3]:** if two consecutive reading sessions produce no change in your experiment sketch, the reading phase is over for now.
