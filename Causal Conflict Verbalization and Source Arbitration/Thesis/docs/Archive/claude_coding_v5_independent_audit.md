# Independent Forensic Cross-Audit — `Experiment/coding_v5/` (Claude Opus 5.5)

## 1. Metadata & Executive Summary

| Field | Value |
|---|---|
| Date | `2026-11-20` |
| Auditor | Claude Opus 5.5 (Claude Code, desktop app), independent of the Antigravity audit |
| Audited commit | `418aa82` (`main`); restored `KEY_*.csv` untracked + gitignored |
| Mode | Strictly read-only. The only file written is this report. No `sample`/`evaluate` run wrote to `Experiment/`; all analysis was inline `python -B -c` / `python -B -` heredocs; `git status` was unchanged before and after (`?? Thesis/docs/Archive/Antigravity Audit.md` only). |
| Environment | Windows 11, Python 3.14.6, `core.autocrlf=true` (system gitconfig), no CUDA |

### 1.1 Anti-anchoring disclosure (read this first)

The protocol asked that `Antigravity Audit.md` not be read until Phase 1 was finished. **That condition was not met, and not by choice:** the file was attached to the session through the `@` mention in the request, so its full text was in my context before I ran any check. Phase 1 is therefore **not blind**. What I did to limit anchoring:

- Every number in §2 comes from Python/CLI output I ran on primary files (git blobs, CSVs, JSONLs, code). None was copied from the Antigravity text.
- I went for the claims most likely to be wrong (line-ending provenance, the κ explanation, the explanation of the dev gap, blinding) and for things Antigravity did not test.
- Where my numbers match Antigravity's exactly, treat that as **reproduction**, not independent discovery.

### 1.2 Verdict on coding-gate readiness

**[Verified] The verdict-coding half of the §8 gate passes.** Raw 7-class κ = `0.8803`, canonical κ = `0.9783` (N = 200). After adjudication, parser accuracy is `168/168` on all 3B+7B rows (Wilson 95% lower bound `0.978`) and `199/200` overall. The one parser error (`V0177`) is on the diagnostic 2B model.

**[Verified] The flip-coding half does not pass §8 as written.** §8 (prereg L558) says "requires inter-coder `κ ≥ 0.80`" without saying which ratings it covers, and L560 says "If a gate fails, the run stops." Flip κ is `0.3258` (grammatical) and `0.0000` (intended source). Raw agreement is 97.3% / 99.3%, Gwet's AC1 is `0.9722` / `0.9933`, and PABAK is `0.9467` / `0.9867`. This has to be fixed with a **logged pre-freeze amendment to §8**, not just a footnote; I rank it **P0** (see §5).

**[Verified] Key status.** Both restored keys equal their `5b57529` blobs after line-ending normalisation. Both regenerate exactly from the 6 main donor files: flips 150 × 11 cells identical, verdicts identical except 5 stale `beh_source` cells. `evaluate_verdicts`/`evaluate_flips` give identical output on the disk keys and on freshly regenerated keys.

**[Verified + Inferred] Points Antigravity got wrong or left out**, detailed in §3–§4:

1. **The CRLF claims are wrong.** The committed coder blobs contain **0 CRLF**. All CRLFs are working-tree artefacts of `core.autocrlf=true` and appear equally in the KEY files.
2. **The gap explanation is overstated.** Topic-anchored flips explain only about **6 of the 21.1 pp** binding `para_flip−para` vs `flip−own` gap in 7B dev. About 17 pp remains in cells with no anchoring, and under non-binding the gap reverses sign.
3. **The flip κ collapse is not purely a prevalence effect.** All 5 grammatical disagreements run the same way (A=0, B=1), and κ equals its marginal-bounded maximum κ_max. Coder B marked 150/150 flips as naming the intended source, including the truly inverted `F0081`.
4. **A larger 2B failure class was missed: "two images" positional verdicts.** 53 2B Math donor rows (50 of which pass all edit gates) have an `own_source` that rests on "the first image" when the model calls both sources images. `F0006`, `F0029`, `F0100` and `V0177` belong to this class. Diagnostic-only, and 2B has 0 competent items, so it never reaches transplant.
5. **Regenerating the keys after a parser fix would silently re-draw the flip sample**, because the flip pool depends on the parser. A `--keys_only` refresh needs an identity assertion.
6. **The KEYs were never truly "absent" during coding.** They stay retrievable from git history (`f802951`, `42f4c55`, `5b57529`). Blinding rested on coder compliance.
7. **§5.3 documents `versus`/`vs.` as contrast foils, but `_FOIL_BEFORE` lacks them.** The gap is latent (0 occurrences in the dev data), yet `"The typed text, versus the image, is more reliable."` parses as `image`.
8. **ChartQA raw-label κ is below 0.80** (`0.7019` on all ChartQA; `0.6632` on 3B/7B ChartQA). The cause is a systematic coder convention on bare answers (A: `neither` 14/14; B: `unclear` 14/14), which points to a gap in the codebook.

---

## 2. Phase 1 — Independent Audit Findings

### 2.1 Files, encoding, git and restored-key provenance

**Git state [Verified]**

- `git status --short --ignored=matching` lists `?? Thesis/docs/Archive/Antigravity Audit.md`, plus ignored `Experiment/__pycache__/` and both `KEY_*.csv`.
- `git ls-files -- '*KEY_*' '*/KEY_*'` returns nothing (no tracked keys).
- `git check-ignore -v`: both keys match `.gitignore:1:Experiment/coding_*/KEY_*.csv`.
- Coding history: `f802951` and `42f4c55` added the keys, `328c8af` (`2026-11-16 00:47 +0600`) deleted them, Coder B committed `057a6c3` (`2026-11-19 00:47`), Coder A committed `6b75f10` (`2026-11-18 23:02`). **[Verified] Both KEY blobs remain retrievable**, e.g. `git show 5b57529:./coding_v5/KEY_verdicts_do_not_open.csv`.
- `preflight_v5.run_preflight("dev")` gives `ok: true`, `errors: []`, `git_dirty: true`. The untracked audit `.md` sets the dirty flag. That is harmless in dev, but the tree must be clean before the confirm phase (§5).

**Key blob identity [Verified]**

| File | `git hash-object` (disk) | `5b57529` blob | Raw bytes equal? | Equal after `\r\n→\n`? |
|---|---|---|---|---|
| `KEY_verdicts_do_not_open.csv` | `01b88f9bd8e5…` | `01b88f9bd8e5…` | **No** (disk has 1,640 CRLF, blob 0) | **Yes** |
| `KEY_flips_do_not_open.csv` | `3d6c87e86f3e…` | `3d6c87e86f3e…` | **No** (151 CRLF vs 0) | **Yes** |

`git hash-object` matches only because `autocrlf=true` normalises line endings before hashing. The restored disk files are CRLF checkouts of the LF blobs.

