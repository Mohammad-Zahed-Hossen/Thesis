---

## 9. How to search like a researcher

### 9.1 Search is a sequence of questions, not one query

Suppose you notice:

> "A multimodal model appears to lose image-grounded content as its reasoning chain gets longer."

Below is the actual search sequence a researcher runs, in order, with the decision each search informs.

| # | Search intent | Example query strings | Decision it informs |
|---|---|---|---|
| 1 | Phenomenon | `"long reasoning" multimodal hallucination`, `reasoning length visual grounding degradation`, `longer chains less visual` | Does the phenomenon exist in the literature at all? |
| 2 | Explanation | append `mechanism`, `attention analysis`, `why`, plus the paper's §Discussion | What cause do authors propose? |
| 3 | Alternative explanation | `modality prior`, `language prior`, `distribution shift`, `prompt length`, `decoding` | What else could produce it? |
| 4 | Confound | `test-time compute control`, `matched compute`, `token budget`, `length-matched` | Has anyone ruled out the boring cause? |
| 5 | Replication / challenge | forward citations of the phenomenon paper; `fails to replicate`, `does not hold`, `reassessment`, `critique` | Has anyone challenged or reinterpreted it? |
| 6 | Boundary condition | `resolution`, `image degradation`, `task type`, `model scale`, `out-of-domain` | Where does the effect stop? |
| 7 | Intervention | `intervention`, `causal`, `prefill`, `activation patching`, `ablation of reasoning` | What manipulations already exist? |
| 8 | Benchmark | `benchmark`, `diagnostic`, `evaluation suite`, plus the metric name | Is there a standard measure, and what does it actually score? |
| 9 | Dataset | `dataset`, `corpus`, plus Hugging Face dataset search | Is there reusable data with known provenance? |
| 10 | Recent work | arXiv listings for the last 3–6 months; author pages; venue accepted-paper lists | Is the space moving under me right now? |

Searches 1–2 tell you what the field believes. Searches 3–5 tell you what the field has *not* ruled out. Searches 6–7 tell you what is testable. Searches 8–9 tell you what is feasible. Search 10 tells you whether to hurry. **[L3]**

### 9.2 Search by design, not by topic wording

Keyword search fails precisely where novelty matters, because your idea's *design* may exist under different words. Search on each design dimension separately **[L2/L3]**:

| Dimension | What to search | Why |
|---|---|---|
| Phenomenon | Behavior descriptions and their synonyms | Finds the field's own name for it |
| Intervention | The manipulation type (prompting, prefill, activation, perturbation) | Finds the closest *causal* design |
| Measurement | The metric or construct (faithfulness, reliance, arbitration, abstention) | Finds the closest *analysis* |
| Dataset | Benchmark or corpus name, plus derivative works | Finds papers using identical items |
| Model | Model family name, e.g. a specific VLM generation | Finds replication and model-specific studies |
| Protocol | "length-matched", "placebo", "control condition", "same items" | Finds the closest *control design* |
| Evaluation | Annotation scheme, inter-annotator agreement, judge calibration | Finds measurement-validity work |

**Worked example.** Searching "conflict verbalization" may return little. Searching the *design* — "matched neutral control + source-attribution + multimodal contradiction" — returns faithfulness studies, explanation-evaluation work, and benchmark papers. One of those may already contain your experiment. **[L3]**

### 9.3 Techniques that find what keyword search misses

1. **Backward citation chain** from the phenomenon paper: which earlier result is being relied upon? Check whether that result was ever controlled. **[L1]**
2. **Forward citation chain:** who cited it, and did they disagree? Use "cited by" on Semantic Scholar/Google Scholar, then filter by title patterns like *revisiting*, *re-examining*, *limitations*, *critique*, *replication*. **[L1]**
3. **Author-and-lab tracking:** the same group often publishes the follow-up. If you are building on their limitation, you are racing them.
4. **Code and README search:** implementation details (prompt templates, decoding settings, preprocessing) are usually only in the repo or appendix, not the abstract. Differences in these often explain contradictory results. **[L1]**
5. **Dataset and model card search:** provenance, licensing, filter criteria, and known biases live there. **[L1: Datasheets for Datasets, arXiv:1803.09010]**
6. **Venue accepted lists:** scan titles for a conference's most recent edition; preprint search alone misses camera-ready changes.
7. **Negative-result search:** search for the null framing ("does not improve", "no significant difference", "under matched compute") to find the papers that quietly falsify popular claims.
8. **Metrics-literature search:** look for papers about *evaluation validity* in your area — these are goldmines for defensible, small-scope contributions.

### 9.4 Practical search hygiene

- Record **every** query that mattered and what it returned, in the Research Log. Six weeks later you will not remember whether you already checked a design.
- Keep a **one-line verdict** per source: `(claim) / (evidence) / (control?) / (what they did not test)`.
- Treat "not found" as weak evidence. Absence of a hit is often a search-vocabulary failure, not a genuine gap.
- Prefer primary text: open the paper's method and results. An AI summary of a paper is not evidence about that paper. **[L1/L3]**
