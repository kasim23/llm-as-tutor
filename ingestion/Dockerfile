# Dockerfile for ingestion job
FROM python:3.9-slim

WORKDIR /ingestion
COPY requirements.txt requirements.txt
RUN pip install --no-cache-dir -r requirements.txt
COPY . .
CMD ["python", "ingest.py"]
