
# 30-Day Thesis Understanding & Defense Plan

Your situation is now clear: **you do not need another thesis-discovery phase.** You already have an experiment and a substantial empirical result. The problem is **knowledge debt**: you need to rebuild the scientific understanding underneath the experiment so that you can independently explain, verify, criticize, and defend it.

The goal of these 30 days is therefore **not** “learn everything about LLMs/VLMs.” It is:

> **Transformer → LLM → multimodal LLM/VLM → Qwen2.5-VL → your experiment → causal inference → statistics → limitations → defense**

By Day 30, you should be able to reconstruct your thesis from a blank page without asking an AI what anything means.

---

# Overall Structure


| Phase                                  |   Days | Main goal                                                 |
| ---------------------------------------- | -------: | ----------------------------------------------------------- |
| **1. LLM Foundations**                 |   1–6 | Understand what the language model actually does          |
| **2. From LLM to VLM**                 |  7–11 | Understand how images enter the Transformer               |
| **3. Qwen2.5-VL**                      | 12–14 | Understand the actual model you used                      |
| **4. Your Experiment**                 | 15–19 | Understand every experimental decision                    |
| **5. Causality & Statistics**          | 20–24 | Understand what your results actually establish           |
| **6. Critical Analysis**               | 25–27 | Destroy weak interpretations and alternative explanations |
| **7. Thesis Reconstruction & Defense** | 28–30 | Become independently defensible                           |

### Daily time target

**2.5–3.5 hours/day** is enough.

Use this cycle every day:

> **Learn → close the material → explain from memory → test yourself → connect to thesis**

Do **not** spend the entire day reading.

---

# PHASE 1 — LLM FOUNDATIONS

## Day 1 — What Is an LLM?

### You must understand

Start from your Transformer knowledge.

Build this chain:

```text
Text
 ↓
Tokens
 ↓
Token IDs
 ↓
Embeddings
 ↓
Transformer
 ↓
Logits
 ↓
Probability distribution
 ↓
Next token
 ↓
Repeat
 ↓
Generated text
```

Understand:

* What a language model is
* What “language modeling” means
* What next-token prediction means
* Vocabulary
* Token IDs
* Embeddings
* Hidden states
* Logits
* Probabilities
* Parameters
* Context window
* Why an LLM can generate a sentence without explicitly storing a sentence template

### Critical question

> If I give an LLM `The cat sat on the`, what exactly is the model predicting?

You should be able to answer this mathematically and intuitively.

### Thesis connection

Your model ultimately produces **tokens**. Everything your thesis observes—rationales, source statements, answers, abstentions—is generated token by token.

### End-of-day test

Without notes, explain:

> “What happens inside an LLM when I give it a sentence?”

---

# Day 2 — Autoregressive Generation

This is one of the **most important days** for your thesis.

### Learn

Understand:

* Autoregressive generation
* Causal language modeling
* Causal attention mask
* Teacher forcing
* Training vs inference
* Greedy decoding
* Sampling
* Temperature
* Top-k
* Top-p
* EOS token
* `max_new_tokens`

Conceptually:

```text
Prompt
 ↓
Transformer
 ↓
logits
 ↓
choose next token
 ↓
append token
 ↓
Transformer again
 ↓
choose next token
 ↓
...
```

### Critical distinction

Training:

```text
"The cat sat on the mat"
       ↓
predict next tokens
```

Inference:

```text
"The cat"
   ↓
predict "sat"
   ↓
"The cat sat"
   ↓
predict "on"
   ↓
...
```

### Thesis connection

Your Arm 2 and Arm 3 differences happen **during generation**.

The model isn't first producing a complete hidden “answer” and then writing it down.

### End-of-day test

Explain why:

> Changing the prompt can change everything the model generates afterward.

---

# Day 3 — What Actually Happens During LLM Training?

You don't need to learn distributed training or GPU engineering.

Understand:

```text
Pretraining
    ↓
Language patterns / world knowledge
    ↓
Instruction tuning
    ↓
Instruction following
    ↓
Alignment / preference optimization
    ↓
Chat/instruction model
```

