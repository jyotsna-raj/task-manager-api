from sqlalchemy.orm import Session
from app.repository import task_repository


def create_task(db: Session, title: str, description: str):
    return task_repository.create_task(db, title, description)


def get_tasks(db: Session):
    return task_repository.get_tasks(db)


def get_task(db: Session, task_id: int):
    return task_repository.get_task(db, task_id)


def delete_task(db: Session, task_id: int):
    return task_repository.delete_task(db, task_id)