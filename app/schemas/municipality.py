from pydantic import BaseModel, ConfigDict



class MunicipalityBase(BaseModel):
    name: str

class MunicipalityOut(MunicipalityBase):
    model_config = ConfigDict(from_attributes=True)

    id: int