from langchain_ollama import ChatOllama, OllamaEmbeddings
from langchain_community.vectorstores import Chroma
from app.config import settings

# Inicialización del LLM con soporte para tools
llm = ChatOllama(
    model=settings.OLLAMA_MODEL,
    base_url=settings.OLLAMA_BASE_URL,
    temperature=0
)

# Inicialización de RAG
embeddings = OllamaEmbeddings(
    model=settings.CHROMA_EMBEDDING_MODEL, 
    base_url=settings.OLLAMA_BASE_URL
)

vector_db = Chroma(
    persist_directory=settings.CHROMA_DB, 
    embedding_function=embeddings
)