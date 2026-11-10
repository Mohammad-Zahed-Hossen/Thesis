# Thesis Narrative & Framing Guide: Transforming Legacy Experiments into Core Assets

> **Document Purpose:** Permanent thesis writing guide for the Principal Researcher (Mohammad Zahed Hossen).  
> **Location:** `Thesis/THESIS_NARRATIVE_AND_FRAMING_GUIDE.md`  
> **Key Function:** How to frame the transition from v1/v3 pilots to the v5 confirmatory study in the final dissertation manuscript.

---

## 1. Executive Framing Strategy: Do Not Hide Past Experiments

In early drafts, students often feel embarrassed by pilot failures or methodological pivots and try to hide them. **In academic research, this is a major strategic mistake.**

Reviewers and defense committees do not expect research to emerge fully formed on Day 1. When an undergraduate student presents:
1. An ambitious initial pilot,
2. An adversarial self-audit that exposed fatal confounds in existing prompt-based evaluation methods,
3. A principled redesign using formal causal inference (prefix-forcing and controlled direct effects),

that student demonstrates **senior-level scientific maturity**. The journey from v1/v3 to v5 is one of the most compelling narratives of the entire thesis.

---

## 2. Chapter-by-Chapter Narrative Map

### Chapter 1: Introduction (The Motivating Dilemma)
- **The Hook:** Vision-Language Models (VLMs) frequently output Chain-of-Thought (CoT) rationales stating judgments about conflicting inputs (e.g., *"The typed text is more reliable than the image"*).
- **The Core Question:** Does stating that reliability verdict causally steer the downstream decision, or is it an unfaithful post-hoc rationalization of an entrenched modality prior?
- **The Motivating Puzzle (The v1/v3 Observation):** Introduce the exploratory pilot where switching between a neutral prompt and a conflict-detection prompt produced a massive **+63.7 percentage point shift** in model decisions.
- **The Scientific Trap:** Explain why this dramatic shift cannot answer the core question: it manipulated the **user instruction**, not the **model's verbalization**.

---

### Chapter 3 / 4: The Methodological Contribution Chapter
*(Dedicated Chapter: "Why Naive Prompt Interventions Fail to Measure Multimodal Faithfulness")*

Frame the v1/v3 experiments as a published **negative critique / diagnostic finding**:

1. **The Hypothesis Tested in Pilots:**  
   Prompting a model to verbalize contradictions will break unimodal dominance and induce deliberative source arbitration.
2. **The Empirical Observation:**  
   Under prompt manipulation, `Qwen2.5-VL-3B` swung heavily toward text (+63.7 pp).
3. **The Critical Re-Analysis (The Four Confounds):**
   - **Instruction Confounding:** Comparing `Arm 2` (Placebo prompt) with `Arm 3` (Conflict prompt) randomized the prompt text $Z$, not the generated verbalization $M$. A model obeying an explicit user order to inspect conflicts is merely showing instruction-following, which says nothing about whether the generated tokens steer downstream reasoning.
   - **Severe Truncation Artifacts:** Re-analysis revealed that 37.6% to 98.1% of pilot outputs hit token length limits, meaning early reports conflated parser truncation with true model behavior (e.g., true refusal was only 2.3%, not 13.65%).
   - **Decoding Hyperparameter Sensitivity:** Small changes in repetition penalty (e.g., 1.0 vs 1.05) artificially shifted placebo image responses from 14.5% to 52.0%.
   - **The "Arbitration" Construct Failure:** On synthetic math benchmarks (GSM8K/SVAMP), both problems are mathematically valid; neither source is objectively "unreliable."
4. **The Takeaway:** Standard prompt-based evaluations in multimodal research are fundamentally incapable of isolating the causal effect of generated text from prompt steering.

---

### Chapter 5: The Rigorous Solution (The v5 Prefix-Forcing Paradigm)

Explain how every defect in the pilots was systematically eliminated in the v5 design:

| Defect in Naive Pilots (v1/v3) | Methodological Repair in v5 |
| :--- | :--- |
| Confounded user instruction | **Hold the prompt 100% frozen**; manipulate only the assistant's opening generated tokens (prefix-forcing). |
| Coarse whole-paragraph swaps | **Minimal-edit counterfactual flips**: swap only the single source noun (*"image"* $\leftrightarrow$ *"text"*) in the model's own sentence. |
| Positional recency bias (~15 pp) | **Counterbalanced evidence ordering**: exactly 50% `[Image][Text]` and 50% `[Text][Image]`. |
| Uncalibrated prompt steerability | **Single-source explicit ceilings** (`explicit_image` / `explicit_text`) to bound the maximum achievable movement. |
| Incompetence noise | **Competency filtering**: evaluate only items where the model solves both sources in isolation. |
| Messy string extraction & truncation | **Direct log-likelihood margin ($\Delta\ell$)** evaluated at the `####` token boundary. |

---

## 3. Recommended Phrasing for Your Defense & Writing

### What to Say:
> *"Our early pilot experiments revealed a critical methodological confound that is widespread in multimodal prompting literature: comparing conflict-prompted generation to direct generation measures the total effect of the instruction, leaving the causal role of the intermediate reasoning trace completely unidentifiable. To overcome this, we formulated 'Does the Verdict Decide?' as a controlled direct effect under prefix-forcing, holding the instruction, ordering, and length strictly invariant."*

### What NOT to Say:
- ❌ *"Our first experiments failed, so we had to abandon them."*
- ❌ *"We downgraded our idea from arbitration to prefix-forcing because arbitration was too hard."*
- ❌ *"Prompting can never test faithfulness in any form."* (Too absolute; state instead that instruction-level contrasts cannot isolate the verbalization pathway).

---

*Keep this reference close when drafting your thesis chapters and creating your final defense slide deck.*
