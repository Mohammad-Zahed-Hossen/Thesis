# Post-v5 Direct PDF Audit & New Related-Work Verification

**Audit date:** 2026-11-14
**Trigger & scope:** Directly verify the **5 core papers** previously audited only via AlphaXiv summaries (`2603.01437`, `2510.27484`, `2307.13702`, `2609.25366`, `2026.magmar-main.3`) after downloading their canonical PDFs into `Docs/Paper/`, and perform full autopsies on the **2 Chapter 2 leads** surfaced during Pass 2 (`2606.22862` and *Same Reasoning, Different Words: Testing Linguistic Invariance in Chain-of-Thought Monitoring*).
**Ground-truth references:** [THESIS_LITERATURE_KNOWLEDGE_BASE.md](../THESIS_LITERATURE_KNOWLEDGE_BASE.md), [PREREGISTRATION_VERDICT_TRANSPLANT.md](../../PREREGISTRATION_VERDICT_TRANSPLANT.md), [lit-dossier-verdict-transplant.md](../lit-dossier-verdict-transplant/lit-dossier-verdict-transplant.md), [prereg-freeze-audit.md](../prereg-freeze-audit/prereg-freeze-audit.md).
**Citation & epistemic convention:** All page numbers are **1-based PDF page indices**. `[Verified]` denotes direct inspection of the downloaded PDF or open official proceedings webpage in this audit; `[Inferred]` denotes methodological interpretation for this thesis; `[PDF Not Available]` marks non-downloadable gated sources.

---

## 0. Download Verification & Integrity Summary (`Docs/Paper/`)

All 5 core PDFs and 1 Chapter 2 lead (`2606.22862.pdf`) downloaded cleanly from their canonical arXiv / ACL Anthology URLs into `Docs/Paper/` (verified with `%PDF-` header, non-trivial byte sizes, and full PyMuPDF text extraction):

| # | Local File | Canonical URL | Size (Bytes) | PDF Pages | Header Check | Audit Status |
|---|---|---|---:|---:|---|---|
| 15 | [2603.01437.pdf](../2603.01437.pdf) | https://arxiv.org/pdf/2603.01437 | 5,549,259 | 23 | `%PDF-` | `[Verified]` Full PDF read |
| 16 | [2510.27484.pdf](../2510.27484.pdf) | https://arxiv.org/pdf/2510.27484 | 13,192,552 | 35 | `%PDF-` | `[Verified]` Full PDF read |
| 17 | [2307.13702.pdf](../2307.13702.pdf) | https://arxiv.org/pdf/2307.13702 | 1,091,161 | 14 | `%PDF-` | `[Verified]` Full PDF read |
| 18 | [2609.25366.pdf](../2609.25366.pdf) | https://arxiv.org/pdf/2609.25366 | 2,648,969 | 27 | `%PDF-` | `[Verified]` Full PDF read |
| 19 | [2026.magmar-main.3.pdf](../2026.magmar-main.3.pdf) | https://aclanthology.org/2026.magmar-main.3.pdf | 1,512,758 | 10 | `%PDF-` | `[Verified]` Full PDF read |
| Lead 1 | [2606.22862.pdf](../2606.22862.pdf) | https://arxiv.org/pdf/2606.22862 | 757,682 | 10 | `%PDF-` | `[Verified]` Full PDF read |
| Lead 2 | `[PDF Not Available]` | https://openreview.net/forum?id=uul4iRQSJ2 | — | — | HTTP 403 Forbidden | Abstract & venue `[Verified]` via [NeurIPS 2026 Workshop page](https://neurips.cc/virtual/2026/loc/sydney/178182) & [author CV](https://joefsmith.github.io/cv.pdf) |

For Lead 2 (*Same Reasoning, Different Words: Testing Linguistic Invariance in Chain-of-Thought Monitoring*, Joe Smith, TAE @ NeurIPS 2026), automated HTTP requests to `openreview.net/forum?id=uul4iRQSJ2`, `openreview.net/pdf?id=uul4iRQSJ2`, and `api2.openreview.net/notes?id=uul4iRQSJ2` all returned `HTTP Error 403: Forbidden`, and checks across arXiv API, OpenAlex API, `joefsmith.github.io`, `cv.pdf`, and `github.com/joefsmith` found no public arXiv ID or open PDF mirror. Following project epistemic rules, it is recorded as `[PDF Not Available]` and audited strictly from the official open NeurIPS 2026 workshop abstract and author CV.

---

## 1. PDF-Verified Autopsies of the 5 Core Papers (#15–#19)

### 1.1 `2603.01437` — *Post-Hoc Reasoning in Chain of Thought: Decoding and Steering Pre-Committed Answers*

