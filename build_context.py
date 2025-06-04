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
SCRIPT_DIR = Path(__file__).resolve().parent
DEFAULT_MAX_TOTAL_TOKENS = 12000
DEFAULT_MAX_FILE_TOKENS = 5000
DEFAULT_MAX_FILE_SIZE_MB = 1
DEFAULT_BASE_DIR = "."
DEFAULT_CONFIG_FILE = "config.json"
DEFAULT_CONTEXT_OUTPUT = ".gptcontext.txt"
DEFAULT_MESSAGE_OUTPUT = ".gptcontext_message.txt"
DEFAULT_OPENAI_MODEL = "gpt-3.5-turbo-0125"
ENCODING_NAME = "cl100k_base"
MESSAGE_TEMPLATE_FILE = SCRIPT_DIR / "message_sample.txt"

DEFAULT_CONFIG_INCLUDE_EXTS = {
    ".py", ".md", ".js", ".ts", ".jsx", ".tsx", ".json", ".toml", ".yaml", ".yml",
    ".html", ".css", ".scss", ".sass", ".less", ".java", ".go", ".rs", ".cpp", ".c",
    ".h", ".hpp", ".cs", ".swift", ".kt", ".m", ".sh", ".bash", ".zsh", ".ps1", ".pl",
    ".rb", ".php", ".ini", ".cfg", ".env", ".txt", ".xml"
}

DEFAULT_CONFIG_EXCLUDE_DIRS = {
    ".git", ".svn", ".hg", "node_modules", "__pycache__", "dist", "build", ".venv",
    "env", ".mypy_cache", ".pytest_cache", ".vscode", ".idea", ".gptcontext-cache",
    ".DS_Store", "__snapshots__", ".coverage", ".cache"
}
DEFAULT_CONFIG_EXCLUDE_FILES = {
    ".gptcontext.txt", ".gptcontext_message.txt", "README.md", "CHANGELOG.md",
    "LICENSE", "CONTRIBUTING.md", "CODE_OF_CONDUCT.md", "SECURITY.md"
}

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


def load_config(config_path: Path) -> tuple[set[str], set[str], set[str], str, str, int, str]:
    if not config_path.exists():
        print(f"Warning: {config_path} not found. Using default config.")
        return (
            DEFAULT_CONFIG_INCLUDE_EXTS,
            DEFAULT_CONFIG_EXCLUDE_DIRS,
            DEFAULT_CONFIG_EXCLUDE_FILES,
            DEFAULT_CONTEXT_OUTPUT,
            DEFAULT_MESSAGE_OUTPUT,
            DEFAULT_MAX_FILE_TOKENS,
            DEFAULT_OPENAI_MODEL,
        )

    config = json.loads(config_path.read_text())
    include_exts = set(config.get("include_extensions", []))
    exclude_dirs = set(config.get("exclude_dirs", []))
    exclude_files = set(config.get("exclude_files", []))

    context_output = config.get("context_output", DEFAULT_CONTEXT_OUTPUT)
    message_output = config.get("message_output", DEFAULT_MESSAGE_OUTPUT)
    file_token_threshold = config.get("file_token_threshold", DEFAULT_MAX_FILE_TOKENS)
    openai_model = config.get("openai_model", DEFAULT_OPENAI_MODEL)

    return (
        include_exts,
        exclude_dirs,
        exclude_files,
        context_output,
        message_output,
        file_token_threshold,
        openai_model,
    )


def list_relevant_files(
    base_path: Path,
    gitignore_spec: pathspec.PathSpec | None,
    include_exts: set[str],
    exclude_dirs: set[str],
    exclude_files: set[str],
    output_files_to_skip: set[str],
) -> list[Path]:
    files = []
    for root, dirs, filenames in os.walk(base_path):
        dirs[:] = [d for d in dirs if d not in exclude_dirs]
        for name in filenames:
            if name in output_files_to_skip or name in exclude_files:
                continue
            ext = Path(name).suffix
            full_path = Path(root) / name
            rel_path = full_path.relative_to(base_path)
            if ext in include_exts and not is_ignored(str(rel_path), gitignore_spec):
                if full_path.stat().st_size <= DEFAULT_MAX_FILE_SIZE_MB * 1024 * 1024:
                    files.append(full_path)
    return sorted(files, key=lambda f: f.stat().st_size)


