from app.crud.base import CRUDBase
from app.models.mobilitaetscheck_ziel_ober import MobilitaetscheckZielOber as Model
from app.schemas.mobilitaetscheck_ziel_ober import (
    MobilitaetscheckZielOberCreate as CreateSchema,
    MobilitaetscheckZielOberUpdate as UpdateSchema,
)


class CRUDMainObjective(CRUDBase[Model, CreateSchema, UpdateSchema]):
    def __init__(self):
        super().__init__(Model)


crud_main_objective = CRUDMainObjective()
