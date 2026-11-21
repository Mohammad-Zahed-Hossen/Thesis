# End-to-End Confirmatory Execution Runbook: `v5confirm` (`prereg-v5`)

Complete, fail-fast execution guide for the **confirmatory v5 experiment (`--phase confirm`)** on a GPU session (Google Colab Pro notebook cells or RunPod `tmux` shell), running strictly from the frozen git tag **`prereg-v5`** (`8bb6ca23bdcd926e90f78f3e457327cf595aed4b`).

- **Canonical short reference:** [`Experiment/RUNBOOK_v5.md`](../../../Experiment/RUNBOOK_v5.md) §6
- **Frozen pre-registration (`prereg-v5`):** [`Docs/PREREGISTRATION_VERDICT_TRANSPLANT.md`](../../../Docs/PREREGISTRATION_VERDICT_TRANSPLANT.md)
- **Prior dev runbook (reference only):** [`RUNBOOK_V5_DEV_LATEST.md`](RUNBOOK_V5_DEV_LATEST.md)
- **Hardware & precision invariant (§3.4):** CUDA compute capability `>= 8.0`, usable VRAM `>= 22 GiB`, `torch.bfloat16` — **NVIDIA L4 (24 GB)**, **A100 (40/80 GB)**, or **RTX 3090/4090**. **Never use a T4 or V100** (`harness_v5.HFBackend` stops on `float16`).
- **One GPU class & one `--batch_size` per model × regime:** All three stages (`base`, `donor`, `transplant`) of any model × regime **must** run on the exact same GPU model and `--batch_size`. The notebook wrappers below write and enforce `$OUT_DIR/gpu_lock_<block>.json` so a reconnect onto a different GPU halts immediately.

---

## Scope, Sample Sizes & Runtime Budget

Timings below scale directly from the `2026-11-15/16` L4 `bfloat16` dev rerun (`1,396` confirm Math items vs. `200` dev Math items; `structured` competency parser; `--n_competent 250` confirm cap per R5):

| Block | Model ID | Split & Role | Pool (`items`) | Stage 1 (`base`) | Stage 2 (`donor`) | Stage 3 (`tp`, `<= 250` items) | Total Est. Time (VRAM) |
|---|---|---|---|---|---|---|---|
| **1 (Confirmatory)** | `Qwen/Qwen2.5-VL-3B-Instruct` (`qwen25`) | `conflict` (Math, primary) | `1,396` | `5,584` rows (~1.9h L4) | `5,584` rows (~3.0h L4) | Up to `30,000` rows (~4.2h L4) | **~9h on L4 (`BS=8`, ~7.5 GB)** |
| **2 (Confirmatory)** | `Qwen/Qwen2.5-VL-7B-Instruct` (`qwen25_7b`) | `conflict` (Math, primary) | `1,396` | `5,584` rows (~7.8h L4) | `5,584` rows (~12.0h L4) | ~`27,000` rows (~11.2h L4) | **~31h on L4 (`BS=2`, ~15.7 GB)** / **~10–12h on A100 (`BS=8`)** |
| *(Excluded, D3)* | `Qwen/Qwen2-VL-2B-Instruct` | Math confirm excluded | — | — | — | — | Diagnostic-only (`0/200` Math dev competency); refused by `--phase confirm` |
| *(Optional, D4)* | `Qwen/Qwen2.5-VL-3B/7B` | `chartqa` (Exploratory) | `199` | `796` rows | `796` rows | Up to `23,880` rows (stops at exit `2` if `<100` pass or `<60%` rate) | Run **only after** Blocks 1 & 2 finish; `max_pixels=200704` locked (§3.4) |

### Unattended Execution Safety

- **What `Experiment/*.py` enforces automatically in `--phase confirm`:**
  - `preflight_v5.py --phase confirm --require_tag prereg-v5 --check_gpu`: GPU compute capability `>= 8.0`, VRAM `>= 22.0 GiB`, exact package pins from `results_v5/pip_freeze.txt`, `8/8` script hashes, clean git `HEAD == prereg-v5` (`8bb6ca23bdcd926e90f78f3e457327cf595aed4b`), and prereg §8 human-coding gate (`evaluation_v5.json` + `adjudication_v5.csv`).
  - `harness_v5.py` / `transplant_v5.py`: refuses `--limit`, non-pinned revisions/pixels, `--n_competent != 250` on Math, `--competency_parser != structured`, diagnostic-only `2B` on Math, non-`bfloat16` dtypes, or dirty/untagged git checkouts; fsyncs every batch; repairs cut-off trailing JSONL lines on resume; records append-only `invocations[]` + `resolved_model_commit` in every `.manifest.json`.
- **What the Cell 1 helpers add on top:**
  - Persistent output directory (`OUT_DIR` on Google Drive or RunPod Network Volume `/workspace`) paired with a clean `/content/Thesis` or `/tmp/Thesis` clone on fast local disk (no `.git` contention, `git status` stays clean).
  - Live-streaming `run_checked(...)` that raises `RuntimeError` immediately on any unexpected non-zero exit code.
  - Exact row verification (`assert_jsonl_rows`) after `base`, `donor`, and `transplant`.
  - Per-block **GPU + batch-size lock** (`$OUT_DIR/gpu_lock_<block>.json`) to catch GPU changes across Colab reconnects.
  - Immediate credential stripping from `.git/config` after cloning a private repo.

