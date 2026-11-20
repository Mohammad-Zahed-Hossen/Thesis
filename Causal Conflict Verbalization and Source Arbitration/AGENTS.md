# AGENTS.md — Thesis Research & Development Directives

> **Workspace:** Causal Conflict Verbalization and Source Arbitration  
> **Principal Researcher:** Mohammad Zahed Hossen (Technical Lead, Final-Year BSc CSE)  
> **Target Horizon:** 2026–2027  
> **Applicable Agents:** Antigravity, Claude, and all LLM Pair Programmers  

---

## 1. Project Overview

- **Parent Field:** Multimodal / Vision-Language Learning and Systems (**FROZEN**)
- **Working Title (pre-registration):** *Does the Verdict Decide? Testing Whether Stated Source Reliability Steers Vision-Language Models under Image–Text Conflict*
  - Replaces "Causal Conflict Verbalization and Source Arbitration in VLMs"; the folder name is unchanged.
- **Research Focus:** Multimodal chain-of-thought faithfulness. Under image–text conflict, does a prefix-forced reliability verdict causally steer which source's answer the model gives?
  - Held fixed: instruction, counterbalanced evidence order, and wording template.
  - Varied: with vs. without a binding instruction.
- **Models:** `Qwen/Qwen2.5-VL-3B-Instruct` and `Qwen/Qwen2.5-VL-7B-Instruct` (confirmatory), plus `Qwen/Qwen2-VL-2B-Instruct` (**diagnostic-only**, pre-freeze D3). v5 runs in `bfloat16` on one ≥ 22 GiB GPU class (NVIDIA L4 [23,034 MiB], A100, RTX 3090/4090); revisions are pinned in `Experiment/harness_v4.py` (`MODEL_PINS`). Claims are per model.
- **Stimuli:**
  - Task-selection conflict (confirmatory Math): `vlm-modality-research/modality-conflict-arbitration-v2` (GSM8K/SVAMP).
  - Evidence conflict (exploratory/secondary, D4): `vlm-modality-research/chartqa-evidence-conflict-v2` (229 analysed items; the 230-row release minus `conflict_id` 45).
  - Both come from *Which Source Wins?* (arXiv:2608.17205).
- **Design Spec:** `Docs/PREREGISTRATION_VERDICT_TRANSPLANT.md` (frozen at tag `prereg-v5`, 2026-11-20), with a concise onboarding brief in `Docs/RESEARCH_OBJECTIVE.md`. Evidence base: `Docs/Paper/THESIS_LITERATURE_KNOWLEDGE_BASE.md` (18 core papers + CMC-Bench; 29 local PDFs: 20 core/lead + 6 audit A-papers + 3 cited B-papers; 0 core missing, listed in `Docs/Paper/README.md`) alongside `Docs/Paper/lit-audit-2026-11-15/lit-audit-2026-11-15.md`, `Docs/Paper/fable52-prefreeze-audit-2026-11-15.md` (with `Docs/Paper/related_repos/`, 16 public repo snapshots), `Docs/Paper/post-v5-pdf-audit/post-v5-pdf-audit.md`, and `Docs/Paper/lit-dossier-verdict-transplant/lit-dossier-verdict-transplant.md`.
- **Current Phase:** v3 pilot and v4 dev runs are done (exploratory only), and the 18-paper + CMC-Bench literature KB, the 2026-11-15 pre-freeze literature audit + 2026-11-17 gap-closure addendum (`lit-audit-2026-11-15/`, `1,452` records, `6` A + `41` B), and the Fable 5.2 forensic audit fixes (`F2`, `F3`, `F5`–`F13`, `Upgrades 1–5`, `Experiment/preflight_v5.py`, plus `lit-audit-2026-11-15` §1.3/§4/§7 sync and title/scope alignment) are applied. The fresh `2026-11-15/16` post-fix v5 dev rerun has completed on an L4 in `bfloat16` across all three models (**34,920 rows** in `Experiment/results_v5/`, including `px501k` ChartQA `max_pixels` comparison, verified `verdict_nll` spans, and `resolved_model_commit` manifests; the initial `29,880`-row pass is archived in `Experiment/archive/results_v5_Prev_backup/`), `Experiment/analyze_v5.py` and `lme4` have been run on the fresh dev pass (`Experiment/results_v5/analysis_dev/` incl. `lme4_out.txt`), and pre-freeze decisions D1–D5 + gate revisions are written into the pre-registration. Double human coding (`Experiment/coding_v5/`) is complete and adjudicated (`adjudication_v5.csv`, `evaluation_v5.json`; prereg §8 revised and logged in §11 on 2026-11-20), and ChartQA `max_pixels` is locked at `200704` (§3.4). Pre-registration **frozen** on `main` at tag `prereg-v5` (2026-11-20); next: run `--phase confirm` on GPU. **No confirmatory data exists.**

