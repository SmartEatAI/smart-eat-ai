from sqlalchemy import Column, Integer, ForeignKey
from sqlalchemy.orm import relationship
from app.database import Base

class ProfileRestriction(Base):
    __tablename__ = "profiles_restrictions"
    profile_id = Column(
        Integer,
        ForeignKey("profiles.id", ondelete="CASCADE", onupdate="CASCADE"),
        primary_key=True
    )
    restriction_id = Column(
        Integer,
        ForeignKey("restrictions.id", ondelete="CASCADE", onupdate="CASCADE"),
        primary_key=True
    )