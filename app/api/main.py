from fastapi import APIRouter

from app.core.deps import auth_backend, fastapi_users
from app.api.routers import (
    indikator,
    klimacheck,
    mobilitaetscheck_eingabe,
    mobilitaetscheck_eingabe_ziel_ober,
    mobilitaetscheck_eingabe_ziel_unter,
    mobilitaetscheck_ziel_ober,
    mobilitaetscheck_ziel_unter,
    option,
    tag,
    textblock,
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
    mobilitaetscheck_eingabe.router,
    prefix="/mobilitaetscheck/eingabe",
    tags=["Mobilitätscheck", "Eingabe"],
)
router.include_router(
    klimacheck.router,
    prefix="/klimacheck/eingabe",
    tags=["Klimacheck", "Eingabe"],
)
router.include_router(
    mobilitaetscheck_eingabe_ziel_ober.router,
    prefix="/mobilitaetscheck/eingabe/ziel/ober",
    tags=["Mobilitätscheck", "Eingabe"],
)
router.include_router(
    mobilitaetscheck_eingabe_ziel_unter.router,
    prefix="/mobilitaetscheck/eingabe/ziel/unter",
    tags=["Mobilitätscheck", "Eingabe"],
)
router.include_router(
    indikator.router,
    prefix="/einstellungen/indikator",
    tags=["Einstellungen", "Indikator"],
)
router.include_router(
    textblock.router,
    prefix="/einstellungen/textblock",
    tags=["Einstellungen", "Textblock"],
)
router.include_router(
    tag.router, prefix="/einstellungen/tag", tags=["Einestellungen", "Tag"]
)
router.include_router(
    mobilitaetscheck_ziel_ober.router,
    prefix="/einstellungen/mobilitaetscheck/ziel/ober",
    tags=["Einstellungen", "Mobilitätscheck"],
)
router.include_router(
    mobilitaetscheck_ziel_unter.router,
    prefix="/einstellungen/mobilitaetscheck/ziel/unter",
    tags=["Einstellungen", "Mobilitätscheck"],
)
router.include_router(option.router, prefix="/option", tags=["Option"])
