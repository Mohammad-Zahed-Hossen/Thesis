#!/usr/bin/env python3
"""Experiment harness v4. Generation runs on Colab; everything else also runs locally.

Differences from v3:
  * Model, revisions and repetition penalty are explicit and recorded with every row.
  * Adds inert filler, description-order, detection-only, reliability-only, congruent
    and single-source arms. The v3 prompts are kept verbatim for replication.
  * Separate dev and confirmatory items that share no problem.
  * Equal-answer pairs are excluded from conflict stimuli.
  * ChartQA now shows the report text; v3 never showed it, so no conflict existed.
  * Detects the token cap exactly, using every EOS id in the generation config.
  * Writes one JSONL row per arm and item, flushed per batch, and resumes by key.

The repetition penalty matters. Qwen2.5-VL-3B ships with 1.05 and v3 didn't override it.
The penalty acts on tokens in input_ids, which contain the typed text but not the words
in the image, so it could tilt output away from copying the typed problem. Qwen2-VL-2B
ships with 1.0, so leaving defaults in place would confound the two models. v4 defaults
to 1.0; run 1.05 once on the v3 arms to measure the effect.

Usage on Colab:
    python harness_v4.py --phase dev --arm_set core --run_tag dev_qwen25
    python harness_v4.py --phase confirm --arm_set core --run_tag confirm_qwen25

Local dry run, using a fake model and no images:
    python harness_v4.py --dry_run --phase dev --arm_set core --limit 20 --run_tag dryrun --output_dir dryrun_out
"""
from __future__ import annotations

import argparse
import hashlib
import json
import os
import platform
import sys
import time
import zlib
from dataclasses import asdict, dataclass, field
from typing import Any, Dict, Iterable, List, Optional, Sequence, Set

import score_v4 as sc

HERE = os.path.dirname(os.path.abspath(__file__))

# Commit hashes read from the Hugging Face API on 2026-11-06.
MODEL_PINS = {
    "Qwen/Qwen2.5-VL-3B-Instruct": "66285546d2b821cf421d4f5eb2576359d3770cd3",
    "Qwen/Qwen2-VL-2B-Instruct": "895c3a49bc3fa70a340399125c650a463535e71c",
    # Added for v5; read from https://huggingface.co/api/models/<id> on 2026-11-11.
    "Qwen/Qwen2.5-VL-7B-Instruct": "cc594898137f460bfe9f0759e9844b3ce807cfb5",
}
DATASET_PINS = {
    "vlm-modality-research/modality-conflict-arbitration-v2": "2c55b099f286554685798d54cea4bde761d486b7",
    "vlm-modality-research/chartqa-evidence-conflict-v2": "7d15a9704bc5e028e7038ef98aa7917059535bf8",
}
CONFLICT_DATASET = "vlm-modality-research/modality-conflict-arbitration-v2"
CHARTQA_DATASET = "vlm-modality-research/chartqa-evidence-conflict-v2"

# ─── Prompts ─────────────────────────────────────────────────────────────────

V3_OPEN = "Look at the image and read the text problem below.\n{text_question}\n\n"
OPEN = "Look at the image and read the typed text below.\n{text_question}\n\n"
FORMAT = "Show your step-by-step working. On the last line, write #### followed by only the final number.\n"


def _v(*instructions: str) -> List[str]:
    return [OPEN + i + " Then solve the problem. " + FORMAT for i in instructions]


@dataclass(frozen=True)
class Arm:
    name: str
    templates: Sequence[str]  # index 0 is canonical; the rest are paraphrases
    stimulus: str = "conflict"  # conflict | congruent | image_only | text_only


