from sqlalchemy import Column, Integer, ForeignKey, DateTime, String
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from pgvector.sqlalchemy import Vector
from app.database import Base


class EmbeddingReceta(Base):
    __tablename__ = "embeddings_recetas"

    id = Column(Integer, primary_key=True, index=True)
    receta_id = Column(Integer, ForeignKey("recetas.id"), nullable=False, unique=True)
    embedding = Column(Vector(384), nullable=False)  # all-MiniLM-L6-v2 dimensionality
    modelo_version = Column(String(50), nullable=False, default="all-MiniLM-L6-v2")
    fecha_creacion = Column(DateTime(timezone=True), server_default=func.now())
    
    # Relationships
    receta = relationship("Receta", back_populates="embedding")
