from app.crud.base import CRUDBase
from app.models.klimacheck_klimarelevanz import KlimacheckKlimarelevanz as Model
from app.schemas.klimacheck_klimarelevanz import (
    KlimacheckKlimarelevanzCreate as CreateSchema,
    KlimacheckKlimarelevanzUpdate as UpdateSchema,
)


class CRUDKlimacheckKlimarelevanz(CRUDBase[Model, CreateSchema, UpdateSchema]):
    def __init__(self):
        super().__init__(Model)


crud_klimacheck_klimarelevanz = CRUDKlimacheckKlimarelevanz()
