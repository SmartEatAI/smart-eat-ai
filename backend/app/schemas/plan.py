from pydantic import BaseModel, Field
from typing import List, Optional
from datetime import datetime, time
from .chat import RecipeCard


class MealDetailSchema(BaseModel):
    """Detalle de una comida específica"""
    id: int
    receta: RecipeCard
    horario: time
    tipo_comida: str = Field(..., description="desayuno, almuerzo, cena, snack")
    estado: Optional[str] = None
    
    class Config:
        from_attributes = True


class DailyMenuSchema(BaseModel):
    """Menú de un día específico"""
    id: int
    dia_semana: int = Field(..., ge=1, le=7, description="1=Lunes, 7=Domingo")
    comidas: List[MealDetailSchema]
    
    class Config:
        from_attributes = True


class PlanSchema(BaseModel):
    """Plan semanal completo del usuario"""
    id: int
    usuario_id: int
    fecha_creacion: datetime
    fecha_modificacion: Optional[datetime] = None
    activo: bool
    menus: List[DailyMenuSchema]
    
    class Config:
        from_attributes = True


class GeneratePlanRequest(BaseModel):
    """Request para generar un nuevo plan"""
    calorias_objetivo: Optional[float] = Field(None, description="Calorías diarias objetivo")
    num_dias: int = Field(7, ge=1, le=14, description="Días a generar (default 7)")
    preferencias: Optional[dict] = Field(None, description="Preferencias adicionales")


class GeneratePlanResponse(BaseModel):
    """Response con el plan generado"""
    plan: PlanSchema
    success: bool
    message: str
