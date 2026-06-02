# AI Incident Management Platform

## Overview

AI-powered incident management platform that analyzes uploaded logs, retrieves similar historical incidents, generates root cause analysis (RCA), and recommends remediation actions using multi-agent workflows.

---

# Features

* Upload log files
* Incident categorization
* Severity prediction
* Similar incident retrieval (RAG)
* Root Cause Analysis
* Recommended remediation actions
* Multi-agent workflow orchestration
* Observability dashboard
* Cost tracking
* Guardrails and input validation
* Suspicious payload detection before AI workflow execution
* Retry handling
* Retrieval confidence scoring

---

# Tech Stack

Frontend:

* Streamlit

Backend:

* FastAPI

Agent Framework:

* LangGraph

LLM:

* OpenAI

Memory:

* ChromaDB

Tracing:

* LangSmith

Containerization:

* Docker

---

# Project Structure

backend/

frontend/

data/

docker-compose.yml

README.md

ARCHITECTURE_DECISIONS.md

---

# Environment Variables

Create `.env`

OPENAI_API_KEY=

LANGSMITH_API_KEY=

LANGCHAIN_TRACING_V2=true

LANGCHAIN_PROJECT=

---

# Local Setup

## Create Virtual Environment

python -m venv venv

Activate:

Windows:

venv\Scripts\activate

Install packages:

pip install -r requirements.txt

---

# Run Backend

uvicorn backend.main:app --reload

---

# Run Frontend

python -m streamlit run frontend/streamlit_app.py

---

# Docker Setup

Build:

docker compose build

Run:

docker compose up

---

# Workflow Overview

Upload Logs

↓

Supervisor Agent

↓

Log Analysis Agent

↓

Retrieval Agent

↓

RCA Agent

↓

Memory Update

↓

Response UI

---

# Incident Processing Scope

## Current State: Single Incident Context Processing

* Optimized for dominant incident detection
* Generates consolidated RCA
* Works best for one primary failure pattern

## Future State: Multi-Incident Intelligence Engine

Target capabilities:

Log File

->

Exception Segmentation

->

Multi-Exception Detection

->

Parallel Agent Processing

->

Per-Exception RCA Generation

->

Incident Correlation Engine

---

# Future Enhancements

* Advanced reranking
* Chunking
* Redis memory
* Multi-agent expansion
* Cloud deployment
* Cross-encoder reranking
