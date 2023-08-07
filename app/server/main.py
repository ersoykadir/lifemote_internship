# Following this tutorial: https://fastapi.tiangolo.com/tutorial/sql-databases/

from typing import List

from fastapi import Depends, FastAPI, HTTPException, status
from sqlalchemy.orm import Session

from database import crud, models, schemas
from database.db import SessionLocal, engine

models.Base.metadata.create_all(bind=engine)

app = FastAPI()

# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.post("/items/", response_model=schemas.Item, status_code=status.HTTP_201_CREATED)
def create_item(item: schemas.ItemCreate, db: Session = Depends(get_db)):
    return crud.create_item(db=db, item=item)


@app.get("/items/{item_id}", response_model=schemas.Item, status_code=status.HTTP_200_OK)
def read_item(item_id: int, db: Session = Depends(get_db)):
    db_item = crud.get_item(db, item_id=item_id)
    if db_item is None:
        raise HTTPException(status_code=404, detail="Item not found")
    return db_item

import uvicorn, os

if __name__ == "__main__":
   uvicorn.run("main:app", host=os.environ.get('HOST'), port=int(os.environ.get('PORT')), reload=True)