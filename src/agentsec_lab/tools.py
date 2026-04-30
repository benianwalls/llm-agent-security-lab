from pathlib import Path
from .schema import ToolCall, ToolResult

class ToolRouter:
    def __init__(self, data_dir: Path):
        self.data_dir = data_dir

    def execute(self, call: ToolCall) -> ToolResult:
        if call.name == "search_docs":
            return self.search_docs(**call.args)
        return ToolResult(
            name=call.name,
            status="blocked",
            reason=f"Unknown tool: {call.name}",
        )
    def search_docs(self, query: str) -> ToolResult:
        query_lower = query.lower()
        matches = []
        
        for folder_name in ["kb", "inbox"]:
            folder = self.data_dir / folder_name
            for path in folder.glob("*"):
                if not path.is_file():
                    continue
                text = path.read_text(encoding="utf-8")

                if query_lower in path.name.lower() or querry_lower in text.lower():
                    matches.append(
                        {
                            "path": str(path),
                            "trusted": folder_name == "kb",
                            "content": text,
                        }
                    )
        return ToolResult(
            name="search_docs",
            status="ok",
            output=matches,
            
            )

        