**Byte-level encoding [Verified]**

| File | Committed blob (`HEAD`) | Working tree |
|---|---|---|
| `coder_A_verdicts.csv` | BOM, **0 CRLF**, 1,640 LF | BOM, 1,640 CRLF |
| `coder_B_verdicts.csv` | BOM, **0 CRLF**, 1,640 LF | BOM, 1,640 CRLF |
| `coder_A_flips.csv` / `coder_B_flips.csv` | BOM, **0 CRLF**, 151 LF | BOM, 151 CRLF |
| `KEY_*` (5b57529) | no BOM, 0 CRLF | no BOM, all CRLF |
| `CODEBOOK_v5.md` | — | no BOM, CRLF |

`git ls-files --eol coding_v5/` reports `i/lf w/crlf` for every tracked file. **So the coders' saves added a UTF-8 BOM but no CRLF to the committed content.** History detail: at `057a6c3`, Coder B's sheets already had a BOM; Coder A's sheets were still pristine and gained the BOM in `6b75f10`.

**Read-only column parity [Verified]** (parsed from blobs with `utf-8-sig`)

- Coder A vs Coder B: **0 differences** on every read-only column, in both sheets. Row order and headers are identical, with no sorting or deletion.
- Coders vs pristine sheets (`5b57529`): **flips 0 differences**. **Verdicts: 7 cell differences, identical in A and B**:

| `sample_id` | Column(s) | Pristine | Coder sheets | Mechanism |
|---|---|---|---|---|
| `V0029` (`gsm8k-image-L0-0054`) | `full_text` | `÷` (U+00F7) | `Ã·` (U+00C3 U+00B7) | UTF-8 bytes decoded as cp1252, then re-saved as UTF-8 |
| `V0059` (`gsm8k-image-L0-0077`) | `full_text` | `÷` | `Ã·` | same |
| `V0114` (`gsm8k-image-L0-0112`) | `full_text` | `×` (U+00D7) | `Ã—` (U+00C3 U+2014) | same (0x97 → em dash in cp1252) |
| `V0076` (ChartQA `21`) | `verbalization_text`, `full_text` | `20.4%` | `20.40%` | Excel number reformatting |
| `V0117` (ChartQA `29`) | `verbalization_text`, `full_text` | `3.0` | `3` | Excel number reformatting |

`evaluate()` never reads these columns, so scoring is unaffected [Verified].

- Coder entries: A has 0 blanks, 0 whitespace issues and 0 notes. B has 0 blanks, but **21 labels carry a leading space** (`' text'` × 16, `' image'` × 5), plus 10 notes (`V0001` `"."`; nine variants of "doesn't identify any preferred source", three spelt "preffered"). `evaluate_*` strips whitespace [Verified].

**Deterministic regeneration (`seed=42`, `n_donors=200`, `n_flips_per_model=50`) [Verified]**

| Input | Donor rows | Verdict key diffs vs `5b57529` KEY | Flip key diffs |
|---|---|---|---|
| 6 main `200704` donor files | 2,760 | `beh_source` **5**; every other column 0 | **0** across all 10 columns |
| Default glob `*_donor_*.jsonl` (8 files, includes `px501k`) | 3,000 | `item_id` **198**, `model_id` 118, `predicted_stated_source` 143, `full_text` 199, … | **0** |

- The 5 stale `beh_source` cells are `V0032`, `V0092`, `V0140`, `V0149` (`Final answer: N`) and `V0176` (`The final answer is: 10.`): KEY says `neither`, current code says `text`/`image`/`text`/`image`/`text`. The cause is the `_MATH_FINAL_ANSWER` edit in `328c8af` (`score_v5.py:202–205`), which is the only `score_v5.py` change in `5b57529..HEAD`. **Every one of the 20 `results_v5` manifests records `score_v5.py` = `3f6bf3e96755…` (HEAD), while `5b57529`'s version is `ff7a587a727e…`.** So the dev rerun used the new parser, and the keys were generated with the old one.
- Why the flips survive the 8-file glob: `build_flip_samples` deduplicates on `(model_id, regime, id, order)` and keeps the first occurrence. `sorted(glob)` places `v5dev_chartqa_donor_*` before `v5dev_chartqa_px501k_donor_*`, so every px501k donor is skipped and the candidate pool, and therefore the RNG draw (`seed+101`), is unchanged. `build_verdict_samples` does not deduplicate, so the extra 240 rows shift every draw.
- `evaluate_verdicts`/`evaluate_flips` on disk keys == on freshly regenerated 6-donor keys: **`True`** (`beh_source` is never read).
- Donor parity with `archive/results_v5_Prev_backup/`: **2,760/2,760 rows, 0 `full_text` differences**, keyed on `(model, id, order, family, key)`.

**Codebook and validation command [Verified]**

- `CODEBOOK_v5.md` equals `sample_v5_for_coding.CODEBOOK_MD` as text; the bytes differ only by CRLF.
- The `HUMAN_CODING_INSTRUCTIONS_v5.md:181` snippet, run verbatim, prints `bad: 0` × 4. That is correct for the label columns, but `encoding='utf-8'` leaves the first header as `'﻿sample_id'`. It works only because the snippet never reads `r['sample_id']`; any extension that does will raise a `KeyError`.

### 2.2 Part 1 — verdict coding (N = 200)

**Stratification vs §8 [Verified]**

| Block | Rows | Detail |
|---|---|---|
| Confirmatory Math | 120 | 3B 60 + 7B 60; each 40 `donor` / 20 `free_binding`; each order 30/30 |
| 3B/7B ChartQA | 48 | each model 16 `donor` / 8 `free_binding`; each order 12/12 |
| Diagnostic 2B | 32 | Math 16 + ChartQA 16; each 8/8 family and 8/8 order |

This matches §8 (60% / 24% / 16%).

Completeness and vocabulary: 0 blanks, 0 out-of-regime labels for either coder. Label counts: A = `text` 96, `image` 35, `unclear` 21, `report` 19, `neither` 18, `chart` 11. B = `text` 94, `image` 36, `unclear` 34, `report` 19, `chart` 11, `neither` 6. Parser = `text` 94, `image` 36, `absent` 35, `report` 19, `chart` 11, `undetermined` 5. The stored `predicted_stated_source` equals the current `stated_reliable_source` on 200/200.

**Agreement and parser accuracy [Verified]** (my own κ/AC1/PABAK code; AC1/PABAK use K = 7 raw, K = 5 canonical label strings, K = 3 strict {S1, S2, NV})