_DIRECT = [
    OPEN + "Solve the problem. " + FORMAT,
    OPEN + "Work out the solution. " + FORMAT,
    OPEN + "Find the answer to the problem. " + FORMAT,
]
_FILLER = _v(
    "In two sentences, state a general tip for checking arithmetic, without mentioning the image or the typed text.",
    "In two sentences, give general advice on avoiding calculation mistakes, without mentioning the image or the typed text.",
    "In two sentences, explain why careful arithmetic is useful, without mentioning the image or the typed text.",
)
_DESC_IMAGE_FIRST = _v(
    "In two sentences, neutrally describe what the image shows and then what the typed text says, without comparing them.",
    "In two sentences, say what is in the image and then what is in the typed text, without comparing them.",
    "In two sentences, neutrally summarize the image and then the typed text, without comparing them.",
)
_DESC_TEXT_FIRST = _v(
    "In two sentences, neutrally describe what the typed text says and then what the image shows, without comparing them.",
)
_DETECT = _v(
    "In two sentences, state whether the image and the typed text agree or contradict each other.",
)
_RELIABILITY = _v(
    "In two sentences, explain which source, the image or the typed text, you consider more reliable.",
)
_CONFLICT_FULL = _v(
    "In two sentences, state whether the image and the typed text agree or contradict each other, and explain which source you consider more reliable.",
    "In two sentences, say if the image and the typed text are consistent or conflict, and which source you trust more.",
    "In two sentences, judge whether the image and the typed text agree or disagree, and explain which source is more reliable.",
)

ARMS: Dict[str, Arm] = {
    a.name: a
    for a in [
        # v3 wording, verbatim. tests/test_v4.py checks this against the v3 file.
        Arm("direct_v3", [V3_OPEN + "Solve the problem. Conclude with: #### <answer>\n"]),
        Arm(
            "placebo_v3",
            [
                V3_OPEN
                + "In two sentences, neutrally describe what is presented in the image and what is stated in the text without comparing them. "
                "Then solve the problem. Conclude with: #### <answer>\n"
            ],
        ),
        Arm(
            "conflict_v3",
            [
                V3_OPEN
                + "In two sentences, state whether the image and the text agree or contradict each other, and explain which source you consider more reliable. "
                "Then solve that problem. Conclude with: #### <answer>\n"
            ],
        ),
        # v4 arms.
        Arm("direct", _DIRECT),
        Arm("filler", _FILLER),
        Arm("desc_image_first", _DESC_IMAGE_FIRST),
        Arm("desc_text_first", _DESC_TEXT_FIRST),
        Arm("detect_only", _DETECT),
        Arm("reliability_only", _RELIABILITY),
        Arm("conflict_full", _CONFLICT_FULL),
        # Same problem in both sources: measures false alarms and overall solving.
        Arm("congruent_direct", _DIRECT, "congruent"),
        Arm("congruent_detect", _DETECT, "congruent"),
        Arm("congruent_conflict", _CONFLICT_FULL, "congruent"),
        # One source only: can the model solve it at all?
        Arm("base_image", ["Look at the image.\n{image_only_question}\nSolve the problem. " + FORMAT], "image_only"),
        Arm("base_text", ["Read the problem below.\n{text_question}\n\nSolve the problem. " + FORMAT], "text_only"),
    ]
}

ARM_SETS = {
    "core": [
        "direct_v3", "placebo_v3", "conflict_v3", "direct", "filler", "desc_image_first",
        "desc_text_first", "detect_only", "reliability_only", "conflict_full",
        "congruent_direct", "congruent_detect", "congruent_conflict", "base_image", "base_text",
    ],
    "replication_model": ["direct", "filler", "desc_image_first", "conflict_full", "base_image", "base_text"],
    "chartqa": ["direct", "filler", "desc_image_first", "desc_text_first", "detect_only", "reliability_only", "conflict_full", "base_image", "base_text"],
    "penalty_check": ["direct_v3", "placebo_v3", "conflict_v3"],
    "paraphrase": ["direct", "filler", "desc_image_first", "conflict_full"],
}

# ─── Items ───────────────────────────────────────────────────────────────────


