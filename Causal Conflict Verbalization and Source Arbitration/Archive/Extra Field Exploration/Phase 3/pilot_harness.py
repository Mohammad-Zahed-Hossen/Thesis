#!/usr/bin/env python3
"""Phase-3 pilot harness: Q1 (visual-evidence utilization vs reasoning length)
and Q2 (Binding-ID swap: synthetic + natural images). RECONSTRUCTIVE harness;
not the original A1/C1 implementation. Pre-registered numbers in
preregistration.md. Verified on CPU pre-flight (see phase3-report Sec. 10):
placeholder is "<|image_pad|>"; vision_start/end are NOT in input_ids (1:1
replace -> attention qlen == input_ids len); attentions need eager backend;
residual capture via model.model.language_model.layers[L].

Run (Colab 16 GB):  python pilot_harness.py --smoke | --stage q1|q2
Checkpoints to pilot_results.csv beside this file; resumes safely.
"""
from __future__ import annotations

import argparse, csv, os, random, time
from dataclasses import dataclass

import numpy as np
import torch
from PIL import Image

try:
    import psutil
except Exception:
    psutil = None


@dataclass
class CFG:
    model_id: str = "Qwen/Qwen2.5-VL-3B-Instruct"
    dtype: str = "bfloat16"
    max_pixels: int = 448 * 448
    seed: int = 7
    q1_n: int = 50
    gen_max_new: int = 180
    q1_probe_layers: tuple = (11, 23, 35)
    q2_n_synthetic: int = 25
    q2_n_natural: int = 25
    q2_patch_layer: int = 12
    q2_rows: tuple = ("&", "$", "#", "@")
    vram_budget_gb: float = 16.0
    ckpt: str = os.path.join(os.path.dirname(os.path.abspath(__file__)), "pilot_results.csv")


def tlog(*a):
    print("[%s]" % time.strftime("%H:%M:%S"), *a, flush=True)


def vram_gb():
    if torch.cuda.is_available():
        return torch.cuda.max_memory_allocated() / 2 ** 30
    p = psutil.Process() if psutil else None
    return p.memory_info().rss / 2 ** 30 if p else -1.0


class Ckpt:
    def __init__(self, path, seed):
        self.path, self.seed = path, seed
        self.fields = ["seed", "stage", "condition", "sample_id", "metric",
                       "value", "vram_gb", "wall_s"]
        self.rows = {}
        if os.path.exists(path):
            with open(path, newline="", encoding="utf-8") as f:
                for r in csv.DictReader(f):
                    self.rows[(r["stage"], r["condition"], r["sample_id"], r["metric"])] = r
        else:
            self._header()

    def _header(self):
        with open(self.path, "w", newline="", encoding="utf-8") as f:
            csv.DictWriter(f, fieldnames=self.fields).writeheader()

    def done(self, stage, cond, sid, metric):
        return (stage, cond, sid, metric) in self.rows

    def put(self, stage, cond, sid, metric, value):
        if self.done(stage, cond, sid, metric):
            return False
        row = {"seed": self.seed, "stage": stage, "condition": cond,
               "sample_id": sid, "metric": metric, "value": round(float(value), 6),
               "vram_gb": round(vram_gb(), 3), "wall_s": round(time.time() - t0, 3)}
        with open(self.path, "a", newline="", encoding="utf-8") as f:
            csv.DictWriter(f, fieldnames=self.fields).writerow(row)
        self.rows[(stage, cond, sid, metric)] = row
        return True


t0 = time.time()


