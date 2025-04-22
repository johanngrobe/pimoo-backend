from typing import List

from fastapi import APIRouter, Depends, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.crud.mobility_result import crud_mobility_result as crud
from app.core.deps import current_active_user, get_async_session
from app.schemas.mobility_result import (
    MobilityResultCreate as CreateSchema,
    MobilityResultUpdate as UpdateSchema,
    MobilityResultRead as ReadSchema,
)

router = APIRouter()

# @router.get(
#     "",
#     response_model=List[MobilityResultRead],
#     dependencies=[Depends(current_active_user)]
# )
# async def get_mobility_results(db: AsyncSession = Depends(get_async_session)):
#     return await crud.get_all(db)


@router.get(
    "/by-submission",
    response_model=List[ReadSchema],
    dependencies=[Depends(current_active_user)],
)
async def get_mobility_result(
    submission_id: int, db: AsyncSession = Depends(get_async_session)
):
    return await crud.get_by_key(db=db, key="submission_id", value=submission_id)


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
    mobility_result: CreateSchema, db: AsyncSession = Depends(get_async_session)
):
    return await crud.create(db, mobility_result)


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
