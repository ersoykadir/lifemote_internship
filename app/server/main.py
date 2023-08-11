# Following this tutorial: https://fastapi.tiangolo.com/tutorial/sql-databases/

from typing import List

from fastapi import Depends, FastAPI, HTTPException, status
from sqlalchemy.orm import Session

from database import crud, models, schemas
from database.db import SessionLocal, engine

# models.Base.metadata.create_all(bind=engine)
# The above line is commented out because we are using Alembic to manage our database migrations.

app = FastAPI()

# # Dependency
# def get_db():
#     db = SessionLocal()
#     try:
#         yield db
#     finally:
#         db.close()
from database.db import get_db


@app.post("/items/", response_model=schemas.Item, status_code=status.HTTP_201_CREATED)
def create_item(item: schemas.ItemCreate, db: Session = Depends(get_db)):
    return crud.create_item(db=db, item=item)


@app.get("/items/{item_id}", response_model=schemas.Item, status_code=status.HTTP_200_OK)
def read_item(item_id: int, db: Session = Depends(get_db)):
    db_item = crud.get_item(db, item_id=item_id)
    if db_item is None:
        raise HTTPException(status_code=404, detail="Item not found")
    return db_item

@app.get("/items/", response_model=List[schemas.Item])
def read_items(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    items = crud.get_items(db, skip=skip, limit=limit)
    return items

@app.post("/users/", response_model=schemas.User)
def create_user(user: schemas.UserCreate, db: Session = Depends(get_db)):
    db_user = crud.get_user_by_email(db, email=user.email)
    if db_user:
        raise HTTPException(status_code=400, detail="Email already registered")
    return crud.create_user(db=db, user=user)

@app.get("/users/", response_model=List[schemas.User])
def read_users(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    users = crud.get_users(db, skip=skip, limit=limit)
    return users

@app.get("/users/{user_id}", response_model=schemas.User)
def read_user(user_id: int, db: Session = Depends(get_db)):
    db_user = crud.get_user(db, user_id=user_id)
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return db_user

@app.post("/users/{user_id}/items/", response_model=schemas.Item)
def create_item_for_user(
    user_id: int, item: schemas.ItemCreate, db: Session = Depends(get_db)
):
    if item.context_name is None:
        # Base context is to-do
        db_context = crud.get_context_by_name_for_user(db, context_name="To-Do", user_id=user_id)
        return crud.create_user_item(db=db, item=item, user_id=user_id, context_id=db_context.id)
    else:
        db_context = crud.get_context_by_name_for_user(db, context_name=item.context_name, user_id=user_id)
        if db_context is not None:
            return crud.create_user_item(db=db, item=item, user_id=user_id, context_id=db_context.id)
        else:
            raise HTTPException(status_code=404, detail="Context not found")
        
@app.get("/users/{user_id}/items/", response_model=List[schemas.Item])
def read_items_for_user(user_id: int, db: Session = Depends(get_db)):
    db_items = crud.get_items_by_user(db, user_id=user_id)
    return db_items

@app.post("/users/{user_id}/contexts/", response_model=schemas.Context)
def create_context_for_user(
    user_id: int, context: schemas.ContextCreate, db: Session = Depends(get_db)
):
    db_context = crud.get_context_by_name_for_user(db, context_name=context.name, user_id=user_id)
    if db_context:
        raise HTTPException(status_code=400, detail="Context already exists")
    return crud.create_context(db=db, context=context, user_id=user_id)

@app.get("/users/{user_id}/contexts/", response_model=List[schemas.Context])
def read_contexts_for_user(user_id: int, db: Session = Depends(get_db)):
    db_user = crud.get_user(db, user_id=user_id)
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    db_contexts = crud.get_contexts_by_user(db, user_id=user_id)
    if db_contexts is None:
        raise HTTPException(status_code=404, detail="Contexts not found")
    return db_contexts

@app.get("/users/{user_id}/items/", response_model=List[schemas.Item])
def read_items_for_user(user_id: int, db: Session = Depends(get_db)):
    db_user = crud.get_user(db, user_id=user_id)
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    db_items = crud.get_items_by_user(db, user_id=user_id)
    if db_items is None:
        raise HTTPException(status_code=404, detail="Contexts not found")
    return db_items

@app.get("/users/{user_id}/contexts/{context}/items/", response_model=List[schemas.Item])
def read_items_for_user_in_context(user_id: int, context: str, db: Session = Depends(get_db)):
    db_context = crud.get_context_by_name_for_user(db, context, user_id=user_id)
    if db_context is None:
        raise HTTPException(status_code=404, detail="Context not found")
    return crud.get_items_by_context_for_user(db, user_id=user_id, context_id=db_context.id)


@app.put("/items/{item_id}", response_model=schemas.Item, status_code=status.HTTP_200_OK)
def update_item(item_id: int, item: schemas.ItemCreate, db: Session = Depends(get_db)):
    return crud.update_item(db=db, item_id=item_id, item=item)

import uvicorn, os

if __name__ == "__main__":
    uvicorn.run("main:app", host=os.environ.get('HOST'), port=int(os.environ.get('PORT')), reload=True)