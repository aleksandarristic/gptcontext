import hashlib
import os
from logging import getLogger
from pathlib import Path

import openai
import tiktoken

from config import ENCODING_NAME

enc = tiktoken.get_encoding(ENCODING_NAME)
logger = getLogger(__name__)


def summarize_text(text: str, rel_path: str, model: str) -> str:
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        logger.warning("OPENAI_API_KEY not set")
        return "[Summary unavailable: OPENAI_API_KEY not set]"
    openai.api_key = api_key

    prompt = (
        f"Summarize the following source file for LLM-assisted understanding:\n"
        f"- File: {rel_path}\n"
        f"- Focus on key components, classes, functions, and logic\n"
        f"- Format clearly and concisely\n\n"
    )
    truncated = enc.decode(enc.encode(text)[:3000])

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
        return content.strip() if content else "[Summary unavailable: empty response]"
    except Exception as e:
        logger.error(f"Error summarizing {rel_path}: {e}")
        return "[Summary unavailable due to error]"


def get_cached_summary(text: str, rel_path: str, model: str, cache_dir: Path) -> str:
    digest = hashlib.sha256(text.encode()).hexdigest()
    cache_file = cache_dir / f"{digest}.txt"
    if cache_file.exists():
        return cache_file.read_text()
    summary = summarize_text(text, rel_path, model)
    cache_file.write_text(summary)
    return summary