@dataclass
class Item:
    id: str
    source: str
    image: Any
    image_question: str
    text_question: str
    y_image: str
    y_text: str
    image_only_question: str = ""


def item_from_conflict_row(row: Dict[str, Any]) -> Item:
    return Item(
        id=row["id"],
        source=row.get("source", row["id"].split("-")[0]),
        image=row.get("image"),
        image_question=row["image_question"],
        text_question=row["text_question"],
        y_image=str(row.get("image_answer")),
        y_text=str(row.get("text_answer")),
    )


def item_from_chartqa_row(row: Dict[str, Any]) -> Item:
    """The report is the competing source, so it must be in the text the model sees."""
    question = row["question"]
    return Item(
        id=str(row["conflict_id"]),
        source="chartqa",
        image=row.get("image"),
        image_question="",
        text_question=f"{row['text_report']}\n\nQuestion: {question}",
        y_image=str(row["chart_answer"]),
        y_text=str(row["report_answer"]),
        image_only_question=f"Question: {question}",
    )


def filter_distinct(items: Iterable[Item]) -> List[Item]:
    return [it for it in items if not sc.numeric_equal(it.y_image, it.y_text)]


def problem_keys(item: Item) -> Set[str]:
    """Problems an item uses. ChartQA has one question per item, so its id is enough."""
    if not item.image_question:
        return {item.id}
    return {item.image_question, item.text_question}


def split_phase(items: Sequence[Item], phase: str, dev_size: int = 200) -> List[Item]:
    """Return dev or confirm items, sharing no problem.

    Dev takes a contiguous block from each dataset source, in proportion to its size.
    Confirm items that use any dev problem are dropped, since pairs share problems with
    their neighbours.
    """
    if phase == "all":
        return list(items)
    if phase not in {"dev", "confirm"}:
        raise ValueError(f"unknown phase {phase!r}")
    by_source: Dict[str, List[Item]] = {}
    for it in items:
        by_source.setdefault(it.source, []).append(it)
    dev: List[Item] = []
    for members in by_source.values():
        dev += members[: round(dev_size * len(members) / len(items))]
    if phase == "dev":
        return dev
    used: Set[str] = set()
    for it in dev:
        used |= problem_keys(it)
    return [it for it in items if not (problem_keys(it) & used)]


def load_items(split: str, dataset_revision: Optional[str]) -> List[Item]:
    from datasets import load_dataset  # Colab only

    if split == "chartqa":
        ds = load_dataset(CHARTQA_DATASET, split="test", revision=dataset_revision)
        return filter_distinct(item_from_chartqa_row(ds[i]) for i in range(len(ds)))
    ds = load_dataset(CONFLICT_DATASET, split="train", revision=dataset_revision)
    ds = ds.filter(lambda x: x["degradation_level"] == 0 and x["channel"] == "image")
    return filter_distinct(item_from_conflict_row(ds[i]) for i in range(len(ds)))


def load_items_from_v3(path: str) -> List[Item]:
    """Questions and answers from stored v3 results, without images, for dry runs."""
    with open(path, encoding="utf-8") as f:
        data = json.load(f)
    return filter_distinct(item_from_conflict_row(d) for d in data)


# ─── Requests ────────────────────────────────────────────────────────────────


@dataclass
class Request:
    item: Item
    arm: str
    prompt: str
    stimulus: str
    prefill: Optional[str] = None
    paraphrase: int = 0

    @property
    def uses_image(self) -> bool:
        return self.stimulus != "text_only"


def build_request(item: Item, arm_name: str, paraphrase: int = 0) -> Request:
    arm = ARMS[arm_name]
    if paraphrase >= len(arm.templates):
        raise ValueError(f"arm {arm_name} has no paraphrase {paraphrase}")
    if arm.stimulus == "congruent" and not item.image_question:
        raise ValueError(f"arm {arm_name} needs an image question; item {item.id} has none")
    text = item.image_question if arm.stimulus == "congruent" else item.text_question
    if arm.stimulus == "image_only":
        prompt = arm.templates[paraphrase].format(image_only_question=item.image_only_question)
    else:
        prompt = arm.templates[paraphrase].format(text_question=text)
    return Request(item=item, arm=arm_name, prompt=prompt, stimulus=arm.stimulus, paraphrase=paraphrase)


