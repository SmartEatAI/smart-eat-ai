from sqlalchemy import Column, Integer, ForeignKey
from sqlalchemy.orm import relationship
from app.database import Base

class PerfilGusto(Base):
    __tablename__ = "perfil_gusto"
    perfil_id = Column(Integer, ForeignKey("perfil.id"), primary_key=True)
    gusto_id = Column(Integer, ForeignKey("gusto.id"), primary_key=True)

    perfil = relationship("Perfil", back_populates="gustos")
    gusto = relationship("Gusto", back_populates="perfiles")