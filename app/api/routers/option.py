from typing import List

from fastapi import APIRouter, Depends, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.crud.gemeinde import crud_gemeinde as crud
from app.core.deps import current_active_user, get_async_session
from app.schemas.gemeinde import GemeindeRead
from app.utils.label_util import (
    CLIMATE_IMPACT_LABELS,
    CLIMATE_IMPACT_GHG_LABELS,
    CLIMATE_IMPACT_DURATION_LABELS,
    MOBILITY_SPATIAL_IMPACT_LABELS,
    MOBILITY_IMPACT_TICKMARK_LABELS,
)
from app.utils.options_util import USER_ROLES

router = APIRouter()


@router.get(
    "/gemeinde",
    response_model=List[GemeindeRead],
    status_code=status.HTTP_200_OK,
)
async def get_municipality_options(db: AsyncSession = Depends(get_async_session)):
    return await crud.get_all(db=db, sort_params=[("name", "desc")])


@router.get("/user-rolle", status_code=status.HTTP_200_OK)
async def get_user_role_options():
    return [{"label": label, "value": value} for value, label in USER_ROLES.items()]


@router.get(
    "/klimacheck/auswirkung",
    dependencies=[Depends(current_active_user)],
    status_code=status.HTTP_200_OK,
)
async def get_climate_impact_options():
    result = [
        {"label": label, "value": value}
        for value, label in CLIMATE_IMPACT_LABELS.items()
    ]
    return result


@router.get(
    "/klimacheck/auswirkung-ghg",
    dependencies=[Depends(current_active_user)],
    status_code=status.HTTP_200_OK,
)
async def get_climate_impact_ghg_options():
    result = [
        {"label": label, "value": value}
        for value, label in CLIMATE_IMPACT_GHG_LABELS.items()
    ]
    return result


@router.get(
    "/klimacheck/auswirkung-dauer",
    dependencies=[Depends(current_active_user)],
    status_code=status.HTTP_200_OK,
)
async def get_climate_impact_duration_options():

    result = [
        {"label": label, "value": value}
        for value, label in CLIMATE_IMPACT_DURATION_LABELS.items()
    ]
    return result


@router.get(
    "/mobilitaetscheck/auswirkung-raeumlich",
    dependencies=[Depends(current_active_user)],
    status_code=status.HTTP_200_OK,
)
async def get_mobility_spatial_impact_options():

    result = [
        {"label": label, "value": value}
        for value, label in MOBILITY_SPATIAL_IMPACT_LABELS.items()
    ]
    return result


@router.get(
    "/mobilitaetscheck/auswirkung-tickmarks",
    dependencies=[Depends(current_active_user)],
    status_code=status.HTTP_200_OK,
)
async def get_mobility_impact_tickmarks_options():

    result = [
        {"label": label, "value": value}
        for value, label in MOBILITY_IMPACT_TICKMARK_LABELS.items()
    ]
    return result
