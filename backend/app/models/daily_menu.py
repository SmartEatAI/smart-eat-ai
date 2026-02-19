from sqlalchemy import Column, Integer, ForeignKey, SmallInteger
from sqlalchemy.orm import relationship
from app.database import Base

class DailyMenu(Base):
    __tablename__ = "daily_menu"
    id = Column(Integer, primary_key=True, index=True)
    plan_id = Column(
        Integer,
        ForeignKey("plan.id", ondelete="CASCADE", onupdate="CASCADE"),
        nullable=False,
        index=True
    )
    day_of_week = Column(SmallInteger)

    plan = relationship("Plan", back_populates="daily_menus")
    meal_details = relationship(
        "MealDetail",
        back_populates="daily_menu",
        cascade="all, delete-orphan",
        passive_deletes=True
    )