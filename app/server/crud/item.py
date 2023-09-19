"""
Kadir Ersoy
Internship Project
Item CRUD
"""
from sqlalchemy.orm import Session
from fastapi import HTTPException

from models import item as item_model
from schemas import item as item_schema

from .context import context

class Item:
    """Item CRUD"""

    def get_item(self, database: Session, item_id: int):
        """Get item by id"""
        db_item = database.query(item_model.Item).filter(item_model.Item.id == item_id).first()
        if db_item is None:
            raise HTTPException(status_code=404, detail="Item not found")
        return db_item

    def get_items_by_user(self, database: Session, user_id: int):
        """Get all items for user"""
        return database.query(item_model.Item).filter(item_model.Item.owner_id == user_id).all()

    def get_items_by_context_for_user(self, database: Session, user_id: int, context_id: int):
        """Get all items for user in context"""
        return database.query(item_model.Item).filter(
            item_model.Item.owner_id == user_id,
            item_model.Item.context_id == context_id
        ).all()

    def create_user_item(
        self,
        database: Session,
        item_data: item_schema.ItemCreate,
        user_id: int, context_id: int
    ):
        """Create item"""
        db_item = item_model.Item(
            message=item_data.message,
            completed=item_data.completed,
            owner_id=user_id,
            context_id=context_id
        )
        database.add(db_item)
        database.commit()
        database.refresh(db_item)
        return db_item

    def update_item(self, database: Session, item_id: int, item_data: item_schema.ItemCreate):
        """Update item"""
        db_item = self.get_item(database, item_id=item_id)
        db_item.message = item_data.message
        db_item.completed = item_data.completed
        db_item.context_id = context.get_context_by_name_for_user(
            database, context_name=item_data.context_name, user_id=db_item.owner_id
        ).id
        database.commit()
        database.refresh(db_item)
        return db_item

    def delete_item(self, database: Session, item_id: int):
        """Delete item"""
        db_item = self.get_item(database, item_id=item_id)
        database.delete(db_item)
        database.commit()
        return db_item

item = Item()
