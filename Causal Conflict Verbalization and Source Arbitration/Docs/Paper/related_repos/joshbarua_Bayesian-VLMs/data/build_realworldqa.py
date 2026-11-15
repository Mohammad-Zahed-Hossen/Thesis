#!/usr/bin/env python3
"""
Build conflicting-modality VQA examples from xai-org/RealworldQA.

RealworldQA contains (image, question, answer) tuples where many questions are
multiple-choice or yes/no.  This script uses Gemini to convert each example into
the conflicting_modality format:

  (dataset, question, text, image, text_answer, vision_answer)

The LLM must:
  1. Rewrite the question to be open-ended (no MC options, no yes/no).
  2. Rewrite the vision_answer as a short phrase (not a letter like "C").
  3. Invent a plausible piece of text evidence that implies a *different* answer.
  4. State what answer the text suggests (text_answer).

All examples should be convertible — the LLM is instructed to creatively
reframe questions (including spatial, yes/no, and MC) as needed.

Usage:
  conda run -n rational python build_realworldqa.py [--save_to_hub REPO_ID]
"""

import json
import os
import sys
import time
from pathlib import Path

from datasets import (
    Dataset,
    DatasetDict,
    Features,
    Value,
    Image as HFImage,
    load_dataset,
    load_from_disk,
)
from dotenv import load_dotenv
from google import genai
from google.genai import types
from tqdm import tqdm

# ---------------------------------------------------------------------------
# Config
# ---------------------------------------------------------------------------
GEMINI_MODEL = "gemini-3-flash-preview"
QPS = 5.0
MAX_RETRIES = 3
CHECKPOINT_DIR = Path(__file__).parent / "checkpoints"
DATASET_NAME = "RealworldQA"

# ---------------------------------------------------------------------------
# Gemini helpers
# ---------------------------------------------------------------------------

def init_gemini() -> genai.Client:
    load_dotenv(Path(__file__).resolve().parent.parent / ".env")
    api_key = os.getenv("GEMINI_API_KEY")
    if not api_key:
        print("[ERROR] GEMINI_API_KEY not found in .env", file=sys.stderr)
        sys.exit(1)
    return genai.Client()


CONVERSION_PROMPT = """\
You are helping build a dataset of **conflicting-modality VQA** examples.
Each example has an image and a piece of text.  The image supports one answer
(the "vision answer") and the text supports a *different* answer (the "text
answer").  The question must be **open-ended** (not multiple-choice, not yes/no).

You are given a RealworldQA example:
- **Image**: (attached)
- **Original question**: {question}
- **Original answer**: {answer}

Your task:

1. **Rewrite the question** so it is open-ended (a short, natural question
   answerable in a word or short phrase).  Remove any multiple-choice options
   or yes/no framing.  You may change the question substantially if needed —
   the goal is a good conflicting-modality example, not faithfulness to the
   original question.

2. **State the vision answer** — the short answer that the *image* supports.
   Must be a word or short phrase (NOT a letter like "A" or "C").

3. **Invent conflicting text evidence** — a 1–2 sentence passage that would
   plausibly accompany this image (e.g. a caption, label, sign description,
   report excerpt) but that implies a *different* answer to the rewritten
   question.

4. **State the text answer** — the short answer someone would give if they
   relied ONLY on the text and ignored the image.

You must ALWAYS produce a valid conversion.  Every question — including
spatial, yes/no, and multiple-choice questions — can be rewritten into a good
conflicting-modality example.  Be creative: reframe the question, change the
focus, or pick a different aspect of the scene if needed.

Output valid JSON (no markdown fences) with these keys:
{{
  "question": "...",
  "vision_answer": "...",
  "text": "...",
  "text_answer": "..."
}}

The question field should end with " Please only output the answer with a single word or phrase."

Rules:
- text_answer and vision_answer must be **different**.
- Both answers should be short (a word or brief phrase).
- The text must NOT reference what the image actually shows; it must plausibly
  lead to the text_answer on its own.
- Do NOT include any explanation outside the JSON.
"""


def convert_example(
    client: genai.Client,
    question: str,
    answer: str,
    image,
) -> dict | None:
    """Ask Gemini to convert one RealworldQA example. Returns dict or None on failure."""
    prompt = CONVERSION_PROMPT.format(question=question, answer=answer)

    config = types.GenerateContentConfig(
        temperature=0.7,
        max_output_tokens=512,
        thinking_config=types.ThinkingConfig(thinking_budget=1024),
    )

    for attempt in range(MAX_RETRIES):
        try:
            resp = client.models.generate_content(
                model=GEMINI_MODEL,
                contents=[image, prompt],
                config=config,
            )
            text = (getattr(resp, "text", None) or "").strip()

            # Strip markdown fences if present
            if text.startswith("```"):
                text = text.split("\n", 1)[1]
                if text.endswith("```"):
                    text = text[: text.rfind("```")]
                text = text.strip()

            parsed = json.loads(text)

            # Validate required keys
            for key in ("question", "vision_answer", "text", "text_answer"):
                if key not in parsed or not parsed[key].strip():
                    raise ValueError(f"Missing or empty key: {key}")
            if parsed["text_answer"].strip().lower() == parsed["vision_answer"].strip().lower():
                raise ValueError("text_answer == vision_answer")

            return parsed

        except Exception as e:
            if attempt < MAX_RETRIES - 1:
                wait = 2 ** (attempt + 1)
                print(f"  [retry {attempt+1}] {e}; waiting {wait}s", file=sys.stderr)
                time.sleep(wait)
            else:
                print(f"  [FAILED] {e}", file=sys.stderr)
                return None


