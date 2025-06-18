import os
from pathlib import Path
from typing import List, Optional, Set

import pathspec

import gptcontext.config as config
from gptcontext.exclude_matcher import ExcludeMatcher


class FileScanner:
    """
    Scans a directory tree (the “scan root”), applying include/exclude rules
    (including .gitignore and ExcludeMatcher), and returns a sorted list of relevant files.
    """

    def __init__(
        self,
        repo_root: Path,
        scan_root: Path,
        include_exts: Set[str],
        exclude_matcher: ExcludeMatcher,
        skip_files: Set[str],
        gitignore_spec: Optional[pathspec.PathSpec],
    ) -> None:
        """
        Args:
            repo_root: The repository root (where .gitignore lives). Patterns in .gitignore
                       are matched against paths relative to this directory.
            scan_root: The directory to actually walk (relative to repo_root). All files under
                       scan_root will be considered (subject to excludes).
            include_exts: File extensions to include (e.g., {".py", ".md"}).
            exclude_matcher: ExcludeMatcher instance to determine excluded files/dirs.
            skip_files: Filenames to skip because they are generated outputs or messages.
            gitignore_spec: A PathSpec compiled from .gitignore (patterns relative to repo_root),
                            or None if there is no .gitignore.
        """
        self.repo_root = repo_root
        self.base_path = scan_root
        self.include_exts = include_exts
        self.exclude_matcher = exclude_matcher
        self.skip_files = skip_files
        self.gitignore_spec = gitignore_spec

    def _is_ignored(self, rel_path: str) -> bool:
        """
        Check the .gitignore spec (if any) for the given relative path.

        Args:
            rel_path: A path string relative to `repo_root`.

        Returns:
            True if the path matches .gitignore; False otherwise.
        """
        return bool(self.gitignore_spec and self.gitignore_spec.match_file(rel_path))

    def list_files(self) -> List[Path]:
        """
        Walk through `scan_root` and collect files that:
          - Have an extension in `include_exts`.
          - Are not inside any directory or file matched by ExcludeMatcher.
          - Are not named in `skip_files`.
          - Are smaller than MAX_FILE_SIZE_MB (from `config`).
          - Are not ignored by .gitignore (if present).

        Returns:
            A list of Path objects (absolute), sorted by ascending file size.
        """
        result: List[Path] = []
        for root, dirs, files in os.walk(self.base_path):
            rel_root = Path(root).relative_to(self.repo_root)

            # Skip entire dir if excluded
            if self.exclude_matcher.is_excluded(rel_root, is_dir=True):
                dirs[:] = []  # prune walk
                continue

            # Filter subdirs (prune walk)
            dirs[:] = [
                d for d in dirs if not self.exclude_matcher.is_excluded(Path(root, d), is_dir=True)
            ]

            for fname in files:
                full_path = Path(root) / fname
                rel_repo = full_path.relative_to(self.repo_root)

                # Skip excluded files by name/ext
                if fname in self.skip_files or full_path.suffix not in self.include_exts:
                    continue

                # Check .gitignore
                if self._is_ignored(str(rel_repo)):
                    continue

                # Check ExcludeMatcher
                why = self.exclude_matcher.why_excluded(rel_repo, is_dir=False)
                if why:
                    # Optional: uncomment for debug output
                    print(f"EXCLUDED {rel_repo} → {why}")
                    continue

                # Check file size limit
                if full_path.stat().st_size > config.MAX_FILE_SIZE_MB * 1024 * 1024:
                    continue

                result.append(full_path)

        # Sort by file size ascending
        return sorted(result, key=lambda p: p.stat().st_size)
