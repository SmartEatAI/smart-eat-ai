"""
API routes V2 para el sistema de chat mejorado.
Usa arquitectura de sesiones: Chat → Mensaje → Sugerencia
"""

from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session
from typing import Optional

from app.api.deps import get_current_user, get_db
from app.models.usuario import Usuario
from app.schemas.chat import (
    ChatCreate,
    ChatSchema,
    ChatMessageRequest,
    ChatMessageResponse,
    AceptarSugerenciaResponse,
    RechazarSugerenciaRequest,
    RechazarSugerenciaResponse,
    ChatHistoryResponse,
    ListChatsResponse,
    SugerenciaSchema
)
from app.services.chat_service import ChatService
from app.services.sugerencia_service import SugerenciaService

router = APIRouter()


# ============================================================================
# CHAT ENDPOINTS
# ============================================================================

@router.post("/chats", response_model=ChatSchema, status_code=status.HTTP_201_CREATED)
async def create_chat(
    request: ChatCreate,
    current_user: Usuario = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Crea una nueva sesión de chat.
    
    **Args:**
    - nombre: Nombre descriptivo del chat (opcional)
    
    **Returns:**
    - ChatSchema con datos del chat creado
    """
    try:
        chat = ChatService.get_or_create_chat(
            usuario_id=current_user.id,
            chat_id=None,
            db=db,
            nombre=request.nombre
        )
        db.commit()
        return ChatSchema.from_orm(chat)
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error creando chat: {str(e)}"
        )


@router.get("/chats", response_model=ListChatsResponse, status_code=status.HTTP_200_OK)
async def list_chats(
    activo_only: bool = Query(False, description="Filtrar solo chats activos"),
    limit: int = Query(50, ge=1, le=100, description="Límite de resultados"),
    current_user: Usuario = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Lista todos los chats del usuario.
    
    **Query Params:**
    - activo_only: Filtrar solo chats activos (default: False)
    - limit: Número máximo de chats (default: 50)
    
    **Returns:**
    - Lista de chats del usuario
    """
    try:
        return ChatService.list_user_chats(
            usuario_id=current_user.id,
            db=db,
            activo_only=activo_only,
            limit=limit
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error listando chats: {str(e)}"
        )


@router.get("/chats/{chat_id}", response_model=ChatHistoryResponse, status_code=status.HTTP_200_OK)
async def get_chat_history(
    chat_id: int,
    current_user: Usuario = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Obtiene el historial completo de un chat con mensajes y sugerencias.
    
    **Args:**
    - chat_id: ID del chat
    
    **Returns:**
    - Chat con mensajes y sugerencias ordenados cronológicamente
    """
    try:
        return ChatService.get_chat_history(
            usuario_id=current_user.id,
            chat_id=chat_id,
            db=db
        )
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(e)
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error obteniendo historial: {str(e)}"
        )


@router.delete("/chats/{chat_id}", status_code=status.HTTP_204_NO_CONTENT)
async def deactivate_chat(
    chat_id: int,
    current_user: Usuario = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Desactiva un chat (soft delete).
    
    **Args:**
    - chat_id: ID del chat a desactivar
    """
    try:
        ChatService.deactivate_chat(
            usuario_id=current_user.id,
            chat_id=chat_id,
            db=db
        )
        return None
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(e)
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error desactivando chat: {str(e)}"
        )


# ============================================================================
# MENSAJE ENDPOINTS
# ============================================================================

@router.post("/chat", response_model=ChatMessageResponse, status_code=status.HTTP_200_OK)
async def send_message(
    request: ChatMessageRequest,
    current_user: Usuario = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Envía un mensaje al agente conversacional.
    
    El agente procesará el mensaje usando LangChain, consultará el modelo KNN
    si es necesario, y retornará una respuesta que puede incluir una sugerencia.
    
    **Args:**
    - chat_id: ID del chat (null para crear uno nuevo)
    - mensaje: Texto del mensaje
    - contexto_plan_id: ID del plan en contexto (opcional)
    
    **Returns:**
    - Respuesta del agente con posible sugerencia de receta
    """
    try:
        response = ChatService.process_user_message(
            usuario_id=current_user.id,
            chat_id=request.chat_id,
            mensaje_texto=request.mensaje,
            db=db,
            contexto_plan_id=request.contexto_plan_id
        )
        return response
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error procesando mensaje: {str(e)}"
        )


# ============================================================================
# SUGERENCIA ENDPOINTS
# ============================================================================

@router.get("/sugerencias/{sugerencia_id}", response_model=SugerenciaSchema, status_code=status.HTTP_200_OK)
async def get_sugerencia(
    sugerencia_id: int,
    current_user: Usuario = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Obtiene los detalles de una sugerencia con datos enriquecidos.
    
    **Args:**
    - sugerencia_id: ID de la sugerencia
    
    **Returns:**
    - Sugerencia con recetas y comparación nutricional
    """
    try:
        return SugerenciaService.get_sugerencia_enriquecida(
            sugerencia_id=sugerencia_id,
            db=db
        )
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(e)
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error obteniendo sugerencia: {str(e)}"
        )


@router.post(
    "/sugerencias/{sugerencia_id}/aceptar",
    response_model=AceptarSugerenciaResponse,
    status_code=status.HTTP_200_OK
)
async def aceptar_sugerencia(
    sugerencia_id: int,
    current_user: Usuario = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Acepta una sugerencia de receta y actualiza el plan del usuario.
    
    Esto modifica el DetalleComida correspondiente y actualiza la fecha
    de modificación del Plan.
    
    **Args:**
    - sugerencia_id: ID de la sugerencia
    
    **Returns:**
    - Confirmación con IDs del plan y comida actualizados
    """
    try:
        response = SugerenciaService.aceptar_sugerencia(
            usuario_id=current_user.id,
            sugerencia_id=sugerencia_id,
            db=db
        )
        return response
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(e)
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error aceptando sugerencia: {str(e)}"
        )


@router.post(
    "/sugerencias/{sugerencia_id}/rechazar",
    response_model=RechazarSugerenciaResponse,
    status_code=status.HTTP_200_OK
)
async def rechazar_sugerencia(
    sugerencia_id: int,
    request: RechazarSugerenciaRequest = None,
    current_user: Usuario = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Rechaza una sugerencia de receta.
    
    Opcionalmente registra el feedback del usuario para mejorar futuras
    recomendaciones.
    
    **Args:**
    - sugerencia_id: ID de la sugerencia
    - feedback: Razón del rechazo (opcional)
    
    **Returns:**
    - Confirmación del rechazo
    """
    try:
        feedback = request.feedback if request else None
        
        response = SugerenciaService.rechazar_sugerencia(
            usuario_id=current_user.id,
            sugerencia_id=sugerencia_id,
            db=db,
            feedback=feedback
        )
        return response
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(e)
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error rechazando sugerencia: {str(e)}"
        )
