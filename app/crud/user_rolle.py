from app.crud.base import CRUDBase
from app.models.user_rolle import UserRolle as Model
from app.schemas.user_rolle import (
    UserRolleCreate as CreateSchema,
    UserRolleUpdate as UpdateSchema,
)


class CRUDUserRolle(CRUDBase[Model, CreateSchema, UpdateSchema]):
    def __init__(self):
        super().__init__(Model)


crud_user_rolle = CRUDUserRolle()
