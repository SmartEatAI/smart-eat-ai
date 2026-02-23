from sqlalchemy import Column, Integer, Enum
from sqlalchemy.orm import relationship
from app.database import Base

class DietType(Base):
    __tablename__ = "diet_types"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(Enum("high_protein", "low_carb", "vegan", "vegetarian", "low_calorie", "high_fiber", "high_carb", name="diet_type_enum"), unique=True, index=True, nullable=False)
    
    recipes = relationship(
        "Recipe",
        back_populates="diet_types",
        secondary="recipe_diet_types", 
        cascade="all",
        passive_deletes=True
    ) 
    
    profiles = relationship(
        "Profile",
        secondary="profiles_diet_types",
        back_populates="diet_types"
    )