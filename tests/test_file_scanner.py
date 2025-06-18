import pytest

import gptcontext.config as config
from gptcontext.exclude_matcher import ExcludeMatcher  # ✅ required
from gptcontext.file_scanner import FileScanner
from gptcontext.gitignore_manager import GitignoreManager


@pytest.fixture
def setup_config(tmp_path, monkeypatch):
    # Initialize config with tmp_path as base
    monkeypatch.chdir(tmp_path)
    config.init_config(tmp_path)
    return tmp_path

@pytest.fixture
def create_repo(setup_config):
    base = setup_config
    # Create files and directories under base
    (base / "include.py").write_text("print(1)")
    (base / "exclude.txt").write_text("ignore me")
    # Create an excluded directory
    excluded_dir = base / "node_modules"
    excluded_dir.mkdir()
    (excluded_dir / "module.js").write_text("console.log(1);")
    # Create .gitignore to ignore ignored.md
    gitignore = base / ".gitignore"
    gitignore.write_text("ignored.md")
    (base / "ignored.md").write_text("# ignore")
    return base

def test_list_files_filters(create_repo):
    base = create_repo
    # Load .gitignore spec
    gim = GitignoreManager(base)
    spec = gim.load_spec()

    exclude_matcher = ExcludeMatcher(patterns=["node_modules/"])  # ✅ fixed

    # Instantiate FileScanner with both repo_root and scan_root set to base
    scanner = FileScanner(
        repo_root=base,
        scan_root=base,
        include_exts={".py", ".md"},
        exclude_matcher=exclude_matcher,  # ✅ required param
        skip_files=set(),
        gitignore_spec=spec,
    )
    files = scanner.list_files()
    # Should include include.py, but not exclude.txt, module.js, or ignored.md
    names = [p.name for p in files]
    assert "include.py" in names
    assert "exclude.txt" not in names
    assert "module.js" not in names
    assert "ignored.md" not in names
