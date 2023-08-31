from sqlalchemy.orm import Session
from fastapi import HTTPException

from models import item as item_model
from schemas import item as item_schema

from .context import context

class Item:

    def get_item(self, db: Session, item_id: int):
        item = db.query(item_model.Item).filter(item_model.Item.id == item_id).first()
        if item is None:
            raise HTTPException(status_code=404, detail="Item not found")
        return item

    def get_items_by_user(self, db: Session, user_id: int):
        return db.query(item_model.Item).filter(item_model.Item.owner_id == user_id).all()

    def get_items_by_context_for_user(self, db: Session, user_id: int, context_id: int):
        return db.query(item_model.Item).filter(item_model.Item.owner_id == user_id, item_model.Item.context_id == context_id).all()

    def create_user_item(self, db: Session, item: item_schema.ItemCreate, user_id: int, context_id: int):
        db_item = item_model.Item(message=item.message, completed=item.completed, owner_id=user_id, context_id=context_id)
        db.add(db_item)
        db.commit()
        db.refresh(db_item)
        return db_item

    def update_item(self, db: Session, item_id: int, item: item_schema.ItemCreate):
        db_item = self.get_item(db, item_id=item_id)
        db_item.message = item.message
        db_item.completed = item.completed
        db_item.context_id = context.get_context_by_name_for_user(db, context_name=item.context_name, user_id=db_item.owner_id).id
        db.commit()
        db.refresh(db_item)
        return db_item
    
    def delete_item(self, db: Session, item_id: int):
        db_item = self.get_item(db, item_id=item_id)
        db.delete(db_item)
        db.commit()
        return db_item
    
item = Item()