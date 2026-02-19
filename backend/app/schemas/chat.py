"""
Schemas actualizados para el sistema de chat según diagrama ER.
Versión mejorada con sesiones de chat y sugerencias.
"""

from pydantic import BaseModel, Field
from typing import Optional, List
from datetime import datetime
from enum import Enum


# ============================================================================
# ENUMS
# ============================================================================

class RolMensajeEnum(str, Enum):
    """Rol del mensaje"""
    USER = "user"
    ASSISTANT = "assistant"
    SYSTEM = "system"


class EstadoSugerenciaEnum(str, Enum):
    """Estado de una sugerencia"""
    PENDIENTE = "pendiente"
    ACEPTADA = "aceptada"
    RECHAZADA = "rechazada"


# ============================================================================
# CHAT SCHEMAS
# ============================================================================

class ChatCreate(BaseModel):
    """Schema para crear una nueva sesión de chat"""
    nombre: Optional[str] = Field(None, description="Nombre descriptivo del chat")


class ChatSchema(BaseModel):
    """Schema de una sesión de chat"""
    id: int
    nombre: Optional[str]
    usuario_id: int
    fecha_creacion: datetime
    activo: bool
    
    class Config:
        from_attributes = True


# ============================================================================
# MENSAJE SCHEMAS
# ============================================================================

class MensajeCreate(BaseModel):
    """Schema para crear un mensaje"""
    texto: str = Field(..., min_length=1, max_length=5000)
    contexto_plan_id: Optional[int] = None


class MensajeSchema(BaseModel):
    """Schema de un mensaje"""
    id: int
    chat_id: int
    texto: str
    rol: RolMensajeEnum
    fecha_hora: datetime
    
    class Config:
        from_attributes = True


# ============================================================================
# SUGERENCIA SCHEMAS (RecipeCard para frontend)
# ============================================================================

class RecipeCard(BaseModel):
    """Card con información básica de una receta"""
    id: int
    name: str
    calories: int
    protein: int
    carbs: int
    fat: int
    image_url: Optional[str] = None
    recipe_url: Optional[str] = None
    
    class Config:
        from_attributes = True


class NutritionalComparison(BaseModel):
    """Comparación nutricional entre dos recetas"""
    calories_diff_pct: float
    protein_diff_pct: float
    carbs_diff_pct: float
    fat_diff_pct: float
    
    original_calories: int
    new_calories: int
    original_protein: int
    new_protein: int
    original_carbs: int
    new_carbs: int
    original_fat: int
    new_fat: int


class SugerenciaCreate(BaseModel):
    """Schema para crear una sugerencia"""
    detalle_comida_id: int
    nueva_receta_id: int
    receta_original_id: Optional[int] = None
    distancia_knn: Optional[float] = None
    justificacion: Optional[str] = None


class SugerenciaSchema(BaseModel):
    """Schema completo de una sugerencia"""
    id: int
    chat_id: int
    detalle_comida_id: int
    nueva_receta_id: int
    estado: EstadoSugerenciaEnum
    fecha_hora: datetime
    distancia_knn: Optional[float]
    justificacion: Optional[str]
    
    # Datos enriquecidos para frontend
    receta_original: Optional[RecipeCard] = None
    receta_nueva: Optional[RecipeCard] = None
    comparacion: Optional[NutritionalComparison] = None
    
    class Config:
        from_attributes = True


# ============================================================================
# REQUEST/RESPONSE SCHEMAS
# ============================================================================

class ChatMessageRequest(BaseModel):
    """Request para enviar mensaje al chat"""
    chat_id: Optional[int] = Field(None, description="ID del chat. Si es None, crea uno nuevo")
    mensaje: str = Field(..., min_length=1, max_length=5000)
    contexto_plan_id: Optional[int] = None


class ChatMessageResponse(BaseModel):
    """Response del agente al mensaje del usuario"""
    chat_id: int
    mensaje_id: int
    respuesta: str
    sugerencia: Optional[SugerenciaSchema] = None
    timestamp: datetime


class AceptarSugerenciaRequest(BaseModel):
    """Request para aceptar una sugerencia"""
    pass  # No requiere body adicional, el ID viene en la URL


class AceptarSugerenciaResponse(BaseModel):
    """Response al aceptar sugerencia"""
    success: bool
    message: str
    plan_actualizado_id: int
    detalle_comida_id: int


class RechazarSugerenciaRequest(BaseModel):
    """Request para rechazar una sugerencia"""
    feedback: Optional[str] = Field(None, description="Razón del rechazo")


class RechazarSugerenciaResponse(BaseModel):
    """Response al rechazar sugerencia"""
    success: bool
    message: str


class ChatHistoryResponse(BaseModel):
    """Response con historial de un chat"""
    chat: ChatSchema
    mensajes: List[MensajeSchema]
    sugerencias: List[SugerenciaSchema]


class ListChatsResponse(BaseModel):
    """Response con lista de chats del usuario"""
    chats: List[ChatSchema]
    total: int
