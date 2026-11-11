#!/usr/bin/env python3
"""Experiment harness v5: order-counterbalanced prompts, base and donor stages.

Implements Docs/PREREGISTRATION_VERDICT_TRANSPLANT.md, §§3–4 and §6. The transplant
stage (minimal-edit verdicts and margin scoring) is in transplant_v5.py, which imports
this module.

What is new relative to v4:
  * No source letters. Sources get modality headers ("Image:", "Typed text:",
    "Chart:", "Report:"), and only their positions swap. The instruction always comes
    before both sources and the format line after them (prereg §4.1).
  * Literal K = 4 templates for the non-binding, binding and explicit arms, in both
    regimes (prereg §§4.2, 4.4).
  * Log-likelihood margin scoring at '####' (prereg §6.1), teacher-forced, with an
    exact token-boundary check.

v4 files are left unchanged so the v4 dev runs still reproduce. This module reuses
v4's loaders, dev/confirm split, manifest and EOS handling.

Stages (Colab):
    python harness_v5.py --stage base  --split conflict --phase dev --run_tag v5dev_base_qwen25
    python harness_v5.py --stage donor --split conflict --phase dev --run_tag v5dev_donor_qwen25
Print the rendered chat for one item in both orders (prereg §8 render gate):
    python harness_v5.py --print_example --split conflict --phase dev --run_tag x
Local dry run, using a fake model and the stored v3 questions:
    python harness_v5.py --dry_run --stage base --limit 4 --run_tag dry --output_dir dryrun_out
"""
from __future__ import annotations

import argparse
import hashlib
import json
import os
import sys
import time
import zlib
from dataclasses import asdict, dataclass, field
from decimal import Decimal, InvalidOperation
from typing import Any, Callable, Dict, List, Optional, Sequence, Set

import harness_v4 as h4
import score_v5 as sc

HERE = os.path.dirname(os.path.abspath(__file__))

MODEL_PINS = h4.MODEL_PINS
DATASET_PINS = h4.DATASET_PINS
REGIME = {"conflict": "math", "chartqa": "chartqa"}
ORDERS = ("image_first", "text_first")
ORDER_CODE = {"image_first": -0.5, "text_first": 0.5}  # prereg §4.1

# ─── Templates (prereg §4.2 and §4.4, literal) ───────────────────────────────

FORMAT_MATH = "Show your step-by-step working. On the last line, write #### followed by only the final number."
FORMAT_CHART = "On the last line, write #### followed by only the answer."

MATH_STEMS = [
    "In two sentences, state whether the image and the typed text present the same problem, and say which source you consider more reliable.",
    "In two sentences, say whether the image and the typed text show the same problem, and state which source you find more reliable.",
    "In two sentences, judge whether the image and the typed text contain the same problem, and say which of the two sources is more reliable.",
    "In two sentences, note whether the image and the typed text give the same problem, and say which source you trust as more reliable.",
]
MATH_ENDINGS = {
    "nonbinding": [
        "Then solve a problem.",
        "Then solve one problem.",
        "Then work out a problem.",
        "Then solve a problem from the sources.",
    ],
    "binding": [
        "Then solve only the problem from the source you named as more reliable, and ignore the other problem.",
        "Then solve only the problem given by the source you said is more reliable, and ignore the other one.",
        "Then work out only the problem from the more reliable source you named, and disregard the other problem.",
        "Then solve only the problem in the source you judged more reliable, and leave the other problem aside.",
    ],
    # {X} is "the image" or "the typed text".
    "explicit": [
        "Then solve only the problem from {X}, and ignore the other problem.",
        "Then solve only the problem given by {X}, and ignore the other one.",
        "Then work out only the problem from {X}, and disregard the other problem.",
        "Then solve only the problem in {X}, and leave the other problem aside.",
    ],
}
CHART_STEMS = [
    "In two sentences, state whether the chart and the report give the same answer, and say which source you consider more reliable.",
    "In two sentences, say whether the chart and the report give the same answer, and state which source you find more reliable.",
    "In two sentences, judge whether the chart and the report support the same answer, and say which of the two sources is more reliable.",
    "In two sentences, note whether the chart and the report agree on the answer, and say which source you trust as more reliable.",
]
CHART_ENDINGS = {
    "nonbinding": [
        "Then answer the question.",
        "Then give an answer to the question.",
        "Then work out the answer to the question.",
        "Then answer the question from the sources.",
    ],
    "binding": [
        "Then answer the question using only the source you named as more reliable, and ignore the other source.",
        "Then answer the question using only the source you said is more reliable, and ignore the other one.",
        "Then work out the answer using only the more reliable source you named, and disregard the other source.",
        "Then answer the question using only the source you judged more reliable, and leave the other source aside.",
    ],
    "explicit": [
        "Then answer the question using only {X}, and ignore the other source.",
        "Then answer the question using only {X}, and ignore the other one.",
        "Then work out the answer using only {X}, and disregard the other source.",
        "Then answer the question using only {X}, and leave the other source aside.",
    ],
}
# What the explicit arms and the paraphrase verdicts call each source.
SOURCE_NAME = {
    "math": {"image": "the image", "text": "the typed text"},
    "chartqa": {"chart": "the chart", "report": "the report"},
}
FAMILIES = ("nonbinding", "binding", "explicit_image", "explicit_text")
BASE_ARMS = ("base_image", "base_text")


