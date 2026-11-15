"""Shared setup and resumable parquet output for the three paper sweeps."""

from __future__ import annotations

import argparse
import json
import sys
import time
from dataclasses import dataclass
from pathlib import Path
from typing import Iterable

import pandas as pd
import torch

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from config import DEFAULT_SEED, QWEN_MODEL, get_run_dir, load_degradation_meta
from attention.model_loader import load_model_and_processor
from attention.patch_hooks import get_layers
from attention.readout import Readout
from attention.stimuli import (
    StimulusBuilder,
    TextVariants,
    build_example_index,
    load_corpus,
    load_splits,
    stratified_sample,
)


DTYPES = {
    "float32": torch.float32,
    "bfloat16": torch.bfloat16,
    "float16": torch.float16,
}


def add_common_args(parser: argparse.ArgumentParser) -> None:
    parser.add_argument("--run_id", required=True)
    parser.add_argument(
        "--deg_run_id", required=True,
        help="Behavioral run supplying splits.json and degradation_meta.json.",
    )
    parser.add_argument("--model_name", default=QWEN_MODEL)
    parser.add_argument("--dataset_path", default=None)
    parser.add_argument("--seed", type=int, default=DEFAULT_SEED)
    parser.add_argument("--dtype", choices=sorted(DTYPES), default="float32")
    parser.add_argument("--split", default="test")
    parser.add_argument(
        "--n_examples", type=int, default=416,
        help="Cap per split; 416 selects all 413 valid examples in the paper test split.",
    )
    parser.add_argument("--shard_id", type=int, default=None)
    parser.add_argument("--num_shards", type=int, default=None)
    parser.add_argument("--checkpoint_every", type=int, default=5)
    parser.add_argument("--overwrite", action="store_true")


@dataclass
class Setup:
    args: argparse.Namespace
    model: object
    processor: object
    adapter: object
    builder: StimulusBuilder
    examples: object
    id_to_local: list[tuple[str, int]]
    ids: list[int]
    layers: list[int]
    n_layers: int
    readout: Readout
    run_dir: Path
    meta: dict

    def example(self, idx: int):
        dataset, local_idx = self.id_to_local[idx]
        return self.examples[dataset][local_idx], dataset, local_idx


def prepare(args: argparse.Namespace) -> Setup:
    if (args.shard_id is None) != (args.num_shards is None):
        raise SystemExit("--shard_id and --num_shards must be supplied together")
    if args.num_shards is not None and not 0 <= args.shard_id < args.num_shards:
        raise SystemExit("--shard_id must be in [0, --num_shards)")

    run_dir = get_run_dir(args.run_id)
    run_dir.mkdir(parents=True, exist_ok=True)
    meta = load_degradation_meta(get_run_dir(args.deg_run_id))
    splits = load_splits(args.deg_run_id)
    datasets, source = load_corpus(args.dataset_path)
    id_to_local = build_example_index(datasets)
    print(f"Dataset: {source} ({len(id_to_local)} examples)")

    ids: list[int] = []
    for split in (part.strip() for part in args.split.split(",")):
        if not split:
            continue
        if split not in splits:
            raise KeyError(f"split {split!r} not found; available: {sorted(splits)}")
        selected = stratified_sample(
            splits[split], id_to_local, args.n_examples, args.seed
        )
        print(f"  split {split}: {len(selected)} ids")
        ids.extend(selected)
    ids = sorted(set(ids))
    if args.shard_id is not None:
        ids = ids[args.shard_id :: args.num_shards]
        print(f"Shard {args.shard_id}/{args.num_shards}: {len(ids)} ids")

    model, processor, adapter = load_model_and_processor(
        args.model_name, dtype=DTYPES[args.dtype]
    )
    n_layers = len(get_layers(model, adapter))
    layers = list(range(1, n_layers + 1))
    builder = StimulusBuilder(adapter, TextVariants(meta["grid"]))
    return Setup(
        args=args,
        model=model,
        processor=processor,
        adapter=adapter,
        builder=builder,
        examples=datasets,
        id_to_local=id_to_local,
        ids=ids,
        layers=layers,
        n_layers=n_layers,
        readout=Readout(model),
        run_dir=run_dir,
        meta=meta,
    )


class ShardedWriter:
    """Checkpoint rows by example and merge them atomically at completion."""

    def __init__(self, run_dir: Path, stem: str, *, shard_id: int | None,
                 checkpoint_every: int = 5, overwrite: bool = False):
        suffix = "" if shard_id is None else f"_shard_{shard_id}"
        self.out_path = run_dir / f"{stem}{suffix}.parquet"
        self.parts_dir = run_dir / f".{stem}{suffix}.parts"
        self.meta_path = run_dir / f"{stem}{suffix}_meta.json"
        self.checkpoint_every = max(1, checkpoint_every)
        self.overwrite = overwrite
        self.rows: list[dict] = []
        self.chunk = 0
        self.done_ids: set[int] = set()
        self.started = time.time()

    def already_complete(self) -> bool:
        return self.out_path.exists() and not self.overwrite

    def open(self):
        self.parts_dir.mkdir(parents=True, exist_ok=True)
        for path in sorted(self.parts_dir.glob("chunk_*.parquet")):
            frame = pd.read_parquet(path, columns=["id"])
            self.done_ids.update(int(value) for value in frame["id"].unique())
            self.chunk = max(self.chunk, int(path.stem.rsplit("_", 1)[1]) + 1)
        if self.done_ids:
            print(f"Resume: {len(self.done_ids)} ids already written")
        return self

    def pending(self, ids: Iterable[int]) -> list[int]:
        return [idx for idx in ids if int(idx) not in self.done_ids]

    def add(self, rows: list[dict]) -> None:
        self.rows.extend(rows)

    def flush(self) -> None:
        if not self.rows:
            return
        path = self.parts_dir / f"chunk_{self.chunk:04d}.parquet"
        tmp = path.with_suffix(".parquet.tmp")
        pd.DataFrame(self.rows).to_parquet(tmp, index=False)
        tmp.rename(path)
        self.rows.clear()
        self.chunk += 1

    def maybe_flush(self, index: int) -> None:
        if (index + 1) % self.checkpoint_every == 0:
            self.flush()

    def finalize(self, metadata: dict) -> int:
        self.flush()
        parts = sorted(self.parts_dir.glob("chunk_*.parquet"))
        frame = (
            pd.concat([pd.read_parquet(path) for path in parts], ignore_index=True)
            if parts else pd.DataFrame()
        )
        tmp = self.out_path.with_suffix(".parquet.tmp")
        frame.to_parquet(tmp, index=False)
        tmp.rename(self.out_path)
        for path in parts:
            path.unlink()
        self.parts_dir.rmdir()
        metadata = dict(metadata)
        metadata.update(n_rows=len(frame), elapsed_sec=time.time() - self.started)
        self.meta_path.write_text(json.dumps(metadata, indent=2, default=str) + "\n")
        print(f"Wrote {len(frame)} rows -> {self.out_path}")
        return len(frame)


def run_meta(setup: Setup, extra: dict | None = None) -> dict:
    args = setup.args
    metadata = {
        "model_name": args.model_name,
        "dtype": args.dtype,
        "deg_run_id": args.deg_run_id,
        "split": args.split,
        "n_ids": len(setup.ids),
        "layers": setup.layers,
        "n_layers_total": setup.n_layers,
        "prompt_order": "image_first",
        "seed": args.seed,
        "readout": setup.readout.calibration_report(),
    }
    if extra:
        metadata.update(extra)
    return metadata
