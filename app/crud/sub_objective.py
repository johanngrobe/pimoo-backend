from typing import List, Union

from app.crud.base import CRUDBase
from app.models.sub_objective import SubObjective as Model
from app.models.user import User
from app.schemas.sub_objective import (
    SubObjectiveCreate as CreateSchema,
    SubObjectiveUpdate as Updateschema,
)


class CRUDSubObjective(CRUDBase[Model, CreateSchema, Updateschema]):
    def __init__(self):
        super().__init__(Model)

    async def get_all(self, db, user: User) -> List[Model]:

        sort_params = [("main_objective.no", "asc"), ("no", "asc")]

        return await super().get_by_key(
            db=db,
            key="municipality_id",
            value=user.municipality_id,
            sort_params=sort_params,
        )


crud_sub_objective = CRUDSubObjective()
