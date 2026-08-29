import requests
from fastapi import APIRouter, Header, HTTPException

router = APIRouter(prefix="/api/tiktok", tags=["TikTok"])

def token(authorization):
    if not authorization:
        raise HTTPException(401, "Authorization token required")
    return authorization

@router.get("/creator")
async def creator_info(authorization: str = Header(None)):
    r = requests.post(
        "https://open.tiktokapis.com/v2/post/publish/creator_info/query/",
        headers={"Authorization": token(authorization), "Content-Type":"application/json"},
        timeout=30)
    return r.json()

@router.post("/publish")
async def publish_video(payload: dict, authorization: str = Header(None)):
    body = {
        "post_info": {
            "title": payload.get("title",""),
            "privacy_level": payload.get("privacy_level","SELF_ONLY"),
            "disable_duet": False,
            "disable_comment": False,
            "disable_stitch": False,
        },
        "source_info": {
            "source": "PULL_FROM_URL",
            "video_url": payload["video_url"],
        }
    }
    r = requests.post(
        "https://open.tiktokapis.com/v2/post/publish/video/init/",
        headers={"Authorization": token(authorization), "Content-Type":"application/json"},
        json=body, timeout=30)
    return r.json()

@router.post("/status")
async def publish_status(payload: dict, authorization: str = Header(None)):
    r = requests.post(
        "https://open.tiktokapis.com/v2/post/publish/status/fetch/",
        headers={"Authorization": token(authorization), "Content-Type":"application/json"},
        json={"publish_id":payload["publish_id"]}, timeout=30)
    return r.json()
