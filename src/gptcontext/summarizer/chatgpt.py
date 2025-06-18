# src/gptcontext/summarizer/chatgpt.py

import hashlib
import logging
import os
import time
from pathlib import Path
from typing import Tuple

import openai
import tiktoken

from gptcontext.config import ENCODING_NAME
from gptcontext.summarizer.base import Summarizer
from gptcontext.summarizer.exceptions import APIKeyError, QuotaExceededError

logger = logging.getLogger(__name__)
enc = tiktoken.get_encoding(ENCODING_NAME)


class ChatGPTSummarizer(Summarizer):
    def __init__(self, model: str, cache_dir: Path):
        self.model = model
        self.cache_dir = cache_dir
        self.api_key = os.getenv("OPENAI_API_KEY")
        if not self.api_key:
            raise APIKeyError("OPENAI_API_KEY environment variable is required")
        openai.api_key = self.api_key

    def summarize(self, text: str, rel_path: str) -> Tuple[str, bool]:
        prompt = (
            f"Summarize the following source file for LLM-assisted understanding:\n"
            f"- File: {rel_path}\n"
            f"- Focus on key components, classes, functions, and logic\n"
            f"- Format clearly and concisely\n\n"
        )
        truncated = enc.decode(enc.encode(text)[:3000])

        for attempt in range(5):
            try:
                response = openai.chat.completions.create(
                    model=self.model,
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
                wait = 2**attempt
                logger.warning(f"Rate limited for {rel_path}, retrying in {wait}s...")
                time.sleep(wait)

            except openai.AuthenticationError as e:
                raise APIKeyError(f"Invalid OpenAI API key: {e}")

            except Exception as e:
                err = str(e).lower()
                if "quota" in err or "insufficient_quota" in err:
                    raise QuotaExceededError(f"OpenAI quota exceeded: {e}")
                elif "rate_limit" in err:
                    continue
                logger.error(f"Error summarizing {rel_path}: {e}")
                return f"[Summary unavailable: {type(e).__name__}]", False

        return "[Summary unavailable: max retries exceeded]", False

    def get_cached_summary(self, text: str, rel_path: str) -> Tuple[str, bool]:
        digest = hashlib.sha256(text.encode()).hexdigest()
        cache_file = self.cache_dir / f"{digest}.txt"
        success_file = self.cache_dir / f"{digest}.success"

        if cache_file.exists() and success_file.exists():
            return cache_file.read_text(), True
        if cache_file.exists():
            return cache_file.read_text(), False

        summary, success = self.summarize(text, rel_path)
        cache_file.write_text(summary)
        if success:
            success_file.write_text("")
        return summary, success
