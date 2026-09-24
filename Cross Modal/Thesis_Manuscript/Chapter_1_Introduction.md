# Chapter 1: Introduction

## 1.1 Background: Vision-Language Models and Multimodal Evidence

Vision-Language Models (VLMs) represent a significant evolution in artificial intelligence, extending the autoregressive sequence-modelling capabilities of large language models into multimodal domains. By integrating visual encoders, cross-modal projectors, and autoregressive language backbones, modern VLMs can jointly interpret visual scenes and textual prompts to perform diverse reasoning tasks, such as visual question answering, document comprehension, and diagrammatic reasoning. A fundamental premise of this multimodal integration is complementary evidence fusion: the model is expected to extract relevant contextual and perceptual features from visual inputs, correlate them with textual instructions, and synthesize both sources into a coherent, accurate response. Crucially, successful multimodal reasoning requires not only feature extraction from individual modalities, but also effective arbitration regarding how the available evidence from each modality should influence the final prediction.

However, multimodal evidence fusion becomes fundamentally problematic when the information streams do not complement one another, but instead provide mutually contradictory premises. While substantial research has addressed visual object recognition, perceptual hallucination, and general visual question answering, a critical and conceptually distinct problem arises when an image and an accompanying textual prompt describe conflicting facts. For instance, in visual-textual reasoning, an image and an accompanying text query may present conflicting numerical premises describing the same underlying scenario. In such settings, the model cannot simultaneously treat both sources as valid ground truth, as doing so leads to inconsistent or mathematically contradictory answers. 

This dilemma necessitates what we formally term **source arbitration**: the observable behavioral process of selecting or following one conflicting information source rather than another, or abstaining when the conflict precludes a definitive conclusion. Importantly, we define source arbitration as an operational, observable behavioral outcome—measured by the alignment between the model's generated response and the competing input sources—rather than as a claim regarding an unobserved internal cognitive mechanism.

---

## 1.2 The Source-Arbitration Problem

Recent empirical literature demonstrates that a model's reliance on visual versus textual information is neither uniform nor static. Rather, multimodal reliance varies dynamically across tasks, architectures, and input quality. A foundational anchor in this area is the study by Ghosh et al. (2026), entitled *"Which Source Wins? Task-Dependent Reliance in Vision-Language Models."* Investigating multimodal competition constructed from arithmetic reasoning benchmarks (GSM8K and SVAMP), Ghosh et al. systematically degraded either the visual or textual modality through noise, downsampling, or typographical perturbations. Their findings established that VLMs exhibit task-dependent and modality-dependent reliance patterns, dynamically shifting preference when one information channel is rendered noisy or illegible.

```
+----------------------------------------------------------------------------------------------------+
|                                    CONCEPTUAL COMPARISON MATRIX                                    |
+------------------------------------+--------------------------------+------------------------------+
| Dimension                          | Prior Degradation Studies      | This Thesis                  |
|                                    | (e.g., Ghosh et al., 2026)     |                              |
+------------------------------------+--------------------------------+------------------------------+
| Core Investigation                 | Modality reliance shifts under | Source arbitration under     |
|                                    | perceptual degradation         | clean, legible contradiction |
| Perceptual Quality                 | Asymmetric degradation         | Symmetrically clean &        |
|                                    | (blur, noise, corruption)      | fully legible (Level 0)      |
| Causal Intervention                | Physical signal corruption     | Prompt-based conflict        |
|                                    |                                | verbalization intervention   |
| Primary Evaluated Outcome          | Reliance under degradation     | Observable source selection  |
|                                    |                                | and abstention behavior      |
+------------------------------------+--------------------------------+------------------------------+
```

While Ghosh et al. (2026) provide critical evidence that multimodal reliance can be modulated by external degradation, their work focuses primarily on physical legibility: a model defaults away from an image because the visual features have been corrupted. This leaves an essential scientific question unaddressed: *what happens when both modalities remain pristine, clean, and fully legible, yet assert mutually contradictory information?* Under clean conditions, modality selection cannot be attributed to perceptual noise. Instead, it reflects the model's intrinsic modality biases and its response to prompt instructions. This thesis isolates this scenario, investigating whether an explicit prompt intervention alters observable source arbitration when both sources are fully legible.

