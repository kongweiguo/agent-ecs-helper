from __future__ import annotations

import os
import re
from pathlib import Path
from typing import Any, Literal

import yaml
from pydantic import BaseModel, Field, field_validator


ENV_PATTERN = re.compile(r"\$\{([A-Za-z_][A-Za-z0-9_]*)(?::-(.*?))?\}")


class ModelConfig(BaseModel):
    provider: str = "volcengine-doubao"
    base_url: str = "https://ark.cn-beijing.volces.com/api/v3"
    name: str
    api_key_env: str = "ARK_API_KEY"
    temperature: float = 0
    timeout_seconds: int = 120

    @field_validator("temperature")
    @classmethod
    def validate_temperature(cls, value: float) -> float:
        if value < 0 or value > 2:
            raise ValueError("temperature must be between 0 and 2")
        return value


class MCPServerConfig(BaseModel):
    transport: Literal["stdio", "streamable_http", "http", "sse"] = "stdio"
    command: str | None = None
    args: list[str] = Field(default_factory=list)
    url: str | None = None
    headers: dict[str, str] = Field(default_factory=dict)
    env: dict[str, str] = Field(default_factory=dict)

    def to_client_config(self) -> dict[str, Any]:
        data: dict[str, Any] = {"transport": self.transport}
        if self.command:
            data["command"] = self.command
        if self.args:
            data["args"] = self.args
        if self.url:
            data["url"] = self.url
        if self.headers:
            data["headers"] = self.headers
        if self.env:
            data["env"] = self.env
        return data


class AgentConfig(BaseModel):
    recursion_limit: int = 20
    system_prompt: str


class AppConfig(BaseModel):
    model: ModelConfig
    mcp_servers: dict[str, MCPServerConfig]
    agent: AgentConfig

    def mcp_client_config(self) -> dict[str, dict[str, Any]]:
        return {name: server.to_client_config() for name, server in self.mcp_servers.items()}


def _expand_env(value: Any) -> Any:
    if isinstance(value, dict):
        return {key: _expand_env(item) for key, item in value.items()}
    if isinstance(value, list):
        return [_expand_env(item) for item in value]
    if not isinstance(value, str):
        return value

    def replace(match: re.Match[str]) -> str:
        name, default = match.group(1), match.group(2)
        env_value = os.getenv(name)
        if env_value is not None:
            return env_value
        if default is not None:
            return default
        raise ValueError(f"Environment variable {name} is required but not set")

    return ENV_PATTERN.sub(replace, value)


def load_config(path: str | Path) -> AppConfig:
    config_path = Path(path)
    with config_path.open("r", encoding="utf-8") as file:
        raw = yaml.safe_load(file) or {}
    expanded = _expand_env(raw)
    return AppConfig.model_validate(expanded)


def require_model_api_key(config: ModelConfig) -> str:
    api_key = os.getenv(config.api_key_env)
    if not api_key:
        raise ValueError(
            f"Environment variable {config.api_key_env} is required for Doubao model access"
        )
    return api_key