---

## Step 0 — Pre-Launch Checklist (Local, 1 Minute)

1. Confirm `prereg-v5` on GitHub points to `8bb6ca23bdcd926e90f78f3e457327cf595aed4b` (`git rev-parse HEAD 'refs/tags/prereg-v5^{commit}'`).
2. **If `Mohammad-Zahed-Hossen/Thesis` is Private on GitHub:** generate a fine-grained **read-only (`Contents: Read-only`)** GitHub Personal Access Token (PAT) for this single repository.
   - **Recommended on Colab:** save it in Colab **Secrets** (left sidebar key icon) as `GITHUB_PAT` and toggle notebook access ON. If you skip Colab Secrets, Cell 1 prompts via masked `getpass`.
   - *(Optional)* Save a Hugging Face token as Colab Secret `HF_TOKEN` (or env var `HF_TOKEN`) to avoid anonymous Hub rate limits.

---

## Step 1 — Setup, `prereg-v5` Checkout, Pinned Packages & Preflight (Cells 1–3)

Open a new Colab Pro notebook attached to an **L4** (for 3B or budget 7B) or **A100** (for fast 7B) runtime, or start a Jupyter/RunPod session on the target GPU.

### Cell 1 — Mount Persistent Storage, Clone `prereg-v5` & Define Fail-Fast Helpers

