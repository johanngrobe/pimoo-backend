from app.crud.base import CRUDBase
from app.models.sub_objective import SubObjective as Model

from app.schemas.sub_objective import (
    SubObjectiveCreate as CreateSchema,
    SubObjectiveUpdate as Updateschema,
)


class CRUDSubObjective(CRUDBase[Model, CreateSchema, Updateschema]):
    def __init__(self):
        super().__init__(Model)


crud_sub_objective = CRUDSubObjective()
