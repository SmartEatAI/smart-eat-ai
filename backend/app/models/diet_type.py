from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship
from app.database import Base

class DietType(Base):
    __tablename__ = "diet_types"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(50), unique=True, index=True, nullable=True)
    
    recipes = relationship(
        "Recipe",
        back_populates="diet_types",
        secondary="recipe_diet_types", 
        cascade="all",
        passive_deletes=True
    ) 