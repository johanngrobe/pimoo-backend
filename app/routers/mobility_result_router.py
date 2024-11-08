from fastapi import APIRouter, Depends, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.crud.mobility_result_crud import crud_mobility_result as crud
from app.dependencies import current_active_user, get_async_session
from app.schemas import MobilityResultCreate, MobilityResultUpdate, MobilityResultRead

router = APIRouter()

# @router.get(
#     "",
#     response_model=List[MobilityResultRead],
#     dependencies=[Depends(current_active_user)]
# )
# async def get_mobility_results(db: AsyncSession = Depends(get_async_session)):
#     return await crud.get_all(db)


@router.get(
    "/{id}",
    response_model=MobilityResultRead,
    dependencies=[Depends(current_active_user)],
)
async def get_mobility_result(id: int, db: AsyncSession = Depends(get_async_session)):
    await crud.get(db, id)


@router.post(
    "", status_code=status.HTTP_201_CREATED, dependencies=[Depends(current_active_user)]
)
async def create_mobility_result(
    mobility_result: MobilityResultCreate, db: AsyncSession = Depends(get_async_session)
):
    return await crud.create(db, mobility_result)


@router.patch(
    "/{id}",
    response_model=MobilityResultRead,
    dependencies=[Depends(current_active_user)],
)
async def update_mobility_result(
    id: int,
    updates: MobilityResultUpdate,
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