class Bundle:
    def __init__(self, cfg: CFG):
        import transformers
        from transformers import Qwen2_5_VLProcessor
        sdtype = torch.bfloat16 if cfg.dtype == "bfloat16" else torch.float16
        self.device = "cuda" if torch.cuda.is_available() else "cpu"
        tlog("loading", cfg.model_id, "on", self.device)
        self.model = transformers.AutoModelForImageTextToText.from_pretrained(
            cfg.model_id, torch_dtype=sdtype, attn_implementation="eager",
            low_cpu_mem_usage=True).to(self.device).eval()
        self.proc = Qwen2_5_VLProcessor.from_pretrained(cfg.model_id)
        self.pad_id = self.proc.tokenizer.convert_tokens_to_ids("<|image_pad|>")
        self.cfg = cfg
        self.hooks = []
        self.swap_spec = None
        tlog("ready; peak vram (GB):", round(vram_gb(), 2))

    # ---- input prep ------------------------------------------------------
    def prep(self, text, image, chat=True):
        assert text.count("<|image_pad|>") == 1, text
        if not chat:
            inputs = self.proc(text=text, images=[image], return_tensors="pt",
                               max_pixels=self.cfg.max_pixels).to(self.device)
        else:
            msgs = [{"role": "user", "content": [
                {"type": "image"}, {"type": "text", "text": text.replace("<|image_pad|>", "")}]}]
            inputs = self.proc.apply_chat_template(
                msgs, add_generation_prompt=True, return_tensors="pt",
                max_pixels=self.cfg.max_pixels).to(self.device)
            inputs = self.proc(text=text, images=[image], return_tensors="pt",
                               max_pixels=self.cfg.max_pixels).to(self.device)
        ids = inputs["input_ids"]
        pad = ids == self.pad_id
        n_vis = int(pad.sum())
        gt = inputs.get("image_grid_thw", torch.tensor([[0, 1, 1]], device=self.device))
        num_patches = [int(x) for x in gt[0, 1:3]]
        return {**inputs, "n_vis": n_vis,
                "num_patches": num_patches, "pad_mask": pad}

    def vision_pos(self, p, rows=()):
        h, w = p["num_patches"]
        mw = max(1, w // 2)
        idx = p["pad_mask"][0].nonzero().squeeze(1).tolist()
        out = []
        for i, tid in enumerate(idx):
            mr = divmod(i, mw)[0]
            if not rows or mr in rows:
                out.append(int(tid))
        return out

    # ---- teacher-forced metric pass --------------------------------------
    def attention(self, p, probe_layers):
        with torch.no_grad():
            out = self.model(pixel_values=p["pixel_values"],
                             image_grid_thw=p["image_grid_thw"],
                             input_ids=p["input_ids"],
                             output_attentions=True,
                             output_hidden_states=False,
                             use_cache=False)
        att = out.attentions
        qlen = att[0].shape[-1]
        assert qlen == p["input_ids"].shape[-1], (qlen, p["input_ids"].shape[-1])
        return att, p["n_vis"], p["input_ids"].shape[-1], p

    def generate(self, p, max_new):
        out = self.model.generate(
            **{k: p[k] for k in ("input_ids", "pixel_values", "image_grid_thw")},
            max_new_tokens=max_new, do_sample=False, use_cache=True,
            pad_token_id=self.proc.tokenizer.eos_token_id)
        return self.proc.tokenizer.decode(out[0][p["input_ids"].shape[-1]:],
                                          skip_special_tokens=True)


def parse_args():
    ap = argparse.ArgumentParser()
    ap.add_argument("--smoke", action="store_true")
    ap.add_argument("--tiny", action="store_true")
    ap.add_argument("--stage", choices=["q1", "q2"], required=False)
    return ap.parse_args()


if __name__ == "__main__":
    args = parse_args()
    cfg = CFG()
    random.seed(cfg.seed)
    np.random.seed(cfg.seed)
    torch.manual_seed(cfg.seed)
    ck = Ckpt(cfg.ckpt, cfg.seed)
    tlog("checkpoint:", cfg.ckpt)
    bundle = Bundle(cfg)

    from pilot_run import run  # stage runners (lazy import; same worktree)

    stage = "tiny" if args.tiny else ("smoke" if args.smoke else args.stage)
    if stage is None:
        raise SystemExit("pass --smoke, --tiny, or --stage q1|q2")
    run(cfg, ck, bundle, stage)