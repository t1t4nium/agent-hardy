import re
from . import llm


class Agent:
    """Tool-calling loop: ask the model, run the tool it names, repeat.

    The loop ends when the model answers with "ANSWER:" or when max_steps
    rounds pass without a final answer (in which case run() returns None).
    """

    def __init__(self, system_prompt, tools, max_steps=8, reasoning="none", temperature=0.1):
        self.system_prompt = system_prompt
        self.tools = tools            # {tool_name: callable}
        self.max_steps = max_steps
        self.reasoning = reasoning
        self.temperature = temperature
        self.trace = []               # step-by-step log for debugging

    def _find_tool(self, text):
        """Return the first registered tool whose name appears in text."""
        for name in self.tools:
            if re.search(rf"\b{name}\b", text):
                return name
        return None

    def run(self, user_prompt):
        """Run one request end to end and return the model's final answer."""
        messages = [
            {"role": "system", "content": self.system_prompt},
            {"role": "user", "content": user_prompt},
        ]
        for _ in range(self.max_steps):
            reply = llm.chat(messages, reasoning=self.reasoning, temperature=self.temperature)
            self.trace.append(("assistant", reply))
            messages.append({"role": "assistant", "content": reply})

            # The model signals it is done by prefixing its answer with "ANSWER:".
            if re.search(r"\bANSWER\s*:", reply):
                return reply

            tool_name = self._find_tool(reply)
            if tool_name is None:
                # No tool was named: nudge the model and try again.
                message = "Name exactly ONE tool from: " + ", ".join(self.tools) + "."
                self.trace.append(("system", message))
                messages.append({"role": "user", "content": message})
                continue

            # Run the tool and feed its output back to the model.
            result = self.tools[tool_name]()
            self.trace.append(("tool", f"{tool_name} -> {result}"))
            messages.append({"role": "user", "content": f"Result of {tool_name}:\n{result}"})
        return None
