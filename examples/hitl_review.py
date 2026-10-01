"""A model-free Microsoft Agent Framework HITL workflow."""

import asyncio

from agent_framework import RunContext, WorkflowRunState, step, workflow


@step
async def prepare_release_notes(version: str) -> str:
    """Represent expensive work that must not repeat after a pause."""
    print(f"Preparing release notes for {version} (this should print once).")
    return f"Release {version}: faster search, clearer errors, and security updates."


@step
async def publish_preview(draft: str, reviewer_note: str) -> str:
    """Represent work allowed only after human review."""
    return f"APPROVED PREVIEW\n{draft}\nReviewer note: {reviewer_note}"


@workflow
async def release_review(version: str, ctx: RunContext) -> str:
    draft = await prepare_release_notes(version)
    decision = await ctx.request_info(
        {
            "action": "publish_release_notes",
            "draft": draft,
            "question": "Approve this draft? Reply with a reviewer note.",
        },
        response_type=str,
        request_id="release_review",
    )
    return await publish_preview(draft, decision)


async def main() -> None:
    instance = release_review.build()
    first_run = await instance.run("2.0.0")
    assert first_run.get_final_state() == WorkflowRunState.IDLE_WITH_PENDING_REQUESTS

    request = first_run.get_request_info_events()[0]
    print("\nWorkflow paused.")
    print(f"Request id: {request.request_id}")
    print(f"Review payload: {request.data}")

    note = input("\nReviewer note (Enter for 'Looks good'): ").strip() or "Looks good"
    final_run = await instance.run(responses={request.request_id: note})
    print("\nWorkflow resumed.")
    print(final_run.get_outputs()[0])


if __name__ == "__main__":
    asyncio.run(main())
