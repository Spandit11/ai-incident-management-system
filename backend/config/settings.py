"""
Application configuration.
"""

# Models

LLM_MODEL = "gpt-4.1-mini"

EMBEDDING_MODEL = (

    "text-embedding-3-small"
)

# Limits

MAX_FILE_SIZE_MB = 5

MAX_LOG_SIZE = 4000

TOP_K_RESULTS = 3

# Backend

BACKEND_URL = (

    "http://127.0.0.1:8000/analyze"
)

# Chroma

CHROMA_DB_PATH = (

    "./chroma_db"
)

# API Pricing

INPUT_TOKEN_PRICE = 0.0000004

OUTPUT_TOKEN_PRICE = 0.0000016

# CORS

CORS_ORIGINS = [

    "*"
]