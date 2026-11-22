# Hardy agent

A small tool-calling agent that talks to any OpenAI-compatible LLM. Tool calling uses the standard OpenAI tools API.

## Requirements

- Python 3
- An OpenAI-compatible LLM server
- A model that supports tool calling

## Install

```bash
pip install -r requirements.txt
```

## Configure

Create a file named `.env` at the root of the repository, or export these as environment variables:

| Variable | Default | What it does |
| --- | --- | --- |
| `LLM_API_URL` | `http://127.0.0.1:8080/v1` | LLM server URL |
| `LLM_API_KEY` | *(empty)* | API key. Leave empty for a local server. |
| `LLM_API_MODEL` | *(see `agent/llm.py`)* | Model name |

Example `.env`:

```
LLM_API_URL=http://127.0.0.1:8080/v1
LLM_API_MODEL=model-name
```

## Usage

```bash
python agent.py "Show me the hostname and the date."
```

The agent calls tools as needed, then answers:

```
The hostname is ... and the date is ...
```

## Adding a tool

Create a module in `tools/` and import it in `tools/__init__.py` so it registers.

Without parameters:

```python
# tools/hostname.py
from agent.tools import tool

@tool
def hostname():
    """Return the machine hostname."""
    import socket
    return socket.gethostname()
```

With parameters, pass a JSON Schema:

```python
# tools/files.py
from agent.tools import tool

@tool(schema={
    "type": "object",
    "properties": {
        "path": {"type": "string", "description": "Absolute path of the file to read."}
    },
    "required": ["path"]
})
def read_file(path):
    """Read a text file."""
    with open(path) as f:
        return f.read()
```

Then register both modules:

```python
# tools/__init__.py
from . import system
from . import hostname
from . import files
```

The first docstring line becomes the tool description. The model sends arguments as JSON, and the function receives them as keyword arguments. The return value is converted to a string.
