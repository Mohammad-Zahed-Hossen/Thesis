# **Adversarial Research Audit of Multimodal Agent Tool Use and Active Perception Thesis Gaps**

## **1\. Executive Conclusion**

An exhaustive verification of secondary research audits against the primary publications of AdaTooler-V, NTEP-R, SRICE, CAM-DF, Agentic Abstention, ToolGate, and TACO confirms that the broad formulation of Candidate 2—whether a multimodal agent can learn to predict tool utility and decide when to invoke a tool versus stop or answer directly—is thoroughly occupied by existing literature. The hypothesis that multimodal large language models (MLLMs) invoke tools blindly and require learned mechanisms to balance tool utility against direct execution is not an open research question.

AdaTooler-V explicitly operationalizes this objective by calculating a sample-level Tool Benefit Score, defined as the accuracy differential between tool-assisted and direct rollouts on a 72B parameter vision-language model, and optimizes an adaptive policy via reinforcement learning to suppress unneeded invocations across twelve benchmarks. Concurrently, ToolGate establishes pre-call execution gating for vision-language agents, predicting whether proposed perceptual operations are worth executing and reducing token overhead by up to thirty-six percent while preserving task accuracy. In parallel, TACO formalizes Differential Answer-Probe Rewards to measure the causal contribution of each intermediate tool operation, penalizing misleading actions without requiring auxiliary judge models. Beyond the visual domain, CAM-DF establishes regret-weighted, cost-aware stopping over tool acquisition prefixes, while Agentic Abstention defines sequential evaluation benchmarks and context playbooks for determining when an agent should cease acting.

Candidate 2 survives only if it pivots away from proposing algorithmic architectures for tool selection or utility prediction, which are already heavily engineered, toward a rigorous, adversarial measurement and confound audit. Existing literature systematically confounds the acquisition of novel visual evidence with the receipt of auxiliary inference-time computation, failing to isolate whether accuracy gains stem from high-resolution image patches or from additional autoregressive tokens, extra forward passes, and expanded reasoning opportunities. Furthermore, current frameworks rely on circular, model-relative definitions of tool necessity that merely capture the perceptual weaknesses of specific model checkpoints rather than the objective informational insufficiency of the visual input. Finally, prior work rarely benchmarks learned agents against trivial, deterministic heuristic baselines, such as uniform multi-scale image slicing.

Candidate 2 is scientifically viable solely as an empirical evaluation thesis that decouples visual evidence from computational scaling, evaluates the cross-model transferability of tool necessity, and establishes the empirical boundary where learned policies fail to outperform static workflows. Under undergraduate compute and hardware constraints, this diagnostic contribution is turnkey, methodologically defensible, and insusceptible to preemptive publication risks.

## **2\. Audit-to-Audit Contradiction Table**

The subsequent analysis cross-examines the claims, supporting evidence, and conclusions of the two secondary research audits (Audit A: AlphaxiV Report; Audit B: Perflexity Source Finder).

| Dimension | Audit A (AlphaxiV Report) | Audit B (Perflexity Source Finder) | Agreement? | Stronger Evidence | Verification Resolution |
| :---- | :---- | :---- | :---- | :---- | :---- |
| **Literature Coverage** | Concentrates on vision-language reinforcement learning and active perception: AdaTooler-V, VTool-R1, ACTIVE-o3, MMSearch-Plus, ActiView, TIR-Bench, Budget-Aware Tool Use. | Concentrates on general agentic tool calling, evidence paths, and abstention: NTEP-R, SRICE, CAM-DF, Agentic Abstention, VisualToolBench, CropVLM, MED. | No | Complementary coverage; Audit A captures core multimodal RL, while Audit B captures sequential agentic stopping. | **VERIFIED.** Combining both corpora is required to evaluate the full scope of active visual acquisition and stopping policies. |
| **Closest Prior Work** | AdaTooler-V (arXiv:2512.16918). | NTEP-R (arXiv:2609.03493) and CAM-DF (arXiv:2607.27083). | No | Audit A identifies work closer to visual utility prediction. | **VERIFIED.** AdaTooler-V directly optimizes tool benefit scores on visual tasks. Audit B omitted AdaTooler-V. |
| **Prior-Art Occupation** | Asserts that the broad domain of adaptive tool invocation is occupied by AdaTooler-V and VTool-R1. | Asserts that tool utility prediction is open because prior work lacks a standalone visual utility classifier. | **Major Contradiction** | Audit A is supported by primary sources. Audit B relies on superficial terminology differences. | **VERIFIED.** AdaTooler-V's AT-GRPO and ToolGate's pre-call gating directly learn utility and skip policies for visual tools. |
| **Tool Utility Prediction** | Cites AdaTooler-V's sample-level Tool Benefit Score \\Delta S \= S^+ \- S^- as direct prior occupation. | Claims NTEP-R and SRICE do not predict utility, and CAM-DF is non-visual, leaving utility prediction open. | **Major Contradiction** | Audit A. | **VERIFIED.** Tool utility prediction is occupied by AdaTooler-V, ToolGate, and TACO. Standalone classification is an incremental implementation detail. |
| **Tool Necessity** | Notes necessity is confounded by reference model weakness and lack of counterfactual controls. | Argues tool necessity is an open gap if framed as a calibrated necessity predictor. | Partial | Audit A provides a deeper critique of circularity and model relativism. | **INFERRED.** Tool necessity cannot serve as a reliable label unless separated from backbone-specific failure modes. |
| **Stopping / Termination** | Focuses on budget tracking (Budget-Aware Tool Use) and active view selection (ActiView). | Formally details CAM-DF (payoff gap stopping) and Agentic Abstention (AbsRec@K, CONVOLVE). | No | Audit B provides formal mathematical stopping models. | **VERIFIED.** General agentic stopping is solved in principle by CAM-DF and Agentic Abstention; visual stopping without external APIs remains narrow. |
| **Active Perception** | Details subview selection in ActiView and region RL in ACTIVE-o3. | Identifies CropVLM, OpenSearch-VL, and OmniAgent. | Yes | Audit A (analysis of ActiView is more actionable). | **VERIFIED.** Visual operations such as zooming, shifting, and cropping are saturated with benchmarks and RL frameworks. |
| **Cost-Aware Reasoning** | Identifies Budget-Aware Tool Use as text-only web search. | Identifies CAM-DF and ESearch-R1 as modeling heterogeneous action costs. | Yes | Audit B (covers formal payoff formulations). | **VERIFIED.** Cost-aware stopping is occupied in text domains; visual token-cost gating is occupied by ToolGate. |
| **Benchmark Availability** | Recommends ActiView (314 QA, 1,625 instances) and deterministic TIR-Bench subsets. | Highlights VisualToolBench, VTC-Bench, and MM-ToolSandBox. | Partial | Audit A is superior for undergraduate execution. | **VERIFIED.** ActiView has deterministic ground truth; VisualToolBench relies heavily on LLM-as-a-judge rubrics. |
| **Reproducibility & Compute** | Asserts that replicating AdaTooler-V or VTool-R1 requires 8 to 16 H100s, exceeding Colab Pro. | Proposes training a visual utility predictor on Colab Pro without analyzing GPU memory limits. | **Major Contradiction** | Audit A is grounded in hardware constraints. | **VERIFIED.** RL fine-tuning of 7B MLLMs is infeasible on Colab Pro; only lightweight routing or frozen probing is viable. |
| **Final Recommendation** | **RESERVE** (pivot to counterfactual evaluation and error decomposition). | Implicitly optimistic about constructing a visual tool-utility predictor. | **Major Contradiction** | Audit A provides a safe academic defense. | **VERIFIED.** Pursuing Audit B's direction would lead to immediate rejection by reviewers familiar with AdaTooler-V and ToolGate. |

