from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from fastapi.middleware.cors import CORSMiddleware
from kafka import KafkaConsumer
import json
import threading
import logging
import time
import os
import asyncio
from dotenv import load_dotenv
from pathlib import Path

# Load environment variables
env_path = Path(__file__).resolve().parent.parent / ".env"
load_dotenv(dotenv_path=env_path)

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

KAFKA_SERVER = os.getenv("KAFKA_SERVER")

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s | %(levelname)s | %(message)s'
)

logger = logging.getLogger(__name__)

connected_clients = []
main_loop = None

async def broadcast_message(data):
    disconnected = []

    for client in connected_clients:
        try:
            await client.send_json(data)
        except:
            disconnected.append(client)

    for client in disconnected:
        if client in connected_clients:
            connected_clients.remove(client)

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

                if main_loop:
                    asyncio.run_coroutine_threadsafe(
                        broadcast_message(data),
                        main_loop
                    )

        except Exception as e:
            logger.error(f"Kafka connection failed: {str(e)}")
            time.sleep(5)

@app.on_event("startup")
async def start_consumer():
    global main_loop

    main_loop = asyncio.get_running_loop()

    thread = threading.Thread(
        target=consume_messages,
        daemon=True
    )

    thread.start()

@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()

    connected_clients.append(websocket)

    logger.info("Frontend connected via WebSocket")

    try:
        while True:
            await websocket.receive_text()

    except WebSocketDisconnect:
        if websocket in connected_clients:
            connected_clients.remove(websocket)

        logger.info("Frontend disconnected")

@app.get("/")
def home():
    return {"message": "Notification Service Running"}

@app.get("/health")
def health():
    return {"status": "OK"}