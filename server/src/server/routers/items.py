"""
Kadir Ersoy
Internship Project
Item Router
"""
from typing import List
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from server import crud
from server import schemas
from server.database.db import get_db
from server.utils.auth import get_current_user, validate_token

router = APIRouter(
    prefix="/items",
    tags=["items"],
    dependencies=[Depends(validate_token)],
    responses={404: {"description": "Not found"}},
)


@router.get(
    "/all",
    response_model=List[schemas.item.Item],
    status_code=status.HTTP_200_OK
)
def read_items_for_user(
    database: Session = Depends(get_db),
    user: schemas.user.User = Depends(get_current_user)
):
    """Get all items for a user"""
    db_items = crud.item_instance.get_items_by_user(database, user_id=user.id)
    return db_items


@router.get(
    "/{item_id}",
    response_model=schemas.item.Item,
    status_code=status.HTTP_200_OK
)
def read_item(
    item_id: int,
    database: Session = Depends(get_db),
    user: schemas.user.User = Depends(get_current_user),
):
    """Get a specific item by id"""

    db_item = crud.item_instance.get_item(database, item_id=item_id)
    if db_item.owner_id != user.id:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="You do not have permission to access this item",
        )
    return db_item


@router.post(
    "/",
    response_model=schemas.item.Item,
    status_code=status.HTTP_201_CREATED
)
def create_item_for_user(
    item: schemas.item.ItemCreate,
    database: Session = Depends(get_db),
    user: schemas.user.User = Depends(get_current_user),
):
    """Create an item for a user"""

    db_context = crud.context_instance.get_context_by_name_for_user(
        database, context_name=item.context_name, user_id=user.id
    )
    if db_context is None:
        raise HTTPException(status_code=404, detail="Context not found")
    return crud.item_instance.create_user_item(
        database, item_data=item, user_id=user.id, context_id=db_context.id
    )


@router.put(
    "/{item_id}",
    response_model=schemas.item.Item,
    status_code=status.HTTP_200_OK
)
def update_item(
    item_id: int,
    item: schemas.item.ItemCreate,
    database: Session = Depends(get_db),
    user: schemas.user.User = Depends(get_current_user),
):
    """Update an item"""

    db_item = crud.item_instance.get_item(database, item_id=item_id)
    if db_item.owner_id != user.id:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="You do not have permission to access this context",
        )
    db_context = crud.context_instance.get_context_by_name_for_user(
        database, context_name=item.context_name, user_id=user.id
    )
    if db_context is None:
        raise HTTPException(status_code=404, detail="Context not found")
    return crud.item_instance.update_item(database, item_id=item_id, item_data=item)


@router.delete("/{item_id}", status_code=status.HTTP_200_OK)
def delete_item(
    item_id: int,
    database: Session = Depends(get_db),
    user: schemas.user.User = Depends(get_current_user),
):
    """Delete an item"""

    db_item = crud.item_instance.get_item(database, item_id=item_id)
    if db_item.owner_id != user.id:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="You do not have permission to access this context",
        )
    return crud.item_instance.delete_item(database, item_id=item_id)
