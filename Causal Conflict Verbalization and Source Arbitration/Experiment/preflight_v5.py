"""Pre-flight verification for v5 runs and preregistration freeze checks.

Checks:
1. Consistency between code pins/templates/lexicon and Docs/PREREGISTRATION_VERDICT_TRANSPLANT.md.
2. Presence and SHA-256 inventory of active Experiment/*_v5 scripts (and optional manifest hash matching).
3. Git cleanliness and tag resolution (required before confirmatory runs).
4. Optional GPU/CUDA/bfloat16/VRAM and package version checks (--check_gpu).
"""

from __future__ import annotations

import argparse
import hashlib
import importlib.metadata
import json
import os
import re
import subprocess
import sys
from typing import Any, Dict, Iterable, List, Mapping, Optional, Sequence, Tuple

HERE = os.path.dirname(os.path.abspath(__file__))
REPO_ROOT = os.path.dirname(HERE)
if HERE not in sys.path:
    sys.path.insert(0, HERE)

import harness_v4 as h4  # noqa: E402
import harness_v5 as h5  # noqa: E402
import transplant_v5 as tp5  # noqa: E402

DEFAULT_PREREG = os.path.join(REPO_ROOT, "Docs", "PREREGISTRATION_VERDICT_TRANSPLANT.md")
DEFAULT_PIP_FREEZE = os.path.join(HERE, "results_v5", "pip_freeze.txt")

CORE_SCRIPTS: Tuple[str, ...] = (
    "harness_v4.py",
    "harness_v5.py",
    "score_v4.py",
    "score_v5.py",
    "transplant_v5.py",
    "sample_v5_for_coding.py",
    "analyze_v5.py",
    "preflight_v5.py",
)

MIN_VRAM_GIB = 22.0
MIN_COMPUTE_CAPABILITY = (8, 0)

EXPECTED_PACKAGES: Dict[str, str] = {
    "torch": "2.14.1+cu130",
    "transformers": "5.22.1",
    "accelerate": "1.15.0",
    "datasets": "4.8.5",
    "pillow": "11.3.0",
    "qwen-vl-utils": "0.0.14",
}


def _iter_strings(obj: Any) -> Iterable[str]:
    """Yield leaf strings from nested strings, sequences, or mappings."""
    if isinstance(obj, str):
        yield obj
    elif isinstance(obj, Mapping):
        for val in obj.values():
            yield from _iter_strings(val)
    elif isinstance(obj, (list, tuple, set)):
        for item in obj:
            yield from _iter_strings(item)


def _iter_swap_pairs(swap_obj: Any) -> Iterable[Tuple[str, str]]:
    """Yield (source_phrase, replacement_phrase) pairs from dict or pair sequence."""
    if isinstance(swap_obj, Mapping):
        for k, v in swap_obj.items():
            yield str(k), str(v)
    elif isinstance(swap_obj, (list, tuple)):
        for entry in swap_obj:
            if isinstance(entry, (list, tuple)) and len(entry) >= 2:
                yield str(entry[0]), str(entry[1])


def _extract_section(text: str, heading_pattern: str) -> Optional[str]:
    """Extract a markdown section from a matching heading up to the next peer/higher heading."""
    match = re.search(heading_pattern, text, flags=re.MULTILINE)
    if not match:
        return None
    start = match.start()
    heading_line = text[start:text.find("\n", start)] if "\n" in text[start:] else text[start:]
    level = len(heading_line) - len(heading_line.lstrip("#"))
    rest = text[match.end():]
    next_heading = re.search(rf"^#{{1,{max(1, level)}}}\s+", rest, flags=re.MULTILINE)
    if next_heading:
        return text[start:match.end() + next_heading.start()]
    return text[start:]


