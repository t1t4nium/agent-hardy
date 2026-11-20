"""Minimal HTTP client for an OpenAI-compatible local LLM server."""

import json
import os
import urllib.request

# Fallbacks used only when the variable is not set in the environment or .env.
LLM_API_URL = "http://127.0.0.1:8080/v1"
LLM_API_KEY = ""
LLM_API_MODEL = "/etc/llama/models/qwen3.8-27b-q3.gguf"


def chat(messages, api_url=None, api_key=None, model=None, reasoning="none", temperature=0.1, max_tokens=512, timeout=180):
    """Send a chat request and return the assistant's text reply."""
    # Environment and .env values win over the module defaults above.
    api_url = (api_url or os.environ.get("LLM_API_URL", LLM_API_URL)).rstrip("/")
    api_key = api_key or os.environ.get("LLM_API_KEY", LLM_API_KEY)
    model = model or os.environ.get("LLM_API_MODEL", LLM_API_MODEL)

    headers = {"Content-Type": "application/json", "Authorization": f"Bearer {api_key}"}
    url = f"{api_url}/chat/completions"
    data = json.dumps({
        "model": model,
        "messages": messages,
        "stream": False,
        # Non-standard field, silently ignored by llama.cpp. Drop it if another
        # server rejects it.
        "reasoning": {"effort": reasoning},
        "temperature": temperature,
        "max_tokens": max_tokens,
    }).encode("utf-8")

    req = urllib.request.Request(url, data=data, headers=headers)
    with urllib.request.urlopen(req, timeout=timeout) as resp:
        result = json.loads(resp.read().decode("utf-8"))
    return result["choices"][0]["message"]["content"]
