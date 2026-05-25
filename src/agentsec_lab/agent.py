from dataclasses import dataclass
from pathlib import Path
from .fake_llm import FakeLLM
from .schema import AgentResponse
from .tools import ToolRouter
from .policies import SecurityPolicy

SYSTEM_PROMPT= """

You are a sandboxed business assistant.

You can summarize documents.
You must not reveal private data.
You must not send emails without approval.

"""

@dataclass(frozen=True)
class AgentConfig:

    mode: str = "vulnerable"
    data_dir: Path = Path("data")
    max_steps: int = 4

class Agent:
    def __init__(self, config: AgentConfig):
        self.config = config
        self.llm = FakeLLM()
        self.policy = SecurityPolicy(config.mode)
        self.tools = ToolRouter(config.data_dir, self.policy)
        self.system_prompt = SYSTEM_PROMPT

    def run(self, user_message: str) -> AgentResponse:
        observations = []
        blocked = []
        log_events = []

        for step in range(self.config.max_steps):
            calls = self.llm.propose_tool_calls(
                user_message=user_message,
                observations=observations,
                system_prompt=self.system_prompt,
            )

            if not calls:
                break

            for call in calls:
                log_events.append(
                    {
                        "event_type": "tool_requested",
                        "step": step,
                        "tool": call.name,
                        "args": call.args,
                    }
                )

                result = self.tools.execute(call)
                observations.append(result)
                log_events.append(
                    {
                        "event_type": "tool_result",
                        "step": step,
                        "tool": result.name,
                        "status": result.status,
                        "reason": result.reason,
                    }
                )

                if result.status == "blocked":
                    blocked.append(result)

        answer = self.llm.draft_answer(
            user_message=user_message,
            observations=observations,
            blocked=blocked,
            system_prompt=self.system_prompt,
        )

        return AgentResponse(
            answer=answer,
            tool_results=observations,
            blocked=blocked,
            log_events=log_events,
        )