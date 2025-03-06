from app.crud.base import CRUDBase
from app.models.mobility_result import MobilityResult as Model
from app.schemas.mobility_result import (
    MobilityResultCreate as CreateSchema,
    MobilityResultUpdate as UpdateSchema,
)


class CRUDMobilityResult(CRUDBase[Model, CreateSchema, UpdateSchema]):
    def __init__(self):
        super().__init__(Model)


crud_mobility_result = CRUDMobilityResult()