The disagreements between the two secondary audits stem from divergent methodologies regarding what constitutes a genuine research gap. Audit B adopts a literal, keyword-based interpretation of novelty: because existing works such as NTEP-R and SRICE do not explicitly label a standalone modular sub-network as a "visual tool-utility predictor," it deduces that visual tool utility prediction remains open. This reasoning fails to account for functional equivalence.

Audit A correctly examines the underlying training objectives and identifies that AdaTooler-V operationalizes the identical empirical relationship through its Tool Benefit Score:

\\Delta S\_i \= S^+(q\_i) \- S^-(q\_i)

which directly drives policy optimization. Furthermore, Audit B overlooks compute feasibility. It suggests training utility predictors on visual benchmarks within Google Colab Pro, whereas primary source inspection of AdaTooler-V and VTool-R1 confirms that policy rollouts, value estimation, and gradient updates on multimodal backbones demand multi-node H100/A100 clusters running distributed frameworks like VERL-tool and LLaMA-Factory. Audit A's conservative recommendation to restrict the scope to deterministic measurement and frozen-model routing reflects the actual state of the literature and computational reality.

## **3\. Primary Literature Autopsies**

### **AdaTooler-V**

The primary investigation examined the full publication by Wang et al. (arXiv:2512.16918v3, accepted to ACL 2026 Findings) and its official implementation repository.

The exact research problem addressed is the phenomenon of blind tool use in multimodal language models, wherein models execute external vision tools indiscriminately, increasing inference latency and degrading reasoning accuracy on problems that can be solved directly. The central hypothesis is that an MLLM can learn an adaptive tool-invocation policy if guided by a reinforcement learning algorithm that scales sample-level rewards based on empirical tool benefit. The model operates across single-image, multi-image, and video modalities on general visual question answering, high-resolution perception, and fine-grained spatial inspection tasks. The available tool action space comprises crop\_image, FrameAt, VideoClip, and PathTracer.

The tool-selection mechanism is autoregressive and interleaved within the MLLM decoder, generating either tool execution tokens or standard text reasoning steps. The model explicitly learns whether to call a tool via Adaptive Tool-use GRPO (AT-GRPO). Offline tool utility is estimated during data curation using the Tool Benefit Score:

\\Delta S\_i \= S^+(q\_i) \- S^-(q\_i)

where S^+ and S^- represent the average accuracy of Qwen2.5-VL-72B-Instruct evaluated across eight rollouts with and without tools, respectively. Action values and information gain are modeled implicitly through the policy advantage weighted by \\Delta S\_i. Tool necessity is explicitly categorized: instances where \\Delta S\_i \\le 0 are designated unhelpful, and tool invocations on these samples are penalized during reinforcement learning. Stopping is learned autoregressively through end-of-turn token generation. Cost is addressed by penalizing unnecessary tool calls, which stabilizes average response length during training, though explicit monetary pricing is omitted. Epistemic uncertainty is not modeled.

The framework compares against no-tool baselines by evaluating S^-(q\_i) during data annotation and conducting ablation studies. Counterfactual evaluation is demonstrated in Section 4.3.4, where disabling tools drops accuracy from 89.8% to 84.4% on V\* Bench. The model is trained on AdaTooler-V-CoT-100k and AdaTooler-V-300k, and evaluated on twelve benchmarks including V\*, VSI-Bench, VideoMMMU, MVBench, Video-MME, and MathVista. Ground truth consists of multiple-choice labels, numerical answers, and Word Error Rate (WER) for text extraction. Code, configuration files, and model checkpoints are available at the official repository, though training requires eight 80GB A100/H100 GPUs. The primary empirical claim is that AdaTooler-V-7B attains 89.8% on V\* Bench, outperforming GPT-4o (84.4%). This work directly preempts any claim that teaching multimodal models when to invoke tools based on accuracy benefit is novel.

### **NTEP-R**

The primary investigation examined the publication by Long et al. (arXiv:2609.03493v1).

The paper addresses the limitation that outcome-only reinforcement learning in agentic VLMs leaves evidence acquisition insufficiently supervised, resulting in redundant, off-target tool calls and failure to extract information from returned observations. The hypothesis posits that process supervision aligning pre-call intent and post-call summaries with an annotated Necessary Tool-Evidence Path (NTEP) maximizes search accuracy while suppressing redundant calls. The framework operates on image-grounded queries for fine-grained VQA and knowledge-intensive visual tasks using a unified three-tool action space: image cropping, visual search, and text retrieval.

The tool-selection mechanism uses a ReAct-style agentic policy. The model learns whether to invoke tools by receiving rewards only when a proposed call aligns with an unsatisfied necessary evidence goal. Tool utility and information gain are supervised through process alignment rewards, and action values are reflected in token-level policy advantages. Tool necessity is explicitly modeled via the NTEP schema, which specifies the essential evidence required for each query. Stopping is learned through policy optimization augmented by a non-repeated-goal regularizer that penalizes redundant calls revisiting satisfied goals. Monetary and token costs are not parameterized, and uncertainty quantification is omitted.

