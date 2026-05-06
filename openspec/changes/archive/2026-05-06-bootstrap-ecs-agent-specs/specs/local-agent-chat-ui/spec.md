# local-agent-chat-ui Delta

## ADDED Requirements

### Requirement: Local Agent Chat UI

The system SHALL provide a local LangChain Agent Chat UI frontend for interacting with the ECS agent.

### Requirement: Local-only frontend path

The frontend SHALL not depend on a remote Studio page for normal operation.

### Requirement: Credential separation

The frontend SHALL NOT read Volcengine AK/SK or Doubao API keys.

### Requirement: Local build stability

The frontend SHALL build without fetching Google Fonts at build time.