- **Citation & Venue:** Kyle Cox, Darius Kianersi, Adrià Garriga-Alonso (2026), *Post-Hoc Reasoning in Chain of Thought: Decoding and Steering Pre-Committed Answers*, `arXiv:2603.01437v2` (23 Jul 2026); footer prints *"Mechanistic Interpretability Workshop at the 43rd International Conference on Machine Learning, Seoul, South Korea, 2026."* `[Verified, p. 1]`
- **Design & Parameters Cross-Checked:**
  - **Models (§2.1, App. F):** 5 instruction-tuned models — `Gemma 2` (`2B-it`, `9B-it`) and `Qwen 2.5` (`1.5B-Instruct`, `3B-Instruct`, `7B-Instruct`) — plus 1 reasoning model in App. F (`GPT-OSS 20B`). `[Verified, pp. 2, 21]`
  - **Datasets & Splits (§2.1):** Anachronisms, Logical Deduction, Social Chemistry, Sports Understanding formatted as binary A/B (option order randomized per example), 4 few-shot CoT demonstrations, `500` train / `500` test per dataset, sampled at `temperature = 0.7`. `[Verified, p. 2]`
  - **CoT Interventions (§2.2, Table 8):** Randomly samples `50` initially correct test generations per model–dataset cell; replaces CoT with `"..."` (*Ellipses*) or a mistake (*Incorrect CoT*). Ellipsis flip rates are $\le 20\%$ in `18/20` model–dataset pairs (exceptions on Sports Understanding: `52%` Gemma 2 9B, `32%` Qwen 2.5 1.5B), while Incorrect CoT reaches `52–78%` on Anachronisms (`78%` on both Qwen 2.5 3B and 7B). `[Verified, pp. 2, 20]`
  - **Probing & Steering (§2.3–§2.5):** Difference-of-means probe $w^{(\ell)} = \mu_{\text{yes}}^{(\ell)} - \mu_{\text{no}}^{(\ell)}$ extracted on residual-stream activation at the last pre-CoT prompt token $t_0$ (the colon in `"Let's think step by step:"`), cosine-similarity scoring $s_j^{(\ell)} = \cos(x_{j,t_0}^{(\ell)}, w^{(\ell)})$. Activation addition $\tilde{x}_t^{(\ell^\star)} = x_t^{(\ell^\star)} + \alpha w^{(\ell^\star)}$ applied at layer $\ell^\star$ (best probe AUC) over $\alpha \in \{0, \pm 2, \dots, \pm 20\}$ for every token $t > t_0$, across the $S_{\text{yes}}$ / $S_{\text{no}}$ initially-correct test subsets (excluding $\alpha$ yielding $<20$ parsed outputs), compared against norm-matched orthogonal random steering $r_j$ on `50` random test examples. Traces judged by `GPT-5-mini` into `{Sound reasoning, Non-entailment, Confabulation, Hallucination}` (`min(50, n)` flips sampled per setting; 200-item Run 1/2 judge consistency `81.5%`, App. C.3 Table 7). `[Verified, pp. 3, 5, 17]`

![Pre-CoT probe AUC across Gemma-2 and Qwen2.5 models in Cox et al. (2026)](figures/2603-01437-table3.png "Table 3 from Cox et al. (2026) showing pre-CoT probe AUCs: Qwen2.5-3B drops from 0.996 on Anachronisms to 0.690 on Logical Deduction [p. 4](https://arxiv.org/pdf/2603.01437)")

![CoT omission (Ellipses) and Incorrect CoT sensitivity table in Cox et al. (2026)](figures/2603-01437-table8.png "Table 8 from Cox et al. (2026) showing Ellipses vs. Incorrect CoT flip rates (%) across 5 models and 4 tasks [p. 20](https://arxiv.org/pdf/2603.01437)")

- **Cross-Check Discrepancies vs. AlphaXiv Pass 2:**
  1. Knowledge Base §3.2 #9 rounded `Qwen 2.5 7B` Logical Deduction probe AUC to `0.78`; exact Table 3 value is **`0.778`** (p. 4). `[Verified]`
  2. Knowledge Base §3.2 #9 compressed `"50 initially correct items/cell"` across §2.2–§2.4; in the PDF, **`50` initially correct items** is the §2.2 CoT-intervention sample (p. 2), whereas §2.4 probe steering runs on the **full** $S_{\text{yes}}$ / $S_{\text{no}}$ correct test subsets (min $n \ge 20$ parsed) and **`50` random test examples (not limited to initially correct)** for the orthogonal baseline (pp. 3, 5). `[Verified]`
  3. Knowledge Base omitted the `GPT-OSS 20B` reasoning-model replication in Appendix F (p. 21), where pre-CoT probe AUC drops on Logic/Social/Sports (remaining $>0.9$ on Anachronisms) and steering flip rates become negligible against the orthogonal baseline. `[Verified]`
- **Verbatim Quotes for Chapter 2 / Chapter 3:**
  - *Pre-CoT probe drop when CoT performs computation (p. 4):* `"In Table 2, we saw that on Logical Deduction, models performed the worst without CoT and benefited the most from the inclusion of CoT, compared to the other datasets. These results suggest that, for this dataset, the answer computation process occurs during CoT. Accordingly, the pre-CoT probes are not very informative. In general, the average probe score for a given task in Table 3 is anticorrelated with the usefulness of CoT for that task in Table 2."` `[Verified, p. 4]`
  - *Steering scope caveat at answer tokens (p. 6):* `"Our intervention applies the activation addition at every decoding position after the prompt, including the tokens where the final answer is produced. Part of the steering effect may therefore reflect direct biasing of final-answer token selection, rather than an edit to a pre-CoT belief that propagates through generation."` `[Verified, p. 6]`

---

### 1.2 `2510.27484` — *Thought Branches: Interpreting LLM Reasoning Requires Resampling*

