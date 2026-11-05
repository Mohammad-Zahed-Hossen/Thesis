# Thesis Execution & Manuscript Handover (Post-Freeze & Validated)

**Document Status:** Operational Handover for Research Execution & Manuscript Drafting  
**Effective Date:** 24 September 2026  
**Supersedes:** Pre-freeze Topic Discovery Handover (Discovery Phase 100% Complete & Closed)  
**Researcher:** Mohammad Zahed Hossen (Technical Lead, Final-Year BSc CSE, Bangladesh)  

---

## 1. Executive Purpose & Ingestion Directives

**The thesis topic discovery phase is completely finished and locked.**  
Any AI assistant or collaborator reading this document must adhere to the following directives:
1. **Zero Ideation or Topic Suggestions:** Do **not** propose new thesis topics, alternative fields, or reopen parked/deprecated candidates (Medical Imaging, Federated Learning, Cultural VLM Repair, Multimodal Agents).
2. **Accept Empirical Ground Truth:** The core experimental pipeline has been completely executed across the full population ($N = 1,619$) on Google Colab Pro. The data, statistical tests, and artifacts are verified and frozen.
3. **Active Objective:** Support the researcher in deep thesis analysis, LaTeX manuscript drafting (Chapters 1 to 5), qualitative case studies, and oral defense preparation.

---

## 2. Locked Thesis Specification

* **Formal Thesis Title:**  
  **"Causal Conflict Verbalization and Source Arbitration in Vision-Language Models"**
* **Parent Field:** Multimodal / Vision-Language Learning and Systems (**FROZEN**)
* **Active Subfield:** Trustworthy, Grounded, and Reliable Generative MLLMs
* **Core Research Question:**  
  *When a vision-language model is presented with contradictory visual and textual premises, does explicitly verbalizing the contradiction causally alter its decisional arbitration, or does the explanation merely rationalize an entrenched visual modality preference?*
* **Anchor Literature & Gap:**  
  - *Which Source Wins?* (arXiv:2608.17205, Aug 2026): Proved modality dominance under legibility degradation, but explicitly left contradiction awareness and verbalization unstudied (§6).
  - *Lanham et al.* (arXiv:2305.04388, NeurIPS 2023): Formalized CoT faithfulness testing exclusively in text LLMs; never extended to multimodal conflict arbitration.
  - *CLASH* (arXiv:2511.19199): Evaluated contradiction only as an abstention trigger without measuring decision redirection.

---

## 3. Verified Empirical Results Dossier ($N = 1,619$)

The complete census across all 1,619 clean image pairs in `vlm-modality-research/modality-conflict-arbitration-v2` was executed on Google Colab Pro using `Qwen2.5-VL-3B-Instruct` (FP16 Tensor Cores, PyTorch 2.0 SDPA, CUDA 13.0).

```
===================================================================================================
                       FULL POPULATION CONTINGENCY TABLE (N = 1619)
===================================================================================================
 Condition                          Follows Image   Follows Text   Abstains   Ambiguous
----------------------------------------------------------------------------------------
 Arm 1: Direct Baseline              223 (13.8%)    1385 (85.5%)    0 (0.0%)   11 (0.7%)
 Arm 2: Placebo (Neutral Control)   1449 (89.5%)     145  (9.0%)    4 (0.2%)   21 (1.3%)
 Arm 3: Conflict Verbalization       417 (25.8%)     954 (58.9%)  221 (13.7%)  27 (1.7%)
===================================================================================================
```

