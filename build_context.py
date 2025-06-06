#!/usr/bin/env python3
"""
CLI wrapper that wires up GitignoreManager, FileScanner, and ContextBuilder.
"""

import argparse
import logging
import sys
from pathlib import Path

import config
from context_builder import ContextBuilder
from file_scanner import FileScanner
from gitignore_manager import GitignoreManager
from summarizer import APIKeyError, QuotaExceededError
from exclude_matcher import ExcludeMatcher

# Silence OpenAI + HTTPX/HTTPCore noise even when --verbose is passed:
logging.getLogger("openai").setLevel(logging.WARNING)
logging.getLogger("httpx").setLevel(logging.WARNING)
logging.getLogger("httpcore").setLevel(logging.WARNING)
logging.getLogger("urllib3").setLevel(logging.WARNING)

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
        logger.info(f'✓ Wrote message file to "{message_path}"')
    except Exception as e:
        logger.error(f"Failed to write message template to {message_path}: {e}")


def main() -> None:
    parser = argparse.ArgumentParser(description="Generate GPT context from codebase.")
    parser.add_argument(
        "--config-file",
        "-c",
        type=str,
        help="Path to a custom .gptcontext-config.yml (overrides default).",
    )
    parser.add_argument(
        "--base", "-b", default=config.BASE_DIR, help="Base directory to scan"
    )
    parser.add_argument(
        "--scan-dir",
        "-s",
        type=str,
        help="Directory (relative to --base) to actually scan. If omitted, uses --base.",
    )
    parser.add_argument(
        "--output-dir",
        "-o",
        type=str,
        help="Root directory under which to write .gptcontext files. Default = $HOME/.gptcontext/",
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
    parser.add_argument(
        "--continue-on-error",
        action="store_true",
        help="Continue processing even if some summaries fail (not recommended for quota errors)",
    )
    args = parser.parse_args()

    logging.basicConfig(
        level=logging.DEBUG if args.verbose else logging.INFO,
        format="%(message)s",
    )

    base_path = Path(args.base).resolve()

    # Determine the “scan” root. If --scan-dir is provided, interpret relative to base_path.
    if args.scan_dir:
        scan_root = (base_path / args.scan_dir).resolve()
        if not scan_root.exists() or not scan_root.is_dir():
            logger.error(
                f"ERROR: scan directory {scan_root} does not exist or is not a directory"
            )
            sys.exit(1)
    else:
        scan_root = base_path

    # Config file lookup logic
    config_path = None
    if args.config_file:
        candidate_paths = [
            Path(__file__).parent / args.config_file,  # relative to build_context.py
            base_path / args.config_file,  # relative to repo root (--base)
        ]
        if args.scan_dir:
            candidate_paths.append(scan_root / args.config_file)  # relative to scan_dir

        # Pick first existing one
        for path in candidate_paths:
            if path.exists():
                config_path = path.resolve()
                break

        if config_path:
            logger.info(f'✓ Using config file "{config_path}"')
            config.init_config(base_path, config_path)
        else:
            logger.error(
                f'ERROR: config file "{args.config_file}" not found in any of the expected locations:'
            )
            logger.error(f"  - {candidate_paths[0]}")
            logger.error(f"  - {candidate_paths[1]}")
            if args.scan_dir:
                logger.error(f"  - {candidate_paths[2]}")
            sys.exit(1)
    else:
        config.init_config(base_path)

    cfg = config.get_config()

    # Determine the “scan” root. If --scan-dir is provided, interpret relative to base_path.
    if args.scan_dir:
        scan_root = (base_path / args.scan_dir).resolve()
        if not scan_root.exists() or not scan_root.is_dir():
            logger.error(
                f"ERROR: scan directory {scan_root} does not exist or is not a directory"
            )
            sys.exit(1)
    else:
        scan_root = base_path

    home = Path.home()
    default_out = home / ".gptcontext"
    out_root = (
        Path(args.output_dir).expanduser().resolve() if args.output_dir else default_out
    )
    # The subfolder name is the final component of scan_root
    subfolder = scan_root.name
    output_base = out_root / subfolder
    output_base.mkdir(parents=True, exist_ok=True)

    # Validate summarization requirements
    if args.summarize:
        import os

        if not os.getenv("OPENAI_API_KEY"):
            logger.error(
                "ERROR: --summarize requires OPENAI_API_KEY environment variable"
            )
            logger.error("Either set OPENAI_API_KEY or remove --summarize flag")
            sys.exit(1)

    # 1) Update .gitignore
    gim = GitignoreManager(base_path)
    gim.ensure_entries(
        [
            cfg.CONTEXT_OUTPUT_FILENAME,
            cfg.MESSAGE_OUTPUT_FILENAME,
            f"{cfg.GPTCONTEXT_CACHE_DIRNAME}/",
            config.LOCAL_CONFIG_FILENAME,  # Also ignore the local config file
        ]
    )
    spec = gim.load_spec()

    # 2) Scan files
    exclude_matcher = ExcludeMatcher(
        patterns=cfg.get("exclude", []),
        use_default_excludes=cfg.get("use_default_excludes", True),
    )

    scanner = FileScanner(
        repo_root=base_path,
        scan_root=scan_root,
        include_exts=cfg.INCLUDE_EXTS,
        exclude_matcher=exclude_matcher,
        skip_files={cfg.CONTEXT_OUTPUT_FILENAME, cfg.MESSAGE_OUTPUT_FILENAME},
        gitignore_spec=spec,
    )

    files = scanner.list_files()

    # 3) Create cache directory if summarization is on
    cache_dir = output_base / cfg.GPTCONTEXT_CACHE_DIRNAME
    if args.summarize:
        cache_dir.mkdir(parents=True, exist_ok=True)
        logger.info(f'✓ Using cache directory "{cache_dir}"')

    # 4) Build context
    builder = ContextBuilder(
        cache_dir=cache_dir,
        scan_root=scan_root,
        model=cfg.OPENAI_MODEL,
        max_file_tokens=args.file_token_threshold or cfg.MAX_FILE_TOKENS,
        max_total_tokens=args.max_tokens,
        summarize_large=args.summarize,
    )

    try:
        context_str, total_used, full_count, summary_count, failed_count = (
            builder.build(files)
        )
    except QuotaExceededError as e:
        logger.error(f"FATAL: {e}")
        logger.error(
            "Please check your OpenAI billing and quota at https://platform.openai.com/account/billing"
        )
        logger.error("You can also run without --summarize to process only small files")
        sys.exit(1)
    except APIKeyError as e:
        logger.error(f"FATAL: {e}")
        logger.error("Please check your OPENAI_API_KEY environment variable")
        sys.exit(1)

    # 5) Summary output
    logger.info("--- Context Build Summary ---")
    logger.info(f"Files included in full:     {full_count}")
    logger.info(f"Files included as summary:  {summary_count}")
    if failed_count > 0:
        logger.warning(f"Files failed to process:    {failed_count}")
    logger.info(f"Total tokens used:          {total_used} / {args.max_tokens}")

    # Warn if we have failures
    if failed_count > 0:
        logger.warning(f"{failed_count} files could not be processed")
        logger.warning("Consider running with --verbose to see detailed errors")

    if args.dry_run:
        logger.info("Dry-run mode: no files written.")
        return

    # 6) Write context file
    context_filename = args.output or cfg.CONTEXT_OUTPUT_FILENAME
    context_path = output_base / context_filename
    try:
        context_path.write_text(context_str, encoding="utf-8")
        logger.info(f'✓ Wrote context file to "{context_path}"')
    except Exception as e:
        logger.error(f"Failed to write context file {context_path}: {e}")
        sys.exit(1)

    # 7) Optionally write message template
    if args.generate_message:
        message_file = output_base / cfg.MESSAGE_OUTPUT_FILENAME
        write_message_template(context_str, message_file)

    # 8) Exit with appropriate code
    if failed_count > 0:
        logger.info("Completed with some failures")
        sys.exit(2)  # Partial success
    else:
        logger.info("Completed successfully")


if __name__ == "__main__":
    main()
