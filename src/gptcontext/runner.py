"""
Runner logic for GPTContext. Orchestrates scanning, summarization, and output.
"""

import logging
import sys
from pathlib import Path
from string import Template

from gptcontext.context_builder import ContextBuilder
from gptcontext.exclude_matcher import ExcludeMatcher
from gptcontext.file_scanner import FileScanner
from gptcontext.gitignore_manager import GitignoreManager
from gptcontext.summarizer import get_summarizer
from gptcontext.summarizer.exceptions import APIKeyError, QuotaExceededError

logger = logging.getLogger(__name__)


def write_message_template(context: str, message_path: Path, template_file: Path) -> None:
    if not template_file.exists():
        logger.warning("No message template found.")
        return

    try:
        template_text = template_file.read_text()
        message = Template(template_text).substitute(context=context)
        message_path.write_text(message, encoding="utf-8")
        logger.info(f'\u2713 Wrote message file to "{message_path}"')
    except Exception as e:
        logger.error(f"Failed to write message template to {message_path}: {e}")


def run(args, cfg, base_path: Path):
    scan_root = (base_path / args.scan_dir).resolve() if args.scan_dir else base_path
    if not scan_root.exists() or not scan_root.is_dir():
        logger.error(f"ERROR: scan directory {scan_root} does not exist or is not a directory")
        sys.exit(1)

    if args.output_dir:
        out_root = Path(args.output_dir).expanduser().resolve()
        output_base = out_root
    else:
        out_root = Path.home() / ".gptcontext"
        output_base = out_root / scan_root.name

    output_base.mkdir(parents=True, exist_ok=True)

    if args.summarize:
        cache_dir = output_base / cfg.GPTCONTEXT_CACHE_DIRNAME
        cache_dir.mkdir(parents=True, exist_ok=True)
        logger.info(f'\u2713 Using cache directory "{cache_dir}"')
    else:
        cache_dir = (
            output_base / cfg.GPTCONTEXT_CACHE_DIRNAME
        )  # lame fallback to fool the type checker

    summarizer = get_summarizer(cfg, args, cache_dir)

    gim = GitignoreManager(base_path)
    spec = gim.load_spec()

    # Combine config excludes with any passed via -x/--exclude
    cfg_excludes = cfg.get("exclude", [])
    cli_excludes = args.exclude or []
    combined_excludes = list(cfg_excludes) + cli_excludes

    exclude_matcher = ExcludeMatcher(
        patterns=combined_excludes,
        use_default_excludes=cfg.get("use_default_excludes", True),
    )

    # Combine config include_exts with CLI args
    cfg_includes = cfg.get("include_exts", set())
    cli_includes = set(args.include or [])
    combined_includes = set(cfg_includes) | cli_includes

    scanner = FileScanner(
        repo_root=base_path,
        scan_root=scan_root,
        include_exts=combined_includes,
        exclude_matcher=exclude_matcher,
        skip_files={cfg.CONTEXT_OUTPUT_FILENAME, cfg.MESSAGE_OUTPUT_FILENAME},
        gitignore_spec=spec,
    )

    files = scanner.list_files()

    builder = ContextBuilder(
        summarizer=summarizer,
        scan_root=scan_root,
        max_file_tokens=args.file_token_threshold or cfg.MAX_FILE_TOKENS,
        max_total_tokens=args.max_tokens,
        summarize_large=args.summarize,
    )

    try:
        context_str, total_used, full_count, summary_count, failed_count = builder.build(files)
    except QuotaExceededError as e:
        logger.error(f"FATAL: {e}")
        logger.error("Please check your OpenAI billing and quota.")
        sys.exit(1)
    except APIKeyError as e:
        logger.error(f"FATAL: {e}")
        sys.exit(1)

    logger.info("--- Context Build Summary ---")
    logger.info(f"Files included in full:     {full_count}")
    logger.info(f"Files included as summary:  {summary_count}")
    if failed_count > 0:
        logger.warning(f"Files failed to process:    {failed_count}")
    logger.info(f"Total tokens used:          {total_used} / {args.max_tokens}")

    if args.dry_run:
        logger.info("Dry-run mode: no files written.")
        return

    context_path = output_base / (args.output or cfg.CONTEXT_OUTPUT_FILENAME)
    try:
        context_path.write_text(context_str, encoding="utf-8")
        logger.info(f'\u2713 Wrote context file to "{context_path}"')
    except Exception as e:
        logger.error(f"Failed to write context file {context_path}: {e}")
        sys.exit(1)

    if args.generate_message:
        message_path = output_base / cfg.MESSAGE_OUTPUT_FILENAME
        write_message_template(context_str, message_path, Path(cfg.get("message_template_file")))

    if failed_count > 0:
        logger.info("Completed with some failures")
        sys.exit(2)
    else:
        logger.info("Completed successfully")
