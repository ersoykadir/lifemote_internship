from sqlalchemy import Boolean, Column, ForeignKey, Integer, String, UniqueConstraint
from sqlalchemy.orm import relationship

from .db import Base


class Item(Base):
    __tablename__ = "items"

    id = Column(Integer, primary_key=True, index=True)
    message = Column(String(64), nullable=False)
    completed = Column(Boolean, default=False, nullable=False)
    owner_id = Column(Integer, ForeignKey("users.id"))
    context_id = Column(Integer, ForeignKey("contexts.id"))

    owner = relationship("User", back_populates="items")
    context = relationship("Context", back_populates="items")

class User(Base):
    __tablename__ = "users"
    __table_args__ = (
        UniqueConstraint('email', name='unique_user_email'),
        )

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String(64), unique=True)
    password = Column(String(64))

    items = relationship("Item", back_populates="owner")
    contexts = relationship("Context", back_populates="owner")

class Context(Base):
    __tablename__ = "contexts"
    __table_args__ = (
        UniqueConstraint('name', 'owner_id', name='unique_context_name'),
      )

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(64))
    description = Column(String(64))
    owner_id = Column(Integer, ForeignKey("users.id"))

    items = relationship("Item", back_populates="context")
    owner = relationship("User", back_populates="contexts")