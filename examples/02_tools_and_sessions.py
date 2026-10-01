"""Lessons 2 and 3: function tools and multi-turn sessions."""

import asyncio
from typing import Annotated

from agent_framework import Agent, tool
from agent_framework.foundry import FoundryChatClient
from azure.identity import AzureCliCredential
from dotenv import load_dotenv

load_dotenv()


@tool(approval_mode="never_require")
def course_progress(
    completed_modules: Annotated[int, "Number of completed course modules"],
) -> str:
    """Return simple course progress for a six-module course."""
    completed = max(0, min(completed_modules, 6))
    return f"{completed}/6 modules complete ({completed / 6:.0%})."


async def main() -> None:
    client = FoundryChatClient(credential=AzureCliCredential())
    agent = Agent(
        client=client,
        name="StudyCoach",
        instructions=(
            "You are a concise study coach. Use course_progress when the user "
            "mentions how many modules they completed."
        ),
        tools=[course_progress],
    )

    session = agent.create_session()

    first = await agent.run(
        "My name is Priya and I completed 2 modules. How am I doing?",
        session=session,
    )
    print(first.text)

    second = await agent.run(
        "What is my name and what should I study next?",
        session=session,
    )
    print(second.text)


if __name__ == "__main__":
    asyncio.run(main())
