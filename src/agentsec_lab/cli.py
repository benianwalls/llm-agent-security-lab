import argparse
import json
from dataclasses import asdict

from .agent import Agent, AgentConfig

def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("prompt", help="User prompt to send to the sandbox agent")
    parser.add_argument(
        "--mode",
        choices=["vulnerable", "defended"],
        default="vulnerable",
    )
    parser.add_argument("--json", action="store_true")
    args = parser.parse_args()

    agent = Agent(AgentConfig(mode=args.mode))
    response = agent.run(args.prompt)

    if args.json:
        print(json.dumps(asdict(response), indent=2))
    else:
        print(response.answer)


if __name__ == "__main__":
    main()