def gold_answers(req: Request) -> Dict[str, str]:
    if req.stimulus in {"congruent", "image_only"}:
        return {"y_image": req.item.y_image, "y_text": req.item.y_image}
    if req.stimulus == "text_only":
        return {"y_image": req.item.y_text, "y_text": req.item.y_text}
    return {"y_image": req.item.y_image, "y_text": req.item.y_text}


def render_chat(apply_chat_template, prompt: str, prefill: Optional[str], has_image: bool) -> str:
    """Build the model input, leaving the assistant turn open after any prefill."""
    content: List[Dict[str, str]] = [{"type": "image"}] if has_image else []
    content.append({"type": "text", "text": prompt})
    messages: List[Dict[str, Any]] = [{"role": "user", "content": content}]
    if prefill:
        messages.append({"role": "assistant", "content": prefill})
    text = apply_chat_template(messages, tokenize=False, add_generation_prompt=not prefill)
    if prefill:
        for suffix in ("<|im_end|>\n", "<|im_end|>"):
            if text.endswith(suffix):
                text = text[: -len(suffix)]
                break
        if not text.endswith(prefill):
            raise RuntimeError("chat template changed the prefill; the intervention would be invalid")
    return text


def decode_ids(ids: Sequence[int], eos_ids: Set[int], pad_id: Optional[int]) -> tuple:
    """Return (kept_ids, reached_eos). Stops at any EOS id or at padding."""
    kept: List[int] = []
    for tok in ids:
        if tok in eos_ids:
            return kept, True
        if pad_id is not None and tok == pad_id:
            return kept, True
        kept.append(tok)
    return kept, False


# ─── Backends ────────────────────────────────────────────────────────────────


class BackendOutOfMemory(Exception):
    pass


@dataclass
class Generation:
    text: str
    tokens: int
    hit_cap: bool


class EchoBackend:
    """A fake model for pipeline tests. Its numbers mean nothing."""

    name = "echo"

    def __init__(self, oom_above: Optional[int] = None):
        self.oom_above = oom_above
        self.batches: List[int] = []

    def info(self) -> Dict[str, Any]:
        return {"backend": self.name, "warning": "fake outputs; not experimental data"}

    def generate(self, requests: Sequence[Request], cfg: "RunConfig") -> List[Generation]:
        if self.oom_above is not None and len(requests) > self.oom_above:
            raise BackendOutOfMemory()
        self.batches.append(len(requests))
        out = []
        for r in requests:
            h = zlib.crc32((r.arm + r.item.id + (r.prefill or "")).encode())
            gold = gold_answers(r)
            pick = gold["y_image"] if h % 3 == 0 else gold["y_text"] if h % 3 == 1 else str(h % 97)
            if r.prefill:
                body = f"To solve the problem, compute it.\n\n#### {pick}"
            else:
                body = (
                    "The image and the typed text do not agree. They present different problems.\n\n"
                    f"To solve the problem, compute it.\n\n#### {pick}"
                )
            words = body.split()
            capped = len(words) >= cfg.max_new_tokens
            out.append(Generation(" ".join(words[: cfg.max_new_tokens]) if capped else body, min(len(words), cfg.max_new_tokens), capped))
        return out