The method is compared against standard SFT and RL baselines trained solely on final outcome correctness, and ablations evaluate performance when removing intent rewards, observation rewards, or the non-repeated-goal regularizer. The approach is evaluated across seven image-grounded benchmarks using task accuracy, redundant call rates, and evidence path coverage. Code was promised for future release. The primary claim is that NTEP-8B improves search-oriented accuracy while curtailing redundant invocations. This work demonstrates that fine-grained tool necessity and redundant call suppression have already been formalized and supervised in vision-language models.

### **SRICE**

The primary investigation examined the publication by Zhi et al. (arXiv:2503.08308v1).

The paper targets visual hallucinations and spatial reasoning errors in MLLMs when interpreting complex scenes containing small or overlapping objects. The hypothesis states that calibrating external vision tools via Conformal Prediction (CP) enables training-free, uncertainty-aware region selection and reasoning path routing. The framework processes static images and text prompts for VQA across VQA-v2, VizWiz, GQA, Flickr30K, and MMBench. The tool space comprises SEEM for semantic segmentation and YOLOv11 for object detection.

The framework operates via a fixed, two-stage pipeline: tools generate object proposals, conformal prediction constructs calibrated prediction sets, and the MLLM selects regions of interest (RoIs). The model does not learn whether to call a tool; the framework is strictly training-free, and tools are executed unconditionally upfront. It does not estimate downstream answer utility or action value, but quantifies perceptual uncertainty via conformal non-conformity scores and quasi-conformal top-p coverage over CoT tokens. It does not model tool necessity or incorporate stopping decisions, executing a static computation graph. Cost is unmodeled, ignoring the overhead of running dense segmentation on every input.

The approach compares against base LLaVA-OneVision-7B and Visual CoT baselines, reporting accuracy and Expected Calibration Error (ECE). Code implementation relies on public model checkpoints and standard COCO calibration data. The primary empirical claim is that conformal calibration of tool outputs improves MLLM reasoning reliability without parameter updates. This demonstrates that uncertainty-aware visual augmentation can be achieved via training-free calibration, challenging the assumption that complex learned agents are necessary for perceptual enhancement.

### **CAM-DF**

The primary investigation examined the publication by Liu et al. (arXiv:2607.27083v1).

The research addresses the problem that tool-calling LLM agents over-acquire tools because retriever confidence scores do not align with optimal decision boundaries, creating substantial compute and monetary inefficiencies. The hypothesis posits that formulating pre-execution tool acquisition as a decision-focused stopping problem trained directly on the empirical payoff gap enables optimal cost-aware termination. The modality is text-based, processing tool descriptions and user queries across \\tau-bench Retail, MCP-Atlas, and WorkBench (1,343 tasks total) over heterogeneous REST APIs and database functions.

The tool-selection mechanism evaluates ranked lists of candidate tools and determines an optimal stopping depth k^\*. The system learns whether to acquire an additional tool or terminate at the current prefix. It explicitly estimates marginal tool utility by predicting the payoff gap between stopping immediately versus continuing execution. It models information sufficiency—whether the acquired tool set resolves the task—and optimizes the objective:

U(A, x) \= \\text{sufficiency}(A, x) \- \\lambda \\sum\_{j \\in A} c\_j

where c\_j represents heterogeneous tool costs. Stopping is the central learned contribution, implemented via a logistic classifier (CAM-DF) trained with regret weights. Uncertainty is handled through empirical decision margins rather than Bayesian posteriors.

Baselines include fixed-k depth, score thresholding, score-per-cost thresholding, predict-then-threshold, and non-deployable prefix oracles. Trajectory ablations compare all sub-prefixes against hindsight optimal prefixes. Evaluation metrics include mean payoff, task sufficiency rate, acquisition cost, and live task success evaluated with 95% bootstrap confidence intervals. The implementation is lightweight and reproducible using standard tabular classifiers over frozen LLM embeddings. The primary claim is that CAM-DF outperforms score thresholding, achieving higher sufficiency at 30% to 50% lower acquisition cost. This work fully occupies the theoretical and algorithmic space of cost-aware stopping under heterogeneous costs.

### **Agentic Abstention**

The primary investigation examined the publication by Han et al. (arXiv:2606.28733v1) and its official project repository.

The paper investigates execution bias in autonomous agents, where agents persistently take redundant or harmful actions when tasks are impossible or required information is missing, rather than abstaining. The hypothesis states that agents must treat abstention as an explicit sequential decision primitive (ACT versus ANSWER versus ABSTAIN) and can learn timely abstention through trajectory-distilled context playbooks (CONVOLVE). The environment covers interactive text, web navigation, and bash terminal interfaces across WebShop, Terminal-Bench 2.0, and interactive QA.

The tool-selection mechanism uses a ReAct agentic policy prompted with CONVOLVE playbooks, operating over bash commands, web interactions, search calls, and an explicit ABSTAIN command. The agent explicitly learns whether to act or abstain, evaluating whether further actions have a positive probability of success. Action values and information gain are represented implicitly via context distillation. Tool necessity is evaluated against task solvability. The stopping decision is the primary research target, learned in-context via playbook distillation. Cost is penalized through Success weighted by Path Length (SPL), and uncertainty is modeled over partial environment observability.

Baselines comprise thirteen frontier LLMs (such as Llama-3.3-70B and Qwen models) and two scaffolding frameworks (Terminus 2, Codex CLI). Ablations evaluate unanswerable tasks where critical entities or tools are removed. The benchmark is supported by the AgentAbstain dataset across 42 sandboxes. Metrics include Abstention Recall at step K (AbsRec@K), Timely Recall (AbsRec@1), SPL, and over-abstention rates on solvable tasks. Code and datasets are publicly accessible. The primary claim is that frontier agents fail at timely abstention (AbsRec@1 \< 25%), and CONVOLVE restores early stopping without harming solvable tasks. This confirms that agentic abstention, sequential stopping, and failure-aware termination are thoroughly formalized.

## **4\. Prior-Art Occupation Map**

The table below maps the conceptual dimensions of the proposed thesis against existing literature, classifying occupation status under the rule that a candidate is occupied if prior work investigates substantially the same causal question regardless of terminology.