```python
import getpass
import json
import os
import subprocess
import sys

IS_COLAB = "google.colab" in sys.modules or os.path.isdir("/content")

if IS_COLAB:
    from google.colab import drive  # type: ignore

    drive.mount("/content/drive")
    REPO_PARENT = "/content"
    OUT_DIR = "/content/drive/MyDrive/Thesis_v5/results_v5_confirm"
else:
    REPO_PARENT = "/tmp"
    OUT_DIR = "/workspace/results_v5_confirm" if os.path.isdir("/workspace") else os.path.expanduser("~/Thesis_v5/results_v5_confirm")

os.makedirs(OUT_DIR, exist_ok=True)
REPO_DIR = os.path.join(REPO_PARENT, "Thesis")
WORK_DIR = os.path.join(REPO_DIR, "Causal Conflict Verbalization and Source Arbitration")
EXP_DIR = os.path.join(WORK_DIR, "Experiment")
TARGET_TAG = "prereg-v5"
EXPECTED_TAG_COMMIT = "8bb6ca23bdcd926e90f78f3e457327cf595aed4b"
PUBLIC_URL = "https://github.com/Mohammad-Zahed-Hossen/Thesis.git"

# Optional HF token from Colab Secrets
if IS_COLAB and not os.environ.get("HF_TOKEN"):
    try:
        from google.colab import userdata  # type: ignore

        hf_tok = userdata.get("HF_TOKEN")
        if hf_tok:
            os.environ["HF_TOKEN"] = hf_tok.strip()
    except Exception:
        pass

if not os.path.isdir(os.path.join(REPO_DIR, ".git")):
    gh_pat = os.environ.get("GITHUB_PAT", "").strip()
    if not gh_pat and IS_COLAB:
        try:
            from google.colab import userdata  # type: ignore

            gh_pat = (userdata.get("GITHUB_PAT") or "").strip()
        except Exception:
            gh_pat = ""
    if not gh_pat:
        gh_pat = getpass.getpass("GitHub read-only PAT (leave blank if repo is public): ").strip()
    clone_url = f"https://x-access-token:{gh_pat}@github.com/Mohammad-Zahed-Hossen/Thesis.git" if gh_pat else PUBLIC_URL
    subprocess.run(["git", "clone", clone_url, REPO_DIR], check=True)
    # Strip any embedded PAT immediately so .git/config and Drive stay secret-free
    subprocess.run(["git", "-C", REPO_DIR, "remote", "set-url", "origin", PUBLIC_URL], check=True)
    del gh_pat, clone_url

subprocess.run(["git", "-C", REPO_DIR, "checkout", TARGET_TAG], check=True)
head_sha = subprocess.check_output(["git", "-C", REPO_DIR, "rev-parse", "HEAD"], text=True).strip()
tag_sha = subprocess.check_output(["git", "-C", REPO_DIR, "rev-parse", f"refs/tags/{TARGET_TAG}^{{commit}}"], text=True).strip()
dirty = subprocess.check_output(["git", "-C", REPO_DIR, "status", "--short"], text=True).strip()

assert head_sha == EXPECTED_TAG_COMMIT, f"HEAD mismatch: {head_sha} != {EXPECTED_TAG_COMMIT}"
assert tag_sha == EXPECTED_TAG_COMMIT, f"Tag mismatch: {tag_sha} != {EXPECTED_TAG_COMMIT}"
assert dirty == "", f"Git checkout is dirty:\n{dirty}"

os.chdir(EXP_DIR)
print(f"[OK] Working directory: {os.getcwd()}")
print(f"[OK] Tag {TARGET_TAG} -> {head_sha}")
print(f"[OK] Persistent OUT_DIR: {OUT_DIR}")


def run_checked(cmd: str, allow_r5_stop_tag: str | None = None) -> int:
    """Stream command output live and raise immediately on unexpected failure."""
    print(f"\n>>> {cmd}", flush=True)
    proc = subprocess.Popen(
        cmd,
        shell=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        text=True,
        bufsize=1,
    )
    assert proc.stdout is not None
    for line in proc.stdout:
        sys.stdout.write(line)
        sys.stdout.flush()
    rc = proc.wait()
    if rc != 0:
        if allow_r5_stop_tag and rc == 2:
            gpath = os.path.join(OUT_DIR, f"{allow_r5_stop_tag}.gates.json")
            if os.path.exists(gpath):
                gates = json.load(open(gpath, encoding="utf-8"))
                if (not gates.get("edit_gate_ok")) or (not gates.get("meets_min_items")):
                    print(
                        f"[INFO] {allow_r5_stop_tag}: R5 stopping rule triggered "
                        f"(passed={gates.get('passed')}, rate={gates.get('edit_gate_pass_rate')}, "
                        f"fails={gates.get('fail_reasons_by_order')}). Valid outcome; continuing.",
                        flush=True,
                    )
                    return rc
        raise RuntimeError(f"Command failed (exit={rc}): {cmd}")
    return rc


def assert_jsonl_rows(path: str, expected_rows: int) -> None:
    """Verify prerequisite JSONL exists, is valid JSON per line, and matches exact expected count."""
    if not os.path.exists(path):
        raise FileNotFoundError(f"Missing JSONL: {path}")
    count = 0
    with open(path, encoding="utf-8") as fh:
        for line in fh:
            if line.strip():
                json.loads(line)
                count += 1
    if count != expected_rows:
        raise RuntimeError(f"{path}: expected {expected_rows} rows, found {count}")
    print(f"[OK] {os.path.basename(path)}: {count}/{expected_rows} rows verified.", flush=True)


def lock_gpu_and_batch_size(block_key: str, batch_size: int) -> None:
    """Pin GPU model and batch size across all stages & resumes of a model x regime block."""
    import torch

    assert torch.cuda.is_available(), "CUDA is not available"
    props = torch.cuda.get_device_properties(0)
    current = {
        "gpu_name": props.name,
        "vram_gib": round(props.total_memory / (1024 ** 3), 2),
        "batch_size": int(batch_size),
    }
    lock_path = os.path.join(OUT_DIR, f"gpu_lock_{block_key}.json")
    if os.path.exists(lock_path):
        locked = json.load(open(lock_path, encoding="utf-8"))
        if locked["gpu_name"] != current["gpu_name"] or locked["batch_size"] != current["batch_size"]:
            raise RuntimeError(
                f"GPU/batch-size lock mismatch for {block_key}! Locked={locked}, current={current}. "
                "Do NOT mix GPU models or batch sizes inside one model x regime."
            )
        print(f"[OK] GPU lock verified for {block_key}: {locked['gpu_name']} | BS={locked['batch_size']}", flush=True)
    else:
        with open(lock_path, "w", encoding="utf-8") as fh:
            json.dump(current, fh, indent=2)
        print(f"[OK] Created GPU lock for {block_key}: {current['gpu_name']} | BS={current['batch_size']}", flush=True)


def assert_confirm_gates_ready(gates_path: str, split: str) -> int:
    """Inspect --gates_only output before launching full transplant scoring."""
    g = json.load(open(gates_path, encoding="utf-8"))
    print(
        f"[GATES] {os.path.basename(gates_path)}: items={g['items']} | competent={g['competent']} | "
        f"taken={g['taken']} | passed={g['passed']} | pass_rate={g['edit_gate_pass_rate']} | "
        f"edit_gate_ok={g['edit_gate_ok']} | meets_min_items={g['meets_min_items']} | "
        f"fails={g.get('fail_reasons_by_order')}",
        flush=True,
    )
    if split == "conflict":
        assert g["competent"] >= 250, f"Expected >=250 competent Math items, got {g['competent']}"
        assert g["taken"] == 250, f"Expected taken=250 on Math confirm, got {g['taken']}"
    assert g["edit_gate_ok"], f"R5 edit_gate_ok is False for {split}: {g}"
    assert g["meets_min_items"], f"R5 meets_min_items is False for {split}: {g}"
    return int(g["passed"])
```

### Cell 2 — Verify/Install Pinned Packages & Run Strict Confirm Preflight

Checks currently installed package versions first so it only reinstalls mismatched packages (skipping a multi-minute `torch` wheel download if `2.14.1+cu130` is already active), then enforces `preflight_v5.py --phase confirm --require_tag prereg-v5 --check_gpu --json`.

