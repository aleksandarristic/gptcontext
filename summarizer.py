import hashlib
import os
import time
from logging import getLogger
from pathlib import Path
from typing import Tuple

import openai
import tiktoken

from config import ENCODING_NAME

enc = tiktoken.get_encoding(ENCODING_NAME)
logger = getLogger(__name__)


class SummarizationError(Exception):
    """Raised when summarization fails in a way that should halt processing."""

    pass


class QuotaExceededError(SummarizationError):
    """Raised when OpenAI quota is exceeded."""

    pass


class APIKeyError(SummarizationError):
    """Raised when API key is missing or invalid."""

    pass


def summarize_text(
    text: str, rel_path: str, model: str, max_retries: int = 5
) -> Tuple[str, bool]:
    """
    Summarize text using OpenAI API with retry logic.

    Returns:
        Tuple of (summary_text, success_flag)
    """
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        logger.error("OPENAI_API_KEY not set - cannot summarize files")
        raise APIKeyError(
            "OPENAI_API_KEY environment variable is required for summarization"
        )

    openai.api_key = api_key

    prompt = (
        f"Summarize the following source file for LLM-assisted understanding:\n"
        f"- File: {rel_path}\n"
        f"- Focus on key components, classes, functions, and logic\n"
        f"- Format clearly and concisely\n\n"
    )
    truncated = enc.decode(enc.encode(text)[:3000])

    for attempt in range(max_retries):
        try:
            response = openai.chat.completions.create(
                model=model,
                messages=[{"role": "user", "content": prompt + truncated}],
                temperature=0.2,
            )
            content = (
                response.choices[0].message.content
                if response.choices and response.choices[0].message
                else None
            )

            if not content:
                logger.warning(f"Empty response from OpenAI for {rel_path}")
                return "[Summary unavailable: empty response]", False

            return content.strip(), True

        except openai.RateLimitError:
            if attempt < max_retries - 1:
                wait_time = 2**attempt  # Exponential backoff
                logger.warning(
                    f"Rate limited for {rel_path}, retrying in {wait_time}s... (attempt {attempt + 1}/{max_retries})"
                )
                time.sleep(wait_time)
                continue
            else:
                logger.error(
                    f"Rate limit exceeded for {rel_path} after {max_retries} attempts"
                )
                return (
                    f"[Summary unavailable: rate limit exceeded after {max_retries} attempts]",
                    False,
                )

        except openai.AuthenticationError as e:
            logger.error(f"Authentication failed: {e}")
            raise APIKeyError(f"Invalid OpenAI API key: {e}")

        except Exception as e:
            error_str = str(e).lower()
            if "quota" in error_str or "insufficient_quota" in error_str:
                logger.error(f"OpenAI quota exceeded: {e}")
                raise QuotaExceededError(
                    f"OpenAI quota exceeded. Please check your billing: {e}"
                )
            elif "rate_limit" in error_str:
                if attempt < max_retries - 1:
                    wait_time = 2**attempt
                    logger.warning(
                        f"Rate limited for {rel_path}, retrying in {wait_time}s..."
                    )
                    time.sleep(wait_time)
                    continue
                else:
                    logger.error(f"Rate limit exceeded for {rel_path}")
                    return "[Summary unavailable: rate limit exceeded]", False
            else:
                logger.error(f"Error summarizing {rel_path}: {e}")
                return f"[Summary unavailable: {type(e).__name__}]", False

    return "[Summary unavailable: max retries exceeded]", False


def get_cached_summary(
    text: str, rel_path: str, model: str, cache_dir: Path
) -> Tuple[str, bool]:
    """
    Get cached summary or generate new one.

    Returns:
        Tuple of (summary_text, success_flag)
    """
    digest = hashlib.sha256(text.encode()).hexdigest()
    cache_file = cache_dir / f"{digest}.txt"
    success_cache_file = cache_dir / f"{digest}.success"

    # Check if we have a successful cached summary
    if cache_file.exists() and success_cache_file.exists():
        return cache_file.read_text(), True

    # Check if we have a failed summary (don't retry failed summaries in same session)
    if cache_file.exists() and not success_cache_file.exists():
        return cache_file.read_text(), False

    # Generate new summary
    summary, success = summarize_text(text, rel_path, model)

    # Cache the result
    cache_file.write_text(summary)
    if success:
        success_cache_file.write_text("")  # Empty success marker file

    return summary, success
