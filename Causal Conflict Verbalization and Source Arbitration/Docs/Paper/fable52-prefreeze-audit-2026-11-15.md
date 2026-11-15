# Pre-freeze forensic audit — commit `03274b3`

> **Archived:** 2026-11-15 (Fable 5.2 forensic audit of commit `03274b3`).  
> **Companion files:** Helper forensic scripts in [fable52_audit_scripts/](fable52_audit_scripts/) (`chart.py`, `floor.py`, `parser.py`, `prefix.py`, `regate.py`) and source-only pinned snapshots of the inspected related-work GitHub repositories in [related_repos/](related_repos/README.md).

This is an in-project reading by one AI session, not an outside review. Nothing in the repo was edited, no `KEY_*` file was opened, and no model was loaded. Unit tests: `Ran 240 tests in 26.568s OK`.

## 1. Executive verdict

**Not freeze-ready.** The design is sound and the statistics match the prereg, but four things block `prereg-v5`:

- **The code you would freeze has never run on a GPU.** All five script hashes in the dev manifests differ from the working tree, and the current gates select different items from the stored dev rows.
- **Manifests cannot record the prereg tag.** The prereg requires the tag hash in every confirmatory manifest; no git field exists, and `resolved_model_commit` is `null` in all 16 manifests.
- **Human coding has not started**, and its evaluator would understate parser accuracy.
- **ChartQA `max_pixels` (R8.4) is open**, with concrete evidence now pointing to a specific value.

P1 items are confirm-phase guards, a resume bug, two edit-gate edge cases, and the two descriptive analyses from the literature audit.

## 2. Findings

| ID | Sev | Area | Evidence | Risk | Fix |
|---|---|---|---|---|---|
| F1 | P0 | Code vs dev pass | [Verified] All 5 `scripts_sha256` entries in `v5dev_conflict_tp_qwen25_7b.manifest.json` differ from the tree. Current gates on stored rows: Math 3B 93 pass (stored 80), 7B 140 (stored 115); ChartQA 3B 5/13, 7B 0/13 (stored 6, 2) | R8.2–R8.3 are met only by older code; the `verdict_nll` span path (`harness_v5.py:541-555`) has never touched the real tokenizer | GPU smoke under new tags (§5); regenerate `gates.json` |
| F2 | P0 | Provenance | [Verified] No `git` or tag field in `harness_v4.write_manifest` (`:629-636`); `resolved_model_commit: null` in all 16 manifests; three 3B stage manifests have `written_at` within 40 s (overwritten on rerun) | Prereg line 12 cannot be satisfied; first-invocation GPU and time are lost | Append-only `invocations` list with `git_commit`, `prereg_tag`, GPU, slice; refuse `--phase confirm` if `prereg-v5` does not resolve to HEAD |
| F3 | P0 | Human coding | [Verified] 0 of 200 and 0 of 150 coder cells filled. `sample_v5_for_coding.py:263-264` compares parser labels (`undetermined`, `absent`) with human labels (`neither`, `both`, `unclear`) as raw strings. Only 32 of 200 verdict rows are 3B/7B × Math × donor; 72 are the diagnostic 2B | Every correct abstention counts as a parser error; the confirmatory stratum gets n = 32 | Map both sides to {source, source, no-usable-verdict} and report the confusion matrix; resample with most rows from confirmatory cells before coders begin |
| F4 | P0 | R8.4 | [Verified] Charts in the source artifact are 800×557 px, so 200704 scales them to 67% linear and 401408 to 95%. The artifact loads the Qwen processor with no pixel arguments (`src/models.py:164-166`). Base-image misses are neighbouring-value reads shared by all three models (67.6→15.7, 320.66→323.6) | Low chart competency is plausibly a resolution artefact [Inferred] | Compare 200704 vs 501760 (§5) and fix the value |
| F5 | P0 | Prereg ≠ code | [Verified] `_SWAP` (`transplant_v5.py:110-121`) includes `visual` and `written`; prereg §5.2 lists neither | The frozen lexicon is not the one that runs | Remove both from code (see F8), or add them to §5.2 |
| F6 | P1 | Resume | [Verified by test] After a crash-truncated last line, the rerun glues one row onto the fragment; `competent_ids` then raises `JSONDecodeError` (`harness_v5.py:694`) | Transplant cannot start until the file is hand-repaired | Write `\n` before appending if the file lacks one; tolerant loaders that count skipped lines |
| F7 | P1 | Confirm guards | [Verified] `config_from_args` (`harness_v5.py:740-743`) accepts any `--model_revision`, `--limit`, `--max_pixels`, `--beh_k`, `--competency_parser` in confirm. `analyze_v5.py:1656` groups by model and regime only | An off-pin or truncated confirm run, or dev and confirm rows pooled, goes unnoticed | In confirm, refuse non-pinned revisions and non-default values; refuse mixed phases in analysis |
| F8 | P1 | Edit gates | [Verified by test] "the written text" flips to "the image image" and passes every gate. "The typed text, unlike the image, is more reliable" is labelled `image`, which inverts that item's orientation. Dev incidence of the first is 0 of 466 cells; the second was not measured | Garbled or mis-oriented interventions | Doubled-noun check in `_BAD_GRAMMAR`; reject verdict clauses with two different source nouns before "reliable" |
| F9 | P1 | Wording floor | [Verified] 3B non-binding: 6 flips in 79 pairs, all `hash_direct`, no cap hits; 7B: 12 in 182, 11 involving the `structured` parser. `para` prefills are much shorter than `own` (219→99, 458→357 chars) | `para` deletes the justification, so the floor measures content removal, not rewording [Inferred]. Wilson intervals (3.5–15.6%, 3.8–11.2%) both contain the 5% limit | State both in §7.6; the gate itself is implemented as written |
| F10 | P1 | Lit-audit rows O, M | [Verified] Per-order CDE exists for Δℓ only (`analyze_v5.py:1188-1191`). `verdict_nll` is reported as a mean per verdict only (`:1230-1235`) | The Math primary outcome has no per-order table | Add an `order` argument to `beh_diff`; add tertiles of `verdict_nll(flip) − verdict_nll(own)`. No new GPU columns needed, but dev values use the old whole-prefill span |
| F11 | P1 | Environment | [Verified] `RUNBOOK_v5.md:25` installs unpinned; line 28 says 5.22.2; manifests record 5.22.1. `min_pixels = 100352` is not in the prereg | Confirm may run on a different library version | Pin versions in the runbook; state `min_pixels` in §3.4 |
| F12 | P1 | 2B model | [Verified] 0 of 200 Math items are competent under `structured` (43 under `lenient`) | The runbook's 2B confirm run exits with the R5 stop | Drop 2B from Math confirm, or state its diagnostic parser |
| F13 | P2 | Analysis | [Verified] The size comparison uses Δℓ ρ (`:1245`), stale after D1. The R script does not detect non-convergence warnings, which §7.4 requires. `ws_skipped` sums both candidates. `read_csv_map` fails on a BOM | Small spec drift | Listed in §7 |

