from langchain_ollama import ChatOllama, OllamaEmbeddings
from langchain_chroma import Chroma
from app.config import settings

# Configuración para 8GB VRAM con Llama 3.1
# Valores aumentados para preservar contexto completo del plan nutricional
OLLAMA_CONFIG = {
    "model": settings.OLLAMA_MODEL,
    "base_url": settings.OLLAMA_BASE_URL,
    "temperature": 0,        # 0 para mejor tool calling
    "num_ctx": 16384,        # Contexto ampliado (de 8192)
    "num_predict": 4096,     # Respuestas más largas (de 2048)
}

# Inicialización del LLM con soporte para tools
llm = ChatOllama(**OLLAMA_CONFIG)

# Inicialización de RAG
embeddings = OllamaEmbeddings(
    model=settings.CHROMA_EMBEDDING_MODEL, 
    base_url=settings.OLLAMA_BASE_URL
)

vector_db = Chroma(
    persist_directory=settings.CHROMA_DB, 
    embedding_function=embeddings
)