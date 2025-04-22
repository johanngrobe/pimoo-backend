from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.core.config import settings
from app.crud.exceptions import AuthorizationError, DatabaseCommitError, NotFoundError
from app.exceptions import (
    authorization_exception_handler,
    database_commit_exception_handler,
    not_found_exception_handler,
)
from app.api.main import router


description = """
This is a fancy API built with [FastAPI🚀](https://fastapi.tiangolo.com/)

📝 [Source Code](https://github.com/johanngrobe/stellplatztool-backend)  
🐞 [Issues](https://github.com/johanngrobe/stellplatztool-backend/issues) 
"""


app = FastAPI(
    title=settings.PROJECT_NAME,
    description=description,
    version="1.0.0",
    openapi_url=f"{settings.API_V1_STR}/openapi.json",
)

app.add_exception_handler(AuthorizationError, authorization_exception_handler)
app.add_exception_handler(DatabaseCommitError, database_commit_exception_handler)
app.add_exception_handler(NotFoundError, not_found_exception_handler)

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.all_cors_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(router)
