# v5 Dev Pass: Forensic Code, Scorer and Construct-Validity Audit

**Audit date:** 2026-11-13
**Auditor:** Claude (AI). This report is AI-generated. Check it against code and data before relying on it.
**Scope:** `Experiment/results_v5/` (16 JSONL, 16 manifests, 6 gate reports, `pip_freeze.txt`), the active code in `Experiment/*.py`, the preregistration draft, and every prior audit named in the request.
**Status of every number: dev-only.** These are spent development items. No group meets the code's minimum sample (150 Math, 100 ChartQA). Nothing here is a confirmatory finding or evidence for H₁ or H₀.
**Read-only.** The only file written is this report. Scripts ran from the session scratchpad with `python -B`. Proposed code changes below are suggestions; none was applied.

**Code version audited.** Commit `09216b0`, where `harness_v5.py`, `transplant_v5.py`, `score_v5.py`, `harness_v4.py` and `score_v4.py` hash-match the v5 manifests. All verification scripts ran before 15:08 local time on 2026-11-13, and every `file:line` reference is to that version.

**Working tree changed after the audit runs, not by this audit.** Between 15:10 and 15:13 local time, uncommitted edits appeared in `analyze_v5.py`, `harness_v4.py`, `harness_v5.py`, `score_v4.py`, `score_v5.py` and `transplant_v5.py`, plus a new `tests/test_v5_fixes.py`. This audit made none of them and has not reviewed them. Two consequences:
- The edited scripts no longer hash-match the v5 manifests, so results recomputed with them are not like-for-like with the stored gate reports.
- The `score_v4.py` edit adds `####` to `_PIVOT` and `U.S./U.K.` to `_ABBREV`. The in-memory test of exactly that change (§2.2 row 15, §4 H3) rescued 0 of 76, 0 of 5 and 4 of 10 truncated donor rows, because the main cause is the two-sentence fallback at `score_v4.py:128-129`.

Tags: `[Verified]` recomputed here from rows or read from code; `[Inferred]`; `[Hypothesis]`; `[Discrepancy]` a prior claim that does not match rows or code.

---

## 1. Executive verdict on dev v5

**What works [Verified]**

- The stored data are complete: 29,880 rows, exactly the request grid, with no duplicates or unreadable lines. All 20,868 scored rows (19,488 `dl` + 1,380 `nll`) have `boundary_mismatch == False` and `ws_skipped == 2`.
- Prompts, prefills and gate reports regenerate from the stored rows with the current code. All 196 unit tests pass.
- The Δℓ machinery itself (teacher forcing, token-boundary check, orientation, bootstrap, sign-flip test) computes what the preregistration says it should. Point estimates reproduce exactly under an independent implementation.

**What is broken or unsafe to freeze**

1. **The primary outcome has a construct problem in Math [Verified numbers, Inferred reading].** Δℓ is scored at `####` before any arithmetic is written. Its sign matches the model's eventual answer less often than always guessing the majority source would:

   | Model | Sign agreement (strict parser) | Majority-class baseline | Agreement (lenient parser) | AUC of Δℓ within evidence order |
   |---|---:|---:|---:|---|
   | 3B Math | 545/1,057 = 51.6% | 55.2% | 669/1,331 = 50.3% | 0.53 / 0.56 |
   | 7B Math | 583/1,030 = 56.6% | 75.9% | 1,413/2,461 = 57.4% | 0.70 / 0.68 (0.75 / 0.69 lenient) |

   For 3B, Δℓ carries almost no information about which problem the model then solves. For 7B it carries moderate information once the large order offset is removed (AUC about 0.7), which the sign statistic hides. Earlier reports, including mine, described both models as simply "decoupled"; that is right for 3B and too strong for 7B.

2. **The flip contrast mostly measures deleting the model's own verdict, not following the reversed one, in 7B Math [Verified].** Of the binding CDE of 1.619, 1.515 (93.6%) appears when the reliability sentence is merely deleted; inserting the flipped sentence adds 0.103 (95% CI [−0.09, 0.29]).

3. **The behavioural scorer discards most 7B Math answers [Verified].** After a prefilled verbalization, 7B writes `####` in only 1,149 of 2,760 behavioural generations (41.6%), against 349/400 (87%) in its single-source base runs. The strict parser scores the rest as "neither". With the v4 last-number fallback, "neither" drops from 62.7% to 10.8%, and the binding behavioural shift rises from +18.3 pp to +49.6 pp.

4. **Retention fails for 2B and for ChartQA [Verified].** 2B has 0/200 competent Math items (it never writes `####`) and 0 gate-passing ChartQA items. ChartQA retains 6 (3B) and 2 (7B) of 30. Both retained 7B ChartQA items carry a gold answer inside the prefill of every arm.

5. **Several scorer and analysis defects are real, but smaller than the prior audits state** (§4). In particular, "fixing" `change_rate` does not make the wording floor pass: with image↔text flips counted only on attributable pairs, 3B non-binding is still at 9.0%, and the 3B binding signed mean is −5.6 pp, outside ±5 pp under every parser.

**What the dev data show, plainly.** Forcing a reversed verdict clearly changes what 3B and 7B then answer in Math when the answer is parsed leniently (+58 pp and +50 pp under binding). The preregistered primary outcome does not capture that cleanly: in Math it mostly reflects evidence order, and in 7B its "effect" is the removal of an anchoring sentence. ChartQA is too small to say anything. None of this is a finding; it is a list of reasons the design cannot be frozen as drafted.

---

## 2. Audit of prior reports

### 2.1 Statements in the audit request that do not match the repository [Discrepancy]

The request asked for these to be verified. They are wrong as stated.

