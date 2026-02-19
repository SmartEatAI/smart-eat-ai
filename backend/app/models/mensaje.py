from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Text, Enum as SQLEnum
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
import enum
from app.database import Base


class RolMensaje(str, enum.Enum):
    """Rol del mensaje en la conversación"""
    USER = "user"
    ASSISTANT = "assistant"
    SYSTEM = "system"  # Para mensajes del sistema


class Mensaje(Base):
    """
    Mensaje individual dentro de una sesión de chat.
    Almacena el texto y rol (usuario o asistente).
    """
    __tablename__ = "mensajes"

    id = Column(Integer, primary_key=True, index=True)
    chat_id = Column(Integer, ForeignKey("chats.id"), nullable=False)
    texto = Column(Text, nullable=False)
    rol = Column(SQLEnum(RolMensaje), nullable=False)
    fecha_hora = Column(DateTime(timezone=True), server_default=func.now())
    
    # Metadata opcional
    contexto_plan_id = Column(Integer, ForeignKey("planes.id"), nullable=True)  # Si el mensaje hace referencia a un plan
    
    # Relationships
    chat = relationship("Chat", back_populates="mensajes")
    plan = relationship("Plan", foreign_keys=[contexto_plan_id])
