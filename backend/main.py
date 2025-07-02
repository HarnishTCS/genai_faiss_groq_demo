from fastapi import FastAPI, Query
from fastapi.middleware.cors import CORSMiddleware
from sentence_transformers import SentenceTransformer
from pymongo import MongoClient
import numpy as np
import faiss
import requests
import os

app = FastAPI()

# CORS setup for frontend access
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Load embedding model
embedder = SentenceTransformer("nomic-ai/nomic-embed-text-v1", trust_remote_code=True)

# Connect to MongoDB
client = MongoClient("mongodb://localhost:27017/")
db = client["genai_db"]
collection = db["documents"]

# Load data and embeddings
docs = list(collection.find({}))
documents = [doc["text"] for doc in docs]
embeddings = embedder.encode(documents).astype("float32") if documents else np.array([])

# Create FAISS index
dimension = embeddings.shape[1] if embeddings.size > 0 else 384
index = faiss.IndexFlatL2(dimension)
if embeddings.size > 0:
    index.add(embeddings)

@app.get("/query")
def query(text: str = Query(..., description="Natural language query")):
    if not text.strip():
        return {"response": "Query is empty."}

    embedding = embedder.encode([text]).astype("float32")
    k = 3
    D, I = index.search(embedding, k)

    context_docs = [documents[i] for i in I[0] if i < len(documents)]
    context = "\n".join(context_docs)

    prompt = f"Answer based on the context:\n{context}\n\nQuestion: {text}\nAnswer:"

    headers = {
        "Authorization": f"Bearer {os.getenv('GROQ_API_KEY')}",
        "Content-Type": "application/json"
    }

    payload = {
        "model": "llama3-8b-8192",
        "messages": [
            {"role": "system", "content": "You are a helpful assistant."},
            {"role": "user", "content": prompt}
        ]
    }

    res = requests.post("https://api.groq.com/openai/v1/chat/completions", headers=headers, json=payload)
    if res.status_code == 200:
        return {"response": res.json()["choices"][0]["message"]["content"].strip()}
    else:
        return {"response": f"Error {res.status_code}: {res.text}"}
