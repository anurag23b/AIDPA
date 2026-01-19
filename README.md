**AIDPA — LLM-Assisted Backend for Structured Task Management**

AIDPA is a **backend-first personal assistant system** focused on converting **free-form user input into structured, validated task workflows** using controlled LLM integration.
The project explores how LLMs can be used as a **non-authoritative system component** within a reliable backend architecture.

This repository represents an **advanced prototype**, built to emphasize correctness, observability, and iteration rather than production scale.

**What the System Does**

Accepts natural-language user input

Converts it into structured task data using **LLM-assisted semantic parsing**

Validates outputs before persistence

Stores structured state separately from conversational context

Exposes functionality via REST APIs

LLMs are used **only for interpretation**, not for business logic or persistence decisions.

**What I Personally Owned End-to-End**

Backend API design and implementation using **FastAPI (async)**

LLM-assisted semantic parsing with **prompt-driven structured extraction**

Validation and guardrails to ensure deterministic downstream behavior

Data modeling and persistence using **PostgreSQL (structured state)** and **MongoDB (context)**

Containerized local deployments using **Docker**

CI workflows using **GitHub Actions**

Performance measurement and documentation of non-production assumptions

**Architecture Overview**

**Backend:** FastAPI (async), REST APIs

**LLM Integration:** Prompt-driven structured extraction (LangChain-style patterns)

**Datastores:** PostgreSQL (tasks), MongoDB (conversation context)

**Infra (local):** Docker, Minikube, NGINX Ingress

**CI:** GitHub Actions

Note: Kubernetes usage is limited to **local orchestration (Minikube)** and is not intended to represent production deployment.

**Design Principles**

Treat LLMs as **assistive components**, not sources of truth

Measure behavior instead of assuming scale

Maintain explicit prototype boundaries

Prefer simple, debuggable systems over over-engineered solutions

**What This Project Is NOT**

❌ Not a production GenAI system

❌ Not a RAG pipeline

❌ Not an agent framework

❌ Not a decentralized application

These choices are intentional to preserve clarity and correctness.

**Running Locally (Prototype Setup)**

The system is designed to run in a local Kubernetes environment for development and testing.

High-level setup:
- Start a local Kubernetes cluster using **Minikube**
- Enable **NGINX Ingress**
- Build backend and frontend Docker images locally
- Deploy services using Kubernetes manifests
- Access the application via a local ingress endpoint

Kubernetes usage is limited to **local orchestration (Minikube)** and is not intended to represent production deployment.

**Why This Exists**

This project was built to explore **how GenAI can be integrated responsibly into backend systems**, and to build strong intuition around **guardrails, validation, and system reliability** before scaling into more advanced GenAI workflows.
