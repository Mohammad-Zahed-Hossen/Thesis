# Does the Verdict Decide? Testing Whether Stated Source Reliability Steers Vision-Language Models under Image–Text Conflict

*(Folder name unchanged: `Causal Conflict Verbalization and Source Arbitration`)*

> **Researcher:** Mohammad Zahed Hossen (Final-Year BSc CSE, Bangladesh)
> **Status:** v3 pilot and v4 dev done; v5 dev rerun (`2026-11-15/16`, `34,920` rows + `px501k` R8.4 comparison + `analysis_dev/` + `lme4_out.txt`) complete; double human coding complete and adjudicated (2026-11-20); 255 CPU unit tests pass; pre-registration not yet frozen (**no confirmatory data**)
> **Models:** `Qwen/Qwen2-VL-2B-Instruct` (diagnostic-only, D3), `Qwen/Qwen2.5-VL-3B-Instruct` & `Qwen/Qwen2.5-VL-7B-Instruct` (confirmatory)
> **Datasets:** `vlm-modality-research/modality-conflict-arbitration-v2` (GSM8K/SVAMP) and `vlm-modality-research/chartqa-evidence-conflict-v2` (exploratory, D4)

**For current state and next steps, read [Experiment/README.md](Experiment/README.md).**

## The question

When an image and a typed text support different answers, does a prefix-forced source-reliability verdict causally steer which source's answer a VLM gives (controlled direct effect)? Or does the answer follow the instruction, evidence order, or prior commitment regardless of what the verdict says?

## Evidence so far

**Exploratory and dev-only.** Details and caveats are in [Experiment/results_v3/README.md](Experiment/results_v3/README.md), [Experiment/results_v4/README.md](Experiment/results_v4/README.md), [Experiment/results_v5/README.md](Experiment/results_v5/README.md), and [claude_v5_independent_deep_audit.md](<Thesis/docs/Archive/dev v5/claude_v5_independent_deep_audit.md>).

- **The v3 instruction contrast is large, but doesn't test verbalization.** Answers matching the image problem fall from 35.7% to 11.8%, and answers matching the text problem rise from 4.2% to 36.1% (N = 1,600 with distinct answers). That compared two *instructions*, not two verbalizations.
- **v4 dev (`dev2`):** On the 110 items solvable from both sources, reversing an authored verdict moved image answers by +20.9 pp under the neutral instruction and −1.8 pp under the conflict instruction.
- **v5 dev pass:** The post-fix `2026-11-15/16` dev rerun across all three models on an L4 in `bfloat16` (`34,920` rows across `20` `.jsonl` files, including the `px501k` ChartQA `max_pixels` comparison and `analysis_dev/` + `lme4_out.txt`) is in [Experiment/results_v5/README.md](Experiment/results_v5/README.md); the initial `2026-11-12/13` pass (`29,880` rows) is archived in [Experiment/archive/results_v5_Prev_backup/README.md](Experiment/archive/results_v5_Prev_backup/README.md). Audits ([fable52-prefreeze-audit-2026-11-15.md](Docs/Paper/fable52-prefreeze-audit-2026-11-15.md), [claude_v5_independent_deep_audit.md](<Thesis/docs/Archive/dev v5/claude_v5_independent_deep_audit.md>)) and fixes (`F2`, `F3`, `F5`–`F13`, `Upgrades 1–5`, `preflight_v5.py`) led to pre-freeze decisions D1–D5 (Math behavioural primary, `Qwen2-VL-2B` diagnostic-only, ChartQA exploratory, fixed 5% churn gate), double human coding (`Experiment/coding_v5/`, 200 verdicts + 150 flips, `0`-diff donor match; coded and adjudicated on 2026-11-20 in `adjudication_v5.csv` / `evaluation_v5.json`; audited in [Antigravity Audit.md](<Thesis/docs/Archive/Antigravity Audit.md>) and [claude_coding_v5_independent_audit.md](Thesis/docs/Archive/claude_coding_v5_independent_audit.md)), locking ChartQA `max_pixels` at `200704` (§3.4), an 18-paper + CMC-Bench literature synthesis ([Docs/Paper/THESIS_LITERATURE_KNOWLEDGE_BASE.md](Docs/Paper/THESIS_LITERATURE_KNOWLEDGE_BASE.md)), the 2026-11-15 pre-freeze literature audit + 2026-11-17 gap-closure addendum ([Docs/Paper/lit-audit-2026-11-15/lit-audit-2026-11-15.md](Docs/Paper/lit-audit-2026-11-15/lit-audit-2026-11-15.md), `1,452` screened records; brief in [Docs/RESEARCH_OBJECTIVE.md](Docs/RESEARCH_OBJECTIVE.md)), and 16 related-work GitHub repo snapshots ([Docs/Paper/related_repos/](Docs/Paper/related_repos/README.md)) before freezing [Docs/PREREGISTRATION_VERDICT_TRANSPLANT.md](Docs/PREREGISTRATION_VERDICT_TRANSPLANT.md).

## Repository

```
├── Experiment/     Code and data (ground truth); start at Experiment/README.md
│   ├── results_v5/ v5 post-fix dev rerun (34,920 rows) + px501k + analysis_dev/ (incl. lme4_out.txt); see its README
│   ├── results_v4/ v4 dev runs and analysis; see its README
│   ├── results_v3/ v3 pilot, N = 1,619; see its README
│   ├── coding_v5/  v5 double human coding (200 verdicts, 150 flips), adjudicated (adjudication_v5.csv, evaluation_v5.json)
│   └── archive/    Superseded v3 harness, v1/v2 pilots, and results_v5_Prev_backup/ (29,880 rows)
├── Thesis/         Writing guides, FAQs, runbooks, compute evaluations, and v5 dev & coding audits (chapters not yet drafted)
├── Docs/           Onboarding brief (RESEARCH_OBJECTIVE.md), pre-registration draft, 18-paper + CMC-Bench knowledge base / 29 local PDFs + 16 repo snapshots + 2026-11-15 audits (Docs/Paper/), and historical decision records
├── Archive/        Parked explorations (Bengali VLM, medical imaging, multimodal agents, etc.)
├── CLAUDE.md       Claude directives
├── AGENTS.md       Instructions for other agents
└── .agents/        Antigravity configuration
```

## Compute

| Component | Spec | Use |
|---|---|---|
| Local | AMD Ryzen 5 5600G, 8 GB RAM, no CUDA | Editing, tests, analysis |
| GPU | NVIDIA L4 (23,034 MiB) / A100 (Colab Pro) or RTX 3090/4090, ≥ 22 GiB VRAM, `bfloat16` | Primary compute for v5 (T4/V100 not used: `float16` only) |
| Models | 2B, 3B, 7B parameters (`bfloat16`) | Inference only |
