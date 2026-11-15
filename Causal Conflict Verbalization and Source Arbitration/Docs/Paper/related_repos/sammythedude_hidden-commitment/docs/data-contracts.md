# Data contracts

The reusable code intentionally does not depend on one private run directory. Exchange artifacts through JSONL and NPZ files with the following fields.

## Behavioral JSONL

```json
{
  "qid": "stable-question-id",
  "question": "When did ...?",
  "context": "Document: ...\n\nDocument: ...",
  "prompt": "fully constructed user prompt",
  "response": "model continuation only",
  "doc1_aliases": ["1922"],
  "doc2_aliases": ["1985"],
  "decision_token_indices": [7],
  "label": "doc1",
  "condition": "original_conflict",
  "split": "train"
}
```

Decision-token indices are relative to the response, not to the chat-formatted prompt. Save model ID, exact revision, tokenizer revision, seed, decoding parameters, and prompt template beside every generated file.

## CETT NPZ

- `X`: float32 `[rows, layers * d_mlp]`
- `y`: int32 `[rows]`, with the positive class documented by the run manifest
- `qids`: string `[rows]`

The `hidden-commitment localize` command consumes this contract.

## Residual NPZ

- `X`: float32 `[rows, positions, layers, hidden_size]`
- `y`: int32 `[rows]`, where `0=doc1` and `1=doc2`
- `qids`: string `[rows]`
- `positions`: string `[positions]`
- `conditions`: optional string `[rows]`, normally original/swapped order

The `hidden-commitment fit-direction` command consumes this contract.

## Direction JSON

The selected object stores the layer, named token position, normalized vector, and positive/negative label semantics. Keep the full candidate table so layer/position selection remains auditable.
