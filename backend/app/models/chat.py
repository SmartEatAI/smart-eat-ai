from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Boolean
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.database import Base


class Chat(Base):
    """
    Sesión de chat del usuario.
    Permite agrupar mensajes y mantener contexto conversacional separado.
    """
    __tablename__ = "chats"

    id = Column(Integer, primary_key=True, index=True)
    nombre = Column(String(100), nullable=True)  # Ej: "Chat del 19 Feb", "Modificar plan semanal"
    usuario_id = Column(Integer, ForeignKey("usuario.id"), nullable=False)
    fecha_creacion = Column(DateTime(timezone=True), server_default=func.now())
    activo = Column(Boolean, default=True)  # Marca el chat actual activo
    
    # Relationships
    usuario = relationship("Usuario", back_populates="chats")
    mensajes = relationship("Mensaje", back_populates="chat", cascade="all, delete-orphan")
    sugerencias = relationship("Sugerencia", back_populates="chat", cascade="all, delete-orphan")
