# 30-Day VLM/MLLM Research Foundation

This is the curriculum I would use for your situation: **you already know ML/DL/Transformers, but need enough LLM + VLM + reliability + research-method knowledge to understand your thesis rather than merely execute AI-generated instructions.**

It follows the research playbook's principle that entering a new field does **not** require exhaustive mastery first; you need enough vocabulary and conceptual understanding to recognize established knowledge, disagreements, failure modes, and research gaps.

Your thesis is also unusually well suited to this approach because its core question is not "how do I build a VLM?" but **what happens when a VLM receives conflicting visual and textual evidence, and does explicit conflict reasoning actually change its arbitration behavior?**

---

# How to use the 30 days

### Daily workload

Aim for **2.5–4 hours/day**:


| Activity                                   |       Time |
| -------------------------------------------- | -----------: |
| Learn/watch/read                           | 60–90 min |
| Read primary paper sections                | 45–90 min |
| Small experiment / code inspection / notes | 30–60 min |
| Explain-from-memory exercise               | 15–30 min |

### Four rules

1. **Do not read every paper cover-to-cover.**
2. **Do not take another giant generic LLM course.**
3. **Do not memorize architectures. Understand information flow.**
4. Every 2–3 days, explain the concept **without looking at notes**.

The research playbook explicitly recommends using AI as a search-expansion tool rather than treating it as the scientific authority, and emphasizes moving from broad field → phenomenon → explanation → gap → hypothesis → discriminating experiment.

---

# Phase 1 — LLM foundation

## Days 1–3: What an LLM actually does

### Day 1 — Transformer refresher → LLM

**Learn**

You already know Transformers, so don't spend the day relearning attention equations.

Focus on:

* tokenization
* token IDs
* embeddings
* positional information
* self-attention
* residual connections
* layer normalization
* feed-forward layers
* logits
* next-token prediction

The key mental model:

```text
text
 ↓
tokens
 ↓
embeddings
 ↓
Transformer layers
 ↓
hidden representation
 ↓
logits
 ↓
probability distribution
 ↓
next token
 ↓
repeat
```

### Primary resource

**Attention Is All You Need** — read:

* Abstract
* §1 Introduction
* §2 Background
* §3 Model Architecture
* §3.1 Encoder/Decoder
* §3.2 Attention

Do **not** attempt to memorize the mathematics.

### Exit test

You should be able to answer:

> "If I give an LLM the sentence `The answer is`, what exactly happens between the characters entering the system and the next token being selected?"

---

## Day 2 — Autoregressive generation

Learn:

* causal masking
* teacher forcing
* logits
* softmax
* greedy decoding
* temperature
* top-k
* top-p
* EOS
* maximum generation length
* deterministic vs stochastic generation

Understand this distinction:

```text
MODEL COMPUTATION
       ↓
logits
       ↓
DECODING PROCEDURE
       ↓
generated token
```

This distinction becomes important later because **prompt interventions and decoding choices are different experimental variables.**

### Practical task

Run a tiny language model and change:

* temperature
* max tokens
* greedy vs sampling

You aren't studying model performance. You're learning what **generation** means.

### Exit test

Explain why:

> "The model knows the answer"

and

> "The model generated the correct answer"

are not necessarily equivalent statements.

---

## Day 3 — Training an LLM

Learn the difference between:

```text
Pretraining
     ↓
SFT
     ↓
Preference/alignment training
     ↓
Inference
```

Understand:

* pretraining objective
* next-token prediction
* supervised fine-tuning
* instruction tuning
* preference optimization at a conceptual level
* pretrained model vs instruction model

### Primary resource

