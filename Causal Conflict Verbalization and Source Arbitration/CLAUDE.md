# CLAUDE.md

## What This Project Is

Undergraduate BSc CSE thesis by Mohammad Zahed Hossen.

**Working title (pre-registration):** *Does the Verdict Decide? Testing Whether Stated Source Reliability Steers Vision-Language Models under Image–Text Conflict*

The earlier title, *Causal Conflict Verbalization and Source Arbitration in Vision-Language Models*, is retired. The workspace folder keeps the old name.

The thesis tests multimodal chain-of-thought faithfulness. When an image and a typed text support different answers, we prefix-force a reliability verdict into the model's own response ("I consider the image / the typed text more reliable"). The question is whether that verdict causally changes which source's answer the model then gives. Instruction, evidence order and wording are held fixed. The test is run with and without a binding instruction that tells the model to act on its verdict.

The full design is in `Docs/PREREGISTRATION_VERDICT_TRANSPLANT.md`, with a quick onboarding brief in `Docs/RESEARCH_OBJECTIVE.md`. The evidence behind it is in `Docs/Paper/THESIS_LITERATURE_KNOWLEDGE_BASE.md` (18 core papers + CMC-Bench; 29 local PDFs: 20 core/lead + 6 audit A-papers + 3 cited B-papers, 0 core missing, listed in `Docs/Paper/README.md`), alongside `Docs/Paper/lit-audit-2026-11-15/lit-audit-2026-11-15.md`, `Docs/Paper/fable52-prefreeze-audit-2026-11-15.md` (with 16 repo snapshots in `Docs/Paper/related_repos/`), `Docs/Paper/post-v5-pdf-audit/post-v5-pdf-audit.md`, and `Docs/Paper/lit-dossier-verdict-transplant/lit-dossier-verdict-transplant.md`.

## Current Phase

- **Done:** v3 pilot (N = 1,619) and v4 dev runs, both exploratory.
- **Done:** 18-paper + CMC-Bench literature audit (`Docs/Paper/THESIS_LITERATURE_KNOWLEDGE_BASE.md`), pre-registration freeze audit (`Docs/Paper/prereg-freeze-audit/`), and pre-freeze literature audit (`Docs/Paper/lit-audit-2026-11-15/lit-audit-2026-11-15.md`, `Docs/RESEARCH_OBJECTIVE.md`).
- **Done:** v5 dev pass across all three models on an L4 in `bfloat16` (29,880 rows in `Experiment/results_v5/`), audited in `Thesis/docs/Archive/`, `analyze_v5.py` run on dev (`Experiment/results_v5/analysis_dev/`), pre-freeze decisions D1–D5 + gate revisions, Fable 5.2 forensic audit fixes (`F2`, `F3`, `F5`–`F13`, `Upgrades 1–5`, `Experiment/preflight_v5.py`), and `lit-audit-2026-11-15` §1.3/§4 + title/scope alignment synced into the draft.
- **Now:** complete double human coding (`Experiment/coding_v5/`), close ChartQA `max_pixels` (R8.4: `200704` vs `501760`) + GPU `--print_example` render & `--limit 20` `verdict_nll` span smoke checks, verify Fable 5.2 final sign-off, and commit + tag `prereg-v5`.
- **No confirmatory data exists yet.**

For current status and next steps, read `Experiment/README.md` first.

## Important: How To Treat Files In This Repo

**Every `.md` document in `Docs/` was AI-generated** during research tracking. They are not ground truth. `Docs/PREREGISTRATION_VERDICT_TRANSPLANT.md` is the one exception: it is the design specification. Even so, check it against code before relying on it.

**The actual ground truth is:**
- `Experiment/results_v5/*.jsonl` and their manifests/gates: v5 dev pass outputs, for tuning/diagnostics only, not findings.
- `Experiment/results_v4/*.jsonl` and their manifests: v4 dev runs, for tuning only, not findings.
- `Experiment/results_v3/full_experiment_results v3.0.json`: v3 pilot outputs, exploratory and read-only.
- `Experiment/*.py`: active code. `Experiment/archive/harness_v3/` holds the v3 harness.
- `Docs/Paper/*.pdf`: the primary papers behind the dossier.

