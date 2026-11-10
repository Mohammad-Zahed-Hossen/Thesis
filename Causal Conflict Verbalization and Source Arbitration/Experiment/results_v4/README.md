# results_v4

v4 runs on Colab, plus local analysis. Every number below is **dev data, for tuning only**, not a confirmatory finding. It covers 200 items on `Qwen/Qwen2.5-VL-3B-Instruct`.

Numbers come from `analysis_dev2/analysis_v4.md`. Regenerate it with:

```bash
python analyze_v4.py --runs results_v4/dev2_qwen25.jsonl results_v4/dev2_transplant_qwen25.jsonl results_v4/dev2_qwen25_rp105.jsonl --gates --output_dir results_v4/analysis_dev2
```

## Directory Structure

```
results_v4/
├── smoke.jsonl / .manifest.json              Initial 8-item smoke test (penalty 1.0, verified)
├── dev2_qwen25.jsonl / .manifest.json        200 items, 15 arms (penalty 1.0, CoT working enabled, 3000 rows complete)
├── dev2_qwen25_rp105.jsonl / .manifest.json  200 items, 3 v3 arms (penalty 1.05, 600 rows complete)
├── dev2_transplant_qwen25.jsonl / .manifest  200 items, 14 cells (transplant run, 2800 rows complete)
├── analysis_dev2/                            Generated report and long-format data for dev2 runs
├── analysis_dev/                             Historical report on initial dev1 run
└── superseded/
    └── dev1/                                 Initial dev1 runs (16 missing rows, old transplant bugs)
```

## Status & Dev Observations (2026-11-07 dev2 run)

### 1. Data Integrity & Completeness
- `dev2_qwen25.jsonl`: **3,000 / 3,000 rows** (all 200 items across all 15 arms present, no missing rows).
- `dev2_qwen25_rp105.jsonl`: **600 / 600 rows** (all 200 items across 3 arms present).
- `dev2_transplant_qwen25.jsonl`: **2,800 / 2,800 rows** (all 200 items across 14 cells present).

### 2. Transplant Fidelity (Bugs Resolved!)
- **`z0_m0 vs desc_image_first`**: **95.3%** fidelity (102 of 107 solvable items reproduced exact same answer).
- **`z1_m1 vs conflict_full`**: **96.5%** fidelity (193 of 200 items reproduced exact same answer).
*(Fidelity in dev1 was broken at ~33% due to mid-sentence truncation and forced blank lines. Both were fixed, restoring fidelity to >95%.)*

### 3. Whole-Verbalization Transplant Contrast (dev observation, not a finding)
Holding the instruction $z$ fixed, prefilling the conflict verbalization $m_1$ in place of the neutral description $m_0$ is followed by a large shift toward the text problem on these 200 dev items:
- Under neutral instruction $z_0$:
  - `answer:image` drops from 47.5% to 26.0% (**-21.5 pp**, $p = 4.09 \times 10^{-6}$)
  - `answer:text` increases from 12.0% to 47.5% (**+35.5 pp**, $p = 2.41 \times 10^{-18}$)
- Under conflict instruction $z_1$:
  - `answer:image` drops from 35.0% to 19.5% (**-15.5 pp**, $p = 4.24 \times 10^{-4}$)
  - `answer:text` increases from 30.5% to 60.0% (**+29.5 pp**, $p = 1.66 \times 10^{-13}$)

**This does not confirm the thesis hypothesis.** An earlier version of this README said it did; that was an overclaim, corrected on 2026-11-11.
- $m_0$ and $m_1$ are whole verbalizations. They differ in content, length and style as well as in the verdict, so the shift cannot be attributed to the verdict.
- The image was always first; evidence order was not varied.
- The p-values are from an exploratory dev run with no pre-registered contrast.

The contrast that isolates the verdict in v4 is the authored pair `rel_image` vs. `rel_text`. On all 200 items it moves image answers by +21.0 pp under $z_0$ and +0.5 pp under $z_1$; on the 110 competency-passing items, +20.9 pp and −1.8 pp. Same-meaning prefills (`eq_a` vs. `eq_b`) change the extracted answer on 39.0% ($z_0$) and 33.0% ($z_1$) of the 200 items, so the wording floor is high. The $z_1$ null fits instruction dominance as well as unfaithfulness; dev data cannot separate them. The v5 design (minimal-edit flips, both orders, binding arm, ceilings) exists to test this properly.

### 4. Solvability Ceilings (Base Arms)
When given only one modality:
- `base_image` (image alone): **72.8%** solved
- `base_text` (text alone): **75.4%** solved
- McNemar test between image-only and text-only: $p = 0.5114$ (no intrinsic modality difficulty disparity).

### 5. Remaining Gate Observations
- `max_new_tokens = 400` had token cap hits between 5% and 13% for long chain-of-thought solutions in `base_text`, `direct`, and `congruent_direct`. For the confirmatory phase, raising `--max_new_tokens` to 512 or 600 will eliminate token truncation.
- `desc_image_first` and `placebo_v3`: The model sometimes provides the 2-sentence description and terminates without calculating.
