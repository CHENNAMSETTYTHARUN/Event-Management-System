from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from fastapi.exceptions import RequestValidationError
from pymysql import IntegrityError
from sqlalchemy.exc import DBAPIError

class AppException(Exception):
    def __init__(self, message: str, status_code: int = 500, details: dict = None):
        self.message = message
        self.status_code = status_code
        self.details = details or {}
        super().__init__(message)

class NotFoundException(AppException):
    def __init__(self, message: str = "Resource not found", details: dict = None):
        super().__init__(message, status_code=404, details=details)

class UnauthorizedException(AppException):
    def __init__(self, message: str = "Could not validate credentials", details: dict = None):
        super().__init__(message, status_code=401, details=details)

class ForbiddenException(AppException):
    def __init__(self, message: str = "You do not have permission to access this resource", details: dict = None):
        super().__init__(message, status_code=403, details=details)

class BadRequestException(AppException):
    def __init__(self, message: str = "Bad request", details: dict = None):
        super().__init__(message, status_code=400, details=details)

class ConflictException(AppException):
    def __init__(self, message: str = "Conflict occurred", details: dict = None):
        super().__init__(message, status_code=409, details=details)

def register_exception_handlers(app: FastAPI):
    @app.exception_handler(AppException)
    async def app_exception_handler(request: Request, exc: AppException):
        return JSONResponse(
            status_code=exc.status_code,
            content={
                "success": False,
                "error": {
                    "code": exc.__class__.__name__,
                    "message": exc.message,
                    "details": exc.details
                }
            }
        )

    @app.exception_handler(RequestValidationError)
    async def validation_exception_handler(request: Request, exc: RequestValidationError):
        details = {}
        for err in exc.errors():
            loc = " -> ".join(str(x) for x in err.get("loc", []))
            details[loc] = err.get("msg", "Validation error")
        return JSONResponse(
            status_code=400,
            content={
                "success": False,
                "error": {
                    "code": "ValidationError",
                    "message": "Input validation failed",
                    "details": details
                }
            }
        )

    @app.exception_handler(IntegrityError)
    async def integrity_exception_handler(request: Request, exc: IntegrityError):
        return JSONResponse(
            status_code=409,
            content={
                "success": False,
                "error": {
                    "code": "DatabaseIntegrityError",
                    "message": "Database integrity constraint violation.",
                    "details": {"error": str(exc)}
                }
            }
        )

    @app.exception_handler(DBAPIError)
    async def db_api_exception_handler(request: Request, exc: DBAPIError):
        return JSONResponse(
            status_code=500,
            content={
                "success": False,
                "error": {
                    "code": "DatabaseError",
                    "message": "A database error occurred.",
                    "details": {"error": str(exc.orig) if exc.orig else str(exc)}
                }
            }
        )

    @app.exception_handler(Exception)
    async def general_exception_handler(request: Request, exc: Exception):
        return JSONResponse(
            status_code=500,
            content={
                "success": False,
                "error": {
                    "code": "InternalServerError",
                    "message": "An unexpected error occurred.",
                    "details": {"error": str(exc)}
                }
            }
        )
