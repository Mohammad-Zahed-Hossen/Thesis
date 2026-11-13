# v5 Dev Pass: Independent Forensic Audit (second pass)

**Audit date:** 2026-11-13
**Auditor:** Claude (AI). This report is AI-generated. Treat it like any other tracking document: check it against code and data before relying on it.
**This file replaces the first-pass report at the same path.** The first pass is preserved in git (`ad58428`). In this pass the first-pass report was treated as a third non-authoritative reference: its claims were re-checked, four factual slips were found and corrected (§9.3), and several analyses it lacked were added.
**Scope:** all 39 files in `Experiment/results_v5/`, the active v5/v4 code and tests, the saved Colab transcript, both runbooks, the preregistration draft, and one external check of the ChartQA dataset on the Hugging Face Hub.
**Status of every number below: dev-only.** These are spent development items, and no group meets the code's minimum sample. Nothing here is a confirmatory or preregistered finding, and nothing here supports or refutes H₁ or H₀.

---

## 1. Executive conclusion and evidence boundary

1. **[Verified] The stored data are complete and internally consistent.**
   - All 16 JSONL files contain exactly the request grid the active code generates: 29,880 rows, with no parse errors, duplicates, missing cells or unexpected cells.
   - No likelihood is non-finite or positive. None of the 20,868 scored rows (19,488 `dl` + 1,380 base `nll`) has a `boundary_mismatch`. All have `ws_skipped = 2`.
   - The six gate reports regenerate exactly from the stored rows. All 28,200 Math rows have prompts whose hash matches the current code. All 24,360 transplant prefills match the current `make_variants`.
   - The stored ChartQA gold answers for all 30 dev items match rows 0–29 of the Hub dataset at the pinned revision (external check, §4.4).
2. **[Verified] The primary numbers reproduce.** Ceiling, CDE, ρ, DiD, CIs and p-values were recomputed with code that does not import `analyze_v5` and uses a different bootstrap seed. Point estimates agree exactly; CI bounds agree within 0.012.
3. **[Verified] Provenance is incomplete.** Most rows were computed in sessions that no stored transcript records, and each manifest describes only the last invocation (§4). Batch sizes and decoding speed in the rows are consistent with the manifests, which narrows the gap but does not close it.
4. **[Verified] New in this pass: in Math, Δℓ at `####` is only weakly coupled to what the model then answers.**
   - The sign of Δℓ agrees with the source of the model's actual answer in 51.6% (3B) and 56.6% (7B) of attributable behavioural rows. Chance is 50%.
   - The sign of Δℓ follows evidence order more than it follows an explicit instruction. Under `explicit_image` with the image first, Δℓ favours the image in only 102/320 (3B) and 198/460 (7B) rows.
   - Cells where the model's answer switched to the flipped source do not show a larger Δℓ shift than cells where it did not.
   - This is a construct-validity question for the primary outcome in the Math regime (§10.1). It is a dev observation, not a finding.
5. **[Verified] New in this pass: for 7B Math, almost all of the CDE comes from deleting the model's own verdict, not from the reversed verdict.** Relative to the no-verdict prefix, the minimal-edit flip adds 0.10 (95% CI [−0.09, 0.29]) under binding, against a total CDE of 1.62. The template paraphrase naming the opposite source adds 0.72 [0.56, 0.88]. So "the answer moved toward the source the reversed verdict names" is not what the 7B flip contrast mostly measures (§8.3).
6. **[Verified] New in this pass: replaying the model's own verdict unchanged already changes answers.** With the same prompt, the same model, greedy decoding and the model's own verbalization as an exact prefix, only 57% (3B) and 53% (7B) of continuations are byte-identical to the donor's, and the answer source changes in 6.4% and 8.2% of cells. The preregistered 5% churn limit therefore sits below the replay floor in Math (§8.5).
7. **[Verified] Feasibility problems that must be settled before the freeze** (unchanged from the first pass, re-verified):
   - Qwen2-VL-2B writes no `####` in any of its 1,200 Math generations, so 0/200 items are competent under the strict rule. This is a format-eligibility failure, not a measured accuracy.
   - ChartQA retains 6 (3B), 2 (7B) and 0 (2B) items. The preregistration's §8 gate (≥ 60% of competent items pass the edit gates) fails for all three and is not implemented in code.
   - The ChartQA render gate is not in the transcript. Human coding of verdict labels has not been done. The ChartQA `max_pixels` decision (R8.4) is open.
   - The behavioural wording floor fails in both retained Math models (churn 20.4–28.1%).

**Evidence boundary.** No `analyze_v5.py` run on these data is recorded: there is no `results_v5/analysis_dev/` and no transcript of the command. Every analysis number here was computed in memory by this audit. No project file other than this report was written.

---

## 2. Evidence hierarchy and audit method

Trust order as specified: rows → manifests and gates → active code → transcript → runbooks → preregistration draft → tracking documents and the three earlier reports.

Method (all read-only):

- Scratch scripts lived in the session scratchpad, outside the repository, and ran with `PYTHONDONTWRITEBYTECODE=1 python -B`.
- **Integrity and regeneration** (first pass, outputs re-read; totals re-run this pass): grid checks against `harness_v5` / `transplant_v5` request builders; gate regeneration with `transplant_v5.plan`; prompt rebuild with `build_content` / `build_base_content` using question text from `results_v3/full_experiment_results v3.0.json`; prefill rebuild with `make_variants`.
- **Statistics, three ways:**
  1. `analyze_v5.analyze_group` with code defaults (seed 42, 10,000 resamples and draws);
  2. a point-estimate cross-check from raw `dl` fields;
  3. this pass: a separate implementation of the item bootstrap, ratio bootstrap, sign-flip test, behavioural Δ and churn, with seeds 2026 and 7. Only the answer parsers in `score_v5` were reused, because they define the outcome.
- **New forensic checks this pass:** batch-size and speed reconstruction from `wall_s`; own-verdict replay; Δℓ-versus-behaviour agreement; decomposition of the CDE through the no-verdict prefix; per-template and per-direction effects; candidate-string checks.
- **Unit tests:** `python -B -m unittest discover tests` gave 196 tests, OK (first pass). They write only to OS temp directories.
- **External check:** one, of the ChartQA dataset on the Hub (§4.4). No paper or citation claim was needed to answer the audit questions, so no literature search was run. Citation statements in the preregistration were **not verified** by this audit.

One assumption: the v3 question text equals the Hub text for the Math items [Inferred; the 100% prompt-hash match supports it].

---

## 3. Complete artifact inventory

`Experiment/results_v5/` holds 39 files: 16 JSONL, 16 manifests, 6 gate reports and `pip_freeze.txt`. There is no Qwen2-VL-2B transplant JSONL or manifest, because both 2B transplant runs stopped with "No requests" (`transplant_v5.py:382-384`).

### 3.1 JSONL files

Expected rows per item, from the code:
- base = 4 (2 generations, 2 gold-answer `nll` scores; `harness_v5.py:614-629`);
- donor = 4 (`donor` and `free_binding` × 2 orders; `:632-654`);
- transplant = 120 (12 cells × 4 templates × 2 orders = 96 `dl`, plus 12 × 1 × 2 = 24 `beh`; `transplant_v5.py:252-295`).

