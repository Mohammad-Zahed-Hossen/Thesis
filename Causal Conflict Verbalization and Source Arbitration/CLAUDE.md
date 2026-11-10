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
- **Now:** upgrade the harness to v5 (order counterbalancing, binding and ceiling arms, minimal-edit verdicts, second model). Then freeze the pre-registration.
- **No confirmatory data exists yet.**

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
- **Evidence conflict:** `vlm-modality-research/chartqa-evidence-conflict-v2`. 229 items: a real chart and a counterfactual report on the same question.
- **Stimuli source:** Ghosh et al., *Which Source Wins?* (arXiv:2608.17205). Cite it.
- **Execution:** Google Colab Pro (NVIDIA T4/V100, 16 GB VRAM, FP16, SDPA).
- **Local machine:** AMD Ryzen 5 5600G, 8 GB RAM, no CUDA. Code editing, tests and analysis only.

## Mandatory Methodological Invariants

Every v5 run and analysis must satisfy all of these. Details are in the pre-registration.

1. **Counterbalanced evidence order.** Run both `<image><text>` and `<text><image>`. The instruction stays fixed before both sources, and the format line stays after them. There are no "Source A/B" labels: sources get modality headers, and only their positions swap (prereg R2).
   - Why: with the instruction fixed, putting a source last moves Qwen2.5-VL-3B toward it by +16.7 / +15.0 pp (arXiv:2609.26986, natural images). If the instruction moves with the text, the sign reverses.
   - `render_chat` currently always puts the image first. That must change.
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
├── Thesis/              ← WHERE THESIS CHAPTERS WILL GO (empty for now)
├── Archive/             ← Parked exploration; Archive/Paper/ holds the primary PDFs and dossier
└── .agents/             ← Antigravity agent config
```

## Behavioral Rules

1. **Be a research partner, not a cheerleader.** Challenge weak claims and ask for evidence.
2. **Epistemic honesty.** Tag claims as [Verified], [Inferred], [Hypothesis] or [Unknown]. Never invent papers, citations or datasets.
3. **Level 3 rigor.** Competing hypotheses (H₁ vs H₀), noise floors and ceilings, deterministic metrics, pre-registered contrasts. No leaderboard chasing.
4. **Code for Colab, not local.** Any model-touching code targets Colab Pro. The local machine is strictly for editing, tests and analysis.
5. **Don't treat Docs/ as truth.** Cross-check against code, data and the papers in `Archive/Paper/`.
