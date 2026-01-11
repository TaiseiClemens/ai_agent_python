# AI Coding Agent

An AI-powered coding assistant that can autonomously interact with your filesystem using Google's Gemini API. This project demonstrates how to build an AI agent with function calling capabilities that can list files, read code, execute Python scripts, and write files within a sandboxed environment.

Built as part of the [Boot.dev](https://boot.dev) AI Agent course.

## Features

The AI agent provides four core capabilities through natural language interaction:

- **List Files**: Browse directories and view file information (size, type)
- **Read Files**: View file contents (up to 10,000 characters)
- **Execute Python Files**: Run Python scripts with optional command-line arguments
- **Write Files**: Create or modify files with automatic directory structure creation

All operations are restricted to a sandboxed working directory (`./calculator`) to ensure security.

## Architecture

The agent uses an agentic loop that:
1. Receives a user prompt
2. Sends the prompt to Gemini along with available function definitions
3. Processes function calls requested by the AI
4. Returns function results to the AI for further reasoning
5. Repeats until the AI provides a final response (max 20 iterations)

## Prerequisites

- Python 3.13 or higher
- Google Gemini API key

## Installation

1. Clone the repository:
```bash
git clone <repository-url>
cd ai_agent_python
```

2. Install dependencies using `uv` (or `pip`):
```bash
uv sync
```

Or with pip:
```bash
pip install google-genai==1.12.1 python-dotenv==1.1.0
```

3. Create a `.env` file in the project root:
```bash
GEMINI_API_KEY=your_api_key_here
```

Get your API key from [Google AI Studio](https://aistudio.google.com/apikey).

## Usage

Run the agent with a natural language prompt:

```bash
python main.py "your prompt here"
```

### Examples

List files in the calculator directory:
```bash
python main.py "What files are in the current directory?"
```

Read and explain code:
```bash
python main.py "Explain what the main.py file does"
```

Execute a Python script:
```bash
python main.py "Run the tests.py file"
```

Create or modify files:
```bash
python main.py "Create a new file called hello.py that prints Hello World"
```

### Verbose Mode

Enable verbose output to see token usage and function call details:
```bash
python main.py "your prompt here" --verbose
```

## Project Structure

```
ai_agent_python/
├── main.py                  # Entry point and agent loop
├── call_function.py         # Function dispatcher and tool definitions
├── prompts.py              # System prompt for the AI agent
├── constants.py            # Configuration constants
├── functions/              # Agent function implementations
│   ├── get_files_info.py   # List files in directory
│   ├── get_file_content.py # Read file contents
│   ├── run_python_file.py  # Execute Python scripts
│   └── write_file.py       # Write/create files
├── test_*.py               # Unit tests for each function
├── calculator/             # Sandboxed working directory
│   └── ...                 # Agent operates here
├── .env                    # API key configuration (not tracked)
├── pyproject.toml          # Project dependencies
└── README.md               # This file
```

## How It Works

### Function Calling Flow

1. **User Input**: You provide a natural language prompt
2. **AI Reasoning**: Gemini analyzes the prompt and determines which functions to call
3. **Function Execution**: The agent executes the requested functions with appropriate parameters
4. **Result Processing**: Function results are sent back to Gemini
5. **Iteration**: Steps 2-4 repeat until Gemini has enough information to respond
6. **Final Response**: The agent presents the final answer to the user

### Available Functions

Each function is defined with a schema that tells Gemini:
- Function name and description
- Required and optional parameters
- Parameter types and descriptions

The AI model uses this information to decide when and how to call each function.

### Security Features

- **Path Traversal Protection**: All file operations validate that paths stay within the working directory
- **Sandboxed Environment**: Agent operates only in `./calculator` directory
- **Execution Timeout**: Python scripts timeout after 30 seconds
- **File Size Limits**: File reads are capped at 10,000 characters
- **Iteration Limit**: Agent loop stops after 20 iterations to prevent infinite loops

## Testing

The project includes unit tests for each function:

```bash
uv run test_get_files_info.py
uv run test_get_file_content.py
uv run test_run_python_file.py
uv run test_write_file.py
```

## Configuration

You can modify these constants in `constants.py`:

- `MAX_CHARS`: Maximum characters to read from files (default: 10,000)
- `AGENT_ITERATION_LIMIT_COUNT`: Maximum agent loop iterations (default: 20)

## Limitations

- Agent operates only within the `./calculator` directory
- File reads are truncated at 10,000 characters
- Python execution timeout is 30 seconds
- Only Python files can be executed
- Maximum 20 iterations per agent run

## Example Session

```bash
$ python main.py "List the files, read main.py, and tell me what it does"

 - Calling function: get_files_info
 - Calling function: get_file_content
Final response:
The calculator directory contains a main.py file along with some text files
and a pkg subdirectory. The main.py file appears to be an entry point that
imports from the pkg.calculator and pkg.render modules...
```

## License

This project is part of the Boot.dev curriculum and is intended for educational purposes.

## Acknowledgments

- Built following the [Boot.dev](https://boot.dev) AI Agent course
- Uses [Google Gemini API](https://ai.google.dev/) for AI capabilities
- Powered by the `google-genai` Python SDK
