# Prompt: evidence-based v4 → v5 design review (for OpenResearch)

*Written 2026-11-14. Copy everything below the line into OpenResearch. It is read-only work: the output is one report.*

---

## Role and goal

You are an independent research reviewer for an undergraduate BSc CSE thesis. The workspace is the folder `Causal Conflict Verbalization and Source Arbitration/`, which you can read directly. The thesis tests whether a reliability verdict, prefix-forced into a vision-language model's own response under image–text conflict, causally changes which source's answer the model gives.

The project went through two earlier redesigns: v3 pilot → v4 dev, then v4 dev → v5 dev. After the v5 dev pass, five pre-freeze decisions (D1–D5) were made, and on 2026-11-14 three gates were tightened. The researcher now wants to **choose the v5 confirmatory design deliberately**, the way v3 → v4 was improved. That means: for each design point, compare the current choice with its realistic alternatives, using the project's own data and the primary papers, then recommend.

**Do not edit, run or freeze anything.**
- No changes to code, data, the pre-registration, `CLAUDE.md` or any existing markdown.
- Do not load any model (local machine: no CUDA, 8 GB RAM).
- Do not create the git tag `prereg-v5`.
- Write one report only: `Thesis/docs/Archive/openresearch_v5_design_decision_review.md`.
- You may run read-only Python on the result files with `python -B`, standard library only, for example to recompute a number from the JSONL rows.

## Trust hierarchy (read `CLAUDE.md` first)

1. **Ground truth.** Rows and manifests in `Experiment/results_v5/`, `Experiment/results_v4/` and `Experiment/results_v3/`; code in `Experiment/*.py`; PDFs in `Docs/Paper/`.
2. **Design specification.** `Docs/PREREGISTRATION_VERDICT_TRANSPLANT.md`: a draft, uncommitted, and checked against code before you rely on it.
3. **Leads only.** Everything else in `Docs/` and `Thesis/docs/` is AI-generated, including earlier audits, both FAQs and the pasted analyses described below. Every number you take from them must be re-derived from rows or code, or marked unverified.

Tag every claim [Verified] (you checked it in rows, code or a paper page), [Inferred], [Hypothesis] or [Unknown]. Cite papers by arXiv ID and page. Never invent a paper, number or citation. If a paper cannot be opened, say so. Follow the project's claim boundaries:
- the estimand is a **controlled direct effect**, never "mediation";
- dev numbers are for tuning, never findings;
- no "first" or "novel" claims beyond dossier §4.1.

## Materials to read

**Project history** (to reconstruct how v3 → v4 was improvised and what lessons carried over):
- `Experiment/README.md`, `Experiment/results_v3/README.md`, `Experiment/results_v4/README.md`, `Experiment/results_v5/README.md`
- `Docs/Decision_Audits/Idea.md`, `Docs/Paper/prereg-freeze-audit/`, `Docs/Paper/lit-dossier-verdict-transplant/lit-dossier-verdict-transplant.md`
- Audits in `Thesis/docs/Archive/` (leads only), especially:
  - `claude_v5_independent_deep_audit.md`
  - `claude_v5_forensic_code_and_construct_audit.md`
  - `claude_v4_vs_v5_plan_audit.md`

**Current design and code:**
- The prereg, §1–§3, §6, §7 and §11. §11 logs every change with its date.
- `Experiment/harness_v5.py` (prompts such as `MATH_STEMS` and `CHART_STEMS`, `max_pixels`, scoring)
- `Experiment/transplant_v5.py` (edit gates, answer-leakage gate, how the `none` prefill is built)
- `Experiment/score_v5.py` (parsers, verdict parsing)
- `Experiment/analyze_v5.py` (decision rules: `decision_test`, `math_reading`, `wording_floor`, `behaviour_benchmark`)

**Dev data:**
- `Experiment/results_v5/*.jsonl` and their manifests and gates files
- `Experiment/results_v5/analysis_dev/analysis_v5.md` and `.json`, regenerated 2026-11-14 with the tightened gates

**Primary papers.** Read the relevant sections; local PDFs are in `Docs/Paper/`, otherwise use AlphaXiv:

| Paper | Why it matters here |
|---|---|
| Ghosh, Gupta & Wang, *Which Source Wins?*, 2608.17205 | Stimuli; margin scored after `####` with no CoT ("direct-answer preference"); per-model margin–behaviour agreement (Table 5); arithmetic parser with last-number fallback |
| Bhowal et al., *CoT-Mediate*, 2607.27304 | Prefix-forced edits of the model's own reasoning; paraphrase floor as any-change flip rate (1.7–3.3%); C1 reference; injection-arm gap |
| Dassen et al., *Grounding on Request*, 2610.33841 | Natural-language modality requests weaker for image than text; FLIP/STAY; model-dependent default preference |
| Barua et al., 2610.19407 | Text-evidence reliance; margin vs. behaviour |
| *Noncommutativity / order effect*, 2609.26986 | Evidence-order effect (+16.7 / +15.0 pp, Qwen2.5-VL-3B) |
| Macar, Bogdan et al., *Thought Branches*, 2510.27484 | A single sampled CoT is inadequate; resampling; off-policy vs. on-policy edits |
| Cox et al., *Post-hoc reasoning*, 2603.01437 | Pre-CoT answer decodability vs. CoT usefulness (Qwen2.5 3B/7B) |
| Lanham et al., 2307.13702 | Early answering, adding mistakes, paraphrasing; size and faithfulness |
| Jia & Mu, 2609.25366 | Load-bearingness tracks model-relative difficulty |
| Catapang 2026, *CMC-Bench* (MAGMaR) | A candidate alternative evidence-conflict benchmark |
| Others in `Docs/Paper/`: 2503.02199, 2504.08974, 2505.23945, 2511.02243, 2602.14518, 2604.14888, 2606.28273, 2609.06704, 2610.38296 | Check each one's relevance before citing it |

Before doing any research, read the two paper sections the project's `CLAUDE.md` requires before a novelty claim for the binding arm: 2610.33841 in full, and 2610.19407.

## Known stale or wrong claims in the leads (verify, do not repeat)

The researcher pasted an analysis that proposes better alternatives for D1–D5. It was written against commit `f802951`, before the 2026-11-14 working-tree changes. Check each of the following against the current files and correct it in your report:

1. **"D1 is half-wired: Math H₁/H₀ still driven by Δℓ; `Ceil_beh` missing."** Now false in the working tree. Math readings come from `analyze_behaviour_primary` via `primary_reading_*`. `Ceil_beh` exists and was later renamed to the benchmark `B_beh`, because the dev effect exceeded it. Confirm this in the code.
2. **"D5 replay cap moves the goalposts."** Correct, and it has been removed. The limit is fixed at 5%, with a ±10 pp neither-shift guard. Under the fixed gate, 3B and 7B non-binding now fail on dev. Confirm in `analysis_dev/analysis_v5.md`.
3. **"ChartQA: 6/20 and 2/20 items passed."** Check the gates files: dev has 30 ChartQA items. Report both competent counts and gate-pass counts.
4. **"Δℓ agreed 50.6% (3B) / 57.4% (7B)."** These are the lenient-parser figures; the strict figures are 51.6% / 56.6%. Report all three parsers next to the majority-class baseline.
5. **"ChartQA is the cleanest Δℓ signal (99.1% agreement)."** Test this. The 16-token decode starts at `####`, the same point where Δℓ is read, and the majority baseline may also be about 99%. If agreement equals the baseline, it is not evidence of validity.
6. **"In `none` rows the model regenerates a verdict in 69.4% (3B) and 88.5% (7B)."** Recompute this from the rows per model and instruction. An earlier audit gave a range of 58–99.6%.
7. **DiD values (3B: +11.3 pp, matched pair +23.1 pp; 7B: +12.2 pp, +40.9 pp).** These match the current `analysis_v5.md`. Confirm them, and state the denominators.

## Questions to answer

### A. What did v3 → v4 → v5 each fix, and what lesson carries forward?

Reconstruct each transition: what failed, what changed, and what evidence drove the change. Then state the methodological lessons that should govern this round. Example: "v4's `m0`/`m1` contrasts swapped whole verbalizations and never isolated the verdict." Each lesson must have a source.

### B. For each design point, evaluate the current choice against its alternatives

For every alternative below, give:
1. what it fixes;
2. evidence from the project's rows (recompute where possible);
3. evidence from papers (page cited);
4. cost: GPU hours, estimated from the timing fields in `Experiment/results_v5/*.manifest.json` and the gates files, and dev items spent;
5. risk to validity, including new post-hoc choices it introduces;
6. effect on what the thesis can claim;
7. a recommendation: **adopt now / adopt as exploratory / reject / needs a pilot**, with the deciding reason.

**D1: the Math outcome.**
- (a) Current: behaviour at k = 1, structured parser, greedy decode.
- (b) Post-CoT Δℓ: score the two candidate answers at the final `####` after the model's own generated solution. Estimate how close this comes to restating the generated answer; is it then a different measure at all?
- (c) Resampling: n = 4–8 continuations at T = 0.7 per cell, P(text answer) per item (*Thought Branches*). Estimate how much the variance of the per-item difference would fall, and the change in TOST power. The tool `analyze_v5.tost_power` exists.
- (d) A second template (k = 2) for behaviour.
- (e) A short-answer probe instead of full solving.

**D2: contrasts and the `none` arm.**
- (a) Current: `flip − own` and `para_flip − para` co-primary; decomposition through `none` descriptive.
- (b) Relabel `none` as "unforced / re-generated verdict" baseline.
- (c) Suppress the regenerated verdict by prefilling the start of solving (for example "Step 1:") in `none`. Check whether this breaks comparability with `own`/`flip`, which prefill the full verbalization.
- (d) Measure the `flip` justification confound directly: the flipped noun with the original justification left in. How often does the donor's justification argue for the other source? Count it from the donor rows.