class HFBackend:
    """Transformers backend. Needs a GPU session; not exercised by the local tests."""

    name = "transformers"

    def __init__(self, cfg: "RunConfig"):
        import glob

        for p in sys.path:
            for lib_dir in glob.glob(os.path.join(p, "nvidia", "*", "lib")):
                if lib_dir not in os.environ.get("LD_LIBRARY_PATH", ""):
                    os.environ["LD_LIBRARY_PATH"] = f"{lib_dir}:{os.environ.get('LD_LIBRARY_PATH', '')}"
        import torch
        import transformers
        from transformers import AutoProcessor

        self.torch = torch
        self.transformers_version = transformers.__version__

        # Same CUDA 13 NVRTC workaround as v3: integer .prod() on CPU.
        original_prod = torch.Tensor.prod

        def safe_prod(tensor, *args, **kwargs):
            if tensor.is_cuda and tensor.dtype in (torch.int64, torch.int32, torch.int16, torch.int8):
                return original_prod(tensor.cpu(), *args, **kwargs).to(tensor.device)
            return original_prod(tensor, *args, **kwargs)

        torch.Tensor.prod = safe_prod

        dtype = torch.float32
        if torch.cuda.is_available():
            major, _ = torch.cuda.get_device_capability()
            dtype = torch.bfloat16 if major >= 8 else torch.float16
        self.dtype = str(dtype)
        kwargs = dict(torch_dtype=dtype, device_map="auto", attn_implementation="sdpa", revision=cfg.model_revision)
        try:
            from transformers import AutoModelForImageTextToText

            self.model = AutoModelForImageTextToText.from_pretrained(cfg.model_id, **kwargs)
        except (ImportError, ValueError):
            if "Qwen2.5" in cfg.model_id:
                from transformers import Qwen2_5_VLForConditionalGeneration as cls
            else:
                from transformers import Qwen2VLForConditionalGeneration as cls
            self.model = cls.from_pretrained(cfg.model_id, **kwargs)
        self.model.eval()
        self.processor = AutoProcessor.from_pretrained(
            cfg.model_id, min_pixels=cfg.min_pixels, max_pixels=cfg.max_pixels, revision=cfg.model_revision
        )
        self.processor.tokenizer.padding_side = "left"
        tok = self.processor.tokenizer
        if tok.pad_token_id is None:
            tok.pad_token_id = tok.eos_token_id
        eos = self.model.generation_config.eos_token_id
        self.eos_ids = set(eos if isinstance(eos, (list, tuple)) else [eos]) | {tok.eos_token_id}
        self.pad_id = tok.pad_token_id

    def info(self) -> Dict[str, Any]:
        t = self.torch
        return {
            "backend": self.name,
            "torch": t.__version__,
            "transformers": self.transformers_version,
            "cuda": t.version.cuda,
            "gpu": t.cuda.get_device_name(0) if t.cuda.is_available() else None,
            "dtype": self.dtype,
            "resolved_model_commit": getattr(self.model.config, "_commit_hash", None),
            "generation_config": self.model.generation_config.to_dict(),
            "eos_ids": sorted(self.eos_ids),
            "peak_vram_gb": t.cuda.max_memory_allocated() / 2**30 if t.cuda.is_available() else None,
        }

    def generate(self, requests: Sequence[Request], cfg: "RunConfig") -> List[Generation]:
        t = self.torch
        uses_image = requests[0].uses_image
        if any(r.uses_image != uses_image for r in requests):
            raise ValueError("a batch can't mix image and text-only requests")
        texts = [render_chat(self.processor.apply_chat_template, r.prompt, r.prefill, uses_image) for r in requests]
        images = [r.item.image.convert("RGB") for r in requests] if uses_image else None
        if cfg.do_sample:
            t.manual_seed(zlib.crc32(f"{cfg.seed}|{requests[0].arm}|{requests[0].item.id}".encode()))
        try:
            inputs = self.processor(text=texts, images=images, return_tensors="pt", padding=True).to(self.model.device)
            prompt_len = inputs["input_ids"].shape[1]
            sampling = (
                {"do_sample": True, "temperature": cfg.temperature, "top_p": 1.0, "top_k": 0}
                if cfg.do_sample
                else {"do_sample": False, "temperature": None, "top_p": None, "top_k": None}
            )
            with t.inference_mode():
                output = self.model.generate(
                    **inputs, max_new_tokens=cfg.max_new_tokens, repetition_penalty=cfg.repetition_penalty, **sampling
                )
        except t.cuda.OutOfMemoryError as exc:
            t.cuda.empty_cache()
            raise BackendOutOfMemory() from exc
        results = []
        for row in output[:, prompt_len:].tolist():
            kept, reached_eos = decode_ids(row, self.eos_ids, self.pad_id)
            text = self.processor.tokenizer.decode(kept, skip_special_tokens=True)
            results.append(Generation(text, len(kept), (not reached_eos) and len(kept) >= cfg.max_new_tokens))
        del inputs, output
        t.cuda.empty_cache()
        return results


