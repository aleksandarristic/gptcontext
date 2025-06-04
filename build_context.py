#!/usr/bin/env python3
"""
Generate GPT context from a codebase by scanning relevant files, optionally summarizing large ones,
and writing the combined context to a single output file. Supports a dry-run mode and reports
a final summary of files included vs. skipped.

Usage:
    build_context.py [--base BASE_DIR] [--max-tokens N] [--file-token-threshold N]
                     [--summarize] [--generate-message] [--output FILE]
                     [--verbose] [--dry-run]
"""

import argparse
import concurrent.futures
import logging
import os
from pathlib import Path
from string import Template
from typing import List, Optional, Set, Tuple

import pathspec
import tiktoken

import config
from summarizer import get_cached_summary

enc = tiktoken.get_encoding(config.ENCODING_NAME)
logger = logging.getLogger(__name__)


def file_token_count(text: str) -> int:
    """
    Count the number of tokens in `text` using the configured tiktoken encoder.

    Args:
        text: The input string to tokenize.

    Returns:
        The number of tokens in the text.
    """
    return len(enc.encode(text))


def load_gitignore(base_path: Path) -> Optional[pathspec.PathSpec]:
    """
    Load a .gitignore file (if it exists) and compile it into a PathSpec for matching.

    Args:
        base_path: The directory path where .gitignore might reside.

    Returns:
        A PathSpec object if .gitignore exists, or None otherwise.
    """
    path = base_path / ".gitignore"
    if not path.exists():
        return None
    try:
        lines = path.read_text(encoding="utf-8").splitlines()
        return pathspec.PathSpec.from_lines("gitwildmatch", lines)
    except Exception as e:
        logger.warning(f"Could not read {path}: {e}")
        return None


def is_ignored(filepath: str, spec: Optional[pathspec.PathSpec]) -> bool:
    """
    Determine whether a given file path should be ignored according to the provided PathSpec.

    Args:
        filepath: The relative file path to check.
        spec: A PathSpec object representing ignore patterns, or None.

    Returns:
        True if the file matches an ignore pattern; False otherwise.
    """
    return bool(spec and spec.match_file(filepath))


def list_relevant_files(
    base_path: Path,
    gitignore_spec: Optional[pathspec.PathSpec],
    include_exts: Set[str],
    exclude_dirs: Set[str],
    exclude_files: Set[str],
    skip_files: Set[str],
) -> List[Path]:
    """
    Recursively walk through the base directory and list all files that:
      - Are not in excluded directories.
      - Have an allowed extension.
      - Are not explicitly excluded by name or by skip_files.
      - Are smaller than MAX_FILE_SIZE_MB.
      - Are not ignored by .gitignore (if present).

    Args:
        base_path: The root directory to start scanning.
        gitignore_spec: A PathSpec compiled from .gitignore, or None.
        include_exts: A set of file extensions to include (e.g., {".py", ".md", ...}).
        exclude_dirs: A set of directory names to skip entirely.
        exclude_files: A set of specific file names to exclude.
        skip_files: A set of filenames representing the context output and message files
                    to avoid including them in the scan.

    Returns:
        A sorted list of Path objects for files that meet all criteria.
    """
    result: List[Path] = []
    for root, dirs, files in os.walk(base_path):
        # Remove excluded directories from traversal
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
    # Sort by file size (ascending)
    return sorted(result, key=lambda p: p.stat().st_size)


def _load_and_count(path: Path) -> Tuple[Path, Optional[str], int]:
    """
    Read file contents and count tokens. If an error occurs, log a warning and return None for content.

    Args:
        path: The Path to read.

    Returns:
        A tuple (path, content_or_None, token_count_or_0).
    """
    try:
        text = path.read_text(encoding="utf-8")
        tokens = file_token_count(text)
        return path, text, tokens
    except Exception as e:
        rel_path = path
        logger.warning(f"Skipping {rel_path}: {e}")
        return path, None, 0


def _decide_inclusion(
    rel_path: Path,
    content: str,
    tokens: int,
    used_tokens: int,
    max_file_tokens: int,
    max_tokens: int,
    summarize_large: bool,
    model: str,
    cache_dir: Path,
) -> Tuple[str, int, str]:
    """
    Decide whether to include a file in full, include a summary, or skip it.

    Args:
        rel_path: Path relative to base for logging.
        content: The full text content of the file.
        tokens: Number of tokens in `content`.
        used_tokens: Number of tokens already included in the context.
        max_file_tokens: Per-file token threshold.
        max_tokens: Total token budget.
        summarize_large: Whether summarization is enabled.
        model: OpenAI model name for summarization.
        cache_dir: Directory to store cached summaries.

    Returns:
        A tuple (action, tokens_to_add, snippet) where:
          - action is one of:
              "include_full", "include_summary",
              "skip_threshold", "skip_summary_token", "skip_total_token"
          - tokens_to_add is the number of tokens this inclusion would add (0 if skipped)
          - snippet is the text to append to context (empty if skipped)
    """
    if tokens > max_file_tokens:
        if summarize_large:
            summary = get_cached_summary(content, str(rel_path), model, cache_dir)
            stokens = file_token_count(summary)
            if used_tokens + stokens <= max_tokens:
                return (
                    "include_summary",
                    stokens,
                    f"\n# Summary of {rel_path}\n{summary}",
                )
            else:
                return "skip_summary_token", 0, ""
        else:
            return "skip_threshold", 0, ""
    else:
        if used_tokens + tokens <= max_tokens:
            return "include_full", tokens, f"\n# {rel_path}\n{content}"
        else:
            return "skip_total_token", 0, ""