| Subset | N | Raw agree / κ / AC1 | Canonical (code's 5 strings) agree / κ | Strict 3-way κ / AC1 / PABAK | Parser vs A | vs B | vs consensus | Adjudicated |
|---|---:|---|---|---|---|---|---|---|
| Overall | 200 | .9150 / **.8803** / .9036 | .9850 / **.9783** | .9742 / .9788 / .9775 | 197 | 200 | 197/197 | **199/200** |
| Conf 3B+7B Math | 120 | .9833 / **.9606** / .9821 | .9833 / .9606 | .9606 / .9789 / .9750 | 118 | 120 | 118/118 | **120/120** |
| All 3B+7B | 168 | .9167 / .8780 / .9060 | .9881 / .9823 | .9778 / .9837 / .9821 | 166 | 168 | 166/166 | **168/168** |
| Diagnostic 2B | 32 | .9062 / .8613 / .8944 | .9688 / .9443 | .9439 / .9567 / .9531 | 31 | 32 | 31/31 | **31/32** |
| ChartQA (3 models) | 64 | .7812 / **.7019** / .7519 | 1.000 / 1.000 | 1.000 | 64 | 64 | 64/64 | 64/64 |
| 3B+7B ChartQA | 48 | .7500 / **.6632** / .7164 | 1.000 / 1.000 | 1.000 | 48 | 48 | 48/48 | 48/48 |

- `evaluate_verdicts()` output: `parser_accuracy_overall = 0.985` (this is Coder A), `raw_exact_match_overall = 0.795`. With the coders swapped it gives `1.0` / `0.80`. **The function's headline accuracy depends on which file is passed as "A"** (`sample_v5_for_coding.py:332`).
- Precision of the 100% claims [Inferred]: 120/120 has a Wilson 95% lower bound of 0.969 and 168/168 one of 0.978. A ~2–3% true error rate on confirmatory rows is not ruled out.

**Every disagreement row, adjudicated [Verified text; adjudication = my judgement against the codebook]**

| IDs | Model / family / order | A | B | Parser | Text | Adjudication |
|---|---|---|---|---|---|---|
| `V0002 V0013 V0030 V0058 V0071 V0076 V0079 V0082 V0117 V0161 V0168 V0171 V0179 V0193` (14) | ChartQA, 3B ×12, 2B ×2 | `neither` | `unclear` | `absent` | Bare answers only (`4.10 million U.S. dollars`, `20.4%`, `Yes`, `3.0`, …) | `neither`, i.e. a complete answer "without stating which is more reliable" (instructions L80). It is not a truncated fragment (L82/L108). Either label maps to `no_verdict`; this is a **codebook gap, not noise**: each coder applied one rule consistently (A 14/14 `neither`, B 14/14 `unclear`). |
| `V0093` (`gsm8k-image-L0-0020`), `V0103` (`-0103`) | 3B Math `free_binding` `text_first` | `text` | `neither` | `absent` | "…I will solve the problem from the typed text." No "reliable" anywhere. | `neither` (instructions L104, explicit example). A erred and was self-inconsistent: A coded the identical `V0194` as `neither`. Parser **correct**. |
| `V0177` (`svamp-image-L0-0022`) | 2B Math `donor` `text_first` | `unclear` | `image` | `image` | "The two images present different problems. The first image asks … girls and boys …, while the second image asks … Dave … apps. Therefore, the source I consider more reliable is the first image…" | `unclear` (instructions L82/L107: a positional reference that does not identify the modality). Parser **wrong**. Ground truth: the 3B and 7B donors for the same item both say "**The typed text** is … about the number of girls and boys", so the model's "first image" is the typed text, and even an order-aware reading would give `text`, not `image`. |

**Blind-spot scan of all-agree rows [Verified]**

I printed the reliability sentence of all 46 rows where A, B and the parser agree on a source and the sentence contains contrast or negation words (`while`, `not`, `less`, `but`), several "reliable" sentences, or comes from 2B. Every one names the source correctly, including the second-sentence downgrades in `V0091`/`V0122` ("The image … is less reliable"), `V0186` (subordinate `Given that the chart…`) and `V0165` (`…same problem, but the typed text is more reliable`). All `undetermined`/positional rows (`V0033`, `V0097`, `V0102`, `V0120`, `V0160`) are correctly `no_verdict` for all three raters. **No hidden parser error other than `V0177`.**

**Blinding [Verified facts / Inferred conclusion]**

- B agrees with the parser canonically 200/200.
- The parser has exactly one adjudicated error, and it is a case where a literal reader would naturally write `image`. So an honest, careful coder would be expected to match the parser on about 199–200 rows. **B's 100% match is fully consistent with independent coding and is not evidence of key access** [Inferred].
- It is not proof of independence either. The keys sat in public-branch history during coding, so the blinding is procedural (honour-based), not technical. Organic signals of independence: B's leading spaces, typo'd notes, the `unclear` convention on bare answers (the parser says `absent`), and B following instruction L104 on `V0093`/`V0103`.

### 2.3 Part 2 — flip coding (N = 150)

**Stratification [Verified]**

- By model: 3B 60, 7B 60, 2B 30. This matches §8 (40/40/20).
- Within each model, strata are drawn round-robin over `(regime, order)`, which **exhausts the small ChartQA pools**: 3B ChartQA takes 29 of a 29-candidate pool, 7B ChartQA 10 of 10, 2B ChartQA 3 of 3. That leaves 3B Math 31, 7B Math 50, 2B Math 27.
- Coded rows on items that passed the dev transplant gates: verdicts **80/200**, flips **53/150** (3B Math 14, 7B Math 29, 3B ChartQA 10, the last being all 10 passed 3B ChartQA cells). Only **43/150** flips come from confirmatory-Math items that were actually transplanted.

**Rates and agreement [Verified]** (κ_max is the largest κ attainable given the two raters' marginals)

| Subset | N | Gram A / B | Gram agree / κ / κ_max / AC1 / PABAK | Src A / B | Src agree / κ / AC1 / PABAK |
|---|---:|---|---|---|---|
| All | 150 | 145 / 149 | .9733 / **.3258** / .3258 / **.9722** / .9467 | 149 / 150 | .9933 / **.0000** / **.9933** / .9867 |
| Conf 3B+7B Math | 81 | 80 / 81 | .9877 / .0000 / .0000 / .9875 / .9753 | 81 / 81 | 1.000 / None / 1.000 / 1.000 |
| All 3B+7B | 120 | 119 / 120 | .9917 / .0000 / .0000 / .9916 / .9833 | 120 / 120 | 1.000 / None / 1.000 / 1.000 |
| Diagnostic 2B | 30 | 26 / 29 | .9000 / .3662 / .3662 / **.8820** / .8000 | 29 / 30 | .9667 / .0000 / .9655 / .9333 |
| 3B | 60 | 60 / 60 | 1.000 / None | 60 / 60 | 1.000 / None |
| 7B | 60 | 59 / 60 | .9833 / .0000 | 60 / 60 | 1.000 / None |
| ChartQA | 42 | 42 / 42 | 1.000 / None | 42 / 42 | 1.000 / None |

**Why κ behaves this way [Verified arithmetic]**

κ = (p_o − p_e) / (1 − p_e) with p_e = p_A·p_B + (1−p_A)(1−p_B).

- *Intended source:* B is constant (p_B = 1), so p_e = p_A = 149/150 = p_o, giving κ = 0 exactly, whatever the 99.3% raw agreement. `cohens_kappa()` (`sample_v5_for_coding.py:297–304`) returns `None` only when p_e ≥ 1, which requires both raters to be constant on the same class.
- *Grammatical:* the contingency table is (1,1) = 145, (0,0) = 1, (0,1) = 4, (1,0) = 0, giving p_e = .9604 and κ = .3258.
- κ_max = κ in every subset. Because **every disagreement is A=0 / B=1**, the marginals themselves cap κ. This combines a prevalence effect with a **rater bias effect**: B almost never rejects a flip (1/150 on grammar, 0/150 on source). AC1/PABAK correctly show the two coders agree on almost everything, but agreement here carries little information about whether defects get *detected*: B detected 1 of the 5 defects A flagged, and missed the real inversion `F0081` [Inferred].

**Every flip with a 0 [Verified text]**

| ID | Model / order / item | A (g,s) | B (g,s) | What happens | My adjudication |
|---|---|---|---|---|---|
| `F0006` | 2B Math `text_first` `gsm8k-image-L0-0133` | 0,1 | 0,1 | "two images … the first image, and the source that is more reliable is the first image" → "…the first typed text … the first typed text" | g = 0 ("first typed text" is ungrammatical for a single text), s = 1. **The own source is itself unidentifiable** (positional "first image" inside a two-images frame). |
| `F0029` | 2B Math `text_first` `-0069` | 0,1 | 1,1 | "the first image, as it … asked in the image" → "the first typed text … in the typed text" | g = 0; s = 1; same positional class |
| `F0081` | 2B Math `text_first` `-0057` | 0,0 | 1,1 | Original verdict = **typed text**; parser reads `image` across `, and`; flip says "…more reliable is **the image**" while `intended_flip_source = text` | g = 0, **s = 0**. B is wrong. A real parser and Gate-2 inversion (§2.4). |
| `F0100` | 2B Math `text_first` `-0049` | 0,1 | 1,1 | "Richard's image" → "Richard's typed text" inside a two-images frame | g = 0 (defensible), s = 1; positional/hallucination class |
| `F0147` | **7B** Math `text_first` `gsm8k-image-L0-0118` | 0,1 | 1,1 | S2: typed text = salary, image = containers; flipped S3: "The image is more reliable as it provides … salary and percentage increase" | Under the instructions' literal "factual oddity → 1" rule (L129–132) B's 1 is defensible; under the codebook's "internally coherent" wording (`CODEBOOK_v5.md` Part 2 Q1) A's 0 is defensible. **A codebook gap: the instructions only cover within-sentence mirrored justifications, not cross-sentence contradictions.** Item not competent in 7B, so never transplanted. |

### 2.4 Structural scans over all donors and all passed transplant cells

**Reconstruction check [Verified]**

For every passed `(item, order)` cell I rebuilt `make_variants()` from the donor file and compared the `flip` text with the stored `tp` prefill (streamed, `nonbinding`/`dl`/`k=1` rows). **3B Math 190/190, 7B Math 280/280, 3B ChartQA 10/10 and px501k 3B ChartQA 2/2 match byte-for-byte.**

Gate reports: `conflict_tp_qwen2` 0 competent; `chartqa_tp_qwen2` 0 passed; `chartqa_tp_qwen25_7b` 0 passed (`gate_answer_leakage` 15, `too_many_swaps` 9); `chartqa_tp_qwen25` 5/13 = **38.5%** edit-gate pass (below the §8 60% threshold, so a ChartQA reading would be `NOT A READING`); `conflict_tp_qwen25` 95/95; `conflict_tp_qwen25_7b` 140/154 = 90.9%.

**(1) Clause crossing in `stated_reliable_source()`** (`score_v5.py:106–121`). `_CLAUSE_SPLIT` is checked only inside `prefix = s[:last_m.start()]`, never between `last_m.end()` and `"reliable"`.

- Over the 2,760 main donors, **38 rows** have a clause split in that gap: 7B Math 25, 7B ChartQA 4, 2B Math 9; 3B none.
- All 29 7B rows are correct as parsed. They are antecedent clauses such as "…from the image, as it is the more reliable source", "Given that the report…, I consider it more reliable", "The chart, being…, is…". A blanket "reject if any split in the gap" rule would break all 29 [Verified].
- 2B errors: `gsm8k-image-L0-0057` (`F0081`, `image` → should be `text`); `gsm8k-image-L0-0162` (`free_binding`, `undetermined` → should be `text`); `gsm8k-image-L0-0119` ("the source of the typed text is not specified, so I will consider Adrien's salary as the more reliable source", `text` → should be `undetermined`).
- A narrow fix that re-parses only the tail after the last `,\s*(and|but)\b` before "reliable" **changes exactly 2/2,760 rows** (`-0057` and `-0162`, both 2B) and leaves every 3B/7B row unchanged [Verified]. It does **not** fix `-0119`, which needs a `so`-clause or "is not specified" rule.

**(2) "Two images" positional verdicts (new, §4).** 53 2B Math donor rows (51 `donor`, 2 `free_binding`) get a source label even though the verbalization calls both sources "images" or names "first/second image/text". **50 of them pass every edit gate.** 0 such rows exist in 3B or 7B.

**(3) Unswapped post-verdict sentences** (verdict not last, and a later sentence names a source).

- **3/190 3B Math cells** [Verified], each directly contradicting the flipped verdict:
  - `gsm8k-image-L0-0046` (`image_first`): "The typed text is a hypothetical problem about ties…"
  - `-0084` (`text_first`): "The image is a statement about a football team's performance, which is not a mathematical problem."
  - `-0113` (`text_first`)
- 7B Math 0/280, 3B ChartQA 0/10. Among coded flips: `F0065` (2B), unflagged by both coders.

**(4) Cross-sentence topic anchoring** (pre-verdict sentence maps topics to sources; the verdict's justification reuses only the own-source topic words).

- My heuristic (stop-word filtered content words) flags **7B Math 31/280 (11.1%), 3B Math 12/190 (6.3%), 3B ChartQA 0/10, coded flips 11/150**.
- Spot-check precision: `gsm8k-image-L0-0067`, `-0116`, `svamp-image-L0-0030` and 3B `-0031` are clear contradictions; 7B `-0001` and 3B `-0048` are weak (shared word "real" only). Realistic estimate: about **9–11% of 7B and 5–6% of 3B passed cells** [Inferred].
- Coded examples: `F0147` (flagged by A), `F0134` (`svamp-image-L0-0007`, 7B, unflagged), `F0016`, `F0022`, `F0050`, `F0060`, `F0094`, `F0099`, `F0014`.

**(5) Adjective-to-noun swaps** (`_SWAP["math"]`). **2/280 7B cells**: `gsm8k-image-L0-0104` ("a typed text representation") and `-0019` ("a clear, image problem"). 3B 0/190, coded 0/150.

**(6) Relationship to `analysis_dev`.** I recomputed per cell, with `analyze_v5.behaviour_table(parser="structured")` and `beh_diff`, which reproduces the dev numbers exactly:

| Model / binding | All: flip−own / para_flip−para / gap | Anchored cells (n) | Non-anchored cells (n) |
|---|---|---|---|
| 7B binding | .457 / .668 / **.211** | .323 / .871 / .548 (31) | .474 / .643 / **.169** (249) |
| 7B non-binding | .311 / .254 / **−.057** | .065 / .194 / .129 (31) | .341 / .261 / −.080 (249) |
| 3B binding | .505 / .605 / .100 | .750 / .750 / .000 (12) | .489 / .596 / .107 (178) |
| 3B non-binding | .353 / .389 / .037 | .250 / .417 / .167 (12) | .360 / .388 / .028 (178) |

On a cell-weighted basis, anchored cells contribute about **31/280 × .548 ≈ 6.1 pp of the 21.1 pp** 7B binding gap. About 16.9 pp remains in non-anchored cells.

[Inferred] Anchoring weakens the 7B flip effect (.323 vs .474) and is a real contributor, but **it is not the main explanation for the gap**: under non-binding, `flip−own` exceeds `para_flip−para`. Other candidates are the template's short, explicit wording and the cell-specific `para` baseline. Dev, small n, descriptive only.

### 2.5 Pipeline and pre-freeze protocol

**`sample_v5_for_coding.py` [Verified]**

- L407: the default glob pulls in the px501k donors. Running without `--donor_files` scrambles 198/200 verdict rows.
- L421–426: `coder_*` and `KEY_*` are overwritten unconditionally, with no guard and no `--keys_only` option.
- L332 `human = a_lbl or b_lbl` and L375–376 `ga if ga is not None else gb`: Coder A takes precedence.
- L297–304: κ returns `0.0` when one rater is constant, and no AC1/PABAK/κ_max is reported.
- The flip pool (L222–225) depends on `make_variants().ok`, which depends on `score_v5`. **Any parser change followed by `sample` re-draws the flip sample**, and the verdict sample is parser-independent only in which rows it picks (new, §4).

**`preflight_v5.py` [Verified]**

- `--check_manifests` over all 20 manifests gives **84 hash-mismatch errors** on Windows, and **84/84 match after `\r\n→\n`** (`_sha256_file`, L169–174).
- There is no gate on `coding_v5/evaluation_v5.json` or on adjudication.
- The confirm phase requires a clean tree, which the two untracked audit `.md` files currently prevent.

**`analyze_v5.py` [Verified]** `manipulation_check()` L660–662 uses `allow_math_fallback=True` (lenient), whereas the headline parser is `HEADLINE_PARSER="structured"` (L112). Dev impact on "answer follows stated verdict":

| Model / family | Lenient | Structured |
|---|---|---|
| 3B `donor` | .769 (n = 281) | .777 (n = 233) |
| 3B `free_binding` | .944 (213) | .941 (186) |
| 7B `donor` | .940 (332) | .945 (311) |
| 7B `free_binding` | .984 (316) | .983 (291) |

**`harness_v5.py` / prereg [Verified]**

- `CONFIRM_MAX_PIXELS["chartqa"] = 200704` is still marked provisional (`harness_v5.py:49–52`; prereg §3.4 L224 "Open before `prereg-v5`").
- §5.3 L368 lists `versus`/`vs.` as foils, but `_FOIL_BEFORE` (`score_v5.py:62–65`) has neither. 0 dev occurrences, but `"The typed text, versus the image, is more reliable."` returns `image`.
- §8 L558–560: the κ gate is unscoped and fail-stops (see §1.2).

**Tests and stale docs [Verified]**

- `python -B -m unittest discover -s tests` ran 248 tests: **OK**. No test covers the coordinate clause, "two images", or `versus` cases (grep).
- Stale "not yet coded" / "0 filled rows" text: `Experiment/README.md` L8, L28, L75, L112, L122; `Experiment/results_v5/README.md` L79; `HUMAN_CODING_INSTRUCTIONS_v5.md` L56; `CLAUDE.md` L20.

---

## 3. Phase 2 — Adversarial Reconciliation vs `Antigravity Audit.md`

| # | Antigravity claim (section) | Status | Evidence / correction |
|---|---|---|---|
| 1 | All 4 sheets complete, 0 blanks, 0 invalid labels (§1) | **Confirmed** | §2.1–2.3 |
| 2 | Verdict raw 91.5% / κ .8803; canonical 98.5% / κ .9783; conf-Math 98.3% / .9606 (§1, §3.2) | **Confirmed** | identical |
| 3 | Parser accuracy A/B/adjudicated: 98.5/100/99.5 overall; 100% on 168 3B+7B (§1) | **Confirmed** | plus Wilson lower bounds .969 / .978 |
| 4 | Flip rates, agreement, κ .3258 / .0000, AC1 .9722 / .9933, PABAK .9467 / .9867 (§1, §4.1) | **Confirmed** | identical |
| 5 | 2B grammatical AC1 = `0.8805` (§4.1) | **Disputed / Corrected** | π = 55/60, p_e(AC1) = .15278 gives AC1 = **.8820**; PABAK .8000 confirmed |
| 6 | κ "collapse" is the prevalence paradox (§4.1) | **Nuanced** | Also a rater-bias effect: all disagreements A=0/B=1 and κ = κ_max; B rejected 0/150 on intended source, including the real inversion `F0081` |
| 7 | Restored KEY blobs `01b88f9bd8e5` / `3d6c87e86f3e`, "no BOM" (§1, §2.1) | **Confirmed (qualified)** | Equal only after LF normalisation; disk files are CRLF (`autocrlf`) |
| 8 | 5 stale `beh_source` cells with the listed IDs/values; `evaluate` unaffected (§2.3) | **Confirmed** | Root cause sharpened: manifests pin HEAD `score_v5` (`3f6bf3e9`), keys used `ff7a587a` |
| 9 | `px501k` glob scrambles 198/200 verdict rows; flips survive via dedup + alphabetical order (§1, §2.3) | **Confirmed** | identical mechanism |
| 10 | `rep_disk == rep_reg` is `True` (§2.3) | **Confirmed** | ran independently |
| 11 | Donor 0-diff vs archive; 200/150 regeneration identity (§2.2) | **Confirmed** | 2,760/2,760 |
| 12 | A vs B read-only 0 diffs; 7 identical Excel content mutations (§1, §2.2) | **Confirmed** | code-point evidence in §2.1 |
| 13 | "All 4 committed coder CSVs now have … CRLF (1,640 / 151)"; "137 `full_text` cells converted `\n` to `\r\n`" (§2.2) | **Disputed / Corrected** | Committed blobs have **0 CRLF** (`git ls-files --eol`: `i/lf`). CRLF exists only in the working tree, from `core.autocrlf=true`, and is equally present in the KEYs. (Antigravity also gives "137" in §2.2 and "140" in §2.3 for the same artefact.) **BOM: confirmed.** |
| 14 | B: 21 leading spaces (16 text / 5 image), 10 notes with typos (§2.2) | **Confirmed** | |
| 15 | Validation snippet uses `utf-8` not `utf-8-sig`; prints `bad: 0` only because `sample_id` is never read (§2.2) | **Confirmed** | header is `'﻿sample_id'` |
| 16 | Stratification matches §8 (§3.1) | **Confirmed** | |
| 17 | 14 ChartQA bare-answer splits are "mild boundary ambiguity" (§3.3) | **Nuanced** | Systematic per-coder convention (14/14 vs 14/14). It pushes ChartQA raw κ to .7019 (3B/7B ChartQA .6632, unreported), below 0.80; this is a codebook gap |
| 18 | `V0093`, `V0103` → `neither`; A self-inconsistent with `V0194` (§3.3) | **Confirmed** | |
| 19 | `V0177` → `unclear`; parser wrong; "first image" is really the typed text (§3.3) | **Confirmed, stronger evidence** | Antigravity inferred from `y_text=333`; the 3B/7B donor verbalizations for the same item explicitly say the typed text is the girls/boys problem |
| 20 | Adjudicated confusion matrix (35/94/11/19/40 + 1 `no_verdict→image`) (§3.3) | **Confirmed** | |
| 21 | Blinding (i): KEYs "absent during human coding" (§3.3) | **Disputed / Corrected** | Removed from the tip in `328c8af`, but retrievable from history (`git show 5b57529:…`). Blinding was honour-based |
| 22 | Blinding (iv): B "disagreed with `KEY_flips` on `F0006`" as evidence of independence (§3.3) | **Disputed** | `KEY_flips` holds no quality judgements; every field coders could compare against (`own_source`, `intended_flip_source`) is already in their sheet. Not evidence either way |
| 23 | Blinding conclusion: independent faithful coding [Inferred] (§3.3) | **Confirmed as Inferred** | B's 100% match is what an honest coder would produce, given a parser with one literal-reading error |
| 24 | `F0081` coordinate-clause bug, inverts own/flip and fools Gate 2 symmetrically (§1, §4.2) | **Confirmed** | |
| 25 | 38 rows with a split in the gap; 29/29 7B correct; 3 errors, all 2B (`-0057`, `-0162`, `-0119`) (§4.2) | **Confirmed** | |
| 26 | Surgical coordinate fix (§4.2, §6 P2-4) | **Nuanced** | Fixes 2/3 (`-0057`, `-0162`), with 0 changes on 3B/7B; `-0119` needs a separate `so` / "is not specified" rule. The fix does nothing about the larger 2B "two images" class (§4) |
| 27 | 5 flagged flips are "2B two-images hallucination → first typed text" grammar issues (§4.3) | **Nuanced** | They are also wrong-`own_source` cases: 53 2B donors (50 gate-passing) rest on positional "first image". Diagnostic-only; 2B never transplanted (0 competent) |
| 28 | `F0147` cross-sentence contradiction; item failed 7B competency (§4.3) | **Confirmed** | `gsm8k-image-L0-0118` not competent in 7B; same for `F0134` (`svamp-image-L0-0007`) |
| 29 | `F0134`, `F0065` unflagged structural issues (§4.3) | **Confirmed** | |
| 30 | Topic contradictions in 37/280 (13.2%) 7B and 10/190 (5.3%) 3B passed cells (§1, §4.3) | **Nuanced** | My detector gives 31/280 (11.1%) and 12/190 (6.3%), with some false positives; best estimate ~9–11% / 5–6%. The count depends on the detector; report it as approximate |
| 31 | Unswapped post-verdict sentences 3/190 3B (`-0084`, `-0046`, `-0113`); 0/280 7B (§4.3) | **Confirmed** | |
| 32 | Adjective swaps 2/280 7B (`-0104`, `-0019`), 0 elsewhere (§4.3) | **Confirmed** | |
| 33 | Anchoring "directly helps explain" the 21.1 pp 7B gap, "validating D2" [Inferred] (§1, §4.3) | **Disputed / Qualified** | Anchored cells account for ~6.1 of 21.1 pp; 16.9 pp persists without anchoring; under non-binding the gap is −5.7 pp. A partial, minor contributor. "Validating D2" is an overclaim on dev data |
| 34 | Evaluator Coder-A bias; κ returns 0.0 (§1, §5.1) | **Confirmed** | `evaluate_verdicts` gives .985 with A first, 1.0 with B first |
| 35 | Overwrite hazard, no `--keys_only` (§5.1) | **Confirmed + extended** | A key refresh after any parser change re-draws the flip pool. It must assert sample identity (§4) |
| 36 | 3B 29 ChartQA vs 31 Math flips; 80/200 and 53/150 overlap; 43/150 from transplanted confirmatory Math (§5.1) | **Confirmed + extended** | The 29 is the entire 3B ChartQA pool (and 10/10 for 7B): round-robin exhausts small strata |
| 37 | Preflight dev OK; 84 false-positive manifest errors, 100% after LF normalisation; no coding gate (§5.2) | **Confirmed** | Add: `git_dirty=True` from the untracked audit `.md` files will block confirm |
| 38 | `CONFIRM_MAX_PIXELS["chartqa"]` provisional; `validate_confirm_config` refuses an untagged confirm (§5.3) | **Confirmed** | |
| 39 | `manipulation_check` lenient vs structured; numbers 76.9/77.7, 94.4/94.1, 94.0/94.5, 98.4/98.3 (§5.4) | **Confirmed** | identical |
| 40 | Stale "0 filled rows" docs (§2.1) | **Confirmed + extended** | Additional stale lines: `Experiment/README.md` L8, L28, L112, L122; `CLAUDE.md` L20. (`README.md` L75 says "not yet coded", not "0 filled rows".) |
| 41 | Rec. P1-3: strip BOM, normalise CRLF, restore 7 cells and trim spaces in the coder CSVs (§6) | **Disputed (recommendation)** | CRLF needs no fix (not in the blobs). Editing the coders' submitted files destroys the raw record of what they returned. Keep them byte-for-byte; normalise in code (it already strips and reads `utf-8-sig`). Optionally save a cleaned copy alongside |
| 42 | Rec.: report AC1/PABAK alongside κ "against §8" (§4.1, §6 P1-1) | **Nuanced → escalated** | Reporting is not enough: §8 as written fail-stops on κ. Requires a logged §8/§11 amendment before freeze (P0) |
| 43 | "Does NOT need fixing: re-coding" (§6) | **Confirmed for verdicts; Nuanced for flips** | Flip coding should not be re-done, but its claim boundary needs stating: the coherent-rate does not certify semantic coherence, because instruction L129–132 told coders to accept factual oddities |
| 44 | Audit status line: date `2026-11-20`, commit `418aa82` | **Confirmed** | |

---

## 4. New Findings Missed or Under-Specified by Antigravity

1. **§8 gate wording is a freeze blocker, not a reporting note** [Verified text]. L558 sets an unscoped "`κ ≥ 0.80`" and L560 says "If a gate fails, the run stops. It does not proceed with a changed gate." Literal flip κ is .33 / .00. Because the prereg is not yet frozen, the honest route is to amend §8 now and log it in §11. The instructions already anticipated the problem at L193, and the κ-under-prevalence behaviour follows from the expected near-ceiling base rate. Amending a gate after seeing the coding data is a researcher degree of freedom, and the §11 entry should say so plainly.
2. **2B "two images" positional verdicts** [Verified counts]. 53 2B Math donors carry a source label that rests on a positional reference inside a frame where both sources are called "images" (`V0177`, `F0006`, `F0029`, `F0100`, and the other "first image … first image" rows `gsm8k-image-L0-0010`, `-0083`, `-0133`, `svamp-image-L0-0009`). 50 of them pass every edit gate. The labels are semantically unidentifiable, and `V0177` is substantively wrong. 3B/7B: 0 such rows. Impact today: none, because 2B has 0 competent Math items (`conflict_tp_qwen2.gates.json`). But any 2B "diagnostic" use of `stated_reliable_source` (manipulation check, verdict distributions) is contaminated.
3. **Line endings: the BOM is real, the CRLF is not** [Verified]. Committed coder blobs are LF; `core.autocrlf=true` produces the CRLFs on every Windows checkout, KEYs included. Practical consequence: on Windows, every multiline cell parsed with `newline=''` contains `\r\n`, so any future code that string-compares sheet text to JSONL text fails on Windows only. Same root cause as the 84 preflight false positives.
4. **The flip-sample identity depends on the parser** [Verified code path, L222–225]. `build_flip_samples` filters on `make_variants().ok`, which calls `stated_reliable_source`. Fixing the parser and then re-running `sample` (even into a scratch directory, to "refresh keys") can change the candidate pool and the RNG draw, misaligning the KEY with the coded `F` rows. Any refresh tool must assert `(sample_id, item_id, model_id, regime, order)` identity against the existing coder sheets and abort on mismatch.
5. **The topic-anchoring explanation of the dev gap is small** (§2.4 (6)): ~6 of 21 pp, and the sign reverses under non-binding.
6. **The flip-coding signal is one-sided** (§2.3). All defect detections came from A; B's names-intended column is constant. The human flip rate certifies the absence of *mechanical* defects (articles, half-swaps), not semantic coherence: instruction L129–132 deliberately counts factual oddity as coherent, and cross-sentence contradiction is not covered at all.
7. **ChartQA raw κ < 0.80** (.7019 all, .6632 3B/7B), driven by the bare-answer convention. Canonically perfect. Report it, and fix the codebook rule for future coding.
8. **§5.3 / `_FOIL_BEFORE` mismatch for `versus`/`vs.`** (latent, 0 dev occurrences).
9. **Keys in git history** compromise technical blinding (§2.1). Report it in the thesis methods as honour-based blinding.
10. **ChartQA small-pool exhaustion in flip stratification** (29/29, 10/10, 3/3). The ChartQA share of the flip sample is pool-driven, not design-driven.
11. **Precision of "100%"**: report Wilson intervals (120/120 → [.969, 1]; 168/168 → [.978, 1]).

---

## 5. Unified Pre-Freeze Modification Blueprint

Ordered for execution. "Verify" lines are the minimum post-fix checks. Paths are relative to the workspace root unless noted.

### P0 — Blocker (resolve before `prereg-v5`)

**P0-1. Amend §8 human-coding gate and log it in §11** (`Docs/PREREGISTRATION_VERDICT_TRANSPLANT.md` L558–560, deviation log §11).

- Scope `κ ≥ 0.80` to **verdict labels, canonical 3-way, pooled N = 200**. Name the statistic (Cohen's κ on `canonical_verdict_label`) and the denominator.
- For flips, replace κ with **raw agreement ≥ 0.90 and Gwet's AC1 ≥ 0.80**, with κ, κ_max and PABAK reported. Also require that every flip with any coder 0 is adjudicated, and report the adjudicated defect rate.
- State in §11 that the change was made after the coding data were seen, why (the near-ceiling base rate makes κ undefined or degenerate), and that the verdict gate itself is unchanged.
- Add the claim boundary: the flip-coherence rate certifies mechanical edit quality, not semantic coherence (cite the structural scan rates from this audit as dev diagnostics).
- Verify: `python -B Experiment/preflight_v5.py --json` (prereg consistency checks still pass).

### P1 — Required before `prereg-v5`

**P1-1. Record adjudication without touching the coders' files.**

- Create a new, tracked `Experiment/coding_v5/adjudication_v5.csv` with columns `sample_id, a, b, adjudicated, rationale`. Rows:
  - verdicts: the 14 bare-answer rows → `neither` (or the label the codebook amendment chooses), `V0093`/`V0103` → `neither`, `V0177` → `unclear`;
  - flips: `F0006` (0,1), `F0029` (0,1), `F0081` (0,0), `F0100` (0,1), `F0147` (decide the cross-sentence rule, then apply it);
  - optionally also `F0134` and `F0065` as automated-scan notes.
- Leave `coder_A_*` and `coder_B_*` byte-for-byte as submitted. Do **not** strip the BOM, restore the 7 Excel cells, or trim spaces in place; `read_csv_map` (`utf-8-sig`) and `.strip()` already handle them. If a clean archival copy is wanted, write `coder_*_clean.csv` next to them and record that in the README.

**P1-2. Fix the evaluator** (`Experiment/sample_v5_for_coding.py`).

- L318–357 `evaluate_verdicts`: report parser accuracy and confusion matrices separately for Coder A, Coder B, consensus-only rows and an optional `--adjudicated` CSV. Remove `human = a_lbl or b_lbl` (L332) as the headline. Add Wilson 95% CIs. Add the strict 3-way κ (S1/S2/NV) alongside the current 5-string κ.
- L360–403 `evaluate_flips`: the same A/B/consensus/adjudicated split (remove L375–376 precedence), and add AC1, PABAK, κ_max and the 2×2 table.
- L297–304 `cohens_kappa`: keep the function, and add `gwet_ac1()`, `pabak()`, `kappa_max()`. Document that κ = 0 when one rater is constant.
- Tests to add in `Experiment/tests/test_v5_fixes.py`:
  - a constant-rater case (expect κ = 0 and AC1 ≈ 0.9933 on 149/150);
  - an order-invariance case (swapping A/B must not change the headline);
  - reproduce this audit's numbers on the committed sheets (`.8803`, `.9783`, `.3258`, AC1 `.9722`).
- Verify: `cd Experiment` then `python -B -m unittest discover -s tests`. Then run `evaluate` **into a scratch `--out_dir`** first and diff against this report's numbers, before writing `coding_v5/evaluation_v5.json` once.

**P1-3. Make `sample` safe** (`Experiment/sample_v5_for_coding.py`).

- L407: exclude `*_px501k_*` from the default glob, or better, require explicit `--donor_files` and fail when the glob matches more than the 6 expected basenames.
- L421–426: refuse to write when any target `coder_*.csv` has a non-empty `coder_*` column, unless `--force` is passed.
- Add `--keys_only`, which writes only `KEY_*` and first **asserts** that the regenerated `(sample_id, item_id, model_id, regime, family/order)` tuples equal the existing coder sheets, aborting otherwise (finding §4-4).
- Use it to refresh the 5 stale `beh_source` cells (`V0032`, `V0092`, `V0140`, `V0149`, `V0176`), or simply document them; `evaluate` does not read `beh_source`.
- Verify: a unit test where a dummy 8-file directory with `px501k` is rejected or filtered, a test that the non-empty-sheet guard fires, and `--keys_only` on the real data reports 0 identity mismatches and exactly 5 `beh_source` changes.

**P1-4. Lock ChartQA `max_pixels`** in prereg §3.4 L224 and `Experiment/harness_v5.py:51` (`CONFIRM_MAX_PIXELS["chartqa"]`). Record the R8.4 numbers (`13→5` vs `16→1`; `13→0` vs `17→0`) as the rationale. Note that the ChartQA edit-gate pass rate is 38.5% at `200704`, below §8's 60%, so with the current gates ChartQA would be `NOT A READING`. Decide whether exploratory ChartQA (D4) is exempt from that gate, and say so.

**P1-5. Update stale docs.**

- `Experiment/README.md` L8, L28, L75, L112, L122;
- `Experiment/results_v5/README.md` L79;
- `Experiment/coding_v5/HUMAN_CODING_INSTRUCTIONS_v5.md` L56 (and fix L181: `encoding='utf-8-sig'`);
- `CLAUDE.md` L20 ("Now:" line).

State the coding outcome with denominators, and the honour-based blinding.

**P1-6. Clean tree for the tag.** Commit (or move out of the repo) `Thesis/docs/Archive/Antigravity Audit.md` and this report. `preflight` currently reports `git_dirty=True` because of them, and `validate_confirm_config` refuses a dirty or untagged confirm.

Verify after all P1 items:

- `cd Experiment` then `python -B -m unittest discover -s tests` (expect ≥ 248 tests OK);
- `python -B preflight_v5.py --json` (ok, no errors);
- `git status --short` empty except ignored files;
- `git tag prereg-v5`, then `python -B preflight_v5.py --phase confirm --json`.

### P2 — Optional cleanup (safe pre-freeze; each must keep 3B/7B dev labels unchanged)

**P2-1. `score_v5.stated_reliable_source` coordinate clause** (L106–121).

- When a `,\s*(?:and|but)\b` occurs before `"reliable"`, re-parse only the tail after the last such break.
- Measured effect: 2/2,760 donor labels change (`gsm8k-image-L0-0057`, `-0162`, both 2B), and 0 change for 3B/7B.
- Optionally add `so` to the clause-break handling for `-0119`; measure that separately.
- Regression tests:
  - `F0081`'s original sentence → `text`, and its flip → `image`;
  - the `-0162` sentence → `text`;
  - 3–4 of the 29 valid 7B antecedent sentences ("…from the image, as it is the more reliable source"; "Given that the report…, I consider it more reliable"; "The chart, being…, is considered more reliable") must stay unchanged.
- **Do not re-run `sample` afterwards.** Re-score `predicted_stated_source` in a copy of the key with the identity-asserting tool (P1-3) and report the post-fix parser accuracy as a §11 note.

**P2-2. 2B "two images" positional verdicts.** Either return `undetermined` when the verbalization names "two images" or uses `first/second image|text` as the referent (expected to remove ~53 2B labels, 0 for 3B/7B; verify before adopting), or document 2B verdict labels as positional and unreliable in the diagnostic sections. No confirmatory impact.

**P2-3. `versus`/`vs.` foil.** Add `versus|vs\.?` to `_FOIL_BEFORE` (`score_v5.py:62–65`), or delete them from §5.3 L368. 0 dev rows are affected either way. Add a test: `"The typed text, versus the image, is more reliable."` → not `image`.

**P2-4. Cross-OS hashing.** Either normalise `\r\n→\n` in `preflight_v5._sha256_file` (L169–174) when checking manifests, or add a tracked `.gitattributes` with `Experiment/*.py text eol=lf` (and `Experiment/coding_v5/*.csv -text`, so multiline cells are never rewritten). Verify: `python -B preflight_v5.py --check_manifests results_v5/*.manifest.json --json` reports 0 errors on Windows.

**P2-5. Preflight coding gate.** In `run_preflight(phase="confirm")` (`preflight_v5.py:337+`), require `coding_v5/evaluation_v5.json` and `adjudication_v5.csv` to exist, and the verdict canonical κ to be ≥ 0.80.

**P2-6. `analyze_v5.manipulation_check`** L660–662: pass `parser=HEADLINE_PARSER`. Expected dev shift ≤ 0.8 pp (§2.5).

**P2-7. Structural flip diagnostics in `gates.json`.** Because `SWAP_SCOPE="sentence"` leaves other sentences untouched, record per cell: post-verdict source mentions (3B: 3/190) and a pre-verdict topic-mapping flag (7B ~9–11%, 3B ~5–6%). Report a sensitivity analysis excluding anchored cells next to the co-primary `para_flip − para`. Changing the gates themselves now would alter the intervention; if that is considered, it must go through §5.3 and §11.

**P2-8. Codebook clarifications for any future coding.** Bare answers → `neither`; cross-sentence contradiction → `0` (or explicitly `1`); "first/second image" in a two-images frame → `unclear`.

### No fix needed

- `.gitignore` already ignores the keys; no key is tracked.
- `KEY_flips_do_not_open.csv` aligns 150 × 11 with regeneration.
- `KEY_verdicts_do_not_open.csv` aligns on every column `evaluate` reads.
- Donor files are 0-diff against the archive.
- Re-coding is not needed. Verdict κ passes comfortably; flips need adjudication and an amended gate, not new coding.
- The recorded pipeline errors in the keys (`V0177`, `F0081`) must stay as they are: they are what human coding exists to catch.
- CRLF in the coder CSVs is not a defect: the committed blobs are LF.
