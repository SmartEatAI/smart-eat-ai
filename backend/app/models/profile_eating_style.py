from sqlalchemy import Column, Integer, ForeignKey
from app.database import Base

class ProfileEatingStyle(Base):
    __tablename__ = "profiles_eating_styles"
    profile_id = Column(
        Integer,
        ForeignKey("profiles.id", ondelete="CASCADE", onupdate="CASCADE"),
        primary_key=True
    )
    eating_style_id = Column(
        Integer,
        ForeignKey("eating_styles.id", ondelete="CASCADE", onupdate="CASCADE"),
        primary_key=True
    )