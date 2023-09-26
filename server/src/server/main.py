"""
Kadir Ersoy
Internship Project
Server Main
Following the tutorial: https://fastapi.tiangolo.com/tutorial/
"""
import os
import uvicorn

from fastapi import FastAPI
from server.routers import users, items, contexts, auth, extras

HOST = os.environ.get("HOST")
PORT = os.environ.get("PORT")

if HOST is None or PORT is None:
    raise ValueError("HOST and PORT environment variables must be set.")

app = FastAPI()

app.include_router(users.router)
app.include_router(items.router)
app.include_router(contexts.router)
app.include_router(auth.router)
app.include_router(extras.router)


@app.get("/")
async def root():
    """Root"""
    return {"message": "Hello World"}


if __name__ == "__main__":
    uvicorn.run(
        "main:app",
        host=HOST,
        port=int(PORT),
        reload=True,
    )