## 3. Code-vs-prereg and test coverage

| Module | Matches prereg | Gaps | Untested high-risk paths |
|---|---|---|---|
| `harness_v5.py` | §4.1 layout, §4.2/4.4 templates, no source letters, 230/229 check, `bfloat16` stop | F2, F7; GPU class not compared across stages | All of `HFBackend` (stated at `tests/test_v5.py:7`); truncated-line resume |
| `transplant_v5.py` | Gates 1–6, Jaccard 0.85, two-swap cap, seeded take | F5, F8 | Real-tokenizer span offsets |
| `score_v5.py` | Parsers; `structured` matched no intermediate statement in 1,392 dev uses | "unlike" construction | — |
| `analyze_v5.py` | Δ formulas, co-primary rule, TOST at 5 pp, Holm doubling, floor gate, inconclusive rule | F7, F10, F13 | Mixed-phase input; label mapping in the coding evaluator |

## 4. Our v5 against related codebases

| Paper | Repo and commit | Mechanism read | What v5 closes or should adopt |
|---|---|---|---|
| 2608.17205 | `Ro-netizen004/multimodal-arbitration-artifact` @ `fe73af7` | `src/models.py:756-796`, `scripts/run_chartqa_conflict.py:373-394` | Closes: they use Source A/B labels, image always first, and no prefix-boundary check. Agrees: same 2B and 7B pins, `bfloat16`, same scored tokens for Qwen. Adopt: their pixel setting (F4); their parser normalises Unicode minus and units, ours does not |
| 2610.33841 | `Maximeswd/Grounding-on-Request` @ `1ffed8c` | `scripts/tokscore.py`, `scripts/stats_pass.py` | Adopt: they score the end-of-turn token because it does not cancel between candidates. Ours omits it, and 8 of 200 Math pairs have one answer as a prefix of the other. Their statistics are Wilson, McNemar and bootstrap, with no equivalence test |
| 2510.27484 | `interp-reasoning/thought-branches` @ `9e2bba4` | `faithfulness/A_run_cued_uncued_problems.py:56` | They transplant through raw completion strings with sampling; ours is chat-template prefill with greedy decoding and a prefill-survival assertion |
| 2609.25366 | `r2m-ai/load-bearing-cot` @ `bf74d68` | `experiments/pipeline/perturb_and_continue.py:362-376` | Same strip-end-of-turn idiom, without our assertion. Adopt: their κ code returns undefined when both raters are constant and reports raw agreement beside κ |
| 2609.06704 | `neuralisa/cct-vlm` @ `dd40740` | `model.py:526-542` | Prompt-elicited CoT only; has a paired no-op control. No prefill to compare |
| 2606.12747 | Anonymous 4open links in the PDF | Not opened | [Unknown] |
| 2607.27304, 2610.30953, 2610.20805, 2609.00550, 2609.26986, 2609.29278, 2307.13702 | No repository link in the local PDF | — | [Unknown / no verified public repo] |

