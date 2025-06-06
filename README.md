# GPTContext

`gptcontext` is a small CLI utility (and underlying Python library) that scans your codebase, applies include/exclude rules (including `.gitignore`), optionally summarizes large files via OpenAI, and outputs a single “context” file for LLM-assisted workflows. This can be used to feed a chat history or prompt into GPT to help it understand your code.

---

## Table of Contents

1. [Features](#features)  
2. [Installation](#installation)  
3. [Configuration](#configuration)  
4. [Basic Usage](#basic-usage)  
5. [Advanced Usage](#advanced-usage)  
   - [Using a Local Override (`.gptcontext-config.yml`)](#using-a-local-override)  
   - [Summarizing Large Files](#summarizing-large-files)  
   - [Generating a Message Template](#generating-a-message-template)  
   - [Dry Run (Preview Only)](#dry-run-preview-only)  
6. [Python API Usage](#python-api-usage)  
7. [Tests](#tests)  
8. [License](#license)  

---

## Features

- **Selective scanning**: Only files with specified extensions (e.g., `.py`, `.md`) are included.  
- **.gitignore support**: Honors your existing `.gitignore` so you don’t accidentally include unwanted files.  
- **Directory exclusions**: Skip common directories like `node_modules`, `.git`, `dist`, etc.  
- **File-size limit**: Automatically skip files larger than a configured megabyte threshold.  
- **Optional OpenAI summarization**: If a file is too large (token-wise), ask OpenAI to produce a concise summary instead of including the entire file.  
- **Caching**: Summaries are cached so you only pay for summarization once per unique file content.  
- **Message template**: Generate a “context + message” prompt that’s ready to send to a GPT model.  
- **Dry-run mode**: Preview which files would be included/skipped without writing anything to disk.  

---

## Installation

1. Clone the repository (or add it as a dependency in your project):

   ```bash
   git clone https://github.com/your-org/gptcontext.git
   cd gptcontext
   ```

2. (Optional) Create a virtual environment and activate it:

   ```bash
   python3 -m venv .venv
   source .venv/bin/activate
   ```

3. Install runtime dependencies:

   ```bash
   pip install -r requirements.txt
   ```

4. Install dev dependencies (for running tests):

   ```bash
   pip install -r requirements-dev.txt
   ```

---

## Configuration

All default settings (token limits, included extensions, excluded directories, etc.) live in `config.py` under `_DEFAULT_CONFIG`. You can override these on a per-project basis by creating a file named `.gptcontext-config.yml` at your repository root. Any keys in `_DEFAULT_CONFIG` can be overridden; for example:

```yaml
MAX_TOTAL_TOKENS: 8000
MAX_FILE_TOKENS: 3000
INCLUDE_EXTS:
  - .py
  - .md
EXCLUDE_DIRS:
  - node_modules
  - dist
  - .venv
```

When you run the CLI, if no explicit `--config-file` is provided, it will automatically look for `.gptcontext-config.yml` in your working directory.

---

## Basic Usage

### 1. Initialize config (optional)

By default, the CLI assumes your “base” directory is `.` (current working directory). If you have a `.gptcontext-config.yml` in that folder, it’ll be loaded automatically.

_No explicit command is needed; just ensure `.gptcontext-config.yml` exists if you want overrides._

### 2. Run `build_context.py`

```bash
python build_context.py --base . --max-tokens 12000
```

- `--base .`  
  Means “look in the current directory for source files.”
- `--max-tokens 12000`  
  Total token budget across all included files (summaries count as tokens).
- By default, **no summarization** is done. If any file has more than `MAX_FILE_TOKENS`, it will simply be skipped.

After running, you’ll see:

```text
✓ Appended [...ignored patterns...] to .gitignore
✓ Building context from 42 files (parallel loading)...
--- Context Build Summary ---
Files included in full:     35
Files included as summary:  0
Files failed to process:    0
Total tokens used:          3456 / 12000
✓ Wrote context file to "/home/user/.gptcontext/<your-folder>/.gptcontext.txt"
Completed successfully
```

Your generated context file will live here by default:

```
~/.gptcontext/<scan_root_folder>/.gptcontext.txt
```

---

## Advanced Usage

### Using a Local Override

If you want to override any of the default settings on a per-project basis, create a file named `.gptcontext-config.yml` in your repo root. Example:

```yaml
# .gptcontext-config.yml
MAX_TOTAL_TOKENS: 8000
MAX_FILE_TOKENS: 2500
INCLUDE_EXTS:
  - .py
  - .md
  - .json
EXCLUDE_DIRS:
  - node_modules
  - dist
  - .venv
EXCLUDE_FILES:
  - SECRET_CONFIG.yaml
```

Then simply run without any special flags:

```bash
python build_context.py --base . --max-tokens 8000
```

Your overrides from `.gptcontext-config.yml` will be loaded automatically.

---

### Summarizing Large Files

If you have very large files (token-wise) and want GPT to generate summaries instead of skipping them entirely, pass the `--summarize` flag. You must have `$OPENAI_API_KEY` set in your environment.

```bash
export OPENAI_API_KEY="sk-xxxx"
python build_context.py --base . --max-tokens 12000 --file-token-threshold 3000 --summarize
```

- `--file-token-threshold 3000`  
  If a file has more than 3000 tokens, we ask GPT to summarize it.  
- Summaries (once fetched) are cached under `~/.gptcontext/<scan_root>/.gptcontext-cache/`.  
- If summarization fails (or quota is exceeded), the file is skipped (unless you pass `--continue-on-error`).

---

## Using Config Presets

GPTContext supports loading custom config presets via the `--config-file` option.

Presets allow you to quickly tailor GPTContext behavior for different types of projects — for example:

- Frontend-only extraction
- Backend code review
- Infrastructure audit
- Monorepos
- Language-specific tuning (Python, Java, CDK, etc.)
- Security audit of configs/secrets

Presets are provided as YAML files in the `presets/` folder.

### How to use a preset

```bash
gptcontext --config-file presets/<preset-name>.yml
```

For example:

```bash
gptcontext --config-file presets/backend_only.yml
```

### Available Presets

| Preset filename          | Description                                    | Example command                                          |
|--------------------------|------------------------------------------------|---------------------------------------------------------|
| `default.yml`            | Default config — matches GPTContext default    | `gptcontext --config-file presets/default.yml`           |
| `minimal.yml`            | Minimal safe defaults                         | `gptcontext --config-file presets/minimal.yml`           |
| `allcode.yml`            | Maximum code coverage (all source files)      | `gptcontext --config-file presets/allcode.yml`           |
| `review_only.yml`        | Optimized for code review                     | `gptcontext --config-file presets/review_only.yml`       |
| `audit.yml`              | Optimized for security audit (configs, secrets)| `gptcontext --config-file presets/audit.yml`             |
| `frontend_only.yml`      | Frontend app (React, Vue, JS focused)         | `gptcontext --config-file presets/frontend_only.yml`     |
| `backend_only.yml`       | Backend app (API / server focused)            | `gptcontext --config-file presets/backend_only.yml`      |
| `design_docs.yml`        | Design docs / architecture-only               | `gptcontext --config-file presets/design_docs.yml`       |
| `tests_only.yml`         | Tests-only (test files and configs)           | `gptcontext --config-file presets/tests_only.yml`        |
| `infra_only.yml`         | Infrastructure-only (Terraform, K8s, Ansible) | `gptcontext --config-file presets/infra_only.yml`        |
| `python.yml`             | Pure Python repo                              | `gptcontext --config-file presets/python.yml`            |
| `splunkapp.yml`          | Splunk app (TA or App builder)                | `gptcontext --config-file presets/splunkapp.yml`         |
| `python_webapp.yml`      | Python webapp (HTML, Jinja, JS, Markdown)     | `gptcontext --config-file presets/python_webapp.yml`     |
| `flutter.yml`            | Flutter / Dart project                        | `gptcontext --config-file presets/flutter.yml`           |
| `android.yml`            | Android project (Java/Kotlin/XML)             | `gptcontext --config-file presets/android.yml`           |
| `unity.yml`              | Unity game project (C#)                       | `gptcontext --config-file presets/unity.yml`             |
| `dotnet.yml`             | .NET Core / C# project                        | `gptcontext --config-file presets/dotnet.yml`            |
| `monorepo.yml`           | Monorepo (multi-language)                     | `gptcontext --config-file presets/monorepo.yml`          |
| `docs.yml`               | Docs-only / static site / knowledge base      | `gptcontext --config-file presets/docs.yml`              |
| `laravel.yml`            | PHP / Laravel project                         | `gptcontext --config-file presets/laravel.yml`           |
| `rails.yml`              | Ruby on Rails project                         | `gptcontext --config-file presets/rails.yml`             |
| `phoenix.yml`            | Elixir / Phoenix project                      | `gptcontext --config-file presets/phoenix.yml`           |
| `clojure.yml`            | Clojure project                               | `gptcontext --config-file presets/clojure.yml`           |
| `haskell.yml`            | Haskell project (Stack / Cabal)               | `gptcontext --config-file presets/haskell.yml`           |
| `latex.yml`              | LaTeX / scientific writing project            | `gptcontext --config-file presets/latex.yml`             |
| `hdl.yml`                | FPGA / Hardware Design repo                   | `gptcontext --config-file presets/hdl.yml`               |
| `solidity.yml`           | Blockchain / Solidity project                 | `gptcontext --config-file presets/solidity.yml`          |
| `unreal.yml`             | Unreal Engine project                         | `gptcontext --config-file presets/unreal.yml`            |
| `bashops.yml`            | Bash / Shell scripts / DevOps repo            | `gptcontext --config-file presets/bashops.yml`           |
| `github_actions.yml`     | GitHub Actions / CI/CD config repo            | `gptcontext --config-file presets/github_actions.yml`    |
| `reactnative.yml`        | Cross-platform mobile app (React Native/Ionic)| `gptcontext --config-file presets/reactnative.yml`       |
| `datapipeline.yml`       | Data pipeline / ETL project                   | `gptcontext --config-file presets/datapipeline.yml`      |
| `kong.yml`               | API Gateway / Kong / NGINX config repo        | `gptcontext --config-file presets/kong.yml`              |
| `cdk_ts.yml`             | AWS CDK — TypeScript project                  | `gptcontext --config-file presets/cdk_ts.yml`            |
| `cdk_py.yml`             | AWS CDK — Python project                      | `gptcontext --config-file presets/cdk_py.yml`            |
| `cdk_java.yml`           | AWS CDK — Java project                        | `gptcontext --config-file presets/cdk_java.yml`          |
| `cdk_csharp.yml`         | AWS CDK — C# (.NET) project                   | `gptcontext --config-file presets/cdk_csharp.yml`        |

---

### Generating a Message Template

Once you have a context file, you may want to inject it into a chat prompt. If you provide a `message_sample.txt` (the default shipped template), you can ask the CLI to fill it in:

```bash
# Example message_sample.txt (in the code repo):
# You are helping me with my code. Below is the generated context:
#
# ${context}
#
# Now can you explain the main logic?

python build_context.py --base . --generate-message
```

This will create `~/.gptcontext/<scan_root>/.gptcontext_message.txt`, where the placeholder `${context}` is replaced by the full `.gptcontext.txt` content.

---

### Dry Run (Preview Only)

If you just want to see which files would be included/skipped (and how many tokens each contributes) without writing any files, use:

```bash
python build_context.py --base . --max-tokens 12000 --dry-run
```

You will see logs about which files are included or skipped, but no `.gptcontext.txt` is written.

---

## Python API Usage

All the core functionality is also exposed as Python classes/functions. You can integrate them into your own scripts:

```python
from pathlib import Path
from gitignore_manager import GitignoreManager
from file_scanner import FileScanner
from context_builder import ContextBuilder
import config

# 1) Initialize config
config.init_config(base_path=Path("/path/to/project"))

# 2) Update .gitignore
base_path = Path("/path/to/project")
gim = GitignoreManager(base_path)
gim.ensure_entries([
    config.CONTEXT_OUTPUT_FILENAME,
    config.MESSAGE_OUTPUT_FILENAME,
    f"{config.GPTCONTEXT_CACHE_DIRNAME}/",
    config.LOCAL_CONFIG_FILENAME,
])
spec = gim.load_spec()

# 3) Scan for files
scanner = FileScanner(
    repo_root=base_path,
    scan_root=base_path,
    include_exts=config.INCLUDE_EXTS,
    exclude_dirs=config.EXCLUDE_DIRS,
    exclude_files=config.EXCLUDE_FILES,
    skip_files={config.CONTEXT_OUTPUT_FILENAME, config.MESSAGE_OUTPUT_FILENAME},
    gitignore_spec=spec,
)
files = scanner.list_files()

# 4) Build context (no summarization)
builder = ContextBuilder(
    cache_dir=Path.home() / ".gptcontext_cache",
    scan_root=base_path,
    model=config.OPENAI_MODEL,
    max_file_tokens=config.MAX_FILE_TOKENS,
    max_total_tokens=config.MAX_TOTAL_TOKENS,
    summarize_large=False,
)
context_str, total_used, full_count, summary_count, failed_count = builder.build(files)

print(f"Including {full_count} full files, {summary_count} summaries.")
print("Generated context (first 500 chars):")
print(context_str[:500])
```

---

## Tests

To run the test suite, simply:

```bash
pytest -q
```

The tests have been updated to reflect the current constructor signatures and behavior of each component.

---

## License

This project is licensed under the MIT License. See [LICENSE](LICENSE) for details.