### What the Pilot Does and Does Not Show
- The pipeline works on `Qwen/Qwen2.5-VL-3B-Instruct` on a T4 [Verified].
- The v3 contrast (placebo vs. conflict prompt) is large, but it compares two *instructions*, not verbalizations [Verified, `Experiment/results_v3/README.md`].
- In v4 dev, on the 110 items solvable from both sources, reversing a forced verdict moved image answers by +20.9 pp under the neutral instruction and −1.8 pp under the conflict instruction. This is dev data only, not a finding [Verified, dossier §2.2].

### Mandatory Methodological Invariants (v5 onward)
1. **Evidence order counterbalanced.** Run `<image><text>` and `<text><image>`. Keep the instruction fixed before both sources and the format line after them. Use no source letters, only modality headers (prereg R2). This controls the roughly +15 pp recency effect in Qwen2.5-VL-3B (arXiv:2609.26986).
2. **Binding arm plus explicit single-source ceilings.** Binding: "solve only the problem from the source you named as more reliable". Ceilings: `explicit_image` / `explicit_text`. These remove prompt ambiguity and bound the binding effect.
3. **Minimal-edit verdicts.** Swap only the source noun in the model's own generated reliability clause. Gates: one clause changed; the stated source actually flips; token Jaccard ≥ 0.85 and at most two swapped noun phrases. Foreign authored verdicts are not run in v5; the matched `para` / `para_flip` pair is the robustness check.
4. **Competency conditioning.** Primary results use only items where `base_image` and `base_text` both solve their problems in isolation.
5. **Regime-split primary outcomes (pre-freeze D1 & D2).** In GSM8K/SVAMP (Math), the primary outcome is behavioural choice shift $\Delta P(Y{=}T)$ at template $k=1$ (`structured` parser; `para_flip - para` co-primary with `flip - own`), and $\Delta\ell$ at `####` is secondary/diagnostic. In ChartQA-Conflict (exploratory, D4), $\Delta\ell$ (image minus text) remains primary. Explicit single-source arms use the no-verdict prefill ($m_\varnothing$) as a benchmark (`B_beh` / `Ceil_ℓ`). No source letters.
6. **Claim boundary.** Prefix-forcing identifies a controlled direct effect, not mediation. Confirmatory claims cover Math *source following* only (not reliability judgement). No "first" claims beyond `Docs/PREREGISTRATION_VERDICT_TRANSPLANT.md` §1.1 / `Docs/Paper/THESIS_LITERATURE_KNOWLEDGE_BASE.md`.

---

## 2. CRITICAL: File Trust Levels

> [!IMPORTANT]
> **All `.md` files in `Docs/` are AI-generated tracking documents.** They are NOT ground truth. They may contain inaccuracies or stale plans.