def check_prereg_consistency(
    prereg_path: str = DEFAULT_PREREG,
    model_pins: Optional[Mapping[str, str]] = None,
    dataset_pins: Optional[Mapping[str, str]] = None,
) -> List[str]:
    """Verify code pins, prompt templates, and swap lexicons match the preregistration."""
    errors: List[str] = []
    if not os.path.isfile(prereg_path):
        flat_fallback = os.path.join(HERE, os.path.basename(prereg_path))
        if prereg_path == DEFAULT_PREREG and os.path.isfile(flat_fallback):
            prereg_path = flat_fallback
        else:
            return [f"Preregistration file not found: {prereg_path}"]

    with open(prereg_path, "r", encoding="utf-8") as fh:
        text = fh.read()

    active_model_pins = h4.MODEL_PINS if model_pins is None else model_pins
    active_dataset_pins = h4.DATASET_PINS if dataset_pins is None else dataset_pins

    for model_id, rev in active_model_pins.items():
        if model_id not in text:
            errors.append(f"Model ID missing from preregistration: {model_id}")
        if rev not in text:
            errors.append(f"Model revision pin missing from preregistration for {model_id}: {rev}")

    for ds_id, rev in active_dataset_pins.items():
        if ds_id not in text:
            errors.append(f"Dataset ID missing from preregistration: {ds_id}")
        if rev not in text:
            errors.append(f"Dataset revision pin missing from preregistration for {ds_id}: {rev}")

    if "bfloat16" not in text:
        errors.append("Required dtype 'bfloat16' not mentioned in preregistration.")
    if str(h5.MIN_PIXELS_PIN) not in text:
        errors.append(f"min_pixels pin {h5.MIN_PIXELS_PIN} not mentioned in preregistration.")
    for sp, px in h5.CONFIRM_MAX_PIXELS.items():
        if str(px) not in text:
            errors.append(f"Confirm max_pixels pin for {sp} ({px}) missing from preregistration.")

    for name, obj, replace_x in (
        ("MATH_STEMS", h5.MATH_STEMS, False),
        ("CHART_STEMS", h5.CHART_STEMS, False),
        ("FORMAT_MATH", h5.FORMAT_MATH, False),
        ("FORMAT_CHART", h5.FORMAT_CHART, False),
        ("MATH_ENDINGS", h5.MATH_ENDINGS, True),
        ("CHART_ENDINGS", h5.CHART_ENDINGS, True),
        ("PARA_TEMPLATES", tp5.PARA_TEMPLATES, True),
    ):
        for s in _iter_strings(obj):
            target = s.replace("{X}", "X") if replace_x else s
            if target not in text:
                errors.append(f"Template from {name} missing in preregistration: {target!r}")

    sec52 = _extract_section(text, r"^#{2,4}\s+5\.2\b")
    if sec52 is None:
        errors.append("Section 5.2 not found in preregistration for minimal-edit swap lexicon check.")
    else:
        for regime in ("math", "chartqa"):
            swap_entries = tp5._SWAP.get(regime, {})
            for src_phrase, dst_phrase in _iter_swap_pairs(swap_entries):
                if src_phrase not in sec52:
                    errors.append(
                        f"Swap source phrase missing in preregistration §5.2 ({regime}): {src_phrase!r}"
                    )
                if dst_phrase not in sec52:
                    errors.append(
                        f"Swap replacement phrase missing in preregistration §5.2 ({regime}): {dst_phrase!r}"
                    )

    return errors


def _sha256_file(path: str) -> str:
    h = hashlib.sha256()
    with open(path, "rb") as fh:
        for chunk in iter(lambda: fh.read(65536), b""):
            h.update(chunk)
    return h.hexdigest()


def check_scripts_sha256(
    scripts_dir: str = HERE,
    manifest_paths: Optional[Sequence[str]] = None,
) -> Tuple[Dict[str, str], List[str]]:
    """Compute SHA-256 digests for active scripts and optionally verify manifests."""
    hashes: Dict[str, str] = {}
    errors: List[str] = []

    for script_name in CORE_SCRIPTS:
        full_path = os.path.join(scripts_dir, script_name)
        if not os.path.isfile(full_path):
            errors.append(f"Core script missing: {full_path}")
        else:
            hashes[script_name] = _sha256_file(full_path)

    for mpath in manifest_paths or ():
        if not os.path.isfile(mpath):
            errors.append(f"Manifest not found: {mpath}")
            continue
        with open(mpath, "r", encoding="utf-8") as fh:
            manifest = json.load(fh)
        recorded = manifest.get("scripts_sha256", {})
        if not recorded:
            errors.append(f"Manifest has no scripts_sha256 field: {mpath}")
            continue
        for script_key, recorded_sha in recorded.items():
            base = os.path.basename(script_key)
            current_sha = hashes.get(base)
            if current_sha is None:
                candidate = os.path.join(scripts_dir, base)
                if os.path.isfile(candidate):
                    current_sha = _sha256_file(candidate)
            if current_sha is None:
                errors.append(f"Manifest {mpath} references missing script: {script_key}")
            elif current_sha != recorded_sha:
                errors.append(
                    f"Manifest {mpath} hash mismatch for {base}: recorded {recorded_sha[:12]} != disk {current_sha[:12]}"
                )

    return hashes, errors


