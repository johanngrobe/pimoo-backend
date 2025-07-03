from typing import Any

from sqlalchemy.ext.asyncio import AsyncSession

from app.crud.base_eingabe import CRUDEingabe
from app.models.mobilitaetscheck_eingabe import MobilitaetscheckEingabe as Model
from app.models.user import User
from app.schemas.mobilitaetscheck_eingabe import (
    MobilitaetscheckEingabeCreate as CreateSchema,
    MobilitaetscheckEingabeUpdate as UpdateSchema,
)
from app.services.pdf.mobilitaetscheck_pdf import MobilitaetscheckPDF


class CRUDMobilitySubmission(CRUDEingabe[Model, CreateSchema, UpdateSchema]):
    def __init__(self):
        super().__init__(Model)

    async def copy(self, db: AsyncSession, id: int, user: User) -> Model:
        exclude = ["id", "erstellt_am"]

        updates = {
            "erstellt_von": user.id,
            "zuletzt_bearbeitet_von": user.id,
            "veroeffentlicht": False,
        }

        nested_attributes = {
            "eingabe_ziel_ober": ["eingabe_ziel_unter"],
        }

        return await super().copy(
            db=db,
            id=id,
            updates=updates,
            exclude=exclude,
            nested_attributes=nested_attributes,
        )

    async def export(self, db: AsyncSession, id: int):
        return await super().export(db=db, id=id, PDF=MobilitaetscheckPDF)


crud_mobility_submission = CRUDMobilitySubmission()
