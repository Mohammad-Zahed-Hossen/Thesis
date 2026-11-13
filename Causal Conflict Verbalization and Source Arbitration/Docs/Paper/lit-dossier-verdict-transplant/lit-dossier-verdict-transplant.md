# Literature dossier: verdict transplant under image–text conflict

*Prepared 2026-11-10 for the pre-registration of the v4/v5 verdict-transplant study (Qwen2.5-VL-3B-Instruct, Qwen2-VL-2B-Instruct).*

## 0. Scope, access and corrections to the brief

**What was read.** All ten arXiv IDs in the brief were downloaded from arXiv, and the text was extracted page by page. Page numbers below are 1-based PDF page indices. Each quote was copied from that extracted text. Where a paper was only skimmed, this dossier says so.

| ID | Read depth |
|---|---|
| 2610.38296 Hidden Commitment | pp. 1–7 in full |
| 2607.27304 CoT-Mediate | pp. 1–6 in full |
| 2604.14888 Sánchez Villegas et al. | pp. 1–9 in full, plus the appendix table on p. 20 |
| 2511.02243 Zhang et al. | pp. 1–8 in full |
| 2609.26986 Noncommutativity | pp. 1–5 in full |
| 2503.02199 Deng et al. | Targeted sections (pp. 1–2, 4–7) |
| 2504.08974 Mixed Signals | Abstract and pp. 1–4, 7 |
| 2602.14518 Diagnosing Knowledge Conflict | Abstract and pp. 2, 7–8, 17, 19 |
| 2606.28273 Vision-Default, Prior-Override | Abstract and p. 2 |
| 2505.23945 Balasubramanian et al. | Abstract and pp. 2, 5 |

**Not found.** No search returned a paper called "CMC-Bench". I ran an alphaXiv keyword search, a semantic search, a keyword search for "cross-modal conflict benchmark", and an OpenAlex search; the "CMC" keyword hits were all mathematics papers. I did not cite it. If you have a link, send it.

**Corrections to the brief.** Several titles and claims attached to these IDs don't match the papers.

| Brief says | Paper actually is |
|---|---|
| 2602.14518 "Knowledge Conflict in Multimodal Long CoT" | *Diagnosing Knowledge Conflict in Multimodal Long-Chain Reasoning* (Tang et al.). It probes and steers 7B/11B reasoning models (R1-Onevision, Ocean-R1, Llama-3.2V-CoT), not Qwen2.5-VL-3B. |
| 2606.28273 "multimodal reasoning / conflict resolution" | *Vision-Default, Prior-Override* (Lietzow et al.). The conflict is between **perception and parametric knowledge** (a blue strawberry), not between image and text. It uses activation patching. |
| 2505.23945 "multimodal conflict / source preference" | *A Closer Look at Bias and Chain-of-Thought Faithfulness of Large (Vision) Language Models*. It asks whether CoTs articulate biasing cues; it does not study source arbitration. |
| 2511.02243 "Modality Balance Points…" | *When Modalities Conflict: How Unimodal Reasoning Uncertainty Governs Preference Dynamics in MLLMs*. Its six models include Qwen2-VL-7B and Qwen2.5-VL-7B, **not 3B**. |
| 2610.38296 "Hidden Commitment in LLMs" | Correct title, ICML 2026. Text-only. The models are **Qwen 0.8B and Gemma 3 1B**. "Disclosure" here means *saying the documents conflict*, not *stating a reliability verdict*. |
| 2607.27304 "CoT-Mediate" | The paper is *Position, Not Provenance: Separating Reasoning Mediation from Sycophancy in Medical VLMs* (Bhowal et al., ICVGIP 2026). CoT-Mediate is the name of its framework. The models are LLaVA-Med and MedGemma on VQA-RAD, not Qwen. |
| 2604.14888 "answer inertia in 18 VLMs incl. Qwen2.5-VL-3B" | Correct for the reasoning-dynamics part. But the **text-hint / monitorability experiments use Qwen2.5-VL-7B/32B and Qwen3-VL-Thinking-8B/32B**, not 3B. |
| 2504.08974 "verbalized vs CoT mismatch detection" | Mixed Signals measures modality bias on five conflict datasets. "Verbalized", "CoT" and "Decomposed" are its three *mitigation* prompts for detecting mismatches. Its models are Qwen2-VL-7B/72B, Llama-3.2-90B and GPT-4o(-mini). |
| "exact mathematical … evidence proving … decoupled circuits" | **No paper here proves decoupled circuits.** Hidden Commitment shows the two states are best read at *different layers and positions* and that one is only partly steerable. The authors say "look like different internal states". |
| "KV-cache level" prefix forcing | CoT-Mediate does prefix forcing at the **prompt-string level**: one literal sequence, then greedy decoding of the answer. No KV-cache manipulation is described. |

