#!/usr/bin/env python3
"""
build_normalized_dataset.py -- Create a pixel-count-normalised copy of the dataset.

Different dataset splits can have very different image resolutions (e.g. DocVQA
document scans are ~15× larger in area than VQAv2 natural photos).  This produces
far more visual tokens for high-resolution splits, confounding any cross-dataset
attention or token-routing analysis.

This script resizes every image (up or down) so its total pixel count is as
close as possible to a shared target (by default: the overall median pixel count
across all splits).  Aspect ratio is preserved.  A --max_upscale cap (default 4×)
prevents extreme interpolation artefacts on tiny images.

Output dataset is saved to dataset_pixnorm/ (or --out_dir) in the same
HuggingFace datasets format as the original, so all downstream scripts can be
pointed at it with --dataset_path.

Usage
-----
  python build_normalized_dataset.py
  python build_normalized_dataset.py --target_pixels 262144   # fixed 512×512 equiv
  python build_normalized_dataset.py --out_dir dataset_pixnorm_512
"""

import argparse
import json
from pathlib import Path

import numpy as np
from PIL import Image, ImageDraw, ImageFont
from datasets import load_from_disk, DatasetDict
from tqdm import tqdm


# ---------------------------------------------------------------------------
# Resize helper
# ---------------------------------------------------------------------------

def resize_to_target_pixels(
    img: Image.Image,
    target_pixels: int,
    max_upscale: float = 4.0,
) -> Image.Image:
    """
    Resize img so total pixels ≈ target_pixels, preserving aspect ratio.

    - Images larger than target are downsampled (LANCZOS).
    - Images smaller than target are upsampled (BICUBIC), but only up to
      max_upscale× in linear dimension (default 4×, i.e. 16× area).
      Beyond that cap the image is left at the cap size rather than stretching
      further, to avoid extreme interpolation artefacts.
    """
    w, h = img.size
    current_pixels = w * h
    scale = (target_pixels / current_pixels) ** 0.5

    if scale > 1.0:
        # Upsampling: cap at max_upscale
        scale = min(scale, max_upscale)
        resample = Image.BICUBIC
    else:
        resample = Image.LANCZOS

    if abs(scale - 1.0) < 1e-3:
        return img

    new_w = max(1, int(w * scale))
    new_h = max(1, int(h * scale))
    return img.resize((new_w, new_h), resample)


# ---------------------------------------------------------------------------
# Resize-example visualiser
# ---------------------------------------------------------------------------