```python
import importlib.metadata as meta

PINS = {
    "torch": "2.14.1+cu130",
    "transformers": "5.22.1",
    "accelerate": "1.15.0",
    "datasets": "4.8.5",
    "pillow": "11.3.0",
    "qwen-vl-utils": "0.0.14",
}

mismatched = []
for pkg, expected in PINS.items():
    try:
        actual = meta.version(pkg)
    except meta.PackageNotFoundError:
        actual = None
    if actual != expected:
        mismatched.append((pkg, expected, actual))
    print(f"pkg {pkg}: installed={actual!r} | expected={expected!r}")

if any(p == "torch" for p, _, _ in mismatched):
    run_checked("pip install -q torch==2.14.1+cu130 --index-url https://download.pytorch.org/whl/cu130")
other_pkgs = [f"{p}=={exp}" for p, exp, _ in mismatched if p != "torch"]
if other_pkgs:
    run_checked("pip install -q " + " ".join(other_pkgs))

run_checked("nvidia-smi")

pf_raw = subprocess.check_output(
    ["python", "-B", "preflight_v5.py", "--phase", "confirm", "--require_tag", "prereg-v5", "--check_gpu", "--json"],
    text=True,
)
print(pf_raw)
pf = json.loads(pf_raw)
assert pf["ok"] is True and pf["errors"] == [], f"Confirm preflight failed: {pf['errors']}"
assert pf["git"]["git_dirty"] is False, f"Git tree dirty: {pf['git']}"
assert pf["git"]["prereg_tag"] == "prereg-v5", f"Bad prereg_tag: {pf['git']}"
assert pf["git"]["prereg_tag_commit"] == EXPECTED_TAG_COMMIT
assert pf["git"]["git_commit"] == EXPECTED_TAG_COMMIT
assert pf["gpu"]["bf16_supported"] is True and pf["gpu"]["vram_gib"] >= 22.0

freeze_out = subprocess.check_output(["pip", "freeze"], text=True)
with open(os.path.join(OUT_DIR, "pip_freeze_confirm.txt"), "w", encoding="utf-8") as fh:
    fh.write(freeze_out)

BS_3B = 8
BS_7B = 8 if pf["gpu"]["vram_gib"] >= 38.0 else 2
print(f"\n[PREFLIGHT PASSED] GPU={pf['gpu']['gpu_name']} ({pf['gpu']['vram_gib']} GiB) | BS_3B={BS_3B} | BS_7B={BS_7B}")
```

*(Pass criterion: prints `[PREFLIGHT PASSED]`, confirms `git_dirty: false`, `prereg_tag: "prereg-v5"`, and sets `BS_3B = 8`, `BS_7B = 2` on L4/24 GB or `8` on A100 40/80 GB.)*

### Cell 3 — Automated Confirm Render Gate (`--print_example`, `3B` & `7B`)

```python
MODELS_CONFIRM = [
    "Qwen/Qwen2.5-VL-3B-Instruct",
    "Qwen/Qwen2.5-VL-7B-Instruct",
]

for split in ("conflict", "chartqa"):
    img_hdr = "Image: " if split == "conflict" else "Chart: "
    txt_hdr = "Typed text:\n" if split == "conflict" else "Report:\n"
    vis = "<|vision_start|><|image_pad|><|vision_end|>"
    for model_id in MODELS_CONFIRM:
        cmd = [
            "python", "-B", "harness_v5.py",
            "--print_example", "--split", split, "--phase", "confirm",
            "--run_tag", "render_confirm_check", "--model_id", model_id,
        ]
        res = subprocess.run(cmd, capture_output=True, text=True, check=True)
        out = res.stdout
        assert "===== image.size:" in out, f"Missing image.size header for {split} {model_id}"
        assert "min_pixels=100352, max_pixels=200704" in out, f"Wrong pixel cap line for {split} {model_id}"
        if split == "chartqa":
            assert "800x557 (445600 px; min_pixels=100352, max_pixels=200704)" in out, out[:400]
        assert "Source A" not in out and "Source B" not in out, f"Forbidden Source A/B in {split} {model_id}"
        m1 = "===== image_first (binding, k=1) ====="
        m2 = "===== text_first (binding, k=1) ====="
        assert m1 in out and m2 in out, f"Missing order sections in {split} {model_id}"
        img_part, txt_part = out.split(m1, 1)[1].split(m2, 1)
        for label, part in (("image_first", img_part), ("text_first", txt_part)):
            assert f"{img_hdr}{vis}" in part, f"Vision tag misaligned in {split} {model_id} {label}"
            assert part.rstrip().endswith("The verdict.\n\n####"), f"Bad prefill suffix in {split} {model_id} {label}"
        assert img_part.index(vis) < img_part.index(txt_hdr), f"Wrong order in image_first ({split} {model_id})"
        assert txt_part.index(txt_hdr) < txt_part.index(vis), f"Wrong order in text_first ({split} {model_id})"
        print(f"[PASS] confirm render check: split={split} | model={model_id}")

print("\nALL 4 CONFIRM RENDER CHECKS PASSED AUTOMATICALLY.")
```

*(Once Cell 3 passes, you can run Cells 4–6 unattended overnight via **Runtime -> Run after** or individually.)*

---

## Step 2 — Confirmatory Block 1: `Qwen/Qwen2.5-VL-3B-Instruct` on Math (Cells 4–6)

Estimated L4 wall time (`BS=8`): **~1.9h (Cell 4) + ~3.0h (Cell 5) + ~4.2h (Cell 6) ≈ 9h total**.

### Cell 4 — Block 1 Stage 1: `3B` Math `base` (`1,396` Items → `5,584` Rows)

```python
lock_gpu_and_batch_size("conflict_qwen25", BS_3B)
run_checked(
    f'python -B harness_v5.py --stage base --split conflict --phase confirm '
    f'--model_id Qwen/Qwen2.5-VL-3B-Instruct --batch_size {BS_3B} '
    f'--output_dir "{OUT_DIR}" --run_tag v5confirm_conflict_base_qwen25'
)
assert_jsonl_rows(os.path.join(OUT_DIR, "v5confirm_conflict_base_qwen25.jsonl"), 5584)
```

