# configuration Delta

## ADDED Requirements

### Requirement: YAML-driven runtime configuration

The system SHALL load model, MCP server, and agent behavior from a YAML configuration file.

The default `configs/volcengine-ecs-agent.yaml` file SHALL be committed because it contains only non-secret defaults and environment variable names.

### Requirement: Secret isolation

The system SHALL keep cloud and model credentials out of committed source files.

### Requirement: Local config exclusion

The repository SHALL ignore local secret and runtime state files while keeping the default runtime config in source control.

### Requirement: Runtime versions

The project SHALL target current Python and allow Rust-backed dependency builds.
