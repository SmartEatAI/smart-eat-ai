from sqlalchemy import Column, Integer, ForeignKey
from app.database import Base

class ProfileDietType(Base):
    __tablename__ = "profiles_diet_types"
    profile_id = Column(
        Integer,
        ForeignKey("profiles.id", ondelete="CASCADE", onupdate="CASCADE"),
        primary_key=True
    )
    diet_type_id = Column(
        Integer,
        ForeignKey("diet_types.id", ondelete="CASCADE", onupdate="CASCADE"),
        primary_key=True
    )