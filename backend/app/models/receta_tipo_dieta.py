from sqlalchemy import Column, Integer, ForeignKey, Enum
from sqlalchemy.orm import relationship
from app.database import Base

class RecetaTipoDieta(Base):
    __tablename__ = "receta_tipo_dieta"
    id = Column(Integer, primary_key=True, index=True)
    receta_id = Column(Integer, ForeignKey("receta.id"))
    nombre = Column(Enum("keto", "vegana", "vegetariana", "normal", name="tipo_dieta_enum"))

    receta = relationship("Receta", back_populates="tipos_dieta")