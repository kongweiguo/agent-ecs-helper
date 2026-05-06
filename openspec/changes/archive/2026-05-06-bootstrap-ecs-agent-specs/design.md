# Design

## Approach

Use OpenSpec as a lightweight documentation layer alongside code:

- Durable current behavior lives in `openspec/specs/<capability>/spec.md`.
- This bootstrap change is archived immediately because it describes the current implemented state rather than a future proposal.
- The specs are split by capability so future changes can target one area without rewriting a monolithic document.

## Capability Split

- `agent-runtime`: LangGraph construction, MCP tools, CLI, SDK, safety behavior.
- `configuration`: YAML config, environment expansion, secret handling, runtime versions.
- `local-agent-chat-ui`: local Next.js Agent Chat UI behavior and backend connection.
- `developer-workflow`: install, verify, OpenSpec, GitHub publishing commands.

## Non-Goals

- Do not introduce a custom OpenSpec schema.
- Do not make OpenSpec CLI a runtime dependency of the agent.
- Do not store real cloud credentials in OpenSpec artifacts.
