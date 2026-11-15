"""
Load VLMs via mlx-vlm on Apple Silicon.
Unified API: load() returns (model, processor); inference uses 4-bit weights from config.
"""

MODEL_CONFIGS = {
    "qwen3-vl-4b": {
        "mlx_id": "mlx-community/Qwen3-VL-4B-Instruct-4bit",
        "family": "Qwen",
        "params": "4B",
    },
    "lfm2.5-vl-1.6b": {
        "mlx_id": "mlx-community/LFM2.5-VL-1.6B-4bit",
        "family": "LiquidAI",
        "params": "1.6B",
    },
    "gemma-3n-e2b": {
        "mlx_id": "mlx-community/gemma-3n-E2B-it-4bit",
        "family": "Google",
        "params": "2B",
    },
    "deepseek-vl2-small": {
        "mlx_id": "mlx-community/deepseek-vl2-small-4bit",
        "family": "DeepSeek",
        "params": "3B (MoE)",
    },
}


def get_device(requested: str | None = None) -> str:
    """MLX uses Metal automatically; this is kept for interface compat."""
    return requested or "mlx"


def load_model(model_name: str, **kwargs):
    """
    Load a VLM via mlx-vlm. Returns (model, processor, config).
    """
    from mlx_vlm import load
    from mlx_vlm.utils import load_config

    cfg = MODEL_CONFIGS.get(model_name)
    if cfg is None:
        raise ValueError(f"Unknown model: {model_name}. Available: {list(MODEL_CONFIGS)}")

    model_path = cfg["mlx_id"]
    model, processor = load(model_path)
    config = load_config(model_path)
    return model, processor, config
