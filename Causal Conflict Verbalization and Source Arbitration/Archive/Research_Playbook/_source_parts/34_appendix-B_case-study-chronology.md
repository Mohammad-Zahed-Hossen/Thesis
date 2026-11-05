---

# Appendix B: reconstructed case-study chronology from this workspace

## B.1 What the corpus contains

Approximately **68 Markdown documents** and **7 Python files**, plus raw results (JSON, CSV), LaTeX tables, a notebook, and two PDFs — spread across `Context/`, `Finalize Topic/`, `VLM/`, `Bengali VLM/`, `Multimodal Agent/`, `Medical Imaging & FL/`, and `Extra Field Exploration/`. There is **no Git history**, so ordering below is reconstructed from content, cross-references, filenames, and experiment provenance **[L2]**.

## B.2 Reconstructed sequence

| Stage | Evidence in the corpus | What it demonstrates |
|---|---|---|
| 1. Broad area orientation | `Extra Field Exploration/Plan.md`, `phase-1---landscape-map---antithesis-scan-turn-1.md`, `VLM Landscape and Adversarial Antithesis Scan.md`, `VLM MLLM Antithesis Scan.md` | Orientation was genuinely broad: multiple subfields scanned and mapped |
| 2. Candidate-field audits | `Medical Imaging & FL/*` (6 docs), `Multimodal Agent/*` (4 docs), `Bengali VLM/*` (10 docs) | Each field received a large audit before a feasibility verdict |
| 3. Consolidation into canonical candidates | `Finalize Topic/Canonical_Proposal_1_Reasoning_Trace_Degradation.md`, `..._2_Binding_IDs_Natural_Transfer.md`, `..._3_Cultural_*` (two variants), plus `Clean Explanation (All 4 Idea).md` | Four candidates were developed in parallel to proposal depth |
| 4. Adversarial audits and decisions | `Final Four-Proposal Thesis Decision Audit.md`, `final_adversarial_thesis_decision_audit.md`, `Extra/FINAL THESIS DECISION AUDIT.md`, `Structural Taxonomy Mind Map...` | Decision documents existed, but were produced after large audits |
| 5. Locked specification | `Canonical_Thesis_Topic_Specification (Locked).md` (four arms; H₁ deliberative control vs H₀ post-hoc rationalization; threats-to-validity table) | The final question had a genuine competing-hypothesis structure — a real methodological step forward |
| 6. Pre-freeze pilot | `Pilot/prefreeze_pilot.py`, `prefreeze_pilot_v2.py`, `pilot_diagnostic_analysis.md` (2026-09-23, 20 items) | The single highest-value artifact: falsified the metric, found the length mismatch, discovered abstention |
| 7. Production runs | `production_experiment_harness.py` (+`_v3`), `Experiment_Result/experiment_results_analysis.md` (N=500), `statistical_report v2.0/v3.0.md`, `full_experiment_results*.json`, checkpoint CSVs, LaTeX table | Truncation failure at N=500 discovered and diagnosed; budgets raised (80/200/20) in v3; full population N=1,619 executed |
| 8. Post-freeze handover | `Thesis_Topic_Discovery_Handover.md` (2026-09-24) | Declares discovery closed; freezes the topic; begins writing schedule |

## B.3 Verified numbers used in this playbook

| Quantity | Value | Source |
|---|---|---|
| Population | N = 1,619 clean image pairs | `statistical_report v3.0.md`, `Thesis_Topic_Discovery_Handover.md` |
| Arm 2 (neutral placebo) visual following | 89.5% (1,449/1,619) | same |
| Arm 3 (conflict verbalization) visual following | 25.8% (417/1,619) | same |
| **Net shift** | **+63.7 pp** reduction; OR = 24.57 (95% CI 20.24–29.83); Cohen's h = 1.42; McNemar χ² = 982.40, p ≈ 1.2e-215 | same |
| Arm 1 (direct) source following | **text 85.5% (1,385), image 13.8% (223)** | `Thesis_Topic_Discovery_Handover.md` contingency table |
| Abstention, Arm 3 | 13.7% (221) vs 0.2% Arm 2, 0.0% Arm 1 | same |
| Prefill probe agreement | 41.4% divergence between opposing prefixes; +5.3 pp text alignment one direction | `statistical_report v3.0.md` §4 |
| Pilot metric failure | 85% of direct-arm outputs matched neither precomputed answer | `pilot_diagnostic_analysis.md` Finding 1 |
| Pilot length mismatch | Placebo 61.2 tokens vs direct 3.4 tokens | `pilot_diagnostic_analysis.md` Finding 3 |
| N = 500 truncation | Arm 1 100% at 15-token ceiling; Arms 2/3 90.4%/98.2% at 90 tokens | `experiment_results_analysis.md` §3 |

## B.4 Case studies extracted (phenomenon → literature → alternative → missing control → causal question → experiment)

1. **Metric–construct mismatch.** Exact-match selection did not measure source arbitration because the model computed new answers. *General behavior:* validate the metric against manual inspection before the main run. **[L2]**
2. **Unmatched control discovered late.** The neutral arm differed by ~18× in tokens. *General behavior:* check per-item matching numerically, not nominally. **[L2]**
3. **Prompt framing dominates the headline phenomenon.** Direct arm follows text (85.5%); neutral prompt follows image (89.5%). *General behavior:* always run a baseline under more than one neutral framing before naming a modality preference. **[L2]**
4. **Freeze by calendar.** Pilot on 2026-09-23 ended with "only THEN freeze"; handover on 2026-09-24 locked the topic. *General behavior:* freeze on recorded gate numbers. **[L2]**
5. **Novelty by vocabulary and document volume.** Many canonical restatements; novelty argued in prose. *General behavior:* novelty is a design comparison. **[L2]**
6. **Feasibility evaluated after exploration.** Three fields were parked for asset reasons after large audits. *General behavior:* 48-hour feasibility probe per territory. **[L2]**

## B.5 Limits of this reconstruction

- No commit history, so chronology is inferred; two documents may have been written in the opposite order from that suggested here.
- The conversation history is incomplete; statements about earlier sessions are inferences from artifacts.
- Retrospective summary documents were treated as claims; where a claim conflicted with raw results, the raw results were used.
- The playbook deliberately does not re-litigate which thesis topic was "best." Its purpose is to extract reusable process behavior.
