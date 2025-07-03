from app.crud.base import CRUDBase
from app.models.textblock import Textblock as Model
from app.schemas.textblock import (
    TextblockCreate as CreateSchema,
    TextblockUpdate as UpdateSchema,
)


class CRUDTextblock(CRUDBase[Model, CreateSchema, UpdateSchema]):
    def __init__(self):
        super().__init__(Model)


crud_textblock = CRUDTextblock()
