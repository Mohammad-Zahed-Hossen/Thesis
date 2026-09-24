# Chat Transcript: VLM Contradiction Thesis

## User

I am conducting a technical feasibility autopsy on arXiv:2511.19199 (CLASH) and arXiv:2608.17205 (Which Source Wins?).

I am designing an undergraduate thesis experiment investigating this precise question:
"When image and text conflict, does requiring a VLM to explicitly identify/verbalize the contradiction causally improve its decisional arbitration, or does it merely act as post-hoc rationalization of an early logit bias?"

Read the full text, figures, tables, and appendices of these papers. Do NOT summarize the abstracts. Answer these 6 specific questions with direct quotes or section citations:

1. DATASET SCHEMA & GROUND TRUTH:

   - For CLASH: What is the exact format of a contradiction pair? Is there an authoritative ground truth defining which source is correct, or does it measure contradiction detection?
   - How many test samples exist, and what is the public download link (Hugging Face / GitHub)?
2. PRIOR EXPERIMENTS ON PROMPTING:

   - Did either paper test an intervention where the model is prompted to "Step 1: check for conflict, Step 2: answer"?
   - If yes, quote the exact prompt template and the reported result. If no, state explicitly that it was not evaluated.
3. PLACEBO & CAUSAL CONTROLS:

   - Did either paper compare conflict prompts against length-matched neutral prompts (placebos) or rationale prefilling (Lanham et al. style)?
4. UNIMODAL BASELINES:

   - Did either paper test text-only (blind LLM) and image-only baselines on their conflict stimuli? What were the scores?
5. MODEL SIZES & FEASIBILITY:

   - What are the smallest open-weight models evaluated (e.g., Qwen2-VL-2B, Qwen2.5-VL-3B, or SmolVLM)?
   - Is inference runnable zero-shot without fine-tuning?
6. AUTHORS' STATED LIMITATIONS:

   - Quote the most critical admissions in the 'Limitations' section regarding task directness, synthetic artifacts, or evaluation confounds.

## Aurelle

> **Read 2 papers**
> CLASH: A Benchmark for Cross-Modal Contradiction Detection · Which Source Wins? Task-Dependent Reliance in Vision-Language Models

> **Identifying scores and baselines**
>
> I need to find the exact scores for unimodal baselines for both items. The CLASH tool might have missed some pages and tables, depending on the specific query. It seems like an intervention in the CLASH might not be necessary. I should inspect the appendices for relevant pages. To make sure I cover everything, I may need to target both queries and consider a second round in parallel.

> **Read 2 papers**
> CLASH: A Benchmark for Cross-Modal Contradiction Detection · Which Source Wins? Task-Dependent Reliance in Vision-Language Models

> **Organizing paper citations**
>
> I need to provide a concise yet detailed answer, citing every named paper with proper links. I've got a tool for paper IDs linked to alphaxiv. Direct quotes will use specific tags, but I don't need to quote everything. I should mention the sample counts for each source and include public links. The prompt regarding CLASH needs to be checked for contradictions, distinguishing between prompts that specify conflicting instructions and what’s meant in the evaluation. I must ensure I cite exact pages for author limitations and synthetic artifacts.

> **Identifying limitations and citations**
>
> I need to clarify the limitations found on page 9 and mention that there’s no causal evidence regarding the intervention tests. I want to craft six numbered points, using accurate citations with anchors from snippets. I’ll link to the relevant papers on alphaxiv. It's important to note that the public download for CLASH is unavailable in the paper, and I need to state that there's no URL provided. I’ll make sure to differentiate between semantic schema and machine-readable field schema as well.

## Bottom line

