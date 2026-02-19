"""
Servicio para gestión de sugerencias de recetas.
Maneja creación, aceptación y rechazo de sugerencias.
"""

from typing import Optional
from sqlalchemy.orm import Session
from datetime import datetime
import logging

from app.models.sugerencia import Sugerencia, EstadoSugerencia
from app.models.detalle_comida import DetalleComida
from app.models.receta import Receta
from app.models.plan import Plan
from app.models.chat import Chat

from app.schemas.chat import (
    SugerenciaSchema,
    SugerenciaCreate,
    AceptarSugerenciaResponse,
    RechazarSugerenciaResponse,
    RecipeCard,
    NutritionalComparison
)

logger = logging.getLogger(__name__)


class SugerenciaService:
    """Servicio para gestionar sugerencias de recetas"""
    
    @staticmethod
    def create_sugerencia(
        chat_id: int,
        detalle_comida_id: int,
        nueva_receta_id: int,
        db: Session,
        receta_original_id: Optional[int] = None,
        distancia_knn: Optional[float] = None,
        justificacion: Optional[str] = None,
        modelo_version: Optional[str] = None
    ) -> Sugerencia:
        """
        Crea una nueva sugerencia de receta.
        
        Args:
            chat_id: ID del chat
            detalle_comida_id: ID del detalle de comida a modificar
            nueva_receta_id: ID de la receta sugerida
            db: Sesión de base de datos
            receta_original_id: ID de la receta original (opcional)
            distancia_knn: Distancia KNN de similitud
            justificacion: Explicación de la sugerencia
            modelo_version: Versión del modelo KNN usado
            
        Returns:
            Sugerencia creada
        """
        # Verificar que el chat existe
        chat = db.query(Chat).filter(Chat.id == chat_id).first()
        if not chat:
            raise ValueError(f"Chat {chat_id} no encontrado")
        
        # Verificar que el detalle_comida existe
        detalle = db.query(DetalleComida).filter(
            DetalleComida.id == detalle_comida_id
        ).first()
        if not detalle:
            raise ValueError(f"DetalleComida {detalle_comida_id} no encontrado")
        
        # Verificar que la nueva receta existe
        nueva_receta = db.query(Receta).filter(
            Receta.id == nueva_receta_id
        ).first()
        if not nueva_receta:
            raise ValueError(f"Receta {nueva_receta_id} no encontrada")
        
        # Si no se especificó receta_original_id, usar la actual del detalle
        if not receta_original_id and detalle.receta_id:
            receta_original_id = detalle.receta_id
        
        # Crear sugerencia
        sugerencia = Sugerencia(
            chat_id=chat_id,
            detalle_comida_id=detalle_comida_id,
            nueva_receta_id=nueva_receta_id,
            receta_original_id=receta_original_id,
            estado=EstadoSugerencia.PENDIENTE,
            distancia_knn=distancia_knn,
            justificacion=justificacion,
            modelo_version=modelo_version
        )
        
        db.add(sugerencia)
        db.flush()
        
        logger.info(f"Sugerencia {sugerencia.id} creada para detalle_comida {detalle_comida_id}")
        return sugerencia
    
    @staticmethod
    def aceptar_sugerencia(
        usuario_id: int,
        sugerencia_id: int,
        db: Session
    ) -> AceptarSugerenciaResponse:
        """
        Acepta una sugerencia y actualiza el plan del usuario.
        
        Args:
            usuario_id: ID del usuario
            sugerencia_id: ID de la sugerencia
            db: Sesión de base de datos
            
        Returns:
            AceptarSugerenciaResponse con resultado
        """
        try:
            # Buscar sugerencia con joins necesarios
            sugerencia = db.query(Sugerencia).join(
                Chat, Sugerencia.chat_id == Chat.id
            ).filter(
                Sugerencia.id == sugerencia_id,
                Chat.usuario_id == usuario_id
            ).first()
            
            if not sugerencia:
                raise ValueError(f"Sugerencia {sugerencia_id} no encontrada")
            
            if sugerencia.estado != EstadoSugerencia.PENDIENTE:
                raise ValueError(f"La sugerencia ya está en estado: {sugerencia.estado.value}")
            
            # Obtener detalle_comida
            detalle = db.query(DetalleComida).filter(
                DetalleComida.id == sugerencia.detalle_comida_id
            ).first()
            
            if not detalle:
                raise ValueError(f"DetalleComida {sugerencia.detalle_comida_id} no encontrado")
            
            # Actualizar receta en el detalle
            detalle.receta_id = sugerencia.nueva_receta_id
            
            # Actualizar estado de sugerencia
            sugerencia.estado = EstadoSugerencia.ACEPTADA
            
            # Obtener plan para actualizar fecha_modificacion
            plan = db.query(Plan).join(
                DetalleComida, DetalleComida.menu_diario_id == Plan.id
            ).filter(
                DetalleComida.id == detalle.id
            ).first()
            
            if plan:
                plan.fecha_modificacion = datetime.now()
                plan_id = plan.id
            else:
                plan_id = 0
                logger.warning(f"No se encontró plan asociado a detalle_comida {detalle.id}")
            
            db.commit()
            
            logger.info(f"Sugerencia {sugerencia_id} aceptada. DetalleComida {detalle.id} actualizado.")
            
            return AceptarSugerenciaResponse(
                success=True,
                message="Receta actualizada exitosamente en tu plan",
                plan_actualizado_id=plan_id,
                detalle_comida_id=detalle.id
            )
            
        except Exception as e:
            db.rollback()
            logger.error(f"Error aceptando sugerencia: {e}")
            raise
    
    @staticmethod
    def rechazar_sugerencia(
        usuario_id: int,
        sugerencia_id: int,
        db: Session,
        feedback: Optional[str] = None
    ) -> RechazarSugerenciaResponse:
        """
        Rechaza una sugerencia y opcionalmente registra feedback.
        
        Args:
            usuario_id: ID del usuario
            sugerencia_id: ID de la sugerencia
            db: Sesión de base de datos
            feedback: Razón del rechazo (opcional)
            
        Returns:
            RechazarSugerenciaResponse con resultado
        """
        try:
            # Buscar sugerencia
            sugerencia = db.query(Sugerencia).join(
                Chat, Sugerencia.chat_id == Chat.id
            ).filter(
                Sugerencia.id == sugerencia_id,
                Chat.usuario_id == usuario_id
            ).first()
            
            if not sugerencia:
                raise ValueError(f"Sugerencia {sugerencia_id} no encontrada")
            
            if sugerencia.estado != EstadoSugerencia.PENDIENTE:
                raise ValueError(f"La sugerencia ya está en estado: {sugerencia.estado.value}")
            
            # Actualizar estado
            sugerencia.estado = EstadoSugerencia.RECHAZADA
            
            # Agregar feedback a la justificación
            if feedback:
                if sugerencia.justificacion:
                    sugerencia.justificacion += f"\n\n[Feedback usuario]: {feedback}"
                else:
                    sugerencia.justificacion = f"[Feedback usuario]: {feedback}"
            
            db.commit()
            
            logger.info(f"Sugerencia {sugerencia_id} rechazada por usuario {usuario_id}")
            
            return RechazarSugerenciaResponse(
                success=True,
                message="Preferencia registrada. Mantenemos la receta original."
            )
            
        except Exception as e:
            db.rollback()
            logger.error(f"Error rechazando sugerencia: {e}")
            raise
    
    @staticmethod
    def get_sugerencia_enriquecida(
        sugerencia_id: int,
        db: Session
    ) -> SugerenciaSchema:
        """
        Obtiene una sugerencia con datos enriquecidos (recetas y comparación).
        
        Args:
            sugerencia_id: ID de la sugerencia
            db: Sesión de base de datos
            
        Returns:
            SugerenciaSchema con recetas y comparación nutricional
        """
        sugerencia = db.query(Sugerencia).filter(
            Sugerencia.id == sugerencia_id
        ).first()
        
        if not sugerencia:
            raise ValueError(f"Sugerencia {sugerencia_id} no encontrada")
        
        # Obtener recetas
        receta_nueva = db.query(Receta).filter(
            Receta.id == sugerencia.nueva_receta_id
        ).first()
        
        receta_original = None
        if sugerencia.receta_original_id:
            receta_original = db.query(Receta).filter(
                Receta.id == sugerencia.receta_original_id
            ).first()
        
        # Construir RecipeCards
        receta_nueva_card = SugerenciaService._build_recipe_card(receta_nueva) if receta_nueva else None
        receta_original_card = SugerenciaService._build_recipe_card(receta_original) if receta_original else None
        
        # Construir comparación
        comparacion = None
        if receta_original and receta_nueva:
            comparacion = SugerenciaService._build_nutritional_comparison(
                receta_original, receta_nueva
            )
        
        # Construir schema
        sugerencia_schema = SugerenciaSchema.from_orm(sugerencia)
        sugerencia_schema.receta_original = receta_original_card
        sugerencia_schema.receta_nueva = receta_nueva_card
        sugerencia_schema.comparacion = comparacion
        
        return sugerencia_schema
    
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
