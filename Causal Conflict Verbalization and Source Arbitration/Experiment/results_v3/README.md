# results_v3

Stored v3 pilot: Qwen2.5-VL-3B, N = 1,619, five conditions, run on a T4 in September 2026. **Treat it as exploratory.** It wasn't pre-registered, and the same data shaped the metric.

## Files

| File | Use |
|---|---|
| `full_experiment_results v3.0.json` | **Primary record:** every output and label. Read-only |
| `experiment_checkpoint v3.0.csv` | Same run, per arm. `item_idx` is per batch, so join on `id` |
| `reanalysis_v3/` | **Current tables**, re-scored by `score_v4.py` |
| `stats_v3_paired/` | **Current paired statistics** on the stored labels |
| `statistical_report v3.0.md` | Historical. Don't cite: verdict wording is hard-coded |
| `thesis_contingency_table v3.0.tex` | Historical. Don't cite: same problem |

Code: `../archive/harness_v3/production_experiment_harness_v3.py`.

To regenerate, from `Experiment/`:

```bash
python reanalyze_v3.py --check --output_dir results_v3/reanalysis_v3
```

```bash
python statistical_analysis.py --results_file "results_v3/full_experiment_results v3.0.json" --output_dir results_v3/stats_v3_paired
```

## What holds up

- **Instruction contrast:** visual label 89.5% to 25.8%; problem-clustered 95% interval on the shift is 59.4 to 68.0 pp.
- **Exact-answer cross-over,** on 1,600 distinct-answer items: Arm 2 is 35.7% image and 4.2% text; Arm 3 is 11.8% image and 36.1% text. Chance is about 1.3%.

## What doesn't

| Claim | Problem |
|---|---|
| "Reverses default visual capture" | Arm 1 is 13.8% visual. Arm 2 isn't inert, and Arm 3 sits above Arm 1 |
| "13.65% refusals" | `score_v4.py` finds 38 (2.3%). Most say "cannot determine if they agree", then solve. Unvalidated |
| "Zero truncation" | 98.1%, 37.6% and 44.2% of Arms 1 to 3 hit the cap |
| "Deterministic #### parsing" | Under v3's parser, exact matches via a numeric `####` were 1, 0 and 0 in Arms 1 to 3; the last-number fallback did the work |
| "Verbalization causes the shift" | Only the instruction was randomized |
| Arm 4 as a causal probe | It confounds rationale with source, and image match is near chance |

The dev penalty check adds another caveat: these arms ran with `repetition_penalty` 1.05, which appears to raise image answers and v3 abstention labels. See `../results_v4/README.md`.

## Known v3 defects

These are kept for the record and fixed in v4: capitalized stopwords counted as entities, names mangled by `rstrip("'s")`, a `+1` margin that did nothing, ChartQA mode never showing the report, and 19 equal-answer pairs included.