- **Citation & Venue:** Uzay Macar, Paul C. Bogdan, Senthooran Rajamanoharan, Neel Nanda (2026), *Thought Branches: Interpreting LLM Reasoning Requires Resampling*, published as a conference paper at **ICLR 2026**, `arXiv:2510.27484v2` (13 Apr 2026, 35 pages). `[Verified, p. 1]`
- **Design & Parameters Cross-Checked:**
  - **Models by Experiment:** §2–§3 Blackmail & Whistleblowing use 4 reasoning models — `qwen-32b`, `qwen3-235b-a22b`, `llama-3.1-nemotron-ultra-235b-v1`, `deepseek-r1-0528` (p. 2); §4.1 Hinted MMLU uses `DeepSeek-R1-Qwen-14B` across `40` effective-hint problems (`100` resamples/position, p. 6); §4.2 Resume bias uses `Qwen3-8B` across `8` variable resumes (`500` base CoTs × `1` resample/sentence clustered into `32` embedding clusters, p. 7).
  - **Sampling & Metrics:** `temperature = 0.7`, `top-p = 0.95`; `20` base traces leading to blackmail, `100` rollouts per sentence; sentence embeddings via `bert-large-nli-stsb-mean-tokens`; `importance(S_i) = D_KL[p(A'_{S_i} | T_i \not\approx S_i) || p(A_{S_i})]` (Eq. 1) and `importance++(S_i) = D_KL[p(A'_{S_i} | \forall j \ge i: T_j \not\approx S_i) || p(A_{S_i})]` (Eq. 2). `[Verified, pp. 2–3]`
  - **Table 1 (p. 5) & Table 5 (App. D.1, p. 29):** On Blackmail & Whistleblow (Table 1), Resampled achieves **`67.4%`** (Blackmail) and **`87.4%`** (Whistleblow) plan shift vs. Handwritten `64.7%` / `78.5%`, Cross-model `64.2%` / `70.5%`, Same-model `62.0%` / `77.8%`, and dramatically lower `No effect` (`11.4%` / `7.1%` vs. `24.5%` / `14.0%` handwritten). In MATH (App. D.1 Table 5, p. 29), local plan-shift % is **`64.7%`** Handwritten vs. **`55.1%`** Resampled, while Resampled has the highest continuous **`Average effect (0–5) ± SE`** (**`3.84 ± 0.06`** vs. `3.49 ± 0.02` handwritten) and higher `No effect` (`32.3%` vs. `9.2%`). `[Verified, pp. 5, 29]`

![Local effect of sentence insertions in Blackmail and Whistleblow scenarios in Macar et al. (ICLR 2026)](figures/2510-27484-table1.png "Table 1 from Macar et al. (ICLR 2026) comparing off-policy vs. resampled sentence insertions on Blackmail and Whistleblow scenarios [p. 5](https://arxiv.org/pdf/2510.27484)")

![MATH appendix local effect of sentence insertions in Macar et al. (ICLR 2026)](figures/2510-27484-table5.png "Table 5 (Appendix D.1) from Macar et al. (ICLR 2026) reporting local plan shifts and 0-5 average effects on MATH [p. 29](https://arxiv.org/pdf/2510.27484)")

- **Cross-Check Discrepancies vs. AlphaXiv Pass 2:**
  - Knowledge Base §2 and §3.2 #10 omitted the specific model list across sections (`qwen-32b`, `qwen3-235b-a22b`, `llama-3.1-nemotron-ultra-235b-v1`, `deepseek-r1-0528` in §2–§3; `DeepSeek-R1-Qwen-14B` in §4.1; `Qwen3-8B` in §4.2) and omitted the important Table 5 nuance that on MATH, Handwritten edits yield more frequent local plan shifts (`64.7%` vs `55.1%`) even though Resampled insertions achieve the highest continuous effect (`3.84 ± 0.06`). Notice `64.7%` happens to match Blackmail Handwritten plan shift (`64.7%` in Table 1) AND MATH Handwritten plan shift (`64.7%` in Table 5)—both numbers are real in their respective tables! `[Verified, pp. 5, 29]`
- **Verbatim Quotes for Chapter 2 / Chapter 3:**
  - *Off-policy distribution shift & error correction (p. 5):* `"Qualitative examples in Table 3 illustrate that on-policy replacements integrate more naturally into the ongoing thought process, while off-policy edits often read as incongruent and are ignored or quickly overwritten."` `[Verified, p. 5]`
  - *Resilience & regeneration (p. 3):* `"Reasoning models often regenerate key ideas post-edit: a sentence removed at position i may resurface at position j ≥ i. We measure resilience with the number of interventions needed before the content stays absent (details in Appendix B.1)."` `[Verified, p. 3]`
  - *MATH receptivity to external edits (App. D.1, p. 29):* `"Interestingly, handwritten interventions show stronger local effects in math problems compared to blackmail scenarios, potentially because mathematical corrections are less context-dependent than strategic reasoning modifications."` `[Verified, p. 29]`

---

### 1.3 `2307.13702` — *Measuring Faithfulness in Chain-of-Thought Reasoning*

- **Citation & Venue:** Tamera Lanham, Anna Chen, Ansh Radhakrishnan, et al. (Jared Kaplan, Jan Brauner, Samuel R. Bowman, Ethan Perez) (2023), *Measuring Faithfulness in Chain-of-Thought Reasoning*, `arXiv:2307.13702v1` (17 Jul 2023, 14 pages). `[Verified, p. 1]`
- **Design & Parameters Cross-Checked:**
  - **Models (§2.1, §3.1):** 175B RLHF decoder-only assistant for §2 (p. 2); scaling sweep across model sizes (from `<13B`, peaking around `13B` for faithfulness on `6/8` tasks, declining monotonically to `175B`, §3.1 Fig. 7, p. 7) plus synthetic addition tasks (`2, 4, 8, 16` operands of `2–3` digits, `810M`/`1.6B` excluded due to XML parse failure, §3.2 Fig. 8, p. 8).
  - **Sampling & Tasks (§2.1):** 8 MCQA benchmarks (ARC Challenge, ARC Easy, AQuA, HellaSwag, LogiQA, MMLU, OpenBookQA, TruthfulQA), `100` reasoning samples/problem, nucleus sampling `p = 0.95`, `temperature = 0.8`. Mean CoT length `4` sentences (`89%` in `3–6` steps, §2.2 p. 3). `[Verified, p. 3]`
  - **Table 2 (p. 5) & Paraphrasing (§2.6–§2.6.1, pp. 6–7):** Early Answering AOC `0.44` (AQuA) vs. `0.02` (ARC Easy); Adding Mistakes AOC `0.52` (AQuA) vs. `0.07` (ARC Easy). Paraphrase accuracy closely matches original CoT (Fig. 6, p. 7), **descriptively with no TOST, no equivalence margin, and no paraphrase-churn gate**. Notice Footnote 3 (p. 7) explicitly warns against paraphrasing an entire CoT up to its conclusion because late answer leakage trivializes the outcome. `[Verified, pp. 5–7]`

