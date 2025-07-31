from pydantic import BaseModel, Field, ConfigDict


class KlimacheckKlimarelevanzBase(BaseModel):
    name: str = Field(..., description="Name der Klimarelevanz")


class KlimacheckKlimarelevanzCreate(KlimacheckKlimarelevanzBase):
    pass


class KlimacheckKlimarelevanzUpdate(KlimacheckKlimarelevanzBase):
    pass


class KlimacheckKlimarelevanzRead(KlimacheckKlimarelevanzBase):
    model_config = ConfigDict(from_attributes=True)

    id: int = Field(..., description="ID der Klimarelevanz")