def instruction(regime: str, family: str, k: int, question: str = "") -> str:
    """The instruction I for template k (1-based)."""
    if not 1 <= k <= 4:
        raise ValueError(f"template k must be 1..4, got {k}")
    stems, endings = (MATH_STEMS, MATH_ENDINGS) if regime == "math" else (CHART_STEMS, CHART_ENDINGS)
    if family in ("nonbinding", "binding"):
        ending = endings[family][k - 1]
    elif family in ("explicit_image", "explicit_text"):
        side = sc.SOURCES[regime][0 if family == "explicit_image" else 1]
        ending = endings["explicit"][k - 1].format(X=SOURCE_NAME[regime][side])
    else:
        raise ValueError(f"unknown family {family!r}")
    text = f"{stems[k - 1]} {ending}"
    return f"Question: {question}\n{text}" if regime == "chartqa" else text


# ─── Items ───────────────────────────────────────────────────────────────────

Item = h4.Item  # for ChartQA: text_question = the report, image_only_question = the question


def item_from_chartqa_row(row: Dict[str, Any]) -> Item:
    return Item(
        id=str(row["conflict_id"]),
        source="chartqa",
        image=row.get("image"),
        image_question="",
        text_question=str(row["text_report"]),
        y_image=str(row["chart_answer"]),
        y_text=str(row["report_answer"]),
        image_only_question=str(row["question"]),
    )


def distinct(items) -> List[Item]:
    return [it for it in items if not sc.answers_match(it.y_image, it.y_text)]


# The Hub release has 230 rows. Which Source Wins? (arXiv:2608.17205, §3.2.2) analyses 229:
# a post-run audit removed one item whose report did not support its answer. The paper's
# artifact names it in data/chartqa_conflict/excluded_items.json and MANIFEST.json
# ("chartqa_excluded_compiled_item_ids": [45]). Row 45 asks for a March 2021 value; its
# report gives 1.81 for March 2021 and puts the "report answer" 2.81 under September 2019.
CHARTQA_EXCLUDED_IDS = frozenset({"45"})
CHARTQA_PINNED_ROWS = 230
CHARTQA_ANALYSED_ITEMS = 229


def chartqa_analysis_set(items: Sequence[Item], pinned: bool = True) -> List[Item]:
    """Drop the audited exclusion, then equal-answer pairs. With the pinned revision the counts are checked."""
    items = list(items)
    present = CHARTQA_EXCLUDED_IDS & {it.id for it in items}
    kept = distinct(it for it in items if it.id not in CHARTQA_EXCLUDED_IDS)
    if pinned:
        if len(items) != CHARTQA_PINNED_ROWS or present != CHARTQA_EXCLUDED_IDS or len(kept) != CHARTQA_ANALYSED_ITEMS:
            raise SystemExit(
                f"ChartQA-Conflict: expected {CHARTQA_PINNED_ROWS} rows including id(s) {sorted(CHARTQA_EXCLUDED_IDS)} "
                f"and {CHARTQA_ANALYSED_ITEMS} items after exclusion; got {len(items)} rows, "
                f"excluded ids present: {sorted(present)}, {len(kept)} items kept. The dataset is not the pinned release."
            )
    return kept