| Conceptual Dimension | Equivalent Literature Terminology | Representative Primary Works | Mechanism and Empirical Scope | Occupation Status |
| :---- | :---- | :---- | :---- | :---- |
| **Tool Selection** | Action selection, tool routing, API recommendation | ReAct, ToolBench, Gorilla, VTC-Bench | Selects a specific tool from a predefined candidate set based on task semantics. | **FULLY OCCUPIED** |
| **Adaptive Tool Invocation** | Adaptive tool-use, dual-mode reasoning, think-with-images | AdaTooler-V, VTool-R1, OpenSearch-VL | Decides between direct text reasoning and invoking vision tools via reinforcement learning advantage weighting. | **FULLY OCCUPIED** |
| **Tool Utility Prediction** | Tool Benefit Score (\\Delta S), pre-call gating, DAPR | AdaTooler-V, ToolGate, TACO | Predicts or scores whether executing a specific visual tool improves final answer correctness. | **FULLY OCCUPIED** |
| **Tool Necessity** | Necessary evidence paths, sufficiency, redundant call suppression | NTEP-R, CAM-DF, CropVLM | Assesses whether the original input contains sufficient evidence or requires external tool execution. | **SUBSTANTIALLY OCCUPIED** |
| **Cost-Aware Stopping** | Payoff-gap stopping, budget-aware scaling, pre-execution gating | CAM-DF, Budget-Aware Tool Use, ToolGate | Optimizes the stopping threshold against explicit monetary, API, or token budgets. | **FULLY OCCUPIED** |
| **Multimodal Abstention** | Agentic abstention, unanswerable VQA, failure deferral | Agentic Abstention, ConflictGuard | Evaluates whether an agent can recognize impossible visual tasks and terminate execution early. | **SUBSTANTIALLY OCCUPIED** |
| **Active Visual Perception** | Zoom/crop policies, guided visual search, dynamic resolution | ActiView, ACTIVE-o3, V\*, CropVLM | Sequentially crops, shifts, or zooms into image sub-regions to extract fine-grained visual details. | **FULLY OCCUPIED** |
| **Counterfactual Confound Isolation** | Causal tool attribution, reasoning vs. perception controls | MED, ToolAnchor | Decomposes tool-induced performance gains into visual information acquisition versus inference compute scaling. | **PARTIALLY OPEN / NICHE** |

## **5\. Tool Utility / Necessity / Stopping Analysis**

A critical vulnerability in current research is the conflation of tool selection, tool necessity, tool utility, and stopping mechanisms into an undifferentiated agent capability. These four concepts represent distinct mathematical and operational formulations:

| Concept | Core Research Question | Formal Mathematical Definition | Operational Scope | Prior Implementations |
| :---- | :---- | :---- | :---- | :---- |
| **Tool Selection** | *Which tool* should be invoked from an available set? | a^\* \= \\arg\\max\_{a \\in \\mathcal{T}} P(a \\mid x, \\tau\_t) | Assumes an action must be taken; optimizes categorical assignment over tools. | ToolBench, VTC-Bench, Gorilla. |
| **Tool Necessity** | Is additional external evidence *required* to resolve the input? | \\mathcal{N}(x) \= \\mathbb{I}(\\text{Info}(x) \< \\Theta) | Property of the input state; holds true even if available tools cannot extract the evidence. | NTEP-R, CAM-DF. |
| **Tool Utility** | Will executing candidate action a *improve* the final answer? | \\Delta U(a, x) \= \\Pr(\\text{Correct} \\mid x, a) \- \\Pr(\\text{Correct} \\mid x) | Property of the action-state pair; can be zero even if the tool is theoretically necessary. | AdaTooler-V, ToolGate, TACO. |
| **Stopping** | Is current evidence *sufficient* to emit a final answer? | \\text{Stop}(\\tau\_t) \= \\mathbb{I}\\left(\\max\_a \\mathbb{E}\[\\Delta U(a, \\tau\_t)\] \\le \\lambda \\cdot \\text{Cost}(a)\\right) | Sequential policy deciding when marginal utility falls below marginal execution cost. | CAM-DF, Agentic Abstention, BATS. |

In addition to separating these four concepts, stopping mechanisms in the literature must be organized into six formal operational categories:

> 1. Fixed horizon stopping, where execution terminates upon reaching a predefined step count limit T\_{\\max}, as seen in basic ReAct frameworks.  
> 2. Heuristic threshold stopping, where execution halts when auxiliary retriever confidence or similarity exceeds a static value \\theta, common in standard retrieval systems.  
> 3. Predictive usefulness gating, where a model predicts whether any action from the tool set will yield useful evidence before executing it, as demonstrated by ToolGate's pre-call classifier.  
> 4. Expected utility prediction, where an agent explicitly models the continuous accuracy improvement \\mathbb{E}\[\\Delta S\] of an action, as implemented in AdaTooler-V's reward structure and TACO's differential probes.  
> 5. Explicit cost-information optimization, where an agent optimizes the objective U \= \\text{Sufficiency} \- \\lambda \\sum \\text{Cost}, trading off marginal information gain against heterogeneous execution costs, as formalized in CAM-DF and BATS.  
> 6. Sufficient-evidence abstention, where an agent sequentially evaluates whether the accumulated evidence justifies emitting an answer, continuing search, or abstaining due to task impossibility, as formulated in Agentic Abstention and NTEP-R.

Because predictive gating, expected utility modeling, cost optimization, and sufficient-evidence stopping are already implemented by ToolGate, AdaTooler-V, CAM-DF, and Agentic Abstention, a thesis proposing to teach an agent when to stop calling tools would simply rename an established mechanism.

## **6\. Experimental Confounds**

Any proposed research in this area must address seven major experimental confounds that undermine the validity of published findings across active perception and tool-use literature.

The primary methodological issue is the token and reasoning compute confound. When an agent invokes a visual tool, such as cropping a region of interest, the execution pipeline introduces four concurrent variables: new visual tokens from the crop, an additional forward pass through the model, extra autoregressive chain-of-thought tokens reflecting on the intermediate observation, and a second opportunity to revise initial reasoning. Consequently, demonstrating that a tool-using agent achieves higher accuracy than a direct-answering model does not prove that the visual crop provided decisive information. The improvement may stem entirely from test-time compute scaling. Existing papers systematically fail to control for this baseline disparity.

