# Attention experiments

This directory contains only the experiments reported in the paper's
attention section:

1. `run_allocation.py` measures image, passage, question, and other attention
   mass at the first-divergent-token readout over the full 6×6 reliability
   grid.
2. `run_knockout.py` masks the direct route from image, passage, or question
   positions to that readout in full-softmax attention layers.
3. `run_linear_output_knockout.py` zeroes Qwen3.5's Gated DeltaNet output at
   the readout, because linear attention has no tokenwise span weights to mask.

`summarize.py`, `plot_allocation.py`, and `make_table.py` produce the reported
confidence intervals, heatmap, and knockout table. Exact commands and run
parameters are in the repository-level README.

The intervention engine uses a custom eager attention path so it can expose
the readout row before softmax. A knockout assigns `-inf` to the selected keys,
giving them exactly zero mass while preserving the ratios among surviving
keys. Run the CPU checks with:

```bash
python attention/test_attention.py
```
