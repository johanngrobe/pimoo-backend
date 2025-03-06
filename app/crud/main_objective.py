from app.crud.base import CRUDBase
from app.models.main_objective import MainObjective as Model
from app.schemas.main_objective import (
    MainObjectiveCreate as CreateSchema,
    MainObjectiveUpdate as UpdateSchema,
)


class CRUDMainObjective(CRUDBase[Model, CreateSchema, UpdateSchema]):
    def __init__(self):
        super().__init__(Model)


crud_main_objective = CRUDMainObjective()
