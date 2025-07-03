from typing import List

from fastapi import APIRouter, Depends, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.crud.mobilitaetscheck_ziel_ober import crud_main_objective as crud
from app.core.deps import current_active_user, get_async_session
from app.models.user import User
from app.schemas.mobilitaetscheck_ziel_ober import (
    MobilitaetscheckZielOberCreate as CreateSchema,
    MobilitaetscheckZielOberUpdate as UpdateSchema,
    MobilitaetscheckZielOberRead as ReadSchema,
)
from app.utils.auth_util import check_user_authorization

router = APIRouter()


@router.get("", response_model=List[ReadSchema])
async def get_main_objectives(
    db: AsyncSession = Depends(get_async_session),
    user: User = Depends(current_active_user),
):
    sort_params = [("nr", "asc")]

    # Fetch all records using get_all
    return await crud.get_by_key(
        db,
        key="gemeinde_id",
        value=user.gemeinde_id,
        sort_params=sort_params,
    )


@router.get("/{id}", response_model=ReadSchema)
async def get_main_objective(
    id: int,
    db: AsyncSession = Depends(get_async_session),
    user: User = Depends(current_active_user),
):
    instance = await crud.get(db, id)
    check_user_authorization(user, instance.gemeinde_id)
    return crud.sort(instance)


@router.post("", status_code=status.HTTP_201_CREATED)
async def create_main_objective(
    main_objective: CreateSchema,
    db: AsyncSession = Depends(get_async_session),
    user: User = Depends(current_active_user),
):
    return await crud.create(db, main_objective, user)


@router.patch("/{id}", response_model=ReadSchema)
async def update_main_objective(
    id: int,
    updates: UpdateSchema,
    db: AsyncSession = Depends(get_async_session),
    user: User = Depends(current_active_user),
):
    instance = await crud.get(db, id)
    check_user_authorization(user, instance.gemeinde_id)
    return await crud.update(db, id, updates, user)


@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_main_objective(
    id: int,
    db: AsyncSession = Depends(get_async_session),
    user: User = Depends(current_active_user),
):
    instance = await crud.get(db, id)
    check_user_authorization(user, instance.gemeinde_id)
    await crud.delete(db, id)
