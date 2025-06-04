#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import argparse
import hashlib
import json
import os
from pathlib import Path
from string import Template

import openai
import pathspec
import tiktoken

# --- Constants & Defaults ---
DEFAULT_MAX_TOTAL_TOKENS = 12000
DEFAULT_MAX_FILE_TOKENS = 2000
DEFAULT_MAX_FILE_SIZE_MB = 1
DEFAULT_OUTPUT_FILE = "context.txt"
DEFAULT_MESSAGE_FILE = "gptcontext_message.txt"
DEFAULT_BASE_DIR = "."
DEFAULT_CONFIG_FILE = "context_config.json"
MESSAGE_TEMPLATE_FILE = "message_sample.txt"
CACHE_DIR = Path(".context-cache")
ENCODING_NAME = "cl100k_base"
OPENAI_MODEL = "gpt-4-turbo"
DEFAULT_CONFIG_INCLUDE_EXTS = {
    ".py", ".md", ".js", ".ts", ".jsx", ".tsx", ".json", ".toml", ".yaml", ".yml",
    ".html", ".css", ".scss", ".sass", ".less", ".java", ".go", ".rs", ".cpp", ".c",
    ".h", ".hpp", ".cs", ".swift", ".kt", ".m", ".sh", ".bash", ".zsh", ".ps1", ".pl",
    ".rb", ".php", ".ini", ".cfg", ".env", ".txt", ".xml"
}

DEFAULT_CONFIG_EXCLUDE_DIRS = {
    ".git", ".svn", ".hg", "node_modules", "__pycache__", "dist", "build", ".venv",
    "env", ".mypy_cache", ".pytest_cache", ".vscode", ".idea", ".context-cache",
    ".DS_Store", "__snapshots__", ".coverage", ".cache"
}

CACHE_DIR.mkdir(exist_ok=True)

enc = tiktoken.get_encoding(ENCODING_NAME)


def file_token_count(text: str) -> int:
    return len(enc.encode(text))


def load_gitignore(base_path: Path) -> pathspec.PathSpec | None:
    path = base_path / ".gitignore"
    if not path.exists():
        return None
    return pathspec.PathSpec.from_lines("gitwildmatch", path.read_text().splitlines())


def is_ignored(filepath: str, spec: pathspec.PathSpec | None) -> bool:
    return spec and spec.match_file(filepath)  # type: ignore


def load_config(config_path: Path) -> tuple[set[str], set[str]]:
    if not config_path.exists():
        print(f"Warning: {config_path} not found. Using default config.")
        return DEFAULT_CONFIG_INCLUDE_EXTS, DEFAULT_CONFIG_EXCLUDE_DIRS

    config = json.loads(config_path.read_text())
    include_exts = set(config.get("include_extensions", []))
    exclude_dirs = set(config.get("exclude_dirs", []))
    return include_exts, exclude_dirs


def list_relevant_files(
    base_path: Path,
    gitignore_spec: pathspec.PathSpec | None,
    include_exts: set[str],
    exclude_dirs: set[str],
) -> list[Path]:
    files = []
    for root, dirs, filenames in os.walk(base_path):
        dirs[:] = [d for d in dirs if d not in exclude_dirs]
        for name in filenames:
            ext = Path(name).suffix
            full_path = Path(root) / name
            rel_path = full_path.relative_to(base_path)
            if ext in include_exts and not is_ignored(str(rel_path), gitignore_spec):
                if full_path.stat().st_size <= DEFAULT_MAX_FILE_SIZE_MB * 1024 * 1024:
                    files.append(full_path)
    return sorted(files, key=lambda f: f.stat().st_size)


def summarize_text(text: str, rel_path: str) -> str:
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        print("Error: OPENAI_API_KEY not set. Skipping summarization.")
        return "[Summary unavailable: OPENAI_API_KEY not set]"
    openai.api_key = api_key

    prompt = (
        f"Summarize the following source file for LLM-assisted understanding:\n"
        f"- File: {rel_path}\n"
        f"- Focus on key components, classes, functions, and logic\n"
        f"- Format clearly and concisely\n\n"
    )
    tokens = enc.encode(text)
    max_tokens = 3000
    truncated = enc.decode(tokens[:max_tokens])

    try:
        response = openai.chat.completions.create(
            model=OPENAI_MODEL,
            messages=[{"role": "user", "content": prompt + truncated}],
            temperature=0.2,
        )
        return response.choices[0].message.content.strip()  # type: ignore
    except Exception as e:
        print(f"Error summarizing {rel_path}: {e}")
        return "[Summary unavailable due to error]"


