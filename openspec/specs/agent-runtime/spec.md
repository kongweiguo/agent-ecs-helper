# agent-runtime Specification

## Purpose

Define how the ECS management agent is constructed, invoked, and exposed through CLI, LangGraph, SDK, and tool-calling workflows.

## Requirements

### Requirement: LangGraph ECS agent construction

The system SHALL construct an ECS management agent with LangGraph using a Doubao-compatible chat model and ECS MCP tools.

#### Scenario: Build graph for LangGraph Agent Server

- GIVEN `ECS_AGENT_CONFIG` points to a valid YAML config
- WHEN `langgraph dev` loads `ecs_agent`
- THEN the system SHALL call `src/agent_ecs_helper/graph.py:make_graph`
- AND create a LangGraph ReAct agent
- AND attach tools discovered from the configured ECS MCP server
- AND use the configured system prompt.

#### Scenario: Build agent for CLI

- GIVEN a user runs `uv run ecs-agent --config <config> "<question>"`
- WHEN the CLI receives the question
- THEN the system SHALL load the config
- AND build the same model and MCP tool set
- AND return the final assistant message.

### Requirement: ECS MCP tool usage

The agent SHALL manage ECS resources only through configured ECS MCP tools.

#### Scenario: Query ECS resources

- GIVEN the user asks for ECS instances, regions, zones, images, or system events
- WHEN the agent decides a tool call is needed
- THEN it SHALL invoke an ECS MCP tool
- AND summarize the returned data with key IDs preserved.

#### Scenario: Missing required operation parameters

- GIVEN a requested ECS operation lacks required parameters such as region, instance ID, image ID, or renewal period
- WHEN the agent evaluates the request
- THEN it SHALL ask the user for the missing parameters before calling a tool.

### Requirement: Risk confirmation

The agent SHALL require explicit user confirmation before performing state-changing or cost-impacting ECS operations.

#### Scenario: Start or renew instance

- GIVEN the user asks to start, renew, or otherwise mutate an ECS resource
- WHEN the operation can change cloud state or incur cost
- THEN the agent SHALL restate the target resource, region, and expected impact
- AND wait for explicit user confirmation before invoking the MCP tool.

### Requirement: SDK access

The system SHALL expose the same agent through the LangGraph SDK when the Agent Server is running.

#### Scenario: SDK run

- GIVEN `uv run langgraph dev` is serving `http://localhost:2024`
- WHEN `examples/langgraph_sdk_ecs_mcp.py` creates a thread and runs `ecs_agent`
- THEN the request SHALL be handled by the same LangGraph graph as the local frontend.
