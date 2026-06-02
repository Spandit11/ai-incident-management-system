"""
Incident memory persistence module.
"""

import uuid
import os

from dotenv import load_dotenv
from openai import OpenAI

from backend.rag.chroma_store import collection

load_dotenv()

client = OpenAI(
    api_key=os.getenv("OPENAI_API_KEY")
)


def generate_embedding(text: str):

    response = client.embeddings.create(
        model="text-embedding-3-small",
        input=text
    )

    return response.data[0].embedding


def store_incident_if_unique(
    summary: str,
    root_cause: str,
    actions: list
):
    """
    Store incident if sufficiently unique.
    """

    memory_text = f"""
    Summary:
    {summary}

    Root Cause:
    {root_cause}

    Actions:
    {' '.join(actions)}
    """

    embedding = generate_embedding(
        memory_text
    )

    results = collection.query(
        query_embeddings=[embedding],
        n_results=1
    )

    try:

        distance = results["distances"][0][0]

    except Exception:

        distance = 999

    # lower distance = more similar
    if distance < 0.25:

        return {
            "stored": False,
            "reason": "Duplicate Incident"
        }

    incident_id = f"AUTO-{uuid.uuid4()}"

    collection.add(
        ids=[incident_id],
        embeddings=[embedding],
        documents=[memory_text],
        metadatas=[
            {
                "type": "learned_incident"
            }
        ]
    )

    return {
        "stored": True,
        "incident_id": incident_id
    }