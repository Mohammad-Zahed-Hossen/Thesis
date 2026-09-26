# Source parts for `AI_ML_Research_Playbook (Cline 2026-09-27).md`

These files are the chunked source of the assembled playbook. They were originally named
`part00.md` ... `part35.md`, which made it impossible to tell what any file contained; they are now
named `<document-order prefix>_<section range>_<topic>.md`.

**Ordering rule.** The published document is produced by concatenating the files below in ascending
filename order, joined with one blank line (`\n\n`). The zero-padded prefix (`00a` ... `35_`) exists
only to make that order automatic, so **never change a prefix when you rename or add a file** - extend
the prefix instead (e.g. add `18b_...` for a new sub-part of Section 18).

Run `python _rebuild_playbook.py` to verify the parts still rebuild the published document exactly, or
`python _rebuild_playbook.py --write` to regenerate it after an edit.

| # | File | Sections covered | Contents |
|---|---|---|---|
| 1 | `00a_front-matter__title-and-evidence-labels.md` | `front-matter` | Document title block, audience line, and the [L1]/[L2]/[L3] evidence-label legend. |
| 2 | `00b_table-of-contents.md` | `table-of-contents` | Table of contents for Sections 0-32 plus Appendices A-C. |
| 3 | `00c_s0-scope-and-epistemic-limits__s1-executive-overview.md` | `s0-scope-and-epistemic-limits` | Section 0 (scope, three epistemic limits, unverified-citation warning) and Section 1 (executive overview, discovery loop, five questions). |
| 4 | `02_s2-how-experienced-researchers-work.md` | `s2-how-experienced-researchers-work` | Section 2: decision-as-unit-of-work, predictions over topics, three ledgers, what 'senior' means operationally. |
| 5 | `03_s3-why-research-is-not-linear__s4.1-s4.3-researchers-mental-model.md` | `s3-why-research-is-not-linear` | Section 3 (false model vs real loop, backtrack triggers, two kinds of stability) and Sections 4.1-4.3 (conditional claims, explanation levels, discrimination principle). |
| 6 | `04_s4.4-s4.6-assumption-audit-and-claim-boundary.md` | `s4.4-s4.6-assumption-audit-and-claim-boundary` | Sections 4.4-4.6: eight-item assumption audit, one-sentence boundary statement, pre-registration of what would change your mind. |
| 7 | `05_s5-finding-research-territories__s6-opening-table.md` | `s5-finding-research-territories` | Section 5 (area vs territory, five signals, scoring grid, three archetypes, rejecting a territory) and the Section 6 source-of-questions table. |
| 8 | `06_s6.1-s6.4-phenomena-and-failures__s7.1-s7.4-question-tests.md` | `s6.1-s6.4-phenomena-and-failures` | Sections 6.1-6.4 (missing control, proxy metric, paper contradictions, low-yield sources) and Sections 7.1-7.4 (the ladder, gap vs question, four tests, anti-patterns). |
| 9 | `07_s7.5-s7.7-worked-ladders-and-terminology-trap.md` | `s7.5-s7.7-worked-ladders-and-terminology-trap` | Sections 7.5-7.7: worked ladder A (frozen question), worked ladder B (abstention branch), and the terminology/novelty trap. |
| 10 | `08_s8-literature-exploration-strategy.md` | `s8-literature-exploration-strategy` | Section 8: reading as resource allocation, when to read deeply, saturation criteria, breadth-first then depth-first, reading queue, search tools. |
| 11 | `09_s9-how-to-search-like-a-researcher.md` | `s9-how-to-search-like-a-researcher` | Section 9: the 10-step search sequence, searching by design dimension, citation-chain techniques, search hygiene. |
| 12 | `10_s10-how-to-read-and-interrogate-papers.md` | `s10-how-to-read-and-interrogate-papers` | Section 10: three reading passes, where to look for what, six limit-revealing questions, safe vs unsafe AI use, when to stop reading. |
| 13 | `11_s11-building-a-field-map.md` | `s11-building-a-field-map` | Section 11: purpose and size, the ten slots, compact format, evolution by day, two-day build plan, frontier date. |
| 14 | `12a_s12.1-s12.3-closest-work-definition-and-search-order.md` | `s12.1-s12.3-closest-work-definition-and-search-order` | Sections 12.1-12.3: definition of closest work, design-vector decomposition and overlap table, where to look in order. |
| 15 | `12b_s12.4-s12.6-closest-work-design-difference-and-worked-table.md` | `s12.4-s12.6-closest-work-design-difference-and-worked-table` | Sections 12.4-12.6: two-sentence design-difference statement, worked closest-work table (four verified anchors), practical tricks. |
| 16 | `13_s13-verifying-whether-a-gap-is-real.md` | `s13-verifying-whether-a-gap-is-real` | Section 13: ten gap questions, three verdicts (REAL/UNCLEAR/OCCUPIED), gap classes and their worth, verification worksheet, self-deception test. |
| 17 | `14_s14-competing-explanations-and-hypotheses.md` | `s14-competing-explanations-and-hypotheses` | Section 14: alternative-explanation taxonomy, hypothesis signatures, control matrix, worked instance of the four arms, hypothesis hygiene. |
| 18 | `15_s15-adversarial-idea-testing.md` | `s15-adversarial-idea-testing` | Section 15: attack list, strongest-objection discipline, three red-team personas, worked adversarial audit of the frozen design. |
| 19 | `16_s16-fast-idea-killing.md` | `s16-fast-idea-killing` | Section 16: one-hour kill checklist, pre-mortem, reconstructed parks/kills, the two-day kill window, kill-note template. |
| 20 | `17_s17-feasibility-during-discovery.md` | `s17-feasibility-during-discovery` | Section 17: feasibility as instrument, two opposite mistakes, honest compute line, feasibility scoring, interpretability check. |
| 21 | `18_s18-minimum-discriminating-experiment.md` | `s18-minimum-discriminating-experiment` | Section 18: MDE definition and reduction procedure, five worked reductions, pilot sizing, one-comparison rule, one-GPU-hour exercise, acceptance checklist. |
| 22 | `19_s19-from-question-to-experimental-system.md` | `s19-from-question-to-experimental-system` | Section 19: transition chain with reasons, operationalization table, unit of analysis, freeze-vs-flexible table, analysis plan, harness improvements. |
| 23 | `20_s20-baselines-controls-metrics-evaluation.md` | `s20-baselines-controls-metrics-evaluation` | Section 20: three baseline kinds, four control kinds, construct validity of metrics, LLM-judge rules, statistical reporting checklist, domain-specific evaluation trap. |
| 24 | `21_s21-pilot-to-main-experiment.md` | `s21-pilot-to-main-experiment` | Section 21: what a pilot is for, numeric pilot gates, main-run practice, what the pilot changed, pilot-to-main decision rule, ablations and robustness. |
| 25 | `22_s22.1-s22.6-negative-and-unexpected-results.md` | `s22.1-s22.6-negative-and-unexpected-results` | Sections 22.1-22.6: negative result vs failure vs uninterpretable, controls that make nulls interpretable, failed hypothesis as contribution, decision tree, re-scoping. |
| 26 | `23_s22.7-s22.8-writing-negative-results__s23-iterating-and-changing-the-question.md` | `s22.7-s22.8-writing-negative-results` | Sections 22.7-22.8 (how to write a negative result, emotional discipline) and Section 23 (iteration table, five legitimate responses, worked Q0-Q4 iteration, change-control rule). |
| 27 | `24_s24-freezing-the-research-question.md` | `s24-freezing-the-research-question` | Section 24: what a freeze means, the eleven-item freeze checklist, what is not frozen, re-open conditions, three freeze artifacts, the workspace lesson. |
| 28 | `25_s25-end-to-end-thesis-execution.md` | `s25-end-to-end-thesis-execution` | Section 25: pipeline purposes, upfront vs flexible decisions, directory layout, reproducibility minimum, figure discipline, documentation, writing order. |
| 29 | `26_s26-from-thesis-to-paper.md` | `s26-from-thesis-to-paper` | Section 26: central claim, what to keep and cut, evidence-first structure, honest framing, limitations, overclaiming phrase audit, venue choice, revision as evidence. |
| 30 | `27_s27-research-timeline.md` | `s27-research-timeline` | Section 27: Phases 0-10 with objective, do/do-not guidance, forward and backward conditions, outputs, and schedule reality. |
| 31 | `28a_s28.1-s28.4-failure-modes-why-discovery-was-slow.md` | `s28.1-s28.4-failure-modes-why-discovery-was-slow` | Sections 28.1-28.4: five causes of slow discovery, looping behaviors, activities that produced real evidence, activities that created the illusion of progress. |
| 32 | `28b_s28.5-s28.11-failure-modes-stopping-points-and-ai-uses.md` | `s28.5-s28.11-failure-modes-stopping-points-and-ai-uses` | Sections 28.5-28.11: missed stopping points, what should have been done earlier, what to stop doing, what must remain human, where AI accelerates or creates false confidence. |
| 33 | `29_s29-reusable-research-workspace.md` | `s29-reusable-research-workspace` | Section 29: the seven artifacts (research map, question ledger, evidence ledger, experiment specification, research log, results record, paper story) and the minimal file layout. |
| 34 | `30_s30.1-s30.5-stop-continue-pivot-kill.md` | `s30.1-s30.5-stop-continue-pivot-kill` | Sections 30.1-30.5: six decisions with required evidence, trigger questions, numeric thresholds, review cadence, application to the live project. |
| 35 | `31_s30.6-eight-factor-intersection__s31-one-page-daily-playbook.md` | `s30.6-eight-factor-intersection` | Section 30.6 (eight-factor intersection rule and two failure shapes) and Section 31 (discovery loop with questions, daily blocks, daily self-check, weekly review, printable loop card). |
| 36 | `32_s32-if-i-start-a-new-research-area-tomorrow.md` | `s32-if-i-start-a-new-research-area-tomorrow` | Section 32: day-by-day eleven-day walkthrough, three-week compression, and the three sentences to remember. |
| 37 | `33_appendix-A_primary-sources-verified.md` | `appendix-A_primary-sources-verified` | Appendix A: the nine primary sources with the sections they support, the unverified arXiv:2608.17205 note, and the evidence standard applied. |
| 38 | `34_appendix-B_case-study-chronology.md` | `appendix-B_case-study-chronology` | Appendix B: corpus contents, reconstructed chronology, verified numbers table, six extracted case studies, limits of the reconstruction. |
| 39 | `35_appendix-C_printable-cards.md` | `appendix-C_printable-cards` | Appendix C: five questions, kill checklist, freeze checklist, metric-validity card, closest-work card, decision card, three sentences. |

## Excluded from the rebuild

- `_superseded/part01-SUPERSEDED-duplicate-of-00a-and-00c.md` - the old `part01.md`: an exact
  concatenation (verified, 4,370 chars) of `00a` + blank line + `00c`. It was never part of the published
  document (substring count: 0 hits), so it was kept for provenance but moved out of the concatenation path.
- `_MANIFEST.md` and `_rebuild_playbook.py` - tooling, not content (any name starting with `_` is skipped).

## Status

- 39 content parts, 172,712 characters, joined to 172,788 characters = the published deliverable.
- Verified on 2026-09-27: every part occurs exactly once, in order, in the deliverable.

**The filename is the source of truth.** If a part is renamed, split, or added, update this table to
match and keep the ordering prefixes ascending, then re-verify with `python _rebuild_playbook.py`.
