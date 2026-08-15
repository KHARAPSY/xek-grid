# 🏗️ xek-grid

> **A layered, enterprise-grade LLM/RAG gateway and MLOps platform featuring dual-pass guardrails, multi-database state management, and continuous async evaluation.**

---

## 📐 Architecture Overview

`xek-grid` provides a structured, multi-layer architecture designed to safely bridge client requests with LLM providers while maintaining continuous telemetry, evaluation, and operational health.

```text
                        ┌─────────────────────┐
                        │       Client        │
                        │ Web / CLI / REST    │
                        └──────────┬──────────┘
                                   │
                                   ▼
                        ┌─────────────────────┐
                        │       FastAPI       │
                        │ API / Auth /        │
                        │ Request validation  │
                        └──────────┬──────────┘
                                   │
                           ┌───────▼───────┐
                           │  Guardrails   │
                           │ safety / schema│
                           │ PII / policies │
                           └───────┬───────┘
                                   │
                   ┌───────────────┼────────────────┐
                   │               │                │
                   ▼               ▼                ▼
              PostgreSQL         Redis          Vector DB
              users/data      cache/state      embeddings
                   │               │                │
                   └───────────────┼────────────────┘
                                   │
                                   ▼
                           ┌─────────────────┐
                           │   AI Service    │
                           │ RAG / Agent     │
                           │ orchestration   │
                           └────────┬────────┘
                                    │
                                    ▼
                               ┌───────────┐
                               │  OpenAI   │
                               └─────┬─────┘
                                     │
                                     ▼
                              Output Guardrails
                                     │
                                     ▼
                                  Response


       ┌───────────────────────────────────────────────────┐
       │                    MLOps Plane                    │
       │                                                   │
       │  MLflow → experiments / traces / evaluation       │
       │  Worker → async evaluation / ingestion            │
       │  Docker → reproducible environments               │
       │  Kubernetes → deployment / scaling                │
       │  CI/CD → test / build / deploy                    │
       │  Monitoring → latency / errors / quality          │
       └───────────────────────────────────────────────────┘

```

---

## 🏛️ Key Structural Layers

* **🛡️ Dual-Pass Guardrail Mesh:** Applies strict schema, PII filtering, and safety policies on incoming requests and outgoing LLM responses.
* **💾 Multi-DB Data Tier:** Combines **PostgreSQL** (relational user data), **Redis** (caching & state), and **Vector DB** (embeddings & retrieval) for fast, context-rich execution.
* **🤖 AI Service Orchestrator:** Manages flexible RAG flows, agent logic, and direct integration with upstream providers like OpenAI.
* **⚙️ Autonomous MLOps Plane:** Offloads evaluation, tracing, and data ingestion to background workers using **MLflow**, fully containerized via **Docker** and scalable on **Kubernetes**.

---
