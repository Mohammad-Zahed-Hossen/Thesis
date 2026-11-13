
## Executive Snapshot: Where You Are Right Now (`2026-11-13`)

* **What is done:**
  * The **v5 dev pass** (`29,880` rows across `Qwen2-VL-2B`, `Qwen2.5-VL-3B`, and `Qwen2.5-VL-7B` in `bfloat16` on an NVIDIA L4, ~11.15 h GPU time) is complete and internally consistent (`0` boundary mismatches across `20,868` scored rows) `[Verified]`.
  * Two forensic/deep audits ([claude_v5_independent_deep_audit.md](file:///d:/Thesis/Important/Causal%20Conflict%20Verbalization%20and%20Source%20Arbitration/Thesis/docs/Archive/claude_v5_independent_deep_audit.md), [claude_v5_forensic_code_and_construct_audit.md](file:///d:/Thesis/Important/Causal%20Conflict%20Verbalization%20and%20Source%20Arbitration/Thesis/docs/Archive/claude_v5_forensic_code_and_construct_audit.md), and [End-to-End Technical & Scientific Audit.md](file:///d:/Thesis/Important/Causal%20Conflict%20Verbalization%20and%20Source%20Arbitration/Docs/Context/End-to-End%20Technical%20&%20Scientific%20Audit.md)) uncovered construct, parser, and attrition issues in the dev data `[Verified]`.
  * **Latest commits (`67405c0` and `f802951` today)** already resolved those CPU/spec issues via **Pre-freeze Decisions D1–D5**, regenerated [analysis_v5.md](file:///d:/Thesis/Important/Causal%20Conflict%20Verbalization%20and%20Source%20Arbitration/Experiment/results_v5/analysis_dev/analysis_v5.md), created v5 human-coding sheets in [coding_v5/](file:///d:/Thesis/Important/Causal%20Conflict%20Verbalization%20and%20Source%20Arbitration/Experiment/coding_v5/), and **all `231` unit tests pass** `[Verified]`. *(Note: [Experiment/README.md](file:///d:/Thesis/Important/Causal%20Conflict%20Verbalization%20and%20Source%20Arbitration/Experiment/README.md) has not yet been updated to reflect commit `f802951`.)*
* **What is NOT done yet:**
  * **No `prereg-v5` git tag exists** (`git tag -l` is empty) — the pre-registration is still a **DRAFT** `[Verified]`.
  * **Human coding is 0% done** ([coder_A_verdicts.csv](file:///d:/Thesis/Important/Causal%20Conflict%20Verbalization%20and%20Source%20Arbitration/Experiment/coding_v5/coder_A_verdicts.csv) and [coder_A_flips.csv](file:///d:/Thesis/Important/Causal%20Conflict%20Verbalization%20and%20Source%20Arbitration/Experiment/coding_v5/coder_A_flips.csv) are blank) `[Verified]`.
  * **Zero confirmatory data exists** (`--phase confirm` has not been run) `[Verified]`.
  * **Zero active thesis chapters** have been drafted in [Thesis/](file:///d:/Thesis/Important/Causal%20Conflict%20Verbalization%20and%20Source%20Arbitration/Thesis/README.md) `[Verified]`.

---

## Phase 1: Topic Discovery & Screening (`Aug – Sept 2026`)

*Sources: [Docs/Context/](file:///d:/Thesis/Important/Causal%20Conflict%20Verbalization%20and%20Source%20Arbitration/Docs/Context/README.md) and [Docs/Decision_Audits/](file:///d:/Thesis/Important/Causal%20Conflict%20Verbalization%20and%20Source%20Arbitration/Docs/Decision_Audits/README.md)*

1. **Parent Field Locked:** You froze **Multimodal / Vision-Language Learning and Systems** under your hardware boundary (local Ryzen 5600G CPU / 8 GB RAM for coding/analysis; Colab Pro for GPU inference) ([Canonical Thesis Field Specification.md](file:///d:/Thesis/Important/Causal%20Conflict%20Verbalization%20and%20Source%20Arbitration/Docs/Context/Canonical%20Thesis%20Field%20Specification.md), [Thesis_Progress_and_Research_Map.md](file:///d:/Thesis/Important/Causal%20Conflict%20Verbalization%20and%20Source%20Arbitration/Docs/Context/Thesis_Progress_and_Research_Map.md)) `[Verified]`.
2. **Fields Screened and Parked:** You evaluated and rejected/parked Medical Imaging & FL, Multimodal Agents (*AdaTooler-V* / *Thyme* occupied the space), Continual Learning, and Long-Context/Planning ([Canonical_Rejected_and_Parked_Thesis_Fields_Report.md](file:///d:/Thesis/Important/Causal%20Conflict%20Verbalization%20and%20Source%20Arbitration/Docs/Context/Canonical_Rejected_and_Parked_Thesis_Fields_Report.md)) `[Verified]`.
3. **Final Four-Proposal Adversarial Audit (`2026-09-23`):** In [final_adversarial_thesis_decision_audit.md](file:///d:/Thesis/Important/Causal%20Conflict%20Verbalization%20and%20Source%20Arbitration/Docs/Decision_Audits/final_adversarial_thesis_decision_audit.md), four VLM proposals were audited:
   * **Candidate B** (Reasoning-trace degradation): pre-empted by *RH-Bench* (`arXiv:2505.21523`).
   * **Candidate C** (Visual binding IDs on natural images): verified gap, but parked due to high risk of an uninformative negative result.
   * **Candidate D** (Bengali Cultural VLM steering): deprecated because the assumed "layer-18 bottleneck" was unverified and *BabelSteering* (`arXiv:2608.16577`) partly pre-empted it.
   * **Candidate A (Chosen):** *"Causal Conflict Verbalization and Source Arbitration in VLMs"* — chosen because it had a verified gap, zero training cost, and clean public stimuli from *Which Source Wins?* (`arXiv:2608.17205`: `vlm-modality-research/modality-conflict-arbitration-v2` and `chartqa-evidence-conflict-v2`) `[Verified]`.

---

## Phase 2: Early Pilots (`v1`–`v3`) & Why the First Topic Broke (`Sept 2026`)

*Sources: [Experiment/results_v3/README.md](file:///d:/Thesis/Important/Causal%20Conflict%20Verbalization%20and%20Source%20Arbitration/Experiment/results_v3/README.md), [Thesis Understanding FAQ (Opus 4.6).md](file:///d:/Thesis/Important/Causal%20Conflict%20Verbalization%20and%20Source%20Arbitration/Thesis/docs/Understanding/Thesis%20Understanding%20FAQ%20(Opus%204.6).md)*

You ran `v1`–`v2` ($N=20$) and the **v3 pilot** ($N=1,619$ on `Qwen2.5-VL-3B-Instruct`, FP16 on T4). Early September documents (like the stale top banner of [Thesis_Progress_and_Research_Map.md](file:///d:/Thesis/Important/Causal%20Conflict%20Verbalization%20and%20Source%20Arbitration/Docs/Context/Thesis_Progress_and_Research_Map.md)) celebrated a $+63.74\text{ pp}$ shift ($89.5\% \to 25.8\%$) as "empirically validated causal proof" `[Verified]`.

When you audited the raw v3 outputs with [reanalyze_v3.py](file:///d:/Thesis/Important/Causal%20Conflict%20Verbalization%20and%20Source%20Arbitration/Experiment/reanalyze_v3.py), **five fatal defects emerged** `[Verified]`:

1. **Instruction vs. Verbalization Confound:** Arm 2 (*"neutrally describe..."*) vs. Arm 3 (*"explain which source you consider more reliable..."*) randomized the **user prompt**, not the model's verbalization. Shifting answers under a different instruction only proves instruction-following, not that the generated words steered the answer.
2. **Token-Cap Truncation & `last_num` Artefacts:** `98.1%` (Arm 1), `37.6%` (Arm 2), and `44.2%` (Arm 3) hit the 256-token limit, forcing the scorer onto a `last_num` fallback that picked up numbers inside image descriptions.
3. **False Refusal Heuristic:** The claimed `13.65%` refusal rate was actually `2.3%` (`38 / 1,619`)—the regex matched words like `"conflict"` in outputs that still solved a problem.
4. **`repetition_penalty = 1.05` Artefact:** Omitting `repetition_penalty=1.0` let Qwen's default `1.05` artificially inflate image answers and abstention labels.
5. **Ill-Posed Construct ("Arbitration"):** In GSM8K/SVAMP conflicts (image of problem $i$ paired with text of problem $i+1$), both problems are mathematically valid—neither is "unreliable".

> **How to use this in your thesis:** Per [THESIS_NARRATIVE_AND_FRAMING_GUIDE.md](file:///d:/Thesis/Important/Causal%20Conflict%20Verbalization%20and%20Source%20Arbitration/Thesis/THESIS_NARRATIVE_AND_FRAMING_GUIDE.md), `v3` is **not** a failed experiment to hide—it is a strong methodological critique showing why prompt-comparison evaluations cannot measure CoT faithfulness `[Verified]`.

---

## Phase 3: The Pivot to *"Does the Verdict Decide?"* (`v4` Dev & Literature Grounding, `Nov 7–10, 2026`)

*Sources: [Experiment/results_v4/README.md](file:///d:/Thesis/Important/Causal%20Conflict%20Verbalization%20and%20Source%20Arbitration/Experiment/results_v4/README.md), [Docs/Decision_Audits/Idea.md](file:///d:/Thesis/Important/Causal%20Conflict%20Verbalization%20and%20Source%20Arbitration/Docs/Decision_Audits/Idea.md), [Docs/Paper/](file:///d:/Thesis/Important/Causal%20Conflict%20Verbalization%20and%20Source%20Arbitration/Docs/Paper/README.md)*

To isolate the verbalization from the instruction, you pivoted to **prefix-forcing** (inspired by Lanham et al. 2023 and *CoT-Mediate*): hold the user prompt fixed, write a reliability verdict directly into the start of the assistant's turn, flip it, and see if the answer follows. That estimates a **Controlled Direct Effect (CDE)**, not natural mediation `[Verified]`.

### What `v4` (`dev2`, $N=200$, `Qwen2.5-VL-3B`) Revealed

* After fixing mid-sentence truncation and locking `repetition_penalty=1.0`, transplant fidelity reached `>95%` `[Verified]`.
* On `110 / 200` dual-competent items, flipping an authored verdict (`rel_image` vs. `rel_text`) shifted image answers by **`+20.9 pp`** under the neutral instruction ($z_0$) vs. **`−1.8 pp`** under the conflict instruction ($z_1$) `[Verified]`.
* **New flaws uncovered in `v4`:**
  1. $z_1$ had **instruction ambiguity** (it asked for a verdict, then said *"solve the math problem"* without binding the answer to the verdict).
  2. Neutral same-meaning paraphrases (`eq_a` vs. `eq_b`) changed source labels on **`24.5%`** ($z_0$) and **`22.7%`** ($z_1$) of competent items over 400-token generations (a huge wording-noise floor).
  3. Evidence order was always `<image><text>`, never counterbalanced.
  4. `rel_image`/`rel_text` were researcher-authored strings, not minimal edits of the model's own words.

### Literature Dossier & Freeze Audit (`2026-11-10`)

You built an evidence base from **14 primary arXiv PDFs** ([lit-dossier-verdict-transplant.md](file:///d:/Thesis/Important/Causal%20Conflict%20Verbalization%20and%20Source%20Arbitration/Docs/Paper/lit-dossier-verdict-transplant/lit-dossier-verdict-transplant.md) and [prereg-freeze-audit.md](file:///d:/Thesis/Important/Causal%20Conflict%20Verbalization%20and%20Source%20Arbitration/Docs/Paper/prereg-freeze-audit/prereg-freeze-audit.md)), retracted overstated claims (*"100% untouched gap"*), and reshaped the design into **v5** via Resolutions **R1–R8**:

* *Noncommutativity* (`arXiv:2609.26986`): showed a `+15–16.7 pp` recency bias in Qwen2.5-VL-3B $\rightarrow$ **counterbalance order (`image_first` & `text_first`) with no Source A/B letters** (`R2`).
* *Grounding on Request* (`arXiv:2610.33841`): prompting gives weak image control $\rightarrow$ **add explicit-source ceilings (`explicit_image` / `explicit_text`)** to bound prompt controllability.
* *CoT-Mediate* (`arXiv:2607.27304`): **minimal-edit swaps** of the model's own verdict + paraphrase floor (`own` vs. `para`).
* *Biased Bayesian Observers* (`arXiv:2610.19407`) & *Which Source Wins?* (`arXiv:2608.17205`): **teacher-forced log-likelihood margin $\Delta\ell$** at `####` (`R3`), competency conditioning (`2511.02243`), and excluding broken ChartQA item `conflict_id = 45` (`229` items from `230` rows).

---

## Phase 4: The `v5` Design, Dev Pass (`results_v5/`), and Forensic Audits (`Nov 11–13, 2026`)

*Sources: [Docs/PREREGISTRATION_VERDICT_TRANSPLANT.md](file:///d:/Thesis/Important/Causal%20Conflict%20Verbalization%20and%20Source%20Arbitration/Docs/PREREGISTRATION_VERDICT_TRANSPLANT.md), [Thesis/docs/Archive/](file:///d:/Thesis/Important/Causal%20Conflict%20Verbalization%20and%20Source%20Arbitration/Thesis/docs/Archive/claude_v5_forensic_code_and_construct_audit.md), [End-to-End Technical & Scientific Audit.md](file:///d:/Thesis/Important/Causal%20Conflict%20Verbalization%20and%20Source%20Arbitration/Docs/Context/End-to-End%20Technical%20&%20Scientific%20Audit.md)*

You implemented the v5 pipeline (`harness_v5.py`, `transplant_v5.py`, `score_v5.py`, `analyze_v5.py`) with 4 wording templates ($K=4$), binding vs. non-binding instructions, explicit ceilings (`m_none` prefill), 5 minimal-edit verdict variants (`own`, `flip`, `none`, `para`, `para_flip`), and ran the full **v5 dev pass** (`200` Math + `30` ChartQA dev items) on an L4 in `bfloat16` (`29,880` rows) `[Verified]`.

### What the Dev Pass & Audits Exposed (Dev Data Only, Not Findings)


| Model × Regime    | Competent → Passed Gates | Key Audit Discoveries (`[Verified]`)                                                                                                                                                                                                                                                                                                                                      |
| -------------------- | --------------------------: | --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| **`2B | Math`**    |                  `0 → 0` | `2B` wrote `####` in `0 / 400` base rows (wrote prose `"Therefore, the answer is X."`), failing strict competency completely.                                                                                                                                                                                                                                             |
| **`3B | Math`**    |                `80 → 80` | `sign(Δℓ)` at `####` agreed with eventual behavioural answers only **`51.6%`** of the time (chance = `50%`; within-order AUC `0.53–0.56`). `Δℓ` mostly measured a `±1.5` recency prior toward whichever source came last. Meanwhile, **behavioural** `flip − own` moved answers strongly (`+45.6 pp` strict / `+49.4 pp` structured under binding).                |
| **`7B | Math`**    |              `124 → 115` | **`93.6%`** of binding $\text{CDE}_\ell$ (`+1.515` of `+1.619`) came from **deleting** the model's own verdict (`none − own`), while `flip − none` added only `+0.103` (`95% CI [−0.09, +0.29]`). Also, strict `####` parsing discarded **`58.3%`** of 7B behavioural outputs as `"neither"` because after `{m}\n\n` (no `####`), 7B wrote `"The final answer is X."`. |
| **`2B | ChartQA`** |                 `10 → 0` | Failed donor gates (`own_absent` 18, `own_undetermined` 2).                                                                                                                                                                                                                                                                                                               |
| **`3B | ChartQA`** |                 `13 → 6` | Severe attrition (`6/30`, below §8's 60% gate and projecting ~40 confirm items vs. R5's 100-item bar), and Sentence 1 leaked the numerical answer before the verdict in ~35–50% of donors.                                                                                                                                                                              |
| **`7B | ChartQA`** |                 `13 → 2` | Both surviving items leaked the gold answer in Sentence 1; `8` item-orders failed `too_many_swaps`, and `score_v4.split_verbalization` sliced off the verdict in `10/60` donor rows due to `"U.S."` and its 2-sentence fallback.                                                                                                                                          |

The audits also caught **code/analysis bugs**: `analyze_v5.py` counted `None` ("neither") transitions in `change_rate`, inflated Holm's family from $m=3$ to $m=5$, `score_v5` lacked regime-aware noun filtering and `"less reliable"` negation handling, `harness_v5.py` scored `verdict_nll` over `\n\n####`, and Math's `none` behavioural prefill (`{m_none}\n\n`) allowed models to spontaneously regenerate a verdict in `69.4%` (3B) and `88.5%` (7B) of trials `[Verified]`.

---

## Phase 5: Today's Pre-Freeze Fixes (`D1–D5`) & Exact Remaining Roadmap

In commits `67405c0` and `f802951` (today, `2026-11-13`), you updated [PREREGISTRATION_VERDICT_TRANSPLANT.md](file:///d:/Thesis/Important/Causal%20Conflict%20Verbalization%20and%20Source%20Arbitration/Docs/PREREGISTRATION_VERDICT_TRANSPLANT.md) (§2, §3.2, §3.4, §6, §7, §8, §11) and `Experiment/*.py` to implement **Decisions D1–D5**:

1. **D1 (Primary Outcome Split):** On **Math (GSM8K/SVAMP)**, **behavioural choice shift** $\Delta P(Y{=}T)$ at $k=1$ is now primary (because Math `Δℓ` at `####` happens before CoT arithmetic and barely tracks solved answers); $\Delta\ell$ stays secondary/diagnostic in Math and primary in ChartQA `[Verified]`.
2. **D2 (Clean Matched Pair & Decomposition):** `para_flip − para` (both variants edited, removing the asymmetric edit artefact) is elevated to **co-primary** alongside `flip − own`, with full $m_\varnothing$ decomposition (`none − own`, `flip − none`, `para_flip − none`) `[Verified]`.
3. **D3 (`structured` Parser & 2B Demotion):** Headline Math parsing uses `score_v5.extract_answer_math_structured` (`####`, else explicit final-answer phrase / `\boxed{X}`), rescuing 7B's `"The final answer is X."` outputs while keeping `strict` and `lenient` side by side. `Qwen2-VL-2B` is now **diagnostic-only**; `Qwen2.5-VL-3B` and `Qwen2.5-VL-7B` are the two confirmatory models `[Verified]`.
4. **D4 (ChartQA Role):** ChartQA-Conflict is designated **exploratory/secondary** `[Verified]`.
5. **D5 (Churn & Replay Noise):** Wording-floor churn tracks true `image <-> text` flips separately from `neither` transitions and benchmarks them against measured unforced replay noise (`donor` vs. non-binding `own`) alongside the fixed `5.0%` cap `[Verified]`.
6. **Bug Fixes & Dev Artifacts Generated:** Fixed Holm `m=3`, regime-aware & negation-aware `stated_reliable_source`, sentence splitting (`####`, `U.S.`/`U.K.`), Sentence-1 answer-leakage gating, `verdict_nll` span scoring, `max_pixels = 200704` for ChartQA, persisted [results_v5/analysis_dev/](file:///d:/Thesis/Important/Causal%20Conflict%20Verbalization%20and%20Source%20Arbitration/Experiment/results_v5/analysis_dev/analysis_v5.md), created [Experiment/coding_v5/](file:///d:/Thesis/Important/Causal%20Conflict%20Verbalization%20and%20Source%20Arbitration/Experiment/coding_v5/CODEBOOK_v5.md) (`1,087` verdict rows + `150` flip rows), and all **`231` unit tests pass** `[Verified]`.

### What Remains To Finish the Thesis

1. **Human Coding (Local, No GPU):** Double-code [coding_v5/](file:///d:/Thesis/Important/Causal%20Conflict%20Verbalization%20and%20Source%20Arbitration/Experiment/coding_v5/CODEBOOK_v5.md) (`coder_A_*` / `coder_B_*`) and compute Cohen's $\kappa$ before any claim uses `stated_reliable_source` or flip quality (prereg §8).
2. **Pre-Freeze GPU Sanity Checks & Doc Sync:**
   * Run and record the `--print_example` **ChartQA render gate** on the real Colab/RunPod processor ([RUNBOOK_v5.md](file:///d:/Thesis/Important/Causal%20Conflict%20Verbalization%20and%20Source%20Arbitration/Experiment/RUNBOOK_v5.md) §3 — previously skipped for ChartQA in `v5_dev_output.md`).
   * Decide if any targeted GPU dev re-check is needed for the modified inputs/gates (e.g., Math `none` behavioural regeneration where `{m_none}\n\n` lets models write a new Sentence-2 verdict, or newly rescued items after the splitter fix), and sync [Experiment/README.md](file:///d:/Thesis/Important/Causal%20Conflict%20Verbalization%20and%20Source%20Arbitration/Experiment/README.md) with `f802951`.
3. **Freeze the Pre-Registration (`prereg-v5`):** Verify every R8 condition in [PREREGISTRATION_VERDICT_TRANSPLANT.md](file:///d:/Thesis/Important/Causal%20Conflict%20Verbalization%20and%20Source%20Arbitration/Docs/PREREGISTRATION_VERDICT_TRANSPLANT.md), commit, and create the `prereg-v5` git tag.
4. **Run Confirmatory Phase (`--phase confirm`) on GPU (L4/A100, `bfloat16`):** Execute `base`, `donor`, and `transplant_v5.py --phase confirm --n_competent 250` on the unseen confirm items (following [RUNBOOK_v5.md](file:///d:/Thesis/Important/Causal%20Conflict%20Verbalization%20and%20Source%20Arbitration/Experiment/RUNBOOK_v5.md) §6), then run `analyze_v5.py` + `analyze_v5_lme4.R`.
5. **Draft the Dissertation (`Thesis/`) & Read `CMC-Bench`:** Read `CMC-Bench` (Catapang, 2026) for the related-work chapter ([PREREGISTRATION_VERDICT_TRANSPLANT.md](file:///d:/Thesis/Important/Causal%20Conflict%20Verbalization%20and%20Source%20Arbitration/Docs/PREREGISTRATION_VERDICT_TRANSPLANT.md) §1.1), and write Chapters 1–7 in `Thesis/` using [THESIS_NARRATIVE_AND_FRAMING_GUIDE.md](file:///d:/Thesis/Important/Causal%20Conflict%20Verbalization%20and%20Source%20Arbitration/Thesis/THESIS_NARRATIVE_AND_FRAMING_GUIDE.md).


Think of your entire thesis as a **courtroom mystery** about how an AI thinks:

> **The Setup:** You show a Vision-Language Model (VLM) two pieces of conflicting evidence—an **Image** (e.g., a photo of a math problem whose answer is `100`) and a **Typed Text** (a different math problem whose answer is `200`).
>
> **What the AI writes:**
>
> 1. *Sentence 1:* "The image and the typed text present different problems."
> 2. *Sentence 2 (**The Verdict**):* "I consider the typed text more reliable."
> 3. *Final Answer:* `200`
>
> **Your Big Question (*"Does the Verdict Decide?"*):** Did writing *"the typed text is more reliable"* actually **cause** the AI to pick `200`? Or had the AI already silently chosen `200` (because it prefers text, or prefers whatever it saw last), making that reliability verdict pure **"theatre"** (post-hoc rationalization)?

In **Phase 2 (`v3`)**, you accidentally tested the wrong thing: you gave Group A the order *"describe the evidence"* and Group B *"say which is more reliable"*. When Group B picked text more often, you couldn't tell whether the AI's **own verdict words** caused the shift, or whether it was simply obeying **your different order**.

Here is **Phases 3–5** in plain English.

---

## Phase 3: The Pivot from `v3` to `v4` & the Literature Check

*Analogy: Stop changing the boss's instructions; instead, secretly swap one word on the judge's teleprompter.*

### 1. The "Teleprompter Trick" (Prefix-Forcing)

In `v4`, you stopped changing the user's prompt. Instead, you used **prefix-forcing**:

1. Give the AI the **exact same prompt** every time.
2. Take the AI's own opening sentences and paste them into the start of the AI's reply (`own` = *"I consider the typed text more reliable."*).
3. In the test condition (`flip`), secretly swap **just the source name** (*"I consider the image more reliable."*) before letting the AI finish solving.

Because the prompt, image, and text didn't change by a single character, **any change in the final answer must come from that swapped verdict**. In causal inference, this is a **Controlled Direct Effect (CDE)**: *"If I put these exact words in your mouth, do your actions follow them?"* (You carefully avoid calling it full "mediation", because forcing words into the AI's mouth is artificial—*off-policy*—compared to the AI choosing them naturally.)

### 2. What `v4` (`N = 200` dev items) Taught You

* When you gave a **Neutral** prompt (*"describe what you see, then solve a problem"*), flipping an authored verdict moved answers toward the image by **`+20.9` percentage points** (`[Verified]` dev).
* When you gave a **Conflict** prompt (*"say which is reliable, then solve the math problem"*), flipping the verdict did almost nothing (**`−1.8` percentage points**).

**Why did the Conflict prompt freeze the verdict?**
Imagine telling someone: *"Tell me whether the red car or the blue car is safer. Then drive a car."* Notice the loophole? You **never told them to drive the car they called safer**!

Reading **14 primary papers** in [Docs/Paper/](file:///d:/Thesis/Important/Causal%20Conflict%20Verbalization%20and%20Source%20Arbitration/Docs/Paper/README.md) plus your `v4` data exposed **three more leaks** you had to plug before running the real experiment:

1. **Recency Bias (*Noncommutativity*, `arXiv:2609.26986`):** Putting Image first and Text second gives Text an automatic ~`15 pp` "last thing I read" advantage. **Fix:** Run every item **both ways** (`Image → Text` and `Text → Image`), and remove `"Source A / Source B"` labels.
2. **The Wording-Noise Floor (*CoT-Mediate*, `arXiv:2607.27304`):** In `v4`, even two sentences with the *same meaning* (`eq_a` vs. `eq_b`) made the AI change which source it solved **`23–25%`** of the time over 400 tokens of rambling. If random rewording changes 25% of answers, a 20% verdict effect is hard to trust. **Fix:** Edit **only** the source noun in the AI's *own* sentence (minimal edit), and add a **paraphrase control** (`para` vs. `own`) to measure pure wording noise.
3. **Need a "Binding" Arm & an "Explicit Ceiling" (*Grounding on Request*, `arXiv:2610.33841`):**
   * **Binding prompt:** Close the loophole: *"Then solve **only** the problem from the source you named as more reliable."*
   * **Explicit ceiling:** Ask *"Solve **only** the image problem"* vs. *"Solve **only** the text problem."* This acts as a **yardstick**: if a model barely listens even when you *directly* command it to use the image, you can't expect it to obey a subtle self-written verdict either!

---

## Phase 4: Building `v5`, Running the Dev Pass, & What the Audits Caught

*Analogy: Doing a full dress rehearsal on practice items—and discovering five hidden props broke on stage.*

### How the `v5` Pipeline Works (Step by Step)

You built `v5` ([harness_v5.py](file:///d:/Thesis/Important/Causal%20Conflict%20Verbalization%20and%20Source%20Arbitration/Experiment/harness_v5.py), [transplant_v5.py](file:///d:/Thesis/Important/Causal%20Conflict%20Verbalization%20and%20Source%20Arbitration/Experiment/transplant_v5.py)) on **two datasets** and **three models** (`Qwen2-VL-2B`, `Qwen2.5-VL-3B`, `Qwen2.5-VL-7B`):

* **Math (`GSM8K/SVAMP`):** Two different valid math problems. Neither is "wrong", so this tests **source following**.
* **ChartQA-Conflict:** A real chart vs. a fake counterfactual report. Here the chart is right, so "reliability" is genuinely meaningful.

For each item:

1. **Competency Filter ("Can you solve each alone?"):** Give the AI *only* the image (`base_image`), then *only* the text (`base_text`). If it can't solve both individually, drop the item (otherwise wrong math looks like source bias).
2. **Donor Stage ("Write your natural opening"):** Ask the AI to compare both sources and state which is more reliable. Save its Sentence 1 + Sentence 2.
3. **Build 5 Variants ("The 5 Masks"):**
   * `own`: Its own opening unchanged (*"I consider the typed text more reliable."*).
   * `flip`: Swap only the source noun (*"I consider the image more reliable."*).
   * `none`: **Delete Sentence 2** completely (only Sentence 1 remains).
   * `para`: Replace Sentence 2 with a clean template naming its *own* choice.
   * `para_flip`: Replace Sentence 2 with that same clean template naming the *opposite* choice.
4. **Measure Two Outcomes:**
   * **$\Delta\ell$ (The "Gut-Feeling Meter" at `####`):** Paste `####` right after the verdict and read the AI's raw log-probability preference for the Image answer vs. Text answer *before* it writes any reasoning.
   * **Behavioural Answer:** Let it actually work out the full math problem (up to 512 tokens) or write the ChartQA answer (16 tokens).

### The 5 "Plot Twists" Caught in the `v5` Dev Dress Rehearsal (`29,880` rows on an L4 GPU)

Good news first: technically, the GPU run was rock-solid (`0` tokenization boundary mismatches out of `20,868` scored rows). **But** the audits ([claude_v5_forensic_code_and_construct_audit.md](file:///d:/Thesis/Important/Causal%20Conflict%20Verbalization%20and%20Source%20Arbitration/Thesis/docs/Archive/claude_v5_forensic_code_and_construct_audit.md), [End-to-End Technical & Scientific Audit.md](file:///d:/Thesis/Important/Causal%20Conflict%20Verbalization%20and%20Source%20Arbitration/Docs/Context/End-to-End%20Technical%20&%20Scientific%20Audit.md)) caught **five major scientific surprises**:

1. **Plot Twist 1 — In Math, $\Delta\ell$ at `####` was a coin flip (`51.6%` agreement on 3B):**
   * *Intuition:* Imagine stopping a student right after they say *"I trust the image problem"* and—**with zero scratch paper**—demanding: *"Quick, is the answer more likely `74` or `129`?"* They haven't done the math yet! So their gut-feeling probability mostly just tracks **whichever problem they read last** (`image_first` favored text; `text_first` favored image).
   * Yet when you *gave* `3B` its scratch paper (Behavioural solving), flipping the verdict actually shifted its final solved answer by nearly **`+50` percentage points**! So $\Delta\ell$ before scratch paper was blind to the real effect in Math.
2. **Plot Twist 2 — 7B's "Ghost Effect" (`none` vs. `flip`):**
   * On `7B Math`, `flip` vs. `own` shifted $\Delta\ell$ by `+1.619`. Looks huge—until you check `none` (just *deleting* Sentence 2)!
   * **`93.6%`** (`+1.515` of `+1.619`) happened simply by **removing** the model's own verdict (`none - own`). Adding the flipped verdict (`flip - none`) only added **`+0.103`**.
   * *Analogy:* You thought flipping a road sign from *"Turn Left"* to *"Turn Right"* steered the driver right. In reality, **taking down the "Turn Left" sign** caused 94% of the change, and putting up *"Turn Right"* barely nudged them (maybe because the model's original reason in Sentence 2 still subtly argued for the old source!). By contrast, the clean `para_flip` template *did* steer it cleanly.
3. **Plot Twist 3 — `Qwen2-VL-2B` Failed the "Dress Code":**
   * `2B` wrote `####` in **`0 / 400`** Math base runs (it prefers prose like *"Therefore, the answer is 26"*), giving **`0 / 200`** eligible Math items—and `0 / 10` passing ChartQA gates.
4. **Plot Twist 4 — ChartQA Lost Almost All Items & "Spoiled the Ending":**
   * Only `6/30` (3B) and `2/30` (7B) ChartQA items survived competency + edit gates.
   * Worse, in `35–50%` (3B) and `68–77%` (7B) of ChartQA donors, the AI blurted out the final number inside **Sentence 1** (*"The chart and report both say **883**..."*) before stating reliability in Sentence 2. Flipping Sentence 2 couldn't un-write `883` from Sentence 1!
5. **Plot Twist 5 — Strict `####` Grading & a Buggy Noise Counter:**
   * After your prefill (`{m}\n\n`), `7B` finished its Math work with *"The final answer is 42."* instead of `#### 42` in **`58.3%`** of runs—so the strict parser threw away more than half of 7B's valid answers as `"neither"`.
   * Also, `analyze_v5.py` had a bug: when `own` wrote `#### 42` (`image`) and `para` wrote `"The answer is 42"` (`None`), `image != None` counted that as a "source flip", inflating wording noise to `20–26%` when real `image ↔ text` flips were `0–3%`!

---

## Phase 5: Today's Fixes (`D1–D5`) & What Happens Next

*Analogy: Updating the rulebook after the dress rehearsal so the real trial is fair—before locking the rules.*

In today's commits (`67405c0` and `f802951`), you already updated [PREREGISTRATION_VERDICT_TRANSPLANT.md](file:///d:/Thesis/Important/Causal%20Conflict%20Verbalization%20and%20Source%20Arbitration/Docs/PREREGISTRATION_VERDICT_TRANSPLANT.md) and the code with **Pre-freeze Decisions D1–D5**:


| Decision | Plain-English Fix                                                         | Why It Solves the Dev Problem                                                                                                                                                |
| ---------- | --------------------------------------------------------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------ |
| **D1**   | **Math uses Behavioural answers as primary; ChartQA keeps $\Delta\ell$.** | Math needs scratch paper (512 tokens) before the AI knows what the answer is; ChartQA doesn't.                                                                               |
| **D2**   | **Promote `para_flip − para` to co-primary + report `none` breakdown.**  | Removes the asymmetric edit bias and separates "deleting the old verdict" from "following the new one."                                                                      |
| **D3**   | **Use the `structured` Math parser + demote `2B` to diagnostic-only.**    | Accepts `#### X`, `"The final answer is X"`, and `\boxed{X}` (rescuing 7B's lost answers). `3B` and `7B` are your two confirmatory models.                                   |
| **D4**   | **Make ChartQA-Conflict exploratory/secondary.**                          | With only ~7–20% survival, ChartQA won't reach the 100-item confirmatory threshold.                                                                                         |
| **D5**   | **Fix churn counting & measure natural "replay noise."**                  | Separates missing `####` (`neither`) from true `image ↔ text` flips, and benchmarks paraphrase noise against how much the model drifts when re-run with *no change at all*. |

You also added the **Sentence-1 answer-leakage gate** (drops items if Sentence 1 spoils the number), fixed the sentence splitter (`"U.S."`, `####`) and Holm correction ($m=3$), generated [analysis_v5.md](file:///d:/Thesis/Important/Causal%20Conflict%20Verbalization%20and%20Source%20Arbitration/Experiment/results_v5/analysis_dev/analysis_v5.md), created blank human-coding sheets in [Experiment/coding_v5/](file:///d:/Thesis/Important/Causal%20Conflict%20Verbalization%20and%20Source%20Arbitration/Experiment/coding_v5/CODEBOOK_v5.md), and all **`231` unit tests pass** `[Verified]`.

### What Is Left for You to Finish

1. **Human Coding (Local, no GPU):** Fill in [coder_A_verdicts.csv](file:///d:/Thesis/Important/Causal%20Conflict%20Verbalization%20and%20Source%20Arbitration/Experiment/coding_v5/coder_A_verdicts.csv) / `coder_B_*` (`1,087` verdicts, `150` flips) to verify your automated parser isn't mislabeling verdicts.
2. **Pre-Freeze Check & Lock (`prereg-v5`):** Run the quick ChartQA `--print_example` render check on GPU, decide whether to re-run any modified dev cells (like the Math `none` behavioural prefill, where `69–89%` of models re-invented a Sentence-2 verdict after `{m_none}\n\n`), and then **git tag `prereg-v5`** (no tag exists yet).
3. **Run `--phase confirm` on GPU (L4/A100, `bfloat16`):** Run `base`, `donor`, and `transplant_v5.py --phase confirm --n_competent 250` on **unseen confirmatory items**. That produces your actual thesis findings.
4. **Write Chapters 1–7 in `Thesis/`:** Using [THESIS_NARRATIVE_AND_FRAMING_GUIDE.md](file:///d:/Thesis/Important/Causal%20Conflict%20Verbalization%20and%20Source%20Arbitration/Thesis/THESIS_NARRATIVE_AND_FRAMING_GUIDE.md), frame `v3` $\rightarrow$ `v4` $\rightarrow$ `v5` as a story of rigorous scientific self-correction culminating in your confirmatory results.