def check_git_tag(require_tag: Optional[str] = None, repo_dir: str = REPO_ROOT) -> Tuple[Dict[str, Any], List[str]]:
    """Inspect git provenance and enforce clean tagged HEAD when require_tag is set."""
    prov = h4.git_provenance(repo_dir)
    errors: List[str] = []

    if not prov.get("git_commit"):
        if require_tag:
            errors.append(f"Unable to resolve git HEAD commit in {repo_dir}")
        return prov, errors

    if require_tag:
        if prov.get("git_dirty"):
            errors.append("Git working tree has uncommitted changes; commit and tag before confirm runs.")
        try:
            tag_commit = subprocess.check_output(
                ["git", "rev-parse", "--verify", f"{require_tag}^{{commit}}"],
                cwd=repo_dir,
                text=True,
                stderr=subprocess.STDOUT,
            ).strip()
            prov["required_tag"] = require_tag
            prov["required_tag_commit"] = tag_commit
            if tag_commit != prov.get("git_commit"):
                errors.append(
                    f"HEAD commit {prov['git_commit'][:12]} does not match required tag {require_tag!r} ({tag_commit[:12]})."
                )
        except subprocess.CalledProcessError:
            errors.append(f"Required git tag {require_tag!r} does not exist in {repo_dir}.")

    return prov, errors


def _load_expected_packages(pip_freeze_path: str) -> Dict[str, str]:
    expected = dict(EXPECTED_PACKAGES)
    if os.path.isfile(pip_freeze_path):
        with open(pip_freeze_path, "r", encoding="utf-8") as fh:
            for line in fh:
                line = line.strip()
                if not line or line.startswith("#") or "==" not in line:
                    continue
                name, ver = line.split("==", 1)
                key = name.strip().lower().replace("_", "-")
                if key in expected:
                    expected[key] = ver.strip()
    return expected


def check_gpu_env(pip_freeze_path: str = DEFAULT_PIP_FREEZE) -> Tuple[Dict[str, Any], List[str]]:
    """Verify CUDA GPU, bfloat16, >=22 GiB VRAM, >=SM8.0, and pinned package versions."""
    info: Dict[str, Any] = {}
    errors: List[str] = []

    try:
        import torch  # noqa: WPS433
    except Exception as exc:
        return info, [f"Failed to import torch for GPU preflight: {exc}"]

    info["torch"] = torch.__version__
    info["cuda_available"] = bool(torch.cuda.is_available())
    if not info["cuda_available"]:
        errors.append("CUDA is not available in this Python environment.")
        return info, errors

    props = torch.cuda.get_device_properties(0)
    cc = (int(props.major), int(props.minor))
    vram_gib = props.total_memory / (1024 ** 3)
    bf16_ok = bool(torch.cuda.is_bf16_supported())

    info.update(
        {
            "gpu_name": props.name,
            "compute_capability": list(cc),
            "vram_gib": round(vram_gib, 3),
            "bf16_supported": bf16_ok,
        }
    )

    if not bf16_ok:
        errors.append("CUDA device does not report bfloat16 support.")
    if cc < MIN_COMPUTE_CAPABILITY:
        errors.append(
            f"GPU compute capability {cc[0]}.{cc[1]} is below minimum {MIN_COMPUTE_CAPABILITY[0]}.{MIN_COMPUTE_CAPABILITY[1]}."
        )
    if vram_gib < MIN_VRAM_GIB:
        errors.append(f"GPU VRAM {vram_gib:.2f} GiB is below minimum {MIN_VRAM_GIB:.0f} GiB.")

    pkg_versions: Dict[str, Optional[str]] = {}
    for pkg, expected_ver in _load_expected_packages(pip_freeze_path).items():
        try:
            installed = importlib.metadata.version(pkg)
        except importlib.metadata.PackageNotFoundError:
            installed = None
        pkg_versions[pkg] = installed
        if installed is None:
            errors.append(f"Pinned package missing: {pkg}=={expected_ver}")
        elif installed != expected_ver:
            errors.append(f"Pinned package version mismatch for {pkg}: installed {installed!r} != expected {expected_ver!r}")
    info["packages"] = pkg_versions

    return info, errors


