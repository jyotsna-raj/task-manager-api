from sqlalchemy.orm import Session
from app.repository import task_repository
import json
import os
from dotenv import load_dotenv
from pathlib import Path

# 🔥 Absolute path fix
env_path = Path(__file__).resolve().parent.parent.parent / ".env"
load_dotenv(dotenv_path=env_path)

KAFKA_SERVER = os.getenv("KAFKA_SERVER")

def create_task(db: Session, title: str, description: str):
    task = task_repository.create_task(db, title, description)

    try:
        from kafka import KafkaProducer

        producer = KafkaProducer(
            bootstrap_servers=KAFKA_SERVER,
            value_serializer=lambda v: json.dumps(v).encode('utf-8')
        )

        producer.send(
            'task-events',
            {
                "event": "task_created",
                "title": title,
                "description": description
            }
        )

    except Exception as e:
        print(f"Kafka error: {str(e)}")

    return task


def get_tasks(db: Session):
    return task_repository.get_tasks(db)


def get_task(db: Session, task_id: int):
    return task_repository.get_task(db, task_id)


def delete_task(db: Session, task_id: int):
    return task_repository.delete_task(db, task_id)