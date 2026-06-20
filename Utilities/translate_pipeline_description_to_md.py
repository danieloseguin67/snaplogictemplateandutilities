"""
Translate a SnapLogic pipeline description into a Markdown document.

Usage examples:
        python translate_pipeline_description_to_md.py

The script always opens a Windows GUI where you can paste a pipeline
description and generate a Markdown file.
"""

from __future__ import annotations

import argparse
import datetime as dt
from dataclasses import dataclass
from pathlib import Path
import tkinter as tk
from tkinter import filedialog, messagebox


DEFAULT_DESCRIPTION = """This pipeline retrieves location information based on a given postcode and uses it to fetch hourly weather forecast data. It first calls a geocoding API to obtain geographic coordinates and place details, then queries a weather API for hourly temperature forecasts. The resulting data is processed and exported in two formats: an Excel file and a CSV file, both named after the input postcode.

Snap Summary:

- HTTP Client: Sends a GET request to the Zippopotam API using the pipeline parameter `_postcode` to retrieve location data, and extracts the JSON response entity.
- JSON Splitter: Splits the JSON response by iterating over the `$entity.places` array, producing one document per place entry.
- MapFromJsonToVar : Maps fields from the split place document to simplified variable names, extracting latitude , longitude , place name , state , and state abbreviation .
- Weather API : Sends a GET request to the Open-Meteo forecast API using the latitude and longitude values as query parameters, requesting hourly 2-meter temperature data in Fahrenheit, and extracts the JSON response entity.
- Hour and Temperature : Maps the hourly time and temperature arrays from the weather API response into an array of objects, each containing an `Hour` and `Temperature` field, stored under `$.rows`.
- Flatten Rows : Splits the `$.rows` array into individual documents, one per hourly time-temperature pair.
- Copy: Duplicates the stream of flattened hourly weather records, sending one copy to the Excel formatter and another to the CSV formatter .
- Excel Formatter: Formats the incoming data into an Excel workbook with a sheet named "Weather Data".
- Excel File Writer : Writes the formatted Excel data to a file named `weather_output_<postcode>.xlsx`, overwriting any existing file with the same name.
- CSV Formatter: Formats the incoming data as a CSV file using comma delimiters, double-quote characters, minimal quoting mode, UTF-8 encoding, and LF newline characters.
- CSV File Writer : Writes the formatted CSV data to a file named `weather_output_<postcode>.csv`, overwriting any existing file with the same name.
"""


@dataclass
class SnapStep:
    name: str
    detail: str


def extract_overview_and_steps(description: str) -> tuple[str, list[SnapStep]]:
    text = description.strip()
    marker = "Snap Summary:"

    if marker in text:
        overview, summary = text.split(marker, 1)
    else:
        overview, summary = text, ""

    steps: list[SnapStep] = []
    for raw_line in summary.splitlines():
        line = raw_line.strip()
        if not line.startswith("- "):
            continue

        content = line[2:].strip()
        if ":" in content:
            name, detail = content.split(":", 1)
            steps.append(SnapStep(name=name.strip(), detail=detail.strip()))
        else:
            steps.append(SnapStep(name="Step", detail=content))

    return overview.strip(), steps


def render_markdown(title: str, overview: str, steps: list[SnapStep]) -> str:
    today = dt.date.today().isoformat()

    lines: list[str] = []
    lines.append(f"# {title}")
    lines.append("")
    lines.append(f"Generated on: {today}")
    lines.append("")
    lines.append("## Overview")
    lines.append("")
    lines.append(overview if overview else "No overview provided.")
    lines.append("")

    lines.append("## Snap Summary")
    lines.append("")

    if not steps:
        lines.append("No snap steps found in the description.")
        lines.append("")
        return "\n".join(lines)

    lines.append("| # | Snap | Description |")
    lines.append("|---|------|-------------|")
    for index, step in enumerate(steps, start=1):
        snap = step.name.replace("|", "\\|")
        detail = step.detail.replace("|", "\\|")
        lines.append(f"| {index} | {snap} | {detail} |")

    lines.append("")
    lines.append("## Notes")
    lines.append("")
    lines.append("- Output files are generated per postcode input.")
    lines.append("- The same weather rows are formatted into both Excel and CSV outputs.")

    return "\n".join(lines)


