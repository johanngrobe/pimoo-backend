from typing import Any

from sqlalchemy.ext.asyncio import AsyncSession

from app.crud.submission_crud import CRUDSubmission
from app.models import MobilitySubmission, User
from app.schemas import MobilitySubmissionCreate, MobilitySubmissionUpdate
from app.services.pdf import MobilitySubmissionPDF

class CRUDMobilitySubmission(CRUDSubmission[MobilitySubmission, MobilitySubmissionCreate, MobilitySubmissionUpdate]):
    def __init__(self):
        super().__init__(MobilitySubmission)

    async def copy(
        self,
        db: AsyncSession,
        id: int,
        user: User
    ) -> MobilitySubmission:
        exclude = ["id", "created_at"]

        updates = {
            "created_by": user.id,
            "last_edited_by": user.id,
            "is.published": False
        }

        nested_attributes = {
            "objectives": ["sub_objectives"],
        }

        return await super().copy(
            db=db,
            id=id,
            updates=updates,
            exclude=exclude,
            nested_attributes=nested_attributes
        )
    
    async def export(
        self,
        db: AsyncSession,
        id: int
    ):
        return await super().export(
            db=db,
            id=id,
            PDF=MobilitySubmissionPDF
        )


crud_mobility_submission = CRUDMobilitySubmission()
