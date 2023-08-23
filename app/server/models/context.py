from sqlalchemy import Boolean, Column, ForeignKey, Integer, String, UniqueConstraint
from sqlalchemy.orm import relationship

from database.db import Base

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