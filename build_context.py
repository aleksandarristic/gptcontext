#!/usr/bin/env python3

import argparse
import logging
import os
from pathlib import Path
from string import Template

import pathspec
import tiktoken

import config
from summarizer import get_cached_summary

enc = tiktoken.get_encoding(config.ENCODING_NAME)
logger = logging.getLogger(__name__)


def file_token_count(text: str) -> int:
    return len(enc.encode(text))


def load_gitignore(base_path: Path) -> pathspec.PathSpec | None:
    path = base_path / ".gitignore"
    return (
        pathspec.PathSpec.from_lines("gitwildmatch", path.read_text().splitlines())
        if path.exists()
        else None
    )


def is_ignored(filepath: str, spec: pathspec.PathSpec | None) -> bool:
    return spec and spec.match_file(filepath)  # type: ignore


def list_relevant_files(
    base_path: Path,
    gitignore_spec,
    include_exts,
    exclude_dirs,
    exclude_files,
    skip_files,
):
    result = []
    for root, dirs, files in os.walk(base_path):
        dirs[:] = [d for d in dirs if d not in exclude_dirs]
        for f in files:
            full_path = Path(root) / f
            rel_path = full_path.relative_to(base_path)
            if (
                f in skip_files
                or f in exclude_files
                or full_path.suffix not in include_exts
            ):
                continue
            if (
                full_path.stat().st_size <= config.MAX_FILE_SIZE_MB * 1024 * 1024
                and not is_ignored(str(rel_path), gitignore_spec)
            ):
                result.append(full_path)
    return sorted(result, key=lambda f: f.stat().st_size)


def build_context(
    base_path,
    max_tokens,
    summarize_large,
    max_file_tokens,
    include_exts,
    exclude_dirs,
    exclude_files,
    context_filename,
    message_filename,
    model,
    cache_dir,
):
    gitignore = load_gitignore(base_path)
    files = list_relevant_files(
        base_path,
        gitignore,
        include_exts,
        exclude_dirs,
        exclude_files,
        {context_filename, message_filename},
    )
    logger.info(f"✓ Found {len(files)} relevant files")
    logger.debug(f"Files: {files}")
    used_tokens = 0
    parts = []

    for path in files:
        rel_path = path.relative_to(base_path)
        try:
            content = path.read_text(encoding="utf-8")
        except Exception as e:
            logger.warning(f"Skipping {rel_path}: {e}")
            continue

        tokens = file_token_count(content)
        if tokens > max_file_tokens:
            if summarize_large:
                summary = get_cached_summary(content, str(rel_path), model, cache_dir)
                stokens = file_token_count(summary)
                if used_tokens + stokens <= max_tokens:
                    parts.append(f"\n# Summary of {rel_path}\n{summary}")
                    used_tokens += stokens
                else:
                    logger.info(f"Skipped summary of {rel_path}: token limit")
            else:
                logger.info(f"Skipped {rel_path}: too large")
        elif used_tokens + tokens <= max_tokens:
            parts.append(f"\n# {rel_path}\n{content}")
            used_tokens += tokens
        else:
            logger.info(f"Skipped {rel_path}: token limit")

    return "\n".join(parts)


def write_message_template(context: str, message_path: Path):
    if not config.MESSAGE_TEMPLATE_FILE.exists():
        logger.warning("No message template found.")
        return
    message = Template(config.MESSAGE_TEMPLATE_FILE.read_text()).substitute(context=context)
    message_path.write_text(message, encoding="utf-8")
    logger.info(f"✓ Wrote message file to \"{message_path}\"")


def main():
    parser = argparse.ArgumentParser(description="Generate GPT context from codebase.")
    parser.add_argument("--base", default=config.BASE_DIR, help="Base directory to scan")
    parser.add_argument("--max-tokens", type=int, default=config.MAX_TOTAL_TOKENS)
    parser.add_argument("--file-token-threshold", type=int, help="Threshold to summarize large files")
    parser.add_argument("--summarize", action="store_true", help="Use OpenAI to summarize large files")
    parser.add_argument("--generate-message", action="store_true", help="Write message template")
    parser.add_argument("--output", type=str, help="Override context output file path")
    parser.add_argument("--verbose", action="store_true", help="Enable debug logging")
    args = parser.parse_args()

    logging.basicConfig(
        level=logging.DEBUG if args.verbose else logging.INFO,
        format="%(message)s"
    )

    base_path = Path(args.base).resolve()
    context_filename = args.output or config.CONTEXT_OUTPUT_FILENAME
    message_filename = config.MESSAGE_OUTPUT_FILENAME
    file_token_threshold = args.file_token_threshold or config.MAX_FILE_TOKENS
    model = config.OPENAI_MODEL

    cache_dir = base_path / ".gptcontext-cache"
    if args.summarize:
        cache_dir.mkdir(exist_ok=True)

    context = build_context(
        base_path,
        args.max_tokens,
        args.summarize,
        file_token_threshold,
        config.INCLUDE_EXTS,
        config.EXCLUDE_DIRS,
        config.EXCLUDE_FILES,
        context_filename,
        message_filename,
        model,
        cache_dir,
    )

    (base_path / context_filename).write_text(context, encoding="utf-8")
    logger.info(f"✓ Wrote context file with {file_token_count(context)} tokens to \"{context_filename}\"")

    if args.generate_message:
        write_message_template(context, base_path / message_filename)


if __name__ == "__main__":
    main()
