#!/usr/bin/env python3
"""Stage runners for pilot_harness.py (Q1 utilization-length; Q2 Binding-ID
swap). RECONSTRUCTIVE implementations; pre-registered. See preregistration.md.
`run(cfg, ck, bundle, stage)` with stage in {"smoke", "q1", "q2"}.
"""
from __future__ import annotations

import os
import random

import numpy as np
import torch
from PIL import Image, ImageDraw

from pilot_harness import CFG, Ckpt, Bundle, tlog, vram_gb

PAD = "<|image_pad|>"
TINY = bool(os.environ.get("THESIS_TINY", ""))


# ---------------------------------------------------------------------------
# Synthetic stimuli
# ---------------------------------------------------------------------------
def draw_grid_image(rows) -> Image.Image:
    """rows: list of strings of equal length (one cell per symbol). 448x448,
    2 rows x 4 cols, cells 1/4 wide x 1/2 tall, symbols centered/large."""
    img = Image.new("RGB", (448, 448), "white")
    d = ImageDraw.Draw(img)
    n, m = len(rows), len(rows[0])
    cw, ch = 448 // m, 448 // n
    try:
        font = ImageFont.truetype(
            "C:/Windows/Fonts/arialbd.ttf" if os.name == "nt" else
            "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", 150)
    except Exception:
        font = ImageFont.load_default()
    for r in range(n):
        for c in range(m):
            d.text((c * cw + cw // 2, r * ch + ch // 2), rows[r][c],
                   fill="black", anchor="mm", font=font)
    return img


def make_balance_scene(count: int, seed: int) -> Image.Image:
    """Count-evidence scene: `count` red discs vs k blue, deterministic."""
    rng = random.Random(seed)
    img = Image.new("RGB", (448, 448), "white")
    d = ImageDraw.Draw(img)
    blue = rng.randint(1, 5)
    for i in range(count):
        x = 40 + i * 90
        d.ellipse((x, 60, x + 60, 120), fill="red", outline="black")
    for i in range(blue):
        x = 40 + i * 90
        d.ellipse((x, 300, x + 60, 360), fill="blue", outline="black")
    return img


# ---------------------------------------------------------------------------
# Q1 conditions (paired factorial, pre-registered)
# ---------------------------------------------------------------------------
def q1_prompts(idx: int, seed: int) -> dict:
    q = ("Q: How many red discs are shown in the image? "
         "Answer with a single number.")
    short = PAD + " " + q
    gold = str(3)  # all items share count=3 (see runner); deterministic
    long_reason = (
        "Let me think step by step about the image. I will first consider "
        "the arrangement and then count the items carefully. Looking at the "
        "sides of the picture, there are several discs. I count only the red "
        "ones and ignore everything drawn in another colour. I scan each row "
        "from top to bottom and note every red disc I encounter. Repeating "
        "the procedure once more to avoid a mistake confirms the number, so "
        "I will answer with that number only.")
    if TINY:
        long_reason = long_reason[:38]
    neutral = (
        "The image has been loaded and its dimensions were recorded. The "
        "file was opened, the format checked, and the resolution was "
        "verified to be within the expected range. Standard preprocessing, "
        "including brightness normalisation and contrast adjustment, was "
        "applied to every channel of the picture. Metadata such as file size, "
        "creation date and colour profile were also read and stored for the "
        "record. These bookkeeping steps are required before further "
        "analysis but do not change the content of the picture.")
    if TINY:
        neutral = neutral[:38]
    return {
        "gold": gold,
        "short": {"text": short, "answer_block": 0},
        "long": {"text": PAD + " " + q + "\n" + long_reason, "answer_block": 1},
        "neutral": {"text": PAD + " " + q + "\n" + neutral, "answer_block": 1},
        "posmatch_short": {"text": PAD + " " + q + " " + short.split(" ", 1)[1]
                          + "\n" + neutral, "answer_block": 1},
    }


def q1_teacher_metric(bundle: Bundle, p: dict, answer_idx: int, layers) -> float:
    """Mean over probe layers of vision-attention mass at answer token,
    minus the uniform null M/N."""
    att, n_vis, qlen, _ = bundle.attention(p, layers)
    sel = bundle.vision_pos(p)
    masses = []
    for l in layers:
        a = att[l][0]                       # (heads, q, k)
        row = a[:, answer_idx, :].float()   # (heads, k)
        norm = row.sum(dim=-1, keepdim=True)
        try:
            m = row[:, sel].sum(dim=-1) / norm.squeeze(-1)
        except Exception:
            m = torch.zeros(a.shape[0], device=a.device)
        masses.append(float(m.mean().cpu()))
    null = n_vis / qlen
    return float(np.mean(masses)) - null


WORDS = {"zero": "0", "one": "1", "two": "2", "three": "3", "four": "4",
         "five": "5", "six": "6", "seven": "7", "eight": "8", "nine": "9"}


def matched(gold: str, gen: str, tok) -> bool:
    """True if gold answer occurs in generated text as digit or number word."""
    gens = " ".join(gen.strip().split()).lower()
    if gold in gens:
        return True
    w = WORDS.get(gold)
    return bool(w and w in gens)


def run_q1(bundle: Bundle, ck: Ckpt, n: int, probe_layers):
    tlog("Q1 stage: n =", n, "probe layers", probe_layers)
    for i in range(n):
        img = make_balance_scene(3, seed=1000 + i)
        prompts = q1_prompts(i, i)
        gold = prompts["gold"]
        for cond, c in prompts.items():
            if not isinstance(c, dict):
                continue
            for metric in ("vig_mass", "correct"):
                if ck.done("q1", cond, str(i), metric):
                    continue
                p = bundle.prep(c["text"], img, chat=False)
                aidx = (p["input_ids"].shape[-1] - 1)
                if metric == "vig_mass":
                    val = q1_teacher_metric(bundle, p, aidx, probe_layers)
                else:
                    val = 1.0 if matched(gold, bundle.generate(p, 24), bundle.proc.tokenizer) else 0.0
                ck.put("q1", cond, str(i), metric, val)
                tlog("  q1", cond, i, metric, round(val, 4))
    tlog("Q1 done")


# ---------------------------------------------------------------------------
# Q2 swap machinery
# ---------------------------------------------------------------------------
def capture_input(bundle: Bundle, p: dict, layer: int) -> torch.Tensor:
    """Residual-stream input to `layer` for token positions (qlen, hidden)."""
    state = {}

    def pre(mod, inp):
        state["x"] = inp[0][0].detach().clone()
        return inp

    h = bundle.model.model.language_model.layers[layer].register_forward_pre_hook(pre)
    try:
        with torch.no_grad():
            bundle.model(pixel_values=p["pixel_values"],
                         image_grid_thw=p["image_grid_thw"],
                         input_ids=p["input_ids"], use_cache=False)
    finally:
        h.remove()
    return state["x"]


def patched_forward(bundle: Bundle, p: dict, layer: int, rows_idx: list[int],
                    src: torch.Tensor, scale: float) -> torch.Tensor:
    """Forward pass whose residual input at `layer` has rows `rows_idx`
    replaced by src[rows_idx]*scale + resid*(1-scale)."""
    if not rows_idx:
        with torch.no_grad():
            out = bundle.model(pixel_values=p["pixel_values"],
                               image_grid_thw=p["image_grid_thw"],
                               input_ids=p["input_ids"], use_cache=False)
        return out.logits[0, -1]

    def pre(mod, inp):
        x = inp[0][0]
        x = x.clone()
        x[rows_idx] = x[rows_idx] * (1 - scale) + src[rows_idx] * scale
        return (x, *inp[1:])

    h = bundle.model.model.language_model.layers[layer].register_forward_pre_hook(pre)
    try:
        with torch.no_grad():
            out = bundle.model(pixel_values=p["pixel_values"],
                               image_grid_thw=p["image_grid_thw"],
                               input_ids=p["input_ids"], use_cache=False)
    finally:
        h.remove()
    return out.logits[0, -1]  # next-token logits at final prompt position


def argmax_symbol(logits: torch.Tensor, symbols: list[str], tok) -> str:
    """Direct scoring over the symbol answer space (robust vs top-k drift)."""
    ids = [(tid, s) for s in symbols
           for tid in [tok.convert_tokens_to_ids(s)]
           if tid != getattr(tok, "unk_token_id", None)]
    if not ids:
        return "?"
    lg = logits[[tid for tid, _ in ids]]
    return ids[int(torch.argmax(lg))][1]


def q2_synthetic_sample(idx: int):
    rng = random.Random(2000 + idx)
    top = rng.sample(list("&$#@"), 4)
    bot = rng.sample(list("+%=!"), 4)
    qtext = (PAD + " Row 1 shows the symbols above the line and row 2 shows "
             "the symbols below the line. What symbol is in row 2, column 2? "
             "Answer with one symbol.")
    return {
        "top": list(top), "bot": list(bot),
        "img": draw_grid_image(["".join(top), "".join(bot)]),
        "text": qtext, "gold": bot[1], "col": 1,
    }


def run_q2(bundle: Bundle, ck: Ckpt, n: int, patch_layer: int):
    tok = bundle.proc.tokenizer
    symbols = list("&=#@+%!")
    tlog("Q2 stage: n =", n, "patch_layer", patch_layer)
    for i in range(n):
        s = q2_synthetic_sample(i)
        p = bundle.prep(s["text"], s["img"], chat=False)
        rows = bundle.vision_pos(p, rows=(1,))      # bottom row of grid image
        logits = patched_forward(bundle, p, patch_layer, [], torch.zeros(1), 0.0)
        pre = argmax_symbol(logits, symbols, tok)
        if pre != s["gold"]:
            tlog("  q2 skip (prepatch wrong)", i, pre, "!=", s["gold"])
            for cond in ("swap_src", "placebo_rand", "placebo_orth", "control"):
                ck.put("q2", cond, str(i), "net_flip", np.nan)
            continue
        rng2 = random.Random(3000 + i)
        top2 = list("&$#@")
        src_bot = rng2.sample(list("+%=!"), 4)
        src_img = draw_grid_image(["".join(top2), "".join(src_bot)])
        sp = bundle.prep(s["text"], src_img, chat=False)
        src = capture_input(bundle, sp, patch_layer)
        qlen = src.shape[0]
        rows = [r for r in rows if r < qlen]
        outs = {}
        for cond, scale, pattern in (("control", 0.0, None),
                                     ("placebo_rand", 1.0, "rand"),
                                     ("placebo_orth", 1.0, "orth"),
                                     ("swap_src", 1.0, "src")):
            if ck.done("q2", cond, str(i), "net_flip"):
                continue
            if cond == "placebo_rand":
                src_use_t = torch.randn_like(src)
                src_use_t *= (src.norm(dim=-1, keepdim=True) /
                              (src_use_t.norm(dim=-1, keepdim=True) + 1e-9))
            elif cond == "placebo_orth":
                src_use_t = src - (src @ torch.ones(src.shape[-1], device=src.device)
                                   / src.shape[-1]).unsqueeze(-1) * torch.ones(
                    src.shape[-1], device=src.device)
                src_use_t *= (src.norm(dim=-1, keepdim=True) /
                              (src_use_t.norm(dim=-1, keepdim=True) + 1e-9))
            else:
                src_use_t = src
            if scale == 0.0:
                src_use_t = torch.zeros_like(src)  # control = no patch
            lg = patched_forward(bundle, p, patch_layer, rows, src_use_t, scale)
            sym = argmax_symbol(lg, symbols, tok)
            net = 1.0 if sym == src_bot[1] else (0.5 if sym != pre else 0.0)
            outs[cond] = net
        for cond, v in outs.items():
            ck.put("q2", cond, str(i), "net_flip", v)
            tlog("  q2", cond, i, "net_flip", round(v, 3))
    tlog("Q2 done")


# ---------------------------------------------------------------------------
# Smoke
# ---------------------------------------------------------------------------
def run_smoke(bundle: Bundle, ck: Ckpt):
    tlog("smoke: 2 Q1 items + 2 Q2 items")
    run_q1(bundle, ck, n=2, probe_layers=bundle.cfg.q1_probe_layers)
    run_q2(bundle, ck, n=2, patch_layer=bundle.cfg.q2_patch_layer)
    tlog("smoke done; peak vram (GB):", round(vram_gb(), 2))


def run(cfg: CFG, ck: Ckpt, bundle: Bundle, stage: str):
    if stage == "smoke":
        run_smoke(bundle, ck)
    elif stage == "tiny":
        tlog("tiny mode (plumbing validation)")
        bundle.cfg.q1_n = 1
        run_q1(bundle, ck, n=1, probe_layers=(35,))
        run_q2(bundle, ck, n=1, patch_layer=cfg.q2_patch_layer)
    elif stage == "q1":
        run_q1(bundle, ck, n=cfg.q1_n, probe_layers=cfg.q1_probe_layers)
    elif stage == "q2":
        run_q2(bundle, ck, n=cfg.q2_n_synthetic, patch_layer=cfg.q2_patch_layer)
    else:
        raise SystemExit("unknown stage " + stage)
    tlog("pilot done; checkpoints in", cfg.ckpt)