def load_items(split: str, dataset_revision: Optional[str]) -> List[Item]:
    if split == "chartqa":
        from datasets import load_dataset  # Colab only

        ds = load_dataset(h4.CHARTQA_DATASET, split="test", revision=dataset_revision)
        pinned = dataset_revision == DATASET_PINS.get(h4.CHARTQA_DATASET)
        return chartqa_analysis_set([item_from_chartqa_row(ds[i]) for i in range(len(ds))], pinned=pinned)
    return h4.load_items(split, dataset_revision)


# ─── Content lists (prereg §4.1) ─────────────────────────────────────────────


def _headers(regime: str, item: Item):
    if regime == "math":
        return "Image: ", f"Typed text:\n{item.text_question}", FORMAT_MATH
    return "Chart: ", f"Report:\n{item.text_question}", FORMAT_CHART


def build_content(regime: str, item: Item, instr: str, order: str) -> List[Dict[str, str]]:
    """User-turn content list: instruction, both sources in the given order, format line.

    Only the two sources swap. The image entry sits where its header puts it.
    """
    image_header, text_block, fmt = _headers(regime, item)
    if order == "image_first":
        return [
            {"type": "text", "text": f"{instr}\n\n{image_header}"},
            {"type": "image"},
            {"type": "text", "text": f"\n\n{text_block}\n\n{fmt}"},
        ]
    if order == "text_first":
        return [
            {"type": "text", "text": f"{instr}\n\n{text_block}\n\n{image_header}"},
            {"type": "image"},
            {"type": "text", "text": f"\n\n{fmt}"},
        ]
    raise ValueError(f"unknown order {order!r}")


def build_base_content(regime: str, item: Item, arm: str) -> List[Dict[str, str]]:
    """Single-source arms (prereg §4.5)."""
    if regime == "math":
        if arm == "base_image":
            return [
                {"type": "text", "text": "Image: "},
                {"type": "image"},
                {"type": "text", "text": f"\n\nSolve the problem shown in the image. {FORMAT_MATH}"},
            ]
        if arm == "base_text":
            return [{"type": "text", "text": f"Typed text:\n{item.text_question}\n\nSolve the typed problem. {FORMAT_MATH}"}]
    else:
        q = item.image_only_question
        if arm == "base_image":
            return [
                {"type": "text", "text": f"Question: {q}\nAnswer the question using the chart.\n\nChart: "},
                {"type": "image"},
                {"type": "text", "text": f"\n\n{FORMAT_CHART}"},
            ]
        if arm == "base_text":
            return [{"type": "text", "text": f"Question: {q}\nAnswer the question using the report.\n\nReport:\n{item.text_question}\n\n{FORMAT_CHART}"}]
    raise ValueError(f"unknown base arm {arm!r}")


def has_image(content: Sequence[Dict[str, str]]) -> bool:
    return any(c["type"] == "image" for c in content)


def render_chat(apply_chat_template: Callable, content: Sequence[Dict[str, str]], prefill: Optional[str]) -> str:
    """Model input text, leaving the assistant turn open after any prefill."""
    messages: List[Dict[str, Any]] = [{"role": "user", "content": list(content)}]
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


def fake_qwen_chat_template(messages, tokenize=False, add_generation_prompt=False) -> str:
    """Test double that follows the Qwen2(.5)-VL chat template's structure.

    Image entries become <|vision_start|><|image_pad|><|vision_end|> in place; text is
    concatenated as is. The real template is checked on Colab with --print_example.
    """
    out = "<|im_start|>system\nYou are a helpful assistant.<|im_end|>\n"
    for m in messages:
        out += f"<|im_start|>{m['role']}\n"
        content = m["content"]
        if isinstance(content, str):
            out += content
        else:
            for c in content:
                out += "<|vision_start|><|image_pad|><|vision_end|>" if c["type"] == "image" else c["text"]
        out += "<|im_end|>\n"
    if add_generation_prompt:
        out += "<|im_start|>assistant\n"
    return out


