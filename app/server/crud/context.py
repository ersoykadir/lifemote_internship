from sqlalchemy.orm import Session
from fastapi import HTTPException

from models import context as context_model
from schemas import context as context_schema

class Context():

    def get_context(self, db: Session, context_id: int):
        return db.query(context_model.Context).filter(context_model.Context.id == context_id).first()

    def get_context_by_name_for_user(self, db: Session, context_name: str, user_id: int):
        return db.query(context_model.Context).filter(context_model.Context.name == context_name, context_model.Context.owner_id == user_id).first()

    def get_contexts_by_user(self, db: Session, user_id: int):
        return db.query(context_model.Context).filter(context_model.Context.owner_id == user_id).all()

    def create_context(self, db: Session, context: context_schema.ContextCreate, user_id: int):
        db_context = context_model.Context(**context.dict(), owner_id=user_id)
        db.add(db_context)
        db.commit()
        db.refresh(db_context)
        return db_context

    def init_user_contexts(self, db: Session, user_id: int):
        context = context_schema.ContextCreate(name='To-Do', description='Default to-do context')
        self.create_context(db, context=context, user_id=user_id)
        context = context_schema.ContextCreate(name='In Progress', description='Default in progress context')
        self.create_context(db, context=context, user_id=user_id)
        context = context_schema.ContextCreate(name='Done', description='Default done context')
        self.create_context(db, context=context, user_id=user_id)

context = Context()