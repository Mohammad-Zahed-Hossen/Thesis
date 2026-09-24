# ⁨Thesis⁩ — OpenResearch

*Exported 9/21/2026, 1:58:30 PM*

---

I'll start by loading the relevant skills and mapping out this large multi-workstream task.

Project is fresh. Now let me verify the anchor papers exist and read them. Starting with the four anchors plus the two Candidate-B papers.

Both A1 and A2 are real and present in alphaXiv. Let me pull full texts for all four anchors plus the two Candidate-B refutations, saving them to temp files for careful reading.

All six papers verified as real. Now reading each in depth.

A1 fully read — highly relevant. Now A2 (VIG).

Let me finish reading VIG (appendices F, G) and then read C1.

A2 fully read. Now C1 (Grounding IDs).

Let me read the remainder of C1 (appendices).

C1 fully read — the closest-work implications are major. Now C2.

C2 fully read. Candidate-B papers confirmed real, but deprioritized by the user — quick verification of their titles/claims only.

Candidate-B refutation confirmed — deprioritization is well-founded. Now running the discovery loops for Q1 and Q2 gap autopsies.

Q1 loop produced dense 2026 hits. Now the Q2 discovery loop.

Reading next Q1 candidates.

Reading remaining Q1 candidates (CoT faithfulness, attention, grounding).

Reading the last five Q1 candidates.

Reading the final three Q1 candidates.

Compiling the Q1 autopsy. Let me check the repo for the original task framing (Q1-A..G, Q2-A..H enumeration).

Repo is empty (no prior notes). Continuing with Q2 discovery + pre-emption scans using refined terms.

Q2 search surfaced a rich, non-anchor literature on binding. Fetching the most load-bearing candidates for verification.

The search JSON dumps are too noisy. Let me parse them properly.

Two more highly relevant Q2 hits: `2608.00726` (Foveated Probes — localized binding info in vision foundation models) and `2605.25427` (Point by Point). Fetching heads, plus running the 2026 pre-emption scan for Q1 and Q2.

Q2 discovery and verification is now thorough. Summary of what the session established:

