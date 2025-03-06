from app.crud.base import CRUDBase
from app.models.mobility_subresult import MobilitySubresult as Model
from app.schemas.mobility_subresult import (
    MobilitySubResultCreate as CreateSchema,
    MobilitySubResultUpdate as UpdateSchema,
)


class CRUDMobilitySubresult(CRUDBase[Model, CreateSchema, UpdateSchema]):
    def __init__(self):
        super().__init__(Model)


crud_mobility_subresult = CRUDMobilitySubresult()
