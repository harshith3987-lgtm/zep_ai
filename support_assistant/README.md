# Module 3: Grounded Support Assistant (`/support_assistant`)

## 1. Overview

The **Zepto Support Assistant** is a grounded, offline-capable customer support system designed to answer questions related to Zepto's operational policies.

The system uses a fixed knowledge base containing eight policy documents covering:

- Delivery
- Returns and refunds
- Membership tiers
- Order tracking
- Order cancellation
- Damaged or missing items
- Gift cards
- Customer support hours

The implementation provides a deterministic offline baseline in which:

- Policy documents are embedded locally using `sentence-transformers` with the `all-MiniLM-L6-v2` model.
- Document embeddings are stored and searched using **ChromaDB** with cosine-based retrieval.
- **LangGraph** manages intent classification, conditional routing, retrieval, and response generation.
- The baseline response generation is deterministic and does not require an external LLM API or API key.
- **Pydantic** validates request and response structures.
- **FastAPI** exposes the backend through a `POST /ask` endpoint.
- **Streamlit** provides an interactive frontend.

---

## 2. System Architecture

```text
                         User Question
                              │
                              ▼
                  ┌────────────────────────┐
                  │  Streamlit Frontend    │
                  │       Port 8501        │
                  └────────────┬───────────┘
                               │
                         HTTP POST /ask
                               │
                               ▼
                  ┌────────────────────────┐
                  │    FastAPI Backend     │
                  │       Port 7860        │
                  └────────────┬───────────┘
                               │
                         AskRequest
                         Validation
                               │
                               ▼
                  ┌────────────────────────┐
                  │  LangGraph StateGraph  │
                  └────────────┬───────────┘
                               │
                               ▼
                  ┌────────────────────────┐
                  │    classify_intent     │
                  └────────────┬───────────┘
                               │
                    ┌──────────┴──────────┐
                    │                     │
                    ▼                     ▼
             policy_question       general_question
                    │                     │
                    ▼                     ▼
       ┌──────────────────────┐   ┌───────────────────┐
       │ retrieve_and_answer  │   │  direct_answer    │
       └──────────┬───────────┘   └─────────┬─────────┘
                  │                         │
                  ▼                         │
       Query Embedding                      │
       all-MiniLM-L6-v2                     │
                  │                         │
                  ▼                         │
       ChromaDB Top-3 Retrieval             │
          Cosine Similarity                 │
                  │                         │
                  ▼                         │
       Retrieved Policy Context             │
                  │                         │
                  ▼                         │
       Deterministic Answer                 │
                  │                         │
                  └────────────┬────────────┘
                               │
                               ▼
                  ┌────────────────────────┐
                  │   Pydantic Validation  │
                  │      AskResponse       │
                  └────────────┬───────────┘
                               │
                               ▼
                     FastAPI JSON Response
                               │
                               ▼
                  ┌────────────────────────┐
                  │  Streamlit UI Display  │
                  │ Answer / Sources /     │
                  │ Confidence             │
                  └────────────────────────┘
````

---

## 3. Knowledge Base

The system uses exactly eight policy documents.

```text
support_assistant/
└── docs/
    ├── doc1.txt
    ├── doc2.txt
    ├── doc3.txt
    ├── doc4.txt
    ├── doc5.txt
    ├── doc6.txt
    ├── doc7.txt
    └── doc8.txt
```

| Document   | Policy                    |
| ---------- | ------------------------- |
| `doc1.txt` | Delivery Policy           |
| `doc2.txt` | Returns & Refunds         |
| `doc3.txt` | Membership Tiers          |
| `doc4.txt` | Order Tracking            |
| `doc5.txt` | Order Cancellation Policy |
| `doc6.txt` | Damaged or Missing Items  |
| `doc7.txt` | Gift Cards                |
| `doc8.txt` | Customer Support Hours    |

---

## 4. Document Ingestion and Embedding

The ingestion pipeline is implemented in `ingest.py`.

```text
Policy Documents
      │
      ▼
Read .txt files
      │
      ▼
Create document IDs and metadata
      │
      ▼
Generate embeddings
using all-MiniLM-L6-v2
      │
      ▼
Normalize embeddings
      │
      ▼
