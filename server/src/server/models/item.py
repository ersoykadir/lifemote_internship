"""
Kadir Ersoy
Internship Project
Item Model
"""
from sqlalchemy import Boolean, Column, ForeignKey, Integer, String
from sqlalchemy.orm import relationship

from server.database.db import Base


class Item(Base):
    """Item Model"""

    __tablename__ = "items"

    id = Column(Integer, primary_key=True, index=True)
    message = Column(String(64), nullable=False)
    completed = Column(Boolean, default=False, nullable=False)
    owner_id = Column(Integer, ForeignKey("users.id"))
    context_id = Column(Integer, ForeignKey("contexts.id"))

    owner = relationship("User", back_populates="items")
    context = relationship("Context", back_populates="items")
