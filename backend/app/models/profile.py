from sqlalchemy import Column, Integer, ForeignKey, Enum, Date, SmallInteger, Float
from sqlalchemy.orm import relationship
from app.database import Base

class Profile(Base):
    __tablename__ = "profiles"
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(
        Integer,
        ForeignKey("users.id", ondelete="CASCADE", onupdate="CASCADE"),
        nullable=False,
        unique=True,
        index=True
    )
    goal = Column(Enum("lose_weight", "maintain_weight", "gain_weight", name="goal_enum"), nullable=False)
    height = Column(Float, nullable=False)
    weight = Column(Float, nullable=False)
    body_type = Column(Enum("lean", "normal", "stocky", "obese", name="body_type_enum"), nullable=False)
    body_fat_percentage = Column(Float)
    calories_target = Column(Float)
    protein_target = Column(Float)
    carbs_target = Column(Float)
    fat_target = Column(Float)
    gender = Column(Enum("male", "female", name="gender_enum"), nullable=False)
    meals_per_day = Column(SmallInteger, nullable=False, default=3)
    activity_level = Column(Enum("low", "medium", "high", name="activity_level_enum"), nullable=False)
    birth_date = Column(Date, nullable=False)

    user = relationship("User", back_populates="profile")
    tastes = relationship(
        "Taste",
        secondary="profiles_tastes",
        back_populates="profiles"
    )
    restrictions = relationship(
        "Restriction",
        secondary="profiles_restrictions",
        back_populates="profiles"
    )
    diet_types = relationship(
        "DietType",
        secondary="profiles_diet_types",
        back_populates="profiles"
    )