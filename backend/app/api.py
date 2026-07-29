from fastapi import APIRouter

from app.modules.users.routers.auth_router import router as auth_router

api_router = APIRouter()

api_router.include_router(auth_router)