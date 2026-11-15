# v5 Double Human Coding Instructions (Utsha & Rafiul)

**Project:** *Does the Verdict Decide? Testing Whether Stated Source Reliability Steers Vision-Language Models under Image–Text Conflict*
**Coders:**

- **Coder A:** Utsha → edits `coder_A_verdicts.csv` and `coder_A_flips.csv`
- **Coder B:** Rafiul → edits `coder_B_verdicts.csv` and `coder_B_flips.csv`

**Authoritative Label Definitions:** [CODEBOOK_v5.md](CODEBOOK_v5.md)

---

## 1. Why This Work Matters (Read This Before Coding)

In our thesis experiments, a Vision-Language Model (VLM) is given **two conflicting sources at once**:

1. In **Math (`regime == math`)**: an **image** of one word problem and a **typed text** of a different word problem.
2. In **ChartQA (`regime == chartqa`)**: a **chart** image and a written **report** that disagree on a fact/number.

Before answering, the model writes a short **reliability verdict** stating which source it trusts more (e.g., *"I consider the typed text more reliable..."*). Then our Python pipeline does two automated things:

1. **Parser (`score_v5.py`):** automatically classifies which source the model claimed was more reliable.
2. **Flipper (`transplant_v5.py`):** swaps the source nouns in that sentence so the verdict now claims the *opposite* source is more reliable, so we can test whether changing the stated verdict changes the model's final answer.

**Your job is a mandatory scientific validation gate before we can freeze our experiment:**

- Your independent human labels measure **whether our automated parser is accurate** and **whether our flipped sentences are clean and grammatical**.
- We must report **Cohen's $\kappa$** (inter-coder agreement between Utsha and Rafiul) in the thesis and pre-registration (target: **$\kappa \ge 0.80$**).
- If either coder rushes, guesses carelessly, or uses slightly different label rules, agreement drops below $\kappa = 0.80$ and **both coders will have to re-code the sheets**. Taking ~60–90 minutes carefully once saves having to redo it.

---

## 2. Five Strict Rules (Non-Negotiable)

1. **NEVER open the held-out key files:** Do **not** open `KEY_verdicts_do_not_open.csv` or `KEY_flips_do_not_open.csv`. Those contain the automated parser's predictions; seeing them invalidates blind human validation.
2. **Code strictly independently:** Utsha and Rafiul must **not** discuss, compare, or message each other about any row's label until both sets of CSVs are submitted to Zahed.
3. **Judge ONLY from the text shown:**
   - Do **not** use the `order` column (`image_first` / `text_first`) to guess vague phrases like `"the first problem"`.
   - Do **not** look at how the model solves the math problem or what final answer it gives after the verdict. Judge **only** the reliability statement.
4. **Use the exact CSV workflow (Multiline Warning!):**
   - `full_text` contains **multi-line paragraphs inside quoted CSV cells**. Double-clicking in plain Windows Microsoft Excel and pressing `Ctrl+S` often breaks line wraps or encoding.
   - **Recommended tool:** Upload your assigned CSV to **Google Sheets** (`File -> Import -> Upload`, UTF-8, comma-delimited) or open in **LibreOffice Calc** (UTF-8, separator = Comma, text delimiter = `"`). When done, export/save as standard **UTF-8 `.csv`** (`File -> Download -> Comma-separated values (.csv)` in Google Sheets).
   - **NEVER** sort rows, delete rows, add columns, or edit `sample_id` (`V0001`–`V0200`, `F0001`–`F0150`) or any pre-filled column. Only fill the blank `coder_*` columns on the right.
5. **Split into 2–3 short sittings to avoid fatigue:** Code ~100 rows at a time, take a 10-minute break, then finish the rest. Almost all coding errors happen from rushing the last 50 rows.

---

## 3. File Assignments & Workload


| Person     | Role    | Files to Edit & Return                       |          Rows |   Est. Time |
| ------------ | --------- | ---------------------------------------------- | --------------: | ------------: |
| **Utsha**  | Coder A | `coder_A_verdicts.csv` + `coder_A_flips.csv` | `200` + `150` | ~60–90 min |
| **Rafiul** | Coder B | `coder_B_verdicts.csv` + `coder_B_flips.csv` | `200` + `150` | ~60–90 min |

