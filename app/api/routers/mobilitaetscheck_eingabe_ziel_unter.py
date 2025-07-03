from fastapi import APIRouter, Depends, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.crud.mobilitaetscheck_eingabe_ziel_unter import crud_mobility_subresult as crud
from app.core.deps import current_active_user, get_async_session
from app.models.indikator import Indikator
from app.schemas.mobilitaetscheck_eingabe_ziel_unter import (
    MobilitaetscheckEingabeZielUnterCreate as CreateSchema,
    MobilitaetscheckEingabeZielUnterUpdate as UpdateSchema,
    MobilitaetscheckEingabeZielUnterRead as ReadSchema,
)

router = APIRouter()

association_fields = ({"indikator_ids": (Indikator, "indikators")},)


@router.get(
    "/{id}",
    response_model=ReadSchema,
    dependencies=[Depends(current_active_user)],
)
async def get_mobility_subresult(
    id: int, db: AsyncSession = Depends(get_async_session)
):
    return await crud.get(db, id)


@router.post(
    "",
    status_code=status.HTTP_201_CREATED,
    response_model=ReadSchema,
    dependencies=[Depends(current_active_user)],
)
async def create_mobility_subresult(
    obj_in: CreateSchema,
    db: AsyncSession = Depends(get_async_session),
):
    return await crud.create_with_associations(
        db=db,
        obj_in=obj_in,
        association_fields=association_fields,
    )


@router.patch(
    "/{id}",
    response_model=ReadSchema,
    dependencies=[Depends(current_active_user)],
)
async def update_mobility_subresult(
    id: int,
    updates: UpdateSchema,
    db: AsyncSession = Depends(get_async_session),
):
    return await crud.update_with_associations(
        db=db,
        id=id,
        obj_in=updates,
        association_fields=association_fields,
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
