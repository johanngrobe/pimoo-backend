from typing import List

from fastapi import APIRouter, Depends, status
from fastapi.responses import StreamingResponse
from sqlalchemy.ext.asyncio import AsyncSession

from app.crud.climate_submission_crud import crud_climate_submission as crud
from app.dependencies import current_active_user, get_async_session
from app.models import ClimateSubmission, User
from app.schemas import (
    ClimateSubmissionCreate,
    ClimateSubmissionUpdate,
    ClimateSubmissionRead,
    ClimateSubmissionFilter,
)
from app.utils.auth_util import check_user_authorization

router = APIRouter()


@router.get("", response_model=List[ClimateSubmissionRead])
async def get_climate_submissions(
    db: AsyncSession = Depends(get_async_session),
    user: User = Depends(current_active_user),
):
    return await crud.get_all(
        db=db,
        user=user,
    )


@router.post("/filter", response_model=List[ClimateSubmissionRead])
async def filter_climate_submissions(
    filters: ClimateSubmissionFilter,
    db: AsyncSession = Depends(get_async_session),
    user: User = Depends(current_active_user),
):
    keys = {
        "author.role": user.role if filters.by_user_role else None,
        "is_published": filters.is_published,
        "created_by": user.id if filters.by_user_id else None,
    }
    # Remove None values from keys
    keys = {k: v for k, v in keys.items() if v is not None}

    sort_params = [("created_at", "desc")]

    return await crud.get_by_multi_keys(db=db, keys=keys, sort_params=sort_params)


@router.get("/{id}", response_model=ClimateSubmissionRead)
async def get_climate_submission(
    id: int,
    db: AsyncSession = Depends(get_async_session),
    user: User = Depends(current_active_user),
):

    instance = await crud.get(db, id)
    check_user_authorization(user, instance.municipality_id)
    return instance


@router.post("/copy/{id}", response_model=ClimateSubmissionRead)
async def copy_climate_submission(
    id: int,
    db: AsyncSession = Depends(get_async_session),
    user: User = Depends(current_active_user),
):
    instance = await crud.get(db, id)
    check_user_authorization(user, instance.municipality_id)
    return await crud.copy(db, id, user)


@router.get("/export/{id}", status_code=status.HTTP_201_CREATED)
async def export_climate_submission(
    id: int,
    db: AsyncSession = Depends(get_async_session),
    user: User = Depends(current_active_user),
):
    instance = await crud.get(db, id)
    check_user_authorization(user, instance.municipality_id)
    export = await crud.export(db, id)

    filename = f"klimacheck{id}.pdf"
    headers = {"Content-Disposition": f"attachment; filename={filename}"}
    return StreamingResponse(export, media_type="application/pdf", headers=headers)


@router.post(
    "", status_code=status.HTTP_201_CREATED, response_model=ClimateSubmissionRead
)
async def create_climate_submission(
    submission: ClimateSubmissionCreate,
    db: AsyncSession = Depends(get_async_session),
    user: User = Depends(current_active_user),
):

    return await crud.create(db, submission, user)


@router.patch("/{id}", response_model=ClimateSubmissionRead)
async def update_climate_submission(
    id: int,
    updates: ClimateSubmissionUpdate,
    db: AsyncSession = Depends(get_async_session),
    user: User = Depends(current_active_user),
):
    instance = await crud.get(db, id)
    check_user_authorization(user, instance.municipality_id)
    return await crud.update(db, id, updates, user)


@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_climate_submission(
    id: int,
    db: AsyncSession = Depends(get_async_session),
    user: User = Depends(current_active_user),
):
    instance = await crud.get(db, id)
    check_user_authorization(user, instance.municipality_id)
    await crud.delete(db, id)
