from fastapi import APIRouter
router = APIRouter(prefix="/api/youtube", tags=["YouTube"])

@router.get("/status")
async def status():
    return {"connector":"youtube","oauth_callback":"/auth/youtube/callback","status":"ready"}
