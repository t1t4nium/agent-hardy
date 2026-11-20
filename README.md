# Hardy agent

A small tool-calling agent that talks to a local LLM. Give it a prompt, it picks a tool, reads the result, and answers.

## Requirements

- Python 3
- A local LLM server with an OpenAI-compatible API

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
python agent.py "prompt"
```
