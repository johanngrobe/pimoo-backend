from app.crud.base import CRUDBase
from app.models.indikator import Indikator as Model
from app.schemas.indikator import (
    IndikatorCreate as CreateSchema,
    IndikatorUpdate as UpdateSchema,
)


class CRUDIndikator(CRUDBase[Model, CreateSchema, UpdateSchema]):
    def __init__(self):
        super().__init__(Model)


crud_indikator = CRUDIndikator()
