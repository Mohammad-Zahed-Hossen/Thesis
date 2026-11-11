# Cloud GPU Platform Evaluation for v5 on a $10–15/month Budget

> **AI-generated (Claude, 2026-11-11). Reference only, not ground truth.** Prices were checked on the web on 2026-11-11 and drift over time; treat them as ±20%. Check the claims tagged [Inferred] or [Unknown] before you rely on them. This replaces the recommendation in `../Thesis Cloude Compute Evaluation.md`, which assumed a $50/month budget and chose RunPod Secure.

## 1. Executive verdict

**Use Colab Pro ($9.99/mo) or Colab Pay-As-You-Go, pin the L4, and run every v5 model × regime on it.** Keep RunPod Community Cloud as an occasional pay-per-hour backup for work that has to run unattended or needs more memory (LoRA, large activation caches), and keep each of those jobs entirely on one platform.

Two problems to fix before you rely on this:

- **The L4 does not meet the pre-registration as written.** [Verified, from a Colab-GPU table] The L4 exposes about **22.5 GB**, not 24 GB. Both prereg §3.4 and `Experiment/RUNBOOK_v5.md` say "at least 24 GB" and also list the L4, so the document contradicts itself. Before the freeze, change it to something like "≥ 22 GB; one named GPU model per model × regime". The runbook's 7B setting (`BS=2`, about 16.6 GB of weights) was planned with the L4 in mind, but you must confirm `peak_vram_gb` in the dev pass.
- **The harness does not check compute capability or VRAM.** [Verified] `harness_v5.HFBackend` only refuses any dtype other than bfloat16. On a T4 or V100 you are stopped indirectly, because the loader falls back to float16. If you want the hardware invariant enforced, add an explicit assert on `torch.cuda.get_device_capability() >= (8, 0)` and on the GPU name.

## 2. Cost and compute

Sources: Colab burn rates from a Colab GPU-pricing post (mccormickml.com, rates checked 2026-03-10); runpod.io/pricing plus northflank.com and flexprice.io roundups; vast.ai/pricing (live median). All prices are approximate.

| Option | GPU (VRAM) | $/GPU-hour | GPU-hours per $10 | Idle or storage cost | Unattended runs? |
|---|---|---|---|---|---|
| **Colab Pro / PAYG, L4** | L4 (22.5 GB) | **~$0.17** (1.71 CU/h) | **~58 h** | $0. Drive holds the results; download the weights from HF each session | ❌ needs an open browser tab |
| Colab, A100 40 GB | A100 | ~$0.54 (5.4 CU/h) | ~18 h | $0 | ❌ |
| Colab, A100 80 GB | A100 | ~$0.75 (7.5 CU/h) | ~13 h | $0 | ❌ |
| RunPod Community | RTX 3090 (24 GB) | ~$0.22 | ~45 h | Pod disk ~$0.20/GB/mo while stopped. Network volumes are Secure-only, ~$0.07/GB/mo (40 GB ≈ $2.80/mo) | ✅ tmux |
| RunPod Community | RTX 4090 (24 GB) | ~$0.34 | ~29 h | same | ✅ |
| RunPod Secure | 3090 / 4090 | ~$0.50 / $0.59–0.89 | 11–20 h | same | ✅ |
| RunPod Community | A100 80 GB | ~$1.19 | ~8 h | same | ✅ |
| Vast.ai | RTX 3090 | $0.10–0.21 (median) | ~47 h at the median | Each host sets its own storage price, and it **keeps billing while stopped**. Delete the instance to stop it | ✅, but reliability varies by host |

**Colab Pro vs. Pay-As-You-Go:** both cost $9.99 for 100 compute units, so the GPU-hours are the same. [Inferred] PAYG fits this thesis better: you buy units only in months when you run something, and units on either plan expire after about 90 days. Pro's extras (priority, more memory) don't change anything for this workload. [Unknown] Whether terminal access differs between the two plans; check in the Colab UI.

**How long v5 takes: [Unknown].** The v4 manifests have no timing data, and nothing has run on v5. Prereg R8 already requires seconds per item in the dev pass. Time the 2B dev block first and scale from it before you buy more units.

## 3. Reproducibility and failure modes

