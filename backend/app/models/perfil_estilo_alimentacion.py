from sqlalchemy import Column, Integer, ForeignKey, Enum
from sqlalchemy.orm import relationship
from app.database import Base

class PerfilEstiloAlimentacion(Base):
    __tablename__ = "perfil_estilo_alimentacion"
    id = Column(Integer, primary_key=True, index=True)
    perfil_id = Column(
        Integer,
        ForeignKey("perfil.id", ondelete="CASCADE", onupdate="CASCADE"),
        nullable=False,
        index=True
    )
    nombre = Column(Enum("alta_en_proteina", "baja_en_carbohidratos", "vegana", "vegetariana", "baja_en_calorias", "alta_en_fibra", "alta_en_carbohidratos", name="estilo_alimentacion_enum"))

    perfil = relationship("Perfil", back_populates="estilos_alimentacion")