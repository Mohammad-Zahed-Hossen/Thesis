I'll read the three uploaded reports first, since their contents aren't in my context yet.The repo cloned. I'll check the data schema, the prompts, and how ground truth is defined for a conflict item, since the top-ranked candidate depends on it.# Methodology audit of the three cross-modal discovery reports

**Verdict:** nothing here clears PROCEED TO PILOT. The weakest assumption in all three reports is that "arbitration accuracy" exists on the data they recommend. It does not. The consensus top candidate (conflict detection improves arbitration) fails the "what observation distinguishes A from B" test as written.

I call them Report 1 (untitled alphaXiv-linked file), Report 2 (Gemini) and Report 3 (Perplexity). I cloned the paper's artifact repo and read its schema, prompts and protocol. Full-text fetches of the paper itself failed (rate limit and bot blocking), so claims about its own limitations are second-hand. I did not re-verify the other 2026 papers the reports cite.

## 1. The three reports are not independent evidence

- **Report 3 was seeded.** Its reference list includes Report 1's filename, the handover, and a local file (`Idea_First_Thesis_Research_and_Recommendation.md`). Its top three are the project's earlier candidates re-labelled, and their literature basis is cited to that local file, not to primary papers. This breaks the anti-anchoring rule in your task file (Section 27).
- **Report 2 mirrors Report 1.** It has the same top three in the same order, the same next investigation, and the same "Which Source Wins? did not test uncertainty" hook. I cannot prove it was given Report 1, but this is what anchoring looks like.
- **Two of three "agreeing" is really one vote.** Count the conflict-detection consensus as a single source.

## 2. Checks against primary sources

