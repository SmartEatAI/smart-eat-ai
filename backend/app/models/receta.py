from sqlalchemy import Column, Integer, String, Float, Text, JSON, Enum as SQLEnum
from sqlalchemy.orm import relationship
from app.database import Base

class Receta(Base):
    __tablename__ = "receta"
    id = Column(Integer, primary_key=True, index=True)
    nombre = Column(String)
    calorias = Column(Integer)
    proteinas = Column(Integer)
    carbohidratos = Column(Integer)
    grasas = Column(Integer)
    url_imagen = Column(String)
    url_receta = Column(String)

    tipos_comida = relationship("RecetaTipoComida", back_populates="receta")
    tipos_dieta = relationship("RecetaTipoDieta", back_populates="receta")
    embedding = relationship("EmbeddingReceta", back_populates="receta", uselist=False)