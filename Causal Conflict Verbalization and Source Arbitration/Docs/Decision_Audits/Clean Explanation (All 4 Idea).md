The report is making one central argument:

> **The four thesis directions were stress-tested against recent work, and the report concludes that the “Trustworthy VLM: Causal Conflict Verbalization” direction has the clearest remaining research question and the lowest execution risk.**

However, there is an important distinction: **this is a decision audit, not proof that the thesis is already validated.** Your exact dataset, papers, runtime estimates, and especially the “100% genuine gap” claim still need independent primary-source verification before you should treat the decision as final. Your broader thesis records explicitly say that a final topic had not previously been established.

---

# 1. First, understand the four ideas

The report compared four possible thesis directions:


| Idea                   | Simple meaning                                                                                                           |
| ------------------------ | -------------------------------------------------------------------------------------------------------------------------- |
| **Multimodal Agents**  | Can an AI decide whether it should zoom, crop, retrieve information, ask a question, or simply answer?                   |
| **Medical Imaging**    | Can a medical AI remain trustworthy when images come from a different camera/source than the training data?              |
| **Federated Learning** | Can multiple hospitals/devices train together while maintaining reliable uncertainty estimates?                          |
| **Trustworthy VLM**    | When image and text disagree, does asking the VLM to explicitly identify the contradiction actually change its decision? |

The report says the first three have significant problems.

The fourth asks a more fundamental question about **how multimodal reasoning actually works**.

---

# 2. The core idea in very simple English

Imagine giving a VLM this:

**Image:** shows `7 + 2`

**Text:** says `7 + 8`

The two sources disagree.

The model has to decide what answer to give.

Now you test two situations.

### Situation A: Ask normally

> “What is the answer?”

Maybe the model chooses the visual information.

### Situation B: Force it to think about the conflict

> “First determine whether the visual and textual information agree or contradict. Explain the contradiction, then answer.”

Now ask:

**Does making the model explicitly recognize the conflict actually change its decision?**

That is the thesis question.

---

# 3. Why this is different from ordinary VLM accuracy research

This is the most important part.

You are **not simply asking:**

> “Does Qwen answer more questions correctly if I give it a better prompt?”

That would be weak.

Instead, you are asking:

> **Does explicitly reasoning about a contradiction causally influence which information the model trusts?**

That is a much more specific question.

The report describes two possible outcomes.

### Outcome 1: Reasoning really helps

The model initially follows the wrong source.

After explicitly identifying the contradiction, it switches to the correct source.

That suggests the intermediate reasoning step can actually influence the final decision.

### Outcome 2: Reasoning does not really control the decision

The model says:

> “The image and text contradict each other.”

It gives a nice explanation.

But then it makes **exactly the same decision it would have made anyway**.

That would suggest that the explanation and the actual decision may be partly disconnected.

In simple terms:

> **The model can talk about the problem without actually using that reasoning to solve the problem.**

That is the phenomenon the report wants to investigate.

---

# 4. What does “post-hoc rationalization” mean?

This phrase sounds complicated but the idea is simple.

Suppose a person chooses **A** first.

Then someone asks:

> “Why did you choose A?”

The person gives a convincing explanation afterward.

The explanation may sound logical, but it does not necessarily mean that the explanation caused the decision.

The report asks whether something similar happens inside multimodal models.

### Possible pattern

```text
Image + Text
     ↓
Model already prefers one modality
     ↓
Decision = A
     ↓
Model generates explanation
     ↓
Explanation sounds logical
```

rather than:

```text
Image + Text
     ↓
Detect contradiction
     ↓
Reason about which evidence is trustworthy
     ↓
Change internal decision
     ↓
Answer = B
```

Your experiment is trying to distinguish these two possibilities.

---

# 5. Why the placebo condition matters

This is probably the most technically important experimental control in the report.

Suppose you compare:

### Baseline

```text
Image + question → answer
```

against:

### Conflict reasoning

```text
Image + question
→ think about contradiction
→ answer
```

Someone can criticize your result:

> “Maybe the second prompt worked simply because the model generated more tokens and therefore had more computation.”

That is a legitimate criticism.

So the report proposes a **neutral placebo condition**.

---

## Three conditions

### A. Direct answer

```text
Look at the inputs.
Give the answer.
```

### B. Neutral thinking

```text
Describe the visual information
and textual information neutrally.
Then answer.
```

### C. Conflict reasoning

```text
Determine whether the visual
and textual information agree.
Explain the contradiction.
Then answer.
```

B and C are deliberately similar in length.

Therefore:

```text
B = extra thinking without conflict reasoning

C = extra thinking + conflict reasoning
```

If C changes the answer more than B, you have stronger evidence that **the content of the reasoning intervention matters**, rather than merely the amount of computation.

This is what the report means by a **length-matched placebo control**.

---

# 6. What is the fourth “Lanham-style prefilling” experiment?

This is more advanced.

Instead of simply asking the model to produce an explanation, you partially provide the beginning of its reasoning.

For example, conceptually:

```text
"The image and text contradict because..."
```

versus

```text
"The image and text agree because..."
```

Then observe what answer follows.

The purpose is to ask:

> **If you force a particular intermediate conclusion, does the model's final decision change?**

This is intended as a stronger test of whether the intermediate reasoning actually influences the answer.

It is based on ideas from chain-of-thought faithfulness research.

---

# 7. Why the report rejects the Multimodal Agent idea

The original agent question was:

> Can an agent learn which action is worth taking, such as zooming, retrieval, clarification, or stopping?

This sounds strong.

But recent work apparently already covers much of that territory.

The report lists examples such as:

* AdaTooler-V
* ToolGate
* CAM-DF
* MED
* Spurious Tool Use

The important lesson is:

> **Changing the name from “tool selection” to “action-value prediction” does not create novelty.**

Your previous research records make the same general point: a thesis must identify what existing work establishes and then isolate the remaining uncertainty rather than treating an existing benchmark or method as a gap.

### Why the agent direction becomes risky

You would potentially need:

* tool environments
* cropping/zooming infrastructure
* retrieval
* action policies
* cost modelling
* agent evaluation
* possibly RL

That means a lot of engineering.

And after all that, a reviewer could say:

> “This is another version of existing active-perception/tool-selection research.”

So the report considers it **too crowded and too engineering-heavy**.

---

# 8. Why Medical Imaging is not considered strong enough

The medical idea sounds practical:

> Train on one image source and test on another.

For example:

```text
Training
ISIC
  ↓
Model
  ↓
Testing
another dermatology dataset
```

Then ask whether confidence calibration still works.

The problem is not that medical imaging is bad.

The problem is that your **scientific question may become secondary to medical-data complications**.

You could spend substantial time dealing with:

* duplicate images
* patient overlap
* different diagnostic labels
* different acquisition conditions
* different annotation standards
* domain shift

Then your final contribution might essentially be:

> “Existing calibration method X behaves this way on medical dataset Y.”

That is potentially useful, but the report argues it is weaker as a **CSE thesis contribution** than a direct question about multimodal reasoning.

Your canonical thesis specification explicitly requires the contribution to remain AI/CSE-heavy and to have direct metrics, ablations, and reproducible baselines.

---

# 9. Why Federated Learning gets rejected

Federated Learning means roughly:

```text
Hospital A ─┐
Hospital B ─┼──→ shared model
Hospital C ─┘
```

without directly combining all their raw data.

The proposed thesis was about whether uncertainty/calibration survives differences between clients.

The report identifies two problems.

### Problem 1: Existing research already addresses much of it

The report claims recent work has already addressed the central conformal-calibration problem.

So you might only be changing something like:

```text
40% client participation
vs.
60% client participation
```

That is more like a parameter study than a new scientific contribution.

### Problem 2: Infrastructure

Real multi-institution datasets may require approval.

Simulating FL introduces:

* client partitioning
* communication
* synchronization
* distributed execution
* non-IID data
* reproducibility issues

That is a lot of complexity for an undergraduate thesis.

---

# 10. Why the Trustworthy VLM idea survives

The report considers this direction different because it is asking about a **mechanism**, not simply an application.

The central question is:

> **When visual and textual evidence conflict, does explicit contradiction reasoning actually control the model's final decision?**

That connects several important areas:

```text
Multimodal models
       +
Conflicting evidence
       +
Reasoning
       +
Faithfulness
       +
Source arbitration
       =
Your research question
```

This fits the frozen parent field of **Multimodal / Vision-Language Learning and Systems**, with trustworthy/reliable VLMs as the primary research lane.

---

# 11. What exactly would you test?

The report proposes four experimental arms.