---

## 1.3 Cross-Modal Contradiction

Cross-modal contradiction constitutes a distinct failure mode in multimodal reasoning. In standard multimodal benchmarks, visual and textual tokens are assumed to represent a unified state of affairs. When this assumption is violated, the model faces semantic incompatibility.

The challenges of multimodal contradiction detection were formalized by Popordanoska, Li, and Blaschko (2025) in their benchmark study, *"CLASH: A Benchmark for Cross-Modal Contradiction Detection."* The authors demonstrated that modern VLMs struggle to reliably identify explicit contradictions between images and accompanying captions, frequently overlooking factual discrepancies and exhibiting unprompted hallucinations or misplaced confidence. The CLASH benchmark firmly established cross-modal contradiction detection as an open capability limitation across contemporary architectures.

Building upon this foundation, a crucial conceptual distinction must be made: **detecting that two sources contradict each other is not equivalent to determining what the model subsequently does with that contradiction.** While benchmarks such as CLASH focus on evaluating whether a model can output a binary contradiction classification, they do not examine how the explicit identification of a contradiction influences downstream task solving. There remains a wide gap between contradiction detection as an isolated classification task and source arbitration as an active decision process.

---

## 1.4 From Contradiction Detection to Source Arbitration

To understand the lifecycle of multimodal conflict resolution, the decision process must be broken down into discrete sequential stages:

```
               THE MULTIMODAL CONFLICT ARBITRATION PIPELINE
               
   [ Dual Inputs ]         Rendered Visual Image (Source A)
                                           +
                           Textual Problem Query (Source B)
                                           │
                                           ▼
   [ Evidence Status ]     Sources assert contradictory premises
                                           │
                                           ▼
   [ Prompt Condition ]    Explicit Verbalization Intervention
                           (Identify agreement/conflict & assess reliability)
                                           │
                                           ▼
   [ Model Response ]      Downstream Computational Execution
                                           │
                           ┌───────────────┼───────────────┐
                           ▼               ▼               ▼
                      Follow Image    Follow Text      Abstain
```

Existing benchmarks primarily study whether a model can recognize the contradiction stage. The central focus of this thesis is situated at the transition between the final two stages: **does the act of explicitly verbalizing the contradiction alter the model's subsequent observable source-selection and problem-solving behavior?** 

By examining whether explicit verbalization changes downstream source execution—causing the model to adhere to the visual problem, switch to the textual problem, or abstain—this thesis directly interrogates how prompting strategies modulate multimodal decision arbitration.

---

## 1.5 Reasoning Traces and Faithfulness

Because the intervention investigated in this thesis requires the model to articulate a two-sentence verbal evaluation before providing a final answer, the study intersects with the literature on Chain-of-Thought (CoT) prompting and reasoning faithfulness.

In autoregressive language models, eliciting intermediate reasoning tokens prior to the final answer frequently improves task accuracy. However, whether generated rationales actively steer downstream decisions or merely rationalize predetermined outputs remains an active debate. Lanham et al. (2023), in *"Measuring Faithfulness in Chain-of-Thought Reasoning,"* introduced systematic intervention techniques—such as rationale truncation, corruption, and filler injection—to measure how strongly model predictions condition on their stated reasoning traces. Their work demonstrated substantial variance across tasks and models, establishing that generated reasoning tokens are not guaranteed to be causally binding on model predictions.

Furthermore, Turpin et al. (NeurIPS 2023), in *"Language Models Don't Always Say What They Think: Unfaithful Explanations in Chain-of-Thought Prompting,"* demonstrated that models can produce highly plausible CoT explanations that systematically misrepresent the actual features influencing their outputs (such as user bias or answer ordering). Their findings provide an essential methodological warning: **a model's generated verbal explanation cannot be uncritically interpreted as a transparent, faithful report of its internal reasoning mechanisms.**

This methodological caution directly shapes the epistemic posture of this thesis. We do not treat generated verbalizations as windows into internal computational circuits or attention heads. Instead, we treat the verbalization prompt strictly as an **experimental behavioral intervention**, measuring its observable causal effect on downstream problem-solving execution and exact-match performance.

---

## 1.6 Research Gap

Bringing these distinct literature streams together reveals a well-defined and unaddressed research gap:

1. **Modality Reliance:** Prior work demonstrates that multimodal reliance varies across tasks and legibility levels (Ghosh et al., 2026), but focuses on physical image degradation rather than clean, legible contradiction.
2. **Contradiction Detection:** Cross-modal contradiction benchmarks establish that detecting discrepancies is difficult (Popordanoska et al., 2025), but do not measure how explicit verbalization influences downstream source selection.
3. **Reasoning Faithfulness:** Natural language explanations can either steer predictions or serve as unfaithful post-hoc rationalizations (Lanham et al., 2023; Turpin et al., 2023), emphasizing the necessity of testing behavioral outcomes with rigorous controls.

### The Precise Gap
What remains insufficiently characterized in the multimodal literature is:
> **Whether explicitly verbalizing a visual-textual contradiction causes a measurable change in which source a vision-language model subsequently arbitrates and executes, when evaluated against a neutral verbalization control on the exact same conflict items.**

### The Methodological Requirement of a Neutral Control
Demonstrating an effect requires controlling for test-time computation and prompt structure. If an intervention simply instructs a model to verbalize conflict and an arbitration shift is observed, that shift could theoretically stem from:
* The computational headroom of generating additional tokens before answering;
* The syntactic preamble structure of the prompt;
* General instruction following; or
* The specific semantic evaluation of contradiction and source reliability.

To isolate the intervention, a simple before-and-after comparison is insufficient. An adequate experimental framework requires a **neutral verbalization control (placebo)** that prompts the model to generate a descriptive preamble of equivalent length without evaluative contradiction phrasing. Comparing the conflict intervention directly against this neutral control on identical items enables a controlled measurement of intervention-induced source arbitration.

---

## 1.7 Research Problem Statement

When presented with contradictory visual and textual inputs, a vision-language model must produce a final response despite conflicting premises. While prior research has documented modality bias, reliance under perceptual degradation, and isolated contradiction classification, the behavioral effect of explicitly verbalizing such contradictions on subsequent source arbitration remains uncharacterized. 

**This thesis investigates whether an explicit conflict-verbalization prompt intervention causally changes observable source arbitration and problem-solving execution in a vision-language model, compared with a neutral verbalization control on clean multimodal conflict items.**

---

## 1.8 Research Questions

To investigate this problem, the thesis formulates one primary research question and five secondary research questions:

### Primary Research Question
* **RQ1 (Primary):** When a vision-language model receives contradictory visual and textual problems, does an explicit conflict-verbalization intervention causally change its subsequent source arbitration compared with a neutral verbalization control?

### Secondary Research Questions
* **RQ2 (Arbitration Magnitude):** How much does conflict verbalization change the probability that the model follows the visual source rather than the textual source?
* **RQ3 (Source-Execution Validity):** Does the change in source selection correspond to execution of the selected source's ground-truth answer, rather than merely a change in categorical source labels?
* **RQ4 (Contradiction-Conditioned Abstention):** Does explicit conflict verbalization increase abstention when the two information sources provide contradictory premises?
* **RQ5 (Within-Item Behavioral Transitions):** How do individual items transition between source-following, abstention, and ambiguous states when moving from the neutral control to the conflict-verbalization condition?
* **RQ6 (Intervention Resistance & Exploratory Prefilling):** Which cases remain resistant to conflict-verbalization intervention, and how does direct rationale prefilling compare with the full conflict-verbalization intervention?

---

## 1.9 Research Hypotheses

The experimental framework tests the following hypotheses, formulated prior to results analysis:

### Primary Hypothesis
* **Null Hypothesis ($H_0$):** Conflict verbalization produces no change in visual-source capture relative to the neutral verbalization control.
  $$H_0: P(\text{Visual}\mid A_2) = P(\text{Visual}\mid A_3) \quad \iff \quad \Delta_{\text{visual}} = 0$$
