# v5 Human Coding Codebook

## Part 1 — Donor Verbalization Coding (`coder_*_verdicts.csv`)
Fill `coder_stated_source` (and optional `coder_notes`) using ONLY the text shown:

- For **Math** (`regime == math`):
  - `image`: clearly states the image / photo / problem in the image is more reliable / trustworthy / accurate.
  - `text`: clearly states the text / written text / problem in the text is more reliable / trustworthy / accurate.
- For **ChartQA** (`regime == chartqa`):
  - `chart`: clearly states the chart / graph / plot / figure / image is more reliable.
  - `report`: clearly states the report / text / summary / written text is more reliable.
- For **either regime**:
  - `neither`: refuses to choose, says both are equally reliable, or discusses something else without picking one source.
  - `both`: explicitly claims both sources are reliable without preferring one, OR states contradictory reliability preferences.
  - `unclear`: truncated, garbled, or too ambiguous to assign one clear preference.

Do NOT look at the final math/chart answer when judging `coder_stated_source`; judge only the reliability verbalization.

## Part 2 — Flipped Clause Coding (`coder_*_flips.csv`)
Fill both binary columns with `1` (yes) or `0` (no):

1. `coder_grammatical_coherent`: Is `flipped_verbalization` grammatical and internally coherent (no half-swapped contradictory phrases like "the text is more reliable than the text")?
2. `coder_names_intended_source`: Does `flipped_verbalization` unambiguously state that `intended_flip_source` is the more reliable source?
