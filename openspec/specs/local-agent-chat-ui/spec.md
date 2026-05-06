# local-agent-chat-ui Specification

## Purpose

Define the fully local frontend experience for chatting with the ECS LangGraph agent.

## Requirements

### Requirement: Local Agent Chat UI

The system SHALL provide a local LangChain Agent Chat UI frontend for interacting with the ECS agent.

#### Scenario: Start frontend

- GIVEN dependencies are installed in `agent-chat-ui`
- WHEN the user runs `pnpm dev` from `agent-chat-ui`
- THEN the frontend SHALL start at `http://localhost:3000`.

#### Scenario: Default local connection

- GIVEN the frontend opens in a browser
- WHEN it initializes connection settings
- THEN it SHALL default to Deployment URL `http://localhost:2024`
- AND Assistant / Graph ID `ecs_agent`
- AND no LangSmith API key for local development.

### Requirement: Local-only frontend path

The frontend SHALL not depend on a remote Studio page for normal operation.

#### Scenario: Avoid remote Studio

- GIVEN the user interacts with the local Agent Chat UI
- WHEN they send a message
- THEN the browser SHALL call the local LangGraph API at `http://localhost:2024`
- AND SHALL NOT route normal chat through `smith.langchain.com`.

### Requirement: Credential separation

The frontend SHALL NOT read Volcengine AK/SK or Doubao API keys.

#### Scenario: Message from browser

- GIVEN a user submits an ECS question in the frontend
- WHEN the frontend calls the LangGraph API
- THEN credentials SHALL remain in the local backend process environment
- AND only message payloads and LangGraph run metadata SHALL flow through the frontend.

### Requirement: Local build stability

The frontend SHALL build without fetching Google Fonts at build time.

#### Scenario: Production build

- GIVEN dependencies are installed
- WHEN `pnpm turbo build --filter=web` is run from `agent-chat-ui`
- THEN the web package SHALL build using local/system fonts
- AND SHALL NOT require `fonts.googleapis.com`.