### Cell 5 — Block 1 Stage 2: `3B` Math `donor` (`1,396` Items → `5,584` Rows)

```python
lock_gpu_and_batch_size("conflict_qwen25", BS_3B)
run_checked(
    f'python -B harness_v5.py --stage donor --split conflict --phase confirm '
    f'--model_id Qwen/Qwen2.5-VL-3B-Instruct --batch_size {BS_3B} '
    f'--output_dir "{OUT_DIR}" --run_tag v5confirm_conflict_donor_qwen25'
)
assert_jsonl_rows(os.path.join(OUT_DIR, "v5confirm_conflict_donor_qwen25.jsonl"), 5584)
```

### Cell 6 — Block 1 Stage 3: `3B` Math Gates Check + Full `transplant` (`--n_competent 250`)

```python
lock_gpu_and_batch_size("conflict_qwen25", BS_3B)
base_3b = os.path.join(OUT_DIR, "v5confirm_conflict_base_qwen25.jsonl")
donor_3b = os.path.join(OUT_DIR, "v5confirm_conflict_donor_qwen25.jsonl")
assert_jsonl_rows(base_3b, 5584)
assert_jsonl_rows(donor_3b, 5584)

run_checked(
    f'python -B transplant_v5.py --gates_only --split conflict --phase confirm '
    f'--model_id Qwen/Qwen2.5-VL-3B-Instruct --batch_size {BS_3B} --n_competent 250 '
    f'--base_file "{base_3b}" --donor_file "{donor_3b}" '
    f'--output_dir "{OUT_DIR}" --run_tag v5confirm_conflict_tp_qwen25'
)
passed_3b = assert_confirm_gates_ready(os.path.join(OUT_DIR, "v5confirm_conflict_tp_qwen25.gates.json"), "conflict")

run_checked(
    f'python -B transplant_v5.py --split conflict --phase confirm '
    f'--model_id Qwen/Qwen2.5-VL-3B-Instruct --batch_size {BS_3B} --n_competent 250 '
    f'--base_file "{base_3b}" --donor_file "{donor_3b}" '
    f'--output_dir "{OUT_DIR}" --run_tag v5confirm_conflict_tp_qwen25'
)
assert_jsonl_rows(os.path.join(OUT_DIR, "v5confirm_conflict_tp_qwen25.jsonl"), 120 * passed_3b)
```

---

## Step 3 — Confirmatory Block 2: `Qwen/Qwen2.5-VL-7B-Instruct` on Math (Cells 7–9)

> [!IMPORTANT]
> If running on an **A100 (40/80 GB)** (`BS_7B = 8`), run all three cells (`base`, `donor`, `transplant`) on A100 (**~10–12h total**). If running on an **L4 (24 GB)** (`BS_7B = 2`), run all three cells on L4 (**~31h total**, across ~2–3 Colab Pro sessions using exact resume in Step 6). Never switch GPU class between stages of `7B`.

### Cell 7 — Block 2 Stage 1: `7B` Math `base` (`1,396` Items → `5,584` Rows)

```python
lock_gpu_and_batch_size("conflict_qwen25_7b", BS_7B)
run_checked(
    f'python -B harness_v5.py --stage base --split conflict --phase confirm '
    f'--model_id Qwen/Qwen2.5-VL-7B-Instruct --batch_size {BS_7B} '
    f'--output_dir "{OUT_DIR}" --run_tag v5confirm_conflict_base_qwen25_7b'
)
assert_jsonl_rows(os.path.join(OUT_DIR, "v5confirm_conflict_base_qwen25_7b.jsonl"), 5584)
```

### Cell 8 — Block 2 Stage 2: `7B` Math `donor` (`1,396` Items → `5,584` Rows)

```python
lock_gpu_and_batch_size("conflict_qwen25_7b", BS_7B)
run_checked(
    f'python -B harness_v5.py --stage donor --split conflict --phase confirm '
    f'--model_id Qwen/Qwen2.5-VL-7B-Instruct --batch_size {BS_7B} '
    f'--output_dir "{OUT_DIR}" --run_tag v5confirm_conflict_donor_qwen25_7b'
)
assert_jsonl_rows(os.path.join(OUT_DIR, "v5confirm_conflict_donor_qwen25_7b.jsonl"), 5584)
```

### Cell 9 — Block 2 Stage 3: `7B` Math Gates Check + Full `transplant` (`--n_competent 250`)

