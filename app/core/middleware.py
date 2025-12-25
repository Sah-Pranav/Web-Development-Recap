# app/core/middleware.py
from fastapi import Request
from fastapi.responses import JSONResponse
from app.core.logging import logger

async def error_handling_middleware(request: Request, call_next):
    try:
        response = await call_next(request)
        return response
    except Exception as e:
        logger.error(f"Unhandled error: {e}", exc_info=True)
        return JSONResponse(
            status_code=500,
            content={"status": "error", "message": "Internal Server Error"}
        )
