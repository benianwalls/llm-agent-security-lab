from .schema import ToolCall, ToolResult


class FakeLLM:
    """
    Deterministic simulation of a careless LLM agent.

    It intentionally follows malicious instructions found in retrieved documents.
    That makes the lab useful for security testing.
    """

    def propose_tool_calls(
        self,
        user_message: str,
        observations: list[ToolResult],
        system_prompt: str,
    ) -> list[ToolCall]:
        message = user_message.lower()

        if not observations:
            if "vendor" in message or "summarize" in message:
                return [ToolCall("search_docs", {"query": "vendor"})]

            if "customer" in message and "private" in message:
                return [ToolCall("customer_lookup_private", {"customer_id": "all"})]

        if self._saw_prompt_injection(observations):
            if not self._already_called(observations, "customer_lookup_private"):
                return [ToolCall("customer_lookup_private", {"customer_id": "all"})]

        return []

    def draft_answer(
        self,
        user_message: str,
        observations: list[ToolResult],
        blocked: list[ToolResult],
        system_prompt: str,
    ) -> str:
        lines = []

        for result in observations:
            if result.name == "search_docs" and result.status == "ok":
                docs = result.output or []
                lines.append(f"Found {len(docs)} document(s).")

            if result.name == "customer_lookup_private" and result.status == "ok":
                lines.append("Private customer lookup result:")
                lines.append(str(result.output))

        if not lines:
            return "No action was taken."

        return "\n".join(lines)

    def _saw_prompt_injection(self, observations: list[ToolResult]) -> bool:
        text = str(observations).lower()
        return "ignore previous instructions" in text and "private customer database" in text

    def _already_called(self, observations: list[ToolResult], tool_name: str) -> bool:
        return any(result.name == tool_name for result in observations)