def get_cached_summary(text: str, rel_path: str) -> str:
    digest = hashlib.sha256(text.encode("utf-8")).hexdigest()
    cache_file = CACHE_DIR / f"{digest}.txt"
    if cache_file.exists():
        return cache_file.read_text()
    summary = summarize_text(text, rel_path)
    cache_file.write_text(summary)
    return summary


def build_context(
    base_path: Path,
    max_tokens: int,
    summarize_large: bool,
    max_file_tokens: int,
    include_exts: set[str],
    exclude_dirs: set[str],
) -> str:
    gitignore = load_gitignore(base_path)
    tokens_used = 0
    parts: list[str] = []

    files = list_relevant_files(base_path, gitignore, include_exts, exclude_dirs)
    print(f"✓ Found {len(files)} relevant files")

    for path in files:
        rel_path = path.relative_to(base_path)
        try:
            content = path.read_text(encoding="utf-8")
        except Exception as e:
            print(f"Skipping {rel_path}: {e}")
            continue

        tokens = file_token_count(content)

        if tokens > max_file_tokens:
            if summarize_large:
                summary = get_cached_summary(content, str(rel_path))
                stokens = file_token_count(summary)
                if tokens_used + stokens <= max_tokens:
                    parts.append(f"\n# Summary of {rel_path}\n{summary}")
                    tokens_used += stokens
                else:
                    print(f"Skipped summary of {rel_path}: token limit")
            else:
                print(f"Skipped {rel_path} (too large and summarization disabled)")
        elif tokens_used + tokens <= max_tokens:
            parts.append(f"\n# {rel_path}\n{content}")
            tokens_used += tokens
        else:
            print(f"Skipped {rel_path}: token limit")

    return "\n".join(parts)


def write_message_template(context: str, message_file: Path):
    template_path = Path(MESSAGE_TEMPLATE_FILE)
    if not template_path.exists():
        print(
            f"Warning: {MESSAGE_TEMPLATE_FILE} not found. Skipping message generation."
        )
        return

    raw_template = template_path.read_text(encoding="utf-8")
    template = Template(raw_template)

    try:
        message = template.substitute(context=context)
    except KeyError as e:
        print(f"Template substitution failed: missing key {e}")
        return

    message_file.write_text(message, encoding="utf-8")
    print(f"✓ Generated full ChatGPT message at {message_file}")


def main():
    parser = argparse.ArgumentParser(description="Generate repo context for ChatGPT.")
    parser.add_argument("--max-tokens", type=int, default=DEFAULT_MAX_TOTAL_TOKENS)
    parser.add_argument(
        "--file-token-threshold",
        type=int,
        default=DEFAULT_MAX_FILE_TOKENS,
        help="Token threshold after which a file is summarized",
    )
    parser.add_argument(
        "--summarize", action="store_true", help="Summarize large files with OpenAI"
    )
    parser.add_argument("--output", type=str, default=DEFAULT_OUTPUT_FILE)
    parser.add_argument("--base", type=str, default=DEFAULT_BASE_DIR)
    parser.add_argument(
        "--config",
        type=str,
        default=DEFAULT_CONFIG_FILE,
        help="Path to JSON config with include/exclude settings",
    )
    parser.add_argument(
        "--generate-message",
        action="store_true",
        help="Output a full ChatGPT message using message_sample.txt",
    )
    args = parser.parse_args()

    base_path = Path(args.base).resolve()
    include_exts, exclude_dirs = load_config(Path(args.config).resolve())

    context = build_context(
        base_path,
        args.max_tokens,
        args.summarize,
        args.file_token_threshold,
        include_exts,
        exclude_dirs,
    )
    output_path = Path(args.output).resolve()
    output_path.write_text(context, encoding="utf-8")

    print(f"\nWrote {output_path} with {file_token_count(context)} tokens.")

    if args.generate_message:
        message_path = Path(DEFAULT_MESSAGE_FILE).resolve()
        write_message_template(context, message_path)


if __name__ == "__main__":
    main()
