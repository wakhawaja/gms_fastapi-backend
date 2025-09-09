# app/middleware/errors.py

from fastapi import Request
from fastapi.responses import JSONResponse
from starlette.middleware.base import BaseHTTPMiddleware

class ExceptionHandlerMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        try:
            return await call_next(request)
        except Exception as e:
            # Log exception here if needed
            return JSONResponse(
                status_code=500,
                content={"detail": "Internal Server Error", "error": str(e)},
            )
