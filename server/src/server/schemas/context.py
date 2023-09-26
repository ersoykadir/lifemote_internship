"""
Kadir Ersoy
Internship Project
Context Schema
"""
from typing import List
from pydantic import BaseModel
from .item import Item


class ContextBase(BaseModel):
    """Context base schema"""

    name: str
    description: str


class Context(ContextBase):
    """Context schema"""

    id: int
    owner_id: int
    items: List[Item] = []

    class Config:
        """Config"""

        from_attribute = True
