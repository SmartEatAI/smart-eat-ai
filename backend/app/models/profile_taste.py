from sqlalchemy import Column, Integer, ForeignKey
from app.database import Base

class ProfileTaste(Base):
    __tablename__ = "profiles_tastes"
    profile_id = Column(
        Integer,
        ForeignKey("profiles.id", ondelete="CASCADE", onupdate="CASCADE"),
        primary_key=True
    )
    taste_id = Column(
        Integer,
        ForeignKey("tastes.id", ondelete="CASCADE", onupdate="CASCADE"),
        primary_key=True
    )