from typing import List, Union

from pydantic import BaseModel

class ItemBase(BaseModel):
    message: str
    completed: bool = False
    
class ItemCreate(ItemBase):
    context_name: Union[str, None] = None

class Item(ItemBase):
    id: int
    owner_id: int
    context_id: int
    
    class Config:
        from_attribute = True