# Microsoft Agent Framework: Human-in-the-Loop Learning Lab

A beginner-friendly, notebook-first project for learning Microsoft Agent Framework (MAF) workflows and human-in-the-loop (HITL) patterns with Python.

The main lesson is deliberately **LLM-free**: it pauses a workflow for human review, exposes the pending request, and resumes from the exact pause point. An optional example demonstrates approval-gated agent tools with an OpenAI model.

> Verified against Microsoft Agent Framework Python **1.19.0** and Microsoft documentation available on 2026-09-30.

## What you will learn

- How agents differ from deterministic workflows.
- How `@workflow` and `@step` compose a functional workflow.
- How `RunContext.request_info()` pauses for human input.
- How to inspect pending requests and resume with `responses`.
- Why checkpointed steps matter around expensive work or side effects.
- How `@tool(approval_mode="always_require")` creates an approval boundary.

## Repository map

```text
maf-hitl-learning/
├── notebooks/01_maf_human_in_the_loop.ipynb
├── examples/hitl_review.py
├── examples/agent_tool_approval.py
├── .env.example
├── requirements.txt
└── pyproject.toml
```

## Quick start

Requires Python 3.10 or newer.

```bash
git clone https://github.com/vinudurai02/maf-hitl-learning.git
cd maf-hitl-learning
python -m venv .venv
source .venv/bin/activate        # Windows: .venv\Scripts\activate
python -m pip install --upgrade pip
python -m pip install -r requirements.txt
jupyter lab
```

Open `notebooks/01_maf_human_in_the_loop.ipynb` and run it from top to bottom.

The main script requires no model or API key:

```bash
python examples/hitl_review.py
```

## Optional agent tool-approval example

```bash
python -m pip install -e '.[openai]'
cp .env.example .env
python examples/agent_tool_approval.py
```

Set `OPENAI_API_KEY` and `OPENAI_CHAT_MODEL` in `.env` first. The example displays the exact proposed tool call before asking for approval. Rejecting it prevents the tool from running.

## Mental model

```text
input → checkpointed work → request_info(...) → PAUSED
                                               ↓
                                  human inspects request
                                               ↓
                         run(responses={request_id: decision})
                                               ↓
                               resume → final output
```

`request_info()` does not call `input()` itself. It emits a request event and returns control to the host. A notebook, CLI, web API, worker, or approval dashboard can act as that host.

## Production checklist

- Authenticate the reviewer and authorize the specific action.
- Show the exact tool, arguments, destination, and expected impact.
- Treat approvals as single-use and make side effects idempotent.
- Persist checkpoints and approval records for long-running work.
- Add expiry, cancellation, escalation, and a safe timeout default.
- Revalidate approved inputs immediately before execution.
- Keep secrets and sensitive data out of prompts, logs, and approval screens.

## Sources

- [Microsoft Agent Framework](https://github.com/microsoft/agent-framework)
- [Human-in-the-loop workflows](https://learn.microsoft.com/en-us/agent-framework/workflows/human-in-the-loop)
- [Workflow checkpoints](https://learn.microsoft.com/en-us/agent-framework/workflows/checkpoints)
- [Function-tool approvals](https://learn.microsoft.com/en-us/agent-framework/agents/tools/tool-approval)
- [Official functional HITL sample](https://github.com/microsoft/agent-framework/blob/main/python/samples/03-workflows/functional/hitl_review.py)
- [Learning-style reference notebook](https://github.com/Thirumurugan240/AutoGen_Framework/blob/main/15_Human_in_the_Loop.ipynb)

## License

MIT. This is an independent learning project, not an official Microsoft sample.