* **Alternative Hypothesis ($H_1$):** Conflict verbalization produces a statistically significant change in visual-source capture relative to the neutral verbalization control.
  $$H_1: P(\text{Visual}\mid A_2) \neq P(\text{Visual}\mid A_3)$$
  *(Because each conflict item is evaluated under both conditions, $H_1$ is evaluated using a two-sided McNemar's paired test).*

### Secondary Hypotheses
* **Hypothesis 2 ($H_2$ — Source-Execution Consistency):** Conflict verbalization changes exact-match problem-solving performance conditional on the source selected by the model.
* **Hypothesis 3 ($H_3$ — Abstention):** Conflict verbalization increases the frequency of abstention on contradictory multimodal items.
* **Hypothesis 4 ($H_4$ — Transition Dynamics):** Moving from the neutral control to the conflict-verbalization condition produces systematic within-item transitions between source-following states.
* **Hypothesis 5 ($H_5$ — Intervention Resistance):** A non-trivial subset of items remains visually captured despite conflict verbalization, demonstrating behavioral heterogeneity.

---

## 1.10 Research Objectives

### General Objective
To empirically evaluate whether explicit conflict verbalization changes observable source-arbitration behavior in a vision-language model when visual and textual inputs provide contradictory information.

### Specific Objectives
1. **Establish Baseline Grounding:** Measure baseline source-selection behavior under a length-matched neutral verbalization control.
2. **Quantify Causal Arbitration Shift:** Measure the change in visual versus textual source selection induced by explicit conflict verbalization.
3. **Validate Computational Problem Execution:** Evaluate whether source-selection shifts are accompanied by corresponding agreement with ground-truth mathematical answers via exact-match accuracy.
4. **Measure Abstention Behavior:** Quantify the emergence of contradiction-conditioned abstention under explicit conflict verbalization.
5. **Map Within-Item Transitions:** Construct a paired state-transition matrix tracking individual item migration between control and treatment conditions.
6. **Characterize Resistant Cases:** Analyze items that persist in visual capture despite the verbalization intervention.
7. **Conduct Exploratory Prefill Probing:** Compare the behavioral effect of full conflict verbalization against short, prefilled counterfactual rationales.

---

## 1.11 Scope and Boundaries

To ensure scientific rigor and prevent overclaiming, the boundaries of this investigation are explicitly defined:

### 1.11.1 Model Scope
The primary empirical investigation evaluates **Qwen2.5-VL-3B-Instruct**. This model was selected due to its competitive multimodal reasoning capabilities, public open-weights availability, native support for high-resolution visual processing, and execution feasibility within standard 16 GB GPU environments. No claim of cross-model universality is asserted.

### 1.11.2 Dataset Scope
The evaluation population is drawn from `vlm-modality-research/modality-conflict-arbitration-v2`, derived from GSM8K and SVAMP arithmetic benchmarks. The primary census comprises **1,619 clean visual-text conflict pairs** (`channel = image`, `degradation_level = 0`). The images consist of synthetically rendered typographical mathematical word problems rather than natural photographic scenes.

### 1.11.3 Conflict Scope
The conflict domain is strictly restricted to **contradictory visual and textual arithmetic word problems**, where each modality asserts numerically incompatible premises implying distinct integer solutions. The study does not evaluate natural photographic ambiguities, charts, temporal sequences, spatial orientations, or commonsense factual disputes.

### 1.11.4 Intervention Scope
The causal entity under investigation is **the experimentally assigned prompt intervention** (comparing a conflict-and-reliability evaluation prompt against a neutral descriptive prompt). The study evaluates the behavioral response to this prompt; it does not claim to directly manipulate internal reasoning states.

### 1.11.5 Mechanistic Boundary
> **Explicit Methodological Boundary:**  
> This study does not measure neural activations, attention weights, individual attention heads, residual stream trajectories, or internal circuit dynamics. Consequently, observed behavioral changes are not interpreted as proof of internal mechanistic routing or specific neural circuits.

### 1.11.6 Generalization Boundary
All empirical findings must be interpreted strictly within the context of the evaluated architecture, prompt templates, benchmark construction, and rendered arithmetic domain. Generalization to other model families, natural visual scenes, or non-mathematical tasks requires dedicated empirical validation.

---

## 1.12 Significance of the Study

The significance of this research is situated across three distinct levels:

* **Scientific Significance:** The study provides the first controlled, full-population empirical evidence examining whether an explicit verbal intervention alters observable multimodal source arbitration when both sources are pristine and legible. It helps bridge the divide between multimodal contradiction detection and downstream decision execution.
* **Methodological Significance:** By combining a length-matched neutral control, paired within-item evaluations, exact-match ground-truth validation, and state-transition analysis, the experimental protocol demonstrates how multimodal prompting interventions can be tested with causal rigor without relying on subjective LLM-as-a-judge evaluators.
* **Practical Significance:** As vision-language models are increasingly deployed in autonomous pipelines where sensors, documents, and textual inputs may conflict, understanding how prompt structures influence source prioritization and abstention can inform the development of more reliable decision workflows.

---

## 1.13 Contributions

This thesis delivers five specific scientific and methodological contributions:

1. **A Controlled Multimodal Source-Arbitration Protocol:** Design and execution of a paired, placebo-controlled 4-arm experimental protocol to measure source arbitration under cross-modal contradiction, controlling for prompt length and token generation depth.
2. **Empirical Characterization of Intervention-Induced Arbitration:** A complete population census ($N = 1,619$) documenting the magnitude and paired statistical significance of source-selection shifts induced by explicit conflict verbalization in Qwen2.5-VL-3B-Instruct.
3. **Source-Conditioned Exact-Match Validation:** Demonstration that the observed source-selection shift is accompanied by corresponding changes in exact-match agreement with source-specific ground-truth answers, confirming that the intervention redirects actual multi-step problem-solving execution rather than merely altering categorical labels.
4. **Characterization of Contradiction-Conditioned Abstention and Resistance:** Empirical mapping of within-item state transitions, quantifying the emergence of explicit abstention and identifying persistent visual-capture resistance under identical inputs.
5. **Exploratory Analysis of Rationale Prefilling:** An empirical comparison between complete conflict verbalization and forced prefix rationale prefilling, documenting the relative behavioral sensitivity of short prefix steering in multi-step arithmetic tasks.

---

## 1.14 Thesis Organization

The remainder of this thesis is organized as follows:

* **Chapter 2 (Related Work):** Reviews the theoretical foundations of Vision-Language Models, surveys recent empirical findings on modality competition and visual capture, examines benchmarks for cross-modal contradiction detection, and reviews the literature on Chain-of-Thought faithfulness and behavioral prompting interventions.
* **Chapter 3 (Methodology):** Formulates the 4-arm factorial experimental protocol, details the dataset curation and filtering criteria, provides the exact literal prompt specifications, documents the production inference harness and GPU optimizations, defines the dual-track evaluation metrics, and specifies the paired statistical testing framework and truncation sensitivity protocol.
* **Chapter 4 (Results):** Presents the empirical findings across the 1,619 conflict items, detailing the baseline visual capture rate, the statistical magnitude of the arbitration shift, the source-conditioned exact-match cross-over, the $4 \times 4$ state-transition dynamics, the truncation sensitivity audit, and the exploratory rationale prefilling probe.
* **Chapter 5 (Discussion & Conclusion):** Synthesizes the empirical findings, evaluates alternative behavioral explanations, discusses the implications of contradiction-conditioned abstention and resistant cases, transparently outlines experimental limitations, and proposes directions for future mechanistic and cross-architectural multimodal research.

---

## References for Chapter 1

1. **Ghosh, S., Gupta, A., & Wang, Y. (2026).** *Which Source Wins? Task-Dependent Reliance in Vision-Language Models.* arXiv preprint [arXiv:2608.17205](https://arxiv.org/abs/2608.17205).
2. **Popordanoska, T., Li, M., & Blaschko, M. B. (2025).** *CLASH: A Benchmark for Cross-Modal Contradiction Detection.* arXiv preprint [arXiv:2511.19199](https://arxiv.org/abs/2511.19199).
3. **Lanham, T., Chen, A., Radhakrishnan, A., Steiner, B., Denison, C., Hernandez, D., ... & Perez, E. (2023).** *Measuring Faithfulness in Chain-of-Thought Reasoning.* arXiv preprint [arXiv:2307.13702](https://arxiv.org/abs/2307.13702).
4. **Turpin, M., Michael, J., Perez, E., & Bowman, S. R. (2023).** *Language Models Don't Always Say What They Think: Unfaithful Explanations in Chain-of-Thought Prompting.* Advances in Neural Information Processing Systems (NeurIPS 2023), [arXiv:2305.04388](https://arxiv.org/abs/2305.04388).
