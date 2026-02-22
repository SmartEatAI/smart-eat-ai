from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship
from app.database import Base

class Taste(Base):
    __tablename__ = "tastes"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False, unique=True)
    
    profiles = relationship(
        "Profile", 
        secondary="profiles_tastes",
        back_populates="tastes",
    )
