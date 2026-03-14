from fastapi import FastAPI
from app.database.db import engine, Base
from app.models import task_model
from app.api import task_routes

app = FastAPI()

Base.metadata.create_all(bind=engine)

app.include_router(task_routes.router)

@app.get("/")
def home():
    return {"message": "Task Manager API Running"}