# developer-workflow Specification

## Purpose

Define how developers install, run, test, document, version, and publish the project.

## Requirements

### Requirement: Environment preparation workflow

The repository SHALL document environment preparation in one place, including toolchains, dependencies, OpenSpec CLI, local config, and secret environment variables.

#### Scenario: Install backend dependencies

- GIVEN Python, Rust, and uv are installed
- WHEN the user runs `uv sync`
- THEN Python dependencies SHALL be installed for CLI, LangGraph Agent Server, and SDK examples.

#### Scenario: Install frontend dependencies

- GIVEN Node and pnpm are installed
- WHEN the user runs `pnpm install` in `agent-chat-ui`
- THEN frontend dependencies SHALL be installed for the local Agent Chat UI.
- AND the frontend SHALL use its own `package.json`, `pnpm-lock.yaml`, and `node_modules/` rather than reusing backend dependencies from the repository root.

#### Scenario: Install OpenSpec CLI

- GIVEN Node and pnpm are installed
- WHEN the user runs `pnpm add -g @fission-ai/openspec@latest`
- THEN `openspec --version` SHALL report an installed CLI version.

#### Scenario: Prepare ECS and model config

- GIVEN the developer prepares the local environment
- WHEN they use the committed `configs/volcengine-ecs-agent.yaml`
- THEN the README SHALL document required environment variables for Volcengine ECS MCP and Doubao model access in the same environment preparation section.

### Requirement: Clean repository workflow

The repository SHALL keep reproducible source files and specifications while excluding generated runtime, dependency, and build directories.

#### Scenario: Clean generated folders

- GIVEN dependencies or local servers have been run
- WHEN the project is cleaned
- THEN `.venv/`, `.uv-cache/`, `.pnpm-store/`, `.langgraph_api/`, `node_modules/`, `.turbo/`, `.next/`, and `__pycache__/` folders SHALL be removable without losing source state.
- AND `configs/volcengine-ecs-agent.yaml` SHALL remain as source state.

### Requirement: Local development runtime workflow

The repository SHALL document local development as a paired LangGraph backend and Agent Chat UI frontend workflow.

#### Scenario: Run local development stack

- GIVEN backend and frontend dependencies are installed
- WHEN the developer starts local development
- THEN they SHALL run `uv run langgraph dev` from the repository root
- AND run `pnpm dev` from `agent-chat-ui`
- AND use `http://localhost:3000` as the local chat UI
- AND use `http://localhost:2024` as the local LangGraph API.
- AND the README SHALL explain that `langgraph dev` may open remote LangSmith Studio
- AND the README SHALL explain that LangSmith Studio tracing notices are not local ECS agent errors.

#### Scenario: Use alternate entrypoints

- GIVEN the developer needs scripting or SDK integration
- WHEN they do not need the local browser UI
- THEN the README SHALL document CLI single-run, CLI interactive, and LangGraph SDK example commands separately from the local development stack.

### Requirement: Local logging and debug workflow

The repository SHALL document how developers inspect user messages, runs, tool calls, and local server logs during development.

#### Scenario: Inspect local execution details

- GIVEN the local LangGraph backend and Agent Chat UI are running
- WHEN a user sends a message
- THEN the README SHALL explain that the browser UI shows messages and tool-call context
- AND the LangGraph API docs at `http://localhost:2024/docs` expose thread and run APIs
- AND backend terminal logs can be adjusted with `--server-log-level`.

#### Scenario: Reduce hot reload noise

- GIVEN `langgraph dev` prints `watchfiles` changes detected messages
- WHEN the developer wants quieter logs
- THEN the README SHALL document `--no-reload`
- AND document `--server-log-level warning`.

### Requirement: Verification workflow

The repository SHALL provide commands to verify Python and frontend changes.

#### Scenario: Verify backend code

- GIVEN source files changed under `src` or `examples`
- WHEN `python3 -m compileall src examples` is run
- THEN Python syntax SHALL be checked.

#### Scenario: Verify frontend code

- GIVEN source files changed under `agent-chat-ui`
- WHEN `pnpm turbo build --filter=web` is run from `agent-chat-ui`
- THEN the local web UI SHALL type-check and build.

### Requirement: OpenSpec workflow

The repository SHALL use OpenSpec as the persistent source of truth for system capabilities and proposed changes.

#### Scenario: Start a new change

- GIVEN a developer wants to change behavior
- WHEN they begin work
- THEN they SHOULD create an OpenSpec change using `/opsx:new <change-id>`
- AND generate proposal, specs, design, and tasks before implementation.

#### Scenario: Archive completed change

- GIVEN a change is implemented and verified
- WHEN it is complete
- THEN it SHOULD be archived with `/opsx:archive`
- AND the durable specs under `openspec/specs/` SHOULD be updated.

### Requirement: GitHub publishing workflow

The repository SHALL document how to authenticate and push changes to GitHub.

#### Scenario: Push after authentication

- GIVEN GitHub authentication is configured with `gh auth login` or SSH
- WHEN `git push -u origin master` is run
- THEN committed changes SHALL be published to the remote repository.
