from typing import List

from fastapi import APIRouter, Depends, status
from fastapi.responses import StreamingResponse
from sqlalchemy.ext.asyncio import AsyncSession

from app.crud.klimacheck_eingabe import crud_klimacheck_eingabe as crud
from app.core.deps import current_active_user, get_async_session
from app.models.user import User
from app.schemas.klimacheckEingabe import (
    KlimacheckEingabeCreate as CreateSchema,
    KlimacheckEingabeUpdate as UpdateSchema,
    KlimacheckEingabeRead as ReadSchema,
    KlimacheckEingabeFilter as FilterSchema,
)
from app.utils.auth_util import check_user_authorization

router = APIRouter()


@router.get("", response_model=List[ReadSchema])
async def get_climate_submissions(
    db: AsyncSession = Depends(get_async_session),
    user: User = Depends(current_active_user),
):
    sort_params = [("erstellt_am", "desc")]

    return await crud.get_by_key(
        db=db,
        key="gemeinde_id",
        value=user.gemeinde_id,
        sort_params=sort_params,
    )


@router.get("/nach-parametern", response_model=List[ReadSchema])
async def filter_climate_submissions(
    user_rolle: bool = None,
    user_id: bool = None,
    veroeffentlicht: bool = None,
    db: AsyncSession = Depends(get_async_session),
    user: User = Depends(current_active_user),
):
    filters = FilterSchema(
        user_rolle=user_rolle, user_id=user_id, veroeffentlicht=veroeffentlicht
    )
    keys = {
        "autor.rolle": user.rolle if filters.user_rolle else None,
        "veroeffentlicht": filters.veroeffentlicht,
        "erstellt_von": user.id if filters.user_id else None,
    }
    # Remove None values from keys
    keys = {k: v for k, v in keys.items() if v is not None}

    sort_params = [("erstellt_am", "desc")]

    return await crud.get_by_multi_keys(db=db, keys=keys, sort_params=sort_params)


@router.get("/{id}", response_model=ReadSchema)
async def get_climate_submission(
    id: int,
    db: AsyncSession = Depends(get_async_session),
    user: User = Depends(current_active_user),
):

    instance = await crud.get(db, id)
    check_user_authorization(user, instance.gemeinde_id)
    return instance


@router.post("/duplizieren/{id}", response_model=ReadSchema)
async def klimacheck_eingabe_duplizieren(
    id: int,
    db: AsyncSession = Depends(get_async_session),
    user: User = Depends(current_active_user),
):
    instance = await crud.get(db, id)
    check_user_authorization(user, instance.gemeinde)
    return await crud.copy(db, id, user)


@router.get("/export/{id}", status_code=status.HTTP_201_CREATED)
async def export_climate_submission(
    id: int,
    db: AsyncSession = Depends(get_async_session),
    user: User = Depends(current_active_user),
):
    instance = await crud.get(db, id)
    check_user_authorization(user, instance.gemeinde_id)
    export = await crud.export(db, id)

    filename = f"klimacheck_{id}.pdf"
    headers = {"Content-Disposition": f"attachment; filename={filename}"}
    return StreamingResponse(export, media_type="application/pdf", headers=headers)


@router.post("", status_code=status.HTTP_201_CREATED, response_model=ReadSchema)
async def create_climate_submission(
    submission: CreateSchema,
    db: AsyncSession = Depends(get_async_session),
    user: User = Depends(current_active_user),
):

    return await crud.create(db, submission, user)


@router.patch("/{id}", response_model=ReadSchema)
async def update_climate_submission(
    id: int,
    updates: UpdateSchema,
    db: AsyncSession = Depends(get_async_session),
    user: User = Depends(current_active_user),
):
    instance = await crud.get(db, id)
    check_user_authorization(user, instance.gemeinde_id)
    return await crud.update(db, id, updates, user)


@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_climate_submission(
    id: int,
    db: AsyncSession = Depends(get_async_session),
    user: User = Depends(current_active_user),
):
    instance = await crud.get(db, id)
    check_user_authorization(user, instance.gemeinde_id)
    await crud.delete(db, id)
