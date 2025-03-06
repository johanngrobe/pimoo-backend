from app.crud.base import CRUDBase
from app.models.text_block import TextBlock as Model
from app.schemas.text_block import (
    TextBlockCreate as CreateSchema,
    TextBlockUpdate as UpdateSchema,
)


class CRUDTextBlock(CRUDBase[Model, CreateSchema, UpdateSchema]):
    def __init__(self):
        super().__init__(Model)


crud_text_block = CRUDTextBlock()
