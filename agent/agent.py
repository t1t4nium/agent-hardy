"""Agent loop: OpenAI-style tool calling."""

import json
from . import llm
from .tools import get_tool_schemas, call_tool

class Agent:
    def __init__(self, system_prompt, max_steps=8, temperature=0.1, reasoning_effort=None, max_completion_tokens=512, timeout=180):
        self.system_prompt = system_prompt
        self.max_steps = max_steps
        self.temperature = temperature
        self.reasoning_effort = reasoning_effort
        self.max_completion_tokens = max_completion_tokens
        self.timeout = timeout
        self.trace = []

    def run(self, user_prompt):
        """Run one request end to end and return message and trace as a dict."""
        messages = [{"role": "system", "content": self.system_prompt}, {"role": "user", "content": user_prompt}]
        tools = get_tool_schemas()
        cache = {}

        for _ in range(self.max_steps):
            reply = llm.chat(
                messages,
                tools=tools,
                temperature=self.temperature,
                reasoning_effort=self.reasoning_effort,
                max_completion_tokens=self.max_completion_tokens,
                timeout=self.timeout
            )
            message = reply["choices"][0]["message"]
            assistant = {"role": "assistant", "content": message.get("content")}

            if message.get("tool_calls"):
                assistant["tool_calls"] = message["tool_calls"]
            messages.append(assistant)
            self.trace.append(assistant)

            tool_calls = message.get("tool_calls") or []
            if not tool_calls:
                return {"message": message.get("content") or "", "trace": self.trace}
            for call in tool_calls:
                fn = call["function"]
                raw = fn.get("arguments") or "{}"
                try:
                    key = (fn["name"], json.dumps(json.loads(raw), sort_keys=True))
                except json.JSONDecodeError:
                    key = (fn["name"], raw)
                if key not in cache:
                    cache[key] = call_tool(fn["name"], raw)
                result = cache[key]
                messages.append({
                    "role": "tool",
                    "tool_call_id": call["id"],
                    "content": result
                })
                self.trace.append(("tool", fn["name"], result))

        return {"message": "Step cap reached.", "trace": self.trace}
