from pydantic import BaseModel, Field, ConfigDict


class KlimacheckAuswirkungDauerBase(BaseModel):
    name: str = Field(..., description="Name der Auswirkungsdauer")
    alt_name: str = Field(..., description="Dauer der Auswirkung")


class KlimacheckAuswirkungDauerCreate(KlimacheckAuswirkungDauerBase):
    pass


class KlimacheckAuswirkungDauerUpdate(KlimacheckAuswirkungDauerBase):
    pass


class KlimacheckAuswirkungDauerRead(KlimacheckAuswirkungDauerBase):
    model_config = ConfigDict(from_attributes=True)

    id: int = Field(..., description="ID der Auswirkungsdauer")
