import pytest

from gptcontext.summarizer import get_cached_summary


class DummyResponse:
    def __init__(self, content):
        self.choices = [
            type("Choice", (), {"message": type("Msg", (), {"content": content})})()
        ]


class DummyAPI:
    def __init__(self, return_text):
        self.return_text = return_text

    def create(self, model, messages, temperature):
        return DummyResponse(self.return_text)


@pytest.fixture
def dummy_openai(monkeypatch):
    # Monkeypatch openai.chat.completions.create to return a dummy summary
    import openai

    # Create a dummy `completions` namespace with a `create` function
    class FakeCompletions:
        def create(self, model, messages, temperature):
            return DummyResponse("dummy summary")

    fake_chat = type("ChatNamespace", (), {"completions": FakeCompletions()})
    monkeypatch.setattr(openai, "chat", fake_chat)
    yield


@pytest.fixture
def temp_cache(tmp_path):
    cache = tmp_path / "cache"
    cache.mkdir()
    return cache


def test_get_cached_summary_creates_files(tmp_path, dummy_openai, temp_cache):
    # Prepare text
    text = "some content"
    rel_path = "file.py"
    model = "gpt-3.5-turbo"
    cache_dir = temp_cache

    summary, success = get_cached_summary(text, rel_path, model, cache_dir)
    assert success is True
    assert summary == "dummy summary"
    # Verify cache files exist
    import hashlib

    digest = hashlib.sha256(text.encode()).hexdigest()
    cache_file = cache_dir / f"{digest}.txt"
    success_file = cache_dir / f"{digest}.success"
    assert cache_file.exists()
    assert success_file.exists()


def test_get_cached_summary_uses_cache(tmp_path, dummy_openai, temp_cache):
    # Prepare a cached file
    text = "cached content"
    digest = __import__("hashlib").sha256(text.encode()).hexdigest()
    cache_file = temp_cache / f"{digest}.txt"
    success_file = temp_cache / f"{digest}.success"
    cache_file.write_text("cached summary")
    success_file.write_text("")

    summary, success = get_cached_summary(text, "file.py", "model", temp_cache)
    assert success is True
    assert summary == "cached summary"
