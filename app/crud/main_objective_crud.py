from typing import List, Optional, Union

from sqlalchemy import Column
from sqlalchemy.ext.asyncio import AsyncSession

from app.crud.base_crud import CRUDBase
from app.models import MainObjective, User
from app.schemas import MainObjectiveCreate, MainObjectiveUpdate


class CRUDMainObjective(
    CRUDBase[MainObjective, MainObjectiveCreate, MainObjectiveUpdate]
):
    def __init__(self):
        super().__init__(MainObjective)

    async def get_all(self, db: AsyncSession, user: User) -> List[MainObjective]:
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
