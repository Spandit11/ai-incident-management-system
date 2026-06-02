"""
ChromaDB setup and vector store initialization.
"""

import chromadb

# Create local ChromaDB client
client = chromadb.PersistentClient(path="./chroma_db")

# Create/get collection
collection = client.get_or_create_collection(
    name="incident_kb"
)