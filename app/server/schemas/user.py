from typing import List, Union

from pydantic import BaseModel
from .item import Item

class UserBase(BaseModel):
    email: str
    
class UserCreate(UserBase):
    password: str

class User(UserBase):
    id: int
    items: List[Item] = []

    class Config:
        from_attribute = True
