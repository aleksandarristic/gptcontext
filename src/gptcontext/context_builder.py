import concurrent.futures
import logging
from pathlib import Path
from typing import List, Optional, Tuple

import tiktoken

import gptcontext.config as config
from gptcontext.summarizer.base import Summarizer
from gptcontext.summarizer.exceptions import (
    APIKeyError,
    QuotaExceededError,
    SummarizationError,
)

logger = logging.getLogger(__name__)


def _file_token_count(text: str) -> int:
    """
    Count tokens in `text` using tiktoken with the configured encoding.
    """
    enc = tiktoken.get_encoding(config.ENCODING_NAME)
    return len(enc.encode(text))


def _load_and_count(path: Path) -> Tuple[Path, Optional[str], int]:
    """
    Read the file at `path` and count its tokens. On error, return (path, None, 0)
    and log a warning.

    Returns:
        (path, content_or_None, token_count_or_zero)
    """
    try:
        text = path.read_text(encoding="utf-8")
        return path, text, _file_token_count(text)
    except Exception as e:
        logger.warning(f"Skipping {path}: {e}")
        return path, None, 0


class ContextBuilder:
    """
    Builds a concatenated context string from a list of files, optionally summarizing
    large files via OpenAI. Uses a thread pool to read & count tokens in parallel.
    """

    def __init__(
        self,
        summarizer: Summarizer,
        scan_root: Path,
        max_file_tokens: int,
        max_total_tokens: int,
        summarize_large: bool,
    ) -> None:
        """
        Args:
            cache_dir: Directory where summaries should be cached. Must exist or be creatable.
            model: OpenAI model name to use for summarization.
            max_file_tokens: Per-file token threshold (beyond which summarization is attempted).
            max_total_tokens: Total token budget for the concatenated context.
            summarize_large: If True, attempt to summarize any file whose token count exceeds max_file_tokens.
        """
        self.summarizer = summarizer
        self.base_path = scan_root
        self.max_file_tokens = max_file_tokens
        self.max_total_tokens = max_total_tokens
        self.summarize_large = summarize_large

    def _decide_inclusion(
        self,
        rel_path: Path,
        content: str,
        tokens: int,
        used_tokens: int,
    ) -> Tuple[str, int, str, bool]:
        """
        Decide whether to:
          - include a file in full,
          - include a summary,
          - or skip (and why).

        Returns:
            (action, tokens_to_add, snippet, success_flag)
            action ∈ {"include_full", "include_summary", "skip_threshold", "skip_summary_token", "skip_total_token", "skip_summary_failed"}
        """  # noqa: E501
        if tokens > self.max_file_tokens:
            if self.summarize_large:
                try:
                    summary, success = self.summarizer.get_cached_summary(content, str(rel_path))

                    s_tokens = _file_token_count(summary)

                    if not success:
                        logger.warning(f"Failed to summarize {rel_path}, skipping file")
                        return "skip_summary_failed", 0, "", False

                    if used_tokens + s_tokens <= self.max_total_tokens:
                        return (
                            "include_summary",
                            s_tokens,
                            f"\n# Summary of {rel_path}\n{summary}",
                            True,
                        )
                    else:
                        return "skip_summary_token", 0, "", True

                except (QuotaExceededError, APIKeyError) as e:
                    logger.error(f"Summarization failed: {e}")
                    logger.error("Stopping context generation due to summarization error")
                    raise
                except SummarizationError as e:
                    logger.warning(f"Could not summarize {rel_path}: {e}")
                    return "skip_summary_failed", 0, "", False
            else:
                return "skip_threshold", 0, "", True
        else:
            if used_tokens + tokens <= self.max_total_tokens:
                return "include_full", tokens, f"\n# {rel_path}\n{content}", True
            else:
                return "skip_total_token", 0, "", True

    def build(
        self,
        files: List[Path],
    ) -> Tuple[str, int, int, int, int]:
        """
        Given a list of file Paths (already filtered by FileScanner), read each file,
        count tokens, and decide inclusion. Uses a thread pool to parallelize I/O.

        Args:
            files: A list of Path objects to process, sorted by ascending file size.

        Returns:
            A tuple of:
              - combined_context (str),
              - total_tokens_used (int),
              - full_count (int, number of files included in full),
              - summary_count (int, number of files included as summaries),
              - failed_count (int, number of files that failed to process)
        """
        logger.info(f"✓ Building context from {len(files)} files (parallel loading)...")

        # Parallel read + token count
        with concurrent.futures.ThreadPoolExecutor() as executor:
            results = list(executor.map(_load_and_count, files))

        used_tokens = 0
        full_count = 0
        summary_count = 0
        failed_count = 0
        parts: List[str] = []

        # Sequentially decide inclusion
        for path, content, tokens in results:
            if content is None:
                failed_count += 1
                continue

            rel_path = path.relative_to(self.base_path)

            try:
                action, t_add, snippet, success = self._decide_inclusion(
                    rel_path, content, tokens, used_tokens
                )
            except (QuotaExceededError, APIKeyError):
                # Re-raise critical errors that should stop processing
                raise

            if action == "include_full":
                parts.append(snippet)
                used_tokens += t_add
                full_count += 1
                logger.debug(f"Including full {rel_path} ({t_add} tokens)")
            elif action == "include_summary":
                parts.append(snippet)
                used_tokens += t_add
                summary_count += 1
                logger.debug(f"Including summary of {rel_path} ({t_add} tokens)")
            elif action == "skip_threshold":
                logger.info(f"Skipped {rel_path}: exceeds per-file token threshold")
            elif action == "skip_summary_token":
                logger.info(f"Skipped summary of {rel_path}: token limit reached")
            elif action == "skip_total_token":
                logger.info(f"Skipped {rel_path}: total token limit reached")
            elif action == "skip_summary_failed":
                logger.warning(f"Skipped {rel_path}: summarization failed")
                failed_count += 1

        combined = "\n".join(parts)
        return combined, used_tokens, full_count, summary_count, failed_count
