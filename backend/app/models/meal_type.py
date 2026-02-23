from sqlalchemy import Column, Integer, Enum
from sqlalchemy.orm import relationship
from app.database import Base

class MealType(Base):
    __tablename__ = "meal_types"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(Enum("breakfast", "lunch", "dinner", "snack", name="meal_type_enum"), unique=True, index=True, nullable=False)
    
    recipes = relationship(
        "Recipe",
        back_populates="meal_types",
        secondary="recipe_meal_types", 
        cascade="all",
        passive_deletes=True
    )