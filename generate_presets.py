#!/usr/bin/env python3
"""
generate_presets_md.py

Scan src/gptcontext/presets/*.yml and produce a PRESETS.md file there,
with a table of presets, and for each preset a detailed section.
"""

import yaml
from pathlib import Path
import sys

def load_preset(path: Path):
    """
    Load a single preset YAML, and normalize fields:
      - name: stem of file
      - filename: path.name
      - short: data['short_description'] or data['description'] or ''
      - long:  data['long_description']  or data['description'] or ''
      - include_exts: list from data['include_exts'] (or [])
      - exclude: list from data['exclude']      (or [])
      - raw: full YAML dict
    """
    data = yaml.safe_load(path.read_text(encoding="utf-8")) or {}
    name = path.stem
    short = data.get("short_description", data.get("description", "")).strip()
    long_desc = data.get("long_description", data.get("description", "")).strip()
    include_exts = data.get("include_exts") or []
    exclude = data.get("exclude") or []
    return {
        "name": name,
        "filename": path.name,
        "short": short,
        "long": long_desc,
        "include_exts": include_exts,
        "exclude": exclude,
        "raw": data,
    }

def main():
    repo_root = Path(__file__).parent
    presets_dir = repo_root / "src" / "gptcontext" / "presets"
    if not presets_dir.is_dir():
        print(f"Error: presets directory not found at {presets_dir}", file=sys.stderr)
        sys.exit(1)

    out_path = presets_dir / "PRESETS.md"

    # collect all .yml presets
    files = sorted(presets_dir.glob("*.yml"))
    presets = [ load_preset(p) for p in files ]

    # --- Build the markdown ---
    lines = []

    # Title
    lines.append("# GPTContext Presets\n")
    lines.append(
        "This document describes each of the built-in configuration presets "
        "you can pass via `--config-file presets/<name>.yml`.\n"
    )

    # Table of presets
    lines.append("## Table of presets\n")
    lines.append("| Preset | Short Description |")
    lines.append("| ------ | ----------------- |")
    for p in presets:
        lines.append(
            f"| [{p['name']}](#{p['name']}) | {p['short']} |"
        )
    lines.append("")

    # Detailed sections
    for p in presets:
        lines.append(f"## {p['name']}\n")
        # link to file
        lines.append(
            f"[View YAML →](./{p['filename']})\n"
        )
        # long description
        if p["long"]:
            lines.append(f"{p['long']}\n")
        # includes
        inc = p["include_exts"]
        if inc:
            inc_list = ", ".join(f"`{e}`" for e in inc)
            lines.append(f"**Include extensions:** {inc_list}\n")
        # excludes
        exc = p["exclude"]
        if exc:
            exc_list = ", ".join(f"`{e}`" for e in exc)
            lines.append(f"**Exclude patterns:** {exc_list}\n")
        # full raw YAML
        lines.append("```yaml")
        # preserve key order if any
        dumped = yaml.dump(p["raw"], sort_keys=False).rstrip()
        lines.append(dumped)
        lines.append("```\n")

    # Write out
    out_path.write_text("\n".join(lines), encoding="utf-8")
    print(f"Wrote {out_path.relative_to(repo_root)}")

if __name__ == "__main__":
    main()
