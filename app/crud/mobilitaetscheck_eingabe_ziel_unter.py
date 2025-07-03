from app.crud.base import CRUDBase
from app.models.mobilitaetscheck_eingabe_ziel_unter import (
    MobilitaetscheckEingabeZielUnter as Model,
)
from app.schemas.mobilitaetscheck_eingabe_ziel_unter import (
    MobilitaetscheckEingabeZielUnterCreate as CreateSchema,
    MobilitaetscheckEingabeZielUnterUpdate as UpdateSchema,
)


class CRUDMobilitySubresult(CRUDBase[Model, CreateSchema, UpdateSchema]):
    def __init__(self):
        super().__init__(Model)


crud_mobility_subresult = CRUDMobilitySubresult()
