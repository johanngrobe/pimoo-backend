from typing import List

from fastapi import APIRouter, Depends, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.crud.gemeinde_gebiet import crud_gemeinde_gebiet as crud
from app.core.deps import current_active_user, get_async_session
from app.models.gemeinde_gebiet import GemeindeGebiet
from app.models.user import User
from app.schemas.gemeinde_gebiet import (
    GemeindeGebietCreate,
    GemeindeGebietUpdate,
    GemeindeGebietRead,
)
from app.utils.auth_util import check_user_authorization

router = APIRouter()


@router.get("", response_model=List[GemeindeGebietRead])
async def get_gemeinede_gebiete(
    db: AsyncSession = Depends(get_async_session),
    user: User = Depends(current_active_user),
):

    sort_params = [("name", "asc")]
    return await crud.get_all(
        db=db, gemeinde_id=user.gemeinde_id, sort_params=sort_params
    )


@router.get("/{id}", response_model=GemeindeGebietRead)
async def get_gemeinde_gebiet(
    id: int,
    db: AsyncSession = Depends(get_async_session),
    user: User = Depends(current_active_user),
):

    instance = await crud.get(db, id)
    check_user_authorization(user, instance.gemeinde_id)
    return instance


@router.post("", status_code=status.HTTP_201_CREATED, response_model=GemeindeGebietRead)
async def create_gemeinde_gebiet(
    obj_in: GemeindeGebietCreate,
    db: AsyncSession = Depends(get_async_session),
    user: User = Depends(current_active_user),
):
    return await crud.create(db=db, obj_in=obj_in, user=user)


@router.patch("/{id}", response_model=GemeindeGebietRead)
async def update_gemeinde_gebiet(
    id: int,
    updates: GemeindeGebietUpdate,
    db: AsyncSession = Depends(get_async_session),
    user: User = Depends(current_active_user),
):
    instance = await crud.get(db, id)
    check_user_authorization(user, instance.gemeinde_id)
    return await crud.update(
        db=db,
        id=id,
        obj_in=updates,
    )


@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_gemeinde_gebiet(
    id: int,
    db: AsyncSession = Depends(get_async_session),
    user: User = Depends(current_active_user),
):

    instance = await crud.get(db, id)
    check_user_authorization(user, instance.gemeinde_id)
    await crud.delete(db, id)