| File (`v5dev_…`) | Model | Stage | Items | Rows (= expected) | Capped generations | Scored rows: mismatch / `ws_skipped` |
|---|---|---|---:|---:|---:|---|
| `conflict_base_qwen2` | 2B | base | 200 | 800 | 11/400 | 0 / all 2 |
| `conflict_base_qwen25` | 3B | base | 200 | 800 | 9/400 | 0 / all 2 |
| `conflict_base_qwen25_7b` | 7B | base | 200 | 800 | 10/400 | 0 / all 2 |
| `conflict_donor_qwen2` | 2B | donor | 200 | 800 | 6/800 | — |
| `conflict_donor_qwen25` | 3B | donor | 200 | 800 | 7/800 | — |
| `conflict_donor_qwen25_7b` | 7B | donor | 200 | 800 | 1/800 | — |
| `conflict_tp_qwen25` | 3B | transplant | 80 | 9,600 | 13/1,920 | 0 / all 2 (7,680 `dl`) |
| `conflict_tp_qwen25_7b` | 7B | transplant | 115 | 13,800 | 0/2,760 | 0 / all 2 (11,040 `dl`) |
| `chartqa_base_qwen2` | 2B | base | 30 | 120 | 0/60 | 0 / all 2 |
| `chartqa_base_qwen25` | 3B | base | 30 | 120 | 0/60 | 0 / all 2 |
| `chartqa_base_qwen25_7b` | 7B | base | 30 | 120 | 0/60 | 0 / all 2 |
| `chartqa_donor_qwen2` | 2B | donor | 30 | 120 | 0/120 | — |
| `chartqa_donor_qwen25` | 3B | donor | 30 | 120 | 0/120 | — |
| `chartqa_donor_qwen25_7b` | 7B | donor | 30 | 120 | 1/120 | — |
| `chartqa_tp_qwen25` | 3B | transplant | 6 | 720 | 0/144 | 0 / all 2 (576 `dl`) |
| `chartqa_tp_qwen25_7b` | 7B | transplant | 2 | 240 | 0/48 | 0 / all 2 (192 `dl`) |

Every file: 0 unparseable lines, 0 duplicate `(id, key)` pairs, 0 missing and 0 unexpected cells, one `run_tag`, one `model_id`, `phase = dev`.

Totals [Verified, re-run this pass]:
- 29,880 rows: Math 28,200 (base 2,400, donor 2,400, transplant 23,400); ChartQA 1,680 (360, 360, 960).
- By outcome: 19,488 `dl`, 1,380 `nll`, 9,012 `beh` (4,872 of them in transplant files).

Item sets [Verified]:
- Math: 163 GSM8K + 37 SVAMP items; the same 200 ids and gold answers in all three models' files; all 200 are in the dev split that `harness_v4.split_phase` produces from the v3 item list.
- ChartQA: ids 0–29 in all three models' files; id 45 is not among them, so the audited exclusion does not affect the dev set.
- No stored pair has equal gold answers. `candidate_text` leaves every dev gold answer unchanged, and all are numeric.

### 3.2 Gate reports

Each report's `passed_ids` equals the item set of its transplant JSONL (4/4 non-empty cases), and all six regenerate exactly with `transplant_v5.plan`.

`fail_reasons_by_order` counts **orders**, not items (`transplant_v5.py:340-344`). An item failing in both orders contributes 2.

### 3.3 Manifests

All 16 manifests record [Verified]:
- `torch.bfloat16`, `NVIDIA L4`, CUDA 13.0, torch `2.14.1+cu130`, transformers `5.22.1`, Python 3.13.16;
- `repetition_penalty 1.0`, `do_sample false`, `min_pixels 100352`, `max_pixels 200704`, `dev_size` 200 / 30;
- the pinned model revisions (`harness_v4.py:45-50`) and dataset revisions (`:51-54`);
- batch size 8 for 2B and 3B, 2 for 7B;
- `resolved_model_commit: null`.

Every `scripts_sha256` entry matches the current local file, and the Drive byte sizes in the transcript (`v5_dev_output.md:27-33`) equal the local sizes.

| Model | `peak_vram_gb` | bf16 weights (parameter counts from CLAUDE.md) | Reading |
|---|---|---|---|
| 2B | 4.1145 in all four | 2,209.0M × 2 bytes = 4.11 GiB | equals the weights [Inferred: load-only] |
| 3B | 6.9936 in all six | 3,754.6M × 2 bytes = 6.99 GiB | equals the weights [Inferred: load-only] |
| 7B | 15.45–15.70 | 8,292.2M × 2 bytes = 15.45 GiB | at most +0.25 GiB over the weights |

Caveats [Verified from code]:
- `generation_config` in a manifest is the model's default (`do_sample: true`, `repetition_penalty 1.05`), not the call. The harness overrides both per call (`harness_v5.py:476-484`); the call-time values are in `config`.
- `peak_vram_gb` is read when the manifest is written, at the end of the last invocation (`harness_v4.py:439`; `harness_v5.py:771-773`). A resume that writes 0 rows records the load footprint only.
- `write_manifest` refuses a changed `config` but only warns on changed script hashes (`harness_v4.py:612-617`). The warning goes to stderr and is not stored.

### 3.4 `pip_freeze.txt`

[Verified] `transformers==5.22.1`, `torch==2.14.1+cu130`, `accelerate==1.15.0`, `datasets==4.8.5`, `pillow==11.3.0`, `qwen-vl-utils==0.0.14`, `tokenizers==0.23.3`, `numpy==2.4.6`. No Python version (that is in the manifests).

It was written in the 09:14 session after an unpinned `pip install -q` (`v5_dev_output.md:39-46`). It describes that session, not necessarily the earlier ones [Inferred]. v4 dev used transformers 5.22.2 (`results_v4/dev2_qwen25.manifest.json:49`), which the runbook recommends (`RUNBOOK_v5.md:28`); v5 recorded 5.22.1.

---

## 4. Execution, environment, and provenance audit

### 4.1 What each recorded invocation did

Source: `Thesis/docs/Archive/v5_dev_output.md`.

| Block | Stage | Transcript line | Rows newly written | Status |
|---|---|---|---:|---|
| 3B Math | base / donor / tp | 223, 229, 236 | 0 / 0 / 0 | resumed; computed earlier, unrecorded |
| 2B Math | base / donor / tp | 266, 272, 275-276 | 0 / 0 / — | resumed; tp "No requests" |
| 3B ChartQA | base / donor / tp | 306, 312, 319 | 0 / 0 / 0 | resumed |
| 2B ChartQA | base / donor / tp | 351, 357, 360-361 | 0 / 0 / — | resumed; tp "No requests" |
| 7B Math | base | 391 | 0 | resumed |
| 7B Math | donor | 399-400 | 354 of 800 | partial resume |
| 7B Math | tp | 409-411 | 13,800 | computed in the recorded session |
| 7B ChartQA | base / donor / tp | 443-447, 455-456, 465-467 | 120 / 120 / 240 | computed in the recorded session |

Row-level corroboration [Verified]:
- The 7B Math transplant `wall_s` sums are 82.8 min (`dl`) and 256.4 min (`beh`); the transcript shows 82.9 and 339.4 − 82.9 = 256.5.
- The last 354 rows of the 7B Math donor file are exactly the `free_binding` rows the transcript says were written (154 `image_first` + 200 `text_first`), and their `wall_s` sums to 43.4 min, the transcript's figure.

### 4.2 Are the unrecorded rows from the same code and setup?

| Check | Result | Tag |
|---|---|---|
| Prompt hash (`content_sha1`) of all 28,200 Math rows vs current code | all match | [Verified] |
| Prefill and `named_source` of all 24,360 transplant rows vs current `make_variants` | all match | [Verified] |
| Gate reports regenerate from stored rows | exact, 6/6 | [Verified] |
| Batch size, reconstructed from runs of identical `wall_s` in file order | 8 in every 2B and 3B file, 2 in every 7B file, including the unrecorded sessions | [Verified] |
| Decoding speed across sessions, 7B Math donor | first 446 rows 0.0391 s/token; last 354 rows 0.0399 s/token | [Inferred: same GPU class] |
| ChartQA prompts | not rebuilt (dataset not local) | [Unknown] |
| Library versions, scoring code path and resolved model commit in the unrecorded sessions | no record | [Unknown] |

`content_sha1` covers the user-turn content list only. It does not cover the rendered chat string, the token ids or the scoring code.

