from fastapi import Depends, FastAPI
from fastapi.middleware.cors import CORSMiddleware

from . import models, schemas
from .database import engine
from .routers import (auth,
                      main_objective,
                      sub_objective,
                      mobility_submission, 
                      climate_submission,
                      mobility_result,
                      mobility_subresult,
                      tag, 
                      text_block, 
                      indicator,
                      option)

from .config import settings
from .utils.fastapi_users import auth_backend, current_active_user, fastapi_users

# Create the database tables, if they do not exist. Not needed if using Alembic
# models.Base.metadata.create_all(bind=engine)

app = FastAPI(root_path=settings.ROOT_PATH)

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.ALLOW_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(
    fastapi_users.get_auth_router(auth_backend), prefix="/auth", tags=["auth"]
)
app.include_router(
    fastapi_users.get_register_router(schemas.UserRead, schemas.UserCreate),
    prefix="/auth",
    tags=["auth"],
)
app.include_router(
    fastapi_users.get_reset_password_router(),
    prefix="/auth",
    tags=["auth"],
)
app.include_router(
    fastapi_users.get_verify_router(schemas.UserRead),
    prefix="/auth",
    tags=["auth"],
)
app.include_router(auth.router)
app.include_router(
    fastapi_users.get_users_router(schemas.UserRead, schemas.UserUpdate),
    prefix="/users",
    tags=["users"],
)
app.include_router(mobility_submission.router)
app.include_router(climate_submission.router)
app.include_router(tag.router)
app.include_router(text_block.router)
app.include_router(indicator.router)
app.include_router(main_objective.router)
app.include_router(sub_objective.router)
app.include_router(mobility_result.router)
app.include_router(mobility_subresult.router)
app.include_router(option.router)