| Arm                        | What happens                                       | Purpose                               |
| ---------------------------- | ---------------------------------------------------- | --------------------------------------- |
| **1. Direct**              | Answer immediately                                 | Normal baseline                       |
| **2. Neutral reasoning**   | Describe both sources before answering             | Controls for extra computation/tokens |
| **3. Conflict reasoning**  | Explicitly identify and explain contradiction      | Main intervention                     |
| **4. Prefilled reasoning** | Force an intermediate agreement/conflict statement | Stronger causal test                  |

Think of it like an experiment in a laboratory.

You change **one important thing**:

> Does the model explicitly reason about the conflict?

while trying to keep other things similar.

---

# 12. What data would look like?

The proposed dataset contains artificial but mathematically verifiable conflicts.

For example:

### Item

Image:

```text
5 + 4 = ?
```

Text:

```text
The equation is 5 + 9.
```

Ground truth:

```text
9
```

The visual and textual evidence intentionally disagree.

You know which one is correct because the underlying mathematical problem is objectively verifiable.

That is important.

You don't want an experiment where you cannot determine whether the model chose the “right” source.

---

# 13. Why arithmetic is useful

Suppose you create:

```text
Image says: 7 + 3
Text says: 7 + 8
```

The correct answer is objectively:

```text
10
```

There is no need for a human judge to decide whether the answer is correct.

That gives you:

* exact ground truth
* deterministic evaluation
* easy error analysis
* no subjective LLM judge
* easy reproduction

The report considers this much stronger than asking something subjective like:

> “Which source seems more trustworthy?”

---

# 14. Why charts are also proposed

Charts provide another type of evidence conflict.

For example:

**Chart:** sales = 20

**Text:** sales = 35

Then ask:

> “What were the sales?”

Again, the correct answer can be determined from the chart/data construction.

This is useful because you don't want the thesis to work only on arithmetic.

You could test:

```text
Arithmetic
+
Charts
```

and eventually ask:

> Does the phenomenon transfer across task types?

---

# 15. What does “source arbitration” mean?

Very simply:

> **When two sources disagree, which source does the model trust?**

For example:

```text
Image → 10
Text  → 13
```

The model must arbitrate.

It might prefer:

* image
* text
* whichever it normally favors
* neither
* a hallucinated answer

Your thesis is **not necessarily saying which modality should always win**.

Instead, you are studying:

> **Does explicit conflict reasoning change the model's arbitration behavior?**

That distinction is important.

---

# 16. The biggest weakness in the report

I would **not yet accept the sentence “100% genuine & open” as established fact.**

The report itself contains extremely strong language:

> “100% Genuine & Open.”

and:

> “First causal isolation...”

Those are publication-level claims.

But your own research-progress document warns that previous reports sometimes claimed “verified gaps” and later audits overturned them.

So the correct interpretation is:

### Currently

**Strong candidate based on the audit.**

Not:

**Proven novel thesis.**

Those are different things.

---

# 17. Another important weakness: “causal” may be too strong

The report calls the experiment a:

> “causal” test.

You need to be careful here.

If you do:

```text
Prompt A → answer A

Prompt B → answer B
```

you have shown that changing the prompt changes behavior.

That is evidence of a **causal effect of the intervention under the experimental setup**.

But it does **not automatically prove**:

> “We discovered what happens inside the model's neural computation.”

You cannot directly conclude:

> “The model's early cross-modal attention changed.”

unless you actually measure that mechanism.

So a safer thesis claim would initially be:

> **Does explicit conflict verbalization causally affect final answer selection under controlled prompting?**

Then, if stronger evidence supports it, you can discuss implications for reasoning faithfulness.

---

# 18. Another weakness: the placebo has to be genuinely matched

This is critical.

Suppose:

### Neutral condition

> “Describe the image and text.”

### Conflict condition

> “Identify whether they contradict and explain why.”

The second instruction is naturally more informative.

So if it performs better, someone can say:

> “Of course. You explicitly told the model what to look for.”

Therefore, the experimental design needs careful controls.

You need to decide exactly what is being held constant:

* token budget
* number of reasoning steps
* prompt length
* output length
* demonstrations
* answer format
* temperature
* image resolution
* ordering of modalities

This is one of the places where the proposed idea can either become a serious experiment or collapse into a prompt comparison.

---

# 19. The dataset itself is not automatically a contribution

The report says the dataset contains:

> 1,304 arithmetic conflict pairs + 229 chart conflict items + controls.

That is useful.

But don't confuse:

```text
public dataset exists
```

with:

```text
scientific contribution exists
```

Your contribution would come from the **experimental question and controlled analysis**, not merely downloading that dataset.

Your own thesis discovery rules explicitly say that an existing benchmark is a foundation, not automatically the contribution.

---

# 20. The four ideas in one picture

Think of the decision this way:

```text
                         THESIS OPTIONS
                              │
             ┌────────────────┼────────────────┐
             │                │                │
          Agents           Medical            FL
             │              Imaging             │
             ↓                ↓                ↓
        Too crowded      Application-heavy   Infrastructure
        + engineering    + clinical/data     + existing work
             │                │                │
             └────────────────┴────────────────┘
                              ↓
                        Trustworthy VLM
                              │
                              ↓
                  Conflicting image + text
                              │
                              ↓
                Does model detect conflict?
                              │
                              ↓
                 Force explicit reasoning
                              │
                              ↓
                    Does decision change?
                       /             \
                     YES              NO
                      ↓                ↓
               Reasoning has      Explanation may
               decision effect    be disconnected
```

That is the intellectual core of the report.

---

# 21. What the thesis would actually contribute

If you eventually proceed, the contribution is **not**:

> “I improved Qwen's accuracy.”

It would be closer to:

> **A controlled empirical study of whether explicit conflict reasoning changes multimodal source arbitration, separating the effect of conflict-specific reasoning from generic additional computation.**

Potential outputs:

### Contribution A: Experimental protocol

A carefully controlled way of testing conflict reasoning.

### Contribution B: Empirical finding

For example:

```text
Direct:
60% correct

Neutral reasoning:
63%

Conflict reasoning:
78%
```

This would suggest conflict-specific reasoning matters.

Or:

```text
Direct:
60%

Neutral:
64%

Conflict:
64%
```

This would suggest the explicit contradiction reasoning did not meaningfully alter decisions beyond generic additional computation.

### Contribution C: Failure analysis

You could discover patterns such as:

```text
Arithmetic → conflict reasoning helps

Charts → conflict reasoning barely helps

Text-dominant models → strong effect

Vision-dominant models → weak effect
```

That kind of pattern may be more interesting than a single overall accuracy number.

---

# 22. What a successful thesis does NOT require

This is important for reducing confusion.

You do **not** necessarily need to:

* train a new VLM
* build an RL agent
* create a chatbot
* create a RAG system
* build a complicated architecture
* fine-tune a 7B model
* collect thousands of human annotations
* beat every existing benchmark
* invent a new neural network

The proposed experiment is primarily:

```text
Existing VLM
      +
Controlled inputs
      +
Controlled prompts
      +
Multiple conditions
      +
Careful metrics
      +
Statistical analysis
      +
Failure analysis
```

That fits the thesis framework's allowance for rigorous empirical research rather than requiring a new model architecture.

---

# 23. What could kill this thesis?

There are several real failure modes.

### Failure 1: The claimed closest paper already did it

This is the biggest literature risk.

If a 2025/2026 paper already performs:

```text
cross-modal conflict
+
explicit conflict reasoning
+
neutral length-matched control
+
rationale prefilling
+
decision-change analysis
```

then your novelty claim becomes much weaker.

**This must be independently verified.**

---

### Failure 2: The model ignores your reasoning instructions

A 2B model may simply output:

```text
Answer: 10
```

without following the requested structure.

Then your four conditions aren't actually four meaningful interventions.

---

### Failure 3: Extra tokens explain everything

Suppose:

```text
Direct       = 60%
Neutral      = 72%
Conflict     = 73%
```

Then the improvement might simply come from thinking longer.

The conflict-specific effect is tiny.

That would weaken the main hypothesis.

---

### Failure 4: Artificial conflicts are too easy

If every item looks like:

```text
Image: 7 + 3
Text: 7 + 8
```

the model may simply learn the benchmark pattern.

Then you're measuring:

> “Can the model solve arithmetic?”

rather than:

> “Can the model intelligently arbitrate conflicting evidence?”

---

### Failure 5: The model has a fixed modality bias

Suppose Qwen always trusts text.

Then:

```text
Direct → text
Neutral → text
Conflict → text
Prefill → text
```

Your result may be:

> Explicit reasoning does not overcome the existing modality preference.

That is actually scientifically useful, but you need enough variation to demonstrate that it isn't merely a trivial prompt failure.

---

# 24. The most important mental distinction

You should separate these four questions:

### Question 1

**Does the model detect the contradiction?**

```text
Image ≠ Text
       ↓
“There's a conflict.”
```

### Question 2

**Does it know which source is correct?**

