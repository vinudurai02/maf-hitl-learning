"""Optional model-backed MAF tool-approval example."""

import asyncio
import os
from typing import Annotated

from agent_framework import Agent, Message, tool
from agent_framework.openai import OpenAIChatClient
from dotenv import load_dotenv

load_dotenv()


@tool(approval_mode="always_require")
def schedule_deployment(
    environment: Annotated[str, "Target environment"],
    version: Annotated[str, "Release version"],
) -> str:
    """Schedule a deployment; this demo changes no real system."""
    return f"Deployment of {version} to {environment} has been scheduled."


async def main() -> None:
    agent = Agent(
        client=OpenAIChatClient(model=os.getenv("OPENAI_CHAT_MODEL", "gpt-4o-mini")),
        name="ReleaseAgent",
        instructions="When asked to deploy, call schedule_deployment with the supplied values.",
        tools=[schedule_deployment],
    )
    query = "Deploy version 2.0.0 to production."
    first_result = await agent.run(query)
    if not first_result.user_input_requests:
        print(first_result.text)
        return

    request = first_result.user_input_requests[0]
    if request.function_call is None:
        raise RuntimeError("Approval request has no function call.")

    print(f"Proposed tool: {request.function_call.name}")
    print(f"Arguments: {request.function_call.arguments}")
    approved = input("Approve? [y/N]: ").strip().lower() == "y"
    approval = Message(
        role="user",
        contents=[request.to_function_approval_response(approved)],
    )
    final_result = await agent.run(
        [query, Message(role="assistant", contents=[request]), approval]
    )
    print(final_result.text)


if __name__ == "__main__":
    asyncio.run(main())