def save_resize_examples(
    all_examples: list,
    target_px: int,
    max_upscale: float,
    out_dir: Path,
    n: int = 3,
    display_h: int = 400,
) -> None:
    """
    Save side-by-side before/after PNGs for the n most extreme upsample and
    downsample cases into out_dir/resize_examples/{upsample,downsample}/.

    Ranking is by ideal (uncapped) scale factor, so a capped image that
    *would* have needed 10× still ranks above one that needed 3×.
    """
    try:
        font = ImageFont.truetype("DejaVuSans.ttf", 14)
    except (OSError, IOError):
        font = ImageFont.load_default()

    # Compute ideal and applied scale for every example
    records = []
    for ex in all_examples:
        w, h = ex["image"].size
        px = w * h
        ideal_scale = (target_px / px) ** 0.5
        if ideal_scale > 1.0:
            applied_scale = min(ideal_scale, max_upscale)
        else:
            applied_scale = ideal_scale
        records.append({
            "image":         ex["image"],
            "dataset":       ex["dataset"],
            "orig_size":     (w, h),
            "ideal_scale":   ideal_scale,
            "applied_scale": applied_scale,
        })

    upsample = sorted(
        [r for r in records if r["ideal_scale"] > 1.001],
        key=lambda r: r["ideal_scale"], reverse=True,
    )[:n]
    downsample = sorted(
        [r for r in records if r["applied_scale"] < 0.999],
        key=lambda r: r["applied_scale"],
    )[:n]

    header_h = 44  # px reserved for text label at top

    def fit_to_height(img: Image.Image, h: int) -> Image.Image:
        scale = h / img.height
        return img.resize((max(1, int(img.width * scale)), h), Image.LANCZOS)

    for category, cases in [("upsample", upsample), ("downsample", downsample)]:
        cat_dir = out_dir / "resize_examples" / category
        cat_dir.mkdir(parents=True, exist_ok=True)

        for rank, rec in enumerate(cases, 1):
            orig_img    = rec["image"].convert("RGB")
            resized_img = resize_to_target_pixels(orig_img, target_px, max_upscale)

            orig_disp    = fit_to_height(orig_img,    display_h)
            resized_disp = fit_to_height(resized_img, display_h)

            gap     = 8
            total_w = orig_disp.width + gap + resized_disp.width
            total_h = header_h + display_h

            canvas = Image.new("RGB", (total_w, total_h), color=(245, 245, 245))
            canvas.paste(orig_disp,    (0,                          header_h))
            canvas.paste(resized_disp, (orig_disp.width + gap,      header_h))

            ow, oh = rec["orig_size"]
            rw, rh = resized_img.size
            capped  = " [capped]" if rec["ideal_scale"] > max_upscale else ""
            label   = (
                f"[{rec['dataset']}]  {category}  #{rank}  "
                f"before: {ow}×{oh} ({ow*oh/1e3:.0f} kpx)  →  "
                f"after: {rw}×{rh} ({rw*rh/1e3:.0f} kpx)  "
                f"scale: {rec['applied_scale']:.2f}×{capped}"
            )

            draw = ImageDraw.Draw(canvas)
            draw.rectangle([(0, 0), (total_w, header_h - 1)], fill=(30, 30, 30))
            draw.text((8, 14), label, fill=(240, 240, 240), font=font)
            # Divider line between panels
            x_div = orig_disp.width + gap // 2
            draw.line([(x_div, header_h), (x_div, total_h)], fill=(180, 180, 180), width=2)

            out_path = cat_dir / f"rank{rank}_{rec['dataset']}.png"
            canvas.save(str(out_path))
            print(f"    {out_path.relative_to(out_dir)}")


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------

