## Discovery table (2025–2026 primary research)

| \# | Paper (year) | arXiv URL | Official pub / venue | GitHub / code | Dataset / benchmark | Exact task | Action / tool space | Tool selection studied? | Active perception studied? | Cost modeled? | Uncertainty modeled? | “When NOT to use a tool” evaluated? | Direct-answer / no-tool baseline? | Code \& data actually available? |
| :-- | :-- | :-- | :-- | :-- | :-- | :-- | :-- | :-- | :-- | :-- | :-- | :-- | :-- | :-- |
| 1 | **NTEP-R: Necessary Tool-Evidence Path Rewards** (2026) | [https://arxiv.org/abs/2609.03493](https://arxiv.org/abs/2609.03493) | arXiv preprint (Sep 2026) | Not yet linked in abstract (claims “will release”) | 7 image-grounded benchmarks (e.g., VQA-style) | Complex image-grounded QA requiring fine-grained visual evidence or external knowledge | 3 tools: image cropping, visual search, text retrieval | **Yes** – rewards align tool calls to necessary evidence paths; penalizes redundant calls | **Yes** – cropping/search to acquire missing visual evidence | **No** – no explicit monetary/compute cost model | **No** – no explicit uncertainty quantification | **Partially** – regularizer discourages redundant calls, but no explicit “abstain from tool” decision | Implicitly: direct-answer VLM baseline vs tool-augmented | Code/data promised but not yet confirmed in abstract |
| 2 | **SRICE: Seeing and Reasoning with Confidence** (2025) | [https://arxiv.org/abs/2503.08308](https://arxiv.org/abs/2503.08308) | arXiv preprint (Mar 2025) | Not explicitly linked | 5 VQA datasets | Training-free multimodal reasoning with external vision tools | External vision models + region selection (multi-stage) | **Yes** – selects optimal tool via uncertainty estimates | **Yes** – autonomously selects regions of interest | **No** – no cost model | **Yes** – conformal prediction-based UQ to calibrate tool outputs and select tools | **No** – focuses on selecting tools, not abstaining | Base MLLM (no-tool) used as baseline | Framework described; code not clearly linked in abstract |
| 3 | **CAM-DF: Cost-Aware Stopping for Tool Acquisition** (2026) | [https://arxiv.org/abs/2607.27083](https://arxiv.org/abs/2607.27083) | arXiv preprint (Jul 2026) | Not explicitly linked | τ-bench Retail + 4 other tool-use domains (1,343 tasks total) | Decide how many ranked tools to acquire before execution | Ranked tool prefixes (generic tool APIs) | **Yes** – learns how many tools to acquire from a ranked list | **No** – not visual; generic tool acquisition | **Yes** – heterogeneous cost regimes explicitly modeled | **No** – decision-focused stopping, not uncertainty-driven | **Yes** – core contribution is “when to stop acquiring tools” | Predict-then-threshold and full-access baselines | Code/data not explicitly linked in abstract |
| 4 | **Agentic Abstention** (2026) | [https://arxiv.org/abs/2606.28733](https://arxiv.org/abs/2606.28733) | arXiv preprint (Jun 2026) | [https://lhannnn.github.io/agentic-abstention](https://lhannnn.github.io/agentic-abstention) (project page; code/data promised) | WebShop, terminal environments, QA (28k+ tasks) | Decide when to stop acting and abstain under uncertainty | Search, browsing, terminal tools | **Partially** – studies tool-use trajectories, but focus is on abstention timing | **No** – not visual perception | **No** – no cost model | **Yes** – sequential decision under uncertainty | **Yes** – defines “agentic abstention” as when to stop instead of act | Multiple LLM-as-agent baselines; direct-answer scenarios included | Dataset \& code promised via project page |
| 5 | **ESearch-R1: Cost-Aware Embodied Search** (2025) | [https://arxiv.org/abs/2512.18571](https://arxiv.org/abs/2512.18571) | arXiv preprint (Dec 2025) | Not explicitly linked | AI2-THOR embodied search tasks | Ambiguous instructions in cluttered rooms; balance exploration vs human query | Ask, GetMemory, Navigate (embodied actions) | **Yes** – learns when to use each action type | **Yes** – active physical exploration for evidence | **Yes** – heterogeneous costs (navigation time, human attention) | **No** – cost-aware RL, not explicit uncertainty | **Partially** – learns to stop exploring and ask instead | ReAct-style agents as baseline | Code not explicitly linked in abstract |
| 6 | **OpenSearch-VL: Open Recipe for Multimodal Search Agents** (2026) | [https://arxiv.org/abs/2605.05185](https://arxiv.org/abs/2605.05185) | arXiv preprint (May 2026) | GitHub page promised | SearchVL-SFT-36k, SearchVL-RL-8k; 7 benchmarks | Deep search for knowledge-intensive visual questions | Text search, image search, OCR, cropping, sharpening, super-resolution, perspective correction | **Yes** – tool invocation learned via RL | **Yes** – active perception via cropping, sharpening, etc. | **No** – no explicit cost model | **No** – no explicit uncertainty | **Partially** – early stopping on failures or confidence, but not “no-tool” decision | Baselines include proprietary models; no explicit no-tool baseline | Code/data/models promised as “fully open-source” |
| 7 | **VTC-Bench: Visual Tool Chaining** (2026) | [https://arxiv.org/abs/2603.15030](https://arxiv.org/abs/2603.15030) | arXiv preprint (Mar 2026) | [https://github.com/zhuzil/vTC-Bench](https://github.com/zhuzil/vTC-Bench) | 680 curated problems, 9 cognitive categories | Compose multiple visual tools to solve complex image tasks | 32 OpenCV-based visual operations | **Yes** – evaluates tool selection/composition ability | **No** – tools are applied, but not active perception loop | **No** – no cost model | **No** – no uncertainty | **No** – focuses on chaining, not abstention | Not a training paper; benchmark only | Code \& benchmark publicly available |
| 8 | **VisualToolBench: Think-with-Images** (2025) | [https://arxiv.org/abs/2510.12712](https://arxiv.org/abs/2510.12712) | arXiv preprint (Oct 2025) | Not explicitly linked | 1,204 vision tasks (single + multi-turn), 5 domains | Active image manipulation (crop, edit, enhance) + reasoning | Image manipulation tools + general-purpose tools | **Yes** – evaluates ability to choose/use tools | **Yes** – “think with images” paradigm | **No** – no cost model | **No** – no uncertainty | **No** – no abstention evaluation | Implicitly: static VLM vs tool-enabled | Benchmark described; code not clearly linked |
| 9 | **MM-ToolSandBox** (2026) | [https://arxiv.org/abs/2607.11818](https://arxiv.org/abs/2607.11818) | arXiv preprint (Jul 2026) | Not explicitly linked | 500+ tools, 16 domains, multi-image multi-turn | Visually grounded tool-calling in stateful conversations | 500+ tools across apps (OCR, detection, segmentation, etc.) | **Yes** – benchmark for visual tool-calling capability | **Partially** – tools include perception ops, but not active loop | **No** – no cost model | **No** – no uncertainty | **No** – benchmark, not a stopping/abstention method | Benchmark only | Framework described; code/data status unclear |
| 10 | **CropVLM: Learning to Zoom** (2025) | [https://arxiv.org/abs/2511.19820](https://arxiv.org/abs/2511.19820) | arXiv preprint (Nov 2025); CVPR GRAIL-V Workshop 2026 | Not explicitly linked | Fine-grained VQA, scene-text, documents | Dynamically crop/zoom to relevant regions | Crop-and-zoom operator | **Partially** – learns when to crop, but not broader tool selection | **Yes** – active zooming for fine-grained perception | **No** – no cost model | **No** – no uncertainty | **No** – no abstention | Base VLM (no crop) as baseline | RL-trained; code not clearly linked |
| 11 | **OmniAgent: Active Perception for Audio-Video** (2025/2026) | [https://arxiv.org/abs/2512.23646](https://arxiv.org/abs/2512.23646) | arXiv preprint (Dec 2025, rev Feb 2026) | Not explicitly linked | 3 audio-video benchmarks | Dynamic orchestration of unimodal tools for omnimodal reasoning | Specialized audio/video tools, coarse-to-fine perception | **Yes** – dynamic tool orchestration | **Yes** – core contribution: active perception agent | **No** – no cost model | **No** – no explicit uncertainty | **No** – focuses on when to use tools, not when not to | SOTA open/closed models as baselines | Code not clearly linked |
| 12 | **MED: Disentangling Tool-Induced vs Intrinsic Effects** (2026) | [https://arxiv.org/abs/2602.01334](https://arxiv.org/abs/2602.01334) | arXiv preprint (Feb 2026); ICML 2026 | Code promised | 6 benchmarks, crop-and-zoom setting | Analyze what vision tool-use RL actually learns | Crop-and-zoom operator | **Partially** – analyzes tool-use RL, not selection policy | **Yes** – crop-and-zoom as active perception | **No** – no cost model | **No** – no uncertainty | **No** – diagnostic framework, not abstention | Base VLM vs tool-use RL | Code promised |

## Do these papers invalidate your apparent gaps?

Your candidate gaps:

1. **Predicting whether a tool call will improve an answer**
2. **Deciding whether additional visual information is necessary**
3. **Cost-aware tool selection**
4. **Uncertainty-aware tool routing**
5. **Stopping when sufficient evidence has been obtained**
6. **Counterfactual evaluation of tool usefulness**

Evidence-based assessment:

- **Gap 1 (tool utility prediction)**:
    - **NTEP-R** and **SRICE** move in this direction by rewarding/choosing tools that gather *necessary* evidence or reduce uncertainty, but they do not explicitly learn a standalone “will this tool improve the answer?” predictor.[^1_1][^1_2]
    - **CAM-DF** learns a stopping rule over ranked tools based on expected payoff, which is close to “is another tool worth it?”, but in a generic (non-visual) setting.[^1_3]
    - **Verdict**: Not invalidated. There is no clear, visual, undergraduate-feasible method that directly predicts per-call utility as a primary contribution.
- **Gap 2 (is more visual info necessary?)**:
    - **SRICE**, **OpenSearch-VL**, **OmniAgent**, and **CropVLM** all implement some form of active perception or region selection, implicitly deciding when more visual info is needed.[^1_2][^1_4][^1_5][^1_6]
    - However, they mostly learn *how* to acquire visual info, not a calibrated “necessary vs unnecessary” decision with a no-tool baseline explicitly evaluated as a research question.
    - **Verdict**: Partially addressed, but not in the narrow, decision-centric way you describe. Still a viable gap if framed as a calibrated necessity predictor.
- **Gap 3 (cost-aware tool selection)**:
    - **CAM-DF** explicitly models heterogeneous tool costs and learns when to stop acquiring tools.[^1_3]
    - **ESearch-R1** models heterogeneous costs (navigation time, human attention) in an embodied setting.[^1_7]
    - Both are non-visual or embodied-robotics focused, not lightweight multimodal QA on static images.
    - **Verdict**: Conceptually addressed in other domains, but not for undergraduate-feasible multimodal visual agents on Colab. Still open in your constraint regime.
- **Gap 4 (uncertainty-aware tool routing)**:
    - **SRICE** uses conformal prediction to calibrate tool outputs and select tools under uncertainty.[^1_2]
    - **Agentic Abstention** studies sequential decisions under uncertainty but not tool routing per se.[^1_8]
    - **Verdict**: Partially addressed, but SRICE is training-free and relatively high-level; a focused, reproducible uncertainty-aware router for visual tools could still be novel.
- **Gap 5 (stopping when sufficient evidence obtained)**:
    - **CAM-DF** and **Agentic Abstention** directly study stopping: CAM-DF for tool acquisition, Agentic Abstention for when to stop acting.[^1_8][^1_3]
    - **OpenSearch-VL** includes early stopping on confidence/failures.[^1_4]
    - **Verdict**: Strong prior work exists, especially in text/embodied settings. For *visual* tool-use with explicit “enough evidence” criteria and no-tool baselines, there is still room.
- **Gap 6 (counterfactual evaluation of tool usefulness)**:
    - **ToolAnchor** uses counterfactual anchor contexts to recover failed trajectories, but focuses on adapting to new tools, not evaluating per-call usefulness.[^1_9]
    - **IG-Search** uses a counterfactual baseline of random documents to measure information gain per search step (text-only).[^1_10]
    - **MED** analyzes tool-induced vs intrinsic effects but does not perform counterfactual “what if I hadn’t called this tool?” evaluation as a primary method.[^1_11]
    - **Verdict**: This is the least directly addressed in visual domains. A counterfactual tool-usefulness evaluator for visual agents is still underexplored.


## Top 5 papers to inspect in full

These are the most relevant for your audit and for shaping an undergraduate-feasible gap:

1. **NTEP-R (2026)** – [https://arxiv.org/abs/2609.03493](https://arxiv.org/abs/2609.03493)
    - Why: Directly supervises *necessary* tool-evidence paths; closest to “tool necessity” and “when not to call redundant tools.”[^1_1]
2. **SRICE (2025)** – [https://arxiv.org/abs/2503.08308](https://arxiv.org/abs/2503.08308)
    - Why: Uncertainty-aware, training-free framework that selects tools and regions using conformal prediction; key for uncertainty-aware routing.[^1_2]
3. **CAM-DF (2026)** – [https://arxiv.org/abs/2607.27083](https://arxiv.org/abs/2607.27083)
    - Why: Explicit cost-aware stopping for tool acquisition; strongest evidence that “cost-aware selection” is solvable in principle (though not visual).[^1_3]
4. **Agentic Abstention (2026)** – [https://arxiv.org/abs/2606.28733](https://arxiv.org/abs/2606.28733)
    - Why: Formalizes “when to stop acting” under uncertainty; directly relevant to “when NOT to use a tool” and stopping criteria.[^1_8]
5. **VisualToolBench (2025)** – [https://arxiv.org/abs/2510.12712](https://arxiv.org/abs/2510.12712)
    - Why: Defines the “think-with-images” paradigm and evaluates active image manipulation; essential for understanding current limits of visual tool use.[^1_12]

If you want, I can next:

- Pull the method sections from these 5 papers and extract exact baselines, metrics, and code links.
- Map each to your thesis constraints (Colab Pro, public data, simple baseline) and propose 2–3 narrowly scoped, undergraduate-feasible research questions that survive this literature.

<span style="display:none">[^1_13][^1_14][^1_15][^1_16][^1_17][^1_18][^1_19][^1_20][^1_21][^1_22][^1_23][^1_24][^1_25][^1_26][^1_27][^1_28][^1_29][^1_30][^1_31][^1_32][^1_33][^1_34][^1_35][^1_36][^1_37][^1_38][^1_39][^1_40][^1_41][^1_42][^1_43][^1_44][^1_45][^1_46][^1_47][^1_48][^1_49][^1_50][^1_51][^1_52][^1_53][^1_54][^1_55][^1_56][^1_57][^1_58][^1_59][^1_60][^1_61][^1_62][^1_63][^1_64][^1_65][^1_66][^1_67][^1_68][^1_69][^1_70][^1_71][^1_72][^1_73][^1_74][^1_75][^1_76][^1_77][^1_78][^1_79][^1_80][^1_81][^1_82][^1_83][^1_84][^1_85][^1_86][^1_87][^1_88][^1_89][^1_90][^1_91][^1_92][^1_93]</span>

<div align="center">⁂</div>

[^1_1]: https://arxiv.org/html/2609.03493v1

[^1_2]: https://arxiv.org/abs/2503.08308

[^1_3]: https://arxiv.org/abs/2607.27083

[^1_4]: https://arxiv.org/abs/2605.05185

[^1_5]: https://arxiv.org/abs/2512.23646v2

[^1_6]: https://arxiv.org/abs/2511.19820

[^1_7]: https://web3.arxiv.org/abs/2512.18571

[^1_8]: https://arxiv.org/abs/2606.28733

[^1_9]: https://arxiv.org/abs/2607.14145

[^1_10]: http://lonepatient.top/2026/04/17/arxiv_papers_2026-04-17

[^1_11]: https://arxiv.org/abs/2602.01334v2

[^1_12]: https://arxiv.org/abs/2510.12712

[^1_13]: https://arxiv.org/abs/2511.05271

[^1_14]: https://arxiv.org/abs/2207.05195

[^1_15]: https://arxiv.org/abs/2310.01331

[^1_16]: https://arxiv.org/html/2605.28192v1

[^1_17]: https://arxiv.org/abs/2503.06745

[^1_18]: https://arxiv.org/abs/2511.14210

[^1_19]: https://arxiv.org/html/2501.11733v2

[^1_20]: https://arxiv.org/abs/2512.23646

[^1_21]: https://arxiv.org/html/2410.07553v2

[^1_22]: https://arxiv.org/html/2606.31504v1

[^1_23]: https://arxiv.org/html/2410.14141

[^1_24]: https://arxiv.org/html/2607.11818v1

[^1_25]: https://arxiv.org/html/2410.02052

[^1_26]: https://arxiv.org/abs/2502.13130

[^1_27]: https://arxiv.org/abs/2510.08567

[^1_28]: https://huggingface.co/papers/2603.15030

[^1_29]: https://www.alphaxiv.org/abs/2602.23166

[^1_30]: https://cvpr.thecvf.com/virtual/2025/poster/32755

[^1_31]: https://arxiv.org/html/2501.02977v1

[^1_32]: https://arxiv.org/abs/2503.08308v1

[^1_33]: https://arxiv.org/abs/2411.02937

[^1_34]: https://arxiv.org/list/cs.AI/2025?skip=6250\&show=2000

[^1_35]: https://arxiv.org/abs/2410.21794

[^1_36]: https://arxiv.org/abs/2511.02734

[^1_37]: https://arxiv.org/abs/2502.11514

[^1_38]: https://arxiv.org/abs/2608.17084

[^1_39]: https://arxiv.org/abs/2405.09369

[^1_40]: https://arxiv.org/abs/2501.01277

[^1_41]: https://arxiv.org/abs/2609.04574

[^1_42]: https://arxiv.org/html/2503.06832v1

[^1_43]: https://arxiv.org/html/2604.06376v1

[^1_44]: https://arxiv.org/abs/2603.21426

[^1_45]: https://openreview.net/forum?id=cuUsD5FJbe

[^1_46]: https://arxiv.org/abs/2502.09780v1

[^1_47]: https://web3.arxiv.org/abs/2510.25612

[^1_48]: https://arxiv.org/abs/2502.15902

[^1_49]: https://arxiv.org/html/2606.08275v1

[^1_50]: https://arxiv.org/abs/2408.01536

[^1_51]: https://arxiv.org/html/2606.22737v1

[^1_52]: https://arxiv.org/abs/2503.09335

[^1_53]: https://arxiv.org/abs/2506.02946

[^1_54]: http://arxiv.org/abs/2504.07103

[^1_55]: https://arxiv.org/html/2603.06859v1

[^1_56]: https://arxiv.org/abs/2410.16441

[^1_57]: https://arxiv.org/html/2609.07255v1

[^1_58]: https://arxiv.org/abs/2501.15988

[^1_59]: https://www.alphaxiv.org/abs/2607.01874

[^1_60]: https://arxiv.org/abs/2501.11107

[^1_61]: https://arxiv.org/abs/2408.01999

[^1_62]: https://commonplace.workforcefutures.net/paper/arxiv:2605.01604

[^1_63]: https://www.curvelabs.org/research-backed-self-improvement-for-autonomous-ai-agents/2026-03-28-1501/counterfactual-emotional-branching-for-socially-reliable-autonomous-agents

[^1_64]: https://arxiv.org/abs/2609.03493

[^1_65]: https://arxiv.org/abs/2512.18571

[^1_66]: https://cvpr.thecvf.com/virtual/2026/poster/37958

[^1_67]: https://arxiv.org/abs/2412.10342

[^1_68]: https://arxiv.org/abs/2404.08449

[^1_69]: https://arxiv.org/format/2504.02762v1

[^1_70]: https://web3.arxiv.org/abs/2512.03687

[^1_71]: https://arxiv.org/format/2504.03628

[^1_72]: https://arxiv.org/format/2504.03536

[^1_73]: https://arxiv.org/format/2504.02061

[^1_74]: https://arxiv.org/html/2602.24134v1

[^1_75]: https://github.com/Nanboy-Ronan/awesome-medical-imaging-agents

[^1_76]: https://huggingface.co/papers/2511.17729

[^1_77]: https://www.niebles.net/blog/2026/cvpr-talks/

[^1_78]: https://www.alphaxiv.org/abs/2607.11818

[^1_79]: https://www.swiftscholar.net/paper/69bddf9e5f5672497d09f018

[^1_80]: https://www.alphaxiv.org/abs/2510.12712

[^1_81]: https://arxiv.org/abs/2602.01334

[^1_82]: https://arxiv.org/abs/2603.15030

[^1_83]: https://papers.cool/arxiv/2608.03979

[^1_84]: https://www.alphaxiv.org/abs/2511.08798

[^1_85]: https://www.alphaxiv.org/abs/2604.12890v1

[^1_86]: https://github.com/MilkThink-Lab/Awesome-Routing-LLMs

[^1_87]: https://arxivsignals.io/papers/2607.10599

[^1_88]: https://www.alphaxiv.org/abs/2604.21375

[^1_89]: https://alopatenko.github.io/LLMEvaluation/

[^1_90]: https://www.alphaxiv.org/abs/2604.04035

[^1_91]: https://prismix.dev/news/2d25bf62fac8

[^1_92]: https://www.alphaxiv.org/abs/2605.11946

[^1_93]: https://agentvista-bench.github.io/


---

```
# \<q>Pull the method sections from these 5 papers and extract exact baselines, metrics, and code links.\</q> @Academic
```

Here are the extracted method details, baselines, metrics, and code/data links for the 5 priority papers.

## 1) SRICE (2025) — Seeing and Reasoning with Confidence

**Method (core):** Training-free, two-stage agentic framework that (i) calls external vision tools (segmentation + object detection), calibrates their outputs via conformal prediction (CP), and lets the MLLM select regions of interest (RoI); then (ii) feeds original image + RoI to the MLLM for CoT reasoning and selects the best pathway using an uncertainty score based on top‑p coverage (quasi‑conformal).[^2_1][^2_2]

**Baselines:**

- Base: LLaVA-OneVision-Qwen2-7B (LLaVA-ov-7B)
- LLaVA-1.5-13B
- Visual CoT (VisCoT) fine-tuned on LLaVA-ov-7B (upper bound) and vicuna-7B-VisCoT
- SPHINX-13B[^2_2]

**Metrics:** Accuracy on five VQA/reasoning datasets (VQA2, VizWiz, GQA, Flickr30K, MMBench); ablations report average accuracy and ECE for reliability.[^2_2]

**Code / data:**

- Tools: SEEM (segmentation) and YOLOv11 (detection); COCO-2017 val used for CP calibration.
- The paper states the framework and calibration procedure in detail but does not provide an explicit GitHub link in the abstract/method; implementation relies on public models (SEEM, YOLOv11) and standard datasets.[^2_2]

______________________________________________________________________

## 2) CAM-DF (2026) — Cost-Aware Stopping for Tool Acquisition

**Method (core):** Pre-execution stopping policy over ranked tool prefixes. Trains a logistic classifier on the *payoff gap* between stopping now vs best continuation (sign = label, magnitude = regret weight). Uses scores, heterogeneous costs, and prefix-progress features; stops at first predicted “stop” along the ranking. CAM-DF-lite is a compact, interpretable variant with 10 theory-motivated features.[^2_3][^2_4]

**Baselines:**

- Tuned fixed‑k (common depth)
- Score threshold
- Score-per-cost threshold
- Retail rule (hand-written keyword mapping + threshold)
- Predict-then-threshold (predict sufficiency, stop above threshold)
- Aggregate-only DF (no next-tool features)
- Prefix oracle (non-deployable upper bound)[^2_4]

**Metrics:** Mean payoff $U(A,x)=\text{sufficiency}(A,x)-\lambda\sum c_j$, sufficiency rate, acquisition cost; 95% paired-bootstrap CIs over 2,000 resamples; live evaluation reports task success and tool exposure.[^2_4]

**Code / data:**

- Datasets: τ-bench Retail (67 tasks), MCP-Atlas (495), WorkBench (639), τ²-bench Airline (28), τ²-bench Telecom (114).
- Rankings from frozen LLM scorers (e.g., qwen-plus).
- The paper describes a modular pre-execution plugin but does not include a GitHub link in the main text; datasets are from public benchmarks (τ-bench family, MCP-Atlas, WorkBench).[^2_4]

______________________________________________________________________

## 3) Agentic Abstention (2026)

**Method (core):** Defines *agentic abstention* as a sequential decision (ANSWER / ABSTAIN / ACT) under partial observability. Evaluates timely vs overall abstention recall (AbsRec@K) across web shopping (WebShop), terminal (Terminal-Bench 2.0), and interactive QA (AbstentionBench subset with local Wikipedia retrieval). Proposes CONVOLVE, a context-engineering method that distills full trajectories into a reusable “playbook” of stopping rules appended to agent context.[^2_5][^2_6]

**Baselines:** 13 LLM-as-agent systems (GPT-5.4-mini, Llama-3.3-{8B,70B}, Qwen3-{8B,14B,32B,235B}, etc.) and 2 scaffolds (Terminus 2, Codex CLI); in-web comparisons include base model vs base + in-context learning vs base + CONVOLVE.[^2_6]

**Metrics:**

- AbsRec@K (Abstention Recall at K steps after abstention becomes warranted), with *Timely Recall* = AbsRec@1 (or @2 for environment-based cases).
- SPL (Success weighted by normalized inverse path length) to penalize delayed abstention.
- Over-abstention rate on solvable tasks.[^2_6]

**Code / data:**

- Project page and dataset/code release: [https://lhannnn.github.io/agentic-abstention](https://lhannnn.github.io/agentic-abstention)
- Hugging Face dataset mirrors: antiquality/agentabstain and novastarlabs/agentabstain-ar (263 paired tasks across 42 MCP sandboxes).[^2_7][^2_8][^2_9][^2_6]

______________________________________________________________________

## 4) VisualToolBench (2025) — “Beyond Seeing”

**Method (core):** Benchmark (not a training method) for the *think-with-images* paradigm: MLLMs must actively manipulate images (crop, edit, enhance) and combine with general-purpose tools to solve 1,204 open-ended tasks (single- and multi-turn) across five domains, with detailed rubrics for systematic evaluation.[^2_10][^2_11]

**Baselines:** Multiple frontier MLLMs (e.g., GPT-5-think, Gemini-2.5-pro, etc.) evaluated under the benchmark’s rubric; reports pass rates and tool-use behavior patterns.[^2_10]

**Metrics:** Pass rate per task under rubric-based evaluation; analysis of tool-use diversity and effectiveness.[^2_10]

**Code / data:**

- Benchmark hosted by Scale Labs; leaderboard and description at [https://labs.scale.com/leaderboard/vtb](https://labs.scale.com/leaderboard/vtb)
- Paper states the benchmark comprises 1,204 tasks with rubrics; code/data availability is via the Scale Labs page (no explicit GitHub link in the abstract).[^2_11][^2_10]

______________________________________________________________________

## 5) NTEP-R (2026) — Necessary Tool-Evidence Path Rewards

**Method (core):** Introduces NTEP annotations that specify the *necessary external evidence* and corresponding tool calls per query. NTEP-R rewards (i) alignment of pre-call intent with a necessary evidence-seeking goal and (ii) alignment of post-call observation summaries with the necessary evidence, plus a non-repeated-goal regularizer to penalize redundant calls. Evaluated with a unified three-tool framework (image crop, image search, text search) on seven image-grounded benchmarks.[^2_12][^2_13]

**Baselines:** Standard tool-use RL / SFT baselines trained only on final answer correctness (no explicit NTEP supervision); comparisons include models without the non-repeated-goal regularizer and without intent/observation alignment rewards.[^2_13]

**Metrics:** Search-oriented accuracy and tool-use efficiency (e.g., redundant call rate, evidence coverage) across seven benchmarks; reports gains for an 8B-parameter instantiation (NTEP-8B).[^2_13]

**Code / data:**

- Paper describes the annotation scheme and reward design; as of the preprint, code/data links are not provided in the abstract (claims “will release” / “publicly available” in some sections).[^2_13]

______________________________________________________________________

## Implications for your undergraduate-feasible gap audit

- **Strongest direct challenges to your gaps:**
    - **CAM-DF** invalidates “cost-aware stopping” as a *novel idea* in general tool-use (but not in *visual* multimodal QA on Colab).[^2_3][^2_4]
    - **Agentic Abstention** and **AgentAbstain** invalidate “when NOT to act” as a *new problem statement* in general agents, but not yet in lightweight, visual, reproducible settings with explicit no-tool baselines.[^2_5][^2_7][^2_6]
    - **SRICE** partially addresses “uncertainty-aware tool routing” and “is more visual info necessary?” but in a training-free, two-tool (seg/det) VQA setup, not a broader visual-tool space.[^2_1][^2_2]
    - **NTEP-R** and **VisualToolBench** show active work on *necessary evidence* and *think-with-images*, but do not provide a calibrated “tool-utility predictor” or counterfactual usefulness evaluator as a primary contribution.[^2_12][^2_10][^2_13]
- **Remaining undergraduate-feasible niches** (if scoped tightly):
    - A **visual tool-utility predictor** that, given a question + image + candidate tool (e.g., crop, OCR, enhance), predicts the expected accuracy gain vs a direct-answer baseline, trained on a small subset of VisualToolBench or a curated VQA set.
    - A **cost-aware visual stopping rule** that adapts CAM-DF’s payoff-gap objective to *visual* tool prefixes (e.g., crop→OCR→search) with heterogeneous simulated costs (API calls, runtime) and evaluates “when NOT to call the next visual tool.”
    - A **counterfactual tool-usefulness evaluator** that estimates “would the answer change if this tool call were removed?” using trajectory perturbation on a small benchmark, explicitly comparing to a no-tool baseline.

If you want, I can next map these to concrete datasets you can run on Colab Pro, propose a minimal baseline stack, and draft 2–3 narrowly scoped research questions that survive this literature.

<span style="display:none">[^2_14][^2_15][^2_16][^2_17][^2_18][^2_19][^2_20][^2_21][^2_22][^2_23][^2_24][^2_25][^2_26][^2_27][^2_28][^2_29][^2_30]</span>

<div align="center">⁂</div>

[^2_1]: https://arxiv.org/abs/2503.08308

[^2_2]: https://arxiv.org/pdf/2503.08308.pdf

[^2_3]: https://arxiv.org/abs/2607.27083

[^2_4]: https://arxiv.org/pdf/2607.27083.pdf

[^2_5]: https://arxiv.org/abs/2606.28733

[^2_6]: https://arxiv.org/pdf/2606.28733.pdf

[^2_7]: https://arxiv.org/abs/2607.10059

[^2_8]: https://huggingface.co/datasets/antiquality/agentabstain

[^2_9]: https://huggingface.co/datasets/novastarlabs/agentabstain-ar

[^2_10]: https://arxiv.org/abs/2510.12712

[^2_11]: https://labs.scale.com/leaderboard/vtb

[^2_12]: https://arxiv.org/html/2609.03493v1

[^2_13]: https://arxiv.org/html/2504.03748v1

[^2_14]: https://arxiv.org/html/2409.12953v4

[^2_15]: https://arxiv.org/html/2607.11818v2

[^2_16]: https://arxiv.org/html/2502.09696v2

[^2_17]: https://arxiv.org/html/2502.08779v1

[^2_18]: https://arxiv.org/abs/2406.11775

[^2_19]: https://arxiv.org/html/2310.10207v4

[^2_20]: https://arxiv.org/abs/2407.00902

[^2_21]: https://www.alphaxiv.org/abs/2603.12056

[^2_22]: https://www.alphaxiv.org/audio/2603.12056

[^2_23]: https://pmc.ncbi.nlm.nih.gov/articles/PMC11957224/

[^2_24]: https://arxiv.org/abs/2609.03493

[^2_25]: https://huggingface.co/papers/2603.15030

[^2_26]: https://www.opentrain.ai/papers/agentic-abstention-do-agents-know-when-to-stop-instead-of-act--arxiv-2606.28733/

[^2_27]: https://arxivday.com/articles?date=2025-10-24

[^2_28]: https://ai-news-bot-henna.vercel.app/news/2026/06/2026-06-30/

[^2_29]: https://www.alphaxiv.org/abs/2602.23166

[^2_30]: https://www.linkedin.com/posts/anthony-alcaraz-b80763155_knowing-when-to-stop-is-the-agent-eval-dimension-activity-7478699308414955520-gW4C

