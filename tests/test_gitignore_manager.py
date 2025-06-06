import pytest

from gitignore_manager import GitignoreManager


@pytest.fixture
def temp_repo(tmp_path):
    # Create a temporary repo with a .gitignore file
    repo = tmp_path / "repo"
    repo.mkdir()
    gitignore = repo / ".gitignore"
    gitignore.write_text("# Initial ignore\nignored_file.txt\n")
    return repo


def test_ensure_entries_appends_missing(temp_repo):
    repo = temp_repo
    manager = GitignoreManager(repo)
    entries = ["new_file.log", "ignored_file.txt"]
    manager.ensure_entries(entries)

    content = (repo / ".gitignore").read_text().splitlines()
    # Should contain original line, comment, and new_file.log (ignored_file.txt was already present)
    assert "ignored_file.txt" in content
    # The code now writes "# Ignore GPT context outputs and cache", so we check the prefix:
    assert any(line.startswith("# Ignore GPT context outputs") for line in content)
    assert "new_file.log" in content
