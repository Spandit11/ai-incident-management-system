# Architecture Decisions

## 1. Why LangGraph?

Decision:

Use LangGraph orchestration.

Reason:

* Multi-agent workflow support
* Stateful execution
* Easy routing
* Future expansion support

Tradeoff:

* More complexity than sequential workflows

---

## 2. Why Supervisor Pattern?

Decision:

Supervisor controls workflow routing.

Reason:

* Dynamic routing
* Future extensibility
* Better orchestration

Tradeoff:

* Additional node complexity

---

## 3. Why FastAPI?

Decision:

Use FastAPI backend.

Reason:

* Lightweight APIs
* Async support
* Easy deployment
* Swagger support

Tradeoff:

* Additional service layer

---

## 4. Why Streamlit?

Decision:

Use Streamlit frontend.

Reason:

* Fast prototyping
* Quick demo creation
* Low frontend effort

Tradeoff:

* Less flexible than React/Angular

---

## 5. Why ChromaDB?

Decision:

Use ChromaDB.

Reason:

* Lightweight vector store
* Easy local setup
* Good for POC/demo

Tradeoff:

* Not enterprise scale

---

## 6. Why Retrieval-Augmented Generation?

Decision:

Use RAG for incident retrieval.

Reason:

* Historical context
* Better RCA quality
* Reusable knowledge

Tradeoff:

* Retrieval quality affects results

---

## 7. Why Guardrails?

Decision:

Input validation before workflow.

Reason:

* Prevent invalid input
* Reject very small or non-log-like content
* Detect excessive special characters
* Block suspicious payload patterns before the AI workflow
* Stable execution
* Better user experience

Tradeoff:

* Additional validation logic
* Some unusual but valid logs may require future allowlist tuning

---

## 8. Why Retry Policies?

Decision:

Retry external failures.

Reason:

* Improve resiliency
* Handle transient issues

Tradeoff:

* Slight latency increase

---

## 9. Why Centralized Prompts?

Decision:

Move prompts to separate files.

Reason:

* Maintainability
* Easier tuning
* Cleaner code

Tradeoff:

* Additional folder structure

---

## 10. Why No Chunking?

Decision:

Avoid chunking for current scope.

Reason:

* File restrictions already exist
* Faster implementation
* Lower complexity

Tradeoff:

* Large logs may lose context

Future:

Introduce chunk summarization.

---

## 11. Why Single Incident Context Processing?

Decision:

Process uploaded logs as one primary incident context.

Current State:

* Optimized for dominant incident detection
* Generates consolidated RCA
* Works best for one primary failure pattern

Tradeoff:

* Multiple independent exceptions in the same log may be blended into one RCA

Future State:

Multi-Incident Intelligence Engine.

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

## 12. Why Simple Reranking?

Decision:

Distance-based reranking.

Reason:

* Low complexity
* Quick improvement

Tradeoff:

* Less accurate than advanced rerankers

---

## 13. Why Docker?

Decision:

Containerized deployment.

Reason:

* Consistent environments
* Easy sharing
* Simplified deployment

Tradeoff:

* Additional setup

---

## 14. Why Observability?

Decision:

Execution metrics and tracing.

Reason:

* Debugging
* Cost visibility
* Workflow transparency

Tradeoff:

* More telemetry storage

---

# Future Roadmap

* Cloud deployment
* Redis memory
* Advanced reranking
* Multi-agent scaling
* Chunking
* Production hardening