Timeline evidence [Inferred]: the Drive copies of the scripts are dated Nov 6–11 (`v5_dev_output.md:27-33`), the last commit touching them is 2026-11-11 14:37 +0600, the Drive `__pycache__` is dated Nov 12 03:45, and `results_v5/` Nov 12 09:08. This is consistent with all sessions falling on Nov 12 with unchanged code. Modification times are not proof.

### 4.3 GPU class

- [Verified] NVIDIA L4, 23,034 MiB by `nvidia-smi` (`v5_dev_output.md:62`). The preregistered class says "at least 24 GB" and names the L4 as eligible (`RUNBOOK_v5.md:3`).
- [Unknown / not recorded] compute capability. That bf16 loaded is indirect evidence: `harness_v4.py:401-402` selects bf16 only at major capability ≥ 8, and `check_dtype` stops otherwise (`harness_v5.py:436-447`).

### 4.4 External check: ChartQA dataset on the Hub

[Verified externally, 2026-11-13] Source: <https://hf.co/datasets/vlm-modality-research/chartqa-evidence-conflict-v2> (dataset viewer, config `default`, split `test`).
- The split has 230 rows.
- The viewer's asset URLs carry revision `7d15a9704bc5e028e7038ef98aa7917059535bf8`, the pinned revision.
- Rows 0–29 have `conflict_id` 0–29, and their `chart_answer` / `report_answer` equal the stored `y_image` / `y_text` for all 30 dev items.

What this does not show: which revision the Colab sessions actually loaded (`resolved_model_commit` is null and no dataset fingerprint is stored).

---

## 5. Runbook and transcript audit

| Item | `Experiment/RUNBOOK_v5.md` | `Thesis/docs/RUNBOOK/RUNBOOK_V5.md` | Transcript |
|---|---|---|---|
| Local unit tests before GPU | required (`:11-16`) | not listed | not recorded |
| Install | unpinned; "use 5.22.2 if you can" (`:25-28`) | unpinned (`:73`) | unpinned; got 5.22.1 |
| Render gate, Math × 3 models | `:33-35` | `:92-94` | run (`:81-195`) |
| Render gate, ChartQA × 3 models | required (`:36-38`) | absent | **absent** |
| Blocks 1–6 | `:57-105` | present | all six recorded |
| Analysis command | with `--base` and `--donor` (`:139-142`) | omits both (`:248`) | **not run / not recorded** |
| lme4 fits | `:150-158` | not listed | not run |
| ChartQA `max_pixels` rerun if `base_image` yield is low | `:115-117` | — | not done |

- [Verified] The Thesis runbook matched git HEAD except for whitespace when first audited; it has since been committed.
- [Verified] Omitting `--base` / `--donor` leaves ceiling, T1, T2 and T3 identical and drops the `manipulation_check` and `relative_uncertainty_binding` secondaries. The manipulation check is one of the R8.3 freeze-record items.
- [Verified] The Math render printouts show, in both orders: instruction first, `Image: <|vision_start|><|image_pad|><|vision_end|>`, the typed-text block on the other side, the format line last, no source letters, and the prefill `The verdict.\n\n####`. This matches `harness_v5.py:201-219`.
- [Unknown] The 3B printout has three blank lines between the instruction and `Image:` (`v5_dev_output.md:95-99`); 2B and 7B have one. The code emits `\n\n`. Probably a copy artifact; the rendered strings are not stored.
- [Verified] The Thesis runbook's disconnect recovery re-runs an unpinned `pip install` (`:231`), so sessions can differ in library versions while only the last is recorded.

---

## 6. Code-to-design verification

"Prereg" is `Docs/PREREGISTRATION_VERDICT_TRANSPLANT.md`, a draft.

| Design element | Implemented fact | Prereg | Agreement |
|---|---|---|---|
| Order counterbalancing, no letters | Only the two sources swap; instruction first, format line last; modality headers (`harness_v5.py:201-219`); both orders in donor, transplant and ceilings (`transplant_v5.py:271`) | §4.1, R2 | ✓ |
| Templates K = 4 | Literal stems and endings for non-binding, binding, explicit; both regimes (`harness_v5.py:57-109`) | §§4.2, 4.4 | ✓ |
| Explicit ceilings | `explicit_image` / `explicit_text` with `m_none` prefilled (`transplant_v5.py:252-255`); 0/160 sampled `none` prefills contain "reliab" | §4.3 | ✓ |
| Donor and `free_binding` | k = 1, both orders, nothing forced (`harness_v5.py:632-654`) | §5.1, §7.5 | ✓ |
| Variants | own / flip / none / para / para_flip (`transplant_v5.py:197-225`) | §5.2 | ✓ |
| Gate 1 | exactly one sentence differs; `none` removes one (`:228-231`) | §5.3.1 | ✓ |
| Gate 2 | parser gives opposite / own / opposite / absent (`:233-238`) | §5.3.2 | ✓ |
| Gate 3a | set Jaccard ≥ 0.85 (`:47, 240`) | §5.3.3a | ✓ |
| Gate 3b | ≤ 2 swapped noun phrases (`:48, 242`) | §5.3.3b | ✓ |
| Gate 4 | regex for agreement and article errors (`:128-159, 245`) | §5.3.4, plus a human check of 50 variants per model | regex ✓; human check not done |
| Gate 5 | own verdict names a source of the regime (`:200-202`) | §5.3.5 | ✓ |
| Both orders must pass | `:339-344` | §5.3 | ✓ |
| Strict competency | gold answer via `behavioural_source`; Math last-number fallback counts as no answer (`harness_v5.py:657-673`; `score_v5.py:150-162`) | §3.3, §6.2 | ✓ |
| Δℓ | `lp_I/n_I − lp_T/n_T` (`score_v5.py:206-210`); prefill ends at `####`; candidate `" " + candidate_text(y)`; exact token-prefix check; leading whitespace token skipped (`harness_v5.py:497-555`) | §6.1 | ✓ |
| CDE orientation | s = −1 if own source is image-side, else +1; CDE = s·(Δℓ_flip − Δℓ_own); mean over 4 k × 2 orders per item (`analyze_v5.py:87-90, 265-292`) | §7.1 | ✓ |
| Ceiling | Δℓ(explicit_image, none) − Δℓ(explicit_text, none) (`:305-314`) | §4.3 | ✓ |
| ρ | mean CDE / mean Ceil; 90% item bootstrap; only if the Ceil 95% CI excludes 0 (`:541-559`) | §7.2, R4 | ✓ |
| T1 | one-sided sign-flip on item DiD, p = (1 + b)/(draws + 1) (`:143-152`) | R7 | ✓ |
| Holm | within model × regime, over T1 and bootstrap p-values for T2/T3 (`:155-161, 536-560`) | §7.2 | ✓ |
| Behavioural TOST | ε = 0.05, 90% CI (`:48, 175-176, 565-571`) | R4 | ✓ |
| Wording floor | signed mean ≤ ε and churn ≤ 5% (`:201-227, 360-368`) | §7.6 | ✓ |
| R5 minimum | `MIN_ITEMS` 150 / 100 sets a flag (`:56, 520`) | R5 | flag only; `reading_binding` is still emitted (`:588`) |
| §8: edit-gate pass ≥ 60% | not implemented | line 416; "If a gate fails, the run stops" (line 423) | ✗ gap |
| §8: boundary mismatch ≤ 1% | reported (`:509-510`), not enforced | line 415 | reported only |
| Size comparison | Δρ on the intersection; no minimum n (`:632-698`) | §7.2 | ✓ as descriptive |

Further observations [Verified]:

