from sqlalchemy import Column, Integer, ForeignKey
from sqlalchemy.orm import relationship
from app.database import Base

class ProfileRestriction(Base):
    __tablename__ = "profile_restriction"
    profile_id = Column(
        Integer,
        ForeignKey("profile.id", ondelete="CASCADE", onupdate="CASCADE"),
        primary_key=True
    )
    restriction_id = Column(
        Integer,
        ForeignKey("restriction.id", ondelete="CASCADE", onupdate="CASCADE"),
        primary_key=True
    )

    profile = relationship("Profile", back_populates="restrictions")
    restriction = relationship("Restriction", back_populates="profiles")