Learn:

* Pretraining
* Cross-entropy loss
* SFT
* Instruction tuning
* Preference optimization at conceptual level
* Why an instruction model behaves differently from a raw pretrained LM

### Critical distinction

Know the difference between:

> “The model knows something”

and

> “The model is likely to generate something given this prompt.”

This distinction will become extremely important when discussing **reasoning and rationalization**.

### Thesis connection

Your prompt intervention is acting on an already-trained model.

You are **not training Qwen2.5-VL**.

You are changing its inference-time input.

---

# Day 4 — Tokens, Chat Templates & Prompts

This day is highly practical.

Understand:

* Tokenization
* Subword tokens
* Special tokens
* System/user/assistant roles
* Chat templates
* Prompt formatting
* Assistant generation
* Prefilling
* Why token count ≠ word count

### You should understand

Why these two are scientifically different:

```text
User:
Solve this problem.
```

and:

```text
User:
Solve this problem.

Assistant:
The image and text contradict...
```

The second changes the **generation context**.

### Thesis connection

This is essential for understanding **Arm 4**.

### End-of-day test

Explain:

> What does assistant prefill actually mean computationally?

---

# Day 5 — Inference, Context and KV Cache

Learn:

* Transformer inference
* Prompt processing
* Generation loop
* KV cache
* Why generation becomes expensive token by token
* Why longer reasoning consumes more inference computation
* What `max_new_tokens` controls
* What truncation means

Conceptually:

```text
Prompt
 ↓
Process context
 ↓
KV cache
 ↓
Generate token 1
 ↓
Generate token 2
 ↓
Generate token 3
 ↓
...
```

### Thesis connection

You need this to understand:

* Arm 2 vs Arm 3
* reasoning-token differences
* Arm 4 prefilling
* truncation
* test-time compute

### Important correction

Do **not** memorize:

> “More tokens = more intelligence.”

Instead:

> More generated tokens provide additional opportunities for computation through sequential generation, but longer generation does not automatically mean better reasoning.

---

# Day 6 — LLM Knowledge Checkpoint

**No major new material.**

Close everything.

Take a blank sheet and draw:

```text
Prompt
 ↓
Tokenization
 ↓
Embeddings
 ↓
Transformer layers
 ↓
Hidden representation
 ↓
Logits
 ↓
Decoding
 ↓
Next token
 ↓
Repeat
```

Then explain each box.

### You must answer

1. What is an LLM?
2. What is a token?
3. What is an embedding?
4. What is a hidden state?
5. What is a logit?
6. What is softmax?
7. What is autoregressive generation?
8. What is causal masking?
9. What is greedy decoding?
10. What does `max_new_tokens` do?
11. What is KV cache?
12. Why can prompts change model behavior?

If you cannot answer one, mark:

> **UNKNOWN — RELEARN**

Do not proceed simply because the calendar says Day 7.

---

# PHASE 2 — FROM LLM TO VLM

# Day 7 — Why an LLM Cannot Directly “See” an Image

This is your conceptual bridge.

An LLM fundamentally processes **token representations**.

An image is:

```text
pixels
```

not language tokens.

So a VLM needs a mechanism like:

```text
Image
 ↓
Vision encoder
 ↓
Visual features
 ↓
Projection / connector
 ↓
LLM-compatible representation
 ↓
Language model
 ↓
Text output
```

### Understand

* Pixel
* Patch
* Vision Transformer
* Visual feature
* Visual token
* Projection
* Multimodal representation

### Thesis connection

Your image does not magically enter Qwen as “an image.”

There is an actual computational pathway.

---

# Day 8 — Vision Transformers & CLIP

You already know CNNs, so use that as the bridge.

Understand:

### CNN

```text
pixels
 ↓
convolution
 ↓
feature maps
 ↓
higher-level features
```

### ViT

```text
image
 ↓
patches
 ↓
patch embeddings
 ↓
Transformer
 ↓
visual representations
```

Learn:

* Image patches
* Patch embeddings
* Positional information
* Self-attention over image patches
* Vision Transformer
* CLIP at conceptual level
* Contrastive image-text learning