- **Sign-flip p floors.** With 10,000 random draws the smallest reportable p is 1/10,001. For small n the exact floor is higher: 1/2⁶ = 0.0156 at n = 6 and 1/4 at n = 2. The 3B ChartQA p of 0.0157 is that floor (all six items positive), not a measured strength.
- **`stated_reliable_source` is a heuristic.** It treats "visual" as an image-side noun (`score_v5.py:35-50`). One 7B ChartQA donor says "The chart, being a **visual** representation of the data, is considered more reliable"; it was labelled `image` and dropped as `own_wrong_regime`. Human coding (§8 of the prereg) has not been run.
- **Gate 3b drops verdicts that justify themselves by contrast.** All 16 `gate3_too_many_swaps` failures (8 Math 7B, 8 ChartQA 7B, counted by order) have exactly 3 source nouns in the reliability sentence.
- **Candidate answers are scored as prefixes.** No end-of-answer token is scored, so a candidate's probability includes longer numbers that start with it. In 8 of 200 Math dev items one candidate is a string prefix of the other (2 of 80 in the 3B transplant set, 5 of 115 in 7B; none in ChartQA). Token counts differ between the two candidates in 53/80 (3B) and 80/115 (7B) Math items, so length normalisation is active for most items.
- **ChartQA behavioural decodes are prefilled through `####`** (`transplant_v5.py:262-265`), the same position where Δℓ is scored. Math decodes are prefilled with `{m}\n\n` and solve freely.

---

## 7. Stage-by-stage empirical audit

### 7.1 Competency (strict rule)

| Regime | Model | `base_image` correct | `base_text` correct | Competent | Parse methods (image / text arm) |
|---|---|---:|---:|---:|---|
| Math (200) | 2B | 0 | 0 | **0** | fallback 200 / fallback 200 |
| Math (200) | 3B | 114 | 138 | **80** | hash 148, fallback 52 / hash 162, fallback 38 |
| Math (200) | 7B | 168 | 148 | **124** | hash 188, fallback 12 / hash 161, fallback 39 |
| ChartQA (30) | 2B | 10 | 20 | **10** | first_line 27, none 3 / first_line 30 |
| ChartQA (30) | 3B | 14 | 26 | **13** | hash 21, first_line 9 / first_line 16, hash 14 |
| ChartQA (30) | 7B | 13 | 28 | **13** | hash 30 / hash 30 |

- **2B Math [Verified].** None of 2B's 1,200 Math generations contains `####`; none contains `\boxed`. Outputs end in prose. With the lenient last-number rule, 70/200 image and 101/200 text answers match gold and 43 items pass both [Inferred: the fallback can pick a wrong number]. Δℓ is teacher-forced and does not need the model to emit `####`; only the competency filter does.
- **Capped base generations** (11, 9 and 10 rows) are never counted correct.
- **Intersections (R8.3):** three-way Math 0, ChartQA 8; 3B ∩ 7B Math 54, ChartQA 11.
- **ChartQA `base_image` yield** is 10–14/30 against 20–28/30 for `base_text`. This is the runbook's trigger for the `max_pixels` rerun, which has not been done.

### 7.2 Natural donor verdicts by order

Rows are (item, order). Labels come from the unvalidated parser.

| Regime | Model | Scope | `image_first` | `text_first` |
|---|---|---|---|---|
| Math | 2B | all 200 | text 142, image 50, undetermined 5, absent 3 | text 93, absent 97, image 9, undetermined 1 |
| Math | 3B | all 200 | text 128, image 72 | text 199, image 1 |
| Math | 3B | competent 80 | text 48, image 32 | text 79, image 1 |
| Math | 7B | all 200 | image 125, text 74, undetermined 1 | text 200 |
| Math | 7B | competent 124 | image 75, text 48, undetermined 1 | text 124 |
| ChartQA | 2B | all 30 | absent 26, chart 2, undetermined 2 | absent 25, undetermined 4, chart 1 |
| ChartQA | 3B | all 30 | absent 18, report 12 | absent 14, report 15, chart 1 |
| ChartQA | 7B | all 30 | chart 16, report 10, absent 4 | report 19, chart 4, absent 6, "image" 1 |

[Verified] In Math, when the typed text comes **first**, 3B and 7B almost always name the typed text. When the image comes first, verdicts are mixed. The verdict asymmetry is primacy-like for text; it is not recency.

Donor structure [Verified]:
- 2B Math: 100/400 donor rows have no reliability sentence, and 166/400 stop after the verbalization with no solution.
- 3B and 7B Math: every donor row has exactly one reliability sentence.
- 3B ChartQA: 32/60 have no reliability sentence, and 29/60 have nothing after the verbalization.

### 7.3 Edit gates

| Regime | Model | Competent | Passed | Rate | §8 ≥ 60% | Fail reasons (orders) | Multiset Jaccard mean / min | Swaps per flip |
|---|---|---:|---:|---:|---|---|---|---|
| Math | 2B | 0 | 0 | — | — | — | — | — |
| Math | 3B | 80 | 80 | 100% | pass | — | 0.9455 / 0.8800 | 1: 119, 2: 41 |
| Math | 7B | 124 | 115 | 92.7% | pass | too_many_swaps 8, undetermined 1 | 0.9549 / 0.8750 | 1: 175, 2: 55 |
| ChartQA | 2B | 10 | 0 | 0% | **fail** | absent 18, undetermined 2 | — | — |
| ChartQA | 3B | 13 | 6 | 46.2% | **fail** | absent 11 | 0.8936 / 0.8667 | 1: 10, 2: 2 |
| ChartQA | 7B | 13 | 2 | 15.4% | **fail** | too_many_swaps 8, absent 3, wrong_regime 1 | 0.9774 / 0.9481 | 1: 1, 2: 3 |

Own source among passed items, by order:
- Math 3B: `image_first` image 32 / text 48; `text_first` text 79 / image 1.
- Math 7B: `image_first` image 71 / text 44; `text_first` text 115.
- ChartQA 3B and 7B: report in every passed order, so every ChartQA flip names the chart.

---

## 8. Independently reproduced primary and secondary results

**All values: dev-only, spent items, below the code's minimum sample.**

### 8.1 Primary Δℓ quantities

From `analyze_v5.analyze_group` (seed 42). The separate implementation (seed 2026) gave identical point estimates and CI bounds within 0.012.

| Quantity | 3B Math | 7B Math | 3B ChartQA | 7B ChartQA |
|---|---:|---:|---:|---:|
| Items analysed (minimum) | 80 (150) | 115 (150) | 6 (100) | 2 (100) |
| `meets_min_items` | false | false | false | false |
| Boundary mismatch | 0/7,680 | 0/11,040 | 0/576 | 0/192 |
| Ceil_ℓ [95% CI] | 0.152 [0.117, 0.193] | 1.423 [1.214, 1.633] | 1.148 [0.903, 1.401] | 0.956 [0.269, 1.644] |
| Ceil, image direction | −0.009 [−0.041, 0.021] | 0.670 [0.559, 0.790] | 0.607 [0.446, 0.766] | 0.409 [0.101, 0.718] |
| Ceil, text direction | 0.161 [0.117, 0.212] | 0.753 [0.609, 0.903] | 0.541 [0.442, 0.651] | 0.547 [0.168, 0.926] |
| CDE_bind [95% CI] | 0.233 [0.182, 0.291] | 1.619 [1.337, 1.919] | 0.461 [0.338, 0.624] | 0.233 [0.005, 0.461] |
| CDE_nonbind [95% CI] | 0.150 [0.106, 0.204] | 1.342 [1.082, 1.626] | 0.357 [0.252, 0.494] | 0.172 [−0.000, 0.344] |
| CDE_bind item median | 0.170 | 1.093 | 0.432 | 0.233 |
| ρ_bind [90% CI] | 1.529 [1.258, 1.865] | 1.138 [1.022, 1.254] | 0.401 [0.332, 0.475] | 0.244 [0.018, 0.281] |
| ρ_nonbind [90% CI] | 0.984 [0.736, 1.305] | 0.943 [0.835, 1.052] | 0.311 [0.260, 0.371] | 0.180 [−0.001, 0.210] |
| Code reading T2 / T3 | decision-relevant / decision-relevant | decision-relevant / decision-relevant | decision-relevant / decision-relevant | inconclusive / equivalent |
| DiD [95% CI] | 0.083 [0.051, 0.113] | 0.277 [0.220, 0.336] | 0.104 [0.053, 0.152] | 0.061 [0.005, 0.117] |
| T1 sign-flip p | 1.0e-4 (floor) | 1.0e-4 (floor) | 0.0157 (= 1/64 floor) | 0.2425 (= 1/4 floor) |
| Holm p: T1 | 0.0005 | 0.0005 | 0.0471 | 0.9699 |
| Holm p: T2 decision-relevant / equivalent | 0.0005 / 1.0 | 0.0005 / 1.0 | 0.0005 / 1.0 | 1.0 / 0.9699 |
| Holm p: T3 decision-relevant / equivalent | 0.0005 / 1.0 | 0.0005 / 1.0 | 0.0228 / 1.0 | 1.0 / 0.0005 |
| Items with CDE_bind > 0 | 73/80 | 108/115 | 6/6 | 2/2 |
| `reading_binding` string emitted by the code | "H1 … binding strengthens it" | same | same | "inconclusive" |

