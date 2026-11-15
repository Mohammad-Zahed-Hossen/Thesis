# Method map

This package implements the reusable primitives behind **Hidden Commitment: When Language Models Silently Pick a Side and How Steering Can Surface It**. The accepted paper remains the specification for reported numbers; this document maps that specification to code.

## 1. Behavioral records

Each record contains a question, two contradictory documents, aliases for the answer supported by each document, a generated response, and response-relative decision-token indices. `hidden_commitment.text` provides conservative whole-phrase alias matching, document swapping, and token-span alignment.

The document-choice label is deliberately positional: `doc1` or `doc2`. It is not a truth label. Rows matching both or neither answer family are ambiguous and should not enter a source-choice readout.

## 2. CETT localization

For MLP intermediate activation `z[l,t,j]` and down-projection matrix `W[l]`, the implementation computes

```text
CETT[l,t,j] = abs(z[l,t,j]) * norm(W[l,:,j]) / (norm(W[l] @ z[l,t]) + eps)
```

The vectorized implementation is `hidden_commitment.cett.cett_scores`. `capture_mlp_inputs` hooks the input of every `mlp.down_proj`, which is the post-gating intermediate activation. Features are averaged over the decision-token span before sparse localization.

`fit_sparse_localization` fits an L1 logistic classifier and selects regularization on validation data. `split_groups` keeps all variants of a question ID in one split. For paper-level stability, repeat localization across seeds and retain neurons whose sign recurs; the helper preserves signed weights so this aggregation is explicit rather than hidden in the trainer.

## 3. Residual source-choice direction

`capture_residual_inputs` records the input to each transformer block. `hidden_commitment.residuals` converts the full sequence into the named positions used in the paper: prompt-final, response onset, and answer-span checkpoints.

`select_direction` fits `mean(doc2) - mean(doc1)` for every layer and position on training rows. Selection uses validation data only. When original/swap condition labels are supplied, candidates are ranked by mean condition AUROC, minimum condition AUROC, pooled AUROC, and class-mean gap. Test rows must not be inspected until selection is frozen.

## 4. Sparse-write bridge

`write_projection` evaluates whether localized neurons write into the independently learned residual direction:

```text
sum_(l,j in localized) mean_t(z[l,t,j]) * dot(W_down[l,:,j], v_source)
```

Compare this score with layer-matched random neuron sets. Do not interpret activation correlation alone as evidence of a write pathway.

## 5. Steering

`residual_steering_hook` applies the paper's RMS-scaled update:

```text
x[t] <- x[t] + delta * RMS(x[t]) * unit_direction
```

The readout is defined at the input to a selected layer, so the implementation edits the preceding block's output. `SteeringWindow` makes prefill and generated-token windows explicit. Always verify a `delta=0` hook reproduces the unhooked generation before interpreting an intervention, especially across model families.

## 6. Required controls

- Split by question ID, never by generated row.
- Evaluate original and swapped document order.
- Compare contradiction with exact-copy, paraphrased-agreement, and single-document prompts.
- Audit a closed-book subset to measure parametric-recall confounding.
- Use layer-matched random neurons for CETT controls.
- Use a stat-matched random residual unit orthogonal to the learned direction for steering.
- Report decided-row denominators, ambiguous/truncated counts, and confidence intervals.

## 7. Surfacing labels

`hidden_commitment.judging` preserves the paper's five-way surfacing schema and derives broad and strict-unresolved labels without collapsing them prematurely. The optional Gemini client uses structured JSON, temperature-controlled classification, no tools, and local validation of every enum. Persist the short rationale for audit, but never use it as a model feature.
