from sqlalchemy import Column, Integer, ForeignKey
from app.database import Base

class PerfilGusto(Base):
    __tablename__ = "perfil_gusto"
    perfil_id = Column(
        Integer,
        ForeignKey("perfil.id", ondelete="CASCADE", onupdate="CASCADE"),
        primary_key=True
    )
    gusto_id = Column(
        Integer,
        ForeignKey("gusto.id", ondelete="CASCADE", onupdate="CASCADE"),
        primary_key=True
    )