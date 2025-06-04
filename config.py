from pathlib import Path

# Absolute path to the directory where this config file resides
SCRIPT_DIR = Path(__file__).resolve().parent

# Maximum total number of tokens allowed in the final context output
MAX_TOTAL_TOKENS = 12000

# Per-file token threshold; if a file exceeds this, it will be summarized (if --summarize is enabled)
MAX_FILE_TOKENS = 5000

# Maximum file size (in megabytes); files larger than this are skipped entirely
MAX_FILE_SIZE_MB = 1

# Default base directory to scan for source files
BASE_DIR = "."

# Output filename for the generated context content
CONTEXT_OUTPUT_FILENAME = ".gptcontext.txt"

# Output filename for the optional message template
MESSAGE_OUTPUT_FILENAME = ".gptcontext_message.txt"

# Cache directory name for summaries, relative to the project root
GPTCONTEXT_CACHE_DIRNAME = ".gptcontext-cache"

# OpenAI model used for summarization (when --summarize is enabled)
OPENAI_MODEL = "gpt-3.5-turbo"

# Token encoder name used by tiktoken to measure token usage
ENCODING_NAME = "cl100k_base"

# Path to the template used when generating a ChatGPT message prompt
MESSAGE_TEMPLATE_FILE = SCRIPT_DIR / "message_sample.txt"

# File extensions to include in context generation
INCLUDE_EXTS = {
    ".py", ".md", ".js", ".ts", ".jsx", ".tsx", ".json", ".toml", ".yaml", ".yml",
    ".html", ".css", ".scss", ".sass", ".less", ".java", ".go", ".rs", ".cpp", ".c",
    ".h", ".hpp", ".cs", ".swift", ".kt", ".m", ".sh", ".bash", ".zsh", ".ps1", ".pl",
    ".rb", ".php", ".ini", ".cfg", ".env", ".txt", ".xml"
}

# Directory names to exclude from scanning (e.g. build artifacts, virtualenvs, caches)
EXCLUDE_DIRS = {
    ".git", ".svn", ".hg", "node_modules", "__pycache__", "dist", "build", ".venv",
    "env", ".mypy_cache", ".pytest_cache", ".vscode", ".idea", ".gptcontext-cache",
    ".DS_Store", "__snapshots__", ".coverage", ".cache"
}

# Specific filenames to exclude even if they match allowed extensions
EXCLUDE_FILES = {
    ".gptcontext.txt", ".gptcontext_message.txt", "README.md", "CHANGELOG.md",
    "LICENSE", "CONTRIBUTING.md", "CODE_OF_CONDUCT.md", "SECURITY.md"
}
