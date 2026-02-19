"""DEPRECATED: Use chat_v2.py para nueva arquitectura con sesiones de Chat.
Este archivo se mantiene por compatibilidad temporal con rutas antiguas."""

from pydantic import BaseModel, Field
from typing import Optional, Dict, Any
from datetime import datetime


class RecipeCard(BaseModel):
    """Card con información básica de una receta"""
    id: int
    name: str
    calories: float
    protein: float
    carbs: float
    fat: float
    image_url: Optional[str] = None
    recipe_url: Optional[str] = None  # URL para ver detalles completos de preparación
    
    class Config:
        from_attributes = True


class NutritionalComparison(BaseModel):
    """Comparación nutricional entre dos recetas"""
    calories_diff_pct: float = Field(..., description="Diferencia porcentual de calorías")
    protein_diff_pct: float = Field(..., description="Diferencia porcentual de proteínas")
    carbs_diff_pct: float = Field(..., description="Diferencia porcentual de carbohidratos")
    fat_diff_pct: float = Field(..., description="Diferencia porcentual de grasas")
    
    # Valores absolutos para referencia
    original_calories: float
    new_calories: float
    original_protein: float
    new_protein: float


class RecipeRecommendation(BaseModel):
    """Estructura completa de una recomendación de receta"""
    recommendation_id: int = Field(..., description="ID del log de recomendación para tracking")
    original: RecipeCard
    alternative: RecipeCard
    comparison: NutritionalComparison
    explanation: str = Field(..., description="Explicación en lenguaje natural de por qué se recomienda")
    knn_distance: float = Field(..., description="Distancia en el espacio KNN")
    confidence_score: Optional[float] = Field(None, description="Score de confianza 0-1")


class ChatMessageRequest(BaseModel):
    """Request del usuario en el chat"""
    message: str = Field(..., min_length=1, max_length=1000)
    context: Optional[Dict[str, Any]] = Field(
        None, 
        description="Contexto adicional: plan_id, dia_semana, tipo_comida, etc."
    )


class ChatMessageResponse(BaseModel):
    """Respuesta del agente al usuario"""
    reply: str = Field(..., description="Mensaje de texto del asistente")
    recommendation: Optional[RecipeRecommendation] = Field(
        None,
        description="Recomendación de receta (si aplica)"
    )
    conversation_id: int = Field(..., description="ID de la conversación guardada")
    timestamp: datetime


class AcceptRecommendationRequest(BaseModel):
    """Request para aceptar una recomendación"""
    detalle_comida_id: Optional[int] = Field(
        None,
        description="ID del detalle de comida a reemplazar (si no viene en contexto)"
    )


class AcceptRecommendationResponse(BaseModel):
    """Response al aceptar una recomendación"""
    success: bool
    message: str
    updated_plan_id: int
    updated_meal_id: int


class RejectRecommendationRequest(BaseModel):
    """Request para rechazar una recomendación"""
    feedback: Optional[str] = Field(None, description="Razón del rechazo (opcional)")


class RejectRecommendationResponse(BaseModel):
    """Response al rechazar una recomendación"""
    success: bool
    message: str