| Invariant or risk | Colab (L4 pinned) | RunPod / Vast |
|---|---|---|
| **bfloat16** | ✅ L4 is compute capability 8.9; the harness enforces bf16 | ✅ 3090 (8.6) and 4090 (8.9) |
| **Same GPU model across stages** | ✅ if you select **L4** as the runtime type. [Inferred] Colab then gives you an L4 or nothing; it doesn't quietly swap in a T4. The real risk is **L4 not being available**, which means waiting. Never fall back to "any GPU". | ✅ You rent the GPU model by name. On Vast, the host (CPU, driver) changes between rentals |
| **Software determinism** | ⚠ Colab's base image (CUDA, driver, torch) changes without notice. Pin your pip versions (the runbook does: transformers 5.22.2, `pip_freeze.txt`). Record the driver and CUDA version per manifest; if they change mid-regime, note it. | ✅ You pick the container image tag |
| **Disconnects** | ⚠ No background execution on Pro or PAYG. Closing the tab or sleeping the laptop ends the session within minutes to about 90 minutes. There is a 24 h hard cap, and GPUs can be reclaimed when demand is high. The row-by-row `fsync` plus resume turns each disconnect into a loss of one batch plus a model reload (minutes), not a lost run. Annoying, not fatal. | ✅ tmux survives your laptop. On Community/Vast the host can be reclaimed or fail; the same resume logic covers it |
| **Drive I/O** | ✅ for JSONL: rows are a few KB, and a per-row fsync on the Drive mount is tiny next to a 512-token decode. ❌ for activations or weights: Drive is slow for large writes. [Inferred] fsync on Drive's FUSE mount doesn't guarantee the file has uploaded before a disconnect. Re-running with the same `--run_tag` and resume covers that gap. | n/a: local NVMe |

**Community reports:** these were not surveyed independently. The failure modes above are Colab's documented behaviour plus inference from it.

## 4. Execution protocol

**For v5 dev and confirmatory runs (Colab, L4):**

1. **Before buying anything:** finish everything you can on the CPU locally (runbook §1). Fix the prereg's "24 GB" wording and add the capability/GPU-name assert.
2. **Start the session:** Runtime → Change runtime type → **L4**. Check that `nvidia-smi` shows an L4; if not, disconnect immediately so you don't burn units.
3. **Install:** install pinned versions from a `requirements_v5.txt` on Drive. Download the weights from the HF Hub at the pinned revisions into `/content/hf_cache` (local disk, not Drive). For the 7B (~16.6 GB) this takes a few minutes per session, which is cheaper than paying for Drive storage.
4. **Results:** set `results_v5/` to a Drive path such as `/content/drive/MyDrive/thesis/results_v5` so resume survives a VM reset. Write `pip_freeze.txt` once per session, not just once overall, since the image can change.
5. **Keep the session alive:** keep the tab open in the foreground and stop the laptop from sleeping. Run the work as `!python harness_v5.py …` in a cell (or `nohup … &` from the terminal, then `tail -f` in a cell). After a disconnect, re-run the same command with the **same `--run_tag`**.
6. **Order to save units:** run the 2B first (fast, and it gives you the seconds-per-item figure), then 3B, then 7B. Run `--gates_only` and `--print_example` on the CPU locally or on a CPU-only Colab runtime, which costs almost no units.
7. **Stop billing:** use Runtime → Disconnect and delete runtime as soon as a stage finishes. An idle connected L4 still burns about 1.7 CU/h.
8. **Keep each model × regime on one platform:** never start a model × regime on Colab L4 and finish it on a RunPod 3090. If the L4 is unavailable for days, move a *whole* model × regime to RunPod and record it in the manifest.

**For later phases:**

- **Activation caching:** store only the token positions you need (for example the `####` boundary and the verdict span). One 7B position across all 28 layers is about 200 KB in bf16, so 1,000 items × 50 positions ≈ 10 GB. Write it to local disk as `.safetensors` and upload it compressed to a **private HF dataset repo**, not Drive. This works on a Colab L4 (the runtime has roughly 50 GB of system RAM [Inferred]).
- **Overnight unattended runs:** use RunPod Community with a 3090 or 4090 in tmux. Don't use a network volume. Download weights from HF on startup, push results to GitHub or HF, then **terminate** the pod rather than stopping it, so you pay $0 when idle.
- **LoRA on the 7B:** 22.5 GB is too tight. Rent a RunPod A100 80 GB (~$1.19/h) in short bursts, and budget for it in a separate month.

**Caveat:** Colab is the cheapest per hour, but it only works if you stay near the laptop. If v5 turns out to need more than about 15 hours per model, the convenience of RunPod at $0.22/h may be worth the roughly 30% extra cost.
