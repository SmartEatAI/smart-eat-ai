from sqlalchemy import Column, Integer, ForeignKey, Enum
from sqlalchemy.orm import relationship
from app.database import Base

class RecipeDietType(Base):
    __tablename__ = "recipe_diet_type"
    id = Column(Integer, primary_key=True, index=True)
    recipe_id = Column(
        Integer,
        ForeignKey("recipe.id", ondelete="CASCADE", onupdate="CASCADE"),
        nullable=False,
        index=True
    )
    name = Column(Enum("high_protein", "low_carb", "vegan", "vegetarian", "low_calorie", "high_fiber", "high_carb", name="diet_type_enum"))

    recipe = relationship("Recipe", back_populates="diet_types")