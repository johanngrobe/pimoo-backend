from app.crud.base import CRUDBase
from app.models.gemeinde import Gemeinde as Model
from app.schemas.gemeinde import (
    GemeindeCreate as CreateSchema,
    GemeindeUpdate as UpdateSchema,
)


class CRUDGemeinde(CRUDBase[Model, CreateSchema, UpdateSchema]):
    def __init__(self):
        super().__init__(Model)


crud_gemeinde = CRUDGemeinde()
