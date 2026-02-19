from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Text, Enum as SQLEnum
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
import enum
from app.database import Base


class RolMensaje(str, enum.Enum):
    USER = "user"
    ASSISTANT = "assistant"


class Conversacion(Base):
    __tablename__ = "conversaciones"

    id = Column(Integer, primary_key=True, index=True)
    usuario_id = Column(Integer, ForeignKey("usuarios.id"), nullable=False)
    mensaje = Column(Text, nullable=False)
    rol = Column(SQLEnum(RolMensaje), nullable=False)
    timestamp = Column(DateTime(timezone=True), server_default=func.now())
    contexto_plan_id = Column(Integer, ForeignKey("planes.id"), nullable=True)
    
    # Relationships
    usuario = relationship("Usuario", back_populates="conversaciones")
    plan = relationship("Plan", foreign_keys=[contexto_plan_id])
