from typing import List

from fastapi import APIRouter, Depends, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.crud.indicator import crud_indicator as crud
from app.core.deps import current_active_user, get_async_session
from app.models.indicator import Indicator
from app.models.user import User
from app.models.tag import Tag
from app.schemas.indicator import IndicatorCreate, IndicatorUpdate, IndicatorDetailRead
from app.utils.auth_util import check_user_authorization

router = APIRouter()


@router.get("", response_model=List[IndicatorDetailRead])
async def get_indicators(
    db: AsyncSession = Depends(get_async_session),
    user: User = Depends(current_active_user),
):

    sort_params = [("label", "asc")]
    return await crud.get_all(
        db=db, municipality_id=user.municipality_id, sort_params=sort_params
    )


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
