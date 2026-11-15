"""
Run VLM inference on CMC-Bench instances via mlx-vlm.
Unified API for all models: apply_chat_template + generate.
"""
from pathlib import Path
from PIL import Image
from data.schema import InstanceRecord


PROMPT_TEMPLATE = (
    "Query: {query}. "
    "Retrieved image evidence: see the attached image. "
    "Retrieved text evidence: {text_passage}. "
    "Answer the query using the provided evidence."
)


def load_image_for_record(rec: InstanceRecord) -> str | None:
    """Return image path string if file exists, else None."""
    p = Path(rec.image_path)
    if not p.exists():
        return None
    return str(p)


def run_inference(
    model,
    processor,
    config,
    rec: InstanceRecord,
    image_path: str,
    max_tokens: int = 128,
    generate_kwargs: dict | None = None,
) -> dict:
    """
    Run a single inference via mlx-vlm.
    Returns {"instance_id": ..., "answer": ...}.
    """
    from mlx_vlm import generate
    from mlx_vlm.prompt_utils import apply_chat_template

    prompt_text = PROMPT_TEMPLATE.format(
        query=rec.query,
        text_passage=rec.text_passage,
    )

    try:
        formatted_prompt = apply_chat_template(
            processor, config, prompt_text, num_images=1
        )
        gen_kw: dict = {"max_tokens": max_tokens, "verbose": False}
        if generate_kwargs:
            gen_kw.update(generate_kwargs)
        output = generate(
            model,
            processor,
            formatted_prompt,
            [image_path],
            **gen_kw,
        )
        text = output if isinstance(output, str) else str(output)
    except Exception as e:
        text = f"[Error: {e}]"

    return {"instance_id": rec.instance_id, "answer": text.strip()}
