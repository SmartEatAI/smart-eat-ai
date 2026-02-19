from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship
from app.database import Base

class Restriction(Base):
    __tablename__ = "restriction"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String)

    profiles = relationship("ProfileRestriction", back_populates="restriction")
