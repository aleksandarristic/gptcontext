class SummarizationError(Exception):
    """Raised when summarization fails in a way that should halt processing."""

    pass


class QuotaExceededError(SummarizationError):
    """Raised when OpenAI quota is exceeded."""

    pass


class APIKeyError(SummarizationError):
    """Raised when API key is missing or invalid."""

    pass
