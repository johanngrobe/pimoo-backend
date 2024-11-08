from typing import List

from fastapi import APIRouter, Depends, status
from fastapi.responses import StreamingResponse
from sqlalchemy.ext.asyncio import AsyncSession

from app.crud.mobility_submission_crud import crud_mobility_submission as crud
from app.dependencies import current_active_user, get_async_session
from app.models import MobilitySubmission, User
from app.schemas import (
    MobilitySubmissionCreate,
    MobilitySubmissionUpdate,
    MobilitySubmissionRead,
    MobilitySubmissionFilter,
)
from app.utils.auth_util import check_user_authorization

router = APIRouter()


@router.get(
    "", response_model=List[MobilitySubmissionRead], status_code=status.HTTP_200_OK
)
async def get_mobility_submissions(
    db: AsyncSession = Depends(get_async_session),
    user: User = Depends(current_active_user),
):
    return await crud.get_all(
        db=db,
        municipality_id=user.municipality_id,
        order_by=MobilitySubmission.created_at,
        ascending=False,
    )


@router.post(
    "/filter",
    response_model=List[MobilitySubmissionRead],
    status_code=status.HTTP_200_OK,
)
async def filter_mobility_submissions(
    filters: MobilitySubmissionFilter,
    db: AsyncSession = Depends(get_async_session),
    user: User = Depends(current_active_user),
):
    # create a dictionary of keys to filter by
    keys = {
        "author.role": user.role if filters.by_user_role else None,
        "is_published": filters.is_published,
        "created_by": user.id if filters.by_user_id else None,
    }
    # Remove None values from keys
    keys = {k: v for k, v in keys.items() if v is not None}

    return await crud.get_by_multi_keys(db=db, keys=keys)


@router.get(
    "/{id}", response_model=MobilitySubmissionRead, status_code=status.HTTP_200_OK
)
async def get_mobility_submission(
    id: int,
    db: AsyncSession = Depends(get_async_session),
    user: User = Depends(current_active_user),
):
    instance = await crud.get(db, id)
    check_user_authorization(user, instance.municipality_id)
    return instance


@router.post(
    "/copy/{id}",
    response_model=MobilitySubmissionRead,
    status_code=status.HTTP_201_CREATED,
)
async def copy_mobility_submission(
    id: int,
    db: AsyncSession = Depends(get_async_session),
    user: User = Depends(current_active_user),
):
    instance = await crud.get(db, id)
    check_user_authorization(user, instance.municipality_id)
    return await crud.copy(db, id, user)


@router.get("/export/{id}", status_code=status.HTTP_201_CREATED)
async def export_mobility_submission(
    id: int,
    db: AsyncSession = Depends(get_async_session),
    user: User = Depends(current_active_user),
):
    instance = await crud.get(db, id)
    check_user_authorization(user, instance.municipality_id)
    export = await crud.export(db, id)

    filename = f"mobilitaetscheck_{id}.pdf"
    headers = {"Content-Disposition": f"attachment; filename={filename}"}
    return StreamingResponse(export, media_type="application/pdf", headers=headers)


@router.post(
    "", response_model=MobilitySubmissionRead, status_code=status.HTTP_201_CREATED
)
async def create_mobility_submission(
    submission: MobilitySubmissionCreate,
    db: AsyncSession = Depends(get_async_session),
    user: User = Depends(current_active_user),
):
    return await crud.create(db, submission, user)


@router.patch(
    "/{id}", response_model=MobilitySubmissionRead, status_code=status.HTTP_202_ACCEPTED
)
async def update_mobility_submission(
    id: int,
    updates: MobilitySubmissionUpdate,
    db: AsyncSession = Depends(get_async_session),
    user: User = Depends(current_active_user),
):
    instance = await crud.get(db, id)
    check_user_authorization(user, instance.municipality_id)
    return await crud.update(db, id, updates, user)


@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_mobility_submission(
    id: int,
    db: AsyncSession = Depends(get_async_session),
    user: User = Depends(current_active_user),
):
    instance = await crud.get(db, id)
    check_user_authorization(user, instance.municipality_id)
    return await crud.delete(db, id)
