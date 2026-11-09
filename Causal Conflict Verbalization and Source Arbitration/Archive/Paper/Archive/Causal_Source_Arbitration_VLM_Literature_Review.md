# **Causal Source Arbitration under Cross-Modal** **Conflict in Vision-Language Models**

30+ Paper Literature Review for Thesis Team

**Primary model:** Qwen/Qwen2.5-VL-3B-Instruct

**Primary dataset:** vlm-modality-research/modality-conflict-arbitration-v2

**Working protocol:** 4-arm factorial design with length-matched placebo and source/conflict prefilling

## **Purpose**

This document is a team reading pack. Its purpose is to identify what has already been established about multimodal conflict, modality preference, source monitoring, chain-of-thought faithfulness and inference-time intervention, then isolate the remaining research space for the proposed thesis. It is deliberately organized around **dataset, method, limitations and future work** so that the team can read papers with the gap in mind.

**Important:** “Limitations” and “Future work” are summarized from the paper when explicitly stated. Where a paper does not provide a directly matching future-work statement, the entry is marked as an interpretive research note rather than presented as an author claim.

Causal Source Arbitration — Team Literature Review Page 1

## **1. Executive Research Summary**

**Current evidence:** recent work has established that VLMs can prefer one modality over another under conflict, that the preference changes with task and evidence structure, that conflict detection and resolution can be distinct processes, and that multimodal reasoning traces can be unfaithful. Therefore, a thesis that merely asks whether a model prefers image or text—or whether a prompt saying "analyze the conflict" improves accuracy—would have limited novelty.

**Candidate gap:** test whether an explicitly represented _conflict/source state_ has a causal effect on the subsequent arbitration decision after controlling for generic extra reasoning/token budget. The strongest version adds a counterfactual source-attribution intervention while keeping the underlying image/text evidence fixed.

**Key warning:** this literature review does not establish that the proposed thesis is publication-safe by itself. Before freezing the protocol, the team should inspect the exact intervention sections, appendices and released code of the closest 2025–2026 papers, especially Mixed Signals, Which Source Wins?, Source-Modality Monitoring, Challenges in Understanding Modality
Conflict, and the recent multimodal faithfulness papers.
## **2. Highest-Priority Reading Order**

|Priority|Paper|Why read it first|
|---|---|---|
|1|Which Source Wins? (2026)|Closest conflict-arbitration benchmark; dataset construction, degradation, CLL<br>metric, limitations.|
|2|Mixed Signals (2025)|Direct overlap with conflict prompts and task decomposition; novelty threat.|
|3|Source-Modality Monitoring (2026)|Closest source-identity concept and monitoring/intervention direction.|
|4|Challenges in Modality Conflict (2025)|Separates conflict detection from conflict resolution; mechanistic framing.|
|5|Words or Vision (CVPR 2025)|Strong evidence of modality bias and prompt/token-order confounds.|
|6|A Closer Look at CoT Faithfulness (2025)|Direct warning that generated rationales may not reveal influential cues.|
|7|Lanham et al. (2023)|Foundational rationale intervention / faithfulness methodology.|
|8|On the Faithfulness of Visual Thinking (2025)|Multimodal intervention methodology.|
|9|SPD-Faith Bench (2026)|Latest multimodal reasoning-faithfulness benchmark.|
|10|Faithful-First RPA (2026)|Recent inference-time faithfulness control.|
|11|VG-CoT (2026)|Grounded reasoning/evidence alignment.|
|12|Qwen2.5-VL Technical Report|Primary model background.|

Causal Source Arbitration — Team Literature Review Page 2

**1. Which Source Wins? Task-Dependent Reliance in Vision-Language Models**

Ghosh, Gupta & Wang (2026), arXiv:2608.17205

