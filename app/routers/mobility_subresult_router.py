from fastapi import APIRouter, Depends, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.crud.mobility_subresult_crud import crud_mobility_subresult as crud
from app.dependencies import current_active_user, get_async_session
from app.models import Indicator
from app.schemas import (
    MobilitySubResultCreate,
    MobilitySubResultUpdate,
    MobilitySubResultRead,
)

router = APIRouter()


@router.get(
    "/{id}",
    response_model=MobilitySubResultRead,
    dependencies=[Depends(current_active_user)],
)
async def get_mobility_subresult(
    id: int, db: AsyncSession = Depends(get_async_session)
):
    return await crud.get(db, id)


@router.post(
    "",
    status_code=status.HTTP_201_CREATED,
    response_model=MobilitySubResultRead,
    dependencies=[Depends(current_active_user)],
)
async def create_mobility_subresult(
    mobility_result: MobilitySubResultCreate,
    db: AsyncSession = Depends(get_async_session),
):
    return await crud.create_with_associations(
        db=db,
        obj_in=mobility_result,
        association_fields={"indicator_ids": (Indicator, "indicators")},
    )


@router.patch(
    "/{id}",
    response_model=MobilitySubResultRead,
    dependencies=[Depends(current_active_user)],
)
async def update_mobility_subresult(
    id: int,
    updates: MobilitySubResultUpdate,
    db: AsyncSession = Depends(get_async_session),
):
    return await crud.update_with_associations(
        db=db,
        id=id,
        obj_in=updates,
        association_fields={"indicator_ids": (Indicator, "indicators")},
    )


@router.delete(
    "/{id}",
    status_code=status.HTTP_204_NO_CONTENT,
    dependencies=[Depends(current_active_user)],
)
async def delete_mobility_subresult(
    id: int, db: AsyncSession = Depends(get_async_session)
):
    return await crud.delete(db, id)