![AOC faithfulness and accuracy metrics across 8 MCQA tasks in Lanham et al. (2023)](figures/2307-13702-table2.png "Table 2 from Lanham et al. (2023) reporting Early Answering and Adding Mistakes AOC alongside accuracy with/without CoT across 8 tasks [p. 5](https://arxiv.org/pdf/2307.13702)")

- **Cross-Check Discrepancies vs. AlphaXiv Pass 2:**
  - All core Table 2 numbers, sampling params, and sections match Pass 2 cleanly. Addition of §3.1 Fig. 7 (`13B -> 175B` inverse scaling, p. 7), §3.2 synthetic addition Fig. 8 (p. 8), and Footnote 3 (p. 7, why prefix-only paraphrasing avoids answer-copying triviality) sharpens our Chapter 2 & Chapter 3 citations. `[Verified]`
- **Verbatim Quotes for Chapter 2 / Chapter 3:**
  - *Post-hoc reasoning & task dependence (p. 3):* `"Overall though, if reasoning is not post-hoc, there are fewer ways for it to be unfaithful than there are for reasoning which is post-hoc..."` and *inverse scaling (p. 7):* `"For 7/8 tasks, the 13B parameter model changes its answer after CoT more often than the 175B model does. In fact, for most tasks, faithfulness gets monotonically worse from 13B to 175B parameter models, indicating inverse scaling in model size for reasoning faithfulness on these tasks."` `[Verified, pp. 3, 7]`
  - *Prefix paraphrasing vs. full-CoT answer leakage (Footnote 3, p. 7):* `"We chose this approach over paraphrasing the entire chain of thought; the model almost always states the final answer it has arrived at in the final steps of the CoT, so paraphrasing the entire CoT would trivially lead the model to produce the same answer."` `[Verified, p. 7]`

---

### 1.4 `2609.25366` — *From Decorative to Load-Bearing: Task Difficulty Shapes the Causal Role of Chain-of-Thought*

- **Citation & Venue:** Renee Jia, Di Mu (2026), *From Decorative to Load-Bearing: Task Difficulty Shapes the Causal Role of Chain-of-Thought*, **Published in Transactions on Machine Learning Research (08/2026)**, OpenReview `TiZQnKDIHq`, `arXiv:2609.25366v1` (21 Sep 2026, 27 pages). `[Verified, p. 1]`
- **Design & Parameters Cross-Checked:**
  - **Models & Data:** `Gemma-2-9B-IT` (`7,691` correct multi-step baselines from `11,390` questions -> `21,238` labeled continuations + `7,346` matched-cell = **`28,584`** combined continuations; App. L p. 22 & Table 5 p. 23), `Llama-3.1-8B-Instruct` (`7,791` continuations, §5.6 p. 10), `DeepSeek-R1-Distill-Qwen-7B` (`1,603` post-`</think>` continuations filtered to $\ge 4$ steps, §5.6 p. 11 & App. O p. 24), plus Base vs IT viability gate (`Gemma-2-9B` base vs IT, App. Q p. 25).
  - **Interventions & Classification (§3.1–§3.3):** 7 perturbation strategies (2 numerical on GSM8K; 5 conceptual on MMLU/BBH and matched GSM8K) at early (`25%`), middle (`50%`), late (`75%`) chain positions; forced continuation from corrupted prefix; 3 behavioral modes: Type A (silent bypass), Type B (self-correction), Type C (error propagation); `Claude Haiku` judge resolved ambiguous cases (`99.9%` of `3,952`), anchored on judge-invariant `C-vs-non-C` verified by a stratified `n = 500` two-annotator blind study (inter-annotator `κ = 0.927` 4-way, `κ = 1.000` on `C-vs-non-C`; consensus matches production label `96.2%` on `C-vs-non-C`, `76.0%` 3-way, App. S p. 26). `[Verified, pp. 5, 26]`
  - **Key Results:** Table 1 (p. 6) Gemma-2-9B-IT: GSM8K `86.5%` base acc, Bypass `94.5%`, Self-Correct `1.6%`, Error Prop `3.9%`; MMLU `74.8%` / `41.5%` / `36.3%` / `22.3%`; BBH `57.9%` / `37.4%` / `21.7%` / `40.9%`. Table 2 & App. M (pp. 8, 23): matched `2×2` (`64.5%` on BBH `multistep_arith` numerical vs. `3.9%` GSM8K numerical) and logistic GLM deviance partition (`n = 28,584`): **`98.8%`** task difficulty ($\Delta=3,567.0$), **`0.8%`** perturbation type ($\Delta=29.4$), **`0.4%`** interaction ($\Delta=13.8$). Hidden-state probes detect behavioral mode (86.2% C-vs-non-C MLP, p. 8), but single-direction steering fails across `11,556` generations and 8-vector basis steering moves only `~25%` (`24.6%`, 14/57) of Type C (§5.5, p. 9). `[Verified, pp. 6–9, 23]`

