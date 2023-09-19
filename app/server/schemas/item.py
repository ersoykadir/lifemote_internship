"""
Kadir Ersoy
Internship Project
Item Schema
"""
from typing import Union
from pydantic import BaseModel

class ItemBase(BaseModel):
    """Item base schema"""
    message: str
    completed: bool = False
    context_id: int

class Item(ItemBase):
    """Item schema"""
    id: int
    owner_id: int

    class Config:
        """Config"""
        from_attribute = True
