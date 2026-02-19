from sqlalchemy import Column, Integer, ForeignKey, Enum, DECIMAL, Date, String, SmallInteger
from sqlalchemy.orm import relationship
from app.database import Base

class Perfil(Base):
    __tablename__ = "perfil"
    id = Column(Integer, primary_key=True, index=True)
    usuario_id = Column(
        Integer,
        ForeignKey("usuario.id", ondelete="CASCADE", onupdate="CASCADE"),
        nullable=False,
        unique=True,
        index=True
    )
    objetivo = Column(Enum("perder_peso", "mantener_peso", "ganar_peso", name="objetivo_enum"))
    altura = Column(DECIMAL)
    peso = Column(DECIMAL)
    pct_grasa = Column(Integer)
    calorias_cal = Column(Integer)
    proteina_cal = Column(Integer)
    carbohidratos_cal = Column(Integer)
    grasa_cal = Column(Integer)
    genero = Column(String)
    num_comidas_dia = Column(SmallInteger)
    nivel_actividad = Column(Enum("bajo", "medio", "alto", name="nivel_actividad_enum"))
    fecha_nacimiento = Column(Date)

    usuario = relationship("Usuario", back_populates="perfil", uselist=False)
    gustos = relationship(
        "Gusto",
        secondary="perfil_gusto",
        back_populates="perfil",
        cascade="all, delete-orphan",
        passive_deletes=True
    )
    restricciones = relationship(
        "Restriccion",
        secondary="perfil_restriccion",
        back_populates="perfil",
        cascade="all, delete-orphan",
        passive_deletes=True
    )
    estilos_alimentacion = relationship(
        "PerfilEstiloAlimentacion",
        back_populates="perfil",
        cascade="all, delete-orphan",
        passive_deletes=True
    )