def render_confluence(title: str, overview: str, steps: list[SnapStep]) -> str:
    today = dt.date.today().isoformat()

    lines: list[str] = []
    lines.append(f"h1. {title}")
    lines.append("")
    lines.append(f"Generated on: {today}")
    lines.append("")
    lines.append("h2. Overview")
    lines.append("")
    lines.append(overview if overview else "No overview provided.")
    lines.append("")

    lines.append("h2. Snap Summary")
    lines.append("")

    if not steps:
        lines.append("No snap steps found in the description.")
        lines.append("")
        return "\n".join(lines)

    lines.append("|| # || Snap || Description ||")
    for index, step in enumerate(steps, start=1):
        snap = step.name.replace("|", "\\|")
        detail = step.detail.replace("|", "\\|")
        lines.append(f"| {index} | {snap} | {detail} |")

    lines.append("")
    lines.append("h2. Notes")
    lines.append("")
    lines.append("* Output files are generated per postcode input.")
    lines.append("* The same weather rows are formatted into both Excel and CSV outputs.")

    return "\n".join(lines)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Open GUI to convert a SnapLogic pipeline description into Markdown."
    )
    parser.add_argument(
        "--output-file",
        default="pipeline_description.md",
        help="Default path shown in the GUI output file field.",
    )
    parser.add_argument(
        "--title",
        default="SnapLogic Pipeline Description",
        help="Default title shown in the GUI title field.",
    )
    return parser.parse_args()


def show_gui_and_generate(default_title: str, default_output: str) -> int:
    root = tk.Tk()
    root.title("SnapLogic Description to Markdown")
    root.geometry("900x680")

    title_var = tk.StringVar(value=default_title)
    output_var = tk.StringVar(value=default_output)
    format_var = tk.StringVar(value="markdown")

    frame = tk.Frame(root, padx=12, pady=12)
    frame.pack(fill=tk.BOTH, expand=True)

    tk.Label(frame, text="Markdown Title").pack(anchor="w")
    tk.Entry(frame, textvariable=title_var).pack(fill=tk.X, pady=(0, 10))

    tk.Label(frame, text="Output File").pack(anchor="w")
    output_row = tk.Frame(frame)
    output_row.pack(fill=tk.X, pady=(0, 10))
    tk.Entry(output_row, textvariable=output_var).pack(side=tk.LEFT, fill=tk.X, expand=True)

    def browse_output() -> None:
        path = filedialog.asksaveasfilename(
            title="Save Markdown As",
            defaultextension=".md",
            filetypes=[("Markdown files", "*.md"), ("All files", "*.*")],
            initialfile=output_var.get(),
        )
        if path:
            output_var.set(path)

    tk.Button(output_row, text="Browse...", command=browse_output).pack(side=tk.LEFT, padx=(8, 0))

    tk.Label(frame, text="Output Format").pack(anchor="w")
    format_row = tk.Frame(frame)
    format_row.pack(fill=tk.X, pady=(0, 10))
    tk.Radiobutton(
        format_row,
        text="Markdown",
        variable=format_var,
        value="markdown",
    ).pack(side=tk.LEFT)
    tk.Radiobutton(
        format_row,
        text="Confluence",
        variable=format_var,
        value="confluence",
    ).pack(side=tk.LEFT, padx=(10, 0))

    tk.Label(frame, text="Pipeline Description Text").pack(anchor="w")
    text_widget = tk.Text(frame, wrap=tk.WORD)
    text_widget.pack(fill=tk.BOTH, expand=True)
    text_widget.insert("1.0", DEFAULT_DESCRIPTION)

    button_row = tk.Frame(frame)
    button_row.pack(fill=tk.X, pady=(10, 0))

    status_var = tk.StringVar(value="Ready")

    def generate() -> None:
        description = text_widget.get("1.0", tk.END).strip()
        if not description:
            messagebox.showerror("Missing Text", "Please enter a pipeline description.")
            return

        title = title_var.get().strip() or "SnapLogic Pipeline Description"
        output_value = output_var.get().strip() or "pipeline_description.md"
        output_path = Path(output_value)
        selected_format = format_var.get()

        try:
            if output_path.parent and str(output_path.parent) != ".":
                output_path.parent.mkdir(parents=True, exist_ok=True)

            overview, steps = extract_overview_and_steps(description)
            if selected_format == "confluence":
                document = render_confluence(title, overview, steps)
            else:
                document = render_markdown(title, overview, steps)

            with open(output_path, "w", encoding="utf-8", newline="\n") as file:
                file.write(document)

            status_var.set(f"Saved ({selected_format}): {output_path}")
            messagebox.showinfo(
                "Success",
                (
                    f"Document created ({selected_format}):\n{output_path}"
                    f"\n\nDetected snap steps: {len(steps)}"
                ),
            )
        except OSError as exc:
            messagebox.showerror("Write Error", f"Could not write output file:\n{exc}")

    tk.Button(button_row, text="Generate Markdown", command=generate).pack(side=tk.LEFT)
    tk.Button(button_row, text="Exit", command=root.destroy).pack(side=tk.LEFT, padx=(8, 0))
    tk.Label(button_row, textvariable=status_var, anchor="w").pack(side=tk.LEFT, padx=(10, 0))

    root.mainloop()
    return 0


def main() -> int:
    args = parse_args()
    return show_gui_and_generate(args.title, args.output_file)


if __name__ == "__main__":
    raise SystemExit(main())