def main():
    parser = argparse.ArgumentParser(
        description="Build pixel-count-normalised copy of the conflicting_modality dataset"
    )
    parser.add_argument(
        "--dataset_dir", type=str,
        default=str(Path(__file__).parent / "dataset"),
        help="Path to the original HuggingFace dataset (default: dataset/)",
    )
    parser.add_argument(
        "--out_dir", type=str,
        default=str(Path(__file__).parent / "dataset_pixnorm"),
        help="Output directory for the normalised dataset",
    )
    parser.add_argument(
        "--target_pixels", type=int, default=None,
        help=(
            "Target total pixels per image (images are resized up OR down). "
            "Default: overall median pixel count across all splits."
        ),
    )
    parser.add_argument(
        "--target_dataset", type=str, default=None,
        help=(
            "Compute target pixel count from this dataset split's mean "
            "(e.g. 'VQAv2'). Default: use overall median across all splits."
        ),
    )
    parser.add_argument(
        "--max_upscale", type=float, default=4.0,
        help=(
            "Maximum linear upscale factor for images smaller than target_pixels "
            "(default: 4.0 = up to 16× area).  Images requiring more are capped "
            "at max_upscale× their original size."
        ),
    )
    args = parser.parse_args()

    dataset_dir = Path(args.dataset_dir)
    out_dir     = Path(args.out_dir)

    # -----------------------------------------------------------------------
    # Load dataset (lazy — images stay on disk until accessed)
    # -----------------------------------------------------------------------
    print(f"Loading dataset from {dataset_dir} …")
    ds_dict = load_from_disk(str(dataset_dir))
    total = sum(len(ds_dict[s]) for s in ds_dict)
    print(f"  {total} total examples across {list(ds_dict.keys())}")

    # -----------------------------------------------------------------------
    # Collect pixel counts and dataset labels WITHOUT decoding images.
    # HF datasets store image dimensions in metadata when saved via
    # save_to_disk, so we iterate with decode=False to read only the
    # file paths / bytes, then open just to get .size.
    # -----------------------------------------------------------------------
    print("Collecting image dimensions …")
    per_ds_pixels: dict[str, list[int]] = {}
    all_pixels_list: list[int] = []
    # Index for finding resize extremes later: (split_name, row_idx, pixel_count)
    _pixel_index: list[tuple[str, int, int]] = []

    for split_name in ds_dict:
        ds = ds_dict[split_name]
        for i in tqdm(range(len(ds)), desc=f"  {split_name}", leave=False):
            ex = ds[i]
            px = ex["image"].size[0] * ex["image"].size[1]
            ds_name = ex["dataset"]
            per_ds_pixels.setdefault(ds_name, []).append(px)
            all_pixels_list.append(px)
            _pixel_index.append((split_name, i, px))

    all_pixels = np.array(all_pixels_list)
    ds_names = sorted(per_ds_pixels.keys())

    # -----------------------------------------------------------------------
    # Compute target pixel count
    # -----------------------------------------------------------------------
    if args.target_pixels is not None:
        target_px = args.target_pixels
        print(f"Using user-specified target: {target_px:,} px  "
              f"(≈ {int(target_px**0.5)}px equiv square)")
    elif args.target_dataset is not None:
        ref_pixels = per_ds_pixels.get(args.target_dataset)
        if not ref_pixels:
            raise ValueError(f"No examples found for --target_dataset '{args.target_dataset}'. "
                             f"Available: {ds_names}")
        ref_arr = np.array(ref_pixels)
        target_px = int(np.mean(ref_arr))
        print(f"{args.target_dataset} pixel stats (n={len(ref_arr)}): "
              f"mean={np.mean(ref_arr):,.0f}  "
              f"median={np.median(ref_arr):,.0f}  "
              f"std={np.std(ref_arr):,.0f}")
        print(f"Target pixel count ({args.target_dataset} mean): {target_px:,}  "
              f"(≈ {int(target_px**0.5)}px equiv square)")
    else:
        target_px = int(np.median(all_pixels))
        print(f"Overall pixel stats (n={len(all_pixels)}): "
              f"mean={np.mean(all_pixels):,.0f}  "
              f"median={np.median(all_pixels):,.0f}  "
              f"std={np.std(all_pixels):,.0f}")
        print(f"Target pixel count (overall median): {target_px:,}  "
              f"(≈ {int(target_px**0.5)}px equiv square)")

    # -----------------------------------------------------------------------
    # Analyse before / after
    # -----------------------------------------------------------------------
    print("\nPer-dataset pixel stats (before normalisation):")
    for ds_name in ds_names:
        px_vals = np.array(per_ds_pixels[ds_name])
        print(f"  {ds_name}: mean={np.mean(px_vals)/1e6:.2f}MP  "
              f"median={np.median(px_vals)/1e6:.2f}MP  "
              f"max={np.max(px_vals)/1e6:.2f}MP")

    # Expected Qwen2.5-VL visual tokens after normalisation:
    # n_vis_tokens ≈ n_patches / 4  where n_patches = W*H / (14*14)
    patch_area = 14 * 14  # 196 px per patch
    print(f"\nExpected Qwen2.5-VL visual tokens after normalisation "
          f"(target={target_px:,} px):")
    for ds_name in ds_names:
        px_vals = np.array(per_ds_pixels[ds_name])
        # Mirror the bidirectional resize logic (with upscale cap)
        scales  = np.sqrt(target_px / px_vals)
        scales  = np.where(scales > 1.0, np.minimum(scales, args.max_upscale), scales)
        normed  = (px_vals * scales ** 2).astype(int)
        vis_tok = normed / patch_area / 4
        print(f"  {ds_name}: mean≈{vis_tok.mean():.0f}  "
              f"median≈{np.median(vis_tok):.0f}  "
              f"(was mean≈{px_vals.mean()/patch_area/4:.0f})")

    # -----------------------------------------------------------------------
    # Apply normalisation split-by-split and save
    # -----------------------------------------------------------------------
    out_dir.mkdir(parents=True, exist_ok=True)
    print(f"\nNormalising and saving to {out_dir} …")

    def normalise_example(example):
        example["image"] = resize_to_target_pixels(
            example["image"], target_px, max_upscale=args.max_upscale
        )
        return example

    new_splits = {}
    for split_name in ds_dict:
        print(f"  Processing split '{split_name}' "
              f"({len(ds_dict[split_name])} examples) …")
        new_splits[split_name] = ds_dict[split_name].map(
            normalise_example,
            desc=f"  Resizing {split_name}",
        )

    new_ds_dict = DatasetDict(new_splits)
    new_ds_dict.save_to_disk(str(out_dir))

    # -----------------------------------------------------------------------
    # Save resize-quality examples (top 3 upsample + top 3 downsample)
    # Use the pixel counts we already collected to find extremes, then
    # load only those few images.
    # -----------------------------------------------------------------------
    print("\nSaving resize-quality examples …")
    n_examples = 3
    _with_scale = [(r, (target_px / r[2]) ** 0.5) for r in _pixel_index]
    upsample_cands = sorted([x for x in _with_scale if x[1] > 1.001],
                            key=lambda x: x[1], reverse=True)[:n_examples]
    downsample_cands = sorted([x for x in _with_scale if x[1] < 0.999],
                              key=lambda x: x[1])[:n_examples]
    extreme_examples = [ds_dict[sn][idx] for (sn, idx, _), _ in upsample_cands + downsample_cands]
    if extreme_examples:
        save_resize_examples(extreme_examples, target_px, args.max_upscale, out_dir)

    # -----------------------------------------------------------------------
    # Save metadata
    # -----------------------------------------------------------------------
    meta = {
        "source_dir":    str(dataset_dir),
        "out_dir":       str(out_dir),
        "target_pixels": target_px,
        "target_sqrt":   int(target_px ** 0.5),
        "max_upscale": args.max_upscale,
        "note": (
            "Images resized (up BICUBIC / down LANCZOS) to target_pixels. "
            "Upscaling capped at max_upscale× linear.  Aspect ratio preserved."
        ),
    }
    with open(out_dir / "normalisation_meta.json", "w") as f:
        json.dump(meta, f, indent=2)

    # -----------------------------------------------------------------------
    # Verification
    # -----------------------------------------------------------------------
    print("\nVerification — pixel stats after normalisation:")
    verify_dict = load_from_disk(str(out_dir))
    verify_pixels: dict[str, list[int]] = {}
    for split_name in verify_dict:
        ds = verify_dict[split_name]
        for i in range(len(ds)):
            ex = ds[i]
            px = ex["image"].size[0] * ex["image"].size[1]
            verify_pixels.setdefault(ex["dataset"], []).append(px)
    for ds_name in ds_names:
        px_vals = np.array(verify_pixels.get(ds_name, []))
        orig_px = np.array(per_ds_pixels[ds_name])
        n_changed = int(np.sum(orig_px != target_px))
        if len(px_vals) == 0:
            print(f"  {ds_name}: (no examples)")
            continue
        print(f"  {ds_name}: mean={np.mean(px_vals)/1e6:.3f}MP  "
              f"median={np.median(px_vals)/1e6:.3f}MP  "
              f"min={np.min(px_vals)/1e6:.3f}MP  "
              f"max={np.max(px_vals)/1e6:.3f}MP  "
              f"({n_changed} images resized)")

    print(f"\nDone.  Normalised dataset saved to {out_dir}")
    print(f"Use with: --dataset_path {out_dir}")


if __name__ == "__main__":
    main()