A secondary challenge is the circularity of tool necessity definitions. In frameworks like AdaTooler-V, tool necessity is operationalized as a positive Tool Benefit Score:

\\Delta S\_i \= S^+(q\_i) \- S^-(q\_i) \> 0

where S^- is evaluated using a specific reference model (Qwen2.5-VL-72B). This creates a model-relative definition of necessity: a tool is deemed necessary simply because that particular model fails without it. This is fundamentally distinct from information-relative necessity, where the visual evidence is physically absent or below the Nyquist sampling limit in the original input. Model-relative necessity merely captures the idiosyncratic visual representations, pre-training corpus distributions, and attention failures of the chosen reference model.

Benchmark construction further introduces artificial pressure to call tools. Datasets like V\* Bench and TIR-Bench deliberately curate images where target entities occupy less than 0.1% of the pixel area or apply artificial distortions that force tool execution. On these benchmarks, an uncalibrated policy that always calls tools performs near-optimally, masking whether an agent possesses true decision calibration. Conversely, standard visual QA benchmarks contain few samples where tools are beneficial, penalizing tool-capable agents through accumulated context noise.

Evaluation protocols introduce additional distortion through model-judge variance. Benchmarks such as VisualToolBench and VideoSeeker rely on proprietary LLMs or VLMs to score open-ended agent trajectories against rubrics. These judges exhibit established self-preference biases, length biases, and high prompt sensitivity. Small reported improvements from adaptive gating can fall entirely within the variance of the judge model.

Furthermore, tool-output advantages are often mistaken for agentic reasoning. When an agent invokes an OCR or object detection tool, the tool returns structured ASCII text or localized bounding boxes, injecting external ground-truth representations directly into the context window. The resulting performance gain reflects the specialized capabilities of the external vision model rather than superior decision-making by the agent.

Literature also frequently ignores fixed-policy equivalence. In active visual perception, complex reinforcement learning policies are rarely compared against static heuristic baselines. A simple deterministic workflow that uniformly tiles an image into a multi-scale grid or extracts a center crop can match the accuracy of an RL-trained cropping policy, while operating with lower latency and avoiding agent decision failures.

Finally, cost confounding remains prevalent. Measuring efficiency purely by counting tool calls ignores real computational and monetary budgets. A single high-resolution crop processed through a dynamic-resolution vision encoder can generate thousands of visual tokens, incurring more latency and FLOPs than multiple text-based API queries. Without token-weighted and dollar-weighted cost accounting, claims of agentic efficiency lack empirical grounding.

## **7\. Controls and Counterfactual Evaluation**

To establish a defensible empirical contribution, an experimental framework must incorporate strict counterfactual controls designed to isolate each confound identified in the literature.

| Target Confound | Experimental Condition | Implementation Protocol | Isolated Causal Factor |
| :---- | :---- | :---- | :---- |
| **Token / Reasoning Confound** | **Compute-Matched Direct CoT** | Direct VLM is prompted with an explicit generation budget matching the total token count of the tool-using agent's multi-turn trajectory. | Separates test-time token scaling from visual information acquisition. |
| **Token / Reasoning Confound** | **Masked Tool Observation** | The agent invokes the tool, but the returned image patch is replaced with a uniform neutral mask; the agent completes reasoning over the blank observation. | Isolates the contribution of the visual pixels from the multi-step deliberation loop. |
| **Visual Information Confound** | **Irrelevant Tool Intervention** | The tool returns a valid high-resolution crop extracted from a completely unrelated distractor image. | Tests whether the agent conditions its answer on the visual evidence or hallucinates from intermediate text. |
| **Model-Relative Necessity** | **Cross-Model Necessity Transfer** | Tool benefit labels \\Delta S computed on Model A (e.g., Qwen2.5-VL-7B) are evaluated against Model B (e.g., Gemini-1.5-Flash or LLaVA-OneVision). | Determines whether tool necessity is an invariant property of the visual query or an artifact of model weakness. |
| **Fixed-Policy Equivalence** | **Deterministic Multi-Scale Workflow** | Evaluates a non-adaptive heuristic (uniform 2\\times 2 grid crop tiling) under identical visual token and inference limits. | Measures the true marginal value of learned agent decisions over static vision pipelines. |
| **Tool-Output Advantage** | **Oracle vs. Model Crop Parameters** | Evaluates final answer accuracy when the model is provided ground-truth crop coordinates versus its own predicted bounding boxes. | Decouples spatial localization failure from downstream visual interpretation failure. |
| **Evaluator Variance** | **Deterministic Closed-Set Filtering** | Restricts primary benchmarks to multiple-choice or exact-match string/numerical tasks, eliminating LLM judges. | Ensures performance measurements reflect true task correctness rather than evaluator instability. |

## **8\. Candidate Research Questions That Survive**

Applying the prior-art occupation test and confound analysis yields four candidate research questions that survive academic scrutiny. Each candidate is paired with the specific empirical observation that distinguishes it from prior art.

### **Candidate RQ 1: Disentangling Visual Evidence Acquisition from Test-Time Compute in Multimodal Tool Use**

> * **Core Question**: To what extent do reported accuracy gains from active visual tools (crop, zoom) reflect genuine visual information acquisition versus inference-token compute expansion, and does a learned pre-call policy outperform compute-matched text self-refinement?  
> * **Closest Prior Work**: AdaTooler-V, ToolGate, MED.  
> * **Why Not Already Answered?**: AdaTooler-V and ToolGate compare tool agents against direct single-pass answering. They do not evaluate compute-matched direct baselines (giving the direct model identical token budgets and forward passes) or masked-observation counterfactuals.  
> * **Distinguishing Empirical Observation**: If a direct-answer VLM with matched CoT tokens recovers at least 70% of the performance gain of a tool-using agent on fine-grained VQA, the claimed active perception gain is primarily a test-time reasoning artifact.  
> * **Strongest Invalidation Risk**: If visual tools provide massive gains on tiny-object tasks that text reasoning mathematically cannot solve (e.g., illegible 4-pixel text), the compute confound may be minor on high-resolution benchmarks.  
> * **Required Control**: Compute-matched direct inference, masked tool returns, and irrelevant crop interventions.  
> * **Feasibility**: High (Turnkey) on Colab Pro using frozen Qwen2.5-VL-7B and ActiView.