| Claim in the request | What the files show |
|---|---|
| `prompts_v5.py`, `prompts_v4.py` are active code | Neither file exists. Prompts are built in `harness_v5.py:57-243` |
| `Docs/Paper/PRE_FREEZE_AUDIT.md` | Does not exist. The freeze audit is `Docs/Paper/prereg-freeze-audit/prereg-freeze-audit.md` |
| `v5_dev_output.md` contains an "initial `analyze_v5.py` run" | It contains no analysis command or output. No `results_v5/analysis_dev/` exists |
| Stages `ceiling_dl`, `ceiling_beh`; arm `base_conflict` | Not present. `outcome` is `beh`, `nll` or `dl`. The ceilings are families `explicit_image` / `explicit_text` with verdict `none` |
| 11 manifests have `n_rows_written: 0` and timestamps `2026-04-17T06:24:36Z`–`06:24:46Z` | Manifests have no `n_rows_written` key. The 11 no-op manifests are stamped `2026-11-12T09:15:48`–`09:19:04`. That they wrote 0 rows comes from the transcript (`v5_dev_output.md:223-391`), not the manifest |
| `.gates.json` has `created_utc`, `both_competent`, `image_competent`, `text_competent`, `all_gates` | None of these keys exist. Keys are `items, competent, taken, no_donor, passed, jaccard_multiset_flip_min/mean, swaps_per_flip, own_source_by_order, fail_reasons_by_order, passed_ids`. Gate files carry no timestamp, so they cannot reconstruct a timeline |
| `holm_bonferroni()`, `beh_panel()` | The functions are `holm()` (`analyze_v5.py:155`) and `behaviour_table()` (`:329`) |
| `analyze_v5.py:390-443` computes T2/T3, split by "instruction (`decision_relevant` vs `equivalent`)" | Lines 386-431 are the manipulation check and relative uncertainty. T2/T3 are at `:541-559`, as ratios of item-level means. `decision_relevant` / `equivalent` are two readings of the same ρ, not instructions |
| `x["image"]` is `1.0` for image and `0.0` for text **or** neither, so text↔neither is not counted | `follows_image` returns `1`, `0` or **`None`** (`analyze_v5.py:102-104`). `0 != None` is true, so text↔neither **is** counted, as is image↔neither |
| `qwen25_vl_7b_conflict_beh.jsonl`; "62.68% (1,610 / 2,568)" | The file is `v5dev_conflict_tp_qwen25_7b.jsonl` with 2,760 `beh` rows. 62.68% is 1,730/2,760 "neither"; 1,611 rows lack `####` |
| 3B Math `none − own = +0.5787`, `flip − none = +0.5620` | +0.1375 and +0.0955 (sum 0.2330) |
| T1 is `flip − own` | In both spec and code T1 is the difference-in-differences, CDE_bind − CDE_nonbind (`analyze_v5.py:526, 537`) |
| Spontaneous-verdict rates for 2B | 2B has no transplant rows in either regime, so there is nothing to measure |

### 2.2 The two "End-to-End" audits

- `Docs/Context/End-to-End Technical & Scientific Audit.md` (313 lines) and `Docs/Decision_Audits/Independent End-to-End Technical & Scientific Audit.md` (264 lines) are **not identical** but share the same body [Verified by normalised diff]. The Context copy adds a header block claiming "highest-priority" status and a §9 inventory appendix, and uses relative links; the other uses `file://` links. Their claims are treated together below as "E2E".

| # | E2E claim | Result | Verdict |
|---|---|---|---|
| 1 | 29,880 rows; 20,868 scored rows with 0 boundary mismatches, `ws_skipped == 2`; 196 tests (114 + 57 + 25) | same | `[Verified]` |
| 2 | JSONL total 34,637,510 bytes; per-file bytes in its §9 (e.g. `conflict_base_qwen2` 917,052) | on disk: 36,146,923 bytes in total; that file is 964,420 bytes | `[Discrepancy]` (probably characters, not bytes) |
| 3 | L4 "CC 8.9" | compute capability is recorded nowhere | `[Discrepancy]` (unrecorded) |
| 4 | Competency and gates: 0/80/124 Math, 10/13/13 ChartQA; passed 80, 115, 0, 6, 2; lenient competency 43 / 127 / 154; 2B all-donor gate pass 88/200 | same | `[Verified]` |
| 5 | Primary table: Ceil, CDE, ρ, DiD, CIs, raw p | same to the printed precision | `[Verified]` |
| 6 | Holm with m = 3: 0.0003 (Math); 3B ChartQA T1 = 0.0314; 7B ChartQA T1 = 0.7275 | 0.0003 ✓; 0.7275 ✓; 3B ChartQA T1 is 0.0157 when T2/T3 enter with their decision-relevant p (it is the largest of the three), or 0.0471 with their equivalence p | `[Discrepancy]` on one value; see §5.1 for why "m = 3" is ambiguous |
| 7 | Decomposition: 7B 1.5154 / 0.1033 (93.6%); 3B 0.1375 / 0.0955; ChartQA 3B 0.1883 / 0.2725, 7B 0.0646 / 0.1684; 7B `text_first` flip − none = −0.2417 | same | `[Verified]` |
| 8 | Sign agreement 545/1,057 (3B), 582–583/1,030 (7B), 108/109, 47/48 | same | `[Verified]`; the majority baseline and within-order AUC (§1) were not reported |
| 9 | `change_rate` counts `None` transitions; 77/86 (3B) and 93/94 (7B) of counted own-vs-para changes involve "neither" | same (binding + non-binding pooled) | `[Verified]` |
| 10 | "True" wording churn is 1.88% (3B binding) and 0.00% (7B binding) | The 3 and 0 flips are right, but the denominators (160, 230) include cells where a flip could not be observed. Among pairs where both answers are attributable: 3/84 = 3.6% and 0/54 (binding); 6/67 = 9.0% and 1/54 = 1.9% (non-binding) | `[Discrepancy]` (denominator). The conclusion "a very clean true wording floor" does not follow |
| 11 | 7B: 1,610 rows omit `####`; lenient rescues 1,431 (774 image + 657 text); "neither" 62.68% → 10.83% | 1,611 rows omit `####` (1,610 parsed by fallback + 1 with no number); rest same | `[Verified]` (off by one) |
| 12 | Math `none` behavioural arm regenerates a verdict: 222/320 (3B), 407/460 (7B) | 3B: 130/160 non-binding + 92/160 binding = 222/320 ✓. 7B: 229/230 + 189/230 = 418/460 contain "reliable"; 406 open with a sentence naming a source | `[Verified]` (7B is 88–91% depending on definition) |
| 13 | `visual` → `image` mislabels 7B ChartQA item 18 `text_first` | same; it is the only wrong-regime row in all six donor files | `[Verified]` |
| 14 | `_REL_NEG` misses "less reliable"; 2B `svamp-image-L0-0033 text_first` gets an inverted label "and passes all edit gates" | The inversion is real. A second inverted row exists (2B `gsm8k-image-L0-0123 text_first`). Neither item is competent, and no row in any transplant set is inverted | `[Verified]` with a caveat: no stored transplant row is affected |
| 15 | `split_verbalization` truncates the reliability sentence in 76/400 (2B Math), 5/60 (3B ChartQA), 10/60 (7B ChartQA) donor rows, **because** `####` is missing from `_PIVOT` and `U.S.` from `_ABBREV` | Counts ✓. The stated cause is mostly wrong: adding `####` and `U.S./U.K.` handling in memory rescues 0/76, 0/5 and 4/10. The main cause is the two-sentence fallback at `score_v4.py:128-129` | Counts `[Verified]`; mechanism `[Discrepancy]` |
| 16 | Competent item-orders falsely rejected: 7B `14 tf`, `21 if`, `28 tf`; 3B `24 if` | With the verbalization extended through the first "reliable" sentence, competent gate-passing items rise 6 → 7 (3B: item 24) and 2 → 4 (7B: items 14 and, via a regime-aware noun set, 18). Items 21 and 28 then fail `gate3_too_many_swaps` | Partly `[Verified]` |
| 17 | ChartQA Sentence-1 leakage: 50.0% (3B), 68.3% (7B) of donor verbalizations | Those figures use all 120 rows per model (including `free_binding`) and substring matching. On the 60 `donor` rows, with numeric boundaries and excluding the reliability sentence: 21/60 = 35% (3B) and 46/60 = 77% (7B). In the rows actually transplanted: 1/12 cells (3B, item 9) and 4/4 cells (7B, items 15 and 16) | Direction `[Verified]`; magnitudes depend on definition |
| 18 | Gate 3b "rejects 8/13 competent 7B ChartQA items" | It rejects 8 item-**orders**; `fail_reasons_by_order` counts orders (`transplant_v5.py:340-344`) | `[Discrepancy]` (unit) |
| 19 | Replay stability 82/84 (3B) and 73/73 (7B) on attributable rows | same | `[Verified]`; see §2.3 item 3 |
| 20 | Behavioural matched pair on 3B: +50.6 pp (binding), +37.5 pp (non-binding) | +61.3 pp and +40.0 pp with the §7.3 single-target definition | `[Discrepancy]` (not reproduced) |
| 21 | Human coding 0/300; manifests' 11 no-op rewrites; `resolved_model_commit` null; `verdict_nll` spans the whole prefill; missing spec outputs in `analyze_v5.py` | same | `[Verified]` |
| 22 | Self-description as "highest-priority" and "verified directly" | It contains the errors in rows 2, 3, 6, 10, 15, 18 and 20 | Treat as a lead, as the request says |

