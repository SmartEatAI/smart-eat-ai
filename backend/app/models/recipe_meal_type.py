from sqlalchemy import Column, Integer, ForeignKey
from app.database import Base

class RecipeMealType(Base):
    __tablename__ = "recipe_meal_types"
    recipe_id = Column(
        Integer,
        ForeignKey("recipes.id", ondelete="CASCADE", onupdate="CASCADE"),
        primary_key=True
    )
    meal_type_id = Column(
        Integer,
        ForeignKey("meal_types.id", ondelete="CASCADE", onupdate="CASCADE"),
        primary_key=True
    )