from sqlalchemy import Column, Integer, ForeignKey, Time, SmallInteger, Enum
from sqlalchemy.orm import relationship
from app.database import Base

class DetalleComida(Base):
    __tablename__ = "detalle_comida"
    id = Column(Integer, primary_key=True, index=True)
    receta_id = Column(Integer, ForeignKey("receta.id"))
    menu_diario_id = Column(Integer, ForeignKey("menu_diario.id"))
    horario = Column(Time)
    estado = Column(SmallInteger)
    tipo_comida = Column(Enum("desayuno", "almuerzo", "cena", "snack", name="tipo_comida_enum"))

    receta = relationship("Receta")
    menu_diario = relationship("MenuDiario", back_populates="detalles_comida")