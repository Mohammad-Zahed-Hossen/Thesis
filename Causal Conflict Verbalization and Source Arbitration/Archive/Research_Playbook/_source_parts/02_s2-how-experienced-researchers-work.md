---

## 2. How experienced researchers actually work

### 2.1 The unit of work is a decision, not a paper read

Experienced researchers rarely work by "reading the literature until an idea appears." They work in short cycles whose output is a **decision**: continue, narrow, pivot, pilot, or kill. A day of work that ends with "I now know that two of my three explanations are indistinguishable with the data I have" is a successful day. **[L3]**

A realistic senior-style week looks like this:

| Day | Activity | Output |
|---|---|---|
| 1 | Orient: find the 5–10 papers that define the area, skim only | A one-page map, not notes |
| 2 | Trace the strongest claim to its evidence and its controls | A list of assumptions and missing controls |
| 3 | Attack: search for the closest existing experiment and for contradicting results | A closest-work table and one candidate question |
| 4 | Scope the minimum experiment; check data/model/logistics reality | A one-page experiment sketch, or a kill |
| 5 | Run or simulate a 10–30 item pilot | Evidence that either strengthens or destroys the candidate |

This cadence is not a rule; it is an illustration of the ratio that matters: **searching is always in service of a decision.** **[L1, L3]**

### 2.2 They think in predictions, not topics

Weak: "This thesis will study reasoning in multimodal models."

Stronger: "If explicit conflict verbalization changes which source a model's reasoning is about, then a length-matched neutral deliberation prompt — same instruction, same output budget, no conflict language — should reproduce the same shift. If both prompts shift behavior identically, the phenomenon is deliberation or length, not conflict verbalization."

The strong version contains, in one sentence:

- the manipulation (conflict language present/absent);
- the matched control (neutral deliberation at equal length);
- the measurement (which source the reasoning follows);
- and the failure interpretation (identical shift ⇒ the construct of interest is not isolated).

You performed a version of this reasoning in the pre-freeze pilot when you discovered that the neutral placebo averaged 61.2 tokens while the direct arm averaged 3.4, and concluded that the control was not actually matched. **[L2]** That is senior behavior: the control was inspected as an object of study, not trusted by its name.

### 2.3 They keep three ledgers

- **Claim ledger:** what is known, what is asserted, what is measured, and what is merely inferred — kept separate.
- **Decision ledger:** the exact evidence that would make you continue, narrow, pivot, pilot, freeze, or kill.
- **Evidence ledger:** the specific table, figure, script, seed, or primary source behind every important belief.

The workspace demonstrates why. In the cross-modal project, the archived reports repeatedly described "visual capture" and "causal arbitration." But the primary table shows the *direct* baseline follows the **text** problem 85.5% of the time and the image problem only 13.8%, while the *neutral placebo* prompt inverts this to 89.5% image. **[L2]** Two claims therefore need to be separated:

1. There is an extremely large effect of prompt framing on which problem the model engages. (Strongly supported by the recorded data.)
2. There is an entrenched *visual* modality preference in the model. (Not supported by the direct baseline in that run; it is suggested only under a specific neutral-descriptive prompt.)

A claim ledger catches that conflated pair in minutes.

### 2.4 What "senior" actually means operationally

Seniority, for these purposes, is the ability to:

- notice a hidden assumption quickly (e.g., "the model *selects* an answer" when it may *compute* one);
- choose the experiment with the highest information per unit of effort;
- distinguish claim, mechanism, and measurement;
- discard sunk cost without drama;
- write a complicated or negative result accurately; and
- stop reading when reading no longer changes the next decision.

### 2.5 They treat "interesting" as a testable claim

"Interesting" is not a property of a topic. It is a relation between a result and a prior belief. A result is interesting when it is:

- **surprising relative to a stated prediction** (not just surprising to you);
- **robust across plausible controls**; and
- **consequential** — it changes what someone would build, evaluate, or claim.

This is the practical content of [L1] falsifiability: state the prediction first, then let the data be surprising.
