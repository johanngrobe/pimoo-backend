from app.crud.base import CRUDBase
from app.models.mobilitaetscheck_ziel_unter import MobilitaetscheckZielUnter as Model

from app.schemas.mobilitaetscheck_ziel_unter import (
    MobilitaetscheckZielUnterCreate as CreateSchema,
    MobilitaetscheckZielUnterUpdate as Updateschema,
)


class CRUDSubObjective(CRUDBase[Model, CreateSchema, Updateschema]):
    def __init__(self):
        super().__init__(Model)


crud_sub_objective = CRUDSubObjective()