Use the relevant sections of the **Qwen2.5-VL Technical Report** later rather than trying to learn every modern training method separately. ([arXiv][1]https://arxiv.org/abs/2502.13923?utm_source=chatgpt.com)

### Exit test

You should be able to explain:

> Why does an instruction-tuned model behave differently from the same base language model?

---

# Phase 2 — From language models to multimodal models

## Day 4 — What does "multimodal" actually mean?

This is the first major transition.

Learn:

```text
IMAGE
 ↓
Vision Encoder
 ↓
Visual representation
 ↓
Connector / Projector
 ↓
LLM representation space
 ↓
Language model
 ↓
Text
```

Understand that an MLLM is **not simply an LLM that magically understands pixels**.

There must be some mechanism that converts visual information into representations the language model can use.

### Exit test

Draw the architecture from memory.

If you cannot draw it, don't proceed.

---

# Day 5 — CLIP

Study **CLIP: Connecting Text and Images**.

CLIP is important because it gives you the basic idea of learning a shared relationship between images and language. OpenAI describes CLIP as learning visual concepts from natural-language supervision and using language to perform zero-shot visual classification. ([OpenAI][2]https://openai.com/index/clip/?utm_source=chatgpt.com)

### Read

Focus on:

* motivation
* contrastive learning
* image encoder
* text encoder
* image/text embeddings
* similarity
* zero-shot prediction

Don't get trapped in implementation details.

### Mental model

```text
IMAGE ──→ Image Encoder ──→ vector
                              ↕ similarity
TEXT  ──→ Text Encoder  ──→ vector
```

### Exit test

Explain why CLIP is useful for understanding the history of modern VLMs even though your thesis uses a generative VLM.

---

# Day 6 — Flamingo

Read **Flamingo: a Visual Language Model for Few-Shot Learning**. ([arXiv][3]https://arxiv.org/abs/2204.14198?utm_source=chatgpt.com)

Focus on:

* pretrained vision model
* pretrained language model
* bridge between modalities
* interleaved image/text inputs
* why freezing existing models can be useful

Don't memorize every component.

### Your task

Write:

> "What problem does Flamingo solve that a language-only model cannot?"

Then:

> "How does Flamingo connect vision and language?"

---

# Day 7 — BLIP-2

Read **BLIP-2**. ([arXiv][4]https://arxiv.org/abs/2301.12597?utm_source=chatgpt.com)

This paper is particularly useful because its architecture gives you a very clean conceptual bridge:

```text
Frozen Image Encoder
        ↓
      Q-Former
        ↓
Frozen LLM
```

The paper's central idea is to bridge a frozen image encoder and frozen LLM using a lightweight Querying Transformer. ([arXiv][4]https://arxiv.org/abs/2301.12597?utm_source=chatgpt.com)

### Exit test

Compare:


| Model    | Main idea                                              |
| ---------- | -------------------------------------------------------- |
| CLIP     | shared image/text representation                       |
| Flamingo | connect pretrained vision + language models            |
| BLIP-2   | lightweight learned bridge between frozen vision + LLM |
| LLaVA    | vision encoder + projection + instruction-tuned LLM    |

You should understand **why the architectures evolved**.

---

# Phase 3 — Modern generative VLMs

## Day 8 — LLaVA

Read **Visual Instruction Tuning**. ([arXiv][5]https://arxiv.org/abs/2304.08485?utm_source=chatgpt.com)

Focus on:

* vision encoder
* projection layer
* LLM
* visual instruction data
* multimodal instruction tuning

Mental model:

```text
             IMAGE
               ↓
        Vision Encoder
               ↓
         Projection
               ↓
       visual tokens
               ↓
TEXT ─────────────────→ LLM
                         ↓
                      answer
```

This architecture is much closer to how you should think about your thesis model.

### Exit test

Explain:

> What does the LLM actually receive from the image?

Not "the image."

It receives **a sequence of learned visual representations/tokens**.

---

# Day 9 — Qwen-VL → Qwen2-VL

Before jumping to Qwen2.5-VL, understand the evolution.

Study the official Qwen material and the Qwen2-VL paper.

Pay particular attention to:

* dynamic resolution
* visual tokenization
* spatial information
* multimodal rotary position encoding
* OCR/document understanding
* image/video input

The official Qwen2.5-VL repository also documents its architecture evolution and dynamic-resolution processing. ([GitHub][6]https://github.com/QwenLM-corp/Qwen2.5-VL?utm_source=chatgpt.com)

---

# Day 10 — Qwen2.5-VL architecture

This is a **high-priority thesis day**.

Read the **Qwen2.5-VL Technical Report**. ([arXiv][1]https://arxiv.org/abs/2502.13923?utm_source=chatgpt.com)

You do not need the entire paper.

Study:

1. model architecture
2. vision encoder
3. dynamic resolution
4. visual token processing
5. position encoding
6. training strategy
7. instruction tuning
8. inference capabilities

The report describes Qwen2.5-VL's native dynamic-resolution ViT, window attention, spatial/temporal processing, and multimodal reasoning capabilities. ([arXiv][1]https://arxiv.org/abs/2502.13923?utm_source=chatgpt.com)

Also inspect the **official repository**, especially the model-loading and inference examples. ([GitHub][6]https://github.com/QwenLM-corp/Qwen2.5-VL?utm_source=chatgpt.com)

### Deliverable

Draw:

```text
             IMAGE
               │
               ▼
        Qwen Vision Encoder
               │
               ▼
      Visual representations
               │
               ▼
       Multimodal position info
               │
               ▼
        Qwen language model
               │
               ▼
       autoregressive output
```

Then annotate where:

* visual evidence enters
* textual evidence enters
* reasoning occurs
* output tokens are generated

---

# Day 11 — Actually run the model

Now stop reading.

Run Qwen2.5-VL-3B-Instruct in Colab.

Use the official implementation rather than writing your own architecture.

[Qwen2.5-VL official repository](https://github.com/QwenLM/Qwen2.5-VL?utm_source=chatgpt.com)

Perform only simple tests:

### Test A

Image + question.

### Test B

Same image + different question.

### Test C

Same question + different image.

### Test D

Image + text containing contradictory information.

Do **not** collect thesis results yet.

You are learning the interface between:

```text
input construction
      ↓
processor
      ↓
model
      ↓
generation
      ↓
output
```

---

# Day 12 — Multimodal information flow

Now answer the most important architectural question for your thesis:

> **Where can visual and textual information compete?**

Study:

* image tokens
* text tokens
* attention
* multimodal sequence
* cross-modal interaction
* autoregressive generation

You don't need mechanistic interpretability yet.

The goal is simply to understand:

```text
IMAGE ──→ visual representations ─┐
                                  ├→ multimodal model → output
TEXT ───→ text representations ───┘
```

### Exercise

Take one of your conflict examples and annotate:

```text
Image says: A
Text says: B
Question: ?
Expected answer: A/B
```

Then ask:

> Which information sources are available to the model at generation time?

This becomes the foundation for your **source-arbitration** thesis.

---

# Phase 4 — VLM failure modes

## Day 13 — VLM hallucination

Study **HallusionBench**. ([arXiv][7]https://arxiv.org/abs/2310.14566?utm_source=chatgpt.com)

Learn:

* visual illusion
* language hallucination
* image-context reasoning
* paired/control questions
* diagnostic evaluation

This is important because it teaches you something more valuable than "VLMs hallucinate":

> **How do researchers turn a vague failure into a controlled benchmark?**

HallusionBench deliberately uses question structures and controls to analyze response tendencies and failure modes. ([arXiv][7]https://arxiv.org/abs/2310.14566?utm_source=chatgpt.com)

---

# Day 14 — Hallucination evaluation

Study the paper:

**Evaluating the Quality of Hallucination Benchmarks for Large Vision-Language Models.** ([arXiv][8]https://arxiv.org/abs/2406.17115?utm_source=chatgpt.com)

This is a methodological day.

Focus on:

* benchmark reliability
* test-retest reliability
* validity
* metric quality
* benchmark construction problems

This is directly relevant to your research philosophy.

A benchmark is **not automatically trustworthy just because it is published.**

---

# Day 15 — Visual grounding

Study:

* object grounding
* spatial grounding
* OCR
* visual evidence
* localization

Use the Qwen2.5-VL report as your primary source for modern capabilities. ([arXiv][1]https://arxiv.org/abs/2502.13923?utm_source=chatgpt.com)

You should understand the difference between:

> "The model generated a plausible answer."

and

> "The answer is actually supported by a particular visual region."

This distinction matters when discussing **evidence**.

---

# Day 16 — Modality bias and conflict

Now directly enter your research territory.

Study literature around:

* modality conflict
* visual bias
* language priors
* cross-modal inconsistency
* visual/text contradiction
* modality dominance
* source arbitration

Do not yet worry about your own results.

Your goal is to build a vocabulary map:

```text
Multimodal reasoning
       │
       ├── grounding
       ├── hallucination
       ├── modality bias
       ├── conflicting evidence
       ├── language priors
       ├── visual priors
       └── source arbitration
```

---

# Day 17 — Reasoning in VLMs

Return briefly to LLM reasoning.

Read **Chain-of-Thought Prompting Elicits Reasoning in Large Language Models**. ([arXiv][9]https://arxiv.org/abs/2201.11903?utm_source=chatgpt.com)

Understand:

* rationale
* intermediate reasoning
* answer generation
* why additional reasoning tokens can change performance

But be careful:

**better answer ≠ faithful explanation.**

That distinction becomes critical tomorrow.

---

# Day 18 — CoT faithfulness

Read **Towards Faithful Chain-of-Thought**. ([arXiv][10]https://arxiv.org/abs/2405.18915?utm_source=chatgpt.com)

This is extremely relevant to your thesis.

Focus on:

* reasoning trace
* context
* intermediate reasoning
* final answer
* causal relevance
* unfaithfulness

The paper explicitly studies cases where the model can use information from context that is not represented in its stated reasoning chain, demonstrating why a generated rationale should not automatically be treated as a faithful explanation of the decision process. ([arXiv][10]https://arxiv.org/abs/2405.18915?utm_source=chatgpt.com)

### Your key question

> If I force a model to verbalize a conflict before answering, did the verbalization **cause** the decision change, or did it merely provide a plausible explanation for a decision the model would have made anyway?

That is essentially the intellectual heart of your thesis.

---

# Phase 5 — Experimental research methodology

## Day 19 — Correlation vs intervention

Learn:

* observation
* intervention
* control
* counterfactual
* causal claim
* confound

Example:

### Weak claim

> Models that produce conflict explanations are more likely to choose the text answer.

### Stronger experimental question

> Does forcing conflict evaluation change source selection compared with a length-matched neutral prompt?

The second is an intervention.

Your canonical playbook explicitly treats competing hypotheses and discriminating interventions as the core of Level-3 causal research.

---

# Day 20 — Experimental controls

This is one of the most important days.

Learn:

### Control variables

Things kept constant.

### Independent variable

What you deliberately change.

### Dependent variable

What you measure.

### Confound

A second explanation for the observed effect.

For your thesis:

```text
Arm 2
Neutral explanation
       ↓
     answer

Arm 3
Conflict explanation
       ↓
     answer
```

But both have additional generated text.

Therefore:

> Is the effect caused by **conflict information**, or merely by **giving the model more reasoning tokens?**

That is why your neutral placebo matters.

---

# Day 21 — Experimental design of your thesis

Now reconstruct your four arms without looking at the canonical specification.

You should be able to explain:


| Arm             | Purpose                                                    |
| ----------------- | ------------------------------------------------------------ |
| Direct          | baseline behavior                                          |
| Neutral placebo | controls for additional prompt/generation budget           |
| Conflict        | tests the intervention                                     |
| Prefill         | tests whether short rationale steering alone is sufficient |

Then explain:

> Why can't Arm 1 vs Arm 3 alone establish your main causal claim?

If you cannot answer this clearly, repeat Days 19–21.

---

# Day 22 — Paired experiments and McNemar

Learn:

* paired observations
* discordant pairs
* contingency tables
* McNemar's test
* odds ratio
* confidence intervals
* effect size
* risk ratio

Do not merely learn the formulas.

Understand why your data are **paired**.

The same conflict item is evaluated under multiple conditions.

So the important question isn't merely:

> "What percentage chose image?"

It is:

> "How often did the **same item** change from visual selection to textual selection after the intervention?"

That is why paired analysis is powerful.

---

# Day 23 — Exact-match and behavioral metrics

Study your evaluation pipeline.

Understand:

* exact match
* answer extraction
* ambiguous output
* abstention
* source classification
* image-ground-truth match
* text-ground-truth match

Separate:

```text
SOURCE SELECTION
        vs
ANSWER CORRECTNESS
```

This is crucial.

A model can select the text source but still calculate the answer incorrectly.

Therefore:

```text
Source arbitration ≠ task accuracy
```

Your thesis measures both.

---

# Day 24 — Threats to validity

Learn to attack your own experiment.

Ask:

### Internal validity

Could something other than the intervention explain the result?

### Measurement validity

Does your metric actually measure what you claim?

### External validity

Does this generalize beyond the tested setting?

### Construct validity

Does "source arbitration" actually correspond to the operational definition you use?

### Statistical validity

Are the statistical tests appropriate?

Your canonical methodology specifically emphasizes leakage-resistant data, matched placebos, deterministic metrics, and controls against trivial compute confounds.

---

# Phase 6 — Become a researcher, not just a model user

## Day 25 — Learn to read papers

Use **Keshav's three-pass style** from your research playbook.

### Pass 1 — Structure

Read:

* title
* abstract
* figures
* section headings
* conclusion

Answer:

> What problem is this paper solving?

### Pass 2 — Evidence

Read:

* methodology
* experiments
* tables
* ablations

Answer:

> What evidence supports the central claim?

### Pass 3 — Reimplementation-level understanding

Only for the **few papers directly adjacent to your thesis**.

Ask:

> Could I reproduce the central experiment from this paper?

Your playbook specifically recommends limiting deep Pass-3 treatment to a small number of directly adjacent papers rather than attempting to deeply read dozens of papers.

---

# Day 26 — How researchers find gaps

Don't search:

> "What is a novel VLM thesis?"

Instead search:

```text
phenomenon
    ↓
existing explanation
    ↓
assumption
    ↓
missing control
    ↓
competing explanation
    ↓
discriminating experiment
```

For example:

```text
VLM visual/text conflict
        ↓
models may favor one modality
        ↓
verbalization appears to help
        ↓
BUT verbalization adds computation
        ↓
is the improvement actually caused by conflict evaluation?
        ↓
neutral length-matched placebo
```

That is much closer to how you should think about research.

The playbook calls this interaction between **phenomenological auditing** and **epistemic interrogation of the literature** the Dual-Engine discovery model.

---

# Day 27 — Reconstruct your thesis from first principles

Close all documents.

Write these yourself:

### 1. Problem

What failure are you studying?

### 2. Phenomenon

What behavior has been observed?

### 3. Existing explanation

What do previous researchers think causes it?

### 4. Gap

What has not been isolated?

### 5. RQ

What exact question are you testing?

### 6. H0

What happens if your causal explanation is wrong?

### 7. H1

What happens if it is correct?

### 8. Intervention

What exactly changes?

### 9. Control

What alternative explanation does the placebo eliminate?

### 10. Measurement

What exactly do you measure?

If you can write all ten without assistance, your conceptual understanding is becoming research-level rather than tool-dependent.

---

# Day 28 — Reconstruct the entire experiment

Draw this:

```text
                    CONFLICT DATASET
                           │
                           ▼
                 ┌───────────────────┐
                 │ Same conflict item│
                 └─────────┬─────────┘
                           │
          ┌────────────────┼────────────────┐
          ▼                ▼                ▼
       Direct          Neutral           Conflict
       Arm 1           Arm 2              Arm 3
          │                │                │
          └────────────────┼────────────────┘
                           ▼
                    Source selection
                           │
              ┌────────────┴────────────┐
              ▼                         ▼
         Image source              Text source
              │                         │
              └────────────┬────────────┘
                           ▼
                    Exact-match answer
                           │
                           ▼
                 Paired statistical test
```

Then add Arm 4.

You should be able to explain every arrow.

---

# Day 29 — Results interpretation

Now study your actual results.

Do **not** start with:

> "My model improved."

Start with:

> "What behavioral transition occurred?"

For example:

```text
Neutral → Conflict

visual
  ↓
text

visual
  ↓
abstention

visual
  ↓
visual
```

This lets you reason about **behavioral state transitions**, not merely aggregate percentages.

Then examine:

* GSM8K vs SVAMP
* source selection
* exact-match crossover
* abstention
* persistent visual cases
* ambiguous cases
* prefilling behavior

This corresponds directly to the roadmap's next-stage **deep data mining and stratified analysis**.

---

# Day 30 — The defense test

This is the final gate.

You should be able to answer these **without AI assistance**.

### Architecture

1. What is an LLM?
2. What is a VLM?
3. What does the vision encoder do?
4. What does the connector/projector do?
5. What does the language model receive?
6. How does Qwen2.5-VL process images?

### Research

7. What phenomenon are you studying?
8. What is the competing explanation?
9. What is the intervention?
10. What is the placebo?
11. What confound does the placebo address?
12. Why is the experiment paired?
13. Why McNemar?
14. What does the odds ratio mean?
15. What does exact-match crossover tell you?
16. What does it **not** tell you?
17. Why doesn't your experiment prove anything about internal attention heads?
18. Why can't you claim natural-image generalization?
19. Why is rationale prefilling a different intervention from full conflict verbalization?
20. What result would weaken your main hypothesis?

### Final scientific test

Answer this in one paragraph:

> **"What new knowledge does this thesis contribute if the main hypothesis is confirmed, and what useful knowledge does it contribute if the hypothesis is not confirmed?"**

If you can answer that cleanly, you are ready to write the scientific story.

---

# The resource stack

Do **not** use 50 different resources. Use a small hierarchy.

## Tier 1 — Primary papers

These are your scientific sources.

### Foundation

* **Attention Is All You Need**
* **CLIP**
* **Flamingo**
* **BLIP-2**
* **LLaVA**

### Modern VLM

* **Qwen2-VL**
* **Qwen2.5-VL Technical Report**

### Reliability

* **HallusionBench**
* **Hallucination Benchmark Quality Measurement**

### Reasoning

* **Chain-of-Thought Prompting**
* **Faithful Chain-of-Thought**

The Qwen2.5-VL technical report is particularly important for you because it describes the exact model family underpinning your thesis. ([arXiv][1]https://arxiv.org/abs/2502.13923?utm_source=chatgpt.com)

---

# Tier 2 — Official implementations

For your thesis model, use the official Qwen repository rather than third-party tutorials.

[Qwen2.5-VL GitHub repository](https://github.com/QwenLM/Qwen2.5-VL?utm_source=chatgpt.com)

The repository provides model usage, processing utilities, multimodal examples, and implementation information. ([GitHub][6]https://github.com/QwenLM-corp/Qwen2.5-VL?utm_source=chatgpt.com)

---

# Tier 3 — YouTube

Use YouTube **only for intuition**.

Good uses:

* Transformer intuition
* attention visualization
* tokenization
* VLM architecture explanations
* Qwen2.5-VL walkthroughs

Bad use:

> Watching 30 hours of "Complete VLM Course" instead of reading the actual papers.

A video can help you understand a concept.

It cannot establish:

> "The paper found X under experimental condition Y."

For that, read the paper.

---

# Tier 4 — Blogs

Use blogs for:

* implementation details
* architecture diagrams
* release explanations
* debugging
* practical intuition

Do not use a blog as the final authority for a scientific claim when the original paper is available.

---

# Your source hierarchy

For **your thesis**, I recommend:

```text
                 YOUR EXPERIMENT
                       ↑
                Official code
                       ↑
                Original paper
                       ↑
            Official documentation
                       ↑
               Technical article
                       ↑
                    Video
                       ↑
                    AI tutor
```

AI is useful at every level for **explaining and connecting information**, but the lower layers should not replace the higher ones for scientific claims.

---

# What you should NOT study during these 30 days

This is important.

Do **not** disappear into:

* RLHF implementation
* PPO mathematics
* distributed LLM training
* CUDA optimization
* FlashAttention internals
* MoE architecture
* multimodal pretraining from scratch
* diffusion models
* video-language models
* robotics/VLA
* agent frameworks
* mechanistic interpretability in full depth
* every new 2026 VLM release

Some of those are valuable fields. They are not prerequisites for understanding your current thesis.

Your canonical constraints are inference-first and centered on compact open models within Colab-class hardware, so learning massive-model training infrastructure would have very low return for this thesis.

---

# The actual progression

The whole 30 days can be compressed into this conceptual chain:

```text
DAYS 1–3
LLM
│
│ "How does language generation work?"
▼
DAYS 4–7
MULTIMODALITY
│
│ "How can an LLM receive visual information?"
▼
DAYS 8–12
MODERN VLM
│
│ "How does Qwen2.5-VL actually process image + text?"
▼
DAYS 13–18
VLM FAILURE + REASONING
│
│ "Why can visual and linguistic evidence conflict?"
▼
DAYS 19–24
EXPERIMENTAL SCIENCE
│
│ "How can I distinguish competing explanations?"
▼
DAYS 25–26
RESEARCH PRACTICE
│
│ "How do researchers turn observations into questions?"
▼
DAYS 27–30
YOUR THESIS
│
│ "What exactly did I discover?"
▼
THESIS WRITING + DEFENSE
```

The important point is that **you do not need to become an expert in all of VLM research before touching your thesis.** Your existing ML/DL/Transformer background means the first week is mostly filling conceptual gaps; the second and third weeks move rapidly toward the exact research territory.

By Day 30, the target is not "I know everything about VLMs."

The target is:

> **I can open a VLM paper, understand its architecture and experiment, identify its assumptions and controls, understand where my thesis sits relative to it, and explain my own experiment without asking an AI to explain my own work.**

That is the right foundation for your current thesis.

[1]: https://arxiv.org/abs/2502.13923?utm_source=chatgpt.com
[2]: https://openai.com/index/clip/?utm_source=chatgpt.com
[3]: https://arxiv.org/abs/2204.14198?utm_source=chatgpt.com
[4]: https://arxiv.org/abs/2301.12597?utm_source=chatgpt.com
[5]: https://arxiv.org/abs/2304.08485?utm_source=chatgpt.com
[6]: https://github.com/QwenLM-corp/Qwen2.5-VL?utm_source=chatgpt.com
[7]: https://arxiv.org/abs/2310.14566?utm_source=chatgpt.com
[8]: https://arxiv.org/abs/2406.17115?utm_source=chatgpt.com
[9]: https://arxiv.org/abs/2201.11903?utm_source=chatgpt.com
[10]: https://arxiv.org/abs/2405.18915?utm_source=chatgpt.com
