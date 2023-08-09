from sqlalchemy.orm import Session

from . import models, schemas


def get_items(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Item).offset(skip).limit(limit).all()

def create_item(db: Session, item: schemas.ItemCreate):
    db_item = models.Item(message=item.message)
    db.add(db_item)
    db.commit()
    db.refresh(db_item)
    return db_item

def update_item(db: Session, item: schemas.Item, completed: bool):
    item.completed = completed
    db.commit()
    db.refresh(item)
    return item

def get_user(db: Session, user_id: int):
    return db.query(models.User).filter(models.User.id == user_id).first()


def get_user_by_email(db: Session, email: str):
    return db.query(models.User).filter(models.User.email == email).first()


def get_users(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.User).offset(skip).limit(limit).all()

def create_user(db: Session, user: schemas.UserCreate):
    db_user = models.User(email=user.email, password=user.password)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

def create_user_item(db: Session, item: schemas.ItemCreate, user_id: int, context_id: int):
    db_item = models.Item(**item.dict(), owner_id=user_id, context_id=context_id)
    db.add(db_item)
    db.commit()
    db.refresh(db_item)
    return db_item

def get_item(db: Session, item_id: int):
    return db.query(models.Item).filter(models.Item.id == item_id).first()

def get_items_by_user(db: Session, user_id: int):
    return db.query(models.Item).filter(models.Item.owner_id == user_id).all()

def get_items_by_context_for_user(db: Session, user_id: int, context_id: int):
    return db.query(models.Item).filter(models.Item.owner_id == user_id).all()

def create_context(db: Session, context: schemas.ContextCreate, user_id: int):
    db_context = models.Item(**context.dict(), owner_id=user_id)
    db.add(db_context)
    db.commit()
    db.refresh(db_context)
    return db_context

def get_context(db: Session, context_id: int):
    return db.query(models.Context).filter(models.Context.id == context_id).first()

def get_context_by_name_for_user(db: Session, context_id: int, user_id: int):
    return db.query(models.Context).filter(models.Context.id == context_id, models.Context.owner_id == user_id).first()

def get_contexts_by_user(db: Session, user_id: int):
    return db.query(models.Context).filter(models.Context.owner_id == user_id).all()