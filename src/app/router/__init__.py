from fastapi import APIRouter

from app.router.auth.route import auth_router


api_v1_route = APIRouter(prefix="/api/v1")
api_v1_route.include_router(auth_router)