[Verified] The code emits H₁-style strings for three groups with `meets_min_items = false`. **They are not findings.** With n = 2 and n = 6, the ChartQA intervals and p-values carry no inferential weight.

**Per-template values** [Verified]. The CDE is stable across templates; the ceiling is not, so ρ varies by template.

| Template k | 3B Math: CDE_bind / Ceil / ρ | 7B Math: CDE_bind / Ceil / ρ |
|---:|---|---|
| 1 | 0.221 / 0.124 / 1.78 | 1.615 / 1.401 / 1.15 |
| 2 | 0.224 / 0.182 / 1.24 | 1.695 / 1.573 / 1.08 |
| 3 | 0.254 / 0.098 / 2.59 | 1.517 / 0.867 / 1.75 |
| 4 | 0.232 / 0.206 / 1.13 | 1.648 / 1.851 / 0.89 |

### 8.2 Order structure in raw Δℓ

Mean raw Δℓ under non-binding with no verdict. Positive favours the image or chart.

| Group | `image_first` | `text_first` | Shift |
|---|---:|---:|---:|
| 3B Math | −0.807 | +0.710 | +1.52 |
| 7B Math | −0.963 | +0.998 | +1.96 |
| 3B ChartQA (n = 6) | 1.076 | 0.833 | −0.24 |
| 7B ChartQA (n = 2) | 1.120 | 0.972 | −0.15 |

[Verified] In Math, Δℓ favours the **last-presented** source by 1.5–2.0 per token. That is ten times the 3B ceiling and larger than the 7B ceiling.

Does the sign of Δℓ follow the explicit instruction? Share of `dl` rows (all four templates) whose sign matches the instructed source:

| Group | `explicit_image`: image first / text first | `explicit_text`: image first / text first |
|---|---|---|
| 3B Math | 102/320 (32%) / 221/320 (69%) | 225/320 (70%) / 103/320 (32%) |
| 7B Math | 198/460 (43%) / 393/460 (85%) | 379/460 (82%) / 185/460 (40%) |
| 3B ChartQA | 24/24 / 24/24 | 8/24 / 12/24 |
| 7B ChartQA | 8/8 / 8/8 | 3/8 / 4/8 |

[Verified] In Math the sign matches the instruction mainly when the instructed source is the one presented last. In ChartQA the sign favours the chart almost regardless of instruction.

### 8.3 What the flip contrast is made of

Oriented toward the source the flipped verdict names; item means over 4 templates × 2 orders; 95% item-bootstrap CIs (seed 2026). `none` is the verbalization with the reliability sentence deleted.

| Contrast (binding) | 3B Math | 7B Math | 3B ChartQA (n = 6) |
|---|---:|---:|---:|
| flip − own (the CDE) | 0.233 [0.181, 0.290] | 1.619 [1.333, 1.933] | 0.461 [0.339, 0.624] |
| none − own (delete own verdict) | 0.137 [0.088, 0.189] | **1.515 [1.246, 1.799]** | 0.188 [0.047, 0.395] |
| flip − none (add the reversed verdict) | 0.096 [0.043, 0.149] | **0.103 [−0.088, 0.289]** | 0.273 [0.181, 0.374] |
| para − own (reword, same source) | 0.003 [−0.028, 0.034] | −0.141 [−0.276, −0.002] | −0.046 [−0.095, 0.013] |
| para_flip − para (matched pair) | 0.225 [0.180, 0.274] | 2.375 [2.024, 2.751] | 0.604 [0.468, 0.770] |
| para_flip − none | 0.091 [0.046, 0.136] | 0.718 [0.564, 0.884] | 0.369 [0.265, 0.474] |

Non-binding shows the same pattern (7B: none − own 1.258 [1.017, 1.517]; flip − none 0.084 [−0.092, 0.254]).

Split by which side the own verdict is on (binding, cell means):

| Group | Own verdict | Cells | none − own | flip − none | para_flip − none |
|---|---|---:|---:|---:|---:|
| 3B Math | text side | 508 | 0.118 | 0.124 | 0.096 |
| 3B Math | image side | 132 | 0.213 | −0.014 | 0.068 |
| 7B Math | text side | 636 | 1.526 | 0.166 | 0.793 |
| 7B Math | image side | 284 | 1.492 | −0.038 | 0.550 |

[Verified] numbers. Reading [Inferred]:
- For 7B Math, removing the model's own verdict moves Δℓ almost as far as replacing it with the reversed one. The minimal-edit flip does not move Δℓ beyond the no-verdict prefix; the clean template naming the opposite source does.
- When the own verdict names the image, a flip toward the text adds nothing over deletion in either model.
- The CDE therefore mixes two things: how strongly the own verdict anchors Δℓ to its source, and how strongly a reversed verdict attracts it to the other. The prereg's description of the CDE ("the answer moved toward the source the reversed verdict names", `analyze_v5.py:16-18`) fits the second, and in 7B Math the first dominates.
- [Hypothesis] The flipped sentence keeps the model's original justification, which no longer fits the swapped noun, and this may weaken it relative to the template sentence. Not tested.

### 8.4 Behavioural (secondary) and wording floor

| Quantity | 3B Math | 7B Math | 3B ChartQA | 7B ChartQA |
|---|---:|---:|---:|---:|
| Δ follow-flip vs own, binding [90% CI] | +45.6 pp [38.8, 52.5] | +18.3 pp [14.3, 22.6] | +8.3 pp [0, 25] | 0 |
| Δ, non-binding [90% CI] | +35.6 pp [28.1, 42.5] | +16.1 pp [11.7, 20.4] | +8.3 pp [0, 25] | 0 |
| Change rate own vs flip (binding / non-binding) | 69.4% / 55.6% | 38.3% / 31.3% | 8.3% / 8.3% | 0 / 0 |
| Wording floor, binding: signed mean / churn | −5.6 pp / **25.6%** | −3.0 pp / **20.4%** | 0 / 0 | 0 / 0 |
| Wording floor, non-binding: signed mean / churn | −1.3 pp / **28.1%** | −5.7 pp / **20.4%** | 0 / 0 | 0 / 0 |
| Floor gate (binding) | **FAIL** | **FAIL** | pass (n = 6) | pass (n = 2) |
| "Neither" rate over all `beh` rows | 44.9% | 62.7% | 24.3% | 0% |
| Parse methods | hash 1,480, fallback 438, hash_no_number 2 | fallback 1,610, hash 1,149, none 1 | hash 144 | hash 48 |

Behavioural ceilings (k = 1, both orders) [Verified]:

| Group | `explicit_image` | `explicit_text` |
|---|---|---|
| 3B Math | image 68, text 8, neither 84 (of 160) | text 83, image 1, neither 76 |
| 7B Math | image 71, text 0, neither 159 (of 230) | text 93, image 1, neither 136 |
| 3B ChartQA | image 12/12 | text 1/12, image 7/12 |
| 7B ChartQA | image 4/4 | text 2/4 |

### 8.5 Replay floor: the model's own verdict, unchanged

The cell `beh | nonbinding | own | k1` uses the same user prompt as the donor generation (identical `content_sha1` in all cells) and prefills the model's own verbalization. If decoding were reproducible, it would regenerate the donor's continuation.

| Quantity | 3B Math | 7B Math |
|---|---:|---:|
| Cells | 160 | 230 |
| Prefill is an exact string prefix of the donor text | 157 | 220 |
| … of those, continuation byte-identical to the donor's | 89 (56.7%) | 117 (53.2%) |
| … of those, same answer source | 147 (93.6%) | 202 (91.8%) |
| **Answer-source churn with no wording change** | **6.4%** | **8.2%** |
| Where divergent continuations first differ (median share of the continuation) | 0.25 | 0.31 |

[Verified] numbers. The cells that are not exact prefixes differ only in whitespace before the solution (the harness writes `\n\n`; some donors wrote ` \n\n`).

Reading:
- [Inferred] Greedy decoding here is not bit-reproducible across runs of the same prompt. The preregistered wording-floor limit (churn ≤ 5%) is below this replay floor, so the gate cannot pass in Math whatever the paraphrase does.
- [Hypothesis] Likely causes are batch composition and left-padding in `bfloat16` (the donor and transplant batches contain different neighbours), or a library difference between sessions. The stored data cannot separate them: 3B donors and transplant both came from unrecorded sessions, and 7B donors came from an earlier session than the transplant.
- [Unknown] Whether the same instability affects the base-stage generations that define competency, and whether Δℓ (scored one request at a time, without padding) is reproducible. No scored cell is duplicated in the data, so this cannot be checked from stored rows.

### 8.6 Δℓ against behaviour

For behavioural rows with an attributable answer (image or text), compared with the `dl` row of the same cell at k = 1:

| Group | Sign of Δℓ agrees with answer source |
|---|---|
| 3B Math | 545/1,057 = **51.6%** |
| 7B Math | 583/1,030 = **56.6%** |
| 3B ChartQA | 108/109 = 99.1% |
| 7B ChartQA | 47/48 = 97.9% |

Oriented Δℓ shift (flip − own, k = 1) in cells where the answer switched to the flipped source versus all other cells:

| Group | Switched: n, mean, median | Other: n, mean, median |
|---|---|---|
| 3B Math | 136, 0.183, 0.061 | 184, 0.167, 0.062 |
| 7B Math | 79, 1.151, 0.677 | 381, 1.516, 0.750 |

[Verified] numbers. Reading [Inferred]:
- In Math, Δℓ at `####` before any working neither predicts the sign of the eventual answer much above chance nor distinguishes cells where behaviour switched.
- The ChartQA agreement is close to built in: the behavioural decode starts at the same `####` position where Δℓ is scored, so it mostly restates the greedy token.
- Limits: only 55% (3B) and 37% (7B) of Math behavioural rows are attributable under the strict parser, and behaviour itself has the replay noise of §8.5.

### 8.7 Manipulation check (donor files)

| Group | `donor`: stated / attributable / follows | `free_binding`: stated / attributable / follows |
|---|---|---|
| 3B Math | 400 / 198 / 80.3% | 313 / 159 / 93.1% |
| 7B Math | 399 / 128 / 93.8% | 396 / 112 / 99.1% |
| 3B ChartQA | 28 / 0 / n/a | 12 / 0 / n/a |
| 7B ChartQA | 49 / 37 / 56.8% | 56 / 47 / 76.6% |

[Verified] For 3B ChartQA, all 27 report-verdict donor rows and the one chart-verdict row parse as "neither" (26 with method `none`, 1 `hash` for report; 1 `none` for chart). The strict parser reads the first non-empty line, which is a sentence. The check is unmeasurable there with the current parser.

### 8.8 Size comparison and other secondaries

| Regime | Intersection n | ρ_bind 3B | ρ_bind 7B | Δρ (7B − 3B) [95% CI] |
|---|---:|---:|---:|---:|
| Math | 50 | 1.369 | 1.056 | −0.314 [−0.784, 0.050] |
| ChartQA | 0 | — | — | not computable |

The code applies no minimum n. A CI that includes 0 at n = 50 on dev items is not evidence of no difference.

Other descriptive values (3B / 7B Math):
- seconds per transplanted item 60.3 / 177.0 (prereg estimate about 45–50, line 299); ChartQA 32.8 / 62.1;
- CDE_bind by order: `image_first` 0.185 / 1.751; `text_first` 0.281 / 1.487;
- CDE_bind by baseline |Δℓ| tertile: 0.178, 0.212, 0.303 / 1.061, 1.346, 2.428;
- relative-uncertainty strata: inside 0.232, outside 0.234 / inside 1.058, outside 1.854.

---

## 9. Comparison with the supplied reference reports

"AG" = `v5_antigravity_analysis.md`; "EA" = `v5_dev_evidence_audit.md`; "C1" = the first-pass version of this file (git `ad58428`).

### 9.1 Antigravity report (AG)

| # | Claim | Authoritative source | Reproduced value | Verdict | Why it matters |
|---|---|---|---|---|---|
| 1 | §4.1, §8.3: "recency bias … placing text **second** induces almost 100% text verdict" | donor rows (§7.2) | near-100% text verdicts occur with text **first** | **Wrong** | Reverses the order effect in verdicts |
| 2 | §6.1A: Ceil 0.152 is "strong single-source separation" | §8.1, §8.2 | image direction −0.009 [−0.041, 0.021]; Δℓ sign follows the instruction in 32% of image-first `explicit_image` rows | **Wrong** | ρ = 1.53 rests on this denominator |
| 3 | §6.1A/B: "binding significantly strengthens the causal effect" | `analyze_v5.py:56, 520`; R5 | n < 150, dev items, p at its floor | **Unsupported** as a claim | Reads as a finding |
| 4 | §6.1C: 7B ChartQA "inconclusive due to sample attrition" | `analyze_v5.py:164-172` | the code does not gate on n; T2 "inconclusive", T3 "equivalent" from CI geometry at n = 2 | **Incomplete** | Wrong reason; T3's "equivalent" is meaningless at n = 2 |
| 5 | §2.2: L4 "24,000 MiB", "compute capability 8.9" | transcript `:62`; manifests | 23,034 MiB; capability not recorded | **Wrong** / **unsupported** | Bears on the "≥ 24 GB" class |
| 6 | §2.1: Python 3.13.16 from `pip_freeze.txt` | file | only in manifests | **Wrong** (source) | Minor |
| 7 | §2.2: "safe from CUDA OOM" | `harness_v5.py:561-568` | OOM batches split silently; recorded VRAM is load-only for 2B/3B | **Unsupported** | Cannot be shown from manifests |
| 8 | §3.2: 2B ended with prose "or `\boxed{26}`" | 2B base rows | 0/400 contain `\boxed` | **Wrong** (detail) | Misdescribes the failure |
| 9 | §5.2: too-many-swaps from "3 or 4 nouns" | regenerated variants | all 16 have exactly 3 | **Partly wrong** | Minor |
| 10 | §7.2: churn caused by "floating-point accumulation in beam/greedy steps" | §8.4, §8.5 | paraphrase churn 20–28%; churn with **no** wording change 6–8% | **Partly supported, overstated** | Run-to-run instability is real (§8.5) but explains about a third of the paraphrase churn at most; there is no beam search |
| 11 | §7.2: the floor failure "confirms" making Δℓ primary | prereg §6, §7.6; §8.6 here | decided before data; and Δℓ agrees with Math behaviour at 52–57% | **Unsupported** | Post hoc, and the new evidence cuts the other way |
| 12 | §7.3: "no statistically significant difference" 3B vs 7B | §8.8 | n = 50, dev, descriptive | **Overstated** | Not a test |
| 13 | §7.1: manipulation check as "verbalization faithfulness" | §8.7 | percentages correct; only 198/400 and 128/400 rows attributable | **Incomplete** | Denominators omitted |
| 14 | §8 open issue 2: "`MAX_SWAPS` must be relaxed (2 → 4)" | — | — | **Unauthorized prescription** | A researcher decision |
| 15 | §4.1B: 3B ChartQA emitted bare answers like "4.10 million" | 3B ChartQA donors | 4 donor-file rows contain that string | **Supported** | — |

