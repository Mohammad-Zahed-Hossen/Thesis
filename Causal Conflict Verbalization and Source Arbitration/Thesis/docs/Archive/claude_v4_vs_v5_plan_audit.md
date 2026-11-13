# v4 dev plan vs. post-v5 plan: objective audit (2026-11-14)

Scope: compare the plan that produced the v4 dev runs with the current, unfrozen post-v5 plan (prereg working tree after D1–D5, `analyze_v5.py` working tree). The comparison is grounded in primary papers, read via AlphaXiv on 2026-11-14. Nothing is frozen. Every dev number below is for tuning only and is not a finding.

**Status (2026-11-14, later the same day):** revisions #1–#3 from §4 are applied in the working tree: the prereg (§2.2, §2.3, §7.6, §8, §11), `analyze_v5.py`, the tests and `results_v5/analysis_dev/`. The rest of §4 is still open. Nothing is committed or frozen.

Tags: [Verified] = read in the paper, code or rows; [Inferred] = my reasoning from verified facts; [Hypothesis] = untested.

## 0. What the two plans actually were

| Axis | v4 dev (as run, `results_v4/README.md`) | Post-v5 plan (prereg working tree) |
|:---|:---|:---|
| RQ | Does a reliability verbalization change which source's answer the model gives? | Same causal question, restricted to a controlled direct effect of a forced verdict at a fixed instruction |
| Intervention | Whole-verbalization swaps (`m0`/`m1`) and authored sentences `rel_image`/`rel_text` | Minimal edit of the model's **own** verdict clause (Jaccard ≥ 0.85, ≤ 2 swaps), plus matched templates `para`/`para_flip` |
| Evidence order | Image always first | Counterbalanced, instruction fixed |
| Instruction | z0 / z1 (neutral, conflict) | Non-binding and binding, plus explicit single-source ceilings |
| Outcome | Behavioural answer source after ~400-token solve | Math: behaviour (k = 1, `structured` parser) primary, Δℓ secondary. ChartQA: Δℓ primary |
| Controls | Wording control only | Competency conditioning, replay noise, wording floor, ceilings, Holm m = 4 |
| Models | Qwen2.5-VL-3B only, T4 fp16 | 3B and 7B confirmatory, 2B diagnostic; L4 bf16 |
| Regimes | Math only | Math confirmatory; ChartQA exploratory |

[Verified] The outcome came back to where it started. v4 measured behaviour. The R3 draft made Δℓ the single primary. D1 moved Math back to behaviour, but now with ceilings, a decision rule and a parser policy that v4 lacked.

## 1. Does the core v4 idea still hold?

**Yes, as a causal question. No, in the claim it can support.** [Inferred]

What held:
- The core manipulation is the same: hold everything fixed, force a different verdict, see whether the answer follows. v5 does this more cleanly than v4 did. v4's `m0`/`m1` contrasts swapped whole verbalizations, so they never isolated the verdict.
- This prefix-forcing design is now an established paradigm. CoT-Mediate (2607.27304) edits exactly one attribute inside the model's own reasoning, prefix-forces it, greedily decodes the answer, and measures adoption against a paraphrase floor. That paper reports that prefix-forcing gives the stronger test of mediation compared with re-prompting. [Verified, pp. 3–6]

What changed, and it is more than wording:
1. **"Reliability" has left the confirmatory claim.** Reliability is well-posed only in ChartQA, and D4 made ChartQA exploratory. The confirmatory question is now: *does a forced statement of which source to trust change which problem the model solves, in a regime where neither problem is wrong?* That is source following, not reliability judgement. The working title ("Stated Source Reliability Steers…") now promises more than the confirmatory design can deliver. [Inferred]
2. **The binding arm is close to a manipulation check.** The binding instruction says "solve only the problem from the source you named". A large binding effect therefore partly measures instruction compliance with a named source. Dev 3B ρ_beh = 1.02 is what that looks like. The faithfulness question proper ("does saying decide?") lives in the **non-binding** arm, and that is the arm where the wording floor fails for 7B and passes for 3B only under D5's replay clause. [Verified numbers, dev; Inferred reading]
3. **Generality narrowed** from "Qwen VLMs" to two Qwen2.5-VL sizes. [Verified]

Verdict: the idea is the same and the method is stronger. The defensible thesis statement has narrowed. That should be said openly in the title and in §1, rather than left for a reader to discover.

## 2. Are D1–D5 sound? Stronger alternatives?