### 2.3 Archive reports

- **`v5_antigravity_analysis.md`**: reverses the verdict order effect (near-100% text verdicts occur with text **first**), misreads the 3B ceiling, and asserts causes with no support. Its raw table values reproduce. Unchanged from my earlier assessment.
- **`v5_dev_evidence_audit.md`**: numerically accurate. It misses the provenance gap and everything in §4 below.
- **`claude_v5_independent_deep_audit.md` (my second-pass report)**: its numbers reproduce. Three of its statements need correcting:
  1. It treated the strict "neither" rate as a property of the model. For 7B it is mostly a format artefact of the prefill (§4, H1).
  2. It called 3B and 7B Math Δℓ alike "weakly coupled" to behaviour. Within evidence order, 7B's Δℓ has an AUC near 0.7 (§1).
  3. Its "replay floor" of 6.4% / 8.2% is correct under the code's definition of churn but is mostly attributable↔"neither" transitions. Under the lenient parser the replay churn is 14/157 = 8.9% (3B) and 11/220 = 5.0% (7B), of which image↔text flips are 4/112 and 2/196.
  It also did not find the `none`-arm regeneration, the splitter fallback, or the prefix leak.

### 2.4 Findings no prior report contains

- Δℓ's sign agreement is **below the majority-class baseline** in both Math models, and Δℓ has real within-order signal for 7B but not 3B (§1, §5.3).
- 7B's `####` compliance collapses from 87% (base) to 35% (donor file) and 42% (transplant) once a verbalization precedes the solution (§4, H1).
- The splitter's failure mode is the two-sentence fallback, not the missing pivot (§4, H3).
- Correcting `change_rate` does not rescue the wording-floor gate (§5.4).
- In 11 of 12 retained 3B ChartQA cells, the prefilled Sentence 1 says the chart and report "give the same answer". They do not; every item is a conflict by construction (§5.5).
- The `none` behavioural arm regenerates a verdict that differs from the cell's own verdict in 68/222 (3B) and 109/417 (7B) cases (§4, H5).

---

## 3. Forensic data, manifest and gate inventory

### 3.1 JSONL files [Verified]

| File (`v5dev_…`) | Bytes | Rows | Items | `beh` | `nll` | `dl` | Capped `beh` | Σ `wall_s` (h) |
|---|---:|---:|---:|---:|---:|---:|---:|---:|
| `conflict_base_qwen2` | 964,420 | 800 | 200 | 400 | 400 | — | 11 | 0.20 |
| `conflict_base_qwen25` | 1,078,307 | 800 | 200 | 400 | 400 | — | 9 | 0.27 |
| `conflict_base_qwen25_7b` | 1,077,533 | 800 | 200 | 400 | 400 | — | 10 | 1.11 |
| `conflict_donor_qwen2` | 1,054,360 | 800 | 200 | 800 | — | — | 6 | 0.22 |
| `conflict_donor_qwen25` | 1,535,020 | 800 | 200 | 800 | — | — | 7 | 0.42 |
| `conflict_donor_qwen25_7b` | 1,577,982 | 800 | 200 | 800 | — | — | 1 | 1.71 |
| `conflict_tp_qwen25` | 10,771,750 | 9,600 | 80 | 1,920 | — | 7,680 | 13 | 1.34 |
| `conflict_tp_qwen25_7b` | 16,829,438 | 13,800 | 115 | 2,760 | — | 11,040 | 0 | 5.65 |
| `chartqa_base_qwen2` | 58,726 | 120 | 30 | 60 | 60 | — | 0 | 0.00 |
| `chartqa_base_qwen25` | 59,477 | 120 | 30 | 60 | 60 | — | 0 | 0.01 |
| `chartqa_base_qwen25_7b` | 60,374 | 120 | 30 | 60 | 60 | — | 0 | 0.01 |
| `chartqa_donor_qwen2` | 60,757 | 120 | 30 | 120 | — | — | 0 | 0.01 |
| `chartqa_donor_qwen25` | 72,542 | 120 | 30 | 120 | — | — | 0 | 0.02 |
| `chartqa_donor_qwen25_7b` | 135,662 | 120 | 30 | 120 | — | — | 1 | 0.10 |
| `chartqa_tp_qwen25` | 571,628 | 720 | 6 | 144 | — | 576 | 0 | 0.05 |
| `chartqa_tp_qwen25_7b` | 238,947 | 240 | 2 | 48 | — | 192 | 0 | 0.03 |
| **Total** | **36,146,923** | **29,880** | | **9,012** | **1,380** | **19,488** | | **≈ 11.15** |

