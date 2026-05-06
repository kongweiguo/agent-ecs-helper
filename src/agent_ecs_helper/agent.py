from __future__ import annotations

from typing import Any

from langchain_core.messages import AIMessage, BaseMessage, HumanMessage
from langchain_mcp_adapters.client import MultiServerMCPClient
from langchain_openai import ChatOpenAI
from langgraph.prebuilt import create_react_agent

from agent_ecs_helper.config import AppConfig, require_model_api_key


def build_model(config: AppConfig) -> ChatOpenAI:
    model_config = config.model
    return ChatOpenAI(
        model=model_config.name,
        api_key=require_model_api_key(model_config),
        base_url=model_config.base_url,
        temperature=model_config.temperature,
        timeout=model_config.timeout_seconds,
    )


async def build_agent(config: AppConfig) -> Any:
    mcp_client = MultiServerMCPClient(config.mcp_client_config())
    tools = await mcp_client.get_tools()
    model = build_model(config)
    return create_react_agent(model, tools, prompt=config.agent.system_prompt)


async def ask(config: AppConfig, question: str) -> str:
    agent = await build_agent(config)
    return await ask_agent(agent, config, [HumanMessage(content=question)])


async def ask_agent(agent: Any, config: AppConfig, messages: list[BaseMessage]) -> str:
    response = await agent.ainvoke(
        {"messages": messages},
        {"recursion_limit": config.agent.recursion_limit},
    )
    return _last_message_content(response)


def messages_from_api(items: list[dict[str, str]]) -> list[BaseMessage]:
    messages: list[BaseMessage] = []
    for item in items:
        role = item.get("role")
        content = item.get("content", "")
        if role == "assistant":
            messages.append(AIMessage(content=content))
        else:
            messages.append(HumanMessage(content=content))
    return messages


def _last_message_content(response: dict[str, Any]) -> str:
    messages = response.get("messages", [])
    if not messages:
        return ""
    content = messages[-1].content
    if isinstance(content, str):
        return content
    return str(content)
