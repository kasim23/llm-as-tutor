# LLM-Powered AWS Tutor

This project is an MVP demonstrating a Retrieval-Augmented Generation (RAG) approach
to building a chat-based AWS Tutor using GPT and AWS docs.

## Structure
- **backend**: Python-based REST API (FastAPI/Flask) containerized with Docker.
- **ingestion**: Scripts for scraping/embedding AWS docs and storing them in a vector DB.
- **frontend**: React (or Next.js) app for the chat UI, containerized with Docker.
- **k8s**: Kubernetes manifests for deploying on AWS EKS.
