from app.crud.base import CRUDBase
from app.models.indicator import Indicator as Model
from app.schemas.indicator import (
    IndicatorCreate as CreateSchema,
    IndicatorUpdate as UpdateSchema,
)


class CRUDIndicator(CRUDBase[Model, CreateSchema, UpdateSchema]):
    def __init__(self):
        super().__init__(Model)


crud_indicator = CRUDIndicator()
