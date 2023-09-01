"""
Kadir Ersoy
Internship Project
Context CRUD
"""
from sqlalchemy.orm import Session
from fastapi import HTTPException

from models import context as context_model
from schemas import context as context_schema
class Context():
    """Context CRUD"""

    def get_context(self, database: Session, context_id: int):
        """Get context by id"""
        db_context = database.query(context_model.Context).filter(
            context_model.Context.id == context_id
        ).first()
        if db_context is None:
            raise HTTPException(status_code=404, detail="Context not found")
        return db_context

    def get_context_by_name_for_user(self, database: Session, context_name: str, user_id: int):
        """Get context by name for user"""
        db_context = database.query(context_model.Context).filter(
            context_model.Context.name == context_name,
            context_model.Context.owner_id == user_id
        ).first()
        # if context is None:
        #     raise HTTPException(status_code=404, detail="Context not found")
        return db_context

    def get_contexts_by_user(self, database: Session, user_id: int):
        """Get all contexts for user"""
        return database.query(context_model.Context).filter(
            context_model.Context.owner_id == user_id
            ).all()

    def create_context(self, database: Session, context: context_schema.ContextCreate, user_id: int):
        """Create context"""
        db_context = context_model.Context(**context.dict(), owner_id=user_id)
        database.add(db_context)
        database.commit()
        database.refresh(db_context)
        return db_context

    def init_user_contexts(self, database: Session, user_id: int):
        """Create default contexts for user"""

        context_todo = context_schema.ContextCreate(
            name='To-Do', 
            description='Default to-do context'
        )
        context_inprogress = context_schema.ContextCreate(
            name='In Progress', 
            description='Default in progress context'
        )
        context_done = context_schema.ContextCreate(
            name='Done', 
            description='Default done context'
        )
        self.create_context(database, context=context_todo, user_id=user_id)
        self.create_context(database, context=context_inprogress, user_id=user_id)
        self.create_context(database, context=context_done, user_id=user_id)

    def update_context(self, database: Session, context_id: int, context: context_schema.ContextCreate):
        db_context = self.get_context(database, context_id=context_id)
        db_context.name = context.name
        db_context.description = context.description
        database.commit()
        database.refresh(db_context)
        return db_context

    def delete_context(self, database: Session, context_id: int):
        db_context = self.get_context(database, context_id=context_id)
        database.delete(db_context)
        database.commit()
        return db_context


context = Context()
