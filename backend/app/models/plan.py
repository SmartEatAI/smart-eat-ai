from sqlalchemy import Column, Integer, ForeignKey, TIMESTAMP, Boolean
from sqlalchemy.orm import relationship
from app.database import Base

class Plan(Base):
    __tablename__ = "plan"
    id = Column(Integer, primary_key=True, index=True)
    usuario_id = Column(
        Integer,
        ForeignKey("usuario.id", ondelete="CASCADE", onupdate="CASCADE"),
        nullable=False,
        index=True
    )
    fecha_creacion = Column(TIMESTAMP)
    fecha_modificacion = Column(TIMESTAMP)
    activo = Column(Boolean, default=True)

    usuario = relationship("Usuario", back_populates="planes")
    menus_diarios = relationship(
        "MenuDiario",
        back_populates="plan",
        cascade="all, delete-orphan",
        passive_deletes=True
    )