# CLAUDE.md

## What This Project Is

Undergraduate BSc CSE thesis by Mohammad Zahed Hossen.

**Working title (pre-registration):** *Does the Verdict Decide? Testing Whether Stated Source Reliability Steers Vision-Language Models under Image–Text Conflict*

The earlier title, *Causal Conflict Verbalization and Source Arbitration in Vision-Language Models*, is retired. The workspace folder keeps the old name.

The thesis tests multimodal chain-of-thought faithfulness. When an image and a typed text support different answers, we prefix-force a reliability verdict into the model's own response ("I consider the image / the typed text more reliable"). The question is whether that verdict causally changes which source's answer the model then gives. Instruction, evidence order and wording are held fixed. The test is run with and without a binding instruction that tells the model to act on its verdict.

The full design is in `Docs/PREREGISTRATION_VERDICT_TRANSPLANT.md`. The evidence behind it is in `Archive/Paper/lit-dossier-verdict-transplant/lit-dossier-verdict-transplant.md`.

## Current Phase

- **Done:** v3 pilot (N = 1,619) and v4 dev runs, both exploratory.
- **Done:** literature audit. The original novelty claim does not hold; the current claim is in the dossier, §4.1.
- **Done:** v5 harness and `analyze_v5.py` are written and pass their CPU tests (`harness_v5.py`, `transplant_v5.py`, `score_v5.py`, `analyze_v5.py`). Nothing in v5 has run on a GPU.
- **Now:** run the v5 dev pass on Colab with `Experiment/RUNBOOK_v5.md` (both models, 200 GSM8K/SVAMP and 30 ChartQA dev items). Record the dev-pass numbers, do the human coding of verdict labels, then freeze the pre-registration.
- **No confirmatory data exists yet, and no v5 data of any kind.**

For current status and next steps, read `Experiment/README.md` first.

## Important: How To Treat Files In This Repo

**Every `.md` document in `Docs/` was AI-generated** during research tracking. They are not ground truth. `Docs/PREREGISTRATION_VERDICT_TRANSPLANT.md` is the one exception: it is the design specification. Even so, check it against code before relying on it.

**The actual ground truth is:**
- `Experiment/results_v4/*.jsonl` and their manifests: v4 dev runs, for tuning only, not findings.
- `Experiment/results_v3/full_experiment_results v3.0.json`: v3 pilot outputs, exploratory and read-only.
- `Experiment/*.py`: active code. `Experiment/archive/harness_v3/` holds the v3 harness.
- `Archive/Paper/*.pdf`: the primary papers behind the dossier.

When in doubt, read the code, data and papers, not the narrative documents.

## Research Setup

- **Models:**
  - `Qwen/Qwen2.5-VL-3B-Instruct`, pinned to `66285546d2b821cf421d4f5eb2576359d3770cd3`
  - `Qwen/Qwen2-VL-2B-Instruct`, pinned to `895c3a49bc3fa70a340399125c650a463535e71c`
  - Both run on Colab Pro 16 GB GPUs. Pins are in `harness_v4.py` (`MODEL_PINS`).
