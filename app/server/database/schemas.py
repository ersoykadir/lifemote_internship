from typing import List, Union

from pydantic import BaseModel

class ItemBase(BaseModel):
    message: str
    completed: bool = False
    
class ContextBase(BaseModel):
    name: str
    description: str

class ItemUpdate(BaseModel):
    message: Union[str, None]
    completed: bool = False
    context_name: Union[str, None]

class ItemCreate(ItemBase):
    context_name: str

class Item(ItemBase):
    id: int
    owner_id: int
    # context_id: int
    context: ContextBase
    
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

class ContextCreate(ContextBase):
    pass

class Context(ContextBase):
    id: int
    owner_id: int
    items: List[Item] = []

    class Config:
        from_attribute = True