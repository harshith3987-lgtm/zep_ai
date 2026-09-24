from typing import TypedDict


class SupportState(TypedDict):
    query: str
    intent: str
    context: str
    answer: str
    sources: list[str]
    confidence: float