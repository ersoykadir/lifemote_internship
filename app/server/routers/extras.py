"""
Kadir Ersoy
Internship Project
Extras Router
"""
from typing import List
from fastapi import APIRouter, status
from sqlalchemy.orm import Session

import crud
import schemas
from database.db import get_db

router = APIRouter(
    prefix="/extras",
    tags=["extras"],
    # dependencies=[Depends(get_token_header)],
    responses={404: {"description": "Not found"}},
)

# Sort context items by their message
# Sort list of context dictionaries by their number of items
# Combine two context items into a single context
    # contextname1, contextname2, newcontextname 
# Maybe we can have a route to filter the items by their completion status

from typing import List
from pydantic import BaseModel

class SortBase(BaseModel):
    """Context base schema"""
    items: List
    property_name: str

class AppendBase(BaseModel):
    """Context base schema"""
    items1: List
    items2: List

class FilterCompletionBase(BaseModel):
    """Context base schema"""
    items: List
    completed: bool

# Sort a list of dictionaries by a property
@router.post("/sort_items", status_code=status.HTTP_200_OK)
def sort_items(input_data: SortBase):
    """Sort a list of dictionaries by a property"""
    return sorted(input_data.items, key=lambda x: x[input_data.property_name].lower())

# """Sort a dictionary by its keys"""
# keys = list(dictionary.keys())
# keys.sort()
# return [dictionary[key] for key in keys]


@router.post("/add_two_lists", status_code=status.HTTP_200_OK)
def add_two_lists(list1: list, list2: list):
    """Add two lists"""
    return [list1[i] + list2[i] for i in range(len(list1))]

@router.post("/append_lists", status_code=status.HTTP_200_OK)
def append_lists(input_data: AppendBase):
    """Append two lists"""
    return input_data.items1 + input_data.items2

@router.post("/filter_list", status_code=status.HTTP_200_OK)
def filter_list(input_data: FilterCompletionBase):
    """Filter a list"""
    return [item for item in input_data.items if item['completed'] == input_data.completed]