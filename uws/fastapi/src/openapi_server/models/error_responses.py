"""General exception handler for FastAPI application."""

from fastapi import HTTPException, Request
from fastapi.responses import JSONResponse

async def http_exception_handler(request: Request, exc: HTTPException) -> JSONResponse:
    """Handle HTTPException and return JSON response."""
    return JSONResponse(
        status_code=500,
        content={"message": exc.with_traceback(None)._errors},
    )