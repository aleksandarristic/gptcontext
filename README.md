# GPTContext

**GPTContext** is a CLI tool that builds a context file from your codebase for use with LLMs like ChatGPT. It scans source files, optionally summarizes large files using OpenAI, and writes a token-bounded context to a single file.

---

## Features

- Recursively scans project directories  
- Honors `.gitignore` and skips common excluded folders  
- Includes only relevant file types (e.g. `.py`, `.md`, `.json`, etc.)  
- Optionally summarizes large files via OpenAI API  
- Caches summaries for speed and efficiency  
- Limits total output by token count  

---

## Requirements

- Python 3.7+
- `openai`, `tiktoken`, `pathspec`

---

## Usage

### 1. Run with defaults

```bash
python build_context.py
```

This will:

- Scan the current directory
- Include relevant files under token and size limits
- Write output to `context.txt`

### 2. With summarization (for large files)

```bash
python build_context.py --summarize
```

Large files (over 2000 tokens) will be summarized using the OpenAI API.

### 3. Customize options

- Set a maximum token count (default is 12000):

  ```bash
  python build_context.py --max-tokens 8000
  ```

- Change output filename:

  ```bash
  python build_context.py --output my_context.txt
  ```

- Use a different base directory:

  ```bash
  python build_context.py --base ../myproject
  ```

---

## Installation

Follow these steps to set up and use **GPTContext** locally:

### 1. Clone the repository

```bash
git clone https://github.com/aleksandarristic/gptcontext.git
cd gptcontext
```

### 2. Create a virtual environment and install dependencies

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

### 3. Set up a shell alias

Edit your `~/.zshrc` or `~/.bashrc` and add the following:

```bash
# Set the path to where you cloned the repo
CONTEXT_DIR="$HOME/Code/gptcontext"  # adjust as needed

# Define the alias
alias gptcontext="$CONTEXT_DIR/.venv/bin/python $CONTEXT_DIR/build_context.py --base . --output context.txt"
```

Then reload your shell:

```bash
source ~/.zshrc  # or ~/.bashrc
```

### 4. Generate context via CLI

In any project directory:

```bash
gptcontext
```

This will scan the current directory, summarize large files using OpenAI (if needed), and output `context.txt`.

Make sure to set your OpenAI API key beforehand:

```bash
export OPENAI_API_KEY=sk-...
```

---

## Output Example

The generated `context.txt` includes:

```
# app/main.py
<file contents>

# Summary of app/utils/large_file.py
<LLM-generated summary>
```

---

## Sample Message Template

A template is provided in `message_sample.txt` to help you send the context to ChatGPT.

### Example format:

```
You are helping me with this codebase.

Below is a sample of files from the project. Use this as your working context.

<context starts>

<paste contents of context.txt here>

<context ends>

Now, ...
```

This message gives ChatGPT the right framing to work with your source code context.


---

## License

MIT License
