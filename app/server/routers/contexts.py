"""
Kadir Ersoy
Internship Project
Context Router
"""
from typing import List
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

import crud
import schemas
from database.db import get_db
from utils.auth import get_current_user, validate_token

router = APIRouter(
    prefix="/contexts",
    tags=["contexts"],
    dependencies=[Depends(validate_token)],
    responses={404: {"description": "Not found"}},
)


@router.get("/all", response_model=List[schemas.Context])
def read_contexts_for_user(
    database: Session = Depends(get_db), user: schemas.User = Depends(get_current_user)
):
    """Get all contexts for a user"""
    db_user = crud.user.get_user(database, user_id=user.id)
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    db_contexts = crud.context.get_contexts_by_user(database, user_id=user.id)
    if db_contexts is None:
        raise HTTPException(status_code=404, detail="Contexts not found")
    return db_contexts


@router.get("/{context_id}", response_model=schemas.Context)
def read_context(
    context_id: int,
    database: Session = Depends(get_db),
    user: schemas.User = Depends(get_current_user),
):
    """Get a specific context by id"""
    db_context = crud.context.get_context(database, context_id=context_id)
    if db_context.owner_id != user.id:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="You do not have permission to access this context",
        )
    return db_context


@router.get("/", response_model=schemas.Context)
def get_context_by_name(
    context_name: str,
    database: Session = Depends(get_db),
    user: schemas.User = Depends(get_current_user),
):
    """Get a specific context by name"""
    db_context = crud.context.get_context_by_name_for_user(
        database, context_name=context_name, user_id=user.id
    )
    if db_context is None:
        raise HTTPException(status_code=404, detail="Context not found")
    # No need to check owner_id because get_context_by_name
    # gets contexts only for the current user
    return db_context


@router.post("/", response_model=schemas.Context)
def create_context_for_user(
    context: schemas.ContextBase,
    database: Session = Depends(get_db),
    user: schemas.User = Depends(get_current_user),
):
    """Create a context for a user"""
    db_context = crud.context.get_context_by_name_for_user(
        database, context_name=context.name, user_id=user.id
    )
    if db_context:
        raise HTTPException(status_code=400, detail="Context already exists!")
    return crud.context.create_context(database, context_data=context, user_id=user.id)


@router.put("/{context_id}", response_model=schemas.Context)
def update_context(
    context_id: int,
    context: schemas.ContextBase,
    database: Session = Depends(get_db),
    user: schemas.User = Depends(get_current_user),
):
    """Update a context"""
    db_context = crud.context.get_context(database, context_id=context_id)
    if db_context.owner_id != user.id:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="You do not have permission to access this context",
        )
    check_context = crud.context.get_context_by_name_for_user(
        database, context_name=context.name, user_id=user.id
    )
    if check_context:
        raise HTTPException(status_code=400, detail="Context already exists!")
    # update_data = context.dict(exclude_unset=True)
    return crud.context.update_context(database, context_id=context_id, context_data=context)


@router.delete("/{context_id}", response_model=schemas.Context)
def delete_context(
    context_id: int,
    database: Session = Depends(get_db),
    user: schemas.User = Depends(get_current_user),
):
    """Delete a context"""
    db_context = crud.context.get_context(database, context_id=context_id)
    if db_context.owner_id != user.id:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="You do not have permission to access this context",
        )
    return crud.context.delete_context(database, context_id=context_id)
