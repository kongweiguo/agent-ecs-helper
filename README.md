# Volcengine ECS LangGraph Agent

这个项目用 **OpenSpec 规格驱动开发** 的方式维护一个火山引擎 ECS 运维 Agent。Agent 基于 LangGraph 构建，通过火山引擎官方 ECS MCP Server 管理 ECS 主机，并使用火山豆包模型完成自然语言推理。

## OpenSpec First

任何行为、架构、运行模式的修改，都先看规格，再改代码。

当前长期规格在：

```text
openspec/specs/
```

核心规格：

- `openspec/specs/agent-runtime/spec.md`：LangGraph agent、CLI、SDK、MCP 工具调用和高风险操作确认。
- `openspec/specs/configuration/spec.md`：YAML 配置、环境变量、密钥隔离和运行时版本。
- `openspec/specs/local-agent-chat-ui/spec.md`：本地 Agent Chat UI 前端和本地 LangGraph 后端连接。
- `openspec/specs/developer-workflow/spec.md`：环境准备、验证、OpenSpec、GitHub 发布流程。

初始化规格变更记录已归档在：

```text
openspec/changes/archive/2026-05-06-bootstrap-ecs-agent-specs/
```

OpenSpec 常用流程：

```text
/opsx:new <change-id>
/opsx:ff
/opsx:apply
/opsx:archive
```

OpenSpec CLI 安装：

```bash
pnpm add -g @fission-ai/openspec@latest
openspec --version
```

本仓库已经包含 `openspec/`，不要为了日常开发重复执行 `openspec init`。只有在全新仓库初始化 OpenSpec 时才使用：

```bash
openspec init
```

## Project Layout

```text
.
├── openspec/                         # OpenSpec source of truth
├── src/agent_ecs_helper/             # Python LangGraph agent
├── configs/                          # Config templates
├── examples/                         # LangGraph SDK examples
├── docs/                             # Learning notes
├── agent-chat-ui/                    # Local LangChain Agent Chat UI
├── langgraph.json                    # LangGraph Agent Server graph registry
├── pyproject.toml                    # Python project metadata
└── uv.lock                           # Python dependency lockfile
```

Ignored local/generated paths include:

```text
.venv/
.uv-cache/
.pnpm-store/
.langgraph_api/
agent-chat-ui/node_modules/
agent-chat-ui/.turbo/
agent-chat-ui/apps/web/.next/
.env
```

## 环境准备

项目默认使用 Python 3.14.x，并允许 Rust 构建高性能 Python 扩展依赖。本节把工具链、依赖、OpenSpec CLI、本地配置和密钥环境变量集中准备好。

### 1. 安装工具链

安装 Rust：

```bash
curl --proto '=https' --tlsv1.2 -sSf https://sh.rustup.rs | sh
source "$HOME/.cargo/env"
rustup update stable
```

确认工具链：

```bash
python --version
rustc --version
cargo --version
node --version
pnpm --version
uv --version
```

### 2. 安装项目依赖

本仓库是两个项目放在一起：

- 主目录是 Python 后端项目，使用 `uv` 管理依赖。
- `agent-chat-ui/` 是本地前端子项目，使用自己的 `package.json`、`pnpm-lock.yaml` 和 `node_modules/`。

因此前端依赖不会复用主目录。首次运行、重新 clone、或清理过 `agent-chat-ui/node_modules/` 后，都需要在 `agent-chat-ui/` 里重新执行 `pnpm install`。

安装 Python 后端依赖：

```bash
uv sync
```

安装本地 Agent Chat UI 前端依赖：

```bash
cd agent-chat-ui
pnpm install
cd ..
```

安装 OpenSpec CLI：

```bash
pnpm add -g @fission-ai/openspec@latest
openspec --version
```

### 3. 准备本地配置

设置火山 ECS MCP 和豆包模型所需环境变量：