- Base files hold two arms (`base_image`, `base_text`) × two outcomes, with no evidence order. `results_v5/README.md` describes them as "200 items × 2 orders × 2 sources", which is wrong [Discrepancy].
- Donor files hold families `donor` and `free_binding`, each in both orders.
- Scored rows: 20,868, all with `boundary_mismatch == False`, `ws_skipped == 2`, finite and non-positive log-probabilities.
- The "about 12-hour run" is 11.15 hours of summed per-row wall time across several sessions, not one recorded run.

### 3.2 Manifests [Verified]

All 16: NVIDIA L4, `torch.bfloat16`, torch 2.14.1+cu130, transformers 5.22.1, Python 3.13.16, pinned model and dataset revisions, `repetition_penalty 1.0`, `max_pixels 200704`; batch size 8 (2B, 3B) or 2 (7B). Script hashes equal the current files.

| Question | Answer |
|---|---|
| Why is `resolved_model_commit` null? | `harness_v4.py:436` reads `getattr(self.model.config, "_commit_hash", None)`. With this transformers version the attribute was not set on the loaded config, so `None` was stored. The requested revision is in `config.model_revision`; what was actually resolved is unrecorded |
| Why do 11 manifests look like no-ops? | `write_manifest` (`harness_v4.py:601-625`) rewrites the file at the start and end of **every** invocation (`harness_v5.py:771-773`), including a resume that finds nothing to do. Eleven manifests carry `written_at` between 09:15:48 and 09:19:04 on 2026-11-12, the session whose transcript shows `Wrote 0 rows` for those blocks. Their `peak_vram_gb` (4.1146, 6.9936, 15.4454) equals the bf16 weight size, i.e. load only |
| Can the true timeline be reconstructed? | Only partly. Gate files have no timestamps. From the transcript and the five later manifests: 7B Math donor finished 10:02:52 (354 new rows, 43.4 min); 7B Math transplant scored by 11:26:10 and generated by 15:42:37; 7B ChartQA 15:43–15:52. Everything for 2B and 3B, 7B Math base, and 446 7B Math donor rows was computed earlier in sessions with no transcript. Drive directory dates (Nov 12 03:40–09:08) are the only hint [Inferred] |
| Is there row-level evidence about those sessions? | Runs of identical `wall_s` show batch size 8 in every 2B/3B file and 2 in every 7B file. The earlier and later halves of the 7B Math donor file decode at 0.0391 and 0.0399 s/token. Both are consistent with the manifests [Inferred: same GPU class] |

### 3.3 Gate reports and competency [Verified]

| Regime | Model | Image-correct | Text-correct | Competent | Passed gates | Rate | Fail reasons (orders) | All-donor gate pass |
|---|---|---:|---:|---:|---:|---:|---|---:|
| Math | 2B | 0 | 0 | 0 | 0 | — | — | 88/200 |
| Math | 3B | 114 | 138 | 80 | 80 | 100% | — | 199/200 |
| Math | 7B | 168 | 148 | 124 | 115 | 92.7% | too_many_swaps 8, undetermined 1 | 186/200 |
| ChartQA | 2B | 10 | 20 | 10 | 0 | 0% | absent 18, undetermined 2 | 1/30 |
| ChartQA | 3B | 14 | 26 | 13 | 6 | 46.2% | absent 11 | 10/30 |
| ChartQA | 7B | 13 | 28 | 13 | 2 | 15.4% | too_many_swaps 8, absent 3, wrong_regime 1 | 6/30 |

- Three-way competency intersection: Math 0, ChartQA 8. 3B ∩ 7B: Math 54 competent (50 gate-passing in both), ChartQA 11 competent (0 gate-passing in both).
- All six gate files regenerate exactly from stored rows with `transplant_v5.plan`.
- The preregistration's §8 rule "analysis proceeds if ≥ 60% of competency items pass" fails for all three ChartQA models.

---

## 4. Code, scorer and spec bug registry

Each "fix" is a proposal for the researcher to accept or reject before the freeze. Where the code matches the letter of the draft spec, the defect is in the spec and is marked so.

### CRITICAL (design, not code)

**C1. Math Δℓ is scored before any reasoning, and does not track the answer.**
- Where: `transplant_v5.py:258-259` (`score_prefill` = `{m}\n\n####`); spec §6.1.
- Evidence: §1 table; §5.3. Raw Δℓ moves by +1.5 to +2.0 toward whichever source is presented last (3B: −0.81 image-first, +0.71 text-first), ten times the 3B ceiling.
- Consequence: T1–T3 in Math test a pre-reasoning number prior. The code implements the spec faithfully; the spec's outcome is the problem.
- Remedy options (decision required): keep Δℓ primary only for ChartQA; or score Δℓ after the model's own working; or promote a fixed-parser behavioural contrast in Math. Each changes R3.

**C2. The CDE mixes "own verdict removed" with "reversed verdict followed".**
- Where: spec §1, §7.1; `analyze_v5.py:285-292`.
- Evidence: §5.2.
- Remedy option: preregister the decomposition through `none` (the rows already exist in every run) and state which component H₁ refers to.

### HIGH

**H1. Strict `####` parsing interacts with the prefill and discards most 7B Math behaviour.**
- Where: `score_v5.py:150-162` (drops `fallback_last_number`), used by `harness_v5.base_correct` (`:657-663`) and all behavioural analysis. Spec §6.2 mandates exactly this, so this is a spec defect that the code inherits.
- Mechanism: 7B ends 1,221 of its 1,611 no-`####` generations with "The final answer is X."
- Evidence: `####` present in 349/400 base rows, 281/800 donor-file rows, 1,149/2,760 transplant `beh` rows. Example (`gsm8k…`, gold 595 / 36): `"…= 595 gems.\n\nThe final answer is 595."` is scored "neither".
- Impact: competency 124 vs 154 (7B), 80 vs 127 (3B), 0 vs 43 (2B); 7B behavioural Δ +18.3 vs +49.6 pp; 7B behavioural ceilings 71/230 and 93/230 vs 208/230 and 205/230.
- Check on the fallback's safety: where a stricter "answer is X" pattern and the last-number fallback both attribute an answer, they never disagree on the source (0 of 2,089 rows for 7B, 0 of 1,101 for 3B).
- Proposed fix (offline): accept, in order, `####`, then an explicit final-answer statement, then optionally the last number, and report all three.
  ```python
  _FINAL = re.compile(r"(?:final answer|answer)\s*(?:is|=|:)\s*\**\s*\$?\s*(-?\d[\d,]*(?:\.\d+)?)", re.I)
  # in behavioural_source, math branch, when method is not hash_direct/hash_tail:
  hits = _FINAL.findall(text); ans = hits[-1].replace(",", "") if hits else None
  ```

