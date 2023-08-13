from typing import List, Union

from pydantic import BaseModel

from .item import Item

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