from app.crud.base_crud import CRUDBase
from app.models import TextBlock
from app.schemas import TextBlockCreate, TextBlockUpdate
from app.models import User
from app.crud.exceptions import DatabaseCommitError, NotFoundError, AuthorizationError
from sqlalchemy.ext.asyncio import AsyncSession

class CRUDTextBlock(CRUDBase[TextBlock, TextBlockCreate, TextBlockUpdate]):
    def __init__(self):
        super().__init__(TextBlock)

crud_text_block = CRUDTextBlock()

