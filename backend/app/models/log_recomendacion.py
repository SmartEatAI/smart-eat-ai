from sqlalchemy import Column, Integer, ForeignKey, DateTime, Boolean, Float, Text, String
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.database import Base


class LogRecomendacion(Base):
    __tablename__ = "logs_recomendaciones"

    id = Column(Integer, primary_key=True, index=True)
    usuario_id = Column(Integer, ForeignKey("usuarios.id"), nullable=False)
    conversacion_id = Column(Integer, ForeignKey("conversaciones.id"), nullable=True)
    receta_original_id = Column(Integer, ForeignKey("recetas.id"), nullable=False)
    receta_sugerida_id = Column(Integer, ForeignKey("recetas.id"), nullable=False)
    aceptada = Column(Boolean, nullable=True)  # None = pendiente, True/False = decidido
    distancia_knn = Column(Float, nullable=False)
    justificacion_texto = Column(Text, nullable=True)
    modelo_version = Column(String(50), nullable=True)  # Versión del modelo KNN usado
    timestamp = Column(DateTime(timezone=True), server_default=func.now())
    
    # Relationships
    usuario = relationship("Usuario", back_populates="logs_recomendaciones")
    conversacion = relationship("Conversacion")
    receta_original = relationship("Receta", foreign_keys=[receta_original_id])
    receta_sugerida = relationship("Receta", foreign_keys=[receta_sugerida_id])