### Important

You do **not** need to reproduce CLIP training.

You need to understand why vision encoders can convert an image into representations that another model can use.

---

# Day 9 — Multimodal Architectures

Study the progression conceptually:

```text
Vision Encoder + LLM
```

and different ways to connect them.

Understand:

* Early fusion
* Late fusion
* Cross-attention
* Projection
* Multimodal tokens
* Vision-language alignment

Use:

* Flamingo
* BLIP-2
* LLaVA

as architectural examples.

### Don't memorize paper details.

Instead ask:

> “Where does the image information enter the language model?”

That question matters much more for your thesis.

---

# Day 10 — What Is a Modern VLM / MLLM?

Clarify terminology.

### LLM

Primarily language.

### VLM

Model capable of processing visual + language information.

### MLLM

More general multimodal language model capable of handling multiple modalities depending on architecture.

Understand:

```text
Image
Text
   ↓
Multimodal processing
   ↓
Language-model reasoning/generation
   ↓
Text
```

### Critical misconception to eliminate

Do not think:

> “VLM = image classifier + chatbot.”

Your model is performing multimodal sequence processing and language generation.

---

# Day 11 — Multimodal Information Flow

This should become one of your strongest conceptual days.

Take **one of your actual thesis samples**.

Trace:

```text
Rendered arithmetic image
        +
Text problem
        ↓
Image processing
        ↓
Visual representations
        +
Text token representations
        ↓
Multimodal Transformer processing
        ↓
Hidden states
        ↓
Autoregressive generation
        ↓
Rationale
        ↓
Answer
```

### Critical question

At what point does the model have access to:

* image information?
* text information?
* both simultaneously?
* generated rationale?

You don't need internal activation access to answer conceptually.

---

# PHASE 3 — UNDERSTAND YOUR ACTUAL MODEL

# Day 12 — Qwen2.5-VL Architecture

Now study **your exact model**, not VLMs generally.

You should be able to explain:

```text
Image
 ↓
Vision Transformer
 ↓
Spatial processing / patch merging
 ↓
Visual representations
 ↓
Multimodal positional information
 ↓
LLM
 ↓
Autoregressive generation
```

Study the official model documentation/paper and verify the architectural facts in your thesis report.

### Particularly understand

* Vision encoder
* Dynamic resolution
* Patch processing
* Visual tokens
* Projector/connector
* MRoPE
* LLM backbone
* Multimodal sequence

### Important

Do not memorize:

> “36 layers, 16 heads...”

unless you understand **why those things exist**.

Architecture numbers are secondary.

---

# Day 13 — Qwen Inference Pipeline

Understand your actual inference process.

Trace one experiment:

```text
Dataset item
 ↓
Image loaded
 ↓
Text prompt constructed
 ↓
Chat template
 ↓
Processor
 ↓
Vision + text inputs
 ↓
Qwen2.5-VL
 ↓
Generation
 ↓
Generated response
 ↓
Parser
 ↓
Behavioral classification
 ↓
Statistics
```

### You should know

What your code actually does at each stage.

This is a critical thesis-defense requirement.

---

# Day 14 — Reconstruct One Sample Completely

Take **one dataset item**.

Without AI:

1. Show its image.
2. Show its text.
3. Explain why the sources conflict.
4. Show Arm 2 prompt.
5. Show Arm 3 prompt.
6. Explain what differs.
7. Explain what the model generates.
8. Explain how source selection is determined.
9. Explain exact-match scoring.
10. Explain what the final row in your dataset means.

If you cannot do this, repeat Days 12–14.

---

# PHASE 4 — UNDERSTAND YOUR EXPERIMENT

# Day 15 — The Scientific Problem

Forget your implementation.

Explain the thesis as a scientific problem:

> A VLM receives two mutually contradictory sources. Under a neutral descriptive prompt, it strongly favors one modality. We test whether explicitly asking it to verbalize the conflict changes that source arbitration.

Then separate:

### Problem

Multimodal contradiction.

### Phenomenon

Visual capture.

### Intervention

Conflict verbalization.

### Outcome