# ---------------------------------------------------------------------------
# Checkpointing
# ---------------------------------------------------------------------------

def checkpoint_path() -> Path:
    return CHECKPOINT_DIR / f"{DATASET_NAME}_conversions.json"


def load_checkpoint() -> dict:
    p = checkpoint_path()
    if p.exists():
        with open(p) as f:
            return json.load(f)
    return {}


def save_checkpoint(data: dict):
    CHECKPOINT_DIR.mkdir(parents=True, exist_ok=True)
    with open(checkpoint_path(), "w") as f:
        json.dump(data, f)


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------

def main():
    import argparse

    ap = argparse.ArgumentParser()
    ap.add_argument(
        "--save_to_hub",
        type=str,
        default=None,
        help="HuggingFace repo ID to push the full dataset to",
    )
    ap.add_argument(
        "--output_dir",
        type=str,
        default=str(Path(__file__).parent / "dataset"),
        help="Dataset directory (RealworldQA split saved as a subdirectory)",
    )
    args = ap.parse_args()

    client = init_gemini()
    sec_per_req = 1.0 / QPS

    # Load RealworldQA
    print("Loading xai-org/RealworldQA ...")
    src = load_dataset("xai-org/RealworldQA", split="test")
    n = len(src)
    print(f"  {n} examples")

    # Load checkpoint
    ckpt = load_checkpoint()
    print(f"  Checkpoint has {len(ckpt)} existing conversions")

    failed = 0
    converted = 0
    last_call = 0.0

    for i in tqdm(range(n), desc="  RealworldQA"):
        ex = src[i]
        idx_key = str(i)

        if idx_key in ckpt:
            if ckpt[idx_key] is None:
                failed += 1
            else:
                converted += 1
            continue

        # Rate limit
        now = time.time()
        wait = sec_per_req - (now - last_call)
        if wait > 0:
            time.sleep(wait)
        last_call = time.time()

        result = convert_example(
            client,
            question=ex["question"],
            answer=ex["answer"],
            image=ex["image"],
        )

        if result is None:
            ckpt[idx_key] = None
            failed += 1
        else:
            ckpt[idx_key] = result
            converted += 1

        # Periodic checkpoint
        if (i + 1) % 25 == 0:
            save_checkpoint(ckpt)

    # Final checkpoint
    save_checkpoint(ckpt)

    print(f"\nConversion summary:")
    print(f"  Converted: {converted}")
    print(f"  Failed:    {failed}")

    if converted == 0:
        print("No examples converted — exiting.")
        return

    # Build HuggingFace dataset via generator to avoid holding all images in memory
    features = Features({
        "dataset": Value("string"),
        "question": Value("string"),
        "text": Value("string"),
        "image": HFImage(),
        "text_answer": Value("string"),
        "vision_answer": Value("string"),
    })

    def gen_rows():
        for i in range(n):
            idx_key = str(i)
            cached = ckpt.get(idx_key)
            if cached is None:
                continue
            yield {
                "dataset": DATASET_NAME,
                "question": cached["question"],
                "text": cached["text"],
                "image": src[i]["image"],
                "text_answer": cached["text_answer"],
                "vision_answer": cached["vision_answer"],
            }

    print("\nBuilding RealworldQA split ...")
    new_ds = Dataset.from_generator(lambda: gen_rows(), features=features)
    print(f"  {new_ds}")

    # Save directly into the dataset directory as a new split.
    # This avoids loading the existing splits into memory.
    out_dir = Path(args.output_dir)
    split_dir = out_dir / DATASET_NAME
    print(f"\nSaving split to {split_dir} ...")
    new_ds.save_to_disk(str(split_dir))

    # Update the DatasetDict manifest so load_from_disk sees the new split
    manifest_path = out_dir / "dataset_dict.json"
    if manifest_path.exists():
        with open(manifest_path) as f:
            manifest = json.load(f)
    else:
        manifest = {"splits": []}
    if DATASET_NAME not in manifest["splits"]:
        manifest["splits"].append(DATASET_NAME)
        with open(manifest_path, "w") as f:
            json.dump(manifest, f)
        print(f"Updated {manifest_path}: {manifest['splits']}")
    print("Saved.")

    if args.save_to_hub:
        print(f"\nPushing to HuggingFace Hub: {args.save_to_hub} ...")
        full_ds = load_from_disk(str(out_dir))
        print(f"  Full dataset: {full_ds}")
        full_ds.push_to_hub(args.save_to_hub)
        print("Pushed.")

    print("\nDone!")


if __name__ == "__main__":
    main()
