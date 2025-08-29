from fastapi import Request
from fastapi.exceptions import HTTPException
from fastapi.responses import JSONResponse
from sqlalchemy.exc import SQLAlchemyError


async def http_error_handler(request: Request, exc: HTTPException) -> JSONResponse:
    """Return JSON for HTTP exceptions."""
    return JSONResponse(
        status_code=exc.status_code,
        content={"code": exc.status_code, "message": exc.detail},
    )


async def db_error_handler(request: Request, exc: SQLAlchemyError) -> JSONResponse:
    """Return JSON for database errors."""
    return JSONResponse(
        status_code=500,
        content={"code": 500, "message": "Database error"},
    )
