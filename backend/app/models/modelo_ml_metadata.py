from sqlalchemy import Column, Integer, String, DateTime, Boolean, JSON
from sqlalchemy.sql import func
from app.database import Base


class ModeloMLMetadata(Base):
    __tablename__ = "modelos_ml_metadata"

    id = Column(Integer, primary_key=True, index=True)
    nombre = Column(String(100), nullable=False)  # e.g., "knn_nutricional"
    version = Column(String(50), nullable=False)  # e.g., "v1.0.0"
    ruta_archivo = Column(String(255), nullable=False)  # Path to .pkl file
    metricas = Column(JSON, nullable=True)  # Metrics: {"accuracy": 0.95, "precision@5": 0.82}
    activo = Column(Boolean, default=False, nullable=False)  # Only one active model per nombre
    fecha_registro = Column(DateTime(timezone=True), server_default=func.now())
    descripcion = Column(String(500), nullable=True)
    
    # Ensure unique active model per name
    __table_args__ = (
        # You can add a unique constraint in migration if needed
    )
