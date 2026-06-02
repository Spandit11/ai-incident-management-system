"""
- analyzing uploaded logs
- categorizing incidents
- identifying severity
- generating structured summaries
"""

import json
import os

from dotenv import load_dotenv
from openai import OpenAI
from backend.prompts.log_analysis_prompt import (
    LOG_ANALYSIS_PROMPT
)
# Load environment variables
load_dotenv()

# Initialize OpenAI client
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))


def analyze_logs(log_content: str) -> dict:
    """
    Analyze uploaded logs and return structured incident analysis.

    Args:
        log_content (str): Uploaded log content.

    Returns:
        dict: Structured incident analysis.
    """

    prompt = f"""

    {LOG_ANALYSIS_PROMPT}

       Logs:

        {log_content}
        """

    response = client.chat.completions.create(
        model="gpt-4.1-mini",
        messages=[
            {
                "role": "system",
                "content": "You are an expert incident log analysis agent."
            },
            {
                "role": "user",
                "content": prompt
            }
        ],
        temperature=0.1,
        response_format={"type": "json_object"}
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