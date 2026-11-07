
In simple, rigorous scientific terms, here is an explanation of **what** you are trying to do, **why** it matters, and **how** you are executing it in this thesis.

---

### 1. What You Are Actually Trying to Do (The Core Scientific Problem)

When a Vision-Language Model (VLM, such as [`Qwen2.5-VL-3B-Instruct`](file:///d:/Thesis/Important/Causal Conflict Verbalization and Source Arbitration/Experiment/harness_v4.py#L46)) is given an image and a typed text problem that **contradict** each other, it faces a dilemma called **Source Arbitration**:

* *Does it solve the problem shown in the image ($A_{\text{img}}$)?*
* *Or does it solve the problem written in the prompt text ($A_{\text{txt}}$)?*

Under default direct prompting, VLMs often exhibit strong biases (e.g., text bias or visual capture). Prior pilot observations suggested that instructing the model to explicitly detect and describe the conflict ("verbalize the conflict") shifts its final answer arbitration.

#### The Central Research Question:

> **Does explicit conflict verbalization *causally steer* multimodal decision arbitration, or does it merely *rationalize* a prompt-induced visual bias?**

In causal mediation terms:

* **Treatment ($Z$):** The prompt instruction (e.g., direct vs. neutral description vs. conflict verbalization).
* **Mediator ($M$):** The intermediate tokens the model generates (verbalizing that a conflict exists and which source is more reliable).
* **Outcome ($Y$):** The final numerical decision ($Y \in \{A_{\text{img}}, A_{\text{txt}}, \text{other}\}$).

You are testing whether generating the mediator tokens ($M$) **actually drives the downstream computation** to favor a source, or whether the prompt instruction ($Z$) directly alters the attention/latents and the verbal text is just an inert post-hoc byproduct.

---

### 2. Why It Matters (The Research Significance)

1. **Mechanistic Faithfulness vs. Hallucinatory Rationalization:** LLMs and VLMs frequently output chain-of-thought explanations that look convincing but do not reflect the actual computation driving the answer. Proving whether intermediate verbalization is a genuine causal driver or unfaithful rationalization is a fundamental question in AI interpretability.
2. **Robust Multimodal Decision Making:** Real-world VLMs (in robotics, medical imaging, autonomous agents) constantly receive conflicting sensor signals (e.g., an outdated text prompt vs. real-time visual sensor feed). Understanding how arbitration can be steered or controlled is critical for reliable deployment.

---

### 3. How You Are Doing It (The Methodology & Architecture)

Your codebase in [`Experiment/`](file:///d:/Thesis/Important/Causal Conflict Verbalization and Source Arbitration/Experiment/README.md) breaks this down into four rigorous phases:

#### A. Controlled Factorial Stimuli & Baselines

* **Dataset:** [`vlm-modality-research/modality-conflict-arbitration-v2`](file:///d:/Thesis/Important/Causal Conflict Verbalization and Source Arbitration/Experiment/harness_v4.py#L50) and ChartQA conflict benchmarks.
* **Strict Disambiguation:** Pairs where $A_{\text{img}} == A_{\text{txt}}$ are purged, ensuring any arithmetic exact-match uniquely identifies which source the model followed.
* **Baselines:**
  * `base_image` & `base_text`: Verifies whether the model can solve each problem in isolation.
  * `congruent_*`: Verifies false-alarm rates when the image and text actually agree.

#### B. Factorial Prompt Arms ([`harness_v4.py`](file:///d:/Thesis/Important/Causal Conflict Verbalization and Source Arbitration/Experiment/harness_v4.py#L104-L140))

To rule out confounding variables (like output length or word order), you define targeted comparison arms:

1. **`direct`:** Direct instruction to solve the problem (baseline bias).
2. **`filler`:** Generates generic math tips of equal length without mentioning the sources (isolates whether token delay/CoT length alone shifts arbitration).
3. **`desc_image_first` & `desc_text_first`:** Neutral summaries of both sources without conflict evaluation (controls for mentioning both sources and order-of-presentation bias).
4. **`detect_only`:** State *only* if they agree or disagree (separates conflict detection from reliability assignment).
5. **`reliability_only`:** State *only* which source is more reliable.
6. **`conflict_full`:** Full verbalization: detect conflict **and** assess source reliability.

#### C. The Causal Test: Mediator Transplant ([`transplant_v4.py`](file:///d:/Thesis/Important/Causal Conflict Verbalization and Source Arbitration/Experiment/transplant_v4.py))

To mathematically distinguish the prompt effect ($Z \to Y$) from the verbalization effect ($M \to Y$), you perform a **mediator transplant via forced prefilling**:

* You cross the instruction $Z$ with the verbalization $M$:
  * **$z_0 / m_1$:** Give the model a *neutral* prompt instruction, but **prefill** its generated prefix with a *conflict verbalization*.
  * **$z_1 / m_0$:** Give the model a *conflict* prompt instruction, but **prefill** its prefix with a *neutral description*.
* **Authored Prefills:** You also prefill fixed synthetic claims ("Image is more reliable" vs. "Text is more reliable") to test whether the stated source direction causally forces the final calculation.

If the final answer flips when you swap the prefilled mediator text $M$ under a fixed instruction $Z$, you have direct causal proof that verbalization steers arbitration.

#### D. Measurement & Evaluation Pipeline

* **Outcome Metric:** Primary outcome is **exact-match arithmetic** against $A_{\text{img}}$ vs. $A_{\text{txt}}$ via [`score_v4.py`](file:///d:/Thesis/Important/Causal Conflict Verbalization and Source Arbitration/Experiment/score_v4.py).
* **Confounder Control:** Explicitly pinning the repetition penalty to `1.0` (avoiding the default `1.05` penalty which penalized the input text prompt tokens and artificially induced visual bias).
* **Split Discipline:** Strict separation between tuning data (`dev`) and confirmatory production runs (`confirm`).

---

### Summary Snapshot


| Dimension               | Thesis Strategy                                                                                                      |
| :------------------------ | :--------------------------------------------------------------------------------------------------------------------- |
| **Target Phenomenon**   | How a VLM chooses between conflicting image vs. text information (**Source Arbitration**).                           |
| **Core Question**       | Is verbalizing the conflict a **causal mechanism** that shifts decisions, or just **post-hoc rationalization**?      |
| **Intervention Method** | **Factorial prompt harness** + **Mediator prefill transplant** (crossing instruction $Z$ and intermediate text $M$). |
| **Ground-Truth Metric** | Exact-match numerical answer equality to $A_{\text{img}}$ vs. $A_{\text{txt}}$.                                      |
| **Target Platform**     | Inference runs on Colab GPU (`Qwen2.5-VL-3B-Instruct`), statistical analysis and dev checks locally.                 |


### Architecture Overview

```
┌────────────────────────────────────────────────────────────────────────┐
│                        COLAB PRO (NVIDIA GPU)                          │
│                                                                        │
│  [Dataset Pins & Model Pins]                                           │
│            │                                                           │
│            ▼                                                           │
│  ┌──────────────────────┐             ┌─────────────────────────────┐  │
│  │    harness_v4.py     │             │      transplant_v4.py       │  │
│  │ (15 Generation Arms) │─(Donor M)──>│ (Prefill Crossed Z & M)     │  │
│  └──────────┬───────────┘             └──────────────┬──────────────┘  │
│             │                                        │                 │
│             ▼                                        ▼                 │
│      *.manifest.json                          *.manifest.json          │
│       *.jsonl rows                             *.jsonl rows            │
└─────────────┼────────────────────────────────────────┼─────────────────┘
              │ Git / Cloud Download                   │
              ▼                                        ▼
┌────────────────────────────────────────────────────────────────────────┐
│                        LOCAL HOST (Ryzen 5)                            │
│                                                                        │
│  ┌───────────────────┐    ┌────────────────────┐    ┌───────────────┐  │
│  │    score_v4.py    │───>│   analyze_v4.py    │───>│  coding_v3/   │  │
│  │ (Deterministic    │    │ (Gates, Contrasts, │    │ (Human Blind  │  │
│  │  Arithmetic Match)│    │  McNemar & Holm)   │    │  Validation)  │  │
│  └───────────────────┘    └────────────────────┘    └───────────────┘  │
└────────────────────────────────────────────────────────────────────────┘
```

---

### 1. Hardware & Execution Pipeline

The experiment operates under a strict physical and computational separation:

* **Inference Engine (Colab Pro, 16 GB VRAM GPU):**

  * Model: [`Qwen/Qwen2.5-VL-3B-Instruct`](file:///d:/Thesis/Important/Causal Conflict Verbalization and Source Arbitration/Experiment/harness_v4.py#L46) pinned to commit `66285546...`.
  * Deterministic Inference: Greedily sampled (`do_sample=False`, temperature $0$).
  * **Confounder Fix (Repetition Penalty):** In v3, Qwen's default repetition penalty of `1.05` was active. Because the typed question is tokenized into `input_ids` while visual features are not, a $>1.0$ penalty penalizes tokens present in the prompt text, inadvertently creating an artificial bias toward the image. In v4, repetition penalty is strictly locked to `1.00`.
  * Outputs are written row-by-row to append-only JSONL files (`results_v4/*.jsonl`) along with an exact environment manifest (`*.manifest.json`).
* **Evaluation Engine (Local CPU):**

  * No model weights are loaded locally.
  * Local scripts run unit tests ([`tests/test_v4.py`](file:///d:/Thesis/Important/Causal Conflict Verbalization and Source Arbitration/Experiment/tests/test_v4.py)), parsing, deterministic arithmetic scoring ([`score_v4.py`](file:///d:/Thesis/Important/Causal Conflict Verbalization and Source Arbitration/Experiment/score_v4.py)), and statistical hypothesis testing ([`analyze_v4.py`](file:///d:/Thesis/Important/Causal Conflict Verbalization and Source Arbitration/Experiment/analyze_v4.py)).

---

### 2. Stimulus Engineering: Disambiguating the Modalities

To measure source arbitration without ambiguity:

1. **Benchmark Datasets:** [`vlm-modality-research/modality-conflict-arbitration-v2`](file:///d:/Thesis/Important/Causal Conflict Verbalization and Source Arbitration/Experiment/harness_v4.py#L50) and ChartQA conflict sets.
2. **Exclusion of Equal Answers ($A_{\text{img}} == A_{\text{txt}}$):** If an image and text problem both resolve to the same number (e.g., both yield `42`), that item cannot reveal which source the model followed. v4 purges all such instances so that every arithmetic match uniquely identifies the selected modality.
3. **Disentangled Splits:**
   * **`dev` split:** Used strictly for fixing pipeline bugs, testing prompt formatting, and validating quality gates.
   * **`confirm` split:** Frozen, unseen items reserved exclusively for the pre-registered confirmatory run.

---

### 3. Factorial Prompt Matrix ([`harness_v4.py`](file:///d:/Thesis/Important/Causal Conflict Verbalization and Source Arbitration/Experiment/harness_v4.py#L74-L140))

Prior studies simply compared a "Direct" prompt to a "Conflict Verbalization" prompt. However, that conflates multiple factors at once: token delay, mentioning both sources, and ordering effects.

v4 isolates each variable using an orthogonal prompt design:


| Prompt Arm                     | What it Instructs the Model to Output                                                                  | Confounder Isolated / Purpose                                                                                                                 |
| :------------------------------- | :------------------------------------------------------------------------------------------------------- | :---------------------------------------------------------------------------------------------------------------------------------------------- |
| **`direct`**                   | "Solve the problem."                                                                                   | Baseline arbitration rate.                                                                                                                    |
| **`filler`**                   | "Give general advice on avoiding calculation mistakes... Then solve the problem."                      | **Token-length / Computation delay:** Tests if merely generating intermediate reasoning tokens shifts arbitration without mentioning sources. |
| **`desc_image_first`**         | "Neutrally describe what the image shows and then what the typed text says... without comparing them." | **Placebo / Neutral CoT:** Measures the effect of processing both modalities explicitly without judging conflict.                             |
| **`desc_text_first`**          | "Neutrally describe what the typed text says and then what the image shows... without comparing them." | **Order of presentation bias:** Tests whether the model favors whichever source it talks about first or last.                                 |
| **`detect_only`**              | "State whether the image and the typed text agree or contradict each other."                           | **Detection vs. Decision:** Tests whether noticing contradiction alone alters the downstream calculation.                                     |
| **`reliability_only`**         | "Explain which source... you consider more reliable."                                                  | **Judgment without detection:** Isolates the effect of assigning trust.                                                                       |
| **`conflict_full`**            | Both state if they contradict **and** explain which source is more reliable.                           | Full combined intervention.                                                                                                                   |
| **`base_image` / `base_text`** | Isolated single-source prompts ($I$-only or $T$-only).                                                 | **Single-source competency:** Proves the model can actually solve each problem alone.                                                         |
| **`congruent_*`**              | Same image and text problem without conflict.                                                          | **False-alarm rate:** Checks if conflict prompts cause the model to hallucinate contradictions when inputs agree.                             |

---

### 4. The Causal Heart: Mediator Transplant ([`transplant_v4.py`](file:///d:/Thesis/Important/Causal Conflict Verbalization and Source Arbitration/Experiment/transplant_v4.py))

Observing that a prompt $Z$ changes output $Y$ does **not** prove that the intermediate explanation $M$ caused the change. The prompt instruction $Z$ might directly alter early attention heads or latent vectors, rendering the written text $M$ an epiphenomenon.

To prove the intermediate text $M$ is causally efficacious, you perform **Mediator Prefill Transplants**:

```
Prompt Instruction (Z) ──────┐
                             ├──> Model Input ──> Model generates remaining solve tokens (Y)
Prefilled Verbalization (M) ─┘
```

#### The Crossed Conditions:

* **$z_0$:** Neutral instruction (`desc_image_first`)
* **$z_1$:** Conflict instruction (`conflict_full`)
* **$m_0$:** Model's generated verbalization from $z_0$ for that exact item
* **$m_1$:** Model's generated verbalization from $z_1$ for that exact item

1. **Fidelity Controls ($z_0 / m_0$ and $z_1 / m_1$):**
   * Feed the original instruction with its own generated prefix. The final calculation must reproduce the free-generation outcome; this verifies that prefilling does not disrupt model mechanics.
2. **Causal Crosses ($z_0 / m_1$ and $z_1 / m_0$):**
   * **$z_0 / m_1$ (Neutral Prompt + Conflict Text):** The model was told to describe neutrally, but the text it has "already typed" states: *"The image and text contradict, and the image is more reliable."* Does the model switch to solving the image?
   * **$z_1 / m_0$ (Conflict Prompt + Neutral Text):** The model was told to verbalize conflict, but its prefix is neutral. Does the visual shift vanish?
3. **Synthetic / Directional Interventions:**
   * **`rel_image` vs. `rel_text`:** Fixed synthetic sentences are injected: *"I consider the image more reliable"* vs. *"I consider the typed text more reliable"*. If the output follows the forced sentence, the verbal claim is directly steerable.
   * **`eq_a` vs. `eq_b`:** Two differently worded sentences asserting the exact same conflict meaning, measuring surface-token sensitivity vs. semantic impact.

---

### 5. Scoring & Deterministic Metrics ([`score_v4.py`](file:///d:/Thesis/Important/Causal Conflict Verbalization and Source Arbitration/Experiment/score_v4.py))

Instead of relying on LLM-as-a-judge (which introduces circular bias), the evaluation is deterministic:

* **Answer Extraction:** Looks for `#### <answer>` on the final lines. Fallback logic extracts trailing numeric tokens and tracks extraction method (`hash_direct`, `hash_tail`, `fallback_last_number`).
* **Exact Decimal Matching:** Uses `Decimal` comparison (e.g., `18.00` correctly matches `18`).
* **Classification:**
  * $\text{Match } A_{\text{img}}$: Model resolved conflict in favor of visual source.
  * $\text{Match } A_{\text{txt}}$: Model resolved conflict in favor of text source.
  * $\text{Other / Refusal / Malformed}$: Logged for failure-rate accounting.

---

### 6. Statistical Analysis & Dev Quality Gates ([`analyze_v4.py`](file:///d:/Thesis/Important/Causal Conflict Verbalization and Source Arbitration/Experiment/analyze_v4.py))

Before running confirmatory tests, the dataset must pass automated **Dev Quality Gates**:

* **Token Cap Gate:** Max token cap cutoff rate must be $< 5\%$ (`MAX_CAP_RATE = 0.05`).
* **Answer Extraction Gate:** At least $90\%$ of rows must yield clean numeric answers (`MIN_ANSWER_RATE = 0.90`).
* **Competency Gate:** `base_image` and `base_text` must show high baseline task-solving accuracy.
* **Transplant Fidelity Gate:** $z_0 / m_0$ must match the free-generation donor outputs within a tight tolerance.

Once gates pass, hypotheses are tested using:

* **Exact McNemar Tests:** Paired non-parametric test comparing binary success/arbitration switches on the same items across paired arms.
* **Holm-Bonferroni Correction:** Adjusts family-wise error rate across all planned behavioral contrasts (`BEHAVIOUR_CONTRASTS`) and transplant contrasts (`TRANSPLANT_CONTRASTS`).

Analyzed score_v4.py:L1-60
Analyzed analyze_v4.py:L1-60

Here is a detailed, component-by-component elaboration of **how** the methodology and experimental architecture work in the codebase.

---

### Architecture Overview

```
┌────────────────────────────────────────────────────────────────────────┐
│                        COLAB PRO (NVIDIA GPU)                          │
│                                                                        │
│  [Dataset Pins & Model Pins]                                           │
│            │                                                           │
│            ▼                                                           │
│  ┌──────────────────────┐             ┌─────────────────────────────┐  │
│  │    harness_v4.py     │             │      transplant_v4.py       │  │
│  │ (15 Generation Arms) │─(Donor M)──>│ (Prefill Crossed Z & M)     │  │
│  └──────────┬───────────┘             └──────────────┬──────────────┘  │
│             │                                        │                 │
│             ▼                                        ▼                 │
│      *.manifest.json                          *.manifest.json          │
│       *.jsonl rows                             *.jsonl rows            │
└─────────────┼────────────────────────────────────────┼─────────────────┘
              │ Git / Cloud Download                   │
              ▼                                        ▼
┌────────────────────────────────────────────────────────────────────────┐
│                        LOCAL HOST (Ryzen 5)                            │
│                                                                        │
│  ┌───────────────────┐    ┌────────────────────┐    ┌───────────────┐  │
│  │    score_v4.py    │───>│   analyze_v4.py    │───>│  coding_v3/   │  │
│  │ (Deterministic    │    │ (Gates, Contrasts, │    │ (Human Blind  │  │
│  │  Arithmetic Match)│    │  McNemar & Holm)   │    │  Validation)  │  │
│  └───────────────────┘    └────────────────────┘    └───────────────┘  │
└────────────────────────────────────────────────────────────────────────┘
```

---

### 1. Hardware & Execution Pipeline

The experiment operates under a strict physical and computational separation:

* **Inference Engine (Colab Pro, 16 GB VRAM GPU):**

  * Model: [`Qwen/Qwen2.5-VL-3B-Instruct`](file:///d:/Thesis/Important/Causal Conflict Verbalization and Source Arbitration/Experiment/harness_v4.py#L46) pinned to commit `66285546...`.
  * Deterministic Inference: Greedily sampled (`do_sample=False`, temperature $0$).
  * **Confounder Fix (Repetition Penalty):** In v3, Qwen's default repetition penalty of `1.05` was active. Because the typed question is tokenized into `input_ids` while visual features are not, a $>1.0$ penalty penalizes tokens present in the prompt text, inadvertently creating an artificial bias toward the image. In v4, repetition penalty is strictly locked to `1.00`.
  * Outputs are written row-by-row to append-only JSONL files (`results_v4/*.jsonl`) along with an exact environment manifest (`*.manifest.json`).
* **Evaluation Engine (Local CPU):**

  * No model weights are loaded locally.
  * Local scripts run unit tests ([`tests/test_v4.py`](file:///d:/Thesis/Important/Causal Conflict Verbalization and Source Arbitration/Experiment/tests/test_v4.py)), parsing, deterministic arithmetic scoring ([`score_v4.py`](file:///d:/Thesis/Important/Causal Conflict Verbalization and Source Arbitration/Experiment/score_v4.py)), and statistical hypothesis testing ([`analyze_v4.py`](file:///d:/Thesis/Important/Causal Conflict Verbalization and Source Arbitration/Experiment/analyze_v4.py)).

---

### 2. Stimulus Engineering: Disambiguating the Modalities

To measure source arbitration without ambiguity:

1. **Benchmark Datasets:** [`vlm-modality-research/modality-conflict-arbitration-v2`](file:///d:/Thesis/Important/Causal Conflict Verbalization and Source Arbitration/Experiment/harness_v4.py#L50) and ChartQA conflict sets.
2. **Exclusion of Equal Answers ($A_{\text{img}} == A_{\text{txt}}$):** If an image and text problem both resolve to the same number (e.g., both yield `42`), that item cannot reveal which source the model followed. v4 purges all such instances so that every arithmetic match uniquely identifies the selected modality.
3. **Disentangled Splits:**
   * **`dev` split:** Used strictly for fixing pipeline bugs, testing prompt formatting, and validating quality gates.
   * **`confirm` split:** Frozen, unseen items reserved exclusively for the pre-registered confirmatory run.

---

### 3. Factorial Prompt Matrix ([`harness_v4.py`](file:///d:/Thesis/Important/Causal Conflict Verbalization and Source Arbitration/Experiment/harness_v4.py#L74-L140))

Prior studies simply compared a "Direct" prompt to a "Conflict Verbalization" prompt. However, that conflates multiple factors at once: token delay, mentioning both sources, and ordering effects.

v4 isolates each variable using an orthogonal prompt design:


| Prompt Arm                     | What it Instructs the Model to Output                                                                  | Confounder Isolated / Purpose                                                                                                                 |
| :------------------------------- | :------------------------------------------------------------------------------------------------------- | :---------------------------------------------------------------------------------------------------------------------------------------------- |
| **`direct`**                   | "Solve the problem."                                                                                   | Baseline arbitration rate.                                                                                                                    |
| **`filler`**                   | "Give general advice on avoiding calculation mistakes... Then solve the problem."                      | **Token-length / Computation delay:** Tests if merely generating intermediate reasoning tokens shifts arbitration without mentioning sources. |
| **`desc_image_first`**         | "Neutrally describe what the image shows and then what the typed text says... without comparing them." | **Placebo / Neutral CoT:** Measures the effect of processing both modalities explicitly without judging conflict.                             |
| **`desc_text_first`**          | "Neutrally describe what the typed text says and then what the image shows... without comparing them." | **Order of presentation bias:** Tests whether the model favors whichever source it talks about first or last.                                 |
| **`detect_only`**              | "State whether the image and the typed text agree or contradict each other."                           | **Detection vs. Decision:** Tests whether noticing contradiction alone alters the downstream calculation.                                     |
| **`reliability_only`**         | "Explain which source... you consider more reliable."                                                  | **Judgment without detection:** Isolates the effect of assigning trust.                                                                       |
| **`conflict_full`**            | Both state if they contradict **and** explain which source is more reliable.                           | Full combined intervention.                                                                                                                   |
| **`base_image` / `base_text`** | Isolated single-source prompts ($I$-only or $T$-only).                                                 | **Single-source competency:** Proves the model can actually solve each problem alone.                                                         |
| **`congruent_*`**              | Same image and text problem without conflict.                                                          | **False-alarm rate:** Checks if conflict prompts cause the model to hallucinate contradictions when inputs agree.                             |

---

### 4. The Causal Heart: Mediator Transplant ([`transplant_v4.py`](file:///d:/Thesis/Important/Causal Conflict Verbalization and Source Arbitration/Experiment/transplant_v4.py))

Observing that a prompt $Z$ changes output $Y$ does **not** prove that the intermediate explanation $M$ caused the change. The prompt instruction $Z$ might directly alter early attention heads or latent vectors, rendering the written text $M$ an epiphenomenon.

To prove the intermediate text $M$ is causally efficacious, you perform **Mediator Prefill Transplants**:

```
Prompt Instruction (Z) ──────┐
                             ├──> Model Input ──> Model generates remaining solve tokens (Y)
Prefilled Verbalization (M) ─┘
```

#### The Crossed Conditions:

* **$z_0$:** Neutral instruction (`desc_image_first`)
* **$z_1$:** Conflict instruction (`conflict_full`)
* **$m_0$:** Model's generated verbalization from $z_0$ for that exact item
* **$m_1$:** Model's generated verbalization from $z_1$ for that exact item

1. **Fidelity Controls ($z_0 / m_0$ and $z_1 / m_1$):**
   * Feed the original instruction with its own generated prefix. The final calculation must reproduce the free-generation outcome; this verifies that prefilling does not disrupt model mechanics.
2. **Causal Crosses ($z_0 / m_1$ and $z_1 / m_0$):**
   * **$z_0 / m_1$ (Neutral Prompt + Conflict Text):** The model was told to describe neutrally, but the text it has "already typed" states: *"The image and text contradict, and the image is more reliable."* Does the model switch to solving the image?
   * **$z_1 / m_0$ (Conflict Prompt + Neutral Text):** The model was told to verbalize conflict, but its prefix is neutral. Does the visual shift vanish?
3. **Synthetic / Directional Interventions:**
   * **`rel_image` vs. `rel_text`:** Fixed synthetic sentences are injected: *"I consider the image more reliable"* vs. *"I consider the typed text more reliable"*. If the output follows the forced sentence, the verbal claim is directly steerable.
   * **`eq_a` vs. `eq_b`:** Two differently worded sentences asserting the exact same conflict meaning, measuring surface-token sensitivity vs. semantic impact.

---

### 5. Scoring & Deterministic Metrics ([`score_v4.py`](file:///d:/Thesis/Important/Causal Conflict Verbalization and Source Arbitration/Experiment/score_v4.py))

Instead of relying on LLM-as-a-judge (which introduces circular bias), the evaluation is deterministic:

* **Answer Extraction:** Looks for `#### <answer>` on the final lines. Fallback logic extracts trailing numeric tokens and tracks extraction method (`hash_direct`, `hash_tail`, `fallback_last_number`).
* **Exact Decimal Matching:** Uses `Decimal` comparison (e.g., `18.00` correctly matches `18`).
* **Classification:**
  * $\text{Match } A_{\text{img}}$: Model resolved conflict in favor of visual source.
  * $\text{Match } A_{\text{txt}}$: Model resolved conflict in favor of text source.
  * $\text{Other / Refusal / Malformed}$: Logged for failure-rate accounting.

---

### 6. Statistical Analysis & Dev Quality Gates ([`analyze_v4.py`](file:///d:/Thesis/Important/Causal Conflict Verbalization and Source Arbitration/Experiment/analyze_v4.py))

Before running confirmatory tests, the dataset must pass automated **Dev Quality Gates**:

* **Token Cap Gate:** Max token cap cutoff rate must be $< 5\%$ (`MAX_CAP_RATE = 0.05`).
* **Answer Extraction Gate:** At least $90\%$ of rows must yield clean numeric answers (`MIN_ANSWER_RATE = 0.90`).
* **Competency Gate:** `base_image` and `base_text` must show high baseline task-solving accuracy.
* **Transplant Fidelity Gate:** $z_0 / m_0$ must match the free-generation donor outputs within a tight tolerance.

Once gates pass, hypotheses are tested using:

* **Exact McNemar Tests:** Paired non-parametric test comparing binary success/arbitration switches on the same items across paired arms.
* **Holm-Bonferroni Correction:** Adjusts family-wise error rate across all planned behavioral contrasts (`BEHAVIOUR_CONTRASTS`) and transplant contrasts (`TRANSPLANT_CONTRASTS`).
