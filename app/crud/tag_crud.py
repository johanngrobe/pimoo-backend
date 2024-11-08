from app.crud.base_crud import CRUDBase
from app.models import Tag
from app.schemas import TagCreate, TagUpdate

class CRUDTag(CRUDBase[Tag, TagCreate, TagUpdate]):
    def __init__(self):
        super().__init__(Tag)

crud_tag = CRUDTag()