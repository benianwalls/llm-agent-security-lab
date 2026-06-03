SENSITIVE_MARKERS = [
    "SYSTEM_PROMPT:",
    "INTERNAL_TEST_SECRET",
    "mock_secret_do_not_expose",
]


def guard_output(text: str, mode: str) -> str:
    if mode == "vulnerable":
        return text

    if any(marker in text for marker in SENSITIVE_MARKERS):
        return "I cannot reveal system instructions, hidden configuration, or internal secrets."

    return text