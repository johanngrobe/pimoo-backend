from app.crud.base import CRUDBase
from app.models.klimacheck_auswirkung_dauer import KlimacheckAuswirkungDauer as Model
from app.schemas.klimacheck_auswirkung_dauer import (
    KlimacheckAuswirkungDauerCreate as CreateSchema,
    KlimacheckAuswirkungDauerUpdate as UpdateSchema,
)


class CRUDKlimacheckAuswirkungDauer(CRUDBase[Model, CreateSchema, UpdateSchema]):
    def __init__(self):
        super().__init__(Model)


crud_klimacheck_auswirkung_dauer = CRUDKlimacheckAuswirkungDauer()