```text
Image = truth
Text = corrupted
```

### Question 3

**Does explicit reasoning change its final decision?**

```text
Before reasoning → A
After reasoning  → B
```

### Question 4

**Does the explanation faithfully represent the reason for the decision?**

This is the hardest question.

Your proposed thesis primarily targets **Question 3**, with implications for Question 4.

Do not accidentally claim that you have completely solved Question 4.

---

# 25. Where this sits relative to your previous thesis journey

Your earlier work was largely about:

> **Can a VLM know when its visual evidence is insufficient?**

You explored:

* uncertainty
* calibration
* degraded images
* answerability
* abstention
* visual evidence

and discovered significant overlap with existing research.

Your research map summarizes that progression as:

> VLM/MLLM → reliable answering from visual evidence → uncertainty/grounding/selective prediction → overlap discovered → exact question still unresolved.

The new direction changes the question slightly:

### Old direction

> **“Does the model know when its evidence is insufficient?”**

### New direction

> **“When its evidence conflicts, can explicit reasoning change which evidence it trusts?”**

That is a meaningful conceptual shift.

---

# 26. My plain-English interpretation of the final decision

The report is essentially saying:

> **Stop looking for a completely untouched topic. Instead, find a precise unanswered question inside trustworthy VLM research.**

Among the four investigated areas:

* **Agents:** interesting but increasingly crowded.
* **Medical imaging:** feasible but contribution risks becoming mostly domain-specific benchmark evaluation.
* **Federated learning:** technically expensive and already heavily addressed around the proposed core.
* **Conflict reasoning in VLMs:** potentially a cleaner AI research question with a controlled experiment and a useful negative result.

That is why the report freezes the fourth direction.

But the word **“freeze” should mean “freeze for focused verification,” not “novelty proven forever.”**

---

# 27. What I would consider the actual current status

Based strictly on the supplied material:


| Component                                   | Status                                      |
| --------------------------------------------- | --------------------------------------------- |
| VLM as parent field                         | **Settled**                                 |
| Trustworthy/reliable VLM as major direction | **Strongly established**                    |
| Conflict/source-arbitration problem         | **Promising**                               |
| Exact research question                     | **Well formulated**                         |
| Experimental structure                      | **Promising but provisional**               |
| Dataset readiness                           | **Claimed, needs verification**             |
| Closest-paper analysis                      | **Needs primary-source re-verification**    |
| “100% genuine gap”                        | **Too strong until independently verified** |
| Causal interpretation                       | **Needs careful wording**                   |
| Compute estimate                            | **Needs actual pilot verification**         |
| Final thesis title                          | **Not necessary yet**                       |
| Ready to implement                          | **Not yet**                                 |
| Ready for focused literature verification   | **Yes**                                     |

This is consistent with your thesis-control documents, which distinguish between having a strong research direction and actually having a demonstrated topic, reproduced baselines, and results.

## Bottom line

The report's core idea is **not**:

> “Make VLMs more accurate.”

It is:

> **Give a VLM contradictory visual and textual evidence. Then experimentally test whether forcing it to explicitly recognize and explain that contradiction actually changes its final decision, while controlling for the possibility that it simply benefits from having more thinking tokens.**

That is the part worth understanding and potentially taking forward.

The next sensible step is **not implementation yet**. It is to verify the decisive claims in the report against the actual 2025–2026 primary papers, especially the alleged closest paper, the dataset, and whether the four-arm experiment is genuinely absent from prior work.

Based on the two proposal files and the broader thesis criteria in your canonical context, the two ideas are **both serious research ideas**, but they are very different in what they ask you to prove.

My current choice for you is **Proposal 1: Reasoning Trace Degradation**. It is the safer thesis direction between these two because the central experiment has cleaner controls, more directly measurable outcomes, and does not depend as heavily on correctly mapping visual regions to internal VLM tokens.

However, I would **not freeze either proposal yet without one small feasibility check**, because both proposals contain some assumptions that are stronger than the documents themselves establish.

---

# 1. Proposal 1 — Reasoning Trace Degradation

### Title

> **Decomposing Multimodal Reasoning Trace Degradation: Causal Reasoning vs. Positional and Attention Dilution Artifacts**

## The idea in one sentence

You are asking:

> **When a VLM seems to "forget" the image while thinking for a long time, is it actually forgetting the image, or are we simply measuring an attention effect caused by the sequence becoming longer and the image becoming farther away?**

That is the whole thesis in simple terms.

---

# 2. Imagine a human example

Suppose I show an AI this image:

**Image:** a red car and a blue car.

Question:

> "What color is the car on the left?"

The correct answer is **red**.

Now imagine the model immediately answers:

> Red.

But then we force it to produce 150 reasoning tokens before answering.

Something like:

> "First, I need to identify the objects. The scene contains two vehicles... The question asks about the leftmost vehicle... I should examine..."

Eventually it answers.

The interesting observation from recent VLM research is that **longer reasoning can sometimes make the model use visual evidence less effectively.**

The obvious explanation is:

> "The model is thinking too much and is forgetting the image."

Proposal 1 says:

**Maybe that explanation is wrong.**

---

# 3. The alternative explanation

There are at least two simpler reasons why visual attention might decrease.

### Problem A — Distance

The image tokens appeared early in the sequence.

After generating 150 reasoning tokens, the answer is now much farther away.

So perhaps the model has not "forgotten" anything.

The visual information is simply **farther away in the Transformer sequence**.

This is related to positional encoding/RoPE.

### Problem B — Attention dilution

Imagine attention has 100 units to distribute.

If there are only 20 tokens, the visual tokens can receive a relatively large share.

If there are 200 tokens, the same visual tokens are competing with many more tokens.

So raw visual attention can decrease simply because:

> **There are more tokens competing for attention.**

This is called the **softmax dilution** explanation in the proposal.

---

# 4. Therefore, Proposal 1 asks a very specific question

The proposal sets up two competing explanations:

### H1 — Genuine reasoning-induced degradation

The reasoning itself is damaging visual evidence usage.

In simple English:

> **"Thinking causes the model to lose access to the image."**

### H0 — Measurement/position artifact

The reasoning isn't actually causing the problem.

Instead:

> **"The image only appears less important because we added many tokens and moved the answer farther away."**

This is what makes the idea scientifically interesting.

You aren't simply asking:

> "Does long reasoning hurt VLMs?"

That has already been studied.

You are asking:

> **"Why does it appear to hurt them?"**

---

# 5. How would you test it?

The proposal has four conditions.

Think of them as four experiments using the same question.

### Condition 1 — Answer immediately

Image + question → answer.

This is your normal baseline.

---

### Condition 2 — Make the model reason

Image + question → **150 reasoning tokens** → answer.

If performance/evidence use gets worse, you have reproduced the phenomenon.

---

### Condition 3 — Add 150 neutral tokens

Image + question → **150 irrelevant/neutral tokens** → answer.

This is extremely important.

You deliberately add approximately the same amount of text, but the text isn't reasoning.

If Condition 2 gets worse but Condition 3 doesn't:

> Maybe the **content of reasoning** matters.

If both get worse equally:

> Maybe merely adding tokens causes the problem.

---

### Condition 4 — Move everything by 150 positions

This is the positional/RoPE control.

You put 150 tokens **before** the image/question rather than between the question and answer.

The purpose is:

> "Can we reproduce the degradation simply by moving things to different positions?"

---

# 6. The experiment is basically this

```text
                 Same image + same question
                           │
        ┌──────────────────┼──────────────────┐
        │                  │                  │
        ▼                  ▼                  ▼

   Direct answer       150 reasoning       150 neutral
                         tokens              tokens
        │                  │                  │
        ▼                  ▼                  ▼
     Result A            Result B           Result C

                           +
                
                    Position control
                    150 tokens moved
                    before the input
```

Then you compare the results.

---

# 7. What would the results mean?

### Result 1

Reasoning causes much more degradation than neutral tokens.

That supports:

> **The content of reasoning itself contributes to visual degradation.**

### Result 2

Reasoning and neutral padding cause approximately the same degradation.

That supports:

> **The apparent "visual forgetting" is largely explained by sequence growth/dilution.**

### Result 3

Position shifting alone reproduces the degradation.

That gives evidence that:

> **position/RoPE is an important explanation.**

### Result 4

Visual information remains recoverable inside intermediate representations even though attention decreases.

That would suggest:

> The model hasn't necessarily destroyed the visual information. It may simply fail to use it effectively at the output.

This is a much deeper question than ordinary accuracy comparison.

---

# 8. Why Proposal 1 is attractive for a thesis

The proposal gives you a very clean scientific structure:

**Known phenomenon**

→ visual utilization appears to decline during long reasoning

**Competing explanations**

→ actual reasoning-induced forgetting
vs.
→ position/token-count artifact

**Intervention**

