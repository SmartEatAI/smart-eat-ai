from sqlalchemy import Column, Integer, String, TIMESTAMP
from sqlalchemy.orm import relationship
from app.database import Base

class Usuario(Base):
    __tablename__ = "usuario"
    id = Column(Integer, primary_key=True, index=True)
    nombre = Column(String, nullable=False)
    correo = Column(String, unique=True, index=True, nullable=False)
    contrasena_hash = Column(String, nullable=False)
    fecha_creacion = Column(TIMESTAMP)
    fecha_actualizacion = Column(TIMESTAMP)
    url_foto_perfil = Column(String)

    perfil = relationship(
        "Perfil",
        back_populates="usuario",
        uselist=False,
        cascade="all, delete-orphan",
        passive_deletes=True
    )
    planes = relationship(
        "Plan",
        back_populates="usuario",
        cascade="all, delete-orphan",
        passive_deletes=True
    )