Observed source arbitration.

### Secondary outcomes

* Exact-match execution
* Abstention
* State transitions

### Non-claim

Internal mechanism.

This distinction should become automatic.

---

# Day 16 — Dataset & Conflict Construction

Understand your dataset from first principles.

You need to explain:

* Where GSM8K/SVAMP contribute
* What an image problem is
* What the text problem is
* Why answers are mutually exclusive
* What `y_img` means
* What `y_txt` means
* Why clean rendering matters
* Why `degradation_level = 0`
* Why the population is 1,619
* Why this is not a random sample if you evaluated the entire defined clean population

### Critical question

> What exactly is being manipulated?

Not:

> “The image is difficult.”

Your images are deliberately **clean**.

The conflict is the important variable.

---

# Day 17 — Experimental Arms

You should be able to explain all arms without looking at your report.


| Arm    | Purpose                             |
| -------- | ------------------------------------- |
| Arm 1  | Direct baseline                     |
| Arm 2  | Neutral descriptive control         |
| Arm 3  | Conflict-verbalization intervention |
| Arm 4a | Exploratory image-directed prefill  |
| Arm 4b | Exploratory text-directed prefill   |

### Most important distinction

Your primary causal comparison is:

> **Arm 2 vs Arm 3**

Not Arm 1 vs Arm 3.

Why?

Because Arm 2 is intended to control for the additional verbalization/generation structure while withholding the semantic conflict-evaluation instruction.

### You must answer

> Why can't I simply compare Arm 1 and Arm 3?

---

# Day 18 — What Exactly Is Your Intervention?

This is probably one of the **most important defense days**.

Your intervention is not:

> “More thinking.”

Not:

> “Chain-of-thought.”

Not:

> “A longer prompt.”

Not:

> “Tell it to trust text.”

Your intervention is:

> **A prompt directive requiring explicit conflict evaluation and source-reliability reasoning before solving.**

Then explain what Arm 2 does differently.

### Major examiner attack

> “Isn't Arm 3 simply telling the model to do something different?”

You need to answer carefully:

**Yes, semantically it is different. That semantic difference is the intended intervention.** Arm 2 controls for the added neutral verbalization structure and approximate generation burden; Arm 3 adds the conflict-evaluation/source-arbitration directive.

Do not claim Arm 2 proves that every possible prompt confound has been eliminated.

---

# Day 19 — Measurements & Parsing

This is a frequently overlooked defense vulnerability.

Understand your measurement system.

## Track 1

Generated response → source classification.

Understand:

* entity extraction
* stoplists
* source indicators
* abstention regex
* ambiguity
* mutually exclusive states

## Track 2

Generated answer → exact numerical answer.

Understand:

```text
answer = y_img
```

versus

```text
answer = y_txt
```

### Critical question

> What if your parser is wrong?

You need to understand the distinction between:

**model behavior**

and

**measurement of model behavior**.

Your parser is an operational measurement system. It requires validation and has limitations.

---

# PHASE 5 — CAUSALITY & STATISTICS

# Day 20 — Correlation vs Causal Effect

You need to understand causal reasoning before using the word **causal**.

Simple example:

```text
Ice cream sales ↑
Drowning deaths ↑
```

Correlation does not mean ice cream causes drowning.

Why?

A third variable:

```text
Hot weather
 ↙       ↘
ice cream  swimming
             ↓
          drowning
```

Your experiment tries to establish a controlled intervention:

```text
Same item
Same model
Same conflicting sources
Same dataset
        ↓
Arm 2       Arm 3
control     intervention
        ↓
behavioral difference
```

### Key idea

You manipulate the prompt condition and observe the paired behavioral change.

---

# Day 21 — Why Paired Experimental Design?

This is extremely important.

You have:

```text
Item 1 → Arm 2 + Arm 3
Item 2 → Arm 2 + Arm 3
Item 3 → Arm 2 + Arm 3
...
Item 1619 → Arm 2 + Arm 3
```

Therefore each item acts as its own comparison unit.

Instead of asking:

> Are two unrelated groups different?

you ask:

> Did the same item change condition?

