from sqlalchemy import Column, Integer, ForeignKey, SmallInteger
from sqlalchemy.orm import relationship
from app.database import Base

class MenuDiario(Base):
    __tablename__ = "menu_diario"
    id = Column(Integer, primary_key=True, index=True)
    plan_id = Column(Integer, ForeignKey("plan.id"))
    dia_semana = Column(SmallInteger)

    plan = relationship("Plan", back_populates="menus_diarios")
    detalles_comida = relationship("DetalleComida", back_populates="menu_diario")