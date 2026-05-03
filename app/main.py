from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.api import task_routes

app = FastAPI()

# 🔥 CORS FIX
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(task_routes.router)

@app.get("/health")
def health():
    return {"status": "Task Service Running"}