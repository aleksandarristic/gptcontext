import os
from pathlib import Path
from typing import List, Optional, Set

import pathspec

import config


class FileScanner:
    """
    Scans a directory tree, applying include/exclude rules (including .gitignore),
    and returns a sorted list of relevant files.
    """

    def __init__(
        self,
        base_path: Path,
        include_exts: Set[str],
        exclude_dirs: Set[str],
        exclude_files: Set[str],
        skip_files: Set[str],
        gitignore_spec: Optional[pathspec.PathSpec],
    ) -> None:
        """
        Args:
            base_path: Root directory to scan.
            include_exts: File extensions to include (e.g. {".py", ".md"}).
            exclude_dirs: Directory names to skip (e.g. {"node_modules", ".git"}).
            exclude_files: Specific filenames to skip (e.g. {".gptcontext.txt"}).
            skip_files: Filenames to skip because they are outputs (context/message).
            gitignore_spec: A PathSpec compiled from .gitignore, or None.
        """
        self.base_path = base_path
        self.include_exts = include_exts
        self.exclude_dirs = exclude_dirs
        self.exclude_files = exclude_files
        self.skip_files = skip_files
        self.gitignore_spec = gitignore_spec

    def _is_ignored(self, rel_path: str) -> bool:
        """
        Check .gitignore spec (if any) for the given relative path.

        Args:
            rel_path: A path string relative to base_path.

        Returns:
            True if the path matches .gitignore; False otherwise.
        """
        return bool(self.gitignore_spec and self.gitignore_spec.match_file(rel_path))

    def list_files(self) -> List[Path]:
        """
        Walk through `base_path` and collect files that:
          - Have an extension in `include_exts`.
          - Are not in `exclude_dirs`.
          - Are not named in `exclude_files` or `skip_files`.
          - Are smaller than MAX_FILE_SIZE_MB.
          - Are not ignored by .gitignore (if present).

        Returns:
            A list of Path objects, sorted by ascending file size.
        """
        result: List[Path] = []
        for root, dirs, files in os.walk(self.base_path):
            # Remove excluded directories from traversal
            dirs[:] = [d for d in dirs if d not in self.exclude_dirs]
            for fname in files:
                full_path = Path(root) / fname
                rel = full_path.relative_to(self.base_path)
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
                if self._is_ignored(str(rel)):
                    continue

                result.append(full_path)

        # Sort by file size ascending
        return sorted(result, key=lambda p: p.stat().st_size)