This removes much item-level variability.

### Understand

* paired data
* matched observations
* discordant pairs
* within-item comparison

---

# Day 22 — McNemar's Test

You need to understand this mathematically.

For the primary binary outcome:

```text
Visual
Non-visual
```

Build:


|                  | Arm 3 Visual | Arm 3 Non-visual |
| ------------------ | -------------: | -----------------: |
| Arm 2 Visual     |            a |                b |
| Arm 2 Non-visual |            c |                d |

McNemar focuses on:

```text
b and c
```

because these are the items that **changed state**.

Your result:

```text
b = 1057
c = 25
```

The important scientific observation is:

> Many more items moved from visual → non-visual than from non-visual → visual.

### Understand the formula

```text
χ² = (|b-c|-1)² / (b+c)
```

You don't need to become a mathematical statistician.

But you must understand **why this test matches your design**.

---

# Day 23 — Effect Sizes

Do not stop at:

> p < 0.001

Learn what each result means.

### Risk difference

```text
89.50% - 25.76%
= 63.74 percentage points
```

This directly describes the marginal change in visual capture.

### Relative risk

```text
RR = 25.76 / 89.50
≈ 0.288
```

Meaning:

> The marginal probability of visual capture under Arm 3 was about 0.288 times that under Arm 2.

### Paired odds ratio

```text
1057 / 25 ≈ 42.28
```

Meaning:

> Among discordant items, the visual → non-visual transition occurred about 42 times as often as the reverse transition.

### Cohen's h

Understand it as a standardized measure of difference between proportions.

Do **not** call it “cognitive variance.”

---

# Day 24 — Exact Match, Abstention & Transition Matrix

Now connect behavior to task performance.

Understand:

### Source-conditioned exact match

For every generated answer:

```text
matches image answer?
matches text answer?
matches neither?
```

Your important result:

```text
Arm 2:
Image = 35.64%
Text  = 4.69%

Arm 3:
Image = 11.74%
Text  = 35.76%
```

The key observation is that source selection and numerical execution move together.

But be careful:

> This does not prove an internal reasoning mechanism.

It provides behavioral evidence that the output changed in a way consistent with solving the competing source's problem.

### Transition matrix

Call it:

> **within-item behavioral state-transition matrix**

rather than automatically calling it a Markov model.

You are observing transitions between conditions; you are not necessarily modeling a stochastic Markov process.

---

# PHASE 6 — CRITICAL ANALYSIS

# Day 25 — Truncation & Test-Time Compute

You need to understand your biggest methodological issue.

Your data shows:

* Arm 2: 37.6% reached the ceiling
* Arm 3: 44.2% reached the ceiling

Understand:

* `max_new_tokens`
* generation ceiling
* censoring/truncation
* why long reasoning can be cut off
* why exact-match scoring can be affected

Then understand your sensitivity analysis:

```text
Full population:
≈ -63.7 pp

Non-truncated:
≈ -65.0 pp
```

### Defense answer

Do not say:

> “Truncation was completely ruled out.”

Say:

> “The sensitivity analysis indicates that the primary arbitration shift persists in the non-truncated cohort, reducing concern that the observed effect is driven primarily by generation truncation.”

That is scientifically safer.

---

# Day 26 — Attack the Thesis

Today you become the hostile examiner.

Write answers to:

### Attack 1

> “Arm 3 simply tells the model to choose differently.”

### Attack 2

> “Arm 3 has more reasoning. Isn't this just extra compute?”

### Attack 3

> “Why not compare Arm 1 and Arm 3?”

### Attack 4

> “Your parser may be wrong.”

### Attack 5

> “The model could simply be following keywords.”

### Attack 6

> “Why only one model?”

### Attack 7

> “Why arithmetic?”

### Attack 8

> “Why rendered images?”

### Attack 9

> “How do you know the model actually changed its internal attention?”

### Attack 10

> “Isn't the rationale merely post-hoc explanation?”

You should answer each in **30–60 seconds**.

---

# Day 27 — What Your Thesis Does NOT Prove

This day is essential because strong defense is not only knowing what you proved.

