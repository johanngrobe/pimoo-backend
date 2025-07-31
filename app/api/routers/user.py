from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from typing import List

from app.core.deps import current_superuser, get_async_session
from app.crud.user import crud_user as crud
from app.models.user import User
from app.schemas.user import UserRead as ReadSchema

router = APIRouter()


@router.get(
    "",
    response_model=List[ReadSchema],
    dependencies=[Depends(current_superuser)],
)
async def get_all_users_in_municipality(
    db: AsyncSession = Depends(get_async_session),
    user: User = Depends(current_superuser),
):

    instances = await crud.get_all(
        db=db,
        gemeinde_id=user.gemeinde_id,
        sort_params=[("name", "asc")],
    )
    return instances
