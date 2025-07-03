from typing import List

from fastapi import APIRouter, Depends, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.crud.mobilitaetscheck_ziel_unter import crud_sub_objective as crud
from app.core.deps import current_active_user, get_async_session
from app.models.user import User
from app.schemas.mobilitaetscheck_ziel_unter import (
    MobilitaetscheckZielUnterCreate as CreateSchema,
    MobilitaetscheckZielUnterUpdate as UpdateSchema,
    MobilitaetscheckZielUnterBaseRead as ReadBaseSchema,
    MobilitaetscheckZielUnterRead as ReadSchema,
)
from app.utils.auth_util import check_user_authorization

router = APIRouter()


@router.get("", response_model=List[ReadSchema])
async def get_sub_objectives(
    db: AsyncSession = Depends(get_async_session),
    user: User = Depends(current_active_user),
):
    sort_params = [("ziel_ober.nr", "asc"), ("nr", "asc")]

    return await crud.get_by_key(
        db=db,
        key="gemeinde_id",
        value=user.gemeinde_id,
        sort_params=sort_params,
    )


@router.get("/nach-parametern", response_model=List[ReadSchema])
async def get_by_params(
    ziel_ober_id: int,
    db: AsyncSession = Depends(get_async_session),
    user: User = Depends(current_active_user),
):
    keys = {
        "gemeinde_id": user.gemeinde_id,
        "ziel_ober_id": ziel_ober_id,
    }
    sort_params = [("nr", "asc")]

    return await crud.get_by_multi_keys(
        db=db,
        keys=keys,
        sort_params=sort_params,
    )


@router.get("/{id}", response_model=ReadBaseSchema)
async def get_sub_objective(
    id: int,
    db: AsyncSession = Depends(get_async_session),
    user: User = Depends(current_active_user),
):
    instance = await crud.get(db, id)
    check_user_authorization(user, instance.gemeinde_id)
    return instance


@router.post("", status_code=status.HTTP_201_CREATED, response_model=ReadSchema)
async def create_sub_objective(
    obj_in: CreateSchema,
    db: AsyncSession = Depends(get_async_session),
    user: User = Depends(current_active_user),
):
    return await crud.create(db, obj_in, user)


@router.patch("/{id}", response_model=ReadSchema)
async def update_sub_objective(
    id: int,
    updates: UpdateSchema,
    db: AsyncSession = Depends(get_async_session),
    user: User = Depends(current_active_user),
):
    instance = await crud.get(db, id)
    check_user_authorization(user, instance.gemeinde_id)
    return await crud.update(db, id, updates, user)


@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_sub_objective(
    id: int,
    db: AsyncSession = Depends(get_async_session),
    user: User = Depends(current_active_user),
):
    instance = await crud.get(db, id)
    check_user_authorization(user, instance.gemeinde_id)
    await crud.delete(db, id)
