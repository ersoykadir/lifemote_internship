from sqlalchemy.orm import Session
from fastapi import HTTPException

from models import user as user_model
from schemas import user as user_schema

from .context import context

class User():
    def get_user(self, db: Session, user_id: int):
        return db.query(user_model.User).filter(user_model.User.id == user_id).first()

    def get_user_by_email(self, db: Session, email: str):
        return db.query(user_model.User).filter(user_model.User.email == email).first()

    def get_users(self, db: Session, skip: int = 0, limit: int = 100):
        return db.query(user_model.User).offset(skip).limit(limit).all()

    def create_user(self, db: Session, user: user_schema.UserCreate):
        db_user = user.User(email=user.email, password=user.password)
        db.add(db_user)
        db.commit()
        db.refresh(db_user)
        context.init_user_contexts(db, user_id=db_user.id)
        return db_user
    
user = User()