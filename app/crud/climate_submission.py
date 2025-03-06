from sqlalchemy.ext.asyncio import AsyncSession

from app.crud.base_submission import CRUDSubmission
from app.models.climate_submission import ClimateSubmission as Model
from app.models.user import User
from app.schemas.climate_submission import (
    ClimateSubmissionCreate as CreateSchema,
    ClimateSubmissionUpdate as UpdateSchema,
)
from app.services.pdf import ClimateSubmissionPDF


class CRUDClimateSubmission(CRUDSubmission[Model, CreateSchema, UpdateSchema]):
    def __init__(self):
        super().__init__(Model)

    async def copy(self, db: AsyncSession, id: int, user: User) -> Model:
        exclude = ["id", "created_at"]

        updates = {
            "created_by": user.id,
            "last_edited_by": user.id,
            "is.published": False,
        }

        return await super().copy(db=db, id=id, updates=updates, exclude=exclude)

    async def export(self, db: AsyncSession, id: int):
        return await super().export(db=db, id=id, PDF=ClimateSubmissionPDF)


crud_climate_submission = CRUDClimateSubmission()