### D1: behaviour primary in Math, Δℓ secondary. **Sound, and the literature supports it.**
- *Which Source Wins?* scores its margin only after `####`, "with no chain-of-thought". The authors say this measures "direct-answer preference, not reasoning-trace attribution". [Verified, p. 5]
- Their pooled 75.4% agreement hides the per-model figures. For Qwen2.5-VL-7B agreement was 62.6% / 68.8% (image / text arm), and for Qwen2-VL-2B it was 72.6% / 58.6% (Table 5). Our 7B figure of 56.6% is low, but it is the same model with a weak margin in their data too. Any comparison should use the per-model rows, not 75.4%. [Verified]
- Post-hoc reasoning (2603.01437): for Qwen2.5-3B/7B, pre-CoT probes decode the answer at AUC 0.99+ on tasks where CoT does not help, but only 0.69 / 0.78 on Logical Deduction, where it does. On multi-step tasks the answer forms during the CoT. Their tasks are binary classification, not arithmetic, so the transfer to GSM8K is [Inferred]. It is still the best available mechanism for why a margin read before any arithmetic barely tracks the eventual answer.
- **Weakness:** the primary outcome rests on one template (k = 1) and one greedy decode per cell.
- **Stronger alternative:** Thought Branches (2510.27484) argues that a single sampled CoT is inadequate for causal claims, and that off-policy edits gave "small and unstable" effects in their decision tasks. [Verified, pp. 1, 5] Our effects are large, so the risk of understating them is not ours. The cost of a single decode is instead that each item gives a 0/1 outcome, so power is low. A cheap upgrade is to sample n = 4–8 continuations (T = 0.7) on the confirm items, binding and non-binding only, and use P(text answer) per item as a robustness outcome. A second option is k = 2 templates for behaviour, at about 2× the behaviour compute.

### D2: `para_flip − para` co-primary with `flip − own`. **Sound.**
- This matches CoT-Mediate's design: flips are measured against re-injecting the original chain (C1), not against no text (C0), and a zero-change paraphrase sets the noise floor. [Verified, p. 3] Our `own` plays the role of C1, and `para` plays the role of the paraphrase control.
- The conjunctive rule (a claim only if both contrasts agree) is the conservative choice. Keep it.
- Caveat: `para`/`para_flip` are authored, so they are off-policy. Because both arms are authored, the off-policy part cancels within the pair. [Inferred]

### D3: `structured` parser; 2B diagnostic. **Justified, but chosen after seeing data.**
- Precedent: *Which Source Wins?* used `####` first and then a fall-back to the **last number** for arithmetic. [Verified, p. 12] That is our *lenient* parser. `structured` is stricter than the published precedent, so it is not a lax choice.
- The effect sizes depend on the parser (strict vs. lenient changed the binding shift by about +18 → +50 pp). All three must be reported side by side, as the code already does.
- Dropping 2B is forced: 0 of 1,200 Math generations contain `####`. The real loss is a cross-family check. Both *Grounding on Request* (2610.33841, Table 1) and *Which Source Wins?* show that default modality preference depends on the model. A single non-Qwen model as an exploratory replication would be stronger than nothing, but it is optional. Without it, claims stay "Qwen2.5-VL, 3B and 7B".

### D4: ChartQA exploratory. **Forced by arithmetic, not a choice.**
- 229 items × about 43% competency ≈ 98 items before the edit gates, below R5's 100. On dev only 6 of 30 (3B) and 2 of 30 (7B) passed, and both 7B donors state an answer before the verdict. [Verified]
- The only alternative is to redesign ChartQA: ask for no numbers in Sentence 1, settle `max_pixels`, and rerun dev. That would spend more of a 229-item pool, so it would not rescue confirmatory status. Accept D4, and change the title and claims to match it (§1).

### D5: churn = image↔text flips among attributable pairs; limit = replay + 5 pp. **This is the weakest decision. Revise it.**
- CoT-Mediate's floor is the **any-change** flip rate of a zero-change paraphrase: 1.7–3.3%. [Verified, p. 6, Table 5] Under any-change churn with the `structured` parser, our own-vs-para churn is 0.231 (3B) and 0.152 (7B), far above a 5 pp limit. Our gate passes only because of the attributable-pair definition. [Verified, dev]
- That definition can be defended on its merits: a source↔neither change is usually a parse or format change, not a source flip. But it was adopted after the original definition failed.
- The replay clause is not needed under binding: churn there is 0.032 for 3B and 0 for 7B, both under a fixed 5 pp. Its only effect is to rescue **3B non-binding** (0.076 < 0.032 + 0.05). It was tuned to one cell. [Verified, dev]
- **Recommendation:**
  1. Drop the replay adjustment and use a fixed 5 pp limit.
  2. Keep the attributable-pair churn as the gate statistic.
  3. Also report any-change churn and the change in the "neither" rate as pre-declared diagnostics.
  4. Add a rule: if the own→para "neither" shift exceeds a set bound (e.g. 10 pp), the floor is read as failed.

  This makes 3B non-binding fail the floor on dev data. That is the honest result.

## 3. Is the current plan better than the v4 plan?

**Yes, on almost every axis that matters for a causal claim.** [Inferred, from §0]

