"""
CLI entrypoint for GPTContext. Parses arguments and delegates to the runner.
"""

import argparse
import logging
import sys
import textwrap
from pathlib import Path
from typing import OrderedDict

import gptcontext.config as config
from gptcontext.runner import run

logger = logging.getLogger(__name__)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Generate GPT context from codebase.",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=textwrap.dedent("""\
            CONFIGURATION RESOLUTION ORDER:
              1. If you pass --config-file <name>, it tries in this sequence:
                 a) the CLI’s code directory (where gptcontext is installed)
                 b) the project base dir (–base)
                 c) the scan subdirectory (–scan-dir), if given
              2. Otherwise, it looks for `.gptcontext-config.yml` in the base dir.
              3. If none is found, it falls back to built-in defaults.

            PRESETS:
              You can ship YAML presets under `presets/` and load one via:
                gptcontext --config-file presets/<preset-name>.yml

              Provided examples:
                • default   Default GPTContext settings
                • python    Pure Python project
                • frontend  Frontend (JS/React) focus
                • backend   Backend (API/server) focus
        """),
    )

    parser.add_argument(
        "--config-file",
        "-c",
        type=str,
        help="Path to a custom .gptcontext-config.yml. You can use presets/<name>.yml here for existing presets.",
    )
    parser.add_argument(
        "-L",
        "--list-presets",
        action="store_true",
        help="List available configuration presets and exit",
    )
    parser.add_argument("--base", "-b", default=config.BASE_DIR, help="Base directory to scan")
    parser.add_argument("--scan-dir", "-s", type=str, help="Subdirectory to scan")
    parser.add_argument(
        "--output-dir", "-o", type=str, help="Root directory for .gptcontext output"
    )
    parser.add_argument(
        "--exclude",
        "-x",
        nargs="+",
        metavar="PATTERN",
        help="Additional glob/literal patterns to exclude (e.g. '*.md', 'tmp/**')",
    )
    parser.add_argument(
        "-i",
        "--include",
        nargs="+",
        metavar="EXT",
        help="Additional file extensions to include (e.g. .md, .txt)",
    )

    parser.add_argument(
        "--max-tokens", type=int, default=None, help="Maximum total tokens in context"
    )
    parser.add_argument(
        "--file-token-threshold", type=int, help="Threshold to summarize large files"
    )
    parser.add_argument(
        "--summarize", action="store_true", help="Use OpenAI to summarize large files"
    )
    parser.add_argument(
        "--summarizer", type=str, help="Override summarizer backend (e.g., chatgpt, simple)"
    )
    parser.add_argument("--generate-message", action="store_true", help="Write message template")
    parser.add_argument("--output", type=str, help="Override context output file path")
    parser.add_argument("--verbose", action="store_true", help="Enable debug logging")
    parser.add_argument("--dry-run", action="store_true", help="Do not write any files")
    parser.add_argument("--continue-on-error", action="store_true", help="Ignore summary failures")

    return parser.parse_args()


def main():
    args = parse_args()

    logging.basicConfig(
        level=logging.DEBUG if args.verbose else logging.INFO,
        format="%(message)s",
    )

    if args.list_presets:

        def _find_presets(base_dir: str):
            presets = OrderedDict()
            # Packaged presets
            pkg_dir = Path(__file__).parent.parent / "presets"
            # Project-local presets
            user_dir = Path(base_dir) / "presets"

            for d in (pkg_dir, user_dir):
                if d.is_dir():
                    for yml in sorted(d.glob("*.yml")):
                        presets[yml.name] = None
            return list(presets)

        names = _find_presets(args.base)
        if names:
            for name in names:
                print(name)
        else:
            print("No presets found.")
        sys.exit(0)

    # # Validate summarization requirements
    # if args.summarize and not os.getenv("OPENAI_API_KEY"):
    #     logger.error("ERROR: --summarize requires OPENAI_API_KEY environment variable")
    #     sys.exit(1)

    # Resolve paths and config
    base_path = Path(args.base).resolve()

    config_path = None
    if args.config_file:
        candidate_paths = [
            Path(__file__).parent / args.config_file,
            base_path / args.config_file,
        ]
        if args.scan_dir:
            candidate_paths.append((base_path / args.scan_dir) / args.config_file)

        for path in candidate_paths:
            if path.exists():
                config_path = path.resolve()
                break

        if not config_path:
            logger.error("ERROR: Config file not found in expected locations:")
            for p in candidate_paths:
                logger.error(f"  - {p}")
            sys.exit(1)

    config.init_config(base_path, config_path) if config_path else config.init_config(base_path)
    cfg = config.get_config()
    if args.max_tokens is None:
        args.max_tokens = cfg.get("MAX_TOTAL_TOKENS", -1)

    run(args, cfg, base_path)


if __name__ == "__main__":
    main()
