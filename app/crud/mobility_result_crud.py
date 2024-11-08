from app.crud.base_crud import CRUDBase
from app.models import MobilityResult
from app.schemas import MobilityResultCreate, MobilityResultUpdate


class CRUDMobilityResult(
    CRUDBase[MobilityResult, MobilityResultCreate, MobilityResultUpdate]
):
    def __init__(self):
        super().__init__(MobilityResult)


crud_mobility_result = CRUDMobilityResult()
