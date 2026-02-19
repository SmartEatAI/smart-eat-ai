"""
API routes para gestión de planes semanales.
Incluye generación, consulta y modificación de planes alimenticios.
"""

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import Optional

from app.api.deps import get_current_user, get_db
from app.models.usuario import Usuario
from app.models.plan import Plan
from app.schemas.plan import (
    PlanSchema,
    GeneratePlanRequest,
    GeneratePlanResponse
)

router = APIRouter()


@router.get("/plans/active", response_model=PlanSchema, status_code=status.HTTP_200_OK)
async def get_active_plan(
    current_user: Usuario = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Obtiene el plan semanal activo del usuario.
    
    **Returns:**
    - Plan completo con todos los menús diarios y recetas
    """
    try:
        plan = db.query(Plan).filter(
            Plan.usuario_id == current_user.id,
            Plan.activo == True
        ).first()
        
        if not plan:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="No se encontró un plan activo. Genera uno nuevo."
            )
        
        # TODO: Cargar relaciones (menus -> comidas -> recetas)
        return plan
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error obteniendo plan: {str(e)}"
        )


@router.get("/plans/{plan_id}", response_model=PlanSchema, status_code=status.HTTP_200_OK)
async def get_plan_by_id(
    plan_id: int,
    current_user: Usuario = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Obtiene un plan específico por ID.
    
    **Args:**
    - plan_id: ID del plan
    
    **Returns:**
    - Plan completo con menús y recetas
    """
    try:
        plan = db.query(Plan).filter(
            Plan.id == plan_id,
            Plan.usuario_id == current_user.id
        ).first()
        
        if not plan:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Plan {plan_id} no encontrado"
            )
        
        # TODO: Cargar relaciones
        return plan
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error obteniendo plan: {str(e)}"
        )


@router.post("/plans/generate", response_model=GeneratePlanResponse, status_code=status.HTTP_201_CREATED)
async def generate_plan(
    request: GeneratePlanRequest,
    current_user: Usuario = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Genera un nuevo plan semanal para el usuario.
    
    Utiliza el perfil del usuario (calorías objetivo, restricciones, gustos)
    y el modelo KNN para seleccionar recetas optimizadas.
    
    **Args:**
    - calorias_objetivo: Calorías diarias objetivo (opcional, usa perfil si no se especifica)
    - num_dias: Número de días a generar (default 7)
    - preferencias: Preferencias adicionales
    
    **Returns:**
    - Plan generado completo
    """
    try:
        # TODO: Implementar lógica de generación de plan
        # 1. Obtener perfil del usuario
        # 2. Calcular distribución de macros por comida
        # 3. Usar KNN para seleccionar recetas que cumplan objetivos
        # 4. Crear Plan, MenuDiario, DetalleComida
        # 5. Marcar otros planes como inactivos
        
        raise HTTPException(
            status_code=status.HTTP_501_NOT_IMPLEMENTED,
            detail="Generación de planes aún no implementada. Próximamente disponible."
        )
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error generando plan: {str(e)}"
        )


@router.get("/plans", status_code=status.HTTP_200_OK)
async def list_user_plans(
    current_user: Usuario = Depends(get_current_user),
    db: Session = Depends(get_db),
    skip: int = 0,
    limit: int = 10
):
    """
    Lista todos los planes del usuario (histórico).
    
    **Args:**
    - skip: Número de registros a saltar
    - limit: Número máximo de planes a retornar
    
    **Returns:**
    - Lista de planes con información básica
    """
    try:
        planes = db.query(Plan).filter(
            Plan.usuario_id == current_user.id
        ).order_by(
            Plan.fecha_creacion.desc()
        ).offset(skip).limit(limit).all()
        
        total = db.query(Plan).filter(
            Plan.usuario_id == current_user.id
        ).count()
        
        return {
            "plans": planes,
            "total": total,
            "skip": skip,
            "limit": limit
        }
        
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error listando planes: {str(e)}"
        )
