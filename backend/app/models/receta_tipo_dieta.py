from sqlalchemy import Column, Integer, ForeignKey, Enum
from sqlalchemy.orm import relationship
from app.database import Base

class RecetaTipoDieta(Base):
    __tablename__ = "receta_tipo_dieta"
    id = Column(Integer, primary_key=True, index=True)
    receta_id = Column(
        Integer,
        ForeignKey("receta.id", ondelete="CASCADE", onupdate="CASCADE"),
        nullable=False,
        index=True
    )
    nombre = Column(Enum("alta_en_proteina", "baja_en_carbohidratos", "vegana", "vegetariana", "baja_en_calorias", "alta_en_fibra", "alta_en_carbohidratos", name="tipo_dieta_enum"))

    receta = relationship("Receta", back_populates="tipos_dieta")