# ─── Run ─────────────────────────────────────────────────────────────────────


@dataclass
class RunConfig:
    run_tag: str
    model_id: str = "Qwen/Qwen2.5-VL-3B-Instruct"
    model_revision: Optional[str] = None
    dataset_revision: Optional[str] = None
    split: str = "conflict"
    phase: str = "dev"
    arm_set: str = "core"
    arms: List[str] = field(default_factory=list)
    paraphrase: int = 0
    max_new_tokens: int = 400
    batch_size: int = 8
    repetition_penalty: float = 1.0
    do_sample: bool = False
    temperature: float = 0.7
    seed: int = 42
    min_pixels: int = 128 * 28 * 28
    max_pixels: int = 256 * 28 * 28
    dev_size: int = 200
    limit: Optional[int] = None
    backend: str = "transformers"


def row_key(arm: str, item_id: str) -> str:
    return f"{arm}|{item_id}"


def load_done(path: str) -> Set[str]:
    """Keys already written. A last line cut off by a crash is dropped and rerun."""
    done: Set[str] = set()
    if not os.path.exists(path):
        return done
    with open(path, encoding="utf-8") as f:
        for line in f:
            try:
                row = json.loads(line)
            except json.JSONDecodeError:
                continue
            done.add(row_key(row["arm"], row["id"]))
    return done


def generate_safe(backend, batch: List[Request], cfg: RunConfig) -> List[Generation]:
    """Halve the batch on out-of-memory; re-raise if a single request doesn't fit."""
    try:
        return backend.generate(batch, cfg)
    except BackendOutOfMemory:
        if len(batch) == 1:
            raise
        mid = len(batch) // 2
        return generate_safe(backend, batch[:mid], cfg) + generate_safe(backend, batch[mid:], cfg)


def make_row(req: Request, gen: Generation, cfg: RunConfig, wall_s: float) -> Dict[str, Any]:
    gold = gold_answers(req)
    return {
        "run_tag": cfg.run_tag,
        "model_id": cfg.model_id,
        "split": cfg.split,
        "phase": cfg.phase,
        "repetition_penalty": cfg.repetition_penalty,
        "do_sample": cfg.do_sample,
        "seed": cfg.seed,
        "paraphrase": req.paraphrase,
        "max_new_tokens": cfg.max_new_tokens,
        "id": req.item.id,
        "source": req.item.source,
        "arm": req.arm,
        "stimulus": req.stimulus,
        "image_question": req.item.image_question,
        "text_question": req.item.text_question,
        "y_image": gold["y_image"],
        "y_text": gold["y_text"],
        "prompt_sha1": hashlib.sha1(req.prompt.encode()).hexdigest()[:12],
        "prefill": req.prefill,
        "generated": gen.text,
        "full_text": (req.prefill or "") + gen.text,
        "tokens": gen.tokens,
        "hit_cap": gen.hit_cap,
        "wall_s": round(wall_s, 3),
    }


