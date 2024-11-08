from typing import List

from fastapi import APIRouter, Depends, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.crud.main_objective_crud import crud_main_objective as crud
from app.dependencies import current_active_user, get_async_session
from app.models import MainObjective, User
from app.schemas import MainObjectiveCreate, MainObjectiveUpdate, MainObjectiveFullRead
from app.utils.auth_util import check_user_authorization

router = APIRouter()


@router.get("", response_model=List[MainObjectiveFullRead])
async def get_main_objectives(
    db: AsyncSession = Depends(get_async_session),
    user: User = Depends(current_active_user),
):
    return await crud.get_all(db, user)


@router.get("/{id}", response_model=MainObjectiveFullRead)
async def get_main_objective(
    id: int,
    db: AsyncSession = Depends(get_async_session),
    user: User = Depends(current_active_user),
):
    instance = await crud.get(db, id)
    check_user_authorization(user, instance.municipality_id)
    return crud.sort(instance)


@router.post("", status_code=status.HTTP_201_CREATED)
async def create_main_objective(
    main_objective: MainObjectiveCreate,
    db: AsyncSession = Depends(get_async_session),
    user: User = Depends(current_active_user),
):
    return await crud.create(db, main_objective, user)


@router.patch("/{id}", response_model=MainObjectiveFullRead)
async def update_main_objective(
    id: int,
    updates: MainObjectiveUpdate,
    db: AsyncSession = Depends(get_async_session),
    user: User = Depends(current_active_user),
):
    instance = await crud.get(db, id)
    check_user_authorization(user, instance.municipality_id)
    return await crud.update(db, id, updates, user)


@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_main_objective(
    id: int,
    db: AsyncSession = Depends(get_async_session),
    user: User = Depends(current_active_user),
):
    instance = await crud.get(db, id)
    check_user_authorization(user, instance.municipality_id)
    await crud.delete(db, id)