def candidate_text(y: str) -> str:
    """How a gold answer is written as a continuation: '18.0' -> '18', '2.50' -> '2.5'."""
    s = str(y).strip()
    try:
        d = Decimal(s.replace(",", ""))
    except InvalidOperation:
        return s
    if d == d.to_integral_value():
        return str(d.to_integral_value())
    return format(d.normalize(), "f")


# ─── Requests and rows ───────────────────────────────────────────────────────


@dataclass
class Req:
    item: Item
    key: str  # unique within the run for this item
    content: List[Dict[str, str]]
    mode: str  # "generate" or "score"
    prefill: Optional[str] = None
    max_new_tokens: int = 512
    cell: Dict[str, Any] = field(default_factory=dict)

    @property
    def uses_image(self) -> bool:
        return has_image(self.content)


@dataclass
class V5Config:
    run_tag: str
    stage: str = "base"
    model_id: str = "Qwen/Qwen2.5-VL-3B-Instruct"
    model_revision: Optional[str] = None
    dataset_revision: Optional[str] = None
    split: str = "conflict"
    phase: str = "dev"
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
    max_new_tokens: int = 512  # read by the v4 backend; v5 sets it per request
    extra: Dict[str, Any] = field(default_factory=dict)

    @property
    def regime(self) -> str:
        return REGIME[self.split]


def row_id(item_id: str, key: str) -> str:
    return f"{key}|{item_id}"


def load_done(path: str) -> Set[str]:
    done: Set[str] = set()
    if not os.path.exists(path):
        return done
    with open(path, encoding="utf-8") as f:
        for line in f:
            try:
                row = json.loads(line)
            except json.JSONDecodeError:
                continue  # a line cut off by a crash is rerun
            done.add(row_id(row["id"], row["key"]))
    return done


def base_row(req: Req, cfg: V5Config, wall_s: float) -> Dict[str, Any]:
    return {
        "run_tag": cfg.run_tag,
        "stage": cfg.stage,
        "model_id": cfg.model_id,
        "split": cfg.split,
        "regime": cfg.regime,
        "phase": cfg.phase,
        "id": req.item.id,
        "source": req.item.source,
        "key": req.key,
        **req.cell,
        "y_image": req.item.y_image,
        "y_text": req.item.y_text,
        "content_sha1": hashlib.sha1(json.dumps(req.content, sort_keys=True).encode()).hexdigest()[:12],
        "prefill": req.prefill,
        "wall_s": round(wall_s, 3),
    }


# ─── Backends ────────────────────────────────────────────────────────────────


