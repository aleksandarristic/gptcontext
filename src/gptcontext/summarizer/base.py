from typing import Tuple


class Summarizer:
    def summarize(self, text: str, rel_path: str) -> Tuple[str, bool]:
        """
        Summarize the given text and return a tuple of (summary, success_flag).
        """
        raise NotImplementedError

    def get_cached_summary(self, text: str, rel_path: str) -> Tuple[str, bool]:
        """
        Return a cached summary if available, or generate one.
        Default implementation: calls summarize(). Override if caching is desired.
        """
        return self.summarize(text, rel_path)
