"""
Kadir Ersoy
Internship Project
User Router
"""
from typing import List
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from server import crud
from server import schemas
from server.database.db import get_db

router = APIRouter(
    prefix="/users",
    tags=["users"],
    # dependencies=[Depends(get_token_header)],
    responses={404: {"description": "Not found"}},
)


@router.get("/", response_model=List[schemas.user.User])
def read_users(
    skip: int = 0, limit: int = 100, database: Session = Depends(get_db)
):
    """Get all users"""
    users = crud.user_instance.get_users(database, skip=skip, limit=limit)
    return users


@router.get("/{user_id}", response_model=schemas.user.User)
def read_user(user_id: int, database: Session = Depends(get_db)):
    """Get a specific user by id"""
    db_user = crud.user_instance.get_user(database, user_id=user_id)
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return db_user
