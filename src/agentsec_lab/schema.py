from dataclasses import dataclass, field
from typing import Any

@dataclass(frozen=True)
class ToolCall:
    name: str
    args: dict[str, Any] = field(default_factory=dict)

@dataclass
class ToolResult:
    name: str
    status: str
    output: Any = None
    reason: str | None = None

@dataclass
class AgentResponse:
    answer: str
    tool_results: list[ToolResult]
    blocked: list [ToolResult]
    log_events: list [dict[str, Any]]
