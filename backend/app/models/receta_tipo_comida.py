from sqlalchemy import Column, Integer, ForeignKey, Enum
from sqlalchemy.orm import relationship
from app.database import Base

class RecetaTipoComida(Base):
    __tablename__ = "receta_tipo_comida"
    id = Column(Integer, primary_key=True, index=True)
    receta_id = Column(Integer, ForeignKey("receta.id"))
    nombre = Column(Enum("desayuno", "almuerzo", "cena", "snack", name="tipo_comida_enum"))

    receta = relationship("Receta", back_populates="tipos_comida")