```python
lock_gpu_and_batch_size("conflict_qwen25_7b", BS_7B)
base_7b = os.path.join(OUT_DIR, "v5confirm_conflict_base_qwen25_7b.jsonl")
donor_7b = os.path.join(OUT_DIR, "v5confirm_conflict_donor_qwen25_7b.jsonl")
assert_jsonl_rows(base_7b, 5584)
assert_jsonl_rows(donor_7b, 5584)

run_checked(
    f'python -B transplant_v5.py --gates_only --split conflict --phase confirm '
    f'--model_id Qwen/Qwen2.5-VL-7B-Instruct --batch_size {BS_7B} --n_competent 250 '
    f'--base_file "{base_7b}" --donor_file "{donor_7b}" '
    f'--output_dir "{OUT_DIR}" --run_tag v5confirm_conflict_tp_qwen25_7b'
)
passed_7b = assert_confirm_gates_ready(os.path.join(OUT_DIR, "v5confirm_conflict_tp_qwen25_7b.gates.json"), "conflict")

run_checked(
    f'python -B transplant_v5.py --split conflict --phase confirm '
    f'--model_id Qwen/Qwen2.5-VL-7B-Instruct --batch_size {BS_7B} --n_competent 250 '
    f'--base_file "{base_7b}" --donor_file "{donor_7b}" '
    f'--output_dir "{OUT_DIR}" --run_tag v5confirm_conflict_tp_qwen25_7b'
)
assert_jsonl_rows(os.path.join(OUT_DIR, "v5confirm_conflict_tp_qwen25_7b.jsonl"), 120 * passed_7b)
```

---

## Step 4 — Optional Exploratory Block: ChartQA-Conflict (`D4`, Cell 10)

Run **only after** Blocks 1 & 2 (confirmatory Math) finish cleanly. `max_pixels` is locked at `200704`. On dev data, ChartQA failed the §8/R5 gate (`5/13` on 3B, `0/13` on 7B), so `transplant_v5.py` is expected to stop with exit code `2` after writing `<tag>.gates.json`; `allow_r5_stop_tag` catches that valid stopping outcome cleanly without halting the notebook.

### Cell 10 — *(Optional)* Run `3B` and `7B` Exploratory ChartQA Confirm Split (`199` Items)

```python
CHARTQA_SPECS = [
    ("Qwen/Qwen2.5-VL-3B-Instruct", "qwen25", BS_3B),
    ("Qwen/Qwen2.5-VL-7B-Instruct", "qwen25_7b", BS_7B),
]

for model_id, tag, bs in CHARTQA_SPECS:
    lock_gpu_and_batch_size(f"chartqa_{tag}", bs)
    base_c = os.path.join(OUT_DIR, f"v5confirm_chartqa_base_{tag}.jsonl")
    donor_c = os.path.join(OUT_DIR, f"v5confirm_chartqa_donor_{tag}.jsonl")
    tp_tag = f"v5confirm_chartqa_tp_{tag}"

    run_checked(
        f'python -B harness_v5.py --stage base --split chartqa --phase confirm '
        f'--model_id {model_id} --batch_size {bs} '
        f'--output_dir "{OUT_DIR}" --run_tag v5confirm_chartqa_base_{tag}'
    )
    assert_jsonl_rows(base_c, 796)

    run_checked(
        f'python -B harness_v5.py --stage donor --split chartqa --phase confirm '
        f'--model_id {model_id} --batch_size {bs} '
        f'--output_dir "{OUT_DIR}" --run_tag v5confirm_chartqa_donor_{tag}'
    )
    assert_jsonl_rows(donor_c, 796)

    run_checked(
        f'python -B transplant_v5.py --gates_only --split chartqa --phase confirm '
        f'--model_id {model_id} --batch_size {bs} '
        f'--base_file "{base_c}" --donor_file "{donor_c}" '
        f'--output_dir "{OUT_DIR}" --run_tag {tp_tag}'
    )

    rc = run_checked(
        f'python -B transplant_v5.py --split chartqa --phase confirm '
        f'--model_id {model_id} --batch_size {bs} '
        f'--base_file "{base_c}" --donor_file "{donor_c}" '
        f'--output_dir "{OUT_DIR}" --run_tag {tp_tag}',
        allow_r5_stop_tag=tp_tag,
    )
    if rc == 0:
        g = json.load(open(os.path.join(OUT_DIR, f"{tp_tag}.gates.json"), encoding="utf-8"))
        assert_jsonl_rows(os.path.join(OUT_DIR, f"{tp_tag}.jsonl"), 120 * int(g["passed"]))
```

---

## Step 5 — Post-Run Integrity Audit, Confirmatory Analysis & `lme4` (Cells 11–12)

### Cell 11 — Hard Assertions for Manifest Provenance, `F1`, `boundary_mismatch`, and GPU Consistency

