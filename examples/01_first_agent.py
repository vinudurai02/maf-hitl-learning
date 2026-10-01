"""Lesson 1: create and run your first Microsoft Agent Framework agent."""

import asyncio

from agent_framework import Agent
from agent_framework.foundry import FoundryChatClient
from azure.identity import AzureCliCredential
from dotenv import load_dotenv

load_dotenv()


async def main() -> None:
    client = FoundryChatClient(credential=AzureCliCredential())
    agent = Agent(
        client=client,
        name="LearningGuide",
        instructions="You are a friendly teacher. Explain ideas briefly and use one example.",
    )

    result = await agent.run("In simple words, what is an AI agent?")
    print(result.text)

    print("\nStreaming example:")
    async for chunk in agent.run("Give me one practical use for an agent.", stream=True):
        if chunk.text:
            print(chunk.text, end="", flush=True)
    print()


if __name__ == "__main__":
    asyncio.run(main())
