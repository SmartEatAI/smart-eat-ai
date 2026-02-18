from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship
from app.database import Base

class Restriccion(Base):
    __tablename__ = "restriccion"
    id = Column(Integer, primary_key=True, index=True)
    nombre = Column(String)

    perfiles = relationship("PerfilRestriccion", back_populates="restriccion")