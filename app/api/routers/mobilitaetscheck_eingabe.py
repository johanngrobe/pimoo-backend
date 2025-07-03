from typing import List

from fastapi import APIRouter, Depends, status
from fastapi.responses import StreamingResponse
from sqlalchemy.ext.asyncio import AsyncSession

from app.crud.mobilitaetscheck_eingabe import crud_mobility_submission as crud
from app.core.deps import current_active_user, get_async_session
from app.models.user import User
from app.schemas.mobilitaetscheck_eingabe import (
    MobilitaetscheckEingabeCreate as CreateSchema,
    MobilitaetscheckEingabeUpdate as UpdateSchema,
    MobilitaetscheckEingabeRead as ReadSchema,
    MobilitaetscheckEingabeFilter as FilterSchema,
)
from app.utils.auth_util import check_user_authorization

router = APIRouter()


@router.get("", response_model=List[ReadSchema], status_code=status.HTTP_200_OK)
async def get_mobility_submissions(
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


@router.get(
    "/nach-parametern",
    response_model=List[ReadSchema],
    status_code=status.HTTP_200_OK,
)
async def filter_mobility_submissions(
    user_rolle: bool = None,
    veroeffentlicht: bool = None,
    user_id: bool = None,
    db: AsyncSession = Depends(get_async_session),
    user: User = Depends(current_active_user),
):
    schema = FilterSchema(
        user_rolle=user_rolle,
        user_id=user_id,
        veroeffentlicht=veroeffentlicht,
    )
    # create a dictionary of keys to filter by
    keys = {
        "autor.rolle": user.rolle if schema.user_rolle else None,
        "veroeffentlicht": schema.veroeffentlicht,
        "erstellt_von": user.id if schema.user_id else None,
    }
    # Remove None values from keys
    keys = {k: v for k, v in keys.items() if v is not None}

    sort_params = [("erstellt_am", "desc")]

    return await crud.get_by_multi_keys(db=db, keys=keys, sort_params=sort_params)


@router.get("/{id}", response_model=ReadSchema, status_code=status.HTTP_200_OK)
async def get_mobility_submission(
    id: int,
    db: AsyncSession = Depends(get_async_session),
    user: User = Depends(current_active_user),
):
    instance = await crud.get(db, id)
    check_user_authorization(user, instance.gemeinde_id)
    return instance


@router.post(
    "/duplizieren/{id}",
    response_model=ReadSchema,
    status_code=status.HTTP_201_CREATED,
)
async def copy_mobility_submission(
    id: int,
    db: AsyncSession = Depends(get_async_session),
    user: User = Depends(current_active_user),
):
    instance = await crud.get(db, id)
    check_user_authorization(user, instance.gemeinde_id)
    return await crud.copy(db, id, user)


@router.get("/export/{id}", status_code=status.HTTP_201_CREATED)
async def export_mobility_submission(
    id: int,
    db: AsyncSession = Depends(get_async_session),
    user: User = Depends(current_active_user),
):
    instance = await crud.get(db, id)
    check_user_authorization(user, instance.gemeinde_id)
    export = await crud.export(db, id)

    filename = f"mobilitaetscheck_{id}.pdf"
    headers = {"Content-Disposition": f"attachment; filename={filename}"}
    return StreamingResponse(export, media_type="application/pdf", headers=headers)


@router.post("", response_model=ReadSchema, status_code=status.HTTP_201_CREATED)
async def create_mobility_submission(
    submission: CreateSchema,
    db: AsyncSession = Depends(get_async_session),
    user: User = Depends(current_active_user),
):
    return await crud.create(db, submission, user)


@router.patch("/{id}", response_model=ReadSchema, status_code=status.HTTP_202_ACCEPTED)
async def update_mobility_submission(
    id: int,
    updates: UpdateSchema,
    db: AsyncSession = Depends(get_async_session),
    user: User = Depends(current_active_user),
):
    instance = await crud.get(db, id)
    check_user_authorization(user, instance.gemeinde_id)
    return await crud.update(db, id, updates, user)


@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_mobility_submission(
    id: int,
    db: AsyncSession = Depends(get_async_session),
    user: User = Depends(current_active_user),
):
    instance = await crud.get(db, id)
    check_user_authorization(user, instance.gemeinde_id)
    return await crud.delete(db, id)
