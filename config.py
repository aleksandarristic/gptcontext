from pathlib import Path
from typing import Any, Optional

import yaml

# Absolute path to the directory where this config file resides
SCRIPT_DIR = Path(__file__).resolve().parent

# Default configuration values
_DEFAULT_CONFIG = {
    # Maximum total number of tokens allowed in the final context output
    "MAX_TOTAL_TOKENS": 12000,
    # Per-file token threshold; if a file exceeds this, it will be summarized (if --summarize is enabled)
    "MAX_FILE_TOKENS": 5000,
    # Maximum file size (in megabytes); files larger than this are skipped entirely
    "MAX_FILE_SIZE_MB": 1,
    # Default base directory to scan for source files
    "BASE_DIR": ".",
    # Output filename for the generated context content
    "CONTEXT_OUTPUT_FILENAME": ".gptcontext.txt",
    # Output filename for the optional message template
    "MESSAGE_OUTPUT_FILENAME": ".gptcontext_message.txt",
    # Cache directory name for summaries, relative to the project root
    "GPTCONTEXT_CACHE_DIRNAME": ".gptcontext-cache",
    # OpenAI model used for summarization (when --summarize is enabled)
    "OPENAI_MODEL": "gpt-3.5-turbo",
    # Token encoder name used by tiktoken to measure token usage
    "ENCODING_NAME": "cl100k_base",
    # File extensions to include in context generation
    "INCLUDE_EXTS": {
        ".py", ".md", ".js", ".ts", ".jsx", ".tsx", ".json", ".toml", ".yaml", ".yml",
        ".html", ".css", ".scss", ".sass", ".less", ".java", ".go", ".rs", ".cpp", ".c",
        ".h", ".hpp", ".cs", ".swift", ".kt", ".m", ".sh", ".bash", ".zsh", ".ps1", ".pl",
        ".rb", ".php", ".ini", ".cfg", ".env", ".txt", ".xml"
    },
    
    # Directory names to exclude from scanning (e.g. build artifacts, virtualenvs, caches)
    "EXCLUDE_DIRS": {
        ".git", ".svn", ".hg", "node_modules", "__pycache__", "dist", "build", ".venv",
        "env", ".mypy_cache", ".pytest_cache", ".vscode", ".idea", ".gptcontext-cache",
        ".DS_Store", "__snapshots__", ".coverage", ".cache"
    },
    
    # Specific filenames to exclude even if they match allowed extensions
    "EXCLUDE_FILES": {
        ".gptcontext.txt", ".gptcontext_message.txt", "README.md", "CHANGELOG.md",
        "LICENSE", "CONTRIBUTING.md", "CODE_OF_CONDUCT.md", "SECURITY.md"
    }
}

# Path to the template used when generating a ChatGPT message prompt
MESSAGE_TEMPLATE_FILE = SCRIPT_DIR / "message_sample.txt"

# Local config file name
LOCAL_CONFIG_FILENAME = ".gptcontext-config.yml"


class ConfigManager:
    """
    Manages configuration with support for local overrides via .gptcontext-config.yml
    """

    def __init__(self, base_path: Optional[Path] = None):
        """
        Initialize config manager.

        Args:
            base_path: Base directory to look for local config file. Defaults to current directory.
        """
        self.base_path = Path(base_path) if base_path else Path.cwd()
        self._config = _DEFAULT_CONFIG.copy()
        self._load_local_config()

    def _load_local_config(self) -> None:
        """Load and apply local configuration overrides if they exist."""
        local_config_path = self.base_path / LOCAL_CONFIG_FILENAME

        if not local_config_path.exists():
            return

        try:
            with open(local_config_path, "r", encoding="utf-8") as f:
                local_config = yaml.safe_load(f) or {}

            # Apply overrides
            for key, value in local_config.items():
                if key in self._config:
                    # Handle set types specially
                    if isinstance(self._config[key], set) and isinstance(value, list):
                        self._config[key] = set(value)
                    else:
                        self._config[key] = value
                else:
                    print(
                        f"Warning: Unknown config key '{key}' in {LOCAL_CONFIG_FILENAME}"
                    )

            print(f"✓ Loaded local config from {LOCAL_CONFIG_FILENAME}")

        except yaml.YAMLError as e:
            print(f"Warning: Failed to parse {LOCAL_CONFIG_FILENAME}: {e}")
        except Exception as e:
            print(f"Warning: Failed to load {LOCAL_CONFIG_FILENAME}: {e}")

    def get(self, key: str, default: Any = None) -> Any:
        """Get a configuration value."""
        return self._config.get(key, default)

    def __getattr__(self, name: str) -> Any:
        """Allow attribute-style access to config values."""
        if name.startswith("_"):
            raise AttributeError(
                f"'{self.__class__.__name__}' object has no attribute '{name}'"
            )
        return self._config.get(name, getattr(_DEFAULT_CONFIG, name, None))


