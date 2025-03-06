from typing import List, Optional, Union

from sqlalchemy import Column
from sqlalchemy.ext.asyncio import AsyncSession

from app.crud.base import CRUDBase
from app.models.main_objective import MainObjective as Model
from app.models.user import User
from app.schemas.main_objective import (
    MainObjectiveCreate as CreateSchema,
    MainObjectiveUpdate as UpdateSchema,
)


class CRUDMainObjective(CRUDBase[Model, CreateSchema, UpdateSchema]):
    def __init__(self):
        super().__init__(Model)

    async def get_all(self, db: AsyncSession, user: User) -> List[Model]:
        """
        Fetches and sorts MainObjective records.
        """
        # Fetch all records using get_all
        return await self.get_by_key(
            db,
            key="municipality_id",
            value=user.municipality_id,
            sort_params=[("no", "asc"), ("sub_objectives", ("no", "asc"))],
        )


crud_main_objective = CRUDMainObjective()
