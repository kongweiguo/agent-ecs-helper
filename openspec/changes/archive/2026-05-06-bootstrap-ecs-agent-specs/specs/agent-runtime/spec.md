# agent-runtime Delta

## ADDED Requirements

### Requirement: LangGraph ECS agent construction

The system SHALL construct an ECS management agent with LangGraph using a Doubao-compatible chat model and ECS MCP tools.

### Requirement: ECS MCP tool usage

The agent SHALL manage ECS resources only through configured ECS MCP tools.

### Requirement: Risk confirmation

The agent SHALL require explicit user confirmation before performing state-changing or cost-impacting ECS operations.

### Requirement: SDK access

The system SHALL expose the same agent through the LangGraph SDK when the Agent Server is running.
