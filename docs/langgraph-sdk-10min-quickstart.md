# LangGraph SDK 10 分钟上手：火山 ECS MCP Agent

这份笔记只讲跑通当前项目需要的 LangGraph 概念和 SDK 用法。目标是：启动本地 LangGraph 后端，然后用 SDK 向 `ecs_agent` 发一句 ECS 查询请求。

## 0. 你正在运行什么

当前项目里有两种入口：

- `uv run ecs-agent ...`：普通 CLI，直接在当前进程里构建 LangGraph agent。
- `uv run langgraph dev`：LangGraph 官方本地后端，也叫 Agent Server。它读取 `langgraph.json`，加载 `ecs_agent` 图，并提供 HTTP API 和 SDK 访问能力。

如果你要用本地 Agent Chat UI 或 SDK，请使用第二种。

## 1. 三个核心概念

`graph`

LangGraph 里的可执行工作流。当前项目的图叫 `ecs_agent`，定义在：

```json
{
  "graphs": {
    "ecs_agent": "./src/agent_ecs_helper/graph.py:make_graph"
  }
}
```

`assistant`

Agent Server 会为注册的图创建 assistant。这里可以直接用 assistant id：`ecs_agent`。

`thread`

一次会话的容器。多轮对话时，消息和状态都挂在线程下面。SDK 调用前通常先创建 thread，再在这个 thread 上发 run。

## 2. 准备环境变量

```bash
export VOLCENGINE_ACCESS_KEY="your-volcengine-ak"
export VOLCENGINE_SECRET_KEY="your-volcengine-sk"
export VOLCENGINE_REGION="cn-beijing"
export VOLCENGINE_ENDPOINT="open.volcengineapi.com"
export ARK_API_KEY="your-doubao-api-key"
export ECS_AGENT_CONFIG="configs/volcengine-ecs-agent.yaml"
```

## 3. 启动 LangGraph 本地后端

```bash
uv sync
uv run langgraph dev
```

这个后端才是真正执行 agent 的地方。它会：

- 读取 `langgraph.json`
- 调用 `src/agent_ecs_helper/graph.py:make_graph`
- 通过配置启动 ECS MCP Server
- 用豆包模型决定何时调用 ECS MCP 工具
- 在本地暴露 LangGraph API，默认地址是 `http://127.0.0.1:2024`

## 4. 启动本地 Agent Chat UI

另开一个终端，启动本地前端：

```bash
cd agent-chat-ui
cp .env.example .env.local
pnpm dev
```

打开：

```text
http://localhost:3000
```

默认连接值：

- Deployment URL: `http://localhost:2024`
- Assistant / Graph ID: `ecs_agent`
- LangSmith API Key: 本地开发留空

Agent Chat UI 是本地 Next.js 前端。它不会读取火山 AK/SK 或豆包 API Key，只会调用本地 LangGraph API。

## 5. 用 SDK 调一次 ECS 查询

另开一个终端，执行：

```bash
uv run python examples/langgraph_sdk_ecs_mcp.py
```

示例代码的关键部分是：

```python
from langgraph_sdk import get_client

client = get_client(url="http://127.0.0.1:2024")
thread = await client.threads.create()

final_state = await client.runs.wait(
    thread["thread_id"],
    "ecs_agent",
    input={
        "messages": [
            {
                "role": "user",
                "content": "列出 cn-beijing 下最近的 ECS 实例，最多返回 5 个。",
            }
        ]
    },
)
```

这段代码做了四件事：

1. 连接本地 LangGraph Agent Server。
2. 创建一个新 thread。
3. 在这个 thread 上运行 `ecs_agent`。
4. 等待运行结束，并从最终 state 里读取消息。

## 6. 用 curl 理解 SDK 背后的 HTTP API

SDK 只是把 HTTP API 包了一层。你也可以直接看 API 文档：

```bash
open http://127.0.0.1:2024/docs
```

创建 thread 的语义接近：

```bash
curl -X POST http://127.0.0.1:2024/threads \
  -H 'Content-Type: application/json' \
  -d '{}'
```

执行 run 的语义接近：

```bash
curl -X POST http://127.0.0.1:2024/threads/<thread_id>/runs/wait \
  -H 'Content-Type: application/json' \
  -d '{
    "assistant_id": "ecs_agent",
    "input": {
      "messages": [
        {
          "role": "user",
          "content": "列出 cn-beijing 下最近的 ECS 实例"
        }
      ]
    }
  }'
```

实际字段以 `http://127.0.0.1:2024/docs` 中的接口说明为准。

## 7. ECS MCP 在哪里发生

SDK 和 Agent Chat UI 都不直接访问火山 ECS，也不直接读取 AK/SK。

实际链路是：

```text
Agent Chat UI or SDK
  -> LangGraph Agent Server at http://localhost:2024
  -> ecs_agent graph
  -> Doubao model
  -> ECS MCP tool call
  -> Volcengine ECS API
```

ECS MCP Server 的启动命令在 `configs/volcengine-ecs-agent.yaml` 中配置。AK/SK 通过环境变量传给本地 MCP 进程。

## 8. 日常开发建议

查询类请求可以直接在 Agent Chat UI 或 SDK 中执行，例如：

```text
列出 cn-beijing 下最近的 ECS 实例
查询 cn-beijing 下可用区信息
帮我检查是否有待处理的 ECS 系统事件
```

写操作要保持二次确认，例如启动实例、续费实例、更新事件状态。这个约束已经写进配置文件里的 system prompt。

## 9. 参考

- LangGraph 本地开发：`langgraph dev` 会启动轻量本地服务器，默认端口为 `2024`。
- Agent Chat UI：本地 Next.js 前端，可连接本地 Agent Server。
- LangGraph SDK：Python 包 `langgraph-sdk` 提供 `get_client` / `get_sync_client`，用于访问 assistants、threads、runs。
