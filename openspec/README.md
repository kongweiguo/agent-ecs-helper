# OpenSpec

This directory captures the durable specification for the Volcengine ECS LangGraph agent.

## Structure

- `specs/`: Current source of truth for what the system does.
- `changes/`: Proposed or archived changes. Completed changes live under `changes/archive/`.

## Workflow

Use OpenSpec before changing behavior:

```bash
/opsx:new <change-id>
/opsx:ff
/opsx:apply
/opsx:archive
```

For CLI usage:

```bash
pnpm add -g @fission-ai/openspec@latest
openspec --version
openspec init
```

This repository already contains the initial specs, so avoid reinitializing unless you intentionally want to refresh OpenSpec assistant files.
