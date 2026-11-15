#!/usr/bin/env python3
"""
Build a HuggingFace dataset of conflicting-modality VQA examples.

Each example is a tuple:
  (dataset, question, text, image, text_answer, vision_answer)

Source: dal-289/word_or_vision (DocVQA and VQAv2 splits, text_type=="corrupted")

text_answer is extracted by querying Gemini 3.0 Flash to determine what answer
the corrupted text cue would suggest, given the question and ground-truth answer.

Usage:
  conda run -n rational python build_dataset.py [--save_to_hub REPO_ID]
"""

import ast
import json
import os
import sys
import time
from pathlib import Path

from datasets import Dataset, DatasetDict, Features, Value, Image as HFImage, load_dataset
from dotenv import load_dotenv
from google import genai
from google.genai import types
from tqdm import tqdm

# ---------------------------------------------------------------------------
# Config
# ---------------------------------------------------------------------------
SPLITS = ["DocVQA", "VQAv2"]
TEXT_TYPE_FILTER = "corrupted"
GEMINI_MODEL = "gemini-3-flash-preview"
QPS = 5.0  # queries per second
MAX_RETRIES = 3
CHECKPOINT_DIR = Path(__file__).parent / "checkpoints"

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


def extract_text_answer(
    client: genai.Client,
    question: str,
    vision_answer: str,
    added_text: str,
) -> str:
    """Ask Gemini what answer the corrupted text cue would suggest."""
    prompt = (
        "You are given a visual question answering (VQA) scenario.\n\n"
        f"Question: {question}\n"
        f"Correct answer (from the image): {vision_answer}\n"
        f"Conflicting text provided alongside the image: {added_text}\n\n"
        "The conflicting text was designed to suggest a DIFFERENT answer than "
        "what the image shows. Your task is to determine what answer someone "
        "would give if they relied ONLY on the text cue and ignored the image.\n\n"
        "Rules:\n"
        "- Output ONLY the answer suggested by the text, nothing else.\n"
        "- The answer should be a single word or short phrase, in a similar "
        "format/style to the correct answer shown above.\n"
        "- If the text is too corrupted/truncated to suggest any specific "
        "answer, output exactly: N/A\n"
    )

    config = types.GenerateContentConfig(
        temperature=0.0,
        max_output_tokens=64,
        thinking_config=types.ThinkingConfig(thinking_budget=0),
    )

    for attempt in range(MAX_RETRIES):
        try:
            resp = client.models.generate_content(
                model=GEMINI_MODEL,
                contents=prompt,
                config=config,
            )
            return (getattr(resp, "text", None) or "N/A").strip()
        except Exception as e:
            if attempt < MAX_RETRIES - 1:
                wait = 2 ** (attempt + 1)
                print(f"  [retry {attempt+1}] {e}; waiting {wait}s", file=sys.stderr)
                time.sleep(wait)
            else:
                print(f"  [FAILED] {e}", file=sys.stderr)
                return "N/A"


# ---------------------------------------------------------------------------
# Answer parsing
# ---------------------------------------------------------------------------

def parse_answers(answers_str: str) -> str:
    """Parse the string-encoded answer list and return the first entry."""
    try:
        parsed = ast.literal_eval(answers_str)
        if isinstance(parsed, list) and len(parsed) > 0:
            return str(parsed[0])
    except Exception:
        pass
    # Fallback: strip brackets and quotes
    s = answers_str.strip().strip("[]").strip("'\"")
    if "," in s:
        s = s.split(",")[0].strip().strip("'\"")
    return s


# ---------------------------------------------------------------------------
# Checkpointing
# ---------------------------------------------------------------------------

def checkpoint_path(split: str) -> Path:
    return CHECKPOINT_DIR / f"{split}_text_answers.json"


def load_checkpoint(split: str) -> dict:
    p = checkpoint_path(split)
    if p.exists():
        with open(p) as f:
            return json.load(f)
    return {}


def save_checkpoint(split: str, data: dict):
    CHECKPOINT_DIR.mkdir(parents=True, exist_ok=True)
    with open(checkpoint_path(split), "w") as f:
        json.dump(data, f)


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------

def main():
    import argparse
    ap = argparse.ArgumentParser()
    ap.add_argument("--save_to_hub", type=str, default=None,
                    help="HuggingFace repo ID to push the dataset to (e.g., user/repo)")
    ap.add_argument("--output_dir", type=str,
                    default=str(Path(__file__).parent / "dataset"),
                    help="Local directory to save the dataset")
    args = ap.parse_args()

    client = init_gemini()
    sec_per_req = 1.0 / QPS

    print("Loading dal-289/word_or_vision ...")
    src = load_dataset("dal-289/word_or_vision")

    all_rows = {split: [] for split in SPLITS}

    for split in SPLITS:
        print(f"\n{'='*60}")
        print(f"Processing split: {split}")
        print(f"{'='*60}")

        ds = src[split]
        # Filter for corrupted text_type
        corrupted = ds.filter(lambda x: x["text_type"] == TEXT_TYPE_FILTER)
        n = len(corrupted)
        print(f"  Found {n} corrupted examples (out of {len(ds)} total)")

        # Load existing checkpoint
        ckpt = load_checkpoint(split)
        print(f"  Checkpoint has {len(ckpt)} existing text_answers")

        last_call = 0.0
        for i in tqdm(range(n), desc=f"  {split}"):
            row = corrupted[i]
            idx_key = str(i)

            # Parse fields
            dataset_name = row["dataset"]
            question = row["question"] + " Please only output the answer with a single word or phrase."
            text = row["added_text"]
            image = row["image"]
            vision_answer = parse_answers(row["answers"])

            # Get text_answer (from checkpoint or Gemini)
            if idx_key in ckpt:
                text_answer = ckpt[idx_key]
            else:
                # Rate limit
                now = time.time()
                wait = sec_per_req - (now - last_call)
                if wait > 0:
                    time.sleep(wait)
                last_call = time.time()

                text_answer = extract_text_answer(
                    client, row["question"], vision_answer, text
                )
                ckpt[idx_key] = text_answer

                # Periodic checkpoint save
                if (i + 1) % 50 == 0:
                    save_checkpoint(split, ckpt)

            all_rows[split].append({
                "dataset": dataset_name,
                "question": question,
                "text": text,
                "image": image,
                "text_answer": text_answer,
                "vision_answer": vision_answer,
            })

        # Final checkpoint save for this split
        save_checkpoint(split, ckpt)
        print(f"  Done. {len(all_rows[split])} examples processed.")

    # Build HuggingFace DatasetDict
    print("\nBuilding HuggingFace DatasetDict ...")
    features = Features({
        "dataset": Value("string"),
        "question": Value("string"),
        "text": Value("string"),
        "image": HFImage(),
        "text_answer": Value("string"),
        "vision_answer": Value("string"),
    })

    ds_dict = DatasetDict({
        split: Dataset.from_list(all_rows[split], features=features)
        for split in SPLITS
    })

    print(ds_dict)

    # Save locally
    out_dir = args.output_dir
    print(f"\nSaving to {out_dir} ...")
    ds_dict.save_to_disk(out_dir)
    print("Saved locally.")

    # Optionally push to hub
    if args.save_to_hub:
        print(f"\nPushing to HuggingFace Hub: {args.save_to_hub} ...")
        ds_dict.push_to_hub(args.save_to_hub)
        print("Pushed to hub.")

    print("\nDone!")


if __name__ == "__main__":
    main()
