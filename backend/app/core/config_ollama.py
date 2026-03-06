"""
Configuración del LLM (Groq) y embeddings para el agente nutricional.

Groq se usa para inferencia LLM (llama-3.1-8b-instant).
Ollama se mantiene solo para embeddings locales (Chroma RAG).
"""
import logging
from functools import lru_cache
from langchain_ollama import OllamaEmbeddings
from langchain_chroma import Chroma
from langchain_groq import ChatGroq
from groq import RateLimitError, APIConnectionError, APIStatusError
from app.config import settings

logger = logging.getLogger(__name__)


# ============================================================
# CONFIGURACIÓN DE GROQ (LLM)
# ============================================================
GROQ_CONFIG = {
    "model": settings.GROQ_MODEL,  # llama-3.1-8b-instant: 128K tokens de contexto
    "temperature": 0,
    "max_tokens": 4096,
    "timeout": 60,
    "max_retries": 3,  # Reintentos automáticos para rate limits
    "api_key": settings.GROQ_API_KEY,
}


def _validate_groq_config() -> None:
    """Valida que la configuración de Groq esté completa."""
    if not settings.GROQ_API_KEY:
        raise ValueError(
            "GROQ_API_KEY no está configurada. "
            "Añádela al archivo .env o como variable de entorno."
        )
    if not settings.GROQ_MODEL:
        logger.warning("GROQ_MODEL no configurado, usando valor por defecto: llama-3.1-8b-instant")


@lru_cache(maxsize=1)
def get_llm() -> ChatGroq:
    """
    Inicializa y retorna el LLM de Groq (singleton).
    
    Maneja errores comunes:
    - RateLimitError: Se excedió el límite de peticiones
    - APIConnectionError: No se puede conectar a Groq
    - APIStatusError: Error en la API de Groq
    """
    _validate_groq_config()
    try:
        llm = ChatGroq(**GROQ_CONFIG)
        logger.info(f"✅ Groq LLM inicializado: {settings.GROQ_MODEL}")
        return llm
    except (RateLimitError, APIConnectionError, APIStatusError) as e:
        logger.error(f"❌ Error inicializando Groq: {e}")
        raise


# Instancia singleton para compatibilidad con código existente
llm = get_llm()


# ============================================================
# CONFIGURACIÓN DE EMBEDDINGS (Ollama local)
# ============================================================
@lru_cache(maxsize=1)
def get_embeddings() -> OllamaEmbeddings:
    """Inicializa embeddings de Ollama (para RAG con Chroma)."""
    return OllamaEmbeddings(
        model=settings.CHROMA_EMBEDDING_MODEL,
        base_url=settings.OLLAMA_BASE_URL
    )


@lru_cache(maxsize=1)
def get_vector_db() -> Chroma:
    """Inicializa la base de datos vectorial Chroma."""
    return Chroma(
        persist_directory=settings.CHROMA_DB,
        embedding_function=get_embeddings()
    )


# Instancias singleton para compatibilidad
embeddings = get_embeddings()
vector_db = get_vector_db()