"""Rebuild (or verify) the assembled AI/ML Research Playbook from its content-named source parts.

Usage (from anywhere):
    python _rebuild_playbook.py                 # verify: rebuild in memory and compare with the published file
    python _rebuild_playbook.py --write         # regenerate the published file from the parts
    python _rebuild_playbook.py --out FILE      # write the assembled document to FILE instead

Ordering rule
-------------
The published document is the concatenation of every ``*.md`` file in this folder in ascending filename
order, joined with one blank line. That is why each part starts with a zero-padded prefix (00a, 00b, 00c,
02, ..., 35): the prefix encodes the position in the document, and the rest of the name says what the file
contains. Files whose name starts with ``_`` (this script, ``_MANIFEST.md``) and the ``_superseded/``
folder are ignored. Never renumber an existing prefix; add a new one instead (e.g. ``18b_...``).
"""

import argparse
import glob
import os

HERE = os.path.dirname(os.path.abspath(__file__))
PLAYBOOK_DIR = os.path.dirname(HERE)
GLUE = "\n\n"
EXPECTED_PARTS = 39


def read(path):
    with open(path, encoding="utf-8", newline="") as handle:
        return handle.read().replace("\r\n", "\n")


def part_names():
    return sorted(
        name
        for name in os.listdir(HERE)
        if name.endswith(".md")
        and not name.startswith("_")
        and os.path.isfile(os.path.join(HERE, name))
    )


def find_deliverable():
    exact = os.path.join(PLAYBOOK_DIR, "AI_ML_Research_Playbook (Cline 2026-09-27).md")
    if os.path.isfile(exact):
        return exact
    candidates = [p for p in glob.glob(os.path.join(PLAYBOOK_DIR, "*Cline*.md")) if os.path.isfile(p)]
    if not candidates:
        raise SystemExit("Cannot locate the Cline deliverable; pass --out explicitly.")
    return max(candidates, key=os.path.getsize)


def newline_style(path):
    """Return "\\r\\n" or "\\n" matching the existing file, so --write is byte-faithful."""
    if path and os.path.isfile(path):
        with open(path, "rb") as handle:
            raw = handle.read()
        crlf = raw.count(b"\r\n")
        lf = raw.count(b"\n") - crlf
        if crlf or lf:
            return "\r\n" if crlf >= lf else "\n"
    return "\r\n"


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--write", action="store_true", help="write the assembled document")
    parser.add_argument("--out", help="alternative output path (implies --write)")
    args = parser.parse_args()

    names = part_names()
    if len(names) != EXPECTED_PARTS:
        raise SystemExit(f"Expected {EXPECTED_PARTS} part files, found {len(names)}:\n  " + "\n  ".join(names))
    if [n[:3] for n in names[:3]] != ["00a", "00b", "00c"]:
        raise SystemExit("Front matter order changed: the first three parts must be 00a, 00b, 00c.")

    body = GLUE.join(read(os.path.join(HERE, name)).strip() for name in names)
    target = args.out or find_deliverable()
    current = read(target).strip() if os.path.isfile(target) else None

    if args.write or args.out:
        text = body + "\n"
        style = newline_style(target)
        if style == "\r\n":
            text = text.replace("\n", "\r\n")
        with open(target, "wb") as handle:
            handle.write(text.encode("utf-8"))
        print(f"wrote {len(text)} chars with {style!r} line endings to {target}")

    same = body == current
    state = "n/a (new file)" if current is None else str(same)
    print(f"parts={len(names)}  chars={len(body)}  target={os.path.basename(target)}  matches_existing={state}")
    if current is not None and not same:
        limit = min(len(body), len(current))
        for i in range(limit):
            if body[i] != current[i]:
                print(f"first difference at char {i}")
                print("  parts   :", repr(body[max(0, i - 60):i + 60]))
                print("  existing:", repr(current[max(0, i - 60):i + 60]))
                break
        else:
            print("  one file is a prefix of the other (trailing content differs)")
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
