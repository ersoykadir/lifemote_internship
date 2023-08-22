from typing import List
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

import schemas, crud
from database.db import get_db
from utils.auth import get_current_user, validate_token

router = APIRouter(
    prefix="/contexts",
    tags=["contexts"],
    dependencies=[Depends(validate_token)],
    responses={404: {"description": "Not found"}},
)


@router.get("/{context_id}", response_model=schemas.Context)
def read_context(
    context_id: int,
    db: Session = Depends(get_db),
    user: schemas.User = Depends(get_current_user),
):
    db_context = crud.context.get_context(db, context_id=context_id)
    if db_context is None:
        raise HTTPException(status_code=404, detail="Context not found")
    return db_context


@router.post("/", response_model=schemas.Context)
def create_context_for_user(
    context: schemas.ContextCreate,
    db: Session = Depends(get_db),
    user: schemas.User = Depends(get_current_user),
):
    db_context = crud.context.get_context_by_name_for_user(
        db, context_name=context.name, user_id=user.id
    )
    if db_context:
        raise HTTPException(status_code=400, detail="Context already exists")
    return crud.context.create_context(db=db, context=context, user_id=user.id)


@router.get("/", response_model=List[schemas.Context])
def read_contexts_for_user(
    db: Session = Depends(get_db), user: schemas.User = Depends(get_current_user)
):
    db_user = crud.user.get_user(db, user_id=user.id)
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    db_contexts = crud.context.get_contexts_by_user(db, user_id=user.id)
    if db_contexts is None:
        raise HTTPException(status_code=404, detail="Contexts not found")
    return db_contexts
