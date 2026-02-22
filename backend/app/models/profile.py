from sqlalchemy import Column, Integer, ForeignKey, Enum, Date, String, SmallInteger, Float
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
    goal = Column(Enum("lose_weight", "maintain_weight", "gain_weight", name="goal_enum"))
    height = Column(Float)
    weight = Column(Float)
    body_type = Column(Enum("lean", "normal", "stocky", "obese", name="body_type_enum"))
    body_fat_percentage = Column(Float)
    calories_target = Column(Float)
    protein_target = Column(Float)
    carbs_target = Column(Float)
    fat_target = Column(Float)
    gender = Column(Enum("male", "female", name="gender_enum"))
    meals_per_day = Column(SmallInteger)
    activity_level = Column(Enum("low", "medium", "high", name="activity_level_enum"))
    birth_date = Column(Date)

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
    eating_styles = relationship(
        "EatingStyle",
        secondary="profiles_eating_styles",
    )