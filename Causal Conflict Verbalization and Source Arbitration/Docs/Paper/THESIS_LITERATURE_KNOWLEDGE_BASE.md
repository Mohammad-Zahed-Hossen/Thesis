# Complete Thesis Literature Report & Knowledge Base (18 Papers + CMC-Bench)

**Last updated:** 2026-11-14 (pre-freeze status in §5–§6 synced 2026-11-20)
**Purpose:** Complete, evidence-grounded literature dossier for all future thesis design, statistical, and dissertation-writing decisions. Every AI agent working on this thesis should consult this file alongside [PREREGISTRATION_VERDICT_TRANSPLANT.md](../PREREGISTRATION_VERDICT_TRANSPLANT.md) and [Experiment/README.md](../../Experiment/README.md).
**Sources merged:**
1. Local primary-PDF audits: [lit-dossier-verdict-transplant.md](lit-dossier-verdict-transplant/lit-dossier-verdict-transplant.md) & [prereg-freeze-audit.md](prereg-freeze-audit/prereg-freeze-audit.md) (2026-11-10)
2. Post-v5 plan audit: [claude_v4_vs_v5_plan_audit.md](<../../Thesis/docs/Archive/dev v5/claude_v4_vs_v5_plan_audit.md>) (2026-11-14)
3. AlphaXiv OpenResearch Pass 1 (8 anchor papers) & Pass 2 (10 remaining papers + CMC-Bench) (2026-11-14)
4. Post-v5 direct PDF audit (#15–#19 + 2 Ch. 2 leads): [post-v5-pdf-audit.md](post-v5-pdf-audit/post-v5-pdf-audit.md) (2026-11-14)

> **Epistemic & Trust Policy:** `[Verified]` = directly checked in a local PDF, open official proceedings page/abstract, or repo code/data. `[Inferred]` = methodological interpretation for this thesis. For verbatim thesis quotes, always double-check the exact wording against the PDF in `Docs/Paper/`.

---

## 0. Local PDF Inventory (`Docs/Paper/`)

> **2026-11-15 audit (+ 2026-11-17 addendum):** a pre-freeze literature audit screened `1,452` unique records (`1,260` on 2026-11-15 + `192` on 2026-11-17) and added `6` A-graded and `41` B-graded papers (`33` on 2026-11-15 + `8` new/upgraded on 2026-11-17; `0` new A papers, `0` new novelty threats). Those papers are **not** core sources and are not merged into the matrix below. See §6 and [lit-audit-2026-11-15.md](lit-audit-2026-11-15/lit-audit-2026-11-15.md). `Docs/Paper/` holds `29` active PDFs: the `20` listed here plus the `6` A papers and `3` cited B papers (`2603.20172.pdf`, `2610.23700.pdf`, `2610.00054.pdf`).

### A. 20 PDFs Currently Present in `Docs/Paper/` (19 Core + 1 Ch. 2 Lead; 0 Core Missing)
| # | Local File | arXiv / Anthology ID | Short Name | Audit Coverage |
|---|---|---|---|---|
| 1 | [2503.02199.pdf](2503.02199.pdf) | `2503.02199` | *Words or Vision* (Deng et al., 2025) | Dossier (targeted) + AlphaXiv Pass 2 (full) |
| 2 | [2504.08974.pdf](2504.08974.pdf) | `2504.08974` | *Mixed Signals* (Pezeshkpour et al., 2025) | Dossier (targeted) + AlphaXiv Pass 2 (full) |
| 3 | [2505.23945.pdf](2505.23945.pdf) | `2505.23945` | *Bias & CoT Faithfulness* (Balasubramanian et al., 2025) | Dossier (targeted) + AlphaXiv Pass 2 (full) |
| 4 | [2511.02243.pdf](2511.02243.pdf) | `2511.02243` | *When Modalities Conflict* (Zhang et al., 2025) | Dossier (pp. 1–8 full) + AlphaXiv Pass 1 |
| 5 | [2602.14518.pdf](2602.14518.pdf) | `2602.14518` | *Diagnosing Knowledge Conflict* (Tang et al., 2026) | Dossier (targeted) + AlphaXiv Pass 2 (full) |
| 6 | [2604.14888.pdf](2604.14888.pdf) | `2604.14888` | *Answer Inertia / Reasoning Dynamics* (Sánchez Villegas et al., COLM 2026) | Dossier (pp. 1–9, 20) + AlphaXiv Pass 1 |
| 7 | [2606.28273.pdf](2606.28273.pdf) | `2606.28273` | *Vision-Default, Prior-Override* (Lietzow et al., 2026) | Dossier (abstract/p. 2) + AlphaXiv Pass 2 (full) |
| 8 | [2607.27304.pdf](2607.27304.pdf) | `2607.27304` | *CoT-Mediate / Position, Not Provenance* (Bhowal et al., ICVGIP 2026) | Dossier (pp. 1–6) + AlphaXiv Pass 1 |
| 9 | [2608.17205.pdf](2608.17205.pdf) | `2608.17205` | *Which Source Wins?* (Ghosh, Gupta & Wang, 2026) | Freeze Audit (pp. 1–7, 9, 15–19) + AlphaXiv Pass 1 |
| 10 | [2609.06704.pdf](2609.06704.pdf) | `2609.06704` | *Counterfactual Tests for CoT Faithfulness in VLMs* (Menzat et al., 2026) | Freeze Audit (pp. 1–6) + AlphaXiv Pass 2 (full) |
| 11 | [2609.26986.pdf](2609.26986.pdf) | `2609.26986` | *Evidence Noncommutativity* (Li et al., 2026) | Dossier (pp. 1–5) + AlphaXiv Pass 1 |
| 12 | [2610.19407.pdf](2610.19407.pdf) | `2610.19407` | *Biased Bayesian Observers* (Barua, Mahowald & Rudman, 2026) | Freeze Audit (pp. 1–9, 17–19) + AlphaXiv Pass 1 |
| 13 | [2610.33841.pdf](2610.33841.pdf) | `2610.33841` | *Grounding on Request* (Dassen et al., 2026) | Freeze Audit (pp. 1–9, 15–16) + AlphaXiv Pass 1 |
| 14 | [2610.38296.pdf](2610.38296.pdf) | `2610.38296` | *Hidden Commitment* (Assefa & Cho, ICML 2026) | Dossier (pp. 1–7) + AlphaXiv Pass 1 |
| 15 | [2603.01437.pdf](2603.01437.pdf) | `2603.01437` | *Post-Hoc Reasoning in Chain of Thought* (Cox, Kianersi & Garriga-Alonso, ICML 2026 Wkshp) | AlphaXiv Pass 2 + **Full local PDF audit** |
| 16 | [2510.27484.pdf](2510.27484.pdf) | `2510.27484` | *Thought Branches: Interpreting LLM Reasoning Requires Resampling* (Macar et al., ICLR 2026) | AlphaXiv Pass 2 + **Full local PDF audit** |
| 17 | [2307.13702.pdf](2307.13702.pdf) | `2307.13702` | *Measuring Faithfulness in Chain-of-Thought Reasoning* (Lanham et al., 2023) | AlphaXiv Pass 2 + **Full local PDF audit** |
| 18 | [2609.25366.pdf](2609.25366.pdf) | `2609.25366` | *From Decorative to Load-Bearing* (Jia & Mu, TMLR 2026) | AlphaXiv Pass 2 + **Full local PDF audit** |
| 19 | [2026.magmar-main.3.pdf](2026.magmar-main.3.pdf) | `2026.magmar-main.3` | *CMC-Bench: When Image and Text Disagree in Multimodal RAG* (Catapang, MAGMaR 2026) | AlphaXiv Pass 2 + **Full local PDF audit** |
| 20 | [2606.22862.pdf](2606.22862.pdf) | `2606.22862` | *Chains That See, Answers That Don't* (Fan, Li & Zhuang, EvalMG @ SIGIR 2026) | **Ch. 2 lead — Full local PDF audit** |

### B. Gated Related-Work Lead Audited Without Local PDF
- *Same Reasoning, Different Words: Testing Linguistic Invariance in Chain-of-Thought Monitoring* (Joe Smith, TAE @ NeurIPS 2026, OpenReview `uul4iRQSJ2`) — **`[PDF Not Available]`** (`HTTP 403 Forbidden` on OpenReview; no public arXiv/mirror). Audited strictly from the official NeurIPS 2026 workshop abstract and author CV in [post-v5-pdf-audit.md](post-v5-pdf-audit/post-v5-pdf-audit.md).

*(Note: `Docs/Paper/Archive/` contains older, superseded calibration/hallucination/Bangla/peer-thesis PDFs — do not cite those for v5 claims without re-checking relevance.)*

---

## 1. Corrections Applied During Verification (Preventing Agent Misconceptions)

1. **`k=1` means template #1, not 1 rollout sample:** In this thesis ([PREREGISTRATION_VERDICT_TRANSPLANT.md](../PREREGISTRATION_VERDICT_TRANSPLANT.md) §2.3, §6.2), `K=4` is the set of wording templates; `k=1` means behavioural solving (`max_new_tokens=512`, `do_sample=False`) runs on **template 1 only** for compute reasons. AlphaXiv Pass 1 confused `k=1` with pass@1.
2. **D5 churn is a post-dev gate change, not an `analyze_v5.py` bug:** CoT-Mediate's (`2607.27304` p. 6) paraphrase floor IS the *any-change* flip rate (`1.7–3.3%`). Under any-change, our Math `own` vs. `para` churn is `23.1%` (3B) and `15.2%` (7B). Our working rule separates attributable `image ↔ text` flips from `neither` transitions with fixed bounds (`±5.0 pp` signed mean, `≤ 5.0%` `image↔text` churn, `±10.0 pp` `neither` shift); even under that stricter definition, **non-binding fails** on dev (`7.6%` 3B, `6.6%` 7B).
3. **ChartQA cannot be rescued by prompt re-wording:** ChartQA-Conflict has `229` analysed items (`199` left after 30 dev items), and base competency alone was `13/30` (~43%) for 3B and 7B—below R5's `100`-item floor before edit gates or Sentence-1 leakage. Demoting ChartQA (D4) was forced by dataset arithmetic.
4. **`2503.02199` vs. `2504.08974` table overlap fixed:** AlphaXiv Pass 2 accidentally listed `+56.8 to −74.4 (Table 4, p. 14)` under *Words or Vision* (`2503.02199`); that range belongs to *Mixed Signals* (`2504.08974`).
5. **Conference venue labels:** Rendered arXiv PDF title pages for `2503.02199`, `2504.08974`, and `2505.23945` do not print venue names (though `2505.23945` appears as EMNLP 2025 Findings in later bibliographies).
6. **CMC-Bench exists:** Previously marked "Not found" in the Nov 10 dossier, verified in `prereg-freeze-audit.md` and Pass 2 (`2026.magmar-main.3`).
7. **Post-v5 PDF verification refinements ([post-v5-pdf-audit.md](post-v5-pdf-audit/post-v5-pdf-audit.md)):**
   - `2603.01437`: exact `Qwen2.5-7B` Logical Deduction probe AUC is `0.778` (Table 3, p. 4, not `0.78`); the `50` initially-correct sample is §2.2 only while §2.4 steers full `S_yes`/`S_no` test subsets; App. F adds a `GPT-OSS 20B` reasoning-model replication.
   - `2510.27484`: specific models differ by experiment (`qwen-32b`, `qwen3-235b-a22b`, `llama-3.1-nemotron-ultra-235b-v1`, `deepseek-r1-0528` in §2–§3; `DeepSeek-R1-Qwen-14B` in §4.1; `Qwen3-8B` in §4.2), and in MATH (App. D.1 Table 5, p. 29) Handwritten edits yield higher local plan-shift % (`64.7%` vs. `55.1%`) while Resampled has the highest continuous effect (`3.84 ± 0.06` vs. `3.49 ± 0.02`).
   - `2609.25366`: `temperature = 0` greedy decoding applies across *all* models/experiments (App. P p. 25), and App. S (p. 26) reports an `n = 500` blind two-annotator audit (`κ = 1.000` on `C-vs-non-C`, `κ = 0.927` 4-way).
   - `2026.magmar-main.3`: all 4 VLMs run in 4-bit `mlx-vlm` quantization (none Qwen2.5-VL), and its `gpt-5-mini` judge lacks formal human validation (p. 8).

---

## 2. Master Comparison Matrix (18 Core Papers + CMC-Bench)

| ID / Ref | Short Name | Models | Conflict / Task | Intervention | Primary Metric(s) | Key Verified Finding |
|---|---|---|---|---|---|---|
| `2607.27304` | **CoT-Mediate** (Bhowal et al., ICVGIP 2026) | LLaVA-Med-7B, MedGemma-4B | Medical VQA (VQA-RAD, 515 closed) | Re-prompt vs. prefix-force (`<think>...</think>`); paraphrase $C_2$ | MFS (adoption of $a^{\text{impl}}$); greedy $\le 24$ tok | Prefix-forcing +39.8 pp (LLaVA-Med) / +4.9 pp (MedGemma); paraphrase floor **1.7–3.3%** |
| `2608.17205` | **Which Source Wins?** (Ghosh et al., 2026) | Qwen2-VL-2B, Qwen2.5-VL-7B, LLaVA, Idefics3, Phi-3.5, InternVL2, GPT/Gemini | **Thesis stimuli:** GSM8K/SVAMP + ChartQA-Conflict (229) | 5-level image/text degradation ($L_0\dots L_5$); Source A/B | Length-normalized CLL margin $\Delta\ell$ at `#### `; behavioural check | Opposite task asymmetry (Math $A>0$, ChartQA $A<0$); pooled $\Delta\ell$–behaviour agreement 75.4% (Qwen2.5-VL-7B: 62.6%/68.8%) |
| `2610.19407` | **Biased Bayesian Observers** (Barua et al., 2026) | Qwen2.5-VL-3B/7B, Qwen3.5-4B/9B, Gemma3-4B/12B, GLM-4.6V | DocVQA, VQAv2, RealworldQA | 2D degradation grid (text noise $p$, blur $\sigma$) | Length-normalized log-odds $s(c)=\ell(a_T)-\ell(a_V)$ | Linear Bayes cue rule $R^2=0.80\text{–}0.86$ (Qwen2.5-VL-3B: `0.852`); text 1.4–3.8× stronger when text states answer |
| `2609.26986` | **Noncommutativity** (Li et al., 2026) | Qwen2.5-VL-3B, Idefics3-8B, Pixtral-12B + audio | GQA, VQAv2, FSC, SLURP | Swap $(I,P,T,q)$ vs. $(I,T,P,q)$, $I,q$ fixed | Selection shift $\Delta A^-$; log-odds swap $C_\theta$ | Recency bias **+9.8 to +28.1 pp** (Qwen2.5-VL-3B: +16.7 GQA, +15.0 VQAv2); moving $I$ flips sign by 38.1 pp |
| `2610.33841` | **Grounding on Request** (Dassen et al., 2026) | Gemma-3-4B, Qwen3.5-4B, Qwen3.5-2B | VCF, ColorSwap, COCO-CF, Ground-CF, MultiVENT-G | NL instruction vs. `<look>`/`<read>` + LoRA | $\text{FLIP}_s$ & $\text{STAY}_{s,u}$ (summed token LL) | NL image request weak (55.5% ID acc, **36.7% FLIP**) vs. text (84.8% acc, **78.4% FLIP**) |
| `2511.02243` | **When Modalities Conflict** (Zhang et al., 2025) | LLaVA-1.5/1.6 (7B/13B), Qwen-VL, Qwen2-VL, Qwen2.5-VL (7B) | Synthetic color/attribute difficulty tiers | Visual/text difficulty $d_v, d_t$; logit lens | $\Delta H_{\text{rel}}$, balance point; **competency filter** | Text reliance falls monotonically with $\Delta H_{\text{rel}}$; Qwen leans visual; layers oscillate near balance point |
| `2610.38296` | **Hidden Commitment** (Assefa & Cho, ICML 2026) | Qwen3.5-0.8B, Gemma-3-1B (text-only) | Retrieval QA conflict (FaithEval, 1,500) | Residual readout $\hat{v}_{\text{doc}}$, CETT, steering $\delta\pm 3$ | Probe AUROC, steered choice % | Choice readable Layer 13 decision tokens (AUROC 0.994), weak pre-response; disclosure Layer 17; steering shifts 51.5%→74.7%/32.2% |
| `2604.14888` | **Answer Inertia** (Sánchez Villegas et al., COLM 2026) | 18 VLMs incl. Qwen2.5-VL-3B/7B/32B, Qwen3-VL, InternVL3/3.5 | MathVerse, PhyX, ScienceQA + text hints | Prefix truncation $t\in[0,T]$, hint injection, monitors | $P_M(y\mid x,\text{CoT}_{1:t})$, Net Gain of CoT | Early commitment in steps 1–2 ("answer inertia"); CoT reinforces rather than revises; silent hint following |
| `2603.01437` | **Post-Hoc Reasoning** (Cox et al., ICML 2026 Wkshp) | 5 Gemma-2 & Qwen2.5 (incl. Qwen2.5-3B) | Text-only: Anachronisms, Logical Deduction, Social Chem, Sports | Ellipsis CoT removal, misleading CoT swap, pre-CoT probe & steering ($T=0.7$) | Answer-change rate, probe AUC | Pre-CoT AUC 0.996 (Anachronisms) vs. **0.690** (Logical Deduction, Qwen2.5-3B) where CoT computes answer |
| `2510.27484` | **Thought Branches** (Macar et al., ICLR 2026) | Reasoning LLMs | Blackmail/whistleblowing, MCQA, MATH appendix | Off-policy edit vs. on-policy resampling (100 rollouts, $T=0.7$) | KL counterfactual importance, resilience | On-policy resampling yields stronger plan shifts (67.4%/87.4%); removed ideas can reappear ("resilience") |
| `2609.06704` | **Counterfactual Tests** (Menzat et al., 2026) | 8 VLMs (incl. Qwen2.5-VL-32B) | Counter-SNLI-VE, Counter-A-OKVQA | Object removal in image + no-op editor control | Continuous vCCT (TVD corr) vs. binary vCT | Binary vCT saturates (0.93–0.95); continuous vCCT discriminates (0.13–0.30). No equivalence bounds |
| `2602.14518` | **Diagnosing Knowledge Conflict** (Tang et al., 2026) | R1-Onevision-7B, Ocean-R1-7B (Qwen2.5-VL), Llama-3.2V-11B-cot | Vision–text, vision–prior, prior–text (PhD, TruthfulQA) | Contrastive decoding, steering, probe reweighting | Anchor-support / rejection / error rates | Steering *toward* truth anchor (vision in V-T) is easier than forcing opposing source |
| `2503.02199` | **Words or Vision** (Deng et al., 2025) | 10 VLMs (incl. Qwen2-VL-7B, Phi-3.5, GPT-4o) | VQAv2, DocVQA, MathVista, phishing + GPT-4o text | Text relevance/corruption, prompts ("Focus on Image/Text"), token order ($T=0$) | Text-preference ratio $p_\text{text}/(p_\text{text}+p_\text{image})$ | Qwen2-VL-7B TPR 29.22% (corrupt) / 13.17% (matched) on VQAv2; prompt shifts only ~2.6 pp (16.8%→14.2%) |
| `2504.08974` | **Mixed Signals** (Pezeshkpour et al., 2025) | Qwen2-VL-7B/72B, Llama-3.2-90B, GPT-4o(-mini) | 5 mismatch tasks (1,729 items) | Verbalized, 3-step CoT, 3-run decomposed prompts | Image−Text preference %, Acc, F1 | Bias flips by task/difficulty: spans **+56.8 image to −74.4 text** (Table 4, p. 14) |
| `2505.23945` | **Bias & CoT Faithfulness** (Balasubramanian et al., 2025) | Qwen2.5-VL-3B/7B/72B, InternVL, Llama-3.2V | Hints, overlays, Waterbirds, CelebA | Paired biased/unbiased inputs; CoT articulation | Articulation / reliance / omission rates | Visual/subtle cues rarely articulated (0% CelebA gender bias articulation for Qwen2.5-VL-3B/7B) |
| `2606.28273` | **Vision-Default, Prior-Override** (Lietzow et al., 2026) | Qwen2.5-VL-3B/7B, LLaVA-NeXT-7B, PaliGemma-3B/10B | Counterfactual color images (perception vs. prior) | Residual/head/MLP patching & ablation | Visual vs. prior flip rates | Ablating sparse prior heads flips **68–96%** prior answers vs. **0.8–7.5%** visual answers |
| `2307.13702` | **Measuring Faithfulness** (Lanham et al., 2023) | 175B RLHF LM (text-only) | 8 MCQA tasks + synthetic addition | Truncation, mistake injection, filler, paraphrase (100 samples, $T=0.8$) | AOC / answer-change rate | Task-dependent CoT sensitivity (AQuA 0.44/0.52 vs. ARC Easy 0.02/0.07); no TOST |
| `2609.25366` | **Decorative to Load-Bearing** (Jia & Mu, TMLR 2026) | Gemma-2-9B-IT, Llama-3.1-8B, DeepSeek-R1-Distill-Qwen-7B | GSM8K, MMLU, BBH (text-only) | Step perturbation + forced continuation; human audit | Bypass, self-correction, error propagation | GSM8K 94.5% bypass / 3.9% propagation vs. BBH 37.4% / 40.9%; difficulty drives 98.8% deviance |
| `2026.magmar-main.3` | **CMC-Bench** (Catapang, MAGMaR 2026) | 4 quantized 4-bit VLMs | Multimodal RAG (3,768 ChartQA & MMMU conflict items) | Aligned, image-correct, text-correct, both-wrong | LLM judge `{IMAGE, TEXT, BOTH, NEITHER, ABSTAIN}` | Measures RAG modality preference & abstention; **no CoT faithfulness or verdict forcing** |

---

## 3. Complete Per-Paper Specification Sheets (1–19)

### 3.1 Anchor Papers (Local PDFs Present — Pass 1 & Local Audits)

#### 1. CoT-Mediate — Bhowal et al. (2026) | `[Local PDF: 2607.27304.pdf]`
- **Citation:** Supratik Bhowal, Subhrajyoti Basu, Aritra Gir Mahanta, Anik Pal Chowdhury. *Position, Not Provenance: Separating Reasoning Mediation from Sycophancy in Medical Vision-Language Models*, arXiv:2607.27304v1 (ICVGIP 2026). `[Verified]`
- **Paradigm & Data:** Medical VQA on VQA-RAD (1,000 items, 515 closed yes/no ground truth) with open VLMs (`LLaVA-Med v1.5 Mistral-7B`, `MedGemma-4B-IT`). Tests whether CoT drives answers vs. post-hoc rationalization. `[Verified]`
- **Intervention & Controls:** Minimal single-attribute edit inside the model's self-generated baseline CoT ($c_i$) across 7 clinical attribute families (laterality, presence/absence, severity, size, location, density, diagnosis). Compares **Arm 1 (Re-prompt)** `[image][question] Evidence: {edited text}` vs. **Arm 2 (Prefix-Forced Continuation)** `[image][question] <think>{edited CoT}</think>\n<answer>` (prompt-string level, no KV-cache surgery; p. 3). Controls: $C_0$ (image only), $C_1$ (re-injected original CoT), $C_2$ (zero-change paraphrase floor), $C_3$ (perturbed CoT + trust prompt), $C_4$ (grey-canvas image ablation), $C_5$ (perturbed CoT without trust prompt). `[Verified, pp. 3–6]`
- **Metrics & Decoding:** Mediation Faithfulness Score ($\text{MFS}$ = rate of transitioning to $a_i^{\text{impl}}$) and $\Delta_{\text{MFS}} = \text{MFS}(\text{Arm 2}) - \text{MFS}(\text{Arm 1})$; greedy decoding (`do_sample=False`, fixed seed), rollout $\le 256$ tokens, continuation $\le 24$ tokens; item bootstrap (2,000 resamples), exact McNemar, Holm correction (p. 4). `[Verified, pp. 4–5]`
- **Key Findings:** Prefix-forcing dramatically exceeds re-prompting: **+39.8 pp** in LLaVA-Med (`33.3% → 73.5%`) and **+4.9 pp** in MedGemma (`55.9% → 61.6%`). Self-attribution discounting in re-prompting drops LLaVA-Med adoption `34.3% → 16.0%` (pp. 1, 6). Paraphrase noise floor ($C_2$): **1.7% [0.6, 3.0]** (LLaVA-Med) / **2.8% [1.3, 4.6]** (MedGemma) under re-prompt; **3.3% [1.9, 5.0]** / **0.5% [0.0, 1.2]** under prefix-forcing (p. 6). Sycophancy: removing "trust" shifts flips `-1.7 pp` (`p=0.20`) in LLaVA-Med vs. `+9.0 pp` (`p=3.1e-8`) in MedGemma. `[Verified]`
- **Thesis Relevance & Limits:** Closest methodological ancestor (`own` ≈ $C_1$, `para` ≈ $C_2$, prefix-forced continuation, minimal-edit gates). Does **not** test image–text conflict or source-reliability verdicts, and its 1.7–3.3% paraphrase floor holds over `≤ 24`-token answers, not ~400-token math CoTs. `[Verified/Inferred]`

#### 2. Which Source Wins? — Ghosh, Gupta & Wang (2026) | `[Local PDF: 2608.17205.pdf]`
- **Citation:** Rodela Ghosh, Aviral Gupta, Guangjing Wang. *Which Source Wins? Task-Dependent Reliance in Vision–Language Models*, arXiv:2608.17205v1. `[Verified]`
- **Paradigm & Data:** **Source of both thesis stimulus sets.** Arithmetic task-selection conflict: GSM8K (1,319) + SVAMP (300) rendering problem $i$ in image vs. text problem $(i+1) \pmod N$. Evidence conflict: ChartQA-Conflict (229 verified items; row `conflict_id=45` excluded post-run because report put 2.81 under Sept 2019 while question asked March 2021; §3.2.2, p. 4). `[Verified]`
- **Intervention & Decoding:** 5-level image degradation ($L_0$ clean → $L_5$ blur+noise+contrast) and text character corruption ($L_0\dots L_5$). Open models (`Qwen2-VL-2B`, `Qwen2.5-VL-7B`, `LLaVA-1.6-Mistral-7B`, `LLaVA-OneVision-7B`, `Idefics3-8B`, `Phi-3.5-Vision-4B`, `InternVL2-8B`): greedy, `bfloat16`, batch size 1, max tokens 256 (arithmetic) / 128 (ChartQA). Uses Source A/B labels (odd items swapped in arithmetic, p. 3; ChartQA always has A shown first, p. 18). `[Verified]`
- **Metrics & Findings:** Length-normalized CLL margin at `#### ` (*text minus image*): $m(c) = \frac{1}{|a_T|}\log P(a_T\mid c) - \frac{1}{|a_I|}\log P(a_I\mid c)$ with **no CoT** ("measures direct-answer preference, not reasoning-trace attribution", p. 5). Opposing task asymmetries: on GSM8K/SVAMP, 5/6 models shift away from degraded text ($A>0$); on ChartQA-Conflict, all 6 shift away from degraded vision ($A<0$; `Qwen2.5-VL-7B` $A=-1.362$). Pooled $\Delta\ell$–behaviour agreement is **75.4%**, but **per-model rows (Table 5, p. 15)** show `Qwen2.5-VL-7B` at `62.6% / 68.8%` and `Qwen2-VL-2B` at `72.6% / 58.6%`. Their random-intercept mixed model failed due to singular boundary variance (p. 16). `[Verified]`
- **Thesis Relevance & Limits:** Supplies datasets, `####` scoring convention, and `last_num` arithmetic fallback precedent (`lenient` parser, p. 12). Does **not** counterbalance evidence order independently of A/B letters, does not use CoT before `####` margin, and has no verdict intervention. `[Verified/Inferred]`

#### 3. Biased Bayesian Observers — Barua, Mahowald & Rudman (2026) | `[Local PDF: 2610.19407.pdf]`
- **Citation:** Josh Barua, Kyle Mahowald, William Rudman. *Vision-Language Models Integrate Conflicting Evidence Like Biased Bayesian Observers*, arXiv:2610.19407v1. `[Verified]`
- **Paradigm & Models:** DocVQA, VQAv2, RealworldQA under 2D continuous degradation grid (text noise $p\in[0,1]$, visual blur $\sigma\in[0,32]$). Models include `Qwen2.5-VL-3B`, `Qwen2.5-VL-7B`, `Qwen3.5-4B/9B`, `Gemma3-4B/12B`, `GLM-4.6V-Flash`. `[Verified]`
- **Metrics & Findings:** Length-normalized candidate-answer log-odds $s(c)=\ell(a_T\mid c)-\ell(a_V\mid c)$ (Eq. 1, p. 3) modeled as $\hat{s}_J = \beta_T e_T + \beta_V e_V + \pi_0$ (Eq. 6, p. 5). Achieves $R^2=0.80\text{–}0.86$ (`Qwen2.5-VL-3B`: $R^2=0.852$, Table 1, p. 6; interaction term adds $\le 0.001$). "Blind faith in text" arises because clean text provides **1.4–2.7×** stronger evidence ($|e_T|\gg|e_V|$, Table 3, p. 8), and when text states an answer while an image must be interpreted, text evidence is **1.4–3.8×** stronger (pp. 7–8). After free reasoning, choices agree with $\operatorname{sign}(s_J)$ in **75.3–82.0%** of pairs (`81.8–93.9%` in highest $|s_J|$ tertile, App. B.5, p. 19). `[Verified]`
- **Thesis Relevance & Limits:** Explains why ChartQA-Conflict text reports dominate charts (`1.4–3.8×`), and why probability-scale CDE saturates at large baseline $|s_i|$ (motivating tertile stratification). Never touches CoT verbalizations. `[Verified/Inferred]`

#### 4. Evidence Noncommutativity — Li, Wang, Huang & Dong (2026) | `[Local PDF: 2609.26986.pdf]`
- **Citation:** Zhuoyun Li, Boxuan Wang, Xiaowei Huang, Yi Dong. *Same Evidence, Different Judgments: Evidence Noncommutativity in Vision/Speech-Text Conflicts*, arXiv:2609.26986v1. `[Verified]`
- **Paradigm & Intervention:** Swaps only evidence position $(I,P,T,q)$ vs. $(I,T,P,q)$ with instruction $I$, question $q$, and options fixed (Eq. 1, p. 2), using role headers rather than source letters (only answer options A/B are swapped). Datasets: GQA/VG, VQAv2/COCO, FSC, SLURP. Models include `Qwen2.5-VL-3B-Instruct`, `Idefics3-8B`, `Pixtral-12B`. `[Verified]`
- **Metrics & Findings:** $\Delta A^- = A(T^-\to P) - A(P\to T^-)$ and log-odds swap score $C_\theta$ (Eqs. 3–4, p. 2). Universal recency bias: placing attachment last raises attachment choices by **+9.8 to +28.1 pp** across all 12 setups; for `Qwen2.5-VL-3B`: **+16.7 pp** (GQA) and **+15.0 pp** (VQAv2) (pp. 3–4). Moving the instruction together with text reverses the apparent sign by `38.1 pp` (`-28.6` vs. `+9.5` in Fig. 3 ablation, p. 4). Adding *"prioritize the image"* leaves 89–145% of the order effect intact (p. 3). Competency precedent: uses `807` dual-competent items (p. 4). `[Verified]`
- **Thesis Relevance & Limits:** Dictates v5 Mandatory Invariant 1 (fixed $I$ before sources, fixed $F$ after, modality headers only, counterbalanced `<image><text>` vs. `<text><image>`). Closed-choice only; no rationale edits. `[Verified]`

#### 5. Grounding on Request — Dassen et al. (2026) | `[Local PDF: 2610.33841.pdf]`
- **Citation:** Maxime Dassen, Alexander Martin, Andrew Yates, Reno Kriz, William Walden. *Grounding on Request: Learning Modality Control in Vision-Language Models*, arXiv:2610.33841v1. `[Verified]`
- **Paradigm & Intervention:** User-requested modality control on VCF, ColorSwap, COCO-CF, Ground-CF, MultiVENT-G (`Gemma-3-4B`, `Qwen3.5-4B`, `Qwen3.5-2B`). Compares natural-language instruction baseline (*"According to the image (and only the image)..."*, Table 7, p. 15) against learned tokens (`<look>`, `<read>`) and LoRA. Evidence order alternates across items (p. 15). `[Verified]`
- **Metrics & Findings:** Summed token log-likelihood forced choice (Eq. 1, p. 4); $\text{FLIP}_s$ (tracks requested edit) & $\text{STAY}_{s,u}$ (invariant to unrequested edit). NL instructions give **weak, asymmetric visual control**: visual accuracy `55.5%` ID / `57.3%` OOD, visual **FLIP `36.7%` (ID) / `40.1%` (OOD)** vs. text accuracy `84.8%` and **FLIP `78.4%`** (Table 2, p. 7). Remarkably, learned tokens control behaviour *"without the model being able to clearly explain or self-verbalize their meaning"* (p. 8)—the mirror image of "saying is not choosing." `[Verified]`
- **Thesis Relevance & Limits:** Replicates our `explicit_image`/`explicit_text` benchmark arms (never claimed novel) and predicts strong directional asymmetry (`explicit_image` weaker than `explicit_text`), justifying per-direction benchmark reporting. No CoT or prefix-forced verdicts. `[Verified/Inferred]`

#### 6. When Modalities Conflict — Zhang et al. (2025) | `[Local PDF: 2511.02243.pdf]`
- **Citation:** Zhuoran Zhang, Tengyue Wang, Xilin Gong, Yang Shi, Haotian Wang, Di Wang, Lijie Hu. *When Modalities Conflict: How Unimodal Reasoning Uncertainty Governs Preference Dynamics in MLLMs*, arXiv:2511.02243v1. `[Verified]`
- **Paradigm & Models:** Controlled difficulty tiers ($d_v\in[0,13]$, $d_t\in[0,2]$) on synthetic single-token color/attribute conflicts (`LLaVA-1.5/1.6 7B/13B`, `Qwen-VL`, `Qwen2-VL`, `Qwen2.5-VL-7B` — note: **no 3B**). `[Verified]`
- **Metrics & Findings:** **Competency conditioning precedent** (p. 5: keep only items correct in both unimodal runs). Normalized relative unimodal uncertainty $\Delta H_{\text{rel}} = \frac{2(H^{(t)}-H^{(v)})}{H^{(t)}+H^{(v)}}$ (p. 6). Text preference falls monotonically with $\Delta H_{\text{rel}}$; Qwen models have negative balance points (inherent visual preference), LLaVA positive; intermediate layers oscillate near the balance point ($\pm 0.5$ window, pp. 6–8). `[Verified]`
- **Thesis Relevance & Limits:** Supplies our competency filter and $\Delta H_{\text{rel}}$ stratification (adapted from single-token entropy to length-normalized gold-answer NLL for multi-token GSM8K answers). Synthetic single-token tasks; no verbalization. `[Verified/Inferred]`

#### 7. Hidden Commitment — Assefa & Cho (2026) | `[Local PDF: 2610.38296.pdf]`
- **Citation:** Samuel Dawit Assefa, Jae Won Cho. *Hidden Commitment: When Language Models Silently Pick a Side and How Steering Can Surface It*, arXiv:2610.38296v2 (ICML 2026). `[Verified]`
- **Paradigm & Intervention:** Text-only retrieval QA under conflicting documents (FaithEval, 1,500 items; `Qwen3.5-0.8B`, `Gemma-3-1B`). Fits class-centroid readout $\hat{v}_{\text{doc}}$, localizes sparse MLP writers via CETT, and steers residuals $\tilde{h}_t^{(\ell)} = h_t^{(\ell)} + \delta\,\text{RMS}(h_t^{(\ell)})\hat{v}_{\text{doc}}$ (pp. 3–6). `[Verified]`
- **Key Findings:** Source choice readout peaks around answer/decision tokens at **Layer 13** (AUROC `0.9945`), while prompt-final and first-response tokens are weak (pp. 4–5). Conflict *disclosure* peaks at **Layer 17** pre-response and is only partly steerable—authors note they *"look like different internal states"* (p. 6; **does not prove decoupled circuits**). Steering $\delta=\pm 3$ shifts document-2 answers `51.5% → 74.7% / 32.2%` (p. 4; noisy in Gemma). `[Verified]`
- **Thesis Relevance & Limits:** Closest conceptual anchor ("disclosing conflict" vs. "choosing a source"), though text-only, small-scale (0.8B–1B), and testing conflict disclosure rather than reliability verdicts. `[Verified/Inferred]`

#### 8. Reasoning Dynamics / Answer Inertia — Sánchez Villegas et al. (2026) | `[Local PDF: 2604.14888.pdf]`
- **Citation:** Danae Sánchez Villegas, Samuel Lewis-Lim, Nikolaos Aletras, Desmond Elliott. *Reasoning Dynamics and the Limits of Monitoring Modality Reliance in Vision-Language Models*, arXiv:2604.14888v3 (COLM 2026). `[Verified]`
- **Paradigm & Models:** Step-wise reasoning dynamics on MathVerse, PhyX, ScienceQA across 18 VLMs (incl. `Qwen2.5-VL-3B/7B/32B`, `Qwen3-VL`, `InternVL3/3.5`; note: hint/monitorability parts use `7B/32B/8B`, not `3B`). `[Verified]`
- **Intervention & Findings:** Prefix truncation $P_M(y\mid x, \text{CoT}_{1:t})$ (Eq. 1, pp. 4–5) + misleading text hints + CoT monitors. **Answer inertia:** instruction-tuned models assign highest probability to their final answer within the first 1–2 CoT steps and reinforce rather than revise (pp. 1, 6). Hints shift answers even when vision suffices, and fluent CoTs conceal silent hint-following. `[Verified]`
- **Thesis Relevance & Limits:** Predicts early commitment in CoTs, though it injects input hints rather than prefix-forcing edits to the model's own verdict. `[Verified/Inferred]`

---

### 3.2 Remaining 10 Core Papers + CMC-Bench (Pass 2 Verified Reads)

#### 9. Post-Hoc Reasoning in CoT — Cox, Kianersi & Garriga-Alonso (2026) | `[Local PDF: 2603.01437.pdf]`
- **Citation:** Kyle Cox, Darius Kianersi, Adrià Garriga-Alonso. *Post-Hoc Reasoning in Chain of Thought: Decoding and Steering Pre-Committed Answers*, arXiv:2603.01437v2 (ICML 2026 Mechanistic Interpretability Workshop, p. 1). `[Verified]`
- **Paradigm & Intervention:** Five instruction-tuned Gemma-2 and Qwen2.5 models (`2B/9B`, `1.5B/3B/7B`) plus `GPT-OSS 20B` (App. F, p. 21) on Anachronisms, Logical Deduction, Social Chemistry, Sports Understanding (500 train / 500 test each, p. 2). §2.2 runs Ellipsis / Incorrect CoT swaps on `50` initially-correct test items/cell; §2.3–§2.5 run pre-CoT residual probing and probe-direction steering ($T=0.7$) across full $S_{\text{yes}}/S_{\text{no}}$ correct subsets (`min n >= 20`) vs. `50` random test examples for the orthogonal baseline (pp. 2–5). `[Verified]`
- **Key Findings:** Pre-CoT probe AUC is `0.996` on Anachronisms vs. **`0.690`** on Logical Deduction for `Qwen2.5-3B` (**`0.778`** for 7B; Table 3, p. 4) because CoT performs actual computation on Logical Deduction. CoT removal shifts answers $\le 20\%$ in 18/20 pairs, whereas misleading-CoT swaps cause `52–78%` flips on Anachronisms (`78%` on Qwen2.5-3B/7B; Table 8, p. 20). `[Verified]`
- **Thesis Relevance & Limits:** Best mechanistic explanation for **D1**: why pre-CoT $\Delta\ell$ at `####` fails to predict multi-step Math solving (`51.6%` / `56.6%` sign agreement on dev). Text-only binary tasks; steering also ran at answer tokens (Sec. 4.1, p. 6). `[Inferred]`

#### 10. Thought Branches — Macar et al. (2026) | `[Local PDF: 2510.27484.pdf]`
- **Citation:** Uzay Macar, Paul C. Bogdan, Senthooran Rajamanoharan, Neel Nanda. *Thought Branches: Interpreting LLM Reasoning Requires Resampling*, arXiv:2510.27484v2 (ICLR 2026, p. 1). `[Verified]`
- **Paradigm & Intervention:** Resamples trajectory segments ($T=0.7$, top-$p=0.95$, `20` base traces, `100` rollouts/sentence; Sec. 2, p. 2) in blackmail/whistleblowing (`qwen-32b`, `qwen3-235b-a22b`, `llama-3.1-nemotron-ultra-235b-v1`, `deepseek-r1-0528`), hinted MCQA (`DeepSeek-R1-Qwen-14B`), resume evals (`Qwen3-8B`), and MATH (App. D.1, p. 29). Compares off-policy handwritten/copied edits vs. on-policy resampling; measures KL counterfactual importance and "resilience" (removed step reappearing later; Eqs. 1–2, p. 3). `[Verified]`
- **Key Findings:** On-policy interventions yield larger directional shifts (`67.4%` blackmail, `87.4%` whistleblowing plan shifts; Table 1, p. 5); in MATH (Table 5, p. 29), handwritten local plan-shift % is `64.7%` vs. `55.1%` resampled, while resampled leads continuous `0–5` effect (`3.84 ± 0.06` vs. `3.49 ± 0.02`). Off-policy edits can be ignored or overwritten. `[Verified]`
- **Thesis Relevance & Limits:** Explains off-policy verdict caveats (`CDE`, not natural mediation) and resilience (e.g., `none` regenerating a verdict). Motivates an optional `T=0.7` sampled sensitivity check, though greedy decoding remains a valid deterministic target. `[Inferred]`

#### 11. Counterfactual Tests for CoT Faithfulness in VLMs — Menzat et al. (2026) | `[Local PDF: 2609.06704.pdf]`
- **Citation:** Bayar Menzat, Maximilian Süss, Ruizhi Wang, Benno Steinegger, Thomas Lukasiewicz, Oana-Maria Camburu. *Counterfactual Tests for Measuring Chain-of-Thought Faithfulness in Visual Language Models*, arXiv:2609.06704v1 (no venue on title page). `[Verified]`
- **Paradigm & Controls:** Object-removal image edits on Counter-SNLI-VE and Counter-A-OKVQA across 8 open VLMs (incl. `Qwen2.5-VL-32B`, Sec. 3.4, p. 5), plus a **no-op reconstruction control** (p. 5). Explicitly contrasts its paradigm with "CoT Interventions" (p. 2). `[Verified]`
- **Metrics & Stats:** Continuous **vCCT** (Pearson $r$ between answer TVD and mention flag, Eq. 6, p. 6) vs. binary **vCT** (Eq. 8). vCT saturates (`0.930–0.951` A-OKVQA, `0.895–0.949` SNLI-VE, Table 2, p. 7), whereas vCCT discriminates (`0.200–0.303` / `0.129–0.264`, Table 1, p. 7). Uses `B=10,000` bootstrap/permutation ($p=\frac{1+b}{B+1}$, Eq. 10, p. 6) and 2-coder human audit (`κ = 0.651–0.795`). **No equivalence test or TOST.** `[Verified]`
- **Thesis Relevance & Limits:** Supplies our $B=10,000$ `(1+b)/(B+1)` permutation formula, no-op control analogue (`para`), and warning against binary saturation. `[Verified/Inferred]`

#### 12. Diagnosing Knowledge Conflict — Tang et al. (2026) | `[Local PDF: 2602.14518.pdf]`
- **Citation:** Jing Tang, Kun Wang, Haolang Lu, Hongjin Chen, KaiTao Chen, Zhongxiang Sun, Qiankun Li, Lingjuan Lyu, Guoshun Nan, Zhigang Zeng. *Diagnosing Knowledge Conflict in Multimodal Long-Chain Reasoning*, arXiv:2602.14518 (no venue on title page). `[Verified]`
- **Paradigm & Models:** Vision–text, vision–prior, and prior–text conflicts (PhD, TruthfulQA; App. A, pp. 13–15) on `R1-Onevision-7B`, `Ocean-R1-7B` (Qwen2.5-VL-based), `Llama-3.2V-11B-cot` (greedy / top-$k=5$, App. B, p. 17). Contrastive decoding, representation steering, probe reweighting (p. 7). `[Verified]`
- **Key Findings:** **Directional asymmetry:** steering toward the truth-anchored source (vision in V-T conflicts) is easier than forcing the opposing source (Sec. 5.2, p. 7; App. D, p. 21). `[Verified]`
- **Thesis Relevance & Limits:** Supports reporting `text→image` and `image→text` descriptively, though truth-anchor asymmetry does not directly map onto two equally valid Math problems. `[Inferred]`

#### 13. Words or Vision — Deng, Cao, Chen & Hooi (2025) | `[Local PDF: 2503.02199.pdf]`
- **Citation:** Ailin Deng, Tri Cao, Zhirui Chen, Bryan Hooi. *Words or Vision: Do Vision-Language Models Have Blind Faith in Text?*, arXiv:2503.02199v1 (no venue on arXiv title page). `[Verified]`
- **Paradigm & Findings:** 1,000 VQAv2, 1,000 DocVQA, 1,000 MathVista, 2,500 phishing items with matched/corrupted/irrelevant GPT-4o text ($T=0$, 10 VLMs; Sec. 3.1, p. 3). Metric: TPR $p_{\text{text}}/(p_{\text{text}}+p_{\text{image}})$. `Qwen2-VL-7B` VQAv2 TPR is `29.22%` (corrupt) / `13.17%` (matched) (Table 11, p. 20); *"Focus on Image"* vs. *"Focus on Text"* shifts preference only `16.8% → 14.2%` (p. 6) and boosts macro accuracy 1–2% (p. 7); token order shifts Phi-3.5 (Fig. 6, p. 7). `[Verified]`
- **Thesis Relevance:** Baseline evidence of modality bias and weak external prompting; later criticized by *Noncommutativity* (`2609.26986`) for moving instructions alongside evidence. `[Verified]`

#### 14. Mixed Signals — Pezeshkpour, Aminnaseri & Hruschka (2025) | `[Local PDF: 2504.08974.pdf]`
- **Citation:** Pouya Pezeshkpour, Moin Aminnaseri, Estevam Hruschka. *Mixed Signals: Decoding VLMs' Reasoning and Underlying Bias in Vision-Language Conflict*, arXiv:2504.08974v1 (no venue on arXiv title page). `[Verified]`
- **Paradigm & Findings:** 5 mismatch datasets (1,729 items: graph connectivity, convexity, polynomial roots, science, spatial; Table 2, p. 10) across `Qwen2-VL-7B/72B`, `Llama-3.2-90B-Vision`, `GPT-4o(-mini)`. Compares Verbalized, 3-step CoT, and 3-run Decomposed prompts for mismatch *detection* (pp. 3–4). Image−text bias ranges from **+56.8 image-favoring to −74.4 text-favoring** by task/difficulty (Table 4, p. 14). `[Verified]`
- **Thesis Relevance:** Cautions against pooling heterogeneous tasks or directions; mitigation prompts detect conflict rather than testing whether a verdict steers solving. `[Verified/Inferred]`

#### 15. Bias & CoT Faithfulness of L(V)LMs — Balasubramanian, Basu & Feizi (2025) | `[Local PDF: 2505.23945.pdf]`
- **Citation:** Sriram Balasubramanian, Samyadeep Basu, Soheil Feizi. *A Closer Look at Bias and Chain-of-Thought Faithfulness of Large (Vision) Language Models*, arXiv:2505.23945v2 (listed as EMNLP 2025 Findings in later bibliographies; title page omits venue). `[Verified]`
- **Paradigm & Findings:** Bias injection (answer hints/order/markings, overlays, Waterbirds, CelebA) including `Qwen2.5-VL-3B` and `7B` (Sec. 4, p. 5). Visual/subtle cues are articulated far less than text cues (`0%` CelebA gender bias articulation for Qwen2.5-VL-3B/7B, Table 6, p. 23); observes inconsistent reasoning where models reason cleanly then abruptly flip answers (p. 1). `[Verified]`
- **Thesis Relevance:** Supports checking CoT articulation and reasoning flips, though testing bias articulation rather than verdict steering. `[Inferred]`

#### 16. Vision-Default, Prior-Override — Lietzow et al. (2026) | `[Local PDF: 2606.28273.pdf]`
- **Citation:** Niclas Lietzow, Danielle Bitterman, Carsten Eickhoff, William Rudman, Michal Golovanevsky. *Vision-Default, Prior-Override: Causal Mechanisms of Perception-Knowledge Conflict in Vision-Language Models*, arXiv:2606.28273v2. `[Verified]`
- **Paradigm & Findings:** Counterfactual color images pitting visual perception against parametric memory (`Qwen2.5-VL-3B/7B`, `LLaVA-NeXT-7B`, `PaliGemma-3B/10B`, p. 3). Residual/head/MLP ablation shows sparse late "prior" heads: ablating them flips **68–96%** of prior-grounded answers vs. **0.8–7.5%** of visually grounded answers (Table 2, p. 7). `[Verified]`
- **Thesis Relevance:** Mechanistic evidence of directional routing asymmetry, though for perception-vs-memory rather than image-vs-text conflict. `[Inferred]`

#### 17. Measuring Faithfulness in CoT Reasoning — Lanham et al. (2023) | `[Local PDF: 2307.13702.pdf]`
- **Citation:** Tamera Lanham et al., *Measuring Faithfulness in Chain-of-Thought Reasoning*, arXiv:2307.13702v1. `[Verified]`
- **Paradigm & Findings:** Text-only 175B RLHF LM across 8 MCQA tasks + synthetic addition (`100` samples/item, $T=0.8$, top-$p=0.95$; Sec. 2.1, p. 3) plus `13B -> 175B` inverse scaling (§3.1 Fig. 7, p. 7). Tests early truncation, mistake injection, filler, and prefix paraphrasing (Footnote 3, p. 7 notes full-CoT paraphrasing trivially leaks the stated answer). Early-answering / mistake AOC is high on AQuA (`0.44` / `0.52`) vs. near zero on ARC Easy (`0.02` / `0.07`; Table 2, p. 5). Paraphrase accuracy is close to original descriptively (Sec. 2.6.1, p. 7) with **no TOST or churn bound**. `[Verified]`
- **Thesis Relevance:** Foundational CoT intervention baseline (and source of "larger models are less faithful", not Turpin et al.); explains why non-significance ≠ equivalence and why prefix-only edits beat full-CoT rewrites. `[Verified/Inferred]`

#### 18. From Decorative to Load-Bearing — Jia & Mu (2026) | `[Local PDF: 2609.25366.pdf]`
- **Citation:** Renee Jia, Di Mu. *From Decorative to Load-Bearing: Task Difficulty Shapes the Causal Role of Chain-of-Thought*, arXiv:2609.25366 (TMLR, August 2026, p. 1). `[Verified]`
- **Paradigm & Findings:** Forced continuation after perturbing one reasoning step (early/mid/late) on GSM8K, MMLU, BBH (`Gemma-2-9B-IT`, `Llama-3.1-8B-Instruct`, `DeepSeek-R1-Distill-Qwen-7B`; `temperature = 0` greedy decoding across all experiments, App. P, p. 25), validated with `n = 500` blind two-annotator human audit (`κ = 1.000` on C-vs-non-C, `κ = 0.927` 4-way, App. S, p. 26). Gemma shows `94.5%` bypass / `3.9%` error propagation on GSM8K vs. `37.4%` / `40.9%` on BBH (Table 1, p. 6); task difficulty explains `98.8%` of deviance vs. `0.8%` perturbation type (p. 2); single-direction residual steering fails (§5.5, p. 9). `[Verified]`
- **Thesis Relevance:** Confirms CoT causal load-bearingness is task/difficulty-dependent and provides a greedy-decoding forced-continuation precedent. `[Inferred]`

#### 19. CMC-Bench — Catapang (2026) | `[Local PDF: 2026.magmar-main.3.pdf]`
- **Citation:** Jasper Kyle Catapang. *When Image and Text Disagree: Cross-Modal Evidence Conflict in Multimodal Retrieval-Augmented Generation*, Proceedings of the 2nd Workshop on Multimodal Augmented Generation via Multimodal Retrieval (MAGMaR 2026, July 4, 2026; `https://aclanthology.org/2026.magmar-main.3/`). `[Verified]`
- **Paradigm & Findings:** 942 examples / 3,768 multimodal RAG instances derived from ChartQA (`500`) and MMMU (`442`) across factual, temporal, entity, and granularity conflicts (`Aligned`, `Image-correct`, `Text-correct`, `Both-wrong`; Secs. 1–3, pp. 1–4). Evaluates 4 open VLMs in **4-bit `mlx-vlm` quantization** (none Qwen2.5-VL) using an unvalidated `gpt-5-mini` judge `{IMAGE, TEXT, BOTH, NEITHER, ABSTAIN}` (Table 3, p. 5; p. 8). **No CoT forcing, no prefix forcing, no verdict extraction, and no order counterbalancing.** `[Verified]`
- **Thesis Relevance:** Cited in `PREREGISTRATION_VERDICT_TRANSPLANT.md` §1.1 & Ch. 2; scopes our novelty claim specifically to *prefix-forced verdict intervention + binding interaction*, not image–text ChartQA/MMMU conflict evaluation generally. `[Verified/Inferred]`

### 3.3 Chapter 2 Related-Work Leads (Post-v5 Audit)

#### Lead 1. Chains That See, Answers That Don't — Fan, Li & Zhuang (2026) | `[Local PDF: 2606.22862.pdf]`
- **Citation:** Zhichao Fan, Yanhang Li, Zexin Zhuang. *Chains That See, Answers That Don't: A Multi-Aspect Evaluation Recipe for Forced Chain-of-Thought on Video-MME*, EvalMG @ SIGIR 2026 (`arXiv:2606.22862v1`). `[Verified, pp. 1–2]`
- **Findings:** Evaluates prompt-instructed `>= 5`-step CoT (calling it *"forced CoT"*, App. F p. 9) on `Qwen2.5-VL-7B` (`bf16/fp16`, `n = 396`) and `32B` (`NF4 4-bit`, `n = 300`) with greedy decoding. Permissive regex fallbacks coerce `63/120` explicit video-swap refusals and flip `32B` `CoT - direct` sign (`-5.33 pp` raw strict vs. `+3.05 pp` all4 strict; Tables 1 & 5, pp. 4, 9). Evaluates a `±5 pp` post-hoc margin on `32B` (`90% CI`), **refusing to call it TOST** because no margin was pre-specified (`p. 4`). `[Verified]`
- **Thesis Relevance:** Does not use assistant-turn prefix-forcing or image–text conflict (§1.1 novelty intact); disambiguates *"prompt-forced CoT"* from *assistant-turn verdict prefix-forcing* and supports strict refusal/unparseable separation + pre-specified TOST margins. `[Verified/Inferred]`

#### Lead 2. Same Reasoning, Different Words — Smith (2026) | `[PDF Not Available — Abstract/CV Only]`
- **Citation:** Joe Smith (Caltech). *Same Reasoning, Different Words: Testing Linguistic Invariance in Chain-of-Thought Monitoring*, `TAE @ NeurIPS 2026`, OpenReview `uul4iRQSJ2` (`HTTP 403` blocked). `[Verified via open NeurIPS 2026 workshop page & author CV]`
- **Findings (verbatim abstract):** Rewrites completed `MMLU-Redux` traces (light paraphrase vs. syntactic/register change) *without resuming the policy* (fixed forced-answer trajectory) and checks an external soft CoT monitor. On `95` trajectories, aggregate disclosure shift passes a prespecified `±0.05` equivalence margin (`ΔD = -0.007`, `95% CI [-0.017, 0.003]`), **yet `20/95` (`21.1%`) item-level shifts exceed `±0.05`**. `[Verified via NeurIPS abstract]`
- **Thesis Relevance:** First related-work paper seen using an explicit TOST-like equivalence test on CoT text variation, but for *external monitor disclosure* over fixed traces—not *generative VLM source choice under conflict*, and with no `≤ 5.0%` item-level churn precedent. Supports reporting both aggregate TOST and item-level churn. `[Inferred]`

---

## 4. Cross-Paper Methodological Synthesis (Design Rules for Future Decisions)

1. **Pre-CoT Likelihood Margins ($\Delta\ell$) vs. Multi-Step Behavioural Rollouts (`2608.17205`, `2610.19407`, `2603.01437`, `2604.14888`):**
   - Teacher-forced $\Delta\ell$ at `#### ` works for direct extraction (ChartQA-Conflict), where text states the answer and no intermediate arithmetic is required.
   - In multi-step Math (GSM8K/SVAMP), pre-CoT $\Delta\ell$ measures zero-shot direct-answer preference (`2608.17205` p. 5) before computation happens (`2603.01437` Table 3: `Qwen2.5-3B` pre-CoT AUC drops to `0.690` on Logical Deduction). Thus **D1** (behavioural choice primary in Math, $\Delta\ell$ primary in exploratory ChartQA) is construct-mandatory.
2. **Prefix-Forcing vs. Re-Prompting vs. Steering (`2607.27304`, `2510.27484`, `2610.38296`, `2602.14518`):**
   - Prefix-forcing raised adoption over re-prompting (+39.8 / +4.9 pp); sycophancy and provenance effects were model-specific (MedGemma +9.0 pp under the deference instruction) (`2607.27304`, pp. 2, 7–9).
   - Because forced edits are off-policy (subject to resilience/ignoring in `2510.27484`), the estimand is strictly a **Controlled Direct Effect (CDE)**, never natural indirect mediation.
   - Binding vs. Non-binding separation: **binding** partly measures conditional instruction compliance, whereas **non-binding** carries the purer test of unprompted verdict faithfulness.
3. **Greedy `k=1` vs. Sampled Rollouts (`2510.27484`, `2307.13702`, `2609.25366`):**
   - Greedy decoding (`do_sample=False`) is reproducible and defines a clean deterministic-system estimand (`2607.27304`, `2503.02199`, `2609.25366` App. P).
   - Running Math behavioural generation on **only template `k=1`** limits cross-template generalization (`K=4` only covers $\Delta\ell$). Keep `k=1` greedy primary unless compute allows `k=2` or a `T=0.7` secondary stochastic check; declare both explicitly as limitations.
4. **Order Counterbalancing, Competency & Explicit Benchmarks (`2609.26986`, `2511.02243`, `2610.33841`):**
   - Never move $I$ with text; never couple Source A/B letters with position (`2609.26986`).
   - Dual single-source competency filtering is mandatory (`2511.02243` p. 5; `2609.26986` p. 4).
   - Explicit-source arms replicate Dassen et al.'s NL baseline (`2610.33841` Table 7) and show asymmetric control (image weaker than text); report both directions separately (`B_beh` as descriptive benchmark, not a ceiling).
5. **Paraphrase Churn, Binary Saturation & TOST (`2607.27304`, `2609.06704`, `2307.13702`, `2606.22862`, Smith 2026):**
   - Long (~400-token) Math CoTs amplify surface noise far beyond CoT-Mediate's `1.7–3.3%` short-answer floor (`15–23%` any-change churn on dev).
   - **No source tests TOST equivalence or a `≤ 5.0%` paraphrase-churn gate on generative VLM source choice under conflict** — both `ε = 5.0 pp` and `5.0%` remain `[Design decision]` rules. (`2606.22862` p. 4 checks a post-hoc `±5 pp` band without calling it TOST; Smith 2026 tests equivalence at `±0.05` on external CoT monitor disclosure over fixed traces, yet still finds `20/95` = `21.1%` item-level shifts above margin.)
   - Keep the fixed `5.0%` `image ↔ text` churn gate + `±10.0 pp` `neither` bound (plus reporting `any-change` churn) and the `para_flip − para` co-primary contrast (**D2**). A `6–8%` non-binding wording floor blocks `H0` equivalence in that arm, not a large positive `H1` shift.
6. **Directional Asymmetry (`2602.14518`, `2503.02199`, `2504.08974`):**
   - Keep `text→image` and `image→text` descriptive in v5; donor verdicts heavily skew toward typed text, underpowering directional tests.

---

## 5. Pre-Freeze Checklist Before Tagging `prereg-v5`

1. **[Done 2026-11-20] Human Coding (`Experiment/coding_v5/`):** Double-coded `200` verdict rows + `150` flip rows, adjudicated in `adjudication_v5.csv` with results in `evaluation_v5.json` (canonical verdict κ = `0.978`, parser `168/168` on 3B+7B and `199/200` overall; flip agreement `97.3%` / `99.3%`, AC1 `0.972` / `0.993`; prereg §8 revised and logged in §11).
2. **[Done 2026-11-15/16 & locked 2026-11-20] ChartQA `max_pixels` & GPU Checks (`Experiment/results_v5/`):** Completed fresh `34,920`-row L4 `bfloat16` rerun + R8.4 `px501k` (`501760`) comparison (`0` `boundary_mismatch`, `verdict_nll_tokens > 0` on all verdict rows) and locked ChartQA `max_pixels` at `200704` in `PREREGISTRATION_VERDICT_TRANSPLANT.md` §3.4 and `harness_v5.CONFIRM_MAX_PIXELS`.
3. **[Done 2026-11-20] Sync Pre-Registration Before Freeze:** §1.1, §3.4, §4, §8, §10–§11, Fable 5.2 fixes (`F2`, `F3`, `F5`–`F13`, `Upgrades 1–5`), and `lit-audit-2026-11-15` gap-closure sync (`1,452` records) are integrated (`255` CPU tests pass; `preflight_v5.py --phase confirm --allow_untagged` passes).
4. **[Frozen 2026-11-20 at `prereg-v5`]** Merged to `main` and tagged `prereg-v5`; next: run `--phase confirm` on GPU.

---

## 6. Pre-Freeze Literature Audit (2026-11-15 + 2026-11-17 Addendum) — pointer

**Full report:** [lit-audit-2026-11-15/lit-audit-2026-11-15.md](lit-audit-2026-11-15/lit-audit-2026-11-15.md). **Data:** `papers.csv` (`1,452` unique screened records, `0` duplicates), `search_log.csv` (`164` rows: `112` on 2026-11-15 + `52` in the 2026-11-17 gap-closure pass), `references.bib` (`47` entries: `6` A + `41` B). **Brief for new agents:** [../RESEARCH_OBJECTIVE.md](../RESEARCH_OBJECTIVE.md).

- **Novelty verdict:** intact, narrowed. Still only `2610.20805` meets the formal two-partial threat rule; the 2026-11-17 pass closed Row 69, Axis G second-tool coverage, OpenAlex hop-2 forward snowballing on the 6 A papers, and anchor-author checks, adding `0` new A papers and `8` new/upgraded B papers (`2610.00601`, `2608.24790`, `2507.02778` as single-component `(a)` partials; `2610.17989` and `2601.05201` as `(b)` partials; `2608.29464`, `10.18653/2026.emnlp-main.1113`, `10.18653/2026.findings-emnlp.1368`).
  - *When Reasoning Traces Conflict with Evidence* (arXiv:2610.20805, text-only) remains the only formal threat under the audit rule: partial on component (a), own-turn trace under conflict, and on component (c), an instruction contrast.
  - Manalu et al. (arXiv:2610.30953), Karnik et al. (arXiv:2610.00601), Xu et al. (arXiv:2608.24790), and Tsui (arXiv:2507.02778) are single-component precedents on (a).
  - §1.1 in `PREREGISTRATION_VERDICT_TRANSPLANT.md` is updated with the `1,452`-record scope and single-component precedents.
- **New A papers:** 2609.00550, 2610.30953, 2610.20805, 2609.29278, 2606.12747, 2610.37070. PDFs are in `Docs/Paper/` (bringing local PDFs to 26 on 2026-11-15; 29 total after adding the 3 cited B-paper PDFs listed in §0).
- **Correction to §4.2 of this file (applied above):** Replaced the overstatement that prefix-forcing "eliminates self-attribution discounting and external-authority sycophancy" (`2607.27304`) with the PDF-verified wording from audit §5 (sycophancy was model-specific: MedGemma +9.0 pp under the deference instruction, p. 2, and an authority gradient of −3.6 pp, p. 7).
- **Design implications (audit §4):**
  - keep order counterbalancing and add a per-order sign rule;
  - cite 2609.29278 for D1;
  - add a prefill-resistance limitation to the H₀ reading, with a descriptive `verdict_nll` stratification;
  - add a competency-population limitation;
  - state that the Math "image" channel is rendered text.

