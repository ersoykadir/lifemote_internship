"""
Kadir Ersoy
Internship Project
User Router
"""
from typing import List
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

import crud
import schemas
from database.db import get_db

router = APIRouter(
    prefix="/users",
    tags=["users"],
    # dependencies=[Depends(get_token_header)],
    responses={404: {"description": "Not found"}},
)

@router.post("/", response_model=schemas.User)
def create_user(user: schemas.UserBase, database: Session = Depends(get_db)):
    """Create a new user"""
    db_user = crud.user.get_user_by_email(database, email=user.email)
    if db_user:
        raise HTTPException(status_code=400, detail="Email already registered")
    return crud.user.create_user(database, user_data=user)

@router.get("/", response_model=List[schemas.User])
def read_users(skip: int = 0, limit: int = 100, database: Session = Depends(get_db)):
    """Get all users"""
    users = crud.user.get_users(database, skip=skip, limit=limit)
    return users

@router.get("/{user_id}", response_model=schemas.User)
def read_user(user_id: int, database: Session = Depends(get_db)):
    """Get a specific user by id"""
    db_user = crud.user.get_user(database, user_id=user_id)
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return db_user
