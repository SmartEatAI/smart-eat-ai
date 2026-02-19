from sqlalchemy import Column, Integer, ForeignKey
from app.database import Base

class RecipeDietType(Base):
    __tablename__ = "recipe_diet_types"
    recipe_id = Column(
        Integer,
        ForeignKey("recipes.id", ondelete="CASCADE", onupdate="CASCADE"),
        primary_key=True
    )
    diet_type_id = Column(
        Integer,
        ForeignKey("diet_types.id", ondelete="CASCADE", onupdate="CASCADE"),
        primary_key=True
    )