def run_requests(requests: Sequence[Request], backend, cfg: RunConfig, out_path: str, log=print) -> int:
    """Generate every request not already in out_path. Returns the number written."""
    done = load_done(out_path)
    by_arm: Dict[str, List[Request]] = {}
    for r in requests:
        if row_key(r.arm, r.item.id) not in done:
            by_arm.setdefault(r.arm, []).append(r)
    written = 0
    start = time.time()
    with open(out_path, "a", encoding="utf-8") as f:
        for arm, pending in by_arm.items():
            capped = 0
            for b in range(0, len(pending), cfg.batch_size):
                batch = pending[b : b + cfg.batch_size]
                t0 = time.time()
                gens = generate_safe(backend, batch, cfg)
                per_item = (time.time() - t0) / len(batch)
                for req, gen in zip(batch, gens):
                    f.write(json.dumps(make_row(req, gen, cfg, per_item), ensure_ascii=False) + "\n")
                    capped += gen.hit_cap
                f.flush()
                os.fsync(f.fileno())
                written += len(batch)
            log(f"[{time.strftime('%H:%M:%S')}] {arm}: {len(pending)} done, {capped} hit the token cap; {(time.time() - start) / 60:.1f} min elapsed")
    return written


def report_missing(requests: Sequence[Request], out_path: str) -> int:
    """Return 1 and list what's absent if any request has no row in out_path."""
    done = load_done(out_path)
    missing = [row_key(r.arm, r.item.id) for r in requests if row_key(r.arm, r.item.id) not in done]
    if missing:
        print(f"INCOMPLETE: {len(missing)} of {len(requests)} requests have no row, e.g. {missing[:5]}. Rerun the same command.", file=sys.stderr)
        return 1
    print(f"Complete: all {len(requests)} requests have a row.")
    return 0


def write_manifest(path: str, cfg: RunConfig, backend, n_items: int, script_paths: Sequence[str]) -> None:
    """Record the run, and refuse to continue one with different settings."""
    config = asdict(cfg)
    config.pop("limit", None)
    scripts = {}
    for p in script_paths:
        with open(p, "rb") as f:
            scripts[os.path.basename(p)] = hashlib.sha256(f.read()).hexdigest()
    if os.path.exists(path):
        with open(path, encoding="utf-8") as f:
            previous = json.load(f)
        if previous["config"] != config:
            differing = sorted(k for k in config if previous["config"].get(k) != config[k])
            raise SystemExit(f"Run tag already used with different settings: {differing}. Pick a new --run_tag.")
        changed = sorted(k for k, v in scripts.items() if previous.get("scripts_sha256", {}).get(k) != v)
        if changed:
            print(f"Warning: {changed} changed since this run tag started. Earlier rows came from the old code.", file=sys.stderr)
    manifest = {
        "config": config,
        "n_items": n_items,
        "scripts_sha256": scripts,
        "python": platform.python_version(),
        "written_at": time.strftime("%Y-%m-%dT%H:%M:%S"),
        "environment": backend.info(),
    }
    with open(path, "w", encoding="utf-8") as f:
        json.dump(manifest, f, indent=2, default=str)


def resolve_revisions(cfg: RunConfig) -> None:
    """Fill in pinned revisions. A confirmatory run with no pin is an error."""
    if cfg.model_revision is None:
        cfg.model_revision = MODEL_PINS.get(cfg.model_id)
    dataset = CHARTQA_DATASET if cfg.split == "chartqa" else CONFLICT_DATASET
    if cfg.dataset_revision is None:
        cfg.dataset_revision = DATASET_PINS.get(dataset)
    if cfg.phase == "confirm" and cfg.backend != "echo" and not (cfg.model_revision and cfg.dataset_revision):
        raise SystemExit("A confirmatory run needs --model_revision and --dataset_revision.")