![Three-mode behavioral taxonomy across GSM8K, MMLU, and BBH in Jia & Mu (TMLR 2026)](figures/2609-25366-table1.png "Table 1 from Jia & Mu (TMLR 2026) reporting Base Acc., Bypass (A), Self-Correct (B), and Error Prop (C) on Gemma-2-9B-IT [p. 6](https://arxiv.org/pdf/2609.25366)")

![Matched 2x2 of perturbation type and task difficulty in Jia & Mu (TMLR 2026)](figures/2609-25366-table2.png "Table 2 from Jia & Mu (TMLR 2026) isolating task difficulty vs. perturbation type on Gemma-2-9B-IT [p. 8](https://arxiv.org/pdf/2609.25366)")

- **Cross-Check Discrepancies vs. AlphaXiv Pass 2:**
  - Knowledge Base §3.2 #18 noted `"greedy in DeepSeek App. P, p. 25"`; Appendix P explicitly states `"our greedy protocol matches the rest of the paper"` (`temperature = 0` greedy decoding was used **across all models and experiments** in the paper, not only DeepSeek). `[Verified, p. 25]`
  - Knowledge Base omitted the `n = 500` human validation metrics (`κ = 1.000` on C-vs-non-C, `κ = 0.927` overall, App. S p. 26) and the probe/additive-steering null (§5.4–§5.5, pp. 8–9). `[Verified]`
- **Verbatim Quotes for Chapter 2 / Chapter 3:**
  - *Why forced continuation beats separate-turn re-prompting (p. 4):* `"Forced continuation avoids the re-derivation confound of the simpler alternative—presenting the full perturbed CoT and asking for the final answer in a separate turn—under which the new turn permits the model to re-derive from the question."` `[Verified, p. 4]`
  - *Greedy decoding precedent (App. P, p. 25):* `"All three formats yielded 38–44% accuracy at temperature 0 (greedy decoding). The accuracy gap to public benchmarks is therefore not prompt-format-driven; the public benchmarks use temperature 0.6 sampled outputs (which R1’s RL training optimizes for), and our greedy protocol matches the rest of the paper."` `[Verified, p. 25]`

---

### 1.5 `2026.magmar-main.3` — *CMC-Bench: When Image and Text Disagree in Multimodal RAG*

- **Citation & Venue:** Jasper Kyle Catapang (2026), *When Image and Text Disagree: Cross-Modal Evidence Conflict in Multimodal Retrieval-Augmented Generation*, **Proceedings of the 2nd Workshop on Multimodal Augmented Generation via Multimodal Retrieval (MAGMaR 2026)**, July 4, 2026, pp. 1–10 (`https://aclanthology.org/2026.magmar-main.3.pdf`). `[Verified, p. 1]`
- **Design & Parameters Cross-Checked:**
  - **Dataset (Table 1, p. 4):** `942` base examples × `4` conditions (`Aligned`, `Image-correct`, `Text-correct`, `Both-wrong`) = **`3,768` instances**: `500` from ChartQA validation/test (`250` Factual / `1,000` inst; `250` Temporal / `1,000` inst) and `442` from MMMU validation/test across 6 subjects (`250` Entity / `1,000` inst; `192` Granularity / `768` inst). Text passages use fixed templates (`10.7 ± 5.6` words). `[Verified, pp. 3–4]`
  - **Models & Quantization (Table 2, p. 4):** 4 open VLMs run in **4-bit quantization via `mlx-vlm`** on Apple Silicon (M3 Pro 36 GB): `Qwen3-VL-4B-Instruct` (4B), `LFM2.5-VL-1.6B` (1.6B), `Gemma-3n-E2B-it` (2B), `DeepSeek-VL2-small` (3B active). Note: **none** of our Qwen2.5-VL models are tested. `[Verified, p. 4]`
  - **Protocol & Judge (§4.2–§4.3, p. 4):** Free-form generation (`"Query: {question}. Retrieved image evidence: [IMAGE]. Retrieved text evidence: {text_passage}. Answer the query using the provided evidence."`, **no CoT forcing, no prefix forcing, no verdict extraction, no order counterbalancing**). Auxiliary LLM judge (`OpenAI gpt-5-mini`, API version `2024-02-15-preview`, blind to gold answer) labels each response in `{IMAGE, TEXT, BOTH, NEITHER, ABSTAIN}`. Metrics (Eqs. 1–7, pp. 4–5): condition Acc, `MFR` (`0.430–0.486`), `MPB_img` / `MPB_txt`, `HR = ConfabR + CDR`, `ΔAcc` (`0.169–0.464`). Limitation acknowledged on p. 8: LLM judge reliability was not formally validated against humans, and conflict conditions occasionally receive `BOTH` labels (`23` for LFM2.5, `13` for Qwen3 in `image-correct`, p. 7). `[Verified, pp. 4–8]`

![Main judge-based results across four quantized VLMs on CMC-Bench in Catapang (MAGMaR 2026)](figures/cmc-bench-table3.png "Table 3 from Catapang (MAGMaR 2026) reporting condition accuracies, MPB, MFR, ConfabR, CDR, HR, and Delta-Acc on CMC-Bench (n=942 per condition) [p. 5](https://aclanthology.org/2026.magmar-main.3.pdf)")

- **Cross-Check Discrepancies vs. AlphaXiv Pass 2:**
  - All core dataset counts (`942` examples / `3,768` instances), conditions, judge classes, and Table 3 headline rates (`Qwen3-VL-4B` `CDR=.317`, `ConfabR=.189`, `HR=.507`; `Gemma-3n-E2B` `ConfabR=.519`, `CDR=.187`, `HR=.706`) match Pass 2 accurately. Important details verified in the full PDF: (i) all 4 models run in **4-bit `mlx-vlm`**, (ii) **`gpt-5-mini`** (`2024-02-15-preview`) has **no human agreement validation** (flagged as limitation, p. 8), and (iii) **no CoT prompt, prefix-forcing, verdict elicitation, or modality-order counterbalancing** exists anywhere in CMC-Bench. `[Verified, pp. 4–8]`
