from __future__ import annotations

import argparse
import asyncio
from pathlib import Path

from agent_ecs_helper.agent import ask
from agent_ecs_helper.config import load_config


DEFAULT_CONFIG = Path("configs/volcengine-ecs-agent.yaml")


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Manage Volcengine ECS with a LangGraph MCP agent.")
    parser.add_argument(
        "question",
        nargs="*",
        help="Question or instruction for the ECS agent. Omit it to start interactive mode.",
    )
    parser.add_argument(
        "-c",
        "--config",
        default=str(DEFAULT_CONFIG),
        help=f"Path to YAML config. Default: {DEFAULT_CONFIG}",
    )
    return parser.parse_args()


async def run_once(config_path: str, question: str) -> None:
    config = load_config(config_path)
    answer = await ask(config, question)
    print(answer)


async def run_interactive(config_path: str) -> None:
    config = load_config(config_path)
    while True:
        try:
            question = input("ecs-agent> ").strip()
        except (EOFError, KeyboardInterrupt):
            print()
            return
        if question.lower() in {"exit", "quit", "q"}:
            return
        if not question:
            continue
        answer = await ask(config, question)
        print(answer)


def main() -> None:
    args = parse_args()
    question = " ".join(args.question).strip()
    if question:
        asyncio.run(run_once(args.config, question))
    else:
        asyncio.run(run_interactive(args.config))


if __name__ == "__main__":
    main()