Neither [CLASH](https://www.alphaxiv.org/abs/2511.19199) nor [Which Source Wins?](https://www.alphaxiv.org/abs/2608.17205) evaluates the intervention you care about: **first require the model to identify/verbalize a contradiction, then require it to arbitrate**. Consequently, neither paper can distinguish a causal improvement in arbitration from post-hoc rationalization of an already-established modality preference.

### 1. Dataset schema and ground truth

#### [CLASH](https://www.alphaxiv.org/abs/2511.19199)

A CLASH instance contains:

1. an MS COCO image;
2. a caption modified in exactly one object or attribute;
3. a targeted question about that changed element;
4. for multiple choice, four answer categories:
   - image-grounded answer,
   - text-grounded answer,
   - plausible distractor,
   - “Conflicting information – cannot answer.”

The paper states:

> “Each sample in CLASH consists of an image from MS COCO, a text description that contradicts the visual content in one aspect, and a targeted question about the contradictory element.” [Dataset Schema](https://www.alphaxiv.org/abs/2511.19199?page=3)

The contradiction is deliberately constructed by changing one element:

> “an LLM modifies exactly one element – an object or an objective attribute … while keeping the rest unchanged.” [Construction](https://www.alphaxiv.org/abs/2511.19199?page=3)

This is **not** a source-arbitration ground truth in which either the image or caption is declared correct. CLASH explicitly uses a “dual ground truth” formulation:

> “both image and text are valid but contradictory information sources.” [Ground Truth](https://www.alphaxiv.org/abs/2511.19199?page=3)

Thus, CLASH’s authoritative label is **that a contradiction exists**, not “the image wins” or “the text wins.” In the multiple-choice task, the correct answer is the contradiction/abstention option. The paper describes this as detecting contradictions and flagging them for review, rather than selecting a trusted modality. [Ground Truth](https://www.alphaxiv.org/abs/2511.19199?page=3)

The human-verified test set contains:

- **1,289 total samples**
- **655 object-level contradictions**
- **634 attribute-level contradictions**

The paper’s stated contribution is:

> “1289 human-verified test cases across fine-grained object and attribute categories.” [Dataset Size](https://www.alphaxiv.org/abs/2511.19199?page=2)

The training set is approximately **15,000 filtered samples**, generated from approximately **30,000 raw samples**. [Dataset Splits](https://www.alphaxiv.org/abs/2511.19199?page=3)

**Download link:** the paper does **not** provide a Hugging Face or GitHub dataset URL. It says only:

> “the codebase will be released upon acceptance.” [Release Status](https://www.alphaxiv.org/abs/2511.19199?page=5)

Therefore, based on the paper itself, there is no public download link to cite for CLASH.

#### [Which Source Wins?](https://www.alphaxiv.org/abs/2608.17205)

This paper uses three different conflict datasets:

- **GSM8K:** the rendered image of problem $i$ paired with the text of problem $(i+1)\bmod N$.
- **SVAMP:** the same shifted-pair construction, using a fixed 300-item subset.
- **ChartQA-Conflict:** a real chart paired with a manually written report supporting a different answer to the same question.

For GSM8K and SVAMP, the “ground truth” consists of two known candidate answers:

- $a_I$: answer supported by the image;
- $a_T$: answer supported by the text.

The paper gives the example where the image supports 18 and the text supports 3:

> “a response of $a_I=18$ is image-following and $a_T=3$ is text-following.” [Conflict Pairing](https://www.alphaxiv.org/abs/2608.17205?page=3)

This is therefore **not primarily a contradiction-detection benchmark**. It forces a response that can be attributed to one source, then measures how that source preference changes when one source is degraded.

Dataset sizes are:

- GSM8K: **1,319 problems**, with **1,304 distinct-answer pairs**; 15 equal-answer pairs remain in the saved outputs but are excluded from the decidable-preference denominator.
- SVAMP: **300 problems**, with **296 distinct-answer pairs**; 4 equal-answer pairs are excluded from the decidable denominator.
- ChartQA-Conflict: **229 valid conflicts**, after one of the original 230 manually reviewed items was removed by an entailment audit.

The paper states:

> “the complete GSM8K test set … (1,319 problems) and a fixed 300-item SVAMP subset.” [Arithmetic Datasets](https://www.alphaxiv.org/abs/2608.17205?page=6)

and:

> “the analysis contains 229 valid conflicts.” [ChartQA Size](https://www.alphaxiv.org/abs/2608.17205?page=6)

Public links supplied by the paper:

- Code: [multimodal-arbitration-artifact](https://github.com/Ro-netizen004/multimodal-arbitration-artifact)
- [ChartQA-Conflict dataset](https://huggingface.co/datasets/vlm-modality-research/chartqa-evidence-conflict-v2)
- [Chart-versus-table ablation](https://huggingface.co/datasets/vlm-modality-research/chartqa-evidence-conflict-table-v1)
- [Rendered GSM8K/SVAMP conflict stimuli](https://huggingface.co/datasets/vlm-modality-research/modality-conflict-arbitration-v2)

These releases are documented in §3.4. [Data Release](https://www.alphaxiv.org/abs/2608.17205?page=6)

### 2. Prompting experiments

#### [CLASH](https://www.alphaxiv.org/abs/2511.19199)

**No two-stage “Step 1: check for conflict; Step 2: answer” intervention was evaluated.**

The model-evaluation prompts were instead:

> “You are given an image and a textual description of the image.
> Use both the visual and textual information to answer the multiple-choice question below as accurately as possible.
> Choose the option that is best supported by both sources.
> If the image and the description contradict each other, or if one is missing key information, select the option ‘Conflicting information – cannot answer.’” [Evaluation Prompt](https://www.alphaxiv.org/abs/2511.19199?page=15)

The open-ended prompt similarly directly instructs the model to output “Conflicting information – cannot answer” when the inputs disagree. [Open-Ended Prompt](https://www.alphaxiv.org/abs/2511.19199?page=15)

That is an **explicit contradiction-aware instruction**, but it is not a sequential verbalization/arbitration intervention. There is no reported comparison between:

- ordinary answering;
- contradiction identification followed by answering;
- contradiction identification without answering;
- or prefilling a rationale before the answer.

#### [Which Source Wins?](https://www.alphaxiv.org/abs/2608.17205)

**No “Step 1: check for conflict; Step 2: answer” experiment was evaluated.**

The arithmetic prompt asks the model to:

> “Solve the problem step by step and end with #### <answer></answer>.” 

The later role-neutral prompt says:

> “You are given two conflicting evidence sources. Neither source is privileged.” [Role-Neutral Prompt](https://www.alphaxiv.org/abs/2608.17205?page=18)

The full ChartQA prompt is:

> “Question: {question}
> You are given two conflicting evidence sources. Neither source is privileged.
> Source {chart label} is the attached chart.
> Source {report label} is the textual report below:
> {report}
> Respond with exactly one line ‘#### <answer></answer>’, giving only the answer value with no explanation.” [ChartQA Prompt](https://www.alphaxiv.org/abs/2608.17205?page=18)

They compare the original framing with this role-neutral framing. This is a **prompt-framing comparison**, not a contradiction-verbalization intervention. The neutral framing changes the effect size in a model-dependent manner; for example, the paper reports that Qwen2.5-VL-7B’s GSM8K asymmetry changes from **+0.813** under the original prompt to **+0.060** under neutral framing. [Prompt Framing](https://www.alphaxiv.org/abs/2608.17205?page=7)

### 3. Placebos and causal controls

Neither paper includes the controls needed for a strong causal claim about verbalized contradiction reasoning.

Specifically, neither paper compares a conflict-checking prompt against:

- a length-matched neutral prompt;
- a semantically matched but contradiction-free prompt;
- a rationale-prefilling condition;
- a Lanham-style “rationalization” control;
- or a condition in which the model is given a contradiction statement without being asked to use it.

[CLASH](https://www.alphaxiv.org/abs/2511.19199) does have automated and human quality controls for constructing examples, but these are **dataset-validation controls**, not causal controls on prompting. Its test prompt directly tells the model what to do if it detects contradiction. [Quality Control](https://www.alphaxiv.org/abs/2511.19199?page=3)

[Which Source Wins?](https://www.alphaxiv.org/abs/2608.17205) has several useful controls, but they address different confounds:

- counterbalanced Source A/B labels;
- image versus text degradation arms;
- unimodal accuracy-loss calibration;
- chart versus table-image substitution;
- alternative CLL length normalizations.

The authors explicitly describe the role-neutral prompt as a framing manipulation, not a placebo or rationale control. [Experimental Logic](https://www.alphaxiv.org/abs/2608.17205?page=4)

For your causal question, the key missing comparison is: **does requiring a contradiction statement change the subsequent answer relative to an otherwise identical prompt?** Neither paper runs it.

### 4. Unimodal baselines

#### [CLASH](https://www.alphaxiv.org/abs/2511.19199)

No image-only or text-only baseline is reported on the CLASH conflict stimuli.

The reported CLASH experiments use the image and conflicting caption together. Table 1 reports multimodal multiple-choice outcomes such as contradiction, image-grounded, text-grounded, distractor, and incorrect responses. For example:

- InstructBLIP-T5-xxl: **63.87% contradiction**
- InternVL 1.5: **16.71%**
- LLaVA-1.5-7B: **0.13%**
- Qwen2.5-VL-7B: **7.79%**
- GPT-5: **86.78%**
- Gemini 2.5 Pro: **88.48%**

[CLASH Results](https://www.alphaxiv.org/abs/2511.19199?page=6)

But the “Image” and “Text” columns are **multimodal model answers that follow one source**, not scores from separate image-only and text-only models. Therefore, CLASH supplies no unimodal baseline score against which to measure contradiction-prompt effects.

#### [Which Source Wins?](https://www.alphaxiv.org/abs/2608.17205)

Yes. This paper explicitly evaluates each problem in text-only and image-only conditions:

> “We also evaluate each problem separately in text-only and image-only conditions.” [Unimodal Baselines](https://www.alphaxiv.org/abs/2608.17205?page=4)

The baseline table reports pooled image-only/text-only accuracy over the arithmetic runs and degradation levels:

| Model                |      Image-only |       Text-only |
| -------------------- | --------------: | --------------: |
| Idefics3-8B          |           86.1% |           78.1% |
| Phi-3.5-Vision       |           85.3% |           74.6% |
| Qwen2-VL-2B          |           72.6% |           58.6% |
| Qwen2.5-VL-7B        |           62.6% |           68.8% |
| LLaVA-OneVision-7B   |           86.2% |           75.1% |
| LLaVA-1.6-7B         |           78.1% |           72.7% |
| **Arm-pooled** | **78.6%** | **71.4%** |

These are **unimodal accuracy baselines**, not contradiction-detection accuracy. They are used to calibrate how much information is lost when a source is degraded. [Unimodal Accuracy](https://www.alphaxiv.org/abs/2608.17205?page=15)

The paper does not provide a separate CLASH-style “contradiction detected” score for text-only or image-only conditions, because [Which Source Wins?](https://www.alphaxiv.org/abs/2608.17205) is measuring source-following/reallocation rather than contradiction awareness.

### 5. Model sizes and feasibility

#### [CLASH](https://www.alphaxiv.org/abs/2511.19199)

The smallest explicitly named open-weight models in the main results are approximately **7B parameters**, including:

- MiniGPT4-7B;
- LRV-MiniGPT4-7B;
- LLaVA-1.5-7B;
- LLaVA-OneVision-7B;
- Qwen2VL-Instruct-7B;
- Qwen2.5VL-Instruct-7B.

The paper also evaluates mPLUG-Owl-1 and other models, but it does not report a 2B or 3B model such as Qwen2-VL-2B, Qwen2.5-VL-3B, or SmolVLM. The model list is given in §4.1. [Models](https://www.alphaxiv.org/abs/2511.19199?page=5)

Zero-shot inference is feasible for the baseline evaluation: the paper uses official implementations and checkpoints and does not fine-tune the models for the main evaluation. However, CLASH also contains a separate LoRA fine-tuning experiment on LLaVA-1.5-7B and mPLUG-Owl-1. The baseline and fine-tuned conditions should not be conflated. [Fine-Tuning](https://www.alphaxiv.org/abs/2511.19199?page=12)

#### [Which Source Wins?](https://www.alphaxiv.org/abs/2608.17205)

The smallest open-weight model is **Qwen2-VL-2B-Instruct**. The six primary open-weight models span **2B–8B parameters**:

- Qwen2-VL-2B;
- Phi-3.5-Vision-4B;
- Qwen2.5-VL-7B;
- LLaVA-1.6-Mistral-7B;
- LLaVA-OneVision-7B;
- Idefics3-8B.

InternVL2-8B is used for generated-answer analysis only. [Model Coverage](https://www.alphaxiv.org/abs/2608.17205?page=3)

Yes, the evaluation is **zero-shot inference without fine-tuning**. The models are loaded from Hugging Face checkpoints, using `device_map="auto"`, bfloat16 where supported, and no quantization. [Inference Setup](https://www.alphaxiv.org/abs/2608.17205?page=12)

The authors ran each open-model inference job on one 48 GB NVIDIA L40S GPU, with approximately 400 GPU-hours for the final experiments. [Hardware](https://www.alphaxiv.org/abs/2608.17205?page=13)

For an undergraduate thesis, the most practical starting point is therefore [Qwen2-VL-2B-Instruct](https://huggingface.co/Qwen/Qwen2-VL-2B-Instruct), followed by a 4B or 7B comparison model. The experiments do not require fine-tuning unless you choose to add it as a separate manipulation.

### 6. Authors’ stated limitations

#### [CLASH](https://www.alphaxiv.org/abs/2511.19199)

The most relevant limitation is that the task is intentionally direct and elementary:

> “it focuses on object– and attribute–level contradictions, rather than spatial, relational, temporal or causal conflicts.” [Limitations](https://www.alphaxiv.org/abs/2511.19199?page=8)

The authors explain why:

> “before evaluating whether models can detect complex inconsistencies, we must first establish whether they can perform basic cross-modal comparison on directly observable properties.” [Task Directness](https://www.alphaxiv.org/abs/2511.19199?page=8)

They also acknowledge domain limitations:

> “extending it to specialized domains like medical, scientific, or technical content remains an important direction for future work.” [Domain Limitation](https://www.alphaxiv.org/abs/2511.19199?page=8)

Regarding synthetic artifacts, the paper says:

> “although some synthetic examples may contain lower quality outputs despite multi-stage filtering” [Synthetic Data Limitation](https://www.alphaxiv.org/abs/2511.19199?page=8)

The construction also deliberately avoids image editing because it could introduce visual confounds:

> “we focus on textual rather than visual contradictions because image editing techniques … often produce unrealistic or artifactual images that introduce confounding factors.” [Synthetic Artifacts](https://www.alphaxiv.org/abs/2511.19199?page=3)

For your thesis, this means CLASH is useful for a clean **contradiction-detection** manipulation, but it does not establish which modality is factually correct and does not isolate arbitration after contradiction verbalization.

#### [Which Source Wins?](https://www.alphaxiv.org/abs/2608.17205)

This paper’s most important admission for your question is explicit:

> “our framework measures forced source arbitration under reduced legibility rather than factual reliability or conflict awareness.” [Conflict Awareness Limitation](https://www.alphaxiv.org/abs/2608.17205?page=9)

The authors continue:

> “Consequently, we do not test whether models detect the contradiction, express uncertainty, or abstain.” [Unmeasured Abilities](https://www.alphaxiv.org/abs/2608.17205?page=9)

That is decisive: [Which Source Wins?](https://www.alphaxiv.org/abs/2608.17205) does not measure the latent variable your proposed intervention targets.

They also admit that the two source types differ in directness:

> “the reversal therefore reflects reallocation between sources with potentially different baseline directness, not a comparison between equally accessible visual and textual evidence.” [Directness Confound](https://www.alphaxiv.org/abs/2608.17205?page=9)

The task construction does not isolate task, representation, and conflict type:

> “the two conflict settings do not isolate task, representation, and conflict construction independently.” [Design Confound](https://www.alphaxiv.org/abs/2608.17205?page=9)

The ChartQA review is also not independent:

> “reviewed by two of the authors, who were not blind to the counterfactual design, rather than independent annotators.” [Annotation Confound](https://www.alphaxiv.org/abs/2608.17205?page=9)

Finally, the paper acknowledges that the CLL measure is only an imperfect proxy:

> “The CLL margin also agrees with generated source choices on 75.4% of attributable trials, indicating that it is a useful but imperfect proxy for behavioral reliance.” [CLL Limitation](https://www.alphaxiv.org/abs/2608.17205?page=9)

## Implication for your thesis design

The cleanest experiment would add a factorial manipulation absent from both papers:

1. **No conflict instruction:** answer normally.
2. **Conflict-check instruction:** explicitly identify whether the sources contradict.
3. **Conflict-check plus arbitration:** identify the contradiction, state which source supports each candidate answer, then decide.
4. **Neutral verbalization placebo:** produce an equally long explanation unrelated to contradiction detection.
5. **Rationale-prefill condition:** provide or force a contradiction rationale before the final answer.
6. **Answer-only condition:** suppress the rationale while retaining the same underlying task.

The crucial outcome is not merely final accuracy. Record:

- pre-verbalization source preference, ideally via candidate log-probabilities;
- contradiction-detection accuracy;
- post-verbalization source preference;
- answer changes induced by the verbalization;
- consistency between stated rationale and selected source.

A genuine causal arbitration effect would require the contradiction-verbalization intervention to change source choice **relative to a length-matched neutral placebo**, not merely produce a plausible explanation after the original choice was already determined.

## User

(File attachment: text/plain)

Target Papers: Seeing without Looking: 2605.22903 and Evidence-Order Calibration: 2609.09184

## Aurelle

> **Read 2 papers**
> Seeing without Looking: Do Vision-Language Benchmarks Really Test Vision? · Evidence-Order Calibration for Selective Visual Reasoning under Progressive Loss of Question-Critical Evidence

> **Considering token usage**
>
> I'm looking at the token usage for different thresholds like 0, 25, 50, and 75, but not 100. I also see global black settings at 0.5 and 0.75, and I'm focusing on items that aren't image-dependent. It seems like I might need to incorporate some math rendering here. My goal is to create a response that is both concise and detailed, so let's think through the best way to present this!

## 1. Blind-solvability controls

### *Seeing without Looking* ([arXiv:2605.22903](https://www.alphaxiv.org/abs/2605.22903))

The paper does **not** report one aggregate “blank-image accuracy.” It reports no-image accuracy by model and benchmark. The no-image condition is implemented as a dummy black image:

> “No-image. We replace the input image with a dummy black image of fixed size.” [No-Image Protocol](https://www.alphaxiv.org/abs/2605.22903?page=17)

For the main binary benchmark results, the complete-removal accuracies are:

| Model           | POPE | A-OKVQA | MME |
| --------------- | ---: | ------: | --: |
| Qwen3-VL-32B    |  50% |     51% | 54% |
| InternVL3-8B    |  50% |     48% | 56% |
| Qwen3-VL-8B     |  50% |     47% | 52% |
| Gemma3-12B      |  57% |     46% | 56% |
| Qwen3-VL-4B     |  50% |     47% | 51% |
| LLaVA-1.5-7B    |  50% |     38% | 50% |
| Molmo-7B-D-0924 |  51% |     47% | 51% |

These are Table 5’s “No Image” values. [No-Image Accuracy](https://www.alphaxiv.org/abs/2605.22903?page=6)

For the expanded-answer POPE condition, the no-image accuracies are also near chance:

- LLaVA: **50%**
- Gemma3: **50%**
- Qwen-32B: **50%**
- Qwen3-8B: **50%**
- Qwen3-4B: **50%**
- InternVL: **47%**
- Molmo: **51%**

[Expanded POPE](https://www.alphaxiv.org/abs/2605.22903?page=20)

The authors therefore establish that the models are **not completely independent of the image**: when the image is entirely removed, performance generally falls to chance. Their more interesting result is that partial degradation preserves unexpectedly high accuracy. For example, at 75% black occlusion, POPE accuracy remains 81% for Qwen3-VL-32B, 80% for Gemma3-12B, and 76% for LLaVA-1.5-7B. [Partial Occlusion](https://www.alphaxiv.org/abs/2605.22903?page=6)

The paper does **not** formally stratify items into “image-dependent” versus “prior-solvable” subsets. It discusses those possibilities conceptually:

> “It may reflect (i) redundancy in visual representations, (ii) the possibility that the benchmark can be solved using only coarse-grained visual information, or (iii) the presence of strong language-side regularities.” [Interpretive Alternatives](https://www.alphaxiv.org/abs/2605.22903?page=2)

It also restricts some entity-level analyses to positive POPE examples and reports a 149-example positive subset, but that is a **label-based subset**, not a validated image-dependent/prior-solvable partition. [Positive Subset](https://www.alphaxiv.org/abs/2605.22903?page=16)

### *Evidence-Order Calibration* ([arXiv:2609.09184](https://www.alphaxiv.org/abs/2609.09184))

This paper does not use a globally blank image as its principal control. It masks a question-critical region progressively. Clean-image accuracy is **0.642**, and accuracy under complete critical-region masking is **0.358**, a **28.4-point decline**. [Critical Masking](https://www.alphaxiv.org/abs/2609.09184?page=4)

The matched non-critical control falls only from **0.641 to 0.635**, a **0.6-point decline**. [Matched Control](https://www.alphaxiv.org/abs/2609.09184?page=4)

It does not use the labels “image-dependent” and “prior-solvable,” but it does perform a related diagnostic: it identifies question-critical regions and compares their masking with equally sized non-critical regions. The authors also explicitly note that some answers survive complete masking through context or priors:

> “some correct answers survive full masking through context or priors.” [Failure Modes](https://www.alphaxiv.org/abs/2609.09184?page=6)

That is evidence of prior/context solvability, but not a formal per-item classification into prior-solvable and image-dependent questions.

## 2. Uncertainty and confidence metrics

### *Seeing without Looking*

The paper does **not** report:

- Normalized Sequence Entropy;
- Expected Calibration Error (ECE);
- selective risk or risk–coverage curves across masking levels.

It does report several other confidence-related quantities:

1. **Decision margin** for binary POPE answers:

$$
\Delta = \log p(\mathrm{yes})-\log p(\mathrm{no}).
$$

[Decision Margin](https://www.alphaxiv.org/abs/2605.22903?page=4)

2. **Mean Reciprocal Rank (MRR)** for open-ended entity generation.
3. **Mean prediction probability** and logit-margin shifts under entity interventions.

For example, on the 117-example entity-swap set, MRR falls from **0.0322** to **0.0101**, while mean prediction probability falls from **0.000690** to **0.000142**. [Entity-Swap Confidence](https://www.alphaxiv.org/abs/2605.22903?page=6)

The paper therefore studies whether decision support weakens when evidence is removed, but it does not evaluate calibration monotonicity with an entropy-vs-mask curve in the way your proposed experiment requires. Its global experiments use no image, black occlusion, and noise/blur conditions, but the reported main metric is accuracy; its entity-level confidence analysis is based mainly on $\Delta$ and probability distributions.

### *Evidence-Order Calibration*

This paper directly measures the quantities most relevant to your thesis:

- mean sequence log-confidence;
- mean predictive entropy;
- EMVR, the evidence monotonicity violation rate;
- AUROC and AUPRC;
- Brier score;
- AURC, area under the risk–coverage curve.

The feature vector includes the final hidden representation, mean sequence log-confidence, and mean predictive entropy:

$$
x_{i,k}=[h_{i,k};c_{i,k};H_{i,k}]\in\mathbb{R}^{2050}.
$$

[Confidence Features](https://www.alphaxiv.org/abs/2609.09184?page=3)

The central monotonicity expectation is:

$$
R_0\ge R_{.25}\ge R_{.5}\ge R_{.75}\ge R_1.
$$

[Monotonicity Target](https://www.alphaxiv.org/abs/2609.09184?page=1)

A violation occurs when reliability increases after additional evidence is removed:

$$
v_{i,k}=\mathbf{1}[R_{i,k+1}>R_{i,k}].
$$

The paper aggregates this as:

$$
\mathrm{EMVR}
=
\frac{1}{4N}
\sum_{i=1}^{N}\sum_{k=0}^{3}v_{i,k}.
$$

[EMVR](https://www.alphaxiv.org/abs/2609.09184?page=3)

The native VLM’s aggregate confidence does respond in the expected direction:

- mean log-confidence: **−0.318 → −0.570**
- mean entropy: **0.826 → 1.382**

But its trajectory-wise behavior is highly non-monotonic:

- native-confidence EMVR: **0.436**
- violations in **162/176 trajectories**, or **92.0%**
- among clean-correct trajectories, EMVR remains **0.383**

[Non-Monotonic Confidence](https://www.alphaxiv.org/abs/2609.09184?page=4)

The paper does measure selective risk. Native confidence has the best AURC:

- native confidence: **0.265**
- BCE-only head: **0.315**
- BCE + order head: **0.316**

At approximately 50% coverage, selective risk is 0.273 for native confidence versus 0.359 for either learned head. [Selective Risk](https://www.alphaxiv.org/abs/2609.09184?page=5)

It does **not** use ECE or Normalized Sequence Entropy by those names. It uses mean token-level predictive entropy, but EMVR—not ECE—is its primary evidence-order diagnostic.

## 3. Masking protocol and bounding boxes

### *Seeing without Looking*

The paper uses several physically different interventions.

#### Global token dropping

At the embedding level, it randomly removes image-token embeddings after the vision encoder and projection/merger stage:

$$
[E^{\text{text}},E^{\text{img}}]
\rightarrow
[E^{\text{text}},E^{\text{kept}}_{\text{img}}].
$$

The tested drop ratios are $r\in\{0,0.25,0.5,0.75\}$. Thus, the token-dropping experiment does **not** include a 100% image-token-drop condition. [Token Dropping](https://www.alphaxiv.org/abs/2605.22903?page=16)

#### Global pixel-level degradation

- **No-image:** replace the image with a black dummy image.
- **Black occlusion:** black out the top half for $p=0.5$; top half plus bottom-left quarter for $p=0.75$; the entire image for $p=1.0$.
- **Noise:** mix the original image with random noise:

$$
I'=(1-p)I+pN.
$$

[Global Degradation](https://www.alphaxiv.org/abs/2605.22903?page=17)

#### Entity-level evidence removal

The target entity is:

1. extracted from the question using GPT-5;
2. localized with Grounding DINO;
3. segmented with SAM2.

The interventions are:

- **BlackMask:** black out only the SAM2 segmentation mask;
- **BlackBox:** black out the entire Grounding DINO bounding box;
- **EntitySwap:** replace the entity with an unrelated image-generated object using Gemini.

[Entity Interventions](https://www.alphaxiv.org/abs/2605.22903?page=4)

Coordinates and masks are used internally by the experiment, but the paper does **not** state that a public Hugging Face dataset or coordinate manifest is released. The supplementary material contains implementation descriptions and output artifacts, but no public dataset URL is provided in the paper.

### *Evidence-Order Calibration*

Masking is local and bounding-box-based. Let $M_q$ be the question-critical object box. At masking severity $\lambda$, a centered gray rectangle is drawn inside the box. Its side lengths scale as $\sqrt{\lambda}$, so the masked area scales linearly with $\lambda$:

- $\lambda=0$: no masking;
- $\lambda=.25$: 25% of the box area;
- $\lambda=.5$: 50%;
- $\lambda=.75$: 75%;
- $\lambda=1$: the entire box covered.

[Mask Geometry](https://www.alphaxiv.org/abs/2609.09184?page=3)

The matched non-critical control uses an equally sized box selected by a deterministic grid search. It must be in bounds and have IoU $\le 0.05$ with the critical box. [Non-Critical Boxes](https://www.alphaxiv.org/abs/2609.09184?page=4)

The paper explicitly names the accepted manifest:

> `data/gqa/manifests/gqa_evidence_scaled_accepted.json`

[Accepted Manifest](https://www.alphaxiv.org/abs/2609.09184?page=3)

Thus, the critical-region coordinates appear to be part of the released experiment manifest, at least according to the paper’s file structure. However, the paper does not provide a public GitHub or Hugging Face URL from which that manifest can be downloaded.

The held-out transfer condition uses local Gaussian blur rather than masking:

$$
r(\lambda)=\min\left(24,\;0.15\lambda\min(w,h)\right),
$$

with blur applied only inside $M_q$. [Blur Transfer](https://www.alphaxiv.org/abs/2609.09184?page=4)

## 4. What remains unknown

### *Seeing without Looking*

This paper does **not** establish a continuous functional response curve for confidence on genuinely image-dependent questions.

It does evaluate multiple global degradation levels:

- token dropping at 0%, 25%, 50%, and 75%;
- black occlusion at 50%, 75%, and 100%;
- noise/blur at comparable global severities;
- complete no-image input.

However:

1. the token-drop experiment stops at 75%;
2. the no-image condition is a separate binary endpoint;
3. the paper does not classify individual questions by image dependence;
4. it does not plot normalized sequence entropy or likelihood margin against percentage of decisive evidence removed;
5. its localized entity interventions are not a five-level trajectory.

The closest confidence analysis is a distributional comparison of $\Delta=\log p(\text{yes})-\log p(\text{no})$ under original, BlackMask, BlackBox, EntitySwap, and no-image conditions. That is multiple-condition evidence, but not the specific continuous image-dependent calibration curve in your proposed design. [Margin Trajectories](https://www.alphaxiv.org/abs/2605.22903?page=5)

### *Evidence-Order Calibration*

This paper **does** evaluate the exact five-level structure:

$$
\lambda\in\{0,.25,.5,.75,1\}.
$$

It uses 176 trajectories and 880 masking conditions, and it reports both aggregate confidence changes and within-trajectory monotonicity. [Five-Level Trajectories](https://www.alphaxiv.org/abs/2609.09184?page=3)

So it establishes an empirical response curve at the aggregate and per-trajectory level—but not a smooth functional law. The primary finding is precisely that confidence is **not reliably monotonic** as evidence is removed:

> “native confidence violates the desired direction 307 times.” [Trajectory Violations](https://www.alphaxiv.org/abs/2609.09184?page=4)

The paper therefore rejects both simplistic possibilities:

- confidence is not entirely insensitive to visual evidence, since accuracy and aggregate confidence change;
- confidence is not a reliable monotonic proxy for evidence loss, since 92% of trajectories contain at least one upward confidence violation.

Its own interpretation is that confidence is evidence-sensitive in aggregate but structurally unreliable at the individual-trajectory level.

## 5. Reproducibility and artifacts

### *Seeing without Looking*

The paper does not provide a public GitHub repository or Hugging Face dataset URL in the text available here. It names the source benchmarks—POPE, A-OKVQA, MME, and AMBER—and describes generated/intervened subsets, but no release URL is supplied.

Therefore, the reproducibility answer from the paper is:

- **GitHub:** no URL stated.
- **Hugging Face:** no URL stated.
- **Coordinate/mask release:** no public URL or explicit downloadable coordinate package stated.

The implementation is substantially based on standard Hugging Face Transformers:

> “Our implementation is primarily based on the Hugging Face transformers library.” [Implementation](https://www.alphaxiv.org/abs/2605.22903?page=16)

But the paper’s actual experiments used RTX 4090 GPUs with bfloat16, and models include 8B, 12B, 32B, and other relatively large VLMs. [Inference Hardware](https://www.alphaxiv.org/abs/2605.22903?page=16)

A 16 GB Colab GPU is therefore plausible for **Qwen3-VL-4B or LLaVA-1.5-7B with careful memory management**, but not a faithful drop-in reproduction of the entire model suite—particularly Qwen3-VL-32B, Gemma3-12B, or InternVL3-8B in bfloat16. The paper does not claim single-16-GB-GPU reproducibility.

### *Evidence-Order Calibration*

The paper also does not provide a GitHub or Hugging Face URL in the paper text. It gives an internal manifest path:

```text
data/gqa/manifests/gqa_evidence_scaled_accepted.json
```

but not a public repository address. Consequently:

- **GitHub:** no URL stated.
- **Hugging Face:** no URL stated.
- **Manifest:** named in the paper, but public accessibility is not established by the paper itself.

The model is Qwen2.5-VL-3B-Instruct, non-quantized, with only lightweight linear heads trained afterward. The authors ran it on an RTX 5060 Laptop GPU with approximately 8 GB of memory and explicitly allowed CPU/disk offload:

> “device map=auto permitted CPU/disk offload where necessary.” [Execution Environment](https://www.alphaxiv.org/abs/2609.09184?page=3)

Therefore, the evaluation should be feasible on a 16 GB GPU using standard Transformers, assuming the manifest and scripts are available. The VLM itself is frozen; the post-hoc reliability head is inexpensive. Exact environment versions were Python 3.14.5, PyTorch 2.11.0+cu128, and Transformers 5.16.1. [Software Stack](https://www.alphaxiv.org/abs/2609.09184?page=3)

## 6. Authors’ stated limitations

### *Seeing without Looking*

The paper’s explicit caveat about image-token dropping is important:

> “the visual tokens used in this intervention are taken after the vision encoder, where bidirectional attention may already have mixed information across patches.” [Token-Drop Caveat](https://www.alphaxiv.org/abs/2605.22903?page=3)

This means deleting a post-encoder token does not necessarily remove the corresponding spatial evidence. The authors partially address this by also intervening directly on input pixels, but the two interventions are not equivalent. [Token-Drop Caveat](https://www.alphaxiv.org/abs/2605.22903?page=3)

The strongest dataset and question-heuristic limitations are:

- POPE is a binary yes/no object-presence benchmark, so answer priors are unusually powerful.
- The positive subset contains only 149 of the 300 POPE examples.
- Entity-level analysis requires a single clearly identifiable target.
- GPT-5 extracts the entity, Grounding DINO localizes it, and SAM2 segments it.
- samples are discarded when localization, segmentation, or editing fails;
- the final entity-swap set contains only 117 examples.

[Entity Filtering](https://www.alphaxiv.org/abs/2605.22903?page=17)

The paper also acknowledges that the observed behavior is model-dependent. For example, some models maintain high accuracy under black masking, while others decline more sharply; unknown-option usage is highly heterogeneous. In the expanded POPE condition, the Unknown Rate is 0% for LLaVA and Qwen3-8B under several conditions but rises to 81% for Qwen-32B under 75% noise. [Model-Dependent Uncertainty](https://www.alphaxiv.org/abs/2605.22903?page=20)

### *Evidence-Order Calibration*

The limitations section states:

> “the frozen benchmark contains only 176 accepted trajectories from one GQA-derived subset and one primary VLM family/model.” [Dataset and Model Scope](https://www.alphaxiv.org/abs/2609.09184?page=7)

The questions are narrowly concentrated:

> “Questions are concentrated in color, identity, material, and shape categories.” [Question Scope](https://www.alphaxiv.org/abs/2609.09184?page=7)

The evidence annotations are not exhaustive human rationales:

> “Evidence regions are scene-graph object boxes rather than exhaustive human rationales.” [Evidence Annotation Limitation](https://www.alphaxiv.org/abs/2609.09184?page=7)

The audit is also primarily automated:

> “the main audit used automated visual quality control with only a limited human spot-check.” [Audit Limitation](https://www.alphaxiv.org/abs/2609.09184?page=7)

The authors explicitly warn about semantic answer matching:

> “Strict normalized exact matching treats semantically close responses such as ‘tan’ and ‘khaki’ as different.” [Matching Limitation](https://www.alphaxiv.org/abs/2609.09184?page=7)

The matched non-critical control is also imperfect:

> “Matched non-critical boxes are equally sized and geometrically separated but can overlap other annotated objects; only 32/170 have zero annotated-object overlap.” [Control Limitation](https://www.alphaxiv.org/abs/2609.09184?page=7)

Finally, the authors explicitly limit architecture generalization:

> “a larger study should test multiple VLM families, datasets, evidence annotations, and intervention mechanisms before generalizing beyond this controlled setting.” [Generalization Limitation](https://www.alphaxiv.org/abs/2609.09184?page=7)

## Feasibility conclusion for your proposed experiment

[Evidence-Order Calibration](https://www.alphaxiv.org/abs/2609.09184) is the closer methodological template: it already implements the five masking levels, extracts sequence confidence and token entropy, and evaluates monotonicity, AUROC, Brier score, and selective risk. Its central result is that **aggregate confidence falls and entropy rises, but individual confidence trajectories are usually non-monotonic**.

[Seeing without Looking](https://www.alphaxiv.org/abs/2605.22903) supplies the complementary blind-solvability warning: complete image removal drives accuracy toward chance, but partial degradation can preserve high accuracy, and no formal item-level prior-solvability partition is performed.

For an undergraduate replication, the strongest design would combine them by adding:

1. a validated **image-dependent subset**;
2. a matched **prior-solvable subset**;
3. masking at exactly $0\%,25\%,50\%,75\%,100\%$;
4. sequence entropy, mean token log-likelihood, and candidate likelihood margin;
5. ECE and selective risk at every masking level;
6. per-item monotonicity tests in addition to aggregate curves;
7. a non-critical-region mask control;
8. a text-only/no-image solvability control.

That would directly test whether uncertainty tracks loss of decisive visual evidence, rather than merely tracking whether the language prior can still produce the benchmark answer.

## User

(File attachment: text/plain)

arXiv:2608.05381 (C3PO) and arXiv:2608.00076 (Which Modality Decides? / CMA).

## Aurelle

> **Read 2 papers**
> C$^3$PO: Evaluating Cross-Modal Composition and Counterfactual Performance in Omnimodal Models · Which Modality Decides? Counterfactual Modality Attribution for Multimodal LLMs

> **Gathering information on C3PO**
>
> I need to answer specific questions and gather more information on C3PO's appendices, especially about limitations and URLs. It seems I also need to look into counts related to paired counterfactuals, possibly referencing CC 1979 and whether they're paired. I should inspect the relevant pages to ensure accuracy. The total paired instances for CMA likely come from synthetic MNIST and OpenAI test sizes, but I'll need to check for the tables in the appendices.

> **Read 2 papers**
> C$^3$PO: Evaluating Cross-Modal Composition and Counterfactual Performance in Omnimodal Models · Which Modality Decides? Counterfactual Modality Attribution for Multimodal LLMs

## Bottom line

Neither [C³PO](https://www.alphaxiv.org/abs/2608.05381) nor [Which Modality Decides?](https://www.alphaxiv.org/abs/2608.00076) tests whether a generated chain-of-thought remains faithful after a **minimal counterfactual pixel edit**. C³PO evaluates short final answers and auxiliary caption-fidelity/attention probes; CMA evaluates a classifier’s modality attribution under diffusion-generated counterfactuals. Neither performs rationale truncation, rationale corruption, or rationale prefilling.

There is also a dataset-count inconsistency in C³PO: the paper states 3,404 samples, while Table 1 totals 3,342 and reports 1,979 counterfactual-conflict samples; Appendix Table 13 reports 2,041 counterfactual-reasoning samples and again totals 3,404.

## 1. Counterfactual datasets and artifacts

### C³PO

C³PO is not built from paired real-image/manual-edit examples in the usual vision-counterfactual sense. It uses real “base media” and automatically generates complementary modalities and queries through templates:

> “Our automated pipeline selects real-world ‘base media’ (video/image/audio) from public datasets and uses it as an anchor to synthesize the missing complementary modalities.” [Data Construction](https://www.alphaxiv.org/abs/2608.05381?page=3)

The counterfactual-conflict templates introduce deliberate contradictions between modalities. For example:

> “a video shows an event triggered by a clearly visible mechanism, while the audio confidently (mis)attributes it to some other cause not present in the video.” [Counterfactual Conflict](https://www.alphaxiv.org/abs/2608.05381?page=4)

The pipeline is fully automatic:

> “Gemini-3-Pro generates the query along with detailed descriptions of the complementary modalities … The corresponding image and audio files are then synthesized using state-of-the-art generative models.” [Generation Pipeline](https://www.alphaxiv.org/abs/2608.05381?page=4)

So C³PO uses **template-controlled multimodal synthesis anchored to real media**, not manually edited image pairs and not a dedicated diffusion-inpainting counterfactual procedure like CMA.

The paper reports:

- **3,404 total samples** in the prose and Appendix Table 13;
- **1,363 Information Composition samples**;
- **2,041 Counterfactual Reasoning samples** in Appendix Table 13;
- but Table 1 reports **1,979 Counterfactual Conflict samples** and totals **3,342**.

Table 1’s displayed tier counts are:

| Category                | Tier 1 | Tier 2 | Tier 3 | Tier 4 | Total shown |
| ----------------------- | -----: | -----: | -----: | -----: | ----------: |
| Information Composition |    692 |    624 |     47 |      0 |       1,363 |
| Counterfactual Conflict |    729 |    795 |    292 |    163 |       1,979 |
| Table total             |  1,133 |  2,295 |    467 |    218 |       3,342 |

[Count Inconsistency](https://www.alphaxiv.org/abs/2608.05381?page=3)

Appendix Table 13 instead reports:

- Counterfactual Reasoning: **2,041**
- Information Composition: **1,363**
- Total: **3,404**

[Appendix Counts](https://www.alphaxiv.org/abs/2608.05381?page=20)

Therefore, the safest answer is:

- **claimed total:** 3,404;
- **counterfactual count in Table 1:** 1,979;
- **counterfactual count in Appendix Table 13:** 2,041;
- **internally consistent total in Appendix Table 13:** 3,404.

The paper does not provide a public Hugging Face or GitHub URL in the text. It says that implementation details are in the appendix, but no repository link is given. The only explicit infrastructure statement is that the code used for the experiments ran on local GPU resources; there is no cited public artifact URL.

### Which Modality Decides? / CMA

CMA constructs image-only, text-only, and joint counterfactuals using **coupled image and text diffusion**, guided by a classifier.

For image counterfactuals, it uses DDPM-style diffusion and a classifier-gradient objective. Image-only generation changes the image while holding text fixed:

> “classifier guidance is applied only to the image diffusion model while the accompanying text remains fixed.” [Image Counterfactuals](https://www.alphaxiv.org/abs/2608.00076?page=4)

It also uses dynamic inpainting to preserve areas that should not change:

> “Dynamic inpainting further preserves unchanged regions by restoring pixels whose predicted changes remain below a threshold.” [Dynamic Inpainting](https://www.alphaxiv.org/abs/2608.00076?page=4)

Text-only counterfactuals use differentiable text diffusion, and joint counterfactuals update both modalities simultaneously under shared classifier guidance. [Joint Counterfactuals](https://www.alphaxiv.org/abs/2608.00076?page=4)

CMA evaluates:

1. **Synthetic Multimodal MNIST**

   - colored MNIST digit;
   - text prompt containing a color-to-code mapping;
   - Balanced, Image-Biased, and Text-Biased variants.
2. **Multiclass OpenI**

   - chest X-ray plus radiology report;
   - labels derived from Problems or MeSH terms;
   - custom canonical pathology mapping and stratified splits.

[Evaluation Data](https://www.alphaxiv.org/abs/2608.00076?page=5)

The paper does not state exact train/validation/test sample counts for either benchmark in the text returned here. It therefore does not support a precise total number of paired counterfactual test instances. It shows qualitative counterfactual examples and reports aggregate attribution accuracy, but does not give a complete test-set cardinality in the main paper.

The paper also says:

> “Code for reproducing all results is included in the supplement and will be released publicly on a dedicated GitHub repository upon acceptance.” [Artifact Status](https://www.alphaxiv.org/abs/2608.00076?page=5)

No actual GitHub URL or Hugging Face URL is provided. Thus, the exact answer is:

- **GitHub URL:** not supplied; repository described as forthcoming.
- **Hugging Face URL:** none supplied.
- **downloadable paired-counterfactual test set:** not established by the paper.

## 2. Rationale and chain-of-thought evaluation

### C³PO

C³PO does **not** evaluate free-form rationales or chain-of-thought faithfulness after counterfactual edits.

The ordinary evaluation asks for a short answer, not an explanation:

> “The responses are expected to be as specific as possible … and within a few words.” [Answer Format](https://www.alphaxiv.org/abs/2608.05381?page=5)

Scoring is:

1. normalized string exact match;
2. if that fails, semantic-equivalence judgment by Qwen3-Omni.

> “first, a normalized string exact match is performed … If this match fails, we use Qwen3-Omni as an LLM-judge.” [Answer Scoring](https://www.alphaxiv.org/abs/2608.05381?page=5)

This is a **final-answer correctness metric**, not rationale faithfulness. The judge is not GPT-4o; it is Qwen3-Omni. The authors additionally compare Qwen3-Omni judgments with Gemini-3-Flash judgments:

- average agreement: **93%**
- Cohen’s $\kappa$: **0.88**
- minimum $\kappa$: **0.74**
- maximum $\kappa$: **0.98**

[Judge Agreement](https://www.alphaxiv.org/abs/2608.05381?page=13)

C³PO does have an E3 “caption-fidelity probe,” but that is not a chain-of-thought faithfulness evaluation. It tests whether modality content can be reconstructed, not whether the model’s verbal reasoning updates consistently with a changed visual fact. [Mechanistic Probes](https://www.alphaxiv.org/abs/2608.05381?page=6)

### CMA

CMA does not generate or evaluate model rationales. Its model is a multimodal classifier with a lightweight two-layer MLP head, not a generative VLM producing chain-of-thought explanations:

> “We use Gemma-3-4B-IT … with a lightweight two-layer MLP classification head.” [Classifier Setup](https://www.alphaxiv.org/abs/2608.00076?page=5)

CMA evaluates the classifier’s logit for the original predicted class under four modality coalitions and computes Shapley values. Its evidence score is the classifier’s logit, not a rationale score:

$$
v(S)=f_{\hat y}(\tilde{x}^{I}_{S},\tilde{x}^{T}_{S}).
$$

[Coalition Value](https://www.alphaxiv.org/abs/2608.00076?page=4)

Thus, neither paper asks whether a rationale mentions the edited visual attribute, whether a rationale changes when the image changes, or whether rationale tokens track the counterfactual decision.

## 3. Causal interventions on rationales

Neither paper evaluates:

- rationale corruption;
- rationale truncation;
- rationale token deletion;
- rationale prefilling;
- “answer after this rationale” interventions;
- or Lanham-style causal tests in which a supplied rationale is manipulated before final-answer generation.

C³PO’s E1 probe issues a structured prompt to obtain content descriptions for attention analysis, and E3 measures modality-content reconstruction. Those are observational probes, not interventions on a generated rationale. [Probe Protocols](https://www.alphaxiv.org/abs/2608.05381?page=13)

CMA has no generated rationale stream to corrupt or truncate. Its counterfactual intervention is applied to the input image, text, or both during diffusion, and the output is a classifier logit and predicted class.

Consequently, neither study can establish that a verbal explanation causally mediates the final decision.

## 4. Baselines and unimodal shortcuts

### C³PO

C³PO does not report separate text-only and image-only **accuracy baselines on the same counterfactual test set**.

It does analyze modality dominance and reports failure categories such as:

- audio-only;
- image-only;
- text-prior;
- incomplete fusion.

But these are post hoc failure-mode labels, not independently trained or evaluated unimodal baselines. In the paper’s decomposition, **86–95% of failures are dominance-driven**. [Dominance Failures](https://www.alphaxiv.org/abs/2608.05381?page=8)

The paper also uses a self-audit to remove examples solvable through unimodal shortcuts:

> “Samples that can be solved through unimodal shortcuts, commonsense priors, query leakage, or ambiguous reasoning must be revised before the model outputs the sample.” [Shortcut Filtering](https://www.alphaxiv.org/abs/2608.05381?page=4)

That is dataset filtering, not a text-only/image-only baseline.

### CMA

CMA creates **image-only and text-only counterfactuals**, but these are not unimodal baseline evaluations. They are interventions used to compute the four Shapley coalitions:

- original image + original text;
- original image + counterfactual text;
- counterfactual image + original text;
- counterfactual image + counterfactual text.

[Shapley Coalitions](https://www.alphaxiv.org/abs/2608.00076?page=5)

CMA does not report a table of text-only accuracy and image-only accuracy on the counterfactual test sets. Its controlled ground truth is instead model bias:

- Image-Biased classifier should be attributed to image;
- Text-Biased classifier should be attributed to text;
- Balanced classifier requires both modalities.

The reported CMA result is **98% modality-attribution accuracy** on the controlled synthetic setting, not a unimodal predictive score. [Attribution Accuracy](https://www.alphaxiv.org/abs/2608.00076?page=6)

The OpenI example does expose a shortcut: removing ECG leads from the image changes the classifier’s prediction from Nodule to Normal, while a text-only counterfactual fails to flip it because the original image shortcut remains. [OpenI Shortcut](https://www.alphaxiv.org/abs/2608.00076?page=5)

But this is a qualitative counterfactual example, not a reported unimodal baseline score.

## 5. Model sizes, hardware, and feasibility

### C³PO

The smallest open-weight models evaluated are:

- **Qwen2.5-Omni-3B**
- **Gemma-3n-E4B**, approximately 4B effective parameters
- **InstructOmni-4B**

The full model table also includes MiniCPM-Omni-7B, Qwen2.5-Omni-7B, InstructOmni-8B, Qwen3-Omni, Phi-4-Multimodal, VITA-1.5, and PandaGPT-7B. [Open Models](https://www.alphaxiv.org/abs/2608.05381?page=6)

The paper’s computational setup is not a single-GPU Colab setup for the complete evaluation:

> “All other computational experiments were ran on a mix of 4x A100 80GB GPUs and 2x RTX 5000 32GB GPUs.” [Hardware](https://www.alphaxiv.org/abs/2608.05381?page=29)

The principal reasons are:

- omnimodal models;
- video/audio/image/text input;
- attention and logit-lens probes;
- generation and evaluation of complementary media;
- architecture-specific internal probing.

The paper explicitly reports that E1 probing could not be conducted on video samples because of GPU memory limits, and that some models were excluded because their architectures were incompatible with the probes. [Probe Constraints](https://www.alphaxiv.org/abs/2608.05381?page=9)

A reduced inference experiment on a single 16 GB GPU might be possible for some 3B–4B models after removing video, generation, and internal probes, but that would not reproduce the full C³PO pipeline. The paper does not claim full Colab Pro feasibility.

### CMA

The multimodal classifier is **Gemma-3-4B-IT** with a lightweight two-layer classification head. [CMA Model](https://www.alphaxiv.org/abs/2608.00076?page=5)

This is the smallest and apparently only explicitly named backbone in the CMA paper. The diffusion components add substantial cost:

- DDPM image diffusion;
- RDLM text diffusion;
- synchronized reverse diffusion;
- classifier-gradient guidance;
- image and text counterfactual generation;
- four coalition evaluations per example.

The authors state:

> “diffusion-based counterfactual generation introduces additional computational cost compared with gradient- or perturbation-based explainability methods, limiting the current implementation to offline analysis.” [Compute Limitation](https://www.alphaxiv.org/abs/2608.00076?page=7)

The paper does not provide a hardware specification, GPU-hour estimate, or a 16 GB memory claim. Standard Transformers inference for the Gemma-3-4B classifier may be feasible on a 16 GB GPU, but **faithfully reproducing CMA’s coupled image/text diffusion generation is not established as a Colab-Pro workload**. The diffusion priors and gradient-guided reverse processes are the computational bottleneck.

## 6. Authors’ stated limitations

### C³PO

The paper’s limitations begin with dependence on a single powerful generator:

> “Gemini currently being the strongest available omnimodal model was used to generate the samples.” [Generator Dependence](https://www.alphaxiv.org/abs/2608.05381?page=9)

This matters because the generator determines the queries, complementary modalities, contradictions, and much of the dataset’s linguistic style. It creates a risk of **generator-specific artifacts and bias**, even though the paper attempts self-audit and media verification.

The paper also acknowledges that final accuracy depends on the judge:

> “the final accuracy entirely depends on the LLM judge’s (Qwen3-Omni) decisions.” [Judge Dependence](https://www.alphaxiv.org/abs/2608.05381?page=9)

They perform an agreement check with Gemini-3-Flash, but that does not eliminate shared model biases in automated semantic evaluation. [Judge Check](https://www.alphaxiv.org/abs/2608.05381?page=13)

The paper additionally states:

> “the probing experiments (specifically E1) could not be conducted on video samples due to GPU memory constraints” [Video Probe Limitation](https://www.alphaxiv.org/abs/2608.05381?page=9)

and:

> “some open-source models had to be excluded from these experiments due to their architecture which was incompatible with our experiments.” [Architecture Limitation](https://www.alphaxiv.org/abs/2608.05381?page=9)

Finally, C³PO’s own filtering acknowledges the danger of artifacts and shortcuts: it must check media verification, query leakage, naturalness, realism, and unimodal shortcut solvability. [Filtering Limitations](https://www.alphaxiv.org/abs/2608.05381?page=4)

### CMA

CMA’s limitation section is unusually direct about counterfactual validity:

> “the quality of the attribution depends on the quality of the generated counterfactuals.” [Counterfactual Quality](https://www.alphaxiv.org/abs/2608.00076?page=7)

The authors acknowledge that realistic-looking diffusion edits can still be imperfect:

> “imperfect counterfactual generation may affect attribution quality.” [Generation Artifacts](https://www.alphaxiv.org/abs/2608.00076?page=7)

They also explicitly reject interpreting CMA as a causal effect in the underlying data-generating process:

> “CMA provides model-relative, reference-dependent counterfactual attributions rather than causal effects in the underlying data-generating process.” [Reference Dependence](https://www.alphaxiv.org/abs/2608.00076?page=7)

And:

> “different valid counterfactual references may lead to different attribution scores.” [Reference Dependence](https://www.alphaxiv.org/abs/2608.00076?page=7)

That admission is directly relevant to your proposed experiment: a diffusion-generated image edit is not automatically a minimal or uniquely correct pixel intervention. The resulting attribution can depend on which valid-looking counterfactual the generator happens to produce.

CMA also operates only at modality level:

> “the current framework … does not identify which individual image regions or textual spans within a modality are responsible for a prediction.” [Granularity Limitation](https://www.alphaxiv.org/abs/2608.00076?page=7)

Thus CMA can say “the image mattered more than the text,” but cannot verify whether the model’s verbal explanation mentioned the exact edited visual attribute or whether the decisive pixel region was faithfully represented in a rationale.

## Feasibility conclusion for your thesis

C³PO is useful for studying **cross-modal conflict and modality dominance**, but it does not provide a clean visual counterfactual-rationale faithfulness test. Its counterfactual samples are automatically synthesized, its answers are short, and its judge scores final-answer semantic equivalence rather than explanations.

CMA provides stronger counterfactual machinery—image-only, text-only, and joint edits with Shapley attribution—but it uses a classifier rather than a rationale-generating model and explicitly concedes reference dependence and imperfect counterfactual generation.

For your thesis, the missing experiment is:

1. generate a normal multimodal answer plus rationale;
2. make a minimal, independently validated pixel edit;
3. regenerate the answer and rationale;
4. score whether the rationale updates on the edited attribute;
5. intervene on the rationale itself by truncating, corrupting, or prefilling it;
6. compare final-answer changes against rationale changes.

A useful faithfulness metric would separately measure:

- **decision flip rate** after the pixel edit;
- **rationale attribute-update rate**;
- **rationale–image entailment**;
- **rationale–answer consistency**;
- and the causal effect of rationale corruption on the final answer.

Neither paper currently supplies those measurements.
