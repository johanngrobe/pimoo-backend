from typing import Any

from sqlalchemy.ext.asyncio import AsyncSession

from app.crud.submission_crud import CRUDSubmission
from app.models import MobilitySubmission, User
from app.schemas import MobilitySubmissionCreate, MobilitySubmissionUpdate
from app.services.pdf import MobilitySubmissionPDF


class CRUDMobilitySubmission(
    CRUDSubmission[
        MobilitySubmission, MobilitySubmissionCreate, MobilitySubmissionUpdate
    ]
):
    def __init__(self):
        super().__init__(MobilitySubmission)

    async def get_all(self, db: AsyncSession, user: User) -> MobilitySubmission:
        return await super().get_by_key(
            db=db,
            key="municipality_id",
            value=user.municipality_id,
            sort_params=[
                ("created_at", "desc"),
            ],
        )

    async def copy(self, db: AsyncSession, id: int, user: User) -> MobilitySubmission:
        exclude = ["id", "created_at"]

        updates = {
            "created_by": user.id,
            "last_edited_by": user.id,
            "is.published": False,
        }

        nested_attributes = {
            "objectives": ["sub_objectives"],
        }

        return await super().copy(
            db=db,
            id=id,
            updates=updates,
            exclude=exclude,
            nested_attributes=nested_attributes,
        )

    async def export(self, db: AsyncSession, id: int):
        return await super().export(db=db, id=id, PDF=MobilitySubmissionPDF)


crud_mobility_submission = CRUDMobilitySubmission()
