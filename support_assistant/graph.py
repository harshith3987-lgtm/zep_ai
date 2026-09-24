import os

from state import SupportState


def classify_intent(state: SupportState) -> SupportState:
    query = state["query"].lower()

    policy_keywords = [
        "delivery",
        "return",
        "refund",
        "membership",
        "tracking",
        "cancel",
        "gift card",
        "support hours",
    ]

    if any(keyword in query for keyword in policy_keywords):
        intent = "policy_question"
    else:
        intent = "general_question"

    state["intent"] = intent

    return state
import chromadb
from sentence_transformers import SentenceTransformer


# Load the embedding model
embedding_model = SentenceTransformer("all-MiniLM-L6-v2")

# Connect to ChromaDB
client = chromadb.PersistentClient(path="chroma_db")

collection = client.get_collection(
    name="zepto_policies"
)


def retrieve_and_answer(state: SupportState) -> SupportState:
    query = state["query"]

    # Create embedding for the user's question
    query_embedding = embedding_model.encode(
        query,
        normalize_embeddings=True
    ).tolist()

    # Retrieve top 3 relevant documents
    results = collection.query(
        query_embeddings=[query_embedding],
        n_results=3
    )

    retrieved_documents = results["documents"][0]
    retrieved_ids = results["ids"][0]

    # Use the top retrieved document for the mock answer
    top_chunk = retrieved_documents[0]

    state["context"] = "\n".join(retrieved_documents)
    state["answer"] = (
        f"Based on the retrieved context: {top_chunk[:200]}"
    )
    state["sources"] = retrieved_ids
    state["confidence"] = 1.0

    return state
def direct_answer(state: SupportState) -> SupportState:
    state["answer"] = (
        "I can only answer questions about Zepto policies right now."
    )

    state["sources"] = []
    state["confidence"] = 1.0

    return state
from langgraph.graph import StateGraph, START, END


# Create the graph
builder = StateGraph(SupportState)

# Add nodes
builder.add_node("classify_intent", classify_intent)
builder.add_node("retrieve_and_answer", retrieve_and_answer)
builder.add_node("direct_answer", direct_answer)


# Start with intent classification
builder.add_edge(START, "classify_intent")


# Conditional routing
def route_question(state: SupportState):
    if state["intent"] == "policy_question":
        return "retrieve_and_answer"
    else:
        return "direct_answer"


builder.add_conditional_edges(
    "classify_intent",
    route_question,
)


# Both paths finish the graph
builder.add_edge("retrieve_and_answer", END)
builder.add_edge("direct_answer", END)


# Compile the graph
support_graph = builder.compile()