**H2. `change_rate` counts transitions to and from "neither" as answer changes.**
- Where: `analyze_v5.py:360-368` with `follows_image` (`:102-104`) returning `None` for "neither".
- Spec §7.6 says "changes at all", so the code follows the letter; the gate it feeds is then dominated by format failures.
- Evidence (strict parser, own vs para):

  | Cell set | Cells | Same | text↔neither | image↔neither | image↔text | Code churn |
  |---|---:|---:|---:|---:|---:|---:|
  | 3B binding | 160 | 119 | 27 | 11 | 3 | 25.6% |
  | 3B non-binding | 160 | 115 | 25 | 14 | 6 | 28.1% |
  | 7B binding | 230 | 183 | 45 | 2 | 0 | 20.4% |
  | 7B non-binding | 230 | 183 | 37 | 9 | 1 | 20.4% |

- Proposed fix (offline): report both the all-transition rate and the flip rate among pairs where both answers are attributable, with its denominator.
  ```python
  if x and y and x["image"] is not None and y["image"] is not None:
      n += 1; changed += x["image"] != y["image"]
  ```
- This does not make the gate pass (§5.4).

**H3. `split_verbalization` cuts the reliability sentence off when the model writes three sentences and no solving cue.**
- Where: `score_v4.py:128-129` (`if len(ends) >= 2: return text[:ends[1]], …`). Secondary: `_ABBREV` (`:88`) lacks `U.S.`; `_PIVOT` (`:92-98`) lacks `####`.
- Evidence: 76/400 2B Math, 5/60 3B ChartQA, 10/60 7B ChartQA donor rows. Example (3B ChartQA item 10): `"The percentage difference … is 3%. The report and the chart give the same answer. The report is considered more reliable."` gives a two-sentence verbalization with no verdict, so the item fails `own_absent`.
- Rescue simulation (gate counts only; verbalization extended through the first "reliable" sentence within the first five): all-donor gate pass 2B Math 88 → 149; competent-and-passing ChartQA 3B 6 → 7, 7B 2 → 4. Existing passed items keep identical verbalizations.
- Proposed fix: after the cue search, extend the cut to the end of the first sentence matching `\breliable\b` when it lies within the first few sentences. Rescued items need GPU rows, because their prefills are new.

**H4. ChartQA prefills contain the gold answer before the verdict.**
- Where: `transplant_v5.py:197-225` keeps every non-reliability sentence in all five variants; no gate checks for answers.
- Evidence: transplanted cells with a gold number in `m_none`: 3B 1/12 (item 9 image-first states "883", the chart answer); 7B 4/4 (item 15 states both "15,299" and "18,237"; item 16 states "35,283"). Among all `donor` rows: 35% (3B), 77% (7B). Math: 0.
- Impact: for 7B ChartQA, both retained items leak, so no clean estimate exists. For 3B, dropping item 9 leaves n = 5 with ρ_bind 0.397 (was 0.401).
- Proposed fix (offline gate): reject a variant set when the prefix without the reliability sentence contains `y_image` or `y_text` as a number. This reduces ChartQA yield further.

**H5. The Math behavioural `none` arm is not a no-verdict condition.**
- Where: `transplant_v5.py:262-265` prefills `{m_none}\n\n` and lets the model continue under an instruction that asks for a verdict.
- Evidence (share of generations containing "reliable"):

  | Family | 3B | 7B |
  |---|---:|---:|
  | non-binding | 130/160 (81%) | 229/230 (99.6%) |
  | binding | 92/160 (58%) | 189/230 (82%) |
  | explicit_image | 61/160 (38%) | 99/230 (43%) |
  | explicit_text | 63/160 (39%) | 141/230 (61%) |

  Example (3B): prefill ends `…the number of teachers.\n\n`; generation begins `"The typed text is more reliable because it is a clear and straightforward problem…"`. The regenerated verdict matches the cell's own verdict in 154/222 (3B) and 308/417 (7B) cases.
- Impact: no confirmatory test uses these cells, but the behavioural ceilings and any behavioural `none` baseline are contaminated. The Δℓ `none` arm is unaffected because `####` is forced.
- Proposed fix: needs a design decision (for example a neutral bridging sentence, or reading the behavioural ceiling only through Δℓ) and a GPU re-run of the affected cells.

### MEDIUM

**M1. Verdict classifier ignores regime and comparative negation.**
- Where: `score_v5.py:35-50` (`_SOURCE_NOUN` includes bare `visual`, `written`), `:52` (`_REL_NEG`), `:57-75`; `transplant_v5.py:108-118` (`_SWAP` does not swap `visual` / `written`).
- Evidence: one wrong-regime row (7B ChartQA 18 `text_first`: "The chart, being a visual representation…, is considered more reliable" → `image`). Two inverted labels, both 2B Math and not competent: `svamp-image-L0-0033 text_first` ("the image is considered less reliable than the typed text" → `image`) and `gsm8k-image-L0-0123 text_first`. No transplanted row is mislabelled.
- Side effect of the noun mismatch: flips that keep an unswapped modality word, e.g. 7B Math `gsm8k-image-L0-0132`: "…whereas the typed text is a visual representation of a word problem".
- Proposed fix: pass `regime` and restrict the noun set to that regime's sources; treat `less|not|un-reliable` as naming the other source or as undetermined; validate with the human coding the spec already requires.

**M2. Flips also swap nouns in the justification clause.**
- Where: `transplant_v5.py:137-144`.
- Evidence: flips with two swaps: 41/160 (3B Math), 55/230 (7B Math), 2/12 and 3/4 (ChartQA). Some are incoherent: 3B ChartQA item 8: "The chart is more reliable as it provides the exact response shares in the pie **report**". 7B ChartQA item 15 asserts the 2019 value "is not shown in the report", which is false.
- Relevance: a candidate explanation for why flips are weaker than template verdicts (§5.2) [Hypothesis].
- Proposed fix: swap only within the clause containing "reliable", and gate on the clause.

**M3. `analyze_v5.py` does not implement several spec requirements.**
- Missing: the §8 60% edit-gate rule and "stop if a gate fails"; enforcement of R5 (it sets `meets_min_items` at `:520` but still emits `reading_binding` at `:588`); a non-binding reading (§2.2); per-template and leave-one-template-out estimates (§7.4); `verdict_nll` in `long_v5.csv` (`CSV_FIELDS`, `:703`); CIs for tertiles, relative uncertainty and the manipulation check (§7.5); the three-way competency intersection (R8.3); the duplicate-row and fake-backend guard that `analyze_v4.py:85-93` has.

