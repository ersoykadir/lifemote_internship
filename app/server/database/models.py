from sqlalchemy import Boolean, Column, ForeignKey, Integer, String
from sqlalchemy.orm import relationship

from .db import Base


class Item(Base):
    __tablename__ = "items"

    id = Column(Integer, primary_key=True, index=True)
    message = Column(String(64), unique=False, index=True, nullable=False)
    completed = Column(Boolean, default=False, nullable=False)
    owner_id = Column(Integer, ForeignKey("users.id"))

    owner = relationship("User", back_populates="items")

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String(64), unique=True, index=True)
    password = Column(String(64))

    items = relationship("Item", back_populates="owner")