### **Candidate RQ 2: Cross-Model Fragility of Tool Necessity: Are Tool-Use Policies Model-Relative or Information-Relative?**

> * **Core Question**: Do tool-necessity and tool-utility gating policies trained on one vision-language model transfer to architecturally distinct or larger models, or do they merely encode the idiosyncratic perceptual weaknesses of the training backbone?  
> * **Closest Prior Work**: AdaTooler-V (uses Qwen2.5-VL-72B for offline \\Delta S scoring); ToolGate (evaluates cross-domain, but within the Qwen family).  
> * **Why Not Already Answered?**: Existing work assumes a universal tool benefit label \\Delta S. No study has systematically evaluated whether \\Delta S^{(M\_1)} correlates with \\Delta S^{(M\_2)} across different model families (e.g., Qwen versus InternVL versus Gemini API).  
> * **Distinguishing Empirical Observation**: A gating classifier trained on Model M\_1's failure boundaries performs near random (F\_1 \\approx 0.5) when deployed on Model M\_2, proving that tool necessity cannot be treated as an invariant benchmark annotation.  
> * **Strongest Invalidation Risk**: If certain questions have fundamental physical information deficits (e.g., crop required because target is 10 pixels wide), necessity will correlate strongly across all models, confirming information-relative validity.  
> * **Required Control**: Evaluation across three distinct model families with differing native visual tokenizers and resolutions; comparison between sub-pixel tasks and semantic reasoning tasks.  
> * **Feasibility**: High on Colab Pro with low-cost commercial APIs (Gemini 1.5 Flash / GPT-4o-mini).

### **Candidate RQ 3: The Fixed-Policy Equivalence Boundary in Active Visual Perception**

> * **Core Question**: Under identical inference token and latency budgets, does an adaptive, learned tool-invocation agent outperform a deterministic static perception policy (multi-scale pyramid tiling) on high-resolution visual reasoning?  
> * **Closest Prior Work**: ActiView, CropVLM, V\*.  
> * **Why Not Already Answered?**: Active perception papers compare learned zoom/crop policies against uncropped single-image baselines. They routinely omit static, multi-scale image pyramid heuristics that apply deterministic crops without agentic decision overhead.  
> * **Distinguishing Empirical Observation**: A deterministic 2\\times 2 grid-crop workflow matches or exceeds the accuracy of an RL-trained or prompted agentic cropping policy while exhibiting lower latency and zero decision-failure modes.  
> * **Strongest Invalidation Risk**: On large, complex images where the informative region is localized in an arbitrary corner, uniform tiling causes combinatorial context explosion, allowing adaptive policies to dominate.  
> * **Required Control**: Strict matching of total visual tokens processed per image; comparison across object-scale spectra (large versus medium versus tiny targets).  
> * **Feasibility**: High on Colab Pro.

### **Candidate RQ 4: Cost-Aware Pre-Call Gating for Visual Perception Tools Under Real API Budget Regimes**

> * **Core Question**: Can a lightweight, training-free uncertainty router operating on base VLM logits and image metadata predict whether external visual tool execution (OCR, crop) will yield positive economic payoff under heterogeneous API pricing?  
> * **Closest Prior Work**: ToolGate, CAM-DF, SRICE.  
> * **Why Not Already Answered?**: CAM-DF is non-visual; ToolGate uses a trained neural classifier that requires multi-task trajectory fine-tuning; SRICE uses conformal prediction on tool outputs after execution, ignoring pre-call costs. A zero-training, pre-call uncertainty router tailored to multimodal costs remains unstudied.  
> * **Distinguishing Empirical Observation**: Logit entropy and semantic consistency across stochastic low-temperature rollouts reliably predict visual tool utility, achieving at least 85% of ToolGate's efficiency gains without requiring trajectory training.  
> * **Strongest Invalidation Risk**: VLM logit confidence on visual tasks is notoriously miscalibrated and poorly correlated with fine-grained perception errors.  
> * **Required Control**: Calibration curves (ECE), Brier scores, Risk-Coverage curves, and actual commercial API token/dollar cost accounting.  
> * **Feasibility**: High on Colab Pro.

## **9\. Hostile Reviewer Analysis**

The surviving research questions are analyzed below against arguments that a skeptical peer reviewer would raise to challenge their validity.

Regarding Candidate RQ 1 (Compute versus Perception Confound), a reviewer might argue that the compute confound is well known in natural language reasoning and demonstrating that additional tokens improve performance is trivial. While compute scaling is established in text LLMs, active perception literature in vision-language models rests on the claim that external tool execution provides visual capabilities that direct reasoning cannot achieve.

If a controlled experiment demonstrates that the majority of performance improvements attributed to visual tools can be recovered by allocating equivalent thinking tokens to the original uncropped image, it challenges the empirical foundation of the visual agent literature. A second objection might state that if an image contains text that is physically illegible at base resolution, no amount of text reasoning can decode it. This objection requires a methodological control: the experimental benchmark must be stratified into resolution-bound tasks, where information is below the image sampling rate, and reasoning-bound tasks, where objects are visible but require systematic visual inspection.

Regarding Candidate RQ 2 (Cross-Model Necessity Transfer), a reviewer might argue that larger models naturally require fewer tools than smaller models, making model dependency an obvious observation. The scientific value of Candidate RQ 2 does not rest on showing that larger models need fewer tools; it tests whether the ranking and relative utility of tool actions transfer across model families. If an agent trains a policy to predict tool necessity based on a smaller model's error boundary, deploying that policy on a stronger model could degrade performance by forcing unneeded tool calls.

A second objection might argue that benchmarks like ActiView curate images where even frontier models fail without tools, making cross-model differences negligible. To prevent this artifact, the evaluation must include standard VQA datasets alongside high-resolution benchmarks to assess the full difficulty spectrum.

Regarding Candidate RQ 3 (Fixed-Policy Equivalence), a reviewer might contend that comparing a learned agent against a uniform grid crop is an engineering baseline comparison rather than a conceptual contribution. In empirical computer vision, establishing that a simple, deterministic pipeline matches or outperforms an agentic reinforcement learning framework is a valuable scientific result. If an agentic policy cannot outperform uniform multi-scale cropping under matched token budgets, the agentic paradigm for active perception is falsified for that class of visual reasoning problems.