```python
import glob
import json
import os
import sys

sys.path.insert(0, os.getcwd())
import harness_v4 as h4  # noqa: E402

print("=== 1. Manifest Provenance & Single-GPU Audit ===")
manifests = sorted(glob.glob(os.path.join(OUT_DIR, "v5confirm_*.manifest.json")))
assert len(manifests) >= 6, f"Expected at least 6 confirm manifests (Math 3B + 7B), found {len(manifests)}"

gpus_by_block = {}
for mpath in manifests:
    m = json.load(open(mpath, encoding="utf-8"))
    cfg, git, env = m["config"], m["git"], m["environment"]
    invs = m.get("invocations", [])
    inv_gpus = {inv["environment"]["gpu"] for inv in invs}
    inv_dtypes = {inv["environment"]["dtype"] for inv in invs}
    expected_rev = h4.MODEL_PINS[cfg["model_id"]]

    assert cfg["phase"] == "confirm", f"Non-confirm phase in {mpath}"
    assert cfg["max_pixels"] == 200704 and cfg["min_pixels"] == 100352
    assert git.get("prereg_tag") == "prereg-v5", f"Missing prereg-v5 tag in {mpath}: {git}"
    assert git.get("git_dirty") is False, f"Dirty git recorded in {mpath}: {git}"
    assert git.get("git_commit") == EXPECTED_TAG_COMMIT, f"Bad git_commit in {mpath}: {git}"
    assert git.get("prereg_tag_commit") == EXPECTED_TAG_COMMIT, f"Bad prereg_tag_commit in {mpath}: {git}"
    assert env.get("dtype") == "torch.bfloat16" and inv_dtypes == {"torch.bfloat16"}, f"Bad dtype in {mpath}"
    assert env.get("resolved_model_commit") == expected_rev, f"Unresolved/wrong commit in {mpath}"
    assert len(inv_gpus) == 1, f"Mixed GPUs inside {mpath}: {inv_gpus}"

    block = (cfg["split"], cfg["model_id"])
    gpus_by_block.setdefault(block, set()).update(inv_gpus)
    print(f"[PASS] {os.path.basename(mpath)} | gpu={next(iter(inv_gpus))} | bs={cfg['batch_size']} | invs={len(invs)}")

for block, gpus in gpus_by_block.items():
    assert len(gpus) == 1, f"Mixed GPUs across stages for {block}: {gpus}"

print("\n=== 2. Transplant Row, F1 (verdict_nll) & Boundary Audit ===")
tp_files = sorted(glob.glob(os.path.join(OUT_DIR, "v5confirm_*_tp_*.jsonl")))
assert len(tp_files) >= 2, f"Expected at least 2 Math transplant JSONLs, found {tp_files}"

for path in tp_files:
    gpath = path.replace(".jsonl", ".gates.json")
    g = json.load(open(gpath, encoding="utf-8"))
    rows = [json.loads(line) for line in open(path, encoding="utf-8") if line.strip()]
    assert len(rows) == 120 * int(g["passed"]), f"Row count mismatch in {path}: {len(rows)} != {120 * int(g['passed'])}"

    dl_rows = [r for r in rows if r.get("outcome") == "dl"]
    verdict_dl = [r for r in dl_rows if r.get("verdict") in ("own", "flip", "para", "para_flip")]
    none_dl = [r for r in dl_rows if r.get("verdict") == "none"]
    n_tok = sum(1 for r in verdict_dl if (r.get("verdict_nll_tokens") or 0) > 0 and r.get("verdict_nll") is not None)
    n_span_bool = sum(1 for r in verdict_dl if r.get("verdict_span_exact") in (True, False))
    n_none = sum(1 for r in none_dl if r.get("verdict_nll") is None and r.get("verdict_nll_tokens") is None)
    bm = sum(1 for r in dl_rows if r.get("boundary_mismatch")) / max(1, len(dl_rows))

    assert n_tok == len(verdict_dl), f"verdict_nll failure in {path}: {n_tok}/{len(verdict_dl)}"
    assert n_span_bool == len(verdict_dl), f"verdict_span_exact missing in {path}"
    assert n_none == len(none_dl), f"non-null verdict_nll on none rows in {path}: {n_none}/{len(none_dl)}"
    assert bm <= 0.01, f"boundary_mismatch exceeded 1% ({bm:.2%}) in {path}"
    print(f"[PASS] {os.path.basename(path)} | rows={len(rows)} | passed={g['passed']} | bm={bm:.3%} | vnll={n_tok}/{len(verdict_dl)}")

print("\nALL CONFIRM PROVENANCE & INTEGRITY CHECKS PASSED.")
```

### Cell 12 — Run Confirmatory Analysis (`analyze_v5.py`) & `lme4` Mixed-Effects Fits

`analyze_v5.py` refuses mixed phases by design; passing only `$OUT_DIR/v5confirm_*` keeps confirmatory data strictly separated from `v5dev_*`.

```python
analysis_dir = os.path.join(OUT_DIR, "analysis_confirm")
run_checked(
    f'python -B analyze_v5.py '
    f'--runs "{OUT_DIR}"/v5confirm_*_tp_*.jsonl '
    f'--gates "{OUT_DIR}"/v5confirm_*_tp_*.gates.json '
    f'--base "{OUT_DIR}"/v5confirm_*_base_*.jsonl '
    f'--donor "{OUT_DIR}"/v5confirm_*_donor_*.jsonl '
    f'--output_dir "{analysis_dir}"'
)

run_checked("apt-get update -qq && apt-get install -y -qq r-base")
run_checked("Rscript -e 'if (!requireNamespace(\"lme4\", quietly=TRUE)) install.packages(\"lme4\", repos=\"https://cloud.r-project.org\")'")
run_checked(
    f'Rscript "{analysis_dir}/analyze_v5_lme4.R" '
    f'"{analysis_dir}/long_v5.csv" '
    f'"{analysis_dir}/lme4_out.txt"'
)

print("\n=== PRIMARY CONFIRMATORY HEADLINES ===")
for line in open(os.path.join(analysis_dir, "analysis_v5.md"), encoding="utf-8"):
    if line.startswith(("## ", "- **PRIMARY READING", "- **T1_beh", "- **T2_beh", "- **T3_beh", "  - **T2_beh", "  - **T3_beh")):
        print(line.rstrip())
```

---

## Step 6 — Disconnect Recovery, RunPod `tmux` Shell Variant & Local Archival

### If Colab Disconnects Mid-Run (Normal on 7B)

