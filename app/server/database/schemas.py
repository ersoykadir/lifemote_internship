from typing import List, Union

from pydantic import BaseModel

class ItemBase(BaseModel):
    message: str

class ItemCreate(ItemBase):
    pass

class Item(ItemBase):
    id: int
    
    class Config:
        from_attribute = True