```bash
export VOLCENGINE_ACCESS_KEY="your-volcengine-ak"
export VOLCENGINE_SECRET_KEY="your-volcengine-sk"
export VOLCENGINE_REGION="cn-beijing"
export VOLCENGINE_ENDPOINT="open.volcengineapi.com"
export ARK_API_KEY="your-doubao-api-key"
```

`configs/volcengine-ecs-agent.yaml` 是已提交的默认运行配置，不包含真实 AK/SK 或 API Key。LangGraph 后端会固定读取这个相对路径，不需要额外配置“配置文件路径”环境变量。配置文件已包含：

- ECS MCP Server：`uvx --from git+https://github.com/volcengine/mcp-server#subdirectory=server/mcp_server_ecs mcp-server-ecs`
- 豆包模型：火山方舟 OpenAI 兼容接口 `https://ark.cn-beijing.volces.com/api/v3`
- 安全提示词：启动、续费、更新状态等写操作前必须二次确认

## 本地开发运行

推荐的本地开发方式是同时运行 LangGraph 后端和本地 Agent Chat UI。后端负责执行 agent、加载 ECS MCP 工具和访问豆包模型；前端只负责本地浏览器交互。

### 1. 启动 LangGraph 后端

在第一个终端运行：

```bash
uv run langgraph dev
```

后端默认监听：

```text
http://localhost:2024
```

LangGraph API 文档：

```text
http://localhost:2024/docs
```

这个命令会启动本地 LangGraph Agent Server。它会根据 `langgraph.json` 加载 `ecs_agent`，并在本机提供 LangGraph API。`ecs_agent` 的实现入口是 `src/agent_ecs_helper/graph.py:make_graph`，里面会连接豆包模型和 ECS MCP 工具。

`make_graph` 会直接读取 `configs/volcengine-ecs-agent.yaml`。如果要临时使用另一份配置，可以继续走 CLI 的 `--config` 参数；LangGraph 后端入口保持固定默认配置，减少开发时的环境变量。

`uv run langgraph dev` 默认可能会自动打开远程 LangSmith Studio：

```text
https://smith.langchain.com/studio/?baseUrl=http://127.0.0.1:2024
```

Studio 里的 `Not seeing LangSmith runs?` 提示不是本地 ECS agent 报错，只表示没有把本地执行数据上传到 LangSmith 云端，所以远程 Studio 看不到 tracing runs。本项目日常开发可以继续使用本地 Agent Chat UI，不需要配置 LangSmith。

### 2. 启动本地 Agent Chat UI

如果之前清理过目录，或者看到 `turbo: command not found` / `node_modules missing`，先运行：

```bash
cd agent-chat-ui
pnpm install
```

在第二个终端运行：

```bash
cd agent-chat-ui
pnpm dev
```

打开：

```text
http://localhost:3000
```

默认连接：

- Deployment URL: `http://localhost:2024`
- Assistant / Graph ID: `ecs_agent`
- LangSmith API Key: 本地开发留空，不上传本地执行数据

前端只调用本地 LangGraph API，不读取 AK/SK 或豆包 API Key。

当你在页面里发消息时，请求会发到本地 LangGraph 后端 `http://localhost:2024`。后端再运行 `ecs_agent`，必要时通过 ECS MCP 调用火山 ECS API。

## 日志与调试

### 查看用户输入和 agent 执行详情

本地开发时有三个地方可以看执行信息：

1. **Agent Chat UI**

打开：

```text
http://localhost:3000
```

这里能看到用户输入、assistant 输出、工具调用展示和当前 thread 的对话上下文。这是日常调试最直观的入口。

2. **LangGraph API 文档**

打开：

```text
http://localhost:2024/docs
```

这里可以直接调用 LangGraph 的 API，例如 threads、runs、assistants 等接口。用户输入会作为 thread/run 的 `messages` 写入本地 LangGraph 后端状态。

3. **后端终端日志**

启动后端时可以调整日志级别：

```bash
uv run langgraph dev --server-log-level debug
```

