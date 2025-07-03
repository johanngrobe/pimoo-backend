from sqlalchemy.ext.asyncio import AsyncSession

from app.crud.base_eingabe import CRUDEingabe
from app.models.klimacheckEingabe import KlimacheckEingabe as Model
from app.models.user import User
from app.schemas.klimacheckEingabe import (
    KlimacheckEingabeCreate as CreateSchema,
    KlimacheckEingabeUpdate as UpdateSchema,
)
from app.services.pdf.klimacheck_pdf import KlimacheckPDF


class CRUDKlimacheckEingabe(CRUDEingabe[Model, CreateSchema, UpdateSchema]):
    def __init__(self):
        super().__init__(Model)

    async def copy(self, db: AsyncSession, id: int, user: User) -> Model:
        exclude = ["id", "erstellt_von"]

        updates = {
            "erstellt_von": user.id,
            "zuletzt_bearbeitet_von": user.id,
            "veroeffentlicht": False,
        }

        return await super().copy(db=db, id=id, updates=updates, exclude=exclude)

    async def export(self, db: AsyncSession, id: int):
        return await super().export(db=db, id=id, PDF=KlimacheckPDF)


crud_klimacheck_eingabe = CRUDKlimacheckEingabe()
