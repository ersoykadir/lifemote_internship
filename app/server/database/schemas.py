from typing import List, Union

from pydantic import BaseModel

class ItemBase(BaseModel):
    message: str
    completed: bool = False

class ItemCreate(ItemBase):
    pass

class Item(ItemBase):
    id: int
    owner_id: int
    
    class Config:
        from_attribute = True

class UserBase(BaseModel):
    email: str
    
class UserCreate(UserBase):
    password: str

class User(UserBase):
    id: int
    items: List[Item] = []

    class Config:
        from_attribute = True