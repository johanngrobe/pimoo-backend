from app.crud.base import CRUDBase
from app.models.magistratsvorlage import Magistratsvorlage as Model
from app.schemas.magistratsvorlage import (
    MagistratsvorlageCreate as CreateSchema,
    MagistratsvorlageUpdate as UpdateSchema,
)


class CRUDMagistratsvorlage(CRUDBase[Model, CreateSchema, UpdateSchema]):
    def __init__(self):
        super().__init__(Model)


crud_magistratsvorlage = CRUDMagistratsvorlage()
