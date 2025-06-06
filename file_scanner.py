import os
from pathlib import Path
from typing import List, Optional, Set

import pathspec

import config


class FileScanner:
    """
    Scans a directory tree (the “scan root”), applying include/exclude rules 
    (including .gitignore), and returns a sorted list of relevant files.
    """

    def __init__(
        self,
        repo_root: Path,
        scan_root: Path,
        include_exts: Set[str],
        exclude_dirs: Set[str],
        exclude_files: Set[str],
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
            exclude_dirs: Directory names to skip during traversal 
                          (e.g., {"node_modules", ".git"}).
            exclude_files: Specific filenames to skip even if they match allowed extensions 
                           (e.g., {".gptcontext.txt"}).
            skip_files: Filenames to skip because they are generated outputs or messages.
            gitignore_spec: A PathSpec compiled from .gitignore (patterns relative to repo_root),
                            or None if there is no .gitignore.
        """
        self.repo_root = repo_root
        self.base_path = scan_root
        self.include_exts = include_exts
        self.exclude_dirs = exclude_dirs
        self.exclude_files = exclude_files
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
          - Are not inside any directory in `exclude_dirs`.
          - Are not named in `exclude_files` or `skip_files`.
          - Are smaller than MAX_FILE_SIZE_MB (from `config`).
          - Are not ignored by .gitignore (if present).

        Returns:
            A list of Path objects (absolute), sorted by ascending file size.
        """
        result: List[Path] = []
        for root, dirs, files in os.walk(self.base_path):
            # Remove excluded directories from traversal
            dirs[:] = [d for d in dirs if d not in self.exclude_dirs]
            for fname in files:
                full_path = Path(root) / fname
                # Path relative to scan_root (used for extension and size checks)
                # rel_scan = full_path.relative_to(self.base_path)  # noqa: F841
                # Path relative to repo_root (used for .gitignore matching)
                rel_repo = full_path.relative_to(self.repo_root)

                if (
                    fname in self.skip_files
                    or fname in self.exclude_files
                    or full_path.suffix not in self.include_exts
                ):
                    continue

                # Check file size limit
                if full_path.stat().st_size > config.MAX_FILE_SIZE_MB * 1024 * 1024:
                    continue

                # Check .gitignore
                if self._is_ignored(str(rel_repo)):
                    continue

                result.append(full_path)

        # Sort by file size ascending
        return sorted(result, key=lambda p: p.stat().st_size)
