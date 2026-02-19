from sqlalchemy import Column, Integer, ForeignKey, DateTime, Float, Text, String, Enum as SQLEnum
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
import enum
from app.database import Base


class EstadoSugerencia(str, enum.Enum):
    """Estado de una sugerencia de receta"""
    PENDIENTE = "pendiente"
    ACEPTADA = "aceptada"
    RECHAZADA = "rechazada"


class Sugerencia(Base):
    """
    Sugerencia de cambio de receta generada por el agente.
    Vinculada a un detalle de comida específico que se propone modificar.
    """
    __tablename__ = "sugerencias"

    id = Column(Integer, primary_key=True, index=True)
    chat_id = Column(Integer, ForeignKey("chats.id"), nullable=False)
    detalle_comida_id = Column(Integer, ForeignKey("detalle_comida.id"), nullable=False)
    nueva_receta_id = Column(Integer, ForeignKey("recetas.id"), nullable=False)
    estado = Column(SQLEnum(EstadoSugerencia), nullable=False, default=EstadoSugerencia.PENDIENTE)
    fecha_hora = Column(DateTime(timezone=True), server_default=func.now())
    
    # Metadata adicional del modelo KNN (útil para análisis)
    receta_original_id = Column(Integer, ForeignKey("recetas.id"), nullable=True)  # Para referencia
    distancia_knn = Column(Float, nullable=True)  # Similitud nutricional
    justificacion = Column(Text, nullable=True)  # Explicación generada por LLM
    modelo_version = Column(String(50), nullable=True)  # Versión del modelo KNN usado
    
    # Relationships
    chat = relationship("Chat", back_populates="sugerencias")
    detalle_comida = relationship("DetalleComida", foreign_keys=[detalle_comida_id])
    nueva_receta = relationship("Receta", foreign_keys=[nueva_receta_id])
    receta_original = relationship("Receta", foreign_keys=[receta_original_id])
