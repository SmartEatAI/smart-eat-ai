from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship
from app.database import Base

class Gusto(Base):
    __tablename__ = "gusto"
    id = Column(Integer, primary_key=True, index=True)
    nombre = Column(String)

    perfiles = relationship("Perfil", secondary="perfil_gusto", back_populates="gusto")