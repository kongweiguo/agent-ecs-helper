# Project Context

## Purpose

Build a local-first AI operations assistant for Volcengine ECS hosts.

The assistant uses:

- LangGraph for agent orchestration.
- Volcengine ECS MCP Server for ECS operations.
- Doubao through the Volcengine Ark OpenAI-compatible endpoint for chat reasoning.
- LangChain Agent Chat UI as a local frontend.
- OpenSpec as the durable source of truth for behavior and development workflow.

## Runtime Architecture

```text
Agent Chat UI at http://localhost:3000
  -> LangGraph Agent Server at http://localhost:2024
  -> ecs_agent graph
  -> Doubao model
  -> ECS MCP tools
  -> Volcengine ECS API
```

CLI and SDK entrypoints reuse the same agent behavior.

## Constraints

- Do not commit real Volcengine AK/SK, Doubao API keys, `.env`, or local config.
- ECS mutations or cost-impacting operations require explicit confirmation.
- Frontend must remain local-first and must not rely on remote Studio for normal chat.
- Config is YAML-driven and environment-variable expanded.
- Keep README commands aligned with `openspec/specs/developer-workflow/spec.md`.

## Verification

Backend:

```bash
python3 -m compileall src examples
```

Frontend:

```bash
cd agent-chat-ui
pnpm turbo build --filter=web
cd ..
```
