from sqlalchemy import Column, Integer, ForeignKey, Enum
from sqlalchemy.orm import relationship
from app.database import Base

class RecipeMealType(Base):
    __tablename__ = "recipe_meal_types"
    id = Column(Integer, primary_key=True, index=True)
    recipe_id = Column(
        Integer,
        ForeignKey("recipes.id", ondelete="CASCADE", onupdate="CASCADE"),
        nullable=False,
        index=True
    )
    name = Column(Enum("breakfast", "lunch", "dinner", "snack", name="meal_type_enum"))

    recipe = relationship("Recipe", back_populates="meal_types")