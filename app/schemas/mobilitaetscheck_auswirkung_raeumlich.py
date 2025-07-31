from pydantic import BaseModel, Field, ConfigDict


class MobilitaetscheckAuswirkungRaeumlichBase(BaseModel):
    name: str = Field(..., description="Name der räumlichen Auswirkung")


class MobilitaetscheckAuswirkungRaeumlichCreate(
    MobilitaetscheckAuswirkungRaeumlichBase
):
    pass


class MobilitaetscheckAuswirkungRaeumlichUpdate(
    MobilitaetscheckAuswirkungRaeumlichBase
):
    pass


class MobilitaetscheckAuswirkungRaeumlichRead(MobilitaetscheckAuswirkungRaeumlichBase):
    model_config = ConfigDict(from_attributes=True)

    id: int = Field(..., description="ID der räumlichen Auswirkung")