→ reasoning vs neutral padding vs positional control

**Measurement**

→ answer sensitivity + attention + hidden-state information

**Possible negative result**

→ the popular interpretation of "visual forgetting" is partly wrong.

That fits your thesis criteria particularly well because the canonical specification explicitly prioritizes falsifiable competing explanations, structural controls, direct metrics, and useful negative results.

---

# 9. But Proposal 1 has an important difficulty

This is the biggest weakness.

The experiment is **mechanistically technical**.

You need to work with:

* Transformer hidden states
* attention tensors
* visual-token positions
* RoPE positions
* teacher-forced prefixes
* token-level probabilities
* intermediate-layer probing

The proposal specifically requires extracting visual attention and residual representations from Qwen2.5-VL.

So:

**Research idea:** very strong.

**Implementation difficulty:** medium-high.

**Conceptual clarity:** high.

---

# 10. Proposal 2 — Visual Binding IDs

Now the second idea.

### Title

> **Do Latent Visual Binding Identifiers Survive Beyond Synthetic Grids? A Placebo-Controlled Natural-Image Transfer Audit**

This one asks a completely different question.

---

# 11. What is "visual binding"?

Imagine an image containing:

* red car
* blue car

The model needs to understand:

> **red → car #1#1#1#1**

and

> **blue → car #2#2#2#2**

It must connect:

**object location ↔ object identity ↔ attribute**

This connection is called **binding**.

The problem is that when there are multiple similar objects, models can make mistakes.

For example:

> "The blue car is on the left."

when the blue car is actually on the right.

That is a **binding error**.

---

# 12. What did the previous research claim?

The proposal discusses research claiming that VLMs contain something like a hidden internal identifier for an object.

You can think of it as:

> **"This group of visual neurons/tokens represents Object A."**

and another group represents:

> **"Object B."**

The previous work called these things **Grounding IDs / Binding IDs**.

The reported experiment supposedly found that if researchers take internal representations belonging to Object A and insert them into Object B's location, the model's answer can shift toward Object A's attribute.

In very simple terms:

> **Take the internal representation of the red object and put it into the blue object's position → the model starts talking about the red object's attribute.**

The proposal therefore asks:

> **Is this a genuine internal mechanism, or is the intervention simply damaging the model's representation?**

---

# 13. Why this is suspicious

The proposal identifies two major concerns with the earlier work.

### Problem 1 — Synthetic images

The original discovery was demonstrated on very clean artificial scenes.

Think:

```text
┌──────────┬──────────┐
│   RED    │   BLUE   │
│   @      │    #     │
└──────────┴──────────┘
```

These are extremely simple compared with:

* real photographs
* clutter
* overlapping objects
* different lighting
* complicated backgrounds

So the question becomes:

> **Does the discovered mechanism work in real photographs?**

### Problem 2 — No strong placebo

Suppose you replace an object's internal representation with another representation.

The model's answer changes.

Does that prove you transferred the object's identity?

Not necessarily.

Maybe you simply **damaged the model's hidden state**.

So Proposal 2 introduces placebo interventions.

---

# 14. The Proposal 2 experiment

You would take two objects.

For example:

```text
Image:

       RED CAR                 BLUE CAR
          🚗                       🚙
```

Then manipulate the internal representations.

### Arm 1 — Real swap

Take internal representations from the red car and insert them into the blue car's region.

If the model now says something associated with red → interesting.

---

### Arm 2 — Random-noise placebo

Instead of inserting the red-car representation, insert carefully scaled random noise.

If random noise produces the same answer change:

> The "Binding ID" explanation becomes much weaker.

Maybe the intervention simply damaged the representation.

---

### Arm 3 — Background placebo

Insert an irrelevant background representation.

Again:

> Does merely disrupting the target representation cause the model to change its answer?

---

### Arm 4 — Swap objects within the same image

Swap Object 1 and Object 2 internally.

This checks whether the effect is specifically related to object identity rather than arbitrary disruption.

---

# 15. The central comparison

This is the heart of Proposal 2:

```text
Real object representation
          │
          ▼
      Model output
          │
          │
          ├───────────────┐
          │               │
          ▼               ▼
Random noise          Background
          │               │
          ▼               ▼
      Model output     Model output
```

If:

**Real swap → target attribute changes**

but

**Noise → nothing useful happens**

and

**Background → nothing useful happens**

then the evidence for a genuine binding mechanism becomes stronger.

But if all three interventions cause similar disruption:

> The supposed "Binding ID" may simply be an artifact.

---

# 16. Proposal 2's key metric

The proposal uses **Net Directed Target Flip Rate**.

In plain English:

> How often did the target object's attribute change in the *specific direction we predicted*, minus how often unrelated objects were damaged?

So it isn't enough to say:

> "The answer changed."

You want:

> **"The answer changed in exactly the direction predicted by the source object's representation."**

That distinction is important.

---

# 17. What would the results mean?

### Result A

Real activation swap works strongly on natural photographs.

Random noise does not.

Background patches do not.

Non-target objects remain mostly intact.

Then:

> There is evidence that the discovered representation contains genuine object-attribute information that transfers beyond the artificial setup.

### Result B

Real swap works on synthetic grids but fails on natural photographs.

Then:

> The mechanism may be heavily dependent on the synthetic environment.

### Result C

Real swap and random noise cause similar changes.

Then:

> The original effect may largely be destructive perturbation rather than genuine binding transfer.

This would also be scientifically useful.

---

# 18. Proposal 2 is more "mechanistic"

This is important.

Proposal 1 asks:

> **Why does visual evidence appear to decline during reasoning?**

Proposal 2 asks:

> **What is actually encoded inside particular visual representations?**

So Proposal 2 goes deeper into the model.

You would literally manipulate internal neural representations.

That is closer to **mechanistic interpretability**.

---

# 19. But Proposal 2 has a major technical risk

This is the biggest problem I see.

You must correctly perform:

**image bounding box**

↓

**visual patch coordinates**

↓

**Qwen2.5-VL visual tokens**

↓

**Layer-22 residual representation**

↓

**activation replacement**

↓

**generation**

That is considerably more fragile.

The proposal itself requires mapping bounding boxes to Qwen2.5-VL's dynamic visual-token structure, interpolation when source/target regions have different dimensions, and hooking the residual stream at a specific layer.

That is not ordinary VLM inference.

A small mistake in token mapping could invalidate the entire experiment.

---

# 20. Proposal 1 vs Proposal 2


| Factor                         | Proposal 1                                         | Proposal 2                            |
| -------------------------------- | ---------------------------------------------------- | --------------------------------------- |
| Main question                  | Why does visual use decline during long reasoning? | Are "binding IDs" real or artifacts?  |
| Core phenomenon                | Visual forgetting during CoT                       | Object-attribute misbinding           |
| Main intervention              | Reasoning vs neutral tokens vs position            | Internal activation swapping          |
| Main control                   | Length/position-matched placebo                    | Noise/background placebo              |
| Mechanistic depth              | High                                               | **Very high**                         |
| Implementation difficulty      | High                                               | **Very high**                         |
| Dataset dependence             | Moderate                                           | Higher                                |
| Internal model access          | Yes                                                | **Heavy**                             |
| Token-coordinate engineering   | Moderate                                           | **Very high**                         |
| Risk of implementation failure | Medium                                             | **High**                              |
| Negative-result value          | High                                               | High                                  |
| Experimental story             | Very clean                                         | Very interesting but more complicated |
| Undergraduate feasibility      | **Better**                                         | More risky                            |
| Main danger                    | Attention interpretation                           | Activation-patching correctness       |

The canonical context itself currently categorizes Proposal 1 as the first reserve direction and Proposal 2 as the second reserve direction, while the primary locked topic remains causal conflict verbalization/source arbitration.

---

# 21. So which one should you choose?

If the choice is **only between Proposal 1 and Proposal 2**:

## **I would choose Proposal 1.**

Not because Proposal 2 is less scientifically interesting.

Actually, Proposal 2 may be **more exciting mechanistically**.

I would choose Proposal 1 because your undergraduate thesis needs to survive the entire pipeline:

> research question → implementation → controlled experiment → analysis → thesis writing → defense.

Proposal 1 gives you a more reliable path through that pipeline.

### Why?

**1. Cleaner causal comparison**

Reasoning vs neutral padding vs positional control is conceptually easy to explain.

**2. Easier to defend**

Your viva explanation can be:

> "Previous work observed visual degradation during long reasoning. We separated reasoning content from sequence-length and positional effects."

That is straightforward.

**3. Better failure isolation**

If something goes wrong, you have multiple control conditions that help tell you why.

**4. Less dependent on perfect spatial-token engineering**

Proposal 2 depends heavily on correctly translating real-image bounding boxes into internal Qwen visual-token regions.

**5. The negative result is still meaningful**

