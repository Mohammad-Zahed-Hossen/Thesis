"""Download and cache ChartQA and MMMU from HuggingFace."""
from pathlib import Path
from datasets import load_dataset, concatenate_datasets
from tqdm import tqdm
try:
    from datasets import Image as HFImage
except ImportError:
    from datasets.features import Image as HFImage  # decoding image columns
try:
    from datasets import enable_progress_bars
    enable_progress_bars()
except ImportError:
    try:
        from datasets.utils import enable_progress_bars
        enable_progress_bars()
    except Exception:
        pass


# Default MMMU domains: STEM, humanities, social, applied (valid config names on HF)
DEFAULT_MMMU_CONFIGS = [
    "Physics",
    "History",
    "Psychology",
    "Computer_Science",
    "Art",
    "Economics",
]


def get_chartqa_splits(data_dir: Path) -> dict:
    """Return dict of split_name -> dataset for ChartQA. Includes 'eval' = val + test (no train)."""
    print("[ChartQA] Loading HuggingFaceM4/ChartQA...", flush=True)
    ds = load_dataset(
        "HuggingFaceM4/ChartQA",
        cache_dir=str(data_dir / "hf_cache" / "datasets"),
    )
    sizes = {k: len(v) for k, v in ds.items()}
    print(f"[ChartQA] Loaded: {sizes}", flush=True)
    val = ds.get("val") or ds.get("validation")
    test = ds.get("test")
    if val is not None and test is not None:
        eval_ds = concatenate_datasets([val, test])
        print(f"[ChartQA] Eval pool (val+test): {len(eval_ds)} examples.", flush=True)
        return {**{k: v for k, v in ds.items()}, "eval": eval_ds}
    if val is not None:
        return {**{k: v for k, v in ds.items()}, "eval": val}
    if test is not None:
        return {**{k: v for k, v in ds.items()}, "eval": test}
    return {k: v for k, v in ds.items()}


def get_one_mmmu_config(data_dir: Path, config_name: str):
    """Load a single MMMU config (validation + test only). Returns Dataset with 'domain' column.
    Use this to avoid loading all configs at once (memory/time).
    MMMU columns: question, answer, image_1..image_7, options, explanation, etc.
    """
    print(f"[MMMU]   Loading {config_name} (val+test)...", flush=True)
    print("[MMMU]   First-time download can take 5–15 min per config (MMMU ~3.6 GB total). Progress below.", flush=True)
    cache = str(data_dir / "hf_cache" / "datasets")
    ds = load_dataset(
        "MMMU/MMMU",
        config_name,
        cache_dir=cache,
    )
    val = ds.get("validation") or ds.get("dev")
    test = ds.get("test")
    if val is not None and test is not None:
        split = concatenate_datasets([val, test])
    else:
        split = val or test
    if split is None:
        return None
    # Ensure image_1 is decoded to PIL when accessed (MMMU has image_1..image_7)
    if "image_1" in split.column_names:
        try:
            split = split.cast_column("image_1", HFImage())
        except Exception:
            pass  # already decoded or different format
    split = split.add_column("domain", [config_name] * len(split))
    return split


def get_mmmu_splits(
    data_dir: Path,
    configs: list[str] | None = None,
) -> dict:
    """Return dict with combined validation+test from multiple MMMU domain configs.
    Each row has a 'domain' column. Prefer processing config-by-config via get_one_mmmu_config
    to avoid loading all configs at once.
    """
    configs = configs or DEFAULT_MMMU_CONFIGS
    cache = str(data_dir / "hf_cache" / "datasets")
    splits_to_merge = []
    for i, config_name in tqdm(enumerate(configs, 1), total=len(configs), desc="MMMU configs (get_mmmu_splits)", unit="config"):
        print(f"[MMMU] Loading config {i}/{len(configs)}: {config_name}...", flush=True)
        split = get_one_mmmu_config(data_dir, config_name)
        if split is None:
            print(f"[MMMU]   No validation/test for {config_name}, skipping.", flush=True)
            continue
        splits_to_merge.append(split)
        print(f"[MMMU]   {config_name}: {len(split)} examples (val+test).", flush=True)
    if not splits_to_merge:
        return {}
    combined = concatenate_datasets(splits_to_merge)
    print(f"[MMMU] Combined: {len(combined)} eval examples.", flush=True)
    return {"validation": combined}
