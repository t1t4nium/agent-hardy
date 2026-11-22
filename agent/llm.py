"""Minimal HTTP client for an OpenAI-compatible API."""

import json
import os
import urllib.request

# Fallbacks used only when the variable is not set in the environment or .env.
LLM_API_URL = "http://127.0.0.1:8080/v1"
LLM_API_KEY = ""
LLM_API_MODEL = "/etc/llama/models/qwen3.8-27b-q3.gguf"

def chat(messages, tools=None, api_url=None, api_key=None, model=None, reasoning_effort=None, temperature=0.1, max_completion_tokens=512, timeout=180):
    """Send a chat request and return the full result."""
    # Environment and .env values win over the module defaults above.
    api_url = (api_url or os.environ.get("LLM_API_URL", LLM_API_URL)).rstrip("/")
    api_key = api_key or os.environ.get("LLM_API_KEY", LLM_API_KEY)
    model = model or os.environ.get("LLM_API_MODEL", LLM_API_MODEL)

    payload = {
        "model": model,
        "messages": messages,
        "stream": False,
        "max_completion_tokens": max_completion_tokens
    }
    if temperature is not None:
        payload["temperature"] = temperature
    if reasoning_effort:
        payload["reasoning_effort"] = reasoning_effort
    if tools:
        payload["tools"] = tools
        payload["tool_choice"] = "auto"

    headers = {"Content-Type": "application/json", "Authorization": f"Bearer {api_key}"}
    url = f"{api_url}/chat/completions"
    data = json.dumps(payload).encode("utf-8")

    req = urllib.request.Request(url, data=data, headers=headers)
    with urllib.request.urlopen(req, timeout=timeout) as resp:
        result = json.loads(resp.read().decode("utf-8"))
    return result
