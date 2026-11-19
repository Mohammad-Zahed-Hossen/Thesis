# Antigravity Forensic Audit — `Experiment/coding_v5`

- **Date:** `2026-11-20`
- **Audited Commit:** `418aa82` (with restored `KEY_*.csv` from `5b57529` untracked & gitignored)
- **Status:** Read-only audit — no fixes applied yet; ready for independent Claude Opus 5.5 cross-audit
- **Scope:** [Experiment/coding_v5/](<file:///c:/Thesis/Important/Thesis/Causal%20Conflict%20Verbalization%20and%20Source%20Arbitration/Experiment/coding_v5>), [Experiment/results_v5/](<file:///c:/Thesis/Important/Thesis/Causal%20Conflict%20Verbalization%20and%20Source%20Arbitration/Experiment/results_v5>), [harness_v5.py](<file:///c:/Thesis/Important/Thesis/Causal%20Conflict%20Verbalization%20and%20Source%20Arbitration/Experiment/harness_v5.py>), [score_v5.py](<file:///c:/Thesis/Important/Thesis/Causal%20Conflict%20Verbalization%20and%20Source%20Arbitration/Experiment/score_v5.py>), [transplant_v5.py](<file:///c:/Thesis/Important/Thesis/Causal%20Conflict%20Verbalization%20and%20Source%20Arbitration/Experiment/transplant_v5.py>), [sample_v5_for_coding.py](<file:///c:/Thesis/Important/Thesis/Causal%20Conflict%20Verbalization%20and%20Source%20Arbitration/Experiment/sample_v5_for_coding.py>), [analyze_v5.py](<file:///c:/Thesis/Important/Thesis/Causal%20Conflict%20Verbalization%20and%20Source%20Arbitration/Experiment/analyze_v5.py>), [preflight_v5.py](<file:///c:/Thesis/Important/Thesis/Causal%20Conflict%20Verbalization%20and%20Source%20Arbitration/Experiment/preflight_v5.py>), [.gitignore](<file:///c:/Thesis/Important/Thesis/Causal%20Conflict%20Verbalization%20and%20Source%20Arbitration/.gitignore>), and [PREREGISTRATION_VERDICT_TRANSPLANT.md](<file:///c:/Thesis/Important/Thesis/Causal%20Conflict%20Verbalization%20and%20Source%20Arbitration/Docs/PREREGISTRATION_VERDICT_TRANSPLANT.md>).

---

## 1. Executive Summary & Gate Status `[Verified]`

Both coders (`Coder A` = Utsha, `Coder B` = Rafiul) have completed **100% of all four coding sheets** (`200/200` verdicts and `150/150` flips, `0` blanks, `0` invalid labels), committed in `057a6c3` (Coder B) and `6b75f10` (Coder A), with `Experiment/archive/results_v5` removed in `418aa82`; `KEY_verdicts_do_not_open.csv` and `KEY_flips_do_not_open.csv` have been restored locally from `5b57529` (untracked and ignored by [.gitignore](<file:///c:/Thesis/Important/Thesis/Causal%20Conflict%20Verbalization%20and%20Source%20Arbitration/.gitignore#L1>) line 1).

| Validation Dimension                                                     |                      Overall (`N=200` / `150`) |       Confirmatory 3B+7B Math (`N=120` / `81`) | Gate / Status                                                                                                                          |
| ------------------------------------------------------------------------ | -------------------------------------------------: | -------------------------------------------------: | -------------------------------------------------------------------------------------------------------------------------------------- |
| **Verdicts — inter-coder agreement (raw 7-class)**                | `91.5%` (`183/200`), **κ = `0.8803`** | `98.3%` (`118/120`), **κ = `0.9606`** | **PASS** (κ ≥ `0.80`)                                                                                                        |
| **Verdicts — inter-coder agreement (canonical 3-way)**            | `98.5%` (`197/200`), **κ = `0.9783`** | `98.3%` (`118/120`), **κ = `0.9606`** | **PASS** (κ ≥ `0.80`)                                                                                                        |
| **Verdicts — `score_v5` parser accuracy (A / B / Adjudicated)** |       `98.5%` / `100.0%` / **`99.5%`** |      `98.3%` / `100.0%` / **`100.0%`** | **PASS** (`168/168` on all 3B+7B)                                                                                              |
| **Flips — grammatical/coherent rate (A / B)**                     |  `96.7%` (`145/150`) / `99.3%` (`149/150`) |     `98.8%` (`80/81`) / `100.0%` (`81/81`) | **Prevalence paradox:** `97.3%` agree, **AC1 = `0.9722`**, **PABAK = `0.9467`**, but **κ = `0.3258`** |
| **Flips — names intended source (A / B)**                         | `99.3%` (`149/150`) / `100.0%` (`150/150`) |    `100.0%` (`81/81`) / `100.0%` (`81/81`) | **Prevalence paradox:** `99.3%` agree, **AC1 = `0.9933`**, **PABAK = `0.9867`**, but **κ = `0.0000`** |

**Top findings requiring attention before tagging `prereg-v5`:**

1. **Restored `KEY_*.csv` status + `sample_v5_for_coding.py` `px501k` glob/clobber hazard:** Both restored key files match `5b57529` (`01b88f9bd8e5` / `3d6c87e86f3e`), `evaluate()` now runs and produces identical JSON (`rep_disk == rep_reg` is `True`), **but** `KEY_verdicts_do_not_open.csv` has **5 stale `beh_source` cells** (`V0032`, `V0092`, `V0140`, `V0149`, `V0176`: `'neither'` vs current `'text'`/`'image'` from post-`328c8af` `_MATH_FINAL_ANSWER`), and running `sample_v5_for_coding.py sample` without `--donor_files` still pulls the 2 `px501k` donor files (scrambling `198/200` verdict rows) and destructively overwrites `coder_A/B_*.csv`.
2. **Real parser + Gate-2 bug exposed by `F0081` (`score_v5.py` / `transplant_v5.py`):** On coordinate-clause verdicts like `"...is the first image, and the source that is more reliable is the typed text."`, `score_v5.stated_reliable_source()` crosses `, and` and returns `image`, inverting `own_source`/`flip_source` and fooling Gate 2 symmetrically. Scanning all `2,760` main donor rows shows **0 hits on confirmatory 3B/7B** and **3 hits all on diagnostic-only 2B** (`gsm8k-image-L0-0057` [`F0081`], `gsm8k-image-L0-0162`, `gsm8k-image-L0-0119`).
3. **Excel round-trip corruption on read-only verdict columns (`coding_v5/`):** Both `coder_A_verdicts.csv` and `coder_B_verdicts.csv` were saved via Windows Excel (UTF-8 BOM + CRLF), introducing **7 identical read-only cell alterations** (`÷`/`×` mojibake in `V0029`/`V0059`/`V0114`; `'20.4%'` → `'20.40%'` in `V0076`; `'3.0'` → `'3'` in `V0117`).
4. **Cross-sentence semantic contradictions in `flip` (`F0147`, `F0134`, `F0065`) explain dev `results_v5` behavior:** Minimal-edit single-sentence swaps leave prior topic mappings (Sentence 2) and post-verdict sentences untouched—affecting **37/280 (`13.2%`)** passed 7B Math cells and **10/190 (`5.3%`)** + **3/190 (`1.6%`)** post-verdict cells in 3B Math, illuminating the `21.1 pp` dev gap on 7B Math (`flip − own = +45.7 pp` vs `para_flip − para = +66.8 pp`).
5. **Flip κ prevalence paradox & `sample_v5_for_coding.py` evaluator bias:** `evaluate_verdicts()` and `evaluate_flips()` silently use Coder A only (`a_lbl or b_lbl`, `ga if ga is not None else gb`), and `cohens_kappa()` returns `0.0` (not `None` or AC1/PABAK) when one rater is `100%` constant `1`.
6. **Windows CRLF vs Linux LF bug in `preflight_v5.py --check_manifests`:** Running manifest verification on Windows yields **84 false-positive hash errors** across all 20 `results_v5/*.manifest.json` files, even though LF-normalized SHA-256 digests match **100%**.

---

## 2. File Inventory, Encoding & Provenance Integrity (`coding_v5/` vs `results_v5/`) `[Verified]`

### 2.1 Files on disk vs expected

In [Experiment/coding_v5/](<file:///c:/Thesis/Important/Thesis/Causal%20Conflict%20Verbalization%20and%20Source%20Arbitration/Experiment/coding_v5>):

- **Present & tracked:** [CODEBOOK_v5.md](<file:///c:/Thesis/Important/Thesis/Causal%20Conflict%20Verbalization%20and%20Source%20Arbitration/Experiment/coding_v5/CODEBOOK_v5.md>) (byte-identical to `sample_v5_for_coding.CODEBOOK_MD`), [HUMAN_CODING_INSTRUCTIONS_v5.md](<file:///c:/Thesis/Important/Thesis/Causal%20Conflict%20Verbalization%20and%20Source%20Arbitration/Experiment/coding_v5/HUMAN_CODING_INSTRUCTIONS_v5.md>), [coder_A_verdicts.csv](<file:///c:/Thesis/Important/Thesis/Causal%20Conflict%20Verbalization%20and%20Source%20Arbitration/Experiment/coding_v5/coder_A_verdicts.csv>), [coder_B_verdicts.csv](<file:///c:/Thesis/Important/Thesis/Causal%20Conflict%20Verbalization%20and%20Source%20Arbitration/Experiment/coding_v5/coder_B_verdicts.csv>), [coder_A_flips.csv](<file:///c:/Thesis/Important/Thesis/Causal%20Conflict%20Verbalization%20and%20Source%20Arbitration/Experiment/coding_v5/coder_A_flips.csv>), [coder_B_flips.csv](<file:///c:/Thesis/Important/Thesis/Causal%20Conflict%20Verbalization%20and%20Source%20Arbitration/Experiment/coding_v5/coder_B_flips.csv>).
- **Present locally (untracked & gitignored):** [KEY_verdicts_do_not_open.csv](<file:///c:/Thesis/Important/Thesis/Causal%20Conflict%20Verbalization%20and%20Source%20Arbitration/Experiment/coding_v5/KEY_verdicts_do_not_open.csv>) (blob `01b88f9bd8e5`, `200` rows, no BOM) and [KEY_flips_do_not_open.csv](<file:///c:/Thesis/Important/Thesis/Causal%20Conflict%20Verbalization%20and%20Source%20Arbitration/Experiment/coding_v5/KEY_flips_do_not_open.csv>) (blob `3d6c87e86f3e`, `150` rows, no BOM) — [.gitignore](<file:///c:/Thesis/Important/Thesis/Causal%20Conflict%20Verbalization%20and%20Source%20Arbitration/.gitignore#L1>) line 1 (`Experiment/coding_*/KEY_*.csv`) already ignores both (`git check-ignore -v` verified; `git ls-files -- *KEY_* */KEY_*` empty; [preflight_v5.py](<file:///c:/Thesis/Important/Thesis/Causal%20Conflict%20Verbalization%20and%20Source%20Arbitration/Experiment/preflight_v5.py#L230-L243>) `errors: []`).
- **Absent (not yet generated):** `evaluation_v5.json`.
- **Stale documentation:** [HUMAN_CODING_INSTRUCTIONS_v5.md](<file:///c:/Thesis/Important/Thesis/Causal%20Conflict%20Verbalization%20and%20Source%20Arbitration/Experiment/coding_v5/HUMAN_CODING_INSTRUCTIONS_v5.md#L56>), [Experiment/README.md](<file:///c:/Thesis/Important/Thesis/Causal%20Conflict%20Verbalization%20and%20Source%20Arbitration/Experiment/README.md#L75>), and [Experiment/results_v5/README.md](<file:///c:/Thesis/Important/Thesis/Causal%20Conflict%20Verbalization%20and%20Source%20Arbitration/Experiment/results_v5/README.md#L79>) still state `0` filled rows.

### 2.2 Exact parity against `results_v5/` & Excel round-trip mutations

- **Donor 0-diff parity:** All 6 main `200704` donor JSONL files in `Experiment/results_v5/` (`2,760` total rows: `800×3` Math + `120×3` ChartQA) have **0 full_text/key diffs** against `Experiment/archive/results_v5_Prev_backup/`. Re-running `build_verdict_samples(..., 200, 42)` and `build_flip_samples(..., 50, 42)` on those 6 main donor files reproduces **200/200 verdict row identities** and **150/150 flip rows byte-for-byte** (after line-ending normalization).
- **A vs B read-only integrity:** `0` differences between Coder A and Coder B on any read-only column (`sample_id`, `item_id`, `model_id`, `regime`, `family`, `order`, `verbalization_text`, `full_text`, `own_source`, `intended_flip_source`, `original_verbalization`, `flipped_verbalization`). Neither coder sorted, deleted, or shifted rows.
- **Excel mutations vs pre-coding sheets / `KEY_verdicts_do_not_open.csv`:** In the original pre-coding sheets (commit `5b57529`), all CSVs were clean UTF-8 without BOM and pure LF (`0` CRLFs); `coder_A/B_*.csv` are now committed at `6b75f10` / `057a6c3`, while `KEY_verdicts_do_not_open.csv` (from `5b57529`) retains the clean pre-Excel UTF-8 text with `0` non-CRLF diffs against `results_v5/`. All 4 committed coder CSVs now have UTF-8 BOM (`\xef\xbb\xbf`) and CRLF (`1,640` CRLFs in verdicts, `151` in flips), and **both** `coder_A_verdicts.csv` and `coder_B_verdicts.csv` share **7 identical content mutations** from opening/re-saving in Windows Excel:
  - `V0029` (`gsm8k-image-L0-0054`), `V0059` (`gsm8k-image-L0-0077`), `V0114` (`gsm8k-image-L0-0112`): UTF-8 math symbols `÷` / `×` mojibaked to `Ã·` / `Ã—` inside `full_text` (not in `verbalization_text`).
  - `V0076` (ChartQA id `21`): `'20.4%'` → `'20.40%'` in both `verbalization_text` and `full_text`.
  - `V0117` (ChartQA id `29`): `'3.0'` → `'3'` in both `verbalization_text` and `full_text`.
  - Plus `137` `full_text` cells converted internal `\n` to `\r\n`. None of these affect label validity or `sample_id` joins, because `sample_v5_for_coding.read_csv_map()` reads `encoding="utf-8-sig"`.
- **Leading whitespace in Coder B:** `coder_B_verdicts.csv` has `21` cells with a leading space (`' text'` × 16, `' image'` × 5) and `10` non-empty `coder_notes` (including typos like `" doesn't identify any preffered source"` and a stray `"."`). `sample_v5_for_coding.py` strips whitespace, so scoring is unaffected, though the CSV should be normalized before archiving.
- **Validation command bug in [HUMAN_CODING_INSTRUCTIONS_v5.md](<file:///c:/Thesis/Important/Thesis/Causal%20Conflict%20Verbalization%20and%20Source%20Arbitration/Experiment/coding_v5/HUMAN_CODING_INSTRUCTIONS_v5.md#L181>):** That PowerShell snippet opens files with `encoding='utf-8'` instead of `encoding='utf-8-sig'`. Because of the BOM, the first header parses as `'\ufeffsample_id'` (it only prints `bad: 0` because the snippet never accesses `r['sample_id']`).

### 2.3 Restored `KEY_*.csv` Audit (`5b57529` vs Current `results_v5/` & Code)

- **`KEY_flips_do_not_open.csv` (`150` rows):** **100.0% aligned** — `0` diffs across all `150 × 11` cells against both 6-donor and 8-donor regeneration, and `0` diffs across all `150 × 9` shared cells against `coder_A_flips.csv` and `coder_B_flips.csv`. *(Why 8-donor regen accidentally matched flips while scrambling `198/200` verdict rows: `build_flip_samples()` deduplicates by `(model_id, regime, id, order)` and `v5dev_chartqa_donor_*` sorts alphabetically before `v5dev_chartqa_px501k_donor_*`, whereas `build_verdict_samples()` does not deduplicate.)*
- **`KEY_verdicts_do_not_open.csv` (`200` rows):** **100.0% aligned on all `evaluate()` columns** — `0/200` diffs on `sample_id`, `item_id`, `model_id`, `regime`, `family`, `order`, `predicted_stated_source`, and `0/200` non-CRLF content diffs on `verbalization_text` / `full_text` (`140` `full_text` cells have CRLF from Windows checkout). Running `evaluate_verdicts()` and `evaluate_flips()` on the restored disk KEY files produces **bit-for-bit identical output (`rep_disk == rep_reg` is `True`)** to fresh 6-donor regeneration.
- **5 stale `beh_source` cells in `KEY_verdicts_do_not_open.csv`:** Commit `5b57529` is the parent of `328c8af`, which updated `_MATH_FINAL_ANSWER` in [score_v5.py](<file:///c:/Thesis/Important/Thesis/Causal%20Conflict%20Verbalization%20and%20Source%20Arbitration/Experiment/score_v5.py#L202-L205>) to accept optional `the` (`Final answer: N`) and `:` after `is` (`The final answer is: N.`). As a result, `KEY_verdicts_do_not_open.csv` retains `beh_source = 'neither'` on 5 rows where current `score_v5.py` (`parser="structured"`) recovers the answer (`evaluate_verdicts()` does not read `beh_source`, so `evaluation_v5.json` is unaffected):

| `sample_id` | Model / Family / Item | Ending in `full_text` | Stored `KEY` `beh_source` | Current `score_v5` `beh_source` |
|---|---|---|---|---|
| `V0032` | 7B Math `free_binding` `gsm8k-image-L0-0099` | `Final answer: 175` | `neither` | **`text`** |
| `V0092` | 7B Math `free_binding` `gsm8k-image-L0-0136` | `Final answer: 6` | `neither` | **`image`** |
| `V0140` | 3B Math `free_binding` `svamp-image-L0-0015` | `Final answer: 5` | `neither` | **`text`** |
| `V0149` | 7B Math `free_binding` `gsm8k-image-L0-0090` | `Final answer: 225` | `neither` | **`image`** |
| `V0176` | 7B Math `donor` `gsm8k-image-L0-0123` | `The final answer is: 10.` | `neither` | **`text`** |

- **Semantic pipeline errors stored inside the KEY files (do NOT hand-edit):** Two diagnostic-2B KEY rows record real pipeline mispredictions — `KEY_verdicts` `V0177` (`svamp-image-L0-0022`, `text_first`, `predicted_stated_source = 'image'`) and `KEY_flips` `F0081` (`gsm8k-image-L0-0057`, `text_first`, `own_source = 'image'`, `flip_source = 'text'`). These are faithful records of what the pipeline produced so human coding can catch them and must not be hand-edited in the KEYs.
- **No stray verification scripts:** Neither `verify_keys.py` nor `inspect_diffs.py` remains on disk.

---

## 3. Part 1 — Donor Verbalization Coding (`200` Rows) vs [score_v5.py](<file:///c:/Thesis/Important/Thesis/Causal%20Conflict%20Verbalization%20and%20Source%20Arbitration/Experiment/score_v5.py>) `[Verified]`

### 3.1 Stratification audit vs pre-registration §8

The sampled `200` rows match [PREREGISTRATION_VERDICT_TRANSPLANT.md](<file:///c:/Thesis/Important/Thesis/Causal%20Conflict%20Verbalization%20and%20Source%20Arbitration/Docs/PREREGISTRATION_VERDICT_TRANSPLANT.md#L558>) §8 exactly:

- **Confirmatory Math (`60%` = `120`):** `60` 3B (`40 donor / 20 free_binding`; `30/30` order) + `60` 7B (`40/20`; `30/30` order).
- **3B/7B ChartQA (`24%` = `48`):** `24` 3B (`16/8`; `12/12`) + `24` 7B (`16/8`; `12/12`).
- **Diagnostic 2B (`16%` = `32`):** `16` Math (`8/8`; `8/8`) + `16` ChartQA (`8/8`; `8/8`).

### 3.2 Agreement & parser accuracy breakdown

| Subset                                   |             N |                   Raw Agree / κ |              Canonical Agree / κ |          Parser Acc (A) |           Parser Acc (B) |           Parser Acc (Adjudicated) |
| ---------------------------------------- | ------------: | -------------------------------: | --------------------------------: | ----------------------: | -----------------------: | ---------------------------------: |
| **Overall**                        | **200** | `91.5%` / **`0.8803`** |  `98.5%` / **`0.9783`** | `98.5%` (`197/200`) | `100.0%` (`200/200`) |  **`99.5%`** (`199/200`) |
| **Confirmatory 3B+7B Math**        | **120** | `98.3%` / **`0.9606`** |  `98.3%` / **`0.9606`** | `98.3%` (`118/120`) | `100.0%` (`120/120`) | **`100.0%`** (`120/120`) |
| **All 3B+7B (Math + ChartQA)**     | **168** | `91.7%` / **`0.8780`** |  `98.8%` / **`0.9823`** | `98.8%` (`166/168`) | `100.0%` (`168/168`) | **`100.0%`** (`168/168`) |
| **Diagnostic 2B (Math + ChartQA)** |  **32** | `90.6%` / **`0.8613`** |  `96.9%` / **`0.9443`** |   `96.9%` (`31/32`) |   `100.0%` (`32/32`) |    **`96.9%`** (`31/32`) |
| **ChartQA (all 3 models)**         |  **64** |           `78.1%` / `0.7019` | `100.0%` / **`1.0000`** |  `100.0%` (`64/64`) |   `100.0%` (`64/64`) |   **`100.0%`** (`64/64`) |

*(Raw exact match against `score_v5` is `79.5%` [A] / `80.0%` [B] only because the parser outputs `absent`/`undetermined` while coders output `neither`/`unclear`—all mapped cleanly to `no_verdict` by `canonical_verdict_label()`.)*

### 3.3 Forensic audit of all 17 raw disagreements & adjudication

1. **14 ChartQA bare-answer rows (`A = neither`, `B = unclear`, `parser = absent`):** `V0002`, `V0013`, `V0030`, `V0058`, `V0071`, `V0076`, `V0079`, `V0082`, `V0117`, `V0161`, `V0168`, `V0171`, `V0179`, `V0193`. Every single one is an unverbalized bare answer (`'4.10 million U.S. dollars'`, `'28706 thousand'`, `'Yes'`, `'307'`, `'23'`, `'20.4%'`, `'30.45'`, `'3.0'`, `'2411'`, `'36'`). Both coders agree `100%` canonically (`no_verdict`), and the raw split reflects a mild boundary ambiguity between `neither` (no preference stated) and `unclear` (aborted fragment per `HUMAN_CODING_INSTRUCTIONS_v5.md` line 108).
2. **2 canonical disagreements in 3B Math `free_binding` (`V0093`, `V0103`) — Coder A error:**
   - `V0093` (`gsm8k-image-L0-0020`): `"...I will solve the problem from the typed text."` → A=`text`, B=`neither`, parser=`absent`.
   - `V0103` (`gsm8k-image-L0-0103`): `"...I will solve the problem from the typed text."` → A=`text`, B=`neither`, parser=`absent`.
   - **Proof:** Both violate the explicit tie-breaker in [HUMAN_CODING_INSTRUCTIONS_v5.md](<file:///c:/Thesis/Important/Thesis/Causal%20Conflict%20Verbalization%20and%20Source%20Arbitration/Experiment/coding_v5/HUMAN_CODING_INSTRUCTIONS_v5.md#L104>) (*"It picked a problem to solve, not which source is more reliable"*). Moreover, Coder A was self-inconsistent, marking the syntactically identical `V0194` (`"...I will solve the problem from the typed text."`) as `neither`. **Adjudication: `neither` (`no_verdict`)** — parser (`absent`) is **correct**.
3. **1 canonical disagreement in diagnostic 2B Math `donor` (`V0177`, `svamp-image-L0-0022`, `text_first`) — Genuine `score_v5` failure:**
   - `VERB`: `"The two images present different problems. The first image asks a question about the number of girls and boys in a school, while the second image asks a question about the number of files and apps Dave had on his phone after deleting some. Therefore, the source I consider more reliable is the first image..."`
   - **Ground-truth cross-check against `v5dev_conflict_donor_qwen25_7b.jsonl`:** On `svamp-image-L0-0022`, the **typed text** is the girls-and-boys problem (`y_text = 333`), while the **image** is Dave's apps (`y_image = 3`)! Because `order == text_first`, 2B hallucinated both sources as `"images"` and picked `"the first image"`—which actually refers to the **typed text**!
   - Coder A (`unclear`) correctly enforced Rule 3 (ambiguous positional reference without peeking at `order`). Both `score_v5` (`image`) and Coder B (`image`) matched `"image"` literally. **Adjudication: `unclear` (`no_verdict`)** — `score_v5` is **wrong** here (`1/200` error, confined to diagnostic 2B).

**Adjudicated canonical 3×3-equivalent confusion matrix (`N = 200`):**

- `image → image`: `35`, `text → text`: `94`, `chart → chart`: `11`, `report → report`: `19`, `no_verdict → no_verdict`: `40`, **`no_verdict → image`: `1`** (`V0177`). Zero `image ↔ text` or `chart ↔ report` confusions.

**Blinding sanity check on Coder B's `200/200` match with the parser `[Inferred]`:** Despite `100.0%` canonical match with `score_v5`, the evidence strongly indicates independent faithful coding rather than key peeking: (i) `KEY_*` files were removed in `328c8af`, gitignored, and absent during human coding (restored locally only after both coders committed); (ii) Coder B typed manual leading spaces on `21` labels and wrote organic free-text notes with typos (`"preffered"`); (iii) Coder B followed the instruction sheet strictly on `V0093`/`V0103` and on bare-answer `unclear` rows; and (iv) on flips, Coder B disagreed with `KEY_flips` on `F0006` (`0`) and failed to catch `F0081`'s inverted source (`1`).

---

## 4. Part 2 — Flip Quality Coding (`150` Rows) vs [transplant_v5.py](<file:///c:/Thesis/Important/Thesis/Causal%20Conflict%20Verbalization%20and%20Source%20Arbitration/Experiment/transplant_v5.py>) & [score_v5.py](<file:///c:/Thesis/Important/Thesis/Causal%20Conflict%20Verbalization%20and%20Source%20Arbitration/Experiment/score_v5.py>) `[Verified]`

### 4.1 Metrics & the Cohen's κ prevalence paradox

| Subset                             |             N |    Grammatical (A / B) |              Gram Agree |                                    Gram κ / AC1 / PABAK |    Intended Src (A / B) |                Src Agree |                                     Src κ / AC1 / PABAK |
| ---------------------------------- | ------------: | ---------------------: | ----------------------: | -------------------------------------------------------: | ----------------------: | -----------------------: | -------------------------------------------------------: |
| **All models**               | **150** |  `96.7%` / `99.3%` | `97.3%` (`146/150`) | `0.3258` / **`0.9722`** / **`0.9467`** |  `99.3%` / `100.0%` |  `99.3%` (`149/150`) | `0.0000` / **`0.9933`** / **`0.9867`** |
| **Confirmatory 3B+7B Math**  |  **81** | `98.8%` / `100.0%` |   `98.8%` (`80/81`) |                     `0.0000` / `0.9875` / `0.9753` | `100.0%` / `100.0%` |   `100.0%` (`81/81`) |                       `None` / `1.0000` / `1.0000` |
| **All 3B+7B (Math+ChartQA)** | **120** | `99.2%` / `100.0%` | `99.2%` (`119/120`) |                     `0.0000` / `0.9916` / `0.9833` | `100.0%` / `100.0%` | `100.0%` (`120/120`) |                       `None` / `1.0000` / `1.0000` |
| **Diagnostic 2B**            |  **30** |  `86.7%` / `96.7%` |   `90.0%` (`27/30`) |                     `0.3662` / `0.8805` / `0.8000` |  `96.7%` / `100.0%` |    `96.7%` (`29/30`) |                     `0.0000` / `0.9655` / `0.9333` |

- **Why κ collapses on flips:** In [sample_v5_for_coding.py](<file:///c:/Thesis/Important/Thesis/Causal%20Conflict%20Verbalization%20and%20Source%20Arbitration/Experiment/sample_v5_for_coding.py#L297-L305>), `cohens_kappa()` only returns `None` when `pe >= 1.0 - 1e-12` (both raters `100%` constant). When Coder B gives `150/150` `1`s and Coder A gives `149/150` `1`s (`names_intended_source`), `pe = 149/150 = agree`, so `(agree - pe)/(1 - pe) = 0.0` despite `99.3%` raw agreement! Similarly, `grammatical` has `145` vs `149` `1`s (`146/150` agree, `1` shared `0`), yielding `κ = 0.3258` even though Gwet's AC1 = `0.9722` and PABAK = `0.9467`. Because [PREREGISTRATION_VERDICT_TRANSPLANT.md](<file:///c:/Thesis/Important/Thesis/Causal%20Conflict%20Verbalization%20and%20Source%20Arbitration/Docs/PREREGISTRATION_VERDICT_TRANSPLANT.md#L558>) §8 states `κ ≥ 0.80` globally, you should explicitly report **raw agreement + Gwet's AC1 / PABAK** alongside κ for near-degenerate binary flip ratings (where expected base rate ≈ `0.98–1.00`), as already anticipated in [HUMAN_CODING_INSTRUCTIONS_v5.md](<file:///c:/Thesis/Important/Thesis/Causal%20Conflict%20Verbalization%20and%20Source%20Arbitration/Experiment/coding_v5/HUMAN_CODING_INSTRUCTIONS_v5.md#L193>).

### 4.2 Critical bug exposed by `F0081`: coordinate-clause crossing in `score_v5.stated_reliable_source()`

Look at `F0081` (`Qwen2-VL-2B`, `math`, `text_first`, `gsm8k-image-L0-0057`, coded `gram=(0,1)`, `intended=(0,1)`):

- **`ORIG`:** `"...Therefore, the source that presents the same problem is the first image, and the source that is more reliable is the typed text."`
- **`FLIP`:** `"...Therefore, the source that presents the same problem is the first typed text, and the source that is more reliable is the image."`
- **What went wrong:** In [score_v5.py](<file:///c:/Thesis/Important/Thesis/Causal%20Conflict%20Verbalization%20and%20Source%20Arbitration/Experiment/score_v5.py#L106-L127>), `stated_reliable_source()` looks for `_SOURCE_NOUN` in `s[:idx]` (before `"reliable"`) and checks `_CLAUSE_SPLIT` only *before* `last_m` (`prefix = s[:last_m.start()]`)—never *between* `last_m.end()` and `idx`. It therefore grabbed `"first image"` from the earlier coordinate clause, misclassified `ORIG` as `own_source = image` (true: `text`), then misclassified `FLIP` as `flip_source = text` (true: `image`) by the exact same bug, causing Gate 2 in [transplant_v5.py](<file:///c:/Thesis/Important/Thesis/Causal%20Conflict%20Verbalization%20and%20Source%20Arbitration/Experiment/transplant_v5.py#L356>) to **falsely pass**. Coder A caught it (`0`); Coder B missed it (`1`).
- **Full scan of all `2,760` main donor rows in `results_v5/`:**
  - `38` rows have a `_CLAUSE_SPLIT` between the last pre-`"reliable"` noun and `"reliable"`.
  - **29/29 confirmatory 7B rows are parsed 100% correctly** (all are valid subordinate/antecedent clauses like `"Given that the report..., I consider it more reliable"` or `"Therefore, I will solve the problem from the image, as it is the more reliable source"`—so blindly rejecting every comma between `last_m` and `"reliable"` would **break 7B**!).
  - **All 3 parser errors occur on diagnostic-only `Qwen2-VL-2B`:**
    1. `gsm8k-image-L0-0057` (`donor`, `text_first`, = `F0081`): returns `image` instead of `text`.
    2. `gsm8k-image-L0-0162` (`free_binding`, `image_first`): `"The image and the typed text present the same problem, but the source you consider more reliable is the typed text."` → returns `undetermined` instead of `text` (triggered two-source rejection in the earlier clause!).
    3. `gsm8k-image-L0-0119` (`donor`, `text_first`): `"However, the source of the typed text is not specified, so I will consider Adrien's salary as the more reliable source."` → returns `text` instead of `undetermined`.
  - *Surgical fix option (if you choose to patch pre-freeze):* restrict `before_matches` to the clause after a coordinate break (`,\s*(?:and|but)\b`) whenever `after` contains a source noun (or inside `s[coord_end:]`).

### 4.3 All 5 flagged flips + 2 unflagged structural flip issues (and how they explain dev `results_v5`)

| Sample ID                 | Model / Split / Order            | A / B (`gram`, `src`) | Root Cause                                                                                                                                                                                                                                                                                                                                                 |
| ------------------------- | -------------------------------- | ------------------------- | ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `F0006`                 | 2B Math `text_first`           | `(0,1)` / `(0,1)`     | 2B `"two images"` hallucination → `"the first typed text"` (both coders `0` on grammar)                                                                                                                                                                                                                                                             |
| `F0029`                 | 2B Math `text_first`           | `(0,1)` / `(1,1)`     | Same 2B `"first image"` → `"first typed text"`                                                                                                                                                                                                                                                                                                        |
| `F0081`                 | 2B Math `text_first`           | `(0,0)` / `(1,1)`     | **Parser + Gate-2 inversion bug** (§4.2 above) + `"first typed text"`                                                                                                                                                                                                                                                                             |
| `F0100`                 | 2B Math `text_first`           | `(0,1)` / `(1,1)`     | 2B `"two images ... Richard's image"` → `"Richard's typed text"`                                                                                                                                                                                                                                                                                      |
| `F0147`                 | **7B Math** `text_first` | `(0,1)` / `(1,1)`     | **Cross-sentence S2–S3 topic contradiction** (`S2` says `typed text` = salary, `image` = containers; `S3` flip says `The image is more reliable as it provides a clear and specific problem related to salary...`). Note `gsm8k-image-L0-0118` failed base competency in 7B, so it did not enter `v5dev_conflict_tp_qwen25_7b.jsonl`. |
| `F0134` *(unflagged)* | **7B Math** `text_first` | `(1,1)` / `(1,1)`     | Identical S2–S3 topic contradiction (`S2`: `typed text` = Helen's cookies, `image` = bus; `S3` flip: `The image is more reliable ... related to the number of cookies Helen baked`). Both coders followed the "factual oddity → 1" instruction.                                                                                                |
| `F0065` *(unflagged)* | 2B Math `text_first`           | `(1,1)` / `(1,1)`     | **Unswapped post-verdict sentence:** `S1` flipped to `"the source of the image is more reliable"`, while `S2` stayed `"The typed text provides a clear and concise solution..., while the image does not..."` — direct contradiction left untouched by Gate 1.                                                                              |

**Quantifying these exact failure modes across all actual passed transplant cells in `Experiment/results_v5/`:**

- **S2–S3 topic contradictions (`F0147`/`F0134` pattern):** **37/280 (`13.2%`)** of passed 7B Math cells (e.g., `gsm8k-image-L0-0067`, `-0015`, `-0010`, `-0107`, `svamp-image-L0-0030`) and **10/190 (`5.3%`)** of passed 3B Math cells (`0/10` 3B ChartQA).
- **Unswapped post-verdict sentences (`F0065` pattern):** **3/190 (`1.6%`)** of passed 3B Math cells—including direct self-contradiction `gsm8k-image-L0-0084` (`"The image is more reliable as it is a mathematical problem... The image is a statement about a football team's performance, which is not a mathematical problem."`), plus `gsm8k-image-L0-0046` and `-0113` (`0/280` in 7B Math, `0/10` in 3B ChartQA).
- **Adjective-to-noun swap awkwardness (`_SWAP["math"]` mapping `"visual"`/`"written"` → `"typed text"`/`"image"`):** `0/150` in `coding_v5`, `0/190` in 3B Math, **`2/280`** in passed 7B Math (`gsm8k-image-L0-0104`: `"a typed text representation"`; `gsm8k-image-L0-0019`: `"a clear, image problem"`).
- **Scientific significance for `results_v5/analysis_dev/` `[Inferred]`:** Because `flip` retains topic-anchored justifications pointing back to `own_source` in ~`13%` of 7B Math cells while `para_flip` replaces the reliability sentence cleanly (`"I consider the image more reliable."`), this directly helps explain why dev 7B Math showed `flip − own = +45.7 pp` vs `para_flip − para = +66.8 pp` (`+21.1 pp` larger on the clean matched pair; [results_v5/README.md](<file:///c:/Thesis/Important/Thesis/Causal%20Conflict%20Verbalization%20and%20Source%20Arbitration/Experiment/results_v5/README.md#L73>)), validating pre-freeze **D2**.

---

## 5. Cross-File Audit Against Each Target Script & Directory `[Verified]`

### 5.1 [sample_v5_for_coding.py](<file:///c:/Thesis/Important/Thesis/Causal%20Conflict%20Verbalization%20and%20Source%20Arbitration/Experiment/sample_v5_for_coding.py>)

1. **`px501k` glob collision (line 407):** `glob.glob(os.path.join(args.input_dir, "*_donor_*.jsonl"))` now matches **8 files** in `results_v5/` instead of 6 (`v5dev_chartqa_px501k_donor_qwen25*.jsonl`, which differ from `200704` on `73/120` 3B and `107/120` 7B rows). Running `sample` without explicit `--donor_files` shifts the RNG draw (`0/200` match with the already-coded CSVs!).
2. **Destructive overwrite risk (lines 421–426):** `cmd_sample()` unconditionally overwrites `coder_A_*.csv` and `coder_B_*.csv`. There is no `--keys_only` flag or overwrite guard to safely regenerate/refresh `KEY_*.csv` files without touching coded sheets.
3. **Coder-A-only evaluation bias (lines 332, 375–376):** `evaluate_verdicts()` computes `human = a_lbl or b_lbl` and `evaluate_flips()` computes `g = ga if ga is not None else gb`. Thus `parser_accuracy_overall` and `grammatical_rate` silently ignore Coder B whenever Coder A is non-empty, with no option for consensus-only, Coder B, or an adjudicated CSV.
4. **Missing prevalence-robust agreement (lines 297–305):** `cohens_kappa()` returns `0.0` when one rater is `100%` constant `1` and the other has one `0`, and does not report Gwet's AC1 or PABAK.
5. **Sampling misalignment with actual transplanted items (lines 211–258):** `build_flip_samples()` evaluates `tp.make_variants()` on single `(id, order)` rows without filtering by competency or both-order survival, and stratifies evenly across `(regime, order)`. Consequently, `3B` got `29` ChartQA flips vs `31` Math flips (almost 50/50 despite ChartQA being exploratory with only `5` surviving 3B items!), and overall only **`80/200` (`40.0%`)** of coded verdict rows and **`53/150` (`35.3%`)** of coded flip rows (`14` 3B Math, `10` 3B ChartQA, `29` 7B Math) actually belong to items that entered `results_v5/*_tp_*.jsonl`. *(Not a bug for validating parser/flipper generality, but worth noting accurately in the thesis—only `43` of the `150` flips come from confirmatory 3B/7B Math transplanted items.)*

### 5.2 [preflight_v5.py](<file:///c:/Thesis/Important/Thesis/Causal%20Conflict%20Verbalization%20and%20Source%20Arbitration/Experiment/preflight_v5.py>)

1. **Current status:** `python -B Experiment/preflight_v5.py --json` passes in dev mode (`ok: true`, `errors: []`, `8/8` scripts hashed, `0` git-tracked `*KEY_*` files) at `HEAD = 418aa82`, with `0` modified tracked files (only untracked `Thesis/docs/Archive/Antigravity Audit.md` and gitignored `KEY_*.csv`) and `prereg_tag: null`.
2. **Cross-OS CRLF/LF hash bug (lines 169–174, 211–214):** `_sha256_file()` hashes raw bytes on Windows (CRLF), while Colab/Linux manifests in `results_v5/*.manifest.json` recorded LF bytes. Running `--check_manifests` on Windows produces **84 false-positive hash mismatch errors across all 20 manifests**, whereas normalizing `\r\n → \n` matches **100%** of recorded hashes (`transplant_v5.py`, `harness_v5.py`, `score_v5.py`, `harness_v4.py`, `score_v4.py`).
3. **No human-coding freeze gate:** `run_preflight(phase="confirm")` checks prereg text pins, scripts, git tag, and `*KEY_*` non-tracking, but does **not** verify that `coding_v5/evaluation_v5.json` exists or passed the §8 coding gate.

### 5.3 [harness_v5.py](<file:///c:/Thesis/Important/Thesis/Causal%20Conflict%20Verbalization%20and%20Source%20Arbitration/Experiment/harness_v5.py>)

- Donor generation (`donor_requests()` producing `donor` + `free_binding`), `base_correct(..., parser="structured")`, and `verdict_nll` span scoring align cleanly with `coding_v5` and `results_v5`.
- Two open freeze items already enforced/tracked in `harness_v5.py`: `CONFIRM_MAX_PIXELS["chartqa"]` ([harness_v5.py](<file:///c:/Thesis/Important/Thesis/Causal%20Conflict%20Verbalization%20and%20Source%20Arbitration/Experiment/harness_v5.py#L51>)) is still provisional (`200704` vs `501760`), and `validate_confirm_config()` ([harness_v5.py](<file:///c:/Thesis/Important/Thesis/Causal%20Conflict%20Verbalization%20and%20Source%20Arbitration/Experiment/harness_v5.py#L820-L832>)) will refuse `--phase confirm` until the working tree is clean and tagged `prereg-v5`.

### 5.4 [analyze_v5.py](<file:///c:/Thesis/Important/Thesis/Causal%20Conflict%20Verbalization%20and%20Source%20Arbitration/Experiment/analyze_v5.py>)

- **Validated dependency:** `manipulation_check()` ([analyze_v5.py](<file:///c:/Thesis/Important/Thesis/Causal%20Conflict%20Verbalization%20and%20Source%20Arbitration/Experiment/analyze_v5.py#L656>)) directly calls `sc.stated_reliable_source(verb, regime=r.get("regime"))`, which `coding_v5` now validates at **`100.0%` (`168/168`)** across all confirmatory 3B and 7B rows.
- **Minor parser inconsistency (line 660–662):** `manipulation_check()` calls `sc.behavioural_source(..., allow_math_fallback=True)` (which resolves to **`lenient`**, not `HEADLINE_PARSER = "structured"`), whereas `sample_v5_for_coding.py` line 179 uses `parser="structured"`. Quantified on dev `results_v5/`:
  - 3B Math `donor`: `76.9%` (`n=281`, lenient) vs `77.7%` (`n=233`, structured); `free_binding`: `94.4%` (`n=213`) vs `94.1%` (`n=186`).
  - 7B Math `donor`: `94.0%` (`n=332`, lenient) vs `94.5%` (`n=311`, structured); `free_binding`: `98.4%` (`n=316`) vs `98.3%` (`n=291`).
  - Substantively identical (`≤ 0.8 pp`), but worth aligning to `parser=HEADLINE_PARSER` for internal consistency with D3.

---

## 6. Recommended Next Steps (Before Tagging `prereg-v5`)

### Priority 1 — Required before `prereg-v5` freeze

1. **Generate `evaluation_v5.json` & record formal adjudication:**
   - Run `python Experiment/sample_v5_for_coding.py evaluate --out_dir Experiment/coding_v5` to save the raw pre-adjudication `evaluation_v5.json` (`rep_disk == rep_reg` is verified `True`).
   - Record an explicit adjudication table/note for the **3 canonical verdict disagreements** (`V0093`, `V0103` → `neither`; `V0177` → `unclear`, yielding **`99.5%` overall / `100.0%` confirmatory 3B+7B parser accuracy**) and the **5 flip disagreements** (`F0006`, `F0029`, `F0081`, `F0100`, `F0147`), reporting **Gwet's AC1 (`0.9722` / `0.9933`) and PABAK (`0.9467` / `0.9867`)** alongside Cohen's κ (`0.3258` / `0.0000`) to document the high-prevalence κ paradox cleanly against [PREREGISTRATION_VERDICT_TRANSPLANT.md](<file:///c:/Thesis/Important/Thesis/Causal%20Conflict%20Verbalization%20and%20Source%20Arbitration/Docs/PREREGISTRATION_VERDICT_TRANSPLANT.md#L558>) §8.
2. **Fix [sample_v5_for_coding.py](<file:///c:/Thesis/Important/Thesis/Causal%20Conflict%20Verbalization%20and%20Source%20Arbitration/Experiment/sample_v5_for_coding.py>) hazards, evaluation bias & refresh stale `beh_source` cells:**
   - Exclude `*_px501k_*` from the default `*_donor_*.jsonl` glob (line 407) so running `sample` on `results_v5/` never pulls duplicate ChartQA resolution runs.
   - Add a `--keys_only` flag (or refuse to overwrite non-empty `coder_*` CSVs without `--force`) so `KEY_*.csv` files can be refreshed safely—which also updates the **5 stale `beh_source` cells** (`V0032`, `V0092`, `V0140`, `V0149`, `V0176`) in `KEY_verdicts_do_not_open.csv` to match post-`328c8af` `score_v5.py`.
   - Fix `evaluate_verdicts()` / `evaluate_flips()` so they do not silently score against Coder A alone (`a_lbl or b_lbl`, `ga if ga is not None else gb`)—report Coder A, Coder B, consensus-only (and optional `--adjudicated` CSV), plus Gwet's AC1 & PABAK.
3. **Clean minor defects in the committed coder CSVs & docs:**
   - Trim the `21` leading spaces (`' text'` / `' image'`) in [coder_B_verdicts.csv](<file:///c:/Thesis/Important/Thesis/Causal%20Conflict%20Verbalization%20and%20Source%20Arbitration/Experiment/coding_v5/coder_B_verdicts.csv>), strip UTF-8 BOM, and restore the `7` Excel-corrupted read-only text cells (`V0029`, `V0059`, `V0076`, `V0114`, `V0117`) in both `coder_A_verdicts.csv` and `coder_B_verdicts.csv` from `KEY_verdicts_do_not_open.csv` (leaving every `coder_*` label and note intact).
   - Fix `encoding='utf-8'` → `encoding='utf-8-sig'` in [HUMAN_CODING_INSTRUCTIONS_v5.md](<file:///c:/Thesis/Important/Thesis/Causal%20Conflict%20Verbalization%20and%20Source%20Arbitration/Experiment/coding_v5/HUMAN_CODING_INSTRUCTIONS_v5.md#L181>) and update stale `"0 filled rows"` text in [HUMAN_CODING_INSTRUCTIONS_v5.md](<file:///c:/Thesis/Important/Thesis/Causal%20Conflict%20Verbalization%20and%20Source%20Arbitration/Experiment/coding_v5/HUMAN_CODING_INSTRUCTIONS_v5.md#L56>), [Experiment/README.md](<file:///c:/Thesis/Important/Thesis/Causal%20Conflict%20Verbalization%20and%20Source%20Arbitration/Experiment/README.md#L75>), and [Experiment/results_v5/README.md](<file:///c:/Thesis/Important/Thesis/Causal%20Conflict%20Verbalization%20and%20Source%20Arbitration/Experiment/results_v5/README.md#L79>).

### Priority 2 — Optional targeted code cleanups before freeze

4. **`score_v5.stated_reliable_source()` coordinate-clause fix:** Fix the `F0081` / `gsm8k-image-L0-0162` bug (where `, and` / `, but` precedes `"the source that is more reliable is <noun>"`) with a regression test verifying all 29 valid 7B subordinate-clause sentences remain unchanged. *(Zero impact on confirmatory 3B/7B dev rows; affects 3 diagnostic 2B rows.)*
5. **`preflight_v5._sha256_file()` CRLF normalization:** Normalize `\r\n → \n` (or accept LF digest) when checking Linux-generated manifests on Windows, eliminating the 84 false-positive hash mismatch errors under `--check_manifests`, and optionally gate `confirm` preflight on `coding_v5/evaluation_v5.json`.
6. **`analyze_v5.manipulation_check()` parser alignment:** Change `allow_math_fallback=True` ([analyze_v5.py](<file:///c:/Thesis/Important/Thesis/Causal%20Conflict%20Verbalization%20and%20Source%20Arbitration/Experiment/analyze_v5.py#L661>)) to `parser=HEADLINE_PARSER` (`"structured"`) for consistency with D3 and `sample_v5_for_coding.py`.
7. **Lock remaining freeze items:** Lock `CONFIRM_MAX_PIXELS["chartqa"]` in [PREREGISTRATION_VERDICT_TRANSPLANT.md](<file:///c:/Thesis/Important/Thesis/Causal%20Conflict%20Verbalization%20and%20Source%20Arbitration/Docs/PREREGISTRATION_VERDICT_TRANSPLANT.md>) §3.4 & [harness_v5.py](<file:///c:/Thesis/Important/Thesis/Causal%20Conflict%20Verbalization%20and%20Source%20Arbitration/Experiment/harness_v5.py#L51>), re-run `unittest` and `preflight_v5.py`, then commit and tag `prereg-v5`.

### Does NOT need fixing

- **`.gitignore`:** Already ignores `Experiment/coding_*/KEY_*.csv` (`git check-ignore -v` verified).
- **`KEY_flips_do_not_open.csv`:** Already `100.0%` aligned across all `150 × 11` cells.
- **Re-coding by Utsha or Rafiul:** Not needed — verdict reliability passes comfortably (`κ = 0.8803` raw / `0.9783` canonical), and confirmatory 3B+7B parser accuracy is `100.0%` (`168/168`).