class EchoBackend:
    """A fake model for pipeline tests. Its numbers mean nothing."""

    name = "echo"
    apply_chat_template = staticmethod(fake_qwen_chat_template)

    def info(self) -> Dict[str, Any]:
        return {"backend": self.name, "warning": "fake outputs; not experimental data"}

    def generate(self, reqs: Sequence[Req], cfg: V5Config) -> List[Dict[str, Any]]:
        out = []
        for r in reqs:
            hsh = zlib.crc32((r.key + r.item.id + (r.prefill or "")).encode())
            pick = r.item.y_image if hsh % 3 == 0 else r.item.y_text if hsh % 3 == 1 else str(hsh % 97)
            family = r.cell.get("family", "")
            if family.startswith("base"):  # base arms answer correctly so dry runs reach the transplant
                gold = r.item.y_image if family == "base_image" else r.item.y_text
                out.append({"generated": f"Compute it.\n\n#### {gold}", "tokens": 3, "hit_cap": False})
                continue
            if r.prefill:
                body = f"{pick}" if r.prefill.endswith("####") else f"Compute it.\n\n#### {pick}"
            else:
                names = list(SOURCE_NAME[cfg.regime].values())
                side = names[0] if hsh % 5 == 0 else names[1]
                body = (
                    f"{names[0].capitalize()} and {names[1]} do not agree. "
                    f"I consider {side} more reliable.\n\nTo solve the problem, compute it.\n\n#### {pick}"
                )
            out.append({"generated": body, "tokens": len(body.split()), "hit_cap": False})
        return out

    def score(self, reqs: Sequence[Req], cfg: V5Config) -> List[Dict[str, Any]]:
        out = []
        for r in reqs:
            res: Dict[str, Any] = {}
            for side, y in (("image", r.item.y_image), ("text", r.item.y_text)):
                hsh = zlib.crc32((side + r.key + r.item.id + (r.prefill or "")).encode())
                n = max(1, len(candidate_text(y)) // 2)
                res[f"lp_{side}"] = -(hsh % 1000) / 100.0
                res[f"n_{side}"] = n
            res["boundary_mismatch"] = False
            res["verdict_nll"] = None
            res["ws_skipped"] = 0
            res["dl"] = sc.margin(res["lp_image"], res["n_image"], res["lp_text"], res["n_text"])
            out.append(res)
        return out


REQUIRED_DTYPE = "torch.bfloat16"  # prereg §3.4


def check_dtype(dtype: str) -> None:
    """Stop unless the model was loaded in the pre-registered dtype.

    h4.HFBackend picks bfloat16 on GPUs with compute capability >= 8 (L4, A100, RTX 30/40)
    and float16 below that (T4, V100). v5 fixes bfloat16 for every model, so a float16 or
    float32 load means the session is on the wrong GPU class.
    """
    if dtype != REQUIRED_DTYPE:
        raise SystemExit(
            f"v5 runs require {REQUIRED_DTYPE} (prereg §3.4) but this session loaded {dtype}. "
            "Use a GPU with compute capability >= 8 (L4, A100, RTX 3090/4090); T4 and V100 fall back to float16."
        )


class HFBackend(h4.HFBackend):
    """Transformers backend for v5 requests. Needs a GPU session; not run by local tests."""

    def __init__(self, cfg):
        super().__init__(cfg)
        check_dtype(self.dtype)

    @property
    def apply_chat_template(self):
        return self.processor.apply_chat_template

    def _encode(self, texts: Sequence[str], images):
        return self.processor(text=list(texts), images=images, return_tensors="pt", padding=True)

    def generate(self, reqs: Sequence[Req], cfg: V5Config) -> List[Dict[str, Any]]:
        t = self.torch
        uses_image = reqs[0].uses_image
        max_new = reqs[0].max_new_tokens
        if any(r.uses_image != uses_image or r.max_new_tokens != max_new for r in reqs):
            raise ValueError("a batch must share image use and max_new_tokens")
        texts = [render_chat(self.apply_chat_template, r.content, r.prefill) for r in reqs]
        images = [r.item.image.convert("RGB") for r in reqs] if uses_image else None
        try:
            inputs = self._encode(texts, images).to(self.model.device)
            prompt_len = inputs["input_ids"].shape[1]
            with t.inference_mode():
                output = self.model.generate(
                    **inputs,
                    max_new_tokens=max_new,
                    repetition_penalty=cfg.repetition_penalty,
                    do_sample=False,
                    temperature=None,
                    top_p=None,
                    top_k=None,
                )
        except t.cuda.OutOfMemoryError as exc:
            t.cuda.empty_cache()
            raise h4.BackendOutOfMemory() from exc
        results = []
        for row in output[:, prompt_len:].tolist():
            kept, reached_eos = h4.decode_ids(row, self.eos_ids, self.pad_id)
            text = self.processor.tokenizer.decode(kept, skip_special_tokens=True)
            results.append({"generated": text, "tokens": len(kept), "hit_cap": (not reached_eos) and len(kept) >= max_new})
        del inputs, output
        t.cuda.empty_cache()
        return results

    def _continuation(self, full_text: str, prefix_ids: List[int], images, extra_from: Optional[int] = None):
        """Summed log-prob of the tokens after prefix_ids, and of tokens from extra_from to the prefix end."""
        t = self.torch
        enc = self._encode([full_text], images).to(self.model.device)
        ids = enc["input_ids"][0].tolist()
        mismatch = ids[: len(prefix_ids)] != prefix_ids
        start = extra_from if extra_from is not None else len(prefix_ids)
        keep = len(ids) - start + 1  # logit rows needed: positions start-1 .. len-2
        with t.inference_mode():
            try:
                logits = self.model(**enc, logits_to_keep=keep).logits[0]
                offset = len(ids) - logits.shape[0]
            except TypeError:  # older transformers
                logits = self.model(**enc).logits[0]
                offset = 0
            lp = t.log_softmax(logits.float(), dim=-1)

        def total(a: int, b: int):
            pos = sc.continuation_positions(a, b)
            return float(sum(lp[row - offset, ids[tok]].item() for row, tok in pos)), len(pos)

        # A leading whitespace-only token is shared by both candidates and is not scored (prereg §6.1).
        tokenizer = self.processor.tokenizer
        skip = sc.leading_ws_skip([tokenizer.decode([i]) for i in ids[len(prefix_ids) :]]) if not mismatch else 0
        cont = total(len(prefix_ids) + skip, len(ids))
        extra = total(extra_from, len(prefix_ids)) if extra_from is not None and extra_from < len(prefix_ids) else None
        del enc, logits, lp
        return cont, extra, mismatch, skip

    def score(self, reqs: Sequence[Req], cfg: V5Config) -> List[Dict[str, Any]]:
        """Teacher-forced margin at '####' (prereg §6.1). One request at a time."""
        t = self.torch
        out = []
        for r in reqs:
            if not r.prefill or not r.prefill.endswith("####"):
                raise ValueError("score requests need a prefill ending in '####'")
            images = [r.item.image.convert("RGB")] if r.uses_image else None
            prefix = render_chat(self.apply_chat_template, r.content, r.prefill)
            base = render_chat(self.apply_chat_template, r.content, None)
            prefix_ids = self._encode([prefix], images)["input_ids"][0].tolist()
            base_ids = self._encode([base], images)["input_ids"][0].tolist()
            verdict_from = len(base_ids) if prefix.startswith(base) and prefix_ids[: len(base_ids)] == base_ids else None
            res: Dict[str, Any] = {"boundary_mismatch": False, "verdict_nll": None, "ws_skipped": 0}
            try:
                for side, y in (("image", r.item.y_image), ("text", r.item.y_text)):
                    full = prefix + " " + candidate_text(y)
                    (lp, n), extra, mismatch, skip = self._continuation(full, prefix_ids, images, verdict_from if side == "image" else None)
                    res[f"lp_{side}"], res[f"n_{side}"] = lp, n
                    res["boundary_mismatch"] |= mismatch
                    res["ws_skipped"] += skip
                    if extra is not None and extra[1] > 0:
                        res["verdict_nll"] = -extra[0] / extra[1]
            except t.cuda.OutOfMemoryError as exc:
                t.cuda.empty_cache()
                raise h4.BackendOutOfMemory() from exc
            res["dl"] = sc.margin(res["lp_image"], res["n_image"], res["lp_text"], res["n_text"])
            out.append(res)
            t.cuda.empty_cache()
        return out


# ─── Run loop ────────────────────────────────────────────────────────────────


def _safe(fn, batch, cfg):
    try:
        return fn(batch, cfg)
    except h4.BackendOutOfMemory:
        if len(batch) == 1:
            raise
        mid = len(batch) // 2
        return _safe(fn, batch[:mid], cfg) + _safe(fn, batch[mid:], cfg)


def run(reqs: Sequence[Req], backend, cfg: V5Config, out_path: str, log=print) -> int:
    """Run every request not already in out_path; append one JSONL row each."""
    done = load_done(out_path)
    groups: Dict[tuple, List[Req]] = {}
    for r in reqs:
        if row_id(r.item.id, r.key) not in done:
            groups.setdefault((r.mode, r.uses_image, r.max_new_tokens), []).append(r)
    written, start = 0, time.time()
    with open(out_path, "a", encoding="utf-8") as f:
        for (mode, _, _), pending in groups.items():
            fn = backend.generate if mode == "generate" else backend.score
            size = cfg.batch_size if mode == "generate" else 1
            for b in range(0, len(pending), size):
                batch = pending[b : b + size]
                t0 = time.time()
                results = _safe(fn, batch, cfg)
                per = (time.time() - t0) / len(batch)
                for req, res in zip(batch, results):
                    row = base_row(req, cfg, per)
                    row.update(res)
                    if mode == "generate":
                        row["full_text"] = (req.prefill or "") + res["generated"]
                    f.write(json.dumps(row, ensure_ascii=False) + "\n")
                f.flush()
                os.fsync(f.fileno())
                written += len(batch)
            log(f"[{time.strftime('%H:%M:%S')}] {mode}: {len(pending)} rows; {(time.time() - start) / 60:.1f} min elapsed")
    return written


def report_missing(reqs: Sequence[Req], out_path: str) -> int:
    done = load_done(out_path)
    missing = [row_id(r.item.id, r.key) for r in reqs if row_id(r.item.id, r.key) not in done]
    if missing:
        print(f"INCOMPLETE: {len(missing)} of {len(reqs)} requests have no row, e.g. {missing[:5]}. Rerun the same command.", file=sys.stderr)
        return 1
    print(f"Complete: all {len(reqs)} requests have a row.")
    return 0


# ─── Stage requests ──────────────────────────────────────────────────────────


def base_requests(items: Sequence[Item], regime: str) -> List[Req]:
    """Single-source arms: one generation (competency) and one gold-answer score (prereg §7.5) each."""
    max_new = 512 if regime == "math" else 64
    reqs = [
        Req(item=it, key=arm, content=build_base_content(regime, it, arm), mode="generate", max_new_tokens=max_new, cell={"family": arm, "outcome": "beh"})
        for arm in BASE_ARMS
        for it in items
    ]
    # Teacher-forced at '####' in the single-source prompt. Only the arm's own gold answer is
    # read from these rows: lp_image/n_image under base_image, lp_text/n_text under base_text.
    reqs += [
        Req(item=it, key=f"nll|{arm}", content=build_base_content(regime, it, arm), mode="score", prefill="####", max_new_tokens=0, cell={"family": arm, "outcome": "nll"})
        for arm in BASE_ARMS
        for it in items
    ]
    return reqs


def donor_requests(items: Sequence[Item], regime: str) -> List[Req]:
    """Free generation at k = 1 in both orders, with nothing forced.

    family "donor"         non-binding; its verbalization is the transplant donor (prereg §5.1)
    family "free_binding"  binding; used only for the manipulation check (prereg §7.5)
    """
    max_new = 512 if regime == "math" else 128
    reqs = []
    for family, instr_family, key in (("donor", "nonbinding", "donor"), ("free_binding", "binding", "free|binding")):
        for order in ORDERS:
            for it in items:
                instr = instruction(regime, instr_family, 1, it.image_only_question)
                reqs.append(
                    Req(
                        item=it,
                        key=f"{key}|{order}",
                        content=build_content(regime, it, instr, order),
                        mode="generate",
                        max_new_tokens=max_new,
                        cell={"family": family, "order": order, "O": ORDER_CODE[order], "k": 1, "outcome": "beh"},
                    )
                )
    return reqs


def base_correct(row: Dict[str, Any]) -> bool:
    """Did a base generation row give the gold answer for its source? Strict parsing (prereg §3.3)."""
    if "full_text" not in row:  # a gold-answer score row
        return False
    gold = row["y_image"] if row["family"] == "base_image" else row["y_text"]
    src, _, _ = sc.behavioural_source(row["full_text"], row["regime"], gold, gold)
    return src == "both"


def competent_ids(base_path: str) -> Set[str]:
    ok: Dict[str, Set[str]] = {}
    with open(base_path, encoding="utf-8") as f:
        for line in f:
            row = json.loads(line)
            if base_correct(row):
                ok.setdefault(row["id"], set()).add(row["family"])
    return {i for i, s in ok.items() if s == {"base_image", "base_text"}}


# ─── CLI ─────────────────────────────────────────────────────────────────────


def add_common_args(parser: argparse.ArgumentParser) -> None:
    parser.add_argument("--run_tag", required=True)
    parser.add_argument("--model_id", default="Qwen/Qwen2.5-VL-3B-Instruct", choices=sorted(MODEL_PINS))
    parser.add_argument("--model_revision", default=None)
    parser.add_argument("--dataset_revision", default=None)
    parser.add_argument("--split", default="conflict", choices=["conflict", "chartqa"])
    parser.add_argument("--phase", default="dev", choices=["dev", "confirm"])
    parser.add_argument("--dev_size", type=int, default=None, help="Default: 200 for conflict, 30 for chartqa")
    parser.add_argument("--batch_size", type=int, default=8)
    parser.add_argument("--max_pixels", type=int, default=256 * 28 * 28)
    parser.add_argument("--seed", type=int, default=42)
    parser.add_argument("--limit", type=int, default=None, help="For smoke tests only")
    parser.add_argument("--output_dir", default="results_v5")
    parser.add_argument("--dry_run", action="store_true", help="Fake model; stored v3 questions (conflict only)")
    parser.add_argument("--v3_results", default=os.path.join(HERE, "results_v3", "full_experiment_results v3.0.json"))


def config_from_args(args: argparse.Namespace, stage: str, **extra: Any) -> V5Config:
    dev_size = args.dev_size if args.dev_size is not None else (30 if args.split == "chartqa" else 200)
    if args.split == "chartqa" and dev_size >= 100:
        raise SystemExit("ChartQA has 229 analysed items; --dev_size must be small (prereg §3.2 uses 30).")
    cfg = V5Config(
        run_tag=args.run_tag,
        stage=stage,
        model_id=args.model_id,
        model_revision=args.model_revision,
        dataset_revision=args.dataset_revision,
        split=args.split,
        phase=args.phase,
        batch_size=args.batch_size,
        seed=args.seed,
        max_pixels=args.max_pixels,
        dev_size=dev_size,
        limit=args.limit,
        backend="echo" if args.dry_run else "transformers",
        extra=extra,
    )
    if cfg.model_revision is None:
        cfg.model_revision = MODEL_PINS.get(cfg.model_id)
    if cfg.dataset_revision is None:
        cfg.dataset_revision = DATASET_PINS.get(h4.CHARTQA_DATASET if cfg.split == "chartqa" else h4.CONFLICT_DATASET)
    return cfg


def select_items(args: argparse.Namespace, cfg: V5Config) -> List[Item]:
    if args.dry_run:
        if cfg.split != "conflict":
            raise SystemExit("--dry_run supports --split conflict only (stored v3 questions).")
        items = h4.load_items_from_v3(args.v3_results)
    else:
        items = load_items(cfg.split, cfg.dataset_revision)
    selected = h4.split_phase(items, cfg.phase, cfg.dev_size)
    return selected[: cfg.limit] if cfg.limit else selected


def print_example(args: argparse.Namespace, cfg: V5Config, items: Sequence[Item]) -> int:
    """Print the rendered chat for the first item in both orders (prereg §8)."""
    if args.dry_run:
        template = fake_qwen_chat_template
    else:
        from transformers import AutoProcessor

        template = AutoProcessor.from_pretrained(cfg.model_id, revision=cfg.model_revision).apply_chat_template
    it = items[0]
    for order in ORDERS:
        instr = instruction(cfg.regime, "binding", 1, it.image_only_question)
        print(f"===== {order} (binding, k=1) =====")
        print(render_chat(template, build_content(cfg.regime, it, instr, order), "The verdict.\n\n####"))
    return 0


def write_manifest(path: str, cfg: V5Config, backend, n_items: int, scripts: Sequence[str]) -> None:
    h4.write_manifest(path, cfg, backend, n_items, scripts)


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    add_common_args(parser)
    parser.add_argument("--stage", choices=["base", "donor"], default="base")
    parser.add_argument("--print_example", action="store_true")
    args = parser.parse_args()
    cfg = config_from_args(args, args.stage)
    items = select_items(args, cfg)
    if args.print_example:
        return print_example(args, cfg, items)
    reqs = base_requests(items, cfg.regime) if cfg.stage == "base" else donor_requests(items, cfg.regime)
    print(f"{len(items)} items, {len(reqs)} requests, stage={cfg.stage}, phase={cfg.phase}, model={cfg.model_id}")
    backend = EchoBackend() if args.dry_run else HFBackend(cfg)
    os.makedirs(args.output_dir, exist_ok=True)
    out_path = os.path.join(args.output_dir, f"{cfg.run_tag}.jsonl")
    manifest = os.path.join(args.output_dir, f"{cfg.run_tag}.manifest.json")
    scripts = [os.path.abspath(__file__), os.path.join(HERE, "score_v5.py"), os.path.join(HERE, "harness_v4.py"), os.path.join(HERE, "score_v4.py")]
    write_manifest(manifest, cfg, backend, len(items), scripts)
    written = run(reqs, backend, cfg, out_path)
    write_manifest(manifest, cfg, backend, len(items), scripts)
    print(f"Wrote {written} rows to {out_path}")
    return report_missing(reqs, out_path)


if __name__ == "__main__":
    sys.exit(main())