**M4. `verdict_nll` is not the NLL of the verdict.**
- Where: `harness_v5.py:538-548`. `verdict_from = len(base_ids)`, so the span is the entire prefill: every sentence of the verbalization plus `\n\n####`. On the `none` arm it scores Sentence 1; on base rows it scores `####`.
- Spec §6.3 calls it "perplexity of the forced verdict".
- Proposed fix: tokenise the prefix up to the start of the reliability sentence and score only that sentence's tokens. Needs GPU to regenerate.

**M5. Manifest provenance.** `harness_v4.py:436` and `:601-625` (see §3.2). Proposed fix: append one record per invocation instead of overwriting; store rows written, the resolved commit from the Hub API, and the dataset fingerprint.

### LOW

**L1. Holm family size.** `analyze_v5.py:536-560` passes five p-values (T1, and both the decision-relevant and equivalence p for T2 and T3). Spec §7.2 says "three tests … Holm-corrected" **and** defines two p-values per interval test without saying which enters. The code's m = 5 is the conservative reading of an ambiguous spec. No reading depends on it (§2.2 of the spec decides on unadjusted criteria), and no dev conclusion changes (§5.1). The spec should state the rule.

**L2. `_REL_SENT` splits at any period** (`score_v5.py:51`), so decimals or `U.S.` inside the reliability sentence shorten the fragment that is labelled. Two 7B ChartQA rows are affected; neither label changes.

**L3. ChartQA strict parser rejects a number followed by a unit** (`score_v5.py:124-142`, `answers_match`). One row: 3B item 13 `base_text` answers "17.0 million" for gold 17. 3B ChartQA competency would be 14, not 13.

**L4. Candidates are scored as prefixes with no end token** (`harness_v5.py:542`). In 8 of 200 Math dev items one gold answer is a string prefix of the other.

**L5. `results_v5/README.md`** misdescribes the base files (§3.1).

---

## 5. Statistical and construct-validity deep dive

All dev-only. "T1" is the DiD; "T2" and "T3" are ρ under binding and non-binding.

### 5.1 Primary tests, with standard errors and both Holm readings

Item bootstrap, 10,000 resamples. SE is the bootstrap standard deviation; the analytic SE agrees to the third decimal for Math.

| Quantity | 3B Math (n = 80) | 7B Math (n = 115) | 3B ChartQA (n = 6) | 7B ChartQA (n = 2) |
|---|---:|---:|---:|---:|
| Ceil_ℓ (SE) | 0.152 (0.020) | 1.423 (0.112) | 1.148 (0.131) | 0.956 (0.487) |
| CDE_bind (SE) [95% CI] | 0.233 (0.028) [0.181, 0.290] | 1.619 (0.150) [1.335, 1.924] | 0.461 (0.075) [0.338, 0.619] | 0.233 (0.162) [0.005, 0.461] |
| CDE_nonbind (SE) [95% CI] | 0.150 (0.025) [0.104, 0.204] | 1.342 (0.139) [1.084, 1.626] | 0.357 (0.064) [0.251, 0.494] | 0.172 (0.122) [−0.000, 0.345] |
| T1 DiD (SE) [95% CI] | 0.083 (0.016) [0.051, 0.113] | 0.277 (0.029) [0.220, 0.335] | 0.104 (0.026) [0.055, 0.152] | 0.061 (0.040) [0.005, 0.117] |
| T1 sign-flip p | 0.0001 | 0.0001 | 0.0157 | 0.2425 |
| T2 ρ_bind [90% CI] | 1.529 [1.258, 1.865] | 1.138 [1.022, 1.254] | 0.401 [0.332, 0.475] | 0.244 [0.018, 0.281] |
| T3 ρ_nonbind [90% CI] | 0.984 [0.736, 1.305] | 0.943 [0.835, 1.052] | 0.311 [0.260, 0.371] | 0.180 [−0.001, 0.210] |
| p: T2 decision-relevant / equivalent | 0.0001 / 1.0 | 0.0001 / 1.0 | 0.0001 / 1.0 | 0.746 / 0.255 |
| p: T3 decision-relevant / equivalent | 0.0001 / 1.0 | 0.0001 / 1.0 | 0.0057 / 0.994 | 1.0 / 0.0001 |
| **Holm, code (m = 5):** T1 | 0.0005 | 0.0005 | 0.0471 | 0.9699 |
| Holm, code: T2 dr / T3 dr | 0.0005 / 0.0005 | 0.0005 / 0.0005 | 0.0005 / 0.0228 | 1.0 / 1.0 |
| **Holm, m = 3 with decision-relevant p:** T1 / T2 / T3 | 0.0003 / 0.0003 / 0.0003 | 0.0003 / 0.0003 / 0.0003 | 0.0157 / 0.0003 / 0.0114 | 0.727 / 1.0 / 1.0 |
| **Holm, m = 3 with equivalence p:** T1 / T2 / T3 | 0.0003 / 1.0 / 1.0 | 0.0003 / 1.0 / 1.0 | 0.0471 / 1.0 / 1.0 | 0.485 / 0.485 / 0.0003 |

Notes:
- p = 0.0001 is the resolution floor of 10,000 draws. With n = 6 the exact floor is 1/64 = 0.0156, and with n = 2 it is 1/4; the ChartQA p-values are those floors.
- No reading changes between m = 5 and m = 3. The 7B ChartQA "T3 equivalent, p = 0.0001" comes from two items and means nothing.
- ρ varies with the template because the ceiling does: ρ_bind by template is 1.78, 1.24, 2.59, 1.13 (3B) and 1.15, 1.08, 1.75, 0.89 (7B).

### 5.2 Deletion versus insertion

Oriented toward the source the flipped verdict names; item means; 95% bootstrap CIs.

| Contrast (binding) | 3B Math | 7B Math | 3B ChartQA | 7B ChartQA |
|---|---:|---:|---:|---:|
| flip − own (CDE) | 0.233 | 1.619 | 0.461 | 0.233 |
| none − own (deletion) | 0.137 [0.088, 0.189] (59%) | **1.515 [1.246, 1.799] (93.6%)** | 0.188 [0.047, 0.395] (41%) | 0.065 (28%) |
| flip − none (insertion) | 0.096 [0.043, 0.149] (41%) | **0.103 [−0.088, 0.289] (6.4%)** | 0.273 [0.181, 0.374] (59%) | 0.168 (72%) |
| para_flip − none (template insertion) | 0.091 [0.046, 0.136] | 0.718 [0.564, 0.884] | 0.369 [0.265, 0.474] | 0.182 |
| para − own (rewording) | 0.003 [−0.028, 0.034] | −0.141 [−0.276, −0.002] | −0.046 | −0.017 |