# Global config manager instance
_config_manager: Optional[ConfigManager] = None


def init_config(base_path: Optional[Path] = None) -> None:
    """Initialize the global config manager with the given base path."""
    global _config_manager
    _config_manager = ConfigManager(base_path)


def get_config() -> ConfigManager:
    """Get the global config manager instance."""
    if _config_manager is None:
        raise RuntimeError("Config not initialized. Call init_config() first.")
    return _config_manager


# For backward compatibility, expose config values as module-level attributes
# These will be updated when init_config() is called
MAX_TOTAL_TOKENS = _DEFAULT_CONFIG["MAX_TOTAL_TOKENS"]
MAX_FILE_TOKENS = _DEFAULT_CONFIG["MAX_FILE_TOKENS"]
MAX_FILE_SIZE_MB = _DEFAULT_CONFIG["MAX_FILE_SIZE_MB"]
BASE_DIR = _DEFAULT_CONFIG["BASE_DIR"]
CONTEXT_OUTPUT_FILENAME = _DEFAULT_CONFIG["CONTEXT_OUTPUT_FILENAME"]
MESSAGE_OUTPUT_FILENAME = _DEFAULT_CONFIG["MESSAGE_OUTPUT_FILENAME"]
GPTCONTEXT_CACHE_DIRNAME = _DEFAULT_CONFIG["GPTCONTEXT_CACHE_DIRNAME"]
OPENAI_MODEL = _DEFAULT_CONFIG["OPENAI_MODEL"]
ENCODING_NAME = _DEFAULT_CONFIG["ENCODING_NAME"]
INCLUDE_EXTS = _DEFAULT_CONFIG["INCLUDE_EXTS"]
EXCLUDE_DIRS = _DEFAULT_CONFIG["EXCLUDE_DIRS"]
EXCLUDE_FILES = _DEFAULT_CONFIG["EXCLUDE_FILES"]


def _update_module_globals():
    """Update module-level globals with current config values."""
    if _config_manager is None:
        return

    global MAX_TOTAL_TOKENS, MAX_FILE_TOKENS, MAX_FILE_SIZE_MB, BASE_DIR
    global CONTEXT_OUTPUT_FILENAME, MESSAGE_OUTPUT_FILENAME, GPTCONTEXT_CACHE_DIRNAME
    global OPENAI_MODEL, ENCODING_NAME, INCLUDE_EXTS, EXCLUDE_DIRS, EXCLUDE_FILES

    MAX_TOTAL_TOKENS = _config_manager.get("MAX_TOTAL_TOKENS")
    MAX_FILE_TOKENS = _config_manager.get("MAX_FILE_TOKENS")
    MAX_FILE_SIZE_MB = _config_manager.get("MAX_FILE_SIZE_MB")
    BASE_DIR = _config_manager.get("BASE_DIR")
    CONTEXT_OUTPUT_FILENAME = _config_manager.get("CONTEXT_OUTPUT_FILENAME")
    MESSAGE_OUTPUT_FILENAME = _config_manager.get("MESSAGE_OUTPUT_FILENAME")
    GPTCONTEXT_CACHE_DIRNAME = _config_manager.get("GPTCONTEXT_CACHE_DIRNAME")
    OPENAI_MODEL = _config_manager.get("OPENAI_MODEL")
    ENCODING_NAME = _config_manager.get("ENCODING_NAME")
    INCLUDE_EXTS = _config_manager.get("INCLUDE_EXTS")
    EXCLUDE_DIRS = _config_manager.get("EXCLUDE_DIRS")
    EXCLUDE_FILES = _config_manager.get("EXCLUDE_FILES")


# Override init_config to also update globals
def init_config(base_path: Optional[Path] = None) -> None:
    """Initialize the global config manager with the given base path."""
    global _config_manager
    _config_manager = ConfigManager(base_path)
    _update_module_globals()