def add_common_args(parser: argparse.ArgumentParser) -> None:
    parser.add_argument("--run_tag", required=True)
    parser.add_argument("--model_id", default="Qwen/Qwen2.5-VL-3B-Instruct")
    parser.add_argument("--model_revision", default=None)
    parser.add_argument("--dataset_revision", default=None)
    parser.add_argument("--split", default="conflict", choices=["conflict", "chartqa"])
    parser.add_argument("--phase", default="dev", choices=["dev", "confirm", "all"])
    parser.add_argument("--max_new_tokens", type=int, default=400)
    parser.add_argument("--batch_size", type=int, default=8)
    parser.add_argument("--repetition_penalty", type=float, default=1.0)
    parser.add_argument("--do_sample", action="store_true")
    parser.add_argument("--temperature", type=float, default=0.7)
    parser.add_argument("--seed", type=int, default=42)
    parser.add_argument("--max_pixels", type=int, default=256 * 28 * 28)
    parser.add_argument("--dev_size", type=int, default=200)
    parser.add_argument("--limit", type=int, default=None, help="For smoke tests only")
    parser.add_argument("--output_dir", default="results_v4")
    parser.add_argument("--dry_run", action="store_true", help="Use the fake model and stored v3 questions")
    parser.add_argument("--v3_results", default=os.path.join(HERE, "results_v3", "full_experiment_results v3.0.json"))


def config_from_args(args: argparse.Namespace, **extra: Any) -> RunConfig:
    return RunConfig(
        run_tag=args.run_tag,
        model_id=args.model_id,
        model_revision=args.model_revision,
        dataset_revision=args.dataset_revision,
        split=args.split,
        phase=args.phase,
        max_new_tokens=args.max_new_tokens,
        batch_size=args.batch_size,
        repetition_penalty=args.repetition_penalty,
        do_sample=args.do_sample,
        temperature=args.temperature,
        seed=args.seed,
        max_pixels=args.max_pixels,
        dev_size=args.dev_size,
        limit=args.limit,
        backend="echo" if args.dry_run else "transformers",
        **extra,
    )


def select_items(args: argparse.Namespace, cfg: RunConfig) -> List[Item]:
    items = load_items_from_v3(args.v3_results) if args.dry_run else load_items(cfg.split, cfg.dataset_revision)
    selected = split_phase(items, cfg.phase, cfg.dev_size)
    return selected[: cfg.limit] if cfg.limit else selected


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    add_common_args(parser)
    parser.add_argument("--arm_set", default="core", choices=sorted(ARM_SETS))
    parser.add_argument("--arms", nargs="*", default=None, help="Overrides --arm_set")
    parser.add_argument("--paraphrase", type=int, default=0)
    args = parser.parse_args()

    arm_names = args.arms or ARM_SETS[args.arm_set]
    unknown = [a for a in arm_names if a not in ARMS]
    if unknown:
        parser.error(f"unknown arms: {unknown}")
    cfg = config_from_args(args, arm_set=args.arm_set, arms=list(arm_names), paraphrase=args.paraphrase)
    resolve_revisions(cfg)

    items = select_items(args, cfg)
    requests = [build_request(it, a, cfg.paraphrase) for a in arm_names for it in items]
    print(f"{len(items)} items, {len(arm_names)} arms, {len(requests)} requests, phase={cfg.phase}, model={cfg.model_id}")

    backend = EchoBackend() if args.dry_run else HFBackend(cfg)
    os.makedirs(args.output_dir, exist_ok=True)
    out_path = os.path.join(args.output_dir, f"{cfg.run_tag}.jsonl")
    manifest = os.path.join(args.output_dir, f"{cfg.run_tag}.manifest.json")
    scripts = [os.path.abspath(__file__), os.path.join(HERE, "score_v4.py")]
    write_manifest(manifest, cfg, backend, len(items), scripts)
    written = run_requests(requests, backend, cfg, out_path)
    write_manifest(manifest, cfg, backend, len(items), scripts)  # records peak VRAM
    print(f"Wrote {written} rows to {out_path}")
    return report_missing(requests, out_path)


if __name__ == "__main__":
    sys.exit(main())
