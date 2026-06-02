"""Root Cause Analysis agent utilities.

This module provides a helper to generate a structured RCA JSON
for a new incident using the OpenAI client and historical context.
"""

import os
import json
from dotenv import load_dotenv
from openai import OpenAI
from backend.prompts.rca_prompt import (
    RCA_PROMPT
)
# Load environment variables
load_dotenv()

# Initialize OpenAI client
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))


def generate_rca(incident_summary: str, similar_incidents: list) -> dict:
    """Generate an RCA using the incident summary and historical incidents.

    Args:
        incident_summary: Current incident summary.
        similar_incidents: Retrieved historical incident texts.

    Returns:
        A dict with keys: `rootCause`, `confidence`, `recommendedActions`.
    """

    historical_context = "\n".join(similar_incidents)

    prompt = f"""
    {RCA_PROMPT}


Current Incident:
{incident_summary}

Historical Similar Incidents:
{historical_context}
"""

    response = client.chat.completions.create(
        model="gpt-4.1-mini",
        messages=[
            {"role": "system", "content": "You are an expert root cause analysis agent."},
            {"role": "user", "content": prompt},
        ],
        temperature=0.1,
        response_format={"type": "json_object"},
    )

    content = response.choices[0].message.content
    return {

    "result": json.loads(content),

    "usage": {

        "prompt_tokens":
        response.usage.prompt_tokens,

        "completion_tokens":
        response.usage.completion_tokens
    }
}