Create two columns:


| Supported                                | Not supported                         |
| ------------------------------------------ | --------------------------------------- |
| Behavioral source arbitration changed    | Internal attention physically changed |
| Change occurred after intervention       | Human-like reasoning occurred         |
| Exact-match behavior also shifted        | Rationale is necessarily faithful     |
| Abstention increased                     | Model has genuine epistemic awareness |
| Effect persisted in sensitivity analysis | Universal VLM behavior                |
| Qwen2.5-VL-3B responded strongly         | Other VLMs will behave identically    |

Your thesis becomes stronger when you know where its boundary ends.

---

# PHASE 7 — RECONSTRUCT THE THESIS

# Day 28 — Rebuild Thesis From Blank Page

No AI.

No thesis report.

No notes.

Start with:

```text
My thesis asks:
_________________________

The problem is:
_________________________

The gap is:
_________________________

My hypothesis is:
_________________________

I manipulate:
_________________________

I compare:
_________________________

My primary outcome is:
_________________________

My statistical test is:
_________________________

My main result is:
_________________________

My strongest alternative explanation is:
_________________________

My strongest limitation is:
_________________________
```

Then reconstruct the complete pipeline.

If you cannot do this, identify exactly which knowledge node failed.

---

# Day 29 — Three-Level Explanation Test

You need to explain the thesis at three levels.

## Level 1 — Nontechnical

Explain it to someone who knows nothing about AI.

Example structure:

> “I gave a vision-language model an image and a text problem containing conflicting information. Under a normal prompt it mostly followed the image. I then added a prompt asking it to explicitly identify the conflict and evaluate the sources. The model's behavior changed substantially, and the change was measured on the same problems.”

## Level 2 — CSE Student

Now explain:

* Transformer
* autoregressive generation
* vision encoder
* multimodal integration
* intervention
* paired experiment
* exact match
* McNemar

## Level 3 — Thesis Examiner

Explain:

* estimand
* intervention
* control
* paired design
* measurement validity
* alternative explanations
* sensitivity analysis
* scope of inference
* limitations
* non-claims

If you can move between all three levels, your understanding is becoming real rather than memorized.

---

# Day 30 — Full Mock Defense

Do a **60–90 minute closed-book defense**.

Answer these without AI.

## Part A — Foundations

1. What is a Transformer?
2. What is an LLM?
3. How does autoregressive generation work?
4. What is a token?
5. What is a logit?
6. What is causal attention?
7. What is greedy decoding?
8. What is KV cache?

## Part B — VLM

9. What is a VLM?
10. How does an image enter a VLM?
11. What does the vision encoder do?
12. What is a visual token?
13. Why is a projector/connector required?
14. How are image and text information combined?
15. What does the LLM ultimately generate?

## Part C — Your model

16. Why Qwen2.5-VL?
17. What is its vision component?
18. What is its language component?
19. What is MRoPE?
20. What happens to an image before generation?

## Part D — Your experiment

21. What is the exact research question?
22. What is the causal intervention?
23. Why Arm 2?
24. Why Arm 3?
25. Why not Arm 1 vs Arm 3?
26. What is visual capture?
27. How is it measured?
28. What is exact match?
29. What is abstention?
30. What is Arm 4?

## Part E — Statistics

31. Why paired data?
32. Why McNemar?
33. What are `b` and `c`?
34. Why is your result statistically significant?
35. What does the 63.74 pp shift mean?
36. What does RR = 0.288 mean?
37. What does OR = 42.28 mean?
38. Why does p-value alone not establish practical importance?

## Part F — Scientific interpretation

39. What does your experiment actually establish?
40. What does it not establish?
41. Could this be prompt-following?
42. Could this be extra computation?
43. Could this be truncation?
44. Could the parser be wrong?
45. Could this be keyword behavior?
46. Why is exact-match evidence useful?
47. Why does abstention matter?
48. Why can't you claim internal attention rerouting?

## Part G — Limitations

49. Why one model?
50. Why arithmetic?
51. Why rendered images?
52. Why not natural images?
53. Why not multiple VLM families?
54. What would you test next if you had another three months?

