"""Lesson 6: coordinate two agents in a sequential orchestration."""

import asyncio

from agent_framework import Agent, AgentResponse
from agent_framework.foundry import FoundryChatClient
from agent_framework.orchestrations import SequentialBuilder
from azure.identity import AzureCliCredential
from dotenv import load_dotenv

load_dotenv()


async def main() -> None:
    client = FoundryChatClient(credential=AzureCliCredential())

    writer = Agent(
        client=client,
        name="Writer",
        instructions="Write one clear paragraph for a beginner.",
    )
    reviewer = Agent(
        client=client,
        name="Reviewer",
        instructions="Review the previous answer and return an improved version.",
    )

    workflow = SequentialBuilder(
        participants=[writer, reviewer],
        chain_only_agent_responses=True,
    ).build()

    events = await workflow.run("Explain why agent tools need clear descriptions.")
    outputs = events.get_outputs()
    if outputs:
        final: AgentResponse = outputs[0]
        print(final.text)


if __name__ == "__main__":
    asyncio.run(main())
