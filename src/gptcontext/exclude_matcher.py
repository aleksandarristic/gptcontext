import fnmatch
from pathlib import Path


class ExcludeMatcher:
    """
    ExcludeMatcher — helper for deciding whether paths should be excluded,
    based on a unified `exclude:` list (supports dir-only, glob, literal patterns).

    Example patterns supported:
        - node_modules/      → dir-only match
        - *.log              → glob match
        - tmp/**             → subtree glob match
        - .DS_Store          → literal file/dir match
    """

    DEFAULT_EXCLUDES = [
        ".git/",
        ".hg/",
        ".svn/",
        "node_modules/",
        "__pycache__/",
        ".DS_Store",
        "Thumbs.db",
    ]

    def __init__(self, patterns=None, use_default_excludes=True):
        """
        :param patterns: list of patterns (strings), from config
        :param use_default_excludes: whether to add built-in excludes
        """
        self.raw_patterns = patterns or []
        if use_default_excludes:
            self.raw_patterns += self.DEFAULT_EXCLUDES

        self.dir_only_patterns = set()
        self.glob_patterns = []
        self.literal_patterns = set()

        self._compile_patterns()

    def _compile_patterns(self):
        for pattern in self.raw_patterns:
            if pattern.endswith("/"):
                # Dir-only pattern
                self.dir_only_patterns.add(pattern.rstrip("/"))
            elif any(char in pattern for char in "*?[]"):
                # Glob pattern
                self.glob_patterns.append(pattern)
            else:
                # Literal file or dir name
                self.literal_patterns.add(pattern)

    def is_excluded(self, path, is_dir=None):
        """
        Check if path should be excluded.

        :param path: Path or str — relative path
        :param is_dir: bool or None — hint if path is a dir
        :return: True if excluded
        """
        return self.why_excluded(path, is_dir=is_dir) is not None

    def why_excluded(self, path, is_dir=None):
        """
        Returns reason why path is excluded, or None if included.

        :param path: Path or str — relative path
        :param is_dir: bool or None — hint if path is a dir
        :return: string reason or None
        """
        path = Path(path)
        name = path.name

        # Determine if dir if not known
        if is_dir is None:
            try:
                is_dir = path.is_dir()
            except OSError:
                is_dir = False

        # Dir-only patterns
        if is_dir and name in self.dir_only_patterns:
            return f"dir-only pattern: {name}/"

        # Literal matches
        if name in self.literal_patterns:
            return f"literal pattern: {name}"

        # Glob patterns — match against full posix path
        path_str = str(path.as_posix())
        for pattern in self.glob_patterns:
            if fnmatch.fnmatch(path_str, pattern):
                return f"glob pattern: {pattern}"

        return None
