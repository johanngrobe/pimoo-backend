from app.crud.base import CRUDBase
from app.models.mobilitaetscheck_auswirkung_raeumlich import (
    MobilitaetscheckAuswirkungRaeumlich as Model,
)
from app.schemas.mobilitaetscheck_auswirkung_raeumlich import (
    MobilitaetscheckAuswirkungRaeumlichCreate as CreateSchema,
    MobilitaetscheckAuswirkungRaeumlichUpdate as UpdateSchema,
)


class CRUDMobilitaetscheckAuswirkungRaeumlich(
    CRUDBase[Model, CreateSchema, UpdateSchema]
):
    def __init__(self):
        super().__init__(Model)


crud_mobilitaetscheck_auswirkung_raeumlich = CRUDMobilitaetscheckAuswirkungRaeumlich()
