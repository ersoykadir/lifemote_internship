"""
Kadir Ersoy
Internship Project
Extras Router
"""
from typing import List
from pydantic import BaseModel
from fastapi import APIRouter, status, Depends, HTTPException, Response
from sqlalchemy.orm import Session

import crud
from database.db import get_db
from utils.auth import get_current_user
from models.item import Item

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

class SortBase(BaseModel):
    """Context base schema"""
    items: List
    property_name: str

class SortBasev1(BaseModel):
    """Context base schema"""
    property_name: str
    context_id: int

class AppendBase(BaseModel):
    """Context base schema"""
    items1: List
    items2: List

class FilterCompletionBase(BaseModel):
    """Context base schema"""
    items: List
    completed: bool

def get_context_items(
    input_data: SortBasev1,
    user: str = Depends(get_current_user),
    database: Session = Depends(get_db)
):
    """Dependency"""
    items = crud.item.get_items_by_context_for_user(database, user_id=user.id, context_id=input_data.context_id)
    return items

# Sort a list of dictionaries by a property
@router.post("/sort_items")
def sort_items(response: Response, input_data: SortBase):
    """Sort a list of dictionaries by a property"""
    if len(input_data.items) == 0:
        return []
    if isinstance(input_data.items[0], dict):
        return sorted(input_data.items, key=lambda x: x[input_data.property_name].lower())
    else:
        response.status_code = status.HTTP_400_BAD_REQUEST
        return HTTPException(status_code=400, detail="Must be a list of dictionaries!")

# Sort a list of dictionaries by a property
@router.post("/sort_itemsv1")
def sort_itemsv1(
    response: Response,
    input_data: SortBasev1,
    items = Depends(get_context_items),
):
    """Sort a list of items by a property"""
    # if items is a list of dictionaries
    if not isinstance(items, list):
        response.status_code = status.HTTP_400_BAD_REQUEST
        return HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Input should be a valid list")
    if len(items) == 0:
        return []
    if isinstance(items[0], Item):
        return sorted(items, key=lambda x: getattr(x, input_data.property_name).lower())
    else:
        response.status_code = status.HTTP_400_BAD_REQUEST
        return HTTPException(status_code=400, detail="Must be a list of item objects!")

@router.post("/add_two_lists")
def add_two_lists(list1: list, list2: list):
    """Add two lists"""
    return [list1[i] + list2[i] for i in range(len(list1))]

@router.post("/append_lists")
def append_lists(input_data: AppendBase):
    """Append two lists"""
    return input_data.items1 + input_data.items2

@router.post("/filter_list")
def filter_list(input_data: FilterCompletionBase):
    """Filter a list"""
    return [item for item in input_data.items if item['completed'] is input_data.completed]