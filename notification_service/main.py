from fastapi import FastAPI
from kafka import KafkaConsumer
import json
import threading
import logging
import time
import os
from dotenv import load_dotenv
from pathlib import Path

# 🔥 Absolute path fix
env_path = Path(__file__).resolve().parent.parent / ".env"
load_dotenv(dotenv_path=env_path)

app = FastAPI()

KAFKA_SERVER = os.getenv("KAFKA_SERVER")

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s | %(levelname)s | %(message)s'
)

logger = logging.getLogger(__name__)

def consume_messages():
    while True:
        try:
            consumer = KafkaConsumer(
                'task-events',
                bootstrap_servers=KAFKA_SERVER,
                group_id='notification-group',
                auto_offset_reset='earliest',
                enable_auto_commit=True,
                value_deserializer=lambda x: json.loads(x.decode('utf-8'))
            )

            logger.info(f"Connected to Kafka at {KAFKA_SERVER}")

            for message in consumer:
                data = message.value
                logger.info(f"Notification received | {data}")

        except Exception as e:
            logger.error(f"Kafka connection failed: {str(e)}")
            time.sleep(5)

@app.on_event("startup")
def start_consumer():
    thread = threading.Thread(target=consume_messages, daemon=True)
    thread.start()

@app.get("/")
def home():
    return {"message": "Notification Service Running"}

@app.get("/health")
def health():
    return {"status": "OK"}