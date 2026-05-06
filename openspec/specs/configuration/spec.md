# configuration Specification

## Purpose

Define configuration, secret handling, runtime versions, and dependency management for the ECS agent.

## Requirements

### Requirement: YAML-driven runtime configuration

The system SHALL load model, MCP server, and agent behavior from a YAML configuration file.

#### Scenario: Load local config

- GIVEN `configs/volcengine-ecs-agent.yaml` exists
- WHEN the agent starts
- THEN it SHALL load model, MCP server, and system prompt settings from that file.

#### Scenario: Expand environment variables

- GIVEN a config value uses `${NAME}` or `${NAME:-default}`
- WHEN the config is loaded
- THEN the system SHALL replace it with the matching environment variable
- AND use the default if provided
- AND fail if a required environment variable is missing.

### Requirement: Secret isolation

The system SHALL keep cloud and model credentials out of committed source files.

#### Scenario: Configure Volcengine credentials

- GIVEN ECS MCP requires Volcengine AK/SK
- WHEN the MCP process is configured
- THEN `VOLCENGINE_ACCESS_KEY` and `VOLCENGINE_SECRET_KEY` SHALL be read from environment variables
- AND real secret values SHALL NOT be committed.

#### Scenario: Configure Doubao credentials

- GIVEN the Doubao model requires an API key
- WHEN the chat model is constructed
- THEN the API key SHALL be read from the configured `api_key_env`
- AND the default key environment name SHALL be `ARK_API_KEY`.

### Requirement: Local config exclusion

The repository SHALL ignore local config and runtime state that may contain account-specific values.

#### Scenario: Ignore local runtime files

- GIVEN the user creates local config or LangGraph runtime state
- WHEN Git status is inspected
- THEN `configs/volcengine-ecs-agent.yaml`, `.env`, `.venv/`, `.uv-cache/`, `.pnpm-store/`, `.langgraph_api/`, Python cache files, frontend dependency folders, and frontend build caches SHALL be ignored.

### Requirement: Runtime versions

The project SHALL target current Python and allow Rust-backed dependency builds.

#### Scenario: Python and Rust setup

- GIVEN a developer prepares the project
- WHEN they install dependencies
- THEN Python 3.14.x SHALL be used
- AND Rust SHALL be available for dependencies with native extensions.
