from sqlalchemy.ext.asyncio import AsyncSession

from app.crud.submission_crud import CRUDSubmission
from app.models import ClimateSubmission, User
from app.schemas import ClimateSubmissionCreate, ClimateSubmissionUpdate
from app.services.pdf import ClimateSubmissionPDF


class CRUDClimateSubmission(
    CRUDSubmission[ClimateSubmission, ClimateSubmissionCreate, ClimateSubmissionUpdate]
):
    def __init__(self):
        super().__init__(ClimateSubmission)

    async def get_all(self, db: AsyncSession, user: User) -> ClimateSubmission:
        return await super().get_by_key(
            db=db,
            key="municipality_id",
            value=user.municipality_id,
            sort_params=[("created_at", "desc")],
        )

    async def copy(self, db: AsyncSession, id: int, user: User) -> ClimateSubmission:
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
