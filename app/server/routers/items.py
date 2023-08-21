from typing import List
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

import schemas, crud
from database.db import get_db
# from ..dependencies import get_token_header

router = APIRouter(
    prefix="/items",
    tags=["items"],
    # dependencies=[Depends(get_token_header)],
    responses={404: {"description": "Not found"}},
)

@router.get("/{item_id}", response_model=schemas.Item, status_code=status.HTTP_200_OK)
def read_item(item_id: int, db: Session = Depends(get_db)):
    db_item = crud.item.get_item(db, item_id=item_id)
    if db_item is None:
        raise HTTPException(status_code=404, detail="Item not found")
    return db_item

@router.get("/", response_model=List[schemas.Item])
def read_items_for_user(user_id: int, db: Session = Depends(get_db)):
    db_items = crud.item.get_items_by_user(db, user_id=user_id)
    return db_items

@router.post("/", response_model=schemas.Item)
def create_item_for_user(
    user_id: int, item: schemas.ItemCreate, db: Session = Depends(get_db)
):
    if item.context_name is None:
        # Base context is to-do
        db_context = crud.context.get_context_by_name_for_user(db, context_name="To-Do", user_id=user_id)
        return crud.item.create_user_item(db=db, item=item, user_id=user_id, context_id=db_context.id)
    else:
        db_context = crud.context.get_context_by_name_for_user(db, context_name=item.context_name, user_id=user_id)
        if db_context is not None:
            return crud.item.create_user_item(db=db, item=item, user_id=user_id, context_id=db_context.id)
        else:
            raise HTTPException(status_code=404, detail="Context not found")

@router.put("/{item_id}", response_model=schemas.Item, status_code=status.HTTP_200_OK)
def update_item(item_id: int, item: schemas.ItemCreate, db: Session = Depends(get_db)):
    return crud.item.update_item(db=db, item_id=item_id, item=item)