When in doubt, read the code, data and papers, not the narrative documents.

## Research Setup

- **Models (two confirmatory + one diagnostic-only; updated pre-freeze D3, 2026-11-13):**
  - `Qwen/Qwen2-VL-2B-Instruct`, pinned to `895c3a49bc3fa70a340399125c650a463535e71c` (**diagnostic-only**, D3)
  - `Qwen/Qwen2.5-VL-3B-Instruct`, pinned to `66285546d2b821cf421d4f5eb2576359d3770cd3` (confirmatory)
  - `Qwen/Qwen2.5-VL-7B-Instruct`, pinned to `cc594898137f460bfe9f0759e9844b3ce807cfb5` (confirmatory)
  - Pins are in `harness_v4.py` (`MODEL_PINS`). Claims are made per model; a cross-model statement needs both confirmatory models to agree. 3B vs. 7B is a descriptive within-generation size comparison, not a scaling law.
- **Task-selection conflict (confirmatory Math):** `vlm-modality-research/modality-conflict-arbitration-v2`. GSM8K/SVAMP rendered image of problem *i* paired with typed problem *i+1*; equal-answer pairs excluded. Neither source is wrong here.
- **Evidence conflict (exploratory/secondary, D4):** `vlm-modality-research/chartqa-evidence-conflict-v2`. 229 analysed items (230 rows; `conflict_id` 45 is excluded, as in the paper's artifact): a real chart and a counterfactual report on the same question.
- **Stimuli source:** Ghosh et al., *Which Source Wins?* (arXiv:2608.17205). Cite it.
- **Execution (v5):** `bfloat16`, SDPA, no quantization, on one GPU class with compute capability ≥ 8 and at least 22 GiB usable VRAM (NVIDIA L4 [23,034 MiB], A100, RTX 3090/4090). `harness_v5.HFBackend` refuses any other dtype. T4/V100 are not used for v5: they fall back to `float16`, and the 7B does not fit. v4 dev ran `float16` on a T4.
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
5. **Regime-split primary outcomes (pre-freeze D1 & D2).** In GSM8K/SVAMP (Math), the primary outcome is behavioural choice shift $\Delta P(Y{=}T)$ at template $k=1$ (`structured` parser; `para_flip - para` co-primary with `flip - own`), and $\Delta\ell$ at `####` is secondary/diagnostic. In ChartQA-Conflict (exploratory, D4), $\Delta\ell$ (image minus text) remains primary. Explicit single-source arms use the no-verdict prefill ($m_\varnothing$). No source letters.
6. **Repetition penalty 1.0, greedy decoding, pinned revisions.** Use a new `--run_tag` for any prompt or setting change.

## Claim Boundaries

- Prefix-forcing identifies a **controlled direct effect** of the verdict at a fixed instruction. Never call it "mediation" or a "natural indirect effect".
- Don't claim "first" or "novel" beyond `Docs/PREREGISTRATION_VERDICT_TRANSPLANT.md` §1.1 and `Docs/Paper/THESIS_LITERATURE_KNOWLEDGE_BASE.md` (18 papers + CMC-Bench).
- In GSM8K/SVAMP, "reliability" is ill-posed because both problems are valid; confirmatory claims are about **source following**. Reliability judgement belongs to ChartQA-Conflict (now exploratory per D4).
- Dev numbers are for tuning, never findings. v3 numbers compare two instructions, not verbalizations. See `Experiment/results_v3/README.md`.

## Verified Constants (audit of 2026-11-11)

Recomputed from `Experiment/results_v4/dev2_*.jsonl` with `score_v4.py`, or read from the paper or the Hub on that date. All dev numbers are for tuning only: one model (Qwen2.5-VL-3B), image always first, heuristic labels.

- **Competency:** 110 of 200 dev items pass both single-source arms. Image alone 72.8%, text alone 75.4% (195 distinct problems).
- **Own verdicts (`conflict_full`):** on the 110 competent items, 94 text, 2 image, 14 unparseable. On all 200: 178 text, 4 image, 18 unparseable. So "98%" is 94/96 and "89%" is 178/200. Always state the denominator.
- **Answers on the 94 text-verdict items:** 61 text (64.9%), 19 image (20.2%), 14 neither (14.9%). Observational only.
- **Authored verdict reversal (110 items):** neutral instruction +20.9 pp image answers, 35.5% of items change source label; conflict instruction −1.8 pp, 7.3%.
- **Wording control (110 items):** +7.3 pp / 24.5% (neutral), −1.8 pp / 22.7% (conflict). On all 200, the extracted answer changes in 39.0% / 33.0%. These are different measures; don't quote "22.7–39%" as one range.
- **v3:** abstention is 38 items (2.3%), not 13.65%. Token-cap hits 98.1% / 37.6% / 44.2% in Arms 1–3.
- **Models (Hub):** Qwen2-VL-2B-Instruct has 2,209.0M parameters; Qwen2.5-VL-3B-Instruct has 3,754.6M; Qwen2.5-VL-7B-Instruct has 8,292.2M (about 16.6 GB of weights). The three pinned revisions ship an identical chat template.
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
│   ├── *.py, tests/     ← Active v4/v5 code, preflight_v5.py, and tests
│   ├── RUNBOOK_v4.md, RUNBOOK_v5.md ← Execution runbooks
│   ├── results_v5/      ← v5 dev pass outputs (29,880 rows)
│   ├── results_v4/      ← v4 runs and dev analysis
│   ├── results_v3/      ← v3 pilot outputs and re-analysis (read-only)
│   ├── coding_v5/       ← v5 human-coding sheets (verdicts + flips)
│   ├── coding_v3/       ← v3 human-coding sheets
│   └── archive/         ← v3 harness and early pilots
├── Docs/                ← AI-GENERATED TRACKING (reference only)
│   ├── RESEARCH_OBJECTIVE.md                 ← Onboarding brief: RQ, estimand, narrowed novelty, reading order
│   ├── PREREGISTRATION_VERDICT_TRANSPLANT.md ← Design spec (draft, not frozen)
│   ├── Paper/           ← 29 primary PDFs, 16 related_repos/ snapshots, lit KB, pre-freeze & Fable 5.2 audits, dossier, freeze audit
│   ├── *.md             ← Older topic spec, master report, roadmap (stale)
│   ├── Context/         ← Historical context tracking
│   ├── Decision_Audits/ ← Topic selection audit trail; Idea.md is current
│   └── Parked_Proposals/← Deprecated proposal specs
├── Thesis/              ← WHERE THESIS CHAPTERS WILL GO; docs/ holds Understanding FAQs, Compute evals, RUNBOOKs, and Archive/dev v5/ (v5 dev audits); dev v1_v5.md is a 2026-11-13 snapshot
├── Archive/             ← Parked exploration domains (inactive)
└── .agents/             ← Antigravity agent config
```

## Behavioral Rules

1. **Be a research partner, not a cheerleader.** Challenge weak claims and ask for evidence.
2. **Epistemic honesty.** Tag claims as [Verified], [Inferred], [Hypothesis] or [Unknown]. Never invent papers, citations or datasets.
3. **Level 3 rigor.** Competing hypotheses (H₁ vs H₀), noise floors and ceilings, deterministic metrics, pre-registered contrasts. No leaderboard chasing.
4. **Code for the GPU session, not local.** Any model-touching code targets the pre-registered GPU class (Colab Pro L4/A100 or an RTX 3090/4090). The local machine is strictly for editing, tests and analysis.
5. **Don't treat Docs/ as truth.** Cross-check against code, data and the papers in `Docs/Paper/`.