**Paper / PDF:** [https://arxiv.org/pdf/2608.17205](https://arxiv.org/pdf/2608.17205)

**Dataset / evaluation:** Controlled image-text conflicts from GSM8K/SVAMP; ChartQA-Conflict (229 chart-report conflicts);
matched chart/table representations.

**What the paper does:** Conflict-source arbitration under controlled degradation; generated answers and length-normalized conditional log-likelihood.

**Limitations:** Conflict construction is centered on attributable numeric answers; open-weight coverage is 2B–8B; arithmetic and chart settings differ in several factors, so one causal mechanism cannot be isolated.

**Future work:** Extend attribution to free-form, categorical and multiple-choice outputs; broaden model/task coverage;
disentangle task, representation and conflict-construction effects.

**Relevance to our thesis:** Closest baseline. It establishes that modality reliance is task/evidence dependent, so our contribution must be intervention/causal rather than another preference benchmark.

**2. Mixed Signals: Decoding VLMs' Reasoning and Underlying Bias in Vision-Language Conflict**

Pezeshkpour, Aminnaseri & Hruschka (EMNLP Findings 2025)

**Paper / PDF:** [https://aclanthology.org/2025.findings-emnlp.1351.pdf](https://aclanthology.org/2025.findings-emnlp.1351.pdf)

**Dataset / evaluation:** Five mismatched image-text datasets spanning mathematics, science and visual descriptions, built from existing benchmarks.

**What the paper does:** Measures text/image preference and tests prompt modifications, explicit conflict-handling instructions and task decomposition.

**Limitations:** Effectiveness of mitigation strategies varies substantially with task/model/modality; prompt interventions are not uniformly reliable.

**Future work:** Explore deeper mechanisms of modality bias and more robust conflict-resolution strategies across tasks.

**Relevance to our thesis:** Critical overlap: explicit conflict instructions already exist, so 'conflict verbalization' alone is not sufficient novelty.

**3. Source-Modality Monitoring in Vision-Language Models**

Hua, Yun & Pavlick (2026), arXiv:2604.22038

**Paper / PDF:** [https://arxiv.org/pdf/2604.22038](https://arxiv.org/pdf/2604.22038)

**Dataset / evaluation:** Target-modality information-retrieval tasks spanning 11 VLMs; source-monitoring probes and prompt manipulations.

**What the paper does:** Tests whether models track which input modality supplied information; studies syntactic vs semantic source cues.

**Limitations:** Source tracking is imperfect and depends on distributional distinctiveness; monitoring is not the same as arbitration under conflict.

**Future work:** Study source monitoring in richer multimodal reasoning, conflict settings and interventions; examine robustness implications.

**Relevance to our thesis:** Highly relevant conceptual bridge: source identity can be treated as an explicit variable in our arbitration experiment.

**4. Challenges in Understanding Modality Conflict in Vision-Language Models**

Nguyen, Michaels, Fiterau & Jensen (2025), arXiv:2509.02805

**Paper / PDF:** [https://arxiv.org/pdf/2509.02805](https://arxiv.org/pdf/2509.02805)

**Dataset / evaluation:** Synthetic 5,600-sample shape/color image-caption conflict dataset; LLaVA-OV-7B.

**What the paper does:** Separates conflict detection from conflict resolution using linear probes and attention-pattern analysis.

**Limitations:** Scope focuses on direct task-relevant conflict; synthetic shapes/colors simplify real-world conflict; mechanistic interpretation is limited by the studied model.

Causal Source Arbitration — Team Literature Review Page 3

**Future work:** Expand to task-irrelevant and indirect conflict; develop targeted interventions using the detection/resolution decomposition.

**Relevance to our thesis:** Important for framing: detection and resolution should not be treated as the same phenomenon.

Causal Source Arbitration — Team Literature Review Page 4

**5. Words or Vision: Do Vision-Language Models Have Blind Faith in Text?**

Deng, Cao, Chen & Hooi (CVPR 2025)

**Paper / PDF:** [https://openaccess.thecvf.com/content/CVPR2025/papers/Deng_Words_or_Vision_Do_Vision-Language_Models_Have_Blind_Fa](https://openaccess.thecvf.com/content/CVPR2025/papers/Deng_Words_or_Vision_Do_Vision-Language_Models_Have_Blind_Faith_in_Text_CVPR_2025_paper.pdf)
[ith_in_Text_CVPR_2025_paper.pdf](https://openaccess.thecvf.com/content/CVPR2025/papers/Deng_Words_or_Vision_Do_Vision-Language_Models_Have_Blind_Faith_in_Text_CVPR_2025_paper.pdf)

**Dataset / evaluation:** Four vision-centric tasks with controlled textual variations; 10 VLMs.

**What the paper does:** Measures modality preference under inconsistencies and studies prompt, model size, relevance, token order and modality certainty.

**Limitations:** Text bias depends on prompt and input factors; supervised text augmentation is explored but does not establish causal inference-time arbitration.

**Future work:** Study broader training distributions and modality balancing; develop robust methods that reduce harmful modality bias.

**Relevance to our thesis:** Establishes modality preference and positional effects; our study needs to control prompt/token confounds.

**6. A Closer Look at Bias and Chain-of-Thought Faithfulness of Large (Vision) Language Models**

Balasubramanian, Basu & Feizi (EMNLP Findings 2025)

**Paper / PDF:** [https://aclanthology.org/2025.findings-emnlp.723.pdf](https://aclanthology.org/2025.findings-emnlp.723.pdf)

**Dataset / evaluation:** Paired biased/unbiased multimodal examples across LVLM tasks; fine-grained CoT bias-articulation evaluation.

**What the paper does:** Studies whether reasoning traces faithfully articulate text-based and image-based biases.

**Limitations:** Subtle image biases are rarely articulated; models can show inconsistent reasoning, indicating that verbalized rationale may not reflect the influential cue.

**Future work:** Extend faithfulness tests to more modalities, tasks and causal interventions.

**Relevance to our thesis:** Directly motivates testing whether a verbalized conflict is causally used rather than merely generated after a decision.

**7. On the Faithfulness of Visual Thinking: Measurement and Enhancement**

Liu, Pan, She, Gao & Xia (2025), arXiv:2510.23482

**Paper / PDF:** [https://arxiv.org/pdf/2510.23482](https://arxiv.org/pdf/2510.23482)

**Dataset / evaluation:** Fine-grained perception/reasoning benchmarks for multimodal chain-of-thought; intervention-based faithfulness evaluation.

**What the paper does:** Intervenes on visual and textual thoughts and measures prediction changes; proposes SCCM.

**Limitations:** Visual reasoning traces can be inaccurate even when final answers are correct; visual interventions may have weak effect relative to textual intervention.

**Future work:** Improve visual thought sufficiency/reliability and evaluate faithfulness across more reasoning models and tasks.

**Relevance to our thesis:** Strong methodological precedent for intervention-based evaluation; our intervention target is source arbitration under conflict.

**8. SPD-Faith Bench: Diagnosing and Improving Faithfulness in CoT for MLLMs**

Lv et al. (ACL Findings 2026)

**Paper / PDF:** [https://aclanthology.org/2026.findings-acl.995.pdf](https://aclanthology.org/2026.findings-acl.995.pdf)

**Dataset / evaluation:** SPD-Faith Bench: fine-grained image-difference reasoning benchmark.

**What the paper does:** Evaluates reasoning-level faithfulness and identifies perceptual blindness and perception-reasoning dissociation; proposes SAGE.

**Limitations:** Focuses on visual-difference reasoning rather than explicit cross-modal source conflict; benchmark is specialized.

**Future work:** Broaden faithfulness diagnostics beyond image-difference tasks and study more causal routing interventions.

**Relevance to our thesis:** Important recent faithfulness benchmark; supports evaluating more than final-answer accuracy.

Causal Source Arbitration — Team Literature Review Page 5

**9. Faithful-First Reasoning, Planning, and Acting for Multimodal LLMs**

Li, Xu, Ma, Zhang & Li (ACL Findings 2026)

**Paper / PDF:** [https://aclanthology.org/2026.findings-acl.336.pdf](https://aclanthology.org/2026.findings-acl.336.pdf)

**Dataset / evaluation:** Multiple multimodal reasoning benchmarks.

**What the paper does:** FaithEvi evaluates step/chain faithfulness and FaithAct uses these signals for inference-time planning/acting.

**Limitations:** Framework is broader than conflict arbitration and emphasizes faithfulness-aware reasoning/acting rather than source attribution.

**Future work:** Investigate faithful inference in additional multimodal settings and mechanisms.

**Relevance to our thesis:** Shows that faithfulness can be an inference-time control signal; our work asks whether source/conflict state causally controls arbitration.

**10. Measuring Faithfulness in Chain-of-Thought Reasoning**

Lanham et al. (2023), arXiv:2307.13702

**Paper / PDF:** [https://arxiv.org/pdf/2307.13702](https://arxiv.org/pdf/2307.13702)

**Dataset / evaluation:** Language-only reasoning tasks with controlled CoT interventions.

**What the paper does:** Intervenes on CoT by adding mistakes/paraphrases and measures downstream prediction changes.

**Limitations:** Results vary strongly by task/model; language-only setting does not address multimodal source conflict.

**Future work:** Extend causal faithfulness methodology to multimodal reasoning and more model/task families.

**Relevance to our thesis:** Foundational rationale-intervention method behind the proposed prefilling/causal-control logic.

**11. Measuring and Improving Chain-of-Thought Reasoning in Vision-Language Models**

Chen et al. (NAACL 2024)

**Paper / PDF:** [https://aclanthology.org/2024.naacl-long.11.pdf](https://aclanthology.org/2024.naacl-long.11.pdf)

**Dataset / evaluation:** Benchmark/dataset with detailed multimodal reasoning chains created through an LLM-human-in-the-loop pipeline.

**What the paper does:** Measures reasoning consistency/grounding and proposes a CoT-based consistency measure.

**Limitations:** High-quality reasoning-chain annotation is costly; consistency is not identical to causal faithfulness.

**Future work:** Scale grounded reasoning evaluation and improve consistency/faithfulness across VLMs.

**Relevance to our thesis:** Useful for separating correct answers from trustworthy reasoning.

**12. VG-CoT: Towards Trustworthy Visual Reasoning via Grounded Chain-of-Thought**

Lim, Kim, Yun & Kim (2026)

**Paper / PDF:** [https://arxiv.org/pdf/2604.21396](https://arxiv.org/pdf/2604.21396)

**Dataset / evaluation:** VG-CoT dataset linking reasoning steps to image regions using an automated pipeline.

**What the paper does:** Grounds each reasoning step in visual evidence and evaluates visual grounding of reasoning.

**Limitations:** Automated grounding can inherit detector/OCR/LLM errors; focus is evidence grounding rather than cross-modal arbitration.

**Future work:** Improve scalable grounding quality and evaluate broader multimodal reasoning tasks.

**Relevance to our thesis:** Supports explicit evidence/source grounding as a reliability dimension.

Causal Source Arbitration — Team Literature Review Page 6

**13. Qwen2.5-VL Technical Report**

Bai et al. (2025), arXiv:2502.13923

**Paper / PDF:** [https://arxiv.org/pdf/2502.13923](https://arxiv.org/pdf/2502.13923)

**Dataset / evaluation:** Large-scale multimodal pretraining/instruction data; multiple Qwen2.5-VL sizes.

**What the paper does:** Documents model architecture, dynamic-resolution vision processing, document/chart understanding and capabilities.

**Limitations:** Technical report is model-development focused; benchmark performance does not establish causal faithfulness.

**Future work:** Future work includes continued scaling/capability development and broader multimodal interaction.

**Relevance to our thesis:** Primary model justification for Qwen2.5-VL-3B; use as model background, not as a novelty source.

**14. Visual Instruction Tuning (LLaVA)**

Liu, Li, Wu & Lee (NeurIPS 2023)

**Paper / PDF:** [https://arxiv.org/pdf/2304.08485](https://arxiv.org/pdf/2304.08485)

**Dataset / evaluation:** Visual instruction data generated with GPT-4 plus multimodal instruction-following datasets.

**What the paper does:** Introduces LLaVA visual instruction tuning for general-purpose multimodal understanding.

**Limitations:** Early-generation VLM; limited relative to current models and does not target conflict arbitration.

**Future work:** Broaden multimodal instruction data/model capabilities.

**Relevance to our thesis:** Historical foundation for instruction-tuned VLMs.

**15. Improved Baselines with Visual Instruction Tuning (LLaVA-1.5)**

Liu et al. (CVPR 2024)

**Paper / PDF:** [https://arxiv.org/pdf/2310.03744](https://arxiv.org/pdf/2310.03744)

**Dataset / evaluation:** 1.2M public multimodal instruction data mixture; academic VQA datasets.

**What the paper does:** Stronger LLaVA connector/data baselines with simple training changes.

**Limitations:** Primarily a baseline/model-engineering study; not a conflict-faithfulness paper.

**Future work:** Further improve data/architecture efficiency and multimodal performance.

**Relevance to our thesis:** Useful background on open-weight VLM evaluation.

**16. InstructBLIP: Towards General-purpose Vision-Language Models with Instruction Tuning**

Dai et al. (NeurIPS 2023)

**Paper / PDF:** [https://arxiv.org/pdf/2305.06500](https://arxiv.org/pdf/2305.06500)

**Dataset / evaluation:** 26 public datasets transformed into instruction-tuning format; 13 held-in/held-out datasets.

**What the paper does:** Instruction-aware Query Transformer and broad VLM instruction tuning.

**Limitations:** Broad capability study rather than causal reasoning/faithfulness; older architecture.

**Future work:** Generalize instruction tuning to more tasks/modalities and improve transfer.

**Relevance to our thesis:** Background on instruction-following VLM behavior.

Causal Source Arbitration — Team Literature Review Page 7

**17. BLIP-2: Bootstrapping Language-Image Pre-training with Frozen Image Encoders and LLMs**

Li et al. (ICML 2023)

**Paper / PDF:** [https://proceedings.mlr.press/v202/li23q/li23q.pdf](https://proceedings.mlr.press/v202/li23q/li23q.pdf)

**Dataset / evaluation:** Image-text pretraining and multiple vision-language evaluation datasets.

**What the paper does:** Efficiently bridges frozen vision encoder and frozen LLM through Q-Former.

**Limitations:** Older generation; not designed for conflict/source attribution.

**Future work:** More efficient multimodal pretraining and stronger alignment.

**Relevance to our thesis:** Architecture history for open VLMs.

**18. Flamingo: a Visual Language Model for Few-Shot Learning**

Alayrac et al. (2022)

**Paper / PDF:** [https://arxiv.org/pdf/2204.14198](https://arxiv.org/pdf/2204.14198)

**Dataset / evaluation:** Interleaved image/video-text data; few-shot multimodal benchmarks.

**What the paper does:** Architecture for few-shot visual-language learning with interleaved multimodal inputs.

**Limitations:** Large proprietary-scale model; not focused on source arbitration.

**Future work:** More capable few-shot multimodal learning and broader modality integration.

**Relevance to our thesis:** Foundational multimodal architecture.

**19. Chain-of-Thought Prompting Elicits Reasoning in Large Language Models**

Wei et al. (2022)

**Paper / PDF:** [https://arxiv.org/pdf/2201.11903](https://arxiv.org/pdf/2201.11903)

**Dataset / evaluation:** GSM8K and several arithmetic/commonsense/symbolic reasoning benchmarks.

**What the paper does:** Shows that intermediate reasoning prompts can improve complex reasoning.

**Limitations:** Language-only; CoT can be unfaithful and prompting effects are not causal explanations.

**Future work:** Understand when/how CoT produces genuine reasoning and improve reliability.

**Relevance to our thesis:** Conceptual foundation for verbalized reasoning.

**20. Self-Consistency Improves Chain of Thought Reasoning in Language Models**

Wang et al. (ICLR 2023)

**Paper / PDF:** [https://arxiv.org/pdf/2203.11171](https://arxiv.org/pdf/2203.11171)

**Dataset / evaluation:** GSM8K, SVAMP, AQuA, StrategyQA, ARC-Challenge.

**What the paper does:** Samples multiple CoT paths and marginalizes to a consistent answer.

**Limitations:** Adds inference cost and does not establish faithfulness of any individual rationale.

**Future work:** Apply consistency-based decoding to broader reasoning settings.

**Relevance to our thesis:** Useful inference-time control baseline, though not central to our causal question.

Causal Source Arbitration — Team Literature Review Page 8

**21. ReAct: Synergizing Reasoning and Acting in Language Models**

Yao et al. (ICLR 2023)

**Paper / PDF:** [https://arxiv.org/pdf/2210.03629](https://arxiv.org/pdf/2210.03629)

**Dataset / evaluation:** QA, fact verification, web interaction and decision-making environments.

**What the paper does:** Interleaves reasoning traces and actions to interact with external information.

**Limitations:** Primarily language-agent setting; not a source-arbitration framework.

**Future work:** More robust reasoning/action integration and external grounding.

**Relevance to our thesis:** Background for distinguishing reasoning traces from actual information use.

**22. Qwen-VL: A Versatile Vision-Language Model**

Bai et al. (2023), arXiv:2308.12966

**Paper / PDF:** [https://arxiv.org/pdf/2308.12966](https://arxiv.org/pdf/2308.12966)

**Dataset / evaluation:** Large multimodal training mixture and common vision-language benchmarks.

**What the paper does:** Introduces Qwen-VL family with visual grounding and instruction capabilities.

**Limitations:** Older model generation; limited direct relevance to current conflict-faithfulness questions.

**Future work:** Scale and improve multimodal understanding/grounding.

**Relevance to our thesis:** Historical Qwen lineage.

**23. Visual Question Answering (VQA): Dataset and Evaluation**

Antol et al. (ICCV 2015)

**Paper / PDF:** [https://arxiv.org/pdf/1505.00468](https://arxiv.org/pdf/1505.00468)

**Dataset / evaluation:** VQA dataset: natural images, questions, human answers.

**What the paper does:** Foundational visual question answering benchmark.

**Limitations:** Open-ended answers can make modality attribution difficult without controlled design.

**Future work:** More robust multimodal QA and reasoning benchmarks.

**Relevance to our thesis:** Useful benchmark history; our conflict dataset needs cleaner source attribution.

**24. GQA: A New Dataset for Real-World Visual Reasoning and Compositional Question Answering**

Hudson & Manning (CVPR 2019)

**Paper / PDF:** [https://openaccess.thecvf.com/content_CVPR_2019/papers/Hudson_GQA_A_New_Dataset_for_Real-World_Visual_Reasoning_](https://openaccess.thecvf.com/content_CVPR_2019/papers/Hudson_GQA_A_New_Dataset_for_Real-World_Visual_Reasoning_and_Compositional_Question_CVPR_2019_paper.pdf)
[and_Compositional_Question_CVPR_2019_paper.pdf](https://openaccess.thecvf.com/content_CVPR_2019/papers/Hudson_GQA_A_New_Dataset_for_Real-World_Visual_Reasoning_and_Compositional_Question_CVPR_2019_paper.pdf)

**Dataset / evaluation:** GQA derived from real-world images with compositional questions and scene graphs.

**What the paper does:** Compositional visual reasoning with structured explanations.

**Limitations:** Natural images contain multiple confounds and do not inherently isolate cross-modal source conflict.

**Future work:** More compositional/grounded visual reasoning.

**Relevance to our thesis:** Potential secondary validation dataset, not the primary conflict benchmark.

Causal Source Arbitration — Team Literature Review Page 9

**25. TextVQA: Towards Reasoning about Text in Images**

Singh et al. (CVPR 2019)

**Paper / PDF:** [https://openaccess.thecvf.com/content_CVPR_2019/papers/Singh_TextVQA_Towards_Reasoning_About_Text_in_Images_CVP](https://openaccess.thecvf.com/content_CVPR_2019/papers/Singh_TextVQA_Towards_Reasoning_About_Text_in_Images_CVPR_2019_paper.pdf)
[R_2019_paper.pdf](https://openaccess.thecvf.com/content_CVPR_2019/papers/Singh_TextVQA_Towards_Reasoning_About_Text_in_Images_CVPR_2019_paper.pdf)

**Dataset / evaluation:** TextVQA: images containing text with question-answer pairs.

**What the paper does:** Tests reading and reasoning over text embedded in images.

**Limitations:** OCR quality and image-text interaction introduce confounds for clean source attribution.

**Future work:** Improve OCR-aware multimodal reasoning and evidence grounding.

**Relevance to our thesis:** Useful for understanding image-text evidence competition.

**26. ChartQA: A Benchmark for Question Answering about Charts with Visual and Logical Reasoning**

Masry et al. (ACL 2022)

**Paper / PDF:** [https://aclanthology.org/2022.findings-acl.177.pdf](https://aclanthology.org/2022.findings-acl.177.pdf)

**Dataset / evaluation:** ChartQA benchmark with chart images, questions and answers.

**What the paper does:** Evaluates visual and logical reasoning over charts.

**Limitations:** Chart questions combine visual parsing and reasoning, making causal source attribution difficult without controlled pairing.

**Future work:** Improve chart reasoning, numerical reasoning and grounded explanations.

**Relevance to our thesis:** Background for chart-based conflict validation.

**27. DocVQA: A Dataset for VQA on Document Images**

Mathew et al. (WACV 2021)

**Paper / PDF:** [https://arxiv.org/pdf/2007.00398](https://arxiv.org/pdf/2007.00398)

**Dataset / evaluation:** Document images and question-answer pairs.

**What the paper does:** Document visual question answering and OCR-aware reasoning.

**Limitations:** Document layout/OCR confounds make it less suitable as a clean conflict-arbitration benchmark.

**Future work:** More robust document understanding and reasoning.

**Relevance to our thesis:** Potential real-world validation setting.

**28. ScienceQA: A Novel Large-Scale Dataset for Science Question Answering**

Lu et al. (CVPR 2022)

**Paper / PDF:** [https://openaccess.thecvf.com/content/CVPR2022/papers/Lu_ScienceQA_A_Novel_Large-Scale_Dataset_for_Science_Question](https://openaccess.thecvf.com/content/CVPR2022/papers/Lu_ScienceQA_A_Novel_Large-Scale_Dataset_for_Science_Question_Answering_CVPR_2022_paper.pdf)
[_Answering_CVPR_2022_paper.pdf](https://openaccess.thecvf.com/content/CVPR2022/papers/Lu_ScienceQA_A_Novel_Large-Scale_Dataset_for_Science_Question_Answering_CVPR_2022_paper.pdf)

**Dataset / evaluation:** Science questions with image/diagram contexts and explanations.

**What the paper does:** Multimodal science reasoning with explanatory answers.

**Limitations:** Question difficulty, domain knowledge and diagram interpretation can confound modality-arbitration analysis.

**Future work:** Improve multimodal science reasoning and explanation grounding.

**Relevance to our thesis:** Useful secondary validation domain.

Causal Source Arbitration — Team Literature Review Page 10

**29. POPE: Polling-based Object Probing Evaluation of Object Hallucination in Large**
**Vision-Language Models**

Li et al. (ECCV 2024)

**Paper / PDF:** [https://arxiv.org/pdf/2305.10355](https://arxiv.org/pdf/2305.10355)

**Dataset / evaluation:** COCO-based object existence probes and adversarial/random/popular sampling.

**What the paper does:** Evaluates object hallucination through controlled polling questions.

**Limitations:** Focuses on hallucination rather than conflicting image/text sources.

**Future work:** More robust hallucination evaluation and mitigation.

**Relevance to our thesis:** Relevant reliability background; not a direct arbitration benchmark.

**30. Hallucination in Large Vision-Language Models: A Survey**

Huang et al. (2023/2024 survey literature)

**Paper / PDF:** [https://arxiv.org/pdf/2311.17397](https://arxiv.org/pdf/2311.17397)

**Dataset / evaluation:** Survey of hallucination datasets and evaluation methods.

**What the paper does:** Organizes hallucination causes, benchmarks and mitigation methods in LVLMs.

**Limitations:** Survey scope is broad and not a causal experiment.

**Future work:** Develop better hallucination definitions, evaluation and mitigation.

**Relevance to our thesis:** Use for related-work framing rather than direct experimental design.

**31. MMHal-Bench: A Comprehensive Benchmark for Multimodal Hallucination**

Sun et al. (2024)

**Paper / PDF:** [https://arxiv.org/pdf/2404.07864](https://arxiv.org/pdf/2404.07864)

**Dataset / evaluation:** Multimodal hallucination evaluation prompts/images with human/LLM-assisted evaluation.

**What the paper does:** Benchmarks hallucination in multimodal answers.

**Limitations:** Evaluation can rely on judge-based scoring and is not designed to isolate source arbitration.

**Future work:** More objective multimodal hallucination evaluation.

**Relevance to our thesis:** Useful adjacent reliability literature.

**32. Chain-of-Thought Hub: A Collection of Reasoning Tasks and Prompting Methods**

Fu et al. / CoT benchmark literature (2023)

**Paper / PDF:** [https://arxiv.org/pdf/2305.08291](https://arxiv.org/pdf/2305.08291)

**Dataset / evaluation:** Collection of reasoning datasets including arithmetic and commonsense tasks.

**What the paper does:** Aggregates reasoning tasks and evaluates prompting methods.

**Limitations:** Primarily language-only and benchmark-oriented.

**Future work:** Broader reasoning evaluation and prompting research.

**Relevance to our thesis:** Useful methodological background for prompt-control experiments.

Causal Source Arbitration — Team Literature Review Page 11

Causal Source Arbitration — Team Literature Review Page 12

## **3. Cross-Paper Gap Matrix**

The table below is the most important team discussion page. A paper can overlap with the thesis in one dimension without occupying the entire proposed contribution.

|Dimension|Already established|What remains relevant to test|
|---|---|---|
|Modality preference|VLMs can favor text or vision; preference changes by<br>task and input reliability.|Measure arbitration in a controlled benchmark, then move<br>beyond measurement to intervention.|
|Conflict detection|Conflict signals can be decoded and may emerge at<br>intermediate layers.|Test whether an explicit conflict state changes the later<br>decision.|
|Conflict resolution|Models show different resolution behaviors under<br>controlled conflicts.|Separate resolution from generic reasoning/prompt-length<br>effects.|
|Explicit conflict prompting|Mixed Signals already evaluates explicit<br>conflict-handling prompts/decomposition.|Do not claim simple conflict verbalization as novel; use<br>computation-matched and counterfactual source<br>interventions.|
|Source monitoring|Models can track source modality imperfectly; syntax<br>and semantic cues matter.|Connect source identity to a concrete conflict-arbitration<br>decision.|
|CoT faithfulness|Generated multimodal explanations can omit or<br>misrepresent influential visual cues.|Test whether a manipulated source/conflict rationale<br>actually changes downstream arbitration.|
|Causal rationale<br>intervention|Lanham et al. show rationale interventions can reveal<br>whether models condition on CoT.|Transfer this logic to cross-modal conflict and source<br>arbitration with matched controls.|
|Multimodal faithfulness|Recent benchmarks/frameworks evaluate or improve<br>visual evidence grounding.|Use arbitration as the concrete decision variable and keep<br>the experiment lightweight/reproducible.|

## **4. Candidate Thesis Gap**

**Candidate gap statement:** Existing studies establish modality preference, conflict detection/resolution, source-modality monitoring and multimodal CoT faithfulness, but it remains insufficiently established whether an explicitly represented cross-modal conflict/source state causally changes the subsequent source-arbitration decision when generic additional inference computation and prompt-length effects are controlled.
## **5. Recommended Experimental Upgrade**

**A0 — Direct:** image + text → answer.
**A1 — Length-matched neutral placebo:** image + text → neutral evidence description → answer.
**A2 — Conflict verbalization:** image source claim + text source claim → explicit agreement/contradiction → answer.
**A3 — Source-attribution intervention:** explicitly identify which source supports which claim before answer.
**A4 — Counterfactual source-attribution:** keep image/text evidence fixed while changing the stated source identity; measure whether arbitration follows content or the manipulated source label.

**Primary outcome:** source-following/arbitration choice. **Secondary outcomes:** conflict-detection accuracy, arbitration flip rate, conditional log-likelihood margin, effect size, and robustness across degradation/task subsets.
## **6. What the Team Should Not Claim**

Do not claim that the study proves the model has a human-like causal reasoning process. Do not claim that one prompt proves or disproves chain-of-thought faithfulness. A defensible claim is narrower: an inference-time intervention caused a measurable change (or no measurable change) in observable source arbitration under the tested controlled conditions.
## **7. Final Team Reading Checklist**

 - Read the full Methods + Appendix of Which Source Wins? and compare its conflict construction to our primary dataset.

 - Read the intervention/mitigation section of Mixed Signals and record exactly what prompts were tested.

 - Read Source-Modality Monitoring and determine whether its source cues can be adapted without duplicating the task.

 - Read Challenges in Modality Conflict for detection-vs-resolution methodology.

 - Read the CoT-faithfulness papers before deciding how to interpret verbalized explanations.

Causal Source Arbitration — Team Literature Review Page 13

 - Reproduce the direct baseline on a small subset before adding any intervention.

 - Pre-register/lock the prompt templates and token-length matching rules before the full run.

 - Include a negative-result interpretation plan: if A2/A3 do not beat A1, that result is scientifically informative.

 - Only after the above checks should the team freeze the final title, RQs and protocol.

**Source note**

The paper summaries were prepared from the linked papers/official paper pages and recent web verification. Recent papers, especially 2026 preprints, may still change. The PDF intentionally distinguishes direct author-stated limitations/future work from reviewer interpretation.

Causal Source Arbitration — Team Literature Review Page 14
