"""
Load sample incidents into ChromaDB.
"""

import json
import os

from dotenv import load_dotenv
from openai import OpenAI

from backend.rag.chroma_store import collection

# Load environment variables
load_dotenv()

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))


def generate_embedding(text: str):
    """
    Generate embeddings using OpenAI.
    """

    response = client.embeddings.create(
        model="text-embedding-3-small",
        input=text
    )

    return response.data[0].embedding


# Load incidents
with open("data/incidents.json", "r") as file:
    incidents = json.load(file)


for incident in incidents:

    embedding_text = f"""
    {incident['category']}
    {incident['summary']}
    {incident['resolution']}
    """

    embedding = generate_embedding(embedding_text)

    collection.add(
        ids=[incident["incidentId"]],
        embeddings=[embedding],
        documents=[embedding_text],
        metadatas=[
            {
                "category": incident["category"],
                "severity": incident["severity"]
            }
        ]
    )

print("Incidents loaded into ChromaDB successfully.")