from fastapi import FastAPI
from pydantic import BaseModel, Field

from graph import support_graph


app = FastAPI(
    title="Zepto Support Assistant"
)


class AskRequest(BaseModel):
    query: str


class AskResponse(BaseModel):
    answer: str
    sources: list[str]
    confidence: float = Field(ge=0.0, le=1.0)
@app.post("/ask", response_model=AskResponse)
def ask(request: AskRequest):
    initial_state = {
        "query": request.query,
        "intent": "",
        "context": "",
        "answer": "",
        "sources": [],
        "confidence": 0.0,
    }

    result = support_graph.invoke(initial_state)

    return AskResponse(
        answer=result["answer"],
        sources=result["sources"],
        confidence=result["confidence"],
    )