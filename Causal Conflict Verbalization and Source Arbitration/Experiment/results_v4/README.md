# results_v4

v4 runs on Colab, plus the local analysis. Every number below is **dev data, for tuning only**, not a finding. It covers 200 items and one model.

Numbers come from `analysis_dev/analysis_v4.md` unless marked as a one-off. Regenerate it with:

```bash
python analyze_v4.py --runs results_v4/dev_qwen25.jsonl results_v4/dev_qwen25_rp105.jsonl --gates --output_dir results_v4/analysis_dev
```

## Files

| File | Contents | Status |
|---|---|---|
| `smoke.jsonl` | 8 items, 15 arms, penalty 1.0 | Complete; all 120 outputs match the dev run exactly |
| `dev_qwen25.jsonl` | 200 items, 15 arms, penalty 1.0 | **16 rows missing**, gates failing |
| `dev_qwen25_rp105.jsonl` | 200 items, 3 v3 arms, penalty 1.05 | Complete |
| `analysis_dev/` | Generated report on the two dev runs | Current |
| `superseded/dev_transplant_qwen25.jsonl` | 200 items, 14 cells | **Invalid: prefill bug; don't analyze** |

Each `.manifest.json` records settings, versions and script hashes. The runs used Tesla T4, torch 2.11.0, transformers 5.22.0, about 7.5 GB peak VRAM, and the pinned model and dataset commits.

## Integrity checks (2026-11-07)

Run as one-off checks against these files:

- No duplicate rows or cut-off lines, and all items are in the dev split.
- Prompt hashes and gold answers match the current code on every row.
- Script hashes in all four manifests match the code as it was before the 2026-11-07 fixes.
- Identical output on a repeat run: 120 of 120 smoke rows, so generation is deterministic here.

## Open problems

### 1. Missing rows
`dev_qwen25.jsonl` has no `direct_v3` row for items 0032 to 0047, which is two batches. The file jumps from 0031 to 0048 with no error. The cause is [Unknown]. To fill them, rerun the same command with the same tag.

### 2. Transplant run is invalid
Fidelity was 32.5% and 35.5%, when own-verbalization prefills should reproduce their own answers. There were two causes, both fixed on 2026-11-07:
- `split_verbalization` matched "to solve" mid-sentence, cutting 106 of 200 conflict donors and 44 of 200 neutral donors in the middle of a sentence.
- `load_donors` forced a blank line after every donor. In a one-off check, answers reproduced in 78 of 84 donors that really had a blank line, and 58 of 316 others.

Rerun under a new tag (see the runbook). Its contrasts shouldn't be used, even as hints.

### 3. Gate failures

| Arm | Rule | Value | Likely cause |
|---|---|---|---|
| `direct_v3` | Rows complete | 16 missing | Problem 1 |
| `direct_v3` | Token cap under 5% | 8.7% | Long working; a few loops |
| `base_text` | Token cap under 5% | 8.0% | Long working |
| `desc_image_first` | Answer or refusal at least 90% | 72.5% | Stops after describing (38.5% have no solving) |
| `placebo_v3` | Answer or refusal at least 90% | 81.0% | Stops after describing (35.0% have no solving) |

### 4. `FORMAT` suppresses working (a decision for the researcher)
"Write #### followed by only the final number" makes many outputs answer-only, at 8 tokens or fewer: `direct` 59.5%, `congruent_direct` 50.0%, `base_image` 33.5%. So `direct` isn't a usable baseline. In a one-off check, `base_image` was right on 22.4% of answer-only outputs and 70.7% of the others. Compare `direct_v3`, which shows its working at 1.1% answer-only. A wording that asks for working first should fix this, and needs a new dev run.

## What dev suggests (to test, not to cite)

### Repetition penalty strongly changes v3's arms
Same arm and items, penalty 1.0 vs 1.05:

| Arm | Exact image | Exact text | v3 abstain label | Stops unsolved |
|---|---:|---:|---:|---:|
| `placebo_v3` | 14.5% → **52.0%** | 2.5% → 3.5% | 0.0% → 0.5% | 35.0% → 7.5% |
| `conflict_v3` | 4.5% → **18.0%** | 41.5% → 48.5% | 0.5% → **12.5%** | 0.0% → 0.0% |
| `direct_v3` (n = 184) | 3.8% → 8.2% | 67.4% → 60.9% | 0.0% → 0.0% | 2.7% → 1.6% |

- **v3 ran with the penalty on.** [Inferred] In a one-off check, the rerun at 1.05 shared its first 150 characters with stored v3 on 198, 191 and 187 of 200 items in the three arms.
- **v3's "abstention" is largely tied to the penalty.** On these items, stored v3 has 24 labels, the rerun at 1.05 has 25, and penalty 1.0 has 1.
- **The Arm 2 to Arm 3 contrast survives on text.** It's +39.0 pp at penalty 1.0 and +45.0 pp at 1.05. On image it shrinks, from a 34.0 pp gap at 1.05 to 10.0 pp at 1.0.

Neither setting is "the right one": 1.05 is the model's shipped default and 1.0 is no penalty. Treat the penalty as a factor and pre-register how to report it.

### Baseline leans to the text
With an inert filler sentence, answers follow the typed problem: image 1.0%, text 63.5%. `direct_v3` is similar at 3.8% and 67.4%. Relative to filler, every arm that mentions the image raises image answers and lowers text answers, including `conflict_full` (image 10.5%, text 32.0%). This fits the audit's point that v3's "visual capture" is relative to a placebo that isn't inert.

### Conflict detection discriminates
| Stimulus | Arm | Says conflict | Says agree |
|---|---|---:|---:|
| Conflict | `conflict_full` | 198 of 200 | 0 |
| Conflict | `detect_only` | 196 of 200 | 2 |
| Congruent | `congruent_conflict` | 5 of 200 | 194 |
| Congruent | `congruent_detect` | 10 of 200 | 190 |

Labels come from an unvalidated regex.

### Stated reliability hardly varies
In `conflict_full`, 102 outputs name the text as more reliable and 3 name the image, and 95 don't say. Observational use of this as a mediator won't work, which is why the transplant authors fixed statements.

### Images are harder than text
The same problem was solved at 55.9% from the image alone and 77.4% from the text alone (195 problems). Part of this is answer-only output. Compare source rates against these ceilings, not against 100%. Legibility at `max_pixels` isn't settled, though the one-off 70.7% vs 77.8% gap among outputs with working suggests it isn't severe.

### Real refusals appear only with detection alone
`detect_only` has 14.0% refusals. Sampled ones say "The problem cannot be solved", with no answer. Other conflict arms are at or near 0%.
