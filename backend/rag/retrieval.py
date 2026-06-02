"""
Semantic retrieval module.
"""

import os

from dotenv import load_dotenv
from openai import OpenAI

from backend.rag.chroma_store import collection

# Load environment variables
load_dotenv()

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))


def generate_embedding(text: str):
    """
    Generate embedding vector.
    """

    response = client.embeddings.create(
        model="text-embedding-3-small",
        input=text
    )

    return response.data[0].embedding



def retrieve_similar_incidents(summary: str):
    """
    Retrieve top similar incidents.

    Args:
        summary (str): Incident summary.

    Returns:
        list: Similar incidents.
    """

    embedding = generate_embedding(summary)

    results = collection.query(
        query_embeddings=[embedding],
        n_results=3
    )

    return results