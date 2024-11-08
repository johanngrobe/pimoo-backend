from app.crud.base_crud import CRUDBase
from app.models import MobilitySubresult
from app.schemas import MobilitySubResultCreate, MobilitySubResultUpdate


class CRUDMobilitySubresult(
    CRUDBase[MobilitySubresult, MobilitySubResultCreate, MobilitySubResultUpdate]
):
    def __init__(self):
        super().__init__(MobilitySubresult)


crud_mobility_subresult = CRUDMobilitySubresult()
