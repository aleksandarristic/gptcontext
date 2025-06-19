"""
CLI entrypoint for GPTContext. Parses arguments and delegates to the runner.
"""

import argparse
import logging
import sys
import textwrap
from pathlib import Path
from typing import OrderedDict

import yaml

import gptcontext.config as config
from gptcontext.runner import run

logger = logging.getLogger(__name__)


def parse_args() -> argparse.Namespace:
    # We define prog and usage so the help shows “gptcontext [OPTIONS]”
    # add_help=False so we can inject -h/--help into our own group
    parser = argparse.ArgumentParser(
        prog="gptcontext",
        usage="gptcontext [OPTIONS]",
        description=textwrap.dedent("""\
            Generate GPT context from your codebase.
                                    
            This tool scans your project files, applies filtering, and optionally summarizes
            large files using one of the summarizer (included: simple, openai). It generates 
            a context file that can be used for various purposes, such as building AI chatbots 
            or providing context to LLMs.

        """),
        formatter_class=argparse.RawDescriptionHelpFormatter,
        add_help=False,
        epilog=textwrap.dedent("""\
            CONFIGURATION RESOLUTION ORDER:
              1. If you pass --config-file <name>, it tries in this sequence:
                 a) the CLI’s code directory (where gptcontext is installed)
                 b) the project base dir (–base)
                 c) the scan subdirectory (–scan-dir), if given
              2. Otherwise, it looks for `.gptcontext-config.yml` in the base dir.
              3. If none is found, it falls back to built-in defaults.

            PRESETS:
              There is a number of YAML presets included under "presets/" and you can load one via:
                gptcontext --config-file presets/<preset-name>.yml
                
              You can list presets with:
                gptcontext --list-presets 
              
              or print a specific one with:
                gptcontext --show-preset <preset-name>
                               

            EXAMPLES:
              # Scan current directory with default settings:
              gptcontext

              # Scan project, include .md files and exclude .log files:
              gptcontext -i .md -x "*.log"

              # Summarize large files via OpenAI (threshold 3000 tokens):
              gptcontext --summarize --file-token-threshold 3000

              # Use a built-in Python preset:
              gptcontext -c presets/python.yml

              # Generate both context and message template:
              gptcontext --generate-message
                               
              # Dry run: scan and summarize, but don’t write files:
              gptcontext --dry-run
                               
              # A bit more complex example with verbose logging:
              gptcontext --base /path/to/project -c presets/python.yml
                         -i .md -x "*.log"
                         --summarize --file-token-threshold 2000
                         --generate-message --verbose
                               
            For more details, see the documentation at https://github.com/aleksandarristic/gptcontext
        """),
    )

    # ─── OPTIONS (just help) ─────────────────────────────────────────────────
    opts = parser.add_argument_group("OPTIONS")
    opts.add_argument("-h", "--help", action="help", help="Show this help message and exit")

    # ─── Configuration ───────────────────────────────────────────────────────
    cfg = parser.add_argument_group("Configuration")
    cfg.add_argument(
        "-c",
        "--config-file",
        metavar="FILE",
        help="YAML file to override defaults (e.g. presets/python.yml)",
    )
    cfg.add_argument(
        "-L", "--list-presets", action="store_true", help="List bundled & local presets and exit"
    )
    cfg.add_argument(
        "-S", "--show-preset", metavar="NAME", help="Print the full YAML of <NAME> preset and exit"
    )

    # ─── Input / Output ─────────────────────────────────────────────────────
    io = parser.add_argument_group("Input / Output")
    io.add_argument(
        "-b",
        "--base",
        metavar="DIR",
        default=config.BASE_DIR,
        help="Directory in which to scan for files (default: .)",
    )
    io.add_argument("-s", "--scan-dir", metavar="DIR", help="Subdirectory under base to scan")
    io.add_argument("-o", "--output-dir", metavar="DIR", help="Where to write .gptcontext outputs")

    # ─── Filtering ───────────────────────────────────────────────────────────
    filt = parser.add_argument_group("Filtering")
    filt.add_argument(
        "-x",
        "--exclude",
        nargs="+",
        metavar="PAT",
        help="Extra glob or literal patterns to ignore (e.g. '*.md')",
    )
    filt.add_argument(
        "-i",
        "--include",
        nargs="+",
        metavar="EXT",
        help="Extra file extensions to include (e.g. .md)",
    )

    # ─── Summaries & Tokens ─────────────────────────────────────────────────
    summ = parser.add_argument_group("Summaries & Tokens")
    summ.add_argument(
        "--summarize", action="store_true", help="Use OpenAI to summarize large files"
    )
    summ.add_argument(
        "--file-token-threshold", type=int, help="Token count above which to summarize"
    )
    summ.add_argument("--summarizer", metavar="NAME", help="Which summarizer backend to use")
    summ.add_argument(
        "--max-tokens", type=int, default=None, help="Total token budget for final context"
    )
    summ.add_argument(
        "--continue-on-error",
        action="store_true",
        help="Ignore summarization failures and keep going",
    )

    # ─── Miscellaneous ───────────────────────────────────────────────────────
    misc = parser.add_argument_group("Miscellaneous")
    misc.add_argument(
        "--generate-message", action="store_true", help="Also build a message template file"
    )
    misc.add_argument("--output", metavar="FILE", help="Override the context output filename")
    misc.add_argument("--verbose", action="store_true", help="Enable debug logging")
    misc.add_argument(
        "--dry-run", action="store_true", help="Scan & summarize, but don’t write any files"
    )

    return parser.parse_args()


# helper to find all presets (stem -> Path to file)
def find_presets(base_dir: str):
    presets = OrderedDict()
    pkg_dir = Path(__file__).parent.parent / "presets"
    user_dir = Path(base_dir) / "presets"
    for d in (pkg_dir, user_dir):
        if d.is_dir():
            for f in sorted(d.glob("*.yml")):
                presets[f.stem] = f
    return presets


def main():
    args = parse_args()

    logging.basicConfig(
        level=logging.DEBUG if args.verbose else logging.INFO,
        format="%(message)s",
    )

    if args.list_presets:
        presets = find_presets(args.base)
        if not presets:
            print("No presets found.")
            sys.exit(0)

        # compute column width based on the longest filename
        max_len = max(len(p.name) for p in presets.values())
        for stem, path in presets.items():
            data = yaml.safe_load(path.read_text(encoding="utf-8")) or {}
            desc = data.get("description", "No description provided")
            # name.ljust to align descriptions
            print(f"{path.name.ljust(max_len + 2)}{desc}")
        sys.exit(0)

    if args.show_preset:
        presets = find_presets(args.base)
        key = args.show_preset

        # this needs to be smarter, but for now we just strip common extensions
        if key.lower().endswith(".yml"):
            key = key[:-4]
        if key.lower().endswith(".yaml"):
            key = key[:-5]

        path = presets.get(key)
        if not path:
            print(f"Preset '{args.show_preset}' not found.")
            sys.exit(1)
        print(path.read_text(encoding="utf-8"))
        sys.exit(0)

    # doesn't actually make sense to have this here
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
