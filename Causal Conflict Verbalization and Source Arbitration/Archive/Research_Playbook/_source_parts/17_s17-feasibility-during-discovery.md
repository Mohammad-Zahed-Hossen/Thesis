---

## 17. Feasibility during discovery

### 17.1 Feasibility is a research instrument, not a gate at the end

Feasibility questions are *scientific* questions in disguise. "Can I measure this deterministically?" is the same as "what is the construct, operationally?" "Can this run in 16 GB?" constrains how many conditions you can compare, which constrains which explanations you can test. **[L3]**

Evaluate feasibility **while** evaluating the question, with a one-page budget:

| Dimension | Concrete question | Your constraint |
|---|---|---|
| Data | Does the dataset exist, is it licensed, inspectable, correctly labeled? | Public HF datasets only |
| Model access | Weights available? Revision pinned? Fits in 16 GB? | ≤3B, FP16 inference |
| Instrumentation | Can behavior be observed without training? | Inference-only; logits/attention optional |
| Compute | Items × arms × tokens × seconds per item → total GPU hours | Colab sessions, session time limits |
| Implementation | Days to a working harness, including parsing and checkpointing | ≤5 days |
| Evaluation | Deterministic parsing possible? Judge needed? | Prefer regex/exact classification |
| Experiment count | How many arms and replications are needed to rule out the main confounds? | ≤6 arms |
| Reproducibility | Seeds, pinned versions, released configs, saved raw outputs | Required |
| Time | Weeks available from now to defense | Fixed |

### 17.2 The two opposite mistakes

**Mistake A — rejecting a good question too early.** "[X] looks hard, so I will not try." Fix: separate *hard* from *blocked*. Hard means it takes weeks; blocked means an asset does not exist. Convert the question to the smallest version that is not blocked, then check whether that version still answers something (usually it does). **[L3]**

**Mistake B — developing a beautiful question that cannot be tested.** You produce an elegant causal story that requires six model families, human annotation in two languages, and 300 GPU hours. Fix: write the compute line *first*, before the theory. If the arithmetic exceeds your budget, either drop conditions or drop the question. **[L3]**

### 17.3 The compute line, computed honestly

```text
GPU hours ≈ items × arms × avg_tokens × seconds_per_token / 3600

Example: 1,619 items × 3 arms × 120 tokens ≈ 583k forward-decoded tokens.
On a T4 at ~2.3 s per item per arm (measured in your harness):
1,619 × 3 ≈ 4,857 item-passes × ~2.3 s ≈ 3.1 hours of GPU time,
plus checkpointing and restarts → plan for 5 hours and two sessions.
```

Notice the two consequences: (i) the full population across arms is affordable, and (ii) *adding* arms is cheap compared with *adding* rounds of annotation. For inference-only behavioral research, **more arms beat more items** — arms buy causal discrimination, items buy statistical precision. Pay for discrimination first. **[L2/L3; your own harness measured ~2.32 s/item at FP16 with SDPA.]**

### 17.4 Feasibility scoring for candidate questions

| Question | Data | Model | Instrument | Compute | Implementation | Verdict |
|---|---|---|---|---|---|---|
| Does conflict verbalization change engaged source under matched length? | ready | ready | deterministic classifier (validated) | ~5 GPU-hours | harness exists | **Feasible** |
| Is abstention conflict-specific or instruction-induced? | ready (add neutral uncertainty arm) | ready | classifier + refusal text inspection | ~2 GPU-hours added | modest | **Feasible, high value** |
| Does the effect generalize to chart reasoning conflicts? | secondary dataset exists in config | ready | domain-specific parsing needed | ~3 GPU-hours | 2–4 days | **Feasible later** |
| Does the effect arise from attention reallocation? | ready | ready | attention instrumentation required, unclear validity | unknown | high | **Blocked for now** |
| Does the mechanism transfer across three model families? | ready | requires additional checkpoints | ready | ~15 GPU-hours | moderate | **Deferred to future work** |

**[L3] Rule:** every candidate question gets a feasibility verdict on the same day it is proposed: Feasible / Feasible later / Blocked. Blocked items go to the Question Ledger with a reuse condition, not into the thesis plan.

### 17.5 Feasibility's second face: interpretability

A run is only worth doing if the outcome can be interpreted under every possible result. Before running, complete:

```text
If the effect appears            → I conclude ______
If the effect is absent          → I conclude ______
If the effect appears only in X  → I conclude ______
If the data are unparseable      → my fallback analysis is ______
```

If any line is blank, the run is not yet feasible in the scientific sense, regardless of compute. **[L3]**
