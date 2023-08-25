# Following this tutorial: https://fastapi.tiangolo.com/tutorial/sql-databases/

from typing import List

from fastapi import Depends, FastAPI, HTTPException, status
from sqlalchemy.orm import Session

from database.db import SessionLocal, engine, get_db

# models.Base.metadata.create_all(bind=engine)
# The above line is commented out because we are using Alembic to manage our database migrations.

from routers import users, items, contexts, auth

app = FastAPI()

# app.include_router(users.router)
app.include_router(items.router)
app.include_router(contexts.router)
app.include_router(auth.router)


@app.get("/")
async def root():
    return {"message": "Hello World"}


import uvicorn, os

if __name__ == "__main__":
    uvicorn.run(
        "main:app",
        host=os.environ.get("HOST"),
        port=int(os.environ.get("PORT")),
        reload=True,
    )
