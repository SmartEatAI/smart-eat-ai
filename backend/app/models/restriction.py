from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship
from app.database import Base

class Restriction(Base):
    __tablename__ = "restrictions"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String)

    profiles = relationship(
        "Profile",
        secondary="profiles_restrictions",
        back_populates="restrictions")