| Better | Worse or narrower |
|:---|:---|
| Own-verdict minimal edit is a verdict CDE; v4's whole-verbalization swap was not | Confirmatory scope has no regime where "reliability" is well-posed |
| Counterbalanced order (v4 confounded order with source) | Primary Math outcome rests on k = 1, single greedy decode |
| Competency conditioning; ceilings; replay and wording floors | Parser and churn definition chosen after dev (declared in R8) |
| Holm-corrected decision rule, item bootstrap, TOST | 2B lost, so there is no second model generation |
| Two model sizes, bf16, pinned revisions | |

v4 could not have answered its own question. v5 can, within a narrower claim.

## 4. Was rigor compromised to reach freeze?

There are some compromises. Most can be justified; three should be revised.

| # | Compromise | Justified? | Action |
|:--|:---|:---|:---|
| 1 | D5 replay clause rescues exactly one failing cell | **No** | Revise (§2, D5) |
| 2 | Behavioural ceiling Ceil_beh is built from explicit arms with a `none` prefill, where the model writes its own verdict. Dev 3B ρ_beh = 1.02 > 1, so the "ceiling" sits below the effect | **No, not as a ceiling** | Treat ρ_beh as unbounded and descriptive, or measure the ceiling with a verdict prefill consistent with the explicit instruction. Do not read R4's 0.25 bounds against a ceiling that the effect can exceed. Also report the two directions separately: *Grounding on Request* finds natural-language image requests much weaker than text requests (Fig. 2, Table 2), and averaging the two directions would hide that |
| 3 | TOST power about 0.64 at n ≈ 250 (0–0.26 at dev n) | Partly | Pre-declare that equivalence can come out "inconclusive", and never read a non-significant difference as "saying is not choosing". Or raise n, or add the sampling outcome (§2, D1) to reduce variance |
| 4 | D1 decided after dev | Yes | Already declared in R8 as a departure. It rests on validity evidence (agreement below the majority baseline), not on the size of the effect |
| 5 | `structured` parser chosen after dev | Yes | Report all three parsers. Stricter than the published precedent |
| 6 | ChartQA demoted | Yes, forced | Retitle; no reliability claims in confirmatory text |
| 7 | k = 1 template for behaviour | Cost-driven, acceptable | Add k = 2 or the sampling outcome if budget allows; list it as a limitation otherwise |
| 8 | Human coding of verdict labels not done (the `coding_v5` sample has 64 of 200 rows from 3B/7B Math) | Not yet a compromise | Must finish before the freeze; re-weight the sample toward 3B/7B Math |
| 9 | CLAUDE.md invariant 5 still says "one primary outcome: Δℓ" | Bookkeeping | Update when the freeze is approved |

Overall [Inferred]: the plan did not become laxer in its core design. Order, competency, ceilings and minimal edits are all stricter than in v4. The softening is concentrated in the **gates**: the D5 churn definition and limit, and a ceiling that is not a ceiling. Those happen to be exactly the places where dev results were inconvenient. Fixing #1–#3 costs no new GPU generation, apart from the optional ceiling re-measure and sampling.

## 5. Antigravity's analysis: corrections

Antigravity assessed commit `f802951`, not the current working tree.
- "Ceil_beh missing" and "readings driven by Δℓ" were fixed later in the working tree: `behaviour_ceiling` and `primary_reading_*` now exist. [Verified, code]
- "6/20, 2/20": the ChartQA counts are 6 of 30 items (6 of 13 competent) for 3B and 2 of 30 for 7B. [Verified]
- "50.6%" is the lenient figure; strict is 51.6%. [Verified]
- The ChartQA "99.1% cleanest agreement" is close to built-in: the 16-token decode starts at `####`, the same point where Δℓ is read, and the majority baseline is also 99.1%. It is not evidence that Δℓ is valid in ChartQA. [Verified]
- Comparing with *Which Source Wins?*' 75.4% should use that paper's per-model rows (§2, D1).

## 6. Sources read for this audit (AlphaXiv, 2026-11-14)

- Bhowal et al., *Position, Not Provenance* (CoT-Mediate), arXiv:2607.27304: pp. 1–8.
- Dassen et al., *Grounding on Request*, arXiv:2610.33841: pp. 1–7, 14, 17.
- Ghosh, Gupta & Wang, *Which Source Wins?*, arXiv:2608.17205: pp. 1–2, 5, 7–8, 12–15.
- Macar, Bogdan et al., *Thought Branches*, arXiv:2510.27484: pp. 1–10, 22–23, 30.
- Cox, Kianersi & Garriga-Alonso, *Post-Hoc Reasoning in Chain of Thought*, arXiv:2603.01437: pp. 1–8, 14, 20–23.
- Read earlier in this audit series: Lanham et al., arXiv:2307.13702; Jia & Mu, arXiv:2609.25366.
