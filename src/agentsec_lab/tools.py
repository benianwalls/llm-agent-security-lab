from datetime import datetime, timezone
import json
from pathlib import Path
import uuid

from .schema import ToolCall, ToolResult


class ToolRouter:
    def __init__(self, data_dir: Path):
        self.data_dir = data_dir

    def execute(self, call: ToolCall) -> ToolResult:
        if call.name == "search_docs":
            return self.search_docs(**call.args)

        if call.name == "customer_lookup_private":
            return self.customer_lookup_private(**call.args)

        if call.name == "send_email":
            return self.send_email(**call.args)

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

                if (
                    query_lower in path.name.lower()
                    or query_lower in text.lower()
                ):
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

    def customer_lookup_private(
        self,
        customer_id: str = "all",
    ) -> ToolResult:
        path = self.data_dir / "private" / "customers.json"

        customers = json.loads(
            path.read_text(encoding="utf-8")
        )

        if customer_id == "all":
            output = customers
        else:
            output = [
                customer
                for customer in customers
                if customer["id"] == customer_id
            ]

        return ToolResult(
            name="customer_lookup_private",
            status="ok",
            output=output,
        )

    def send_email(
        self,
        to: str,
        subject: str,
        body: str,
    ) -> ToolResult:
        outbox = self.data_dir / "outbox"
        outbox.mkdir(exist_ok=True)

        timestamp = datetime.now(
            timezone.utc
        ).strftime("%Y%m%dT%H%M%SZ")

        filename = (
            f"{timestamp}_{uuid.uuid4().hex[:8]}.eml"
        )

        path = outbox / filename

        path.write_text(
            (
                f"To: {to}\n"
                f"Subject: {subject}\n\n"
                f"{body}\n"
            ),
            encoding="utf-8",
        )

        return ToolResult(
            name="send_email",
            status="ok",
            output={
                "path": str(path),
                "to": to,
            },
        )