- **Verbatim Quote for Chapter 2 / Chapter 3:**
  - *Core gap vs. CMC-Bench (p. 6 & p. 8):* `"The convergence of MFR values across four architecturally diverse models (range 0.430–0.486, a spread of only 5.6 points) is unlikely to be coincidental... The near-identical MFR values suggest that none of the four models has learned to track which modality is evidentially correct on a per-instance basis; each instead expresses a static prior whose ceiling is structurally similar across architectures."` and *Unvalidated judge caveat (p. 8):* `"The LLM-as-judge protocol is central to every reported metric; its reliability has not been formally validated in this work."` `[Verified, pp. 6, 8]`

---

## 2. Full Autopsies of the 2 Chapter 2 Related-Work Leads

### 2.1 Lead 1: `2606.22862` — *Chains That See, Answers That Don’t: A Multi-Aspect Evaluation Recipe for Forced Chain-of-Thought on Video-MME*

- **Citation & Venue:** Zhichao Fan, Yanhang Li, Zexin Zhuang (2026). *Chains That See, Answers That Don’t: A Multi-Aspect Evaluation Recipe for Forced Chain-of-Thought on Video-MME*, Proceedings of the **2nd Workshop on Evaluation for Multimodal Generation @ SIGIR 2026 (EvalMG ’26)**, July 24, 2026, Melbourne, Australia (10 pages, `arXiv:2606.22862v1`). `[Verified, pp. 1–2]`
- **Paradigm, Models & Decoding:** Evaluates 4-way video MCQ (`Video-MME`) on **`Qwen2.5-VL-7B-Instruct`** (`bf16/fp16`; `n = 396` primary, `180` swap, `144` ladder) and **`Qwen2.5-VL-32B-Instruct`** (`NF4 4-bit` bitsandbytes with visual encoder in full precision; `n = 300` primary, `120` swap, `96` ladder, `n = 61` subtitle ablation). Inference uses HuggingFace Transformers SDPA, **greedy decoding (`do_sample=False`)**, `16` uniformly sampled frames, `max_side=448`. `[Verified, pp. 2–3]`
- **Probes & Scoring Design:**
  1. **Probe 1 (Primary conditions, App. F):** `direct` (`"Answer with only the letter..."`), `CoT` (`"Reason step by step in at least 5 numbered steps, citing a frame for each step. Conclude with 'Answer: X' on its own line."`), `answer-first` (`"First write 'Answer: X'... Then justify..."`), `no-video` (`0` frames, same as `direct`). `[Verified, pp. 3, 9]`
  2. **Probe 2 (Counterfactual video swap):** Replaces real video with same-task different video (seed `0`); scores content-word `token-Jaccard`, paired-parsed letter flip rate, and original-label retention under swap. `[Verified, pp. 3, 5]`
  3. **Probe 3 (Visual-corruption ladder):** Four ordered degradation rungs (`real -> shuffle -> single x16 -> black`) with exact-permutation Spearman $\rho_4$, plus two off-axis contamination checks (`swap_task`, `swap_domain`). `[Verified, pp. 3, 5–6]`
  4. **Dual Regex Scorer (`strict` `(a)–(c)` vs. `permissive` `(a)–(d)`):** Permissive rule `(d)` falls back to the last word-bounded `A/B/C/D` anywhere, which **coerces explicit refusals** (e.g., `"the video does not match any option... Answer: None of the above options apply"`) into MCQ letters! Unparsed outputs count wrong in `raw` and drop out of `all4`-parsed. `[Verified, pp. 3–6, Table 5 p. 9]`
- **Statistics & Key Quantitative Findings:**
  - Exact two-sided McNemar, 50,000-resample paired bootstrap `90% CI`, Holm step-down correction over a manuscript-declared (non-preregistered) 4-test primary family (2× `raw` strict McNemar + 2× `ladder` Spearman $\rho_4$). `[Verified, p. 4]`
  - **Table 1 (p. 4):** On `32B`, `raw (strict; n=300)` `CoT - direct = -5.33 pp` (`61.67% -> 56.33%`, `90% CI [-9.33, -1.33]`, McNemar `p=0.048`, Holm `0.125`), `raw (perm.) = -2.33 pp` (Holm `0.43`), yet `all4 (strict; n=262)` flips sign to **`+3.05 pp`** (`90% CI [-0.76, +6.87]`, `p=0.23`) due to CoT strict parse rate dropping to **`87.33%`** (App. B, p. 8)! On `7B` (`n=396`), `raw (strict)` `CoT - direct = -7.32 pp` (`59.09% -> 51.77%`, `90% CI [-11.11, -3.28]`, McNemar `p=0.003`, **Holm `0.012`** — the only Holm-surviving primary test, while `raw (perm.) = -5.81 pp`, Holm `0.077`). `[Verified, pp. 4, 8]`
  - **Table 2 & Table 5 (pp. 5–6, 9):** Under counterfactual video swap, chain Jaccard collapses to **`0.140` (32B)** / **`0.119` (7B)** and paired-parsed letters flip **`67.2%` / `59.9%` permissive** (`63.3% / 59.4% strict`), proving CoT chains are genuinely video-conditioned — yet `strict` reveals **`63/120` unparseable explicit refusals on 32B** that permissive rule `(d)` coerced to letters (`swap-prs` `117/120 -> 57/120`, Table 5). Over the 4-rung degradation ladder, $\rho_4 = -1.0$ (`p = 1/24 \approx 0.042`, Holm `0.125`). `[Verified, pp. 5–6, 9]`

