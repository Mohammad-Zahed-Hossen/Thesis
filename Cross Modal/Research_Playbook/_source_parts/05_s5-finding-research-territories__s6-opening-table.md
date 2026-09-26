---

## 6. Finding phenomena and failures

A phenomenon is a repeatable, describable behavior or outcome — not a topic, a method, or an opinion about a paper.

| Source of a question | How to recognize it | Cheapest check | Question it yields |
|---|---|---|---|
| Unexplained empirical phenomenon | Reported, unexplained | One ablation table | What causes this? |
| Surprising failure | Fails where it "should" succeed | Run 10 hand-picked items | When does it fail? |
| Contradiction between papers | Opposite directions reported | Compare dataset, prompt, metric | What differs between setups? |
| Obvious-but-untested alternative | Reviewers say "couldn't it be…?" | Design the matched control | Does it survive the alternative? |
| Limitation in an influential paper | Stated in §Limitations | Read that paragraph | Does the claim hold outside it? |
| Missing control | Intervention has no placebo | List nuisance variables | Is the cause the intended variable? |
| Boundary condition | Works in one setting only | Change one factor | Where exactly does it break? |
| Measurement problem | Metric proxies the construct | Re-read its definition | Does the metric measure the claim? |
| Benchmark weakness | Templated, leaky, or adjacent task | Read 20 items | What is actually measured? |
| Replication divergence | Your rerun disagrees | Compare published config | Is the effect setup-dependent? |
| Toy-only method | No realistic evaluation | Add realistic perturbation | Does it survive realism? |
| Unclear mechanism | Behavior real, cause unknown | Ask what distinguishes causes | Which mechanism explains it? |
| Untested assumption | Universally assumed | Pick cheapest test | Does it hold? |
| Engineering bottleneck | A fix changes results oddly | Ablate the fix | Is the result an artifact? |

Three of these are the highest-yield sources for a short thesis.

### 6.1 Missing or mismatched control

**Recognition.** Read the intervention and ask "compared to what?" If the answer is "not doing it," the comparison is confounded with length, format, token budget, instruction burden, and layout.

**Cheapest check.** Count tokens per arm on 20 items. If arms differ by more than roughly 20%, the control is unmatched — unless you can argue the difference is irrelevant, in which case it is also irrelevant to the effect you claim.

**Failure mode to avoid.** A control matched in tokens but not in *content*, *difficulty*, or *instruction type*, or matched on average while diverging per item. Prefer per-item matching. **[L3]**

### 6.2 A metric that is a proxy

**Recognition.** Ask of any metric: what construct is named, what does it operationally count, and can the first be true while the second misleads?

**Cheapest check.** Manually inspect 20 outputs beside the metric value. Disagreements reveal the gap immediately.

**Worked instance [L2].** In your pre-freeze pilot, "which source the model followed" was measured by exact match to one of two precomputed answers. Inspecting 20 items showed the model was **solving** problems rather than **selecting** answers; 85% of direct-arm outputs matched neither answer. The remedy — classify *which problem the reasoning engages with* from entity evidence, and add abstention as an explicit outcome — is the general pattern: **classify the behavior, not the answer key** **[L2/L3]**.

**What it yields.** A measurement-validity contribution: "the common metric conflates X and Y; we propose and validate a measure that separates them." For an undergraduate thesis this is often more defensible than a new method.

### 6.3 Contradiction between papers, or between a paper and your rerun

**Recognition.** Opposite directions for the same effect, or a rerun that disagrees.

**Cheapest check.** Build one column per difference: model revision, prompt template, decoding parameters, token budget, preprocessing resolution, split, metric definition, seeds. One difference usually explains the discrepancy.

**What it yields.** A boundary condition ("holds only up to resolution R") or a correction ("the gain disappears under matched decoding").

### 6.4 Low-yield sources (use with care)

These can produce well-written theses with little scientific content. Do not build on them unless they expose a real measurement or causal question **[L3]**:

- "Apply method M to dataset D" — a substitution, not a question.
- "Improve accuracy of X" — an objective, not a phenomenon.
- "Build a system that…" — engineering, unless the system exists to answer a question.
- "No paper uses my exact phrase" — almost always a terminology gap.
- "Combine two papers' methods" — a recipe, not a result, unless the combination is theoretically forced.
