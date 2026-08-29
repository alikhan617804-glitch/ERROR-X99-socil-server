import os
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from dotenv import load_dotenv

load_dotenv()

from routers import auth, youtube, tiktok, instagram

app = FastAPI(title="ERROR Social Manager", version="1.0.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:8000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth.router)
app.include_router(youtube.router)
app.include_router(tiktok.router)
app.include_router(instagram.router)

app.mount("/static", StaticFiles(directory="../frontend"), name="static")

@app.get("/")
async def home():
    return FileResponse("../frontend/index.html")

@app.get("/health")
async def health():
    return {"status": "online", "service": "ERROR Social Manager"}
