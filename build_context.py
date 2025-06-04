#!/usr/bin/env python3
"""
CLI wrapper that wires up GitignoreManager, FileScanner, and ContextBuilder.
"""

import argparse
import logging
from pathlib import Path

import config
from context_builder import ContextBuilder
from file_scanner import FileScanner
from gitignore_manager import GitignoreManager

logger = logging.getLogger(__name__)


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

    from string import Template

    template_text = config.MESSAGE_TEMPLATE_FILE.read_text()
    message = Template(template_text).substitute(context=context)
    try:
        message_path.write_text(message, encoding="utf-8")
        logger.info(f'✓ Wrote message file to "{message_path.name}"')
    except Exception as e:
        logger.error(f"Failed to write message template to {message_path}: {e}")


def main() -> None:
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

    # 1) Update .gitignore
    gim = GitignoreManager(base_path)
    gim.ensure_entries(
        [
            config.CONTEXT_OUTPUT_FILENAME,
            config.MESSAGE_OUTPUT_FILENAME,
            f"{config.GPTCONTEXT_CACHE_DIRNAME}/",
        ]
    )
    spec = gim.load_spec()

    # 2) Scan files
    scanner = FileScanner(
        base_path=base_path,
        include_exts=config.INCLUDE_EXTS,
        exclude_dirs=config.EXCLUDE_DIRS,
        exclude_files=config.EXCLUDE_FILES,
        skip_files={config.CONTEXT_OUTPUT_FILENAME, config.MESSAGE_OUTPUT_FILENAME},
        gitignore_spec=spec,
    )
    files = scanner.list_files()

    # 3) Create cache directory if summarization is on
    cache_dir = base_path / config.GPTCONTEXT_CACHE_DIRNAME
    if args.summarize:
        if not cache_dir.exists():
            cache_dir.mkdir()
            logger.info(f'✓ Created cache directory "{cache_dir.name}"')
        else:
            cache_dir.mkdir(exist_ok=True)

    # 4) Build context
    builder = ContextBuilder(
        cache_dir=cache_dir,
        model=config.OPENAI_MODEL,
        max_file_tokens=args.file_token_threshold or config.MAX_FILE_TOKENS,
        max_total_tokens=args.max_tokens,
        summarize_large=args.summarize,
    )
    context_str, total_used, full_count, summary_count = builder.build(files)

    # 5) Summary output
    logger.info("--- Context Build Summary ---")
    logger.info(f"Files included in full:     {full_count}")
    logger.info(f"Files included as summary:  {summary_count}")
    logger.info(f"Total tokens used:          {total_used} / {args.max_tokens}")

    if args.dry_run:
        logger.info("Dry-run mode: no files written.")
        return

    # 6) Write context file
    context_filename = args.output or config.CONTEXT_OUTPUT_FILENAME
    try:
        (base_path / context_filename).write_text(context_str, encoding="utf-8")
        logger.info(f'✓ Wrote context file to "{context_filename}"')
    except Exception as e:
        logger.error(f"Failed to write context file {context_filename}: {e}")
        return

    # 7) Optionally write message template
    if args.generate_message:
        write_message_template(context_str, base_path / config.MESSAGE_OUTPUT_FILENAME)


if __name__ == "__main__":
    main()
