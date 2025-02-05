# main.py
# Entry point for your Python backend (FastAPI, Flask, etc.)

from fastapi import FastAPI
from .routes import chat
from .utils.config import settings
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI()

app.include_router(chat.router)

@app.get("/")
def read_root():
    logger.info("Root endpoint accessed")
    return {"message": "Welcome to the AWS Tutor API"}

@app.get("/config")
def get_config():
    return {
        "database_url": settings.DATABASE_URL,
        "vector_db_url": settings.VECTOR_DB_URL
    }

if __name__ == "__main__":
    print("Backend entry point. Implement your app logic here.")
