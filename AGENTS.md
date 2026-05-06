# Agent Instructions

This repository uses OpenSpec for spec-driven development.

Before changing behavior:

1. Read the relevant files under `openspec/specs/`.
2. Create or update an OpenSpec change under `openspec/changes/<change-id>/` when the work changes behavior or architecture.
3. Keep `proposal.md`, `design.md`, `tasks.md`, and spec deltas aligned with the implementation.
4. After implementation and verification, archive the change and update durable specs under `openspec/specs/`.

Current core specs:

- `openspec/specs/agent-runtime/spec.md`
- `openspec/specs/configuration/spec.md`
- `openspec/specs/local-agent-chat-ui/spec.md`
- `openspec/specs/developer-workflow/spec.md`

Never commit real Volcengine AK/SK, Doubao API keys, local config, `.env`, `.venv`, `.langgraph_api`, `node_modules`, or build cache directories.
