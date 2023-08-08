from sqlalchemy import Boolean, Column, ForeignKey, Integer, String
from sqlalchemy.orm import relationship

from .db import Base


class Item(Base):
    __tablename__ = "item"

    id = Column(Integer, primary_key=True, index=True)
    message = Column(String(64), unique=False, index=True, nullable=False)
    completed = Column(Boolean, default=False, nullable=False)
