from sqlalchemy import Column, Integer, ForeignKey, Enum
from sqlalchemy.orm import relationship
from app.database import Base

class ProfileEatingStyle(Base):
    __tablename__ = "profile_eating_styles"
    id = Column(Integer, primary_key=True, index=True)
    profile_id = Column(
        Integer,
        ForeignKey("profiles.id", ondelete="CASCADE", onupdate="CASCADE"),
        nullable=False,
        index=True
    )
    name = Column(Enum("high_protein", "low_carb", "vegan", "vegetarian", "low_calorie", "high_fiber", "high_carb", name="eating_style_enum"))

    profile = relationship("Profile", back_populates="eating_styles")