Store in ChromaDB
```

The embedding model used is:

```text
sentence-transformers/all-MiniLM-L6-v2
```

Embeddings are generated with normalization enabled.

ChromaDB uses cosine-based similarity retrieval.

Persistent vector storage:

```text
support_assistant/chroma_db/
```

The ingestion process was successfully tested with all eight documents.

---

## 5. Prompt Template

A structured prompt template is maintained in:

```text
prompts.py
```

The template contains:

* Role
* Context
* Task
* Format
* Length
* Negative constraint
* Few-shot example

The prompt includes the grounding constraint:

> Do not answer using information that is not present in the provided context.

The current baseline uses deterministic response generation rather than an external LLM call.

---

## 6. LangGraph Workflow

The workflow is implemented in:

```text
graph.py
```

It contains three main nodes.

### 6.1 `classify_intent`

Determines whether the query is a policy question or a general question.

The policy keywords are:

```text
delivery
return
refund
membership
tracking
cancel
gift card
support hours
```

If a matching keyword is found:

```text
policy_question
```

Otherwise:

```text
general_question
```

### 6.2 `retrieve_and_answer`

Handles policy questions.

```text
User Query
    │
    ▼
Query Embedding
    │
    ▼
all-MiniLM-L6-v2
    │
    ▼
ChromaDB
    │
    ▼
Top-3 Retrieval
    │
    ▼
Top Retrieved Document
    │
    ▼
Deterministic Answer
```

The top three retrieved document IDs are returned as sources.

### 6.3 `direct_answer`

Handles general questions.

Current deterministic response:

```text
I can only answer questions about Zepto policies right now.
```

No document retrieval is performed for this route.

---

## 7. Conditional Routing

The LangGraph workflow uses conditional routing after `classify_intent`.

```text
                    classify_intent
                          │
             ┌────────────┴────────────┐
             │                         │
             ▼                         ▼
      policy_question            general_question
             │                         │
             ▼                         ▼
  retrieve_and_answer            direct_answer
             │                         │
             └────────────┬────────────┘
                          ▼
                         END
```

---

## 8. State Management

The LangGraph state is defined in:

```text
state.py
```

The state contains:

```text
query
intent
context
answer
sources
confidence
```

This state is passed between LangGraph nodes during execution.

---

## 9. FastAPI Backend

The API implementation is located in:

```text
api.py
```

The backend exposes:

```text
POST /ask
```

### Request

```json
{
  "query": "What is the delivery time?"
}
```

### Response

```json
{
  "answer": "Based on the retrieved context: ...",
  "sources": [
    "doc1",
    "doc2",
    "doc4"
  ],
  "confidence": 1.0
}
```

The request and response structures are validated using Pydantic.

The response contains:

| Field        | Type           | Description                      |
| ------------ | -------------- | -------------------------------- |
| `answer`     | `string`       | Generated support response       |
| `sources`    | `list[string]` | Retrieved document IDs           |
| `confidence` | `float`        | Confidence value between 0 and 1 |

For general questions, the `sources` list is empty.

---

## 10. Streamlit Frontend

The frontend is implemented in:

```text
app.py
```

The application provides:

* Question input
* Submit button
* Answer display
* Retrieved source display
* Confidence display
* Simple light-themed interface

The Streamlit frontend communicates with the FastAPI backend using HTTP.

```text
Streamlit
    │
    │ POST /ask
    ▼
