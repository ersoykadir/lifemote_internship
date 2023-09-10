"""
Kadir Ersoy
Internship Project
User Schema
"""
from typing import List
from pydantic import BaseModel
from .item import Item
from .context import Context

class UserBase(BaseModel):
    """User base schema"""
    email: str
    name: str

class User(UserBase):
    """User schema"""
    id: int
    items: List[Item] = []
    contexts: List[Context] = []

    class Config:
        """Config"""
        from_attribute = True
