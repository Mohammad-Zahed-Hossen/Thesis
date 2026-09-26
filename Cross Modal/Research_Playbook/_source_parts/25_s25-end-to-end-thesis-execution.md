---

## 25. End-to-end thesis execution

### 25.1 The pipeline, with the purpose of each element

```text
data preparation   → makes the population explicit and reproducible
baseline           → defines "no effect" and the trivial alternative
experiment harness → controls the manipulation, budgets, and logging
logging            → preserves raw evidence so claims can be re-derived
reproducibility    → pins versions, seeds, and configs
analysis           → quantifies the contrast under stated assumptions
visualization      → makes one claim visible per figure
statistical testing→ separates signal from noise, with uncertainty
failure analysis   → explains where and why the design broke
robustness checks  → tests fragility of the conclusion
documentation      → lets a stranger reproduce and audit the work
```

### 25.2 Design upfront vs keep flexible

| Decide before implementation | Decide during/after implementation |
|---|---|
| Item selection and exclusion rules | Figure aesthetics |
| Prompt templates (verbatim) and output format | Additional descriptive statistics |
| Arm structure and token budgets | Exploratory subgroup analyses |
| Primary metric and parsing rules | Secondary visualizations |
| Seeds, dtype, model revision, attention implementation | Narrative structure and emphasis |
| Output schema for logs and checkpoints | Related-work additions |
| Statistical tests and unit of analysis | Future-work branches |
| Directory layout and file naming | — |

### 25.3 A directory layout that prevents chaos

```text
project/
  PROTOCOL.md            frozen design
  ANALYSIS_PLAN.md       pre-registered analyses
  BOUNDARY.md            claims this study does not make
  src/                   one module per responsibility: data, prompts, model, classify, stats
  configs/               one YAML/JSON per experiment revision (v1, v2, v3)
  results/               raw JSONL per run + checkpoint CSV
  analysis/              scripts that read results/ and emit tables/ + reports/
  figures/               generated only, never hand-edited
  notes/                 research log, question ledger, evidence ledger
  drafts/                thesis chapters
```

Your existing project already approximates this (harness, statistical suite, results, LaTeX table output). The missing pieces are `PROTOCOL.md`, `ANALYSIS_PLAN.md`, and a `configs/` record per version — the three artifacts that make a re-run reproducible months later. **[L2/L3]**

### 25.4 The reproducibility minimum

- One command reproduces the main table from raw outputs.
- Raw outputs are archived and never overwritten (new version = new filename).
- Model revision, library versions, dtype, and attention implementation are recorded.
- Determinism: seeds set; note where nondeterminism remains (GPU kernels, sampling).
- Every number in the thesis traces to a script and a file.

**[L1]** This is the substance of community reproducibility expectations ([arXiv:2003.12206](https://arxiv.org/abs/2003.12206)) and of variance-reporting guidance in ML ([arXiv:1709.06560](https://arxiv.org/abs/1709.06560)). It is also the cheapest defense against the "did you really run this?" question.

### 25.5 Analysis and visualization discipline

- **One figure, one claim.** If a figure needs two paragraphs to explain, split it.
- **Show distributions, not only means** — per-arm token counts, truncation rates, per-class behavior.
- **Annotate uncertainty** on every reported effect.
- **Keep a "figure provenance" line** in the caption: script, run ID, and date.
- **Plot the diagnostics**, not only the headline result: parse rate and truncation by arm belong in the thesis, because they establish interpretability.

### 25.6 Documentation as scientific work

Write, as you go, not at the end:

| Document | Written when | Contents |
|---|---|---|
| Research Log | Daily | decisions, dead ends, bugs, surprises |
| Question Ledger | At each candidate question | status, kill reason, reopen condition |
| Evidence Ledger | At each finding | claim, source, script, file, date |
| `PROTOCOL.md` | At freeze | everything needed to re-run |
| Results Record | During analysis | numbers + interpretation + limitations |

### 25.7 Writing the thesis while running experiments

Draft sections in the order in which they become stable, not in the order they appear in the document:

1. **Method** — drafted at freeze, revised as the harness changes.
2. **Results** — drafted incrementally as runs complete, including diagnostics.
3. **Related work** — written continuously; it is the only chapter that never freezes.
4. **Discussion/limitations** — written with the results, while the confounds are fresh in mind.
5. **Introduction and abstract** — written last, when the contribution is actually known.

This ordering is why the common "write it in chapter order" plan fails: chapters 1 and 2 depend on what chapters 4 and 5 turn out to say. Your current plan (Chapters 3–4 first, then 1–2, then 5) is consistent with this principle. **[L2]**
