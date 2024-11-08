from typing import List

from fastapi import APIRouter, Depends, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.crud.tag_crud import crud_tag as crud
from app.dependencies import current_active_user, get_async_session
from app.models import User
from app.schemas import TagCreate, TagUpdate, TagRead
from app.utils.auth_util import check_user_authorization

router = APIRouter()


@router.get("", response_model=List[TagRead])
async def get_tags(
    db: AsyncSession = Depends(get_async_session),
    user: User = Depends(current_active_user),
):
    return await crud.get_all(db, user.municipality_id)


@router.get("/{id}", response_model=TagRead)
async def get_tag(
    id: int,
    db: AsyncSession = Depends(get_async_session),
    user: User = Depends(current_active_user),
):

    tag = await crud.get(db, id)
    check_user_authorization(user, tag.municipality_id)
    return tag


@router.post("", status_code=status.HTTP_201_CREATED)
async def create_tag(
    tag: TagCreate,
    db: AsyncSession = Depends(get_async_session),
    user: User = Depends(current_active_user),
):
    return await crud.create(db, tag, user)


@router.patch("/{id}", response_model=TagRead)
async def update_tag(
    id: int,
    updates: TagUpdate,
    db: AsyncSession = Depends(get_async_session),
    user: User = Depends(current_active_user),
):

    tag = await crud.get(db, id)
    check_user_authorization(user, tag.municipality_id)
    return await crud.update(db, id, updates)


@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_tag(
    id: int,
    db: AsyncSession = Depends(get_async_session),
    user: User = Depends(current_active_user),
):

    tag = await crud.get(db, id)
    check_user_authorization(user, tag.municipality_id)
    await crud.delete(db, id)
