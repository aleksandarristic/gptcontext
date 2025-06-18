import hashlib
from pathlib import Path

import pytest

from gptcontext.summarizer.chatgpt import ChatGPTSummarizer


@pytest.fixture
def dummy_openai(monkeypatch):
    class FakeCompletions:
        def create(self, model, messages, temperature):
            class Msg:
                content = "dummy summary"
            class Choice:
                message = Msg()
            class Response:
                choices = [Choice()]
            return Response()

    class FakeChat:
        completions = FakeCompletions()

    monkeypatch.setattr("openai.chat", FakeChat())
    monkeypatch.setenv("OPENAI_API_KEY", "test-key")
    yield


@pytest.fixture
def temp_cache(tmp_path) -> Path:
    cache_dir = tmp_path / "cache"
    cache_dir.mkdir()
    return cache_dir


def test_get_cached_summary_creates_files(dummy_openai, temp_cache):
    text = "some content"
    rel_path = "file.py"
    model = "gpt-3.5-turbo"

    summarizer = ChatGPTSummarizer(model=model, cache_dir=temp_cache)
    summary, success = summarizer.get_cached_summary(text, rel_path)

    assert success is True
    assert summary == "dummy summary"

    digest = hashlib.sha256(text.encode()).hexdigest()
    assert (temp_cache / f"{digest}.txt").exists()
    assert (temp_cache / f"{digest}.success").exists()


def test_get_cached_summary_uses_cache(dummy_openai, temp_cache):
    text = "cached content"
    digest = hashlib.sha256(text.encode()).hexdigest()
    (temp_cache / f"{digest}.txt").write_text("cached summary")
    (temp_cache / f"{digest}.success").write_text("")

    summarizer = ChatGPTSummarizer(model="gpt-3.5-turbo", cache_dir=temp_cache)
    summary, success = summarizer.get_cached_summary(text, "file.py")

    assert success is True
    assert summary == "cached summary"