![Paired direct-vs-CoT accuracy under permissive and strict regex scorers on Video-MME in Fan, Li & Zhuang (2026)](figures/2606-22862-table1.png "Table 1 from Fan, Li & Zhuang (2026) showing Qwen2.5-VL-32B and 7B direct vs. CoT accuracy and scorer-dependent sign flip [p. 4](https://arxiv.org/pdf/2606.22862)")

![Counterfactual video-swap probe under permissive vs. strict scoring in Fan, Li & Zhuang (2026)](figures/2606-22862-table5.png "Table 5 from Fan, Li & Zhuang (2026) showing explicit refusal coercion under permissive rule (d) on 32B (117/120 vs. 57/120 strict) [p. 9](https://arxiv.org/pdf/2606.22862)")

- **Verbatim Quotes (TOST / Definition of Forced CoT):**
  - *Prompted vs. prefix-forced CoT (p. 1):* `"Forced chain-of-thought (CoT) prompting—instructing the model to produce several reasoning steps before committing to an answer—has become a default setting when adapting vision–language models (VLMs) to multiple-choice benchmarks."` `[Verified, p. 1]`
  - *Why TOST was NOT claimed (p. 4):* `"Equivalence testing [10, 24] and parse-rate-controlled scoring are standard in clinical and psycholinguistic measurement but remain rare in VLM evaluation, where 'CoT − direct < 0 but p > 0.05' is routinely reported as 'no effect' rather than as an underpowered null."` (p. 2); `"For the 32B null we report a ±5 pp post-hoc sensitivity margin and the 90% CI; we do not call this a TOST equivalence test because the margin was not pre-specified."` (p. 4) `[Verified, pp. 2, 4]`

---

### 2.2 Lead 2: *Same Reasoning, Different Words: Testing Linguistic Invariance in Chain-of-Thought Monitoring*

