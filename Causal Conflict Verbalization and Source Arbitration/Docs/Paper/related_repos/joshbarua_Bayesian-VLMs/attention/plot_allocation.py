#!/usr/bin/env python3
"""Plot relative image-vs-passage attention over the degradation grid."""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.colors import TwoSlopeNorm
import pandas as pd

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from config import get_run_dir


TEXT_LABELS = ("p=0", "p=0.20", "p=0.40", "p=0.60", "p=0.80", "p=1.00")


def load_allocation(run_dir: Path) -> pd.DataFrame:
    combined = run_dir / "allocation.parquet"
    paths = [combined] if combined.exists() else sorted(
        run_dir.glob("allocation_shard_*.parquet")
    )
    if not paths:
        raise FileNotFoundError(f"no allocation parquet files in {run_dir}")
    return pd.concat([pd.read_parquet(path) for path in paths], ignore_index=True)


def relative_image_surface(run_dir: Path) -> pd.DataFrame:
    frame = load_allocation(run_dir)
    required = {"blur_sigma", "text_level", "A_image", "A_passage"}
    missing = required - set(frame.columns)
    if missing:
        raise ValueError(f"{run_dir}: missing columns {sorted(missing)}")
    denominator = frame["A_image"] + frame["A_passage"]
    if (denominator <= 0).any():
        raise ValueError(f"{run_dir}: non-positive image + passage attention")
    frame = frame.assign(relative_image=frame["A_image"] / denominator)
    return frame.pivot_table(
        index="blur_sigma",
        columns="text_level",
        values="relative_image",
        aggfunc="mean",
    ).sort_index().sort_index(axis=1)


def annotation_color(value: float) -> str:
    return "white" if value <= 0.20 or value >= 0.80 else "black"


def plot(surfaces: list[tuple[str, pd.DataFrame]], out: Path) -> None:
    figure, axes = plt.subplots(
        len(surfaces), 1, figsize=(4.2, 7.0), squeeze=False,
        sharex=True, sharey=True,
    )
    norm = TwoSlopeNorm(vmin=0.0, vcenter=0.5, vmax=1.0)
    image = None
    for axis, (model, surface) in zip(axes[:, 0], surfaces):
        image = axis.imshow(
            surface.to_numpy(), origin="lower", cmap="RdBu", norm=norm,
            interpolation="nearest", aspect="equal",
        )
        axis.set_title(model, fontsize=15, pad=7)
        axis.set_xticks(range(surface.shape[1]), TEXT_LABELS[:surface.shape[1]])
        axis.set_yticks(
            range(surface.shape[0]),
            [rf"$\sigma$={value:g}" for value in surface.index],
        )
        axis.set_xlabel(r"Text Noise $p$", fontsize=13, labelpad=5)
        axis.set_ylabel(r"Blur $\sigma$", fontsize=13, labelpad=6)
        axis.tick_params(labelsize=10, length=3)
        axis.tick_params(axis="x", labelrotation=30, labelbottom=True)
        for tick in axis.get_xticklabels():
            tick.set_ha("right")
        for row in range(surface.shape[0]):
            for column in range(surface.shape[1]):
                value = float(surface.iloc[row, column])
                axis.text(
                    column, row, f"{value:.2f}", ha="center", va="center",
                    color=annotation_color(value), fontsize=8.5,
                )

    figure.subplots_adjust(left=0.21, right=0.79, bottom=0.08, top=0.965, hspace=0.30)
    colorbar_axis = figure.add_axes([0.84, 0.19, 0.035, 0.64])
    colorbar = figure.colorbar(image, cax=colorbar_axis, ticks=[0, .25, .5, .75, 1])
    colorbar.set_label("Relative Image Attention", fontsize=11, labelpad=8)
    out.parent.mkdir(parents=True, exist_ok=True)
    figure.savefig(out, dpi=240, facecolor="white", bbox_inches="tight")
    figure.savefig(out.with_suffix(".pdf"), facecolor="white", bbox_inches="tight")
    plt.close(figure)


def _parse_run(value: str) -> tuple[str, str]:
    if "=" not in value:
        raise argparse.ArgumentTypeError("runs must use LABEL=RUN_ID")
    return tuple(value.split("=", 1))


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--run", action="append", type=_parse_run, required=True,
        help="Model label and run id as LABEL=RUN_ID; pass once per model.",
    )
    parser.add_argument("--out", type=Path, default=Path("runs/attention_allocation.png"))
    args = parser.parse_args()
    plot(
        [(label, relative_image_surface(get_run_dir(run_id))) for label, run_id in args.run],
        args.out,
    )
    print(args.out)
    print(args.out.with_suffix(".pdf"))


if __name__ == "__main__":
    main()