- **Task-selection conflict:** `vlm-modality-research/modality-conflict-arbitration-v2`. GSM8K/SVAMP rendered image of problem *i* paired with typed problem *i+1*; equal-answer pairs excluded. Neither source is wrong here.
- **Evidence conflict:** `vlm-modality-research/chartqa-evidence-conflict-v2`. 229 analysed items (230 rows; `conflict_id` 45 is excluded, as in the paper's artifact): a real chart and a counterfactual report on the same question.
- **Stimuli source:** Ghosh et al., *Which Source Wins?* (arXiv:2608.17205). Cite it.
- **Execution:** Google Colab Pro (NVIDIA T4/V100, 16 GB VRAM, FP16, SDPA).
- **Local machine:** AMD Ryzen 5 5600G, 8 GB RAM, no CUDA. Code editing, tests and analysis only.

## Mandatory Methodological Invariants

Every v5 run and analysis must satisfy all of these. Details are in the pre-registration.

1. **Counterbalanced evidence order.** Run both `<image><text>` and `<text><image>`. The instruction stays fixed before both sources, and the format line stays after them. There are no "Source A/B" labels: sources get modality headers, and only their positions swap (prereg R2).
   - Why: with the instruction fixed, putting a source last moves Qwen2.5-VL-3B toward it by +16.7 / +15.0 pp (arXiv:2609.26986, natural images). If the instruction moves with the text, the sign reverses.
   - v4 prompts always put the image first, so v4 dev never measured an order effect. v5 fixes this in `harness_v5.build_content`. Whether the literature's order effect appears on these stimuli is unknown until the v5 dev pass.
2. **Binding arm plus explicit single-source ceilings.**
   - Binding: "…Then solve only the problem from the source you named as more reliable, and ignore the other problem."
   - Ceilings: `explicit_image` / `explicit_text`. Report any binding effect as a fraction of this ceiling.
   - Why: without binding, a null verdict effect can't be told apart from the instruction dominating.
3. **Minimal-edit verdicts.** Flipped verdicts swap only the source noun phrase in the reliability clause of the model's own `conflict_full` verbalization. Gates: exactly one clause changed; the flip actually reverses `stated_reliable_source`; token Jaccard ≥ 0.85 and at most two swapped noun phrases. Authored sentences (`rel_image` / `rel_text`) are not run in v5; the matched `para` / `para_flip` pair is the robustness check.
4. **Competency conditioning.** Primary results use only items where `base_image` solves the item's image problem and `base_text` solves its text problem, under the same decoding. Items that fail the filter are never transplanted. Cross-model comparisons use the intersection of these sets.
5. **One primary outcome: Δℓ.** This is the length-normalized log-likelihood margin at `####`, image minus text, teacher-forced right after the verdict. Behavioural decodes are secondary: 512-token solving for GSM8K/SVAMP and a 16-token answer-only decode for ChartQA. Ceilings use the no-verdict prefill. No source letters.
6. **Repetition penalty 1.0, greedy decoding, pinned revisions.** Use a new `--run_tag` for any prompt or setting change.

## Claim Boundaries

- Prefix-forcing identifies a **controlled direct effect** of the verdict at a fixed instruction. Never call it "mediation" or a "natural indirect effect".
- Don't claim "first" or "novel" beyond the sources listed in the dossier, §4.1. Read 2610.33841 (*Grounding on Request*) and 2610.19407 in full before claiming novelty for the binding arm.
- In GSM8K/SVAMP, "reliability" is ill-posed because both problems are valid. Reliability claims belong to ChartQA-Conflict.
- Dev numbers are for tuning, never findings. v3 numbers compare two instructions, not verbalizations. See `Experiment/results_v3/README.md`.

## Verified Constants (audit of 2026-11-11)

Recomputed from `Experiment/results_v4/dev2_*.jsonl` with `score_v4.py`, or read from the paper or the Hub on that date. All dev numbers are for tuning only: one model (Qwen2.5-VL-3B), image always first, heuristic labels.

- **Competency:** 110 of 200 dev items pass both single-source arms. Image alone 72.8%, text alone 75.4% (195 distinct problems).
- **Own verdicts (`conflict_full`):** on the 110 competent items, 94 text, 2 image, 14 unparseable. On all 200: 178 text, 4 image, 18 unparseable. So "98%" is 94/96 and "89%" is 178/200. Always state the denominator.
- **Answers on the 94 text-verdict items:** 61 text (64.9%), 19 image (20.2%), 14 neither (14.9%). Observational only.
- **Authored verdict reversal (110 items):** neutral instruction +20.9 pp image answers, 35.5% of items change source label; conflict instruction −1.8 pp, 7.3%.
- **Wording control (110 items):** +7.3 pp / 24.5% (neutral), −1.8 pp / 22.7% (conflict). On all 200, the extracted answer changes in 39.0% / 33.0%. These are different measures; don't quote "22.7–39%" as one range.
- **v3:** abstention is 38 items (2.3%), not 13.65%. Token-cap hits 98.1% / 37.6% / 44.2% in Arms 1–3.
- **Models (Hub):** Qwen2.5-VL-3B-Instruct has 3,754.6M parameters; Qwen2-VL-2B-Instruct has 2,209.0M.
- **Datasets (Hub):** `modality-conflict-arbitration-v2` has 13.0K rows in `train` (1,304 GSM8K + 296 SVAMP distinct-answer pairs at L0, image channel). `chartqa-evidence-conflict-v2` has **230** rows in `test` at the pinned revision. 229 are analysed: `conflict_id` 45 is excluded, as recorded in the *Which Source Wins?* artifact (`excluded_items.json`). `harness_v5.chartqa_analysis_set` enforces both counts.
- **Literature checks:**
  - *Which Source Wins?* (Ghosh, Gupta & Wang) tested Qwen2-VL-2B and Qwen2.5-VL-**7B**, not the 3B. It used Source A/B labels and a text-minus-image margin, and has no faithfulness analysis.
  - The +16.7 / +15.0 pp order effect (arXiv:2609.26986, Table 1) is for natural-image VQA with a forced A/B choice.
  - "Larger models are less faithful" is from Lanham et al. (arXiv:2307.13702), not Turpin et al.
  - Barua et al.'s 1.4–3.8× text-evidence ratio was measured on DocVQA, VQAv2 and RealworldQA, not on ChartQA-Conflict.
  - Dassen et al. (arXiv:2610.33841) do not prefix-force any model text.
- **Overclaim corrected 2026-11-11:** `Experiment/results_v4/README.md` §3 used to say dev "confirms the central causal hypothesis". It doesn't; the `m0` vs. `m1` contrasts swap whole verbalizations. Older docs may still repeat the claim.
- **Naming:** there is no "v2 stimulus stage". v1 and v2 are two 20-item pilots in `Experiment/archive/pilots_v1_v2/`; an N = 500 run is in `Archive/Experiment_History/`. "-v2" is a dataset name suffix.

## Directory Layout

```
├── Experiment/          ← CODE + DATA (ground truth); start at its README.md
│   ├── *.py, tests/     ← Active v4 code and tests (v5 upgrade in progress)
│   ├── RUNBOOK_v4.md    ← Exact commands, in order
│   ├── results_v4/      ← v4 runs and dev analysis
│   ├── results_v3/      ← v3 pilot outputs and re-analysis (read-only)
│   ├── coding_v3/       ← Human-coding sheets
│   └── archive/         ← v3 harness and early pilots
├── Docs/                ← AI-GENERATED TRACKING (reference only)
│   ├── PREREGISTRATION_VERDICT_TRANSPLANT.md ← Design spec (draft, not frozen)
│   ├── *.md             ← Older topic spec, master report, roadmap (stale)
│   ├── Context/         ← Historical context tracking
│   ├── Decision_Audits/ ← Topic selection audit trail; Idea.md is current
│   └── Parked_Proposals/← Deprecated proposal specs
├── Thesis/              ← WHERE THESIS CHAPTERS WILL GO; docs/Understanding/ holds two AI-generated FAQs (audited 2026-11-11, reference only)
├── Archive/             ← Parked exploration; Archive/Paper/ holds the primary PDFs and dossier
└── .agents/             ← Antigravity agent config
```

## Behavioral Rules

1. **Be a research partner, not a cheerleader.** Challenge weak claims and ask for evidence.
2. **Epistemic honesty.** Tag claims as [Verified], [Inferred], [Hypothesis] or [Unknown]. Never invent papers, citations or datasets.
3. **Level 3 rigor.** Competing hypotheses (H₁ vs H₀), noise floors and ceilings, deterministic metrics, pre-registered contrasts. No leaderboard chasing.
4. **Code for Colab, not local.** Any model-touching code targets Colab Pro. The local machine is strictly for editing, tests and analysis.
5. **Don't treat Docs/ as truth.** Cross-check against code, data and the papers in `Archive/Paper/`.
