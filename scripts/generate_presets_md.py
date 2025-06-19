#!/usr/bin/env python3
"""
generate_presets.py

Scan ./presets/*.yml and produce a PRESETS.md file in the repo root,
with a table of presets and, for each preset, a detailed section
(and a link back to the table).  The "[View YAML]" links now correctly
point to presets/<name>.yml.
"""

import sys
from pathlib import Path

import yaml


def load_preset(path: Path):
    """
    Load a single preset YAML, and normalize fields:
      - name: stem of file
      - filename: path.name
      - short: data['short_description'] or data['description'] or ''
      - long:  data['long_description']  or data['description'] or ''
      - include_exts: list from data['include_exts'] (or [])
      - exclude: list from data['exclude']      (or [])
    """
    data = yaml.safe_load(path.read_text(encoding="utf-8")) or {}
    return {
        "name": path.stem,
        "filename": path.name,
        "short": data.get("short_description", data.get("description", "")).strip(),
        "long": data.get("long_description", data.get("description", "")).strip(),
        "include_exts": data.get("include_exts") or [],
        "exclude": data.get("exclude") or [],
    }


def main():
    # assume this script lives in the reporoot/scripts/ directory
    repo_root = Path(__file__).parent.parent.resolve()
    presets_dir = repo_root / "presets"
    if not presets_dir.is_dir():
        print(f"Error: presets directory not found at {presets_dir}", file=sys.stderr)
        sys.exit(1)

    out_path = repo_root / "PRESETS.md"

    # collect all .yml presets
    files = sorted(presets_dir.glob("*.yml"))
    presets = [load_preset(p) for p in files]

    lines = []

    # Title
    lines.append("# GPTContext Presets\n")
    lines.append(
        "This document describes each of the built-in configuration presets "
        "you can pass via `--config-file presets/<name>.yml`.\n\n"
        "All the presets are in the `presets/` directory.\n"
    )

    # Table of presets
    lines.append("## Table of presets\n")
    lines.append("| Preset | Short Description |")
    lines.append("| ------ | ----------------- |")
    for p in presets:
        lines.append(f"| [{p['name']}](#{p['name']}) | {p['short']} |")
    lines.append("")

    # Detailed sections
    for p in presets:
        lines.append(f"## {p['name']}\n")
        # correct relative link into presets/
        link_path = Path("presets") / p["filename"]
        lines.append(f"[View YAML →]({link_path.as_posix()})\n")
        # long description
        if p["long"]:
            lines.append(f"{p['long']}\n")
        # includes
        if p["include_exts"]:
            inc_list = ", ".join(f"`{e}`" for e in p["include_exts"])
            lines.append(f"**Include extensions:** {inc_list}\n")
        # excludes
        if p["exclude"]:
            exc_list = ", ".join(f"`{e}`" for e in p["exclude"])
            lines.append(f"**Exclude patterns:** {exc_list}\n")
        # back to TOC
        lines.append("[Back to Table of presets](#table-of-presets)\n")

    out_path.write_text("\n".join(lines), encoding="utf-8")
    print(f"Wrote {out_path.relative_to(repo_root)}")


if __name__ == "__main__":
    main()
