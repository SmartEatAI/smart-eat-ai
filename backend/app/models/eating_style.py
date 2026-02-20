from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship
from app.database import Base

class EatingStyle(Base):
    __tablename__ = "eating_styles"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String)
    
    profiles = relationship(
        "Profile", 
        secondary="profiles_eating_styles",
        back_populates="eating_styles",
    )
