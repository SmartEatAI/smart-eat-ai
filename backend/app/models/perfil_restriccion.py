from sqlalchemy import Column, Integer, ForeignKey
from sqlalchemy.orm import relationship
from app.database import Base

class PerfilRestriccion(Base):
    __tablename__ = "perfil_restriccion"
    perfil_id = Column(Integer, ForeignKey("perfil.id"), primary_key=True)
    restriccion_id = Column(Integer, ForeignKey("restriccion.id"), primary_key=True)

    perfil = relationship("Perfil", back_populates="restricciones")
    restriccion = relationship("Restriccion", back_populates="perfiles")