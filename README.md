# GPTContext

**GPTContext** is a small CLI utility (and underlying Python library) that scans your codebase, applies include/exclude rules (including your `.gitignore`), optionally summarizes large files via OpenAI, and generates a single “context” file for LLM-assisted workflows. It can also produce a message template ready to send to a GPT model.

---

## Table of Contents

1. [Features](#features)
2. [Installation](#installation)
3. [Configuration](#configuration)
4. [Basic Usage](#basic-usage)
5. [Advanced Usage](#advanced-usage)
6. [CLI Reference](#cli-reference)
7. [Configuration Presets](#configuration-presets)
8. [Development & Testing](#development--testing)
9. [Contributing](#contributing)
10. [License](#license)

---

## Features

* **Selective scanning**: Include only files with configured extensions (e.g. `.py`, `.md`, `.js`).
* **.gitignore support**: Honors existing `.gitignore` patterns.
* **Directory exclusions**: Skip common directories like `node_modules/`, `.venv/`, `dist/`, etc.
* **File-size limit**: Skip files larger than a configured megabyte threshold.
* **Optional OpenAI summarization**: Summarize token‑heavy files instead of skipping them.
* **Caching**: Summaries are cached (by SHA‑256 digest) so you only pay once per unique content.
* **Message template**: Generate a prompt template with `${context}` placeholder.
* **Dry-run mode**: Preview which files would be included or skipped.

---

## Installation

Requires Python 3.8 or newer.

```bash
# Install runtime dependencies only
pip install .

# Install runtime + development dependencies
pip install .[dev]
```

> **Note**: This project uses [PEP 621](https://www.python.org/dev/peps/pep-0621/) metadata in `pyproject.toml`. If your environment does not support PEP 517 install, you can export flat lockfiles:
>
> **With Poetry**:
>
> ```bash
> poetry export --without-hashes -f requirements.txt --output requirements.txt
> poetry export --without-hashes -f requirements.txt --with dev --output requirements-dev.txt
> ```
>
> **With pip-tools**:
>
> 1. Create `requirements.in` containing:
>
>    ```txt
>    -e .
>    ```
> 2. `requirements-dev.in`:
>
>    ```txt
>    -r requirements.in
>    pytest
>    ruff
>    mypy
>    ruamel.yaml
>    ```
> 3. Run:
>
>    ```bash
>    pip-compile requirements.in
>    pip-compile requirements-dev.in
>    ```

---

## Configuration

Runtime and dev dependencies are declared in `pyproject.toml`:

```toml
[project]
dependencies = [
  "openai>=1.14,<2.0",
  "tiktoken>=0.5.1",
  "pathspec>=0.12.1",
  "PyYAML>=6.0",
]

[project.optional-dependencies]
dev = [
  "pytest",
  "ruamel.yaml",
  "ruff",
  "mypy",
]
```

Project-specific overrides live in `.gptcontext-config.yml` at your repo root. Example:

```yaml
MAX_TOTAL_TOKENS: 8000
MAX_FILE_TOKENS: 3000
include_exts:
  - .py
  - .md
exclude:
  - node_modules/
  - dist/
  - .venv/
```

These keys correspond to those in `gptcontext/config.py`.

---

## Basic Usage

```bash
gptcontext --base /path/to/project --max-tokens 12000
```

* `--base`: directory to scan (defaults to current working dir).
* `--max-tokens`: total token budget for the concatenated context.
* By default, large files (token count > `MAX_FILE_TOKENS`) are skipped unless `--summarize` is enabled.

After running, a context file is written to:

```
~/.gptcontext/<project_name>/.gptcontext.txt
```

To also generate a message template:

```bash
gptcontext --base . --max-tokens 12000 --generate-message
```

This creates `.gptcontext_message.txt` alongside the context file, filling in the `${context}` placeholder in your `message_sample.txt` template.

---

## Advanced Usage

### Summarizing Large Files

Enable GPT summarization for files exceeding `--file-token-threshold`:

```bash
export OPENAI_API_KEY="sk-..."
gptcontext --base . --max-tokens 12000 --file-token-threshold 3000 --summarize
```

* Summaries are cached under `~/.gptcontext/<project_name>/.gptcontext-cache/`.
* On quota/auth errors, summarization stops with an error unless `--continue-on-error` is set.

### Dry-run Mode

Preview inclusion/skips without writing any files:

```bash
gptcontext --base . --max-tokens 12000 --dry-run
```

---

## CLI Reference

```text
gptcontext [OPTIONS]

Options:
  -c, --config-file TEXT       custom .gptcontext-config.yml
  -b, --base TEXT              base directory to scan
  -s, --scan-dir TEXT          subdirectory under base to scan
  -o, --output-dir TEXT        directory for output files
      --max-tokens INTEGER     total token budget
      --file-token-threshold INTEGER  threshold to summarize large files
      --summarize              enable OpenAI summarization
      --summarizer TEXT        override summarizer backend (chatgpt, simple)
      --generate-message       also write a message template
      --output TEXT            override context output filename
      --verbose                debug logging
      --dry-run                no files written
      --continue-on-error      ignore summarization failures
  -h, --help                   show this message and exit
```

---

## Configuration Presets

You can ship YAML presets in a `presets/` folder and load them via:

```bash
gptcontext --config-file presets/<preset-name>.yml
```

Preset examples include:

| Preset         | Description                 |
| -------------- | --------------------------- |
| `default.yml`  | Default GPTContext settings |
| `python.yml`   | Pure Python project         |
| `frontend.yml` | Frontend (JS/React) focus   |
| `backend.yml`  | Backend (API/server) focus  |
| ...            | ...                         |

---

## Development & Testing

Clone the repo and install dev extras:

```bash
git clone https://github.com/youruser/gptcontext.git
cd gptcontext
pip install .[dev]
```

Run the test suite with **pytest**:

```bash
pytest -q
```

Lint & type-check with **ruff** and **mypy**:

```bash
ruff .
mypy src/gptcontext
```

---

## Contributing

1. Fork the repo and create a feature branch.
2. Write tests for your changes.
3. Follow existing code style and add type hints.
4. Submit a pull request describing your change.

---

## License

This project is licensed under the **MIT License**. See [LICENSE](LICENSE) for details.
