from typing import List

from fastapi import APIRouter, Depends, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.crud.klimacheck_klimarelevanz import crud_klimacheck_klimarelevanz
from app.crud.klimacheck_auswirkung_dauer import crud_klimacheck_auswirkung_dauer
from app.crud.mobilitaetscheck_auswirkung_raeumlich import (
    crud_mobilitaetscheck_auswirkung_raeumlich,
)
from app.crud.gemeinde import crud_gemeinde
from app.crud.user_rolle import crud_user_rolle
from app.core.deps import current_active_user, get_async_session
from app.schemas.klimacheck_klimarelevanz import KlimacheckKlimarelevanzRead
from app.schemas.klimacheck_auswirkung_dauer import KlimacheckAuswirkungDauerRead
from app.schemas.mobilitaetscheck_auswirkung_raeumlich import (
    MobilitaetscheckAuswirkungRaeumlichRead,
)
from app.schemas.gemeinde import GemeindeRead
from app.schemas.user_rolle import UserRolleRead
from app.utils.label_util import (
    KLIMACHECK_AUSWIRKUNG_LABELS,
    MOBILITAETSCHECK_AUSWIRKUNG_TICKMARK_LABELS,
)

router = APIRouter()


@router.get(
    "/gemeinde",
    response_model=List[GemeindeRead],
    status_code=status.HTTP_200_OK,
)
async def get_municipality_options(db: AsyncSession = Depends(get_async_session)):
    return await crud_gemeinde.get_all(db=db, sort_params=[("name", "asc")])


@router.get(
    "/user-rolle", response_model=List[UserRolleRead], status_code=status.HTTP_200_OK
)
async def get_user_role_options(db: AsyncSession = Depends(get_async_session)):
    return await crud_user_rolle.get_all(db=db, sort_params=[("name", "asc")])


@router.get(
    "/klimacheck/klimarelevanz",
    response_model=List[KlimacheckKlimarelevanzRead],
    dependencies=[Depends(current_active_user)],
    status_code=status.HTTP_200_OK,
)
async def get_climate_impact_options(db: AsyncSession = Depends(get_async_session)):
    return await crud_klimacheck_klimarelevanz.get_all(
        db=db, sort_params=[("name", "asc")]
    )


@router.get(
    "/klimacheck/auswirkung",
    dependencies=[Depends(current_active_user)],
    status_code=status.HTTP_200_OK,
)
async def get_climate_impact_ghg_options():
    result = [
        {"label": label, "value": value}
        for value, label in KLIMACHECK_AUSWIRKUNG_LABELS.items()
    ]
    return result


@router.get(
    "/klimacheck/auswirkung-dauer",
    response_model=List[KlimacheckAuswirkungDauerRead],
    dependencies=[Depends(current_active_user)],
    status_code=status.HTTP_200_OK,
)
async def get_climate_impact_duration_options(
    db: AsyncSession = Depends(get_async_session),
):
    return await crud_klimacheck_auswirkung_dauer.get_all(
        db=db, sort_params=[("name", "asc")]
    )


@router.get(
    "/mobilitaetscheck/auswirkung-raeumlich",
    response_model=List[MobilitaetscheckAuswirkungRaeumlichRead],
    dependencies=[Depends(current_active_user)],
    status_code=status.HTTP_200_OK,
)
async def get_mobility_spatial_impact_options(
    db: AsyncSession = Depends(get_async_session),
):
    return await crud_mobilitaetscheck_auswirkung_raeumlich.get_all(
        db=db, sort_params=[("name", "asc")]
    )


@router.get(
    "/mobilitaetscheck/auswirkung-tickmarks",
    dependencies=[Depends(current_active_user)],
    status_code=status.HTTP_200_OK,
)
async def get_mobility_impact_tickmarks_options():

    result = [
        {"label": label, "value": value}
        for value, label in MOBILITAETSCHECK_AUSWIRKUNG_TICKMARK_LABELS.items()
    ]
    return result