Non-binding 7B Math: deletion 1.258, insertion 0.084 [−0.092, 0.254].

By the side of the own verdict (binding, cell means): when the own verdict names the image, insertion is −0.014 (3B) and −0.038 (7B); when it names the text, +0.124 and +0.166.

What this means for "the verdict steers the model":
- [Verified] In 7B Math the model's own reliability sentence strongly anchors Δℓ to its source. Removing it returns Δℓ to the order-driven baseline. A minimally edited reversed sentence does not push beyond that baseline; a clean template sentence does (+0.72).
- [Inferred] "Reversing the verdict moves the answer toward the newly named source" is supported in 7B Math only for template verdicts. For minimal-edit flips the supported statement is "the own verdict holds the answer; without it the answer reverts".
- [Inferred] 3B Math and 3B ChartQA show both components. ChartQA numbers rest on 6 and 2 items.
- [Hypothesis] The flip keeps the original justification, which contradicts the swapped noun (M2), weakening it.

### 5.3 Teacher-forced Δℓ versus behaviour

| Group | Parser | Attributable rows | Sign agreement | Majority baseline | AUC within order (image-first / text-first) |
|---|---|---:|---:|---:|---|
| 3B Math | strict | 1,057/1,920 | 51.6% | 55.2% | 0.531 / 0.561 |
| 3B Math | lenient | 1,331/1,920 | 50.3% | 55.3% | 0.549 / 0.557 |
| 7B Math | strict | 1,030/2,760 | 56.6% | 75.9% | 0.699 / 0.684 |
| 7B Math | lenient | 2,461/2,760 | 57.4% | 58.5% | 0.753 / 0.693 |
| 3B ChartQA | strict | 109/144 | 99.1% | 99.1% | 1.0 / — |
| 7B ChartQA | strict | 48/48 | 97.9% | 87.5% | 1.0 / 0.989 |

Why Math is near chance and ChartQA near 100%:
- [Verified] In ChartQA the behavioural decode starts at the same `####` position where Δℓ is scored (`transplant_v5.py:262-264`), so behaviour is essentially the greedy token of the distribution Δℓ summarises. The agreement is close to built in. In 3B ChartQA, 108 of 109 attributable answers are the chart answer, so 99.1% is also the majority baseline: there is no variation to explain.
- [Verified] In Math, behaviour is produced after up to 512 tokens of working that Δℓ never sees, and Δℓ's sign follows evidence order (the "answer = last-presented source" rule agrees with behaviour only 32–50% of the time, i.e. order predicts Δℓ, not the answer).
- [Inferred] The two regimes therefore measure different things under one name: in ChartQA, the immediate answer token; in Math, a pre-computation prior.

Literature context:
- Lanham et al., *Measuring Faithfulness in Chain-of-Thought Reasoning* (arXiv:2307.13702), define "early answering": truncate the chain of thought and force an answer. They report that on AQuA (algebra word problems) the chain of thought changes the final answer more than 60% of the time, and that reliance on the chain varies widely by task [Verified from the paper, pp. 3–5]. Scoring Δℓ at `####` with zero working is their 0%-of-CoT condition applied to word problems, the task type where they found the pre-reasoning answer least predictive.
- Jia & Mu, *From Decorative to Load-Bearing* (arXiv:2609.25366), find that whether written reasoning constrains the answer tracks model-relative task difficulty, and restrict their claim to the text → answer link [Verified from the paper, pp. 1–2, 11]. This supports treating Math and ChartQA as potentially different mechanisms, and reporting per model.
- The preregistration's own citation for margin–behaviour agreement (75.3–82.0%, Barua et al.) was not checked here.
- The spec's restriction to a controlled direct effect, with no mediation claim (§1), is the right boundary and is unaffected by these results.

### 5.4 Offline sensitivity: Math behaviour under three parsers

"Structured" = `####`, else an explicit "answer is X"; "lenient" = v4 extractor with last-number fallback. No GPU needed.

| Metric | 3B strict | 3B structured | 3B lenient | 7B strict | 7B structured | 7B lenient |
|---|---:|---:|---:|---:|---:|---:|
| "Neither" rate | 44.9% | 42.7% | 30.7% | 62.7% | 24.3% | 10.8% |
| Competent items (of 200) | 80 | 80 | 127 | 124 | 124 | 154 |
| Behavioural Δ, binding [90% CI] | +45.6 [38.8, 52.5] | +48.8 [41.9, 55.6] | +58.1 [51.9, 64.4] | +18.3 [13.9, 22.6] | +42.6 [37.4, 47.4] | +49.6 [44.8, 54.4] |
| Behavioural Δ, non-binding | +35.6 | +36.9 | +43.8 | +16.1 | +28.7 | +32.6 |
| Matched pair (para_flip vs para), binding | +61.3 | +63.8 | +69.4 | +33.0 | +57.4 | +72.2 |
| Wording floor signed mean, binding | −5.6 | −5.6 | −8.1 | −3.0 | −1.3 | 0.0 |
| Churn, code definition, binding | 25.6% | 24.4% | 20.6% | 20.4% | 18.7% | 7.0% |
| Churn, code definition, non-binding | 28.1% | 28.1% | 20.0% | 20.4% | 18.7% | 12.2% |
| image↔text flips / attributable pairs, binding | 3/84 | 3/90 | 3/105 | 0/54 | 0/148 | 0/197 |
| image↔text flips / attributable pairs, non-binding | 6/67 | 6/70 | 8/105 | 1/54 | 10/165 | 13/200 |
| `explicit_image` → image answers | 68/160 | — | 85/160 | 71/230 | — | 208/230 |
| `explicit_text` → text answers | 83/160 | — | 107/160 | 93/230 | — | 205/230 |
| Own-verdict replay: source unchanged | 147/157 | — | 143/157 | 202/220 | — | 209/220 |

Readings [Verified numbers]:
- The 7B behavioural effect was being suppressed by the parser by a factor of about 2.7.
- The wording-floor gate (binding: signed mean within ±5 pp **and** churn ≤ 5%) still fails for 3B under every parser, on the signed mean alone. For 7B it fails on churn (7.0%) under the lenient parser and passes only if churn is redefined as flips among attributable pairs.
- Under the lenient parser, replaying the model's own verdict unchanged leaves the source unchanged in 91.1% (3B) and 95.0% (7B) of cells, so the 5% churn limit remains at or below the no-change floor for 3B.
- 2B Math under the lenient parser: 43 competent, of which 23 pass the edit gates.

### 5.5 Offline sensitivity: ChartQA and donor repair

