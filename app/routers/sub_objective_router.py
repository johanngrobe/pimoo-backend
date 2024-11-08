from typing import List

from fastapi import APIRouter, Depends, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.crud.sub_objective_crud import crud_sub_objective as crud
from app.dependencies import current_active_user, get_async_session
from app.models import User
from app.schemas import (
    SubObjectiveCreate,
    SubObjectiveUpdate,
    SubObjectiveBasicRead,
    SubObjectiveFullRead,
)
from app.utils.auth_util import check_user_authorization

router = APIRouter()


@router.get("", response_model=List[SubObjectiveFullRead])
async def get_sub_objectives(
    db: AsyncSession = Depends(get_async_session),
    user: User = Depends(current_active_user),
):
    return await crud.get_all(db, user)


@router.get("/{id}", response_model=SubObjectiveBasicRead)
async def get_sub_objective(
    id: int,
    db: AsyncSession = Depends(get_async_session),
    user: User = Depends(current_active_user),
):
    instance = await crud.get(db, id)
    check_user_authorization(user, instance.municipality_id)
    return instance


@router.post(
    "", status_code=status.HTTP_201_CREATED, response_model=SubObjectiveFullRead
)
async def create_sub_objective(
    sub_objective: SubObjectiveCreate,
    db: AsyncSession = Depends(get_async_session),
    user: User = Depends(current_active_user),
):
    return await crud.create(db, sub_objective, user)


@router.patch("/{id}", response_model=SubObjectiveFullRead)
async def update_sub_objective(
    id: int,
    updates: SubObjectiveUpdate,
    db: AsyncSession = Depends(get_async_session),
    user: User = Depends(current_active_user),
):
    instance = await crud.get(db, id)
    check_user_authorization(user, instance.municipality_id)
    return await crud.update(db, id, updates, user)


@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_sub_objective(
    id: int,
    db: AsyncSession = Depends(get_async_session),
    user: User = Depends(current_active_user),
):
    instance = await crud.get(db, id)
    check_user_authorization(user, instance.municipality_id)
    await crud.delete(db, id)
