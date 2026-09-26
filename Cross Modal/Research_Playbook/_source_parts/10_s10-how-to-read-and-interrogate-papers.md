---

## 10. How to read and interrogate papers

### 10.1 Three passes with three different purposes

**Pass 1 — Triage (5 minutes).** Read title, abstract, figures, and the first and last paragraphs of the introduction *and* of the conclusion. Then answer in one line each:

1. What problem does this paper claim to solve?
2. What did they actually measure?
3. Does it threaten my idea? (If yes, go to Pass 2.)
4. Does it supply something I need: data, metric, baseline, method, or vocabulary?

Stop here for most papers. Write a one-line verdict and move on. **[L3]**

**Pass 2 — Method and evidence (20–40 minutes).** Read the method section, the main results tables, and the limitations paragraph. Extract:

| Field | What you are looking for |
|---|---|
| Claim | The narrow, defensible claim (often narrower than the abstract) |
| Population | Model(s), dataset, split, sample size |
| Manipulation | What varied, and what was held constant |
| Control | The comparison that makes the causal claim meaningful |
| Metric | Construct named vs what is operationally counted |
| Main number | Effect size, not just significance |
| Failure interpretation | What the authors say a null result would mean |
| Limitation | Authors' own admitted boundary |
| **Not tested** | The experiment this paper conspicuously avoided |

The "not tested" column is where your questions come from. **[L3]**

**Pass 3 — Deep interrogation (2–4 hours, only for the handful that matter).** Read appendices, prompt templates, decoding settings, and the code if available. Reproduce one headline number, or at least recompute it from their released outputs. Check whether the metric is computed as described. Check whether the sample is balanced. Check whether the training/test split leaks. This is also the pass where you often discover that a claim is *narrower* than the abstract implies — which reshapes your own question. **[L1/L3]**

### 10.2 Where to look for what

| You want | Look here |
|---|---|
| The real claim | Last paragraph of the intro; limitations |
| What actually changed | Method section, "Experimental Setup" |
| Whether the effect is real | Results tables + effect sizes, not figures alone |
| Whether the comparison is fair | Appendices, prompt templates, hyperparameters |
| Whether the data supports it | Dataset card, item inspection, label statistics |
| Whether it reproduces | Code repo, released outputs, version history on arXiv |
| Whether it was challenged | Forward citations, later papers, review discussion |
| What they avoided | The gap between their claim and their strongest control |

### 10.3 Six questions that make a paper yield its limits

1. What is the **control**, exactly?
2. What **else** differs between conditions?
3. Does the **metric** measure the construct named in the title?
4. What happens to the result if the **metric** is changed to a continuous/linear variant? (A lesson from the emergent-abilities reassessment: [arXiv:2304.15004](https://arxiv.org/abs/2304.15004).)
5. What is the **strongest simpler explanation** the paper does not rule out?
6. What would the paper look like if the **effect did not exist** — is any figure or statistic incompatible with that?

Question 6 is a compact falsifiability test. If nothing in the paper is incompatible with "no effect," the paper is descriptive, and you now know exactly what experiment is missing. **[L3]**

### 10.4 Reading with AI assistance — rules that keep you honest

**Safe uses [L3]:**
- Summarize a paper you have already opened, then verify each claim against the PDF.
- Generate query variants and vocabulary synonyms.
- Extract a structured table (claim/data/control/metric/limitation) for a paper you paste in.
- Explain a technical method or statistic you do not know.

**Unsafe uses:**
- Asking "is this gap novel?" and treating the answer as evidence.
- Asking "what did paper X find?" without reading paper X.
- Accepting invented citations. Every reference must be opened before it enters your thesis.
- Letting a summary of a summary become your description of a paper's design.

**Rule [L3]:** AI may compress your reading; it may not replace the act of verification. One fabricated citation in a thesis is far more costly than an extra hour of reading.

### 10.5 When to stop reading a paper

Stop immediately if any is true:

- the paper's question is not your question, and it supplies no data, metric, baseline, or design idea;
- you are reading it only because it appeared in a search list;
- you cannot state its main claim after ten minutes;
- you are reading the same background section for the fourth time;
- you already have its one relevant sentence.

Deep reading is reserved for the papers that can change your experiment. Everything else is five minutes. **[L3]**