**Discovered but read only as abstracts.** These are potentially close and should be read before submission:
- [Which Source Wins? (2608.17205)](https://www.alphaxiv.org/abs/2608.17205). This is the source of your GSM8K/SVAMP image-of-one-problem conflict construction and of ChartQA-Conflict. You must cite it.
- [Grounding on Request (2610.33841)](https://www.alphaxiv.org/abs/2610.33841). It tests whether a user can control which modality a VLM follows, which is directly relevant to the binding arm.
- [VLMs Integrate Conflicting Evidence Like Biased Bayesian Observers (2610.19407)](https://www.alphaxiv.org/abs/2610.19407).
- [Counterfactual Tests for CoT Faithfulness in VLMs (2609.06704)](https://www.alphaxiv.org/abs/2609.06704).

---

## 1. Executive evidence matrix

| Paper | Models | Conflict paradigm | Intervention | Key finding / metric | Difference from this thesis |
|---|---|---|---|---|---|
| **Deng et al. 2025**, *Words or Vision* (2503.02199, CVPR) | 10 VLMs (incl. Qwen2-VL-7B, Phi-3.5, GPT-4o) | Factual: matched, corrupted or irrelevant text vs. image (VQAv2 etc.) | Input text and instruction prompts; token order; SFT | "Blind faith in text". "Focus on Image" vs "Focus on Text" shifts Qwen2-VL-7B text preference only 16.8% → 14.2% ([p. 6](https://www.alphaxiv.org/pdf/2503.02199?page=6)). The instruction gives "a slight improvement (1–2%) in Macro accuracy" ([p. 7](https://www.alphaxiv.org/pdf/2503.02199?page=7)) | Perturbs inputs only; no reasoning or verdict |
| **Mixed Signals** (2504.08974, EMNLP Findings 2025) | Qwen2-VL-7B/72B, Llama-3.2-90B, GPT-4o(-mini) | Math, science and description conflicts; easy/hard | Prompting: Verbalized, CoT, Decomposed | Bias depends on difficulty: text is favoured on simple queries and images on complex ones; image-minus-text preference ranges from +56.8% to −74.4% ([p. 1](https://www.alphaxiv.org/pdf/2504.08974?page=1)) | Mitigation means *detecting* the mismatch; no test of whether a verdict steers the answer |
| **Balasubramanian et al.** (2505.23945) | Qwen2.5-VL 3B/7B/72B, InternVL, Llama-3.2V, reasoning LVLMs | Biasing cues (text hints, image cues), no source conflict | Bias injection; scoring whether the CoT articulates the bias | Image biases are rarely articulated; "inconsistent" reasoning, where the model "correctly reason[s] before abruptly changing answers" ([p. 1](https://www.alphaxiv.org/pdf/2505.23945?page=1)) | CoT faithfulness to injected cues, not to a source verdict |
| **Zhang et al.** (2511.02243) | LLaVA-1.5/1.6 (7B/13B), Qwen2-VL-7B, Qwen2.5-VL-7B | Factual, single-token attributes (colour etc.) on a toy dataset with controllable difficulty | None causal; difficulty manipulation; logit lens | Text-following probability falls monotonically with ΔH_rel. The **balance point** measures inherent preference. Qwen models lean towards vision. Near the balance point, models oscillate between modalities across layers ([pp. 6–8](https://www.alphaxiv.org/pdf/2511.02243?page=6)) | No verbalization; but it supplies the stratification variable |
| **Tang et al.** (2602.14518) | R1-Onevision-7B, Ocean-R1-7B (both Qwen2.5-VL-based), Llama-3.2V-11B-CoT | Objective vs. effective knowledge conflict in long CoT | Linear probes plus probe-guided steering | Conflict is linearly decodable in mid-to-late layers. **Directional asymmetry**: steering towards the model's reliability-aligned source is easy; "Reverse control remains challenging" ([p. 8](https://www.alphaxiv.org/pdf/2602.14518?page=8)) | Activation steering, not verbal verdicts; but it predicts asymmetric verdict effects (§2.3) |
| **Sánchez Villegas et al.** (2604.14888, COLM 2026) | 18 VLMs (Qwen2.5-VL 3B/7B/32B, Qwen3-VL, InternVL3/3.5) | MathVerse/PhyX modality variants; misleading text hints on Vision-Only | CoT truncation; confidence over CoT prefixes; hint injection; CoT monitors | **Answer inertia**: "early commitments to a prediction are reinforced, rather than revised" ([p. 1](https://www.alphaxiv.org/pdf/2604.14888?page=1)). Hints shift answers even when the visual evidence suffices, and the CoT only partly reveals this | Inputs are perturbed; the CoT is never edited; no source verdict |
| **Lietzow et al.** (2606.28273) | Qwen-VL 3B/7B, LLaVA-NeXT-7B, PaliGemma 3B/10B | Perception vs. parametric knowledge | Activation patching; head ablation | Sparse late "prior" heads (2.5–4.8%). Ablating them flips knowledge answers to visual answers in 68–96% of cases ([p. 1](https://www.alphaxiv.org/pdf/2606.28273?page=1)) | A different conflict type; mechanistic only |
| **CoT-Mediate** (2607.27304, ICVGIP 2026) | LLaVA-Med-7B, MedGemma-4B | Medical VQA; one clinical attribute edited inside the model's own CoT | **Prefix-forced continuation vs. re-prompt**; provenance labels; paraphrase floor | Mediation Faithfulness Score (MFS) 33.3% → 73.5% (LLaVA-Med) and 55.9% → 61.6% (MedGemma). The paraphrase floor is **1.7–3.3%** ([p. 6](https://www.alphaxiv.org/pdf/2607.27304?page=6)) | The **closest method**. It edits clinical content, not source-reliability verdicts; no modality conflict |
| **Noncommutativity** (2609.26986) | Qwen2.5-VL-3B, Idefics3-8B, Pixtral-12B (+ 3 speech models) | Factual: attachment vs. conflicting description | Swap evidence order with the instruction fixed | Placing the attachment last raises answers matching it by +9.8 to +28.1 pp. For Qwen2.5-VL-3B: +16.7 (GQA) and +15.0 (VQAv2). Under Deng's protocol: −13.7 vs. +17.7 ([pp. 3–4](https://www.alphaxiv.org/pdf/2609.26986?page=3)) | No verbalization; but it sets the order protocol |
| **Hidden Commitment** (2610.38296, ICML 2026) | Qwen 0.8B, Gemma 3 1B (text-only) | Two conflicting documents (FaithEval) | Residual readout; steering; analysis of sparse MLP writers | The source choice is a residual coordinate at layer 13 (held-out test AUROC 0.9945). Disclosure is read best at layer 17, before the response, and is only partly steerable ([pp. 3–6](https://www.alphaxiv.org/pdf/2610.38296?page=3)) | The **closest concept**. But the text is about *disclosing* a conflict, not a reliability verdict; it is text-only; and there is no prefix forcing |

---

## 2. Mechanistic deep dive: is "saying" separate from "choosing"?

### 2.1 What the anchor papers actually show

**Hidden Commitment (text LLMs).** The source choice becomes readable only around the answer span:

> "Prompt-final and first-response probes are much weaker in Qwen, while the clean readout appears when the model is about to produce and commit to one of the two supported answers." ([p. 4](https://www.alphaxiv.org/pdf/2610.38296?page=4))

The readout direction is a class-centroid difference, $\hat v_{doc} = (\mu_+ - \mu_-)/\lVert\mu_+ - \mu_-\rVert_2$. It is applied by steering $\tilde h_t^{(\ell)} = h_t^{(\ell)} + \delta\,\mathrm{RMS}(h_t^{(\ell)})\,\hat v_{doc}$ (Eqs. 2–3, [p. 3](https://www.alphaxiv.org/pdf/2610.38296?page=3)). Steering at δ = ±3 moves the share of answers using document 2 from 51.5% to 74.7% or 32.2%, while a random direction stays at 51.0–52.3% ([p. 4](https://www.alphaxiv.org/pdf/2610.38296?page=4)). Conflict disclosure behaves differently:

> "The best Qwen surfacing readout appears before the response begins, at pre response last in layer 17, while source choice is strongest around answer tokens at layer 13. […] The signals therefore look like different internal states rather than two labels for the same computation." ([p. 6](https://www.alphaxiv.org/pdf/2610.38296?page=6))

![Hidden Commitment layer/position sweep](figures/hidden-commitment-fig3-layer-sweep.png "Hidden Commitment, Figure 3: validation AUROC of the source-choice readout across layers and token positions in Qwen 0.8B. Readability is near ceiling only at decision tokens in middle layers; prompt-end ('pre-resp.') positions are weak. [p. 5](https://www.alphaxiv.org/pdf/2610.38296?page=5)")

**Sánchez Villegas et al. (VLMs).** "Answer inertia" is a **behavioural** finding about confidence trajectories, not a layer-level one. The confidence at CoT step *t* is the probability of the gold answer letter after the prefix `Answer:`, conditioned on $(x, \text{CoT}_{1:t})$ ([p. 4](https://www.alphaxiv.org/pdf/2604.14888?page=4)). Truncation accuracy is $\mathrm{Acc}(t)=\frac1N\sum_i \mathbb 1[\arg\max_y P_M(y\mid x_i,\text{CoT}^i_{1:t})=y_i^*]$ (Eq. 1, [p. 5](https://www.alphaxiv.org/pdf/2604.14888?page=5)). Instruction-tuned models such as Qwen2.5-VL change little as more CoT is included:

> "models often assign highest probability to their final answer before or within the first few CoT steps, indicating that errors arise from reinforcing early incorrect predictions." ([p. 6](https://www.alphaxiv.org/pdf/2604.14888?page=6))

The paper gives **no layer at which commitment happens**. Its monitorability experiments did not include the 3B model.

### 2.2 Your dev data in this light

These are recomputed from `results_v4/dev2_*.jsonl` on the 110 items that both single-source arms solve:

| Instruction | Contrast | Items whose answer changes | Δ image answers |
|---|---|---|---|
| Neutral (z0) | verdict `rel_image` vs `rel_text` | 35.5% | **+20.9 pp** |
| Neutral (z0) | wording `eq_a` vs `eq_b` | 24.5% | +7.3 pp |
| Conflict (z1) | verdict `rel_image` vs `rel_text` | **7.3%** | −1.8 pp |
| Conflict (z1) | wording `eq_a` vs `eq_b` | 22.7% | −1.8 pp |

*The interpretation below is mine, not a finding of the cited papers.*

1. **The verdict is not inert in general.** Under the neutral instruction, reversing it moves image answers by about 21 pp, nearly three times the wording shift. It is inert only under the conflict instruction. So a blanket "saying is not choosing" headline does not fit the data.
2. **The conflict instruction seems to saturate the direct path $Z\to Y$.** It says "Then solve the problem" after "read the typed text". v3 showed this instruction alone moves answers strongly towards the text (text-matching answers 4.2% → 36.1%). If $Z$ already fixes which problem gets solved, $M$ has no room to act. That is **instruction dominance**, not unfaithfulness. The binding arm (§3.2) is the test that tells these two apart.
3. **The pattern fits Hidden Commitment's timing result, but this is an inference.** In Qwen 0.8B, the source choice is not readable at the end of the prompt; it forms around the answer span. In your design, the verdict is forced *before* any solving tokens, so the commitment has not yet happened when the verdict is read. The verdict therefore *could* influence the choice. Observing that it does not, under z1, points to the instruction rather than to early lock-in.
4. **Your wording floor is about 10× CoT-Mediate's, and this is a design artefact to fix.** CoT-Mediate's "clinically null paraphrases flip 1.7% and 2.8% of items in Arm 1 and 3.3% and 0.5% in Arm 2" ([p. 6](https://www.alphaxiv.org/pdf/2607.27304?page=6)). That paper decodes at most 24 answer tokens after the forced CoT ([p. 5](https://www.alphaxiv.org/pdf/2607.27304?page=5)). Your harness lets the model generate up to 400 tokens of greedy solving after the prefix. Small changes to the prefix then grow into different trajectories, which inflates per-item churn and noise. **Remedy:** make the primary outcome a short-horizon readout. Force `####` immediately after the verdict, or after a fixed commit sentence, and score the log-likelihood margin between the image answer $y_I$ and the text answer $y_T$. Keep the full free solution as a secondary outcome.

### 2.3 Causal model and estimand

```
              U_i  (item: ΔH_rel, problem content)
             /   \
            v     v
  Z ──────► M ──► Y        O (evidence order) → M, Y
   \______________^        B (binding wording)  modifies M → Y
        direct path
```

- $Z$: instruction (neutral vs. conflict). $M$: the verbalized verdict. $Y \in \{\text{image}, \text{text}, \text{neither}\}$: which source's answer the output matches. $O$: evidence order. $B$: binding wording.
- Prefix forcing sets $M$ by intervention. This cuts $U\to M$ and identifies the **controlled direct effect of the verdict** at fixed $(z,o,b)$:
$$\mathrm{CDE}_{z,o,b} = P\big(Y{=}\text{img}\mid do(M{=}m_{\text{img}}),z,o,b\big) - P\big(Y{=}\text{img}\mid do(M{=}m_{\text{txt}}),z,o,b\big).$$
- This is **not** a natural indirect effect. Calling it "mediation" needs cross-world assumptions; the module docstring of `transplant_v4.py` already says so. The forced verdict is also off-policy, so the effect may not transfer to free generation.
- **Directional asymmetry should be expected.** Tang et al. report that "biasing the model toward fact-consistent, truth-anchored sources is significantly easier and more reliable than forcing it to rely on fact-inconsistent sources" ([p. 8](https://www.alphaxiv.org/pdf/2602.14518?page=8)). The analogue here: forcing the verdict *against* the model's own verdict (which your audit puts at about 89% "text more reliable") may do less than forcing it *with* that verdict. Pre-register two direction-specific contrasts, own-verdict vs. flipped and flipped vs. none, rather than only the pooled $\beta_{\text{Dir}}$.

---

## 3. Countermeasure architecture

### 3.1 Order counterbalancing

**What the literature fixes.** Noncommutativity holds the instruction $I$ before both sources and the question $q$ after them, and swaps only $P$ and $T$:
$x_{P\to T}=(I,P,T,q)$, $x_{T\to P}=(I,T,P,q)$ (Eq. 1, [p. 2](https://www.alphaxiv.org/pdf/2609.26986?page=2)). For Qwen2.5-VL-3B, letting the instruction move together with the text reverses the sign of the order effect:

![Noncommutativity Qwen2.5-VL-3B diagnostics](figures/noncommutativity-fig3-qwen25vl3b-instruction-ablation.png "Noncommutativity, Figure 3 (Qwen2.5-VL-3B, 20 exploratory examples). Panel (b): with the framing moving together with the text, placing the image last changes image answers by −28.6 pp; with the instruction fixed and only the evidence swapped, by +9.5 pp. The authors say the attention panel (a) is descriptive, not causal. [p. 4](https://www.alphaxiv.org/pdf/2609.26986?page=4)")

**Token layout for Qwen2(.5)-VL.** *None of the cited papers describes the tokenizer.* The following is from the Qwen chat template as `render_chat` uses it; verify it on Colab by printing `apply_chat_template(..., tokenize=False)`. Each `{"type":"image"}` entry in the content list becomes `<|vision_start|><|image_pad|><|vision_end|>` at that list position, and the processor expands `<|image_pad|>` to the image's patch tokens. Interleaving is therefore controlled entirely by the order of the content list:

```
image-first:  <|im_start|>user\n
              [I: instruction + binding clause]
              Source A: <|vision_start|><|image_pad|>…<|vision_end|>
              Source B: <typed problem text>
              [F: format line "…#### …"]<|im_end|>\n<|im_start|>assistant\n[forced verdict]
text-first:   identical, but Source A = typed text, Source B = image
```

Implementation:
- `render_chat(…, order)` builds `[text(I), text("Source A:"), image|text, text("Source B:"), text|image, text(F)]`.
- Counterbalance which source is labelled A or B, because labels carry their own bias. Noncommutativity likewise ran each condition with the A/B options swapped ([p. 2](https://www.alphaxiv.org/pdf/2609.26986?page=2)).
- Verdicts then name the source by modality ("the image" / "the typed text"), never by its A/B letter.
- Today `render_chat` always puts the image first (`harness_v4.py:290-292`).

### 3.2 Binding prompt

**What the literature says.**
- None of the papers read tests a *conditional* binding ("solve the problem from the source you judged more reliable").
- The nearest tests use *unconditional* source instructions, and those are weak:
  - Deng's "focus on image" moves text preference by 2.6 pp ([p. 6](https://www.alphaxiv.org/pdf/2503.02199?page=6)).
  - In Noncommutativity, adding "If the description conflicts with the image, prioritize the image" leaves the order effect at "89–145% of the original order effect" ([p. 3](https://www.alphaxiv.org/pdf/2609.26986?page=3)).
- *Grounding on Request* (2610.33841, abstract only) frames user control of modality as something to *learn*, which suggests prompting alone is insufficient. Read it before claiming novelty for the binding arm.

**Consequence: add an instruction-controllability ceiling.** Before reading the binding arm, measure how far an *explicit* source instruction moves answers:
- `explicit_image`: "…Then solve only the problem shown in the image."
- `explicit_text`: "…Then solve only the typed problem."

If even explicit instructions move answers only partly, the most the binding verdict can do is bounded by that gap. Report the binding effect as a fraction of this ceiling.

**Wording templates.** These remove the anaphora problem, since v3's "that problem" and v4's "the problem" are both ambiguous. Each has K = 4 paraphrases.

| Arm | Template (canonical) |
|---|---|
| Non-binding | "In two sentences, state whether the image and the typed text present the same problem, and say which source you consider more reliable. Then solve a problem." |
| Binding | "In two sentences, state whether the image and the typed text present the same problem, and say which source you consider more reliable. Then solve only the problem from the source you named as more reliable, and ignore the other problem." |
| Explicit-image (ceiling) | "…Then solve only the problem shown in the image." |
| Explicit-text (ceiling) | "…Then solve only the typed problem." |

**Manipulation check (free generation, no forcing).** Under binding, the model's *own* verdict should predict its answer source. If it does not, the binding wording failed, and the transplant result under binding cannot be read as unfaithfulness.

### 3.3 Minimal-edit verdict generator

Why: CoT-Mediate found that the *framing* of identical text matters. In re-prompting, self-attribution moved adoption "from 34.3% to 16.0%" for LLaVA-Med ([p. 1](https://www.alphaxiv.org/pdf/2607.27304?page=1)). Prefix-forcing inside the assistant turn avoids attribution labels altogether:

> "The edited tokens sit in the model's own context as if it had produced them, and the model is never told to pretend the reasoning was its own." ([p. 3](https://www.alphaxiv.org/pdf/2607.27304?page=3))

![CoT-Mediate mediation and provenance](figures/cotmediate-fig1-mfs-provenance.png "CoT-Mediate, Figure 1. (a) The Mediation Faithfulness Score rises from re-prompting (A1) to prefix-forcing (A2) in both medical VLMs. (b) Flip rates for byte-identical text under four source labels; LLaVA-Med discounts text labelled as its own. [p. 6](https://www.alphaxiv.org/pdf/2607.27304?page=6)")

**Algorithm**, applied to each item's own `conflict_full` donor verbalization $v$:
1. Segment $v$ with the existing `split_verbalization`. Keep only the verbalization part.
2. Find the **reliability clause**: the sentence where `stated_reliable_source(v)` matches, using the source-noun lexicon {image, picture, visual, typed text, text, written}.
3. **Own verdict**, $m_{own}$: $v$ unchanged. **Flipped verdict**, $m_{flip}$: swap only the source noun phrases in that clause (image ↔ typed text), keeping every other token. **No verdict**, $m_{\varnothing}$: delete the reliability clause.
4. **Gates** (adapted from CoT-Mediate's minimality and genuineness gates, [p. 3](https://www.alphaxiv.org/pdf/2607.27304?page=3)):
   - exactly one clause changed;
   - `stated_reliable_source(m_flip)` equals the opposite of `stated_reliable_source(v)`;
   - the token-level Jaccard similarity $J(v,m_{flip})$ is at least 0.85;
   - grammatical agreement checked by a regex for "is/are" and by human spot-checks;
   - items whose verdict is "both" or "unclear" are excluded and the exclusions counted.
5. **Paraphrase floor**, $m_{para}$: the same verdict direction as $v$, with one clause reworded by a fixed template set and the source noun kept. This is CoT-Mediate's "paraphrase control (zero clinical change)" ([p. 3](https://www.alphaxiv.org/pdf/2607.27304?page=3)), with a source verdict in place of the clinical content.
6. Keep the authored verdicts (`rel_image` / `rel_text`) as a secondary arm.

### 3.4 Statistics

**Unit of analysis.** Items $i$, verdict direction $d\in\{\text{own},\text{flip}\}$ (or {img, txt}), template $k\in\{1..4\}$, order $o\in\{IT, TI\}$, binding $b\in\{0,1\}$.

**Primary GLMM** (binary: does the answer match the image problem's answer):
$$\operatorname{logit} P(Y_{idkob}=\text{img}) = \beta_0 + \beta_1 D + \beta_2 O + \beta_3 B + \beta_4 (D\times B) + \beta_5 (D\times O) + u_i + v_k,\quad u_i\sim\mathcal N(0,\sigma_u^2),\ v_k\sim\mathcal N(0,\sigma_v^2).$$
- **$\beta_4$ is the key test**: whether binding makes the verdict decision-relevant. Add a by-item random slope for $D$ if the model converges.
- With $K=4$, $\sigma_v$ is poorly estimated. Back it up with the template-level permutation test: $\binom{8}{4}=70$ arrangements, so the smallest attainable $p$ is about 0.014.

**Graded outcome.** At a forced `####`, compute the length-normalized log-likelihood margin $\Delta\ell = \frac{1}{|y_I|}\log p(y_I\mid\cdot) - \frac{1}{|y_T|}\log p(y_T\mid\cdot)$. Fit a linear mixed model with the same fixed and random effects. This follows the "length-normalized conditional log-likelihood margin" of Which Source Wins (abstract) and Noncommutativity's log-odds swap score $C_\theta$ (Eqs. 3–4, [p. 2](https://www.alphaxiv.org/pdf/2609.26986?page=2)).

**Equivalence test (TOST) for the "verdict does not matter" claim**, separately within each binding level:
$$\Delta = P(\text{img}\mid m_{\text{img}}) - P(\text{img}\mid m_{\text{txt}}),\qquad H_{01}:\Delta\le -\epsilon,\quad H_{02}:\Delta\ge \epsilon.$$
- Reject both at α = 0.05 (equivalently, the 90% item-bootstrap CI lies inside $(-\epsilon,\epsilon)$) to conclude equivalence.
- The margin $\epsilon$ must be pre-registered. A defensible choice is $\epsilon$ = 7.3 pp, the largest wording-induced mean shift in dev. Report the per-item flip rates (verdict vs. wording) as a separate, descriptive *instability* quantity, not as the estimand.

**Stratification.** Compute $\Delta H_{rel}(x)=\frac{2(H^{(t)}-H^{(v)})}{H^{(t)}+H^{(v)}}$ (Zhang et al., [p. 6](https://www.alphaxiv.org/pdf/2511.02243?page=6)). Report the verdict effect inside and outside a ±0.5 window around each model's balance point, mirroring Zhang's ambiguous-region definition ([p. 7](https://www.alphaxiv.org/pdf/2511.02243?page=7)).
- **Adaptation needed.** Zhang uses the entropy of a single answer token over the vocabulary. GSM8K answers span several tokens, so use the length-normalized negative log-likelihood of the gold answer under `base_image` / `base_text` as $H^{(v)}$ / $H^{(t)}$. Say explicitly that this is an adaptation.

![Zhang et al. balance points](figures/zhang-fig4a-balance-points.png "Zhang et al., Figure 4a: the probability of following the text falls monotonically with relative uncertainty ΔH_rel. Each model's balance point is where its curve crosses 0.5; both Qwen-VL models sit left of zero, an inherent vision preference. The models are 7B, not the 3B/2B used here. [p. 6](https://www.alphaxiv.org/pdf/2511.02243?page=6)")

**Competency filter.** Keep only items where both single-source arms are correct. This is the filter Zhang et al. use: "we focus on the subset of instances where the model answers correctly in both the vision-only and text-only settings" ([p. 5](https://www.alphaxiv.org/pdf/2511.02243?page=5)). Noncommutativity does the same ("807 examples answered correctly from each source in isolation", [p. 4](https://www.alphaxiv.org/pdf/2609.26986?page=4)).

**Multiplicity and inference.** Follow CoT-Mediate:
- item-level bootstrap with 2,000 resamples;
- exact McNemar tests on paired discordant items;
- Holm correction over a pre-declared family ([p. 4](https://www.alphaxiv.org/pdf/2607.27304?page=4)).

---

## 4. Framing and novelty boundary

### 4.1 Defensible novelty claim

> In the eleven targeted sources and four abstract-level neighbours examined, no study prefix-forces **opposite source-reliability verdicts** into a vision-language model's own generation under image–text conflict, while holding evidence order, wording template and instruction fixed and testing whether a **binding instruction** makes the verdict decision-relevant.

- The closest **method** is CoT-Mediate: prefix-forced edits of the model's own reasoning, but on clinical attributes in medical VQA with no modality conflict.
- The closest **concept** is Hidden Commitment: choosing a source vs. disclosing it, but text-only and mechanistic.
- The **stimuli** come from Which Source Wins.

Do not claim "first" beyond these sources. Read 2610.33841 and 2610.19407 in full first.

### 4.2 Title

Use a neutral title until the confirmatory data are in:

**Does the Verdict Decide? Testing Whether Stated Source Reliability Steers Vision-Language Models under Image–Text Conflict**

### 4.3 Contribution statement (Chapter 1 draft; each item holds only if the confirmatory run supports it)

- **A controlled verdict-transplant protocol.** It forces on-policy, minimally edited source-reliability verdicts into the model's own response under image–text conflict. The design crosses verdict direction × wording template × evidence order × binding instruction, includes a pre-registered wording-noise floor and an instruction-controllability ceiling, and applies to a task-selection conflict (GSM8K/SVAMP) and an evidence conflict (ChartQA-Conflict).
- **An equivalence-bounded estimate of the verdict's causal effect** for Qwen2.5-VL-3B and Qwen2-VL-2B. It separates the effect of *what the verdict says* from the effect of *the instruction itself*, both with and without binding, and is broken down by relative single-source uncertainty and evidence order.
- **Measurement diagnostics.** It quantifies how instruction placement, evidence order, decoding horizon and repetition penalty change measured modality preference on these stimuli. It also shows why single-arm prompt contrasts overstate the effect of verbalization.

---

## 5. Remaining blind spots and likely reviewer objections

1. **"Reliability" is ill-posed for task-selection conflicts.** In GSM8K/SVAMP, both problems are valid; neither source is *wrong*. "The typed text is more reliable" may simply mean "the typed problem is the task". A reviewer can argue the verdict is not about reliability at all. Treat ChartQA-Conflict, where one source *is* wrong, as the setting where the reliability verdict is semantically meaningful. Consider making the evidence conflict primary for the 3B model, if its N allows.
2. **Instruction dominance vs. unfaithfulness.** The dev null appears only under the conflict instruction, so the binding arm and the explicit-source ceiling are both needed before any unfaithfulness claim (§2.2).
3. **The decoding horizon inflates noise.** The wording floor is about 10× CoT-Mediate's. Without a short-horizon or log-likelihood outcome, any equivalence test will be under-powered or meaningless (§2.2).
4. **Asymmetry.** Effects of the flipped verdict may differ from those of the own verdict (Tang et al.). Pooled estimates can hide this.
5. **Off-policy forcing.** Minimal edits reduce this but do not remove it. Report the perplexity of the forced verdict under the model as a covariate.
6. **Regex labels.** The verdict and solving-attempt labels from `score_v4` have not been validated by humans. Plan to code about 200 items with two coders and report κ.
7. **Generality.** Two small Qwen models from one family. Main venues will ask for a second family (e.g. InternVL or Idefics3, which Noncommutativity also ran).
8. **Unread neighbours.** 2610.33841 (Grounding on Request) is the most likely to overlap with the binding arm.

---

### Reference list (alphaXiv)

- Deng et al., *Words or Vision* — https://www.alphaxiv.org/abs/2503.02199
- Pezeshkpour et al., *Mixed Signals* — https://www.alphaxiv.org/abs/2504.08974
- Balasubramanian et al., *A Closer Look at Bias and CoT Faithfulness of L(V)LMs* — https://www.alphaxiv.org/abs/2505.23945
- Zhang et al., *When Modalities Conflict* — https://www.alphaxiv.org/abs/2511.02243
- Tang et al., *Diagnosing Knowledge Conflict in Multimodal Long-Chain Reasoning* — https://www.alphaxiv.org/abs/2602.14518
- Sánchez Villegas et al., *Reasoning Dynamics and the Limits of Monitoring Modality Reliance in VLMs* — https://www.alphaxiv.org/abs/2604.14888
- Lietzow et al., *Vision-Default, Prior-Override* — https://www.alphaxiv.org/abs/2606.28273
- Bhowal et al., *Position, Not Provenance* (CoT-Mediate) — https://www.alphaxiv.org/abs/2607.27304
- Li et al., *Same Evidence, Different Judgments* — https://www.alphaxiv.org/abs/2609.26986
- Assefa & Cho, *Hidden Commitment* — https://www.alphaxiv.org/abs/2610.38296