All 4 coder files currently have `0` filled rows. When finished, return **only** your two completed `.csv` files with the exact same filenames.

---

## 4. Part 1 — Donor Verbalization Coding (`coder_*_verdicts.csv`, 200 Rows)

### Columns in this file

- **Read-only context:** `sample_id` (`V0001`–`V0200`), `item_id`, `model_id`, `regime` (`math` or `chartqa`), `family`, `order`, `verbalization_text`, `full_text`
- **Columns YOU fill:**
  - `coder_stated_source` (**required for all 200 rows**)
  - `coder_notes` (*optional* — note anything weird/borderline)

### Exact Allowed Values for `coder_stated_source`

Type **exact lowercase strings** with no extra spaces, typos, or synonyms:


| `regime`  | Allowed Label | Meaning                                                                                                                                                                                                                                                                                                   |
| ----------- | --------------- | ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `math`    | `image`       | Clearly states the **image / photo / problem in the image** is more reliable, trustworthy, or accurate.                                                                                                                                                                                                   |
| `math`    | `text`        | Clearly states the **typed text / text / written problem** is more reliable, trustworthy, or accurate.                                                                                                                                                                                                    |
| `chartqa` | `chart`       | Clearly states the **chart / graph / plot / figure / image** is more reliable, trustworthy, or accurate.                                                                                                                                                                                                  |
| `chartqa` | `report`      | Clearly states the **report / text / summary / written text** is more reliable, trustworthy, or accurate.                                                                                                                                                                                                 |
| *either*  | `neither`     | Complete text that **refuses to choose**, says **both are equally reliable**, solves one problem **without stating which is more reliable**, or discusses something else without picking one source's reliability.                                                                                        |
| *either*  | `both`        | Explicitly claims **both sources are reliable** without preferring one (e.g., *"Both the image and text are reliable"*), **OR** states **contradictory** preferences in the same verbalization (e.g., first says text is more reliable, then says image is more reliable).                                |
| *either*  | `unclear`     | **Truncated/aborted** fragment (e.g., just `"Statista 2021"` or `"Source: Statista 2021"`), garbled text, or **ambiguous reference** where the text alone does not identify which modality is meant (e.g., `"the first problem is more reliable"` without saying whether `"first"` is the image or text). |

> **Warning:** Watch out for `regime`! Never write `chart`/`report` on a `math` row, and never write `image`/`text` on a `chartqa` row. Check the `regime` column every time.

### Step-by-Step Decision Rule for Each Verdict Row

1. Check `regime` (`math` vs. `chartqa`).
2. Read **`verbalization_text`** first. If `verbalization_text` looks cut off mid-sentence or unclear, check the opening sentences of **`full_text`** (ignoring any math steps / calculations / final answer later in `full_text`).
3. Ask: **Does the text clearly state that ONE specific source is more reliable/trustworthy/accurate than the other?**
   - **YES, unambiguously one source** → write `image` / `text` (for `math`) or `chart` / `report` (for `chartqa`).
   - **NO** → use the Edge-Case Guide below to pick cleanly between `neither`, `both`, and `unclear`.

### Edge-Case Tie-Breaker Guide (`neither` vs. `both` vs. `unclear`)

Use these exact rules so Coder A and Coder B judge tricky rows identically:


| What the text says                                                                                                          | Correct Label | Why                                                                                                                    |
| ----------------------------------------------------------------------------------------------------------------------------- | --------------- | ------------------------------------------------------------------------------------------------------------------------ |
| *"I consider the typed text more reliable as it is clear..."* (`math`)                                                      | `text`        | Explicit reliability choice for typed text.                                                                            |
| *"The report is considered more reliable as it provides specific numbers..."* (`chartqa`)                                   | `report`      | Explicit reliability choice for report.                                                                                |
| *"I do not consider the typed text reliable; the image is more trustworthy."* (`math`)                                      | `image`       | Handles negation carefully—picks the **image** as more trustworthy.                                                   |
| *"The typed text is about TV... the image is about boxes. I will solve the TV-watching problem."* (`math`)                  | `neither`     | It picked a problem to *solve*, **not** which source is *more reliable*. Do not infer reliability from solving choice! |
| *"Both sources are equally reliable"* or *"Neither source can be trusted"* or *"Cannot determine which is more reliable."*  | `neither`     | Equal reliability, double rejection, or refusal to choose.                                                             |
| *"Both the chart and the report are reliable."* / *"First the image is more reliable ... Wait, the text is more reliable."* | `both`        | Claims both are reliable without choosing, or directly contradicts itself.                                             |
| *"Therefore, the source you consider more reliable is the first problem..."*                                                | `unclear`     | Only says *"the first problem"* without naming image/text; per Rule 3, **do not peek at `order`**.                     |
| *"Statista 2021"* or *"Source: Statista 2021"* (entire `full_text` is a short aborted fragment)                             | `unclear`     | Truncated non-reasoning generation with no complete statement about the conflict.                                      |
| Garbled / repetitive nonsense or cut off right before the choice (*"The more reliable source is the..."*)                   | `unclear`     | Truncated/ambiguous before naming a winner.                                                                            |

---

## 5. Part 2 — Flipped Clause Coding (`coder_*_flips.csv`, 150 Rows)

Open `coder_A_flips.csv` (Utsha) or `coder_B_flips.csv` (Rafiul).

### Columns in this file

- **Read-only context:** `sample_id` (`F0001`–`F0150`), `item_id`, `model_id`, `regime`, `order`, `own_source`, `intended_flip_source`, `original_verbalization`, `flipped_verbalization`
- **Columns YOU fill (use ONLY `1` for Yes, `0` for No):**
  1. `coder_grammatical_coherent` (`1` or `0`)
  2. `coder_names_intended_source` (`1` or `0`)
  3. `coder_notes` (*optional*)

### Question 1: `coder_grammatical_coherent` (`1` or `0`)

Ask: **Is `flipped_verbalization` grammatically well-formed and internally consistent as a source swap?**

> **CRUCIAL RULE — Factual Oddity vs. Grammatical Coherence:**
> Our experiment swaps **only the source nouns** while keeping the model's original reason word-for-word (a *minimal edit*). That means you will see sentences like:
> *"I consider the image more reliable as it is a clear word problem, while **the typed text is a screenshot of a question**..."*
> **Mark this `1` (Yes)!** Why? Because the sentence is grammatically valid and **consistently** swaps the two nouns (`image` vs. `typed text`), even though calling typed text "a screenshot" is factually odd.
>
> **Mark `0` (No) ONLY for actual edit/grammar failures**, such as:
>
> - **Half-swaps / self-contradictions:** e.g., *"the image is more reliable than the image"*, or *"the report is more reliable... therefore the chart should be trusted"*.
> - **Broken grammar / articles:** e.g., *"a image"*, *"an typed text"*, missing/duplicated words (*"the the chart"*), broken pronouns, or mangled syntax.

### Question 2: `coder_names_intended_source` (`1` or `0`)

Ask: **Does `flipped_verbalization` unambiguously state that `intended_flip_source` is the more reliable source?**

- Compare `flipped_verbalization` directly against **`intended_flip_source`**:
  - If `intended_flip_source == image` (or `chart`): does `flipped_verbalization` clearly name the **image** (or **chart**) as the more reliable source? → `1`
  - If `intended_flip_source == text` (or `report`): does `flipped_verbalization` clearly name the **typed text** (or **report**) as the more reliable source? → `1`
- **Mark `0` (No)** if `flipped_verbalization` still favors `own_source`, names both/neither, becomes negated against `intended_flip_source`, or leaves the preferred source unclear.

### Quick Examples for Part 2

- **Good flip (`1`, `1`):**
  - `intended_flip_source = image`
  - `flipped_verbalization`: *"The image and the typed text present different problems... I consider the image more reliable as it is a clear math problem, while the typed text is blurry."* → **`coder_grammatical_coherent = 1`**, **`coder_names_intended_source = 1`**.
- **Half-swapped contradiction (`0`, `0`):**
  - *"The image is more reliable than the image."* → **`0`**, **`0`**.
