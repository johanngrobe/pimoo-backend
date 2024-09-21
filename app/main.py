from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from . import models
from .database import engine
from .routers import tag, text_block, indicator, objective, mobility_result, submission, option
from .config import settings

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

app.include_router(submission.router)
app.include_router(tag.router)
app.include_router(text_block.router)
app.include_router(indicator.router)
app.include_router(objective.router)
app.include_router(mobility_result.router)
app.include_router(option.router)


