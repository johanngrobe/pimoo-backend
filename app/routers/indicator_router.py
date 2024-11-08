from typing import List

from fastapi import APIRouter, Depends, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.crud.indicator_crud import crud_indicator as crud
from app.dependencies import current_active_user, get_async_session
from app.models import Indicator, User, Tag
from app.schemas import IndicatorCreate, IndicatorUpdate, IndicatorDetailRead
from app.utils.auth_util import check_user_authorization

router = APIRouter()


@router.get("", response_model=List[IndicatorDetailRead])
async def get_indicators(
    db: AsyncSession = Depends(get_async_session),
    user: User = Depends(current_active_user),
):
    return await crud.get_all(db, user.municipality_id, Indicator.label)


@router.get("/{id}", response_model=IndicatorDetailRead)
async def get_indicator(
    id: int,
    db: AsyncSession = Depends(get_async_session),
    user: User = Depends(current_active_user),
):

    instance = await crud.get(db, id)
    check_user_authorization(user, instance.municipality_id)
    return instance


@router.post(
    "", status_code=status.HTTP_201_CREATED, response_model=IndicatorDetailRead
)
async def create_indicator(
    indicator: IndicatorCreate,
    db: AsyncSession = Depends(get_async_session),
    user: User = Depends(current_active_user),
):
    return await crud.create_with_associations(
        db=db,
        obj_in=indicator,
        user=user,
        association_fields={"tag_ids": (Tag, "tags")},
    )


@router.patch("/{id}", response_model=IndicatorDetailRead)
async def update_indicator(
    id: int,
    updates: IndicatorUpdate,
    db: AsyncSession = Depends(get_async_session),
    user: User = Depends(current_active_user),
):
    instance = await crud.get(db, id)
    check_user_authorization(user, instance.municipality_id)
    return await crud.update_with_associations(
        db=db,
        id=id,
        obj_in=updates,
        user=user,
        association_fields={"tag_ids": (Tag, "tags")},
    )


@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_indicator(
    id: int,
    db: AsyncSession = Depends(get_async_session),
    user: User = Depends(current_active_user),
):

    instance = await crud.get(db, id)
    check_user_authorization(user, instance.municipality_id)
    await crud.delete(db, id)
