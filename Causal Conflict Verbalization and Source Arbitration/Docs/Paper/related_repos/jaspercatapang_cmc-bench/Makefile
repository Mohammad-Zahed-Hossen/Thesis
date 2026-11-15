# CMC-Bench: Cross-Modal Conflict Benchmark
# Targets for download, instance build, and local VLM eval (see src/configs/default.yaml).

PYTHON ?= python
SRC := src
CONFIG := $(SRC)/configs/default.yaml

.PHONY: help install download data eval all clean

help:
	@echo "CMC-Bench targets:"
	@echo "  make download - Download ChartQA + MMMU to cache (run once; then make data is fast)"
	@echo "  make data     - Build instances from cache (1,000 examples, 4,000 instances)"
	@echo "  make eval     - Run evaluation on all models"
	@echo "  make all      - data then eval"

# Keep Hugging Face cache inside project to avoid ~/.cache permission issues
HF_CACHE := $(shell pwd)/data_cache/hf_cache
HF_ENV := HF_HUB_ENABLE_HF_TRANSFER=1 HF_HOME=$(HF_CACHE) HF_DATASETS_CACHE=$(HF_CACHE)/datasets

# Download ChartQA + all MMMU configs to cache in one go (run once; then make data is fast)
download:
	$(HF_ENV) PYTHONPATH=$(SRC) $(PYTHON) $(SRC)/scripts/download_data.py --config $(CONFIG)

# Build instances from cache (requires make download first, or will download on first run)
data:
	$(HF_ENV) PYTHONPATH=$(SRC) $(PYTHON) $(SRC)/scripts/run_example_generation.py --config $(CONFIG)

eval:
	PYTHONPATH=$(SRC) $(PYTHON) $(SRC)/scripts/run_evaluation.py --config $(CONFIG)

install:
	pip install -r $(SRC)/requirements.txt

clean:
	rm -rf outputs/ data_cache/

all: data eval
