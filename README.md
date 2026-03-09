# AI_Agent_LLM

An AI-powered coding agent framework that uses Google's Gemini API to execute natural language requests through a sandboxed execution environment.

## Overview

AI_Agent_LLM is an autonomous agent system that:
- Accepts natural language prompts from users
- Processes requests using Google's Gemini LLM
- Executes Python code, manages files, and lists directory contents
- Operates within a security-constrained sandbox directory
- Implements a multi-turn agentic loop for complex task handling

## Features

- **LLM-Powered Agent**: Leverages Google Gemini API for intelligent task planning and execution
- **Sandboxed Execution**: All file and code operations confined to a designated working directory
- **Multi-turn Conversations**: Agent maintains state across up to 20 iterations per request
- **File Operations**: Read, write, and list files programmatically
- **Python Execution**: Run Python scripts with 30-second timeout protection
- **Bundled Calculator**: Includes a standalone mathematical expression evaluator with proper operator precedence

## Project Structure

```
AI_Agent_LLM/
├── main.py                 # Main agent entry point
├── config.py               # System prompt and agent configuration
├── requirements.txt        # Python dependencies
├── pyproject.toml          # Project metadata
├── tests.py                # Integration tests
├── functions/              # Core agent capabilities
│   ├── get_files_info.py   # File operations and Gemini function routing
│   └── run_python.py       # Safe Python subprocess execution
└── calculator/             # Standalone calculator application (agent sandbox)
    ├── main.py             # Calculator entry point
    ├── tests.py            # Calculator unit tests
    └── pkg/
        ├── calculator.py   # Expression evaluator (shunting-yard algorithm)
        └── render.py       # Unicode box output formatting
```

## Requirements

- Python 3.10+
- Google Gemini API key

## Installation

1. Clone the repository:
   ```bash
   git clone <repo-url>
   cd AI_Agent_LLM
   ```

2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   # or with uv:
   uv sync
   ```

3. Create a `.env` file with your API key:
   ```
   GEMINI_API_KEY=your_api_key_here
   ```

## Usage

### Run the AI Agent

```bash
python main.py "your natural language prompt here"
```

Add `--verbose` to print detailed function call information:
```bash
python main.py --verbose "list all files in the project"
```

### Run the Calculator

```bash
python calculator/main.py "3 + 5"
python calculator/main.py "10 * 2 - 3 / 1"
```

### Run Tests

```bash
# Calculator unit tests
python -m unittest calculator.tests

# Integration tests
python tests.py
```

## How It Works

1. The user provides a natural language prompt.
2. The agent sends the prompt to the Gemini API with a set of available tools.
3. Gemini responds with either:
   - A final text answer (loop ends), or
   - One or more function calls to execute (e.g., read a file, run Python code).
4. The agent executes the function calls within the sandbox and feeds results back to Gemini.
5. This loop repeats up to 20 iterations until the task is complete.

## Available Agent Tools

| Function | Description |
|---|---|
| `get_files_info` | List directory contents with file sizes |
| `get_file_content` | Read file contents (10 KB limit) |
| `write_file` | Create or overwrite files |
| `run_python_file` | Execute a Python script safely |

## Security

- All file and execution operations are constrained to the `./calculator` working directory.
- Directory traversal is prevented via `os.path.commonpath()` validation.
- Python script execution is limited to a 30-second timeout.
- No arbitrary shell command execution is permitted.

## Dependencies

| Package | Purpose |
|---|---|
| `google-genai` | Google Gemini API client |
| `google-generativeai` | Legacy SDK compatibility |
| `python-dotenv` | `.env` file support |
