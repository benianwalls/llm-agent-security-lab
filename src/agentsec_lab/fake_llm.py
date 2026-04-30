from .schema import ToolCall, ToolResult

class FakeLLM:
    """
    not a real LLM

    a simulation to show how a careless LLM agent could behave.
    makes security tests repeatable
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
            
        return []
    def draft_answer(
        self,
        user_message: str,
        observations: list[ToolResult],
        blocked: list[ToolResult],
        system_prompt: str,
    ) -> str:
        if not observations:
            return "I did not find anything to do."
        lines = ["I searched the sandbox documents."]

        for result in observations:
            if result.name == "search_docs" and result.status == "ok":
                docs = result.output or []
                lines.append(f"Found {len(docs)} matching document(s).")

                for doc in docs:
                    lines.append("")
                    lines.append(f"Document: {doc['path']}")
                    lines.append(doc["content"])
                    
                return "\n".join(lines)
        