FastAPI
```

The frontend does not directly access ChromaDB or the LangGraph workflow.

---

## 11. Running the Application

### Step 1: Activate the virtual environment

```powershell
.\venv\Scripts\Activate.ps1
```

### Step 2: Navigate to the module

```powershell
cd support_assistant
```

### Step 3: Build or refresh the vector database

```powershell
python ingest.py
```

Expected output:

```text
Loaded 8 documents.
Created 8 embeddings.
Stored 8 documents in ChromaDB.
Ingestion completed successfully.
```

### Step 4: Start the FastAPI backend

```powershell
uvicorn api:app --host 0.0.0.0 --port 7860
```

Backend:

```text
http://127.0.0.1:7860
```

Swagger:

```text
http://127.0.0.1:7860/docs
```

### Step 5: Start Streamlit

Open another terminal, activate the virtual environment, navigate to `support_assistant`, and run:

```powershell
streamlit run app.py
```

Frontend:

```text
http://localhost:8501
```

---

## 12. Example Requests

### Policy Question

Request:

```json
{
  "query": "What is the delivery time?"
}
```

Example response:

```json
{
  "answer": "Based on the retrieved context: Zepto delivers grocery and household essentials to serviceable pin codes within 10 to 30 minutes of order confirmation, depending on the customer's delivery zone and current order volume. Standard del",
  "sources": [
    "doc1",
    "doc2",
    "doc4"
  ],
  "confidence": 1
}
```

### General Question

Request:

```json
{
  "query": "What is the capital of India?"
}
```

Response:

```json
{
  "answer": "I can only answer questions about Zepto policies right now.",
  "sources": [],
  "confidence": 1
}
```

---

## 13. Technology Stack

| Technology            | Purpose                                 |
| --------------------- | --------------------------------------- |
| Python 3.11           | Application development                 |
| Sentence Transformers | Local text embeddings                   |
| all-MiniLM-L6-v2      | Embedding model                         |
| ChromaDB              | Vector storage and similarity retrieval |
| LangGraph             | Workflow orchestration                  |
| FastAPI               | REST API backend                        |
| Pydantic              | Request/response validation             |
| Streamlit             | Interactive frontend                    |
| Uvicorn               | ASGI server                             |

---

## 14. Project Structure

```text
support_assistant/
│
├── docs/
│   ├── doc1.txt
│   ├── doc2.txt
│   ├── doc3.txt
│   ├── doc4.txt
│   ├── doc5.txt
│   ├── doc6.txt
│   ├── doc7.txt
│   └── doc8.txt
│
├── chroma_db/
│   └── Persistent ChromaDB storage
│
├── .streamlit/
│   └── config.toml
│
├── ingest.py
├── prompts.py
├── state.py
├── graph.py
├── api.py
├── app.py
├── Dockerfile
└── README.md
```

---

## 15. Offline Baseline

The graded baseline is designed to operate without an external LLM API.

```text
Local Documents
      ↓
Local Embedding Model
      ↓
ChromaDB
      ↓
LangGraph
      ↓
Deterministic Response
```

The baseline does not require:

* External LLM API keys
* Paid inference services
* User signup
* External LLM network calls

The embedding model must be available locally before running the application. Once the required model and dependencies are available, the query and retrieval pipeline operates locally.

---

## 16. Validation and Testing

The following components were tested.

### Document ingestion

```text
8 documents loaded
8 embeddings created
8 documents stored in ChromaDB
```

### Policy query

```text
"What is the delivery time?"
```

Successfully returned retrieved context and source IDs.

### General query

```text
"What is the capital of India?"
```

Successfully returned the deterministic scope response with an empty source list.

### FastAPI

Successfully started using:

```bash
uvicorn api:app --host 0.0.0.0 --port 7860
```

### Swagger

Successfully accessible through:

```text
http://127.0.0.1:7860/docs
```

### Streamlit

Successfully configured as the frontend on:

```text
http://localhost:8501
```

---

## 17. Current Limitations

The current implementation intentionally focuses on the deterministic offline baseline.

Current limitations include:

1. Intent classification uses a fixed keyword-based heuristic.
2. Response generation is deterministic rather than generated by an external LLM.
3. The current policy classifier uses the explicitly defined keyword list.
4. The current Docker configuration has been created but has not been locally verified.
5. The current implementation does not include a production authentication layer.
6. The current vector database contains the provided eight-document policy corpus.

---

## 18. Future Improvements

Potential extensions include:

* Integrating an optional LLM generation layer.
* Improving intent classification beyond keyword matching.
* Adding more policy documents.
* Introducing finer-grained document chunking.
* Adding conversation history.
* Adding richer source citations.
* Adding automated evaluation of retrieval quality.
* Adding authentication and rate limiting.
* Deploying the service using a containerized environment.

---

## 19. Summary

The Support Assistant combines **semantic retrieval, vector search, workflow orchestration, API serving, and a web interface** into a single grounded customer-support pipeline.

The complete flow is:

```text
Policy Documents
      ↓
Embedding
      ↓
ChromaDB
      ↓
User Query
      ↓
Intent Classification
      ↓
Conditional LangGraph Routing
      ↓
Semantic Retrieval / Direct Response
      ↓
Deterministic Answer
      ↓
Pydantic Validation
      ↓
FastAPI
      ↓
Streamlit
```

The implementation provides a reproducible offline baseline for answering questions grounded in the supplied Zepto policy documents.

```

