from app.crud.base_crud import CRUDBase
from app.models import Municipality
from app.schemas import MunicipalityCreate, MunicipalityUpdate

class CRUDMunicipality(CRUDBase[Municipality, MunicipalityCreate, MunicipalityUpdate]):
    def __init__(self):
        super().__init__(Municipality)

crud_municipality = CRUDMunicipality()