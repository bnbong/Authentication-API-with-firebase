from fastapi import APIRouter
from app.msng.app.api.api_v1.endpoints.auth.route import auth_router


api_v1_route = APIRouter(prefix="/api/v1")
api_v1_route.include_router(auth_router)