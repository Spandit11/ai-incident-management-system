"""
OpenAI service responsible for AI-based incident analysis.
"""

import os
from dotenv import load_dotenv
from openai import OpenAI

# Load environment variables
load_dotenv()

# Initialize OpenAI client
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))


def analyze_logs(log_content: str) -> str:
    """
    Analyze uploaded logs using OpenAI.

    Args:
        log_content (str): Uploaded log content.

    Returns:
        str: AI-generated incident analysis.
    """

    prompt = f"""
    You are an AI Incident Management Assistant.

    Analyze the following logs and provide:
    1. Incident category
    2. Severity
    3. Possible root cause
    4. Suggested remediation

    Logs:
    {log_content}
    """

    response = client.chat.completions.create(
        model="gpt-4.1-mini",
        messages=[
            {
                "role": "system",
                "content": "You are an expert production incident analyzer."
            },
            {
                "role": "user",
                "content": prompt
            }
        ],
        temperature=0.2
    )

    return response.choices[0].message.content
