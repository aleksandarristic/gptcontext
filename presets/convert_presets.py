#!/usr/bin/env python3

"""
Convert old EXCLUDE_DIRS + EXCLUDE_FILES + INCLUDE_EXTS → unified exclude + include_exts + use_default_excludes.
Preserve comments and inject blank lines between sections.

Run this inside presets/:  python3 convert_presets.py
"""

from pathlib import Path
from ruamel.yaml import YAML

yaml = YAML()
yaml.indent(mapping=2, sequence=2, offset=0)
yaml.preserve_quotes = True

def convert_file(path: Path):
    print(f"Processing {path}...")

    with path.open("r", encoding="utf-8") as f:
        data = yaml.load(f)

    exclude = []

    # Handle EXCLUDE_DIRS
    if "EXCLUDE_DIRS" in data:
        for d in data["EXCLUDE_DIRS"]:
            d = d.rstrip("/") + "/"  # ensure trailing slash
            exclude.append(d)
        del data["EXCLUDE_DIRS"]

    # Handle EXCLUDE_FILES
    if "EXCLUDE_FILES" in data:
        for f_ in data["EXCLUDE_FILES"]:
            exclude.append(f_)  # as is
        del data["EXCLUDE_FILES"]

    # Inject unified exclude
    if exclude:
        data["exclude"] = exclude
        # Insert blank line before 'exclude'
        data.yaml_set_comment_before_after_key("exclude", before="\n")

    # Handle INCLUDE_EXTS → include_exts
    if "INCLUDE_EXTS" in data:
        data["include_exts"] = data["INCLUDE_EXTS"]
        del data["INCLUDE_EXTS"]
        # Insert blank line before 'include_exts'
        data.yaml_set_comment_before_after_key("include_exts", before="\n")

    # Inject use_default_excludes
    data["use_default_excludes"] = True
    # Insert blank line before 'use_default_excludes'
    data.yaml_set_comment_before_after_key("use_default_excludes", before="\n")

    # Write back with preserved comments and spacing
    with path.open("w", encoding="utf-8") as f:
        yaml.dump(data, f)

    print(f"✓ Converted {path}")


def main():
    for path in Path(".").glob("*.yml"):
        convert_file(path)


if __name__ == "__main__":
    main()
