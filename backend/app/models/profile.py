from sqlalchemy import Column, Integer, ForeignKey, Enum, DECIMAL, Date, String, SmallInteger
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
    height = Column(DECIMAL)
    weight = Column(DECIMAL)
    body_fat_percentage = Column(Integer)
    calories_target = Column(Integer)
    protein_target = Column(Integer)
    carbs_target = Column(Integer)
    fat_target = Column(Integer)
    gender = Column(String)
    meals_per_day = Column(SmallInteger)
    activity_level = Column(Enum("low", "medium", "high", name="activity_level_enum"))
    birth_date = Column(Date)

    user = relationship("User", back_populates="profile")
    tastes = relationship(
        "Taste",
        secondary="profiles_tastes"
    )
    restrictions = relationship(
        "Restriction",
        secondary="profiles_restrictions"
    )
    eating_styles = relationship(
        "ProfileEatingStyle",
        back_populates="profile",
        cascade="all, delete-orphan",
        passive_deletes=True
    )