| Report claim | What I found | Status |
|---|---|---|
| Clone the artifact for ChartQA-Conflict and GSM8K-Conflict; 400 chart items, or "500 chart + 500 arithmetic" (Report 2) | [The repo](https://github.com/Ro-netizen004/multimodal-arbitration-artifact) has 229 chart items. Rendered GSM8K/SVAMP stimuli are not in it. They sit on anonymous review mirrors that the README says will be replaced. I did not test those links. | Count contradicted; arithmetic access unverified |
| Arbitration accuracy; "image-correct/text-false", "text-correct/image-false", aligned controls (Reports 1, 2) | The artifact prompt states "Neither source is privileged" and forbids abstaining or hedging. Outcomes are exact-match source preference. Text reports are curated counterfactuals. No aligned or insufficient-evidence items exist. | Not defined on this data |
| "No manual annotation" (Reports 1, 2) | The protocol requires per-item reviewer certification, and 230 items were manually reviewed. New conditions need the same review. | Contradicted |
| Run Qwen2.5-VL-3B on the artifact (Report 2) | The config lists Qwen2-VL-2B, Qwen2.5-VL-7B, Idefics3-8B, LLaVA-OV-7B, LLaVA-1.6-7B, Phi-3.5-Vision and InternVL2-8B. There is no 3B and no unimodal competence data for it. | Unverified |
| Chain-of-thought prompts are cheap to add | Repo comments say rationale prompts made some models exhaust the output budget, so the authors used answer-only. Phi-3.5's chart accuracy was 2/229 until the parser was fixed, then 166/229. | Format compliance is a large confound |
| "Task-dependent reliance is established" | [The paper](https://arxiv.org/abs/2608.17205) is a single-group preprint from 17 Aug 2026. Its arithmetic conflicts pair the rendered image of one problem with the text of a different problem. A machine review (secondary) says the directness confound is flagged in the authors' own Limitations. | Second-hand |
| Conflict-detection prompting is untested (Reports 1, 2) | Zhu et al. (2024) already detect, interpret and mitigate cross-modality conflicts, including two prompt-based strategies. [CLASH](https://arxiv.org/abs/2511.19199) is a contradiction-detection benchmark. Neither report engages them. | Novelty overstated |
| Evidence removal then flat confidence is an open question (Reports 1, 2) | [Seeing without Looking](https://arxiv.org/abs/2605.22903) reports that even after the queried entity is removed, models frequently remain confidently affirmative. | Partly occupied |
| Report 2 compute table | Internally inconsistent: it lists 4 ratios × 3 pruners = 12 passes, then totals 6,000 passes. The 0.15 s per pass ignores multi-sentence generation. | Arithmetic error |

## 3. Cross-cutting faults

- **Identifiability.** Prompt conditions bundle a conflict cue, extra tokens, decomposition and a format change. No condition isolates which one acts.
- **Post-treatment conditioning.** Report 2 tests accuracy among items where the model "explicitly identifies a conflict". That conditions on a mediator and biases the comparison. Use intention-to-treat.
- **Weak metrics.**
  - Modality Preference Bias (MPB) is computed only among errors, so its denominator changes with the treatment.
  - Sequence entropy averaged over all generated tokens is diluted by format tokens.
  - Attention weight is used as "evidence use" (Report 2 U4), even though the same reports cite work showing attention does not track correctness.
  - Rationale faithfulness is judged by the same model.
- **Leakage.** In the arithmetic construction, each problem appears in both the image role and the text role across items. Splits and confidence intervals must cluster by underlying problem.
- **Prompt variance.** One template per condition is one draw from prompt space. "Greedy, one seed" reports no variance at all. Use at least 3 to 5 paraphrases per condition.
- **Power, no report does one.** This is my estimate: with paired binary outcomes, 20% discordant pairs and 80% power, about 1,000 items detect a 4-point change. About 165 items detect roughly 10 points. Filtering to items the model answers correctly from each source alone leaves about that many out of 229, even at Phi's 0.725 chart accuracy.
- **Compute.** GPU time is not the constraint. Item construction and review are.

## 4. The A vs B test

**C1: Explicit conflict detection improves arbitration (Reports 1, 2; Report 3 RQ4 in variant form)**

- **A:** stating the conflict makes the model compare sources.
- **B:** the prompt adds scaffolding or a demand cue, or the answer is fixed before the rationale is written.
- **As written, nothing distinguishes A from B.** The outcome has no truth when the prompt says no source is privileged. The chart gold answer is only "correct" if you impose an authority rule, and that turns the task into instruction-following.
- **What would distinguish them:**
  1. A length-matched placebo prompt (describe both sources, no comparison).
  2. A cue-only control ("sources may disagree", no required verdict).
  3. Aligned items to price false conflict declarations.
  4. A rationale intervention: prefill a correct or wrong verdict and see whether the answer follows it. Truncating or corrupting the rationale is the [Lanham et al.](https://arxiv.org/abs/2307.13702) style of test (background knowledge, not re-read).
  5. Compare the direct-answer margin with the post-rationale answer. A predicts the verdict changes answers. B predicts the answer tracks the pre-rationale margin.
- **Verdict: RESERVE.** All three designs fail. A repaired design passes.

**C2: Evidence-sufficiency calibration under masking (Reports 1, 2)**

- **A:** confidence tracks evidence.
- **B:** confidence tracks language prior.
- **Distinguishing observation:** stratify items by blind solvability, meaning whether a model without the image gets the item right. Under masking, confidence should fall on evidence-needed items and not on prior-answerable ones. At 100% mask, compare confidence to blind accuracy, not to zero. The reports treat flat confidence as "evidence-blind", which conflates B with miscalibration.
- **Faults:**
  - "Proportional to lost evidence" has no reference curve.
  - Partial masks leave answers inferable.
  - A "decisive bounding box" is undefined for multi-value chart questions. I am not aware of released answer boxes for DocVQA or ChartQA, so verify before relying on them.
- **Novelty:** this is the lane your earlier audits already covered (Evidence-Order Calibration, BCEA, Bigger or Cheaper). Treat novelty as low until compared against them.
- **Verdict: RESERVE.**

**C3: Token compression destroys localized evidence (Reports 1, 2, 3)**

- **A:** pruning drops answer-critical tokens.
- **B:** uniform information loss.
- **The design cannot separate them.** "Tier" equals benchmark, which equals answer format, chance level and baseline accuracy. Ratios to full-token accuracy are not comparable across tiers. ANOVA on binary outcomes is inappropriate. Forcing 448×448 likely lowers the OCR baseline (my inference).
- **What would distinguish them:** an item-level indicator of whether retained tokens overlap the answer region. Then compare error rates when the region was retained versus dropped at matched retention, with a random-drop control.
- **The result is uninformative anyway:** fine text failing first is expected a priori, because legibility scales with pixels.
- **Verdict: REJECT** as a thesis identity. Your project already lists generic token pruning as inactive.

**Everything else**

| Candidate | Why A vs B is unclear | Verdict |
|---|---|---|
| Bengali cultural repair (R3 RQ1) | Repair by a hint does not locate the deficit, because any sufficient hint can flip an answer. Visual, linguistic and cultural interventions are not orthogonal, since a visual description is text. The "initially wrong" set invites regression to the mean. The leakage line between knowledge and answer is subjective. Provenance is unverified. | REJECT |
| Action-value (R3 RQ2) | The oracle is an argmax over noisy single-draw outcomes, so regret is inflated. Action costs are not commensurable. The policy can learn dataset identity. Retrieval and clarification environments must be built. | REJECT |
| Dialect normalization (R3 RQ3) | It is outside the VLM field, and no ground truth exists for "critical meaning". Ambiguity cannot be separated from annotator unfamiliarity without several dialect-native raters. | REJECT |
| Grounding drift via prompt schedules (R2 U4) | The outcome is an attention weight, which softmax dilution over longer context lowers mechanically. Re-attends versus rationalizes is only separable by ablating image tokens mid-generation, which is not in the design. | REJECT |
| Tokenizer fertility drives modality reliance (R2 U5) | Fertility cannot be manipulated independent of language, so "causal" is invalid. Reliance measured as accuracy drop when the image is removed is bounded by the baseline. Floor effects mimic reduced reliance. | REJECT |
| Language changes arbitration (R1 U5) | It stacks a second factor on the unresolved C1 construct. Translation quality and comprehension confound it. | Park until C1 is fixed |
| Adaptation and evidence use (R1 U4) | The outcome is defined on conflict data unrelated to the shift domain. The cited method is CLIP-based, so the setups do not match. | REJECT |
| Missing-modality and benchmark-shortcut audits | Blank-image results are expected. Benchmark audits are occupied. Useful only as a blind-solvability filter inside C2. | Fold into C2 |

## 5. Decision and next action

**Decision log**
- **Decision:** No candidate is ready for a pilot. C1 and C2 are held in reserve, and the rest are rejected as specified.
- **Evidence:** the artifact's prompt, schema and protocol (repo inspection), plus the search snippets cited above.
- **Limitation:** the paper's full text was unreadable to me. The 2026 papers cited in the reports are unverified beyond what is noted here.
- **Status:** provisional.

**Next action (30 to 90 minutes, no model run):** decide the construct before anything else. Either measure source preference (the paper's construct, no accuracy) or verification against a stated authority (an image-authoritative task). Then compute how many of the 229 items survive a competence filter for your chosen model. If under about 150 do, you must build new items, and the annotation plan is the real feasibility question.

Do you want me to (A) write the repaired C1 protocol, with authority rule, placebo, prefill test, item counts and clustered statistics; (B) draft the competence-filter script for the 229 items; or (C) audit C2 against the earlier overlap set (Evidence-Order Calibration, BCEA, Bigger or Cheaper, Seeing without Looking) to pick the reserve lane? I can also save this as a Markdown record for the project.