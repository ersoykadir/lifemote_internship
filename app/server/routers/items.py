from typing import List
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

import schemas, crud
from database.db import get_db
from utils.auth import get_current_user, validate_token

router = APIRouter(
    prefix="/items",
    tags=["items"],
    dependencies=[Depends(validate_token)],
    responses={404: {"description": "Not found"}},
)


@router.get("/all", response_model=List[schemas.Item], status_code=status.HTTP_200_OK)
def read_items_for_user(
    db: Session = Depends(get_db), user: schemas.User = Depends(get_current_user)
):
    db_items = crud.item.get_items_by_user(db, user_id=user.id)
    return db_items


@router.get("/{item_id}", response_model=schemas.Item, status_code=status.HTTP_200_OK)
def read_item(
    item_id: int,
    db: Session = Depends(get_db),
    user: schemas.User = Depends(get_current_user),
):
    db_item = crud.item.get_item(db, item_id=item_id)
    if db_item.owner_id != user.id:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="You do not have permission to access this item",
        )
    return db_item


@router.post("/", response_model=schemas.Item, status_code=status.HTTP_201_CREATED)
def create_item_for_user(
    item: schemas.ItemCreate,
    db: Session = Depends(get_db),
    user: schemas.User = Depends(get_current_user),
):
    if item.context_name is None:
        # Base context is to-do
        db_context = crud.context.get_context_by_name_for_user(
            db, context_name="To-Do", user_id=user.id
        )
        if db_context is None:
            raise HTTPException(status_code=404, detail="Context not found")
        if db_context.owner_id != user.id:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="You do not have permission to access this context",
            )
        return crud.item.create_user_item(
            db=db, item=item, user_id=user.id, context_id=db_context.id
        )
    else:
        db_context = crud.context.get_context_by_name_for_user(
            db, context_name=item.context_name, user_id=user.id
        )
        if db_context is None:
            raise HTTPException(status_code=404, detail="Context not found")
        return crud.item.create_user_item(
            db=db, item=item, user_id=user.id, context_id=db_context.id
        )


@router.put("/{item_id}", response_model=schemas.Item, status_code=status.HTTP_200_OK)
def update_item(
    item_id: int,
    item: schemas.ItemCreate,
    db: Session = Depends(get_db),
    user: schemas.User = Depends(get_current_user),
):
    db_item = crud.item.get_item(db, item_id=item_id)
    if db_item.owner_id != user.id:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="You do not have permission to access this context",
        )
    db_context = crud.context.get_context_by_name_for_user(
        db, context_name=item.context_name, user_id=user.id
    )
    if db_context is None:
        raise HTTPException(status_code=404, detail="Context not found")
    return crud.item.update_item(db=db, item_id=item_id, item=item)


@router.delete("/{item_id}", status_code=status.HTTP_200_OK)
def delete_item(item_id: int, db: Session = Depends(get_db), user: schemas.User = Depends(get_current_user)):
    db_item = crud.item.get_item(db, item_id=item_id)
    if db_item.owner_id != user.id:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="You do not have permission to access this context",
        )
    return crud.item.delete_item(db=db, item_id=item_id)
