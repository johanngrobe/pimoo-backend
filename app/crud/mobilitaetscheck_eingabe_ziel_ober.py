from app.crud.base import CRUDBase
from app.models.mobilitaetscheck_eingabe_ziel_ober import (
    MobilitaetscheckEingabeZielOber as Model,
)
from app.schemas.mobilitaetscheck_eingabe_ziel_ober import (
    MobilitaetscheckEingabeZielOberCreate as CreateSchema,
    MobilitaetscheckEingabeZielOberUpdate as UpdateSchema,
)


class CRUDMobilityResult(CRUDBase[Model, CreateSchema, UpdateSchema]):
    def __init__(self):
        super().__init__(Model)


crud_mobility_result = CRUDMobilityResult()
