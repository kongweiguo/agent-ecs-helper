from __future__ import annotations

import asyncio
import os

from langgraph_sdk import get_client


LANGGRAPH_URL = os.getenv("LANGGRAPH_URL", "http://127.0.0.1:2024")
ASSISTANT_ID = os.getenv("LANGGRAPH_ASSISTANT_ID", "ecs_agent")


async def main() -> None:
    client = get_client(url=LANGGRAPH_URL)

    thread = await client.threads.create()
    print(f"thread_id={thread['thread_id']}")

    final_state = await client.runs.wait(
        thread["thread_id"],
        ASSISTANT_ID,
        input={
            "messages": [
                {
                    "role": "user",
                    "content": "列出 cn-beijing 下最近的 ECS 实例，最多返回 5 个，并说明实例 ID、名称和状态。",
                }
            ]
        },
    )

    messages = final_state.get("messages", [])
    if not messages:
        print("No messages returned.")
        return

    last_message = messages[-1]
    if isinstance(last_message, dict):
        print(last_message.get("content", last_message))
    else:
        print(last_message)


if __name__ == "__main__":
    asyncio.run(main())