- **Citation & Venue:** Joe Smith (California Institute of Technology, 2026). *Same Reasoning, Different Words: Testing Linguistic Invariance in Chain-of-Thought Monitoring*, NeurIPS 2026 Workshop *Can We Trust AI Evaluation? Robustness, Causality, and Risk in Modern AI Assessment* (`TAE @ NeurIPS 2026`, Sydney, AUS), OpenReview ID `uul4iRQSJ2`, [NeurIPS 2026 workshop page](https://neurips.cc/virtual/2026/loc/sydney/178182), [author CV](https://joefsmith.github.io/cv.pdf). **Full PDF status:** `[PDF Not Available]` (OpenReview returns HTTP 403 Forbidden to non-browser clients; no open mirror located). `[Verified via open NeurIPS page & author CV]`
- **Verified Protocol & Quantitative Abstract Findings:**
  - **Paradigm (verbatim abstract):** *"Textual chain-of-thought (CoT) monitors observe language, not cognition directly. We ask whether a temporal monitorability result changes when the same reasoning is expressed differently. A policy first produces one complete trace and answer. We then rewrite each reasoning step as either a light-paraphrase control or a proposition-aligned syntactic and register intervention, without resuming the policy. The forced-answer trajectory is therefore fixed across conditions, while an independently validated soft monitor reads matched prefixes."*
  - **API / Measurement Audit (verbatim abstract):** *"Two of three tested API routes expose class log-probabilities that are structurally valid but empirically degenerate. This finding motivates a six-test responsiveness gate and a hard-policy, soft-observer protocol."*
  - **Quantitative Results (verbatim abstract):** *"Of 100 MMLU-Redux traces, 97 rewrite pairs pass the preservation gates and 95 yield complete monitor trajectories. We estimate ∆D=−0.007 (95% CI [−0.017, 0.003]), which is equivalent within a prespecified ±0.05 margin. The mean action–observer divergence also changes little (∆J=−0.005), although 20 of 95 item-level disclosure shifts exceed the equivalence margin in either direction. Aggregate disclosure is therefore invariant for this monitor, transformation family, and retrieval-heavy regime, but individual judge readings remain sensitive to realization."* `[Verified via NeurIPS 2026 official abstract]`

---

### 2.3 Direct Answers to the 3 Post-v5 Design & Novelty Questions

1. **Question 1 (`2606.22862`): Prefix-forcing, image–text conflict, TOST skip, and `PREREGISTRATION_VERDICT_TRANSPLANT.md` §1.1 novelty boundary:**
   - *Prefix-forced CoT or image–text conflict?* **Neither.** Fan, Li & Zhuang (2026) use **"forced CoT"** to mean **prompt-instructed multi-step reasoning before an MCQ answer** (`"Reason step by step in at least 5 numbered steps..."`, App. F p. 9), not assistant-turn prefix injection/transplantation of an edited verdict or reasoning step, and test single-video Video-MME MCQs (video swaps & frame degradation, plus an $n=61$ descriptive aligned subtitle prefix in App. A), **not** cross-modal image–text evidence conflicts. `[Verified]`
   - *Why did it discuss/skip TOST?* It explicitly cites Schuirmann (1987) and Lakens (2017), evaluates `Qwen2.5-VL-32B` against a `±5 pp` post-hoc margin with a `90% CI`, and **refuses to call it a TOST equivalence test** because (a) the study was not pre-registered and the margin was not pre-specified (`p. 4`), and (b) both `raw strict 90% CI [-9.33, -1.33]` (harm side) and `all4 strict 90% CI [-0.76, +6.87]` (`+6.87 > +5 pp`) fail equivalence anyway. `[Verified, p. 4]`
   - *Does it narrow §1.1 novelty?* **No** on our empirical claim (assistant-turn prefix-forcing of a model's own minimally edited source-reliability verdict under counterbalanced image–text conflict + binding interaction). We should however cite `2606.22862` in §1.1 and Chapter 2 to explicitly disambiguate *"prompt-forced CoT before answering"* from our *assistant-turn verdict prefix-forcing*. `[Verified/Inferred]`

2. **Question 2 (*Same Reasoning, Different Words*): Published precedent for our `ε = 5.0 pp` TOST or `5.0%` paraphrase-churn gate?**
   - **No — both remain `[Design decision]`**, though `PREREGISTRATION_VERDICT_TRANSPLANT.md` should qualify its prior blanket statement (`"no paper read uses an equivalence test"`).
   - *Why it is NOT a direct precedent for `ε = 5.0 pp` or `5.0%` churn:* (a) Smith (2026) tests **external CoT monitor disclosure** ($\Delta D$, action–observer divergence $\Delta J$) over **unresumed, fixed-answer** `MMLU-Redux` traces (`n = 95`), not generative **VLM source choice (`para − own`)** on resumed CoT completions under image–text conflict; (b) its prespecified `±0.05` equivalence margin applies to monitor disclosure $\Delta D$ (`-0.007`, `95% CI [-0.017, 0.003]`, note 95% CI rather than 90% TOST CI; internal statistical details uncheckable with PDF 403-gated), not generative choice pp shifts; and (c) **most critically, Smith reports `20 / 95` (`21.1%`) item-level disclosure shifts exceeding `±0.05`**, confirming there is **no `≤ 5.0%` item-level paraphrase-churn precedent** (indeed, Smith's `~21%` item-level realization sensitivity aligns closely with our dev Math `any-change` churn of `15.2–23.1%`!). `[Verified from abstract / Inferred for thesis mapping]`
   - Meanwhile, `2606.22862` shows that `±5 pp` + `90% CI` is a recognized heuristic sensitivity band in VLM CoT evaluation (`p. 4`), validating our decision to **pre-specify `ε = 5.0 pp` before `--phase confirm`**, while keeping both `ε = 5.0 pp` and `5.0%` churn explicitly tagged `[Design decision]`. `[Verified]`

3. **Question 3 (Both leads): Any blind spots exposed in v5 (`binding` vs. `non-binding`, `k=1` behavioural template, `para_flip − para`, or ChartQA exploratory)?**
   - Neither paper breaks or invalidates binding vs. non-binding, `k=1` behavioural rollout, `para_flip − para`, or exploratory ChartQA, **but both reinforce specific methodological safeguards already helpful in v5**:
     1. **Terminology disambiguation (`2606.22862`):** Never use bare `"forced CoT"` without specifying *assistant-turn prefix-forcing*, so readers do not conflate our manipulation with prompt-elicited step-by-step CoT. `[Inferred]`
     2. **Parser sensitivity & refusal/unparseable decomposition (`2606.22862` Tables 1 & 5):** Shows permissive regex fallbacks can coerce refusals/unmatched answers and even flip effect signs (`-2.01` vs `+3.05 pp` on Qwen2.5-VL-32B). Our v5 separation of `image`, `text`, `neither`, plus strict vs. lenient parser checks, directly prevents that pitfall. `[Verified/Inferred]`
     3. **Pre-specified vs. post-hoc margin discipline (`2606.22862` p. 4):** Refusing to run confirmatory TOST without pre-registration directly justifies locking `PREREGISTRATION_VERDICT_TRANSPLANT.md` before `--phase confirm`. `[Verified]`
     4. **Aggregate equivalence masking item-level realization noise (*Same Reasoning, Different Words*):** `ΔD = -0.007` passing `±0.05` while `20/95` items exceed `±0.05` shows why v5's dual reporting of TOST mean shift AND item-level D5 churn (`image↔text` + `neither` + `any-change`) is essential rather than relying on signed means alone. Also reinforces verifying local HF log-probs / score responsiveness directly on dev renders (`verdict_nll` / `--print_example`) rather than assuming API logprobs are well-behaved. `[Verified/Inferred]`

---

## 3. Repository Synchronization Actions Executed

1. **[THESIS_LITERATURE_KNOWLEDGE_BASE.md](../THESIS_LITERATURE_KNOWLEDGE_BASE.md):** Moved #15–#19 into locally present PDFs (`20` total PDFs in `Docs/Paper/`, `14 -> 19` core + `2606.22862.pdf`), added `Same Reasoning, Different Words` as Lead #2 (`[PDF Not Available]`), applied PDF-verified page/metric refinements in §1, §2, §3.2, and updated §4 rule #5 on TOST/equivalence precedents.
2. **[PREREGISTRATION_VERDICT_TRANSPLANT.md](../../PREREGISTRATION_VERDICT_TRANSPLANT.md):** Updated ONLY `§Sources`, `§1.1` (resolving the two 2026 leads and disambiguating prompt-forced CoT vs. assistant-turn verdict prefix-forcing), qualified the `"no paper read uses an equivalence test"` notes in §7.3 / §10 while preserving all `[Design decision]` tags, thresholds, and §4 templates intact (`test_v5.py` clean), and logged the update in §11.
3. **Documentation indices synced:** Updated [Docs/Paper/README.md](../README.md), [Docs/README.md](../../README.md), [AGENTS.md](../../../AGENTS.md), [CLAUDE.md](../../../CLAUDE.md), [README.md](../../../README.md), [Experiment/README.md](../../../Experiment/README.md), and [Thesis/README.md](../../../Thesis/README.md) to reflect `20` local PDFs (`0` missing core PDFs) and `Docs/Paper/post-v5-pdf-audit/`.
