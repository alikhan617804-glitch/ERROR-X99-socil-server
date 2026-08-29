import requests
from fastapi import APIRouter

router = APIRouter(prefix="/api/instagram", tags=["Instagram"])

@router.get("/profile")
async def profile(access_token: str):
    r = requests.get(
        "https://graph.facebook.com/v23.0/me",
        params={"fields":"id,name","access_token":access_token}, timeout=30)
    return r.json()

@router.post("/media")
async def create_media(payload: dict):
    r = requests.post(
        f"https://graph.facebook.com/v23.0/{payload['ig_user_id']}/media",
        data={
            "image_url":payload["image_url"],
            "caption":payload.get("caption",""),
            "access_token":payload["access_token"],
        }, timeout=30)
    return r.json()

@router.post("/publish")
async def publish_media(payload: dict):
    r = requests.post(
        f"https://graph.facebook.com/v23.0/{payload['ig_user_id']}/media_publish",
        data={"creation_id":payload["creation_id"],"access_token":payload["access_token"]},
        timeout=30)
    return r.json()
