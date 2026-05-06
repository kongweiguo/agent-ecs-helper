from __future__ import annotations

from pathlib import Path
from typing import Any

from langchain_mcp_adapters.client import MultiServerMCPClient
from langgraph.prebuilt import create_react_agent

from agent_ecs_helper.agent import build_model
from agent_ecs_helper.config import load_config


DEFAULT_CONFIG = Path("configs/volcengine-ecs-agent.yaml")


async def make_graph() -> Any:
    config = load_config(DEFAULT_CONFIG)
    mcp_client = MultiServerMCPClient(config.mcp_client_config())
    tools = await mcp_client.get_tools()
    model = build_model(config)
    return create_react_agent(model, tools, prompt=config.agent.system_prompt)
