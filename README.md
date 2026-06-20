# SnapLogic Templates and Utilities

A collection of templates and utilities to support SnapLogic pipeline development and documentation.

## Project Structure

```
SnapLogicTemplatesAndUtilities/
├── Templates/          # SnapLogic pipeline templates (coming soon)
└── Utilities/          # Helper scripts and tools
    └── translate_pipeline_description_to_md.py
```

---

## Utilities

### `translate_pipeline_description_to_md.py`

A GUI tool that converts a SnapLogic pipeline description (plain text) into a formatted **Markdown** or **Confluence wiki** document.

#### Features

- Windows GUI (Tkinter) for pasting pipeline descriptions
- Parses a `Snap Summary:` section into a structured table of snap steps
- Outputs either:
  - **Markdown** (`.md`) — GitHub/VS Code compatible
  - **Confluence wiki markup** — ready to paste into Confluence pages
- Allows custom document title and output file path (with Browse dialog)
- Includes a built-in example description for quick testing

#### Requirements

- Python 3.8+
- Standard library only (`tkinter`, `argparse`, `dataclasses`, `pathlib`, `datetime`)

#### Usage

```bash
python Utilities/translate_pipeline_description_to_md.py
```

**Optional arguments:**

| Argument | Default | Description |
|----------|---------|-------------|
| `--title` | `SnapLogic Pipeline Description` | Default title shown in the GUI |
| `--output-file` | `pipeline_description.md` | Default output file path shown in the GUI |

#### Input Format

Paste a pipeline description in the GUI text area. Use the following format for best results:

```
<Overview paragraph describing what the pipeline does>

Snap Summary:

- Snap Name: Description of what this snap does.
- Another Snap: Description of this snap.
```

The tool splits the text on `Snap Summary:`, using everything before as the **Overview** and each `- Name: Detail` bullet as a row in the snap table.

#### Output Example (Markdown)

```markdown
# My Pipeline

Generated on: 2026-06-20

## Overview

This pipeline retrieves weather data based on a postcode...

## Snap Summary

| # | Snap | Description |
|---|------|-------------|
| 1 | HTTP Client | Sends a GET request to the geocoding API... |
| 2 | JSON Splitter | Splits the response by the places array... |

## Notes

- Output files are generated per postcode input.
```

---

## Templates

The `Templates/` folder is reserved for reusable SnapLogic pipeline templates. Contents will be added as the project grows.

---

## License

This project is for internal/demo use. No license applied.
