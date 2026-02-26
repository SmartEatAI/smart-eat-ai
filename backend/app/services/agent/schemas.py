from pydantic import BaseModel
from typing import Optional, Dict, Any

class AgentResponse(BaseModel):
    text: str  # El mensaje que leerá el usuario
    suggestion: Optional[Dict[str, Any]] = None  # Objeto con IDs de recetas/detalles si hay cambio