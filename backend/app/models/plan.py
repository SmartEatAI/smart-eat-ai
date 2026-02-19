from sqlalchemy import Column, Integer, ForeignKey, TIMESTAMP, Boolean
from sqlalchemy.orm import relationship
from app.database import Base

class Plan(Base):
    __tablename__ = "plans"
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(
        Integer,
        ForeignKey("users.id", ondelete="CASCADE", onupdate="CASCADE"),
        nullable=False,
        index=True
    )
    created_at = Column(TIMESTAMP)
    updated_at = Column(TIMESTAMP)
    active = Column(Boolean, default=True)

    user = relationship("User", back_populates="plans")
    daily_menus = relationship(
        "DailyMenu",
        back_populates="plan",
        cascade="all, delete-orphan",
        passive_deletes=True
    )