#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import sys
import argparse
import hashlib
from pathlib import Path

import tiktoken
import pathspec
import openai

DEFAULT_MAX_TOTAL_TOKENS = 12000
MAX_FILE_TOKENS_BEFORE_SUMMARY = 2000
MAX_FILE_SIZE_MB = 1

INCLUDE_EXTS = {'.py', '.md', '.js', '.ts', '.json', '.toml', '.yaml', '.yml', '.html', '.css'}
EXCLUDE_DIRS = {'.git', 'node_modules', '__pycache__', 'dist', 'build', '.venv', 'env'}
OPENAI_MODEL = "gpt-4-turbo"

CACHE_DIR = Path(".context-cache")
CACHE_DIR.mkdir(exist_ok=True)

api_key = os.getenv("OPENAI_API_KEY")
if not api_key:
    print("Error: OPENAI_API_KEY not set.")
    sys.exit(1)
openai.api_key = api_key

enc = tiktoken.get_encoding("cl100k_base")


def file_token_count(text: str) -> int:
    return len(enc.encode(text))


def load_gitignore(base_path: Path) -> pathspec.PathSpec | None:
    path = base_path / ".gitignore"
    if not path.exists():
        return None
    return pathspec.PathSpec.from_lines("gitwildmatch", path.read_text().splitlines())


def is_ignored(filepath: str, spec: pathspec.PathSpec | None) -> bool:
    return spec and spec.match_file(filepath) # type: ignore


def list_relevant_files(base_path: Path, gitignore_spec: pathspec.PathSpec | None) -> list[Path]:
    files = []
    for root, dirs, filenames in os.walk(base_path):
        dirs[:] = [d for d in dirs if d not in EXCLUDE_DIRS]
        for name in filenames:
            ext = Path(name).suffix
            full_path = Path(root) / name
            rel_path = full_path.relative_to(base_path)
            if ext in INCLUDE_EXTS and not is_ignored(str(rel_path), gitignore_spec):
                if full_path.stat().st_size <= MAX_FILE_SIZE_MB * 1024 * 1024:
                    files.append(full_path)
    return sorted(files, key=lambda f: f.stat().st_size)


def summarize_text(text: str) -> str:
    prompt = (
        "Summarize the following source file for LLM-assisted understanding:\n"
        "- Focus on key components, classes, functions, and logic\n"
        "- Format clearly and concisely\n\n"
        f"{text[:4000]}"
    )
    try:
        response = openai.chat.completions.create(
            model=OPENAI_MODEL,
            messages=[{"role": "user", "content": prompt}],
            temperature=0.2
        )
        if response and response.choices:
            return response.choices[0].message.content.strip() # type: ignore
        return "[Summary unavailable due to empty response]"
    except Exception as e:
        print(f"Error summarizing file: {e}")
        return "[Summary unavailable due to error]"


def get_cached_summary(text: str) -> str:
    digest = hashlib.sha256(text.encode("utf-8")).hexdigest()
    cache_file = CACHE_DIR / f"{digest}.txt"
    if cache_file.exists():
        return cache_file.read_text()
    summary = summarize_text(text)
    cache_file.write_text(summary)
    return summary


def build_context(base_path: Path, max_tokens: int, summarize_large: bool) -> str:
    gitignore = load_gitignore(base_path)
    tokens_used = 0
    parts = []

    files = list_relevant_files(base_path, gitignore)
    print(f"✓ Found {len(files)} relevant files")

    for path in files:
        try:
            content = path.read_text(encoding="utf-8", errors="ignore")
        except Exception as e:
            print(f"Skipping {path}: {e}")
            continue

        tokens = file_token_count(content)
        rel_path = path.relative_to(base_path)

        if tokens > MAX_FILE_TOKENS_BEFORE_SUMMARY:
            if summarize_large:
                summary = get_cached_summary(content)
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


def main():
    parser = argparse.ArgumentParser(description="Generate repo context for ChatGPT.")
    parser.add_argument("--max-tokens", type=int, default=DEFAULT_MAX_TOTAL_TOKENS)
    parser.add_argument("--summarize", action="store_true", help="Summarize large files with OpenAI.")
    parser.add_argument("--output", type=str, default="context.txt")
    parser.add_argument("--base", type=str, default=".")
    args = parser.parse_args()

    base_path = Path(args.base).resolve()
    context = build_context(base_path, args.max_tokens, args.summarize)
    output_path = Path(args.output).resolve()
    output_path.write_text(context, encoding="utf-8")

    print(f"\nWrote {output_path} with {file_token_count(context)} tokens.")


if __name__ == "__main__":
    main()
