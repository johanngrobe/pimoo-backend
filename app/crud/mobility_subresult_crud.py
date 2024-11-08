from typing import Any, Optional

from sqlalchemy import select
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.ext.asyncio import AsyncSession

from app.crud.base_crud import CRUDBase
from app.exceptions import DatabaseCommitError
from app.models import Indicator, MobilitySubresult, User
from app.schemas import MobilitySubResultCreate, MobilitySubResultUpdate


class CRUDMobilitySubresult(CRUDBase[MobilitySubresult, MobilitySubResultCreate, MobilitySubResultUpdate]):
    def __init__(self):
        super().__init__(MobilitySubresult)


crud_mobility_subresult = CRUDMobilitySubresult()