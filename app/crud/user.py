from app.crud.base import CRUDBase
from app.models.user import User as Model
from app.schemas.user import (
    UserCreate as CreateSchema,
    UserUpdate as UpdateSchema,
)


class CRUDUser(CRUDBase[Model, CreateSchema, UpdateSchema]):
    def __init__(self):
        super().__init__(Model)


crud_user = CRUDUser()
