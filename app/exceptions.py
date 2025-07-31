from fastapi import Request
from fastapi.responses import JSONResponse

from app.crud.exceptions import AuthorizationError, DatabaseCommitError, NotFoundError


async def authorization_exception_handler(request: Request, exc: AuthorizationError):
    return JSONResponse(status_code=403, content={"message": exc.message})


async def database_commit_exception_handler(request: Request, exc: DatabaseCommitError):
    return JSONResponse(status_code=500, content={"message": exc.message})


async def not_found_exception_handler(request: Request, exc: NotFoundError):
    return JSONResponse(status_code=204, content={"message": exc.message})
