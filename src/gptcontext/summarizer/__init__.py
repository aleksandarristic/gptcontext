from pathlib import Path

from gptcontext.summarizer.base import Summarizer
from gptcontext.summarizer.chatgpt import ChatGPTSummarizer
from gptcontext.summarizer.simple import SimpleSummarizer


def get_summarizer(cfg, args, cache_dir: Path) -> Summarizer:
    """
    Factory to return the appropriate Summarizer instance based on config.
    """
    selected = (args.summarizer or cfg.get("SUMMARIZER", "chatgpt")).lower()

    if selected == "chatgpt":
        if not args.summarize:
            raise RuntimeError(
                "Config selects 'chatgpt' summarizer, but --summarize is not enabled."
            )
        return ChatGPTSummarizer(model=cfg.OPENAI_MODEL, cache_dir=cache_dir)

    elif selected == "simple":
        return SimpleSummarizer()

    raise ValueError(f"Unknown summarizer selected in config: {selected}")
