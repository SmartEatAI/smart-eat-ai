from sqlalchemy import Column, Integer, ForeignKey, Time, SmallInteger, Enum
from sqlalchemy.orm import relationship
from app.database import Base

class MealDetail(Base):
    __tablename__ = "meal_details"
    id = Column(Integer, primary_key=True, index=True)
    recipe_id = Column(
        Integer,
        ForeignKey("recipes.id", ondelete="RESTRICT", onupdate="CASCADE"),
        nullable=False,
        index=True
    )
    daily_menu_id = Column(
        Integer,
        ForeignKey("daily_menus.id", ondelete="CASCADE", onupdate="CASCADE"),
        nullable=False,
        index=True
    )
    schedule = Column(SmallInteger, nullable=False)
    status = Column(SmallInteger, default=False, nullable=False)
    meal_type = Column(Enum("breakfast", "lunch", "dinner", "snack", name="meal_type_enum"), nullable=False)

    recipe = relationship("Recipe")
    daily_menu = relationship("DailyMenu", back_populates="meal_details")