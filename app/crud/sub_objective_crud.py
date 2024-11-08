from typing import List, Union

from app.crud.base_crud import CRUDBase
from app.models import SubObjective, User
from app.schemas import SubObjectiveCreate, SubObjectiveUpdate


class CRUDSubObjective(CRUDBase[SubObjective, SubObjectiveCreate, SubObjectiveUpdate]):
    def __init__(self):
        super().__init__(SubObjective)

    async def get_all(self, db, user: User) -> List[SubObjective]:

        sort_params = [("main_objective.no", "asc"), ("no", "asc")]

        return await super().get_by_key(
            db=db,
            key="muncipality_id",
            value=user.muncipality_id,
            sort_params=sort_params,
        )


crud_sub_objective = CRUDSubObjective()