| Change | 3B ChartQA | 7B ChartQA |
|---|---|---|
| Remove prefix-leak items (H4) | 6 → 5 items; ρ_bind 0.401 → 0.397 [0.322, 0.484]; DiD 0.104 → 0.091, p 0.016 → 0.030 | 2 → 0 items; nothing computable |
| Repair verbalization split + regime-aware nouns (H3, M1), gate counts only | competent-and-passing 6 → 7 (item 24) | 2 → 4 (items 14, 18) |
| Tolerate a unit after the number in base answers (L3) | competent 13 → 14 | 13 → 13 |
| Remaining competent failures after repair (orders) | absent 10 | too_many_swaps 9 |

Other donor-repair results: 2B Math all-donor gate pass 88 → 149 (irrelevant while 2B has no competent items under the strict rule); 3B and 7B Math unchanged.

A validity observation the counts hide [Verified]: in 11 of the 12 retained 3B ChartQA cells, Sentence 1 of the prefill is "The chart and the report give the same answer." Every item is a constructed conflict. The reliability verdict that follows is therefore issued, and then flipped, under a stated belief that there is no conflict.

---

## 6. Pre-freeze decisions and action plan

Nothing below is authorized by this audit. Each item is a decision for the researcher, to be logged in §11 of the preregistration before the freeze.

### (a) Fixable offline now, zero GPU hours

These change scoring or analysis of rows that already exist. All 29,880 rows remain usable.

| # | Change | Files | Effect shown in |
|---|---|---|---|
| 1 | Choose and fix one Math answer extractor; report strict, structured and lenient side by side | `score_v5.py:150-162` | §5.4 |
| 2 | Report churn as (i) all transitions and (ii) flips among attributable pairs, with denominators | `analyze_v5.py:360-368` | §4 H2, §5.4 |
| 3 | Add the `none` decomposition (deletion, insertion) to the primary table | `analyze_v5.py` | §5.2 |
| 4 | Add the Δℓ–behaviour agreement and within-order AUC as a reported validity diagnostic | `analyze_v5.py` | §5.3 |
| 5 | Implement the missing spec outputs: 60% gate, minimum-n enforcement of readings, non-binding reading, per-template and leave-one-out, secondary CIs, three-way intersection, duplicate and backend guard | `analyze_v5.py` | §4 M3 |
| 6 | State the Holm rule in the spec (which p-value per interval test; m) | spec §7.2 | §5.1 |
| 7 | Add an answer-in-prefix gate; add regime-aware and negation-aware verdict labelling | `transplant_v5.py`, `score_v5.py` | §4 H4, M1 |
| 8 | Run `analyze_v5.py` on `results_v5/` with `--base` and `--donor` and store the output | — | freeze record |
| 9 | Human coding of verdict labels (two coders, about 200 items); none exists for v5 | `coding_v3/` is blank | spec §8 |
| 10 | Correct `results_v5/README.md` and the Thesis runbook's analysis and render-gate commands | docs | §3.1 |

Caveat: items 1 and 7 change which items count as competent or pass the gates. The existing transplant rows for items already transplanted stay valid, but newly eligible items have no transplant rows.

### (b) Changes to model inputs: need a targeted GPU re-verification

| # | Change | Why GPU is needed | Minimum re-run |
|---|---|---|---|
| 1 | Verbalization split repair (H3) | Rescued donors produce new prefills | Transplant for newly passing items only |
| 2 | Lenient or structured competency (H1) | Newly competent items (3B +47, 7B +30, 2B +43) have no transplant rows | Transplant for those items |
| 3 | Math behavioural `none` arm redesign (H5) | Prefill text changes | `beh` cells with verdict `none`, all four families |
| 4 | Clause-restricted flips (M2) | Flip sentences change | `flip` cells, `dl` and `beh` |
| 5 | Any change to where Δℓ is scored in Math (C1) | New scoring position | All Math `dl` cells |
| 6 | `verdict_nll` span (M4) | Recomputed forward passes | `dl` cells (scoring only) |
| 7 | ChartQA `max_pixels` rerun (R8.4, still open) | New image resolution | ChartQA blocks, new run tags |
| 8 | ChartQA render gate for three models | Never recorded | `--print_example` only, no GPU memory |
| 9 | Per-invocation manifest log (M5) | Takes effect on the next run | — |

### Decisions that only the researcher can make

1. Whether Δℓ at `####` stays the sole primary outcome in Math (C1). This reopens R3, which the spec says dev numbers may not change; that conflict needs an explicit ruling.
2. Which component of the flip contrast H₁ is about (C2).
3. The competency rule for all models, which decides whether 2B has a Math result at all (H1).
4. Whether ChartQA is declared secondary now. At dev rates it cannot reach 100 items for any model, and leak removal and gate repairs roughly cancel.
5. What the wording-floor gate should measure, given that it fails for 3B under every definition tried.

---

## Appendix: commands and sources

**Scripts** (session scratchpad, `python -B`, no project writes):
- `bugs.py`: transition breakdown for `change_rate`; `####` presence and parser alternatives; `none`-arm regeneration; negation and regime labels; unswapped nouns in flips; splitter truncation with an in-memory patch; gold numbers in prefills.
- `rescue.py`: Holm under three families; bootstrap SEs; sign agreement, baselines and within-order AUC; behavioural metrics under three parsers; competency under three parsers; all-donor gate pass; donor repair simulation; ChartQA with leak items removed.
- `forensic.py`, `indep.py` (earlier this session): totals, batch-size and speed reconstruction, own-verdict replay, decomposition, independent bootstrap.
- Inline checks: manifest and gate keys and timestamps; byte sizes; `_REL_SENT` fragments; matched-pair behavioural contrast; coding sheets; test counts; normalised diff of the two End-to-End audits.

**Unit tests:** 196 passing (run earlier this session with `python -B -m unittest discover tests` from `Experiment/`; counts per file confirmed by `grep -c "def test_"`: 114, 57, 25).

**External sources:**
- arXiv:2307.13702, <https://www.alphaxiv.org/abs/2307.13702> (read: abstract, §2.3, Table 2).
- arXiv:2609.25366, <https://www.alphaxiv.org/abs/2609.25366> (read: abstract, §1, §6.1).
- Hugging Face dataset `vlm-modality-research/chartqa-evidence-conflict-v2` (checked earlier this session: 230 rows; rows 0–29 match stored gold answers).

**Not verified here:** the literature dossier's citations other than the two papers above; library versions in the unrecorded Colab sessions; anything requiring model inference.

**Self-check.** Every number in §§1–5 comes from the scripts above or from a cited file and line. Every result is labelled dev-only. Claims from prior reports appear only as items checked in §2. Proposed fixes are marked as proposals and none was applied.
