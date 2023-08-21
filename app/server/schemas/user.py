from typing import List, Union

from pydantic import BaseModel
from .item import Item
from .context import Context

class UserBase(BaseModel):
    email: str
    name: str

class UserCreate(UserBase):
    pass

class User(UserBase):
    id: int
    items: List[Item] = []
    contexts: List[Context] = []

    class Config:
        from_attribute = True
