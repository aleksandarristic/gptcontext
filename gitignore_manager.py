import logging
from pathlib import Path
from typing import List, Optional

import pathspec

logger = logging.getLogger(__name__)


class GitignoreManager:
    """
    Responsible for reading and updating a .gitignore file under `base_path`.
    """

    def __init__(self, base_path: Path) -> None:
        """
        Args:
            base_path: The root directory where .gitignore may reside.
        """
        self.base_path = base_path
        self.gitignore_path = base_path / ".gitignore"

    def load_spec(self) -> Optional[pathspec.PathSpec]:
        """
        Load and compile .gitignore into a PathSpec, or return None if not present.

        Returns:
            A PathSpec object if .gitignore exists and is readable; otherwise None.
        """
        if not self.gitignore_path.exists():
            return None

        try:
            lines = self.gitignore_path.read_text(encoding="utf-8").splitlines()
            return pathspec.PathSpec.from_lines("gitwildmatch", lines)
        except Exception as e:
            logger.warning(f"Could not read {self.gitignore_path}: {e}")
            return None

    def ensure_entries(self, entries: List[str]) -> None:
        """
        Ensure that each string in `entries` appears (exactly) on its own line
        in .gitignore. If .gitignore is missing, do nothing. Any missing
        entries are appended at the end (with a preceding comment).

        Args:
            entries: A list of patterns (e.g. [".gptcontext.txt", ".gptcontext-cache/"]).
        """
        if not self.gitignore_path.exists():
            return

        try:
            raw = self.gitignore_path.read_text(encoding="utf-8")
        except Exception as e:
            logger.warning(f"Could not read {self.gitignore_path}: {e}")
            return

        lines = raw.splitlines()
        existing = {line.strip() for line in lines if line.strip() in set(entries)}
        missing = [e for e in entries if e not in existing]
        if not missing:
            return

        try:
            with self.gitignore_path.open("a", encoding="utf-8") as f:
                # Ensure final newline
                if lines and not raw.endswith("\n"):
                    f.write("\n")
                f.write("# Ignore GPT context outputs and cache\n")
                for entry in missing:
                    f.write(f"{entry}\n")
            logger.info(f"Appended {missing} to {self.gitignore_path.name}")
        except Exception as e:
            logger.warning(f"Failed to update {self.gitignore_path}: {e}")
