from pathlib import Path

import chromadb
from sentence_transformers import SentenceTransformer


# -----------------------------
# 1. Paths
# -----------------------------

BASE_DIR = Path(__file__).resolve().parent
DOCS_DIR = BASE_DIR / "docs"
CHROMA_DIR = BASE_DIR / "chroma_db"


# -----------------------------
# 2. Load documents
# -----------------------------

documents = []
document_ids = []
metadatas = []

for file_path in sorted(DOCS_DIR.glob("*.txt")):
    text = file_path.read_text(encoding="utf-8").strip()

    if text:
        documents.append(text)
        document_ids.append(file_path.stem)
        metadatas.append({
            "source": file_path.name
        })

print(f"Loaded {len(documents)} documents.")


# -----------------------------
# 3. Load embedding model
# -----------------------------

model = SentenceTransformer("all-MiniLM-L6-v2")

embeddings = model.encode(
    documents,
    normalize_embeddings=True
).tolist()

print(f"Created {len(embeddings)} embeddings.")


# -----------------------------
# 4. Create ChromaDB
# -----------------------------

client = chromadb.PersistentClient(
    path=str(CHROMA_DIR)
)

collection = client.get_or_create_collection(
    name="zepto_policies",
    metadata={"hnsw:space": "cosine"}
)


# -----------------------------
# 5. Store documents
# -----------------------------

collection.upsert(
    ids=document_ids,
    documents=documents,
    embeddings=embeddings,
    metadatas=metadatas
)

print(f"Stored {collection.count()} documents in ChromaDB.")
print("Ingestion completed successfully.")