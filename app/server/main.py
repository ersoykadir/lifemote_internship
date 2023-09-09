"""
Kadir Ersoy
Internship Project
Server Main
Following the tutorial: https://fastapi.tiangolo.com/tutorial/
"""
import os
import uvicorn

from fastapi import FastAPI
from routers import users, items, contexts, auth

app = FastAPI()

app.include_router(users.router)
app.include_router(items.router)
app.include_router(contexts.router)
app.include_router(auth.router)


@app.get("/")
async def root():
    """Root"""
    return {"message": "Hello World"}

if __name__ == "__main__":
    uvicorn.run(
        "main:app",
        host=os.environ.get("HOST"),
        port=int(os.environ.get("PORT")),
        reload=True,
    )
