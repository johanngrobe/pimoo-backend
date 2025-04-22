from fastapi import APIRouter

from app.core.deps import auth_backend, fastapi_users
from app.api.routers import (
    climate_submission,
    indicator,
    main_objective,
    mobility_result,
    mobility_submission,
    mobility_subresult,
    option,
    sub_objective,
    tag,
    text_block,
)
from app.schemas.user import UserRead, UserCreate, UserUpdate

router = APIRouter()

router.include_router(
    fastapi_users.get_auth_router(auth_backend), prefix="/auth", tags=["Auth"]
)
router.include_router(
    fastapi_users.get_register_router(UserRead, UserCreate),
    prefix="/auth",
    tags=["Auth"],
)
router.include_router(
    fastapi_users.get_reset_password_router(), prefix="/auth", tags=["Auth"]
)
router.include_router(
    fastapi_users.get_verify_router(UserRead), prefix="/auth", tags=["Auth"]
)
router.include_router(
    fastapi_users.get_users_router(UserRead, UserUpdate),
    prefix="/users",
    tags=["Users"],
)
router.include_router(
    mobility_submission.router,
    prefix="/submission/mobility",
    tags=["Mobility Submission"],
)
router.include_router(
    climate_submission.router,
    prefix="/submission/climate",
    tags=["Climate Submission"],
)
router.include_router(
    mobility_result.router, prefix="/mobility-result", tags=["Mobility Result"]
)
router.include_router(
    mobility_subresult.router,
    prefix="/mobility-result/sub",
    tags=["Mobility Subresult"],
)
router.include_router(indicator.router, prefix="/indicator", tags=["Indicator"])
router.include_router(text_block.router, prefix="/text-block", tags=["Text Block"])
router.include_router(tag.router, prefix="/tag", tags=["Tag"])
router.include_router(
    main_objective.router, prefix="/objective/main", tags=["Main Objective"]
)
router.include_router(
    sub_objective.router, prefix="/objective/sub", tags=["Sub Objective"]
)
router.include_router(option.router, prefix="/option", tags=["Option"])
