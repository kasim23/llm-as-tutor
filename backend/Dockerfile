# Dockerfile for the backend
FROM python:3.9-slim

WORKDIR /app
COPY requirements.txt requirements.txt
RUN pip install --no-cache-dir -r requirements.txt
COPY . .

# Expose the port (e.g., 8000 for FastAPI/uvicorn)
EXPOSE 8000

# Adjust the CMD as needed for your framework, e.g., uvicorn
CMD ["python", "main.py"]
