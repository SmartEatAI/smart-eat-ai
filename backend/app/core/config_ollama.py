from langchain_ollama import ChatOllama, OllamaEmbeddings
from langchain_chroma import Chroma
from langchain_groq import ChatGroq
from langchain_core.messages import HumanMessage
from app.config import settings


GROQ_CONFIG = {
    "model": settings.GROQ_MODEL,  # 32K tokens de contexto
    "temperature": 0,
    "max_tokens": 4096,  # Respuestas largas
    "timeout": 60,
    "max_retries": 2,
    "api_key": settings.GROQ_API_KEY,
}

# Inicialización del LLM con Groq
llm = ChatGroq(**GROQ_CONFIG)
print("✅ Groq inicializado correctamente")

try:
    # Probar una llamada simple
    response = llm.invoke([HumanMessage(content="Hola, ¿cómo estás?")])
    print(f"✅ Respuesta recibida: {response.content[:50]}...")
    
except Exception as e:
    print(f"❌ Error: {str(e)}")
    import traceback
    traceback.print_exc()


# Inicialización de RAG
embeddings = OllamaEmbeddings(
    model=settings.CHROMA_EMBEDDING_MODEL, 
    base_url=settings.OLLAMA_BASE_URL
)

vector_db = Chroma(
    persist_directory=settings.CHROMA_DB, 
    embedding_function=embeddings
)