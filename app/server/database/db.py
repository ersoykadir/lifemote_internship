from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

import os
from dotenv import load_dotenv
load_dotenv()
host = os.getenv("MYSQL_HOST")
user = os.getenv("MYSQL_USER")
password = os.getenv("MYSQL_PASSWORD")
db = os.getenv("MYSQL_DB")
# host = os.environ["MYSQL_HOST"]
# user = os.environ["MYSQL_USER"]
# password = os.environ["MYSQL_PASSWORD"]
# db = os.environ["MYSQL_DB"]

SQLALCHEMY_DATABASE_URL = f"mysql+pymysql://{user}:{password}@{host}:3306/{db}"

engine = create_engine(
    SQLALCHEMY_DATABASE_URL
)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

def validate_connection(db):
    try:
        conn = db.connection()
        return True
    except Exception as e:
        return False

from fastapi import Depends, HTTPException
# Dependency
def get_db():
    db = SessionLocal()
    if not validate_connection(db):
        print("Connection to database failed")
        raise HTTPException(status_code=500, detail="Internal server error")
    try:
        yield db
    finally:
        db.close()
