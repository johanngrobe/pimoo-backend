from app.crud.base import CRUDBase
from app.models.gemeinde_gebiet import GemeindeGebiet as Model
from app.schemas.gemeinde_gebiet import (
    GemeindeGebietCreate as CreateSchema,
    GemeindeGebietUpdate as UpdateSchema,
)


class CRUDGemeindeGebiet(CRUDBase[Model, CreateSchema, UpdateSchema]):
    def __init__(self):
        super().__init__(Model)


crud_gemeinde_gebiet = CRUDGemeindeGebiet()
