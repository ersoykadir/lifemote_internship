"""
Kadir Ersoy
Internship Project
Database
"""
import os
from dotenv import load_dotenv

from fastapi import HTTPException
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy.exc import OperationalError

load_dotenv()
host = os.getenv('MYSQL_HOST')
user = os.getenv('MYSQL_USER')
password = os.getenv('MYSQL_PASSWORD')
db_name = os.getenv('MYSQL_DB')

SQLALCHEMY_DATABASE_URL = f"mysql+pymysql://{user}:{password}@{host}:3306/{db_name}"

engine = create_engine(
    SQLALCHEMY_DATABASE_URL
)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

def validate_connection(database):
    """ Validate database connection """
    try:
        database.connection()
        return True
    except OperationalError:
        return False

def get_db():
    """ Get database """
    database = SessionLocal()
    if not validate_connection(database):
        print("Connection to database failed")
        raise HTTPException(status_code=500, detail="Internal server error")
    try:
        yield database
    finally:
        database.close()
