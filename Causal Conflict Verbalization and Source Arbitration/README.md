# Causal Conflict Verbalization and Source Arbitration in Vision-Language Models

> **Researcher:** Mohammad Zahed Hossen (Final-Year BSc CSE, Bangladesh)
> **Status:** Exploratory v3 pilot done; v4 dev phase in progress; no confirmatory data; thesis not started
> **Model:** `Qwen/Qwen2.5-VL-3B-Instruct`
> **Dataset:** `vlm-modality-research/modality-conflict-arbitration-v2`

**For current state and next steps, read [Experiment/README.md](Experiment/README.md).**

## The question

When a VLM gets conflicting image and text inputs, does stating the conflict causally change which source it follows? Or does the statement merely rationalize a choice made anyway?

## Evidence so far

**Exploratory only.** Details and caveats are in [Experiment/results_v3/README.md](Experiment/results_v3/README.md) and [Experiment/results_v4/README.md](Experiment/results_v4/README.md).

- **The v3 instruction contrast is large.** Answers matching the image problem fall from 35.7% to 11.8%, and answers matching the text problem rise from 4.2% to 36.1% (N = 1,600 with distinct answers).
- **That doesn't show verbalization causes it.** v3 randomized the instruction only. The v4 transplant is designed to separate the two, and its first dev run was invalid.
- **The neutral placebo in v3 isn't inert.** Direct prompting leans toward the text, so "reversing visual capture" isn't supported.
- **Dev data suggest `repetition_penalty` matters.** v3 ran at the model's default of 1.05, and this appears to raise image answers and abstention labels. This still needs confirmatory testing.

## Repository

```
├── Experiment/     Code and data; start at its README
├── Thesis/         Thesis chapters; empty so far
├── Docs/           AI-generated tracking; reference only, partly stale
├── Archive/        Parked explorations (Bengali VLM, medical imaging, etc.)
├── CLAUDE.md       Claude directives
├── AGENTS.md       Instructions for other agents
└── .agents/        Antigravity configuration
```

## Compute

| Component | Spec | Use |
|---|---|---|
| Local | AMD Ryzen 5 5600G, 8 GB RAM, no CUDA | Editing, tests, analysis |
| GPU | Google Colab Pro (T4/V100) | All model runs |
| Model | Up to 3B parameters | Inference only |
