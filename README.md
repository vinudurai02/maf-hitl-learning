# Microsoft Agent Framework Learning Lab

A beginner-friendly, notebook-first course for learning **Microsoft Agent Framework (MAF) with Python**. It starts with the mental model and your first agent, then adds tools, multi-turn sessions, workflows, multi-agent orchestration, and Human-in-the-Loop (HITL) safety patterns.

The teaching style follows the supplied AutoGen notebook: plain-language explanations, a real-life analogy, small runnable examples, and concise takeaways.

> API baseline: Microsoft Agent Framework Python **1.19.0**, verified against current Microsoft documentation and official samples on 2026-09-30.

## Learning path

| Module | Topic | Requires a model? |
|---|---|---|
| 0 | MAF overview, setup, and first agent | Yes |
| 1 | Function tools and safe tool design | Yes |
| 2 | Multi-turn conversations with sessions | Yes |
| 3 | Functional workflows and deterministic control | No for the basic workflow |
| 4 | Human-in-the-Loop review and tool approval | No for review; yes for agent approval |
| 5 | Multi-agent orchestration patterns | Yes |

Start with [the complete fundamentals notebook](notebooks/00_maf_learning_path.ipynb), then use [the focused HITL lab](notebooks/01_maf_human_in_the_loop.ipynb).

## Repository structure

```text
maf-hitl-learning/
├── notebooks/
│   ├── 00_maf_learning_path.ipynb
│   └── 01_maf_human_in_the_loop.ipynb
├── examples/
│   ├── 01_first_agent.py
│   ├── 02_tools_and_sessions.py
│   ├── 03_functional_workflow.py
│   ├── 04_sequential_agents.py
│   ├── hitl_review.py
│   └── agent_tool_approval.py
├── .env.example
├── requirements.txt
├── requirements-models.txt
├── pyproject.toml
└── LICENSE
```

## Setup

Python 3.10 or newer is required.

```bash
git clone https://github.com/vinudurai02/maf-hitl-learning.git
cd maf-hitl-learning
python -m venv .venv
source .venv/bin/activate        # Windows: .venv\Scripts\activate
python -m pip install --upgrade pip
python -m pip install -r requirements.txt
```

The model-free workflow and HITL lessons now work:

```bash
python examples/03_functional_workflow.py
python examples/hitl_review.py
```

### Configure a model provider

Install the provider dependencies:

```bash
python -m pip install -r requirements-models.txt
```

This course uses Microsoft Foundry in the main agent examples:

```bash
az login
cp .env.example .env
```

Fill in:

```dotenv
FOUNDRY_PROJECT_ENDPOINT=https://your-project.services.ai.azure.com
FOUNDRY_MODEL=gpt-4o
```

The optional tool-approval example also supports OpenAI through `OPENAI_API_KEY` and `OPENAI_CHAT_MODEL`.

## Core mental model

| Building block | Purpose |
|---|---|
| `Agent` | Combines a model client, instructions, tools, and behavior |
| `@tool` | Exposes a typed Python function to an agent |
| Session | Preserves conversation state across agent runs |
| `@workflow` | Defines deterministic multi-step control flow |
| `@step` | Checkpoints a completed functional-workflow step |
| Orchestration | Coordinates multiple specialized agents |
| HITL request | Pauses work for external information or judgment |
| Tool approval | Requires a person to approve a proposed tool call |

Use an agent when reasoning is useful. Use a workflow when order, branching, durability, or auditability matters. Combine them when you need both.

## Human-in-the-Loop safety

HITL is one course module—not the entire framework. MAF supports two important patterns:

1. **Free-form review:** a workflow calls `request_info()`, emits a request event, and resumes with `responses={request_id: value}`.
2. **Tool approval:** a tool marked `approval_mode="always_require"` produces an approval request before its function executes.

Production systems should authenticate reviewers, show exact arguments and impact, expire approvals, log decisions, revalidate inputs, and make side effects idempotent.

## Verified API sources

- [MAF get-started learning path](https://learn.microsoft.com/en-us/agent-framework/get-started/)
- [Official Python progressive samples](https://github.com/microsoft/agent-framework/tree/main/python/samples/01-get-started)
- [Workflow capabilities](https://learn.microsoft.com/en-us/agent-framework/workflows/)
- [Multi-agent orchestrations](https://learn.microsoft.com/en-us/agent-framework/workflows/orchestrations/)
- [Sequential orchestration](https://learn.microsoft.com/en-us/agent-framework/workflows/orchestrations/sequential)
- [Human-in-the-loop workflows](https://learn.microsoft.com/en-us/agent-framework/workflows/human-in-the-loop)
- [Function-tool approvals](https://learn.microsoft.com/en-us/agent-framework/agents/tools/tool-approval)
- [Reference learning notebook](https://github.com/Thirumurugan240/AutoGen_Framework/blob/main/15_Human_in_the_Loop.ipynb)

## License

MIT. This is an independent learning project, not an official Microsoft sample.