### 9.2 Evidence audit (EA)

| # | Claim | Reproduced | Verdict | Why it matters |
|---|---|---|---|---|
| 1 | Complete, parseable, consistent rows; 29,880 / 24,360 / 19,488 / 4,872 | same | **Correct** | — |
| 2 | Missing ChartQA render checks; runbooks differ on `--base` / `--donor`; no stored analysis | same | **Correct** | — |
| 3 | All competency, fallback (90 / 51), gate and Jaccard figures | same | **Correct** | — |
| 4 | All primary numbers, p-values, churn, size comparison, 13 capped 3B rows | same | **Correct** | — |
| 5 | "All manifests record L4 … bf16" as environment evidence | manifests are rewritten per invocation; most rows predate the recorded session | **Incomplete** | Main provenance gap not noted |
| 6 | ChartQA "may not yield 100 retained items" | competency alone implies ≈ 86 of 199 (Wilson 95% for 13/30: 0.27–0.61, i.e. ≈ 54–121); after gates ≈ 40 (3B), ≈ 13 (7B) | **Correct, understated** | Competency, not only gates, is binding |
| 7 | "ρ above one is mathematically possible" | §10.1 | **Correct, incomplete** | Omits the ceiling's order dependence and the decomposition |
| 8 | Wording-floor failure "does not invalidate the primary margins" | §8.6 | **Correct but incomplete** | The primary margin has its own validity question in Math |
| 9 | No mention of the §8 60% gate, `peak_vram` being load-only, the parser mislabel, the replay floor, or Δℓ–behaviour agreement | — | **Incomplete** | Each bears on the freeze |

### 9.3 First-pass version of this report (C1)

| # | C1 claim | Authoritative source | Reproduced value | Verdict | Why it matters |
|---|---|---|---|---|---|
| 1 | "All 28,440 Math rows" have matching prompt hashes (§1, §4.2) | row counts | 28,200 Math rows (2,400 + 2,400 + 23,400) | **Wrong** (number) | The check itself covered every Math row; only the count was misstated |
| 2 | Margin scoring ran "in all three tokenizers that reached it (two …)" (§1) | base `nll` rows | scoring ran for all three models in the base stage (1,380 `nll` rows, 0 mismatches) and for two in transplant | **Wrong** (muddled) | 2B's tokenizer handling is in fact evidenced |
| 3 | "If a gate fails, the run stops" at prereg line 422 | prereg | line 423 | **Wrong** (citation) | Minor |
| 4 | Drive scripts "dated Nov 9–11" | transcript `:27-33` | Nov 6–11 | **Wrong** (detail) | Minor |
| 5 | 3B ChartQA report-verdict donors all parse with method `none` | donor rows | 26 `none`, 1 `hash` | **Partly wrong** | Minor |
| 6 | ρ_3B "compares a mostly image-ward verdict effect with a text-ward instruction effect" | §8.1–8.3 | In the cells where 3B flips toward the image (508 of 640), the total ceiling is 0.170 and its image-direction part is −0.009 | **Correct in substance, imprecise** | Better stated as: the ceiling is small, order-dependent and has no image-direction component, so ρ is driven by a weak denominator |
| 7 | [Hypothesis] Δℓ at `####` tracks order more than instruction | §8.2, §8.6 | sign follows instruction in 32–43% of rows when the instructed source is first | **Now [Verified]** for the sign; mechanism still a hypothesis | Upgrades a hypothesis to an observation |
| 8 | "External research: none" | §4.4 | one Hub check now done | **Superseded** | — |
| 9 | T1 "p ≥ 1/10,001" | `analyze_v5.py:143-152` | also bounded by 1/2ⁿ: 0.0156 at n = 6, 0.25 at n = 2 | **Incomplete** | The ChartQA p-values are floors |
| 10 | No replay check, no Δℓ–behaviour check, no decomposition, no per-template table | §8.3, §8.5, §8.6 | added | **Incomplete** | These are the main new results |
| 11 | All inventory, manifest, transcript, competency, donor, gate, primary, behavioural, manipulation and size-comparison numbers | this pass | identical | **Correct** | — |

---

## 10. Methodological risks and unresolved pre-freeze decisions

Every possible remedy named here is a **pre-freeze decision requiring the researcher's approval**. None is authorized or recommended as settled by this audit.

### 10.1 The assessments requested

1. **Technical feasibility: [Verified] shown for the machinery.** Scoring runs on an L4 in bf16 with zero boundary failures for all three models (base stage) and two (transplant). Not shown: a confirmatory-scale ChartQA family, any 2B Math transplant, or run-to-run reproducibility of generations (§8.5).
2. **Counterbalancing: [Verified] justified on these stimuli.** Order moves raw Δℓ by 1.5–2.0 toward the last source in Math and nearly fixes the stated verdict when text comes first. Two consequences follow:
   - order and flip direction are confounded (in `text_first` almost every flip is text → image);
   - order effects are larger than the ceiling they are compared against.
3. **2B Math: [Verified] an eligibility issue created by the strict format rule**, not an accuracy conclusion. *Decision:* whether the competency rule changes, for all models, as a logged deviation before the freeze.
4. **ChartQA attrition: [Inferred] the confirmatory ChartQA family is very unlikely to reach 100 items for any model.** Competency alone caps 3B and 7B near 86 of 199. The dev n of 30 makes this imprecise. *Decisions:* the `max_pixels` rerun; whether ChartQA is declared secondary; what to do about the unimplemented 60% gate that, as written, stops the run.
5. **Wording floor: [Verified] fails in Math** (20–28% churn), so under prereg §7.6 the behavioural TOST is uninterpretable there and H₀ cannot be read in Math. Two additions from this pass:
   - the 5% limit is below the 6–8% replay floor, so the gate is unpassable in Math as specified (§8.5);
   - the failure says nothing in favour of Δℓ. It only removes the behavioural test.
6. **ρ > 1: [Verified] arithmetically valid.** ρ is a ratio of two separately estimated mean contrasts and nothing bounds it at 1.
   - What it says: at the `####` position, swapping the verdict moved the answer-token margin more than swapping the explicit instruction target did.
   - What it does not say: that verdicts outweigh instructions in behaviour, that ρ is a proportion, or that the numerator reflects attraction to the reversed verdict (§8.3).
   - It is sensitive to the denominator: the ceiling varies twofold across templates (ρ_3B from 1.13 to 2.59), and in 3B it is a tenth of the order effect.
7. **Explicit ceilings: [Verified] only partly functioning.**
   - 7B Math and ChartQA: both directions are positive in the mean Δℓ.
   - 3B Math: the image direction is zero in Δℓ, although behaviourally `explicit_image` works (68 image answers against 28–30 at baseline).
   - Math, both models: the Δℓ sign follows order over instruction (§8.2).
   - ChartQA: behaviourally `explicit_text` rarely produces the report answer (3B 1/12, 7B 2/4).
   - *Decision:* whether a ceiling that order dominates is an adequate scale for ρ. Changing ρ's definition touches R4/R6, which the prereg says dev numbers may not change; that conflict needs an explicit, logged ruling.

### 10.2 Construct validity of the primary outcome in Math (new)