| Location | Trust Level | What It Contains |
|:---------|:-----------|:-----------------|
| `Experiment/*.py` | **Ground truth** | Active v4/v5 code; start at `Experiment/README.md` |
| `Experiment/results_v5/`, `results_v4/`, `results_v3/` | **Ground truth** | Run outputs and analysis; each has a README |
| `Experiment/archive/` | **Historical** | v3 harness and early pilots |
| `Docs/PREREGISTRATION_VERDICT_TRANSPLANT.md` | **Design spec** | Frozen pre-registration (`prereg-v5`); check it against code |
| `Docs/` (other files) | **Reference only** | AI-generated narrative, tracking, and decision logs; several are stale |
| `Docs/Paper/` | **Primary sources** | Downloaded papers, literature dossier, and pre-registration freeze audit |
| `Archive/` (other files) | **Historical** | Parked explorations, not active |

---

## 3. Agent Behavioral Rules

1. **Scientific Rigor (Level 3):** Controlled factorial interventions with pre-registered contrasts, wording-noise floors and instruction ceilings. No leaderboard chasing.
2. **Epistemic Tags:** `[Verified]`, `[Inferred]`, `[Hypothesis]`, `[Unknown]`.
3. **No Hallucinations:** Never invent papers, citations, datasets, or repos.
4. **Don't treat Docs/ as truth:** Cross-check narrative claims against actual code and data.
5. **No reopening parked fields** without new primary evidence.

---

## 4. Hardware & Execution Boundaries

| Environment | Specs | Rules |
|:-----------|:------|:------|
| **Local** | AMD Ryzen 5 5600G, 8 GB RAM, no CUDA | Code editing, docs, git, analysis only. No model loading. |
| **GPU session** | NVIDIA L4 (23,034 MiB) / A100 (Colab Pro) or RTX 3090/4090, ≥ 22 GiB, `bfloat16` | Primary compute for v5. T4/V100 are not used: they load `float16`, which the v5 harness refuses. |
| **Model** | Qwen2-VL-2B (2.2B), Qwen2.5-VL-3B (3.75B), Qwen2.5-VL-7B (8.29B) | Inference-first. No quantization. No full pretraining. |

---

## 5. Directory Structure

```
├── Experiment/          ← CODE + DATA (ground truth)
│   ├── README.md        ← Current status; read first
│   ├── *.py, tests/     ← Active v4/v5 code, preflight_v5.py, and tests
│   ├── results_v5/      ← v5 post-fix dev rerun (34,920 rows) + px501k + analysis_dev/ (incl. lme4_out.txt)
│   ├── results_v4/      ← v4 runs and dev analysis
│   ├── results_v3/      ← v3 pilot outputs and re-analysis
│   ├── coding_v5/       ← v5 human-coding sheets (verdicts + flips), adjudicated (adjudication_v5.csv, evaluation_v5.json)
│   ├── coding_v3/       ← v3 human-coding sheets
│   └── archive/         ← v3 harness, v1/v2 pilots, and results_v5_Prev_backup/ (29,880 rows)
├── Docs/                ← AI-generated tracking (reference only)
│   ├── RESEARCH_OBJECTIVE.md                 ← Onboarding brief (post-2026-11-15 audit)
│   ├── PREREGISTRATION_VERDICT_TRANSPLANT.md ← Design spec (frozen at `prereg-v5`)
│   ├── Paper/           ← 29 primary PDFs, 16 related_repos/ snapshots, lit KB, pre-freeze & Fable 5.2 audits, dossier, freeze audit
│   ├── Context/         ← Historical context
│   ├── Decision_Audits/ ← Topic selection audits
│   └── Parked_Proposals/← Deprecated proposals
├── Thesis/              ← Writing guides, FAQs, runbooks, compute evals, v5 dev & coding audits (chapters not yet drafted)
├── Archive/             ← Parked exploration domains
├── CLAUDE.md            ← Claude-specific directives
└── .agents/             ← Antigravity agent config
```

---

## 6. Code Conventions

- **Python & PyTorch:** Modular, reproducible, PEP8-compliant.
- **Transformers:** Explicit revision tags, `torch_dtype=torch.bfloat16` for v5 (`float16` for historical v4), `attn_implementation="sdpa"`.
- **Paths:** Relative or configurable CLI args. Structured JSON/JSONL logging.