**Verified Q2 claims (with control/quality notes):**
- **Dual Mechanisms** (2603.22278, Cui et al., MIT/Northeastern/Sony): models confirmed Qwen2-VL-7B-Instruct + Gemma-3-4b-it (Qwen2-VL-2B for intervention on hard subset); datasets Squares/Shapes/Objects + What'sUp natural control subset (2,687 images) + COCO-spatial. Spatial signal is global across visual tokens incl. background; stripping ordering info from vision embeddings drops accuracy to 0.43–0.64 (both major VLM families — supports universality *within* architecture axes). **Has a random-amplification control**: Gemma 0.53 → 0.72 (40.2%), random amp only 0.57 (9.6%); Qwen 0.60 → 0.82 (54.5%), random 0.65 (13.1%).
- **Formalizing the Binding Problem** (2606.03976, Huang et al./Kording): info-theoretic definition; [CLS] token encodes <half of scene binding info, largely quadratic structure; spatial tokens encode it near-perfectly, decodable via simplified attention probe. Natural + synthetic binding-challenge datasets.
- **Point by Point** (2605.25427, Princeton/Mila): pointing-via-text induces internal visual search routine; fine-tuning to point eliminates binding errors and yields compositional generalization — serial processing as the human-style solution.
- **Foveated Probes** (2608.00726, Rice/Queensland): global-embedding readout is the bottleneck, not missing spatial info; foveated/question-conditioned readouts recover oracle-level localized binding accuracy on GQA natural images + synthetic clutter.
- Plus earlier-verified: **Limits in Dual Encoders** (Lo, UCL), **VISER** (Sharif = C1's own group), **Fragile Multilingual** (Chakraborty), **Seeing to Generalize** (Buzeta), **DSCAM/InstaBind-Lite** (Xu).

**2026 pre-emption scan: no direct pre-emption found.** Top hits for Q1 (2609.12606 geometry CoT, 2608.27265 SCIT, 2609.09928 process supervision) and Q2 (2609.18345 framing, 2608.11024 attribute hallucination) are adjacent but none runs the causal matched-control with trace-length as IV that defines Q1, nor tests a binding-ID mechanism on natural images across architectures as Q2 does.

**Blocking item before I write the report.** The exact texts of the Q1-A..G (7 axes) and Q2-A..H (8 axes) antithesis questions were in earlier session transcripts that are no longer accessible. My reconstructed Q2-A..H is:

- A: does binding rely on a universal mechanism across VLM architectures, or is it architecture-specific?
- B: does it generalize from synthetic geometric scenes to natural images?
- C: is it a genuine mechanism rather than an artifact (random-vector placebo, scramble controls)?
- D: is it causal (intervention changes output), not just correlational probing?
- E: can alternative explanations (attention-only, spatial shortcuts, modality-gap stats, hallucination) account for it?
- F: is it position-independent within a model (universality across token positions)?
- G: does it require cue/symbol framing (binding ID as symbol) to function?
- H: does it reduce to a simpler statistic (e.g., nearest-neighbor feature overlap)?

**Can you confirm/correct Q2-A..H and paste the exact Q1-A..G texts?** Once I have them I'll tag all claims, run the dataset/model/protocol/Colab audits, and write the 16-section report.

---

Phase-2 audit complete. Report written to <file path="artifacts/phase2/phase2-report.md" />.

**Headline verdicts:**
- **Q1 (primary): ALIVE.** Verified against all 11 candidate papers — none runs trace-length as a causal IV with position/context/denominator held fixed. No 2026 pre-emption found. Feasible on 16 GB Colab.
- **Q2 (secondary): ALIVE but contested.** The anchors are *not* isolated — 9 verified 2025–26 papers attack VLM binding (dual mechanisms with random-amp baselines, point-by-point serial search, foveated readouts, DSCAM dense benchmark, dual-encoder limit theorems). The specific "cross-family linear Binding ID subspace, natural-image, placebo-controlled" niche is still open, but K4–K7 gate commitment.
- Both protocols are designed; 8 kill tests (K1–K8) defined, all REQUIRES RUNTIME TEST.

The only remaining work is the Phase-2 Colab pilot to run the eight kill tests before committing to either thesis.

---

I'll start by locating the authoritative input files and auditing the environment before touching any code.

GPUs: none here (no nvidia-smi). 4 of the 5 required input files are missing from artifacts — let me search the whole user profile before concluding, and read the existing report.

Only 1 of 5 required files exists on this machine: `phase2-report.md` (found in `files\thesis\phase2\`). Missing: `Plan.md`, `Multimodal AI Thesis Feasibility Audit (Phase 2).md`, `Phase2 AlphaXiV Report.md`, `Canonical_Thesis_Topic_Specification.md` (the only `PLAN.md` on disk is an unrelated Wix-plugin file). I will not silently reconstruct them.

Let me set up the tracking and start the pre-flight checks that don't need a GPU.

No transformers/torch installed; disk fine (78.8 GB free). Let me verify architecture facts via the official model config (Tier-1, zero download) and verify datasets, in parallel.

Critical Phase-3 find: **RH-Bench (2505.21523, NeurIPS 2025, "More Thinking, Less Seeing?")** is a direct, published attack on Q1's core claim — it manipulates reasoning length (latent-state steering, budget forcing), measures visual attention decline and hallucination, and releases length-control code (github.com/MLRM-Halu/MLRM-Halu, HF `LCZZZZ/RH-Bench`). **InstaBind-Lite/DSCAM is verified public** (github.com/InstaBind-Lite/InstaBind-Lite; 524 imgs/529 groups/1,773 instances/9,580 questions; **boxes included = clean intervention targets**). Config for Qwen2.5-VL-3B verified: 36 layers, hidden 2048, 2 KV heads, mrope, vision 32-layer ViT (patch 14, merge 2).

WhatIfVis did not appear in search — verifying the real dataset name, and starting the model stack install in parallel.

Torch (CPU) installed. WhatIf search came up empty for an official "WhatIfVis" — checking paper text for dataset provenance/availability, reading C1's method section, and installing transformers in parallel.

Verified from text: **WhatIfVis is an A1-derived benchmark** (3,049 samples) rebuilt from public sources (`VLind-Bench`, `Pixels-versus-Priors`, + 67 generated balance-scale items); response-template-constrained eval; A1 eval'd on Qwen2.5-VL 3B/7B — download availability unconfirmed in the paper → Q1 dataset must be **reconstructed from documented public sources**. **C1 intervention clarified** (from 2509.24072): ICG (eq. 3) is the *alignment metric*; the *causal intervention* is **activation patching** of row-partition tokens between source/target grids on Qwen2.5-VL-7B with non-ordinal row symbols {&,$,#,@}.

Now the CPU pre-flight: checking transformers version and starting the model download.

7.5 GB model downloaded in ~10 min. Running the CPU pre-flight (architecture/hooks/attention extraction) now.

Model loads (3.755B params, 7.51 GB bf16 weights). Fixing the config attribute access for transformers 5.x (text_config nested) and re-running.

Processor needs the `<image>` placeholder in the text. Fixing and re-running.

The 5.x placeholder is `<|image_pad|>`, not `<image>`. Fixing.

Attention weights ARE exposed under eager attention (36×[1,16,70,70]), hidden states 37×[1,70,2048]. Note: image tokens arrive via 64 `<|image_pad|>`; vision_start/end are injected inside the model forward (not in input_ids) — critical for correct K-position mapping in the real harness. Fixing the layer-attribution for hooks.

Pre-flight complete: attention weights exposed under eager (verified), residual-stream hooks work at `model.model.language_model.layers[18]` (verified), stable greedy generation (verified; described image correctly), CPU ≈7.4 s/token (too slow for full pilot → GPU needed). Now finalizing the remaining audits and writing artifacts. Grabbing Gemma-3-4B-IT config (Q2-A secondary) as Tier-1 evidence.

Gemma-3-4b-it returns 401 (gated; requires HF login + license). Quick check whether it's even multimodal (relevant to Q2-A cross-architecture choice) while I start writing artifacts.

Gemma-3-4B-IT IS multimodal (SigLIP, 256 image tokens) but gated. That's Q2-A-relevant. Before writing artifacts, loading the reports skill per project convention.

Artifacts live under `...\files\thesis\` with `phase2/` present. Creating `phase3/` deliverables: preregistration lock, pilot harness, and the Phase-3 report.

Now the Colab-ready pilot harness (reconstructive, pre-registered).

Write failed (content too long). Rewriting the harness more compactly.

Core library written. Now wiring a delegated stage runner and removing the dead stubs.

Adding a fast `--tiny` smoke path (shortened prompts) so I can validate plumbing on CPU without the full-trace generation cost.

Compile-checking both files, then running a tiny CPU smoke to validate the full plumbing.

Q1 pipeline runs end-to-end on CPU. Two fixes: (1) empty takeover rows must short-circuit the patch hook; (2) correctness parse must accept number words ("three" not "3").

Q2 skipped: predicted "?" — symbol tokens not in the top-8 logits and symbols may be untokenizable/unreadable. Checking tokenizer IDs and fixing the answer scoring to score the 8-symbol answer space directly (plus a larger font).

The venv vanished. Checking what remains in the temp opencode directory.

The entire temp env (venv + 7.5 GB model cache) was wiped between runs — environmental reset, not a code issue. The deliverables in the artifacts dir are what matter. Applying the Q2 robustness fixes (score symbol-ID space directly, larger grid font), then deleting the smoke checkbox CSV so the real GPU run computes all 50 samples cleanly.

Now the Phase-3 report (main deliverable). Writing in two parts to stay within write limits.

Verifying the final files compile and exist, then wrapping up.

Phase 3 deliverables complete. Summary:

- **Phase-3 report** (18 sections, per your §34 spec): `<file path="artifacts/phase3/phase3-report.md" />`
- **Pre-registration lock** (before any measurement): `<file path="artifacts/phase3/preregistration.md" />`
- **Pilot harness** (runtime-verified pieces + pre-registered stages): `<file path="artifacts/phase3/pilot_harness.py" />` and `<file path="artifacts/phase3/pilot_run.py" />`

Headline findings:
- **Required files**: 4 of 5 missing (only `<file path="artifacts/phase2/phase2-report.md" />` present); they're reported, not reconstructed. K7 was recovered from the phase-2 report (it was specified there, not missing).
- **Q1 pre-empted, not killed**: RH-Bench (arXiv:2505.21523) already did VLM length-control and found more reasoning → more hallucination. Q1 reframed as **mechanistic decomposition** (position/content/dilution/causal-availability) layered on RH-Bench's tooling — verdict SURVIVES WITH MODIFICATION, UNCERTAIN.
- **Q2**: artifact risk is real (C1 nearly pre-empts it in synthetic scenes); gates K4/K5/K7 are now the deciders — verdict SURVIVES, UNCERTAIN, conditional on those.
- **Validity audit**: every K1–K8 criterion repaired and logged (e.g., K2's "normalized VIG" was underspecified → derived M/N dilution null + slope test; K1's single gate → two TOST-equivalence contrasts; K3 split into probe/steering).
- **Runtime**: attention extraction (eager), residual-stream hooks, and generation are verified working on the downloaded model; Qwen2.5-VL's quirky `<|image_pad|>` placeholder is handled. CPU is 7.4 s/token → **all K-measurements need your Colab 16 GB**; the smoke run also surfaced an answer-parse fix (symbol answer-space scoring) already applied.
- **Entry gate**: DO NOT PROCEED — ADDITIONAL PHASE 3 TEST REQUIRED (run `--smoke` then `--stage q1/q2` in the harness).

One note: the local temp venv + 7.5 GB model cache were wiped by the environment mid-session; that only affects re-running locally (not needed — the pilot is GPU-bound anyway).