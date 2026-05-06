# ECS Agent Chat UI

This is the local LangChain Agent Chat UI for the Volcengine ECS LangGraph agent.

It is a Next.js frontend generated with `create-agent-chat-app`. It does not run
the ECS agent itself. It connects to the Python LangGraph Agent Server in the
repository root.

## Run

Terminal 1, start the Python LangGraph backend from the repository root:

```bash
export ECS_AGENT_CONFIG="configs/volcengine-ecs-agent.yaml"
uv run langgraph dev
```

Terminal 2, start this local frontend:

```bash
cd agent-chat-ui
pnpm dev
```

Open:

```text
http://localhost:3000
```

Expected connection values:

- Deployment URL: `http://localhost:2024`
- Assistant / Graph ID: `ecs_agent`
- LangSmith API Key: empty for local development

These values are already the frontend defaults. You only need `.env.local` if
you want to override them.

## Notes

The root `pnpm dev` script starts only the Next.js frontend. The Python
LangGraph backend is intentionally started from the repository root with
`uv run langgraph dev`, because the ECS agent is implemented in Python.
