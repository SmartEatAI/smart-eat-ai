from sqlalchemy import Column, Integer, ForeignKey
from app.database import Base

class PerfilRestriccion(Base):
    __tablename__ = "perfil_restriccion"
    perfil_id = Column(
        Integer,
        ForeignKey("perfil.id", ondelete="CASCADE", onupdate="CASCADE"),
        primary_key=True
    )
    restriccion_id = Column(
        Integer,
        ForeignKey("restriccion.id", ondelete="CASCADE", onupdate="CASCADE"),
        primary_key=True
    )