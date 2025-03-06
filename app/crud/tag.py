from app.crud.base import CRUDBase
from app.models.tag import Tag as Model
from app.schemas.tag import TagCreate as CreateSchema, TagUpdate as UpdateSchema


class CRUDTag(CRUDBase[Model, CreateSchema, UpdateSchema]):
    def __init__(self):
        super().__init__(Model)


crud_tag = CRUDTag()
