from sqlalchemy import Column, Integer, ForeignKey
from sqlalchemy.orm import relationship
from app.database import Base

class ProfileTaste(Base):
    __tablename__ = "profile_taste"
    profile_id = Column(
        Integer,
        ForeignKey("profile.id", ondelete="CASCADE", onupdate="CASCADE"),
        primary_key=True
    )
    taste_id = Column(
        Integer,
        ForeignKey("taste.id", ondelete="CASCADE", onupdate="CASCADE"),
        primary_key=True
    )