Regarding Candidate RQ 4 (Cost-Aware Logit Uncertainty Gating), a reviewer would note that ToolGate already introduced pre-call gating for visual tools, and CAM-DF solved cost-aware stopping, rendering Candidate RQ 4 an incremental combination. This objection invalidates any claim of algorithmic novelty. If pursued, Candidate RQ 4 cannot be framed as a novel method; it must be framed as an empirical comparison evaluating whether simple, training-free logit uncertainty heuristics can match the performance of trained controllers like ToolGate, saving practitioners from expensive trajectory collection.

## **10\. Feasibility / Turnkey Audit**

The surviving candidates are evaluated under undergraduate resource constraints: Google Colab Pro, limited local hardware, open datasets, and a modest API budget.

ActiView provides a turnkey evaluation testbed. The dataset contains 314 curated questions across 1,625 instances, accompanied by deterministic multiple-choice ground truth and spatial view annotations. Because scoring is deterministic, the benchmark requires no LLM-as-a-judge infrastructure. Complementing ActiView, a deterministic subset of TIR-Bench provides approximately 300 tasks evaluating cropping, rotation, and text extraction with exact short-string answers. Conversely, VisualToolBench and MMSearch-Plus are rejected: VisualToolBench relies on LLM-judge rubric evaluation, while MMSearch-Plus requires live web search APIs that introduce network latency, non-deterministic content drift, and escalating execution costs.

Open-weight model execution is turnkey using Qwen2.5-VL-7B-Instruct. Quantized 4-bit and 8-bit inference executes within 16GB to 24GB of VRAM on a Colab L4 or T4 instance, while unquantized FP16 inference runs on a Colab A100 (40GB). Baselines—comprising direct execution, compute-matched reasoning, uniform 2\\times 2 grid cropping, unconditional tool use, and oracle cropping—are implemented in native Python using standard libraries (PIL, OpenCV, transformers).

| Operational Parameter | Value | Estimation Basis | Audit Status |
| :---- | :---- | :---- | :---- |
| **Evaluation Benchmark Size** | 500 instances | 300 ActiView \+ 200 deterministic TIR-Bench tasks | **DESIGNED** |
| **Experimental Conditions** | 6 conditions | Direct, Compute-Matched, Always-Crop, Static 2\\times 2, Masked-Crop, Oracle | **DESIGNED** |
| **Total Model Forward Passes** | 3,000 passes | 500 samples \\times 6 conditions | **CALCULATED** |
| **Local Inference Time (Qwen2.5-VL-7B on A100)** | \~2.5 hours | \~3.0s per forward pass \\times 3,000 passes \\approx 9,000 seconds | **APPROXIMATE** |
| **Colab Compute Units Consumed** | \~15 compute units | Based on Colab Pro A100 consumption rates (\~6 units/hour) | **CALCULATED** |
| **Commercial API External Baseline (Gemini 1.5 Flash)** | 1,000 calls | 500 samples \\times 2 conditions (Direct vs. Tool) | **DESIGNED** |
| **Input Token Volume (Gemini API)** | \~1.5M tokens | 1,000 calls \\times \~1,500 tokens (image \+ prompt) | **CALCULATED** |
| **Output Token Volume (Gemini API)** | \~0.2M tokens | 1,000 calls \\times \~200 generation tokens | **CALCULATED** |
| **Gemini 1.5 Flash Pricing** | $0.075 / 1M input; $0.30 / 1M output | Official Google Cloud pricing schedules | **VERIFIED** |
| **Total Gemini API Cost** | **$0.17** | (1.5 \\times \\$0.075) \+ (0.2 \\times \\$0.30) \= \\$0.1125 \+ \\$0.060 | **CALCULATED** |
| **Commercial API Comparison (GPT-4o-mini)** | 1,000 calls | 500 samples \\times 2 conditions (Direct vs. Tool) | **DESIGNED** |
| **GPT-4o-mini Pricing** | $0.15 / 1M input; $0.60 / 1M output | Official OpenAI API pricing schedules | **VERIFIED** |
| **Total GPT-4o-mini API Cost** | **$0.35** | (1.5 \\times \\$0.15) \+ (0.2 \\times \\$0.60) \= \\$0.225 \+ \\$0.120 | **CALCULATED** |
| **Judge / Annotation Expenses** | **$0.00** | Strict adherence to deterministic exact match | **VERIFIED** |
| **Total Out-of-Pocket Cost** | **\< $15.00** | Base monthly Colab Pro subscription plus minimal API usage | **CALCULATED** |

The audit confirms that Candidate RQ 1 and Candidate RQ 3 are turnkey and feasible. The entire empirical evaluation can be completed on Google Colab Pro within a weekend at minimal cost, requiring no distributed GPU infrastructure.

## **11\. Comparison With Existing Fallback RQ1**

Candidate 2, formulated specifically as Candidate RQ 1 (Disentangling Visual Evidence from Test-Time Compute), is evaluated below against the verified fallback candidate (Fallback RQ1).

| Evaluation Dimension | Existing Fallback RQ1 | Candidate 2 (Formulated as Candidate RQ 1\) | Comparative Trade-off Assessment |
| :---- | :---- | :---- | :---- |
| **Literature Gap Confidence** | High (Pre-verified gap) | Medium-High (As an empirical confound audit) | Fallback RQ1 has an established gap; Candidate 2 is viable only if framed as a critical audit rather than a novel system. |
| **Prior-Art Occupation Risk** | Low | Low (Narrowed audit scope) | Candidate 2 avoids occupation by auditing AdaTooler-V and ToolGate rather than proposing an alternative agent. |
| **Benchmark Maturity** | High | High | ActiView and TIR-Bench subsets provide stable, closed-set evaluations. |
| **Baseline Maturity** | High | High | Direct VLM, static cropping, and prompted agent baselines are standardized. |
| **Experimental Simplicity** | High | High | Relies entirely on forward inference and logit recording; requires no model training. |
| **Confound Risk** | Low / Controlled | Medium | Candidate 2 investigates confounds directly, requiring strict token matching. |
| **Reproducibility** | High | Very High | Deterministic code execution, open weights (Qwen2.5-VL), and public datasets. |
| **Compute Burden** | Low | Extremely Low | Less than 3 hours on a single Colab A100 GPU; total cost under $15.00. |
| **Career / Industry Relevance** | High | Very High | Test-time compute scaling and vision agent deployment efficiency are prominent industry priorities. |
| **Academic Contribution** | Constructive / Algorithmic | Critical / Diagnostic Measurement | Candidate 2 provides an empirical audit that challenges over-claimed agent capabilities. |
| **Value of Negative Results** | High | Very High | If visual tools provide substantial gains after compute controls, the visual agent paradigm is validated. |
|  | **Implementation Risk** | Low | Low |
| **Publication Defensibility** | Solid | High (Target: EMNLP / CVPR Workshop / Findings) | Rigorous measurement and diagnostic papers are well received at major AI conferences. |

