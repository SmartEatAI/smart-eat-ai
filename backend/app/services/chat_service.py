"""
Servicio de chat V2 usando arquitectura mejorada con sesiones de Chat.
Compatible con diagrama ER: Chat → Mensaje → Sugerencia
"""

from typing import Optional, Dict, Any, List
from sqlalchemy.orm import Session, joinedload
from datetime import datetime
import logging

from app.models.chat import Chat
from app.models.mensaje import Mensaje, RolMensaje
from app.models.sugerencia import Sugerencia, EstadoSugerencia
from app.models.plan import Plan
from app.models.usuario import Usuario
from app.models.detalle_comida import DetalleComida
from app.models.receta import Receta

from app.schemas.chat import (
    ChatSchema,
    ChatCreate,
    MensajeSchema,
    SugerenciaSchema,
    ChatMessageResponse,
    ChatHistoryResponse,
    ListChatsResponse,
    RecipeCard,
    NutritionalComparison
)
from app.services.langchain_agent import LangChainAgentService

logger = logging.getLogger(__name__)


class ChatService:
    """Servicio para gestionar sesiones de chat y mensajes"""
    
    @staticmethod
    def get_or_create_chat(
        usuario_id: int,
        chat_id: Optional[int],
        db: Session,
        nombre: Optional[str] = None
    ) -> Chat:
        """
        Obtiene un chat existente o crea uno nuevo.
        
        Args:
            usuario_id: ID del usuario
            chat_id: ID del chat (None para crear uno nuevo)
            db: Sesión de base de datos
            nombre: Nombre del chat (para nuevos chats)
            
        Returns:
            Instancia de Chat
        """
        if chat_id:
            # Buscar chat existente
            chat = db.query(Chat).filter(
                Chat.id == chat_id,
                Chat.usuario_id == usuario_id
            ).first()
            
            if not chat:
                raise ValueError(f"Chat {chat_id} no encontrado para usuario {usuario_id}")
            
            return chat
        else:
            # Crear nuevo chat
            if not nombre:
                nombre = f"Chat {datetime.now().strftime('%Y-%m-%d %H:%M')}"
            
            nuevo_chat = Chat(
                usuario_id=usuario_id,
                nombre=nombre,
                activo=True
            )
            db.add(nuevo_chat)
            db.flush()
            
            logger.info(f"Nuevo chat creado: {nuevo_chat.id} para usuario {usuario_id}")
            return nuevo_chat
    
    @staticmethod
    def process_user_message(
        usuario_id: int,
        chat_id: Optional[int],
        mensaje_texto: str,
        db: Session,
        contexto_plan_id: Optional[int] = None
    ) -> ChatMessageResponse:
        """
        Procesa un mensaje del usuario a través del agente LangChain.
        
        Args:
            usuario_id: ID del usuario
            chat_id: ID del chat (None crea uno nuevo)
            mensaje_texto: Texto del mensaje
            db: Sesión de base de datos
            contexto_plan_id: ID del plan en contexto
            
        Returns:
            ChatMessageResponse con respuesta del agente
        """
        try:
            # Verificar usuario
            usuario = db.query(Usuario).filter(Usuario.id == usuario_id).first()
            if not usuario:
                raise ValueError(f"Usuario {usuario_id} no encontrado")
            
            # Obtener o crear chat
            chat = ChatService.get_or_create_chat(
                usuario_id=usuario_id,
                chat_id=chat_id,
                db=db
            )
            
            # Obtener plan activo si no viene en contexto
            if not contexto_plan_id:
                plan_activo = db.query(Plan).filter(
                    Plan.usuario_id == usuario_id,
                    Plan.activo == True
                ).first()
                if plan_activo:
                    contexto_plan_id = plan_activo.id
            
            # Guardar mensaje del usuario
            mensaje_user = Mensaje(
                chat_id=chat.id,
                texto=mensaje_texto,
                rol=RolMensaje.USER,
                contexto_plan_id=contexto_plan_id
            )
            db.add(mensaje_user)
            db.flush()
            
            # Ejecutar agente LangChain con historial del chat
            historial = ChatService._get_chat_history(chat.id, db)
            context = {'plan_id': contexto_plan_id} if contexto_plan_id else None
            
            agent_result = LangChainAgentService.run_agent(
                user_message=mensaje_texto,
                chat_history=historial,
                db_session=db,
                context=context
            )
            
            # Obtener respuesta del agente
            if agent_result.get("success"):
                respuesta_texto = agent_result.get("response", "Error procesando respuesta")
            else:
                respuesta_texto = f"Lo siento, ocurrió un error: {agent_result.get('error', 'Desconocido')}"
            
            # Guardar respuesta del asistente
            mensaje_assistant = Mensaje(
                chat_id=chat.id,
                texto=respuesta_texto,
                rol=RolMensaje.ASSISTANT,
                contexto_plan_id=contexto_plan_id
            )
            db.add(mensaje_assistant)
            db.commit()
            
            # TODO: Parsear respuesta del agente para detectar sugerencias
            sugerencia = None
            
            return ChatMessageResponse(
                chat_id=chat.id,
                mensaje_id=mensaje_assistant.id,
                respuesta=respuesta_texto,
                sugerencia=sugerencia,
                timestamp=mensaje_assistant.fecha_hora
            )
            
        except Exception as e:
            db.rollback()
            logger.error(f"Error procesando mensaje: {e}")
            raise
    
    @staticmethod
    def _get_chat_history(chat_id: int, db: Session, limit: int = 20) -> List[Dict[str, str]]:
        """
        Obtiene historial de mensajes del chat para contexto del agente.
        
        Args:
            chat_id: ID del chat
            db: Sesión de base de datos
            limit: Número máximo de mensajes
            
        Returns:
            Lista de mensajes en formato [{"role": "user", "content": "..."}]
        """
        mensajes = db.query(Mensaje).filter(
            Mensaje.chat_id == chat_id
        ).order_by(Mensaje.fecha_hora.desc()).limit(limit).all()
        
        # Invertir para orden cronológico
        mensajes.reverse()
        
        return [
            {
                "role": msg.rol.value,
                "content": msg.texto
            }
            for msg in mensajes
        ]
    
    @staticmethod
    def get_chat_history(
        usuario_id: int,
        chat_id: int,
        db: Session
    ) -> ChatHistoryResponse:
        """
        Obtiene el historial completo de un chat con mensajes y sugerencias.
        
        Args:
            usuario_id: ID del usuario
            chat_id: ID del chat
            db: Sesión de base de datos
            
        Returns:
            ChatHistoryResponse con chat, mensajes y sugerencias
        """
        # Buscar chat
        chat = db.query(Chat).filter(
            Chat.id == chat_id,
            Chat.usuario_id == usuario_id
        ).first()
        
        if not chat:
            raise ValueError(f"Chat {chat_id} no encontrado")
        
        # Obtener mensajes
        mensajes = db.query(Mensaje).filter(
            Mensaje.chat_id == chat_id
        ).order_by(Mensaje.fecha_hora).all()
        
        # Obtener sugerencias
        sugerencias = db.query(Sugerencia).filter(
            Sugerencia.chat_id == chat_id
        ).order_by(Sugerencia.fecha_hora).all()
        
        return ChatHistoryResponse(
            chat=ChatSchema.from_orm(chat),
            mensajes=[MensajeSchema.from_orm(m) for m in mensajes],
            sugerencias=[SugerenciaSchema.from_orm(s) for s in sugerencias]
        )
    
    @staticmethod
    def list_user_chats(
        usuario_id: int,
        db: Session,
        activo_only: bool = False,
        limit: int = 50
    ) -> ListChatsResponse:
        """
        Lista todos los chats de un usuario.
        
        Args:
            usuario_id: ID del usuario
            db: Sesión de base de datos
            activo_only: Filtrar solo chats activos
            limit: Número máximo de chats
            
        Returns:
            ListChatsResponse con lista de chats
        """
        query = db.query(Chat).filter(Chat.usuario_id == usuario_id)
        
        if activo_only:
            query = query.filter(Chat.activo == True)
        
        chats = query.order_by(Chat.fecha_creacion.desc()).limit(limit).all()
        total = query.count()
        
        return ListChatsResponse(
            chats=[ChatSchema.from_orm(c) for c in chats],
            total=total
        )
    
    @staticmethod
    def deactivate_chat(
        usuario_id: int,
        chat_id: int,
        db: Session
    ) -> bool:
        """
        Desactiva un chat (soft delete).
        
        Args:
            usuario_id: ID del usuario
            chat_id: ID del chat
            db: Sesión de base de datos
            
        Returns:
            True si se desactivó correctamente
        """
        chat = db.query(Chat).filter(
            Chat.id == chat_id,
            Chat.usuario_id == usuario_id
        ).first()
        
        if not chat:
            raise ValueError(f"Chat {chat_id} no encontrado")
        
        chat.activo = False
        db.commit()
        
        logger.info(f"Chat {chat_id} desactivado")
        return True
    
    @staticmethod
    def _build_recipe_card(receta: Receta) -> RecipeCard:
        """Helper para construir RecipeCard desde modelo Receta"""
        return RecipeCard(
            id=receta.id,
            name=receta.nombre,
            calories=receta.calorias,
            protein=receta.proteinas,
            carbs=receta.carbohidratos,
            fat=receta.grasas,
            image_url=receta.url_imagen,
            recipe_url=receta.url_receta
        )
    
    @staticmethod
    def _build_nutritional_comparison(
        receta_original: Receta,
        receta_nueva: Receta
    ) -> NutritionalComparison:
        """Helper para construir comparación nutricional"""
        def calc_pct_diff(original, nuevo):
            if original == 0:
                return 0.0
            return ((nuevo - original) / original) * 100
        
        return NutritionalComparison(
            calories_diff_pct=calc_pct_diff(receta_original.calorias, receta_nueva.calorias),
            protein_diff_pct=calc_pct_diff(receta_original.proteinas, receta_nueva.proteinas),
            carbs_diff_pct=calc_pct_diff(receta_original.carbohidratos, receta_nueva.carbohidratos),
            fat_diff_pct=calc_pct_diff(receta_original.grasas, receta_nueva.grasas),
            original_calories=receta_original.calorias,
            new_calories=receta_nueva.calorias,
            original_protein=receta_original.proteinas,
            new_protein=receta_nueva.proteinas,
            original_carbs=receta_original.carbohidratos,
            new_carbs=receta_nueva.carbohidratos,
            original_fat=receta_original.grasas,
            new_fat=receta_nueva.grasas
        )
