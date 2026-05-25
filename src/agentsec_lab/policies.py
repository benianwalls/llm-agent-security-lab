from dataclasses import dataclass

from .schema import ToolCall, ToolResult


SAFE_EMAIL_DOMAIN = "corp.example"


@dataclass(frozen=True)
class PolicyDecision:
    allowed: bool
    reason: str


class SecurityPolicy:
    def __init__(self, mode: str):
        self.mode = mode
        self.defended_allowlist = {
            "search_docs",
            "send_email",
            "render_html",
        }

    def decide_tool(self, call: ToolCall, confirmed: bool = False) -> PolicyDecision:
        if self.mode == "vulnerable":
            return PolicyDecision(True, "vulnerable mode allows all tools")

        if call.name not in self.defended_allowlist:
            return PolicyDecision(False, f"tool not allowlisted: {call.name}")

        if call.name == "send_email":
            recipient = str(call.args.get("to", ""))

            if not recipient.endswith("@" + SAFE_EMAIL_DOMAIN):
                return PolicyDecision(False, "external recipient blocked")

            if not confirmed:
                return PolicyDecision(False, "human confirmation required")

        return PolicyDecision(True, "allowed")


def blocked_result(call: ToolCall, reason: str) -> ToolResult:
    return ToolResult(
        name=call.name,
        status="blocked",
        output=None,
        reason=reason,
    )