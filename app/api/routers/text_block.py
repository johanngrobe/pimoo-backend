from typing import List

from fastapi import APIRouter, Depends, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.crud.text_block import crud_text_block as crud
from app.dependencies import current_active_user, get_async_session
from app.models.text_block import TextBlock
from app.models.user import User
from app.models.tag import Tag
from app.schemas.text_block import (
    TextBlockCreate as CreateSchema,
    TextBlockUpdate as UpdateSchema,
    TextBlockRead as ReadSchema,
)
from app.utils.auth_util import check_user_authorization

router = APIRouter()


@router.get("", response_model=List[ReadSchema])
async def get_all_text_blocks(
    db: AsyncSession = Depends(get_async_session),
    user: User = Depends(current_active_user),
):
    return await crud.get_all(db, user.municipality_id, TextBlock.label)


@router.get("/{id}", response_model=ReadSchema)
async def get_text_block(
    id: int,
    db: AsyncSession = Depends(get_async_session),
    user: User = Depends(current_active_user),
):
    instance = await crud.get(db, id)
    check_user_authorization(user, instance.municipality_id)
    return instance


@router.post("", status_code=status.HTTP_201_CREATED, response_model=ReadSchema)
async def create_text_block(
    text_block: CreateSchema,
    db: AsyncSession = Depends(get_async_session),
    user: User = Depends(current_active_user),
):
    return await crud.create_with_associations(
        db=db,
        obj_in=text_block,
        user=user,
        association_fields={"tag_ids": (Tag, "tags")},
    )


@router.patch("/{id}", response_model=ReadSchema)
async def update_text_block(
    id: int,
    updates: UpdateSchema,
    db: AsyncSession = Depends(get_async_session),
    user: User = Depends(current_active_user),
):
    instance = await crud.get(db, id)
    check_user_authorization(user, instance.municipality_id)
    return await crud.update_with_associations(
        db=db,
        id=id,
        obj_in=updates,
        user=user,
        association_fields={"tag_ids": (Tag, "tags")},
    )


@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_text_block(
    id: int,
    db: AsyncSession = Depends(get_async_session),
    user: User = Depends(current_active_user),
):
    instance = await crud.get(db, id)
    check_user_authorization(user, instance.municipality_id)
    await crud.delete(db, id)