- [Verified] Δℓ is scored at `####` directly after the verdict, before any working (`transplant_v5.py:258-259`). For Math the model has not yet solved either problem at that point.
- [Verified] There, Δℓ's sign agrees with the eventual answer at 52–57%, and its shift does not separate cells where behaviour switched (§8.6).
- [Inferred] In Math, Δℓ may be measuring a pre-reasoning number prior shaped by position, rather than the model's choice of problem. The prereg cites 75.3–82.0% sign agreement for a related margin in other work (`PREREGISTRATION…:290`; not verified by this audit); the dev agreement here is far lower.
- *Decision:* whether Δℓ at this position remains the sole primary outcome for the Math regime, and whether a validity gate on Δℓ–behaviour agreement belongs in §8. This is the most consequential open item this audit found.

### 10.3 Remaining threats

- **Provenance:** unrecorded sessions; unpinned installs; `resolved_model_commit` null; manifests describe the last invocation only.
- **Reproducibility:** generations are not bit-stable (§8.5). Competency sets, donors and all behavioural outcomes inherit this.
- **Label validity:** `stated_reliable_source` is unvalidated and has one demonstrated mislabel. Competency, gates, orientation and the manipulation check all depend on parsers.
- **Selection:** the both-orders rule and gate 3b favour terse verdicts; 3B and 7B retain different items (intersection 50).
- **Estimand:** the flip contrast mixes anchoring by the own verdict with attraction by the reversed one (§8.3). In ChartQA every flip is in one direction.
- **Statistics:** p-values at their floors; uninformative CIs at n = 2 and 6; Holm applied in groups that R5 would not admit; right-skewed item CDEs (7B mean 1.62, median 1.09).
- **Code/design gaps:** 60% gate unimplemented; `reading_binding` ignores `meets_min_items`; no minimum n in the size comparison; boundary-mismatch limit reported, not enforced.
- **Freeze record (R8.3) still missing:** a stored analysis output, the ChartQA render gate, the `max_pixels` decision, human coding, and a recorded three-way competency intersection (Math 0, ChartQA 8).

---

## 11. Verified facts, inferences, hypotheses, and unknowns

**[Verified]**
- Row grids complete; no duplicates, parse errors, non-finite or positive likelihoods, or boundary mismatches; `ws_skipped = 2` throughout.
- Gates regenerate; Math prompts and all transplant prefills match current code; batch sizes in the rows match the manifests; 196 tests pass.
- ChartQA dev gold answers match Hub rows 0–29; the Hub split has 230 rows at the pinned revision.
- Every number in the tables of §§3, 7 and 8.
- 2B emits no `####` in Math. The ChartQA render gate and any analysis run are absent from the record.
- Manifests are rewritten per invocation; most blocks wrote 0 rows in the recorded session.
- The §8 60% gate fails for all ChartQA models and is not implemented.
- In Math, the Δℓ sign follows evidence order over explicit instruction, and agrees with behaviour at 52–57%.
- For 7B Math, flip − none is 0.10 with a CI spanning 0, while none − own is 1.52.
- Replaying the own verdict changes the answer source in 6.4% (3B) and 8.2% (7B) of exact-prefix cells.

**[Inferred]**
- 2B/3B `peak_vram_gb` values are load-only.
- The unrecorded rows came from the same code and GPU class (hash, batch-size and speed evidence), though not provably the same library versions.
- ChartQA cannot reach 100 items per model at dev rates.
- About 43 2B Math items would pass a lenient rule.
- The 5% churn limit is unattainable in Math as specified.
- In Math, Δℓ at `####` reflects a position-shaped prior more than problem choice.

**[Hypothesis]**
- Run-to-run divergence comes from batch padding in bf16 or from library differences between sessions.
- Minimal-edit flips are weaker than template verdicts because the retained justification clashes with the swapped noun.
- The both-orders and gate-3b rules bias retention toward terse verdicts.

**[Unknown]**
- Library versions and resolved model and dataset commits in the unrecorded sessions.
- Whether Δℓ scoring is bit-reproducible, and whether competency sets would survive a rerun.
- The L4's compute capability as recorded; whether any OOM split occurred.
- Agreement of `stated_reliable_source` with human coders.
- Accuracy of the preregistration's literature citations (not checked here).

---

## 12. Appendix: files inspected and read-only commands

**Data:** all 39 files in `Experiment/results_v5/`.

**Code:** `Experiment/harness_v5.py`, `transplant_v5.py`, `score_v5.py`, `analyze_v5.py`; `harness_v4.py` (pins `:45-54`; `split_phase` `:210-232`; dtype `:401-402`; backend info `:428-440`; `write_manifest` `:601-625`); `score_v4.py` (`split_verbalization` `:110-130`); `tests/`.

**Documents:**
- `Thesis/docs/Archive/v5_dev_output.md`, `v5_antigravity_analysis.md`, `v5_dev_evidence_audit.md`, and the first-pass `claude_v5_independent_deep_audit.md` (git `ad58428`);
- `Experiment/RUNBOOK_v5.md`; `Thesis/docs/RUNBOOK/RUNBOOK_V5.md`;
- `Docs/PREREGISTRATION_VERDICT_TRANSPLANT.md` (§4.3 `:182-191`; §5.3 `:262-274`; §6 `:278-299`; §7.6 `:390-406`; §8 `:412-423`; R5 `:100-113`, `:473-477`; R8 `:514-524`);
- `Experiment/results_v4/dev2_qwen25.manifest.json` (transformers version);
- `Experiment/results_v3/full_experiment_results v3.0.json` (question text for the prompt rebuild).

**External:** Hugging Face dataset viewer for `vlm-modality-research/chartqa-evidence-conflict-v2` (structure, and rows 0–30 of `default/test`).

**Commands** (scripts in the session scratchpad; none wrote to the project):

First pass (outputs retained and re-read):
1. `find` / `ls` / `wc` over `results_v5/` and the sources.
2. Print each `*.gates.json` and one full manifest; tabulate all manifests against SHA-256 of current sources.
3. `grep` / `sed` over `harness_v4.py`, both runbooks and the preregistration; `git status`, `git diff`, `git log`.
4. `inv.py`: row inventory, grid checks, competency with parse methods, donor verdict tables, gate regeneration with `transplant_v5.plan`.
5. `ana.py`: `analyze_v5.analyze_group` with and without base/donor rows, raw cross-check, cell means, behavioural tables, `analyze_size_comparison`.
6. Inline checks: 2B `####` / `\boxed` counts; gate-3b swap counts; lenient 2B competency; 3B ChartQA donor parsing; prompt and prefill rebuild for all 16 files.
7. `python -B -m unittest discover tests` (196 tests, OK).

Second pass:
8. `forensic.py`: totals by split, stage and outcome; item sets and gold equality across models; `candidate_text` effects; token-count asymmetry; batch size and speed from `wall_s`; donor verbalization structure; own-verdict replay; Δℓ-versus-behaviour sign agreement; Δℓ sign against explicit instruction; per-template and per-direction CDE and ceiling; capped rows against competency.
9. `indep.py`: separate bootstrap, ratio bootstrap and sign-flip test (seeds 2026 and 7); behavioural Δ and churn; decomposition through `none` and `para`; Δℓ shift against behavioural switching; exact-prefix replay analysis.
10. Inline: candidate prefix pairs; stored ChartQA gold answers for comparison with the Hub rows; prereg line lookups.
11. `git log` to confirm the first-pass report is preserved in `ad58428`.

**Final self-audit.**
- Each number in §§3–4 and §§7–9 comes from the commands above or from the cited file and line.
- Every result is labelled dev-only, and no group is described as meeting its minimum sample.
- No conclusion rests on AG, EA or C1 alone: their claims were items to check, and C1's own errors are listed in §9.3.
- Remedies appear only as pre-freeze decisions for the researcher.
- The only project file written is this report.
