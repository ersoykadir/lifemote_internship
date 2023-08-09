from typing import List, Union

from pydantic import BaseModel

class ItemBase(BaseModel):
    message: str
    completed: bool = False

class ItemCreate(ItemBase):
    context: Union[str, None]

class Item(ItemBase):
    id: int
    owner_id: int
    context_id: Union[int, None]
    
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

class ContextBase(BaseModel):
    name: str
    description: str

class ContextCreate(ContextBase):
    pass

class Context(ContextBase):
    id: int
    owner_id: int
    items: List[Item] = []

    class Config:
        from_attribute = True