If neutral padding reproduces the degradation, you have learned something important:

> The apparent "reasoning-induced visual forgetting" may be largely explained by positional/context effects.

That fits your preferred thesis structure very well. The canonical research standard explicitly values a result that remains useful even when the original hypothesis fails.

---

# 22. But there is an even more important point

You originally had the **Causal Conflict Verbalization / Source Arbitration** idea.

That means your real decision is probably:

```text
                 Thesis candidates

                       VLM
                        │
       ┌────────────────┼─────────────────┐
       │                │                 │
       ▼                ▼                 ▼
 Conflict          Proposal 1         Proposal 2
Verbalization      Reasoning           Binding IDs
Source Arbitration Degradation         Natural Transfer
```

From the material currently available, I would rank the **research directions conceptually** as:

### **1. Causal Conflict Verbalization / Source Arbitration**

Primary candidate.

### **2. Proposal 1 — Reasoning Trace Degradation**

Strong reserve.

### **3. Proposal 2 — Binding IDs Natural Transfer**

Interesting but higher implementation risk.

That is **not a claim that #1#1#1#1 is universally "better" science**. It means that for *your stated undergraduate constraints*, the first direction currently offers the strongest combination of question clarity, controllability, and feasibility based on the evidence already collected.

The canonical context explicitly identifies causal conflict verbalization/source arbitration as the locked primary topic, with Proposal 1 and Proposal 2 as reserve proposals.

---

# 23. The simplest way to remember the three

### Conflict Verbalization

> **"If I force the VLM to recognize the conflict, does it actually change which source it trusts?"**

### Proposal 1

> **"When the VLM seems to forget the image while thinking, did reasoning actually cause it, or did adding tokens make it look that way?"**

### Proposal 2

> **"Did researchers really discover an internal object-binding mechanism, or does their activation-swap trick only work on toy images?"**

These are three genuinely different thesis questions.

---

## Thesis-decision comparison

I would treat these as **three different kinds of research questions**, not simply three versions of the same VLM topic:

1. **Conflict Verbalization** → Does explicit contradiction reasoning change *which modality/source the model trusts*?
2. **Proposal 1 — Reasoning Trace Degradation** → Is visual forgetting during long reasoning *actually caused by reasoning*, or by sequence-position/context effects?
3. **Proposal 2 — Binding IDs** → Are reported internal visual-binding representations *genuine transferable mechanisms*, or artifacts of synthetic setups/perturbations?

The table below combines the supplied canonical proposals with a current literature check.

### 1. Core thesis comparison


| Criterion                                   | Conflict Verbalization                                                                    | Proposal 1: Reasoning Trace Degradation                                                  | Proposal 2: Binding IDs                                                        |
| --------------------------------------------- | ------------------------------------------------------------------------------------------- | ------------------------------------------------------------------------------------------ | -------------------------------------------------------------------------------- |
| **Core question**                           | Does explicitly verbalizing a visual/text contradiction causally change source selection? | Does long reasoning itself cause visual degradation, beyond positional/context dilution? | Do localized activation swaps reveal a genuine transferable binding mechanism? |
| **Research type**                           | Behavioral causal intervention / reliability                                              | Controlled causal diagnosis / mechanistic analysis                                       | Mechanistic interpretability / causal activation patching                      |
| **Main failure mode**                       | Model receives conflicting evidence but may arbitrarily favor one source                  | Model appears to "forget" visual evidence during long CoT                                | Model may associate an attribute with the wrong object                         |
| **Scientific question strength**            | **High**                                                                                  | **High**                                                                                 | **High**                                                                       |
| **Novelty risk**                            | **Medium**                                                                                | **Medium–High**                                                                         | **High**                                                                       |
| **Implementation risk**                     | **Low–Medium**                                                                           | **Medium**                                                                               | **Very High**                                                                  |
| **Evaluation complexity**                   | Medium                                                                                    | High                                                                                     | Very high                                                                      |
| **Dependence on fragile internals**         | Low                                                                                       | Medium                                                                                   | **Very high**                                                                  |
| **Easy to explain to examiner**             | **Very easy**                                                                             | Easy–medium                                                                             | Difficult                                                                      |
| **Can produce meaningful negative result?** | **Yes**                                                                                   | **Yes, strongly**                                                                        | **Yes, strongly**                                                              |
| **Undergraduate suitability**               | **Very high**                                                                             | **High**                                                                                 | Medium–low                                                                    |
| **Colab Pro compatibility**                 | **Strong**                                                                                | **Plausible, but needs memory testing**                                                  | **Plausible but fragile**                                                      |
| **Main risk**                               | Intervention may be interpreted as merely better prompting                                | Teacher-forced reasoning/filler may not perfectly isolate the mechanisms                 | Activation mapping/patching may consume the thesis                             |
| **My current status**                       | **PROCEED**                                                                               | **PROCEED / very strong reserve**                                                        | **RESERVE**                                                                    |

---

# 2. What is already occupied?

This is the most important part of the comparison.

### Conflict Verbalization

Recent work has now clearly established that **multimodal conflict and source reliance are real research problems**.

