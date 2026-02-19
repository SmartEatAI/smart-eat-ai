"""
LangChain Tools personalizadas para el agente de recomendación de recetas.
Cada tool realiza una operación específica: consultar KNN, obtener detalles de recetas,
actualizar planes, etc.
"""

from typing import Optional, Type, List
from pydantic import BaseModel, Field
from langchain.tools import BaseTool
from sqlalchemy.orm import Session

# TODO: Importar servicios y modelos cuando estén implementados
# from app.services.knn_service import KNNService
# from app.models.receta import Receta
# from app.models.detalle_comida import DetalleComida


class SearchSimilarRecipesInput(BaseModel):
    """Input schema para búsqueda de recetas similares"""
    receta_id: int = Field(..., description="ID de la receta de referencia")
    num_sugerencias: int = Field(default=5, description="Número de recetas similares a retornar")


class SearchSimilarRecipesTool(BaseTool):
    """Herramienta para buscar recetas nutricionalmente similares usando KNN"""
    
    name: str = "search_similar_recipes"
    description: str = (
        "Busca recetas nutricionalmente similares a una receta dada. "
        "Usa el modelo KNN entrenado para encontrar vecinos cercanos. "
        "Input: receta_id (int) y num_sugerencias (int, default=5). "
        "Output: Lista de recetas con sus distancias."
    )
    args_schema: Type[BaseModel] = SearchSimilarRecipesInput
    db_session: Session = None  # Inyectado en runtime
    
    def _run(self, receta_id: int, num_sugerencias: int = 5) -> str:
        """Ejecuta la búsqueda de recetas similares"""
        # TODO: Implementar con KNNService
        return f"Búsqueda de {num_sugerencias} recetas similares a {receta_id} - PENDIENTE IMPLEMENTAR"
    
    async def _arun(self, receta_id: int, num_sugerencias: int = 5) -> str:
        """Versión async (no implementada)"""
        raise NotImplementedError("Async no soportado aún")


class GetRecipeDetailsInput(BaseModel):
    """Input schema para obtener detalles de receta"""
    receta_id: int = Field(..., description="ID de la receta")


class GetRecipeDetailsTool(BaseTool):
    """Herramienta para obtener información completa de una receta"""
    
    name: str = "get_recipe_details"
    description: str = (
        "Obtiene todos los detalles de una receta específica incluyendo "
        "macronutrientes, micronutrientes, ingredientes e instrucciones. "
        "Input: receta_id (int). "
        "Output: Información completa de la receta en formato texto."
    )
    args_schema: Type[BaseModel] = GetRecipeDetailsInput
    db_session: Session = None
    
    def _run(self, receta_id: int) -> str:
        """Obtiene detalles de la receta"""
        # TODO: Implementar query a BD
        return f"Detalles de receta {receta_id} - PENDIENTE IMPLEMENTAR"
    
    async def _arun(self, receta_id: int) -> str:
        raise NotImplementedError("Async no soportado aún")


class GetUserPlanInput(BaseModel):
    """Input schema para obtener plan del usuario"""
    usuario_id: int = Field(..., description="ID del usuario")


class GetUserPlanTool(BaseTool):
    """Herramienta para obtener el plan semanal activo del usuario"""
    
    name: str = "get_user_plan"
    description: str = (
        "Obtiene el plan semanal activo de un usuario con todas las recetas asignadas. "
        "Input: usuario_id (int). "
        "Output: Plan semanal con menús diarios y recetas."
    )
    args_schema: Type[BaseModel] = GetUserPlanInput
    db_session: Session = None
    
    def _run(self, usuario_id: int) -> str:
        """Obtiene el plan activo del usuario"""
        # TODO: Implementar JOIN Plan -> MenuDiario -> DetalleComida -> Receta
        return f"Plan semanal de usuario {usuario_id} - PENDIENTE IMPLEMENTAR"
    
    async def _arun(self, usuario_id: int) -> str:
        raise NotImplementedError("Async no soportado aún")


class CompareNutritionalProfilesInput(BaseModel):
    """Input schema para comparar perfiles nutricionales"""
    receta_original_id: int = Field(..., description="ID de la receta original")
    receta_alternativa_id: int = Field(..., description="ID de la receta alternativa")


class CompareNutritionalProfilesTool(BaseTool):
    """Herramienta para comparar nutricionalmente dos recetas"""
    
    name: str = "compare_nutritional_profiles"
    description: str = (
        "Compara dos recetas y calcula diferencias porcentuales en macronutrientes. "
        "Input: receta_original_id (int), receta_alternativa_id (int). "
        "Output: Comparación detallada con diferencias en calorías, proteínas, etc."
    )
    args_schema: Type[BaseModel] = CompareNutritionalProfilesInput
    db_session: Session = None
    
    def _run(self, receta_original_id: int, receta_alternativa_id: int) -> str:
        """Compara dos recetas nutricionalmente"""
        # TODO: Implementar cálculo de diferencias porcentuales
        return f"Comparación entre {receta_original_id} y {receta_alternativa_id} - PENDIENTE IMPLEMENTAR"
    
    async def _arun(self, receta_original_id: int, receta_alternativa_id: int) -> str:
        raise NotImplementedError("Async no soportado aún")


class UpdateMealInPlanInput(BaseModel):
    """Input schema para actualizar comida en plan"""
    detalle_comida_id: int = Field(..., description="ID del detalle de comida a actualizar")
    nueva_receta_id: int = Field(..., description="ID de la nueva receta")


class UpdateMealInPlanTool(BaseTool):
    """Herramienta para reemplazar una receta en el plan del usuario"""
    
    name: str = "update_meal_in_plan"
    description: str = (
        "Actualiza una comida específica en el plan semanal del usuario. "
        "Reemplaza la receta actual por una nueva. "
        "Input: detalle_comida_id (int), nueva_receta_id (int). "
        "Output: Confirmación de actualización."
    )
    args_schema: Type[BaseModel] = UpdateMealInPlanInput
    db_session: Session = None
    
    def _run(self, detalle_comida_id: int, nueva_receta_id: int) -> str:
        """Actualiza la receta en el plan"""
        # TODO: Implementar UPDATE en DetalleComida
        # TODO: Registrar en LogRecomendacion
        return f"Actualizado detalle {detalle_comida_id} con receta {nueva_receta_id} - PENDIENTE IMPLEMENTAR"
    
    async def _arun(self, detalle_comida_id: int, nueva_receta_id: int) -> str:
        raise NotImplementedError("Async no soportado aún")
