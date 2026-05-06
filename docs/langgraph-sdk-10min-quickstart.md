# LangGraph 10 分钟从 0 到 1

这份文档用 10 分钟建立 LangGraph 的基本心智模型：什么是 graph、state、node、edge、agent、thread、run，以及如何通过本地 Agent Server 和 SDK 调用一个 agent。

示例使用当前项目的火山 ECS MCP agent。你不需要先掌握 ECS MCP 的所有细节，只要把它当成一个真实工具调用场景：用户问 ECS 问题，模型决定是否调用 ECS MCP 工具，LangGraph 负责组织执行过程。

## 1. LangGraph 解决什么问题

LangGraph 用来构建可控的 LLM 应用工作流。它不是只发一次模型请求，而是把“模型思考、工具调用、状态保存、条件分支、多轮对话”组织成一个图。

最常见的 agent 流程是：

```text
user message
  -> model
  -> tool call if needed
  -> tool result
  -> model
  -> final answer
```

LangGraph 把这个流程变成可运行、可调试、可通过 API 调用的 graph。

## 2. 五个核心概念

`state`

图运行时携带的数据。聊天 agent 最常见的 state 是 `messages`，也就是用户消息、模型消息、工具结果组成的列表。

`node`

图里的一个执行步骤。它可以是一次模型调用、一次工具执行、一次数据处理，或者你自己写的任意 Python 函数。

`edge`

节点之间的流转关系。普通 edge 表示固定下一步；conditional edge 表示根据当前 state 决定下一步。

`graph`

由 state、node、edge 组成的可执行工作流。当前项目的 graph 叫 `ecs_agent`。

`thread` 和 `run`

当 graph 通过 LangGraph Agent Server 暴露为 HTTP API 后，一次会话叫 thread，一次执行叫 run。多轮对话时，多个 run 可以挂在同一个 thread 下。

## 3. 最小 LangGraph 长什么样

一个最小图通常长这样：

```python
from typing import TypedDict

from langgraph.graph import END, StateGraph


class State(TypedDict):
    question: str
    answer: str


def answer(state: State) -> State:
    return {"question": state["question"], "answer": "hello from LangGraph"}


builder = StateGraph(State)
builder.add_node("answer", answer)
builder.set_entry_point("answer")
builder.add_edge("answer", END)

graph = builder.compile()
```

这个例子没有模型、没有工具，只展示 LangGraph 的骨架：

1. 定义 state。
2. 定义 node。
3. 用 edge 连接 node。
4. `compile()` 得到可执行 graph。

## 4. Agent 是怎么来的

真实 agent 通常不手写完整循环，而是用 LangGraph 预置的 ReAct agent：

```python
from langgraph.prebuilt import create_react_agent

graph = create_react_agent(
    model,
    tools,
    prompt="你是一个运维助手。",
)
```

ReAct agent 会自动处理这类循环：

```text
messages
  -> call model
  -> model decides final answer or tool call
  -> run tool
  -> append tool result to messages
  -> call model again
```

当前项目就是这种模式，只是工具来自火山 ECS MCP Server，模型使用火山豆包。

## 5. 当前 ECS agent 的 graph 在哪里

LangGraph Agent Server 通过 `langgraph.json` 找到 graph：

```json
{
  "graphs": {
    "ecs_agent": "./src/agent_ecs_helper/graph.py:make_graph"
  }
}
```

对应实现是：

```python
async def make_graph():
    config = load_config(Path("configs/volcengine-ecs-agent.yaml"))
    mcp_client = MultiServerMCPClient(config.mcp_client_config())
    tools = await mcp_client.get_tools()
    model = build_model(config)
    return create_react_agent(model, tools, prompt=config.agent.system_prompt)
```

这段代码做了四件事：

1. 读取默认配置 `configs/volcengine-ecs-agent.yaml`。
2. 根据配置启动并连接 ECS MCP Server。
3. 创建豆包 chat model。
4. 用 `create_react_agent` 生成 LangGraph agent。

## 6. 准备环境变量

配置文件不包含真实密钥。真实 AK/SK 和豆包 API Key 仍然通过环境变量提供：

```bash
export VOLCENGINE_ACCESS_KEY="your-volcengine-ak"
export VOLCENGINE_SECRET_KEY="your-volcengine-sk"
export VOLCENGINE_REGION="cn-beijing"
export VOLCENGINE_ENDPOINT="open.volcengineapi.com"
export ARK_API_KEY="your-doubao-api-key"
```

LangGraph 后端会固定读取 `configs/volcengine-ecs-agent.yaml`，不需要再设置额外的配置文件环境变量。

## 7. 启动本地 Agent Server

在仓库根目录运行：

```bash
uv sync
uv run langgraph dev
```

启动后你会得到一个本地 LangGraph API：

```text
http://localhost:2024
```

API 文档：

```text
http://localhost:2024/docs
```

`langgraph dev` 还可能自动打开 LangSmith Studio。没有配置 LangSmith 云端 tracing 时，Studio 里出现 `Not seeing LangSmith runs?` 可以忽略；本地 agent 仍然可以正常运行。

## 8. 用本地 Agent Chat UI 体验

另开一个终端：

```bash
cd agent-chat-ui
pnpm install
pnpm dev
```

打开：

```text
http://localhost:3000
```

默认连接：

- Deployment URL: `http://localhost:2024`
- Assistant / Graph ID: `ecs_agent`
- LangSmith API Key: 连接本地后端时留空

可以输入：

```text
列出 cn-beijing 下最近的 ECS 实例，最多返回 5 个。
```

本地链路是：

```text
Agent Chat UI
  -> LangGraph Agent Server
  -> ecs_agent graph
  -> Doubao model
  -> ECS MCP tools
  -> Volcengine ECS API
```

## 9. 用 SDK 调用同一个 graph

SDK 适合脚本、测试、服务间调用。先确保 `uv run langgraph dev` 正在运行，然后执行：

```bash
uv run python examples/langgraph_sdk_ecs_mcp.py
```

示例核心代码：

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

这段 SDK 调用对应三个动作：

1. 连接本地 Agent Server。
2. 创建一个 thread。
3. 在这个 thread 上运行 `ecs_agent` 并等待结果。

## 10. SDK 背后就是 HTTP API

SDK 只是 LangGraph HTTP API 的封装。你也可以打开：

```text
http://127.0.0.1:2024/docs
```

典型 API 语义是：

```text
POST /threads
POST /threads/{thread_id}/runs/wait
```

所以三种入口本质上都在调用同一个 graph：

```text
CLI
Agent Chat UI
SDK / HTTP API
  -> ecs_agent
```

区别只是入口不同：

- CLI：适合一次性命令行查询。
- Agent Chat UI：适合人工交互和观察工具调用。
- SDK：适合集成到脚本、测试和其他服务。

## 11. 继续学习时看什么

从当前项目继续深入，可以按这个顺序读：

1. `langgraph.json`：Agent Server 如何发现 graph。
2. `src/agent_ecs_helper/graph.py`：graph 如何被构建。
3. `src/agent_ecs_helper/agent.py`：模型和 agent 调用逻辑。
4. `configs/volcengine-ecs-agent.yaml`：模型、MCP Server、system prompt 如何配置。
5. `examples/langgraph_sdk_ecs_mcp.py`：SDK 如何调用本地 graph。

学会这条链路后，你已经具备了从 0 到 1 搭一个 LangGraph agent 的核心能力：定义 graph，把它暴露成 Agent Server，再通过 UI 或 SDK 调用它。