`Which Source Wins?` studies conflicting visual/textual evidence and shows that modality reliance changes depending on task and evidence structure. However, its intervention is **degrading image/text legibility**, not testing whether explicit contradiction verbalization changes the subsequent source decision. ([arXiv][1]https://arxiv.org/abs/2608.17205?utm_source=chatgpt.com)

`CLASH` studies **cross-modal contradiction detection**, including object- and attribute-level contradictions. But its central question is detecting contradictions, rather than testing a sequential:

> conflict → explicit verbalization → source arbitration

mechanism. ([arXiv][2]https://arxiv.org/abs/2511.19199?utm_source=chatgpt.com)

So the potential gap is reasonably well-defined:

> **Existing work studies whether conflict exists and which modality wins; your proposed intervention asks whether explicitly representing the conflict changes the arbitration decision.**

That is a cleaner distinction than simply saying "nobody studied conflict."

**Novelty confidence: Medium–High**, subject to a deeper full-text search for papers using chain-of-thought/rationale prompting specifically as a causal intervention for multimodal source arbitration.

---

# 3. Proposal 1 has become more interesting after the 2026 literature

Proposal 1 is supported by several very recent papers.

`More Thinking, Less Seeing?` reports that longer multimodal reasoning can reduce visual grounding and introduces RH-AUC/RH-Bench to measure this trade-off. ([Hugging Face][3]https://huggingface.co/papers/2505.21523?utm_source=chatgpt.com)

More importantly, `Seeing or Knowing?` (July 2026) argues that, for the coarse attributes it studies, **visual information can remain represented even when the model fails to use it**. It explicitly separates:

> visual information being available

from

> the model actually using that information.

It also uses the `WhatIfVis` benchmark and activation interventions. ([arXiv][4]https://arxiv.org/abs/2607.26326?utm_source=chatgpt.com)

`Remember-R1` subsequently treats long-context visual forgetting as a real phenomenon and attempts to mitigate it through reinforcement learning. ([arXiv][5]https://arxiv.org/abs/2608.01314?utm_source=chatgpt.com)

That makes Proposal 1's question more precise:

> **If visual utilization falls during long reasoning, how much of that decline is actually attributable to the reasoning tokens themselves, rather than simply adding tokens and changing positional/context conditions?**

This is a strong research question because a negative result is still useful.

For example:

**Reasoning → visual degradation**

might actually turn out to be:

**More tokens → positional/context effects → apparent visual degradation.**

That is a meaningful distinction.

### But there is a serious caveat

The proposal's strongest claim is causal:

> "reasoning tokens cause true visual forgetting."

Your experiment therefore has to isolate **reasoning content** from **token count, position, context length, and generation dynamics** extremely carefully.

The proposed four-arm design is directionally good, but I would **not yet call the proposed controls sufficient without a full implementation-level audit**.

**Novelty confidence: Medium–High**

**Scientific value: High**

**Execution risk: Medium**

---

# 4. Proposal 2 has the strongest mechanistic flavor—but the largest failure surface

The literature is already substantial here.

`Investigating Mechanisms for In-Context Vision Language Binding` explicitly investigates Binding IDs using a **synthetic dataset/task** and reports distinct binding representations between image objects and textual references. ([arXiv][6]https://arxiv.org/abs/2505.22200?utm_source=chatgpt.com)

`Uncovering Grounding IDs` goes further, proposing Grounding IDs and using activation swapping, probing, similarity analysis, and natural-image interventions. Its official repository also provides the research code. ([arXiv][7]https://arxiv.org/abs/2509.24072?utm_source=chatgpt.com)

Then `InstaBind-Lite/DSCAM` makes the problem itself more concrete: models can recognize the correct objects and attributes but assign an attribute to the **wrong same-class instance**. The benchmark contains 524 images and 9,580 deterministically evaluated questions. ([arXiv][8]https://arxiv.org/abs/2608.16805?utm_source=chatgpt.com)

This creates a very good research space.

But it also creates the main problem:

### The thesis would depend on reproducing somebody else's internal intervention correctly.

You need to get all of these right:

* visual-token indexing;
* image resizing/dynamic resolution;
* patch-to-object correspondence;
* residual-stream hook location;
* source/target activation alignment;
* layer selection;
* activation normalization;
* placebo construction;
* generation stability;
* non-target preservation;
* natural-image transfer.

A mistake in any one of these can produce an apparently interesting result that is actually an intervention artifact.

That makes Proposal 2 scientifically ambitious but **engineering-fragile for a 3–4 month undergraduate thesis**.

**Novelty confidence: High if the exact natural-image placebo experiment is genuinely absent.**

**Execution confidence: Medium–Low.**

---

# 5. The most important distinction: what happens if the hypothesis fails?

This is where I would differentiate the candidates.


| Outcome                                                 | Conflict Verbalization            | Proposal 1                               | Proposal 2                                  |
| --------------------------------------------------------- | ----------------------------------- | ------------------------------------------ | --------------------------------------------- |
| Hypothesis supported                                    | Verbalization changes arbitration | Reasoning causes genuine degradation     | Binding mechanism transfers                 |
| Hypothesis rejected                                     | Verbalization doesn't matter      | Degradation mostly positional/dilutional | Binding effect is artifact/non-transferable |
| Scientific value of negative result                     | **Moderate–High**                | **High**                                 | **High**                                    |
| Ease of interpreting negative result                    | **High**                          | **High–Medium**                         | **Low–Medium**                             |
| Chance negative result becomes "implementation failure" | Low                               | Medium                                   | **High**                                    |

This is important for an undergraduate thesis.

A negative Proposal 2 result could mean:

> "Binding IDs do not transfer."

But it could also mean:

> "Our token mapping was wrong."

That ambiguity is dangerous.

A negative Proposal 1 result is easier to interpret:

> reasoning ≈ position-matched filler

therefore the original "reasoning causes forgetting" interpretation is weakened.

---

# 6. Causal strength

I would distinguish **causal behavioral evidence** from **mechanistic causal evidence**.


|                                           | Conflict Verbalization |       Proposal 1 |    Proposal 2 |
| ------------------------------------------- | -----------------------: | -----------------: | --------------: |
| Manipulates model input                   |                    Yes |              Yes |           Yes |
| Has explicit control/placebo              |                **Yes** |          **Yes** |       **Yes** |
| Tests alternative explanation             |             **Strong** |  **Very strong** |    **Strong** |
| Requires internal activation intervention |                     No | Optional/partial |       **Yes** |
| Causal interpretation complexity          |                 Medium | **Medium–High** | **Very High** |
| Risk of overclaiming internal mechanism   |                 Medium |           Medium |      **High** |

One terminology correction is important:

If Conflict Verbalization changes the output after prompting, you can legitimately say:

> **"The intervention causally changes model behavior under this experimental manipulation."**

You should **not** automatically say:

> "We proved the model's internal reasoning mechanism."

That distinction will matter in the thesis defense.

---

# 7. Data and experimental burden


| Requirement                  | Conflict Verbalization | Proposal 1           | Proposal 2                                                 |
| ------------------------------ | ------------------------ | ---------------------- | ------------------------------------------------------------ |
| Existing public data         | Likely                 | **Yes — WhatIfVis** | **Yes — InstaBind-Lite/DSCAM + synthetic reconstruction** |
| New annotation               | Low                    | Low                  | Low–Medium                                                |
| Dataset construction         | Moderate               | Moderate             | **Moderate–High**                                         |
| Model modification           | None/low               | Low–medium          | **High**                                                   |
| Activation hooks             | No                     | Possibly             | **Essential**                                              |
| Special visual-token mapping | No                     | Some                 | **Essential**                                              |
| Multiple placebo conditions  | **Essential**          | **Essential**        | **Essential**                                              |
| Reproduction dependency      | Medium                 | Medium               | **High**                                                   |

`WhatIfVis` is particularly attractive for Proposal 1 because the 2026 paper explicitly describes it as a controlled benchmark for visual-versus-prior sensitivity and reports that visual evidence remains reconstructible in final-layer representations. ([arXiv][4]https://arxiv.org/abs/2607.26326?utm_source=chatgpt.com)

---

# 8. Compute risk

I would **not trust the exact VRAM numbers in the canonical proposals until they are experimentally profiled**.

Still, qualitatively:

### Conflict Verbalization

**Lowest compute risk.**

You mainly need repeated inference under different prompts.

### Proposal 1

**Moderate compute risk.**

The danger isn't simply model size. It is the combination of:

* long sequences;
* teacher forcing;
* hidden-state extraction;
* multiple layers;
* attention analysis;
* repeated conditions.

The proposal's claim that peak VRAM stays below ~11.5 GB is **a proposal estimate, not yet an experimentally verified fact**.

### Proposal 2

**Moderate GPU memory + high engineering risk.**

Activation patching itself isn't necessarily enormous, but repeatedly capturing and manipulating intermediate visual representations can become expensive and brittle.

---

# 9. Thesis contribution type

This is perhaps the clearest way to understand them.

### Conflict Verbalization

> **"Does making the contradiction explicit actually improve/change source arbitration?"**

Contribution type:

**Behavioral causal evidence about multimodal decision-making.**

---

### Proposal 1

> **"Is apparent visual forgetting really caused by reasoning, or are we confusing reasoning with sequence/context effects?"**

Contribution type:

**Causal decomposition of an existing MLLM failure phenomenon.**

---

### Proposal 2

> **"Are claimed internal visual-binding representations genuinely transferable, or are they artifacts of the experimental setup?"**

Contribution type:

**Mechanistic audit / replication + adversarial generalization test.**

---

# 10. My decision matrix

I would use **qualitative categories rather than fake numerical scores**, because we have not yet completed the full paper-by-paper audit needed to justify precise numerical scoring.


| Dimension                      | Conflict Verbalization | Proposal 1          | Proposal 2    |
| -------------------------------- | ------------------------ | --------------------- | --------------- |
| Research question              | **Excellent**          | **Excellent**       | **Excellent** |
| Gap clarity                    | **Strong**             | **Strong**          | Strong        |
| Current literature support     | **Strong**             | **Very strong**     | **Strong**    |
| Novelty confidence             | **Medium–High**       | **Medium–High**    | **High**      |
| Experimental cleanliness       | **Very strong**        | **Strong**          | Medium        |
| Control design                 | **Very strong**        | **Very strong**     | **Strong**    |
| Implementation simplicity      | **Strongest**          | Medium              | Weakest       |
| Mechanistic depth              | Medium                 | **High**            | **Very high** |
| Interpretability of results    | **High**               | **High**            | Medium        |
| Failure/negative-result value  | High                   | **Very high**       | **Very high** |
| Reproduction dependency        | Low–medium            | Medium              | **High**      |
| Colab feasibility              | **Strong**             | Strong–conditional | Conditional   |
| 3–4 month feasibility         | **Strong**             | **Strong**          | Risky         |
| Defense/explanation difficulty | **Low–medium**        | Medium              | **High**      |
| Overall thesis risk            | **Low–medium**        | Medium              | **High**      |

---

# 11. Current decision

### **1. Conflict Verbalization — PROCEED TO PILOT**

This currently gives the best combination of:

**clear question + causal controls + manageable implementation + interpretable results + meaningful negative outcome.**

The important thing is that the contribution is **not**:

> "Adding chain-of-thought makes VLMs better."

It is much narrower:

> **When multimodal evidence conflicts, does explicitly verbalizing the contradiction causally change the model's source-arbitration decision, beyond the effect of simply adding more tokens?**

That is a thesis-sized question.

---

### **2. Proposal 1 — PROCEED TO PILOT / VERY STRONG RESERVE**

This is the candidate I would keep **closest behind Conflict Verbalization**.

In fact, the recent `Seeing or Knowing?` work makes the conceptual motivation stronger: it explicitly distinguishes preservation of visual information from its downstream utilization. ([arXiv][4]https://arxiv.org/abs/2607.26326?utm_source=chatgpt.com)

Proposal 1 then asks an even more specific question about what happens when the reasoning trace becomes long.

Its biggest advantage is that **both positive and negative outcomes are scientifically useful**.

Its biggest weakness is experimental control complexity.

---

### **3. Proposal 2 — RESERVE**

Not because the research question is weak.

The opposite: **the scientific question is arguably the most mechanistic of the three.**

The problem is that the thesis can easily turn into:

> "I spent most of the semester getting activation patching to work."

The existing literature already has Binding IDs/Grounding IDs and natural-image binding diagnostics, so your novelty has to come from the **specific adversarial placebo-controlled transfer test**, not from merely studying binding. ([arXiv][7]https://arxiv.org/abs/2509.24072?utm_source=chatgpt.com)

That makes the burden of proof higher.

---

# 12. The decision tree I would use

```text
                         THREE CANDIDATES
                               │
              ┌────────────────┼────────────────┐
              │                │                │
       Conflict Verbal.   Proposal 1       Proposal 2
              │                │                │
       Behavioral causal   Causal diagnosis  Mechanistic
          intervention       of forgetting      audit
              │                │                │
        Lower risk          Medium risk       High risk
              │                │                │
          ┌───┴───┐       ┌────┴────┐      ┌────┴────┐
          │       │       │         │      │         │
       strong   null    strong     null   transfer   artifact
          │       │       │         │      │         │
        useful   useful  useful    useful  useful    useful
```

The key point is that **none of the three depends on achieving a new state-of-the-art score**. That fits your thesis-selection criteria unusually well.

## One thing I would NOT do yet

I would **not freeze the final title yet**.

The three questions are sufficiently different that the better next step is to freeze the **research question + experimental contrast** first. The title should emerge from that.

### Current evidence-based status

**Conflict Verbalization > Proposal 1 > Proposal 2 for undergraduate thesis risk/feasibility.**

That ordering is **not a scientific importance ranking**. It is a thesis-decision assessment under your constraints.


## Proposal 3 in plain English

**Proposal 3 is basically asking:**

> **When a VLM correctly identifies a Bengali cultural object, did it actually understand the image, or did it already know the answer from the text/question and barely use the image?**

And then it asks a second question:

> **If we use "how much the model relied on the image" as a confidence/reliability signal, does that actually help us decide which answers are trustworthy?**

That is the core of the entire proposal.

---

# 1. The problem in one simple example

Imagine you show a VLM this picture:

> A traditional Bengali dish of **Shorshe Ilish**.

And ask:

> "Which dish is shown?"

The model answers:

> **A. Shorshe Ilish** — 95% confidence.

At first glance, this looks excellent.

But there are two very different possibilities.

### Case A — The model actually looked at the image

It sees:

* the fish,
* mustard-based preparation,
* presentation,
* other visual characteristics,

and concludes:

> "This is Shorshe Ilish."

That is a **visually grounded correct answer**.

### Case B — The model didn't really need the image

The Bengali question itself contains strong textual clues.

The language model may already have learned:

> Bengali food + this type of question + these options → Shorshe Ilish.

It might give:

> **A. Shorshe Ilish — 95%**

even if you remove the image.

That is a **correct but ungrounded answer**.

The answer is correct, but the model did not necessarily get it from the visual evidence.

---

# 2. Why does that matter?

Because a lot of modern VLM reliability research assumes something roughly like:

> **If the model isn't using the image, its answer is probably hallucinated or unreliable.**

So researchers develop methods that measure:

> "How sensitive is the model's answer to the image?"

If the model barely changes when the image disappears, they may consider that answer suspicious.

That works reasonably naturally for something like:

> Image: a dog
> Question: "What animal is shown?"

If the model answers "dog" even after removing the image, that's suspicious.

But Bengali cultural questions create a potentially different situation.

The model might know:

> "Nakshi Kantha"

from language training even without seeing the actual image.

So you could have:

**No visual evidence → correct answer**

That creates the unusual situation:

> **Correctness ≠ visual grounding**

And that is what Proposal 3 wants to investigate.

---

# 3. The central idea: "correct but ungrounded"

This is the most important concept in the proposal.

Suppose there are 100 questions.

The model gets 70 correct.

Now you remove the images.

Suppose it still gets 55 correct.

That tells us something interesting.

A large portion of its correct answers may have come from its **language/world knowledge**, rather than visual recognition.

The proposal calls attention to this phenomenon as:

> **Correct-but-Ungrounded**

Meaning:

**The answer is correct, but the model did not need/use the visual evidence to produce it.**

---

# 4. Why Bengali culture is being used

The proposal argues that cultural objects can create an unusual imbalance between the two modalities.

For example:


| Information       | Possible situation                                                                       |
| ------------------- | ------------------------------------------------------------------------------------------ |
| Textual knowledge | Model may have seen "Nakshi Kantha", "Pitha", "Shorshe Ilish", etc. many times online    |
| Visual knowledge  | Much fewer/highly varied visual examples may have been available during pretraining      |
| Result            | Model may know the*name/concept* better than it can recognize the actual visual evidence |

The proposal calls this:

> **Asymmetric Cross-Modal Pretraining Representation**

In simple English:

**The model may have learned more about a cultural concept from text than from images.**

So Bengali cultural data becomes a useful stress test for visual-grounding methods.

---

# 5. What exactly is the research question?

The proposal's formal question is complicated, but in plain English:

> **When a VLM answers Bengali cultural questions correctly, does it actually need the image?**

And then:

> **If visual reliance is used to decide whether an answer is trustworthy, does that method still work for Bengali cultural questions?**

There are two possible outcomes.

---

## Outcome A — Visual grounding still works

The model genuinely needs visual information.

For example:

```text
Image present:
95% → Shorshe Ilish

Image removed:
30% → Shorshe Ilish
```

The answer depends strongly on the image.

Then visual sensitivity is useful for identifying reliable answers.

This corresponds roughly to **H1**.

---

## Outcome B — Cultural knowledge dominates

The model already knows the answer from language.

```text
Image present:
95% → Shorshe Ilish

Image removed:
91% → Shorshe Ilish
```

The model barely cares about the image.

Yet the answer is still correct.

That means:

> low visual reliance does NOT necessarily mean incorrectness.

This corresponds roughly to **H0**, the proposal's "cultural decoupling" idea.

---

# 6. The experiment is actually quite simple

The proposal uses **four conditions**.

Think of them as four different versions of the same question.

### Condition 1 — Normal VLM

Give the model:

**Image + Bengali question + answer options**

Example:

> [Image]
> Which traditional item is shown?
> A. X
> B. Shorshe Ilish
> C. Y
> D. Z

This gives the normal baseline.

---

### Condition 2 — Remove the image

Now give:

> [Black image]
> Same question
> Same options

The model still receives the text.

This asks:

> **Can the language model answer without seeing anything?**

This is extremely important.

If the model still answers correctly, that suggests textual knowledge may be enough.

---

### Condition 3 — Scramble the image

Instead of deleting the image, break its spatial structure.

Imagine this:

```text
Original:

┌─────────────┐
│   person    │
│      ↓      │
│   object    │
└─────────────┘

Scrambled:

┌─────────────┐
│ ↑   object  │
│ background  │
│   person    │
└─────────────┘
```

The same visual pieces are still present, but their spatial arrangement is destroyed.

This helps distinguish:

> "The model uses actual visual structure"

from:

> "The model just uses colors/background/texture."

---

### Condition 4 — Text-only LLM

Now remove the vision system entirely.

Give the underlying language model:

> Bengali question + answer options

No image.

This is a stronger test of:

> **How much can the language model know without vision at all?**

So the four conditions are essentially:

```text
1. Image + Text
       ↓
2. Blank Image + Text
       ↓
3. Scrambled Image + Text
       ↓
4. Text Only
```

---

# 7. What would the researchers learn?

Suppose we get this:


| Condition              | Accuracy |
| ------------------------ | ---------: |
| Image + text           |      80% |
| Blank image + text     |      72% |
| Scrambled image + text |      68% |
| Text-only              |      70% |

That would be interesting.

It would suggest the model gets substantial performance from language knowledge, while the image provides some additional information.

But imagine:


| Condition              | Accuracy |
| ------------------------ | ---------: |
| Image + text           |      80% |
| Blank image + text     |      79% |
| Scrambled image + text |      78% |
| Text-only              |      77% |

Then the image contributes surprisingly little.

The model may mostly be answering from its language knowledge.

---

# 8. The proposal's main metric: MRI

The report introduces:

> **Modality Reliance Index (MRI)**

Don't worry about the equation initially.

Conceptually, MRI asks:

> **How much did the model's confidence depend on the image?**

For example:

### Strong visual dependence

```text
With image:     95%
Without image:  20%

MRI → high
```

The model really needed the image.

### Weak visual dependence

```text
With image:     95%
Without image:  93%

MRI → near zero
```

The model barely needed the image.

So MRI gives each prediction a rough:

> **"How visually grounded was this answer?"**

measurement.

---

# 9. The most interesting measurement: Correct-but-Ungrounded Disparity

The proposal then asks:

> Among the answers that were correct, how many had almost no visual dependence?

For example:

```text
100 correct answers

70 strongly used image
30 barely used image
```

Then:

> 30% of correct answers were correct-but-ungrounded.

The report calls this:

**δ_CUG**

You can think of it simply as:

> **"How often is the model correct even though it doesn't really need the image?"**

---

# 10. Then comes the second half of the thesis

This is where Proposal 3 becomes more than just:

> "Does the model look at the image?"

It asks whether **visual grounding can be used for selective prediction**.

Selective prediction means:

> **The model is allowed to say "I don't trust this answer" instead of answering everything.**

For example:

```text
Question 1 → Answer confidently
Question 2 → Answer confidently
Question 3 → ABSTAIN
Question 4 → Answer confidently
Question 5 → ABSTAIN
```

The goal is:

> When the model answers, can we make the remaining answers safer?

---

# 11. Why visual grounding could cause a problem

Suppose a system uses:

> "Low visual reliance = suspicious answer."

That sounds reasonable.

Now consider:

```text
Question:
What is this Bengali cultural object?

Correct answer:
Nakshi Kantha

Visual reliance:
very low

Reason:
The model already knew the concept from language.
```

A visual-grounding-based system might say:

> "Low visual reliance → reject this answer."

But the answer was actually correct.

So the reliability system could accidentally throw away **correct answers**.

That's the proposal's:

> **Evidence-Order Trap**

In plain English:

> **A reliability method designed to protect against ungrounded answers may accidentally punish correct cultural answers that happen to be obtainable from language knowledge.**

---

# 12. What does "selective prediction" test?

The proposal compares several ways of deciding:

> **Which answers should we trust?**

### Method 1 — Raw confidence

"If the model says 95%, trust it."

### Method 2 — Temperature-calibrated confidence

Adjust the model's confidence to make its probabilities better calibrated.

### Method 3 — Visual grounding score

"If the answer depends strongly on the image, trust it more."

### Method 4 — Hidden-state probe

Use internal representations to estimate whether the answer is grounded.

Then compare:

> **Which method is actually better at separating reliable answers from unreliable ones?**

---

# 13. AUGRC in simple English

The proposal uses:

> **AUGRC — Area Under the Generalized Risk-Coverage Curve**

You don't need to memorize the equation right now.

Conceptually, imagine you tell the system:

### Very strict

> "Only give me answers you're extremely confident about."

Maybe:

```text
Coverage: 20%
Error: 1%
```

### Less strict

> "Give me more answers."

Maybe:

```text
Coverage: 60%
Error: 5%
```

### Very permissive

```text
Coverage: 95%
Error: 20%
```

The curve tells you how well the confidence/selection method behaves as you change how many answers it is willing to provide.

**Lower risk at the same coverage is better.**

The proposal wants to know:

> Is visual-grounding confidence actually better than ordinary model confidence?

---

# 14. The entire thesis can therefore be reduced to this diagram

```text
                 Bengali cultural image
                         +
                    Bengali question
                         │
                         ▼
                       VLM
                         │
              ┌──────────┴──────────┐
              │                     │
         Correct answer       Wrong answer
              │
              ▼
       Did it use the image?
          /          \
        YES           NO
         │             │
   Grounded        Correct but
    correct        ungrounded
                       │
                       ▼
              Does visual-grounding
              confidence still work?
                       │
                ┌──────┴──────┐
                │             │
              YES            NO
                │             │
        grounding is     cultural language
        useful for       priors break the
        reliability      assumption
```

That is Proposal 3.

---

# 15. What makes Proposal 3 different from the other two?

This is important given your three-candidate comparison.

### Conflict Verbalization

Asks:

> **"When sources disagree, can explicit contradiction reasoning change which source the VLM trusts?"**

Focus:

**source arbitration**

---

### Proposal 1

Asks:

> **"When reasoning gets long, does the model genuinely lose visual information, or does it only appear to because of positional/context effects?"**

Focus:

**reasoning-induced visual degradation**

---

### Proposal 2

Asks:

> **"Are the internal representations claimed to encode visual binding actually genuine and transferable?"**

Focus:

**internal visual-binding mechanism**

---

### Proposal 3

Asks:

> **"Can a model be correct without using the image, and does that break visual-grounding-based reliability methods?"**

Focus:

**visual reliance vs correctness**

So Proposal 3 is much closer to your earlier **trustworthy VLM / calibration / selective prediction** research direction.

---

# 16. Why Proposal 3 is potentially interesting

The strongest part is **not** simply:

> "Bengali VLMs don't look at images."

That would be too narrow.

The stronger research question is:

> **Does a reliability assumption developed primarily around visual hallucination remain valid when a model has strong textual knowledge but weak visual knowledge of culturally localized concepts?**

That is much more general.

Bengali culture becomes the **stress-test environment**, not necessarily the entire scientific contribution.

---

# 17. But there are several important weaknesses in this proposal

This is where I would be cautious.

### Weakness 1 — Some claims are stronger than the experiment automatically proves

For example:

> "The model answered correctly because of textual knowledge."

A blank-image result alone does **not prove** that.

It shows:

> The model can produce the correct answer without the original visual information.

That is evidence for language-prior contribution, but not direct proof of the exact internal causal mechanism.

The text-only control helps, but even that doesn't completely establish *why* the model knew the answer.

So the thesis should use careful wording:

**"consistent with language-prior-driven prediction"**

rather than automatically:

**"proves the model used textual memory."**

---

# 18. Weakness 2 — The proposed thresholds look somewhat arbitrary

The report contains thresholds such as:

* MRI < 0.10
* δ_CUG > 30% or 35%
* ΔAUGRC > 0.02
* ΔAUGRC > 0.05
* p < 0.001
* C@5% ≥ 2.5× baseline

These are very specific.

But the report itself does not establish from the supplied text why those exact thresholds are scientifically justified.

For example:

> Why exactly is 10% MRI the boundary between grounded and ungrounded?

That needs justification or should be treated as an analysis threshold rather than a fundamental definition.

---

# 19. Weakness 3 — "Causal contribution" needs careful language

The proposal calls MRI a measure of:

> "normalized causal contribution of the image."

But comparing:

```text
image present
vs.
blank image
```

is a **causal intervention on the input**, which is useful.

However, it does not mean MRI perfectly measures the model's internal causal reasoning.

It measures:

> **output sensitivity to removing the image.**

That is a much safer interpretation.

---

# 20. Weakness 4 — Proposal 3 may be more complicated than it first appears

At first it sounds simple:

> Original vs blank image.

But the full thesis actually combines:

1. cultural VQA;
2. multimodal inference;
3. image ablation;
4. image scrambling;
5. text-only controls;
6. confidence calibration;
7. selective prediction;
8. risk-coverage analysis;
9. hidden-state probing;
10. potentially multiple VLM architectures.

That's a lot.

The proposal says:

> **500 samples, zero training, approximately 40 minutes on a T4.**

Those are **execution estimates from the proposal**, not verified measurements. I would not freeze those numbers before actually checking the dataset/model interfaces and inference pipeline.

---

# 21. The biggest conceptual question for Proposal 3

There is one question I would investigate before treating this as a final thesis candidate:

> **Is the "correct-but-ungrounded cultural prediction" phenomenon actually large and systematic enough to justify a thesis?**

Because everything depends on this.

If you run the basic experiment and find:

```text
Correct answers:
80%

Correct + low visual reliance:
4%
```

then the proposed cultural decoupling phenomenon is weak.

But if you find:

```text
Correct answers:
80%

Correct + low visual reliance:
35–50%
```

then the central idea becomes much more compelling.

This is why the proposal's **K1-style early diagnostic** is valuable.

---

# 22. What I would understand as the thesis contribution

If the experiment succeeds, the contribution is **not**:

> "I built a Bengali VLM."

And it is not:

> "Qwen is bad at Bengali."

Instead, it would be something like:

> **We show that visual-grounding-based confidence signals can behave differently under cultural distribution shift because correctness and visual reliance can become partially decoupled.**

That is a much stronger scientific contribution.

And if the effect does **not** appear?

You could instead conclude:

> **Visual reliance remains a useful reliability signal even in the tested Bengali cultural setting.**

That is still a useful empirical result, provided the experiment is sufficiently controlled.

---

# 23. One-sentence explanation

If you need to explain Proposal 3 to your supervisor:

> **"I want to test whether VLMs can correctly answer Bengali cultural questions from language knowledge without actually using the image, and whether that makes existing visual-grounding-based confidence and abstention methods unreliable."**

That is the proposal in its simplest form.

### How I currently see it

Compared with the other two proposals:

* **Conflict Verbalization** → simpler causal behavioral question.
* **Proposal 1** → deeper question about long-reasoning visual degradation.
* **Proposal 2** → deepest internal-mechanism question but highest implementation risk.
* **Proposal 3** → strong connection to **trustworthy VLMs, calibration, selective prediction, and Bengali cultural evaluation**, but its central empirical phenomenon needs to be verified carefully before committing.
