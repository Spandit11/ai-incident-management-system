# Deployment Plan – AI Incident Management Platform

## Overview

The platform follows a containerized deployment approach where frontend, backend, vector storage, observability, and configuration are independently deployable components.

---

# 1. Frontend Deployment

## Component

Streamlit UI

## Responsibility

* Log upload
* Results visualization
* Workflow monitoring
* Metrics display

## Deployment Options

### Option A – Streamlit Cloud

Best for:

* Demo deployment
* Quick setup

### Option B – Container Deployment

Run using Docker container.

Example:

```bash
docker run frontend-image
```

### Option C – VM Deployment

Deploy on:

* Linux VM
* Windows VM
* Cloud VM

## Required Config

```text
BACKEND_URL
```

---

# 2. Backend Deployment

## Component

FastAPI Service

## Responsibility

* Workflow orchestration
* Agent execution
* RAG retrieval
* RCA generation

## Deployment Options

### Option A – Docker Container

Run FastAPI inside container.

Expose:

```text
Port 8000
```

### Option B – Cloud App Services

Examples:

* Azure App Service
* Container Apps
* VM deployment

## Runtime Components

* FastAPI
* LangGraph
* OpenAI SDK
* ChromaDB
* Retry handlers

---

# 3. LangGraph Workflow Layer

## Components

* Supervisor Agent
* Analysis Agent
* Retrieval Agent
* RCA Agent

## Deployment Model

Embedded within backend container.

Benefits:

* Reduced network latency
* Simpler orchestration
* Easier scaling

---

# 4. Vector Database Deployment

## Component

ChromaDB

## Responsibility

* Incident embeddings
* Historical retrieval
* Similarity search

## Current Deployment

Local persistent storage.

```text
/chroma_db
```

## Future Deployment

Possible options:

* Persistent volumes
* Managed vector DB
* Separate storage container

## Persistence Requirement

Volume mounting recommended.

---

# 5. Memory Layer Deployment

## Components

```text
incidents.json
metrics.json
```

## Responsibility

* Historical incidents
* Metrics persistence

## Current State

Local file storage.

## Future State

Move to:

* SQL DB
* NoSQL DB
* Blob storage

---

# 6. Observability Deployment

## Components

* LangSmith
* Metrics Logger
* Cost Tracker

## Deployment Model

External services + backend integration.

## Tracks

* Workflow traces
* Token usage
* Costs
* Execution time

---

# 7. Secrets Management

## Sensitive Values

```text
OPENAI_API_KEY

LANGSMITH_API_KEY

LANGCHAIN_PROJECT
```

## Current Approach

```text
.env
```

## Deployment Recommendation

Use:

* Environment Variables
* Secret Managers
* CI/CD Secrets

Never commit secrets to source control.

---

# 8. Docker Deployment Strategy

## Containers

```text
Frontend Container

Backend Container
```

## Orchestration

```text
docker-compose
```

## Execution

```bash
docker compose build

docker compose up
```

Benefits:

* Portable deployment
* Consistent environments
* Simplified setup

---

# 9. Networking

Frontend:

```text
Port 8501
```

Backend:

```text
Port 8000
```

Communication:

```text
Streamlit

↓

FastAPI REST API
```

---

# 10. Deployment Flow

Developer

↓

Clone Repository

↓

Create .env

↓

Install Docker

↓

docker compose up

↓

Application Ready

---

# 11. Current Deployment Scope

Implemented:

* Dockerized architecture
* Environment-driven configuration
* Local persistence
* Containerized services

Not Implemented:

* CI/CD pipelines
* Cloud hosting
* Autoscaling
* Kubernetes
* Managed databases

---

# 12. Future Deployment Roadmap

Phase 1:

Containerized Deployment

↓

Phase 2:

Cloud Hosting

↓

Phase 3:

Managed Storage

↓

Phase 4:

Enterprise Scale Deployment