---

# The Knowledge You Actually Need

After 30 days, your knowledge should look approximately like this:

```text
                    YOUR THESIS
                        │
        ┌───────────────┴────────────────┐
        │                                │
     SCIENCE                         EXPERIMENT
        │                                │
   Transformer                       Dataset
        │                                │
       LLM                           Conflict
        │                                │
 Autoregressive                     Arm 2
  generation                          │
        │                            Arm 3
     VLM                                │
        │                         Measurement
 Vision encoder                         │
        │                           Statistics
 Multimodal                              │
 integration                        Results
        │                                │
 Qwen2.5-VL ─────────────────────── Interpretation
                                         │
                                   Limitations
                                         │
                                      Defense
```

You **do not** need to become an expert in every branch of modern GenAI.

---

# What You Should NOT Spend These 30 Days Learning

This is important because your biggest risk is **scope explosion**.

Do not spend serious study time on:

* RLHF implementation
* PPO implementation
* distributed LLM training
* CUDA programming
* FlashAttention implementation details
* MoE internals
* diffusion models
* image generation
* video-language models
* robotics/VLA
* autonomous driving
* agents
* RAG
* MCP
* vector databases
* prompt-engineering tricks
* every new 2026 VLM
* mechanistic interpretability in general
* training your own LLM
* training your own VLM

Unless a specific defense question requires one of these, they are **outside your immediate knowledge requirement**.

---

# The 10 Things You Must Know Extremely Well

If time becomes tight, prioritize these:

### 1. Autoregressive generation

You must understand exactly how the model generates its response.

### 2. How an image becomes model-readable information

```text
image → vision encoder → visual representation → multimodal model
```

### 3. Qwen2.5-VL's actual architecture

Not every implementation detail—just the information flow.

### 4. Arm 2 vs Arm 3

You should be able to explain the control/intervention distinction instantly.

### 5. What “causal” means in your thesis

Not philosophical causality. Your experimental intervention and its observed effect.

### 6. Your measurement system

You must know exactly how source selection and exact-match outcomes are produced.

### 7. Why McNemar's test

Especially:

```text
b = 1057
c = 25
```

and why those discordant pairs matter.

### 8. Exact-match crossover

This is central to your interpretation.

### 9. Alternative explanations

Especially:

* extra compute
* prompt-following
* parser validity
* truncation
* keyword effects
* domain limitation

### 10. Claim boundaries

Know exactly what you **can** and **cannot** claim.

---

# One Important Correction to Your Current Thesis Report

There are two pieces of terminology I would clean up **before final thesis writing**.

### 1. “4-arm factorial design”

Your experiment is not really a conventional factorial design.

You have multiple experimental conditions/arms, but you are not crossing independent factors in the usual factorial sense.

Safer:

> **four-condition experimental design**

or:

> **multi-condition within-item experimental design**

### 2. “4 × 4 Markovian state migration matrix”

Unless you actually estimate a Markov process or use Markov assumptions, don't call it Markovian.

Use:

> **4 × 4 within-item behavioral state-transition matrix**

or:

> **behavioral migration matrix**

That describes exactly what you did without making an unnecessary modeling claim.

---

# Your Real Goal at Day 30

Do **not** measure success by:

> “I finished 30 days.”

Measure it by this:

> **Can I look at my experiment and explain why every major component exists, what assumption it makes, what evidence supports it, what could invalidate it, and what the result does and does not mean?**

If yes, you are ready to move from **AI-generated research understanding** toward **your own scientific understanding**.

The sequence I recommend is therefore:

**Days 1–6:** understand the LLM
→ **Days 7–11:** understand the VLM
→ **Days 12–14:** understand Qwen2.5-VL
→ **Days 15–19:** understand your experiment
→ **Days 20–24:** understand causal/statistical reasoning
→ **Days 25–27:** attack the thesis
→ **Days 28–30:** reconstruct and defend it.

And importantly, **do not restart literature exploration during these 30 days unless you encounter a specific knowledge gap that requires a paper.** Your immediate bottleneck is understanding, not discovering another topic.