Candidate 2 does not justify immediately discarding Fallback RQ1. Fallback RQ1 remains the safer choice because its gap is pre-verified and carries no occupation baggage. Candidate 2 should be held in reserve while a 48-hour pilot experiment is conducted on Candidate RQ 1 to determine whether the compute confound accounts for a meaningful fraction (\\ge 25\\%) of the performance delta on ActiView. If the pilot confirms that text-only compute matching recovers a substantial portion of visual tool gains, Candidate 2 becomes a high-impact diagnostic paper that justifies replacing Fallback RQ1.

## **12\. Final Research Status**

The final classification for each candidate research question is detailed below, paired with its primary supporting evidence, counter-evidence, and next verification step.

| Candidate Research Question | Audit Status | Primary Supporting Evidence | Primary Opposing Evidence | Unresolved Uncertainty | Single Most Critical Next Verification Action |
| :---- | :---- | :---- | :---- | :---- | :---- |
| **Candidate RQ 1** (Visual Evidence vs. Compute Confound) | **PROCEED TO DEEP AUDIT** | Major publications (AdaTooler-V, NTEP-R, ToolGate) do not control for token-matched text reasoning. | Reviewers may argue that compute scaling is already well established in natural language processing. | The exact magnitude of the compute confound on sub-pixel visual perception tasks. | Execute a 50-sample pilot on ActiView comparing direct VLM inference with matched CoT length against crop-augmented VLM inference. |
| **Candidate RQ 2** (Cross-Model Fragility of Tool Necessity) | **RESERVE** | Tool benefit is universally labeled using a single reference model (e.g., Qwen-72B in AdaTooler-V). | May degenerate into the trivial observation that smaller models fail more often than larger models. | Whether the relative utility ranking of candidate visual tools transfers across model architectures. | Calculate the Spearman rank correlation of sample-level \\Delta S between Qwen2.5-VL-7B and Gemini-1.5-Flash across 100 benchmark queries. |
| **Candidate RQ 3** (Fixed-Policy Equivalence in Perception) | **PROCEED TO DEEP AUDIT** | Dynamic resolution and active perception literature rarely benchmarks against static uniform image pyramids. | On ultra-high-resolution images, uniform tiling leads to combinatorial expansion of visual tokens. | The resolution threshold where adaptive cropping outperforms static tiling in FLOP efficiency. | Benchmark Qwen2.5-VL-7B on ActiView comparing a static 2\\times 2 grid crop against an adaptive zoom prompt under matched token budgets. |
| **Candidate RQ 4** (Cost-Aware Logit Uncertainty Gating) | **REJECT** | CAM-DF is text-only; training-free multimodal cost routers are conceptually straightforward. | Direct prior occupation: ToolGate already demonstrated token-efficient pre-call gating for visual tools. | Whether logit entropy correlates with fine-grained visual perception errors. | **REJECTED.** No further action required; prior art by ToolGate and CAM-DF is dense. |

The immediate verification action is to conduct a 48-hour pilot on Candidate RQ 1\. Download fifty sample instances from the public ActiView repository. Evaluate frozen Qwen2.5-VL-7B-Instruct across three conditions: standard direct answering, direct answering prompted with an explicit thinking budget matching tool-interaction token lengths (\~500 output tokens), and tool-augmented answering using ground-truth crop subviews. If the compute-matched direct condition closes more than thirty percent of the gap between direct answering and tool-assisted answering, the research gap is verified, methodologically defensible, and ready for execution.

#### **Works cited**

1\. AdaTooler-V: Adaptive Tool-Use for Images and Videos \- arXiv, https://arxiv.org/pdf/2512.16918 2\. Necessary Tool-Evidence Path Rewards for Agentic Vision ... \- arXiv, https://arxiv.org/abs/2609.03493 3\. ToolGate: Token-Efficient Pre-Call Control for Tool-Augmented, https://arxiv.org/html/2606.03054v1 4\. TACO: Tool-Augmented Credit Optimization for Agentic Tool Use, https://huggingface.co/papers/2606.30251 5\. Agentic video papers and benchmarks \- Scouts by Yutori, https://scouts.yutori.com/485790dc-de48-4f3f-b215-7f3d50e80d7d 6\. CYWang735/AdaTooler-V \- GitHub, https://github.com/CYWang735/AdaTooler-V 7\. \[2512.16918\] AdaTooler-V: Adaptive Tool-Use for Images and Videos, https://arxiv.org/abs/2512.16918 8\. Smarter Multimodal AI: AdaTooler-V Enables Efficient Image, https://quantumzeitgeist.com/ai-smarter-multimodal-adatooler-enables-efficient-image-video-problem/ 9\. Supercharging Multimodal LLMs with an Uncertainty-Aware Agentic, https://arxiv.org/abs/2503.08308 10\. LaTeX Guidelines for Author Response \- arXiv, https://arxiv.org/html/2503.08308v1 11\. Ranking Isn't a Stopping Rule: Three Papers on Knowing What You, https://arc0.me/blog/2026-07-31-ranking-isnt-a-stopping-rule-three-papers-on-knowing-what-you-dont-know/ 12\. Agentic Abstention: Do Agents Know When to Stop Instead of Act?, https://arxiv.org/abs/2606.28733 13\. Paper page \- Budget-Aware Tool-Use Enables Effective Agent Scaling, https://huggingface.co/papers/2511.17006 14\. VideoSeeker: Incentivizing Instance-level Video Understanding via, https://arxiv.org/html/2605.16079v1 15\. Daily Papers \- Hugging Face, https://huggingface.co/papers?q=Qwen3-VL%20backbone