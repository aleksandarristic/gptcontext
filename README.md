# GPTContext

**GPTContext** is a CLI tool that builds a context file from your codebase for use with LLMs like ChatGPT. It scans source files, optionally summarizes large files using OpenAI, and writes a token-bounded context to a single file.

---

## Features

- Recursively scans project directories  
- Honors `.gitignore` and `context_config.json`  
- Supports configurable include/exclude rules  
- Optionally summarizes large files via OpenAI API  
- Caches summaries for efficiency  
- Limits output to a maximum total token count  

---

## Requirements

- Python 3.7+
- `openai`, `tiktoken`, `pathspec`

---

## Installation and Usage

### 1. Clone the repository

```bash
git clone https://github.com/aleksandarristic/gptcontext.git
cd gptcontext
```

### 2. Set up virtual environment and install dependencies

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

### 3. Set up a shell alias (optional)

Edit your `~/.zshrc` or `~/.bashrc`:

```bash
# Set the path to where you cloned the repo
CONTEXT_DIR="$HOME/Code/gptcontext"  # adjust if needed

# Define the alias
alias gptcontext="$CONTEXT_DIR/.venv/bin/python $CONTEXT_DIR/build_context.py --base . --output context.txt"
```

Then reload your shell:

```bash
source ~/.zshrc  # or ~/.bashrc
```

---

## CLI Usage

### Run with defaults

```bash
python build_context.py
```

This will:
- Scan the current directory
- Use default config from constants (or `context_config.json` if present)
- Write `context.txt`

### Summarize large files

```bash
python build_context.py --summarize
```

Files over 2000 tokens will be summarized using the OpenAI API (set your API key via `OPENAI_API_KEY`).

### Other options

- Set max total tokens:

  ```bash
  python build_context.py --max-tokens 8000
  ```

- Change output file:

  ```bash
  python build_context.py --output alt_context.txt
  ```

- Use a different base directory:

  ```bash
  python build_context.py --base ../myproject
  ```

- Generate a message template for ChatGPT:

  ```bash
  python build_context.py --generate-message
  ```

---

## Configuration

By default, file types and excluded directories are defined in code (`DEFAULT_CONFIG_INCLUDE_EXTS`, `DEFAULT_CONFIG_EXCLUDE_DIRS`).

To override, place a `context_config.json` file in your project root with:

```json
{
  "include_extensions": [".py", ".md", ".json"],
  "exclude_dirs": [".git", "node_modules", "__pycache__"]
}
```

---

## OpenAI API Key

If using summarization, set your key via:

```bash
export OPENAI_API_KEY=sk-...
```

---

## Output Example

The generated `context.txt` contains:

```
# app/main.py
<source code>

# Summary of app/large_module.py
<LLM-generated summary>
```

---

## Message Template

To generate a ChatGPT-ready message, use:

```bash
python build_context.py --generate-message
```

It reads from `message_sample.txt` and outputs a filled message to `gptcontext_message.txt`.

Example structure:

```
You are helping me with this codebase.

Below is a sample of files from the project. Use this as your working context.

<context starts>

<paste contents of context.txt here>

<context ends>

Now, ...
```

---

## License

MIT License
