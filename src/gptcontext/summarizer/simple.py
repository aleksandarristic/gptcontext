from typing import Tuple

from gptcontext.summarizer.base import Summarizer


class SimpleSummarizer(Summarizer):
    def summarize(self, text: str, rel_path: str) -> Tuple[str, bool]:
        lines = text.splitlines()
        preview = "\n".join(lines[:20])
        return f"# Preview of {rel_path}\n{preview}", True
