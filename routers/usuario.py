from fastapi import APIRouter

router = APIRouter(prefix="/usuario", tags=["usuario"])

@router.get("/ping")
async def ping_usuario():
    return {"modulo": "usuario", "status": "ok"}
