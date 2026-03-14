from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.database.db import get_db
from app.schemas.task_schema import TaskCreate
from app.services import task_service

router = APIRouter()


@router.post("/tasks")
def create_task(task: TaskCreate, db: Session = Depends(get_db)):
    return task_service.create_task(db, task.title, task.description)


@router.get("/tasks")
def get_tasks(db: Session = Depends(get_db)):
    return task_service.get_tasks(db)


@router.get("/tasks/{task_id}")
def get_task(task_id: int, db: Session = Depends(get_db)):
    return task_service.get_task(db, task_id)


@router.delete("/tasks/{task_id}")
def delete_task(task_id: int, db: Session = Depends(get_db)):
    return task_service.delete_task(db, task_id)