from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from pydantic import ValidationError


class APIError(Exception):
    def __init__(self, status_code: int, detail: str):
        self.status_code = status_code
        self.detail = detail


def register_exception_handlers(app: FastAPI):
    @app.exception_handler(APIError)
    async def handle_api_error(_: Request, exc: APIError):
        return JSONResponse(status_code=exc.status_code, content={"detail": exc.detail})

    @app.exception_handler(ValidationError)
    async def handle_validation(_: Request, exc: ValidationError):
        return JSONResponse(status_code=422, content={"detail": exc.errors()})

    @app.exception_handler(Exception)
    async def handle_generic(_: Request, exc: Exception):
        return JSONResponse(status_code=500, content={"detail": "Unexpected server error", "error": str(exc)})
