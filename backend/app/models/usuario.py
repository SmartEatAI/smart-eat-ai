from sqlalchemy import Column, Integer, String, TIMESTAMP
from sqlalchemy.orm import relationship
from app.database import Base

class Usuario(Base):
    __tablename__ = "usuario"
    id = Column(Integer, primary_key=True, index=True)
    nombre = Column(String)
    correo = Column(String, unique=True, index=True)
    contrasena = Column(String)
    fecha_registro = Column(TIMESTAMP)
    fecha_actualizacion = Column(TIMESTAMP)
    url_foto_perfil = Column(String)

    perfil = relationship("Perfil", back_populates="usuario", uselist=False)
    planes = relationship("Plan", back_populates="usuario")
    chats = relationship("Chat", back_populates="usuario", cascade="all, delete-orphan")
    
    # DEPRECATED: Mantener compatibilidad temporal con código antiguo
    # conversaciones = relationship("Conversacion", back_populates="usuario")
    # logs_recomendaciones = relationship("LogRecomendacion", back_populates="usuario")