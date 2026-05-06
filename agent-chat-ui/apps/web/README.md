# ECS Agent Chat UI Web

This app is the local Next.js frontend for the Volcengine ECS LangGraph agent.
It connects to the Python LangGraph Agent Server running from the repository
root at `http://localhost:2024`.

## Setup

Install dependencies:

```bash
cd agent-chat-ui
pnpm install
```

Run the app:

```bash
pnpm dev
```

The app will be available at `http://localhost:3000`.

## Usage

Once the app is running (or if using the deployed site), you'll be prompted to enter:

- **Deployment URL**: The URL of the LangGraph server you want to chat with. This can be a production or development URL.
- **Assistant/Graph ID**: The name of the graph, or ID of the assistant to use when fetching, and submitting runs via the chat interface.
- **LangSmith API Key**: (only required for connecting to deployed LangGraph servers) Your LangSmith API key to use when authenticating requests sent to LangGraph servers.

For this project:

- **Deployment URL**: `http://localhost:2024`
- **Assistant/Graph ID**: `ecs_agent`
- **LangSmith API Key**: leave empty for local development

These values are already configured as frontend defaults. You only need an env
file if you want to override them.

After entering these values, click `Continue`. You'll then be redirected to a chat interface where you can start chatting with your LangGraph server.
