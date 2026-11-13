# Does the Verdict Decide? Testing Whether Stated Source Reliability Steers Vision-Language Models under Image–Text Conflict

*(Folder name unchanged: `Causal Conflict Verbalization and Source Arbitration`)*

> **Researcher:** Mohammad Zahed Hossen (Final-Year BSc CSE, Bangladesh)
> **Status:** v3 pilot and v4 dev done; v5 dev pass done and audited (pre-registration not yet frozen; **no confirmatory data**)
> **Models:** `Qwen/Qwen2-VL-2B-Instruct`, `Qwen/Qwen2.5-VL-3B-Instruct`, `Qwen/Qwen2.5-VL-7B-Instruct`
> **Datasets:** `vlm-modality-research/modality-conflict-arbitration-v2` (GSM8K/SVAMP) and `vlm-modality-research/chartqa-evidence-conflict-v2`

**For current state and next steps, read [Experiment/README.md](Experiment/README.md).**

## The question

When an image and a typed text support different answers, does a prefix-forced source-reliability verdict causally steer which source's answer a VLM gives (controlled direct effect)? Or does the answer follow the instruction, evidence order, or prior commitment regardless of what the verdict says?

## Evidence so far

**Exploratory and dev-only.** Details and caveats are in [Experiment/results_v3/README.md](Experiment/results_v3/README.md), [Experiment/results_v4/README.md](Experiment/results_v4/README.md), [Experiment/results_v5/README.md](Experiment/results_v5/README.md), and [Thesis/docs/Archive/claude_v5_independent_deep_audit.md](Thesis/docs/Archive/claude_v5_independent_deep_audit.md).

- **The v3 instruction contrast is large, but doesn't test verbalization.** Answers matching the image problem fall from 35.7% to 11.8%, and answers matching the text problem rise from 4.2% to 36.1% (N = 1,600 with distinct answers). That compared two *instructions*, not two verbalizations.
- **v4 dev (`dev2`):** On the 110 items solvable from both sources, reversing an authored verdict moved image answers by +20.9 pp under the neutral instruction and −1.8 pp under the conflict instruction.
- **v5 dev pass:** 29,880 rows across all three models ran on an L4 in `bfloat16` (`Experiment/results_v5/`). Audits flagged pre-freeze blockers (2B `####` format eligibility, ChartQA attrition, Math Δℓ–behaviour agreement, and replay/wording churn) that must be settled before freezing [Docs/PREREGISTRATION_VERDICT_TRANSPLANT.md](Docs/PREREGISTRATION_VERDICT_TRANSPLANT.md).

## Repository

```
├── Experiment/     Code and data (ground truth); start at Experiment/README.md
│   ├── results_v5/ v5 dev pass (29,880 rows); see its README
│   ├── results_v4/ v4 dev runs and analysis; see its README
│   └── results_v3/ v3 pilot, N = 1,619; see its README
├── Thesis/         Writing guides, FAQs, runbooks, compute evaluations, and v5 dev audits (chapters not yet drafted)
├── Docs/           Pre-registration draft, primary PDFs/literature audits (Docs/Paper/), and historical decision records
├── Archive/        Parked explorations (Bengali VLM, medical imaging, multimodal agents, etc.)
├── CLAUDE.md       Claude directives
├── AGENTS.md       Instructions for other agents
└── .agents/        Antigravity configuration
```

## Compute

| Component | Spec | Use |
|---|---|---|
| Local | AMD Ryzen 5 5600G, 8 GB RAM, no CUDA | Editing, tests, analysis |
| GPU | NVIDIA L4 / A100 (Colab Pro) or RTX 3090/4090, ≥ 24 GB, `bfloat16` | Primary compute for v5 (T4/V100 not used: `float16` only) |
| Models | 2B, 3B, 7B parameters (`bfloat16`) | Inference only |
