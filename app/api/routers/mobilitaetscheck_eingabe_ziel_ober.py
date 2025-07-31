from typing import List

from fastapi import APIRouter, Depends, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.crud.mobilitaetscheck_eingabe_ziel_ober import crud_mobility_result as crud
from app.core.deps import current_active_user, get_async_session
from app.schemas.mobilitaetscheck_eingabe_ziel_ober import (
    MobilitaetscheckEingabeZielOberCreate as CreateSchema,
    MobilitaetscheckEingabeZielOberUpdate as UpdateSchema,
    MobilitaetscheckEingabeZielOberRead as ReadSchema,
)

router = APIRouter()

# @router.get(
#     "",
#     response_model=List[MobilitaetscheckEingabeZielOberRead],
#     dependencies=[Depends(current_active_user)]
# )
# async def get_mobility_results(db: AsyncSession = Depends(get_async_session)):
#     return await crud.get_all(db)


@router.get(
    "/nach-eingabe",
    response_model=List[ReadSchema],
    dependencies=[Depends(current_active_user)],
)
async def get_mobility_result(
    eingabe_id: int, db: AsyncSession = Depends(get_async_session)
):
    return await crud.get_by_key(db=db, key="submission_id", value=eingabe_id)


@router.get(
    "/{id}",
    response_model=ReadSchema,
    dependencies=[Depends(current_active_user)],
)
async def get_mobility_result(id: int, db: AsyncSession = Depends(get_async_session)):
    return await crud.get(db, id)


@router.post(
    "",
    response_model=ReadSchema,
    status_code=status.HTTP_201_CREATED,
    dependencies=[Depends(current_active_user)],
)
async def create_mobility_result(
    obj_in: CreateSchema, db: AsyncSession = Depends(get_async_session)
):
    return await crud.create(db, obj_in)


@router.patch(
    "/{id}",
    response_model=ReadSchema,
    dependencies=[Depends(current_active_user)],
)
async def update_mobility_result(
    id: int,
    updates: UpdateSchema,
    db: AsyncSession = Depends(get_async_session),
):
    return await crud.update(db, id, updates)


@router.delete(
    "/{id}",
    status_code=status.HTTP_204_NO_CONTENT,
    dependencies=[Depends(current_active_user)],
)
async def delete_mobility_result(
    id: int, db: AsyncSession = Depends(get_async_session)
):
    return await crud.delete(db, id)
