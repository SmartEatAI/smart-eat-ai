from langchain.tools import tool

from app.core.config_ollama import vector_db

@tool
def buscar_en_base_datos(query: str):
    """Útil para buscar información específica sobre dietas, alimentos o nutrición."""
    docs = vector_db.similarity_search(query)
    return [{"content": doc.page_content, "metadata": doc.metadata} for doc in docs]
