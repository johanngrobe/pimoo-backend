from app.crud.base_crud import CRUDBase
from app.models import Indicator
from app.schemas import IndicatorCreate, IndicatorUpdate

class CRUDIndicator(CRUDBase[Indicator, IndicatorCreate, IndicatorUpdate]):
    def __init__(self):
        super().__init__(Indicator)

crud_indicator = CRUDIndicator()

