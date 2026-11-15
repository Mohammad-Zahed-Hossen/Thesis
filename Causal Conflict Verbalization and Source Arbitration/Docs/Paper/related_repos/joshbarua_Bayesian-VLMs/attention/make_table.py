#!/usr/bin/env python3
"""Create the paper's attention-knockout CSV and LaTeX table."""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

import pandas as pd

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from config import get_run_dir


CELLS = ("C", "T", "V")
SPAN_LABELS = {"image": "Image span", "passage": "Passage span", "question": "Question span"}


def _whole_stack(path: Path) -> pd.DataFrame:
    frame = pd.read_csv(path)
    frame = frame[frame["block"] == "all"].copy()
    if frame.empty:
        raise ValueError(f"{path} has no whole-stack rows")
    return frame


def collect(qwen25_run: str, qwen35_run: str) -> pd.DataFrame:
    rows = []
    for model, run_id in (
        ("Qwen2.5-VL-3B", qwen25_run),
        ("Qwen3.5-4B", qwen35_run),
    ):
        span = _whole_stack(get_run_dir(run_id) / "summary_knockout.csv")
        for span_name in ("image", "passage", "question"):
            row = {"model": model, "pathway": "Full attention", "route": SPAN_LABELS[span_name]}
            for cell in CELLS:
                value = span[(span["span"] == span_name) & (span["cell"] == cell)].iloc[0]
                row.update({
                    f"{cell}_mean": value["delta_mean"],
                    f"{cell}_lo": value["delta_lo"],
                    f"{cell}_hi": value["delta_hi"],
                    f"{cell}_n": int(value["n"]),
                })
            rows.append(row)

    linear = _whole_stack(
        get_run_dir(qwen35_run) / "summary_linear_output_knockout.csv"
    )
    row = {"model": "Qwen3.5-4B", "pathway": "Linear attention", "route": "Readout write"}
    for cell in CELLS:
        value = linear[linear["cell"] == cell].iloc[0]
        row.update({
            f"{cell}_mean": value["delta_mean"],
            f"{cell}_lo": value["delta_lo"],
            f"{cell}_hi": value["delta_hi"],
            f"{cell}_n": int(value["n"]),
        })
    rows.append(row)
    return pd.DataFrame(rows)


def _number(value: float) -> str:
    return f"{value:+.2f}"


def latex_table(frame: pd.DataFrame) -> str:
    lines = [
        r"\begin{table*}[t]",
        r"  \centering",
        r"  \small",
        r"  \newcommand{\koresult}[3]{$#1$\textcolor{gray}{$_{\,[#2,#3]}$}}",
        r"  \begin{tabular}{lllccc}",
        r"    \toprule",
        r"    \textbf{Model} & \textbf{Pathway} & \textbf{Knocked-out route} & \textbf{$C$} & \textbf{$T$} & \textbf{$V$} \\",
        r"    \midrule",
    ]
    previous_model = None
    for _, row in frame.iterrows():
        model = row["model"] if row["model"] != previous_model else ""
        previous_model = row["model"]
        cells = [
            rf"\koresult{{{_number(row[f'{cell}_mean'])}}}{{{_number(row[f'{cell}_lo'])}}}{{{_number(row[f'{cell}_hi'])}}}"
            for cell in CELLS
        ]
        lines.append(
            f"    {model} & {row['pathway']} & {row['route']} & "
            + " & ".join(cells)
            + r" \\"
        )
    lines.extend([
        r"    \bottomrule",
        r"  \end{tabular}",
        r"  \caption{Causal effects of attention pathways. Entries are mean $\Delta_{\mathrm{KO}}$ in nats with 95\% bootstrap confidence intervals.}",
        r"  \label{tab:attention-knockout}",
        r"\end{table*}",
        "",
    ])
    return "\n".join(lines)


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--qwen25_run_id", required=True)
    parser.add_argument("--qwen35_run_id", required=True)
    parser.add_argument("--out", type=Path, default=Path("runs/attention_knockout.tex"))
    args = parser.parse_args()

    frame = collect(args.qwen25_run_id, args.qwen35_run_id)
    args.out.parent.mkdir(parents=True, exist_ok=True)
    frame.to_csv(args.out.with_suffix(".csv"), index=False)
    args.out.write_text(latex_table(frame))
    print(args.out)
    print(args.out.with_suffix(".csv"))


if __name__ == "__main__":
    main()
