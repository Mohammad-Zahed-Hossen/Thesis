#!/usr/bin/env python3
"""
Download and cache ChartQA and all MMMU configs in one go.
Run this once (or when you need to refresh cache); then make data will use the cache and be fast.
"""
import argparse
import sys
from pathlib import Path

_ROOT = Path(__file__).resolve().parents[1]
if str(_ROOT) not in sys.path:
    sys.path.insert(0, str(_ROOT))

import yaml
from data.download import DEFAULT_MMMU_CONFIGS, get_chartqa_splits, get_one_mmmu_config


def main():
    parser = argparse.ArgumentParser(description="Download ChartQA + MMMU to cache (one go)")
    parser.add_argument("--config", default=str(_ROOT / "configs" / "default.yaml"))
    parser.add_argument("--data-dir", default=None)
    args = parser.parse_args()

    with open(args.config) as f:
        cfg = yaml.safe_load(f)
    paths = cfg.get("paths", {})
    data_dir = Path(args.data_dir or paths.get("data_dir", "./data_cache")).resolve()
    data_dir.mkdir(parents=True, exist_ok=True)

    print("[download] ChartQA + MMMU → one-time download to cache. Then run make data.", flush=True)
    print("[download] Data dir:", data_dir, flush=True)

    # ChartQA: download once
    print("\n[1/2] ChartQA...", flush=True)
    get_chartqa_splits(data_dir)
    print("ChartQA done.\n", flush=True)

    # MMMU: each config one by one (each download goes to cache; we drop after)
    mmmu_configs = (cfg.get("datasets") or {}).get("mmmu_configs") or DEFAULT_MMMU_CONFIGS
    print(f"[2/2] MMMU ({len(mmmu_configs)} configs)...", flush=True)
    for i, config_name in enumerate(mmmu_configs, 1):
        print(f"  {i}/{len(mmmu_configs)} {config_name}...", flush=True)
        split = get_one_mmmu_config(data_dir, config_name)
        if split is not None:
            print(f"  Cached: {len(split)} examples.", flush=True)
        del split  # free memory before next config

    print("\n[download] All data cached. Run: make data", flush=True)


if __name__ == "__main__":
    main()
