"""Lesson 4: a deterministic functional workflow that needs no model."""

import asyncio

from agent_framework import step, workflow


@step
async def collect_facts(topic: str) -> list[str]:
    print("1. Collecting facts")
    return [
        f"{topic} combines model reasoning with application code.",
        "Workflows make control flow explicit and observable.",
    ]


@step
async def write_summary(facts: list[str]) -> str:
    print("2. Writing summary")
    return " ".join(facts)


@workflow
async def learning_pipeline(topic: str) -> str:
    facts = await collect_facts(topic)
    return await write_summary(facts)


async def main() -> None:
    instance = learning_pipeline.build()
    result = await instance.run("Microsoft Agent Framework")
    print("\nResult:")
    print(result.get_outputs()[0])


if __name__ == "__main__":
    asyncio.run(main())