def build_context(
    base_path: Path,
    max_tokens: int,
    summarize_large: bool,
    max_file_tokens: int,
    include_exts: Set[str],
    exclude_dirs: Set[str],
    exclude_files: Set[str],
    context_filename: str,
    message_filename: str,
    model: str,
    cache_dir: Path,
) -> Tuple[str, int, int, int]:
    """
    Build a combined context string by reading (and possibly summarizing) each relevant file,
    until the total token budget is reached.

    Uses a thread pool to read files and count tokens in parallel, then applies inclusion logic
    sequentially in ascending file-size order.

    Args:
        base_path: The root directory to scan for source files.
        max_tokens: The maximum total token budget for the combined context.
        summarize_large: Whether to call OpenAI to summarize files exceeding max_file_tokens.
        max_file_tokens: Per-file token threshold; files with more tokens are candidates for summarization.
        include_exts: File extensions to include in context generation.
        exclude_dirs: Directory names to skip.
        exclude_files: Specific filenames to exclude.
        context_filename: The name of the context output file (so it is skipped).
        message_filename: The name of the message template file (so it is skipped).
        model: The OpenAI model to use for summarization.
        cache_dir: Directory where summaries are cached.

    Returns:
        A tuple consisting of:
          - combined_context (str),
          - total_tokens_used (int),
          - full_count (number of files included in full),
          - summary_count (number of files included via summary).
    """
    gitignore = load_gitignore(base_path)
    files = list_relevant_files(
        base_path=base_path,
        gitignore_spec=gitignore,
        include_exts=include_exts,
        exclude_dirs=exclude_dirs,
        exclude_files=exclude_files,
        skip_files={context_filename, message_filename},
    )
    logger.info(f"✓ Found {len(files)} relevant files")
    logger.debug(f"All candidate files: {' '.join(p.name for p in files)}")

    # --------- Parallel file loading and token counting ---------
    results: List[Tuple[Path, Optional[str], int]] = []
    with concurrent.futures.ThreadPoolExecutor() as executor:
        # executor.map preserves order of `files`
        results = list(executor.map(_load_and_count, files))

    used_tokens = 0
    full_count = 0
    summary_count = 0
    parts: List[str] = []

    # --------- Sequential inclusion logic ---------
    for path, content, tokens in results:
        if content is None:
            # _load_and_count already logged the error
            continue

        rel_path = path.relative_to(base_path)
        action, tokens_to_add, snippet = _decide_inclusion(
            rel_path=rel_path,
            content=content,
            tokens=tokens,
            used_tokens=used_tokens,
            max_file_tokens=max_file_tokens,
            max_tokens=max_tokens,
            summarize_large=summarize_large,
            model=model,
            cache_dir=cache_dir,
        )

        if action == "include_full":
            parts.append(snippet)
            used_tokens += tokens_to_add
            full_count += 1
            logger.debug(f"Including full {rel_path} ({tokens_to_add} tokens)")
        elif action == "include_summary":
            parts.append(snippet)
            used_tokens += tokens_to_add
            summary_count += 1
            logger.debug(f"Including summary of {rel_path} ({tokens_to_add} tokens)")
        elif action == "skip_threshold":
            logger.info(f"Skipped {rel_path}: exceeds per-file token threshold")
        elif action == "skip_summary_token":
            logger.info(f"Skipped summary of {rel_path}: token limit reached")
        elif action == "skip_total_token":
            logger.info(f"Skipped {rel_path}: total token limit reached")

    combined_context = "\n".join(parts)
    return combined_context, used_tokens, full_count, summary_count


def write_message_template(context: str, message_path: Path) -> None:
    """
    Write out a message template file by substituting the generated context into the template.

    Args:
        context: The string containing the combined context to inject.
        message_path: The Path where the message template should be written.
    """
    if not config.MESSAGE_TEMPLATE_FILE.exists():
        logger.warning("No message template found.")
        return
    template_text = config.MESSAGE_TEMPLATE_FILE.read_text()
    message = Template(template_text).substitute(context=context)
    try:
        message_path.write_text(message, encoding="utf-8")
        logger.info(f'✓ Wrote message file to "{message_path.name}"')
    except Exception as e:
        logger.error(f"Failed to write message template to {message_path}: {e}")


