from app.crud.base import CRUDBase
from app.models.municipality import Municipality as Model
from app.schemas.municipality import (
    MunicipalityCreate as CreateSchema,
    MunicipalityUpdate as UpdateSchema,
)


class CRUDMunicipality(CRUDBase[Model, CreateSchema, UpdateSchema]):
    def __init__(self):
        super().__init__(Model)


crud_municipality = CRUDMunicipality()