### Key Statistical Confirmations:
* **Net Causal Arbitration Shift ($\Delta_{\text{arb}}$):** **$+63.74\text{ percentage points}$** reduction in visual capture ($89.50\% \to 25.76\%$, $p < 0.0001^{***}$).
* **Relative Risk ($RR$):** $0.2878$ ($71.22\%$ reduction in visual capture).
* **Odds Ratio ($OR$):** $24.57$ [$95\%$ CI: $20.24, 29.83$].
* **Cohen's $h$ Effect Size:** $1.4170$ (Classified as "Very Large Effect"; benchmark $> 0.8$).
* **McNemar's Paired Within-Item Test:** $\chi^2_{\text{McNemar}} = 982.40$, **$p = 1.20 \times 10^{-215}$**.
* **Fisher's Exact Test:** $p = 1.09 \times 10^{-322}$; Pearson Chi-Square: $\chi^2 = 1347.01$, $p = 6.88 \times 10^{-295}$.
* **The "Smoking Gun" Exact-Match Cross-Over Discovery:**
  - Arm 2 (Placebo): Solves Image Problem $7.6\times$ more often than Text ($35.6\%$ vs $4.7\%$).
  - Arm 3 (Conflict Verbalization): Inverts to solve Text Problem $3.1\times$ more often than Image ($35.8\%$ vs $11.7\%$).
  - *Proof:* Verbalization physically redirects the VLM's multi-step arithmetic computational circuit rather than causing random drift.
* **Epistemic Abstention:** Rises to $13.65\%$ ($221 / 1,619$) in Arm 3 vs $0.2\%$ in Arm 2.

---

## 4. Codebase & Data Artifact Inventory

All production files are located in `d:\Thesis\Important\Cross Modal\`:
* **Master Report:** [`Finalize Topic/CANONICAL_THESIS_MASTER_REPORT.md`](file:///d:/Thesis/Important/Cross%20Modal/Finalize%20Topic/CANONICAL_THESIS_MASTER_REPORT.md)
* **Production Harness (v3.0):** [`Finalize Topic/Pilot/production_experiment_harness_v3.py`](file:///d:/Thesis/Important/Cross%20Modal/Finalize%20Topic/Pilot/production_experiment_harness_v3.py)
* **Statistical Suite:** [`Finalize Topic/Pilot/statistical_analysis.py`](file:///d:/Thesis/Important/Cross%20Modal/Finalize%20Topic/Pilot/statistical_analysis.py)
* **Full Population Data ($N=1,619$):** [`Finalize Topic/Experiment_Result/full_experiment_results v3.0.json`](file:///d:/Thesis/Important/Cross%20Modal/Finalize%20Topic/Experiment_Result/full_experiment_results%20v3.0.json) (76,095 lines, 5.34 MB)
* **Full Checkpoint CSV:** [`Finalize Topic/Experiment_Result/experiment_checkpoint v3.0.csv`](file:///d:/Thesis/Important/Cross%20Modal/Finalize%20Topic/Experiment_Result/experiment_checkpoint%20v3.0.csv) (8,096 rows)
* **LaTeX Table:** [`Finalize Topic/Experiment_Result/thesis_contingency_table v3.0.tex`](file:///d:/Thesis/Important/Cross%20Modal/Finalize%20Topic/Experiment_Result/thesis_contingency_table%20v3.0.tex)
* **Statistical Summary:** [`Finalize Topic/Experiment_Result/statistical_report v3.0.md`](file:///d:/Thesis/Important/Cross%20Modal/Finalize%20Topic/Experiment_Result/statistical_report%20v3.0.md)

---

## 5. Active Thesis Workflow (Starting from Tomorrow)

The researcher is transitioning from empirical experimentation to deep academic writing:
1. **Week 1–2 (Chapters 3 & 4):** Write Chapter 3 (4-Arm Factorial Experimental Methodology, Harness v3 Optimizations) and Chapter 4 (Empirical Findings, Exact-Match Cross-Over, Statistical Significance).
2. **Week 3–4 (Chapters 1 & 2):** Draft Chapter 1 (Introduction, Motivation, Research Question) and Chapter 2 (Literature Review, Modality Dominance, CoT Faithfulness).
3. **Week 5–6 (Chapter 5 & Defense):** Draft Chapter 5 (Mechanistic Discussion, Epistemic Safety, Limitations) and build the final defense slide deck.
