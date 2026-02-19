from sqlalchemy import Column, Integer, ForeignKey, Time, SmallInteger, Enum
from sqlalchemy.orm import relationship
from app.database import Base

class MealDetail(Base):
    __tablename__ = "meal_detail"
    id = Column(Integer, primary_key=True, index=True)
    recipe_id = Column(
        Integer,
        ForeignKey("recipe.id", ondelete="RESTRICT", onupdate="CASCADE"),
        nullable=False,
        index=True
    )
    daily_menu_id = Column(
        Integer,
        ForeignKey("daily_menu.id", ondelete="CASCADE", onupdate="CASCADE"),
        nullable=False,
        index=True
    )
    schedule = Column(Time)
    status = Column(SmallInteger)
    meal_type = Column(Enum("breakfast", "lunch", "dinner", "snack", name="meal_type_enum"))

    recipe = relationship("Recipe")
    daily_menu = relationship("DailyMenu", back_populates="meal_details")