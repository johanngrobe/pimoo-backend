from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.config import settings
from app.crud.exceptions import AuthorizationError, DatabaseCommitError, NotFoundError
from app.exceptions import (
    authorization_exception_handler,
    database_commit_exception_handler,
    not_found_exception_handler,
)
from app.routers.api import router


app = FastAPI(title=settings.PROJECT_NAME, root_path=settings.ROOT_PATH)

app.add_exception_handler(AuthorizationError, authorization_exception_handler)
app.add_exception_handler(DatabaseCommitError, database_commit_exception_handler)
app.add_exception_handler(NotFoundError, not_found_exception_handler)

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.ALLOW_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(router)