`CCS-CoTFE/CCS-CoTFE` @ `a454bd7` and `milesaturpin/cot-unfaithfulness` @ `df09945` exist; I did not read their code.

## 5. Execution plan before the tag

1. **Local:** apply F2, F5, F6, F7, F8 with tests; fix the F3 evaluator and resample the coding sheets.
2. **Local:** humans code the new sheets; run `evaluate`.
3. **GPU:** six `--print_example` render checks (the ChartQA three were never run).
4. **GPU:** one `transplant_v5.py --phase dev --limit 20` per confirmatory model under a new tag; check `verdict_nll_tokens > 0`, `verdict_span_exact`, and boundary mismatches ≤ 1%.
5. **GPU:** ChartQA base and donor at `--max_pixels 501760` for 3B and 7B (30 items each), then `--gates_only`. 501760 is my choice: 800×557 should round to 812×560 = 454,720 px [Inferred, not run].
6. **Local:** rerun `analyze_v5.py`, apply the prereg patches, commit, tag.

I have not estimated GPU minutes; `seconds_per_item` in `analysis_v5.json` gives the basis.

## 6. Upgrades worth building

1. **`preflight_v5.py`**: one command that checks pins, template hashes, dtype, tag-at-HEAD and library versions, and fails on a planted wrong pin. It turns F2, F7 and F11 into one gate.
2. **Append-only manifest provenance** (F2): `invocations[]`, with a test that a second run adds an entry.
3. **Descriptive suite** in `analyze_v5.py`: per-order behavioural Δ, `verdict_nll` tertiles, and three-parser tables as CSV.
4. **Consistency tests**: assert the §4.2/§4.4 templates and §5.2 lexicon in the prereg equal the code constants. This would have caught F5.
5. **End-of-turn margin** as a logged diagnostic beside Δℓ, for the exploratory ChartQA reading.

## 7. Patch plan for the prereg and docs

- **Sources:** "20 local PDFs" → "26 (20 core/lead + 6 audit)"; add `lit-audit-2026-11-15`.
- **§1.1:** replace with the lit-audit §1.3 text, keeping the Dassen, Barua, Menzat, CMC-Bench and Fan sentences.
- **§2.2 row 5 and §2.3 row 5:** add "a null may reflect resistance to an off-preference prefill rather than verdict irrelevance (arXiv:2606.12747)".
- **§3.1:** add "the image is a rendered image of problem text; claims concern rendered-text vs typed-text".
- **§3.3:** add "the estimand is conditional on dual competence; pass rate is reported per model; the filter uses separate arms and is pre-treatment".
- **§3.4:** state `min_pixels = 100352`, the library versions, and the R8.4 outcome.
- **§5.2:** make the lexicon match the code (F5).
- **§5.3:** add the two F8 checks; renumber so the code's "Gate 5" comment matches.
- **§6.3:** add the `verdict_nll` tertile analysis as descriptive [Design decision].
- **§7.2:** define the Math size comparison on Δ_bind, not ρ.
- **§7.3:** add the general ML TOST precedent (arXiv:2610.23700).
- **§7.5 Order:** add "if per-order CDEs differ in sign, the averaged CDE carries that caveat and both are read side by side".
- **§7.6:** add the F9 sentences.
- **§8:** state the κ threshold and its consequence, which currently exist only in the coder instructions.
- **§11:** log all of the above.
- **Other docs:** `RUNBOOK_v5.md` lines 25, 28 and 167 (version pins, 2B). `THESIS_NARRATIVE_AND_FRAMING_GUIDE.md` already has the rendered-text note at line 73, so it needs no change.
