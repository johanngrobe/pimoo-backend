from fastapi import APIRouter

from app.dependencies import auth_backend, fastapi_users
from app.routers import (
    climate_submission_router,
    indicator_router,
    main_objective_router,
    mobility_result_router,
    mobility_submission_router,
    mobility_subresult_router,
    option_router,
    sub_objective_router,
    tag_router,
    text_block_router,
)
from app.schemas.user_schema import UserRead, UserCreate, UserUpdate

router = APIRouter()

router.include_router(
    fastapi_users.get_auth_router(auth_backend), prefix="/auth", tags=["auth"]
)
router.include_router(
    fastapi_users.get_register_router(UserRead, UserCreate),
    prefix="/auth",
    tags=["auth"],
)
router.include_router(
    fastapi_users.get_reset_password_router(), prefix="/auth", tags=["auth"]
)
router.include_router(
    fastapi_users.get_verify_router(UserRead), prefix="/auth", tags=["auth"]
)
router.include_router(
    fastapi_users.get_users_router(UserRead, UserUpdate),
    prefix="/users",
    tags=["users"],
)
router.include_router(
    mobility_submission_router.router,
    prefix="/submission/mobility",
    tags=["submission"],
)
router.include_router(
    climate_submission_router.router, prefix="/submission/climate", tags=["submission"]
)
router.include_router(tag_router.router, prefix="/tag", tags=["tag"])
router.include_router(
    text_block_router.router, prefix="/text_block", tags=["text_block"]
)
router.include_router(indicator_router.router, prefix="/indicator", tags=["indicator"])
router.include_router(
    main_objective_router.router, prefix="/objective/main", tags=["objective"]
)
router.include_router(
    sub_objective_router.router, prefix="/objective/sub", tags=["objective"]
)
router.include_router(
    mobility_result_router.router, prefix="/mobility-result", tags=["Mobility Result"]
)
router.include_router(
    mobility_subresult_router.router,
    prefix="/mobility-result/sub",
    tags=["Mobility Result"],
)
router.include_router(option_router.router, prefix="/option", tags=["option"])
