#!/usr/bin/env python3
"""Command-line entry point: build the prompt, wire up tools, run one request."""

import argparse
import tools # Importing this registers every tool declared in tools/__init__.py.
from agent import config # Importing this loads the .env file into os.environ.
from agent.agent import Agent

system_prompt = """You are a technical operator agent.
Use the available tools when needed, then answer the user's request.
"""

def main():
    parser = argparse.ArgumentParser(description="Chat with agent")
    parser.add_argument("prompt", help="Prompt to send")
    args = parser.parse_args()

    agent = Agent(system_prompt=system_prompt, reasoning_effort="none")
    try:
        reply = agent.run(args.prompt)
    except Exception as e:
        reply = {"message": f"Error: {str(e)}"}
    print(reply["message"])

if __name__ == "__main__":
    main()