1. Reconnect to the **same GPU type** (L4 or A100 — `lock_gpu_and_batch_size` catches any mismatch automatically).
2. Re-run **Cell 1** and **Cell 2** (which verify `prereg-v5` + packages + strict confirm preflight).
3. Re-run the interrupted cell (and any remaining cells). `harness_v5.py` and `transplant_v5.py` automatically skip completed keys, repair any half-written trailing JSONL line, and append the resumed run to `invocations[]`.

### Pure-Bash RunPod Variant (Overnight Inside `tmux`, No Jupyter Needed)

Use this when running interactively on a RunPod pod with persistent storage at `/workspace` (adjust `BS_7B=2` on 24 GB GPUs or `BS_7B=8` on 40/80 GB A100s):

```bash
tmux new -s confirm_v5
set -euo pipefail

export OUT_DIR="/workspace/results_v5_confirm"
mkdir -p "$OUT_DIR"

# 1. Clone cleanly at prereg-v5 (paste token interactively only if repo is private)
git clone https://github.com/Mohammad-Zahed-Hossen/Thesis.git /tmp/Thesis
cd "/tmp/Thesis/Causal Conflict Verbalization and Source Arbitration/Experiment"
git fetch --tags origin && git checkout prereg-v5
test "$(git rev-parse HEAD)" = "8bb6ca23bdcd926e90f78f3e457327cf595aed4b"
test -z "$(git status --short)"

# 2. Verify/install pins + strict confirm preflight + freeze log
pip install -q transformers==5.22.1 accelerate==1.15.0 datasets==4.8.5 pillow==11.3.0 qwen-vl-utils==0.0.14
python -B preflight_v5.py --phase confirm --require_tag prereg-v5 --check_gpu
pip freeze > "$OUT_DIR/pip_freeze_confirm.txt"

# 3. Run Block 1 (3B Math, BS=8) then Block 2 (7B Math, BS=2 on L4/3090/4090 or BS=8 on A100)
BS_3B=8
BS_7B=2
for ITEM in "Qwen/Qwen2.5-VL-3B-Instruct:qwen25:$BS_3B" "Qwen/Qwen2.5-VL-7B-Instruct:qwen25_7b:$BS_7B"; do
  IFS=: read -r MODEL TAG BS <<< "$ITEM"
  python -B harness_v5.py --stage base  --split conflict --phase confirm --model_id "$MODEL" --batch_size "$BS" --output_dir "$OUT_DIR" --run_tag "v5confirm_conflict_base_${TAG}"
  python -B harness_v5.py --stage donor --split conflict --phase confirm --model_id "$MODEL" --batch_size "$BS" --output_dir "$OUT_DIR" --run_tag "v5confirm_conflict_donor_${TAG}"
  python -B transplant_v5.py --gates_only --split conflict --phase confirm --model_id "$MODEL" --batch_size "$BS" --n_competent 250 \
    --base_file "$OUT_DIR/v5confirm_conflict_base_${TAG}.jsonl" --donor_file "$OUT_DIR/v5confirm_conflict_donor_${TAG}.jsonl" \
    --output_dir "$OUT_DIR" --run_tag "v5confirm_conflict_tp_${TAG}"
  python -B transplant_v5.py --split conflict --phase confirm --model_id "$MODEL" --batch_size "$BS" --n_competent 250 \
    --base_file "$OUT_DIR/v5confirm_conflict_base_${TAG}.jsonl" --donor_file "$OUT_DIR/v5confirm_conflict_donor_${TAG}.jsonl" \
    --output_dir "$OUT_DIR" --run_tag "v5confirm_conflict_tp_${TAG}"
done

# 4. Analysis + lme4
python -B analyze_v5.py \
  --runs "$OUT_DIR"/v5confirm_*_tp_*.jsonl \
  --gates "$OUT_DIR"/v5confirm_*_tp_*.gates.json \
  --base "$OUT_DIR"/v5confirm_*_base_*.jsonl \
  --donor "$OUT_DIR"/v5confirm_*_donor_*.jsonl \
  --output_dir "$OUT_DIR/analysis_confirm"
apt-get update -qq && apt-get install -y -qq r-base
Rscript -e 'if (!requireNamespace("lme4", quietly=TRUE)) install.packages("lme4", repos="https://cloud.r-project.org")'
Rscript "$OUT_DIR/analysis_confirm/analyze_v5_lme4.R" "$OUT_DIR/analysis_confirm/long_v5.csv" "$OUT_DIR/analysis_confirm/lme4_out.txt"
```

*(Detach anytime with `Ctrl+B` then `D`; reattach with `tmux attach -t confirm_v5`.)*

### Bringing Outputs Back Locally

1. Download the entire `$OUT_DIR` folder (`v5confirm_*`, `gpu_lock_*.json`, `pip_freeze_confirm.txt`, and `analysis_confirm/`) into a separate local directory such as `Experiment/results_v5_confirm/` (keep `Experiment/results_v5/` untouched as your archived dev rerun).
2. **Never delete, move, or re-point git tag `prereg-v5`.**
3. Only if a genuine unplanned procedural deviation occurred after the freeze, document it in `Docs/PREREGISTRATION_VERDICT_TRANSPLANT.md` §11 (`Deviation log`) with date, reason, and impact statement after downloading the data.