**D3: models and parser.**
- (a) Current: Qwen2.5-VL-3B and 7B confirmatory, 2B diagnostic, structured parser.
- (b) A cross-family model that fits a 24 GB L4 in bf16 (for example InternVL2.5-4B/8B or Gemma-3-4B/12B). Check:
  - whether its chat template allows assistant-turn prefill the way `harness_v5.render_chat` needs;
  - whether teacher-forced scoring works with it (*Which Source Wins?* had to exclude InternVL2 from likelihood scoring, p. 12);
  - the approximate memory footprint;
  - which pinned revision to use (do not guess a hash; say how to obtain it).
- (c) Rescuing Qwen2-VL-2B with a relaxed-format base check. What would that do to the competency invariant?

**D4: ChartQA, the only regime where "reliability" is well-posed.**
- (a) Current: exploratory.
- (b) Prompt rescue: a `CHART_STEMS` rule of "no numbers or answers in Sentence 1", plus `max_pixels` 200704 vs. 401408.
  - From the donor rows, classify why ChartQA items failed: answer leakage, swap count, missing "reliable", other. How many failures would the rule plausibly remove?
  - Can the remaining pool reach R5's 100 items? It holds 229 − 30 dev = 199 items. Show the arithmetic from competency rates.
  - Does testing the rescue spend more items, and how many?
- (c) An alternative evidence-conflict benchmark (CMC-Bench, Ground-CF or others found in the papers). Check licence, size, conflict construction, and whether one source is factually wrong.
- (d) Accept exploratory status and retitle around source following.
- Give the decision as a comparison of what each option lets the thesis claim.

**D5 and the gates (after the 2026-11-14 revision).**
- (a) Current: fixed 5% attributable churn, ±5 pp signed mean, ±10 pp neither shift.
- (b) Any-change churn as the gate, as in CoT-Mediate. What would it imply on dev?
- (c) Whether the ±10 pp neither-shift bound is well-chosen. It is itself a post-hoc number: propose how to justify it or replace it.
- (d) Whether the absolute ε = 5 pp Math rule (Δ against ε) is too easy to pass given dev effects of 30–65 pp. Should a relative criterion against the directional benchmarks be reported? How would that be pre-registered without repeating the ceiling problem?

**Cross-cutting.**
- **Binding vs. non-binding.** Is binding H₁ close to a manipulation check, since the binding instruction says "solve only the problem from the source you named"? Should non-binding (T3_beh) be the headline faithfulness test? What does the literature say about instructed vs. uninstructed reasoning use?
- **Off-policy edits.** *Thought Branches* reports small effects for off-policy edits, but our minimal edits produced large ones. Explain the discrepancy, or mark it [Unknown].
- **Power.** Using dev variances, compute TOST power and the minimum detectable effect at the expected confirm n for 3B and 7B. Is an H₀ claim realistically reachable for either?
- **Human coding.** `Experiment/coding_v5/` has 64 of 200 verdict rows from 3B/7B Math. What sample is needed for κ to support the Math claims? Propose a re-weighting.

### C. Scope and title

Lay out the options for the confirmatory claim and the title, with what each option requires:
1. "Source following under task-selection conflict" (Math only).
2. Source following plus a rescued ChartQA reliability arm.
3. Either of the above, with a cross-family replication.

Say which claims each option supports and which it forbids.

## Required output

Write `Thesis/docs/Archive/openresearch_v5_design_decision_review.md` with these sections:

1. **Summary** (≤ 15 lines): the recommended v5 confirmatory design in one table, covering outcome, contrasts, models, regimes, gates, sampling and title.
2. **History and lessons** (question A).
3. **Corrections ledger**: each stale claim, what is actually true, and the source.
4. **Decision matrix**: one row per alternative in B, with columns *fixes / evidence (rows) / evidence (papers) / GPU cost / items spent / new post-hoc risk / claim impact / recommendation*.
5. **Detailed analysis** per decision point, showing the numbers you recomputed and the commands or code used.
6. **Scope and title options** (C).
7. **Budget**: total GPU hours for the recommended design on one L4, from manifest timings, with assumptions stated.
8. **Pre-freeze checklist**: what must be done, in order, before the tag `prereg-v5`. Mark which items need the researcher's decision and which need GPU time.
9. **Open questions for the researcher**: decisions only they can make, each with your recommendation.
10. **Sources**: papers with the pages read, and files read.

Rules for the report:
- Plain language. One idea per sentence.
- Every number has a denominator and a source.
- If evidence is thin, say "not enough evidence" rather than recommending.
- Do not recommend anything just because it is cheaper or faster to freeze. State the cost, and let the evidence decide.
