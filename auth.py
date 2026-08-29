import os, secrets
from urllib.parse import urlencode
import requests
from fastapi import APIRouter
from fastapi.responses import RedirectResponse

router = APIRouter(prefix="/auth", tags=["Authentication"])

@router.get("/youtube")
async def youtube_login():
    params = {
        "client_id": os.getenv("GOOGLE_CLIENT_ID"),
        "redirect_uri": os.getenv("GOOGLE_REDIRECT_URI"),
        "response_type": "code",
        "scope": "https://www.googleapis.com/auth/youtube.upload https://www.googleapis.com/auth/youtube.readonly",
        "access_type": "offline",
        "prompt": "consent",
    }
    return RedirectResponse("https://accounts.google.com/o/oauth2/v2/auth?" + urlencode(params))

@router.get("/youtube/callback")
async def youtube_callback(code: str):
    data = {
        "code": code,
        "client_id": os.getenv("GOOGLE_CLIENT_ID"),
        "client_secret": os.getenv("GOOGLE_CLIENT_SECRET"),
        "redirect_uri": os.getenv("GOOGLE_REDIRECT_URI"),
        "grant_type": "authorization_code",
    }
    r = requests.post("https://oauth2.googleapis.com/token", data=data, timeout=30)
    return {"platform":"youtube","connected":"access_token" in r.json(),"token_response":r.json()}

@router.get("/tiktok")
async def tiktok_login():
    state = secrets.token_urlsafe(24)
    params = {
        "client_key": os.getenv("TIKTOK_CLIENT_KEY"),
        "response_type": "code",
        "scope": "user.info.basic,video.list,video.publish",
        "redirect_uri": os.getenv("TIKTOK_REDIRECT_URI"),
        "state": state,
    }
    return RedirectResponse("https://www.tiktok.com/v2/auth/authorize/?" + urlencode(params))

@router.get("/tiktok/callback")
async def tiktok_callback(code: str, state: str = ""):
    data = {
        "client_key": os.getenv("TIKTOK_CLIENT_KEY"),
        "client_secret": os.getenv("TIKTOK_CLIENT_SECRET"),
        "code": code,
        "grant_type": "authorization_code",
        "redirect_uri": os.getenv("TIKTOK_REDIRECT_URI"),
    }
    r = requests.post("https://open.tiktokapis.com/v2/oauth/token/", data=data, timeout=30)
    return {"platform":"tiktok","connected":"access_token" in r.json(),"token_response":r.json()}

@router.get("/instagram")
async def instagram_login():
    params = {
        "client_id": os.getenv("META_APP_ID"),
        "redirect_uri": os.getenv("META_REDIRECT_URI"),
        "response_type": "code",
        "scope": "instagram_basic,instagram_content_publish,instagram_manage_insights",
    }
    return RedirectResponse("https://www.facebook.com/v23.0/dialog/oauth?" + urlencode(params))

@router.get("/instagram/callback")
async def instagram_callback(code: str):
    params = {
        "client_id": os.getenv("META_APP_ID"),
        "client_secret": os.getenv("META_APP_SECRET"),
        "redirect_uri": os.getenv("META_REDIRECT_URI"),
        "code": code,
    }
    r = requests.get("https://graph.facebook.com/v23.0/oauth/access_token", params=params, timeout=30)
    return {"platform":"instagram","token_response":r.json()}
