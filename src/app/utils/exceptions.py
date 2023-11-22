import logging

from fastapi import Request, HTTPException
from fastapi.responses import JSONResponse
from starlette.middleware.base import BaseHTTPMiddleware


logger = logging.getLogger(__name__)


class CustomExceptionMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        try:
            response = await call_next(request)
        # HTTP exceptions
        except HTTPException as exc:
            logger.info(f"HTTPException occurred: {exc.detail}")
            return JSONResponse(
                {"error": exc.detail, "detail": exc.detail}, status_code=exc.status_code
            )
        # Generic exceptions
        except Exception as exc:
            logger.info(f"General Exception occurred: {str(exc)}")
            return JSONResponse(
                {"error": "서버 로직에 오류가 발생했습니다.", "detail": str(exc)}, status_code=500
            )
        return response
