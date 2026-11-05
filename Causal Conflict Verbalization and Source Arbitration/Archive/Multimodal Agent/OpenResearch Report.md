I verified the remaining anchors and found two more occupation-critical papers (see below). I now have everything needed to compile the audit.

Key new findings this round:

Thyme = arXiv:2508.11630 (I previously had it unverified at the wrong ID).
"What Does Vision Tool-Use RL Really Learn? (MED)" arXiv:2602.01334 — disentangles intrinsic vs tool-induced gains in crop-and-zoom RL; tool-contribution ratio only 0.30/0.22, >70% of learning comes from intrinsic capability. This directly occupies the credit-assignment gap the Illusion paper left open.
VTool-R1 (ICLR 2026), ToolVQA (2508.03284), MLLM-Tool (WACV 2025) — more occupation of "learn when/how to use visual tools."
ToolVLM's arXiv ID remains unverifiable; tool-use MMT-Bench paper not found — I will not cite either with an ID.
Candidate 2 Audit: Multimodal Agent Active Perception & Tool Selection
A. Executive verdict
This direction is saturated. Every component the candidate depends on now has 1–3 strong, recent (2025–2026) occupants with released code and real compute: (i) when to zoom is GapSight; (ii) why tool calls help or fail is "Illusion of Visual Tool-Use" and MED (2602.01334); (iii) rewarding tool use only when it helps is ToolVision, NTEP, Selective Tool Use, VTool-R1; (iv) whether a tool is even available matters is "When Tools Get in the Way"; (v) budget/stop control is ToolGate, StepPrune, Switch-Reasoner. The two gaps the community itself still names as open — inference-time gating/stopping and process-aware credit assignment — are either already attacked (MED, NTEP, StepPrune, ToolGate) or require SFT/RL infra you explicitly lack. The bundle you described in earlier turn under "Help?" (what the upstream/parent-agent turn is — I'm continuing with the exact spec that was stated in the prior audit scaffolding, i.e., not reducing to "attach tools and report accuracy") survives, but only as an incremental, mostly-occupied micro-slot whose realistic Colab contribution is a thin delta.

Final classification: REJECT (broad form); see K for the single narrow RESERVE alternative and why the fallback remains the stronger play.

B. Landscape map
Three clusters, all active 2025–2026:

End-to-end "learn to act on images" models (SFT/RL, code-based tool loops): Thyme 2508.11630; DeepEyes (ICLR'26); Pixel Reasoner (NeurIPS'25); VTool-R1 (ICLR'26); VISTA-R1 (2511.19773); ToolVision 2608.08907; Selective Tool Use 2609.14523; "Reinforcing VLMs to Use Tools…" 2506.14821. All require training budgets beyond Colab.
Free or light-weight controllers/actually-launched gating works:* GapSight 2608.21762 (frozen VLM, router); ToolGate 2606.03054; StepPrune 2609.13804; Switch-Reasoner 2607.08572; Dynamo 2606.30185; AdaptVision (2512.03794); PRISMS 2608.00218; steering 2608.25198.
Diagnostic / causal audits (released code, near-zero training): Illusion of Visual Tool-Use 2608.06270; MED 2602.01334; Spurious Tool Use 2609.16268; When Tools Get in the Way 2609.14157; CoBRA 2609.00967.
Closest incident for your constraints (no pretraining, no multi-GPU): cluster 3 diagnostics + cluster 2 frozen-VLM inference gates. Both are occupied but their code is your fastest reuse surface.

C. Closest-work matrix
Any new claim must be compared against these; unevaluated-deliverable losses ↓.

Work (year, arXiv)	Claim they own	Evidence (quotation/anchor)	Confidence	Limitation / what a thesis could still add
Illusion of Visual Tool-Use (2026, 2608.06270)	Tool calls help only via a "Calibrated" minority; 70.7% Mode-1 "call without looking"; VEG step-level audit	"Qwen3-VL-8B: +7.6 pp from 'Calibrated' subset (f=20.9%, +36.2 pp each)… 70.7% Mode 1"; LLM judge Qwen3-30B; code released	HIGH (read full text)	They leave open inference-time gating/stopping, process-aware credit assignment, matched training varying only reward signal — but MED (2602.01334) already does the reward-variation part
MED "What Does Vision Tool-Use RL Really Learn?" (2026, 2602.01334)	In crop-and-zoom RL, most gain is intrinsic, not tool-induced; RL reduces tool-induced harm rather than mastering tools	"tool contribution ratio 
S
t
o
o
l
S 
tool
​
 =0.30 (Qwen2.5-VL) and 0.22 (Qwen3-VL); >70% of learning progress from intrinsic capability"	MED/HIGH (HTML text read)	Crop-and-zoom only, outcome-only reward; no reward-signal ablation
GapSight "Learning to Look Again" (2026, 2608.21762)	When-to-zoom routing with loss-gap supervision, frozen VLM	"InternVL2.5-8B 52.25→64.29 avg over 6 benchmarks; review rate 74% (TextVQA) vs 25.6% (MME-Lite)"	HIGH	Router-trained; no tool-necessity/cost axis; 2D crop only
OpenVisTool 2608.08557	Causal-utility (with-vs-without-tool probe avg@4) filtering; cross-domain collapse of Thyme/DeepEyes V2	"GPT-5.5: 41.9 no-tool / 49.0 tool-aug"; 296,993 calls; 559-bench	HIGH (full text)	Bench+dataset release announced, not yet confirmed
ToolVision 2608.08907	Reward tool use only when tools clearly improve (SFT+RL, 7 benchmarks)	uses min LLM-judge usage	MED (abstract)	SFT/RL infra
NTEP 2609.03493	Necessary-tool-evidence path rewards + redundancy penalty	"reward tool calls only on necessary evidence paths"	MED (abstract)	RL infra; pathway annotations
Selective Tool Use (change VQA) 2609.14523	Reference-map/no-reference routing for agentic change VQA	"73.77→88.79 (reference maps); 77.47 predicted"	MED (abstract)	Single task; LoRA (Colab-possible!)
When Tools Get in the Way 2609.14157	Availability of unnecessary tool degrades answers 98.2%→63.5%; instruction fix		MED (abstract)	LLM/VLM text-scope, prompting fix
ToolGate 2606.03054	Pre-call execute/skip gating controller	"helpful calls 11.8% vs harmful 9.9%; token cost ↓64–69%"	MED (abstract)	External controller
StepPrune 2609.13804	STOP-token adaptive visual-token selection		MED (abstract)	Token-level, not tool-level
VTool-R1 (ICLR'26) "VLMs Learn to Think with Images"	Interleaved visual-step tool use via RFT	"ReFOCUS-TableVQA 64.7→71.7 (7B)"; Qwen2.5-VL 3B/7B/32B	HIGH	Tables/charts only; RL infra
Thyme 2508.11630 (corrected ID)	SFT(500K)+RL(GRPO-ATS) code-based image ops; ~200 GPU-hr SFT	"perception +27.14% / reasoning +81.57% (monitoring)"	HIGH	Requires GPU-hours + RL data collection
ToolVQA 2508.03284	23K-sample multi-step tool VQA; FT LLaVA-7B beat GPT-3.5-Turbo on 5 OOD	"noise introduced by tool usage can outweigh the benefits"	MED	Dataset; domain narrow
When Should Active RAG Retrieve? 2607.24010	Budget-aware retrieval routing (text analog)		MED (abstract)	Text-only; VLM analog open
Deliberately excluded (not numerated): ToolVLM and MMT-Bench-tool-use — IDs unverifiable across alphaXiv+web searches (ToolVLM ≠ MLLM-Tool ≠ ToolVQA); do not cite by ID. Multitask MMT-Bench (2404.16006, ICML'24) is the 31,325-Q AGI benchmark and is not the tool-use MMT-Bench.

D. Benchmark / environment audit
Candidate eval	Automation of success metric	Fit	Verdict
OpenVisTool-Bench (559, 5 domains, GT tool trajectories)	reuse probe avg@4 / outcome-validity	native sibling eval for your causal RQ	MODERATE — announce-not-yet-release; watch repo
VTC-Bench 2603.15030 (680 probs, 32 OpenCV tools, GT trajectories)	exact-match over GT tool sequences	ideal for "call right/wrong"	MODERATE — verify release
V* (2312.14135) + HR-Bench 4K/8K + VisualProbe E/M/H + MME-RealWorld-Lite	exact/LLM-judge	Illusion-paper partitions, code+judge released	MODERATE — heavy; judge-LLM (Qwen3-30B) needs API or local vruntime
CDVQA extension 2609.14523	answerability split w/ deterministic change-analysis tool	single-task, low API	MODERATE
DocVQA/TextVQA/ChartQA/InfographicVQA	VQA acc	GapSight's set, trivial APIs	TURNKEY — acquisition easy, but every gain here already claimed by GapSight
Open"call/help/hurt" meter (your own re-metric on HR-Bench-VisualProbe samples)	you author; grounded in VEG/logit audits	the only new surfaces candidate could offer	MODERATE — but the meter itself is Illusion-paper derivative
VizWiz answerability (1802.08218; VT 2609.16565)	answerability AP	2018 data; VT-Transformer already regresses it	BLOCKED for novelty; strong for a replicability exercise
SFT/RL training for any new policy	n/a	violates Colab/no-multi-GPU	BLOCKED
E. Gap destruction
New contribution = "build VLM agent with tools and show accuracy" — eliminated 2023 (LLaVA-Plus / Sketchpad) and, in every 2025–26 variant above, by Thyme, VTool-R1, GapSight.
"When to look / zoom" — eliminated Jan–Sep 2026 by GapSight.
"When do tool calls help" — eliminated 2026 by Illusion + MED (with released code and judge).
"Weight tools only when they help" — eliminated 2026 by ToolVision, NTEP, Selective-Tool-Use, VTool-R1.
"Tool availability alone changes behavior" — eliminated 2026 by When-Tools-Get-in-the-Way (your "get-out-of-the-way" instinct is a done paper).
"Budget-aware / stop control" — eliminated by ToolGate, StepPrune, Switch-Reasoner, Active-RAG analog.
Surviving slivers: (a) only the combination (few domain, drop-ToolGate-controls, prize = causal VEG≥0 subset accuracy vs cost Pareto) in a clean two-arm matched study at inference-only on OpenVisTool-Bench — but the Illusion paper already reports a VEG-correlated calibrated minority; (b) process-level credit assignment on public GT-trace data — but requires a training loop (NTEP-adjacent), which you banned, or a control-theoretic gate no one has yet built on open logs; both are fast-moving, infra-rich lanes.
F. Candidate RQs (max 3) — condition → intervention → outcome → comparison → setting
RQ-A (inference-only, causal gating): Given measure-tool-gating VEG≥0 (Visual Evidence Gain) as the stop/execute controller on frozen VLMs → what is the accuracy-vs-token budget Pareto of VEG-threshold gating vs GapSight's router and ToolGate's controller → on OpenVisTool-Bench + VTC-Bench, only public/open-weight APIs (no training).
RQ-B (availability effect): Does silencing unnecessary tool availability recover % answer rate without accuracy loss on HR-Bench-4K/8K and DocVQA → measure answer-rate/accuracy/evidence, using the 2609.14157 instruction as the intervention, on open-weight VLMs alone.
RQ-C (deferred/training): Does process-aware credit assignment (necessary-tool-evidence rewards, NTEP-style) transfer to change-VQA routing (2609.14523-style) under matched rewards-only-vruns, i.e., vary only reward signal, identical data/optimizer — a direct test of the Illusion paper's stated open problem.Requires training; keep as the "if compute becomes available" reserve lane.
G. Minimal experiments
RQ-A: 6 open VLMs × 2 benches × {VEG-threshold ∈ {0, .1, .25}} — ~0 GPU training; estimate ≤3–5 API-hr-equivalents + judge LLM bills.
RQ-B: 4 VLMs × 2 benches × {no-tool / tool-available / silenced} — pure inference, ~1 API-weekend, no training.
RQ-C: 1 LoRA (Qwen3.5-4B, 2609.14523's setup) with only the reward signal toggled — the single artifact that would differentiate from all above; cost = single-GPU fine-tune ×3, likely Colab-boundary.
H. Plug-and-play scoring (/5)
Dimension	RQ-A	RQ-B	RQ-C
Dataset	4 (OpenVisTool-Bench pending)	4 (Illusion partitions public)	3 (CDVQA ext)
Baseline	3 (GapSight, ToolGate)	5 (no-tool)	3 (NTEP, Selective)
Environment	5 (inference-only)	5	2 (needs train)
Colab	5	5	1–2
API	4 (judge LLM needed)	5	3
Eval	4 (GT GT-eval / VEG)	4	4
Reproducibility	4 (uses released code)	5	2 (heavier)
RQ-A/B are short-shot confirmations; their delta value is thin because the parent works already report the same decompositions. RQ-C is the only differentiating lane and it is the least Colab-fit.

I. Kill risks (hostile Q-list)
"The Illusion paper's VEG≥0 is your gate." → Reuse of released code kills RQ-A unless VEG-threshold Pareto is genuinely novel and measurably better on token budget — my read: likely a marginal delta.
"2609.14157 is your RQ-B." → Yes, it is; you'd be replicating an existing abstract-only paper.
"NTEP + VTool-R1 + Thyme already do reward engineering" → Kills RQ-C's novelty claim at the review table unless matched-only-reward-variation is a rigorous ablation they did not run — MED's study suggests you'd then likely reproduce their conclude-intrinsic-not-tool finding rather than overturn it.
"Compute/leakage": open benchmarks releases (OpenVisTool) may change their splits mid-thesis.
"No more headroom on the interesting axis at Colab scale."
J. Comparison with fallback (Surviving RQ 1)
Dimensions below are descriptive, not a rank.

Dimension	Candidate 2 (best lane RQ-A/B)	Surviving RQ 1 (fallback)
Concrete failure mode	Tool calls that don't help; availability harm	(defined in prior audit, has a crisper failure anchor)
Precision of RQ	Medium (occupiers abound)	High
Compute fit	High (inference) / Low (differentiating RQ-C)	Match
Anti-occupation	Weak — every component has a 2026 paper	Strong (fallback lane was pre-audited clear)
Meaningful negative-result capacity	Medium (negatives plausible but not surprising)	Higher
K. Final classification
REJECT Candidate 2 in both broad and RQ-A/B forms. The landscape is not only occupied but internally coherent: audits (Illusion, MED, Spurious Tool Use) already answer the causal "help-vs-harm" question that was this candidate's best hook, and the controllers (GapSight, ToolGate, StepPrune) claim the gating surfaces. The remaining differentiate-able lane (RQ-C: matched reward-only variation) cannot be honorably executed under Colab/no-multi-GPU/frozen-VLM constraints, and even with compute, MED's direction suggests a confirming negative is the likely result. Recommend proceeding with the Surviving RQ 1 fallback; keep RQ-C only as a conditional reserve lane if GPU training budget materializes and the two announced releases (OpenVisTool-Bench, VTC-Bench) land before proposal lock.