def summarize_text(text: str, rel_path: str, model: str, cache_dir: Path) -> str:
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
            model=model,
            messages=[{"role": "user", "content": prompt + truncated}],
            temperature=0.2,
        )
        return response.choices[0].message.content.strip()  # type: ignore
    except Exception as e:
        print(f"Error summarizing {rel_path}: {e}")
        return "[Summary unavailable due to error]"


def get_cached_summary(text: str, rel_path: str, model: str, cache_dir: Path) -> str:
    digest = hashlib.sha256(text.encode("utf-8")).hexdigest()
    cache_file = cache_dir / f"{digest}.txt"
    if cache_file.exists():
        return cache_file.read_text()
    summary = summarize_text(text, rel_path, model, cache_dir)
    cache_file.write_text(summary)
    return summary


def build_context(
    base_path: Path,
    max_tokens: int,
    summarize_large: bool,
    max_file_tokens: int,
    include_exts: set[str],
    exclude_dirs: set[str],
    exclude_files: set[str],
    context_filename: str,
    message_filename: str,
    model: str,
    cache_dir: Path,
) -> str:
    gitignore = load_gitignore(base_path)
    tokens_used = 0
    parts: list[str] = []

    files = list_relevant_files(
        base_path,
        gitignore,
        include_exts,
        exclude_dirs,
        exclude_files,
        output_files_to_skip={context_filename, message_filename},
    )
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
                summary = get_cached_summary(content, str(rel_path), model, cache_dir)
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


def write_message_template(context: str, message_path: Path):
    if not MESSAGE_TEMPLATE_FILE.exists():
        print(
            f"Warning: {MESSAGE_TEMPLATE_FILE} not found. Skipping message generation."
        )
        return

    raw_template = MESSAGE_TEMPLATE_FILE.read_text(encoding="utf-8")
    template = Template(raw_template)

    try:
        message = template.substitute(context=context)
    except KeyError as e:
        print(f"Template substitution failed: missing key {e}")
        return

    message_path.write_text(message, encoding="utf-8")
    print(f"✓ Generated full ChatGPT message at {message_path}")


def main():
    parser = argparse.ArgumentParser(description="Generate repo context for ChatGPT.")
    parser.add_argument("--max-tokens", type=int, default=DEFAULT_MAX_TOTAL_TOKENS)
    parser.add_argument(
        "--file-token-threshold",
        type=int,
        help="Token threshold after which a file is summarized",
    )
    parser.add_argument(
        "--summarize", action="store_true", help="Summarize large files with OpenAI"
    )
    parser.add_argument("--base", type=str, default=DEFAULT_BASE_DIR)
    parser.add_argument(
        "--config", type=str, default=DEFAULT_CONFIG_FILE, help="Path to config JSON"
    )
    parser.add_argument(
        "--generate-message",
        action="store_true",
        help="Create full ChatGPT message file",
    )
    args = parser.parse_args()

    base_path = Path(args.base).resolve()
    config_path = base_path / args.config

    (
        include_exts,
        exclude_dirs,
        exclude_files,
        context_filename,
        message_filename,
        config_token_threshold,
        openai_model,
    ) = load_config(config_path)

    file_token_threshold = args.file_token_threshold or config_token_threshold
    cache_dir = base_path / ".gptcontext-cache"

    if args.summarize:
        cache_dir.mkdir(exist_ok=True)

    context = build_context(
        base_path,
        args.max_tokens,
        args.summarize,
        file_token_threshold,
        include_exts,
        exclude_dirs,
        exclude_files,
        context_filename,
        message_filename,
        openai_model,
        cache_dir,
    )

    output_path = base_path / context_filename
    output_path.write_text(context, encoding="utf-8")
    print(f"\nWrote {output_path} with {file_token_count(context)} tokens.")

    if args.generate_message:
        message_path = base_path / message_filename
        write_message_template(context, message_path)


if __name__ == "__main__":
    main()