如果日志太吵，可以降噪：

```bash
uv run langgraph dev --server-log-level warning
```

如果只想记录到文件，也可以用 shell 重定向：

```bash
uv run langgraph dev --server-log-level debug > langgraph-dev.log 2>&1
```

### 为什么一直打印 `watchfiles` 的 changes detected

类似下面的日志：

```text
3 changes detected [watchfiles.main]
```

来自 `langgraph dev` 的热重载文件监听。开发模式会监控项目文件变化，只要检测到 Python 文件、前端产物、缓存、临时状态或编辑器保存动作，就会打印 `watchfiles` 的变更提示。

如果不需要热重载，可以关闭：

```bash
uv run langgraph dev --no-reload
```

如果只是嫌它刷屏，可以提高日志级别：

```bash
uv run langgraph dev --server-log-level warning
```

推荐的安静后端启动命令：

```bash
uv run langgraph dev --no-reload --server-log-level warning
```

## 其他运行入口

### CLI 单次运行

适合临时查询或脚本化调用。

```bash
uv run ecs-agent --config configs/volcengine-ecs-agent.yaml "列出 cn-beijing 下最近的 ECS 实例"
```

这个命令不会启动常驻后端。它会在当前进程里加载配置、创建 agent、回答一次问题，然后退出。

### CLI 交互模式

适合在终端中连续询问多个 ECS 运维问题。

```bash
uv run ecs-agent --config configs/volcengine-ecs-agent.yaml
```

退出：

```text
exit
quit
q
```

### LangGraph SDK 示例

需要先启动 LangGraph 后端。

```bash
uv run python examples/langgraph_sdk_ecs_mcp.py
```

更多说明：

```text
docs/langgraph-sdk-10min-quickstart.md
```

## Verify

检查 Python 语法：

```bash
python3 -m compileall src examples
```

构建本地 Agent Chat UI：

```bash
cd agent-chat-ui
pnpm turbo build --filter=web
cd ..
```

查看工作区：

```bash
git status --short
git diff --stat
```

确认忽略规则：

```bash
git check-ignore -v .venv .uv-cache .langgraph_api agent-chat-ui/node_modules agent-chat-ui/.turbo .env
```

## Develop With OpenSpec

开发一个行为变更时：

```text
/opsx:new <change-id>
```

让助手补齐 proposal、design、tasks 和 spec delta：

```text
/opsx:ff
```

按 tasks 实现：

```text
/opsx:apply
```

实现后验证：

```bash
python3 -m compileall src examples
cd agent-chat-ui && pnpm turbo build --filter=web && cd ..
```

完成后归档：

```text
/opsx:archive
```

如果只是维护命令、文档或补充当前状态，也要确保 `openspec/specs/` 与 README 一致。

## Command Cheat Sheet

```bash
# Config
export VOLCENGINE_ACCESS_KEY="your-volcengine-ak"
export VOLCENGINE_SECRET_KEY="your-volcengine-sk"
export VOLCENGINE_REGION="cn-beijing"
export VOLCENGINE_ENDPOINT="open.volcengineapi.com"
export ARK_API_KEY="your-doubao-api-key"

# Install
rustup update stable
uv sync
cd agent-chat-ui && pnpm install && cd ..
pnpm add -g @fission-ai/openspec@latest

# CLI
uv run ecs-agent --config configs/volcengine-ecs-agent.yaml "列出 cn-beijing 下最近的 ECS 实例"
uv run ecs-agent --config configs/volcengine-ecs-agent.yaml

# LangGraph backend
uv run langgraph dev

# Local frontend
cd agent-chat-ui
pnpm dev

# SDK
uv run python examples/langgraph_sdk_ecs_mcp.py

# Verify
python3 -m compileall src examples
cd agent-chat-ui && pnpm turbo build --filter=web && cd ..

# OpenSpec
openspec --version

# GitHub
gh auth login
git status --short
git add .
git commit -m "Update project"
git push -u origin master
```