def ensure_gitignore_has_gptcontext(base_path: Path) -> None:
    """
    If a .gitignore exists at base_path, ensure it contains separate entries for:
      - config.CONTEXT_OUTPUT_FILENAME
      - config.MESSAGE_OUTPUT_FILENAME
      - f"{config.GPTCONTEXT_CACHE_DIRNAME}/"
    If any of those lines are missing, append them with a comment.

    Args:
        base_path: The root directory where .gitignore may reside.
    """
    gitignore_path = base_path / ".gitignore"
    if not gitignore_path.exists():
        return

    try:
        raw = gitignore_path.read_text(encoding="utf-8")
    except Exception as e:
        logger.warning(f"Could not read {gitignore_path}: {e}")
        return

    lines = raw.splitlines()
    needed = {
        config.CONTEXT_OUTPUT_FILENAME,
        config.MESSAGE_OUTPUT_FILENAME,
        f"{config.GPTCONTEXT_CACHE_DIRNAME}/",
    }
    existing = {line.strip() for line in lines if line.strip() in needed}

    missing = needed - existing
    if not missing:
        return

    try:
        with gitignore_path.open("a", encoding="utf-8") as f:
            # Ensure there is a final newline before appending
            if lines and not raw.endswith("\n"):
                f.write("\n")
            f.write("# Ignore GPT context outputs and cache\n")
            for entry in sorted(missing):
                f.write(f"{entry}\n")
        logger.info(f"Appended {missing} to {gitignore_path.name}")
    except Exception as e:
        logger.warning(f"Failed to update {gitignore_path}: {e}")


def main() -> None:
    """
    Parse command-line arguments, update .gitignore if present, and generate the
    GPT context file and optionally a message template. In dry-run mode, report
    what would be included without writing any files.
    """
    parser = argparse.ArgumentParser(description="Generate GPT context from codebase.")
    parser.add_argument(
        "--base", default=config.BASE_DIR, help="Base directory to scan"
    )
    parser.add_argument("--max-tokens", type=int, default=config.MAX_TOTAL_TOKENS)
    parser.add_argument(
        "--file-token-threshold",
        type=int,
        help="Threshold to summarize large files",
    )
    parser.add_argument(
        "--summarize",
        action="store_true",
        help="Use OpenAI to summarize large files",
    )
    parser.add_argument(
        "--generate-message",
        action="store_true",
        help="Write message template",
    )
    parser.add_argument("--output", type=str, help="Override context output file path")
    parser.add_argument("--verbose", action="store_true", help="Enable debug logging")
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Do not write any files; just report what would be included",
    )
    args = parser.parse_args()

    logging.basicConfig(
        level=logging.DEBUG if args.verbose else logging.INFO,
        format="%(message)s",
    )

    base_path = Path(args.base).resolve()

    # Update .gitignore entries using values from config.py, if .gitignore exists
    ensure_gitignore_has_gptcontext(base_path)

    context_filename = args.output or config.CONTEXT_OUTPUT_FILENAME
    message_filename = config.MESSAGE_OUTPUT_FILENAME
    file_token_threshold = args.file_token_threshold or config.MAX_FILE_TOKENS
    model = config.OPENAI_MODEL

    cache_dir = base_path / config.GPTCONTEXT_CACHE_DIRNAME
    if args.summarize:
        if not cache_dir.exists():
            cache_dir.mkdir()
            logger.info(f"✓ Created cache directory \"{cache_dir.name}\"")
        else:
            cache_dir.mkdir(exist_ok=True)

    # Build the context (and gather final stats)
    context, total_used, full_count, summary_count = build_context(
        base_path=base_path,
        max_tokens=args.max_tokens,
        summarize_large=args.summarize,
        max_file_tokens=file_token_threshold,
        include_exts=config.INCLUDE_EXTS,
        exclude_dirs=config.EXCLUDE_DIRS,
        exclude_files=config.EXCLUDE_FILES,
        context_filename=context_filename,
        message_filename=message_filename,
        model=model,
        cache_dir=cache_dir,
    )

    # Report summary
    logger.info("--- Context Build Summary ---")
    logger.info(f"Files included in full:     {full_count}")
    logger.info(f"Files included as summary:  {summary_count}")
    logger.info(f"Total tokens used:          {total_used} / {args.max_tokens}")

    if args.dry_run:
        logger.info("Dry-run mode: no files written.")
        return

    # Write context file
    try:
        (base_path / context_filename).write_text(context, encoding="utf-8")
        logger.info(f'✓ Wrote context file to "{context_filename}"')
    except Exception as e:
        logger.error(f"Failed to write context file {context_filename}: {e}")
        return

    if args.generate_message:
        write_message_template(context, base_path / message_filename)


if __name__ == "__main__":
    main()
