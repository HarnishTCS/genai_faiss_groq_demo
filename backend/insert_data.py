from pymongo import MongoClient
from datetime import datetime

# Connect to MongoDB
client = MongoClient("mongodb://localhost:27017/")
db = client["genai_db"]

# 1. Insert real question-answer data in a 'queries' collection
queries_collection = db["queries"]
queries_collection.insert_many([
    {
        "question": "What is FastAPI?",
        "answer": "FastAPI is a modern, fast (high-performance) web framework for building APIs with Python 3.6+.",
        "timestamp": datetime.now()
    },
    {
        "question": "What is MongoDB?",
        "answer": "MongoDB is a NoSQL database designed for storing and retrieving large volumes of unstructured data.",
        "timestamp": datetime.now()
    },
    {
        "question": "What is FAISS?",
        "answer": "FAISS is a library developed by Facebook for efficient similarity search and clustering of dense vectors.",
        "timestamp": datetime.now()
    }
])

# 2. Optional: Check inserted data
print("Inserted documents:")
for doc in queries_collection.find():
    print(doc)
