# configuration Delta

## ADDED Requirements

### Requirement: YAML-driven runtime configuration

The system SHALL load model, MCP server, and agent behavior from a YAML configuration file.

### Requirement: Secret isolation

The system SHALL keep cloud and model credentials out of committed source files.

### Requirement: Local config exclusion

The repository SHALL ignore local config and runtime state that may contain account-specific values.

### Requirement: Runtime versions

The project SHALL target current Python and allow Rust-backed dependency builds.
