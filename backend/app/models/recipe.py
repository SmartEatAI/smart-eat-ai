from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship
from app.database import Base

class Recipe(Base):
    __tablename__ = "recipes"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    calories = Column(Integer, nullable=False, default=0)
    protein = Column(Integer, nullable=False, default=0)
    carbs = Column(Integer, nullable=False, default=0)
    fat = Column(Integer, nullable=False, default=0)
    image_url = Column(String, default="/images/Image_not_available.png")
    recipe_url = Column(String)

    meal_types = relationship(
        "MealType", 
        secondary="recipe_meal_types",
        back_populates="recipes",
        cascade="all, delete"
    )
    diet_types = relationship(
        "DietType", 
        secondary="recipe_diet_types",
        back_populates="recipes",
        cascade="all, delete"
    )