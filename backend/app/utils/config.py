from pydantic import BaseSettings

class Settings(BaseSettings):
    DATABASE_URL: str
    OPENAI_API_KEY: str
    VECTOR_DB_URL: str

    class Config:
        env_file = ".env"

settings = Settings()