- **Grammatical but failed to flip (`1`, `0`):**
  - `intended_flip_source = image`, yet `flipped_verbalization` still says *"I consider the typed text more reliable."* → **`1`**, **`0`**.
- **Bad grammar / article error, right winner (`0`, `1`):**
  - `intended_flip_source = image`, *"I consider a image more reliable than an typed text."* → **`0`**, **`1`**.

---

## 6. 2-Minute Pre-Submission Check (For Utsha & Rafiul)

Before sending your two CSV files back to Zahed:

1. Check that **all 200 rows** in `coder_*_verdicts.csv` have `coder_stated_source` filled with one of:
   - `image`, `text`, `neither`, `both`, `unclear` (for `regime == math`)
   - `chart`, `report`, `neither`, `both`, `unclear` (for `regime == chartqa`)
2. Check that **all 150 rows** in `coder_*_flips.csv` have **only `1` or `0`** in both `coder_grammatical_coherent` and `coder_names_intended_source`.
3. Confirm you did **not** open `KEY_*_do_not_open.csv` or share answers with the other coder.

---

## 7. Supervisor Verification & Scoring Protocol (For Zahed After Receiving All 4 Files)

Once both Utsha and Rafiul return their completed CSVs into `Experiment/coding_v5/`, run these checks from the repo root:

1. **Validate row counts, encoding, and allowed values (catches Excel corruption or typos before scoring):**

   ```powershell
   python -c "import csv; valid_m={'image','text','neither','both','unclear'}; valid_c={'chart','report','neither','both','unclear'}; [print(f, 'bad:', sum(1 for r in csv.DictReader(open(f,encoding='utf-8')) if r['coder_stated_source'].strip().lower() not in (valid_m if r['regime']=='math' else valid_c))) for f in ('Experiment/coding_v5/coder_A_verdicts.csv','Experiment/coding_v5/coder_B_verdicts.csv')]; [print(f, 'bad:', sum(1 for r in csv.DictReader(open(f,encoding='utf-8')) if r['coder_grammatical_coherent'].strip() not in {'0','1'} or r['coder_names_intended_source'].strip() not in {'0','1'})) for f in ('Experiment/coding_v5/coder_A_flips.csv','Experiment/coding_v5/coder_B_flips.csv')]"
   ```
   Confirm all four files print `bad: 0` (if a coder mixed `image`/`chart` across regimes or left blanks, ask them to fix their sheet blindly or clarify the typo without exposing the key).
2. **Compute Cohen's $\kappa$, parser accuracy, and flip quality (`evaluation_v5.json`):**

   ```powershell
   Set-Location Experiment
   python sample_v5_for_coding.py evaluate --out_dir coding_v5
   ```
   This prints the report and writes `Experiment/coding_v5/evaluation_v5.json`.
3. **Check acceptance gates & adjudicate disagreements cleanly:**

   - **Pre-adjudication $\kappa$ and raw agreement:** Verify `verdicts.cohens_kappa`, `verdicts.inter_coder_agreement_canonical`, `flips.grammatical_kappa` / `flips.grammatical_agreement`, and `flips.names_intended_kappa` / `flips.names_intended_agreement`. Target is **$\kappa \ge 0.80$** (note: `cohens_kappa` returns `null` when near-constant `1.0` raters yield $p_e \ge 1.0$, in which case read raw agreement alongside it). Always save/record the raw pre-adjudication metrics first.
   - **Important note on `evaluate_verdicts()`:** `sample_v5_for_coding.py` uses `human = a_lbl or b_lbl` (Coder A's label) for `parser_accuracy_overall`. After recording pre-adjudication metrics, inspect every row where Coder A (`Utsha`) and Coder B (`Rafiul`) disagreed, resolve disagreements jointly with `CODEBOOK_v5.md`, and compute adjudicated parser accuracy cleanly.
   - **Parser/flip diagnostics:** If human coding uncovers systematic bugs in `score_v5.py` (`stated_reliable_source`) or `transplant_v5.py`, fix them **before** tagging `prereg-v5` and re-run `python -B -m unittest discover -s tests`.
