from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

import os
from dotenv import load_dotenv
load_dotenv()
host = os.getenv('MYSQL_HOST')
user = os.getenv('MYSQL_USER')
password = os.getenv('MYSQL_PASSWORD')
db = os.getenv('MYSQL_DB')
# host = os.environ['MYSQL_HOST']
# user = os.environ['MYSQL_USER']
# password = os.environ['MYSQL_PASSWORD']
# db = os.environ['MYSQL_DB']

SQLALCHEMY_DATABASE_URL = f"mysql+pymysql://{user}:{password}@{host}:3306/{db}"

engine = create_engine(
    SQLALCHEMY_DATABASE_URL
)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

from database import crud
from fastapi import Depends
from sqlalchemy.orm import Session

def init_db(db: Session = Depends(get_db)):
    # Create base users
    if not crud.get_user_by_email(db, name='admin'):
        crud.create_user(db, email='admin', password='admin')
    # Can we guarantee that the admin user will always have id 1?
    # Create base contexts
    if not crud.get_context_by_name_for_user(db, name='To-Do', user_id=1):
        crud.create_context(db, name='To-Do', description='Default to-do context', user_id=1)
    if not crud.get_context_by_name_for_user(db, name='In Progress', user_id=1):
        crud.create_context(db, name='In Progress', description='Default in progress context', user_id=1)
    if not crud.get_context_by_name_for_user(db, name='Done', user_id=1):
        crud.create_context(db, name='Done', description='Default done context', user_id=1)