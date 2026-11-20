#!/usr/bin/env python3
"""Command-line entry point: build the prompt, wire up tools, run one request."""

import argparse
import tools  # Importing this registers every tool declared in tools/__init__.py.
from agent import config  # Importing this loads the .env file into os.environ.
from agent.agent import Agent
from agent.tools import get_tools, describe_tools

# System prompt that steers the model. The available tools are appended here so
# the model always sees the current set of registered tools.
system_prompt = """You are a technical operator agent.
Answer the user's request by following these RULES:
- Name exactly ONE tool at a time, using its exact name.
- When you are done, end with "ANSWER:" followed by your final answer.
"""
system_prompt += f"\nAvailable tools:\n{describe_tools()}"

def main():
    parser = argparse.ArgumentParser(description="Chat with agent")
    parser.add_argument("prompt", help="Prompt to send")
    args = parser.parse_args()
    user_prompt = args.prompt
    agent = Agent(system_prompt=system_prompt, tools=get_tools())
    try:
        reply = agent.run(user_prompt)
        if reply is None:
            reply = "Step cap reached."
    except Exception as e:
        reply = f"Error:\n{e}"
    print(reply)

if __name__ == "__main__":
    main()