def run_preflight(
    phase: str = "dev",
    require_tag: Optional[str] = None,
    allow_untagged: bool = False,
    check_gpu: bool = False,
    prereg_path: str = DEFAULT_PREREG,
    manifest_paths: Optional[Sequence[str]] = None,
    pip_freeze_path: str = DEFAULT_PIP_FREEZE,
) -> Dict[str, Any]:
    """Run all requested v5 pre-flight checks and return a structured report."""
    effective_tag = require_tag
    if phase == "confirm" and not effective_tag and not allow_untagged:
        effective_tag = "prereg-v5"

    errors: List[str] = []
    prereg_errors = check_prereg_consistency(prereg_path=prereg_path)
    errors.extend(prereg_errors)

    script_hashes, script_errors = check_scripts_sha256(manifest_paths=manifest_paths)
    errors.extend(script_errors)

    git_prov, git_errors = check_git_tag(require_tag=effective_tag)
    errors.extend(git_errors)

    gpu_info: Dict[str, Any] = {}
    if check_gpu:
        gpu_info, gpu_errors = check_gpu_env(pip_freeze_path=pip_freeze_path)
        errors.extend(gpu_errors)

    return {
        "ok": len(errors) == 0,
        "phase": phase,
        "require_tag": effective_tag,
        "errors": errors,
        "git": git_prov,
        "scripts_sha256": script_hashes,
        "gpu": gpu_info if check_gpu else None,
    }


def main(argv: Optional[Sequence[str]] = None) -> int:
    parser = argparse.ArgumentParser(description="Pre-flight checker for v5 preregistration and GPU runs.")
    parser.add_argument("--phase", choices=["dev", "confirm"], default="dev")
    parser.add_argument("--require_tag", default=None, help="Git tag required at HEAD (defaults to prereg-v5 in confirm phase).")
    parser.add_argument("--allow_untagged", action="store_true", help="Skip required git tag check in confirm phase.")
    parser.add_argument("--check_gpu", action="store_true", help="Verify CUDA GPU (>=22 GiB, SM>=8.0, bf16) and package pins.")
    parser.add_argument("--check_manifests", nargs="*", default=None, help="Optional manifest JSON files to verify against disk script hashes.")
    parser.add_argument("--prereg", default=DEFAULT_PREREG)
    parser.add_argument("--pip_freeze", default=DEFAULT_PIP_FREEZE)
    parser.add_argument("--json", action="store_true", help="Emit JSON report.")
    args = parser.parse_args(argv)

    report = run_preflight(
        phase=args.phase,
        require_tag=args.require_tag,
        allow_untagged=args.allow_untagged,
        check_gpu=args.check_gpu,
        prereg_path=args.prereg,
        manifest_paths=args.check_manifests,
        pip_freeze_path=args.pip_freeze,
    )

    if args.json:
        print(json.dumps(report, indent=2, sort_keys=True))
    else:
        status = "OK" if report["ok"] else "FAILED"
        print(f"[preflight_v5] {status} (phase={report['phase']}, commit={report['git'].get('git_commit')}, dirty={report['git'].get('git_dirty')})")
        print(f"[preflight_v5] Scripts verified: {len(report['scripts_sha256'])}/{len(CORE_SCRIPTS)}")
        if report["gpu"] is not None:
            print(f"[preflight_v5] GPU: {report['gpu']}")
        for err in report["errors"]:
            print(f"  ERROR: {err}", file=sys.stderr)

    return 0 if report["ok"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
