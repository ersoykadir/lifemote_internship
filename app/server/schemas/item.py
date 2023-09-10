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
    
class ItemCreate(ItemBase):
    """Item create schema"""
    context_name: Union[str, None] = None

class Item(ItemBase):
    """Item schema"""
    id: int
    owner_id: int
    context_id: int
    
    class Config:
        from_attribute = True