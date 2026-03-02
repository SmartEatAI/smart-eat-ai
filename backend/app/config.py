import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

class Settings:
    # Database
    DATABASE_URL: str = os.getenv("DATABASE_URL")
    CHROMA_DB: str = os.getenv("CHROMA_DB")
    CHROMA_EMBEDDING_MODEL: str = os.getenv("CHROMA_EMBEDDING_MODEL")
    
    # JWT
    SECRET_KEY: str = os.getenv("SECRET_KEY")
    ALGORITHM: str = os.getenv("ALGORITHM", "HS256")
    ACCESS_TOKEN_EXPIRE_MINUTES: int = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", "3000"))
    
    # Backend
    BACKEND_URL: str = os.getenv("BACKEND_URL", "http://localhost:8000")
    FRONTEND_URL: str = os.getenv("FRONTEND_URL", "http://localhost:3000")
    
    # OLLAMA
    OLLAMA_MODEL: str = os.getenv("OLLAMA_MODEL")
    OLLAMA_BASE_URL: str = os.getenv("OLLAMA_BASE_URL")

    def __init__(self):
        if not self.DATABASE_URL:
            raise ValueError("DATABASE_URL is not set")
        if not self.SECRET_KEY:
            raise ValueError("SECRET_KEY is not set")

settings = Settings()